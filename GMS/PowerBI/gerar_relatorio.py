# -*- coding: utf-8 -*-
"""Gera o projeto Power BI (PBIR) do painel GMS.

Uso:  python gerar_relatorio.py
Saida: GMS_Painel.Report/ (relatorio "thin" ligado ao modelo semantico "(GMS)" do workspace
       "Controle de Fabricação"). Nada de dado e gravado aqui.
Base:  pares campo x medida validados no relatorio antigo "(GMS) (4).pbix" (mesma pasta),
       filtros de refeicao, logo Danfoss e cores de turno aproveitados dele.
Regras: GMS_Mestre_BI.md. Medida nova nasce como medida de relatorio (reportExtensions).
"""
import json
import shutil
from pathlib import Path

RAIZ = Path(__file__).parent
REL = RAIZ / "GMS_Painel.Report"
DEF = REL / "definition"
RES = RAIZ / "recursos"

WORKSPACE = "Controle de Fabricação"
MODELO = "(GMS)"
MODELO_ID = "b48699da-af0b-4f0e-9b2e-f89cc657dbc1"
LOGO = "Danfoss-Logo37611713405676106.jpg"
BASE_TEMA = "CY25SU12"

SCH = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition"
VERSAO_IMPORT = {"visual": "2.5.0", "report": "3.1.0", "page": "2.3.0"}  # formato que o Desktop exige

# ---- paleta (Danfoss) ------------------------------------------------------
VERMELHO = "#E30613"
GRAFITE = "#1F2937"
ARDOSIA = "#475569"
CINZA = "#6B7280"
LINHA = "#E5E7EB"
FUNDO = "#F3F4F6"
BRANCO = "#FFFFFF"
CORES = [VERMELHO, "#334155", "#64748B", "#94A3B8", "#CBD5E1", "#B91C1C", "#0F766E", "#D97706"]
COR_TURNO = {"1º Turno": "#4FC3F7", "2º Turno": "#FFD54F", "3º Turno": "#34D399"}  # do relatorio antigo


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


def fp(prop):
    return med(prop, "ficha_producao")


def proj(campo, ativo=False):
    k = "Column" if "Column" in campo else "Measure"
    ent = campo[k]["Expression"]["SourceRef"]["Entity"]
    p = campo[k]["Property"]
    d = {"field": campo, "queryRef": f"{ent}.{p}", "nativeQueryRef": p}
    if ativo:
        d["active"] = True
    return d


# ---- medidas de relatorio (reportExtensions) ------------------------------
D_MES = "DATEADD(dCalendario[Date], -1, MONTH)"
FMT_VAR = '+0.0%;-0.0%;0.0%'
EXT = [
    ("Disponibilidade", "Double", "[Disponibilidade %]", "0.0%"),
    ("Tempo Parado %", "Double", "[% Tempo Parado]", "0.0%"),
    ("Δ Metragem vs mês ant.", "Double",
     f"VAR a = [Metragem Produzida] VAR b = CALCULATE([Metragem Produzida], {D_MES}) "
     "RETURN IF(NOT ISBLANK(b) && b <> 0, DIVIDE(a - b, b))", FMT_VAR),
    ("Δ Disponibilidade vs mês ant.", "Double",
     f"VAR a = [Disponibilidade %] VAR b = CALCULATE([Disponibilidade %], {D_MES}) "
     "RETURN IF(NOT ISBLANK(b), a - b)", FMT_VAR),
    ("Δ Tempo Parado vs mês ant.", "Double",
     f"VAR a = [% Tempo Parado] VAR b = CALCULATE([% Tempo Parado], {D_MES}) "
     "RETURN IF(NOT ISBLANK(b), a - b)", FMT_VAR),
    ("Fila Média (h)", "Double", "AVERAGE(fFluxoEtapas[Fila_h])", "0.0"),
    ("Processamento Médio (h)", "Double", "AVERAGE(fFluxoEtapas[Proc_h])", "0.0"),
    ("Lead Time Médio (h)", "Double", "AVERAGE(fFluxoEtapas[Lead_h])", "0.0"),
    ("Tempo Parado Montagem (min)", "Double", "SUM(Paradas_Montagem[TempoParadoMin])", "#,0"),
    ("Quantidade Produzida Montagem", "Double", "SUM(Producao_Montagem[QtdProduzida])", "#,0"),
]


