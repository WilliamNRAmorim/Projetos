"""Lances duplicados: aba 'Duplicados GMS' (refugo e produção, com grau de certeza) e 'Duplicados MB51' (só os com certeza).
Rodar depois do conferir_lances_por_op.py:  python Producao_GMS_x_MB51/scripts/duplicados.py
"""
import csv, collections, datetime as dt
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

AQUI = Path(__file__).resolve().parents[1]  # pasta Producao_GMS_x_MB51
ARQ = AQUI / "Conferencia_Lances_por_OP.xlsx"
JANELA_MIN = 2        # minutos entre os dois registros iguais no GMS (clique duplo / registro repetido)
JANELA_MEDIDA = 30    # inspeção com as mesmas medidas (DI, DE, concentricidade): até 30 min


def ler(p):
    return list(csv.DictReader(open(p, encoding="utf-8-sig"), delimiter=";"))


def data(s):
    for f in ("%d/%m/%Y %H:%M", "%d/%m/%Y"):
        try:
            return dt.datetime.strptime(s.strip(), f)
        except ValueError:
            pass


def num(s):
    s = str(s).strip().replace(",", ".")
    return float(s) if s else 0.0


wb = openpyxl.load_workbook(ARQ)
L = list(wb["Linha a linha"].iter_rows(min_row=2, values_only=True))
status = {x[7]: x for x in L if x[3] == "GMS"}                      # 'Inspeção linha N' -> linha
dif_op = {r[0]: r[11] for r in wb["Resumo por OP"].iter_rows(min_row=2, values_only=True)}
sap_por_op = collections.defaultdict(list)
for x in L:
    if x[3] == "MB51":
        sap_por_op[x[0]].append(x)

# ---------- GMS ----------
EXCL = {r["referencia"] for r in ler(AQUI / "dados" / "lances_excluidos.csv")} if (AQUI / "dados" / "lances_excluidos.csv").exists() else set()
regs = []
for i, r in enumerate(ler(AQUI / "dados" / "inspecao_14out.csv"), start=2):
    regs.append(("Produção", f"Inspeção linha {i}", r["OP_ID"].strip(), num(r["Quantidade"]), data(r["Created"]),
                 (r["Diametro_Interno"], r["Diametro_Externo"], r["Concentricidade"]), r["Mangueira"] or ""))
for i, r in enumerate(ler(AQUI / "dados" / "refugo_14out.csv"), start=2):
    regs.append(("Refugo", f"Refugo linha {i}", r["OP_ID"].strip(), num(r["Quantidade"]), data(r["Created"]),
                 r["CodigoErro"], ""))

grupos = collections.defaultdict(list)
for g in regs:
    if g[3] > 0 and g[4] and g[1] not in EXCL:
        chave = (g[0], g[2], round(g[3], 2)) + ((g[5],) if g[0] == "Refugo" else ())
        grupos[chave].append(g)

dup_gms = []
for chave, v in grupos.items():
    v.sort(key=lambda t: t[4])
    for a, b in zip(v, v[1:]):
        mins = (b[4] - a[4]).total_seconds() / 60
        mesma_medida = a[0] == "Produção" and a[5] == b[5]
        if not (mins <= JANELA_MIN or (mesma_medida and mins <= JANELA_MEDIDA)):
            continue
        sa, sb = status.get(a[1]), status.get(b[1])
        st = [str(s[9]) if s else "" for s in (sa, sb)]
        so = sum(s.startswith("SÓ") for s in st)
        if so == 0 and a[0] == "Produção":
            continue  # SAP também tem os dois: rolo de tamanho padrão (50/80/100 m), lance real
        d_op = dif_op.get(a[2]) or 0
        if so == 1:
            sap = "SAP tem só um"
            certeza = "Alta" if d_op < 0 and abs(d_op + a[3]) <= 0.05 else "Média"
        elif so == 0:
            sap = "SAP lançou os dois (copiou o GMS)"
            certeza = "Baixa"
        else:
            sap = "SAP não tem nenhum dos dois"
            certeza = "Baixa"
        motivo = f"mesma quantidade{', mesmo defeito' if a[0] == 'Refugo' else ''}, {mins:.0f} min de diferença" + (", mesmas medidas" if mesma_medida else "")
        mang = (sa[1] if sa else "") or a[6]
        dup_gms.append([a[2], mang, a[0], b[4], b[3], a[1], b[1], motivo, sap, certeza, round(d_op, 1), st[0], st[1]])

