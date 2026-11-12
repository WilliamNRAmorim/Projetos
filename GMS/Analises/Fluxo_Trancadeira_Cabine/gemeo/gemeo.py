"""Gemeo digital da celula GMS (missao P2, 12/11/2026).

Simulacao de eventos discretos, lote (OP) a lote, pelas 8 etapas:
Mandril -> Tubo -> Trancagem -> Cobertura -> Bandagem -> Vulcanizacao -> Debandagem -> Extracao/Teste.

Regras de negocio usadas (NAO mudar aqui; fonte = NORMA de 27/10/2026, MEL-250):
  turnos   T1 05:20-13:57 (517 min) | T2 13:57-22:20 (503 min) | T3 22:20-05:20 (420 min)
  data_ref dia produtivo comeca 05:20; antes disso pertence ao dia anterior
Tudo o que e turno/dia produtivo passa por `turno_de()` e `SLOT_INI/SLOT_MIN` (um unico lugar).

Uso:  python -X utf8 gemeo.py calibrar | backtest | whatif | aps | tudo
"""
import sys, json, heapq, math, pathlib, itertools
import numpy as np, pandas as pd

AQUI = pathlib.Path(__file__).resolve().parent
GMS = AQUI.parents[2]
FICHA = GMS / "IA" / "dados" / "ficha_producao.csv"
HH_DIR = GMS / "Analises" / "Historico_HoraHora"
SAIDA = AQUI / "saida"; SAIDA.mkdir(exist_ok=True)
PARAMS = AQUI / "gemeo_parametros.json"

# ---------------------------------------------------------------- turno (NORMA MEL-250)
SLOT_INI = (0, 517, 1020)          # minutos depois das 05:20
SLOT_MIN = (517, 503, 420)         # soma 1440
EPOCA = pd.Timestamp("2025-11-01 05:20")   # minuto 0 = inicio do 1o turno de 01/11/2025

def tmin(ts):
    """Timestamp -> minutos desde EPOCA (float, NaN se vazio)."""
    return (ts - EPOCA).total_seconds() / 60.0

def turno_de(m):
    """minuto desde EPOCA -> (dia_idx, turno 1..3). dia_idx 0 = data_ref 2025-11-01."""
    d, off = divmod(int(math.floor(m)), 1440)
    return d, (1 if off < 517 else 2 if off < 1020 else 3)

def slot_lim(d, t):
    a = d * 1440 + SLOT_INI[t - 1]
    return a, a + SLOT_MIN[t - 1]

def data_ref(d):
    return (EPOCA.normalize() + pd.Timedelta(days=int(d))).strftime("%Y-%m-%d")

# ---------------------------------------------------------------- etapas
ETAPAS = ["mandril", "tubo", "tranc", "cob", "band", "vulc", "deb", "ext"]
NOME = {"mandril": "Mandril", "tubo": "Tubo", "tranc": "Trançagem", "cob": "Cobertura", "band": "Bandagem",
        "vulc": "Vulcanização", "deb": "Debandagem", "ext": "Extração/Teste"}
COL = {"mandril": ("data_hora_inicio_mandril", "data_hora_final_mandril", "quantidade_mandril", "operador_mandril"),
       "tubo": ("data_hora_inicio_tubo", "data_hora_final_tubo", "quantidade_tubo", "operador_tubo"),
       "tranc": ("data_hora_inicio_trancadeira", "data_hora_final_trancadeira", "quantidade_trancagem", "operador_trancagem"),
       "cob": ("data_hora_inicio_cobertura", "data_hora_final_cobertura", "quantidade_cobertura", "operador_cobertura"),
       "band": ("data_hora_inicio_bandagem", "data_hora_final_bandagem", "quantidade_bandagem", "operador_bandagem"),
       "vulc": ("data_hora_inicio_vulcanizacao", "data_hora_final_vulcanizacao", "quantidade_vulcanizacao", "operador_vulcanizacao"),
       "deb": ("data_hora_inicio_debandagem", "data_hora_final_debandagem", "quantidade_debandagem", "operador_debandagem"),
       "ext": ("data_hora_inicio_extracao", "data_hora_final_extracao", "quantidade_extracao", "operador_extracao")}
