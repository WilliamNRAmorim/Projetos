"""Produção por mangueira, 16/05 a 16/09/2026: GMS x MB51 (metros). Rodar na raiz do repositório: python Producao_GMS_x_MB51/scripts/gerar_producao.py"""
import csv, sys, datetime as dt, collections, re
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "Refugo" / "Refugo_por_Material"))
from gms_dados import norm_material, USUARIOS_REFUGO, RELATORIO

GMS = Path(__file__).resolve().parents[2] / "GMS"
SP = GMS / "Sharepoint Data GMS"
INI, FIM = dt.date(2026, 5, 16), dt.date(2026, 9, 16)

def csv_rows(nome):
    for enc in ("utf-8-sig", "latin-1"):
        try:
            return list(csv.DictReader(open(SP / nome, encoding=enc)))
        except UnicodeDecodeError:
            pass
f = lambda s: float(str(s).replace(",", ""))
def d_us(s):  # 'MM/DD/AAAA h:mm AM/PM' ou 'MM/DD/AAAA'
    return dt.datetime.strptime(s.split()[0], "%m/%d/%Y").date()

ALIAS = {"HC139-7_S-GX": "HC139-7", "GH781-6-2": "GH781-6"}  # mesma mangueira com sufixo de cliente
def canon(m):
    return ALIAS.get(m, m)
def eh_mangueira(m):
    return not m.startswith(("MANDREL", "MANDRIL"))

# GMS
fichas = {r["OP"]: (norm_material(r["Mangueira"]) if r["Mangueira"].startswith("HOSE") else r["Mangueira"].strip()).upper() for r in csv_rows("ficha_producao.csv")}
gms_boa, gms_ref = collections.defaultdict(float), collections.defaultdict(float)
ops_sem_ficha = collections.Counter()
for r in csv_rows("RegistrosInspeção.csv"):
    d = d_us(r["DataHoraInspecao"])
    if INI <= d <= FIM:
        m = r["Mangueira"].strip().upper() or fichas.get(r["OP_ID"], "(sem mangueira)")
        gms_boa[canon(m)] += f(r["Quantidade"])
for r in csv_rows("TiposErros.csv"):
    d = d_us(r["DataHoraRefugo"] or r["Criado"])
    if INI <= d <= FIM:
        m = fichas.get(r["OP_ID"])
        m = m.upper() if m else m
        if m is None: ops_sem_ficha[r["OP_ID"]] += 1; m = "(OP sem ficha)"
        gms_ref[canon(m)] += f(r["Quantidade"])

# MB51 (aba MB51 do relatório de 01/10, a mesma base dos números de referência)
sap_boa, sap_ref = collections.defaultdict(float), collections.defaultdict(float)
ws = openpyxl.load_workbook(RELATORIO, read_only=True, data_only=True)["MB51"]
for r in ws.iter_rows(min_row=2, values_only=True):
    d, mvt, un, q, usr = r[9], str(r[5]), r[11], r[14], r[15]
    if not isinstance(d, dt.datetime) or not INI <= d.date() <= FIM or q is None or un != "M" or mvt not in ("101", "102"): continue
    m = canon(norm_material(r[2]).upper()); s = q  # 102 já vem negativo na MB51
    (sap_ref if usr in USUARIOS_REFUGO else sap_boa)[m] += s

mats = sorted(m for m in set(gms_boa) | set(gms_ref) | set(sap_boa) | set(sap_ref) if eh_mangueira(m))
wb = openpyxl.Workbook(); ws = wb.active; ws.title = "Por mangueira"
cab = ["Mangueira", "GMS boa (m)", "GMS refugo (m)", "GMS total (m)", "MB51 boa (m)", "MB51 refugo (m)", "MB51 total (m)", "Dif. boa (MB51 - GMS)", "Dif. total (MB51 - GMS)"]
ws.append(cab)
for i, m in enumerate(mats, start=2):
    ws.append([m, round(gms_boa[m], 2), round(gms_ref[m], 2), f"=B{i}+C{i}", round(sap_boa[m], 2), round(sap_ref[m], 2), f"=E{i}+F{i}", f"=E{i}-B{i}", f"=G{i}-D{i}"])
n = len(mats) + 1
ws.append(["TOTAL"] + [f"=SUM({c}2:{c}{n})" for c in "BCDEFGHI"])
for c in ws[1]: c.font = Font(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor="C8102E"); c.alignment = Alignment(wrap_text=True, horizontal="center")
for c in ws[n + 1]: c.font = Font(bold=True)
for row in ws.iter_rows(min_row=2, min_col=2):
    for c in row: c.number_format = "#,##0.0"
ws.column_dimensions["A"].width = 18
for col in "BCDEFGHI": ws.column_dimensions[col].width = 16
ws.freeze_panes = "B2"
ws.auto_filter.ref = f"A1:I{n}"

p = wb.create_sheet("Premissas")
for l in [
    f"Período: {INI:%d/%m/%Y} a {FIM:%d/%m/%Y} (inclusive). Metros.",
    "GMS boa: RegistrosInspeção (coluna Quantidade), pela data da inspeção, agrupada pela mangueira do registro.",
    "GMS refugo: TiposErros (Quantidade), pela data do refugo; a mangueira vem da ficha_producao pela OP.",
    "MB51: aba MB51 do Relatorio_Conferencia_MB51_v3_2.xlsx (01/10/2026), só unidade M, movimentos 101 + 102 (o estorno 102 já vem negativo), pela Posting Date.",
    "MB51 refugo = lançamentos dos usuários de refugo (U445131 e U452021); MB51 boa = os demais.",
    "Só mangueiras: mandris (MANDREL-…, MANDRIL FLEXIVEL) ficam fora. HC139-7_S-GX foi somado ao HC139-7 e GH781-6-2 ao GH781-6.",
    "Mangueira da MB51 vem da Material Description normalizada (norm_material); seis materiais podem ficar com nome diferente nos dois lados.",
    "Diferença = MB51 - GMS: positiva = sobra no SAP; negativa = falta lançar no SAP. Material não compensa com material.",
    "Fonte de verdade: SAP. Dados são fotografias de 01/10 (MB51) e 02/10-06/10 (GMS).",
]: p.append([l])
p.column_dimensions["A"].width = 130
out = Path(__file__).resolve().parents[1] / "resultados" / "Producao_por_Mangueira_GMS_x_MB51_16mai_16set.xlsx"
wb.save(out)
print("salvo", out.name, len(mats), "mangueiras")
print("GMS boa %.1f ref %.1f | MB51 boa %.1f ref %.1f" % tuple(sum(d[m] for m in mats) for d in (gms_boa, gms_ref, sap_boa, sap_ref)))
print("refugo OP sem ficha:", dict(ops_sem_ficha))
only = [m for m in mats if (gms_boa[m] + gms_ref[m] == 0) or (sap_boa[m] + sap_ref[m] == 0)]
print("só de um lado:", only)
