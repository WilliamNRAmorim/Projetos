"""Renderiza as PNGs de reserva a partir de assets/mangueira.glb (rasterizador proprio em numpy).

Camera fixa, 1920x1080, fundo transparente. Saidas em assets/:
  mangueira_inteira.png, mangueira_explodida.png,
  mangueira_terminal.png, mangueira_tubo.png, mangueira_tranca.png, mangueira_cobertura.png
Uso: python renderizar.py
"""
import io, json, os, struct
import numpy as np
from PIL import Image, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(AQUI, '..'))
W, H, SS = 1920, 1080, 2
ORDEM = ['terminal', 'tubo', 'tranca', 'cobertura']
GAP = 0.55
INDIGO = np.array([0x63, 0x66, 0xF1]) / 255
SUPERF = np.array([0x10, 0x15, 0x1C]) / 255
LINHA = np.array([0x23, 0x2B, 0x36]) / 255


def s2l(c): return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
def l2s(c): c = np.clip(c, 0, 1); return np.where(c <= 0.0031308, c * 12.92, 1.055 * c ** (1 / 2.4) - 0.055)
def nrm(v): return v / np.maximum(np.linalg.norm(v, axis=-1, keepdims=True), 1e-12)


# ---------------------------------------------------------------- leitura do glb
def ler_glb(caminho):
    d = open(caminho, 'rb').read()
    mg, ver, tot = struct.unpack_from('<III', d, 0)
    assert mg == 0x46546C67 and ver == 2 and tot == len(d)
    jl, _ = struct.unpack_from('<II', d, 12)
    gl = json.loads(d[20:20 + jl])
    bl, _ = struct.unpack_from('<II', d, 20 + jl)
    binc = d[28 + jl:28 + jl + bl]
    tipos = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4}
    dt = {5126: np.float32, 5125: np.uint32, 5123: np.uint16}

    def acc(i):
        a = gl['accessors'][i]; v = gl['bufferViews'][a['bufferView']]
        n = tipos[a['type']]
        arr = np.frombuffer(binc, dt[a['componentType']], a['count'] * n, v.get('byteOffset', 0))
        return arr.reshape(a['count'], n) if n > 1 else arr

    def img(i):
        im = gl['images'][i]; v = gl['bufferViews'][im['bufferView']]
        return Image.open(io.BytesIO(binc[v['byteOffset']:v['byteOffset'] + v['byteLength']])).convert('RGB')

    camadas = {}
    for no in gl['nodes']:
        if 'mesh' not in no: continue
        pr = gl['meshes'][no['mesh']]['primitives'][0]
        at = pr['attributes']; mat = gl['materials'][pr['material']]
        pbr = mat['pbrMetallicRoughness']
        tex = lambda key: img(gl['textures'][key['index']]['source'])
        camadas[no['name']] = dict(
            P=acc(at['POSITION']).astype(np.float64), N=acc(at['NORMAL']).astype(np.float64),
            UV=acc(at['TEXCOORD_0']).astype(np.float64), T=acc(at['TANGENT']).astype(np.float64),
            I=acc(pr['indices']).reshape(-1, 3).astype(np.int64),
            cor=np.array(pbr.get('baseColorFactor', [1, 1, 1, 1])[:3]),
            met=pbr.get('metallicFactor', 1.0), rug=pbr.get('roughnessFactor', 1.0),
            tcor=tex(pbr['baseColorTexture']) if 'baseColorTexture' in pbr else None,
            tnor=tex(mat['normalTexture']) if 'normalTexture' in mat else None,
            material=mat['name'])
    return gl, camadas


# ---------------------------------------------------------------- camera e rasterizacao
def camera(alvo, dist, yaw, pitch, fov_v):
    d = np.array([-np.sin(yaw) * np.cos(pitch), np.sin(pitch), np.cos(yaw) * np.cos(pitch)])
    olho = alvo + d * dist
    f = nrm(alvo - olho); r = nrm(np.cross(f, [0, 1, 0])); u = np.cross(r, f)
    # rolagem: o eixo X da mangueira fica horizontal na imagem, como na prancha
    ang = np.arctan2(u[0], r[0])
    r, u = r * np.cos(ang) + u * np.sin(ang), -r * np.sin(ang) + u * np.cos(ang)
    return dict(olho=olho, f=f, r=r, u=u, foco=(H * SS / 2) / np.tan(fov_v / 2))


