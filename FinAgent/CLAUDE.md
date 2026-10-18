# CLAUDE.md: FinAgent

App mobile de finanças pessoais com agente de IA.

## Stack
Expo (SDK 57, o Expo Go da Play Store ainda não suporta o 58) + TypeScript + expo-router (abas: Início, Gastos, Metas, Mercado, Economista; UI base em `src/ui/` (ver README); Configurações em `app/configuracoes.tsx`). IA em `src/ai/` (interface `ask(messages, context)`, implementação Gemini `gemini-2.5-flash`, trocável por Claude). Chaves em `src/secrets.ts`. Verificação: `npx tsc --noEmit` e `npx expo-doctor`.

## Regras
- Chaves (Mercado Pago, Gemini, brapi) ficam SÓ no expo-secure-store. Nunca no repositório, em código, log ou chat. Não ler `Chave*.txt` da raiz.
- O app é educativo e não é consultoria de investimentos registrada; o aviso deve aparecer na interface.
- Persona do economista só na etapa 5.
