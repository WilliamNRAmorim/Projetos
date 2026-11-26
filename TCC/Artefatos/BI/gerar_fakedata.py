# -*- coding: utf-8 -*-
"""
gerar_fakedata.py - gera dados FICTICIOS para o modelo semantico do GMS (artefato do TCC).

Le as colunas e tipos declarados nos .tmdl de GMS_Painel_TCC.SemanticModel/definition/tables
e REESCREVE o `source` da particao de cada tabela real (as que vinham de listas SharePoint)
para um literal M embutido:

    let Source = #table(type table [Col = tipo, ...], { {linha}, ... }) in Source

Assim o Atualizar do Power BI Desktop nao precisa de arquivo, rede nem credencial.
Nao mexe em relacionamentos, medidas, colunas calculadas, tabelas calculadas (DAX) nem nas
tabelas de data automaticas. Tambem troca as duas expressoes M de SharePoint (expressions.tmdl)
por tabelas vazias inline.

Uso:  python gerar_fakedata.py            (pode rodar de novo: e idempotente)
Todos os nomes, OPs, mangueiras e operadores sao inventados. Semente fixa.
"""
import glob
import os
import random
import re
import sys
from datetime import datetime, timedelta

AQUI = os.path.dirname(os.path.abspath(__file__))
MODELO = os.path.join(AQUI, "GMS_Painel_TCC.SemanticModel", "definition")
TABELAS = os.path.join(MODELO, "tables")

R = random.Random(20261125)

# ----------------------------------------------------------------------------
# Domino ficticio
# ----------------------------------------------------------------------------
INI = datetime(2026, 8, 3)          # segunda
AGORA = datetime(2026, 10, 30, 14, 0)
ULT_INICIO_OP = datetime(2026, 10, 26)

# (mangueira, construcao, dash)
MANGUEIRAS = [
    ("GH100-04", "TEXTILE", 4), ("GH100-06", "TEXTILE", 6), ("GH100-08", "TEXTILE", 8),
    ("GH100-10", "TEXTILE", 10), ("GH195-04", "SD20-04/06", 4), ("GH195-06", "SD20-04/06", 6),
    ("GH195-08", "SD24-08/10/12", 8), ("GH195-10", "SD24-08/10/12", 10),
    ("GH250-06", "DD20-04/06", 6), ("GH250-08", "DD24-08/10/12", 8),
    ("GH250-12", "DD24-08/10/12", 12), ("GH300-16", "SD/DD36-16", 16),
    ("GH400-12", "SPIRAL", 12),
]
PESO_MANG = [10, 14, 12, 6, 6, 10, 8, 5, 6, 6, 4, 2, 3]

TRANCADEIRAS = ["TR%02d" % i for i in range(1, 12)]            # 11 trancadeiras
CELULAS_MONT = ["HIGH", "FF1", "FF2", "FF3", "Bundle", "Acessorios", "Conexão"]
META_HORA_MONT = {"HIGH": 18, "FF1": 50, "FF2": 62, "FF3": 31, "Bundle": 2, "Acessorios": 62, "Conexão": 187}
OPERADORES = ["Operador %02d" % i for i in range(1, 25)]
CABINES = ["Cabine 1", "Cabine 2"]

CODIGOS_ERRO = [
    "E01 - Vazamento no teste", "E02 - Diâmetro fora de especificação", "E03 - Defeito de cobertura",
    "E04 - Trança irregular", "E05 - Bolha no tubo", "E06 - Marca de bandagem",
    "E07 - Comprimento fora de tolerância", "E08 - Contaminação",
]

OP_BASE = 100101
N_OP = 300


def dias_uteis(a, b):
    d = a
    while d <= b:
        if d.weekday() < 5:
            yield d
        d += timedelta(days=1)


def turno_de(dt):
    tm = dt.hour * 60 + dt.minute
    if 320 <= tm < 820:
        return 1
    if 820 <= tm < 1340:
        return 2
    return 3


def pick_mang():
    return R.choices(MANGUEIRAS, weights=PESO_MANG)[0]


def motivos_parada():
    """Le a lista de motivos da tabela calculada dMotivoParada (nao e alterada)."""
    txt = open(os.path.join(TABELAS, "dMotivoParada.tmdl"), encoding="utf-8").read()
    pares = re.findall(r'\{"((?:[^"\\]|\\.)*)", "([A-Za-zçãõé]+)"\}', txt)
    return [(m, t) for m, t in pares]


MOTIVOS = []

# ----------------------------------------------------------------------------
# Geracao das linhas (dict coluna -> valor) por tabela
# ----------------------------------------------------------------------------
FICHAS = []   # lista de dicts auxiliares para manter coerencia entre tabelas


def sistema(ts_, i):
    """Colunas de sistema do SharePoint que usamos (ID, Created, Modified, Version)."""
    return {"ID": i, "Created": ts_, "Modified": ts_, "Version": "1.0"}


