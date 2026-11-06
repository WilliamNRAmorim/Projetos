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
    txt(sl, x + 150000, y + 100000, w - 300000, 500000, grande, size=26, color=cor, space=0)
    sl.shapes[-1].text_frame.paragraphs[0].runs[0].font.bold = True
    txt(sl, x + 150000, y + 620000, w - 300000, h - 700000, legenda, size=11, color=leg)

s = p.slides.add_slide(LAY['Only title'])
s.shapes.title.text = 'Refugo de fio da bobinadeira: o separador decimal sumia e o banco precisou ser corrigido'
for r in s.shapes.title.text_frame.paragraphs[0].runs: r.font.size = Pt(26)

# coluna 1: o que aconteceu
txt(s, L, 1650000, 3700000, 4500000, [
    ('O que aconteceu', {'b': True, 'c': RED, 's': 15}),
    'Na tela de refugo de fio, o campo de quantidade engolia a vírgula e o ponto. O operador digitava 3,6 e o app guardava 36.',
    'Foi preciso corrigir todo o banco (lista Refugo_Bobinadeira) para os valores voltarem à escala certa.',
    ('Causa', {'b': True, 'c': RED, 's': 15}),
    'A vírgula foi uma das causas, não a única: ela agravou os erros de divergência, mas não impedia o lançamento.',
    ('Correção na tela', {'b': True, 'c': RED, 's': 15}),
    'O campo passa a aceitar vírgula e ponto com o mesmo peso, igual à cabine e ao mandril. Texto inválido deixa a borda vermelha e bloqueia o Registrar.'],
    size=12, space=5)

# coluna 2: evidência do vídeo
txt(s, 4400000, 1650000, 3800000, 300000, ('Evidência (vídeo de 06/11)', {'b': True, 'c': RED, 's': 15}))
txt(s, 4400000, 2050000, 3800000, 250000, ('Digitado: 3.6', {'b': True, 's': 12}))
s.shapes.add_picture('img_refugo_fio/digitado_3_6.png', Emu(4400000), Emu(2330000), width=Emu(3800000))
txt(s, 4400000, 3720000, 3800000, 250000, ('Ficou gravado no campo: 36', {'b': True, 'c': RED, 's': 12}))
s.shapes.add_picture('img_refugo_fio/ficou_36.png', Emu(4400000), Emu(4000000), width=Emu(3800000))

# coluna 3: números
X = 8600000; CW = 3178000
card(s, X, 1650000, CW, 1300000, '1.229', 'registros de refugo de fio, de mai a nov/2026')
card(s, X, 3080000, CW, 1300000, '1.042', 'com ponto decimal (ex.: 18.3); 187 são inteiros', fill=LGREY, cor=DARK)
card(s, X, 4510000, CW, 1300000, '7.706', 'soma no banco corrigido; o BI chegou a mostrar 287.578,93 em 23/10', fill=RED, cor=WHITE, leg=WHITE)

txt(s, L, 6330000, W, 250000, 'Fontes: Refugo_Bobinadeira_2026-11-06.csv, vídeo da tela de 06/11/2026, GMS_Diario (23/10). Patch: GMS/Telas/_patch_RefugoBobinadeira_virgula_ponto_2026-11-06.md.', size=10, color=GREY)
for sh in list(s.placeholders):
    print(sh.placeholder_format.type, sh.name, sh.has_text_frame and sh.text_frame.text[:40])
p.save('Ocorrencia_Refugo_Fio.pptx')
print('ok')