# ---------- MB51: só com certeza ----------
# (1) o duplicado do GMS foi lançado também no SAP (clique duplo no GMS virou dois lançamentos);
# (2) dois lançamentos iguais na mesma OP, mesmo dia, mesmo usuário, e o GMS tem menos lances desse valor (um sobra sem par e sem ser de outra OP).
dup_mb = []
# Certeza no SAP: dois lançamentos iguais na mesma OP, mesmo dia e mesmo usuário; o GMS tem menos lances desse valor;
# o que sobra não casou com nada nem é de outra OP; e a diferença inteira da OP (SAP - GMS) é exatamente o que sobra.
for op, S in sap_por_op.items():
    g = collections.defaultdict(list)
    for x in S:
        if x[4] != "estorno" and not str(x[9]).startswith("Estornado"):
            g[(round(x[6], 2), x[5].date() if x[5] else None, x[8])].append(x)
    for (q, dia, usr), v in g.items():
        if len(v) < 2:
            continue
        sobra = [x for x in v if str(x[9]).startswith("SÓ NA MB51") and not x[13]]
        n_gms = sum(1 for y in L if y[0] == op and y[3] == "GMS" and abs(y[6] - q) <= 0.05)
        extra = len(v) - n_gms
        if not sobra or extra < 1:
            continue
        extra = min(extra, len(sobra))
        if abs((dif_op.get(op) or 0) - q * extra) > 0.05:
            continue
        for x in sobra[:extra]:
            dup_mb.append([op, x[2], x[4], x[5], x[6], x[7], x[8],
                           f"{len(v)} lançamentos de {q} m no mesmo dia pelo mesmo usuário; o GMS tem {n_gms}; "
                           f"a diferença inteira da OP ({dif_op.get(op):+.1f} m) é este lançamento"])

# ---------- planilha ----------
for nome in ("Duplicados GMS", "Duplicados MB51"):
    if nome in wb.sheetnames:
        del wb[nome]
pos = wb.sheetnames.index("Divergência por mangueira") + 1 if "Divergência por mangueira" in wb.sheetnames else 0
w1 = wb.create_sheet("Duplicados GMS", pos)
w1.append(["OP", "Mangueira", "Tipo", "Data do 2º registro", "Metros a mais", "1º registro", "2º registro (o duplicado)", "Por que parece duplicado", "No SAP", "Certeza", "Dif. da OP SAP - GMS (m)", "Situação 1º", "Situação 2º"])
for d in sorted(dup_gms, key=lambda d: ({"Alta": 0, "Média": 1, "Baixa": 2}[d[9]], -d[3].timestamp())):
    w1.append(d)
w2 = wb.create_sheet("Duplicados MB51", pos + 1)
w2.append(["OP", "Material SAP", "Tipo", "Data", "Metros a mais", "Documento", "Usuário", "Por que tenho certeza"])
for d in sorted(dup_mb, key=lambda d: d[3] or dt.datetime(2000, 1, 1), reverse=True):
    w2.append(d)
for ws, larg in ((w1, [11, 14, 10, 16, 11, 18, 22, 46, 30, 9, 12, 30, 30]), (w2, [11, 14, 9, 12, 11, 18, 10, 90])):
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor="C8102E")
        c.alignment = Alignment(wrap_text=True, horizontal="center")
    for i, wd in enumerate(larg):
        ws.column_dimensions[chr(65 + i)].width = wd
    for row in ws.iter_rows(min_row=2):
        row[3].number_format = "dd/mm/yyyy hh:mm" if ws is w1 else "dd/mm/yyyy"
        row[4].number_format = "#,##0.0"
    ws.freeze_panes = "B2"; ws.auto_filter.ref = ws.dimensions
wb.save(ARQ)

c = collections.Counter((d[2], d[9]) for d in dup_gms)
print("GMS:", len(dup_gms), "registros duplicados,", round(sum(d[4] for d in dup_gms), 1), "m |", dict(c))
print("MB51 com certeza:", len(dup_mb), round(sum(d[4] for d in dup_mb), 1), "m")
for d in dup_mb: print("  ", d[:7])
ini, fim = dt.date(2026, 5, 16), dt.date(2026, 9, 16)
p = [d for d in dup_gms if ini <= d[3].date() <= fim]
print("16/05-16/09 GMS:", len(p), round(sum(d[4] for d in p), 1), collections.Counter((d[2], d[9]) for d in p))
for d in dup_gms:
    if d[9] == "Alta": print("  alta", d[:5], d[10])
