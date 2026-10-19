import openpyxl, pickle, csv, collections
rows=pickle.load(open(r'C:/Users/U445131/AppData/Local/Temp/mb51.pkl','rb'))
wb=openpyxl.load_workbook('Conferencia_Lances_por_OP.xlsx',read_only=True)
ll=[r for r in wb['Linha a linha'].iter_rows(min_row=2,values_only=True)]
def gms(op,lado='GMS'): return [r for r in ll if r[0]==op and r[3]=='GMS' and r[4] in('boa','refugo')]
def sap(op): return [r for r in rows[1:] if str(r[1]).strip()==op and str(r[5]) in('101','102')]
out=[]
def mover(op_gms,op_sap,mat,tipo,acao):
    # lances GMS da op_gms (tipo) cujo valor e data batem com lance SAP em op_sap
    s=[(r[14],r) for r in sap(op_sap)]
    usados=set()
    for g in sorted(gms(op_gms),key=lambda r:r[5]):
        if tipo and g[4]!=tipo: continue
        for i,(q,r) in enumerate(s):
            if i in usados or abs(q-g[6])>0.05: continue
            if g[4]=='refugo' and tipo is None: pass
            usados.add(i)
            out.append([op_gms,op_sap,mat,g[4],g[7],g[5].strftime('%d/%m/%Y %H:%M'),g[6],f"{r[7]}/{r[8]}",acao]); break
mover('29788690','29774579','GH781-4','boa','No GMS, trocar a OP destes lances de 29788690 para 29774579 (o SAP lançou na 29774579)')
mover('29791112','29805524','GH781-8','boa','No GMS, trocar a OP destes lances de 29791112 para 29805524 (o SAP lançou na 29805524; essa OP não existe no GMS)')
mover('29059118','29072012','GH781-4','boa','No GMS, trocar a OP destes lances de 29059118 para 29072012 (boa está na 29072012 no SAP; refugo 7,5 m fica na 29059118)')
mover('29115542','29133080','EC215-06L','boa','OP 29115542 foi cancelada e virou 29133080: lances conferem 1 a 1 (SAP lançou 680 + 151,2 na 29115542 e estornou)')
mover('29118867','29147685','2556-4','boa','No GMS os lances boa de 11-12/06 (806,1 m) estão na 29118867; o SAP lançou na 29147685')
mover('30337761','30421672','GH781-8','boa','No GMS, boa da 30337761 está lançada no SAP na 30421672')
mover('30337761','30406738','GH781-8','refugo','Refugo da 30337761 (0,82+3,2+7,2+0,9=12,12 m) está lançado no SAP como 1 lançamento na 30406738')
mover('29878642','29820550','GH781-8','boa','SAP lançou a boa na 29820550 (GH781-8); ficha 3309 e packing dizem 29878642')
w=csv.writer(open('registros/tratativas_op.csv','w',newline='',encoding='utf-8-sig'),delimiter=';')
w.writerow(['OP no GMS','OP onde o SAP lançou','Mangueira','Tipo','Lance GMS (referência)','Data/hora GMS','Qtd (m)','Doc SAP','Ação'])
w.writerows(out)
tot=collections.defaultdict(float)
for o in out: tot[(o[0],o[1],o[3])]+=o[6]
for k,v in tot.items(): print(k,round(v,1),sum(1 for o in out if (o[0],o[1],o[3])==k))
for o in out:
    if o[0]=='29788690': print(o[4],o[5],o[6],o[7])
