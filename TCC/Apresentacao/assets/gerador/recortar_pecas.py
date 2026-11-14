# Recorta as 4 camadas das PNGs de reserva (mangueira_<camada>.png) em 8 imagens (acesa e apagada de cada camada),
# todas com a mesma tela por camada, para o Morph do cap3 mover as pecas e acender uma de cada vez.
# Uso: python recortar_pecas.py   (le ../mangueira_*.png, grava ../pecas/pc_<camada>_{on,off}.png)
from PIL import Image
import numpy as np, os
here = os.path.dirname(os.path.abspath(__file__)); a = os.path.join(here, '..'); out = os.path.join(a, 'pecas')
os.makedirs(out, exist_ok=True)
BODY = {'terminal': (181, 533), 'tubo': (566, 935), 'tranca': (960, 1327), 'cobertura': (1335, 1710)}
UNLIT_FROM = {'terminal': 'cobertura', 'tubo': 'cobertura', 'tranca': 'terminal', 'cobertura': 'terminal'}
PAD, Y0, Y1 = 45, 370, 710
for k, (b0, b1) in BODY.items():
    x0, x1 = b0 - PAD, b1 + PAD + 1
    for state, src in (('on', k), ('off', UNLIT_FROM[k])):
        im = Image.open(os.path.join(a, f'mangueira_{src}.png')).convert('RGBA')
        arr = np.array(im)
        for k2, (c0, c1) in BODY.items():           # apaga o corpo das vizinhas (e o brilho sobre elas)
            if k2 != k: arr[:, c0:c1 + 1, 3] = 0
        if state == 'on':                           # brilho some devagar ate a borda da vizinha (sem corte seco)
            ks = list(BODY); i = ks.index(k)
            gl = (b0 - BODY[ks[i - 1]][1]) if i > 0 else PAD
            gr = (BODY[ks[i + 1]][0] - b1) if i < len(ks) - 1 else PAD
            xs = np.arange(arr.shape[1], dtype=float)
            f = np.ones_like(xs)
            f = np.where(xs > b1, np.clip(1 - (xs - b1 - 4) / max(gr - 4, 1), 0, 1), f)
            f = np.where(xs < b0, np.clip(1 - (b0 - xs - 4) / max(gl - 4, 1), 0, 1), f)
            arr[:, :, 3] = (arr[:, :, 3] * f[None, :]).astype(np.uint8)
        if state == 'off':                          # apagada: so o corpo, sem brilho
            arr[:, :b0 - 3, 3] = 0; arr[:, b1 + 4:, 3] = 0
        Image.fromarray(arr).crop((x0, Y0, x1, Y1)).save(os.path.join(out, f'pc_{k}_{state}.png'))
        print(k, state, (x1 - x0, Y1 - Y0))
