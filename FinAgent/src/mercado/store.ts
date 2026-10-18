import AsyncStorage from '@react-native-async-storage/async-storage';
import type { Alerta } from './alertas.ts';
import { WATCHLIST_PADRAO } from './ativos.ts';
import type { Ativo } from './tipos.ts';

const K_LISTA = 'finagent_watchlist_v1';
const K_ALERTAS = 'finagent_alertas_v1';

async function ler<T>(k: string, padrao: T): Promise<T> {
  try {
    const t = await AsyncStorage.getItem(k);
    return t ? (JSON.parse(t) as T) : padrao;
  } catch {
    return padrao;
  }
}

export const lerWatchlist = () => ler<Ativo[]>(K_LISTA, WATCHLIST_PADRAO);
export const salvarWatchlist = (l: Ativo[]) => AsyncStorage.setItem(K_LISTA, JSON.stringify(l));
export const lerAlertas = () => ler<Alerta[]>(K_ALERTAS, []);
export const salvarAlertas = (a: Alerta[]) => AsyncStorage.setItem(K_ALERTAS, JSON.stringify(a));
