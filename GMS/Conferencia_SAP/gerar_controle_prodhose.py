# Gera ProdHose_Controle.xlsx (controle da PROD-GR-HOSE com historico). Nao sobrescreve: depois de criado, o arquivo e do William.
import csv, sys
from datetime import datetime
from pathlib import Path
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as L
from openpyxl.formatting.rule import FormulaRule
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.chart import BarChart, Reference

AQUI = Path(__file__).resolve().parent
COR = AQUI.parent / "Analises" / "Conferencia_SAP_Correcoes"
EXP = AQUI.parent / "Analises" / "ProdHose_Teste" / "EXPORT_20261124_140928.xlsx"
SAIDA = Path(sys.argv[1]) if len(sys.argv) > 1 else AQUI / "ProdHose_Controle.xlsx"
if SAIDA.exists():
    sys.exit(f"{SAIDA} ja existe: apague ou mude de nome antes (tem registro do usuario).")

F = "Arial"
AZ, CINZA, FUNDO = "1E293B", "64748B", "F1F5F9"
fH, fN, fB = Font(name=F, bold=True, color="FFFFFF", size=10), Font(name=F, size=10), Font(name=F, size=10, bold=True)
fI = Font(name=F, size=10, color="0000FF")
H, EDIT = PatternFill("solid", fgColor=AZ), PatternFill("solid", fgColor="FFFBEB")
VERM, AMAR, VERD = (PatternFill("solid", bgColor=c) for c in ("FEE2E2", "FEF3C7", "D1FAE5"))
LIN = Border(bottom=Side(style="thin", color="E2E8F0"))
N, D = "#,##0.0;-#,##0.0;-", "dd/mm/yyyy"
NH, NT, NF, NM, NS = 3000, 120, 30, 120, 1500     # linhas: historico, pendencias, fotos, materiais, SAP


def ld(nome):
    d = {}
    for r in csv.reader(open(COR / nome, encoding="utf-8-sig"), delimiter=";"):
        try:
            v = float(r[1].replace(".", "").replace(",", ".")) if "," in r[1] else float(r[1])
        except Exception:
            continue
        d[r[0]] = d.get(r[0], 0) + v
    return d


def aba(wb, nome, titulo, sub, cab, larg, linha=4):
    ws = wb.create_sheet(nome)
    ws.sheet_view.showGridLines = False
    ws["A1"], ws["A2"] = titulo, sub
    ws["A1"].font, ws["A2"].font = Font(name=F, bold=True, size=14, color=AZ), Font(name=F, size=9, color=CINZA)
    for i, (t, w) in enumerate(zip(cab, larg), 1):
        c = ws.cell(linha, i, t)
        c.font, c.fill, c.alignment = fH, H, Alignment(wrap_text=True, vertical="center")
        ws.column_dimensions[L(i)].width = w
    ws.row_dimensions[linha].height = 32
    ws.freeze_panes = ws.cell(linha + 1, 1)
    return ws


def put(ws, r, c, v, fmt=None, font=fN, fill=None, wrap=False):
    x = ws.cell(r, c, v)
    x.font, x.border, x.alignment = font, LIN, Alignment(vertical="top", wrap_text=wrap)
    if fmt: x.number_format = fmt
    if fill: x.fill = fill
    return x


def lista(ws, ref, itens):
    dv = DataValidation(type="list", formula1=itens if itens.startswith("=") else f'"{itens}"', allow_blank=True)
    ws.add_data_validation(dv); dv.add(ref)


dt = lambda d: datetime(2026, 11, d)
FOTOS = [(18, "Saldo colado; sem separar tipo de estoque"), (19, "Saldo colado; sem separar tipo de estoque"),
         (23, "Saldo colado; sem separar tipo de estoque"), (24, "Export das 10:09 (hora de Brasília)")]
