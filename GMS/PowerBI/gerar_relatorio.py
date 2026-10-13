# -*- coding: utf-8 -*-
"""Gera o projeto Power BI (PBIR) do painel GMS.

Uso:  python gerar_relatorio.py
Saida: GMS_Painel.Report/ + GMS_Painel.pbip (relatorio "thin" ligado ao modelo semantico
       "(GMS)" do workspace "Controle de Fabricacao"). Nada de dado e gravado aqui.
Regras: GMS_Mestre_BI.md. Toda medida nova nasce como medida de relatorio (reportExtensions).
"""
import json
import shutil
from pathlib import Path

RAIZ = Path(__file__).parent
REL = RAIZ / "GMS_Painel.Report"
DEF = REL / "definition"

WORKSPACE = "Controle de Fabricação"
MODELO = "(GMS)"
MODELO_ID = "b48699da-af0b-4f0e-9b2e-f89cc657dbc1"

SCH = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition"

# ---- paleta (tema) -------------------------------------------------------
VERMELHO = "#E2000F"
GRAFITE = "#1F2937"
ARDOSIA = "#475569"
CINZA = "#6B7280"
LINHA = "#E5E7EB"
FUNDO = "#F3F4F6"
BRANCO = "#FFFFFF"
CORES = [VERMELHO, "#334155", "#64748B", "#94A3B8", "#CBD5E1", "#B91C1C", "#0F766E", "#D97706"]


def lit(v):
    return {"expr": {"Literal": {"Value": v}}}


def txt(s):
    return lit("'" + s.replace("'", "''") + "'")


def num(n):
    return lit(f"{n}D")


def boo(b):
    return lit("true" if b else "false")


def cor(hexa):
    return {"solid": {"color": txt(hexa)}}


def col(ent, prop):
    return {"Column": {"Expression": {"SourceRef": {"Entity": ent}}, "Property": prop}}


def med(prop, ent="Medidas"):
    return {"Measure": {"Expression": {"SourceRef": {"Entity": ent}}, "Property": prop}}


def proj(campo, ativo=False):
    k = "Column" if "Column" in campo else "Measure"
    ent = campo[k]["Expression"]["SourceRef"]["Entity"]
    p = campo[k]["Property"]
    d = {"field": campo, "queryRef": f"{ent}.{p}", "nativeQueryRef": p}
    if ativo:
        d["active"] = True
    return d


# ---- medidas de relatorio (reportExtensions) ----------------------------
D_MES = "DATEADD(dCalendario[Date], -1, MONTH)"
EXT = [
    ("Disponibilidade", "Double", "[Disponibilidade %]", "0.0%"),
    ("Tempo Parado %", "Double", "[% Tempo Parado]", "0.0%"),
    ("Δ Metragem vs mês ant.", "Double",
     f"VAR a = [Metragem Média Diária] VAR b = CALCULATE([Metragem Média Diária], {D_MES}) "
     "RETURN IF(NOT ISBLANK(b) && b <> 0, DIVIDE(a - b, b))", '+0.0%;-0.0%;0.0%'),
    ("Δ Disponibilidade vs mês ant.", "Double",
     f"VAR a = [Disponibilidade %] VAR b = CALCULATE([Disponibilidade %], {D_MES}) "
     "RETURN IF(NOT ISBLANK(b), a - b)", '+0.0%;-0.0%;0.0%'),
    ("Δ Tempo Parado vs mês ant.", "Double",
     f"VAR a = [% Tempo Parado] VAR b = CALCULATE([% Tempo Parado], {D_MES}) "
     "RETURN IF(NOT ISBLANK(b), a - b)", '+0.0%;-0.0%;0.0%'),
    ("Δ Produtividade vs mês ant.", "Double",
     f"VAR a = [Produtividade da Célula (m/h)] VAR b = CALCULATE([Produtividade da Célula (m/h)], {D_MES}) "
     "RETURN IF(NOT ISBLANK(b) && b <> 0, DIVIDE(a - b, b))", '+0.0%;-0.0%;0.0%'),
    ("Fila Média (h)", "Double", "AVERAGE(fFluxoEtapas[Fila_h])", "0.0"),
    ("Processamento Médio (h)", "Double", "AVERAGE(fFluxoEtapas[Proc_h])", "0.0"),
    ("Lead Time Médio (h)", "Double", "AVERAGE(fFluxoEtapas[Lead_h])", "0.0"),
]

