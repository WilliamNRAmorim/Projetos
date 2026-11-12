"""Calibra o gemeo no treino (ate 12/08/2026) e mede o erro contra o real (teste: 13/08 a 05/10/2026).
Gera gemeo_parametros.json, saida/backtest_diario.csv, saida/backtest_resumo.csv e GEMEO_BACKTEST.md."""
import json, numpy as np, pandas as pd
import gemeo as G

L = G.carregar()
pessoas, aberta = G.slots_reais(L)
ATE = (G.D_TREINO + 1) * 1440
P = G.calibrar(L, pessoas, aberta, ATE)
P["paradas_hh"] = G.paradas_hh()
R, dias = G.dias_validos(L)
treino = [d for d in dias if d <= G.D_TREINO]; teste = [d for d in dias if d > G.D_TREINO]
lotes = G.lotes_reais(L)
FORA = {e: G.sem_registro(L, e) for e in G.ETAPAS}

# pessoas tipicas por etapa x dia da semana x turno (mediana do treino, slots abertos)
tip = {}
for e in G.ETAPAS:
    acc = {}
    for (d, t) in aberta:
        if d <= G.D_TREINO and d >= G.D_INI - 60: acc.setdefault(((d + 5) % 7, t), []).append(pessoas[e].get((d, t), 0))
    for k, v in acc.items(): tip[(e, k[0], k[1])] = float(np.median(v))
P["pessoas_tipicas"] = {f"{e}|{w}|{t}": v for (e, w, t), v in tip.items()}

# kappa por etapa: de cima para baixo, escolhe o fator do tempo de processo que minimiza o WAPE diario do treino
cal = G.cal_real(P, pessoas, aberta)
GRADE = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.35, 1.5, 1.75, 2.0]
for e in G.ETAPAS:
    melhor = None
    for k in GRADE:
        P["kappa"][e] = k
        res, _ = G.simular(lotes, P, cal, so_ate_etapa=e)
        m = G.metricas(R[e], G.serie_diaria(res, e, FORA[e]), treino)
        obj = m["wape"] + abs(m["vies"])      # sem o vies, o ajuste prefere saturar a etapa (saida constante) e a fila explode
        if k == 1.0: base = obj
        if melhor is None or obj < melhor[0]: melhor = (obj, k)
    P["kappa"][e] = melhor[1] if base - melhor[0] >= 1.5 else 1.0   # ganho pequeno: fica 1.0 (sem ajuste)
G.salvar_params(P)

def avaliar(nome, sim_por_etapa):
    out = []
    for e in G.ETAPAS:
        for per, dd in (("treino", treino), ("teste", teste)):
            out.append({"modelo": nome, "etapa": e, "periodo": per, **G.metricas(R[e], sim_por_etapa[e], dd)})
    return out

linhas = []; series = {}
# A) gemeo com pessoas observadas no slot
resA, usoA = G.simular(lotes, P, cal); series["gemeo_obs"] = {e: G.serie_diaria(resA, e, FORA[e]) for e in G.ETAPAS}
# B) gemeo com pessoas tipicas (mediana por dia da semana e turno; calendario de fabrica aberta e o real)
resB, _ = G.simular(lotes, P, G.cal_real(P, pessoas, aberta, tipico=tip)); series["gemeo_tipico"] = {e: G.serie_diaria(resB, e, FORA[e]) for e in G.ETAPAS}
# C) base ingenua: mediana de metros/dia do treino
series["mediana"] = {e: pd.Series({d: R[e].reindex(treino).median() for d in dias}) for e in G.ETAPAS}
# D) base "so desloca": cada lote sai da etapa com o atraso mediano do treino desde a liberacao, sem fila nem capacidade
des = {}
for e in G.ETAPAS:
    x = L[["id", e + "_f"]].merge(lotes[["id", "arr"]], on="id").dropna(); x = x[x[e + "_f"] <= ATE]
    at = float((x[e + "_f"] - x.arr).median())
    q = lotes.q0.where(~lotes.id.isin(FORA[e]), 0) * np.prod([P["rend"][s] for s in G.ETAPAS[:G.ETAPAS.index(e) + 1]])
    des[e] = q.groupby((lotes.arr + at).map(lambda m: G.turno_de(m)[0])).sum()
series["desloca"] = des
for nome, s in series.items(): linhas += avaliar(nome, s)
resumo = pd.DataFrame(linhas); resumo["etapa_nome"] = resumo.etapa.map(G.NOME); resumo["ordem"] = resumo.etapa.map(G.ETAPAS.index) + 1
resumo.to_csv(G.SAIDA / "backtest_resumo.csv", index=False, encoding="utf-8-sig")
diario = pd.DataFrame([{"data_ref": G.data_ref(d), "etapa": e, "etapa_nome": G.NOME[e], "ordem": G.ETAPAS.index(e) + 1,
                        "periodo": "treino" if d <= G.D_TREINO else "teste", "real_m": round(float(R[e].get(d, 0)), 1),
                        "gemeo_m": round(float(series["gemeo_obs"][e].get(d, 0)), 1), "gemeo_tipico_m": round(float(series["gemeo_tipico"][e].get(d, 0)), 1)}
                       for d in dias for e in G.ETAPAS])
diario.to_csv(G.SAIDA / "backtest_diario.csv", index=False, encoding="utf-8-sig")

# lead time (liberacao -> fim da extracao), em horas
def lt(df, arr): x = (df.ext_f - arr.reindex(df.index)).dropna() / 60; return x[(x > 0) & (x < 24 * 40)]
arr = lotes.set_index("id").arr
ltr = lt(L.set_index("id"), arr); lts = lt(resA.set_index("id"), arr)

