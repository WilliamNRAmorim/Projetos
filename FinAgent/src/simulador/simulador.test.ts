// Rodar: node src/simulador/simulador.test.ts (e npm test). Números FICTÍCIOS.
import assert from 'node:assert/strict';
import {
  aliquotaIR, amostrarSerie, faixaDeParcelas, fimDoAparelho, formatarMesAno, lerRespostaCdi, mediaLiquidoMensal,
  mesDaUltimaParcela, mesesCobertos, projetarConta, projetarCofrinho, redirecionarParcela, simular, simularCofrinho,
  taxaMensal,
} from './calc.ts';
import { PERFIL_VAZIO, validarPerfil } from '../metas.ts';
import type { Transacao } from '../mp/extrato.ts';

const perto = (a: number, b: number, tol = 0.011) => assert.ok(Math.abs(a - b) <= tol, `${a} != ${b}`);

// taxa mensal equivalente: (1,12)^(1/12) - 1 = 0,94888% e fecha 12% ao ano
perto(taxaMensal(12), 0.0094888, 1e-7);
perto(Math.pow(1 + taxaMensal(12), 12), 1.12, 1e-12);
assert.equal(taxaMensal(0), 0);

// juros compostos com aporte (conta à mão, i = 1%): 1000 -> 1110 -> 1221,10 -> 1333,311
const s3 = simular({ saldoInicial: 1000, aporte: 100, meses: 3, taxaMensal: 0.01 });
assert.deepEqual(s3.serie.map((x) => x.saldo), [1110, 1221.1, 1333.31]);
assert.deepEqual(s3.serie.map((x) => x.aportado), [100, 200, 300]);
assert.equal(s3.aportado, 300);
assert.equal(s3.saldoBruto, 1333.31);
assert.equal(s3.rendimentoBruto, 33.31);
assert.equal(s3.aliquota, 0.225); // 90 dias
perto(s3.ir, 7.5); // 33,311 x 22,5%
perto(s3.liquido, 1325.82);

// sem juros: nada de rendimento nem IR
const s0 = simular({ saldoInicial: 0, aporte: 100, meses: 10, taxaMensal: 0 });
assert.equal(s0.saldoBruto, 1000);
assert.equal(s0.rendimentoBruto, 0);
assert.equal(s0.ir, 0);
assert.equal(s0.liquido, 1000);

// atalho pelo CDI: 12% ao ano, 100% do CDI, 12 meses, saldo 1000 sem aporte = 1000 x 1,12
perto(simularCofrinho({ saldoInicial: 1000, aporte: 0, meses: 12, cdiAnualPct: 12, pctCdi: 100 }).saldoBruto, 1120);
// 110% do CDI = 13,2% ao ano
perto(simularCofrinho({ saldoInicial: 1000, aporte: 0, meses: 12, cdiAnualPct: 12, pctCdi: 110 }).saldoBruto, 1132);

// faixas do IR pelo prazo (meses x 30 dias)
assert.equal(aliquotaIR(180), 0.225);
assert.equal(aliquotaIR(181), 0.2);
assert.equal(aliquotaIR(360), 0.2);
assert.equal(aliquotaIR(361), 0.175);
assert.equal(aliquotaIR(720), 0.175);
assert.equal(aliquotaIR(721), 0.15);
assert.equal(simular({ saldoInicial: 100, aporte: 0, meses: 6, taxaMensal: 0.01 }).aliquota, 0.225);
assert.equal(simular({ saldoInicial: 100, aporte: 0, meses: 7, taxaMensal: 0.01 }).aliquota, 0.2);
assert.equal(simular({ saldoInicial: 100, aporte: 0, meses: 12, taxaMensal: 0.01 }).aliquota, 0.2);
assert.equal(simular({ saldoInicial: 100, aporte: 0, meses: 13, taxaMensal: 0.01 }).aliquota, 0.175);
assert.equal(simular({ saldoInicial: 100, aporte: 0, meses: 24, taxaMensal: 0.01 }).aliquota, 0.175);
assert.equal(simular({ saldoInicial: 100, aporte: 0, meses: 25, taxaMensal: 0.01 }).aliquota, 0.15);

// meses de reserva e amostragem do gráfico
assert.equal(mesesCobertos(1800, 900), 2);
assert.equal(mesesCobertos(1000, 0), null);
assert.equal(mesesCobertos(1000, null), null);
const amostra = amostrarSerie(simular({ saldoInicial: 0, aporte: 10, meses: 36, taxaMensal: 0 }).serie, 12);
assert.equal(amostra.length, 12);
assert.equal(amostra[11].mes, 36);

// CDI do Banco Central (SGS 4389)
assert.deepEqual(lerRespostaCdi([{ data: '17/10/2026', valor: '14.90' }]), { taxa: 14.9, data: '2026-10-17' });
assert.equal(lerRespostaCdi([]), null);
assert.equal(lerRespostaCdi([{ data: 'x', valor: '14.90' }]), null);
assert.equal(lerRespostaCdi([{ data: '17/10/2026', valor: 'abc' }]), null);
assert.equal(lerRespostaCdi({ erro: 1 }), null);

