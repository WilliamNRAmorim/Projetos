"""Simula a classificação em cadeia do produto (MEL-273) sobre a tabela mb51_coois da Máscara.
Cadeia: 1) MRP da COOIS pela OP; 2) MRP do material já visto em OP com MRP; 3) regra depósito/unidade/descrição.
Acurácia da regra (3) medida nas linhas que têm MRP conhecido (como se não tivessem)."""
import sys, openpyxl, collections, datetime as dt, re
MAPA={'AIH':'Mangueira','Z35':'Montagem','AWE':'Montagem','AO0':'Fittings'}
FIT=re.compile(r'^(HOSE FTG|CON PRENS|CON MONT|CON ESPECIAL|FTNG|FTG|HOSE NIPPLE|NIPLE|NIPPLE|TUBO)', re.I)
def regra(sl,u,op,desc):
    if not op: return None
    if sl=='GRT4' and u=='M': return 'Mangueira'
    if sl=='KAN' and u=='PC': return 'Montagem'
    if sl in ('GRT4','ASSY') and u=='PC': return 'Fittings' if FIT.match(desc or '') else 'Montagem'
    return None
wb=openpyxl.load_workbook(sys.argv[1], read_only=True, data_only=True)
ws=wb[[s for s in wb.sheetnames if s.startswith('MB5')][0]]
rows=list(ws.iter_rows(values_only=True)); hdr=rows[0]; ix={h:i for i,h in enumerate(hdr)}; rows=rows[1:]
mat2=collections.defaultdict(collections.Counter)
for r in rows:
    m=(r[ix['MRP controller']] or '').strip()
    if m in MAPA: mat2[str(r[ix['Material']]).strip()][MAPA[m]]+=1
tot=collections.defaultdict(float); orig=collections.Counter(); acc=collections.Counter(); err=collections.Counter()
for r in rows:
    d=r[ix['Posting Date']]
    if not isinstance(d,(dt.date,dt.datetime)): continue
    d=d.date() if isinstance(d,dt.datetime) else d
    mat=str(r[ix['Material']] or '').strip(); u=r[ix['Unit of Entry']]
    if not mat or mat.upper().startswith('FM') or u=='KG': continue
    sl=r[ix['Storage location']]; op=r[ix['Order']]; desc=str(r[ix['Material Description']] or ''); q=r[ix['Qty in unit of entry']] or 0
    m=(r[ix['MRP controller']] or '').strip()
    rg=regra(sl,u,op,desc)
    if m in MAPA:
        p=MAPA[m]; o='1 COOIS'
        if rg is not None: acc['regra ok' if rg==p else 'regra erra']+=1
        if rg is not None and rg!=p: err[(p,rg,desc[:30])]+=1
    elif mat in mat2: p=mat2[mat].most_common(1)[0][0]; o='2 material'
    elif rg: p=rg; o='3 regra'
    else: continue
    ym=d.strftime('%Y-%m'); tot[(ym,p)]+=q; orig[(ym,o)]+=1
print('acurácia da regra nas linhas com MRP:', dict(acc))
print('erros mais comuns:', err.most_common(8))
for ym in ('2026-08','2026-09','2026-10','2026-11'):
    print(ym, {p:round(tot[(ym,p)],1) for p in ('Mangueira','Montagem','Fittings')}, {o:orig[(ym,o)] for o in ('1 COOIS','2 material','3 regra')})
