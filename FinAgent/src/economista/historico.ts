// Histórico do chat: só no AsyncStorage do aparelho.
import AsyncStorage from '@react-native-async-storage/async-storage';

const CHAVE = 'finagent_economista_v1';
export const MAX_GUARDADAS = 30;

export type MensagemChat = {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  aviso?: string | null; // aviso da guarda, mostrado sob a bolha
  flags?: string[]; // registro da guarda
};

export async function lerHistorico(): Promise<MensagemChat[]> {
  try {
    const t = await AsyncStorage.getItem(CHAVE);
    const lista = t ? (JSON.parse(t) as MensagemChat[]) : [];
    return Array.isArray(lista) ? lista.slice(-MAX_GUARDADAS) : [];
  } catch {
    return [];
  }
}

export async function salvarHistorico(lista: MensagemChat[]): Promise<void> {
  try {
    await AsyncStorage.setItem(CHAVE, JSON.stringify(lista.slice(-MAX_GUARDADAS)));
  } catch {
    // sem armazenamento: a conversa vale só nesta sessão
  }
}

export async function limparHistorico(): Promise<void> {
  try {
    await AsyncStorage.removeItem(CHAVE);
  } catch {
    // ignora
  }
}
