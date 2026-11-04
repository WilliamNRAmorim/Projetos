# -*- coding: utf-8 -*-
"""Gera as medidas do relatorio (reportExtensions.json) e as 2 paginas do Fluxo v2 (tubo, espiral, carreteis).

Uso:
    python gerar_medidas_paginas_fluxo.py [CAMINHO_DO_.Report]           (gera e valida)
    python gerar_medidas_paginas_fluxo.py [CAMINHO_DO_.Report] --validar  (so valida, nao grava)
    python gerar_medidas_paginas_fluxo.py ... --forcar                    (permite gravar fora de pasta *_teste)

Padrao do caminho: GMS/PowerBI/Painel_PBIP_teste/GMS_Painel.Report (copia local do GMS_Painel, fora do git).
O GMS_Painel e relatorio ligado ao vivo ao modelo (GMS): so aceita MEDIDAS DO RELATORIO. Nada de tabela, coluna ou
relacionamento novo. Medida do relatorio nao pode chamar outra medida do relatorio (erro semantico no servico,
COMO_ARRUMAR_HORAHORA.md): cada medida e escrita por extenso a partir do mesmo nucleo DAX (funcao nucleo()).

Idempotente: tira do reportExtensions.json so as medidas 'Fluxo · ...', poe as novas no fim; apaga e recria so
pages/pg_fluxo_1 e pages/pg_fluxo_2 e poe as 2 no fim do pages.json (pagina ativa nao muda). Nao mexe no
report.json, no tema nem nas outras paginas. Grava tambem Consulta_Conferencia_v2.dax nesta pasta.

Regras: PLANO_v2_tubo_espiral_carreteis.md e LEIAME_v2.md. Estilo das paginas: gerar_paginas_fluxo.py (importado).
"""
import argparse
import json
import re
import shutil
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
# estilo aprovado das paginas claras (paleta, caixa, segmentacao, navegador, Pagina): reaproveitado do gerador v1
from gerar_paginas_fluxo import (  # noqa: E402
    boo, caixa, col, cor_hex, inteiro, num, txt, v_carimbo, v_navegador, v_segmentacao, v_texto,
    HEX_AZUL, HEX_BORDA, HEX_CARTAO, HEX_LARANJA, HEX_PAGINA, HEX_SUAVE, HEX_TINTA,
    VALORES_CLAROS, CABECALHO_CLARO, SCH, V_PAGE, W_PAG, H_PAG, MARGEM, Pagina, le,
)

RAIZ_GMS = AQUI.parents[2]  # .../GMS
PADRAO_REL = RAIZ_GMS / "PowerBI" / "Painel_PBIP_teste" / "GMS_Painel.Report"
TMDL = RAIZ_GMS / "PowerBI" / "Modelo_PBIP" / "GMS_Modelo.SemanticModel" / "definition"  # snapshot, so leitura
ARQ_CONF = AQUI / "Consulta_Conferencia_v2.dax"

PAGINAS = ("pg_fluxo_1", "pg_fluxo_2")
PREFIXO = "Fluxo · "
PASTA = "Fluxo (relatório)"
M = "Medidas"

# ---- regras de negocio (fonte unica) ---------------------------------------
QTD_MAX = 2000          # m por ficha e etapa; acima disso e erro de digitacao e vira vazio
CORTE_DIA = 3000        # dia produtivo: trancagem + espiral (com maquina lixo) >= 3.000 m no dia inteiro
VIRADA_MIN = 320        # 05:20
T2_MIN, T3_MIN = 837, 1340  # 2o turno a partir de 13:57, 3o a partir de 22:20 (norma, MEL-250)
LT_MIN, LT_MAX = 0.5, 720
CARRETEL = [(4, 800), (6, 680), (8, 680), (10, 460), (12, 400), (16, 250)]  # bitola -> metros por carretel
BRAIDERS = ["TH01", "TH02", "TH03", "TH04", "TH05", "TH06", "TH07", "TM01", "TM04", "TO04"]
ESPIRAL = ["SPIRAL", "TE01", "TE0"]
TE = "{ 0, 2, 3 }"      # E da linha da trancadeira: 2 = trancagem, 3 = espiral, 0 = maquina vazia/lixo

# (E, nome, coluna do fim, quantidade, operador). Trancagem e Espiral leem a mesma trinca e se separam pela maquina.
ETAPAS = [
    (1, "Tubo", "data_hora_final_tubo", "quantidade_tubo", "operador_tubo"),
    (2, "Trançagem", "data_hora_final_trancadeira", "quantidade_trancagem", "operador_trancagem"),
    (3, "Espiral", "data_hora_final_trancadeira", "quantidade_trancagem", "operador_trancagem"),
    (4, "Cobertura", "data_hora_final_cobertura", "quantidade_cobertura", "operador_cobertura"),
    (5, "Bandagem", "data_hora_final_bandagem", "quantidade_bandagem", "operador_bandagem"),
    (6, "Vulcanização", "data_hora_final_vulcanizacao", "quantidade_vulcanizacao", "operador_vulcanizacao"),
    (7, "Debandagem", "data_hora_final_debandagem", "quantidade_debandagem", "operador_debandagem"),
    (8, "Cabine (teste)", "data_hora_final_extracao", "quantidade_extracao", "operador_extracao"),
]
NOME = {e: n for e, n, *_ in ETAPAS}
TODAS = [e for e, *_ in ETAPAS]
CAB = 8
COL_MAQ = "ficha_producao[Trançadeira]"
COL_TURNO = "fHoraHora[Turno]"  # segmentacao de Turno (coluna que o GMS_Painel ja usa na pagina Hora-Hora)

ACENTOS = [("Á", "A"), ("À", "A"), ("Â", "A"), ("Ã", "A"), ("Ä", "A"), ("É", "E"), ("È", "E"), ("Ê", "E"),
           ("Ë", "E"), ("Í", "I"), ("Ì", "I"), ("Î", "I"), ("Ï", "I"), ("Ó", "O"), ("Ò", "O"), ("Ô", "O"),
           ("Õ", "O"), ("Ö", "O"), ("Ú", "U"), ("Ù", "U"), ("Û", "U"), ("Ü", "U"), ("Ç", "C"), ("Ñ", "N")]


# ---- nucleo DAX ------------------------------------------------------------
def fc(c):
    return f"ficha_producao[{c}]"


# Nomes de VAR: o DAX nao diferencia maiusculas e nao aceita repetir um nome na mesma medida, nem em escopo aninhado
# (erro do Desktop em 04/11: "__corLa" da paleta x "__LA" do nucleo). Toda VAR aninhada leva o sufixo da fonte (s);
# a validacao lista os repetidos por medida.
def dia_ref(fim, s):
    """Dia de producao: fim da etapa menos 05:20, so a data."""
    v = f"__f{s}"
    return f"VAR {v} = {fc(fim)} - {VIRADA_MIN} / 1440 RETURN DATE ( YEAR ( {v} ), MONTH ( {v} ), DAY ( {v} ) )"


def turno_do_fim(fim, s):
    v = f"__m{s}"
    return (f"VAR {v} = HOUR ( {fc(fim)} ) * 60 + MINUTE ( {fc(fim)} ) "
            f"RETURN IF ( {v} >= {VIRADA_MIN} && {v} < {T2_MIN}, 1, IF ( {v} >= {T2_MIN} && {v} < {T3_MIN}, 2, 3 ) )")


def qtd(c, s):
    v = f"__q{s}"
    return f"VAR {v} = {fc(c)} RETURN IF ( {v} > {QTD_MAX}, BLANK (), {v} )"


def norm_op(c):
    """Maiusculas, sem acento, sem pontuacao; '/' separa pessoas (vira '|' para PATHITEM). TRIM depois do corte."""
    e = f"UPPER ( {fc(c)} )"
    for a, b in ACENTOS:
        e = f'SUBSTITUTE({e},"{a}","{b}")'
    for p in (".", ",", "-", "_"):
        e = f'SUBSTITUTE({e},"{p}","")'
    return f'SUBSTITUTE({e},"/","|")'


def carretel(c, s):
    """VARs __c<s> (quantidade), __cv<s> (quantidade limpa) e __mc<s> (metros do carretel da bitola)."""
    sw = ", ".join(f"{b}, {m}" for b, m in CARRETEL)
    return (f"VAR __c{s} = {fc(c)} VAR __cv{s} = IF ( __c{s} > {QTD_MAX}, BLANK (), __c{s} ) "
            f"VAR __mc{s} = SWITCH ( ficha_producao[Bitola], {sw} )")


def classe_maquina():
    lim = COL_MAQ
    for p in (".", "-", " ", "_"):
        lim = f'SUBSTITUTE ( {lim}, "{p}", "" )'
    br = ", ".join(f'"{x}"' for x in BRAIDERS)
    es = ", ".join(f'"{x}"' for x in ESPIRAL)
    return (f"VAR __mq = UPPER ( {lim} ) "
            f"RETURN IF ( __mq IN {{ {br} }}, 2, IF ( __mq IN {{ {es} }}, 3, 0 ) )")


