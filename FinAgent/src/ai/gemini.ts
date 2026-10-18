import { getSecret } from '../secrets';
import { AiContext, AiProvider, Message } from './types';

const MODEL = 'gemini-2.5-flash';
const URL = `https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent`;

export const gemini: AiProvider = {
  async ask(messages: Message[], context: AiContext): Promise<string> {
    const apiKey = await getSecret('gemini');
    if (!apiKey) throw new Error('Chave do Gemini não configurada (Configurações).');

    const systemText = [context.system, context.data].filter(Boolean).join('\n\n');
    const body: Record<string, unknown> = {
      contents: messages.map((m) => ({
        role: m.role === 'assistant' ? 'model' : 'user',
        parts: [{ text: m.content }],
      })),
    };
    if (systemText) body.systemInstruction = { parts: [{ text: systemText }] };

    const res = await fetch(URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'x-goog-api-key': apiKey },
      body: JSON.stringify(body),
    });
    if (!res.ok) throw new Error(`Gemini respondeu ${res.status}`);
    const json = await res.json();
    const parts: { text?: string }[] = json?.candidates?.[0]?.content?.parts ?? [];
    return parts.map((p) => p.text ?? '').join('');
  },
};
