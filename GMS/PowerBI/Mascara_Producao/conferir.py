# -*- coding: utf-8 -*-
"""Conferência da Máscara de produção: aplica em Python as MESMAS regras das medidas DAX.
Uso: python -I conferir.py [caminho_do_xlsx] [AAAA-MM-DD = "hoje" simulado]
Lê a cópia local (openpyxl read_only): tabela mb51_coois (aba MB51) e aba Resumo BI.
"""
import sys, collections, datetime as dt
import openpyxl

PADRAO = (r"C:\Users\U445131\AppData\Local\Temp\claude\9be407617cb2adde\ebd84360-bfd7-42fd-8843-d2d7d165a7d7"
          r"\scratchpad\xl\mascara.xlsx")
arq = sys.argv[1] if len(sys.argv) > 1 else PADRAO
if len(sys.argv) > 2:
    hoje = dt.date.fromisoformat(sys.argv[2])
else:
    hoje = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=3)).date()   # hoje no Brasil

MRP = {"AIH": "Mangueira", "Z35": "Montagem", "AWE": "Montagem", "AO0": "Fittings"}
ORDEM = ["Mangueira", "Montagem", "Fittings"]
UN = {"Mangueira": "m", "Montagem": "pç", "Fittings": "pç"}
CASAS = {"Mangueira": 1, "Montagem": 0, "Fittings": 0}

wb = openpyxl.load_workbook(arq, read_only=True, data_only=True)

# --- dProduto (aba Resumo BI)
meta, uteis = {}, {}
ws = wb["Resumo BI"]
it = ws.iter_rows(values_only=True)
cab = [str(c) if c is not None else "" for c in next(it)]
iP, iT, iV = cab.index("PRODUTO"), cab.index("TIPO"), cab.index("VALOR")
norm = {"MANGUEIRA": "Mangueira", "MONTAGEM": "Montagem", "FITTINGS": "Fittings"}
for r in it:
    if r[iP] is None:
        continue
    p = norm.get(str(r[iP]).strip().upper())
    if p is None:
        continue
    if r[iT] == "Meta diária":
        meta[p] = float(r[iV])
    elif r[iT] == "Dias úteis":
        uteis[p] = int(r[iV])

# --- fProducao (tabela mb51_coois, aba MB51: A1:Z115926)
ws = wb["MB51"]
it = ws.iter_rows(values_only=True)
cab = list(next(it))
iM, iD, iQ, iU = (cab.index(c) for c in ("MRP controller", "Posting Date", "Qty in unit of entry", "Unit of Entry"))
soma = collections.defaultdict(float)     # (data, produto) -> qtd
for r in it:
    if r[iD] is None or r[iM] is None:
        continue
    prod = MRP.get(str(r[iM]).strip())
    if prod is None or r[iU] == "KG":
        continue
    d = r[iD]
    d = d.date() if isinstance(d, dt.datetime) else d
    soma[(d, prod)] += float(r[iQ] or 0)

# --- regras
datas = sorted({d for d, _ in soma})
corte = max(d for d in datas if d < hoje)
mes = (corte.year, corte.month)
dias = [d for d in datas if (d.year, d.month) == mes and d <= corte]
n = len(dias)


def br(v, c):
    s = f"{v:,.{c}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


print(f"hoje={hoje:%d/%m/%Y} corte={corte:%d/%m/%Y} mês={mes[1]:02d}/{mes[0]} dias contabilizados={n}: "
      + ", ".join(f"{d:%d}" for d in dias))
for p in ORDEM:
    md, du, c, u = meta[p], uteis[p], CASAS[p], UN[p]
    serie = [soma.get((d, p), 0.0) for d in dias]
    prod = sum(serie)
    macum = md * n
    saldo = prod - macum
    pct = prod / macum if macum else None
    rest = du - n
    ritmo = (md * du - prod) / rest if rest > 0 else None
    print(f"\n{p}: meta diária {br(md,0)} {u} | dias úteis {du} | dias contabilizados {n}")
    print(f"  produzido {br(prod,c)} {u} | meta acumulada {br(macum,0)} | saldo {br(saldo,c)} | "
          f"% da meta {br(pct*100,1) if pct is not None else '-'}% | feliz={saldo >= 0}")
    print(f"  dias que faltam {rest} | ritmo para fechar "
          f"{br(ritmo,c) + ' ' + u + '/dia' if ritmo is not None else '-'}")
    print("  série diária: " + "  ".join(f"{d:%d/%m}={br(v,c)}" for d, v in zip(dias, serie)))
