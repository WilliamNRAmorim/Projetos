// Funções puras (sem React Native) para analisar pagamentos do Mercado Pago.

export type Pagamento = {
  id: number;
  date_created: string;
  transaction_amount: number;
  payment_type_id?: string;
  status?: string;
  description?: string | null;
  collector_id?: number;
};

export type Movimento = {
  id: number;
  data: string; // ISO original
  dia: string; // YYYY-MM-DD (local)
  mes: string; // YYYY-MM (local)
  valor: number;
  tipo: string;
  descricao: string;
  categoria: string;
  direcao: 'gasto' | 'recebimento';
  interna: boolean;
};

const CATEGORIAS: [string, string[]][] = [
  ['Telefonia', ['vivo', 'claro', 'telefon', 'recarga']],
  ['Banco', ['santander', 'itau', 'itaú', 'bradesco', 'nubank', 'banco', 'caixa']],
  ['Transporte', ['uber', 'combust', 'posto', 'estacion', 'pedagio', 'pedágio']],
  ['Alimentação', ['ifood', 'restaurante', 'lanche', 'mercado', 'padaria', 'supermerc']],
  ['Assinaturas', ['netflix', 'spotify', 'youtube', 'prime', 'assinatura', 'google']],
  ['Moradia', ['aluguel', 'energia', 'agua', 'água', 'condom', 'internet']],
  ['Saúde', ['farmacia', 'farmácia', 'drogaria', 'consulta', 'plano de saude']],
];

export const SEM_DESCRICAO = 'Sem descrição';
export const OUTROS = 'Outros';

export function categorizar(descricao?: string | null): string {
  const d = (descricao ?? '').trim().toLowerCase();
  if (!d) return SEM_DESCRICAO;
  for (const [cat, palavras] of CATEGORIAS) {
    if (palavras.some((p) => d.includes(p))) return cat;
  }
  return OUTROS;
}

const p2 = (n: number) => String(n).padStart(2, '0');

export function chaveDia(iso: string): string {
  const d = new Date(iso);
  return `${d.getFullYear()}-${p2(d.getMonth() + 1)}-${p2(d.getDate())}`;
}

export function chaveMes(iso: string): string {
  return chaveDia(iso).slice(0, 7);
}

export function mesAnterior(mes: string): string {
  const [a, m] = mes.split('-').map(Number);
  return m === 1 ? `${a - 1}-12` : `${a}-${p2(m - 1)}`;
}

const cent = (v: number) => Math.round(v * 100);
const r2 = (n: number) => Math.round(n * 100) / 100;

/** Classifica pagamentos aprovados em gastos/recebimentos e marca movimentação interna. */
export function classificar(pagamentos: Pagamento[], userId: number): Movimento[] {
  const movs: Movimento[] = pagamentos
    .filter((p) => p.status === 'approved')
    .map((p) => ({
      id: p.id,
      data: p.date_created,
      dia: chaveDia(p.date_created),
      mes: chaveMes(p.date_created),
      valor: p.transaction_amount,
      tipo: p.payment_type_id ?? 'desconhecido',
      descricao: (p.description ?? '').trim(),
      categoria: categorizar(p.description),
      direcao: p.collector_id === userId ? ('recebimento' as const) : ('gasto' as const),
      interna: false,
    }));

  // Pareia gasto e recebimento com mesmo valor e mesmo dia (1 para 1).
  const recebimentos = new Map<string, Movimento[]>();
  for (const m of movs) {
    if (m.direcao !== 'recebimento') continue;
    const k = `${m.dia}|${cent(m.valor)}`;
    recebimentos.set(k, [...(recebimentos.get(k) ?? []), m]);
  }
  for (const g of movs) {
    if (g.direcao !== 'gasto') continue;
    const r = recebimentos.get(`${g.dia}|${cent(g.valor)}`)?.find((x) => !x.interna);
    if (r) {
      r.interna = true;
      g.interna = true;
    }
  }
  return movs;
}

export type TotaisMes = { mes: string; recebido: number; gasto: number; sobra: number; interno: number };

export function totaisDoMes(movs: Movimento[], mes: string): TotaisMes {
  let recebido = 0;
  let gasto = 0;
  let interno = 0;
  for (const m of movs) {
    if (m.mes !== mes) continue;
    if (m.interna) {
      if (m.direcao === 'gasto') interno += m.valor;
      continue;
    }
    if (m.direcao === 'recebimento') recebido += m.valor;
    else gasto += m.valor;
  }
  return { mes, recebido: r2(recebido), gasto: r2(gasto), sobra: r2(recebido - gasto), interno: r2(interno) };
}

function agrupar(movs: Movimento[], mes: string, chave: (m: Movimento) => string) {
  const acc = new Map<string, number>();
  for (const m of movs) {
    if (m.mes !== mes || m.interna || m.direcao !== 'gasto') continue;
    acc.set(chave(m), (acc.get(chave(m)) ?? 0) + m.valor);
  }
  return [...acc.entries()].map(([nome, total]) => ({ nome, total: r2(total) })).sort((a, b) => b.total - a.total);
}

export const gastoPorCategoria = (movs: Movimento[], mes: string) => agrupar(movs, mes, (m) => m.categoria);
export const gastoPorTipo = (movs: Movimento[], mes: string) => agrupar(movs, mes, (m) => m.tipo);

export function maioresGastos(movs: Movimento[], mes: string, n = 10): Movimento[] {
  return movs
    .filter((m) => m.mes === mes && !m.interna && m.direcao === 'gasto')
    .sort((a, b) => b.valor - a.valor)
    .slice(0, n);
}

export const brl = (v: number) => `R$ ${v.toFixed(2).replace('.', ',').replace(/\B(?=(\d{3})+(?!\d))/g, '.')}`;
