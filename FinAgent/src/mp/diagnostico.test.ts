// Rodar: npm test. Fixtures FICTÍCIOS.
import assert from 'node:assert/strict';
import { contarPor, nomesDeCampos } from './diagnostico.ts';

assert.deepEqual(nomesDeCampos({ b: 1, a: { x: 'segredo', y: [{ z: 2 }] }, c: [] }), ['a', 'a.x', 'a.y', 'a.y[].z', 'b', 'c']);
assert.deepEqual(nomesDeCampos(null), []);
assert.deepEqual(nomesDeCampos('texto'), []);
assert.ok(!nomesDeCampos({ nome: 'Fulano' }).some((n) => n.includes('Fulano')));
assert.deepEqual(contarPor([{ t: 'pix' }, { t: 'pix' }, { t: 'credit_card' }, {}], 't'), { pix: 2, credit_card: 1, '(sem)': 1 });
