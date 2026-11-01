"""Calibra o simulador de headcount x demanda (trancagem -> cabine) -> parametros_simulador.csv.
Regras de tempo: NORMA 27/10/2026 (MEL-250). Turno pela hora do apontamento final; dia produtivo (data_ref) comeca 05:20.
Headcount PROVISORIO = operadores distintos que apontaram a etapa no data_ref-turno (nomes NAO sao gravados).
Se existir escala_real.csv (data_ref,turno,etapa,pessoas) ele sobrescreve o provisorio."""
import math
import pathlib
import numpy as np
import pandas as pd

AQUI = pathlib.Path(__file__).resolve().parent
SRC = AQUI.parents[1] / "Sharepoint Data GMS" / "ficha_producao.csv"
ESCALA = AQUI / "escala_real.csv"
OUT = AQUI / "parametros_simulador.csv"

ETAPAS = ["tranc", "cob", "band", "vulc", "deb", "cab"]
COLS = {"tranc": ("data_hora_final_trancadeira", "quantidade_trancagem", "operador_trancagem"),
        "cob": ("data_hora_final_cobertura", "quantidade_cobertura", "operador_cobertura"),
        "band": ("data_hora_final_bandagem", "quantidade_bandagem", "operador_bandagem"),
        "vulc": ("data_hora_final_vulcanizacao", "quantidade_vulcanizacao", "operador_vulcanizacao"),
        "deb": ("data_hora_final_debandagem", "quantidade_debandagem", "operador_debandagem"),
        "cab": ("data_hora_final_extracao", "quantidade_extracao", "operador_extracao")}
MIN_TURNO = {1: 517, 2: 503, 3: 420}
FAMILIAS = ["3-4", "6", "7-8", "10", "12", "16+", "ND"]
LIMITE_BAIXO = 0.30
# debandagem so passa a ser apontada em 26/02/2026 e a cabine ate ~fev/2026 e parcial: janela completa a partir de 01/03/2026
JANELA_INI = pd.Timestamp("2026-03-01")


def turno_e_dataref(t):
    """T1 05:20-13:56, T2 13:57-22:19, T3 22:20-05:19. data_ref = dia produtivo (comeca 05:20)."""
    mm = t.dt.hour * 60 + t.dt.minute
    turno = np.where((mm >= 320) & (mm <= 836), 1, np.where((mm >= 837) & (mm <= 1339), 2, 3))
    dref = (t - pd.Timedelta(hours=5, minutes=20)).dt.normalize()
    return pd.Series(turno, index=t.index), dref


def familia(b):
    if pd.isna(b):
        return "ND"
    b = float(b)
    if b <= 5.5:
        return "3-4"
    if b < 6.5:
        return "6"
    if b < 9:
        return "7-8"
    if b < 11:
        return "10"
    if b < 14:
        return "12"
    return "16+"


def norm_trancadeira(s):
    if pd.isna(s):
        return None
    x = str(s).upper().replace("-", "").replace(".", "").replace(" ", "")
    if x in ("0", "", "TE0"):
        return None
    if x == "T004":
        x = "TO04"
    return x


def carregar():
    d = pd.read_csv(SRC, encoding="utf-8-sig", low_memory=False)
    d.columns = [c.encode("latin1").decode("utf8") if "Ã" in c else c for c in d.columns]
    d = d[d["status_processo"].astype(str).str.strip().str.lower() != "cancelado"].copy()
    d["fam"] = d["Bitola"].map(familia)
    col_tr = [c for c in d.columns if c.startswith("Tran") and c.endswith("adeira") and "Inicio" not in c][0]
    d["tr_norm"] = d[col_tr].map(norm_trancadeira)
    return d


def celulas(d):
    """Por etapa: linhas (t, q, op, fam, turno, data_ref) validas."""
    out = {}
    for e in ETAPAS:
        tc, qc, oc = COLS[e]
        x = pd.DataFrame({"t": pd.to_datetime(d[tc], errors="coerce", format="mixed"),
                          "q": pd.to_numeric(d[qc], errors="coerce"),
                          "op": d[oc], "fam": d["fam"], "tr": d["tr_norm"]})
        x = x.dropna(subset=["t", "q"])
        x = x[x.q > 0].copy()
        x["turno"], x["dref"] = turno_e_dataref(x.t)
        out[e] = x
    return out


def aplicar_escala(pess):
    """pess[e]: DataFrame (dref,turno,pessoas,m,m_op,...). Sobrescreve com escala_real.csv se existir."""
    if not ESCALA.exists():
        return False
    esc = pd.read_csv(ESCALA)
    esc["turno"] = esc["turno"].astype(str).str.extract(r"(\d)")[0].astype(int)
    esc["data_ref"] = pd.to_datetime(esc["data_ref"])
    for e in ETAPAS:
        s = esc[esc.etapa == e].set_index(["data_ref", "turno"]).pessoas
        if s.empty:
            continue
        idx = pd.MultiIndex.from_frame(pess[e][["dref", "turno"]])
        novo = s.reindex(idx).values
        pess[e]["pessoas"] = np.where(np.isnan(novo), pess[e]["pessoas"], novo)
    return True


