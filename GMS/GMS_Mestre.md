# GMS — DOCUMENTO MESTRE
### Constituição do Guaratinguetá Manufacturing System
**Versão 2.0 · 17/08/2026 · norma estável**

> **Este arquivo é só a NORMA.** Ele muda pouco e só por emenda. O progresso do dia a dia **não entra aqui** — vai para o `GMS_Diario.md`, que é append-only.
>
> **Os três arquivos do projeto:**
>
> | Arquivo | O que é | Com que frequência muda |
> |---|---|---|
> | `GMS_Mestre.md` (este) | protocolo, visão, padrões técnicos, catálogo de conceitos | raro — só consolidação em lote |
> | `GMS_Diario.md` | uma linha por fato: entrega, decisão, lição, pendência, melhoria nova | toda conversa, sempre no fim |
> | `gms.py` | gera backlog, estado, próximo ID, pendências a partir do diário | nunca (é ferramenta) |
>
> **Por que assim:** manter backlog e changelog dentro do Mestre obrigava a reescrever o documento inteiro para registrar uma linha. Backlog, estado e histórico agora são **derivados** do diário — não se mantêm à mão.
>
> **Base factual:** auditoria do `.msapp` v2026-06-22 (25 telas, 26 fontes, App Checker 2.854 apontamentos), 20 screenshots de produção, mapa de navegação (`GMS_Mapa_Navegacao.pdf`) e mapeamento de telas (`GMS_Frente1_Mapeamento_Telas.md`).
> **Base normativa:** Microsoft Learn (Power Apps), coding standards da comunidade (Matthew Devaney 2024, white paper oficial Microsoft, Practical Power Apps) e as lições validadas em produção no próprio GMS.

---

# PARTE 0 — PROTOCOLO DE TRABALHO (Claude, leia isto primeiro)

Estas regras valem para **toda conversa deste projeto**, independente de quanto tempo passou:

**P1. A norma deste arquivo é a fonte de verdade.** Toda sugestão, código ou decisão deve ser coerente com as Partes A, B e C. Se uma conversa contradisser o documento, o documento vence — a menos que a conversa o emende explicitamente (ver P6). Linhas `NORMA` do `GMS_Diario.md` posteriores à última consolidação **também valem**, e valem mais que este arquivo quando houver conflito (são mais novas).

**P2. Melhoria vence conservadorismo.** O objetivo declarado do projeto é fazer do GMS o melhor MES possível. Mudança de estrutura, de lógica ou de arquitetura é **permitida e bem-vinda** quando comprovadamente melhora o sistema — desde que citando a evidência (auditoria, doc oficial, ou dado do próprio GMS) e respeitando a migração progressiva (⚠️ da Parte B).

**P3. Formato de entrega de código:** patch cirúrgico, nunca rewrite; bloco YAML sempre completo; somente versões de controle já provadas no projeto (lista na Parte B §3.8); validação de nome duplicado antes de export. Uma única melhor solução implementada — não um cardápio de opções.

**P4. Em caso de dúvida, uma pergunta diagnóstica** — não três hipóteses especulativas.

**P5. Toda tela nova nasce dos Templates (Parte B §6) e dos tokens (Parte B §5.2).** Toda tela tocada converge para eles.

**P6. Emendas não reescrevem este arquivo — viram linha no diário.** Quando uma decisão nova alterar a norma, Claude diz "isso emenda o Mestre, seção X" e entrega **a linha pronta** no formato do diário (`DATA | NORMA | ALVO | VER | REF | TEXTO`). William cola no fim do `GMS_Diario.md`. A linha `NORMA` **vale a partir do momento em que é escrita**; o Mestre a absorve depois, em lote, quando William pedir consolidação (`python3 gms.py --consolidar` lista o que está pendente).

**P7. Prioridade de raciocínio ao propor qualquer coisa:** 1º confiabilidade do dado (números que batem) → 2º esforço do operador (menos digitação) → 3º poder de decisão da supervisão → 4º estética. Nunca inverter.

**P8. Estado atual das frentes:** Frente 1 (mapeamento + padronização) **concluída** — produtos: mapa MD/PDF + este documento. Frente 2 (consolidação das ~28 fontes) **bloqueada aguardando**: export dos fluxos do Power Automate + contagem de linhas das maiores listas. Quando esses insumos chegarem, o modelo relacional enxuto é o próximo entregável.

**P9. Pendências e insumos vivem no diário, não aqui.** Rode `python3 gms.py --pendencias`. Toda pendência nova entra como linha `PENDÊNCIA`; quando o insumo chegar, entra uma linha `RESOLVIDO` citando o mesmo `REF`. Nada de lista de pendências dentro deste arquivo — ela desatualiza a cada conversa.

**P10. Todo ciclo de trabalho termina em linhas de diário.** Claude entrega o código **e** as linhas prontas para colar no fim do `GMS_Diario.md` — uma por fato (entrega, lição, norma, melhoria nova, pendência). William só cola. Não existe "atualizar o documento": existe acrescentar linha. Se Claude não entregou as linhas, o ciclo não terminou.

**P11. Antes de propor, Claude lê:** este arquivo inteiro + as últimas ~40 linhas do `GMS_Diario.md` + a saída de `gms.py --estado`. Nunca o diário inteiro.

---

# PARTE A — VISÃO: O QUE FAZ O GMS SER ÚNICO

## A.0 GMS é mudança cultural, não ferramenta

O GMS não é "um app que a fábrica usa" — é **a forma como a fábrica pensa**: decisões saem do feeling e entram no dado; a informação deixa de morar em papel, planilha solta e na cabeça das pessoas e passa a morar num lugar só, visível a todos; o operador deixa de ser digitador e vira sensor inteligente do processo; o supervisor deixa de compilar o passado e passa a decidir o presente. Toda proposta técnica deste documento serve a essa mudança — se uma funcionalidade não muda comportamento, ela é enfeite.

## A.0.1 Taxonomia: um híbrido deliberado

O GMS tem núcleo de **MES**, mas rouba deliberadamente o melhor de cada disciplina vizinha — critério único: *se cabe no liquidificador e melhora a fábrica, entra*:

| Disciplina | O que o GMS rouba dela | Onde aparece |
|---|---|---|
| **MES/MOM** | Execução, genealogia, apontamento, OEE | Núcleo (fichas, ConsultaOP, Hora-Hora) |
| **APS** (Advanced Planning & Scheduling) | Sequenciamento com capacidade finita, sincronização de materiais entre etapas (pegging), what-if | C9, C23, C24, C8 |
| **SCADA** | Supervisão em tempo real, aquisição por sensor, alarmes, **historian** (histórico de processo) | C1, C20, C25 |
| **LIMS** | Gestão de resultados de ensaio, especificação vs. medido, cadeia de custódia, certificado de qualidade | C5, C26, C27, C28 |
| **Lean/TPM** | Andon, SQDC, TOC, skill matrix, passagem de turno | C1, C3, C6, C7, C12 |
| **IA nativa / Agentes (fronteira 2026)** | Linguagem natural sobre dados, classificação/sumarização automática, agentes autônomos vigiando o processo, visão computacional | C30–C34 |

Não existe categoria de mercado para isso — e é exatamente o ponto.

## A.1 Tese

MES tradicional **registra o passado**: o operador digita, o sistema guarda, o relatório sai amanhã. A tese do GMS é ser um MES que **enxerga o presente e antecipa o futuro** com os dados que já coleta — sem hardware caro, sem consultor, rodando em Power Platform e mantido por quem entende o processo (a fábrica).

Quatro pilares, em ordem de prioridade (mesma ordem do P7):

1. **Verdade única** — todo número do painel tem que bater com o chão de fábrica. Confiança é o produto nº 1.
2. **Esforço zero desnecessário** — o sistema deriva tudo que puder ser derivado; operador só informa o que só o operador sabe (paradas, motivos, observações).
3. **Supervisão por exceção** — o supervisor não caça problema em relatório; o problema chega nele, ranqueado por impacto.
4. **Memória de processo** — cada OP conta sua história completa (genealogia); cada turno deixa herança pro próximo.

## A.2 O diferencial honesto

O que já existe em MES comercial não é diferencial (ficha digital, hora-hora, dashboards). O diferencial do GMS está em três apostas que MES de prateleira **não** faz porque exige intimidade com o processo:

- **Derivação em vez de digitação** (Hora-Hora automático a partir da ficha; ETA por OP a partir de lead times reais);
- **Decisão empurrada** (Andon de exceções + OP Health Score + Radar de Gargalo — o sistema diz *onde olhar primeiro*);
- **Memória operacional** (passagem de turno assistida + voz do operador + genealogia QR).

---

# PARTE C — CATÁLOGO DE CONCEITOS
*(A Parte B — Padrões Técnicos — vem após o catálogo por ser material de consulta; os conceitos são o norte.)*

Cada conceito segue o formato: **o que é → por que é raro/único → como construir no Power Platform → decisão que habilita**. Legenda de horizonte: **H1** = dá pra fazer agora com o que existe · **H2** = depende da Frente 2 (dados consolidados) ou do token Factbird · **H3** = visão, depende de H1+H2 maduros. Marcação ★ = conceito raro ou inédito em MES.

## C.1 — Supervisão que decide (o coração do sistema)

### C1. Andon Digital — Feed de Exceções `H1`
**O que é:** um feed único, ordenado por criticidade, no Painel de Supervisão: OP parada além do teto, refugo acima do limite do dia, máquina parada com motivo recorrente, SPC fora de controle, composto vencendo. Cada card = 1 exceção + 1 ação sugerida.
**Por que:** hoje cada tela tem seu alerta isolado (e a OP zumbi de 4.162h prova que alerta isolado não é visto). Andon físico existe; Andon *agregado e ranqueado* em MES low-code, não.
**Como:** coleção `colExcecoes` montada no OnVisible da Supervisão com regras Power Fx sobre `ficha_producao`, `TiposErros`, `Hora-Hora`; severidade calculada; galeria única. Zero tabela nova.
**Decisão:** onde o supervisor gasta os próximos 15 minutos.

### C2. ★ OP Health Score `H1`
**O que é:** nota 0–100 por OP ativa, composta de 4 fatores: idade na etapa atual vs. lead time médio da etapa, refugo acumulado vs. tolerância, risco de validade de composto, e nº de retrabalhos/edições na ficha. Exibida como badge colorido no card da fila e na Supervisão.
**Por que:** MES mostra *status* (aguardando/em processo); nenhum mostra *saúde*. É o conceito que transforma 28 OPs ativas numa lista priorizada automaticamente.
**Como:** UDF `fx_HealthScore(op)` em `App.Formulas` usando os `data_hora_*` que já existem; lead times médios calculados de coleção histórica (H1 com média fixa por etapa; H2 com média móvel real).
**Decisão:** qual OP acelerar, qual investigar, qual replanejar — sem abrir nenhuma ficha.

### C3. ★ Radar de Gargalo Dinâmico (TOC aplicado) `H1→H2`
**O que é:** o sistema identifica **a restrição do dia**: a etapa com maior WIP acumulado × menor vazão nas últimas horas (Teoria das Restrições — o "tambor"). O painel declara: *"Gargalo agora: Trançagem (14 OPs, vazão 2.270 m/turno)"* e as demais etapas ganham orientação de subordinação (não produzir além do que o gargalo consome).
**Por que:** TOC é teoria consagrada, mas MES que *aponta o tambor em tempo real* praticamente não existe fora de APS caríssimo.
**Como:** H1 = contagem de WIP por etapa (o pipeline da Supervisão já tem!) + vazão do dia por `data_hora_final_<etapa>`; fórmula de razão WIP/vazão. H2 = refinado com tempos de ciclo do Factbird.
**Decisão:** onde colocar gente, hora-extra e atenção HOJE — a decisão mais valiosa de um supervisor de produção.

### C4. Previsão de Conclusão — ETA por OP `H2`
**O que é:** cada OP ganha data/hora prevista de finalização, calculada por lead time médio das etapas restantes (por família de mangueira). Lista de "OPs em risco" quando ETA > necessidade.
**Como:** tabela de lead times médios derivada do histórico da `ficha_producao` (pós-Frente 2, com dados limpos); `fx_ETA(op)`.
**Decisão:** o que prometer pro cliente/PCP e quando intervir antes do atraso acontecer.

