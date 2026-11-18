"""Excel das divergências da ProdHose, uma aba por ação, agrupado por OP.
Uso: python -I gerar_excel_prodhose.py dados_excel_2026-11-18.json dados_tripla_2026-11-18.json Divergencias_ProdHose_2026-11-18.xlsx
"""
import json, sys
from collections import defaultdict
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

E = json.load(open(sys.argv[1], encoding="utf-8"))
T = json.load(open(sys.argv[2], encoding="utf-8"))
SAIDA = sys.argv[3]
ph = {r["m"]: r["ph"] for r in T if r["ph"] > 0.05}

CORR = set(range(21776, 21787)) | set(range(21391, 21399))
FICHA = {"30575954": 4094, "30619643": 4137, "30575840": 4059, "30690631": 4232, "30749038": 4264, "30770798": 4265,
         "30751352": 4355, "30800824": 4459, "30829741": 4487, "30750671": 4267, "30649293": 4495}
MAT_OP = {"30351277": "GH781-4", "30495028": "GH781-10", "30575946": "GH781-12", "30637731": "GH781-6", "30751352": "FC839B-06", "30829741": "GH781-8"}
REFUGO = {"GH781-10", "GH681-12", "FC839B-08", "2556-12"}
ULT = {"EC215-08LRL": "03/08", "EC215-08L": "09/10", "FC735-08": "05/10", "HC101-8": "05/10", "2556-8": "31/08",
       "EC118-10L": "26/08 · 1 doc da OP 29878655 = o saldo", "EC115-10L": "18/06", "GH493-10": "09/10 · 1 doc da OP 30446700 = o saldo",
       "2556-10": "17/09", "12078544": "01/12/2025 · 1 doc da OP 26992559 = o saldo", "2556-3": "28/09", "2556-6": "01/10", "FC639-16": "14/05",
       "GH681-10": "26/06", "FC598-10": "18/09", "FC598-12": "13/10", "GH681-16": "06/10", "FC350-20": "nenhum desde 11/2024",
       "EC600-12": "nenhum desde 11/2024", "FC254-08": "nenhum desde 11/2024", "12055040": "16/10"}

ESCURO = "3C3C3B"; VERM = "E2000F"
COR = {"imprimir": "1F5FA8", "refugo": "C27400", "sap": "E2000F", "parado": "6B4FA0", "trans": "6B6B69"}
fino = Side(style="thin", color="DCDCDA")

def nova(wb, nome, titulo, sub, cor):
    ws = wb.create_sheet(nome)
    ws.sheet_properties.tabColor = cor
    ws.sheet_view.showGridLines = False
    ws["A1"] = titulo; ws["A1"].font = Font(bold=True, size=16, color=cor)
    ws["A2"] = sub; ws["A2"].font = Font(size=10, color="6B6B69")
    ws.row_dimensions[1].height = 26
    return ws

def tabela(ws, nome, cab, linhas, larg, linha0=4, num=(), total=None, estilo="TableStyleMedium2"):
    for j, c in enumerate(cab, 1):
        ws.cell(linha0, j, c)
    for i, l in enumerate(linhas, linha0 + 1):
        for j, v in enumerate(l, 1):
            c = ws.cell(i, j, v)
            c.alignment = Alignment(wrap_text=True, vertical="top")
            if j - 1 in num:
                c.number_format = "#,##0.0"
    fim = linha0 + max(len(linhas), 1)
    t = Table(displayName=nome, ref=f"A{linha0}:{get_column_letter(len(cab))}{fim}")
    t.tableStyleInfo = TableStyleInfo(name=estilo, showRowStripes=True)
    ws.add_table(t)
    for j in range(1, len(cab) + 1):
        ws.cell(linha0, j).alignment = Alignment(wrap_text=True, vertical="center")
    ws.row_dimensions[linha0].height = 32
    for j, w in enumerate(larg, 1):
        ws.column_dimensions[get_column_letter(j)].width = w
    if total:
        r = fim + 1
        ws.cell(r, 1, "Total").font = Font(bold=True)
        for j in total:
            c = ws.cell(r, j + 1, f"=SUBTOTAL(109,{nome}[{cab[j]}])")
            c.font = Font(bold=True); c.number_format = "#,##0.0"
            c.border = Border(top=Side(style="medium", color=ESCURO))
    ws.freeze_panes = ws.cell(linha0 + 1, 1)

