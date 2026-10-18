// Agregados dos indicadores da watchlist (só ativos e números de mercado; nenhum dado pessoal).
import { lerCache } from './api.ts';
import { calcularIndicadores } from './indicadores.ts';
import { montarResumo } from './leitura.ts';
import { lerWatchlist } from './store.ts';

export async function resumoMercadoParaIA(): Promise<string> {
  const [lista, cache] = await Promise.all([lerWatchlist(), lerCache()]);
  const itens = lista.map((a) => {
    const d = cache.dados[a.id];
    return { nome: a.nome, tipo: a.tipo, ind: d ? calcularIndicadores(d.serie, d.cotacao.preco) : null };
  });
  return montarResumo(itens);
}
