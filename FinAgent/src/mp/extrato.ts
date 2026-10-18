// Funções puras para o extrato CSV do Mercado Pago (sem React Native).
import { CAT, PREFIXOS, categoriaPorPalavra, ehCompraCartao, ehMovimentoInterno, faturaDaCompra, norm } from './categorias.ts';

export type Transacao = {
  data: string; // YYYY-MM-DD
  tipo: string; // TRANSACTION_TYPE original (inclui a contraparte)
  ref: string;
  valor: number;
  saldo: number; // PARTIAL_BALANCE
  seq: number; // ordem cronológica dentro do arquivo
};

export type Lancamento = Transacao & {
  categoria: string;
  contraparte: string;
  excluida: boolean; // estorno ou par anulado: fora dos totais
  reserva: boolean; // movimento da reserva Emergências
};

const r2 = (n: number) => Math.round(n * 100) / 100;
const cent = (n: number) => Math.round(n * 100);

/** "1.900,00" / "-74,99" / "0,00" -> número. Inválido -> null. */
export function parseValorBR(texto: string): number | null {
  const t = texto.trim().replace(/[R$\s]/g, '');
  if (!/^-?\d{1,3}(\.\d{3})*(,\d+)?$|^-?\d+(,\d+)?$/.test(t)) return null;
  const n = Number(t.replace(/\./g, '').replace(',', '.'));
  return Number.isFinite(n) ? n : null;
}

/** "05-10-2026" -> "2026-10-05". */
export function parseData(texto: string): string | null {
  const m = /^(\d{2})-(\d{2})-(\d{4})$/.exec(texto.trim());
  if (!m) return null;
  const [, d, mes, a] = m;
  if (Number(mes) < 1 || Number(mes) > 12 || Number(d) < 1 || Number(d) > 31) return null;
  return `${a}-${mes}-${d}`;
}

/** Lê o CSV de extrato. Ignora cabeçalho de resumo e linhas inválidas. */
export function parseExtratoCsv(texto: string): Transacao[] {
  const linhas = texto.replace(/^﻿/, '').split(/\r?\n/);
  const ini = linhas.findIndex((l) => l.toUpperCase().startsWith('RELEASE_DATE'));
  if (ini < 0) return [];
  const lista: Transacao[] = [];
  for (const linha of linhas.slice(ini + 1)) {
    if (!linha.trim()) continue;
    const c = linha.split(';');
    const data = parseData(c[0] ?? '');
    const valor = parseValorBR(c[3] ?? '');
    const saldo = parseValorBR(c[4] ?? '');
    if (!data || valor === null || saldo === null) continue;
    lista.push({ data, tipo: (c[1] ?? '').trim(), ref: (c[2] ?? '').trim(), valor, saldo, seq: 0 });
  }
  // Descobre se o arquivo vem em ordem crescente ou decrescente pela coerência dos saldos.
  let asc = 0;
  let desc = 0;
  for (let i = 1; i < lista.length; i++) {
    if (cent(lista[i - 1].saldo + lista[i].valor) === cent(lista[i].saldo)) asc++;
    if (cent(lista[i].saldo + lista[i - 1].valor) === cent(lista[i - 1].saldo)) desc++;
  }
  const ordenada = desc > asc ? [...lista].reverse() : lista;
  return ordenada.map((t, i) => ({ ...t, seq: i }));
}

export const chaveTransacao = (t: Transacao) => `${t.ref}|${t.tipo}|${cent(t.valor)}|${t.data}`;

/** Junta extratos sem duplicar (ref+tipo+valor+data) e ordena cronologicamente. */
export function mesclar(existentes: Transacao[], novas: Transacao[]): Transacao[] {
  const mapa = new Map<string, Transacao>();
  for (const t of [...existentes, ...novas]) {
    const k = chaveTransacao(t);
    if (!mapa.has(k)) mapa.set(k, t);
  }
  return [...mapa.values()].sort((a, b) => a.data.localeCompare(b.data) || a.seq - b.seq);
}

