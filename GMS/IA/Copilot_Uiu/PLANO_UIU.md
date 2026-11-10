# Plano: Uiu vira o "William dentro do Copilot Studio"

> **Histórico do plano aprovado em 09/11/2026.** Para executar, começar pelo [PLANO_EXECUCAO_GMS.md](PLANO_EXECUCAO_GMS.md), que detalha F0–F5 e resolve lacunas de planejamento. O estado do Default, o caminho Knowledge nativo e algumas propostas técnicas abaixo foram superados pelos registros posteriores. As decisões de negócio aprovadas são preservadas; este texto não deve ser usado isoladamente como roteiro atual.

Data: 2026-11-09. Agente: Uiu (Copilot Studio, ambiente Default Danfoss). Situação hoje, vista no Studio:
- Orquestração generativa ligada, modelo GPT Chat Latest (Oct 2026), instruções com 4.595 de 8.000 caracteres.
- 60 ferramentas de SharePoint; as de criar e apagar estão desligadas e as de listar, ligadas. Nenhuma fonte de conhecimento.
- Desligados: Code interpreter (premium), Deep reasoning (premium), upload de arquivo, busca na web.
- Gatilhos bloqueados pela DLP "Allow default connectors - Danfoss Default". Então não dá para o Uiu agir sozinho por evento; o alerta tem que vir de um fluxo do Power Automate.
- O limite que ele mesmo declara ("não somo centenas de linhas") é o que mais o separa de você.

## Arquitetura alvo
O Uiu passa a ser um orquestrador com 4 agentes-filho, cada um com instruções próprias, assim nenhum estoura os 8.000 caracteres:
1. **Consulta**: OP, etapa, turno, Hora-Hora, paradas. Só leitura, com os nomes internos das colunas.
2. **Detetive de B.O.**: roda os mesmos diagnósticos que você faz, cada um com uma receita escrita (sintoma, consulta, como confirmar, causa provável, correção).
3. **Mecânico**: faz as correções do catálogo. Só escreve depois de mostrar o antes e o depois e receber "sim" no chat (o Studio pede confirmação antes de cada ferramenta). Cada correção grava uma linha numa lista nova, `Log_Uiu` (quem, quando, item, antes, depois).
4. **Professor**: explica norma, KPI, DAX e regras (turno, parada x pausa, setup, PPM, meta 21h45) a partir dos documentos.

## Fases
**F0: Conhecimento (o "cérebro William")**
- Montar o pacote de conhecimento em `GMS/IA/Copilot_Uiu/conhecimento/`: Mestre (Parte 0, C e B resumidos), Mestre_BI (KPIs K01–K17), Lições, glossário, memória aprovada da IA local, roteiro da Hora-Hora, COMO_USAR_OS_DADOS, normas recentes do Diário e o mapa das listas com os nomes internos.
- Escrever o arquivo novo `Manual_BO.md`: o seu jeito de achar problema, em receitas. Exemplos: OP travada na etapa, turno T2 que devia ser T3 (janela 22:20–22:40, de 05/10 a 27/10), mangueira GMS sem match no SAP (ligar pela OP, nunca zerar), divergência GMS x MB51, Hora-Hora sem apontamento, carretel duplicado, evento Cancelado contado como produção.
- Subir os arquivos no Knowledge do Uiu. Isso é upload, então peço o seu "sim" antes.

**F1: Instruções e agentes-filho**
- Reescrever as instruções do orquestrador e criar os 4 filhos. Os textos ficam versionados aqui (`instrucoes/*.md`) e eu colo no Studio só com o seu "sim".

**F2: Contas de verdade (tirar o "não somo")**
- Ligar o Code interpreter para ele somar e cruzar listas inteiras. É premium, então quem decide é você.
- Criar um fluxo `GMS_Uiu_Agregados` no Power Automate que entrega os totais prontos (produção, parada e refugo por dia, turno e máquina). O Uiu chama esse fluxo como ferramenta.

**F3: Correções com trava**
- Catálogo inicial: corrigir turno, trocar OP pela do SAP na ficha só-SAP (regra de 15/10), fechar etapa esquecida e reclassificar motivo de parada.
- Ligar só as ferramentas de **atualizar** desses itens, com "pedir confirmação ao usuário" ativado. Criar e apagar continuam desligados.
- Revisão obrigatória pelo `revisor` (Opus), porque mexe em turno e em cálculo de parada.

**F4: Prova (ele entende no seu nível?)**
- Bateria de 40 perguntas com resposta esperada, tiradas de `IA/treino/bateria_20.md` mais casos reais de B.O. Roda na avaliação do Studio, e a meta é acertar pelo menos 90%. O que errar volta para F0/F1.

**F5: Alerta e canal**
- Fluxo agendado que roda o Detetive (OP parada há mais de X h, divergência nova) e manda o resumo no Teams.
- Publicar no Teams. Isso é publicação, então peço o seu "sim".

## Time e custo
- F0–F1: chefe (Sonnet) monta o pacote e o `Manual_BO`; `revisor` (Opus) confere as receitas que têm turno e parada.
- F2–F3: `executor` (Sonnet) faz os fluxos e as instruções; `revisor` (Opus) aprova as correções antes de ligar.
- F4: chefe roda a bateria no Studio pelo navegador.
- Sugestão: fazer a execução em sessão nova, a partir deste plano, como nas outras demandas grandes.

## Decisões do William (09/11/2026) — plano APROVADO
1. Mecânico escreve no SharePoint, só no catálogo, com confirmação a cada correção e log no `Log_Uiu`.
2. Usuário: só o William por enquanto. F5 publica no Teams apenas para ele (sem compartilhar com supervisores).
3. Ligar Code interpreter e Deep reasoning (premium). Ligar no Studio ainda pede o "sim" na hora.
4. Execução em sessão nova a partir deste arquivo, começando pela F0.
