# Telas RECRIADAS do GMS para a defesa (peca P4). Dado 100% ficticio; nenhum print real.
# Uso: python gerar_telas.py   (grava ../telas/*.png)
from PIL import Image, ImageDraw, ImageFont
import os

here = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(here, '..', 'telas'); os.makedirs(OUT, exist_ok=True)

BG, SURF, LINE = '#07090D', '#10151C', '#232B36'
TXT, SEC = '#F5F7FA', '#8B97A6'
VIO, VIO2, CYA, AMB, RED = '#8B5CF6', '#C4B5FD', '#06B6D4', '#F59E0B', '#EF4444'
FD = 'C:/Windows/Fonts/'

def bahn(size, var='Bold Condensed'):
    f = ImageFont.truetype(FD + 'bahnschrift.ttf', size); f.set_variation_by_name(var); return f
def cons(size, bold=False):
    return ImageFont.truetype(FD + ('consolab.ttf' if bold else 'consola.ttf'), size)

def mix(c, k, base=SURF):
    a = [int(c[i:i + 2], 16) for i in (1, 3, 5)]; b = [int(base[i:i + 2], 16) for i in (1, 3, 5)]
    return '#%02X%02X%02X' % tuple(int(b[i] + (a[i] - b[i]) * k) for i in range(3))

def box(d, xy, fill=SURF, line=LINE, w=1):
    d.rectangle(xy, fill=fill, outline=line, width=w)

def pill(d, x, y, s, col, f, anchor='l'):
    tw = d.textlength(s, font=f); h = f.size + 12
    x0 = x if anchor == 'l' else x - tw - 24
    d.rectangle((x0, y, x0 + tw + 24, y + h), fill=mix(col, .18), outline=col, width=2)
    d.text((x0 + 12, y + h / 2), s, font=f, fill=col, anchor='lm')
    return x0 + tw + 24

def dashed_h(d, x0, x1, y, col, w=2, on=10, off=8):
    x = x0
    while x < x1:
        d.line((x, y, min(x + on, x1), y), fill=col, width=w); x += on + off

def save(im, name):
    im.save(os.path.join(OUT, name)); print(name, im.size)

ETAPAS = ['Mandril', 'Tubo', 'Trançagem', 'Cobertura', 'Bandagem', 'Vulcanização', 'Debandagem', 'Extração/Teste']

