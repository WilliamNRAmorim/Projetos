// Rodar: npm test. Fixtures FICTÍCIOS.
import assert from 'node:assert/strict';
import {
  comprometidoDoMes, diasAteSalario, faixaLimite, livreAteSalario, mediaGastoMensal, mesesDeReserva, metaReserva,
  perfilParaNumeros, PERFIL_VAZIO, progressoReserva, resumoMetas, retiradasCofrinho, usoLimite, validarCampo,
} from './metas.ts';
import { resumoParaIA } from './mp/resumoParaIA.ts';
import { classificarExtrato, totaisMes, type Transacao } from './mp/extrato.ts';

const perfil = perfilParaNumeros({
  ...PERFIL_VAZIO, salario: '3.000,00', diaSalario: '30', parcela: '300,00', cofrinho: '1.800,00',
  separadoAparelho: '100,00', limiteCartao: '1.000,00', faturaAberta: '450,00',
});
assert.equal(perfil.salario, 3000);
assert.equal(perfil.parcelasRestantes, null);

// validação
assert.equal(validarCampo('salario', '1.234,56'), null);
assert.equal(validarCampo('salario', ''), null);
assert.ok(validarCampo('salario', 'abc'));
assert.ok(validarCampo('salario', '-5,00'));
assert.ok(validarCampo('diaSalario', '32'));
assert.ok(validarCampo('diaSalario', '15,5'));
assert.equal(validarCampo('diaSalario', '30'), null);

// comprometido
const c = comprometidoDoMes(perfil);
assert.deepEqual(c, { parcela: 300, fatura: 450, total: 750, pctSalario: 25 });
assert.equal(comprometidoDoMes({ ...perfil, parcelasRestantes: 0 }).total, 450);
assert.equal(comprometidoDoMes({ ...perfil, salario: null }).pctSalario, null);

// dias até o salário
assert.equal(diasAteSalario(new Date(2026, 9, 18), 30), 12);
assert.equal(diasAteSalario(new Date(2026, 9, 30), 30), 0);
assert.equal(diasAteSalario(new Date(2026, 9, 31), 30), 30);
assert.equal(diasAteSalario(new Date(2026, 1, 10), 30), 18); // fevereiro: dia 28

// livre: 2000 - 450 - (300-100) = 1350, 12 dias
assert.deepEqual(livreAteSalario(2000, perfil, new Date(2026, 9, 18)), { valor: 1350, dias: 12, porDia: 112.5 });
assert.equal(livreAteSalario(2000, { ...perfil, diaSalario: null }, new Date(2026, 9, 18)), null);

// fatura vence dia 5, salário dia 30: em 18/10 o vencimento (05/11) cai DEPOIS do salário (30/10): não subtrai a fatura
assert.equal(livreAteSalario(2000, { ...perfil, diaVencimento: 5 }, new Date(2026, 9, 18))?.valor, 1800); // 2000 - 0 - (300-100)
// em 02/11 o vencimento (05/11) cai ANTES do próximo salário (30/11): subtrai
assert.equal(livreAteSalario(2000, { ...perfil, diaVencimento: 5 }, new Date(2026, 10, 2))?.valor, 1350);
// parcela dia 10: em 18/10 a próxima (10/11) cai depois do salário (30/10): não subtrai; dia 25 ainda vai cair: subtrai
assert.equal(livreAteSalario(2000, { ...perfil, diaVencimento: 5, diaParcela: 10 }, new Date(2026, 9, 18))?.valor, 2000);
assert.equal(livreAteSalario(2000, { ...perfil, diaVencimento: 5, diaParcela: 25 }, new Date(2026, 9, 18))?.valor, 1800);
// dia da parcela é hoje: ainda conta
assert.equal(livreAteSalario(2000, { ...perfil, diaVencimento: 5, diaParcela: 18 }, new Date(2026, 9, 18))?.valor, 1800);
// sem dia de vencimento nem da parcela: subtrai tudo (conservador)
assert.equal(livreAteSalario(2000, perfil, new Date(2026, 9, 18))?.valor, 1350);

// limite
assert.equal(usoLimite(1000, 450), 45);
assert.equal(usoLimite(null, 450), null);
assert.equal(faixaLimite(29.9), 'ok');
assert.equal(faixaLimite(30), 'atencao');
assert.equal(faixaLimite(60), 'atencao');
assert.equal(faixaLimite(60.1), 'alerta');

