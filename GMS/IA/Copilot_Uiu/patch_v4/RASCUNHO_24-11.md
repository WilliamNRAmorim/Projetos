# Passo 4: rascunho do Uiu (24/11/2026)

**Não publicado.** O Teams segue na versão de 11/11.

## O que mudou no rascunho
- **Ligadas (5):** Consultar GMS, Perguntar ao BI, Ler linhas, Ler conhecimento do GMS, Somar no GMS (fica até a bateria passar).
- **Desligadas (31):** todas as outras do conector SharePoint, inclusive a Get items genérica. Nada apagado.
- **Instruções:** `instrucoes/instrucoes_uiu_v4.md` (5.774 caracteres, lidas de volta e idênticas).
- **Não mexido:** modelo (GPT-6 Luna Quick response, escolha do William), Code interpreter, tópicos, conhecimento.
- **Consultar GMS:** % refugo sem inspeção no recorte agora vem vazio com aviso.

| Ferramenta nova | Componente |
|---|---|
| Consultar GMS | `a6ddf20c-fee7-f111-84e7-7ced8dc3b05d` |
| Perguntar ao BI | `1193ed12-fee7-f111-84e7-7ced8dc3b05d` |
| Ler linhas | `3c93ed12-fee7-f111-84e7-7ced8dc3b05d` |

## Voltar atrás
Cópia completa em `backup_antes_v4_2026-11-24/` (`pac copilot clone`). Religar = `statecode 0, statuscode 1` nos 31 componentes (ou Enabled na aba Tools) e colar `agent.mcs.yml` de volta.

## Teste de fumaça (painel do Studio, Luna Quick)
| Pergunta | Resposta | Tempo da ferramenta |
|---|---|---|
| quanto foi inspecionado dia 13/11/2026, só de 00h às 23h59? | 7.324,3 m, 93 linhas, civil de Brasília: certo | 71 s (primeira chamada) |
| tem certeza? e o volume por processo desse dia? | chamou de novo, manteve 7.324,3 m; 8 processos iguais ao gabarito, sem somar, avisou o corte e o cancelamento | 39 s e 31 s |

## Lições
- Entrada obrigatória de ferramenta não aceita `shouldPromptUser: false` (erro MustPromptUserWhenRequired).
- Desligar ferramenta pela API = componente inativo (`statecode 1, statuscode 2`); o Studio mostra Off.

## Falta
1. Passo 5: as 40 perguntas, 3 meses de período e leitura incompleta; comparar Luna Quick com Opus.
2. Tempo: a primeira chamada chegou perto do limite de 100 s.
3. `OnError` e Fallback em português, e os documentos de conhecimento atrasados (21h45): não estavam neste passo.
