"""Passo 5 do redesign: leva o esqueleto da Visao Geral as outras 9 paginas da copia (idempotente).
Le GMS_Painel.Report (vigente, so leitura) e grava em Painel_Redesign/GMS_Painel.Report.
A Visao Geral (piloto aprovado) e feita por build_visao_geral.py e nao e tocada aqui."""
import json, os, copy, re, shutil

AQUI = os.path.dirname(os.path.abspath(__file__))
VIG = os.path.normpath(os.path.join(AQUI, "..", "GMS_Painel.Report", "definition", "pages"))
NOVO = os.path.join(AQUI, "GMS_Painel.Report", "definition", "pages")
SEMI, REG = "Segoe UI Semibold", "Segoe UI"


# ------------------------------------------------------------------ utilidades
def lj(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def wj(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)


def F(px):
    """px do prototipo -> pt do Power BI (x0,75, passo de 0,5 pt)."""
    return {10: 7.5, 11: 8, 12: 9, 13: 10, 14: 10.5, 16: 12, 20: 15, 22: 16.5, 30: 22.5}[px]


def fmt(x):
    return str(int(x)) if x == int(x) else str(x)


def lit(v):
    return {"expr": {"Literal": {"Value": v}}}


def s(txt):
    return lit("'" + txt.replace("'", "''") + "'")


def cor(h):
    return {"solid": {"color": s(h)}}


def valor(n):
    """Valor literal de uma propriedade ({'expr':{'Literal':...}}), sem aspas."""
    return n["expr"]["Literal"]["Value"].strip("'")


def pos(d, x, y, w, h, z=None):
    p = d["position"]
    p["x"], p["y"], p["width"], p["height"] = x, y, w, h
    if z is not None:
        p["z"] = z
        p["tabOrder"] = z


def alt(txt):
    return {"general": [{"properties": {"altText": s(txt)}}]}


def sem_titulo():
    return {"title": [{"properties": {"show": lit("false")}}]}


VG = "pg_visao_geral"


def vin(pg, nome):
    return lj(os.path.join(VIG, pg, "visuals", nome, "visual.json"))


# ------------------------------------------------------------------ configuracao por pagina
H = 32
Y0 = 106
Y_MONT = Y0 + 8 * H + 16  # 378
ORDEM = ["sub_visao_geral", "sub_horahora", "sub_paradas", "sub_refugo_ppm", "sub_refugo_ppm_cortes",
         "sub_extrusora", "sub_fluxo_1", "sub_fluxo_2"]
DESTINO = {"sub_visao_geral": "pg_visao_geral", "sub_horahora": "pg_horahora", "sub_paradas": "pg_paradas",
           "sub_refugo_ppm": "pg_refugo_ppm", "sub_refugo_ppm_cortes": "pg_refugo_ppm_cortes",
           "sub_extrusora": "pg_extrusora", "sub_fluxo_1": "pg_fluxo_1", "sub_fluxo_2": "pg_fluxo_2",
           "sub_producao_montagem": "pg_producao_montagem", "sub_paradas_montagem": "pg_paradas_montagem"}
ATIVO = {v: k for k, v in DESTINO.items()}
ROTULO_MONT = {"sub_producao_montagem": "Produção", "sub_paradas_montagem": "Paradas"}

CFG = {
    "pg_horahora": dict(
        titulo="Hora-Hora · Trançagem", sub="Metros, meta e paradas por hora cheia",
        corpo={"g_prod_hora": (216, 208, 640, 456), "g_motivo": (872, 208, 392, 272),
               "g_motivo2": (872, 496, 392, 168), "dia_produtivo": (216, 680, 640, 24)},
        subs={"g_prod_hora": "Metros por hora cheia, real × meta", "g_motivo": "Minutos parados",
              "g_motivo2": "Minutos parados, 2º motivo"}),
    "pg_paradas": dict(
        titulo="Paradas e Qualidade", sub="Mangueira · horas paradas, motivos e refugo",
        corpo={"g_pareto": (216, 208, 640, 240), "g_turno": (872, 208, 392, 240),
               "g_pareto_ref": (216, 464, 516, 240), "g_tipo": (748, 464, 516, 240)},
        subs={"g_pareto": "Horas paradas e % acumulado", "g_turno": "Horas paradas por turno",
              "g_pareto_ref": "Metros refugados e % acumulado", "g_tipo": "Horas paradas por tipo"}),
    "pg_refugo_ppm": dict(
        titulo="Refugo PPM", sub="Mangueira · refugo sobre a produção, contra a base de 2025",
        corpo={"g_ppm_mes": (216, 208, 1048, 240), "g_causa": (216, 464, 1048, 240)},
        subs={"g_ppm_mes": "PPM por mês, contra a meta", "g_causa": "Metros refugados e % acumulado"}),
    "pg_refugo_ppm_cortes": dict(
        titulo="Refugo PPM por corte", sub="Por dia, turno, tipo de mangueira e trançadeira",
        corpo={"g_dia": (216, 88, 516, 300), "g_turno": (748, 88, 516, 300),
               "g_mangueira": (216, 404, 516, 300), "g_trancadeira": (748, 404, 516, 300)},
        subs={"g_dia": "PPM por dia", "g_turno": "PPM por turno", "g_mangueira": "PPM por tipo de mangueira",
              "g_trancadeira": "PPM por trançadeira"}),
    "pg_extrusora": dict(
        titulo="Extrusora de Mandril", sub="Metros extrudados e refugo",
        corpo={"g_dia": (216, 208, 516, 240), "g_bitola": (748, 208, 516, 240),
               "g_turno": (216, 464, 336, 240), "g_ref_causa": (568, 464, 336, 240),
               "g_ref_dia": (920, 464, 344, 240)},
        subs={"g_dia": "Metros por dia", "g_bitola": "Metros por bitola", "g_turno": "Metros por turno",
              "g_ref_causa": "Kg refugados por código de erro", "g_ref_dia": "Kg refugados por dia"}),
    "pg_fluxo_1": dict(
        titulo="Fluxo · Etapas", sub="Tubo → cabine, etapa por etapa", corpo={}, subs={}),
    "pg_fluxo_2": dict(
        titulo="Fluxo · Mão de obra", sub="Trançagem e cabine: metros e pessoas por dia",
        corpo={"g_metros": (216, 384, 516, 280), "g_pessoas": (748, 384, 516, 280)},
        subs={"g_metros": "Metros por dia, por mês", "g_pessoas": "Pessoas por dia, por mês"}),
    "pg_producao_montagem": dict(
        titulo="Produção da Montagem", sub="Peças, OTs e paradas por célula e turno",
        corpo={"g_dia": (216, 208, 516, 240), "g_celula": (748, 208, 516, 240),
               "g_turno": (216, 464, 336, 240), "g_parada_dia": (568, 464, 696, 240)},
        subs={"g_dia": "Peças por dia", "g_celula": "Peças por célula", "g_turno": "Peças por turno",
              "g_parada_dia": "Minutos de parada real por dia"}),
    "pg_paradas_montagem": dict(
        titulo="Paradas da Montagem", sub="Parada real e tempo excedido, por célula e motivo",
        corpo={"g_motivo": (216, 208, 516, 496), "g_celula": (748, 208, 516, 496)},
        subs={"g_motivo": "Minutos por motivo", "g_celula": "Minutos por célula"}),
}

# cores por serie (so formatacao; as series ja existem na consulta)
VERM, GRAF = "#E2000F", "#3C3C3B"
SERIES = {
    ("pg_horahora", "g_prod_hora"): {"Medidas.HH Real (m)": (VERM, False), "Medidas.HH Meta (m)": (GRAF, True)},
    ("pg_refugo_ppm", "g_ppm_mes"): {"Medidas.Refugo PPM": (VERM, False), "Medidas.Meta Refugo PPM": (GRAF, True)},
    ("pg_paradas", "g_pareto"): {"Medidas.PA Tempo Parado (h)": (VERM, False),
                                 "Medidas.PA % Acumulado Paradas": (GRAF, False)},
    ("pg_paradas", "g_pareto_ref"): {"Medidas.Refugo (m)": (VERM, False), "Medidas.% Acumulado Refugo": (GRAF, False)},
    ("pg_refugo_ppm", "g_causa"): {"Medidas.Refugo (m)": (VERM, False), "Medidas.% Acumulado Refugo": (GRAF, False)},
}
# ThemeDataColor: indices da paleta antiga -> indice equivalente na paleta nova (mesma cor, ou a mais proxima)
REMAP_COR = {0: 0, 1: 1, 2: 4, 3: 2, 4: 2, 5: 7, 6: 5, 7: 6}


# ------------------------------------------------------------------ menu, cabecalho
def textbox(nome, x, y, w, h, z, texto, tam, cor_txt, fonte, alt_txt):
    d = vin(VG, "titulo")
    d["name"] = nome
    pos(d, x, y, w, h, z)
    d["visual"]["objects"]["general"][0]["properties"]["paragraphs"] = [{"textRuns": [{
        "value": texto, "textStyle": {"fontSize": f"{fmt(F(tam))}pt", "color": cor_txt, "fontFamily": fonte}}]}]
    d["visual"]["visualContainerObjects"] = {**sem_titulo(), **alt(alt_txt)}
    return d


def estilo_botao(d, ativo):
    o = d["visual"]["objects"]
    texto = o["text"][1]["properties"]
    texto.update({"fontColor": cor("#FFFFFF" if ativo else "#BDBDBD"), "fontSize": lit(fmt(F(13)) + "D"),
                  "bold": lit("true" if ativo else "false"),
                  "horizontalAlignment": s("Left"), "leftMargin": lit("19L")})
    if ativo:
        o["fill"] = [{"properties": {"show": lit("true")}},
                     {"properties": {"fillColor": cor("#2A2A2A"), "transparency": lit("0D")},
                      "selector": {"id": "default"}}]
    else:
        o["fill"] = [{"properties": {"show": lit("false")}}]
    o["outline"] = [{"properties": {"show": lit("false")}}]
    o["shape"] = [{"properties": {"roundEdge": lit("0L")}, "selector": {"id": "default"}}]


def botao(nome, ativo_nome, y, z):
    origem = "pg_producao_montagem" if nome in ROTULO_MONT else VG
    d = vin(origem, nome)
    vco = d["visual"]["visualContainerObjects"]
    assert vco["visualLink"][0]["properties"]["navigationSection"] == s(DESTINO[nome]), nome
    texto = ROTULO_MONT.get(nome) or valor(d["visual"]["objects"]["text"][1]["properties"]["text"])
    d["visual"]["objects"]["text"][1]["properties"]["text"] = s(texto)
    pos(d, 0, y, 200, H, z)
    estilo_botao(d, nome == ativo_nome)
    if nome == ativo_nome:
        vco["general"] = [{"properties": {"altText": s("Página atual: " + texto)}}]
    else:
        sufixo = " (Montagem)" if nome in ROTULO_MONT else ""
        vco["general"] = [{"properties": {"altText": s("Ir para a página " + texto + sufixo)}}]
    return d


def menu(pg, out):
    """Menu lateral igual ao da Visao Geral; devolve o nome do botao ativo."""
    ativo = ATIVO[pg]
    d = vin(VG, "faixa")
    pos(d, 0, 0, 200, 720, 0)
    d["visual"]["objects"]["fill"][0]["properties"]["fillColor"] = cor("#1E1E1E")
    d["visual"]["visualContainerObjects"] = {**alt("Fundo do menu lateral."), **sem_titulo()}
    out("faixa", d)
    d = vin(VG, "logo")
    pos(d, 16, 16, 168, 40, 100)
    vco = d["visual"]["visualContainerObjects"]
    vco["background"] = [{"properties": {"show": lit("true"), "color": cor("#FFFFFF"), "transparency": lit("0D")}}]
    vco["general"] = [{"properties": {"keepLayerOrder": lit("true"), "altText": s("Logotipo Danfoss")}}]
    out("logo", d)
    out("txt_app", textbox("txt_app", 16, 58, 168, 18, 110, "GMS · Guaratinguetá", 11, "#7A7A7A", REG,
                           "Nome do sistema e da unidade."))
    out("txt_secao_mangueira", textbox("txt_secao_mangueira", 16, 86, 168, 18, 120, "MANGUEIRA", 10, "#7A7A7A", SEMI,
                                       "Seção Mangueira do menu."))
    out("txt_secao_montagem", textbox("txt_secao_montagem", 16, Y_MONT, 168, 18, 130, "MONTAGEM", 10, "#7A7A7A", SEMI,
                                      "Seção Montagem do menu."))
    ys = {}
    for i, nome in enumerate(ORDEM):
        ys[nome] = Y0 + i * H
        out(nome, botao(nome, ativo, ys[nome], 200 + i * 10))
    ys["sub_producao_montagem"] = Y_MONT + 20
    ys["sub_paradas_montagem"] = Y_MONT + 20 + H
    out("sub_producao_montagem", botao("sub_producao_montagem", ativo, ys["sub_producao_montagem"], 280))
    out("sub_paradas_montagem", botao("sub_paradas_montagem", ativo, ys["sub_paradas_montagem"], 290))
    d = vin(VG, "faixa")
    d["name"] = "nav_barra_ativa"
    pos(d, 0, ys[ativo], 3, H, 300)
    d["visual"]["objects"]["fill"][0]["properties"]["fillColor"] = cor("#E2000F")
    d["visual"]["visualContainerObjects"] = {**alt("Marca a página atual no menu."), **sem_titulo()}
    out("nav_barra_ativa", d)
    return ativo


def atualizado(pg, out):
    d = vin(pg, "atualizado")
    pos(d, 16, 652, 168, 52, 400)
    o = d["visual"].setdefault("objects", {})
    o["labels"] = [{"properties": {"fontSize": lit(fmt(F(12)) + "D"), "color": cor("#BDBDBD"), "bold": lit("false")}}]
    o["categoryLabels"] = [{"properties": {"show": lit("true"), "fontSize": lit(fmt(F(11)) + "D"),
                                           "color": cor("#7A7A7A")}}]
    d["visual"]["visualContainerObjects"] = {
        **sem_titulo(),
        "background": [{"properties": {"show": lit("false")}}],
        "border": [{"properties": {"show": lit("false")}}],
        "padding": [{"properties": {"top": lit("0D"), "bottom": lit("0D"), "left": lit("0D"), "right": lit("0D")}}],
        **alt("Data e hora da última atualização dos dados."),
    }
    out("atualizado", d)


# ------------------------------------------------------------------ filtros
def nome_filtro(d):
    vco = d["visual"]["visualContainerObjects"]
    t = vco.get("title", [{}])[0].get("properties", {}).get("text")
    if t:
        return valor(t)
    return valor(d["visual"]["objects"]["header"][0]["properties"]["text"])


def filtros(pg, out):
    """Todos os slicers no cabecalho, alinhados a direita. Devolve x do primeiro filtro (ou 1264)."""
    nomes = [n for n in os.listdir(os.path.join(VIG, pg, "visuals"))
             if vin(pg, n)["visual"]["visualType"] == "slicer"]
    info = []
    for n in nomes:
        d = vin(pg, n)
        info.append((nome_filtro(d) == "Período", d["position"]["x"], n, d))
    info.sort(key=lambda t: (t[0], t[1]))
    k = len(info)
    wp = 248 if k < 4 else 200
    wo = 144 if k >= 4 else 160
    larg = [(wp if p else wo) for p, _, _, _ in info]
    x = 1264 - (sum(larg) + 8 * (k - 1))
    x_ini = x
    for i, (_, _, n, d) in enumerate(info):
        pos(d, x, 12, larg[i], 56, 30000 + i * 100)
        vco = d["visual"]["visualContainerObjects"]
        o = d["visual"].setdefault("objects", {})
        t = vco.get("title", [{"properties": {}}])[0]["properties"]
        if "text" in t and valor(t.get("show", lit("true"))) == "true":
            texto = t["text"]
        else:                                  # fluxo: o texto estava no cabecalho interno do slicer
            texto = o["header"][0]["properties"]["text"]
        vco["title"] = [{"properties": {"show": lit("true"), "text": texto}}]
        o["header"] = [{"properties": {"show": lit("false")}}]
        o["items"] = [{"properties": {}}]
        for k2 in ("background", "border", "dropShadow", "padding"):
            vco.pop(k2, None)
        out(n, d)
        x += larg[i] + 8
    return x_ini


def cabecalho(pg, out, x_filtros):
    w = min(600, int(x_filtros - 8 - 216))
    assert w >= 380, (pg, w)
    out("titulo", textbox("titulo", 216, 12, w, 32, 1000, CFG[pg]["titulo"], 22, "#1F1F1E", SEMI,
                          "Título da página: " + CFG[pg]["titulo"] + "."))
    out("txt_subtitulo", textbox("txt_subtitulo", 216, 44, w, 20, 1010, CFG[pg]["sub"], 12, "#5F6368", REG,
                                 "Subtítulo: " + CFG[pg]["sub"] + "."))


# ------------------------------------------------------------------ KPIs
def kpis(pg, out):
    nomes = sorted(n for n in os.listdir(os.path.join(VIG, pg, "visuals")) if re.fullmatch(r"kpi\d+", n))
    n = len(nomes)
    if n == 0:
        return
    w = round((1048 - 16 * (n - 1)) / n, 2)
    for i, nome in enumerate(nomes):
        v = vin(pg, nome)
        proj = copy.deepcopy(v["visual"]["query"]["queryState"]["Values"]["projections"][0])
        vco = v["visual"]["visualContainerObjects"]
        titulo = valor(vco["title"][0]["properties"]["text"])
        proj["displayName"] = titulo.upper()
        alt_txt = valor(vco["general"][0]["properties"]["altText"])
        objs = {}
        if os.path.exists(os.path.join(VIG, pg, "visuals", nome + "_d")):
            dlt = vin(pg, nome + "_d")
            f = dlt["visual"]["query"]["queryState"]["Values"]["projections"][0]["field"]
            objs["referenceLabel"] = [{"properties": {"value": {"expr": f}}, "selector": {"id": "ref0"}}]
            alt_txt += " " + valor(dlt["visual"]["visualContainerObjects"]["general"][0]["properties"]["altText"])
        novo = {
            "$schema": v["$schema"], "name": nome,
            "position": {"x": round(216 + i * (w + 16), 2), "y": 88, "z": 8000 + i * 100, "height": 104,
                         "width": w, "tabOrder": 8000 + i * 100},
            "visual": {
                "visualType": "cardVisual",
                "query": {"queryState": {"Data": {"projections": [proj]}}},
                "objects": objs,
                "visualContainerObjects": {
                    **sem_titulo(),
                    "padding": [{"properties": {"top": lit("0D"), "bottom": lit("0D"), "left": lit("0D"),
                                                "right": lit("0D")}}],
                    **alt(alt_txt),
                },
                "drillFilterOtherVisuals": True,
            },
        }
        if not objs:
            del novo["visual"]["objects"]
        out(nome, novo)


def kpis_fluxo(out):
    """Fluxo_1: cardVisual de 9 tiles na faixa de KPI, com 1048 de largura."""
    d = vin("pg_fluxo_1", "kpis")
    pos(d, 216, 88, 1048, 104, 8000)
    o = d["visual"]["objects"]
    px = {20: 15, 16: 12, 12: 9}
    o["layout"] = [{"properties": {"maxTiles": lit("9L")}},
                   {"properties": {"cellPadding": lit("0L"), "paddingUniform": lit("8L"),
                                   "backgroundShow": lit("false")}, "selector": {"id": "default"}}]
    for it in o["value"]:
        p = it["properties"]
        p["fontSize"] = lit(fmt(px[int(valor(p["fontSize"]).rstrip("D"))]) + "D")
        if "fontColor" in p:
            p["fontColor"] = cor("#1F1F1E")
    for it in o["label"]:
        p = it["properties"]
        p["fontSize"] = lit(fmt(px[int(valor(p["fontSize"]).rstrip("D"))]) + "D")
        p["fontColor"] = cor("#5F6368")
    o.pop("outline", None)
    d["visual"]["visualContainerObjects"] = {
        **sem_titulo(),
        "padding": [{"properties": {"top": lit("0D"), "bottom": lit("0D"), "left": lit("0D"), "right": lit("0D")}}],
        "general": d["visual"]["visualContainerObjects"]["general"],
    }
    out("kpis", d)


# ------------------------------------------------------------------ graficos
def limpa_container(d, subtitulo):
    vco = d["visual"]["visualContainerObjects"]
    t = vco["title"][0]["properties"]
    vco["title"] = [{"properties": {"show": t["show"], "text": t["text"]}}]
    if "subTitle" in vco and "text" in vco["subTitle"][0]["properties"]:
        st = vco["subTitle"][0]["properties"]
        vco["subTitle"] = [{"properties": {"show": st["show"], "text": st["text"]}}]   # subtitulo por medida: mantem
    else:
        vco["subTitle"] = [{"properties": {"show": lit("true"), "text": s(subtitulo)}}]
    for k in ("background", "border", "dropShadow", "padding"):
        vco.pop(k, None)


def limpa_objetos(o):
    for k in ("categoryAxis", "valueAxis"):
        if k not in o:
            continue
        for it in o[k]:
            for p in ("fontSize", "labelColor", "gridlineColor", "fontFamily"):
                it["properties"].pop(p, None)
        o[k] = [it for it in o[k] if it["properties"] or "selector" in it]
        if not o[k]:
            del o[k]
    if "labels" in o:
        novos = []
        for it in o["labels"]:
            for p in ("fontSize", "color", "fontFamily"):
                it["properties"].pop(p, None)
            novos.append(it)
        o["labels"] = novos
    if "legend" in o:
        o["legend"] = [{"properties": {"show": o["legend"][0]["properties"]["show"]}}]
    if "lineStyles" in o:
        for it in o["lineStyles"]:
            it["properties"].pop("strokeWidth", None)
        o["lineStyles"] = [it for it in o["lineStyles"] if it["properties"]]
        if not o["lineStyles"]:
            del o["lineStyles"]
    for it in o.get("dataPoint", []):            # paleta nova: mantem a cor equivalente
        fill = it["properties"].get("fill")
        try:
            tc = fill["solid"]["color"]["expr"]["ThemeDataColor"]
            tc["ColorId"] = REMAP_COR[tc["ColorId"]]
        except (KeyError, TypeError):
            pass


def graficos(pg, out, destino_pos):
    for nome, (x, y, w, h) in CFG[pg]["corpo"].items():
        if nome == "dia_produtivo":
            continue
        d = vin(pg, nome)
        pos(d, x, y, w, h, destino_pos[nome])
        limpa_container(d, CFG[pg]["subs"][nome])
        o = d["visual"]["objects"]
        limpa_objetos(o)
        cores = SERIES.get((pg, nome))
        if cores:
            o["dataPoint"] = [{"properties": {"fill": cor(c)}, "selector": {"metadata": ref}}
                              for ref, (c, _) in cores.items()]
            tracejadas = [ref for ref, (_, tr) in cores.items() if tr]
            if tracejadas:
                o["lineStyles"] = [{"properties": {"lineStyle": s("dashed")}, "selector": {"metadata": ref}}
                                   for ref in tracejadas]
        out(nome, d)
    if "dia_produtivo" in CFG[pg]["corpo"]:
        x, y, w, h = CFG[pg]["corpo"]["dia_produtivo"]
        d = vin(pg, "dia_produtivo")
        pos(d, x, y, w, h, 14900)
        d["visual"]["objects"]["labels"] = [{"properties": {"fontSize": lit(fmt(F(12)) + "D"),
                                                            "color": cor("#5F6368"), "bold": lit("false")}}]
        vco = d["visual"]["visualContainerObjects"]
        vco["background"] = [{"properties": {"show": lit("false")}}]
        out("dia_produtivo", d)


def fluxo_corpo(pg, out):
    if pg == "pg_fluxo_1":
        for i in range(8):
            nome = f"cartao_{i + 1}"
            d = vin(pg, nome)
            pos(d, 216 + (i % 4) * 266, 208 + (i // 4) * 184, 250, 168, 14000 + i * 100)   # 303x205 -> 250x168 (proporção mantida)
            out(nome, d)
        d = vin(pg, "legenda")
        pos(d, 216, 576, 1048, 48, 15000)
        for par in d["visual"]["objects"]["general"][0]["properties"]["paragraphs"]:
            for run in par["textRuns"]:
                if "textStyle" in run:
                    run["textStyle"].update({"fontSize": fmt(F(12)) + "pt", "color": "#5F6368"})
        out("legenda", d)
    else:
        d = vin(pg, "t_conteudo")
        pos(d, 216, 88, 1048, 278, 14000)                                                  # 1280x340 -> 1048x278 (proporção mantida)
        out("t_conteudo", d)
    for nome, (x, w) in (("rodape", (216, 520)), ("subtitulo", (744, 520))):
        d = vin(pg, nome)
        pos(d, x, 672, w, 32, 15100 if nome == "rodape" else 15200)
        out(nome, d)


# ------------------------------------------------------------------ pagina
def construir(pg):
    pasta = os.path.join(NOVO, pg)
    vdir = os.path.join(pasta, "visuals")
    for n in os.listdir(vdir):
        shutil.rmtree(os.path.join(vdir, n))
    escritos = []

    def out(nome, d):
        escritos.append(nome)
        wj(os.path.join(vdir, nome, "visual.json"), d)

    menu(pg, out)
    atualizado(pg, out)
    x_filtros = filtros(pg, out)
    cabecalho(pg, out, x_filtros)
    if pg == "pg_fluxo_1":
        kpis_fluxo(out)
        fluxo_corpo(pg, out)
    elif pg == "pg_fluxo_2":
        fluxo_corpo(pg, out)
        graficos(pg, out, {"g_metros": 14100, "g_pessoas": 14200})
    else:
        kpis(pg, out)
        graficos(pg, out, {n: 14000 + i * 100 for i, n in enumerate(CFG[pg]["corpo"])})
    # layout mobile (so posicao): copia como esta
    for n in os.listdir(os.path.join(VIG, pg, "visuals")):
        m = os.path.join(VIG, pg, "visuals", n, "mobile.json")
        if os.path.exists(m) and n in escritos:
            shutil.copyfile(m, os.path.join(vdir, n, "mobile.json"))
    # fundo da pagina
    pj = lj(os.path.join(VIG, pg, "page.json"))
    pj["objects"]["background"][0]["properties"]["color"] = cor("#F2F3F5")
    wj(os.path.join(pasta, "page.json"), pj)
    return sorted(escritos)


if __name__ == "__main__":
    for pg in CFG:
        e = construir(pg)
        print(pg, len(e), "visuais")
