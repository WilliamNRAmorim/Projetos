# Cacada de packlists repetidos (Packing_Pallets inteiro, 592 registros, + versoes) no formato do v3.
# Dados lidos do SharePoint em 26/11/2026 (Packing_Pallets, RegistrosInspecao, ficha_producao e versoes dos pallets).
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from openpyxl.utils import get_column_letter as L
from openpyxl.worksheet.table import Table, TableStyleInfo

SAIDA = Path(__file__).resolve().parent / "Cacada_Pallets_Repetidos_2026-11-26.xlsx"
# OP, material, metros da OP no GMS, soma dos registros, registros (id nº lances m), relacao, 1a data
OPS = [
    ("30885514", "GH493-16", 217.2, 434.4, "589 (nº1, 5 lances, 217,2); 590 (nº2, 1, 80,0); 591 (nº3, 4, 137,2)", "589 = 590 + 591", "26/11"),
    ("30915068", "GH781-12", 395.5, 581.3, "581 (nº1, 5, 395,5); 582 (nº2, 2, 185,8)", "582 dentro do 581", "25/11"),
    ("30885821", "GH781-8", 513.4, 931.8, "564 (nº1, 8, 513,4); 566 (nº2, 4, 418,4)", "566 dentro do 564", "24/11"),
    ("30885827", "GH781-4", 812.4, 1147.4, "561 (nº1, 10, 812,4); 562 (nº2, 5, 335,0)", "562 dentro do 561", "24/11"),
    ("30885826", "GH781-4", 818.7, 2457.1, "543 (nº1, 6, 818,7); 544 (nº2, 6, 818,7); 545 (nº3, 6, 818,7); 546 (nº4, 1, 1,0 apagado)", "543 = 544 = 545", "23/11"),
    ("30900101", "GH781-12", 349.1, 698.7, "519 (nº1, 7, 349,1); 520 (nº2, 3, 127,9); 521 (nº3, 4, 221,2); 522 (nº4, 1, 0,5 apagado)", "519 = 520 + 521", "19/11"),
    ("30872771", "GH681-4", 689.8, 2067.4, "497 (nº1, 7, 689,8); 498 (nº2, 6, 688,8); 499 (nº3, 6, 688,8)", "498 = 499, os dois dentro do 497", "17/11"),
    ("30842505", "GH493-8", 504.8, 1009.6, "468 (nº1, 6, 504,8); 469 (nº2, 2, 130,2); 470 (nº3, 4, 374,6)", "468 = 469 + 470", "14/11"),
    ("30829741", "GH781-8", 619.1, 768.0, "451 (nº1, 7, 545,7); 452 (nº2, 2, 148,9); 534 (nº3, 1, 73,4)", "452 dentro do 451", "13/11"),
    ("30770799", "GH493-8", 527.6, 997.5, "363 (nº1, 6, 527,6); 364 (nº2, 5, 469,9)", "364 dentro do 363", "07/11"),
    ("30721705", "FC839B-08", 507.5, 980.8, "366 (nº1, 7, 507,5); 367 (nº2, 6, 473,3)", "367 dentro do 366", "07/11"),
    ("30770800", "GH493-8", 502.0, 599.4, "353 (nº1, 10, 502,0); 354 (nº2, 2, 97,4)", "354 dentro do 353", "06/11"),
    ("30750582", "GH493-16", 239.6, 1258.2, "328 (nº1, 7, 297,5); 329 a 336 (nº2 a 9: 105,9 / 133,7 / 105,9 / 133,7 / 105,9 / 105,9 / 105,9 / 163,8)", "8 pallets repetindo os mesmos lances; todos dentro do 328", "05/11"),
    ("30749038", "EC415-16", 257.4, 386.6, "338 (nº1, 7, 231,5); 339 (nº2, 3, 129,0); 539 (nº3, 1, 26,1)", "339 dentro do 338", "05/11"),
    ("30690495", "GH493-12", 278.0, 525.3, "298 (nº1, 8, 278,0); 299 (nº2, 6, 247,3)", "299 dentro do 298", "31/10"),
    ("30649299", "EC118-12L", 383.1, 530.3, "246 (nº1, 7, 383,1); 247 (nº2, 3, 147,2)", "247 dentro do 246", "28/10"),
    ("30636249", "GH493-16", 236.8, 532.8, "228 (nº1, 7, 236,8); 229 (nº2, 3, 148,0); 230 (nº3, 3, 148,0)", "229 = 230, os dois dentro do 228", "27/10"),
    ("30575537", "GH781-6", 617.1, 1991.2, "173 (nº1, 15, 617,1); 174, 175, 176 (nº2 a 4, 11, 378,5 cada); 177 (nº5, 4, 238,6)", "174 = 175 = 176; todos dentro do 173", "22/10"),
    ("30564363", "EC215-06L", 836.3, 1148.8, "132 (nº1, 12, 836,3); 135 (nº2, 8, 312,5 com 2 lances apagados)", "sobrepostos em 272,7 m", "20/10"),
    ("30479149", "GH781-16", 266.3, 331.2, "106 (nº1, 7, 266,3); 107 (nº2, 4, 64,9 com 1 lance apagado)", "sobrepostos em 52,5 m", "19/10"),
    ("30548095", "EC115-08L", 501.6, 615.2, "101 (nº1, 7, 501,6); 102 (nº2, 2, 113,6)", "102 dentro do 101", "18/10"),
    ("30527597", "EC115-08L", 593.2, 774.3, "87 (nº1, 7, 593,2); 88 (nº2, 3, 181,1)", "88 dentro do 87", "17/10"),
]
SINAL = {  # fotos do saldo de 18, 19, 23, 24, 25 e 26/11
    "30885514": "HOJE: o saldo das 08:18 tem o 591 (137,2) uma vez só. Ainda não transferido",
    "30915068": "Sem sinal de dobra: o saldo de GH781-12 em 26/11 não caiu mais que o produzido",
    "30885821": "Sem sinal de dobra: GH781-8 ficou em 74,5 m de 24 para 25/11",
    "30885827": "Sem sinal de dobra: GH781-4 ficou em 216,5 m de 24 para 25/11",
    "30885826": "Sem sinal de dobra: GH781-4 ficou em ~216 m de 23 para 24/11 (dobrar 818,7 m zeraria o material)",
    "30900101": "Sem sinal de dobra: o saldo de GH781-12 em 23/11 fecha exato",
    "30872771": "Sem sinal de dobra: GH681-4 ficou em 29,1 m de 18 a 25/11",
}
SEQ = [l.split("|") for l in """30885514|589|1|26/11 06:50|2|88,6|Imprimir (papel)
30885514|590|2|26/11 06:51|1|80,0|Dividir pallet (papel)
30885514|591|3|26/11 07:23|4|137,2|Dividir pallet (papel)
30885514|589|1|26/11 07:30|5|217,2|Imprimir de novo (papel)
30885514|589|1|26/11 07:31|5|217,2|Finalizar (sem papel)
30915068|581|1|25/11 18:59|4|222,2|Imprimir (papel)
30915068|582|2|25/11 19:28|2|185,8|Dividir pallet (papel)
30915068|581|1|25/11 19:33|5|395,5|Imprimir de novo (papel)
30915068|581|1|25/11 19:34|5|395,5|Finalizar (sem papel)
30885821|564|1|24/11 21:14|4|95,0|Imprimir (papel)
30885821|564|1|24/11 22:04|8|513,4|Imprimir de novo (papel)
30885821|566|2|24/11 22:05|4|418,4|Dividir pallet (papel)
30885821|564|1|24/11 22:06|8|513,4|Finalizar (sem papel)
30885827|561|1|24/11 19:37|5|477,4|Imprimir (papel)
30885827|561|1|24/11 20:30|10|812,4|Imprimir de novo (papel)
30885827|562|2|24/11 20:30|5|335,0|Dividir pallet (papel)
30885827|561|1|24/11 20:32|10|812,4|Finalizar (sem papel)
30885826|543|1|23/11 20:31|6|818,7|Imprimir (papel)
30885826|544|2|23/11 20:32|6|818,7|Dividir pallet (papel)
30885826|545|3|23/11 20:41|6|818,7|Dividir pallet (papel)
30885826|546|4|23/11 20:42|1|1,0|Dividir pallet (papel)
30885826|543|1|23/11 20:43|6|818,7|Finalizar (sem papel)
30900101|519|1|19/11 16:20|3|127,9|Imprimir (papel)
30900101|520|2|19/11 16:22|3|127,9|Dividir pallet (papel)
30900101|521|3|19/11 17:08|4|221,2|Dividir pallet (papel)
30900101|522|4|19/11 17:16|1|0,5|Dividir pallet (papel)
30900101|519|1|19/11 17:18|8|350,1|Imprimir de novo (papel)
30900101|519|1|19/11 17:18|7|349,1|Imprimir de novo (papel)
30900101|519|1|19/11 17:19|7|349,1|Finalizar (sem papel)
30872771|497|1|17/11 19:11|7|691,3|Imprimir (papel)
30872771|498|2|17/11 19:22|6|688,8|Dividir pallet (papel)
30872771|499|3|17/11 19:23|6|688,8|Dividir pallet (papel)
30872771|497|1|17/11 19:27|6|688,8|Imprimir de novo (papel)
30872771|497|1|17/11 19:28|7|689,8|Imprimir de novo (papel)
30872771|497|1|17/11 19:28|7|689,8|Finalizar (sem papel)
30842505|468|1|14/11 21:38|6|504,8|Imprimir (papel)
30842505|469|2|14/11 21:39|2|130,2|Dividir pallet (papel)
30842505|470|3|14/11 21:42|4|374,6|Dividir pallet (papel)
30842505|468|1|14/11 21:43|6|504,8|Finalizar (sem papel)
30829741|451|1|13/11 21:48|6|470,2|Imprimir (papel)
30829741|452|2|13/11 21:50|2|148,9|Dividir pallet (papel)
30829741|451|1|13/11 23:20|12|1.136,1|Imprimir de novo (papel)
30829741|451|1|14/11 11:43|7|545,7|Imprimir de novo (papel)
30829741|451|1|14/11 11:43|7|545,7|Finalizar (sem papel)
30770799|363|1|07/11 00:55|6|527,6|Imprimir (papel)
30770799|364|2|07/11 00:55|5|469,9|Dividir pallet (papel)
30770799|363|1|07/11 00:56|6|527,6|Finalizar (sem papel)
30721705|366|1|07/11 04:50|7|507,5|Imprimir (papel)
30721705|367|2|07/11 04:50|6|473,3|Dividir pallet (papel)
30721705|366|1|07/11 04:50|7|507,5|Finalizar (sem papel)
30770800|353|1|06/11 09:35|7|395,3|Imprimir (papel)
30770800|354|2|06/11 09:50|2|97,4|Dividir pallet (papel)
30770800|353|1|06/11 09:52|10|502,0|Imprimir de novo (papel)
30770800|353|1|06/11 09:53|10|502,0|Finalizar (sem papel)
30750582|328|1|05/11 08:34|4|133,7|Imprimir (papel)
30750582|329|2|05/11 09:00|2|105,9|Dividir pallet (papel)
30750582|330|3|05/11 09:04|4|133,7|Dividir pallet (papel)
30750582|331|4|05/11 09:04|2|105,9|Dividir pallet (papel)
30750582|328|1|05/11 09:10|6|239,6|Imprimir de novo (papel)
30750582|332|5|05/11 09:10|4|133,7|Dividir pallet (papel)
30750582|333|6|05/11 09:11|2|105,9|Dividir pallet (papel)
30750582|334|7|05/11 09:20|2|105,9|Dividir pallet (papel)
30750582|335|8|05/11 09:29|2|105,9|Dividir pallet (papel)
30750582|336|9|05/11 09:32|3|163,8|Dividir pallet (papel)
30750582|328|1|05/11 10:07|7|297,5|Correção manual do William (sem papel)
30749038|338|1|05/11 11:06|4|102,5|Imprimir (papel)
30749038|338|1|05/11 12:13|7|231,5|Imprimir de novo (papel)
30749038|339|2|05/11 12:29|3|129,0|Dividir pallet (papel)
30749038|338|1|05/11 12:31|7|231,5|Finalizar (sem papel)
30690495|298|1|31/10 00:15|8|278,0|Imprimir (papel)
30690495|299|2|31/10 00:16|6|247,3|Dividir pallet (papel)
30690495|298|1|31/10 00:17|8|278,0|Finalizar (sem papel)
30649299|246|1|28/10 06:56|4|235,9|Imprimir (papel)
30649299|246|1|28/10 07:10|7|383,1|Imprimir de novo (papel)
30649299|247|2|28/10 07:16|3|147,2|Dividir pallet (papel)
30649299|246|1|28/10 07:19|7|383,1|Finalizar (sem papel)
30636249|228|1|27/10 16:48|4|88,8|Imprimir (papel)
30636249|229|2|27/10 16:50|3|148,0|Dividir pallet (papel)
30636249|230|3|27/10 16:51|3|148,0|Dividir pallet (papel)
30636249|228|1|27/10 16:57|7|236,8|Imprimir de novo (papel)
30636249|228|1|27/10 16:57|7|236,8|Finalizar (sem papel)
30575537|173|1|22/10 16:48|11|378,5|Imprimir (papel)
30575537|174|2|22/10 16:49|11|378,5|Dividir pallet (papel)
30575537|175|3|22/10 16:52|11|378,5|Dividir pallet (papel)
30575537|176|4|22/10 16:53|11|378,5|Dividir pallet (papel)
30575537|173|1|22/10 16:53|15|617,1|Imprimir de novo (papel)
30575537|177|5|22/10 16:54|4|238,6|Dividir pallet (papel)
30575537|173|1|22/10 17:13|15|617,1|Finalizar (sem papel)
30564363|132|1|20/10 17:33|5|542,0|Imprimir (papel)
30564363|132|1|20/10 17:38|6|563,6|Imprimir de novo (papel)
30564363|135|2|20/10 18:51|8|312,5|Dividir pallet (papel)
30564363|132|1|20/10 18:53|12|836,3|Imprimir de novo (papel)
30564363|132|1|20/10 18:53|12|836,3|Finalizar (sem papel)
30479149|106|1|19/10 08:56|4|213,8|Imprimir (papel)
30479149|107|2|19/10 09:05|4|64,9|Dividir pallet (papel)
30479149|106|1|19/10 13:26|6|261,9|Imprimir de novo (papel)
30479149|106|1|19/10 13:27|7|266,3|Imprimir de novo (papel)
30479149|106|1|19/10 13:27|7|266,3|Finalizar (sem papel)
30548095|101|1|17/10 22:00|5|388,0|Imprimir (papel)
30548095|101|1|18/10 20:32|7|501,6|Imprimir de novo (papel)
30548095|102|2|18/10 20:33|2|113,6|Dividir pallet (papel)
30548095|101|1|18/10 20:34|7|501,6|Finalizar (sem papel)
30527597|87|1|17/10 07:17|4|412,1|Imprimir (papel)
30527597|87|1|17/10 07:18|7|593,2|Imprimir de novo (papel)
30527597|88|2|17/10 07:24|3|181,1|Dividir pallet (papel)
30527597|87|1|17/10 07:26|7|593,2|Finalizar (sem papel)""".splitlines()]
OUTROS = [  # registro, OP, nº, TotalM, soma dos lances, problema, origem
    (546, "30885826", 4, 1.0, 0.0, "Lance 21950 apagado depois de impresso", "Cabine"),
    (522, "30900101", 4, 0.5, 0.0, "Lance 21884 apagado depois de impresso", "Cabine"),
    (225, "30636252", 2, 145.9, 0.0, "Os 4 lances (19974-19977) foram apagados depois de impressos", "Cabine"),
    (226, "30636252", 3, 87.6, 0.0, "Os 2 lances (19978-19979) foram apagados depois de impressos", "Cabine"),
    (135, "30564363", 2, 312.5, 272.7, "Lances 19466 e 19467 apagados depois de impressos", "Cabine"),
    (107, "30479149", 2, 64.9, 52.5, "Lance 19274 apagado depois de impresso", "Cabine"),
    (308, "30707080", 1, 0.1, 0.0, "Lance 20530 (0,1 m) apagado na correção de 12/11", "Correção do Claude"),
    (19, "30447770", 1, 572.4, 485.6, "Lance 17870 apagado (12/11) e lance 17869 hoje na OP 30406468", "Correção do Claude"),
    (46, "30479026", 1, 776.8, 750.4, "Lance 18493 apagado (12/11) e 10 lances hoje na OP 30424233", "Correção do Claude e anterior"),
    (49, "30447183", 1, 716.4, 577.5, "Lance 18425 apagado na correção de 12/11", "Correção do Claude"),
    (93, "30495038", 1, 653.1, 616.9, "Lance 19161 apagado (12/11) e 7 lances movidos para a OP 30495036", "Correção do Claude"),
    (9, "30424231", 1, 649.0, 649.0, "Os 26 lances estão hoje na OP 30351277", "Correção anterior a 12/11"),
    (10, "30424231", 2, 27.0, 27.0, "Os 5 lances estão hoje na OP 30351277", "Correção anterior a 12/11"),
    (11, "30406468", 1, 674.7, 674.7, "Lances 17734 e 17735 hoje na OP 30447770", "Correção anterior a 12/11"),
    (240, "30636253", 1, 559.7, 559.7, "Lance 20091 hoje na OP 30604449", "Correção anterior a 12/11"),
    (241, "30636253", 2, 462.7, 462.7, "Lance 20089 hoje na OP 30604449", "Correção anterior a 12/11"),
    (301, "30678924", 1, 399.0, 399.5, "10 lances movidos para a OP 30651981 (12/11); total 0,5 m diferente", "Correção do Claude"),
    (302, "30678924", 2, 281.6, 281.6, "Lances 20489 e 20496 movidos para a OP 30651981 (12/11)", "Correção do Claude"),
    (305, "30721225", 2, 284.4, 284.4, "5 lances movidos para a OP 30707080 (12/11)", "Correção do Claude"),
    (323, "30678925", 1, 849.4, 849.4, "Lances 20633 e 20634 movidos para a OP 30604956 (12/11)", "Correção do Claude"),
    (328, "30750582", 1, 297.5, 297.5, "Lance 20688 movido para a OP 30750535 (12/11)", "Correção do Claude"),
    (336, "30750582", 9, 163.8, 163.8, "Lance 20688 movido para a OP 30750535 (12/11)", "Correção do Claude"),
    (360, "30771528", 2, 405.6, 405.6, "Lance 20840 movido para a OP 30771531 (12/11)", "Correção do Claude"),
    (60, "30529216", 1, 532.8, 532.0, "Total do registro 0,8 m acima da soma dos lances", "Cabine"),
    (338, "30749038", 1, 231.5, 231.3, "Total do registro 0,2 m acima da soma dos lances", "Cabine"),
    (339, "30749038", 2, 129.0, 128.8, "Total do registro 0,2 m acima da soma dos lances", "Cabine"),
]


