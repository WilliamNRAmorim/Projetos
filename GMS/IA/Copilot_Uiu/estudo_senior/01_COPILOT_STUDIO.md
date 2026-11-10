# Copilot Studio aplicado ao Uiu

Estudo de 09/11/2026. As recomendações de arquitetura são propostas para validação no ambiente Danfoss.

## 1. Confirmar a experiência de execução

A documentação atual distingue mecanismos de execução, chamados harnesses. O Uiu documentado tem tópicos, orquestração generativa, ferramentas SharePoint e publicação no Teams. Esse conjunto sugere a experiência padrão, mas a identificação no Studio precisa ser confirmada. A Microsoft mantém documentação específica para experiência padrão e experiência com GitHub Copilot. A mesma expressão “agente” pode apontar para capacidades diferentes. [Visão geral](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-overview)

Na experiência com GitHub Copilot, capacidades internas reutilizáveis usam skills e a especialização externa usa agentes conectados. A FAQ informa que a migração cria uma cópia e deixa componentes para tratamento posterior, incluindo conhecimento, Power Fx e agentes-filho. A compatibilidade entre agentes de mecanismos diferentes também tem restrições. Aplicação proposta ao Uiu: inventariar os componentes atuais, reproduzir os testes e decidir sobre migração somente a partir do resultado. [FAQ do mecanismo GitHub Copilot](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/faqs-copilot-harness)

## 2. Orquestração generativa

A orquestração seleciona conhecimento, ferramentas, tópicos e outros agentes a partir das capacidades disponíveis e de suas descrições. O mapa de atividades permite examinar a sequência usada em uma resposta. Para o Uiu, a primeira análise de uma resposta errada deve identificar onde o erro surgiu: entendimento da pergunta, escolha de ferramenta, parâmetros, retorno, cálculo ou redação final. [Orquestração generativa](https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-generative-actions)

Proposta de rotina de diagnóstico

1. Repetir a pergunta com uma fotografia conhecida dos dados.
2. Registrar a ferramenta escolhida e seus parâmetros.
3. Conferir o retorno bruto e a paginação.
4. Comparar o cálculo com um resultado independente.
5. Verificar se a resposta preservou unidade, período e ressalvas.
6. Corrigir a camada responsável e repetir a bateria relacionada.

Exemplo de pergunta composta: “Qual trançadeira teve mais refugo no mês e quais OPs explicam isso?”. O contrato precisa estabelecer mês, critério do ranking, total, participação, OPs relacionadas e completude. A ferramenta de detalhe usa os identificadores do resultado agregado.

## 3. Instruções que descrevem capacidades reais

A Microsoft orienta que instruções estejam ligadas a ferramentas e conhecimento efetivamente configurados. Nomes, descrições e referências aos objetos ajudam a seleção pelo orquestrador. A alteração das instruções requer publicação para chegar à versão publicada. [Instruções do agente](https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-instructions)

Para o Uiu, cada ferramenta proposta deve ter uma finalidade única e exemplos de entrada. “Consultar produção da Trançagem” precisa declarar sua fonte, granularidade, período e unidade. A descrição deve explicar situações em que outro recurso é necessário, como conciliação contábil SAP ou especificação de crimpagem.

A instrução principal deve conter papel, sequência de trabalho, precedência das fontes, tratamento de falhas e formato da resposta. Regras extensas de produto ficam em documentos recuperáveis. Mapas físicos das colunas pertencem aos contratos das ferramentas, com referência para diagnóstico.

## 4. Conhecimento e recuperação

O comportamento da busca depende do modo de orquestração e do tipo de fonte. A documentação descreve seleção de fontes na orquestração generativa e diferenças frente ao modo clássico. A arquitetura deve ser testada com o caminho de ingestão realmente usado. [Fontes de conhecimento](https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-copilot-studio)

