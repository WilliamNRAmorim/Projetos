// Rodar: node src/gastos/gastos.test.ts. Fixtures FICTÍCIOS.
import assert from 'node:assert/strict';
import { CAT } from '../mp/categorias.ts';
import { classificarExtrato, type Transacao } from '../mp/extrato.ts';
import {
  REGRAS_VAZIAS, adicionarRegra, agruparPorDia, faixaOrcamento, filtrarTransacoes, linhasOrcamento,
  mediaUltimos3Meses, mesesDoPeriodo, porCategoriaNoPeriodo,
} from './gastos.ts';

let seq = 0;
const tx = (data: string, tipo: string, valor: number, ref = String(1000 + seq)): Transacao => ({ data, tipo, ref, valor, saldo: 0, seq: seq++ });

const trans: Transacao[] = [
  tx('2026-07-10', 'Pagamento com QR Pix Ifood Restaurante', -100),
  tx('2026-08-10', 'Pagamento com QR Pix Ifood Restaurante', -200),
  tx('2026-09-10', 'Pagamento com QR Pix Ifood Restaurante', -300),
  tx('2026-09-12', 'Pagamento de fatura Cartão de crédito', -900),
  tx('2026-10-02', 'Pagamento com QR Pix Ifood Restaurante', -90),
  tx('2026-10-02', 'Pagamento com QR Pix Loja Teste', -40),
  tx('2026-10-03', 'Pix enviado Fulano de Tal', -30),
  tx('2026-10-03', 'Dinheiro reservado Emergências', -500),
  tx('2026-10-04', 'Pix recebido Maria Cliente', 1000),
  tx('2026-10-05', 'Pagamento de fatura Cartão de crédito', -1000),
];
const base = classificarExtrato(trans);

// faixas
assert.equal(faixaOrcamento(79.9), 'ok');
assert.equal(faixaOrcamento(80), 'atencao');
assert.equal(faixaOrcamento(100), 'atencao');
assert.equal(faixaOrcamento(100.1), 'estourou');

// orçamento do mês
const o = linhasOrcamento(base, '2026-10', { [CAT.COMIDA]: 100, [CAT.OUTROS]: 200, [CAT.FATURA]: 800 });
const comida = o.linhas.find((l) => l.categoria === CAT.COMIDA)!;
assert.equal(comida.gasto, 90);
assert.equal(comida.faixa, 'atencao');
assert.equal(o.linhas.find((l) => l.categoria === CAT.OUTROS)!.faixa, 'ok');
const fat = o.linhas.find((l) => l.categoria === CAT.FATURA)!;
assert.equal(fat.gasto, 1000);
assert.equal(fat.faixa, 'estourou');
assert.equal(o.linhas[o.linhas.length - 1].categoria, CAT.FATURA); // fatura por último
assert.equal(o.totalOrcado, 1100);
assert.equal(o.totalGasto, 1130);
// sem teto: sem faixa
assert.equal(o.linhas.find((l) => l.categoria === CAT.PIX_PESSOAS)!.faixa, null);
// movimento interno nunca entra no orçamento
assert.ok(!o.linhas.some((l) => l.categoria === CAT.INTERNO));

// sugestão: média dos 3 meses anteriores (100, 200, 300)
assert.equal(mediaUltimos3Meses(base, '2026-10', CAT.COMIDA), 200);
assert.equal(mediaUltimos3Meses(base, '2026-10', CAT.FATURA), 300); // só setembro tem fatura -> 900/3
assert.equal(mediaUltimos3Meses(base, '2026-07', CAT.COMIDA), null); // sem meses anteriores
assert.equal(mediaUltimos3Meses(base, '2026-10', CAT.TRANSPORTE), null);

// períodos
assert.deepEqual(mesesDoPeriodo('mes', [], '2026-10'), ['2026-10']);
assert.deepEqual(mesesDoPeriodo('3m', [], '2026-01'), ['2026-01', '2025-12', '2025-11']);
const mes = porCategoriaNoPeriodo(base, 'mes', '2026-10');
assert.equal(mes[0].nome, CAT.COMIDA);
assert.equal(mes.reduce((s, c) => s + c.total, 0), 160);
const tres = porCategoriaNoPeriodo(base, '3m', '2026-10');
assert.equal(tres.find((c) => c.nome === CAT.COMIDA)!.total, 590); // set + ago + out
const tudo = porCategoriaNoPeriodo(base, 'tudo', '2026-10');
assert.equal(tudo.find((c) => c.nome === CAT.COMIDA)!.total, 690);
assert.ok(Math.abs(tudo.reduce((s, c) => s + c.pct, 0) - 100) < 0.5);
assert.ok(!tudo.some((c) => c.nome === CAT.FATURA || c.nome === CAT.INTERNO));

