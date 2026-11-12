"""Verificação do passo 3 (MEL-266): GMS_Painel.Report (vigente) com a página pg_oee2 e o item OEE2 no menu.

Uso:  python verificar_oee2.py [--base REV]      (REV = commit de partida; padrão HEAD, antes do commit desta mudança)

Confere:
 1. todo .json/.pbir do relatório faz parse;
 2. as 10 páginas antigas: nada mudou fora do menu (só position.y dos itens do menu, +32 px do que ficou abaixo de "Hora-Hora"),
    mais o visual novo sub_oee2; page.json, reportExtensions.json e arquivos fora das páginas idênticos aos da base;
 3. navegação: 11 botões por página, cada um aponta para a página certa, o ativo é o da própria página, a barra vermelha
    fica na altura dele, OEE2 vem logo depois de Hora-Hora e nada no menu passa de x = 200;
 4. nada fora do canvas 1280x720 e sem sobreposição (exceto o fundo do menu e a barra ativa) nas 11 páginas;
 5. pg_oee2: slicers e syncGroup iguais aos da pg_horahora, só campos que existem (medidas do oee2.tmdl.md e colunas do
    modelo), sem medida de relatório (schema extension) nova, 5 cartões, 4 gráficos, rodapé, títulos em pergunta;
 6. pages.json: pg_oee2 logo depois de pg_horahora."""
import argparse
import io
import itertools
import json
import os
import re
import subprocess
import sys
import tarfile

AQUI = os.path.dirname(os.path.abspath(__file__))
REL = os.path.normpath(os.path.join(AQUI, "..", "GMS_Painel.Report"))
MD = os.path.normpath(os.path.join(AQUI, "..", "modelo", "oee2.tmdl.md"))
CSV_MOTIVOS = os.path.normpath(os.path.join(AQUI, "..", "modelo", "dMotivoParada.csv"))
H = 32

ORDEM = ["sub_visao_geral", "sub_horahora", "sub_oee2", "sub_paradas", "sub_refugo_ppm", "sub_refugo_ppm_cortes",
         "sub_extrusora", "sub_fluxo_1", "sub_fluxo_2"]
DESTINO = {"sub_visao_geral": "pg_visao_geral", "sub_horahora": "pg_horahora", "sub_oee2": "pg_oee2",
           "sub_paradas": "pg_paradas", "sub_refugo_ppm": "pg_refugo_ppm", "sub_refugo_ppm_cortes": "pg_refugo_ppm_cortes",
           "sub_extrusora": "pg_extrusora", "sub_fluxo_1": "pg_fluxo_1", "sub_fluxo_2": "pg_fluxo_2",
           "sub_producao_montagem": "pg_producao_montagem", "sub_paradas_montagem": "pg_paradas_montagem"}
ATIVO = {v: k for k, v in DESTINO.items()}
MENU = set(DESTINO) | {"txt_secao_montagem", "nav_barra_ativa"}
Y = {n: 106 + i * H for i, n in enumerate(ORDEM)}
Y.update({"sub_producao_montagem": 430, "sub_paradas_montagem": 462, "txt_secao_montagem": 410})
falhas = []


def ok(c, msg):
    print(("OK    " if c else "FALHA ") + msg)
    if not c:
        falhas.append(msg)


def lit(n):
    return n["expr"]["Literal"]["Value"].strip("'")


def base_do_git(rev):
    topo = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=AQUI, capture_output=True, text=True, check=True).stdout.strip()
    rel = os.path.relpath(REL, topo).replace("\\", "/")
    tar = subprocess.run(["git", "archive", "--format=tar", rev, "--", rel], cwd=topo, capture_output=True, check=True).stdout
    arq = {}
    with tarfile.open(fileobj=io.BytesIO(tar)) as t:
        for m in t.getmembers():
            if m.isfile():
                arq[m.name[len(rel) + 1:]] = t.extractfile(m).read()
    return arq


def atuais():
    arq = {}
    for raiz, _, nomes in os.walk(REL):
        for n in nomes:
            p = os.path.join(raiz, n)
            with open(p, "rb") as f:
                arq[os.path.relpath(p, REL).replace("\\", "/")] = f.read()
    return arq


