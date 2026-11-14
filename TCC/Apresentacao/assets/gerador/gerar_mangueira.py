"""Gera assets/mangueira.glb: mangueira hidraulica trancada de arame, feita so por codigo.

Camadas (um no e um material por camada, todas com origem e eixo comuns):
  terminal  - conexao metalica: rosca macho com assento conico, sextavado, capa prensada e espiga
  tubo      - tubo interno de borracha
  tranca    - reforco de arame trancado (a tranca e textura + normal map, nao geometria)
  cobertura - cobertura externa de borracha

Eixo da mangueira = X. Modelo centrado na origem (centro da caixa envolvente).
Uso: python gerar_mangueira.py   (precisa so de numpy e Pillow)
"""
import io, json, os, struct
import numpy as np
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.normpath(os.path.join(AQUI, '..'))

L = 3.8      # comprimento das camadas da mangueira
X0 = 0.25    # inicio da mangueira dentro da capa do terminal (coordenada antes de centrar)
TUBO = (0.45, 0.60)
TRANCA = (0.61, 0.67)
COBERTURA = (0.70, 0.85)
NSEG = 128
TRANCA_U = 8             # repeticoes do ladrilho em volta (8 x 2 = 16 portadoras por sentido)
TRANCA_ANG = 54.7        # angulo da tranca em relacao ao eixo
TAU = 2 * np.pi


# ---------------------------------------------------------------- geometria
class Malha:
    def __init__(self):
        self.P, self.N, self.UV, self.T, self.I = [], [], [], [], []
        self.n = 0

    def add(self, P, N, UV, T, I):
        self.P.append(P); self.N.append(N); self.UV.append(UV); self.T.append(T)
        self.I.append(I + self.n); self.n += len(P)

    def arrays(self):
        P = np.concatenate(self.P).astype(np.float32)
        N = np.concatenate(self.N).astype(np.float32)
        UV = np.concatenate(self.UV).astype(np.float32)
        T = np.concatenate(self.T).astype(np.float32)
        I = np.concatenate(self.I).astype(np.uint32)
        # enrolamento: frente anti-horaria, coerente com a normal de vertice
        a, b, c = P[I[:, 0]], P[I[:, 1]], P[I[:, 2]]
        fn = np.cross(b - a, c - a)
        vn = N[I[:, 0]] + N[I[:, 1]] + N[I[:, 2]]
        flip = (fn * vn).sum(1) < 0
        I[flip] = I[flip][:, [0, 2, 1]]
        area = np.linalg.norm(fn, axis=1)
        I = I[area > 1e-12]
        return P, N, UV, T, I


def _norm(v):
    return v / np.maximum(np.linalg.norm(v, axis=-1, keepdims=True), 1e-12)


def _quads(rows, cols):
    i = np.arange(rows)[:, None] * (cols + 1) + np.arange(cols)[None, :]
    i = i.ravel()
    a, b, c, d = i, i + 1, i + cols + 2, i + cols + 1
    return np.concatenate([np.stack([a, b, c], 1), np.stack([a, c, d], 1)])


def superficie(m, th, xs, rf, fora=True, uvf=None):
    """Superficie de revolucao r = rf(theta, x). Normais analiticas por diferenca central."""
    TH, X = np.meshgrid(th, xs)
    r = rf(TH, X)
    e = 1e-5
    rth = (rf(TH + e, X) - rf(TH - e, X)) / (2 * e)
    rx = (rf(TH, X + e) - rf(TH, X - e)) / (2 * e)
    c, s = np.cos(TH), np.sin(TH)
    P = np.stack([X, r * c, r * s], -1)
    dth = np.stack([np.zeros_like(r), rth * c - r * s, rth * s + r * c], -1)
    dx = np.stack([np.ones_like(r), rx * c, rx * s], -1)
    N = _norm(np.cross(dth, dx))
    if not fora:
        N = -N
    T = _norm(dth)
    # bitangente glTF = cross(N,T)*w deve apontar para v decrescente (v cresce com x)
    w = np.sign((np.cross(N, T) * -dx).sum(-1))
    w[w == 0] = 1
    if uvf is None:
        UV = np.stack([TH / TAU, (X - xs[0]) / max(xs[-1] - xs[0], 1e-6)], -1)
    else:
        UV = np.stack(uvf(TH, X), -1)
    T4 = np.concatenate([T, w[..., None]], -1)
    m.add(P.reshape(-1, 3), N.reshape(-1, 3), UV.reshape(-1, 2), T4.reshape(-1, 4),
          _quads(len(xs) - 1, len(th) - 1))


