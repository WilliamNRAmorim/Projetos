# -*- coding: utf-8 -*-
"""Extrai as planilhas de Eficiencia (uma aba por dia) para dois CSV:
dados/eficiencia_maquina.csv (trancadeira x turno) e dados/eficiencia_etapa.csv (etapa x turno).
Uso: python extrair_eficiencia.py"""
import csv, glob, os, re, warnings, datetime as dt
import openpyxl
warnings.filterwarnings("ignore")
AQUI = os.path.dirname(os.path.abspath(__file__))
FONTE = os.path.join(AQUI, "..", "..", "Dados_Historicos", "Eficiencia_Processo", "2026")
MESES = {"Jan": 1, "Fev": 2, "Mar": 3, "Abr": 4, "Mai": 5, "Jun": 6, "Jul": 7, "Ago": 8, "Set": 9, "Out": 10, "Nov": 11, "Dez": 12}
ETAPAS = {"solda mandril": "mandril", "extrusora 1": "tubo", "trançadeiras": "trancagem", "extrusora 2": "cobertura",
          "bandagem": "bandagem", "debandagem": "debandagem", "extração": "extracao", "extrusora 3": "extrusora3",
          "bobinadeira 1": "bobinadeira1", "bobinadeira 2": "bobinadeira2"}

def num(v):
    return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else None

def txt(v):
    return "" if v is None else re.sub(r"\s+", " ", str(v)).strip()

def ler_aba(ws, ano, mes):
    linhas = [list(r) for r in ws.iter_rows(min_row=1, max_row=60, max_col=27, values_only=True)]
    if not linhas or not ws.title.strip().isdigit():
        return None, [], []
    dia = int(ws.title)
    try:
        data = dt.date(ano, mes, dia)
    except ValueError:
        return None, [], []
    cab = next((i for i, r in enumerate(linhas) if sum(1 for v in r if txt(v) == "Hs") >= 2), None)
    if cab is None:
        return data, [], []
    hs_cols = [j for j, v in enumerate(linhas[cab]) if txt(v) == "Hs"][:3]
    maq, etp = [], []
    for r in linhas[cab + 1:]:
        nome = txt(r[hs_cols[0] - 1])
        if txt(r[hs_cols[0]]).lower() in ETAPAS:
            break
        if not re.match(r"^(T[HMO]\s?\d+|Spiral)$", nome, re.I):
            continue
        for t, c in enumerate(hs_cols, 1):
            hs, hose, pd_, plan, real = num(r[c]), txt(r[c + 1]), num(r[c + 2]), num(r[c + 3]), num(r[c + 4])
            motivo = txt(r[c + 6]) if c + 6 < len(r) else ""
            if hose or (real or 0) > 0 or motivo:
                maq.append([data, t, nome.upper().replace(" ", ""), hs or "", hose, pd_ or 0, round(plan or 0, 1), real or 0, motivo])
    if True:  # bloco por etapa: qualquer linha abaixo do cabecalho com o nome da etapa na coluna "Hs"
        for r in linhas[cab + 1:]:
            nome = ETAPAS.get(txt(r[hs_cols[0]]).lower())
            if not nome:
                continue
            for t, c in enumerate(hs_cols, 1):
                plan, real = num(r[c + 2]), num(r[c + 4])
                etp.append([data, t, nome, plan or 0, real or 0])
    return data, maq, etp

def main():
    maq_all, etp_all, dias = [], [], 0
    for p in sorted(glob.glob(os.path.join(FONTE, "Eficiencia-*.xlsx"))):
        m = re.search(r"Eficiencia-([A-Za-z]{3})(\d{4})", os.path.basename(p))
        mes, ano = MESES[m.group(1)], int(m.group(2))
        wb = openpyxl.load_workbook(p, data_only=True, read_only=True)
        n0 = len(etp_all)
        for ws in wb.worksheets:
            data, maq, etp = ler_aba(ws, ano, mes)
            if data and etp:
                dias += 1
                maq_all += maq; etp_all += etp
        wb.close()
        print(f"{os.path.basename(p)}: linhas etapa {len(etp_all) - n0}")
    out = os.path.join(AQUI, "dados"); os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "eficiencia_maquina.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["data", "turno", "maquina", "horas", "mangueira", "vel_m_h", "planejado", "real", "motivo"]); w.writerows(maq_all)
    with open(os.path.join(out, "eficiencia_etapa.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["data", "turno", "etapa", "planejado", "real"]); w.writerows(etp_all)
    print(f"abas lidas: {dias}; linhas maquina: {len(maq_all)}; linhas etapa: {len(etp_all)}")

if __name__ == "__main__":
    main()
