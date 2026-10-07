"""Gera os PDFs de packlist (mesmo layout dos PDFs de 06/10), com o código de barras novo:
 PN em Code 39 e TOTAL em Code 128 Start A (igual à macro do Excel antigo: texto = soma crua, vírgula).
Saída em pastas separadas para o William subir por conta própria; nada é gravado no SharePoint."""
import csv, collections, datetime as dt, os, re, sys, openpyxl

AQUI = os.path.dirname(os.path.abspath(__file__))
GMS = os.path.abspath(os.path.join(AQUI, '..', '..'))
SP = os.path.join(GMS, 'Sharepoint Data GMS')
OUT = os.path.join(AQUI, 'saida')

F = open(os.path.join(GMS, 'Telas', 'Formulas.txt'), encoding='utf-8').read()
P128 = re.search(r'fx_C128Patterns = "([01]+)"', F).group(1)
P39 = re.search(r'fx_C39Patterns = "([nw]+)"', F).group(1)
CS39 = re.search(r'fx_C39Charset = "(.*)";', F).group(1)
CS128 = ''.join(chr(32 + i) for i in range(95))

# ---------------------------------------------------------------- código de barras
fp = lambda n: '1100011101011' if n == 106 else P128[n * 11:n * 11 + 11]


def bits128A(t):
    v = CS128.index
    chk = (103 + sum(v(c) * (i + 1) for i, c in enumerate(t))) % 103
    return fp(103) + ''.join(fp(v(c)) for c in t) + fp(chk) + fp(106)


def runs(bits, m):
    out, i = [], 0
    while i < len(bits):
        if bits[i] == '1':
            j = i
            while j < len(bits) and bits[j] == '1':
                j += 1
            out.append((i * m, (j - i) * m))
            i = j
        else:
            i += 1
    return out


def bars39(t, n):
    out, x = [], 0.0
    for c in '*' + t.upper() + '*':
        k = CS39.find(c)
        k = 0 if k < 0 else k
        pat = P39[k * 9:k * 9 + 9]
        for j in range(9):
            w = (3 if pat[j] == 'w' else 1) * n
            if j % 2 == 0:
                out.append((x, w))
            x += w
        x += n
    return out, x - n


# ---------------------------------------------------------------- texto
REG = {' ': .278, ',': .278, '.': .278, '-': .333, '(': .333, ')': .333, '°': .4, 'm': .833, 'A': .667, 'B': .667, 'C': .722, 'D': .722, 'E': .667, 'F': .611, 'G': .778, 'H': .722, 'I': .278, 'J': .5, 'K': .667, 'L': .556, 'M': .833, 'N': .722, 'O': .778, 'P': .667, 'Q': .778, 'R': .722, 'S': .667, 'T': .611, 'U': .722, 'V': .667, 'W': .944, 'X': .667, 'Y': .667, 'Z': .611}
BLD = dict(REG, m=.889, A=.722, B=.722, C=.722, D=.722, J=.556, K=.722, L=.611, R=.722, U=.722)


def tw(s, sz, bold):
    t = BLD if bold else REG
    return sum(.556 if c.isdigit() else t.get(c, .556) for c in s) * sz


def esc(s):
    return s.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)').replace('°', '\\272')


f2 = lambda n: '%.2f' % n
br = lambda v: ('%.2f' % v).replace('.', ',')


def total_txt(vals):
    s = ('%.6f' % round(sum(vals), 6)).rstrip('0').rstrip('.')
    return s.replace('.', ',')