def fonte(e_expr, fim, q, op, com_op, com_car, s):
    cols = [f'"@E", {e_expr}', f'"@Dia", {dia_ref(fim, s)}', f'"@T", {turno_do_fim(fim, s)}', f'"@Q", {qtd(q, s)}']
    if com_op:
        cols.append(f'"@Op", {norm_op(op)}')
    if com_car:
        cols.append(f'"@Car", {carretel(q, s + "Car")} RETURN DIVIDE ( __cv{s}Car, __mc{s}Car )')
        cols.append(f'"@Cob", {carretel(q, s + "Cob")} RETURN IF ( NOT ISBLANK ( __mc{s}Cob ), __cv{s}Cob )')
    corpo = ",\n            ".join(cols)
    return (f"FILTER (\n        SELECTCOLUMNS (\n            FILTER ( ALL ( ficha_producao ), NOT ISBLANK ( {fc(fim)} ) ),\n"
            f"            {corpo}\n        ),\n        [@Dia] IN __Datas\n    )")


def nucleo(etapas=TODAS, com_op=False, com_car=False, com_lt=False):
    """VARs comuns. etapas: quais E entram (a linha da trancadeira entra sempre: define o dia produtivo).

    Contexto: a selecao do dCalendario e capturada ANTES de qualquer limpeza (VAR __Datas). A ficha e lida com
    ALL ( ficha_producao ), que ignora os relacionamentos ativos (DataProducao -> dCalendario) e qualquer filtro;
    o dia vem da data de referencia calculada aqui. Turno: so le o conjunto de turnos da segmentacao fHoraHora[Turno]
    (ISFILTERED), sem usar Turno_* da ficha nem Etapas[Turno]."""
    fontes = []
    for e, _, fim, q, op in ETAPAS:
        if e == 3:
            continue  # espiral sai da mesma fonte da trancagem
        if e == 2:
            fontes.append(fonte(classe_maquina(), fim, q, op, com_op, com_car, f"S{e}"))
        elif e in etapas:
            fontes.append(fonte(str(e), fim, q, op, com_op, com_car, f"S{e}"))
    base = fontes[0] if len(fontes) == 1 else "UNION (\n    " + ",\n    ".join(fontes) + "\n)"
    v = [
        "VAR __Datas = CALCULATETABLE ( VALUES ( dCalendario[Date] ), REMOVEFILTERS ( fHoraHora[Turno] ) )",
        "VAR __UmDia = COUNTROWS ( __Datas ) = 1",
        f"VAR __FT = ISFILTERED ( {COL_TURNO} )",
        "VAR __Turnos =\n    FILTER (\n        SELECTCOLUMNS (\n"
        f"            CALCULATETABLE ( VALUES ( {COL_TURNO} ), REMOVEFILTERS ( dCalendario ) ),\n"
        f'            "@T", VAR __tTx = {COL_TURNO} & "" VAR __tP1 = SEARCH ( "1", __tTx, 1, 999 ) '
        'VAR __tP2 = SEARCH ( "2", __tTx, 1, 999 ) VAR __tP3 = SEARCH ( "3", __tTx, 1, 999 ) '
        "VAR __tPm = MIN ( MIN ( __tP1, __tP2 ), __tP3 ) "
        "RETURN IF ( __tPm = 999, BLANK (), IF ( __tPm = __tP1, 1, IF ( __tPm = __tP2, 2, 3 ) ) )\n"
        "        ),\n        NOT ISBLANK ( [@T] )\n    )",
        "VAR __B =\n" + base,
        f"VAR __BTE = FILTER ( __B, [@E] IN {TE} )",
        'VAR __DiasCom = DISTINCT ( SELECTCOLUMNS ( __B, "@Dia", [@Dia] ) )',
        "VAR __DiasProd =\n    FILTER (\n        __DiasCom,\n        VAR __dProd = [@Dia]\n"
        f"        RETURN __UmDia || SUMX ( FILTER ( __BTE, [@Dia] = __dProd ), [@Q] ) >= {CORTE_DIA}\n    )",
        "VAR __nD = COUNTROWS ( __DiasProd )",
        "VAR __LA = FILTER ( __B, NOT __FT || [@T] IN __Turnos )",
        "VAR __LP = FILTER ( __LA, [@Dia] IN __DiasProd )",
        f"VAR __MTE = DIVIDE ( SUMX ( FILTER ( __LP, [@E] IN {TE} ), [@Q] ), __nD )",
    ]
    for e in etapas:
        v.append(f"VAR __M{e} = DIVIDE ( SUMX ( FILTER ( __LP, [@E] = {e} ), [@Q] ), __nD )")
    if com_op:
        v.append(
            "VAR __P =\n    DISTINCT (\n        SELECTCOLUMNS (\n            FILTER (\n                GENERATE (\n"
            '                    FILTER ( __LP, [@Op] <> "" ),\n'
            "                    VAR __sOp = [@Op]\n"
            "                    RETURN SELECTCOLUMNS ( GENERATESERIES ( 1, PATHLENGTH ( __sOp ) ), "
            '"@Pe", TRIM ( PATHITEM ( __sOp, [Value] ) ) )\n'
            "                ),\n"
            '                [@Pe] <> ""\n'
            "            ),\n"
            '            "@E", [@E], "@Dia", [@Dia], "@Pe", [@Pe]\n'
            "        )\n    )")
        v.append(f'VAR __PpTE = DIVIDE ( COUNTROWS ( DISTINCT ( SELECTCOLUMNS ( FILTER ( __P, [@E] IN {TE} ), '
                 '"@Dia", [@Dia], "@Pe", [@Pe] ) ) ), __nD )')
        for e in etapas:
            v.append(f"VAR __Pp{e} = DIVIDE ( COUNTROWS ( FILTER ( __P, [@E] = {e} ) ), __nD )")
            v.append(f"VAR __K{e} = DIVIDE ( __Pp{e}, DIVIDE ( __M{e}, 1000 ) )")
        if set(etapas) == set(TODAS):
            # 8 cartoes individuais: destaque "mais gente/metro" e a etapa individual de maior conteudo
            v.append("VAR __Kt = { " + ", ".join(f"( {e}, __K{e} )" for e in TODAS) + " }")
            v.append("VAR __Kv = FILTER ( __Kt, NOT ISBLANK ( [Value2] ) )")
            v.append("VAR __KMaior = MAXX ( __Kv, [Value2] )")
            # serie de 7 etapas: Trancagem + Espiral (maquinas paralelas, com lixo) = 1 etapa (chave 2)
            v.append("VAR __KTE = DIVIDE ( __PpTE, DIVIDE ( __MTE, 1000 ) )")
            v.append("VAR __KSt = { " + ", ".join(f"( {k}, {x} )" for k, x in serie("__K")) + " }")
            v.append("VAR __KSv = FILTER ( __KSt, NOT ISBLANK ( [Value2] ) )")
            v.append("VAR __KSMedia = AVERAGEX ( __KSv, [Value2] )")
            v.append("VAR __KSMaior = MAXX ( __KSv, [Value2] )")
    if com_car:
        for e in etapas:
            v.append(f"VAR __C{e} = DIVIDE ( SUMX ( FILTER ( __LP, [@E] = {e} ), [@Car] ), __nD )")
            v.append(f"VAR __Cob{e} = DIVIDE ( SUMX ( FILTER ( __LP, [@E] = {e} ), [@Cob] ), "
                     f"SUMX ( FILTER ( __LP, [@E] = {e} ), [@Q] ) )")
    if set(etapas) == set(TODAS):
        v.append("VAR __Vt = { " + ", ".join(f"( {e}, __M{e} )" for e in TODAS) + " }")  # escala das barras
        v.append("VAR __VSt = { " + ", ".join(f"( {k}, {x} )" for k, x in serie("__M")) + " }")  # serie de 7
    if com_lt:
        fe, ft = "data_hora_final_extracao", "data_hora_final_trancadeira"
        v.append(
            "VAR __LTt =\n    FILTER (\n        SELECTCOLUMNS (\n"
            f"            FILTER ( ALL ( ficha_producao ), NOT ISBLANK ( {fc(fe)} ) && NOT ISBLANK ( {fc(ft)} ) ),\n"
            f'            "@Dia", {dia_ref(fe, "LT")},\n            "@T", {turno_do_fim(fe, "LT")},\n'
            f'            "@LT", ( {fc(fe)} - {fc(ft)} ) * 24\n        ),\n'
            f"        [@Dia] IN __Datas && ( NOT __FT || [@T] IN __Turnos ) && [@LT] >= {LT_MIN} && [@LT] <= {LT_MAX}\n"
            "    )")
        v.append("VAR __LTMediana = MEDIANX ( FILTER ( __LTt, [@Dia] IN __DiasProd ), [@LT] )")
        v.append("VAR __LTMedio = AVERAGEX ( __LTt, [@LT] )")
        v.append("VAR __Ini = MINX ( __DiasCom, [@Dia] )")
        v.append("VAR __Fim = MAXX ( __DiasCom, [@Dia] )")
        v.append(f"VAR __Lambda = DIVIDE ( SUMX ( FILTER ( __LA, [@E] = {CAB} ), [@Q] ), INT ( __Fim - __Ini ) + 1 )")
        v.append("VAR __WIP = IF ( NOT ISBLANK ( __Lambda ) && NOT ISBLANK ( __LTMedio ), __Lambda * __LTMedio / 24 )")
    return "\n".join(v)


def serie(pref):
    """Etapas em serie (7): Trancagem + Espiral viram 1 etapa (chave 2, VAR <pref>TE); a Espiral (3) sai."""
    return [(e, f"{pref}TE" if e == 2 else f"{pref}{e}") for e in TODAS if e != 3]


