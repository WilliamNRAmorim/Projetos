// Leitura educativa DETERMINÍSTICA (regras, não IA). Linguagem condicional.
// Regras duras: nunca instruir compra/venda, nunca prometer ganho, sempre incluir o aviso abaixo.
import type { Indicadores, TipoAtivo } from './tipos.ts';

export const AVISO_LEITURA = 'Indicador não prevê o futuro. Educativo, não é consultoria de investimentos.';

const pct = (n: number) => `${Math.abs(n).toFixed(1).replace('.', ',')}%`;

const RESERVA_FRASE = 'Antes de renda variável vem a reserva. ';
const RESERVA_PRIMEIRO: Record<TipoAtivo, string> = { moeda: '', cripto: RESERVA_FRASE, acao: RESERVA_FRASE };

const SUJEITO: Record<TipoAtivo, string> = { moeda: 'A cotação', cripto: 'O preço', acao: 'O preço' };

export function gerarLeitura(nome: string, tipo: TipoAtivo, ind: Indicadores | null): string {
  if (!ind || ind.pontos < 10) {
    return `Ainda não há histórico suficiente de ${nome} para calcular indicadores. ${RESERVA_PRIMEIRO[tipo]}${AVISO_LEITURA}`;
  }
  const partes: string[] = [];

  if (ind.mediaSerie != null) {
    const dif = (ind.preco / ind.mediaSerie - 1) * 100;
    const ref = `a média dos últimos ${Math.min(ind.pontos, 90)} dias`;
    if (Math.abs(dif) < 1) {
      partes.push(`${SUJEITO[tipo]} de ${nome} está próximo d${ref} (diferença de ${pct(dif)}).`);
    } else if (dif > 0) {
      partes.push(
        `${SUJEITO[tipo]} de ${nome} está ${pct(dif)} acima d${ref}. ` +
          (tipo === 'moeda'
            ? 'Quem precisa comprar a moeda costuma reduzir risco dividindo a compra em parcelas ao longo do tempo.'
            : 'Quem pensa em entrar costuma reduzir o risco de escolher um mau momento dividindo os aportes ao longo do tempo.'),
      );
    } else {
      partes.push(
        `${SUJEITO[tipo]} de ${nome} está ${pct(dif)} abaixo d${ref}. ` +
          'Estar abaixo da média pode indicar que o preço caiu recentemente, mas também pode refletir uma queda que continua; por isso muita gente prefere fracionar as decisões.',
      );
    }
  }

  if (ind.posicao != null && ind.minima90 != null && ind.maxima90 != null) {
    const p = Math.round(ind.posicao);
    const onde = p >= 80 ? 'perto da máxima' : p <= 20 ? 'perto da mínima' : 'no meio do intervalo';
    partes.push(`Em relação ao intervalo do período, está ${onde} (posição ${p}% entre a mínima e a máxima).`);
  }

  if (ind.tendencia !== 'indefinida') {
    const t =
      ind.tendencia === 'alta'
        ? 'O preço está acima das médias de 20 e 50 dias, com a média curta acima da longa: leitura de tendência de alta.'
        : ind.tendencia === 'baixa'
          ? 'O preço está abaixo das médias de 20 e 50 dias, com a média curta abaixo da longa: leitura de tendência de baixa.'
          : 'As médias de 20 e 50 dias não apontam uma direção clara: leitura lateral.';
    partes.push(t);
  }

  if (ind.rsi14 != null) {
    if (ind.rsi14 >= 70) partes.push(`O RSI(14) está em ${Math.round(ind.rsi14)}, região que costuma indicar alta esticada; isso pode se corrigir, mas também pode persistir.`);
    else if (ind.rsi14 <= 30) partes.push(`O RSI(14) está em ${Math.round(ind.rsi14)}, região que costuma indicar queda esticada; isso pode se reverter, mas também pode persistir.`);
  }

  if (ind.volatilidade != null) {
    const v = ind.volatilidade;
    const nivel = tipoVol(v);
    partes.push(`A oscilação diária recente é de cerca de ${v.toFixed(1).replace('.', ',')}% (${nivel}).`);
  }

  partes.push('Essa leitura muda se o preço romper a faixa recente ou se o cenário econômico mudar.');
  if (RESERVA_PRIMEIRO[tipo]) partes.push(RESERVA_PRIMEIRO[tipo].trim());
  partes.push(AVISO_LEITURA);
  return partes.join(' ');
}

function tipoVol(v: number): string {
  return v < 0.8 ? 'baixa' : v < 2 ? 'moderada' : 'alta';
}

export type ItemResumo = { nome: string; tipo: TipoAtivo; ind: Indicadores | null };

/** Texto vindo de API vai para o contexto da IA sem colchetes (não forja os delimitadores do bloco de dados). */
export const semColchetes = (t: string) => t.replace(/[[\]]/g, ' ').replace(/\s+/g, ' ').trim();

/** Agregados da watchlist, sem dados pessoais, para o Economista. */
export function montarResumo(itens: ItemResumo[]): string {
  const f = (n: number | null, d = 1) => (n == null ? 'n/d' : n.toFixed(d));
  const linhas = itens
    .filter((i) => i.ind)
    .map((i) => {
      const x = i.ind!;
      return `- ${semColchetes(i.nome)} (${i.tipo}): preço ${f(x.preco, 2)}, 1d ${f(x.var1d)}%, 7d ${f(x.var7d)}%, 30d ${f(x.var30d)}%, 90d ${f(x.var90d)}%, RSI ${f(x.rsi14, 0)}, posição no intervalo ${f(x.posicao, 0)}%, vol. diária ${f(x.volatilidade)}%, tendência ${x.tendencia}`;
    });
  if (!linhas.length) return 'Mercado: sem dados de mercado disponíveis.';
  return ['Mercado (indicadores da watchlist, sem dados pessoais; indicador não prevê o futuro):', ...linhas].join('\n');
}
