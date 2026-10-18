export type Message = { role: 'user' | 'assistant'; content: string };

/**
 * Contexto de uma chamada.
 * - system: instrução de sistema (persona), vai no campo próprio do provedor.
 * - data: bloco de DADOS (ex.: JSON de agregados). Nunca é tratado como instrução.
 * - temperature / maxOutputTokens / thinkingBudget: parâmetros de geração (opcionais).
 */
export type AiContext = {
  system?: string;
  data?: string;
  temperature?: number;
  maxOutputTokens?: number;
  thinkingBudget?: number;
};

export interface AiProvider {
  ask(messages: Message[], context: AiContext): Promise<string>;
}
