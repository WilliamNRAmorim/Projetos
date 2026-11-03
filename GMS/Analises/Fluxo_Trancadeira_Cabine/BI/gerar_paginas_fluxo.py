# -*- coding: utf-8 -*-
"""Gera as 2 paginas-piloto "Fluxo Trancagem -> Cabine" (PBIR) dentro de um relatorio existente.

Uso:
    python gerar_paginas_fluxo.py [CAMINHO_DO_.Report]          (gera e valida)
    python gerar_paginas_fluxo.py [CAMINHO_DO_.Report] --validar (so valida, nao grava)

Padrao do caminho: GMS/PowerBI/Modelo_PBIP_teste/GMS_Modelo.Report (copia local de teste).
Idempotente: apaga e recria so pages/pg_fluxo_1 e pages/pg_fluxo_2 e poe as 2 no fim do pages.json
(sem mudar a pagina ativa). NAO mexe no report.json nem no tema do relatorio (William, 03/11/2026): as 2 paginas
sao claras e autossuficientes, com fundo no page.json e cores em hex em cada visual.
Recusa gravar fora de uma pasta *_teste sem --forcar (o GMS_Painel e o snapshot Modelo_PBIP nao podem mudar).

Layout, campos e formatacao: LEIAME_Pagina.md (secoes 3 e 5). Nomes de medidas/colunas: TMDL da copia.
Validacao (sempre roda no fim): JSON valido, Entity/Property existem no modelo do definition.pbir,
nomes de visual unicos por pagina, posicao dentro de 1280x720 e nenhuma sobreposicao.
"""
import argparse
import json
import re
import shutil
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ_GMS = AQUI.parents[2]  # .../GMS
PADRAO_REL = RAIZ_GMS / "PowerBI" / "Modelo_PBIP_teste" / "GMS_Modelo.Report"
TEMA_ESCURO = "Tema_FluxoTrancagem.json"  # tema escuro do piloto: nao e mais registrado (a validacao confere)

SCH = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition"
V_VISUAL = "2.14.0"   # mesma do gerar_relatorio.py (aberta e salva pelo Desktop no GMS_Painel)
V_PAGE = "2.1.0"

PAGINAS = ("pg_fluxo_1", "pg_fluxo_2")
W_PAG, H_PAG = 1280, 720

# Paleta clara do piloto (referencia: Tema_FluxoTrancagem_Claro.json), em hex em cada visual, porque as paginas nao
# dependem do tema do relatorio. Contraste sobre o branco: texto 18,6:1, secundario 7,7:1 (7,1:1 no fundo da
# pagina); azul 4,4:1, verde 3,4:1 e laranja 3,2:1 so como serie, barra e borda.
HEX_TINTA, HEX_SUAVE, HEX_CARTAO = "#14130F", "#55534D", "#FFFFFF"
HEX_PAGINA, HEX_BORDA = "#F6F5F2", "#E1E0D9"
HEX_AZUL, HEX_LARANJA, HEX_VERDE = "#2A78D6", "#EB6834", "#0CA30C"
HEX_SELECAO = "#D6E4F7"  # botao ativo do navegador: texto escuro a 14:1
MARGEM = 16  # margem minima do canvas (William, 03/11)

M = "Medidas"


# ---- expressoes -----------------------------------------------------------
def lit(v):
    return {"expr": {"Literal": {"Value": v}}}


def txt(s):
    return lit("'" + s.replace("'", "''") + "'")


def num(n):
    return lit(f"{n}D")


def inteiro(n):
    return lit(f"{n}L")


def boo(b):
    return lit("true" if b else "false")


def cor_hex(h):
    return {"solid": {"color": txt(h)}}


def col(ent, prop):
    return {"Column": {"Expression": {"SourceRef": {"Entity": ent}}, "Property": prop}}


def med(prop, ent=M):
    return {"Measure": {"Expression": {"SourceRef": {"Entity": ent}}, "Property": prop}}


def chave(campo):
    k = "Column" if "Column" in campo else "Measure"
    return k, campo[k]["Expression"]["SourceRef"]["Entity"], campo[k]["Property"]


def qref(campo):
    _, e, p = chave(campo)
    return f"{e}.{p}"


def proj(campo, rotulo=None, ativo=False, formato=None):
    _, e, p = chave(campo)
    d = {"field": campo, "queryRef": f"{e}.{p}", "nativeQueryRef": rotulo or p}
    if rotulo:
        d["displayName"] = rotulo
    if formato:  # cadeia de formato so deste visual (RoleProjection.format)
        d["format"] = formato
    if ativo:
        d["active"] = True
    return d


def titulo_fx(medida):
    """Titulo do visual por formatacao condicional (fx -> Valor do campo)."""
    return {"expr": {"Measure": {"Expression": {"SourceRef": {"Entity": M}}, "Property": medida}}}