RITMO_MAQUINA = {"tranc", "vulc"}   # rodam em todo turno com a fabrica aberta; as demais dependem de gente na etapa
TEMPO_FIXO = {"vulc"}               # ciclo de autoclave nao depende dos metros
MAQ_FIXO = {"mandril": 2, "tranc": 11}   # termofusao+vibracional; fx_CelulasTrancagem. As demais: p95 de lotes simultaneos
TRANC = ["TH01", "TH02", "TH03", "TH04", "TH05", "TH06", "TH07", "TM01", "TM04", "TO04", "SPIRAL"]

def familia(b):
    try: b = int(b)
    except Exception: return "ND"
    return "3-4" if b <= 4 else "6" if b <= 6 else "7-8" if b <= 8 else "10" if b <= 10 else "12" if b <= 12 else "16+"

def _num(s):
    s = s.astype(str).str.strip()
    mil = s.str.match(r"^\d{1,3}(,\d{3})+$")
    v = pd.to_numeric(s.where(~mil, s.str.replace(",", "")).str.replace(",", "."), errors="coerce")
    return v.where((v > 0) & (v < 6000))      # metros de uma OP; fora disso e erro de digitacao

def _maq(s):
    s = s.astype(str).str.upper().str.replace(r"[^A-Z0-9]", "", regex=True)
    s = s.replace({"T004": "TO04", "SPIRAL": "SPIRAL"})
    return s.where(s.isin(TRANC))

def carregar():
    d = pd.read_csv(FICHA, encoding="utf-8-sig", low_memory=False)
    d.columns = [c.encode("latin1").decode("utf8") if "Ã" in c else c for c in d.columns]
    d = d[d.status_processo != "Cancelado"].copy()
    L = pd.DataFrame({"id": d.ID.values, "mang": d.Mangueira.astype(str).str.strip().values,
                      "fam": d.Bitola.map(familia).values, "maq": _maq(d["Trançadeira"]).values,
                      "fin": (d.status_processo == "Finalizado").values})
    for e, (ci, cf, cq, co) in COL.items():
        ti = pd.to_datetime(d[ci], errors="coerce", format="mixed"); tf = pd.to_datetime(d[cf], errors="coerce", format="mixed")
        L[e + "_i"] = ((ti - EPOCA).dt.total_seconds() / 60).values
        L[e + "_f"] = ((tf - EPOCA).dt.total_seconds() / 60).values
        L[e + "_q"] = _num(d[cq]).values
        L[e + "_o"] = d[co].astype(str).str.strip().str.upper().replace({"NAN": None, "": None, "0": None}).values
    return L.reset_index(drop=True)

# ---------------------------------------------------------------- calendario real (slots)
def slots_reais(L):
    """pessoas[e][(d,t)] = operadores distintos que fecharam lote da etapa no slot (PROVISORIO: quem apontou).
    aberta = slots com qualquer apontamento final em qualquer etapa."""
    pessoas = {e: {} for e in ETAPAS}; aberta = set()
    for e in ETAPAS:
        ok = L[e + "_f"].notna()
        for f, o in zip(L.loc[ok, e + "_f"], L.loc[ok, e + "_o"]):
            k = turno_de(f); aberta.add(k)
            pessoas[e].setdefault(k, set())
            if o: pessoas[e][k].add(o)
        for i in L.loc[L[e + "_i"].notna(), e + "_i"]:            # inicio apontado tambem prova gente na etapa
            k = turno_de(i); aberta.add(k); pessoas[e].setdefault(k, set())
        pessoas[e] = {k: max(1, len(v)) for k, v in pessoas[e].items()}
    return pessoas, aberta

def trabalho(i, f, abertos):
    """minutos de trabalho entre i e f contando so os slots abertos (set de (d,t))."""
    if not (f > i): return 0.0
    tot = 0.0; d, t = turno_de(i)
    while True:
        a, b = slot_lim(d, t)
        if a >= f: break
        if (d, t) in abertos: tot += max(0.0, min(b, f) - max(a, i))
        t += 1
        if t == 4: t, d = 1, d + 1
    return tot