### C5. SPC ao Vivo na Inspeção `H1`
**O que é:** carta de controle Xbar-R sobre Ø interno/externo/concentricidade (dados que a Finalização **já captura**, 6.078 registros na amostra), com alerta de tendência (regras de Nelson simplificadas: 7 pontos subindo, ponto fora de 3σ).
**Por que:** transforma inspeção de "registrar defeito" em "prever defeito antes do refugo".
**Como:** coleção dos últimos N registros por mangueira; média/desvio em Power Fx; gráfico nativo ou HtmlViewer (respeitando as regras de HTML da Parte B).
**Decisão:** parar/ajustar a máquina ANTES de refugar metros.

### C6. ★ Passagem de Turno Assistida `H1`
**O que é:** na virada de turno, o sistema monta sozinho o resumo: OPs que fecharam, OPs que travaram e onde, paradas e motivos, refugo do turno, pendências abertas. O supervisor que sai confirma/anota em 2 minutos; o que entra lê em 2 minutos. Fica registrado (lista `Passagem_Turno`).
**Por que:** a passagem de turno é o momento onde mais informação se perde em qualquer fábrica — e nenhum MES low-code ataca isso. É memória operacional pura.
**Como:** tela nova no Template C; agregações sobre dados existentes filtrados por `fx_TurnoAtual`/`fx_DataRef`; 1 lista nova pequena.
**Decisão:** o turno que entra começa sabendo, não descobrindo.

### C7. Quadro Tier/SQDC Automático `H2`
**O que é:** o quadro de reunião diária (Segurança-Qualidade-Entrega-Custo) preenchido sozinho: Q = refugo do dia, E = aderência ao plano, C = custo do refugo (C15). Supervisor adiciona só S e ações.
**Por que:** o ritual Tier existe em toda fábrica lean — mas alimentado à mão. Aqui ele nasce dos dados.
**Decisão:** reunião diária de 10 min olhando pra frente, não compilando o passado.

### C8. ★ Simulador de Fila ("E se?") `H3`
**O que é:** modo sandbox no painel: arrasta uma OP pra frente da fila e vê o impacto no ETA de todas as outras antes de confirmar. Confirmou → vira o plano; cancelou → nada muda.
**Por que:** análise what-if é território de APS de seis dígitos. Uma versão honesta (lead times médios, sem otimização matemática) já muda o jogo da decisão de priorização.
**Como:** coleção-espelho da fila + recálculo de `fx_ETA` em memória; nenhuma escrita até confirmar.
**Decisão:** priorizar com consequência visível, não no feeling.

## C.2 — Chão de fábrica que flui

### C9. Sequenciamento Inteligente da Fila `H2`
**O que é:** a fila de cada etapa ordenada por algoritmo simples: due date + minimização de troca de bitola/mangueira (setup), não FIFO de chegada. Card "próxima OP recomendada" com o porquê.
**Como:** score de ordenação em Power Fx (`peso1·atraso + peso2·igualdade_de_bitola_com_atual`); pesos em `ConfiguracaoGMS` pra fábrica calibrar.
**Decisão:** menos setup = OEE direto, sem investir um real.

### C10. Kanban Eletrônico de Carretéis `H1`
**O que é:** saldo vivo de carretéis por estado (vazio/em uso/cheio aguardando) e alerta de escassez por bitola. Os dados já existem (`lista_carreteis`, `Historico_Carretel` — 1 linha por carretel/etapa/OP).
**Decisão:** nunca mais parar trançadeira por falta de carretel sem aviso prévio.

### C11. FIFO Enforcement na Bobinadeira `H1`
**O que é:** a `FifoBobinadeira` já existe; o conceito é o *enforcement suave*: consumir fora da ordem exige motivo (dropdown), e o furo de FIFO vira métrica no painel.
**Decisão:** disciplina de FIFO auditável sem burocracia.

### C12. ★ Matriz de Habilidades Viva `H2`
**O que é:** `Colaboradores` × etapas × nível (treinando/apto/certificado/instrutor). O dropdown de operador de cada tela filtra por aptidão; o painel mostra gaps ("só 1 operador certificado em Vulcanização no turno 3").
**Por que:** skill matrix existe em Excel morto em toda fábrica; viva e conectada à operação, praticamente nunca.
**Decisão:** alocação de gente e plano de treinamento guiados por dado.

### C13. Hora-Hora Automático — em TODOS os processos `H1→H2`
**O que é:** decisão de projeto (emenda v1.1): **todo processo terá seu Hora-Hora** — Mandril e Trançagem já têm, Tubo será concluído (a `scrHoraHora_Tubo` órfã deixa de ser candidata a exclusão e passa a ser terminada: religar entrada + corrigir fonte), e os demais entram progressivamente via Template B parametrizado por processo (como Montagem já faz com 13 células em 1 tela). Meta derivada de takt/velocidade por mangueira (`colVelocidadeProducao` existe), Real derivado dos patches da ficha por janela horária. Operador só confirma paradas e motivos.
**Por que:** mata a digitação dupla — o maior desperdício de esforço do GMS hoje — e elimina a divergência ficha×hora-hora por construção.
**Decisão:** hora-hora vira sensor de aderência, não tarefa.

### C14. ★ Voz do Operador `H1`
**O que é:** botão discreto em toda tela: "Reportar problema" → 1 campo de texto + foto opcional (câmera do tablet) → vira card no feed do supervisor (C1) com tela/OP/máquina anexadas automaticamente.
**Por que:** canal direto chão-de-fábrica→gestão com contexto automático é raríssimo; em MES low-code, inédito. Custa uma lista e um modal.
**Decisão:** problemas pequenos aparecem antes de virarem paradas grandes — e o operador vira sensor inteligente do sistema.

### C35. ★ Bipe Universal — todo campo bipável tem câmera ao lado `H1`
**O que é:** decisão de projeto (emenda v1.3): **todo campo de entrada que hoje é preenchido a partir de uma etiqueta física ou crachá ganha um `BarcodeReader` inline ao lado**, seguindo o padrão já provado na Montagem (P/N, OT, Crachá). Nada de tela de "escolher o que bipar" — a câmera mora no próprio campo, sem decisão extra pro operador (P7: esforço zero).
**Por que:** bipagem pontual (só na Montagem) já mostrou o ganho — digitação vira toque. Generalizar é puro replay do padrão, sem inventar nada novo; o custo por tela é baixo (1 controle + 1 `ctx` + 1 `Default` por campo).
**Onde entra primeiro (candidatos por volume de digitação/erro):**
- **OP** em toda ficha de etapa (Mandril, Tubo, Trançagem, Cobertura, Bandagem, Vulcanização, Debandagem, Finalização) — hoje digitada ou colada, maior campo repetido do sistema;
- **Crachá do operador** em toda tela que hoje pede identificação manual (Template A e C);
- **Lote de composto** (Tubo/Cobertura) — reforça C18 (validade de composto), porque lote errado digitado é a causa raiz que a validação de validade não pega;
- **Carretel** (Kanban C10, Custódia C27) — bipar o ID do carretel na troca de etapa em vez de escolher em dropdown;
- **Genealogia QR** (C21) — fecha o ciclo: a mesma ficha que **gera** o QR (C21) agora também **lê** QR em outras etapas do processo, com o mesmo controle.
**Como:** Template A e C ganham o `bcr_*` como elemento padrão do layout ao lado de qualquer `inp_*`/`txt_*` que hoje recebe dado de etiqueta; regras de B §3.9 se aplicam a todas as instâncias. Nenhuma tabela nova.
**Decisão:** o "bipe ou digite" deixa de ser exceção de uma tela e vira o modo padrão de entrada do GMS inteiro — ataca esforço do operador (pilar 2) em escala, com uma peça de tecnologia já testada e paga.

### C36. ★ Sinóptico Vivo da Planta `H1→H2` *(consolidado v1.5)*
**O que é:** a planta real da célula como pano de fundo e o estado vivo desenhado em cima: uma baliza por máquina/etapa (em processo · fila aguardando · livre) + contador de carretéis na espera; toque na baliza abre o detalhe (OP, mangueira, operador, tempo na etapa). Recortes por área cobrem a fábrica inteira.
**Por que:** é o painel sinóptico (*mimic panel*) do SCADA aplicado a MES low-code — praticamente inédito. Responde a pergunta espacial "**ONDE** está o problema", complementando o Andon C1 ("**QUAL** é o problema"). Vira a TV da célula.
**Como:** H1 = `Image` da planta + balizas nativas (`Classic/Button`) lendo `colEstadoProcessos` derivada da `ficha_producao` por timer somente-leitura (B §3.4); posições em % numa Named Formula (`fx_LayoutBalizas`, com colunas `id, nome, etapa_gms, Trançadeira, tranc, temFila, px, py, fx, fy`), recalibráveis pelo protótipo HTML. H2 = estados de sensor (parada não programada, setup) via Monitor/Factbird (C20), badge de carretel via custódia (C27), buffers via kanban (C10), navegação entre recortes.
**Lição paga na implementação (vale para todo `AddColumns` do GMS):** dentro de `AddColumns`, um `LookUp`/`Filter` aninhado faz `ThisRecord` resolver para o **escopo interno**, não para a linha externa — e nome de coluna entre aspas duplas compila silenciosamente como literal de texto, avaliando sempre falso. Ambos os erros são **silenciosos**: a tela renderiza, os números vêm errados. Norma decorrente: usar sempre o operador `As` com alias explícito em escopo aninhado, e nunca aspas em nome de coluna. Na v1.2 do sinóptico a fórmula foi simplificada para um `Switch` sobre `LookUp(colEstadoProcessos, ...)` sem escopo aninhado.
**Decisão:** um olhar responde quem roda, quem espera e onde o material acumulou — antes de abrir qualquer ficha.

## C.3 — Dados que se defendem sozinhos

### C15. Custo da Qualidade em R$ `H1`
**O que é:** metros de refugo × custo padrão por família de mangueira (tabela de domínio pequena) = R$ do dia/semana/mês no painel, com Pareto por causa.
**Por que:** metro não sensibiliza diretoria; real sensibiliza. O dado de refugo já existe em 3 fontes (unificadas na Frente 2).
**Decisão:** priorização de melhorias por dinheiro, não por percepção.

### C16. Pareto Vivo de Refugo `H1`
**O que é:** Pareto automático por causa/máquina/turno/mangueira, período selecionável, direto no app (sem esperar o Power BI de amanhã). `TiposErros` tem 1.574 registros prontos.
**Decisão:** atacar a causa nº 1 da semana com dado da semana.

### C17. ★ Guardião de Apontamento (anomalia de digitação) `H1`
**O que é:** validação estatística no Patch: quantidade fora do perfil histórico da mangueira/etapa (ex.: 5.000 m onde a média é 500) pede confirmação explícita antes de gravar; confirmações ficam auditáveis.
**Por que:** data quality guard estatístico embutido no apontamento é conceito de sistema corporativo caro — e aqui custa uma UDF.
**Decisão:** o painel nunca mais mente por erro de dedo — protege o pilar nº 1 (verdade única).

### C18. Validade de Composto Proativa `H1`
**O que é:** os campos de validade já capturados (Tubo/Cobertura) alimentam alerta: lote a X dias de vencer aparece no Andon antes de ser usado.
**Decisão:** zero refugo por composto vencido, zero descarte por esquecimento.

### C19. MTBF/MTTR por Máquina `H2`
**O que é:** derivado dos motivos de parada do Hora-Hora: tempo médio entre falhas e tempo médio de reparo por trançadeira; ranking de máquinas problemáticas alimenta manutenção.
**Decisão:** manutenção preventiva direcionada por dado, e munição objetiva para pedir investimento.

### C20. Integração Factbird (IoT) `H2 — piloto já desenhado`
**O que é:** (já em andamento no projeto) webhook Factbird → Power Automate → campos paralelos `inicio_sensor`/`fim_sensor` na ficha, validando confiabilidade antes de aposentar o apontamento manual de início/fim.
**Estado:** arquitetura pronta; bloqueado no token da API (via suporte Factbird).
**Decisão:** timestamps de máquina = verdade absoluta de tempo de ciclo → alimenta C3, C4, C13 com precisão de sensor.

