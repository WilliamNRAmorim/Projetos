"""Montador deterministico de .docx do TCC II, usando o .docx do TCC I como molde.

Uso: python -I build_docx.py entrada.md saida.docx
So biblioteca padrao (zipfile, re, struct). Nao altera o molde.
Extra: uma primeira linha "# Titulo" no markdown troca o texto do titulo do molde.
"""
import re
import struct
import sys
import zipfile
from pathlib import Path

RAIZ_TCC = Path(__file__).resolve().parents[2]   # .../Projetos/TCC
MOLDE = RAIZ_TCC / "TCC_GMS.docx"
FIGURAS = RAIZ_TCC / "Fase2" / "figuras"
MAX_W = 5760000   # 16 cm em EMU
MAX_H = 7200000   # 20 cm em EMU
FIG_ESPECIAL = "fig04_evolucao_interface.png"
CM = 360000  # EMU por cm
LARG_CM = {"fig01": 15, "fig02": 11, "fig03": 11, "fig05": 11, "fig06": 12.5, "fig07": 13.5,
           "fig08": 14, "fig09": 11.5, "fig10": 13.5, "fig11": 8.5, "fig12": 13, "fig13": 13,
           "print": 12.5}
FIG04_CM = 7.8  # largura de cada tela (a) e (b) reaproveitada do TCC I

FONT = ('<w:rFonts w:ascii="Times New Roman" w:cs="Times New Roman" '
        'w:eastAsia="Times New Roman" w:hAnsi="Times New Roman"/>')
CONSOLAS = ('<w:rFonts w:ascii="Consolas" w:cs="Consolas" '
            'w:eastAsia="Consolas" w:hAnsi="Consolas"/>')
BORDAS = ''.join(f'<w:{l} w:color="000000" w:space="0" w:sz="4" w:val="single"/>'
                 for l in ("top", "left", "bottom", "right"))
CELMAR = ('<w:tcMar><w:top w:w="80.0" w:type="dxa"/><w:left w:w="120.0" w:type="dxa"/>'
          '<w:bottom w:w="80.0" w:type="dxa"/><w:right w:w="120.0" w:type="dxa"/></w:tcMar>')
TBLPR = ('<w:tblPr><w:tblStyle w:val="Table1"/><w:tblW w:w="9072.0" w:type="dxa"/>'
         '<w:jc w:val="left"/><w:tblBorders>'
         + ''.join(f'<w:{l} w:color="000000" w:space="0" w:sz="4" w:val="single"/>'
                   for l in ("top", "left", "bottom", "right", "insideH", "insideV"))
         + '</w:tblBorders><w:tblLayout w:type="fixed"/><w:tblLook w:val="0000"/></w:tblPr>')


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def rpr(sz=24, b=False, i=False, font=FONT):
    x = font
    if b:
        x += '<w:b w:val="1"/><w:bCs w:val="1"/>'
    if i:
        x += '<w:i w:val="1"/><w:iCs w:val="1"/>'
    return f'<w:rPr>{x}<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/><w:rtl w:val="0"/></w:rPr>'


def run(text, **kw):
    if text == "":
        return ""
    return f'<w:r>{rpr(**kw)}<w:t xml:space="preserve">{esc(text)}</w:t></w:r>'


def runs(text, sz=24, b=False, i=False, font=FONT):
    """Texto com **negrito** e *italico* inline."""
    out = []
    for parte in re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*)", text):
        if parte.startswith("**") and parte.endswith("**") and len(parte) > 4:
            out.append(run(parte[2:-2], sz=sz, b=True, i=i, font=font))
        elif parte.startswith("*") and parte.endswith("*") and len(parte) > 2:
            out.append(run(parte[1:-1], sz=sz, b=b, i=True, font=font))
        else:
            out.append(run(parte, sz=sz, b=b, i=i, font=font))
    return "".join(out)


def para(inner, before=0, after=0, line=360, jc="left", ind="", keep=False):
    kn = "<w:keepNext/>" if keep else ""
    return (f'<w:p><w:pPr>{kn}<w:spacing w:after="{after}" w:before="{before}" '
            f'w:line="{line}" w:lineRule="auto"/>{ind}<w:jc w:val="{jc}"/></w:pPr>{inner}</w:p>')


def p_titulo(texto, centro, quebra=False):
    br = '<w:r><w:br w:type="page"/></w:r>' if quebra else ""
    return para(br + runs(texto, b=True), before=240, after=120,
                jc="center" if centro else "left", keep=True)