# ---------------------------------------------------------------- motor: uma etapa, c servidores por slot
def rodar_etapa(jobs, slots, por_maquina=False, setup=None, pos=None):
    """jobs: dicts {id, arr, work, maq, mang, pri}; slots: lista ordenada (t0, t1, c).
    Fila por `pri` (padrao = chegada). Lote e interrompido no fim do slot e retoma no proximo.
    por_maquina: o lote so roda na sua maquina; pos[maq] = lotes simultaneos que a maquina aceita (padrao 1). setup(maq, mang_anterior, job) -> minutos extras.
    Devolve ({id: (inicio, fim)}, uso) com uso = (min ocupados, min disponiveis)."""
    pend = sorted(jobs, key=lambda j: j["arr"]); pi = 0; seq = itertools.count()
    fila = []; rod = []; fim = {}; ini = {}; ult = {}; ocup = disp = 0.0
    for t0, t1, c in slots:
        if c <= 0: continue
        disp += (t1 - t0) * c
        while len(rod) > c:                               # menos servidores que no slot anterior: devolve a fila
            j, r = rod.pop(); j["_rem"] = r; heapq.heappush(fila, (j["pri"], next(seq), j))
        t = t0
        while True:
            while pi < len(pend) and pend[pi]["arr"] <= t:
                j = pend[pi]; pi += 1; heapq.heappush(fila, (j["pri"], next(seq), j))
            if len(rod) < c and fila:
                volta = []; ocupadas = {}
                if por_maquina:
                    for r in rod: ocupadas[r[0]["maq"]] = ocupadas.get(r[0]["maq"], 0) + 1
                while fila and len(rod) < c:
                    it = heapq.heappop(fila); j = it[2]
                    if por_maquina and ocupadas.get(j["maq"], 0) >= (pos or {}).get(j["maq"], 1): volta.append(it); continue
                    w = j.pop("_rem", None)
                    if w is None:
                        w = j["work"]
                        if setup: w += setup(j["maq"], ult.get(j["maq"]), j)
                        ini[j["id"]] = t
                    ult[j["maq"]] = (j["mang"], j.get("fam"))
                    rod.append([j, w])
                    if por_maquina: ocupadas[j["maq"]] = ocupadas.get(j["maq"], 0) + 1
                for it in volta: heapq.heappush(fila, it)
            nxt = t1
            if rod: nxt = min(nxt, t + min(r[1] for r in rod))
            if pi < len(pend) and len(rod) < c: nxt = min(nxt, pend[pi]["arr"])
            dt = max(0.0, nxt - t); ocup += dt * len(rod)
            for r in rod: r[1] -= dt
            t = nxt
            for r in [r for r in rod if r[1] <= 1e-6]: fim[r[0]["id"]] = t
            rod = [r for r in rod if r[1] > 1e-6]
            if t >= t1: break
    return {k: (ini[k], v) for k, v in fim.items()}, (ocup, disp)

# ---------------------------------------------------------------- calibracao
def _mediana_fam(df, col, minimo=8):
    g = df.groupby("fam")[col].agg(["median", "size"])
    return {"*": float(df[col].median()), **{k: float(r["median"]) for k, r in g.iterrows() if r["size"] >= minimo}}

