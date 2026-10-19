"""Simula os packlists de 6 e 7/10/2026 com o código de barras novo (igual ao Excel antigo).
Dados: dados.txt (RegistrosInspeção + Packing_Manual). Barras: mesmas tabelas do Telas/Formulas.txt."""
import re, html, datetime as dt, openpyxl

F = open('../../GMS/Telas/Formulas.txt', encoding='utf-8').read()
p128 = re.search(r'fx_C128Patterns = "([01]+)"', F).group(1)
cs128 = re.search(r'fx_C128Charset = "(.*)";', F).group(1).replace('""', '"')
c39cs = re.search(r'fx_C39Charset = "(.*)";', F).group(1)
c39p = re.search(r'fx_C39Patterns = "([nw]+)"', F).group(1)


def fp(n):
    return '1100011101011' if n == 106 else p128[n * 11:n * 11 + 11]


def bits128A(t):
    v = lambda c: cs128.index(c)
    chk = (103 + sum(v(c) * (i + 1) for i, c in enumerate(t))) % 103
    return fp(103) + ''.join(fp(v(c)) for c in t) + fp(chk) + fp(106)


def bits39(t):
    out = ''
    for c in '*' + t.upper() + '*':
        k = c39cs.index(c) if c in c39cs else 0
        for j, ch in enumerate(c39p[k * 9:k * 9 + 9]):
            out += ('1' if j % 2 == 0 else '0') * (3 if ch == 'w' else 1)
        out += '0'
    return out


