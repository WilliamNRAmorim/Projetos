# -*- coding: utf-8 -*-
"""MEL-266, passo 2: recalcula o OEE2 da Trançagem direto da lista Hora-Hora (CSV), com as mesmas regras e o mesmo
grão de hora cheia das medidas de GMS/PowerBI/modelo/oee2.tmdl.md. É a referência para o William conferir o BI
depois de aplicar o modelo (critério: ±0,5 ponto, mesmo período e mesmo filtro).

Uso (rodar com -I, só pandas):
    python -I conferir_oee2.py                      # 04/09 a 06/11: total, máquina, turno BI; grava o CSV de referência
    python -I conferir_oee2.py --explica 2026-10-20 TH07 "2º Turno"   # um dia x turno x máquina, linha a linha

O que ele faz (nada é gravado fora do CSV de referência):
 1. Lê Dados_Brutos/Hora-Hora_2026-11-06.csv e Dados_Brutos/TiposErros_2026-11-06.csv (pasta ignorada pelo git).
 2. Fatia cada janela da lista em horas cheias, como a tabela calculada fHoraCheia (fHoraCheia.tmdl.md): dia produtivo
    05:00 a 05:00 (Data BI), Turno BI 05-14 / 14-22 / 22-05, Fração, Minutos, Meta Cheia (sem desconto de refeição),
    Real e Parado (capado na fatia).
 3. Aplica a regra da seção B do PLANO_OEE2.md: pausa fixa de 45 min por Célula x Data BI x Turno BI com Real > 0
    (a refeição declarada fica absorvida); turno sem produção mantém a refeição declarada como cinza;
    Valorizado = Janela - soma de P; Vermelha = resíduo (Produção - Amarela - Valorizado).
 4. Qualidade = 1 - refugo / Real; refugo = TiposErros[Quantidade] com a Trançadeira normalizada, na data do refugo
    (e, com turno filtrado, no Turno Erro igual ao turno).
 5. TCU = Valorizado x Q / (minutos do turno x dias x máquinas), 11 máquinas da fx_CelulasTrancagem.
 6. Reconcilia com a seção "Achados" do plano (mesma conta no grão linha, 01/09 a 06/11).
"""
import argparse
import csv
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[3]
CSV_HH = RAIZ / "Dados_Brutos" / "Hora-Hora_2026-11-06.csv"
CSV_ERROS = RAIZ / "Dados_Brutos" / "TiposErros_2026-11-06.csv"
CSV_MAPA = RAIZ / "GMS" / "PowerBI" / "modelo" / "dMotivoParada.csv"
SAIDA = Path(__file__).resolve().parent / "oee2_referencia_2026-09-04_a_11-06.csv"

INI, FIM = pd.Timestamp("2026-09-04"), pd.Timestamp("2026-11-06")
CELULAS = ["TH01", "TH02", "TH03", "TH04", "TH05", "TH06", "TH07", "TO04", "TM01", "TM04", "Spiral"]  # fx_CelulasTrancagem
TURNOS = ["1º Turno", "2º Turno", "3º Turno"]
MIN_TURNO = {"1º Turno": 540, "2º Turno": 480, "3º Turno": 420}   # horas cheias 05-14, 14-22, 22-05
PAUSA = 45
TURNO_MIN_PAUSA = 240  # turno com menos de 4 h (só hora extra) não recebe pausa (William, 12/11/2026)
LIM_AVISO = 1.02            # Valorizado (Real) acima do Valorizado em mais de 2%


# ------------------------------------------------------------------ leitura
def numero(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s.str.replace(",", "", regex=False), errors="coerce")


def motivo_padrao(t):
    """Mesma regra da coluna fHoraHora[Motivo Padrão]: tira o prefixo numérico "NN - ", Refeição vira Almoço."""
    if not isinstance(t, str) or not t.strip():
        return None
    t = t.strip()
    p = t.find("-")
    pre = t[:p].strip() if p > 0 else ""
    try:
        float(pre)
        limpo = t[p + 1:].strip()
    except ValueError:
        limpo = t
    return {"Refeição": "Almoço", "Problema no tubo": "Análise/Problema no tubo"}.get(limpo, limpo)


