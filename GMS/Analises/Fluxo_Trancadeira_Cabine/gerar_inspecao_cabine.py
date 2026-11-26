# gerar_inspecao_cabine.py: Excel + HTML da lista RegistrosInspeção (tela TesteInspeção do GMS), sem limite de linhas.
# Entrada: JSON {users:{id:nome}, rows:[itens da lista]} puxado pelo navegador do app (REST, todas as páginas).
# Uso: python -I gerar_inspecao_cabine.py <inspecao.json> <AAAA-MM-DD>
# Saída em Relatorios_locais/ (ignorada no git: tem nome de inspetor).
import json, sys, os, datetime as dt
from collections import defaultdict
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils import get_column_letter

SRC, DIA = sys.argv[1], sys.argv[2]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Relatorios_locais")
d = json.load(open(SRC, encoding="utf-8"))
users = d["users"]
UTC3 = dt.timedelta(hours=-3)  # Brasil sem horário de verão

def linha(x):
    t = dt.datetime.fromisoformat(x["DataHoraInspecao"].replace("Z", "")) + UTC3
    prod = (t - dt.timedelta(hours=5, minutes=20)).date()  # dia produtivo começa 05:20 (início do 1º turno)
    return {
        "ID": x["Id"], "DataHora": t, "Data": t.date(), "DiaProdutivo": prod,
        "Turno": x.get("TurnoTeste"), "Cabine": x.get("cabine_teste") or "",
        "Trancadeira": x.get("Tran_x00e7_adeira") or "", "Mangueira": x.get("Mangueira") or "",
        "OP": x.get("OP_ID"), "Metros": x.get("Quantidade_Inspe_x00e7__x00e3_o") or 0,
        "DI": x.get("Diametro_Interno"), "DE": x.get("Diametro_Externo"),
        "Concentricidade": x.get("Concentricidade") or "",
        "Defeito": x.get("Defeito_Inspe_x00e7__x00e3_o") or "", "CodigoDefeito": x.get("CodigoDefeito") or "",
        "Inspetor": users.get(str(x.get("AuthorId")), ""),
    }

rows = sorted((linha(x) for x in d["rows"] if x.get("DataHoraInspecao")), key=lambda r: r["DataHora"])
COLS = list(rows[0].keys())
dia = dt.date.fromisoformat(DIA)
hoje = [r for r in rows if r["DiaProdutivo"] == dia]
hoje_cal = [r for r in rows if r["Data"] == dia]

# ---------- Excel ----------
wb = Workbook()
B = Font(bold=True); H = PatternFill("solid", fgColor="1F4E78"); HF = Font(bold=True, color="FFFFFF")

def aba(ws, dados, nome_tab):
    ws.append(COLS)
    for r in dados:
        ws.append([r[c] for c in COLS])
    for i, c in enumerate(COLS, 1):
        ws.column_dimensions[get_column_letter(i)].width = {"DataHora": 18, "Inspetor": 24, "Mangueira": 14}.get(c, 12)
    for row in ws.iter_rows(min_row=2):
        row[1].number_format = "dd/mm/yyyy hh:mm"; row[2].number_format = "dd/mm/yyyy"; row[3].number_format = "dd/mm/yyyy"
        row[9].number_format = "#,##0.00"
    if dados:
        t = Table(displayName=nome_tab, ref=f"A1:{get_column_letter(len(COLS))}{len(dados)+1}")
        t.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True)
        ws.add_table(t)
    ws.freeze_panes = "A2"

ws = wb.active; ws.title = "Resumo"
ws["A1"] = f"Inspeção / Teste (RegistrosInspeção) — dia produtivo {dia:%d/%m/%Y} (05:20 a 05:20)"; ws["A1"].font = Font(bold=True, size=13)
ws["A2"] = f"Puxado do SharePoint em {dt.datetime.now():%d/%m/%Y %H:%M}. Lista inteira: {len(rows)} linhas (aba Tudo, sem limite)."
lin = 4
def bloco(titulo, chave, dados):
    global lin
    ws.cell(lin, 1, titulo).font = B; lin += 1
    for j, h in enumerate([chave, "Lances", "Metros"], 1):
        c = ws.cell(lin, j, h); c.font = HF; c.fill = H
    lin += 1
    acc = defaultdict(lambda: [0, 0.0])
    for r in dados:
        k = r[chave] if not isinstance(chave, tuple) else " | ".join(str(r[c]) for c in chave)
        acc[k][0] += 1; acc[k][1] += r["Metros"]
    for k in sorted(acc, key=str):
        ws.cell(lin, 1, k); ws.cell(lin, 2, acc[k][0]); c = ws.cell(lin, 3, round(acc[k][1], 2)); c.number_format = "#,##0.00"; lin += 1
    ws.cell(lin, 1, "Total").font = B; ws.cell(lin, 2, len(dados)).font = B
    c = ws.cell(lin, 3, round(sum(r["Metros"] for r in dados), 2)); c.font = B; c.number_format = "#,##0.00"
    lin += 2
bloco("Por cabine", "Cabine", hoje)
bloco("Por turno", "Turno", hoje)
bloco("Por trançadeira", "Trancadeira", hoje)
bloco("Por mangueira", "Mangueira", hoje)
bloco("Por OP", "OP", hoje)
m_cal = f"{sum(r['Metros'] for r in hoje_cal):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
ws.cell(lin, 1, f"Obs.: no dia de calendário {dia:%d/%m} (00:00 a 24:00) entram também os lances do turno 3 da madrugada, que são do dia produtivo anterior: {len(hoje_cal)} lances, {m_cal} m.")
ws.column_dimensions["A"].width = 26; ws.column_dimensions["B"].width = 10; ws.column_dimensions["C"].width = 12

aba(wb.create_sheet(f"Hoje"), hoje, "tHoje")
for cab in sorted({r["Cabine"] for r in hoje}):
    aba(wb.create_sheet(f"Hoje_{cab}"[:31]), [r for r in hoje if r["Cabine"] == cab], "t" + "".join(ch for ch in cab if ch.isalnum()))
aba(wb.create_sheet("Tudo"), rows, "tTudo")
xlsx = os.path.join(OUT, f"Inspecao_Cabine_{DIA}.xlsx")
wb.save(xlsx)

# ---------- HTML ----------
def js(r):
    return [r["ID"], r["DataHora"].strftime("%Y-%m-%d %H:%M"), r["DiaProdutivo"].isoformat(), r["Turno"], r["Cabine"],
            r["Trancadeira"], r["Mangueira"], r["OP"], r["Metros"], r["DI"], r["DE"], r["Concentricidade"],
            r["Defeito"] or r["CodigoDefeito"], r["Inspetor"]]
dados_js = json.dumps([js(r) for r in rows], ensure_ascii=False, separators=(",", ":"))
tpl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "inspecao_template.html"), encoding="utf-8").read()
html = tpl.replace("__DADOS__", dados_js).replace("__DIA__", DIA).replace("__GERADO__", dt.datetime.now().strftime("%d/%m/%Y %H:%M"))
hp = os.path.join(OUT, f"Inspecao_Cabine_{DIA}.html")
open(hp, "w", encoding="utf-8").write(html)

por_cab = defaultdict(float)
for r in hoje: por_cab[r["Cabine"]] += r["Metros"]
print(len(rows), "linhas |", len(hoje), "lances no dia produtivo |", {k: round(v, 2) for k, v in por_cab.items()})
print(xlsx); print(hp)
