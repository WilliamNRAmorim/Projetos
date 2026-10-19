"""Monta a apresentação das tratativas GMS x SAP (MB51) no template Danfoss.
Rodar nesta pasta: python -I montar_apresentacao.py (gera Tratativas_GMS_x_SAP.pptx a partir de template_base.pptx)."""
import copy, io
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION

RED = RGBColor(0xED, 0x07, 0x1B); DARK = RGBColor(0x77, 0x04, 0x0E); GREY = RGBColor(0x87, 0x88, 0x96)
PINK = RGBColor(0xFD, 0xEA, 0xEC); LGREY = RGBColor(0xF5, 0xF5, 0xF7); BLACK = RGBColor(0, 0, 0); WHITE = RGBColor(255, 255, 255)
L, W = 414000, 11364000          # margem esquerda e largura útil do template

p = Presentation('template_base.pptx')
# foto da capa (do slide de exemplo do template)
foto = None
for sh in p.slides[0].shapes:
    if sh.shape_type == 14 and hasattr(sh, 'image'):
        try: foto = sh.image.blob
        except Exception: pass
if foto is None:
    for rel in p.slides[0].part.rels.values():
        if 'image' in rel.reltype: foto = rel.target_part.blob; break
# remove os slides de exemplo
ids = p.slides._sldIdLst
for sid in list(ids):
    p.part.drop_rel(sid.rId); ids.remove(sid)

LAY = {l.name: l for l in p.slide_layouts}

def txt(sl, x, y, w, h, linhas, size=15, bold=False, color=BLACK, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, space=4):
    tb = sl.shapes.add_textbox(Emu(x), Emu(y), Emu(w), Emu(h)); tf = tb.text_frame; tf.word_wrap = True
    tf.vertical_anchor = anchor; tf.margin_left = tf.margin_right = Emu(0); tf.margin_top = tf.margin_bottom = Emu(0)
    if isinstance(linhas, str): linhas = [linhas]
    for i, l in enumerate(linhas):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        b, c, s, t = bold, color, size, l
        if isinstance(l, tuple): t, opt = l[0], l[1]; b = opt.get('b', b); c = opt.get('c', c); s = opt.get('s', s)
        r = para.add_run(); r.text = t; r.font.size = Pt(s); r.font.bold = b; r.font.color.rgb = c
        para.alignment = align; para.space_after = Pt(space)
    return tb

def card(sl, x, y, w, h, grande, legenda, fill=PINK, cor=RED, gs=34, leg=BLACK):
    r = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Emu(x), Emu(y), Emu(w), Emu(h))
    r.adjustments[0] = 0.08; r.fill.solid(); r.fill.fore_color.rgb = fill; r.line.fill.background(); r.shadow.inherit = False
    txt(sl, x + 180000, y + 150000, w - 360000, 600000, grande, size=gs, bold=True, color=cor)
    txt(sl, x + 180000, y + 150000 + int(gs * 17000) + 80000, w - 360000, h - 700000, legenda, size=13, color=leg)

def slide(titulo, layout='Only title'):
    s = p.slides.add_slide(LAY[layout]); s.shapes.title.text = titulo
    for ph in list(s.placeholders):
        if ph.placeholder_format.idx != 0 and ph.placeholder_format.type is not None and ph.is_placeholder and not ph.has_text_frame:
            ph._element.getparent().remove(ph._element)
    return s

