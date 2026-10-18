// Funções puras do simulador do Cofrinho e projeções (sem React Native). Valores em reais.
import { classificarExtrato, mesDe, mesesDisponiveis, totaisMes, type Transacao } from '../mp/extrato.ts';

const r2 = (n: number) => Math.round(n * 100) / 100;

/** Taxa mensal equivalente a uma taxa anual em %: (1 + a)^(1/12) - 1. */
export function taxaMensal(anualPct: number): number {
  return Math.pow(1 + anualPct / 100, 1 / 12) - 1;
}

/** Taxa anual efetiva do produto = CDI anual x (% do CDI / 100). */
export const taxaAnualDoProduto = (cdiAnualPct: number, pctCdi: number) => cdiAnualPct * (pctCdi / 100);

/** Tabela regressiva de renda fixa pelo prazo em dias: 22,5% até 180; 20% até 360; 17,5% até 720; 15% acima. */
export function aliquotaIR(dias: number): number {
  if (dias <= 180) return 0.225;
  if (dias <= 360) return 0.2;
  if (dias <= 720) return 0.175;
  return 0.15;
}

export type SimEntrada = { saldoInicial: number; aporte: number; meses: number; taxaMensal: number };
export type SimResultado = {
  /** Saldo bruto e total aportado ao fim de cada mês (índice 0 = mês 1). */
  serie: { mes: number; aportado: number; saldo: number }[];
  aportado: number; // soma dos aportes (sem o saldo inicial)
  saldoBruto: number;
  rendimentoBruto: number;
  aliquota: number;
  ir: number;
  liquido: number; // saldo final menos o IR estimado
};

/**
 * Juros compostos mensais: a cada mês o saldo rende pela taxa e o aporte entra no fim do mês.
 * saldo(n) = saldo(n-1) x (1 + i) + aporte. IR: alíquota do prazo total (meses x 30 dias) sobre o rendimento (estimativa).
 */
export function simular(e: SimEntrada): SimResultado {
  const meses = Math.max(0, Math.floor(e.meses));
  let saldo = e.saldoInicial;
  const serie: SimResultado['serie'] = [];
  for (let m = 1; m <= meses; m++) {
    saldo = saldo * (1 + e.taxaMensal) + e.aporte;
    serie.push({ mes: m, aportado: r2(e.aporte * m), saldo: r2(saldo) });
  }
  const aportado = r2(e.aporte * meses);
  const rend = Math.max(0, saldo - e.saldoInicial - aportado);
  const aliquota = aliquotaIR(meses * 30);
  const ir = r2(rend * aliquota);
  return {
    serie, aportado, saldoBruto: r2(saldo), rendimentoBruto: r2(rend), aliquota, ir, liquido: r2(saldo - ir),
  };
}

/** Atalho: simula a partir do CDI anual (%) e do % do CDI do produto. */
export function simularCofrinho(p: { saldoInicial: number; aporte: number; meses: number; cdiAnualPct: number; pctCdi: number }): SimResultado {
  return simular({ ...p, taxaMensal: taxaMensal(taxaAnualDoProduto(p.cdiAnualPct, p.pctCdi)) });
}

/** Quantos meses de gasto o valor cobre (1 casa). */
export function mesesCobertos(valor: number, mediaGasto: number | null): number | null {
  if (!mediaGasto || mediaGasto <= 0) return null;
  return Math.round((valor / mediaGasto) * 10) / 10;
}

/** Reduz a série a no máximo `max` pontos (sempre inclui o último), para o gráfico. */
export function amostrarSerie<T>(serie: T[], max = 12): T[] {
  if (serie.length <= max) return serie;
  const out: T[] = [];
  for (let i = 0; i < max; i++) out.push(serie[Math.round(((i + 1) * serie.length) / max) - 1]);
  return out;
}

// ---- CDI (API do Banco Central, série SGS 4389) ----

export const URL_CDI_BCB = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.4389/dados/ultimos/1?formato=json';

/** Resposta do SGS: [{ data: "dd/MM/aaaa", valor: "14.90" }]. Retorna taxa anual (%) e data ISO, ou null se inválida. */
export function lerRespostaCdi(json: unknown): { taxa: number; data: string } | null {
  if (!Array.isArray(json) || json.length === 0) return null;
  const u = json[json.length - 1] as { data?: unknown; valor?: unknown };
  const taxa = Number(String(u?.valor ?? '').replace(',', '.'));
  const m = /^(\d{2})\/(\d{2})\/(\d{4})$/.exec(String(u?.data ?? ''));
  if (!m || !Number.isFinite(taxa) || taxa <= 0 || taxa > 100) return null;
  return { taxa, data: `${m[3]}-${m[2]}-${m[1]}` };
}

// ---- Fim do aparelho ----

export type MesAno = { ano: number; mes: number }; // mes 1-12

export const formatarMesAno = (m: MesAno) => `${String(m.mes).padStart(2, '0')}/${m.ano}`;