def caixa(titulo=None, fundo=True, alt=None, pad=None, titulo_expr=None, tam_titulo=None):
    """visualContainerObjects com a paleta clara explicita: cartao branco, borda fina, titulo escuro."""
    o = {}
    if titulo_expr is not None:
        o["title"] = [{"properties": {"show": boo(True), "text": titulo_expr}}]
    elif titulo:
        o["title"] = [{"properties": {"show": boo(True), "text": txt(titulo)}}]
    else:
        o["title"] = [{"properties": {"show": boo(False)}}]
    if titulo or titulo_expr is not None:
        o["title"][0]["properties"].update({"fontColor": cor_hex(HEX_TINTA), "fontFamily": txt("Segoe UI Semibold"),
                                            "fontSize": num(tam_titulo or 12), "alignment": txt("left")})
    if pad is None and fundo:
        pad = (12, 12, 14, 14)
    if pad is not None and not isinstance(pad, tuple):
        pad = (pad, pad, pad, pad)
    if fundo:
        o["background"] = [{"properties": {"show": boo(True), "color": cor_hex(HEX_CARTAO), "transparency": num(0)}}]
        o["border"] = [{"properties": {"show": boo(True), "color": cor_hex(HEX_BORDA), "radius": num(12),
                                       "width": num(1)}}]
    else:
        o["background"] = [{"properties": {"show": boo(False)}}]
        o["border"] = [{"properties": {"show": boo(False)}}]
    o["dropShadow"] = [{"properties": {"show": boo(False)}}]
    if pad is not None:
        o["padding"] = [{"properties": {"top": num(pad[0]), "bottom": num(pad[1]),
                                        "left": num(pad[2]), "right": num(pad[3])}}]
    if alt:
        o["general"] = [{"properties": {"altText": txt(alt)}}]
    return o


def filtro_verdadeiro(ent, prop, nome):
    return {
        "name": nome, "field": col(ent, prop), "type": "Categorical",
        "filter": {"Version": 2, "From": [{"Name": "e", "Entity": ent, "Type": 0}],
                   "Where": [{"Condition": {"In": {
                       "Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "e"}}, "Property": prop}}],
                       "Values": [[{"Literal": {"Value": "true"}}]]}}}]},
        "howCreated": "User",
    }


def filtro_nao_vazio(campo, nome):
    """Sem '(Em branco)' na segmentacao (regra do William de 26/10/2026, igual ao gerar_relatorio.py)."""
    _, ent, prop = chave(campo)
    return {"name": nome, "field": campo, "type": "Advanced",
            "filter": {"Version": 2, "From": [{"Name": "c", "Entity": ent, "Type": 0}],
                       "Where": [{"Condition": {"Not": {"Expression": {"Comparison": {
                           "ComparisonKind": 0,
                           "Left": {"Column": {"Expression": {"SourceRef": {"Source": "c"}}, "Property": prop}},
                           "Right": {"Literal": {"Value": "null"}}}}}}}]}}


def ordenar(campo, desc=False):
    return {"sort": [{"field": campo, "direction": "Descending" if desc else "Ascending"}], "isDefaultSort": False}


# ---- visuais ---------------------------------------------------------------
# Regras de encaixe (William, 03/11): margem minima de 16 px e conjunto simetrico; nada passa de 1280x720;
# nenhuma rolagem interna; nenhum texto com reticencias; ~10% de folga nas larguras de texto.
def v_texto(linhas, alt=None):
    """linhas = [(texto, tamanho_pt, fonte, hex)] -> um paragrafo por linha. Sem fundo e sem borda."""
    pars = [{"textRuns": [{"value": t, "textStyle": {"fontFamily": f, "fontSize": f"{s}pt", "color": c}}]}
            for t, s, f, c in linhas]
    return {"visualType": "textbox",
            "objects": {"general": [{"properties": {"paragraphs": pars}}]},
            "visualContainerObjects": caixa(None, fundo=False, alt=alt, pad=0),
            "drillFilterOtherVisuals": True}


def v_segmentacao(campo, rotulo, grupo):
    """Lista suspensa, cabecalho ligado, selecao multipla, 'Selecionar tudo' ligado, sincronizada por grupo.
    Padding do container pequeno (o do tema, 12/14, cortava a caixa 'Todos' em 56 px de altura)."""
    vc = caixa(None, pad=(4, 4, 8, 8))
    vc["visualHeader"] = [{"properties": {"show": boo(False)}}]
    return {
        "visualType": "slicer",
        "query": {"queryState": {"Values": {"projections": [proj(campo, rotulo, ativo=True)]}}},
        "objects": {
            "data": [{"properties": {"mode": txt("Dropdown")}}],
            "header": [{"properties": {"show": boo(True), "text": txt(rotulo), "fontColor": cor_hex(HEX_SUAVE),
                                       "textSize": num(9), "fontFamily": txt("Segoe UI")}}],
            "items": [{"properties": {"textSize": num(10), "fontFamily": txt("Segoe UI"),
                                      "fontColor": cor_hex(HEX_TINTA), "background": cor_hex(HEX_CARTAO)}}],
            "selection": [{"properties": {"singleSelect": boo(False), "strictSingleSelect": boo(False),
                                          "selectAllCheckboxEnabled": boo(True)}}],
        },
        "visualContainerObjects": vc,
        "syncGroup": {"groupName": grupo, "fieldChanges": True, "filterChanges": True},
        "filterConfig": {"filters": [filtro_nao_vazio(campo, "f_sem_vazio_seg")]},
        "drillFilterOtherVisuals": True,
    }