def ids_txt(ids):
    ids = sorted(ids)
    out, ini, ant = [], ids[0], ids[0]
    for i in ids[1:] + [None]:
        if i is not None and i == ant + 1:
            ant = i; continue
        out.append(str(ini) if ini == ant else f"{ini}–{ant}")
        if i is not None:
            ini = ant = i
    return ", ".join(out)

wb = Workbook(); wb.remove(wb.active)

# ---------- dados agrupados
ls = [x for x in E["ls"] if x[4] >= "2026-10-06 05:30"]
por_op = defaultdict(lambda: {"ids": [], "m": 0.0, "mat": "", "d0": "9", "d1": ""})
for lid, op, mat, q, dt in ls:
    g = por_op[op]; g["ids"].append(lid); g["m"] += q; g["mat"] = mat; g["d0"] = min(g["d0"], dt); g["d1"] = max(g["d1"], dt)

imprimir, trans = [], []
for op, g in por_op.items():
    corr = any(i in CORR for i in g["ids"])
    dia = g["d0"][8:10] + "/" + g["d0"][5:7] + (" a " + g["d1"][8:10] + "/" + g["d1"][5:7] if g["d1"][:10] != g["d0"][:10] else "")
    if op in ("30575954", "30649293"):
        continue
    if corr or g["d0"] >= "2026-10-15":
        motivo = "Lances criados na conferência (SAP tinha, GMS não)" if corr else "Lances aprovados que nunca foram para pallet"
        imprimir.append([op, FICHA.get(op, "ver no GMS"), g["mat"], len(g["ids"]), round(g["m"], 1), ids_txt(g["ids"]), dia, motivo,
                         "Cabine: imprimir o packlist da ficha" if corr else "Cabine: confirmar o físico e imprimir o packlist"])
    else:
        trans.append([g["mat"], op, len(g["ids"]), round(g["m"], 1), dia, round(ph.get(g["mat"], 0), 1)])
imprimir.sort(key=lambda r: -r[4])
trans.sort(key=lambda r: (r[0], r[4]))

ref_mat = defaultdict(lambda: {"docs": [], "m": 0.0, "d0": "9", "d1": ""})
for m, op, doc, dia, q in E["preso"]:
    g = ref_mat[m]; g["docs"].append((dia, op, doc, q)); g["m"] += q; g["d0"] = min(g["d0"], dia); g["d1"] = max(g["d1"], dia)
baixar = []
for m, g in sorted(ref_mat.items(), key=lambda kv: -kv[1]["m"]):
    det = "; ".join(f"{d[8:]}/{d[5:7]} OP {op} {q:g} m" for d, op, doc, q in sorted(g["docs"]))
    baixar.append([m, round(ph.get(m, 0), 1), round(g["m"], 1), len(g["docs"]), f"{g['d0'][8:]}/{g['d0'][5:7]} a {g['d1'][8:]}/{g['d1'][5:7]}"])
docs = [[m, op, doc, f"{dia[8:]}/{dia[5:7]}/{dia[:4]}", q] for m, op, doc, dia, q in sorted(E["preso"], key=lambda x: (x[0], x[3]))]

lancar = []
for o in sorted(E["sem"], key=lambda o: -sum(x[1] for x in o["semLanc"])):
    s = o["semLanc"]
    mot = defaultdict(float)
    for _, q, m, *_ in s:
        mot[m.split(" - ")[0]] += q
    lancar.append([o["op"], MAT_OP.get(o["op"], ""), o["item"], len(s), round(sum(x[1] for x in s), 2),
                   ", ".join(str(x[0]) for x in s), " · ".join(f"{k} {v:g} m" for k, v in sorted(mot.items(), key=lambda kv: -kv[1])),
                   sorted({x[3][8:] + "/" + x[3][5:7] for x in s})[0], s[0][4].replace("CABINE_", "")])

trans_mat = defaultdict(float)
for r in trans:
    trans_mat[r[0]] += r[3]