def nova(wb, nome, tit, sub, cor):
    ws = wb.create_sheet(nome); ws.sheet_properties.tabColor = cor; ws.sheet_view.showGridLines = False
    ws["A1"], ws["A2"] = tit, sub
    ws["A1"].font, ws["A2"].font = Font(bold=True, size=16, color=cor), Font(size=10, color="6B6B69")
    ws.row_dimensions[1].height = 26; ws.freeze_panes = "A5"
    return ws


def tabela(ws, nome, cab, lin, larg, num=(), total=None, estilo="TableStyleMedium2"):
    for j, c in enumerate(cab, 1):
        ws.cell(4, j, c).alignment = Alignment(wrap_text=True, vertical="center"); ws.column_dimensions[L(j)].width = larg[j - 1]
    ws.row_dimensions[4].height = 32
    for i, l in enumerate(lin, 5):
        for j, v in enumerate(l, 1):
            c = ws.cell(i, j, v); c.alignment = Alignment(wrap_text=True, vertical="top")
            if j - 1 in num: c.number_format = "#,##0.0"
    fim = 4 + len(lin)
    t = Table(displayName=nome, ref=f"A4:{L(len(cab))}{fim}"); t.tableStyleInfo = TableStyleInfo(name=estilo, showRowStripes=True); ws.add_table(t)
    if total is not None:
        ws.cell(fim + 1, 1, "Total").font = Font(bold=True)
        for k in total:
            c = ws.cell(fim + 1, k + 1, f"=SUBTOTAL(109,{nome}[{cab[k]}])"); c.font = Font(bold=True); c.number_format = "#,##0.0"
    return fim + 1


