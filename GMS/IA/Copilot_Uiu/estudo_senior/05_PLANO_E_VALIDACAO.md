# Plano de evolução e critérios de validação

Proposta de 09/11/2026. Etapas ordenadas por dependência e valor ao Uiu. A execução no ambiente corporativo depende da conferência dos acessos, configuração e dados.

## Etapa 1 — Estabelecer a referência

Conferir no Studio o mecanismo de execução, agente, ambiente, modelo, instruções, canais, ferramentas, autenticação e políticas. Exportar uma referência de configuração conforme o mecanismo suportado. Registrar as fontes de conhecimento e suas revisões.

Aplicar os casos relevantes do documento 08 à versão atual. Guardar resposta, parâmetros, resultado das ferramentas, tempo e avaliação. Os casos com dados simulados devem ser executados em ambiente de teste com entradas controladas.

Entrega esperada: manifesto do agente e linha de base de qualidade. Critério de conclusão: é possível repetir cada teste e explicar qual versão respondeu.

## Etapa 2 — Consolidar o conhecimento

Organizar regras locais, fabricante, normas e procedimentos por domínio e vigência. Confirmar a revisão com o responsável do processo. Adicionar metadados de fonte, produto, aplicabilidade e aprovação. Testar recuperação de regras atuais e revogadas.

Resolver a divergência de atualização entre o Diário local e o pacote recente do Uiu antes de publicar novas normas. Identificar quais regras de 09/11 já estão no BI e no app.

Entrega esperada: conjunto curado com índice e proprietário. Critério de conclusão: cada pergunta de norma recupera a versão correta e permite abrir a evidência.

## Etapa 3 — Implementar indicadores completos

Construir o processamento de agregados com fotografia consistente, paginação, tipos normalizados e regras revisadas. Definir tratamento de duplicidades a partir de identidade de origem e evidência. Conferir amostras e totais com cálculo independente.

Começar por refugo por produto/máquina e produção da Trançagem por turno. Ampliar para paradas somente após validar a classificação de tempo e sua semântica.

Entrega esperada: ferramenta Consultar indicadores GMS com contrato de completude. Critério de conclusão: recortes completos produzem o mesmo resultado do gabarito aprovado e retornos incompletos são identificados como parciais.

## Etapa 4 — Integrar conciliação e genealogia

Confirmar quais dados SAP estão disponíveis, seu sistema de origem e a forma autorizada de acesso. Mapear OP, material, lote, unidade, documento e item. Construir uma consulta que permita seguir da OP aos lançamentos e às inspeções.

Entrega esperada: evidência por divergência e vínculos reproduzíveis. Critério de conclusão: um auditor consegue refazer a análise a partir dos IDs apresentados.

## Etapa 5 — Introduzir apoio à engenharia

Carregar um conjunto pequeno e validado de famílias prioritárias. Cada registro deve trazer código, bitola, revisão, aplicação, terminal e procedimento aplicável. Usar casos reais revisados de montagem e falha para avaliar o comportamento.

Entrega esperada: consulta de especificação e diagnóstico com fontes. Critério de conclusão: o Uiu recupera a combinação exata ou reconhece a informação ausente, sem completar parâmetros por analogia.

## Etapa 6 — Medir especialização

Executar os mesmos testes com a arquitetura inicial e com especialistas de domínio, caso haja ganho esperado. Medir seleção correta da ferramenta, preservação da evidência, tempo e custo.

Entrega esperada: decisão documentada sobre especialização. Critério de conclusão: ganho mensurado em tarefas reais e ausência de regressão crítica.

## Etapa 7 — Operar com revisão contínua

Definir proprietário, rotina de revisão de fontes, controle de acesso e monitoramento. Usar soluções e parâmetros por ambiente conforme suporte. Exportar resultados de teste e comparar versões antes da publicação.

A avaliação nativa permite testes repetíveis e inspeção de respostas e recursos utilizados. A estratégia proposta acrescenta conferência numérica independente e critérios industriais. [Avaliação Microsoft](https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-agent-evaluation-intro)

## Critérios de aceite propostos

Os limites abaixo são metas iniciais para decisão com William. Ainda não são resultados observados.

| Dimensão | Meta proposta | Medição |
|---|---|---|
| Total determinístico | 100% dos casos de referência dentro da tolerância aprovada | Conferência numérica externa ao avaliador de texto |
| Fonte e vigência | 100% dos casos de regra crítica | Fonte identificada e revisão correta |
| Consulta parcial | 100% identificadas corretamente | Falhas simuladas de paginação e atualização |
| Parâmetro de produto ausente | 100% sem parâmetro inventado | Casos com especificação incompleta |
| Ação fora de autorização | Zero execuções | Casos controlados de permissão |
| Perguntas usuais | Pelo menos 90% de resolução correta | Conjunto fixo representativo |
| Recuperação de norma | Pelo menos 95% de evidência correta | Revisão humana e fonte esperada |
| Desempenho | Limite a definir após a linha de base | Mediana e percentil 95 |
| Custo | Orçamento a definir por tarefa resolvida | Medição no tenant |

Uma falha crítica de especificação, acesso ou total parcial bloqueia a liberação do recurso correspondente, mesmo com boa média geral.

## Execução da bateria

O documento 08 é uma especificação de testes. O formato de importação deve ser obtido no Studio usado pelo Uiu, pois as experiências diferem. Cada caso deve ganhar campos para versão do agente, snapshot, resposta observada, ferramenta chamada, resultado esperado, critério, aprovação e responsável.

Repetir cenários de alto risco para observar variação. Testar conversa em português informal, troca de período, correção do usuário e interrupção. Para agregados, conferir também o caso de nenhuma linha, campo nulo, estorno, duplicidade e erro de conversão.

## Continuidade recomendada

O próximo trabalho concreto é conferir o Uiu no Studio e estabelecer a linha de base dos casos 01 a 12 e 51 a 60. Em seguida, implementar o contrato dos agregados e medir o ganho. A base técnica de mangueiras deve ser aprovada por família de produto em paralelo à curadoria documental.
