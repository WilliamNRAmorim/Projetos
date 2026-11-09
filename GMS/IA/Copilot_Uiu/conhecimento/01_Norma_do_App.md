# Norma do App GMS (resumo para o Uiu)

Fonte: GMS_Mestre.md v2.0 (resumo para o Uiu, gerado em 09/11/2026). Linhas NORMA do diário mais novas valem mais que este resumo (ver 08_Normas_Diario.md).

O GMS (Guaratinguetá Manufacturing System) é um MES híbrido em Power Apps Canvas + SharePoint + Power Automate + Power BI, em produção na Danfoss Guaratinguetá. Legenda de horizonte dos conceitos: H1 = dá para fazer agora com o que existe; H2 = depende da Frente 2 (dados consolidados) ou do token Factbird; H3 = visão, depende de H1+H2 maduros. Marcação ★ = conceito raro em MES.

---

## Parte 0. Protocolo de trabalho (como responder)

- P1. A norma do Mestre é a fonte de verdade. Linhas NORMA do diário posteriores à última consolidação também valem e valem mais que o Mestre em caso de conflito (são mais novas). Precedência: 1º linhas NORMA recentes do diário, 2º Mestre (Partes 0, A, B, C), 3º Mestre BI (modelo semântico, DAX, relatórios).
- P2. Melhoria vence conservadorismo: mudança de estrutura é bem-vinda quando há evidência (auditoria, doc oficial ou dado do próprio GMS) e respeita a migração progressiva.
- P3. Ao sugerir mudança no app: patch cirúrgico, nunca rewrite; uma única melhor solução, não cardápio. Quem edita o app é o William.
- P4. Em caso de dúvida, fazer uma única pergunta diagnóstica, não três hipóteses.
- P5. Toda tela nova nasce dos Templates (B §6) e dos tokens de design (B §5.2); tela tocada converge para eles.
- P6. Emendas não reescrevem o Mestre: viram linha no diário (formato DATA | TIPO | ALVO | VER | REF | TEXTO). A linha NORMA vale desde que é escrita; o Mestre a absorve depois, em lote.
- P7. Prioridade de raciocínio, nunca invertida: 1º confiabilidade do dado (números que batem), 2º esforço do operador, 3º poder de decisão da supervisão, 4º estética.
- P8. Frente 1 (mapeamento e padronização) concluída; Frente 2 (consolidação das cerca de 28 fontes) estava aguardando insumos (fluxos do Power Automate e contagem de linhas). Para o estado atual, consultar o diário, não este resumo.
- P9. Pendências e insumos vivem no diário (linhas PENDÊNCIA e RESOLVIDO com o mesmo REF), nunca dentro do Mestre.
- P10. Todo ciclo de trabalho termina em linhas de diário, uma por fato (entrega, lição, norma, melhoria, pendência).
- P11. Antes de responder sobre norma, conferir este resumo e o 08_Normas_Diario.md (as linhas mais novas mandam).

Para quem responde perguntas: se a resposta depende de "o que está vigente", priorize linhas NORMA recentes do diário; backlog, estado e próximo MEL não estão no Mestre, saem do diário. Nunca inventar ID: sem ID real, dizer que não há.

## Parte A, em breve

- GMS é mudança cultural, não ferramenta: decisão sai do feeling e entra no dado; informação deixa de morar em papel e planilha; o operador deixa de ser digitador e vira sensor do processo; o supervisor deixa de compilar o passado e decide o presente.
- Taxonomia: núcleo de MES/MOM, mais APS (sequenciamento, pegging, what-if), SCADA (supervisão, historian), LIMS (especificação vs. medido, custódia, certificado), Lean/TPM (Andon, SQDC, TOC, skill matrix, passagem de turno) e IA nativa/agentes (C30 a C34).
- Tese: MES tradicional registra o passado; o GMS enxerga o presente e antecipa o futuro com os dados que já coleta, em Power Platform, mantido por quem entende o processo.
- Quatro pilares, na ordem do P7: verdade única, esforço zero desnecessário, supervisão por exceção, memória de processo.
- Três apostas diferenciais: derivação em vez de digitação; decisão empurrada (Andon, Health Score, Radar de Gargalo); memória operacional (passagem de turno, voz do operador, genealogia QR).

