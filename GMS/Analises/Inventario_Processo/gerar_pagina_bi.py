# gerar_pagina_bi.py: cria a página pg_inventario_processo e as medidas "IP · SVG ..." num relatório PBIP (MEL-278).
# Uso: python -I gerar_pagina_bi.py [pasta definition do .Report]   (padrão: cópia de teste Painel_PBIP_teste)
# Só acrescenta: página nova, a entrada dela no pages.json e as 5 medidas SVG no reportExtensions.json.
import json, os, sys
BASE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "PowerBI", "Painel_PBIP_teste", "GMS_Painel.Report", "definition")
FOLDER = "Inventário Processo (relatório)\\Visual"

INK, SUB, LINE, CARD, CORE = "%2314130f", "%2355534d", "%23e1e0d9", "%23ffffff", "%23efeee9"
COL = {"tubo": "%232a78d6", "trama": "%23eb6834", "cobertura": "%231baf7a", "bandagem": "%23eda100"}
RING = {"tubo": (24, 10), "trama": (34.5, 7), "cobertura": (44, 8), "bandagem": (52.5, 5)}
ORDEM = ["tubo", "trama", "cobertura", "bandagem"]


def corte(ncam):
    parts = ["<circle r='58' fill='none' stroke='%s' stroke-dasharray='2 4'/>" % LINE,
             "<circle r='18' fill='%s'/>" % CORE]
    for i, c in enumerate(ORDEM):
        r, w = RING[c]
        if i >= ncam:
            parts.append("<circle r='%s' fill='none' stroke='%s' stroke-width='%s' opacity='0.5'/>" % (r, LINE, w - 2))
            continue
        parts.append("<circle r='%s' fill='none' stroke='%s' stroke-width='%s' opacity='\" & __Op & \"'/>" % (r, COL[c], w - 2))
        if c == "trama":
            parts.append("<circle r='%s' fill='none' stroke='%s' stroke-width='%s' stroke-dasharray='1.6 3.2' opacity='0.55'/>" % (r, CARD, w - 2))
        if c == "bandagem":
            parts.append("<circle r='%s' fill='none' stroke='%s' stroke-width='1' opacity='0.7'/>" % (r, CARD))
    return "".join(parts)


def svg_corte(sit, onde, ncam):
    return f'''-- Cartão "Onde está a mangueira": corte da mangueira ({ncam} camada(s)), onde está, metros, OPs e kg da situação "{sit}". Camadas ausentes em cinza claro. · MEL-278
VAR __Sit = "{sit}"
VAR __Met = CALCULATE ( [IP Metros], fInventarioOP[Situação] = __Sit )
VAR __Ops = CALCULATE ( [IP OPs na Conta], fInventarioOP[Situação] = __Sit )
VAR __Kg = CALCULATE ( [IP Insumo kg], fInventarioOP[Situação] = __Sit )
VAR __Op = IF ( __Ops > 0, "1", "0.35" )
VAR __Aneis = "{corte(ncam)}"
VAR __Texto =
    "<text x='136' y='52' font-size='15' font-weight='700' fill='{INK}'>{sit}</text>"
        & "<text x='136' y='70' font-size='10.5' fill='{SUB}'>{onde}</text>"
        & "<text x='136' y='110' fill='{INK}'><tspan font-size='24' font-weight='700'>" & FORMAT ( COALESCE ( __Met, 0 ), "#,0", "pt-BR" ) & "</tspan><tspan font-size='12' fill='{SUB}'> m</tspan></text>"
        & "<text x='136' y='134' font-size='12' fill='{SUB}'>" & FORMAT ( COALESCE ( __Ops, 0 ), "0", "pt-BR" ) & " OPs · " & FORMAT ( COALESCE ( __Kg, 0 ), "#,0", "pt-BR" ) & " kg</text>"
RETURN
    "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='303' height='176' viewBox='0 0 303 176' font-family='Segoe UI, sans-serif'>"
        & "<rect x='0.5' y='0.5' width='302' height='175' rx='12' fill='{CARD}' stroke='{LINE}' stroke-width='1'/>"
        & "<g transform='translate(66 88)'>" & __Aneis & "</g>" & __Texto & "</svg>"'''