### C21. Genealogia QR — Certidão da OP `H1`
**O que é:** a ficha impressa carrega QR Code 128 (implementação offline já validada no projeto, 4 UDFs) que abre a ConsultaOP daquela OP: quem fez, quando, com que lote, com que resultado — a mangueira conta a própria história anos depois.
**Decisão:** rastreabilidade de auditoria/recall em segundos, não em arquivos.

### C22. Aderência ao Plano (Schedule Adherence) `H2`
**O que é:** % de OPs concluídas na data planejada, por semana/família. O "E" do quadro SQDC (C7).
**Decisão:** a métrica que conecta a fábrica ao compromisso comercial.

## C.4 — Sabores das disciplinas vizinhas (emenda v1.1)

### C23. ★ Cadeia Interna Sincronizada — o upstream enxerga o downstream `H1→H2`
**O que é:** cada etapa fornecedora vê a demanda real de quem ela alimenta (pegging de APS aplicado dentro da célula):
- **Tubo enxerga as trançadeiras**: fila, velocidade e consumo de cada TH/TM/TO/Spiral (dados do fluxo "Monitor" já existente no Power Automate) → o Tubo sabe **para qual trançadeira priorizar** produção.
- **Mandril enxerga Tubo + Trançagem**: antes de extrusar mais de uma bitola, o painel do Mandril mostra o estoque daquela bitola já em processo no Tubo e o que a Trançagem vai puxar → decide se **realmente precisa** fazer mais.
**Por que:** MES clássico é cego por etapa — cada tela vê só a si mesma. Sincronização de material entre estágios é território de APS; aqui nasce dos dados que o GMS já tem (`ficha_producao` por etapa + estoque por bitola da Extrusora + Monitor das trançadeiras).
**Como:** H1 = cards de demanda downstream nas telas de Tubo e Mandril (coleções agregadas); H2 = enriquecido com velocidades reais do Monitor/Factbird. Depende do arquivo do fluxo Monitor (P9).
**Decisão:** produzir o que o próximo processo vai consumir — não o que a fila local sugere.

### C24. Planejamento de Máquina Simples + Alertas Reconciliados `H1`
**O que é:** plano por máquina × turno (feijão com arroz: uma lista `Plano_Maquina` com trançadeira, turno, OPs previstas), e — o pulo do gato — **os alertas conversam com o plano**: o sistema só acusa "vai faltar mandril para a TH6" se o plano daquela máquina naquele turno ainda tiver produção pendente que dependa desse mandril. Plano completo = alerta suprimido.
**Por que:** alerta sem contexto de plano gera falso positivo, e falso positivo mata Andon (o supervisor para de olhar). Capacidade finita simplificada + reconciliação de alarme é conceito de APS/SCADA que MES low-code não faz.
**Como:** 1 lista pequena + regra de supressão nas fórmulas do Andon (C1). Evolui depois; nasce simples de propósito.
**Decisão:** todo alerta que chega é real — confiança no Andon preservada.

### C25. ★ Diário de Bordo por Processo (Historian) `H1`
**O que é:** cada processo ganha seu histórico navegável **por Dia e Turno**: linha a linha com hora, OP, metragem, diâmetros, quem fez — "o que passou por aqui hoje?" respondido em 2 toques. É o conceito de *historian* do SCADA aplicado a apontamentos: registro imutável e consultável da operação, separado da tela transacional.
**Por que:** hoje esse dado existe espalhado na `ficha_producao` (103 colunas, 1 linha por OP) mas é inconsultável por processo/dia/turno. O historian inverte o eixo: a pergunta deixa de ser "o que aconteceu com a OP X" (ConsultaOP já responde) e passa a ser "o que aconteceu no Tubo no 2º turno de ontem".
**Como:** tela única parametrizada por processo (Template C invertido: filtros Dia/Turno/Processo em cima, tabela embaixo), lendo os `data_hora_*`, `quantidade_*`, `diametro_*`, `operador_*` da etapa; ordenada por hora usando `fx_DataRef` (respeita a virada 05:20). Zero tabela nova em H1; na Frente 2 o modelo normalizado (evento por linha) torna isso trivial e rápido.
**Decisão:** auditoria diária, resposta a "quem fez/quando" e matéria-prima da Passagem de Turno (C6) — os dois conceitos se alimentam.

### C26. Delineamento Vivo — especificação na tela `H1→H2`
**O que é:** o Delineamento (especificação de engenharia da mangueira: picks, diâmetros nominais, fita, composto — hoje no site `DelineamentoHM`, parcialmente integrado via `Imagens Fitas`) migra para **dentro das telas que faltam**: ao lado de cada campo de entrada, o valor especificado; entrada fora da spec ganha aviso visual imediato (poka-yoke).
**Por que:** é o conceito LIMS de *specification vs. measured* aplicado ao apontamento. O operador compara com a spec no momento da digitação, não a qualidade dois dias depois.
**Como:** H1 = concluir a migração do Delineamento nas telas pendentes (leitura da fonte + exibição contextual); H2 = validação automática spec×medido com faixas por mangueira.
**Decisão:** desvio de especificação morre na origem.

### C27. Custódia de Carretel — handoff confirmado `H1`
**O que é:** a transferência de carretel entre processos ganha **confirmação de recebimento**: o processo seguinte confirma que recebeu o carretel X da OP Y (1 toque no card). Até confirmar, o carretel fica "em trânsito" — visível no kanban (C10). É cadeia de custódia (chain of custody, conceito LIMS) aplicada ao material.
**Por que:** hoje o envio é registrado por quem manda; sumiu carretel, ninguém sabe onde. Custódia fecha o ciclo com custo de 1 status + 1 botão (a `Historico_Carretel` já tem a estrutura 1-linha-por-carretel-por-etapa).
**Decisão:** carretel nunca mais "some" entre processos — sempre há um responsável atual.

### C28. Certificado de Qualidade por OP (LIMS-lite) `H2`
**O que é:** ao finalizar a OP, o sistema monta o **certificado**: medições de inspeção (Ø int/ext, concentricidade — `RegistrosInspeção` já tem 6 mil registros), lotes de composto usados, operadores, resultado vs. especificação (C26). Imprimível/PDF com o QR de genealogia (C21).
**Por que:** Certificate of Analysis é entregável clássico de LIMS; num MES de chão de fábrica, praticamente inexiste. Para cliente exigente ou auditoria, é ouro.
**Decisão:** qualidade demonstrável documento em mãos, gerada em zero minutos.

### C29. Power Automate como Camada de Cálculo `H1 — arquitetural`
**O que é:** cálculos pesados, agregações históricas e transformações saem do Power Fx da tela e vão para fluxos do Power Automate (ou, na Frente 2, para o servidor): lead times médios (C4), estatísticas do SPC (C5), score de saúde histórico (C2), fechamentos de turno (C6/C25). O app **lê resultado pronto** de uma lista de resultados, em vez de calcular na abertura da tela.
**Por que:** a própria arquitetura de referência da Microsoft recomenda deslocar lógica complexa do canvas para o servidor — reduz espera, centraliza a regra e escala. E casa com a realidade do GMS: o fluxo "Monitor" já existe e já calcula velocidades de trançadeira; o padrão é expandi-lo, não inventar outro.
**Como:** fluxos agendados (recorrência por turno/hora) gravando em listas de resultado (`Resultados_Calculados` ou similar); app consome com filtro delegável simples.
**Decisão:** telas rápidas + regra de negócio num lugar só, testável fora do app.

### C39. ★ Etapa em Batelada — o processo que não se aponta, se acompanha `H1` *(emenda v1.4)*
**O que é:** algumas etapas do GMS **não produzem metragem**: recebem material pronto, aplicam tempo/temperatura e devolvem a mesma metragem. A Vulcanização é o caso puro — a autoclave não corta mangueira. Nessas etapas o operador **não aponta quantidade nem se identifica por OP**: ele aciona transições físicas (carregar → resfriar → descarregar) e o sistema mede o resto. A ficha deixa de ser formulário e vira **painel de estado**.
**Por que é raro:** MES de prateleira modela toda etapa como "apontamento de produção" e obriga o operador a redigitar quantidade e operador em cada uma. Isso gera duas mentiras: número redigitado que diverge do real (fere o pilar 1) e digitação que não informa nada (fere o pilar 2). Diagnóstico que originou o conceito: na `scr_Vulcanização_1` v0.1.3, os campos `operador_vulcanizacao` e `quantidade_vulcanizacao` eram digitados pelo operador e **sobrescritos no envio em lote** pelo `ForAll` do modal — 100% do esforço de digitação era descartado pelo próprio sistema.
**Como construir:**
1. Estado da OP é **função pura** dos campos de transição, nunca variável (ver B §3.10).
2. Um único botão de ação, cujo texto/cor/ação derivam do estado (ver B §6.1, Template A′).
3. Quantidade **herdada** da etapa anterior e exibida read-only, com a origem escrita na tela ("675 m recebidos da Bandagem"). Ajuste vira exceção explícita, nunca campo de rotina.
4. Operador informado **uma vez por lote**, no descarregamento, não por OP.
5. A transição física intermediária (no caso, o resfriamento) é **pré-requisito de fluxo**, não trava de relógio: sem ela o botão de envio não existe e a OP não entra na coleção de elegíveis.
**Onde mais se aplica:** Vulcanização (implantado), Post-Cure, e qualquer forno/estufa futuro. Debandagem e Extração/Teste devem ser reavaliadas contra este conceito — se a metragem que registram é sempre cópia da anterior, elas também são etapas de batelada disfarçadas de apontamento.
**Decisão que habilita:** o tempo de ciclo real da autoclave passa a ser medido (início → resfriamento) sem ninguém cronometrar, alimentando o Diário de Bordo (C25) e o MTBF/MTTR (C19) de graça.

---

## C.5 — Fronteira 2026: IA nativa e agentes (emenda v1.2)

*Contexto: o 2025 release wave 2 da Power Platform (out/2025→mar/2026) tornou o padrão da plataforma "agent-first": apps modernos, responsivos e offline por default; agentes autônomos no Copilot Studio; Dataverse com MCP Server e funções de IA chamáveis direto do Power Fx. O GMS deve surfar isso — não reimplementar na mão o que a plataforma agora dá de graça.*

### C30. Copiloto do GMS — pergunte à fábrica `H2`
**O que é:** caixa de linguagem natural no Painel de Supervisão: *"quantos metros a TH06 fez ontem no 2º turno?"*, *"qual mangueira mais refugou essa semana?"* — respondida sobre os dados reais do GMS.
**Por que:** o wave 2 entrega Copilot para usuários explorarem dados e navegarem apps por linguagem natural; com Dataverse (MEL-049) e Dataverse Search agent-ready, isso vira configuração, não desenvolvimento.
**Como:** pós-migração Dataverse: Copilot habilitado no app + prompts grounded nas tabelas (RAG nativo do Prompt Builder). Em SharePoint isso não existe — mais um peso na balança da migração.
**Decisão:** a pergunta que hoje exige abrir 3 telas e filtrar vira uma frase.

### C31. ★ Agente Autônomo de Supervisão — o MES que age sozinho `H3`
**O que é:** um agente (Copilot Studio) que **vigia** o GMS continuamente e **age** dentro de limites definidos: OP estagnada > teto → notifica o supervisor no Teams com contexto; refugo anômalo → abre registro de ação e sugere causa provável com base no histórico; falta prevista de mandril reconciliada com o plano (C24) → aciona a Extrusora. Humano aprova ações críticas (human-in-the-loop, padrão do wave 2 do Power Automate).
**Por que:** é a materialização do "MES do próximo século": supervisão por exceção (pilar 3) executada por agente, não por olho humano varrendo painel. Autonomous agents + teams of agents são exatamente a aposta central da Microsoft para 2026.
**Como:** Copilot Studio agent com gatilhos dos fluxos existentes (Monitor expandido, C29) + ações limitadas e auditáveis; governança pelo admin center (o wave 2 trouxe o arcabouço de governança de agentes).
**Decisão:** o supervisor deixa de ser alarme humano e vira aprovador de ações já preparadas.