---

## Parte C. Catálogo de conceitos (C1 a C40)

### Supervisão que decide
- C1. Andon Digital, feed de exceções (H1). Feed único no Painel de Supervisão, ordenado por criticidade (OP parada além do teto, refugo acima do limite, máquina parada recorrente, SPC fora de controle, composto vencendo); cada card traz 1 exceção e 1 ação sugerida. Coleção `colExcecoes` montada no OnVisible; zero tabela nova.
- C2. ★ OP Health Score (H1). Nota 0 a 100 por OP ativa, de 4 fatores: idade na etapa vs. lead time médio, refugo vs. tolerância, risco de validade de composto, nº de retrabalhos/edições. UDF `fx_HealthScore(op)`; H1 usa média fixa por etapa, H2 média móvel real.
- C3. ★ Radar de Gargalo Dinâmico, TOC (H1 para H2). Aponta a restrição do dia: etapa com maior WIP e menor vazão recente. H1 = WIP por etapa / vazão do dia por `data_hora_final_<etapa>`; H2 refinado com tempos de ciclo do Factbird.
- C4. Previsão de Conclusão, ETA por OP (H2). Data/hora prevista por lead time médio das etapas restantes (por família); lista de OPs em risco quando ETA > necessidade. Depende de dados limpos pós-Frente 2; `fx_ETA(op)`.
- C5. SPC ao Vivo na Inspeção (H1). Carta Xbar-R sobre Ø interno/externo/concentricidade que a Finalização já captura, com regras de Nelson simplificadas (7 pontos subindo, ponto fora de 3 sigma). Objetivo: ajustar a máquina antes de refugar.
- C6. ★ Passagem de Turno Assistida (H1). Na virada, o sistema monta o resumo (OPs fechadas, travadas, paradas e motivos, refugo, pendências); quem sai confirma em 2 minutos; fica na lista `Passagem_Turno`. Usa `fx_TurnoAtual`/`fx_DataRef`.
- C7. Quadro Tier/SQDC Automático (H2). Quadro de reunião diária preenchido sozinho: Q = refugo do dia, E = aderência ao plano (C22), C = custo do refugo (C15); supervisor só adiciona S e ações.
- C8. ★ Simulador de Fila "E se?" (H3). Sandbox: arrasta uma OP para frente da fila e vê o impacto no ETA das outras; nenhuma escrita até confirmar. Coleção-espelho + recálculo de `fx_ETA` em memória.

### Chão de fábrica que flui
- C9. Sequenciamento Inteligente da Fila (H2). Fila ordenada por due date + minimização de troca de bitola (setup), não FIFO de chegada; pesos calibráveis em `ConfiguracaoGMS`.
- C10. Kanban Eletrônico de Carretéis (H1). Saldo vivo de carretéis por estado (vazio/em uso/cheio aguardando) e alerta de escassez por bitola; dados em `lista_carreteis` e `Historico_Carretel`.
- C11. FIFO Enforcement na Bobinadeira (H1). Enforcement suave: consumir fora de ordem exige motivo (dropdown) e o furo de FIFO vira métrica. Usa `FifoBobinadeira`.
- C12. ★ Matriz de Habilidades Viva (H2). `Colaboradores` x etapas x nível (treinando/apto/certificado/instrutor); dropdown de operador filtra por aptidão; painel mostra gaps.
- C13. Hora-Hora Automático em todos os processos (H1 para H2). Todo processo terá Hora-Hora via Template B parametrizado; Meta derivada de takt/velocidade (`colVelocidadeProducao`), Real derivado dos patches da ficha por janela horária; operador só confirma paradas e motivos. Mata a digitação dupla e a divergência ficha x hora-hora.
- C14. ★ Voz do Operador (H1). Botão "Reportar problema" em toda tela: texto + foto opcional, vira card no feed do supervisor (C1) com tela/OP/máquina anexadas.
- C35. ★ Bipe Universal (H1). Todo campo preenchido a partir de etiqueta ou crachá ganha `BarcodeReader` inline (OP, crachá, lote de composto, carretel, QR de genealogia). Padrão do Montagem; regras em B §3.9. Nenhuma tabela nova.
- C36. ★ Sinóptico Vivo da Planta (H1 para H2). Planta real de fundo com uma baliza por máquina/etapa (em processo, fila, livre) lendo `colEstadoProcessos` por timer somente-leitura; posições em `fx_LayoutBalizas`. Responde ONDE (complementa o Andon, que responde QUAL). Lição: em AddColumns, LookUp/Filter aninhado resolve ThisRecord no escopo interno e nome de coluna entre aspas vira texto (ver B §3.13).

