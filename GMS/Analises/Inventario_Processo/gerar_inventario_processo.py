# gerar_inventario_processo.py: inventario de material em processo (WIP) da celula, sem digitar mangueira.
# Faz o que o "Inventario Mangueiras - Simulador.xlsm" faz, mas para todas as OPs abertas da ficha_producao:
# situacao = ultima etapa fechada da OP; quantidade = BOM por metro x metros dessa etapa.
#
# Uso: python -I gerar_inventario_processo.py <ficha_producao.csv | ficha.json> <GMS_BOM_Mangueira.json | Simulador.xlsm>
#   - .csv: export da lista (cabecalho com nomes de exibicao).
#   - .json: {"rows":[...]} puxado por REST (nomes internos do SharePoint).
# Saida (nesta pasta): bom_mangueira.csv (BOM em formato longo, molde da futura lista GMS_BOM_Mangueira)
#                      inventario_processo.html (prototipo com SVG; o calculo fino roda no navegador).
import csv, json, os, re, sys, datetime as dt
import openpyxl

FICHA, SIM = sys.argv[1], sys.argv[2]
AQUI = os.path.dirname(os.path.abspath(__file__))

# ---------- BOM do simulador ----------
CAMADAS = [  # (coluna PN, coluna BOM, material, camada, unidade) como na aba INVENTARIO
    (1, 2, "Composto / Tubo", "tubo", "kg"),
    (3, 4, "Fio (arame / textil)", "trama", "kg"),
    (5, 6, "Insulation", "trama", "kg"),
    (7, 8, "Leno", "trama", "kg"),
    (9, 10, "Composto / Cobertura", "cobertura", "kg"),
    (11, 12, "Fita match-mate", "bandagem", "m"),
    (13, 14, "Filme", "bandagem", "m"),
]
CIMENTO = {"HC139-7", "HC139-7(S/G)"}  # regra fixa da celula E24 do simulador

def chave(nome):
    n = re.sub(r"\s+", "", str(nome or "")).upper()
    return re.sub(r"-0+(\d)", r"-\1", n)  # FC598-08 -> FC598-8

bom = {}
if SIM.lower().endswith(".json"):
    # itens da lista GMS_BOM_Mangueira (REST: Title=Mangueira, PartNumber, BOM_por_metro, Camada, Unidade, Material)
    d = json.load(open(SIM, encoding="utf-8"))
    for r in (d["rows"] if isinstance(d, dict) else d):
        b = bom.setdefault(chave(r["Title"]), {"nome": r["Title"], "itens": [], "fonte": r.get("Fonte", "")})
        if any(i["pn"] == r["PartNumber"] for i in b["itens"]):
            continue  # linha repetida na lista não conta duas vezes
        b["itens"].append({"pn": r["PartNumber"], "bom": float(r["BOM_por_metro"]), "mat": r["Material"],
                           "cam": r["Camada"], "un": r["Unidade"]})
else:
    wb = openpyxl.load_workbook(SIM, data_only=True)
    for r in wb["BASE DE DADOS"].iter_rows(min_row=3, values_only=True):
        if not r[0] or chave(r[0]) in bom:
            continue
        itens = []
        for cp, cb, mat, cam, un in CAMADAS:
            pn, q = r[cp], r[cb]
            if pn not in (None, "-", "") and q:
                itens.append({"pn": str(pn), "bom": float(q), "mat": mat, "cam": cam, "un": un})
        if str(r[0]) in CIMENTO:
            itens.append({"pn": "CIMENTO", "bom": 0.007943, "mat": "Cimento", "cam": "trama", "un": "kg"})
        bom[chave(r[0])] = {"nome": str(r[0]), "itens": itens, "fonte": "Simulador 2020"}