/** Soma `n` meses a um mês/ano. */
export function somarMeses(base: MesAno, n: number): MesAno {
  const idx = base.ano * 12 + (base.mes - 1) + n;
  return { ano: Math.floor(idx / 12), mes: (idx % 12) + 1 };
}

/**
 * Mês da última parcela. Supõe que as `restantes` parcelas incluem a deste mês:
 * a última cai em (mês atual + restantes - 1). Restantes <= 0: já terminou (null).
 */
export function mesDaUltimaParcela(hoje: Date, restantes: number): MesAno | null {
  if (!Number.isInteger(restantes) || restantes <= 0) return null;
  return somarMeses({ ano: hoje.getFullYear(), mes: hoje.getMonth() + 1 }, restantes - 1);
}

export type FaixaParcelas = { min: number; max: number };

/** Faixa de parcelas restantes: usa min/max do Perfil; só um deles vale como os dois; sem nenhum, usa o valor exato. */
export function faixaDeParcelas(min: number | null, max: number | null, exato: number | null): FaixaParcelas | null {
  const a = min ?? max ?? exato;
  const b = max ?? min ?? exato;
  if (a === null || b === null) return null;
  return { min: Math.min(a, b), max: Math.max(a, b) };
}

export type FimAparelho = { de: MesAno | null; ate: MesAno | null };

export function fimDoAparelho(hoje: Date, f: FaixaParcelas): FimAparelho {
  return { de: mesDaUltimaParcela(hoje, f.min), ate: mesDaUltimaParcela(hoje, f.max) };
}

export type Redirecionamento = {
  /** Saldo do Cofrinho no fim do aparelho (só rendimento, sem aportes). */
  saldoNoFim: number;
  /** Depois do fim: a parcela vai para o Cofrinho por `meses` meses. */
  depois: SimResultado;
};

/**
 * Cenário: o Cofrinho rende `mesesAteFim` meses sem aporte e, depois do fim do aparelho,
 * recebe a parcela todo mês durante `meses` meses (padrão 12).
 */
export function redirecionarParcela(p: {
  saldoInicial: number; parcela: number; mesesAteFim: number; taxaMensal: number; meses?: number;
}): Redirecionamento {
  const meses = p.meses ?? 12;
  const saldoNoFim = r2(p.saldoInicial * Math.pow(1 + p.taxaMensal, Math.max(0, p.mesesAteFim)));
  const depois = simular({ saldoInicial: saldoNoFim, aporte: p.parcela, meses, taxaMensal: p.taxaMensal });
  return { saldoNoFim, depois };
}

// ---- Se continuar assim ----

export type MediaLiquida = { media: number; meses: string[] };

/**
 * Média do líquido mensal dos últimos `n` meses fechados: entradas (sem transferência de outra conta
 * própria) - gastos - fatura paga; movimento interno (Cofrinho, Emergências) fica fora. Sem mês fechado, null.
 */
export function mediaLiquidoMensal(trans: Transacao[], meuNome: string, hoje: Date, n = 3): MediaLiquida | null {
  const atual = mesDe(`${hoje.getFullYear()}-${String(hoje.getMonth() + 1).padStart(2, '0')}-01`);
  const fechados = mesesDisponiveis(trans).filter((m) => m < atual).slice(0, n);
  if (fechados.length === 0) return null;
  const lancs = classificarExtrato(trans, meuNome);
  const soma = fechados.reduce((acc, m) => {
    const t = totaisMes(lancs, m);
    return acc + (t.entradas - t.entradasOutraConta) - t.gastos - t.fatura;
  }, 0);
  return { media: r2(soma / fechados.length), meses: fechados };
}

export type Projecao = { fimDoMes: number; dezembro: number; mesesAteDezembro: number };

/**
 * Projeção linear: saldo + líquido médio x tempo. Fim do mês = fração dos dias que faltam; dezembro soma os meses
 * inteiros seguintes. Se hoje já é dezembro, dezembro = fim do mês.
 */
export function projetarConta(saldo: number, liquidoMensal: number, hoje: Date): Projecao {
  const diasMes = new Date(hoje.getFullYear(), hoje.getMonth() + 1, 0).getDate();
  const fracao = (diasMes - hoje.getDate()) / diasMes;
  const inteiros = 11 - hoje.getMonth();
  return {
    fimDoMes: r2(saldo + liquidoMensal * fracao),
    dezembro: r2(saldo + liquidoMensal * (fracao + inteiros)),
    mesesAteDezembro: r2(fracao + inteiros),
  };
}

/** Cofrinho sem novos aportes (meta: não mexer): só rende pela taxa mensal. Tempo em meses (pode ser fracionado). */
export function projetarCofrinho(saldo: number, taxa: number, meses: number): number {
  return r2(saldo * Math.pow(1 + taxa, Math.max(0, meses)));
}