def gerar_fichas():
    etapas = [
        # chave, (fila_min_h, fila_max_h), (proc_min_h, proc_max_h)
        ("mandril", (0, 0), (0.5, 2.0)),
        ("tubo", (1, 8), (1.0, 3.0)),
        ("tran", (2, 20), (2.0, 6.0)),
        ("cobertura", (1, 10), (1.0, 3.0)),
        ("bandagem", (1, 12), (1.5, 4.0)),
        ("vulc", (1, 6), (6.0, 9.0)),
        ("debandagem", (4, 16), (1.0, 3.0)),
        ("extracao", (1, 10), (1.0, 3.0)),
    ]
    dias = list(dias_uteis(INI, ULT_INICIO_OP))
    for k in range(N_OP):
        mang, constr, dash = pick_mang()
        op = OP_BASE + k
        dia = dias[int(k * len(dias) / N_OP)] if R.random() < 0.7 else R.choice(dias)
        t0 = dia + timedelta(hours=R.choice([5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 21]),
                             minutes=R.randint(0, 59))
        qtd = R.choice([300, 400, 450, 500, 600, 750, 800, 1000, 1200, 1500])
        f = {"i": k + 1, "op": op, "mang": mang, "constr": constr, "dash": dash, "qtd": qtd,
             "est": {}, "tran": R.choice(TRANCADEIRAS), "cabine": R.choice(CABINES),
             "mandril": "MND-%03d" % R.randint(1, 60)}
        t = t0
        fila_ini = t
        for chave, fila, proc in etapas:
            esperar = R.uniform(*fila)
            ini = fila_ini + timedelta(hours=esperar)
            fim = ini + timedelta(hours=R.uniform(*proc))
            if fim > AGORA:
                # ainda em processo ou na fila
                if ini <= AGORA:
                    f["est"][chave] = (fila_ini, ini, None)
                elif fila_ini <= AGORA:
                    f["est"][chave] = (fila_ini, None, None)
                break
            f["est"][chave] = (fila_ini, ini, fim)
            fila_ini = fim
        f["fim"] = f["est"].get("extracao", (None, None, None))[2]
        f["status"] = "Finalizado" if f["fim"] else "Em processo"
        if R.random() < 0.02 and f["fim"]:
            f["status"] = "Descartado"
        FICHAS.append(f)


