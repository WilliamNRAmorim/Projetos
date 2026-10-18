// Contexto enviado ao Gemini: SOMENTE agregados. Nunca nomes de contrapartes, CPF, endereço,
// descrições de transações nem chaves. Funções puras (testáveis em node).
import { comprometidoDoMes, mediaGastoMensal, mesesDeReserva, resumoMetas, usoLimite, type PerfilNum } from '../metas.ts';
import { classificarExtrato, mesAnteriorDe, mesesDisponiveis, totaisMes, type Transacao } from '../mp/extrato.ts';
import { resumoParaIA } from '../mp/resumoParaIA.ts';

export type EntradaContexto = {
  hoje: Date;
  perfil: PerfilNum;
  trans: Transacao[];
  meuNome: string; // usado só para classificar o extrato; NUNCA vai no contexto
  mercadoResumo: string; // texto de mercado já agregado (montarResumo)
  mercadoAtualizadoEm: string | null;
};

const r2 = (n: number) => Math.round(n * 100) / 100;
const chaveMes = (d: Date) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`;
const dataISO = (d: Date) => `${chaveMes(d)}-${String(d.getDate()).padStart(2, '0')}`;

/** Remove padrões sensíveis que não deveriam estar aqui (CPF, CNPJ, e-mail, sequências longas de dígitos). */
export function sanitizar(texto: string): string {
  return texto
    .replace(/\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b/g, '[removido]')
    .replace(/\b\d{2}\.?\d{3}\.?\d{3}\/?\d{4}-?\d{2}\b/g, '[removido]')
    .replace(/[\w.+-]+@[\w-]+\.[\w.-]+/g, '[removido]')
    .replace(/\b\d{9,}\b/g, '[removido]');
}

export type ContextoEconomista = {
  data_hoje: string;
  perfil: {
    salario: number | null;
    dia_salario: number | null;
    pct_comprometido: number | null;
    fatura_aberta: number | null;
    limite_cartao: number | null;
    pct_limite_usado: number | null;
    reserva_saldo: number | null;
    meses_de_reserva: number | null;
    gasto_medio_mensal: number | null;
  };
  mes_atual: string;
  ultimos_meses: { mes: string; gastos: number; fatura_paga: number; por_categoria: Record<string, number> }[];
  tendencias: {
    gasto_vs_mes_anterior_pct: number | null;
    categorias_que_mais_subiram: { categoria: string; variacao_reais: number }[];
  };
  mercado: { atualizado_em: string | null; resumo: string };
};

export function montarContexto(e: EntradaContexto): ContextoEconomista {
  const lancs = classificarExtrato(e.trans, e.meuNome);
  const meses = mesesDisponiveis(e.trans); // mais recente primeiro
  const atual = chaveMes(e.hoje);
  const ref = meses.includes(atual) ? atual : meses[0] ?? atual;
  const media = mediaGastoMensal(e.trans, e.meuNome, e.hoje)?.media ?? null;
  const metas = resumoMetas(e.perfil, media);

  const ultimos = meses
    .filter((m) => m <= ref)
    .slice(0, 3)
    .map((m) => {
      const t = totaisMes(lancs, m);
      return {
        mes: m,
        gastos: t.gastos,
        fatura_paga: t.fatura,
        por_categoria: Object.fromEntries(t.porCategoria.map((c) => [c.nome, c.total])),
      };
    });

  const tRef = meses.length ? totaisMes(lancs, ref) : null;
  const antCats = new Map(totaisMes(lancs, mesAnteriorDe(ref)).porCategoria.map((c) => [c.nome, c.total]));
  const subiram = (tRef?.porCategoria ?? [])
    .map((c) => ({ categoria: c.nome, variacao_reais: r2(c.total - (antCats.get(c.nome) ?? 0)) }))
    .filter((c) => c.variacao_reais > 0)
    .sort((a, b) => b.variacao_reais - a.variacao_reais)
    .slice(0, 3);

  const p = e.perfil;
  return {
    data_hoje: dataISO(e.hoje),
    perfil: {
      salario: p.salario,
      dia_salario: p.diaSalario,
      pct_comprometido: comprometidoDoMes(p).pctSalario,
      fatura_aberta: p.faturaAberta,
      limite_cartao: p.limiteCartao,
      pct_limite_usado: usoLimite(p.limiteCartao, p.faturaAberta),
      reserva_saldo: p.cofrinho,
      meses_de_reserva: mesesDeReserva(p.cofrinho, media),
      gasto_medio_mensal: media,
    },
    mes_atual: tRef ? sanitizar(resumoParaIA(tRef, metas)) : 'sem extrato importado',
    ultimos_meses: ultimos,
    tendencias: { gasto_vs_mes_anterior_pct: tRef?.variacaoGasto ?? null, categorias_que_mais_subiram: subiram },
    mercado: { atualizado_em: e.mercadoAtualizadoEm, resumo: sanitizar(e.mercadoResumo) },
  };
}

/** JSON enviado à IA (compacto) ou formatado para mostrar ao usuário na tela. */
export const contextoParaJson = (c: ContextoEconomista, indentado = false) =>
  JSON.stringify(c, null, indentado ? 2 : undefined);
