"""Backtest do simulador (trancagem -> cabine). Gera backtest_simulador.md.
capacidade_turno = min(pessoas x prod_mediana x minutos, teto_turno); cadeia com estoque entre etapas."""
import numpy as np
import pandas as pd
import calibrar_simulador as C

E = C.ETAPAS
NOME = {"tranc": "Trancagem", "cob": "Cobertura", "band": "Bandagem", "vulc": "Vulcanizacao", "deb": "Debandagem", "cab": "Cabine (extracao)"}
MD = C.AQUI / "backtest_simulador.md"


class Dados:
    pass


def preparar():
    d = C.carregar()
    cel = C.celulas(d)
    pn = C.painel(cel)
    prov = not C.aplicar_escala(pn)
    dias, exc, baixo = C.dias_atipicos(cel)
    dias = dias[dias >= C.JANELA_INI]
    X = Dados()
    X.prov, X.dias, X.exc, X.baixo, X.pn = prov, dias, exc, baixo, pn
    n = len(dias)
    ix = {x: i for i, x in enumerate(dias)}
    X.real = {e: np.zeros(n) for e in E}
    X.hc = {e: np.zeros((n, 3)) for e in E}
    X.share = {e: np.zeros((n, len(C.FAMILIAS))) for e in E}
    X.cell_m = {e: np.zeros((n, 3)) for e in E}
    for e in E:
        q = pn[e][pn[e].dref.isin(ix)]
        ii = q.dref.map(ix).values
        tt = q.turno.astype(int).values - 1
        np.add.at(X.real[e], ii, q.m.values)
        X.hc[e][ii, tt] = q.pessoas.values
        X.cell_m[e][ii, tt] = q.m.values
        for k, fa in enumerate(C.FAMILIAS):
            np.add.at(X.share[e][:, k], ii, q["f_" + fa].values)
        s = X.share[e].sum(1, keepdims=True)
        X.share[e] = np.divide(X.share[e], s, out=np.zeros_like(X.share[e]), where=s > 0)
    X.valid = np.array([(x not in exc) and X.real["tranc"][i] > 0 for i, x in enumerate(dias)])
    return X


def capacidade(X, e, P, usar_mix):
    n = len(X.dias)
    cap = np.zeros(n)
    pm = P["prod_etapa"][e]
    fator = np.ones(n)
    if usar_mix:
        r = np.array([pm / P["prod_fam"][(e, f)] if not np.isnan(P["prod_fam"][(e, f)]) else 1.0 for f in C.FAMILIAS])
        den = (X.share[e] * r).sum(1)
        fator = np.where(den > 0, 1 / np.where(den > 0, den, 1), 1.0)
    for t in (1, 2, 3):
        c = X.hc[e][:, t - 1] * P["prod"][(e, t)] * P.get("k", 1.0) * fator * C.MIN_TURNO[t]
        cap += np.minimum(c, P["teto_turno"][e])
    return np.minimum(cap, P["teto_dia"][e])


def estagio(entrada, cap, estoque):
    n = len(entrada)
    s = np.zeros(n)
    est = 0.0
    for i in range(n):
        disp = (est if estoque else 0.0) + entrada[i]
        s[i] = min(cap[i], disp)
        est = disp - s[i]
    return s


def deslocar(v, lag):
    if lag == 0:
        return v
    o = np.zeros_like(v)
    o[lag:] = v[:-lag]
    return o


def simular(X, P, cfg, lags=None):
    """cfg: dict(estoque, mix, atraso). Retorna saidas por etapa."""
    saida = {}
    ent = X.real["tranc"].copy()  # demanda do dia
    saida["tranc"] = estagio(ent, capacidade(X, "tranc", P, cfg["mix"]), cfg["estoque"])
    for e in E[1:]:
        lag = (lags or {}).get(e, 0) if cfg["atraso"] else 0
        ent = deslocar(saida[E[E.index(e) - 1]], lag)
        saida[e] = estagio(ent, capacidade(X, e, P, cfg["mix"]), cfg["estoque"])
    return saida