def lin_ficha(f):
    e = f["est"]

    def g(chave, pos):
        v = e.get(chave)
        return v[pos] if v else None

    def tn(chave):
        d = g(chave, 2)
        return "Turno %d" % turno_de(d) if d else None

    r = {}
    r["ID"] = f["i"]
    r["processo"] = "Mangueira"
    r["Carretel Entrada"] = "CR-%04d" % R.randint(1, 800)
    r["Carretel Saida"] = "CR-%04d" % R.randint(1, 800)
    bit = float(f["dash"])
    if R.random() < 0.03:
        bit = None
    r["Bitola"] = bit
    r["Mangueira"] = f["mang"]
    r["OP"] = float(f["op"])
    r["status_processo"] = f["status"]
    r["Trançadeira"] = f["tran"]
    r["cod_mandril"] = f["mandril"]
    r["Turno_mandril"] = tn("mandril")
    r["data_hora_inicio_mandril"] = g("mandril", 1)
    r["data_hora_final_mandril"] = g("mandril", 2)
    r["lote_mandril"] = "LM-%04d" % R.randint(2600, 2699)
    r["desmoldante_mandril"] = R.choice(["DM-A", "DM-B"])
    r["diametro_mandril"] = float(f["dash"])
    r["operador_mandril"] = R.choice(OPERADORES)
    r["quantidade_mandril"] = float(f["qtd"])
    r["Turno_Tubo"] = tn("tubo")
    r["data_hora_inicio_tubo"] = g("tubo", 1)
    r["data_hora_final_tubo"] = g("tubo", 2)
    r["diametro_tubo"] = round(f["dash"] * 1.6 + R.uniform(-0.1, 0.1), 2)
    r["defeito_tubo"] = float(R.choice([0, 0, 0, 0, 1, 2, 3, 5]))
    r["quantidade_tubo"] = float(f["qtd"])
    r["operador_tubo"] = R.choice(OPERADORES)
    r["Turno_Trançagem"] = tn("tran")
    r["data_hora_final_trancadeira"] = g("tran", 2)
    r["data_hora_inicio_trancadeira"] = g("tran", 1)
    r["Diametro_Trançagem"] = round(f["dash"] * 1.9 + R.uniform(-0.1, 0.1), 2)
    r["quantidade_trancagem"] = float(f["qtd"])
    r["defeito_trancagem"] = float(R.choice([0, 0, 0, 1, 2, 4, 6]))
    r["operador_trancagem"] = R.choice(OPERADORES)
    r["Turno_Cobertura"] = tn("cobertura")
    r["data_hora_inicio_cobertura"] = g("cobertura", 1)
    r["data_hora_final_cobertura"] = g("cobertura", 2)
    r["diametro_cobertura"] = round(f["dash"] * 2.3 + R.uniform(-0.1, 0.1), 2)
    r["defeito_cobertura"] = float(R.choice([0, 0, 0, 0, 1, 2, 3]))
    r["quantidade_cobertura"] = float(f["qtd"])
    r["operador_cobertura"] = R.choice(OPERADORES)
    r["Turno_Bandagem"] = tn("bandagem")
    r["data_hora_inicio_bandagem"] = g("bandagem", 1)
    r["data_hora_final_bandagem"] = g("bandagem", 2)
    r["operador_bandagem"] = R.choice(OPERADORES)
    r["Cód_Fita_Bandagem"] = "FB-%02d" % R.randint(1, 6)
    r["Código_Filme_UHMWPE"] = "UH-%02d" % R.randint(1, 4)
    r["quantidade_bandagem"] = float(f["qtd"])
    r["data_hora_final_vulcanizacao"] = g("vulc", 2)
    r["data_hora_inicio_vulcanizacao"] = g("vulc", 1)
    r["Turno_Vulcanização"] = tn("vulc")
    vf = g("vulc", 2)
    r["InicioResfriamento_Vulcanizacao"] = (vf - timedelta(minutes=R.randint(40, 90))) if vf else None
    r["quantidade_vulcanizacao"] = float(f["qtd"])
    r["operador_vulcanizacao"] = R.choice(OPERADORES)
    r["Turno_Debandagem"] = tn("debandagem")
    r["data_hora_inicio_debandagem"] = g("debandagem", 1)
    r["data_hora_final_debandagem"] = g("debandagem", 2)
    r["quantidade_debandagem"] = float(f["qtd"])
    r["operador_debandagem"] = R.choice(OPERADORES)
    d = g("extracao", 2)
    r["Turno_Extr/Teste"] = float(turno_de(d)) if d else None
    r["data_hora_inicio_extracao"] = g("extracao", 1)
    r["data_hora_final_extracao"] = d
    r["quantidade_extracao"] = float(f["qtd"]) if d else None
    r["operador_extracao"] = R.choice(OPERADORES) if d else None
    r["Cod.Cobertura"] = "CC-%03d" % R.randint(100, 120)
    r["Cod.CompostoTubo"] = "CT-%03d" % R.randint(200, 215)
    r["Created"] = f["est"]["mandril"][0]
    base = g("mandril", 1) or f["est"]["mandril"][0]
    r["Data de Validade  do composto cobertura"] = datetime(base.year, base.month, base.day) + timedelta(days=R.randint(90, 300))
    r["Data de Validade do Composto Tubo"] = datetime(base.year, base.month, base.day) + timedelta(days=R.randint(90, 300))
    r["Lote Composto Tubo"] = "LT-%04d" % R.randint(1, 400)
    r["Lote_cobertura"] = "LC-%04d" % R.randint(1, 400)
    r["Lote_Trançagem"] = "LR-%04d" % R.randint(1, 400)
    r["N°Picks"] = str(R.choice([10, 12, 14, 16]))
    r["Cod_Trançagem"] = "TRN-%03d" % R.randint(1, 40)
    r["InicioAguardando_Trançadeira"] = g("tran", 0)
    r["InicioAguardando_Tubo"] = g("tubo", 0)
    r["InicioAguardando_bandagem"] = g("bandagem", 0)
    r["InicioAguardando_Vulcanização"] = g("vulc", 0)
    r["InicioAguardando_Debandagem"] = g("debandagem", 0)
    r["InicioAguardando_Extr./Teste"] = g("extracao", 0)
    r["InicioEmProcesso_Mandril"] = g("mandril", 1)
    r["InicioEmProcesso_Tubo"] = g("tubo", 1)
    r["InicioEmProcesso_Trançagem"] = g("tran", 1)
    r["InicioEmProcesso_Cobertura"] = g("cobertura", 1)
    r["InicioEmProcesso_Bandagem"] = g("bandagem", 1)
    r["InicioEmProcesso_Vulcanização"] = g("vulc", 1)
    r["InicioEmProcesso_Debandagem"] = g("debandagem", 1)
    r["InicioEmProcesso_Extr./Teste"] = g("extracao", 1)
    r["InicioAguardandoCobertura"] = g("cobertura", 0)
    # quantidade por turno (na etapa de extrusao, cobertura, bandagem, vulc., debandagem)
    def por_turno(prefixo_chave, nomes):
        d_ = g(prefixo_chave, 2)
        for n_ in nomes:
            r[n_] = 0.0
        if d_:
            r[nomes[turno_de(d_) - 1]] = float(f["qtd"])
    por_turno("tubo", ["Qtd_Turno1", "Qtd_Turno2", "Qtd_Turno3"])
    por_turno("cobertura", ["Qtd_Turno1_Cobertura", "Qtd_Turno2_Cobertura", "Qtd_Turno3_Cobertura"])
    por_turno("bandagem", ["Qtd_Turno1_Bandagem", " Qtd_Turno2_Bandagem", " Qtd_Turno3_Bandagem"])
    por_turno("vulc", ["Qtd_Turno1_Vulcanizacao", "Qtd_Turno2_Vulcanizacao", "Qtd_Turno3_Vulcanizacao"])
    por_turno("debandagem", ["Qtd_Turno1_Debandagem", "Qtd_Turno2_Debandagem", "Qtd_Turno3_Debandagem"])
    ultimo = max([v for est in e.values() for v in est if v] or [base])
    r["Modified"] = ultimo
    r["DataFinalizacao"] = d
    r["PackList Cabine"] = "PL-%d" % f["op"] if d else None
    r["ordem_producao"] = float(f["op"])
    r["cod_mangueira"] = f["mang"]
    r["lote"] = "L%d" % f["op"]
    r["Qtd. Planejada"] = float(f["qtd"])
    r["Turno"] = "Turno %d" % turno_de(base)
    r["Created By"] = None
    r["Version"] = "1.0"
    r["maquina_mandril"] = "Mandril %d" % R.randint(1, 2)
    r["cabine_teste"] = f["cabine"] if d else None
    return r


