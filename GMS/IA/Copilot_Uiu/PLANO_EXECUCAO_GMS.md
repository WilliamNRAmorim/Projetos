# Uiu — plano de execução baseado no GMS

Versão 2.0 · 09/11/2026, horário de Brasília · revisão de planejamento solicitada por William.

**Este é o ponto de entrada vigente para planejar a evolução do Uiu.** Detalha o plano F0–F5 sem alterar normas industriais, telas, dados ou configuração publicada. O pedido atual é estruturar e cobrir gaps antes de implementar. Nenhuma fase técnica passa a concluída pela existência deste documento.

## 1. Resultado que queremos entregar

William consulta o Uiu no Teams e obtém respostas verificáveis sobre OPs, produção, refugo e perdas do GMS, com período, unidade, cobertura e evidência. O Uiu explica as regras, investiga B.O.s e, numa fase posterior já prevista, executa somente correções do catálogo confirmado. A resposta de um agregado suportado deve sair no próprio Uiu; mandar para o BI não é o fluxo normal. Quando faltar informação, ele identifica exatamente o que falta.

Critério de entrada de trabalho: resolver uma pergunta do GMS, uma pendência F0–F5 ou uma dependência necessária para a confiabilidade desse resultado. A lista anterior de 50 propostas não é o backlog oficial; sua destinação está na [matriz de gaps](planejamento/GAPS_E_DECISOES.md).

## 2. O que permanece e o que não entra nesta entrega

Permanecem as decisões registradas no [plano original](PLANO_UIU.md): William como único usuário; quatro papéis (Consulta, Detetive, Mecânico, Professor); agregados; recursos premium previstos; correções com antes/depois, confirmação e log; Teams e alertas. A confirmação de uma proposta de correção continua vinculada àquela proposta e aos itens exibidos.

O projeto não passa a ser somente leitura para sempre: a operação documentada atual é de leitura e F3 continua no plano. Entretanto, aprovação conceitual do Mecânico não resolve ambiguidades de suas receitas nem comprova sua implantação.

Ficam fora da primeira entrega: nova integração direta SAP, novo MES, alteração de telas do app, mudança de regra de OEE2, conciliação Hora-Hora × ficha adiada em MEL-266, saneamento amplo do histórico, Factbird, treinamento de modelo local, previsão de falha, Cpk/SPC e liberação de produto. O estudo de mangueiras, conjuntos e crimpagem permanece como referência para uma evolução específica; não bloqueia F2.

Consulta de especificações já existentes no GMS pode ser preservada como capacidade atual se confirmada. Criar uma base de engenharia de conjuntos é outro pacote, com necessidade e responsável próprios.

## 3. Estado de partida e confiabilidade da evidência

| Elemento | Última evidência documental | Tratamento nesta revisão |
|---|---|---|
| Agente usado | DPS - Non Prod; bot `dd8888ce-de52-4f4a-be5f-1a2109a461cf` | Confirmar ao vivo na entrada E0; não trabalhar no Default antigo |
| Ambiente | `8944b737-0def-e6f9-93c8-840d950e5e44` | Ambiente compartilhado de não produção; não presumir aprovação para operação corporativa permanente |
| Canal | Publicação em 09/11 às 14:39, Microsoft 365/Teams, somente William | Publicação inicial não é pendência nova; português posterior ainda aguardava republicação |
| Ferramentas | 32 de leitura SharePoint, incluindo Ler conhecimento do GMS | Inventariar nomes, parâmetros, conexões e permissões reais |
| Conhecimento | 11 Markdown, 75 seções em Uiu_Conhecimento | Conferência anterior documentada; comparar versão local/remota antes de substituir |
| Recursos | Deep reasoning ligado; Code Interpreter desligado | Intenção aprovada não equivale a recurso ativo ou licença confirmada |
| Qualidade | Dois testes pontuais descritos, em ambientes diferentes | Não equivalem a bateria aprovada no DPS/Teams |
| Documentação | Diário local vai até 06/11; pacote de conhecimento tem decisões de 09/11 | Conciliar origem antes de regenerar conhecimento ou atribuir novo MEL |

Fonte desse estado: [passagem anterior](PROXIMA_SESSAO.md) e [histórico do Studio](instrucoes/estado_studio_2026-11-09.md). Não houve nova inspeção do tenant nesta revisão. As contagens de listas são referências de 09/11, não capacidade medida agora.

## 4. Organização dos documentos