NOME_SERIE = {e: ("Trançagem+Espiral" if e == 2 else n) for e, n in NOME.items() if e != 3}


def nome_etapa_dax(var_idx, nomes=None):
    nomes = nomes or NOME
    pares = ", ".join(f'{e}, "{n}"' for e, n in nomes.items())
    return f"SWITCH ( {var_idx}, {pares} )"


def cv_dax():
    return (f"VAR __DiasCV = FILTER ( __DiasCom, VAR __dCV = [@Dia] RETURN SUMX ( FILTER ( __BTE, [@Dia] = __dCV ), [@Q] ) >= {CORTE_DIA} )\n"
            f"VAR __TEt = FILTER ( __LA, [@E] IN {TE} )\n"
            "VAR __CV =\n    IF (\n        COUNTROWS ( __DiasCV ) >= 2,\n        DIVIDE (\n"
            "            STDEVX.S ( __DiasCV, VAR __dSd = [@Dia] RETURN SUMX ( FILTER ( __TEt, [@Dia] = __dSd ), [@Q] ) + 0 ),\n"
            "            AVERAGEX ( __DiasCV, VAR __dAv = [@Dia] RETURN SUMX ( FILTER ( __TEt, [@Dia] = __dAv ), [@Q] ) + 0 )\n"
            "        )\n    )")


def eficiencia_dax():
    """Balanceamento na serie de 7 etapas (Trancagem + Espiral combinadas)."""
    return "VAR __Ef = DIVIDE ( SUMX ( __KSv, [Value2] ), COUNTROWS ( __KSv ) * __KSMaior )"


def restricoes_dax():
    """Restricao de vazao na serie de 7 (nunca a Espiral sozinha); maior conteudo entre os 8 cartoes individuais."""
    return ("VAR __iV = MAXX ( TOPN ( 1, FILTER ( __VSt, [Value2] > 0 ), [Value2], ASC, [Value1], ASC ), [Value1] )\n"
            "VAR __iC = MAXX ( TOPN ( 1, FILTER ( __Kt, [Value2] > 0 ), [Value2], DESC, [Value1], ASC ), [Value1] )\n"
            "VAR __MenorV = MINX ( FILTER ( __VSt, [Value2] > 0 ), [Value2] )")


# ---- SVG -------------------------------------------------------------------
# Paleta clara aprovada (Medidas_SVG_FluxoTrancagemCabine.md); '#' vira '%23' no data URI.
CORES = [("Ca", "ffffff"), ("Ti", "14130f"), ("Su", "55534d"), ("Li", "e1e0d9"), ("La", "eb6834"),
         ("LaF", "fdebe3"), ("LaT", "b34510"), ("Ve", "0a6a0a"), ("VeF", "e8f5e8"), ("SeF", "ff8a50"),
         ("SeT", "11161d"), ("On", "2a78d6"), ("Off", "cfd6df"), ("VeB", "0ca30c")]
SVG_VARS = " ".join(f'VAR __cor{n} = "%23{h}"' for n, h in CORES)
CARD_W, CARD_H = 272, 184      # viewBox e tamanho da imagem do cartao (2 x 4 em 1.248 px, sem rolagem)
ICONES_MAX = 12
PASSO_ICONE = 17


def svg_cartao(e, n):
    """Cartao horizontal 272 x 184: ETAPA n, nome, pessoas, carreteis, barra de m/dia e caixa de m/pessoa."""
    corpo = f"""{nucleo(TODAS, com_op=True, com_car=True)}
{SVG_VARS}
VAR __Pes = __Pp{e}
VAR __Met = __M{e}
VAR __Max = MAXX ( __DiasProd, VAR __dMx = [@Dia] RETURN COUNTROWS ( FILTER ( __P, [@E] = {e} && [@Dia] = __dMx ) ) )
VAR __MPe = DIVIDE ( __Met, __Pes )
VAR __Con = __K{e}
VAR __Pos = IF ( NOT ISBLANK ( __Con ), COUNTROWS ( FILTER ( __Kt, [Value2] > __Con ) ) + 1 )
VAR __Quente = NOT ISBLANK ( __Pos ) && __Pos <= 2
VAR __Car = __C{e}
VAR __Cob = __Cob{e}
VAR __CPe = DIVIDE ( __Car, __Pes )
VAR __Esc = MAXX ( __Vt, [Value2] ) * 1.05
VAR __Lb = IF ( __Esc > 0 && __Met > 0, ROUND ( 136 * DIVIDE ( __Met, __Esc ), 1 ), 0 )
VAR __SemDado = NOT ( __Met > 0 ) && NOT ( __Pes > 0 )
VAR __TotP = MAX ( __Max, ROUNDUP ( __Pes, 0 ) )
VAR __NP = MIN ( {ICONES_MAX}, __TotP )
VAR __IcP =
    IF (
        __NP > 0,
        CONCATENATEX (
            GENERATESERIES ( 0, __NP - 1, 1 ),
            VAR __iPe = [Value]
            VAR __frPe = FORMAT ( MAX ( 0, MIN ( 1, __Pes - __iPe ) ), "0.00", "en-US" )
            RETURN
                "<linearGradient id='p" & __iPe & "'><stop offset='" & __frPe & "' stop-color='" & __corOn & "'/><stop offset='" & __frPe & "' stop-color='" & __corOff & "'/></linearGradient>"
                    & "<g transform='translate(" & __iPe * {PASSO_ICONE} & " 0) scale(0.7)'><circle cx='10' cy='5' r='4.6' fill='url(%23p" & __iPe & ")'/><path d='M2 24v-6a8 8 0 0 1 16 0v6z' fill='url(%23p" & __iPe & ")'/></g>",
            "",
            [Value], ASC
        )
    )
VAR __XP = IF ( __TotP > {ICONES_MAX}, "<text x='{ICONES_MAX * PASSO_ICONE + 2}' y='13' font-size='10' fill='" & __corSu & "'>+" & ( __TotP - {ICONES_MAX} ) & "</text>" )
VAR __TotC = ROUNDUP ( __Car, 0 )
VAR __NC = MIN ( {ICONES_MAX}, __TotC )
VAR __IcC =
    IF (
        __NC > 0,
        CONCATENATEX (
            GENERATESERIES ( 0, __NC - 1, 1 ),
            VAR __iCa = [Value]
            VAR __frCa = FORMAT ( MAX ( 0, MIN ( 1, __Car - __iCa ) ), "0.00", "en-US" )
            RETURN
                "<linearGradient id='c" & __iCa & "' gradientUnits='userSpaceOnUse' x1='0' y1='0' x2='14' y2='0'><stop offset='" & __frCa & "' stop-color='" & __corOn & "'/><stop offset='" & __frCa & "' stop-color='" & __corOff & "'/></linearGradient>"
                    & "<g transform='translate(" & __iCa * {PASSO_ICONE} & " 0)'><rect x='0' y='0' width='3' height='16' rx='1' fill='url(%23c" & __iCa & ")'/><rect x='11' y='0' width='3' height='16' rx='1' fill='url(%23c" & __iCa & ")'/><rect x='3' y='3.5' width='8' height='9' fill='url(%23c" & __iCa & ")'/><path d='M5 4v8M7 4v8M9 4v8' stroke='" & __corCa & "' stroke-width='0.6'/></g>",
            "",
            [Value], ASC
        )
    )
VAR __XC = IF ( __TotC > {ICONES_MAX}, "<text x='{ICONES_MAX * PASSO_ICONE + 2}' y='12' font-size='10' fill='" & __corSu & "'>+" & ( __TotC - {ICONES_MAX} ) & "</text>" )
VAR __Contorno =
    IF (
        __Quente,
        "<rect x='3' y='3' width='266' height='178' rx='12' fill='none' stroke='" & __corLaF & "' stroke-width='4'/>"
            & "<rect x='3' y='3' width='266' height='178' rx='12' fill='" & __corCa & "' stroke='" & __corLa & "' stroke-width='1.5'/>",
        "<rect x='1.5' y='1.5' width='269' height='181' rx='12' fill='" & __corCa & "' stroke='" & __corLi & "' stroke-width='1'/>"
    )
VAR __Selo =
    IF (
        __Quente,
        "<rect x='162' y='9' width='100' height='18' rx='9' fill='" & __corSeF & "'/>"
            & "<text x='212' y='21.5' text-anchor='middle' font-size='10' font-weight='700' fill='" & __corSeT & "'>mais gente/metro</text>"
    )
VAR __Cab =
    "<text x='14' y='22' font-size='10' font-weight='700' letter-spacing='0.6' fill='" & __corSu & "'>ETAPA {e}</text>"
        & "<text x='14' y='41' font-size='15' font-weight='700' fill='" & __corTi & "'>{n}</text>"
VAR __Pessoas =
    "<g transform='translate(14 50)'>" & __IcP & __XP & "</g>"
        & "<text x='14' y='84' fill='" & __corTi & "'><tspan font-size='14' font-weight='700'>" & IF ( ISBLANK ( __Pes ), "–", FORMAT ( __Pes, "0.0", "pt-BR" ) ) & "</tspan>"
        & "<tspan font-size='10.5' fill='" & __corSu & "'> pessoas/dia" & IF ( NOT ISBLANK ( __Max ), " · máx " & FORMAT ( __Max, "0" ) ) & "</tspan></text>"
VAR __Carreteis =
    IF (
        __Car > 0,
        "<g transform='translate(14 92)'>" & __IcC & __XC & "</g>"
            & "<text x='14' y='124' fill='" & __corTi & "'><tspan font-size='13' font-weight='700'>" & FORMAT ( __Car, "0.0", "pt-BR" ) & "</tspan>"
            & "<tspan font-size='10.5' fill='" & __corSu & "'> carretéis/dia" & IF ( NOT ISBLANK ( __CPe ), " · " & FORMAT ( __CPe, "0.0", "pt-BR" ) & " por pessoa" ) & "</tspan></text>"
            & IF ( __Cob < 0.995, "<text x='14' y='137' font-size='9.5' fill='" & __corSu & "'>carretéis em " & FORMAT ( __Cob * 100, "0" ) & "%25 dos metros</text>" ),
        IF ( __Met > 0, "<text x='14' y='112' font-size='10.5' fill='" & __corSu & "'>carretéis n/d (bitola fora da tabela)</text>" )
    )
VAR __Barra =
    "<rect x='14' y='148' width='136' height='8' rx='4' fill='" & __corLi & "'/>"
        & IF ( __Lb > 0, "<rect x='14' y='148' width='" & FORMAT ( __Lb, "0.0", "en-US" ) & "' height='8' rx='4' fill='" & __corOn & "'/>" )
        & "<text x='14' y='173' fill='" & __corTi & "'><tspan font-size='13' font-weight='700'>" & IF ( ISBLANK ( __Met ), "–", FORMAT ( __Met, "#,0", "pt-BR" ) ) & "</tspan><tspan font-size='10.5'> m/dia</tspan></text>"
VAR __Caixa =
    "<rect x='156' y='142' width='102' height='34' rx='8' fill='" & IF ( __Quente, __corLaF, __corVeF ) & "'/>"
        & "<text x='164' y='157' fill='" & __corTi & "'><tspan font-size='14' font-weight='700' fill='" & IF ( __Quente, __corLaT, __corVe ) & "'>" & IF ( ISBLANK ( __MPe ), "–", FORMAT ( __MPe, "#,0", "pt-BR" ) ) & "</tspan><tspan font-size='10'> m/pessoa</tspan></text>"
        & "<text x='164' y='170' font-size='9' fill='" & __corSu & "'>" & IF ( ISBLANK ( __Con ), "–", FORMAT ( __Con, "0.00", "pt-BR" ) ) & " p/1.000 m</text>"
RETURN
    IF (
        __SemDado,
        BLANK (),
        "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='{CARD_W}' height='{CARD_H}' viewBox='0 0 {CARD_W} {CARD_H}' font-family='Segoe UI, sans-serif'>"
            & __Contorno & __Selo & __Cab & __Pessoas & __Carreteis & __Barra & __Caixa & "</svg>"
    )"""
    return corpo


