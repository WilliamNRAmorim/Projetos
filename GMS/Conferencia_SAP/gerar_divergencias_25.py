# Divergencias_ProdHose_2026-11-25.xlsx no formato do Divergencias_ProdHose_2026-11-18_v3.xlsx (uma aba por acao).
# Saldo: EXPORT_20261125_125249.xlsx (08:52). SAP: mb51.xlsx de 25/11 06:21. GMS: listas lidas em 25/11.
import openpyxl
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from openpyxl.utils import get_column_letter as L
from openpyxl.worksheet.table import Table, TableStyleInfo

AQUI = Path(__file__).resolve().parent
V3 = AQUI / "Divergencias_ProdHose_2026-11-18_v3.xlsx"
EXP = AQUI.parent / "Analises" / "ProdHose_Teste" / "EXPORT_20261125_125249.xlsx"
SAIDA = AQUI / "Divergencias_ProdHose_2026-11-25.xlsx"
COR = {"imprimir": "1F5FA8", "refugo": "C27400", "sap": "E2000F", "parado": "6B4FA0", "trans": "6B6B69", "ok": "2E7D32"}

it = list(openpyxl.load_workbook(EXP, data_only=True).worksheets[0].iter_rows(values_only=True)); ix = {}
for i, n in enumerate(it[0]): ix.setdefault(n, i)
saldo, tot = {}, {}
for r in it[1:]:
    m = r[ix["Product"]]
    if not m: continue
    d, st = str(r[ix["Document"]] or ""), str(r[ix["Description of Stock Type"]])
    g = "PDI " + d if r[ix["Document Category"]] else "Bloqueado" if "Blocked" in st else "Inspeção" if "QI" in st else "Livre"
    x = saldo.setdefault((m, g), [0.0, r[ix["Goods Receipt Date"]]]); x[0] += float(r[ix["Quantity"]])
    tot[m] = tot.get(m, 0) + float(r[ix["Quantity"]])
livre = lambda m: round(saldo.get((m, "Livre"), [0])[0], 3)
v3 = openpyxl.load_workbook(V3)


def nova(wb, nome, tit, sub, cor):
    ws = wb.create_sheet(nome); ws.sheet_properties.tabColor = cor; ws.sheet_view.showGridLines = False
    ws["A1"], ws["A2"] = tit, sub
    ws["A1"].font, ws["A2"].font = Font(bold=True, size=16, color=cor), Font(size=10, color="6B6B69")
    ws.row_dimensions[1].height = 26; ws.freeze_panes = "A5"
    ws.page_setup.orientation = "landscape"; ws.page_setup.fitToHeight = 0; ws.sheet_properties.pageSetUpPr = openpyxl.worksheet.properties.PageSetupProperties(fitToPage=True)
    return ws


def tabela(ws, nome, cab, lin, larg, l0=4, num=(), total=None, estilo="TableStyleMedium2"):
    for j, c in enumerate(cab, 1):
        ws.cell(l0, j, c).alignment = Alignment(wrap_text=True, vertical="center")
        if larg: ws.column_dimensions[L(j)].width = larg[j - 1]
    ws.row_dimensions[l0].height = 32
    for i, l in enumerate(lin, l0 + 1):
        for j, v in enumerate(l, 1):
            c = ws.cell(i, j, v); c.alignment = Alignment(wrap_text=True, vertical="top")
            if j - 1 in num: c.number_format = "#,##0.0"
    fim = l0 + len(lin)
    t = Table(displayName=nome, ref=f"A{l0}:{L(len(cab))}{fim}"); t.tableStyleInfo = TableStyleInfo(name=estilo, showRowStripes=True); ws.add_table(t)
    if total is not None:
        ws.cell(fim + 1, 1, "Total").font = Font(bold=True)
        c = ws.cell(fim + 1, total + 1, f"=SUBTOTAL(109,{nome}[{cab[total]}])"); c.font = Font(bold=True); c.number_format = "#,##0.0"
    return fim + 1


def nota(ws, r, txt): ws.cell(r, 1, txt).font = Font(size=10, color="6B6B69")


