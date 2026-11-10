# Gaps, decisões e rastreabilidade do Uiu

Versão 2.0 · 09/11/2026 · complemento do [plano vigente](../PLANO_EXECUCAO_GMS.md).

Status desta matriz: **gaps documentados e tratamento planejado; implantação e aceite pendentes**. G01–G30 são identificadores desta revisão, não novos MELs. A evidência aponta arquivos relativos à pasta Copilot_Uiu; documentos históricos provam o registro, não o estado atual do tenant.

## Matriz de cobertura

| Gap | Evidência e risco concreto | Tratamento necessário | Entrega / responsável | Evidência de fechamento |
|---|---|---|---|---|
| G01 | PLANO_UIU começa no Default; PROXIMA_SESSAO registra DPS | Fixar ambiente/bot, inventariar publicado e rascunho, preservar cópia antiga | E0 / implementador | Export/configuração datada e identidade conferida |
| G02 | 32 ferramentas e conexão do autor; ambiente compartilhado Non Prod | Verificar permissões, licença e isolamento para William; não ampliar público | E0 / implementador e TI se necessário | Teste com identidade real e registro das restrições |
| G03 | Diário local termina 06/11; 08_Normas_Diario contém 09/11 | Reconciliar versões antes de regenerar, preservar origem/hash | E0–E1 / implementador | Pacote canônico identificado, sem perda das decisões recentes |
| G04 | F0 diz Knowledge nativo; estado usa Uiu_Conhecimento | Manter caminho funcional e versionar atualização por seção | E1 / implementador | Recuperação da revisão correta no DPS e contagem/texto conferidos |
| G05 | F1 prevê quatro filhos sem prova da configuração atual | Manter quatro papéis; validar divisão física, contexto e ferramentas | E1–E3 / implementador | Prova de roteamento, evidência preservada e custo comparado |
| G06 | F2 atribui somas completas ao Code Interpreter | Agregação determinística no processamento; recurso premium auxiliar | E2 / implementador | Totais corretos sem depender de uma soma do modelo |
| G07 | Top 50 no agente; Top alto proposto para agregados | Paginação/partição validada, filtros restritos e completude explícita | E2 / implementador | Teste além da primeira página e de falha intermediária |
| G08 | Instruções permitem tentar sem filtro após erro de coluna | Falhar com diagnóstico; validar schema e parâmetros antes da consulta | E1–E2 / implementador | Coluna inválida não gera resposta sobre amostra diferente |
| G09 | Fontes expõem zeros, vazios, texto e culturas distintas | Tipos por adaptador, quarentena de inválidos e contagens | E2 / implementador | Casos de vírgula, ponto, nulo e zero sem soma silenciosa |
| G10 | UTC, data de referência e rótulo de janela confundidos | Contrato temporal por fonte; não deslocar novamente data já produtiva | E1–E2 / implementador e revisor | Testes de meia-noite e 05h20 por origem |
| G11 | Roteiro informa publicação da v3.0.15 entre 27 e 29/10 a confirmar | Marcar faixa incerta; manter gravado/recalculado separados | E1 / William e revisor | D01 resolvida com evidência, sem correção histórica implícita |
| G12 | Resumos dizem uma linha por OP; mapa diz OP/lote | ID da ficha como identidade; join deve provar cardinalidade | E2 / implementador | Uma OP com duas fichas não duplica refugo |
| G13 | Mapa: recurso dos eventos é trançadeira de origem | Distinguir máquina da etapa, origem e cabine; normalizar só aliases aprovados | E1–E4 / implementador | Teste que impede atribuir produção de todas as etapas à TH da origem |
| G14 | Passagem manda deduplicar OP+erro+quantidade+data | Apenas sinalizar suspeitas; excluir só identidade repetida comprovada | E2 / implementador, William nos casos ambíguos | Eventos legítimos semelhantes preservados; duplicata confirmada rastreável |
| G15 | F2 usa TiposErros; K10 reúne outras origens; data do refugo e data do erro SAP são distintas | Nomear métrica específica, resolver D09; consolidado só após validar origens/unidades | E1–E4 / implementador e William | Resposta informa fonte/escopo/data e não se apresenta como K10 completo |
| G16 | F2 propõe só Fim; MEL-260 inclui Parcial; MEL-261 usa inspeções | Definir política de produção por etapa e granularidade | E1–E4 / implementador e revisor | Gabarito de Mandril, Trançagem e Extração separados |
| G17 | “Cancelada não conta” versus Manual_BO preserva Fim anterior | Distinguir produção por etapa, saída final e cancelamento; não zerar tudo | E1–E4 / William e revisor | D02 decidida por métrica e casos de cancelamento aprovados |
| G18 | Painel usa Created na inspeção; mapa também tem DataHoraInspecao | Confirmar data autoritativa e regra de fallback; não trocar silenciosamente | E1–E4 / William e revisor | D03 e teste de inspeção registrada após o fato |
| G19 | Receita mistura soma gravada e estimativa de janela sem apontamento | Separar real registrado de produção estimada do painel | E1–E4 / William e revisor | D04; mesma pergunta não alterna fórmulas entre canais |
| G20 | Refugo%, PPM e divergência são métricas diferentes | Numerador/denominador e sinais explícitos; zero denominador indisponível | E2–E4 / implementador | 10/(90+10)=10%; PPM usa boa SAP, sem substituição de base |
| G21 | field_11 pode ser déficit calculado; motivos mudaram; meta útil mudou | Classificar perdas por vigência e preservar origem do tempo; fator só onde autorizado | E1–E4 / revisor | Pausa, parada informada, déficit e excedido distintos; sem dupla dedução |
| G22 | SAP/packing são exports; vínculo por nome pode omitir material | Cobertura explícita, sinais 101/102, unidade M, alias validado e divergência por material | E4–E5 / implementador e William | Conciliação independente; sem compensação entre materiais |
| G23 | Lista proposta não tem versão, consistência ou tratamento retroativo | Controle de execução, publicação validada e reprocessamento histórico | E2–E4 / implementador | Falha não expõe carga pela metade; correção antiga aparece na revisão |
| G24 | Fluxo diário fica “depois”; não há SLA, custo, retenção ou dono | Dimensionar e definir operação antes de chamar F2 de concluída | E2–E4 / William, implementador e TI se necessário | D05–D06; execução recorrente, falha, recuperação e custo medidos |
| G25 | Receita 1 usa Parcial/HH como prova de fim; receita 4 troca OP | Revisar pré-condições e referências; impedir fechamento presumido ou vínculo quebrado | E5 / William e revisor | Receitas completas, teste negativo e efeito nas listas relacionadas conferidos |
| G26 | Log_Uiu previsto; agente “não cria”; sem atomicidade descrita | Exceção técnica restrita de auditoria, confirmação por proposta, guarda de versão e retomada | E5 / implementador e revisor | D07; falha de log, conflito, timeout e repetição tratados |
| G27 | Plano tem 40 perguntas; estudo tem 60 de escopos diferentes | Matriz de testes por entrega, gabarito independente e critérios críticos | Todas / implementador e revisor | Resultado por caso, denominador elegível e versão registrados |
| G28 | Teams já publicado; português posterior pendente | Republicar só delta validado; testar canal/identidade e rollback | E0/E3–E6 / implementador | Resposta pt-BR no Teams e versão anterior recuperável |
| G29 | Alertas “X h” sem política; OP velha pode ser dado velho | Definir limiar, frescor, deduplicação, resolução e único destinatário | E6 / William e implementador | D08; simulação evita alerta repetido ou falso por falha de carga |
| G30 | 50 propostas misturam estudo e backlog sem rastreabilidade | Vincular cada item a necessidade F0–F5, agrupar dependências e adiar expansão | Planejamento / implementador | Mapeamento abaixo, nenhuma funcionalidade só para completar 50 |

