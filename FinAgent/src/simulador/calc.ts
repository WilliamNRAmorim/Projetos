// Funções puras do simulador do Cofrinho e projeções (sem React Native). Valores em reais.
import { CAT, ehCompraCartao, ehMovimentoInterno } from '../mp/categorias.ts';
import { classificarExtrato, mesDe, mesesDisponiveis, totaisMes, type RegrasUsuario, type Transacao } from '../mp/extrato.ts';

const r2 = (n: number) => Math.round(n * 100) / 100;

/** Taxa mensal equivalente a uma taxa anual em %: (1 + a)^(1/12) - 1. */
export function taxaMensal(anualPct: number): number {
  return Math.pow(1 + anualPct / 100, 1 / 12) - 1;
}

/**
 * Taxa anual efetiva (%) de um produto que paga `pctCdi`% do CDI. O % incide sobre a taxa DIÁRIA do CDI
 * (252 dias úteis), depois capitaliza: diária = ((1 + CDI)^(1/252) - 1) x pct; anual = (1 + diária)^252 - 1.
 * Com 100% do CDI devolve o próprio CDI; com 120% e CDI de 14,9% dá cerca de 18,14% ao ano (não 17,88%).
 */
export function taxaAnualDoProduto(cdiAnualPct: number, pctCdi: number): number {
  const diariaCdi = Math.pow(1 + cdiAnualPct / 100, 1 / 252) - 1;
  const diariaProduto = diariaCdi * (pctCdi / 100);
  return (Math.pow(1 + diariaProduto, 252) - 1) * 100;
}

/** Prazo em dias corridos de um prazo em meses (ano de 365,25 dias): 6 meses = 183, 12 = 365, 24 = 731. */
export const diasDoPrazo = (meses: number) => Math.round((meses * 365.25) / 12);

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
 * saldo(n) = saldo(n-1) x (1 + i) + aporte. IR: alíquota do prazo total (meses x 365,25/12 dias) sobre o rendimento (estimativa: cada aporte tem prazo próprio).
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
  const aliquota = aliquotaIR(diasDoPrazo(meses));
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
 * Mês da última parcela. Supõe que as `restantes` parcelas incluem a deste mês (a última cai em mês atual + restantes - 1),
 * a menos que o dia da parcela deste mês já tenha passado: aí a deste mês está paga e a última cai em mês atual + restantes. Restantes <= 0: já terminou (null).
 */