wb = Workbook(); wb.remove(wb.active)
# ---- 1
CRI = "Lances criados na conferência (SAP tinha, GMS não)"
def ac(p): return f"1) Achar o material na ProdHose. 2) Achou: imprimir o pallet {p} em Consulta de OP > Packlists da OP. 3) Logística transfere. Não achou: NÃO imprimir; avisar a supervisão"
IMP = [("30478616", 3983, "GH493-8", 6, 492.2, "18475–18480", "15/10", "Lances aprovados que nunca foram para pallet", f"ATENÇÃO: o saldo do material é só {livre('GH493-8'):.1f} m. Contar no físico antes; só o que existir vai para packlist"),
       ("30750671", 4267, "GH493-16", 8, 166.6, "21391–21398", "11/11", CRI, f"ATENÇÃO: o saldo é só {livre('GH493-16'):.1f} m, para 218,7 m desta OP. " + ac(2)),
       ("30750671", 4267, "GH493-16", 1, 52.1, "20905", "07/11", "Packlist do pallet 1 saiu com 1,0 m; o lance tem 53,1 m", f"ATENÇÃO: o saldo é só {livre('GH493-16'):.1f} m. Conferir a etiqueta do rolo; se for 53,1 m, reimprimir o pallet 1"),
       ("30619643", 4137, "FC735-12", 1, 106.1, "21779", "26/10", CRI, ac(2)),
       ("30829741", 4487, "GH781-8", 1, 73.4, "21786", "13/11", CRI, f"ATENÇÃO: o saldo é {livre('GH781-8'):.1f} m, para 88,8 m das duas OPs. " + ac(3)),
       ("30770798", 4265, "GH493-8", 1, 40.7, "21783", "06/11", CRI, ac(3)),
       ("30690631", 4232, "GH781-4", 1, 37.0, "21781", "04/11", CRI, ac(2)), ("30575840", 4059, "GH781-4", 1, 35.4, "21780", "27/10", CRI, ac(2)),
       ("30751352", 4355, "FC839B-06", 1, 28.9, "21784", "09/11", CRI, ac(2)), ("30749038", 4264, "EC415-16", 1, 26.1, "21782", "05/11", CRI, ac(3)),
       ("30800824", 4459, "GH781-8", 1, 15.4, "21785", "11/11", CRI, f"ATENÇÃO: o saldo é {livre('GH781-8'):.1f} m, para 88,8 m das duas OPs. " + ac(2))]
ws = nova(wb, "1 Imprimir packlist", "1 · Lances aprovados sem packlist", "Uma linha por OP. Só imprimir depois de achar o material. Quem: Cabine e Logística.", COR["imprimir"])
r = tabela(ws, "Imprimir", ["OP", "Ficha", "Material", "Lances", "Metros", "IDs dos lances", "Data", "Por quê", "Ação"], IMP, [11, 9, 13, 8, 10, 16, 9, 34, 62], num=(4,), total=4)
nota(ws, r + 2, "Fora da lista: OP 30575954 (o metro já saiu por packlist de outra OP): NÃO imprimir o pallet 2 (registro 532) que existe no GMS. OP 30649293: depósito PAE.")
nota(ws, r + 3, "Os pallets citados foram registrados no GMS em 23/11 sem impressão. A soma passa do saldo em GH493-8, GH493-16 e GH781-8: parte não está lá.")
# ---- 2
old = [tuple(c.value for c in x) for x in v3["2 Baixar refugo"].iter_rows(min_row=13, max_row=50, max_col=5)]
FORA = {"3031105063/1", "3031104931/1", "3031104873/1", "3031247482/1"}      # GH781-10 de 16 e 17/11: baixados
DOC = [o for o in old if o[2] not in FORA]
DOC += [(m, op, d, dt, q) for m, op, d, dt, q in [
    ("GH781-12", "30575946", "3031562600/1", "19/11/2026", 1.2), ("GH781-12", "30900106", "3031840694/1", "23/11/2026", 4.8), ("GH781-12", "30900101", "3031840741/1", "23/11/2026", 4.9),
    ("GH781-12", "30860017", "3031840744/1", "23/11/2026", 4.5), ("GH781-12", "30885837", "3031840746/1", "23/11/2026", 1.0), ("GH781-12", "30842515", "3031840793/1", "23/11/2026", 1.4),
    ("GH781-12", "30860018", "3031990060/1", "24/11/2026", 11.5), ("GH781-12", "30900102", "3031990061/1", "24/11/2026", 6.5), ("GH781-12", "30900103", "3031990366/1", "24/11/2026", 1.2),
    ("EC215-12L", "30885836", "3031840672/1", "23/11/2026", 11.16), ("EC215-12L", "30885835", "3031840584/1", "23/11/2026", 1.0),
    ("GH781-4", "30860262", "3031840749/1", "23/11/2026", 4.6), ("GH781-4", "30885825", "3031840745/1", "23/11/2026", 4.5),
    ("EC115-06L", "30914923", "3031840792/1", "23/11/2026", 5.6), ("GH781-6", "30637731", "3031563083/1", "19/11/2026", 4.8), ("FC839B-06", "30751352", "3031563387/1", "19/11/2026", 2.5)]]
