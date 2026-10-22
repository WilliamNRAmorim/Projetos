# -*- coding: utf-8 -*-
"""Gera o projeto Power BI (PBIR) do painel GMS.

Uso:  python gerar_relatorio.py            (gera o projeto, usando layout_salvo.json)
      python gerar_relatorio.py --extrair-layout   (le o projeto salvo no Desktop e atualiza layout_salvo.json)
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
    ref = {"Entity": ent}
    if ent == "Medidas" and prop in NOMES_EXT:  # medida de relatorio: o Desktop exige Schema "extension"
        ref = {"Schema": "extension", "Entity": ent}
    return {"Measure": {"Expression": {"SourceRef": ref}, "Property": prop}}


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
# Regra: so nasce medida aqui quando o modelo nao tem (formato % e variacao vs mes anterior).
# O DAX do modelo foi lido ao vivo em 13/10/2026 (DAX query view). Padrao de mes anterior = o mesmo
# da medida "Refugo PPM vs Mes Anterior" do modelo (PREVIOUSMONTH em dCalendario[Date]).
FMT_VAR = '+0.0%;-0.0%;0.0%'
FMT_PPM = '+#,0;-#,0;0'
M = "Medidas"


def delta_mtd(medida, coluna_data, relativo=True):
    """Variacao do mes corrente (1o dia ate o ultimo dia com dado no contexto) contra o MESMO periodo
    do mes anterior. Funciona sem filtro de mes (usa o ultimo mes com dado) e com filtro (usa o mes escolhido).
    REMOVEFILTERS(dCalendario) so dentro do CALCULATE: o ultimo dia (d) ja nasce do contexto da pagina."""
    conta = "DIVIDE(a - b, b)" if relativo else "a - b"
    guarda = "NOT ISBLANK(a) && NOT ISBLANK(b)" + (" && b <> 0" if relativo else "")
    return (
        f"VAR d = CALCULATE(MAX({coluna_data})) "
        "VAR ini = DATE(YEAR(d), MONTH(d), 1) "
        f"VAR a = CALCULATE([{medida}], REMOVEFILTERS(dCalendario), DATESBETWEEN(dCalendario[Date], ini, d)) "
        f"VAR b = CALCULATE([{medida}], REMOVEFILTERS(dCalendario), "
        "DATESBETWEEN(dCalendario[Date], EDATE(ini, -1), EDATE(d, -1))) "
        f"RETURN IF(NOT ISBLANK(d) && {guarda}, {conta})"
    )


DATA_FICHA = "'ficha_producao'[DataProducao]"
DATA_HH = "'Hora-Hora'[Data]"
EXT = [
    # (nome, tipo, DAX, formato, [(entidade, medida) referenciadas])
    ("Disponibilidade", "Double", "[Disponibilidade %]", "0.0%", [(M, "Disponibilidade %")]),
    ("Tempo Parado %", "Double", "[% Tempo Parado]", "0.0%", [(M, "% Tempo Parado")]),
    ("Δ Metragem vs mês ant.", "Double", delta_mtd("Metragem Produzida", DATA_FICHA), FMT_VAR,
     [("ficha_producao", "Metragem Produzida")]),
    ("Δ Disponibilidade vs mês ant.", "Double", delta_mtd("Disponibilidade %", DATA_HH, False), FMT_VAR,
     [(M, "Disponibilidade %")]),
    ("Δ Tempo Parado vs mês ant.", "Double", delta_mtd("% Tempo Parado", DATA_HH, False), FMT_VAR,
     [(M, "% Tempo Parado")]),
    ("Δ Refugo PPM vs mês ant.", "Double", delta_mtd("Refugo PPM", DATA_FICHA, False), FMT_PPM,
     [(M, "Refugo PPM")]),
    ("Minutos Parados Montagem", "Double", "SUM(Paradas_Montagem[TempoParadoMin])", "#,0", []),
    ("Quantidade Produzida Montagem", "Double", "SUM(Producao_Montagem[QtdProduzida])", "#,0", []),
    # Tempo excedido (TE) fica FORA da parada real; este e o unico lugar onde ele aparece, separado.
    ("Minutos Excedidos Montagem", "Double",
     'CALCULATE(SUM(Paradas_Montagem[TempoParadoMin]), REMOVEFILTERS(Paradas_Montagem[Motivo]), '
     'Paradas_Montagem[Motivo] = "TE - Tempo Excedido")', "#,0", []),
    # ---- pagina Hora-Hora Trancagem: mesmas contas do rodape da tela do app (Meta, Real, Aderencia, Parado)
    ("HH Meta (m)", "Double", "SUM(fHoraHora[Meta Hora])", "#,0", []),
    # Meta dos cartoes: a grade soma 24 h (1.440 min), mas o dia util e 21h35 (1.295 min, ja sem as pausas de almoco).
    # Meta continua 100%: produzir acima dela e ganho (Aderencia passa de 100%). O grafico por hora segue com HH Meta (m).
    ("HH Meta Útil (m)", "Double", "SUM(fHoraHora[Meta Hora]) * 1295 / 1440", "#,0", []),
    ("HH Real (m)", "Double", "SUM(fHoraHora[Real. Hora])", "#,0", []),
    ("HH Aderência", "Double", "DIVIDE(SUM(fHoraHora[Real. Hora]), [HH Meta Útil (m)])", "0%", [(M, "HH Meta Útil (m)")]),
    ("HH Parado (min)", "Double", "SUM(fHoraHora[Tempo Parado (min)])", "#,0", []),
    ("HH Principal Parada", "Text",
     "VAR t = ADDCOLUMNS(FILTER(VALUES(fHoraHora[Motivo Padrão]), NOT ISBLANK(fHoraHora[Motivo Padrão])), "
     "\"MinParado\", CALCULATE(SUM(fHoraHora[Tempo Parado (min)]))) "
     "VAR topo = TOPN(1, FILTER(t, [MinParado] > 0), [MinParado], DESC) "
     "RETURN IF(COUNTROWS(topo) = 0, \"Sem parada\", MAXX(topo, fHoraHora[Motivo Padrão]))", None, []),
]
NOMES_EXT = {e[0] for e in EXT}


# ---- infraestrutura -------------------------------------------------------
# Layout salvo no Desktop em 20/10/2026 (filtros cabem): norma, nao reposicionar. Regerar com extracao do projeto.
LAYOUT_SALVO = json.loads((RAIZ / "layout_salvo.json").read_text(encoding="utf-8"))


class Pagina:
    def __init__(self, nome, titulo, filtros=None):
        self.nome, self.titulo, self.filtros = nome, titulo, filtros or []
        self.visuais, self.z = [], 0

    def add(self, nome, x, y, w, h, visual):
        self.z += 1
        pos = {"x": x, "y": y, "z": self.z, "height": h, "width": w, "tabOrder": self.z}
        pos.update(LAYOUT_SALVO.get(self.nome, {}).get(nome, {}))  # posicao salva pelo William no Desktop vence
        filtros = visual.pop("filterConfig", None)  # filterConfig fica no container, nao dentro de "visual"
        cont = {
            "$schema": f"{SCH}/visualContainer/2.14.0/schema.json",
            "name": nome,
            "position": pos,
            "visual": visual,
        }
        if filtros:
            cont["filterConfig"] = filtros
        self.visuais.append(cont)


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


def filtro_incluir(ent, prop, valores, alias, nome):
    """Filtro de pagina 'somente estes valores'."""
    return {
        "name": nome, "field": col(ent, prop), "type": "Categorical",
        "filter": {"Version": 2, "From": [{"Name": alias, "Entity": ent, "Type": 0}],
                   "Where": [{"Condition": {"In": {
                       "Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": alias}}, "Property": prop}}],
                       "Values": [[{"Literal": {"Value": "'" + v + "'"}}] for v in valores]}}}]},
        "howCreated": "User",
    }


TRANCADEIRAS = ["TH01", "TH02", "TH03", "TH05", "TH06", "TH07", "Spiral"]


FILTRO_HH = lambda: [filtro_excluir("Hora-Hora", "Motivo Padrão", ["Almoço"], "h", "f_refeicao_hh")]
FILTRO_PM = lambda: [filtro_excluir("Paradas_Montagem", "Motivo",
                                    ["RF - Refeição", "TE - Tempo Excedido"], "p", "f_refeicao_excedido_pm")]


def container(titulo=None, fundo=True, tam_titulo=11, cor_titulo=ARDOSIA, pad=(6, 6, 10, 10)):
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
    o["padding"] = [{"properties": {"top": num(pad[0]), "bottom": num(pad[1]),
                                    "left": num(pad[2]), "right": num(pad[3])}}]
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
            "categoryLabels": [{"properties": {"show": boo(False)}}],  # rotulo de categoria bugava (decisao 20/10)
        },
        "visualContainerObjects": container(None),
        "drillFilterOtherVisuals": True,
    }


def slicer(campo, titulo, sync=None, unico=False, modo="Dropdown"):
    """Slicer com titulo visivel e dropdown legivel (altura 46); cabecalho de ferramentas oculto."""
    vc = container(titulo, tam_titulo=9, pad=(2, 2, 8, 8))
    vc["visualHeader"] = [{"properties": {"show": boo(False)}}]
    v = {
        "visualType": "slicer",
        "query": {"queryState": {"Values": {"projections": [proj(campo, True)]}}},
        "objects": {
            "data": [{"properties": {"mode": txt(modo)}}],
            "header": [{"properties": {"show": boo(False)}}],
            "items": [{"properties": {"fontSize": num(10)}}],
            **({"selection": [{"properties": {"strictSingleSelect": boo(True)}}]} if unico else {}),
        },
        "visualContainerObjects": vc,
        "drillFilterOtherVisuals": True,
    }
    if sync:
        v["syncGroup"] = {"groupName": sync, "fieldChanges": True, "filterChanges": True}
    return v


def filtro_nao_vazio(campo, nome):
    """Visual sem a categoria '(Em branco)' (fatos sem data)."""
    k = "Column"
    ent, prop = campo[k]["Expression"]["SourceRef"]["Entity"], campo[k]["Property"]
    return {"name": nome, "field": campo, "type": "Advanced",
            "filter": {"Version": 2, "From": [{"Name": "c", "Entity": ent, "Type": 0}],
                       "Where": [{"Condition": {"Not": {"Expression": {"Comparison": {
                           "ComparisonKind": 0,
                           "Left": {"Column": {"Expression": {"SourceRef": {"Source": "c"}}, "Property": prop}},
                           "Right": {"Literal": {"Value": "null"}}}}}}}]}}


def grafico(tipo, categoria, valores, titulo, ordenar=None, desc=False, segunda=None, legenda=False,
            cores_turno=None, sem_vazio=False, categorico=False):
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
    if categorico:  # eixo por categoria: um ponto por dia/valor, sem escala de tempo (sem horas)
        obj["categoryAxis"][0]["properties"]["axisType"] = txt("Categorical")
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
    if sem_vazio:
        v["filterConfig"] = {"filters": [filtro_nao_vazio(categoria, "f_sem_vazio")]}
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


def cabecalho(p, titulo, slicers, larg_seg=168):
    """Faixa vermelha com titulo/logo, navegador entre paginas e ate 3 slicers (cada um com sua largura)."""
    p.add("faixa", 0, 0, 1280, 48, faixa(VERMELHO))
    p.add("titulo", MARGEM, 4, 720, 40, caixa_texto(f"GMS · {titulo}", 16))
    p.add("atualizado", 760, 8, 330, 32,
          card(med("Dado Atualizado até"), None, fonte=11, cor_valor=BRANCO, fundo=False))
    p.add("logo", 1100, 0, 180, 48, logo())
    larguras = [(sl[4] if len(sl) > 4 else larg_seg) for sl in slicers]
    ocupado = sum(larguras) + VAO * len(slicers)
    p.add("nav", MARGEM, 52, LARG_UTIL - ocupado, 46, navegador())
    x = W_PAG - MARGEM
    for i, (sl, larg) in enumerate(reversed(list(zip(slicers, larguras)))):
        x -= larg
        campo, rotulo, sync, unico = sl[:4]
        modo = sl[5] if len(sl) > 5 else "Dropdown"
        p.add(f"seg{i}", x, 52, larg, 46, slicer(campo, rotulo, sync, unico, modo))
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


SEG_MES = (col("dCalendario", "Date"), "Período", "gms_data", False, 250, "Between")
WL, WR = 626, 610
FT = lambda prop: med(prop, "fFluxoEtapas")
ET = lambda prop: med(prop, "Etapas")
PM = lambda prop: med(prop, "Producao_Montagem")


def pg_visao_geral():
    p = Pagina("pg_visao_geral", "Visão Geral", FILTRO_HH())
    cabecalho(p, "Visão Geral da Produção", [SEG_MES])
    kpis(p, [
        ("Metragem Produzida", fp("Metragem Produzida"), med("Δ Metragem vs mês ant.")),
        ("Mangueiras Produzidas", fp("Qtd Mangueiras Produzidas"), None),
        ("Disponibilidade", med("Disponibilidade %"), med("Δ Disponibilidade vs mês ant.")),
        ("Tempo Parado", med("Tempo Parado %"), med("Δ Tempo Parado vs mês ant.")),
        ("Refugo PPM", med("Refugo PPM"), med("Δ Refugo PPM vs mês ant.")),
        ("OPs Ativas", fp("OPs Ativas"), None),
    ])
    p.add("g_tendencia", MARGEM, Y_R1, WL, 244, grafico(
        "lineChart", col("dCalendario", "Date"), [fp("Metragem Produzida")], "Metragem produzida por dia",
        categorico=True))
    p.add("g_etapa", MARGEM + WL + VAO, Y_R1, WR, 244, grafico(
        "clusteredBarChart", col("Etapas", "Etapa"), [ET("Realizado Etapa"), ET("Planejado Etapa")],
        "Realizado × planejado por etapa (m)", ordenar=col("Etapas", "OrdemEtapa"), legenda=True))
    p.add("g_motivo", MARGEM, Y_R2, WL, 240, grafico(
        "clusteredBarChart", col("Hora-Hora", "Motivo Padrão"), [med("Tempo Parado (h)")],
        "Motivos de parada por tempo (h)", ordenar=med("Tempo Parado (h)"), desc=True))
    p.add("g_ppm", MARGEM + WL + VAO, Y_R2, WR, 240, grafico(
        "lineChart", col("dCalendario", "Mês Nº"), [med("Refugo PPM")], "Refugo PPM por mês (nº do mês)",
        sem_vazio=True))
    return p


def pg_gargalo():
    p = Pagina("pg_gargalo", "Gargalo e Fluxo", FILTRO_HH())
    cabecalho(p, "Gargalo e Fluxo", [SEG_MES, (col("Hora-Hora", "Célula"), "Célula", "gms_celula", False)])
    kpis(p, [
        ("Etapa Gargalo (maior fila)", FT("Etapa Gargalo"), None),
        ("Eficiência de Fluxo", FT("Eficiencia de Fluxo"), None),
        ("Lead Total por Ficha (h)", FT("Lead Total por Ficha (h)"), None),
        ("Célula com mais Parada", med("Célula Gargalo"), None),
        ("Turnos-Célula Ativos", med("Turnos-Célula Ativos"), None),
    ])
    p.add("g_fluxo", MARGEM, Y_R1, WL, 244, grafico(
        "barChart", col("fFluxoEtapas", "Etapa"), [FT("Fila Media (h)"), FT("Proc Media (h)")],
        "Fila + processamento médios por etapa (h)", ordenar=col("fFluxoEtapas", "Ordem_Etapa"), legenda=True))
    p.add("g_razao", MARGEM + WL + VAO, Y_R1, WR, 244, grafico(
        "clusteredBarChart", col("fFluxoEtapas", "Etapa"), [FT("Razao Fila-Processo")],
        "Quantas vezes a fila supera o processamento", ordenar=col("fFluxoEtapas", "Ordem_Etapa")))
    p.add("g_prod_cel", MARGEM, Y_R2, WL, 240, grafico(
        "clusteredColumnChart", col("Hora-Hora", "Célula"), [med("Produtividade da Célula (m/h)")],
        "Produtividade por célula (m/h)", ordenar=med("Produtividade da Célula (m/h)"), desc=True))
    p.add("t_fluxo", MARGEM + WL + VAO, Y_R2, WR, 240, tabela(
        [col("fFluxoEtapas", "Etapa"), FT("Fila Mediana (h)"), FT("Proc Mediana (h)"),
         FT("Lead Mediana (h)"), FT("Fila P90 (h)")], "Fluxo por etapa (medianas)"))
    return p


def pg_paradas():
    p = Pagina("pg_paradas", "Paradas", FILTRO_HH())
    cabecalho(p, "Paradas e Qualidade (Mangueira)",
              [SEG_MES, (col("Hora-Hora", "Turno"), "Turno", "gms_turno", False),
               (col("Hora-Hora", "Motivo Padrão"), "Motivo", None, False, 200)])
    kpis(p, [
        ("Tempo Parado (h)", med("Tempo Parado (h)"), None),
        ("Tempo Parado", med("Tempo Parado %"), med("Δ Tempo Parado vs mês ant.")),
        ("Motivo Nº1", med("Motivo Nº1"), None),
        ("Horas Perdidas (Motivo Nº1)", med("Horas Perdidas Motivo Nº1"), None),
        ("Refugo PPM", med("Refugo PPM"), med("Δ Refugo PPM vs mês ant.")),
        ("Refugo (m)", med("Refugo (m)"), None),
    ])
    wl, wr = 760, 476
    p.add("g_pareto", MARGEM, Y_R1, wl, 244, grafico(
        "lineClusteredColumnComboChart", col("Hora-Hora", "Motivo Padrão"), [med("Tempo Parado (h)")],
        "Pareto de paradas (h) e % acumulado", ordenar=med("Tempo Parado (h)"), desc=True,
        segunda=[med("% Acumulado Paradas")]))
    p.add("g_turno", MARGEM + wl + VAO, Y_R1, wr, 244, grafico(
        "clusteredColumnChart", col("Hora-Hora", "Turno"), [med("Tempo Parado (h)")],
        "Tempo parado por turno (h)", cores_turno=True))
    p.add("g_pareto_ref", MARGEM, Y_R2, WL, 240, grafico(
        "lineClusteredColumnComboChart", col("TiposErros", "CodigoErro"), [med("Refugo (m)")],
        "Pareto de refugo (m) e % acumulado", ordenar=med("Refugo (m)"), desc=True,
        segunda=[med("% Acumulado Refugo")]))
    p.add("g_tipo", MARGEM + WL + VAO, Y_R2, WR, 240, grafico(
        "clusteredBarChart", col("dMotivoParada", "Tipo"), [med("Tempo Parado (h)")],
        "Tempo parado por tipo (falha × programada × material…)", ordenar=med("Tempo Parado (h)"), desc=True))
    return p


def pg_horahora():
    """Hora-Hora de UMA trancadeira por vez: producao por hora (esq.), motivos (dir.), 5 cartoes."""
    p = Pagina("pg_horahora", "Hora-Hora Trançagem",
               [filtro_excluir("fHoraHora", "Motivo Padrão", ["Almoço"], "h", "f_refeicao_hh")] + [filtro_incluir("fHoraHora", "Célula", TRANCADEIRAS, "c", "f_trancadeiras")])
    cabecalho(p, "Hora-Hora · Trançagem",
              [SEG_MES, (col("fHoraHora", "Turno"), "Turno", "gms_turno_hh", False),
               (col("fHoraHora", "Célula"), "Máquina", "gms_maquina_hh", True, 150)])
    kpis(p, [
        ("Meta (m)", med("HH Meta Útil (m)"), None),
        ("Real (m)", med("HH Real (m)"), None),
        ("Aderência", med("HH Aderência"), None),
        ("Parado (min)", med("HH Parado (min)"), None),
        ("Principal parada", med("HH Principal Parada"), None),
    ])
    wl, wr = 760, 476
    alt = 720 - MARGEM - Y_R1
    p.add("g_prod_hora", MARGEM, Y_R1, wl, alt, grafico(
        "lineClusteredColumnComboChart", col("fHoraHora", "Hora"), [med("HH Real (m)")],
        "Produção por hora (m): Real × Meta", ordenar=col("fHoraHora", "Hora"),
        segunda=[med("HH Meta (m)")], legenda=True, categorico=True))
    p.add("g_motivo", MARGEM + wl + VAO, Y_R1, wr, 290, grafico(
        "clusteredBarChart", col("fHoraHora", "Motivo Padrão"), [med("HH Parado (min)")],
        "Motivos de parada (min)", ordenar=med("HH Parado (min)"), desc=True, sem_vazio=True))
    p.add("g_motivo2", MARGEM + wl + VAO, Y_R1 + 290 + VAO, wr, alt - 290 - VAO, grafico(
        "clusteredBarChart", col("fHoraHora", "Motivo 2 Padrão"), [med("HH Parado (min)")],
        "2º motivo (min)", ordenar=med("HH Parado (min)"), desc=True, sem_vazio=True))
    return p


def pg_paradas_montagem():
    p = Pagina("pg_paradas_montagem", "Paradas Mont.", FILTRO_PM())
    cabecalho(p, "Paradas da Montagem",
              [(col("Paradas_Montagem", "Turno"), "Turno", None, False),
               (col("Paradas_Montagem", "Celula"), "Célula", None, False),
               (col("Paradas_Montagem", "Motivo"), "Motivo", None, False)])
    kpis(p, [
        ("Minutos Parados (parada real)", med("Minutos Parados Montagem"), None),
        ("Horas Paradas", med("Horas Decimais Montagem"), None),
        ("Célula Gargalo", med("Célula Gargalo Montagem"), None),
        ("Motivo Mais Frequente", med("Motivo Mais Frequente Montagem"), None),
        ("Tempo Excedido (min) — fora da parada", med("Minutos Excedidos Montagem"), None),
    ])
    p.add("g_motivo", MARGEM, Y_R1, WL, 494, grafico(
        "clusteredBarChart", col("Paradas_Montagem", "Motivo"), [med("Minutos Parados Montagem")],
        "Minutos parados por motivo", ordenar=med("Minutos Parados Montagem"), desc=True))
    p.add("g_celula", MARGEM + WL + VAO, Y_R1, WR, 494, grafico(
        "clusteredColumnChart", col("Paradas_Montagem", "Celula"), [med("Minutos Parados Montagem")],
        "Minutos parados por célula", ordenar=med("Minutos Parados Montagem"), desc=True))
    return p


def pg_extrusora():
    """Extrusora de Mandril: producao (m) e refugo (kg). Unidades diferentes: nunca somadas nem em % sobre metros.
    As duas listas nao tem relacionamento com dCalendario; as medidas fazem a data virtual (INT do datetime),
    entao o slicer de periodo vale para todos os visuais."""
    p = Pagina("pg_extrusora", "Extrusora")
    cabecalho(p, "Extrusora de Mandril (produção e refugo)", [SEG_MES])
    EX = lambda prop: med(prop, "ControleExtrusora_estrutura")
    kpis(p, [
        ("Metros Extrudados", EX("Qtd Extrusora Mandril"), None),
        ("Extrusões (carretéis)", EX("Extrusoes Mandril"), None),
        ("Metros por Dia com Extrusão", EX("Metros por Dia Extrusora"), None),
        ("Refugo (kg)", EX("Refugo Extrusora Mandril"), None),
        ("Refugo kg por 1.000 m", EX("Refugo kg por 1000 m"), None),
    ])
    p.add("g_dia", MARGEM, Y_R1, WL, 244, grafico(
        "lineChart", col("dCalendario", "Date"), [EX("Qtd Extrusora Mandril")], "Metros extrudados por dia",
        categorico=True))
    p.add("g_bitola", MARGEM + WL + VAO, Y_R1, WR, 244, grafico(
        "clusteredColumnChart", col("ControleExtrusora_estrutura", "Bitola"), [EX("Qtd Extrusora Mandril")],
        "Metros extrudados por bitola", categorico=True))
    p.add("g_turno", MARGEM, Y_R2, 400, 240, grafico(
        "clusteredColumnChart", col("ControleExtrusora_estrutura", "Turno"), [EX("Qtd Extrusora Mandril")],
        "Metros extrudados por turno", cores_turno=True))
    p.add("g_ref_causa", MARGEM + 412, Y_R2, 420, 240, grafico(
        "clusteredBarChart", col("RefugoExtrusora_Mandril", "CodigoErro"), [EX("Refugo Extrusora Mandril")],
        "Refugo (kg) por tipo de erro", ordenar=EX("Refugo Extrusora Mandril"), desc=True))
    p.add("g_ref_dia", MARGEM + 844, Y_R2, 392, 240, grafico(
        "lineChart", col("dCalendario", "Date"), [EX("Refugo Extrusora Mandril")], "Refugo (kg) por dia", categorico=True))
    return p


# ---- gravacao ------------------------------------------------------------
def grava(caminho, obj):
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    platform = (REL / ".platform").read_bytes() if (REL / ".platform").exists() else None
    if REL.exists():
        shutil.rmtree(REL)
    if platform:  # id do item criado pelo Desktop: nao perder
        REL.mkdir(parents=True)
        (REL / ".platform").write_bytes(platform)
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
            dict({"name": n, "dataType": t, "expression": e, **({"formatString": f} if f else {}),
                  "displayFolder": "Painel (relatório)"},
                 **({"references": {"measures": [{"entity": en, "name": nm} for en, nm in refs]}} if refs else {}))
            for n, t, e, f, refs in EXT]}],
    })
    paginas = [pg_visao_geral(), pg_gargalo(), pg_paradas(), pg_horahora(), pg_paradas_montagem(), pg_extrusora()]
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


def extrair_layout():
    """Le posicao/tamanho de cada visual do projeto salvo e grava layout_salvo.json (nao gera nada)."""
    out = {}
    for f in sorted((DEF / "pages").glob("*/visuals/*/visual.json")):
        out.setdefault(f.parts[-4], {})[f.parts[-2]] = json.loads(f.read_text(encoding="utf-8"))["position"]
    (RAIZ / "layout_salvo.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("layout_salvo.json atualizado:", {k: len(v) for k, v in out.items()})


if __name__ == "__main__":
    import sys
    extrair_layout() if "--extrair-layout" in sys.argv else main()
