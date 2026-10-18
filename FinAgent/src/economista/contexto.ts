// Contexto enviado ao Gemini: SOMENTE faixas e percentuais (nenhum valor exato de salário, saldo, limite, fatura ou gasto).
// Nunca nomes de contrapartes, CPF, endereço,
// descrições de transações nem chaves. Funções puras (testáveis em node).
import { comprometidoDoMes, mediaGastoMensal, mesesDeReserva, usoLimite, type PerfilNum } from '../metas.ts';
import { classificarExtrato, mesAnteriorDe, mesesDisponiveis, totaisMes, type RegrasUsuario, type Transacao } from '../mp/extrato.ts';

export type EntradaContexto = {
  hoje: Date;
  perfil: PerfilNum;
  trans: Transacao[];
  meuNome: string; // usado só para classificar o extrato; NUNCA vai no contexto
  mercadoResumo: string; // texto de mercado já agregado (montarResumo)
  mercadoAtualizadoEm: string | null;
  regras?: RegrasUsuario; // recategorizações do usuário
};

const r2 = (n: number) => Math.round(n * 100) / 100;
const chaveMes = (d: Date) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`;
const dataISO = (d: Date) => `${chaveMes(d)}-${String(d.getDate()).padStart(2, '0')}`;

/** Remove padrões sensíveis que não deveriam estar aqui (CPF, CNPJ, e-mail, sequências longas de dígitos). */
export function sanitizar(texto: string): string {
  return texto
    .replace(/\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b/g, '(removido)')
    .replace(/\b\d{2}\.?\d{3}\.?\d{3}\/?\d{4}-?\d{2}\b/g, '(removido)')
    .replace(/[\w.+-]+@[\w-]+\.[\w.-]+/g, '(removido)')
    .replace(/\b\d{9,}\b/g, '(removido)')
    .replace(/[[\]]/g, ' '); // sem colchetes: ninguém forja os delimitadores do bloco de dados
}

/** Faixa de R$ 500 do valor: 1.610 vira "R$ 1.500–2.000". Nunca o valor exato. */
export function faixaSalario(v: number | null): string | null {
  if (v === null || v <= 0) return null;
  const lo = Math.floor(v / 500) * 500;
  const f = (n: number) => String(n).replace(/\B(?=(\d{3})+(?!\d))/g, '.');
  return `R$ ${f(lo)}–${f(lo + 500)}`;
}

const pct1 = (n: number) => Math.round(n * 10) / 10;
/** valor como % do salário (1 casa); null sem salário. */
const pctSal = (v: number | null, salario: number | null) => (v === null || !salario || salario <= 0 ? null : pct1((v / salario) * 100));

export type ContextoEconomista = {
  data_hoje: string;
  perfil: {
    salario_faixa: string | null;
    dia_salario: number | null;
    dia_vencimento_fatura: number | null;
    pct_comprometido: number | null;
    fatura_aberta_pct_salario: number | null;
    limite_cartao_pct_salario: number | null;
    pct_limite_usado: number | null;
    reserva_em_meses: number | null;
    gasto_medio_pct_salario: number | null;
  };
  mes_atual: string;
  ultimos_meses: { mes: string; gastos_pct_salario: number | null; fatura_paga_pct_salario: number | null; por_categoria_pct_salario: Record<string, number | null> }[];
  tendencias: {
    gasto_vs_mes_anterior_pct: number | null;
    categorias_que_mais_subiram: { categoria: string; variacao_pct_salario: number | null }[];
  };
  mercado: { atualizado_em: string | null; resumo: string };
};

export function montarContexto(e: EntradaContexto): ContextoEconomista {
  const lancs = classificarExtrato(e.trans, e.meuNome, e.regras);
  const meses = mesesDisponiveis(e.trans); // mais recente primeiro
  const atual = chaveMes(e.hoje);
  const ref = meses.includes(atual) ? atual : meses[0] ?? atual;
  const mg = mediaGastoMensal(e.trans, e.meuNome, e.hoje, undefined, e.regras);
  const media = mg?.media ?? null;
  const p = e.perfil;
  const sal = p.salario;

  const ultimos = meses
    .filter((m) => m <= ref)
    .slice(0, 3)
    .map((m) => {
      const t = totaisMes(lancs, m);
      return {
        mes: m,
        gastos_pct_salario: pctSal(t.gastos, sal),
        fatura_paga_pct_salario: pctSal(t.fatura, sal),
        por_categoria_pct_salario: Object.fromEntries(t.porCategoria.map((c) => [c.nome, pctSal(c.total, sal)])),
      };
    });

  const tRef = meses.length ? totaisMes(lancs, ref) : null;
  const antCats = new Map(totaisMes(lancs, mesAnteriorDe(ref)).porCategoria.map((c) => [c.nome, c.total]));
  const subiram = (tRef?.porCategoria ?? [])
    .map((c) => ({ categoria: c.nome, variacao: r2(c.total - (antCats.get(c.nome) ?? 0)) }))
    .filter((c) => c.variacao > 0)
    .sort((a, b) => b.variacao - a.variacao)
    .slice(0, 3)
    .map((c) => ({ categoria: c.categoria, variacao_pct_salario: pctSal(c.variacao, sal) }));

  const gastoMedioPct = pctSal(media, sal);
  const mesesRes = mesesDeReserva(p.cofrinho, media);
  const partes: string[] = [];
  if (tRef) {
    const cats = ultimos[0]?.por_categoria_pct_salario ?? {};
    partes.push(`Mês ${tRef.mes}`);
    if (sal) {
      partes.push(`gastos ${pctSal(tRef.gastos, sal)}% do salário (${tRef.variacaoGasto === null ? 'sem mês anterior' : tRef.variacaoGasto + '% vs mês anterior'})`);
      partes.push(`fatura do cartão paga ${pctSal(tRef.fatura, sal)}% do salário`);
      partes.push(`gastos por categoria (% do salário): ${Object.entries(cats).map(([k, v]) => k + ' ' + v).join('; ') || 'nenhum'}`);
    } else {
      partes.push('sem salário informado: valores em R$ omitidos');
    }
  }

  return {
    data_hoje: dataISO(e.hoje),
    perfil: {
      salario_faixa: faixaSalario(sal),
      dia_salario: p.diaSalario,
      dia_vencimento_fatura: p.diaVencimento,
      pct_comprometido: comprometidoDoMes(p).pctSalario,
      fatura_aberta_pct_salario: pctSal(p.faturaAberta, sal),
      limite_cartao_pct_salario: pctSal(p.limiteCartao, sal),
      pct_limite_usado: usoLimite(p.limiteCartao, p.faturaAberta),
      reserva_em_meses: mesesRes,
      gasto_medio_pct_salario: gastoMedioPct,
    },
    mes_atual: tRef ? sanitizar(partes.join(' | ')) : 'sem extrato importado',
    ultimos_meses: ultimos,
    tendencias: { gasto_vs_mes_anterior_pct: tRef?.variacaoGasto ?? null, categorias_que_mais_subiram: subiram },
    mercado: { atualizado_em: e.mercadoAtualizadoEm, resumo: sanitizar(e.mercadoResumo) },
  };
}

/** JSON enviado à IA (compacto) ou formatado para mostrar ao usuário na tela. */
export const contextoParaJson = (c: ContextoEconomista, indentado = false) =>
  JSON.stringify(c, null, indentado ? 2 : undefined);
