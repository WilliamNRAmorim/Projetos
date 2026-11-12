"""What-if de demanda x pessoas do gemeo (missao P2, item 1).

Gera OPs pelo mix dos ultimos 90 dias do historico (sorteio com reposicao, mesma semente em todos os cenarios),
monta a equipe por etapa e turno, simula 6 semanas (2 de aquecimento, 4 medidas) e grava em saida/:
  whatif_cenarios.csv  uma linha por cenario: demanda, entregue, atendimento, gargalo, lead time
  whatif_etapas.csv    cenario x etapa: pessoas por turno, servidores, ocupacao, fila, saida
  whatif_inverso.csv   conta inversa: pessoas a mais por etapa e turno para atender uma demanda
Regra de turno: a do gemeo.py (NORMA MEL-250), sem mudanca. Pessoas = quem apontou (PROVISORIO).
Trancagem: maquinas rodando = min(11, pessoas x tranc_maq_por_pessoa); lotes simultaneos = maquinas x posicoes / 11.
Turno aberto em que ninguem aponta na Trancagem (3o turno tipico): as maquinas seguem rodando, como no backtest.

Uso: python -X utf8 gemeo_whatif.py
"""
import numpy as np, pandas as pd
import gemeo as G

SEMANAS, AQUEC, SEMENTE, META = 6, 2, 259, 97.0
COLS = ["id", "arr", "q0", "fam", "maq", "mang"]
NMAQ = len(G.TRANC)

def base90(L, pessoas, aberta):
    """Mix, demanda semanal, turnos abertos e equipe tipica dos ultimos 90 dias (fora a parada de julho)."""
    dias = [d for d in range(G.D_FIM - 89, G.D_FIM + 1) if not (G.PARADA_JUL[0] <= d <= G.PARADA_JUL[1])]
    lot = G.lotes_reais(L); dd = lot.arr.map(lambda m: G.turno_de(m)[0])
    pool = lot[dd.isin(dias)].copy(); dp = dd[pool.index]
    pool["off"] = pool.arr - (dp - (dp + 5) % 7) * 1440          # minutos desde a segunda 05:20 da semana da OP
    demanda = float(pool.q0.sum() / (len(dias) / 7))
    aberto, tip = {}, {}
    for w in range(7):
        dw = [d for d in dias if (d + 5) % 7 == w]
        for t in (1, 2, 3):
            ab = [d for d in dw if (d, t) in aberta]
            aberto[(w, t)] = bool(dw) and len(ab) / len(dw) >= 0.5
            for e in G.ETAPAS:
                tip[(e, w, t)] = float(np.median([pessoas[e].get((d, t), 0) for d in ab])) if ab else 0.0
    return pool.reset_index(drop=True), demanda, aberto, tip

D0 = G.D_FIM + (7 - (G.D_FIM + 5) % 7)       # primeira segunda depois do historico
T0, T1 = (D0 + 7 * AQUEC) * 1440, (D0 + 7 * SEMANAS) * 1440

def gerar(pool, m_sem):
    """OPs sorteadas do mix ate fechar `m_sem` metros liberados por semana; hora de liberacao = a da OP sorteada."""
    out = []
    for s in range(SEMANAS):
        if m_sem <= 0 or pool.empty: break
        rng = np.random.default_rng([SEMENTE, s]); acc = 0.0
        while acc < m_sem:
            r = pool.iloc[int(rng.integers(len(pool)))]
            if acc and acc + r.q0 - m_sem > m_sem - acc: break
            acc += r.q0
            out.append((len(out) + 1, (D0 + 7 * s) * 1440 + r.off, r.q0, r.fam, r.maq, r.mang))
    return pd.DataFrame(out, columns=COLS)

def calendario(P, aberto, tip, delta=None, fixo=None):
    """cal[e] = [(t0, t1, servidores)] das 6 semanas. Equipe = tipica (dia da semana x turno) + delta[(etapa, turno)];
    fixo[(etapa, turno)] troca a equipe tipica por um numero fixo de pessoas. Devolve tambem gente[(e, t)] (dia util mediano)."""
    delta = delta or {}; fixo = fixo or {}; cal = {e: [] for e in G.ETAPAS}; gente = {}
    pos = sum(P["tranc_pos"].values()); k = P["tranc_maq_por_pessoa"]
    for d in range(D0, D0 + 7 * SEMANAS):
        w = (d + 5) % 7
        for t in (1, 2, 3):
            a, b = G.slot_lim(d, t)
            for e in G.ETAPAS:
                mexeu = (e, t) in fixo or delta.get((e, t), 0) != 0
                p0 = int(fixo.get((e, t), int(round(tip[(e, w, t)]))))
                sozinha = e == "tranc" and p0 == 0 and (e, t) not in fixo      # turno aberto sem ninguem apontando na Trancagem:
                p = 0 if sozinha else max(0, p0 + delta.get((e, t), 0))        # o backtest roda as maquinas; pessoa a mais nao muda
                if not aberto[(w, t)]: c = 0
                elif e == "tranc": c = min(pos, int(round((NMAQ if sozinha else min(NMAQ, p * k)) * pos / NMAQ)))   # maquinas -> lotes simultaneos
                elif e in G.RITMO_MAQUINA: c = 0 if (mexeu and p == 0) else P["maquinas"][e]   # autoclave roda com a fabrica aberta
                else: c = min(P["maquinas"][e], p)
                cal[e].append((a, b, c))
                if aberto[(w, t)] and w < 5: gente.setdefault((e, t), []).append(p)
    return cal, {kk: float(np.median(v)) for kk, v in gente.items()}