// fim do aparelho: hoje 18/10/2026, as parcelas restantes incluem a de outubro
const hoje = new Date(2026, 9, 18);
assert.equal(formatarMesAno(mesDaUltimaParcela(hoje, 1)!), '10/2026');
assert.equal(formatarMesAno(mesDaUltimaParcela(hoje, 4)!), '01/2027'); // vira o ano
assert.equal(mesDaUltimaParcela(hoje, 0), null);
const faixa = faixaDeParcelas(6, 10, null)!;
assert.deepEqual(faixa, { min: 6, max: 10 });
const fim = fimDoAparelho(hoje, faixa);
assert.equal(formatarMesAno(fim.de!), '03/2027');
assert.equal(formatarMesAno(fim.ate!), '07/2027');
assert.deepEqual(faixaDeParcelas(10, 6, null), { min: 6, max: 10 }); // invertido
assert.deepEqual(faixaDeParcelas(null, 8, null), { min: 8, max: 8 });
assert.deepEqual(faixaDeParcelas(null, null, 5), { min: 5, max: 5 });
assert.equal(faixaDeParcelas(null, null, null), null);

// redirecionar a parcela: sem juros, 12 x 100 sobre 1000 = 2200; com 1%, 12 meses de espera = 1000 x 1,01^12
const r0 = redirecionarParcela({ saldoInicial: 1000, parcela: 100, mesesAteFim: 0, taxaMensal: 0 });
assert.equal(r0.saldoNoFim, 1000);
assert.equal(r0.depois.saldoBruto, 2200);
assert.equal(r0.depois.aportado, 1200);
perto(redirecionarParcela({ saldoInicial: 1000, parcela: 100, mesesAteFim: 12, taxaMensal: 0.01 }).saldoNoFim, 1126.83);

// "se continuar assim": 3 meses fechados com líquido de 2300 cada (3000 - 200 - 500)
let seq = 0;
const t = (data: string, tipo: string, valor: number): Transacao => ({ data, tipo, ref: `r${seq}`, valor, saldo: 0, seq: seq++ });
const trans: Transacao[] = [];
for (const m of ['2026-07', '2026-08', '2026-09']) {
  trans.push(t(`${m}-05`, 'Pix recebido Empresa Alfa', 3000));
  trans.push(t(`${m}-10`, 'Pagamento com QR Pix IFOOD', -200));
  trans.push(t(`${m}-20`, 'Pagamento de fatura cartão de crédito', -500));
}
trans.push(t('2026-09-12', 'Pix recebido Joao Silva Teste', 500)); // própria conta: entra na média (salário chega assim)
trans.push(t('2026-10-05', 'Pix recebido Empresa Alfa', 3000)); // mês corrente: fora da média
const media = mediaLiquidoMensal(trans, 'Joao Silva Teste', hoje)!;
perto(media.media, 2466.67); // (2300 + 2800 + 2300) / 3: a entrada própria de 500 em setembro agora conta
assert.deepEqual(media.meses, ['2026-09', '2026-08', '2026-07']);
assert.equal(mediaLiquidoMensal([], '', hoje), null);

// salário que chega como transferência da própria conta ("Entrada da sua outra conta") conta como renda
const salProprio: Transacao[] = [];
for (const m of ['2026-07', '2026-08', '2026-09']) {
  salProprio.push(t(`${m}-05`, 'Pix recebido Joao Silva Teste', 3000));
  salProprio.push(t(`${m}-10`, 'Pagamento com QR Pix IFOOD', -200));
  salProprio.push(t(`${m}-20`, 'Pagamento de fatura cartão de crédito', -500));
}
assert.equal(mediaLiquidoMensal(salProprio, 'Joao Silva Teste', hoje)!.media, 2300);
assert.equal(mediaLiquidoMensal(trans, 'Joao Silva Teste', hoje, 1)!.meses.length, 1);

// projeção da conta: 13 dias de 31 restantes em outubro, 2 meses inteiros até dezembro
const pj = projetarConta(1000, 2300, hoje);
perto(pj.fimDoMes, 1964.52);
perto(pj.dezembro, 6564.52);
perto(pj.mesesAteDezembro, 2.42);
const dez = projetarConta(1000, 2300, new Date(2026, 11, 10));
assert.equal(dez.dezembro, dez.fimDoMes);
perto(projetarCofrinho(1000, 0.01, 2), 1020.1);
assert.equal(projetarCofrinho(1000, 0.01, 0), 1000);

// faixa de parcelas no Perfil: máximo menor que o mínimo é erro
assert.ok(validarPerfil({ ...PERFIL_VAZIO, parcelasMin: '10', parcelasMax: '6' }).parcelasMax);
assert.deepEqual(validarPerfil({ ...PERFIL_VAZIO, parcelasMin: '6', parcelasMax: '10' }), {});

console.log('simulador.test.ts: ok');