def svg(bits, alt, cap=None):
    n = max(1, 520 // len(bits))
    x0 = (560 - len(bits) * n) // 2
    h = alt - (32 if cap else 12)
    path = ''.join('M%d 6h%dv%dh-%dz' % (x0 + i * n, n, h, n) for i, b in enumerate(bits) if b == '1')
    t = ''
    if cap:
        t = "<text x='280' y='%d' text-anchor='middle' font-family='monospace' font-size='16'>%s</text>" % (alt - 8, html.escape(cap))
    return ("<svg xmlns='http://www.w3.org/2000/svg' width='560' height='%d' viewBox='0 0 560 %d' shape-rendering='crispEdges'>"
            "<rect width='100%%' height='100%%' fill='white'/><path d='%s'/>%s</svg>") % (alt, alt, path, t)


def total_txt(vals):
    s = ('%.6f' % round(sum(vals), 6)).rstrip('0').rstrip('.')
    return s.replace('.', ',')


br = lambda v: ('%.2f' % v).replace('.', ',')

rows = []
for l in open('dados.txt', encoding='utf-8'):
    if not l.strip():
        continue
    op, pn, cab, t0, t1, q = l.strip().split('|')
    vals = [float(x) for x in q.split(';')]
    d = dt.datetime.fromisoformat(t1.replace('Z', '')) - dt.timedelta(hours=3)
    rows.append(dict(op=op, pn=pn, cab=cab, data=d.strftime('%Y-%m-%d %H:%M'), vals=vals, total=sum(vals), tt=total_txt(vals)))

pages = []
for r in rows:
    v = r['vals'] + [None] * (26 - len(r['vals']))
    tr = ''.join("<tr><td>%d</td><td>%s</td><td>%d</td><td>%s</td></tr>" % (
        i + 1, '' if v[i] is None else br(v[i]), i + 14, '' if v[i + 13] is None else br(v[i + 13])) for i in range(13))
    tarja = "<div class='tarja'>PACKING MANUAL — SEM OP NO SISTEMA</div>" if r['cab'] == 'MANUAL' else ''
    pages.append(
        "<section class='pg'><div class='l'>"
        "<table class='k'><tr><th>DATE</th><td>%s</td></tr><tr><th>LOCAL</th><td>DANFOSS DRT</td></tr>"
        "<tr><th>ID PALLET</th><td>%s</td></tr><tr><th>PART-NUMBER</th><td class='pn'>%s</td></tr></table>%s"
        "<div class='th'>TOTAL (m)</div><div class='tv'>%s</div>%s<div class='tt'>(texto do código do total: %s)</div>%s</div>"
        "<div class='r'><div class='ph'>PACKING LIST</div><table class='lt'><tr><th>N°</th><th>QTY (m)</th><th>N°</th><th>QTY (m)</th></tr>%s</table></div></section>"
        % (r['data'], r['op'], html.escape(r['pn']), svg(bits39(r['pn']), 120, r['pn'].upper()), br(r['total']),
           svg(bits128A(r['tt']), 130), r['tt'], tarja, tr))

css = """@page{size:297mm 210mm;margin:0}body{margin:0;font-family:'Open Sans',Arial,sans-serif}
.pg{width:1123px;height:794px;box-sizing:border-box;padding:28px;page-break-after:always;display:flex;gap:20px;border:1px solid #000}
.l{width:560px}.r{flex:1}table{border-collapse:collapse}.k{width:100%}.k th,.k td{border:2px solid #000;font-weight:700;text-align:left;padding:4px 8px;font-size:24px}.k th{width:170px;font-size:18px}.k td.pn{font-size:32px}
.th,.tv{border:2px solid #000;text-align:center;font-weight:700}.th{background:#d0d0d0;font-size:24px;margin-top:8px}.tv{background:#ff0;font-size:48px;padding:14px}
.ph{border:2px solid #000;background:#d0d0d0;text-align:center;font-weight:700;font-size:26px;padding:6px}.lt{width:100%;margin-top:6px}.lt th{background:#d0d0d0}.lt th,.lt td{border:1px solid #000;padding:8px 12px;font-size:19px}
.tarja{border:3px solid #c0392b;color:#c0392b;text-align:center;font-weight:700;font-size:22px;padding:8px;margin-top:6px}.tt{font:12px monospace;color:#555}"""
open('Packlists_6e7_Outubro.html', 'w', encoding='utf-8').write(
    "<!doctype html><meta charset='utf-8'><title>Packlists 6 e 7 de outubro</title><style>%s</style>%s" % (css, ''.join(pages)))

wb = openpyxl.Workbook()
ws = wb.active
ws.title = 'Resumo'
ws.append(['OP (ID PALLET)', 'Part-number', 'Origem', 'Data/hora da última leitura (-03)', 'Lances', 'Total (m)',
           'Texto do código do PN (Code 39)', 'Texto do código do total (Code 128A)'])
for r in rows:
    ws.append([int(r['op']), r['pn'], r['cab'], r['data'], len(r['vals']), round(r['total'], 2), '*' + r['pn'].upper() + '*', r['tt']])
w2 = wb.create_sheet('Lances')
w2.append(['OP', 'Part-number', 'Nº', 'QTY (m)'])
for r in rows:
    for i, x in enumerate(r['vals']):
        w2.append([int(r['op']), r['pn'], i + 1, x])
for c, wd in zip('ABCDEFGH', (16, 14, 12, 30, 8, 10, 32, 36)):
    ws.column_dimensions[c].width = wd
wb.save('Packlists_6e7_Outubro.xlsx')
print(len(rows), 'folhas;', sum(1 for r in rows if ',' in r['tt']), 'com decimal no total')

# Uma folha por arquivo (para imprimir um por um): paginas/<OP>_<PN>.html
import os, subprocess, pathlib
os.makedirs('paginas', exist_ok=True)
os.makedirs('pdf', exist_ok=True)
EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
for r, pg in zip(rows, pages):
    nome = '%s_%s' % (r['op'], re.sub(r'[^A-Za-z0-9-]', '', r['pn']))
    h = "<!doctype html><meta charset='utf-8'><title>%s</title><style>%s</style>%s" % (nome, css, pg)
    hp = pathlib.Path('paginas/%s.html' % nome).resolve()
    hp.write_text(h, encoding='utf-8')
    pdf = pathlib.Path('pdf/%s.pdf' % nome).resolve()
    subprocess.run([EDGE, '--headless', '--disable-gpu', '--no-pdf-header-footer',
                    '--print-to-pdf=' + str(pdf), hp.as_uri()], check=False,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
print('pdfs:', len(os.listdir('pdf')))