def medir(lotes, res, uso, P):
    """Indicadores nas 4 semanas medidas. Ocupacao e do horizonte inteiro (o motor nao separa por janela)."""
    r = res.merge(lotes[["id", "arr", "q0"]], on="id") if len(lotes) else pd.DataFrame(columns=["id", "arr", "q0"] + [f"{e}_{s}" for e in G.ETAPAS for s in "ifq"])
    jan = r.arr.between(T0, T1, inclusive="left"); rend = float(np.prod([P["rend"][e] for e in G.ETAPAS]))
    lib = float(r.loc[jan, "q0"].sum()); ent = float(r.loc[r.ext_f.between(T0, T1, inclusive="left"), "ext_q"].sum())
    lead = ((r.ext_f - r.arr)[jan] / 60).dropna(); n = int(jan.sum())
    geral = {"demanda_m_sem": round(lib / (SEMANAS - AQUEC), 1), "entregue_m_sem": round(ent / (SEMANAS - AQUEC), 1),
             "atendimento_pct": round(100 * ent / (lib * rend), 1) if lib else np.nan,
             "lead_mediana_h": round(float(lead.median()), 1) if len(lead) else np.nan,
             "lead_p75_h": round(float(lead.quantile(.75)), 1) if len(lead) else np.nan,
             "ops_liberadas": n, "ops_concluidas_pct": round(100 * len(lead) / n, 1) if n else np.nan,
             "wip_final_m": round(float(r.loc[(r.arr < T1) & r.ext_f.isna(), "q0"].sum()), 1)}
    etapas = []; ch = r.arr
    for i, e in enumerate(G.ETAPAS):
        if i: ch = r[G.ETAPAS[i - 1] + "_f"] + P["transf"][e]
        m = ch.between(T0, T1, inclusive="left"); esp = (r[e + "_i"].fillna(T1) - ch)[m].clip(lower=0) / 60
        preso = (ch < T1) & r[e + "_i"].isna()
        etapas.append({"etapa": e, "etapa_nome": G.NOME[e], "ordem": i + 1,
                       "ocupacao_pct": round(100 * uso[e][0] / uso[e][1], 1) if uso[e][1] else np.nan,
                       "espera_media_h": round(float(esp.mean()), 1) if len(esp) else 0.0,
                       "fila_final_ops": int(preso.sum()), "fila_final_m": round(float(r.loc[preso, e + "_q"].sum()), 1),
                       "saida_m_sem": round(float(r.loc[r[e + "_f"].between(T0, T1, inclusive="left"), e + "_q"].sum()) / (SEMANAS - AQUEC), 1)})
    esp = max(etapas, key=lambda x: x["espera_media_h"]); fil = max(etapas, key=lambda x: x["fila_final_m"])
    geral["gargalo"] = esp["etapa_nome"] if esp["espera_media_h"] > 0 else ""
    geral["etapa_maior_fila_final"] = fil["etapa_nome"] if fil["fila_final_m"] > 0 else ""
    return geral, etapas, (fil["etapa"] if fil["fila_final_m"] > 0 else esp["etapa"])

def cenario(P, pool, aberto, tip, m_sem, delta=None, fixo=None, maquinas=None):
    """Roda um cenario. maquinas = {etapa: n} troca o numero de servidores da etapa (nao vale para a Trancagem)."""
    if maquinas: P = {**P, "maquinas": {**P["maquinas"], **maquinas}}
    lotes = gerar(pool, m_sem); cal, gente = calendario(P, aberto, tip, delta, fixo)
    res, uso = G.simular(lotes, P, cal)
    geral, etapas, pior = medir(lotes, res, uso, P)
    for x in etapas:
        e = x["etapa"]
        for t in (1, 2, 3): x[f"pessoas_t{t}"] = gente.get((e, t), 0.0)
        x["servidores_max"] = max((c for _, _, c in cal[e]), default=0)
    return geral, etapas, pior, gente

