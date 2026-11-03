# -*- coding: utf-8 -*-
"""Gerador das figuras do TCC II (GMS).
Desenha cada figura em SVG (tela de 1000 px de largura), grava o HTML em
figuras/fonte/ e renderiza o PNG a 2x com o Edge headless em figuras/.
Uso: python gerar_figuras.py [fig01 fig02 ...]
"""
import math, os, subprocess, sys

FONTE = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.dirname(FONTE)
EDGE = r"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"

NAVY = '#1F3A5F'; DARK = '#333333'; MID = '#8A94A6'
L1 = '#EEF2F7'; L2 = '#F7F7F7'; RED = '#B03A2E'; GREEN = '#2E7D32'; WHITE = '#FFFFFF'
FONT = "Arial, 'Segoe UI', Helvetica, sans-serif"


class Fig:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.p = []

    def add(self, s):
        self.p.append(s)

    # ---------- primitivas ----------
    def rect(self, x, y, w, h, fill=L2, stroke=MID, sw=1.5, rx=6, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
                 f'stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def text(self, x, y, s, size=16, anchor='start', weight='normal', color=DARK, italic=False, bg=None):
        st = ' font-style="italic"' if italic else ''
        if bg:
            # fundo branco aproximado para não ser cortado por linhas
            wid = len(s) * size * 0.55 + 12
            x0 = x - wid / 2 if anchor == 'middle' else (x - wid if anchor == 'end' else x - 6)
            self.add(f'<rect x="{x0:.1f}" y="{y - size}" width="{wid:.1f}" height="{size * 1.45:.1f}" fill="{bg}"/>')
        self.add(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" '
                 f'fill="{color}" font-family="{FONT}"{st}>{s}</text>')

    def html(self, x, y, w, h, content, size=16, color=DARK, align='center', valign='center',
             weight='normal', pad=6, italic=False, lh=1.22):
        for t in ('Hora-Hora', 'Code 128', 'Code 39', '≈ 28', '(16 seções)', '(1 linha', '(e-mail corporativo)', 'packing list)', 'Power Fx)'):
            content = content.replace(t, f'<span style="white-space:nowrap">{t}</span>')
        jc = {'center': 'center', 'left': 'flex-start', 'right': 'flex-end'}[align]
        ai = {'center': 'center', 'top': 'flex-start', 'bottom': 'flex-end'}[valign]
        fs = 'italic' if italic else 'normal'
        self.add(
            f'<foreignObject x="{x}" y="{y}" width="{w}" height="{h}">'
            f'<div xmlns="http://www.w3.org/1999/xhtml" style="width:{w}px;height:{h}px;box-sizing:border-box;'
            f'padding:{pad}px;display:flex;align-items:{ai};justify-content:{jc};text-align:{align};'
            f'font-family:{FONT};font-size:{size}px;line-height:{lh};color:{color};font-weight:{weight};'
            f'font-style:{fs};"><div>{content}</div></div></foreignObject>')

    def box(self, x, y, w, h, content, fill=L2, stroke=MID, sw=1.5, rx=6, size=16, color=DARK,
            weight='normal', dash=None, align='center', pad=8, italic=False, valign='center'):
        self.rect(x, y, w, h, fill, stroke, sw, rx, dash)
        self.html(x, y, w, h, content, size, color, align, valign, weight, pad, italic)

    def oval(self, x, y, w, h, content, fill=WHITE, stroke=DARK, sw=1.8, size=16, color=DARK, weight='bold'):
        self.rect(x, y, w, h, fill, stroke, sw, rx=h / 2)
        self.html(x, y, w, h, content, size, color, weight=weight, pad=10)

    def diamond(self, cx, cy, w, h, content, fill=WHITE, stroke=NAVY, sw=1.8, size=16, color=DARK):
        pts = f'{cx},{cy - h / 2} {cx + w / 2},{cy} {cx},{cy + h / 2} {cx - w / 2},{cy}'
        self.add(f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
        self.html(cx - w * 0.31, cy - h * 0.31, w * 0.62, h * 0.62, content, size, color, pad=0)

    def doc(self, x, y, w, h, content, fill=WHITE, stroke=DARK, sw=1.6, size=16, color=DARK):
        b = y + h - 10
        d = (f'M{x},{y + 4} Q{x},{y} {x + 4},{y} L{x + w - 4},{y} Q{x + w},{y} {x + w},{y + 4} L{x + w},{b} '
             f'C{x + w * 0.75},{b - 12} {x + w * 0.62},{b + 12} {x + w / 2},{b} '
             f'C{x + w * 0.38},{b - 12} {x + w * 0.25},{b + 12} {x},{b} Z')
        self.add(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
        self.html(x, y, w, h - 12, content, size, color, pad=8)

    def poly(self, pts, fill, stroke=MID, sw=1.5):
        s = ' '.join(f'{a:.1f},{b:.1f}' for a, b in pts)
        self.add(f'<polygon points="{s}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>')

    def line(self, pts, color=DARK, sw=2, dash=None, head=None, tail=False):
        d = 'M' + ' L'.join(f'{a:.1f},{b:.1f}' for a, b in pts)
        da = f' stroke-dasharray="{dash}"' if dash else ''
        me = f' marker-end="url(#h{head})"' if head else ''
        ms = f' marker-start="url(#h{head})"' if (tail and head) else ''
        self.add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}"{da}{me}{ms} '
                 f'stroke-linejoin="round"/>')

    def arrow(self, pts, color=DARK, sw=2, dash=None, both=False):
        key = {DARK: 'd', NAVY: 'n', MID: 'g', RED: 'r', GREEN: 'v'}[color]
        self.line(pts, color, sw, dash, head=key, tail=both)

    def queue(self, cx, cy, color=MID):
        for i in (-6, 0, 6):
            self.add(f'<rect x="{cx + i - 2}" y="{cy - 8}" width="4" height="16" fill="{color}"/>')

    # ---------- saída ----------
    def svg(self):
        defs = ''.join(
            f'<marker id="h{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="11" markerHeight="11" '
            f'markerUnits="userSpaceOnUse" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>'
            for k, c in (('d', DARK), ('n', NAVY), ('g', MID), ('r', RED), ('v', GREEN)))
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
                f'viewBox="0 0 {self.w} {self.h}"><defs>{defs}</defs>'
                f'<rect width="{self.w}" height="{self.h}" fill="#fff"/>' + '\n'.join(self.p) + '</svg>')

    def save(self, nome):
        html = ('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>' + nome +
                '</title><style>html,body{margin:0;padding:0;background:#fff;overflow:hidden}svg{display:block}'
                '</style></head><body>' + self.svg() + '</body></html>')
        hp = os.path.join(FONTE, nome + '.html')
        with open(hp, 'w', encoding='utf-8') as f:
            f.write(html)
        png = os.path.join(SAIDA, nome + '.png')
        url = 'file:///' + hp.replace('\\', '/')
        subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--hide-scrollbars',
                        '--force-device-scale-factor=2', f'--window-size={self.w},{self.h}',
                        f'--screenshot={png}', url], capture_output=True, timeout=120)
        print(nome, self.w, self.h)