### C32. Funções de IA no fluxo de dados (AIClassify / AISummarize / AIExtract) `H2`
**O que é:** três aplicações cirúrgicas das funções de IA prontas do Dataverse (chamáveis do Power Fx via `Environment.AIClassify(...)` e do Power Automate via unbound action):
- **AIClassify** sobre observações livres de refugo/parada → categoria automática (alimenta o Pareto C16 sem burocratizar o operador);
- **AISummarize** sobre os eventos do turno → rascunho automático do texto da Passagem de Turno (C6) que o supervisor só ajusta;
- **AIExtract** sobre observações → puxa lote/máquina/medida citados em texto livre para campos estruturados.
**Por que:** zero treinamento de modelo, zero coleta de dados — são prebuilt. O custo é licença AI Builder + Dataverse; o ganho é dado estruturado nascendo de texto livre.
**Decisão:** o texto solto do operador vira dado analisável — sem obrigar o operador a preencher mais campos.

### C33. Visão Computacional na Inspeção `H3`
**O que é:** foto do defeito (a Voz do Operador C14 já prevê câmera) classificada por modelo de detecção do AI Builder: tipo de defeito sugerido automaticamente; galeria de defeitos vira base de treinamento contínuo.
**Por que:** inspeção visual assistida por IA é o degrau acima do SPC (C5): o SPC vê o número; a visão vê o defeito.
**Decisão:** classificação de defeito consistente entre turnos e operadores.

### C34. Offline-First — a rede cai, o apontamento não para `H1→H2`
**O que é:** o GMS sobrevive a queda de Wi-Fi no chão de fábrica: H1 (SharePoint) = fila local de escrita — `Patch` que falha (o `IfError` da Parte B §3.7) grava numa coleção persistida com `SaveData()`, e um sincronizador reenvia quando `Connection.Connected` volta; H2 (Dataverse) = offline nativo **de um toque** — o wave 2 tornou apps offline o default da plataforma, mas **SharePoint não é suportado** pelo offline moderno, só Dataverse.
**Por que:** apontamento perdido por queda de rede fere o pilar 1 (verdade única) e o 2 (esforço zero — redigitar é o pior esforço). E é mais um argumento objetivo e documentado para a MEL-049.
**Decisão:** confiabilidade de apontamento independente da infraestrutura de rede da célula.

## C.7 — Execução multi-recurso e estrutura de fluxo (emenda v1.5)

### C37. ★ Posto de Trabalho como Entidade de Estado `H1`
**O que é:** em etapa com mais de um recurso físico, **o estado de processo pertence ao posto, nunca à tela**. Uma tela abre N raias simultâneas, uma por máquina, cada uma com sua OP, seu cronômetro e sua ação. O `recurso` do evento passa a ser a **máquina física**, não o cadastro do PN.
**Por que:** o padrão anterior (uma variável `varProduzindo`/`varFichaAtiva` por tela) impunha um processo ativo por vez. Consequência real medida no Mandril: com dois operadores no mesmo PC, o segundo **fechava a OP do primeiro antes da hora** para liberar a tela. Isso não é inconveniência de UX — é **corrupção de tempo de ciclo na origem**, e invalida C3 (gargalo), C13 (hora-hora) e C19 (MTBF/MTTR) de uma vez. Fere o pilar 1 pela raiz.
**Como construir:**
1. Coluna de posto na `ficha_producao` (instância Mandril: `maquina_mandril`, texto simples, **indexada** — MEL-012), gravada no início.
2. Cadastro dos postos numa coleção (`colMaquinasMandril`: `Posto`, `Rotulo`), com o rótulo de chão de fábrica só na tela.
3. **Coleção chaveada por posto** (`colPostosMandril`) construída com `ForAll` sobre o cadastro, cada linha carregando `FichaID`, `Inicio`, `Bitola`, `Produzindo`. Ela substitui as variáveis de estado único.
4. `Filter` delegável por duas igualdades no lugar do `LookUp` não delegável (B §4.2).
5. **Seleção do posto acontece a montante**, no menu de navegação (`scr_selecaosetor_1`): a tela da etapa recebe `varPostoAtivo` já definido antes do `OnVisible`, com o card do menu mostrando o estado vivo de cada posto (livre / em produção com OP e bitola).
6. O Delineamento (C26) filtra pela tecnologia do posto: parâmetro que não é daquela máquina não aparece, em vez de aparecer lado a lado para o operador escolher no olho.
**Instância implantada:** Mandril, com os dois soldadores reais — `TERMOFUSAO` (solda quente) e `VIBRACIONAL` (solda vibracional). Rollout previsto para Trançagem.
**Cutover:** marco zero, sem backfill (mesma regra do `Eventos_Producao`). OPs em processo no momento do publish caem num bloco de atribuição onde o operador diz de qual posto são; depois disso a coleção de órfãs fica vazia para sempre.
**Consequência a tratar:** o Hora-Hora da etapa passa a somar duas máquinas na mesma meta. A meta do turno dobra ou vira meta por posto (entra em MEL-033/035).
**Decisão que habilita:** tempo de ciclo real por tecnologia e por bitola, o que não existia. Se a diferença entre as tecnologias for material, vira regra de sequenciamento (C9) sem investir nada.

### C38. ★ Split de Lote por Sobra `H1`
**O que é:** quando o operador informa que sobrou material do carretel, o sistema **divide a ficha**: corrige o registro pai para refletir só o que foi consumido, e cria um registro filho com a sobra, herdando os campos de origem (Mandril) e preservando quantidade original, carimbos de tempo e posto. O filho **reentra na fila** da etapa com o mesmo carretel.
**Por que:** sem split, a sobra vira uma de duas mentiras — ou some do sistema (metragem que existe fisicamente e não existe no dado), ou infla o consumo do pai (rendimento falso). Ambas ferem o pilar 1. Com split, cada metro tem exatamente um dono.
**Como:** campo `ficha_pai` na `ficha_producao` guardando o `ID` do registro de origem (nunca o número da OP — B §4.2). O `ficha_pai` **não é requisito operacional**: o filho funciona sem ele. Ele serve à genealogia e à rastreabilidade de qualidade (C21/C28), respondendo "de qual bobina veio este pedaço". Alternativa leve, se a coluna não puder ser criada: gravar a referência em campo de observação como texto, aceitando que a consulta reversa vira busca textual.
**Instância:** tela do Tubo. Aplicável a qualquer etapa que consuma carretel parcialmente.
**Decisão que habilita:** rendimento por carretel deixa de ser estimativa e a sobra para de evaporar entre turnos.

### C40. ★ Grafo de Fluxo e Genealogia — tabela de arestas, travessia no servidor `H1→H2`
**O que é:** promover o fluxo do processo e a genealogia do material a **estrutura de grafo explícita**: uma tabela de arestas consultável, não um encadeamento implícito espalhado pelo código. **Não é banco de grafo** (Neo4j, Dataverse graph): trocar a fonte tem custo alto e ganho zero para o operador. É tabela de arestas + travessia no servidor.
**Três ganhos, em ordem de retorno:**
1. **Matar o fluxo hardcoded.** Hoje "quem vem depois de mim" mora como string literal repetida nas 8 telas de etapa — um grafo implícito escrito 8 vezes, sem validação. Promover a `fFluxoEtapas` a autoritativa (`etapa_origem → etapa_destino` + condição) faz as telas **lerem** o próximo passo em vez de **saberem** o próximo passo. Mudar roteiro (pular Bandagem numa família, inserir Post-Cure) vira linha na lista, não 8 publishes. É pré-requisito do Template B parametrizado (C13/MEL-035).
2. **Genealogia que aguenta recall.** Rastreabilidade real é N:N: 1 lote de composto → N OPs; 1 OP → N carretéis; e com C38, 1 ficha → N filhas. Achatado nas 103 colunas da `ficha_producao`, isso não é consultável de trás para frente — "que OPs usaram o lote X?" é arqueologia. Uma tabela `Genealogia` (`no_origem, tipo_origem, no_destino, tipo_destino, relacao, data`) responde em uma consulta. É o que falta para C21 e C28 valerem em auditoria, e não só na tela.
3. **Gargalo calculado, não codificado.** Sem aresta, cada par upstream/downstream é código novo — MEL-039 e MEL-050 são literalmente a mesma lógica escrita duas vezes. Com aresta, é uma fórmula só rodando sobre a tabela (C3, C23).
**Onde não usar:** a `ficha_producao` **continua linear**, como passaporte da OP. O grafo mora ao lado; não substitui a máquina de estados da etapa (B §3.10).
**Restrição técnica ⛔:** **Power Fx não tem recursão** — travessia de grafo não roda no app. Vai em Power Automate (C29) ou em DAX com `PATH()`/`PATHCONTAINS` no Power BI. Qualquer proposta de travessia em Power Fx deve ser recusada de saída.
**Decisão que habilita:** roteiro de produção vira configuração, e rastreabilidade vira consulta em vez de escavação.

## C.6 — Mapa de dependências entre conceitos

```
Fundação (Parte B: fx_TurnoAtual, fx_DataRef, tokens, dados que batem)
   ├─ C1 Andon ──────────┬─ C6 Passagem de Turno
   │                     └─ C14 Voz do Operador (alimenta C1)
   ├─ C35 Bipe Universal ─ reforça C13, C18, C21, C27 (menos erro de digitação)
   ├─ C2 Health Score ───┬─ C4 ETA ──── C8 Simulador (H3)
   │                     └─ C3 Radar de Gargalo
   ├─ C5 SPC · C16 Pareto · C15 Custo R$ · C17 Guardião · C18 Validade
   ├─ C10 Kanban Carretel · C11 FIFO · C21 QR
   └─ C13 Hora-Hora Auto ── C19 MTBF/MTTR ── C22 Aderência
Frente 2 (dados consolidados) desbloqueia: C4, C7, C9, C12, C19, C22, C28
Factbird (token) turbina: C3, C4, C13, C19, C20
Fluxo Monitor (arquivo pendente — P9) alimenta: C23, C24, C29
C25 Diário de Bordo ⇄ C6 Passagem de Turno (se alimentam mutuamente)
C26 Delineamento → C28 Certificado (spec é insumo do CoA)
Dataverse (MEL-049) desbloqueia a fronteira: C30 Copiloto, C32 AI functions, C34 offline nativo
C36 Sinóptico ⇄ C1 Andon (ONDE × O QUÊ) · v2 consome C20, C10, C27
C37 Posto de Trabalho → pré-requisito de tempo de ciclo honesto: C3, C13, C19
C38 Split de Lote → alimenta C21/C28 (genealogia da sobra) · consome C27
C39 Etapa em Batelada → alimenta C25 Diário de Bordo (ciclo medido sem cronômetro)
C40 Grafo ── fFluxoEtapas autoritativa → C13/C35 (roteamento por bipe) · Genealogia → C21, C28 · arestas → C3, C23
   └─ travessia SEMPRE em C29 (Power Automate) ou DAX; nunca em Power Fx
C31 Agente Autônomo consome: C1 Andon + C24 plano reconciliado + C29 camada de cálculo
```

---

# PARTE B — PADRÕES TÉCNICOS OBRIGATÓRIOS
*(padronização de código, dados e UI/UX — consolidada do antigo `GMS_Guia_Padronizacao.md`)*

**Como ler:** cada norma traz **Evidência GMS** (onde a auditoria encontrou o problema) e **Fonte** (documentação oficial ou padrão de comunidade). ⛔ = bloqueante para tela nova · ⚠️ = migração progressiva (aplicar quando a tela for tocada).

## 1. Nomenclatura

### 1.1 Norma ⛔ — Prefixo de tipo + propósito, em camelCase com underscore de seção

O GMS já tem convenção validada em produção. Ela é mantida e passa a ser obrigatória em **todo controle novo**:

| Prefixo | Tipo de controle | Exemplo GMS |
|---|---|---|
| `scr_` | Tela | `scr_ExtrusoraMandril` |
| `gal_` | Gallery | `gal_sobras_vitrine` |
| `frm_` | Form | `frm_FichaTubo` |
| `ctn_` | GroupContainer / modal | `cntr_confirma_historico_tubo` |
| `btn_` | Botão | `btn_IniciarOP` |
| `ico_` | Ícone/imagem clicável | `ico_Refresh` |
| `rct_` | Rectangle | `rct_HeaderFundo` |
| `lbl_` | Label | `lbl_TituloTela` |
| `tmr_` | Timer | `tmr_AutoRefresh` |
| `cmb_` | Dropdown/ComboBox | `cmb_Operador` |
| `inp_` | TextInput (em DataCard) | `inp_Quantidade` |
| `spr_` | Spinner | `spr_Carregando` |
| `html_` | HtmlViewer | `html_FichaImpressao` |
| `dc_` | DataCard | `dc_Lote` |
| `bcr_` | BarcodeReader | `bcr_bipe_pn_m_1` |

