import sys, openpyxl, collections, datetime as dt
wb=openpyxl.load_workbook(sys.argv[1], read_only=True, data_only=True)
ws=wb[[s for s in wb.sheetnames if s.startswith('MB5')][0]]
rows=ws.iter_rows(values_only=True); hdr=next(rows); ix={h:i for i,h in enumerate(hdr)}
T=collections.defaultdict(lambda: collections.Counter()); Q=collections.defaultdict(float)
mat2mrp=collections.defaultdict(set); semmrp_mat=set()
for r in rows:
    d=r[ix['Posting Date']]
    if not isinstance(d,(dt.date,dt.datetime)): continue
    mat=str(r[ix['Material']] or '').strip()
    if not mat or mat.upper().startswith('FM'): continue
    u=r[ix['Unit of Entry']]
    if u=='KG': continue
    mrp=(r[ix['MRP controller']] or '').strip(); sl=r[ix['Storage location']]; op='OP' if r[ix['Order']] else 'semOP'
    key=(sl,u,op)
    T[key][mrp or '-']+=1
    if mrp: mat2mrp[mat].add(mrp)
    elif op=='OP': semmrp_mat.add(mat)
print('== depósito, unidade, OP -> MRP (contagem de linhas)')
for k,c in sorted(T.items(), key=lambda x:-sum(x[1].values()))[:20]: print(k, dict(c.most_common(6)))
amb=[m for m,s in mat2mrp.items() if len(s)>1]
print('materiais com mais de um MRP:',len(amb), amb[:10])
cob=[m for m in semmrp_mat if m in mat2mrp]
print('materiais com OP sem MRP:',len(semmrp_mat),' cobertos pelo mapa material->MRP:',len(cob))