# ---- infraestrutura -------------------------------------------------------
class Pagina:
    def __init__(self, nome, titulo, filtros=None):
        self.nome, self.titulo, self.filtros = nome, titulo, filtros or []
        self.visuais, self.z = [], 0

    def add(self, nome, x, y, w, h, visual):
        self.z += 1
        self.visuais.append({
            "$schema": f"{SCH}/visualContainer/2.12.0/schema.json",
            "name": nome,
            "position": {"x": x, "y": y, "z": self.z, "height": h, "width": w, "tabOrder": self.z},
            "visual": visual,
        })


def filtro_excluir(ent, prop, valores, alias, nome):
    """Filtro de pagina 'tudo exceto estes valores' (refeicao nao e parada)."""
    return {
        "name": nome, "field": col(ent, prop), "type": "Categorical",
        "filter": {"Version": 2, "From": [{"Name": alias, "Entity": ent, "Type": 0}],
                   "Where": [{"Condition": {"Not": {"Expression": {"In": {
                       "Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": alias}}, "Property": prop}}],
                       "Values": [[{"Literal": {"Value": "'" + v + "'"}}] for v in valores]}}}}}]},
        "howCreated": "User",
        "objects": {"general": [{"properties": {"isInvertedSelectionMode": boo(True)}}]},
    }


FILTRO_HH = lambda: [filtro_excluir("Hora-Hora", "Motivo", ["Almoço", "22 - Refeição"], "h", "f_refeicao_hh")]
FILTRO_PM = lambda: [filtro_excluir("Paradas_Montagem", "Motivo", ["RF - Refeição"], "p", "f_refeicao_pm")]


def container(titulo=None, fundo=True, tam_titulo=11, cor_titulo=ARDOSIA):
    o = {}
    if titulo:
        o["title"] = [{"properties": {
            "show": boo(True), "text": txt(titulo), "fontColor": cor(cor_titulo),
            "fontSize": num(tam_titulo), "bold": boo(True), "alignment": txt("left")}}]
    else:
        o["title"] = [{"properties": {"show": boo(False)}}]
    o["background"] = [{"properties": {"show": boo(fundo), "color": cor(BRANCO), "transparency": num(0)}}]
    o["border"] = [{"properties": {"show": boo(fundo), "color": cor(LINHA), "radius": num(8), "width": num(1)}}]
    o["dropShadow"] = [{"properties": {"show": boo(False)}}]
    o["padding"] = [{"properties": {"top": num(6), "bottom": num(6), "left": num(10), "right": num(10)}}]
    return o


def card(campo, titulo, fonte=24, cor_valor=GRAFITE, fundo=True, cor_titulo=ARDOSIA):
    return {
        "visualType": "card",
        "query": {"queryState": {"Values": {"projections": [proj(campo)]}}},
        "objects": {
            "labels": [{"properties": {"fontSize": num(fonte), "color": cor(cor_valor), "bold": boo(True)}}],
            "categoryLabels": [{"properties": {"show": boo(False)}}],
        },
        "visualContainerObjects": container(titulo, fundo=fundo, cor_titulo=cor_titulo),
        "drillFilterOtherVisuals": True,
    }


def card_delta(campo):
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
        },
        "visualContainerObjects": container(titulo, tam_titulo=9),
        "drillFilterOtherVisuals": True,
    }
    if sync:
        v["syncGroup"] = {"groupName": sync, "fieldChanges": True, "filterChanges": True}
    return v


def grafico(tipo, categoria, valores, titulo, ordenar=None, desc=False, segunda=None, legenda=False,
            cores_turno=None):
    qs = {"Category": {"projections": [proj(categoria, True)]},
          "Y": {"projections": [proj(m) for m in valores]}}
    if segunda:
        qs["Y2"] = {"projections": [proj(m) for m in segunda]}
    obj = {
        "legend": [{"properties": {"show": boo(legenda), "position": txt("Bottom")}}],
        "categoryAxis": [{"properties": {"fontSize": num(9), "labelColor": cor(ARDOSIA)}}],
        "valueAxis": [{"properties": {"fontSize": num(9), "labelColor": cor(ARDOSIA), "gridlineColor": cor(LINHA)}}],
        "labels": [{"properties": {"show": boo(tipo != "lineChart"), "fontSize": num(9), "color": cor(GRAFITE)}}],
    }
    if cores_turno:
        ent = categoria["Column"]["Expression"]["SourceRef"]["Entity"]
        obj["dataPoint"] = [{
            "properties": {"fill": cor(c)},
            "selector": {"data": [{"scopeId": {"Comparison": {"ComparisonKind": 0,
                                  "Left": col(ent, "Turno"),
                                  "Right": {"Literal": {"Value": "'" + t + "'"}}}}}]},
        } for t, c in COR_TURNO.items()]
    v = {"visualType": tipo, "query": {"queryState": qs}, "objects": obj,
         "visualContainerObjects": container(titulo), "drillFilterOtherVisuals": True}
    if ordenar is not None:
        v["query"]["sortDefinition"] = {
            "sort": [{"field": ordenar, "direction": "Descending" if desc else "Ascending"}],
            "isDefaultSort": False}
    return v


