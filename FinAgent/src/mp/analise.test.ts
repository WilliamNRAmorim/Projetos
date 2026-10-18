// Rodar: npm test (node executa TypeScript direto). Dados fictícios.
import assert from 'node:assert/strict';
import { categorizar, classificar, totaisDoMes, mesAnterior, gastoPorCategoria, SEM_DESCRICAO } from './analise.ts';

const USER = 1;
const p = (id: number, date: string, valor: number, collector: number, description = '', extra = {}) => ({
  id,
  date_created: date,
  transaction_amount: valor,
  payment_type_id: 'account_money',
  status: 'approved',
  description,
  collector_id: collector,
  ...extra,
});

// categoria
assert.equal(categorizar('Recarga Vivo'), 'Telefonia');
assert.equal(categorizar('Claro fatura'), 'Telefonia');
assert.equal(categorizar('Santander cartao'), 'Banco');
assert.equal(categorizar(''), SEM_DESCRICAO);
assert.equal(categorizar(null), SEM_DESCRICAO);
assert.equal(categorizar('xyz qualquer'), 'Outros');

// mês
assert.equal(mesAnterior('2026-01'), '2025-12');
assert.equal(mesAnterior('2026-10'), '2026-09');

const dados = [
  p(1, '2026-10-05T12:00:00-03:00', 3000, USER), // recebido
  p(2, '2026-10-06T12:00:00-03:00', 100, 99, 'Vivo'), // gasto
  p(3, '2026-10-07T12:00:00-03:00', 1000.17, 99, 'transf'), // interna (pago)
  p(4, '2026-10-07T15:00:00-03:00', 1000.17, USER), // interna (recebido)
  p(5, '2026-10-08T12:00:00-03:00', 50, 99), // gasto sem descrição
  p(6, '2026-10-09T12:00:00-03:00', 70, 99, 'x', { status: 'cancelled' }), // ignorado
  p(7, '2026-09-10T12:00:00-03:00', 200, 99, 'Santander'), // mês anterior
];
const movs = classificar(dados, USER);
assert.equal(movs.length, 6);
assert.equal(movs.filter((m) => m.interna).length, 2);

const out = totaisDoMes(movs, '2026-10');
assert.equal(out.recebido, 3000);
assert.equal(out.gasto, 150);
assert.equal(out.sobra, 2850);
assert.equal(out.interno, 1000.17);
assert.equal(totaisDoMes(movs, '2026-09').gasto, 200);

const cats = gastoPorCategoria(movs, '2026-10');
assert.deepEqual(cats.map((c) => c.nome), ['Telefonia', SEM_DESCRICAO]);

console.log('analise: todos os testes passaram');