# ---- construtores de visual ---------------------------------------------
class Pagina:
    def __init__(self, nome, titulo):
        self.nome = nome
        self.titulo = titulo
        self.visuais = []
        self.z = 0

    def add(self, nome, x, y, w, h, visual):
        self.z += 1
        self.visuais.append({
            "$schema": f"{SCH}/visualContainer/2.12.0/schema.json",
            "name": nome,
            "position": {"x": x, "y": y, "z": self.z, "height": h, "width": w, "tabOrder": self.z},
            "visual": visual,
        })


def container(titulo=None, fundo=True, tam_titulo=11):
    o = {}
    if titulo:
        o["title"] = [{"properties": {
            "show": boo(True), "text": txt(titulo), "fontColor": cor(ARDOSIA),
            "fontSize": num(tam_titulo), "bold": boo(True), "alignment": txt("left")}}]
    else:
        o["title"] = [{"properties": {"show": boo(False)}}]
    o["background"] = [{"properties": {"show": boo(fundo), "color": cor(BRANCO), "transparency": num(0)}}]
    o["border"] = [{"properties": {"show": boo(fundo), "color": cor(LINHA), "radius": num(8), "width": num(1)}}]
    o["dropShadow"] = [{"properties": {"show": boo(False)}}]
    o["padding"] = [{"properties": {"top": num(6), "bottom": num(6), "left": num(10), "right": num(10)}}]
    return o


def card(campo, titulo, fonte=24, cor_valor=GRAFITE):
    return {
        "visualType": "card",
        "query": {"queryState": {"Values": {"projections": [proj(campo)]}}},
        "objects": {
            "labels": [{"properties": {"fontSize": num(fonte), "color": cor(cor_valor), "bold": boo(True)}}],
            "categoryLabels": [{"properties": {"show": boo(False)}}],
        },
        "visualContainerObjects": container(titulo),
        "drillFilterOtherVisuals": True,
    }


def card_delta(campo):
    """Faixa pequena sob o KPI: mostra a variacao vs mes anterior (nome da medida como rotulo)."""
    return {
        "visualType": "card",
        "query": {"queryState": {"Values": {"projections": [proj(campo)]}}},
        "objects": {
            "labels": [{"properties": {"fontSize": num(11), "color": cor(ARDOSIA), "bold": boo(True)}}],
            "categoryLabels": [{"properties": {"show": boo(True), "fontSize": num(8), "color": cor(CINZA)}}],
        },
        "visualContainerObjects": container(None),
        "drillFilterOtherVisuals": True,
    }


def slicer(campo, titulo, sync=None):
    v = {
        "visualType": "slicer",
        "query": {"queryState": {"Values": {"projections": [proj(campo, True)]}}},
        "objects": {
            "data": [{"properties": {"mode": txt("Dropdown")}}],
            "header": [{"properties": {"show": boo(False)}}],
            "general": [{"properties": {"outlineColor": cor(LINHA)}}],
        },
        "visualContainerObjects": container(titulo, tam_titulo=9),
        "drillFilterOtherVisuals": True,
    }
    if sync:
        v["syncGroup"] = {"groupName": sync, "fieldChanges": True, "filterChanges": True}
    return v


def grafico(tipo, categoria, valores, titulo, ordenar=None, desc=False, segunda=None, legenda=False):
    qs = {"Category": {"projections": [proj(categoria, True)]},
          "Y": {"projections": [proj(m) for m in valores]}}
    if segunda:
        qs["Y2"] = {"projections": [proj(m) for m in segunda]}
    v = {
        "visualType": tipo,
        "query": {"queryState": qs},
        "objects": {
            "legend": [{"properties": {"show": boo(legenda), "position": txt("Bottom")}}],
            "categoryAxis": [{"properties": {"fontSize": num(9), "labelColor": cor(ARDOSIA)}}],
            "valueAxis": [{"properties": {"fontSize": num(9), "labelColor": cor(ARDOSIA),
                                          "gridlineColor": cor(LINHA)}}],
            "labels": [{"properties": {"show": boo(tipo != "lineChart"), "fontSize": num(9),
                                       "color": cor(GRAFITE)}}],
        },
        "visualContainerObjects": container(titulo),
        "drillFilterOtherVisuals": True,
    }
    if ordenar is not None:
        v["query"]["sortDefinition"] = {
            "sort": [{"field": ordenar, "direction": "Descending" if desc else "Ascending"}],
            "isDefaultSort": False}
    return v