CONT_W, CONT_H = 560, 286     # SVG unico das 8 barras (pagina 2)


def svg_conteudo():
    linhas = []
    for i, e in enumerate(TODAS):
        y = 36 + i * 31
        linhas.append(
            f"VAR __Pos{e} = IF ( NOT ISBLANK ( __K{e} ), COUNTROWS ( FILTER ( __Kt, [Value2] > __K{e} ) ) + 1 )\n"
            f"VAR __Q{e} = NOT ISBLANK ( __Pos{e} ) && __Pos{e} <= 2\n"
            f"VAR __L{e} = IF ( __Esc > 0 && __K{e} > 0, ROUND ( 360 * DIVIDE ( __K{e}, __Esc ), 1 ), 0 )\n"
            f"VAR __R{e} =\n"
            f"    \"<text x='0' y='{y + 16}' font-size='12' fill='\" & __corTi & \"'>{NOME[e]}</text>\"\n"
            f"        & \"<rect x='120' y='{y + 4}' width='360' height='16' rx='5' fill='\" & __corLi & \"'/>\"\n"
            f"        & IF ( __L{e} > 0, \"<rect x='120' y='{y + 4}' width='\" & FORMAT ( __L{e}, \"0.0\", \"en-US\" ) & \"' height='16' rx='5' fill='\" & IF ( __Q{e}, __corLa, __corVeB ) & \"'/>\" )\n"
            f"        & \"<text x='556' y='{y + 17}' text-anchor='end' font-size='13' font-weight='700' fill='\" & IF ( __Q{e}, __corLaT, __corTi ) & \"'>\" & IF ( ISBLANK ( __K{e} ), \"–\", FORMAT ( __K{e}, \"0.00\", \"pt-BR\" ) ) & \"</text>\"")
    y_fim = 36 + len(TODAS) * 31
    juntar = " & ".join(f"__R{e}" for e in TODAS)
    return f"""{nucleo(TODAS, com_op=True)}
{SVG_VARS}
VAR __Esc = MAX ( __KMaior, __KSMaior ) * 1.1
VAR __XM = IF ( __Esc > 0 && NOT ISBLANK ( __KSMedia ), FORMAT ( 120 + ROUND ( 360 * DIVIDE ( __KSMedia, __Esc ), 1 ), "0.0", "en-US" ) )
{chr(10).join(linhas)}
VAR __Titulo =
    "<text x='0' y='16' fill='" & __corTi & "'><tspan font-size='13' font-weight='700'>Quais etapas usam mais gente por 1.000 m?</tspan>"
        & "<tspan font-size='11' fill='" & __corSu & "'>" & IF ( NOT ISBLANK ( __KSMedia ), "  ·  tracejado = média do trecho " & FORMAT ( __KSMedia, "0.00", "pt-BR" ) ) & "</tspan></text>"
VAR __Media =
    IF ( NOT ISBLANK ( __XM ), "<line x1='" & __XM & "' x2='" & __XM & "' y1='30' y2='{y_fim}' stroke='" & __corTi & "' stroke-width='1.5' stroke-dasharray='4 3'/>" )
RETURN
    IF (
        ISBLANK ( __KMaior ),
        BLANK (),
        "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='{CONT_W}' height='{CONT_H}' viewBox='0 0 {CONT_W} {CONT_H}' font-family='Segoe UI, sans-serif'>"
            & __Titulo & {juntar} & __Media & "</svg>"
    )"""


# ---- medidas ---------------------------------------------------------------
def leitura():
    return f"""{nucleo(TODAS, com_op=True, com_lt=True)}
{eficiencia_dax()}
{restricoes_dax()}
VAR __EtV = {nome_etapa_dax("__iV", NOME_SERIE)}
VAR __EtC = {nome_etapa_dax("__iC")}
VAR __UmDiaDado = __UmDia && NOT ISEMPTY ( __DiasCom )
VAR __P1 =
    IF ( NOT ISBLANK ( __iV ),
        "A etapa que mais limita a vazão é " & __EtV & " (" & FORMAT ( __MenorV, "#,0", "pt-BR" )
            & " m/dia). Pela Teoria das Restrições, só o que melhora ali aumenta a entrega da linha." )
VAR __P2 =
    IF ( NOT ISBLANK ( __iC ),
        "A etapa que mais consome gente por metro é " & __EtC & " (" & FORMAT ( __KMaior, "0.00", "pt-BR" )
            & " pessoas por 1.000 m, " & FORMAT ( DIVIDE ( __KMaior, __KSMedia ), "0.0", "pt-BR" )
            & "× a média do trecho). É onde está a maior movimentação de pessoas." )
VAR __P3 =
    IF ( NOT ISBLANK ( __Ef ),
        "Eficiência de balanceamento de " & FORMAT ( __Ef, "0%", "pt-BR" )
            & " (100% seria o mesmo número de pessoas por metro em todas as etapas). Cada etapa tem uma natureza de trabalho; a diferença só vira espaço de realocação onde há ociosidade." )
VAR __P4 =
    IF ( NOT ISBLANK ( __WIP ),
        "Pela Lei de Little, cerca de " & FORMAT ( __WIP, "#,0", "pt-BR" )
            & " m ficam em processo entre a trançagem/espiral e a cabine (lead time médio de " & FORMAT ( __LTMedio, "#,0", "pt-BR" )
            & " h" & IF ( NOT ISBLANK ( __LTMediana ), "; mediana de " & FORMAT ( __LTMediana, "#,0", "pt-BR" ) & " h" )
            & "). Reduzir lead time ou variabilidade reduz esse estoque sem mexer na vazão." )
VAR __P5 =
    IF ( __UmDiaDado, "Dia único: a média é o próprio dia, então a leitura de variabilidade não se aplica." )
VAR __Partes = {{ ( 1, __P1 ), ( 2, __P2 ), ( 3, __P3 ), ( 4, __P4 ), ( 5, __P5 ) }}
VAR __Texto = CONCATENATEX ( FILTER ( __Partes, [Value2] <> "" ), [Value2], UNICHAR ( 10 ) & UNICHAR ( 10 ), [Value1], ASC )
RETURN
    IF ( __Texto = "", "Sem dados no filtro.", __Texto )"""


def m_simples(etapas, com_op, ret, com_car=False, com_lt=False, extra=""):
    return f"{nucleo(etapas, com_op=com_op, com_car=com_car, com_lt=com_lt)}\n{extra}{'' if not extra else chr(10)}RETURN\n    {ret}"


