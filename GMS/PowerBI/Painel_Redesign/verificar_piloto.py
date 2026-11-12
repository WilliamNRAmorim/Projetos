"""Verificacao do redesign (piloto + passo 5): copia Painel_Redesign x vigente GMS_Painel.Report, 10 paginas."""
import json, os, re, filecmp, itertools, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
VIG = os.path.normpath(os.path.join(AQUI, "..", "GMS_Painel.Report"))
NOV = os.path.join(AQUI, "GMS_Painel.Report")
falhas = []

DESTINO = {"sub_visao_geral": "pg_visao_geral", "sub_horahora": "pg_horahora", "sub_paradas": "pg_paradas",
           "sub_refugo_ppm": "pg_refugo_ppm", "sub_refugo_ppm_cortes": "pg_refugo_ppm_cortes",
           "sub_extrusora": "pg_extrusora", "sub_fluxo_1": "pg_fluxo_1", "sub_fluxo_2": "pg_fluxo_2",
           "sub_producao_montagem": "pg_producao_montagem", "sub_paradas_montagem": "pg_paradas_montagem"}
ATIVO = {v: k for k, v in DESTINO.items()}
PAGINAS = sorted(ATIVO)


def ok(c, msg):
    print(("OK    " if c else "FALHA ") + msg)
    if not c:
        falhas.append(msg)