// extrato fictício de 4 meses
const t = (data: string, tipo: string, ref: string, valor: number): Transacao => ({ data, tipo, ref, valor, saldo: 0, seq: 0 });
const trans: Transacao[] = [
  t('2026-07-02', 'Pix enviado Loja Teste', '1', -400),
  t('2026-07-20', 'Pagamento de fatura Cartão de crédito', '2', -200),
  t('2026-08-05', 'Pix enviado Loja Teste', '3', -600),
  t('2026-08-20', 'Pagamento de fatura Cartão de crédito', '4', -400),
  t('2026-09-05', 'Dinheiro reservado Emergências', '5', -300), // interno, fora
  t('2026-09-06', 'Pix enviado Loja Teste', '6', -800),
  t('2026-09-12', 'Dinheiro retirado Cofrinho', '7', 150),
  t('2026-09-25', 'Dinheiro retirado Emergências', '8', 50), // não é Cofrinho
  t('2026-10-02', 'Pix enviado Loja Teste', '9', -50),
];
// mês corrente (out) fica de fora: (600+400 + 800 + 600) / 3 ... jul=600, ago=1000, set=800 -> 800
const media = mediaGastoMensal(trans, '', new Date(2026, 9, 18));
assert.deepEqual(media, { media: 800, meses: ['2026-09', '2026-08', '2026-07'] });
assert.equal(mediaGastoMensal(trans, '', new Date(2026, 9, 18), 2)?.media, 900);
assert.equal(mediaGastoMensal([], '', new Date(2026, 9, 18)), null);
// com um só mês (o corrente) usa-o mesmo assim
assert.equal(mediaGastoMensal([trans[8]], '', new Date(2026, 9, 18))?.media, 50);
assert.equal(mediaGastoMensal([trans[8]], '', new Date(2026, 9, 18))?.parcial, true);
assert.equal(media?.parcial, undefined, 'com meses completos não é parcial');

// mês parcial: o extrato começa em 20/07 (parcial, jul fica de fora); out é o corrente (fora). Média = ago e set.
{
  const parc = trans.filter((x) => x.data >= '2026-08').concat([t('2026-07-20', 'Pix enviado Loja Teste', '0', -90)]);
  const m = mediaGastoMensal(parc, '', new Date(2026, 9, 18));
  assert.deepEqual(m, { media: 900, meses: ['2026-09', '2026-08'] });
  // só meses parciais (primeiro mês incompleto + mês corrente): usa todos e marca como parcial
  const so = mediaGastoMensal([t('2026-09-20', 'Pix enviado Loja Teste', '0', -100), t('2026-10-02', 'Pix enviado Loja Teste', '0', -50)], '', new Date(2026, 9, 18));
  assert.equal(so?.parcial, true);
  assert.deepEqual(so?.meses, ['2026-10', '2026-09']);
  assert.equal(so?.media, 75);
  // extrato que começa no dia 1 a 3 não é parcial
  const ini3 = mediaGastoMensal([t('2026-09-03', 'Pix enviado Loja Teste', '0', -100), t('2026-10-02', 'Pix enviado Loja Teste', '0', -50)], '', new Date(2026, 9, 18));
  assert.equal(ini3?.parcial, undefined);
  assert.equal(ini3?.media, 100);
}

// reserva
assert.equal(metaReserva(800, 3), 2400);
assert.equal(progressoReserva(1800, 2400), 75);
assert.equal(progressoReserva(5000, 2400), 100);
assert.equal(progressoReserva(100, 0), null);
assert.equal(mesesDeReserva(1800, 800), 2.3);
assert.equal(mesesDeReserva(1800, null), null);

// retirada do Cofrinho
assert.deepEqual(retiradasCofrinho(trans), [{ data: '2026-09-12', valor: 150 }]);
assert.deepEqual(retiradasCofrinho([]), []);

// resumo para IA: só agregados
const r = resumoMetas(perfil, media!.media);
assert.deepEqual(r, { salario: 3000, pctComprometido: 25, pctLimite: 45, mesesReserva: 2.3 });
const txt = resumoParaIA(totaisMes(classificarExtrato(trans), '2026-09'), r);
assert.ok(txt.includes('salário 3000.00') && txt.includes('25% do salário') && txt.includes('45% do limite') && txt.includes('2.3 meses'));
assert.ok(!/Loja|Cofrinho/i.test(txt));

console.log('metas: todos os testes passaram');