def metricas(pred, real, mask, dias):
    m = mask & (real > 0)
    if m.sum() == 0:
        return dict(n=0, mape=np.nan, wape=np.nan, vies=np.nan, mape_sem=np.nan, ok15=np.nan)
    p, r = pred[m], real[m]
    ape = np.abs(p - r) / r
    df = pd.DataFrame({"p": p, "r": r, "sem": dias[m].to_period("W")})
    w = df.groupby("sem").agg(p=("p", "sum"), r=("r", "sum"), n=("p", "size"))
    w = w[w.n >= 3]
    return dict(n=int(m.sum()), mape=100 * ape.mean(), wape=100 * np.abs(p - r).sum() / r.sum(),
                vies=100 * (p.sum() - r.sum()) / r.sum(),
                mape_sem=100 * (np.abs(w.p - w.r) / w.r).mean() if len(w) else np.nan, ok15=100 * (ape <= .15).mean())


def calibrar(X, mask_dias):
    ok = {x for x, m in zip(X.dias, mask_dias) if m}
    return C.parametros(X.pn, ok, X.baixo)


def escolher_lags(X, P, mask):
    lags = {}
    cfg = dict(estoque=True, mix=False, atraso=True)
    saida = {}
    ent = X.real["tranc"].copy()
    saida["tranc"] = estagio(ent, capacidade(X, "tranc", P, False), True)
    for e in E[1:]:
        melhor = None
        for lag in (0, 1, 2):
            ent = deslocar(saida[E[E.index(e) - 1]], lag)
            s = estagio(ent, capacidade(X, e, P, False), True)
            w = metricas(s, X.real[e], mask, X.dias)["wape"]
            if melhor is None or w < melhor[0] - 0.5:  # exige ganho de 0,5 pp
                melhor = (w, lag, s)
        lags[e] = melhor[1]
        saida[e] = melhor[2]
    return lags


def tab(linhas, cab):
    s = "| " + " | ".join(cab) + " |\n|" + "---|" * len(cab) + "\n"
    for l in linhas:
        s += "| " + " | ".join(l) + " |\n"
    return s


def f(x, d=1):
    return "-" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:.{d}f}"


def linha_met(nome, m):
    return [nome, str(m["n"]), f(m["mape"]), f(m["wape"]), f(m["vies"]), f(m["mape_sem"]), f(m["ok15"], 0)]


CAB = ["Etapa", "dias", "MAPE diario %", "WAPE %", "Vies %", "MAPE semanal %", "dias com erro <=15 %"]


