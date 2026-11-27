# gerar_bom_sap.py: BOM por metro de cada mangueira a partir da COOIS "Components" (requisito de cada OP).
# BOM/m = mediana, entre as OPs da mangueira, de (Requirement Quantity / quantidade da OP em metros).
# Quantidade e mangueira da OP: COOIS de cabeçalho; OP que não está nela usa a ficha (Mangueira e metros do Mandril = Tubo).
#
# Uso: python -I gerar_bom_sap.py <coois_componentes.xlsx> <coois_cabecalho.xlsx> [ficha_ops.json] [simulador_bom.csv]
# Saída (nesta pasta): bom_mangueira_sap.csv (formato da lista GMS_BOM_Mangueira) e bom_comparacao.csv (SAP x simulador)
import csv, json, os, re, sys, statistics as st
from collections import defaultdict
import openpyxl

AQUI = os.path.dirname(os.path.abspath(__file__))
COMP, CAB = sys.argv[1], sys.argv[2]
FICHA = sys.argv[3] if len(sys.argv) > 3 else None
SIM = sys.argv[4] if len(sys.argv) > 4 else os.path.join(AQUI, "bom_mangueira.csv")

def tabela(f):
    ws = openpyxl.load_workbook(f, read_only=True, data_only=True).worksheets[0]
    it = ws.iter_rows(values_only=True); h = next(it)
    return [dict(zip(h, r)) for r in it]

ops = {}  # OP -> (mangueira, metros, origem)
for r in tabela(CAB):
    if r["Unit of measure (=GMEIN)"] == "M" and r["Order quantity (GMEIN)"]:
        ops[str(r["Order"])] = (str(r["Material"]).strip(), float(r["Order quantity (GMEIN)"]), "COOIS")
if FICHA:
    for op, (mang, _, tubo, mandril) in json.load(open(FICHA, encoding="utf-8")).items():
        if op not in ops and mang and tubo and tubo == mandril:  # só quando a ficha é coerente
            ops[op] = (mang.strip(), float(tubo), "ficha")

def camada(pn, desc, un):
    d = (desc or "").upper()
    if un == "PC" or "REVISION" in d:
        return None
    if "TUBE" in d or "TUBO" in d or pn in ("2023", "640-53"):
        return "tubo"
    if "COVER" in d or "COBERTURA" in d:
        return "cobertura"
    if any(k in d for k in ("WIRE", "FIO", "POLIESTER", "POLYESTER", "INSULATION", "INS.", "LENO", "FABRIC", "CIMENTO", "CELIK")):
        return "trama"
    return "bandagem"  # brand, fita de identificação, ink transfer, filme, match-mate

def material(cam, d):
    d = d.upper()
    return {"tubo": "Composto / Tubo", "cobertura": "Composto / Cobertura"}.get(cam) or (
        "Fio (arame / textil)" if any(k in d for k in ("WIRE", "FIO", "POLI", "POLY", "CELIK")) else
        "Insulation" if "INS" in d else "Leno" if ("LENO" in d or "FABRIC" in d) else "Cimento" if "CIMENTO" in d else
        "Filme" if "FILME" in d else "Fita match-mate")

razoes = defaultdict(lambda: defaultdict(list)); nops = defaultdict(set); info = {}
for r in tabela(COMP):
    op = str(r["Order"]); pn = str(r["Material"] or "").strip()
    if op not in ops or not pn:
        continue
    un = r["Base Unit of Measure (=EINHEIT)"]; q = float(r["Requirement Quantity (EINHEIT)"] or 0)
    cam = camada(pn, r["Material Description"], un)
    if cam is None or q <= 0:
        continue
    fator, un2 = {"G": (0.001, "kg"), "MM": (0.001, "m")}.get(un, (1, un.lower()))
    mang, metros, _ = ops[op]
    razoes[mang][pn].append(q * fator / metros); nops[mang].add(op)
    info[pn] = (cam, material(cam, r["Material Description"]), un2, r["Material Description"])

linhas = []
for mang in sorted(razoes):
    n = len(nops[mang])
    for pn, v in razoes[mang].items():
        if len(v) < max(1, n / 2):  # componente que aparece em menos da metade das OPs: alternativo, fica fora
            continue
        cam, mat, un, desc = info[pn]
        disp = (max(v) - min(v)) / st.median(v) if st.median(v) else 0
        linhas.append({"Mangueira": mang, "Material": mat, "Camada": cam, "PartNumber": pn, "Descricao": desc,
                       "BOM_por_metro": round(st.median(v), 6), "Unidade": un, "OPs": len(v), "Dispersao": round(disp, 3)})

with open(os.path.join(AQUI, "bom_mangueira_sap.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=list(linhas[0]), delimiter=";")
    w.writeheader()
    for l in linhas:
        w.writerow({**l, "BOM_por_metro": str(l["BOM_por_metro"]).replace(".", ","), "Dispersao": str(l["Dispersao"]).replace(".", ",")})

# comparação com o simulador
chave = lambda n: re.sub(r"-0+(\d)", r"-\1", re.sub(r"\s+", "", str(n)).upper())
sim = defaultdict(dict)
for b in csv.DictReader(open(SIM, encoding="utf-8-sig"), delimiter=";"):
    sim[chave(b["Mangueira"])][b["PartNumber"]] = float(b["BOM_por_metro"].replace(",", "."))
comp = []
for l in linhas:
    s = sim.get(chave(l["Mangueira"]))
    if s is None:
        continue
    v = s.get(l["PartNumber"])
    comp.append([l["Mangueira"], l["PartNumber"], l["Camada"], l["BOM_por_metro"], v if v is not None else "",
                 f"{(l['BOM_por_metro'] / v - 1) * 100:+.1f}%" if v else "PN novo"])
with open(os.path.join(AQUI, "bom_comparacao.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f, delimiter=";"); w.writerow(["Mangueira", "PartNumber", "Camada", "BOM_SAP", "BOM_simulador", "Diferenca"])
    w.writerows(comp)

fonte = defaultdict(int)
for op, (m, _, o) in ops.items():
    fonte[o] += 1
print(f"{len(razoes)} mangueiras, {len(linhas)} linhas de BOM; OPs usadas: {dict(fonte)}")
print(f"comparação com o simulador: {len(comp)} linhas em {len({c[0] for c in comp})} mangueiras")
