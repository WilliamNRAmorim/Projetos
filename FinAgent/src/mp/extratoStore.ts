import AsyncStorage from '@react-native-async-storage/async-storage';
import * as DocumentPicker from 'expo-document-picker';
import { mesclar, parseExtratoCsv, type Transacao } from './extrato';

const CHAVE = 'finagent_extrato_v1';
const NOME = 'finagent_meu_nome';

export async function lerExtrato(): Promise<Transacao[]> {
  try {
    const t = await AsyncStorage.getItem(CHAVE);
    return t ? (JSON.parse(t) as Transacao[]) : [];
  } catch {
    return [];
  }
}

export async function lerNome(): Promise<string> {
  try {
    return (await AsyncStorage.getItem(NOME)) ?? '';
  } catch {
    return '';
  }
}

export async function salvarNome(n: string): Promise<void> {
  await AsyncStorage.setItem(NOME, n);
}

/** Abre o seletor, lê os CSVs escolhidos, mescla com o que já está salvo. Nunca loga conteúdo. */
export async function importarExtratos(): Promise<{ arquivos: number; linhas: number; total: Transacao[] } | null> {
  const r = await DocumentPicker.getDocumentAsync({ type: '*/*', multiple: true, copyToCacheDirectory: true });
  if (r.canceled) return null;
  let atual = await lerExtrato();
  let linhas = 0;
  for (const a of r.assets) {
    const texto = await (await fetch(a.uri)).text();
    const novas = parseExtratoCsv(texto);
    linhas += novas.length;
    atual = mesclar(atual, novas);
  }
  await AsyncStorage.setItem(CHAVE, JSON.stringify(atual));
  return { arquivos: r.assets.length, linhas, total: atual };
}

export async function limparExtrato(): Promise<void> {
  await AsyncStorage.removeItem(CHAVE);
}