# MB51 lido em 24/11 05:24 (GRT4, unidade M, 101-102). B = boa, R = refugo (U452021/U445131)
SAP = {"EC115-06L": "20B691.6 23R5.6", "EC115-12L": "19B396.4", "EC115-16L": "17B238.4 17R1.5 19R15.9", "EC118-04L": "17R53.28",
       "EC118-06L": "18B622.5 19B700.5 19R30.5", "EC118-08L": "19B559.2 17R2 19R1.5", "EC118-16L": "17R5", "FC735-08": "24B989.6",
       "EC215-12L": "19B774.2 23R12.16", "FC735-10": "17B927.7 19R5.7 23B595.6 24B301.6", "FC839B-06": "19R2.5",
       "GH493-16": "17B202.7 19R3.5", "GH493-8": "17B505.2 18B996.5 19R12.75", "GH493-12": "17B1227.7 17R7.5",
       "GH681-4": "17B688.8 19R4.5", "GH681-6": "23B729.1", "GH781-10": "17R11.4 19R7.5 23B472.5",
       "GH781-4": "17B1680.6 18B500.9 19B1878.6 19R12.4 23B818.7 23R9.1",
       "GH781-12": "17B374.1 17R1.8 19B1929.1 19R11.9 20B386.2 23B934.4 23R26 24B191.9",
       "GH781-6": "17R13.4 18B1274.8 19R11.6", "GH781-8": "23B497.6"}
NI = "Pallet registrado no GMS em 23/11 sem impressão. Achar o material antes de imprimir e transferir"
PEND = [  # tipo, OP, material, metros, situacao, o que fazer, quem
    ("Produção boa nova", "30915066", "GH781-12", 421.0, "Pallet 556 de 24/11 07:06. Saldo compatível; SAP ainda não conferido", "Confirmar a transferência em 25/11. Se não saiu, está preso", "Logística"),
    ("Produção boa nova", "30900107", "GH781-12", 347.6, "Pallet 557 de 24/11 09:43. Saldo compatível; SAP ainda não conferido", "Confirmar a transferência em 25/11. Se não saiu, está preso", "Logística"),
    ("Produção boa antiga", "30750671", "GH493-16", 166.6, "Pallet 531. O depósito só tem 106,8 m desse material", NI, "Cabine / Logística"),
    ("Produção boa antiga", "30750671", "GH493-16", 52.1, "Lance 20905: o packlist do pallet 1 saiu com 1,0 m e o lance tem 53,1 m", "Conferir no físico e reimprimir o pallet 1", "Cabine / Logística"),
    ("Produção boa antiga", "30575954", "HC139-7_S-GX", 145.5, "Pallet 532. Saldo do material 169,7 m, parado", NI, "Cabine / Logística"),
    ("Produção boa antiga", "30619643", "FC735-12", 106.1, "Pallet 533. Saldo livre do material 259,0 m, parado", NI, "Cabine / Logística"),
    ("Produção boa antiga", "30829741", "GH781-8", 73.4, "Pallet 534. Saldo do material 74,5 m, para 88,8 m pendentes", NI, "Cabine / Logística"),
    ("Produção boa antiga", "30770798", "GH493-8", 40.7, "Pallet 535. Saldo do material 111,4 m", NI, "Cabine / Logística"),
    ("Produção boa antiga", "30690631", "GH781-4", 37.0, "Pallet 536. Saldo do material 216,5 m", NI, "Cabine / Logística"),
    ("Produção boa antiga", "30575840", "GH781-4", 35.4, "Pallet 537. Saldo do material 216,5 m", NI, "Cabine / Logística"),
    ("Produção boa antiga", "30751352", "FC839B-06", 28.9, "Pallet 538. Saldo do material 36,8 m (2,5 m são refugo de 19/11)", NI, "Cabine / Logística"),
    ("Produção boa antiga", "30749038", "EC415-16", 26.1, "Pallet 539. Saldo do material 33,8 m", NI, "Cabine / Logística"),
    ("Produção boa antiga", "30800824", "GH781-8", 15.4, "Pallet 540. Saldo do material 74,5 m, para 88,8 m pendentes", NI, "Cabine / Logística"),
    ("Acerto no SAP", "30860262", "GH781-4", 129.1, "Lance 21902 é da OP 30885825 (ficha de 1.080 m); o SAP lançou na 30860262, doc 3031623382", "Estornar na 30860262 e lançar 101 na 30885825", "SAP / PCP"),
    ("Acerto no SAP", "30803594", "GH781-4", 15.3, "SAP com 15,3 m de produção boa a mais que o GMS", "Conferir no físico: estornar ou apontar", "Supervisão / SAP"),
    ("Acerto no SAP", "30482097", "GH681-8", 66.8, "SAP de 08/10 sem OP no GMS. O depósito só tem 6,0 m de GH681-8", "Conferir se já saiu; apontar ou estornar", "Supervisão / SAP"),
    ("Conferir packlist", "30885826", "GH781-4", 818.7, "Pallets 543, 544 e 545 com os mesmos 6 lances; o SAP lançou uma vez só", "Ver se saíram três packlists e se houve transferência repetida", "Cabine / Logística"),
    ("Refugo (cobrança à parte)", "6 OPs de 23/11", "GH781-12", 26.0, "Refugo lançado em 23/11", "Dar baixa", "Qualidade / SAP"),
    ("Refugo (cobrança à parte)", "30885835/36", "EC215-12L", 12.16, "Refugo de 23/11; é todo o saldo do material", "Dar baixa", "Qualidade / SAP"),
    ("Refugo (cobrança à parte)", "30885825/30860262", "GH781-4", 9.1, "Refugo lançado em 23/11", "Dar baixa", "Qualidade / SAP"),
    ("Refugo (cobrança à parte)", "30914923", "EC115-06L", 5.6, "Refugo de 23/11; é todo o saldo do material", "Dar baixa", "Qualidade / SAP"),
    ("Refugo (cobrança à parte)", "-", "FC839B-06", 2.5, "Refugo lançado em 19/11, ainda no saldo", "Dar baixa", "Qualidade / SAP"),
]


