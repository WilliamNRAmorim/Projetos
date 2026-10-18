// Rodar: node src/exportar.test.ts. Fixtures FICTÍCIOS.
import assert from 'node:assert/strict';
import { PERFIL_VAZIO, perfilParaNumeros } from './metas.ts';
import { type Transacao } from './mp/extrato.ts';
import { descricaoCartao, descricaoExport, limparTexto, montarExport } from './exportar.ts';
import { classificarExtrato } from './mp/extrato.ts';

let seq = 0;
const tx = (data: string, tipo: string, valor: number, ref = `r${seq}`): Transacao => ({ data, tipo, ref, valor, saldo: 0, seq: seq++ });
const trans: Transacao[] = [
  tx('2026-08-05', 'Pix recebido Empresa Alfa Ltda', 3000),
  tx('2026-08-10', 'Pix enviado Maria da Silva Souza', -150),
  tx('2026-08-12', 'Pagamento com QR Pix Ifood Restaurante', -60),
  tx('2026-08-15', 'Pagamento com cartão Visa MP*JOAOTESTESILVA', -30, 'CARTAO-2026-08-2026-08-15-30.00-1'),
  tx('2026-08-16', 'Pagamento com cartão Visa DL*UberRides', -25, 'CARTAO-2026-08-2026-08-16-25.00-1'),
  tx('2026-09-05', 'Pix recebido 123.456.789-09', 3000),
  tx('2026-09-06', 'Pagamento de fatura Cartão de crédito', -55),
  tx('2026-09-09', 'Pagamento com QR Pix Fulano 98765432101 teste@exemplo.com', -20),
  tx('2026-10-02', 'Pagamento com QR Pix Ifood Restaurante', -40),
  tx('2026-10-03', 'Pix enviado Joao Tim Pereira', -10), // nome com palavra-chave de telefonia
  tx('2026-10-04', 'Pagamento com QR Pix Beltrano Oliveira Neto', -15), // QR Pix a pessoa física
  tx('2026-10-05', 'Pagamento com QR Pix - cancelado Cicrano de Tal', 15), // estorno
  tx('2026-10-06', 'Transferência Pix recebida Fulana Pagadora', 80),
];
const perfil = perfilParaNumeros({ ...PERFIL_VAZIO, salario: '3.000,00', diaSalario: '5', cofrinho: '1.500,00' });
const texto = montarExport({ hoje: new Date(2026, 9, 18), perfil, trans, meuNome: 'Joao Teste Silva', tetos: { 'Comida/delivery': 200 }, inicioCorte: '2026-10', basesCorte: {} });

// estrutura
assert.ok(texto.startsWith('# Exportação do FinAgent para o Claude'));
for (const t of ['## Como usar', '## Perfil financeiro', '## Gastos por mês', '## Orçamento de 2026-10', '## Metas e projeções', '## Corte de gastos', '## Transações classificadas']) {
  assert.ok(texto.includes(t), t);
}
assert.ok(texto.includes('R$ 3.000,00'));
assert.ok(texto.includes('R$ 1.500,00'));

// privacidade: nome de pessoa, nome do usuário, CPF, e-mail e sequências longas não saem
assert.ok(!texto.includes('Maria da Silva'), 'nome de pessoa em Pix');
assert.ok(!/joao|teste silva/i.test(texto.replace(/teste@exemplo/gi, '')), 'nome do usuário');
assert.ok(!texto.includes('123.456.789-09') && !texto.includes('98765432101'), 'CPF/sequência longa');
assert.ok(!texto.includes('teste@exemplo.com'), 'e-mail');
assert.ok(!texto.includes('Empresa Alfa'), 'nome de quem enviou Pix');
for (const nomePessoa of ['Joao Tim', 'Pereira', 'Beltrano', 'Oliveira', 'Cicrano', 'Fulana', 'Pagadora', 'Fulano']) assert.ok(!texto.includes(nomePessoa), `vazou ${nomePessoa}`);
assert.ok(!/gemini|mercadopago|brapi|access token/i.test(texto.replace(/mercado pago/gi, '')), 'chaves/serviços de chave');
// lojas ficam
assert.ok(/ifood/i.test(texto));
assert.ok(/uberrides/i.test(texto));
assert.ok(texto.includes('Pix para pessoa'));
// o pagamento da fatura de set quita a fatura de ago (importada): vira interno, e as compras de ago contam como gasto
assert.ok(/Movimento interno/.test(texto));

// funções
const l = classificarExtrato(trans, 'Joao Teste Silva');
assert.equal(descricaoExport(l[1], 'Joao Teste Silva'), 'Pix para pessoa');
assert.equal(limparTexto('MP*JOAOTESTESILVA', 'Joao Teste Silva'), 'MP*eu'); // nome colado vira um "eu"
assert.equal(limparTexto('MP*WILLIAMAMORIM', 'William Nathan Ribeiro de Amorim'), 'MP*eu'); // primeiro + último colados
assert.equal(limparTexto('Pix JOÃO Silva', 'João Silva'), 'Pix eu eu'); // acento no nome e no texto
assert.equal(limparTexto('Pix Joao', 'João Silva'), 'Pix eu'); // acento só no nome
assert.equal(limparTexto('Banana Mariana', 'Ana Souza'), 'Banana Mariana'); // parte do nome dentro de outra palavra não é mascarada
assert.equal(limparTexto('Loja X', 'Jo(a)o *+ [Silva'), 'Loja X'); // caracteres especiais no nome não quebram
assert.equal(descricaoExport(l[l.length - 4], 'Joao Teste Silva'), 'Pix enviado (Telefonia)');
assert.equal(descricaoExport(l[l.length - 3], 'Joao Teste Silva'), 'Pagamento QR Pix (estabelecimento ou pessoa)');
assert.equal(descricaoExport(l[l.length - 2], 'Joao Teste Silva'), 'Estorno/cancelamento');
assert.equal(limparTexto('CPF 123.456.789-09', ''), 'CPF (removido)');

// descrições do cartão: pessoa física some, marca fica
assert.equal(descricaoCartao('DL*UberRides', ''), 'DL*UberRides');
assert.equal(descricaoCartao('MP*CAUANBRIAN', ''), 'Mercado Pago (vendedor)');
assert.equal(descricaoCartao('IFD*WALTER LUCAS BALIE', ''), 'iFood (restaurante)');
assert.equal(descricaoCartao('99Food *Burger Grill bg', ''), '99Food (restaurante)');
assert.equal(descricaoCartao('Wellhub Raul Cesar Couto', ''), 'Wellhub (…)');
assert.equal(descricaoCartao('Steam Parcela 1 de 3', ''), 'Steam Parcela 1 de 3'); // tem número: mantém
assert.equal(descricaoCartao('MERCADOLIVRE*BLACKARROW', ''), 'Mercado Livre (vendedor)');

// sem dados nenhum: não quebra
const vazio = montarExport({ hoje: new Date(2026, 9, 18), perfil: perfilParaNumeros(PERFIL_VAZIO), trans: [], meuNome: '', tetos: {}, inicioCorte: null, basesCorte: {} });
assert.ok(vazio.includes('sem extrato'));

console.log('exportar: ok');
