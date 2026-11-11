# Plano: ferramenta genérica "Somar no GMS" (11/11/2026)

**Status: proposta, nada construído.**

## Por que

Nos testes de 11/11 ([gabarito](instrucoes/gabarito_teste_2026-11-11.md)), o Uiu montou o filtro certo e aplicou a regra certa, mas errou os totais em 10% a 25%:
- O conector Get items devolve as linhas para o modelo.
- O modelo copia as linhas para o Python e perde parte delas no caminho.

Total não pode depender dessa cópia. A soma precisa acontecer fora do modelo, numa ferramenta que lê todas as linhas e devolve só o resultado.

O desenho é o de um SELECT genérico com filtro, agrupamento e soma, não uma ferramenta por pergunta. É o modelo quem escolhe a consulta.

## O que a ferramenta faz

Fluxo de agente (agent flow) no ambiente DPS - Non Prod, com o gatilho "When an agent calls the flow".

| Entrada | Exemplo | Regra |
|---|---|---|
| `lista` | `Eventos_Producao` | só listas da lista permitida (abaixo); outra lista → erro |
| `filtro` | `data_ref ge datetime'2026-11-10T00:00:00Z' and data_ref lt datetime'2026-11-11T00:00:00Z' and (tipo eq 'Fim' or tipo eq 'Parcial')` | obrigatório; vazio → erro |
| `agrupar` | `etapa` ou `etapa,turno` | 0, 1 ou 2 colunas |
| `somar` | `metros` | coluna numérica; vazio = só contar linhas |
| `top` | `10` | opcional: devolve os N maiores grupos |

**Saída:** um texto JSON curto com os campos abaixo.
- Por grupo: `grupos: [{chave, soma, linhas}]`, em ordem decrescente de soma.
- No total: `total_soma`, `total_linhas`, `paginas_lidas`, `completo: true/false`.
- Em caso de falha: `erro`.

**Passos do fluxo:**
1. Valida a lista contra a lista permitida e exige o filtro.
2. Lê as linhas com "Send an HTTP request to SharePoint", método **GET fixo**:
   - endereço: `_api/web/lists/getbytitle('{lista}')/items?$select=ID,{agrupar},{somar}&$filter={filtro}&$orderby=ID&$top=5000`;
   - cabeçalho `Accept: application/json;odata=nometadata`;
   - repete pelo `odata.nextLink` (Do until), com teto de 10 páginas (50 mil linhas). Se bater no teto, devolve `completo: false`.
3. Junta as páginas num só array.
4. Acha as chaves distintas com `union()`.
5. Para cada chave, com concorrência 20: `Filter array` e soma por `xpath(xml(...), 'sum(/r/v)')`.
6. Ordena com `sort()` e `reverse()` e corta no `top`.
7. Devolve o JSON ao agente.

**Lista permitida:** Eventos_Producao, Hora-Hora, TiposErros, RegistrosInspeção, ficha_producao, Producao_Montagem, Paradas_Montagem, Plano_OPs, Refugo_Bobinadeira, RefugoExtrusora_estrutura, Controle_Catenaria.

**Limites de segurança:**
- só leitura: o método é fixo em GET e o Uiu não consegue trocá-lo;
- o fluxo nunca grava;
- usa a conexão SharePoint que já existe (conta do William).

## Receitas nas instruções

O fluxo só soma. A regra de negócio fica nas instruções do Uiu, num bloco RECEITAS que diz qual chamada responde cada tipo de pergunta, por exemplo:

| Pergunta | Chamada |
|---|---|
| Volume por processo | Eventos_Producao, `tipo` Fim ou Parcial, agrupar `etapa`, somar `metros`; Vulcanização numa 2ª chamada com Início; Trançagem pela Hora-Hora |
| Trançagem por máquina | Hora-Hora, `field_0` do período, agrupar `field_2`, somar `field_7` (e `field_5` para a meta) |
| Refugo por código | TiposErros, agrupar `A`, somar `_x0043_` |
| Tempo Parado por motivo | Hora-Hora, agrupar `field_12`, somar `field_11` (é déficit contra a meta, não cronômetro; pausa programada separada) |

As receitas de parada, turno e refugo passam pelo `revisor` (Opus) antes de entrar.

## Etapas

| # | Etapa | Quem | Pede "sim" |
|---|---|---|---|
| 1 | Escrever a definição do fluxo e as receitas em arquivo; receitas ao `revisor` | chefe + revisor | não |
| 2 | Criar o fluxo no Studio (Workflows → agent flow), pelo designer ou pela API do Dataverse com a definição do item 1 | chefe, no navegador | **sim** (fluxo novo no ambiente) |
| 3 | Testar o fluxo sozinho contra o gabarito de 10/11 (as rodadas de teste não consomem créditos) | chefe | não |
| 4 | Adicionar o fluxo como ferramenta "Somar no GMS" no Uiu e colar as receitas nas instruções (rascunho) | chefe | não (rascunho) |
| 5 | Repetir os testes: volume de ontem, Trançagem por máquina, refugo por código no mês, Tempo Parado por motivo na semana, top 10 de refugo por mangueira no mês | chefe | não |
| 6 | Republicar no Teams | chefe | **sim** |

## Riscos e o que conferir

1. **TiposErros sem índice na data.** A `DataHoraRefugo` não é indexada e a lista passa de 5 mil linhas, então um filtro por data pode ser recusado pelo SharePoint. Saídas: filtrar por faixa de ID ou criar o índice na coluna, que é um clique na lista e pede **sim**.
2. **Tempo:** o fluxo chamado pelo agente tem limite de 100 segundos.
   - Um dia ou uma semana cabe com folga.
   - Um ano de Hora-Hora (cerca de 30 mil linhas) pode passar do limite. Para esse caso fica a `Uiu_Agregados`, como atalho de período longo, depois.
3. **Custo (Copilot Credits):**
   - Fluxo de agente: 13 créditos a cada 100 ações. Os testes no painel não consomem créditos, e com licença Microsoft 365 Copilot a execução pelo próprio usuário não é cobrada.
   - **O Claude Opus 4.8 é modelo de raciocínio:** cobra 10 créditos por mil tokens, e cada resposta do Uiu lê dezenas de milhares de tokens de instruções e conhecimento.
   - Medir o consumo de uma pergunta no Power Platform admin center antes de publicar e, se pesar, voltar ao GPT Chat Latest (Nov 2026). A ferramenta nova tira do modelo a parte difícil, que era a soma.
4. **Chave com valor vazio** (sem máquina, sem motivo) vira o grupo "(vazio)", mostrado separado, nunca descartado.
