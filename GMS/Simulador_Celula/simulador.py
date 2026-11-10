# -*- coding: utf-8 -*-
"""Simulador da celula de mangueiras (GMS): 8 etapas, turnos, paradas, setup, refugo e pessoas.
Diagnostico e proposta: le so arquivos locais, nao toca em producao.

  python simulador.py                      calibra, faz o backtest e roda o what-if de exemplo
  python simulador.py whatif --demanda 8000 --t3 trancagem,extracao --pessoas extracao=3 --sem falta_tubo --trocas 0.5

Regra de turno/parada/setup, parametros e suposicoes: ver LEIAME.md.
"""
import argparse, json, os, re
import numpy as np, pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(AQUI, "dados")
GMS_DADOS = os.path.join(AQUI, "..", "IA", "dados")
ETAPAS = ["mandril", "tubo", "trancagem", "cobertura", "bandagem", "vulcanizacao", "debandagem", "extracao"]
MIN_TURNO = {1: 517, 2: 503, 3: 420}          # T1 05:20-13:57, T2 13:57-22:20, T3 22:20-05:20
PAUSA_MIN = 45                                # pausa por turno (regra do BI desde 09/11: 1.305 de 1.440 min)
H_DISP = {t: (m - PAUSA_MIN) / 60 for t, m in MIN_TURNO.items()}
INICIO, CORTE = pd.Timestamp("2026-04-01"), pd.Timestamp("2026-09-01")   # treino: [INICIO, CORTE); teste: >= CORTE
MANUAIS = {"mandril", "bandagem", "debandagem", "extracao"}              # suposicao: mais gente rende mais (ate o teto)
CLASSES = [("setup", r"set.?up|troca"), ("falta_tubo", r"tubo"), ("falta_fio", r"fio|arame"),
           ("manutencao", r"manut|prevent|corret|quebra|falha"), ("falta_operador", r"operador|pessoa"),
           ("sem_plano", r"sem plan|sem prog")]


def classe_motivo(t):
    t = t.strip().lower()
    for nome, rx in CLASSES:
        if re.search(rx, t):
            return nome
    return "outras_paradas" if t else "normal"


def carregar():
    if not os.path.exists(os.path.join(DADOS, "eficiencia_etapa.csv")):
        import extrair_eficiencia
        extrair_eficiencia.main()
    e = pd.read_csv(os.path.join(DADOS, "eficiencia_etapa.csv"), parse_dates=["data"])
    m = pd.read_csv(os.path.join(DADOS, "eficiencia_maquina.csv"), parse_dates=["data"])
    return e[e.data >= INICIO], m[m.data >= INICIO]


def tabela_trancagem(m):
    """Uma linha por maquina x turno planejado: velocidade cadastrada, real, troca de mangueira, classe e desempenho."""
    m = m.copy()
    m["motivo"], m["mangueira"] = m.motivo.fillna(""), m.mangueira.fillna("")
    vh = m[m.vel_m_h > 0].groupby("mangueira").vel_m_h.median()
    sem_vel = (m.vel_m_h <= 0) & (m.real > 0)
    m.loc[sem_vel, "vel_m_h"] = m[sem_vel].mangueira.map(vh)      # velocidade nao cadastrada na aba: usa a da mangueira
    m = m[m.vel_m_h > 0]
    g = m.groupby(["data", "turno", "maquina"]).agg(
        vel=("vel_m_h", "mean"), real=("real", "sum"), plan=("planejado", "sum"),
        hose=("mangueira", lambda s: "+".join(sorted(set(s) - {""}))), motivo=("motivo", " ".join)).reset_index()
    g = g.sort_values(["maquina", "data", "turno"])
    ant = g.groupby("maquina").hose.shift()
    g["troca"] = ant.notna() & (ant != g.hose)
    g["perf"] = g.real / (g.turno.map(H_DISP) * g.vel)
    g["classe"] = [classe_motivo(x) for x in g.motivo]
    g.loc[(g.classe == "normal") & (g.perf < 0.05), "classe"] = "zero_sem_motivo"
    g.loc[g.troca & g.classe.isin(["normal", "zero_sem_motivo"]), "classe"] = "setup"   # parada com motivo proprio nao vira setup
    return g[g.perf <= 2.5]