def tabela(sl, x, y, w, cabec, linhas, larg, size=12, alt=330000, numcols=()):
    n = len(linhas) + 1
    gt = sl.shapes.add_table(n, len(cabec), Emu(x), Emu(y), Emu(w), Emu(alt * n)); t = gt.table
    tblPr = gt._element.graphic.graphicData.tbl.tblPr
    for a in ('bandRow', 'firstRow'): tblPr.set(a, '0')
    sid = tblPr.find('{http://schemas.openxmlformats.org/drawingml/2006/main}tableStyleId')
    if sid is not None: sid.text = '{2D5ABB26-0587-4C30-8999-92F81FD0307C}'   # sem estilo
    tot = sum(larg)
    for i, lw in enumerate(larg): t.columns[i].width = Emu(int(w * lw / tot))
    def cel(c, texto, bold=False, fill=None, color=BLACK, al=PP_ALIGN.LEFT):
        c.text = ''; tf = c.text_frame; tf.word_wrap = True
        r = tf.paragraphs[0].add_run(); r.text = str(texto); r.font.size = Pt(size); r.font.bold = bold; r.font.color.rgb = color
        tf.paragraphs[0].alignment = al
        c.margin_left = c.margin_right = Emu(70000); c.margin_top = c.margin_bottom = Emu(35000); c.vertical_anchor = MSO_ANCHOR.MIDDLE
        if fill is not None: c.fill.solid(); c.fill.fore_color.rgb = fill
        else: c.fill.background()
    for j, h in enumerate(cabec): cel(t.cell(0, j), h, True, RED, WHITE)
    for i, lin in enumerate(linhas, 1):
        for j, v in enumerate(lin):
            num = isinstance(v, str) and v.replace('.', '').replace(',', '').replace('−', '').replace('+', '').replace('-', '').strip().isdigit()
            cel(t.cell(i, j), v, False, LGREY if i % 2 == 0 else WHITE, BLACK, PP_ALIGN.RIGHT if (num and j in numcols) else PP_ALIGN.LEFT)
        t.rows[i].height = Emu(alt)
    t.rows[0].height = Emu(alt)
    return gt

def rodape(sl, texto):
    txt(sl, L, 6330000, W, 250000, texto, size=10, color=GREY)

# ---------------------------------------------------------------- 1. capa
s = p.slides.add_slide(LAY['7_Title A_Campus'])
s.shapes.title.text = 'Conciliação GMS × SAP: de 37.087 m para 774 m de divergência'
for r in s.shapes.title.text_frame.paragraphs[0].runs: r.font.size = Pt(40)
txt(s, L, 3000000, 8000000, 400000, 'Produção Guaratinguetá · período 20/05/2026 a 20/09/2026 · posição em 19/10/2026', size=15, color=GREY)

# ---------------------------------------------------------------- 2. objetivo
s = slide('Objetivo: deixar o GMS como espelho do SAP')
txt(s, L, 1700000, 5400000, 4300000, [
    ('Por que', {'b': True, 'c': RED}),
    'O GMS (apontamento do chão de fábrica) e a MB51 (movimentos de entrada de produção no SAP) deviam mostrar os mesmos metros por OP. No início, os dois estavam muito longe um do outro.',
    ('O que fizemos', {'b': True, 'c': RED}),
    'Comparamos lance a lance, OP por OP, achamos onde cada metro foi parar e corrigimos o GMS para refletir o SAP. O que o SAP errou, ou não lançou, ficou registrado como divergência real, para o SAP corrigir.'], size=15, space=8)
txt(s, 6300000, 1700000, 5400000, 4300000, [
    ('Como medimos', {'b': True, 'c': RED}),
    'Divergência bruta = soma do módulo da diferença (MB51 − GMS) de cada OP.',
    'Só OPs com primeiro lance entre 20/05 e 20/09/2026 (1.082 OPs).',
    'Metros bons e refugo são comparados juntos.',
    ('Fontes', {'b': True, 'c': RED}),
    'SAP MB51 (movimentos 101 e 102) · listas do GMS no SharePoint (lances, refugo, fichas) · BD Packing List (prova independente do que foi embalado) · planilha de Apontamento (refugo por código de defeito).'], size=15, space=8)

# ---------------------------------------------------------------- 3. resultado
s = slide('Resultado: −98% de divergência bruta em 5 dias')
card(s, L, 1700000, 3500000, 1750000, '37.087 m', 'Divergência bruta em 14/10, antes das tratativas')
card(s, L + 3860000, 1700000, 3500000, 1750000, '13.383 m', 'Depois das trocas de OP, reconstruções e remoções')
card(s, L + 7720000, 1700000, 3644000, 1750000, '774 m', 'Hoje, 19/10: 106 das 1.082 OPs ainda divergem', fill=RED, cor=WHITE, leg=WHITE)
cd = CategoryChartData(); cd.categories = ['14/10 (antes)', 'Depois das correções em lote', '19/10 (hoje)']; cd.add_series('Divergência bruta (m)', (37087, 13383, 774))
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Emu(L), Emu(3650000), Emu(6200000), Emu(2650000), cd); ch = gf.chart
ch.has_legend = False; ch.has_title = False
pl = ch.plots[0]; pl.gap_width = 60; pl.has_data_labels = True; pl.data_labels.font.size = Pt(10); pl.data_labels.number_format = '#,##0'; pl.data_labels.number_format_is_linked = False
pl.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
pl.series[0].format.fill.solid(); pl.series[0].format.fill.fore_color.rgb = RED
ch.value_axis.visible = False; ch.value_axis.has_major_gridlines = False; ch.category_axis.tick_labels.font.size = Pt(10)
txt(s, 6900000, 3750000, 4880000, 2500000, [
    ('Hoje restam', {'b': True, 'c': RED}),
    'SAP a mais: 564,5 m',
    'SAP a menos: −209,4 m',
    'Líquido: +355,1 m',
    ('Produção do período: 515.465 m. Divergência bruta de 774 m = 0,15% (era 7,19% em 14/10).', {'b': True}),
    ('Tudo que sobrou tem causa identificada e está nas próximas páginas.', {'s': 13, 'c': GREY})], size=15, space=6)
