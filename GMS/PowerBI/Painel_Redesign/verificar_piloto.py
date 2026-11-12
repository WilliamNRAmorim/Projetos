"""Verificacao do piloto (passos 1-3): copia Painel_Redesign x vigente GMS_Painel.Report."""
import json, os, re, filecmp, itertools, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
VIG = os.path.normpath(os.path.join(AQUI, "..", "GMS_Painel.Report"))
NOV = os.path.join(AQUI, "GMS_Painel.Report")
PG = "pg_visao_geral"
falhas = []


def ok(c, msg):
    print(("OK   " if c else "FALHA ") + msg)
    if not c:
        falhas.append(msg)


def lj(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


# 1. todo json faz parse
n = 0
for raiz, _, arqs in os.walk(NOV):
    for a in arqs:
        if a.endswith(".json") or a.endswith(".pbir"):
            try:
                lj(os.path.join(raiz, a))
                n += 1
            except Exception as e:
                ok(False, f"parse {os.path.join(raiz, a)}: {e}")
ok(True, f"1. {n} arquivos .json/.pbir da copia fazem parse")

# 2. query / filterConfig / visualLink
vv = os.path.join(VIG, "definition", "pages", PG, "visuals")
nv = os.path.join(NOV, "definition", "pages", PG, "visuals")
convertidos = {"kpi0", "kpi1", "kpi2", "kpi3"}
comuns = sorted(set(os.listdir(vv)) & set(os.listdir(nv)))
dif = []
for nome in comuns:
    if nome in convertidos:
        continue
    a, b = lj(os.path.join(vv, nome, "visual.json")), lj(os.path.join(nv, nome, "visual.json"))
    for rotulo, ga, gb in (
        ("query", a["visual"].get("query"), b["visual"].get("query")),
        ("filterConfig", a.get("filterConfig"), b.get("filterConfig")),
        ("visualLink", a["visual"].get("visualContainerObjects", {}).get("visualLink"),
         b["visual"].get("visualContainerObjects", {}).get("visualLink")),
        ("syncGroup", a["visual"].get("syncGroup"), b["visual"].get("syncGroup")),
        ("sort/expansion", a["visual"].get("expansionStates"), b["visual"].get("expansionStates")),
    ):
        if ga != gb:
            dif.append(f"{nome}.{rotulo}")
ok(not dif, f"2a. query/filterConfig/visualLink/syncGroup idênticos em {len(comuns) - len(convertidos)} visuais comuns {dif or ''}")
ok(set(comuns) >= convertidos, "2b. kpi0..3 existem nas duas")


def medidas(d):
    return set(re.findall(r'"Property": "([^"]+)"', json.dumps(d, ensure_ascii=False)))


for k in sorted(convertidos):
    a, b = lj(os.path.join(vv, k, "visual.json")), lj(os.path.join(nv, k, "visual.json"))
    ma, mb = medidas(a), medidas(b)
    ok(ma == mb and b["visual"]["visualType"] == "cardVisual",
       f"2c. {k}: cardVisual, mesmas medidas {sorted(mb)}" + ("" if ma == mb else f" (antes {sorted(ma)})"))
    qa = a["visual"]["query"]["queryState"]["Values"]["projections"][0]
    qb = b["visual"]["query"]["queryState"]["Data"]["projections"][0]
    qb2 = {x: y for x, y in qb.items() if x != "displayName"}
    ok(qa == qb2, f"2d. {k}: projeção (campo, queryRef, nativeQueryRef, format) preservada")

# 3. canvas e sobreposicao
pos = {}
for nome in os.listdir(nv):
    d = lj(os.path.join(nv, nome, "visual.json"))
    p = d["position"]
    pos[nome] = (p["x"], p["y"], p["x"] + p["width"], p["y"] + p["height"])
fora = [k for k, (x0, y0, x1, y1) in pos.items() if x0 < 0 or y0 < 0 or x1 > 1280 or y1 > 720]
ok(not fora, f"3a. {len(pos)} visuais dentro de 1280x720 {fora or ''}")
permitido = {frozenset(p) for p in [("faixa", "logo"), ("faixa", "txt_app")]}
sobre = []
for (a, ra), (b, rb) in itertools.combinations(pos.items(), 2):
    if min(ra[2], rb[2]) > max(ra[0], rb[0]) and min(ra[3], rb[3]) > max(ra[1], rb[1]):
        if "faixa" in (a, b):          # fundo do menu: tudo do menu fica em cima dele de proposito
            continue
        if {a, b} == {"nav_barra_ativa", "sub_visao_geral"}:
            continue
        sobre.append((a, b))
ok(not sobre, f"3b. sem sobreposição fora o fundo do menu e a barra do item ativo {sobre or ''}")
conteudo_fora_menu = [k for k, r in pos.items() if k != "faixa" and r[0] >= 200 or False]
menu_vaza = [k for k, r in pos.items() if k != "faixa" and r[0] < 200 and r[2] > 200]
ok(not menu_vaza, f"3c. itens do menu não passam de x=200 {menu_vaza or ''}")

# 4. as outras paginas identicas
iguais = True
pg_dirs = [p for p in os.listdir(os.path.join(VIG, "definition", "pages")) if p.startswith("pg_") and p != PG]
for pg in pg_dirs:
    cmp = filecmp.dircmp(os.path.join(VIG, "definition", "pages", pg), os.path.join(NOV, "definition", "pages", pg))
    def difere(c):
        if c.left_only or c.right_only or c.diff_files or c.funny_files:
            return True
        return any(difere(s) for s in c.subdirs.values())
    if difere(cmp):
        iguais = False
        print("   difere:", pg)
ok(iguais and len(pg_dirs) == 9, f"4. {len(pg_dirs)} outras páginas idênticas à vigente")

# fora das paginas: so tema muda
difs = []
for raiz, _, arqs in os.walk(NOV):
    for a in arqs:
        rel = os.path.relpath(os.path.join(raiz, a), NOV)
        v = os.path.join(VIG, rel)
        if rel.replace("\\", "/").startswith(f"definition/pages/{PG}/"):
            continue
        if not os.path.exists(v) or not filecmp.cmp(v, os.path.join(raiz, a), shallow=False):
            difs.append(rel)
print("   arquivos fora da pg_visao_geral que diferem da vigente:", difs)
print("RESULTADO:", "tudo certo" if not falhas else f"{len(falhas)} falha(s)")
sys.exit(1 if falhas else 0)