def ler_ficha():
    f = pd.read_csv(os.path.join(GMS_DADOS, "ficha_producao.csv"), dtype=str, encoding="utf-8-sig")
    f = f[f.status_processo != "Cancelado"]
    partes = []
    for s in ETAPAS:
        ts = pd.to_datetime(f["data_hora_final_" + ("trancadeira" if s == "trancagem" else s)], format="%m/%d/%Y %I:%M %p", errors="coerce")
        mm = ts.dt.hour * 60 + ts.dt.minute
        partes.append(pd.DataFrame({
            "etapa": s, "data": (ts - pd.Timedelta(minutes=320)).dt.normalize(),      # dia produtivo comeca 05:20
            "turno": np.where((mm >= 320) & (mm < 837), 1, np.where((mm >= 837) & (mm < 1340), 2, 3)),
            "metros": pd.to_numeric(f["quantidade_" + s].str.replace(",", ""), errors="coerce").where(lambda q: q <= 3000),  # lote > 3000 m = erro de digitacao
            "operador": f["operador_" + s].str.strip().str.upper()}).dropna(subset=["data", "metros"]))
    return pd.concat(partes)


def taxa_refugo(ini, fim):
    def soma(arq, col):
        d = pd.read_csv(os.path.join(GMS_DADOS, arq), dtype=str, encoding="utf-8-sig")
        if "CodigoErro" in d:
            d = d.drop_duplicates(["OP_ID", "CodigoErro", "Quantidade", "Criado"])
        ts = pd.to_datetime(d[col], format="%m/%d/%Y %I:%M %p", errors="coerce")
        return float(pd.to_numeric(d.Quantidade.str.replace(",", ""), errors="coerce")[(ts >= ini) & (ts < fim)].sum())
    r, b = soma("TiposErros.csv", "Criado"), soma("RegistrosInspeção.csv", "DataHoraInspecao")
    return r / (r + b), r, b


def montar_entradas(e, g, ficha):
    """Entradas conhecidas antes do dia: plano da trancagem e turnos abertos (planejado > 0). Mais as series reais."""
    real = e.groupby(["data", "etapa"]).real.sum().unstack().reindex(columns=ETAPAS)
    dias = [d for d in real.index if (real.loc[d, "trancagem"] or 0) > 0 or (real.loc[d, "extracao"] or 0) > 0]
    real = real.loc[dias]
    v = ficha[ficha.etapa == "vulcanizacao"].groupby("data").metros.sum()
    real["vulcanizacao"] = [v.get(d, 0.0) if d <= ficha.data.max() else np.nan for d in dias]
    plano = {k: list(zip(x.maquina, x.vel, x.troca)) for k, x in g.groupby(["data", "turno"])}
    # turno trabalhado = real > 0 (a planilha traz planejado ate em dia sem producao; nao ha escala real no repositorio)
    ab = e[e.real > 0]
    abertos = set(zip(ab.data, ab.turno, ab.etapa))
    fv = ficha[ficha.etapa == "vulcanizacao"].groupby(["data", "turno"]).metros.sum()
    abertos |= {(d, t, "vulcanizacao") for (d, t), q in fv.items() if q > 0}
    abertos |= {(d, t, "vulcanizacao") for d, t, s in abertos if s == "bandagem" and d > ficha.data.max()}
    planej = e.groupby(["data", "etapa"]).planejado.sum().unstack().reindex(index=dias, columns=ETAPAS)
    planej["trancagem"] = g.groupby("data").plan.sum().reindex(dias).fillna(0).values
    return dias, real, plano, abertos, planej


