import collections, datetime as dt, openpyxl, pickle, csv
from openpyxl.styles import Font, PatternFill, Alignment
ini=dt.datetime(2026,5,20); fim=dt.datetime(2026,9,20,23,59)
rows=pickle.load(open(r'C:/Users/U445131/AppData/Local/Temp/mb51.pkl','rb'))
refl=collections.defaultdict(list)
for x in rows[1:]:
    if x[15] in('U452021','U445131') and str(x[5]) in('101','102') and x[11]=='M': refl[str(x[1]).strip()].append((x[9].date(),round(x[14],2),f"{x[7]}/{x[8]}",str(x[5])))
refgms=collections.defaultdict(float)
for r in csv.reader(open('dados/refugo_14out.csv',encoding='utf-8-sig'),delimiter=';'):
    if r[0].startswith('OP'): continue
    try: refgms[r[0]]+=float(r[2].replace(',','.'))
    except: pass
bd=openpyxl.load_workbook('../GMS/Sharepoint Data GMS/BD Packing List.xlsx',read_only=True,data_only=True)['Data Base']
sl=collections.defaultdict(list)
for r in bd.iter_rows(min_row=3,values_only=True):
    if isinstance(r[5],dt.datetime) and not r[7]: sl[(r[1],round(float(r[3]),1))].append((r[0],r[2],r[5]))
wb=openpyxl.load_workbook('Conferencia_Lances_por_OP.xlsx',read_only=True)
res=[r for r in wb['Resumo por OP'].iter_rows(min_row=2,values_only=True) if r[5] and ini<=r[5]<=fim and r[0]!='0']
sem=[r for r in wb['MB51 sem GMS'].iter_rows(min_row=2,values_only=True) if r[3] and ini<=r[3]<=fim]
ll=list(wb['Linha a linha'].iter_rows(min_row=2,values_only=True))
gmb=collections.defaultdict(list); sap_sv=collections.defaultdict(list); gms_sv=collections.defaultdict(list)
for r in ll:
    if r[4]=='boa':
        if r[3]=='GMS': gmb[r[0]].append(round(r[6],1))
        if r[9][0] in 'SV': (sap_sv if r[3]=='MB51' else gms_sv)[r[0]].append((round(r[6],1),r[9][0]))
boa=[];refu=[]
for r in res:
    d=(r[10] or 0)-(r[9] or 0)
    if abs(d)<0.05: continue
    L=refl.get(r[0],[]); sref=sum(q for _,q,_,_ in L); ref=sref-refgms.get(r[0],0); b=d-ref
    if ref>0.05:
        cnt=collections.defaultdict(list)
        for d_,q,doc,t in L:
            if t=='101': cnt[q].append((d_,doc))
        sobra=[];exp=0
        for q,v in cnt.items():
            if len(v)>1 and q>=0.5:
                for d_,doc in sorted(v)[1:]: sobra.append(f"{doc} ({str(q).replace('.',',')} m, {d_:%d/%m})"); exp+=q
        tipo='Refugo duplicado no SAP' if sobra and abs(exp-ref)<0.3 else 'Refugo SAP maior que GMS (sem repetição)'
        refu.append([r[0],r[2],round(sref,2),round(refgms.get(r[0],0),2),round(ref,2),tipo,'; '.join(sobra)])
    if b>0.5:
        gv=[x for x in gms_sv.get(r[0],[]) if x[1]=='V']; sv=[x for x in sap_sv.get(r[0],[]) if x[1]=='V']
        S=[(x[9],round(x[14],1),x[0]) for x in rows[1:] if str(x[1]).strip()==r[0] and str(x[5])=='101' and x[11]=='M' and x[15] not in('U452021','U445131')]
        nb=sum(1 for d_,q,m in S if [s for s in sl.get((m,q),[]) if abs((s[2].date()-d_.date()).days)<=1])
        if r[0] in ('29788884','30078414'): mot='SAP lançou 51 m nas duas OPs (duplicidade provável no SAP)'
        elif gv and sv: mot='Lance com valor diferente entre GMS e SAP (décimos de metro ou soma)'
        elif nb>=len(S)*0.8 and S: mot='Falta lance no GMS, BD Packing List cobre'
        elif S: mot='Falta lance no GMS, BD Packing List não cobre'
        else: mot='A conferir'
        boa.append([r[0],r[2],round(b,1),mot,'; '.join(f"{q} m" for q,_ in sap_sv.get(r[0],[]))[:80]])
for r in sem:
    if r[6]>0.5: boa.append([r[0],r[1],round(r[6],1),'OP só no SAP, sem lances no GMS',''])
boa.sort(key=lambda x:-x[2]); refu.sort(key=lambda x:-x[4])
w=openpyxl.Workbook(); ws=w.active; ws.title='Resumo'
tb=round(sum(x[2] for x in boa),1); td=round(sum(x[4] for x in refu if x[5].startswith('Refugo dup')),1); to=round(sum(x[4] for x in refu if not x[5].startswith('Refugo dup')),1)
ws.append(['Divergências positivas (SAP maior que GMS), 20/05 a 20/09/2026','']); ws.append(['Tipo','Metros'])
ws.append(['Boa',tb]); ws.append(['Refugo duplicado no SAP',td]); ws.append(['Refugo SAP maior que GMS, sem repetição',to]); ws.append(['Total positivo',f'=SUM(B3:B5)'])
mots=collections.defaultdict(float)
for x in boa: mots[x[3]]+=x[2]
ws.append([]); ws.append(['Boa por motivo','Metros'])
for k,v in sorted(mots.items(),key=lambda t:-t[1]): ws.append([k,round(v,1)])
for c in ws[2]: c.font=Font(bold=True,color='FFFFFF'); c.fill=PatternFill('solid',fgColor='C8102E')
ws['A1'].font=Font(bold=True); ws.column_dimensions['A'].width=58; ws.column_dimensions['B'].width=14
w2=w.create_sheet('Boa'); w2.append(['OP','Mangueira','Boa a mais no SAP (m)','Motivo','Lances em conflito (SAP)'])
for x in boa: w2.append(x)
w3=w.create_sheet('Refugo'); w3.append(['OP','Mangueira','Refugo no SAP (m)','Refugo no GMS (m)','Diferença (m)','Tipo','Docs repetidos (os de sobra)'])
for x in refu: w3.append(x)
for s in (w2,w3):
    for c in s[1]: c.font=Font(bold=True,color='FFFFFF'); c.fill=PatternFill('solid',fgColor='C8102E'); c.alignment=Alignment(wrap_text=True)
    s.freeze_panes='A2'
for col,wd in zip('ABCDEFG',[12,16,18,52,18,38,70]): w2.column_dimensions[col].width=wd; w3.column_dimensions[col].width=wd
w.save('resultados/Divergencias_positivas_completo.xlsx')
a=sum(abs(r[11]) for r in res if abs(r[11] or 0)>=0.05); b=sum(r[6] for r in sem)
pos=sum(r[11] for r in res if (r[11] or 0)>=0.05)+b; neg=sum(r[11] for r in res if (r[11] or 0)<=-0.05)
print('BRUTO',round(a+b),'pos',round(pos),'neg',round(neg),'so SAP',len(sem),round(b))
print('Boa',tb,len(boa),'| Refugo dup',td,sum(1 for x in refu if x[5].startswith('Refugo dup')),'| Refugo outros',to,sum(1 for x in refu if not x[5].startswith('Refugo dup')))
for k,v in sorted(mots.items(),key=lambda t:-t[1]): print(' ',k,round(v,1),sum(1 for x in boa if x[3]==k))
for x in boa[:12]: print(x)