def v_carimbo():
    return {
        "visualType": "card",
        "query": {"queryState": {"Values": {"projections": [proj(med("Dado Atualizado até"))]}}},
        "objects": {
            "labels": [{"properties": {"fontSize": num(9), "color": cor_hex(HEX_SUAVE),
                                       "fontFamily": txt("Segoe UI")}}],
            "categoryLabels": [{"properties": {"show": boo(False)}}],
        },
        "visualContainerObjects": caixa(None, fundo=False, pad=0,
                                        alt="Data e hora do último dado carregado no modelo."),
        "drillFilterOtherVisuals": True,
    }


def v_navegador(outras_paginas):
    """Navegador de pagina com as outras paginas do relatorio desligadas (so as 2 do piloto)."""
    obj = {
        "text": [{"properties": {"fontSize": num(9), "fontFamily": txt("Segoe UI"), "fontColor": cor_hex(HEX_SUAVE)},
                  "selector": {"id": "default"}},
                 {"properties": {"fontColor": cor_hex(HEX_TINTA), "bold": boo(True)}, "selector": {"id": "selected"}}],
        "fill": [{"properties": {"show": boo(True), "fillColor": cor_hex(HEX_CARTAO), "transparency": num(0)},
                  "selector": {"id": "default"}},
                 {"properties": {"fillColor": cor_hex(HEX_SELECAO)}, "selector": {"id": "selected"}}],
        "outline": [{"properties": {"show": boo(True), "lineColor": cor_hex(HEX_BORDA), "weight": num(1)},
                     "selector": {"id": "default"}}],
        "pages": [{"properties": {"showPage": boo(False)}, "selector": {"id": p}} for p in outras_paginas],
    }
    return {"visualType": "pageNavigator", "objects": obj,
            "visualContainerObjects": caixa(None, fundo=False, pad=0,
                                            alt="Navegação entre as 2 páginas do piloto."),
            "drillFilterOtherVisuals": True}


# (medida, rotulo no cartao, formato so deste visual). Rotulo = displayName da projecao (a medida nao muda).
# Rotulos curtos (03/11, conferido no Desktop: com 18-19 caracteres saiam reticencias). Texto longo no LEIAME 5.3.
KPIS = [
    ("Vazão Cabine (m/dia)", "m/dia cabine", "#,0"),
    ("Pessoas por Dia no Trecho", "pessoas no trecho", "#,0.0"),
    ("Pessoas Trançagem / Cabine", "pessoas tranç./cab.", None),
    ("m por Pessoa Cabine", "m/pessoa cabine", "#,0"),
    ("Eficiência de Balanceamento", "eficiência", "0%"),
    ("Lead Time Tranç→Cabine (h)", "lead time", '#,0 "h"'),
    ("WIP Little (m)", "em processo", '#,0 "m"'),
    ("CV Vazão Trançagem", "CV vazão", "0.0%"),
    ("Rendimento de Fluxo", "rendimento", "0%"),
]
KPI_TEXTO_LONGO = "Pessoas Trançagem / Cabine"  # valor "6,8 / 5,0": fonte menor para nao cortar


def v_kpis():
    """Cartao novo (cardVisual) com as 9 medidas lado a lado (maxTiles 9), unidades de exibicao = Nenhuma."""
    sel = {"id": "default"}
    return {
        "visualType": "cardVisual",
        "query": {"queryState": {"Data": {"projections": [proj(med(m), r, formato=f) for m, r, f in KPIS]}}},
        "objects": {
            "layout": [
                {"properties": {"maxTiles": inteiro(len(KPIS))}},
                {"properties": {"backgroundShow": boo(False), "cellPadding": inteiro(4),
                                "paddingUniform": inteiro(4)}, "selector": sel},
            ],
            "value": [
                {"properties": {"fontSize": num(20), "fontFamily": txt("Segoe UI Semibold"),
                                "fontColor": cor_hex(HEX_TINTA), "displayUnits": num(1),
                                "labelDisplayUnits": num(1), "valueDisplayUnits": num(1)}, "selector": sel},
                {"properties": {"fontSize": num(16)}, "selector": {"metadata": f"{M}.{KPI_TEXTO_LONGO}"}},
            ],
            "label": [{"properties": {"show": boo(True), "position": txt("belowValue"), "fontSize": num(9),
                                      "fontFamily": txt("Segoe UI"), "fontColor": cor_hex(HEX_SUAVE)},
                       "selector": sel}],
            "outline": [{"properties": {"show": boo(False)}, "selector": sel}],
        },
        "visualContainerObjects": caixa(None, pad=(6, 6, 8, 8),
                                        alt="Nove indicadores do trecho trançagem→cabine no filtro escolhido."),
        "drillFilterOtherVisuals": True,
    }