# ---------------------------------------------------------------- 1. painel da celula (TV)
def painel():
    W, H = 1600, 900
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    d.text((40, 52), 'Painel da Célula', font=bahn(52), fill=TXT, anchor='lm')
    d.text((40, 96), 'Sequência das 8 etapas · dado fictício', font=bahn(24, 'SemiCondensed'), fill=SEC, anchor='lm')
    pill(d, W - 40, 34, 'TURNO A · 10:30', VIO2, cons(24, True), anchor='r')
    # (estado, OP, fila, idade, idade_col)
    data = [(1, 'OP 0007', 2, '0h20', TXT), (1, 'OP 0006', 1, '0h35', TXT), (1, 'OP 0005', 3, '1h10', AMB),
            (0, '—', 0, '—', SEC), (1, 'OP 0004', 1, '0h25', TXT), (1, 'OP 0003', 2, '2h40', RED),
            (0, '—', 1, '—', SEC), (1, 'OP 0002', 0, '0h15', TXT)]
    x0, y0, y1, gap = 40, 132, 624, 14
    cw = (W - 2 * x0 - gap * 7) / 8
    for i, (on, op, fila, idade, icol) in enumerate(data):
        x = x0 + i * (cw + gap); xe = x + cw
        col = CYA if on else SEC
        box(d, (x, y0, xe, y1), line=LINE)
        d.rectangle((x, y0, xe, y0 + 6), fill=CYA if on else LINE)
        d.text((x + 14, y0 + 36), f'{i + 1:02d}', font=cons(24, True), fill=SEC, anchor='lm')
        nm = ETAPAS[i]; f = bahn(30)
        while d.textlength(nm, font=f) > cw - 24: f = bahn(f.size - 1)
        d.text((x + 14, y0 + 78), nm, font=f, fill=TXT, anchor='lm')
        # estado
        st = 'EM PRODUÇÃO' if on else 'AGUARDANDO'
        d.rectangle((x + 14, y0 + 108, xe - 14, y0 + 144), fill=mix(col, .2), outline=col, width=2)
        d.text(((x + xe) / 2, y0 + 126), st, font=cons(20, True), fill=col, anchor='mm')
        # OP
        d.text((x + 14, y0 + 184), 'OP EM CURSO', font=cons(20), fill=SEC, anchor='lm')
        d.text((x + 14, y0 + 220), op, font=cons(32, True), fill=TXT if on else SEC, anchor='lm')
        # fila de carreteis
        d.text((x + 14, y0 + 278), 'FILA', font=cons(20), fill=SEC, anchor='lm')
        d.text((xe - 14, y0 + 278), str(fila), font=cons(28, True), fill=TXT, anchor='rm')
        for k in range(4):
            cx = x + 14 + k * 38; cy = y0 + 312
            if k < fila:
                d.ellipse((cx, cy, cx + 30, cy + 30), outline=VIO2, width=4)
                d.ellipse((cx + 10, cy + 10, cx + 20, cy + 20), fill=VIO)
            else:
                d.ellipse((cx, cy, cx + 30, cy + 30), outline=LINE, width=2)
        d.text((x + 14, y0 + 382), 'carretéis', font=bahn(20, 'SemiCondensed'), fill=SEC, anchor='lm')
        # idade da OP
        d.line((x + 14, y0 + 418, xe - 14, y0 + 418), fill=LINE, width=1)
        d.text((x + 14, y0 + 440), 'IDADE OP', font=cons(20), fill=SEC, anchor='lm')
        d.text((x + 14, y0 + 470), idade, font=cons(30, True), fill=icol, anchor='lm')
        if i < 7:  # seta de sequencia
            ax = xe + gap / 2; ay = y0 + 126
            d.polygon([(ax - 5, ay - 9), (ax + 6, ay), (ax - 5, ay + 9)], fill=SEC)
    # faixa onde olhar agora
    fy = 648
    box(d, (40, fy, W - 40, H - 40), fill=SURF)
    d.rectangle((40, fy, 48, H - 40), fill=VIO)
    d.text((72, fy + 40), 'Onde olhar agora', font=bahn(34), fill=TXT, anchor='lm')
    alerts = [(RED, 'Vulcanização', 'OP 0003 há 2h40 nesta etapa', 'idade acima do limite'),
              (AMB, 'Trançagem', 'fila com 3 carretéis aguardando', 'gargalo se formando')]
    aw = (W - 40 - 72 - 24 - 24) / 2
    for j, (c, et, t1, t2) in enumerate(alerts):
        ax = 72 + j * (aw + 24); ay = fy + 72
        d.rectangle((ax, ay, ax + aw, ay + 124), fill=mix(c, .14), outline=c, width=2)
        d.rectangle((ax, ay, ax + 10, ay + 124), fill=c)
        d.text((ax + 32, ay + 32), et.upper(), font=cons(24, True), fill=c, anchor='lm')
        d.text((ax + 32, ay + 70), t1, font=bahn(28, 'SemiBold SemiCondensed'), fill=TXT, anchor='lm')
        d.text((ax + 32, ay + 102), t2, font=bahn(22, 'SemiCondensed'), fill=SEC, anchor='lm')
    save(im, 'tela_painel_celula.png')