def lj(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def medidas(d):
    return set(re.findall(r'"Property": "([^"]+)"', json.dumps(d, ensure_ascii=False)))


def vis(raiz, pg):
    base = os.path.join(raiz, "definition", "pages", pg, "visuals")
    return {n: lj(os.path.join(base, n, "visual.json")) for n in os.listdir(base)}


def lit(n):
    return n["expr"]["Literal"]["Value"].strip("'")


# 1. parse
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

tot_vis = tot_mant = tot_conv = 0
for pg in PAGINAS:
    print(f"--- {pg}")
    a, b = vis(VIG, pg), vis(NOV, pg)
    pa = lj(os.path.join(VIG, "definition", "pages", pg, "page.json"))
    pb = lj(os.path.join(NOV, "definition", "pages", pg, "page.json"))

    # 2. query / filterConfig / visualLink em todo visual mantido
    removidos = sorted(set(a) - set(b))
    permitidos = {n for n in removidos if n in ("mod_mangueira", "mod_montagem") or re.fullmatch(r"kpi\d+_d", n)}
    ok(set(removidos) == permitidos, f"2a. visuais removidos só mod_* e cards-delta fundidos: {removidos}")
    dif, mantidos = [], 0
    for nome in sorted(set(a) & set(b)):
        va, vb = a[nome], b[nome]
        if re.fullmatch(r"kpi\d+", nome) and va["visual"]["visualType"] == "card":
            continue
        mantidos += 1
        for rot, ga, gb in (
            ("query", va["visual"].get("query"), vb["visual"].get("query")),
            ("filterConfig", va.get("filterConfig"), vb.get("filterConfig")),
            ("visualLink", va["visual"].get("visualContainerObjects", {}).get("visualLink"),
             vb["visual"].get("visualContainerObjects", {}).get("visualLink")),
            ("syncGroup", va["visual"].get("syncGroup"), vb["visual"].get("syncGroup")),
            ("expansionStates", va["visual"].get("expansionStates"), vb["visual"].get("expansionStates")),
            ("tipo", va["visual"]["visualType"], vb["visual"]["visualType"]),
        ):
            if ga != gb:
                dif.append(f"{nome}.{rot}")
    ok(not dif, f"2b. {mantidos} visuais mantidos: query/filterConfig/visualLink/syncGroup/tipo idênticos {dif or ''}")
    ok(pa.get("filterConfig") == pb.get("filterConfig") and
       {k: v for k, v in pa.items() if k != "objects"} == {k: v for k, v in pb.items() if k != "objects"},
       "2c. page.json: filtros e metadados da página idênticos (só o fundo muda)")
    ok(lit(pb["objects"]["background"][0]["properties"]["color"]["solid"]["color"]) == "#F2F3F5",
       "2d. fundo da página #F2F3F5")

    # 3. cards convertidos ou fundidos
    for nome in sorted(x for x in a if re.fullmatch(r"kpi\d+", x) and a[x]["visual"]["visualType"] == "card"):
        antes = medidas(a[nome]) | (medidas(a[nome + "_d"]) if nome + "_d" in a else set())
        vb = b[nome]
        depois = medidas(vb)
        qa = a[nome]["visual"]["query"]["queryState"]["Values"]["projections"][0]
        qb = {k: v for k, v in vb["visual"]["query"]["queryState"]["Data"]["projections"][0].items()
              if k != "displayName"}
        ok(antes == depois and vb["visual"]["visualType"] == "cardVisual" and qa == qb,
           f"3. {nome}{'+_d' if nome + '_d' in a else ''}: cardVisual, mesmas medidas {sorted(depois)}"
           + ("" if antes == depois else f" (antes {sorted(antes)})"))
        tot_conv += 1

    # 4. nenhuma medida perdida na página
    ua = set().union(*[medidas(v) for v in a.values()])
    ub = set().union(*[medidas(v) for v in b.values()])
    ok(ua == ub, f"4. união de medidas/campos da página igual ({len(ua)})"
       + ("" if ua == ub else f" perdidas {sorted(ua - ub)} novas {sorted(ub - ua)}"))

    # 5. canvas e sobreposicao
    pos = {}
    for nome, d in b.items():
        p = d["position"]
        pos[nome] = (p["x"], p["y"], p["x"] + p["width"], p["y"] + p["height"])
    fora = [k for k, (x0, y0, x1, y1) in pos.items() if x0 < 0 or y0 < 0 or x1 > 1280.001 or y1 > 720.001]
    ok(not fora, f"5a. {len(pos)} visuais dentro de 1280x720 {fora or ''}")
    sobre = []
    for (n1, r1), (n2, r2) in itertools.combinations(pos.items(), 2):
        if min(r1[2], r2[2]) > max(r1[0], r2[0]) + 0.01 and min(r1[3], r2[3]) > max(r1[1], r2[1]) + 0.01:
            if "faixa" in (n1, n2):
                continue
            if "nav_barra_ativa" in (n1, n2) and (set([n1, n2]) - {"nav_barra_ativa"}) <= {ATIVO[pg]}:
                continue
            sobre.append((n1, n2))
    ok(not sobre, f"5b. sem sobreposição fora o fundo do menu e a barra ativa {sobre or ''}")
    vaza = [k for k, r in pos.items() if k != "faixa" and r[0] < 200 and r[2] > 200]
    ok(not vaza, f"5c. itens do menu não passam de x=200 {vaza or ''}")
    ok(all(r[0] >= 200 for k, r in pos.items() if k not in
           {"faixa", "logo", "txt_app", "txt_secao_mangueira", "txt_secao_montagem", "nav_barra_ativa", "atualizado"}
           and not k.startswith("sub_")), "5d. todo o resto fica à direita do menu (x ≥ 200)")

    # 6. botoes de navegacao
    botoes = {k for k in b if k.startswith("sub_")}
    certo = botoes == set(DESTINO) and not any(k.startswith("mod_") for k in b)
    for k in botoes & set(DESTINO):
        vl = b[k]["visual"]["visualContainerObjects"]["visualLink"][0]["properties"]
        certo &= lit(vl["type"]) == "PageNavigation" and lit(vl["navigationSection"]) == DESTINO[k]
    ativos = [k for k in botoes if any("fillColor" in p["properties"] for p in b[k]["visual"]["objects"]["fill"])]
    barra_y = b["nav_barra_ativa"]["position"]["y"]
    ok(certo and ativos == [ATIVO[pg]] and barra_y == b[ATIVO[pg]]["position"]["y"],
       f"6. 10 botões apontam certo, ativo = {ATIVO[pg]}, barra vermelha na altura dele")

    tot_vis += len(b)
    tot_mant += mantidos

# 7. paginas e arquivos fora do esperado
ok(filecmp.cmp(os.path.join(VIG, "definition", "reportExtensions.json"),
               os.path.join(NOV, "definition", "reportExtensions.json"), shallow=False),
   "7a. reportExtensions.json igual ao da vigente")
difs = []
for raiz, _, arqs in os.walk(NOV):
    for a_ in arqs:
        rel = os.path.relpath(os.path.join(raiz, a_), NOV).replace("\\", "/")
        if rel.startswith("definition/pages/pg_"):
            continue
        v = os.path.join(VIG, rel)
        if not os.path.exists(v) or not filecmp.cmp(v, os.path.join(raiz, a_), shallow=False):
            difs.append(rel)
ok(difs == ["StaticResources/RegisteredResources/GMS_Tema.json"],
   f"7b. fora das páginas só o tema difere da vigente {difs}")
pj_ok = filecmp.cmp(os.path.join(VIG, "definition", "pages", "pages.json"),
                    os.path.join(NOV, "definition", "pages", "pages.json"), shallow=False)
ok(pj_ok, "7c. pages.json igual")
print(f"\n{len(PAGINAS)} páginas, {tot_vis} visuais na cópia ({tot_mant} mantidos sem conversão, {tot_conv} cards convertidos)")
print("RESULTADO:", "tudo certo" if not falhas else f"{len(falhas)} falha(s)")
sys.exit(1 if falhas else 0)
