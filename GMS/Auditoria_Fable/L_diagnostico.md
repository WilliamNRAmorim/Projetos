# Missão L: diagnóstico de layout e eficácia (BI, app e fluxos)

Data: 10/11/2026. Quem fez: sessão Fable, a partir do `BRIEF_FABLE_L_P2.md`.
Nada foi alterado em produção. Tudo aqui é leitura dos arquivos do repositório e proposta.

Mockup antes/depois: `L_mockup_antes_depois.png` (gerado por `gerar_mockup_L.py`; é esquema com valores de exemplo, não print da tela).

## Como ler este documento

- **Medido** quer dizer que saiu de um script sobre os arquivos (`GMS_Painel.Report`, `Telas/*.txt`, `definition.json` dos fluxos).
- **Conferir no PC da fábrica** quer dizer que o arquivo sugere o problema, mas só o modelo vivo, a lista do SharePoint ou o tablet confirmam.
- Prioridade: **P1** atrapalha a decisão ou pode parar algo; **P2** custa tempo todo dia; **P3** acabamento.
- Itens marcados **[revisor]** tocam regra de parada, turno ou norma e passam pelo `revisor` antes de virar mudança.

## Resumo: os 5 achados de cada frente

**Power BI**
1. A Visão Geral não diz se o dia está bom ou ruim: 6 cartões da mesma cor, sem meta, com variação só contra o mês anterior.
2. A cor padrão de toda série é o vermelho da marca. Quase todo gráfico sai vermelho e a exceção não aparece.
3. Nenhuma das 10 páginas tem layout para celular.
4. Texto pequeno: 123 ocorrências de 9 pt e 7 de 8 pt (eixos, rótulos de dado, variação).
5. Segmentação de Turno e de Período muda de lugar, de tipo e de tabela conforme a página, e parte delas não acompanha a navegação.

**Power Apps**
1. Ações em ícone de 24 × 24 px (editar e excluir lance, imprimir, dividir pallet) com 6 px de vão entre elas.
2. Texto de apoio em 11 e corpo em 13, com rótulo cinza de contraste 2,6:1, usado 584 vezes.
3. `App.OnError` está vazio: erro não tratado aparece ao operador como faixa técnica.
4. Gravações longas com 5 a 7 `Patch` em sequência no mesmo botão (Mandril), sem volta se a rede cair no meio.
5. Lista de mangueiras e trançadeiras escrita à mão no `OnStart`: mangueira nova exige publicar o app.

**Power Automate**
1. `GMS_PlanoOPs_Sync` olha a pasta `Plano Trançadeira/2026`, escrita à mão. Em 01/01/2027 ele para sem avisar.
2. `Monitor Solda Mandril` lê `DM_Velocidade` sem Top Count: vêm só as 100 primeiras linhas.
3. `GMS_PlanoOPs_Sync` e `GMS_Tempos_Sync` leem a lista de destino com Top 5000 sem paginação: acima disso o sync cria duplicata.
4. `Monitor Solda Mandril` e `GMS_AutoResfriamentoVulca` não avisam quando falham, e a tela do Monitor não mostra a idade do dado.
5. `GMS_Conferencia_Diaria` manda o e-mail de falha, mas a execução termina verde no histórico.

A unidade da hora de parada do Monitor está respondida na seção 3.2: o fluxo trata a velocidade como **metros por hora**.

---

## 1. Power BI (`GMS/PowerBI/GMS_Painel.pbip`)

Medido: 10 páginas de 1280 × 720, 166 visuais, tema `GMS_Tema.json`. O layout salvo não foi tocado.

### O que já está bom
- Toda página mostra "Dado atualizado até".
- A página **Hora-Hora Trançagem** é a melhor do arquivo: Meta, Real, Aderência, Parado e Principal parada no topo, um gráfico grande Real × Meta e os motivos ao lado.
- As páginas de Refugo já usam título em forma de pergunta.
- Pareto e barras de motivo estão ordenados por valor.

### B1 (P1). A Visão Geral não responde "como está agora"
- Medido: 6 cartões (`kpi0` a `kpi5`) com valor em `#1F2937`, nenhum com cor condicional. Quatro têm variação "vs mês ant." em 11 pt com rótulo de 8 pt. Não há meta em nenhum cartão.
- O que o supervisor vê em 5 s: seis números do mesmo peso, sem saber qual está fora.
- Proposta: 5 cartões, cada um com valor, comparação contra a meta do dia e uma barra de estado (verde, laranja, vermelho, sempre com seta e texto). Visual principal: "Qual etapa está mais longe da meta agora?" (Real × Planejado por etapa, a pior em destaque). Apoio: os motivos de parada do dia e a linha do dia contra a meta. É o quadro "DEPOIS" do mockup e segue a Parte D.1 e D.2 do `GMS_Mestre_BI.md`.
- Depende de: medidas de meta do dia e de estado (DAX). Validar no PC da fábrica.

