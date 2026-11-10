"""Missao L: folha de mockup antes/depois (esquema, nao e print da tela real).

ANTES do BI = posicoes lidas do projeto GMS/PowerBI/GMS_Painel.Report (pagina Visao Geral).
DEPOIS = proposta do L_diagnostico.md. Nada aqui altera o relatorio nem o layout salvo.
Rodar:  python GMS/Auditoria_Fable/gerar_mockup_L.py   (precisa de Pillow)
"""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

AQUI = Path(__file__).resolve().parent
REL = AQUI.parent / "PowerBI" / "GMS_Painel.Report" / "definition" / "pages" / "pg_visao_geral"
SAIDA = AQUI / "L_mockup_antes_depois.png"

VERM, AZUL, OK, ALERTA, ERRO = "#E30613", "#2C6FBF", "#16A34A", "#E67E22", "#C0392B"
TXT, SUAVE, ROT, BORDA, FUNDO = "#0F172A", "#64748B", "#94A3B8", "#E2E8F0", "#F3F4F6"


def fonte(tam, negrito=False):
    for nome in (("segoeuib.ttf" if negrito else "segoeui.ttf"), ("arialbd.ttf" if negrito else "arial.ttf")):
        try:
            return ImageFont.truetype("C:/Windows/Fonts/" + nome, tam)
        except OSError:
            pass
    return ImageFont.load_default()


def caixa(d, x, y, w, h, fill="#FFFFFF", borda=BORDA, r=8, lw=1):
    d.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=fill, outline=borda, width=lw)


def barras(d, x, y, w, h, cor, n=7, horizontal=True, destaque=None):
    vals = [1.0, 0.82, 0.66, 0.5, 0.38, 0.27, 0.18, 0.12][:n]
    if horizontal:
        passo = h / n
        for i, v in enumerate(vals):
            c = destaque if (destaque and i == 0) else cor
            d.rectangle([x, y + i * passo + 3, x + w * v, y + (i + 1) * passo - 3], fill=c)
    else:
        passo = w / n
        for i, v in enumerate(vals):
            d.rectangle([x + i * passo + 4, y + h * (1 - v), x + (i + 1) * passo - 4, y + h], fill=cor)


def linha(d, x, y, w, h, cor, meta=None):
    pts = [0.55, 0.62, 0.4, 0.7, 0.66, 0.5, 0.78, 0.6, 0.72, 0.45, 0.8, 0.68]
    xy = [(x + w * i / (len(pts) - 1), y + h * (1 - p)) for i, p in enumerate(pts)]
    if meta:
        for i in range(0, int(w), 14):
            d.line([x + i, y + h * 0.35, x + i + 7, y + h * 0.35], fill=meta, width=2)
    d.line(xy, fill=cor, width=3)