def carregar_hh() -> pd.DataFrame:
    d = pd.read_csv(CSV_HH, encoding="utf-8-sig", dtype=str)
    d = d.rename(columns={"Meta Hora": "MetaHora", "Real. Hora": "Real0", "Tempo Parado (min)": "Par0"})
    d["Data"] = pd.to_datetime(d["Data"], format="%m/%d/%Y")
    for c in ("MetaHora", "Real0", "Par0", "Minutos"):
        d[c] = numero(d[c])
    d["ID"] = d["ID"].astype(int)
    d["MotivoP"] = d["Motivo"].map(motivo_padrao)
    return d[d["Célula"].notna()].copy()          # a página filtra Célula não vazia


def carregar_mapa() -> pd.DataFrame:
    m = pd.read_csv(CSV_MAPA, sep=";", encoding="utf-8-sig", dtype=str, keep_default_na=False)
    return m.set_index("Motivo")


def carregar_erros() -> pd.DataFrame:
    t = pd.read_csv(CSV_ERROS, encoding="utf-8-sig", dtype=str)
    t["Quantidade"] = numero(t["Quantidade"])
    t["Cel"] = t["Trançadeira"].fillna("").str.strip().str.replace("-", "", regex=False).str.replace(".", "", regex=False)
    t["DataRefugo"] = pd.to_datetime(t["DataHoraRefugo"].str.split(" ").str[0], format="%m/%d/%Y", errors="coerce")
    t["TurnoErro"] = t["Turno Erro"].where(t["Turno Erro"].isin(["1", "2", "3"])).map(
        lambda v: f"{v}º Turno" if isinstance(v, str) else None)
    return t


