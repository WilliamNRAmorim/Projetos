// Perfil financeiro: digitado no app e guardado só no AsyncStorage do aparelho. Nada disso vai para o repositório.
import AsyncStorage from '@react-native-async-storage/async-storage';
import { PERFIL_VAZIO, type PerfilTexto } from './metas';

const CHAVE = 'finagent_perfil_v1';
const SALDO_ANTIGO = 'finagent_saldo_manual'; // campo antigo "Reserva Emergências/Cofrinho" do Painel

/** Lê o perfil. Se existir o saldo antigo do Painel e o Cofrinho estiver vazio, migra o valor para o Cofrinho. */
export async function lerPerfil(): Promise<PerfilTexto> {
  let perfil: PerfilTexto = { ...PERFIL_VAZIO };
  try {
    const t = await AsyncStorage.getItem(CHAVE);
    if (t) perfil = { ...PERFIL_VAZIO, ...(JSON.parse(t) as Partial<PerfilTexto>) };
    const antigo = await AsyncStorage.getItem(SALDO_ANTIGO);
    if (antigo !== null) {
      if (antigo.trim() && !perfil.cofrinho.trim()) {
        perfil.cofrinho = antigo.trim();
        await AsyncStorage.setItem(CHAVE, JSON.stringify(perfil));
      }
      await AsyncStorage.removeItem(SALDO_ANTIGO);
    }
  } catch {
    // sem armazenamento: segue com o padrão vazio
  }
  return perfil;
}

export async function salvarPerfil(p: PerfilTexto): Promise<void> {
  await AsyncStorage.setItem(CHAVE, JSON.stringify(p));
}