def tab_ficha_producao():
    return [lin_ficha(f) for f in FICHAS]


def tab_part_number():
    out = []
    for i, (m, c, d) in enumerate(MANGUEIRAS, 1):
        out.append({"Title": m, "Dash size": float(d), "Wide Braiders": R.choice(["Sim", "Não"]),
                    "Construction": c, "Braider": "B%02d" % R.randint(1, 4),
                    "ID": i, "Created": INI, "Modified": INI, "Version": "1.0"})
    return out


def tab_eventos():
    out = []
    n = 0
    amostra = [f for f in FICHAS if f["i"] % 5 in (0, 1) and f["fim"]]
    for f in amostra:
        for chave, nome, rec in (("tubo", "Extrusora 1", "EX1"), ("tran", "Trançadeira", f["tran"]),
                                 ("extracao", "Extração", f["cabine"])):
            fim = f["est"][chave][2]
            n += 1
            out.append({
                "Eventos": "EV-%05d" % n, "origem": "ficha_producao", "origem_ID": float(f["i"]),
                "etapa": nome, "tipo": "Fim", "data_hora": fim,
                "data_ref": datetime(fim.year, fim.month, fim.day), "turno": float(turno_de(fim)),
                "bitola": float(f["dash"]), "metros": float(f["qtd"]),
                "refugo": float(R.choice([0, 0, 0, 1, 2, 4])), "operador": R.choice(OPERADORES),
                "recurso": rec, "carretel": "CR-%04d" % R.randint(1, 800),
                "sobra": float(R.choice([0, 0, 5, 10, 20])),
            })
    return out


def tab_historico_carretel():
    out = []
    n = 0
    for f in FICHAS:
        if f["i"] % 3 != 0:
            continue
        for chave, nome in (("tubo", "Tubo"), ("tran", "Trançagem"), ("cobertura", "Cobertura")):
            est = f["est"].get(chave)
            if not est or not est[2]:
                continue
            n += 1
            ent = est[1]
            sai = est[2]
            out.append({
                "carretel_id": "CR-%04d" % R.randint(1, 800), "OP_ID": float(f["op"]), "etapa": nome,
                "mangueira": f["mang"], "metros_entrada": float(f["qtd"] + R.choice([0, 10, 20])),
                "metros_saida": float(f["qtd"]), "data_hora_entrada": ent, "data_hora_saida": sai,
                "operador": R.choice(OPERADORES), "status": "Consumido",
                "ID": n, "Created": ent, "Modified": sai, "Version": "1.0",
            })
    return out


CEL_HH = TRANCADEIRAS[:4]
DIA_HH_INI = datetime(2026, 9, 21)
META_BITOLA = {4: 90, 6: 80, 8: 70, 10: 60, 12: 50, 16: 40}
# (rotulo, hora_ini, min_ini, minutos, turno)
JANELAS = ([("05:20 - 06:00", 5, 20, 40, 1)] +
           [("%02d:00 - %02d:00" % (h, h + 1), h, 0, 60, 1) for h in range(6, 14)] +
           [("%02d:00 - %02d:00" % (h, h + 1), h, 0, 60, 2) for h in range(14, 22)] +
           [("22:00 - 23:00", 22, 0, 60, 3), ("23:00 - 00:00", 23, 0, 60, 3)] +
           [("%02d:00 - %02d:00" % (h, h + 1), h, 0, 60, 3) for h in range(0, 5)])
REFEICAO = {"11:00 - 12:00": 1, "19:00 - 20:00": 2, "02:00 - 03:00": 3}