ref = {}
for m, _, _, dt, q in DOC: ref.setdefault(m, []).append((dt, q))
COMO = {"GH781-10": "Saldo é todo refugo. Baixar os documentos abaixo; eles somam 157,8 m, 0,9 m a mais que o saldo: conferir 0,9 m já baixado",
        "GH781-12": "Parte do saldo. Contas de 23 a 25/11 fecham com estes documentos", "GH781-4": "Parte do saldo", "GH781-6": "Parte do saldo", "FC839B-06": "Parte do saldo"}
chave = lambda s: s[6:] + s[3:5] + s[:2]
RES = []
for m, v in ref.items():
    q = round(sum(x for _, x in v), 2); ds = sorted((d for d, _ in v), key=chave)
    RES.append((m, round(livre(m), 2), min(q, round(livre(m), 2)), len(v), f"{ds[0][:5]} a {ds[-1][:5]}", COMO.get(m, "Saldo é exatamente este refugo. Baixar tudo")))
RES.sort(key=lambda x: -x[2])
ws = nova(wb, "2 Baixar refugo", "2 · Refugo que entrou na ProdHose e não saiu", "Quem: Qualidade / SAP. Baixar no SAP pelo documento abaixo. Cobrança à parte: não é produção boa presa.", COR["refugo"])
r = tabela(ws, "BaixarResumo", ["Material", "Saldo ProdHose (m)", "Refugo a baixar (m)", "Docs", "Período", "Como tratar"], RES, [13, 12, 15, 11, 15, 90], num=(1, 2), total=2, estilo="TableStyleMedium3")
ws.cell(r + 2, 1, "Detalhe por documento do SAP").font = Font(bold=True, size=12)
DOC.sort(key=lambda d: (-sum(x for _, x in ref[d[0]]), d[0], chave(d[3])))
r2 = tabela(ws, "BaixarDocs", ["Material", "OP", "Doc SAP", "Data", "Metros"], DOC, None, l0=r + 3, num=(4,), estilo="TableStyleLight10")
for q in range(r + 4, r2): ws.cell(q, 3).alignment = Alignment(vertical="top")
ws.column_dimensions["C"].width = 18; ws.column_dimensions["D"].width = 12
# ---- 3
ws = nova(wb, "3 Lançar refugo SAP", "3 · Refugo do GMS que o SAP não lançou", "Uma linha por OP. Lançar no SAP; se o refugo não existiu, apagar do GMS. Quem: Qualidade / SAP.", COR["sap"])
r = tabela(ws, "Lancar", ["OP", "Material", "Item da lista", "Refugos", "Metros", "IDs no GMS (TiposErros)", "Motivos", "Desde", "Cabine"],
           [("30351277", "GH781-4", 67, 4, 6.4, "5755, 5756, 5757, 5760", "B 3,4 m · C 3,0 m", "05/10", "L1"), ("30842762", "GH781-4", 364, 3, 2.8, "7521, 7522, 7523", "O 2,0 m · C 0,4 m · E 0,4 m", "16/11", "L1")],
           [11, 12, 10, 9, 10, 30, 34, 9, 8], num=(4,), total=4, estilo="TableStyleMedium4")
