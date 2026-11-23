# -*- coding: utf-8 -*-
"""Conferência da página "Plano de mangueira x SAP" (GMS_Painel).
Reproduz em Python a lógica das medidas HP (modelo/plano_mangueira.tmdl.md) a partir da planilha do planejamento:
  - classificação e plano: aba Dados, linhas 58-160 (C=Mangueira, D=C.Standard, F=Arame, H=Tipo, K=Vol/mês)
  - produzido: aba MB51 da própria planilha (col A Material, J Posting Date, K Qty in unit of entry, L unidade)
Imprime por C.Standard, Tipo e Arame: plano, produzido, %, atraso, com dias úteis do modelo (22) e da planilha (23).
Opcional: --sap MB51.xlsx COOIS.xlsx compara o produzido com a regra MRP AIH (Mangueira) do fProducaoSAP.

Uso: python -I conferir.py [--planilha CAMINHO] [--hoje AAAA-MM-DD] [--uteis 22] [--contab N] [--sap MB51 COOIS]
"""
import sys, argparse, collections, datetime as dt
import openpyxl

sys.stdout.reconfigure(encoding="utf-8")
PLAN = r"C:\Users\U445131\Downloads\Novembro-10.xlsm"
MES = dt.date(2026, 11, 1)


def br(v, c=0):
    return f"{v:,.{c}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def ler_plano(arq):
    wb = openpyxl.load_workbook(arq, read_only=True, data_only=True)
    ws = wb["Dados"]
    linhas = []
    for r in ws.iter_rows(min_row=58, max_row=160, min_col=3, max_col=14, values_only=True):
        mang, cs, _dk, wire, _bit, tipo, _m, _h, vol, _hs, _gap, prod = r
        if mang is None or str(mang).strip() == "":
            continue
        linhas.append(dict(mang=str(mang).strip(), cs=cs, arame=wire, tipo=tipo, vol=float(vol or 0),
                           prod_planilha=float(prod or 0)))
    resumo = {}
    for r in ws.iter_rows(min_row=5, max_row=39, min_col=3, max_col=7, values_only=True):
        if r[0] and isinstance(r[1], (int, float)):
            resumo.setdefault(str(r[0]).strip(), (r[1], r[2], r[3], r[4]))
    k36 = ws["K36"].value
    cont = ws["K35"].value
    uteis = ws["K34"].value
    wb.close()
    return linhas, resumo, k36, cont, uteis


def ler_mb51_planilha(arq):
    wb = openpyxl.load_workbook(arq, read_only=True, data_only=True)
    ws = wb["MB51"]
    it = ws.iter_rows(values_only=True)
    cab = list(next(it))
    iM, iD, iQ, iU = (cab.index("Material"), cab.index("Posting Date"), cab.index("Qty in unit of entry"),
                      cab.index("Unit of Entry"))
    out = []
    for r in it:
        if r[iM] is None or not isinstance(r[iD], dt.datetime):
            continue
        out.append((str(r[iM]).strip().upper(), r[iD].date(), float(r[iQ] or 0), str(r[iU]).strip().upper()))
    wb.close()
    return out


def agrega(linhas, prod, chave):
    g = collections.OrderedDict()
    for l in linhas:
        a = g.setdefault(l[chave], [0.0, 0.0])
        a[0] += l["vol"]
        a[1] += prod.get(l["mang"].upper(), 0.0)
    return g


