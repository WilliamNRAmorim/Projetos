// Rodar: node src/padroes.test.ts. Fixtures FICTÍCIOS.
import assert from 'node:assert/strict';
import { classificarExtrato, type Transacao } from './mp/extrato.ts';
import { GRUPOS_CORTE } from './cortes.ts';
import {
  alvoDoNivel, analisarPadroes, coberturaAte, diaDaSemana, estadoDoPlano, inicioDaSemana, perfilSemanal, primeiraSemanaDoPlano,
  resumoPadroesPct, semanasFechadas, somarDias, tipoDaSemana,
} from './padroes.ts';

const [transp] = GRUPOS_CORTE;
let seq = 0;
const uber = (data: string, v: number): Transacao => ({ data, tipo: 'Pagamento com cartão Visa DL*UberRides', ref: `CARTAO-x-${seq}`, valor: -v, saldo: 0, seq: seq++ });

// datas
assert.equal(diaDaSemana('2026-10-05'), 0); // segunda
assert.equal(inicioDaSemana('2026-10-11'), '2026-10-05'); // domingo
assert.equal(somarDias('2026-12-30', 3), '2027-01-02');
assert.equal(primeiraSemanaDoPlano('2026-10'), '2026-10-05'); // 1/10 é quinta
assert.equal(primeiraSemanaDoPlano('2026-06'), '2026-06-01'); // já é segunda

// 12 semanas de histórico (13/07 a 04/10): semana solta (>=100) no sábado, as outras na terça
const hist = [100, 40, 150, 30, 160, 50, 170, 40, 140, 60, 150, 30];
const base: Transacao[] = hist.map((v, i) => uber(somarDias('2026-07-13', i * 7 + (v >= 100 ? 5 : 1)), v));
base.push(uber('2026-10-04', 0)); // fatura importada até o fim da 12ª semana (sem gasto nesse dia)
const monta = (plano: Array<[string, number]>) => classificarExtrato([...base, ...plano.map(([d, v]) => uber(d, v))]);

const semanas = semanasFechadas(monta([]), transp, '2026-10-05');
assert.equal(semanas.length, 12);
assert.deepEqual(semanas.map((s) => s.total), hist);
assert.equal(coberturaAte(monta([])), '2026-10-04');
// semana sem fatura importada NÃO vira semana zerada: com dados só até 05/10, a semana de 05 a 11/10 fica de fora
assert.equal(semanasFechadas(monta([['2026-10-06', 10]]), transp, '2026-10-19').length, 12);
assert.equal(semanasFechadas(monta([['2026-10-06', 10], ['2026-10-11', 1]]), transp, '2026-10-19').length, 13);

// perfil: mediana 80, contida 35 (terço inferior), solta 155 (terço superior)
const perfil = perfilSemanal(semanas)!;
assert.equal(perfil.mediana, 80);
assert.equal(perfil.contida, 35);
assert.equal(perfil.solta, 155);
assert.equal(perfilSemanal(semanas.slice(0, 7)), null); // poucas semanas: sem padrão
assert.equal(tipoDaSemana(30, perfil), 'contida');
assert.equal(tipoDaSemana(150, perfil), 'solta');
assert.equal(tipoDaSemana(80, perfil), 'media');

// alvo por nível: desce até o piso (corte máximo da configuração = 30% da mediana = 56)
assert.equal(alvoDoNivel(perfil, 0), 80);
assert.equal(alvoDoNivel(perfil, 1), 65);
assert.equal(alvoDoNivel(perfil, 3), 56);

// semana boa seguida de outra boa: sobe de nível. Hoje = quarta 21/10, já gastou 50 na semana
const bom = analisarPadroes(monta([['2026-10-06', 60], ['2026-10-13', 70], ['2026-10-19', 20], ['2026-10-20', 30]]), transp, '2026-10', '2026-10-21')!;
assert.equal(bom.plano.semanasNoPlano, 2);
assert.equal(bom.plano.nivel, 1);
assert.equal(bom.plano.alvo, 65);
assert.equal(bom.plano.compensacao, 0);
assert.equal(bom.atual.diaIndice, 2);
assert.equal(bom.atual.gasto, 50);
assert.equal(bom.atual.restante, 15);
// padrões: o gasto solto cai no sábado; depois de semana contida, 2 de 3 vezes veio solta; depois de solta, nunca
assert.equal(bom.diaMaisSolto, 5);
assert.equal(bom.dias[5], 78);
assert.deepEqual(bom.transicao.aposContida, { amostra: 3, pSolta: 67 });
assert.deepEqual(bom.transicao.aposSolta, { amostra: 4, pSolta: 0 });

// uma semana solta isolada NÃO muda o nível; só compensa parte do excesso na seguinte (50% do excesso, máx. 20% do alvo)
const solta1 = analisarPadroes(monta([['2026-10-11', 200]]), transp, '2026-10', '2026-10-14')!;
assert.equal(solta1.plano.nivel, 0);
assert.equal(solta1.plano.compensacao, 16); // min((200-80)*0,5 = 60, 80*0,2 = 16)
assert.equal(solta1.plano.alvoEfetivo, 64);

// duas estouradas seguidas no nível 1 relaxam para o nível 0; boa semana zera a compensação
const p = perfil;
const sem = (total: number) => ({ inicio: 'x', total, porDia: [0, 0, 0, 0, 0, 0, 0] });
assert.equal(estadoDoPlano([sem(60), sem(60)], p).nivel, 1);
assert.equal(estadoDoPlano([sem(60), sem(60), sem(200), sem(200)], p).nivel, 0);
assert.equal(estadoDoPlano([sem(60), sem(60), sem(200), sem(10)], p).compensacao, 0);
assert.equal(estadoDoPlano([], p).nivel, 0);

// ritmo da semana em andamento: quarta com 50 gastos é ritmo de semana contida? (contida típica ~ 20 até quarta)
assert.ok(['contido', 'medio', 'solto'].includes(bom.atual.ritmo));

// resumo para o economista: só percentuais e nomes de dia
const resumo = resumoPadroesPct(monta([]), '2026-10', '2026-10-14');
assert.equal(resumo.length, 1); // iFood não tem semanas suficientes com gasto: sem padrão, não entra
assert.equal(resumo[0].dia_mais_solto, 'sábado');
assert.equal(resumo[0].semana_solta_gasta_a_mais_pct, 343); // (155-35)/35
assert.equal(resumo[0].chance_solta_apos_contida_pct, 67);
assert.ok(!/\d+[.,]\d{2}\b/.test(JSON.stringify(resumo)), 'nenhum valor em reais no resumo');

console.log('padroes: ok');
