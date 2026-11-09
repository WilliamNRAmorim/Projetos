#!/usr/bin/env python3
# Converte conhecimento/*.md em conhecimento_docx/*.docx para o Knowledge do Uiu.
# Motivo: a DLP da Danfoss bloqueia upload de arquivo local no Copilot Studio; SharePoint/OneDrive
# passam por outro conector, mas só aceitam doc/docx/pdf/ppt/xls.
# Uso: python md_para_docx.py   (precisa de: pip install python-docx)
import os, re
from docx import Document
from docx.shared import Pt

AQUI = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(AQUI, "conhecimento")
DST = os.path.join(AQUI, "conhecimento_docx")
os.makedirs(DST, exist_ok=True)

INLINE = re.compile(r"(\*\*[^*]+\*\*|`[^`]+`)")


def add_runs(par, texto):
    for parte in INLINE.split(texto):
        if not parte:
            continue
        if parte.startswith("**") and parte.endswith("**"):
            par.add_run(parte[2:-2]).bold = True
        elif parte.startswith("`") and parte.endswith("`"):
            r = par.add_run(parte[1:-1])
            r.font.name = "Consolas"
        else:
            par.add_run(parte)


def converte(md, docx_path):
    doc = Document()
    doc.styles["Normal"].font.size = Pt(10)
    for linha in open(md, encoding="utf-8").read().splitlines():
        s = linha.rstrip()
        if not s.strip() or s.strip() in ("---",) or s.lstrip().startswith("<!--"):
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            doc.add_heading(m.group(2).replace("**", ""), level=min(len(m.group(1)), 4))
            continue
        m = re.match(r"^(\s*)[-*]\s+(.*)$", s)
        if m:
            nivel = len(m.group(1)) // 2
            p = doc.add_paragraph(style="List Bullet" if nivel == 0 else "List Bullet 2")
            add_runs(p, m.group(2))
            continue
        m = re.match(r"^(\s*)\d+\.\s+(.*)$", s)
        if m:
            p = doc.add_paragraph(style="List Number")
            add_runs(p, m.group(2))
            continue
        if s.startswith(">"):
            s = s.lstrip("> ")
        add_runs(doc.add_paragraph(), s.strip())
    doc.save(docx_path)


for n in sorted(os.listdir(SRC)):
    if n.endswith(".md"):
        out = os.path.join(DST, n[:-3] + ".docx")
        converte(os.path.join(SRC, n), out)
        print(f"{n} -> {os.path.basename(out)} ({os.path.getsize(out)//1024} KB)")