### B2 (P1). Vermelho como cor padrão de série
- Medido: `dataColors[0] = #E30613` no tema, e só 6 dos 30 gráficos definem cor própria. Os outros herdam o vermelho. No tema, `bad` também é `#E30613`.
- A norma B.6.1 do Mestre BI proíbe exatamente isso ("vermelho em barra lê como tudo errado").
- O tema também diverge dos tokens do app: `#E30613` contra `#E2231A`, verde `#0F766E` contra `#16A34A`, fundo `#F3F4F6` contra `#F5F7FA` (as páginas Fluxo usam `#F6F5F2`).
- Proposta: trocar só o `GMS_Tema.json` (um arquivo): primeira cor `#2C6FBF`, `good #16A34A`, `neutral #E67E22`, `bad #C0392B`. Não mexe em posição nem tamanho de nada.
- Precisa do "sim": muda a aparência do relatório publicado.

### B3 (P1). Sem layout para celular
- Medido: 0 arquivos `mobile.json` em 10 páginas.
- Efeito: no app do Power BI no celular, a página de 1280 px encolhe para cerca de 360 px. O texto de 9 pt fica perto de 2,5 pt.
- Proposta: layout móvel só para Visão Geral e Hora-Hora (4 cartões em grade 2 × 2 e dois gráficos empilhados). O layout móvel é separado do layout de mesa, então o layout salvo continua igual.
- Precisa do "sim" e do Desktop no PC da fábrica.

### B4 (P2). Texto pequeno
- Medido: eixos e rótulos de dado em 9 pt (123 ocorrências), rótulo de variação em 8 pt (7), navegador de páginas em 10 pt, título de cartão em 11 pt.
- Em tablet de 10" a 9 pt dá para ler de perto. Em TV ou de pé na linha, não.
- Proposta: eixos e rótulos em 12, variação em 12, navegador em 12. Entra no tema (`textClasses`), sem tocar em cada visual.

### B5 (P2). Segmentações inconsistentes entre páginas
- Medido, posição do Período: x = 1014 (Visão Geral, Refugo, Cortes, Extrusora), 672 (Hora-Hora), 621 (Paradas), 654 (Produção Mont.), 508 (Paradas Mont.), e três caixas separadas nas páginas Fluxo.
- Medido, tipo do Período: lista suspensa Ano/Mês/Dia em 4 páginas (mais as 2 da Montagem) e intervalo de datas em 2, todas no mesmo grupo de sincronização `gms_data`. As páginas Fluxo usam grupos próprios (`fluxo_ano`, `fluxo_mes`, `fluxo_dia`), então o período escolhido não chega nelas.
- Medido, Turno: 5 colunas de 5 tabelas (`fHoraHora.Turno`, `Hora-Hora.Turno`, `TiposErros.Turno Erro`, `Producao_Montagem.Turno`, `Paradas_Montagem.Turno`), em 4 grupos de sincronização diferentes, e 6 segmentações sem sincronização (Montagem e Motivo).
- Efeito: o supervisor escolhe o 2º turno numa página e a seguinte volta para todos os turnos. A norma B.6.5 chama isso de motivo nº 1 de "o painel mente".
- Proposta: uma dimensão `dTurno` ligada aos fatos (norma B.2.3) e uma faixa fixa de Período, Turno e Etapa/Máquina na mesma posição em todas as páginas. **[revisor]** por tocar `dTurno`.
- Conferir no PC da fábrica: nas duas páginas da Montagem, o segmentador Período aparece no `.pbip` sem campo ligado (pode ser só o formato do arquivo).

### B6 (P2). Mesmo fato em duas tabelas **[revisor]**
- Medido: Visão Geral e Paradas usam a tabela `Hora-Hora`; a página Hora-Hora usa `fHoraHora`. As duas primeiras têm um filtro de página escondido "Motivo Padrão diferente de Almoço"; a terceira trata refeição dentro das medidas.
- Risco: "Tempo Parado" de uma página não bater com "Parado (min)" de outra para o mesmo dia. Daqui não dá para afirmar que diverge, porque não há modelo vivo.
- Proposta: conferir um dia fechado nas duas páginas no PC da fábrica. Se divergir, uma tabela só e a regra de refeição só na medida.