A página de limites diferencia busca em sites SharePoint e upload de arquivos do SharePoint. Tamanho permitido, processamento, sincronização e capacidade analítica variam por caminho e configuração. O estudo encontrou, por exemplo, limite documentado de payload de conector de 5 MB em nuvem pública. Isso reforça o uso de respostas compactas com total e evidência, em vez de transportar todo o histórico ao agente. Limites devem ser reconferidos antes da implantação. [Cotas e limites](https://learn.microsoft.com/pt-br/microsoft-copilot-studio/requirements-quotas)

Para a Uiu_Conhecimento, a proposta é acrescentar metadados de vigência e fonte. A recuperação deve retornar um pacote de evidências com título, seção, revisão, texto e link. Uma consulta por nome de arquivo pode funcionar no Get items configurado no projeto, mas o comportamento da busca nativa de conhecimento é outro e precisa de teste próprio.

Perguntas para testar recuperação

- Qual documento resolve a fronteira de turno vigente?
- Qual regra foi revogada e em qual data?
- Onde está a especificação exata para determinada família e bitola?
- Qual regra se aplica ao apontamento histórico, considerando sua data?
- O documento encontrado pertence à produção de mangueira ou à montagem de conjuntos?

## 5. Ferramentas e fluxos

A FAQ informa que um fluxo adicionado ao agente precisa estar em solução e conter o gatilho de chamada pelo agente e a ação de resposta. Fluxos criados no Power Automate e agent flows têm diferenças de gerenciamento e cobrança. [FAQ de agent flows](https://learn.microsoft.com/microsoft-copilot-studio/flows-faqs)

Desenho proposto ao Uiu

| Categoria | Entrada controlada | Saída de negócio |
|---|---|---|
| OP | Identificador e escopo | Etapa, eventos, quantidade, pendências |
| Indicador | Métrica, período, dimensões | Resultado, cobertura, regra e atualização |
| Conciliação | OP ou material, período | Lançamentos, diferença, evidências |
| Especificação | Código completo e revisão | Parâmetros aprovados e fonte |
| Diagnóstico | Sintoma e identificadores | Achados e testes que discriminam causas |
| Alteração futura | Proposta aprovada e versão esperada | Resultado por item e auditoria |

Os contratos devem controlar operadores, tipos, campos e escopo. Uma entrada textual ampla transformada diretamente em filtro exige validação adicional. Para consultas frequentes, oferecer parâmetros de negócio que o fluxo converte para os nomes internos corretos.

## 6. Code interpreter

A FAQ descreve execução Python em ambiente isolado para tratar arquivos, fazer análises e gerar resultados. O acesso é aos arquivos e entradas fornecidos. Há restrições de rede, tempo, documentos protegidos e apresentação de imagens em determinados canais. Assim, habilitar a opção precisa ser acompanhado de um caminho explícito para fornecer os dados completos e de testes no Teams. [FAQ de Code interpreter](https://learn.microsoft.com/en-us/microsoft-copilot-studio/faq-code-interpreter)

Aplicação proposta: usar cálculos determinísticos para indicadores oficiais e explorar hipóteses com Code interpreter sobre recortes identificados. Toda análise deve registrar a fotografia de dados, campos, exclusões, tratamento de nulos e versão da regra. Um gráfico de causa provável deve preservar a diferença entre associação estatística e comprovação de causa.

## 7. Especialização

Agentes-filho e conectados podem modularizar tarefas na experiência padrão. A documentação alerta para complexidade adicional, latência e preservação de citações entre agentes. [Outros agentes](https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-add-other-agents)

Para o Uiu, começar com o orquestrador e ferramentas bem delimitadas. Introduzir especialistas quando a avaliação mostrar confusão consistente de domínio. Os papéis candidatos são Operação MES, Qualidade e SAP, Engenharia de Produto e Diagnóstico. A futura função de correção deve ter permissões e critérios próprios. Cada resposta delegada precisa devolver evidências estruturadas ao orquestrador.

## 8. Identidade e políticas

O agente e suas ferramentas têm configurações de autenticação distintas. A autenticação do usuário nas ferramentas é relevante quando a operação precisa respeitar o acesso de quem está conversando. O uso de credenciais do criador precisa ser entendido antes de expandir o público do Uiu. [Autenticação das ferramentas](https://learn.microsoft.com/en-us/microsoft-copilot-studio/configure-enduser-authentication)

As políticas de dados podem limitar conectores, conhecimento e canais. O histórico local relata bloqueios no Default e migração para DPS – Non Prod. Para qualquer expansão, registrar a aprovação administrativa do desenho, as conexões usadas e o público autorizado. A possibilidade técnica de ler uma lista deve ser acompanhada da validação de uso dessa informação no agente. [Políticas de dados](https://learn.microsoft.com/microsoft-copilot-studio/admin-data-loss-prevention)

## 9. Avaliação e operação

A plataforma permite testar conjuntos de casos e comparar respostas com critérios. A execução considera a identidade usada na avaliação. O desenho do Uiu precisa incluir testes com o perfil real do usuário e confirmação no canal publicado. [Avaliação](https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-agent-evaluation-intro)

Critérios como qualidade geral, comparação semântica, correspondência exata, uso de ferramentas e avaliação personalizada respondem a perguntas diferentes. O teste de um total precisa conferir valor, unidade, recorte e completude. Uma avaliação de texto plausível, sozinha, não demonstra que o total está correto. [Métodos de avaliação](https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-agent-evaluation-overview)

Telemetria pode ir ao Application Insights. A documentação distingue escopo de agente e de ambiente, este último com recursos em prévia. Proposta: medir latência, falha por ferramenta, truncamento, respostas sem evidência e custo por tarefa concluída, com controle sobre conteúdo sensível dos registros. [Telemetria](https://learn.microsoft.com/microsoft-copilot-studio/telemetry-overview)

A estratégia de ALM deve definir desenvolvimento, teste e produção, soluções, referências de conexão e parâmetros por ambiente. Canais, autenticação e outras configurações podem precisar de passos após a implantação. Proposta ao Uiu: manter manifesto de versão com instruções, ferramentas, fontes, testes, identidade e procedimento de retorno. [ALM](https://learn.microsoft.com/microsoft-copilot-studio/guidance/alm)

## 10. Modelo e custo

A escolha do modelo deve ser comparada nas mesmas tarefas. Medir acerto, tempo, custo e qualidade de recuperação antes de elevar a capacidade de raciocínio de todas as perguntas. Consultar situação atual de OP e investigar uma falha de conjunto exigem esforços distintos.

A documentação apresenta cobrança por Copilot Credits com regras que dependem da experiência e do uso. A experiência GitHub Copilot descreve consumo desde a construção. O orçamento precisa separar desenvolvimento, avaliação e produção e ser conferido no tenant. [Cobrança por uso](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/billing-credit-overview)
