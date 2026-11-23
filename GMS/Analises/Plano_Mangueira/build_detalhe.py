# -*- coding: utf-8 -*-
"""Monta a página pg_plano_mangueira_detalhe (Detalhe por mangueira) no GMS_Painel.Report.

Copia de pg_plano_mangueira o que é moldura (faixa, logo, menu, rodapé 'atualizado', segmentação de mês)
sem mexer em posição/formatação, e cria: título, subtítulo, botão Voltar, 4 filtros suspensos,
tabela por mangueira e matriz dia a dia. Acrescenta o botão 'Ver detalhe' na pg_plano_mangueira e as
3 medidas de cor no reportExtensions.json. Só cria a página se ela não existir: depois que o William ajusta no Desktop, edite o visual.json direto (--forcar recria do zero e APAGA os ajustes dele).
Uso: python -I -X utf8 build_detalhe.py
"""
import json, os, re, shutil, copy

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "PowerBI", "GMS_Painel.Report", "definition")
PAGES = os.path.join(RAIZ, "pages")
ORIG = os.path.join(PAGES, "pg_plano_mangueira")
NOVA = os.path.join(PAGES, "pg_plano_mangueira_detalhe")
SCH_V = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.14.0/schema.json"
MOLDURA_PREFIXOS = ("sub_", "txt_secao", "nav_barra_ativa", "faixa", "logo", "txt_app", "atualizado", "seg_mes")


def lit(v):
    return {"expr": {"Literal": {"Value": v}}}


def txt(s):
    return lit("'" + s.replace("'", "''") + "'")


def col(ent, prop):
    return {"Column": {"Expression": {"SourceRef": {"Entity": ent}}, "Property": prop}}


def med(prop):
    return {"Measure": {"Expression": {"SourceRef": {"Entity": "Medidas"}}, "Property": prop}}


def ext(prop):
    return {"Measure": {"Expression": {"SourceRef": {"Schema": "extension", "Entity": "Medidas"}}, "Property": prop}}


def proj_col(ent, prop, nome=None):
    p = {"field": col(ent, prop), "queryRef": f"{ent}.{prop}", "nativeQueryRef": nome or prop}
    if nome:
        p["displayName"] = nome
    return p


def proj_med(prop, nome):
    return {"field": med(prop), "queryRef": f"Medidas.{prop}", "nativeQueryRef": nome, "displayName": nome}


def grava(pasta, nome, d):
    os.makedirs(os.path.join(pasta, "visuals", nome), exist_ok=True)
    with open(os.path.join(pasta, "visuals", nome, "visual.json"), "w", encoding="utf-8", newline="\r\n") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)


def base(nome, x, y, w, h, z, vt):
    return {"$schema": SCH_V, "name": nome,
            "position": {"x": x, "y": y, "z": z, "height": h, "width": w, "tabOrder": z},
            "visual": {"visualType": vt}}


def caixa_sem_fundo(alt):
    return {"title": [{"properties": {"show": lit("false")}}],
            "background": [{"properties": {"show": lit("false")}}],
            "visualHeader": [{"properties": {"show": lit("false")}}],
            "general": [{"properties": {"altText": txt(alt)}}]}


def caixa_branca(alt, titulo=None):
    o = {"background": [{"properties": {"show": lit("true"), "color": {"solid": {"color": lit("'#FFFFFF'")}}, "transparency": lit("0D")}}],
         "border": [{"properties": {"show": lit("true"), "color": {"solid": {"color": lit("'#FFFFFF'")}}, "radius": lit("8D")}}],
         "padding": [{"properties": {"top": lit("8D"), "bottom": lit("8D"), "left": lit("10D"), "right": lit("10D")}}],
         "general": [{"properties": {"altText": txt(alt)}}]}
    if titulo:
        o["title"] = [{"properties": {"show": lit("true"), "text": txt(titulo), "fontSize": lit("10D"),
                                      "fontColor": {"solid": {"color": lit("'#3C3C3B'")}}, "bold": lit("true")}}]
    else:
        o["title"] = [{"properties": {"show": lit("false")}}]
    return o


def texto(nome, x, y, w, h, z, s, size, cor, fam):
    d = base(nome, x, y, w, h, z, "textbox")
    d["visual"]["objects"] = {"general": [{"properties": {"paragraphs": [{"textRuns": [{"value": s, "textStyle": {"fontSize": size, "color": cor, "fontFamily": fam}}]}]}}]}
    d["visual"]["visualContainerObjects"] = caixa_sem_fundo(s)
    return d


