# Passo 5: bateria das 40 perguntas (24/11/2026)

Modelo do rascunho: GPT-6 Luna Quick response. Painel de teste do Studio. Gabarito refeito no dia, sem mudança.
**Resultado: 31 de 40 firmes. Reprovado** (aceite: 38, zero invenção, zero erro técnico). Não publicar.

## Como foi
- Rodada 1 (instruções v4): as 40 perguntas.
- Rodada 2 (v4.1): 18 das 19 previstas; perdi o resultado da última (4). Um erro meu derrubou as consultas ao BI: chaves `{ }` nas instruções viram expressão do Studio.
- Rodada 3 (v4.2, sem chaves; indicadores `op` e `canceladas` dentro da ferramenta): 14 perguntas.
- Vale o resultado mais recente de cada pergunta; as versões 4.1 e 4.2 não foram repassadas nas que já estavam certas.

## Certas (31)
1, 2, 3, 4 (número certo, formato americano), 5 a 17, 19 a 26, 28, 29, 30, 33, 34, 40.

## Não passaram (9)
| # | O que houve |
|---|---|
| 18 | rodadas 1 e 2 chamou ficha de OP; rodada 3 sem resposta |
| 27, 31 | certas na rodada 1 (7.915,86 m; 55,52%); **sem resposta** na rodada 3 |
| 32 | tabela por mangueira, sem causa inventada, mas no corte civil e só com 7 códigos iguais: parcial |
| 35, 39 | **bloqueadas pelo filtro de conteúdo** do agente (ContentFiltered), em 2 e 3 tentativas |
| 36 | "você fez" na rodada 1; etapas na 2; **sem resposta** na 3 |
| 37 | **sem resposta** nas rodadas 1 e 3 (a 2 caiu no erro das chaves) |
| 38 | recusou a soma (certo); deu 3.125 min de parada oficial, sem os blocos, não conferido com o painel |

Na rodada 2, a pergunta 15 saiu com um dígito de OP trocado (3057661 no lugar de 30576661). É erro de cópia do modelo: conta como número inventado. Na 3 saiu certa.

## Achados
1. **Agente mudo:** em 5 das 14 da rodada 3 a conversa terminou sem texto. No registro Activity da pergunta 36 a ferramenta completou (11,6 s) e não há resposta gravada. Aconteceu com a aba visível (27, 31, 36) e oculta. Ainda sem correção. Suspeitas: opção "After running: Don't respond" das ferramentas e o modelo Quick.
2. **Filtro de conteúdo em High** bloqueia pergunta comum ("Corrige o refugo da OP..."). Mudar é ajuste de proteção: decisão do William.
3. **Tempo com a aba visível:** 10 a 40 s na maioria; primeira chamada do dia 71 a 122 s.
4. **3 meses de inspeção:** o modelo dividiu por mês e somou (464.792,9 m = 146.306,6 + 151.963,6 + 166.522,7). Só outubro confere com o gabarito; agosto e setembro não foram conferidos. Pedido direto de 3 meses ao SharePoint dá erro 500 (limite de 5.000 itens).
5. `completo=false` não foi testado.

## Mudado no rascunho e nos fluxos durante a bateria
- Consultar GMS: ranking acima de 300 grupos (devolve os 100 maiores), indicadores `op` e `canceladas`, aviso das duas passadas corrigido, sem repetição automática em erro do SharePoint.
- Ler linhas: sem repetição automática em erro.
- Instruções v4.2 (7.075 caracteres), sem chaves.
- O ranking por OP e o % por máquina foram conferidos em lote; `op`, `canceladas` e a falta de repetição foram exercitados só pelo agente (a `canceladas` ainda sem resposta lida). Essas mudanças não passaram pelo `revisor`.

## Próximo
1. Achar a causa do agente mudo (completar com resposta gerada; trocar o modelo).
2. Comparar com Opus na mesma bateria: precisa do "sim" do William para trocar o modelo do rascunho.
3. Decidir o filtro de conteúdo.
4. Repassar as 40 na versão final antes de publicar, e levar ao `revisor` a mudança do agrupamento.