# =====================================================================
def fig01():
    f = Fig(1000, 470)
    x0, bw, gap = 122, 156, 22
    xs = [x0 + i * (bw + gap) for i in range(5)]

    def faixa(y, rot, cor_rot, fill_rot, txt_rot, itens, fill, stroke, cor_seta, regua, cor_regua):
        f.box(10, y, 100, 112, rot, fill=fill_rot, stroke=cor_rot, sw=2, size=18, color=txt_rot)
        for i, t in enumerate(itens):
            f.box(xs[i], y, bw, 112, t, fill=fill, stroke=stroke, sw=1.6, size=16)
            if i < 4:
                f.arrow([(xs[i] + bw + 1, y + 56), (xs[i + 1] - 1, y + 56)], cor_seta)
        ry = y + 136
        f.line([(x0, ry), (990, ry)], MID, 2)
        f.line([(x0, ry - 8), (x0, ry + 8)], MID, 2)
        f.line([(990, ry - 8), (990, ry + 8)], MID, 2)
        f.text(x0 - 8, ry + 6, 'tempo', 15, 'end', color=MID, italic=True)
        f.text(556, ry + 6, regua, 17, 'middle', 'bold', cor_regua, bg='#fff')

    faixa(10, '<b>ANTES</b><br>(papel)', RED, L2, RED, [
        'Operador escreve na ficha física, nas 8 etapas',
        'Ficha acompanha a mangueira (rasuras, graxa, campos ilegíveis)',
        'No turno seguinte: transcrição manual para planilha',
        'Lançamento no SAP',
        'Supervisão recebe o relato do dia anterior'], L2, MID, DARK, 'defasagem de 1 a 2 dias', RED)
    notas = ['387 fichas de papel em um mês', '≈ 2.900 lançamentos manuais por mês',
             '≈ 28 fontes de dados desconectadas', 'conferir uma OP com o SAP custava uma manhã']
    nw = (990 - x0 - 3 * 14) / 4
    for i, t in enumerate(notas):
        f.box(x0 + i * (nw + 14), 168, nw, 54, t, fill=WHITE, stroke=RED, sw=1.2, dash='5 4', size=15)
    # seta entre faixas
    f.arrow([(330, 236), (330, 296)], NAVY, 2.5)
    f.html(345, 238, 600, 56, 'Não se criou o dado: zerou-se o custo de acessá-lo', 18, NAVY,
           align='left', weight='bold', italic=True, pad=0)
    faixa(310, '<b>DEPOIS</b><br>(GMS)', NAVY, NAVY, WHITE, [
        'Operador registra na estação (tablet + leitor de código de barras)',
        'Validação na origem (formato, faixa, obrigatoriedade)',
        'Registro único por OP nas listas do SharePoint',
        'Painel da Célula, Power BI e conferência com o SAP',
        'Supervisão acompanha o turno corrente'], L1, NAVY, NAVY, 'defasagem de segundos', GREEN)
    f.save('fig01_fluxo_antes_depois')


# =====================================================================
def fig02():
    f = Fig(1000, 580)
    T, B = 36, 540
    k = 120 / (B - T)
    xl = lambda y: 190 + k * (B - y)
    xr = lambda y: 790 - k * (B - y)
    f.text(812, 24, 'Escala de tempo típica', 16, weight='bold', color=DARK)
    niveis = [
        (84, '<b>Nível 4: Planejamento do negócio e logística</b><br>Exemplo: ERP (SAP)', 'meses, semanas, dias', False),
        (116, '<b>Nível 3: Gestão das operações de manufatura</b><br>MES: GMS (coleta, rastreabilidade, qualidade, filas, indicadores)',
         'dias, turnos, horas, minutos, segundos', True),
        (76, '<b>Nível 2: Supervisão e controle</b><br>SCADA / IHM', 'horas, minutos, segundos', False),
        (76, '<b>Nível 1: Sensoriamento e atuação</b><br>CLP, sensores', 'segundos, frações de segundo', False),
        (70, '<b>Nível 0: Processo físico</b><br>máquinas da célula de mangueiras', '', False),
    ]
    gaps = [64, 6, 6, 6]
    y = T
    pos = []
    for i, (h, txt, esc, dest) in enumerate(niveis):
        y1, y2 = y, y + h
        pos.append((y1, y2))
        fill = NAVY if dest else (L1 if i == 0 else L2)
        stroke = NAVY if dest else MID
        f.poly([(xl(y1), y1), (xr(y1), y1), (xr(y2), y2), (xl(y2), y2)], fill, stroke, 1.6)
        f.html(xl(y1) + 14, y1, xr(y1) - xl(y1) - 28, h, txt, 17 if dest else 16,
               WHITE if dest else DARK, pad=2)
        if esc:
            ym = (y1 + y2) / 2
            f.line([(xr(ym) + 6, ym), (804, ym)], MID, 1.2, dash='2 4')
            f.html(810, y1, 185, h, esc, 15, DARK, align='left', pad=2)
        if i < 4:
            y = y2 + gaps[i]
    # setas ERP <-> GMS no intervalo entre nível 4 e 3
    g1, g2 = pos[0][1], pos[1][0]
    f.arrow([(440, g1 + 3), (440, g2 - 3)], NAVY, 2.2, both=True)
    f.html(240, g1 + 4, 190, g2 - g1 - 8, 'conferência diária<br>com o MB51', 15, NAVY, align='right', pad=0)
    f.arrow([(560, g1 + 3), (560, g2 - 3)], NAVY, 2.2)
    f.html(572, g1 + 4, 200, g2 - g1 - 8, 'validação da OP<br>contra o plano', 15, NAVY, align='left', pad=0)
    # seta tracejada nível 1-2 -> 3
    ys = (pos[2][1] + pos[3][0]) / 2 + 30
    y3 = (pos[1][0] + pos[1][1]) / 2
    f.arrow([(xl(ys) - 6, ys), (150, ys), (150, y3), (xl(y3) - 6, y3)], MID, 2, dash='7 5')
    f.html(8, y3 + 20, 136, ys - y3 - 40, 'coleta automática das máquinas (trabalho futuro)', 15, DARK,
           align='right', italic=True, pad=0)
    f.text(10, 568, 'Base: ANSI/ISA-95 (níveis funcionais)', 15, color=MID, italic=True)
    f.save('fig02_isa95')


