# -*- coding: utf-8 -*-
"""Gera prototipo.html: renderiza, com os números de novembro/2026 da planilha, o MESMO desenho das medidas
HP · SVG (reportExtensions.json). Os dados vêm do conferir.py (plano da aba Dados, produzido da aba MB51, M, até o corte).
Uso: python -I prototipo.py [--hoje AAAA-MM-DD] [--uteis 22]"""
import sys, os, argparse, math, datetime as dt, collections, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import conferir as C

VERM, OK, SU, LI = "#E2000F", "#3C3C3B", "#8A8A88", "#D9D9D9"


def br(v, c=0):
    return C.br(v, c)


def k(v):
    return br(v / 1000, 1) + "k"


def dados(hoje, uteis):
    linhas, _r, _k, _c, _u = C.ler_plano(C.PLAN)
    mb = C.ler_mb51_planilha(C.PLAN)
    chaves = {l["mang"].upper() for l in linhas}
    fim = hoje - dt.timedelta(days=1)
    datas = sorted({d for kk, d, q, u in mb if C.MES <= d <= fim and kk in chaves and u == "M"})
    corte = max(datas)
    prod = collections.defaultdict(float)
    for kk, d, q, u in mb:
        if C.MES <= d <= corte and u == "M" and not kk.startswith("FM"):
            prod[kk] += q
    return linhas, prod, corte, len(datas), chaves


def grupos(linhas, prod, campo):
    g = collections.OrderedDict()
    for l in linhas:
        a = g.setdefault(l[campo], [0.0, 0.0])
        a[0] += l["vol"]
        a[1] += prod.get(l["mang"].upper(), 0.0)
    return [(n, p, q) for n, (p, q) in g.items() if p > 0]


def svg(w, h, corpo):
    return f"<svg xmlns='http://www.w3.org/2000/svg' width='{w}' height='{h}' viewBox='0 0 {w} {h}' font-family='Segoe UI, sans-serif'>{corpo}</svg>"


def cartoes(plano, prod, fora, ritmo, uteis, cont, rest, corte, nome_mes):
    pct = prod / plano
    atraso = ritmo * plano - prod
    fechar = (plano - prod) / rest if rest > 0 else None
    diario = plano / uteis
    cpr = VERM if pct < ritmo else OK
    cat = VERM if atraso > 0 else OK
    nota = f"  ·  +{br(fora)} m fora do plano" if fora > 0.5 else ""
    f1 = lambda v: f"{v:.1f}"
    s = f"<rect width='253' height='108' rx='8' fill='#fff'/><rect width='253' height='4' rx='2' fill='{OK}'/>"
    s += f"<text x='16' y='28' font-size='12' fill='{SU}'>Plano de {nome_mes}</text>"
    s += f"<text x='16' y='64' font-size='26' font-weight='700' fill='{OK}'>{br(plano)} m</text>"
    s += f"<text x='16' y='88' font-size='10' fill='{SU}'>{uteis} dias úteis</text>"
    s += f"<g transform='translate(265,0)'><rect width='253' height='108' rx='8' fill='#fff'/><rect width='253' height='4' rx='2' fill='{cpr}'/>"
    s += f"<text x='16' y='28' font-size='12' fill='{SU}'>Produzido até {corte:%d/%m}</text>"
    s += f"<text x='16' y='64' font-size='26' font-weight='700' fill='{cpr}'>{br(prod)} m</text>"
    s += f"<text x='237' y='64' font-size='16' font-weight='700' text-anchor='end' fill='{cpr}'>{br(pct * 100, 1)}%</text>"
    s += f"<rect x='16' y='76' width='221' height='6' rx='3' fill='{LI}'/><rect x='16' y='76' width='{f1(min(1, pct) * 221)}' height='6' rx='3' fill='{cpr}'/>"
    s += f"<rect x='{f1(16 + min(1, ritmo) * 221 - 1)}' y='72' width='2' height='14' fill='{OK}'/>"
    s += f"<text x='16' y='100' font-size='10' fill='{SU}'>ritmo esperado {br(ritmo * 100, 1)}%{nota}</text></g>"
    s += f"<g transform='translate(530,0)'><rect width='253' height='108' rx='8' fill='#fff'/><rect width='253' height='4' rx='2' fill='{cat}'/>"
    s += f"<text x='16' y='28' font-size='12' fill='{SU}'>{'Atrasado' if atraso > 0 else 'Adiantado'}</text>"
    s += f"<text x='16' y='64' font-size='26' font-weight='700' fill='{cat}'>{'−' if atraso > 0 else '+'}{br(abs(atraso))} m</text>"
    s += f"<text x='16' y='88' font-size='10' fill='{SU}'>contra o ritmo de {cont} de {uteis} dias úteis</text></g>"
    fechado = rest <= 0
    cf = VERM if (not fechado and fechar > 0 and fechar > diario) else OK
    val = "Mês fechado" if fechado else ("Plano atingido" if fechar <= 0 else f"{br(fechar)} m/dia")
    sub = ("" if (fechado or fechar <= 0) else f"nos {rest} dias que faltam · ") + f"plano {br(diario)} m/dia"
    s += f"<g transform='translate(795,0)'><rect width='253' height='108' rx='8' fill='#fff'/><rect width='253' height='4' rx='2' fill='{OK}'/>"
    s += f"<text x='16' y='28' font-size='12' fill='{SU}'>Para fechar o mês</text>"
    s += f"<text x='16' y='64' font-size='26' font-weight='700' fill='{cf}'>{val}</text>"
    s += f"<text x='16' y='88' font-size='10' fill='{SU}'>{sub}</text></g>"
    return svg(1048, 108, s)


