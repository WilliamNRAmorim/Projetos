# -*- coding: utf-8 -*-
"""Gera o catálogo visual de peças (Magnatech 225-II e RB2).

Rodar de novo regenera tudo:
  python -X utf8 gerar_catalogo.py            (tudo)
  python -X utf8 gerar_catalogo.py --extrair  (só extração, mostra estatística)

Etapas: 1) lê tabelas e balões dos PDFs vetoriais; 2) medidas, tipo e nome PT;
3) recortes e páginas marcadas; 4) atlas por tipo; 5) planilha; 6) log.
"""
import sys, os, re, json, time, math, csv, unicodedata
from collections import defaultdict, Counter
import numpy as np
import pymupdf

BASE = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE)
DADOS = "dados"

# id, arquivo, pasta de imagens, rótulo, máquina, tem texto vetorial
MANUAIS = [
    ("COMUM26", "Magnatech - 225-II COMMON PARTS SECTION - 09-2026.pdf",
     "Magnatech - 225-II COMMON PARTS SECTION - 09-2026", "COMUM rev 09-2026", "225-II COMUM"),
    ("COMUM18", "262-EN - 225-II - COMMON PARTS SECTION - 01-2018.pdf",
     "262-EN - 225-II - COMMON PARTS SECTION -", "COMUM rev 01-2018", "225-II COMUM"),
    ("24C", "262-EN - 225-II - 24C PARTS SECTION - 01-2025.pdf",
     "262-EN - 225-II - 24C PARTS SECTION - 01", "24C rev 01-2025", "225-II 24C"),
    ("20C", "225-II 20C Parts List.pdf", "225-II 20C Parts List", "20C rev 10-2017", "225-II 20C"),
    ("RB2", "RB2 24C Parts List 2022.pdf", "RB2 24C Parts List 2022", "RB2 24C 2022", "RB2 24C"),
]
M261 = ("261", None, "261-EN 225-II Parts List -06-09", "261-EN (escaneado)", "225-II (261-EN)")
PRIOR = ["COMUM26", "COMUM18", "24C", "20C", "RB2", "261"]

