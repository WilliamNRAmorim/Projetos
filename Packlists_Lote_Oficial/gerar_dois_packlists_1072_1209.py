"""Reconstroi os packlists das OPs 29788884 (ficha 3327) e 30078414 (ficha 3486), que dividem o packing 1209 do BD.
ID PALLET = id do packing no BD Packing List: 1072 (OP 29788884, 521,3 m), 1209 (OP 29788884, pecas 6 a 10, 224,3 m) e 1209 (OP 30078414, pecas 1 a 5, 186,5 m).
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
s1072 = dict(b1072['sl'])
saida = os.path.join(g.AQUI, 'saida_corrigidos'); os.makedirs(saida, exist_ok=True)
for f in os.listdir(saida):
    os.remove(os.path.join(saida, f))
# ID PALLET = id do packing no BD Packing List. O 1209 e dividido entre duas OPs, entao sai um PDF do 1209 para cada OP.
itens = [(3327, '29788884', 1072, '2026-08-24', [s1072[i] for i in sorted(s1072)], 'Packing #1072 do BD Packing List, inteiro (OP 29788884)'),
         (3327, '29788884', 1209, '2026-09-04', [s1209[i] for i in range(6, 11)], 'Pecas 6 a 10 do packing #1209 do BD Packing List (OP 29788884; as pecas 1 a 5 sao da OP 30078414)'),
         (3486, '30078414', 1209, '2026-09-04', [s1209[i] for i in range(1, 6)], 'Pecas 1 a 5 do packing #1209 do BD Packing List (OP 30078414; as pecas 6 a 10 sao da OP 29788884)')]
for fid, op, pid, data, lances, nota in itens:
    d = dict(date=data, id=str(pid), pn='HC139-7', lances=lances, foot='Reconstruido do BD Packing List - ' + nota)
    d['tt'] = g.total_txt(lances); d['total'] = sum(lances)
    open(os.path.join(saida, 'PackList_%d_%s_pallet%d.pdf' % (fid, op, pid)), 'wb').write(g.pdf(d))
    print('ficha', fid, 'OP', op, '| ID PALLET', pid, '|', len(lances), 'pecas', round(sum(lances), 1), 'm | codigo do total:', d['tt'])
