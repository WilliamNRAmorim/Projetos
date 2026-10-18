import AsyncStorage from '@react-native-async-storage/async-storage';
import { getSecret } from '@/src/secrets';
import type { Pagamento } from './analise';

const BASE = 'https://api.mercadopago.com';
const CACHE = 'finagent_mp_cache_v1';
const SALDO = 'finagent_saldo_manual';
const PAGINA = 50;

export class SemTokenError extends Error {
  constructor() {
    super('Token do Mercado Pago não configurado.');
  }
}

export type DadosMP = { userId: number; pagamentos: Pagamento[]; atualizadoEm: string };

async function get<T>(token: string, caminho: string): Promise<T> {
  const r = await fetch(`${BASE}${caminho}`, { headers: { Authorization: `Bearer ${token}` } });
  if (!r.ok) throw new Error(`Mercado Pago respondeu ${r.status}.`);
  return (await r.json()) as T;
}

export async function lerCache(): Promise<DadosMP | null> {
  try {
    const t = await AsyncStorage.getItem(CACHE);
    return t ? (JSON.parse(t) as DadosMP) : null;
  } catch {
    return null;
  }
}

/**
 * Busca pagamentos (mais recentes primeiro). Com cache, pagina só até encontrar
 * um id já conhecido e junta com o que está salvo; sem cache, baixa tudo.
 */
export async function atualizar(): Promise<DadosMP> {
  const token = await getSecret('mercadopago');
  if (!token) throw new SemTokenError();

  const cache = await lerCache();
  const conhecidos = new Set((cache?.pagamentos ?? []).map((p) => p.id));
  const eu = cache?.userId ?? (await get<{ id: number }>(token, '/users/me')).id;

  const novos: Pagamento[] = [];
  let offset = 0;
  let total = Infinity;
  let achouConhecido = false;
  while (offset < total && !achouConhecido) {
    const res = await get<{ paging: { total: number }; results: Pagamento[] }>(
      token,
      `/v1/payments/search?limit=${PAGINA}&offset=${offset}&sort=date_created&criteria=desc`,
    );
    total = res.paging.total;
    for (const p of res.results) {
      if (conhecidos.has(p.id)) {
        // status pode ter mudado: reaproveita o item novo e continua só até a página acabar
        achouConhecido = true;
      }
      novos.push(slim(p));
    }
    if (res.results.length === 0) break;
    offset += PAGINA;
  }

  const porId = new Map<number, Pagamento>();
  for (const p of cache?.pagamentos ?? []) porId.set(p.id, p);
  for (const p of novos) porId.set(p.id, p);
  const pagamentos = [...porId.values()].sort((a, b) => b.date_created.localeCompare(a.date_created));

  const dados: DadosMP = { userId: eu, pagamentos, atualizadoEm: new Date().toISOString() };
  await AsyncStorage.setItem(CACHE, JSON.stringify(dados));
  return dados;
}

// Guarda só os campos usados (menos dados pessoais no cache).
function slim(p: Pagamento): Pagamento {
  return {
    id: p.id,
    date_created: p.date_created,
    transaction_amount: p.transaction_amount,
    payment_type_id: p.payment_type_id,
    status: p.status,
    description: p.description ?? null,
    collector_id: p.collector_id,
  };
}

export async function lerSaldo(): Promise<string> {
  try {
    return (await AsyncStorage.getItem(SALDO)) ?? '';
  } catch {
    return '';
  }
}

export async function salvarSaldo(texto: string): Promise<void> {
  await AsyncStorage.setItem(SALDO, texto);
}

/** Converte "1.234,56" ou "1234.56" em número. */
export function parseValor(texto: string): number | null {
  const t = texto.trim().replace(/[R$\s]/g, '');
  if (!t) return null;
  const n = Number(t.includes(',') ? t.replace(/\./g, '').replace(',', '.') : t);
  return Number.isFinite(n) ? n : null;
}
