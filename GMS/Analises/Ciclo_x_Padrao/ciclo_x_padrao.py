"""Ciclo medido no GMS x tempo padrão da Engenharia, por etapa (TCC II, seção 4.3).

Ciclo medido = data_hora_final - data_hora_inicio da etapa, por OP (ficha_producao.csv).
Tempo padrão = metragem da etapa / velocidade de delineamento (DM_*), em minutos.
  Tubo       -> DM_TUBE_EXTRUSION.SPEEDY_mpm (m/min), pela mangueira
  Cobertura  -> DM_EXTRUSAO_COBERTURA.SPEEDY_mpm (m/min), pela mangueira
  Trançagem  -> DM_ENGRENAGENS._13TEORICA_M_H (m/h), pela máquina + construção (DM_TRANÇAGEM._2BRD_CODE, como o app)
                (máquinas de duas passadas, TH01 e TO04, ficam fora)
Só leitura. Uso: python -I ciclo_x_padrao.py  (grava ciclo_x_padrao.csv e imprime o resumo)
"""
import csv
import re
import statistics as st
from datetime import datetime
from pathlib import Path

import openpyxl

GMS = Path(__file__).resolve().parents[2]
FICHA = GMS / "Sharepoint Data GMS" / "ficha_producao.csv"
DM = GMS / "Engenharia" / "DM_DATABASE"
SAIDA = Path(__file__).with_name("ciclo_x_padrao.csv")


def norm(s):
    return re.sub(r"[^A-Z0-9]", "", str(s or "").upper())


def num(s):
    s = str(s or "").strip().replace("'", "").replace(",", ".")
    m = re.match(r"^-?\d+(\.\d+)?", s)
    return float(m.group(0)) if m else None


def data(s):
    s = (s or "").strip()
    for f in ("%m/%d/%Y %I:%M %p", "%m/%d/%Y %H:%M", "%Y-%m-%dT%H:%M:%SZ"):
        try:
            return datetime.strptime(s, f)
        except ValueError:
            pass
    return None


def tabela(nome):
    ws = openpyxl.load_workbook(DM / nome, read_only=True, data_only=True).active
    linhas = list(ws.iter_rows(values_only=True))
    h = [str(c) if c is not None else "" for c in linhas[0]]
    return [dict(zip(h, r)) for r in linhas[1:]]


vel_tubo = {norm(r["PARTNUMBER"]): num(r["SPEEDY_mpm"]) for r in tabela("DM_TUBE_EXTRUSION.xlsx")}
vel_cob = {norm(r["PARTNUMBER"]): num(r["SPEEDY_mpm"]) for r in tabela("DM_EXTRUSAO_COBERTURA.xlsx")}
construcao = {norm(r["PARTNUMBER"]): norm(r["_2BRD_CODE"]) for r in tabela("DM_TRANÇAGEM.xlsx")}
vel_tr = {}
duas = set()
for r in tabela("DM_ENGRENAGENS.xlsx"):
    k = (norm(r["_4MAQUINA"]), norm(r["_1CONSTRUCAO"]))
    vel_tr[k] = num(r["_13TEORICA_M_H"])
    if "DUAS PASSADAS" in str(r.get("_15OBSERVACAO") or "").upper():
        duas.add(k)

ETAPAS = [
    ("Tubo", "data_hora_inicio_tubo", "data_hora_final_tubo", "quantidade_tubo"),
    ("Trançagem", "data_hora_inicio_trancadeira", "data_hora_final_trancadeira", "quantidade_trancagem"),
    ("Cobertura", "data_hora_inicio_cobertura", "data_hora_final_cobertura", "quantidade_cobertura"),
]

saida = []
descartes = {}
with open(FICHA, encoding="utf-8-sig") as f:
    for r in csv.DictReader(f):
        mang = norm(r.get("Mangueira"))
        for etapa, ci, cf, cq in ETAPAS:
            ini, fim, q = data(r.get(ci)), data(r.get(cf)), num(r.get(cq))
            if not (ini and fim and q and q > 0):
                continue
            ciclo = (fim - ini).total_seconds() / 60
            if etapa == "Tubo":
                v = vel_tubo.get(mang)
                padrao = q / v if v else None
            elif etapa == "Cobertura":
                v = vel_cob.get(mang)
                padrao = q / v if v else None
            else:
                k = (norm(r.get("Trançadeira")), construcao.get(mang, ""))
                v = vel_tr.get(k)
                padrao = q / v * 60 if v and k not in duas else None
            if padrao is None:
                descartes[etapa] = descartes.get(etapa, 0) + 1
                continue
            if ciclo <= 0:
                descartes[etapa + " (ciclo <= 0)"] = descartes.get(etapa + " (ciclo <= 0)", 0) + 1
                continue
            saida.append({"etapa": etapa, "id": r["ID"], "mangueira": r.get("Mangueira"),
                          "inicio": ini.isoformat(), "metros": q, "ciclo_min": round(ciclo, 1),
                          "padrao_min": round(padrao, 1), "razao": round(ciclo / padrao, 3)})

with open(SAIDA, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(saida[0]))
    w.writeheader()
    w.writerows(saida)

print("Etapa | OPs | Ciclo mediano (min) | Padrão mediano (min) | Diferença | Razão mediana | P90 razão | Período")
for etapa, *_ in ETAPAS:
    s = [x for x in saida if x["etapa"] == etapa]
    if not s:
        print(etapa, "sem dado")
        continue
    c = st.median(x["ciclo_min"] for x in s)
    p = st.median(x["padrao_min"] for x in s)
    rz = sorted(x["razao"] for x in s)
    p90 = rz[int(0.9 * (len(rz) - 1))]
    datas = sorted(x["inicio"][:10] for x in s)
    print(f"{etapa} | {len(s)} | {c:.0f} | {p:.0f} | {c - p:+.0f} ({(c / p - 1) * 100:+.0f}%) | "
          f"{st.median(rz):.2f} | {p90:.2f} | {datas[0]} a {datas[-1]}")
print("Descartes (sem velocidade no delineamento ou ciclo inválido):", descartes)