def bi_antes(img, ox, oy, s):
    d = ImageDraw.Draw(img)
    d.rectangle([ox, oy, ox + 1280 * s, oy + 720 * s], fill=FUNDO, outline=BORDA)
    vis = []
    for vf in sorted((REL / "visuals").glob("*/visual.json")):
        v = json.loads(vf.read_text(encoding="utf-8"))
        p, vv = v["position"], v.get("visual", {})
        tit = ""
        for t in vv.get("visualContainerObjects", {}).get("title", []):
            tit = t.get("properties", {}).get("text", {}).get("expr", {}).get("Literal", {}).get("Value", "").strip("'")
        vis.append((p.get("z", 0), vf.parent.name, vv.get("visualType"), p["x"], p["y"], p["width"], p["height"], tit))
    for z, nome, tipo, x, y, w, h, tit in sorted(vis):
        X, Y, W, H = ox + x * s, oy + y * s, w * s, h * s
        if tipo == "shape":
            d.rectangle([X, Y, X + W, Y + H], fill="#FFFFFF", outline=BORDA)
        elif tipo == "textbox":
            d.text((X + 4, Y + 8 * s), "GMS · Visão Geral da Produção", font=fonte(int(18 * s), True), fill=TXT)
        elif tipo == "image":
            d.text((X + 40 * s, Y + 14 * s), "Danfoss", font=fonte(int(16 * s), True), fill=VERM)
        elif tipo == "pageNavigator":
            for i in range(10):
                caixa(d, X + i * W / 10, Y + 6, W / 10 - 4, H - 12, fill="#FFFFFF", r=4)
            d.text((X + 6, Y + H / 2 - 6), "10 abas · texto 10 pt", font=fonte(int(10 * s) + 1), fill=SUAVE)
        elif tipo == "slicer":
            caixa(d, X, Y, W, H)
            d.text((X + 6, Y + 4), tit, font=fonte(int(11 * s) + 1), fill=SUAVE)
        elif tipo == "card":
            if nome == "atualizado":
                d.text((X, Y + 6), "Dado atualizado até dd/mm hh:mm", font=fonte(int(11 * s) + 1), fill=SUAVE)
            elif nome.endswith("_d"):
                caixa(d, X, Y, W, H, r=0)
                d.text((X + 8, Y + 4), "Δ vs mês ant.", font=fonte(int(11 * s) + 1), fill=SUAVE)
            else:
                caixa(d, X, Y, W, H)
                d.text((X + 8, Y + 4), tit, font=fonte(int(11 * s) + 1, True), fill="#475569")
                d.text((X + 8, Y + 24 * s), "12.345", font=fonte(int(24 * s) + 2, True), fill="#1F2937")
        else:
            caixa(d, X, Y, W, H)
            d.text((X + 8, Y + 5), tit, font=fonte(int(12 * s) + 1, True), fill="#1F2937")
            gx, gy, gw, gh = X + 14, Y + 34 * s, W - 28, H - 48 * s
            if "line" in tipo.lower():
                linha(d, gx, gy, gw, gh, VERM)
            else:
                barras(d, gx, gy, gw * 0.9, gh, VERM, n=7, horizontal="Bar" in tipo)
            d.text((gx, Y + H - 14 * s), "eixos e rótulos 9 pt", font=fonte(int(9 * s) + 1), fill=ROT)


def kpi(d, x, y, w, h, rotulo, valor, delta, cor):
    caixa(d, x, y, w, h)
    d.rectangle([x, y + 8, x + 6, y + h - 8], fill=cor)
    d.text((x + 16, y + 8), rotulo, font=fonte(14, True), fill=SUAVE)
    d.text((x + 16, y + 28), valor, font=fonte(34, True), fill=TXT)
    d.text((x + 16, y + h - 26), delta, font=fonte(14, True), fill=cor)