# ---------------------------------------------------------------- 2. apontamento (tablet)
def apontamento():
    W, H = 1280, 800
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W, 88), fill=SURF); d.line((0, 88, W, 88), fill=LINE)
    d.text((32, 44), 'Apontamento', font=bahn(40), fill=TXT, anchor='lm')
    x = 32 + d.textlength('Apontamento', font=bahn(40)) + 20
    pill(d, x, 24, 'ETAPA 03 · TRANÇAGEM', CYA, cons(22, True))
    d.text((W - 32, 44), 'TURNO A', font=cons(24, True), fill=SEC, anchor='rm')
    # seletor de OP
    lx0, lx1 = 32, 420
    d.text((lx0, 128), 'Selecione a OP', font=bahn(28, 'SemiBold SemiCondensed'), fill=TXT, anchor='lm')
    ops = [('OP 0005', 'Item B', True), ('OP 0006', 'Item A', False), ('OP 0008', 'Item C', False),
           ('OP 0009', 'Item A', False), ('OP 0010', 'Item B', False)]
    for i, (op, it, sel) in enumerate(ops):
        y = 160 + i * 96
        box(d, (lx0, y, lx1, y + 84), fill=mix(VIO, .22) if sel else SURF, line=VIO if sel else LINE, w=3 if sel else 1)
        d.ellipse((lx0 + 22, y + 26, lx0 + 54, y + 58), outline=VIO2 if sel else SEC, width=3)
        if sel: d.ellipse((lx0 + 30, y + 34, lx0 + 46, y + 50), fill=VIO2)
        d.text((lx0 + 76, y + 42), op, font=cons(30, True), fill=TXT, anchor='lm')
        d.text((lx1 - 22, y + 42), it, font=bahn(24, 'SemiCondensed'), fill=SEC, anchor='rm')
    d.text((lx0, 668), 'na fila desta etapa', font=bahn(22, 'SemiCondensed'), fill=SEC, anchor='lm')
    # metragem
    rx0, rx1 = 460, W - 32
    d.text((rx0, 128), 'Metragem', font=bahn(28, 'SemiBold SemiCondensed'), fill=TXT, anchor='lm')
    box(d, (rx0, 160, rx1, 256), fill=SURF, line=AMB, w=3)
    d.text((rx0 + 28, 208), '52,0', font=cons(60, True), fill=TXT, anchor='lm')
    d.text((rx1 - 28, 208), 'm', font=cons(36), fill=SEC, anchor='rm')
    # aviso amarelo nao bloqueante
    box(d, (rx0, 272, rx1, 344), fill=mix(AMB, .16), line=AMB, w=2)
    tx, ty = rx0 + 26, 308
    d.polygon([(tx, ty + 16), (tx + 18, ty - 16), (tx + 36, ty + 16)], fill=AMB)
    d.text((tx + 18, ty + 5), '!', font=cons(22, True), fill=BG, anchor='mm')
    d.text((tx + 56, ty - 1), 'Medida fora da faixa especificada: confira', font=bahn(28, 'SemiBold SemiCondensed'), fill=AMB, anchor='lm')
    d.text((rx1 - 22, ty), 'pode apontar', font=bahn(22, 'SemiCondensed'), fill=SEC, anchor='rm')
    # teclado (botoes >= 72 px)
    keys = ['7', '8', '9', '4', '5', '6', '1', '2', '3', ',', '0', '⌫']
    bw, bh, g = 120, 78, 12
    for k, s in enumerate(keys):
        cx = rx0 + (k % 3) * (bw + g); cy = 368 + (k // 3) * (bh + g)
        box(d, (cx, cy, cx + bw, cy + bh), fill=SURF, line=LINE, w=2)
        f = cons(36, True) if s != '⌫' else ImageFont.truetype(FD + 'seguisym.ttf', 36) if os.path.exists(FD + 'seguisym.ttf') else cons(36, True)
        d.text((cx + bw / 2, cy + bh / 2), s if s != '⌫' else ('⌫' if f.path.endswith('seguisym.ttf') else '<'), font=f, fill=TXT, anchor='mm')
    kx1 = rx0 + 3 * bw + 2 * g; ky1 = 368 + 4 * bh + 3 * g
    # Limpar e Apontar
    ax0 = kx1 + 28
    box(d, (ax0, 368, rx1, 368 + bh), fill=SURF, line=LINE, w=2)
    d.text(((ax0 + rx1) / 2, 368 + bh / 2), 'Limpar', font=bahn(30, 'SemiBold SemiCondensed'), fill=SEC, anchor='mm')
    d.rectangle((ax0, 368 + bh + g, rx1, ky1), fill=VIO)
    d.text(((ax0 + rx1) / 2, (368 + bh + g + ky1) / 2 - 18), 'Apontar', font=bahn(52), fill=TXT, anchor='mm')
    d.text(((ax0 + rx1) / 2, (368 + bh + g + ky1) / 2 + 30), 'OP 0005 · 52,0 m', font=cons(24, True), fill=VIO2, anchor='mm')
    save(im, 'tela_apontamento.png')

# ---------------------------------------------------------------- 3. consulta de OP
def consulta():
    W, H = 1280, 800
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    d.text((40, 56), 'Consulta de OP', font=bahn(46), fill=TXT, anchor='lm')
    box(d, (40, 100, 1040, 176), fill=SURF, line=VIO, w=2)
    sx, sy = 70, 138
    d.ellipse((sx - 12, sy - 14, sx + 12, sy + 10), outline=SEC, width=3); d.line((sx + 9, sy + 7, sx + 20, sy + 18), fill=SEC, width=4)
    d.text((sx + 40, sy), 'OP 0003', font=cons(32, True), fill=TXT, anchor='lm')
    d.rectangle((1056, 100, W - 40, 176), fill=VIO)
    d.text(((1056 + W - 40) / 2, 138), 'Buscar', font=bahn(32), fill=TXT, anchor='mm')
    # resultado
    box(d, (40, 200, W - 40, H - 40))
    d.text((72, 248), 'OP 0003', font=cons(40, True), fill=TXT, anchor='lm')
    d.text((72 + d.textlength('OP 0003', font=cons(40, True)) + 20, 250), 'Item B', font=bahn(28, 'SemiCondensed'), fill=SEC, anchor='lm')
    pill(d, W - 72, 228, 'ESTADO: EM VULCANIZAÇÃO', CYA, cons(22, True), anchor='r')
    d.text((72, 296), 'Idade da OP: 2h40 · etapa 6 de 8', font=bahn(24, 'SemiCondensed'), fill=SEC, anchor='lm')
    # linha do tempo
    tx0, tx1, ty = 120, W - 120, 380
    step = (tx1 - tx0) / 7; cur = 5
    d.line((tx0, ty, tx0 + step * cur, ty), fill=VIO, width=6)
    for i in range(cur, 7): dashed_h(d, tx0 + step * i + 18, tx0 + step * (i + 1) - 18, ty, LINE, 4)
    times = ['06:40', '07:00', '07:15', '07:30', '07:40', '07:50', '', '']
    for i, nm in enumerate(ETAPAS):
        cx = tx0 + step * i
        if i < cur:
            d.ellipse((cx - 16, ty - 16, cx + 16, ty + 16), fill=VIO)
            d.line((cx - 7, ty, cx - 2, ty + 6, cx + 8, ty - 6), fill=TXT, width=4)
        elif i == cur:
            d.ellipse((cx - 22, ty - 22, cx + 22, ty + 22), outline=CYA, width=5); d.ellipse((cx - 9, ty - 9, cx + 9, ty + 9), fill=CYA)
        else:
            d.ellipse((cx - 14, ty - 14, cx + 14, ty + 14), fill=BG, outline=LINE, width=3)
        c = TXT if i <= cur else SEC
        d.text((cx, ty + 44), nm, font=bahn(22, 'SemiBold Condensed'), fill=CYA if i == cur else c, anchor='mm')
        d.text((cx, ty + 74), times[i] or '—', font=cons(20), fill=SEC, anchor='mm')
    # historico por etapa
    hy = 500
    cols = [(72, 'ETAPA'), (420, 'ENTRADA'), (620, 'SAÍDA'), (820, 'TURNO'), (1000, 'SITUAÇÃO')]
    for x, s in cols: d.text((x, hy), s, font=cons(20, True), fill=SEC, anchor='lm')
    d.line((72, hy + 20, W - 72, hy + 20), fill=LINE)
    rows = [('Bandagem', '07:40', '07:50', 'A', 'concluída', TXT),
            ('Vulcanização', '07:50', '—', 'A', 'em produção', CYA),
            ('Debandagem', '—', '—', '—', 'aguardando', SEC)]
    for r, (et, a, b, t, s, c) in enumerate(rows):
        y = hy + 58 + r * 52
        d.text((72, y), et, font=bahn(26, 'SemiBold SemiCondensed'), fill=TXT, anchor='lm')
        for x, v in zip((420, 620, 820), (a, b, t)): d.text((x, y), v, font=cons(24), fill=TXT, anchor='lm')
        d.text((1000, y), s, font=bahn(24, 'SemiCondensed'), fill=c, anchor='lm')
        d.line((72, y + 26, W - 72, y + 26), fill=LINE)
    d.text((72, H - 72), 'Histórico mostra as últimas etapas; as anteriores ficam na linha do tempo', font=bahn(20, 'SemiCondensed'), fill=SEC, anchor='lm')
    save(im, 'tela_consulta_op.png')

# ---------------------------------------------------------------- 4. cartoes de relatorio
CW, CH = 800, 500
def card(title, sub=None):
    im = Image.new('RGB', (CW, CH), SURF); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, CW - 1, CH - 1), outline=LINE)
    d.text((32, 44), title, font=bahn(36), fill=TXT, anchor='lm')
    if sub: d.text((32, 80), sub, font=bahn(20, 'SemiCondensed'), fill=SEC, anchor='lm')
    return im, d