rodape(s, 'Divergência bruta por OP = soma de |MB51 − GMS| de cada OP no período. Fonte: Conferencia_Lances_por_OP.xlsx, recalculada em 19/10/2026.')

# ---------------------------------------------------------------- 4. regras
s = slide('Regras que combinamos para decidir cada caso')
tabela(s, L, 1650000, W, ['Situação encontrada', 'O que fazemos'], [
    ['Lance está no GMS na OP errada e o SAP lançou em outra OP', 'Mover o lance para a OP do SAP (troca de OP_ID no GMS)'],
    ['OP existe só no SAP', 'Reconstruir a ficha e os lances a partir do SAP, com a observação "Ficha reconstruída a partir do SAP"'],
    ['Lance ou refugo no GMS sem par no SAP e sem prova no BD Packing List', 'Remover do GMS (vai para a lixeira do SharePoint, dá para restaurar)'],
    ['Valor do lance diferente entre GMS e SAP', 'Igualar ao SAP, a não ser que o BD Packing List confirme o valor do GMS'],
    ['Quantidade da ficha diferente da soma dos lances', 'Ficha passa a ser a soma dos lances'],
    ['Refugo lançado duas vezes no SAP', 'Não mexer no GMS: é divergência real, o SAP precisa estornar'],
    ['Produção que o SAP não lançou', 'Não inventar no GMS: registrar como divergência real'],
], [5, 6], size=13, alt=560000)
rodape(s, 'Regra de ouro: o SAP é a verdade. Nada foi apagado em definitivo e nenhuma correção foi feita no SAP.')

# ---------------------------------------------------------------- 5. o que foi feito
s = slide('O que foi feito no GMS')
n = [('200+', 'lances movidos para a OP certa'), ('84', 'lances reconstruídos a partir do SAP'), ('30', 'fichas criadas para OPs que só existiam no SAP'),
     ('28', 'fichas com quantidade acertada (soma dos lances)'), ('22,7 m', 'de refugo lançado a partir da planilha de Apontamento'), ('3', 'packlists reconstruídos em PDF (BD 1072 e 1209)')]