# Cartao SVG 208x304 reduzido na mesma razao: 6 x 190 = 1.140 px em 1.248 px (18 px de folga por coluna
# para o espacamento da celula, sem rolagem). A seta entre cartoes esta dentro do SVG e escala junto.
CARTAO_L, CARTAO_A = 190, 278


def v_matriz_cartoes():
    """6 cartoes SVG: dEtapa[Etapa no Fluxo] em Colunas, SVG Cartao Etapa em Valores (LEIAME 5.4).
    Sem fundo proprio: celulas e cabecalho na cor da pagina (o cartao branco com borda vem do SVG).
    Cabecalho de coluna escondido: fonte 1, cor da fonte e fundo = cor da pagina."""
    etapa = col("dEtapa", "Etapa no Fluxo")
    vc = caixa(None, fundo=False, pad=0, titulo_expr=titulo_fx("Título Cartões"), tam_titulo=12,
               alt="Seis cartões, da trançagem à cabine: pessoas por dia, metros por dia e pessoas a cada "
                   "1.000 m de cada etapa.")
    return {
        "visualType": "pivotTable",
        "query": {"queryState": {"Columns": {"projections": [proj(etapa, ativo=True)]},
                                 "Values": {"projections": [proj(med("SVG Cartão Etapa"))]}},
                  "sortDefinition": ordenar(etapa)},
        "objects": {
            "subTotals": [{"properties": {"rowSubtotals": boo(False), "columnSubtotals": boo(False)}}],
            "grid": [{"properties": {"gridVertical": boo(False), "gridHorizontal": boo(False),
                                     "outlineColor": cor_hex(HEX_PAGINA), "rowPadding": num(0),
                                     "imageHeight": num(CARTAO_A), "imageWidth": num(CARTAO_L)}}],
            "columnHeaders": [{"properties": {"fontSize": num(1), "fontColor": cor_hex(HEX_PAGINA),
                                              "backColor": cor_hex(HEX_PAGINA), "wordWrap": boo(False),
                                              "autoSizeColumnWidth": boo(True)}}],
            "values": [{"properties": {"backColorPrimary": cor_hex(HEX_PAGINA),
                                       "backColorSecondary": cor_hex(HEX_PAGINA)}}],
        },
        "visualContainerObjects": vc,
        "filterConfig": {"filters": [filtro_verdadeiro("dEtapa", "Trecho Tranç-Cabine", "f_trecho")]},
        "drillFilterOtherVisuals": True,
    }


VALORES_CLAROS = {"fontColorPrimary": cor_hex(HEX_TINTA), "backColorPrimary": cor_hex(HEX_CARTAO),
                  "fontColorSecondary": cor_hex(HEX_TINTA), "backColorSecondary": cor_hex(HEX_CARTAO)}
CABECALHO_CLARO = {"fontColor": cor_hex(HEX_SUAVE), "backColor": cor_hex(HEX_CARTAO), "fontFamily": txt("Segoe UI"),
                   "fontSize": num(9)}


# Barra SVG 440x32 reduzida na mesma razao para caber sem rolagem: 130 + 400 + espacamento < 588 px uteis.
CONTEUDO_L, CONTEUDO_A = 400, 29


def v_tabela_conteudo():
    etapa = col("dEtapa", "Etapa no Fluxo")
    svg = med("SVG Conteúdo")
    return {
        "visualType": "tableEx",
        "query": {"queryState": {"Values": {"projections": [proj(etapa), proj(svg, "Pessoas a cada 1.000 m")]}},
                  "sortDefinition": ordenar(etapa)},
        "objects": {
            "values": [{"properties": {"fontSize": num(11), "fontFamily": txt("Segoe UI"), **VALORES_CLAROS}}],
            "columnHeaders": [{"properties": CABECALHO_CLARO}],
            "grid": [{"properties": {"imageHeight": num(CONTEUDO_A), "imageWidth": num(CONTEUDO_L),
                                     "gridVertical": boo(False), "gridHorizontal": boo(True),
                                     "gridHorizontalColor": cor_hex(HEX_BORDA), "outlineColor": cor_hex(HEX_BORDA)}}],
            "total": [{"properties": {"totals": boo(False)}}],
            "columnWidth": [{"properties": {"value": num(130)}, "selector": {"metadata": qref(etapa)}}],
        },
        "visualContainerObjects": caixa(None, titulo_expr=titulo_fx("Título Conteúdo"), tam_titulo=12,
                                        alt="Pessoas a cada 1.000 m por etapa; laranja são as duas etapas com mais "
                                            "gente por metro; tracejado é a média."),
        "filterConfig": {"filters": [filtro_verdadeiro("dEtapa", "Trecho Tranç-Cabine", "f_trecho")]},
        "drillFilterOtherVisuals": True,
    }