def abas(wb, pre=""):
  papel = {}
  for s in SEQ:
      if "(papel)" in s[6]: papel[s[0]] = papel.get(s[0], 0) + 1
  ws = nova(wb, pre + "1 Packlist repetido", "1 · OPs com o mesmo lance em mais de um packlist",
            "Varredura dos 592 registros de pallet do GMS (06/10 a 26/11). Risco: transferir o mesmo metro duas vezes. Quem: Cabine e Logística.", "E2000F")
  lin = []
  for op, pn, gms, soma, regs, rel, d in OPS:
      hoje = op == "30885514"
      lin.append((op, pn, gms, soma, round(soma - gms, 1), papel.get(op, 0), regs, rel, d, SINAL.get(op, "Antes de 18/11: sem foto do saldo para conferir"),
                  ("HOJE, antes de transferir: separar os papéis desta OP. Vale o 590 (80,0) + o 591 (137,2) OU o 589 (217,2), nunca os três. "
                   if hoje else "Perguntar à logística quais destes packlists foram transferidos. ") + "Recolher os repetidos e corrigir o registro no GMS"))
  r = tabela(ws, "Repetidos", ["OP", "Material", "Metros da OP (GMS)", "Soma dos packlists (m)", "A mais (m)", "Papéis possíveis", "Registros (id, nº, lances, m)",
                               "Relação", "Desde", "Sinal no saldo", "Ação"], lin, [11, 11, 11, 12, 10, 9, 46, 26, 8, 40, 52], num=(2, 3, 4), total=(2, 3, 4))
  for t in ("Como acontece: a cabine imprime o pallet 1 com os lances da hora; depois usa Dividir pallet para os seguintes; aí o Imprimir (ou o Finalizar) regrava o pallet 1 com a OP inteira, por cima.",
            "Papéis possíveis = versões que passaram pela tela de impressão (aba 2). O GMS não sabe se o operador imprimiu de fato: confirmar com a cabine.",
            "Correção: a tela da Finalização v0.4.4 (Telas/_colar_Finalizacao_Pallets.md) faz o Imprimir abrir o Dividir e nunca sobrescreve pallet. Ainda não foi colada no Studio.",
            "SAP: em todos estes casos cada lance entrou uma vez só no SAP (101). O risco é só na transferência da PROD-GR-HOSE."):
      r += 1; ws.cell(r, 1, t).font = Font(size=10, color="6B6B69")
  ws = nova(wb, pre + "2 Sequência", "2 · O que aconteceu em cada OP, minuto a minuto", "Cada linha é uma versão do registro de pallet no GMS (horário de Brasília).", "1F5FA8")
  tabela(ws, "Sequencia", ["OP", "Registro", "Pallet nº", "Quando", "Lances", "Metros", "O que foi"],
         [(a, int(b), int(c), d, int(e), float(f.replace(".", "").replace(",", ".")), g) for a, b, c, d, e, f, g in SEQ], [11, 10, 9, 14, 8, 10, 40], num=(5,), estilo="TableStyleLight9")
  ws = nova(wb, pre + "3 Lance apagado ou movido", "3 · Packlist com lance que não existe mais nessa OP",
            "Se o papel foi transferido com esse lance, a transferência pegou metro que não é desta OP. Quem: Supervisão.", "6B4FA0")
  tabela(ws, "Outros", ["Registro", "OP", "Pallet nº", "Total do registro (m)", "Lances que existem na OP (m)", "Problema", "Origem"],
         [(a, b, c, d, e, f, g) for a, b, c, d, e, f, g in OUTROS], [10, 11, 9, 12, 14, 70, 26], num=(3, 4), estilo="TableStyleMedium5")


if __name__ == "__main__":
    wb = Workbook(); wb.remove(wb.active); abas(wb)
    wb.save(SAIDA)
    print(SAIDA.name)