### B7 (P3). Acabamento
- Títulos-rótulo em Visão Geral, Paradas, Montagem e Extrusora ("Metragem produzida por dia"); a norma B.6.2 pede pergunta.
- `g_ppm` da Visão Geral usa "Mês Nº" no eixo: em janeiro de 2027 os meses de anos diferentes se somam no mesmo número. Trocar por Ano-Mês.
- `g_motivo` de Paradas Mont. está em ordem alfabética, e o título do gráfico faz papel de legenda de cor ("vermelho: parada real · azul: tempo excedido").
- Gráficos por turno usam `#4FC3F7`, `#FFD54F` e `#34D399`, fora dos tokens; o amarelo tem pouco contraste no branco.
- Texto alternativo em 18 de 166 visuais (norma B.6.4).
- Filtro de página da Hora-Hora lista as máquinas à mão (TH01, TH02...): máquina nova não aparece.
- Não há página de auditoria com drill-through (Parte D.9) nem "Dono" no rodapé.
- Densidade: Visão Geral e Paradas têm 15 visuais de dado cada, contra o teto de 8 da norma B.6.3. O arquivo junta supervisão, gestão, qualidade, Montagem e Extrusora em 10 abas.

---

## 2. Power Apps (`GMS/Telas/`)

Medido: 30 telas, 3.159 controles, 846 clicáveis. Triagem com `gms_qa_yaml.py` em todas.

### O que já está bom
- Ações principais usam os tokens `fx_AlturaAcao` (56) e `fx_AlturaAcaoS` (48): Iniciar, Salvar, Enviar e Confirmar têm alvo bom.
- `varProcessando` aparece 614 vezes e há spinner: toque duplo não grava duas vezes.
- Excluir lance abre confirmação antes de apagar.
- As telas de etapa conferem `Errors()` depois do `Patch`.
- Cor por token em quase tudo (só `scr_Monitor_Mandril`, `scrHoraHora_Mandril`, `scrHoraHora_Tubo` e `scr_FichaImpressao` têm cor escrita à mão).

### A1 (P1). Alvos de toque pequenos
- Medido: 312 clicáveis com menos de 44 px. Desses, 167 estão nos dois painéis de TV, que não são tocados. Dos 145 restantes, parte é botão auxiliar invisível ou faixa decorativa. Sobram dezenas de alvos reais, e o padrão que se repete é o ícone de 24 × 24 px.
- Casos reais:
  - `scr_Finalização_1`: `ico_EditarLanceExt` e `ico_ExcluirLanceExt` com 24 px, em X=262 e X=292 (6 px de vão); também `ico_ImprimirExt`, `ico_PackingManualExt`, `ico_DividirPalletExt`, `ico_EditarPlanoExt`.
  - `scr_mandril_1`: motivos da correção (`btn_MotBitolaCorrMand_1` e irmãos) com 128 × 36; `ico_CorrigirMand_1` com 30.
  - `scr_ConsultaOP_1`: `btn_Recente1COP` a `4COP` com 85 × 32.
  - `scr_HoraHora_Trancagem_2` e `Cobertura_1`: `btn_ReplicarLinha` com 26 × 38.
  - Voltar com 32 × 32 nos dois Históricos de turno; ícones de 24 em Bandagem, Bobinadeira, Cobertura, Debandagem e Extrusora.
- Onde o ícone de 24 fica em cima de um botão grande (Mandril: `btn_HoraHoraMand_2`, 183 × 58), o alvo real é o botão e está certo.
- Proposta: alvo mínimo de 48 px e 16 px de vão para toda ação em galeria, com a palavra junto do ícone (quadro "DEPOIS" do mockup). Patch por bloco, tela por tela, começando pela Finalização.
- Isso muda Width, Height e X de controles. A lista exata sai antes de cada patch, como manda a regra.

