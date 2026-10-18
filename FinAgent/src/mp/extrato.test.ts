// Rodar: npm test. Fixtures FICTÍCIOS.
import assert from 'node:assert/strict';
import {
  classificarExtrato, mesclar, parseData, parseExtratoCsv, parseValorBR, saldoFinal, totaisMes,
} from './extrato.ts';
import { resumoParaIA } from './resumoParaIA.ts';

assert.equal(parseValorBR('1.900,00'), 1900);
assert.equal(parseValorBR('-74,99'), -74.99);
assert.equal(parseValorBR('4.117,31'), 4117.31);
assert.equal(parseValorBR('0,00'), 0);
assert.equal(parseValorBR('abc'), null);
assert.equal(parseData('05-10-2026'), '2026-10-05');
assert.equal(parseData('2026-10-05'), null);

const csv = [
  '﻿INITIAL_BALANCE;CREDITS;DEBITS;FINAL_BALANCE',
  '100,00;3.000,00;-2.500,00;600,00',
  '',
  'RELEASE_DATE;TRANSACTION_TYPE;REFERENCE_ID;TRANSACTION_NET_AMOUNT;PARTIAL_BALANCE',
  '01-10-2026;Pix recebido Maria Cliente;1001;3.000,00;3.100,00;',
  '02-10-2026;Pagamento com QR Pix Ifood Restaurante;1002;-50,00;3.050,00',
  '02-10-2026;Pagamento com QR Pix Loja Teste;1003;-80,00;2.970,00',
  '03-10-2026;Pagamento com código QR Pix - Cancelado Loja Teste;1003;80,00;3.050,00',
  '03-10-2026;Dinheiro reservado Emergências;1004;-500,00;2.550,00',
  '04-10-2026;Dinheiro retirado Emergências;1005;100,00;2.650,00',
  '05-10-2026;Pagamento de fatura Cartão de crédito;1006;-1.000,00;1.650,00',
  '06-10-2026;Transferência recebida Joao Silva Santos;1007;200,00;1.850,00',
  '07-10-2026;Pix enviado Fulano de Tal;1008;-1.250,00;600,00',
  '07-10-2026;Rendimentos;1009;0,50;600,50',
].join('\r\n');

const t = parseExtratoCsv(csv);
assert.equal(t.length, 10);
assert.equal(t[0].valor, 3000);
assert.equal(t[0].data, '2026-10-01');

// reimportar não duplica
assert.equal(mesclar(t, parseExtratoCsv(csv)).length, 10);

// saldo final = parcial da última linha cronológica
assert.deepEqual(saldoFinal(t), { saldo: 600.5, data: '2026-10-07' });

// arquivo em ordem decrescente dá o mesmo saldo final
const linhasDados = csv.split('\r\n').slice(4).reverse();
const csvDesc = ['RELEASE_DATE;TRANSACTION_TYPE;REFERENCE_ID;TRANSACTION_NET_AMOUNT;PARTIAL_BALANCE', ...linhasDados].join('\n');
assert.equal(saldoFinal(parseExtratoCsv(csvDesc))?.saldo, 600.5);

const l = classificarExtrato(t, 'Joao Silva Santos');
const cat = (ref: string) => l.find((x) => x.ref === ref)!;
assert.equal(cat('1001').categoria, 'Entrada');
assert.equal(cat('1002').categoria, 'Comida/delivery');
assert.equal(cat('1004').categoria, 'Movimento interno');
assert.equal(cat('1007').categoria, 'Entrada da sua outra conta');
assert.equal(cat('1008').categoria, 'Pix para pessoas');
assert.equal(cat('1006').categoria, 'Fatura do cartão');

// par pagamento + estorno some dos totais
assert.equal(l.filter((x) => x.ref === '1003' && x.excluida).length, 2);

const tot = totaisMes(l, '2026-10');
assert.equal(tot.entradas, 3200);
assert.equal(tot.entradasOutraConta, 200);
assert.equal(tot.rendimentos, 0.5);
assert.equal(tot.gastos, 1300); // 50 + 1250; interno, fatura e par estornado ficam fora
assert.equal(tot.fatura, 1000);
assert.equal(tot.reservaLiquida, 400); // reservou 500, retirou 100
assert.deepEqual(tot.porCategoria.map((c) => c.nome), ['Pix para pessoas', 'Comida/delivery']);
assert.equal(tot.variacaoGasto, null);

// meses seguintes: variação
const t2 = mesclar(t, [{ data: '2026-11-02', tipo: 'Pagamento Uber Trip', ref: '2001', valor: -650, saldo: 0, seq: 0 }]);
const tot2 = totaisMes(classificarExtrato(t2), '2026-11');
assert.equal(tot2.gastos, 650);
assert.equal(tot2.variacaoGasto, -50);

// resumo para IA: só agregados
const resumo = resumoParaIA(tot);
assert.ok(resumo.includes('Pix para pessoas'));
assert.ok(!/Fulano|Maria|Joao|Ifood|Loja/i.test(resumo));

console.log('extrato: todos os testes passaram');