nota(ws, r + 2, "Da lista de 18/11: 30495028, 30637731, 30751352 e 30575946 foram lançados no SAP em 19/11; 30829741 e o refugo 5761 (26,5 m) saíram do GMS.")
# ---- 4
exp1 = {}
for x in IMP: exp1[x[2]] = exp1.get(x[2], 0) + x[4]
TRANS = {"GH781-12": 776.6}
so_ref = {x[0] for x in RES if x[0] not in ("GH781-12", "GH781-4", "GH781-6", "FC839B-06")}
pr = {m: sum(q for _, q in v) for m, v in ref.items() if m not in so_ref}
ULT = {x[1].value: x[5].value for x in v3["4 Sem explicação"].iter_rows(min_row=5, max_row=35) if x[5].value and x[5].value != "em produção"}
ULT["EC215-08LRL"] = "03/08"; ULT.pop("FC735-08", None)
PISTA = {x[0].value: x[4].value for x in v3["Transição 06-14-10"].iter_rows(min_row=5, max_row=15)}
ANT = "Contar no físico. Achou: transferir da ProdHose. Não achou: PCP / inventário decide o ajuste"
PAR = "Contar no físico e separar os pallets do dia. O resto: achar o packlist e transferir; sem packlist, PCP decide"
SEM = []
for (m, g), (q, d) in saldo.items():
    if g == "Livre":
        if m in so_ref: continue
        q = q - exp1.get(m, 0) - pr.get(m, 0) - TRANS.get(m, 0)
        if q < 0.5: continue
        gr, le = ("Antigo", ANT) if m in ULT else ("Parado", PAR)
    elif g == "Bloqueado": gr, le = "Bloqueado", "Qualidade decide: liberar ou refugar, e tirar da ProdHose"
    elif g == "Inspeção": gr, le = "Inspeção", "Qualidade conclui a inspeção e libera ou refuga"
    else: gr, le = "Com documento", f"Expedição: verificar o documento {g[4:]} e concluir ou cancelar; depois tirar da ProdHose"
    if m == "GH781-12": le = "Já estava antes de 18/11. " + PAR
    SEM.append((gr, m, round(tot[m], 2), round(q, 2), PISTA.get(m, 0), ULT.get(m) if gr == "Antigo" else f"entrada no EWM {d:%d/%m/%Y}", le))
SEM.sort(key=lambda x: -x[3])
ws = nova(wb, "4 Sem explicação", "4 · Saldo da ProdHose que o GMS não explica", "Antigo = sem produção recente. Parado = material em produção. Quem: Logística conta; PCP decide. Comece de cima: os maiores saldos.", COR["parado"])
r = tabela(ws, "SemExplicacao", ["Grupo", "Material", "Saldo ProdHose (m)", "Sem explicação (m)", "Pista: transição 06-14/10 (m)", "Último 101 no SAP", "Leitura"], SEM, [15, 14, 14.7, 14, 16, 34, 70], num=(2, 3, 4), total=3, estilo="TableStyleMedium5")
nota(ws, r + 2, "Já descontados: aba 1, aba 2 e os 776,6 m de GH781-12 em trânsito. O material da coluna C inclui tudo (livre, bloqueado e documento).")
# ---- 5
ws = nova(wb, "5 Corrigir no SAP", "5 · Lançamento errado no SAP", "Uma linha por OP. Não é material preso: é cadastro. Quem: SAP / PCP.", COR["sap"])
tabela(ws, "Corrigir", ["OP", "Material", "Metros", "Item da lista", "Doc SAP", "O que está errado", "Ação"], [
    ("30860262", "GH781-4", 129.1, "377 e 378", "3031623382", "O lance 21902 é da OP 30885825 (ficha de 1.080 m, pallet 2)", "Estornar (102) na 30860262 e lançar 101 de 129,1 m na 30885825"),
    ("30803594", "GH781-4", 15.3, "321", "3030914931", "SAP 15,3 m acima do GMS. Provável refugo em dobro: o GMS tem 17,5 m de refugo, igual ao lote", "Conferir os lançamentos da OP e estornar os 15,3 m repetidos"),
    ("30482097", "GH681-8", 66.8, "376", "3027688835", f"SAP de 08/10 sem OP no GMS. O saldo do material é {tot['GH681-8']:.1f} m: o resto já saiu", "Confirmar se foi produzido: regularizar no GMS ou estornar"),
    ("30872771", "GH681-4", 1.0, "359", "sem doc", "Lance 21739 (1,0 m) apontado depois do lançamento", "Conferir se existe: lançar no SAP ou excluir no GMS")],
    [11, 12, 10, 13, 16, 58, 58], num=(2,), total=2, estilo="TableStyleMedium4")