### A2 (P1). Tamanho e contraste do texto
- Medido: `fx_FonteApoio = 11` em 835 usos e `fx_FonteCorpo = 13` em 654.
- Medido: `fx_CorRotulo #94A3B8` sobre branco dá contraste 2,6:1, em 584 usos. `fx_CorAlerta #E67E22` como cor de texto dá 2,9:1, em 44 usos. A norma pede 4,5:1.
- Proposta, só nos tokens do `Formulas.txt`: `fx_FonteApoio` 11 para 13, `fx_FonteCorpo` 13 para 15, `fx_CorRotulo` para `#64748B` (4,8:1). Texto de alerta usa `fx_CorTexto` com fundo `fx_CorAlertaSuave`.
- Risco: fonte maior pode cortar texto em rótulo de largura fixa. Conferir tela a tela no tablet antes de publicar.

### A3 (P1). `App.OnError` vazio
- Medido: `Telas/OnError.txt` tem 0 byte.
- Efeito: erro que escapa do tratamento local aparece como faixa vermelha com texto técnico.
- Proposta: `App.OnError` com `Notify` em português ("Não gravou. Confira a rede e toque de novo.") e registro do erro numa lista de log.

### A4 (P2). Gravação em vários `Patch` no mesmo botão
- Medido em `scr_mandril_1`: `btn_EnviarMand_2` (9.006 caracteres, 6 `Patch`), `btn_DescartarCorrMand_1` (9.295, 7), `btn_ConfirmarInicioMand_2` (6.430, 5), `btn_TrocarBitolaCorrMand_1` (5.000, 3).
- Risco: se a rede cair entre o 2º e o 3º `Patch`, a ficha fica meio gravada. O SharePoint não tem transação.
- Proposta: o `Patch` que muda o status da ficha fica por último, e cada passo anterior pode ser repetido sem duplicar. Conferir a ordem atual antes de mexer. **[revisor]** se tocar regra de setup.

### A5 (P2). Listas escritas à mão no `OnStart`
- Medido: cerca de 70 mangueiras e 11 trançadeiras em `Telas/OnStart.txt`. O arquivo `_patch_OnStart_EC215-06L-2.md` mostra que mangueira nova já exigiu patch.
- Proposta: ler as duas listas de uma lista do SharePoint (ou da `DM_ENGRENAGENS`, que já tem máquina e construção).
- Conferir: `ClearCollect(colDM_MANDREL, DM_MANDREL)` e as outras duas DM trazem no máximo o limite de linhas não delegáveis (500 ou 2.000). Se alguma DM passar disso, corta sem avisar.

### A6 (P2). Desempenho
- Medido: 3 timers por tela de etapa (30 s, 45 s e 120 s na do Tubo) e 154 chamadas de `Refresh`. `Refresh` recarrega a fonte inteira.
- Medido: `LookUp` dentro de galeria em `scr_selecaosetor_1` (13), `scr_AMDM02_Trancagem_1` (9), `scr_PainelMontagem_1` (8), nas duas Hora-Hora (7 cada) e em `scr_selecaosetor_Montagem` (7). É uma consulta por linha.
- Proposta: um timer por tela, `ClearCollect` com filtro no lugar do `Refresh` cheio, e `LookUp` trocado por coluna calculada na carga (`AddColumns`).
- Conferir no tablet com o Monitor do Power Apps antes de mexer: daqui não dá para medir tempo.

### A7 (P3). Triagem de qualidade
- Medido: 15 das 30 telas falham no `gms_qa_yaml.py`.
  - Versão de controle fora da lista provada: `ModernSpinner@1.1.0` (4 telas), `Text@0.0.51`, `ModernDropdown@1.0.3`, `PenInput@2.3.0`.
  - Ramos de `If` com tipos misturados em 8 telas (`OnVisible` de `scr_mandril_1`, `scr_ExtrusoraMandril_1` e `scr_HoraHora_Cobertura_1`; botões dos dois Históricos, da ConsultaOP e das duas `scrHoraHora_*`).
  - Propriedade fora do padrão em Bandagem e Debandagem.
- `scrHoraHora_Mandril` e `scrHoraHora_Tubo` são telas antigas: nomes `ButtonCanvas5_2`, `TextCanvas2_12`, 22 cores à mão cada.
- `scr_Monitor_Mandril`: 42 cores à mão, fonte 11, velocidade sem unidade na tela, e não mostra `Atualizado_Em`.

### A8. Fluxo do apontamento
- Pelos nomes dos botões do Mandril, começar uma OP leva 4 toques: card da OP, "Iniciar Solda", "Conferi o set-up", "Confirmar Início". Fechar leva 1 ou 2 ("Salvar Parcial" ou "Enviar p/ Tubo").
- Está enxuto. Não contei no tablet, então trate como leitura do YAML e não como teste de uso.

