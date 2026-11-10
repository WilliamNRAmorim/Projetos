# Arquitetura proposta e contratos de dados do Uiu

Proposta de engenharia elaborada em 09/11/2026 a partir da pesquisa e dos arquivos locais. Os nomes de ferramentas abaixo são candidatos a implementação.

## Objetivo da arquitetura

Uma resposta industrial deve permitir reconstruir a decisão. Para “top 10 de refugo”, precisamos saber o período, a definição de refugo, as listas lidas, a quantidade de registros processados, as duplicidades tratadas, a regra de vínculo com o produto e a data da extração.

A documentação do Copilot Studio sustenta o uso de ferramentas, conhecimento e avaliação. Os contratos e os controles de consistência deste documento são decisões de projeto propostas para o GMS. [Referência de arquitetura](https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/generative-orchestration)

## Fluxo de uma resposta

1. Identificar intenção, objeto, período e unidade.
2. Recuperar a regra aplicável e sua vigência.
3. Selecionar a ferramenta autorizada para a pergunta.
4. Validar parâmetros e obter o resultado.
5. Verificar completude, atualização e compatibilidade do recorte.
6. Apresentar resultado e evidência, explicando limitações concretas.
7. Registrar a avaliação ou a necessidade de revisão.

O Uiu deve guardar o contexto relevante como campos explícitos durante o fluxo, incluindo OP, máquina, data inicial/final e métrica. Quando o usuário disser “e no mês passado?”, alterar o período preservando os demais filtros confirmados.

## Camadas propostas

| Camada | Responsabilidade | Evidência de funcionamento |
|---|---|---|
| Conhecimento aprovado | Normas, produto, regras locais e diagnósticos | Trecho recuperado com revisão |
| Consulta operacional | OP, eventos, apontamentos e inspeção | IDs e atualização da fonte |
| Cálculo de indicadores | Agregação completa e reproduzível | Total reconciliado e cobertura |
| Análise exploratória | Comparações e hipóteses | Método e dados de entrada |
| Orquestração | Escolha dos recursos e redação | Rastro de ferramentas |
| Alteração controlada | Aplicação de proposta revisada | Auditoria e resultado por item |

## Contrato comum de resposta das ferramentas

Proposta de esquema lógico, a adaptar aos conectores.

| Campo | Significado |
|---|---|
| request_id | Correlação entre conversa, execução e logs |
| status | ok, parcial, vazio, erro ou desatualizado |
| fonte | Lista, API ou conjunto de dados consultado |
| snapshot_id | Fotografia consistente usada na consulta |
| extraido_em | Momento da extração |
| maior_data_evento | Evento mais recente coberto |
| periodo_inicio / periodo_fim | Intervalo e convenção de fronteiras |
| fuso / regra_dia_produtivo | Interpretação temporal |
| filtros_aplicados | Critérios realmente usados |
| unidade | m, min, peça, kg ou outra unidade explícita |
| regra_versao | Identificador da regra aplicada |
| registros_lidos / elegiveis / excluidos | Conferência de cobertura |
| completo | Indicador de término da paginação |
| dados | Resultado numérico ou documental |
| evidencias | Links e IDs usados na conclusão |
| avisos | Lacunas específicas que afetam a leitura |

“Última atualização do fluxo” e “último evento da fonte” são campos separados. Um fluxo pode rodar com sucesso sobre um export antigo.

## Ferramentas prioritárias

### Consultar OP GMS

Entrada com OP e, se necessário, lote ou identificador da ficha. Retornar todos os vínculos candidatos se a OP aparecer em múltiplas fichas. Usar o ID da ficha para detalhe. Apresentar etapa, status, eventos, quantidades, cancelamentos, inspeção e packing quando disponíveis.

Falhas previstas: OP inexistente, OP com múltiplos lotes, permissão negada e ausência de atualização. Nenhuma dessas condições deve virar quantidade zero.

### Consultar indicadores GMS

Entrada com métrica enumerada, período, etapa, máquina, turno, produto e agrupamento permitido. Retorno deve conter o contrato comum. Definir catálogo de métricas com numerador, denominador e regra temporal.

O número de grupos retornados pode ser limitado para apresentação. O cálculo deve considerar o universo elegível completo. O “Top 10” será aplicado após a agregação.

### Conciliar OP SAP e GMS

Entrada com OP, material, centro e período. Recuperar documento/item SAP e evento de origem GMS. Tratar estorno conforme o sinal e o tipo na fonte. Entregar diferenças por material, documentos relacionados e classificação da pendência. O critério local de usuários que lançam refugo deve ter configuração versionada.