def painel(cel):
    """Painel por etapa: linha = (dref, turno) com m (todas as fichas), m_op (fichas com operador), pessoas, e metros por familia."""
    pn = {}
    for e, x in cel.items():
        g = x.groupby(["dref", "turno"])
        p = g.agg(m=("q", "sum")).join(x[x.op.notna()].groupby(["dref", "turno"]).agg(
            m_op=("q", "sum"), pessoas=("op", "nunique")))
        p["m_op"] = p["m_op"].fillna(0)
        p["pessoas"] = p["pessoas"].fillna(0)
        f = x.pivot_table(index=["dref", "turno"], columns="fam", values="q", aggfunc="sum", fill_value=0)
        for fa in FAMILIAS:
            p["f_" + fa] = f[fa] if fa in f else 0.0
            p["f_" + fa] = p["f_" + fa].fillna(0)
        pn[e] = p.reset_index()
    return pn


def dias_atipicos(cel):
    """Retorna (todos_os_dias, excluidos{dia:motivo}, baixo_por_etapa{e:set})."""
    tot = {e: x.groupby("dref").q.sum() for e, x in cel.items()}
    ini = min(s.index.min() for s in tot.values())
    fim = max(s.index.max() for s in tot.values())
    dias = pd.date_range(ini, fim, freq="D")
    med = {e: tot[e][tot[e] > 0].median() for e in ETAPAS}
    baixo = {e: set(tot[e][tot[e] < LIMITE_BAIXO * med[e]].index) for e in ETAPAS}
    exc = {}
    for dia in dias[dias < JANELA_INI]:
        exc[dia] = "antes da janela completa (debandagem/cabine sem apontamento completo)"
    # parada: corridas >= 5 dias corridos com tranc+cab < 30% da mediana somada
    soma = (tot["tranc"].reindex(dias, fill_value=0) + tot["cab"].reindex(dias, fill_value=0))
    lim = LIMITE_BAIXO * (med["tranc"] + med["cab"])
    low = ((soma < lim) & (dias >= JANELA_INI)).values
    i = 0
    while i < len(dias):
        if low[i]:
            j = i
            while j + 1 < len(dias) and low[j + 1]:
                j += 1
            if j - i + 1 >= 5:
                for k in range(i, j + 1):
                    exc[dias[k]] = f"parada ({dias[i].date()} a {dias[j].date()}, {j - i + 1} dias)"
            i = j + 1
        else:
            i += 1
    for dia in dias:
        if dia in exc:
            continue
        t = tot["tranc"].get(dia, 0)
        c = tot["cab"].get(dia, 0)
        if t == 0 and c == 0:
            exc[dia] = "sem producao (folga/fim de semana)"
        elif t < LIMITE_BAIXO * med["tranc"] or c < LIMITE_BAIXO * med["cab"]:
            exc[dia] = "volume < 30% da mediana (tranc ou cabine)"
        elif dia.weekday() == 6 and t < 0.5 * med["tranc"]:
            exc[dia] = "domingo de baixo volume"
    return dias, exc, baixo


def quantis(v):
    v = np.asarray(v, float)
    return {"mediana": np.median(v), "p25": np.percentile(v, 25), "p75": np.percentile(v, 75)}


def parametros(pn, dias_ok, baixo):
    """Calibra com os dias em dias_ok (set de Timestamps ja sem atipicos). Retorna dict de parametros."""
    P = {"prod": {}, "prod_etapa": {}, "prod_fam": {}, "teto_turno": {}, "teto_dia": {}, "n": {}}
    for e in ETAPAS:
        p = pn[e]
        p = p[p.dref.isin(dias_ok) & ~p.dref.isin(baixo[e]) & (p.pessoas > 0) & (p.m_op > 0)].copy()
        p["min"] = p.turno.map(MIN_TURNO)
        p["prod"] = p.m_op / (p.pessoas * p["min"])
        P["prod_etapa"][e] = float(p["prod"].median()) if len(p) else np.nan
        for t in (1, 2, 3):
            s = p[p.turno == t]["prod"]
            P["prod"][(e, t)] = float(s.median()) if len(s) >= 3 else P["prod_etapa"][e]
            P["n"][(e, t)] = len(s)
        for fa in FAMILIAS:
            s = p[(p["f_" + fa] / p.m > 0.6)]["prod"]  # celulas dominadas pela familia
            P["prod_fam"][(e, fa)] = float(s.median()) if len(s) >= 5 else np.nan
            P["n"][(e, fa)] = len(s)
        pe = pn[e][pn[e].dref.isin(dias_ok)]
        ts = pe[pe.pessoas > 0].m
        td = pe.groupby("dref").m.sum()
        P["teto_turno"][e] = float(np.percentile(ts, 95)) if len(ts) else np.nan
        P["teto_dia"][e] = float(np.percentile(td, 95)) if len(td) else np.nan
    return P


