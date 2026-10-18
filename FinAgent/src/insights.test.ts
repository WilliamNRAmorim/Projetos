// Rodar: npm test. Fixtures FICTÍCIOS.
import assert from 'node:assert/strict';
import { alertasDoInicio, gerarInsights, nomeMes, serieEntrouSaiu } from './insights.ts';
import { PERFIL_VAZIO, perfilParaNumeros } from './metas.ts';
import { classificarExtrato, type Transacao } from './mp/extrato.ts';

let seq = 0;
const t = (data: string, tipo: string, valor: number): Transacao => ({ data, tipo, ref: `r${seq}`, valor, saldo: 0, seq: seq++ });

const trans: Transacao[] = [
  t('2026-08-05', 'Pix recebido Empresa Alfa', 3000),
  t('2026-08-10', 'Pagamento com QR Pix IFOOD', -100),
  t('2026-08-12', 'Pagamento com QR Pix UBER', -50),
  t('2026-08-20', 'Pagamento de fatura cartão de crédito', -400),
  t('2026-09-05', 'Pix recebido Empresa Alfa', 3000),
  t('2026-09-05', 'Pagamento de fatura cartão de crédito', -500),
  t('2026-09-10', 'Pagamento com QR Pix IFOOD', -200),
  t('2026-09-12', 'Pagamento com QR Pix UBER', -50),
  t('2026-10-05', 'Pix recebido Empresa Alfa', 3000),
  t('2026-10-06', 'Pagamento de fatura cartão de crédito', -450),
  t('2026-10-08', 'Pagamento Mercado Teste', -300),
  t('2026-10-10', 'Pagamento com QR Pix IFOOD', -40),
  t('2026-10-12', 'Dinheiro retirado Cofrinho', 100),
];
const lancs = classificarExtrato(trans);
const hoje = new Date(2026, 9, 18);
const perfil = perfilParaNumeros({ ...PERFIL_VAZIO, salario: '3.000,00', diaSalario: '30', parcela: '300,00', limiteCartao: '1.000,00', faturaAberta: '650,00' });

assert.equal(nomeMes('2026-10'), 'outubro');

// insights: no máximo 4, ordenados por prioridade, delivery (prioridade 5) fica de fora
const ins = gerarInsights({ trans, lancs, perfil, hoje });
assert.deepEqual(ins.map((i) => i.id), ['cofrinho', 'fatura', 'maior', 'variacao']);
assert.equal(ins[0].texto, 'Retirada de R$ 100,00 do Cofrinho em 12/10.');
assert.equal(ins[1].tipo, 'sucesso');
assert.equal(ins[1].texto, 'Fatura paga em outubro: R$ 450,00, 10% a menos que em setembro.');
assert.match(ins[2].texto, /Outros comércio, R\$ 300,00 \(88% dos gastos\)/);
assert.equal(ins[3].texto, 'Comida/delivery subiu R$ 100,00 de agosto para setembro.');
assert.equal(ins[3].tipo, 'alerta');

// com limite maior o delivery aparece
const todos = gerarInsights({ trans, lancs, perfil, hoje }, 10);
assert.equal(todos.find((i) => i.id === 'delivery')?.texto, '8 dias sem gasto com comida/delivery.');

// sem retirada recente (hoje em dezembro): some o alerta do Cofrinho
assert.equal(gerarInsights({ trans, lancs, perfil, hoje: new Date(2026, 11, 20) }, 10).some((i) => i.id === 'cofrinho'), false);

// sem dados
assert.deepEqual(gerarInsights({ trans: [], lancs: [], perfil, hoje }), []);

// alertas do sino: retirada, limite 65%, saldo não cobre (500 - 650 - 300)
const al = alertasDoInicio({ trans, perfil, saldoConta: 500, hoje });
assert.equal(al.length, 3);
assert.equal(alertasDoInicio({ trans: [], perfil: perfilParaNumeros(PERFIL_VAZIO), saldoConta: null, hoje }).length, 0);

// série do gráfico: meses em ordem crescente, saiu = gastos + fatura
assert.deepEqual(serieEntrouSaiu(lancs, trans), [
  { mes: '2026-08', entrou: 3000, saiu: 550 },
  { mes: '2026-09', entrou: 3000, saiu: 750 },
  { mes: '2026-10', entrou: 3000, saiu: 790 },
]);
assert.equal(serieEntrouSaiu(lancs, trans, 2).length, 2);

console.log('insights: ok');