def tabela(colunas, titulo):
    return {
        "visualType": "tableEx",
        "query": {"queryState": {"Values": {"projections": [proj(c) for c in colunas]}}},
        "objects": {
            "grid": [{"properties": {"gridVertical": boo(False), "gridHorizontal": boo(True),
                                     "gridHorizontalColor": cor(LINHA), "textSize": num(10)}}],
            "columnHeaders": [{"properties": {"fontColor": cor(BRANCO), "backColor": cor(ARDOSIA),
                                              "fontSize": num(10), "bold": boo(True)}}],
        },
        "visualContainerObjects": container(titulo),
        "drillFilterOtherVisuals": True,
    }


def caixa_texto(texto, tamanho, negrito=True, cor_t=GRAFITE, alinhamento="left"):
    return {
        "visualType": "textbox",
        "objects": {"general": [{"properties": {"paragraphs": [{
            "textRuns": [{"value": texto, "textStyle": {
                "fontWeight": "bold" if negrito else "normal", "fontSize": f"{tamanho}pt",
                "color": cor_t, "fontFamily": "Segoe UI Semibold"}}],
            "horizontalTextAlignment": alinhamento}]}}]},
        "visualContainerObjects": container(None, fundo=False),
    }


# ---- layout (grade 1280x720; margem 16; vao 12) ------------------------
MARGEM, VAO, W_PAG = 16, 12, 1280
LARG_UTIL = W_PAG - 2 * MARGEM  # 1248


def cabecalho(p, subtitulo):
    p.add("cab_titulo", MARGEM, 8, 760, 44, caixa_texto(f"GMS · {subtitulo}", 18))
    p.add("cab_atualizado", 940, 10, 324, 40,
          card(med("Dado Atualizado até"), None, fonte=11, cor_valor=ARDOSIA))
    p.add("seg_mes", MARGEM, 56, 200, 38, slicer(col("dCalendario", "AnoMês"), "Mês", sync="gms_mes"))
    p.add("seg_turno", MARGEM + 212, 56, 200, 38, slicer(col("Etapas", "Turno"), "Turno", sync="gms_turno"))


def kpis_com_delta(p, itens, y=100):
    """itens = [(rotulo, campo_medida, campo_delta|None)] em 6 colunas."""
    n = len(itens)
    w = (LARG_UTIL - VAO * (n - 1)) // n
    for i, (rotulo, campo, delta) in enumerate(itens):
        x = MARGEM + i * (w + VAO)
        if delta is None:
            p.add(f"kpi{i}", x, y, w, 100, card(campo, rotulo))
        else:
            p.add(f"kpi{i}", x, y, w, 72, card(campo, rotulo))
            p.add(f"kpi{i}_d", x, y + 72, w, 28, card_delta(delta))


