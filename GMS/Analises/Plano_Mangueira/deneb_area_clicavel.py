# -*- coding: utf-8 -*-
"""Gera as especificações Vega-Lite (Deneb) da pg_plano_mangueira com a área clicável inteira (linha da barra / célula do anel).

python -I -X utf8 deneb_area_clicavel.py            -> imprime as 3 especificações em JSON (para teste)
python -I -X utf8 deneb_area_clicavel.py --aplicar  -> troca só o jsonSpec dos 3 visuais, sem mexer em posição nem formato
Antes de --aplicar: git status na pasta da página (mudança não commitada é do William) e Desktop fechado.
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
VIS = os.path.join(AQUI, "..", "..", "PowerBI", "GMS_Painel.Report", "definition", "pages", "pg_plano_mangueira", "visuals")
ALVO = {"cstandard": "a0436a85f344a1281d65", "tipo": "f8c62aca67ae57dcfa35", "arame": "043903d3a2fa8b475198"}
VERM, CINZA = "#E2000F", "#3C3C3B"
SCHEMA = "https://vega.github.io/schema/vega-lite/v5.json"
COR = {"field": "situacao", "type": "nominal", "scale": {"domain": ["atrás", "em dia"], "range": [VERM, CINZA]}, "legend": None}
APAGA = {"condition": {"test": "datum.__selected__ == 'off'", "value": 0.25}, "value": 1}
PARAMS = [{"name": "__select__", "select": {"type": "point"}},
          {"name": "passa", "select": {"type": "point", "on": "pointerover", "clear": "pointerout"}}]
# fundo invisível que recebe o clique: cinza leve ao passar o mouse e no item selecionado
FUNDO = {"condition": [{"param": "passa", "empty": False, "value": "rgba(60,60,59,0.08)"},
                       {"test": "datum.__selected__ == 'on'", "value": "rgba(60,60,59,0.05)"}],
         "value": "transparent"}
MIL = "replace(format(datum['HP Plano do Mês'] / 1000, '.1f'), '.', ',') + 'k'"
COMUM = [
    {"filter": "datum['HP Plano do Mês'] > 0"},
    {"calculate": "datum['HP % do Plano'] < datum['HP % Ritmo Esperado'] ? 'atrás' : 'em dia'", "as": "situacao"},
    {"calculate": "replace(format(datum['HP % do Plano'], '.1%'), '.', ',')", "as": "pct1"},
    {"calculate": "format(datum['HP % do Plano'], '.0%')", "as": "pct0"},
    {"calculate": "replace(format(datum['HP % Ritmo Esperado'], '.1%'), '.', ',')", "as": "ritmo1"},
    {"calculate": "replace(format(datum['HP Plano do Mês'], ',.0f'), regexp(',', 'g'), '.')", "as": "plano1"},
    {"joinaggregate": [{"op": "max", "field": "HP Plano do Mês", "as": "pmax"}]},
    {"calculate": "datum.pmax - datum['HP Plano do Mês']", "as": "chave"},
]


def titulo(t, sub, off):
    return {"text": t, "subtitle": sub, "anchor": "start", "font": "Segoe UI", "fontSize": 13, "fontWeight": 600, "color": CINZA,
            "subtitleFont": "Segoe UI", "subtitleFontSize": 10, "subtitleColor": "#8A8A88", "offset": off}


def dica(campo, nome):
    return [{"field": campo, "title": nome}, {"field": "plano1", "title": "Plano (m)"},
            {"field": "pct1", "title": "% do plano"}, {"field": "ritmo1", "title": "Ritmo esperado"}]


def cstandard():
    return {
        "$schema": SCHEMA,
        "title": titulo("Quanto de cada C.Standard saiu?",
                        "% do plano do mês · traço = ritmo esperado · vermelho = atrás do ritmo · clique na linha para filtrar", 10),
        "data": {"name": "dataset"},
        "transform": COMUM + [{"calculate": "datum['C_Standard'] + '   ' + " + MIL, "as": "rotulo"}],
        "width": "container",
        "height": {"step": 24},
        "encoding": {"y": {"field": "rotulo", "type": "nominal", "sort": {"field": "chave", "op": "min", "order": "ascending"}, "title": None,
                           "axis": {"labelFont": "Segoe UI", "labelFontSize": 11, "labelColor": CINZA, "domain": False, "ticks": False,
                                    "labelPadding": 8, "labelLimit": 220}}},
        "layer": [
            {"mark": {"type": "bar", "cornerRadius": 2, "height": 11, "color": "#EDEDED"},
             "encoding": {"x": {"datum": 1, "type": "quantitative", "scale": {"domain": [0, 1]}, "axis": None}}},
            {"mark": {"type": "bar", "cornerRadius": 2, "height": 11},
             "encoding": {"x": {"field": "HP % do Plano", "type": "quantitative", "scale": {"domain": [0, 1], "clamp": True}, "axis": None},
                          "color": COR, "opacity": APAGA}},
            {"mark": {"type": "tick", "color": CINZA, "thickness": 2, "size": 17},
             "encoding": {"x": {"field": "HP % Ritmo Esperado", "type": "quantitative"}}},
            {"mark": {"type": "text", "align": "left", "dx": 6, "font": "Segoe UI", "fontSize": 11, "fontWeight": "bold"},
             "encoding": {"x": {"datum": 1, "type": "quantitative"}, "text": {"field": "pct1"}, "color": COR}},
            {"params": PARAMS,
             "mark": {"type": "rect", "cursor": "pointer", "cornerRadius": 4},
             "encoding": {"x": {"value": -150}, "x2": {"value": {"expr": "width + 46"}}, "fill": FUNDO,
                          "tooltip": dica("C_Standard", "C.Standard")}},
        ],
        "config": {"view": {"stroke": None}, "padding": {"left": 6, "right": 6, "top": 4, "bottom": 4}},
    }


def aneis(tit, campo, nome, largura, espaco, extra, ordem):
    return {
        "$schema": SCHEMA,
        "title": titulo(tit, "% do plano do mês · vermelho = atrás do ritmo · clique no anel para filtrar", 4),
        "data": {"name": "dataset"},
        "transform": COMUM + extra + [{"calculate": "clamp(datum['HP % do Plano'], 0, 1)", "as": "pct"}],
        "facet": {"column": {"field": campo, "type": "nominal", "sort": {"field": ordem, "op": "min"}, "title": None, "header": None}},
        "spacing": espaco,
        "spec": {"width": largura, "height": 72, "layer": [
            {"mark": {"type": "arc", "innerRadius": 18, "outerRadius": 26, "color": "#E3E3E3"},
             "encoding": {"theta": {"datum": 1, "type": "quantitative", "scale": {"domain": [0, 1]}}, "y": {"value": 28}}},
            {"mark": {"type": "arc", "innerRadius": 18, "outerRadius": 26},
             "encoding": {"theta": {"field": "pct", "type": "quantitative", "scale": {"domain": [0, 1]}}, "y": {"value": 28},
                          "color": COR, "opacity": APAGA}},
            {"mark": {"type": "text", "font": "Segoe UI", "fontSize": 11, "fontWeight": "bold"},
             "encoding": {"y": {"value": 28}, "text": {"field": "pct0"}, "color": COR}},
            {"mark": {"type": "text", "font": "Segoe UI", "fontSize": 11, "color": CINZA},
             "encoding": {"y": {"value": 64}, "text": {"field": "rotulo"}}},
            {"params": PARAMS,
             "mark": {"type": "rect", "cursor": "pointer", "cornerRadius": 6},
             "encoding": {"x": {"value": 0}, "x2": {"value": "width"}, "y": {"value": 0}, "y2": {"value": "height"},
                          "fill": FUNDO, "tooltip": dica(campo, nome)}},
        ]},
        "config": {"view": {"stroke": None}, "padding": {"left": 8, "right": 8, "top": 0, "bottom": 0}},
    }


def specs():
    tipo = aneis("Quanto de cada tipo saiu?", "Tipo", "Tipo", 106, 10, [
        {"calculate": "indexof(['1T', '1A', '2A', '4A'], datum['Tipo']) < 0 ? 9 : indexof(['1T', '1A', '2A', '4A'], datum['Tipo'])", "as": "ordem"},
        {"calculate": "datum['Tipo'] + '  ' + " + MIL, "as": "rotulo"}], "ordem")
    arame = aneis("Quanto de cada arame saiu?", "nome", "Arame", 88, 5, [
        {"calculate": "indexof(datum['Arame'], '20C') >= 0 ? 'Arame 20C' : indexof(datum['Arame'], '24C') >= 0 ? 'Arame 24C' : "
                      "indexof(datum['Arame'], '36C') >= 0 ? 'Arame 36C' : upper(datum['Arame']) == 'SPIRAL' ? 'Espiral' : "
                      "upper(datum['Arame']) == 'TEXTIL' ? 'Têxtil' : datum['Arame']", "as": "nome"},
        {"calculate": "datum.nome + '  ' + " + MIL, "as": "rotulo"}], "chave")
    return {"cstandard": cstandard(), "tipo": tipo, "arame": arame}


def main():
    s = specs()
    if "--aplicar" not in sys.argv:
        print(json.dumps(s, ensure_ascii=False))
        return
    for k, pasta in ALVO.items():
        p = os.path.join(VIS, pasta, "visual.json")
        raw = open(p, encoding="utf-8", newline="").read()
        nl = "\r\n" if "\r\n" in raw else "\n"
        d = json.loads(raw)
        prop = next(o["properties"] for o in d["visual"]["objects"]["vega"] if "jsonSpec" in o["properties"])
        aspas = chr(39)
        texto = json.dumps(s[k], ensure_ascii=False, indent=2).replace(aspas, aspas * 2)
        prop["jsonSpec"]["expr"]["Literal"]["Value"] = aspas + texto + aspas
        fim = nl if raw.endswith("\n") else ""
        open(p, "w", encoding="utf-8", newline="").write(json.dumps(d, ensure_ascii=False, indent=2).replace("\n", nl) + fim)
        print("aplicado", k)


if __name__ == "__main__":
    main()
