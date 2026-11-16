import sys, openpyxl, collections, datetime as dt, json
wb=openpyxl.load_workbook(sys.argv[1], read_only=True, data_only=True)
ws=wb[[s for s in wb.sheetnames if s.startswith('MB5')][0]]
rows=ws.iter_rows(values_only=True); hdr=next(rows)
ix={h:i for i,h in enumerate(hdr)}
M=collections.defaultdict(float); D=collections.defaultdict(float); X=collections.defaultdict(float); dias=collections.defaultdict(set)
mapa={'AIH':'Mangueira','Z35':'Montagem','AWE':'Montagem','AO0':'Fittings'}
for r in rows:
    mat=r[ix['Material']]; d=r[ix['Posting Date']]; q=r[ix['Qty in unit of entry']] or 0; u=r[ix['Unit of Entry']]; mrp=r[ix['MRP controller']]
    if not isinstance(d,(dt.date,dt.datetime)): continue
    d=d.date() if isinstance(d,dt.datetime) else d
    if mat is None or str(mat).strip()=='' or str(mat).strip().upper().startswith('FM'): continue
    ym=d.strftime('%Y-%m')
    if u=='KG': X[(ym,'KG')]+=q; continue
    p=mapa.get((mrp or '').strip())
    if p is None: X[(ym,'MRP:'+str(mrp))]+=q; continue
    M[(ym,p)]+=q; D[(d.isoformat(),p)]+=q; dias[ym].add(d)
out={'mes':{f'{k[0]}|{k[1]}':round(v,2) for k,v in sorted(M.items())},
     'dias':{k:len(v) for k,v in sorted(dias.items())},
     'ultimo':{k:max(v).isoformat() for k,v in sorted(dias.items())},
     'excluido':{f'{k[0]}|{k[1]}':round(v,2) for k,v in sorted(X.items()) if k[0]>='2026-08'},
     'dia_out_nov':{f'{k[0]}|{k[1]}':round(v,2) for k,v in sorted(D.items()) if k[0]>='2026-10-01'}}
json.dump(out,open('valida_local.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
for k in ('mes','dias','ultimo','excluido'):
    print('==',k); print(json.dumps(out[k],ensure_ascii=False)[:2500])
