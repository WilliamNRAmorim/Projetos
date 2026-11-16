# -*- coding: utf-8 -*-
"""Conferência da página "Produção x meta (SAP)" do GMS_Painel (MEL-273).
Aplica em Python a MESMA transformação da tabela fProducaoSAP (modelo/mascara_producao.tmdl.md) e as MESMAS regras
das medidas "SAP ...": mês da página, corte, dias contabilizados, produzido, meta acumulada, saldo, ritmo.

Dois modos de entrada (um só por execução):
  --bruto MB51.xlsx COOIS.xlsx   exports crus do SAP (aba única "Data"): faz tudo (RemoveLastN, FM, join, KG, grupo)
  --mascara arquivo.xlsx         cópia local da Máscara (aba MB51 = tabela mb51_coois, já com MRP controller)
                                 (padrão: a cópia de 13/11 que está no scratchpad da sessão)

Opções:
  --hoje AAAA-MM-DD   "hoje" simulado (padrão: hoje no Brasil, UTC-3)
  --mes AAAA-MM       mês escolhido na segmentação (padrão: vazio = mês de ontem)
  --meta M,A,F        meta diária Mangueira,Montagem,Fittings (padrão 6600,2517,800)
  --uteis N           dias úteis do mês (padrão 22)

Uso:  python -I conferir_sap.py --mascara  [--hoje 2026-11-13]
      python -I conferir_sap.py --bruto mb51.xlsx coois.xlsx --hoje 2026-11-05
"""
import sys, argparse, collections, datetime as dt
import openpyxl

sys.stdout.reconfigure(encoding="utf-8")

PADRAO = (r"C:\Users\U445131\AppData\Local\Temp\claude\9be407617cb2adde\ebd84360-bfd7-42fd-8843-d2d7d165a7d7"
          r"\scratchpad\xl\mascara.xlsx")
ORDEM = ["Mangueira", "Montagem", "Fittings"]
UN = {"Mangueira": "m", "Montagem": "pç", "Fittings": "pç"}
CASAS = {"Mangueira": 1, "Montagem": 0, "Fittings": 0}


def produto_do_mrp(mrp):
    """Mesma regra do M: AIH Mangueira; Z35 ou AWE Montagem; AO0 Fittings; o resto sai."""
    m = ("" if mrp is None else str(mrp)).strip()
    if m == "AIH":
        return "Mangueira"
    if m in ("Z35", "AWE"):
        return "Montagem"
    if m == "AO0":
        return "Fittings"
    return None


def como_data(v):
    if isinstance(v, dt.datetime):
        return v.date()
    return v if isinstance(v, dt.date) else None


def como_int(v):
    try:
        return int(str(v).strip())
    except (TypeError, ValueError):
        return None


def vazio(v):
    return v is None or str(v).strip() == ""


