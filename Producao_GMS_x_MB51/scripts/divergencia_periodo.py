"""Divergencia por mangueira (SAP - GMS) num periodo, antes e depois das tratativas (ops_tratadas.csv).
Rodar na pasta Producao_GMS_x_MB51: python -I divergencia_periodo.py [inicio] [fim]  (padrao 2026-05-20 a 2026-09-20)
Mesma regra do divergencia_por_mangueira.py: OP so no SAP entra apenas se diminuir a divergencia da mangueira."""
import os as _os, pathlib as _pl; _os.chdir(_pl.Path(__file__).resolve().parents[1])  # roda sempre a partir de Producao_GMS_x_MB51
import sys, csv, collections, itertools, datetime as dt, openpyxl
ini=dt.datetime.fromisoformat(sys.argv[1]) if len(sys.argv)>1 else dt.datetime(2026,5,20)
fim=(dt.datetime.fromisoformat(sys.argv[2]) if len(sys.argv)>2 else dt.datetime(2026,9,20)).replace(hour=23,minute=59)
TRAT={r['op'] for r in csv.DictReader(open('dados/ops_tratadas.csv',encoding='utf-8'),delimiter=';') if r['estado']=='tratada'}  # pendentes continuam contando
wb=openpyxl.load_workbook('Conferencia_Lances_por_OP.xlsx',read_only=True)
res=list(wb['Resumo por OP'].iter_rows(min_row=2,values_only=True))
sem=list(wb['MB51 sem GMS'].iter_rows(min_row=2,values_only=True))
def calcular(tratadas):
    dif=collections.defaultdict(float); so=collections.defaultdict(list)
    for r in res:
        if r[5] and ini<=r[5]<=fim and r[2] and r[0] not in tratadas: dif[r[2]]+=(r[10] or 0)-(r[9] or 0)
    for r in sem:
        if r[3] and ini<=r[3]<=fim and r[0] not in tratadas: so[r[1]].append(r)
    for m,ops in so.items():
        base=dif[m]
        if len(ops)<=15:
            melhor=min((c for k in range(len(ops)+1) for c in itertools.combinations(ops,k)),key=lambda c:(abs(base+sum(o[6] for o in c)),len(c)))
        else:
            melhor=[];d=base
            for o in sorted(ops,key=lambda o:-abs(o[6])):
                if abs(d+o[6])<abs(d): melhor.append(o); d+=o[6]
        dif[m]=base+sum(o[6] for o in melhor)
    d={m:v for m,v in dif.items() if abs(v)>=0.05}
    return d
for nome,t in (('ANTES das tratativas',set()),('DEPOIS das tratativas',TRAT)):
    d=calcular(t)
    mais=sum(v for v in d.values() if v>0); menos=sum(v for v in d.values() if v<0)
    print(f"{nome}: {ini:%d/%m/%Y} a {fim:%d/%m/%Y} | {len(d)} mangueiras | SAP a mais {mais:,.1f} m | SAP a menos {menos:,.1f} m | total |dif| {mais-menos:,.1f} m | liquido {mais+menos:,.1f} m")
    if t:
        for m,v in sorted(d.items(),key=lambda x:-abs(x[1]))[:8]: print(f"   {m:12s} {v:+10.1f}")
