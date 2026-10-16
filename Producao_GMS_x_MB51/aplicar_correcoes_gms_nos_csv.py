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
# troca 29048972 -> 29032972 (6 lances) e lances reconstruidos a partir do SAP
for q in ('100,7','55','62,2','99,8','101,6','104,6'):
    for r in ins:
        if r[0]=='29048972' and r[1]==q and r[5][:10]=='28/05/2026': r[0]='29032972'; feitos+=1; break
mat={'29347123':'GH781-4','29102387':'HC139-7','29160712':'GH681-4','29118863':'FC735-06','29145242':'GH681-4','29133128':'FC735-06','28970615':'EC115-08L','29820546':'GH781-8'}
novos=0
for r in csv.reader(open('pendencias_lancar_lote4.csv',encoding='utf-8-sig'),delimiter=';'):
    if r[0] in mat:
        linha=[r[0],r[3],'','','',r[2]+' 12:00','',r[2]+' 12:00',mat[r[0]],'','','','Item','sites/OperationsGuaratingueta/Lists/RegistrosInspeo']
        ins.append(linha); novos+=1
print('lances reconstruidos:',novos)
for r in csv.reader(open('tratativas_lote5_lances.csv',encoding='utf-8-sig'),delimiter=';'):
    if r[0].startswith('OP no GMS'): continue
    for row in ins:
        if row[0]==r[0] and row[1]==r[6] and row[5][:16]==r[5]:
            row[0]=r[1]
            if r[3] and r[3]!=r[2]: row[8]=r[3]
            feitos+=1; break
    else: print('NAO ACHEI lote5',r[:2],r[5],r[6])
for r in csv.reader(open('reconstrucao_lances_lote6.csv',encoding='utf-8-sig'),delimiter=';'):
    if r[0]=='OP': continue
    ins.append([r[0],r[3],'','','',r[2],'',r[2],r[1],'','','','Item','sites/OperationsGuaratingueta/Lists/RegistrosInspeo'])
# lance14161: lance solto de 18,3 m da 29949597 vai para a 29978233 (ficha 3324)
for r in ins:
    if r[0]=='29949597' and r[1]=='18,3': r[0]='29978233'; feitos+=1; break
# duplicados16: originais do GMS movidos para a OP do SAP (os duplicados reconstruidos sairam da lista)
for de,para,q in (('29702384','29102384','40,7'),('30036777','30063848','165,4'),('30036777','30063848','9,2'),('29112843','28880785','39,5'),('29422872','29422873','34,6')):
    for r in ins:
        if r[0]==de and r[1]==q: r[0]=para; feitos+=1; break
for r in ins:   # move144: lance de 14,4 m da 29162764 para a 29162763
    if r[0]=='29162764' and r[1]=='14,4': r[0]='29162763'; feitos+=1; break
print('lances movidos:',feitos,'de',len(mov))
# refugo16b / 29733207 / 29949228 e 29949591 espelhando o SAP
ins=[r for r in ins if not (r[0]=='29733207' and r[1]=='520') and r[0] not in('29949228','29949591')]
for q,h in (('96,6','14:29'),('73,8','14:53'),('8,2','14:45'),('16,1','14:54'),('21,3','15:11'),('51,3','15:12'),('16,4','15:13'),('78,9','15:36'),('13','15:37'),('57,6','15:53'),('29','15:54')):
    ins.append(['29733207',q,'','','','03/08/2026 '+h,'','03/08/2026 '+h,'EC215-08LRL','','','','Item','sites/OperationsGuaratingueta/Lists/RegistrosInspeo'])
for q in ('11,2','12,5','14','15,1','29,1','30,3','30,9','31,2','37,2','43,9','88','162'):
    ins.append(['29949228',q,'','','','22/08/2026 12:00','','22/08/2026 12:00','EC118-06L','','','','Item','sites/OperationsGuaratingueta/Lists/RegistrosInspeo'])
for q in ('10,3','11,1','13,6','26,5','56','75,5','78,2','83,2','156,3','161,8'):
    ins.append(['29949591',q,'','','','24/08/2026 12:00','','24/08/2026 12:00','EC118-06L','','','','Item','sites/OperationsGuaratingueta/Lists/RegistrosInspeo'])
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
for r in saida:   # refugo16b: pares de refugo lancados em outra OP
    if r[0]=='29422610': r[0]='29367063'
    elif r[0]=='30063849': r[0]='30063850'
    elif r[0]=='30120931': r[0]='30120930'
    elif r[0]=='29395275': r[0]='29305868'
gravar('dados/refugo_14out.csv',cab,saida)
# fichas: OP corrigida em 3168 e 3076 nao afeta a conferencia (lista de inspecao)
