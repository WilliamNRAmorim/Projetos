import sys, openpyxl, collections, datetime as dt
wb=openpyxl.load_workbook(sys.argv[1], read_only=True, data_only=True)
ws=wb[[s for s in wb.sheetnames if s.startswith('MB5')][0]]
rows=ws.iter_rows(values_only=True); hdr=next(rows); ix={h:i for i,h in enumerate(hdr)}
A=collections.defaultdict(float); N=collections.Counter(); ex=collections.defaultdict(list)
for r in rows:
    d=r[ix['Posting Date']]
    if not isinstance(d,(dt.date,dt.datetime)): continue
    d=d.date() if isinstance(d,dt.datetime) else d
    if d < dt.date(2026,9,1): continue
    mat=str(r[ix['Material']] or '').strip()
    if not mat or mat.upper().startswith('FM'): continue
    if r[ix['Unit of Entry']]=='KG': continue
    mrp=r[ix['MRP controller']]
    if mrp not in (None,''): continue
    k=(d.strftime('%Y-%m'), r[ix['Unit of Entry']], r[ix['Movement type']], r[ix['Storage location']], 'OP' if r[ix['Order']] else 'sem OP', r[ix['Production Supervisor']])
    A[k]+=r[ix['Qty in unit of entry']] or 0; N[k]+=1
    if len(ex[k])<3: ex[k].append((d.isoformat(), mat, r[ix['Order']], r[ix['Material Description']], r[ix['Qty in unit of entry']], r[ix['Movement Type Text']]))
for k,v in sorted(A.items(), key=lambda x:-abs(x[1]))[:25]:
    print(k, round(v,1), N[k], ex[k][:2])
