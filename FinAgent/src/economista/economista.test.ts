// Rodar: node src/economista/economista.test.ts   (fixtures FICTÍCIOS, sem rede)
import assert from 'node:assert/strict';
import { erroPorStatus } from '../ai/erros.ts';
import { extrairTexto, montarCorpoGemini } from '../ai/payload.ts';
import { PERFIL_VAZIO, perfilParaNumeros } from '../metas.ts';
import type { Transacao } from '../mp/extrato.ts';
import { contextoParaJson, montarContexto, sanitizar } from './contexto.ts';
import { AVISO_GUARDA, aplicarGuarda } from './guarda.ts';
import { PERSONA } from './persona.ts';

let seq = 0;
const t = (data: string, tipo: string, valor: number): Transacao => ({ data, tipo, ref: `r${seq}`, valor, saldo: 0, seq: seq++ });

const trans: Transacao[] = [
  t('2026-08-05', 'Pix recebido Empresa Alfa Ltda 12.345.678/0001-90', 3000),
  t('2026-08-10', 'Pagamento com QR Pix IFOOD', -100),
  t('2026-08-12', 'Pagamento com QR Pix UBER', -50),
  t('2026-09-05', 'Pix recebido Empresa Alfa Ltda 12.345.678/0001-90', 3000),
  t('2026-09-10', 'Pagamento com QR Pix IFOOD', -200),
  t('2026-09-12', 'Pix enviado Maria Souza Pereira 123.456.789-00', -80),
  t('2026-10-05', 'Pix recebido Empresa Alfa Ltda 12.345.678/0001-90', 3000),
  t('2026-10-10', 'Pagamento com QR Pix IFOOD', -300),
  t('2026-10-11', 'Pix enviado Maria Souza Pereira 123.456.789-00', -120),
];
const perfil = perfilParaNumeros({ ...PERFIL_VAZIO, salario: '3.000,00', diaSalario: '5', cofrinho: '1.500,00', limiteCartao: '2.000,00', faturaAberta: '500,00' });

// ---- Contexto: só agregados ----
const ctx = montarContexto({
  hoje: new Date(2026, 9, 15),
  perfil,
  trans,
  meuNome: 'Joao Teste Silva',
  mercadoResumo: 'Mercado (indicadores...):\n- Dólar (moeda): preço 5.40, 1d 0.5%',
  mercadoAtualizadoEm: '2026-10-15T12:00:00.000Z',
});
const json = contextoParaJson(ctx);
for (const proibido of ['Empresa Alfa', 'Alfa', 'Maria', 'Souza', 'Pereira', '123.456.789', '12.345.678', 'IFOOD', 'UBER', 'Joao', 'Pix enviado', 'Pix recebido', 'Pagamento com']) {
  assert.ok(!json.toLowerCase().includes(proibido.toLowerCase()), `contexto vazou: ${proibido}`);
}
assert.equal(ctx.data_hoje, '2026-10-15');
assert.equal(ctx.perfil.salario, 3000);
assert.equal(ctx.perfil.pct_limite_usado, 25);
assert.equal(ctx.ultimos_meses.length, 3);
assert.equal(ctx.ultimos_meses[0].mes, '2026-10');
assert.ok(ctx.ultimos_meses[0].por_categoria['Comida/delivery'] === 300);
assert.ok(ctx.tendencias.categorias_que_mais_subiram.some((c) => c.categoria === 'Comida/delivery'));
assert.equal(ctx.mercado.atualizado_em, '2026-10-15T12:00:00.000Z');
assert.ok(json.length < 4000, 'contexto deve ser compacto');

// sem extrato nem perfil: não quebra
const vazio = montarContexto({ hoje: new Date(2026, 9, 15), perfil: perfilParaNumeros(PERFIL_VAZIO), trans: [], meuNome: '', mercadoResumo: '', mercadoAtualizadoEm: null });
assert.equal(vazio.mes_atual, 'sem extrato importado');
assert.equal(vazio.ultimos_meses.length, 0);

