import csv,datetime as dt,json,sys,collections
b='C:/Users/U445131/Downloads/Projetos/GMS/Analises/Historico_Apontamento/'
rows=list(csv.reader(open(b+'Historico_Apontamento_carga_completa.csv',encoding='utf-8-sig'),delimiter=';'))
h=rows[0];rows=rows[1:]
M=sorted({r[3] for r in rows});Mi={m:i for i,m in enumerate(M)}
base=dt.date(2018,1,1)
def f(v):
    if v=='' : return ''
    x=round(float(v),2); return ('%g'%x)
def enc(r):
    d=(dt.date.fromisoformat(r[0])-base).days
    defs=''.join(L+f(v) for L,v in zip('ABCDEFGHIJKLMNOP',r[5:21]) if v not in ('','0','0.0'))
    ex=''
    if r[22] or r[23] or r[24]:
        dl=''.join(c for c in r[24] if c.isdigit())
        ex=f"{r[22]}~{r[23]}~{dl}"
    return f"{d},{r[1]},{Mi[r[3]] if r[3] else ''},{r[2]},{f(r[4])},{defs},{f(r[21])},{ex}"
enc_rows=[enc(r) for r in rows]
years=collections.OrderedDict()
for i,r in enumerate(rows): years.setdefault(r[0][:4],[]).append(i)
for y,ix in years.items(): print(y,ix[0]+1,ix[-1]+1,len(ix),sum(len(enc_rows[i]) for i in ix))
json.dump({'M':M,'rows':enc_rows},open(b+'enc.json','w',encoding='utf-8'),ensure_ascii=False)
