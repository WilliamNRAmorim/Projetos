"""Reconstroi os dois packlists que dividem o packing 1209 do BD (16/10/2026):
 - ficha 3327 / OP 29788884: packing 1072 inteiro (19 pecas, 521,3 m) + pecas 6 a 10 do 1209 (224,3 m) = 24 pecas, 745,6 m
 - ficha 3486 / OP 30078414: pecas 1 a 5 do packing 1209 (186,5 m)
Saida em saida_corrigidos/ (nada e gravado no SharePoint)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import types
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gerar_lote.py'), encoding='utf-8').read()
src = src.replace("GMS = os.path.abspath(os.path.join(AQUI, '..', '..'))", "GMS = os.path.abspath(os.path.join(AQUI, '..', 'GMS'))")
g = types.ModuleType('gerar_lote'); g.__file__ = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gerar_lote.py')
exec(compile(src, g.__file__, 'exec'), g.__dict__)
bd = g.carregar_bd()
b1072 = next(v for k, v in bd.items() if k[0] == 1072)
b1209 = next(v for k, v in bd.items() if k[0] == 1209)
s1209 = dict(b1209['sl'])
l3327 = list(b1072['lances']) + [s1209[i] for i in range(6, 11)]
l3486 = [s1209[i] for i in range(1, 6)]
saida = os.path.join(g.AQUI, 'saida_corrigidos'); os.makedirs(saida, exist_ok=True)
for fid, op, lances, nota in ((3327, '29788884', l3327, 'Reconstruido do BD Packing List: packing #1072 inteiro + pecas 6 a 10 do #1209 (dividido com a OP 30078414)'),
                              (3486, '30078414', l3486, 'Reconstruido do BD Packing List: pecas 1 a 5 do packing #1209 (dividido com a OP 29788884)')):
    d = dict(date='2026-09-04', id=op, pn='HC139-7', lances=lances, foot=nota)
    d['tt'] = g.total_txt(lances); d['total'] = sum(lances)
    open(os.path.join(saida, 'PackList_%d_%s.pdf' % (fid, op)), 'wb').write(g.pdf(d))
    print(fid, op, len(lances), 'pecas', round(sum(lances), 1), 'm | codigo do total:', d['tt'], '|', [round(x, 1) for x in lances])
