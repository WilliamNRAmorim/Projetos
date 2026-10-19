import openpyxl, pickle, datetime as dt, collections, json
ini=dt.datetime(2026,5,20); fim=dt.datetime(2026,9,20,23,59)
rows=pickle.load(open(r'C:/Users/U445131/AppData/Local/Temp/mb51.pkl','rb'))
wb=openpyxl.load_workbook('Conferencia_Lances_por_OP.xlsx',read_only=True)
ll=list(wb['Linha a linha'].iter_rows(min_row=2,values_only=True))
res={r[0]:r for r in wb['Resumo por OP'].iter_rows(min_row=2,values_only=True)}
semops={r[0] for r in wb['MB51 sem GMS'].iter_rows(min_row=2,values_only=True)}
# lances GMS soltos (boa)
G=[(r[0],r[2],r[5],round(r[6],1),r[7]) for r in ll if r[3]=='GMS' and r[4]=='boa' and r[9][0] in 'SV' and r[5] and ini<=r[5]<=fim+dt.timedelta(days=3)]
# lances SAP soltos: das OPs com GMS (Linha a linha MB51) + OPs so SAP (raw)
S=[(r[0],r[2],r[5],round(r[6],1),r[7]) for r in ll if r[3]=='MB51' and r[4]=='boa' and r[9][0] in 'SV' and r[5] and ini<=r[5]<=fim+dt.timedelta(days=3)]
for x in rows[1:]:
    op=str(x[1]).strip()
    if op in semops and str(x[5])=='101' and x[11]=='M' and x[15] not in('U452021','U445131') and x[9] and ini<=x[9]<=fim+dt.timedelta(days=3):
        S.append((op,x[0],x[9],round(x[14],1),f"{x[7]}/{x[8]}"))
print('GMS soltos',len(G),round(sum(g[3] for g in G),1),'| SAP soltos',len(S),round(sum(s[3] for s in S),1))
idx=collections.defaultdict(list)
for g in G: idx[g[3]].append(g)
usados=set(); pares=[]
for s in sorted(S,key=lambda s:s[2]):
    c=[g for g in idx.get(s[3],[]) if id(g) not in usados and g[0]!=s[0] and abs((g[2].date()-s[2].date()).days)<=3]
    if not c: continue
    c.sort(key=lambda g:(g[1]!=s[1],abs((g[2].date()-s[2].date()).days)))
    g=c[0]; usados.add(id(g)); pares.append((g,s))
agg=collections.defaultdict(lambda:{'n':0,'m':0.0,'mesma':0,'dias':0,'l':[]})
for g,s in pares:
    k=(g[0],s[0]); a=agg[k]; a['n']+=1; a['m']+=g[3]; a['mesma']+= (g[1]==s[1]); a['dias']=max(a['dias'],abs((g[2].date()-s[2].date()).days)); a['l'].append((g[4],g[3],g[2].strftime('%d/%m/%Y %H:%M'),s[4],g[1],s[1]))
alta=[];disc=[]
for k,a in agg.items():
    forte=(a['mesma']==a['n'] and a['dias']<=1 and (a['n']>=2 or a['m']>=40)) or (a['n']>=3 and a['dias']<=1 and a['m']>=100)
    (alta if forte else disc).append((k,a))
print('pares OP->OP',len(agg),'alta',len(alta),round(sum(a['m'] for _,a in alta),1),'lances',sum(a['n'] for _,a in alta),'| discutir',len(disc),round(sum(a['m'] for _,a in disc),1))
alta.sort(key=lambda x:-x[1]['m'])
for k,a in alta: print('ALTA',k[0],'->',k[1],a['n'],round(a['m'],1),'mesma mangueira' if a['mesma']==a['n'] else 'mangueira diferente','dias',a['dias'])
disc.sort(key=lambda x:-x[1]['m'])
for k,a in disc[:30]: print('DISC',k[0],'->',k[1],a['n'],round(a['m'],1),'mesma' if a['mesma']==a['n'] else 'dif','dias',a['dias'],a['l'][0][4],a['l'][0][5])
json.dump({'alta':[[k[0],k[1],a['l']] for k,a in alta],'disc':[[k[0],k[1],a['l']] for k,a in disc]},open('C:/Users/U445131/AppData/Local/Temp/pares5.json','w'))
