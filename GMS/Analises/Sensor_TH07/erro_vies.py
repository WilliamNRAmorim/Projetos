"""Erro médio absoluto e viés do tempo parado do Hora-Hora contra o sensor da TH07 (01 a 15/10/2026).

Compara duas versões do tempo parado com o sensor (paradas >= 1 min):
  digitado  = Tempo Parado (min) que o operador lançou
  derivado  = regra publicada em 29/10 (MEL-255): Minutos x (Meta - Real) / Meta; Real 0 = janela inteira.
              Meta vem da velocidade teórica da máquina e Real do metrador.
Viés = sensor - GMS (positivo: o GMS aponta parada a menos).
Só leitura. Uso: python -I erro_vies.py
"""
import csv
import statistics as st
from pathlib import Path

AQUI = Path(__file__).resolve().parent
HH = AQUI.parent / "Higienizacao_HoraHora" / "HoraHora_backup_2026-09-01_a_2026-10-15.csv"
CMP = AQUI / "Comparacao_HoraHora_TH07_2026-10-01_a_15.csv"

hh = {}
with open(HH, encoding="utf-8-sig") as f:
    for x in csv.DictReader(f):
        if x["Celula"] == "TH07":
            k = (x["Title"].split(" - ")[0], x["Turno"][0], x["Hora"].replace(" ", ""))
            hh.setdefault(k, x)

linhas = []
with open(CMP, encoding="utf-8-sig") as f:
    for c in csv.DictReader(f):
        x = hh[(c["data"], c["turno"], c["hora"].replace(" ", ""))]
        meta, real = float(x["Meta Hora"] or 0), float(x["Real. Hora"] or 0)
        mins = float(x["Minutos"] or 60)
        der = mins if real <= 0 else max(0.0, min(mins, mins * (meta - real) / meta))
        linhas.append({"turno": c["turno"], "status": c["status"], "sensor": float(c["fb_ge1"]),
                       "digitado": float(c["gms_parado"]), "derivado": der})


def medir(sel, campo):
    e = [r["sensor"] - r[campo] for r in sel]
    return f"{st.mean(abs(v) for v in e):.1f} | {st.mean(e):+.1f}"


grupos = [("1º e 2º turnos fechados", [r for r in linhas if r["status"] == "Finalizado"]),
          ("3º turno", [r for r in linhas if r["turno"] == "3"]),
          ("Todas as horas", linhas)]
print("Grupo | Horas | Digitado: erro médio (min) | viés | Derivado: erro médio (min) | viés")
for nome, sel in grupos:
    print(f"{nome} | {len(sel)} | {medir(sel, 'digitado')} | {medir(sel, 'derivado')}")
