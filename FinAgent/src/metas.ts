// Funções puras das Metas (sem React Native). Valores monetários em reais.
import { ehCompraCartao, norm } from './mp/categorias.ts';
import { classificarExtrato, mesDe, mesesDisponiveis, parseValorBR, totaisMes, type RegrasUsuario, type Transacao } from './mp/extrato.ts';
import { LIMITE_ATENCAO_ATE, LIMITE_OK_ATE, MESES_NA_MEDIA } from './metasConfig.ts';

/** Perfil como o usuário digitou (texto). Padrão vazio. */
export type PerfilTexto = {
  salario: string;
  diaSalario: string;
  parcela: string;
  diaParcela: string;
  parcelasRestantes: string;
  parcelasMin: string; // faixa de parcelas restantes (incerteza), opcional
  parcelasMax: string;
  cofrinho: string;
  separadoAparelho: string;
  limiteCartao: string;
  faturaAberta: string;
  diaFechamento: string;
  diaVencimento: string;
};

export const PERFIL_VAZIO: PerfilTexto = {
  salario: '', diaSalario: '', parcela: '', diaParcela: '', parcelasRestantes: '', parcelasMin: '', parcelasMax: '',
  cofrinho: '', separadoAparelho: '', limiteCartao: '', faturaAberta: '', diaFechamento: '', diaVencimento: '',
};

export type PerfilNum = { [K in keyof PerfilTexto]: number | null };

const CAMPOS_DIA: (keyof PerfilTexto)[] = ['diaSalario', 'diaParcela', 'diaFechamento', 'diaVencimento'];
const CAMPOS_INTEIRO: (keyof PerfilTexto)[] = [...CAMPOS_DIA, 'parcelasRestantes', 'parcelasMin', 'parcelasMax'];

/** Valida um campo. Retorna mensagem de erro ou null (vazio é válido). */
export function validarCampo(campo: keyof PerfilTexto, texto: string): string | null {
  if (!texto.trim()) return null;
  const n = parseValorBR(texto);
  if (n === null) return 'Número inválido. Use o formato 1.234,56.';
  if (n < 0) return 'Não pode ser negativo.';
  if (CAMPOS_INTEIRO.includes(campo) && !Number.isInteger(n)) return 'Use um número inteiro.';
  if (CAMPOS_DIA.includes(campo) && (n < 1 || n > 31)) return 'Dia entre 1 e 31.';
  return null;
}

export function validarPerfil(p: PerfilTexto): Partial<Record<keyof PerfilTexto, string>> {
  const erros: Partial<Record<keyof PerfilTexto, string>> = {};
  for (const k of Object.keys(p) as (keyof PerfilTexto)[]) {
    const e = validarCampo(k, p[k]);
    if (e) erros[k] = e;
  }
  const min = parseValorBR(p.parcelasMin);
  const max = parseValorBR(p.parcelasMax);
  if (!erros.parcelasMax && min !== null && max !== null && max < min) erros.parcelasMax = 'O máximo não pode ser menor que o mínimo.';
  return erros;
}

export function perfilParaNumeros(p: PerfilTexto): PerfilNum {
  const out = {} as PerfilNum;
  for (const k of Object.keys(PERFIL_VAZIO) as (keyof PerfilTexto)[]) {
    out[k] = validarCampo(k, p[k]) || !p[k].trim() ? null : parseValorBR(p[k]);
  }
  return out;
}

const r2 = (n: number) => Math.round(n * 100) / 100;

export type Comprometido = { parcela: number; fatura: number; total: number; pctSalario: number | null };

/** Comprometido do mês = parcela do aparelho (se ainda restam parcelas) + fatura aberta. */
export function comprometidoDoMes(p: PerfilNum): Comprometido {
  const parcela = p.parcelasRestantes === 0 ? 0 : p.parcela ?? 0;
  const fatura = p.faturaAberta ?? 0;
  const total = r2(parcela + fatura);
  return { parcela, fatura, total, pctSalario: p.salario && p.salario > 0 ? r2((total / p.salario) * 100) : null };
}

/** Dias corridos de `hoje` até o próximo dia de salário (0 = é hoje). Dia 30 em fevereiro cai no último dia. */
export function diasAteSalario(hoje: Date, dia: number): number {
  const ini = new Date(hoje.getFullYear(), hoje.getMonth(), hoje.getDate());
  const alvo = (ano: number, mes: number) => new Date(ano, mes, Math.min(dia, new Date(ano, mes + 1, 0).getDate()));
  let t = alvo(ini.getFullYear(), ini.getMonth());
  if (t < ini) t = alvo(ini.getFullYear(), ini.getMonth() + 1);
  return Math.round((t.getTime() - ini.getTime()) / 86400000);
}

/** Próxima data (hoje inclusive) em que cai o dia `dia` do mês; mês curto cai no último dia. */
function proximaData(hoje: Date, dia: number): Date {
  const ini = new Date(hoje.getFullYear(), hoje.getMonth(), hoje.getDate());
  const alvo = (ano: number, mes: number) => new Date(ano, mes, Math.min(dia, new Date(ano, mes + 1, 0).getDate()));
  const t = alvo(ini.getFullYear(), ini.getMonth());
  return t < ini ? alvo(ini.getFullYear(), ini.getMonth() + 1) : t;
}

/** Vence antes do próximo salário? Sem o dia do vencimento (ou do salário), assume que sim (conservador). */
function venceAntesDoSalario(hoje: Date, diaVenc: number | null, diaSalario: number): boolean {
  if (diaVenc === null) return true;
  return proximaData(hoje, diaVenc) < proximaData(hoje, diaSalario);
}

