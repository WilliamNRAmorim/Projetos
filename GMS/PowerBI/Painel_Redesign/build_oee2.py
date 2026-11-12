"""MEL-266, passo 3: página pg_oee2 "OEE2 Trançagem" no GMS_Painel.Report (vigente, já no layout novo) e o item "OEE2"
no menu Mangueira das 11 páginas (idempotente: rodar de novo dá o mesmo resultado).

O que grava, todos em GMS/PowerBI/GMS_Painel.Report/definition/pages:
  - pg_oee2/ (page.json e visuals/*): menu, cabeçalho, 3 slicers (os da pg_horahora, mesmo syncGroup), 5 cartões, cascata,
    Pareto por categoria, matriz máquina x turno, linha por dia e rodapé;
  - nas 10 páginas antigas: só o menu. Entra o botão sub_oee2 logo depois de "Hora-Hora" (y = 170) e tudo que estava
    abaixo desce 32 px (botões, o título MONTAGEM e a barra vermelha da página atual). Nada mais muda;
  - pages.json: pg_oee2 entra depois da pg_horahora.
As medidas usadas (pasta OEE2 do modelo, GMS/PowerBI/modelo/oee2.tmdl.md) ainda não existem no modelo vivo: a página só
abre sem erro depois que o William aplicar o script do modelo e reabrir o projeto. Não há medida de relatório nova.
Usa as funções de build_paginas.py (mesmo padrão de cores, tipografia e posições do redesign)."""
import copy
import json
import os
import shutil
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import build_paginas as bp  # noqa: E402  (só importa; o main dele não roda)

lit, s, cor, pos, alt, fmt, F, SEMI, REG = bp.lit, bp.s, bp.cor, bp.pos, bp.alt, bp.fmt, bp.F, bp.SEMI, bp.REG
PAGES = bp.VIG                                   # .../GMS_Painel.Report/definition/pages (vigente)
PG = "pg_oee2"
TITULO = "OEE2 Trançagem"
SUBTITULO = "OEE2 (apontamento) · padrão Danfoss/Factbird · sem sensor"
H, Y0 = bp.H, bp.Y0
SCHEMA = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.14.0/schema.json"

# ------------------------------------------------------------------ menu: 9 itens em Mangueira, 2 em Montagem
ORDEM = ["sub_visao_geral", "sub_horahora", "sub_oee2", "sub_paradas", "sub_refugo_ppm", "sub_refugo_ppm_cortes",
         "sub_extrusora", "sub_fluxo_1", "sub_fluxo_2"]
DESTINO = {**bp.DESTINO, "sub_oee2": PG}
ATIVO = {v: k for k, v in DESTINO.items()}
Y_MONT = Y0 + len(ORDEM) * H + 16                # 410
NOVO_Y = {n: Y0 + i * H for i, n in enumerate(ORDEM)}
NOVO_Y.update({"txt_secao_montagem": Y_MONT, "sub_producao_montagem": Y_MONT + 20, "sub_paradas_montagem": Y_MONT + 20 + H})
# posições de antes do OEE2 (menu de 8 itens em Mangueira): serve para conferir o estado de partida e rodar de novo sem somar 32 duas vezes
ANTIGO_Y = {n: (y - H if y >= NOVO_Y["sub_paradas"] else y) for n, y in NOVO_Y.items() if n != "sub_oee2"}
Z_OEE2 = 215                                     # entre sub_horahora (210) e sub_paradas (220)


# ------------------------------------------------------------------ arquivos (CRLF, sem quebra no fim, como o Desktop grava)
def ler(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def bytes_json(d):
    return json.dumps(d, ensure_ascii=False, indent=2).replace("\n", "\r\n").encode("utf-8")


def gravar(p, d):
    """Grava só se mudou. Devolve True se escreveu."""
    novo = bytes_json(d)
    if os.path.exists(p):
        with open(p, "rb") as f:
            if f.read() == novo:
                return False
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "wb") as f:
        f.write(novo)
    return True


