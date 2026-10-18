// Lógica pura da aba Gastos (sem React Native): orçamento, períodos, filtros, regras.
import { CAT, norm } from '../mp/categorias.ts';
import { chaveTransacao, mesAnteriorDe, mesDe, mesesDisponiveis, totaisMes, type Lancamento, type RegrasUsuario } from '../mp/extrato.ts';

export const r2 = (n: number) => Math.round(n * 100) / 100;

/** Categorias de gasto que o usuário pode escolher ao recategorizar. */
export const CATEGORIAS_GASTO: string[] = [
  CAT.COMIDA, CAT.TRANSPORTE, CAT.TELEFONIA, CAT.ASSINATURAS, CAT.EMPRESTIMO, CAT.PIX_PESSOAS, CAT.OUTROS,
];

// ---------- Orçamento ----------

export type Tetos = Record<string, number>; // categoria -> teto mensal (R$). Fatura usa CAT.FATURA.
export type Faixa = 'ok' | 'atencao' | 'estourou';

/** <80% ok, 80 a 100% atenção, >100% estourou. */
export function faixaOrcamento(pct: number): Faixa {
  if (pct > 100) return 'estourou';
  if (pct >= 80) return 'atencao';
  return 'ok';
}

export type LinhaOrcamento = { categoria: string; teto: number | null; gasto: number; pct: number | null; faixa: Faixa | null };

export function linhasOrcamento(lancs: Lancamento[], mes: string, tetos: Tetos): { linhas: LinhaOrcamento[]; totalOrcado: number; totalGasto: number } {
  const tot = totaisMes(lancs, mes);
  const gasto = new Map<string, number>(tot.porCategoria.map((c) => [c.nome, c.total]));
  gasto.set(CAT.FATURA, tot.fatura);
  const cats = new Set<string>([...gasto.keys(), ...Object.keys(tetos)]);
  const linhas: LinhaOrcamento[] = [...cats]
    .map((categoria) => {
      const g = gasto.get(categoria) ?? 0;
      const t = tetos[categoria] > 0 ? tetos[categoria] : null;
      const pct = t ? r2((g / t) * 100) : null;
      return { categoria, teto: t, gasto: r2(g), pct, faixa: pct === null ? null : faixaOrcamento(pct) };
    })
    .filter((l) => l.teto !== null || l.gasto > 0)
    .sort((a, b) => (a.categoria === CAT.FATURA ? 1 : 0) - (b.categoria === CAT.FATURA ? 1 : 0) || b.gasto - a.gasto);
  const comTeto = linhas.filter((l) => l.teto !== null);
  return {
    linhas,
    totalOrcado: r2(comTeto.reduce((s, l) => s + (l.teto ?? 0), 0)),
    totalGasto: r2(comTeto.reduce((s, l) => s + l.gasto, 0)),
  };
}

/** Média da categoria nos até 3 meses anteriores ao `mes` que tenham dados. Sem dados: null. */
export function mediaUltimos3Meses(lancs: Lancamento[], mes: string, categoria: string): number | null {
  const meses: string[] = [];
  let m = mes;
  for (let i = 0; i < 3; i++) {
    m = mesAnteriorDe(m);
    meses.push(m);
  }
  const comDados = meses.filter((x) => lancs.some((l) => mesDe(l.data) === x));
  if (comDados.length === 0) return null;
  const soma = comDados.reduce((s, x) => {
    const t = totaisMes(lancs, x);
    return s + (categoria === CAT.FATURA ? t.fatura : t.porCategoria.find((c) => c.nome === categoria)?.total ?? 0);
  }, 0);
  const media = soma / comDados.length;
  return media > 0 ? Math.round(media) : null;
}

// ---------- Pra onde foi ----------

export type Periodo = 'mes' | '3m' | 'tudo';

/** Meses incluídos no período, tendo `mesRef` (o mais recente do extrato) como "mês atual". */
export function mesesDoPeriodo(periodo: Periodo, todos: string[], mesRef: string): string[] {
  if (periodo === 'tudo') return todos;
  if (periodo === 'mes') return [mesRef];
  const m1 = mesAnteriorDe(mesRef);
  return [mesRef, m1, mesAnteriorDe(m1)];
}

export function porCategoriaNoPeriodo(lancs: Lancamento[], periodo: Periodo, mesRef: string): { nome: string; total: number; pct: number }[] {
  const meses = new Set(mesesDoPeriodo(periodo, mesesDisponiveis(lancs), mesRef));
  const mapa = new Map<string, number>();
  for (const m of meses) {
    for (const c of totaisMes(lancs, m).porCategoria) mapa.set(c.nome, (mapa.get(c.nome) ?? 0) + c.total);
  }
  const total = [...mapa.values()].reduce((s, v) => s + v, 0);
  return [...mapa.entries()]
    .map(([nome, t]) => ({ nome, total: r2(t), pct: total > 0 ? r2((t / total) * 100) : 0 }))
    .sort((a, b) => b.total - a.total);
}

// ---------- Transações ----------

export type Filtro = { busca?: string; categoria?: string | null; mes?: string | null; mostrarInternos?: boolean };

/** Texto da contraparte com iniciais maiúsculas; sem contraparte, o tipo original. */
export function descricaoLimpa(l: Lancamento): string {
  const base = l.contraparte || l.tipo;
  return base
    .split(' ')
    .filter(Boolean)
    .map((p) => (p.length > 2 ? p.charAt(0).toUpperCase() + p.slice(1).toLowerCase() : p.toLowerCase()))
    .join(' ');
}

export function filtrarTransacoes(lancs: Lancamento[], f: Filtro): Lancamento[] {
  const q = norm(f.busca ?? '');
  return lancs
    .filter((l) => {
      if (!f.mostrarInternos && l.categoria === CAT.INTERNO) return false;
      if (f.mes && mesDe(l.data) !== f.mes) return false;
      if (f.categoria && l.categoria !== f.categoria) return false;
      if (q && !norm(`${descricaoLimpa(l)} ${l.tipo} ${l.categoria}`).includes(q)) return false;
      return true;
    })
    .sort((a, b) => b.data.localeCompare(a.data) || b.seq - a.seq);
}

export function agruparPorDia(lancs: Lancamento[]): { data: string; itens: Lancamento[] }[] {
  const grupos: { data: string; itens: Lancamento[] }[] = [];
  for (const l of lancs) {
    const g = grupos[grupos.length - 1];
    if (g && g.data === l.data) g.itens.push(l);
    else grupos.push({ data: l.data, itens: [l] });
  }
  return grupos;
}

// ---------- Regras de recategorização ----------

export type RegrasSalvas = { porContraparte: Record<string, string>; porTransacao: Record<string, string> };
export const REGRAS_VAZIAS: RegrasSalvas = { porContraparte: {}, porTransacao: {} };

/** Cria a regra: com contraparte e `soEsta=false`, vale para todas com a mesma contraparte; senão, só para esta linha. */
export function adicionarRegra(regras: RegrasSalvas, l: Lancamento, categoria: string, soEsta: boolean): RegrasSalvas {
  if (l.contraparte && !soEsta) {
    return { ...regras, porContraparte: { ...regras.porContraparte, [l.contraparte]: categoria } };
  }
  return { ...regras, porTransacao: { ...regras.porTransacao, [chaveTransacao(l)]: categoria } };
}

export const paraRegrasUsuario = (r: RegrasSalvas): RegrasUsuario => r;

export function formatarDia(data: string): string {
  const [a, m, d] = data.split('-');
  return `${d}/${m}/${a}`;
}