def calibrar(L, pessoas, aberta, ate_min):
    """Parametros medidos so com lotes ate `ate_min` (fim do treino)."""
    P = {"taxa": {}, "ciclo_fixo": {}, "maquinas": {}, "transf": {}, "rend": {}, "kappa": {e: 1.0 for e in ETAPAS}}
    for n, e in enumerate(ETAPAS):
        ab = aberta if e in RITMO_MAQUINA else set(pessoas[e])
        x = L[[e + "_i", e + "_f", e + "_q", "fam", "maq"]].dropna(subset=[e + "_i", e + "_f"]).copy()
        x = x[(x[e + "_f"] <= ate_min) & (x[e + "_f"] - x[e + "_i"] > 1.5) & (x[e + "_f"] - x[e + "_i"] < 20 * 1440)]
        x["w"] = [trabalho(i, f, ab) for i, f in zip(x[e + "_i"], x[e + "_f"])]
        x = x[x.w > 1.5]
        if e in TEMPO_FIXO:
            P["ciclo_fixo"][e] = _mediana_fam(x, "w")
        else:
            x = x[x[e + "_q"].notna()].copy(); x["r"] = x[e + "_q"] / x.w
            P["taxa"][e] = _mediana_fam(x, "r")
            if e == "tranc":
                g = x.groupby("maq").r.agg(["median", "size"])
                P["taxa_maq"] = {k: float(r["median"]) for k, r in g.iterrows() if r["size"] >= 8}
                g = x.groupby(["maq", "fam"]).r.agg(["median", "size"])
                P["taxa_maq_fam"] = {f"{k[0]}|{k[1]}": float(r["median"]) for k, r in g.iterrows() if r["size"] >= 8}
        # servidores: p95 de lotes simultaneos em processo (medido no inicio de cada lote)
        ii = np.sort(x[e + "_i"].values); ff = np.sort(x[e + "_f"].values)
        conc = np.searchsorted(ii, ii, side="right") - np.searchsorted(ff, ii, side="right")
        P["maquinas"][e] = int(MAQ_FIXO.get(e, max(1, round(float(np.percentile(conc, 95))) if len(conc) else 1)))
        if e == "tranc":   # posicoes por trancadeira: p90 de lotes abertos ao mesmo tempo na mesma maquina
            P["tranc_pos"] = {}
            for m, g in x.groupby("maq"):
                ii = np.sort(g.tranc_i.values); ff = np.sort(g.tranc_f.values)
                cc = np.searchsorted(ii, ii, side="right") - np.searchsorted(ff, ii, side="right")
                P["tranc_pos"][m] = int(max(1, round(float(np.percentile(cc, 90)))))
        if n:   # transferencia minima e rendimento em relacao a etapa anterior
            a = ETAPAS[n - 1]
            ok = L[[a + "_f", e + "_i", e + "_f"]].notna().all(axis=1) & (L[e + "_f"] <= ate_min)
            esp = (L.loc[ok, e + "_i"] - L.loc[ok, a + "_f"]); esp = esp[(esp >= 0) & (esp < 10 * 1440)]
            P["transf"][e] = float(np.percentile(esp, 10)) if len(esp) else 0.0
            ok = L[[a + "_q", e + "_q"]].notna().all(axis=1) & (L[e + "_f"] <= ate_min)
            rz = L.loc[ok, e + "_q"] / L.loc[ok, a + "_q"]; ok2 = rz.between(0.5, 1.2)
            P["rend"][e] = float(L.loc[ok & ok2, e + "_q"].sum() / L.loc[ok & ok2, a + "_q"].sum())
        else:
            P["transf"][e] = 0.0; P["rend"][e] = 1.0
    # setup da trancagem (PROVISORIO, por apontamento): intervalo, em minutos de fabrica aberta, entre o fim de um lote e
    # o inicio do seguinte na mesma maquina, SO quando o seguinte ja estava pronto no Tubo (a maquina era a restricao).
    x = L.dropna(subset=["tranc_i", "tranc_f", "maq"]).sort_values("tranc_i")
    x = x[x.tranc_f <= ate_min]; gp = {"mesma": [], "mang": [], "bitola": []}
    for _, g in x.groupby("maq"):
        g = g.reset_index(drop=True)
        for k in range(1, len(g)):
            a_, b_ = g.tranc_f[k - 1], g.tranc_i[k]
            if 0 <= b_ - a_ < 3 * 1440 and g.tubo_f[k] <= a_:
                tipo = "mesma" if g.mang[k] == g.mang[k - 1] else "mang" if g.fam[k] == g.fam[k - 1] else "bitola"
                gp[tipo].append(trabalho(a_, b_, aberta))
    md = lambda v: float(np.median(v)) if v else 0.0
    P["setup_tranc"] = {"mesma_mangueira_min": md(gp["mesma"]), "troca_mangueira_min": max(md(gp["mang"]), md(gp["mesma"])),
                        "troca_bitola_min": max(md(gp["bitola"]), md(gp["mang"]), md(gp["mesma"])),
                        "n_mesma": len(gp["mesma"]), "n_mangueira": len(gp["mang"]), "n_bitola": len(gp["bitola"])}
    # maquinas por pessoa na trancagem (para o what-if): maquinas rodando no slot / operadores que apontaram
    r = []
    for (d, t), p in pessoas["tranc"].items():
        a, b = slot_lim(d, t)
        if b <= ate_min:
            n = int(((x.tranc_i < b) & (x.tranc_f > a)).sum())
            if n: r.append(min(n, 11) / p)
    P["tranc_maq_por_pessoa"] = float(np.median(r)) if r else 2.0
    return P

