import * as SecureStore from 'expo-secure-store';

export type NomeChave = 'mercadopago' | 'gemini' | 'brapi';

export const CHAVES: { nome: NomeChave; rotulo: string }[] = [
  { nome: 'mercadopago', rotulo: 'Access Token do Mercado Pago' },
  { nome: 'gemini', rotulo: 'Chave do Gemini' },
  { nome: 'brapi', rotulo: 'Token da brapi' },
];

const key = (nome: NomeChave) => `finagent_${nome}`;

export async function getSecret(nome: NomeChave): Promise<string | null> {
  return SecureStore.getItemAsync(key(nome));
}

export async function setSecret(nome: NomeChave, valor: string): Promise<void> {
  const v = valor.trim();
  if (!v) return SecureStore.deleteItemAsync(key(nome));
  return SecureStore.setItemAsync(key(nome), v);
}