def v_tabela_leitura():
    """Uma coluna, quebra de linha ligada, fonte 11 (era 12 e rolava); coluna de 556 px (folga para a barra)."""
    leitura = med("Leitura Automática")
    return {
        "visualType": "tableEx",
        "query": {"queryState": {"Values": {"projections": [proj(leitura, "Leitura automática")]}}},
        "objects": {
            "values": [{"properties": {"wordWrap": boo(True), "fontSize": num(11), "fontFamily": txt("Segoe UI"),
                                       **VALORES_CLAROS}}],
            "columnHeaders": [{"properties": CABECALHO_CLARO}],
            "grid": [{"properties": {"gridVertical": boo(False), "gridHorizontal": boo(False),
                                     "outlineColor": cor_hex(HEX_BORDA)}}],
            "total": [{"properties": {"totals": boo(False)}}],
            "columnWidth": [{"properties": {"value": num(556)}, "selector": {"metadata": qref(leitura)}}],
        },
        "visualContainerObjects": caixa(None, alt="Leitura automática do trecho: gargalo, conteúdo de mão de obra "
                                                  "e avisos do filtro escolhido."),
        "drillFilterOtherVisuals": True,
    }


# Eixo dos graficos mensais: dCalendario[AnoMes] (numero AAAAMM, ex.: 202512). E a unica coluna de mes do modelo que
# ordena certo sozinha; "Mes" ("jan".."dez") nao tem Classificar por coluna e sairia em ordem alfabetica. Rotulo curto
# "dez/25" exige coluna de texto nova no dCalendario (decisao do William; ver LEIAME secao 7).
EIXO_MES = col("dCalendario", "AnoMês")
COR_TRANC, COR_CABINE = HEX_AZUL, HEX_LARANJA  # iguais nos 2 graficos (cabine = laranja das etapas destaque)


def v_colunas(series, titulo, alt, formato, fonte_rotulo):
    """Colunas agrupadas por mes: media dos dias produtivos no mes, rotulo de dado em cada coluna, eixo Y oculto e
    sem grade (o rotulo ja da o numero), colunas largas, legenda no topo. series = [(medida, rotulo, cor)]."""
    return {
        "visualType": "clusteredColumnChart",
        "query": {"queryState": {"Category": {"projections": [proj(EIXO_MES, "Mês", ativo=True)]},
                                 "Y": {"projections": [proj(med(m), r, formato=formato) for m, r, _ in series]}},
                  "sortDefinition": ordenar(EIXO_MES)},
        "objects": {
            "categoryAxis": [{"properties": {"show": boo(True), "axisType": txt("Categorical"),
                                             "labelColor": cor_hex(HEX_SUAVE), "fontSize": num(9),
                                             "showAxisTitle": boo(False), "gridlineShow": boo(False),
                                             "innerPadding": num(8), "concatenateLabels": boo(False)}}],
            "valueAxis": [{"properties": {"show": boo(False), "start": num(0), "showAxisTitle": boo(False),
                                          "gridlineShow": boo(False)}}],
            "legend": [{"properties": {"show": boo(True), "position": txt("Top"), "labelColor": cor_hex(HEX_SUAVE),
                                       "fontSize": num(10), "showTitle": boo(False)}}],
            "labels": [{"properties": {"show": boo(True), "color": cor_hex(HEX_TINTA), "fontSize": num(fonte_rotulo),
                                       "fontFamily": txt("Segoe UI"), "labelDisplayUnits": num(1),
                                       "labelPosition": txt("OutsideEnd"), "enableBackground": boo(False)}}],
            "dataPoint": [{"properties": {"fill": cor_hex(c)}, "selector": {"metadata": f"{M}.{m}"}}
                          for m, _, c in series],
        },
        "visualContainerObjects": caixa(titulo, alt=alt, tam_titulo=12, pad=(8, 6, 8, 8)),
        "filterConfig": {"filters": [filtro_nao_vazio(EIXO_MES, "f_sem_vazio_mes")]},
        "drillFilterOtherVisuals": True,
    }


# ---- paginas ---------------------------------------------------------------
# Grade vertical (as 2 paginas): faixa 16-80, conteudo 92-660, rodape 672-704 (16 px da borda de baixo).
# Horizontal: 16 a 1264 nas 2 paginas (simetrico). Colunas da pagina 2: 16-632 e 648-1264.
LINHA2 = "Ficha de produção · dia de 05:20 a 05:20 · média dos dias com trançagem ≥ 3.000 m"
LEGENDA = ("Borda laranja = as 2 etapas com mais gente por metro · caixa verde = as demais · "
           "seta = sentido do fluxo")
RODAPE = "Pessoas = operadores distintos que apontaram a etapa no dia (estimativa, não é escala oficial)."
Y_FAIXA, H_FAIXA = 16, 64
Y_CONT = Y_FAIXA + H_FAIXA + 12          # 92
Y_RODAPE, H_RODAPE = 672, 32             # termina em 704
FIM_CONT = Y_RODAPE - 12                 # 660
SEGMENTACOES = [  # (nome, campo, rotulo, grupo de sync, x) - LEIAME 3, faixa comum
    ("seg_ano", col("dCalendario", "Ano"), "Ano", "fluxo_ano", 620),
    ("seg_mes", col("dCalendario", "Mês"), "Mês", "fluxo_mes", 784),
    ("seg_dia", col("dCalendario", "Dia"), "Dia", "fluxo_dia", 948),
    ("seg_turno", col("dTurno", "Rótulo"), "Turno", "fluxo_turno", 1112),
]