Complementos vindos do padrão Microsoft/Devaney para tipos ainda sem prefixo no GMS: `chk_` (checkbox), `tgl_` (toggle), `dte_` (date picker), `img_` (imagem não clicável), `cmp_` (instância de componente).

**Evidência GMS:** as 16 telas antigas do dump ainda carregam nomes auto-gerados (`Gallery4_9`, `Rectangle11`, `DataCardValue38_1`, `Button3_1`). Isso torna o App Checker ilegível (não dá pra saber o que é o quê nos 2.854 apontamentos) e trava manutenção por terceiros.

**Fonte:** o guia de legibilidade da Microsoft recomenda exatamente esse formato — descritor de tipo + propósito em camelCase — porque facilita construir fórmulas e buscar controles; e o white paper oficial reforça que a convenção específica importa menos que a **consistência total** (learn.microsoft.com/power-apps/guidance/coding-guidelines/code-readability).

### 1.2 Norma ⛔ — Variáveis com escopo no nome

| Prefixo | Escopo | Criada com | Exemplo GMS |
|---|---|---|---|
| `gbl` | Global (app inteiro) | `Set()` | `gblTurno1_Inicio` |
| `ctx` | Local (uma tela) | `UpdateContext()` | `ctxDataRef` |
| `col` | Coleção | `ClearCollect()` | `colMangueiraTrancadeira` |
| `fx_` | Named Formula / UDF | `App.Formulas` | `fx_TurnoAtual` (novo, ver §3.2) |

Regra de decisão: **prefira `ctx` a menos que o valor realmente precise cruzar telas** — variável global desnecessária é acoplamento desnecessário.

**Evidência GMS:** o App Checker encontrou **83 variáveis mortas** (15 só no `App`), resíduo direto de iterações sem convenção de escopo — variáveis globais criadas "por garantia" e nunca lidas.

### 1.3 Norma ⚠️ — Renomeação progressiva

Não renomear em massa (risco de quebrar referência em fórmula). A regra é: **tocou na tela, renomeia os controles que a mudança envolve**. A validação de nomes duplicados (`PA1001`) já existente no fluxo de trabalho com Python continua obrigatória antes de todo import de YAML.

---

## 2. Estrutura do App e Fontes de Dados

### 2.1 Norma ⛔ — Teto de fontes conectadas e fim das fontes-fantasma

O app conecta hoje **26 fontes reais + 5 SampleData de template** (`ComboBoxSample`, `RadioSample`, `DropDownSample`, `ListboxSample`, `CustomGallerySample`). As 5 samples devem ser removidas imediatamente — são lixo herdado de template que infla o carregamento das definições.

A documentação oficial recomenda limitar conexões de dados porque cada conector adicional aumenta o tempo de inicialização do app. O GMS está dentro do limite duro, mas a direção é **reduzir** (Frente 2), nunca adicionar lista nova sem antes verificar se uma existente resolve.

**Fonte:** learn.microsoft.com/power-apps/maker/canvas-apps/performance-tips (limite de conexões); auditoria do `References/DataSources.json` do próprio `.msapp`.

### 2.2 Norma ⛔ — Excel Online como fonte viva está proibido para dados transacionais

O GMS tem 3 fontes Excel (`DM_MANDREL`, `DM_BANDAGEM`, `DM_LAYLINE`). A documentação oficial é explícita: o conector Excel tem funções delegáveis muito limitadas e restringe o carregamento a poucos milhares de registros, além de lidar mal com contenção multi-usuário. Excel é aceitável **apenas** como tabela de domínio pequena e raramente alterada (o caso atual dos DMs — dados mestres). A norma:

1. DM_* permanece em Excel **só até a Frente 2** consolidar dados mestres em lista/Dataverse.
2. **Nenhuma fonte Excel nova**, sob nenhuma justificativa.
3. Nenhum `Patch` em fonte Excel — leitura apenas.

**Fonte:** learn.microsoft.com/power-apps/maker/canvas-apps/app-performance-considerations (limitações do conector Excel).

### 2.3 Norma ⛔ — Proibido referência cruzada entre telas

A Microsoft documenta que referências cross-screen (controle da tela A lido pela tela B) forçam o app a carregar e avaliar múltiplas telas simultaneamente, degradando performance e manutenção. A alternativa é passar valores por variável ou coleção.

**Evidência GMS:** o App Checker acusou **7 acoplamentos cruzados entre telas**. Cada um deve ser substituído por `gbl*`/`ctx*` quando a tela for tocada.

**Fonte:** learn.microsoft.com/power-platform/architecture/key-concepts/performance/top-issues.

---

## 3. Padrões de Código Power Fx

### 3.1 Norma ⛔ — `ClearCollect` quando a lógica depende do dado; `UpdateContext` nunca é awaitable

Lição já paga pelo GMS (perda de dados na `scrHoraHora_Trancagem`): `UpdateContext` não espera a leitura do SharePoint terminar antes da próxima linha executar. Onde uma etapa seguinte depende do dado carregado, usar `ClearCollect()` — que é awaitable — e só então prosseguir.

```powerfx
// ❌ ERRADO — a linha 2 pode rodar antes do dado chegar
UpdateContext({ctxFicha: LookUp(ficha_producao, OP = gblOP)});
Patch(ficha_producao, ctxFicha, {status_processo: "Em Processo"});

// ✅ CERTO — ClearCollect conclui antes da próxima instrução
ClearCollect(colFichaAtual, Filter(ficha_producao, OP = gblOP));
Patch(ficha_producao, First(colFichaAtual), {status_processo: "Em Processo"});
```

### 3.2 Norma ⛔ — `App.Formulas` (Named Formulas) para constantes e cálculos derivados; OnStart enxuto

A prática moderna recomendada pela comunidade e pela Microsoft é tirar o máximo possível do `App.OnStart` e mover constantes para Named Formulas — elas são avaliadas sob demanda, sempre atualizadas, e não atrasam o start.

Aplicação direta no GMS — os turnos, hoje `Set()` no OnStart, viram fórmulas nomeadas:

**⛔ [emenda v1.4] Função volátil dentro de Named Formula é PROIBIDA.** A redação anterior desta seção estava errada e produziu bug em produção: `Now()` e `Today()` dentro de uma Named Formula **congelam no primeiro cálculo da sessão**. Num tablet aberto o turno inteiro, `fx_TurnoAtual` continua devolvendo o turno de quando o app abriu — é exatamente o bug do `Set()` no `App.OnStart` que a norma pretendia matar, reencarnado.

**Regra:** Named Formula guarda **constante ou derivação pura**. Toda lógica dependente do tempo vira **UDF com o instante como parâmetro**. Quem fornece o instante é quem chama: um bloco de ação (`Now()` local dentro de `With`) ou um relógio de tela (B §3.11).

```powerfx
// App.Formulas — ✅ CERTO: puras, parametrizadas, sem volátil
// Fronteiras reais do GMS (alinhadas ao Formulas.txt v3.0.5): T1 320–836 min (05:20–13:56) · T2 837–1360 (13:57–22:40) · T3 1361–319 (22:41–05:19)
fx_Turno(minutosDoDia: Number): Number =
    If(minutosDoDia >= 320 && minutosDoDia < 837, 1,
       minutosDoDia >= 837 && minutosDoDia < 1361, 2, 3);

fx_DataRefDe(minutosDoDia: Number): Date =
    DateAdd(Today(), If(minutosDoDia < 320, -1, 0), TimeUnit.Days);

// ❌ ERRADO — congela na primeira avaliação da sessão
// fx_TurnoAtual = With({mins: Hour(Now()) * 60 + Minute(Now())}, ...);
// fx_DataRef    = If((Hour(Now()) * 60 + Minute(Now())) < 320, ...);
```

Uso no bloco de ação, com o instante capturado uma vez e reaproveitado (garante que turno, `data_ref` e carimbo de hora do mesmo Patch nunca discordem entre si):

```powerfx
With({ agora: Now(), min: Hour(Now()) * 60 + Minute(Now()) },
    Patch(ficha_producao, _r, {
        Turno_<Etapa>: Text(fx_Turno(min)),
        data_hora_final_<etapa>: agora
    })
)
```

Isso elimina três classes de bug: o `gblTurnoAtual` congelado (já deprecado no projeto), a lógica de turno duplicada por tela, e a Named Formula volátil descrita acima.

**⚠️ Débito aberto:** `fx_TurnoAtual`, `fx_TurnoAtualLabel`, `fx_DataRef`, `fx_JanelaInicio` e `fx_JanelaFim` ainda existem no `App.Formulas` com volátil dentro (MEL-075). `fx_UltimoIdFicha` acumula dois problemas — volátil não, mas `Sort()` completo sobre `ficha_producao` sem delegação — e `fx_ConsultaOP_Padrao` depende dele (MEL-076).

**Evidência GMS:** o App Checker marcou o `App.OnStart` como o maior foco individual de avisos (6 de delegação + 15 variáveis mortas).

**Fonte:** learn.microsoft.com/power-apps/maker/canvas-apps/create-performant-apps-overview (OnStart sobrecarregado é anti-padrão documentado); matthewdevaney.com — Performance Optimization Guidelines (Named Formulas para constantes no lugar de variáveis).

### 3.3 Norma ⛔ — Data/hora nunca se compara com número

A auditoria confirmou **20 ocorrências** de comparação de tipo incompatível (classe `Now() >= 6`), concentradas em `scr_VolumeDiário_1` (7), `scr_Supervisao_1` (6), `scr_Finalização_1` (3), `scr_mandril_1` (2) e `scrHoraHora_Tubo` (2). É a causa raiz dos totais e da eficiência não baterem na virada de turno/dia.

Padrão único para lógica temporal:

```powerfx
// ❌ ERRADO
If(Now() >= 6 && Now() < 15, ...)

// ✅ CERTO — minutos do dia, ou as fx_ do §3.2
With({mins: Hour(Now()) * 60 + Minute(Now())},
    If(mins >= 360 && mins < 920, ...))
```

E para filtro de data por etapa, a lição já validada no projeto vira norma: **nunca filtrar por `Modified`** — OP que avançou de etapa tem `Modified` atualizado e some do histórico. Usar sempre o `data_hora_final_<etapa>` da própria etapa.

### 3.4 Norma ⛔ — Timers são somente-leitura

Padrão de auto-refresh já validado: `Timer` de 3000–5000 ms, `Repeat: true`, `AutoStart: true`, com `Refresh()`/`LookUp` no `OnTimerEnd`. **Timer nunca executa `Patch`** — escrever em timer cria condição de corrida com a digitação do operador. Das 25 telas, 16 têm timer; todos devem obedecer.

### 3.5 Norma ⚠️ — `Concurrent()` para cargas independentes

Telas que carregam várias fontes na entrada (Bandagem lê 6; Finalização lê 5) devem envolver as cargas independentes em `Concurrent()` — as requisições saem em paralelo em vez de fila:

```powerfx
// OnVisible da scr_Bandagem
Concurrent(
    ClearCollect(colFita,    Filter('Imagens Fitas', Ativo = true)),
    ClearCollect(colLayline, DM_LAYLINE),
    ClearCollect(colColabs,  Filter(Colaboradores, Setor = "Bandagem"))
);
```

**Fonte:** padrão documentado nos guias de performance da Microsoft para reduzir tempo de carga de tela.

### 3.6 Norma ⚠️ — Anti-padrão N+1 em galerias

`LookUp` em fonte externa **dentro de item de galeria** gera uma chamada de rede por linha (50 itens = 51 requisições). A Microsoft documenta esse padrão como um dos principais vilões de performance. Regra: resolver o join **antes**, via `AddColumns` sobre coleção, e a galeria consome a coleção pronta.

**Evidência GMS:** parte dos 34 avisos de delegação de `scr_trançagem_1` e `scr_tubo_1` vem de lookups dentro das galerias de fila.

**Fonte:** learn.microsoft.com/power-platform/architecture/key-concepts/performance/top-issues (Select N+1).

### 3.7 Norma ⚠️ — Tratamento de erro explícito em toda escrita

