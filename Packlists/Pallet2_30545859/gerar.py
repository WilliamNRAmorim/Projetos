"""Packlist do pallet 2 da OP 30545859 (ficha 3988): 12 lancamentos do SAP de 27/10 (582,4 m). Previa local; nada gravado no SharePoint."""
import os, types
AQ = r"C:\Users\U445131\Downloads\Projetos\Packlists\Packlists_Lote_Oficial"
src = open(os.path.join(AQ, 'gerar_lote.py'), encoding='utf-8').read()
src = src.replace("GMS = os.path.abspath(os.path.join(AQUI, '..', '..'))", "GMS = os.path.abspath(r'C:/Users/U445131/Downloads/Projetos/GMS')")
g = types.ModuleType('gerar_lote'); g.__file__ = os.path.join(AQ, 'gerar_lote.py')
exec(compile(src, g.__file__, 'exec'), g.__dict__)
lances = [51.0, 48.9, 32.8, 28.3, 42.3, 53.2, 32.6, 24.6, 68.9, 70.7, 66.5, 62.6]
d = dict(date='2026-10-27', id='30545859  .  PALLET 2', pn='HC139-7', lances=lances, foot='Pallet 2 da OP 30545859 (ficha 3988): lancamentos do SAP de 27/10 (docs 3029003870 a 3029009686)')
d['tt'] = g.total_txt(lances); d['total'] = sum(lances)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'PackList_3988_30545859_P2.pdf')
open(out, 'wb').write(g.pdf(d)); print(out, round(d['total'], 1), d['tt'])
