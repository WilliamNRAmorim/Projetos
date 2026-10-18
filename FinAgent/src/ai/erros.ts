// Erros da IA por tipo, com mensagem amigável. Sem dependências de React Native (testável em node).
export type TipoErroIA = 'sem_chave' | 'chave_invalida' | 'limite' | 'rede' | 'servidor' | 'bloqueado' | 'vazio' | 'outro';

export class AiError extends Error {
  tipo: TipoErroIA;
  status?: number;
  constructor(tipo: TipoErroIA, mensagem: string, status?: number) {
    super(mensagem);
    this.name = 'AiError';
    this.tipo = tipo;
    this.status = status;
  }
}

/** Converte o status HTTP da API em AiError. */
export function erroPorStatus(status: number): AiError {
  if (status === 429) return new AiError('limite', 'Limite de uso do Gemini atingido. Tente de novo em alguns minutos.', status);
  if (status === 401 || status === 403) return new AiError('chave_invalida', 'O Gemini recusou a chave. Confira em Configurações.', status);
  if (status === 400) return new AiError('chave_invalida', 'O Gemini recusou o pedido (chave inválida ou pedido malformado).', status);
  if (status >= 500) return new AiError('servidor', 'O Gemini está instável agora. Tente de novo em instantes.', status);
  return new AiError('outro', `O Gemini respondeu com erro ${status}.`, status);
}

export const mensagemDoErro = (e: unknown): { tipo: TipoErroIA; texto: string } =>
  e instanceof AiError ? { tipo: e.tipo, texto: e.message } : { tipo: 'outro', texto: 'Algo deu errado. Tente de novo.' };