### Dados que se defendem sozinhos
- C15. Custo da Qualidade em R$ (H1). Metros de refugo x custo padrão por família = R$ por dia/semana/mês, com Pareto por causa.
- C16. Pareto Vivo de Refugo (H1). Pareto automático por causa/máquina/turno/mangueira dentro do app; fonte `TiposErros`.
- C17. ★ Guardião de Apontamento (H1). Validação estatística no Patch: quantidade fora do perfil histórico da mangueira/etapa pede confirmação explícita; confirmações auditáveis. Protege o pilar 1.
- C18. Validade de Composto Proativa (H1). Campos de validade de Tubo/Cobertura alimentam alerta no Andon antes do uso.
- C19. MTBF/MTTR por Máquina (H2). Derivado dos motivos de parada do Hora-Hora; ranking de máquinas para manutenção.
- C20. Integração Factbird, IoT (H2, piloto desenhado). Webhook Factbird para Power Automate, campos `inicio_sensor`/`fim_sensor` na ficha para validar antes de aposentar o apontamento manual. Estado registrado no Mestre: bloqueado no token da API. (Verificar o diário para o estado atual.)
- C21. Genealogia QR, Certidão da OP (H1). A ficha impressa carrega QR Code 128 (implementação offline, 4 UDFs) que abre a ConsultaOP da OP: quem fez, quando, com que lote, com que resultado.
- C22. Aderência ao Plano (H2). % de OPs concluídas na data planejada, por semana/família; é o "E" do SQDC (C7).

### Sabores das disciplinas vizinhas
- C23. ★ Cadeia Interna Sincronizada (H1 para H2). Upstream enxerga o downstream: Tubo vê as trançadeiras (fila, velocidade, consumo via fluxo "Monitor"); Mandril vê estoque da bitola em processo no Tubo e o que a Trançagem vai puxar. Produzir o que o próximo processo vai consumir.
- C24. Planejamento de Máquina Simples + Alertas Reconciliados (H1). Lista `Plano_Maquina` (trançadeira, turno, OPs previstas); alerta só dispara se o plano ainda tiver produção pendente dependente; plano completo suprime o alerta (evita falso positivo no Andon).
- C25. ★ Diário de Bordo por Processo, Historian (H1). Histórico navegável por Dia e Turno e Processo ("o que aconteceu no Tubo no 2º turno de ontem"); usa `fx_DataRef` (respeita a virada 05:20). Alimenta a Passagem de Turno (C6) e vice-versa.
- C26. Delineamento Vivo (H1 para H2). Especificação de engenharia (picks, diâmetros nominais, fita, composto) ao lado de cada campo; entrada fora da spec ganha aviso (poka-yoke); H2 valida spec x medido automaticamente.
- C27. Custódia de Carretel (H1). Transferência de carretel entre processos tem confirmação de recebimento (1 toque); até confirmar fica "em trânsito" no kanban (C10).
- C28. Certificado de Qualidade por OP, LIMS-lite (H2). Ao finalizar a OP monta o certificado (medições de `RegistrosInspeção`, lotes, operadores, resultado vs. spec C26) em PDF com QR (C21).
- C29. Power Automate como Camada de Cálculo (H1, arquitetural). Cálculos pesados e agregações saem do Power Fx da tela e vão para fluxos agendados que gravam em lista de resultados (`Resultados_Calculados` ou similar); o app lê resultado pronto com filtro delegável. Expande o fluxo "Monitor".
- C39. ★ Etapa em Batelada (H1). Etapa que não produz metragem (Vulcanização é o caso puro): operador não aponta quantidade nem se identifica por OP, aciona transições físicas (carregar, resfriar, descarregar) e o sistema mede o resto. Estado é função pura (B §3.10); um único botão derivado do estado; quantidade herdada da etapa anterior e exibida com a origem; operador informado uma vez por lote, no descarregamento; resfriamento é pré-requisito de fluxo. Aplica-se também a Post-Cure e fornos/estufas; Debandagem e Extração/Teste devem ser reavaliadas.