def p_corpo(texto):
    return para(runs(texto), after=80, jc="both", ind='<w:ind w:firstLine="708"/>')


def p_ref(texto):
    return para(runs(texto), after=120, line=240, jc="left")


def p_chave(texto):
    rot, _, resto = texto.partition(":")
    return para(run(rot + ":", b=True) + runs(resto), after=80, jc="both")


def p_legenda(texto):
    return para(runs(texto, sz=22, b=True), before=180, after=60, line=276, keep=True)


def p_fonte(texto):
    return para(runs(texto, sz=22), before=60, after=180, line=276)


def png_dim(path):
    d = path.read_bytes()[:24]
    if d[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path} nao e PNG")
    return struct.unpack(">II", d[16:24])


def drawing(rid, nome, docid, cx, cy):
    return (f'<w:drawing><wp:inline distB="114300" distT="114300" distL="114300" distR="114300">'
            f'<wp:extent cx="{cx}" cy="{cy}"/><wp:effectExtent b="0" l="0" r="0" t="0"/>'
            f'<wp:docPr id="{docid}" name="{nome}"/><a:graphic><a:graphicData '
            f'uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic><pic:nvPicPr>'
            f'<pic:cNvPr id="0" name="{nome}"/><pic:cNvPicPr preferRelativeResize="0"/></pic:nvPicPr>'
            f'<pic:blipFill><a:blip r:embed="{rid}"/><a:srcRect b="0" l="0" r="0" t="0"/>'
            f'<a:stretch><a:fillRect/></a:stretch></pic:blipFill><pic:spPr><a:xfrm>'
            f'<a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"/>'
            f'<a:ln/></pic:spPr></pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing>')


def p_imagem(dr):
    return para(f'<w:r><w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>{dr}</w:r>',
                before=60, line=276, jc="center", keep=True)


def celula(w, paragrafos, cab=False):
    shd = '<w:shd w:fill="dddddd" w:val="clear"/>' if cab else ""
    return (f'<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/><w:tcBorders>{BORDAS}</w:tcBorders>'
            f'{shd}{CELMAR}</w:tcPr>{paragrafos}</w:tc>')