/** Saldo da conta = saldo parcial da última linha cronológica. */
export function saldoFinal(trans: Transacao[]): { saldo: number; data: string } | null {
  if (trans.length === 0) return null;
  const conta = trans.filter((t) => !ehCompraCartao(t.tipo)); // compra de cartão não mexe no saldo da conta
  if (conta.length === 0) return null;
  const u = [...conta].sort((a, b) => a.data.localeCompare(b.data) || a.seq - b.seq)[conta.length - 1];
  return { saldo: u.saldo, data: u.data };
}

export const mesDe = (data: string) => data.slice(0, 7);

/** Meses com movimento na conta. Compras de cartão importadas não contam (um mês só de cartão não é mês do extrato). */
export function mesesDisponiveis(trans: Transacao[]): string[] {
  return [...new Set(trans.filter((t) => !ehCompraCartao(t.tipo)).map((t) => mesDe(t.data)))].sort().reverse();
}

export function mesAnteriorDe(mes: string): string {
  const [a, m] = mes.split('-').map(Number);
  return m === 1 ? `${a - 1}-12` : `${a}-${String(m - 1).padStart(2, '0')}`;
}

const comecaCom = (n: string, prefixos: string[]) => prefixos.find((p) => n.startsWith(p));

function mesmaPessoa(contraNorm: string, meuNome: string): boolean {
  const meu = norm(meuNome).split(' ').filter((x) => x.length > 2);
  if (meu.length < 2) return false;
  const tokens = new Set(contraNorm.split(' '));
  return meu.every((p) => tokens.has(p));
}

function classificarUma(t: Transacao, meuNome: string): Pick<Lancamento, 'categoria' | 'contraparte' | 'excluida' | 'reserva'> {
  const n = norm(t.tipo);
  const base = { contraparte: '', excluida: false, reserva: false };
  const resto = (p: string) => n.slice(p.length).trim();

  let p = comecaCom(n, PREFIXOS.rendimento);
  if (p) return { ...base, categoria: CAT.RENDIMENTO };

  p = comecaCom(n, PREFIXOS.estorno);
  if (p) return { ...base, categoria: CAT.ESTORNO, excluida: true, contraparte: resto(p) };

  p = comecaCom(n, PREFIXOS.interno);
  if (p) return { ...base, categoria: CAT.INTERNO, reserva: n.includes('emergencias') };

  if (comecaCom(n, PREFIXOS.fatura)) return { ...base, categoria: CAT.FATURA };
  if (comecaCom(n, PREFIXOS.emprestimo)) return { ...base, categoria: CAT.EMPRESTIMO };

  p = comecaCom(n, PREFIXOS.entrada);
  if (p) {
    const contra = resto(p);
    const propria = mesmaPessoa(contra, meuNome);
    return { ...base, contraparte: contra, categoria: propria ? CAT.OUTRA_CONTA : CAT.ENTRADA };
  }

  p = comecaCom(n, PREFIXOS.pixEnviado);
  if (p) {
    const contra = resto(p);
    if (mesmaPessoa(contra, meuNome)) return { ...base, contraparte: contra, categoria: CAT.SAIDA_OUTRA_CONTA };
    return { ...base, contraparte: contra, categoria: categoriaPorPalavra(contra) ?? CAT.PIX_PESSOAS };
  }

  p = comecaCom(n, PREFIXOS.pagamento);
  if (p) {
    const contra = resto(p).replace(/^com cartao visa /, '');
    return { ...base, contraparte: contra, categoria: categoriaPorPalavra(contra) ?? CAT.OUTROS };
  }

  // Desconhecido: positivo vira entrada, negativo vira outros.
  return { ...base, categoria: t.valor > 0 ? CAT.ENTRADA : categoriaPorPalavra(n) ?? CAT.OUTROS };
}

/** Regras do usuário (recategorização). Têm prioridade sobre as palavras-chave. */
export type RegrasUsuario = {
  porContraparte?: Record<string, string>; // contraparte normalizada -> categoria
  porTransacao?: Record<string, string>; // chaveTransacao -> categoria (vale só para aquela linha)
};