### Fronteira 2026: IA e agentes
- C30. Copiloto do GMS, pergunte à fábrica (H2). Linguagem natural no Painel de Supervisão sobre dados reais; pós-migração Dataverse (MEL-049), com RAG nativo do Prompt Builder. Em SharePoint isso não existe.
- C31. ★ Agente Autônomo de Supervisão (H3). Agente do Copilot Studio vigia e age dentro de limites (notifica no Teams OP estagnada, abre registro em refugo anômalo, aciona Extrusora em falta prevista reconciliada com o plano C24); humano aprova ações críticas.
- C32. Funções de IA no fluxo de dados (H2). AIClassify (observações livres para categoria, alimenta o Pareto C16), AISummarize (rascunho da Passagem de Turno C6), AIExtract (lote/máquina/medida de texto livre para campos). Exige licença AI Builder + Dataverse.
- C33. Visão Computacional na Inspeção (H3). Foto do defeito (câmera da Voz do Operador C14) classificada por modelo do AI Builder; degrau acima do SPC.
- C34. Offline-First (H1 para H2). H1 (SharePoint): Patch que falha grava em coleção persistida com `SaveData()` e um sincronizador reenvia quando `Connection.Connected` volta. H2 (Dataverse): offline nativo; SharePoint não é suportado pelo offline moderno.

### Execução multi-recurso e estrutura de fluxo
- C37. ★ Posto de Trabalho como Entidade de Estado (H1). Em etapa com mais de um recurso físico, o estado pertence ao posto, nunca à tela: uma tela abre N raias, uma por máquina, cada uma com OP, cronômetro e ação. Coluna de posto na `ficha_producao` (Mandril: `maquina_mandril`, indexada, MEL-012); coleção chaveada por posto (`colPostosMandril`) substitui variáveis de estado único; seleção do posto no menu de navegação (`scr_selecaosetor_1`, `varPostoAtivo`). Instância: Mandril, postos TERMOFUSAO e VIBRACIONAL; rollout previsto para Trançagem. Motivo: com um estado por tela, o segundo operador fechava a OP do primeiro antes da hora, corrompendo tempo de ciclo (invalida C3, C13, C19). Cutover marco zero, sem backfill. Consequência: Hora-Hora soma duas máquinas na mesma meta (MEL-033/035).
- C38. ★ Split de Lote por Sobra (H1). Quando sobra material do carretel, a ficha se divide: pai corrigido ao consumido, filho com a sobra herda campos de origem e reentra na fila com o mesmo carretel. Campo `ficha_pai` guarda o ID do registro de origem (nunca o número da OP); não é requisito operacional, serve à genealogia (C21/C28). Instância: tela do Tubo.
- C40. ★ Grafo de Fluxo e Genealogia (H1 para H2). Tabela de arestas, não banco de grafo. Ganhos: (1) matar o fluxo hardcoded, tornando `fFluxoEtapas` autoritativa (etapa_origem para etapa_destino + condição) para as telas lerem o próximo passo; pré-requisito do Template B parametrizado (C13/MEL-035); (2) tabela `Genealogia` (`no_origem, tipo_origem, no_destino, tipo_destino, relacao, data`) para recall N:N; (3) gargalo calculado (C3, C23; MEL-039 e MEL-050 são a mesma lógica). A `ficha_producao` continua linear. Restrição: Power Fx não tem recursão; travessia vai em Power Automate (C29) ou DAX com PATH()/PATHCONTAINS.

