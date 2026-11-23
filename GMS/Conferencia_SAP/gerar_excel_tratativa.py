# Gera ProdHose_Tratativa_2026-11-23.xlsx: o que está parado na PROD-GR-HOSE e o que fazer com cada item.
# Fonte: saldo colado pelo William em 23/11 (Analises/Conferencia_SAP_Correcoes/prodhose_2026-11-23.csv),
# lista Conferencia_SAP e Packing_Pallets lidas pela API em 23/11.
import csv
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

AQUI = Path(__file__).resolve().parent
SALDO = AQUI.parent / "Analises" / "Conferencia_SAP_Correcoes" / "prodhose_2026-11-23.csv"
SAIDA = AQUI / "ProdHose_Tratativa_2026-11-23.xlsx"

F = "Arial"
H = Font(name=F, bold=True, color="FFFFFF")
FILL_H = PatternFill("solid", fgColor="1E293B")
FILL_OK = PatternFill("solid", fgColor="D1FAE5")
FILL_PEND = PatternFill("solid", fgColor="FEF3C7")
FILL_SAP = PatternFill("solid", fgColor="FEE2E2")
B = Border(bottom=Side(style="thin", color="E2E8F0"))
N = "#,##0.0"

# OP, PN no deposito, metros, situacao, o que o Claude ja fez, o que falta, quem, status
ITENS = [
    ("30750671", "GH493-16", 166.6, "8 lances recriados em 13/11 (21391-21398) já lançados no SAP e sem pallet no GMS",
     "Pallet 2 registrado (Packing_Pallets 531, 8 lances, 166,6 m)", "Conferir no físico antes: o depósito só tem 110,3 m de GH493-16 contra 218,7 m pendentes. O que existir: imprimir o pallet 2 em Consulta de OP > Packlists da OP e transferir", "Cabine + Logística", "Imprimir e transferir"),
    ("30750671", "GH493-16", 52.1, "Lance 20905 corrigido de 1,0 m para 53,1 m em 13/11; o pallet 1 saiu impresso com 1,0 m",
     "Pallet 1 (374) corrigido para TotalM 53,1 m", "Reimprimir o pallet 1 em Consulta de OP e transferir os 52,1 m que faltaram", "Cabine + Logística", "Imprimir e transferir"),
    ("30575954", "HC139-7_S-GX", 145.5, "3 lances recriados em 18/11 (21776-21778) sem pallet",
     "Pallet 2 registrado (532, 3 lances, 145,5 m)", "Imprimir o pallet 2 e transferir", "Cabine + Logística", "Imprimir e transferir"),
    ("30619643", "FC735-12", 106.1, "Lance recriado em 18/11 (21779) sem pallet",
     "Pallet 2 registrado (533, 106,1 m)", "Imprimir o pallet 2 e transferir", "Cabine + Logística", "Imprimir e transferir"),
    ("30829741", "GH781-8", 73.4, "Lance recriado em 18/11 (21786) sem pallet",
     "Pallet 3 registrado (534, 73,4 m)", "Conferir no físico antes: o depósito tem 74,5 m de GH781-8 contra 88,8 m pendentes (esta OP + 30800824). Depois imprimir o pallet 3 e transferir", "Cabine + Logística", "Imprimir e transferir"),
    ("30770798", "GH493-8", 40.7, "Lance recriado em 18/11 (21783) sem pallet",
     "Pallet 3 registrado (535, 40,7 m)", "Imprimir o pallet 3 e transferir", "Cabine + Logística", "Imprimir e transferir"),
    ("30690631", "GH781-4", 37.0, "Lance recriado em 18/11 (21781) sem pallet",
     "Pallet 2 registrado (536, 37,0 m)", "Imprimir o pallet 2 e transferir", "Cabine + Logística", "Imprimir e transferir"),
    ("30575840", "GH781-4", 35.4, "Lance recriado em 18/11 (21780) sem pallet",
     "Pallet 2 registrado (537, 35,4 m)", "Imprimir o pallet 2 e transferir", "Cabine + Logística", "Imprimir e transferir"),
    ("30751352", "FC839B-06", 28.9, "Lance recriado em 18/11 (21784) sem pallet",
     "Pallet 2 registrado (538, 28,9 m)", "Imprimir o pallet 2 e transferir", "Cabine + Logística", "Imprimir e transferir"),
    ("30749038", "EC415-16", 26.1, "Lance recriado em 18/11 (21782) sem pallet",
     "Pallet 3 registrado (539, 26,1 m)", "Imprimir o pallet 3 e transferir", "Cabine + Logística", "Imprimir e transferir"),
    ("30800824", "GH781-8", 15.4, "Lance recriado em 18/11 (21785) sem pallet",
     "Pallet 2 registrado (540, 15,4 m)", "Imprimir o pallet 2 e transferir", "Cabine + Logística", "Imprimir e transferir"),
    ("30860262", "GH781-4", 129.1, "O SAP lançou na OP 30860262 o lance 21902 (129,1 m), que pertence à OP 30885825 (ficha de 1.080 m, pallet 2). O GMS está certo",
     "Nada no GMS (o GMS está certo; o material está no pallet 2 da 30885825)", "SAP: estornar (102) o doc 3031623382 na OP 30860262 e lançar 101 de 129,1 m na OP 30885825", "SAP / PCP", "Corrigir no SAP"),
    ("30803594", "GH781-4", 15.3, "O SAP tem 15,3 m de produção boa a mais que o GMS (pendência 321)",
     "Nada (não dá para saber pelo sistema se o material existe)", "Conferir no físico: se não existe, estornar no SAP; se existe, apontar o lance no GMS", "Supervisão / SAP", "Conferir no físico"),
    ("30482097", "-", 66.8, "OP lançada no SAP em 08/10 (doc 3027688835, U395488) que o GMS não tem",
     "Nada (OP da transição de outubro, fora do indicador desde a v1.3.1)", "Conferir se ainda está na PROD-GR-HOSE; se estiver, achar o pallet ou estornar", "Supervisão / SAP", "Conferir no físico"),
    ("Refugo 20-23/11", "vários", 39.6, "Lote de refugo lançado no SAP na sexta/segunda (EC115-16L 15,9; GH781-10 7,5; FC735-10 5,7; GH681-4 4,5; GH493-16 3,5; FC839B-06 2,5)",
     "Nada", "Dar baixa do refugo na PROD-GR-HOSE", "Qualidade / SAP", "Baixa de refugo"),
]