def calibrar(e, g, ficha, dias, real, abertos):
    tr, P = g[g.data < CORTE], {"k": {s: 1.0 for s in ETAPAS}}
    dias_tr = [d for d in dias if d < CORTE]
    nt = tr[~tr.troca]
    P["tr"] = {mq: {"perf": x.perf.round(3).tolist(), "classe": x.classe.tolist()} for mq, x in nt.groupby("maquina") if len(x) >= 20}
    P["tr"]["_todas"] = {"perf": nt.perf.round(3).tolist(), "classe": nt.classe.tolist()}
    P["setup_perf"] = tr[tr.troca].perf.round(3).tolist()
    P["normal_perf"] = tr[tr.classe == "normal"].perf.round(3).tolist()
    ref = float(np.median(P["normal_perf"]))
    perda = ((ref - tr.perf).clip(lower=0) * tr.turno.map(H_DISP) * tr.vel).groupby(tr.classe).sum() / len(dias_tr)
    P["perda_m_dia"] = perda.round(0).to_dict()
    P["perf_mediana"] = {"normal": round(ref, 3), "setup": round(float(tr[tr.classe == "setup"].perf.median()), 3)}
    P["setup_min_por_troca"] = round((ref - P["perf_mediana"]["setup"]) * 60 * float(np.mean(list(H_DISP.values()))))
    P["turnos_maquina_por_classe"] = tr.classe.value_counts().to_dict()
    # etapas de linha: capacidade por turno trabalhado = real historico do turno (paradas e ritmo juntos)
    et = e[(e.data < CORTE) & (e.real > 0)]
    P["cap"] = {f"{s}|{t}": x.real.round(0).tolist() for (s, t), x in et.groupby(["etapa", "turno"])}
    fv = ficha[(ficha.etapa == "vulcanizacao") & (ficha.data >= INICIO) & (ficha.data < CORTE)].groupby(["data", "turno"]).metros.sum()
    for t in (1, 2, 3):
        P["cap"][f"vulcanizacao|{t}"] = [float(q) for (d, tt), q in fv.items() if tt == t and q > 0]
    for s in ETAPAS:
        P["cap"][f"{s}|0"] = sum((P["cap"].get(f"{s}|{t}", []) for t in (1, 2, 3)), [])
    tot = real.loc[dias_tr].sum()
    P["f"] = {s: round(float(tot[s] / tot[ETAPAS[i - 1]]), 4) for i, s in enumerate(ETAPAS) if i > 0}
    med = real.loc[dias_tr].median()
    P["mediana_dia"] = med.round(0).to_dict()
    P["bmax"] = {"tubo": float(med["tubo"]), "trancagem": 1.5 * float(med["trancagem"])}       # suposicao
    fx = ficha[(ficha.data >= INICIO) & (ficha.data < CORTE) & (ficha.operador.fillna("") != "")]
    pes = fx.groupby(["etapa", "turno", "data"]).operador.nunique().groupby(level=[0, 1]).median()
    P["pessoas_ref"] = {f"{s}|{t}": float(v) for (s, t), v in pes.items()}                       # provisorio: quem apontou
    r, mr, mb = taxa_refugo(INICIO, CORTE)
    P["refugo"] = {"taxa": round(r, 5), "refugo_m": round(mr), "bom_m": round(mb)}
    return P


