# -*- coding: utf-8 -*-
"""Prototipo da fHoraCheia (MEL-267). Rodar: python -I prototipo_hora_cheia.py
Le o backup da Hora-Hora, aplica a regra de hora cheia e grava conferencia_prototipo.md."""
import csv, re, os, collections
from datetime import datetime, timedelta

AQUI = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(AQUI, "..", "Higienizacao_HoraHora", "HoraHora_backup_2026-09-01_a_2026-10-15.csv")
SAIDA = os.path.join(AQUI, "conferencia_prototipo.md")
REFEICAO_MIN = 45
EPS = 1e-6


def num(t):
    t = (t or "").strip()
    return float(t) if t else 0.0


def hm(t):
    return int(t[:2]) * 60 + int(t[3:5])


def motivo_padrao(m):
    """Mesma logica da coluna 'Motivo Padrão' da fHoraHora (vazio -> None)."""
    t = (m or "").strip()
    if not t:
        return None
    p = t.find("-") + 1  # SEARCH("-"): 1-based, 0 se nao achar
    pre = t[:p - 1].strip() if p > 1 else ""
    limpo = t[p:p + 300].strip() if (p > 1 and re.fullmatch(r"\d+", pre)) else t
    if limpo == "Refeição":
        return "Almoço"
    if limpo == "Problema no tubo":
        return "Análise/Problema no tubo"
    return limpo


def data_local(utc):
    # 2026-09-14T03:00:00Z = dia 14 local (UTC-3)
    return (datetime.strptime(utc, "%Y-%m-%dT%H:%M:%SZ") - timedelta(hours=3)).date()


def janela(hora):
    """Inicio e fim absolutos em minutos desde 00:00 da Data (pos-meia-noite = 1440+).
    HoraOrdem da base: h < 05:20 -> +1440. 13:47-15:00 vale 13:57-15:00."""
    a, b = hora.split(" - ")
    h = hm(a)
    ini = h + 1440 if h < 5 * 60 + 20 else h
    if hora == "13:47 - 15:00":
        ini = 13 * 60 + 57
    fim = hm(b)
    while fim <= ini:
        fim += 1440
    return ini, fim


def turno_bi(k):
    return "1º Turno" if k < 9 else ("2º Turno" if k < 17 else "3º Turno")


def rotulo(k):
    h = (5 + k) % 24
    return "%02d:00 - %02d:00" % (h, (h + 1) % 24)