### Mapa de dependências
- Fundação (Parte B: fx_TurnoAtual, fx_DataRef, tokens, dado que bate) sustenta tudo. C1 Andon alimenta C6; C14 alimenta C1; C35 reforça C13, C18, C21, C27.
- C2 Health Score leva a C4 ETA (e C8 Simulador) e a C3 Radar de Gargalo. C13 Hora-Hora leva a C19 MTBF/MTTR e C22 Aderência.
- Frente 2 desbloqueia C4, C7, C9, C12, C19, C22, C28. Factbird (token) turbina C3, C4, C13, C19, C20. Fluxo Monitor alimenta C23, C24, C29.
- C25 Diário de Bordo e C6 Passagem de Turno se alimentam. C26 Delineamento alimenta C28 Certificado. C36 Sinóptico e C1 Andon se complementam (ONDE x O QUÊ).
- C37 Posto é pré-requisito de tempo de ciclo honesto (C3, C13, C19). C38 Split alimenta C21/C28 e consome C27. C39 Batelada alimenta C25. C40 Grafo: `fFluxoEtapas` para C13/C35, Genealogia para C21/C28, arestas para C3/C23.
- Dataverse (MEL-049) desbloqueia C30, C32 e o offline nativo de C34. C31 Agente consome C1 + C24 + C29.

---

## Parte B. Padrões técnicos (normas). Legenda: ⛔ bloqueante para tela nova; ⚠️ migração progressiva (aplicar ao tocar a tela)

### 1. Nomenclatura
- ⛔ §1.1 Todo controle novo usa prefixo de tipo + propósito em camelCase: scr_ (tela), gal_ (galeria), frm_ (form), ctn_ (container/modal), btn_ (botão), ico_ (ícone clicável), rct_ (retângulo), lbl_ (label), tmr_ (timer), cmb_ (dropdown/combobox), inp_ (TextInput), spr_ (spinner), html_ (HtmlViewer), dc_ (DataCard), bcr_ (BarcodeReader); complementos chk_, tgl_, dte_, img_, cmp_. Controle com nome auto-gerado (Gallery4_9, Rectangle11) torna o App Checker ilegível.
- ⛔ §1.2 Variável com escopo no nome: gbl (global, Set), ctx (local da tela, UpdateContext), col (coleção, ClearCollect), fx_ (Named Formula/UDF no App.Formulas). Preferir ctx a menos que o valor cruze telas.
- ⚠️ §1.3 Renomeação progressiva: não renomear em massa; tocou a tela, renomeia os controles envolvidos. Validação de nome duplicado (PA1001) continua obrigatória antes de import de YAML.

### 2. Estrutura e fontes de dados
- ⛔ §2.1 Reduzir fontes conectadas (26 reais + 5 SampleData de template a remover); nenhuma lista nova sem checar se uma existente resolve.
- ⛔ §2.2 Excel Online como fonte viva é proibido para dado transacional: DM_MANDREL, DM_BANDAGEM e DM_LAYLINE ficam só como tabela de domínio, apenas leitura, até a Frente 2; nenhuma fonte Excel nova; nenhum Patch em Excel.
- ⛔ §2.3 Proibida referência cruzada entre telas (controle da tela A lido pela tela B); passar valor por variável ou coleção. O App Checker acusou 7 acoplamentos.