Todo `Patch`/`SubmitForm` de produção ganha `IfError` com notificação — hoje uma falha de rede no chão de fábrica falha em silêncio e o apontamento se perde:

```powerfx
IfError(
    Patch(ficha_producao, ctxFicha, {quantidade_tubo: Value(inp_Quantidade.Text)}),
    Notify("Falha ao salvar — tente novamente. Se persistir, chame o supervisor.",
           NotificationType.Error)
);
```

### 3.8 Regras de YAML (consolidação das lições GMS) ⛔

Permanecem em vigor as regras já pagas com retrabalho, agora formalizadas:

1. Valores contendo `: ` usam bloco `|-` com prefixo `=`.
2. `RadiusBottomLeft/Right/TopLeft/TopRight` é inválido em `Rectangle@2.3.0`.
3. `Bold` é inválido em `Label@2.5.1` (usar `FontWeight`).
4. `PlaceholderText` → `HintText` em `Classic/TextInput@2.3.2`.
5. `Classic/Spinner` → `Spinner@1.4.6`.
6. Somente versões de controle já provadas no projeto; tipo novo entra incrementalmente e testado. **Lista vigente [v1.4]:**

   | Controle | Versão |
   |---|---|
   | `Classic/Button` | `@2.2.0` |
   | `Classic/TextInput` | `@2.3.2` |
   | `Classic/DropDown` | `@2.3.1` |
   | `Classic/ComboBox` | `@2.4.0` |
   | `Classic/Icon` | `@2.5.0` |
   | `Label` | `@2.5.1` |
   | `Rectangle` | `@2.3.0` |
   | `GroupContainer` | `@1.5.0` |
   | `Gallery` | `@2.15.0` |
   | `Timer` | `@2.1.0` |
   | `Image` | `@2.2.3` |
   | `Spinner` | `@1.4.6` |
   | `HtmlViewer` | `@2.1.0` |
   | `ModernText` | `@1.0.0` |
   | `ModernIcon` | `@1.1.1` |
   | `BarcodeReader` | `@1.0.25` |
   | `Form` / `FormViewer` | `@2.4.4` / `@2.3.4` — legado, ver §3.12 |
   | `TypedDataCard` | `@1.0.7` — legado, só dentro de Form existente |

7. Patch cirúrgico, nunca rewrite; bloco YAML sempre completo.
8. Validação de nome duplicado antes de todo export.
9. **[v1.4] Import de YAML em nível de tela cria tela duplicada.** Consequência prática: para reformar uma tela existente, o YAML entra como **tela nova com nomes de controle novos** (nunca reaproveitar nomes da tela velha, senão `PA1001` durante a coexistência), publica-se, redireciona-se o `Navigate` do router, e só então a tela antiga é excluída. Ajuste pontual em tela existente vai direto na barra de fórmulas, não por import.
10. **[v1.4] Toda fórmula inline que contenha `: ` quebra o parse do YAML** — inclusive `UpdateContext({ctx: valor})` de uma linha só. Regra operacional: fórmula com chaves de registro **sempre** em bloco `|-`, sem exceção para as curtas.
11. **[v1.4] Bateria de QA obrigatória antes de qualquer entrega de YAML** (script Python do projeto): parse PyYAML · `PA1001` duplicados · nome sem espaço (§1.1) · prefixo de tipo (§1.1) · versão de controle nesta lista (§3.8.6) · balanceamento de parênteses/chaves por fórmula · padrões proibidos (§3.3, §3.4) · referência órfã a controle inexistente (§2.3) · zero `RGBA(`/tamanho literal fora dos tokens (§5.2) · zero `Now()` em propriedade que não seja bloco de ação (§3.11).

### 3.9 Norma ⛔ — `BarcodeReader@1.0.25` (bipe de código de barras/QR)

**[v1.3]** Controle moderno, provado em produção (Montagem HoraHora: bipe de P/N, OT e Crachá — base do conceito C35). Lições pagas nesta integração, agora obrigatórias em toda instância nova:

1. **Não aceita `Color` nem `Fill`.** Cor vem do tema global, não é configurável por instância — não tentar setar (gera `PA2108 Unknown property`).
2. **`Self` não resolve dentro do próprio `OnScan`** — limitação conhecida de modern controls. Referenciar o controle **pelo nome**, nunca `Self`.
3. **A saída não é `Self.Value` — é `Barcodes`, uma tabela** (suporta multi-leitura por scan). Padrão de extração obrigatório:
   ```powerfx
   UpdateContext({ctxBipeX: Text(First(bcr_xxx.Barcodes).Value)});
   Reset(txt_campo_x)
   ```
4. O valor bipado alimenta o input via `Default: =ctxBipeX` no `TextInput` correspondente — operador sempre pode digitar por cima.
5. **Toda tela com bipe limpa os `ctx` de bipe no fechamento/reset do fluxo** (ex.: ao finalizar OP) — senão o valor antigo "ressuscita" no próximo `Reset()`, risco direto ao pilar 1 (verdade única).
6. Câmera **não funciona no preview do Studio nem no navegador desktop** — só testa de verdade no Power Apps Mobile/tablet.
7. `BarcodeType.Auto` funciona mas é mais lento pra travar foco; se o código físico é sempre Code 128, usar `BarcodeType.Code128` direto — trava mais rápido.

### 3.10 Norma ⛔ — Estado de etapa é função pura, nunca variável *(v1.4)*

O estado de uma OP dentro de uma etapa **se calcula a partir dos campos gravados**, com uma UDF pura. Nunca se guarda em variável, nunca se infere de propriedade de UI.

```powerfx
// App.Formulas — padrão canônico (instância: Vulcanização)
fx_EstadoVulca(status: Text, inicioResf: DateTime, agora: DateTime): Text =
    If(
        status <> "Em processo", "AGUARDANDO",
        IsBlank(inicioResf),     "VULCANIZANDO",
        "RESFRIANDO"
    );
```

Três consequências obrigatórias:

1. **Poka-yoke nunca depende de `Visible`.** Se uma ação não pode acontecer, ela some **e** a coleção que a alimenta não contém o registro. Uma barreira só é meia barreira. Evidência: na `scr_Vulcanização_1` v0.1.3 era possível enviar OP para a Debandagem **sem ter acionado o resfriamento**, porque a elegibilidade morava apenas no `DisplayMode` de um botão.
2. **Proibido derivar lógica de texto de interface.** `If(Label_Status.Text = "🟢", ...)` é referência a pixel, não a dado: quebra em qualquer troca de rótulo e é ilegível em auditoria. Ler sempre o campo (`status_processo`).
3. **Proibido comparar `DisplayMode` ou `Visible` de outro controle** para decidir gravação.

### 3.11 Norma ⛔ — Relógio de tela: `Now()` só em bloco de ação *(v1.4)*

`Now()` dentro de propriedade de exibição (`Text`, `Visible`, `Fill`, `Color`) recalcula em cadência imprevisível e força reavaliação em cascata na galeria inteira. Padrão único:

```powerfx
// tmr_Relogio<Tela> — AutoStart: true · Repeat: true · Duration: 30000 · Visible: false
OnTimerEnd: =UpdateContext({ctxAgora: Now()})
// OnVisible da tela inicializa: UpdateContext({ctxAgora: Now()})
```

Toda propriedade de exibição consome `ctxAgora`; `Now()` literal aparece somente dentro de `OnSelect`/`OnVisible`/`OnTimerEnd`. Cadência: 30 s para cronômetro em minutos, 1 s só quando a tela exibe segundos. Compatível com §3.4 (o timer continua somente-leitura).

### 3.12 Norma ⚠️ — `Form`/`TypedDataCard` são legado; entrada nova usa controles diretos *(v1.4)*

O controle `Form` produz o bug "No item to display" quando o item vinculado está em branco, obriga o `DisplayName` a vir do schema (colidindo com §5.3) e infla o YAML em ~10× por campo. **Tela nova ou reformada usa controles de entrada individuais** (`inp_`, `cmb_`, `rad_`) com `Patch` direto e verificação de `Errors()` (§3.7). `Form` existente permanece até a tela ser tocada (§1.3, migração progressiva).

### 3.13 Norma ⛔ — Escopo aninhado usa `As`; nome de coluna nunca entre aspas *(v1.5)*

Dois erros **silenciosos** — a tela renderiza, os números vêm errados — pagos na implementação do C36:

1. Dentro de `AddColumns`/`ForAll`, um `LookUp`/`Filter` aninhado faz `ThisRecord` resolver para o **escopo interno**, não para a linha externa. Toda iteração aninhada declara alias: `ForAll(colX As _x, ... LookUp(colY, campo = _x.campo) ...)`.
2. Nome de coluna entre aspas duplas compila como **literal de texto** e a comparação avalia sempre falso, sem erro no App Checker.

Como ambos falham em silêncio, a validação é obrigatoriamente **numérica**: conferir o resultado contra o CSV export antes de publicar (§7.2.5), nunca "a tela abriu, então está certo".

---

## 4. Dados e Delegação (SharePoint)

### 4.1 Contexto do risco

`ficha_producao` tem 1.176 linhas × 103 colunas e cresce todo dia. A auditoria acusou **177 avisos de delegação**, com os focos em Trançagem (34), Tubo (34), Cobertura (27), Supervisão (20) e Finalização (11). O comportamento documentado do SharePoint: consulta não-delegável traz só os primeiros 500 registros (configurável até 2.000) e **ignora silenciosamente o resto** — o número parcial parece completo.

### 4.2 Normas

⛔ **Data row limit em 2.000** nas configurações do app (mitigação imediata, não solução).

⛔ **Filtro delegável primeiro, refinamento depois.** O padrão validado do GMS continua correto — `Filter(ficha_producao, processo = "Tubo")` é delegável e retorna conjunto pequeno; refinamentos não-delegáveis (`Search`, `in`, data complexa) aplicam-se **depois**, sobre a coleção local:

```powerfx
ClearCollect(colEtapa, Filter(ficha_producao, processo = "Tubo"));       // delegável, roda no servidor
ClearCollect(colFila,  SortByColumns(Filter(colEtapa, IsBlank(data_hora_final_tubo)), "OP"));  // local, seguro
```

⛔ **Colunas de filtro indexadas no SharePoint.** `processo`, `status_processo`, `OP` e os `data_hora_final_*` mais consultados devem ter índice de coluna criado na lista (até 20 índices por lista). Sem índice, `Filter`/`LookUp` param de avaliar além do item 5.000.

⚠️ **Preferir tipos delegáveis no schema**: texto simples, número, data. Evitar Choice/Lookup/Person em coluna que será filtrada — Choice só delega com `=`, e Lookup gera chamadas extras. (Insumo direto para o desenho da Frente 2.)

⚠️ **`StartsWith` no lugar de `Search`** para busca digitada (ConsultaOP): `StartsWith` é delegável no SharePoint, `Search` não.

**Fontes:** learn.microsoft.com/power-apps/maker/canvas-apps/delegation-overview; matthewdevaney.com — SharePoint Delegation Cheat Sheet; practicalpowerapps.com — Delegation.

### 4.3 Norma estrutural (ponte para a Frente 2)

Remendo de fórmula tem teto. A solução estrutural para os 177 avisos é a consolidação/normalização das fontes (menos colunas por lista, filtros nativos delegáveis) e, no horizonte já identificado do projeto, **Dataverse** — que suporta muito mais operadores delegáveis que o SharePoint. Este guia padroniza o presente; a Frente 2 corrige a causa.

---

## 5. Design System GMS

### 5.1 Decisão de fundação ⛔ — O padrão Montagem é o canônico

A auditoria identificou **4 linguagens visuais** convivendo. O padrão do módulo Montagem (o mais novo) vence por três motivos objetivos: é o único sem vazamento de nome interno de coluna, é bipe-first (menos digitação), e sua hierarquia visual é a mais limpa. Todas as telas convergem para ele quando forem tocadas.

### 5.2 Tokens de design ⛔

Definidos uma vez em `App.Formulas`, consumidos em toda propriedade visual. **Proibido hardcode de cor/tamanho/raio em controle:**