def main():
    hist = []
    for d, _ in FOTOS[:-1]:
        hist += [(dt(d), m, q, "Não separado", None, "") for m, q in sorted(ld(f"prodhose_2026-11-{d}.csv").items())]
    it = load_workbook(EXP, data_only=True).worksheets[0].iter_rows(values_only=True)
    cab = [str(x or "").strip() for x in next(it)]; ix = {}
    for i, n in enumerate(cab): ix.setdefault(n, i)
    for r in it:
        if r[ix["Product"]]:
            st, doc = str(r[ix["Description of Stock Type"]]), r[ix["Document Category"]]
            tipo = "Documento PDI" if doc else "Bloqueado" if "Blocked" in st else "Inspeção" if "QI" in st else "Livre"
            hist.append((dt(24), r[ix["Product"]], float(r[ix["Quantity"]]), tipo, r[ix["Goods Receipt Date"]], str(r[ix["Document"]] or "")))
    mats = sorted({h[1] for h in hist} | set(SAP))

    wb = Workbook(); wb.remove(wb.active)
    pn = wb.create_sheet("Painel")
    # Pendencias
    pe = aba(wb, "Pendências", "Pendências", "Feito e Falta calculam sozinhos pela aba Ações. Para incluir: preencha a próxima linha vazia. Amarelo = você edita.",
             ["Nº", "Tipo", "OP", "Material", "Metros", "Situação", "O que fazer", "Quem", "Aberta em", "Feito (m)", "Falta (m)", "Status", "Última ação", "Dias aberta"],
             [6, 24, 18, 16, 10, 46, 42, 19, 12, 10, 10, 13, 12, 9])
    for i in range(NT):
        r = 5 + i
        p = PEND[i] if i < len(PEND) else None
        put(pe, r, 1, f'=IF(B{r}="","",{i + 1})')
        for j in range(7):
            put(pe, r, 2 + j, p[j] if p else None, N if j == 3 else None, fI if j == 3 else fN, EDIT, j >= 4)
        put(pe, r, 9, dt(24) if p else None, D, fN, EDIT)
        put(pe, r, 10, f'=IF(B{r}="","",SUMIFS(Ações!$D$5:$D$1004,Ações!$B$5:$B$1004,A{r}))', N)
        put(pe, r, 11, f'=IF(B{r}="","",MAX(0,E{r}-J{r}))', N, fB)
        put(pe, r, 12, f'=IF(B{r}="","",IF(K{r}<=0.05,"Concluída",IF(J{r}>0,"Parcial","Pendente")))', None, fB)
        put(pe, r, 13, f'=IF(B{r}="","",IF(COUNTIFS(Ações!$B$5:$B$1004,A{r})=0,"",SUMPRODUCT(MAX((Ações!$B$5:$B$1004=A{r})*Ações!$A$5:$A$1004))))', D)
        put(pe, r, 14, f'=IF(OR(B{r}="",I{r}=""),"",IF(L{r}="Concluída",M{r},TODAY())-I{r})', "0")
    fim = 4 + NT
    lista(pe, f"B5:B{fim}", "Produção boa nova,Produção boa antiga,Acerto no SAP,Conferir packlist,Refugo (cobrança à parte)")
    for txt, fl in (("Concluída", VERD), ("Parcial", AMAR), ("Pendente", VERM)):
        pe.conditional_formatting.add(f"L5:L{fim}", FormulaRule(formula=[f'$L5="{txt}"'], fill=fl))
    pe.auto_filter.ref = f"A4:N{fim}"
    # Acoes
    ac = aba(wb, "Ações", "Ações (histórico de tratativas)", "Uma linha por ação. Metros resolvidos dá baixa na pendência. Só conferiu? Deixe metros vazio.",
             ["Data", "Nº da pendência", "O que foi feito", "Metros resolvidos", "Quem fez", "Pendência (confere)", "Aviso"], [13, 12, 60, 12, 22, 40, 34])
    for r in range(5, 1005):
        for c in range(1, 6):
            put(ac, r, c, None, D if c == 1 else N if c == 4 else None, fN, EDIT, c == 3)
        put(ac, r, 6, f'=IF(B{r}="","",IFERROR(INDEX(Pendências!$C$5:$C${fim},B{r})&" · "&INDEX(Pendências!$D$5:$D${fim},B{r}),"não existe"))')
        put(ac, r, 7, f'=IF(AND(A{r}="",B{r}="",C{r}="",D{r}=""),"",IF(OR(A{r}="",B{r}=""),"Falta data ou nº",IF(COUNTIFS(Pendências!$A$5:$A${fim},B{r})=0,"Nº não existe",IF(SUMIFS($D$5:$D$1004,$B$5:$B$1004,B{r})>INDEX(Pendências!$E$5:$E${fim},B{r})+0.05,"Baixou mais que a pendência",""))))', None, Font(name=F, size=10, bold=True, color="C0392B"))
    ac.freeze_panes = "A5"
    dv = DataValidation(type="date", operator="greaterThan", formula1="46000", allow_blank=True); ac.add_data_validation(dv); dv.add("A5:A1004")
    # Evolucao
    nf = 12
    ev = aba(wb, "Evolução", "Evolução do saldo por material (m)", "Mostra as 12 fotos mais recentes. Piso = menor saldo entre elas. Igual há = fotos seguidas com o mesmo saldo.",
             ["Material"] + [None] * nf + ["Piso", "Var. última", "Igual há"], [18] + [11] * nf + [11, 12, 10])
    for k in range(nf):
        c = ev.cell(4, 2 + k, f'=IF(Fotos!$H$2-{nf - 1 - k}<1,"",SMALL(Fotos!$A$5:$A${4 + NF},Fotos!$H$2-{nf - 1 - k}))')
        c.number_format = "dd/mm"; c.font, c.fill, c.alignment = fH, H, Alignment(horizontal="right", vertical="center")
    ue = 4 + NM
    for i in range(NM):
        r = 5 + i
        put(ev, r, 1, mats[i] if i < len(mats) else None, None, fB, EDIT)
        for k in range(nf):
            col = L(2 + k)
            put(ev, r, 2 + k, f'=IF(OR($A{r}="",{col}$4=""),"",SUMIFS(Histórico!$C$5:$C${4 + NH},Histórico!$A$5:$A${4 + NH},{col}$4,Histórico!$B$5:$B${4 + NH},$A{r}))', N)
        a, p, z = L(2), L(nf), L(nf + 1)
        put(ev, r, nf + 2, f'=IF($A{r}="","",MIN({a}{r}:{z}{r}))', N, fB)
        put(ev, r, nf + 3, f'=IF(OR($A{r}="",{p}{r}=""),"",ROUND({z}{r}-{p}{r},3))', '+#,##0.0;-#,##0.0;-', fB)
        conds = [f'IF(AND({L(q)}{r}<>"",ABS(N({L(q)}{r})-N({z}{r}))<0.05),1,0)' for q in range(nf, 1, -1)]
        s = "0"
        for q in reversed(conds):
            s = f"{q}*(1+{s})"
        put(ev, r, nf + 4, f'=IF($A{r}="","",IF({z}{r}=0,0,1+{s}))', "0")
    for k, tit in ((ue + 1, "Total"),):
        put(ev, k, 1, tit, None, fB)
        for q in list(range(2, nf + 2)):
            put(ev, k, q, f'=IF({L(q)}$4="","",SUM({L(q)}5:{L(q)}{ue}))', N, fB)
        put(ev, k, nf + 2, f"=SUM({L(nf + 2)}5:{L(nf + 2)}{ue})", N, fB)
    ev.conditional_formatting.add(f"{L(nf + 3)}5:{L(nf + 3)}{ue}", FormulaRule(formula=[f'AND(ISNUMBER(${L(nf + 3)}5),${L(nf + 3)}5>0.05)'], fill=VERM))
    ev.conditional_formatting.add(f"{L(nf + 3)}5:{L(nf + 3)}{ue}", FormulaRule(formula=[f'AND(ISNUMBER(${L(nf + 3)}5),${L(nf + 3)}5<-0.05)'], fill=VERD))
    ev.freeze_panes = "B5"; ev.auto_filter.ref = f"A4:{L(nf + 4)}{ue}"
    # Movimentos
    mv = aba(wb, "Movimentos", "Movimentos da última foto contra a anterior", "Leitura compara o saldo com o SAP lançado no período. É pista, não prova: confirme no físico.",
             ["Material", "Anterior", "Última", "Variação", "Boa lançada", "Refugo lançado", "Leitura"], [18, 12, 12, 12, 14, 14, 60])
    z, p = L(nf + 1), L(nf)
    for i in range(NM):
        r = 5 + i
        put(mv, r, 1, f'=IF(Evolução!A{r}="","",Evolução!A{r})', None, fB)
        put(mv, r, 2, f'=IF(A{r}="","",Evolução!{p}{r})', N); put(mv, r, 3, f'=IF(A{r}="","",Evolução!{z}{r})', N)
        put(mv, r, 4, f'=IF(OR(A{r}="",B{r}=""),"",ROUND(C{r}-B{r},3))', '+#,##0.0;-#,##0.0;-', fB)
        for c, t in ((5, "Boa"), (6, "Refugo")):
            put(mv, r, c, f'=IF(A{r}="","",SUMIFS(SAP!$D$5:$D${4 + NS},SAP!$B$5:$B${4 + NS},A{r},SAP!$C$5:$C${4 + NS},"{t}",SAP!$A$5:$A${4 + NS},">="&Evolução!${p}$4,SAP!$A$5:$A${4 + NS},"<="&Evolução!${z}$4))', N)
        put(mv, r, 7, f'=IF(OR(A{r}="",D{r}=""),"",IF(ABS(D{r})<0.05,IF(C{r}=0,"",IF(E{r}>0,"Igual: produção nova passou e saiu","Igual: parado")),IF(D{r}<0,"Caiu: saiu material ou refugo",IF(ABS(D{r}-F{r})<=0.1,"Subiu: igual ao refugo lançado",IF(E{r}>0,"Subiu: pode ser pallet em trânsito. CONFIRMAR a saída","Subiu sem produção no SAP do período. VERIFICAR")))))')
    mv.conditional_formatting.add(f"G5:G{ue}", FormulaRule(formula=['OR(ISNUMBER(SEARCH("CONFIRMAR",$G5)),ISNUMBER(SEARCH("VERIFICAR",$G5)))'], fill=VERM))
    mv.conditional_formatting.add(f"G5:G{ue}", FormulaRule(formula=['ISNUMBER(SEARCH("refugo lançado",$G5))'], fill=AMAR))
    mv.auto_filter.ref = f"A4:G{ue}"
    # Fotos
    fo = aba(wb, "Fotos", "Fotos do saldo", "Uma linha por dia, na coluna Data. O total vem da aba Histórico.",
             ["Data", "Observação", "Total (m)", "Linhas", "Confere com Evolução?"], [13, 52, 13, 10, 24])
    fo["G2"], fo["H2"] = "Fotos:", f"=COUNT(A5:A{4 + NF})"
    for i in range(NF):
        r = 5 + i
        put(fo, r, 1, dt(FOTOS[i][0]) if i < len(FOTOS) else None, D, fN, EDIT)
        put(fo, r, 2, FOTOS[i][1] if i < len(FOTOS) else None, None, fN, EDIT)
        put(fo, r, 3, f'=IF(A{r}="","",SUMIFS(Histórico!$C$5:$C${4 + NH},Histórico!$A$5:$A${4 + NH},A{r}))', N)
        put(fo, r, 4, f'=IF(A{r}="","",COUNTIFS(Histórico!$A$5:$A${4 + NH},A{r}))', "0")
        put(fo, r, 5, f'=IF(A{r}="","",IF(D{r}=0,"Sem saldo no Histórico",IF(COUNTIFS($A$5:$A${4 + NF},A{r})>1,"Data repetida",IFERROR(IF(ABS(C{r}-HLOOKUP(A{r},Evolução!$B$4:{z}${ue + 1},{ue - 2},FALSE))<0.1,"ok","Falta material na Evolução"),"fora das 12 últimas"))))')
    # Historico
    hi = aba(wb, "Histórico", "Histórico do saldo (todas as fotos)", "Cole o export novo embaixo: Data, Material, Metros, Tipo. Entrada e Documento são opcionais. Quantidade deve ser número.",
             ["Data da foto", "Material", "Metros", "Tipo de estoque", "Entrada (SAP)", "Documento"], [14, 20, 13, 18, 15, 16])
    for i in range(NH):
        h = hist[i] if i < len(hist) else (None,) * 6
        for c, (v, fm) in enumerate(zip(h, (D, None, "#,##0.000", None, D, None)), 1):
            put(hi, 5 + i, c, v, fm, fI if c == 3 else fN, None if i < len(hist) else EDIT)
    lista(hi, f"D5:D{4 + NH}", "Livre,Bloqueado,Inspeção,Documento PDI,Não separado"); hi.auto_filter.ref = f"A4:F{4 + NH}"
    # SAP
    sp = aba(wb, "SAP", "Lançamentos do SAP (MB51) por dia e material", "101-102, GRT4, unidade M. Refugo = U452021 e U445131. Lido do mb51.xlsx de 24/11 05:24: depois disso não está aqui.",
             ["Data", "Material", "Tipo", "Metros"], [13, 20, 12, 13])
    linhas = sorted((dt(int(x[:2])), m, "Boa" if x[2] == "B" else "Refugo", float(x[3:])) for m, s in SAP.items() for x in s.split())
    for i in range(NS):
        v = linhas[i] if i < len(linhas) else (None,) * 4
        for c, (a, fm) in enumerate(zip(v, (D, None, None, N)), 1):
            put(sp, 5 + i, c, a, fm, fI if c == 4 else fN, None if i < len(linhas) else EDIT)
    lista(sp, f"C5:C{4 + NS}", "Boa,Refugo"); sp.auto_filter.ref = f"A4:D{4 + NS}"
    # Como usar
    cu = aba(wb, "Como usar", "Como usar", "", ["Passo", "O que fazer"], [10, 110], 3)
    for i, (a, b) in enumerate([
        ("Todo dia", "1. Histórico: cole o export da PROD-GR-HOSE abaixo da última linha (data, material, metros, tipo)."),
        ("", "2. Fotos: escreva a data na próxima linha. A coluna E precisa dar ok; 'Falta material' = escreva o código novo no fim da coluna A da Evolução."),
        ("", "3. SAP: acrescente os lançamentos do dia (data, material, Boa ou Refugo, metros). Sem isso, a aba Movimentos não explica a variação."),
        ("", "4. Movimentos: filtre as linhas vermelhas e confirme no físico."),
        ("Ao tratar", "5. Ações: data, nº da pendência, o que foi feito e metros. Feito, Falta e Status mudam sozinhos."),
        ("Nova", "6. Pendências: preencha a próxima linha vazia; o número aparece sozinho. Não ordene nem apague linhas (o número é a posição); use o filtro."),
        ("Cores", "Amarelo = você edita. Azul = número digitado ou importado. Preto = fórmula."),
        ("Limite", "O saldo é por material e não prova qual OP ficou presa. Não some pendências com o saldo: elas se sobrepõem."),
        ("Limite", "Saldos de 18, 19 e 23/11 não separam livre, bloqueado e PDI; por isso o total inclui tudo. A separação começa em 24/11."),
        ("Fonte", "Saldos colados/exportados pelo William; MB51 e GMS lidos em 24/11. Pendências: aba Conferencia_SAP e análise de 24/11."),
    ], 4):
        put(cu, i, 1, a, None, fB); put(cu, i, 2, b, None, fN, None, True)

    # Painel
    pn.sheet_view.showGridLines = False
    for c, w in zip("ABCDEFGH", (3, 24, 15, 15, 15, 15, 15, 15)): pn.column_dimensions[c].width = w
    pn["B2"] = "PROD-GR-HOSE · Controle"; pn["B2"].font = Font(name=F, bold=True, size=18, color=AZ)
    ult = f"Evolução!{z}4"
    pn["B3"] = f'="Última foto: "&TEXT({ult},"dd/mm")&"   ·   anterior: "&TEXT(Evolução!{p}4,"dd/mm")'; pn["B3"].font = Font(name=F, size=10, color=CINZA)
    tot = ue + 1
    cards = [("Saldo total (m)", f"=Evolução!{z}{tot}", "B"), ("Variação (m)", f"=Evolução!{z}{tot}-Evolução!{p}{tot}", "C"),
             ("Boa nova em aberto (m)", f'=SUMIFS(Pendências!$K$5:$K${fim},Pendências!$B$5:$B${fim},"Produção boa nova")', "D"),
             ("Boa antiga em aberto (m)", f'=SUMIFS(Pendências!$K$5:$K${fim},Pendências!$B$5:$B${fim},"Produção boa antiga")', "E"),
             ("Materiais p/ confirmar", '=COUNTIFS(Movimentos!$G$5:$G$%d,"*CONFIRMAR*")+COUNTIFS(Movimentos!$G$5:$G$%d,"*VERIFICAR*")' % (ue, ue), "F"),
             ("Pendências abertas", f'=COUNTIFS(Pendências!$L$5:$L${fim},"Pendente")+COUNTIFS(Pendências!$L$5:$L${fim},"Parcial")', "G"),
             ("Ações registradas", "=COUNT(Ações!$A$5:$A$1004)", "H")]
    bg = PatternFill("solid", fgColor=FUNDO)
    for t, fx, c in cards:
        pn[f"{c}5"], pn[f"{c}6"] = t, fx
        pn[f"{c}5"].font, pn[f"{c}6"].font = Font(name=F, size=9, color=CINZA), Font(name=F, bold=True, size=16, color="C0392B" if c == "D" else AZ)
        pn[f"{c}6"].number_format = "0" if c in "FGH" else "+#,##0.0;-#,##0.0;0" if c == "C" else "#,##0.0"
        for k in "56": pn[f"{c}{k}"].fill, pn[f"{c}{k}"].alignment = bg, Alignment(horizontal="center", vertical="center", wrap_text=True)
    pn.row_dimensions[5].height, pn.row_dimensions[6].height = 28, 32

    def bloco(r, tits):
        for i, t in enumerate(tits):
            c = pn.cell(r, 2 + i, t); c.font, c.fill, c.alignment = fH, H, Alignment(wrap_text=True, vertical="center")
    bloco(8, ["Pendências por tipo", "Total (m)", "Feito (m)", "Falta (m)", "Abertas", "% feito"])
    for i, t in enumerate(["Produção boa nova", "Produção boa antiga", "Acerto no SAP", "Conferir packlist", "Refugo (cobrança à parte)"]):
        r = 9 + i; put(pn, r, 2, t)
        for c, col in ((3, "E"), (4, "J"), (5, "K")):
            put(pn, r, c, f"=SUMIFS(Pendências!${col}$5:${col}${fim},Pendências!$B$5:$B${fim},$B{r})", N)
        put(pn, r, 6, f'=COUNTIFS(Pendências!$B$5:$B${fim},$B{r},Pendências!$K$5:$K${fim},">"&0.05)', "0")
        put(pn, r, 7, f"=IF(C{r}=0,0,1-E{r}/C{r})", "0%")
    bloco(16, ["Maiores saldos da última foto", "Saldo (m)", "Piso (m)", "Variação (m)", "Fotos igual"])
    # chave auxiliar sem empate
    for r in range(5, ue + 1):
        ev.cell(r, nf + 6, f'=IF(OR($A{r}="",{z}{r}=""),"",{z}{r}+ROW()/1000000)')
    ev.column_dimensions[L(nf + 6)].hidden = True
    ch = f"Evolução!${L(nf + 6)}$5:${L(nf + 6)}${ue}"
    for i in range(15):
        r = 17 + i; m = f"MATCH(LARGE({ch},{i + 1}),{ch},0)"
        for c, col, fm in ((2, "A", None), (3, z, N), (4, L(nf + 2), N), (5, L(nf + 3), '+#,##0.0;-#,##0.0;-'), (6, L(nf + 4), "0")):
            put(pn, r, c, f"=IFERROR(INDEX(Evolução!${col}$5:${col}${ue},{m}),\"\")", fm)
    pn["B33"] = "Saldo total inclui refugo, bloqueado, inspeção e PDI. 'Boa nova' ainda precisa de confirmação física. Não some pendências com saldo."
    pn["B33"].font = Font(name=F, size=9, italic=True, color=CINZA)
    g = BarChart(); g.type = "col"; g.title = "Saldo total por foto (m)"; g.style = 10; g.legend = None
    g.add_data(Reference(ev, min_col=2, max_col=nf + 1, min_row=tot), from_rows=True)
    g.set_categories(Reference(ev, min_col=2, max_col=nf + 1, min_row=4))
    g.roundedCorners = False; g.title.overlay = False; g.x_axis.delete = False; g.y_axis.delete = False
    g.x_axis.number_format = "dd/mm"; g.y_axis.number_format = "#,##0"; g.gapWidth = 60
    g.series[0].graphicalProperties.solidFill = "2C6FBF"; g.height, g.width = 9, 15
    pn.add_chart(g, "J4")
    for ws in wb:
        ws.sheet_properties.tabColor = {"Painel": "E2231A", "Pendências": "E67E22", "Ações": "16A34A"}.get(ws.title, "64748B")
        ws.page_setup.orientation = "landscape"; ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0; ws.sheet_properties.pageSetUpPr.fitToPage = True
    wb.save(SAIDA); print(SAIDA, len(hist), "linhas de histórico;", len(mats), "materiais;", len(linhas), "lançamentos")


main()