# ------------------------------------------------------------------ texto
def palavras(page):
    """Palavras da página sem o texto duplicado (fonte 'negrito' sobreposta).
    Devolve linhas: [(y, [(x0,y0,x1,y1,texto), ...])] ordenadas."""
    raw = page.get_text("rawdict")
    chars, vistos, girados = [], {}, []
    for b in raw["blocks"]:
        for l in b.get("lines", []):
            if abs(l["dir"][1]) > 0.2:      # texto girado (balões em desenhos girados): palavra inteira
                t = "".join(c["c"] for s in l["spans"] for c in s["chars"]).strip()
                bb = l["bbox"]
                if t and not any(e[4] == t and abs(e[0] - bb[0]) < 1.5 and abs(e[1] - bb[1]) < 1.5 for e in girados):
                    girados.append((bb[0], bb[1], bb[2], bb[3], t))
                continue
            for s in l["spans"]:
                for c in s["chars"]:
                    ch = c["c"]
                    if ch.isspace():
                        continue
                    x0, y0, x1, y1 = c["bbox"]
                    k = (ch, int(x0 // 2), int(y0 // 2))
                    dup = False
                    for dx in (-1, 0, 1):
                        for dy in (-1, 0, 1):
                            for o in vistos.get((ch, k[1] + dx, k[2] + dy), ()):
                                if abs(o[0] - x0) < 1.0 and abs(o[1] - y0) < 1.0:
                                    dup = True
                    if dup:
                        continue
                    vistos.setdefault(k, []).append((x0, y0))
                    chars.append((ch, x0, y0, x1, y1))
    chars.sort(key=lambda c: (c[2] + c[4]) / 2)
    linhas, cur, ref = [], [], None
    for c in chars:
        ym = (c[2] + c[4]) / 2
        if ref is None or abs(ym - ref) <= 3:
            cur.append(c)
            ref = ym if ref is None else (ref + ym) / 2
        else:
            linhas.append(cur); cur = [c]; ref = ym
    if cur:
        linhas.append(cur)
    saida = []
    for ln in linhas:
        ln.sort(key=lambda c: c[1])
        ws, w = [], None
        for ch, x0, y0, x1, y1 in ln:
            if w and x0 - w[2] <= 1.8:
                w[0] = min(w[0], x0); w[1] = min(w[1], y0); w[2] = max(w[2], x1)
                w[3] = max(w[3], y1); w[4] += ch
            else:
                if w: ws.append(tuple(w))
                w = [x0, y0, x1, y1, ch]
        if w: ws.append(tuple(w))
        y = sum((a[1] + a[3]) / 2 for a in ws) / len(ws)
        saida.append((y, ws))
    for w in girados:
        saida.append(((w[1] + w[3]) / 2, [w]))
    saida.sort(key=lambda t: t[0])
    return saida


def texto_linha(ws):
    return " ".join(w[4] for w in ws)

ITEM_RE = re.compile(r"^\d{1,3}[A-Za-z]?$")
TITULO_RE = re.compile(r"^(?:[A-Z]{1,3}\d?-[0-9][0-9A-Z-]*\s*[–\-]\s*\S.*|.*\s[–\-]\s*[A-Z]{1,3}\d?-?[0-9][0-9A-Z-]*)$")


def achar_cabecalho(linhas):
    """Cabeçalhos de tabela: lista de (y, dict colunas). Formato A: Item/PART NO./DESCRIPTION/Quantity.
    Formato B (RB2 plate): NO./PART NO./PART NAME."""
    res = []
    for y, ws in linhas:
        t = [w[4] for w in ws]
        if "PART" in t and "DESCRIPTION" in t and "Item" in t:
            d = {"fmt": "A"}
            for w in ws:
                if w[4] == "PART" and "part" not in d: d["part"] = w[0]
                if w[4] == "DESCRIPTION": d["desc"] = w[0]
                if w[4] == "Quantity": d["qty"] = (w[0] + w[2]) / 2
                if w[4] in ("UM", "U"): d["um"] = w[0]
            res.append((y, d))
        elif "PART" in t and "NAME" in t and "NO." in t and "Item" not in t:
            d = {"fmt": "B"}
            for w in ws:
                if w[4] == "PART" and "part" not in d: d["part"] = w[0]
            res.append((y, d))
    return res


def linhas_tabela(linhas, y_ini, y_fim, cab):
    """Lê linhas de dados de uma tabela. Retorna lista de dict(item,codigo,desc,qtd,um,y)."""
    xp = cab["part"]
    rows = []
    ultimo_y = None
    for y, ws in linhas:
        if y <= y_ini + 1 or y >= y_fim or y > 722:
            continue
        txt = [w[4] for w in ws]
        if all(t in ("Number", "M", "Qty", "NO.") for t in txt):
            continue
        item = [w for w in ws if w[0] < xp - 12]
        resto = [w for w in ws if w[0] >= xp - 12]
        if item and ITEM_RE.match(item[0][4]) and resto:
            if cab["fmt"] == "A":
                xd = xp + 58
                cod = [w for w in resto if w[0] < xd]
                desc = [w for w in resto if w[0] >= xd]
                xq = cab.get("qty", 9999) - 14
                xu = cab.get("um", 9999) - 8
                qtd = [w for w in desc if xq <= w[0] < xu]
                um = [w for w in desc if w[0] >= xu]
                desc = [w for w in desc if w[0] < xq]
                if not cod:
                    continue
                rows.append(dict(item=item[0][4], codigo="".join(w[4] for w in cod),
                                 desc=texto_linha(desc), qtd=texto_linha(qtd), um=texto_linha(um), y=y))
            else:
                cod = resto[0]
                desc = resto[1:]
                rows.append(dict(item=item[0][4], codigo=cod[4], desc=texto_linha(desc),
                                 qtd="", um="", y=y))
            ultimo_y = y
        elif not item and rows and ultimo_y is not None and y - ultimo_y < 15 \
                and all(w[0] >= xp + 40 for w in ws) and not any(re.match(r"^[A-Z]{1,3}\d?-\d", w[4]) and w[0] < xp + 50 for w in ws):
            # continuação de descrição
            if cab["fmt"] == "A":
                xq = cab.get("qty", 9999) - 14
                ws = [w for w in ws if w[0] < xq]
            if ws:
                rows[-1]["desc"] += " " + texto_linha(ws)
                ultimo_y = y
        elif rows and cab["fmt"] == "A":
            # linha de outra coisa: encerra a tabela
            if not item:
                continue
            break
    return rows


def limpar_titulo(t):
    t = re.sub(r"\s*\(continued\)", "", t, flags=re.I)
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"\s[–\-]\s", " – ", t)
    return t

# ------------------------------------------------------------------ geometria
def geometria(page):
    """Segmentos de linha e pontos candidatos a círculo de balão."""
    segs = []   # x0,y0,x1,y1,largura
    pts = []    # pontos para ajuste de círculo
    filled = []
    for d in page.get_drawings():
        for it in d["items"]:
            if it[0] == "l":
                p, q = it[1], it[2]
                L = math.hypot(q.x - p.x, q.y - p.y)
                if d["type"] in ("s", "fs"):
                    segs.append((p.x, p.y, q.x, q.y, d.get("width") or 0))
                if L < 8:
                    pts.append(((p.x + q.x) / 2, (p.y + q.y) / 2))
            elif it[0] == "c":
                p1, p2, p3, p4 = it[1:5]
                t = .5
                x = (p1.x + 3 * p2.x + 3 * p3.x + p4.x) / 8
                y = (p1.y + 3 * p2.y + 3 * p3.y + p4.y) / 8
                pts.append((x, y)); pts.append((p1.x, p1.y)); pts.append((p4.x, p4.y))
    return np.array(segs, float).reshape(-1, 5), np.array(pts, float).reshape(-1, 2)


def _circ3(a, b, c):
    ax, ay = a; bx, by = b; cx, cy = c
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    if abs(d) < 1e-6:
        return None
    ux = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
    uy = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
    return ux, uy, math.hypot(ax - ux, ay - uy)


def ajusta_circulo(P, c0, rmax=16, iters=250):
    """RANSAC + Kasa: circulo do balão perto de c0. Devolve (cx,cy,R,n) ou None."""
    if len(P) < 12:
        return None
    rng = np.random.default_rng(1)
    melhor, mi = None, None
    for _ in range(iters):
        idx = rng.choice(len(P), 3, replace=False)
        c = _circ3(P[idx[0]], P[idx[1]], P[idx[2]])
        if not c or not (4.0 <= c[2] <= rmax) or math.hypot(c[0] - c0[0], c[1] - c0[1]) > 7:
            continue
        dist = np.hypot(P[:, 0] - c[0], P[:, 1] - c[1])
        inl = np.abs(dist - c[2]) < 0.6
        n = int(inl.sum())
        if melhor is None or n > melhor:
            melhor, mi = n, inl
    if melhor is None or melhor < 12:
        return None
    sel = P[mi]
    A = np.c_[sel[:, 0], sel[:, 1], np.ones(len(sel))]
    b = -(sel[:, 0] ** 2 + sel[:, 1] ** 2)
    a, bb, c = np.linalg.lstsq(A, b, rcond=None)[0]
    cx, cy = -a / 2, -bb / 2
    v = cx * cx + cy * cy - c
    if v <= 0:
        return None
    R = math.sqrt(v)
    dist = np.hypot(P[:, 0] - cx, P[:, 1] - cy)
    sel = P[np.abs(dist - R) < 0.7]
    ang = np.sort(np.arctan2(sel[:, 1] - cy, sel[:, 0] - cx))
    gaps = np.diff(np.r_[ang, ang[0] + 2 * math.pi])
    if len(sel) < 12 or gaps.max() > 2.4:
        return None
    return cx, cy, R, len(sel)


def linha_de_chamada(segs, cx, cy, R, circulos):
    """Segue a linha de chamada que sai do círculo. Devolve lista de pontos [(x,y)...] ou []."""
    if len(segs) == 0:
        return []
    p = segs[:, :2]; q = segs[:, 2:4]
    comp = np.hypot(q[:, 0] - p[:, 0], q[:, 1] - p[:, 1])
    d1 = np.hypot(p[:, 0] - cx, p[:, 1] - cy)
    d2 = np.hypot(q[:, 0] - cx, q[:, 1] - cy)
    cand = []
    for i in range(len(segs)):
        if comp[i] < 2.5:
            continue
        a_perto = abs(d1[i] - R) <= 1.7
        b_perto = abs(d2[i] - R) <= 1.7
        if a_perto == b_perto:
            continue
        if a_perto and d2[i] > R + 2.5:
            cand.append((abs(d1[i] - R), -comp[i], i, False))
        elif b_perto and d1[i] > R + 2.5:
            cand.append((abs(d2[i] - R), -comp[i], i, True))
    if not cand:
        return []
    cand.sort()
    _, _, i, inv = cand[0]
    w0 = segs[i, 4]
    cadeia = [(segs[i, 2], segs[i, 3])] if not inv else [(segs[i, 0], segs[i, 1])]
    usados = {i}
    # ponto inicial na borda do círculo
    ini = (segs[i, 0], segs[i, 1]) if not inv else (segs[i, 2], segs[i, 3])
    cadeia = [ini] + cadeia
    for _ in range(6):
        ex, ey = cadeia[-1]
        achou = []
        for j in range(len(segs)):
            if j in usados or comp[j] < 2.0:
                continue
            if abs(segs[j, 4] - w0) > 0.35 * max(w0, 0.1):
                continue
            if math.hypot(p[j, 0] - ex, p[j, 1] - ey) < 1.0:
                achou.append((j, (q[j, 0], q[j, 1])))
            elif math.hypot(q[j, 0] - ex, q[j, 1] - ey) < 1.0:
                achou.append((j, (p[j, 0], p[j, 1])))
        achou = [a for a in achou
                 if not any(abs(math.hypot(a[1][0] - c[0], a[1][1] - c[1]) - c[2]) < 2 for c in circulos)]
        if len(achou) != 1:
            break
        usados.add(achou[0][0])
        cadeia.append(achou[0][1])
    return cadeia


def baloes_da_pagina(page, linhas):
    """Balões: lista de dict(num, cx, cy, R, cadeia)."""
    segs, pts = geometria(page)
    if len(pts) == 0:
        return []
    cands = []
    for y, ws in linhas:
        for w in ws:
            if re.fullmatch(r"\d{1,3}", w[4]):
                cands.append(w)
    achados, circ = [], []
    for w in cands:
        c0 = ((w[0] + w[2]) / 2, (w[1] + w[3]) / 2)
        d = np.hypot(pts[:, 0] - c0[0], pts[:, 1] - c0[1])
        r = ajusta_circulo(pts[d < 13], c0, 9.5, 300) or ajusta_circulo(pts[d < 22], c0, 16, 600)
        if r:
            achados.append((w, r)); circ.append(r)
    saida = []
    for w, (cx, cy, R, n) in achados:
        cad = linha_de_chamada(segs, cx, cy, R, [c for c in circ if c[:2] != (cx, cy)])
        saida.append(dict(num=w[4], cx=cx, cy=cy, R=R, cadeia=cad))
    return saida

# ------------------------------------------------------------------ extração dos manuais
def titulo_acima(linhas, yc):
    """Último título acima do cabeçalho; junta linhas quando o título quebra depois de um traço."""
    acima = [(y, texto_linha(ws)) for y, ws in linhas if y < yc - 1]
    k = None
    for i, (y, t) in enumerate(acima):
        if ("Parts List" not in t) and (TITULO_RE.match(t) or (t.endswith(("–", "-")) and len(t) > 12)):
            k = i
    if k is None:
        return ""
    tit = acima[k][1]
    i = k
    while tit.endswith(("–", "-")) and i + 1 < len(acima) and acima[i + 1][0] - acima[i][0] < 26:
        i += 1
        tit += " " + acima[i][1]
    return tit


def extrair_manual(mid, arq):
    """Retorna (paginas, linhas_da_lista, baloes_atribuidos)."""
    doc = pymupdf.open(arq)
    n = len(doc)
    blocos = []     # dicts: pagina, y, cab, rows, titulo, cont
    bal_pag = {}
    rect = {}
    titulo_ant = ""
    for pi in range(n):
        pg = doc[pi]
        rect[pi + 1] = (pg.rect.width, pg.rect.height)
        linhas = palavras(pg)
        cabs = achar_cabecalho(linhas)
        for k, (yc, cab) in enumerate(cabs):
            y_fim = cabs[k + 1][0] if k + 1 < len(cabs) else 9999
            # título: última linha-título acima do cabeçalho
            tit = titulo_acima(linhas, yc)
            if cab["fmt"] == "B":
                # RB2 plate: título = linha logo abaixo (código + nome)
                for y, ws in linhas:
                    if yc < y < yc + 40 and re.match(r"^[A-Z]{1,3}\d?-\d", ws[0][4]):
                        tit = texto_linha(ws); break
                tit = re.sub(r"^(\S+)\s+(.*)$", r"\1 – \2", tit) if tit else titulo_ant
            if not tit:
                tit = titulo_ant
            cont = bool(re.search(r"\(continued\)", tit, re.I)) or "(continued)" in tit.lower()
            rows = linhas_tabela(linhas, yc, y_fim, cab)
            titulo_ant = tit
            blocos.append(dict(pagina=pi + 1, y=yc, rows=rows, titulo=limpar_titulo(tit), cont=cont))
        if not cabs or True:
            bal = baloes_da_pagina(pg, linhas)
            if bal:
                bal_pag[pi + 1] = bal
    # grupos (conjuntos): continuação junta no anterior
    grupos = []
    for b in blocos:
        g = None
        if b["cont"] or (grupos and b["titulo"] == grupos[-1]["titulo"]):
            for gg in reversed(grupos):
                if gg["titulo"] == b["titulo"]:
                    g = gg; break
        if g is None:
            g = dict(titulo=b["titulo"], pos=(b["pagina"], b["y"]), rows=[])
            grupos.append(g)
        for r in b["rows"]:
            r = dict(r); r["pagina_lista"] = b["pagina"]
            g["rows"].append(r)
    # atribuir balões ao próximo grupo posterior
    for pgn, lista in bal_pag.items():
        for bl in lista:
            bl["pagina"] = pgn
            dono = None
            for g in grupos:
                if g["pos"] > (pgn, bl["cy"]):
                    nums = {r["item"] for r in g["rows"]}
                    if bl["num"] in nums:
                        dono = g
                    break
            bl["grupo"] = dono
    return n, rect, grupos, bal_pag



# ------------------------------------------------------------------ medidas
NUM = r"(?:\d+\s?-\s?\d+/\d+|\d+\s\d+/\d+|\d+/\d+|\d*\.\d+|\d+)"


def para_pol(s):
    """'1-1/2' -> 1.5 ; '3/8' -> .375 ; '.50' -> .5 ; '1 1/4' -> 1.25"""
    s = s.strip().replace("..", ".")
    m = re.fullmatch(r"(\d+)\s?-?\s?(\d+)/(\d+)", s)
    if m:
        return int(m.group(1)) + int(m.group(2)) / int(m.group(3))
    m = re.fullmatch(r"(\d+)/(\d+)", s)
    if m:
        return int(m.group(1)) / int(m.group(2))
    return float(s)


def r4(v):
    return round(v, 4)


def parse_medidas(desc, tipo=""):
    """Extrai medidas de uma descrição. Polegadas como número."""
    d = " " + desc.upper().replace("..", ".").replace("*", " ") + " "
    m = {}

    def num(g):
        return para_pol(g)

    def achar(chave, sufixo):
        r = re.search(r"(%s)\s*(MM)?\s*%s\b" % (NUM, sufixo), d)
        if r:
            v = num(r.group(1))
            if r.group(2):
                v = v / 25.4
            m[chave] = r4(v)
            return r

    achar("id_in", r"(?:I\.?D\.?|ID)")
    achar("od_in", r"(?:O\.?D\.?|OD)")
    achar("comp_in", r"(?:LG|L)")
    r = re.search(r"(%s)\s*(?:W|THICK|THK)\b" % NUM, d)
    if r:
        m["espessura_in"] = r4(num(r.group(1)))
    r = re.search(r"(%s)\s*WIRE" % NUM, d) or re.search(r"WIRE\s*(?:DIA\.?)?\s*(%s)" % NUM, d)
    if r and "SPRING" in d:
        m["fio_in"] = r4(num(r.group(1)))
    r = re.search(r"(%s)\s*FT\b" % NUM, d)
    if r:
        m["comp_in"] = r4(num(r.group(1)) * 12)
    r = re.search(r"OD\s*[xX]\s*(%s)\b" % NUM, d)
    if r and "id_in" in m and "od_in" in m:
        m.setdefault("comp_in", r4(num(r.group(1))))
    if "WASHER" in d and "id_in" in m and "od_in" in m and "espessura_in" not in m:
        r = re.search(r"OD\s*(%s)\s*$" % NUM, d.rstrip() + " ")
        if r:
            m["espessura_in"] = r4(num(r.group(1)))
    if "WASHER" in d and "id_in" not in m:
        r = re.search(r"(%s)\s*[xX]\s*(%s)\s*[xX]\s*(%s)" % (NUM, NUM, NUM), d)
        if r:
            m["id_in"], m["od_in"], m["espessura_in"] = (r4(num(r.group(i))) for i in (1, 2, 3))
    r = re.search(r"(%s)\s*DIA\b" % NUM, d)
    if r and "fio_in" not in m:
        if "O-RING" in d:
            m["espessura_in"] = r4(num(r.group(1)))
        elif "od_in" not in m:
            m["od_in"] = r4(num(r.group(1)))
    if re.search(r"\bPIN\b|DOWEL", d) and "od_in" not in m and not re.search(r"\bM\s?\d", d):
        r = re.search(r"(%s)\s*[xX]\s*(%s)" % (NUM, NUM), d)
        if r:
            m["od_in"] = r4(num(r.group(1)))
            m["comp_in"] = r4(num(r.group(2)))
    if "SHIM" in d and "espessura_in" not in m:
        r = re.search(r"(\.\d+)", d)
        if r:
            m["espessura_in"] = r4(num(r.group(1)))
    if "SPRING" in d and "od_in" not in m:
        r = re.search(r"(%s)\s*[xX]\s*(%s)\s*[xX]\s*(%s)" % (NUM, NUM, NUM), d)
        if r:
            m["dims_x"] = [r.group(i).strip() for i in (1, 2, 3)]
    # rosca
    r = re.search(r"\bM\s?(\d+(?:\.\d+)?)\s*[xX]\s*(\d*\.?\d+)(?:\s*[xX]\s*(\d*\.?\d+))?", d)
    if r and "id_in" not in m:
        if r.group(3):
            m["rosca"] = "M%sx%s" % (r.group(1), r.group(2))
            m["comp_rosca_in"] = r4(float(r.group(3)) / 25.4)
        elif re.search(r"\bPIN\b|DOWEL", d):
            m["od_in"] = r4(float(r.group(1)) / 25.4)
            m["comp_in"] = r4(float(r.group(2)) / 25.4)
        else:
            m["rosca"] = "M%s" % r.group(1)
            m["comp_rosca_in"] = r4(float(r.group(2)) / 25.4)
    elif "WASHER" in d and re.search(r"\bM\s?(\d+)\b", d):
        m["rosca"] = "M" + re.search(r"\bM\s?(\d+)\b", d).group(1)
    elif re.match(r"\s*(SCREW|NUT|STUD|FITTING|LOCKNUT|BOLT|PIN|SPRING|EYEBOLT|PLUG|RIVET|SET)", d) or "THD" in d:
        r = re.search(r"(?<![\w.#/-])(#?\d-\d{1,2}/\d{1,2}|#?\d{1,2}/\d{1,2}|#?\d{1,2})\s*-\s*(\d{1,2})\b(?!/)", d)
        if r:
            a = r.group(1).replace("#", "")
            if re.fullmatch(r"\d{1,2}", a) and int(a) <= 12:
                m["rosca"] = "#%s-%s" % (a, r.group(2))
            else:
                m["rosca"] = "%s-%s" % (a, r.group(2))
            r2 = re.search(r"\s[xX]\s*(%s)\b" % NUM, d[r.end():])
            if r2:
                m["comp_rosca_in"] = r4(num(r2.group(1)))
    if "rosca" not in m:
        r = re.search(r"(%s)\s*(NPT|FPT|MPT)\b" % NUM, d)
        if r:
            m["rosca"] = "%s NPT" % r.group(1).strip()
        else:
            r = re.search(r"(\d+/\d+)\s?P\b", d)
            if r and re.match(r"\s*(FITTING|PIPE|ELBOW|NIPPLE)", d):
                m["rosca"] = "%s NPT" % r.group(1)
    # dentes / passo
    if re.search(r"GEAR|SPROCKET|PINION|TEETH|TOOTH", d):
        r = re.search(r"(?<![/\d.])(\d+)\s*-?\s*(?:TEETH|TOOTH|T\.|T\b)", d)
        if r:
            m["dentes"] = int(r.group(1))
    if re.search(r"SPROCKET|CHAIN|GEAR", d):
        r = re.search(r"(?<![\d.])(\d+/\d+|\d*\.\d+|\d+)\s*P\b\.?", d)
        if r:
            m["passo"] = r.group(1)
    r = re.search(r"(?<!\w)-(\d{3})\b", d)
    if r and "RING" in d:
        m["oring"] = "-" + r.group(1)
    if re.search(r"\bBRG\b|BEARING|CAM FOLLOWER|\bCONE\b|\bCUP\b", d):
        pad = (r"(?<![\w./])(?:CFL-[\d/]+-[A-Z]+|[A-Z]{1,3}-\d{3,6}|[A-Z]{2,3}\d{2,6}[A-Z]?|"
               r"\d{3,5}[A-Z]{1,2}|\d{4,5}|[A-Z]\d{4,6}|TN\d+|TW\d+)(?![\w./])")
        for t in re.findall(pad, d):
            if re.fullmatch(r"\d+(?:ID|OD|LG|W|MM|DIA)", t) or t.startswith("RB-"):
                continue
            m["rolamento"] = t
            break
    if "id_in" not in m and "od_in" not in m and re.match(r"\s*(RING,?\s*RET|WASHER,?\s*(LOCK|FLAT))", d):
        r = re.search(r"(?:EXTERNAL|INTERNAL|LOCK|FLAT|RET\.?)\s+(%s)\s*$" % NUM, d.rstrip() + " ")
        if r:
            m["nominal_in"] = r4(num(r.group(1)))
    return m


def fmt_pol(v):
    s = "%.3f" % v
    if s.endswith("0"):
        s = s[:-1]
    return '%s" (%.1f mm)' % (s, v * 25.4)


def medidas_txt(m):
    p = []
    for k, rot in [("id_in", "Øint"), ("od_in", "Øext"), ("comp_in", "comp"), ("espessura_in", "esp"),
                   ("fio_in", "fio"), ("nominal_in", "nominal")]:
        if k in m:
            p.append("%s %s" % (rot, fmt_pol(m[k])))
    if "rosca" in m:
        p.append("rosca %s" % m["rosca"])
    if "comp_rosca_in" in m:
        p.append("comp. rosca %s" % fmt_pol(m["comp_rosca_in"]))
    if "dentes" in m:
        p.append("%d dentes" % m["dentes"])
    if "passo" in m:
        p.append("passo %s" % m["passo"])
    if "rolamento" in m:
        p.append("rolamento %s" % m["rolamento"])
    if "oring" in m:
        p.append("o-ring %s" % m["oring"])
    if "dims_x" in m:
        p.append("dim. " + " x ".join(m["dims_x"]))
    return " · ".join(p)


def _testes_medidas():
    t = parse_medidas
    x = t("BUSHING, DU .50ID  .59OD  .63LG")
    assert x["id_in"] == 0.5 and x["od_in"] == 0.59 and x["comp_in"] == 0.63, x
    x = t("SCREW,SOC HD CAP 3/8-16 X 1-3/4")
    assert x["rosca"] == "3/8-16" and x["comp_rosca_in"] == 1.75, x
    x = t("SCREW,SOC HD CAP 10-24 X 5/8")
    assert x["rosca"] == "#10-24" and x["comp_rosca_in"] == 0.625, x
    x = t("SCREW,SOC HD CAP M8 X 1.25 X 20")
    assert x["rosca"] == "M8x1.25" and abs(x["comp_rosca_in"] - 0.7874) < 1e-3, x
    x = t("SPROCKET 1/2 P. 60 T.")
    assert x["dentes"] == 60 and x["passo"] == "1/2", x
    x = t("IDLER SPROCKET 1/2P 23-TEETH")
    assert x["dentes"] == 23 and x["passo"] == "1/2", x
    x = t("BRG, ROLLER 1 ID x 1.31 OD x .75")
    assert x["id_in"] == 1 and x["od_in"] == 1.31 and x["comp_in"] == 0.75, x
    x = t("SEAL,OIL 1.63ID 2.38OD .31W")
    assert x["id_in"] == 1.63 and x["espessura_in"] == 0.31, x
    x = t("PIN,DOWEL .250 X 3/4")
    assert x["od_in"] == 0.25 and x["comp_in"] == 0.75, x
    x = t("SPRING,TENSION .037 WIRE DIA .25OD 1.75LG")
    assert x["fio_in"] == 0.037 and x["od_in"] == 0.25 and x["comp_in"] == 1.75, x
    assert t("CAM FOLLOWER CFL-3/4-SB")["rolamento"] == "CFL-3/4-SB"
    x = t("WASHER,FLAT .16ID .38OD .03")
    assert x["espessura_in"] == 0.03, x
    x = t("SCREW,SOC HD CAP 1-1/2-12 X 2")
    assert x["rosca"] == "1-1/2-12", x
    assert t("RING,RET EXTERNAL 1-11/16")["nominal_in"] == 1.6875
    assert t("BEARING,BALL 6203")["rolamento"] == "6203"


_testes_medidas()

# ------------------------------------------------------------------ tipo e nome em português
TIPOS = ["Parafuso", "Porca", "Arruela", "Anel de retenção", "Pino", "Chaveta", "Mola", "Rolamento",
         "Bucha / luva", "Eixo", "Engrenagem", "Roda dentada", "Corrente / elo", "Polia", "Correia",
         "Rolete / roda", "Came / seguidor", "Espaçador", "Vedação / o-ring / retentor",
         "Graxeira / conexão", "Acoplamento", "Embreagem", "Trava / trinco / lingueta",
         "Alavanca / braço / haste", "Placa / chapa / pad", "Suporte / bracket",
         "Carcaça / housing / bloco", "Tampa / guarda", "Tubo / mangueira",
         "Elétrico / sensor / motor", "Ferramenta", "Conjunto (montagem)", "Outro"]

# palavra-chave (cabeça da descrição) -> tipo
CABECA = {
    "SCREW": "Parafuso", "BOLT": "Parafuso", "EYEBOLT": "Parafuso", "STUD": "Parafuso", "RIVET": "Parafuso",
    "NUT": "Porca", "LOCKNUT": "Porca",
    "WASHER": "Arruela", "RING": "Anel de retenção", "CIRCLIP": "Anel de retenção",
    "PIN": "Pino", "DOWEL": "Pino", "KEY": "Chaveta", "SPRING": "Mola",
    "BRG": "Rolamento", "BEARING": "Rolamento", "CONE": "Rolamento", "CUP": "Rolamento",
    "BUSHING": "Bucha / luva", "SLEEVE": "Bucha / luva", "LINER": "Bucha / luva",
    "SHAFT": "Eixo", "AXLE": "Eixo", "TRUNION": "Eixo", "TRUNNION": "Eixo",
    "GEAR": "Engrenagem", "PINION": "Engrenagem",
    "SPROCKET": "Roda dentada", "CHAIN": "Corrente / elo", "PULLEY": "Polia", "BELT": "Correia",
    "ROLLER": "Rolete / roda", "CAM": "Came / seguidor", "ECCENTRIC": "Came / seguidor",
    "FOLLOWER": "Came / seguidor",
    "SPACER": "Espaçador", "SHIM": "Espaçador", "COLLAR": "Espaçador",
    "SEAL": "Vedação / o-ring / retentor", "O-RING": "Vedação / o-ring / retentor",
    "GASKET": "Vedação / o-ring / retentor", "FITTING": "Graxeira / conexão", "FITTINH": "Graxeira / conexão",
    "ADAPTER": "Graxeira / conexão", "ADAPTOR": "Graxeira / conexão", "NIPPLE": "Graxeira / conexão",
    "CONNECTOR": "Graxeira / conexão", "QUICK": "Graxeira / conexão", "PLUG": "Graxeira / conexão",
    "COUPLING": "Acoplamento", "CLUTCH": "Embreagem",
    "LATCH": "Trava / trinco / lingueta", "PAWL": "Trava / trinco / lingueta", "LOCK": "Trava / trinco / lingueta",
    "LOCKPLATE": "Trava / trinco / lingueta", "RELEASE": "Trava / trinco / lingueta",
    "CLIP": "Trava / trinco / lingueta", "RETAINER": "Trava / trinco / lingueta",
    "HOOK": "Trava / trinco / lingueta", "STOP": "Trava / trinco / lingueta", "TANG": "Trava / trinco / lingueta",
    "LEVER": "Alavanca / braço / haste", "ARM": "Alavanca / braço / haste", "HANDLE": "Alavanca / braço / haste",
    "ROD": "Alavanca / braço / haste", "LINK": "Alavanca / braço / haste", "CRANK": "Alavanca / braço / haste",
    "YOKE": "Alavanca / braço / haste", "PLUNGER": "Alavanca / braço / haste",
    "COMPENSATOR": "Alavanca / braço / haste", "BAR": "Alavanca / braço / haste",
    "BALER": "Alavanca / braço / haste", "END": "Alavanca / braço / haste",
    "PLATE": "Placa / chapa / pad", "NAMEPLATE": "Placa / chapa / pad", "SLIPPER": "Placa / chapa / pad",
    "PAD": "Placa / chapa / pad", "STRIP": "Placa / chapa / pad", "SLIDER": "Placa / chapa / pad",
    "DISC": "Placa / chapa / pad", "SEGMENT": "Placa / chapa / pad", "TAG": "Placa / chapa / pad",
    "BRACKET": "Suporte / bracket", "SUPPORT": "Suporte / bracket", "MOUNT": "Suporte / bracket",
    "MOUNTING": "Suporte / bracket", "POST": "Suporte / bracket", "HOLDER": "Suporte / bracket",
    "BASE": "Suporte / bracket", "FRAME": "Suporte / bracket", "RAIL": "Suporte / bracket",
    "STRAP": "Suporte / bracket", "GUIDE": "Suporte / bracket", "TRACK": "Suporte / bracket",
    "HOUSING": "Carcaça / housing / bloco", "BOX": "Carcaça / housing / bloco", "GEARBOX": "Carcaça / housing / bloco",
    "CASING": "Carcaça / housing / bloco", "CARTRIDGE": "Carcaça / housing / bloco",
    "BLOCK": "Carcaça / housing / bloco", "HUB": "Carcaça / housing / bloco",
    "MANIFOLD": "Carcaça / housing / bloco", "RESERVOIR": "Carcaça / housing / bloco",
    "ROTOR": "Carcaça / housing / bloco", "SHUTTLE": "Carcaça / housing / bloco",
    "PUMP": "Carcaça / housing / bloco", "FILTER": "Carcaça / housing / bloco",
    "COVER": "Tampa / guarda", "GUARD": "Tampa / guarda", "SHIELD": "Tampa / guarda", "CAP": "Tampa / guarda",
    "DEFLECTOR": "Tampa / guarda", "DOOR": "Tampa / guarda", "SPLASH": "Tampa / guarda",
    "TUBE": "Tubo / mangueira", "TUBING": "Tubo / mangueira", "PIPE": "Tubo / mangueira", "HOSE": "Tubo / mangueira",
    "STRAP/COLLAR": "Suporte / bracket", "EYELET": "Outro", "E": "Elétrico / sensor / motor", "SWITCH": "Elétrico / sensor / motor", "SENSOR": "Elétrico / sensor / motor",
    "MOTOR": "Elétrico / sensor / motor", "SOLENOID": "Elétrico / sensor / motor",
    "PICK-UP": "Elétrico / sensor / motor", "PROBE": "Elétrico / sensor / motor",
    "WIRE": "Elétrico / sensor / motor", "CABLE": "Elétrico / sensor / motor",
    "OPERATOR": "Elétrico / sensor / motor",
    "TOOL": "Ferramenta", "WRENCH": "Ferramenta", "BEARINGSTRIP": "Placa / chapa / pad",
}
# tradução de termos em inglês (RB2 vem em Title Case): palavra -> cabeça equivalente
EXTRA_CABECA = {"HEADLESS": "SCREW", "LOCKWASHER": "WASHER", "LOCKNUT": "NUT", "PINION": "GEAR",
                "SOCKET": "SCREW", "HEX": "NUT", "RETAINING": "RING", "OIL": "SEAL", "GREASE": "FITTING",
                "CHECK": "FITTING", "DOWEL": "PIN", "ROLL": "PIN", "COTTER": "PIN", "KEYED": "WASHER",
                "RADIAL": "BEARING", "THRUST": "BEARING", "NEEDLE": "BEARING", "BALL": "BEARING",
                "TIMKEN": "BEARING", "CLAMPING": "RING", "LOCKING": "RING", "SPLIT": "GEAR",
                "COMPOUND": "GEAR", "DRIVE": "SHAFT", "OUTPUT": "SHAFT", "INPUT": "SHAFT",
                "WORM": "GEAR", "TIMING": "PULLEY", "SET": "SCREW"}


def tipo_de(desc):
    d = desc.upper().strip()
    d = re.sub(r"\s+", " ", d)
    toks = [t for t in re.split(r"[,\s]+", d) if t]
    if not toks:
        return "Outro"
    if re.search(r"\bASS(?:Y|EMBLY)\b|ASS'Y|\bSYSTEM\b", d) and toks[0] not in ("SCREW", "WASHER", "NUT"):
        return "Conjunto (montagem)"
    if toks[0] == "GEAR" and re.search(r"\bBOX\b|\bBOX COVER", d[:12]) or d.startswith(("GEAR BOX", "GEARBOX")):
        return "Carcaça / housing / bloco" if "COVER" not in d else "Tampa / guarda"
    if d.startswith("BOX,GEAR") or d.startswith("LOWER CHANGE GEAR BOX") or d.startswith("POWER FORMER GEAR BOX HOUSING"):
        return "Carcaça / housing / bloco"
    if re.match(r"(GEAR BOX|CHANGE GEAR BOX|BOX)", d) and "COVER" in d:
        return "Tampa / guarda"
    if toks[0] in ("COVER",) or (len(toks) > 1 and toks[1] == "COVER" and toks[0] in ("GEAR", "GEARBOX")):
        return "Tampa / guarda"
    if toks[0] == "GEAR" and len(toks) > 1 and toks[1] in ("SET",):
        return "Engrenagem"
    if toks[0] == "RING" and not re.search(r"RET", d):
        return "Anel de retenção" if "SNAP" in d else "Trava / trinco / lingueta"
    if toks[0] == "RET.":
        return "Placa / chapa / pad"
    if toks[0] in ("SPACER", "SLEEVE") and "WASHER" in d[:20]:
        return "Espaçador"
    if toks[0] == "SLEEVE" and len(toks) > 1 and toks[1] == "SPACER":
        return "Espaçador"
    if toks[0] == "WASHER" and len(toks) > 1 and toks[1] == "SPACER":
        return "Espaçador"
    if toks[0] == "SPACER" and len(toks) > 1 and toks[1] == "WASHER":
        return "Espaçador"
    if toks[0] == "CLUTCH" and "SPRING" in toks[:3]:
        return "Mola"
    if toks[0] in ("TENSION", "PLUG") and "SPRING" in toks[:3]:
        return "Mola" if toks[0] == "PLUG" and False else ("Carcaça / housing / bloco" if "HOUSING" in toks else "Alavanca / braço / haste")
    if d.startswith("CAM FOLLOWER") or d.startswith("BRG,CAM FOLLOWER"):
        return "Came / seguidor"
    if toks[0] == "BEARING" and re.search(r"LOCK ?NUT", d):
        return "Porca"
    if toks[0] == "BEARING" and re.search(r"LOCK ?WASHER", d):
        return "Arruela"
    if toks[0] == "BEARING" and "CARTRIDGE" in d:
        return "Carcaça / housing / bloco"
    if re.match(r"TRACK ROLLER|ROLLER", d):
        return "Rolete / roda"
    if toks[0] == "E" and re.match(r"E,\s*(CLAMP|MISC|CONDUIT|LUG|CONNECTOR COUPLING)", d):
        return "Graxeira / conexão" if "CONNECTOR" in d or "CONDUIT" in d else "Suporte / bracket" if "CLAMP" in d else "Elétrico / sensor / motor"
    if toks[0] == "IDLER" and "SPROCKET" in d:
        return "Roda dentada"
    if toks[0] == "ROTOR" and "GEAR" in toks:
        return "Engrenagem"
    if toks[0] == "PUMP" and "GEAR" in toks:
        return "Carcaça / housing / bloco"
    if toks[0] == "TUBE" and "FEED" in toks:
        return "Tubo / mangueira"
    if toks[0] == "BOBBIN" or toks[0] == "PIPE" and "PLUG" in toks:
        return "Graxeira / conexão" if toks[0] == "PIPE" else "Carcaça / housing / bloco"
    if toks[0] == "PIPE" and "SEALANT" in toks:
        return "Outro"
    if toks[0] == "GAUGE":
        return "Outro"
    if toks[0] == "QUICK":
        return "Graxeira / conexão"
    h = toks[0]
    if h in CABECA:
        return CABECA[h]
    if h in EXTRA_CABECA:
        return CABECA[EXTRA_CABECA[h]]
    # procura qualquer palavra conhecida na descrição (prioridade pela ordem)
    for t in toks[1:]:
        if t in CABECA and t not in ("E", "END", "CAP", "SET", "BAR", "TRACK", "GUIDE", "STOP"):
            return CABECA[t]
    for t in toks[1:]:
        if t in CABECA:
            return CABECA[t]
    return "Outro"


# --- nome em português
TERMOS = [  # (regex em maiúsculas, tradução) aplicados em ordem; os mais longos primeiro
    (r"SOC(?:KET)? HD CAP", "Allen cabeça cilíndrica"), (r"SOCKET HEAD CAP", "Allen cabeça cilíndrica"),
    (r"BUTTON SOC HD CAP", "Allen cabeça abaulada (button)"), (r"SET HEX SOC CUP", "de pressão Allen ponta copo (set)"),
    (r"HEX HD CAP", "sextavado"), (r"PAN HD(?: |$)", "cabeça panela "), (r"PAN HEAD", "cabeça panela"),
    (r"RD HD", "cabeça redonda"), (r"ROUND HEAD", "cabeça redonda"), (r"FLAT HD", "cabeça chata"),
    (r"MACHINE", "(máquina)"), (r"TAPPING", "autoatarraxante"), (r"SHOULDER", "de ombro"),
    (r"SELF-LOCKING", "autotravante"), (r"JAM", "fina (jam)"), (r"SQUARE", "quadrada"),
    (r"HEX", "sextavada"), (r"CAD-PLATED", "cadmiada"), (r"GALVANIZED|GALV", "galvanizado"),
]
MODS = {
    "STEEL": "de aço", "URETHANE": "de uretano", "BRASS": "de latão", "ALUMINUM": "de alumínio",
    "PLASTIC": "de plástico", "COPPER": "de cobre", "BRONZE": "de bronze", "NYLON": "de náilon",
    "RUBBER": "de borracha", "ADIPRENE": "de adiprene", "HARDENED": "endurecido", "TRACK": "da pista",
    "REAR": "traseiro", "FRONT": "dianteiro", "INNER": "interno", "OUTER": "externo", "LEADING": "dianteiro",
    "TRAILING": "traseiro", "UPPER": "superior", "LOWER": "inferior", "TOP": "superior", "LEFT": "esquerdo",
    "RIGHT": "direito", "CARRIER": "do carrier", "BOBBIN": "da bobina", "YARN": "do fio", "WIRE": "de arame",
    "SHUTTLE": "do shuttle", "OIL": "de óleo", "GREASE": "de graxa", "CLUTCH": "da embreagem",
    "MOUNTING": "de montagem", "SUPPORT": "de suporte", "GUIDE": "guia", "DRIVE": "de acionamento",
    "ADJUSTING": "de ajuste", "ADJUSTABLE": "ajustável", "SPECIAL": "especial", "STATIONARY": "fixo",
    "MOVABLE": "móvel", "CABLE": "de cabo", "SENSOR": "do sensor", "PIVOT": "de pivô",
    "PINION": "do pinhão", "ECCENTRIC": "do excêntrico", "ROTOR": "do rotor", "DECK": "do deck",
    "FOR": "p/", "F/": "p/", "WITH": "c/", "W/": "c/", "AND": "e", "&": "e", "OF": "de",
    "GEAR BOX": "da caixa de engrenagens", "GEARBOX": "da caixa de engrenagens",
}
NOMES = {
    "SCREW": "Parafuso", "NUT": "Porca", "WASHER": "Arruela", "PIN": "Pino", "KEY": "Chaveta",
    "BRG": "Rolamento", "BEARING": "Rolamento", "BUSHING": "Bucha", "SLEEVE": "Luva (sleeve)",
    "LINER": "Forro (liner)", "SHAFT": "Eixo", "AXLE": "Eixo", "STUD": "Prisioneiro (stud)", "GEAR": "Engrenagem",
    "PINION": "Pinhão", "SPROCKET": "Roda dentada", "CHAIN": "Corrente", "ROLLER": "Rolete", "CAM": "Came",
    "SPACER": "Espaçador", "SHIM": "Calço (shim)", "COLLAR": "Colar", "SEAL": "Retentor / vedação",
    "GASKET": "Junta", "FITTING": "Conexão", "ADAPTER": "Adaptador", "ADAPTOR": "Adaptador",
    "CLUTCH": "Embreagem", "LATCH": "Trinco", "PAWL": "Lingueta (pawl)", "LEVER": "Alavanca", "ARM": "Braço",
    "HANDLE": "Manopla", "ROD": "Haste", "LINK": "Elo / biela", "CRANK": "Manivela", "PLUNGER": "Êmbolo (plunger)",
    "PLATE": "Placa", "SLIPPER": "Sapata (slipper)", "SLIDER": "Corrediça (slider)", "BRACKET": "Suporte",
    "SUPPORT": "Suporte", "POST": "Coluna / poste", "HOLDER": "Porta-", "BASE": "Base", "FRAME": "Estrutura",
    "RAIL": "Trilho", "STRAP": "Cinta", "GUIDE": "Guia", "HOUSING": "Carcaça (housing)", "BOX": "Caixa",
    "CASING": "Carcaça", "CARTRIDGE": "Cartucho", "BLOCK": "Bloco", "HUB": "Cubo", "MANIFOLD": "Manifold",
    "RESERVOIR": "Reservatório", "PUMP": "Bomba", "FILTER": "Filtro", "COVER": "Tampa", "GUARD": "Protetor",
    "SHIELD": "Escudo / protetor", "CAP": "Tampa", "TUBE": "Tubo", "TUBING": "Tubo", "PIPE": "Tubo",
    "SWITCH": "Chave / sensor", "SENSOR": "Sensor", "SOLENOID": "Solenoide", "TOOL": "Ferramenta",
    "SPRING": "Mola", "BOBBIN": "Bobina", "CUP": "Capa de rolamento (cup)", "CONE": "Cone de rolamento",
    "RING": "Anel", "CLIP": "Presilha", "RETAINER": "Retentor / trava", "HOOK": "Gancho", "YOKE": "Garfo (yoke)",
    "ROTOR": "Rotor", "SHUTTLE": "Shuttle", "DISC": "Disco", "COMPENSATOR": "Compensador",
    "TAG": "Etiqueta", "PLUG": "Bujão", "NIPPLE": "Niple", "CONNECTOR": "Conector", "ECCENTRIC": "Excêntrico",
    "EYEBOLT": "Parafuso olhal", "STRAP/COLLAR": "Cinta / colar", "BAR": "Barra", "EYE": "Olhal", "STRIP": "Tira", "TRUNION": "Munhão (trunion)", "TRUNNION": "Munhão (trunion)",
}


def _pt_mods(resto):
    """Traduz o restante da descrição palavra a palavra (o que não souber fica em inglês)."""
    t = " " + resto.upper() + " "
    for k in sorted(MODS, key=len, reverse=True):
        t = re.sub(r"(?<![A-Z/])%s(?![A-Z])" % re.escape(k), "<%s>" % MODS[k], t)
    return t


def nome_pt(desc, tipo, med):
    d = re.sub(r"\s+", " ", desc.strip())
    u = d.upper()
    toks = [t for t in re.split(r"[,\s]+", u) if t]
    h = toks[0] if toks else ""
    tam = ""
    if "rosca" in med:
        tam = " " + med["rosca"]
        if "comp_rosca_in" in med:
            tam += " x %s" % fmt_comp(med["comp_rosca_in"])
    if h in ("SCREW",) or (h in ("SET", "HEADLESS", "SOCKET") and "SCREW" in u):
        k = ""
        if "SET" in toks or "HEADLESS" in toks:
            k = "de pressão (set)" + (" Allen" if "SOC" in u else "")
        else:
            for rx, pt in TERMOS:
                if re.search(rx, u):
                    k = pt.strip(); break
        return ("Parafuso %s%s" % (k, tam)).replace("  ", " ").strip()
    if h == "NUT" or h == "LOCKNUT":
        k = ""
        for rx, pt in TERMOS:
            if re.search(rx, u) and pt not in ("sextavado",):
                k = pt.strip(); break
        if h == "LOCKNUT":
            return "Porca de trava de rolamento %s" % (med.get("rolamento", "")) if "BEARING" in u else "Contraporca" + tam
        return ("Porca %s%s" % (k, tam)).replace("  ", " ").strip()
    if h == "WASHER":
        k = "lisa" if "FLAT" in u else "de pressão" if "LOCK" in u else "de compressão" if "COMPR" in u else ""
        if re.search(r"SPACER|BEARING", u[7:]):
            k = "espaçadora" if "SPACER" in u else "de trava de rolamento"
        dims = ""
        if "id_in" in med and "od_in" in med:
            dims = " %s x %s" % (fmt_comp(med["id_in"]), fmt_comp(med["od_in"]))
        elif "nominal_in" in med:
            dims = " p/ %s" % fmt_comp(med["nominal_in"])
        return ("Arruela %s%s" % (k, dims)).replace("  ", " ").strip()
    if h in ("BRG", "BEARING") and tipo == "Arruela":   # ex.: BEARING LOCK WASHER
        return "Arruela de trava de rolamento"
    if h in ("BRG", "BEARING") and tipo == "Porca":     # ex.: BEARING LOCKNUT
        return "Porca de trava de rolamento"
    if h in ("BRG", "BEARING") or (h in ("CONE", "CUP") and ("BEARING" in u or "TIMKEN" in u)):
        k = "de esferas" if "BALL" in u else "de agulhas" if "NEEDLE" in u else "de rolos" if "ROLLER" in u else \
            "(bucha)" if "BUSHING" in u else "(seguidor de came)" if "CAM FOLLOWER" in u else \
            "pista externa (cup)" if h == "CUP" or "CUP" in toks else "cone" if "CONE" in toks else \
            "pista (race)" if "RACE" in u else ""
        dims = ""
        if "id_in" in med:
            dims += " Øint %s" % fmt_comp(med["id_in"])
        if "od_in" in med:
            dims += " Øext %s" % fmt_comp(med["od_in"])
        if "rolamento" in med:
            dims += " " + med["rolamento"]
        return ("Rolamento %s%s" % (k, dims)).replace("  ", " ").strip()
    if h == "SPRING" or (h == "CLUTCH" and "SPRING" in toks[:3]):
        k = "de compressão" if "COMP" in u else "de tração" if ("TENS" in u or "EXT" in u) else \
            "de torção" if "TORSION" in u else "helicoidal"
        extra = ""
        if "fio_in" in med:
            extra += " fio %s" % fmt_comp(med["fio_in"])
        if "od_in" in med:
            extra += " Øext %s" % fmt_comp(med["od_in"])
        if "comp_in" in med:
            extra += " x %s" % fmt_comp(med["comp_in"])
        return ("Mola %s%s" % (k, extra)).replace("  ", " ").strip()
    if h == "SPROCKET" or (h == "IDLER" and "SPROCKET" in u):
        return "Roda dentada%s%s" % (" %d dentes" % med["dentes"] if "dentes" in med else "",
                                     " (passo %s)" % med["passo"] if "passo" in med else "")
    if h == "GEAR" and "dentes" in med:
        return "Engrenagem %d dentes" % med["dentes"]
    if h == "RING" and "RET" in u:
        k = "externo" if "EXT" in u else "interno" if "INT" in u else ""
        return ("Anel elástico %s%s" % (k, " p/ %s" % fmt_comp(med["nominal_in"]) if "nominal_in" in med else "")).replace("  ", " ").strip()
    if h in ("SEAL",) and "O-RING" in u:
        return "O-ring%s" % (" Øint %s" % fmt_comp(med["id_in"]) if "id_in" in med else "")
    if h == "SEAL" and "OIL" in u:
        dims = ""
        if "id_in" in med:
            dims += " %s x %s" % (fmt_comp(med["id_in"]), fmt_comp(med.get("od_in", 0)))
        return "Retentor (oil seal)%s" % dims
    if h == "PIN":
        k = "paralelo (dowel)" if "DOWEL" in u else "elástico (roll)" if "ROLL" in u else "cônico" if "TAPER" in u else \
            "de mola" if "SPRING" in u else ""
        dims = ""
        if "od_in" in med:
            dims = " Ø%s" % fmt_comp(med["od_in"])
            if "comp_in" in med:
                dims += " x %s" % fmt_comp(med["comp_in"])
        return ("Pino %s%s" % (k, dims)).replace("  ", " ").strip()
    if h == "FITTING" and "GREASE" in u:
        return "Graxeira%s" % tam
    # genérico: substantivo + modificadores traduzidos
    noun = NOMES.get(h, None)
    resto = re.sub(r"^\s*" + re.escape(toks[0]) + r"[,\s]*", "", d, flags=re.I) if toks else d
    if noun is None and h in EXTRA_CABECA:
        noun = NOMES.get(EXTRA_CABECA[h])
    if noun is None:
        base = tipo.split(" / ")[0]
        return ("%s (%s)" % (base, d.lower())) if tipo != "Outro" else d.capitalize()
    mod = _pt_mods(resto)
    mod = mod.replace("<", "").replace(">", "")
    mod = re.sub(r"\s+", " ", mod).strip(" ,")
    # palavras em inglês que sobraram: minúsculas
    mod = " ".join(w.lower() if w.upper() == w else w for w in mod.split())
    return ("%s %s" % (noun, mod)).strip()


def fmt_comp(v):
    s = "%.3f" % v
    s = s.rstrip("0")
    if s.endswith("."):
        s += "0"
    if len(s.split(".")[1]) < 2:
        s += "0"
    return s + '"'

# ------------------------------------------------------------------ montagem das ocorrências
def sem_acento(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_").lower()


def norm_codigo(c):
    return re.sub(r"\s+", "", c).upper()


def separa_qtd(qtd, um):
    qtd = qtd.strip(); um = um.strip()
    if not um and " " in qtd:
        qtd, um = qtd.rsplit(" ", 1)
    return qtd.strip(), um.strip()


def montar_ocorrencias():
    ocs, manuais, extra = [], {}, {}
    for mid, arq, pasta, rot, maq in MANUAIS:
        n, rect, grupos, bal = extrair_manual(mid, arq)
        manuais[mid] = dict(arquivo=arq, pasta_imagens="manuais_imagens/" + pasta, rotulo=rot,
                            maquina=maq, paginas=n, vetorial=True)
        extra[mid] = dict(rect=rect)
        por_grupo = defaultdict(lambda: defaultdict(list))
        for pgn in sorted(bal):
            for b in sorted(bal[pgn], key=lambda b: b["cy"]):
                if b["grupo"] is not None:
                    por_grupo[id(b["grupo"])][b["num"]].append(b)
        usados = Counter()
        for g in grupos:
            cod_conj = g["titulo"].split(" ")[0]
            for r in g["rows"]:
                qtd, um = separa_qtd(r["qtd"], r["um"])
                bl = por_grupo[id(g)].get(r["item"], [])
                tipo = tipo_de(r["desc"])
                med = parse_medidas(r["desc"], tipo)
                base = "%s-%d-%s-%s" % (mid, r["pagina_lista"], cod_conj, r["item"])
                usados[base] += 1
                oid = base if usados[base] == 1 else "%s-%d" % (base, usados[base])
                oc = dict(id=oid, codigo=r["codigo"], codigo_norm=norm_codigo(r["codigo"]), descricao=r["desc"],
                          tipo=tipo, nome_pt=nome_pt(r["desc"], tipo, med), maquina=maq, conjunto=g["titulo"],
                          item=r["item"], qtd=qtd, um=um, manual=mid, pagina_lista=r["pagina_lista"],
                          pagina_desenho=bl[0]["pagina"] if bl else None,
                          medidas=med, medidas_txt=medidas_txt(med), _bal=bl)
                oc["baloes"] = []
                oc["pontas"] = []
                ocs.append(oc)
    # 261 (escaneado), se existir a lista estruturada
    f261 = os.path.join(DADOS, "261_estruturado.csv")
    if os.path.exists(f261):
        _, _, pasta, rot, maq = M261
        npag = len([x for x in os.listdir("manuais_imagens/" + pasta) if x.endswith(".png")])
        manuais["261"] = dict(arquivo="261-EN (escaneado, sem texto)", pasta_imagens="manuais_imagens/" + pasta,
                              rotulo=rot, maquina=maq, paginas=npag, vetorial=False)
        usados = Counter()
        with open(f261, encoding="utf-8-sig", newline="") as fh:
            for r in csv.DictReader(fh, delimiter=";"):
                if not r.get("codigo"):
                    continue
                desc = r.get("descricao", "")
                tipo = tipo_de(desc); med = parse_medidas(desc, tipo)
                try:
                    pl = int(r["pagina_lista"])
                except Exception:
                    pl = 0
                pds = [int(x) for x in re.findall(r"\d+", r.get("paginas_desenho", ""))]
                base = "261-%d-%s-%s" % (pl, r.get("plate", ""), r.get("item", ""))
                usados[base] += 1
                oid = base if usados[base] == 1 else "%s-%d" % (base, usados[base])
                oc = dict(id=oid, codigo=r["codigo"], codigo_norm=norm_codigo(r["codigo"]), descricao=desc,
                          tipo=tipo, nome_pt=nome_pt(desc, tipo, med), maquina=maq,
                          conjunto=(r.get("plate", "") + " – " + r.get("plate_titulo", "")).strip(" –"),
                          item=r.get("item", ""), qtd=r.get("qtd", ""), um="", manual="261",
                          pagina_lista=pl, pagina_desenho=pds[0] if pds else None, medidas=med,
                          medidas_txt=medidas_txt(med), _bal=[], baloes=[], pontas=[])
                ocs.append(oc)
    else:
        print("AVISO: dados/261_estruturado.csv não existe; seguindo sem o manual 261.")
    return ocs, manuais, extra

# ------------------------------------------------------------------ imagens
from PIL import Image, ImageDraw, ImageFont

def fonte(tam, negrito=False):
    for nome in (("arialbd.ttf" if negrito else "arial.ttf"), "calibri.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype("C:/Windows/Fonts/" + nome if os.path.exists("C:/Windows/Fonts/" + nome) else nome, tam)
        except Exception:
            continue
    return ImageFont.load_default()

VERM = (230, 20, 20)
W_REC, H_DES, H_FOOT = 520, 376, 44


def desenha_baloes(dr, baloes, f, ox, oy, grosso=3, tip=True):
    """Círculos, linhas de chamada e pontas em vermelho. f = px por pt; (ox,oy) = origem em pt."""
    for b in baloes:
        cx, cy = (b["cx"] - ox) * f, (b["cy"] - oy) * f
        R = b["R"] * f + grosso
        dr.ellipse([cx - R, cy - R, cx + R, cy + R], outline=VERM, width=grosso + 1)
        cad = b["cadeia"]
        if len(cad) > 1:
            pts = [((x - ox) * f, (y - oy) * f) for x, y in cad]
            dr.line(pts, fill=VERM, width=max(2, grosso - 1), joint="curve")
            if tip:
                x, y = pts[-1]
                dr.ellipse([x - 9, y - 9, x + 9, y + 9], outline=VERM, width=3)
                dr.ellipse([x - 3, y - 3, x + 3, y + 3], fill=VERM)


def ajusta_texto(dr, txt, fnt_fun, tam, largura, minimo, negrito=False):
    while tam >= minimo:
        fn = fonte(tam, negrito)
        if dr.textlength(txt, font=fn) <= largura:
            return fn, txt
        tam -= 1
    fn = fonte(minimo, negrito)
    while len(txt) > 4 and dr.textlength(txt + "…", font=fn) > largura:
        txt = txt[:-1]
    return fn, txt + "…"


def recorte(img, zoom, bls, w_pt, h_pt, linhas_rodape, destino):
    """Recorta a região que contém o 1º balão e a ponta; img = página renderizada em 'zoom'."""
    b = bls[0]
    xs = [b["cx"] - b["R"], b["cx"] + b["R"]] + [p[0] for p in b["cadeia"]]
    ys = [b["cy"] - b["R"], b["cy"] + b["R"]] + [p[1] for p in b["cadeia"]]
    x0, x1, y0, y1 = min(xs) - 26, max(xs) + 26, min(ys) - 26, max(ys) + 26
    rw, rh = max(x1 - x0, 124), max(y1 - y0, 124 * H_DES / W_REC)
    asp = W_REC / H_DES
    if rw / rh < asp:
        rw = rh * asp
    else:
        rh = rw / asp
    rw, rh = min(rw, w_pt), min(rh, h_pt)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    x0 = min(max(cx - rw / 2, 0), w_pt - rw); y0 = min(max(cy - rh / 2, 0), h_pt - rh)
    box = tuple(int(round(v * zoom)) for v in (x0, y0, x0 + rw, y0 + rh))
    cut = img.crop(box).resize((W_REC, H_DES), Image.LANCZOS)
    f = W_REC / rw
    dr = ImageDraw.Draw(cut)
    ext = [bb for bb in bls if x0 - 10 <= bb["cx"] <= x0 + rw + 10 and y0 - 10 <= bb["cy"] <= y0 + rh + 10]
    desenha_baloes(dr, ext, f, x0, y0, grosso=3)
    out = Image.new("RGB", (W_REC, H_DES + H_FOOT), "white")
    out.paste(cut, (0, 0))
    d2 = ImageDraw.Draw(out)
    fn, t1 = ajusta_texto(d2, linhas_rodape[0], None, 16, W_REC - 12, 11, True)
    d2.text((6, H_DES + 4), t1, fill=(0, 0, 0), font=fn)
    fn, t2 = ajusta_texto(d2, linhas_rodape[1], None, 14, W_REC - 12, 10)
    d2.text((6, H_DES + 24), t2, fill=(70, 70, 70), font=fn)
    d2.rectangle([0, 0, W_REC - 1, H_DES + H_FOOT - 1], outline=(180, 180, 180))
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    out.save(destino, "JPEG", quality=82)


def pagina_marcada(img, zoom, bls, destino):
    f = 1100 / (img.height / zoom)
    im = img.resize((int(img.width * f / zoom), 1100), Image.LANCZOS)
    dr = ImageDraw.Draw(im)
    desenha_baloes(dr, bls, f, 0, 0, grosso=3)
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    im.save(destino, "JPEG", quality=82)


def gerar_imagens(ocs, manuais, extra):
    cfg = {m[0]: m for m in MANUAIS}
    # pasta de imagens do COMUM26
    pasta = "manuais_imagens/" + cfg["COMUM26"][2]
    os.makedirs(pasta, exist_ok=True)
    doc = pymupdf.open(cfg["COMUM26"][1])
    for i in range(len(doc)):
        fn = os.path.join(pasta, "p%03d.png" % (i + 1))
        if not os.path.exists(fn):
            doc[i].get_pixmap(matrix=pymupdf.Matrix(1.25, 1.25)).save(fn)
    doc.close()
    nomes = set()
    def unico(rel):
        base, ext = os.path.splitext(rel); k = 1; cand = rel
        while cand in nomes:
            k += 1; cand = "%s_%d%s" % (base, k, ext)
        nomes.add(cand); return cand
    grupos = defaultdict(list)
    for oc in ocs:
        if oc["_bal"]:
            grupos[(oc["manual"], oc["pagina_desenho"])].append(oc)
    ordem = sorted(grupos, key=lambda k: (PRIOR.index(k[0]), k[1]))
    Z = 3
    docs = {}
    for (mid, pg) in ordem:
        if mid not in docs:
            docs[mid] = pymupdf.open(cfg[mid][1])
        page = docs[mid][pg - 1]
        W, H = page.rect.width, page.rect.height
        pix = page.get_pixmap(matrix=pymupdf.Matrix(Z, Z), alpha=False)
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        for oc in grupos[(mid, pg)]:
            todos = oc["_bal"]
            na_pag = [b for b in todos if b["pagina"] == pg]
            oc["baloes"] = [[round((b["cx"] - b["R"]) / W, 5), round((b["cy"] - b["R"]) / H, 5),
                             round((b["cx"] + b["R"]) / W, 5), round((b["cy"] + b["R"]) / H, 5)] for b in todos]
            oc["pontas"] = [[round(b["cadeia"][-1][0] / W, 5), round(b["cadeia"][-1][1] / H, 5)]
                            for b in todos if len(b["cadeia"]) > 1]
            rod1 = "%s · %s" % (oc["codigo"], oc["descricao"])
            rod2 = "%s pág. %d  (item %s · %s)" % (cfg[mid][3], pg, oc["item"], oc["conjunto"][:40])
            rel = unico("recortes/%s/%s__p%d_i%s.jpg" % (mid, re.sub(r"[^\w.-]", "_", oc["codigo"]), pg, oc["item"]))
            recorte(img, Z, na_pag, W, H, (rod1, rod2), rel)
            oc["recorte"] = rel
            if "--paginas-marcadas" in sys.argv:   # opcional: ~100 MB; a tela do Identificador marca por cima da página
                relm = unico("paginas_marcadas/%s/p%03d__%s_i%s.jpg" % (mid, pg, re.sub(r"[^\w.-]", "_", oc["codigo"]), oc["item"]))
                pagina_marcada(img, Z, na_pag, relm)
                oc["pagina_marcada"] = relm
            else:
                oc["pagina_marcada"] = "%s/p%03d.png" % (manuais[mid]["pasta_imagens"], pg)
    # 261: página de desenho reduzida (sem círculo)
    for oc in ocs:
        if oc["manual"] == "261" and oc.get("pagina_desenho"):
            fn = "%s/p%03d.png" % (manuais["261"]["pasta_imagens"], oc["pagina_desenho"])
            if os.path.exists(fn):
                # um arquivo por página de desenho (todas as peças do plate apontam para ele)
                rel = "recortes/261/p%03d.jpg" % oc["pagina_desenho"]
                if rel not in nomes:
                    nomes.add(rel)
                    im = Image.open(fn).convert("RGB")
                    im.thumbnail((W_REC, H_DES))
                    out = Image.new("RGB", (W_REC, H_DES + H_FOOT), "white")
                    out.paste(im, ((W_REC - im.width) // 2, 0))
                    d2 = ImageDraw.Draw(out)
                    d2.text((6, H_DES + 4), "261-EN pág. %d · Plate %s" % (oc["pagina_desenho"], oc.get("conjunto", "")[:50]), fill=(0, 0, 0), font=fonte(15, True))
                    d2.text((6, H_DES + 24), "escaneado: balão não marcado, procure o nº do item", fill=(70, 70, 70), font=fonte(13))
                    os.makedirs(os.path.dirname(rel), exist_ok=True)
                    out.save(rel, "JPEG", quality=82)
                oc["recorte"] = rel
    for d in docs.values():
        d.close()

# ------------------------------------------------------------------ atlas
CW, CH, LAB = 384, 312, 62


def curto(txt):
    return re.sub(r"\s*\([\d.]+ mm\)", "", txt)


def bitola(med):
    r = med.get("rosca")
    if r:
        m = re.match(r"^(.+)-\d+$", r)
        return (m.group(1) if m else r.split("x")[0]).replace("#", "n").replace("/", "-")
    for k in ("id_in", "nominal_in", "od_in"):
        if k in med:
            return "d%.3f" % med[k]
    return "outros"


def gerar_atlas(ocs, log):
    pasta = "atlas"
    os.makedirs(pasta, exist_ok=True)
    for f in os.listdir(pasta):
        if f.endswith(".jpg") or f.endswith(".csv"):
            os.remove(os.path.join(pasta, f))
    por_tipo = defaultdict(dict)
    maquinas = defaultdict(list)
    for oc in ocs:
        k = oc["codigo_norm"]
        if oc["maquina"] not in maquinas[k]:
            maquinas[k].append(oc["maquina"])
        cur = por_tipo[oc["tipo"]].get(k)
        chave = (0 if oc.get("recorte") else 1, PRIOR.index(oc["manual"]), 0 if oc["pontas"] else 1)
        if cur is None or chave < cur[0]:
            por_tipo[oc["tipo"]][k] = (chave, oc)
    indice, folhas_tipo = [], {}
    fnt1, fnt2, fnt3 = fonte(14, True), fonte(12), fonte(11)
    for tipo in TIPOS:
        itens = [v[1] for v in por_tipo.get(tipo, {}).values()]
        if not itens:
            continue
        itens.sort(key=lambda o: (0 if o.get("recorte") else 1, o["descricao"].casefold(), o["codigo_norm"]))  # sem desenho vão para o fim
        base = sem_acento(tipo)
        grupos = [(base, itens)]
        if tipo in ("Parafuso", "Porca", "Arruela", "Anel de retenção") and len(itens) > 120:
            log.append("AVISO atlas: %s tem %d códigos (> 6 folhas); folhas agrupadas por bitola." % (tipo, len(itens)))
            d = defaultdict(list)
            for o in itens:
                d[bitola(o["medidas"])].append(o)
            grupos = [("%s_%s" % (base, k), v) for k, v in sorted(d.items())]
        nf = 0
        for gnome, lista in grupos:
            for ini in range(0, len(lista), 20):
                nf += 1
                lote = lista[ini:ini + 20]
                folha = Image.new("RGB", (4 * CW, 5 * CH), "white")
                dr = ImageDraw.Draw(folha)
                nome_f = "%s__%02d" % (gnome, ini // 20 + 1)
                for i, o in enumerate(lote):
                    col, lin = i % 4, i // 4
                    x, y = col * CW, lin * CH
                    dr.rectangle([x, y, x + CW - 1, y + CH - 1], outline=(190, 190, 190))
                    if o.get("recorte") and os.path.exists(o["recorte"]):
                        im = Image.open(o["recorte"]).convert("RGB").crop((0, 0, W_REC, H_DES))
                        im.thumbnail((CW - 6, CH - LAB - 4), Image.LANCZOS)
                        folha.paste(im, (x + (CW - im.width) // 2, y + 2))
                    else:
                        dr.rectangle([x + 3, y + 2, x + CW - 4, y + CH - LAB - 3], fill=(240, 240, 240))
                        dr.text((x + 90, y + 110), "sem desenho localizado", fill=(120, 120, 120), font=fnt2)
                    ty = y + CH - LAB + 1
                    cel = i + 1
                    _, t = ajusta_texto(dr, "#%02d %s" % (cel, o["codigo"]), None, 14, CW - 8, 11, True)
                    dr.text((x + 4, ty), t, fill=(0, 0, 0), font=fnt1)
                    _, t = ajusta_texto(dr, o["descricao"], None, 12, CW - 8, 9)
                    dr.text((x + 4, ty + 18), t, fill=(30, 30, 30), font=fnt2)
                    _, t = ajusta_texto(dr, curto(o["medidas_txt"]) or "-", None, 11, CW - 8, 8)
                    dr.text((x + 4, ty + 35), t, fill=(0, 70, 140), font=fnt3)
                    indice.append([tipo, nome_f, cel, o["codigo"], o["descricao"], o["medidas_txt"],
                                   " | ".join(maquinas[o["codigo_norm"]]), o.get("recorte", "")])
                folha.save("%s/%s.jpg" % (pasta, nome_f), "JPEG", quality=85)
        folhas_tipo[tipo] = nf
    with open(pasta + "/indice_atlas.csv", "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["tipo", "folha", "celula", "codigo", "descricao", "medidas_txt", "maquinas", "recorte"])
        w.writerows(indice)
    return folhas_tipo

# ------------------------------------------------------------------ planilha
def gerar_xlsx(ocs, manuais):
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment
    from openpyxl.utils import get_column_letter
    wb = Workbook()
    ws = wb.active; ws.title = "Catálogo"
    cab = ["Código", "Nome PT", "Tipo", "Descrição EN", "Medidas", "Øint pol", "Øext pol", "Comp pol", "Rosca",
           "Dentes", "Rolamento", "Máquina", "Conjunto", "Item", "Qtd", "Manual (rótulo)", "Pág. lista",
           "Pág. desenho", "Recorte", "Página inteira", "Øint mm", "Øext mm", "Comp mm"]
    ws.append(cab)
    for c in ws[1]:
        c.fill = PatternFill("solid", fgColor="1F4E78")
        c.font = Font(bold=True, color="FFFFFF")
        c.alignment = Alignment(vertical="center", wrap_text=True)
    link = Font(color="0563C1", underline="single")
    for oc in ocs:
        m = oc["medidas"]
        ws.append([oc["codigo"], oc["nome_pt"], oc["tipo"], oc["descricao"], oc["medidas_txt"], m.get("id_in"),
                   m.get("od_in"), m.get("comp_in"), m.get("rosca"), m.get("dentes"), m.get("rolamento"),
                   oc["maquina"], oc["conjunto"], oc["item"], oc["qtd"], manuais[oc["manual"]]["rotulo"],
                   oc["pagina_lista"], oc["pagina_desenho"], None, None,
                   *[round(m[k] * 25.4, 1) if isinstance(m.get(k), (int, float)) else None for k in ("id_in", "od_in", "comp_in")]])
        r = ws.max_row
        for col, k in ((19, "recorte"), (20, "pagina_marcada")):
            if oc.get(k):
                c = ws.cell(row=r, column=col, value="ver")
                c.hyperlink = oc[k]; c.font = link
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    larg = [14, 38, 22, 40, 52, 9, 9, 9, 12, 8, 14, 16, 36, 6, 6, 18, 9, 11, 9, 14, 9, 9, 9]
    for i, w in enumerate(larg, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws2 = wb.create_sheet("Por tipo")
    ws2.append(["Tipo", "Ocorrências", "Códigos únicos"])
    for c in ws2[1]:
        c.fill = PatternFill("solid", fgColor="1F4E78"); c.font = Font(bold=True, color="FFFFFF")
    cont = defaultdict(list)
    for oc in ocs:
        cont[oc["tipo"]].append(oc["codigo_norm"])
    for t in TIPOS:
        if t in cont:
            ws2.append([t, len(cont[t]), len(set(cont[t]))])
    ws2.column_dimensions["A"].width = 32; ws2.column_dimensions["B"].width = 14; ws2.column_dimensions["C"].width = 16
    ws3 = wb.create_sheet("Leia-me")
    linhas = [
        "CATÁLOGO DE PEÇAS - trançadeiras Magnatech 225-II e RB2 (gerado por gerar_catalogo.py)",
        "",
        "Aba Catálogo: uma linha por ocorrência da peça em um conjunto de um manual.",
        "Código / Descrição EN: como está no manual. Nome PT: tradução curta automática. Tipo: classe em português.",
        "Medidas: texto com o que foi lido da descrição. Øint, Øext, Comp: em polegadas (1 pol = 25,4 mm).",
        "Rosca: bitola-fios por polegada (ex. 3/8-16, #10-32) ou métrica (M8x1.25). Dentes: nº de dentes (engrenagem/roda dentada).",
        "Recorte: imagem do desenho com o balão da peça circulado em vermelho e a ponta da linha de chamada.",
        "Página inteira: a página do manual onde está o desenho (com --paginas-marcadas, sai com os balões marcados).",
        "Øint mm, Øext mm, Comp mm: as mesmas medidas em milímetros, para filtrar com o valor do paquímetro (use filtro de número 'entre').",
        "Os atlas por tipo estão na pasta atlas (folhas JPG + indice_atlas.csv).",
        "",
        "Como achar uma peça pela medida com o paquímetro:",
        "1) Meça Øint, Øext e comprimento e converta para polegadas (mm / 25,4).",
        "2) Na aba Catálogo, ative o filtro da coluna Tipo e depois filtre Øint, Øext, Comp ou Dentes (Filtros de número > Entre...).",
        "3) Use uma tolerância de ±0,01 pol (±0,25 mm) e confira o desenho no Recorte.",
        "Nem toda peça tem medida na descrição: peças fabricadas (códigos B1-, B6-) costumam ter só o nome.",
    ]
    for l in linhas:
        ws3.append([l])
    ws3.column_dimensions["A"].width = 130
    ws3["A1"].font = Font(bold=True, size=13)
    wb.save("CATALOGO_PECAS.xlsx")

# ------------------------------------------------------------------ principal
def main():
    t0 = time.time()
    os.makedirs(DADOS, exist_ok=True)
    ocs, manuais, extra = montar_ocorrencias()
    if "--extrair" in sys.argv:
        pass
    else:
        gerar_imagens(ocs, manuais, extra)
    log = []
    folhas = {}
    if "--extrair" not in sys.argv:
        folhas = gerar_atlas(ocs, log)
    saida = []
    for oc in ocs:
        o = {k: v for k, v in oc.items() if not k.startswith("_")}
        o.setdefault("recorte", ""); o.setdefault("pagina_marcada", "")
        o["pagina_desenho"] = o["pagina_desenho"] if o["pagina_desenho"] else None
        saida.append(o)
    # --extrair não gera recortes: grava à parte para não apagar os recortes do catalogo.json
    alvo = "/catalogo_extracao.json" if "--extrair" in sys.argv else "/catalogo.json"
    with open(DADOS + alvo, "w", encoding="utf-8") as fh:
        json.dump(dict(gerado_em=time.strftime("%Y-%m-%dT%H:%M:%S"), manuais=manuais, pecas=saida),
                  fh, ensure_ascii=False, indent=1)
    if "--extrair" not in sys.argv:
        gerar_xlsx(ocs, manuais)
    # estatísticas
    print("manual: ocorrências | códigos únicos | % balão | % ponta")
    sem = []
    for mid in manuais:
        l = [o for o in ocs if o["manual"] == mid]
        u = len({o["codigo_norm"] for o in l})
        b = sum(1 for o in l if o["baloes"] or o["_bal"]); p = sum(1 for o in l if o["pontas"] or any(len(x["cadeia"]) > 1 for x in o["_bal"]))
        pc = lambda v: 100 * v / len(l) if l else 0
        if mid != "261":
            print("%-8s %5d | %4d | %5.1f%% | %5.1f%%" % (mid, len(l), u, pc(b), pc(p)))
        else:
            print("261      %5d | %4d | (sem balão: página inteira)" % (len(l), u))
        sem += [o for o in l if not o["_bal"] and mid != "261"]
    vet = [o for o in ocs if o["manual"] != "261"]
    if vet:
        print("TOTAL vetoriais: %d ocorrências, balão em %.1f%%" % (len(vet), 100 * sum(1 for o in vet if o["_bal"]) / len(vet)))
    print("folhas de atlas por tipo:", folhas)
    with open(DADOS + "/log_catalogo.txt", "w", encoding="utf-8") as fh:
        fh.write("Ocorrências sem balão (manual, página lista, conjunto, item, código)\n")
        for o in sem:
            fh.write("%s | pág %s | %s | item %s | %s\n" % (o["manual"], o["pagina_lista"], o["conjunto"], o["item"], o["codigo"]))
        fh.write("\n" + "\n".join(log) + "\n")
    print("sem balão:", len(sem), "(ver dados/log_catalogo.txt)")
    print("tempo total: %.1f s" % (time.time() - t0))


if __name__ == "__main__":
    main()