def medidas():
    """[(nome, tipo, DAX, formato, categoria, pasta)]"""
    ms = []
    pv = PASTA
    pvis = PASTA + "\\Visual"
    ms.append((PREFIXO + "Vazão Cabine (m/dia)", "Double", m_simples([CAB], False, f"__M{CAB}"), "#,0", None, pv))
    ms.append((PREFIXO + "Vazão Tranç+Esp (m/dia)", "Double", m_simples([CAB], False, "__MTE"), "#,0", None, pv))
    ms.append((PREFIXO + "Pessoas nas 8 Etapas", "Double",
               m_simples(TODAS, True, " + ".join(f"__Pp{e}" for e in TODAS)), "#,0.0", None, pv))
    ms.append((PREFIXO + "Pessoas Tranç+Esp (por dia)", "Double", m_simples([CAB], True, "__PpTE"), "#,0.0", None, pv))
    ms.append((PREFIXO + "Pessoas Cabine (por dia)", "Double", m_simples([CAB], True, f"__Pp{CAB}"), "#,0.0", None, pv))
    ms.append((PREFIXO + "Pessoas Tranç+Esp / Cabine", "Text", m_simples([CAB], True,
               f'IF ( NOT ISBLANK ( __PpTE ) || NOT ISBLANK ( __Pp{CAB} ), '
               f'IF ( ISBLANK ( __PpTE ), "–", FORMAT ( __PpTE, "0.0", "pt-BR" ) ) & " / " & '
               f'IF ( ISBLANK ( __Pp{CAB} ), "–", FORMAT ( __Pp{CAB}, "0.0", "pt-BR" ) ) )'), None, None, pv))
    ms.append((PREFIXO + "m por Pessoa Cabine", "Double",
               m_simples([CAB], True, f"DIVIDE ( __M{CAB}, __Pp{CAB} )"), "#,0", None, pv))
    ms.append((PREFIXO + "Eficiência de Balanceamento", "Double",
               m_simples(TODAS, True, "__Ef", extra=eficiencia_dax()), "0%", None, pv))
    ms.append((PREFIXO + "Lead Time (h)", "Double", m_simples([CAB], False, "__LTMediana", com_lt=True),
               "#,0", None, pv))
    ms.append((PREFIXO + "WIP Little (m)", "Double", m_simples([CAB], False, "__WIP", com_lt=True), "#,0", None, pv))
    ms.append((PREFIXO + "CV Vazão Tranç+Esp", "Double", m_simples([CAB], False, "__CV", extra=cv_dax()),
               "0.0%", None, pv))
    ms.append((PREFIXO + "Rendimento de Fluxo", "Double",
               m_simples([CAB], False, f"DIVIDE ( __M{CAB}, __MTE )"), "0%", None, pv))
    ms.append((PREFIXO + "Dias Produtivos", "Double", m_simples([CAB], False, "IF ( __nD > 0, __nD )"),
               "#,0", None, pv))
    ms.append((PREFIXO + "Leitura Automática", "Text", leitura(), None, None, pvis))
    for e, n, *_ in ETAPAS:
        ms.append((nome_svg(e), "Text", svg_cartao(e, n), None, "ImageUrl", pvis))
    ms.append((PREFIXO + "SVG Conteúdo", "Text", svg_conteudo(), None, "ImageUrl", pvis))
    return ms


def nome_svg(e):
    return f"{PREFIXO}SVG {e} {NOME[e]}"


def ext_json(ms):
    out = []
    for n, t, e, f, cat, pasta in ms:
        d = {"name": n, "dataType": t, "expression": e}
        if f:
            d["formatString"] = f
        if cat:
            d["dataCategory"] = cat
        d["displayFolder"] = pasta
        out.append(d)
    return out


# ---- visuais ---------------------------------------------------------------
def mx(prop):
    """Medida do relatorio: o Desktop exige Schema 'extension' (gerar_relatorio.py)."""
    return {"Measure": {"Expression": {"SourceRef": {"Schema": "extension", "Entity": M}}, "Property": prop}}


def chave(campo):
    if "HierarchyLevel" in campo:
        h = campo["HierarchyLevel"]["Expression"]["Hierarchy"]
        pv = h["Expression"]["PropertyVariationSource"]
        ent = pv["Expression"]["SourceRef"]["Entity"]
        return "HierarchyLevel", ent, f'{pv["Property"]}.{pv["Name"]}.{h["Hierarchy"]}.{campo["HierarchyLevel"]["Level"]}'
    k = "Column" if "Column" in campo else "Measure"
    return k, campo[k]["Expression"]["SourceRef"]["Entity"], campo[k]["Property"]


def proj(campo, rotulo=None, ativo=False, formato=None):
    k, e, p = chave(campo)
    nq = rotulo or (f'{campo["HierarchyLevel"]["Expression"]["Hierarchy"]["Expression"]["PropertyVariationSource"]["Property"]} '
                    f'{campo["HierarchyLevel"]["Level"]}' if k == "HierarchyLevel" else p)
    d = {"field": campo, "queryRef": f"{e}.{p}", "nativeQueryRef": nq}
    if rotulo:
        d["displayName"] = rotulo
    if formato:
        d["format"] = formato
    if ativo:
        d["active"] = True
    return d


def nivel_data(nivel):
    return {"HierarchyLevel": {"Expression": {"Hierarchy": {"Expression": {"PropertyVariationSource": {
        "Expression": {"SourceRef": {"Entity": "dCalendario"}}, "Name": "Variation", "Property": "Date"}},
        "Hierarchy": "Hierarquia de datas"}}, "Level": nivel}}


KPIS = [  # (medida, rotulo curto <= 19 caracteres, formato do visual)
    (PREFIXO + "Vazão Cabine (m/dia)", "m/dia cabine", "#,0"),
    (PREFIXO + "Pessoas nas 8 Etapas", "pessoas no trecho", "#,0.0"),
    (PREFIXO + "Pessoas Tranç+Esp / Cabine", "pessoas tranç./cab.", None),
    (PREFIXO + "m por Pessoa Cabine", "m/pessoa cabine", "#,0"),
    (PREFIXO + "Eficiência de Balanceamento", "eficiência", "0%"),
    (PREFIXO + "Lead Time (h)", "lead time", '#,0 "h"'),
    (PREFIXO + "WIP Little (m)", "em processo", '#,0 "m"'),
    (PREFIXO + "CV Vazão Tranç+Esp", "CV vazão", "0.0%"),
    (PREFIXO + "Rendimento de Fluxo", "rendimento", "0%"),
]


def v_kpis():
    sel = {"id": "default"}
    return {
        "visualType": "cardVisual",
        "query": {"queryState": {"Data": {"projections": [proj(mx(m), r, formato=f) for m, r, f in KPIS]}}},
        "objects": {
            "layout": [{"properties": {"maxTiles": inteiro(len(KPIS))}},
                       {"properties": {"backgroundShow": boo(False), "cellPadding": inteiro(4),
                                       "paddingUniform": inteiro(4)}, "selector": sel}],
            "value": [{"properties": {"fontSize": num(20), "fontFamily": txt("Segoe UI Semibold"),
                                      "fontColor": cor_hex(HEX_TINTA), "displayUnits": num(1),
                                      "labelDisplayUnits": num(1), "valueDisplayUnits": num(1)}, "selector": sel},
                      {"properties": {"fontSize": num(16)}, "selector": {"metadata": f"{M}.{KPIS[2][0]}"}}],
            "label": [{"properties": {"show": boo(True), "position": txt("belowValue"), "fontSize": num(9),
                                      "fontFamily": txt("Segoe UI"), "fontColor": cor_hex(HEX_SUAVE)},
                       "selector": sel}],
            "outline": [{"properties": {"show": boo(False)}, "selector": sel}],
        },
        "visualContainerObjects": caixa(None, pad=(6, 6, 8, 8),
                                        alt="Nove indicadores do fluxo tubo→cabine no filtro escolhido."),
        "drillFilterOtherVisuals": True,
    }


def v_imagem(medida, rotulo, img_w, img_h, alt, fundo_cartao=False):
    """Tabela de 1 coluna com 1 medida SVG (ImageUrl). Cabecalho invisivel (fonte 1, cor e fundo iguais ao fundo),
    sem total, sem grade. fundo_cartao: o visual tem cartao branco (pagina 2); senao some na pagina (pagina 1)."""
    m = mx(medida)
    fundo = HEX_CARTAO if fundo_cartao else HEX_PAGINA
    return {
        "visualType": "tableEx",
        "query": {"queryState": {"Values": {"projections": [proj(m, rotulo)]}}},
        "objects": {
            "columnHeaders": [{"properties": {"fontSize": num(1), "fontColor": cor_hex(fundo), "backColor": cor_hex(fundo),
                                              "wordWrap": boo(False)}}],
            "values": [{"properties": {"backColorPrimary": cor_hex(fundo), "backColorSecondary": cor_hex(fundo),
                                       "fontColorPrimary": cor_hex(fundo), "fontColorSecondary": cor_hex(fundo)}}],
            "grid": [{"properties": {"gridVertical": boo(False), "gridHorizontal": boo(False),
                                     "outlineColor": cor_hex(fundo), "rowPadding": num(0),
                                     "imageHeight": num(img_h), "imageWidth": num(img_w)}}],
            "total": [{"properties": {"totals": boo(False)}}],
            "columnWidth": [{"properties": {"value": num(img_w + 8)}, "selector": {"metadata": f"{M}.{medida}"}}],
        },
        "visualContainerObjects": caixa(None, fundo=fundo_cartao, pad=(12, 12, 14, 14) if fundo_cartao else 0, alt=alt),
        "drillFilterOtherVisuals": True,
    }


