// Funções puras das Metas (sem React Native). Valores monetários em reais.
import { norm } from './mp/categorias.ts';
import { classificarExtrato, mesDe, mesesDisponiveis, parseValorBR, totaisMes, type Transacao } from './mp/extrato.ts';
import { LIMITE_ATENCAO_ATE, LIMITE_OK_ATE, MESES_NA_MEDIA } from './metasConfig.ts';

/** Perfil como o usuário digitou (texto). Padrão vazio. */
export type PerfilTexto = {
  salario: string;
  diaSalario: string;
  parcela: string;
  diaParcela: string;
  parcelasRestantes: string;
  cofrinho: string;
  separadoAparelho: string;
  limiteCartao: string;
  faturaAberta: string;
  diaFechamento: string;
  diaVencimento: string;
};

export const PERFIL_VAZIO: PerfilTexto = {
  salario: '', diaSalario: '', parcela: '', diaParcela: '', parcelasRestantes: '',
  cofrinho: '', separadoAparelho: '', limiteCartao: '', faturaAberta: '', diaFechamento: '', diaVencimento: '',
};

export type PerfilNum = { [K in keyof PerfilTexto]: number | null };

const CAMPOS_DIA: (keyof PerfilTexto)[] = ['diaSalario', 'diaParcela', 'diaFechamento', 'diaVencimento'];
const CAMPOS_INTEIRO: (keyof PerfilTexto)[] = [...CAMPOS_DIA, 'parcelasRestantes'];

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

export type Livre = { valor: number; porDia: number | null; dias: number };

/**
 * Livre até o salário = saldo da conta (extrato) - fatura aberta - parte da parcela que o separado do aparelho não cobre.
 * Estimativa: não inclui o Cofrinho (reserva) e supõe que o saldo do extrato é o da conta.
 */
export function livreAteSalario(saldoConta: number, p: PerfilNum, hoje: Date): Livre | null {
  if (p.diaSalario === null) return null;
  const parcela = p.parcelasRestantes === 0 ? 0 : p.parcela ?? 0;
  const faltaParcela = Math.max(0, parcela - (p.separadoAparelho ?? 0));
  const valor = r2(saldoConta - (p.faturaAberta ?? 0) - faltaParcela);
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

export type MediaGasto = { media: number; meses: string[] };

/**
 * Média mensal de gasto (gastos sem movimento interno + fatura paga) dos últimos `n` meses do extrato.
 * O mês corrente (incompleto) fica de fora se houver outros meses.
 */
export function mediaGastoMensal(trans: Transacao[], meuNome: string, hoje: Date, n = MESES_NA_MEDIA): MediaGasto | null {
  const todos = mesesDisponiveis(trans);
  if (todos.length === 0) return null;
  const atual = mesDe(`${hoje.getFullYear()}-${String(hoje.getMonth() + 1).padStart(2, '0')}-01`);
  const fechados = todos.filter((m) => m !== atual);
  const usar = (fechados.length > 0 ? fechados : todos).slice(0, n);
  const lancs = classificarExtrato(trans, meuNome);
  const soma = usar.reduce((acc, m) => {
    const t = totaisMes(lancs, m);
    return acc + t.gastos + t.fatura;
  }, 0);
  return { media: r2(soma / usar.length), meses: usar };
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