def imprime(titulo, g, ritmo_m, ritmo_p, resumo, ordem=None):
    print(f"\n== {titulo}")
    print(f"{'grupo':26}{'plano':>9}{'produz.':>10}{'%':>8}{'atraso22':>10}{'atraso23':>10}   planilha(plan/mtd/atraso)")
    ks = ordem or sorted(g, key=lambda k: -g[k][0])
    tp = tq = 0
    for k in ks:
        pl, pr = g[k]
        tp += pl
        tq += pr
        pct = pr / pl if pl else None
        a22 = ritmo_m * pl - pr if pl else None
        a23 = ritmo_p * pl - pr if pl else None
        rs = resumo.get(str(k).strip())
        rss = f"{br(rs[0])}/{br(rs[1], 1)}/{br(rs[3])}" if rs else "-"
        ps = (br(pct * 100, 1) + "%") if pct is not None else "-"
        print(f"{str(k):26}{br(pl):>9}{br(pr, 1):>10}{ps:>8}"
              f"{br(a22) if a22 is not None else '-':>10}{br(a23) if a23 is not None else '-':>10}   {rss}")
    pct = tq / tp if tp else 0
    print(f"{'TOTAL':26}{br(tp):>9}{br(tq, 1):>10}{br(pct * 100, 1) + '%':>8}{br(ritmo_m * tp - tq):>10}{br(ritmo_p * tp - tq):>10}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--planilha", default=PLAN)
    ap.add_argument("--hoje")
    ap.add_argument("--uteis", type=int, default=22)
    ap.add_argument("--contab", type=int)
    ap.add_argument("--sap", nargs=2, metavar=("MB51", "COOIS"))
    a = ap.parse_args()
    linhas, resumo, k36, cont_pl, uteis_pl = ler_plano(a.planilha)
    mb = ler_mb51_planilha(a.planilha)
    hoje = dt.date.fromisoformat(a.hoje) if a.hoje else dt.date(2026, 11, 19)
    fim = min(hoje - dt.timedelta(days=1), dt.date(2026, 11, 30))
    chaves = {l["mang"].upper() for l in linhas}
    datas_mang = sorted({d for k, d, q, u in mb if MES <= d <= fim and k in chaves and u == "M"})
    corte = max(datas_mang)
    prod_m, prod_todas = collections.defaultdict(float), collections.defaultdict(float)
    for k, d, q, u in mb:
        if MES <= d <= corte:
            prod_todas[k] += q
            if u == "M":
                prod_m[k] += q
    n = a.contab or len(datas_mang)
    print(f"planilha: {a.planilha}")
    print(f"hoje={hoje:%d/%m/%Y} corte={corte:%d/%m/%Y} dias com produção (datas distintas, mangueiras do plano)={n}: "
          + ",".join(f"{d:%d}" for d in datas_mang))
    print(f"planilha digita: contabilizados={cont_pl}, úteis={uteis_pl}, K36={k36:.4f} | modelo: úteis={a.uteis}, ritmo={n / a.uteis:.4f}")
    ritmo_m, ritmo_p = n / a.uteis, cont_pl / uteis_pl
    print(f"produzido das mangueiras do plano: só M = {br(sum(prod_m[k] for k in chaves), 1)} | "
          f"todas as unidades = {br(sum(prod_todas[k] for k in chaves), 1)}")
    divs = [(l["mang"], l["prod_planilha"], prod_todas.get(l["mang"].upper(), 0.0)) for l in linhas
            if abs(l["prod_planilha"] - prod_todas.get(l["mang"].upper(), 0.0)) > 0.01]
    print(f"linhas em que o N cacheado da planilha difere da minha soma (todas as unidades, até {corte:%d/%m}): {len(divs)}")
    for d in divs[:10]:
        print("  ", d)
    fora = {k: v for k, v in prod_m.items() if k not in chaves and abs(v) > 1e-9 and not k.startswith("FM")}
    print(f"materiais da MB51 da planilha sem linha no plano (unidade M): {len(fora)} com {br(sum(fora.values()), 1)} m "
          f"(sem filtro de MRP AIH; o 'fora do plano' real do modelo só conta Produto = Mangueira)")
    for k, v in sorted(fora.items(), key=lambda x: -abs(x[1]))[:6]:
        print("   ", k, br(v, 1))
    prod = prod_m
    imprime("C.Standard", agrega(linhas, prod, "cs"), ritmo_m, ritmo_p, resumo)
    imprime("Tipo", agrega(linhas, prod, "tipo"), ritmo_m, ritmo_p, resumo, ["1T", "1A", "2A", "4A"])
    imprime("Arame", agrega(linhas, prod, "arame"), ritmo_m, ritmo_p, resumo)
    pl = sum(l["vol"] for l in linhas)
    pr = sum(prod[l["mang"].upper()] for l in linhas)
    rest = a.uteis - n
    print(f"\nTotal: plano {br(pl)} | produzido {br(pr, 1)} ({br(pr / pl * 100, 1)}%) | planilha: 162.016 / 85.671 (52,9%) / atraso 5.903")
    print(f"Para fechar/dia (modelo) = (plano - produzido)/(úteis - contab.) = {br((pl - pr) / rest, 1) if rest > 0 else '-'} m/dia "
          f"com {rest} dias; plano diário {br(pl / a.uteis, 1)}")
    print("(A 'Meta ajustada' da planilha usa a meta planejada digitada em K38; a conta do modelo é plano/úteis + atraso/restantes.)")
    print("\nTop 8 atrasadas (atraso = ritmo x plano - produzido, ritmo do modelo):")
    top = sorted(((ritmo_m * l["vol"] - prod[l["mang"].upper()], l["mang"]) for l in linhas if l["vol"] > 0), reverse=True)[:8]
    for v, m in top:
        print(f"   {m:18}{br(v)} m")
    if a.sap:
        sap(a, chaves, corte)


