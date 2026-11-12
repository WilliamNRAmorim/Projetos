"""Piloto do redesign: reconstroi pg_visao_geral na copia a partir da vigente (idempotente).
Le GMS_Painel.Report (vigente, so leitura) e grava em Painel_Redesign/GMS_Painel.Report."""
import json, os, copy, shutil

AQUI = os.path.dirname(os.path.abspath(__file__))
VIG = os.path.join(AQUI, "..", "GMS_Painel.Report", "definition", "pages")
NOVO = os.path.join(AQUI, "GMS_Painel.Report", "definition", "pages")
PG = "pg_visao_geral"
SCHEMA = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.14.0/schema.json"


def lj(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def wj(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)


def F(px):
    """px do prototipo -> pt do Power BI (x0,75, passo de 0,5 pt)."""
    return {10: 7.5, 11: 8, 12: 9, 13: 10, 22: 16.5}[px]


def fmt(x):
    return str(int(x)) if x == int(x) else str(x)


def lit(v):
    return {"expr": {"Literal": {"Value": v}}}


def s(txt):
    return lit("'" + txt.replace("'", "''") + "'")


def cor(h):
    return {"solid": {"color": s(h)}}


def vis_in(nome):
    return lj(os.path.join(VIG, PG, "visuals", nome, "visual.json"))


def vis_out(nome, d):
    wj(os.path.join(NOVO, PG, "visuals", nome, "visual.json"), d)


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


# ---------------------------------------------------------------- limpeza
vis_dir = os.path.join(NOVO, PG, "visuals")
for n in os.listdir(vis_dir):          # recomeca a pagina a partir da vigente
    shutil.rmtree(os.path.join(vis_dir, n))

# ---------------------------------------------------------------- fundo do menu
d = vis_in("faixa")
pos(d, 0, 0, 200, 720, 0)
d["visual"]["objects"]["fill"][0]["properties"]["fillColor"] = cor("#1E1E1E")
d["visual"]["visualContainerObjects"] = {**alt("Fundo do menu lateral."), **sem_titulo()}
vis_out("faixa", d)

# ---------------------------------------------------------------- logo
d = vis_in("logo")
pos(d, 16, 16, 168, 40, 100)
vco = d["visual"]["visualContainerObjects"]
vco["background"] = [{"properties": {"show": lit("true"), "color": cor("#FFFFFF"), "transparency": lit("0D")}}]
vco["general"] = [{"properties": {"keepLayerOrder": lit("true"), "altText": s("Logotipo Danfoss")}}]
vis_out("logo", d)

SEMI, REG = "Segoe UI Semibold", "Segoe UI"


# ---------------------------------------------------------------- textbox (modelo: titulo da vigente)
def textbox(nome, x, y, w, h, z, texto, tam, cor_txt, fonte, alt_txt):
    d = vis_in("titulo")
    d["name"] = nome
    pos(d, x, y, w, h, z)
    d["visual"]["objects"]["general"][0]["properties"]["paragraphs"] = [{"textRuns": [{
        "value": texto,
        "textStyle": {"fontSize": f"{fmt(F(tam))}pt", "color": cor_txt, "fontFamily": fonte}}]}]
    d["visual"]["visualContainerObjects"] = {**sem_titulo(), **alt(alt_txt)}
    return d


vis_out("txt_app", textbox("txt_app", 16, 58, 168, 18, 110, "GMS · Guaratinguetá", 11, "#7A7A7A", REG,
                           "Nome do sistema e da unidade."))
vis_out("txt_secao_mangueira", textbox("txt_secao_mangueira", 16, 86, 168, 18, 120, "MANGUEIRA", 10, "#7A7A7A", SEMI,
                                       "Seção Mangueira do menu."))
Y0, H = 106, 32
y_mont = Y0 + 8 * H + 16            # 378
vis_out("txt_secao_montagem", textbox("txt_secao_montagem", 16, y_mont, 168, 18, 130, "MONTAGEM", 10, "#7A7A7A", SEMI,
                                      "Seção Montagem do menu."))

# cabecalho (largura 476 em vez de 600 para nao encostar no filtro Maquina, que comeca em x=700)
vis_out("titulo", textbox("titulo", 216, 12, 476, 32, 1000, "Visão Geral da Produção", 22, "#1F1F1E", SEMI,
                          "Título da página: Visão Geral da Produção."))
vis_out("txt_subtitulo", textbox("txt_subtitulo", 216, 44, 476, 20, 1010,
                                 "Trançagem · metros, meta e paradas por máquina", 12, "#5F6368", REG,
                                 "Subtítulo: recorte da página."))

# ---------------------------------------------------------------- itens do menu
ordem = ["sub_visao_geral", "sub_horahora", "sub_paradas", "sub_refugo_ppm", "sub_refugo_ppm_cortes",
         "sub_extrusora", "sub_fluxo_1", "sub_fluxo_2"]


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


for i, nome in enumerate(ordem):
    d = vis_in(nome)
    pos(d, 0, Y0 + i * H, 200, H, 200 + i * 10)
    estilo_botao(d, nome == "sub_visao_geral")
    vis_out(nome, d)


# botoes de Montagem: estrutura copiada dos botoes de navegacao da pagina de Montagem
def botao_montagem(nome, texto, destino, y, z):
    d = lj(os.path.join(VIG, "pg_producao_montagem", "visuals", nome, "visual.json"))
    pos(d, 0, y, 200, H, z)
    d["visual"]["objects"]["text"][1]["properties"]["text"] = s(texto)
    estilo_botao(d, False)
    vco = d["visual"]["visualContainerObjects"]
    assert vco["visualLink"][0]["properties"]["navigationSection"] == s(destino)
    vco["general"] = [{"properties": {"altText": s("Ir para a página " + texto + " (Montagem)")}}]
    return d


vis_out("sub_producao_montagem", botao_montagem("sub_producao_montagem", "Produção", "pg_producao_montagem",
                                                y_mont + 20, 280))
vis_out("sub_paradas_montagem", botao_montagem("sub_paradas_montagem", "Paradas", "pg_paradas_montagem",
                                               y_mont + 20 + H, 290))

# barra vermelha do item ativo (forma nova, modelo: faixa)
d = vis_in("faixa")
d["name"] = "nav_barra_ativa"
pos(d, 0, Y0, 3, H, 300)
d["visual"]["objects"]["fill"][0]["properties"]["fillColor"] = cor("#E2000F")
d["visual"]["visualContainerObjects"] = {**alt("Marca a página atual no menu."), **sem_titulo()}
vis_out("nav_barra_ativa", d)

# ---------------------------------------------------------------- atualizado
d = vis_in("atualizado")
pos(d, 16, 652, 168, 52, 400)
o = d["visual"]["objects"]
o["labels"] = [{"properties": {"fontSize": lit(fmt(F(12)) + "D"), "color": cor("#BDBDBD"), "bold": lit("false")}}]
o["categoryLabels"] = [{"properties": {"show": lit("true"), "fontSize": lit(fmt(F(11)) + "D"), "color": cor("#7A7A7A")}}]
d["visual"]["visualContainerObjects"] = {
    **sem_titulo(),
    "background": [{"properties": {"show": lit("false")}}],
    "border": [{"properties": {"show": lit("false")}}],
    "padding": [{"properties": {"top": lit("0D"), "bottom": lit("0D"), "left": lit("0D"), "right": lit("0D")}}],
    **alt("Data e hora da última atualização dos dados."),
}
vis_out("atualizado", d)


# ---------------------------------------------------------------- filtros
def slicer(nome, x, w, z):
    d = vis_in(nome)
    pos(d, x, 12, w, 56, z)
    vco = d["visual"]["visualContainerObjects"]
    t = vco["title"][0]["properties"]       # fica so o conteudo; o resto vem do tema
    vco["title"] = [{"properties": {"show": t["show"], "text": t["text"]}}]
    for k in ("background", "border", "dropShadow", "padding"):
        vco.pop(k, None)
    return d


vis_out("747140ef9b591b54b318", slicer("747140ef9b591b54b318", 700, 160, 17000))
vis_out("seg1", slicer("seg1", 868, 140, 17100))
vis_out("seg0", slicer("seg0", 1016, 248, 17200))

# ---------------------------------------------------------------- KPIs (card -> cardVisual)
CARD_X = [216, 482, 748, 1014]
for i in range(4):
    nome = f"kpi{i}"
    v = vis_in(nome)
    q = v["visual"]["query"]["queryState"]["Values"]["projections"]
    assert len(q) == 1
    proj = copy.deepcopy(q[0])
    vco = v["visual"]["visualContainerObjects"]
    titulo = vco["title"][0]["properties"]["text"]["expr"]["Literal"]["Value"].strip("'")
    proj["displayName"] = titulo.upper()
    sub_expr = vco["subTitle"][0]["properties"]["text"]["expr"]
    cor_expr = vco["border"][0]["properties"]["color"]["solid"]["color"]["expr"]
    alt_txt = vco["general"][0]["properties"]["altText"]["expr"]["Literal"]["Value"].strip("'")
    novo = {
        "$schema": SCHEMA,
        "name": nome,
        "position": {"x": CARD_X[i], "y": 88, "z": v["position"]["z"], "height": 104, "width": 250,
                     "tabOrder": v["position"]["tabOrder"]},
        "visual": {
            "visualType": "cardVisual",
            "query": {"queryState": {"Data": {"projections": [proj]}}},
            "objects": {
                "accentBar": [{"properties": {"color": {"solid": {"color": {"expr": cor_expr}}}},
                               "selector": {"id": "default"}}],
                "referenceLabel": [{"properties": {"value": {"expr": sub_expr}},
                                    "selector": {"id": "ref0"}}],
            },
            "visualContainerObjects": {
                **sem_titulo(),
                "padding": [{"properties": {"top": lit("0D"), "bottom": lit("0D"), "left": lit("0D"),
                                            "right": lit("0D")}}],
                **alt(alt_txt),
            },
            "drillFilterOtherVisuals": True,
        },
    }
    vis_out(nome, novo)


# ---------------------------------------------------------------- graficos
def limpa_container(d, subtitulo=None):
    vco = d["visual"]["visualContainerObjects"]
    t = vco["title"][0]["properties"]
    vco["title"] = [{"properties": {"show": t["show"], "text": t["text"]}}]
    if subtitulo is not None:
        vco["subTitle"] = [{"properties": {"show": lit("true"), "text": subtitulo}}]
    elif "subTitle" in vco:
        st = vco["subTitle"][0]["properties"]
        vco["subTitle"] = [{"properties": {"show": st["show"], "text": st["text"]}}]
    for k in ("background", "border", "dropShadow", "padding"):
        vco.pop(k, None)


def sem_formatacao_literal(o):
    for k in ("categoryAxis", "valueAxis"):
        props = o.get(k, [{"properties": {}}])[0]["properties"]
        keep = {p: v for p, v in props.items() if p not in ("fontSize", "labelColor", "gridlineColor")}
        if keep:
            o[k] = [{"properties": keep}]
        else:
            o.pop(k, None)
    o["labels"] = [{"properties": {"show": o["labels"][0]["properties"]["show"]}}]
    o["legend"] = [{"properties": {"show": o["legend"][0]["properties"]["show"]}}]


# g_maquina: mantem o subtitulo por medida (VG Pior Máquina)
d = vis_in("g_maquina")
pos(d, 216, 208, 600, 496, 14000)
limpa_container(d)
o = d["visual"]["objects"]
sem_formatacao_literal(o)
for dp in o["dataPoint"]:
    if dp["selector"].get("metadata") == "Medidas.HH Meta Útil (m)":
        dp["properties"]["fill"] = cor("#D5D8DD")
o["layout"] = [{"properties": {"clusteredGapOverlaps": lit("true"), "clusteredGapOverlapReverse": lit("true")}}]
vis_out("g_maquina", d)

d = vis_in("g_motivo")
pos(d, 832, 208, 432, 240, 15000)
limpa_container(d, s("Minutos parados"))
sem_formatacao_literal(d["visual"]["objects"])
vis_out("g_motivo", d)

d = vis_in("g_dia")
pos(d, 832, 464, 432, 240, 16000)
limpa_container(d, s("Metros por hora cheia"))
o = d["visual"]["objects"]
sem_formatacao_literal(o)
real, meta = "Medidas.HH Real (m)", "Medidas.HH Meta (m)"
o["dataPoint"] = [{"properties": {"fill": cor("#E2000F")}, "selector": {"metadata": real}},
                  {"properties": {"fill": cor("#3C3C3B")}, "selector": {"metadata": meta}}]
o["lineStyles"] = [{"properties": {"strokeWidth": lit("2D")}, "selector": {"metadata": real}},
                   {"properties": {"strokeWidth": lit("2D"), "lineStyle": s("dashed")}, "selector": {"metadata": meta}}]
vis_out("g_dia", d)

# ---------------------------------------------------------------- layout mobile (so posicao): copia como esta
for n in os.listdir(os.path.join(VIG, PG, "visuals")):
    m = os.path.join(VIG, PG, "visuals", n, "mobile.json")
    if os.path.exists(m) and os.path.isdir(os.path.join(vis_dir, n)):
        shutil.copyfile(m, os.path.join(vis_dir, n, "mobile.json"))

# ---------------------------------------------------------------- pagina
pj = lj(os.path.join(VIG, PG, "page.json"))
pj["objects"]["background"][0]["properties"]["color"] = cor("#F2F3F5")
wj(os.path.join(NOVO, PG, "page.json"), pj)
print("ok", sorted(os.listdir(vis_dir)))