def tab_fhorahora():
    """Hora-Hora completo (1 linha por celula x dia produtivo x janela), com ou sem parada."""
    por_cel = {c: [] for c in CEL_HH}
    for f in FICHAS:
        e = f["est"].get("tran")
        if f["tran"] in por_cel and e and e[1] and e[2]:
            por_cel[f["tran"]].append((e[1], e[2], f))
    for c in por_cel:
        por_cel[c].sort(key=lambda x: x[0])
    mot = [m for m, t_ in MOTIVOS if t_ not in ("Excedido", "Programada")]
    pesos = [3 if t_ in ("Material", "Processo", "Falha") else 1 for m, t_ in MOTIVOS if t_ not in ("Excedido", "Programada")]
    out = []
    n = 0
    for d in dias_uteis(DIA_HH_INI, datetime(2026, 10, 30)):
        for cel in CEL_HH:
            for rot, h, mi, minutos, turno in JANELAS:
                ini = datetime(d.year, d.month, d.day, h, mi) + (timedelta(days=1) if turno == 3 and h < 12 else timedelta())
                ficha = None
                for a, b, f in por_cel[cel]:
                    if a <= ini:
                        ficha = f
                if ficha is None:
                    ficha = FICHAS[CEL_HH.index(cel)]
                meta = float(META_BITOLA[ficha["dash"]])
                par = 0.0
                motivo = motivo2 = None
                if REFEICAO.get(rot) == turno and R.random() < 0.85:
                    par, motivo = 45.0, "21 - Refeição"
                elif R.random() < 0.07:
                    par = float(R.choice([5, 10, 15, 20, 30, 45]))
                    motivo = "%02d - %s" % (R.randint(1, 30), R.choices(mot, weights=pesos)[0])
                    if R.random() < 0.18:
                        motivo2 = "%02d - %s" % (R.randint(1, 30), R.choices(mot, weights=pesos)[0])
                real = round(meta * (minutos - par) / 60 * R.uniform(0.85, 1.05) * minutos / 60)
                n += 1
                out.append({"ID": n, "Data": d, "Turno": "%dº Turno" % turno, "Célula": cel, "Hora": rot,
                            "Mangueira": ficha["mang"], "Minutos": float(minutos),
                            "Meta Hora": float(round(meta * minutos / 60)), "Real. Hora": float(real),
                            "Tempo Parado (min)": par, "Motivo": motivo, "Motivo 2": motivo2,
                            "Status": "Fechado"})
    return out


def tab_hora_hora(fhh):
    """Linhas COM motivo (filtro da fonte original: celula preenchida e motivo diferente de refeicao)."""
    out = []
    for r in fhh:
        if r["Motivo"] and r["Motivo"] != "21 - Refeição":
            out.append({"Turno": r["Turno"], "Data": r["Data"], "Célula": r["Célula"],
                        "Tempo Parado (min)": r["Tempo Parado (min)"], "Motivo": r["Motivo"],
                        "Motivo 2": r["Motivo 2"],
                        "Comentário / Ação": R.choice([None, None, "Ajuste realizado", "Aguardando material", "Acionado apoio"]),
                        "Minutos": r["Minutos"]})
    return out


def tab_refugo_extrusora():
    ext = [f for f in FICHAS if f["est"].get("mandril") and f["est"]["mandril"][2]][:220]
    out = []
    codigos = ["1 - Defeito superficial", "2 - Set-Up", "3 - Bolha", "4 - Diâmetro fora", "5 - Contaminação", "6 - Outros"]
    for i, f in enumerate(R.sample(ext, 120), 1):
        fim = f["est"]["mandril"][2] + timedelta(minutes=R.randint(0, 40))
        out.append({"Title": "REF-MND-%04d" % i, "Bitola": float(f["dash"]), "cod_mandril": f["mandril"],
                    "CodigoErro": R.choice(codigos), "Quantidade": round(R.uniform(0.5, 15), 1),
                    "operador": R.choice(OPERADORES), "DataHoraRefugo": fim,
                    "Turno": "Turno %d" % turno_de(fim), "Observacao": None, "ID": i})
    return out


def tab_paradas_montagem(prod):
    out = []
    mot = [(m, t) for m, t in MOTIVOS]
    pesos = [4 if t == "Material" else 3 if t in ("Processo", "Organizacional") else 2 if t == "Excedido" else 1
             for m, t in mot]
    for d in dias_uteis(INI, datetime(2026, 10, 30)):
        for cel in CELULAS_MONT:
            for turno in (1, 2):
                if R.random() > 0.17:
                    continue
                m, t = R.choices(mot, weights=pesos)[0]
                cand = [p for p in prod if p["Data"] == d and p["Celula"] == cel and p["Turno"] == "%dº Turno" % turno]
                ot = str(R.choice(cand)["OT"]) if cand and R.random() < 0.75 else None
                h = 6 if turno == 1 else 14
                reg = d + timedelta(hours=h + R.randint(0, 7), minutes=R.randint(0, 59))
                out.append({"Data": d, "Turno": "%dº Turno" % turno, "Celula": cel, "RegistradoEm": reg,
                            "Motivo": m, "TempoParadoMin": float(R.choice([5, 10, 15, 20, 30, 45, 60])),
                            "Observacao": None, "OPVinculada": ot})
    return out


def tab_producao_montagem():
    out = []
    ot = 9000001
    for d in dias_uteis(INI, datetime(2026, 10, 30)):
        for cel in CELULAS_MONT:
            for turno in (1, 2):
                if R.random() > 0.43:
                    continue
                inicio = d + timedelta(hours=(6 if turno == 1 else 14), minutes=R.randint(0, 40))
                meta = float(META_HORA_MONT[cel])
                dur = R.randint(45, 240)
                fim = inicio + timedelta(minutes=dur)
                desc = float(R.choice([0, 0, 5, 10, 15]))
                real = dur - desc
                qtd_ot = max(1, int(meta * dur / 60 * R.uniform(0.9, 1.2)))
                qprod = max(1, int(meta * real / 60 * R.uniform(0.75, 1.15)))
                out.append({"Data": d, "Turno": "%dº Turno" % turno, "Celula": cel,
                            "PN": "FH-%04d" % R.randint(1001, 1030), "OT": ot, "QtdOT": float(qtd_ot),
                            "InicioEm": inicio, "FimEm": fim, "QtdProduzida": float(qprod),
                            "MetaHora": meta, "DuracaoMin": float(dur), "DuracaoSeg": float(dur * 60),
                            "Status": "Concluída", "Cracha": "C%03d" % R.randint(1, 24),
                            "DuracaoRealMin": float(real), "DescontoMin": desc})
                ot += 1
    return out