### 3. Padrões de código Power Fx
- ⛔ §3.1 Quando a lógica depende do dado carregado, usar `ClearCollect` (awaitable); `UpdateContext` nunca espera a leitura do SharePoint (causou perda de dados na `scrHoraHora_Trancagem`).
- ⛔ §3.2 App.Formulas (Named Formulas) para constantes e derivações puras; OnStart enxuto. Função volátil (`Now()`, `Today()`) dentro de Named Formula é PROIBIDA: congela no primeiro cálculo da sessão. Lógica dependente do tempo vira UDF com o instante como parâmetro (`fx_Turno(minutosDoDia)`, `fx_DataRefDe(minutosDoDia)`); quem chama fornece o instante (`Now()` capturado uma vez num `With` em bloco de ação, ou relógio de tela). Fronteiras de turno: o exemplo do Mestre (T1 320–827, T2 828–1360) está REVOGADO. Vigente pela NORMA de 27/10/2026 (MEL-250): T1 05:20–13:56 (320–836), T2 13:57–22:19 (837–1339), T3 22:20–05:19 (1340–319). Débito aberto: `fx_TurnoAtual`, `fx_TurnoAtualLabel`, `fx_DataRef`, `fx_JanelaInicio`, `fx_JanelaFim` ainda têm volátil (MEL-075); `fx_UltimoIdFicha` faz `Sort()` completo sem delegação e `fx_ConsultaOP_Padrao` depende dele (MEL-076). Se o diário registrar que isso foi resolvido, ele vale mais.
- ⛔ §3.3 Data/hora nunca se compara com número (classe `Now() >= 6`, 20 ocorrências na auditoria; causa raiz de totais e eficiência que não batem na virada de turno/dia). Usar minutos do dia (`Hour(Now())*60+Minute(Now())`) ou as fx_ de turno. Nunca filtrar por `Modified` (OP que avança de etapa atualiza `Modified` e some do histórico); usar o `data_hora_final_<etapa>` da própria etapa.
- ⛔ §3.4 Timers são somente-leitura: Timer de 3000 a 5000 ms, Repeat, AutoStart, com Refresh/LookUp no OnTimerEnd; nunca executa Patch (condição de corrida com a digitação do operador).
- ⚠️ §3.5 Usar `Concurrent()` para cargas independentes na entrada da tela.
- ⚠️ §3.6 Anti-padrão N+1: LookUp em fonte externa dentro de item de galeria gera uma chamada por linha; resolver o join antes com `AddColumns` sobre coleção.
- ⚠️ §3.7 Todo Patch/SubmitForm de produção ganha `IfError` com `Notify`; sem isso, falha de rede perde o apontamento em silêncio.
- ⛔ §3.8 Regras de YAML: valor com `: ` ou fórmula com chaves de registro vai em bloco `|-` com prefixo `=` (mesmo as curtas); só versões de controle provadas (lista vigente no Mestre); import de YAML em nível de tela cria tela duplicada (reforma = tela nova com nomes novos, redireciona Navigate, exclui a antiga); bateria de QA de YAML obrigatória antes de entregar (feita fora do Uiu).
- ⛔ §3.9 `BarcodeReader@1.0.25`: não aceita Color/Fill; `Self` não resolve no OnScan (usar o nome); a saída é `Barcodes` (tabela), extrair com `Text(First(bcr_xxx.Barcodes).Value)`; valor alimenta o input via `Default: =ctxBipeX`; limpar os ctx de bipe no fechamento do fluxo; câmera só funciona no Power Apps Mobile/tablet (não no preview do Studio nem no desktop); preferir `BarcodeType.Code128` quando o código é sempre Code 128.
- ⛔ §3.10 Estado de etapa é função pura, nunca variável: calculado dos campos gravados por UDF (ex.: `fx_EstadoVulca(status, inicioResf, agora)` devolve AGUARDANDO, VULCANIZANDO ou RESFRIANDO). Poka-yoke nunca depende só de `Visible`/`DisplayMode`: a coleção que alimenta a ação não pode conter o registro inelegível. Proibido derivar lógica do texto de um label ou comparar DisplayMode/Visible de outro controle.
- ⛔ §3.11 Relógio de tela: `Now()` só em bloco de ação (OnSelect/OnVisible/OnTimerEnd); propriedade de exibição consome `ctxAgora`, atualizado por um timer (30 s para cronômetro em minutos, 1 s só se exibe segundos).
- ⚠️ §3.12 `Form`/`TypedDataCard` são legado (bug "No item to display", DisplayName do schema); tela nova usa controles diretos (inp_, cmb_) com Patch e verificação de `Errors()`.
- ⛔ §3.13 Escopo aninhado usa `As` (`ForAll(colX As _x, ...)`); nome de coluna nunca entre aspas (vira literal de texto, comparação sempre falsa). Ambos falham em silêncio, então a validação é numérica, contra o CSV export.

