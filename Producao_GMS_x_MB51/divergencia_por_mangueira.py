"""Divergência por mangueira: soma do SAP - soma do GMS, por material SAP (o lance trocado de OP se anula dentro da mangueira).
Rodar depois do conferir_lances_por_op.py:
  python Producao_GMS_x_MB51/divergencia_por_mangueira.py [AAAA-MM-DD inicio] [AAAA-MM-DD fim]   (padrão 2026-05-16 a 2026-09-16)
Grava a aba 'Divergência por mangueira' como primeira aba da Conferencia_Lances_por_OP.xlsx.
"""
import sys, collections, datetime as dt
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
for r in wb["MB51 sem GMS"].iter_rows(min_row=2, values_only=True):
    if r[3] and ini <= r[3].date() <= fim:                    # OP só no SAP, pela data do 1º lançamento
        dif[r[1]] += r[6] or 0
        desc.setdefault(r[1], r[2])

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

ws["A1"].font = Font(bold=True)
for c in ws[2]:
    c.font = Font(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor="C8102E")
    c.alignment = Alignment(horizontal="center")
for row in ws.iter_rows(min_row=3):
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

print(f"{len(linhas)} mangueiras | total |dif| {sum(abs(d) for _, d in linhas):,.1f} m | a mais {sum(d for _, d in linhas if d > 0):,.1f} | a menos {sum(d for _, d in linhas if d < 0):,.1f}")
for m, d in linhas[:12]:
    print(f"{m:14s} {d:10.1f}")