def inverso(P, pool, aberto, tip, m_sem, passos=15):
    """Soma uma pessoa por vez na etapa com mais metros presos no fim, no turno com menos gente, ate atender META %."""
    delta = {}; pos = sum(P["tranc_pos"].values()); k = P["tranc_maq_por_pessoa"]
    for n in range(passos + 1):
        geral, _, g, gente = cenario(P, pool, aberto, tip, m_sem, delta)
        if not (geral["atendimento_pct"] < META): return delta, geral, "atende" if geral["ops_liberadas"] else "sem demanda"
        if g == "vulc": return delta, geral, "limite de máquina na Vulcanização: pessoa não resolve"
        cap = (lambda p: 0 < p and p * k < NMAQ) if g == "tranc" else (lambda p: p < P["maquinas"][g])
        cand = sorted((gente.get((g, t), 0.0), t) for t in (1, 2, 3) if (g, t) in gente and cap(gente[(g, t)]))
        if not cand: return delta, geral, f"limite de máquina na {G.NOME[g]}: pessoa não resolve"
        if n == passos: break
        delta[(g, cand[0][1])] = delta.get((g, cand[0][1]), 0) + 1
    return delta, geral, f"não fechou em {passos} pessoas a mais"

def main():
    L = G.carregar(); pessoas, aberta = G.slots_reais(L); P = G.ler_params()
    pool, dem, aberto, tip = base90(L, pessoas, aberta)
    T = (1, 2, 3); todos = lambda e, n: {(e, t): n for t in T}
    CEN = [("base", "Demanda e equipe dos últimos 90 dias", 1.0, {}),
           ("demanda_-20", "Demanda 20% menor, mesma equipe", 0.8, {}),
           ("demanda_+10", "Demanda 10% maior, mesma equipe", 1.1, {}),
           ("demanda_+20", "Demanda 20% maior, mesma equipe", 1.2, {}),
           ("demanda_+30", "Demanda 30% maior, mesma equipe", 1.3, {}),
           ("tranc_+1", "Uma pessoa a mais na Trançagem em cada turno", 1.0, todos("tranc", 1)),
           ("tranc_-1", "Uma pessoa a menos na Trançagem em cada turno", 1.0, todos("tranc", -1)),
           ("ext_+1", "Uma pessoa a mais na Extração/Teste em cada turno", 1.0, todos("ext", 1)),
           ("ext_-1", "Uma pessoa a menos na Extração/Teste em cada turno", 1.0, todos("ext", -1)),
           ("sem_3o_turno", "Sem 3º turno em nenhuma etapa", 1.0, None),
           ("demanda_+20_tranc_+1", "Demanda 20% maior com uma pessoa a mais na Trançagem", 1.2, todos("tranc", 1)),
           ("demanda_+20_ext_+1", "Demanda 20% maior com uma pessoa a mais na Extração/Teste", 1.2, todos("ext", 1))]
    cen, eta = [], []
    for nome, desc, f, delta in CEN:
        geral, etapas, _, _ = cenario(P, pool, aberto, tip, f * dem, delta, fixo=None if delta is not None else {(e, 3): 0 for e in G.ETAPAS})
        cen.append({"cenario": nome, "descricao": desc, "demanda_fator": f, **geral})
        eta += [{"cenario": nome, **x} for x in etapas]
    inv = []
    for f in (1.0, 1.2, 1.5):
        delta, geral, status = inverso(P, pool, aberto, tip, f * dem)
        _, gente = calendario(P, aberto, tip); _, nova = calendario(P, aberto, tip, delta)
        for e in G.ETAPAS:
            for t in T:
                inv.append({"demanda_fator": f, "demanda_m_sem": geral["demanda_m_sem"], "etapa": e, "etapa_nome": G.NOME[e],
                            "ordem": G.ETAPAS.index(e) + 1, "turno": t, "pessoas_base": gente.get((e, t), 0.0),
                            "pessoas_necessarias": nova.get((e, t), 0.0), "pessoas_a_mais": delta.get((e, t), 0),
                            "atendimento_pct": geral["atendimento_pct"], "lead_mediana_h": geral["lead_mediana_h"], "situacao": status})
    cen, eta, inv = pd.DataFrame(cen), pd.DataFrame(eta), pd.DataFrame(inv)
    cen.to_csv(G.SAIDA / "whatif_cenarios.csv", index=False, encoding="utf-8-sig")
    eta.to_csv(G.SAIDA / "whatif_etapas.csv", index=False, encoding="utf-8-sig")
    inv.to_csv(G.SAIDA / "whatif_inverso.csv", index=False, encoding="utf-8-sig")
    print(f"mix: {len(pool)} OPs, demanda base {dem:.0f} m/sem, tranc_maq_por_pessoa {P['tranc_maq_por_pessoa']}")
    print(cen[["cenario", "demanda_m_sem", "entregue_m_sem", "atendimento_pct", "gargalo", "lead_mediana_h", "wip_final_m"]].to_string(index=False))
    print(inv[inv.pessoas_a_mais > 0][["demanda_fator", "etapa", "turno", "pessoas_base", "pessoas_necessarias"]].to_string(index=False))
    print(inv.groupby("demanda_fator")[["atendimento_pct", "situacao"]].first().to_string())

if __name__ == "__main__":
    main()