# ------------------------------------------------------------------ leitura
def ler_bruto(arq_mb51, arq_coois):
    """Replica o M do fProducaoSAP. Devolve (linhas [(data, produto, material, tipo, unidade, qtd, key_doc)], info)."""
    info = {}
    wb = openpyxl.load_workbook(arq_coois, read_only=True, data_only=True)
    it = wb[wb.sheetnames[0]].iter_rows(values_only=True)
    cab = list(next(it))
    iO, iM = cab.index("Order"), cab.index("MRP controller")
    coois = collections.defaultdict(list)            # Order -> [MRP controller, ...]
    for r in it:
        o = como_int(r[iO])
        if o is not None or not vazio(r[iO]):
            coois[o].append(r[iM])
    rep = {o: len(v) for o, v in coois.items() if len(v) > 1}
    info["coois_linhas"] = sum(len(v) for v in coois.values())
    info["orders_repetidas"] = len(rep)
    info["orders_repetidas_mrp_diferente"] = sum(1 for o in rep if len({str(x).strip() for x in coois[o]}) > 1)
    info["orders_repetidas_exemplos"] = sorted(rep.items())[:5]

    wb = openpyxl.load_workbook(arq_mb51, read_only=True, data_only=True)
    linhas_mb = [list(r) for r in wb[wb.sheetnames[0]].iter_rows(values_only=True)]
    cab = linhas_mb[0]
    cab = ["Storage location" if c == "Storage Location" else "Movement type" if c == "Movement Type" else c for c in cab]
    corpo = linhas_mb[1:]
    info["mb51_linhas_cruas"] = len(corpo)
    corpo = corpo[:-3] if len(corpo) > 3 else []     # Table.RemoveLastN(..., 3): linhas de total do SAP
    ix = {c: cab.index(c) for c in ("Material", "Order", "Movement type", "Posting Date", "Qty in unit of entry",
                                    "Unit of Entry", "Material Document", "Material Doc.Item")}
    saida, sem_mrp, dup_extra = [], 0, 0
    for r in corpo:
        mat = r[ix["Material"]]
        if vazio(mat) or str(mat).strip().upper().startswith("FM"):
            continue
        o = como_int(r[ix["Order"]])
        mrps = coois.get(o) if o is not None else None
        if not mrps:
            mrps = [None]                                   # LEFT JOIN: sem match, MRP controller nulo
            sem_mrp += 1
        dup_extra += len(mrps) - 1
        for mrp in mrps:                                    # repetição de Order duplica a linha (igual à Máscara)
            saida.append((r[ix["Posting Date"]], mrp, mat, como_int(r[ix["Movement type"]]),
                          r[ix["Unit of Entry"]], r[ix["Qty in unit of entry"]],
                          (r[ix["Material Document"]], r[ix["Material Doc.Item"]])))
    info["linhas_apos_join"] = len(saida)
    info["linhas_sem_match_coois"] = sem_mrp
    info["linhas_duplicadas_pelo_join"] = dup_extra
    return saida, info


def ler_mascara(arq):
    """Tabela mb51_coois (aba MB51) da Máscara: já sem totais, com MRP controller."""
    wb = openpyxl.load_workbook(arq, read_only=True, data_only=True)
    it = wb["MB51"].iter_rows(values_only=True)
    cab = list(next(it))
    ix = {c: cab.index(c) for c in ("MRP controller", "Material", "Movement type", "Posting Date",
                                    "Qty in unit of entry", "Unit of Entry", "Material Document", "Material Doc.Item")}
    saida, chaves = [], collections.Counter()
    for r in it:
        if r[ix["Posting Date"]] is None or r[ix["MRP controller"]] is None:
            continue
        k = (r[ix["Material Document"]], r[ix["Material Doc.Item"]])
        chaves[k] += 1
        saida.append((r[ix["Posting Date"]], r[ix["MRP controller"]], r[ix["Material"]], como_int(r[ix["Movement type"]]),
                      r[ix["Unit of Entry"]], r[ix["Qty in unit of entry"]], k))
    info = {"linhas_apos_join": len(saida),
            "linhas_duplicadas_pelo_join": sum(c - 1 for c in chaves.values() if c > 1)}
    return saida, info


# ------------------------------------------------------------------ fProducaoSAP e medidas
def montar_fato(linhas):
    """Grão final: Data, Produto, Material, Tipo de movimento, Unidade (soma de Quantidade). Sem KG; sem produto fora."""
    g = collections.defaultdict(float)
    for data, mrp, mat, tipo, un, qtd, _ in linhas:
        prod = produto_do_mrp(mrp)
        d = como_data(data)
        if prod is None or d is None or un == "KG":
            continue
        g[(d, prod, mat, tipo, un)] += float(qtd or 0)
    return g


