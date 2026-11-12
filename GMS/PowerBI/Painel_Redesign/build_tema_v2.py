"""Gera StaticResources/RegisteredResources/GMS_Tema.json (tema v2) na copia Painel_Redesign."""
import json, os
AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, "GMS_Painel.Report", "StaticResources", "RegisteredResources", "GMS_Tema.json")

def cor(h):
    return {"solid": {"color": h}}

def F(px):
    """px do prototipo -> pt do Power BI (x0,75, passo de 0,5 pt)."""
    return {7.5: 7.5, 10: 7.5, 11: 8, 12: 9, 13: 10, 14: 10.5, 30: 22.5}[px]


SEMI = "Segoe UI Semibold"
REG = "Segoe UI"
TXT, TXT2, TXT3 = "#1F1F1E", "#5F6368", "#8A8F96"
GRADE, BORDA = "#EEF0F2", "#E4E6EA"

eixo_cat = {"fontSize": F(10), "fontFamily": REG, "labelColor": cor(TXT3), "showAxisTitle": False,
            "gridlineShow": False}
eixo_val = {"fontSize": F(10), "fontFamily": REG, "labelColor": cor(TXT3), "showAxisTitle": False,
            "gridlineShow": True, "gridlineColor": cor(GRADE), "gridlineThickness": 1, "gridlineStyle": "solid"}
rotulos = {"fontSize": F(11), "fontFamily": REG, "color": cor(TXT)}
legenda = {"position": "Top", "fontSize": F(11), "fontFamily": REG, "labelColor": cor(TXT2), "showTitle": False}

def grafico(extra=None):
    d = {"categoryAxis": [eixo_cat], "valueAxis": [eixo_val], "labels": [rotulos], "legend": [legenda]}
    if extra:
        d.update(extra)
    return {"*": d}

sem_caixa = {  # textbox, botao, imagem, forma: sem cartao
    "background": [{"show": False}],
    "border": [{"show": False}],
    "dropShadow": [{"show": False}],
    "padding": [{"top": 0, "bottom": 0, "left": 0, "right": 0}],
}

tema = {
    "name": "GMS_Tema",
    "dataColors": ["#E2000F", "#3C3C3B", "#D5D8DD", "#F4A3A8", "#8A8F96", "#16A34A", "#D97706", "#5F6368"],
    "background": "#FFFFFF",
    "foreground": TXT,
    "tableAccent": "#E2000F",
    "good": "#16A34A",
    "neutral": "#D97706",
    "bad": "#C0392B",
    "maximum": "#E2000F",
    "center": "#D5D8DD",
    "minimum": "#3C3C3B",
    "textClasses": {
        "callout": {"fontSize": F(30), "fontFace": SEMI},
        "title": {"fontSize": F(14), "fontFace": SEMI},
        "header": {"fontSize": F(12), "fontFace": SEMI},
        "label": {"fontSize": F(11), "fontFace": REG},
    },
    "visualStyles": {
        "*": {"*": {
            "title": [{"fontFamily": SEMI, "fontSize": F(14), "fontColor": cor(TXT), "alignment": "left"}],
            "subTitle": [{"fontFamily": REG, "fontSize": F(11), "fontColor": cor(TXT3), "alignment": "left"}],
            "background": [{"show": True, "color": cor("#FFFFFF"), "transparency": 0}],
            "border": [{"show": True, "color": cor(BORDA), "radius": 6, "width": 1}],
            "dropShadow": [{"show": False}],
            "padding": [{"top": 12, "bottom": 12, "left": 16, "right": 16}],
        }},
        "cardVisual": {"*": {
            "layout": [{"$id": "default", "backgroundShow": False, "cellPadding": 0, "paddingUniform": 12}],
            "accentBar": [{"$id": "default", "show": True, "position": "Left", "width": 4, "color": cor("#3C3C3B")}],
            "value": [{"$id": "default", "fontSize": F(30), "fontFamily": SEMI, "fontColor": cor(TXT)}],
            "label": [{"$id": "default", "position": "aboveValue", "fontSize": F(11), "fontFamily": SEMI,
                       "fontColor": cor(TXT2)}],
            "referenceLabel": [{"$id": "default", "backgroundShow": False, "paddingUniform": 0}],
            "referenceLabelValue": [{"$id": "default", "valueFontSize": F(12), "valueFontFamily": REG,
                                     "valueFontColor": cor(TXT2)}],
            "referenceLabelTitle": [{"$id": "default", "show": False}],
        }},
        "card": {"*": {
            "labels": [{"fontSize": F(30), "fontFamily": SEMI, "color": cor(TXT)}],
            "categoryLabels": [{"fontSize": F(11), "fontFamily": REG, "color": cor(TXT2)}],
        }},
        "slicer": {"*": {
            "title": [{"fontSize": F(10), "fontFamily": SEMI, "fontColor": cor(TXT3), "alignment": "left"}],
            "items": [{"textSize": F(12), "fontFamily": SEMI, "fontColor": cor(TXT)}],
            "padding": [{"top": 4, "bottom": 4, "left": 8, "right": 8}],
        }},
        "actionButton": {"*": sem_caixa},
        "textbox": {"*": sem_caixa},
        "image": {"*": sem_caixa},
        "shape": {"*": sem_caixa},
        "clusteredBarChart": grafico(),
        "clusteredColumnChart": grafico(),
        "lineChart": grafico({"lineStyles": [{"strokeWidth": 2}]}),
        "lineClusteredColumnComboChart": grafico({"lineStyles": [{"strokeWidth": 2}]}),
        "page": {"*": {
            "background": [{"color": cor("#F2F3F5"), "transparency": 0}],
        }},
    },
}

if __name__ == "__main__":
    with open(SAIDA, "w", encoding="utf-8") as f:
        json.dump(tema, f, ensure_ascii=False, indent=2)
    print("gravado", SAIDA)
