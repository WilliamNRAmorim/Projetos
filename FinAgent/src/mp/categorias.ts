// Tabela editável de palavras-chave do extrato. Tudo em minúsculas e sem acento.
// Palavras com 5+ letras casam como trecho; as curtas só como palavra inteira.

export const CAT = {
  ENTRADA: 'Entrada',
  OUTRA_CONTA: 'Entrada da sua outra conta',
  RENDIMENTO: 'Rendimento',
  INTERNO: 'Movimento interno',
  SAIDA_OUTRA_CONTA: 'Saída para sua outra conta',
  ESTORNO: 'Estorno/cancelado',
  FATURA: 'Fatura do cartão',
  COMIDA: 'Comida/delivery',
  TRANSPORTE: 'Transporte',
  TELEFONIA: 'Telefonia',
  ASSINATURAS: 'Assinaturas',
  EMPRESTIMO: 'Empréstimo',
  PIX_PESSOAS: 'Pix para pessoas',
  OUTROS: 'Outros comércio',
} as const;

/** Movimento entre contas/reservas do próprio usuário: fora dos gastos e da média. */
export const ehMovimentoInterno = (categoria: string) => categoria === CAT.INTERNO || categoria === CAT.SAIDA_OUTRA_CONTA;

/** Categorias de gasto por palavra-chave na contraparte (ordem importa). */
export const PALAVRAS_GASTO: [string, string[]][] = [
  [CAT.COMIDA, ['ifood', '99 food', '99food', 'lanchonete', 'lanche', 'pizza', 'pizzaria', 'restaurante', 'acai', 'hamburgueria', 'padaria', 'ifd']],
  [CAT.TRANSPORTE, ['uber', 'uberrides', '99pop', '99 pop', '99 tecnologia', '99tecnologia']],
  [CAT.TELEFONIA, ['tim', 'vivo', 'claro']],
  [CAT.ASSINATURAS, ['google', 'mp*melimais', 'melimais']],
];

/** Prefixos do TRANSACTION_TYPE por tipo de linha (já normalizados). */
export const PREFIXOS = {
  rendimento: ['rendimentos'],
  interno: ['dinheiro reservado', 'dinheiro retirado', 'reserva por gastos', 'reserva programada'],
  estorno: ['reembolso', 'estorno cartao visa', 'pagamento com codigo qr pix - cancelado', 'pagamento com qr pix - cancelado'],
  fatura: ['pagamento de fatura cartao de credito', 'pagamento cartao de credito'],
  emprestimo: ['pagamento de parcela emprestimos'],
  entrada: [
    'pix recebido', 'transferencia pix recebida', 'transferencia recebida',
    'venda de criptomoedas', 'venda de bitcoin', 'liberacao de dinheiro',
  ],
  pixEnviado: ['pix enviado', 'transferencia pix enviada'],
  pagamento: ['pagamento com qr pix', 'pagamento com codigo qr', 'pagamento de conta', 'pagamento'],
};

/** Linhas do cartão de crédito importadas das faturas (scripts/faturas_para_csv.py): compras (já são o gasto de fato) e estornos. */
export const PREFIXO_COMPRA_CARTAO = 'pagamento com cartao visa ';
export const PREFIXO_ESTORNO_CARTAO = 'estorno cartao visa ';
/** Compra OU estorno do cartão importado: nenhuma das duas é movimento da conta. */
export const ehCompraCartao = (tipo: string) => {
  const n = norm(tipo);
  return n.startsWith(PREFIXO_COMPRA_CARTAO) || n.startsWith(PREFIXO_ESTORNO_CARTAO);
};
/** Mês (YYYY-MM) da fatura de uma compra de cartão importada (ref "CARTAO-<fatura>-..."); outra linha: null. */
export const faturaDaCompra = (ref: string): string | null => /^CARTAO-(\d{4}-\d{2})-/.exec(ref)?.[1] ?? null;

/** Minúsculas, sem acento, espaços normalizados. */
export function norm(t: string): string {
  return t.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/\s+/g, ' ').trim();
}

export function contemPalavra(textoNorm: string, palavra: string): boolean {
  if (palavra.length >= 5) return textoNorm.includes(palavra);
  const esc = palavra.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  return new RegExp(`(^|[^a-z0-9])${esc}([^a-z0-9]|$)`).test(textoNorm);
}

export function categoriaPorPalavra(textoNorm: string): string | null {
  for (const [cat, palavras] of PALAVRAS_GASTO) {
    if (palavras.some((p) => contemPalavra(textoNorm, p))) return cat;
  }
  return null;
}
