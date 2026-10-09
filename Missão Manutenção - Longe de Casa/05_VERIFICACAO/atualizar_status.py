import os, glob, datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

AQUI = os.path.dirname(os.path.abspath(__file__))
rows = []
f = os.path.join(AQUI, "VERIFICACAO_GERAL.xlsx")
try:
    ws = openpyxl.load_workbook(f, data_only=True).active
except PermissionError:
    raise SystemExit("VERIFICACAO_GERAL.xlsx esta aberto/bloqueado: feche no Excel e rode de novo")
for r in ws.iter_rows(min_row=2, values_only=True):
    if not r[1]:
        continue
    v = lambda i: str(r[i]).strip() if len(r) > i and r[i] not in (None, "") else ""
    cand, cod, nome, parte, obs = v(14), v(15), v(16), v(17), v(18)
    if r[2] == "SEM FOTO":
        st = "Sem foto"
    elif cod:
        st = "Verificado"
    elif cand:
        st = "Sem código (" + cand + ")"
    else:
        st = "Pendente"
    rows.append([r[0], r[1], st, cand, cod, nome, parte, obs, "VERIFICACAO_GERAL.xlsx"])
wb = openpyxl.Workbook()
res = wb.active; res.title = "Resumo"
res.append(["Bloco", "Total", "Verificado", "Em andamento", "Pendente", "Sem foto"])
for b in sorted({x[0] for x in rows}):
    s = [x[2] for x in rows if x[0] == b]
    res.append([b, len(s), s.count("Verificado"), sum(t.startswith("Sem código") for t in s), s.count("Pendente"), s.count("Sem foto")])
n = len(res["A"]) 
res.append(["TOTAL"] + [f"=SUM({c}2:{c}{n})" for c in "BCDEF"])
res.append([]); res.append(["Atualizado em", datetime.datetime.now().strftime("%d/%m/%Y %H:%M")])
det = wb.create_sheet("Detalhe")
det.append(["Bloco", "Material (NI)", "Status", "Candidata escolhida", "Código FINAL", "Nome FINAL", "Parte da máquina FINAL", "Observação", "Arquivo"])
cor = {"Verificado": "C6EFCE", "Pendente": "FFC7CE", "Sem foto": "D9D9D9"}
for x in rows:
    det.append(x)
    c = det.cell(row=det.max_row, column=3)
    c.fill = PatternFill("solid", fgColor=cor.get(x[2], "FFEB9C"))
for ws in (res, det):
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor="1F4E78")
        c.alignment = Alignment(horizontal="center", wrap_text=True)
    for col in ws.columns:
        ws.column_dimensions[col[0].column_letter].width = 20
det.freeze_panes = "A2"; det.auto_filter.ref = det.dimensions
out = os.path.join(AQUI, "STATUS_VERIFICACAO.xlsx")
try:
    wb.save(out)
except PermissionError:
    out = out.replace(".xlsx", "_novo.xlsx"); wb.save(out)
print("ok", out, "-", sum(x[2] == "Verificado" for x in rows), "verificados de", len(rows))

