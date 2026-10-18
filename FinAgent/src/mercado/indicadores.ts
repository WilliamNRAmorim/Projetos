// Funções puras. "Dias" = pontos diários da série (pregões/dias com dado).
import type { Indicadores, Ponto, Tendencia } from './tipos.ts';

const fechamentos = (s: Ponto[]) => s.map((p) => p.fechamento);

export function variacao(serie: Ponto[], dias: number): number | null {
  const n = serie.length;
  if (dias < 1 || n < dias + 1) return null;
  const base = serie[n - 1 - dias].fechamento;
  if (!base) return null;
  return (serie[n - 1].fechamento / base - 1) * 100;
}

export function mediaMovel(serie: Ponto[], janela: number): number | null {
  if (janela < 1 || serie.length < janela) return null;
  const fim = fechamentos(serie).slice(-janela);
  return fim.reduce((a, b) => a + b, 0) / janela;
}

/** RSI de Wilder. Precisa de pelo menos periodo+1 pontos. */
export function rsi(serie: Ponto[], periodo = 14): number | null {
  const c = fechamentos(serie);
  if (c.length < periodo + 1) return null;
  let ganho = 0;
  let perda = 0;
  for (let i = 1; i <= periodo; i++) {
    const d = c[i] - c[i - 1];
    if (d >= 0) ganho += d;
    else perda -= d;
  }
  ganho /= periodo;
  perda /= periodo;
  for (let i = periodo + 1; i < c.length; i++) {
    const d = c[i] - c[i - 1];
    ganho = (ganho * (periodo - 1) + (d > 0 ? d : 0)) / periodo;
    perda = (perda * (periodo - 1) + (d < 0 ? -d : 0)) / periodo;
  }
  if (perda === 0) return ganho === 0 ? 50 : 100;
  return 100 - 100 / (1 + ganho / perda);
}

/** Desvio-padrão (amostral) dos retornos diários, em %. */
export function volatilidade(serie: Ponto[]): number | null {
  const c = fechamentos(serie);
  if (c.length < 3) return null;
  const r: number[] = [];
  for (let i = 1; i < c.length; i++) if (c[i - 1]) r.push((c[i] / c[i - 1] - 1) * 100);
  if (r.length < 2) return null;
  const m = r.reduce((a, b) => a + b, 0) / r.length;
  const v = r.reduce((a, b) => a + (b - m) ** 2, 0) / (r.length - 1);
  return Math.sqrt(v);
}

export function posicaoNoIntervalo(preco: number, minima: number, maxima: number): number | null {
  if (maxima <= minima) return null;
  return Math.min(100, Math.max(0, ((preco - minima) / (maxima - minima)) * 100));
}

export function rotuloTendencia(preco: number, mm20: number | null, mm50: number | null): Tendencia {
  if (mm20 == null || mm50 == null) return 'indefinida';
  if (preco > mm20 && mm20 > mm50) return 'alta';
  if (preco < mm20 && mm20 < mm50) return 'baixa';
  return 'lateral';
}

export function calcularIndicadores(serie: Ponto[], precoAtual?: number): Indicadores | null {
  if (serie.length === 0 && precoAtual == null) return null;
  const s = serie.slice(-91);
  const preco = precoAtual ?? s[s.length - 1].fechamento;
  const base: Ponto[] = precoAtual != null && s.length && s[s.length - 1].fechamento !== precoAtual
    ? [...s.slice(0, -1), { data: s[s.length - 1].data, fechamento: precoAtual }]
    : s;
  const janela90 = base.slice(-90);
  const valores = fechamentos(janela90);
  const maxima = valores.length ? Math.max(...valores) : null;
  const minima = valores.length ? Math.min(...valores) : null;
  const mm20 = mediaMovel(base, 20);
  const mm50 = mediaMovel(base, 50);
  return {
    preco,
    var1d: variacao(base, 1),
    var7d: variacao(base, 7),
    var30d: variacao(base, 30),
    var90d: janela90.length >= 60 ? variacao(janela90, janela90.length - 1) : null,
    mm20,
    mm50,
    mediaSerie: valores.length >= 10 ? valores.reduce((a, b) => a + b, 0) / valores.length : null,
    rsi14: rsi(base, 14),
    volatilidade: volatilidade(janela90),
    maxima90: maxima,
    minima90: minima,
    distMaxima: maxima ? (preco / maxima - 1) * 100 : null,
    distMinima: minima ? (preco / minima - 1) * 100 : null,
    posicao: maxima != null && minima != null ? posicaoNoIntervalo(preco, minima, maxima) : null,
    tendencia: rotuloTendencia(preco, mm20, mm50),
    pontos: base.length,
  };
}