if not SIM.lower().endswith(".json"):
  with open(os.path.join(AQUI, "bom_mangueira.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["Mangueira", "Material", "Camada", "PartNumber", "BOM_por_metro", "Unidade"])
    for b in bom.values():
        for i in b["itens"]:
            w.writerow([b["nome"], i["mat"], i["cam"], i["pn"], str(i["bom"]).replace(".", ","), i["un"]])

# ---------- Ficha ----------
# nome de exibicao (csv) -> nome interno (json REST)
CAMPOS = {
    "processo": "processo", "status_processo": "status_processo", "OP": "OP", "Mangueira": "Mangueira",
    "Bitola": "Bitola", "Trançadeira": "Tran_x00e7_adeira",
    "quantidade_tubo": "quantidade_tubo", "quantidade_trancagem": "quantidade_trancagem",
    "quantidade_cobertura": "quantidade_cobertura", "quantidade_bandagem": "quantidade_bandagem",
    "quantidade_vulcanizacao": "quantidade_vulcanizacao", "quantidade_debandagem": "quantidade_debandagem",
    "data_hora_final_tubo": "data_hora_final_tubo", "data_hora_final_trancadeira": "data_hora_final_trancadeira",
    "data_hora_final_cobertura": "data_hora_final_cobertura", "data_hora_final_bandagem": "data_hora_final_bandagem",
    "data_hora_final_vulcanizacao": "data_hora_final_vulcanizacao", "data_hora_final_debandagem": "data_hora_final_debandagem",
    "data_hora_final_mandril": "data_hora_final_mandril",
}

def ler_ficha():
    if FICHA.lower().endswith(".json"):
        # REST: chaves curtas q_<etapa> / f_<etapa> (ou nomes internos); datas em UTC
        d = json.load(open(FICHA, encoding="utf-8"))
        def campo(x, k):
            curto = k.replace("quantidade_", "q_").replace("data_hora_final_", "f_")
            v = x.get(k, x.get(curto, x.get(CAMPOS[k])))
            if k.startswith("data_hora_final_") and v and d.get("utc"):
                v = (dt.datetime.fromisoformat(str(v)[:16]) - dt.timedelta(hours=3)).isoformat(timespec="minutes")
            return v
        return [{k: campo(x, k) for k in CAMPOS} for x in d["rows"]], d.get("puxado_em")
    rows = list(csv.DictReader(open(FICHA, encoding="utf-8-sig")))
    return [{k: x.get(k) for k in CAMPOS} for x in rows], dt.datetime.fromtimestamp(os.path.getmtime(FICHA)).isoformat(timespec="minutes")

def num(v):
    try:
        return float(str(v).replace(",", "."))
    except (TypeError, ValueError):
        return 0.0

def data(v):
    if not v:
        return None
    s = str(v)
    for fmt in ("%m/%d/%Y %I:%M %p", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M"):
        try:
            t = dt.datetime.strptime(s, fmt)
            return t - dt.timedelta(hours=3) if s.endswith("Z") else t
        except ValueError:
            pass
    return None

def etapa(p):
    p = (p or "").lower()
    for k, v in (("mandril", "Mandril"), ("tubo", "Tubo"), ("tran", "Trançagem"), ("cobert", "Cobertura"),
                 ("debanda", "Debandagem"), ("banda", "Bandagem"), ("vulc", "Vulcanização"), ("extr", "Extração/Teste")):
        if k in p:
            return v
    return p or "?"

ALIAS = {}
_al = os.path.join(AQUI, "..", "..", "..", "Producao_GMS_x_MB51", "dados", "aliases_mangueira.csv")
if os.path.exists(_al):
    for a in csv.DictReader(open(_al, encoding="utf-8-sig"), delimiter=";"):
        if a["material_sap"].strip().isdigit():
            ALIAS.setdefault(a["material_sap"].strip(), a["nome_gms"].strip())

def mangueira(v):
    v = str(v or "").strip()
    if v.isdigit() and v in ALIAS:
        return ALIAS[v]  # codigo SAP digitado no lugar do nome
    return f"{v or 'vazio'} (inválida)" if len(v) < 3 else v  # "0", "1": digitação errada na ficha

# etapa atual -> (situacao, ordem das quantidades a tentar: a da ultima etapa fechada primeiro)
SITUACAO = {
    "Trançagem": ("tubo", ["quantidade_tubo"]),
    "Cobertura": ("trancada", ["quantidade_trancagem", "quantidade_tubo"]),
    "Bandagem": ("coberta", ["quantidade_cobertura", "quantidade_trancagem", "quantidade_tubo"]),
    "Vulcanização": ("bandada", ["quantidade_bandagem", "quantidade_cobertura"]),
    "Debandagem": ("bandada", ["quantidade_vulcanizacao", "quantidade_bandagem", "quantidade_cobertura"]),
    # decisao do William (27/11): depois da Debandagem a mangueira ainda conta como Bandada
    "Extração/Teste": ("bandada", ["quantidade_debandagem", "quantidade_vulcanizacao", "quantidade_bandagem"]),
}
FINAIS = [k for k in CAMPOS if k.startswith("data_hora_final_")]

rows, puxado = ler_ficha()
agora = data(puxado) if puxado and "T" not in str(puxado) else dt.datetime.fromisoformat(str(puxado)[:16])
ops, fora = [], []
for x in rows:
    st = (x["status_processo"] or "").lower()
    if st not in ("aguardando", "em processo"):
        continue
    et = etapa(x["processo"])
    base = {"op": str(x["OP"] or "").split(".")[0] or "(sem OP)", "mang": mangueira(x["Mangueira"]),
            "etapa": et, "status": "Em processo" if st == "em processo" else "Aguardando"}
    ult = max([t for t in (data(x[c]) for c in FINAIS) if t], default=None)
    base["dias"] = round((agora - ult).total_seconds() / 86400, 1) if ult and agora else None
    if et not in SITUACAO:
        fora.append(base)  # Mandril e Tubo: ainda nao ha mangueira para contar
        continue
    sit, qs = SITUACAO[et]
    m = next((num(x[q]) for q in qs if num(x[q]) > 0), 0.0)
    b = bom.get(chave(base["mang"]))
    base.update({"sit": sit, "m": m, "bom": bool(b), "fonteBom": b["fonte"] if b else None})
    ops.append(base)

dados = {"puxado": puxado, "fonte": os.path.basename(FICHA), "fonteBom": "lista GMS_BOM_Mangueira" if SIM.lower().endswith(".json") else "simulador", "ops": ops, "fora": fora,
         "bom": {k: v["itens"] for k, v in bom.items()}, "chaves": {o["op"]: chave(o["mang"]) for o in ops}}
tpl = open(os.path.join(AQUI, "inventario_template.html"), encoding="utf-8").read()
html = tpl.replace("/*DADOS*/null", json.dumps(dados, ensure_ascii=False))
open(os.path.join(AQUI, "inventario_processo.html"), "w", encoding="utf-8").write(html)
sem = sum(1 for o in ops if not o["bom"])
print(f"{len(ops)} OPs com mangueira em processo ({sem} sem BOM), {len(fora)} no Mandril/Tubo; {len(bom)} mangueiras na BOM")
