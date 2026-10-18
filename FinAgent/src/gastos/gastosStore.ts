import AsyncStorage from '@react-native-async-storage/async-storage';
import { REGRAS_VAZIAS, type RegrasSalvas, type Tetos } from './gastos';

const K_TETOS = 'finagent_tetos_v1';
const K_REGRAS = 'finagent_regras_cat_v1';

async function ler<T>(chave: string, vazio: T): Promise<T> {
  try {
    const t = await AsyncStorage.getItem(chave);
    return t ? ({ ...vazio, ...JSON.parse(t) } as T) : vazio;
  } catch {
    return vazio;
  }
}

export const lerTetos = () => ler<Tetos>(K_TETOS, {});
export const salvarTetos = (t: Tetos) => AsyncStorage.setItem(K_TETOS, JSON.stringify(t));

/** Regras de recategorização. Passe o resultado como 3º argumento de classificarExtrato. */
export const lerRegras = () => ler<RegrasSalvas>(K_REGRAS, REGRAS_VAZIAS);
export const salvarRegras = (r: RegrasSalvas) => AsyncStorage.setItem(K_REGRAS, JSON.stringify(r));
