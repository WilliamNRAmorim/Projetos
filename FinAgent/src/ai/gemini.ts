import { getSecret } from '../secrets';
import { AiError, erroPorStatus } from './erros';
import { extrairTexto, montarCorpoGemini } from './payload';
import { AiContext, AiProvider, Message } from './types';

const MODEL = 'gemini-3.8-flash';
const URL = `https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent`;

export const gemini: AiProvider = {
  async ask(messages: Message[], context: AiContext): Promise<string> {
    const apiKey = await getSecret('gemini');
    if (!apiKey) throw new AiError('sem_chave', 'Chave do Gemini não configurada.');

    let res: Response;
    try {
      res = await fetch(URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'x-goog-api-key': apiKey },
        body: JSON.stringify(montarCorpoGemini(messages, context)),
      });
    } catch {
      throw new AiError('rede', 'Sem conexão com a internet. Verifique e tente de novo.');
    }
    if (!res.ok) throw erroPorStatus(res.status);
    const { texto, bloqueado } = extrairTexto(await res.json());
    if (!texto) {
      throw bloqueado
        ? new AiError('bloqueado', 'O Gemini não quis responder a essa pergunta. Tente reformular.')
        : new AiError('vazio', 'O Gemini não devolveu resposta. Tente de novo.');
    }
    return texto;
  },
};