def carregar():
    rows = []
    with open(CSV, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            ini, fim = janela(r["Hora"])
            mp = motivo_padrao(r["Motivo"])
            minutos = num(r["Minutos"])
            meta = num(r["Meta Hora"])
            meta_ef = meta * max(0.0, minutos - REFEICAO_MIN) / minutos if (mp == "Almoço" and minutos > 0) else meta
            rows.append(dict(id=int(r["ID"]), cel=r["Celula"], data=data_local(r["Data"]), turno=r["Turno"].strip(),
                             hora=r["Hora"], ini=ini, fim=fim, minutos=minutos, meta=meta, meta_ef=meta_ef,
                             real=num(r["Real. Hora"]), parado=num(r["Tempo Parado (min)"]),
                             motivo=r["Motivo"].strip(), mp=mp))
    return rows


def ratear(rows):
    """Uma linha por janela x hora cheia (fHoraCheia)."""
    out = []
    for r in rows:
        s, e = r["ini"] - 300, r["fim"] - 300  # origem = 05:00 da Data
        comp = e - s
        for k in range(s // 60, (e - 1) // 60 + 1):
            ov = min(e, (k + 1) * 60) - max(s, k * 60)
            if ov <= 0:
                continue
            fr = ov / comp
            min_f = r["minutos"] * fr
            out.append(dict(cel=r["cel"], dia=r["data"] + timedelta(days=k // 24), ordem=k % 24, id=r["id"],
                            hora_org=r["hora"], fr=fr, minutos=min_f, meta=r["meta_ef"] * fr, real=r["real"] * fr,
                            parado=min(r["parado"] * fr, min_f), parado_sem_cap=r["parado"] * fr,
                            mp=r["mp"], motivo=r["motivo"], extra=(r["hora"] == "22:20 - 23:20"),
                            noite3=(r["hora"] in ("22:20 - 23:00", "23:00 - 00:00"))))
    return out


def somar(lst, chave, campos):
    d = collections.defaultdict(lambda: dict.fromkeys(campos, 0.0))
    for x in lst:
        for c in campos:
            d[chave(x)][c] += x[c]
    return d


def main():
    rows = carregar()
    out = ratear(rows)
    L = []
    P = L.append
    P("# Conferência do protótipo da hora cheia (MEL-267)\n")
    P("Gerado por `prototipo_hora_cheia.py` (`python -I`) sobre `HoraHora_backup_2026-09-01_a_2026-10-15.csv`. "
      "Regra: seção 1 de `PLANO.md`. Não altera nada no modelo nem no relatório.\n")
    P("- Linhas da base: %d. Linhas da fHoraCheia (janela × hora cheia): %d. Máquinas: %s." %
      (len(rows), len(out), ", ".join(sorted({r['cel'] for r in rows}))))
    P("- Dias da base (Data): %s a %s. Dias BI gerados: %s a %s.\n" % (
        min(r['data'] for r in rows), max(r['data'] for r in rows), min(x['dia'] for x in out), max(x['dia'] for x in out)))

    # ---------- invariantes ----------
    P("## 1. Invariantes\n")
    campos = ["minutos", "meta", "real", "parado"]
    antes = somar(rows, lambda r: (r["cel"], r["data"]), ["minutos", "meta_ef", "meta", "real", "parado"])
    depois = somar(out, lambda x: (x["cel"], x["dia"]), campos)
    cb = ["minutos", "meta_ef", "real", "parado"]
    saida = collections.defaultdict(lambda: dict.fromkeys(cb, 0.0))
    entra = collections.defaultdict(lambda: dict.fromkeys(cb, 0.0))
    movidas = 0
    for r in rows:
        if r["hora"] == "05:00 - 05:20":
            movidas += 1
            for c in cb:
                saida[(r["cel"], r["data"])][c] += r[c]
                entra[(r["cel"], r["data"] + timedelta(days=1))][c] += r[c]
    chaves = set(antes) | set(depois)
    mx = dict.fromkeys(campos, 0.0)
    for k in chaves:
        a, d = antes.get(k), depois.get(k)
        for c, ca in (("minutos", "minutos"), ("meta", "meta_ef"), ("real", "real"), ("parado", "parado")):
            esp = (a[ca] if a else 0.0) - saida[k][ca] + entra[k][ca]
            got = d[c] if d else 0.0
            mx[c] = max(mx[c], abs(got - esp))
    P("Por máquina e dia (%d pares máquina × dia). Esperado do dia D = base(D) − janela 05:00-05:20 de D + janela 05:00-05:20 de D−1; "
      "as %d janelas 05:00-05:20 da base são a única coisa que muda de dia." % (len(chaves), movidas))
    P("")
    P("| Grandeza | Σ base (sem desconto) | Σ depois | Maior desvio por máquina × dia vs esperado |")
    P("|---|---:|---:|---:|")
    tb = {c: sum(r[c] for r in rows) for c in ("minutos", "meta", "meta_ef", "real", "parado")}
    ta = {c: sum(x[c] for x in out) for c in campos}
    P("| Minutos | %.2f | %.2f | %.2e |" % (tb["minutos"], ta["minutos"], mx["minutos"]))
    P("| Real | %.2f | %.2f | %.2e |" % (tb["real"], ta["real"], mx["real"]))
    P("| Parado (min) | %.2f | %.2f | %.2e |" % (tb["parado"], ta["parado"], mx["parado"]))
    P("| Meta (depois do desconto do almoço) | %.2f | %.2f | %.2e |" % (tb["meta_ef"], ta["meta"], mx["meta"]))
    P("")
    P("Σ minutos, real e parado antes × depois: diferença total %.2e, %.2e, %.2e (o total geral não muda; muda só o dia, por causa da fronteira das 05:00)." %
      (abs(tb["minutos"] - ta["minutos"]), abs(tb["real"] - ta["real"]), abs(tb["parado"] - ta["parado"])))
    cap = sum(x["parado_sem_cap"] - x["parado"] for x in out)
    P("Parado cortado pelo limite dos minutos da fatia: %.4f min no total (%s)." % (cap, "nenhuma fatia estourou" if cap < EPS else "ver divergência"))
    desc = sum(r["meta"] - r["meta_ef"] for r in rows)
    alm = [r for r in rows if r["mp"] == "Almoço"]
    P("")
    P("**Meta.** Σ meta base = %.2f; desconto do almoço = %.2f (%d janelas com Motivo Padrão Almoço); base − desconto = %.2f; Σ meta depois = %.2f; diferença %.2e." %
      (tb["meta"], desc, len(alm), tb["meta"] - desc, ta["meta"], abs(tb["meta"] - desc - ta["meta"])))
    zeradas = [r for r in alm if r["minutos"] <= REFEICAO_MIN]
    P("Janelas de Almoço com Minutos ≤ 45 (meta vai a zero): %d. Janelas de Almoço com Minutos > 45: %d." % (len(zeradas), len(alm) - len(zeradas)))
    ca = collections.Counter(r["hora"] for r in alm)
    P("Almoço por janela de origem: " + "; ".join("%s: %d" % kv for kv in sorted(ca.items())) + ".")

    # ---------- colisoes ----------
    P("\n## 2. Colisões\n")
    ex = {(r["cel"], r["data"]) for r in rows if r["hora"] == "22:20 - 23:20"}
    n3 = {(r["cel"], r["data"]) for r in rows if r["hora"] in ("22:20 - 23:00", "23:00 - 00:00")}
    colis = ex & n3
    P("- Hora extra `22:20 - 23:20` na mesma máquina e dia (Data) de linhas do 3º turno `22:20 - 23:00`/`23:00 - 00:00`: **%d** de %d máquinas × dia com hora extra (hora extra em %d linhas)." %
      (len(colis), len(ex), sum(1 for r in rows if r["hora"] == "22:20 - 23:20")))
    h = collections.defaultdict(set)
    for x in out:
        if x["ordem"] in (17, 18):
            h[(x["cel"], x["dia"], x["ordem"])].add("extra" if x["extra"] else ("n3" if x["noite3"] else "outra"))
    P("- Horas cheias 22:00 e 23:00 (3º turno) com fatia da hora extra E fatia do 3º turno: %d (22:00-23:00: %d; 23:00-00:00: %d). Nelas as duas somam (rateio proporcional)." %
      (sum(1 for v in h.values() if {"extra", "n3"} <= v),
       sum(1 for k, v in h.items() if k[2] == 17 and {"extra", "n3"} <= v),
       sum(1 for k, v in h.items() if k[2] == 18 and {"extra", "n3"} <= v)))
    dup = collections.Counter((r["cel"], r["data"], r["hora"]) for r in rows)
    dups = {k: v for k, v in dup.items() if v > 1}
    P("- Janelas duplicadas na base (mesma máquina, Data e Hora): **%d** combinações (%d linhas a mais). Entram duas vezes no rateio, como entram hoje na fHoraHora; é sujeira da lista (MEL-104/155), não da regra." %
      (len(dups), sum(v - 1 for v in dups.values())))
    por_hora = collections.Counter(k[2] for k in dups)
    P("  Por janela: " + "; ".join("%s: %d" % kv for kv in sorted(por_hora.items())) + ".")
    exc = [k for k, v in somar(out, lambda x: (x["cel"], x["dia"], x["ordem"]), ["minutos"]).items() if v["minutos"] > 60 + EPS]
    P("- Horas cheias (máquina × dia × hora) com mais de 60 minutos somados: **%d**. Causa: janelas `22:00 - 22:20` com Minutos 41 e `22:20 - 23:00` com Minutos 19 na base, mais duplicatas e a hora extra (22:20-23:20) somada ao 3º turno. O protótipo rateia pelo rótulo (20 e 40 min) e carrega o Minutos da linha; não corrigi." % len(exc))
    c41 = collections.Counter((r["hora"], r["minutos"]) for r in rows if r["hora"] in ("22:00 - 22:20", "22:20 - 23:00"))
    P("  Minutos por janela 22:xx na base: " + "; ".join("%s = %g: %d linhas" % (k[0], k[1], v) for k, v in sorted(c41.items())) + ".")

    # ---------- divergencias ----------
    P("\n## 3. Divergências do plano com os dados\n")
    desc_turno = collections.Counter()
    for r in rows:
        k = ((r["ini"] - 300) // 60) % 24
        if turno_bi(k) != r["turno"]:
            desc_turno[(r["hora"], r["turno"])] += 1
    P("- Rótulo `Turno` da base diferente do turno pela hora: %d linhas (soltas, já conhecidas). O `Turno BI` sai só da hora, como o plano manda." % sum(desc_turno.values()))
    P("- `HoraOrdem` da fHoraHora (minutos desde 00:00, +1440 se < 05:20) confere: `05:00 - 05:20` = 1740 (D+1 05:00 na conta); `05:20 - 06:00` = 320; `13:47 - 15:00` = 827, tratada como 837 (13:57).")
    P("- Todas as linhas têm Hora no formato `hh:mm - hh:mm`; nenhum rótulo fora dos que o plano lista.")
    P("- Janelas 22:xx: na base a `22:00 - 22:20` tem Minutos 41 em 54 linhas e a `22:20 - 23:00` tem Minutos 19 em 20 linhas (o 2º turno fecha 524 min e o 3º 399 min, soma do dia 1.440). O plano não prevê isso; mantive o Minutos da linha (sem inventar regra).")
    P("- `13:47 - 15:00`: pelo rótulo seriam 73 min, mas a janela vale 13:57–15:00 = 63 min (igual ao Minutos da base): 3/63 vai à hora 13:00 e 60/63 à 14:00, como no plano.")
    P("- Meta do almoço usa 45 fixo (plano), mesmo quando o Tempo Parado da linha de Almoço é outro (ex.: 46).")

    # ---------- dia completo TH07 ----------
    P("\n## 4. Dia completo da TH07: antes (por janela) × depois (por hora cheia)\n")
    dias = sorted({r["data"] for r in rows if r["cel"] == "TH07"})

    def pontos(d):
        rr = [r for r in rows if r["cel"] == "TH07" and r["data"] == d]
        ant = [r for r in rows if r["cel"] == "TH07" and r["data"] == d - timedelta(days=1) and r["hora"] == "05:00 - 05:20"]
        horas = {r["hora"] for r in rr}
        n_dup = len(rr) - len(horas)
        return (("22:20 - 23:20" in horas) * 3 + any(r["mp"] == "Almoço" for r in rr) * 2 + (len(ant) > 0) * 2
                + len(horas) - n_dup * 5, d)

    dia = max(dias, key=pontos)
    P("Dia escolhido: **TH07, dia produtivo %s** (05:00 de %s até 05:00 de %s), com hora extra, almoço e a janela 05:00-05:20 da noite anterior (se existir na base)." % (dia, dia, dia + timedelta(days=1)))
    rr = sorted([r for r in rows if r["cel"] == "TH07" and r["data"] == dia], key=lambda r: (r["ini"], r["id"]))
    P("\n**Antes: por janela da base (Data = %s)**\n" % dia)
    P("| Turno (base) | Hora (janela) | Min | Meta Hora | Real | Parado | Motivo Padrão |")
    P("|---|---|---:|---:|---:|---:|---|")
    for r in rr:
        P("| %s | %s | %g | %.2f | %g | %.1f | %s |" % (r["turno"], r["hora"], r["minutos"], r["meta"], r["real"], r["parado"], r["mp"] or ""))
    P("| **Total** | | %g | %.2f | %g | %.1f | |" % tuple(sum(r[c] for r in rr) for c in ("minutos", "meta", "real", "parado")))
    xs = sorted([x for x in out if x["cel"] == "TH07" and x["dia"] == dia], key=lambda x: (x["ordem"], x["id"]))
    P("\n**Depois: por hora cheia (Data BI = %s)**\n" % dia)
    P("| Turno BI | Hora | Min | Meta | Real | Parado | Origem (ID: janela × fração) |")
    P("|---|---|---:|---:|---:|---:|---|")
    por = collections.defaultdict(list)
    for x in xs:
        por[x["ordem"]].append(x)
    for k in sorted(por):
        g = por[k]
        orig = "; ".join("%d: %s × %.3f" % (x["id"], x["hora_org"], x["fr"]) for x in g)
        P("| %s | %s | %.2f | %.2f | %.2f | %.2f | %s |" % (turno_bi(k), rotulo(k), sum(x["minutos"] for x in g),
                                                         sum(x["meta"] for x in g), sum(x["real"] for x in g),
                                                         sum(x["parado"] for x in g), orig))
    tt = {c: sum(x[c] for x in xs) for c in campos}
    P("| **Total** | | %.2f | %.2f | %.2f | %.2f | |" % (tt["minutos"], tt["meta"], tt["real"], tt["parado"]))
    por_t = collections.defaultdict(lambda: dict.fromkeys(campos, 0.0))
    for x in xs:
        for c in campos:
            por_t[turno_bi(x["ordem"])][c] += x[c]
    P("\nPor turno BI: " + "; ".join("%s: min %.1f, meta %.1f, real %.1f, parado %.1f" % (t, v["minutos"], v["meta"], v["real"], v["parado"]) for t, v in sorted(por_t.items())) + ".")
    P("\nLeitura: a `05:00 - 05:20` da noite anterior (Data %s, 3º turno) entra no 05:00-06:00 do dia %s; a `05:00 - 05:20` deste dia (Data %s) sai para o dia %s. Por isso o total do dia difere do da base só por essas duas janelas." % (dia - timedelta(days=1), dia, dia, dia + timedelta(days=1)))
    P("\nReferência para o DAX de conferência de `fHoraCheia.tmdl.md`: comparar com a tabela 'Depois' acima (dia %s, célula TH07)." % dia)
    with open(SAIDA, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L) + "\n")
    print("ok", dia)


main()
