"""Packlists refeitos em 29/10: pallet 208 (OP 30589719, ficha 4112) e pallet 256 (OP 30636250, ficha 4164). Previa local."""
import os, types
AQ = r"C:\Users\U445131\Downloads\Projetos\Packlists\Packlists_Lote_Oficial"
src = open(os.path.join(AQ, 'gerar_lote.py'), encoding='utf-8').read()
src = src.replace("GMS = os.path.abspath(os.path.join(AQUI, '..', '..'))", "GMS = os.path.abspath(os.path.join(AQUI, '..', 'GMS'))")
src = src.replace("os.path.join(AQUI, '..', 'GMS')", "r'C:/Users/U445131/Downloads/Projetos/GMS'")
g = types.ModuleType('gerar_lote'); g.__file__ = os.path.join(AQ, 'gerar_lote.py')
exec(compile(src, g.__file__, 'exec'), g.__dict__)
saida = os.path.dirname(os.path.abspath(__file__))
for fid, op, pn, data, lances in [(4112, '30589719', 'GH781-12', '2026-10-22', [11.0, 17.8, 105.1, 57.8, 103.1, 102.6]),
                                  (4164, '30636250', 'GH493-16', '2026-10-27', [27.0, 51.2, 50.2, 17.5, 49.8, 37.8])]:
    d = dict(date=data, id=op, pn=pn, lances=lances, foot='Refeito em 29/10/2026 com os lancamentos do SAP (ficha %d)' % fid)
    d['tt'] = g.total_txt(lances); d['total'] = sum(lances)
    out = os.path.join(saida, 'PackList_%d_%s.pdf' % (fid, op)); open(out, 'wb').write(g.pdf(d)); print(out, round(d['total'], 1), d['tt'])