| Documento | Responsabilidade |
|---|---|
| Este plano | Escopo, dependências, entregas e critérios de avanço |
| [Gaps e decisões](planejamento/GAPS_E_DECISOES.md) | Evidência da lacuna, solução, responsável, bloqueio e destinação das 50 propostas |
| [Contratos e métricas](planejamento/CONTRATOS_E_METRICAS.md) | Identidades, fontes, temporalidade, cálculos, integridade e correções |
| [Execução e aceite](planejamento/EXECUCAO_E_ACEITE.md) | Trabalho executável, casos de teste, liberação e recuperação |
| [Estudo técnico](estudo_senior/00_LEIA_PRIMEIRO.md) | Referências e hipóteses; não define sozinho o escopo ou a norma do GMS |

As normas do GMS e suas emendas continuam acima deste plano. Divergência entre resumo, norma e publicado vira item com evidência, sem escolher silenciosamente a versão mais conveniente.

## 5. Arquitetura a validar antes de construir

Manter Copilot Studio, SharePoint e Power Automate como base. Separar três responsabilidades: consulta operacional limitada; processamento completo de indicadores fora do contexto do modelo; interpretação e resposta pelo Uiu.

O processamento faz extração paginada, normalização, validação e agregação. Publica uma versão validada em Uiu_Agregados com controle de execução. A ferramenta de consulta recebe parâmetros de negócio restritos e devolve resultados compactos. O modelo não recebe listas inteiras para executar contas oficiais.

Code Interpreter é recurso auxiliar de exploração/apresentação, condicionado ao suporte e à licença do ambiente. Não resolve paginação, falta de fonte, autorização, regra de negócio ou integridade. F2 não depende dele para acertar o total.

Conservar os quatro papéis do plano. Antes de criar quatro agentes físicos, testar o mecanismo de execução disponível, o repasse de contexto/evidência, as permissões e o custo. Os contratos serão os mesmos se a implementação usar tópicos/ferramentas ou agentes-filho. Uma mudança da arquitetura física aprovada será registrada como decisão, não feita silenciosamente. A quantidade de agentes não é critério de aceite.

Uiu_Agregados permanece a primeira opção de armazenamento, sujeita a uma prova com volume real. Não criar banco ou migrar para Dataverse por antecipação. Se a prova falhar por volume, duração ou limites do tenant, documentar a medição e mudar somente a camada necessária, mantendo os contratos.

## 6. Sequência com dependências e entregas

| Entrega | Fase original | Entrada obrigatória | Trabalho e saída | Critério para avançar |
|---|---|---|---|---|
| E0 — referência do ambiente | Pré-F0/F1 | Leitura dos documentos atuais e acesso corporativo | Inventário, export disponível, versões e evidência do publicado; verificar fonte do Diário | Agente correto identificado; configuração recuperável; divergências registradas |
| E1 — definições e conhecimento | F0/F1 | E0 para estado remoto; análise local pode iniciar antes | Dicionário de métricas/fontes, decisões de negócio por recorte, atualização das receitas e instruções | Nenhuma regra ambígua codificada como certeza; pacote de conhecimento conferido |
| E2 — prova da extração e cálculo | F2, com F4 desde o início | E1 das métricas do piloto | Fotografias controladas, paginação, vínculos, cálculo e gabarito independente | Completude e integridade comprovadas; desempenho/custo medidos |
| E3 — primeiro resultado útil | F2 + F4 + canal existente F5 | E2 para refugo | Top 10 anual de refugo TiposErros por mangueira ou trançadeira, detalhamento e filtros no Uiu | Total/ranking corretos no Studio e no Teams, sem encaminhamento obrigatório ao BI |
| E4 — ampliar e operar F2 | F2 + F4 | E3 e definições específicas resolvidas | Produção por etapa/turno, perdas classificadas, atualização recorrente e rotina de recuperação | Cada métrica liberada separadamente; período antigo corrigido atualiza resultado |
| E5 — Mecânico controlado | F3 + F4 | E1, consulta confiável e receita individual aprovada | Proposta, confirmação, guarda de versão, alteração restrita, log e releitura | Testes de conflito e falha parcial aprovados; nenhuma gravação fora da receita |
| E6 — alertas úteis | F5 + F4 | Indicador/diagnóstico da regra já aceito | Alertas com destinatário William, limiar, deduplicação e encerramento | Não dispara por dado velho/incompleto; não repete a mesma ocorrência sem necessidade |

E5 não precisa esperar todo o catálogo de E4, mas só pode usar fontes e receitas já validadas. E6 não depende de habilitar o Mecânico. Correção de português no canal pode ser uma publicação pequena após E0 e teste, sem esperar os agregados.

## 7. Primeiro recorte e evolução sem trocar o fundamento