def bi_depois(img, ox, oy, s):
    d = ImageDraw.Draw(img)
    W, H = 1280 * s, 720 * s
    d.rectangle([ox, oy, ox + W, oy + H], fill="#F5F7FA", outline=BORDA)
    d.rectangle([ox, oy, ox + W, oy + 50], fill="#FFFFFF", outline=BORDA)
    d.text((ox + 14, oy + 12), "Como está a célula hoje?", font=fonte(20, True), fill=TXT)
    for i, t in enumerate(["Período: hoje", "Turno: atual", "Etapa: todas"]):
        caixa(d, ox + W - 560 + i * 150, oy + 9, 140, 32, r=6)
        d.text((ox + W - 552 + i * 150, oy + 16), t, font=fonte(13), fill=TXT)
    d.text((ox + W - 96, oy + 14), "Danfoss", font=fonte(15, True), fill=VERM)
    m, g = 14, 12
    kw = (W - 2 * m - 4 * g) / 5
    dados = [("Metros × meta do dia", "8.420 m", "▼ 6% abaixo da meta", ALERTA), ("Aderência Hora-Hora", "91%", "▲ dentro da meta", OK),
             ("Tempo parado", "1h52", "▲ 38 min acima do teto", ERRO), ("Refugo PPM", "4.310", "▼ melhor que a base", OK),
             ("OPs ativas / zumbi", "23 / 2", "2 paradas há +24 h", ALERTA)]
    for i, (a, b, c, cor) in enumerate(dados):
        kpi(d, ox + m + i * (kw + g), oy + 62, kw, 104, a, b, c, cor)
    y2 = oy + 62 + 104 + g
    hp = H - (y2 - oy) - 40
    wp = (W - 2 * m - g) * 0.64
    caixa(d, ox + m, y2, wp, hp)
    d.text((ox + m + 12, y2 + 8), "Qual etapa está mais longe da meta agora?", font=fonte(16, True), fill=TXT)
    d.text((ox + m + 12, y2 + 30), "Real × planejado por etapa · a pior em destaque", font=fonte(12), fill=SUAVE)
    barras(d, ox + m + 130, y2 + 58, wp - 160, hp - 76, AZUL, n=8, destaque=VERM)
    for i, e in enumerate(["Trançagem", "Cobertura", "Vulcanização", "Tubo", "Bandagem", "Debandagem", "Mandril", "Extração"]):
        d.text((ox + m + 12, y2 + 62 + i * (hp - 76) / 8), e, font=fonte(13), fill=TXT)
    xa = ox + m + wp + g
    wa = W - 2 * m - g - wp
    ha = (hp - g) / 2
    caixa(d, xa, y2, wa, ha)
    d.text((xa + 12, y2 + 8), "O que mais parou a célula hoje?", font=fonte(16, True), fill=TXT)
    barras(d, xa + 12, y2 + 40, wa - 40, ha - 52, AZUL, n=5, destaque=ERRO)
    caixa(d, xa, y2 + ha + g, wa, ha)
    d.text((xa + 12, y2 + ha + g + 8), "A produção do dia acompanha a meta?", font=fonte(16, True), fill=TXT)
    linha(d, xa + 14, y2 + ha + g + 44, wa - 28, ha - 62, AZUL, meta=SUAVE)
    d.text((ox + m, oy + H - 26), "Atualizado em dd/mm hh:mm · Dono: William · eixos e rótulos 12 pt · azul = série, vermelho = só exceção",
           font=fonte(12), fill=SUAVE)