KPI = f'''-- Faixa de 4 cartões KPI: OPs na conta, metros em processo, kg de insumo, metros sem BOM (com OPs sem BOM e OPs paradas fora). Cartão 4 com borda amarela se há metros sem BOM. · MEL-278
VAR __Ops = COALESCE ( [IP OPs na Conta], 0 )
VAR __Met = COALESCE ( [IP Metros], 0 )
VAR __Kg = COALESCE ( [IP Insumo kg], 0 )
VAR __MSem = COALESCE ( [IP Metros sem BOM], 0 )
VAR __OSem = COALESCE ( [IP OPs sem BOM], 0 )
VAR __OPar = COALESCE ( [IP OPs Paradas], 0 )
VAR __C1 =
    "<rect x='0.5' y='0.5' width='299' height='83' rx='12' fill='{CARD}' stroke='{LINE}'/>"
        & "<text x='16' y='44' font-size='26' font-weight='700' fill='{INK}'>" & FORMAT ( __Ops, "#,0", "pt-BR" ) & "</text>"
        & "<text x='16' y='66' font-size='12' fill='{SUB}'>OPs na conta</text>"
VAR __C2 =
    "<rect x='316.5' y='0.5' width='299' height='83' rx='12' fill='{CARD}' stroke='{LINE}'/>"
        & "<text x='332' y='44' fill='{INK}'><tspan font-size='26' font-weight='700'>" & FORMAT ( __Met, "#,0", "pt-BR" ) & "</tspan><tspan font-size='14' fill='{SUB}'> m</tspan></text>"
        & "<text x='332' y='66' font-size='12' fill='{SUB}'>de mangueira em processo</text>"
VAR __C3 =
    "<rect x='632.5' y='0.5' width='299' height='83' rx='12' fill='{CARD}' stroke='{LINE}'/>"
        & "<text x='648' y='44' fill='{INK}'><tspan font-size='26' font-weight='700'>" & FORMAT ( __Kg, "#,0", "pt-BR" ) & "</tspan><tspan font-size='14' fill='{SUB}'> kg</tspan></text>"
        & "<text x='648' y='66' font-size='12' fill='{SUB}'>de insumo em processo</text>"
VAR __C4 =
    "<rect x='948.5' y='0.5' width='299' height='83' rx='12' fill='{CARD}' stroke='" & IF ( __MSem > 0, "%23fab219", "{LINE}" ) & "' stroke-width='" & IF ( __MSem > 0, "1.5", "1" ) & "'/>"
        & "<text x='964' y='44' fill='{INK}'><tspan font-size='26' font-weight='700'>" & FORMAT ( __MSem, "#,0", "pt-BR" ) & "</tspan><tspan font-size='14' fill='{SUB}'> m</tspan></text>"
        & "<text x='964' y='66' font-size='11.5' fill='{SUB}'>sem BOM (" & FORMAT ( __OSem, "0", "pt-BR" ) & " OPs) · " & FORMAT ( __OPar, "0", "pt-BR" ) & " OPs paradas fora</text>"
RETURN
    "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='1248' height='84' viewBox='0 0 1248 84' font-family='Segoe UI, sans-serif'>"
        & __C1 & __C2 & __C3 & __C4 & "</svg>"'''

CR = ["IP Metros", "IP OPs na Conta", "IP Insumo kg"]
MEAS = [
    ("IP · SVG KPIs", KPI, ["IP OPs na Conta", "IP Metros", "IP Insumo kg", "IP Metros sem BOM", "IP OPs sem BOM", "IP OPs Paradas"]),
    ("IP · SVG Corte Tubo interno", svg_corte("Tubo interno", "na fila ou na Trançagem", 1), CR),
    ("IP · SVG Corte Trançada", svg_corte("Trançada / Espiralada", "na Cobertura", 2), CR),
    ("IP · SVG Corte Coberta", svg_corte("Coberta", "na Bandagem", 3), CR),
    ("IP · SVG Corte Bandada", svg_corte("Bandada", "Vulcanização, Debandagem e Cabine", 4), CR),
]

# ---- reportExtensions
p = os.path.join(BASE, "reportExtensions.json")
d = json.load(open(p, encoding="utf-8"))
ms = d["entities"][0]["measures"]
ms[:] = [m for m in ms if not m["name"].startswith("IP · SVG")]
for name, expr, refs in MEAS:
    ms.append({"name": name, "dataType": "Text", "expression": expr, "dataCategory": "ImageUrl",
               "displayFolder": FOLDER,
               "references": {"measures": [{"entity": "Medidas", "name": r} for r in refs]}})
open(p, "w", encoding="utf-8", newline="").write(json.dumps(d, indent=2, ensure_ascii=False))