export function mesDaUltimaParcela(hoje: Date, restantes: number, diaParcela: number | null = null): MesAno | null {
  if (!Number.isInteger(restantes) || restantes <= 0) return null;
  // Se a parcela deste mês já passou (dia da parcela < hoje), ela não conta como restante: a contagem começa no mês seguinte.
  const jaPassou = diaParcela !== null && hoje.getDate() > diaParcela;
  return somarMeses({ ano: hoje.getFullYear(), mes: hoje.getMonth() + 1 }, jaPassou ? restantes : restantes - 1);
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

export function fimDoAparelho(hoje: Date, f: FaixaParcelas, diaParcela: number | null = null): FimAparelho {
  return { de: mesDaUltimaParcela(hoje, f.min, diaParcela), ate: mesDaUltimaParcela(hoje, f.max, diaParcela) };
}

export type Redirecionamento = {
  /** Saldo do Cofrinho no fim do aparelho (só rendimento, sem aportes). */
  saldoNoFim: number;
  /**
   * Depois do fim: a parcela vai para o Cofrinho por `meses` meses. Valores BRUTOS: `depois.saldoBruto` e
   * `rendimentoBruto` vêm antes do IR; mostrar como "bruto" (o `liquido` do SimResultado é só uma estimativa grosseira).
   */
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

export type MediaLiquida = { media: number; meses: string[]; entradas: number; gastos: number; fatura: number };

/**
 * Média do líquido mensal dos últimos `n` meses fechados: entradas (inclui transferências da própria
 * conta: o salário costuma chegar assim) - gastos - fatura paga; movimento interno (Cofrinho, Emergências) fica fora. Sem mês fechado, null.
 * É CAIXA, não competência: com as compras do cartão importadas, `gastos` é só o que sai da conta no dia a dia
 * (sem as compras no cartão) e `fatura` é o que foi pago de fatura no mês, também quando as compras foram importadas.
 */
export function mediaLiquidoMensal(trans: Transacao[], meuNome: string, hoje: Date, n = 3, regras?: RegrasUsuario): MediaLiquida | null {
  const atual = mesDe(`${hoje.getFullYear()}-${String(hoje.getMonth() + 1).padStart(2, '0')}-01`);
  const fechados = mesesDisponiveis(trans).filter((m) => m < atual).slice(0, n);
  if (fechados.length === 0) return null;
  const lancs = classificarExtrato(trans, meuNome, regras);
  let ent = 0;
  let gas = 0;
  let fat = 0;
  for (const m of fechados) {
    const t = totaisMes(lancs, m);
    const noCartao = lancs.reduce((s, l) => (mesDe(l.data) === m && !l.excluida && l.valor < 0 && ehCompraCartao(l.tipo) && !ehMovimentoInterno(l.categoria) && l.categoria !== CAT.FATURA ? s - l.valor : s), 0);
    const faturaQuitada = lancs.reduce((s, l) => (mesDe(l.data) === m && !l.excluida && l.faturaQuitada && l.valor < 0 ? s - l.valor : s), 0);
    ent += t.entradas;
    gas += t.gastos - noCartao;
    fat += t.fatura + faturaQuitada;
  }
  const n2 = fechados.length;
  return { media: r2((ent - gas - fat) / n2), meses: fechados, entradas: r2(ent / n2), gastos: r2(gas / n2), fatura: r2(fat / n2) };
}

export type Projecao = { fimDoMes: number; dezembro: number; mesesAteDezembro: number; salarioPendente: boolean };

/**
 * Projeção da CONTA (saldo do extrato; não inclui o Cofrinho). Separa o que cai de uma vez do gasto diário:
 * - gastos do dia a dia: média mensal x fração do mês que falta (gasta-se aos poucos);
 * - se o dia do salário ainda NÃO passou neste mês: soma as entradas médias e subtrai a fatura média (paga no dia do salário);
 * - se já passou: o salário e a fatura já estão no saldo, não entram de novo (não soma fração de salário já recebido).
 * Sem o dia do salário, cai na projeção linear antiga (líquido x fração). Dezembro soma os meses inteiros seguintes
 * (líquido médio). Hoje em dezembro: dezembro = fim do mês.
 */
export function projetarConta(
  saldo: number,
  media: { entradas: number; gastos: number; fatura: number },
  hoje: Date,
  diaSalario: number | null,
): Projecao {
  const diasMes = new Date(hoje.getFullYear(), hoje.getMonth() + 1, 0).getDate();
  const fracao = (diasMes - hoje.getDate()) / diasMes;
  const inteiros = 11 - hoje.getMonth();
  const liquido = media.entradas - media.gastos - media.fatura;
  const salarioPendente = diaSalario !== null && Math.min(diaSalario, diasMes) > hoje.getDate();
  const fimDoMes =
    diaSalario === null
      ? saldo + liquido * fracao
      : saldo + (salarioPendente ? media.entradas - media.fatura : 0) - media.gastos * fracao;
  return {
    fimDoMes: r2(fimDoMes),
    dezembro: r2(fimDoMes + liquido * inteiros),
    mesesAteDezembro: r2(fracao + inteiros),
    salarioPendente,
  };
}

/** Cofrinho sem novos aportes (meta: não mexer): só rende pela taxa mensal. Valor BRUTO (antes do IR). Tempo em meses (pode ser fracionado). */
export function projetarCofrinho(saldo: number, taxa: number, meses: number): number {
  return r2(saldo * Math.pow(1 + taxa, Math.max(0, meses)));
}