def anel(m, x, th, rin, rout, lado, nr=2):
    """Face plana anular em x, normal (lado,0,0). rin/rout: escalares ou funcoes de theta."""
    rin_ = rin(th) if callable(rin) else np.full_like(th, rin)
    rout_ = rout(th) if callable(rout) else np.full_like(th, rout)
    t = np.linspace(0, 1, nr + 1)[:, None]
    R = rin_[None, :] * (1 - t) + rout_[None, :] * t
    TH = np.broadcast_to(th[None, :], R.shape)
    c, s = np.cos(TH), np.sin(TH)
    P = np.stack([np.full_like(R, x), R * c, R * s], -1)
    N = np.zeros_like(P); N[..., 0] = lado
    UV = np.stack([TH / TAU, t.repeat(len(th), 1) * 0.05], -1)
    T4 = np.stack([np.zeros_like(R), -s, c, np.ones_like(R)], -1)
    m.add(P.reshape(-1, 3), N.reshape(-1, 3), UV.reshape(-1, 2), T4.reshape(-1, 4), _quads(nr, len(th) - 1))


def ss(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def terminal():
    m = Malha()
    th = np.linspace(0, TAU, 145)
    ROOT, PASSO, PROF = 0.585, 0.125, 0.06

    def r_rosca(TH, X):
        f = np.mod(X / PASSO - TH / TAU, 1.0)
        perfil = np.clip((1 - np.abs(2 * f - 1)) * 1.35, 0, 1)      # crista truncada
        fade = ss(-1.49, -1.40, X) * (1 - ss(-0.84, -0.76, X))
        r = ROOT + PROF * perfil * fade
        cone = 0.44 + (X + 1.65) / 0.15 * (ROOT - 0.44)              # assento conico na ponta
        return np.where(X < -1.50, cone, r)

    superficie(m, th, np.linspace(-1.65, -0.70, 161), r_rosca)
    anel(m, -1.65, th, 0.30, 0.44, -1)

    # sextavado com chanfro
    xa, xb = -0.70, -0.12
    F = 1.06 * np.cos(np.pi / 6)

    def r_hex(TH, X, c):
        rh = F / np.cos(TH - c)
        rc = 0.93 + 1.0 * np.minimum(X - xa, xb - X)
        return np.minimum(rh, rc)

    for k in range(6):
        c = k * np.pi / 3 + np.pi / 6
        tk = np.linspace(k * np.pi / 3, (k + 1) * np.pi / 3, 25)
        superficie(m, tk, np.linspace(xa, xb, 31), lambda TH, X, c=c: r_hex(TH, X, c))
        contorno = lambda t, c=c: np.minimum(F / np.cos(t - c), 0.93)
        anel(m, xa, tk, ROOT, contorno, -1)
        anel(m, xb, tk, 0.72, contorno, +1)

    # pescoco
    superficie(m, th, np.linspace(-0.12, 0.0, 3), lambda TH, X: np.full_like(X, 0.72))

    # capa prensada (ferrule): sulcos e 8 faces de prensagem
    RF = 0.98

    def r_capa(TH, X):
        r = RF - 0.04 * (1 - ss(0.0, 0.06, X)) - 0.04 * ss(1.84, 1.90, X)
        for g in (0.38, 0.76, 1.14, 1.52):
            r = r - 0.022 * np.exp(-((X - g) / 0.014) ** 2)
        zona = ss(0.45, 0.62, X) * (1 - ss(1.66, 1.80, X))
        r = r - zona * (0.018 - 0.012 * np.cos(8 * TH))
        return r

    xs = np.unique(np.concatenate([np.linspace(0, 1.9, 90),
                                   *[np.linspace(g - 0.05, g + 0.05, 11) for g in (0.38, 0.76, 1.14, 1.52)]]))
    thc = np.linspace(0, TAU, 129)
    superficie(m, thc, xs, r_capa)
    anel(m, 0.0, thc, 0.72, lambda t: r_capa(t, np.zeros_like(t)), -1)
    anel(m, 1.9, thc, 0.87, lambda t: r_capa(t, np.full_like(t, 1.9)), +1)
    superficie(m, th, np.linspace(0.2, 1.9, 4), lambda TH, X: np.full_like(X, 0.87), fora=False)
    anel(m, 0.2, th, 0.44, 0.87, +1)

    # espiga (inserto) com farpas e furo passante
    def r_espiga(TH, X):
        f = np.mod((X - 0.2) / 0.32, 1.0)
        return 0.415 + 0.03 * np.clip(f * 1.15, 0, 1) * ss(0.25, 0.35, X)
    thi = np.linspace(0, TAU, 97)
    superficie(m, thi, np.linspace(0.2, 1.8, 65), r_espiga)
    anel(m, 1.8, thi, 0.30, lambda t: r_espiga(t, np.full_like(t, 1.8)), +1)
    superficie(m, th, np.linspace(-1.65, 1.8, 6), lambda TH, X: np.full_like(X, 0.30), fora=False)
    return m


def casca(ri, ro, uvf=None):
    m = Malha()
    th = np.linspace(0, TAU, NSEG + 1)
    xs = np.linspace(X0, X0 + L, 9)
    superficie(m, th, xs, lambda TH, X: np.full_like(X, ro), True, uvf)
    superficie(m, th, xs, lambda TH, X: np.full_like(X, ri), False, uvf)
    anel(m, X0, th, ri, ro, -1)
    anel(m, X0 + L, th, ri, ro, +1)
    return m


# ---------------------------------------------------------------- texturas
def textura_tranca(n=1024, K=2, fios=5):
    """Ladrilho sem emenda da tranca: dois sentidos cruzados a 45 graus no ladrilho, tecido 1x1."""
    s, t = np.meshgrid((np.arange(n) + 0.5) / n, (np.arange(n) + 0.5) / n)
    pt, qt = (s + t) * K, (s - t) * K + 2 * K     # coordenadas das duas familias
    i, j = np.floor(pt), np.floor(qt)
    fp, fq = pt - i, qt - j

    def fio(f):
        dentro = (f > 0.05) & (f < 0.95)
        g = (f - 0.05) / 0.9 * fios
        g = g - np.floor(g)
        return dentro, np.sqrt(np.clip(1 - (2 * g - 1) ** 2, 0, 1))

    dP, wP = fio(fp)
    dQ, wQ = fio(fq)
    sgnI = 1 - 2 * np.mod(i, 2)
    sgnJ = 1 - 2 * np.mod(j, 2)
    A = 0.55
    hP = np.where(dP, A * sgnI * np.sin(np.pi * qt) + 0.35 * wP, -2.0)
    hQ = np.where(dQ, -A * sgnJ * np.sin(np.pi * pt) + 0.35 * wQ, -2.0)
    H = np.maximum(hP, hQ)
    vao = (H < -1.5)
    H = np.where(vao, -1.1, H)
    # cor: aco com oclusao nos vales
    ao = np.clip((H + 1.1) / 1.9, 0, 1) ** 0.8
    base = np.array([0.80, 0.82, 0.85])
    cor = base[None, None, :] * (0.10 + 0.90 * ao[..., None] ** 1.6)
    cor[vao] = [0.02, 0.022, 0.025]
    # normal map (tangente = +u, bitangente = v decrescente)
    k = 0.016 * n
    dHu = (np.roll(H, -1, 1) - np.roll(H, 1, 1)) / 2
    dHv = (np.roll(H, -1, 0) - np.roll(H, 1, 0)) / 2
    nx, ny = -dHu * k / 2, dHv * k / 2
    nz = np.ones_like(H)
    nn = np.sqrt(nx * nx + ny * ny + nz * nz)
    nrm = np.stack([nx / nn, ny / nn, nz / nn], -1)
    img_c = Image.fromarray((np.clip(cor, 0, 1) ** (1 / 2.2) * 255 + 0.5).astype(np.uint8))
    img_n = Image.fromarray(((nrm * 0.5 + 0.5) * 255 + 0.5).astype(np.uint8))
    return img_c, img_n


def textura_cobertura(w=1024, h=512):
    rng = np.random.default_rng(7)
    ruido = rng.normal(0, 1, (h // 4, w // 4))
    ruido = np.array(Image.fromarray(((ruido * 0.25 + 0.5).clip(0, 1) * 255).astype(np.uint8))
                     .resize((w, h), Image.BICUBIC)) / 255.0 - 0.5
    v = 0.085 + 0.012 * ruido
    cor = np.stack([v * 0.96, v * 1.0, v * 1.08], -1)
    u = (np.arange(w) + 0.5) / w
    faixa = np.exp(-((u - 0.30) / 0.006) ** 4)[None, :]           # linha longitudinal (sem texto)
    cor = cor * (1 - faixa[..., None]) + np.array([0.21, 0.24, 0.29]) * faixa[..., None]
    return Image.fromarray((np.clip(cor, 0, 1) * 255 + 0.5).astype(np.uint8))


def png_bytes(img):
    b = io.BytesIO(); img.save(b, 'PNG', optimize=True); return b.getvalue()


def lin(hexcor):
    c = np.array([int(hexcor[i:i + 2], 16) / 255 for i in (1, 3, 5)])
    return [float(x) for x in np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)] + [1.0]


# ---------------------------------------------------------------- glb
def escrever_glb(caminho, camadas, materiais, imagens):
    buf = bytearray()
    views, accs = [], []

    def view(dados, alvo=None):
        while len(buf) % 4: buf.append(0)
        off = len(buf); buf.extend(dados)
        v = {'buffer': 0, 'byteOffset': off, 'byteLength': len(dados)}
        if alvo: v['target'] = alvo
        views.append(v); return len(views) - 1

    def acc(arr, tipo, comp, alvo, mm=False):
        a = {'bufferView': view(arr.tobytes(), alvo), 'componentType': comp,
             'count': int(arr.shape[0]), 'type': tipo}
        if mm:
            a['min'] = [float(x) for x in arr.min(0)]; a['max'] = [float(x) for x in arr.max(0)]
        accs.append(a); return len(accs) - 1

    imgs = [{'bufferView': view(png_bytes(im)), 'mimeType': 'image/png', 'name': nome} for nome, im in imagens]
    texs = [{'sampler': 0, 'source': k} for k in range(len(imgs))]
    meshes, nodes = [], []
    for k, (nome, (P, N, UV, T, I)) in enumerate(camadas):
        at = {'POSITION': acc(P, 'VEC3', 5126, 34962, True), 'NORMAL': acc(N, 'VEC3', 5126, 34962),
              'TEXCOORD_0': acc(UV, 'VEC2', 5126, 34962), 'TANGENT': acc(T, 'VEC4', 5126, 34962)}
        ind = acc(I.reshape(-1), 'SCALAR', 5125, 34963)
        meshes.append({'name': nome, 'primitives': [{'attributes': at, 'indices': ind, 'material': k, 'mode': 4}]})
        nodes.append({'name': nome, 'mesh': k})
    nodes.append({'name': 'mangueira', 'children': list(range(len(camadas)))})
    gl = {'asset': {'version': '2.0', 'generator': 'gerar_mangueira.py'},
          'scene': 0, 'scenes': [{'name': 'mangueira', 'nodes': [len(nodes) - 1]}],
          'nodes': nodes, 'meshes': meshes, 'materials': materiais, 'accessors': accs,
          'bufferViews': views, 'buffers': [{'byteLength': 0}]}
    if imgs:
        gl.update(images=imgs, textures=texs,
                  samplers=[{'magFilter': 9729, 'minFilter': 9987, 'wrapS': 10497, 'wrapT': 10497}])
    while len(buf) % 4: buf.append(0)
    gl['buffers'][0]['byteLength'] = len(buf)
    js = json.dumps(gl, separators=(',', ':')).encode()
    js += b' ' * ((4 - len(js) % 4) % 4)
    total = 12 + 8 + len(js) + 8 + len(buf)
    with open(caminho, 'wb') as f:
        f.write(struct.pack('<III', 0x46546C67, 2, total))
        f.write(struct.pack('<II', len(js), 0x4E4F534A)); f.write(js)
        f.write(struct.pack('<II', len(buf), 0x004E4942)); f.write(buf)


def main():
    h = (TAU * TRANCA[1] / TRANCA_U) / np.tan(np.radians(TRANCA_ANG))
    uv_tr = lambda TH, X: (TH / TAU * TRANCA_U, (X - X0) / h)
    camadas = {
        'terminal': terminal(),
        'tubo': casca(*TUBO),
        'tranca': casca(*TRANCA, uv_tr),
        'cobertura': casca(*COBERTURA),
    }
    arr = {k: v.arrays() for k, v in camadas.items()}
    todos = np.concatenate([a[0] for a in arr.values()])
    centro = (todos.min(0) + todos.max(0)) / 2
    centro[1:] = 0.0                                   # eixo da mangueira passa exatamente pela origem
    for k in arr:
        P = arr[k][0] - centro
        arr[k] = (P.astype(np.float32),) + arr[k][1:]

    tc, tn = textura_tranca()
    cob = textura_cobertura()
    imagens = [('tranca_cor', tc), ('tranca_normal', tn), ('cobertura_cor', cob)]
    mats = [
        {'name': 'terminal', 'pbrMetallicRoughness': {'baseColorFactor': lin('#C7CCD2'), 'metallicFactor': 1.0, 'roughnessFactor': 0.30}},
        {'name': 'tubo', 'pbrMetallicRoughness': {'baseColorFactor': lin('#3A3F47'), 'metallicFactor': 0.0, 'roughnessFactor': 0.62}},
        {'name': 'tranca', 'pbrMetallicRoughness': {'baseColorTexture': {'index': 0}, 'metallicFactor': 1.0, 'roughnessFactor': 0.38},
         'normalTexture': {'index': 1, 'scale': 1.0}},
        {'name': 'cobertura', 'pbrMetallicRoughness': {'baseColorTexture': {'index': 2}, 'metallicFactor': 0.0, 'roughnessFactor': 0.70}},
    ]
    ordem = ['terminal', 'tubo', 'tranca', 'cobertura']
    escrever_glb(os.path.join(SAIDA, 'mangueira.glb'), [(k, arr[k]) for k in ordem], mats, imagens)

    # uma camada por arquivo, mesmo referencial (para montar a vista explodida no PowerPoint)
    pasta = os.path.join(SAIDA, 'camadas'); os.makedirs(pasta, exist_ok=True)
    texidx = {'tranca': [0, 1], 'cobertura': [2]}
    for k, nome in enumerate(ordem):
        mat = json.loads(json.dumps(mats[k]))
        ims = [imagens[i] for i in texidx.get(nome, [])]
        if nome == 'tranca':
            mat['pbrMetallicRoughness']['baseColorTexture']['index'] = 0; mat['normalTexture']['index'] = 1
        if nome == 'cobertura':
            mat['pbrMetallicRoughness']['baseColorTexture']['index'] = 0
        escrever_glb(os.path.join(pasta, f'mangueira_{nome}.glb'), [(nome, arr[nome])], [mat], ims)

    tri = {k: len(arr[k][4]) for k in ordem}
    print('triangulos', tri, 'total', sum(tri.values()))
    print('centro removido', centro, 'caixa', todos.min(0) - centro, todos.max(0) - centro)


if __name__ == '__main__':
    main()
