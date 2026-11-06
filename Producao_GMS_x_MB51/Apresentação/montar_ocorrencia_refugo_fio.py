"""Slide único: ocorrência do refugo de fio da bobinadeira (vírgula/ponto). Rodar nesta pasta: python -I montar_ocorrencia_refugo_fio.py"""
import os, pathlib
os.chdir(pathlib.Path(__file__).resolve().parent)
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

RED = RGBColor(0xED, 0x07, 0x1B); DARK = RGBColor(0x77, 0x04, 0x0E); GREY = RGBColor(0x87, 0x88, 0x96)
PINK = RGBColor(0xFD, 0xEA, 0xEC); LGREY = RGBColor(0xF5, 0xF5, 0xF7); BLACK = RGBColor(0, 0, 0); WHITE = RGBColor(255, 255, 255)
L, W = 414000, 11364000

p = Presentation('template_base.pptx')
ids = p.slides._sldIdLst
for sid in list(ids):
    p.part.drop_rel(sid.rId); ids.remove(sid)
LAY = {l.name: l for l in p.slide_layouts}

def txt(sl, x, y, w, h, linhas, size=14, color=BLACK, space=5, align=PP_ALIGN.LEFT):
    tb = sl.shapes.add_textbox(Emu(x), Emu(y), Emu(w), Emu(h)); tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Emu(0)
    if isinstance(linhas, (str, tuple)): linhas = [linhas]
    for i, l in enumerate(linhas):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        b, c, s, t = False, color, size, l
        if isinstance(l, tuple): t, o = l; b = o.get('b', b); c = o.get('c', c); s = o.get('s', s)
        r = para.add_run(); r.text = t; r.font.size = Pt(s); r.font.bold = b; r.font.color.rgb = c
        para.space_after = Pt(space); para.alignment = align

def card(sl, x, y, w, h, grande, legenda, fill=PINK, cor=RED, leg=BLACK):
    r = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Emu(x), Emu(y), Emu(w), Emu(h))
    r.adjustments[0] = 0.08; r.fill.solid(); r.fill.fore_color.rgb = fill; r.line.fill.background(); r.shadow.inherit = False
    txt(sl, x + 150000, y + 100000, w - 300000, 500000, grande, size=24, color=cor, space=0)
    sl.shapes[-1].text_frame.paragraphs[0].runs[0].font.bold = True
    txt(sl, x + 150000, y + 620000, w - 300000, h - 700000, legenda, size=11, color=leg)

def novo(titulo):
    s = p.slides.add_slide(LAY['Only title']); s.shapes.title.text = titulo
    for r in s.shapes.title.text_frame.paragraphs[0].runs: r.font.size = Pt(26)
    return s

# ------------------------------------------------ slide 1: o que aconteceu + video
s = novo('Refugo de fio da bobinadeira: o separador decimal sumia ao digitar')
txt(s, L, 1650000, 3500000, 4500000, [
    ('O que aconteceu', {'b': True, 'c': RED, 's': 15}),
    'Na tela de refugo de fio, o campo de quantidade engolia a vírgula e o ponto. O operador digitava 3,6 e o app guardava 36.',
    'Foi preciso corrigir todo o banco (lista Refugo_Bobinadeira) para os valores voltarem à escala certa.',
    ('Causa', {'b': True, 'c': RED, 's': 15}),
    'A vírgula foi uma das causas, não a única: ela agravou os erros de divergência, mas não impedia o lançamento.'],
    size=12, space=6)
VX, VW = 4200000, 7578000; VH = int(VW * 9 / 16)
s.shapes.add_movie('Ocorrencia_Refugo_Fio_video.mp4', Emu(VX), Emu(1650000), Emu(VW), Emu(VH),
                   poster_frame_image='img_refugo_fio/poster_video.png', mime_type='video/mp4')
txt(s, VX, 1650000 + VH + 120000, VW, 300000, 'Vídeo da tela em 06/11/2026, em câmera lenta: digitar 3,6 ou 3.6 gravava 36.', size=11, color=GREY)
txt(s, L, 6330000, W, 250000, 'Fonte: vídeo da tela de refugo de fio de 06/11/2026 (antes da correção).', size=10, color=GREY)

# ------------------------------------------------ slide 2: depois da correcao
s = novo('Depois: tela aceita vírgula e ponto e o banco foi corrigido')
IW = 6900000; IH = int(IW * 758 / 1357)
s.shapes.add_picture('img_refugo_fio/depois_tela.png', Emu(L), Emu(1650000), width=Emu(IW))
txt(s, L, 1650000 + IH + 120000, IW, 600000, 'Tela de 06/11 após a correção: o campo aceita 3,6 e a lista mostra os valores certos (2.27, 31.06, total 49.15; antes 2.270, 31.060 e 49.150).', size=11, color=GREY)
X = 7600000; CW = 4178000
card(s, X, 1650000, CW, 1300000, '≈640', 'dos 1.229 registros (52%) tinham o separador decimal perdido e foram corrigidos em 05 e 06/11')
card(s, X, 3080000, CW, 1300000, '1554 → 15,54', 'exemplo real (ID 1032): sem o ponto, o valor ficava 100× maior', fill=LGREY, cor=DARK)
card(s, X, 4510000, CW, 1300000, '13', 'registros duplicados ou com quantidade zero apagados (lixeira, restauráveis por 93 dias)', fill=RED, cor=WHITE, leg=WHITE)
txt(s, L, 6330000, W, 250000, 'Fontes: histórico de correções do Refugo_Bobinadeira de 05 e 06/11/2026 (192 + 268 + 110 + 55 + 13 itens), foto da tela publicada em 06/11/2026.', size=10, color=GREY)

p.save('Ocorrencia_Refugo_Fio_com_video.pptx')
print('ok')