sem = []
for r in sorted(T, key=lambda r: -r["ph"]):
    p = r["ph"]
    if p <= 0.05 or r["m"] in REFUGO:
        continue
    resto = p; fl = min(resto, r["pal48"]); resto -= fl; co = min(resto, r["semPal"]); resto -= co
    if resto <= max(0.5, 0.15 * p):
        continue
    antigo = r["ops"] == 0 or r["m"] in ULT
    sem.append(["Antigo" if antigo else "Parado", r["m"], round(p, 1), round(resto, 1), round(trans_mat.get(r["m"], 0), 1),
                ULT.get(r["m"], "em produção"),
                "Sem produção no GMS desde 15/10: estoque velho" if antigo else "Tudo que o GMS apontou desde 15/10 está em pallet: pallet não transferido no EWM ou estoque de antes"])

# ---------- Resumo
ws = nova(wb, "Resumo", "Divergências SAP × GMS × ProdHose", "18/11/2026 · saldo da PROD-GR-HOSE: 8.579 m · MB51 de 18/11 08:06 · GMS ao vivo", ESCURO)
blocos = [
    ("1 · Imprimir packlist", COR["imprimir"], sum(r[4] for r in imprimir), f"{len(imprimir)} OPs", "Cabine", "Imprimir no GMS o packlist das fichas da aba 1"),
    ("2 · Baixar refugo da ProdHose", COR["refugo"], sum(r[2] for r in baixar), f"{len(docs)} docs SAP", "Logística / EWM", "Mover da PROD-GR-HOSE para o refugo"),
    ("3 · Lançar refugo no SAP", COR["sap"], sum(r[4] for r in lancar), f"{len(lancar)} OPs", "Apontador SAP", "Lançar o refugo que o GMS tem e o SAP não"),
    ("4 · Sem explicação", COR["parado"], sum(r[3] for r in sem), f"{len(sem)} materiais", "Logística + export EWM", "Exportar a PROD-GR-HOSE com lote/OP e data de entrada"),
]
ws["A4"] = "O que fazer"; ws["A4"].font = Font(bold=True, size=12)
for j, c in enumerate(["Bloco", "Metros", "Quantos", "Quem", "Ação"], 1):
    x = ws.cell(5, j, c); x.font = Font(bold=True, color="FFFFFF"); x.fill = PatternFill("solid", fgColor=ESCURO)
for i, (b, cor, m, q, quem, acao) in enumerate(blocos, 6):
    ws.cell(i, 1, b).font = Font(bold=True, color=cor, size=12)
    c = ws.cell(i, 2, round(m, 1)); c.number_format = "#,##0.0"; c.font = Font(bold=True, size=12)
    ws.cell(i, 3, q); ws.cell(i, 4, quem); ws.cell(i, 5, acao)
    for j in range(1, 6):
        ws.cell(i, j).border = Border(bottom=fino, left=Side(style="thick", color=cor) if j == 1 else None)
        ws.cell(i, j).alignment = Alignment(vertical="center", wrap_text=True)
    ws.row_dimensions[i].height = 30
for j, w in enumerate([32, 12, 14, 22, 56], 1):
    ws.column_dimensions[get_column_letter(j)].width = w
ws["A11"] = "Como ler"; ws["A11"].font = Font(bold=True, size=12)
notas = ["SAP × GMS bate: 378 de 384 OPs com lance desde 15/10 fecham no metro.",
         "O resto da ProdHose (cerca de 2.700 m) são pallets impressos de 16 a 18/11 ainda não transferidos: saem sozinhos.",
         "O MB51 só tem entradas (101/102). A saída da PROD-GR-HOSE só aparece no EWM; por isso o bloco 4 precisa do export do EWM.",
         "Aba 'Transição 06-14-10': OPs com packlist impresso no papel mas sem registro (falha de permissão em Packing_Pallets de 08 a 15/10; o BD antigo para em 06/10). Só serve de pista para o bloco 4."]
for i, n in enumerate(notas, 12):
    ws.cell(i, 1, "• " + n).alignment = Alignment(wrap_text=False)

# ---------- abas
ws = nova(wb, "1 Imprimir packlist", "1 · Lances aprovados sem packlist", "Uma linha por OP. Cabine imprime pelo GMS (Packing) a ficha indicada.", COR["imprimir"])
tabela(ws, "Imprimir", ["OP", "Ficha", "Material", "Lances", "Metros", "IDs dos lances", "Data", "Por quê", "Ação"], imprimir,
       [11, 9, 13, 8, 10, 26, 13, 34, 38], num=(4,), total=(4,))
