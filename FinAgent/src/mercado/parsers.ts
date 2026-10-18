// Parsers tolerantes das 3 fontes. Puros (sem rede). Retornam null/[] se o formato não bater.
import type { Cotacao, Ponto } from './tipos.ts';

const num = (v: unknown): number | null => {
  const n = typeof v === 'string' ? Number(v.replace(',', '.')) : typeof v === 'number' ? v : NaN;
  return Number.isFinite(n) ? n : null;
};

export const isoDia = (ms: number) => new Date(ms).toISOString().slice(0, 10);

/** Mantém o último valor de cada dia e ordena de forma crescente. */
export function normalizarSerie(pontos: Ponto[]): Ponto[] {
  const porDia = new Map<string, number>();
  for (const p of pontos.sort((a, b) => a.data.localeCompare(b.data))) porDia.set(p.data, p.fechamento);
  return [...porDia.entries()].map(([data, fechamento]) => ({ data, fechamento }));
}

/** AwesomeAPI /json/last/USD-BRL,EUR-BRL -> { 'USD-BRL': Cotacao } */
export function parseAwesomeLast(json: unknown): Record<string, Cotacao> {
  const out: Record<string, Cotacao> = {};
  if (!json || typeof json !== 'object') return out;
  for (const v of Object.values(json as Record<string, any>)) {
    const preco = num(v?.bid);
    if (preco == null || typeof v?.code !== 'string' || typeof v?.codein !== 'string') continue;
    out[`${v.code}-${v.codein}`] = { preco, variacaoDia: num(v?.pctChange) };
  }
  return out;
}

/** AwesomeAPI /json/daily/USD-BRL/90 (mais recente primeiro) -> série crescente. */
export function parseAwesomeDaily(json: unknown): Ponto[] {
  if (!Array.isArray(json)) return [];
  const pts: Ponto[] = [];
  for (const it of json) {
    const f = num(it?.bid);
    const ts = num(it?.timestamp);
    if (f == null || ts == null) continue;
    pts.push({ data: isoDia(ts * 1000), fechamento: f });
  }
  return normalizarSerie(pts);
}

/** CoinGecko simple/price -> { bitcoin: Cotacao } */
export function parseCoingeckoPreco(json: unknown): Record<string, Cotacao> {
  const out: Record<string, Cotacao> = {};
  if (!json || typeof json !== 'object') return out;
  for (const [id, v] of Object.entries(json as Record<string, any>)) {
    const preco = num(v?.brl);
    if (preco == null) continue;
    out[id] = { preco, variacaoDia: num(v?.brl_24h_change) };
  }
  return out;
}

/** CoinGecko market_chart: { prices: [[ms, preco], ...] } */
export function parseCoingeckoSerie(json: unknown): Ponto[] {
  const prices = (json as any)?.prices;
  if (!Array.isArray(prices)) return [];
  const pts: Ponto[] = [];
  for (const it of prices) {
    if (!Array.isArray(it)) continue;
    const ms = num(it[0]);
    const f = num(it[1]);
    if (ms == null || f == null) continue;
    pts.push({ data: isoDia(ms), fechamento: f });
  }
  return normalizarSerie(pts);
}

/** brapi /api/quote/PETR4?range=3mo&interval=1d */
export function parseBrapi(json: unknown): { cotacao: Cotacao; serie: Ponto[]; nome?: string } | null {
  const r = (json as any)?.results?.[0];
  if (!r) return null;
  const preco = num(r.regularMarketPrice);
  if (preco == null) return null;
  const pts: Ponto[] = [];
  if (Array.isArray(r.historicalDataPrice)) {
    for (const h of r.historicalDataPrice) {
      const d = num(h?.date);
      const f = num(h?.close);
      if (d == null || f == null) continue;
      pts.push({ data: isoDia(d * 1000), fechamento: f });
    }
  }
  return {
    cotacao: { preco, variacaoDia: num(r.regularMarketChangePercent) },
    serie: normalizarSerie(pts),
    nome: typeof r.shortName === 'string' ? r.shortName : undefined,
  };
}

/** Mensagem amigável para erros HTTP da brapi. */
export function erroBrapi(status: number, temToken: boolean): string {
  if (status === 401) return temToken ? 'Token da brapi recusado. Confira em Configurações.' : 'Token da brapi ausente. Cadastre em Configurações.';
  if (status === 402) return 'Este ativo ou período não está no plano gratuito da brapi.';
  if (status === 429) return 'Limite do plano gratuito da brapi atingido. Tente mais tarde.';
  if (status === 404) return 'Ativo não encontrado na brapi.';
  return `Falha ao consultar a brapi (${status}).`;
}