```powerfx
// App.Formulas — design tokens GMS
fx_CorPrimaria   = ColorValue("#E2231A");   // Danfoss red — só para marca e alerta máximo
fx_CorFundo      = ColorValue("#F5F7FA");
fx_CorSuperficie = Color.White;
fx_CorTexto      = ColorValue("#0F172A");
fx_CorTextoSuave = ColorValue("#64748B");
fx_CorOK         = ColorValue("#16A34A");
fx_CorAlerta     = ColorValue("#E67E22");
fx_CorErro       = ColorValue("#C0392B");
fx_CorInfo       = ColorValue("#2C6FBF");

fx_FonteTitulo   = 22;
fx_FonteSecao    = 15;
fx_FonteCorpo    = 13;
fx_FonteApoio    = 11;

fx_Raio          = 12;   // raio padrão de card
fx_EspacoS       = 8;
fx_EspacoM       = 16;
fx_EspacoL       = 24;
```

**[v1.4] Paleta e escala completas.** A base acima cobria marca e semântica, mas não superfície, hierarquia de rótulo nem estado físico — o que empurrava toda tela nova de volta ao `RGBA()` literal. Tokens complementares, obrigatórios:

```powerfx
// Superfície e estrutura
fx_CorHeader        = ColorValue("#1E293B");   // faixa escura (cabeçalho de fila)
fx_CorBorda         = ColorValue("#E2E8F0");   // borda de card e divisor
fx_CorRotulo        = ColorValue("#94A3B8");   // rótulo de campo (mais claro que TextoSuave)
fx_CorChip          = RGBA(122, 138, 143, 0.36); // chip sobre superfície escura
fx_CorOverlayForte  = RGBA(0, 0, 0, 0.7);        // scrim de gravação (spinner)

// Tons suaves — fundo de badge e de linha selecionada
fx_CorInfoSuave     = ColorValue("#EFF6FF");
fx_CorOKSuave       = ColorValue("#D1FAE5");
fx_CorAlertaSuave   = ColorValue("#FEF3C7");
fx_CorErroSuave     = ColorValue("#FEE2E2");

// Estado físico: processo em curso que não é produção (resfriamento, cura, repouso)
fx_CorGelo          = ColorValue("#0284C7");
fx_CorGeloSuave     = ColorValue("#E0F2FE");

// Tipografia — os fx_Fonte* são TAMANHO; a família ganha token próprio
fx_FonteFamilia  = Font.'Open Sans';
fx_FonteDestaque = 16;   // valor de campo em card
fx_FonteNumero   = 28;   // contador grande
fx_FonteReceita  = 32;   // parâmetro de processo em modal
fx_FonteCrono    = 40;   // cronômetro de ficha

// Raios
fx_RaioS = 8;    // botão, linha de lista
fx_RaioG = 16;   // modal
```

**Named Formulas de layout.** `fx_BalizaTam` (tamanho da baliza) e `fx_LayoutBalizas` (tabela de posições em %, colunas `id, nome, etapa_gms, Trançadeira, tranc, temFila, px, py, fx, fy`) são parte do padrão desde o C36 — posição de elemento sobre imagem de planta é **dado**, não coordenada hardcoded em controle.

**Armadilha de nomenclatura, registrada para não se repetir:** `fx_Fonte*` significa **tamanho**, não família. Nome de fonte é `fx_FonteFamilia`. E `fx_CorPrimaria` é o **vermelho Danfoss** — serve de acento de marca (card ativo da fila) e **não** de cor de botão de ação: vermelho em chão de fábrica lê como *parar*. Ação primária usa `fx_CorInfo`.

Isso replica em Power Fx a prática de temas centralizados que a Microsoft empurra com o theming moderno — e prepara a migração futura para Modern Controls + `App.Theme`, onde o tema vive num único lugar e todos os controles herdam. **Nota v1.2:** o 2025 wave 2 tornou modern controls, layout responsivo e offline o *default* de apps novos da plataforma — a direção está confirmada; o GMS migra no seu ritmo (MEL-063), com os tokens `fx_` como ponte.

**Fonte:** learn.microsoft.com/power-apps/maker/canvas-apps/controls/modern-controls/modern-theming; michaelharley.net — Power Apps Naming Convention (tokens `fx_`).

### 5.3 Norma ⛔ — Rótulo limpo em PT-BR; schema nunca aparece pro operador

A auditoria fotografou `operador_vulcanizacao`, `quantidade_debandagem`, `diametro_co...`, `quantidade_bandag...`, `Cód_Fita_Bandagem`, `Código_Filme_UHMWPE` como labels visíveis. Norma: **todo DataCard tem `DisplayName` humano**, título em caixa normal, sem underscore, sem truncamento. O nome interno da coluna é assunto do desenvolvedor, nunca do operador. (O módulo Montagem prova que o padrão é atingível: "Part Number", "Crachá do Operador".)

### 5.4 Norma ⛔ — Alvos de toque de chão de fábrica

Operador usa o app em pé, às vezes de luva, em tablet. Botões de ação primária (Iniciar/Salvar/Enviar/Registrar): **altura mínima 48 px, área de toque ≥ 48×48**; espaçamento ≥ `fx_EspacoM` entre alvos adjacentes. A própria Microsoft passou a aplicar touch targets maiores como default mobile nos Modern Controls — o GMS antecipa a regra nos Classic.

**Fonte:** microsoft.com/power-platform/blog — quality updates to modern controls (defaults mobile com alvos de toque maiores).

**[v1.5] Adendo mobile ("regra de luva").** Em telefone, a ação primária sobe para **56 px**. Além disso: zero dropdown acima de 7 itens (vira bipe ou campo de busca); stepper `+`/`−` no lugar de teclado numérico onde o valor é pequeno e discreto; `AccessibleLabel` em **todo** input — hoje não existe em nenhum controle do GMS.

### 5.5 Norma ⛔ — Contraste e acessibilidade

Contraste texto/fundo ≥ **4.5:1** (WCAG AA), regra explícita da documentação de acessibilidade do Power Apps. Impacto direto no GMS: os formulários desabilitados hoje usam cinza-sobre-cinza com contraste insuficiente (prints de Vulcanização/Debandagem). Estado desabilitado usa `fx_CorTextoSuave` sobre `fx_CorSuperficie`, nunca cinza sobre cinza.

Complementos da doc oficial: todo controle de entrada com `AccessibleLabel` definido; pelo menos um heading por tela (Role de Label); `TabIndex` 0 apenas em interativos.

**Fonte:** learn.microsoft.com/power-apps/maker/canvas-apps/accessible-apps.

### 5.6 Norma ⛔ — Datas e números em padrão BR único

A ficha de impressão mistura `July 3, 2026` com `29/06/26`. Norma: `Text(data, "dd/mm/yyyy")` em toda exibição; `Text(data, "dd/mm/yyyy hh:mm")` quando houver hora; separador decimal vírgula na exibição (`Text(valor, "#.##0,0")` via Language()). Proibido default fantasma `12/31/2001` em DatePicker — default é `Blank()` com campo obrigatório validado, ou `fx_DataRef`.

### 5.7 Estados visuais padronizados ⛔

Todo elemento de status usa o mesmo mapa semântico (já parcialmente adotado nos cards de fila):

| Estado | Cor | Uso |
|---|---|---|
| Em processo (selecionado) | `fx_CorPrimaria` fundo, texto branco | Card ativo da fila |
| Aguardando | `fx_CorAlerta` (ponto/badge) | Fila |
| Concluído/OK | `fx_CorOK` | Resumo, confirmações |
| Erro/refugo | `fx_CorErro` | Refugo, falha de Patch |
| Informativo | `fx_CorInfo` | Links, metadados, **botão de ação primária** |
| **[v1.4]** Processo físico em curso (resfriamento/cura/repouso) | `fx_CorGelo` fundo `fx_CorGeloSuave` | Badge de fila, cronômetro, botão de transição |

Cronômetro de card ganha **teto visual**: acima de 24 h exibe "‹ +24 h ›" com badge `fx_CorAlerta` em vez do contador absoluto (mata o "4162:41" da OP zumbi como sintoma visível; a causa entra no Andon — conceito C1).

### 5.8 Norma ⛔ — Ícone sobre botão nunca duplica lógica *(v1.4)*

Padrão recorrente no GMS: um `Classic/Button` com o rótulo e um `Image`/`Icon` posicionado por cima para compor o visual. O ícone captura o clique. **O `OnSelect` do ícone deve ser exclusivamente `Select(btn_Alvo)`** — nunca uma cópia da lógica.

**Evidência:** em `scr_Vulcanização_1` v0.1.3, `Btn_play_5.OnSelect` abria o modal de Set-up Delineamento, enquanto o `Play_5` sobreposto executava `Patch` de início direto. Como o ícone estava por cima, o modal **nunca abria em produção**: toda OP iniciava sem passar pelo set-up, sem `Turno_Vulcanização` e sem evento em `Eventos_Producao`. Lógica duplicada não diverge "talvez" — ela diverge.

### 5.9 Norma ⛔ — Densidade: espaço vazio é bug de layout *(v1.4)*

Modal ou card cujo conteúdo ocupa menos de ~60% da área desenhada deve ser redimensionado ao conteúdo, não preenchido com caixas vazias. **Evidência:** o modal de Set-up Delineamento da Vulcanização ocupava 1193×705 px para exibir dois valores (tempo e temperatura), com três containers vazios reservados para campos que a etapa não tem. Reduzido a 560×390 com dois cards de valor. Regra prática: modal dimensionado pelo conteúdo real da etapa, e o que a etapa não possui simplesmente não aparece.

---

## 6. Templates de Tela

Três templates cobrem 90% do GMS. Tela nova **deve** nascer de um deles; tela antiga converge ao ser tocada.

### 6.1 Template A — Ficha de Etapa (linha de produção)
Estrutura validada nos prints, agora formalizada:

```
┌──────────────┬──────────────────────────────┬───────────────┐
│ FILA (280px) │ FICHA (flex)                 │ LATERAL(220px)│
│ gal_Fila     │ ctn_DadosOrdem (read-only)   │ btn_EditarOP  │
│ card ativo   │ ctn_EntradaDados (form)      │ btn_HoraHora  │
│ vermelho +   │                              │ ctn_Resumo    │
│ cronômetro   │                              │  Turno        │
├──────────────┴──────────────────────────────┴───────────────┤
│ tmr_AutoRefresh · btn_Iniciar · btn_Salvar · btn_Enviar     │
└──────────────────────────────────────────────────────────────┘
```

Regras do template: fila só leitura; máquina de estados dos botões (`Iniciar` habilita → `Salvar`/`Enviar`); `Enviar` sempre com confirmação quando finaliza etapa; resumo do turno alimentado pelo relógio de tela (`fx_Turno(min)` sobre `ctxAgora`, §3.11).

#### 6.1.1 Template A′ — Ficha de Etapa sem apontamento (batelada) *(v1.4)*

Variante obrigatória quando a etapa se enquadra em **C39** (não gera metragem própria, o operador aciona transições). Implantação de referência: `scr_Vulcanizacao_2` v0.2.0.

```
┌──────────────┬──────────────────────────────────────┬───────────────┐
│ FILA (315px) │ ctn_DadosOrdem (4 campos read-only)   │ LATERAL(222px)│
│ card ativo   ├───────────────────────┬──────────────┤ btn_EditarOP  │
│ fx_CorPrima. │ ctn_Situacao          │ ctn_Resumo   │               │
│ + badge de   │  stepper 3 fases      │  T1/T2/T3    │               │
│   estado     │  cronômetro grande    │  elegíveis   │               │
│ + cronômetro │  receita + alerta     │              │               │
├──────────────┴───────────────────────┴──────────────┴───────────────┤
│ ico_Refresh   ·   btn_Acao  ← ÚNICO botão, texto/cor/ação = estado  │
└──────────────────────────────────────────────────────────────────────┘
```

Regras do A′:
1. **Zero campo de entrada na ficha.** O que a etapa não mede, ela não pergunta.
2. **Um único botão de ação**, com `Text`, `Fill` e `OnSelect` em `Switch` sobre a UDF de estado (§3.10). Cada fase tem exatamente uma ação possível, então não há como errar a ordem.
3. **Stepper de 3 fases** substitui o bloco "ENTRADA DE DADOS": o operador vê onde está, não onde digitar.
4. **Quantidade herdada, exibida com a origem** ("675 m recebidos da Bandagem"), nunca editável na rotina.
5. **Identificação do operador só no fechamento do lote**, no modal de envio.
6. **Receita do Delineamento visível** (C26) com alerta quando o ciclo real ultrapassa o especificado.
7. **Modal de lote alimentado por coleção materializada** com o filtro de elegibilidade aplicado localmente, e mensagem explícita quando vazia — nunca lista vazia sem explicação.