def campos(d):
    """Medidas e colunas referenciadas num visual: {(entidade, propriedade, tipo, schema)}."""
    achados = set()

    def anda(x):
        if isinstance(x, dict):
            for k in ("Measure", "Column"):
                if k in x and isinstance(x[k], dict) and "Property" in x[k]:
                    ref = x[k].get("Expression", {}).get("SourceRef", {})
                    if "Entity" in ref:
                        achados.add((ref["Entity"], x[k]["Property"], k, ref.get("Schema")))
            for v in x.values():
                anda(v)
        elif isinstance(x, list):
            for v in x:
                anda(v)

    anda(d)
    return achados


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="HEAD")
    a = ap.parse_args()
    base, agora = base_do_git(a.base), atuais()

    # 1. parse
    n = 0
    for rel, b in agora.items():
        if rel.endswith(".json") or rel.endswith(".pbir"):
            try:
                json.loads(b.decode("utf-8"))
                n += 1
            except Exception as e:
                ok(False, f"parse {rel}: {e}")
    ok(True, f"1. {n} arquivos .json/.pbir do relatório fazem parse")

    paginas = sorted({r.split("/")[2] for r in agora if r.startswith("definition/pages/pg_")})
    antigas = [p for p in paginas if p != "pg_oee2"]
    ok(len(paginas) == 11 and len(antigas) == 10, f"1b. 11 páginas ({', '.join(paginas)})")

    # 2. páginas antigas: só o menu
    # .pbi/ é cache local do Desktop (ignorado pelo git): fora da comparação
    fora = [r for r in agora if not r.startswith("definition/pages/pg_") and not r.startswith(".pbi/")]
    dif_fora = sorted(r for r in set(fora) | {b for b in base if not b.startswith("definition/pages/pg_")}
                      if agora.get(r) != base.get(r))
    ok(dif_fora == ["definition/pages/pages.json"], f"2a. fora das páginas só o pages.json muda {dif_fora}")
    tot_y = 0
    for pg in antigas:
        pref = f"definition/pages/{pg}/"
        rels_b = {r for r in base if r.startswith(pref)}
        rels_a = {r for r in agora if r.startswith(pref)}
        novos = sorted(rels_a - rels_b)
        removidos = sorted(rels_b - rels_a)
        ok(novos == [pref + "visuals/sub_oee2/visual.json"] and not removidos,
           f"2b. {pg}: único arquivo novo é sub_oee2; nenhum removido {novos if novos != [pref + 'visuals/sub_oee2/visual.json'] else ''}{removidos or ''}")
        erradas, movidos = [], []
        for r in sorted(rels_a & rels_b):
            if agora[r] == base[r]:
                continue
            nome = r.split("/")[-2] if r.endswith("visual.json") else None
            if nome not in MENU:
                erradas.append(r)
                continue
            da, db = json.loads(agora[r]), json.loads(base[r])
            ya, yb = da["position"]["y"], db["position"]["y"]
            da["position"]["y"] = db["position"]["y"] = 0
            esperado = yb + H if (nome != "nav_barra_ativa" and yb >= 170) else None
            if da != db or (esperado is not None and ya != esperado):
                erradas.append(f"{r} (y {yb}->{ya})")
            movidos.append(nome)
        tot_y += len(movidos)
        ok(not erradas, f"2c. {pg}: {len(movidos)} itens do menu mudaram só de y (+32); nada mais {erradas or ''}")

    # 3. navegação e menu (11 páginas)
    for pg in paginas:
        vis = {}
        pref = f"definition/pages/{pg}/visuals/"
        for r, b in agora.items():
            if r.startswith(pref) and r.endswith("visual.json"):
                vis[r.split("/")[-2]] = json.loads(b)
        botoes = {k for k in vis if k.startswith("sub_")}
        certo = botoes == set(DESTINO)
        for k in botoes & set(DESTINO):
            vl = vis[k]["visual"]["visualContainerObjects"]["visualLink"][0]["properties"]
            certo &= lit(vl["type"]) == "PageNavigation" and lit(vl["navigationSection"]) == DESTINO[k]
        ys_ok = all(vis[k]["position"]["y"] == Y[k] for k in botoes & set(Y)) and vis["txt_secao_montagem"]["position"]["y"] == Y["txt_secao_montagem"]
        ativos = [k for k in botoes if any("fillColor" in p["properties"] for p in vis[k]["visual"]["objects"]["fill"])]
        barra = vis["nav_barra_ativa"]["position"]["y"]
        ok(certo and ys_ok and ativos == [ATIVO[pg]] and barra == vis[ATIVO[pg]]["position"]["y"],
           f"3. {pg}: 11 botões apontam certo, y esperados, ativo = {ATIVO[pg]}, barra na altura dele")
        ok(vis["sub_oee2"]["position"]["y"] == vis["sub_horahora"]["position"]["y"] + H
           and lit(vis["sub_oee2"]["visual"]["objects"]["text"][1]["properties"]["text"]) == "OEE2",
           f"3b. {pg}: item OEE2 logo depois de Hora-Hora")
        # 4. canvas e sobreposição
        pos = {k: (d["position"]["x"], d["position"]["y"], d["position"]["x"] + d["position"]["width"],
                   d["position"]["y"] + d["position"]["height"]) for k, d in vis.items()}
        fora_c = [k for k, (x0, y0, x1, y1) in pos.items() if x0 < 0 or y0 < 0 or x1 > 1280.001 or y1 > 720.001]
        sobre = []
        for (n1, r1), (n2, r2) in itertools.combinations(pos.items(), 2):
            if min(r1[2], r2[2]) > max(r1[0], r2[0]) + 0.01 and min(r1[3], r2[3]) > max(r1[1], r2[1]) + 0.01:
                if "faixa" in (n1, n2):
                    continue
                if "nav_barra_ativa" in (n1, n2) and (set([n1, n2]) - {"nav_barra_ativa"}) <= {ATIVO[pg]}:
                    continue
                sobre.append((n1, n2))
        vaza = [k for k, r in pos.items() if k != "faixa" and r[0] < 200 and r[2] > 200]
        menu_y = max(r[3] for k, r in pos.items() if k in MENU)
        ok(not fora_c and not sobre and not vaza and menu_y <= 720,
           f"4. {pg}: {len(pos)} visuais dentro de 1280x720, sem sobreposição, menu até y={menu_y:.0f} e sem passar de x=200 "
           f"{fora_c or ''}{sobre or ''}{vaza or ''}")

    # 5. pg_oee2
    pref = "definition/pages/pg_oee2/visuals/"
    v = {r.split("/")[-2]: json.loads(b) for r, b in agora.items() if r.startswith(pref) and r.endswith("visual.json")}
    h = {r.split("/")[-2]: json.loads(b) for r, b in agora.items()
         if r.startswith("definition/pages/pg_horahora/visuals/") and r.endswith("visual.json")}
    ok(all(v[k] == h[k] for k in ("seg0", "seg1", "seg2")) and
       [v[k]["visual"]["syncGroup"]["groupName"] for k in ("seg0", "seg1", "seg2")] == ["gms_maquina_hh", "gms_turno", "gms_data"],
       "5a. slicers Máquina, Turno e Período iguais aos da pg_horahora, com o mesmo syncGroup")
    pj = json.loads(agora["definition/pages/pg_oee2/page.json"].decode("utf-8"))
    ok(pj["name"] == "pg_oee2" and pj["displayName"] == "OEE2 Trançagem" and pj["width"] == 1280 and pj["height"] == 720,
       "5b. page.json: pg_oee2 / OEE2 Trançagem / 1280x720")
    txt = lambda d: d["visual"]["objects"]["general"][0]["properties"]["paragraphs"][0]["textRuns"][0]["value"]
    ok(txt(v["titulo"]) == "OEE2 Trançagem" and txt(v["txt_subtitulo"]) == "OEE2 (apontamento) · padrão Danfoss/Factbird · sem sensor",
       "5c. título e subtítulo certos")
    kp = [v[f"kpi{i}"] for i in range(5)]
    nomes_kpi = [k["visual"]["query"]["queryState"]["Data"]["projections"][0]["field"]["Measure"]["Property"] for k in kp]
    ok(nomes_kpi == ["OEE2", "OEE2 TCU", "OEE2 Disponibilidade", "OEE2 Performance", "OEE2 Qualidade"]
       and all(k["visual"]["visualType"] == "cardVisual" for k in kp), f"5d. 5 cardVisual: {nomes_kpi}")
    refs = [k["visual"].get("objects", {}).get("referenceLabel", [{}])[0].get("properties", {}).get("value", {}).get("expr", {})
            .get("Measure", {}).get("Property") for k in kp]
    ok(refs == ["OEE2 Ref. OEE2", "OEE2 Ref. TCU", None, None, None], f"5e. referências de set a nov só no OEE2 e no TCU {refs}")
    tipos = {k: v[k]["visual"]["visualType"] for k in ("g_cascata", "g_pareto", "g_matriz", "g_dia")}
    ok(tipos == {"g_cascata": "waterfallChart", "g_pareto": "clusteredBarChart", "g_matriz": "pivotTable", "g_dia": "lineChart"},
       f"5f. cascata, Pareto, matriz e linha: {tipos}")
    perguntas = [lit(v[k]["visual"]["visualContainerObjects"]["title"][0]["properties"]["text"]) for k in tipos]
    ok(all(p.endswith("?") for p in perguntas), f"5g. títulos dos gráficos são perguntas: {perguntas}")
    ok("rodape" in v and "Limitações" in txt(v["rodape"]) and "sensor" in txt(v["rodape"]) and "data do refugo" in txt(v["rodape"]),
       "5h. rodapé com as limitações (sem sensor; qualidade pela data do refugo)")

    # campos: medidas do oee2.tmdl.md, colunas do modelo, nada de medida de relatório nova
    with open(MD, encoding="utf-8") as f:
        medidas_md = set(re.findall(r"measure '([^']+)' =", f.read()))
    with open(CSV_MOTIVOS, encoding="utf-8-sig") as f:
        cols_motivo = set(f.readline().strip().split(";"))
    colunas_ok = {"fHoraCheia": {"Célula", "Data BI", "Turno BI", "Motivo Padrão", "Parado", "Real", "Minutos", "Meta Cheia"},
                  "dTurno": {"Turno"}, "dCalendario": {"Date", "Ano", "Mês", "Dia"}, "dEtapaOEE": {"Etapa", "Ordem"},
                  "dMotivoParada": cols_motivo}
    usados = set()
    for d in v.values():
        usados |= campos(d)
    ruins = []
    for ent, prop, tipo, schema in sorted(usados, key=str):
        if tipo == "Measure":
            if schema == "extension" or not (prop in medidas_md or (ent == "Medidas" and prop == "Dado Atualizado até")):
                ruins.append((ent, prop, schema))
        elif prop not in colunas_ok.get(ent, set()):
            ruins.append((ent, prop, schema))
    medidas_usadas = sorted(p for e, p, t, sc in usados if t == "Measure")
    ok(not ruins, f"5i. todos os campos da pg_oee2 existem (medidas no oee2.tmdl.md, colunas do modelo), nenhuma medida de "
                  f"relatório nova {ruins or ''}")
    print("      medidas usadas:", ", ".join(medidas_usadas))
    ok(agora["definition/reportExtensions.json"] == base["definition/reportExtensions.json"],
       "5j. reportExtensions.json igual ao da base (nenhuma medida de relatório criada)")

    # 6. pages.json
    pjson = json.loads(agora["definition/pages/pages.json"].decode("utf-8"))
    ordem = pjson["pageOrder"]
    ok(ordem.index("pg_oee2") == ordem.index("pg_horahora") + 1 and sorted(ordem) == sorted(paginas),
       f"6. pages.json: pg_oee2 logo depois de pg_horahora ({ordem.index('pg_oee2') + 1}ª de {len(ordem)})")
    print(f"\n{len(paginas)} páginas; {tot_y} itens de menu movidos nas 10 antigas; pg_oee2 com {len(v)} visuais")
    print("RESULTADO:", "tudo certo" if not falhas else f"{len(falhas)} falha(s)")
    sys.exit(1 if falhas else 0)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