# ---- helpers de visual
def lit(v): return {"expr": {"Literal": {"Value": v}}}
def hexc(c): return {"solid": {"color": lit("'%s'" % c)}}
def off(): return [{"properties": {"show": lit("false")}}]
def hide_all():
    return {"title": off(), "background": off(), "border": off(), "dropShadow": off(),
            "padding": [{"properties": {k: lit("0D") for k in ("top", "bottom", "left", "right")}}]}
def card_box(title):
    return {"title": [{"properties": {"show": lit("true"), "text": lit("'%s'" % title), "fontColor": hexc("#475569"), "fontSize": lit("11D"), "bold": lit("true"), "alignment": lit("'left'")}}],
            "background": [{"properties": {"show": lit("true"), "color": hexc("#FFFFFF"), "transparency": lit("0D")}}],
            "border": [{"properties": {"show": lit("true"), "color": hexc("#E5E7EB"), "radius": lit("8D"), "width": lit("1D")}}],
            "dropShadow": off(),
            "padding": [{"properties": {"top": lit("6D"), "bottom": lit("6D"), "left": lit("10D"), "right": lit("10D")}}]}
SCH = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.14.0/schema.json"
def alt(box, text):
    box["general"] = [{"properties": {"altText": lit("'%s'" % text)}}]
    return box
def col(ent, prop): return {"Column": {"Expression": {"SourceRef": {"Entity": ent}}, "Property": prop}}
def meas(prop, ext=False):
    sr = {"Schema": "extension", "Entity": "Medidas"} if ext else {"Entity": "Medidas"}
    return {"Measure": {"Expression": {"SourceRef": sr}, "Property": prop}}
def proj(field, ent, prop, display=None, active=False):
    pr = {"field": field, "queryRef": "%s.%s" % (ent, prop), "nativeQueryRef": prop}
    if display: pr["displayName"] = display
    if active: pr["active"] = True
    return pr
def textbox(paragraphs):
    return {"visualType": "textbox", "objects": {"general": [{"properties": {"paragraphs": paragraphs}}]}, "drillFilterOtherVisuals": True}
def para(*runs): return {"textRuns": list(runs)}
def run(t, size, color, font="Segoe UI"): return {"value": t, "textStyle": {"fontFamily": font, "fontSize": size, "color": color}}
def image(measure):
    return {"visualType": "image", "objects": {"image": [{"properties": {"sourceType": lit("'imageUrl'"), "sourceUrl": {"expr": meas(measure, True)}}}]}, "drillFilterOtherVisuals": True}

visuals = {}
def put(name, x, y, w, h, z, visual, box, extra=None):
    visual["visualContainerObjects"] = box
    v = {"$schema": SCH, "name": name, "position": {"x": x, "y": y, "z": z, "height": h, "width": w, "tabOrder": z}, "visual": visual}
    if extra: v.update(extra)
    visuals[name] = v

put("titulo", 16, 8, 800, 48, 1000,
    textbox([para(run("Inventário em processo · material na linha", "18pt", "#14130f", "Segoe UI Semibold")),
             para(run("Ficha de produção · OPs Aguardando ou Em processo, da Trançagem à Cabine · OP parada acima de 15 dias fica fora da conta", "10pt", "#55534d"))]), hide_all())
put("kpis", 16, 64, 1248, 84, 2000, image("IP · SVG KPIs"), alt(hide_all(), "Quatro indicadores: OPs na conta, metros em processo, kg de insumo e metros sem BOM."))
for i, (nm, sit) in enumerate([("Tubo interno", "Tubo interno"), ("Trançada", "Trançada / Espiralada"), ("Coberta", "Coberta"), ("Bandada", "Bandada")]):
    put("sit_%d" % (i + 1), 16 + 315 * i, 156, 303, 176, 3000 + i * 100,
        image("IP · SVG Corte " + nm), alt(hide_all(), "%s: corte da mangueira com as camadas já aplicadas, onde está, metros, OPs e kg." % sit))
leg = [para(run("Camadas:  ", "9pt", "#55534D"),
             run("■ ", "9pt", "#2a78d6"), run("Tubo interno (composto)    ", "9pt", "#55534D"),
             run("■ ", "9pt", "#eb6834"), run("Trama (fio, insulation, leno, cimento)    ", "9pt", "#55534D"),
             run("■ ", "9pt", "#1baf7a"), run("Cobertura (composto)    ", "9pt", "#55534D"),
             run("■ ", "9pt", "#eda100"), run("Bandagem (match-mate, filme)    ", "9pt", "#55534D"),
             run("Camada ausente em cinza claro", "9pt", "#898781"))]