def botao(modelo, nome, x, y, w, h, z, rotulo, destino, alt):
    d = copy.deepcopy(modelo)
    d["name"] = nome
    d["position"] = {"x": x, "y": y, "z": z, "height": h, "width": w, "tabOrder": z}
    v = d["visual"]
    for t in v["objects"]["text"]:
        if "text" in t["properties"]:
            t["properties"]["text"] = txt(rotulo)
    v["objects"]["fill"] = [{"properties": {"show": lit("true")}},
                            {"properties": {"fillColor": {"solid": {"color": lit("'#FFFFFF'")}}, "transparency": lit("0D")}, "selector": {"id": "default"}}]
    for t in v["objects"]["text"]:
        t["properties"]["fontColor"] = {"solid": {"color": lit("'#3C3C3B'")}}
    v["objects"]["shape"] = [{"properties": {"roundEdge": lit("8L")}, "selector": {"id": "default"}}]
    v["objects"]["outline"] = [{"properties": {"show": lit("true"), "lineColor": {"solid": {"color": lit("'#D9D9D9'")}}}, "selector": {"id": "default"}}]
    vco = v["visualContainerObjects"]
    vco["visualLink"][0]["properties"]["navigationSection"] = txt(destino)
    vco["general"] = [{"properties": {"altText": txt(alt)}}]
    return d


def filtro(nome, x, w, z, prop, titulo):
    d = base(nome, x, 88, w, 56, z, "slicer")
    v = d["visual"]
    v["query"] = {"queryState": {"Values": {"projections": [dict(proj_col("dClasseMangueira", prop, titulo), active=True)]}}}
    v["objects"] = {"data": [{"properties": {"mode": lit("'Dropdown'")}}],
                    "header": [{"properties": {"show": lit("false")}}],
                    "items": [{"properties": {}}],
                    "selection": [{"properties": {"singleSelect": lit("false"), "strictSingleSelect": lit("false"), "selectAllCheckboxEnabled": lit("true")}}]}
    vco = caixa_branca(f"Filtro de {titulo}", titulo)
    vco["visualHeader"] = [{"properties": {"show": lit("false")}}]
    v["visualContainerObjects"] = vco
    v["drillFilterOtherVisuals"] = True
    return d


def tabela():
    d = base("tbl_mangueira", 216, 152, 1048, 300, 40000, "tableEx")
    v = d["visual"]
    v["query"] = {"queryState": {"Values": {"projections": [
        proj_col("dClasseMangueira", "Mangueira"),
        proj_col("dClasseMangueira", "C.Standard"),
        proj_col("dClasseMangueira", "Tipo"),
        proj_col("dClasseMangueira", "Arame"),
        proj_med("HP Plano do Mês", "Plano (m)"),
        proj_med("HP Devia até Corte", "Devia até o corte (m)"),
        proj_med("HP Produzido", "Produzido (m)"),
        proj_med("HP Diferença", "Diferença (m)"),
        proj_med("HP % do Plano", "% do plano")]}},
        "sortDefinition": {"sort": [{"field": med("HP Diferença"), "direction": "Ascending"}]}}
    cor = lambda m, fonte: {"properties": {"fontColor": {"solid": {"color": {"expr": ext(fonte)}}}},
                            "selector": {"data": [{"dataViewWildcard": {"matchingOption": 1}}], "metadata": f"Medidas.{m}"}}
    v["objects"] = {
        "columnHeaders": [{"properties": {"fontColor": {"solid": {"color": lit("'#8A8A88'")}}, "fontSize": lit("9D"), "bold": lit("true"),
                                          "backColor": {"solid": {"color": lit("'#FFFFFF'")}}, "wordWrap": lit("true")}}],
        "values": [{"properties": {"fontSize": lit("9D"), "fontColorPrimary": {"solid": {"color": lit("'#3C3C3B'")}},
                                   "backColorPrimary": {"solid": {"color": lit("'#FFFFFF'")}},
                                   "backColorSecondary": {"solid": {"color": lit("'#F7F7F7'")}}}},
                   cor("HP Diferença", "HP · Cor Atraso"), cor("HP % do Plano", "HP · Cor Atraso")],
        "total": [{"properties": {"fontSize": lit("9D"), "bold": lit("true"), "fontColor": {"solid": {"color": lit("'#1F1F1E'")}}}}],
        "grid": [{"properties": {"gridHorizontal": lit("true"), "gridHorizontalColor": {"solid": {"color": lit("'#EDEDED'")}},
                                 "gridVertical": lit("false"), "outlineColor": {"solid": {"color": lit("'#D9D9D9'")}}}}]}
    v["visualContainerObjects"] = caixa_branca("Tabela por mangueira: plano do mês, quanto devia ter saído até o corte, produzido no SAP, diferença em metros (produzido − devia; negativo = atrás) e percentual do plano. Ordenada da mais atrasada para a mais adiantada; clique no título da coluna para ordenar.",
                                               "Por mangueira · vermelho = atrás do planejado até o corte")
    v["drillFilterOtherVisuals"] = True
    return d