def pagina_visao_geral():
    p = Pagina("pg_visao_geral", "Visão Geral")
    cabecalho(p, "Visão Geral da Produção")
    p.add("seg_etapa", MARGEM + 424, 56, 200, 38, slicer(col("Etapas", "Etapa"), "Etapa"))
    kpis_com_delta(p, [
        ("Metragem Média Diária", med("Metragem Média Diária"), med("Δ Metragem vs mês ant.")),
        ("Disponibilidade", med("Disponibilidade"), med("Δ Disponibilidade vs mês ant.")),
        ("Tempo Parado", med("Tempo Parado %"), med("Δ Tempo Parado vs mês ant.")),
        ("Refugo PPM", med("Refugo PPM"), med("Refugo PPM vs Mês Anterior")),
        ("Produtividade (m/h)", med("Produtividade da Célula (m/h)"), med("Δ Produtividade vs mês ant.")),
        ("Ordens em Andamento", med("Ordens em Andamento"), None),
    ])
    wl, wr = 626, 610
    p.add("g_tendencia", MARGEM, 208, wl, 246, grafico(
        "lineChart", col("dCalendario", "AnoMês"), [med("Metragem Média Diária")],
        "Metragem média diária por mês"))
    p.add("g_etapa", MARGEM + wl + VAO, 208, wr, 246, grafico(
        "clusteredBarChart", col("Etapas", "Etapa"), [med("Produção por Etapa")],
        "Produção por etapa (ordem do fluxo)", ordenar=col("Etapas", "OrdemEtapa")))
    p.add("g_celula", MARGEM, 466, wl, 238, grafico(
        "clusteredColumnChart", col("Producao_Montagem", "Celula"), [med("Produção por Célula")],
        "Produção por célula (Montagem)", ordenar=med("Produção por Célula"), desc=True))
    p.add("g_disp", MARGEM + wl + VAO, 466, wr, 238, grafico(
        "lineChart", col("dCalendario", "AnoMês"), [med("Tempo Disponível (h)"), med("Tempo Parado (h)")],
        "Tempo disponível × tempo parado (h)", legenda=True))
    return p


def pagina_gargalo():
    p = Pagina("pg_gargalo", "Gargalo e Fluxo")
    cabecalho(p, "Gargalo e Fluxo")
    kpis_com_delta(p, [
        ("Célula Gargalo", med("Célula Gargalo"), None),
        ("Fila no Gargalo (h)", med("Fila no Gargalo (h)"), None),
        ("Produtividade da Célula (m/h)", med("Produtividade da Célula (m/h)"), None),
        ("Turnos-Célula Ativos", med("Turnos-Célula Ativos"), None),
    ])
    wl, wr = 626, 610
    p.add("g_fluxo", MARGEM, 208, wl, 246, grafico(
        "barChart", col("fFluxoEtapas", "Etapa"), [med("Fila Média (h)"), med("Processamento Médio (h)")],
        "Fila × processamento por etapa (h)", ordenar=col("fFluxoEtapas", "Ordem_Etapa"), legenda=True))
    p.add("g_prod_cel", MARGEM + wl + VAO, 208, wr, 246, grafico(
        "clusteredColumnChart", col("Producao_Montagem", "Celula"), [med("Produtividade da Célula (m/h)")],
        "Produtividade por célula (m/h)", ordenar=med("Produtividade da Célula (m/h)"), desc=True))
    p.add("t_fluxo", MARGEM, 466, LARG_UTIL, 238, tabela(
        [col("fFluxoEtapas", "Etapa"), med("Fila Média (h)"), med("Processamento Médio (h)"),
         med("Lead Time Médio (h)")], "Lead time por etapa"))
    return p


def pagina_paradas():
    p = Pagina("pg_paradas", "Paradas e Qualidade")
    cabecalho(p, "Paradas e Qualidade")
    kpis_com_delta(p, [
        ("Tempo Parado (h)", med("Tempo Parado (h)"), None),
        ("Tempo Parado", med("Tempo Parado %"), med("Δ Tempo Parado vs mês ant.")),
        ("Motivo Nº1", med("Motivo Nº1"), None),
        ("Horas Perdidas (Motivo Nº1)", med("Horas Perdidas Motivo Nº1"), None),
        ("Refugo PPM", med("Refugo PPM"), med("Refugo PPM vs Mês Anterior")),
        ("Refugo (m)", med("Refugo (m)"), None),
    ])
    wl, wr = 760, 476
    p.add("g_pareto", MARGEM, 208, wl, 246, grafico(
        "lineClusteredColumnComboChart", col("Hora-Hora", "Motivo"), [med("Tempo Parado (h)")],
        "Pareto de paradas (h) e % acumulado", ordenar=med("Tempo Parado (h)"), desc=True,
        segunda=[med("% Acumulado Paradas")]))
    p.add("g_turno", MARGEM + wl + VAO, 208, wr, 246, grafico(
        "clusteredColumnChart", col("Hora-Hora", "Turno"), [med("Tempo Parado (h)")],
        "Tempo parado por turno (h)"))
    p.add("g_ppm", MARGEM, 466, 626, 238, grafico(
        "lineChart", col("dCalendario", "AnoMês"), [med("Refugo PPM")], "Refugo PPM por mês"))
    p.add("t_motivos", MARGEM + 626 + VAO, 466, 610, 238, tabela(
        [col("Hora-Hora", "Motivo"), med("Tempo Parado (h)"), med("% Acumulado Paradas")],
        "Motivos de parada"))
    return p


