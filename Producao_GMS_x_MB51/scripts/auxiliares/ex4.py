import openpyxl, pickle, csv, collections
rows=pickle.load(open(r'C:/Users/U445131/AppData/Local/Temp/mb51.pkl','rb'))
wb=openpyxl.load_workbook('Conferencia_Lances_por_OP.xlsx',read_only=True)
ll=[r for r in wb['Linha a linha'].iter_rows(min_row=2,values_only=True)]
def gms(op): return [r for r in ll if r[0]==op and r[3]=='GMS' and r[4]=='boa' and r[9][0] in 'SV']
def sap(op): return [r for r in rows[1:] if str(r[1]).strip()==op and str(r[5])=='101' and r[11]=='M']
out=[]
def mover(op_gms,op_sap,acao,qs=None):
    s=sap(op_sap); used=set()
    for g in sorted(gms(op_gms),key=lambda r:r[5]):
        if qs and not any(abs(g[6]-q)<=0.05 for q in qs): continue
        for i,r in enumerate(s):
            if i in used or abs(r[14]-g[6])>0.05 or abs(r[9]-g[5].replace(hour=0,minute=0))>__import__('datetime').timedelta(days=8): continue
            used.add(i); out.append([op_gms,op_sap,r[0],g[7],g[5].strftime('%d/%m/%Y %H:%M'),g[6],f"{r[7]}/{r[8]}",acao]); break
mover('29963502','29963530','Trocar no GMS a OP de 29963502 para 29963530')
mover('29963530','29894895','Lance de 26/08 está no GMS na 29963530; o SAP lançou na 29894895',[109.4])
mover('29963530','29894896','Lance de 26/08 está no GMS na 29963530; o SAP lançou na 29894896',[103.1])
mover('29963530','29878655','Lance de 26/08 está no GMS na 29963530; o SAP lançou na 29878655 (EC118-10L: mangueira diferente, conferir)',[98.8])
mover('29259769','29259772','Trocar no GMS a OP de 29259769 para 29259772 (6 lances)')
mover('29259772','29259769','Trocar no GMS a OP de 29259772 para 29259769 (1 lance)')
mover('29259771','29259769','Trocar no GMS a OP de 29259771 para 29259769 (1 lance)')
mover('29788415','29774167','Trocar no GMS a OP de 29788415 para 29774167')
mover('29788415','29774166','Trocar no GMS a OP de 29788415 para 29774166')
mover('29048968','28913388','Trocar no GMS a OP de 29048968 para 28913388')
mover('29048968','28913387','Trocar no GMS a OP de 29048968 para 28913387')
mover('30078414','29788884','Trocar no GMS a OP de 30078414 para 29788884')
w=csv.writer(open('registros/tratativas_lote2.csv','w',newline='',encoding='utf-8-sig'),delimiter=';')
w.writerow(['OP no GMS (hoje)','OP certa (onde o SAP lançou)','Mangueira','Lance GMS (referência)','Data/hora GMS','Qtd (m)','Doc SAP','Ação'])
w.writerows(out)
t=collections.defaultdict(lambda:[0,0.0])
for o in out: t[(o[0],o[1])][0]+=1; t[(o[0],o[1])][1]+=o[5]
for k,v in t.items(): print(k,v[0],round(v[1],1))
for o in out:
    if o[0] in('29259769','29259772','29259771','29963502','29963530','29788415','29048968','30078414'): print(o[0],'->',o[1],o[3],o[4],o[5],o[6])