def pizza(categoria, valor, titulo):
    return {
        "visualType": "pieChart",
        "query": {"queryState": {"Category": {"projections": [proj(categoria, True)]},
                                 "Y": {"projections": [proj(valor)]}}},
        "objects": {"legend": [{"properties": {"show": boo(True), "position": txt("Bottom")}}]},
        "visualContainerObjects": container(titulo),
        "drillFilterOtherVisuals": True,
    }


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


def matriz(linhas, valores, titulo):
    return {
        "visualType": "pivotTable",
        "query": {"queryState": {"Rows": {"projections": [proj(c, True) for c in linhas]},
                                 "Values": {"projections": [proj(m) for m in valores]}}},
        "objects": {
            "columnHeaders": [{"properties": {"fontColor": cor(BRANCO), "backColor": cor(ARDOSIA),
                                              "fontSize": num(10), "bold": boo(True)}}],
            "grid": [{"properties": {"gridHorizontal": boo(True), "gridHorizontalColor": cor(LINHA)}}],
        },
        "visualContainerObjects": container(titulo),
        "drillFilterOtherVisuals": True,
    }


def caixa_texto(texto, tamanho, cor_t=BRANCO):
    return {
        "visualType": "textbox",
        "objects": {"general": [{"properties": {"paragraphs": [{
            "textRuns": [{"value": texto, "textStyle": {
                "fontWeight": "bold", "fontSize": f"{tamanho}pt", "color": cor_t,
                "fontFamily": "Segoe UI Semibold"}}]}]}}]},
        "visualContainerObjects": container(None, fundo=False),
    }


def faixa(cor_fill):
    return {
        "visualType": "shape",
        "objects": {
            "shape": [{"properties": {"tileShape": txt("rectangle")}}],
            "fill": [{"properties": {"fillColor": cor(cor_fill)}, "selector": {"id": "default"}}],
            "outline": [{"properties": {"show": boo(False)}}],
        },
        "drillFilterOtherVisuals": True,
    }


def logo():
    return {
        "visualType": "image",
        "objects": {"image": [{"properties": {"sourceFile": {"image": {
            "name": txt(LOGO),
            "url": {"expr": {"ResourcePackageItem": {"PackageName": "RegisteredResources", "PackageType": 1,
                                                    "ItemName": LOGO}}},
            "scaling": txt("Fit")}}}}]},
        "visualContainerObjects": {
            "background": [{"properties": {"show": boo(True), "color": cor(BRANCO)}}],
            "title": [{"properties": {"show": boo(False)}}]},
        "drillFilterOtherVisuals": True,
    }


def navegador():
    return {
        "visualType": "pageNavigator",
        "objects": {
            "fill": [{"properties": {"fillColor": cor(BRANCO)}, "selector": {"id": "default"}},
                     {"properties": {"fillColor": cor(VERMELHO)}, "selector": {"id": "selected"}}],
            "text": [{"properties": {"fontColor": cor(GRAFITE), "fontSize": num(10)}, "selector": {"id": "default"}},
                     {"properties": {"fontColor": cor(BRANCO)}, "selector": {"id": "selected"}}],
        },
        "visualContainerObjects": container(None, fundo=False),
        "drillFilterOtherVisuals": True,
    }


# ---- layout (grade 1280x720; margem 16; vao 12) ---------------------------
MARGEM, VAO, W_PAG = 16, 12, 1280
LARG_UTIL = W_PAG - 2 * MARGEM
Y_KPI, Y_R1, Y_R2 = 102, 210, 464