def barras(g, titulo, w, h, ritmo):
    g = sorted(g, key=lambda x: (-x[1], x[0]))
    n = len(g)
    pitch = min(30, (h - 62) / n)
    bh = min(10, pitch * 0.5)
    fs = 10 if pitch < 18 else 11
    bw = w - 62 - 196
    xr = 196 + min(1, ritmo) * bw
    s = f"<rect width='{w}' height='{h}' rx='8' fill='#fff'/>"
    s += f"<text x='14' y='22' font-size='13' font-weight='600' fill='{OK}'>{titulo}</text>"
    s += f"<text x='14' y='38' font-size='10' fill='{SU}'>% do plano do mês · traço = ritmo esperado ({br(ritmo * 100, 1)}%) · vermelho = atrás do ritmo</text>"
    for i, (nome, pl, pr) in enumerate(g):
        cy = 54 + (i + 0.5) * pitch
        pct = pr / pl
        c = VERM if pct < ritmo else OK
        s += f"<text x='14' y='{cy + 4:.1f}' font-size='{fs}' fill='{OK}'>{html.escape(nome)}<tspan font-size='10' fill='{SU}'>  {k(pl)}</tspan></text>"
        s += f"<rect x='196' y='{cy - bh / 2:.1f}' width='{bw}' height='{bh:.1f}' rx='2' fill='{LI}' fill-opacity='0.5'/>"
        s += f"<rect x='196' y='{cy - bh / 2:.1f}' width='{min(1, pct) * bw:.1f}' height='{bh:.1f}' rx='2' fill='{c}'/>"
        s += f"<rect x='{xr - 1:.1f}' y='{cy - bh / 2 - 3:.1f}' width='2' height='{bh + 6:.1f}' fill='{OK}'/>"
        s += f"<text x='{w - 14}' y='{cy + 4:.1f}' font-size='{fs}' font-weight='700' text-anchor='end' fill='{c}'>{br(pct * 100, 1)}%</text>"
    return svg(w, h, s)


def aneis(g, ritmo):
    def chave(t):
        try:
            a = int(t[0])
        except ValueError:
            a = 9
        return (a * 10 + (0 if t[-1] == "T" else 1), t)
    g = sorted(g, key=lambda x: chave(x[0]))
    n = len(g)
    s = "<rect width='520' height='132' rx='8' fill='#fff'/>"
    s += f"<text x='14' y='22' font-size='13' font-weight='600' fill='{OK}'>Quanto de cada tipo saiu?</text>"
    s += f"<text x='14' y='38' font-size='10' fill='{SU}'>% do plano do mês · vermelho = atrás do ritmo ({br(ritmo * 100, 1)}%)</text>"
    for i, (nome, pl, pr) in enumerate(g):
        cx = 520 * (i + 0.5) / n
        pct = pr / pl
        c = VERM if pct < ritmo else OK
        s += f"<circle cx='{cx:.1f}' cy='76' r='24' fill='none' stroke='{LI}' stroke-width='8'/>"
        s += f"<circle cx='{cx:.1f}' cy='76' r='24' fill='none' stroke='{c}' stroke-width='8' stroke-dasharray='{min(1, pct) * 150.8:.1f} 150.8' transform='rotate(-90 {cx:.1f} 76)'/>"
        s += f"<text x='{cx:.1f}' y='80' font-size='11' font-weight='700' text-anchor='middle' fill='{c}'>{br(pct * 100)}%</text>"
        s += f"<text x='{cx:.1f}' y='122' font-size='11' font-weight='600' text-anchor='middle' fill='{OK}'>{nome}<tspan font-weight='400' font-size='10' fill='{SU}'>  {k(pl)}</tspan></text>"
    return svg(520, 132, s)


