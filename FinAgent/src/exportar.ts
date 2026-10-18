// Export para o William entregar ao Claude (economista): tudo que o app tem e aprendeu, em Markdown. Função pura.
// NUNCA entram: chaves de API, CPF, nome do usuário. Nomes de pessoas em Pix viram "pessoa". Lojas ficam (a análise precisa delas).
import { CORTE_DEGRAUS_PCT } from './metasConfig.ts';
import { metasDeCorte, type BasesCorte } from './cortes.ts';
import { CAT, PALAVRAS_GASTO, PREFIXOS, contemPalavra, ehCompraCartao, norm } from './mp/categorias.ts';
import { classificarExtrato, mesDe, mesesDisponiveis, saldoFinal, totaisMes, type Lancamento, type RegrasUsuario, type Transacao } from './mp/extrato.ts';
import { linhasOrcamento, type Tetos } from './gastos/gastos.ts';
import {
  comprometidoDoMes, faixaLimite, livreAteSalario, mediaGastoMensal, mesesDeReserva, usoLimite, type PerfilNum,
} from './metas.ts';
import { DIAS_SEMANA, analisarTodos, dataLocal } from './padroes.ts';
import { mediaLiquidoMensal, projetarConta } from './simulador/calc.ts';

export type EntradaExport = {
  hoje: Date;
  perfil: PerfilNum;
  trans: Transacao[];
  meuNome: string; // só para classificar e para mascarar; nunca sai no texto
  regras?: RegrasUsuario;
  tetos: Tetos;
  inicioCorte: string | null;
  basesCorte: BasesCorte;
};

const brl = (v: number | null | undefined) =>
  v === null || v === undefined || !Number.isFinite(v) ? 'não informado' : `R$ ${v.toFixed(2).replace('.', ',').replace(/\B(?=(\d{3})+(?!\d))/g, '.')}`;
const pct = (v: number | null | undefined) => (v === null || v === undefined ? 'n/d' : `${String(Math.round(v * 10) / 10).replace('.', ',')}%`);
const dataBR = (d: string) => `${d.slice(8)}/${d.slice(5, 7)}/${d.slice(0, 4)}`;
const celula = (t: string) => t.replace(/\|/g, '/').replace(/\s+/g, ' ').trim();

const semAcento = (t: string) => t.normalize('NFD').replace(/[̀-ͯ]/g, '');
const escapar = (t: string) => t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

/** Padrões do nome do usuário: partes isoladas (3+ letras, palavra inteira) e junções de partes coladas ("WILLIAMAMORIM"). */
function padroesDoNome(meuNome: string): RegExp[] {
  const partes = semAcento(meuNome).toLowerCase().split(/\s+/).filter((x) => x.length > 2).slice(0, 6);
  const juntas: string[] = [];
  for (let m = 1; m < 1 << partes.length; m++) {
    const sel = partes.filter((_, i) => m & (1 << i));
    if (sel.length >= 2) juntas.push(sel.join(''));
  }
  juntas.sort((x, y) => y.length - x.length);
  const out = juntas.map((j) => new RegExp(escapar(j), 'gi'));
  for (const parte of partes) out.push(new RegExp(`(?<![a-z0-9])${escapar(parte)}(?![a-z0-9])`, 'gi'));
  return out;
}

/** Tira CPF/CNPJ/e-mail/sequências longas e o nome do usuário (com ou sem acento, partes coladas) do texto livre. */
export function limparTexto(texto: string, meuNome: string): string {
  let t = semAcento(texto)
    .replace(/\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b/g, '(removido)')
    .replace(/\b\d{2}\.?\d{3}\.?\d{3}\/?\d{4}-?\d{2}\b/g, '(removido)')
    .replace(/[\w.+-]+@[\w-]+\.[\w.-]+/g, '(removido)')
    .replace(/\b\d{9,}\b/g, '(removido)');
  for (const re of padroesDoNome(meuNome)) t = t.replace(re, 'eu');
  return t;
}

/**
 * Estabelecimento da fatura do cartão, sem nomes de pessoas: vendedores de marketplace e restaurantes de app costumam ser
 * pessoa física ("MP*FULANO", "IFD*NOME DO RESTAURANTE"), então viram a marca. Descrição sem "*" com 3+ palavras e sem número
 * (ex.: "Wellhub Fulano de Tal") fica só com a primeira palavra.
 */