def stream(d):
    o = []
    box = lambda x, y, w, h, fill: o.append('%s rg 1.4 w %s %s %s %s re B' % (fill, f2(x), f2(y), f2(w), f2(h)))
    txt = lambda x, y, font, sz, s, g='0': o.append('%s g BT /%s %s Tf %s %s Td (%s) Tj ET' % (g, font, sz, f2(x), f2(y), esc(s)))
    ctr = lambda cx, y, font, sz, s: txt(cx - tw(s, sz, font == 'F2') / 2, y, font, sz, s)
    ys = [530.08, 498.90, 467.72, 436.54]
    for (k, v, sz), y in zip([('DATE', d['date'], 15), ('LOCAL', 'DANFOSS DRT', 15), ('ID PALLET', d['id'], 15), ('PART-NUMBER', d['pn'], 17)], ys):
        box(34.02, y, 107.72, 31.18, '1 1 1'); txt(42.52, y + 11.39, 'F2', 12, k)
        box(141.73, y, 246.61, 31.18, '1 1 1'); txt(150.24, y + (9.64 if sz == 17 else 10.34), 'F2', sz, v)
    cx = 211.185
    o.append('0 g')
    b, wid = bars39(d['pn'], 1.70)
    for x, w in b:
        o.append('%s 331.66 %s 62.36 re f' % (f2(cx - wid / 2 + x), f2(w)))
    txt(cx - tw(d['pn'], 9, False) / 2, 317.48, 'F1', 9, d['pn'].upper())
    box(34.02, 277.80, 354.33, 31.18, '.82 .82 .82'); ctr(cx, 288.84, 'F2', 13, 'TOTAL (m)')
    box(34.02, 226.78, 354.33, 51.02, '1 1 0'); ctr(cx, 240.39, 'F2', 34, br(d['total']))
    o.append('0 g')
    bits = bits128A(d['tt']); m = 2.5; tot = len(bits) * m
    for x, w in runs(bits, m):
        o.append('%s 150.24 %s 62.36 re f' % (f2(cx - tot / 2 + x), f2(w)))
    box(411.02, 530.08, 396.85, 31.18, '.82 .82 .82'); ctr(609.445, 540.77, 'F2', 14, 'PACKING LIST')
    cells = [(411.02, 47.62), (458.65, 150.80), (609.45, 47.62), (657.07, 150.80)]
    for i, s in enumerate(['N°', 'QTY (m)', 'N°', 'QTY (m)']):
        box(cells[i][0], 497.48, cells[i][1], 32.60, '.82 .82 .82'); ctr(cells[i][0] + cells[i][1] / 2, 510.78, 'F2', 10, s)
    L = d['lances'] + [0] * (26 - len(d['lances']))
    for i in range(13):
        y = 464.89 - 32.60 * i
        for k, s in enumerate([str(i + 1), br(L[i]), str(i + 14), br(L[i + 13])]):
            box(cells[k][0], y, cells[k][1], 32.60, '1 1 1'); ctr(cells[k][0] + cells[k][1] / 2, y + 12.80, 'F1', 11, s)
    if d.get('foot'):
        txt(34.02, 22.68, 'F1', 7, d['foot'], '.4')
    return '\n'.join(o) + '\n'


def pdf(d):
    s = stream(d)
    objs = ['<</Type/Catalog/Pages 2 0 R>>', '<</Type/Pages/Kids[3 0 R]/Count 1>>',
            '<</Type/Page/Parent 2 0 R/MediaBox[0 0 841.89 595.28]/Contents 7 0 R/Resources<</Font<</F1 4 0 R/F2 5 0 R/F3 6 0 R>>>>>>',
            '<</Type/Font/Subtype/Type1/BaseFont/Helvetica/Encoding/WinAnsiEncoding>>',
            '<</Type/Font/Subtype/Type1/BaseFont/Helvetica-Bold/Encoding/WinAnsiEncoding>>',
            '<</Type/Font/Subtype/Type1/BaseFont/Helvetica-Oblique/Encoding/WinAnsiEncoding>>',
            '<</Length %d>>\nstream\n%sendstream' % (len(s), s)]
    out = '%PDF-1.4\n'; offs = []
    for i, b in enumerate(objs):
        offs.append(len(out)); out += '%d 0 obj\n%s\nendobj\n' % (i + 1, b)
    xr = len(out)
    out += 'xref\n0 %d\n0000000000 65535 f \n' % (len(objs) + 1) + ''.join('%010d 00000 n \n' % o for o in offs)
    out += 'trailer\n<</Size %d/Root 1 0 R>>\nstartxref\n%d\n%%%%EOF' % (len(objs) + 1, xr)
    return out.encode('latin-1')