## Decisões de negócio/ambiente que o documento não pode inventar

| ID | Decisão pendente | Evidência a preparar antes de perguntar | Dono | Bloqueia | O que pode avançar |
|---|---|---|---|---|---|
| D01 | Data/hora efetiva da nova grade e tratamento da faixa 27–29/10 | Publicação/versões e exemplos de cada dia | William + revisor | Reclassificação histórica e comparações corrigidas nessa faixa | Consulta do gravado com aviso; dados de período inequivocamente conhecido |
| D02 | Efeito de cancelamento no indicador de cada etapa | Fim anterior, Parcial, descarte e inspeção de uma mesma ficha | William + revisor | Total que dependa do tratamento ambíguo | Refugo e consultas individuais sem alterar o histórico |
| D03 | Created ou DataHoraInspecao para o indicador da Extração; fallback permitido | Medida publicada e exemplos com datas diferentes | William + revisor | Produção por dia/turno da Extração | Demais etapas e consulta por OP |
| D04 | Valor registrado versus estimativa do painel para janela ausente | Fórmula vigente e casos com janela faltante/turno vazio | William + revisor | Equivalência declarada entre indicador Uiu e painel | Métrica explicitamente registrada, sem afirmar equivalência |
| D05 | Frequência de atualização, atraso tolerável e horário | Tempos/custo de uma carga com volume real | William | Agendamento e declaração de atualidade | Piloto manual com data de corte |
| D06 | Limites aceitáveis de custo, resposta/carga, retenção e destino operacional | Medições E2, política de TI e licença atual | William + TI quando necessário | Prontidão operacional/expansão de uso | Testes com acesso atual e quantidade controlada |
| D07 | Campos exatos de cada correção e exceção de criação do log | Proposta de receita, antes/depois e análise de impacto | William + revisor | Habilitar a respectiva ferramenta de escrita | Detetive e prévia sem escrita |
| D08 | Limiar, janela de repetição e política de resolução dos alertas | Incidentes simulados e amostra histórica | William | Envio recorrente no Teams | Avaliação local sem envio |
| D09 | Campo temporal do refugo, fallback para data vazia e regra de atribuição de produto ambíguo | Amostra de DataHoraRefugo/Created/OP e ficha da métrica vigente | William + revisor | Certificação do ranking temporal por produto em E3 | Extração bruta, testes sintéticos e total da fonte com limitações explícitas |