def pessoas_necessarias(demanda_m, etapa, turno, params):
    """pessoas = ceil(demanda_turno / (prod_mediana * k * minutos_turno)); demanda ja por turno; params = dict de parametros()."""
    if demanda_m <= 0:
        return 0
    p = params["prod"][(etapa, turno)]
    k = params.get("k", 1.0)
    return int(math.ceil(demanda_m / (p * k * MIN_TURNO[turno]) - 1e-9))


def main():
    d = carregar()
    cel = celulas(d)
    pn = painel(cel)
    prov = not aplicar_escala(pn)
    dias, exc, baixo = dias_atipicos(cel)
    ok = set(dias) - set(exc)
    ok = {x for x in ok if x in set(pn["tranc"].dref)}
    P = parametros(pn, ok, baixo)
    obs_h = "headcount provisorio" if prov else "headcount escala_real.csv"
    L = []

    def add(tipo, et, fam, turno, met, val, n, obs):
        L.append((tipo, et, fam, turno, met, round(float(val), 6) if pd.notna(val) else "", n, obs))

    for e in ETAPAS:
        p = pn[e]
        p = p[p.dref.isin(ok) & ~p.dref.isin(baixo[e]) & (p.pessoas > 0) & (p.m_op > 0)].copy()
        p["prod"] = p.m_op / (p.pessoas * p.turno.map(MIN_TURNO))
        for nome, sub, tur in [("todos", p, "todos")] + [(str(t), p[p.turno == t], t) for t in (1, 2, 3)]:
            if len(sub):
                q = quantis(sub["prod"])
                for k, v in q.items():
                    add("produtividade", e, "todas", tur, k + "_m_pessoa_min", v, len(sub), "provisorio" if prov else "escala real")
        for fa in FAMILIAS:
            sub = p[p["f_" + fa] / p.m > 0.6]
            if len(sub) >= 5:
                q = quantis(sub["prod"])
                for k, v in q.items():
                    add("produtividade", e, fa, "todos", k + "_m_pessoa_min", v, len(sub),
                        "celulas com >60% dos metros da familia; " + ("provisorio" if prov else "escala real"))
            else:
                add("produtividade", e, fa, "todos", "mediana_m_pessoa_min", np.nan, len(sub), "n<5: usar mediana da etapa")
        add("teto", e, "todas", "turno", "p95_metros_data_ref_turno", P["teto_turno"][e], len(pn[e]), "empirico")
        add("teto", e, "todas", "dia", "p95_metros_data_ref", P["teto_dia"][e], len(ok), "empirico")
    # trancadeiras distintas por data_ref
    tr = cel["tranc"]
    tr = tr[tr.dref.isin(ok) & tr.tr.notna()].groupby("dref").tr.nunique()
    add("teto", "tranc", "todas", "dia", "p95_trancadeiras_ativas_dia", np.percentile(tr, 95), len(tr), "empirico")
    add("teto", "tranc", "todas", "dia", "max_trancadeiras_ativas_dia", tr.max(), len(tr), "empirico")
    # lead time
    ts = {e: pd.to_datetime(d[COLS[e][0]], errors="coerce", format="mixed") for e in ETAPAS}
    for a, b in zip(ETAPAS[:-1], ETAPAS[1:]):
        h = (ts[b] - ts[a]).dt.total_seconds() / 3600
        h = h[(h > 0) & (h < 24 * 30)]
        add("lead_time", f"{a}->{b}", "todas", "todos", "mediana_horas", h.median(), len(h), "mediana entre apontamentos finais consecutivos")
        add("lead_time", f"{a}->{b}", "todas", "todos", "p75_horas", h.quantile(.75), len(h), "")
    for t, m in MIN_TURNO.items():
        add("turno", "todas", "todas", t, "minutos", m, 0, "NORMA 27/10/2026 MEL-250")
    pd.DataFrame(L, columns=["tipo", "etapa", "familia", "turno", "metrica", "valor", "n", "obs"]).to_csv(
        OUT, index=False, encoding="utf-8-sig")
    print("gravado", OUT, len(L), "linhas; dias:", len(dias), "excluidos:", len(exc), "usados:", len(ok))
    for e in ETAPAS:
        print(e, {t: round(P["prod"][(e, t)], 3) for t in (1, 2, 3)}, "teto_turno", round(P["teto_turno"][e]), "teto_dia", round(P["teto_dia"][e]))


if __name__ == "__main__":
    main()