class Pagina:
    def __init__(self, nome, titulo):
        self.nome, self.titulo, self.visuais, self.z = nome, titulo, [], 0

    def add(self, nome, x, y, w, h, visual):
        self.z += 1000
        filtros = visual.pop("filterConfig", None)  # filterConfig fica no container
        c = {"$schema": f"{SCH}/visualContainer/{V_VISUAL}/schema.json", "name": nome,
             "position": {"x": x, "y": y, "z": self.z, "height": h, "width": w, "tabOrder": self.z},
             "visual": visual}
        if filtros:
            c["filterConfig"] = filtros
        self.visuais.append(c)


def faixa_comum(p, titulo1, outras_paginas):
    # Titulo 18 pt (~36 caracteres = ~380 px) e linha 2 a 10 pt (~83 caracteres = ~460 px) em 588 px: 1 linha cada.
    p.add("titulo", 16, Y_FAIXA, 588, H_FAIXA, v_texto([(titulo1, 18, "Segoe UI Semibold", HEX_TINTA),
                                                         (LINHA2, 10, "Segoe UI", HEX_SUAVE)]))
    for nome, campo, rot, grupo, x in SEGMENTACOES:
        p.add(nome, x, Y_FAIXA, 152, H_FAIXA, v_segmentacao(campo, rot, grupo))
    # Rodape ~485 px de texto a 9 pt em 576 px; navegador com 368 px (2 botoes de ~184) para "Fluxo · Mão de obra".
    p.add("rodape", 16, Y_RODAPE, 576, H_RODAPE, v_texto([(RODAPE, 9, "Segoe UI", HEX_SUAVE)]))
    p.add("nav", 608, Y_RODAPE, 368, H_RODAPE, v_navegador(outras_paginas))
    p.add("atualizado", 992, Y_RODAPE, 272, H_RODAPE, v_carimbo())


def pg_fluxo_1(outras):
    p = Pagina("pg_fluxo_1", "Fluxo · Etapas")
    faixa_comum(p, "Fluxo trançagem → cabine · etapas", outras)
    p.add("kpis", 16, Y_CONT, 1248, 104, v_kpis())                                   # 92-196
    # Cartoes ficam em 190 x 278 (200 x 292 deixaria ~8 px por coluna e pode voltar a rolar). O conteudo da
    # matriz tem ~322 px; matriz (340) + legenda (28) centralizados no vao 208-660: sobra 36 em cima e embaixo.
    y0, fim = Y_CONT + 104 + 12, FIM_CONT                                             # 208, 660
    h_m, h_l = 340, 28
    y_m = y0 + (fim - y0 - (h_m + 12 + h_l)) // 2                                     # 244
    p.add("cartoes", 16, y_m, 1248, h_m, v_matriz_cartoes())                           # 244-584
    p.add("legenda", 16, y_m + h_m + 12, 1248, h_l, v_texto([(LEGENDA, 10, "Segoe UI", HEX_SUAVE)],
                                                             alt="Legenda das cores dos cartões."))  # 596-624
    return p


def pg_fluxo_2(outras):
    p = Pagina("pg_fluxo_2", "Fluxo · Mão de obra")
    faixa_comum(p, "Fluxo trançagem → cabine · mão de obra", outras)
    h_tab = 340                                       # 92-432: leitura com 4 a 5 frases sem rolar
    y_g = Y_CONT + h_tab + 12                         # 444
    h_g = FIM_CONT - y_g                              # 216, termina em 660
    p.add("t_conteudo", 16, Y_CONT, 616, h_tab, v_tabela_conteudo())
    p.add("t_leitura", 648, Y_CONT, 616, h_tab, v_tabela_leitura())
    # Metros "6.654" a 8 pt (~26 px) cabem em colunas de ~24 px com 12 meses em 616 px so com espaco entre
    # categorias pequeno; pessoas "6,8" a 9 pt sobram.
    p.add("g_metros", 16, y_g, 616, h_g, v_colunas(
        [("Vazão Trançagem (m/dia)", "Trançagem", COR_TRANC), ("Vazão Cabine (m/dia)", "Cabine", COR_CABINE)],
        "Metros por dia · média dos dias produtivos, por mês",
        "Colunas por mês: metros por dia da trançagem e da cabine, média dos dias produtivos.", "#,0", 8))
    p.add("g_pessoas", 648, y_g, 616, h_g, v_colunas(
        [("Pessoas Trançagem (por dia)", "Trançagem", COR_TRANC), ("Pessoas Cabine (por dia)", "Cabine", COR_CABINE)],
        "Pessoas por dia · média dos dias produtivos, por mês",
        "Colunas por mês: pessoas por dia na trançagem e na cabine, média dos dias produtivos.", "#,0.0", 9))
    return p


# ---- gravacao --------------------------------------------------------------
def le(c):
    return json.loads(Path(c).read_text(encoding="utf-8-sig"))