### 4. Dados e delegação (SharePoint)
- Contexto: `ficha_producao` tem cerca de 1.176 linhas x 103 colunas (números da auditoria) e cresce todo dia; a auditoria acusou 177 avisos de delegação (focos: Trançagem 34, Tubo 34, Cobertura 27, Supervisão 20, Finalização 11).
- Risco central: consulta não delegável traz só os primeiros 500 registros (limite configurável até 2.000) e ignora o resto em silêncio; o número parcial parece completo. É uma causa clássica de total que não bate.
- ⛔ Data row limit em 2.000 nas configurações do app (mitigação, não solução).
- ⛔ Filtro delegável primeiro, refinamento depois: `Filter(ficha_producao, processo = "Tubo")` roda no servidor; Search, `in` e data complexa aplicam-se depois, sobre a coleção local.
- ⛔ Colunas de filtro indexadas no SharePoint (`processo`, `status_processo`, `OP` e os `data_hora_final_*` mais consultados; até 20 índices por lista). Sem índice, Filter/LookUp param de avaliar além do item 5.000 (limite de exibição de lista).
- ⚠️ Preferir tipos delegáveis no schema (texto simples, número, data); Choice só delega com `=`; Lookup gera chamadas extras; evitar Choice/Lookup/Person em coluna filtrada.
- ⚠️ `StartsWith` no lugar de `Search` para busca digitada (ConsultaOP).
- Estrutural: a solução da causa é consolidar fontes (Frente 2) e, no horizonte, Dataverse, que delega mais operadores. Para diagnosticar total que não bate, suspeitar primeiro de delegação (500/2000/5000), filtro por `Modified` ou comparação data x número.

### 5. Design system
- ⛔ §5.1 O padrão Montagem é o canônico (único sem vazamento de nome de coluna, bipe-first, hierarquia limpa).
- ⛔ §5.2 Tokens `fx_` em App.Formulas; proibido hardcode de cor/tamanho/raio. Famílias: cores (CorPrimaria = vermelho Danfoss só para marca/alerta máximo, não para botão de ação; CorInfo para ação primária; Fundo, Superficie, Texto, TextoSuave, OK, Alerta, Erro, Info e tons Suave, Header, Borda, Rotulo, Gelo), tamanhos de fonte (`fx_Fonte*` é TAMANHO; família é `fx_FonteFamilia`), espaços (EspacoS/M/L) e raios (Raio, RaioS, RaioG). Layout do sinóptico em `fx_BalizaTam`/`fx_LayoutBalizas`. Valores exatos: ver o Mestre.
- ⛔ §5.3 Rótulo limpo em PT-BR; nome interno de coluna (ex.: `operador_vulcanizacao`) nunca aparece para o operador.
- ⛔ §5.4 Alvos de toque: botão de ação primária com altura mínima 48 px e área de toque 48x48; em telefone 56 px; espaçamento mínimo `fx_EspacoM`; dropdown acima de 7 itens vira bipe ou busca; `AccessibleLabel` em todo input.
- ⛔ §5.5 Contraste texto/fundo mínimo 4.5:1 (WCAG AA); desabilitado usa `fx_CorTextoSuave` sobre `fx_CorSuperficie`, nunca cinza sobre cinza.
- ⛔ §5.6 Datas e números em padrão BR único: `dd/mm/yyyy` (e `dd/mm/yyyy hh:mm` com hora), vírgula decimal; proibido default fantasma `12/31/2001` em DatePicker (default é Blank() com validação, ou `fx_DataRef`).
- ⛔ §5.7 Estados visuais: Em processo (selecionado) = CorPrimaria fundo com texto branco; Aguardando = CorAlerta; Concluído/OK = CorOK; Erro/refugo = CorErro; Informativo e botão de ação primária = CorInfo; Processo físico em curso (resfriamento, cura, repouso) = CorGelo sobre CorGeloSuave. Cronômetro de card acima de 24 h exibe "+24 h" com badge de alerta (evita o sintoma "4162:41" da OP zumbi).
- ⛔ §5.8 Ícone sobre botão: o OnSelect do ícone é exclusivamente `Select(btn_Alvo)`, nunca cópia da lógica (caso Vulcanização v0.1.3: o modal de set-up nunca abria).
- ⛔ §5.9 Densidade: modal/card com menos de cerca de 60% da área ocupada deve ser redimensionado ao conteúdo; espaço vazio é bug de layout.

