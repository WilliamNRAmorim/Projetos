# MES SAP e controle da qualidade no Uiu

Síntese de pesquisa e desenho proposto, 09/11/2026.

## 1. Relação entre fábrica e sistemas

A ISA-95 organiza a integração entre funções empresariais e de controle e operação da manufatura. Seu modelo orienta os objetos e as informações compartilhadas entre níveis. Para o Uiu, é útil distinguir planejamento empresarial, execução da ordem e evidência do processo. [ISA-95](https://www.isa.org/standards-and-publications/isa-standards/isa-95-standard)

Proposta de responsabilidades a validar na planta

| Domínio | Fonte candidata | Papel do Uiu |
|---|---|---|
| Cadastro e movimentos empresariais | SAP | Explicar e conciliar lançamentos |
| Execução da ordem | GMS | Consultar andamento, eventos e quantidades |
| Processo físico | Equipamentos e registros aprovados | Relacionar condições com ocorrências |
| Especificação do produto | Desenho, cadastro e engenharia | Recuperar revisão aplicável |
| Qualidade | Inspeções e registros de não conformidade | Apresentar resultado, situação e evidências |
| Indicadores | Camada governada do BI | Explicar definição e reproduzir recorte |

A instalação real da empresa precisa ser identificada. O fato de a SAP oferecer Digital Manufacturing não demonstra que o produto esteja implantado na Danfoss Guaratinguetá.

## 2. SAP e integração

A documentação pública de integração do SAP Digital Manufacturing menciona dados de ordem, estoque, lote e qualidade em comunicação com ERP ou S/4HANA. As páginas SAP abertas apresentaram conteúdo limitado na ferramenta de leitura. A pesquisa registrou o material indexado e deixou a validação detalhada do cenário, APIs, edição e permissões como pendência. [Integração SAP](https://help.sap.com/docs/sap-digital-manufacturing/integration-guide/business-integration-with-sap-s-4hana-or-sap-erp)

A referência SAP de genealogia relaciona materiais e operações a produtos serializados, incluindo características de inspeção. Para o Uiu, a proposta é permitir seguir um lote até os conjuntos montados e voltar de uma ocorrência de cliente aos materiais e processos envolvidos. A granularidade disponível no GMS precisa ser confirmada. [Genealogia SAP](https://help.sap.com/docs/SAP_S4HANA_ON-PREMISE/9c4986bda35f4840ae438960ffbef64d/f06fb7d493fd40ada77cd1e41802b714.html)

## 3. Objetos mínimos de rastreabilidade

- Material com código e revisão.
- Ordem, operação e lote de produção.
- Lote de composto, arame, cobertura e terminais conforme disponibilidade.
- Equipamento e ferramenta usados.
- Registro de execução com instante, turno e operador autorizado.
- Inspeção, característica, resultado e instrumento.
- Conjunto montado, identificação e expedição.
- Não conformidade, contenção, análise, ação e verificação.

O relacionamento pode ser muitos-para-muitos. Uma batelada atende várias OPs, uma OP pode gerar vários lances e um conjunto pode consumir mais de um componente. O desenho precisa representar divisão, mistura e retrabalho explicitamente.

## 4. Conciliação SAP GMS

Regras locais identificadas no pacote

- Vincular material pela OP e verificar aliases aprovados.
- Considerar unidade M quando o indicador for metragem.
- Tratar estornos sem inverter duas vezes valores já negativos.
- Examinar diferenças por material.
- Tratar exports como fotografias com datas distintas.
- Identificar produção boa e refugo segundo os critérios locais documentados.
- Excluir linha de total do export quando ela estiver junto dos movimentos.
- Considerar que um lance pode ter sido apontado em outra OP do mesmo material.

O uso dos usuários SAP U445131 e U452021 para identificar refugo é uma convenção do conjunto de dados local. Deve ser validado com os responsáveis do processo e versionado antes de uso contínuo.

Proposta de estados de conciliação

| Estado | Evidência exigida |
|---|---|
| Conciliado | Chaves, unidade, período e quantidade compatíveis |
| Diferença temporal | Documento ou evento localizado em outra data |
| Divergência de material | OP associada a produto inconsistente |
| Suspeita de duplicidade | Correspondência forte e IDs disponíveis |
| Movimento sem contrapartida | Fonte completa e ausência verificada |
| Dados insuficientes | Cobertura, vínculo ou campo faltante |
| Correção proposta | Antes/depois com origem e justificativa |
| Correção verificada | Releitura e reconciliação após execução |

## 5. Indicadores com definição rastreável

| Indicador | Elementos a fixar |
|---|---|
| Produção da etapa | Evento ou apontamento, etapa e quantidade válida |
| Produção final | Ponto de saída escolhido e regra para retrabalho |
| Refugo | Quantidade, classificação e momento de reconhecimento |
| Percentual de refugo | Numerador e denominador no mesmo recorte |
| PPM | Tipo de defeito/erro e denominador aprovado |
| Aderência Hora-Hora | Real e meta da mesma janela e velocidade |
| WIP | Estado, quantidade e instante da fotografia |
| Lead time | Eventos de início/fim e regra de calendário |
| Parada | Intervalo e classe de perda |
| OEE/TCU | Fórmula aprovada e definição de tempo |

No pacote local, a produção da Trançagem passou a usar Hora-Hora. A meta útil de 21h45 aparece como decisão de 09/11 para recortes específicos do BI. O Uiu deve citar a decisão e verificar sua aplicação no modelo publicado antes de reproduzir o indicador.

A soma de metros das oito etapas representa atividade ao longo do processo e precisa de um rótulo compatível. Para responder “quanto de mangueira produzimos?”, a definição aprovada deve escolher o ponto de produção final. Misturar essas granularidades distorce a resposta.

## 6. Qualidade da medição e estabilidade

O material ASQ sobre saúde do processo destaca que capacidade, centragem, estabilidade e sistema de medição são dimensões relacionadas. Aplicação proposta: antes de interpretar uma mudança no diâmetro, identificar instrumento, método, resolução, condições e série de medições. [Saúde do processo](https://asq.org/quality-resources/articles/a-recommended-set-of-indices-for-evaluating-process-health?id=b0a157d516a0434d9c16b057aa3ef2c6)

Cartas de controle acompanham dados em sequência temporal e ajudam a examinar sinais de mudança. O tipo de carta e os critérios devem corresponder ao tipo de dado e à amostragem. Limites de controle e limites de especificação têm origens diferentes e precisam aparecer com identificação própria. [Cartas de controle ASQ](https://asq.org/quality-resources/control-chart)

Proposta de contrato para análise estatística do Uiu

1. Característica, unidade e revisão da especificação.
2. Dados individuais ou subgrupos, com ordem temporal.
3. Produto, máquina, ferramenta, lote e turno.
4. Tratamento de ausências, retrabalho e valores inválidos.
5. Método de estimativa e hipóteses da análise.
6. Situação do sistema de medição.
7. Resultado reproduzível e interpretação revisada.

Um índice de capacidade calculado sobre mistura de produtos ou limites incorretos pode aparentar precisão e ainda induzir uma conclusão errada. O agente deve identificar esses casos antes de calcular.

## 7. FMEA plano de controle e tratativa

A ASQ descreve FMEA como método de identificar modos de falha, efeitos e prioridades de ação, com aplicação em projeto e processo. O Uiu pode ajudar a reunir evidências e redigir uma proposta de análise para revisão multidisciplinar. [FMEA ASQ](https://asq.org/quality-resources/fmea)

Modelo proposto de vínculo

| Elemento | Registro esperado |
|---|---|
| Requisito | Função do produto ou operação |
| Falha potencial | Perda da função e efeito |
| Causa candidata | Mecanismo a investigar |
| Controle | Prevenção ou detecção documentada |
| Característica | Variável acompanhada |
| Plano de reação | Responsável e ação prevista |
| Evidência | Ensaio, inspeção, ocorrência e versão |
| Eficácia | Resultado após a ação |

Para ocorrência real, o Uiu deve ajudar a definir escopo, identificar lotes potencialmente afetados, reunir evidências, testar causas e verificar eficácia. O registro precisa separar a ação que contém o problema da ação que elimina sua causa.

## 8. Receitas de investigação propostas

### Aumento de refugo por trançadeira

Validar período e cobertura. Comparar refugo absoluto e taxa dentro de grupos de produto compatíveis. Conferir mudanças de mix, volume, código de defeito e registro. Investigar materiais e processo com os responsáveis. A máquina com mais metros de refugo pode ser também a de maior produção.

### Divergência de produção entre SAP e GMS

Selecionar o mesmo material, OP, unidade e intervalo. Listar movimentos e eventos. Identificar estornos, duplicidades, datas diferentes, cancelamentos e troca de OP. Exibir documentos que explicam cada parcela.

### Queda de aderência Hora-Hora

Conferir a meta vigente, duração da janela, velocidade e produto. Separar perda por classificação de tempo, falta de apontamento e desempenho. O próprio pacote local diferencia parada real, pausa programada e tempo excedido.

### Falha de conjunto montado

Identificar produto, revisão, lote de mangueira, terminais e registros de montagem. Recuperar procedimento e resultados de inspeção. Relacionar condições de uso e evidências do componente. Encaminhar conclusão técnica à engenharia/qualidade com rastreabilidade.
