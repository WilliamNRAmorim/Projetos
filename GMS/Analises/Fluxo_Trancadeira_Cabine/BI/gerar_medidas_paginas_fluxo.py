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
CORTE_DIA = 3000        # dia produtivo: trancagem (linha inteira, toda maquina e todo turno) >= 3.000 m no dia
VIRADA_MIN = 320        # 05:20
T2_MIN, T3_MIN = 837, 1340  # 2o turno a partir de 13:57, 3o a partir de 22:20 (norma, MEL-250)
LT_MIN, LT_MAX = 0.5, 1440   # lead time do processo: fim do mandril -> fim da cabine
CARRETEL = [(4, 800), (6, 680), (8, 680), (10, 460), (12, 400), (16, 250)]  # bitola -> metros por carretel
BRAIDERS = ["TH01", "TH02", "TH03", "TH04", "TH05", "TH06", "TH07", "TM01", "TM04", "TO04"]
ESPIRAL = ["SPIRAL", "TE01", "TE0"]   # a mesma maquina (Spiral no app = TE01 na planilha): chave normalizada SPIRAL

# Processo inteiro em serie (William, 05/11): 8 etapas, do Mandril ("Solda de mandril", nome da tela no app) a Cabine.
# A Espiral nao e etapa: e maquina da Trancagem e vira FILTRO de maquina por ficha (04/11).
# (E, nome, coluna do fim, quantidade, operador)
ETAPAS = [
    (1, "Solda de mandril", "data_hora_final_mandril", "quantidade_mandril", "operador_mandril"),
    (2, "Tubo", "data_hora_final_tubo", "quantidade_tubo", "operador_tubo"),
    (3, "Trançagem", "data_hora_final_trancadeira", "quantidade_trancagem", "operador_trancagem"),
    (4, "Cobertura", "data_hora_final_cobertura", "quantidade_cobertura", "operador_cobertura"),
    (5, "Bandagem", "data_hora_final_bandagem", "quantidade_bandagem", "operador_bandagem"),
    (6, "Vulcanização", "data_hora_final_vulcanizacao", "quantidade_vulcanizacao", "operador_vulcanizacao"),
    (7, "Debandagem", "data_hora_final_debandagem", "quantidade_debandagem", "operador_debandagem"),
    (8, "Cabine (teste)", "data_hora_final_extracao", "quantidade_extracao", "operador_extracao"),
]
NOME = {e: n for e, n, *_ in ETAPAS}
TODAS = [e for e, *_ in ETAPAS]
TR, CAB = 3, 8
MAQ_LISTA = BRAIDERS + ["Spiral"]   # itens da segmentacao Maquina (filtro de nivel do visual)
COL_MAQ = "ficha_producao[Trançadeira]"   # segmentacao de Maquina (coluna existente da ficha)
COL_TURNO = "fHoraHora[Turno]"            # segmentacao de Turno (coluna que o GMS_Painel ja usa na pagina Hora-Hora)

ACENTOS = [("Á", "A"), ("À", "A"), ("Â", "A"), ("Ã", "A"), ("Ä", "A"), ("É", "E"), ("È", "E"), ("Ê", "E"),
           ("Ë", "E"), ("Í", "I"), ("Ì", "I"), ("Î", "I"), ("Ï", "I"), ("Ó", "O"), ("Ò", "O"), ("Ô", "O"),
           ("Õ", "O"), ("Ö", "O"), ("Ú", "U"), ("Ù", "U"), ("Û", "U"), ("Ü", "U"), ("Ç", "C"), ("Ñ", "N")]


# ---- nucleo DAX ------------------------------------------------------------
def fc(c):
    return f"ficha_producao[{c}]"


# Nomes de VAR: o DAX nao diferencia maiusculas e nao aceita repetir um nome na mesma medida, nem em escopo aninhado
# (erro do Desktop em 04/11: "__La" da paleta x "__LA" do nucleo). Toda VAR aninhada leva o sufixo da fonte (s);
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


def norm_maq(col_expr, s):
    """Maquina normalizada: maiusculas, sem ponto, hifen, espaco e sublinhado; SPIRAL, TE01 e TE0 = 'SPIRAL'."""
    lim = col_expr
    for p in (".", "-", " ", "_"):
        lim = f'SUBSTITUTE ( {lim}, "{p}", "" )'
    es = ", ".join(f'"{x}"' for x in ESPIRAL)
    return f'VAR __mq{s} = UPPER ( {lim} ) RETURN IF ( __mq{s} IN {{ {es} }}, "SPIRAL", __mq{s} )'


def carretel(c, s):
    """VARs __c<s> (quantidade), __cv<s> (quantidade limpa) e __mc<s> (metros do carretel da bitola)."""
    sw = ", ".join(f"{b}, {m}" for b, m in CARRETEL)
    return (f"VAR __c{s} = {fc(c)} VAR __cv{s} = IF ( __c{s} > {QTD_MAX}, BLANK (), __c{s} ) "
            f"VAR __mc{s} = SWITCH ( ficha_producao[Bitola], {sw} )")


def fonte(e, fim, q, op, com_op, com_car, s):
    """Linhas ficha x etapa concluida, no dia da selecao. @M = maquina da ficha (vale para TODAS as etapas dela)."""
    cols = [f'"@E", {e}', f'"@Dia", {dia_ref(fim, s)}', f'"@T", {turno_do_fim(fim, s)}', f'"@Q", {qtd(q, s)}',
            f'"@M", {norm_maq(COL_MAQ, s)}']
    if com_op:
        cols.append(f'"@Op", {norm_op(op)}')
    if com_car:
        cols.append(f'"@Car", {carretel(q, s + "Car")} RETURN DIVIDE ( __cv{s}Car, __mc{s}Car )')
        cols.append(f'"@Cob", {carretel(q, s + "Cob")} RETURN IF ( NOT ISBLANK ( __mc{s}Cob ), __cv{s}Cob )')
    corpo = ",\n            ".join(cols)
    return (f"FILTER (\n        SELECTCOLUMNS (\n            FILTER ( ALL ( ficha_producao ), NOT ISBLANK ( {fc(fim)} ) ),\n"
            f"            {corpo}\n        ),\n        [@Dia] IN __Datas\n    )")