Decisão técnica que não altera regra nem escopo pode ser resolvida pelo implementador com evidência. Não pedir confirmação para cada arquivo do planejamento. Buscar primeiro as respostas no GMS; perguntar ao William apenas o que continuar ambíguo, com a amostra pronta. Nenhuma D01–D09 está marcada como respondida por esta revisão.

## Destinação das 50 propostas anteriores

Os números são os da mensagem anterior. Esta tabela cobre todos de 1 a 50; eles não são 50 entregas independentes.

| Propostas | Destinação no plano | Gaps relacionados |
|---|---|---|
| 1, 2, 3 | Parte da extração íntegra de E2 | G07, G23 |
| 4, 5 | Validação de consulta, sem fallback que muda a pergunta | G08 |
| 6, 7, 8, 9, 10 | Contrato de tipos, tempo, origem e falhas | G09, G10, G23 |
| 11, 12, 13 | Temporalidade com vigência e decisão histórica | G10, G11 |
| 14, 15, 16, 17 | Política de produção por fonte/etapa; não quatro projetos | G16, G18, G19 |
| 18 | Reformular: não excluir indiscriminadamente todo Fim de ficha cancelada | G17 |
| 19, 20 | Semântica de produção e espera versus parada | G16, G21 |
| 21, 22, 23, 24, 25 | Consultas F2; taxas somente com denominador compatível disponível | G15, G16, G20 |
| 26, 27, 28 | Meta e perdas segundo normas vigentes, sem criar OEE alternativo | G21 |
| 29, 30 | Comparação equivalente e diagnóstico; não prometer índice de gargalo sem K06 válido | G10, G19, G27 |
| 31, 32, 33, 34, 35, 36 | Conferência SAP do Detetive, com exports disponíveis; API nova fora | G12, G22 |
| 37, 38, 39, 40 | Integridade do processamento e publicação de agregados | G14, G23 |
| 41, 42, 43, 44 | Base ampliada de engenharia adiada; preservar consulta existente validada e não inventar spec | G30 |
| 45 | Diagnóstico com evidência; corrigir certezas indevidas das receitas atuais | G25 |
| 46 | Atualização do conhecimento existente, sem implantar plataforma documental nova | G03, G04 |
| 47 | Reformular: leitura agora; F3 autorizado conceitualmente continua com catálogo e controles | G02, G26 |
| 48, 49, 50 | Avaliação, versão e recuperação por entrega | G27, G28 |