def vis_path(pg, nome):
    return os.path.join(PAGES, pg, "visuals", nome, "visual.json")


# ------------------------------------------------------------------ menu das 10 páginas antigas
def texto_botao(d):
    return bp.valor(d["visual"]["objects"]["text"][1]["properties"]["text"])


def botao_oee2_a_partir_de(pg):
    """Clona um botão inativo da própria página e transforma no item OEE2."""
    origem = "sub_visao_geral" if ATIVO.get(pg) != "sub_visao_geral" else "sub_paradas"
    d = copy.deepcopy(ler(vis_path(pg, origem)))
    d["name"] = "sub_oee2"
    pos(d, 0, NOVO_Y["sub_oee2"], 200, H, Z_OEE2)
    d["visual"]["objects"]["text"][1]["properties"]["text"] = s("OEE2")
    vco = d["visual"]["visualContainerObjects"]
    vco["visualLink"][0]["properties"]["navigationSection"] = s(PG)
    vco["general"] = [{"properties": {"altText": s("Ir para a página OEE2")}}]
    return d


def atualiza_menu(pg, relatorio):
    ativo = ATIVO[pg]
    nomes = set(os.listdir(os.path.join(PAGES, pg, "visuals")))
    for nome, y in NOVO_Y.items():
        if nome == "sub_oee2":
            continue
        d = ler(vis_path(pg, nome))
        atual = d["position"]["y"]
        assert atual in (y, ANTIGO_Y[nome]), f"{pg}/{nome}: y={atual}, esperava {ANTIGO_Y[nome]} ou {y}"
        d["position"]["y"] = y
        if gravar(vis_path(pg, nome), d):
            relatorio.append(f"{pg}/{nome} y {atual}->{y}")
    d = ler(vis_path(pg, "nav_barra_ativa"))
    y = NOVO_Y[ativo]
    assert d["position"]["y"] in (y, ANTIGO_Y[ativo]), f"{pg}/nav_barra_ativa y={d['position']['y']}"
    d["position"]["y"] = y
    if gravar(vis_path(pg, "nav_barra_ativa"), d):
        relatorio.append(f"{pg}/nav_barra_ativa y->{y}")
    if gravar(vis_path(pg, "sub_oee2"), botao_oee2_a_partir_de(pg)):
        relatorio.append(f"{pg}/sub_oee2 {'novo' if 'sub_oee2' not in nomes else 'atualizado'}")


# ------------------------------------------------------------------ campos e containers
def c_col(ent, prop):
    return {"Column": {"Expression": {"SourceRef": {"Entity": ent}}, "Property": prop}}


def c_med(prop):
    """Medida do MODELO (tabela Medidas, pasta OEE2): sem Schema "extension" (esse é só das medidas de relatório)."""
    return {"Measure": {"Expression": {"SourceRef": {"Entity": "Medidas"}}, "Property": prop}}


def proj(campo, ativo=False, nome=None):
    k = "Column" if "Column" in campo else "Measure"
    ent = campo[k]["Expression"]["SourceRef"]["Entity"]
    prop = campo[k]["Property"]
    p = {"field": campo, "queryRef": f"{ent}.{prop}", "nativeQueryRef": prop}
    if ativo:
        p["active"] = True
    if nome:
        p["displayName"] = nome
    return p


def container(titulo, subtitulo, alt_txt):
    return {"title": [{"properties": {"show": lit("true"), "text": s(titulo)}}],
            "general": [{"properties": {"altText": s(alt_txt)}}],
            "subTitle": [{"properties": {"show": lit("true"), "text": s(subtitulo)}}]}


