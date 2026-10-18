export type Ponto = { data: string; fechamento: number }; // data = AAAA-MM-DD, ordem crescente

export type TipoAtivo = 'moeda' | 'cripto' | 'acao';

export type Ativo = {
  id: string; // ex.: moeda:USD, cripto:bitcoin, acao:PETR4
  tipo: TipoAtivo;
  codigo: string; // USD, bitcoin, PETR4
  nome: string;
};

export type Cotacao = {
  preco: number;
  variacaoDia: number | null; // %
};

export type Indicadores = {
  preco: number;
  var1d: number | null;
  var7d: number | null;
  var30d: number | null;
  var90d: number | null;
  mm20: number | null;
  mm50: number | null;
  mediaSerie: number | null; // média do período disponível (até 90 pontos)
  rsi14: number | null;
  volatilidade: number | null; // desvio-padrão dos retornos diários, em %
  maxima90: number | null;
  minima90: number | null;
  distMaxima: number | null; // % do preço atual em relação à máxima (<= 0)
  distMinima: number | null; // % do preço atual em relação à mínima (>= 0)
  posicao: number | null; // 0-100 no intervalo mínima-máxima
  tendencia: Tendencia;
  pontos: number;
};

export type Tendencia = 'alta' | 'baixa' | 'lateral' | 'indefinida';