for i, (g, l) in enumerate(n):
    card(s, L + (i % 3) * 3860000, 1700000 + (i // 3) * 2150000, 3640000, 1950000, g, l, gs=32)
rodape(s, 'Registro completo em reconstrucao_gms_2026-10-15.csv, correcoes_gms_2026-10-15.csv e Pendentes_GMS_x_SAP.xlsx.')

# ---------------------------------------------------------------- 6. tipos de erro
s = slide('Onde estavam os 37 mil metros')
tabela(s, L, 1650000, W, ['Tipo de erro', 'Exemplo', 'Tratativa'], [
    ['Lances na OP errada no GMS', '29788690 → 29774579: 13 lances, 521,1 m', 'Mover as OPs no GMS'],
    ['OP cancelada que virou outra', '29115542 → 29133080: 7 lances, 627,7 m', 'Mover para a OP nova'],
    ['OP no GMS com número diferente do SAP', '29791112 → 29805524: 8 lances, 508,4 m', 'Mover e criar a ficha'],
    ['Troca de lances entre duas OPs', '29847619 ↔ 29847701: 4 lances (101,0 · 100,9 · 101,8 · 35,1)', 'Mover os 4 lances, acertar as fichas'],
    ['OP só no SAP, sem nada no GMS', '30092889: 7 lances, 313,5 m', 'Reconstruir ficha e lances'],
    ['Lance sem OP candidata no SAP nem no BD', 'Lances de OPs sem ficha, refugo sem origem', 'Remover do GMS'],
    ['Refugo na OP errada', '29963502 → 29963527: 3 linhas, 2,3 m', 'Mover o refugo no GMS'],
], [3.6, 5.2, 3.2], size=12, alt=560000)

# ---------------------------------------------------------------- 7. exemplo
s = slide('Exemplo: troca de lances 29847619 ↔ 29847701')
tabela(s, L, 1650000, 6700000, ['Packing no BD', 'Peças (m)', 'Total', 'OP certa'], [
    ['958 (13/08 18:21)', '23,0 · 101,0 · 100,1 · 100,9 · 72,8 · 126,3', '524,1', '29847619'],
    ['960 (13/08 19:47)', '110,8 · 93,3 · 105,3 · 28,8 · 101,8 · 35,1', '475,1', '29847701'],
], [2.2, 4.8, 1.2, 1.6], size=12, alt=620000, numcols=(2,))
txt(s, L, 3950000, 6700000, 2300000, [
    ('O que estava errado no GMS', {'b': True, 'c': RED}),
    'Os lances de 101,8 e 35,1 m estavam na 29847619, mas pertencem à 29847701.',
    'Os lances de 101,0 e 100,9 m estavam na 29847701, mas pertencem à 29847619.',
    'A diferença de 65 m na OP era só o saldo dessa troca: (101,0 + 100,9) − (101,8 + 35,1).'], size=14, space=6)
card(s, 7400000, 1650000, 4378000, 2000000, '4 lances', 'Movidos no GMS em 19/10. As fichas 3239 e 3249 passaram a 524,1 m e 475,1 m.')
card(s, 7400000, 3850000, 4378000, 2000000, 'Igual ao SAP', 'O SAP e os dois packings do BD confirmam a divisão. Divergência dessas duas OPs: zero.', fill=LGREY, cor=DARK)

# ---------------------------------------------------------------- 8. validação
s = slide('Como validamos antes de mexer')
txt(s, L, 1700000, 5400000, 4300000, [
    ('BD Packing List', {'b': True, 'c': RED}),
    'É a prova independente do que foi embalado: cada peça (slice) do pallet tem metragem e horário. Quando o BD tem o valor do GMS, o GMS fica como está. Quando tem o valor do SAP, o GMS é corrigido.',
    ('Exemplos de hoje', {'b': True, 'c': RED}),
    '30121886: lance de 36,7 m no GMS, 37,2 m no SAP e no BD (packing 1256). GMS corrigido para 37,2 m.',
    '30122271: lance de 60,2 m no GMS e no BD (packing 1288), 60,8 m no SAP. GMS mantido, 0,6 m de divergência real.'], size=14, space=8)
txt(s, 6300000, 1700000, 5400000, 4300000, [
    ('Planilha de Apontamento', {'b': True, 'c': RED}),
    'Para refugo, confirma se ele existe e com qual código de defeito. Se está lá e não estava no GMS, lançamos no GMS.',
    ('Exemplo', {'b': True, 'c': RED}),
    '30223117, 30078602, 29118845, 29321285 e 29788415: 22,7 m de refugo estavam no Apontamento e no SAP, mas não no GMS. Foram criadas 10 linhas com o código de defeito.',
    '29948511: o GMS está correto, e os 4,45 m extras do SAP seguem como divergência real.'], size=14, space=8)

# ---------------------------------------------------------------- 9. refugo
s = slide('Refugo: o maior bloco do que sobrou')
tabela(s, L, 1650000, W, ['Caso', 'O que encontramos', 'Resultado'], [
    ['Refugo repetido no SAP', 'O mesmo valor foi lançado 2 ou 3 vezes (ex.: 28975553, 32 m ×2; 29048965, 15 m ×3; 29321294, 24,9 m ×2)', 'Divergência real: sem estorno possível'],
    ['Entregas EWM abertas', '6 entregas de saída abertas seguravam refugo; foram excluídas na transação do monitor EWM', 'Resolvido'],
    ['Estorno pelo MBST', 'O documento de material não foi encontrado ("No documents found")', 'Fica como divergência'],
    ['Refugo existe no Apontamento', 'Lançado no GMS: 22,7 m em 5 OPs', 'Resolvido'],
    ['Refugo sem origem', 'Linhas do GMS sem SAP, sem Apontamento e sem OP candidata', 'Removido do GMS'],
], [2.6, 6.6, 2.8], size=12, alt=620000)
rodape(s, 'Refugo lançado no SAP em duplicidade não é erro do GMS; por isso não foi corrigido no GMS.')

# ---------------------------------------------------------------- 10. o que sobrou
s = slide('O que sobrou: 774 m em 106 OPs')
cd = CategoryChartData()
cats = [('Refugo no SAP a mais (90 OPs)', 384.8), ('Produção boa: 29733203, 29862025 e 29847701', 242.9), ('Lance de 51 m duplicado (30078414, 29788884)', 102.0),
        ('Refugo 29949591 sem lançar', 26.8), ('Diferenças pequenas (< 4 m)', 17.4)]
cd.categories = [c for c, _ in cats][::-1]; cd.add_series('m', [v for _, v in cats][::-1])
gf = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Emu(L), Emu(1650000), Emu(7600000), Emu(4500000), cd); ch = gf.chart
ch.has_legend = False; ch.has_title = False
pl = ch.plots[0]; pl.gap_width = 50; pl.has_data_labels = True; pl.data_labels.font.size = Pt(10); pl.data_labels.number_format = '#,##0.0'; pl.data_labels.number_format_is_linked = False
pl.series[0].format.fill.solid(); pl.series[0].format.fill.fore_color.rgb = RED
ch.value_axis.visible = False; ch.value_axis.has_major_gridlines = False; ch.category_axis.tick_labels.font.size = Pt(10)
txt(s, 8300000, 1700000, 3480000, 4400000, [
    ('Leitura', {'b': True, 'c': RED}),
    'Metade do que sobrou é refugo lançado a mais no SAP.',
    'O restante é produção que o SAP não lançou ou lançou em outra OP, e um lance de 51 m duplicado.',
    ('Nada disso se resolve no GMS.', {'b': True})], size=14, space=8)
rodape(s, 'Metros brutos por OP. Fonte: Conferencia_Lances_por_OP.xlsx, 19/10/2026.')

# ---------------------------------------------------------------- 11. divergências reais
s = slide('Divergências reais: o que o SAP precisa corrigir')
tabela(s, L, 1650000, W, ['OP', 'Mangueira', 'm', 'O que é', 'Ação no SAP'], [
    ['29733203', 'GH681-8', '−116,1', 'Produção não lançada no SAP', 'Lançar a produção'],
    ['29862025', 'EC215-08L', '−63,4', 'Produção não lançada no SAP (a 29847701 está com 63,4 a mais)', 'Lançar a produção'],
    ['30078414 e 29788884', 'HC139-7', '51 + 51', 'Lance de 51 m lançado nas duas OPs', 'Estornar uma das duas'],
    ['29949591', 'EC118-06L', '−26,8', 'Refugo que falta lançar', 'Lançar o refugo'],
    ['29086344', '—', 'refugo', 'Refugo repetido', 'Estornar o repetido'],
    ['74 OPs', 'várias', '296,8', 'Mesmo refugo lançado mais de uma vez', 'Estornar o repetido'],
    ['30122271', 'GH493-16', '0,6', 'Lance de 60,8 m no SAP, 60,2 m no GMS e no BD', 'Corrigir para 60,2'],
], [2.3, 1.5, 1.2, 5.0, 2.4], size=12, alt=520000, numcols=(2,))
rodape(s, 'Lista completa, com documentos de material, em Pendentes_GMS_x_SAP.xlsx e Refugo_duplicado_SAP_20mai_20set.xlsx.')

# ---------------------------------------------------------------- 12. próximos passos
s = slide('Próximos passos')
tabela(s, L, 1650000, W, ['Quem', 'O que'], [
    ['SAP / Controladoria', 'Estornar o refugo repetido e o lance de 51 m duplicado; lançar a produção das 29733203 e 29862025 e o refugo da 29949591'],
    ['William', 'Decidir se recriamos no GMS a linha de 2,5 m de refugo da 29935321 (apagada por engano da 30007587) ou se fica como divergência'],
    ['Acompanhamento', 'Repetir a conferência (conferir_lances_por_op.py, ~4 min) quando o SAP corrigir e atualizar o tracker de pendentes'],
], [2.4, 9.6], size=14, alt=780000)

# fim
for lay in ('End',):
    p.slides.add_slide(LAY[lay])
p.save('Tratativas_GMS_x_SAP.pptx')
print('ok', len(p.slides))
