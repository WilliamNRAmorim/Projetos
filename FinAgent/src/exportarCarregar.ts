// Carrega os dados do aparelho e monta o texto de export (usa AsyncStorage; não roda em node puro).
import { lerBasesCorte, lerInicioCorte } from './cortesStore';
import { montarExport } from './exportar';
import { lerRegras, lerTetos } from './gastos/gastosStore';
import { perfilParaNumeros } from './metas';
import { lerExtrato, lerNome } from './mp/extratoStore';
import { lerPerfil } from './perfil';

export async function gerarExport(hoje = new Date()): Promise<string> {
  const [perfil, trans, meuNome, regras, tetos, inicioCorte, basesCorte] = await Promise.all([
    lerPerfil(), lerExtrato(), lerNome(), lerRegras(), lerTetos(), lerInicioCorte(hoje), lerBasesCorte(),
  ]);
  return montarExport({ hoje, perfil: perfilParaNumeros(perfil), trans, meuNome, regras, tetos, inicioCorte, basesCorte });
}