def tab(nome, per):
    x = resumo[(resumo.modelo == nome) & (resumo.periodo == per)]
    s = "| Etapa | dias | MAPE dia % | WAPE dia % | Viés % | MAPE semana % | dias com erro ≤15 % |\n|---|---|---|---|---|---|---|\n"
    return s + "\n".join(f"| {r.etapa_nome} | {r.dias} | {r.mape} | {r.wape} | {r.vies} | {r.mape_sem} | {r.ate15} |" for r in x.itertuples()) + "\n"

piores = diario[(diario.etapa == "ext") & (diario.periodo == "teste")].assign(err=lambda x: (x.gemeo_m - x.real_m)).assign(a=lambda x: x.err.abs()).nlargest(6, "a")
uso_txt = "\n".join(f"| {G.NOME[e]} | {P['maquinas'][e]} | {P['kappa'][e]} | {round(100 * usoA[e][0] / max(1, usoA[e][1]))} | {round(P['rend'][e], 4)} | {round(P['transf'][e])} |" for e in G.ETAPAS)
h = P["paradas_hh"]; st = P["setup_tranc"]
md = f"""# Gêmeo digital da célula GMS: backtest (gerado por `gemeo_backtest.py`)

Dados: `ficha_producao.csv` (export de 06/10/2026, {len(lotes)} OPs não canceladas). Treino: 01/03 a 12/08/2026 ({len(treino)} dias válidos). Teste fora da amostra: 13/08 a 05/10/2026 ({len(teste)} dias). Fora: parada de 03 a 27/07 e dias com volume abaixo de 30% da mediana (mesmo critério do backtest de 01/11).

## Como o gêmeo funciona
- Cada OP entra no Mandril na hora real de liberação e percorre as 8 etapas. Em cada etapa espera na fila, ocupa um servidor (máquina com gente) e sai; a saída vira chegada da próxima.
- Turnos pela NORMA de 27/10/2026 (MEL-250): 1º 05:20–13:57 (517 min), 2º 13:57–22:20 (503), 3º 22:20–05:20 (420); dia produtivo começa 05:20. Lote aberto na virada continua no turno seguinte.
- Tempo de processo = metros ÷ taxa mediana da etapa e da família de bitola (na Trançagem, por máquina e família), vezes um fator `kappa` ajustado no treino. Vulcanização tem ciclo fixo por família.
- Trançagem e Vulcanização rodam em todo turno com a fábrica aberta. As outras etapas só rodam nos turnos em que alguém apontou nelas, com servidores = mín(máquinas, pessoas).
- Refugo e perda entram como rendimento de metros de uma etapa para a seguinte.
- Setup da Trançagem: intervalo mediano entre lotes seguidos na mesma máquina; mesma mangueira {round(st['mesma_mangueira_min'])} min (n = {st['n_mesma']}), troca de mangueira na mesma bitola {round(st['troca_mangueira_min'])} min (n = {st['n_mangueira']}), troca de bitola {round(st['troca_bitola_min'])} min (n = {st['n_bitola']}). Medido só quando o lote seguinte já estava pronto no Tubo. É por apontamento (clique), não pela peça boa: provisório.
- Paradas não entram dia a dia (o Hora-Hora da era GMS não está exportado neste PC). Elas estão dentro da taxa efetiva. No Hora-Hora antigo ({h['periodo'][0]} a {h['periodo'][1]}, {h['janelas']} janelas) o parado soma {round(100 * h['parado_sobre_minutos_geral'])}% dos minutos das janelas registradas; serve só de referência para o cenário de redução de parada.

## Erro fora da amostra (teste), gêmeo com as pessoas que apontaram no turno
{tab('gemeo_obs', 'teste')}
## Erro fora da amostra, gêmeo com equipe típica (mediana por dia da semana e turno)
{tab('gemeo_tipico', 'teste')}
## Comparação 1: "só desloca" (cada OP sai com o atraso mediano, sem fila nem capacidade), teste
{tab('desloca', 'teste')}
## Comparação 2: mediana de metros por dia do treino, teste
{tab('mediana', 'teste')}
## Dentro da amostra (treino), gêmeo com as pessoas que apontaram
{tab('gemeo_obs', 'treino')}
## Parâmetros calibrados
| Etapa | servidores | kappa | ocupação % | rendimento vs etapa anterior | espera mínima (min) |
|---|---|---|---|---|---|
{uso_txt}

Lead time da liberação ao fim da Extração (h), real × gêmeo: mediana {round(ltr.median())} × {round(lts.median())}; p25 {round(ltr.quantile(.25))} × {round(lts.quantile(.25))}; p75 {round(ltr.quantile(.75))} × {round(lts.quantile(.75))}.

## Dias em que a Extração mais errou no teste
| data_ref | real (m) | gêmeo (m) | erro (m) |
|---|---|---|---|
""" + "\n".join(f"| {r.data_ref} | {r.real_m:.0f} | {r.gemeo_m:.0f} | {r.err:+.0f} |" for r in piores.itertuples()) + "\n"
(G.AQUI.parent / "GEMEO_BACKTEST.md").write_text(md, encoding="utf-8")
print(resumo[resumo.periodo == "teste"].pivot(index="etapa", columns="modelo", values="wape").reindex(G.ETAPAS))
print(resumo[resumo.periodo == "teste"].pivot(index="etapa", columns="modelo", values="mape_sem").reindex(G.ETAPAS))
print({k: P[k] for k in ("maquinas", "kappa", "setup_tranc", "tranc_maq_por_pessoa", "tranc_pos")}); print(h)
print("lead", ltr.median(), lts.median(), "ocup", {e: round(usoA[e][0] / max(1, usoA[e][1]), 2) for e in G.ETAPAS})