def visual(nome, tipo, x, y, w, h, z, query, objetos, vco, filtros=None):
    d = {"$schema": SCHEMA, "name": nome,
         "position": {"x": x, "y": y, "z": z, "height": h, "width": w, "tabOrder": z},
         "visual": {"visualType": tipo, "query": query, "objects": objetos, "visualContainerObjects": vco,
                    "drillFilterOtherVisuals": True}}
    if filtros:
        d["filterConfig"] = {"filters": filtros}
    return d


def filtro_incluir(ent, prop, valores, alias, nome):
    return {"name": nome, "field": c_col(ent, prop), "type": "Categorical",
            "filter": {"Version": 2, "From": [{"Name": alias, "Entity": ent, "Type": 0}],
                       "Where": [{"Condition": {"In": {
                           "Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": alias}}, "Property": prop}}],
                           "Values": [[{"Literal": {"Value": "'" + v + "'"}}] for v in valores]}}}]},
            "howCreated": "User"}


# ------------------------------------------------------------------ visuais do corpo
def cartoes(out):
    """Faixa de cardVisual: OEE2, TCU, Disponibilidade, Performance e Qualidade (mesma geometria da pg_horahora)."""
    base = ler(vis_path("pg_horahora", "kpi0"))
    lista = [("OEE2", "OEE2", "OEE2 Ref. OEE2", "Cartão: OEE2 (apontamento) do período. Referência de set a nov: 52%."),
             ("OEE2 TCU", "TCU", "OEE2 Ref. TCU", "Cartão: TCU (24/7) do período. Referência de set a nov: 20%."),
             ("OEE2 Disponibilidade", "DISPONIBILIDADE", None, "Cartão: Disponibilidade do OEE2."),
             ("OEE2 Performance", "PERFORMANCE", None, "Cartão: Performance do OEE2."),
             ("OEE2 Qualidade", "QUALIDADE", None, "Cartão: Qualidade do OEE2 (refugo na data do refugo).")]
    n = len(lista)
    w = round((1048 - 16 * (n - 1)) / n, 2)
    for i, (medida, rotulo, ref, alt_txt) in enumerate(lista):
        d = copy.deepcopy(base)
        d["name"] = f"kpi{i}"
        d["position"] = {"x": round(216 + i * (w + 16), 2), "y": 88, "z": 8000 + i * 100, "height": 104, "width": w,
                         "tabOrder": 8000 + i * 100}
        d["visual"]["query"] = {"queryState": {"Data": {"projections": [proj(c_med(medida), nome=rotulo)]}}}
        d["visual"]["visualContainerObjects"]["general"] = [{"properties": {"altText": s(alt_txt)}}]
        d["visual"].pop("objects", None)
        if ref:
            d["visual"]["objects"] = {"referenceLabel": [{"properties": {"value": {"expr": c_med(ref)}},
                                                          "selector": {"id": "ref0"}}]}
        out(f"kpi{i}", d)


def cascata(out):
    q = {"queryState": {"Category": {"projections": [proj(c_col("dEtapaOEE", "Etapa"), ativo=True)]},
                        "Y": {"projections": [proj(c_med("OEE2 Cascata"))]}},
         "sortDefinition": {"sort": [{"field": c_col("dEtapaOEE", "Etapa"), "direction": "Ascending"}]}}
    o = {"legend": [{"properties": {"show": lit("false")}}],
         "labels": [{"properties": {"show": lit("true")}}],
         "sentimentColors": [{"properties": {"increaseFill": cor("#3C3C3B"), "decreaseFill": cor("#E2000F"),
                                             "totalFill": cor("#16A34A")}}]}
    vco = container("Para onde vai o tempo da janela até o valorizado bom (min)?",
                    "Janela, parada planejada, troca de lote, perdas na operação e refugo; o total é o valorizado bom",
                    "Gráfico de cascata em minutos: janela menos parada planejada, troca de lote, perdas na operação e "
                    "refugo, terminando no tempo valorizado bom. Para onde vai o tempo da janela até o valorizado bom?")
    out("g_cascata", visual("g_cascata", "waterfallChart", 748, 208, 516, 192, 14000, q, o, vco))


