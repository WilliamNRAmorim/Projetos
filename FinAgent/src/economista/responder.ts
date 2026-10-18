// Resposta com guarda: bloqueia e refaz UMA vez. Função pura (a chamada ao modelo entra por parâmetro).
import { aplicarGuarda, type ResultadoGuarda } from './guarda.ts';

export const LEMBRETE_REESCREVER = 'Reescreva sem indicar ativo, valor ou ordem de compra/venda, seguindo as regras 2 e 2b';

export type Msg = { role: 'user' | 'assistant'; content: string };

/**
 * Pede a resposta; se a guarda disparar, descarta (não é devolvida) e pede UMA nova com o lembrete no fim do
 * histórico. Se a segunda também disparar, devolve ela com o aviso (aviso != null).
 */
export async function responderComGuarda(
  perguntar: (msgs: Msg[]) => Promise<string>,
  msgs: Msg[],
): Promise<ResultadoGuarda & { refeita: boolean }> {
  const g1 = aplicarGuarda(await perguntar(msgs));
  if (!g1.flags.length) return { ...g1, refeita: false };
  const g2 = aplicarGuarda(await perguntar([...msgs, { role: 'user', content: LEMBRETE_REESCREVER }]));
  return { ...g2, refeita: true };
}
