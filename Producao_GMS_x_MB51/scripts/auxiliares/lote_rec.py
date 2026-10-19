import openpyxl, pickle, datetime as dt, collections, json, sys
ops=sys.argv[1].split(',')
bd=openpyxl.load_workbook('../GMS/Sharepoint Data GMS/BD Packing List.xlsx',read_only=True,data_only=True)['Data Base']
sl=collections.defaultdict(list)
for r in bd.iter_rows(min_row=3,values_only=True):
    if isinstance(r[5],dt.datetime) and not r[7]: sl[(r[1],round(float(r[3]),1))].append((r[0],r[2],r[5]))
rows=pickle.load(open(r'C:/Users/U445131/AppData/Local/Temp/mb51.pkl','rb'))
wb=openpyxl.load_workbook('Conferencia_Lances_por_OP.xlsx',read_only=True)
gm=collections.defaultdict(list)
for r in wb['Linha a linha'].iter_rows(min_row=2,values_only=True):
    if r[3]=='GMS' and r[4]=='boa': gm[r[0]].append(round(r[6],1))
out={}
for op in ops:
    L=sorted([(x[9],round(x[14],1),x[0],x[7],str(x[5])) for x in rows[1:] if str(x[1]).strip()==op and str(x[5]) in('101','102') and x[11]=='M' and x[15] not in('U452021','U445131')],key=lambda t:(t[0],t[3]))
    base=[l for l in L if l[4]=='101']
    for e in [l for l in L if l[4]=='102']:
        for b in base:
            if abs(b[1]+e[1])<0.01: base.remove(b); break
    ja=list(gm.get(op,[])); lan=[]
    for d,q,m,doc,t in base:
        if q in ja: ja.remove(q); continue
        c=[s for s in sl.get((m,q),[]) if abs((s[2].date()-d.date()).days)<=1]
        ts=c[0][2] if c else dt.datetime(d.year,d.month,d.day,12,0)
        lan.append([(ts+dt.timedelta(hours=3)).strftime('%Y-%m-%dT%H:%M:00Z'),q])
    seen=collections.Counter()
    for l in lan:
        i=seen[l[0]]; seen[l[0]]+=1
        if i: l[0]=(dt.datetime.strptime(l[0],'%Y-%m-%dT%H:%M:00Z')+dt.timedelta(minutes=i)).strftime('%Y-%m-%dT%H:%M:00Z')
    out[op]={'m':L[0][2],'d':L[0][0].strftime('%Y-%m-%d'),'tot':round(sum(b[1] for b in base),1),'S':lan,'ja':len(gm.get(op,[]))}
    print(op,out[op]['m'],out[op]['d'],'SAP liq',out[op]['tot'],'a criar',len(lan),round(sum(l[1] for l in lan),1),'GMS ja tem',out[op]['ja'])
json.dump(out,open('C:/Users/U445131/AppData/Local/Temp/rec_next.json','w'))
print(json.dumps(out,separators=(',',':')))
