// Rodar: node src/cortes.test.ts. Fixtures FICTÍCIOS.
import assert from 'node:assert/strict';
import { classificarExtrato, mesesDisponiveis, saldoFinal, type Transacao } from './mp/extrato.ts';
import { GRUPOS_CORTE, baseDoGrupo, degrauDoMes, gastoDoGrupo, metaDeCorte, metasDeCorte, proximoMes } from './cortes.ts';

let seq = 0;
const tx = (data: string, tipo: string, valor: number, saldo = 0): Transacao => ({ data, tipo, ref: `r${seq}`, valor, saldo, seq: seq++ });
const cartao = (data: string, nome: string, v: number) => ({ ...tx(data, `Pagamento com cartão Visa ${nome}`, -v), ref: `CARTAO-${data.slice(0, 7)}-${data}-${v}-1` });

const trans: Transacao[] = [
  cartao('2026-07-03', 'DL*UberRides', 100), cartao('2026-07-09', 'UBER * PENDING', 50),
  cartao('2026-08-05', 'DL *UberRides', 150), cartao('2026-08-11', '99Food *Burger Grill', 60),
  cartao('2026-09-04', 'DL*UberRides', 200), cartao('2026-09-12', 'IFD*iFood', 90), cartao('2026-09-20', 'IFOODCOM AGENCIA', 30),
  cartao('2026-09-21', 'MERCADOLIVRE*XYZ', 500),
  tx('2026-10-02', 'Pagamento com QR Pix Ifood Restaurante', -40, 960),
  tx('2026-10-03', 'Pix enviado Uber do Brasil', -45, 915),
  tx('2026-10-05', 'Pagamento de fatura Cartão de crédito', -1000, -85),
  tx('2026-10-06', 'Pix recebido Cliente Teste', 1000, 915),
  tx('2026-07-05', 'Pagamento de fatura Cartão de crédito', -300, 5000), // quita a fatura de jun (não importada)
];
const lancs = classificarExtrato(trans);
const [transp, deliv] = GRUPOS_CORTE;

// palavras-chave do cartão: UberRides, IFD, 99Food
assert.equal(gastoDoGrupo(lancs, transp, '2026-07'), 150);
assert.equal(gastoDoGrupo(lancs, transp, '2026-08'), 150);
assert.equal(gastoDoGrupo(lancs, transp, '2026-09'), 200);
assert.equal(gastoDoGrupo(lancs, deliv, '2026-09'), 120);
assert.equal(gastoDoGrupo(lancs, deliv, '2026-08'), 60);
assert.equal(gastoDoGrupo(lancs, transp, '2026-10'), 45); // Pix para Uber também conta

// pagamento da fatura não conta em dobro quando há compras de cartão
assert.equal(lancs.find((l) => l.valor === -1000)!.categoria, 'Movimento interno');
// pagamento de fatura NÃO importada segue como gasto (jul paga jun; só há compras de jul em diante)
assert.equal(lancs.find((l) => l.valor === -300)!.categoria, 'Fatura do cartão');
// mês só com cartão não vira mês do extrato
assert.ok(!mesesDisponiveis(trans).includes('2026-08'));
// compra de cartão não mexe no saldo da conta
assert.deepEqual(saldoFinal(trans), { saldo: 915, data: '2026-10-06' });

// degraus 10/20/30 e depois mantém
assert.equal(degrauDoMes('2026-10', '2026-09'), 0);
assert.equal(degrauDoMes('2026-10', '2026-10'), 10);
assert.equal(degrauDoMes('2026-10', '2026-11'), 20);
assert.equal(degrauDoMes('2026-10', '2026-12'), 30);
assert.equal(degrauDoMes('2026-10', '2027-05'), 30);
assert.equal(proximoMes('2026-12'), '2027-01');

// base = média dos 3 meses antes do início
assert.equal(baseDoGrupo(lancs, transp, '2026-10'), 166.67); // (150 + 150 + 200) / 3
assert.equal(baseDoGrupo(lancs, deliv, '2026-10'), 60); // (0 + 60 + 120) / 3
assert.equal(baseDoGrupo(lancs, transp, '2026-07'), null); // sem meses anteriores

// meta do mês de início: -10%, gasto 45 de 150 (ok); próximo degrau -20%
const m = metaDeCorte(lancs, transp, '2026-10', '2026-10');
assert.equal(m.degrau, 10);
assert.equal(m.teto, 150);
assert.equal(m.gasto, 45);
assert.equal(m.faixa, 'ok');
assert.equal(m.proximoDegrau, 20);
assert.equal(m.proximoTeto, 133.34);
const e = metaDeCorte(lancs, deliv, '2026-10', '2026-10');
assert.equal(e.teto, 54);
assert.equal(e.faixa, 'ok'); // 40 de 54 = 74%
assert.equal(metasDeCorte(lancs, '2026-10', '2026-10').length, 2);

console.log('cortes: ok');