def tab_inspecao_e_erros():
    insp, err = [], []
    n_err = 0
    for f in FICHAS:
        if f["status"] != "Finalizado":
            continue
        fim = f["fim"]
        quando = fim + timedelta(hours=R.uniform(0.5, 6))
        i = len(insp) + 1
        qtd = float(R.choice([10, 20, 30, 40, 60]))
        cod = None
        defeito = None
        if R.random() < 0.22:
            cod = R.choice(CODIGOS_ERRO)
            defeito = cod.split(" - ")[1]
        insp.append({
            "OP_ID": float(f["op"]), "Quantidade": qtd,
            "Diametro_Interno": round(f["dash"] * 1.58 + R.uniform(-0.05, 0.05), 2),
            "Diametro_Externo": round(f["dash"] * 2.3 + R.uniform(-0.08, 0.08), 2),
            "Concentricidade": R.choice(["OK", "OK", "OK", "Limite"]),
            "DataHoraInspecao": quando, "TurnoTeste": float(turno_de(quando)), "Created": quando,
            "Mangueira": f["mang"], "CodigoDefeito": cod, "Trançadeira": f["tran"],
            "Title": "INS-%04d" % i, "Defeito_Inspeção": defeito, "Modified": quando, "ID": i,
            "Version": "1.0", "cabine_teste": f["cabine"],
        })
        if cod:
            n_err += 1
            err.append({
                "OP_ID": float(f["op"]), "CodigoErro": cod, "Quantidade": float(R.choice([1, 1, 2, 3, 5])),
                "Created": quando, "DataHoraRefugo": quando, "Trançadeira": f["tran"],
                "Turno Erro": "Turno %d" % turno_de(quando), "Title": "REF-%04d" % n_err,
                "OP_refugo": float(f["op"]), "ID_RegistroInspecao": str(i), "Modified": quando,
                "ID": n_err, "Version": "1.0", "cabine_teste": f["cabine"],
            })
    return insp, err


def tab_catenaria():
    out = []
    for i in range(1, 141):
        f = R.choice([x for x in FICHAS if x["est"].get("tran")])
        t = f["est"]["tran"][1] + timedelta(minutes=R.randint(0, 60))
        esp = round(f["dash"] * 1.9, 1)
        out.append({
            "Title": "CAT-%04d" % i, "DataHora": t, "Maquina": f["tran"], "Mangueira": f["mang"],
            "NFios": float(R.choice([16, 20, 24, 32])), "DiamEspecPol": str(round(esp / 25.4, 3)),
            "DiamEspecMM": str(esp), "DiamAtualMM": str(round(esp + R.uniform(-0.08, 0.08), 2)),
            "TensaoPol": str(R.choice([10, 12, 14])), "Aprovado": R.random() < 0.93,
            "ENumber": "E%04d" % R.randint(1, 500), "Observacoes": None, "Turno": float(turno_de(t)),
            "ID": i, "Created": t, "Modified": t, "Version": "1.0",
        })
    return out


def tab_extrusora_estrutura():
    out = []
    for i, f in enumerate([x for x in FICHAS if x["est"].get("mandril") and x["est"]["mandril"][2]][:220], 1):
        ini, fim = f["est"]["mandril"][1], f["est"]["mandril"][2]
        out.append({
            "OP_ID": str(f["op"]), "OP": float(f["op"]), "Bitola": float(f["dash"]),
            "cod_mandril": f["mandril"], "desmoldante": R.choice(["DM-A", "DM-B"]),
            "quantidade": float(f["qtd"]), "operador": R.choice(OPERADORES),
            "lote_mandril": "LM-%04d" % R.randint(2600, 2699), "data_hora_inicio": ini,
            "data_hora_final": fim, "Turno": "Turno %d" % turno_de(fim), "Observacao": None,
            "Criado": fim.strftime("%d/%m/%Y"), "ID": i, "Created": fim, "Modified": fim, "Version": "1.0",
        })
    return out