def simular(P, dias, plano, abertos, R=200, seed=1, pessoas=None, maq_max=None, sem=(), refugo=None):
    """Passo de um turno. Devolve (saida, capacidade): dict etapa -> matriz (dias, R) em metros."""
    rng = np.random.default_rng(seed)
    A = lambda x: np.asarray(x, float)
    trn = {mq: (A(h["perf"]), np.array(h["classe"])) for mq, h in P["tr"].items()}
    setup, normal = A(P["setup_perf"]), A(P["normal_perf"])
    caps = {k: A(v) for k, v in P["cap"].items() if len(v)}
    f, k = P["f"], P["k"]
    wip = {s: np.full(R, 0.5 * P["mediana_dia"][s]) for s in ETAPAS}
    out = {s: np.zeros((len(dias), R)) for s in ETAPAS}
    cap_acc = {s: np.zeros((len(dias), R)) for s in ETAPAS}
    for di, d in enumerate(dias):
        for t in (1, 2, 3):
            for i, s in enumerate(ETAPAS):
                cap = np.zeros(R)
                if s == "trancagem":
                    linhas = plano.get((d, t), [])
                    if maq_max is not None:                                   # menos operadores: rodam as maquinas mais rapidas
                        linhas = sorted(linhas, key=lambda x: -x[1])[:int(maq_max.get(t, 99))]
                    for mq, vel, troca in linhas:
                        if troca:
                            perf = rng.choice(setup, R)
                        else:
                            hp, hc = trn.get(mq, trn["_todas"])
                            j = rng.integers(0, len(hp), R)
                            perf = hp[j]
                            if sem:
                                perf = np.where(np.isin(hc[j], sem), rng.choice(normal, R), perf)
                        cap += H_DISP[t] * vel * perf
                    o = cap
                    wip[s] = np.maximum(wip[s] - o, 0)                         # consome o tubo (falta de tubo ja vem do historico)
                else:
                    if (d, t, s) in abertos:
                        arr = caps.get(f"{s}|{t}", caps.get(f"{s}|0"))
                        cap = k[s] * rng.choice(arr, R)
                        if pessoas and s in pessoas:
                            pr = P["pessoas_ref"].get(f"{s}|{t}") or P["pessoas_ref"].get(f"{s}|1", 1.0)
                            fat = max(pr + pessoas[s], 0) / pr                 # pessoas[s] = variacao sobre a referencia do turno
                            cap = cap * (min(fat, 1.5) if s in MANUAIS else min(fat, 1.0))
                    o = cap if i == 0 else np.minimum(cap, wip[s])
                    if s in ("mandril", "tubo"):                               # puxado: para quando o estoque a frente enche
                        nx = ETAPAS[i + 1]
                        o = np.minimum(o, np.maximum(P["bmax"][nx] - wip[nx], 0) / f[nx])
                    if i > 0:
                        wip[s] = wip[s] - o
                if i < len(ETAPAS) - 1:
                    wip[ETAPAS[i + 1]] = wip[ETAPAS[i + 1]] + o * f[ETAPAS[i + 1]]
                out[s][di] += o
                cap_acc[s][di] += cap
    if refugo is not None:                                                     # e se o refugo mudar (saida boa da extracao)
        out["extracao"] = out["extracao"] * (1 - refugo) / (1 - P["refugo"]["taxa"])
    return out, cap_acc


def ajustar_k(P, dias_tr, real, plano, abertos):
    """Calibracao por simulacao, so com o treino: escala a capacidade de cada etapa ate o vies do treino zerar."""
    for s in [x for x in ETAPAS if x != "trancagem"]:
        ok = real.loc[dias_tr, s].notna().values
        alvo, melhor = real.loc[dias_tr, s].values[ok].sum(), (9e9, 1.0)
        for kk in np.arange(0.8, 2.01, 0.1):
            P["k"][s] = round(float(kk), 2)
            sim = simular(P, dias_tr, plano, abertos, R=30, seed=7)[0][s].mean(axis=1)[ok].sum()
            if abs(sim / alvo - 1) < melhor[0] - 0.002:
                melhor = (abs(sim / alvo - 1), P["k"][s])
        P["k"][s] = melhor[1]