---

## 3. Power Automate (5 fluxos exportados em 10/11)

### 3.1 Quadro

| Fluxo | Gatilho | Concorrência | Paginação | Erro |
|---|---|---|---|---|
| GMS_AutoResfriamentoVulca | a cada 5 min | sem limite | Top 50 com filtro | não avisa |
| GMS_Conferencia_Diaria | terça a sábado, 8h (Brasília) | sem limite | 6 leituras com `$top=5000`, as mais novas por ID | e-mail, mas a execução fica verde |
| GMS_PlanoOPs_Sync | arquivo criado ou alterado, verifica a cada 1 min | 1 por vez, fila de 50 | Top 5000 sem paginação | e-mail |
| GMS_Tempos_Sync | arquivo alterado, verifica a cada 1 min | 1 por vez | Top 5000 sem paginação | e-mail |
| Monitor Solda Mandril | a cada 10 min | sem limite | `ficha_producao` paginada (5000); `DM_Velocidade` sem Top | não avisa |

### 3.2 Unidade da hora de parada do Monitor Solda Mandril
- A conta do fluxo: `HoraParada = agora + (MaterialTotal ÷ Velocidade) × 3600 segundos`.
- Metros divididos pela velocidade dão horas, e horas vezes 3.600 dão segundos. Então o fluxo trata `DM_Velocidade.field_3` como **metros por hora**.
- Isso bate com o `MEL-231_Monitor_Mandril_sem_PowerAutomate.md` e com o app, onde toda velocidade é m/h (`_13TEORICA_M_H`, `fx_NumVelocidade`).
- Conferir no PC da fábrica: abrir a `DM_Velocidade` e olhar uma linha. Valor na casa de dezenas ou centenas é m/h e está certo. Valor entre 0 e 5 seria m/min, e a parada prevista sairia 60 vezes mais tarde.
- Dois pontos ligados **[revisor]**:
  - O Monitor usa `DM_Velocidade`, e a Hora-Hora e o Painel usam `DM_ENGRENAGENS` com o desvio. São duas fontes para a mesma velocidade.
  - `RestanteAtual` considera só a primeira OP "Em processo" da máquina.

### F1 (P1). `GMS_PlanoOPs_Sync` para na virada do ano
- Medido: `folderPath` do gatilho é `.../Plano Trançadeira/2026`. O plano de 2027 vai para outra pasta e o gatilho nunca dispara. Não há e-mail, porque nada falha.
- Medido: a condição do gatilho só aceita arquivo com o prefixo do mês corrente (`PL_NOV_`). O plano de dezembro salvo em novembro não sincroniza; só entra quando alguém salvar de novo em dezembro.
- Proposta: gatilho na pasta `Plano Trançadeira` com subpastas, e condição que aceite o mês corrente e o seguinte. O parâmetro `mes` do script sai do nome do arquivo e não da data.
- Prazo: antes de 01/01/2027.

### F2 (P1). `DM_Velocidade` lida sem Top Count
- Medido: a ação `DM_Velocidade` (Get items) não tem `$top` nem paginação. O conector devolve 100 linhas por padrão.
- Efeito, se a lista tiver mais de 100 linhas: a combinação máquina + mangueira que ficar de fora sai com velocidade 0, a `Hora_Parada` fica vazia e a máquina nunca aparece como crítica.
- Conferir no PC da fábrica: quantas linhas a `DM_Velocidade` tem.
- Proposta: Top Count 5000 na ação. É uma linha de configuração.

### F3 (P1). Sync com Top 5000 sem paginação
- Medido: `Get_items` de `Plano_OPs` e de `Tempos_Montagem` com `$top: 5000` e sem política de paginação. O script recebe essa lista para decidir o que é novo.
- Efeito, quando a lista passar de 5.000 itens: o script não vê os itens além do limite e cria de novo. Vira duplicata.
- Conferir no PC da fábrica: contagem das duas listas. `Plano_OPs` cresce todo mês.
- Proposta: ligar a paginação (limite 20.000), ou filtrar `Plano_OPs` pelo mês antes de mandar ao script.

