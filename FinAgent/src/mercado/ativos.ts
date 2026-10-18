import type { Ativo } from './tipos.ts';

export const WATCHLIST_PADRAO: Ativo[] = [
  { id: 'moeda:USD', tipo: 'moeda', codigo: 'USD', nome: 'Dólar' },
  { id: 'moeda:EUR', tipo: 'moeda', codigo: 'EUR', nome: 'Euro' },
  { id: 'cripto:bitcoin', tipo: 'cripto', codigo: 'bitcoin', nome: 'Bitcoin' },
  { id: 'cripto:ethereum', tipo: 'cripto', codigo: 'ethereum', nome: 'Ethereum' },
  { id: 'acao:BOVA11', tipo: 'acao', codigo: 'BOVA11', nome: 'BOVA11' },
  { id: 'acao:IVVB11', tipo: 'acao', codigo: 'IVVB11', nome: 'IVVB11' },
  { id: 'acao:PETR4', tipo: 'acao', codigo: 'PETR4', nome: 'PETR4' },
  { id: 'acao:VALE3', tipo: 'acao', codigo: 'VALE3', nome: 'VALE3' },
  { id: 'acao:ITUB4', tipo: 'acao', codigo: 'ITUB4', nome: 'ITUB4' },
];

const CRIPTOS: Record<string, { id: string; nome: string }> = {
  BTC: { id: 'bitcoin', nome: 'Bitcoin' },
  ETH: { id: 'ethereum', nome: 'Ethereum' },
  SOL: { id: 'solana', nome: 'Solana' },
  ADA: { id: 'cardano', nome: 'Cardano' },
  XRP: { id: 'ripple', nome: 'XRP' },
  LTC: { id: 'litecoin', nome: 'Litecoin' },
  DOGE: { id: 'dogecoin', nome: 'Dogecoin' },
};
const MOEDAS: Record<string, string> = { USD: 'Dólar', EUR: 'Euro', GBP: 'Libra', ARS: 'Peso argentino', JPY: 'Iene', CAD: 'Dólar canadense', CHF: 'Franco suíço' };

/** Converte o que o usuário digitou (USD, btc, PETR4...) em Ativo, ou null. */
export function ativoDeEntrada(entrada: string): Ativo | null {
  const t = entrada.trim().toUpperCase().replace(/\.SA$/, '');
  if (CRIPTOS[t]) return { id: `cripto:${CRIPTOS[t].id}`, tipo: 'cripto', codigo: CRIPTOS[t].id, nome: CRIPTOS[t].nome };
  if (MOEDAS[t]) return { id: `moeda:${t}`, tipo: 'moeda', codigo: t, nome: MOEDAS[t] };
  if (/^[A-Z]{4}\d{1,2}$/.test(t)) return { id: `acao:${t}`, tipo: 'acao', codigo: t, nome: t };
  return null;
}