def v_leitura():
    m = PREFIXO + "Leitura Automática"
    return {
        "visualType": "tableEx",
        "query": {"queryState": {"Values": {"projections": [proj(mx(m), "Leitura automática")]}}},
        "objects": {
            "values": [{"properties": {"wordWrap": boo(True), "fontSize": num(11), "fontFamily": txt("Segoe UI"),
                                       **VALORES_CLAROS}}],
            "columnHeaders": [{"properties": CABECALHO_CLARO}],
            "grid": [{"properties": {"gridVertical": boo(False), "gridHorizontal": boo(False),
                                     "outlineColor": cor_hex(HEX_BORDA)}}],
            "total": [{"properties": {"totals": boo(False)}}],
            "columnWidth": [{"properties": {"value": num(556)}, "selector": {"metadata": f"{M}.{m}"}}],
        },
        "visualContainerObjects": caixa(None, alt="Leitura automática do fluxo: restrição, mão de obra, "
                                                  "balanceamento, Little e avisos do filtro escolhido."),
        "drillFilterOtherVisuals": True,
    }


EIXO = [nivel_data("Ano"), nivel_data("Mês")]  # hierarquia de datas do dCalendario, expandida ate o mes


def v_colunas(series, titulo, alt, formato, fonte_rotulo):
    return {
        "visualType": "clusteredColumnChart",
        "query": {"queryState": {"Category": {"projections": [proj(EIXO[0], ativo=True), proj(EIXO[1], ativo=True)]},
                                 "Y": {"projections": [proj(mx(m), r, formato=formato) for m, r, _ in series]}},
                  "sortDefinition": {"sort": [{"field": EIXO[0], "direction": "Ascending"},
                                              {"field": EIXO[1], "direction": "Ascending"}], "isDefaultSort": False}},
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
        "drillFilterOtherVisuals": True,
    }


# ---- paginas ---------------------------------------------------------------
LINHA2 = "Ficha de produção · dia de 05:20 a 05:20 · média dos dias com trançagem + espiral ≥ 3.000 m"
RODAPE = "Pessoas = operadores distintos que apontaram a etapa no dia (estimativa, não é escala oficial)."
LEGENDA = ("Laranja = as 2 etapas com mais gente por 1.000 m · p/1.000 m = pessoas a cada 1.000 m · carretel: "
           "4→800 m, 6 e 8→680, 10→460, 12→400, 16→250 · n/d = bitola fora da tabela · Turno pelo fim da etapa")
Y_FAIXA, H_FAIXA = 16, 64
Y_CONT = Y_FAIXA + H_FAIXA + 12          # 92
Y_RODAPE, H_RODAPE = 672, 32
FIM_CONT = Y_RODAPE - 12                 # 660
SEGMENTACOES = [  # (nome, campo, rotulo, grupo, x)
    ("seg_ano", col("dCalendario", "Ano"), "Ano", "fluxo_ano", 620),
    ("seg_mes", col("dCalendario", "Mês"), "Mês", "fluxo_mes", 784),
    ("seg_dia", col("dCalendario", "Dia"), "Dia", "fluxo_dia", 948),
    ("seg_turno", col("fHoraHora", "Turno"), "Turno", "fluxo_turno", 1112),
]
# Pagina 1: KPIs 92-188; cartoes 2 x 4 de 303 x 206 (200-406 e 418-624); legenda 636-660.
H_KPI = 96
CARD_VW, CARD_VH, GAP = 303, 206, 12


def faixa_comum(p, titulo1, outras):
    p.add("titulo", 16, Y_FAIXA, 588, H_FAIXA, v_texto([(titulo1, 18, "Segoe UI Semibold", HEX_TINTA),
                                                         (LINHA2, 10, "Segoe UI", HEX_SUAVE)]))
    for nome, campo, rot, grupo, x in SEGMENTACOES:
        p.add(nome, x, Y_FAIXA, 152, H_FAIXA, v_segmentacao(campo, rot, grupo))
    p.add("rodape", 16, Y_RODAPE, 576, H_RODAPE, v_texto([(RODAPE, 9, "Segoe UI", HEX_SUAVE)]))
    p.add("nav", 608, Y_RODAPE, 368, H_RODAPE, v_navegador(outras))
    p.add("atualizado", 992, Y_RODAPE, 272, H_RODAPE, v_carimbo())


def pg_fluxo_1(outras):
    p = Pagina("pg_fluxo_1", "Fluxo · Etapas")
    faixa_comum(p, "Fluxo tubo → cabine · etapas e carretéis", outras)
    p.add("kpis", 16, Y_CONT, 1248, H_KPI, v_kpis())
    y0 = Y_CONT + H_KPI + GAP                                         # 200
    for i, (e, n, *_) in enumerate(ETAPAS):
        lin, colu = divmod(i, 4)
        x = 16 + colu * (CARD_VW + GAP)
        y = y0 + lin * (CARD_VH + GAP)
        p.add(f"cartao_{e}", x, y, CARD_VW, CARD_VH, v_imagem(
            nome_svg(e), n, CARD_W, CARD_H,
            f"Etapa {e}, {n}: pessoas por dia, carretéis por dia, metros por dia e metros por pessoa."))
    y_leg = y0 + 2 * CARD_VH + GAP + GAP                               # 636
    p.add("legenda", 16, y_leg, 1248, FIM_CONT - y_leg, v_texto([(LEGENDA, 9, "Segoe UI", HEX_SUAVE)],
                                                                alt="Legenda das cores e dos carretéis."))
    return p


def pg_fluxo_2(outras):
    p = Pagina("pg_fluxo_2", "Fluxo · Mão de obra")
    faixa_comum(p, "Fluxo tubo → cabine · mão de obra", outras)
    h_tab = 340
    y_g = Y_CONT + h_tab + 12                       # 444
    h_g = FIM_CONT - y_g                            # 216
    p.add("t_conteudo", 16, Y_CONT, 616, h_tab, v_imagem(
        PREFIXO + "SVG Conteúdo", "Pessoas a cada 1.000 m", CONT_W, CONT_H,
        "Pessoas a cada 1.000 m nas 8 etapas; laranja são as duas com mais gente por metro; tracejado é a média.",
        fundo_cartao=True))
    p.add("t_leitura", 648, Y_CONT, 616, h_tab, v_leitura())
    p.add("g_metros", 16, y_g, 616, h_g, v_colunas(
        [(PREFIXO + "Vazão Tranç+Esp (m/dia)", "Trançagem + espiral", HEX_AZUL),
         (PREFIXO + "Vazão Cabine (m/dia)", "Cabine", HEX_LARANJA)],
        "Metros por dia · média dos dias produtivos, por mês",
        "Colunas por mês: metros por dia da trançagem mais espiral e da cabine, média dos dias produtivos.", "#,0", 8))
    p.add("g_pessoas", 648, y_g, 616, h_g, v_colunas(
        [(PREFIXO + "Pessoas Tranç+Esp (por dia)", "Trançagem + espiral", HEX_AZUL),
         (PREFIXO + "Pessoas Cabine (por dia)", "Cabine", HEX_LARANJA)],
        "Pessoas por dia · média dos dias produtivos, por mês",
        "Colunas por mês: pessoas por dia na trançagem mais espiral e na cabine, média dos dias produtivos.",
        "#,0.0", 9))
    return p


# ---- saida (tudo em memoria; gravar e conferir idempotencia usam o mesmo mapa) ----
def dumps(o):
    return json.dumps(o, ensure_ascii=False, indent=2)


def saidas(rel):
    """{caminho: texto} de tudo o que o gerador escreve, a partir do estado atual (sem as paginas/medidas Fluxo)."""
    d = rel / "definition"
    ext = le(d / "reportExtensions.json")
    ents = ext.setdefault("entities", [])
    ent = next((x for x in ents if x.get("name") == M), None)
    if ent is None:
        ent = {"name": M, "measures": []}
        ents.append(ent)
    ent["measures"] = [x for x in ent.get("measures", []) if not x["name"].startswith(PREFIXO)] + ext_json(medidas())
    meta = le(d / "pages" / "pages.json")
    outras = [p for p in meta.get("pageOrder", []) if p not in PAGINAS]
    meta["pageOrder"] = outras + list(PAGINAS)
    out = {d / "reportExtensions.json": dumps(ext), d / "pages" / "pages.json": dumps(meta)}
    for p in (pg_fluxo_1(outras), pg_fluxo_2(outras)):
        out[d / "pages" / p.nome / "page.json"] = dumps({
            "$schema": f"{SCH}/page/{V_PAGE}/schema.json", "name": p.nome, "displayName": p.titulo,
            "displayOption": "FitToPage", "height": H_PAG, "width": W_PAG,
            "objects": {"background": [{"properties": {"color": cor_hex(HEX_PAGINA), "transparency": num(0)}}],
                        "outspace": [{"properties": {"color": cor_hex(HEX_PAGINA), "transparency": num(0)}}]}})
        for v in p.visuais:
            out[d / "pages" / p.nome / "visuals" / v["name"] / "visual.json"] = dumps(v)
    out[ARQ_CONF] = consulta_conferencia()
    return out