def cab(ws, linha, titulos, larg):
    for i, (t, w) in enumerate(zip(titulos, larg), 1):
        c = ws.cell(row=linha, column=i, value=t)
        c.font, c.fill = H, FILL_H
        c.alignment = Alignment(vertical="center", wrap_text=True)
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = ws.cell(row=linha + 1, column=1)


def main():
    saldo = {}
    with open(SALDO, encoding="utf-8-sig") as f:
        for r in csv.reader(f, delimiter=";"):
            if len(r) < 2 or r[0].lower().startswith("mat"):
                continue
            saldo[r[0]] = saldo.get(r[0], 0) + float(r[1].replace(",", "."))

    wb = Workbook()
    rs = wb.active
    rs.title = "Resumo"
    tr = wb.create_sheet("Tratar")
    sd = wb.create_sheet("Saldo PROD-GR-HOSE")

    # Tratar
    tit = ["OP", "Material no depósito", "Metros", "Situação", "O que já foi feito no GMS (23/11)", "O que falta fazer", "Quem", "Status"]
    cab(tr, 1, tit, [16, 18, 10, 60, 45, 60, 20, 20])
    for i, it in enumerate(ITENS, 2):
        for j, v in enumerate(it, 1):
            c = tr.cell(row=i, column=j, value=v)
            c.font = Font(name=F)
            c.alignment = Alignment(vertical="top", wrap_text=True)
            c.border = B
        tr.cell(row=i, column=3).number_format = N
        fill = FILL_PEND if it[7] == "Imprimir e transferir" else FILL_SAP
        tr.cell(row=i, column=8).fill = fill
    ult = len(ITENS) + 1

    # Saldo por material
    cab(sd, 1, ["Material", "Saldo 23/11 (m)", "Explicado pela aba Tratar (m)", "Resto (m)", "Atenção"], [18, 16, 26, 12, 60])
    for i, (m, q) in enumerate(sorted(saldo.items()), 2):
        sd.cell(row=i, column=1, value=m).font = Font(name=F)
        c = sd.cell(row=i, column=2, value=round(q, 3)); c.font = Font(name=F, color="0000FF"); c.number_format = N
        c = sd.cell(row=i, column=3, value=f"=SUMIFS(Tratar!$C$2:$C${ult},Tratar!$B$2:$B${ult},A{i})"); c.font = Font(name=F); c.number_format = N
        c = sd.cell(row=i, column=4, value=f"=B{i}-C{i}"); c.font = Font(name=F); c.number_format = N
        c = sd.cell(row=i, column=5, value=f'=IF(D{i}<-0.5,"Depósito tem menos que o pendente: conferir no físico antes de imprimir","")')
        c.font = Font(name=F, bold=True, color="C0392B")
    us = len(saldo) + 1
    t = us + 1
    sd.cell(row=t, column=1, value="Total").font = Font(name=F, bold=True)
    for col in "BCD":
        c = sd[f"{col}{t}"]; c.value = f"=SUM({col}2:{col}{us})"; c.font = Font(name=F, bold=True); c.number_format = N
    sd.cell(row=t + 2, column=1, value="Saldo (azul) colado pelo William em 23/11 da PROD-GR-HOSE (EWM 9015). 'Resto' é produção do dia aguardando transferência, refugo antigo ou estoque sem pendência aberta (ex.: EC215-08LRL 1.024,6 m desde 03/08).").font = Font(name=F, italic=True, color="64748B")

    # Resumo
    rs.column_dimensions["A"].width = 52
    rs.column_dimensions["B"].width = 16
    rs["A1"] = "PROD-GR-HOSE: tratativa de 23/11/2026"; rs["A1"].font = Font(name=F, bold=True, size=14)
    linhas = [
        ("Saldo total na PROD-GR-HOSE (m)", f"='Saldo PROD-GR-HOSE'!B{t}"),
        ("Pendências para tratar (m)", f"=SUM(Tratar!C2:C{ult})"),
        ("  Imprimir pallet e transferir (m)", f'=SUMIFS(Tratar!C2:C{ult},Tratar!H2:H{ult},"Imprimir e transferir")'),
        ("  Corrigir no SAP (m)", f'=SUMIFS(Tratar!C2:C{ult},Tratar!H2:H{ult},"Corrigir no SAP")'),
        ("  Conferir no físico (m)", f'=SUMIFS(Tratar!C2:C{ult},Tratar!H2:H{ult},"Conferir no físico")'),
        ("  Baixa de refugo (m)", f'=SUMIFS(Tratar!C2:C{ult},Tratar!H2:H{ult},"Baixa de refugo")'),
        ("Entrou algo novo sem pallet desde 19/11?", "Não"),
    ]
    for i, (a, b) in enumerate(linhas, 3):
        rs.cell(row=i, column=1, value=a).font = Font(name=F)
        c = rs.cell(row=i, column=2, value=b); c.font = Font(name=F, bold=True); c.number_format = N
    rs["A11"] = ("Torneira: os 112 lances do GMS de 19/11 a 23/11 estão todos em pallet (exceto 1 lance de hoje, OP 30900102, ainda em produção). "
                 "O que subiu no saldo foi o pallet de hoje da OP 30860018 (GH781-12, 325,1 m, aguardando transferência) e o lote de refugo. "
                 "O lado do SAP será confirmado pela conferência de 24/11 (o mb51.xlsx não foi salvo desde 20/11).")
    rs["A13"] = ("Os pallets novos (IDs 531 a 540) foram registrados no GMS em 23/11 para os lances recriados nas correções de 13 e 18/11. "
                 "Na cabine: Consulta de OP > escolher a OP > Packlists da OP > imprimir o pallet indicado na aba Tratar.")
    for cel in ("A11", "A13"):
        rs[cel].font = Font(name=F, color="334155")
        rs[cel].alignment = Alignment(wrap_text=True, vertical="top")
        rs.merge_cells(f"{cel}:{cel.replace('A', 'B')}")
        rs.row_dimensions[int(cel[1:])].height = 75
    wb.save(SAIDA)
    print(SAIDA)


if __name__ == "__main__":
    main()
