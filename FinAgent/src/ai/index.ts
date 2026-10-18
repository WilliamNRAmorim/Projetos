import { gemini } from './gemini';
import { AiContext, AiProvider, Message } from './types';

// Para trocar de provedor (ex.: Claude), implemente AiProvider e aponte aqui.
const provider: AiProvider = gemini;

export function ask(messages: Message[], context: AiContext = {}): Promise<string> {
  return provider.ask(messages, context);
}

export type { AiContext, AiProvider, Message } from './types';
export { AiError, mensagemDoErro, type TipoErroIA } from './erros';