def tab_fifo():
    out = []
    consumidas = [f for f in FICHAS if f["est"].get("tran") and f["est"]["tran"][1]]
    for i in range(1, 131):
        f = R.choice(consumidas)
        ini = f["est"]["tran"][0] - timedelta(hours=R.uniform(1, 10))
        fin = ini + timedelta(minutes=R.randint(20, 90))
        status = R.choices(["Consumido", "Aguardando", "Cancelado"], weights=[80, 8, 12])[0]
        lin = {
            "Title": "FIFO-%04d" % i, "Linha": float(R.randint(1, 4)), "Mangueira": f["mang"],
            "Trancadeira": f["tran"], "Quantidade": str(R.choice([4, 6, 8, 12])), "Status": status,
            "CodProduto": "BOB-%03d" % R.randint(1, 60), "QtdBobinas": float(R.choice([4, 6, 8, 12])),
            "Metragem": float(f["qtd"]), "NFios": float(R.choice([16, 20, 24, 32])),
            "RT": "RT%03d" % R.randint(1, 99), "LI": "LI%03d" % R.randint(1, 99),
            "Operador": R.choice(OPERADORES), "Turno": float(turno_de(ini)),
            "DataHoraInicio": ini, "DataHoraSalvo": fin, "DataHoraFinal": fin,
            "Maquina de Bobinagem": "BOB%02d" % R.randint(1, 4), "Observação": None,
            "ID": i, "Created": ini, "Modified": fin, "Version": "1.0",
        }
        if status == "Consumido":
            lin["OP_Consumo"] = str(f["op"])
            lin["FichaID_Consumo"] = float(f["i"])
            lin["DataHoraConsumo"] = f["est"]["tran"][1]
            lin["Carrinho"] = float(R.randint(1, 12))
        elif status == "Cancelado":
            lin["MotivoCancelamento"] = R.choice(["Fio errado", "Bobina danificada", "Troca de programação"])
            lin["CanceladoPor"] = R.choice(OPERADORES)
            lin["DataHoraCancelamento"] = fin + timedelta(minutes=R.randint(5, 120))
        out.append(lin)
    return out


def tab_hose_plan():
    out = []
    for i, (m, c, d) in enumerate(MANGUEIRAS, 1):
        plan = float(R.choice([6000, 8000, 10000, 12000, 15000, 20000]))
        mtd = round(plan * R.uniform(0.55, 1.05) / 10) * 10.0
        esperado = plan * 0.92
        out.append({"Title": m, "Construction": c, "PlanMes": plan, "MTD": mtd,
                    "Atraso": max(0.0, round(esperado - mtd)),
                    "ID": i, "Created": datetime(2026, 10, 1), "Modified": datetime(2026, 10, 30), "Version": "1.0"})
    return out


def tab_ordens_planejadas():
    meses = {8: "AGO/2026", 9: "SET/2026", 10: "OUT/2026"}
    out = []
    for f in FICHAS:
        t = f["est"]["mandril"][0]
        d = datetime(t.year, t.month, t.day)
        out.append({"MÊS": meses[d.month], "Trançadeira": f["tran"], "OP": float(f["op"]),
                    "Mangueira": f["mang"], "Qtd.Planejada": float(f["qtd"]), "Data": d,
                    "ID": f["i"], "Created": d, "Modified": d, "Version": "1.0"})
    return out


def tab_lista_carreteis():
    out = []
    for i in range(1, 141):
        f = R.choice(FICHAS)
        enc = f["est"]["tubo"][1] if f["est"].get("tubo") and f["est"]["tubo"][1] else f["est"]["mandril"][0]
        status = R.choice(["Disponível", "Em uso", "Consumido", "Consumido", "Consumido"])
        cons = enc + timedelta(hours=R.uniform(3, 40)) if status == "Consumido" else None
        out.append({
            "ID": i, "Título": "CR-%04d" % i, "op": str(f["op"]),
            "etapa_processo": R.choice(["Trançagem", "Cobertura", "Bandagem"]),
            "metros_restantes": 0.0 if status == "Consumido" else float(R.choice([100, 250, 400, 600])),
            "mangueira_atual": f["mang"], "Material": R.choice(["Tubo", "Cobertura"]), "Status": status,
            "Bitola": float(f["dash"]), "cod_mandril": f["mandril"], "desmoldante": R.choice(["DM-A", "DM-B"]),
            "quantidade_metros": float(f["qtd"]), "OP_extrusora": str(f["op"]),
            "operador_extrusora": R.choice(OPERADORES), "data_enchimento": enc, "data_consumo": cons,
            "lote": "LM-%04d" % R.randint(2600, 2699), "OP.1": float(f["op"]),
            "Created": enc, "Modified": cons or enc, "Version": "1.0",
        })
    return out


# ----------------------------------------------------------------------------
# Leitura do TMDL e escrita do M
# ----------------------------------------------------------------------------
def parse_tabela(path):
    txt = open(path, encoding="utf-8").read()
    L = txt.split("\n")
    cols, cur = [], None
    for l in L:
        m = re.match(r"^\tcolumn (.+?)( =.*)?$", l)
        if m:
            nm = m.group(1)
            if nm.startswith("'") and nm.endswith("'"):
                nm = nm[1:-1].replace("''", "'")
            cur = {"n": nm, "calc": bool(m.group(2)), "t": None, "sc": None}
            cols.append(cur)
            continue
        if re.match(r"^\t(measure|partition|hierarchy|annotation|table|ref|extendedProperty)", l):
            cur = None
        if cur:
            m = re.match(r"^\t\t(dataType|sourceColumn|type|expression)(?:: ?| =)(.*)$", l)
            if m:
                k, v = m.group(1), m.group(2)
                if k == "dataType":
                    cur["t"] = v.strip()
                elif k == "sourceColumn":
                    s = v.strip()
                    if s.startswith("[") and s.endswith("]"):
                        s = s[1:-1]
                    if s.startswith("'") and s.endswith("'"):
                        s = s[1:-1]
                    if s.startswith('"') and s.endswith('"'):
                        s = s[1:-1]
                    cur["sc"] = s
                elif k == "type" and "calculated" in v:
                    cur["calc"] = True
                elif k == "expression":
                    cur["calc"] = True
    return txt, L, cols


