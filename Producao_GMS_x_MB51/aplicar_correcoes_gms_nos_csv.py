"""Aplica nos CSVs locais (dados/) as correcoes que foram gravadas no SharePoint em 15/10/2026,
para a conferencia refletir o GMS de hoje sem baixar as listas de novo.
Rodar na pasta Producao_GMS_x_MB51 a partir dos *_antes_tratativas.csv."""
import csv, shutil
def ler(p):
    with open(p,encoding='utf-8-sig',newline='') as f: r=list(csv.reader(f,delimiter=';'))
    return r[0],r[1:]
def gravar(p,cab,rows):
    with open(p,'w',encoding='utf-8-sig',newline='') as f: w=csv.writer(f,delimiter=';'); w.writerow(cab); w.writerows(rows)
cab,ins=ler('dados/inspecao_14out_antes_tratativas.csv')
mov=[]
for r in csv.reader(open('correcoes_gms_2026-10-15.csv',encoding='utf-8-sig'),delimiter=';'):
    if r[0].startswith('ID'): continue
    mov.append((r[1],r[2],r[3].replace('.',','),r[4][:16],None))
mov.append(('29963530','29878655','98,8','26/08/2026 17:45','EC118-10L'))
for q,h in (('143,5','06:59'),('140,3','07:07'),('63,9','07:11'),('38,1','07:32'),('188,2','07:37')): mov.append(('29878642','29820550',q,'27/08/2026 '+h,None))
for r in csv.reader(open('tratativas_lote3_lances.csv',encoding='utf-8-sig'),delimiter=';'):
    if r[0].startswith('OP no GMS'): continue
    mov.append((r[0],r[1],r[5],r[4],None))
feitos=0
for de,para,q,dh,mang in mov:
    for r in ins:
        if r[0]==de and r[1]==q and r[5][:16]==dh:
            r[0]=para; feitos+=1
            if mang: r[8]=mang
            break
    else: print('NAO ACHEI',de,para,q,dh)
print('lances movidos:',feitos,'de',len(mov))
gravar('dados/inspecao_14out.csv',cab,ins)
cab,ref=ler('dados/refugo_14out_antes_tratativas.csv')
saida=[]
for r in ref:
    # refugo 29963502 -> 29963527 (3 linhas de 25/08)
    if r[0]=='29963502' and r[3][:10]=='25/08/2026': r[0]='29963527'
    # excluidos: 29115542 1,0 O - Pontas; 29733210 1,2 O - Pontas e 1,1 A - Quebra
    if (r[0]=='29115542' and r[1]=='O - Pontas' and r[2]=='1') or (r[0]=='29733210' and r[3][:10]=='03/08/2026' and r[2] in('1,2','1,1')) or (r[0]=='27002870' and r[1].startswith('D - Marca') and r[2]=='1'): continue
    saida.append(r)
print('refugos:',len(ref),'->',len(saida))
gravar('dados/refugo_14out.csv',cab,saida)
# fichas: OP corrigida em 3168 e 3076 nao afeta a conferencia (lista de inspecao)