def gera(rel):
    out = saidas(rel)
    for nome in PAGINAS:
        alvo = rel / "definition" / "pages" / nome
        if alvo.exists():
            shutil.rmtree(alvo)
    for c, t in out.items():
        c.parent.mkdir(parents=True, exist_ok=True)
        c.write_text(t, encoding="utf-8")
    n_vis = sum(1 for c in out if c.name == "visual.json")
    print(f"ok: {len(medidas())} medidas 'Fluxo · ' no reportExtensions.json, {n_vis} visuais em {', '.join(PAGINAS)}, "
          f"{ARQ_CONF.name}")


# ---- consulta de conferencia -------------------------------------------------
def tabela_etapas():
    linhas = []
    for e, n, *_ in ETAPAS:
        linhas.append(f'( "{e} {n}", __M{e}, __Pp{e}, DIVIDE ( __M{e}, __Pp{e} ), __K{e}, __C{e}, __Cob{e}, '
                      f"DIVIDE ( __C{e}, __Pp{e} ) )")
    linhas.append('( "Tranç+Esp com máquina lixo (= Trançagem do piloto)", __MTE, __PpTE, DIVIDE ( __MTE, __PpTE ), '
                  "DIVIDE ( __PpTE, DIVIDE ( __MTE, 1000 ) ), BLANK (), BLANK (), BLANK () )")
    linhas.append('( "Dias produtivos", __nD, BLANK (), BLANK (), BLANK (), BLANK (), BLANK (), BLANK () )')
    cols = ['"Etapa", [Value1]', '"m/dia", [Value2]', '"pessoas/dia", [Value3]', '"m/pessoa", [Value4]',
            '"pessoas/1.000 m", [Value5]', '"carretéis/dia", [Value6]', '"fatia com carretel", [Value7]',
            '"carretéis/pessoa", [Value8]']
    return (f"{nucleo(TODAS, com_op=True, com_car=True)}\nRETURN\n    SELECTCOLUMNS (\n        {{\n            "
            + ",\n            ".join(linhas) + "\n        },\n        " + ", ".join(cols) + "\n    )")


def ind(s, n):
    return "\n".join((" " * n + x) if x.strip() else x for x in s.splitlines())


def consulta_conferencia():
    filtro_data = "dCalendario[Date] <= DATE ( 2026, 10, 6 )"
    filtro_t1 = 'FILTER ( ALL ( fHoraHora[Turno] ), CONTAINSSTRING ( fHoraHora[Turno], "1" ) )'
    defs, campos_row = [], []
    for n, t, e, f, cat, _ in medidas():
        if cat:
            continue
        cn = "Conf2 · " + n[len(PREFIXO):]
        defs.append(f"    MEASURE {M}[{cn}] =\n{ind(e, 8)}")
        campos_row.append(f'"{n[len(PREFIXO):]}", [{cn}]')
    row = "ROW (\n        " + ",\n        ".join(campos_row) + "\n    )"
    tab = ind(tabela_etapas(), 8)
    return f"""// Consulta de conferência do Fluxo v2 (tubo, espiral, carretéis). GERADO por gerar_medidas_paginas_fluxo.py: não edite à mão.
// Onde rodar: Power BI Desktop com GMS_PainelTeste.pbip aberto (ligado ao vivo ao (GMS)) -> Exibição de consulta DAX -> colar -> Executar.
// As medidas abaixo (DEFINE) são cópia exata das medidas do relatório 'Fluxo · ...' (reportExtensions.json), com prefixo 'Conf2 · ' para não colidir.
// Recorte: dCalendario[Date] <= 06/10/2026 (a virada 05:20 vem da regra: fim em 07/10 antes das 05:20 conta no dia 06/10).
//
// Esperado (validação do piloto em 03/11, Data de Referência, mesmo período; LEIAME_Pagina.md, fim):
//   1) Por etapa: a linha "Tranç+Esp com máquina lixo" ≈ Trançagem do piloto (6.654 m/dia · 6,8 pessoas · 1,02 p/1.000 m);
//      Trançagem + Espiral (cartões, sem máquina lixo) um pouco abaixo; Cabine ≈ 5.508 m/dia e 4,8 pessoas (0,88 p/1.000 m);
//      Tubo ≈ 7.203 · 2,3; Cobertura ≈ 6.650 · 2,6; Bandagem ≈ 6.383 · 3,2; Vulcanização ≈ 6.524 · 2,2; Debandagem ≈ 5.541 · 2,0.
//      "fatia com carretel" < 1 nas etapas com bitola 7, 3, 5, 17 ou vazia (os metros contam; o carretel fica n/d).
//   2) Totais: dias produtivos ≈ 185; rendimento ≈ cabine ÷ trançagem+espiral; lead time (mediana) ≈ 22 h.
//      Eficiência de balanceamento na série de 7 etapas (Trançagem+Espiral = 1 etapa, máquinas paralelas). Na leitura
//      automática a restrição nunca pode ser "Espiral" sozinha (piloto: Debandagem); a frase de mão de obra cita a
//      etapa individual (pode ser Espiral) e compara com a média do trecho (7 etapas).
//   3) Turno = 1 (texto de fHoraHora[Turno] com "1"): cabine 1º turno ≈ 1.920 m/dia e ≈ 1,6 pessoa; o nº de dias
//      produtivos NÃO muda (o corte de 3.000 m é do dia inteiro).
DEFINE
{chr(10).join(defs)}

// 1) Por etapa, todos os turnos
EVALUATE
CALCULATETABLE (
{tab},
    {filtro_data}
)

// 2) Totais (as mesmas medidas dos cartões de KPI e dos gráficos), todos os turnos
EVALUATE
CALCULATETABLE (
    {row},
    {filtro_data}
)

// 3) Por etapa, só o 1º turno (filtro direto em fHoraHora[Turno], como a segmentação)
EVALUATE
CALCULATETABLE (
{tab},
    {filtro_data},
    {filtro_t1}
)
"""


# ---- validacao -------------------------------------------------------------
RX_OBJ = re.compile(r"^\s*(table|column|measure|hierarchy|level)\s+('(?:[^']|'')*'|[^\s=]+)")


def nome_tmdl(s):
    return s[1:-1].replace("''", "'") if s.startswith("'") else s


def le_tmdl():
    """{tabela: {'column', 'measure', 'hierarchy', 'level'}} + {tabela: {coluna: defaultHierarchy}}."""
    tabelas, variacoes = {}, {}
    for f in (TMDL / "tables").glob("*.tmdl"):
        atual, atual_col = None, None
        for linha in f.read_text(encoding="utf-8-sig").splitlines():
            m = RX_OBJ.match(linha)
            if m:
                tipo, nome = m.group(1), nome_tmdl(m.group(2))
                if tipo == "table":
                    atual = tabelas.setdefault(nome, {"column": set(), "measure": set(), "hierarchy": set(),
                                                      "level": set()})
                    atual_col = None
                    nome_tab = nome
                elif atual is not None:
                    atual[tipo].add(nome)
                    atual_col = nome if tipo == "column" else None
                continue
            s = linha.strip()
            if atual_col and s.startswith("defaultHierarchy:"):
                variacoes.setdefault(nome_tab, {})[atual_col] = s.split(":", 1)[1].strip()
    return tabelas, variacoes


def campos(o):
    if isinstance(o, dict):
        if "HierarchyLevel" in o:
            yield ("HierarchyLevel",) + chave(o)[1:]
            return
        for k in ("Column", "Measure"):
            v = o.get(k)
            if isinstance(v, dict) and "Property" in v:
                sr = v.get("Expression", {}).get("SourceRef", {})
                if sr.get("Entity"):
                    yield k, sr["Entity"], v["Property"], sr.get("Schema")
        for v in o.values():
            yield from campos(v)
    elif isinstance(o, list):
        for v in o:
            yield from campos(v)


def campos_ao_vivo(rel):
    """Campos que as paginas existentes do GMS_Painel ja usam (provados no modelo ao vivo, que o snapshot nao tem)."""
    vivos = set()
    for f in (rel / "definition" / "pages").glob("*/visuals/*/visual.json"):
        if f.parts[-4] in PAGINAS:
            continue
        for c in campos(le(f)):
            if c[0] in ("Column", "Measure") and c[3] is None:
                vivos.add((c[0], c[1], c[2]))
    return vivos


def tira_strings(s):
    return re.sub(r'"(?:[^"]|"")*"', '""', s)


def vars_repetidas(e):
    """Nomes de VAR declarados mais de uma vez na expressao (o DAX nao diferencia maiusculas e recusa repetir
    mesmo em escopo aninhado). Devolve os nomes como aparecem."""
    vistos, rep_ = {}, []
    for v in re.findall(r"\bVAR\s+([^\s=]+)", tira_strings(e)):
        k = v.lower()
        if k in vistos and v not in rep_:
            rep_.append(v)
        vistos.setdefault(k, v)
    return rep_