# ---- gravacao ------------------------------------------------------------
def grava(caminho, obj):
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    if REL.exists():
        shutil.rmtree(REL)
    grava(RAIZ / "GMS_Painel.pbip", {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/pbip/pbipProperties/1.0.0/schema.json",
        "version": "1.0",
        "artifacts": [{"report": {"path": "GMS_Painel.Report"}}],
        "settings": {"enableAutoRecovery": True},
    })
    grava(REL / "definition.pbir", {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json",
        "version": "4.0",
        "datasetReference": {"byConnection": {"connectionString": (
            f'Data Source="powerbi://api.powerbi.com/v1.0/myorg/{WORKSPACE}";'
            f'initial catalog={MODELO};access mode=readonly;integrated security=ClaimsToken;'
            f'semanticmodelid={MODELO_ID}')}},
    })
    grava(DEF / "version.json", {"$schema": f"{SCH}/versionMetadata/1.0.0/schema.json", "version": "2.0.0"})
    grava(DEF / "report.json", {
        "$schema": f"{SCH}/report/3.3.0/schema.json",
        "themeCollection": {
            "baseTheme": {"name": "CY26SU02", "reportVersionAtImport": "5.70", "type": "SharedResources"},
            "customTheme": {"name": "GMS_Tema.json", "reportVersionAtImport": "5.70", "type": "RegisteredResources"},
        },
        "resourcePackages": [{
            "name": "RegisteredResources", "type": "RegisteredResources",
            "items": [{"name": "GMS_Tema.json", "path": "GMS_Tema.json", "type": "CustomTheme"}],
        }],
        "settings": {"useStylableVisualContainerHeader": True, "exportDataMode": "AllowSummarized"},
    })
    grava(REL / "StaticResources" / "RegisteredResources" / "GMS_Tema.json", {
        "name": "GMS_Tema", "dataColors": CORES, "background": BRANCO, "foreground": GRAFITE,
        "tableAccent": VERMELHO, "good": "#0F766E", "neutral": "#D97706", "bad": VERMELHO,
        "maximum": VERMELHO, "center": "#CBD5E1", "minimum": "#334155",
        "textClasses": {
            "label": {"fontFace": "Segoe UI", "fontSize": 10},
            "callout": {"fontFace": "Segoe UI Semibold", "fontSize": 24},
            "title": {"fontFace": "Segoe UI Semibold", "fontSize": 12},
            "header": {"fontFace": "Segoe UI Semibold", "fontSize": 12},
        },
    })
    grava(DEF / "reportExtensions.json", {
        "$schema": f"{SCH}/reportExtension/1.0.0/schema.json",
        "name": "extension",
        "entities": [{"name": "Medidas", "measures": [
            {"name": n, "dataType": t, "expression": e, "formatString": f, "displayFolder": "Painel (relatório)"}
            for n, t, e, f in EXT]}],
    })
    paginas = [pagina_visao_geral(), pagina_gargalo(), pagina_paradas()]
    grava(DEF / "pages" / "pages.json", {
        "$schema": f"{SCH}/pagesMetadata/1.1.0/schema.json",
        "pageOrder": [p.nome for p in paginas], "activePageName": paginas[0].nome})
    for p in paginas:
        grava(DEF / "pages" / p.nome / "page.json", {
            "$schema": f"{SCH}/page/2.1.0/schema.json",
            "name": p.nome, "displayName": p.titulo, "displayOption": "FitToPage",
            "height": 720, "width": 1280,
            "objects": {"background": [{"properties": {"color": cor(FUNDO), "transparency": num(0)}}]},
        })
        for v in p.visuais:
            grava(DEF / "pages" / p.nome / "visuals" / v["name"] / "visual.json", v)
    print("ok:", sum(len(p.visuais) for p in paginas), "visuais em", len(paginas), "paginas")


if __name__ == "__main__":
    main()