def c_fila():
    im, d = card('Fila por etapa', 'carretéis aguardando · dado fictício')
    vals = [2, 1, 3, 0, 1, 2, 1, 0]
    y0, rh, bx = 112, 44, 230
    for i, (nm, v) in enumerate(zip(ETAPAS, vals)):
        y = y0 + i * rh
        d.text((32, y + 18), nm, font=bahn(22, 'SemiCondensed'), fill=TXT, anchor='lm')
        d.rectangle((bx, y + 4, CW - 90, y + 32), fill=BG)
        c = AMB if v == max(vals) else VIO
        if v: d.rectangle((bx, y + 4, bx + (CW - 90 - bx) * v / 4, y + 32), fill=c)
        d.text((CW - 32, y + 18), str(v), font=cons(24, True), fill=c if v else SEC, anchor='rm')
    save(im, 'cartao_fila_etapa.png')

def c_paradas():
    im, d = card('Paradas', 'Pareto de motivos · tempo parado por turno')
    mot = [('Setup', 1.0), ('Material', .62), ('Manutenção', .40), ('Qualidade', .22), ('Outros', .12)]
    px0, px1, py0, py1 = 40, 500, 120, 420
    bw = (px1 - px0) / len(mot)
    tot = sum(v for _, v in mot); acc = 0; pts = []
    for i, (nm, v) in enumerate(mot):
        x = px0 + i * bw
        d.rectangle((x + 10, py1 - (py1 - py0) * v * .9, x + bw - 10, py1), fill=VIO if i == 0 else mix(VIO, .65))
        d.text((x + bw / 2, py1 + 22), nm, font=bahn(20, 'Condensed'), fill=TXT, anchor='mm')
        acc += v; pts.append((x + bw / 2, py1 - (py1 - py0) * acc / tot))
    d.line(pts, fill=AMB, width=4)
    for p in pts: d.ellipse((p[0] - 6, p[1] - 6, p[0] + 6, p[1] + 6), fill=AMB)
    d.text((px1, py0 - 4), '100%', font=cons(18, True), fill=AMB, anchor='rm')
    d.line((px1 + 30, py0, px1 + 30, CH - 40), fill=LINE)
    # por turno
    d.text((560, py0 + 4), 'POR TURNO', font=cons(20, True), fill=SEC, anchor='lm')
    tv = [('A', .55), ('B', .85), ('C', .35)]
    for i, (t, v) in enumerate(tv):
        y = py0 + 50 + i * 90
        d.text((560, y + 22), t, font=cons(28, True), fill=TXT, anchor='lm')
        d.rectangle((600, y + 6, 760, y + 38), fill=BG)
        d.rectangle((600, y + 6, 600 + 160 * v, y + 38), fill=RED if v == max(x[1] for x in tv) else CYA)
    save(im, 'cartao_paradas.png')