function aplicarRegras(l: Lancamento, regras?: RegrasUsuario): Lancamento {
  if (!regras || l.excluida) return l;
  const cat = regras.porTransacao?.[chaveTransacao(l)] ?? (l.contraparte ? regras.porContraparte?.[l.contraparte] : undefined);
  return cat ? { ...l, categoria: cat } : l;
}

/** Classifica as linhas e anula pares pagamento+estorno (mesma referência e valor oposto). `regras` é opcional. */
export function classificarExtrato(trans: Transacao[], meuNome = '', regras?: RegrasUsuario): Lancamento[] {
  const lancs: Lancamento[] = trans.map((t) => aplicarRegras({ ...t, ...classificarUma(t, meuNome) }, regras));
  // O pagamento do mês M quita a fatura de M-1. Se as compras dessa fatura foram importadas, contar o pagamento
  // seria contar em dobro: vira movimento interno. Fatura não importada: o pagamento segue como gasto.
  const faturasImportadas = new Set(trans.map((t) => faturaDaCompra(t.ref)).filter((f): f is string => f !== null));
  for (const l of lancs) {
    if (l.categoria === CAT.FATURA && faturasImportadas.has(mesAnteriorDe(mesDe(l.data)))) l.categoria = CAT.INTERNO;
  }
  for (const e of lancs) {
    if (e.categoria !== CAT.ESTORNO || e.valor <= 0) continue;
    const par = lancs.find(
      (x) => x !== e && !x.excluida && x.ref === e.ref && x.categoria !== CAT.ESTORNO && cent(x.valor) === -cent(e.valor),
    );
    if (par) par.excluida = true;
  }
  return lancs;
}

export type TotaisExtrato = {
  mes: string;
  entradas: number; // inclui "outra conta"
  entradasOutraConta: number;
  rendimentos: number;
  gastos: number; // sem interno, estorno, rendimento e fatura
  fatura: number;
  porCategoria: { nome: string; total: number }[];
  reservaLiquida: number; // reservado menos retirado na Emergências (positivo = foi para a reserva)
  variacaoGasto: number | null; // % contra o mês anterior
};

function gastosDoMes(lancs: Lancamento[], mes: string): number {
  let g = 0;
  for (const l of lancs) {
    if (mesDe(l.data) !== mes || l.excluida || l.valor >= 0) continue;
    if (ehMovimentoInterno(l.categoria) || l.categoria === CAT.FATURA) continue;
    g += -l.valor;
  }
  return r2(g);
}

export function totaisMes(lancs: Lancamento[], mes: string): TotaisExtrato {
  let entradas = 0;
  let outra = 0;
  let rend = 0;
  let fatura = 0;
  let reserva = 0;
  const cats = new Map<string, number>();
  for (const l of lancs) {
    if (mesDe(l.data) !== mes) continue;
    if (l.reserva) reserva += -l.valor;
    if (l.excluida) continue;
    if (l.categoria === CAT.RENDIMENTO) rend += l.valor;
    else if (l.categoria === CAT.ENTRADA || l.categoria === CAT.OUTRA_CONTA) {
      entradas += l.valor;
      if (l.categoria === CAT.OUTRA_CONTA) outra += l.valor;
    } else if (l.categoria === CAT.FATURA) fatura += -l.valor;
    else if (!ehMovimentoInterno(l.categoria) && l.valor < 0) cats.set(l.categoria, (cats.get(l.categoria) ?? 0) + -l.valor);
  }
  const gastos = gastosDoMes(lancs, mes);
  const ant = gastosDoMes(lancs, mesAnteriorDe(mes));
  return {
    mes,
    entradas: r2(entradas),
    entradasOutraConta: r2(outra),
    rendimentos: r2(rend),
    gastos,
    fatura: r2(fatura),
    porCategoria: [...cats.entries()].map(([nome, total]) => ({ nome, total: r2(total) })).sort((a, b) => b.total - a.total),
    reservaLiquida: r2(reserva),
    variacaoGasto: ant > 0 ? r2(((gastos - ant) / ant) * 100) : null,
  };
}