export function descricaoCartao(descricao: string, meuNome: string): string {
  const t = limparTexto(descricao, meuNome).trim();
  if (/^MP\s*\*/i.test(t)) return 'Mercado Pago (vendedor)';
  if (/^MERCADOLIVRE\s*\*/i.test(t)) return 'Mercado Livre (vendedor)';
  if (/^IFD\s*\*/i.test(t)) return 'iFood (restaurante)';
  if (/^99\s*Food\s*\*/i.test(t)) return '99Food (restaurante)';
  const palavras = t.split(/\s+/);
  if (!t.includes('*') && !/\d/.test(t) && palavras.length >= 3) return `${palavras[0]} (…)`;
  return t;
}

const comecaCom = (n: string, prefixos: string[]) => prefixos.some((p) => n.startsWith(p));
const PIX_ENTRE_PESSOAS = [...PREFIXOS.pixEnviado, ...PREFIXOS.entrada.filter((p) => p.includes('pix') || p.includes('transferencia'))];

/**
 * Descrição segura, decidida pelo TIPO do lançamento (não pela categoria final, que o usuário pode mudar):
 * - rendimento, reserva, fatura e empréstimo não trazem contraparte: o texto original fica;
 * - compra do cartão: o texto da fatura (estabelecimento), sem o nome do usuário;
 * - Pix enviado/recebido e transferências: nunca o nome, só a categoria;
 * - pagamento por QR Pix: só a marca conhecida (iFood, Uber...), senão genérico (pode ser pessoa física);
 * - qualquer outra coisa: genérico.
 */
export function descricaoExport(l: Lancamento, meuNome: string): string {
  const n = norm(l.tipo);
  if (comecaCom(n, [...PREFIXOS.rendimento, ...PREFIXOS.interno, ...PREFIXOS.fatura, ...PREFIXOS.emprestimo])) return celula(limparTexto(l.tipo, meuNome));
  if (ehCompraCartao(l.tipo)) return celula(descricaoCartao(l.tipo.replace(/^pagamento com cart[aã]o visa /i, ''), meuNome));
  if (l.categoria === CAT.SAIDA_OUTRA_CONTA) return 'Saída para sua outra conta';
  if (l.categoria === CAT.OUTRA_CONTA) return 'Entrada da sua outra conta';
  if (comecaCom(n, PREFIXOS.estorno)) return 'Estorno/cancelamento';
  if (comecaCom(n, PIX_ENTRE_PESSOAS)) {
    const entrada = comecaCom(n, PREFIXOS.entrada);
    if (entrada) return 'Entrada (Pix/transferência recebida)';
    return l.categoria === CAT.PIX_PESSOAS ? 'Pix para pessoa' : `Pix enviado (${l.categoria})`;
  }
  if (comecaCom(n, PREFIXOS.pagamento)) {
    const marca = PALAVRAS_GASTO.flatMap(([, palavras]) => palavras).find((w) => contemPalavra(norm(l.contraparte), w));
    return marca ? `Pagamento QR Pix (${marca})` : 'Pagamento QR Pix (estabelecimento ou pessoa)';
  }
  return 'Outro lançamento';
}

function secaoPerfil(p: PerfilNum): string[] {
  const comp = comprometidoDoMes(p);
  const uso = usoLimite(p.limiteCartao, p.faturaAberta);
  return [
    '## Perfil financeiro (informado por mim no app)',
    `- Salário: ${brl(p.salario)}${p.diaSalario ? `, cai no dia ${p.diaSalario}` : ''}`,
    `- Parcela do aparelho: ${brl(p.parcela)}${p.diaParcela ? `, dia ${p.diaParcela}` : ''}; parcelas restantes: ${p.parcelasRestantes ?? 'n/d'}${p.parcelasMin !== null || p.parcelasMax !== null ? ` (faixa ${p.parcelasMin ?? '?'} a ${p.parcelasMax ?? '?'})` : ''}`,
    `- Cofrinho (reserva): ${brl(p.cofrinho)}; separado para o aparelho: ${brl(p.separadoAparelho)}`,
    `- Limite do cartão: ${brl(p.limiteCartao)}; fatura aberta: ${brl(p.faturaAberta)}${uso !== null ? ` (${pct(uso)} do limite, faixa ${faixaLimite(uso)})` : ''}`,
    `- Fechamento da fatura: dia ${p.diaFechamento ?? 'n/d'}; vencimento: dia ${p.diaVencimento ?? 'n/d'}`,
    `- Comprometido no mês (parcela + fatura): ${brl(comp.total)}${comp.pctSalario !== null ? ` (${pct(comp.pctSalario)} do salário)` : ''}`,
    '',
  ];
}