def metricas(real, prev, lo, hi, datas):
    real, prev, lo, hi = (np.asarray(x, float) for x in (real, prev, lo, hi))
    ok = ~np.isnan(real)
    real, prev, lo, hi, datas = real[ok], prev[ok], lo[ok], hi[ok], [d for d, o in zip(datas, ok) if o]
    pos = real > 0
    sem = pd.DataFrame({"r": real, "p": prev}, index=pd.DatetimeIndex(datas)).resample("W").sum()
    sem = sem[sem.r > 0]
    return {"dias": int(ok.sum()), "real_dia": real.mean(), "sim_dia": prev.mean(),
            "mape": np.mean(np.abs(prev[pos] - real[pos]) / real[pos]) * 100,
            "wape": np.abs(prev - real).sum() / real.sum() * 100, "vies": (prev.sum() / real.sum() - 1) * 100,
            "mape_sem": float((np.abs(sem.p - sem.r) / sem.r).mean() * 100), "cob": np.mean((real >= lo) & (real <= hi)) * 100}


def backtest(P, dias, real, plano, abertos, planej, R=300):
    out, _ = simular(P, dias, plano, abertos, R=R, seed=11)
    tr = np.array([d < CORTE for d in dias])
    linhas, res = [], {}
    for nome, mask in (("TESTE (fora da amostra)", ~tr), ("TREINO (dentro da amostra)", tr)):
        dd = [d for d, m in zip(dias, mask) if m]
        linhas += [f"\n## {nome}: {dd[0].date()} a {dd[-1].date()}, {len(dd)} dias\n",
                   "| Etapa | dias | real m/dia | simulado m/dia | MAPE dia % | WAPE % | viés % | MAPE semana % | real dentro de p10–p90 % | WAPE mediana do treino % | WAPE planejado da planilha % |",
                   "|---|---|---|---|---|---|---|---|---|---|---|"]
        soma = None
        for s in ETAPAS + ["SOMA DAS 7 ETAPAS DA PLANILHA"]:
            if s in ETAPAS:
                x, r = out[s][mask], real[s].values[mask]
                mt = metricas(r, x.mean(axis=1), np.percentile(x, 10, axis=1), np.percentile(x, 90, axis=1), dd)
                ing = metricas(r, np.full(len(r), P["mediana_dia"][s]), r, r, dd)["wape"]
                pl = metricas(r, planej[s].fillna(0).values[mask], r, r, dd)["wape"] if s != "vulcanizacao" else float("nan")
                if s != "vulcanizacao":
                    soma = (r, x) if soma is None else (soma[0] + r, soma[1] + x)
            else:
                r, x = soma
                mt = metricas(r, x.mean(axis=1), np.percentile(x, 10, axis=1), np.percentile(x, 90, axis=1), dd)
                ing, pl = float("nan"), float("nan")
            res[(nome[:5], s)] = mt
            rot = {"extracao": "**extracao (saída da célula)**", "vulcanizacao": "vulcanizacao (real = ficha, até 06/10)"}.get(s, s)
            linhas.append(f"| {rot} | {mt['dias']} | {mt['real_dia']:.0f} | {mt['sim_dia']:.0f} | {mt['mape']:.1f} | {mt['wape']:.1f} | {mt['vies']:+.1f} | {mt['mape_sem']:.1f} | {mt['cob']:.0f} | {ing:.1f} | {pl:.1f} |")
        if nome.startswith("TESTE"):
            x, r = out["extracao"][mask].mean(axis=1), real["extracao"].values[mask]
            pior = np.argsort(-np.abs(x - r))[:5]
            linhas += ["\nCinco dias de teste em que a extração simulada mais errou (m): " +
                       "; ".join(f"{dd[j].date()} real {r[j]:.0f} x simulado {x[j]:.0f}" for j in pior) + "."]
    return linhas, res