TIPO_M = {"string": "nullable text", "int64": "Int64.Type", "double": "nullable number",
          "dateTime": "nullable datetime", "boolean": "nullable logical", "decimal": "nullable number"}


def m_nome(n):
    return '#"%s"' % n.replace('"', '""')


def m_valor(v, tipo):
    if v is None:
        return "null"
    if tipo == "string":
        return '"%s"' % str(v).replace('"', '""')
    if tipo == "dateTime":
        if not isinstance(v, datetime):
            raise ValueError("esperava datetime, veio %r" % (v,))
        return "#datetime(%d,%d,%d,%d,%d,%d)" % (v.year, v.month, v.day, v.hour, v.minute, v.second)
    if tipo == "boolean":
        return "true" if v else "false"
    if tipo == "int64":
        return str(int(v))
    x = float(v)
    s = ("%.4f" % x).rstrip("0").rstrip(".")
    return s if s not in ("", "-0") else "0"


def construir_m(cols, linhas):
    cab = ", ".join("%s = %s" % (m_nome(c["sc"] or c["n"]), TIPO_M[c["t"]]) for c in cols)
    corpo = []
    for lin in linhas:
        vals = [m_valor(lin.get(c["sc"] or c["n"]), c["t"]) for c in cols]
        corpo.append("{" + ", ".join(vals) + "}")
    ind = "\t\t\t\t"
    out = [ind + "let", ind + "    Source = #table(", ind + "        type table [" + cab + "],", ind + "        {"]
    for i, c in enumerate(corpo):
        out.append(ind + "            " + c + ("," if i < len(corpo) - 1 else ""))
    out += [ind + "        }", ind + "    )", ind + "in", ind + "    Source"]
    return out


def reescrever_particao(path, linhas_m):
    txt = open(path, encoding="utf-8").read()
    L = txt.split("\n")
    i = next(k for k, l in enumerate(L) if l == "\t\tsource =")
    j = i + 1
    while j < len(L) and (L[j].startswith("\t\t\t") or L[j].strip() == "" and j + 1 < len(L) and L[j + 1].startswith("\t\t\t")):
        j += 1
    L[i + 1:j] = linhas_m
    open(path, "w", encoding="utf-8", newline="\n").write("\n".join(L))


def main():
    global MOTIVOS
    MOTIVOS = motivos_parada()
    assert len(MOTIVOS) > 30, "lista de motivos nao encontrada"
    gerar_fichas()
    fhh = tab_fhorahora()
    prod = tab_producao_montagem()
    insp, err = tab_inspecao_e_erros()
    dados = {
        "ficha_producao": tab_ficha_producao(),
        "Part Number x Construction": tab_part_number(),
        "Eventos_Producao": tab_eventos(),
        "Historico_Carretel": tab_historico_carretel(),
        "fHoraHora": fhh,
        "Hora-Hora": tab_hora_hora(fhh),
        "RefugoExtrusora_Mandril": tab_refugo_extrusora(),
        "Producao_Montagem": prod,
        "Paradas_Montagem": tab_paradas_montagem(prod),
        "RegistrosInspeção": insp,
        "TiposErros": err,
        "Controle_Catenaria": tab_catenaria(),
        "ControleExtrusora_estrutura": tab_extrusora_estrutura(),
        "FifoBobinadeira": tab_fifo(),
        "HosePlanMensal": tab_hose_plan(),
        "OrdensPlanejadas": tab_ordens_planejadas(),
        "lista_carreteis": tab_lista_carreteis(),
    }
    resumo = []
    for nome, linhas in dados.items():
        path = os.path.join(TABELAS, nome + ".tmdl")
        txt, L, cols = parse_tabela(path)
        reais = [c for c in cols if not c["calc"]]
        conhecidas = set()
        for lin in linhas:
            conhecidas.update(lin.keys())
        extras = conhecidas - {c["sc"] or c["n"] for c in reais}
        if extras:
            sys.exit("%s: colunas geradas que nao existem no modelo: %s" % (nome, sorted(extras)))
        reescrever_particao(path, construir_m(reais, linhas))
        resumo.append((nome, len(reais), len(linhas)))

    # expressoes M de SharePoint sem tabela (nao carregadas) -> tabela vazia inline
    ex = os.path.join(MODELO, "expressions.tmdl")
    t = open(ex, encoding="utf-8").read()
    t = re.sub(r"(expression \S+ =\n)(?:\t\t.*\n)+?(\tlineageTag)",
               r'\1\t\tlet\n\t\t  Source = #table(type table [Coluna1 = nullable text], {})\n\t\tin\n\t\t  Source\n\2', t)
    open(ex, "w", encoding="utf-8", newline="\n").write(t)

    for n, c, l in resumo:
        print("%-30s %3d colunas  %4d linhas" % (n, c, l))


if __name__ == "__main__":
    main()