## Conflitos que exigem cuidado ao atualizar o conhecimento

1. A instrução atual manda o documento vencer instruções: limitar essa precedência a regras de domínio. Conteúdo recuperado não muda permissões, ferramentas ou identidade do agente.
2. Uma OP sem apontamento posterior não prova etapa encerrada. Parcial registra produção com etapa ainda aberta. Alterar a receita 1 somente após a revisão, mantendo o histórico da mudança.
3. O guia SAP usa “uma linha por OP”, mas o mapa mais recente admite OP/lote. Não usar OP como chave primária da ficha.
4. A regra de análise de um lote antigo que inclui OP só-SAP “só se diminuir a divergência” não pode virar filtro genérico da conciliação. O universo completo vem antes das hipóteses de correção.
5. O mapa de listas orienta Top 50 para conversa. O processamento F2 tem contrato separado de extração completa e não herda esse teto como cobertura.
6. “Complete=true” deve provar término da extração, não ausência de erros semânticos. Completude, qualidade e atualidade são dimensões separadas.

Esses pontos são propostas de resolução de conflito, não emendas ao Mestre nem correções publicadas nas fontes de conhecimento.

## Evidência de leitura para D02–D04 (10/11/2026, só leitura)

Janela de 11/10 a 09/11/2026. Decisões continuam abertas; estas são propostas para o William escolher.

- **D02 (cancelamento):** Cobertura não é afetada (nenhum cancelado tem Fim de Cobertura). Cancelados no período: 16 de Mandril e 1 de Tubo. Caso real: OP 4207 tem Fim de Mandril com 1 m e depois Tubo cancelado. Proposta: Fim da etapa concluída conta como produção dela, mesmo se a OP for cancelada depois; Cancelado é só registro de descarte. Impacto no período: 1 m.
- **D03 (data da inspeção x Created):** afeta só a Extração. Dos cadastros feitos desde 11/10, 336 têm inspeção antes do cadastro. A diferença de 18.552 m vem de cadastro atrasado de inspeções anteriores a 11/10. Exemplo: inspeção de 27/10 às 22h30 cadastrada em 28/10. Proposta: DataHoraInspecao para dia e turno; Created só para auditoria; painel que usa Created declarado como diferente.
- **D04 (janela ausente):** Cobertura não aparece na lista Hora-Hora nesse período (células presentes: Spiral, TH01/02/03/05/06/07, TM01/04, TO04). Logo, a janela da Cobertura não tem fonte aqui e D04 não se aplica a ela por esta lista. Nas células presentes, há 1 linha com Real vazio em 3.600; real 0 é janela inteira parada. Proposta: real registrado sempre; janela sem apontamento vira "sem apontamento", nunca zero nem estimativa sem rótulo.
- **Pares Início/Fim:** só 1 OP de Cobertura tem Fim sem Início na janela (OP 4232, Fim em 03/11). As diferenças dia a dia vêm de OP que cruza a virada do dia.
