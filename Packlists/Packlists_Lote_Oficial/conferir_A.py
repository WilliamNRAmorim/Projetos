"""Confere os 778 PDFs gerados (grupo A) contra os PDFs já publicados no SharePoint:
hash SHA-1 de 'nome|data|id|pn|lances' (o mesmo calculado dentro do navegador, só leitura)."""
import re, os, hashlib

AQUI = os.path.dirname(os.path.abspath(__file__))
ERROS = {'PackList_%s.pdf' % x for x in "2281_28826448 2478_28970607 2531_28913384 2582_29059116 2699_29146054 2781_29219224 2866_29234470 2879_29321284 2950_29380434 3045_29701059 3180_29788689 3259_29852432 3354_29894895 3369_29861920 3410_30053027 3496_30066875 3556_30036775 3631_30137264 3689_30206903 3752_30106390".split()}


def parse(b):
    t = b.decode('latin-1')
    un = lambda s: s.replace('\\272', '°').replace('\\(', '(').replace('\\)', ')').replace('\\\\', '\\')
    tok = [un(m) for m in re.findall(r'\(((?:[^()\\]|\\.|\([^()]*\))*)\)\s*Tj', t)]
    i = tok.index('PACKING LIST')
    rows = tok[i + 5:i + 5 + 52]
    L = [0.0] * 26
    for r in range(13):
        L[r] = float(rows[r * 4 + 1].replace(',', '.'))
        L[r + 13] = float(rows[r * 4 + 3].replace(',', '.'))
    return tok[1], tok[5], tok[7], L


if __name__ == '__main__':
    pasta = os.path.join(AQUI, 'saida', '1_substituir_PackLists')
    lines = []
    for f in sorted(os.listdir(pasta)):
        if f in ERROS:
            continue
        d, i, pn, L = parse(open(os.path.join(pasta, f), 'rb').read())
        lines.append('%s|%s|%s|%s|%s' % (f, d, i, pn, ';'.join('%.2f' % x for x in L)))
    lines.sort()
    h = hashlib.sha1('\n'.join(lines).encode()).hexdigest()
    esperado = '4e96e504518641c8de868467e2d11f619e6dfc37'
    print(len(lines), h, 'IGUAL' if h == esperado else 'DIFERENTE')
