// Resumo seguro para enviar à IA: SOMENTE agregados, nunca nomes de contrapartes nem descrições.
import type { ResumoMetas } from '../metas.ts';
import type { TotaisExtrato } from './extrato.ts';

export function resumoParaIA(totais: TotaisExtrato, metas?: ResumoMetas): string {
  const cats = totais.porCategoria.map((c) => `${c.nome}: ${c.total.toFixed(2)}`).join('; ');
  const var_ = totais.variacaoGasto === null ? 'sem mês anterior' : `${totais.variacaoGasto}% vs mês anterior`;
  const partes = [
    `Mês ${totais.mes}`,
    `entradas ${totais.entradas.toFixed(2)}`,
    `rendimentos ${totais.rendimentos.toFixed(2)}`,
    `gastos ${totais.gastos.toFixed(2)} (${var_})`,
    `fatura do cartão ${totais.fatura.toFixed(2)}`,
    `líquido para a reserva ${totais.reservaLiquida.toFixed(2)}`,
    `gastos por categoria: ${cats || 'nenhum'}`,
  ];
  if (metas) {
    if (metas.salario !== null) partes.push(`salário ${metas.salario.toFixed(2)}`);
    if (metas.pctComprometido !== null) partes.push(`comprometido ${metas.pctComprometido}% do salário`);
    if (metas.pctLimite !== null) partes.push(`cartão usando ${metas.pctLimite}% do limite`);
    if (metas.mesesReserva !== null) partes.push(`reserva cobre ${metas.mesesReserva} meses de gasto`);
  }
  return partes.join(' | ');
}
