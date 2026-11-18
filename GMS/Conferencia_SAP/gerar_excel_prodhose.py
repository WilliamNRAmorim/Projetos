"""Excel das divergências da ProdHose: sem packlist, refugo a tratar, sem explicação.
Uso: python -I gerar_excel_prodhose.py dados_excel_2026-11-18.json dados_tripla_2026-11-18.json Divergencias_ProdHose_2026-11-18.xlsx
"""
import json, sys
from collections import defaultdict
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

E = json.load(open(sys.argv[1], encoding="utf-8"))
T = json.load(open(sys.argv[2], encoding="utf-8"))
SAIDA = sys.argv[3]
ph = {r["m"]: r["ph"] for r in T if r["ph"] > 0.05}

CORRIGIDOS = set(range(21776, 21787)) | set(range(21391, 21399)) | {20905, 21290}
FICHA = {"30575954": 4094, "30619643": 4137, "30575840": 4059, "30690631": 4232, "30749038": 4264, "30770798": 4265,
         "30751352": 4355, "30800824": 4459, "30829741": 4487, "30750671": 4267, "30649293": 4495}

wb = Workbook()
CAB = PatternFill("solid", fgColor="3C3C3B"); BR = Font(color="FFFFFF", bold=True)
VERM = PatternFill("solid", fgColor="FDE8E9"); AMAR = PatternFill("solid", fgColor="FBF0DE"); AZUL = PatternFill("solid", fgColor="E8EEF7"); CINZA = PatternFill("solid", fgColor="F0F0EE")

