// Pós-filtro da resposta: detecta ordem de compra/venda e promessa de ganho. NÃO reescreve o texto:
// só devolve um aviso e as flags para a interface mostrar/registrar.
//
// Critério: cada padrão é testado frase a frase. Se, na MESMA frase, nos ~40 caracteres antes do trecho
// houver negação/advertência ("não", "nunca", "jamais", "evite", "ninguém", "sem", "nem"), o trecho é
// considerado educativo e não dispara ("não é recomendável vender agora no desespero").
// Exceção: "não hesite/perca/espere/deixe" não são negação ("Não hesite: compre agora" dispara).
// "garantido pelo FGC" (garantia legal) não dispara.
// Residual conhecido: negação distante ou ironia pode escapar; é um filtro de segurança, não um classificador.

export const AVISO_GUARDA =
  'Atenção: esta resposta pode soar como recomendação de compra/venda ou promessa de ganho. É conteúdo educativo, ninguém consegue garantir retorno e a decisão é sua.';

type Padrao = { id: string; re: RegExp };

const PADROES: Padrao[] = [
  { id: 'ordem_compra', re: /\b(compre|comprar|compra)\s+(agora|já|hoje|tudo|sem\s+medo)\b/i },
  { id: 'ordem_venda', re: /\b(venda|vender|vende)\s+(agora|já|hoje|tudo)\b/i },
  { id: 'previsao_certa', re: /\bvai\s+(subir|disparar|explodir|valorizar|dobrar)\b/i },
  { id: 'previsao_certa', re: /\bcom\s+certeza\s+(vai|irá)\s+(subir|valorizar|disparar|render)/i },
  { id: 'previsao_certa', re: /\b(sem\s+d[úu]vida|certamente)\s+(vai|irá)\s+(subir|valorizar|disparar|render)/i },
  { id: 'ganho_garantido', re: /\b(lucro|ganho|retorno|rendimento)s?\s+(certo|certos|garantid[oa]s?|assegurad[oa]s?)\b/i },
  { id: 'ganho_garantido', re: /\bgarantid[oa]s?\b(?!\s+(pelo|pela|pelos|pelas|por)\b)/i },
  { id: 'ganho_garantido', re: /\b(vai|vão)\s+dar\s+lucro\b/i },
  { id: 'ganho_garantido', re: /\bn[ãa]o\s+tem\s+como\s+(perder|dar\s+errado)\b/i },
  { id: 'ganho_garantido', re: /\bdinheiro\s+f[áa]cil\b/i },
];

const NEGACAO = /\b(n[ãa]o|nunca|jamais|evite|evitar|ningu[ée]m|nem|sem)\b/i;
const NAO_NEGA = /\bn[ãa]o\s+(hesite|perca|espere|deixe)\b/gi;

function negado(antes: string): boolean {
  const janela = antes.slice(-40).replace(NAO_NEGA, ' ');
  return NEGACAO.test(janela);
}

export type ResultadoGuarda = { texto: string; aviso: string | null; flags: string[] };

export function aplicarGuarda(texto: string): ResultadoGuarda {
  const flags = new Set<string>();
  for (const frase of texto.split(/(?<=[.!?\n])/)) {
    for (const p of PADROES) {
      const m = p.re.exec(frase);
      if (m && !negado(frase.slice(0, m.index))) flags.add(p.id);
    }
  }
  return { texto, aviso: flags.size ? AVISO_GUARDA : null, flags: [...flags] };
}
