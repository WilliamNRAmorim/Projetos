// Diagnóstico da API do Mercado Pago: só GET, e só estrutura (nomes de campos e contagens), nunca valores.

/** Reduz um JSON à lista ordenada de nomes de campos (caminhos com ponto; arrays viram "[]"). */
export function nomesDeCampos(json: unknown, prefixo = '', profundidade = 3): string[] {
  const out = new Set<string>();
  const visitar = (v: unknown, caminho: string, nivel: number) => {
    if (Array.isArray(v)) {
      if (v.length > 0 && nivel > 0) visitar(v[0], `${caminho}[]`, nivel - 1);
      return;
    }
    if (v && typeof v === 'object') {
      for (const [k, x] of Object.entries(v as Record<string, unknown>)) {
        const c = caminho ? `${caminho}.${k}` : k;
        out.add(c);
        if (nivel > 0) visitar(x, c, nivel - 1);
      }
    }
  };
  visitar(json, prefixo, profundidade);
  return [...out].sort();
}

/** Conta ocorrências de um campo (string) nos itens; ausente vira "(sem)". */
export function contarPor(itens: unknown[], campo: string): Record<string, number> {
  const r: Record<string, number> = {};
  for (const it of itens) {
    const v = (it as Record<string, unknown> | null)?.[campo];
    const k = typeof v === 'string' && v ? v : '(sem)';
    r[k] = (r[k] ?? 0) + 1;
  }
  return r;
}

export type Sonda = { nome: string; resultado: string; linhas: string[] };

type Resp = { status: number; json: unknown; taxa: string[] };

async function pegar(token: string, caminho: string): Promise<Resp> {
  const r = await fetch(`https://api.mercadopago.com${caminho}`, { headers: { Authorization: `Bearer ${token}` } });
  const taxa: string[] = [];
  r.headers.forEach((valor, nome) => {
    const n = nome.toLowerCase();
    if (n.startsWith('x-ratelimit') || n === 'retry-after') taxa.push(`${n}: ${valor}`);
  });
  let json: unknown = null;
  try {
    json = await r.json();
  } catch {
    json = null;
  }
  return { status: r.status, json, taxa };
}

const ok = (s: number) => s >= 200 && s < 300;
const rotulo = (s: number) => (ok(s) ? 'ok' : `erro HTTP ${s}`);

async function sonda(nome: string, fn: () => Promise<{ resultado: string; linhas: string[] }>): Promise<Sonda> {
  try {
    return { nome, ...(await fn()) };
  } catch {
    return { nome, resultado: 'sem conexão', linhas: [] };
  }
}

/** Roda as sondagens (cada uma independente). Nada é logado; o token não sai deste módulo. */
export async function rodarDiagnostico(): Promise<Sonda[]> {
  const { getSecret } = await import('@/src/secrets');
  const token = await getSecret('mercadopago');
  if (!token) return [{ nome: 'Token', resultado: 'não configurado', linhas: [] }];

  const taxas = new Set<string>();
  const guardaTaxa = (t: string[]) => t.forEach((x) => taxas.add(x));
  let userId: unknown;

  const sondas: Sonda[] = [];
  sondas.push(
    await sonda('GET /users/me', async () => {
      const r = await pegar(token, '/users/me');
      guardaTaxa(r.taxa);
      userId = (r.json as Record<string, unknown> | null)?.id;
      return { resultado: rotulo(r.status), linhas: ok(r.status) ? nomesDeCampos(r.json) : [] };
    }),
  );
  sondas.push(
    await sonda('Saldo /users/me/mercadopago_account/balance', async () => {
      const r = await pegar(token, '/users/me/mercadopago_account/balance');
      guardaTaxa(r.taxa);
      return { resultado: rotulo(r.status), linhas: ok(r.status) ? nomesDeCampos(r.json) : [] };
    }),
  );
  sondas.push(
    await sonda('Pagamentos com filtro de data (30 dias)', async () => {
      const fim = new Date();
      const ini = new Date(fim.getTime() - 30 * 86400000);
      const q = `range=date_created&begin_date=${encodeURIComponent(ini.toISOString())}&end_date=${encodeURIComponent(fim.toISOString())}&limit=5&sort=date_created&criteria=desc`;
      const [com, sem] = await Promise.all([
        pegar(token, `/v1/payments/search?${q}`),
        pegar(token, '/v1/payments/search?limit=5&sort=date_created&criteria=desc'),
      ]);
      guardaTaxa(com.taxa);
      guardaTaxa(sem.taxa);
      const tot = (r: Resp) => (r.json as { paging?: { total?: number } } | null)?.paging?.total;
      const tc = tot(com);
      const ts = tot(sem);
      const aceito =
        typeof tc === 'number' && typeof ts === 'number' ? (tc < ts ? 'sim (total menor)' : 'indefinido (totais iguais)') : 'indefinido';
      const linhas = [`total com filtro: ${tc ?? '?'} | sem filtro: ${ts ?? '?'}`, `filtro de data aceito: ${aceito}`];
      const itens = (com.json as { results?: unknown[] } | null)?.results ?? [];
      if (itens.length) linhas.push('campos de um item:', ...nomesDeCampos(itens[0]));
      return { resultado: rotulo(com.status), linhas };
    }),
  );
  sondas.push(
    await sonda('Últimos 100 pagamentos (contagens)', async () => {
      const r = await pegar(token, '/v1/payments/search?limit=100&sort=date_created&criteria=desc');
      guardaTaxa(r.taxa);
      if (!ok(r.status)) return { resultado: rotulo(r.status), linhas: [] };
      const itens = (r.json as { results?: Record<string, unknown>[] } | null)?.results ?? [];
      const fmt = (o: Record<string, number>) =>
        Object.entries(o)
          .map(([k, n]) => `${k}: ${n}`)
          .join(', ') || '(vazio)';
      const parcelados = itens.filter((p) => typeof p.installments === 'number' && p.installments > 1).length;
      const recebidos = itens.filter((p) => userId != null && p.collector_id === userId).length;
      return {
        resultado: rotulo(r.status),
        linhas: [
          `itens: ${itens.length}`,
          `payment_type_id -> ${fmt(contarPor(itens, 'payment_type_id'))}`,
          `operation_type -> ${fmt(contarPor(itens, 'operation_type'))}`,
          `installments > 1: ${parcelados}`,
          `recebidos (usuário é collector): ${recebidos}`,
        ],
      };
    }),
  );
  sondas.push({ nome: 'Cabeçalhos de taxa', resultado: taxas.size ? 'ok' : 'nenhum encontrado', linhas: [...taxas].sort() });
  return sondas;
}