def aba(ws, titulo, nota, cab, linhas, larg, fill_col=None):
    ws.append([titulo]); ws["A1"].font = Font(bold=True, size=14)
    ws.append([nota]); ws["A2"].font = Font(italic=True, color="6B6B69")
    ws.append([])
    ws.append(cab)
    for c in ws[4]:
        c.fill, c.font, c.alignment = CAB, BR, Alignment(wrap_text=True, vertical="center")
    for l in linhas:
        ws.append(l[0] if isinstance(l, tuple) else l)
        if isinstance(l, tuple) and l[1]:
            for c in ws[ws.max_row]:
                c.fill = l[1]
    for i, w in enumerate(larg, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A5"
    ws.auto_filter.ref = f"A4:{get_column_letter(len(cab))}{ws.max_row}"
    for row in ws.iter_rows(min_row=5):
        for c in row:
            if isinstance(c.value, float):
                c.number_format = "#,##0.00"

# 1) sem packlist
ls = [x for x in E["ls"] if x[4] >= "2026-10-06 05:30"]
lin1 = []
for lid, op, mat, q, dt in sorted(ls, key=lambda x: (x[0] not in CORRIGIDOS, x[4])):
    if lid in CORRIGIDOS:
        if op == "30649293":
            tipo, acao, f = "Correção 12/11 (depósito PAE)", "Não vai para a ProdHose: nada a fazer", CINZA
        elif op == "30575954":
            tipo, acao, f = "Correção 18/11 (lote 3)", "Não imprimir: o metro já saiu por packlist de outra OP", CINZA
        else:
            tipo, acao, f = "Correção (lote 3 ou OP 30750671)", f"Imprimir packlist da ficha {FICHA.get(op, '?')}", AZUL
    elif dt >= "2026-10-15":
        tipo, acao, f = "Produção sem pallet", "Conferir com a cabine e imprimir o packlist", VERM
    else:
        tipo, acao, f = "Transição 06-14/10 (packlist antigo apagado em 08/10)", "Candidato ao saldo sem explicação: ver se está na prateleira", AMAR
    lin1.append(([lid, op, mat, round(q, 2), dt, round(ph.get(mat, 0), 2), tipo, acao], f))
aba(wb.active, "1. Lances aprovados que não foram para o packlist do GMS",
    "Desde 06/10 (início do Packing_Pallets). Lance = RegistrosInspeção; pallet = Packing_Pallets.LanceIDs. Saldo ProdHose = do material, colado em 18/11.",
    ["ID lance", "OP", "Material", "Metros", "Data/hora", "Saldo ProdHose do material (m)", "Tipo", "Ação"], lin1, [10, 11, 15, 9, 17, 14, 40, 58])
wb.active.title = "1 Sem packlist"

# 2) refugo
ws2 = wb.create_sheet("2 Refugo")
lin2 = []
for m, op, doc, dia, q in E["preso"]:
    lin2.append(([m, op, f"doc SAP {doc}", dia, round(q, 2), "", "Refugo lançado no SAP (101, U452021) que continua na PROD-GR-HOSE",
                  "Baixar da PROD-GR-HOSE no EWM (mover para o refugo/sucata)"], AMAR))
for o in E["sem"]:
    for rid, q, mot, dt, cab, tr in o["semLanc"]:
        lin2.append(([o["op"], o["op"], f"refugo GMS Id {rid}", dt, round(q, 2), f"{mot} · {cab} · {tr}",
                      f"Refugo do GMS sem lançamento no SAP (item {o['item']} da Conferencia_SAP)", "Lançar o refugo no SAP (ou apagar do GMS se não existiu)"], VERM))
# coluna A = material para o preso; para o sem lançamento, material vem do tripla
mat_op = {"30351277": "GH781-4", "30495028": "GH781-10", "30575946": "GH781-12", "30637731": "GH781-6", "30751352": "FC839B-06", "30829741": "GH781-8"}
lin2 = [((([mat_op.get(l[0][0], l[0][0])] + l[0][1:]) if l[0][0] in mat_op else l[0]), l[1]) for l in lin2]
aba(ws2, "2. Refugo que falta tratar",
    "Amarelo: o saldo da ProdHose do material é exatamente a soma desses refugos (entrou e não saiu). Vermelho: o GMS tem, o SAP não lançou.",
    ["Material", "OP", "Documento", "Data", "Metros", "Motivo · cabine · trançadeira", "O que é", "Ação"], lin2, [14, 11, 22, 11, 9, 42, 52, 52])
tot_preso = sum(x[4] for x in E["preso"]); tot_sem = sum(q for o in E["sem"] for _, q, *_ in o["semLanc"])
ws2.append([]); ws2.append(["Total a baixar da ProdHose", "", "", "", round(tot_preso, 2)]); ws2.append(["Total a lançar no SAP", "", "", "", round(tot_sem, 2)])
for r in (ws2.max_row - 1, ws2.max_row):
    ws2.cell(r, 1).font = Font(bold=True); ws2.cell(r, 5).font = Font(bold=True)

# 3) sem explicação
REFUGO = {"GH781-10", "GH681-12", "FC839B-08", "2556-12"}
ULT = {"EC215-08LRL": "03/08", "EC215-08L": "09/10", "FC735-08": "05/10", "HC101-8": "05/10", "2556-8": "31/08",
       "EC118-10L": "26/08 (1 doc, OP 29878655, 98,8 m = o saldo)", "EC115-10L": "18/06", "GH493-10": "09/10 (1 doc, OP 30446700, 34,5 m = o saldo)",
       "2556-10": "17/09", "12078544": "01/12/2025 (1 doc, OP 26992559, 23,9 m = o saldo)", "2556-3": "28/09", "2556-6": "01/10", "FC639-16": "14/05",
       "GH681-10": "26/06", "FC598-10": "18/09", "FC598-12": "13/10", "GH681-16": "06/10", "FC350-20": "sem 101 desde 11/2024",
       "EC600-12": "sem 101 desde 11/2024", "FC254-08": "sem 101 desde 11/2024", "12055040": "16/10"}
trans = defaultdict(float)
for lid, op, mat, q, dt in ls:
    if lid not in CORRIGIDOS and dt < "2026-10-15":
        trans[mat] += q
lin3 = []
for r in sorted(T, key=lambda r: -r["ph"]):
    p = r["ph"]
    if p <= 0.05 or r["m"] in REFUGO:
        continue
    sem = p
    fl = min(sem, r["pal48"]); sem -= fl
    co = min(sem, r["semPal"]); sem -= co
    if sem <= max(0.5, 0.15 * p):
        continue
    antigo = r["ops"] == 0 or r["m"] in ULT
    if antigo:
        leitura = "Sem produção no GMS desde 15/10. Último 101 no SAP: " + ULT.get(r["m"], "?")
        f = CINZA
    else:
        leitura = "Material em produção; tudo o que o GMS apontou desde 15/10 está em pallet. Sobra = pallet não transferido no EWM ou estoque de antes de 15/10"
        f = VERM
    lin3.append(([r["m"], round(p, 2), round(fl + co, 2), round(sem, 2), round(trans.get(r["m"], 0), 2), "Antigo" if antigo else "Parado", leitura], f))
ws3 = wb.create_sheet("3 Sem explicação")
aba(ws3, "3. Saldo da ProdHose que o GMS não explica",
    "O MB51 só tem entradas (101/102); a saída da PROD-GR-HOSE é no EWM. Para achar sem inventário: exportar do EWM o estoque da lixeira PROD-GR-HOSE com lote/OP e data de entrada de cada quant.",
    ["Material", "Saldo ProdHose (m)", "Explicado (pallets 48 h + sem pallet)", "Sem explicação (m)", "Lances da transição 06-14/10 sem pallet no GMS (m)", "Grupo", "Leitura"],
    lin3, [15, 12, 16, 14, 18, 10, 90])
ws3.append([]); ws3.append(["Total sem explicação", "", "", round(sum(l[0][3] for l in lin3), 2)])
ws3.cell(ws3.max_row, 1).font = Font(bold=True); ws3.cell(ws3.max_row, 4).font = Font(bold=True)

# resumo
ws0 = wb.create_sheet("Resumo", 0)
ws0.append(["Divergências SAP × GMS × ProdHose · 18/11/2026"]); ws0["A1"].font = Font(bold=True, size=14)
ws0.append([])
res = [("1 Sem packlist · correções a imprimir", sum(l[0][3] for l in lin1 if l[1] is AZUL), sum(1 for l in lin1 if l[1] is AZUL)),
       ("1 Sem packlist · produção desde 15/10", sum(l[0][3] for l in lin1 if l[1] is VERM), sum(1 for l in lin1 if l[1] is VERM)),
       ("1 Sem packlist · transição 06-14/10", sum(l[0][3] for l in lin1 if l[1] is AMAR), sum(1 for l in lin1 if l[1] is AMAR)),
       ("2 Refugo a baixar da ProdHose", tot_preso, len(E["preso"])),
       ("2 Refugo a lançar no SAP", tot_sem, sum(len(o["semLanc"]) for o in E["sem"])),
       ("3 Sem explicação · parado", sum(l[0][3] for l in lin3 if l[0][5] == "Parado"), sum(1 for l in lin3 if l[0][5] == "Parado")),
       ("3 Sem explicação · antigo", sum(l[0][3] for l in lin3 if l[0][5] == "Antigo"), sum(1 for l in lin3 if l[0][5] == "Antigo"))]
ws0.append(["Bloco", "Metros", "Linhas"])
for c in ws0[3]:
    c.fill, c.font = CAB, BR
for a, b, c in res:
    ws0.append([a, round(b, 2), c])
for row in ws0.iter_rows(min_row=4):
    row[1].number_format = "#,##0.00"
ws0.column_dimensions["A"].width = 44; ws0.column_dimensions["B"].width = 12; ws0.column_dimensions["C"].width = 9
ws0.append([]); ws0.append(["Fontes: MB51 de 18/11 08:06, RegistrosInspeção, TiposErros e Packing_Pallets ao vivo, saldo da PROD-GR-HOSE colado pelo William em 18/11."])
wb.save(SAIDA)
for a, b, c in res:
    print(f"{a}: {b:.1f} m ({c})")