def larguras(linhas, n):
    minimo = min(1300, 9072 // n)
    pesos = []
    for c in range(n):
        m = max(len(l[c].replace("*", "")) for l in linhas)
        pesos.append(max(m, 4) ** 0.8)
    livre = 9072 - minimo * n
    tot = sum(pesos)
    w = [minimo + int(livre * p / tot) for p in pesos]
    w[-1] += 9072 - sum(w)
    return w


def tabela(linhas):
    n = len(linhas[0])
    linhas = [(l + [""] * n)[:n] for l in linhas]
    w = larguras(linhas, n)
    grid = "".join(f'<w:gridCol w:w="{x}"/>' for x in w)
    trs = []
    for k, l in enumerate(linhas):
        cab = k == 0
        tr = (f'<w:tr><w:trPr><w:cantSplit w:val="0"/><w:tblHeader w:val="{1 if cab else 0}"/></w:trPr>'
              + "".join(celula(w[c], para(runs(l[c], sz=22, b=cab), line=252), cab)
                        for c in range(n)) + '</w:tr>')
        trs.append(tr)
    return f'<w:tbl>{TBLPR}<w:tblGrid>{grid}</w:tblGrid>{"".join(trs)}</w:tbl>'


def tabela_codigo(codigo):
    ps = "".join(para(run(l, sz=18, font=CONSOLAS), line=240) for l in codigo.split("\n"))
    return (f'<w:tbl>{TBLPR}<w:tblGrid><w:gridCol w:w="9072"/></w:tblGrid><w:tr><w:trPr>'
            f'<w:cantSplit w:val="0"/><w:tblHeader w:val="0"/></w:trPr>'
            f'{celula(9072, ps)}</w:tr></w:tbl>')


def fig04_lado_a_lado(fig1):
    """Monta as telas (a) e (b) do TCC I lado a lado, numa tabela sem bordas."""
    fat = FIG04_CM * CM / 5760000

    def _esc(m):
        return (m.group(1) + 'cx="' + str(round(int(m.group(2)) * fat)) + '" cy="'
                + str(round(int(m.group(3)) * fat)) + '"')

    def _img(par):
        dr = re.search(r"<w:drawing>.*?</w:drawing>", par, re.S).group(0)
        dr = re.sub(r'(<wp:extent |<a:ext )cx="(\d+)" cy="(\d+)"', _esc, dr)
        return para('<w:r>' + dr + '</w:r>', before=60, line=240, jc="center", keep=True)

    def _sub(par):
        txt = "".join(re.findall(r"<w:t[^>]*>(.*?)</w:t>", par, re.S)).strip()
        return para(run(txt, sz=22), line=240, jc="center")

    semborda = ('<w:tcBorders><w:top w:val="nil"/><w:left w:val="nil"/>'
                '<w:bottom w:val="nil"/><w:right w:val="nil"/></w:tcBorders>')
    meia = 9072 // 2
    cel = lambda conteudo: (f'<w:tc><w:tcPr><w:tcW w:w="{meia}" w:type="dxa"/>{semborda}'
                            f'</w:tcPr>{conteudo}</w:tc>')
    tblpr = ('<w:tblPr><w:tblW w:w="9072" w:type="dxa"/><w:jc w:val="center"/>'
             '<w:tblBorders><w:top w:val="nil"/><w:left w:val="nil"/><w:bottom w:val="nil"/>'
             '<w:right w:val="nil"/><w:insideH w:val="nil"/><w:insideV w:val="nil"/></w:tblBorders>'
             '<w:tblLayout w:type="fixed"/><w:tblCellMar><w:left w:w="60" w:type="dxa"/>'
             '<w:right w:w="60" w:type="dxa"/></w:tblCellMar></w:tblPr>')
    a = cel(_img(fig1[0]) + _sub(fig1[1]))
    b = cel(_img(fig1[2]) + _sub(fig1[3]))
    return (f'<w:tbl>{tblpr}<w:tblGrid><w:gridCol w:w="{meia}"/><w:gridCol w:w="{meia}"/></w:tblGrid>'
            f'<w:tr><w:trPr><w:cantSplit/></w:trPr>{a}{b}</w:tr></w:tbl>')


def split_row(linha):
    l = linha.strip()
    if l.startswith("|"):
        l = l[1:]
    if l.endswith("|") and not l.endswith("\\|"):
        l = l[:-1]
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", l)]


def eh_separador(r):
    return all(re.fullmatch(r":?-+:?", c) for c in r)


def main():
    if len(sys.argv) != 3:
        sys.exit("uso: python -I build_docx.py entrada.md saida.docx")
    entrada, saida = Path(sys.argv[1]), Path(sys.argv[2])
    linhas = entrada.read_text(encoding="utf-8-sig").replace("\r\n", "\n").split("\n")

    zin = zipfile.ZipFile(MOLDE)
    doc = zin.read("word/document.xml").decode("utf-8")
    raiz = doc[:doc.index("<w:body>") + len("<w:body>")]
    corpo = doc[len(raiz):]
    paras = re.findall(r"<w:p [^>]*>.*?</w:p>", corpo, re.S)
    ini = paras[:4]
    sect = re.search(r"<w:sectPr>.*?</w:sectPr>", doc, re.S).group(0)
    k = next(n for n, p in enumerate(paras) if re.search(r"<w:t[^>]*>Figura 1 ", p))
    fig1 = paras[k + 1:k + 5]   # imagem a, subtitulo a, imagem b, subtitulo b

    novas_rels, novas_midias = [], {}
    usou_fig1 = False
    prox = {"rid": 100, "img": 1, "doc": 100}
    out = []
    ref_mode = False
    buf = []

    def flush():
        nonlocal buf
        if buf:
            txt = " ".join(x.strip() for x in buf)
            out.append(p_ref(txt) if ref_mode else p_corpo(txt))
            buf = []

    i = 0
    while i < len(linhas):
        s = linhas[i].strip()
        i += 1
        if not s:
            flush()
            continue
        if s.startswith("# ") and not out:
            titulo = esc(s[2:].strip())
            ini[0] = re.sub(r'(<w:t xml:space="preserve">).*?(</w:t>)',
                            lambda m: m.group(1) + titulo + m.group(2), ini[0], count=1, flags=re.S)
            continue
        if s.startswith("###"):
            flush()
            out.append(p_titulo(s.lstrip("#").strip(), False))
            continue
        if s.startswith("## "):
            flush()
            t = s[3:].strip()
            if t[:1].isdigit():
                out.append(p_titulo(t, False))
            else:
                out.append(p_titulo(t, True, quebra=t.upper().startswith("AP\u00caNDICE A")))
            ref_mode = t.upper().startswith("REFER\u00caNCIAS")
            continue
        if s.startswith("[[FIGURA"):
            flush()
            partes = [x.strip() for x in s[2:-2].split("|")]
            num = partes[0].split()[1]
            titulo, arq, fonte = partes[1], partes[2], partes[3]
            out.append(p_legenda(f"Figura {num} \u2013 {titulo}"))
            if arq == FIG_ESPECIAL:
                usou_fig1 = True
                out.append(fig04_lado_a_lado(fig1))
            else:
                f = FIGURAS / arq
                w, h = png_dim(f)
                cx = min(MAX_W, round(LARG_CM.get(arq[:5], 16) * CM))
                cy = round(cx * h / w)
                if cy > MAX_H:
                    cy = MAX_H
                    cx = round(cy * w / h)
                nome = f"img{prox['img']:02d}.png"
                rid = f"rId{prox['rid']}"
                novas_rels.append((rid, nome))
                novas_midias[f"word/media/{nome}"] = f.read_bytes()
                out.append(p_imagem(drawing(rid, nome, prox["doc"], cx, cy)))
                prox["rid"] += 1
                prox["img"] += 1
                prox["doc"] += 1
            out.append(p_fonte(fonte))
            continue
        if s.startswith(("[[QUADRO", "[[TABELA")):
            flush()
            partes = [x.strip() for x in s[2:-2].split("|")]
            tipo, num = partes[0].split()[0].capitalize(), partes[0].split()[1]
            titulo, fonte = partes[1], partes[2]
            out.append(p_legenda(f"{tipo} {num} \u2013 {titulo}"))
            while i < len(linhas) and not linhas[i].strip():
                i += 1
            if i < len(linhas) and linhas[i].strip().startswith("```"):
                i += 1
                cod = []
                while i < len(linhas) and not linhas[i].strip().startswith("```"):
                    cod.append(linhas[i])
                    i += 1
                i += 1
                while True:
                    j = i
                    while j < len(linhas) and not linhas[j].strip():
                        j += 1
                    if j < len(linhas) and linhas[j].strip().startswith("```"):
                        i = j + 1
                        cod.append("")
                        while i < len(linhas) and not linhas[i].strip().startswith("```"):
                            cod.append(linhas[i])
                            i += 1
                        i += 1
                    else:
                        break
                out.append(tabela_codigo("\n".join(cod)))
            else:
                rows = []
                while i < len(linhas) and linhas[i].strip().startswith("|"):
                    r = split_row(linhas[i])
                    i += 1
                    if not eh_separador(r):
                        rows.append(r)
                if not rows:
                    raise SystemExit("quadro sem tabela nem bloco de codigo")
                out.append(tabela(rows))
            out.append(p_fonte(fonte))
            continue
        if s.startswith("Palavras-chave:") or s.startswith("Keywords:"):
            flush()
            out.append(p_chave(s))
            continue
        if s.startswith("*Process Digitalization"):
            flush()
            out.append(para(runs(s.strip("*"), b=True, i=True), after=120, jc="center"))
            continue
        buf.append(s)
    flush()

    rels = zin.read("word/_rels/document.xml.rels").decode("utf-8")
    if not usou_fig1:
        rels = re.sub(r'<Relationship Id="rId[78]"[^>]*media/image[12]\.png"/>', "", rels)
    rels = rels.replace("</Relationships>", "".join(
        f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
        f'relationships/image" Target="media/{n}"/>' for rid, n in novas_rels) + "</Relationships>")
    ct = zin.read("[Content_Types].xml").decode("utf-8")
    if 'Extension="png"' not in ct:
        ct = ct.replace("</Types>", '<Default ContentType="image/png" Extension="png"/></Types>')

    novo_doc = raiz + "".join(ini) + "".join(out) + sect + "</w:body></w:document>"

    saida.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(saida, "w", zipfile.ZIP_DEFLATED) as zo:
        zo.writestr("[Content_Types].xml", ct)
        for info in zin.infolist():
            n = info.filename
            if n in ("[Content_Types].xml", "word/document.xml", "word/_rels/document.xml.rels"):
                continue
            if n in ("word/media/image1.png", "word/media/image2.png") and not usou_fig1:
                continue
            zo.writestr(n, zin.read(n))
        zo.writestr("word/_rels/document.xml.rels", rels)
        zo.writestr("word/document.xml", novo_doc)
        for n, b in novas_midias.items():
            zo.writestr(n, b)
    print(f"ok: {saida} ({len(out)} blocos, {len(novas_rels)} imagens novas)")


if __name__ == "__main__":
    main()
