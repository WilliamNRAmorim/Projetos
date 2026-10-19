"""Gera Divergencias_GMS_x_SAP.xlsx (todas as OPs que ainda divergem, 20/05 a 20/09/2026) a partir de
Conferencia_Lances_por_OP.xlsx e Pendentes_GMS_x_SAP.xlsx.
Rodar na pasta Producao_GMS_x_MB51: python -I Apresentação/gerar_excel_divergencias.py"""
import openpyxl, datetime, re, collections
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.formatting.rule import CellIsRule

wb = openpyxl.load_workbook('Conferencia_Lances_por_OP.xlsx', read_only=True)
res = list(wb['Resumo por OP'].iter_rows(values_only=True))[1:]
ini, fim = datetime.datetime(2026, 5, 20), datetime.datetime(2026, 9, 21)
D = {str(r[0]): r for r in res if r[5] and ini <= r[5] < fim and str(r[0]) != '0' and r[11] is not None and abs(r[11]) >= 0.05}
tot_ops = sum(1 for r in res if r[5] and ini <= r[5] < fim and str(r[0]) != '0')
sem_par = collections.defaultdict(list); todas = collections.defaultdict(list)
for r in wb['Linha a linha'].iter_rows(values_only=True):
    op = str(r[0])
    if op not in D: continue
    todas[op].append(r)
    if not str(r[9]).startswith('Casado'): sem_par[op].append(r)

tr = {}
for r in list(openpyxl.load_workbook('Pendentes_GMS_x_SAP.xlsx', read_only=True)['Pendentes'].iter_rows(values_only=True))[1:]:
    if not r[0]: continue
    for op in set(re.findall(r'\d{8}', ' '.join(str(c) for c in (r[2], r[3]) if c))):
        tr.setdefault(op, []).append(f'{r[0]} ({r[10]})')

PROD = 'Produção boa não lançada / OP diferente no SAP'
GRUPOS = {'29733203': PROD, '29862025': PROD, '29847701': PROD, '30078414': 'Lance de 51 m duplicado no SAP', '29788884': 'Lance de 51 m duplicado no SAP',
          '29949591': 'Refugo que falta lançar no SAP', '30122271': 'Lance de valor diferente (BD confirma o GMS)'}

def classe(op):
    r = D[op]
    if op in GRUPOS: return GRUPOS[op], 'SAP'
    if any(l[4] in ('boa', 'estorno') for l in sem_par[op]): return 'Diferença pequena de lance', 'SAP'
    if r[11] > 0:
        sap = collections.Counter(round(l[6], 2) for l in todas[op] if l[3] == 'MB51' and l[4] == 'refugo')
        extra = [round(l[6], 2) for l in sem_par[op] if l[3] == 'MB51' and l[4] == 'refugo']
        casados = {round(l[6], 2) for l in todas[op] if l[3] == 'MB51' and l[4] == 'refugo' and str(l[9]).startswith('Casado')}
        rep = any(sap[v] > 1 or v in casados for v in extra)
        return ('Refugo repetido no SAP' if rep else 'Refugo no SAP sem par no GMS'), 'SAP'
    return 'Refugo do GMS sem lançamento no SAP', 'GMS / SAP'

AZ = PatternFill('solid', fgColor='ED071B'); BR = Font(color='FFFFFF', bold=True, name='Segoe UI', size=10); FN = Font(name='Segoe UI', size=10)
FB = Font(name='Segoe UI', size=10, bold=True)
out = openpyxl.Workbook()

def tabela(ws, nome, ncols):
    t = Table(displayName=nome, ref=f'A1:{get_column_letter(ncols)}{ws.max_row}')
    t.tableStyleInfo = TableStyleInfo(name='TableStyleLight1', showRowStripes=True); ws.add_table(t)

ws = out.active; ws.title = 'Divergências por OP'
cab = ['OP', 'Mangueira', 'Material SAP', '1º lance GMS', 'Último lance GMS', 'GMS boa (m)', 'GMS refugo (m)', 'GMS total (m)', 'SAP líquido (m)', 'Diferença SAP − GMS (m)',
       'Sentido', '|Diferença| (m)', 'Categoria', 'Quem corrige', 'Documentos SAP sem par', 'Tracker', 'Lances GMS', 'Lanç. SAP']
ws.append(cab)
for op, r in sorted(D.items(), key=lambda x: -abs(x[1][11])):
    cat, quem = classe(op)
    docs = '; '.join(sorted({str(l[7]).replace('Doc ', '') for l in sem_par[op] if l[3] == 'MB51' and 'Doc' in str(l[7])}))[:250]
    ws.append([int(op), r[1], r[2], r[5], r[6], r[7], r[8], r[9], r[10], round(r[11], 2), 'SAP a mais' if r[11] > 0 else 'SAP a menos', round(abs(r[11]), 2), cat, quem, docs, '; '.join(tr.get(op, [])), r[12], r[13]])
for c in ws[1]: c.fill = AZ; c.font = BR; c.alignment = Alignment(wrap_text=True, vertical='center')
for row in ws.iter_rows(min_row=2):
    for c in row: c.font = FN
    row[3].number_format = row[4].number_format = 'dd/mm/yyyy'
    for i in (5, 6, 7, 8, 9, 11): row[i].number_format = '#,##0.0'