def grava(c, obj):
    c = Path(c)
    c.parent.mkdir(parents=True, exist_ok=True)
    c.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def gera(rel):
    pages_dir = rel / "definition" / "pages"
    meta = le(pages_dir / "pages.json")
    outras = [p for p in meta.get("pageOrder", []) if p not in PAGINAS]
    for nome in PAGINAS:
        alvo = pages_dir / nome
        if alvo.exists():
            shutil.rmtree(alvo)
    paginas = [pg_fluxo_1(outras), pg_fluxo_2(outras)]
    for p in paginas:
        grava(pages_dir / p.nome / "page.json", {
            "$schema": f"{SCH}/page/{V_PAGE}/schema.json", "name": p.nome, "displayName": p.titulo,
            "displayOption": "FitToPage", "height": H_PAG, "width": W_PAG,
            # fundo claro proprio: a pagina nao depende do tema do relatorio
            "objects": {"background": [{"properties": {"color": cor_hex(HEX_PAGINA), "transparency": num(0)}}],
                        "outspace": [{"properties": {"color": cor_hex(HEX_PAGINA), "transparency": num(0)}}]}})
        for v in p.visuais:
            grava(pages_dir / p.nome / "visuals" / v["name"] / "visual.json", v)
    meta["pageOrder"] = outras + list(PAGINAS)  # pagina ativa e inicial ficam como estavam
    grava(pages_dir / "pages.json", meta)
    print("ok:", ", ".join(f"{p.nome} ({len(p.visuais)} visuais)" for p in paginas))


# ---- validacao -------------------------------------------------------------
RX_OBJ = re.compile(r"^\s*(table|column|measure)\s+('(?:[^']|'')*'|[^\s=]+)")


def nome_tmdl(s):
    return s[1:-1].replace("''", "'") if s.startswith("'") else s


def le_modelo(rel):
    """{tabela: {'column': set, 'measure': set}} a partir do TMDL do modelo apontado pelo definition.pbir."""
    pbir = le(rel / "definition.pbir")
    caminho = pbir.get("datasetReference", {}).get("byPath", {}).get("path")
    if not caminho:
        return None
    tabelas = {}
    for f in ((rel / caminho).resolve() / "definition" / "tables").glob("*.tmdl"):
        atual = None
        for linha in f.read_text(encoding="utf-8-sig").splitlines():
            m = RX_OBJ.match(linha)
            if not m:
                continue
            tipo, nome = m.group(1), nome_tmdl(m.group(2))
            if tipo == "table":
                atual = tabelas.setdefault(nome, {"column": set(), "measure": set()})
            elif atual is not None:
                atual[tipo].add(nome)
    return tabelas


def campos(o):
    """Todas as referencias Column/Measure com Entity (SourceRef.Source de filtro e ignorado)."""
    if isinstance(o, dict):
        for k in ("Column", "Measure"):
            v = o.get(k)
            if isinstance(v, dict) and "Property" in v:
                ent = v.get("Expression", {}).get("SourceRef", {}).get("Entity")
                if ent:
                    yield k, ent, v["Property"]
        for v in o.values():
            yield from campos(v)
    elif isinstance(o, list):
        for v in o:
            yield from campos(v)