def main():
    X = preparar()
    idx_val = np.where(X.valid)[0]
    corte = idx_val[int(len(idx_val) * 0.7) - 1]
    treino = np.zeros(len(X.dias), bool)
    treino[:corte + 1] = True
    m_tr, m_te = X.valid & treino, X.valid & ~treino
    P = calibrar(X, m_tr)
    # fator de escala k (produtividade efetiva = k x mediana), escolhido no treino pelo WAPE da cabine
    cand = []
    for k in (1.0, 1.1, 1.2, 1.3, 1.4, 1.5):
        P["k"] = k
        sk = simular(X, P, dict(estoque=True, mix=False, atraso=False))
        cand.append((metricas(sk["cab"], X.real["cab"], m_tr, X.dias)["wape"], k))
    P["k"] = min(cand)[1]
    k_esc = P["k"]
    lags = escolher_lags(X, P, m_tr)

    variantes = [("V0 base (prod. mediana etapa x turno, sem estoque)", dict(estoque=False, mix=False, atraso=False)),
                 ("V1 + estoque entre etapas", dict(estoque=True, mix=False, atraso=False)),
                 ("V2 + mix por bitola", dict(estoque=True, mix=True, atraso=False)),
                 ("V3 + atraso entre etapas", dict(estoque=True, mix=True, atraso=True)),
                 ("V4 estoque + atraso (sem mix)", dict(estoque=True, mix=False, atraso=True))]
    res_v = []
    for nome, cfg in variantes:
        s = simular(X, P, cfg, lags)
        res_v.append((nome, cfg, s, metricas(s["cab"], X.real["cab"], m_tr, X.dias), metricas(s["cab"], X.real["cab"], m_te, X.dias)))
    # escolha pelo WAPE de TREINO da cabine
    esc = min(res_v, key=lambda r: r[3]["wape"])
    nome_f, cfg_f, S, _, _ = esc

    # baseline ingenuo: mediana de metros do dia (treino) para cada etapa
    base = {e: np.full(len(X.dias), np.median(X.real[e][m_tr & (X.real[e] > 0)])) for e in E}

    # leave-one-month-out
    meses = pd.Series(X.dias.to_period("M"))
    pred_lomo = {e: np.full(len(X.dias), np.nan) for e in E}
    for mes in meses.unique():
        sel = (meses == mes).values
        P2 = calibrar(X, X.valid & ~sel)
        P2["k"] = k_esc
        S2 = simular(X, P2, cfg_f, lags)
        for e in E:
            pred_lomo[e][sel] = S2[e][sel]

    md = ["# Backtest do simulador de headcount x demanda (trancagem -> cabine)", "",
          f"Gerado por `backtest_simulador.py` (dados ate {X.dias[-1].date()}). Headcount **{'PROVISORIO (operadores distintos que apontaram a etapa no data_ref-turno)' if X.prov else 'de escala_real.csv'}**.",
          "", "## Modelo",
          "- `capacidade_turno = min(pessoas x prod_mediana(etapa,turno) x minutos_turno, teto_p95_turno)`; dia = soma dos 3 turnos, limitada ao teto p95 do dia.",
          "- Cadeia: demanda do dia = metros reais de trancagem do data_ref. `saida(etapa,dia) = min(capacidade_dia, estoque + entrada)`; entrada = saida da etapa anterior (com atraso em dias quando melhora o acerto). Volume da cabine = saida da ultima.",
          "- Turnos pela hora do apontamento final (NORMA 27/10/2026, MEL-250): T1 05:20-13:56 (517 min), T2 13:57-22:19 (503), T3 22:20-05:19 (420); data_ref comeca 05:20.",
          f"- Janela: a partir de {C.JANELA_INI.date()} (antes, debandagem/cabine nao tinham apontamento completo). Fichas Canceladas fora.",
          f"- Treino: ate {X.dias[corte].date()} ({int(m_tr.sum())} dias uteis); teste fora da amostra: {int(m_te.sum())} dias ate {X.dias[-1].date()}.",
          f"- Fator de escala da produtividade (k x mediana), escolhido no treino: **{k_esc}** (candidatos 1.0 a 1.5; k=1 e a mediana pura; k>1 compensa o vies de subestimar dias fortes). Variantes V0-V4 usam esse k.",
          f"- Configuracao final (escolhida pelo WAPE de treino da cabine): **{nome_f}**; atraso em dias por etapa: {lags if cfg_f['atraso'] else 'nao usado'}.", ""]

    for titulo, mask, pred in [("Fora da amostra (teste, ~30% finais; parametros do treino, mas headcount e demanda de trancagem observados no proprio dia: nao e previsao pura)", m_te, S),
                               ("Dentro da amostra (treino, ~70% iniciais)", m_tr, S)]:
        md += [f"## {titulo} - modelo final", tab([linha_met(NOME[e], metricas(pred[e], X.real[e], mask, X.dias)) for e in E], CAB)]
    md += ["## Leave-one-month-out (PARCIALMENTE dentro da amostra: k e atrasos escolhidos com treino que inclui os meses testados)",
           tab([linha_met(NOME[e], metricas(pred_lomo[e], X.real[e], X.valid & ~np.isnan(pred_lomo[e]), X.dias)) for e in E], CAB)]
    md += ["## Baseline ingenuo (mediana de metros/dia do treino) - fora da amostra",
           tab([linha_met(NOME[e], metricas(base[e], X.real[e], m_te, X.dias)) for e in E], CAB)]

    md += ["## O que foi ajustado (cabine, MAPE/WAPE %: treino | teste)",
           tab([[r[0], f(r[3]["mape"]) + " / " + f(r[3]["wape"]), f(r[4]["mape"]) + " / " + f(r[4]["wape"]), f(r[4]["vies"])] for r in res_v],
               ["Variante", "treino MAPE/WAPE", "teste MAPE/WAPE", "vies teste %"]), "",
           "Leitura: o estoque entre etapas ajuda no treino (reduz o vies); o mix por bitola PIORA (a produtividade por familia vem de celulas dominadas por uma bitola, poucas e ruidosas, e o headcount provisorio confunde); o atraso em dias nao melhorou o acerto (lead time mediano e de horas, menor que 1 dia). O modelo calibrado NAO bate o baseline ingenuo (mediana do dia) na maioria das etapas: com o headcount provisorio, a capacidade pessoas x produtividade nao explica o volume diario melhor que a mediana.", ""]

    # 10 piores dias (cabine, todos validos)
    real, pred = X.real["cab"], S["cab"]
    err = np.where(X.valid & (real > 0), np.abs(pred - real), -1)
    medcab = np.median(real[X.valid & (real > 0)])
    top = np.argsort(-err)[:10]
    # estoque na entrada da cabine
    est_cab = np.cumsum(deslocar(S["deb"], lags["cab"] if cfg_f["atraso"] else 0) - S["cab"])
    linhas = []
    for i in top:
        dia = X.dias[i]
        mot = []
        if real[i] < 0.5 * medcab:
            mot.append("dia de poucos metros na cabine (real < 50% da mediana)")
        if any((dia - pd.Timedelta(days=k)) in X.exc and "parada" in X.exc[dia - pd.Timedelta(days=k)] for k in range(1, 4)):
            mot.append("retomada logo apos parada")
        if est_cab[i] > 0.3 * real[i]:
            mot.append("estoque acumulado na entrada da cabine")
        if X.hc["cab"][i].sum() <= 2:
            mot.append("headcount da cabine muito baixo no apontamento")
        den = (X.share["cab"][i] * np.array([P["prod_etapa"]["cab"] / P["prod_fam"][("cab", f_)] if not np.isnan(P["prod_fam"][("cab", f_)]) else 1 for f_ in C.FAMILIAS])).sum()
        if den > 0 and (1 / den < 0.9 or 1 / den > 1.1):
            mot.append(f"mix de bitola (fator {1 / den:.2f})")
        if pred[i] >= P["teto_dia"]["cab"] - 1:
            mot.append("modelo bateu no teto do dia")
        if not mot:
            mot.append("lote/hora de apontamento da cabine desacoplado da trancagem do dia (lead time), sem causa unica nos dados")
        linhas.append([str(dia.date()), "teste" if m_te[i] else "treino", f(real[i], 0), f(pred[i], 0), f(100 * (pred[i] - real[i]) / real[i], 0), "; ".join(mot)])
    md += ["## 10 dias que mais erraram na cabine (maior erro absoluto em metros; motivo = heuristica a partir dos dados)",
           tab(linhas, ["data_ref", "periodo", "real m", "previsto m", "erro %", "motivo provavel"]), ""]

    # teste da conta inversa
    tot = ok_sem = ok_com = 0
    falhas = 0
    for e in E:
        for t in (1, 2, 3):
            cm = X.cell_m[e][:, t - 1]
            for i in np.where(X.valid & (cm > 0))[0]:
                n = C.pessoas_necessarias(cm[i], e, t, P)
                cap_sem = n * P["prod"][(e, t)] * P.get("k", 1.0) * C.MIN_TURNO[t]
                cap_com = min(cap_sem, P["teto_turno"][e])
                tot += 1
                ok_sem += cap_sem >= cm[i] - 1e-6
                ok_com += cap_com >= min(cm[i], P["teto_turno"][e]) - 1e-6
    md += ["## Teste da conta inversa (pessoas necessarias vs capacidade direta)",
           f"`pessoas_necessarias(demanda, etapa, turno, params)` = ceil(demanda_turno / (prod_mediana x k x minutos)). Isto e VERIFICACAO ARITMETICA (verdadeira por construcao), nao validacao do modelo. Para cada celula etapa x turno x dia valido ({tot} celulas), rodou-se a capacidade direta com essas pessoas: "
           f"capacidade >= demanda em **{ok_sem}/{tot}** celulas (sem teto) e, com o teto de maquina, capacidade >= min(demanda, teto) em **{ok_com}/{tot}**. "
           f"Demandas acima do teto p95 do turno sao inviaveis pelo teto empirico mesmo com mais gente (o modelo sinaliza gargalo de maquina).", ""]

    # dias excluidos
    por_motivo = {}
    for dia, mot in sorted(X.exc.items()):
        if dia >= C.JANELA_INI:
            por_motivo.setdefault(mot, []).append(str(dia.date()))
    md += ["## Dias excluidos (janela a partir de 01/03/2026)"]
    for mot, ds in por_motivo.items():
        if mot.startswith("sem producao"):
            md.append(f"- {mot}: {len(ds)} dias (nao listados).")
        else:
            md.append(f"- {mot}: {len(ds)} dias: {', '.join(ds)}")
    md += ["- Antes de 01/03/2026: excluido por falta de apontamento completo de debandagem/cabine (inclui a parada de dez/2025-jan/2026).", ""]

    # pendencias
    mc = metricas(S["cab"], X.real["cab"], m_te, X.dias)
    atingiu = mc["mape"] <= 15
    md += ["## Meta (erro diario <= 10-15%) e o que falta",
           f"- Cabine fora da amostra: MAPE {f(mc['mape'])}%, WAPE {f(mc['wape'])}%, {f(mc['ok15'], 0)}% dos dias com erro <= 15%. **Meta {'atingida' if atingiu else 'NAO atingida'}** no diario.",
           "- Limitacoes sem maquiagem: (1) headcount provisorio = quem apontou, nao quem estava escalado (pessoas que apontam por colega, ou escalados que nao apontam, distorcem pessoa x minuto e criam circularidade: mais fichas => mais operadores distintos); (2) a demanda usada e a trancagem realizada, nao a demanda real do cliente; (3) o apontamento e em lotes/ fichas fechadas por hora, entao a producao do dia na cabine depende de quando a ficha e fechada, nao so da capacidade; (4) sem horas extras, paradas de maquina e setups por dia no modelo.",
           "- Proximo passo para fechar a meta: `escala_real.csv` (data_ref,turno,etapa,pessoas) com a escala real de alguns meses, e a demanda real; basta soltar o arquivo na pasta e rodar `calibrar_simulador.py` e `backtest_simulador.py`.", ""]
    md += ["", "## Ressalvas da revisao (Opus)",
           "- Fora da amostra o estoque entre etapas nao melhora o erro diario da cabine; so ajuda no treino.",
           "- A trancagem 'ganha' do baseline em parte porque a demanda e a propria trancagem real do dia e o headcount e o de quem apontou no dia: nao e previsao pura.",
           "- Produtividade vem de fichas com operador; o real inclui fichas sem operador. Celulas com metros e sem operador ficam com capacidade 0 e o k pode compensar erro de dado.",
           "- parametros_simulador.csv e calibrado com todos os dias (inclui o teste); o k foi escolhido sobre parametros so de treino.",
           "- Produtividade (m/pessoa*min) NAO e a Meta HH do BI (velocidade x minutos); nao chamar de meta.",
           "- Pendente do William: hora extra do T2 (ate 23:20) cai no T3 pela fronteira 22:20 da NORMA; confirmar se serve ou se a escala real separa."]
    MD.write_text("\n".join(md), encoding="utf-8")
    print("gravado", MD)
    print("final:", nome_f, lags)
    for e in E:
        m = metricas(S[e], X.real[e], m_te, X.dias)
        print(e, "teste MAPE", f(m["mape"]), "WAPE", f(m["wape"]), "vies", f(m["vies"]), "baseMAPE", f(metricas(base[e], X.real[e], m_te, X.dias)["mape"]))


if __name__ == "__main__":
    main()