def projetar(P, cam):
    q = P - cam['olho']
    z = q @ cam['f']; x = q @ cam['r']; y = q @ cam['u']
    sx = W * SS / 2 + cam['foco'] * x / z
    sy = H * SS / 2 - cam['foco'] * y / z
    return sx, sy, z


def rasterizar(sx, sy, z, I):
    """Devolve por pixel: indice do triangulo (-1 = vazio) e baricentricas perspectiva-corretas."""
    Wp, Hp = W * SS, H * SS
    x0, y0, z0 = sx[I[:, 0]], sy[I[:, 0]], z[I[:, 0]]
    x1, y1, z1 = sx[I[:, 1]], sy[I[:, 1]], z[I[:, 1]]
    x2, y2, z2 = sx[I[:, 2]], sy[I[:, 2]], z[I[:, 2]]
    area = (x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)
    vis = area < -1e-9            # frente anti-horaria no espaco do mundo -> horaria na tela (y para baixo)
    ids = np.nonzero(vis)[0]
    bx0 = np.clip(np.floor(np.minimum(np.minimum(x0, x1), x2)), 0, Wp - 1).astype(np.int64)
    bx1 = np.clip(np.ceil(np.maximum(np.maximum(x0, x1), x2)), 0, Wp - 1).astype(np.int64)
    by0 = np.clip(np.floor(np.minimum(np.minimum(y0, y1), y2)), 0, Hp - 1).astype(np.int64)
    by1 = np.clip(np.ceil(np.maximum(np.maximum(y0, y1), y2)), 0, Hp - 1).astype(np.int64)
    S = np.maximum(bx1 - bx0, by1 - by0) + 1
    frag = []
    for lo, hi in [(0, 2), (2, 4), (4, 8), (8, 16), (16, 32), (32, 64), (64, 128), (128, 256), (256, 4096)]:
        sel = ids[(S[ids] > lo) & (S[ids] <= hi)]
        if len(sel) == 0: continue
        n = hi if hi < 4096 else int(S[sel].max())
        o = np.arange(n)
        passo = max(1, 3_000_000 // (n * n))
        for k in range(0, len(sel), passo):
            t = sel[k:k + passo]
            px = bx0[t][:, None, None] + o[None, None, :]
            py = by0[t][:, None, None] + o[None, :, None]
            cx, cy = px + 0.5, py + 0.5
            ar = area[t][:, None, None]
            w0 = ((x1[t][:, None, None] - cx) * (y2[t][:, None, None] - cy) - (x2[t][:, None, None] - cx) * (y1[t][:, None, None] - cy)) / ar
            w1 = ((x2[t][:, None, None] - cx) * (y0[t][:, None, None] - cy) - (x0[t][:, None, None] - cx) * (y2[t][:, None, None] - cy)) / ar
            w2 = 1 - w0 - w1
            ok = (w0 >= 0) & (w1 >= 0) & (w2 >= 0) & (px <= bx1[t][:, None, None]) & (py <= by1[t][:, None, None])
            ti, yy, xx = np.nonzero(ok)
            if len(ti) == 0: continue
            a0 = w0[ti, yy, xx] / z0[t][ti]; a1 = w1[ti, yy, xx] / z1[t][ti]; a2 = w2[ti, yy, xx] / z2[t][ti]
            iz = a0 + a1 + a2
            frag.append((py[ti, yy, 0] * Wp + px[ti, 0, xx], iz, t[ti], a1 / iz, a2 / iz))
    pix = np.concatenate([f[0] for f in frag]); iz = np.concatenate([f[1] for f in frag])
    tri = np.concatenate([f[2] for f in frag]); b1 = np.concatenate([f[3] for f in frag]); b2 = np.concatenate([f[4] for f in frag])
    o = np.lexsort((-iz, pix))
    pix, tri, b1, b2 = pix[o], tri[o], b1[o], b2[o]
    prim = np.ones(len(pix), bool); prim[1:] = pix[1:] != pix[:-1]
    T = np.full(Wp * Hp, -1, np.int64); B1 = np.zeros(Wp * Hp); B2 = np.zeros(Wp * Hp)
    T[pix[prim]] = tri[prim]; B1[pix[prim]] = b1[prim]; B2[pix[prim]] = b2[prim]
    return T, B1, B2


# ---------------------------------------------------------------- texturas
class Tex:
    def __init__(self, img, srgb):
        self.mips = []
        im = img
        while True:
            a = np.asarray(im, np.float64) / 255
            self.mips.append(s2l(a) if srgb else a * 2 - 1)
            if min(im.size) <= 8: break
            im = im.resize((im.size[0] // 2, im.size[1] // 2), Image.BOX)

    def _bil(self, a, u, v):
        h, w = a.shape[:2]
        x = u * w - 0.5; y = v * h - 0.5
        xi = np.floor(x).astype(np.int64); yi = np.floor(y).astype(np.int64)
        fx = (x - xi)[:, None]; fy = (y - yi)[:, None]
        x0, x1 = xi % w, (xi + 1) % w; y0, y1 = yi % h, (yi + 1) % h
        return (a[y0, x0] * (1 - fx) + a[y0, x1] * fx) * (1 - fy) + (a[y1, x0] * (1 - fx) + a[y1, x1] * fx) * fy

    def amostra(self, u, v, lod):
        lod = np.clip(lod, 0, len(self.mips) - 1)
        l0 = np.floor(lod).astype(int); f = (lod - l0)[:, None]
        out = np.zeros((len(u), 3))
        for l in np.unique(l0):
            m = l0 == l
            a = self._bil(self.mips[l], u[m], v[m])
            b = self._bil(self.mips[min(l + 1, len(self.mips) - 1)], u[m], v[m])
            out[m] = a * (1 - f[m]) + b * f[m]
        return out


def env(R, rug):
    """Estudio simples: softbox longo no alto, rebatedor lateral e chao escuro."""
    k = 0.06 + rug * 0.45
    topo = np.clip((R[:, 1] - 0.45) / k, 0, 1) * np.clip((0.97 - R[:, 1]) / k, 0, 1)
    lado = np.exp(-(((R[:, 0] + 0.55) / (0.25 + k)) ** 2 + ((R[:, 1] - 0.05) / (0.35 + k)) ** 2))
    base = 0.035 + 0.05 * np.clip(R[:, 1], 0, 1)
    return (base + 2.4 * topo + 0.7 * lado)[:, None] * np.array([0.93, 0.97, 1.05])


def aces(x):
    return np.clip((x * (2.51 * x + 0.03)) / (x * (2.43 * x + 0.59) + 0.14), 0, 1)


# ---------------------------------------------------------------- cena
def montar(camadas, explodida):
    """Concatena as camadas (deslocadas ao longo do eixo X se explodida)."""
    Ps, outs, desloc = [], {}, {}
    x_fim = None
    for nome in ORDEM:
        c = camadas[nome]
        if not explodida:
            dx = 0.0
        elif x_fim is None:
            dx = 0.0
        else:
            dx = x_fim + GAP - c['P'][:, 0].min()
        desloc[nome] = dx
        x_fim = c['P'][:, 0].max() + dx
    return desloc


def render(camadas, desloc, estado, cam, centro_dx=0.0):
    """estado[nome] in {'on', 'acento', 'dim'}"""
    Ps, Ns, UVs, Ts, Is, lay = [], [], [], [], [], []
    base = 0
    for li, nome in enumerate(ORDEM):
        c = camadas[nome]
        P = c['P'].copy(); P[:, 0] += desloc[nome] + centro_dx
        Ps.append(P); Ns.append(c['N']); UVs.append(c['UV']); Ts.append(c['T'])
        Is.append(c['I'] + base); lay.append(np.full(len(c['I']), li)); base += len(P)
    P = np.concatenate(Ps); N = np.concatenate(Ns); UV = np.concatenate(UVs); TG = np.concatenate(Ts)
    I = np.concatenate(Is); LAY = np.concatenate(lay)
    sx, sy, z = projetar(P, cam)
    T, B1, B2 = rasterizar(sx, sy, z, I)
    Wp, Hp = W * SS, H * SS
    m = T >= 0
    t = T[m]; b1 = B1[m][:, None]; b2 = B2[m][:, None]; b0 = 1 - b1 - b2
    i0, i1, i2 = I[t, 0], I[t, 1], I[t, 2]
    itp = lambda A: A[i0] * b0 + A[i1] * b1 + A[i2] * b2
    pos = itp(P); n = nrm(itp(N)); uv = itp(UV); tg = itp(TG)
    camada = LAY[t]

    # LOD por derivada de tela das UVs
    uvimg = np.full((Hp, Wp, 2), np.nan); uvimg.reshape(-1, 2)[m] = uv
    du = np.abs(np.diff(uvimg, axis=1, append=np.nan)); dv = np.abs(np.diff(uvimg, axis=0, append=np.nan))
    dd = np.fmin(np.nan_to_num(du, nan=np.inf).max(-1), np.nan_to_num(dv, nan=np.inf).max(-1)).reshape(-1)[m]

    cor = np.zeros((len(t), 3)); met = np.zeros(len(t)); rug = np.zeros(len(t))
    for li, nome in enumerate(ORDEM):
        c = camadas[nome]; k = camada == li
        if not k.any(): continue
        met[k] = c['met']; rug[k] = c['rug']
        if c['tcor'] is not None:
            tx = c.setdefault('_tc', Tex(c['tcor'], True))
            lod = np.log2(np.maximum(np.minimum(dd[k], 0.5) * tx.mips[0].shape[1], 1e-6))
            cor[k] = tx.amostra(uv[k, 0], uv[k, 1], lod) * c['cor']
        else:
            cor[k] = c['cor']
        if c['tnor'] is not None:
            tn = c.setdefault('_tn', Tex(c['tnor'], False))
            lod = np.log2(np.maximum(np.minimum(dd[k], 0.5) * tn.mips[0].shape[1], 1e-6))
            ts = tn.amostra(uv[k, 0], uv[k, 1], lod)
            N0 = n[k]; Tt = nrm(tg[k, :3] - N0 * (tg[k, :3] * N0).sum(1, keepdims=True))
            Bt = np.cross(N0, Tt) * tg[k, 3:4]
            n[k] = nrm(Tt * ts[:, :1] + Bt * ts[:, 1:2] + N0 * ts[:, 2:3])

    V = nrm(cam['olho'] - pos)
    ndv = np.clip((n * V).sum(1), 1e-3, 1)[:, None]
    F0 = 0.04 * (1 - met[:, None]) + cor * met[:, None]
    luzes = [(nrm(np.array([-0.45, 0.85, 0.55])), 2.3), (nrm(np.array([0.75, -0.05, 0.6])), 0.55),
             (nrm(np.array([0.25, 0.55, -0.85])), 1.4)]
    out = 0.05 * cor * (1 - met[:, None])
    expo = 2.0 / np.maximum(rug, 0.05) ** 4 - 2
    for Ld, Li in luzes:
        ndl = np.clip((n * Ld).sum(1), 0, 1)[:, None]
        Hh = nrm(Ld[None, :] + V)
        ndh = np.clip((n * Hh).sum(1), 0, 1)
        vdh = np.clip((V * Hh).sum(1), 0, 1)[:, None]
        Fs = F0 + (1 - F0) * (1 - vdh) ** 5
        spec = ((expo + 8) / (8 * np.pi) * ndh ** expo)[:, None] * Fs
        out = out + Li * ndl * (cor * (1 - met[:, None]) / np.pi * 2.2 + spec * 0.9)
    R = 2 * (n * V).sum(1, keepdims=True) * n - V
    Fe = F0 + (1 - F0) * (1 - ndv) ** 5 * (1 - rug[:, None]) ** 2
    out = out + Fe * env(R, rug) * np.where(met[:, None] > 0.5, 1.0, 0.35)
    srgb = l2s(aces(out * 1.1))

    # destaque e apagado
    rim = (1 - ndv) ** 2.5
    for li, nome in enumerate(ORDEM):
        k = camada == li
        e = estado[nome]
        if e == 'acento':
            srgb[k] = srgb[k] + INDIGO * rim[k] * 0.85
        elif e == 'dim':
            lum = (srgb[k] @ np.array([0.2126, 0.7152, 0.0722]))[:, None]
            srgb[k] = SUPERF * 0.9 + (lum * 0.12) + LINHA * rim[k] * 0.5
    img = np.zeros((Hp * Wp, 4)); img[m, :3] = np.clip(srgb, 0, 1); img[m, 3] = 1
    img = img.reshape(Hp, Wp, 4)
    lay_img = np.full(Hp * Wp, -1); lay_img[m] = camada; lay_img = lay_img.reshape(Hp, Wp)

    # contornos: linha indigo nas camadas em acento, linha discreta nas apagadas
    def contorno(mask, raio):
        im = Image.fromarray((mask * 255).astype(np.uint8))
        d = np.asarray(im.filter(ImageFilter.MaxFilter(raio * 2 + 1))) / 255.0
        return np.clip(d - mask, 0, 1)
    acc = np.isin(lay_img, [ORDEM.index(k) for k, v in estado.items() if v == 'acento']).astype(float)
    dim = np.isin(lay_img, [ORDEM.index(k) for k, v in estado.items() if v == 'dim']).astype(float)

    # reduz para 1920x1080 (pre-multiplicado)
    pm = img.copy(); pm[..., :3] *= pm[..., 3:4]
    pm = pm.reshape(H, SS, W, SS, 4).mean((1, 3))
    acc1 = acc.reshape(H, SS, W, SS).mean((1, 3)); dim1 = dim.reshape(H, SS, W, SS).mean((1, 3))

    camadas_fx = []
    if dim1.any():
        ln = contorno(dim1, 1) * 0.9
        camadas_fx.append((LINHA, ln))
    if acc1.any():
        ln = contorno(acc1, 2)
        g1 = np.asarray(Image.fromarray((acc1 * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(10))) / 255
        g2 = np.asarray(Image.fromarray((acc1 * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(28))) / 255
        glow = np.clip(g1 * 0.55 + g2 * 0.35, 0, 1) * (1 - acc1)
        camadas_fx.append((INDIGO, glow))
        camadas_fx.append((INDIGO, ln * 0.95))
    # objeto por cima dos efeitos
    fundo = np.zeros((H, W, 4))
    for corfx, a in camadas_fx:
        a = a[..., None]
        fundo[..., :3] = corfx * a + fundo[..., :3] * (1 - a)
        fundo[..., 3:] = a + fundo[..., 3:] * (1 - a)
    final = pm + fundo * (1 - pm[..., 3:4])
    rgb = np.where(final[..., 3:4] > 1e-6, final[..., :3] / np.maximum(final[..., 3:4], 1e-6), 0)
    return np.concatenate([rgb, final[..., 3:4]], -1)


def salvar(arr, nome):
    Image.fromarray((np.clip(arr, 0, 1) * 255 + 0.5).astype(np.uint8), 'RGBA').save(os.path.join(ASSETS, nome), optimize=True)
    print('ok', nome)


def main():
    gl, camadas = ler_glb(os.path.join(ASSETS, 'mangueira.glb'))
    desloc = montar(camadas, True)
    xs = np.concatenate([camadas[k]['P'][:, 0] + desloc[k] for k in ORDEM])
    centro = (xs.min() + xs.max()) / 2
    vao = xs.max() - xs.min()
    fov = np.radians(13.0)
    hfov = 2 * np.arctan(np.tan(fov / 2) * W / H)
    dist = (vao / 0.80) / (2 * np.tan(hfov / 2))
    cam = camera(np.array([0.0, 0.0, 0.0]), dist, np.radians(13), np.radians(8), fov)
    dx = -centro                                     # vista explodida centrada no quadro
    sem = {k: 0.0 for k in ORDEM}
    salvar(render(camadas, sem, {k: 'acento' for k in ORDEM}, cam), 'mangueira_inteira.png')
    salvar(render(camadas, desloc, {k: 'acento' for k in ORDEM}, cam, dx), 'mangueira_explodida.png')
    for k in ORDEM:
        est = {j: ('acento' if j == k else 'dim') for j in ORDEM}
        salvar(render(camadas, desloc, est, cam, dx), f'mangueira_{k}.png')


if __name__ == '__main__':
    main()