def cabecalho(p, titulo, slicers):
    """Faixa vermelha com titulo/logo, navegador entre paginas e ate 3 slicers."""
    p.add("faixa", 0, 0, 1280, 48, faixa(VERMELHO))
    p.add("titulo", MARGEM, 6, 700, 36, caixa_texto(f"GMS · {titulo}", 18))
    p.add("atualizado", 760, 8, 330, 32,
          card(med("Dado Atualizado até"), None, fonte=11, cor_valor=BRANCO, fundo=False))
    p.add("logo", 1100, 0, 180, 48, logo())
    p.add("nav", MARGEM, 54, 700, 40, navegador())
    larg, x = 168, W_PAG - MARGEM
    for i, (campo, rotulo, sync) in enumerate(reversed(slicers)):
        x -= larg
        p.add(f"seg{i}", x, 54, larg, 40, slicer(campo, rotulo, sync))
        x -= VAO


def kpis(p, itens, y=Y_KPI):
    """itens = [(rotulo, campo, delta|None)] distribuidos na largura util."""
    n = len(itens)
    w = (LARG_UTIL - VAO * (n - 1)) // n
    for i, (rotulo, campo, delta) in enumerate(itens):
        x = MARGEM + i * (w + VAO)
        if delta is None:
            p.add(f"kpi{i}", x, y, w, 100, card(campo, rotulo))
        else:
            p.add(f"kpi{i}", x, y, w, 72, card(campo, rotulo))
            p.add(f"kpi{i}_d", x, y + 72, w, 28, card_delta(delta))


SEG_MES = (col("dCalendario", "AnoMês"), "Mês", "gms_mes")
WL, WR = 626, 610


def pg_visao_geral():
    p = Pagina("pg_visao_geral", "Visão Geral", FILTRO_HH())
    cabecalho(p, "Visão Geral da Produção",
              [SEG_MES, (col("Hora-Hora", "Turno"), "Turno", "gms_turno")])
    kpis(p, [
        ("Metragem Produzida", fp("Metragem Produzida"), med("Δ Metragem vs mês ant.")),
        ("Atingimento da Meta", fp("% Atingimento Meta"), None),
        ("Disponibilidade", med("Disponibilidade"), med("Δ Disponibilidade vs mês ant.")),
        ("Tempo Parado", med("Tempo Parado %"), med("Δ Tempo Parado vs mês ant.")),
        ("Refugo PPM", med("Refugo PPM"), med("Refugo PPM vs Mês Anterior")),
        ("Ordens em Andamento", med("Ordens em Andamento"), None),
    ])
    p.add("g_tendencia", MARGEM, Y_R1, WL, 244, grafico(
        "lineChart", col("dCalendario", "AnoMês"), [fp("Metragem Produzida")], "Metragem produzida por mês"))
    p.add("g_etapa", MARGEM + WL + VAO, Y_R1, WR, 244, grafico(
        "clusteredBarChart", col("Etapas", "Etapa"), [med("Produção por Etapa")],
        "Produção por etapa (ordem do fluxo)", ordenar=col("Etapas", "OrdemEtapa")))
    p.add("g_motivo", MARGEM, Y_R2, WL, 240, grafico(
        "clusteredBarChart", col("Hora-Hora", "Motivo"), [med("Tempo Parado (h)")],
        "Motivos de parada por tempo (h)", ordenar=med("Tempo Parado (h)"), desc=True))
    p.add("g_refugo", MARGEM + WL + VAO, Y_R2, WR, 240, grafico(
        "clusteredColumnChart", col("TiposErros", "CodigoErro"), [med("Refugo (m)")],
        "Refugo (m) por código de erro", ordenar=med("Refugo (m)"), desc=True))
    return p


def pg_gargalo():
    p = Pagina("pg_gargalo", "Gargalo e Fluxo", FILTRO_HH())
    cabecalho(p, "Gargalo e Fluxo", [SEG_MES, (col("Hora-Hora", "Célula"), "Célula", "gms_celula")])
    kpis(p, [
        ("Célula Gargalo", med("Célula Gargalo"), None),
        ("Fila no Gargalo (h)", med("Fila no Gargalo (h)"), None),
        ("Produtividade da Célula (m/h)", med("Produtividade da Célula (m/h)"), None),
        ("Turnos-Célula Ativos", med("Turnos-Célula Ativos"), None),
    ])
    p.add("g_fluxo", MARGEM, Y_R1, WL, 244, grafico(
        "barChart", col("fFluxoEtapas", "Etapa"), [med("Fila Média (h)"), med("Processamento Médio (h)")],
        "Fila × processamento por etapa (h)", ordenar=col("fFluxoEtapas", "Ordem_Etapa"), legenda=True))
    p.add("g_celula", MARGEM + WL + VAO, Y_R1, WR, 244, grafico(
        "clusteredColumnChart", col("Hora-Hora", "Célula"), [med("Tempo Parado (h)")],
        "Tempo parado por célula (h)", ordenar=med("Tempo Parado (h)"), desc=True))
    p.add("t_fluxo", MARGEM, Y_R2, LARG_UTIL, 240, tabela(
        [col("fFluxoEtapas", "Etapa"), med("Fila Média (h)"), med("Processamento Médio (h)"),
         med("Lead Time Médio (h)")], "Lead time por etapa"))
    return p