# ------------------------------------------------------------------ fHoraCheia (fHoraCheia.tmdl.md, linha 6 e script)
def fatiar(d: pd.DataFrame) -> pd.DataFrame:
    """Devolve a fHoraCheia: 1 linha por Célula x Data BI x hora cheia x janela de origem."""
    d = d.reset_index(drop=True)
    cel = d["Célula"].to_numpy()
    out = []
    for i, r in enumerate(d.itertuples(index=False)):
        h = r.Hora
        if not isinstance(h, str) or len(h) != 13:
            continue
        try:
            i0 = int(h[0:2]) * 60 + int(h[3:5])
            f0 = int(h[8:10]) * 60 + int(h[11:13])
        except ValueError:
            continue
        sini = (837 if h == "13:47 - 15:00" else (i0 + 1440 if i0 < 320 else i0)) - 300
        efim = f0 - 300 + 1440 if f0 - 300 <= sini else f0 - 300
        dur = efim - sini
        if not 0 < dur <= 120:
            continue
        mn = r.Minutos if (pd.notna(r.Minutos) and r.Minutos > 0) else dur
        meta = 0.0 if pd.isna(r.MetaHora) else r.MetaHora
        real = 0.0 if pd.isna(r.Real0) else r.Real0
        par = 0.0 if pd.isna(r.Par0) else r.Par0
        for k in range(sini // 60, (efim - 1) // 60 + 1):
            fr = (min(efim, (k + 1) * 60) - max(sini, k * 60)) / dur
            ho = k % 24
            out.append((r.ID, cel[i], r.Data + pd.Timedelta(days=k // 24), ho,
                        "1º Turno" if ho < 9 else "2º Turno" if ho < 17 else "3º Turno",
                        mn * fr, meta * fr, real * fr, min(par * fr, mn * fr), r.MotivoP, r.Mangueira, h))
    return pd.DataFrame(out, columns=["ID", "Célula", "DataBI", "HoraOrdem", "TurnoBI", "Minutos", "MetaCheia", "Real",
                                      "Parado", "MotivoP", "Mangueira", "HoraOrigem"])


# ------------------------------------------------------------------ OEE2
def classificar(f: pd.DataFrame, mapa: pd.DataFrame) -> pd.DataFrame:
    f = f.copy()
    f["Familia"] = f["MotivoP"].map(mapa["Família"]).fillna("")
    f["Refeicao"] = f["MotivoP"] == "Almoço"
    return f


def valorizado_real(f: pd.DataFrame) -> pd.Series:
    """Σ MIN(Real, Meta Cheia) x Minutos ÷ Meta Cheia (medida de controle, com a Meta Cheia)."""
    razao = np.where(f["MetaCheia"] > 0, np.minimum(f["Real"], f["MetaCheia"]) / f["MetaCheia"].where(f["MetaCheia"] > 0, 1),
                     np.where(f["Real"] > 0, 1.0, 0.0))
    return pd.Series(razao * f["Minutos"], index=f.index)


def turnos_de_maquina(f: pd.DataFrame) -> pd.DataFrame:
    """Uma linha por Célula x Data BI x Turno BI, com a pausa fixa aplicada (seção B do plano)."""
    f = f.copy()
    f["P_amarela"] = np.where(f["Familia"] == "Amarela", f["Parado"], 0.0)
    f["P_vermelha"] = np.where(f["Familia"] == "Vermelha", f["Parado"], 0.0)
    f["P_azcz_sem_ref"] = np.where(f["Familia"].isin(["Azul", "Cinza"]) & ~f["Refeicao"], f["Parado"], 0.0)
    f["P_ref"] = np.where(f["Refeicao"], f["Parado"], 0.0)
    f["P_semfam"] = np.where(f["Familia"] == "", f["Parado"], 0.0)
    f["VR"] = valorizado_real(f)
    f["Meta_op"] = np.where(f["Real"] > 0, f["MetaCheia"], 0.0)
    f["Real_op"] = np.where(f["Real"] > 0, f["Real"], 0.0)
    g = f.groupby(["Célula", "TurnoBI", "DataBI"], as_index=False).agg(
        Min=("Minutos", "sum"), Real=("Real", "sum"), P=("Parado", "sum"), Am=("P_amarela", "sum"),
        Verm_decl=("P_vermelha", "sum"), AzCz=("P_azcz_sem_ref", "sum"), Ref=("P_ref", "sum"),
        SemFam=("P_semfam", "sum"), VR=("VR", "sum"), MetaOp=("Meta_op", "sum"), RealOp=("Real_op", "sum"),
        Meta=("MetaCheia", "sum"))
    recebe = (g["Real"] > 0) & (g["Min"] >= TURNO_MIN_PAUSA)
    g["Pausa"] = np.where(recebe, PAUSA, 0.0)
    g["Plan"] = g["AzCz"] + np.where(recebe, g["Pausa"], g["Ref"])
    return g


def refugo(erros: pd.DataFrame, celulas, turno=None, ini=INI, fim=FIM) -> float:
    e = erros[erros["DataRefugo"].between(ini, fim) & erros["Cel"].isin(celulas)]
    if turno is not None:
        e = e[e["TurnoErro"].isin(turno)]
    return float(e["Quantidade"].sum())


def indices(g: pd.DataFrame, erros: pd.DataFrame, celulas, turnos, dias, filtra_turno) -> dict:
    """Todos os números de um corte (g já filtrado para as máquinas/turnos do corte)."""
    j, plan = g["Min"].sum(), g["Plan"].sum()
    prod = j - plan
    am = g["Am"].sum()
    val = j - g["P"].sum()
    verm = prod - am - val
    real = g["Real"].sum()
    ref = refugo(erros, celulas, turnos if filtra_turno else None)
    op = prod - am
    q = max(0.0, 1 - ref / real) if real > 0 else np.nan
    d_ = (prod - am) / prod if prod > 0 and real > 0 else np.nan
    p_ = val / op if op > 0 and real > 0 else np.nan
    n_maq = sum(1 for c in CELULAS if c in celulas)
    den = sum(MIN_TURNO[t] for t in turnos) * dias * n_maq
    tcu = (val * q / den) if real > 0 and den > 0 else 0.0
    vr = g["VR"].sum()
    pv = g["RealOp"].sum() / g["MetaOp"].sum() if g["MetaOp"].sum() > 0 else np.nan
    return {
        "Janela": j, "Planejada": plan, "Producao": prod, "Amarela": am, "Vermelha": verm, "Vermelha_declarada": g["Verm_decl"].sum(),
        "Sem_familia": g["SemFam"].sum(), "Parado_total": g["P"].sum(), "Valorizado": val, "Valorizado_Real": vr,
        "Real_m": real, "Refugo_m": ref, "D": d_, "P": p_, "Q": q, "OEE2": (d_ * p_ * q) if real > 0 and not np.isnan(d_ * p_) else np.nan,
        "TCU": tcu, "Perf_velocidade": pv, "Dif_Val_Real_pct": (vr / val - 1) if val > 0 else np.nan,
        "Aviso": bool((not np.isnan(pv) and pv > 1) or (val > 0 and vr > val * LIM_AVISO)),
    }


def cortes(g: pd.DataFrame, erros: pd.DataFrame, dias: int) -> pd.DataFrame:
    linhas = []

    def add(corte, chave, sub, celulas, turnos, filtra_turno):
        r = indices(sub, erros, celulas, turnos, dias, filtra_turno)
        r.update({"Corte": corte, "Chave": chave})
        linhas.append(r)

    todas = set(CELULAS)
    add("Total", "Total", g, todas, TURNOS, False)
    for c in CELULAS:
        add("Máquina", c, g[g["Célula"] == c], {c}, TURNOS, False)
    for t in TURNOS:
        add("Turno BI", t, g[g["TurnoBI"] == t], todas, [t], True)
    for c in CELULAS:
        for t in TURNOS:
            add("Máquina x Turno BI", f"{c} | {t}", g[(g["Célula"] == c) & (g["TurnoBI"] == t)], {c}, [t], True)
    cols = ["Corte", "Chave", "Janela", "Planejada", "Producao", "Amarela", "Vermelha", "Vermelha_declarada", "Sem_familia",
            "Parado_total", "Valorizado", "Valorizado_Real", "Real_m", "Refugo_m", "D", "P", "Q", "OEE2", "TCU",
            "Perf_velocidade", "Dif_Val_Real_pct", "Aviso"]
    return pd.DataFrame(linhas)[cols]


# ------------------------------------------------------------------ Achados do plano (grão linha, 01/09 a 06/11)
def achados_linha(d: pd.DataFrame, mapa: pd.DataFrame, minutos_do_rotulo: bool) -> dict:
    """Refaz a conta da seção "Achados" do plano: 1 linha da lista = 1 janela, sem hora cheia, 01/09 a 06/11, sem pausa fixa.
    Como no plano (achado 4), as linhas com Minutos = 0 saem; com minutos_do_rotulo=True elas entram pela duração do rótulo."""
    x = d[(d["Data"] >= "2026-09-01") & (d["Data"] <= "2026-11-06")].copy()
    dur = x["Hora"].map(lambda h: (lambda i0, f0: (f0 - i0) % 1440)(int(h[0:2]) * 60 + int(h[3:5]), int(h[8:10]) * 60 + int(h[11:13]))
                        if isinstance(h, str) and len(h) == 13 else np.nan)
    if minutos_do_rotulo:
        x["Min"] = np.where(x["Minutos"] > 0, x["Minutos"], dur)
    else:
        x = x[x["Minutos"].fillna(0) > 0].copy()
        x["Min"] = x["Minutos"]
    x["P"] = np.minimum(x["Par0"].fillna(0), x["Min"])
    x["Familia"] = x["MotivoP"].map(mapa["Família"]).fillna("")
    j = x["Min"].sum()
    plan = x.loc[x["Familia"].isin(["Azul", "Cinza"]), "P"].sum()
    am = x.loc[x["Familia"] == "Amarela", "P"].sum()
    ve = x.loc[x["Familia"] == "Vermelha", "P"].sum()
    sem = x.loc[x["Familia"] == "", "P"].sum()
    return {"linhas": len(x), "Janela": j, "Planejada": plan, "Producao": j - plan, "Amarela": am, "Vermelha": ve,
            "Sem_familia": sem, "Valorizado": j - x["P"].sum(), "Parado_total": x["P"].sum()}


# ------------------------------------------------------------------ saída
def pct(v):
    return "   --  " if pd.isna(v) else f"{v * 100:6.1f}%"


def imprime(c: pd.DataFrame, titulo, filtro):
    print(f"\n== {titulo}")
    print(f"{'':22s}{'Janela':>9s}{'Plan.':>8s}{'Prod.':>9s}{'Amar.':>8s}{'Verm.':>8s}{'Valor.':>9s}{'Real m':>9s}{'Ref m':>7s}"
          f"{'D':>8s}{'P':>8s}{'Q':>8s}{'OEE2':>8s}{'TCU':>8s}  aviso")
    for r in c[filtro(c)].itertuples():
        print(f"{r.Chave:22s}{r.Janela:9.0f}{r.Planejada:8.0f}{r.Producao:9.0f}{r.Amarela:8.0f}{r.Vermelha:8.0f}"
              f"{r.Valorizado:9.0f}{r.Real_m:9.0f}{r.Refugo_m:7.0f}{pct(r.D)}{pct(r.P)}{pct(r.Q)}{pct(r.OEE2)}{pct(r.TCU)}"
              f"  {'SIM' if r.Aviso else ''}")


def explica(f: pd.DataFrame, dia, cel, turno):
    s = f[(f["DataBI"] == pd.Timestamp(dia)) & (f["Célula"] == cel) & (f["TurnoBI"] == turno)].sort_values("HoraOrdem")
    pd.set_option("display.width", 200)
    print(s[["ID", "HoraOrigem", "HoraOrdem", "Minutos", "MetaCheia", "Real", "Parado", "MotivoP", "Familia"]].round(2).to_string(index=False))
    g = turnos_de_maquina(s)
    print(g.assign(DataBI=g["DataBI"].dt.strftime("%d/%m/%Y")).round(1).T.to_string(header=False))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--explica", nargs=3, metavar=("DATA_BI", "CELULA", "TURNO"))
    a = ap.parse_args()
    mapa, d, erros = carregar_mapa(), carregar_hh(), carregar_erros()
    cheia = classificar(fatiar(d), mapa)
    if a.explica:
        explica(cheia, *a.explica)
        return
    per = cheia[(cheia["DataBI"] >= INI) & (cheia["DataBI"] <= FIM)]
    dias = (per["DataBI"].max() - per["DataBI"].min()).days + 1
    print(f"Lista: {len(d)} linhas com Célula (de {len(pd.read_csv(CSV_HH, encoding='utf-8-sig', dtype=str))}); fHoraCheia: {len(cheia)} linhas; "
          f"período {INI:%d/%m} a {FIM:%d/%m}: {len(per)} linhas, {dias} dias, {per['Célula'].nunique()} máquinas")
    nao_mapeados = sorted(per.loc[per["Familia"] == "", "MotivoP"].dropna().unique())
    print("Motivos sem família no período (caem no resíduo vermelho):", nao_mapeados or "nenhum")
    g = turnos_de_maquina(per)
    c = cortes(g, erros, dias)
    imprime(c, "TOTAL e por turno BI (minutos; D, P, Q, OEE2 e TCU)", lambda x: x["Corte"].isin(["Total", "Turno BI"]))
    imprime(c, "POR MÁQUINA", lambda x: x["Corte"] == "Máquina")
    t = c[c["Corte"] == "Total"].iloc[0]
    print("\n-- Fechamento: Σ P por família = Parado capado total")
    print(f"   amarela {t.Amarela:,.0f} + vermelha declarada {t.Vermelha_declarada:,.0f} + sem família {t.Sem_familia:,.0f} "
          f"+ azul/cinza {t.Parado_total - t.Amarela - t.Vermelha_declarada - t.Sem_familia:,.0f} = {t.Parado_total:,.0f} (Parado total)")
    print(f"   Produção - Amarela - Valorizado = Vermelha residual {t.Vermelha:,.0f}; "
          f"vermelha declarada {t.Vermelha_declarada:,.0f} + sem família {t.Sem_familia:,.0f} + refeição declarada nos turnos com "
          f"produção - pausa fixa = {t.Vermelha:,.0f} (a diferença é a refeição absorvida)")
    n_turnos = int(((g["Real"] > 0) & (g["Min"] >= TURNO_MIN_PAUSA)).sum())
    print(f"   turnos de máquina: {len(g)}; com Real > 0 (recebem pausa): {n_turnos}; pausa fixa {g['Pausa'].sum():,.0f} min; "
          f"refeição declarada nesses turnos {g.loc[g['Real'] > 0, 'Ref'].sum():,.0f} min; "
          f"turnos com refeição declarada acima de 45 min: {int((g['Ref'] > PAUSA).sum())}")
    print(f"   Valorizado (Real) / Valorizado - 1 = {t.Dif_Val_Real_pct * 100:+.1f}% (controle exige < 2% em módulo)")
    sem_plano = per[(per["MetaCheia"] == 0) & (per["Real"] == 0) & (per["Parado"] == 0)]
    print(f"   janelas sem meta, sem produção e sem parada (contam como valorizado pela conta Janela - Σ P): "
          f"{sem_plano['Minutos'].sum():,.0f} min ({sem_plano['Minutos'].sum() / t.Janela * 100:.1f}% da janela)")
    sem_real = g[g["Real"] == 0]
    print(f"   turnos de máquina sem nenhum metro (Real = 0): {len(sem_real)}, {sem_real['Min'].sum():,.0f} min na janela, "
          f"Valorizado delas {(sem_real['Min'] - sem_real['P']).sum():,.0f} min")
    avisos = c[(c["Corte"] == "Máquina") & c["Aviso"]]
    print("   máquinas com aviso de velocidade:", ", ".join(
        f"{r.Chave} (Real/Meta {r.Perf_velocidade * 100:.0f}%, VR/Val {r.Dif_Val_Real_pct * 100:+.0f}%)" for r in avisos.itertuples()) or "nenhuma")

    # reconciliação com os "Achados" do plano
    a0, a1 = achados_linha(d, mapa, False), achados_linha(d, mapa, True)
    print("\n== Reconciliação com os Achados do plano (grão linha, 01/09 a 06/11, sem pausa fixa)")
    esperado = {"Janela": 429920, "Planejada": 51431, "Producao": 378489, "Amarela": 60681, "Vermelha": 114532, "Valorizado": 203276}
    print(f"   {'':11s}{'plano':>10s}{'aqui, regra do plano':>22s}{'dif.':>8s}{'com minutos do rótulo':>24s}")
    for k, v in esperado.items():
        print(f"   {k:11s}{v:>10,d}{a0[k]:>22,.0f}{a0[k] - v:>+8,.0f}{a1[k]:>24,.0f}")
    print(f"   linhas {a0['linhas']} (plano: 8.140 com e sem Minutos; aqui só as com Minutos > 0, e {a1['linhas']} com o rótulo); "
          f"o Valorizado do plano (Prod. - Amarela - Vermelha) não desconta {a0['Sem_familia']:,.0f} min de linhas sem motivo; "
          f"Janela - Σ P = {a0['Valorizado']:,.0f}")
    print(f"   OEE2 sem qualidade na conta do plano: {a0['Valorizado'] / a0['Producao'] * 100:.1f}% (plano 53,7%); "
          f"com os minutos do rótulo: {a1['Valorizado'] / a1['Producao'] * 100:.1f}%")

    c.to_csv(SAIDA, sep=";", index=False, encoding="utf-8-sig", float_format="%.4f", quoting=csv.QUOTE_MINIMAL)
    print(f"\nReferência gravada: {SAIDA.name} ({len(c)} linhas)")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
