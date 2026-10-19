"""Top 10 OPs mais divergentes (MB51 x GMS) com 1o lance a partir de 20/05/2026 e OPs da mesma mangueira que compensam a diferenca (sinal oposto, janela de 60 dias, ate 3 OPs, tolerancia 0,5%).
Rodar dentro da pasta Producao_GMS_x_MB51: python -I top_ops_compensacao.py [inicio AAAA-MM-DD] [fim AAAA-MM-DD] (padrao 2026-05-20 a 2026-09-20). Pula as OPs de ops_tratadas.csv. Ignora OP 0 e OPs com 1o lance a partir de 13/10 (MB51 ainda nao chegou). Candidatas tambem so do periodo."""
import os as _os, pathlib as _pl; _os.chdir(_pl.Path(__file__).resolve().parents[1])  # roda sempre a partir de Producao_GMS_x_MB51
import sys, openpyxl, collections, itertools, datetime as dt
INI=dt.datetime.fromisoformat(sys.argv[1]) if len(sys.argv)>1 else dt.datetime(2026,5,20)  # so OPs (e candidatas) com 1o lance a partir desta data
FIM=dt.datetime.fromisoformat(sys.argv[2]).replace(hour=23,minute=59) if len(sys.argv)>2 else dt.datetime(2026,9,20,23,59)  # ... ate esta data
import csv
TRAT={r['op'] for r in csv.DictReader(open('dados/ops_tratadas.csv',encoding='utf-8'),delimiter=';')}  # OPs ja tratadas: fora do ranking e das candidatas
wb=openpyxl.load_workbook('Conferencia_Lances_por_OP.xlsx',read_only=True)
res=[r for r in wb['Resumo por OP'].iter_rows(min_row=2,values_only=True)]
sem=[r for r in wb['MB51 sem GMS'].iter_rows(min_row=2,values_only=True)]
outra=[r for r in wb['Lance em outra OP'].iter_rows(min_row=2,values_only=True)]
pool=collections.defaultdict(list)
for r in res:
    if r[0]!='0' and r[2] and abs(r[11] or 0)>=0.05 and r[5] and INI<=r[5]<=FIM and r[0] not in TRAT: pool[r[2]].append((r[0],r[11],r[5],r[6],'GMS+SAP'))
for r in sem:
    if r[3] and INI<=r[3]<=FIM and r[0] not in TRAT: pool[r[1]].append((r[0],r[6],r[3],r[4],'só SAP'))
top=[r for r in res if r[0]!='0' and abs(r[11] or 0)>=0.05 and r[5] and INI<=r[5]<=FIM and r[0] not in TRAT]
top.sort(key=lambda r:-abs(r[11])); top=top[:10]
for r in top:
    op,mat,d=r[0],r[2],r[11]
    print(f"\n=== OP {op} {mat} 1o lance {r[5].date()} GMS {r[9]} MB51 {r[10]} dif {d:+.1f}")
    saiu=collections.defaultdict(float); entrou=collections.defaultdict(float)
    for o in outra:
        if o[1]==op: saiu[o[5]]+=o[4]
        if o[5]==op: entrou[o[1]]+=o[4]
    print('  lances da OP que a MB51 lançou em outra OP:',{k:round(v,1) for k,v in saiu.items()})
    print('  lances de outras OPs do GMS que a MB51 lançou nesta:',{k:round(v,1) for k,v in entrou.items()})
    lo,hi=r[5]-dt.timedelta(days=60),(r[6] or r[5])+dt.timedelta(days=60)
    cands=[c for c in pool[mat] if c[0]!=op and c[1]*d<0 and c[2] and lo<=c[2]<=hi]
    tol=max(2,abs(d)*0.005); found=[]
    for k in (1,2,3):
        if len(cands)>60 and k==3: continue
        for comb in itertools.combinations(cands,k):
            e=d+sum(c[1] for c in comb)
            if abs(e)<=tol: found.append((k,abs(e),comb,e))
    found.sort(key=lambda t:(t[0],t[1]))
    print(f'  candidatas na janela ±60 dias, sinal oposto: {len(cands)}')
    for k,_,comb,e in found[:3]:
        print(f"  -> sobra {e:+.1f} | "+' + '.join(f"{c[0]} ({c[1]:+.1f} m, {c[2].date()}, {c[4]})" for c in comb))
    if not found:
        near=sorted(((abs(d+sum(c[1] for c in comb)),comb) for k in (1,2) for comb in itertools.combinations(cands,k)),key=lambda t:t[0])[:1]
        for e,comb in near: print(f"  melhor aproximação: sobra {d+sum(c[1] for c in comb):+.1f} | "+' + '.join(f"{c[0]} ({c[1]:+.1f}, {c[2].date()}, {c[4]})" for c in comb))