def paradas_hh():
    """Disponibilidade historica por celula a partir do Hora-Hora pre-GMS (08/2023 a 09/2025; Espiral ate 07/2026).
    Parado e limitado aos minutos da janela (mesma regra da fHoraCheia). So leitura, nao altera a regra."""
    man = json.loads((HH_DIR / "hh_manifest.json").read_text(encoding="utf-8")); rows = []
    for a in man["arquivos"]:
        s = (HH_DIR / "dados" / a["arquivo"]).read_text(encoding="utf-8")
        rows += json.loads(s[s.index("["):s.rindex("]") + 1])
    h = pd.DataFrame([r[:14] for r in rows], columns=["tit", "data", "turno", "cel", "hora", "mang", "meta", "meta_ac", "real", "real_ac", "dif", "parado", "motivo", "cat"])
    def jan(s):
        try:
            a, b = [int(p[:2]) * 60 + int(p[3:5]) for p in str(s).split(" - ")]; return (b - a) % 1440 or 60
        except Exception: return 60
    h["min"] = h.hora.map(jan); h["parado"] = pd.to_numeric(h.parado, errors="coerce").fillna(0).clip(lower=0)
    h["parado"] = h[["parado", "min"]].min(axis=1)
    h["cel"] = h.cel.astype(str).str.upper().str.replace(r"[^A-Z0-9]", "", regex=True)
    h = h[h.cel.isin(TRANC)]
    g = h.groupby("cel").agg(janelas=("min", "size"), min=("min", "sum"), parado=("parado", "sum"), real=("real", "sum"), meta=("meta", "sum"))
    mot = (h.groupby("motivo").parado.sum() / h.parado.sum()).sort_values(ascending=False).head(10)
    return {"periodo": [str(h.data.dropna().min()), str(h.data.dropna().max())], "janelas": int(len(h)),
            "parado_sobre_minutos": {k: round(float(r.parado / r["min"]), 3) for k, r in g.iterrows()},
            "real_sobre_meta": {k: round(float(r.real / r.meta), 3) for k, r in g.iterrows() if r.meta},
            "parado_sobre_minutos_geral": round(float(g.parado.sum() / g["min"].sum()), 3),
            "parado_por_motivo": {str(k): round(float(v), 3) for k, v in mot.items()}}

# ---------------------------------------------------------------- simulacao da cadeia
def taxa_tranc(P, maq, fam):
    return P["taxa_maq_fam"].get(f"{maq}|{fam}") or P["taxa_maq"].get(maq) or P["taxa"]["tranc"].get(fam) or P["taxa"]["tranc"]["*"]

def tempo(P, e, q, fam, maq=None, fator_tranc=1.0):
    k = P["kappa"][e]
    if e in TEMPO_FIXO: return k * (P["ciclo_fixo"][e].get(fam) or P["ciclo_fixo"][e]["*"])
    if e == "tranc": return k * q / (taxa_tranc(P, maq, fam) * fator_tranc)
    return k * q / (P["taxa"][e].get(fam) or P["taxa"][e]["*"])

def simular(lotes, P, cal, ate=None, pri=None, usar_setup=True, fator_tranc=1.0, so_ate_etapa=None):
    """lotes: DataFrame id, arr (min), q0, fam, maq, mang. cal[e] = lista (t0,t1,c).
    Devolve (res: DataFrame com e_i, e_f, e_q por etapa; uso[e] = (ocupado, disponivel))."""
    res = lotes[["id"]].copy(); arr = dict(zip(lotes.id, lotes.arr)); q = dict(zip(lotes.id, lotes.q0)); uso = {}
    st = P["setup_tranc"]
    def setup(maq, ant, j):
        if ant is None or ant[0] == j["mang"]: return st["mesma_mangueira_min"]
        return st["troca_mangueira_min"] if ant[1] == j["fam"] else st["troca_bitola_min"]
    info = {r.id: r for r in lotes.itertuples()}
    for e in ETAPAS:
        jobs = []
        for i, a in arr.items():
            r = info[i]; q[i] = q[i] * P["rend"][e]
            jobs.append({"id": i, "arr": a + P["transf"][e], "work": tempo(P, e, q[i], r.fam, r.maq, fator_tranc),
                         "maq": r.maq if e == "tranc" else None, "mang": r.mang, "fam": r.fam,
                         "pri": (pri.get(i, a) if (pri and e == "tranc") else a)})   # OP fora de `pri` segue por chegada
        out, uso[e] = rodar_etapa(jobs, cal[e], por_maquina=(e == "tranc"), setup=setup if (e == "tranc" and usar_setup) else None,
                                  pos=P.get("tranc_pos") if e == "tranc" else None)
        res[e + "_i"] = res.id.map(lambda i: out.get(i, (np.nan, np.nan))[0]); res[e + "_f"] = res.id.map(lambda i: out.get(i, (np.nan, np.nan))[1])
        res[e + "_q"] = res.id.map(q)
        arr = {i: v[1] for i, v in out.items()}
        if e == so_ate_etapa: break
    return res, uso

