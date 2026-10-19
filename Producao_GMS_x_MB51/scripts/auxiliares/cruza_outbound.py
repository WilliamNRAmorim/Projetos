import openpyxl, re, datetime as dt, collections, pickle, csv
ob=openpyxl.load_workbook('C:/Users/U445131/Downloads/New Microsoft Excel Worksheet.xlsx',read_only=True,data_only=True).worksheets[0]
OB=[r for r in ob.iter_rows(min_row=2,values_only=True) if r[0]]
idx=collections.defaultdict(list)
for r in OB:
    d=r[12].date() if isinstance(r[12],dt.datetime) else None
    idx[(r[2],round(float(r[3]),2))].append((r[0],d,r[13],r[6],r[10]))
ws=openpyxl.load_workbook('resultados/Divergencias_positivas_completo.xlsx')['Refugo']
mb=pickle.load(open(r'C:/Users/U445131/AppData/Local/Temp/mb51.pkl','rb'))
docs={}
for x in mb[1:]:
    if x[9]: docs[f"{x[7]}/{x[8]}"]=(x[9].date(),x[15],round(x[14],2))
linhas=[];usados=set()
for r in ws.iter_rows(min_row=2,values_only=True):
    if not r[0] or not r[5] or not str(r[5]).startswith('Refugo duplicado'): continue
    op,mat=r[0],r[1]
    for m in re.finditer(r'(\d+/\d+) \(([\d,]+) m, (\d\d/\d\d)\)',r[6] or ''):
        doc,q=m.group(1),float(m.group(2).replace(',','.'))
        info=docs.get(doc); dd=info[0] if info else None
        cand=[o for o in idx.get((mat,round(q,2)),[]) if dd and o[1] and 0<=(o[1]-dd).days<=5 and o[0] not in usados]
        cand.sort(key=lambda o:abs((o[1]-dd).days))
        out=cand[0] if cand else None
        if out: usados.add(out[0])
        linhas.append((op,mat,doc,q,dd,info[1] if info else '',out[0] if out else '',out[1] if out else '',out[3] if out else '',out[4] if out else ''))
tot=sum(l[3] for l in linhas); ach=[l for l in linhas if l[6]]
print('Outbounds',len(OB),'| todos Not Started:',all(o[6]=='Not Started' and o[10]=='Not Started' for o in OB))
print('documentos duplicados:',len(linhas),round(tot,1),'m | com outbound correspondente:',len(ach),round(sum(l[3] for l in ach),1),'m | sem:',len(linhas)-len(ach),round(tot-sum(l[3] for l in ach),1),'m')
w=csv.writer(open('registros/refugo_duplicado_x_outbound.csv','w',newline='',encoding='utf-8-sig'),delimiter=';')
w.writerow(['OP','Mangueira','Doc SAP duplicado','Qtd (m)','Data do lançamento','Usuário','Outbound (delivery)','Criado em','Picking','Goods issue'])
for l in linhas: w.writerow([l[0],l[1],l[2],str(l[3]).replace('.',','),l[4],l[5],l[6],l[7],l[8],l[9]])
for l in linhas[:6]: print(l)
print('outbounds sem par (qualquer):',len(OB)-len(usados))