### 6. Templates de tela (uma linha cada)
- Template A, Ficha de Etapa: fila (esquerda, só leitura) + ficha (centro: dados da ordem e entrada) + lateral; botões Iniciar, Salvar, Enviar em máquina de estados; Enviar com confirmação ao finalizar etapa.
- Template A′, etapa em batelada (C39): zero campo de entrada, um único botão derivado do estado, stepper de 3 fases, quantidade herdada, operador só no fechamento do lote; referência `scr_Vulcanizacao_2`.
- Template B, Hora-Hora: duas colunas Produção | Paradas, Meta e Real derivados, uma tela parametrizada por célula (como a Montagem, com 13 células).
- Template C, Registro Rápido: formulário (máx. 7 campos) à esquerda, registros do dia à direita, botão único Registrar.
- Template D, Mobile (só tela nova): cabeçalho fixo, corpo com no máximo 5 campos, rodapé com uma ação; navegação por bipe (C35 sobre C40). Apontamento mobile não deve ser liberado antes da fila offline (MEL-057, C34).

### 7. Qualidade e governança
- ⛔ §7.1 Tela nova publica com zero erro de tipo e zero referência cruzada no App Checker.
- ⛔ §7.2 Checklist pré-publicação: PA1001; App Checker; teste de virada de turno (05:19/05:21 e 15:19/15:21); teste offline curto (IfError notifica); validação contra CSV export; QA de YAML verde; teste de barreira dupla (restrição na coleção, não só em DisplayMode/Visible); teste de ícone sobreposto; teste de sessão longa (mais de 1 h atravessando virada de turno, caça Named Formula volátil).
- ⚠️ §7.3 Higiene contínua: remover variáveis mortas da tela tocada (83 mapeadas), mídia órfã e as 5 fontes Sample.
- ⚠️ §7.4 Git Integration (GA desde abril/2025) como ALM oficial; o fluxo manual (export YAML, validação, import) segue válido até a ativação.
- §7.5 Monitor (Power Apps Studio) é a ferramenta padrão para investigar lentidão; usar antes de culpar o SharePoint.

---

## Pistas rápidas para diagnóstico de dado que não bate
- Total parcial ou faltando linhas: delegação (limites 500, 2000, 5000) em `ficha_producao`; confira se o filtro é delegável e a coluna é indexada.
- Registro some do histórico: filtro por `Modified` em vez de `data_hora_final_<etapa>`.
- Turno ou data de referência errados na virada, ou tablet aberto muito tempo: Named Formula volátil congelada (MEL-075) ou comparação de data com número.
- Número renderiza mas vem errado em tela com AddColumns/ForAll: escopo aninhado sem `As` ou nome de coluna entre aspas.
- Apontamento ausente após queda de rede: Patch sem IfError (§3.7), sem fila offline (C34).
- Tempo de ciclo corrompido em etapa com duas máquinas: estado por tela em vez de por posto (C37).
- Ação irreversível feita sem pré-requisito: barreira só em Visible/DisplayMode (§3.10).
