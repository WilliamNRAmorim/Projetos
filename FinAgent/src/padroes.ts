// Padrões de gasto por semana (Uber/99, iFood/99Food) e meta semanal que se adapta. Funções puras, sem React Native.
// Estatística simples e local: nada daqui sai do aparelho (o economista recebe só percentuais, ver resumoPadroesPct).
import { CORTE_DEGRAUS_PCT } from './metasConfig.ts';
import { GRUPOS_CORTE, noGrupo, type GrupoCorte } from './cortes.ts';
import { ehCompraCartao } from './mp/categorias.ts';
import type { Lancamento } from './mp/extrato.ts';

export const DIAS_SEMANA = ['segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'domingo'] as const;

/** Mínimo de semanas fechadas para dizer que há padrão. Abaixo disso, a tela pede mais faturas. */
export const MIN_SEMANAS = 8;
/** Mínimo de semanas COM gasto no grupo; sem isso o "padrão" seria só zeros. */
export const MIN_SEMANAS_COM_GASTO = 3;
/** O padrão olha só as últimas semanas antes do plano (um trimestre): hábito de um ano atrás não é o seu ritmo de hoje. */
export const HISTORICO_SEMANAS = 13;
/** Mínimo de semanas depois de contida (ou solta) para falar em probabilidade. */
export const MIN_AMOSTRA_TRANSICAO = 3;
/** Semanas seguidas dentro do alvo para descer um nível, e semanas seguidas estouradas para subir um. */
export const SEMANAS_PARA_DESCER = 2;
export const SEMANAS_PARA_RELAXAR = 2;
/** A compensação de uma semana solta é metade do excesso, no máximo 20% do alvo da semana seguinte. */
export const COMPENSACAO_FRACAO = 0.5;
export const COMPENSACAO_MAX_PCT_ALVO = 0.2;

const r2 = (n: number) => Math.round(n * 100) / 100;

// ---------- datas (ISO YYYY-MM-DD, sem fuso) ----------

const utc = (iso: string) => new Date(`${iso}T00:00:00Z`);
const iso = (d: Date) => d.toISOString().slice(0, 10);
export const somarDias = (data: string, n: number) => iso(new Date(utc(data).getTime() + n * 86400000));
/** 0 = segunda ... 6 = domingo. */
export const diaDaSemana = (data: string) => (utc(data).getUTCDay() + 6) % 7;
export const inicioDaSemana = (data: string) => somarDias(data, -diaDaSemana(data));
export const dataLocal = (d: Date) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;

// ---------- semanas ----------

export type Semana = { inicio: string; total: number; porDia: number[] };

/** Até que dia há dado importado. Com compras de cartão importadas, vale a última compra do cartão (a fatura do mês
 * ainda não importada não pode virar "semana sem gasto"); sem cartão, a última data do extrato. */
export function coberturaAte(lancs: Lancamento[]): string | null {
  const datas = lancs.filter((l) => ehCompraCartao(l.tipo)).map((l) => l.data);
  const base = datas.length > 0 ? datas : lancs.map((l) => l.data);
  return base.length === 0 ? null : base.reduce((a, b) => (a > b ? a : b));
}

/** Semanas fechadas (segunda a domingo) desde a primeira data do extrato até a semana ANTERIOR a `semanaAtual`, com zeros
 * incluídos, mas só as inteiramente cobertas por dado importado. */
export function semanasFechadas(lancs: Lancamento[], g: GrupoCorte, semanaAtual: string): Semana[] {
  const coberto = coberturaAte(lancs);
  if (lancs.length === 0 || coberto === null) return [];
  const limite = [semanaAtual, inicioDaSemana(somarDias(coberto, 1))].sort()[0];
  const primeira = lancs.reduce((min, l) => (l.data < min ? l.data : min), lancs[0].data);
  const mapa = new Map<string, number[]>();
  for (let s = inicioDaSemana(primeira); s < limite; s = somarDias(s, 7)) mapa.set(s, [0, 0, 0, 0, 0, 0, 0]);
  for (const l of lancs) {
    if (!noGrupo(l, g)) continue;
    const dias = mapa.get(inicioDaSemana(l.data));
    if (dias) dias[diaDaSemana(l.data)] = Math.max(0, dias[diaDaSemana(l.data)] - l.valor); // estorno não deixa o dia negativo
  }
  return [...mapa.entries()].map(([inicio, porDia]) => ({ inicio, porDia: porDia.map(r2), total: r2(porDia.reduce((a, b) => a + b, 0)) }));
}

// ---------- estatística ----------

function quantil(ordenado: number[], q: number): number {
  if (ordenado.length === 0) return 0;
  const pos = (ordenado.length - 1) * q;
  const i = Math.floor(pos);
  const frac = pos - i;
  return ordenado[i] + (i + 1 < ordenado.length ? (ordenado[i + 1] - ordenado[i]) * frac : 0);
}
const mediana = (v: number[]) => quantil([...v].sort((a, b) => a - b), 0.5);

export type PerfilSemanal = {
  semanas: number;
  mediana: number;
  contida: number; // semana típica entre as mais contidas (mediana do terço inferior)
  solta: number; // semana típica entre as mais soltas (mediana do terço superior)
  limiteContida: number; // até aqui conta como semana contida
  limiteSolta: number; // a partir daqui conta como semana solta
};

export function perfilSemanal(sem: Semana[]): PerfilSemanal | null {
  if (sem.length < MIN_SEMANAS || sem.filter((s) => s.total > 0).length < MIN_SEMANAS_COM_GASTO) return null;
  const ord = sem.map((s) => s.total).sort((a, b) => a - b);
  if (quantil(ord, 0.5) <= 0) return null; // mediana zero: a maior parte das semanas sem gasto, alvo não faria sentido
  const limiteContida = quantil(ord, 1 / 3);
  const limiteSolta = quantil(ord, 2 / 3);
  const terco = Math.max(1, Math.floor(ord.length / 3));
  return {
    semanas: sem.length,
    mediana: r2(quantil(ord, 0.5)),
    contida: r2(mediana(ord.slice(0, terco))),
    solta: r2(mediana(ord.slice(ord.length - terco))),
    limiteContida: r2(limiteContida),
    limiteSolta: r2(limiteSolta),
  };
}

export type TipoSemana = 'contida' | 'media' | 'solta';
export function tipoDaSemana(total: number, p: PerfilSemanal): TipoSemana {
  if (total <= p.limiteContida) return 'contida';
  if (total >= p.limiteSolta && total > p.limiteContida) return 'solta';
  return 'media';
}

export type Transicao = { amostra: number; pSolta: number } | null;
/** Chance (%) de a semana seguinte ser solta, depois de uma semana contida e depois de uma solta. */
export function transicoes(sem: Semana[], p: PerfilSemanal): { aposContida: Transicao; aposSolta: Transicao } {
  const conta = { contida: [0, 0], solta: [0, 0] }; // [amostra, seguintes soltas]
  for (let i = 0; i + 1 < sem.length; i++) {
    const t = tipoDaSemana(sem[i].total, p);
    if (t === 'media') continue;
    conta[t][0]++;
    if (tipoDaSemana(sem[i + 1].total, p) === 'solta') conta[t][1]++;
  }
  const f = ([n, s]: number[]): Transicao => (n >= MIN_AMOSTRA_TRANSICAO ? { amostra: n, pSolta: Math.round((s / n) * 100) } : null);
  return { aposContida: f(conta.contida), aposSolta: f(conta.solta) };
}

/** Quanto do gasto (%) cai em cada dia da semana. Todos zero se não houve gasto. */
export function padraoPorDia(sem: Semana[]): number[] {
  const tot = [0, 0, 0, 0, 0, 0, 0];
  for (const s of sem) s.porDia.forEach((v, i) => (tot[i] += v));
  const soma = tot.reduce((a, b) => a + b, 0);
  return tot.map((v) => (soma > 0 ? Math.round((v / soma) * 100) : 0));
}

/** Gasto acumulado médio ao fim de cada dia da semana, nas semanas soltas e nas contidas. */
export function ritmoAcumulado(sem: Semana[], p: PerfilSemanal): { solta: number[]; contida: number[] } {
  const media = (tipo: TipoSemana) => {
    const alvo = sem.filter((s) => tipoDaSemana(s.total, p) === tipo);
    return [0, 1, 2, 3, 4, 5, 6].map((d) => {
      if (alvo.length === 0) return 0;
      return r2(alvo.reduce((acc, s) => acc + s.porDia.slice(0, d + 1).reduce((a, b) => a + b, 0), 0) / alvo.length);
    });
  };
  return { solta: media('solta'), contida: media('contida') };
}

// ---------- meta semanal que se adapta ----------

const NIVEL_MAX = CORTE_DEGRAUS_PCT.length;

/** Alvo do nível: do nível 0 (a semana mediana) ao último (a semana contida típica), sem passar do corte máximo da configuração. */
export function alvoDoNivel(p: PerfilSemanal, nivel: number): number {
  const n = Math.max(0, Math.min(NIVEL_MAX, nivel));
  const teorico = p.mediana - (n / NIVEL_MAX) * (p.mediana - Math.min(p.contida, p.mediana));
  const piso = p.mediana * (1 - CORTE_DEGRAUS_PCT[NIVEL_MAX - 1] / 100);
  return r2(Math.max(teorico, piso));
}

export type EstadoPlano = {
  nivel: number; // 0..3
  alvo: number; // alvo do nível
  compensacao: number; // quanto a semana solta anterior reduz o alvo desta semana
  alvoEfetivo: number; // alvo - compensação
  seguidasNoAlvo: number;
  semanasNoPlano: number;
};

/**
 * Percorre as semanas fechadas DESDE o início do plano. Desce um nível depois de SEMANAS_PARA_DESCER semanas seguidas dentro do alvo;
 * sobe um nível (relaxa) só depois de SEMANAS_PARA_RELAXAR semanas seguidas estouradas. Uma semana solta isolada não muda o nível:
 * só compensa parte do excesso na semana seguinte.
 */
export function estadoDoPlano(semanasPlano: Semana[], p: PerfilSemanal): EstadoPlano {
  let nivel = 0;
  let seguidas = 0;
  let estouros = 0;
  let compensacao = 0;
  for (const s of semanasPlano) {
    const alvo = alvoDoNivel(p, nivel);
    const efetivo = Math.max(0, alvo - compensacao);
    if (s.total <= efetivo) {
      seguidas++;
      estouros = 0;
      compensacao = 0;
      if (seguidas >= SEMANAS_PARA_DESCER && nivel < NIVEL_MAX) {
        nivel++;
        seguidas = 0;
      }
    } else {
      seguidas = 0;
      estouros++;
      compensacao = Math.min((s.total - efetivo) * COMPENSACAO_FRACAO, alvo * COMPENSACAO_MAX_PCT_ALVO);
      if (estouros >= SEMANAS_PARA_RELAXAR && nivel > 0) {
        nivel--;
        estouros = 0;
      }
    }
  }
  const alvo = alvoDoNivel(p, nivel);
  return { nivel, alvo, compensacao: r2(compensacao), alvoEfetivo: r2(Math.max(0, alvo - compensacao)), seguidasNoAlvo: seguidas, semanasNoPlano: semanasPlano.length };
}

// ---------- semana em andamento ----------

export type RitmoAtual = 'contido' | 'medio' | 'solto';
export type SemanaAtual = {
  inicio: string;
  diaIndice: number; // 0 = segunda ... 6 = domingo (hoje)
  gasto: number;
  restante: number; // alvo efetivo - gasto (negativo = passou)
  tipicoSolta: number; // acumulado típico de uma semana solta até hoje
  tipicoContida: number;
  ritmo: RitmoAtual;
};

export function semanaAtual(lancs: Lancamento[], g: GrupoCorte, hoje: string, alvoEfetivo: number, p: PerfilSemanal, rit: { solta: number[]; contida: number[] }): SemanaAtual {
  const inicio = inicioDaSemana(hoje);
  const diaIndice = diaDaSemana(hoje);
  const gasto = r2(lancs.filter((l) => noGrupo(l, g) && l.data >= inicio && l.data <= hoje).reduce((s, l) => s - l.valor, 0));
  const tipicoSolta = rit.solta[diaIndice];
  const tipicoContida = rit.contida[diaIndice];
  const ritmo: RitmoAtual = gasto >= Math.max(tipicoSolta * 0.9, p.limiteContida * 0.5) && gasto > tipicoContida * 1.2 ? 'solto' : gasto <= tipicoContida * 1.1 ? 'contido' : 'medio';
  return { inicio, diaIndice, gasto, restante: r2(alvoEfetivo - gasto), tipicoSolta, tipicoContida, ritmo };
}

// ---------- tudo junto ----------

export type AnalisePadroes = {
  grupo: GrupoCorte;
  perfil: PerfilSemanal;
  dias: number[];
  diaMaisSolto: number;
  transicao: ReturnType<typeof transicoes>;
  plano: EstadoPlano;
  atual: SemanaAtual;
};

/** Primeira segunda-feira em ou depois do dia 1 do mês de início do plano. */
export function primeiraSemanaDoPlano(inicioMes: string): string {
  const d = `${inicioMes}-01`;
  const dow = diaDaSemana(d);
  return dow === 0 ? d : somarDias(d, 7 - dow);
}

/** Null se ainda não há semanas suficientes antes do plano para aprender o padrão. */
export function analisarPadroes(lancs: Lancamento[], g: GrupoCorte, inicioMes: string, hoje: string): AnalisePadroes | null {
  const semHoje = inicioDaSemana(hoje);
  const todas = semanasFechadas(lancs, g, semHoje);
  const iniPlano = primeiraSemanaDoPlano(inicioMes);
  const historico = todas.filter((s) => s.inicio < iniPlano).slice(-HISTORICO_SEMANAS);
  const perfil = perfilSemanal(historico);
  if (!perfil) return null;
  const plano = estadoDoPlano(todas.filter((s) => s.inicio >= iniPlano), perfil);
  const dias = padraoPorDia(historico);
  const rit = ritmoAcumulado(historico, perfil);
  return {
    grupo: g,
    perfil,
    dias,
    diaMaisSolto: dias.indexOf(Math.max(...dias)),
    transicao: transicoes(historico, perfil),
    plano,
    atual: semanaAtual(lancs, g, hoje, plano.alvoEfetivo, perfil, rit),
  };
}

export const analisarTodos = (lancs: Lancamento[], inicioMes: string, hoje: string): AnalisePadroes[] =>
  GRUPOS_CORTE.map((g) => analisarPadroes(lancs, g, inicioMes, hoje)).filter((a): a is AnalisePadroes => a !== null);

/** Para o economista: SÓ percentuais e nomes de dia, nenhum valor em reais. */
export type ResumoPadroes = {
  grupo: string;
  semanas_analisadas: number;
  semana_solta_gasta_a_mais_pct: number | null; // quanto a semana solta típica gasta a mais que a contida típica
  dia_mais_solto: string;
  chance_solta_apos_contida_pct: number | null;
  chance_solta_apos_solta_pct: number | null;
  nivel_do_plano: string; // "2 de 3"
};

export function resumoPadroesPct(lancs: Lancamento[], inicioMes: string, hoje: string): ResumoPadroes[] {
  return analisarTodos(lancs, inicioMes, hoje).map((a) => ({
    grupo: a.grupo.nome,
    semanas_analisadas: a.perfil.semanas,
    semana_solta_gasta_a_mais_pct: a.perfil.contida > 0 ? Math.round(((a.perfil.solta - a.perfil.contida) / a.perfil.contida) * 100) : null,
    dia_mais_solto: DIAS_SEMANA[a.diaMaisSolto],
    chance_solta_apos_contida_pct: a.transicao.aposContida?.pSolta ?? null,
    chance_solta_apos_solta_pct: a.transicao.aposSolta?.pSolta ?? null,
    nivel_do_plano: `${a.plano.nivel} de ${NIVEL_MAX}`,
  }));
}
