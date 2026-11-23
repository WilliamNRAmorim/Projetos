# Uiu: patch geral v4 (23/11/2026)

**Status: proposta. Nada foi alterado no agente, no fluxo nem no SharePoint.** O diagnóstico foi só leitura.

## 1. Por que o Uiu responde mal (o que foi medido)

| # | Achado | Evidência |
|---|---|---|
| 1 | **Cortou o dia em UTC e disse "você está em UTC".** | Pedido: 13/11 de 00h a 23h59. RegistrosInspeção: Brasília 03:00Z a 03:00Z = **7.324,30 m em 93 registros** (lido em 23/11). O Uiu deu 8.611,4 m em 105, que é exatamente 00:00Z a 24:00Z: entrou 21h a 24h do dia 12 e saiu 21h a 24h do dia 13. As instruções não têm regra para dia civil. |
| 2 | **Não reconheceu o SAP.** | 7.915,86 m é a MB51 de 13/11 (`GMS/Analises/Mascara_SAP/Validacao_2026-11-16.md`). O Uiu chamou as linhas de RegistrosInspeção, disse que "a divergência é recorte de janela" e somou refugo em cima. Nenhuma ferramenta dele lê o SAP. |
| 3 | **As instruções do refugo estão erradas.** | TiposErros desde 01/08: 3.785 de 3.829 linhas têm DataHoraRefugo só com a data (03:00Z). A v3.2 manda cortar às 08:20Z, e isso devolve o **dia seguinte**. 13/11: certo 85,87 m em 42 linhas; com 08:20Z, 116,76 m em 46. O gabarito "3.072,49 m pelo dia produtivo" (11/11) tem o mesmo erro. |
| 4 | **33 ferramentas sobrepostas.** | 32 são GetItem/GetItems do conector, com descrição genérica em inglês; em uma delas o modelo ainda escolhe a tabela. Só uma faz conta exata (Somar no GMS). |
| 5 | **Erro técnico na conversa.** | ConnectorPowerFxError às 15:18:06Z de 16/11. O fluxo Somar só rodou 15:15:46, 15:16:42 e 15:20:19, todas com sucesso: o erro não veio dele. Hipótese: um Get items do conector. |
| 6 | **Explicação sem consulta de soma.** | Entre 15:16:42 e 15:20:19 não houve execução do Somar, justo quando ele explicou a divergência. (Chamadas de Get items não aparecem nesse registro.) |
| 7 | **Instruções saturadas e contraditórias.** | 7.890 de 8.000 caracteres. Prometem criar e atualizar itens, e não existe ferramenta de escrita. O modelo precisa lembrar UTC, coluna interna e regra de cada lista. |
| 8 | **Modelo.** | A conversa de 16/11 usou a versão publicada em 11/11, registrada com Opus 4.8: só trocar o modelo não resolve. Hoje às 14:16 o rascunho foi gravado com **GPT-6 Luna Quick response**. O Opus 4.8 sai em 15/02/2027 (substituto: Opus 5.5). |

Entre 16/11 e hoje a RegistrosInspeção recebeu o ID 21786 (criado em 18/11, com data de 14/11 00:41Z), e o refugo de 13/11 passou de 44 para 42 linhas. Por isso números de 16/11 e de hoje podem diferir um pouco.

## 2. A mudança de patamar

Hoje o modelo escreve o filtro, converte fuso, lembra a regra e faz a leitura. Passa a ser: **o modelo entende a pergunta e explica; a ferramenta aplica a regra e entrega o número.**

### A. Ferramenta "Consultar GMS" (fluxo de agente novo)
- Entradas em linguagem de negócio: `indicador`, `de`, `ate` (DD/MM/AAAA), `corte` (civil ou produtivo), `agrupar`, `onde` (máquina, mangueira, turno, OP).
- O fluxo monta o filtro, converte Brasília para UTC, escolhe a coluna e aplica a regra.
- Saída: número, linhas lidas, período escrito em Brasília, fonte, completo/parcial e avisos.
- Indicadores: produção por etapa, inspeção boa, refugo, % refugo, Hora-Hora real/meta/Tempo Parado, Montagem, paradas da Montagem, refugo da Bobinadeira e da Extrusora, Catenária, OPs em processo, carretéis.
- Regras de turno, parada e contagem passam pelo `revisor` antes de entrar.

### B. Ferramenta "Perguntar ao BI" (DAX no modelo `(GMS)` do Power BI)
- Traz SAP (MB51, COOIS), meta, plano, PPM e OEE2 com as medidas já validadas.
- **Portão:** a política de DLP pode bloquear o conector Power BI (o Studio mostra a ação, mas não diz se está liberada). Teste: o William cria a conexão e roda uma consulta.
- Se estiver bloqueado: lista `GMS_SAP_Dia` (dia × material × OP, metros) lida pela ferramenta A.

### C. Limpeza das ferramentas: de 33 para 4
Consultar GMS, Perguntar ao BI, Ler linhas (detalhe, até 50 linhas, por fluxo GET com colunas escolhidas) e Ler conhecimento. As outras ficam **desligadas**, não apagadas; o Somar no GMS fica ligado até a A passar nos testes.

### D. Instruções v4 (cerca de 4.500 caracteres)
- "Tem certeza?" = consultar de novo e mostrar a conta; nunca defender nem ceder sem consulta.
- Dado colado = identificar a fonte pelas colunas antes de somar (descrição "HOSE-AER…" e data de lançamento = SAP).
- Dois números diferentes = reconciliar fonte, data e recorte; dizer qual é qual.
- "Dia 13" = dia civil de Brasília se ele disser 00h a 23h59; senão dia produtivo, dito em meia linha.
- Sem promessa de escrita enquanto não existir ferramenta.

### E. Modelo
Rodar a mesma bateria no Opus 5.5 (ou no Opus 4.8, se o 5.5 não aparecer no ambiente) e no GPT-6 Luna Quick, que está no rascunho. Fica o que acertar mais; empate, o mais barato. O William decide.

### F. Bateria de aceite
- 40 perguntas com gabarito calculado pela API, incluindo esta conversa inteira e as réplicas ("tem certeza?", dado colado, período ambíguo).
- Aceite: pelo menos 38 de 40 números exatos, **zero** número ou explicação inventados e zero erro técnico. Só publica se passar.

### G. Acabamento
Erro e Fallback em português, com nova tentativa; corrigir o gabarito e a receita de refugo.

## 3. Ordem e "sim"

| # | Etapa | Pede "sim" |
|---|---|---|
| 1 | Gabarito das 40 perguntas e especificação dos indicadores; regras ao `revisor` | aprovar este plano |
| 2 | Teste do portão do Power BI | sim (conexão: clique do William) |
| 3 | Criar os fluxos Consultar GMS e Ler linhas | sim |
| 4 | Rascunho: ligar as novas, desligar as antigas, instruções v4 | sim |
| 5 | Bateria nos dois modelos; correção até passar | não |
| 6 | Publicar no Teams | sim |

Volta atrás: guardar antes as instruções, as definições das 33 ferramentas e o fluxo; religar é desfazer o passo 4.

Pendências de ambiente: o agente `revisor` não está carregado nesta sessão; ler transcrições exige um privilégio do Dataverse que a conta não tem (a bateria substitui).
