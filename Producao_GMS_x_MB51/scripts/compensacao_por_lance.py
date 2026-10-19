"""Top N OPs mais divergentes (MB51 x GMS) no periodo e, para cada uma, as OPs da mesma mangueira que ficaram com os lances trocados.
Prova por lance: lance 'so no GMS' (ou 'so na MB51') com a mesma metragem (+-0,05 m), na mesma mangueira, em outra OP, em +-7 dias.
Rodar na pasta Producao_GMS_x_MB51: python -I compensacao_por_lance.py [N] [inicio] [fim] [saida.csv]   (padrao 10, 2026-05-20 a 2026-09-20). Pula ops_tratadas.csv.
Le o mb51 (5).xlsx (cerca de 1 minuto)."""
import os as _os, pathlib as _pl; _os.chdir(_pl.Path(__file__).resolve().parents[1])  # roda sempre a partir de Producao_GMS_x_MB51
import sys, csv, collections, datetime as dt, openpyxl
N=int(sys.argv[1]) if len(sys.argv)>1 else 10
INI=dt.datetime.fromisoformat(sys.argv[2]) if len(sys.argv)>2 else dt.datetime(2026,5,20)
FIM=(dt.datetime.fromisoformat(sys.argv[3]) if len(sys.argv)>3 else dt.datetime(2026,9,20)).replace(hour=23,minute=59)
TRAT={r['op'] for r in csv.DictReader(open('dados/ops_tratadas.csv',encoding='utf-8'),delimiter=';')}
wb=openpyxl.load_workbook('Conferencia_Lances_por_OP.xlsx',read_only=True)
res=list(wb['Resumo por OP'].iter_rows(min_row=2,values_only=True))
ll=list(wb['Linha a linha'].iter_rows(min_row=2,values_only=True))
mb=collections.defaultdict(list)   # material -> (op, data, qtd, doc, tipo)
for r in openpyxl.load_workbook('dados/mb51 (5).xlsx',read_only=True,data_only=True).worksheets[0].iter_rows(min_row=2,values_only=True):
    if r[11]!='M' or str(r[5])!='101' or not r[1] or r[14] is None: continue
    mb[str(r[0])].append((str(r[1]).strip(),r[9],float(r[14]),f"{r[7]}/{r[8]}"))
gm=collections.defaultdict(list)   # material -> lances GMS 'so no GMS'
solo=collections.defaultdict(list)
for r in ll:
    if r[9] and r[9].startswith('S') and r[3]=='GMS': gm[r[2]].append(r)
    if r[9] and r[9].startswith('S') and r[3]=='MB51': solo[(r[0],r[2])].append(r)
top=[r for r in res if r[0]!='0' and abs(r[11] or 0)>=0.05 and r[5] and INI<=r[5]<=FIM and r[0] not in TRAT]
top.sort(key=lambda r:-abs(r[11])); top=top[:N]
D=dt.timedelta(days=7)
SAIDA=[['OP divergente','OP candidata','Mangueira','Sentido','Referência do lance no GMS','Qtd (m)','Doc SAP / referência'],]
for r in top:
    op,mat,d=r[0],r[2],r[11]
    print(f"\n=== OP {op} | {mat} | 1o lance GMS {r[5]:%d/%m/%Y} | GMS {r[9]:,.1f} | MB51 {r[10]:,.1f} | dif {d:+,.1f} m")
    ach=collections.defaultdict(list)
    if d<0:   # GMS a mais: lances 'so no GMS' desta OP procurados na MB51 em outra OP
        exc=[x for x in gm[mat] if x[0]==op and x[4]=='boa']
        for x in exc:
            for (o,dd,q,doc) in mb[mat]:
                if o!=op and abs(q-x[6])<=0.05 and abs(dd-x[5].replace(hour=0,minute=0))<=D: ach[o].append((x[7],x[6],doc)); break
    else:     # SAP a mais: lances 'so na MB51' desta OP procurados no GMS em outra OP
        exc=[x for x in solo[(op,mat)] if x[4]=='boa']
        for x in exc:
            for y in gm[mat]:
                if y[0]!=op and y[4]=='boa' and abs(y[6]-x[6])<=0.05 and abs(y[5].replace(hour=0,minute=0)-x[5])<=D: ach[y[0]].append((y[7],y[6],x[7])); break
    tot=sum(x[6] for x in exc)
    for o,l in ach.items():
        for t in l: SAIDA.append([op,o,mat,'GMS a mais (SAP lançou na candidata)' if d<0 else 'SAP a mais (GMS tem na candidata)',t[0],t[1],t[2]])
    print(f"  lances soltos (boa): {len(exc)} = {tot:,.1f} m")
    if not ach: print("  sem OP candidata por lance"); continue
    for o,l in sorted(ach.items(),key=lambda kv:-sum(t[1] for t in kv[1]))[:3]:
        print(f"  -> OP {o}: {len(l)} lances = {sum(t[1] for t in l):,.1f} m de {tot:,.1f} m ({'GMS a mais; SAP lancou la' if d<0 else 'SAP a mais; GMS tem la'})")

if len(sys.argv)>4:
    csv.writer(open(sys.argv[4],'w',newline='',encoding='utf-8-sig'),delimiter=';').writerows(SAIDA)
