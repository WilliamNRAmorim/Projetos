import openpyxl, pickle, csv
rows=pickle.load(open(r'C:/Users/U445131/AppData/Local/Temp/mb51.pkl','rb'))
wb=openpyxl.load_workbook('Conferencia_Lances_por_OP.xlsx',read_only=True)
ll=[r for r in wb['Linha a linha'].iter_rows(min_row=2,values_only=True)]
out=[['OP','Mangueira','Onde falta lançar','Tipo','Data','Qtd (m)','Doc SAP / referência GMS','Observação']]
def sap(op): return [r for r in rows[1:] if str(r[1]).strip()==op and str(r[5])=='101' and r[11]=='M']
for op,dsde in (('29733210','2026-08-03'),('30092889','2026-09-24'),('29260119','2026-06-27')):
    for r in sorted(sap(op),key=lambda r:(r[9],r[7])):
        if r[9].strftime('%Y-%m-%d')>=dsde and r[15] not in('U452021','U445131'):
            out.append([op,r[0],'GMS (lançar a produção boa)','boa',r[9].strftime('%d/%m/%Y'),r[14],f"{r[7]}/{r[8]}",f"usuário SAP {r[15]}"])
for g in ll:
    if g[0]=='29733210' and g[3]=='GMS' and g[4]=='refugo':
        out.append(['29733210','EC215-08L','SAP (lançar o refugo; nem existe na OP do SAP)','refugo',g[5].strftime('%d/%m/%Y %H:%M'),g[6],g[7],g[8]])
w=csv.writer(open('registros/pendencias_lancar.csv','w',newline='',encoding='utf-8-sig'),delimiter=';'); w.writerows(out)
for o in out[1:]: print(o)