# ---------------------------------------------------------------- dados
def carregar_bd():
    wb = openpyxl.load_workbook(os.path.join(SP, 'BD Packing List.xlsx'), read_only=True, data_only=True)
    ids = collections.OrderedDict()
    for i, r in enumerate(wb['Data Base'].iter_rows(values_only=True)):
        if i < 2 or not r[0]:
            continue
        _id, pn, sl, q, tot, ts, cb, canc = r[:8]; pn = str(pn)
        d = ids.setdefault((int(_id), pn), dict(id=int(_id), pn=pn, sl=[], ts=ts, canc=False))
        d['sl'].append((int(sl or 0), float(q or 0)))
        if canc is True:
            d['canc'] = True
    for d in ids.values():
        d['sl'].sort(); d['lances'] = [q for _, q in d['sl']]
    return ids


def carregar_mapa():
    rows = list(csv.reader(open(os.path.join(GMS, 'Analises', 'Mapa_BDPackingList_x_ficha_producao.csv'), encoding='utf-8-sig'), delimiter=';'))[1:]
    por = {}
    for nivel, pid, ficha, op, pn, metros, ts, fim, qtd in rows:
        por[int(ficha)] = dict(packing=int(pid), ficha=int(ficha), op=op, pn=pn)
    return por


def carregar_gms():
    """OPs com lances (RegistrosInspeção.csv até 02/10 + delta_gms.txt) e fichas (ficha_producao.csv)."""
    fichas = {}
    for r in csv.DictReader(open(os.path.join(SP, 'ficha_producao.csv'), encoding='utf-8-sig')):
        fichas[r['OP']] = dict(ficha=int(r['ID']), pn=r['Mangueira'], proc=r['processo'])
    ops = collections.OrderedDict()
    for r in csv.DictReader(open(os.path.join(SP, 'RegistrosInspeção.csv'), encoding='utf-8-sig')):
        try:
            d = dt.datetime.strptime(r['DataHoraInspecao'], '%m/%d/%Y %I:%M %p')
            q = float(r['Quantidade'])
        except Exception:
            continue
        ops.setdefault(r['OP_ID'], []).append((d, q))
    delta = {}
    for l in open(os.path.join(AQUI, 'delta_gms.txt'), encoding='utf-8'):
        if not l.strip():
            continue
        op, fid, pn, last, q = l.strip().split('|')
        delta[op] = (int(fid), pn, dt.datetime.fromisoformat(last.replace('Z', '')) - dt.timedelta(hours=3), [float(x) for x in q.split(';')])
    return fichas, ops, delta


def nome(s):
    return re.sub(r'[^A-Za-z0-9._-]', '', s)


def gravar(pasta, arq, d, indice, grupo, extra=''):
    os.makedirs(os.path.join(OUT, pasta), exist_ok=True)
    d['tt'] = total_txt(d['lances']); d['total'] = sum(d['lances'])
    open(os.path.join(OUT, pasta, arq), 'wb').write(pdf(d))
    indice.append([grupo, pasta + '/' + arq, d['id'], d['pn'], len(d['lances']), round(d['total'], 2), d['tt'], d['date'], extra])


def pallets(lances):
    return [lances[i:i + 26] for i in range(0, len(lances), 26)] or [[]]