def br(v, c):
    s = f"{v:,.{c}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def medidas(fato, hoje, mes_escolhido, meta, uteis):
    soma = collections.defaultdict(float)          # (data, produto) -> qtd
    for (d, p, *_), q in fato.items():
        soma[(d, p)] += q
    datas = sorted({d for d, _ in soma})
    ontem = hoje - dt.timedelta(days=1)
    if mes_escolhido:
        ini = dt.date(mes_escolhido[0], mes_escolhido[1], 1)
    else:
        ini = dt.date(ontem.year, ontem.month, 1)
    fim_mes = (dt.date(ini.year + (ini.month == 12), ini.month % 12 + 1, 1) - dt.timedelta(days=1))
    fim = min(fim_mes, ontem)
    cand = [d for d in datas if d <= fim]
    corte = max(cand) if cand else None
    if corte is not None and corte < ini:
        corte = None
    print(f"hoje={hoje:%d/%m/%Y} | mês da página={ini:%m/%Y} ({'escolhido' if mes_escolhido else 'vazio = mês de ontem'})"
          f" | corte={corte:%d/%m/%Y}" if corte else f"hoje={hoje:%d/%m/%Y} | mês={ini:%m/%Y} | sem dado até o corte")
    if corte is None:
        return
    dias = [d for d in datas if ini <= d <= corte]
    n = len(dias)
    encerrado = fim_mes < hoje
    print(f"dias contabilizados={n} (de {uteis} úteis): " + ", ".join(f"{d:%d}" for d in dias))
    for p in ORDEM:
        md, c, u = meta[p], CASAS[p], UN[p]
        serie = [soma.get((d, p), 0.0) for d in dias]
        prod = sum(serie)
        macum = md * n
        saldo = prod - macum
        pct = prod / macum if macum else None
        rest = uteis - n
        ritmo = (md * uteis - prod) / rest if (rest > 0 and not encerrado) else None
        print(f"\n{p}: meta diária {br(md, 0)} {u} | dias úteis {uteis} | dias contabilizados {n}")
        print(f"  produzido {br(prod, c)} {u} | meta acumulada {br(macum, 0)} | saldo {br(saldo, c)} | "
              f"% da meta {br(pct * 100, 1) + '%' if pct is not None else '-'} | feliz={saldo >= 0}")
        print(f"  dias que faltam {rest} | ritmo para fechar "
              f"{br(ritmo, c) + ' ' + u + '/dia' if ritmo is not None else '- (Mês fechado)'}")
        print("  série diária: " + "  ".join(f"{d:%d/%m}={br(v, c)}" for d, v in zip(dias, serie)))


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--bruto", nargs=2, metavar=("MB51", "COOIS"))
    g.add_argument("--mascara", nargs="?", const=PADRAO, default=None)
    ap.add_argument("--hoje")
    ap.add_argument("--mes")
    ap.add_argument("--meta", default="6600,2517,800")
    ap.add_argument("--uteis", type=int, default=22)
    a = ap.parse_args()

    hoje = dt.date.fromisoformat(a.hoje) if a.hoje else (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=3)).date()
    mes = tuple(int(x) for x in a.mes.split("-")) if a.mes else None
    meta = dict(zip(ORDEM, (float(x) for x in a.meta.split(","))))

    if a.bruto:
        linhas, info = ler_bruto(*a.bruto)
        print("MODO bruto:", a.bruto[0], "+", a.bruto[1])
    else:
        arq = a.mascara or PADRAO
        linhas, info = ler_mascara(arq)
        print("MODO máscara (tabela mb51_coois já unida):", arq)
    for k, v in info.items():
        print(f"  {k}: {v}")
    fato = montar_fato(linhas)
    print(f"  fProducaoSAP: {len(fato)} linhas no grão Data x Produto x Material x Tipo x Unidade")
    if "orders_repetidas" in info and info["orders_repetidas"]:
        print("  AVISO: a COOIS tem Order repetida; o join duplica linha (igual à Máscara). Confira os números acima.")
    if info.get("linhas_duplicadas_pelo_join"):
        print(f"  AVISO: {info['linhas_duplicadas_pelo_join']} linhas repetidas por (Material Document, Item).")
    print()
    medidas(fato, hoje, mes, meta, a.uteis)


if __name__ == "__main__":
    main()