# ---- 6
ws = nova(wb, "6 Confirmar pallet", "6 · Pallets para confirmar", "Em trânsito = produzido hoje. Repetido = os mesmos lances em mais de um pallet no GMS. Quem: Cabine e Logística.", COR["ok"])
tabela(ws, "Confirmar", ["OP", "Material", "Tipo", "Pallets (registro)", "Metros", "Situação", "Ação"], [
    ("30930300", "GH781-12", "Em trânsito", "572", 390.3, "Impresso 25/11 07:28", "Confirmar a saída em 26/11. Continuou no saldo: está preso"),
    ("30915070", "GH781-12", "Em trânsito", "573", 406.8, "Impresso 25/11 08:59; 386,3 m já na foto", "Confirmar a saída em 26/11. Continuou no saldo: está preso"),
    ("30885826", "GH781-4", "Repetido", "543, 544, 545 e 546", 818.7, "Três iguais; o 546 tem um lance apagado (1,0 m)", "Ver quantos packlists saíram no papel e recolher os repetidos"),
    ("30885827", "GH781-4", "Repetido", "561 e 562", 335.0, "Os 335,0 m do 562 já estão no 561", "Ver quantos packlists saíram no papel e recolher os repetidos"),
    ("30885821", "GH781-8", "Repetido", "564 e 566", 418.4, "Os 418,4 m do 566 já estão no 564", "Ver quantos packlists saíram no papel e recolher os repetidos"),
    ("30900101", "GH781-12", "Repetido", "519, 520, 521 e 522", 349.1, "O 520 e o 521 são partes do 519; o 522 tem um lance apagado", "Ver quantos packlists saíram no papel e recolher os repetidos"),
    ("30872771", "GH681-4", "Repetido", "497, 498 e 499", 688.8, "Os três têm os mesmos lances", "Ver quantos packlists saíram no papel e recolher os repetidos"),
    ("30575954", "HC139-7_S-GX", "Não imprimir", "532", 145.5, "Registrado em 23/11 por engano: o metro já saiu por outra OP", "Não imprimir")],
    [11, 14, 13, 20, 10, 48, 58], num=(4,), estilo="TableStyleMedium7")
# ---- Transicao
sx = {}
for x in SEM: sx[x[1]] = sx.get(x[1], 0) + x[3]
ws = nova(wb, "Transição 06-14-10", v3["Transição 06-14-10"]["A1"].value, v3["Transição 06-14-10"]["A2"].value, COR["trans"])
TRA = [(x[0].value, round(tot.get(x[0].value, 0), 2), round(sx.get(x[0].value, 0), 2), x[3].value, x[4].value, x[5].value) for x in v3["Transição 06-14-10"].iter_rows(min_row=5, max_row=15) if tot.get(x[0].value, 0) > 0.5]
tabela(ws, "Transicao", ["Material", "Saldo ProdHose (m)", "Sem explicação (m)", "OPs", "Metros sem registro de pallet", "OPs (metros e data)"], TRA, [14, 12, 14, 6, 18.6, 109.7], num=(1, 2, 4), estilo="TableStyleLight1")
wb.save(SAIDA)
print(SAIDA.name, "| aba1", round(sum(x[4] for x in IMP), 1), "| aba2", round(sum(x[2] for x in RES), 1), "| aba4", round(sum(x[3] for x in SEM), 1), len(SEM), "| total", round(sum(tot.values()), 1))
c1 = sum(min(exp1[m], livre(m)) for m in exp1); print("prova:", round(c1 + sum(x[2] for x in RES) + sum(x[3] for x in SEM) + 776.6, 1), "x", round(sum(tot.values()), 1))
for x in RES: print(x[:5])
