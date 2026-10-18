// Tokens visuais do FinAgent (tema escuro). Use estes valores em vez de cores soltas.
export const cores = {
  fundo: '#0e1116',
  superficie: '#171b22',
  superficie2: '#1e242d',
  borda: '#2a3039',
  texto: '#e8eaed',
  texto2: '#9aa0a6',
  primaria: '#4fc3a1',
  sucesso: '#4fc3a1',
  alerta: '#e0b04a',
  perigo: '#ef7b7b',
  info: '#6aa9ff',
} as const;

/** 6 cores para categorias, legíveis no fundo escuro. */
export const paleta = ['#4fc3a1', '#6aa9ff', '#e0b04a', '#c58af9', '#ef7b7b', '#5fd0e8'] as const;

export const espaco = { xs: 4, sm: 8, md: 12, lg: 16, xl: 24 } as const;
export const raio = { sm: 8, md: 12, lg: 16, pill: 999 } as const;
export const fonte = { pequena: 12, corpo: 14, titulo: 18, numero: 24, heroi: 40 } as const;

export type Variante = 'info' | 'alerta' | 'sucesso' | 'perigo';
export const corDaVariante: Record<Variante, string> = {
  info: cores.info, alerta: cores.alerta, sucesso: cores.sucesso, perigo: cores.perigo,
};