### Consultar especificação aprovada

Entrada com código completo, bitola, terminal, região e revisão ou data de fabricação. Entregar fonte aprovada, situação da combinação e parâmetros aplicáveis. Ausência de combinação válida deve gerar uma lacuna de engenharia claramente identificada.

### Diagnosticar ocorrência

Receber sintoma, lote/OP e fase em que foi detectado. Retornar evidências, causas candidatas e próximo teste que separa hipóteses. Uma causa só passa a confirmada quando o critério de comprovação definido pela qualidade for atendido.

## Revisão da proposta Uiu_Agregados

O plano existente propõe uma lista com Tipo, Periodo, Etapa, Maquina, Mangueira, Turno, Motivo, Valor e Unidade. Acrescentar fotografia, revisão de regra, cobertura e chave de grupo evita ambiguidades na consulta.

Granularidades propostas

| Fato | Grão |
|---|---|
| Produção | Dia produtivo × etapa × máquina × turno × produto |
| Refugo | Dia de referência × máquina × produto × código de defeito |
| Perdas de tempo | Dia × máquina × turno × classe de perda × motivo |
| Conciliação | Centro × OP × material × período |
| Qualidade dimensional | Característica × amostra × lote × instante |

Guardar fatos com grão distinto em tabelas separadas ou com validação rígida por Tipo. Para dados estatísticos, manter observações individuais disponíveis. Um agregado mensal é insuficiente para construir uma carta cronológica ou investigar uma mudança de processo.

## Atualização consistente

Proposta de processamento

1. Definir snapshot e versão de regra antes de iniciar.
2. Ler todas as páginas da fonte, com ordenação estável.
3. Normalizar tipos e registrar erros de conversão.
4. Aplicar validações e gerar totais de controle.
5. Gravar o novo snapshot completo em área de preparação.
6. Verificar contagens, chaves, totais e partições.
7. Tornar o snapshot válido visível ao agente por um marcador de publicação.
8. Manter o anterior disponível para recuperação.

Retentativa deve usar uma chave idempotente, para que o mesmo lote seja reconhecido. Corrigir um lançamento antigo exige reprocessar a partição afetada. Usar apenas a data do último evento pode perder alterações retroativas.

Para SharePoint, confirmar limites e índices antes de definir volume. Caso o tempo ou a capacidade sejam insuficientes, avaliar Dataverse, banco analítico ou camada governada já disponível na empresa. A decisão depende de volume, licença, acesso e operação.

## Duplicidades

O plano anterior sugere OP + erro + quantidade + data para detectar duplicidade de refugo. Essa combinação é candidata a auditoria. Dois apontamentos legítimos podem coincidir nesses campos. Antes de excluir do total, procurar ID de origem, item duplicado, integração repetida ou regra aprovada de desempate. Registrar duplicatas confirmadas separadamente de suspeitas.

## Temporalidade

Usar intervalos de início inclusivo e fim exclusivo. Converter instantes com fuso explícito. Aplicar dia produtivo e turno por regra com vigência.

As fronteiras T1 05:20, T2 13:57 e T3 22:20 constam do pacote recente. O histórico registra uma janela anterior de classificação diferente. A ferramenta deve distinguir turno gravado, turno recalculado e correção aprovada.

## Conhecimento versionado

Metadados propostos para cada seção

- Identificador estável, título e domínio.
- Fonte original, seção e versão.
- Data de revisão e vigência.
- Produto, etapa e planta a que se aplica.
- Proprietário técnico e status de aprovação.
- Documento substituído e motivo da mudança.
- Hash de conteúdo para identificar duplicação.
- Restrição de acesso.

O pacote contém fontes externas, regras da fábrica e hipóteses. A indexação deve preservar esses tipos. Um catálogo comercial pode explicar a construção de uma mangueira, mas a instrução de fabricação e o desenho aprovado precisam governar os parâmetros específicos da linha.

## Alterações futuras

Uma operação de correção deve receber proposta já calculada, IDs, versão esperada de cada registro, autor e motivo. Antes de gravar, reler o estado. Se o registro mudou, recompor a proposta. Em lote parcialmente concluído, registrar sucesso/falha por item para permitir retomada. A auditoria deve ligar pedido, aprovação, execução e resultado.

Esse desenho complementa a regra local de mostrar antes/depois e obter confirmação para correções. A autorização de pesquisa desta sessão resulta na documentação e nos casos de teste.
