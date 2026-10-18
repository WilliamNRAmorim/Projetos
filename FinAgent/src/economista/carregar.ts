// Carrega os dados do aparelho e monta o contexto (usa AsyncStorage; não roda em node puro).
import { perfilParaNumeros } from '../metas';
import { lerCache } from '../mercado/api';
import { resumoMercadoParaIA } from '../mercado/resumoParaIA';
import { lerExtrato, lerNome } from '../mp/extratoStore';
import { lerPerfil } from '../perfil';
import { montarContexto, type ContextoEconomista } from './contexto';

export async function carregarContexto(hoje = new Date()): Promise<ContextoEconomista> {
  const [perfil, trans, meuNome, cache] = await Promise.all([lerPerfil(), lerExtrato(), lerNome(), lerCache()]);
  let mercadoResumo = 'Mercado: sem dados de mercado disponíveis.';
  try {
    mercadoResumo = await resumoMercadoParaIA();
  } catch {
    // segue sem mercado
  }
  return montarContexto({
    hoje,
    perfil: perfilParaNumeros(perfil),
    trans,
    meuNome,
    mercadoResumo,
    mercadoAtualizadoEm: cache.atualizadoEm,
  });
}
