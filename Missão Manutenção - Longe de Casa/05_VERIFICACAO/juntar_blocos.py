import openpyxl, glob, re, os, pandas as pd, pymupdf
from openpyxl.drawing.image import Image as XLImage
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter
from PIL import Image
from urllib.parse import quote

RAIZ = os.path.dirname(os.path.abspath(__file__))
MAN = os.path.join(os.path.dirname(RAIZ), "02_MANUAIS")
GRT = r"C:\Users\U445131\.copilot\workspaces\3495a970-b3dc-41ef-a72f-ef8077636c5e\attachments\474401ba-9974-45a8-a74e-359d2fe985cc-materiais.csv"

NOVO_COMUM = "Magnatech - 225-II COMMON PARTS SECTION - 09-2026.pdf"
PDFS = {"225-II 20C": "225-II 20C Parts List.pdf",
        "225-II 24C": "262-EN - 225-II - 24C PARTS SECTION - 01-2025.pdf",
        "225-II COMUM": "262-EN - 225-II - COMMON PARTS SECTION - 01-2018.pdf",
        "RB2 24C": "RB2 24C Parts List 2022.pdf"}
IMG261 = "261-EN 225-II Parts List -06-09"

def paginas(pdf):
    return [p.get_text() for p in pymupdf.open(os.path.join(MAN, pdf))]
TXT = {"novo": paginas(NOVO_COMUM), "RB2 24C": paginas(PDFS["RB2 24C"])}

def achar(code, textos):
    c = code.upper().replace(" ", "")
    for i, t in enumerate(textos):
        if c in t.upper().replace(" ", ""):
            return i + 1
    return None

forn = {}
m = pd.read_csv(GRT, dtype=str).fillna("")
for _, r in m.iterrows():
    for c in re.split(r"[,/;\s]+", r.descricao_fornecedor.upper()):
        if c:
            forn[c] = f"{r.grt} {r.nome}"

def alvo(code, maq, pag):
    """retorna (rótulo, link relativo) usando o manual mais atual disponível"""
    cod = re.split(r"[,/;\s]+", code)[0]
    if maq == "225-II COMUM":
        p = achar(cod, TXT["novo"])
        if p:
            return f"COMUM rev 09-2026 p{p}", "../02_MANUAIS/" + quote(NOVO_COMUM) + f"#page={p}"
        return f"COMUM rev 01-2018 p{pag}", "../02_MANUAIS/" + quote(PDFS[maq]) + f"#page={pag}"
    if maq == "RB2 24C":
        p = achar(cod, TXT["RB2 24C"]) or int(pag)
        return f"RB2 24C p{p}", "../02_MANUAIS/" + quote(PDFS[maq]) + f"#page={p}"
    if maq == "261":
        return f"261-EN p{pag} (imagem)", "../02_MANUAIS/manuais_imagens/" + quote(IMG261) + f"/p{int(pag):03d}.png"
    return f"{maq} p{pag}", "../02_MANUAIS/" + quote(PDFS[maq]) + f"#page={pag}"

linhas = []
for d in sorted(glob.glob(os.path.join(RAIZ, "BLOCO_*"))):
    bl = os.path.basename(d)
    nova = os.path.join(d, "VERIFICACAO_BLOCO_01_com_links.xlsx")
    fs = [nova] if os.path.exists(nova) else glob.glob(os.path.join(d, "VERIFICACAO_*.xlsx"))
    for r in openpyxl.load_workbook(fs[0]).active.iter_rows(min_row=2, values_only=True):
        if r[0]:
            linhas.append((bl, r))

hdr = ["Bloco", "Material (NI)", "Foto", "Pallet / Caixa / Qtd", "O que parece ser", "Nome sugerido (PT)",
       "Candidata 1", "Candidata 2", "Candidata 3", "Candidata 4", "Candidata 5", "Maior %", "Já no GRT?",
       "Medir / fotografar para confirmar", "APRENDIZ: qual candidata confere? (1-5 / Nenhuma)",
       "Código FINAL confirmado", "Nome da peça FINAL", "Parte da máquina FINAL", "Observação do aprendiz"]
wb = openpyxl.Workbook(); ws = wb.active; ws.title = "Verificar"; ws.append(hdr)
thin = Side(style="thin", color="999999")
for c in ws[1]:
    c.font = Font(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor="1F4E78")
    c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
for c in ws[1][14:]:
    c.fill = PatternFill("solid", fgColor="7F6000")
ws.row_dimensions[1].height = 48; ws.freeze_panes = "C2"

thumbs = []
for n, (bl, r) in enumerate(linhas, start=2):
    ni = r[0]
    cands, grt, pcts = [], [], []
    for c in r[5:10]:
        if not c:
            cands.append(("", None)); continue
        L = str(c).split("\n")
        code, desc, parte = L[0], (L[1] if len(L) > 1 else ""), (L[2] if len(L) > 2 else "")
        mm = re.match(r"(.*?) p(\d+) · (\d+)%", L[-1])
        if not mm:
            cands.append((str(c), None)); continue
        maq, pag, pct = mm.group(1).replace("261-EN", "261"), mm.group(2), mm.group(3)
        pcts.append(int(pct))
        rot, link = alvo(code, maq, pag)
        cands.append((f"{code}\n{desc}\n{parte}\n{rot} · {pct}%", link))
        for k in re.split(r"[,/;\s]+", code.upper()):
            if k in forn and forn[k] not in grt:
                grt.append(f"{k} = {forn[k]}")
    sem_foto = r[1] == "SEM FOTO"
    ws.append([bl, ni, "SEM FOTO" if sem_foto else "", r[2], r[3], r[4],
               *[t for t, _ in cands], max(pcts) if pcts else "", "\n".join(grt), r[10],
               *(r[11:16] if len(r) > 15 else [""] * 5)][:19])
    for j, (_, link) in enumerate(cands):
        if link:
            cel = ws.cell(row=n, column=7 + j); cel.hyperlink = link
            cel.font = Font(color="0563C1", underline="single")
    foto = os.path.join(RAIZ, bl, f"{ni}.jpg")
    if not sem_foto and os.path.exists(foto):
        im = Image.open(foto); im.thumbnail((320, 180))
        tp = os.path.join(RAIZ, f".g_{ni}.png"); im.save(tp); thumbs.append(tp)
        xi = XLImage(tp); xi.width, xi.height = im.size; ws.add_image(xi, f"C{n}")
        ws.row_dimensions[n].height = 150
    else:
        ws.row_dimensions[n].height = 40

for i, w in enumerate([9, 11, 46, 16, 30, 22, 30, 30, 30, 30, 30, 8, 28, 36, 24, 22, 24, 24, 34], 1):
    ws.column_dimensions[get_column_letter(i)].width = w
for row in ws.iter_rows(min_row=2, max_row=len(linhas) + 1):
    for c in row:
        c.alignment = Alignment(wrap_text=True, vertical="top")
        c.border = Border(top=thin, bottom=thin, left=thin, right=thin)
    for c in row[14:]:
        c.fill = PatternFill("solid", fgColor="FFF2CC")
dv = DataValidation(type="list", formula1='"1,2,3,4,5,Nenhuma,Precisa de mais fotos"', allow_blank=True)
ws.add_data_validation(dv); dv.add(f"O2:O{len(linhas) + 1}")
ws.auto_filter.ref = f"A1:{get_column_letter(len(hdr))}{len(linhas) + 1}"
out = os.path.join(RAIZ, "VERIFICACAO_GERAL.xlsx")
wb.save(out)
for t in thumbs: os.remove(t)
print("ok", out, len(linhas), "NI")