def cenario(hist, n_dias, turnos, trocas=1.0, seed=3):
    """Plano da trancagem = planos reais dos ultimos 45 dias com producao, sorteados por turno (mesmo sorteio em todos os cenarios)."""
    rng = np.random.default_rng(seed)
    ult = sorted({d for d, _ in hist})[-45:]
    por_turno = {t: [hist[(d, t)] for d in ult if (d, t) in hist] for t in (1, 2, 3)}
    dias = list(pd.bdate_range("2027-01-04", periods=n_dias))
    plano, abertos = {}, set()
    for d in dias:
        for s in ETAPAS:
            for t in turnos.get(s, (1, 2)):
                abertos.add((d, t, s))
        for t in (1, 2, 3):
            base = por_turno[t][rng.integers(len(por_turno[t]))]
            u = rng.random(len(base))
            if t in turnos.get("trancagem", (1, 2)):
                plano[(d, t)] = [(mq, vel, bool(troca and u[j] < trocas)) for j, (mq, vel, troca) in enumerate(base)]
    return dias, plano, abertos


def whatif(P, hist, demanda, casos, n_dias=40, R=300):
    fd, acc = {}, 1.0
    for s in reversed(ETAPAS):
        fd[s] = acc
        acc *= P["f"].get(s, 1.0)
    linhas = ["| Cenário | saída boa m/dia (média) | p10–p90 do dia | % dos dias ≥ demanda | % das semanas ≥ demanda | gargalo (menor capacidade, m/dia equivalentes na extração) |", "|---|---|---|---|---|---|"]
    for nome, c in casos:
        turnos = {s: (1, 2, 3) if s in c.get("t3", ()) else (1, 2) for s in ETAPAS}
        dias, plano, abertos = cenario(hist, n_dias, turnos, c.get("trocas", 1.0))
        out, cap = simular(P, dias, plano, abertos, R=R, seed=5, pessoas=c.get("pessoas"), maq_max=c.get("maq_max"), sem=c.get("sem", ()), refugo=c.get("refugo"))
        x = out["extracao"]
        semana = x.reshape(n_dias // 5, 5, R).mean(axis=1)
        ce = {s: cap[s].mean() * fd[s] for s in ETAPAS}
        g = min(ce, key=ce.get)
        linhas.append(f"| {nome} | {x.mean():.0f} | {np.percentile(x, 10):.0f}–{np.percentile(x, 90):.0f} | {np.mean(x >= demanda) * 100:.0f} | {np.mean(semana >= demanda) * 100:.0f} | {g} ({ce[g]:.0f}) |")
    return linhas


def preparar():
    e, m = carregar()
    g, ficha = tabela_trancagem(m), ler_ficha()
    dias, real, plano, abertos, planej = montar_entradas(e, g, ficha)
    P = calibrar(e, g, ficha, dias, real, abertos)
    ajustar_k(P, [d for d in dias if d < CORTE], real, plano, abertos)
    return P, dias, real, plano, abertos, planej


def tudo(demanda=8000):
    P, dias, real, plano, abertos, planej = preparar()
    with open(os.path.join(AQUI, "parametros.json"), "w", encoding="utf-8") as fo:
        json.dump(P, fo, ensure_ascii=False)
    bt, res = backtest(P, dias, real, plano, abertos, planej)
    pr = P["pessoas_ref"]
    casos = [("Base: 2 turnos, pessoas de referência", {}),
             ("3º turno só na trançagem", {"t3": ["trancagem"]}),
             ("3º turno em todas as etapas", {"t3": ETAPAS}),
             ("Base com 1 pessoa a menos por turno na extração", {"pessoas": {"extracao": -1}}),
             ("Base com 1 pessoa a mais por turno na extração", {"pessoas": {"extracao": 1}}),
             ("3º turno em todas as etapas e 1 pessoa a mais na extração", {"t3": ETAPAS, "pessoas": {"extracao": 1}}),
             ("Base sem falta de tubo e de fio na trançagem", {"sem": ("falta_tubo", "falta_fio")}),
             ("Base com metade das trocas de mangueira (sequenciamento)", {"trocas": 0.5}),
             ("Base com 1 trançadeira a menos por turno (falta de operador)", {"maq_max": {1: 7, 2: 7}})]
    wi = whatif(P, plano, demanda, casos)
    cab = ["# Backtest do simulador da célula", "", "Gerado por `python simulador.py`. Não editar à mão.", "",
           f"Fonte do real: planilhas de Eficiência (`Dados_Historicos/Eficiencia_Processo/2026`), {len(dias)} dias com produção de {dias[0].date()} a {dias[-1].date()}.",
           f"Calibração (treino): dias antes de {CORTE.date()}. Teste: de {CORTE.date()} em diante; nenhum parâmetro viu esses dias.",
           "Entradas dadas ao simulador em cada dia: plano da trançagem (máquina, mangueira, velocidade cadastrada) e turnos planejados por etapa. Todo o resto é sorteado.",
           "Simulado = média de 300 réplicas; o estoque entre etapas é o simulado desde o primeiro dia, não o real."]
    with open(os.path.join(AQUI, "BACKTEST.md"), "w", encoding="utf-8") as fo:
        fo.write("\n".join(cab + bt) + "\n")
    with open(os.path.join(AQUI, "WHATIF_exemplo.md"), "w", encoding="utf-8") as fo:
        fo.write("\n".join([f"# What-if de exemplo: demanda de {demanda} m/dia de saída boa", "",
                            "Gerado por `python simulador.py`. 40 dias úteis simulados, 300 réplicas, plano típico dos últimos 60 dias do histórico.",
                            "Pessoas de referência = mediana de quem apontou na ficha (provisório).", ""] + wi) + "\n")
    for (per, st), mt in res.items():
        print(f"{per} {st[:12]:12s} real {mt['real_dia']:6.0f} sim {mt['sim_dia']:6.0f} MAPE {mt['mape']:5.1f} WAPE {mt['wape']:5.1f} vies {mt['vies']:+6.1f} sem {mt['mape_sem']:5.1f} cob {mt['cob']:3.0f}")
    print("\n".join(wi))
    print("k:", P["k"], "\nf:", P["f"], "\nperda m/dia por classe:", P["perda_m_dia"], "\nturnos-maquina:", P["turnos_maquina_por_classe"],
          "\nrefugo:", P["refugo"], "\npessoas_ref:", P["pessoas_ref"])


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Simulador da celula de mangueiras (GMS)")
    ap.add_argument("modo", nargs="?", default="tudo", choices=["tudo", "whatif"])
    ap.add_argument("--demanda", type=float, default=8000)
    ap.add_argument("--t3", default="", help="etapas com 3o turno, separadas por virgula (ou 'todas')")
    ap.add_argument("--pessoas", default="", help="pessoas por turno: etapa=n,etapa=n")
    ap.add_argument("--sem", default="", help="classes de parada a retirar: falta_tubo,falta_fio,manutencao,...")
    ap.add_argument("--trocas", type=float, default=1.0, help="multiplicador da frequencia de troca de mangueira")
    ap.add_argument("--maquinas", type=int, default=None, help="maximo de trancadeiras por turno")
    ap.add_argument("--refugo", type=float, default=None, help="taxa de refugo (ex.: 0.02)")
    a = ap.parse_args()
    if a.modo == "tudo":
        tudo(a.demanda)
    else:
        P, _, _, hist, _, _ = preparar()
        c = {"t3": ETAPAS if a.t3 == "todas" else [x for x in a.t3.split(",") if x], "trocas": a.trocas, "refugo": a.refugo,
             "sem": tuple(x for x in a.sem.split(",") if x),
             "pessoas": {x.split("=")[0]: float(x.split("=")[1]) for x in a.pessoas.split(",") if x} or None,
             "maq_max": {1: a.maquinas, 2: a.maquinas, 3: a.maquinas} if a.maquinas else None}
        print("\n".join(whatif(P, hist, a.demanda, [("Base", {}), ("Cenário pedido", c)])))