export type Livre = { valor: number; porDia: number | null; dias: number };

/**
 * Livre até o salário = saldo da conta (extrato) - fatura aberta - parte da parcela que o separado do aparelho não cobre.
 * Só entra o que sai da conta ANTES do próximo salário: a fatura aberta só é subtraída se o vencimento cai antes do
 * salário (senão sai do próximo salário) e a parcela só se o dia dela ainda não passou neste ciclo (a próxima data
 * da parcela vem antes do salário). Sem o dia do vencimento/da parcela, subtrai (conservador).
 * Estimativa: não inclui o Cofrinho nem o separado do aparelho (ficam na reserva, fora do saldo da conta).
 */
export function livreAteSalario(saldoConta: number, p: PerfilNum, hoje: Date): Livre | null {
  if (p.diaSalario === null) return null;
  const parcelaCheia = p.parcelasRestantes === 0 ? 0 : p.parcela ?? 0;
  const parcelaNoCiclo = p.diaParcela === null || proximaData(hoje, p.diaParcela) < proximaData(hoje, p.diaSalario) ? parcelaCheia : 0;
  const faltaParcela = Math.max(0, parcelaNoCiclo - (p.separadoAparelho ?? 0));
  const fatura = venceAntesDoSalario(hoje, p.diaVencimento, p.diaSalario) ? p.faturaAberta ?? 0 : 0;
  const valor = r2(saldoConta - fatura - faltaParcela);
  const dias = diasAteSalario(hoje, p.diaSalario);
  return { valor, dias, porDia: dias > 0 ? r2(valor / dias) : null };
}

export type Faixa = 'ok' | 'atencao' | 'alerta';

export function usoLimite(limite: number | null, usado: number | null): number | null {
  if (!limite || limite <= 0 || usado === null) return null;
  return r2((usado / limite) * 100);
}

/** <30% ok, 30-60% atenção, >60% alerta (limites em metasConfig.ts). */
export function faixaLimite(pct: number): Faixa {
  if (pct < LIMITE_OK_ATE) return 'ok';
  return pct <= LIMITE_ATENCAO_ATE ? 'atencao' : 'alerta';
}

/** `parcial`: só havia meses incompletos; a média é uma estimativa. */
export type MediaGasto = { media: number; meses: string[]; parcial?: boolean };

/**
 * Média mensal de gasto (gastos sem movimento interno + fatura paga) dos últimos `n` meses do extrato.
 * Meses parciais ficam de fora: o mês corrente e o primeiro mês do extrato quando ele não começa nos dias 1 a 3.
 * Se só houver meses parciais, usa todos e devolve `parcial: true` (estimativa com mês incompleto).
 */
export function mediaGastoMensal(trans: Transacao[], meuNome: string, hoje: Date, n = MESES_NA_MEDIA, regras?: RegrasUsuario): MediaGasto | null {
  const todos = mesesDisponiveis(trans);
  if (todos.length === 0) return null;
  const atual = mesDe(`${hoje.getFullYear()}-${String(hoje.getMonth() + 1).padStart(2, '0')}-01`);
  const daConta = trans.filter((t) => !ehCompraCartao(t.tipo));
  const primeiraData = daConta.reduce((min, t) => (t.data < min ? t.data : min), daConta[0].data);
  const primeiroParcial = Number(primeiraData.slice(8)) > 3 ? mesDe(primeiraData) : null;
  const completos = todos.filter((m) => m !== atual && m !== primeiroParcial);
  const parcial = completos.length === 0;
  const usar = (parcial ? todos : completos).slice(0, n);
  const lancs = classificarExtrato(trans, meuNome, regras);
  const soma = usar.reduce((acc, m) => {
    const t = totaisMes(lancs, m);
    return acc + t.gastos + t.fatura;
  }, 0);
  return parcial ? { media: r2(soma / usar.length), meses: usar, parcial: true } : { media: r2(soma / usar.length), meses: usar };
}

export const metaReserva = (media: number, meses: number) => r2(media * meses);

/** Progresso (0-100) do saldo contra a meta; null sem meta. */
export function progressoReserva(saldo: number, meta: number): number | null {
  return meta > 0 ? Math.min(100, r2((saldo / meta) * 100)) : null;
}

/** Quantos meses de gasto o saldo cobre. */
export function mesesDeReserva(saldo: number | null, media: number | null): number | null {
  if (saldo === null || !media || media <= 0) return null;
  return Math.round((saldo / media) * 10) / 10;
}

export type Retirada = { data: string; valor: number };

/** Retiradas do Cofrinho no extrato ("Dinheiro retirado Cofrinho"), da mais recente para a mais antiga. */
export function retiradasCofrinho(trans: Transacao[]): Retirada[] {
  return trans
    .filter((t) => {
      const n = norm(t.tipo);
      return n.startsWith('dinheiro retirado') && n.includes('cofrinho') && t.valor > 0;
    })
    .map((t) => ({ data: t.data, valor: r2(t.valor) }))
    .sort((a, b) => b.data.localeCompare(a.data));
}

export const dataCurta = (iso: string) => `${iso.slice(8)}/${iso.slice(5, 7)}`;

export type ResumoMetas = {
  salario: number | null;
  pctComprometido: number | null;
  pctLimite: number | null;
  mesesReserva: number | null;
};

export function resumoMetas(p: PerfilNum, media: number | null): ResumoMetas {
  return {
    salario: p.salario,
    pctComprometido: comprometidoDoMes(p).pctSalario,
    pctLimite: usoLimite(p.limiteCartao, p.faturaAberta),
    mesesReserva: mesesDeReserva(p.cofrinho, media),
  };
}
