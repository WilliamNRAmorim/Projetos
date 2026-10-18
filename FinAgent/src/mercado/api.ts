// Clientes de mercado: AwesomeAPI (moedas), CoinGecko (cripto), brapi (B3, token no header).
// Só tickers/moedas saem do aparelho; nenhum dado pessoal. Cache em AsyncStorage.
import AsyncStorage from '@react-native-async-storage/async-storage';
import { getSecret } from '../secrets';
import {
  erroBrapi,
  parseAwesomeDaily,
  parseAwesomeLast,
  parseBrapi,
  parseCoingeckoPreco,
  parseCoingeckoSerie,
} from './parsers.ts';
import type { Ativo, Cotacao, Ponto } from './tipos.ts';

export type DadosAtivo = { cotacao: Cotacao; serie: Ponto[]; em: string };
export type Resultado =
  | { ok: true; dados: DadosAtivo; doCache: boolean; aviso?: string }
  | { ok: false; erro: string };
export type Atualizacao = { resultados: Record<string, Resultado>; atualizadoEm: string | null };

const CHAVE_CACHE = 'finagent_mercado_cache_v1';
const TIMEOUT_MS = 12000;

class HttpErro extends Error {
  status: number;
  constructor(status: number) {
    super(`HTTP ${status}`);
    this.status = status;
  }
}

async function getJson(url: string, headers?: Record<string, string>): Promise<unknown> {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), TIMEOUT_MS);
  try {
    const r = await fetch(url, { headers: { Accept: 'application/json', ...headers }, signal: ctrl.signal });
    if (!r.ok) throw new HttpErro(r.status);
    return await r.json();
  } finally {
    clearTimeout(t);
  }
}

function msgErro(e: unknown, fonte: string): string {
  if (e instanceof HttpErro) {
    return e.status === 429
      ? `Limite de consultas de ${fonte} atingido. Tente em alguns minutos.`
      : `${fonte} respondeu com erro (${e.status}).`;
  }
  if (e instanceof Error && e.name === 'AbortError') return `${fonte} demorou demais para responder.`;
  return `Sem conexão com ${fonte}.`;
}

type Cache = { atualizadoEm: string | null; dados: Record<string, DadosAtivo> };

export async function lerCache(): Promise<Cache> {
  try {
    const t = await AsyncStorage.getItem(CHAVE_CACHE);
    if (t) return JSON.parse(t) as Cache;
  } catch {}
  return { atualizadoEm: null, dados: {} };
}

async function buscarMoedas(ativos: Ativo[]): Promise<Record<string, Resultado>> {
  const out: Record<string, Resultado> = {};
  if (!ativos.length) return out;
  const pares = ativos.map((a) => `${a.codigo}-BRL`);
  let last: Record<string, Cotacao> = {};
  let erroLast = '';
  try {
    last = parseAwesomeLast(await getJson(`https://economia.awesomeapi.com.br/json/last/${pares.join(',')}`));
  } catch (e) {
    erroLast = msgErro(e, 'a AwesomeAPI');
  }
  for (const a of ativos) {
    const cot = last[`${a.codigo}-BRL`];
    if (!cot) {
      out[a.id] = { ok: false, erro: erroLast || 'Cotação não encontrada na AwesomeAPI.' };
      continue;
    }
    let serie: Ponto[] = [];
    try {
      serie = parseAwesomeDaily(await getJson(`https://economia.awesomeapi.com.br/json/daily/${a.codigo}-BRL/90`));
    } catch {}
    out[a.id] = { ok: true, doCache: false, dados: { cotacao: cot, serie, em: new Date().toISOString() } };
  }
  return out;
}

async function buscarCriptos(ativos: Ativo[]): Promise<Record<string, Resultado>> {
  const out: Record<string, Resultado> = {};
  if (!ativos.length) return out;
  let precos: Record<string, Cotacao> = {};
  let erro = '';
  try {
    const ids = ativos.map((a) => a.codigo).join(',');
    precos = parseCoingeckoPreco(
      await getJson(`https://api.coingecko.com/api/v3/simple/price?ids=${ids}&vs_currencies=brl&include_24hr_change=true`),
    );
  } catch (e) {
    erro = msgErro(e, 'a CoinGecko');
  }
  for (const a of ativos) {
    const cot = precos[a.codigo];
    if (!cot) {
      out[a.id] = { ok: false, erro: erro || 'Cripto não encontrada na CoinGecko.' };
      continue;
    }
    let serie: Ponto[] = [];
    try {
      serie = parseCoingeckoSerie(
        await getJson(`https://api.coingecko.com/api/v3/coins/${a.codigo}/market_chart?vs_currency=brl&days=90&interval=daily`),
      );
    } catch {}
    out[a.id] = { ok: true, doCache: false, dados: { cotacao: cot, serie, em: new Date().toISOString() } };
  }
  return out;
}

/** Um ticker por vez; o token vai só no header Authorization. Erro por ativo, sem derrubar o resto. */
async function buscarAcao(a: Ativo, token: string | null): Promise<Resultado> {
  try {
    const json = await getJson(
      `https://brapi.dev/api/quote/${encodeURIComponent(a.codigo)}?range=3mo&interval=1d`,
      token ? { Authorization: `Bearer ${token}` } : undefined,
    );
    const p = parseBrapi(json);
    if (!p) return { ok: false, erro: 'Resposta da brapi sem dados para este ativo.' };
    return { ok: true, doCache: false, dados: { cotacao: p.cotacao, serie: p.serie, em: new Date().toISOString() } };
  } catch (e) {
    if (e instanceof HttpErro) return { ok: false, erro: erroBrapi(e.status, !!token) };
    return { ok: false, erro: msgErro(e, 'a brapi') };
  }
}

export async function atualizarMercado(ativos: Ativo[]): Promise<Atualizacao> {
  const cache = await lerCache();
  let token: string | null = null;
  try {
    token = await getSecret('brapi');
  } catch {}

  const [moedas, criptos] = await Promise.all([
    buscarMoedas(ativos.filter((a) => a.tipo === 'moeda')),
    buscarCriptos(ativos.filter((a) => a.tipo === 'cripto')),
  ]);
  const acoes: Record<string, Resultado> = {};
  for (const a of ativos.filter((x) => x.tipo === 'acao')) acoes[a.id] = await buscarAcao(a, token);

  const todos = { ...moedas, ...criptos, ...acoes };
  const resultados: Record<string, Resultado> = {};
  const novoCache: Cache = { atualizadoEm: cache.atualizadoEm, dados: { ...cache.dados } };
  let algumNovo = false;
  for (const a of ativos) {
    const r = todos[a.id];
    if (r?.ok) {
      resultados[a.id] = r;
      novoCache.dados[a.id] = r.dados;
      algumNovo = true;
    } else if (cache.dados[a.id]) {
      resultados[a.id] = { ok: true, doCache: true, dados: cache.dados[a.id], aviso: r && !r.ok ? r.erro : undefined };
    } else {
      resultados[a.id] = r ?? { ok: false, erro: 'Sem dados.' };
    }
  }
  if (algumNovo) {
    novoCache.atualizadoEm = new Date().toISOString();
    try {
      await AsyncStorage.setItem(CHAVE_CACHE, JSON.stringify(novoCache));
    } catch {}
  }
  return { resultados, atualizadoEm: novoCache.atualizadoEm };
}
