"""APS simples do gemeo (missao P2, item 2): mesma carteira de uma semana real, tres regras de fila na Trancagem.

  chegada   ordem de chegada na Trancagem (o que o gemeo faz no backtest)
  agrupar   junta por bitola e mangueira (menos troca de bitola e de mangueira)
  menor     menor lote primeiro

A semana e escolhida sozinha: entre as 8 ultimas semanas completas do historico, a de metros liberados mais perto da
mediana. Simula com o calendario real (pessoas que apontaram), 3 semanas antes para encher a fabrica e 3 depois para
escoar. So as OPs da semana mudam de prioridade; as demais seguem por chegada. Duas formas de liberar a carteira:
  real      cada OP entra no Mandril na hora real de liberacao
  segunda   a carteira inteira entra na segunda 05:20, ja na ordem da regra (o sequenciador enxerga a semana toda)
Setup = o do gemeo (por apontamento, PROVISORIO; a regra do GMS e de peca boa a peca boa).

Saida: saida/aps_regras.csv (uma linha por regra x liberacao) e saida/aps_diario.csv (metros por dia da carteira).
Uso: python -X utf8 gemeo_aps.py
"""
import numpy as np, pandas as pd
import gemeo as G

REGRAS = {"chegada": "Ordem de chegada", "agrupar": "Agrupar por bitola e mangueira", "menor": "Menor lote primeiro"}
ORDEM_FAM = {"3-4": 0, "6": 1, "7-8": 2, "10": 3, "12": 4, "16+": 5, "ND": 6}

def semana_tipica(lotes):
    seg = (G.D_FIM - (G.D_FIM + 5) % 7) - 7                       # ultima segunda com semana completa
    d = lotes.arr.map(lambda m: G.turno_de(m)[0])
    m = {s: float(lotes.q0[(d >= s) & (d < s + 7)].sum()) for s in range(seg - 49, seg + 1, 7)}
    med = float(np.median(list(m.values())))
    return min(m, key=lambda s: abs(m[s] - med))

def ordem(cart, regra):
    if regra == "agrupar": return list(cart.assign(k=cart.fam.map(ORDEM_FAM)).sort_values(["k", "mang", "arr"]).id)
    return list(cart.sort_values(["q0", "arr"] if regra == "menor" else ["arr"]).id)

def prioridade(ids, regra, w0):
    """Chegada virtual na fila da Trancagem: a ordem da regra espalhada pela semana (mesma escala das demais OPs)."""
    if regra == "chegada" or not ids: return None
    return {i: w0 + 7 * 1440 * n / len(ids) for n, i in enumerate(ids)}

def setups(res, lotes, P):
    """Refaz o setup que o motor cobrou: por maquina, na ordem de inicio, compara cada lote com o anterior."""
    st = P["setup_tranc"]; x = res[["id", "tranc_i"]].merge(lotes[["id", "maq", "mang", "fam"]], on="id").dropna(subset=["tranc_i"])
    out = {}
    for _, g in x.sort_values("tranc_i").groupby("maq"):
        ant = None
        for r in g.itertuples():
            tipo = "mesma" if (ant is None or ant[0] == r.mang) else "mang" if ant[1] == r.fam else "bitola"
            out[r.id] = (tipo, st["mesma_mangueira_min"] if tipo == "mesma" else st["troca_mangueira_min"] if tipo == "mang" else st["troca_bitola_min"])
            ant = (r.mang, r.fam)
    return out

def rodar(lotes, P, cal, seg, regra, liberacao):
    w0, w1 = seg * 1440, (seg + 7) * 1440
    sim = lotes[(lotes.arr >= w0 - 21 * 1440) & (lotes.arr < w1 + 21 * 1440)].copy()
    na = (sim.arr >= w0) & (sim.arr < w1)
    ids = ordem(sim[na], regra)
    if liberacao == "segunda":      # um minuto entre uma OP e a seguinte: o Mandril ja recebe a carteira na ordem da regra
        sim.loc[na, "arr"] = sim.loc[na, "id"].map({i: w0 + float(n) for n, i in enumerate(ids)})
    cart = sim[na]
    res, _ = G.simular(sim, P, cal, pri=prioridade(ids, regra, w0))
    r = res[res.id.isin(cart.id)].merge(cart[["id", "arr", "q0"]], on="id")
    su = setups(res, sim, P); s = [su[i] for i in r.id if i in su]
    lead = ((r.ext_f - r.arr) / 60).dropna(); fim = (r.ext_f.max() - w0) / 1440 if len(lead) else np.nan
    dia = lambda e: r.dropna(subset=[e + "_f"]).groupby(r[e + "_f"].dropna().map(lambda m: G.turno_de(m)[0]))[e + "_q"].sum()
    te, tt = dia("ext"), dia("tranc")
    linha = {"regra": regra, "regra_nome": REGRAS[regra], "liberacao": liberacao, "semana_ref": G.data_ref(seg),
             "ops": len(r), "metros_liberados": round(float(r.q0.sum()), 1),
             "setup_total_min": round(sum(v for _, v in s), 1), "setup_total_h": round(sum(v for _, v in s) / 60, 1),
             "trocas_bitola": sum(t == "bitola" for t, _ in s), "trocas_mangueira": sum(t == "mang" for t, _ in s),
             "ext_m_por_dia_na_semana": round(float(te[te.index < seg + 7].sum()) / 7, 1),
             "ext_m_ate_dia_14": round(float(te[te.index < seg + 14].sum()), 1),
             "tranc_m_por_dia_na_semana": round(float(tt[tt.index < seg + 7].sum()) / 7, 1),
             "lead_mediana_h": round(float(lead.median()), 1) if len(lead) else np.nan,
             "lead_p75_h": round(float(lead.quantile(.75)), 1) if len(lead) else np.nan,
             "ops_concluidas_pct": round(100 * len(lead) / len(r), 1) if len(r) else np.nan,
             "dias_ate_ultima_op": round(float(fim), 1) if len(lead) else np.nan}
    dias = sorted(set(te.index) | set(tt.index))
    diario = [{"regra": regra, "regra_nome": REGRAS[regra], "liberacao": liberacao, "data_ref": G.data_ref(d), "dia_da_semana_ref": d - seg + 1,
               "tranc_m": round(float(tt.get(d, 0)), 1), "ext_m": round(float(te.get(d, 0)), 1)} for d in dias]
    return linha, diario

def main():
    L = G.carregar(); pessoas, aberta = G.slots_reais(L); P = G.ler_params()
    lotes = G.lotes_reais(L); cal = G.cal_real(P, pessoas, aberta); seg = semana_tipica(lotes)
    linhas, diario = [], []
    for lib in ("real", "segunda"):
        for regra in REGRAS:
            a, b = rodar(lotes, P, cal, seg, regra, lib); linhas.append(a); diario += b
    df = pd.DataFrame(linhas)
    df.to_csv(G.SAIDA / "aps_regras.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(diario).to_csv(G.SAIDA / "aps_diario.csv", index=False, encoding="utf-8-sig")
    print("semana de", G.data_ref(seg))
    print(df[["regra", "liberacao", "ops", "setup_total_h", "trocas_bitola", "trocas_mangueira", "ext_m_por_dia_na_semana",
              "ext_m_ate_dia_14", "lead_mediana_h", "lead_p75_h", "ops_concluidas_pct", "dias_ate_ultima_op"]].to_string(index=False))

if __name__ == "__main__":
    main()
