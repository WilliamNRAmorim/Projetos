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

export const COR_FAIXA = { ok: '#4fc3a1', atencao: '#e0b04a', alerta: '#ef7b7b' } as const;