def celular(img, ox, oy, depois):
    d = ImageDraw.Draw(img)
    w, h = 300, 620
    caixa(d, ox, oy, w, h, fill="#111827", borda="#111827", r=28)
    caixa(d, ox + 10, oy + 34, w - 20, h - 68, fill="#F5F7FA", r=4)
    x, y, ww = ox + 18, oy + 44, w - 36
    if not depois:
        mini = Image.new("RGB", (1280, 720), FUNDO)
        bi_antes(mini, 0, 0, 1.0)
        mini = mini.resize((ww, int(ww * 720 / 1280)), Image.LANCZOS)
        img.paste(mini, (x, y + 150))
        d.text((x, y + 10), "Sem layout móvel:", font=fonte(15, True), fill=TXT)
        d.text((x, y + 34), "a página de 1280 px encolhe para", font=fonte(13), fill=SUAVE)
        d.text((x, y + 52), "~360 px. Texto de 9 pt vira ~2,5 pt.", font=fonte(13), fill=SUAVE)
        d.text((x, y + 330), "Só dá para ler com pinça e zoom.", font=fonte(13), fill=ERRO)
    else:
        d.text((x, y + 4), "Como está a célula hoje?", font=fonte(15, True), fill=TXT)
        dados = [("Metros × meta", "8.420 m", ALERTA), ("Aderência HH", "91%", OK), ("Tempo parado", "1h52", ERRO), ("Refugo PPM", "4.310", OK)]
        for i, (a, b, cor) in enumerate(dados):
            cx, cy = x + (i % 2) * (ww / 2 + 3), y + 32 + (i // 2) * 86
            caixa(d, cx, cy, ww / 2 - 4, 80)
            d.rectangle([cx, cy + 8, cx + 5, cy + 72], fill=cor)
            d.text((cx + 12, cy + 8), a, font=fonte(12, True), fill=SUAVE)
            d.text((cx + 12, cy + 30), b, font=fonte(26, True), fill=TXT)
        gy = y + 32 + 2 * 86 + 6
        caixa(d, x, gy, ww, 200)
        d.text((x + 10, gy + 8), "Etapa mais longe da meta", font=fonte(13, True), fill=TXT)
        barras(d, x + 10, gy + 34, ww - 30, 156, AZUL, n=6, destaque=VERM)
        caixa(d, x, gy + 208, ww, 110)
        d.text((x + 10, gy + 216), "O que mais parou hoje", font=fonte(13, True), fill=TXT)
        barras(d, x + 10, gy + 240, ww - 30, 70, AZUL, n=3, destaque=ERRO)


def app_linha(img, ox, oy, depois):
    d = ImageDraw.Draw(img)
    w = 760
    d.text((ox, oy), "Finalização · linha de lance" + (" (proposta)" if depois else " (hoje)"), font=fonte(16, True), fill=TXT)
    hl = 64 if depois else 44
    for i in range(3):
        y = oy + 30 + i * (hl + 6)
        caixa(d, ox, y, w, hl)
        d.text((ox + 14, y + hl / 2 - 10), "Lance %d   ·   250 m   ·   14:3%d" % (i + 1, i), font=fonte(16), fill=TXT)
        if not depois:
            for j, (cor, t) in enumerate([(AZUL, "✎"), (ERRO, "🗑")]):
                x = ox + w - 70 + j * 30
                d.rectangle([x, y + 10, x + 24, y + 34], outline=cor, width=2)
        else:
            for j, (cor, t) in enumerate([(AZUL, "Editar"), (ERRO, "Excluir")]):
                x = ox + w - 232 + j * 116
                caixa(d, x, y + 8, 100, 48, fill="#FFFFFF", borda=cor, lw=2)
                d.text((x + 22, y + 22), t, font=fonte(15, True), fill=cor)
    yb = oy + 30 + 3 * (hl + 6) + 4
    if not depois:
        d.text((ox, yb), "Editar e Excluir: ícones de 24 × 24 px com 6 px de vão (X=262 e X=292).", font=fonte(14), fill=ERRO)
        d.text((ox, yb + 22), "Dedo com luva cobre os dois. Rótulo cinza #94A3B8: contraste 2,6:1.", font=fonte(14), fill=ERRO)
    else:
        d.text((ox, yb), "Alvo de 48 px (fx_AlturaAcaoS), 16 px de vão, palavra junto do ícone.", font=fonte(14), fill=OK)
        d.text((ox, yb + 22), "Rótulo em fx_CorTextoSuave #64748B: contraste 4,8:1.", font=fonte(14), fill=OK)


def main():
    s = 0.9
    LW, LH = int(1280 * s), int(720 * s)
    M = 40
    img = Image.new("RGB", (2 * LW + 3 * M, LH + 760 + 3 * M + 60), "#FFFFFF")
    d = ImageDraw.Draw(img)
    d.text((M, 14), "Missão L · mockup antes/depois (esquema; valores de exemplo, não são dados reais)", font=fonte(24, True), fill=TXT)
    y1 = 86
    d.text((M, y1 - 30), "ANTES · BI, página Visão Geral (posições do projeto .pbip)", font=fonte(18, True), fill=ERRO)
    d.text((2 * M + LW, y1 - 30), "DEPOIS · proposta (mesmo canvas 1280 × 720)", font=fonte(18, True), fill=OK)
    bi_antes(img, M, y1, s)
    bi_depois(img, 2 * M + LW, y1, s)
    y2 = y1 + LH + 70
    d.text((M, y2 - 30), "ANTES · BI no celular", font=fonte(18, True), fill=ERRO)
    d.text((M + 340, y2 - 30), "DEPOIS · layout móvel", font=fonte(18, True), fill=OK)
    celular(img, M, y2, False)
    celular(img, M + 340, y2, True)
    xa = M + 720
    d.text((xa, y2 - 30), "ANTES · app no tablet", font=fonte(18, True), fill=ERRO)
    app_linha(img, xa, y2 + 6, False)
    d.text((xa, y2 + 290), "DEPOIS · app no tablet", font=fonte(18, True), fill=OK)
    app_linha(img, xa, y2 + 326, True)
    img.save(SAIDA)
    print("gravado:", SAIDA, img.size)


if __name__ == "__main__":
    main()