def c_hora():
    im, d = card('Hora a hora', 'realizado × meta por janela')
    jan = ['06', '07', '08', '09', '10', '11', '12', '13']
    real = [.8, 1.05, 1.1, .7, .95, 1.15, .55, 1.0]
    x0, x1, y0, y1 = 48, CW - 40, 120, 420
    bw = (x1 - x0) / len(jan); my = y1 - (y1 - y0) * .72
    for i, (j, r) in enumerate(zip(jan, real)):
        x = x0 + i * bw; top = y1 - (y1 - y0) * .72 * r
        c = CYA if r >= 1 else (AMB if r >= .75 else RED)
        d.rectangle((x + 12, top, x + bw - 12, y1), fill=c)
        d.text((x + bw / 2, y1 + 24), j + 'h', font=cons(20), fill=TXT, anchor='mm')
    dashed_h(d, x0, x1, my, TXT, 3)
    d.text((x1, my - 18), 'META', font=cons(18, True), fill=TXT, anchor='rm')
    lx = 520
    for c, s in ((CYA, 'na meta'), (AMB, 'perto'), (RED, 'abaixo')):
        d.rectangle((lx, 36, lx + 16, 52), fill=c); d.text((lx + 24, 44), s, font=bahn(20, 'SemiCondensed'), fill=SEC, anchor='lm')
        lx += 30 + d.textlength(s, font=bahn(20, 'SemiCondensed')) + 18
    save(im, 'cartao_hora_hora.png')