O primeiro recorte é a pergunta que já falhou: “top 10 anual de refugo por mangueira/trançadeira”. A primeira métrica será nomeada **refugo registrado na TiposErros**, em metros. Não será apresentada como K10 consolidado, que inclui outras origens.

Para ranking por mangueira, resolver vínculos OP → ficha sem multiplicar apontamentos. Para trançadeira, usar o campo da origem com semântica explícita, sem chamar isso de causa comprovada do defeito. Definir ano e limites de cobertura antes de responder. Ano corrente significa acumulado coberto do ano; ano encerrado exige cobertura integral do período solicitado.

O schema já deve suportar dia, produto, máquina, turno, motivo, fonte, regra e versão de carga, mesmo que a primeira pergunta seja anual. Isso evita reconstruir a base quando vier “e no mês passado?”. Dimensões sem fonte confiável ficam indisponíveis, não preenchidas por inferência.

## 8. Critérios gerais de aceite

1. Cada entrega liga requisito → regra/fonte → implementação → teste → evidência → versão publicada.
2. Totais são conferidos por cálculo independente no mesmo recorte e snapshot; arredondamento apenas na exibição, com precisão da origem documentada.
3. Zero falha crítica em completude, autorização, vínculo, unidade e especificação. Uma média de 90% não compensa essas falhas.
4. Meta original de pelo menos 90% vale para os casos funcionais elegíveis e executados da entrega, com denominador, falhas e casos bloqueados separados.
5. Todo indicador informa cobertura e atualização; dado ausente não vira zero e dado velho não vira “hoje”.
6. Sucesso no painel do Studio não substitui teste no Teams, com a identidade realmente usada.
7. Critérios de latência, frequência, retenção e custo são fechados com medições de E2 antes de E4; sem esses valores não se declara prontidão operacional.
8. Conhecimento externo ou resposta livre não autoriza ferramentas nem substitui especificação aprovada.

## 9. Responsabilidades e decisões ainda necessárias

| Papel | Responsabilidade |
|---|---|
| William | Priorizar perguntas; confirmar ambiguidades do processo e gabaritos; validar propostas de correção |
| Implementador | Produzir contratos, fluxos/instruções, testes, evidências e pacote de recuperação |
| Revisor técnico do GMS | Conferir turno, parada/setup e receitas que alteram dados; registrar parecer e ressalvas |
| Administrador do ambiente/TI | Confirmar licença, políticas, conexões, ambiente e condições para uso permanente quando necessário |

Nenhuma pessoa ou agente foi convocado por esta revisão. O papel revisor é requisito de qualidade previsto no projeto, não comprovação de revisão já feita.

As decisões D01–D09 da matriz serão solicitadas somente quando bloquearem a entrega correspondente, já acompanhadas da amostra e da consequência de cada escolha. Primeiro será feita a busca de evidência nos documentos e no ambiente; só uma ambiguidade não resolvida vai ao William. A ausência de resposta mantém aquele recorte bloqueado; não bloqueia documentação, testes sintéticos ou métricas independentes.

## 10. Controle de mudança e retomada

Antes de codificar um pacote, conferir: pergunta-alvo, fonte disponível, regra aprovada, identidade/grão, gabarito, teste negativo e recuperação. Se faltar algo, registrar o gap específico e concluir o trabalho independente.

Mudança de escopo deve apontar qual pergunta nova resolve e quais entregas altera. Não incluir funcionalidades para completar uma quantidade de propostas. Não modificar o Mestre nem o BI por esta revisão.

**Próxima ação concreta:** executar E0 e preparar o gabarito de E2 para o recorte TiposErros. Não criar ainda toda a lista de agregados nem habilitar ferramentas de escrita. Confirmar primeiro os campos, vínculos, cobertura e comportamento da extração com a mesma consulta que será usada no fluxo.

## 11. Referências da plataforma verificadas nesta revisão

- [Instruções de agentes](https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-instructions): instruções dependem de recursos efetivamente configurados; preservar o comportamento nativo de citações.
- [Get items e Get files](https://learn.microsoft.com/en-us/sharepoint/dev/business-apps/power-automate/guidance/working-with-get-items-and-get-files): limites, filtros e paginação exigem configuração e prova; Top Count alto não é evidência de cobertura completa.
- [Avaliação de agentes](https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-agent-evaluation-intro): conjuntos repetíveis e inspeção de resultados; confirmar suporte no mecanismo de execução e autenticação do Uiu.

Os contratos e os critérios industriais deste plano são decisões de projeto propostas a partir do GMS, não funcionalidades automaticamente fornecidas pelo Copilot Studio.
