"""Funções para ler e cruzar os dados de conferência SAP x GMS (refugo e produção boa).

Uso:  python gms_dados.py                      # período padrão 16/05 a 16/09/2026
      python gms_dados.py 2026-05-01 2026-05-31
Veja COMO_USAR_OS_DADOS.md para as regras e os cuidados.
"""
import collections
import datetime as dt
import re
import sys
from pathlib import Path

import openpyxl

GMS = Path(__file__).resolve().parents[2]
RELATORIO = GMS / "Relatorio_Conferencia_MB51_v3_2.xlsx"
ALINHADO = GMS / "Analises" / "Refugo_SAP_vs_GMS" / "Refugo_GMS_alinhado_ao_SAP.xlsx"
USUARIOS_REFUGO = {"U445131", "U452021"}  # lançam refugo (101) na MB51


def norm_material(desc):
    """'HOSE-AER, GH781, -6, R2/2SC' -> 'GH781-6'; 'HOSE-WIN, EC118, -4L, R17' -> 'EC118-04L'."""
    m = re.match(r"HOSE-\w+,\s*([A-Z0-9]+),\s*-(\d+L?),", str(desc).strip())
    if not m:
        return str(desc).strip()
    fam, sz = m.groups()
    if sz.endswith("L"):
        sz = sz[:-1].zfill(2) + "L"
    elif fam.startswith("FC"):
        sz = sz.zfill(2)
    return f"{fam}-{sz}"


def _limites(ini, fim):
    return (dt.datetime.combine(ini, dt.time.min), dt.datetime.combine(fim, dt.time.max))


def producao_boa_sap(ini, fim):
    """Metros bons por dia e por material na MB51: 101 menos 102, só unidade M, sem refugo."""
    a, b = _limites(ini, fim)
    wb = openpyxl.load_workbook(RELATORIO, read_only=True, data_only=True)
    por_dia, por_mat = collections.defaultdict(float), collections.defaultdict(float)
    for r in wb["MB51"].iter_rows(min_row=2, values_only=True):
        d, mvt, un, qtd, usr = r[9], r[5], r[11], r[14], r[15]
        if not isinstance(d, dt.datetime) or not a <= d <= b or qtd is None:
            continue
        if un != "M" or mvt not in (101, 102) or usr in USUARIOS_REFUGO:
            continue
        por_dia[d.date()] += qtd
        por_mat[norm_material(r[2])] += qtd
    return por_dia, por_mat


def linhas_refugo(ini, fim):
    """Linhas de ajuste de refugo (SAP - GMS) no período: (data, op, material, ação, variação em m).
    Data = data do SAP quando existe; senão a criação no GMS."""
    a, b = _limites(ini, fim)
    wb = openpyxl.load_workbook(ALINHADO, data_only=True)
    mat = {r[0]: norm_material(r[1]) for r in wb["Por OP"].iter_rows(min_row=2, values_only=True)}
    out = []
    for r in wb["Ajustes"].iter_rows(min_row=2, values_only=True):
        op, acao, var = r[0], r[1], r[7]
        d = r[9] or r[3]  # Data SAP ou Criado em (GMS)
        if a <= d <= b:
            out.append((d.date(), op, mat[op], acao, var))
    return out


def faltou_sobrou(linhas, chave=lambda l: l[2]):
    """Soma a variação por chave (padrão: material) e separa o que faltou (<0) do que sobrou (>0).
    Material não compensa com material; dentro da mesma chave o saldo é líquido."""
    saldo = collections.defaultdict(float)
    for l in linhas:
        saldo[chave(l)] += l[4]
    faltou = sum(-v for v in saldo.values() if v < -0.005)
    sobrou = sum(v for v in saldo.values() if v > 0.005)
    return faltou, sobrou, dict(saldo)


def ppm(erro_m, producao_m):
    return erro_m / producao_m * 1e6 if producao_m else None


if __name__ == "__main__":
    ini = dt.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 2 else dt.date(2026, 5, 16)
    fim = dt.date.fromisoformat(sys.argv[2]) if len(sys.argv) > 2 else dt.date(2026, 9, 16)
    dia, _ = producao_boa_sap(ini, fim)
    lin = linhas_refugo(ini, fim)
    f, s, _ = faltou_sobrou(lin)
    prod = sum(dia.values())
    print(f"{ini} a {fim}: {len(lin)} linhas de ajuste")
    print(f"faltou {f:,.1f} m | sobrou {s:,.1f} m | total {f + s:,.1f} m")
    print(f"produção boa SAP {prod:,.0f} m | PPM {ppm(f + s, prod):,.0f}")
