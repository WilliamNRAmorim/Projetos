// Metas de corte progressivo de gastos (Uber/99 e iFood/99Food). Funções puras, sem React Native.
import { CAT, contemPalavra, ehCompraCartao, norm } from './mp/categorias.ts';
import { mesAnteriorDe, mesDe, type Lancamento } from './mp/extrato.ts';
import { CORTE_DEGRAUS_PCT, CORTE_MESES_BASE } from './metasConfig.ts';
import { faixaOrcamento, r2, type Faixa } from './gastos/gastos.ts';

export type GrupoCorte = { id: 'transporte' | 'delivery'; nome: string; palavras: string[] };

export const GRUPOS_CORTE: GrupoCorte[] = [
  { id: 'transporte', nome: 'Uber e 99', palavras: ['uber', 'uberrides', '99pop', '99 pop', '99 tecnologia', '99tecnologia'] },
  { id: 'delivery', nome: 'iFood e 99Food', palavras: ['ifood', 'ifd', '99food', '99 food'] },
];

/** Saída real deste grupo? Movimento interno e estorno ficam de fora. */
const noGrupo = (l: Lancamento, g: GrupoCorte) =>
  l.valor < 0 && !l.excluida && l.categoria !== CAT.INTERNO && g.palavras.some((p) => contemPalavra(norm(`${l.contraparte} ${l.tipo}`), p));

export function gastoDoGrupo(lancs: Lancamento[], g: GrupoCorte, mes: string): number {
  return r2(lancs.filter((l) => mesDe(l.data) === mes && noGrupo(l, g)).reduce((s, l) => s - l.valor, 0));
}

export function proximoMes(mes: string): string {
  const [a, m] = mes.split('-').map(Number);
  return m === 12 ? `${a + 1}-01` : `${a}-${String(m + 1).padStart(2, '0')}`;
}

/** Meses desde o início do plano (0 = mês de início). */
export function mesesDesde(inicio: string, mes: string): number {
  const [a1, m1] = inicio.split('-').map(Number);
  const [a2, m2] = mes.split('-').map(Number);
  return (a2 - a1) * 12 + (m2 - m1);
}

/** % de corte do mês: 1º mês do plano = 1º degrau; passando do último, mantém. Antes do início: 0. */
export function degrauDoMes(inicio: string, mes: string): number {
  const i = mesesDesde(inicio, mes);
  if (i < 0) return 0;
  return CORTE_DEGRAUS_PCT[Math.min(i, CORTE_DEGRAUS_PCT.length - 1)];
}

/** Média mensal dos até `n` meses anteriores ao início que tenham algum lançamento. Sem dados ou sem gasto: null. */
export function baseDoGrupo(lancs: Lancamento[], g: GrupoCorte, inicio: string, n = CORTE_MESES_BASE): number | null {
  const meses: string[] = [];
  let m = inicio;
  for (let i = 0; i < n; i++) {
    m = mesAnteriorDe(m);
    if (lancs.some((l) => mesDe(l.data) === m)) meses.push(m);
  }
  if (meses.length === 0) return null;
  const media = meses.reduce((s, x) => s + gastoDoGrupo(lancs, g, x), 0) / meses.length;
  return media > 0 ? r2(media) : null;
}

export type MetaCorte = {
  grupo: GrupoCorte;
  base: number | null;
  degrau: number; // % de corte no mês
  teto: number | null;
  gasto: number;
  pct: number | null;
  faixa: Faixa | null;
  proximoDegrau: number;
  proximoTeto: number | null;
};

/** Bases congeladas no início do plano, por grupo. Sem base congelada, calcula do extrato. */
export type BasesCorte = Partial<Record<GrupoCorte['id'], number>>;

export function metaDeCorte(lancs: Lancamento[], g: GrupoCorte, inicio: string, mes: string, bases: BasesCorte = {}): MetaCorte {
  const base = bases[g.id] ?? baseDoGrupo(lancs, g, inicio);
  const degrau = degrauDoMes(inicio, mes);
  const proximoDegrau = degrauDoMes(inicio, proximoMes(mes));
  const aplicar = (b: number, d: number) => r2(b * (1 - d / 100));
  const teto = base === null ? null : aplicar(base, degrau);
  const gasto = gastoDoGrupo(lancs, g, mes);
  const pct = teto && teto > 0 ? r2((gasto / teto) * 100) : null;
  return {
    grupo: g, base, degrau, teto, gasto, pct,
    faixa: pct === null ? null : faixaOrcamento(pct),
    proximoDegrau,
    proximoTeto: base === null ? null : aplicar(base, proximoDegrau),
  };
}

export const metasDeCorte = (lancs: Lancamento[], inicio: string, mes: string, bases: BasesCorte = {}): MetaCorte[] =>
  GRUPOS_CORTE.map((g) => metaDeCorte(lancs, g, inicio, mes, bases));

/** A base só é confiável se CADA um dos meses que a formam tem compras de cartão importadas. */
export function cartaoCobreABase(lancs: Lancamento[], inicio: string, n = CORTE_MESES_BASE): boolean {
  let m = inicio;
  for (let i = 0; i < n; i++) {
    m = mesAnteriorDe(m);
    if (!lancs.some((l) => mesDe(l.data) === m && ehCompraCartao(l.tipo))) return false;
  }
  return true;
}

/** Bases a gravar agora: as que ainda não estão congeladas e já têm valor. `cartaoCompleto` (cartaoCobreABase) evita
 * travar uma base baixa calculada com meses só de Pix. */
export function basesParaCongelar(metas: MetaCorte[], congeladas: BasesCorte, cartaoCompleto: boolean): BasesCorte {
  const novas: BasesCorte = {};
  if (!cartaoCompleto) return novas;
  for (const m of metas) if (congeladas[m.grupo.id] === undefined && m.base !== null) novas[m.grupo.id] = m.base;
  return novas;
}
