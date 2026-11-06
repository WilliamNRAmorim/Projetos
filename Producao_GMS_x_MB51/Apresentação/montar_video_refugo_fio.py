"""Edita o video de 06/11 da tela de refugo de fio: estabiliza, recorta no campo, camera lenta e legendas.
Rodar nesta pasta: python -I montar_video_refugo_fio.py <video_de_entrada.mp4>"""
import sys, os, pathlib
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont
os.chdir(pathlib.Path(__file__).resolve().parent)
SRC = sys.argv[1]; OUT = 'Ocorrencia_Refugo_Fio_video.mp4'
F0, F1 = 255, 432            # trecho em que o separador some
W, H = 1280, 720
RED = (237, 7, 27)
FB = ImageFont.truetype(r'C:/Windows/Fonts/arialbd.ttf', 44); FM = ImageFont.truetype(r'C:/Windows/Fonts/arialbd.ttf', 34)
FS = ImageFont.truetype(r'C:/Windows/Fonts/arial.ttf', 26)

cap = cv2.VideoCapture(SRC)
def frame(i):
    cap.set(1, i); ok, f = cap.read(); return f
ref = frame(F0); g0 = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
TX, TY, TW, TH = 320, 880, 530, 120          # bloco estatico (rotulo + dropdown do motivo) usado para seguir a camera
tpl = g0[TY:TY+TH, TX:TX+TW]
cx0, cy0 = 590, 1015                           # centro do recorte no frame de referencia
CW, CH = 800, 450

offs = []
for i in range(F0, F1 + 1):
    g = cv2.cvtColor(frame(i), cv2.COLOR_BGR2GRAY)
    x0, y0 = max(TX - 120, 0), max(TY - 120, 0)
    win = g[y0:y0 + TH + 240, x0:x0 + TW + 240]
    r = cv2.matchTemplate(win, tpl, cv2.TM_CCOEFF_NORMED); _, _, _, loc = cv2.minMaxLoc(r)
    offs.append((x0 + loc[0] - TX, y0 + loc[1] - TY))
offs = np.array(offs, float)
k = 9; pad = np.pad(offs, ((k, k), (0, 0)), mode='edge')
sm = np.stack([np.convolve(pad[:, j], np.ones(2 * k + 1) / (2 * k + 1), mode='valid') for j in range(2)], 1)

def crop(i, n):
    f = frame(i); dx, dy = sm[n]
    x = int(round(cx0 + dx - CW / 2)); y = int(round(cy0 + dy - CH / 2))
    x = min(max(x, 0), f.shape[1] - CW); y = min(max(y, 0), f.shape[0] - CH)
    return cv2.resize(f[y:y+CH, x:x+CW], (W, H), interpolation=cv2.INTER_CUBIC)

def overlay(img, topo, base):
    im = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)); d = ImageDraw.Draw(im, 'RGBA')
    d.rectangle([0, 0, W, 78], fill=RED + (235,)); d.text((36, 16), topo, font=FM, fill=(255, 255, 255))
    d.rounded_rectangle([40, H - 110, W - 40, H - 30], radius=14, fill=(255, 255, 255, 235))
    d.text((70, H - 94), base, font=FM, fill=(0, 0, 0))
    d.text((W - 250, 100), 'câmera lenta 0,5×', font=FS, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0))
    return cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)

def card(linhas, seg=2.0):
    im = Image.new('RGB', (W, H), (255, 255, 255)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 24, H], fill=RED)
    y = 230
    for i, (t, f, c) in enumerate(linhas):
        d.text((90, y), t, font=f, fill=c); y += 86 if i == 0 else 54
    return [cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)] * int(30 * seg)

wr = cv2.VideoWriter(OUT, cv2.VideoWriter_fourcc(*'mp4v'), 30, (W, H))
topo, base = 'ANTES: a tela de refugo de fio', 'Digitou 3,6 ou 3.6 → o campo gravou 36'
n = F1 - F0
for j in range(n):
    a = crop(F0 + j, j); b = crop(F0 + j + 1, j + 1)
    wr.write(overlay(a, topo, base)); wr.write(overlay(cv2.addWeighted(a, .5, b, .5, 0), topo, base))
last = overlay(crop(F1, n), topo, base)
for _ in range(45): wr.write(last)
wr.release(); print('ok', OUT)