### F4 (P2). Falha silenciosa
- `Monitor Solda Mandril` e `GMS_AutoResfriamentoVulca` não têm ramo de erro. Se a conexão cair, a tela do Monitor continua mostrando o último cálculo.
- `GMS_Conferencia_Diaria`: o `Avisar_Falha` roda e termina bem, então a execução aparece como sucesso.
- Os três e-mails de falha vão só para o William. Na ausência dele, ninguém vê.
- Proposta: ramo de erro com e-mail nos dois fluxos agendados; `Terminate` com status Falha depois do `Avisar_Falha`; um segundo destinatário; e `Atualizado_Em` visível na `scr_Monitor_Mandril`, em vermelho quando passar de 20 min.

### F5 (P2). Fila do `GMS_PlanoOPs_Sync`
- Medido: `Delay` de 30 s antes de conferir se o arquivo mudou, com 1 execução por vez e fila de até 50.
- Efeito: o Excel salva sozinho várias vezes. Cada salvamento entra na fila, espera 30 s e só então se cancela. Cinquenta salvamentos somam até 25 min de atraso.
- Proposta: conferir o `Modified` antes do `Delay`. Quem já está velho sai na hora.
- Medido: o corpo do POST é montado com `concat`, sem escapar aspas. Uma aspa ou barra invertida no PN, na Origem ou no Tipo quebra o JSON e derruba a execução.
- Proposta: montar o corpo como objeto JSON, não como texto colado.

### F6 (P3). Tempo e volume
- `Monitor Solda Mandril`: 11 ações por máquina, 144 execuções por dia. Com 11 máquinas são cerca de 18 mil ações por dia. O MEL-231 já propõe levar a conta para o app; concordo, porque também acaba com F2 e com as duas fontes de velocidade.
- Conferir: o limite diário de ações da licença do William. Não consultei a documentação nesta sessão.
- `GMS_Conferencia_Diaria`: as 6 leituras rodam em fila e podem rodar em paralelo. O parâmetro `packingJson` vai sempre como `[]`.
- `GMS_AutoResfriamentoVulca`: os 110 min estão escritos em dois lugares (filtro e gravação). Se o tempo mudar por mangueira, precisa editar o fluxo.
- Conferir: se `field_10`, `field_11` e `Status` são colunas indexadas. Filtro em coluna sem índice falha quando a lista passa de 5.000 itens.
- `int(field_14)` no Monitor quebra se a metragem vier com casa decimal.

---

## 4. Ordem sugerida

| # | O que | Esforço | Depende de |
|---|---|---|---|
| 1 | F1: pasta e mês do `GMS_PlanoOPs_Sync` | pequeno | "sim" e Power Automate |
| 2 | F2 e F3: Top Count e paginação | pequeno | contagem das listas e "sim" |
| 3 | B2 e B4: tema do BI (cor e tamanho de texto) | pequeno | "sim" e Desktop |
| 4 | A1: alvos de 48 px na Finalização | médio | plano aprovado, tablet |
| 5 | A3: `App.OnError` | pequeno | "sim" e publicação |
| 6 | F4: aviso de falha e idade do dado | pequeno | "sim" |
| 7 | B1 e B3: Visão Geral nova e layout móvel | médio | DAX no PC da fábrica |
| 8 | A2: tokens de fonte e contraste | médio | conferência tela a tela |
| 9 | B5 e B6: `dTurno` e tabela única de Hora-Hora | grande | `revisor` e modelo vivo |

## 5. O que precisa do "sim" do William
- Qualquer edição nos 5 fluxos.
- Trocar o tema do BI e criar layout móvel.
- Qualquer patch em tela, com a lista de X, Y, Width e Height que mudam.
- Mudar tokens do `Formulas.txt`.

## 6. O que depende do PC da fábrica
- Contagem de linhas de `DM_Velocidade`, `Plano_OPs` e `Tempos_Montagem`, e um valor de exemplo de `DM_Velocidade`.
- Colunas indexadas da `ficha_producao`.
- Bater "Tempo Parado" (Paradas) com "Parado (min)" (Hora-Hora) num dia fechado.
- Segmentador Período das páginas da Montagem.
- Medir tempo de carga das telas com o Monitor do Power Apps.
- Abrir o `.pbip` no Desktop para confirmar a cor herdada dos gráficos.

## 7. Limites desta análise
- Não abri o relatório no Desktop nem o app no tablet. Layout e cor vêm do JSON e do YAML.
- A contagem de alvos pequenos trata como clicável todo botão e todo controle com `OnSelect`. Por isso o número bruto (312) é maior que o real.
- Não validei DAX.
- O mockup foi gerado por script nesta sessão, não pelo `produtor-de-artes`.
- Os itens **[revisor]** ainda não passaram pelo `revisor`.
