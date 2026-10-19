"""Comunicado simples a partir da Conferencia_Lances_por_OP.xlsx (rodar depois do conferir_lances_por_op.py).
Uso: python Producao_GMS_x_MB51/scripts/comunicado.py [AAAA-MM-DD inicio] [AAAA-MM-DD fim]   (padrão 2026-05-16 a 2026-09-16)
Gera Comunicado_GMS_x_SAP.xlsx com as abas 'Comunicado' (texto pronto) e 'OPs para corrigir' (diferença >= 50 m).
"""
import sys, collections, datetime as dt
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

AQUI = Path(__file__).resolve().parents[1]  # pasta Producao_GMS_x_MB51
ARQ = AQUI / "Conferencia_Lances_por_OP.xlsx"
ini = dt.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else dt.date(2026, 5, 16)
fim = dt.date.fromisoformat(sys.argv[2]) if len(sys.argv) > 2 else dt.date(2026, 9, 16)
LIMITE = 50  # m: OP entra na lista de correção

wb = openpyxl.load_workbook(ARQ, read_only=True)
R = list(wb["Resumo por OP"].iter_rows(min_row=2, values_only=True))
L = list(wb["Linha a linha"].iter_rows(min_row=2, values_only=True))
ops = {r[0]: r for r in R if r[5] and ini <= r[5].date() <= fim}

CAUSAS = {
    "outra": "Lance lançado em outra OP no SAP",
    "g_boa": "Produção no GMS sem lançamento no SAP",
    "s_boa": "Produção no SAP sem registro no GMS",
    "g_ref": "Refugo no GMS sem lançamento no SAP",
    "s_ref": "Refugo no SAP sem registro no GMS",
}
cat = collections.defaultdict(lambda: [0, 0.0, set()])
por_op = collections.defaultdict(collections.Counter)
for x in L:
    if x[0] not in ops or not str(x[9] or "").startswith("SÓ"):
        continue
    obs = str(x[13] or "")
    if x[3] == "GMS":
        k = "outra" if obs.startswith("Provável lance lançado") else ("g_ref" if x[4] == "refugo" else "g_boa")
    else:
        if obs.startswith("Provável lance da OP"):
            por_op[x[0]]["outra"] += x[6]
            continue  # já contado do lado do GMS
        k = "s_ref" if x[4] == "refugo" else "s_boa"
    c = cat[k]; c[0] += 1; c[1] += x[6]; c[2].add(x[0])
    por_op[x[0]][k] += x[6]

st = collections.Counter(r[-1] for r in ops.values())
dv = [r for r in ops.values() if r[-1] == "DIVERGE"]
peq = sum(1 for r in dv if abs(r[11]) < 5)
bate = st["Bate lance a lance"] + st["Bate (com ressalva)"] + peq
real = len(dv) - peq
grandes = sorted([r for r in dv if abs(r[11]) >= 5 and (abs(r[11]) >= LIMITE or r[17] + r[19] >= LIMITE)], key=lambda r: -(r[17] + r[19]))
troca = [r for r in ops.values() if str(r[4]).startswith("MANGUEIRA")]
sem = [r for r in ops.values() if r[-1].startswith("OP sem")]
gt, st_ = sum(r[9] for r in ops.values()), sum(r[10] for r in ops.values())
n = len(ops)
km = lambda m: f"{m / 1000:,.1f} km".replace(",", "X").replace(".", ",").replace("X", ".")
mm = lambda m: f"{m:,.0f} m".replace(",", ".")
pc = lambda a: f"{100 * a / n:.0f}%"

def linha(k):
    c = cat[k]
    return f"{CAUSAS[k]}: {c[0]} lances, {km(c[1]) if c[1] >= 1000 else mm(c[1])}, em {len(c[2])} OPs."

texto = [
    f"Conferência da produção GMS x SAP (MB51), lance a lance por OP, {ini:%d/%m} a {fim:%d/%m/%Y}",
    "",
    f"Conferi {n:,} OPs".replace(",", ".") + f". No total o GMS tem {km(gt)} e o SAP {km(st_)} (diferença de " + f"{abs(st_ - gt) / gt * 100:.1f}".replace(".", ",") + "%).",
    f"- {bate} OPs ({pc(bate)}) batem: {st['Bate lance a lance'] + st['Bate (com ressalva)']} lance a lance e {peq} com diferença menor que 5 m (só arredondamento ou agrupamento).",
    f"- {real} OPs ({pc(real)}) têm diferença real (5 m ou mais); {len(grandes)} delas com {LIMITE} m ou mais para acertar.",
    f"- {len(sem)} OPs do GMS sem nenhum lançamento no SAP.",
    "",
    "De onde vem a diferença:",
    "1. " + linha("outra") + " A metragem existe, mas foi apontada na OP vizinha (mesmo material).",
    "2. " + linha("g_boa"),
    "3. " + linha("s_boa"),
    "4. " + linha("g_ref"),
    "5. " + linha("s_ref"),
    f"6. Mangueira diferente na OP: {len(troca)} OPs em que o GMS registra uma mangueira e a OP no SAP é de outra.",
    "",
    "Próximos passos:",
    f"- Corrigir as {len(grandes)} OPs da aba 'OPs para corrigir' (diferença de {LIMITE} m ou mais), começando pelas maiores.",
    "- Reforçar o apontamento na OP certa no SAP (item 1).",
    "- Conferir as OPs de mangueira diferente com o PCP.",
    "",
    "Detalhe lance a lance: Conferencia_Lances_por_OP.xlsx (abas Resumo por OP e Linha a linha).",
]

out = openpyxl.Workbook()
cm = out.active; cm.title = "Comunicado"
for t in texto:
    cm.append([t])
cm["A1"].font = Font(bold=True, size=13)
for r in (8, 16):
    cm.cell(r, 1).font = Font(bold=True)
cm.column_dimensions["A"].width = 150

oc = out.create_sheet("OPs para corrigir")
oc.append(["OP", "Mangueira GMS", "Material SAP", "1º lance GMS", "GMS total (m)", "SAP líquido (m)", "Dif. SAP - GMS (m)", "Causa principal", "Mangueira"])
for r in grandes:
    c = por_op[r[0]]
    causa = CAUSAS[c.most_common(1)[0][0]] if c else "Valor diferente"
    if r[-1].startswith("OP sem"):
        causa = "OP sem lançamento no SAP"
    oc.append([r[0], r[1], r[2], r[5], r[9], r[10], r[11], causa, "DIFERENTE" if str(r[4]).startswith("MANGUEIRA") else ""])
for r in troca:
    if r not in grandes:
        oc.append([r[0], r[1], r[2], r[5], r[9], r[10], r[11], "Mangueira diferente na OP", "DIFERENTE"])
for c in oc[1]:
    c.font = Font(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor="C8102E")
    c.alignment = Alignment(wrap_text=True, horizontal="center")
for col, w in zip("ABCDEFGHI", [11, 14, 14, 16, 12, 12, 13, 40, 11]):
    oc.column_dimensions[col].width = w
for row in oc.iter_rows(min_row=2):
    row[3].number_format = "dd/mm/yyyy"
    for c in row[4:7]:
        c.number_format = "#,##0.0"
oc.freeze_panes = "B2"; oc.auto_filter.ref = oc.dimensions
out.save(AQUI / "resultados" / f"Comunicado_GMS_x_SAP_{ini:%d-%m}_a_{fim:%d-%m}.xlsx")
print("\n".join(texto))