# =====================================================================
def fig03():
    f = Fig(1000, 548)
    cx, cy, rx, ry = 380, 274, 260, 220
    f.add(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{MID}" stroke-width="2.5"/>')
    for a in (-60, 0, 60, 120, 180, 240):
        t = math.radians(a)
        px, py = cx + rx * math.cos(t), cy + ry * math.sin(t)
        tx, ty = -rx * math.sin(t), ry * math.cos(t)
        n = math.hypot(tx, ty); tx, ty = tx / n, ty / n
        nx, ny = -ty, tx
        L, W = 22, 7
        f.add(f'<polygon points="{px + tx * L / 2:.1f},{py + ty * L / 2:.1f} '
              f'{px - tx * L / 2 + nx * W:.1f},{py - ty * L / 2 + ny * W:.1f} '
              f'{px - tx * L / 2 - nx * W:.1f},{py - ty * L / 2 - ny * W:.1f}" fill="{DARK}"/>')
    etapas = ['Manhã: observação na estação (Gemba)',
              'Registro da decisão (diário e backlog rastreável)',
              'Tarde: desenvolvimento (patch no código-fonte YAML da tela, Power Fx)',
              'QA automatizado (bateria de 17 testes)',
              'Publicação da nova versão',
              'Turno seguinte: uso real pelo operador e retorno']
    cw, ch = 226, 86
    for i, (a, t) in enumerate(zip((-90, -30, 30, 90, 150, 210), etapas)):
        r = math.radians(a)
        px, py = cx + rx * math.cos(r), cy + ry * math.sin(r)
        f.box(px - cw / 2, py - ch / 2, cw, ch,
              f'<span style="color:{NAVY};font-weight:bold;font-size:19px">{i + 1}</span>&nbsp; {t}',
              fill=L2, stroke=NAVY, sw=1.6, size=16)
    f.add(f'<circle cx="{cx}" cy="{cy}" r="100" fill="{NAVY}"/>')
    f.html(cx - 80, cy - 70, 160, 140, 'menos de 24 h entre observação e correção', 19, WHITE, weight='bold', pad=0)
    f.box(800, cy - 160, 186, 320, '<b style="font-size:19px">Norma escrita</b><br><br>princípios, padrões e 40 conceitos',
          fill=L1, stroke=NAVY, sw=1.8, size=17)
    f.arrow([(798, cy), (cx + rx + 6, cy)], NAVY, 2, dash='7 5')
    f.html(cx + rx + 10, cy - 48, 146, 44, 'orienta cada iteração', 15, NAVY, italic=True, pad=0)
    f.save('fig03_ciclo_rad')


# =====================================================================
def fig05():
    f = Fig(1000, 950)
    MX, MW = 10, 720       # coluna principal
    RX, RW = 790, 200      # sistemas corporativos

    def camada(y, h, titulo, itens, fill=L1, stroke=NAVY, th=34, bh=None):
        f.rect(MX, y, MW, h, fill, stroke, 1.8, 6)
        f.html(MX + 12, y + 4, MW - 24, th, titulo, 18, NAVY, align='left', weight='bold', pad=2)
        n = len(itens)
        iw = (MW - 28 - 12 * (n - 1)) / n
        by = y + th + 8
        bh = bh or (h - th - 20)
        for i, t in enumerate(itens):
            f.box(MX + 14 + i * (iw + 12), by, iw, bh, t, fill=WHITE, stroke=MID, sw=1.4, size=15, pad=7)

    def gap_seta(x, y1, y2, rot, both=False, up=False, w=300):
        pts = [(x, y2 - 2), (x, y1 + 2)] if up else [(x, y1 + 2), (x, y2 - 2)]
        f.arrow(pts, NAVY, 2.2, both=both)
        f.html(x + 10, y1, w, y2 - y1, rot, 15, DARK, align='left', pad=0, lh=1.15)

    y = 10
    camada(y, 116, 'Chão de fábrica e dispositivos', [
        'Tablet por estação (terminal autenticado)', 'Leitor de código de barras',
        'Impressora de packing list (Code 39 e Code 128)', 'TV de gestão (Painel da Célula)'], fill=L2, stroke=MID)
    gap_seta(160, 126, 170, 'entrada (toque, leitura) e saída (impressão, TV)', both=True, w=500)
    camada(170, 140, 'Coleta: Power Apps (Canvas)', [
        '28 telas de operação e gestão', 'Power Fx: fórmulas nomeadas e funções do usuário (16 seções)',
        'Tokens de design e templates de tela', 'Código-fonte YAML por tela'])
    gap_seta(160, 310, 356, 'grava e consulta', w=200)
    gap_seta(470, 310, 356, 'pendências da conferência<br>na tela de tratativa', up=True, w=250)
    camada(356, 150, 'Persistência: Microsoft Lists (SharePoint Online)', [
        '≈ 28 listas', 'ficha_producao: passaporte da OP (1 linha por OP)',
        'Inspeção, refugo, Hora-Hora, carretéis, packing, conferência',
        'Dados mestres de engenharia (Excel Online)'], th=44)
    f.box(MX + MW - 196, 362, 184, 38, 'consultas delegáveis<br>e colunas indexadas', fill=WHITE,
          stroke=NAVY, sw=1.2, rx=10, size=15, color=NAVY, pad=2)
    gap_seta(120, 506, 552, 'leitura (Power Query)', w=200)
    gap_seta(470, 506, 552, 'gatilhos, leitura e gravação', both=True, w=250)
    # linha inferior: Power BI | Orquestração
    yb, hb = 552, 222
    hw = (MW - 20) / 2
    for j, (tit, itens) in enumerate([
        ('Análise: Power BI', ['Power Query: camadas Bronze, Prata e Ouro', 'Modelo estrela (fatos e dimensões)',
                                'DAX: tempo de ciclo, lead time, gargalo, Hora-Hora']),
        ('Orquestração: Power Automate + Office Scripts (TypeScript)',
         ['Conferência diária GMS × SAP × Packing', 'Início automático do resfriamento (+110 min)',
          'E-mail diário à supervisão'])]):
        x = MX + j * (hw + 20)
        f.rect(x, yb, hw, hb, L1, NAVY, 1.8, 6)
        f.html(x + 12, yb + 4, hw - 24, 48, tit, 18, NAVY, align='left', weight='bold', pad=2, lh=1.15)
        for i, t in enumerate(itens):
            f.box(x + 14, yb + 58 + i * 54, hw - 28, 46, t, fill=WHITE, stroke=MID, sw=1.4, size=15, pad=6)
    xo = MX + hw + 20
    # supervisão
    ys = yb + hb + 44
    gap_seta(MX + hw / 2, yb + hb, ys, 'relatórios e painéis', w=200)
    gap_seta(xo + hw / 2, yb + hb, ys, 'e-mail diário', w=160)
    f.box(MX, ys, MW, 44, 'Supervisão e gerência', fill=WHITE, stroke=NAVY, sw=1.8, size=17, color=NAVY, weight='bold')
    # coluna sistemas corporativos
    f.rect(RX, 10, RW, ys - 10 + 44, WHITE, MID, 1.5, 6, dash='6 4')
    f.html(RX + 8, 16, RW - 16, 50, 'Sistemas corporativos', 18, DARK, weight='bold', pad=0)
    f.box(RX + 14, 190, RW - 28, 100, '<b>Microsoft 365</b><br>identidade por e-mail corporativo, Outlook',
          fill=L2, stroke=MID, sw=1.5, size=15)
    sy = yb + 58 + 23
    f.box(RX + 14, sy - 50, RW - 28, 100, '<b>SAP ERP</b><br>MB51, plano de OPs', fill=L2, stroke=MID, sw=1.5, size=15)
    f.arrow([(RX + 12, sy), (MX + MW + 2, sy)], NAVY, 2.2)
    f.html(MX + MW + 2, sy - 44, RX - MX - MW - 2, 40, 'export<br>MB51', 15, DARK, pad=0, lh=1.1)
    # engenharia do sistema
    ye = ys + 44 + 18
    f.rect(10, ye, 980, 62, L2, MID, 1.5, 6)
    f.html(20, ye, 190, 62, 'Engenharia do sistema', 17, NAVY, align='left', weight='bold', pad=0)
    itens = ['Norma escrita', 'Diário de decisões', 'Backlog rastreável', 'QA automatizado (Python)']
    iw = (980 - 210 - 12 - 36) / 4
    for i, t in enumerate(itens):
        f.box(220 + i * (iw + 12), ye + 11, iw, 40, t, fill=WHITE, stroke=MID, sw=1.3, size=15, pad=4)
    f.h = ye + 62 + 10
    f.save('fig05_arquitetura')


# =====================================================================
def fig06():
    f = Fig(1000, 640)
    FS = 17
    # coluna esquerda: do início até a validação
    ca, wa = 220, 300
    esq = [('o', 'Início', 40), ('p', 'Terminal da estação autenticado (e-mail corporativo)', 52),
           ('p', 'Abre a tela da etapa', 40), ('p', 'Carrega a fila da etapa (cargas em paralelo)', 52),
           ('p', 'Operador seleciona a OP ou lê o código do carretel', 52),
           ('d', 'OP disponível para esta etapa?', 92, 300),
           ('p', 'Preenche os campos da etapa', 40),
           ('d', 'Validação na origem: formato, faixa, obrigatoriedade, metragem &gt; 0?', 140, 390)]
    gap = 18

    def coluna(nos, cx, w, y, gap):
        geo = []
        for n in nos:
            tipo, t, h = n[0], n[1], n[2]
            geo.append((tipo, y, h, n[3] if tipo == 'd' else w))
            if tipo == 'o':
                f.oval(cx - 90, y, 180, h, t, size=FS)
            elif tipo == 'p':
                f.box(cx - w / 2, y, w, h, t, fill=L1, stroke=NAVY, sw=1.6, size=FS, pad=5)
            else:
                f.diamond(cx, y + h / 2, n[3], h, t, size=FS)
            y += h + gap
        for i in range(len(geo) - 1):
            _, y1, h1, _ = geo[i]
            _, y2, _, _ = geo[i + 1]
            f.arrow([(cx, y1 + h1 + 1), (cx, y2 - 1)], DARK, 2)
            if geo[i][0] == 'd':
                f.text(cx + 8, y1 + h1 + 15, 'Sim', 15, weight='bold', color=GREEN)
        return geo

    ga = coluna(esq, ca, wa, 10, gap)

    def laco(idx_d, idx_back, txt):
        _, yd, hd, dw = ga[idx_d]
        ym = yd + hd / 2
        _, yb, hb, _ = ga[idx_back]
        yback = yb + hb / 2
        bx, bw = 458, 140
        f.arrow([(ca + dw / 2, ym), (bx - 1, ym)], RED, 2)
        f.text(ca + dw / 2 + 6, ym - 7, 'Não', 15, weight='bold', color=RED)
        f.box(bx, ym - 26, bw, 52, txt, fill=WHITE, stroke=RED, sw=1.6, size=FS, pad=4)
        f.arrow([(bx + bw / 2, ym - 26), (bx + bw / 2, yback), (ca + wa / 2 + 1, yback)], RED, 2)

    laco(5, 4, 'Aviso ao operador')
    laco(7, 6, 'Mensagem e correção')
    # coluna direita: da gravação até o fim
    cb, wb = 800, 310
    dir_ = [('p', 'Grava o registro (carimbo de data, hora e turno)', 52),
            ('p', 'Atualiza a situação da OP', 44), ('p', 'OP entra na fila da etapa seguinte', 44),
            ('p', 'Atualiza totais do turno, Hora-Hora e Painel', 52), ('o', 'Fim', 40)]
    gb = coluna(dir_, cb, wb, 10, 46)
    # ligação pela base: validação (Sim) -> grava o registro
    _, yd, hd, _ = ga[7]
    yl = yd + hd + 20
    xl = 618
    y6 = gb[0][1] + gb[0][2] / 2
    f.arrow([(ca, yd + hd + 1), (ca, yl), (xl, yl), (xl, y6), (cb - wb / 2 - 1, y6)], DARK, 2)
    f.text(ca - 8, yd + hd + 18, 'Sim', 15, 'end', 'bold', GREEN)
    f.h = int(yl + 10)
    f.save('fig06_fluxograma_tela')


# =====================================================================
def fig07():
    f = Fig(1000, 520)
    cw, cg = 128, 34
    r1 = [10 + i * (cw + cg) for i in range(5)]
    y1, ch = 120, 90
    nomes = ['Mandril', 'Tubo', 'Trançagem', 'Cobertura', 'Bandagem', 'Vulcanização', 'Debandagem',
             'Extração e Inspeção']

    def card(x, y, n, nome):
        f.box(x, y, cw, ch, f'<span style="color:{NAVY};font-weight:bold;font-size:19px">{n}</span><br>{nome}',
              fill=L1, stroke=NAVY, sw=1.6, size=16, pad=6)

    # alimentações
    f.box(10, 10, cw, 62, 'Extrusora de mandril', fill=L2, stroke=MID, size=16)
    f.arrow([(74, 73), (74, y1 - 1)], DARK, 2)
    f.html(148, 10, 176, 62, 'estado do carretel: vazio, enchendo, cheio, em uso', 15, DARK, align='left',
           italic=True, pad=0)
    f.box(r1[2], 10, cw, 62, 'Bobinadeira (fio, FIFO)', fill=L2, stroke=MID, size=16)
    f.arrow([(r1[2] + cw / 2, 73), (r1[2] + cw / 2, y1 - 1)], DARK, 2)
    f.html(r1[2] + cw + 10, 10, 140, 62, 'Trançagem: 11 trançadeiras', 15, DARK, align='left', italic=True, pad=0)
    # legenda
    f.queue(672, 36)
    f.text(688, 42, 'fila da etapa', 15, color=DARK)
    f.line([(800, 36), (836, 36)], MID, 1.4, dash='4 3', head='g')
    f.text(844, 42, 'grava na ficha', 15, color=DARK)
    # linha 1
    for i in range(5):
        card(r1[i], y1, i + 1, nomes[i])
        if i < 4:
            f.arrow([(r1[i] + cw + 1, y1 + ch / 2 + 8), (r1[i + 1] - 1, y1 + ch / 2 + 8)], DARK, 2)
            f.queue(r1[i] + cw + cg / 2, y1 + ch / 2 - 14)
    # faixa
    fy, fh = 262, 54
    f.box(10, fy, 776, fh, 'ficha_producao, o passaporte da OP: cada etapa grava a sua parte',
          fill=NAVY, stroke=NAVY, size=17, color=WHITE, weight='bold')
    for i in range(5):
        xc = r1[i] + cw / 2
        f.line([(xc, y1 + ch + 2), (xc, fy - 2)], MID, 1.4, dash='4 3', head='g')
    # linha 2 (direita para esquerda)
    y2 = 366
    r2 = [r1[4], r1[3], r1[2], r1[1], r1[0]]
    for j in range(3):
        card(r2[j], y2, 6 + j, nomes[5 + j])
        xc = r2[j] + cw / 2
        f.line([(xc, y2 - 2), (xc, fy + fh + 2)], MID, 1.4, dash='4 3', head='g')
    f.box(r2[3], y2, cw, ch, 'Finalização: packing list e pallet', fill=L2, stroke=MID, sw=1.6, size=16)
    f.box(r2[4], y2, cw, ch, 'Estoque e SAP', fill=L2, stroke=MID, sw=1.6, size=16)
    for j in range(4):
        f.arrow([(r2[j] - 1, y2 + ch / 2 + 8), (r2[j + 1] + cw + 1, y2 + ch / 2 + 8)], DARK, 2)
        if j < 2:
            f.queue(r2[j] - cg / 2, y2 + ch / 2 - 14)
    # conector 5 -> 6
    xr = 966
    f.arrow([(r1[4] + cw + 1, y1 + ch / 2 + 8), (xr, y1 + ch / 2 + 8), (xr, y2 + ch / 2 + 8),
             (r2[0] + cw + 1, y2 + ch / 2 + 8)], DARK, 2)
    f.queue(876, y1 + ch / 2 - 6)
    # nota do painel
    f.arrow([(788, fy + fh / 2), (808, fy + fh / 2)], NAVY, 2)
    f.box(810, fy - 26, 136, fh + 52, 'Painel da Célula (TV) e Hora-Hora leem o estado em tempo real',
          fill=WHITE, stroke=NAVY, sw=1.4, size=15, pad=6)
    # notas sob a linha 2
    f.html(r2[0] - 20, y2 + ch + 4, cw + 40, 44, 'batelada (autoclave)', 15, DARK, italic=True, valign='top', pad=2)
    f.html(r2[2] - 20, y2 + ch + 4, cw + 40, 44, 'lances aprovados e refugados', 15, DARK, italic=True,
           valign='top', pad=2)
    f.h = y2 + ch + 52
    f.save('fig07_fluxo_celula')


# =====================================================================
def fig08():
    f = Fig(1000, 470)
    X = lambda m: 40 + m * 49       # m = meses desde ago/2025
    A = 300
    # barras de fase
    def barra(m1, m2, y, txt, fill, dash=None):
        f.text(X(m1), y + 18, txt, 16, color=DARK, weight='bold')
        if dash:
            f.rect(X(m1), y + 26, X(m2) - X(m1), 16, WHITE, NAVY, 1.6, 3, dash=dash)
        else:
            f.rect(X(m1), y + 26, X(m2) - X(m1), 16, fill, fill, 1, 3)
    barra(0, 3, 8, 'Desenvolvimento inicial (ago a out/2025)', MID)
    barra(10, 15, 8, 'Consolidação e expansão (jun a out/2026)', NAVY)
    barra(2, 10, 58, 'Implantação e validação papel × digital (out/2025 a mai/2026)', NAVY)
    f.text(X(15), 58 + 18, 'Replicação (próxima etapa)', 16, color=DARK, weight='bold')
    f.rect(X(15), 58 + 26, 975 - X(15), 16, WHITE, NAVY, 1.6, 3, dash='6 4')
    # eixo
    f.arrow([(30, A), (985, A)], DARK, 2)
    for m in range(0, 18):
        big = m in (5, 17)
        f.line([(X(m), A - (8 if big else 4)), (X(m), A + (8 if big else 4))], DARK, 2 if big else 1.2)
    f.text(X(0), A - 12 + 0, '', 15)
    for m, ano in ((5, '2026'), (17, '2027')):
        f.text(X(m), A - 14, ano, 15, 'middle', 'bold', MID)
    f.text(X(0) - 2, A + 26, '', 15)

    lv_up = {1: 248, 2: 200, 3: 128}
    lv_dn = {1: 312, 2: 378, 3: 422}

    def marco(m, data, txt, lado, nivel, w=230, h=44, dash=None):
        x = X(m) if isinstance(m, (int, float)) else m
        f.add(f'<circle cx="{x}" cy="{A}" r="6" fill="{WHITE if dash else NAVY}" stroke="{NAVY}" stroke-width="2"/>')
        if lado == 'up':
            ytop = lv_up[nivel]
            f.line([(x, A - 7), (x, ytop)], MID, 1.4, dash=dash)
        else:
            ytop = lv_dn[nivel]
            f.line([(x, A + 7), (x, ytop + h)], MID, 1.4, dash=dash)
        f.html(x + 6, ytop, w, h, f'<b style="color:{NAVY}">{data}</b><br>{txt}', 15, DARK, align='left',
               valign='top', pad=0, lh=1.18)

    marco(0, 'ago/2025', 'Gemba Walk e início', 'up', 1)
    marco(9, 'mai/2026', 'ficha de papel retirada', 'up', 3, w=190)
    marco(11, 'jul/2026', 'norma escrita v1.0', 'up', 2, w=180)
    marco(13, 'set/2026', 'Painel da Célula (TV)', 'up', 1, w=180)
    marco(2, 'out/2025', 'primeiras telas em produção', 'down', 1)
    marco(10, 'jun/2026', 'qualificação (TCC I) e auditoria do app', 'down', 3, w=300)
    marco(12, 'ago/2026', 'Kaizen Award e norma do BI', 'down', 2, w=240)
    marco(14, 'out/2026', 'conferência diária com o SAP e packing com código de barras', 'down', 1, w=252, h=62)
    # marcador final tracejado
    xf = 960
    f.add(f'<circle cx="{xf}" cy="{A}" r="6" fill="{WHITE}" stroke="{NAVY}" stroke-width="2" stroke-dasharray="3 2"/>')
    f.line([(xf, A - 7), (xf, 128)], MID, 1.4, dash='4 3')
    f.html(xf - 300, 128, 294, 64, f'<b style="color:{NAVY}">próxima etapa</b><br>Forest City, Carolina do Norte (EUA)'
           f'<br>migração para Dataverse', 15, DARK, align='right', valign='top', pad=0, lh=1.18)
    f.h = lv_dn[3] + 44 + 6
    f.save('fig08_linha_tempo')


# =====================================================================
def fig09():
    f = Fig(1000, 760)
    lanes = [(10, 'Power Automate'), (340, 'Office Scripts (TypeScript)'), (670, 'Power Apps / Supervisão')]
    H = 742
    for x, t in lanes:
        f.rect(x, 10, 320, H - 10, WHITE, MID, 1.3, 4)
        f.box(x, 10, 320, 38, t, fill=L1, stroke=MID, sw=1.3, rx=4, size=17, weight='bold', color=NAVY)
    # Power Automate
    f.oval(40, 62, 260, 58, 'Agendamento: terça a sábado, 08:00', size=16)
    f.arrow([(170, 121), (170, 143)], DARK, 2)
    f.diamond(170, 196, 250, 104, 'Export do MB51 atualizado?', size=16)
    f.box(50, 282, 240, 56, 'Nova verificação a cada 30 min, até 4 h', fill=L1, stroke=NAVY, sw=1.6, size=16)
    f.arrow([(170, 249), (170, 281)], RED, 2)
    f.text(180, 270, 'Não', 16, weight='bold', color=RED)
    f.arrow([(49, 310), (24, 310), (24, 196), (44, 196)], RED, 2)
    f.doc(50, 384, 240, 76, 'E-mail com alerta de dado desatualizado', fill=WHITE, stroke=RED, size=16)
    f.arrow([(170, 339), (170, 383)], RED, 2)
    f.text(180, 366, 'esgotou 4 h', 15, color=RED, italic=True)
    f.box(30, 560, 280, 120, '<b>Regras:</b> o SAP é a referência; faltas e sobras são somadas por material, '
          'nunca entre materiais.', fill=L2, stroke=MID, sw=1.4, dash='6 4', size=16, align='left', pad=12)
    # Office Scripts
    f.arrow([(296, 196), (359, 196)], GREEN, 2)
    f.text(312, 186, 'Sim', 16, 'middle', 'bold', GREEN)
    bx, bw = 360, 280
    osb = [(168, 56, 'Office Script: lê o packing list'),
           (254, 84, 'Office Script: lê o MB51 em blocos e cruza com o GMS (ficha de produção e inspeção)'),
           (368, 56, 'Classifica em 14 categorias de divergência'),
           (454, 56, 'Grava pendências na lista de conferência')]
    for i, (y, h, t) in enumerate(osb):
        f.box(bx, y, bw, h, t, fill=L1, stroke=NAVY, sw=1.6, size=16)
        if i < 3:
            f.arrow([(500, y + h + 1), (500, osb[i + 1][0] - 1)], DARK, 2)
    # Apps / Supervisão
    f.doc(700, 446, 250, 74, 'E-mail diário à supervisão (resumo)', size=16)
    f.arrow([(641, 482), (699, 482)], DARK, 2)
    f.box(700, 548, 250, 76, 'Tela de tratativa no app: responsável e justificativa obrigatória',
          fill=L1, stroke=NAVY, sw=1.6, size=16)
    f.arrow([(825, 512), (825, 547)], DARK, 2)
    f.diamond(825, 688, 236, 100, 'GMS e SAP batem?', size=16)
    f.arrow([(825, 625), (825, 637)], DARK, 2)
    f.arrow([(707, 688), (601, 688)], GREEN, 2)
    f.text(636, 678, 'Sim', 16, 'middle', 'bold', GREEN)
    f.oval(400, 662, 200, 52, 'Item resolvido', size=16)
    f.arrow([(943, 688), (976, 688), (976, 586), (951, 586)], RED, 2)
    f.text(948, 712, 'Não', 16, weight='bold', color=RED)
    f.h = H + 10
    f.save('fig09_conferencia')


# =====================================================================
def fig10():
    f = Fig(1000, 500)
    # legenda
    f.rect(20, 14, 22, 16, '#B5BCC8', '#B5BCC8', 1, 2); f.text(50, 28, 'Antes do GMS', 16)
    f.rect(190, 14, 22, 16, NAVY, NAVY, 1, 2); f.text(220, 28, 'Com o GMS', 16)
    x0, S = 20, 5.0   # 100 -> 500 px
    cats = [('Horas de consolidação de relatórios', 3, '3 (−97%)'),
            ('Tempo de resposta a reclamação', 2.8, '2,8 (36× mais rápido)'),
            ('Escopo de contenção de lote', 12.5, '12,5 (−87,5%)')]
    yax = 412
    for v in (0, 25, 50, 75, 100):
        f.line([(x0 + v * S, 64), (x0 + v * S, yax)], '#D5DAE2', 1, dash='3 3')
    for i, (t, v, rot) in enumerate(cats):
        c = 58 + i * 116
        f.text(x0, c + 20, t, 17, weight='bold', color=DARK)
        f.rect(x0, c + 30, 100 * S, 28, '#B5BCC8', '#B5BCC8', 1, 2)
        f.text(x0 + 100 * S + 8, c + 50, '100', 16, color=DARK)
        f.rect(x0, c + 64, v * S, 28, NAVY, NAVY, 1, 2)
        f.text(x0 + v * S + 8, c + 84, rot, 16, weight='bold', color=NAVY)
    f.line([(x0, yax), (x0 + 100 * S, yax)], DARK, 1.5)
    for v in (0, 25, 50, 75, 100):
        f.line([(x0 + v * S, yax), (x0 + v * S, yax + 6)], DARK, 1.5)
        f.text(x0 + v * S, yax + 24, str(v), 15, 'middle')
    f.text(x0 + 50 * S, yax + 48, 'índice: situação anterior = 100', 15, 'middle', italic=True)
    # painel direito
    px, PS = 680, 2.6
    f.line([(640, 50), (640, 470)], MID, 1.2)
    f.text(px, 78, 'WIP visível por etapa', 17, weight='bold')
    f.line([(px, 88), (px, 152)], DARK, 1.5)
    f.text(px + 8, 108 + 0, '0%', 16)
    f.rect(px, 122, 100 * PS, 28, NAVY, NAVY, 1, 2)
    f.text(px + 100 * PS + 8, 142, '100%', 16, weight='bold', color=NAVY)
    f.line([(px, 170), (px + 100 * PS, 170)], DARK, 1.5)
    for v in (0, 50, 100):
        f.line([(px + v * PS, 170), (px + v * PS, 176)], DARK, 1.5)
        f.text(px + v * PS, 194, f'{v}%', 15, 'middle')
    f.html(px, 214, 300, 70, 'antes: sem registro da fila por etapa (0%); com o GMS: todas as etapas visíveis',
           15, DARK, align='left', valign='top', italic=True, pad=0)
    f.text(20, 490, 'Fonte dos valores: dossiê do Kaizen Award corporativo (2026)', 15, color=MID, italic=True)
    f.save('fig10_indicadores')


# =====================================================================
def _borda(cx, cy, w, h, tx, ty):
    """ponto na borda do retângulo centrado em (cx,cy) na direção de (tx,ty)"""
    dx, dy = tx - cx, ty - cy
    s = min((w / 2) / abs(dx) if dx else 1e9, (h / 2) / abs(dy) if dy else 1e9)
    return cx + dx * s, cy + dy * s


def fig11():
    f = Fig(1000, 620)
    bw, bg = 195, 37
    xs = [10, 10 + bw + bg, 10 + 2 * (bw + bg)]
    blocos = [('Fontes', 'listas do SharePoint (≈ 28)<br>Excel de dados mestres<br>export do SAP (MB51)', L2, MID),
              ('Bronze', 'consultas de origem (Power Query, não carregadas)', L2, MID),
              ('Prata', 'tipagem, unpivot para OP × etapa, data de referência e turno', L1, NAVY)]
    for i, (t, c, fl, st) in enumerate(blocos):
        f.rect(xs[i], 10, bw, 180, fl, st, 1.8, 6)
        f.html(xs[i], 14, bw, 30, t, 19, NAVY, weight='bold', pad=0)
        f.html(xs[i] + 6, 46, bw - 12, 140, c, 16, DARK, pad=4)
        if i < 2:
            f.arrow([(xs[i] + bw + 1, 100), (xs[i + 1] - 1, 100)], NAVY, 2.4)
    # legenda de notação
    f.box(710, 10, 280, 180, '<b>Notação</b><br><b>1</b> = lado “um” (dimensão)<br><b>*</b> = lado “muitos” (fato)'
          '<br>relações 1:N de sentido único', fill=WHITE, stroke=MID, sw=1.3, dash='5 4', size=15,
          align='left', pad=14)
    # Ouro
    oy, oh = 240, 370
    f.rect(10, oy, 659, oh, L1, NAVY, 2.2, 6)
    f.html(20, oy + 4, 640, 30, 'Ouro: modelo semântico', 19, NAVY, align='left', weight='bold', pad=4)
    f.arrow([(xs[2] + bw / 2, 191), (xs[2] + bw / 2, oy - 1)], NAVY, 2.4)
    fx, fy, fw, fh = 340, 405, 200, 58
    dims = [('Calendário', 130, 318), ('Turno', 340, 300), ('Etapa', 550, 318), ('OP', 100, 405),
            ('Mangueira', 580, 405), ('Posto', 170, 494), ('Colaborador', 510, 494)]
    dw, dh = 132, 36
    for n, x, y in dims:
        a = _borda(fx, fy, fw, fh, x, y)
        b = _borda(x, y, dw, dh, fx, fy)
        f.line([a, b], DARK, 1.6)
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
        nx, ny = -uy, ux
        if ny > 0 or (abs(ny) < 1e-6 and nx < 0):
            nx, ny = -nx, -ny
        for (px, py), s in ((a, '*'), (b, '1')):
            d = 13 if s == '*' else -13
            f.text(px + ux * d + nx * 11, py + uy * d + ny * 11 + 6, s, 17, 'middle', 'bold', NAVY)
    for n, x, y in dims:
        f.box(x - dw / 2, y - dh / 2, dw, dh, n, fill=WHITE, stroke=NAVY, sw=1.5, size=16, pad=2)
    f.box(fx - fw / 2, fy - fh / 2, fw, fh, '<b>Etapas</b><br>(OP × etapa)', fill=NAVY, stroke=NAVY, size=16,
          color=WHITE, pad=2)
    f.html(24, oy + oh - 68, 630, 60, '<b>Demais fatos:</b> Refugo, Inspeção, Hora-Hora, Parada, Carretel, Evento, '
           'Fluxo de etapas', 16, DARK, align='left', pad=2)
    # medidas
    f.arrow([(670, oy + oh / 2), (709, oy + oh / 2)], NAVY, 2.4)
    f.rect(710, oy, 280, oh, WHITE, NAVY, 1.8, 6)
    f.html(720, oy + 4, 260, 54, 'Relatórios e medidas DAX', 19, NAVY, align='left', weight='bold', pad=4)
    med = ['Tempo de ciclo por etapa (mediana)', 'Lead time da OP (mediana e P90)', 'Índice de gargalo (WIP ÷ vazão)',
           'Idade da OP na etapa', 'Hora-Hora: real × meta']
    for i, m in enumerate(med):
        f.box(724, oy + 48 + i * 62, 252, 52, m, fill=L2, stroke=MID, sw=1.3, size=16, pad=6)
    f.save('fig11_bi')


# =====================================================================
def fig12():
    f = Fig(1000, 700)

    def ent(x, y, w, nome, attrs, hh=36):
        lh = 21
        n = sum(a.count('<br>') + 1 for a in attrs)
        h = hh + 10 + n * lh + 6
        f.rect(x, y, w, h, WHITE, NAVY, 1.6, 4)
        f.add(f'<path d="M{x},{y + hh} L{x},{y + 4} Q{x},{y} {x + 4},{y} L{x + w - 4},{y} Q{x + w},{y} {x + w},{y + 4} '
              f'L{x + w},{y + hh} Z" fill="{NAVY}"/>')
        f.html(x, y, w, hh, nome, 17, WHITE, weight='bold', pad=2, lh=1.12)
        f.html(x + 12, y + hh + 4, w - 20, h - hh - 6, '<br>'.join(attrs), 15, DARK, align='left', valign='top',
               pad=2, lh=1.4)
        return x, y, w, h

    A, B, C = 15, 355, 725
    WA, WB, WC = 270, 300, 260
    ms = ent(A, 10, WA, 'MapeamentoSetor', ['e-mail', 'área'])
    dm = ent(B, 10, WB, 'Dados mestres de engenharia (Excel)', ['mangueira × código de trança', 'parâmetros por etapa'], hh=50)
    te = ent(C, 10, WC, 'TiposErros', ['código', 'descrição (catálogo de refugo)'])
    fi = ent(B, 186, WB, 'ficha_producao<br><span style="font-weight:normal;font-size:15px">(passaporte da OP)</span>',
             ['<b>ID</b> (chave)', 'OP', 'mangueira', 'situação',
              'campos por etapa (data/hora,<br>quantidade, operador, máquina)', 'ficha_pai → ficha'], hh=50)
    ca = ent(A, 216, WA, 'Carretéis', ['código', 'estado (vazio, enchendo,<br>cheio, em uso)', 'OP de consumo'])
    ri = ent(C, 200, WC, 'RegistrosInspeção', ['<b>ID</b>', 'OP_ID → ficha', 'lance', 'aprovado / refugado',
                                               'tipo de erro'])
    hy = 470
    hh_ = ent(A, hy, WA, 'Hora-Hora', ['data de referência, turno', 'máquina, janela', 'real, meta',
                                       'motivo de parada'])
    pk = ent(B, hy, WB, 'Packing / Pallets', ['OP_ID → ficha', 'pallet', 'metros', 'código de barras'])
    cs = ent(C, hy, WC, 'Conferência SAP', ['OP', 'categoria de divergência', 'responsável', 'justificativa',
                                            'situação'])

    def card(p, q, lp, lq, side_p, side_q, rot=None, rotpos=None):
        f.line([p, q], DARK, 1.8)
        for (x, y), s, (dx, dy) in ((p, lp, side_p), (q, lq, side_q)):
            f.text(x + dx, y + dy, s, 17, 'middle', 'bold', NAVY)
        if rot:
            f.html(*rotpos, rot, 15, DARK, italic=True, pad=0, align='center' if rot == 'consumo' else 'left')

    bot = lambda e: e[1] + e[3]
    # Dados mestres 1 — N ficha
    xm = B + 150
    card((xm, bot(dm)), (xm, fi[1]), '1', 'N', (12, 18), (12, -6), 'por mangueira', (xm + 24, bot(dm) + 6, 140, 40))
    # TiposErros 1 — N inspeção
    xt = C + 130
    card((xt, bot(te)), (xt, ri[1]), '1', 'N', (12, 18), (12, -6))
    # ficha 1 — N inspeção
    yi = 270
    card((B + WB, yi), (C, yi), '1', 'N', (12, -8), (-12, -8))
    # Carretéis N — 1 ficha
    yc = 290
    card((A + WA, yc), (B, yc), 'N', '1', (12, -8), (-12, -8), 'consumo', (A + WA + 2, yc + 4, B - A - WA - 4, 22))
    # ficha 1 — N packing
    card((xm, bot(fi)), (xm, pk[1]), '1', 'N', (12, 18), (12, -6))
    # autorrelação ficha_pai
    yb = bot(fi)
    f.line([(B + 230, yb), (B + 230, yb + 28), (B + 280, yb + 28), (B + 280, yb)], DARK, 1.8)
    f.text(B + 220, yb + 18, '1', 17, 'middle', 'bold', NAVY)
    f.text(B + 290, yb + 18, 'N', 17, 'middle', 'bold', NAVY)
    f.html(B + WB + 8, yb + 2, 360, 44, 'ficha_pai: divisão por sobra de carretel', 15, DARK, italic=True,
           align='left', pad=0)
    yn = max(bot(hh_), bot(pk), bot(cs)) + 14
    f.box(A, yn, WA + 340 + 15, 36, '<b>Chave canônica entre registros:</b> ID (nunca o número da OP)',
          fill=L2, stroke=MID, sw=1.3, dash='5 4', size=15, align='left', pad=10)
    f.h = yn + 36 + 10
    f.save('fig12_modelo_dados')


# =====================================================================
def fig13():
    f = Fig(1000, 700)
    f.box(410, 10, 180, 42, 'Abertura', fill=L1, stroke=NAVY, sw=1.6, size=17, weight='bold')
    f.arrow([(500, 53), (500, 79)], DARK, 2)
    f.box(320, 80, 360, 46, 'Menu (controle de acesso por setor)', fill=NAVY, stroke=NAVY, size=17, color=WHITE,
          weight='bold')
    cols = [(285, 'Setores de mangueira', 'Seleção de etapa e posto', 260),
            (690, 'Gestão', 'Seleção de gestão', 210),
            (905, 'Montagem', 'Seleção de célula (12 células)', 160)]
    f.line([(500, 127), (500, 152)], DARK, 2)
    f.line([(285, 152), (905, 152)], DARK, 2)
    for x, a, b, w in cols:
        f.arrow([(x, 152), (x, 179)], DARK, 2)
        f.box(x - w / 2, 180, w, 44, a, fill=L1, stroke=NAVY, sw=1.6, size=17, weight='bold')
        f.arrow([(x, 225), (x, 253)], DARK, 2)
        f.box(x - w / 2, 254, w, 52 if w < 200 else 44, b, fill=WHITE, stroke=NAVY, sw=1.6, size=16)
    # --- ramo Setores de mangueira
    bus = 20
    f.line([(285 - 130, 276), (bus, 276), (bus, 640)], DARK, 1.8)
    # contêiner 8 etapas
    cy0 = 330
    f.rect(36, cy0, 524, 136, L2, MID, 1.4, 6)
    f.html(46, cy0 + 2, 500, 26, 'Telas das 8 etapas', 16, NAVY, align='left', weight='bold', pad=2)
    et = ['1 Mandril', '2 Tubo', '3 Trançagem', '4 Cobertura', '5 Bandagem', '6 Vulcanização', '7 Debandagem',
          '8 Extração e Inspeção']
    ew = (524 - 20 - 30) / 4
    for i, t in enumerate(et):
        r, c = divmod(i, 4)
        f.box(46 + c * (ew + 10), cy0 + 32 + r * 52, ew, 44, t, fill=WHITE, stroke=MID, sw=1.3, size=15, pad=3)
    f.arrow([(bus, cy0 + 68), (35, cy0 + 68)], DARK, 1.8)
    # contêiner estações de apoio
    ay0 = 484
    f.rect(36, ay0, 524, 92, L2, MID, 1.4, 6)
    f.html(46, ay0 + 2, 500, 26, 'Estações de apoio', 16, NAVY, align='left', weight='bold', pad=2)
    ap = ['Extrusora de mandril', 'Bobinadeira', 'Refugo da bobinadeira', 'Catenária', 'Finalização']
    aw = (524 - 20 - 40) / 5
    for i, t in enumerate(ap):
        f.box(46 + i * (aw + 10), ay0 + 32, aw, 50, t, fill=WHITE, stroke=MID, sw=1.3, size=15, pad=3)
    f.arrow([(bus, ay0 + 46), (35, ay0 + 46)], DARK, 1.8)
    xfin = 46 + 4 * (aw + 10) + aw / 2
    f.arrow([(xfin, ay0 + 83), (xfin, 603)], DARK, 1.8)
    f.box(xfin - 84, 604, 168, 54, 'Impressão<br>(packing list)', fill=WHITE, stroke=NAVY, sw=1.5, size=15, pad=3)
    f.box(36, 600, 236, 54, 'Hora-Hora (Trançagem, Cobertura, Mandril, Tubo)', fill=WHITE, stroke=NAVY, sw=1.5,
          size=15, pad=4)
    f.arrow([(bus, 627), (35, 627)], DARK, 1.8)
    f.box(282, 600, 120, 54, 'Histórico do turno', fill=WHITE, stroke=NAVY, sw=1.5, size=15, pad=4)
    f.line([(bus, 640), (bus, 670), (342, 670), (342, 655)], DARK, 1.8, head='d')
    # --- ramo Gestão
    gb = 598
    gi = [('Consulta de OP', 0), ('Ficha / impressão', 1), ('Volume diário', 0), ('Conferência SAP', 0),
          ('Painel da Célula (TV)', 0), ('Ficha técnica', 0), ('Plano de OPs', 0)]
    y = 330
    last = 0
    for t, ind in gi:
        if ind:
            f.box(650, y, 150, 38, t, fill=WHITE, stroke=MID, sw=1.3, size=15, pad=2)
            f.arrow([(630, y - 10), (630, y + 19), (649, y + 19)], DARK, 1.6)
        else:
            f.box(612, y, 188, 38, t, fill=WHITE, stroke=NAVY, sw=1.4, size=15, pad=2)
            f.arrow([(gb, y + 19), (611, y + 19)], DARK, 1.6)
            last = y + 19
        y += 46
    f.line([(690, 298), (690, 316), (gb, 316), (gb, last)], DARK, 1.8)
    # --- ramo Montagem
    f.arrow([(905, 307), (905, 335)], DARK, 2)
    f.box(825, 336, 160, 52, 'Hora-Hora da Montagem', fill=WHITE, stroke=NAVY, sw=1.4, size=15, pad=3)
    f.h = 680
    f.save('fig13_navegacao')


TODAS = {'fig01': fig01, 'fig02': fig02, 'fig03': fig03, 'fig05': fig05, 'fig06': fig06, 'fig07': fig07,
         'fig08': fig08, 'fig09': fig09, 'fig10': fig10, 'fig11': fig11, 'fig12': fig12, 'fig13': fig13}

if __name__ == '__main__':
    alvo = sys.argv[1:] or list(TODAS)
    for k in alvo:
        TODAS[k]()