def valida_dax(nome, e, colunas_ficha, nomes_rel, tabelas_modelo=()):
    erros = []
    rep_ = vars_repetidas(e)
    if rep_:
        erros.append(f"{nome}: VAR repetida na mesma medida (maiusculas nao contam): {', '.join(rep_)}")
    tab_low = {t.lower() for t in tabelas_modelo}
    for v in sorted({v for v in re.findall(r"\bVAR\s+([^\s=]+)", tira_strings(e)) if v.lower() in tab_low}):
        erros.append(f"{nome}: VAR '{v}' tem o nome de uma tabela do modelo")
    sem = tira_strings(e)
    for a, b in (("(", ")"), ("{", "}"), ("[", "]")):
        if sem.count(a) != sem.count(b):
            erros.append(f"{nome}: '{a}' e '{b}' desbalanceados")
    if e.count('"') % 2:
        erros.append(f"{nome}: aspas desbalanceadas")
    for v in re.findall(r"\bVAR\s+([^\s=]+)", sem):
        if not re.fullmatch(r"__[A-Za-z0-9]+", v):
            erros.append(f"{nome}: VAR '{v}' fora do padrao __Nome (evita palavra reservada do DAX)")
    for c in re.findall(r"ficha_producao\[([^\]]+)\]", sem):
        if c not in colunas_ficha:
            erros.append(f"{nome}: coluna ficha_producao[{c}] nao existe no TMDL")
    for r in re.findall(r"(?<![\w\]'])\[([^\]]+)\]", sem):
        if r in nomes_rel:
            erros.append(f"{nome}: chama a medida do relatorio [{r}] (nao pode: escrever por extenso)")
    if "__LP" in sem and f"ISFILTERED ( {COL_TURNO} )" not in sem:
        erros.append(f"{nome}: nao le a segmentacao de turno (ISFILTERED ( {COL_TURNO} ))")
    if "ALL ( ficha_producao )" in sem and "VAR __Datas = CALCULATETABLE ( VALUES ( dCalendario[Date] )" not in sem:
        erros.append(f"{nome}: precisa capturar a selecao do dCalendario antes de limpar a ficha")
    if re.search(r"Turno_|Etapas\[", sem):
        erros.append(f"{nome}: usa Turno_* da ficha ou a tabela Etapas (proibido)")
    return erros


def valida(rel, checar_idem=True):
    erros = []
    tabelas, variacoes = le_tmdl()
    vivos = campos_ao_vivo(rel)
    d = rel / "definition"
    for arq in [d / "report.json", d / "pages" / "pages.json", d / "reportExtensions.json"]:
        try:
            le(arq)
        except Exception as ex:  # noqa: BLE001
            erros.append(f"{arq.name}: JSON invalido ({ex})")
    ext = le(d / "reportExtensions.json")
    medidas_ext = [m for en in ext.get("entities", []) for m in en.get("measures", [])]
    nomes_ext = [m["name"] for m in medidas_ext]
    dup = {n for n in nomes_ext if nomes_ext.count(n) > 1}
    if dup:
        erros.append(f"reportExtensions: nomes repetidos {sorted(dup)}")
    nomes_modelo = {n for t in tabelas.values() for n in t["measure"]} | {n for t in tabelas.values() for n in t["column"]}
    fluxo = [m for m in medidas_ext if m["name"].startswith(PREFIXO)]
    esperadas = {n for n, *_ in medidas()}
    if {m["name"] for m in fluxo} != esperadas:
        erros.append("reportExtensions: medidas 'Fluxo · ' diferentes das geradas (rode sem --validar)")
    for m in fluxo:
        if m["name"] in nomes_modelo:
            erros.append(f"medida '{m['name']}' colide com nome do modelo")
        erros += valida_dax(m["name"], m["expression"], tabelas["ficha_producao"]["column"], set(nomes_ext),
                            tabelas.keys())
        if m.get("dataType") not in ("Double", "Text"):
            erros.append(f"{m['name']}: dataType invalido")
        if "SVG" in m["name"] and m.get("dataCategory") != "ImageUrl":
            erros.append(f"{m['name']}: SVG sem dataCategory ImageUrl")
    erros += valida_dax("Consulta_Conferencia_v2 (tabela por etapa)", tabela_etapas(),
                        tabelas["ficha_producao"]["column"], set(nomes_ext), tabelas.keys())
    meta = le(d / "pages" / "pages.json")
    if meta.get("pageOrder", [])[-2:] != list(PAGINAS):
        erros.append("pages.json: as 2 paginas do fluxo nao estao no fim")
    if meta.get("activePageName") in PAGINAS:
        erros.append("pages.json: pagina ativa mudou para o fluxo")
    for p in meta.get("pageOrder", []):
        if not (d / "pages" / p / "page.json").exists():
            erros.append(f"pages.json cita {p}, que nao existe")
    grupos, total = {}, 0
    for nome in PAGINAS:
        pdir = d / "pages" / nome
        try:
            pg = le(pdir / "page.json")
            if (pg.get("name"), pg.get("width"), pg.get("height"), pg.get("displayOption")) != (nome, W_PAG, H_PAG, "FitToPage"):
                erros.append(f"{nome}/page.json: precisa de name = pasta, 1280x720 e FitToPage")
        except Exception as ex:  # noqa: BLE001
            erros.append(f"{nome}/page.json: {ex}")
            continue
        caixas, vistos = [], set()
        for f in sorted(pdir.glob("visuals/*/visual.json")):
            total += 1
            v = le(f)
            n = v.get("name")
            if n != f.parent.name or n in vistos:
                erros.append(f"{nome}/{f.parent.name}: nome de visual repetido ou diferente da pasta")
            vistos.add(n)
            p = v["position"]
            x, y, w, h = p["x"], p["y"], p["width"], p["height"]
            if x < MARGEM or y < MARGEM or x + w > W_PAG - MARGEM or y + h > H_PAG - MARGEM:
                erros.append(f"{nome}/{n}: fora da area util ({x},{y},{w},{h})")
            caixas.append((n, x, y, x + w, y + h))
            for c in campos(v):
                k, ent, prop = c[0], c[1], c[2]
                if k == "HierarchyLevel":
                    col_, var_, hier, lvl = prop.split(".", 3)
                    dh = variacoes.get(ent, {}).get(col_, "")
                    loc = dh.split(".")[0]
                    if var_ != "Variation" or not dh.endswith(f"'{hier}'") or lvl not in tabelas.get(loc, {}).get("level", set()):
                        erros.append(f"{nome}/{n}: nivel {ent}.{prop} nao existe no TMDL")
                elif k == "Measure" and c[3] == "extension":
                    if prop not in nomes_ext:
                        erros.append(f"{nome}/{n}: medida do relatorio '{prop}' nao existe no reportExtensions")
                elif k == "Measure" and ent == M and prop in nomes_ext:
                    erros.append(f"{nome}/{n}: medida do relatorio '{prop}' sem Schema 'extension'")
                else:
                    tipo = "column" if k == "Column" else "measure"
                    if not (prop in tabelas.get(ent, {}).get(tipo, set()) or (k, ent, prop) in vivos):
                        erros.append(f"{nome}/{n}: {tipo} '{ent}[{prop}]' nao existe no TMDL nem nas paginas atuais")
            for q in v.get("visual", {}).get("query", {}).get("queryState", {}).values():
                for pr in q.get("projections", []):
                    _, ent, prop = chave(pr["field"])
                    if pr.get("queryRef") != f"{ent}.{prop}":
                        erros.append(f"{nome}/{n}: queryRef '{pr.get('queryRef')}' nao bate com o campo")
            sg = v.get("visual", {}).get("syncGroup")
            if sg:
                cp = v["visual"]["query"]["queryState"]["Values"]["projections"][0]["queryRef"]
                grupos.setdefault(sg["groupName"], set()).add((nome, cp))
        esq = min(c[1] for c in caixas)
        dir_ = W_PAG - max(c[3] for c in caixas)
        if esq != dir_:
            erros.append(f"{nome}: margens laterais diferentes ({esq} x {dir_})")
        for i, a in enumerate(caixas):
            for b in caixas[i + 1:]:
                if a[1] < b[3] and b[1] < a[3] and a[2] < b[4] and b[2] < a[4]:
                    erros.append(f"{nome}: '{a[0]}' sobrepoe '{b[0]}'")
    for g, membros in grupos.items():
        if {m[0] for m in membros} != set(PAGINAS) or len({m[1] for m in membros}) != 1:
            erros.append(f"syncGroup '{g}': precisa do mesmo campo nas 2 paginas ({sorted(membros)})")
    turno = [g for g, ms in grupos.items() if {m[1] for m in ms} == {"fHoraHora.Turno"}]
    if len(turno) != 1:
        erros.append("segmentacao 'Turno' (fHoraHora[Turno]) precisa existir nas 2 paginas com o mesmo syncGroup")
    # encaixe das imagens: o cartao SVG (com o cabecalho invisivel ~10 px) cabe no visual sem rolagem
    if CARD_W + 8 + 10 > CARD_VW or CARD_H + 14 > CARD_VH:
        erros.append("cartao SVG nao cabe no visual sem rolagem")
    if CONT_W + 8 + 10 > 616 - 28 or CONT_H + 14 > 340 - 24:
        erros.append("SVG de conteudo nao cabe no visual sem rolagem")
    if checar_idem:
        for c, t in saidas(rel).items():
            if not c.exists() or c.read_text(encoding="utf-8") != t:
                erros.append(f"idempotencia: {c.name} ({c.parent.name}) mudaria numa nova geracao")
                break
    if erros:
        print("VALIDACAO FALHOU:")
        for e in erros:
            print("  -", e)
        return False
    print(f"validacao ok: {len(fluxo)} medidas 'Fluxo · ' (DAX conferido), {total} visuais, campos no TMDL/paginas "
          f"atuais, {len(grupos)} grupos de sincronizacao (Turno incluso), sem sobreposicao, margem >= {MARGEM} px, "
          "idempotente")
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