ws.cell(ws.max_row + 2, 1, "Fora da lista: OP 30575954 (o metro já saiu por packlist de outra OP) e OP 30649293 (depósito PAE, não passa pela ProdHose).").font = Font(italic=True, color="6B6B69")

ws = nova(wb, "2 Baixar refugo", "2 · Refugo que entrou na ProdHose e não saiu", "Nestes materiais o saldo da ProdHose é exatamente a soma dos refugos lançados (101, usuário U452021). Detalhe por documento abaixo.", COR["refugo"])
tabela(ws, "BaixarResumo", ["Material", "Saldo ProdHose (m)", "Refugo a baixar (m)", "Docs", "Período"], baixar,
       [13, 12, 12, 7, 15], num=(1, 2), total=(2,), estilo="TableStyleMedium3")
r0 = ws.max_row + 3
ws.cell(r0 - 1, 1, "Detalhe por documento do SAP").font = Font(bold=True, size=12)
tabela(ws, "BaixarDocs", ["Material", "OP", "Doc SAP", "Data", "Metros"], docs, [13, 12, 12, 7, 15, 90], linha0=r0, num=(4,), estilo="TableStyleLight10")
ws.freeze_panes = "A5"

ws = nova(wb, "3 Lançar refugo SAP", "3 · Refugo do GMS que o SAP não lançou", "Uma linha por OP. Lançar no SAP; se o refugo não existiu, apagar do GMS.", COR["sap"])
tabela(ws, "Lancar", ["OP", "Material", "Item da lista", "Refugos", "Metros", "IDs no GMS (TiposErros)", "Motivos", "Desde", "Cabine"], lancar,
       [11, 12, 10, 9, 9, 30, 34, 9, 8], num=(4,), total=(4,), estilo="TableStyleMedium4")

ws = nova(wb, "4 Sem explicação", "4 · Saldo da ProdHose que o GMS não explica", "Antigo = sem produção desde 15/10. Parado = material em produção, mas a sobra passa dos pallets das últimas 48 h.", COR["parado"])
tabela(ws, "SemExplicacao", ["Grupo", "Material", "Saldo ProdHose (m)", "Sem explicação (m)", "Pista: transição 06-14/10 (m)", "Último 101 no SAP", "Leitura"], sem,
       [9, 14, 12, 13, 14, 34, 70], num=(2, 3, 4), total=(3,), estilo="TableStyleMedium5")

ws = nova(wb, "Transição 06-14-10", "Pista · OPs da transição sem pallet no GMS", "Não estão no BD Packing List (ele para em 06/10 09:00) nem nos PDFs da biblioteca PackLists (06-08/10). De 08 a 15/10 o Imprimir Ficha imprimia, mas a gravação em Packing_Pallets falhava (E_ACCESSDENIED): o packlist saiu no papel e não ficou registro. Só os materiais com saldo na ProdHose interessam.", COR["trans"])
trans_f = [r for r in trans if r[5] > 0]
grp = defaultdict(list)
for r in trans_f:
    grp[r[0]].append(r)
sem_por_mat = {r[1]: r[3] for r in sem}
trans_m = []
for mat, rs in sorted(grp.items(), key=lambda kv: -ph.get(kv[0], 0)):
    trans_m.append([mat, round(ph.get(mat, 0), 1), round(sem_por_mat.get(mat, 0), 1), len(rs), round(sum(x[3] for x in rs), 1),
                    "; ".join(f"OP {x[1]} {x[3]:g} m ({x[4]})" for x in sorted(rs, key=lambda x: -x[3]))])
tabela(ws, "Transicao", ["Material", "Saldo ProdHose (m)", "Sem explicação (m)", "OPs", "Metros sem registro de pallet", "OPs (metros e data)"], trans_m,
       [14, 12, 12, 6, 14, 110], num=(1, 2, 4), estilo="TableStyleLight1")

wb.active = 0
wb.save(SAIDA)
print("imprimir", len(imprimir), round(sum(r[4] for r in imprimir), 1), "| baixar", round(sum(r[2] for r in baixar), 1),
      "| lancar", round(sum(r[4] for r in lancar), 1), "| sem", len(sem), round(sum(r[3] for r in sem), 1), "| trans", len(trans_m))