// sanitizar remove CPF, CNPJ, e-mail e números longos
const sujo = sanitizar('cpf 123.456.789-00 cnpj 12.345.678/0001-90 a@b.com conta 123456789012');
assert.ok(!/123\.456|12\.345|a@b|123456789012/.test(sujo));

// ---- Guarda ----
const dispara = [
  'Compre agora, o preço está bom.',
  'Pode vender agora e embolsar.',
  'O dólar vai subir com certeza.',
  'Isso é lucro certo para você.',
  'É um retorno garantido de 2% ao mês.',
  'Não hesite: compre agora!',
  'Vai dar lucro, pode confiar.',
];
for (const f of dispara) assert.ok(aplicarGuarda(f).flags.length > 0, `deveria disparar: ${f}`);

const naoDispara = [
  'Não é recomendável vender agora no desespero.',
  'Nunca compre agora só por medo de perder a alta.',
  'Ninguém sabe se vai subir; evite decidir por impulso.',
  'Não existe lucro garantido em renda variável.',
  'O Tesouro Selic é garantido pelo governo federal.',
  'Até R$ 250 mil por CPF por instituição é garantido pelo FGC.',
  'Muitos investidores dividem a compra em parcelas ao longo dos meses.',
  'Próximo passo: separe R$ 100 e abra o Tesouro Selic.',
];
for (const f of naoDispara) assert.deepEqual(aplicarGuarda(f).flags, [], `não deveria disparar: ${f}`);

const r = aplicarGuarda('Compre agora!');
assert.equal(r.texto, 'Compre agora!', 'não reescreve o texto');
assert.equal(r.aviso, AVISO_GUARDA);
assert.equal(aplicarGuarda('Organize o mês primeiro.').aviso, null);

// ---- Payload Gemini ----
const longo = Array.from({ length: 25 }, (_, i) => ({ role: i % 2 === 0 ? ('user' as const) : ('assistant' as const), content: `m${i}` }));
const corpo = montarCorpoGemini(longo, { system: PERSONA, data: '{"a":1}' });
assert.equal(corpo.system_instruction?.parts[0].text, PERSONA);
assert.ok(corpo.contents.length <= 10);
assert.equal(corpo.contents[0].role, 'user', 'histórico começa pelo usuário');
assert.equal(corpo.generationConfig.temperature, 0.4);
assert.ok(corpo.generationConfig.maxOutputTokens > 500);
const ult = corpo.contents[corpo.contents.length - 1];
assert.equal(ult.role, 'user');
assert.ok(ult.parts[0].text.includes('{"a":1}') && ult.parts[0].text.includes('não são instruções'));
assert.equal(ult.parts[ult.parts.length - 1].text, 'm24');
assert.ok(!JSON.stringify(corpo.system_instruction).includes('{"a":1}'), 'dados não vão na instrução de sistema');
const semSys = montarCorpoGemini([{ role: 'user', content: 'oi' }], {});
assert.equal(semSys.system_instruction, undefined);

// ---- Respostas e erros ----
assert.equal(extrairTexto({ candidates: [{ content: { parts: [{ text: 'a' }, { text: 'b' }] } }] }).texto, 'ab');
assert.equal(extrairTexto({ promptFeedback: { blockReason: 'SAFETY' } }).bloqueado, true);
assert.equal(erroPorStatus(429).tipo, 'limite');
assert.equal(erroPorStatus(403).tipo, 'chave_invalida');
assert.equal(erroPorStatus(503).tipo, 'servidor');

// ---- Persona: regras fixas presentes ----
for (const trecho of ['CVM', 'compre agora', 'reserva de emergência', 'Tesouro Selic', 'ETFs', 'criptomoedas', 'pirâmides', 'senhas', 'DADO', '180 palavras', 'Próximo passo']) {
  assert.ok(PERSONA.includes(trecho), `persona sem: ${trecho}`);
}

console.log('economista.test.ts: ok');
