"""Gera CARTAO_DE_ESCALA_A4.pdf: cartão de escala para fotografar peças (imprimir em 100%)."""
import os
import pymupdf as fitz

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, "CARTAO_DE_ESCALA_A4.pdf")
MM = 72 / 25.4
W, H = 210 * MM, 297 * MM
PRETO = (0, 0, 0)
CINZA = (0.8, 0.8, 0.8)


def p(x, y):
    return fitz.Point(x * MM, y * MM)


def linha(pg, x0, y0, x1, y1, w=0.4, cor=PRETO):
    pg.draw_line(p(x0, y0), p(x1, y1), color=cor, width=w)


def texto(pg, x, y, t, tam=8, fonte="helv", alinhar=0):
    f = fitz.Font(fonte)
    larg = f.text_length(t, fontsize=tam)
    x_pt = x * MM - (larg / 2 if alinhar == 1 else larg if alinhar == 2 else 0)
    pg.insert_text(fitz.Point(x_pt, y * MM), t, fontsize=tam, fontname=fonte, color=PRETO)


def main():
    doc = fitz.open()
    pg = doc.new_page(width=W, height=H)
    X0, Y0 = 15, 15  # origem das réguas (mm)

    # grade clara de 10 mm na área central
    for i in range(0, 181, 10):
        linha(pg, X0 + i, Y0 + 10, X0 + i, 282, 0.2, CINZA)
    for j in range(Y0 + 10, 283, 10):
        linha(pg, X0, j, X0 + 180, j, 0.2, CINZA)

    # régua em mm: borda superior (0-180) e borda esquerda (0-180 para baixo)
    linha(pg, X0, Y0, X0 + 180, Y0, 0.6)
    linha(pg, X0, Y0, X0, Y0 + 180, 0.6)
    for i in range(0, 181):
        c = 5 if i % 10 == 0 else 3.5 if i % 5 == 0 else 2
        linha(pg, X0 + i, Y0, X0 + i, Y0 + c, 0.4 if i % 5 == 0 else 0.25)
        linha(pg, X0, Y0 + i, X0 + c, Y0 + i, 0.4 if i % 5 == 0 else 0.25)
        if i % 10 == 0 and i > 0:
            texto(pg, X0 + i, Y0 + 9, str(i // 10), 7, alinhar=1)
            texto(pg, X0 + 6, Y0 + i + 1, str(i // 10), 7)
    texto(pg, X0 + 2, Y0 - 3, "mm  (numeros = cm)", 7)

    # régua em polegadas (1/16) na borda inferior, 0 a 7 pol (178 mm)
    yb = 287
    linha(pg, X0, yb, X0 + 7 * 25.4, yb, 0.6)
    for k in range(0, 7 * 16 + 1):
        x = X0 + k * 25.4 / 16
        c = 5 if k % 16 == 0 else 4 if k % 8 == 0 else 3 if k % 4 == 0 else 2 if k % 2 == 0 else 1.2
        linha(pg, x, yb, x, yb - c, 0.4 if k % 4 == 0 else 0.25)
        if k % 16 == 0:
            texto(pg, x, yb + 4, str(k // 16), 7, alinhar=1)
    texto(pg, X0 + 7 * 25.4 + 2, yb + 1, "pol (1/16)", 7)

    # régua em mm na borda direita também (0-180 para baixo, a partir de 15 mm)
    xr = 195
    linha(pg, xr, Y0, xr, Y0 + 180, 0.6)
    for i in range(0, 181):
        c = 5 if i % 10 == 0 else 3.5 if i % 5 == 0 else 2
        linha(pg, xr, Y0 + i, xr - c, Y0 + i, 0.4 if i % 5 == 0 else 0.25)
        if i % 10 == 0 and i > 0:
            texto(pg, xr - 6, Y0 + i + 1, str(i // 10), 7, alinhar=2)

    # círculos de referência 5 a 60 mm, de 5 em 5 (3 fileiras)
    texto(pg, 26, 36, "Círculos de referência (diâmetro em mm)", 8, "hebo")
    for diams, cy_, gap in (([5, 10, 15, 20, 25, 30, 35], 58, 3), ([40, 45, 50], 105, 8), ([55, 60], 163, 10)):
        x = 22
        for d in diams:
            x += d / 2
            pg.draw_circle(p(x, cy_), d / 2 * MM, color=PRETO, width=0.5)
            texto(pg, x, cy_ + d / 2 + 3.5, f"{d}", 6.5, alinhar=1)
            x += d / 2 + gap

    # quadrado de controle 50x50 mm
    qx, qy = 26, 205
    pg.draw_rect(fitz.Rect(qx * MM, qy * MM, (qx + 50) * MM, (qy + 50) * MM), color=PRETO, width=1.0)
    texto(pg, qx + 25, qy + 26, "50 x 50 mm", 10, "hebo", 1)
    texto(pg, qx + 25, qy + 32, "quadrado de controle", 7, alinhar=1)
    texto(pg, qx, qy + 57, "Imprimir em 100% / tamanho real.", 9, "hebo")
    texto(pg, qx, qy + 62, "Confira: este quadrado deve medir 50 mm.", 9, "hebo")

    # campos
    fx = 88
    texto(pg, fx, 212, "Material / NI:", 10, "hebo")
    linha(pg, fx + 28, 212.5, 188, 212.5, 0.5)
    texto(pg, fx, 223, "Pallet / Caixa:", 10, "hebo")
    linha(pg, fx + 30, 223.5, 188, 223.5, 0.5)

    # lembrete
    texto(pg, fx, 236, "Foto ideal:", 10, "hebo")
    for i, t in enumerate([
        "1. Peça inteira, de cima, sobre o cartão (perto das réguas).",
        "2. Close das gravações e marcações (código, números, letras).",
        "3. Segunda foto de lado (altura / espessura).",
        "Câmera parada, de frente, sem inclinar; boa luz, sem sombra forte.",
    ]):
        texto(pg, fx, 242 + i * 5.5, t, 8)

    doc.save(SAIDA, deflate=True)
    print("ok", SAIDA)


if __name__ == "__main__":
    main()
