// Pós-filtro da resposta: detecta ordem de compra/venda, indicação de ativo/valor e promessa de ganho.
// NÃO reescreve o texto: devolve o aviso e as flags. A tela descarta a resposta que disparar e pede UMA nova
// (ver responder.ts); só se a segunda também disparar ela aparece, com o aviso.
//
// Critério: cada padrão é testado frase a frase. A negação só vale se estiver ADJACENTE ao trecho
// (até 3 palavras antes) e sem ':', ',', ';' ou "mas" entre a negação e o trecho
// ("não é recomendável vender agora" é educativo; "não é recomendação, mas compre agora" dispara).
// "não hesite/perca/espere/deixe/fique/pense/tenha medo" não são negação. "sem" e "nem" não negam.
// "garantido pelo/pela FGC/governo/Tesouro" (garantia legal) não dispara.
// Residual conhecido: ironia ou negação indireta pode escapar; é um filtro de segurança, não um classificador.

export const AVISO_GUARDA =
  'Atenção: esta resposta pode soar como recomendação de compra/venda ou promessa de ganho. É conteúdo educativo, ninguém consegue garantir retorno e a decisão é sua.';

type Padrao = { id: string; re: RegExp; ok?: (m: RegExpExecArray) => boolean };


const PADROES: Padrao[] = [
  { id: 'ordem_compra', re: /\b(compre|comprar)\s+(agora|já|hoje|tudo|sem\s+medo)(?!\w)/i },
  { id: 'ordem_compra', re: /(?:^|\s)(?:é|e)\s+hora\s+de\s+(comprar|vender)\b/i },
  { id: 'ordem_compra', re: /\bvale\s+a\s+pena\s+(comprar|vender)\b/i },
  { id: 'ordem_compra', re: /(?:^|\s)(?:é|e)\s+uma\s+boa\s+compra\b/i },
  { id: 'ordem_compra', re: /\brecomendo\s+(comprar|investir)\b/i },
  {
    id: 'indica_ativo',
    re: /\b(compre|invista|coloque|aloque|aplique)\b.{0,30}?\b([A-Za-z]{4}\d{1,2})\b/i,
    ok: (m) => /^[A-Z]{4}\d{1,2}$/.test(m[2]),
  },
  {
    id: 'indica_valor',
    re: /\b(invista|aplique|coloque|aloque|destine)\b.{0,25}?(R\$\s*\d[\d.,]*|\d+(?:[.,]\d+)?\s*%).{0,25}?\b(em|no|na)\b/i,
  },
  { id: 'ordem_venda', re: /\b(venda|vender|vende)\s+(agora|já|hoje|tudo)(?!\w)/i },
  { id: 'previsao_certa', re: /\bvai\s+(subir|disparar|explodir|valorizar|dobrar)\b/i },
  { id: 'previsao_certa', re: /\bdeve\s+subir\b/i },
  { id: 'previsao_certa', re: /\bvai\s+render\s+\d/i },
  { id: 'previsao_certa', re: /\bcom\s+certeza\s+(vai|irá)\s+(subir|valorizar|disparar|render)/i },
  { id: 'previsao_certa', re: /\b(sem\s+d[úu]vida|certamente)\s+(vai|irá)\s+(subir|valorizar|disparar|render)/i },
  { id: 'ganho_garantido', re: /\b(lucro|ganho|retorno|rendimento)s?\s+(certo|certos|garantid[oa]s?|assegurad[oa]s?)\b(?!\s+(?:pelo|pela|pelos|pelas|por)\b)/i },
  { id: 'ganho_garantido', re: /\bgarantid[oa]s?\b(?!\s+(?:pelo|pela|pelos|pelas|por)\b)/i },
  { id: 'ganho_garantido', re: /\b(vai|vão)\s+dar\s+lucro\b/i },
  { id: 'ganho_garantido', re: /\bn[ãa]o\s+tem\s+como\s+(perder|dar\s+errado)\b/i },
  { id: 'ganho_garantido', re: /\bdinheiro\s+f[áa]cil\b/i },
];

const NEGACAO = /\b(n[ãa]o|nunca|jamais|evite|evitar|ningu[ée]m)\b/i;
const NAO_NEGA = /\bn[ãa]o\s+(hesite|perca|espere|deixe|fique|pense|tenha\s+medo)\b/gi;
const QUEBRA = /[:,;]|\bmas\b/i;

function negado(antes: string): boolean {
  const limpo = antes.replace(NAO_NEGA, ' ');
  const janela = limpo.trim().split(/\s+/).slice(-3).join(' ');
  const m = NEGACAO.exec(janela);
  if (!m) return false;
  return !QUEBRA.test(janela.slice(m.index + m[0].length));
}

export type ResultadoGuarda = { texto: string; aviso: string | null; flags: string[] };

export function aplicarGuarda(texto: string): ResultadoGuarda {
  const flags = new Set<string>();
  for (const frase of texto.split(/(?<=[.!?\n])/)) {
    for (const p of PADROES) {
      const m = p.re.exec(frase);
      if (m && (!p.ok || p.ok(m)) && !negado(frase.slice(0, m.index))) flags.add(p.id);
    }
  }
  return { texto, aviso: flags.size ? AVISO_GUARDA : null, flags: [...flags] };
}