def pg_paradas():
    p = Pagina("pg_paradas", "Paradas e Qualidade", FILTRO_HH())
    cabecalho(p, "Paradas e Qualidade (Mangueira)",
              [SEG_MES, (col("Hora-Hora", "Turno"), "Turno", "gms_turno"),
               (col("Hora-Hora", "Motivo"), "Motivo", None)])
    kpis(p, [
        ("Tempo Parado (h)", med("Tempo Parado (h)"), None),
        ("Tempo Parado", med("Tempo Parado %"), med("Δ Tempo Parado vs mês ant.")),
        ("Motivo Mais Frequente", med("Motivo Mais Frequente"), None),
        ("Horas Perdidas (Motivo Nº1)", med("Horas Perdidas Motivo Nº1"), None),
        ("Refugo PPM", med("Refugo PPM"), med("Refugo PPM vs Mês Anterior")),
        ("Refugo (m)", med("Refugo (m)"), None),
    ])
    wl, wr = 760, 476
    p.add("g_pareto", MARGEM, Y_R1, wl, 244, grafico(
        "lineClusteredColumnComboChart", col("Hora-Hora", "Motivo"), [med("Tempo Parado (h)")],
        "Pareto de paradas (h) e % acumulado", ordenar=med("Tempo Parado (h)"), desc=True,
        segunda=[med("% Acumulado Paradas")]))
    p.add("g_turno", MARGEM + wl + VAO, Y_R1, wr, 244, grafico(
        "clusteredColumnChart", col("Hora-Hora", "Turno"), [med("Tempo Parado (h)")],
        "Tempo parado por turno (h)", cores_turno=True))
    p.add("g_ppm", MARGEM, Y_R2, WL, 240, grafico(
        "lineChart", col("dCalendario", "AnoMês"), [med("Refugo PPM")], "Refugo PPM por mês"))
    p.add("t_motivos", MARGEM + WL + VAO, Y_R2, WR, 240, tabela(
        [col("Hora-Hora", "Motivo"), med("Tempo Parado (h)"), med("% Acumulado Paradas")],
        "Motivos de parada"))
    return p


def pg_paradas_montagem():
    p = Pagina("pg_paradas_montagem", "Paradas Montagem", FILTRO_PM())
    cabecalho(p, "Paradas da Montagem",
              [(col("Paradas_Montagem", "Turno"), "Turno", None),
               (col("Paradas_Montagem", "Celula"), "Célula", None),
               (col("Paradas_Montagem", "Motivo"), "Motivo", None)])
    kpis(p, [
        ("Total Tempo Parado (min)", med("Tempo Parado Montagem (min)"), None),
        ("Célula Gargalo", med("Célula Gargalo Montagem"), None),
        ("Motivo Mais Frequente", med("Motivo Mais Frequente Montagem"), None),
    ])
    p.add("g_motivo", MARGEM, Y_R1, WL, 494, grafico(
        "clusteredBarChart", col("Paradas_Montagem", "Motivo"), [med("Tempo Parado Montagem (min)")],
        "Minutos parados por motivo", ordenar=med("Tempo Parado Montagem (min)"), desc=True))
    p.add("g_celula", MARGEM + WL + VAO, Y_R1, WR, 494, grafico(
        "clusteredColumnChart", col("Paradas_Montagem", "Celula"), [med("Tempo Parado Montagem (min)")],
        "Minutos parados por célula", ordenar=med("Tempo Parado Montagem (min)"), desc=True))
    return p


