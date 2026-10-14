"""Divergência por mangueira: soma do SAP - soma do GMS, por material SAP (o lance trocado de OP se anula dentro da mangueira).
Rodar depois do conferir_lances_por_op.py:
  python Producao_GMS_x_MB51/divergencia_por_mangueira.py [AAAA-MM-DD inicio] [AAAA-MM-DD fim]   (padrão 2026-05-16 a 2026-09-16)
Grava a aba 'Divergência por mangueira' como primeira aba da Conferencia_Lances_por_OP.xlsx.
"""
import sys, collections, itertools, datetime as dt
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

AQUI = Path(__file__).resolve().parent
ARQ = AQUI / "Conferencia_Lances_por_OP.xlsx"
ini = dt.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else dt.date(2026, 5, 16)
fim = dt.date.fromisoformat(sys.argv[2]) if len(sys.argv) > 2 else dt.date(2026, 9, 16)
ABA = "Divergência por mangueira"

wb = openpyxl.load_workbook(ARQ)
dif = collections.defaultdict(float)
desc = {}
for r in wb["Resumo por OP"].iter_rows(min_row=2, values_only=True):
    if r[5] and ini <= r[5].date() <= fim and r[2]:          # OP pela data do 1º lance no GMS
        dif[r[2]] += (r[10] or 0) - (r[9] or 0)              # MB51 líquido - GMS total
        desc[r[2]] = r[3]
# OP só no SAP (sem nenhum lance no GMS): entra só se diminuir a divergência da mangueira (decisão do William, 14/10)
so_sap = collections.defaultdict(list)
for r in wb["MB51 sem GMS"].iter_rows(min_row=2, values_only=True):
    if r[3] and ini <= r[3].date() <= fim:
        so_sap[r[1]].append(r)
        desc.setdefault(r[1], r[2])
entra, sai = [], []
for m, ops in so_sap.items():
    base = dif[m]
    if len(ops) <= 15:   # melhor combinação: a que deixa a divergência mais perto de zero
        melhor = min((c for k in range(len(ops) + 1) for c in itertools.combinations(ops, k)),
                     key=lambda c: (abs(base + sum(o[6] for o in c)), len(c)))
    else:
        melhor, d = [], base
        for o in sorted(ops, key=lambda o: -abs(o[6])):
            if abs(d + o[6]) < abs(d):
                melhor.append(o); d += o[6]
    for o in ops:
        (entra if o in melhor else sai).append((m, base, o))
    dif[m] = base + sum(o[6] for o in melhor)

if ABA in wb.sheetnames:
    del wb[ABA]
ws = wb.create_sheet(ABA, 0)
ws.append([f"Divergência por mangueira (SAP - GMS), OPs de {ini:%d/%m/%Y} a {fim:%d/%m/%Y}. Positivo = SAP tem a mais; negativo = SAP tem a menos."])
ws.append(["Mangueira (SAP)", "Descrição SAP", "Divergência (m)", "Sentido"])
linhas = sorted(((m, d) for m, d in dif.items() if abs(d) >= 0.05), key=lambda t: -abs(t[1]))
for m, d in linhas:
    ws.append([m, desc.get(m, ""), round(d, 1), "SAP a mais" if d > 0 else "SAP a menos"])
n = ws.max_row
ws.append([])
ws.append(["Total da divergência (sem compensar uma mangueira com outra)", "", f"=SUMPRODUCT(ABS(C3:C{n}))", ""])
ws.append(["SAP a mais", "", f'=SUMIF(C3:C{n},">0")', ""])
ws.append(["SAP a menos", "", f'=SUMIF(C3:C{n},"<0")', ""])

ws.append([])
ws.append(["OPs só no SAP (nenhum lance no GMS): entram na conta só quando diminuem a divergência da mangueira"])
ws.cell(ws.max_row, 1).font = Font(bold=True)
cab = ws.max_row + 1
ws.append(["Mangueira (SAP)", "OP", "SAP (m)", "Na conta?", "1º lançamento", "Divergência da mangueira sem as OPs só no SAP (m)"])
for c in ws[cab]:
    c.font = Font(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor="C8102E")
for lst, sim in ((entra, "Entra (diminui)"), (sai, "Fora (aumentaria)")):
    for m, base, o in sorted(lst, key=lambda t: (t[0], -t[2][6])):
        ws.append([m, o[0], round(o[6], 1), sim, o[3], round(base, 1)])
        ws.cell(ws.max_row, 5).number_format = "dd/mm/yyyy"
ws.column_dimensions["E"].width = 14; ws.column_dimensions["F"].width = 22
ws["A1"].font = Font(bold=True)
for c in ws[2]:
    c.font = Font(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor="C8102E")
    c.alignment = Alignment(horizontal="center")
for row in ws.iter_rows(min_row=3, max_row=n):
    row[2].number_format = "#,##0.0"
    if row[3].value in ("SAP a mais", "SAP a menos"):
        row[3].fill = PatternFill("solid", fgColor="FFE699" if row[3].value == "SAP a mais" else "F8CBAD")
for r in range(n + 2, n + 5):
    ws.cell(r, 1).font = Font(bold=True); ws.cell(r, 3).font = Font(bold=True)
for col, w in zip("ABCD", [16, 38, 16, 14]):
    ws.column_dimensions[col].width = w
ws.freeze_panes = "A3"
wb.active = 0
for s in wb.worksheets:
    s.sheet_view.tabSelected = s.title == ABA
wb.save(ARQ)

print("OPs só no SAP: entram", len(entra), round(sum(o[6] for _, _, o in entra)), "| fora", len(sai), round(sum(o[6] for _, _, o in sai)))
for m, b, o in sorted(entra): print("  entra", m, o[0], o[6], "base", round(b, 1))
print(f"{len(linhas)} mangueiras | total |dif| {sum(abs(d) for _, d in linhas):,.1f} m | a mais {sum(d for _, d in linhas if d > 0):,.1f} | a menos {sum(d for _, d in linhas if d < 0):,.1f}")
for m, d in linhas[:12]:
    print(f"{m:14s} {d:10.1f}")