def pareto(out):
    cat = c_col("dMotivoParada", "Categoria Danfoss")
    med = c_med("OEE2 Minutos Parados")
    q = {"queryState": {"Category": {"projections": [proj(cat, ativo=True)]}, "Y": {"projections": [proj(med)]}},
         "sortDefinition": {"sort": [{"field": med, "direction": "Descending"}]}}
    o = {"legend": [{"properties": {"show": lit("false")}}],
         "labels": [{"properties": {"show": lit("true")}}],
         "dataPoint": [{"properties": {"fill": {"solid": {"color": {"expr": c_med("OEE2 Cor Família")}}}},
                        "selector": {"data": [{"dataViewWildcard": {"matchingOption": 1}}],
                                     "metadata": "Medidas.OEE2 Minutos Parados"}}]}
    vco = container("Em quais categorias de parada a máquina perdeu mais minutos?",
                    "Minutos parados por categoria Danfoss; a cor é a família (azul, cinza, amarela, vermelha)",
                    "Gráfico de barras de minutos parados por categoria Danfoss, colorido pela família do motivo. "
                    "Em quais categorias de parada a máquina perdeu mais minutos?")
    filtros = [filtro_incluir("dMotivoParada", "Família", ["Azul", "Cinza", "Amarela", "Vermelha"], "f", "f_familia")]
    out("g_pareto", visual("g_pareto", "clusteredBarChart", 748, 416, 516, 248, 14100, q, o, vco, filtros))


def matriz(out):
    q = {"queryState": {
        "Rows": {"projections": [proj(c_col("fHoraCheia", "Célula"), ativo=True)]},
        "Columns": {"projections": [proj(c_col("dTurno", "Turno"), ativo=True)]},
        "Values": {"projections": [proj(c_med("OEE2")), proj(c_med("OEE2 Aviso Velocidade"))]}},
        "sortDefinition": {"sort": [{"field": c_col("fHoraCheia", "Célula"), "direction": "Ascending"}]}}
    tam = lit("9D")
    o = {"columnHeaders": [{"properties": {"fontSize": tam, "wordWrap": lit("true")}}],
         "rowHeaders": [{"properties": {"fontSize": tam}}],
         "values": [{"properties": {"fontSize": tam}}],
         "general": [{"properties": {"layout": s("Compact")}}]}
    vco = container("Qual máquina e qual turno têm o menor OEE2?",
                    "OEE2 por máquina e turno BI; o aviso aponta velocidade validada abaixo do real",
                    "Matriz de OEE2 por máquina e turno BI, com uma coluna de aviso de velocidade validada abaixo do "
                    "real. Qual máquina e qual turno têm o menor OEE2?")
    out("g_matriz", visual("g_matriz", "pivotTable", 216, 208, 516, 304, 14200, q, o, vco))


def linha_dia(out):
    q = {"queryState": {"Category": {"projections": [proj(c_col("dCalendario", "Date"), ativo=True)]},
                        "Y": {"projections": [proj(c_med("OEE2"))]}}}
    o = {"legend": [{"properties": {"show": lit("false")}}],
         "categoryAxis": [{"properties": {"axisType": s("Categorical")}}],
         "labels": [{"properties": {"show": lit("false")}}]}
    vco = container("O OEE2 está subindo ou caindo por dia?", "OEE2 por dia produtivo (Data BI, 05:00 a 05:00)",
                    "Gráfico de linhas do OEE2 por dia produtivo. O OEE2 está subindo ou caindo por dia?")
    out("g_dia", visual("g_dia", "lineChart", 216, 528, 516, 136, 14300, q, o, vco))