def cal_real(P, pessoas, aberta, tipico=None):
    """Calendario de servidores por etapa. tipico=None -> pessoas observadas no slot; senao dict (e, dia_semana, t) -> pessoas."""
    cal = {}; slots = sorted(aberta)
    for e in ETAPAS:
        M = P["maquinas"][e]; lst = []
        for (d, t) in slots:
            a, b = slot_lim(d, t)
            if e == "tranc": c = sum(P["tranc_pos"].values())
            elif e in RITMO_MAQUINA: c = M
            elif tipico is None: c = min(M, pessoas[e].get((d, t), 0))
            else: c = min(M, int(round(tipico.get((e, (d + 5) % 7, t), 0))))   # 01/11/2025 = sabado (5)
            lst.append((a, b, c))
        cal[e] = lst
    return cal

def sem_registro(L, e):
    """OPs finalizadas sem data de fim ou sem metros na etapa: o real nao tem como contar, entao o simulado tambem nao conta."""
    return set(L.loc[L.fin & (L[e + "_f"].isna() | L[e + "_q"].isna()), "id"])

def serie_diaria(df, e, fora=None):
    x = df[[e + "_f", e + "_q"]].dropna() if not fora else df.loc[~df.id.isin(fora), [e + "_f", e + "_q"]].dropna()
    return x.groupby(x[e + "_f"].map(lambda m: turno_de(m)[0]))[e + "_q"].sum()

def lotes_reais(L):
    arr = L.mandril_i.fillna(L.mandril_f).fillna(L.tubo_i).fillna(L.tubo_f).fillna(L.tranc_i)
    q0 = L.mandril_q.fillna(L.tubo_q).fillna(L.tranc_q).fillna(L.cob_q)
    x = pd.DataFrame({"id": L.id, "arr": arr, "q0": q0, "fam": L.fam, "maq": L.maq.fillna("TH07"), "mang": L.mang})
    return x.dropna(subset=["arr", "q0"]).reset_index(drop=True)

# ---------------------------------------------------------------- metricas
def metricas(real, sim, dias):
    r = real.reindex(dias).fillna(0.0); s = sim.reindex(dias).fillna(0.0); ok = r > 0
    if ok.sum() == 0: return {}
    ape = ((s[ok] - r[ok]).abs() / r[ok])
    sem = pd.Series(dias).map(lambda d: (d + 5) // 7).values       # semana comecando na segunda
    rs = r.groupby(sem).sum(); ss = s.groupby(sem).sum(); oks = rs > 0
    return {"dias": int(ok.sum()), "mape": round(float(ape.mean() * 100), 1), "wape": round(float((s - r).abs().sum() / r.sum() * 100), 1),
            "vies": round(float((s.sum() - r.sum()) / r.sum() * 100), 1),
            "mape_sem": round(float(((ss[oks] - rs[oks]).abs() / rs[oks]).mean() * 100), 1),
            "ate15": round(float((ape <= 0.15).mean() * 100))}

def dia_idx(s): return int((pd.Timestamp(s) - EPOCA.normalize()).days)

D_INI, D_TREINO, D_FIM = dia_idx("2026-03-01"), dia_idx("2026-08-12"), dia_idx("2026-10-05")
PARADA_JUL = (dia_idx("2026-07-03"), dia_idx("2026-07-27"))

def dias_validos(L):
    """Mesmo criterio do backtest antigo: desde 01/03/2026, fora a parada de julho e dias com volume < 30% da mediana."""
    R = {e: serie_diaria(L, e) for e in ETAPAS}
    dias = [d for d in range(D_INI, D_FIM + 1) if not (PARADA_JUL[0] <= d <= PARADA_JUL[1])]
    mt, mc = R["tranc"].reindex(dias).dropna().median(), R["ext"].reindex(dias).dropna().median()
    dias = [d for d in dias if R["tranc"].get(d, 0) >= 0.3 * mt and R["ext"].get(d, 0) >= 0.3 * mc]
    return R, dias

def salvar_params(P):
    PARAMS.write_text(json.dumps(P, ensure_ascii=False, indent=1), encoding="utf-8")

def ler_params():
    return json.loads(PARAMS.read_text(encoding="utf-8"))