function secaoMeses(lancs: Lancamento[], salario: number | null): string[] {
  const meses = mesesDisponiveis(lancs).sort().reverse();
  const out = ['## Gastos por mês (por competência: compras do cartão contam no mês da compra)', '', '| Mês | Entradas | Gastos | Fatura paga (caixa) | Variação do gasto | % do salário | Principais categorias |', '|---|---|---|---|---|---|---|'];
  for (const m of meses) {
    const t = totaisMes(lancs, m);
    const cats = t.porCategoria.slice(0, 4).map((c) => `${celula(c.nome)} ${brl(c.total)}`).join('; ');
    out.push(`| ${m} | ${brl(t.entradas)} | ${brl(t.gastos)} | ${brl(t.fatura)} | ${pct(t.variacaoGasto)} | ${salario ? pct((t.gastos / salario) * 100) : 'n/d'} | ${cats || '-'} |`);
  }
  out.push('', 'Observação: o pagamento da fatura só aparece como "fatura paga" quando as compras daquela fatura NÃO foram importadas; quando foram, as compras já estão em "Gastos" e o pagamento é só saída de caixa.', '');
  return out;
}

function secaoOrcamento(lancs: Lancamento[], tetos: Tetos, mes: string): string[] {
  const o = linhasOrcamento(lancs, mes, tetos);
  const out = [`## Orçamento de ${mes}`, ''];
  if (o.linhas.length === 0) return [...out, 'Sem dados.', ''];
  out.push('| Categoria | Gasto | Teto | % do teto |', '|---|---|---|---|');
  for (const l of o.linhas) out.push(`| ${celula(l.categoria)} | ${brl(l.gasto)} | ${l.teto === null ? 'sem teto' : brl(l.teto)} | ${pct(l.pct)} |`);
  out.push('');
  return out;
}

function secaoMetas(e: EntradaExport, lancs: Lancamento[]): string[] {
  const { perfil: p, trans, meuNome, regras, hoje } = e;
  const saldo = saldoFinal(trans);
  const gasto = mediaGastoMensal(trans, meuNome, hoje, undefined, regras);
  const livre = saldo ? livreAteSalario(saldo.saldo, p, hoje) : null;
  const liq = mediaLiquidoMensal(trans, meuNome, hoje, undefined, regras);
  const proj = liq && saldo ? projetarConta(saldo.saldo, liq, hoje, p.diaSalario) : null;
  const out = ['## Metas e projeções calculadas pelo app', ''];
  out.push(`- Saldo da conta no extrato: ${saldo ? `${brl(saldo.saldo)} em ${dataBR(saldo.data)}` : 'sem extrato'}`);
  out.push(`- Gasto médio mensal (meses fechados, gastos + fatura): ${gasto ? `${brl(gasto.media)}${gasto.parcial ? ' (estimativa, mês incompleto)' : ''}` : 'n/d'}`);
  out.push(`- Meses de reserva que o Cofrinho cobre: ${mesesDeReserva(p.cofrinho, gasto?.media ?? null) ?? 'n/d'} (meta do app: 3 a 6)`);
  out.push(`- Livre até o salário: ${livre ? `${brl(livre.valor)}${livre.porDia !== null ? `, ${brl(livre.porDia)} por dia (${livre.dias} dias)` : ''}` : 'n/d'}`);
  out.push(`- Líquido médio mensal em caixa (entradas - gastos na conta - fatura paga): ${liq ? brl(liq.media) : 'n/d'}`);
  if (proj) out.push(`- Projeção da conta: fim do mês ${brl(proj.fimDoMes)}; dezembro ${brl(proj.dezembro)} (sem o Cofrinho; estimativa, não promessa)`);
  out.push('');
  return out;
}

