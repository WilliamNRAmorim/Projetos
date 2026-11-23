# -*- coding: utf-8 -*-
"""Gera nov_2026_lista.csv (linhas da lista GMS_PlanoMangueira) a partir da aba Dados da planilha do planejamento.
Regra: Volume > 0, mais as mangueiras com Volume vazio/0 que tiveram produção no mês (a classificação precisa existir
para a produção não cair em 'Fora do plano'). Linhas sem classificação (C.Standard/Tipo/Arame vazios) ficam de fora."""
import sys, csv, collections, datetime as dt
import openpyxl
sys.stdout.reconfigure(encoding="utf-8")
ARQ = r"C:\Users\U445131\Downloads\Novembro-10.xlsm"
MES = dt.date(2026, 11, 1)
wb = openpyxl.load_workbook(ARQ, read_only=True, data_only=True)
prod = collections.defaultdict(float)
for r in wb["MB51"].iter_rows(min_row=2, values_only=True):
    if r[0] is not None and isinstance(r[9], dt.datetime) and MES <= r[9].date() <= dt.date(2026, 11, 30) and str(r[11]).strip().upper() == "M":
        prod[str(r[0]).strip().upper()] += float(r[10] or 0)
out, pulou = [], []
for r in wb["Dados"].iter_rows(min_row=58, max_row=160, min_col=3, max_col=11, values_only=True):
    mang, cs, _d, arame, _b, tipo, _m, _h, vol = r
    if mang is None or not str(mang).strip():
        continue
    mang = str(mang).strip(); vol = float(vol or 0); p = prod.get(mang.upper(), 0.0)
    if not (cs and tipo and arame):
        pulou.append((mang, vol, p)); continue
    if vol > 0 or abs(p) > 1e-9:
        out.append([mang, MES.isoformat(), cs, tipo, arame, f"{vol:g}"])
with open("nov_2026_lista.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f); w.writerow(["Title", "Mes", "CStandard", "Tipo", "Arame", "Volume"]); w.writerows(out)
print(len(out), "linhas; volume total", sum(float(x[5]) for x in out), "| sem classificação (fora):", pulou)
