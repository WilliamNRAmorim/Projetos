import AsyncStorage from '@react-native-async-storage/async-storage';
import type { BasesCorte } from './cortes';

const K_INICIO = 'finagent_corte_inicio_v1';
const K_BASES = 'finagent_corte_bases_v1';

/** Mês de início do plano de corte (YYYY-MM). Na primeira vez, grava o mês atual. */
export async function lerInicioCorte(hoje = new Date()): Promise<string> {
  const padrao = `${hoje.getFullYear()}-${String(hoje.getMonth() + 1).padStart(2, '0')}`;
  try {
    const t = await AsyncStorage.getItem(K_INICIO);
    if (t && /^\d{4}-\d{2}$/.test(t)) return t;
    await AsyncStorage.setItem(K_INICIO, padrao);
  } catch {
    // sem armazenamento: usa o mês atual
  }
  return padrao;
}

/** Bases congeladas no início do plano: os tetos não mudam quando importar mais faturas depois. */
export async function lerBasesCorte(): Promise<BasesCorte> {
  try {
    const t = await AsyncStorage.getItem(K_BASES);
    const bruto = t ? (JSON.parse(t) as Record<string, unknown>) : {};
    const bases: BasesCorte = {};
    for (const id of ['transporte', 'delivery'] as const) {
      const v = bruto[id];
      if (typeof v === 'number' && Number.isFinite(v) && v > 0) bases[id] = v;
    }
    return bases;
  } catch {
    return {};
  }
}

export async function salvarBasesCorte(bases: BasesCorte): Promise<void> {
  try {
    await AsyncStorage.setItem(K_BASES, JSON.stringify(bases));
  } catch {
    // sem armazenamento: a base segue calculada do extrato
  }
}

/** Recomeça o plano no mês atual e descarta as bases congeladas (serão recalculadas e congeladas de novo). */
export async function reiniciarPlanoCorte(hoje = new Date()): Promise<string> {
  const mes = `${hoje.getFullYear()}-${String(hoje.getMonth() + 1).padStart(2, '0')}`;
  try {
    await AsyncStorage.setItem(K_INICIO, mes);
    await AsyncStorage.removeItem(K_BASES);
  } catch {
    // sem armazenamento: o plano segue como estava
  }
  return mes;
}