def valida(rel):
    erros = []
    modelo = le_modelo(rel)
    if modelo is None:
        erros.append("definition.pbir sem byPath: nao deu para conferir os campos no TMDL")
    pages_dir = rel / "definition" / "pages"
    for arq in [rel / "definition" / "report.json", pages_dir / "pages.json"]:
        try:
            le(arq)
        except Exception as e:  # noqa: BLE001
            erros.append(f"{arq.name}: JSON invalido ({e})")
    meta = le(pages_dir / "pages.json")
    for nome in PAGINAS:
        if nome not in meta.get("pageOrder", []):
            erros.append(f"pages.json sem {nome}")
    if meta.get("pageOrder", [])[-2:] != list(PAGINAS):
        erros.append("pages.json: as 2 paginas do piloto nao estao no fim")
    if meta.get("activePageName") in PAGINAS:
        erros.append("pages.json: pagina ativa mudou para o piloto")
    r = le(rel / "definition" / "report.json")
    if r.get("themeCollection", {}).get("customTheme", {}).get("name") == TEMA_ESCURO or TEMA_ESCURO in json.dumps(r):
        erros.append("report.json: o tema escuro do piloto ainda esta registrado (o gerador nao mexe mais no tema)")
    grupos = {}
    total = 0
    for nome in PAGINAS:
        pdir = pages_dir / nome
        try:
            pg = le(pdir / "page.json")
            if pg.get("name") != nome:
                erros.append(f"{nome}/page.json: name diferente da pasta")
            if (pg.get("width"), pg.get("height"), pg.get("displayOption")) != (W_PAG, H_PAG, "FitToPage"):
                erros.append(f"{nome}/page.json: precisa de 1280x720 e FitToPage")
        except Exception as e:  # noqa: BLE001
            erros.append(f"{nome}/page.json: {e}")
            continue
        caixas, vistos = [], set()
        for f in sorted(pdir.glob("visuals/*/visual.json")):
            total += 1
            try:
                v = le(f)
            except Exception as e:  # noqa: BLE001
                erros.append(f"{f}: JSON invalido ({e})")
                continue
            n = v.get("name")
            if n != f.parent.name:
                erros.append(f"{nome}/{f.parent.name}: name '{n}' diferente da pasta")
            if n in vistos:
                erros.append(f"{nome}: nome de visual repetido '{n}'")
            vistos.add(n)
            p = v["position"]
            x, y, w, h = p["x"], p["y"], p["width"], p["height"]
            if x < MARGEM or y < MARGEM or x + w > W_PAG - MARGEM or y + h > H_PAG - MARGEM:
                erros.append(f"{nome}/{n}: fora da area util (1280x720 com margem de {MARGEM}) ({x},{y},{w},{h})")
            caixas.append((n, x, y, x + w, y + h))
            if modelo is not None:
                for k, ent, prop in campos(v):
                    tipo = "column" if k == "Column" else "measure"
                    if ent not in modelo:
                        erros.append(f"{nome}/{n}: tabela '{ent}' nao existe no modelo")
                    elif prop not in modelo[ent][tipo]:
                        erros.append(f"{nome}/{n}: {tipo} '{ent}[{prop}]' nao existe no modelo")
            for q in v.get("visual", {}).get("query", {}).get("queryState", {}).values():
                for pr in q.get("projections", []):
                    k, ent, prop = chave(pr["field"])
                    if pr.get("queryRef") != f"{ent}.{prop}":
                        erros.append(f"{nome}/{n}: queryRef '{pr.get('queryRef')}' nao bate com o campo")
            sg = v.get("visual", {}).get("syncGroup")
            if sg:
                campo = v["visual"]["query"]["queryState"]["Values"]["projections"][0]["queryRef"]
                grupos.setdefault(sg["groupName"], set()).add((nome, campo))
        if caixas:
            esq = min(c[1] for c in caixas)
            dir_ = W_PAG - max(c[3] for c in caixas)
            if esq != dir_:
                erros.append(f"{nome}: margens laterais diferentes (esquerda {esq}, direita {dir_})")
        for i, a in enumerate(caixas):
            for b in caixas[i + 1:]:
                if a[1] < b[3] and b[1] < a[3] and a[2] < b[4] and b[2] < a[4]:
                    erros.append(f"{nome}: '{a[0]}' sobrepoe '{b[0]}'")
    for g, membros in grupos.items():
        pags = {m[0] for m in membros}
        cps = {m[1] for m in membros}
        if pags != set(PAGINAS) or len(cps) != 1:
            erros.append(f"syncGroup '{g}': precisa do mesmo campo nas 2 paginas ({sorted(membros)})")
    for g in ("g_metros", "g_pessoas"):
        arq = pages_dir / "pg_fluxo_2" / "visuals" / g / "visual.json"
        if not arq.exists():
            erros.append(f"pg_fluxo_2/{g}: nao existe")
            continue
        v = le(arq)["visual"]
        qs = v["query"]["queryState"]
        cat = qs.get("Category", {}).get("projections", [])
        sort = v["query"].get("sortDefinition", {}).get("sort", [])
        ok = (v["visualType"] == "clusteredColumnChart" and len(cat) == 1
              and cat[0]["queryRef"] == qref(EIXO_MES) and len(qs.get("Y", {}).get("projections", [])) == 2
              and sort and sort[0]["field"] == EIXO_MES and sort[0]["direction"] == "Ascending"
              and v["objects"]["categoryAxis"][0]["properties"]["axisType"] == txt("Categorical")
              and v["objects"]["labels"][0]["properties"]["show"] == boo(True))
        if not ok:
            erros.append(f"pg_fluxo_2/{g}: precisa ser colunas agrupadas por {qref(EIXO_MES)} (categorico, crescente), "
                         "2 series e rotulos ligados")
    if erros:
        print("VALIDACAO FALHOU:")
        for e in erros:
            print("  -", e)
        return False
    print(f"validacao ok: {total} visuais, campos conferidos no TMDL, {len(grupos)} grupos de sincronizacao, "
          f"sem sobreposicao, margem >= {MARGEM} px e laterais simetricas em 1280x720")
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("relatorio", nargs="?", default=str(PADRAO_REL), help="pasta .Report (PBIR)")
    ap.add_argument("--validar", action="store_true", help="so valida, nao grava")
    ap.add_argument("--forcar", action="store_true", help="permite gravar fora de uma pasta *_teste")
    a = ap.parse_args()
    rel = Path(a.relatorio).resolve()
    if not (rel / "definition" / "pages" / "pages.json").exists():
        sys.exit(f"nao achei definition/pages/pages.json em {rel}")
    if not a.validar:
        if not rel.parent.name.endswith("_teste") and not a.forcar:
            sys.exit(f"recusado: {rel} nao esta numa pasta *_teste (use --forcar se for de proposito)")
        gera(rel)
    sys.exit(0 if valida(rel) else 1)


if __name__ == "__main__":
    main()