def sap(a, chaves, corte):
    """Compara com a regra MRP AIH (Produto = Mangueira do fProducaoSAP): MRP da OP na COOIS."""
    mb51, coois = a.sap
    wb = openpyxl.load_workbook(coois, read_only=True, data_only=True)
    it = wb[wb.sheetnames[0]].iter_rows(values_only=True)
    cab = list(next(it))
    iO, iM = cab.index("Order"), cab.index("MRP controller")
    mrp = {}
    for r in it:
        try:
            mrp[int(str(r[iO]).strip())] = str(r[iM] or "").strip()
        except (TypeError, ValueError):
            pass
    wb = openpyxl.load_workbook(mb51, read_only=True, data_only=True)
    rows = [list(r) for r in wb[wb.sheetnames[0]].iter_rows(values_only=True)]
    cab, rows = rows[0], rows[1:-3]
    ix = {c: cab.index(c) for c in ("Material", "Order", "Posting Date", "Qty in unit of entry", "Unit of Entry")}
    aih, un = collections.defaultdict(float), collections.Counter()
    for r in rows:
        mat = r[ix["Material"]]
        if mat is None or str(mat).strip() == "" or str(mat).upper().startswith("FM"):
            continue
        d = r[ix["Posting Date"]]
        if not isinstance(d, dt.datetime) or not (MES <= d.date() <= corte):
            continue
        try:
            o = int(str(r[ix["Order"]]).strip())
        except (TypeError, ValueError):
            o = None
        if o is None or mrp.get(o) != "AIH" or str(r[ix["Unit of Entry"]]) == "KG":
            continue
        aih[str(mat).strip().upper()] += float(r[ix["Qty in unit of entry"]] or 0)
        un[str(r[ix["Unit of Entry"]])] += 1
    no = sum(v for k, v in aih.items() if k in chaves)
    fora = sum(v for k, v in aih.items() if k not in chaves)
    print(f"\n== MRP AIH (COOIS) até {corte:%d/%m}: no plano {br(no, 1)} m | fora do plano {br(fora, 1)} m | total {br(no + fora, 1)} | linhas por unidade: {dict(un)}")
    for k, v in sorted(((k, v) for k, v in aih.items() if k not in chaves), key=lambda x: -abs(x[1]))[:8]:
        print("   fora:", k, br(v, 1))


if __name__ == "__main__":
    main()
