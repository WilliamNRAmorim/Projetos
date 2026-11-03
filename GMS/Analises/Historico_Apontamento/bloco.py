# Uso: python -I -X utf8 bloco.py <tituloInicial> <quantidade>   (Title = numero da linha no CSV, 1..29049)
# Imprime as linhas codificadas do bloco (uma por linha) e a soma esperada de aprovado/reprovado, para conferir depois.
import json,sys
d=json.load(open('enc.json',encoding='utf-8'))
a=int(sys.argv[1]);n=int(sys.argv[2]);ls=d['rows'][a-1:a-1+n]
sa=sr=0
for l in ls:
    p=l.split(',')
    sa+=float(p[4]) if p[4] else 0; sr+=float(p[6]) if p[6] else 0
print(f'# INICIO {a} QTD {len(ls)} APROV {sa:.1f} REP {sr:.1f}')
print('\n'.join(ls))