def c_montagem():
    im, d = card('Montagem', '12 estações · estado atual')
    st = [CYA, CYA, AMB, CYA, SEC, CYA, RED, CYA, CYA, AMB, CYA, SEC]
    lab = {CYA: 'produzindo', AMB: 'atenção', RED: 'parada', SEC: 'livre'}
    gx, gy, cw, ch, g = 32, 110, (CW - 64 - 3 * 14) / 4, 108, 14
    for i, c in enumerate(st):
        x = gx + (i % 4) * (cw + g); y = gy + (i // 4) * (ch + g)
        d.rectangle((x, y, x + cw, y + ch), fill=mix(c, .14) if c != SEC else BG, outline=c if c != SEC else LINE, width=2)
        d.rectangle((x, y, x + 8, y + ch), fill=c if c != SEC else LINE)
        d.text((x + 24, y + 34), f'E{i + 1:02d}', font=cons(28, True), fill=TXT, anchor='lm')
        d.text((x + 24, y + 76), lab[c], font=bahn(22, 'SemiCondensed'), fill=c if c != SEC else SEC, anchor='lm')
    save(im, 'cartao_montagem.png')

def c_extrusora():
    im, d = card('Extrusora', 'metros por janela · refugo')
    x0, x1, y0, y1 = 48, CW - 40, 120, 330
    v = [.6, .75, .9, .85, .5, .8, .95, .7]
    bw = (x1 - x0) / len(v)
    for i, a in enumerate(v):
        x = x0 + i * bw
        d.rectangle((x + 12, y1 - (y1 - y0) * a, x + bw - 12, y1), fill=VIO)
    d.text((x0, y0 - 8), 'METROS', font=cons(18, True), fill=VIO2, anchor='lm')
    d.line((x0, y1 + 1, x1, y1 + 1), fill=LINE)
    r = [.2, .15, .1, .25, .6, .2, .1, .3]
    ry0, ry1 = 360, 440
    d.text((x0, ry0 - 4), 'REFUGO', font=cons(18, True), fill=RED, anchor='lm')
    for i, a in enumerate(r):
        x = x0 + i * bw
        d.rectangle((x + 12, ry1 - (ry1 - ry0 - 16) * a, x + bw - 12, ry1), fill=RED if a >= .5 else mix(RED, .6))
        d.text((x + bw / 2, ry1 + 22), f'{6 + i:02d}h', font=cons(20), fill=TXT, anchor='mm')
    save(im, 'cartao_extrusora.png')

def placeholder(title, name):
    im = Image.new('RGBA', (CW, CH), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.text((32, 44), title, font=bahn(36), fill=SEC, anchor='lm')
    save(im, name)

if __name__ == '__main__':
    painel(); apontamento(); consulta()
    c_fila(); c_paradas(); c_hora(); c_montagem(); c_extrusora()
    placeholder('OEE por hora', 'cartao_oee_hora.png')
    placeholder('Simulador de demanda × pessoas', 'cartao_simulador.png')
    placeholder('Genealogia entre lotes', 'cartao_genealogia.png')