### 6.2 Template B — Apontamento Hora-Hora
Herda o layout do Montagem (2 colunas Produção | Paradas), substituindo a grade manual de 11 linhas. Meta e Real derivados (ver conceito C13); operador confirma paradas e motivos. Uma única tela parametrizada por célula — como Montagem já faz com 13 células — no lugar de 1 tela por área.

### 6.3 Template C — Registro Rápido (refugo, catenária, movimentos)
Formulário à esquerda (máx. 7 campos), tabela "registros do dia" à direita, botão único `Registrar`. Combos com estilo do design system (nunca `Find items` cru). Já é a estrutura da Refugo Bobinadeira — falta só o skin.

### 6.4 Template D — Mobile: uma coluna, uma tarefa *(v1.5)*

O Template A é 315 px + flex + 222 px. Em tela de 6" isso é inutilizável, e converter as 25 telas existentes para layout responsivo é **rewrite — proibido (P3)**. Daí a regra: **Template D vale só para tela nova; tela antiga não é convertida.**

Estrutura: cabeçalho fixo (OP · etapa · turno), corpo rolável com **no máximo 5 campos**, rodapé fixo com **uma** ação primária. Implementação: *Scale to fit* desligado em Settings > Display, `Container` com `FillPortions` e `App.SizeBreakpoints`.

**Duas travas antes de liberar apontamento no celular:**
1. **O problema do mobile é navegação, não layout.** Rolar uma fila de 28 itens num telefone é pior que o desktop, por melhor que seja o layout. A solução é o bipe (C35) sobre a `fFluxoEtapas` autoritativa (C40): abre o app → câmera → bipa a OP → o sistema descobre em que etapa ela está e abre a tela certa com a OP carregada. Zero menu, zero rolagem. **É onde C35 e C40 se encontram.**
2. **⛔ Não liberar apontamento mobile antes da MEL-057 (fila offline / C34).** Wi-Fi de chão de fábrica sem fila de escrita faz o mobile **piorar** a confiabilidade do dado — fere o pilar 1, que é justamente o que o mobile deveria servir.

---

## 7. Qualidade e Governança

### 7.1 Norma ⛔ — App Checker limpo em tela nova

Tela nova publica com **zero** erro de tipo, **zero** referência cruzada e delegação justificada por comentário quando inevitável. As 2.854 pendências do legado entram no Backlog Mestre (Parte D), não bloqueiam operação.

### 7.2 Checklist pré-publicação ⛔

1. Nome duplicado (`PA1001`) — script Python existente.
2. App Checker: aba Performance e Regras sem itens novos.
3. Teste de virada de turno: forçar horário 05:19/05:21 e 15:19/15:21 e conferir `fx_TurnoAtual`/`fx_DataRef`.
4. Teste offline curto: derrubar rede, tentar Salvar, conferir `IfError` notificando.
5. Validação contra CSV export (pipeline Python já validado no projeto).
6. Commit message no publish descrevendo a mudança (o campo já existe e está vazio no histórico — "Versão 1.2 hora-hora montagem" foi exceção, deve ser regra).
7. **[v1.4] Bateria de QA de YAML** (§3.8.11) verde antes do import.
8. **[v1.4] Teste de barreira dupla:** para cada ação irreversível da tela, confirmar que a restrição existe **na coleção de dados** e não só no `DisplayMode`/`Visible` (§3.10.1).
9. **[v1.4] Teste de ícone sobreposto:** clicar em cada ícone que estiver sobre botão e confirmar que dispara a mesma ação do botão (§5.8).
10. **[v1.4] Teste de sessão longa:** app aberto > 1 h atravessando virada de turno, conferindo que turno e `data_ref` acompanham (caça Named Formula volátil, §3.2).

### 7.3 Norma ⚠️ — Higiene contínua

A cada sprint de manutenção: remover variáveis mortas da tela tocada (83 mapeadas), remover mídia órfã (apontada pelo Checker), remover as 5 fontes Sample no primeiro ciclo.

### 7.4 Norma ⚠️ — Git Integration como ALM oficial (emenda v1.2)

A integração Git da Power Platform está **GA desde abril/2025**: o source do canvas app sincroniza com repositório Git — histórico de mudanças, pull request, CI/CD — oficialmente suportado. Isso **profissionaliza o fluxo que o GMS já faz na mão** (export YAML → validação Python → import): o mesmo pipeline de validação (PA1001, YAML rules do §3.8) passa a rodar sobre o repositório, e cada publish vira commit rastreável. Adoção: ativar a sincronização no ambiente, apontar para repo Azure DevOps/GitHub, migrar os scripts Python para rodarem no repo. O fluxo manual continua válido até a ativação.

**Fonte:** anúncio de GA da Git integration (Power Platform, abril/2025); release plan 2025 wave 2 (code management no Studio para apps enterprise).

### 7.5 Ferramentas de diagnóstico

**Monitor** (Power Apps Studio) passa a ser a ferramenta padrão para investigar lentidão — mostra cada chamada de rede em tempo real e expõe N+1 e payload gordo imediatamente. Sessão de Monitor é obrigatória antes de culpar "o SharePoint".

**Fonte:** learn.microsoft.com/training/paths/improve-app-performance (Monitor tool).

---

## 8. Plano de Adoção — ordem de ataque *(superado pela Parte D — mantido como referência histórica dos números)*

Sequência que maximiza retorno por esforço, usando os números da auditoria:

| # | Ação | Alvo | Esforço | Retorno |
|---|---|---|---|---|
| 1 | Excluir `scrHoraHora_Tubo` (órfã) + 5 fontes Sample | app | Baixo | Remove tela quebrada e lixo de template |
| 2 | Corrigir os 20 bugs de tipo (`Now()>=6`) migrando para `fx_TurnoAtual`/`fx_DataRef` | VolumeDiário, Supervisão, Finalização, Mandril | Médio | **Números do BI passam a bater** — maior ganho de confiança do sistema |
| 3 | Trocar filtros por `Modified` → `data_hora_final_<etapa>` | VolumeDiário, Supervisão | Baixo | Corrige subcontagem histórica |
| 4 | Rótulos limpos + datas BR + default `Blank()` | 8 telas da linha | Baixo | Ganho visível pro operador no dia 1 |
| 5 | Design tokens em `App.Formulas` + skin dos botões/estados | app | Médio | Fundação do design system |
| 6 | `Concurrent()` + eliminação de N+1 nas 5 telas de delegação alta | Trançagem, Tubo, Cobertura, Supervisão, Finalização | Médio | Corta os piores dos 177 avisos |
| 7 | Índices de coluna no SharePoint (`processo`, `OP`, `data_hora_final_*`) | listas | Baixo | Protege contra o crescimento da `ficha_producao` |
| 8 | Unificação do Hora-Hora no Template B | 3 telas → 1 | Alto | Mata digitação dupla; depende da Frente 2 p/ fonte única |
| 9 | Limpeza contínua (variáveis mortas, mídia órfã, renomeação progressiva) | app | Diluído | Manutenibilidade |

Itens 1–4 são um único ciclo curto de trabalho e entregam o maior salto de confiabilidade percebida do GMS desde o go-live.

---

## 9. Referências

**Documentação oficial (Microsoft Learn / Power Apps):**
- Performance considerations for Power Apps — `learn.microsoft.com/power-apps/maker/canvas-apps/app-performance-considerations`
- How to create performant Power Apps — `learn.microsoft.com/power-apps/maker/canvas-apps/create-performant-apps-overview`
- Identify and mitigate canvas app performance issues (cross-screen, N+1) — `learn.microsoft.com/power-platform/architecture/key-concepts/performance/top-issues`
- Understand delegation in a canvas app — `learn.microsoft.com/power-apps/maker/canvas-apps/delegation-overview`
- Code readability best practices — `learn.microsoft.com/power-apps/guidance/coding-guidelines/code-readability`
- Application design guidelines (modern controls, forms, containers, galerias) — `learn.microsoft.com/power-apps/guidance/coding-guidelines/app-design-guidelines`
- Modern controls & theming — `learn.microsoft.com/power-apps/maker/canvas-apps/controls/modern-controls/overview-modern-controls`
- Create accessible canvas apps — `learn.microsoft.com/power-apps/maker/canvas-apps/accessible-apps`
- Training path: improve app performance (Monitor) — `learn.microsoft.com/training/paths/improve-app-performance`

**Fronteira 2026 (emenda v1.2):**
- Power Apps 2025 release wave 2 overview (modern/responsive/offline por default; Copilot; agent-first; Plan Designer; agent apps) — `learn.microsoft.com/power-platform/release-plan/2025wave2/power-apps/`
- Power Platform 2025 wave 2 (Dataverse MCP Server, Dataverse for Agents, governança de agentes; Power Automate generative actions + human-in-the-loop) — `learn.microsoft.com/power-platform/release-plan/2025wave2/`
- Generative pages GA (GPT-5, model-driven, EUA) — blog Power Platform, nov/2025
- Git integration GA (source control oficial p/ canvas) — Power Platform, abr/2025
- Dataverse AI functions no Power Fx (`Environment.AIClassify/AISummarize/AIExtract/...`) — `learn.microsoft.com/power-platform/power-fx/reference/function-ai`
- Offline canvas: Dataverse 1-toque (SharePoint não suportado no offline moderno); padrões SaveData/LoadData — `learn.microsoft.com/power-apps/mobile/limitations-canvas-apps` + `.../maker/canvas-apps/offline-apps`

**Comunidade:**
- Matthew Devaney — Power Apps Coding Standards for Canvas Apps (2024) e SharePoint Delegation Cheat Sheet — `matthewdevaney.com`
- Microsoft — PowerApps Canvas App Coding Standards and Guidelines (white paper oficial)
- Practical Power Apps — Delegation series — `practicalpowerapps.com`
- Michael Harley — naming convention com tokens `fx_` — `michaelharley.net`

**Interno GMS:**
- Auditoria `.msapp` v2026-06-22 + App Checker SARIF (2.854 apontamentos)
- `GMS_Frente1_Mapeamento_Telas.md` (mapeamento de telas) e `GMS_Mapa_Navegacao.pdf`
- Lições validadas em produção: UpdateContext não-awaitable, timers read-only, `Modified` não confiável, fronteira do 3º turno (05:20), regras de YAML do PA Source Code

---

---

# PARTE D — BACKLOG

**O backlog não mora mais neste arquivo.** Ele é derivado do `GMS_Diario.md`:

```bash
python3 gms.py --backlog        # tudo, agrupado por fase
python3 gms.py --backlog F0     # só a fundação
python3 gms.py --estado         # telas, aguardando publish, pendências, normas fora do Mestre
python3 gms.py --mel 073        # histórico completo de um item
python3 gms.py --novo           # próximo ID livre + linha modelo pra colar
```

## Regras do backlog (estas continuam sendo norma)

1. **Fase 0 antes de fase 1** é inegociável: conceito bonito sobre número errado destrói confiança (pilar 1). Dentro da fase, a ordem é guia, não lei.
2. **Item novo:** `gms.py --novo` dá o próximo ID. Nunca reusar ID, nunca renumerar.
3. **Item muda de estado com linha nova**, jamais editando a linha antiga. `ABERTO → ENTREGUE → PUBLICADO → VALIDADO` é o caminho feliz; `REVERTIDO` e `DESCARTADO` existem e são legítimos.
4. **Fases:** `#F0` correção/fundação · `#F1` conceitos H1 · `#F2` conceitos H2 (dependem da Frente 2/Factbird) · `#F3` visão.
5. **Conceito ou MEL citado em conversa e não escrito no diário não existe.** Lição de governança paga na v1.5: ele reaparece como "ID reservado" e trava a numeração.
6. O pacote mínimo de maior retorno segue sendo **MEL-001→004** num único ciclo curto: é o que faz os números do BI baterem.

---

# CHANGELOG

Também vive no diário, como linhas `NORMA` com alvo `GMS_Mestre`:

```bash
grep "NORMA | GMS_Mestre" GMS_Diario.md
```

O histórico das versões 1.0 a 1.5 foi migrado para lá na criação da v2.0.