def pg_produtividade():
    p = Pagina("pg_produtividade", "Produtividade Montagem")
    cabecalho(p, "Produtividade da Montagem",
              [(col("Producao_Montagem", "Turno"), "Turno", None),
               (col("Producao_Montagem", "Celula"), "Célula", None),
               (col("Producao_Montagem", "Status"), "Status", None)])
    kpis(p, [
        ("Início", med("Inicio em Selecionado"), None),
        ("Fim", med("Fim em Selecionado"), None),
        ("Quantidade Produzida", med("Quantidade Produzida Montagem"), None),
        ("Ordens em Andamento", med("Ordens em Andamento"), None),
    ])
    p.add("g_status", MARGEM, Y_R1, 380, 494, pizza(
        col("Producao_Montagem", "Status"), med("Quantidade Produzida Montagem"), "Quantidade por status"))
    p.add("g_celula", MARGEM + 392, Y_R1, 856, 244, grafico(
        "clusteredColumnChart", col("Producao_Montagem", "Celula"), [med("Quantidade Produzida Montagem")],
        "Quantidade produzida por célula"))
    p.add("t_ops", MARGEM + 392, Y_R2, 856, 240, tabela(
        [col("Producao_Montagem", c) for c in ("Celula", "PN", "MetaHora", "QtdProduzida", "Status", "Turno")],
        "Ordens de montagem"))
    return p


def pg_plano():
    p = Pagina("pg_plano", "Plano de Produção")
    cabecalho(p, "Plano de Produção (Hose)", [])
    kpis(p, [
        ("Meta do Mês", fp("Meta Plan"), None),
        ("Realizado (GMS)", fp("Realizado MTD"), None),
        ("Atingimento %", fp("% Atingimento Meta"), None),
        ("Em Atraso", fp("Atraso"), None),
        ("Meta Diária", fp("Meta Diaria Planejada"), None),
        ("Dias Úteis", fp("Dias Uteis Mes"), None),
    ])
    p.add("ritmo", MARGEM, Y_R1, LARG_UTIL, 56, card(fp("Status Ritmo Texto"), None, fonte=16))
    p.add("m_tipo", MARGEM, 274, LARG_UTIL, 430, matriz(
        [col("Part Number x Construction", "Tipo_Plan")],
        [fp("Meta Plan"), fp("Realizado MTD"), fp("% Atingimento Meta"), fp("Atraso")],
        "Plano por tipo de mangueira"))
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
            "baseTheme": {"name": BASE_TEMA, "reportVersionAtImport": VERSAO_IMPORT, "type": "SharedResources"},
            "customTheme": {"name": "GMS_Tema.json", "reportVersionAtImport": VERSAO_IMPORT,
                            "type": "RegisteredResources"},
        },
        "resourcePackages": [
            {"name": "SharedResources", "type": "SharedResources",
             "items": [{"name": BASE_TEMA, "path": f"BaseThemes/{BASE_TEMA}.json", "type": "BaseTheme"}]},
            {"name": "RegisteredResources", "type": "RegisteredResources", "items": [
                {"name": "GMS_Tema.json", "path": "GMS_Tema.json", "type": "CustomTheme"},
                {"name": LOGO, "path": LOGO, "type": "Image"}]},
        ],
        "settings": {"useStylableVisualContainerHeader": True, "exportDataMode": "AllowSummarized",
                     "defaultDrillFilterOtherVisuals": True, "useEnhancedTooltips": True},
    })
    base_dir = REL / "StaticResources" / "SharedResources" / "BaseThemes"
    base_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(RES / f"{BASE_TEMA}.json", base_dir / f"{BASE_TEMA}.json")
    (REL / "StaticResources" / "RegisteredResources").mkdir(parents=True, exist_ok=True)
    shutil.copy(RES / LOGO, REL / "StaticResources" / "RegisteredResources" / LOGO)
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
    paginas = [pg_visao_geral(), pg_gargalo(), pg_paradas(), pg_paradas_montagem(), pg_produtividade(), pg_plano()]
    grava(DEF / "pages" / "pages.json", {
        "$schema": f"{SCH}/pagesMetadata/1.1.0/schema.json",
        "pageOrder": [p.nome for p in paginas], "activePageName": paginas[0].nome})
    for p in paginas:
        pagina = {
            "$schema": f"{SCH}/page/2.1.0/schema.json",
            "name": p.nome, "displayName": p.titulo, "displayOption": "FitToPage",
            "height": 720, "width": 1280,
            "objects": {"background": [{"properties": {"color": cor(FUNDO), "transparency": num(0)}}]},
        }
        if p.filtros:
            pagina["filterConfig"] = {"filters": p.filtros}
        grava(DEF / "pages" / p.nome / "page.json", pagina)
        for v in p.visuais:
            grava(DEF / "pages" / p.nome / "visuals" / v["name"] / "visual.json", v)
    print("ok:", sum(len(p.visuais) for p in paginas), "visuais em", len(paginas), "paginas")


if __name__ == "__main__":
    main()
