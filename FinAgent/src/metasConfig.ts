// Constantes editáveis das Metas (regras de bolso, não promessas).

/** Uso do limite do cartão: abaixo de LIMITE_OK_ATE é ok; até LIMITE_ATENCAO_ATE atenção; acima disso alerta (em %). */
export const LIMITE_OK_ATE = 30;
export const LIMITE_ATENCAO_ATE = 60;

/** Meses de reserva usados como meta. */
export const MESES_RESERVA = [3, 6] as const;

/** Quantos meses fechados entram na média de gasto mensal. */
export const MESES_NA_MEDIA = 3;

/** Faixa de regra de bolso para a fatura em relação à renda (%). */
export const FATURA_SAUDAVEL_PCT = '30–40';

/** Corte progressivo: % a menos que a média base, por mês de plano (1º, 2º, 3º). Depois do último, mantém. */
export const CORTE_DEGRAUS_PCT = [10, 20, 30] as const;

/** Quantos meses antes do início do plano formam a base do corte. */
export const CORTE_MESES_BASE = 3;

export const COR_FAIXA = { ok: '#4fc3a1', atencao: '#e0b04a', alerta: '#ef7b7b' } as const;