def nucleo(etapas=TODAS, com_op=False, com_car=False, com_lt=False):
    """VARs comuns. etapas: quais E entram (a Trancagem entra sempre: define o dia produtivo).

    Contexto: as selecoes (datas do dCalendario, turnos da fHoraHora[Turno], maquinas da ficha_producao[Trançadeira])
    sao capturadas em VAR ANTES de qualquer limpeza. A ficha e lida com ALL ( ficha_producao ), que ignora o
    relacionamento ativo DataProducao -> dCalendario e a propria segmentacao de maquina; o dia vem da data de
    referencia calculada aqui, e turno e maquina sao reaplicados por linha. Sem Turno_* da ficha nem Etapas[Turno]."""
    fontes = [fonte(str(e), fim, q, op, com_op, com_car, f"S{e}") for e, _, fim, q, op in ETAPAS
              if e in etapas or e == TR]
    base = fontes[0] if len(fontes) == 1 else "UNION (\n    " + ",\n    ".join(fontes) + "\n)"
    v = [
        "VAR __Datas = CALCULATETABLE ( VALUES ( dCalendario[Date] ), REMOVEFILTERS ( fHoraHora[Turno] ), "
        f"REMOVEFILTERS ( {COL_MAQ} ) )",
        "VAR __UmDia = COUNTROWS ( __Datas ) = 1",
        f"VAR __FT = ISFILTERED ( {COL_TURNO} )",
        "VAR __Turnos =\n    FILTER (\n        SELECTCOLUMNS (\n"
        f"            CALCULATETABLE ( VALUES ( {COL_TURNO} ), REMOVEFILTERS ( dCalendario ) ),\n"
        f'            "@T", VAR __tTx = {COL_TURNO} & "" VAR __tP1 = SEARCH ( "1", __tTx, 1, 999 ) '
        'VAR __tP2 = SEARCH ( "2", __tTx, 1, 999 ) VAR __tP3 = SEARCH ( "3", __tTx, 1, 999 ) '
        "VAR __tPm = MIN ( MIN ( __tP1, __tP2 ), __tP3 ) "
        "RETURN IF ( __tPm = 999, BLANK (), IF ( __tPm = __tP1, 1, IF ( __tPm = __tP2, 2, 3 ) ) )\n"
        "        ),\n        NOT ISBLANK ( [@T] )\n    )",
        # Maquina: FILTERS devolve so o que a segmentacao escolheu (sem o filtro cruzado das datas)
        f"VAR __FM = ISFILTERED ( {COL_MAQ} )",
        f'VAR __Maqs = DISTINCT ( SELECTCOLUMNS ( FILTERS ( {COL_MAQ} ), "@M", {norm_maq(COL_MAQ, "Sel")} ) )',
        'VAR __MaqTxt = CONCATENATEX ( FILTER ( __Maqs, [@M] <> "" ), [@M], ", ", [@M], ASC )',
        'VAR __TemSp = "SPIRAL" IN __Maqs',
        'VAR __TemBr = NOT ISEMPTY ( FILTER ( __Maqs, [@M] <> "SPIRAL" ) )',
        'VAR __NomeTr = IF ( NOT __FM || ( __TemSp && __TemBr ), "Trançagem + Espiral", '
        'IF ( __TemSp, "Espiral", "Trançagem" ) )',
        "VAR __B =\n" + base,
        f"VAR __BTr = FILTER ( __B, [@E] = {TR} )",
        'VAR __DiasCom = DISTINCT ( SELECTCOLUMNS ( __B, "@Dia", [@Dia] ) )',
        # dia produtivo: linha inteira (toda maquina, todo turno), como o corte do turno
        "VAR __DiasProd =\n    FILTER (\n        __DiasCom,\n        VAR __dProd = [@Dia]\n"
        f"        RETURN __UmDia || SUMX ( FILTER ( __BTr, [@Dia] = __dProd ), [@Q] ) >= {CORTE_DIA}\n    )",
        "VAR __nD = COUNTROWS ( __DiasProd )",
        "VAR __LA = FILTER ( __B, ( NOT __FT || [@T] IN __Turnos ) && ( NOT __FM || [@M] IN __Maqs ) )",
        "VAR __LP = FILTER ( __LA, [@Dia] IN __DiasProd )",
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
        for e in etapas:
            v.append(f"VAR __Pp{e} = DIVIDE ( COUNTROWS ( FILTER ( __P, [@E] = {e} ) ), __nD )")
            v.append(f"VAR __K{e} = DIVIDE ( __Pp{e}, DIVIDE ( __M{e}, 1000 ) )")
        if set(etapas) == set(TODAS):
            v.append("VAR __Kt = { " + ", ".join(f"( {e}, __K{e} )" for e in TODAS) + " }")
            v.append("VAR __Kv = FILTER ( __Kt, NOT ISBLANK ( [Value2] ) )")
            v.append("VAR __KMedia = AVERAGEX ( __Kv, [Value2] )")
            v.append("VAR __KMaior = MAXX ( __Kv, [Value2] )")
    if com_car:
        for e in etapas:
            v.append(f"VAR __C{e} = DIVIDE ( SUMX ( FILTER ( __LP, [@E] = {e} ), [@Car] ), __nD )")
            v.append(f"VAR __Cob{e} = DIVIDE ( SUMX ( FILTER ( __LP, [@E] = {e} ), [@Cob] ), "
                     f"SUMX ( FILTER ( __LP, [@E] = {e} ), [@Q] ) )")
    if set(etapas) == set(TODAS):
        v.append("VAR __Vt = { " + ", ".join(f"( {e}, __M{e} )" for e in TODAS) + " }")
    if com_lt:
        fe, ft = "data_hora_final_extracao", "data_hora_final_mandril"  # lead time do processo inteiro
        v.append(
            "VAR __LTt =\n    FILTER (\n        SELECTCOLUMNS (\n"
            f"            FILTER ( ALL ( ficha_producao ), NOT ISBLANK ( {fc(fe)} ) && NOT ISBLANK ( {fc(ft)} ) ),\n"
            f'            "@Dia", {dia_ref(fe, "LT")},\n            "@T", {turno_do_fim(fe, "LT")},\n'
            f'            "@M", {norm_maq(COL_MAQ, "LT")},\n'
            f'            "@LT", ( {fc(fe)} - {fc(ft)} ) * 24\n        ),\n'
            f"        [@Dia] IN __Datas && ( NOT __FT || [@T] IN __Turnos ) && ( NOT __FM || [@M] IN __Maqs )\n"
            f"            && [@LT] >= {LT_MIN} && [@LT] <= {LT_MAX}\n"
            "    )")
        v.append("VAR __LTMediana = MEDIANX ( FILTER ( __LTt, [@Dia] IN __DiasProd ), [@LT] )")
        v.append("VAR __LTMedio = AVERAGEX ( __LTt, [@LT] )")
        v.append("VAR __Ini = MINX ( __DiasCom, [@Dia] )")
        v.append("VAR __Fim = MAXX ( __DiasCom, [@Dia] )")
        v.append(f"VAR __Lambda = DIVIDE ( SUMX ( FILTER ( __LA, [@E] = {CAB} ), [@Q] ), INT ( __Fim - __Ini ) + 1 )")
        v.append("VAR __WIP = IF ( NOT ISBLANK ( __Lambda ) && NOT ISBLANK ( __LTMedio ), __Lambda * __LTMedio / 24 )")
    return "\n".join(v)


def nome_etapa_dax(var_idx):
    """Nome da etapa; a Trancagem leva o nome dinamico do filtro de maquina (__NomeTr)."""
    pares = ", ".join((f"{e}, __NomeTr" if e == TR else f'{e}, "{n}"') for e, n in NOME.items())
    return f"SWITCH ( {var_idx}, {pares} )"


def cv_dax():
    return (f"VAR __DiasCV = FILTER ( __DiasCom, VAR __dCV = [@Dia] RETURN SUMX ( FILTER ( __BTr, [@Dia] = __dCV ), [@Q] ) >= {CORTE_DIA} )\n"
            f"VAR __TRt = FILTER ( __LA, [@E] = {TR} )\n"
            "VAR __CV =\n    IF (\n        COUNTROWS ( __DiasCV ) >= 2,\n        DIVIDE (\n"
            "            STDEVX.S ( __DiasCV, VAR __dSd = [@Dia] RETURN SUMX ( FILTER ( __TRt, [@Dia] = __dSd ), [@Q] ) + 0 ),\n"
            "            AVERAGEX ( __DiasCV, VAR __dAv = [@Dia] RETURN SUMX ( FILTER ( __TRt, [@Dia] = __dAv ), [@Q] ) + 0 )\n"
            "        )\n    )")


def eficiencia_dax():
    """Balanceamento nas 8 etapas em serie (do mandril a cabine)."""
    return "VAR __Ef = DIVIDE ( SUMX ( __Kv, [Value2] ), COUNTROWS ( __Kv ) * __KMaior )"


def restricoes_dax():
    return ("VAR __iV = MAXX ( TOPN ( 1, FILTER ( __Vt, [Value2] > 0 ), [Value2], ASC, [Value1], ASC ), [Value1] )\n"
            "VAR __iC = MAXX ( TOPN ( 1, FILTER ( __Kt, [Value2] > 0 ), [Value2], DESC, [Value1], ASC ), [Value1] )\n"
            "VAR __MenorV = MINX ( FILTER ( __Vt, [Value2] > 0 ), [Value2] )")


# ---- SVG -------------------------------------------------------------------
# Paleta clara aprovada (Medidas_SVG_FluxoTrancagemCabine.md); '#' vira '%23' no data URI.
CORES = [("Ca", "ffffff"), ("Ti", "14130f"), ("Su", "55534d"), ("Li", "e1e0d9"), ("La", "eb6834"),
         ("LaF", "fdebe3"), ("LaT", "b34510"), ("Ve", "0a6a0a"), ("VeF", "e8f5e8"), ("SeF", "ff8a50"),
         ("SeT", "11161d"), ("On", "2a78d6"), ("Off", "cfd6df"), ("VeB", "0ca30c")]
SVG_VARS = " ".join(f'VAR __cor{n} = "%23{h}"' for n, h in CORES)
CARD_W, CARD_H = 272, 184      # viewBox e tamanho da imagem do cartao (2 x 4 em 1.248 px, sem rolagem)
ICONES_MAX = 12
PASSO_ICONE = 17
# width/height = tamanho do visual Imagem que mostra o SVG; viewBox = coordenadas do desenho (mesma proporcao)
SVG_ABRE = ("\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='{w}' height='{h}' "
            "viewBox='0 0 {vw} {vh}' font-family='Segoe UI, sans-serif'>\"")


def svg_cartao(e, n):
    """Cartao horizontal 272 x 184: ETAPA n, nome, icones de pessoa, numero de carreteis (sem desenho de carretel,
    William 05/11), barra de m/dia e caixa de m/pessoa.
    Cartao 2 (Trancagem): nome pelo filtro de maquina (Trançagem + Espiral / Trançagem / Espiral)."""
    nome = '" & __NomeTr & "' if e == TR else n
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
        & "<text x='14' y='43' font-size='15' font-weight='700' fill='" & __corTi & "'>{nome}</text>"
VAR __Pessoas =
    "<g transform='translate(14 50)'>" & __IcP & __XP & "</g>"
        & "<text x='14' y='84' fill='" & __corTi & "'><tspan font-size='14' font-weight='700'>" & IF ( ISBLANK ( __Pes ), "–", FORMAT ( __Pes, "0.0", "pt-BR" ) ) & "</tspan>"
        & "<tspan font-size='10.5' fill='" & __corSu & "'> pessoas/dia" & IF ( NOT ISBLANK ( __Max ), " · máx " & FORMAT ( __Max, "0" ) ) & "</tspan></text>"
VAR __Carreteis =
    IF (
        __Car > 0,
        "<text x='14' y='110' fill='" & __corTi & "'><tspan font-size='14' font-weight='700'>" & FORMAT ( __Car, "0.0", "pt-BR" ) & "</tspan>"
            & "<tspan font-size='10.5' fill='" & __corSu & "'> carretéis/dia" & IF ( NOT ISBLANK ( __CPe ), " · " & FORMAT ( __CPe, "0.0", "pt-BR" ) & " por pessoa" ) & "</tspan></text>"
            & IF ( __Cob < 0.995, "<text x='14' y='125' font-size='9.5' fill='" & __corSu & "'>carretéis em " & FORMAT ( __Cob * 100, "0" ) & "%25 dos metros</text>" ),
        IF ( __Met > 0, "<text x='14' y='110' font-size='10.5' fill='" & __corSu & "'>carretéis n/d (bitola fora da tabela)</text>" )
    )
VAR __Barra =
    "<rect x='14' y='144' width='136' height='8' rx='4' fill='" & __corLi & "'/>"
        & IF ( __Lb > 0, "<rect x='14' y='144' width='" & FORMAT ( __Lb, "0.0", "en-US" ) & "' height='8' rx='4' fill='" & __corOn & "'/>" )
        & "<text x='14' y='170' fill='" & __corTi & "'><tspan font-size='13' font-weight='700'>" & IF ( ISBLANK ( __Met ), "–", FORMAT ( __Met, "#,0", "pt-BR" ) ) & "</tspan><tspan font-size='10.5'> m/dia</tspan></text>"
VAR __Caixa =
    "<rect x='156' y='136' width='102' height='38' rx='8' fill='" & IF ( __Quente, __corLaF, __corVeF ) & "'/>"
        & "<text x='164' y='153' fill='" & __corTi & "'><tspan font-size='14' font-weight='700' fill='" & IF ( __Quente, __corLaT, __corVe ) & "'>" & IF ( ISBLANK ( __MPe ), "–", FORMAT ( __MPe, "#,0", "pt-BR" ) ) & "</tspan><tspan font-size='10'> m/pessoa</tspan></text>"
        & "<text x='164' y='167' font-size='9' fill='" & __corSu & "'>" & IF ( ISBLANK ( __Con ), "–", FORMAT ( __Con, "0.00", "pt-BR" ) ) & " p/1.000 m</text>"
RETURN
    IF (
        __SemDado,
        BLANK (),
        {SVG_ABRE.format(w=CARD_VW, h=CARD_VH, vw=CARD_W, vh=CARD_H)}
            & __Contorno & __Selo & __Cab & __Pessoas & __Carreteis & __Barra & __Caixa & "</svg>"
    )"""
    return corpo


CONT_VW, CONT_VH = 1248, 340  # visual Imagem t_conteudo = tamanho do SVG (William ampliou a barra em 05/11)
CONT_DX, CONT_DY = 24, 20     # desenho dentro do cartao branco do proprio SVG
CONT_W, CONT_H = 1200, 300    # desenho das 8 barras
PASSO_CONT = 32
CONT_X0, CONT_BW = 170, 940   # inicio e largura da barra; rotulo da etapa a esquerda, valor a direita


def svg_conteudo():
    linhas = []
    for i, e in enumerate(TODAS):
        y = 36 + i * PASSO_CONT
        nome = '" & __NomeTr & "' if e == TR else NOME[e]
        linhas.append(
            f"VAR __Pos{e} = IF ( NOT ISBLANK ( __K{e} ), COUNTROWS ( FILTER ( __Kt, [Value2] > __K{e} ) ) + 1 )\n"
            f"VAR __Q{e} = NOT ISBLANK ( __Pos{e} ) && __Pos{e} <= 2\n"
            f"VAR __L{e} = IF ( __Esc > 0 && __K{e} > 0, ROUND ( {CONT_BW} * DIVIDE ( __K{e}, __Esc ), 1 ), 0 )\n"
            f"VAR __R{e} =\n"
            f"    \"<text x='0' y='{y + 16}' font-size='12' fill='\" & __corTi & \"'>{nome}</text>\"\n"
            f"        & \"<rect x='{CONT_X0}' y='{y + 4}' width='{CONT_BW}' height='16' rx='5' fill='\" & __corLi & \"'/>\"\n"
            f"        & IF ( __L{e} > 0, \"<rect x='{CONT_X0}' y='{y + 4}' width='\" & FORMAT ( __L{e}, \"0.0\", \"en-US\" ) & \"' height='16' rx='5' fill='\" & IF ( __Q{e}, __corLa, __corVeB ) & \"'/>\" )\n"
            f"        & \"<text x='{CONT_W - 4}' y='{y + 17}' text-anchor='end' font-size='13' font-weight='700' fill='\" & IF ( __Q{e}, __corLaT, __corTi ) & \"'>\" & IF ( ISBLANK ( __K{e} ), \"–\", FORMAT ( __K{e}, \"0.00\", \"pt-BR\" ) ) & \"</text>\"")
    y_fim = 36 + len(TODAS) * PASSO_CONT
    juntar = " & ".join(f"__R{e}" for e in TODAS)
    return f"""{nucleo(TODAS, com_op=True)}
{SVG_VARS}
VAR __Esc = __KMaior * 1.1
VAR __XM = IF ( __Esc > 0 && NOT ISBLANK ( __KMedia ), FORMAT ( {CONT_X0} + ROUND ( {CONT_BW} * DIVIDE ( __KMedia, __Esc ), 1 ), "0.0", "en-US" ) )
{chr(10).join(linhas)}
VAR __Titulo =
    "<text x='0' y='16' fill='" & __corTi & "'><tspan font-size='13' font-weight='700'>Quais etapas usam mais gente por 1.000 m?</tspan>"
        & "<tspan font-size='11' fill='" & __corSu & "'>" & IF ( NOT ISBLANK ( __KMedia ), "  ·  tracejado = média " & FORMAT ( __KMedia, "0.00", "pt-BR" ) ) & "</tspan></text>"
VAR __Media =
    IF ( NOT ISBLANK ( __XM ), "<line x1='" & __XM & "' x2='" & __XM & "' y1='30' y2='{y_fim}' stroke='" & __corTi & "' stroke-width='1.5' stroke-dasharray='4 3'/>" )
RETURN
    IF (
        ISBLANK ( __KMaior ),
        BLANK (),
        {SVG_ABRE.format(w=CONT_VW, h=CONT_VH, vw=CONT_VW, vh=CONT_VH)}
            & "<rect x='0.5' y='0.5' width='{CONT_VW - 1}' height='{CONT_VH - 1}' rx='12' fill='" & __corCa & "' stroke='" & __corLi & "' stroke-width='1'/>"
            & "<g transform='translate({CONT_DX} {CONT_DY})'>" & __Titulo & {juntar} & __Media & "</g></svg>"
    )"""


# ---- medidas ---------------------------------------------------------------
def m_simples(etapas, com_op, ret, com_car=False, com_lt=False, extra=""):
    return f"{nucleo(etapas, com_op=com_op, com_car=com_car, com_lt=com_lt)}\n{extra}{'' if not extra else chr(10)}RETURN\n    {ret}"


def medidas():
    """[(nome, tipo, DAX, formato, categoria, pasta)]"""
    ms = []
    pv = PASTA
    pvis = PASTA + "\\Visual"
    ms.append((PREFIXO + "Vazão Cabine (m/dia)", "Double", m_simples([CAB], False, f"__M{CAB}"), "#,0", None, pv))
    ms.append((PREFIXO + "Vazão Trançagem (m/dia)", "Double", m_simples([TR], False, f"__M{TR}"), "#,0", None, pv))
    ms.append((PREFIXO + "Pessoas nas 8 Etapas", "Double",
               m_simples(TODAS, True,
                         'DIVIDE ( COUNTROWS ( DISTINCT ( SELECTCOLUMNS ( __P, "@Dia", [@Dia], "@Pe", [@Pe] ) ) ), __nD )'),
               "#,0.0", None, pv))
    ms.append((PREFIXO + "Pessoas Trançagem (por dia)", "Double", m_simples([TR], True, f"__Pp{TR}"), "#,0.0", None, pv))
    ms.append((PREFIXO + "Pessoas Cabine (por dia)", "Double", m_simples([CAB], True, f"__Pp{CAB}"), "#,0.0", None, pv))
    ms.append((PREFIXO + "Pessoas Trançagem / Cabine", "Text", m_simples([TR, CAB], True,
               f'IF ( NOT ISBLANK ( __Pp{TR} ) || NOT ISBLANK ( __Pp{CAB} ), '
               f'IF ( ISBLANK ( __Pp{TR} ), "–", FORMAT ( __Pp{TR}, "0.0", "pt-BR" ) ) & " / " & '
               f'IF ( ISBLANK ( __Pp{CAB} ), "–", FORMAT ( __Pp{CAB}, "0.0", "pt-BR" ) ) )'), None, None, pv))
    ms.append((PREFIXO + "m por Pessoa Cabine", "Double",
               m_simples([CAB], True, f"DIVIDE ( __M{CAB}, __Pp{CAB} )"), "#,0", None, pv))
    ms.append((PREFIXO + "Eficiência de Balanceamento", "Double",
               m_simples(TODAS, True, "__Ef", extra=eficiencia_dax()), "0%", None, pv))
    ms.append((PREFIXO + "Lead Time do Processo (h)", "Double", m_simples([CAB], False, "__LTMediana", com_lt=True),
               "#,0", None, pv))
    ms.append((PREFIXO + "WIP Little (m)", "Double", m_simples([CAB], False, "__WIP", com_lt=True), "#,0", None, pv))
    ms.append((PREFIXO + "CV Vazão Trançagem", "Double", m_simples([TR], False, "__CV", extra=cv_dax()),
               "0.0%", None, pv))
    ms.append((PREFIXO + "Rendimento de Fluxo", "Double",
               m_simples([TR, CAB], False, f"DIVIDE ( __M{CAB}, __M{TR} )"), "0%", None, pv))
    ms.append((PREFIXO + "Dias Produtivos", "Double", m_simples([TR], False, "IF ( __nD > 0, __nD )"),
               "#,0", None, pv))
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
    (PREFIXO + "Pessoas nas 8 Etapas", "pessoas diferentes", "#,0.0"),
    (PREFIXO + "Pessoas Trançagem / Cabine", "pessoas tranç./cab.", None),
    (PREFIXO + "m por Pessoa Cabine", "m/pessoa cabine", "#,0"),
    (PREFIXO + "Eficiência de Balanceamento", "eficiência", "0%"),
    (PREFIXO + "Lead Time do Processo (h)", "lead time processo", '#,0 "h"'),
    (PREFIXO + "WIP Little (m)", "em processo", '#,0 "m"'),
    (PREFIXO + "CV Vazão Trançagem", "CV vazão", "0.0%"),
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


def v_imagem(medida, alt):
    """Visual Imagem nativo com a URL = medida SVG (fx -> valor do campo). Vencedor do teste de 04/11 (pagina
    pg_teste_tooltip, variante B): desenha o SVG inteiro e NAO mostra o texto bruto 'data:image/svg+xml...' ao passar o
    mouse. Tabela/matriz mostra esse texto (atributo title nativo da celula) mesmo com a dica de ferramenta desligada;
    o cartao novo (cardVisual) tambem. Propriedades copiadas exatamente da variante B (sem modo de ajuste: o SVG ja
    tem o tamanho do visual). Dica de ferramenta desligada."""
    return {
        "visualType": "image",
        "objects": {"image": [{"properties": {"sourceType": txt("imageUrl"), "sourceUrl": {"expr": mx(medida)}}}]},
        "visualContainerObjects": {
            **caixa(None, fundo=False, pad=0, alt=alt),
            "visualTooltip": [{"properties": {"show": boo(False)}}],
        },
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
LINHA2 = "Ficha de produção · dia de 05:20 a 05:20 · média dos dias com trançagem ≥ 3.000 m na linha"
RODAPE = ("Pessoas = operadores distintos que apontaram a etapa no dia · máx = maior dia do período "
          "(estimativa, não é escala oficial).")
LEGENDA = ("Laranja = 2 etapas com mais gente por 1.000 m (p/1.000 m) · carretel: 4→800 m, 6 e 8→680, 10→460, "
           "12→400, 16→250; n/d = bitola fora da tabela · turno pelo fim da etapa · máquina filtra a ficha inteira")


def filtro_lista_maquinas():
    """Filtro de NIVEL DO VISUAL (basico) na segmentacao Maquina: so as maquinas que existem (William, 05/11). Nao filtra
    as medidas: sem selecao direta na segmentacao, todas as fichas entram. Sai quando a limpeza da fonte terminar."""
    ent, prop = "ficha_producao", "Trançadeira"
    return {
        "name": "f_lista_maquinas", "field": col(ent, prop), "type": "Categorical",
        "filter": {"Version": 2, "From": [{"Name": "f", "Entity": ent, "Type": 0}],
                   "Where": [{"Condition": {"In": {
                       "Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "f"}}, "Property": prop}}],
                       "Values": [[{"Literal": {"Value": "'" + m + "'"}}] for m in MAQ_LISTA]}}}]},
        "howCreated": "User",
    }
Y_FAIXA, H_FAIXA = 16, 64
Y_CONT = Y_FAIXA + H_FAIXA + 12          # 92
Y_RODAPE, H_RODAPE = 672, 32
FIM_CONT = Y_RODAPE - 12                 # 660
# 5 segmentacoes de 124 px (passo 136) de 596 a 1264; titulo 16-584.
SEG_W, SEG_X0, W_TITULO = 124, 596, 568
SEGMENTACOES = [  # (nome, campo, rotulo, grupo, x)
    ("seg_ano", col("dCalendario", "Ano"), "Ano", "fluxo_ano", SEG_X0),
    ("seg_mes", col("dCalendario", "Mês"), "Mês", "fluxo_mes", SEG_X0 + 136),
    ("seg_dia", col("dCalendario", "Dia"), "Dia", "fluxo_dia", SEG_X0 + 2 * 136),
    ("seg_turno", col("fHoraHora", "Turno"), "Turno", "fluxo_turno", SEG_X0 + 3 * 136),
    # Maquina: coluna existente da ficha; as medidas leem a escolha (ISFILTERED + FILTERS) e filtram a ficha inteira
    ("seg_maquina", col("ficha_producao", "Trançadeira"), "Máquina", "fluxo_maquina", SEG_X0 + 4 * 136),
]
# Pagina 1: KPIs 92-188; cartoes 2 x 4 de 303 x 205 (200-405 e 417-622); legenda 634-660.
# 303 x 205 = proporcao do desenho 272 x 184 (1,478): o SVG preenche o visual Imagem sem sobra nem corte.
H_KPI = 96
CARD_VW, CARD_VH, GAP = 303, 205, 12


def faixa_comum(p, titulo1, outras):
    p.add("titulo", 16, Y_FAIXA, W_TITULO, H_FAIXA, v_texto([(titulo1, 18, "Segoe UI Semibold", HEX_TINTA),
                                                         (LINHA2, 10, "Segoe UI", HEX_SUAVE)]))
    for nome, campo, rot, grupo, x in SEGMENTACOES:
        seg = v_segmentacao(campo, rot, grupo)
        if nome == "seg_maquina":
            seg["filterConfig"] = {"filters": [filtro_lista_maquinas()]}  # a lista ja exclui vazio e lixo
        p.add(nome, x, Y_FAIXA, SEG_W, H_FAIXA, seg)
    p.add("rodape", 16, Y_RODAPE, 576, H_RODAPE, v_texto([(RODAPE, 9, "Segoe UI", HEX_SUAVE)]))
    p.add("nav", 608, Y_RODAPE, 368, H_RODAPE, v_navegador(outras))
    p.add("atualizado", 992, Y_RODAPE, 272, H_RODAPE, v_carimbo())


def pg_fluxo_1(outras):
    p = Pagina("pg_fluxo_1", "Fluxo · Etapas")
    faixa_comum(p, "Fluxo mandril → cabine · etapas e carretéis", outras)
    p.add("kpis", 16, Y_CONT, 1248, H_KPI, v_kpis())
    y0 = Y_CONT + H_KPI + GAP                                         # 200
    slots = [(f"cartao_{e}", nome_svg(e), n,
              f"Etapa {e}, {n}: pessoas por dia, carretéis por dia, metros por dia e metros por pessoa.")
             for e, n, *_ in ETAPAS]
    for i, (nome, medida, rot, alt) in enumerate(slots):   # 8 etapas na grade 2 x 4
        lin, colu = divmod(i, 4)
        x = 16 + colu * (CARD_VW + GAP)
        y = y0 + lin * (CARD_VH + GAP)
        p.add(nome, x, y, CARD_VW, CARD_VH, v_imagem(medida, alt))
    y_leg = y0 + 2 * CARD_VH + GAP + GAP                               # 634
    p.add("legenda", 16, y_leg, 1248, FIM_CONT - y_leg, v_texto([(LEGENDA, 9, "Segoe UI", HEX_SUAVE)],
                                                                alt="Legenda das cores e dos carretéis."))
    return p


def pg_fluxo_2(outras):
    p = Pagina("pg_fluxo_2", "Fluxo · Mão de obra")
    faixa_comum(p, "Fluxo mandril → cabine · mão de obra", outras)
    y_g = Y_CONT + CONT_VH + 12                     # 444
    h_g = FIM_CONT - y_g                            # 216
    p.add("t_conteudo", 16, Y_CONT, CONT_VW, CONT_VH, v_imagem(
        PREFIXO + "SVG Conteúdo",
        "Pessoas a cada 1.000 m nas 8 etapas; laranja são as duas com mais gente por metro; tracejado é a média."))
    # Leitura automatica removida pelo William em 05/11; a barra ocupa a largura toda (1248 x 340).
    p.add("g_metros", 16, y_g, 616, h_g, v_colunas(
        [(PREFIXO + "Vazão Trançagem (m/dia)", "Trançagem", HEX_AZUL),
         (PREFIXO + "Vazão Cabine (m/dia)", "Cabine", HEX_LARANJA)],
        "Metros por dia · média dos dias produtivos, por mês",
        "Colunas por mês: metros por dia da trançagem e da cabine, média dos dias produtivos.", "#,0", 8))
    p.add("g_pessoas", 648, y_g, 616, h_g, v_colunas(
        [(PREFIXO + "Pessoas Trançagem (por dia)", "Trançagem", HEX_AZUL),
         (PREFIXO + "Pessoas Cabine (por dia)", "Cabine", HEX_LARANJA)],
        "Pessoas por dia · média dos dias produtivos, por mês",
        "Colunas por mês: pessoas por dia na trançagem e na cabine, média dos dias produtivos.",
        "#,0.0", 9))
    return p



# Pagina de experimento do teste de 04/11 (dica nativa do SVG): concluido, a variante B (visual Imagem) virou o padrao.
# O gerador so a remove, se ainda existir na copia.
PG_EXP = "pg_teste_tooltip"


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
    outras = [p for p in meta.get("pageOrder", []) if p not in PAGINAS and p != PG_EXP]
    meta["pageOrder"] = outras + list(PAGINAS)
    out = {d / "reportExtensions.json": dumps(ext), d / "pages" / "pages.json": dumps(meta)}
    paginas = [pg_fluxo_1(outras), pg_fluxo_2(outras)]
    for p in paginas:
        pagina = {
            "$schema": f"{SCH}/page/{V_PAGE}/schema.json", "name": p.nome, "displayName": p.titulo,
            "displayOption": "FitToPage", "height": H_PAG, "width": W_PAG,
            "objects": {"background": [{"properties": {"color": cor_hex(HEX_PAGINA), "transparency": num(0)}}],
                        "outspace": [{"properties": {"color": cor_hex(HEX_PAGINA), "transparency": num(0)}}]}}
        out[d / "pages" / p.nome / "page.json"] = dumps(pagina)
        for v in p.visuais:
            out[d / "pages" / p.nome / "visuals" / v["name"] / "visual.json"] = dumps(v)
    out[ARQ_CONF] = consulta_conferencia()
    return out


def gera(rel):
    out = saidas(rel)
    for nome in PAGINAS + (PG_EXP,):
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
    lim = COL_MAQ
    for c in (".", "-", " ", "_"):
        lim = f'SUBSTITUTE ( {lim}, "{c}", "" )'
    es = ", ".join(f'"{x}"' for x in ESPIRAL)
    br = ", ".join(f'"{x}"' for x in BRAIDERS)
    filtro_sp = f"FILTER ( ALL ( {COL_MAQ} ), UPPER ( {lim} ) IN {{ {es} }} )"
    filtro_br = f"FILTER ( ALL ( {COL_MAQ} ), UPPER ( {lim} ) IN {{ {br} }} )"
    defs, campos_row = [], []
    for n, t, e, f, cat, _ in medidas():
        if cat:
            continue
        cn = "Conf2 · " + n[len(PREFIXO):]
        defs.append(f"    MEASURE {M}[{cn}] =\n{ind(e, 8)}")
        campos_row.append(f'"{n[len(PREFIXO):]}", [{cn}]')
    restr = (f"{nucleo(TODAS, com_op=True)}\n{restricoes_dax()}\n"
             f"RETURN\n    IF ( NOT ISBLANK ( __iV ), {nome_etapa_dax('__iV')} & \" (\" & FORMAT ( __MenorV, \"#,0\" ) & \" m/dia)\" )")
    defs.append(f"    MEASURE {M}[Conf2 · Restrição (menor m/dia)] =\n{ind(restr, 8)}")
    campos_row.append('"Restrição (menor m/dia)", [Conf2 · Restrição (menor m/dia)]')
    row = "ROW (\n        " + ",\n        ".join(campos_row) + "\n    )"
    tab = ind(tabela_etapas(), 8)
    return f"""// Consulta de conferência do Fluxo v2 (mandril → cabine, filtro de máquina, carretéis). GERADO por gerar_medidas_paginas_fluxo.py: não edite à mão.
// Onde rodar: Power BI Desktop com GMS_PainelTeste.pbip aberto (ligado ao vivo ao (GMS)) -> Exibição de consulta DAX -> colar -> Executar.
// As medidas abaixo (DEFINE) são cópia exata das medidas do relatório 'Fluxo · ...' (reportExtensions.json), com prefixo 'Conf2 · ' para não colidir.
// 'Conf2 · Restrição' só existe aqui (a leitura automática saiu da página 2).
// Recorte: dCalendario[Date] <= 06/10/2026 (a virada 05:20 vem da regra: fim em 07/10 antes das 05:20 conta no dia 06/10).
//
// Esperado:
//   1) Por etapa, sem filtro de máquina (TODAS as fichas): Cabine ≈ 5.679 m/dia e 4,9 pessoas e Trançagem ≈ 6.724 m/dia e
//      6,7 pessoas (iguais à 3ª geração, conferida no Desktop em 04/11: o mandril não muda as outras etapas nem o dia
//      produtivo). Solda de mandril ≈ 8.185 m/dia e 3,2 pessoas (piloto de 03/11; o mandril corta lance longo, ver LEIAME).
//      Piloto: Tubo ≈ 7.203 · 2,3; Cobertura ≈ 6.650 · 2,6; Bandagem ≈ 6.383 · 3,2; Vulcanização ≈ 6.524 · 2,2;
//      Debandagem ≈ 5.541 · 2,0. "fatia com carretel" < 1 onde há bitola 7, 3, 5, 17 ou vazia.
//   2) Totais: dias produtivos ≈ 185; rendimento = cabine ÷ trançagem; eficiência de balanceamento nas 8 etapas;
//      lead time do processo (mediana por ficha, fim do mandril → fim da cabine, 0,5 a 1.440 h): número novo, sem
//      referência (o do trecho trançagem→cabine era ≈ 22 h; o do processo tem de ser maior); restrição = a etapa de menor m/dia.
//   3) Turno = 1 (texto de fHoraHora[Turno] com "1"): cabine 1º turno ≈ 1.920 m/dia e ≈ 1,6 pessoa; dias produtivos iguais.
//   4) Só Spiral (Spiral/TE01/TE0): Trançagem ≈ 669 m/dia; as outras etapas (mandril incluso) só com as fichas da espiral.
//   5) Sem Spiral (TH01–TH07, TM01, TM04, TO04): Trançagem ≈ 6.055 m/dia; 4) + 5) ≈ 1) em metros, a menos das fichas de
//      máquina vazia/lixo, que só entram sem filtro.
DEFINE
{chr(10).join(defs)}

// 1) Por etapa, todos os turnos, todas as máquinas
EVALUATE
CALCULATETABLE (
{tab},
    {filtro_data}
)

// 2) Totais (as mesmas medidas dos cartões de KPI, dos gráficos e da leitura), todos os turnos e máquinas
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

// 4) Por etapa, só a espiral (filtro direto em ficha_producao[Trançadeira], como a segmentação Máquina)
EVALUATE
CALCULATETABLE (
{tab},
    {filtro_data},
    {filtro_sp}
)

// 5) Por etapa, sem a espiral (só braiders)
EVALUATE
CALCULATETABLE (
{tab},
    {filtro_data},
    {filtro_br}
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
    if "__LP" in sem and (f"ISFILTERED ( {COL_MAQ} )" not in sem or f"FILTERS ( {COL_MAQ} )" not in sem
                          or "[@M] IN __Maqs" not in sem):
        erros.append(f"{nome}: nao aplica o filtro de maquina por ficha (ISFILTERED/FILTERS ( {COL_MAQ} ))")
    if re.search(r"Espiral\b", tira_strings(nome)) or "Tranç+Esp" in nome:
        erros.append(f"{nome}: Espiral nao e mais etapa (vira filtro de maquina)")
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
    # A pagina ativa e a que o William deixou aberta ao salvar no Desktop: o gerador nunca a muda (nao e erro).
    for p in meta.get("pageOrder", []):
        if not (d / "pages" / p / "page.json").exists():
            erros.append(f"pages.json cita {p}, que nao existe")
    grupos, total, n_svg = {}, 0, 0
    svgs = {m["name"] for m in medidas_ext if m.get("dataCategory") == "ImageUrl"}
    if PG_EXP in meta.get("pageOrder", []) or (d / "pages" / PG_EXP).exists():
        erros.append(f"pagina de experimento {PG_EXP} ainda esta na copia (rode o gerador)")
    expr_svg = {m["name"]: m["expression"] for m in medidas_ext if m.get("dataCategory") == "ImageUrl"}
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
            # visual com imagem SVG: dica de ferramenta desligada (senao mostra o texto bruto do data URI)
            usa_svg = any(c[0] == "Measure" and c[3] == "extension" and c[2] in svgs for c in campos(v))
            tip = v.get("visual", {}).get("visualContainerObjects", {}).get("visualTooltip", [{}])
            if usa_svg and tip[0].get("properties", {}).get("show") != boo(False):
                erros.append(f"{nome}/{n}: imagem SVG com dica de ferramenta ligada (visualTooltip.show = false)")
            if usa_svg:
                n_svg += 1
                vis = v.get("visual", {})
                props = vis.get("objects", {}).get("image", [{}])[0].get("properties", {})
                url = props.get("sourceUrl", {}).get("expr", {}).get("Measure", {})
                med = url.get("Property")
                if vis.get("visualType") != "image" or props.get("sourceType") != txt("imageUrl") or med not in svgs \
                        or url.get("Expression", {}).get("SourceRef", {}).get("Schema") != "extension":
                    erros.append(f"{nome}/{n}: SVG tem de ir em visual Imagem (image.sourceType 'imageUrl', "
                                 "image.sourceUrl = medida do relatorio); tabela mostra o texto bruto ao passar o mouse")
                else:
                    mt = re.search(r"<svg xmlns='[^']*' width='(\d+)' height='(\d+)' viewBox='0 0 (\d+) (\d+)'",
                                   expr_svg[med])
                    if not mt:
                        erros.append(f"{nome}/{n}: SVG de '{med}' sem width/height/viewBox")
                    else:
                        sw, sh, vbw, vbh = map(int, mt.groups())
                        if (sw, sh) != (w, h):
                            erros.append(f"{nome}/{n}: SVG de {sw}x{sh} num visual de {w}x{h} (sobra ou corte)")
                        if abs(vbw / vbh - w / h) > 0.01 * (w / h):
                            erros.append(f"{nome}/{n}: proporcao do desenho {vbw}x{vbh} diferente do visual {w}x{h}")
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
    # estrutura pedida pelo William em 05/11: 8 cartoes, sem Linha, sem leitura, barra de conteudo 1248 x 340,
    # mandril como 1a etapa, sem desenho de carretel, segmentacao Maquina com a lista final (filtro de nivel do visual)
    pg1 = d / "pages" / "pg_fluxo_1" / "visuals"
    pg2 = d / "pages" / "pg_fluxo_2" / "visuals"
    if {f.name for f in pg1.glob("cartao_*")} != {f"cartao_{e}" for e in TODAS}:
        erros.append("pg_fluxo_1: precisa de exatamente os 8 cartoes cartao_1..cartao_8 (sem cartao_linha)")
    if (pg2 / "t_leitura").exists() or any(m["name"] == PREFIXO + "Leitura Automática" for m in fluxo):
        erros.append("pg_fluxo_2: a leitura automatica saiu (visual e medida)")
    if (pg2 / "t_conteudo" / "visual.json").exists():
        pc = le(pg2 / "t_conteudo" / "visual.json")["position"]
        if (pc["x"], pc["y"], pc["width"], pc["height"]) != (16, Y_CONT, 1248, 340):
            erros.append("pg_fluxo_2/t_conteudo: precisa ficar em x16 y92 1248 x 340")
    else:
        erros.append("pg_fluxo_2/t_conteudo: nao existe")
    if ETAPAS[0][2] != "data_hora_final_mandril":
        erros.append("o mandril (Solda de mandril) tem de ser a 1a etapa")
    for m in fluxo:
        if "SVG" in m["name"] or m["name"].startswith(PREFIXO + "Lead Time"):
            if "data_hora_final_mandril" not in m["expression"]:
                erros.append(f"{m['name']}: nao inclui o mandril")
        if m["name"].startswith(PREFIXO + "SVG ") and ("gradientUnits='userSpaceOnUse'" in m["expression"]
                                                        or "__IcC" in m["expression"]):
            erros.append(f"{m['name']}: ainda desenha o carretel (so o numero fica)")
    for pg in PAGINAS:
        f = d / "pages" / pg / "visuals" / "seg_maquina" / "visual.json"
        if not f.exists():
            continue
        fs = le(f).get("filterConfig", {}).get("filters", [])
        vals = [x[0]["Literal"]["Value"].strip("'") for fl in fs if fl.get("type") == "Categorical"
                for x in fl["filter"]["Where"][0]["Condition"]["In"]["Values"]]
        if sorted(vals) != sorted(MAQ_LISTA):
            erros.append(f"{pg}/seg_maquina: filtro de nivel do visual precisa ser so {', '.join(MAQ_LISTA)}")
    for campo_seg, rot in (("fHoraHora.Turno", "Turno"), ("ficha_producao.Trançadeira", "Máquina")):
        if len([g for g, ms in grupos.items() if {m[1] for m in ms} == {campo_seg}]) != 1:
            erros.append(f"segmentacao '{rot}' ({campo_seg}) precisa existir nas 2 paginas com o mesmo syncGroup")
    # desenho de conteudo: barras dentro do desenho e desenho dentro do cartao do SVG
    if 36 + len(TODAS) * PASSO_CONT > CONT_H:
        erros.append("SVG de conteudo: as barras passam da altura do desenho")
    if CONT_DX + CONT_W > CONT_VW - 8 or CONT_DY + CONT_H > CONT_VH - 8:
        erros.append("SVG de conteudo: desenho passa do cartao")
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
          f"atuais, {len(grupos)} grupos de sincronizacao (Turno e Maquina), {n_svg} imagens SVG em visual Imagem sem dica, sem sobreposicao, margem >= {MARGEM} px, "
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