def matriz():
    d = base("mtx_dia", 216, 460, 1048, 244, 41000, "pivotTable")
    v = d["visual"]
    v["query"] = {"queryState": {
        "Rows": {"projections": [dict(proj_col("dClasseMangueira", "Mangueira"), active=True)]},
        "Columns": {"projections": [dict(proj_col("dCalendario", "Dia"), active=True)]},
        "Values": {"projections": [proj_med("HP Produzido no Dia", "m")]}}}
    cel = lambda prop, m: {"properties": {prop: {"solid": {"color": {"expr": ext(m)}}}},
                           "selector": {"data": [{"dataViewWildcard": {"matchingOption": 1}}], "metadata": "Medidas.HP Produzido no Dia"}}
    v["objects"] = {
        "columnHeaders": [{"properties": {"fontColor": {"solid": {"color": lit("'#8A8A88'")}}, "fontSize": lit("9D"), "alignment": lit("'Center'"),
                                          "backColor": {"solid": {"color": lit("'#FFFFFF'")}}}}],
        "rowHeaders": [{"properties": {"fontColor": {"solid": {"color": lit("'#3C3C3B'")}}, "fontSize": lit("9D")}}],
        "values": [{"properties": {"fontSize": lit("9D")}}, cel("backColor", "HP · Fundo Dia"), cel("fontColor", "HP · Fonte Dia")],
        "grid": [{"properties": {"gridHorizontal": lit("true"), "gridHorizontalColor": {"solid": {"color": lit("'#FFFFFF'")}},
                                 "gridVertical": lit("true"), "gridVerticalColor": {"solid": {"color": lit("'#FFFFFF'")}}}}],
        "subTotals": [{"properties": {"rowSubtotals": lit("true"), "columnSubtotals": lit("true")}}]}
    v["visualContainerObjects"] = caixa_branca("Produzido por dia: metros de cada mangueira em cada dia do mês (dia do lançamento no SAP). Quanto mais escuro, mais metros. Última coluna e última linha são os totais.",
                                               "Produzido por dia (m) · mais escuro = mais metros")
    v["drillFilterOtherVisuals"] = True
    return d


def medidas_cor():
    p = os.path.join(RAIZ, "reportExtensions.json")
    raw = open(p, encoding="utf-8").read()
    nl = "\r\n" if "\r\n" in raw else "\n"
    d = json.loads(raw)
    novas = {
        "HP · Cor Atraso": "-- Cor da fonte do atraso e do % na tabela da página de detalhe: vermelho Danfoss quando atrás do planejado até o corte. · Plano mangueira x SAP\nIF ( [HP Diferença] < 0, \"#E2000F\", \"#3C3C3B\" )",
        "HP · Fundo Dia": "-- Fundo da célula da grade dia a dia: cinza mais escuro quanto mais metros no dia. Vazio sem produção. · Plano mangueira x SAP\nVAR __v = [HP Produzido no Dia]\nRETURN\nSWITCH ( TRUE (), NOT ( __v > 0 ), BLANK (), __v < 250, \"#E9E9EA\", __v < 500, \"#CFCFD0\", __v < 1000, \"#A9A9A8\", __v < 1500, \"#6F6F6E\", \"#3C3C3B\" )",
        "HP · Fonte Dia": "-- Cor do número na grade dia a dia: branco nas células escuras, cinza escuro nas claras. · Plano mangueira x SAP\nIF ( [HP Produzido no Dia] > 1000, \"#FFFFFF\", \"#3C3C3B\" )",
    }
    ent = d["entities"][0]
    ent["measures"] = [m for m in ent["measures"] if m["name"] not in novas]
    refs = {"HP · Cor Atraso": "HP Diferença", "HP · Fundo Dia": "HP Produzido no Dia", "HP · Fonte Dia": "HP Produzido no Dia"}
    for n, e in novas.items():
        ent["measures"].append({"name": n, "dataType": "Text", "expression": e, "displayFolder": "Plano Mangueira (relatório)",
                                "references": {"measures": [{"entity": "Medidas", "name": refs[n]}]}})
    s = json.dumps(d, ensure_ascii=False, indent=2).replace("\n", nl)
    open(p, "w", encoding="utf-8", newline="").write(s + (nl if raw.endswith("\n") else ""))