function secaoCorte(e: EntradaExport, lancs: Lancamento[]): string[] {
  const out = ['## Corte de gastos e padrão semanal (Uber/99 e iFood/99Food)', ''];
  if (!e.inicioCorte) return [...out, 'Plano de corte ainda não iniciado.', ''];
  const mes = `${e.hoje.getFullYear()}-${String(e.hoje.getMonth() + 1).padStart(2, '0')}`;
  out.push(`Plano iniciado em ${e.inicioCorte}; corte mensal ${CORTE_DEGRAUS_PCT.map((d) => `-${d}%`).join(', ')} sobre a média dos 3 meses anteriores (base congelada).`, '');
  for (const m of metasDeCorte(lancs, e.inicioCorte, mes, e.basesCorte)) {
    out.push(`- **${m.grupo.nome}**: base ${brl(m.base)}, teto do mês ${brl(m.teto)} (-${m.degrau}%), gasto no mês ${brl(m.gasto)}${m.pct !== null ? ` (${pct(m.pct)} do teto)` : ''}.`);
  }
  out.push('', 'Padrão aprendido (semanas de segunda a domingo, últimas 13 antes do plano):', '');
  const padroes = analisarTodos(lancs, e.inicioCorte, dataLocal(e.hoje));
  if (padroes.length === 0) out.push('Ainda sem histórico suficiente para aprender o padrão.');
  for (const a of padroes) {
    out.push(`- **${a.grupo.nome}**: semana típica ${brl(a.perfil.mediana)}; contida ~${brl(a.perfil.contida)}; solta ~${brl(a.perfil.solta)}; dia que mais solta: ${DIAS_SEMANA[a.diaMaisSolto]} (${a.dias[a.diaMaisSolto]}% do gasto).`);
    if (a.transicao.aposContida) out.push(`  - Depois de semana contida, a próxima é solta em ${a.transicao.aposContida.pSolta}% das vezes (${a.transicao.aposContida.amostra} casos).`);
    if (a.transicao.aposSolta) out.push(`  - Depois de semana solta, a próxima é solta em ${a.transicao.aposSolta.pSolta}% das vezes (${a.transicao.aposSolta.amostra} casos).`);
    out.push(`  - Plano semanal: nível ${a.plano.nivel} de ${CORTE_DEGRAUS_PCT.length}, alvo ${brl(a.plano.alvoEfetivo)}; semana atual: gastou ${brl(a.atual.gasto)} até hoje (ritmo ${a.atual.ritmo}).`);
  }
  out.push('');
  return out;
}

function secaoTransacoes(lancs: Lancamento[], meuNome: string): string[] {
  const out = ['## Transações classificadas (mais recentes primeiro)', '', 'Valores negativos = saída. "Fatura do cartão" e "Movimento interno" não são gasto. Compras de cartão aparecem como "Pagamento com cartão Visa ...".', '', '| Data | Categoria | Descrição | Valor |', '|---|---|---|---|'];
  const ordem = [...lancs].sort((a, b) => b.data.localeCompare(a.data) || b.seq - a.seq);
  let mes = '';
  for (const l of ordem) {
    if (mesDe(l.data) !== mes) {
      mes = mesDe(l.data);
      out.push(`| **${mes}** | | | |`);
    }
    const cat = l.excluida ? `${l.categoria} (anulada)` : l.categoria;
    const desc = descricaoExport(l, meuNome);
    out.push(`| ${dataBR(l.data)} | ${celula(cat)} | ${desc} | ${l.valor.toFixed(2).replace('.', ',')} |`);
  }
  out.push('');
  return out;
}

export function montarExport(e: EntradaExport): string {
  const lancs = classificarExtrato(e.trans, e.meuNome, e.regras);
  const meses = mesesDisponiveis(e.trans).sort();
  const mesAtual = `${e.hoje.getFullYear()}-${String(e.hoje.getMonth() + 1).padStart(2, '0')}`;
  const mesOrc = meses.includes(mesAtual) ? mesAtual : meses[meses.length - 1] ?? mesAtual;
  const linhas = [
    '# Exportação do FinAgent para o Claude (economista pessoal)',
    '',
    `Gerado em ${dataBR(dataLocal(e.hoje))}. Período do extrato: ${meses.length > 0 ? `${meses[0]} a ${meses[meses.length - 1]}` : 'sem extrato'}; ${e.trans.length} lançamentos.`,
    '',
    '## Como usar (instruções para o Claude)',
    '- Você é meu economista pessoal. Analise estes dados, aponte padrões, riscos e oportunidades de economia, e me dê opinião direta e prática em português.',
    '- Sou mais compulsivo em algumas semanas e mais contido em outras; considere esse ritmo, não só médias. Não me puna por uma semana solta: ajude a entender gatilhos e a reduzir aos poucos.',
    '- Os números vêm do app. Meses recentes podem estar incompletos (a fatura do cartão do mês corrente só entra quando fecha). Diga quando algo depender disso.',
    '- Isto é educativo, não é consultoria de investimentos registrada. Não invente dados que não estão aqui; peça o que faltar.',
    '- Privacidade: nomes de pessoas foram trocados por "pessoa"; não há chaves, CPF nem meu nome.',
    '',
    ...secaoPerfil(e.perfil),
    ...secaoMeses(lancs, e.perfil.salario),
    ...secaoOrcamento(lancs, e.tetos, mesOrc),
    ...secaoMetas(e, lancs),
    ...secaoCorte(e, lancs),
    ...secaoTransacoes(lancs, e.meuNome),
  ];
  return linhas.join('\n');
}