put("legenda", 16, 336, 1248, 20, 7000, textbox(leg), alt(hide_all(), "Legenda das cores das camadas da mangueira."))


def bar(name, x, w, title, measure, z, unid):
    visual = {"visualType": "barChart",
              "query": {"queryState": {
                  "Category": {"projections": [proj(col("fInventarioInsumo", "PartNumber"), "fInventarioInsumo", "PartNumber", active=True)]},
                  "Series": {"projections": [proj(col("fInventarioInsumo", "Camada"), "fInventarioInsumo", "Camada", active=True)]},
                  "Y": {"projections": [proj(meas(measure), "Medidas", measure)]}},
                  "sortDefinition": {"sort": [{"field": meas(measure), "direction": "Descending"}]}},
              "objects": {
                  "legend": [{"properties": {"show": lit("false")}}],
                  "categoryAxis": [{"properties": {"fontSize": lit("9D"), "labelColor": hexc("#475569")}}],
                  "valueAxis": [{"properties": {"fontSize": lit("9D"), "labelColor": hexc("#475569"), "gridlineColor": hexc("#E5E7EB")}}],
                  "labels": [{"properties": {"show": lit("true"), "fontSize": lit("9D"), "color": hexc("#1F2937")}}],
                  "dataPoint": [{"properties": {"fill": hexc(c)}, "selector": {"data": [{"scopeId": {"Comparison": {"ComparisonKind": 0, "Left": col("fInventarioInsumo", "Camada"), "Right": {"Literal": {"Value": "'%s'" % k}}}}}]}}
                                for k, c in [("tubo", "#2a78d6"), ("trama", "#eb6834"), ("cobertura", "#1baf7a"), ("bandagem", "#eda100")]]},
              "drillFilterOtherVisuals": True}
    put(name, x, 362, w, 150, z, visual, alt(card_box(title), "Insumo em %s por part-number, cor pela camada." % unid))


bar("g_kg", 16, 440, "Insumo em processo (kg) por part-number", "IP Insumo kg", 8000, "kg")
bar("g_m", 464, 380, "Insumo em processo (m) por part-number", "IP Insumo m", 8100, "metros")

flt = {"filterConfig": {"filters": [{"name": "f_sembom", "field": meas("IP OPs sem BOM"), "type": "Advanced",
                                     "filter": {"Version": 2, "From": [{"Name": "m", "Entity": "Medidas", "Type": 0}],
                                                "Where": [{"Condition": {"Comparison": {"ComparisonKind": 2,
                                                    "Left": {"Measure": {"Expression": {"SourceRef": {"Source": "m"}}, "Property": "IP OPs sem BOM"}},
                                                    "Right": {"Literal": {"Value": "0D"}}}}}]}}]}}


def tbl_objs(sz="9D"):
    return {"columnHeaders": [{"properties": {"fontSize": lit(sz), "fontColor": hexc("#55534D"), "backColor": hexc("#F6F5F2"), "bold": lit("true")}}],
            "values": [{"properties": {"fontSize": lit(sz), "fontColor": hexc("#14130F")}}],
            "grid": [{"properties": {"gridVertical": lit("false"), "gridHorizontal": lit("true"), "gridHorizontalColor": hexc("#E1E0D9")}}]}


sb = {"visualType": "tableEx",
      "query": {"queryState": {"Values": {"projections": [
          proj(col("fInventarioOP", "Mangueira"), "fInventarioOP", "Mangueira", "Mangueira"),
          proj(meas("IP OPs sem BOM"), "Medidas", "IP OPs sem BOM", "OPs"),
          proj(meas("IP Metros sem BOM"), "Medidas", "IP Metros sem BOM", "Metros")]}},
          "sortDefinition": {"sort": [{"field": meas("IP Metros sem BOM"), "direction": "Descending"}]}},
      "objects": tbl_objs(), "drillFilterOtherVisuals": True}
put("t_sem_bom", 856, 362, 408, 150, 8200, sb, alt(card_box("Mangueiras sem BOM (metros ficam fora da conta)"), "Mangueiras sem BOM, com OPs e metros."), flt)


