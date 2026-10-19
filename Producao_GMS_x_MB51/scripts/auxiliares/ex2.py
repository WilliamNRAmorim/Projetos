import openpyxl, pickle, sys, collections
rows=pickle.load(open(r'C:/Users/U445131/AppData/Local/Temp/mb51.pkl','rb'))
wb=openpyxl.load_workbook('Conferencia_Lances_por_OP.xlsx',read_only=True)
ll=list(wb['Linha a linha'].iter_rows(min_row=2,values_only=True))
def mb(op):
    return [r for r in rows[1:] if str(r[1]).strip()==op and str(r[5]) in('101','102')]
def show(op):
    print(f'\n##### OP {op}')
    print('MB51:')
    for r in sorted(mb(op),key=lambda r:(r[9],r[7])): print(' ',r[0],r[5],r[9].date(),r[14],r[11],r[15],r[7],r[8],'|',r[2][:30])
    print('GMS:')
    for r in ll:
        if r[0]==op: print(' ',r[2],r[4],str(r[5])[:16],r[6],r[8],'|',r[9][:22],'|',r[13] or '')
for op in sys.argv[1:]: show(op)