def atrasadas(linhas, prod, ritmo):
    t = [(ritmo * l["vol"] - prod.get(l["mang"].upper(), 0.0), l["mang"]) for l in linhas if l["vol"] > 0]
    t = sorted([x for x in t if x[0] > 0], key=lambda x: (-x[0], x[1]))[:8]
    s = "<rect width='1048' height='136' rx='8' fill='#fff'/>"
    s += f"<text x='14' y='22' font-size='13' font-weight='600' fill='{OK}'>Mangueiras mais atrasadas</text>"
    s += f"<text x='14' y='38' font-size='10' fill='{SU}'>metros abaixo do ritmo esperado do mês (ritmo × plano − produzido)</text>"
    mx = t[0][0] if t else 1
    for i, (a, nome) in enumerate(t):
        x0 = 14 + (i // 4) * 524
        cy = 58 + (i % 4) * 22
        bw = a / mx * 280
        s += f"<text x='{x0}' y='{cy + 4}' font-size='11' fill='{OK}'>{html.escape(nome)}</text>"
        s += f"<rect x='{x0 + 120}' y='{cy - 5}' width='{bw:.1f}' height='10' rx='2' fill='{VERM}'/>"
        s += f"<text x='{x0 + 126 + bw:.1f}' y='{cy + 4}' font-size='11' font-weight='600' fill='{VERM}'>−{br(a)}</text>"
    return svg(1048, 136, s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hoje", default="2026-11-19")
    ap.add_argument("--uteis", type=int, default=22)
    a = ap.parse_args()
    hoje = dt.date.fromisoformat(a.hoje)
    linhas, prod, corte, cont, chaves = dados(hoje, a.uteis)
    uteis = a.uteis
    ritmo = min(1, cont / uteis)
    plano = sum(l["vol"] for l in linhas)
    pr = sum(prod.get(l["mang"].upper(), 0.0) for l in linhas)
    cs, ar, ti = grupos(linhas, prod, "cs"), grupos(linhas, prod, "arame"), grupos(linhas, prod, "tipo")
    fora = 0.0  # produção de mangueira (MRP AIH) sem linha no plano: 0 em nov/2026 (conferir.py --sap)
    blocos = [
        (216, 160, cartoes(plano, pr, fora, ritmo, uteis, cont, uteis - cont, corte, "novembro")),
        (216, 280, barras(cs, "Quanto de cada C.Standard saiu?", 516, 276, ritmo)),
        (744, 280, aneis(ti, ritmo)),
        (744, 424, barras(ar, "Quanto de cada arame saiu?", 520, 132, ritmo)),
        (216, 568, atrasadas(linhas, prod, ritmo)),
    ]
    div = "".join(f"<div style='position:absolute;left:{x}px;top:{y}px'>{s}</div>" for x, y, s in blocos)
    menu = "".join(f"<div style='position:absolute;left:0;top:{y}px;width:200px;height:32px;line-height:32px;padding-left:19px;box-sizing:border-box;font-size:10px;font-weight:700;color:{'#fff' if ativo else '#BDBDBD'};background:{'#2A2A2A' if ativo else 'none'}'>{t}</div>"
                   for y, t, ativo in [(530, "Produção x meta", False), (562, "Plano de mangueira x SAP", True)])
    pg = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Prévia: Plano de mangueira x SAP</title>
<style>body{{margin:0;background:#ddd;font-family:'Segoe UI',sans-serif}}#p{{position:relative;width:1280px;height:720px;background:#F2F3F5;margin:12px auto;overflow:hidden}}</style></head><body>
<div id="p">
<div style="position:absolute;left:0;top:0;width:200px;height:720px;background:#2A2A2A"></div>{menu}
<div style="position:absolute;left:16px;top:510px;font-size:10px;color:#7A7A7A;font-weight:600">PRODUÇÃO SAP</div>
<div style="position:absolute;left:216px;top:12px;font-size:20px;font-weight:600;color:#3C3C3B">Plano de mangueira x SAP</div>
<div style="position:absolute;left:216px;top:44px;font-size:12px;color:#7A7A7A">Plano mensal do planejamento contra a produção do SAP, por C.Standard, tipo e arame</div>
<div style="position:absolute;left:216px;top:88px;width:1048px;height:56px;background:#fff;border-radius:8px"></div>
<div style="position:absolute;left:216px;top:88px;width:8px;height:56px;background:{VERM};border-radius:4px"></div>
<div style="position:absolute;left:242px;top:100px;font-size:15px;font-weight:600;color:#3C3C3B">Estamos no ritmo para fechar o plano de mangueira?</div>
<div style="position:absolute;left:216px;top:109px;width:1028px;text-align:right;font-size:13px;color:{SU}">MB51 até {corte:%d/%m/%Y} · {cont} de {uteis} dias úteis</div>
{div}
</div>
<p style="text-align:center;font:12px 'Segoe UI';color:#555">Prévia gerada por prototipo.py com a planilha Novembro-10.xlsm (plano da aba Dados, produzido da aba MB51, unidade M, até {corte:%d/%m}); {uteis} dias úteis (modelo), não 23 (planilha). Cabeçalho e menu aproximados; os cinco gráficos são o desenho exato das medidas.</p>
</body></html>"""
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prototipo.html")
    open(out, "w", encoding="utf-8").write(pg)
    print("gerado", out)


if __name__ == "__main__":
    main()