def main():
    import sys
    if os.path.isdir(NOVA) and "--forcar" not in sys.argv:
        sys.exit("A página já existe e pode ter ajustes do William feitos no Desktop. Edite o visual.json direto; só use --forcar para recriar do zero.")
    if os.path.isdir(NOVA):
        shutil.rmtree(NOVA)
    os.makedirs(os.path.join(NOVA, "visuals"))
    pg = json.load(open(os.path.join(ORIG, "page.json"), encoding="utf-8"))
    pg["name"] = "pg_plano_mangueira_detalhe"
    pg["displayName"] = "Detalhe por mangueira"
    pg["visibility"] = "HiddenInViewMode"
    with open(os.path.join(NOVA, "page.json"), "w", encoding="utf-8", newline="\r\n") as f:
        json.dump(pg, f, ensure_ascii=False, indent=2)
    # moldura copiada sem mudar posição nem formato
    for v in os.listdir(os.path.join(ORIG, "visuals")):
        if v.startswith(MOLDURA_PREFIXOS):
            shutil.copytree(os.path.join(ORIG, "visuals", v), os.path.join(NOVA, "visuals", v))
    modelo_btn = json.load(open(os.path.join(ORIG, "visuals", "sub_plano_mangueira", "visual.json"), encoding="utf-8"))
    grava(NOVA, "titulo", texto("titulo", 216, 12, 456, 32, 1000, "Detalhe por mangueira", "16.5pt", "#1F1F1E", "Segoe UI Semibold"))
    grava(NOVA, "txt_subtitulo", texto("txt_subtitulo", 216, 44, 520, 20, 1100, "Plano do mês x produção do SAP, por mangueira e por dia", "9pt", "#8A8A88", "Segoe UI"))
    grava(NOVA, "btn_voltar", botao(modelo_btn, "btn_voltar", 852, 22, 148, 36, 1200, "‹ Voltar ao plano", "pg_plano_mangueira", "Voltar para a página Plano de mangueira x SAP"))
    for i, (nome, x, w, prop, tit) in enumerate([("flt_cstandard", 216, 300, "C.Standard", "C.Standard"), ("flt_tipo", 524, 150, "Tipo", "Tipo"),
                                                  ("flt_arame", 682, 200, "Arame", "Arame"), ("flt_mangueira", 890, 374, "Mangueira", "Mangueira")]):
        grava(NOVA, nome, filtro(nome, x, w, 30000 + i * 100, prop, tit))
    grava(NOVA, "tbl_mangueira", tabela())
    grava(NOVA, "mtx_dia", matriz())
    # botão na página principal
    grava(ORIG, "btn_detalhe", botao(modelo_btn, "btn_detalhe", 836, 22, 168, 36, 1200, "Ver detalhe por mangueira ›", "pg_plano_mangueira_detalhe",
                                     "Abre o detalhe por mangueira: tabela com atraso de cada mangueira e produção dia a dia"))
    # páginas
    pj = os.path.join(PAGES, "pages.json")
    raw = open(pj, encoding="utf-8").read()
    p = json.loads(raw)
    if "pg_plano_mangueira_detalhe" not in p["pageOrder"]:
        p["pageOrder"].insert(p["pageOrder"].index("pg_plano_mangueira") + 1, "pg_plano_mangueira_detalhe")
    nl = "\r\n" if "\r\n" in raw else "\n"
    open(pj, "w", encoding="utf-8", newline="").write(json.dumps(p, ensure_ascii=False, indent=2).replace("\n", nl) + (nl if raw.endswith("\n") else ""))
    medidas_cor()
    print("ok:", sorted(os.listdir(os.path.join(NOVA, "visuals"))))


if __name__ == "__main__":
    main()
