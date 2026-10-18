export type Message = { role: 'user' | 'assistant'; content: string };

/** Contexto financeiro/de mercado enviado junto (texto livre; sem persona nesta etapa). */
export type AiContext = { system?: string; data?: string };

export interface AiProvider {
  ask(messages: Message[], context: AiContext): Promise<string>;
}
