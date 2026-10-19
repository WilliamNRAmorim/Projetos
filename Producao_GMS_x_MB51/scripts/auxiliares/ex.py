import openpyxl, pickle, collections
ws=openpyxl.load_workbook('dados/mb51 (5).xlsx',read_only=True,data_only=True).worksheets[0]
rows=[r for r in ws.iter_rows(values_only=True)]
pickle.dump(rows,open(r'C:/Users/U445131/AppData/Local/Temp/mb51.pkl','wb'))
print(rows[0]); print(rows[1]); print(len(rows))
