// CDI anualizado (base 252): API pública do Banco Central (SGS 4389), com cache diário e valor manual de reserva.
import AsyncStorage from '@react-native-async-storage/async-storage';
import { URL_CDI_BCB, lerRespostaCdi } from './calc';

const CHAVE_CACHE = 'finagent_cdi_cache_v1';
const CHAVE_MANUAL = 'finagent_cdi_manual_v1';

export type FonteCdi = 'bcb' | 'cache' | 'manual';
export type CdiInfo = {
  taxa: number; // % ao ano
  fonte: FonteCdi;
  dataRef: string | null; // data da taxa no BC (YYYY-MM-DD)
  buscadoEm: string | null; // dia em que o app consultou o BC (YYYY-MM-DD)
};

type Cache = { taxa: number; dataRef: string; buscadoEm: string };

const hojeIso = () => {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
};

async function lerCache(): Promise<Cache | null> {
  try {
    const t = await AsyncStorage.getItem(CHAVE_CACHE);
    return t ? (JSON.parse(t) as Cache) : null;
  } catch {
    return null;
  }
}

export async function lerCdiManual(): Promise<string> {
  try {
    return (await AsyncStorage.getItem(CHAVE_MANUAL)) ?? '';
  } catch {
    return '';
  }
}

export async function salvarCdiManual(texto: string): Promise<void> {
  try {
    await AsyncStorage.setItem(CHAVE_MANUAL, texto);
  } catch {
    // sem armazenamento: o valor vale só nesta sessão
  }
}

async function buscarNoBanco(): Promise<{ taxa: number; data: string } | null> {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), 8000);
  try {
    const r = await fetch(URL_CDI_BCB, { signal: ctrl.signal });
    if (!r.ok) return null;
    return lerRespostaCdi(await r.json());
  } catch {
    return null;
  } finally {
    clearTimeout(timer);
  }
}

/**
 * Ordem: cache de hoje, consulta ao BC, valor manual do usuário, cache antigo. Sem nada, null.
 * `manual` já vem convertido para número (ou null).
 */
export async function carregarCdi(manual: number | null): Promise<CdiInfo | null> {
  const cache = await lerCache();
  if (cache && cache.buscadoEm === hojeIso()) {
    return { taxa: cache.taxa, fonte: 'bcb', dataRef: cache.dataRef, buscadoEm: cache.buscadoEm };
  }
  const novo = await buscarNoBanco();
  if (novo) {
    const c: Cache = { taxa: novo.taxa, dataRef: novo.data, buscadoEm: hojeIso() };
    try {
      await AsyncStorage.setItem(CHAVE_CACHE, JSON.stringify(c));
    } catch {
      // segue sem cache
    }
    return { taxa: c.taxa, fonte: 'bcb', dataRef: c.dataRef, buscadoEm: c.buscadoEm };
  }
  if (manual !== null && manual > 0) return { taxa: manual, fonte: 'manual', dataRef: null, buscadoEm: null };
  if (cache) return { taxa: cache.taxa, fonte: 'cache', dataRef: cache.dataRef, buscadoEm: cache.buscadoEm };
  return null;
}

export const dataBR = (iso: string) => `${iso.slice(8)}/${iso.slice(5, 7)}/${iso.slice(0, 4)}`;
