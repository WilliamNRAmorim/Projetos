"""Compara os 20 PDFs do lote de teste (Analises/Lote_Teste_PackList, os mesmos publicados em 06/10) com os gerados.
Esses 20 têm streams comprimidos (outro gerador); descomprime e lê os textos."""
import os, re, zlib, base64
from gerar_lote import GMS

AQUI = os.path.dirname(os.path.abspath(__file__))
orig = os.path.join(GMS, 'Analises', 'Lote_Teste_PackList')
novo = os.path.join(AQUI, 'saida', '1_substituir_PackLists')


def texto(b):
    t = b.decode('latin-1')
    streams = re.findall(r'stream\r?\n(.*?)endstream', t, re.S)
    partes = []
    for s in streams:
        raw = s.encode('latin-1')
        try:
            partes.append(zlib.decompress(raw).decode('latin-1'))
        except Exception:
            try:
                partes.append(zlib.decompress(base64.a85decode(raw.strip(), adobe=raw.strip().startswith(b'<~'))).decode('latin-1'))
            except Exception:
                try:
                    partes.append(zlib.decompress(base64.a85decode(raw.strip().rstrip(b'~>').rstrip())).decode('latin-1'))
                except Exception:
                    partes.append(s)
    return '\n'.join(partes)


def tokens(t):
    un = lambda s: s.replace('\\272', '°').replace('\\(', '(').replace('\\)', ')').replace('\\\\', '\\')
    return [un(m) for m in re.findall(r'\(((?:[^()\\]|\\.|\([^()]*\))*)\)\s*Tj', t)]


if __name__ == '__main__':
    ok = 0
    for f in sorted(os.listdir(orig)):
        if not f.endswith('.pdf'):
            continue
        a = tokens(texto(open(os.path.join(orig, f), 'rb').read()))
        b = tokens(texto(open(os.path.join(novo, f), 'rb').read()))
        if f.startswith('PackList_2281'):
            print('antigo:', a[:40]); print('novo  :', b[:40])
        # compara só o miolo (data, id, pn, total e lances), ignorando legendas e rodapé
        pegar = lambda tk: [x for x in tk if re.fullmatch(r'[\d.,-]+', x) or re.fullmatch(r'[A-Z0-9-]{4,}', x)]
        dedup = lambda xs: [x for i, x in enumerate(xs) if i == 0 or x != xs[i - 1]]
        ia, ib = dedup(pegar(a)), dedup(pegar(b))
        print(f, 'tokens', len(a), len(b), 'miolo igual' if ia == ib else 'DIFERE')
        ok += ia == ib
    print('iguais:', ok)