def colp(prop, disp, agg=None):
    f = col("fInventarioOP", prop)
    if agg is not None:
        f = {"Aggregation": {"Expression": f, "Function": agg}}
    pr = {"field": f, "queryRef": ("Sum(fInventarioOP.%s)" % prop) if agg is not None else "fInventarioOP.%s" % prop,
          "nativeQueryRef": disp if agg is not None else prop}
    if disp != prop: pr["displayName"] = disp
    return pr


ops_proj = [colp("OP", "OP"), colp("Mangueira", "Mangueira"), colp("Etapa", "Etapa"), colp("Status", "Status"), colp("Situação", "Situação"),
            colp("Metros", "Metros", 0),
            proj(meas("IP Dias Parada"), "Medidas", "IP Dias Parada", "Dias parada"),
            proj(meas("IP Insumo kg"), "Medidas", "IP Insumo kg", "Insumo kg"),
            proj(meas("IP Motivo Fora"), "Medidas", "IP Motivo Fora", "Fora da conta"),
            proj(meas("IP Alerta Metros"), "Medidas", "IP Alerta Metros", "Alerta")]
ot = {"visualType": "tableEx",
      "query": {"queryState": {"Values": {"projections": ops_proj}},
                "sortDefinition": {"sort": [{"field": {"Aggregation": {"Expression": col("fInventarioOP", "Metros"), "Function": 0}}, "direction": "Descending"}]}},
      "objects": tbl_objs(), "drillFilterOtherVisuals": True}
put("t_ops", 16, 518, 1248, 158, 8300, ot, alt(card_box("OPs em processo"), "Tabela de OPs em processo: etapa, status, situação, metros, dias parada, insumo e alertas."))

at = {"visualType": "card",
      "query": {"queryState": {"Values": {"projections": [proj(meas("Dado Atualizado até"), "Medidas", "Dado Atualizado até")]}}},
      "objects": {"labels": [{"properties": {"fontSize": lit("9D"), "color": hexc("#55534D"), "fontFamily": lit("'Segoe UI'")}}],
                  "categoryLabels": [{"properties": {"show": lit("false")}}]},
      "drillFilterOtherVisuals": True}
put("atualizado", 992, 682, 272, 32, 9000, at, alt(hide_all(), "Data e hora do último dado carregado no modelo."))
nav = {"visualType": "pageNavigator",
       "objects": {
           "text": [{"properties": {"fontSize": lit("9D"), "fontFamily": lit("'Segoe UI'"), "fontColor": hexc("#55534D")}, "selector": {"id": "default"}},
                    {"properties": {"fontColor": hexc("#14130F"), "bold": lit("true")}, "selector": {"id": "selected"}}],
           "fill": [{"properties": {"show": lit("true"), "fillColor": hexc("#FFFFFF"), "transparency": lit("0D")}, "selector": {"id": "default"}},
                    {"properties": {"fillColor": hexc("#D6E4F7")}, "selector": {"id": "selected"}}],
           "outline": [{"properties": {"show": lit("true"), "lineColor": hexc("#E1E0D9"), "weight": lit("1D")}, "selector": {"id": "default"}}]},
       "drillFilterOtherVisuals": True}
put("nav", 16, 682, 960, 32, 8500, nav, alt(hide_all(), "Navegação entre as páginas do painel."))

# ---- página
pg = os.path.join(BASE, "pages", "pg_inventario_processo")
os.makedirs(pg, exist_ok=True)
src = json.load(open(os.path.join(BASE, "pages", "pg_fluxo_1", "page.json"), encoding="utf-8"))
src["name"] = "pg_inventario_processo"
src["displayName"] = "Inventário em processo"
open(os.path.join(pg, "page.json"), "w", encoding="utf-8", newline="").write(json.dumps(src, indent=2, ensure_ascii=False))
for n, v in visuals.items():
    dd = os.path.join(pg, "visuals", n)
    os.makedirs(dd, exist_ok=True)
    open(os.path.join(dd, "visual.json"), "w", encoding="utf-8", newline="").write(json.dumps(v, indent=2, ensure_ascii=False))

# ---- pages.json
pj = os.path.join(BASE, "pages", "pages.json")
d = json.load(open(pj, encoding="utf-8"))
if "pg_inventario_processo" not in d["pageOrder"]:
    d["pageOrder"].append("pg_inventario_processo")
open(pj, "w", encoding="utf-8", newline="").write(json.dumps(d, indent=2, ensure_ascii=False))
print("ok")
