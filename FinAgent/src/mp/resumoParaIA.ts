// Resumo seguro para enviar à IA: SOMENTE agregados, nunca nomes de contrapartes nem descrições.
import type { TotaisExtrato } from './extrato.ts';

export function resumoParaIA(totais: TotaisExtrato): string {
  const cats = totais.porCategoria.map((c) => `${c.nome}: ${c.total.toFixed(2)}`).join('; ');
  const var_ = totais.variacaoGasto === null ? 'sem mês anterior' : `${totais.variacaoGasto}% vs mês anterior`;
  return [
    `Mês ${totais.mes}`,
    `entradas ${totais.entradas.toFixed(2)}`,
    `rendimentos ${totais.rendimentos.toFixed(2)}`,
    `gastos ${totais.gastos.toFixed(2)} (${var_})`,
    `fatura do cartão ${totais.fatura.toFixed(2)}`,
    `líquido para a reserva ${totais.reservaLiquida.toFixed(2)}`,
    `gastos por categoria: ${cats || 'nenhum'}`,
  ].join(' | ');
}
