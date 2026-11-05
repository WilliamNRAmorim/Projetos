import openpyxl,json,warnings,datetime as dt,collections
warnings.filterwarnings('ignore')
src='C:/Users/U445131/Downloads/Projetos/Dados_Historicos/HoraHora_pre_GMS/'
out='C:/Users/U445131/Downloads/Projetos/GMS/Analises/Historico_HoraHora/'
def num(v):
    if isinstance(v,bool) or v is None or v=='': return None
    if isinstance(v,(int,float)): return round(float(v),2)
    return None
def txt(v):
    if v is None: return None
    s=str(v).strip()
    return s or None
rows=[];n=0
for nome,arq,orig in (('Dados','Banco_de_Dados_Hora_Hora_2023-08_a_2025-09.xlsx','Banco geral'),('Dados','Banco_de_Dados_Espiral_2024-03_a_2026-01.xlsx','Espiral')):
    ws=openpyxl.load_workbook(src+arq,read_only=True,data_only=True)[nome]
    for r in ws.iter_rows(min_row=2,max_col=16,values_only=True):
        r=list(r)+[None]*(16-len(r))
        if all(v is None for v in r[:14]): continue
        alerta=None
        if hasattr(r[0],'year'):
            d=r[0].strftime('%Y-%m-%d');turno,cel=txt(r[1]),txt(r[2])
        else:
            d=None;turno,cel=txt(r[0]),txt(r[1]);alerta='Sem data: linha desalinhada na planilha original (Data e Celula deslocadas)'
        if cel and cel.upper().replace('-','').replace(' ','') in ('TH7','TH07'): cel='TH07'
        if turno and turno not in ('1º','2º','3º') and turno.upper().startswith('TH'):
            cel='TH07';turno=None;alerta=(alerta+'; ' if alerta else '')+'Turno nao informado na planilha original (so a celula TH-07)'
        com=' | '.join(x for x in (txt(r[13]),txt(r[14]) if orig=='Espiral' else None,txt(r[15]) if orig=='Espiral' else None) if x) or None
        n+=1
        rows.append([n,d,turno,cel,txt(r[3]),txt(r[4]),num(r[5]),num(r[6]),num(r[7]),num(r[8]),num(r[9]),num(r[10]),txt(r[11]),txt(r[12]),com,orig,alerta])
print(len(rows),collections.Counter(r[15] for r in rows),sum(1 for r in rows if r[16]))
TAM=2000;man=[]
for i in range(0,len(rows),TAM):
    ch=rows[i:i+TAM];k=i//TAM+1
    open(out+f'dados/hh_{k:02d}.js','w',encoding='utf-8',newline='\n').write('window.__R='+json.dumps(ch,ensure_ascii=False,separators=(',',':'))+';\n')
    man.append(dict(arquivo=f'hh_{k:02d}.js',titulo_ini=ch[0][0],titulo_fim=ch[-1][0],linhas=len(ch),real=round(sum(r[8] or 0 for r in ch),2),meta=round(sum(r[6] or 0 for r in ch),2),parado=round(sum(r[11] or 0 for r in ch),2),de=min((r[1] for r in ch if r[1]),default=None),ate=max((r[1] for r in ch if r[1]),default=None)))
tot=dict(linhas=len(rows),real=round(sum(r[8] or 0 for r in rows),2),meta=round(sum(r[6] or 0 for r in rows),2),parado=round(sum(r[11] or 0 for r in rows),2))
json.dump(dict(total=tot,arquivos=man),open(out+'hh_manifest.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(tot,len(man))
import os;print(sum(os.path.getsize(out+'dados/'+f) for f in os.listdir(out+'dados')))