for i, w in enumerate([11, 15, 15, 12, 12, 11, 11, 11, 11, 13, 11, 12, 44, 12, 40, 28, 9, 9], 1): ws.column_dimensions[get_column_letter(i)].width = w
ws.row_dimensions[1].height = 34; ws.freeze_panes = 'C2'; tabela(ws, 'Divergencias', len(cab))
ws.conditional_formatting.add(f'J2:J{ws.max_row}', CellIsRule(operator='lessThan', formula=['0'], font=Font(color='1F6FB2', bold=True)))
ws.conditional_formatting.add(f'J2:J{ws.max_row}', CellIsRule(operator='greaterThan', formula=['0'], font=Font(color='ED071B', bold=True)))

wl = out.create_sheet('Linhas sem par')
cab2 = ['OP', 'Mangueira', 'Lado', 'Tipo', 'Data', 'Qtd (m)', 'Referência (lance GMS / doc SAP)', 'Trançadeira / usuário SAP / defeito', 'Situação', 'Categoria da OP']
wl.append(cab2)
for op in sorted(D, key=lambda o: -abs(D[o][11])):
    cat, _ = classe(op)
    for l in sem_par[op]:
        wl.append([int(op), l[1], l[3], l[4], l[5], l[6], str(l[7]), str(l[8]), str(l[9]), cat])
for c in wl[1]: c.fill = AZ; c.font = BR
for row in wl.iter_rows(min_row=2):
    for c in row: c.font = FN
    row[4].number_format = 'dd/mm/yyyy hh:mm'; row[5].number_format = '#,##0.0'
for i, w in enumerate([11, 15, 8, 9, 16, 9, 30, 34, 40, 44], 1): wl.column_dimensions[get_column_letter(i)].width = w
wl.freeze_panes = 'A2'; tabela(wl, 'Linhas', len(cab2))

wr = out.create_sheet('Resumo', 0)
wr['A1'] = 'Divergência GMS x SAP (MB51): OPs com 1º lance de 20/05 a 20/09/2026'; wr['A1'].font = Font(name='Segoe UI', size=14, bold=True)
wr['A2'] = f'Posição em 19/10/2026. {tot_ops} OPs no período, {len(D)} ainda divergem.'; wr['A2'].font = FN
for j, h in enumerate(['Categoria', 'OPs', 'SAP a mais (m)', 'SAP a menos (m)', '|Total| (m)', 'Quem corrige'], 1):
    c = wr.cell(4, j, h); c.fill = AZ; c.font = BR
agg = {}
for op, r in D.items():
    cat, quem = classe(op); a = agg.setdefault(cat, [0, 0.0, 0.0, quem]); a[0] += 1
    if r[11] > 0: a[1] += r[11]
    else: a[2] += r[11]
lin = 5
for cat, a in sorted(agg.items(), key=lambda x: -(x[1][1] - x[1][2])):
    for j, v in enumerate([cat, a[0], round(a[1], 1), round(a[2], 1), round(a[1] - a[2], 1), a[3]], 1):
        c = wr.cell(lin, j, v); c.font = FN
        if 3 <= j <= 5: c.number_format = '#,##0.0'
    lin += 1
for j, v in enumerate(['Total', f'=SUM(B5:B{lin-1})', f'=SUM(C5:C{lin-1})', f'=SUM(D5:D{lin-1})', f'=SUM(E5:E{lin-1})'], 1):
    c = wr.cell(lin, j, v); c.font = FB
    if 3 <= j <= 5: c.number_format = '#,##0.0'
lin += 2
wr.cell(lin, 1, 'Evolução da divergência bruta (soma de |dif| por OP)').font = Font(name='Segoe UI', size=11, bold=True)
bruta = round(sum(abs(r[11]) for r in D.values()), 1)
for i, (a, b) in enumerate([('14/10 (antes das tratativas)', 37087), ('Depois das correções em lote', 13383), ('19/10 (hoje)', bruta)], 1):
    wr.cell(lin + i, 1, a).font = FN; c = wr.cell(lin + i, 2, b); c.font = FN; c.number_format = '#,##0.0'
prod = sum(r[9] for r in res if r[5] and ini <= r[5] < fim and str(r[0]) != '0' and r[9] is not None)
l2 = lin + 5
wr.cell(l2, 1, 'Divergência sobre a produção do período').font = Font(name='Segoe UI', size=11, bold=True)
for i, (a, b, f) in enumerate([('Produção total no GMS (m)', round(prod, 1), '#,##0.0'), ('Divergência bruta hoje (m)', bruta, '#,##0.0'), ('% da produção', bruta / prod, '0.00%'),
                               ('% em 14/10 (37.087 m)', 37087 / prod, '0.00%')], 1):
    wr.cell(l2 + i, 1, a).font = FN; c = wr.cell(l2 + i, 2, b); c.font = FN; c.number_format = f
for i, w in enumerate([52, 12, 16, 16, 14, 14], 1): wr.column_dimensions[get_column_letter(i)].width = w
out.save('Apresentação/Divergencias_GMS_x_SAP.xlsx'); print('ok', len(D), bruta)
for cat, a in agg.items(): print(cat, a)
