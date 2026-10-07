"""Gera Engenharia/INDICE.md: para cada DM_*.xlsx lista as abas, tamanho e o cabeçalho (1ª linha preenchida).
Rodar de dentro de GMS/Engenharia:  python indexar.py"""
import os, openpyxl, datetime as dt

AQUI = os.path.dirname(os.path.abspath(__file__))
PASTA = os.path.join(AQUI, 'DM_DATABASE')
out = ['# Engenharia: bases DM_ (Delineamento Hose Manufacturing)', '',
       'Fonte: site SharePoint `Delineamento Hose Manufacturing` (`https://danfoss.sharepoint.com/sites/DelineamentoHM`),',
       'biblioteca `DM_DATABASE` e listas `DM_MANDREL` e `AdminConsole`. Cópia de 08/10/2026; a fonte oficial é o SharePoint da Engenharia.', '',
       '| Arquivo | Aba | Linhas × colunas | Cabeçalho (primeiras colunas) |', '|---|---|---|---|']
for f in sorted(os.listdir(PASTA)):
    if not f.lower().endswith('.xlsx'):
        continue
    try:
        wb = openpyxl.load_workbook(os.path.join(PASTA, f), read_only=True, data_only=True)
    except Exception as e:
        out.append('| %s | (erro ao abrir: %s) | | |' % (f, e)); continue
    for ws in wb.worksheets:
        head = []
        for r in ws.iter_rows(min_row=1, max_row=15, values_only=True):
            vals = [str(v).strip() for v in r if v not in (None, '')]
            if len(vals) >= 2:
                head = vals[:8]; break
        out.append('| %s | %s | %s × %s | %s |' % (f, ws.title, ws.max_row, ws.max_column, ' · '.join(head).replace('|', '/')[:150]))
out += ['', 'Listas do site (CSV em `listas/`): `DM_MANDREL` (13 itens) e `AdminConsole` (7 itens).', '',
        'Não copiados (não são DM_ e são grandes): `Hose_Assembly_Database.xlsx` (9 MB), `Banco_de_Datos.xlsx` (1,2 MB), `Conexoes.xlsx`, `Dados_Prensagem.xlsx`, `PressaoeProjetil.xlsx`.']
open(os.path.join(AQUI, 'INDICE.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print(len(out) - 8, 'linhas de índice')