// regra de recategorização prevalece sobre palavra-chave (ifood = comida por palavra)
const ifood = base.find((l) => l.data === '2026-10-02' && l.valor === -90)!;
assert.equal(ifood.categoria, CAT.COMIDA);
assert.ok(ifood.contraparte.includes('ifood'));
const r1 = adicionarRegra(REGRAS_VAZIAS, ifood, CAT.OUTROS, false);
const comRegra = classificarExtrato(trans, '', r1);
assert.equal(comRegra.filter((l) => l.contraparte === ifood.contraparte).every((l) => l.categoria === CAT.OUTROS), true); // todas as com mesma contraparte
assert.equal(comRegra.find((l) => l.valor === -40)!.categoria, CAT.OUTROS); // sem regra, segue igual
// assinatura antiga continua funcionando
assert.equal(classificarExtrato(trans, '')[4].categoria, CAT.COMIDA);

// só esta transação
const r2 = adicionarRegra(REGRAS_VAZIAS, ifood, CAT.TRANSPORTE, true);
const soEsta = classificarExtrato(trans, '', r2);
assert.equal(soEsta.filter((l) => l.categoria === CAT.TRANSPORTE).length, 1);
assert.equal(soEsta.find((l) => l.data === '2026-10-02' && l.valor === -90)!.categoria, CAT.TRANSPORTE);
assert.equal(soEsta.find((l) => l.data === '2026-09-10')!.categoria, CAT.COMIDA);
// por transação ganha da por contraparte
const r3 = adicionarRegra(r1, ifood, CAT.TRANSPORTE, true);
const mix = classificarExtrato(trans, '', r3);
assert.equal(mix.find((l) => l.data === '2026-10-02' && l.valor === -90)!.categoria, CAT.TRANSPORTE);
assert.equal(mix.find((l) => l.data === '2026-09-10')!.categoria, CAT.OUTROS);
// regra não reabre estorno nem mexe em linha sem contraparte
const comEstorno = [...trans, tx('2026-10-06', 'Reembolso Loja Teste', 40)];
const ce = classificarExtrato(comEstorno, '', { porContraparte: { 'loja teste': CAT.COMIDA } });
assert.equal(ce[ce.length - 1].categoria, CAT.ESTORNO);

// regra reflete no orçamento
const oReg = linhasOrcamento(comRegra, '2026-10', { [CAT.COMIDA]: 100 });
assert.equal(oReg.linhas.find((l) => l.categoria === CAT.COMIDA)!.gasto, 0);

// busca e filtros
assert.equal(filtrarTransacoes(base, {}).some((l) => l.categoria === CAT.INTERNO), false); // internos ocultos
assert.equal(filtrarTransacoes(base, { mostrarInternos: true }).some((l) => l.categoria === CAT.INTERNO), true);
assert.equal(filtrarTransacoes(base, { busca: 'IFOOD' }).length, 4); // sem acento/caixa
assert.equal(filtrarTransacoes(base, { busca: 'maria' }).length, 1);
assert.equal(filtrarTransacoes(base, { mes: '2026-10', categoria: CAT.OUTROS }).length, 1);
assert.equal(filtrarTransacoes(base, { mes: '2026-09' }).length, 2);
assert.equal(filtrarTransacoes(base, { busca: 'zzz' }).length, 0);

// ordem e agrupamento por dia (mais recente primeiro)
const lista = filtrarTransacoes(base, { mes: '2026-10' });
assert.equal(lista[0].data, '2026-10-05');
const g = agruparPorDia(lista);
assert.deepEqual(g.map((x) => x.data), ['2026-10-05', '2026-10-04', '2026-10-03', '2026-10-02']);
assert.equal(g[3].itens.length, 2);

console.log('gastos.test.ts: ok');