def main():
    bd = carregar_bd(); mapa = carregar_mapa(); fichas, regs, delta = carregar_gms()
    ind = []
    usados = set()
    # A: fichas que já têm PDF publicado (substituir)
    faltou = []
    for fid, m in sorted(mapa.items()):
        if fid == 3826:      # ficha pulada em 06/10 (BD 286,5 m x ficha 312,5 m)
            continue
        k = (m['packing'], m['pn']); k = k if k in bd else next((kk for kk in bd if kk[0] == m['packing']), None)
        if not k:
            faltou.append(fid); continue
        usados.add(k); b = bd[k]
        d = dict(date=b['ts'].strftime('%Y-%m-%d'), id=m['op'], pn=(m['pn'] or b['pn']).strip().upper(), lances=b['lances'],
                 foot='Reimpressao do BD Packing List antigo - packing #%d - importado em lote (MEL-237)' % b['id'])
        gravar('1_substituir_PackLists', 'PackList_%d_%s.pdf' % (fid, m['op']), d, ind, 'A_substitui_existente', 'packing BD #%d' % b['id'])
    # B: romaneios do BD sem ficha, não cancelados
    for k, b in bd.items():
        if b['canc'] or k in usados or not b['lances']:
            continue
        d = dict(date=b['ts'].strftime('%Y-%m-%d'), id=str(b['id']), pn=b['pn'].strip().upper(), lances=b['lances'],
                 foot='BD Packing List antigo - romaneio #%d (sem ficha no GMS) - importado (MEL-237)' % b['id'])
        gravar('2_BD_sem_ficha', 'PackListBD_%d_%s.pdf' % (b['id'], nome(b['pn'].upper())), d, ind, 'B_BD_sem_ficha', 'Packing_Manual OrigemBD=%d' % b['id'])
    # C: OPs do GMS sem romaneio no BD (reconstrução pelos lances)
    ja = {m['op'] for fid, m in mapa.items() if fid != 3826}
    pulados = []
    todas = set(regs) | set(delta)
    for op in sorted(todas):
        if op in ja:
            continue
        if op in delta:
            fid, pn, last, lances = delta[op]
            proc = 'Finalizado'
        else:
            fi = fichas.get(op)
            if not fi:
                pulados.append((op, 'sem ficha no GMS')); continue
            fid, pn, proc = fi['ficha'], fi['pn'], fi['proc']
            seq = sorted(regs[op]); lances = [q for _, q in seq]; last = seq[-1][0]
        if proc != 'Finalizado':
            pulados.append((op, 'ficha em %s (nao finalizada)' % proc)); continue
        if not pn:
            pulados.append((op, 'sem part-number')); continue
        pasta = '3_GMS_pos_BD' if last >= dt.datetime(2026, 5, 4) else '4_GMS_pre_BD'
        ps = pallets(lances)
        for n, ls in enumerate(ps, 1):
            sufixo = '' if len(ps) == 1 else '_P%d' % n
            d = dict(date=last.strftime('%Y-%m-%d'), id=op + ('' if len(ps) == 1 else '  .  PALLET %d' % n), pn=pn, lances=ls,
                     foot='Reconstruido do GMS (lances do RegistrosInspecao) - sem romaneio no BD (MEL-237)')
            gravar(pasta, 'PackList_%d_%s%s.pdf' % (fid, op, sufixo), d, ind, 'C_GMS_reconstruido', 'ficha %d%s' % (fid, '' if len(ps) == 1 else ' pallet %d de %d' % (n, len(ps))))
    with open(os.path.join(OUT, 'indice.csv'), 'w', newline='', encoding='utf-8-sig') as fh:
        w = csv.writer(fh, delimiter=';'); w.writerow(['grupo', 'arquivo', 'id_pallet', 'part_number', 'lances', 'total_m', 'texto_codigo_total', 'data', 'obs'])
        w.writerows(ind)
    with open(os.path.join(OUT, 'nao_gerados.csv'), 'w', newline='', encoding='utf-8-sig') as fh:
        w = csv.writer(fh, delimiter=';'); w.writerow(['op_ou_ficha', 'motivo']); w.writerows(pulados); w.writerows([(f, 'packing do mapa nao achado no BD') for f in faltou])
    c = collections.Counter(r[0] for r in ind)
    print(dict(c), 'total', len(ind), '| nao gerados', len(pulados), '| mapa sem BD', len(faltou))
    print(collections.Counter(p[1].split(' (')[0] for p in pulados))


if __name__ == '__main__':
    main()
