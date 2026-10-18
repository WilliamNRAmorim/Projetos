import AsyncStorage from '@react-native-async-storage/async-storage';

const K_INICIO = 'finagent_corte_inicio_v1';

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
