import sys, openpyxl, collections, datetime as dt, re
wb=openpyxl.load_workbook(sys.argv[1], read_only=True, data_only=True)
ws=wb[[s for s in wb.sheetnames if s.startswith('MB5')][0]]
rows=ws.iter_rows(values_only=True); hdr=next(rows); ix={h:i for i,h in enumerate(hdr)}
C=collections.defaultdict(collections.Counter); EX=collections.defaultdict(set); U=collections.Counter(); UQ=collections.defaultdict(float)
for r in rows:
    if not r[ix['Order']] or r[ix['Unit of Entry']]!='PC' or r[ix['Storage location']] not in ('GRT4','KAN','ASSY'): continue
    mat=str(r[ix['Material']] or ''); desc=str(r[ix['Material Description']] or '')
    pref=' '.join(desc.split()[:2]).rstrip(',')
    mrp=(r[ix['MRP controller']] or '').strip() or '-'
    C[pref][mrp]+=1
    if len(EX[(pref,mrp)])<3: EX[(pref,mrp)].add(mat+' / '+desc[:40])
    d=r[ix['Posting Date']]
    if mrp=='-' and isinstance(d,(dt.date,dt.datetime)) and d.year==2026 and d.month in (9,10):
        U[pref]+=1; UQ[pref]+= r[ix['Qty in unit of entry']] or 0
for k,c in sorted(C.items(), key=lambda x:-sum(x[1].values()))[:15]: print(repr(k), dict(c), [list(EX[(k,m)])[:2] for m in c if m!='-'][:2])
print('== sem MRP set/out por prefixo:', {k:(U[k],round(UQ[k])) for k in U})