def rodape(out):
    d = bp.textbox("rodape", 216, 672, 1048, 32, 15100,
                   "Limitações: OEE2 pelo apontamento do Hora-Hora, sem sensor (microparada e velocidade reduzida só aparecem "
                   "pelo motivo declarado). Qualidade pela data do refugo, não da trança; refugo sem trançadeira fica fora. "
                   "Pausa fixa de 45 min por turno com produção. Referência de set a nov do GMS, sem meta fixa. "
                   "Os 21h35 do cartão Meta não entram no OEE2.",
                   12, "#5F6368", REG, "Rodapé: limitações do OEE2 (apontamento, sem sensor; qualidade pela data do refugo).")
    out("rodape", d)


# ------------------------------------------------------------------ a página
def construir_pagina():
    pasta = os.path.join(PAGES, PG)
    vdir = os.path.join(pasta, "visuals")
    if os.path.isdir(vdir):
        shutil.rmtree(vdir)
    os.makedirs(vdir)
    escritos = []

    def out(nome, d):
        escritos.append(nome)
        gravar(os.path.join(vdir, nome, "visual.json"), d)

    # menu: cópia do menu já atualizado da pg_horahora; OEE2 fica ativo
    ori = os.path.join(PAGES, "pg_horahora", "visuals")
    for nome in sorted(os.listdir(ori)):
        if nome in ("faixa", "logo", "txt_app", "txt_secao_mangueira", "txt_secao_montagem", "nav_barra_ativa", "atualizado") \
                or nome.startswith("sub_") or nome.startswith("seg"):
            d = ler(os.path.join(ori, nome, "visual.json"))
            if nome == "sub_horahora":
                bp.estilo_botao(d, False)
                d["visual"]["visualContainerObjects"]["general"] = [{"properties": {"altText": s("Ir para a página " + texto_botao(d))}}]
            elif nome == "sub_oee2":
                bp.estilo_botao(d, True)
                d["visual"]["visualContainerObjects"]["general"] = [{"properties": {"altText": s("Página atual: OEE2")}}]
            elif nome == "nav_barra_ativa":
                d["position"]["y"] = NOVO_Y["sub_oee2"]
                d["visual"]["visualContainerObjects"]["general"] = [{"properties": {"altText": s("Marca a página atual no menu.")}}]
            out(nome, d)
    # cabeçalho: os slicers (Máquina, Turno, Período) já estão copiados acima e ocupam x >= 680
    w = 456
    out("titulo", bp.textbox("titulo", 216, 12, w, 32, 1000, TITULO, 22, "#1F1F1E", SEMI, "Título da página: " + TITULO + "."))
    out("txt_subtitulo", bp.textbox("txt_subtitulo", 216, 44, w, 20, 1010, SUBTITULO, 12, "#5F6368", REG,
                                    "Subtítulo: " + SUBTITULO + "."))
    cartoes(out)
    cascata(out)
    pareto(out)
    matriz(out)
    linha_dia(out)
    rodape(out)
    pj = ler(os.path.join(PAGES, "pg_horahora", "page.json"))
    pj["name"], pj["displayName"] = PG, TITULO
    gravar(os.path.join(pasta, "page.json"), pj)
    return sorted(escritos)


def ordem_das_paginas(relatorio):
    p = os.path.join(PAGES, "pages.json")
    d = ler(p)
    ordem = [x for x in d["pageOrder"] if x != PG]
    ordem.insert(ordem.index("pg_horahora") + 1, PG)
    d["pageOrder"] = ordem
    if gravar(p, d):
        relatorio.append("pages.json: pg_oee2 depois de pg_horahora")


if __name__ == "__main__":
    rel = []
    antigas = [p for p in sorted(os.listdir(PAGES)) if p.startswith("pg_") and p != PG]
    assert len(antigas) == 10, antigas
    for pg in antigas:
        atualiza_menu(pg, rel)
    v = construir_pagina()
    ordem_das_paginas(rel)
    print(f"menu: {len(rel)} arquivos alterados nas 10 páginas antigas + pages.json")
    for r in rel:
        print("  ", r)
    print(f"{PG}: {len(v)} visuais: {', '.join(v)}")
