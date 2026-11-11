# Mudanças do relatório GMS_Painel (etapa 1': tema, B5, B6, B7, medidas HH e TE)

Data: 11/11/2026. Só o relatório `GMS/PowerBI/GMS_Painel.Report`. Não toquei no modelo, na `pg_visao_geral` nem nos visuais `nav`. Sem commit e sem publicação. O relatório só funciona depois que o modelo ganhar `fHoraCheia` e `dTurno` (etapa de modelo) e o William reabrir o projeto no Desktop.

## Tema (GMS_Tema.json, vale para o relatório todo)
- `dataColors[0]` #E30613 -> #2C6FBF; `good` #16A34A; `neutral` #E67E22; `bad` #C0392B; `textClasses.label` 10 -> 12 pt (rótulo de dado e eixo herdam). `tableAccent`, `maximum` e as outras cores ficaram como estavam (ainda #E30613).

## Medidas de relatório (reportExtensions.json, entidade Medidas)
- `HH Meta (m)` = SUM(fHoraCheia[Meta]); `HH Real (m)` = SUM(fHoraCheia[Real]).
- `HH Meta Útil (m)` e `HH Aderência`: fator 1295/1440 só quando `ISFILTERED(fHoraCheia[Hora])` é falso.
- `HH Parado (min)` e `HH Principal Parada` leem fHoraCheia[Parado] com KEEPFILTERS(Motivo Padrão <> "Almoço").
- `HH Dia Produtivo`: texto passou de 05:20 para 05:00 (regra nova do dia produtivo).
- `Minutos Excedidos Montagem`: SUMX por Paradas_Montagem[OPVinculada]; TE da OP = MAX(0, TE - 45) se a OP tem parada com LEFT(TRIM(Motivo),2) = "RF" (detectada com REMOVEFILTERS do Motivo, então vale com Motivo no eixo); OP vazia fica inteira.
- Novas (leem fHoraCheia, substituem as do modelo na pg_paradas): `PA Tempo Parado (h)`, `PA Tempo Parado %`, `PA Δ Tempo Parado vs mês ant.`, `PA Motivo Nº1`, `PA Horas Perdidas Motivo Nº1`, `PA % Acumulado Paradas`, `PA Tempo Parado por Tipo (h)`. As medidas antigas do modelo ficam (a Visão Geral ainda as usa).
- `PA Tempo Parado %` = parado sem Almoço / (SUM(Minutos) - parado de Almoço), os dois sem filtro de motivo. O modelo antigo usava 507/533/398 min por turno; confira um dia fechado.

## Por página

### Hora-Hora Trançagem (`pg_horahora`)
- Filtro de página f_trancadeiras (lista TH01..Spiral) trocado por 'Célula não vazia' em fHoraCheia (filtro f_sem_vazio_celula); máquina nova aparece sozinha.
- g_prod_hora: eixo fHoraHora[Hora BI] -> fHoraCheia[Hora] (ordem pelo HoraOrdem do modelo); medidas HH Real/Meta já leem fHoraCheia.
- g_motivo: eixo e filtros fHoraHora[Motivo Padrão] -> fHoraCheia[Motivo Padrão] (filtros do visual: não vazio e sem refeições, mantidos).
- seg0 (Máquina): fHoraHora[Célula] -> fHoraCheia[Célula]. seg1 (Turno): fHoraHora[Turno] -> dTurno[Turno].
- g_motivo2 (2º motivo) NÃO trocado: a fHoraCheia não tem 'Motivo 2 Padrão'. Continua em fHoraHora[Motivo 2 Padrão] e HH Parado (min) agora lê fHoraCheia: sem relação entre elas as barras saem iguais. PENDENTE: modelo precisa da coluna (ou o visual sai).
- Faixa de filtros: Período x=1014 w=250 (era 672), Turno x=834 w=168 (era 934, grupo gms_turno_hh -> gms_turno), Máquina x=666 w=156 (era 1114); y=52 h=63.
- g_prod_hora: título 'Produção por hora (m): Real × Meta' -> 'Em quais horas a produção ficou abaixo da meta (m)?'
- g_motivo: título 'Motivos de parada (min)' -> 'Quais motivos mais pararam a máquina (min)?'
- g_motivo2: título '2º motivo (min)' -> 'Qual foi o 2º motivo de parada (min)?'
- Fontes explícitas de 8/9 pt -> 12 pt em 12 propriedades (só a fonte; nav e Visão Geral intocados). Texto alternativo acrescentado em 10 visuais de dado.

### Paradas (`pg_paradas`)
- Removido o filtro de página escondido f_refeicao_hh (Motivo Padrão <> Almoço); a refeição sai nas medidas PA (KEEPFILTERS Motivo Padrão <> Almoço).
- Trocadas as medidas do modelo (leem 'Hora-Hora') por medidas de relatório novas que leem fHoraCheia: kpi0 PA Tempo Parado (h); kpi1 PA Tempo Parado %; kpi1_d PA Δ Tempo Parado vs mês ant.; kpi2 PA Motivo Nº1; kpi3 PA Horas Perdidas Motivo Nº1; g_pareto eixo fHoraCheia[Motivo Padrão] + PA Tempo Parado (h) + PA % Acumulado Paradas; g_turno eixo dTurno[Turno] + PA Tempo Parado (h); g_tipo PA Tempo Parado por Tipo (h) (TREATAS dMotivoParada[Motivo] -> fHoraCheia[Motivo Padrão]); seg0 Motivo -> fHoraCheia[Motivo Padrão]; seg1 Turno -> dTurno[Turno].
- Faixa de filtros: Período x=1014 w=250 (era 622), Turno x=834 w=168 (era 884, grupo gms_turno mantido), Motivo x=666 w=156 (era 1064); y=52 h=63.
- g_turno: 3 cores de turno (#4FC3F7/#FFD54F/#34D399) trocadas por cores do tema (azul, verde-azulado, âmbar).
- g_pareto: título 'Pareto de paradas (h) e % acumulado' -> 'Quais motivos concentram as paradas (h)?'
- g_pareto_ref: título 'Pareto de refugo (m) e % acumulado' -> 'Quais causas concentram o refugo (m)?'
- g_tipo: título 'Tempo parado por tipo (falha × programada × material…)' -> 'Que tipo de parada pesa mais (falha, material, programada...)?'
- g_turno: título 'Tempo parado por turno (h)' -> 'Qual turno mais parou (h)?'
- Fontes explícitas de 8/9 pt -> 12 pt em 17 propriedades (só a fonte; nav e Visão Geral intocados). Texto alternativo acrescentado em 13 visuais de dado.

### Produção Montagem (`pg_producao_montagem`)
- Faixa de filtros: Período x=1014 w=250 (campos dCalendario Ano/Mês/Dia, como as outras páginas, grupo gms_data); Turno x=834 w=168 (dTurno[Turno], grupo gms_turno); Célula x=666 w=156; y=52 h=63.
- g_turno: eixo Producao_Montagem[Turno] -> dTurno[Turno].
- g_turno: 3 cores de turno (#4FC3F7/#FFD54F/#34D399) trocadas por cores do tema (azul, verde-azulado, âmbar).
- g_celula: título 'Peças produzidas por célula' -> 'Qual célula produziu mais peças?'
- g_dia: título 'Peças produzidas por dia' -> 'Quantas peças a Montagem produziu por dia?'
- g_parada_dia: título 'Parada real por dia (min)' -> 'Quanto a Montagem parou por dia (min)?'
- g_turno: título 'Peças produzidas por turno' -> 'Qual turno produziu mais peças?'
- Fontes explícitas de 8/9 pt -> 12 pt em 15 propriedades (só a fonte; nav e Visão Geral intocados). Texto alternativo acrescentado em 10 visuais de dado.

### Paradas Montagem (`pg_paradas_montagem`)
- Faixa de filtros: Período x=1014 w=250 (campos dCalendario Ano/Mês/Dia, como as outras páginas, grupo gms_data); Turno x=834 w=168 (dTurno[Turno], grupo gms_turno); Célula x=666 w=156 e Motivo x=498 w=156; y=52 h=63.
- g_motivo: ordem alfabética -> por Minutos Parados Montagem (maior primeiro); cores TE/RF passaram a cores do tema (índices 1 e 2, as mesmas séries do g_celula, que tem legenda de verdade).
- g_celula: título 'Por célula (min): parada real × tempo excedido × refeição' -> 'Quanto cada célula perdeu em parada, excesso e refeição (min)?'
- g_motivo: título 'Minutos por motivo — vermelho: parada real · azul: tempo excedido · cinza: refeição' -> 'Quais motivos tiram mais minutos da Montagem? (cores como no gráfico por célula)'
- Fontes explícitas de 8/9 pt -> 12 pt em 10 propriedades (só a fonte; nav e Visão Geral intocados). Texto alternativo acrescentado em 9 visuais de dado.

### Extrusora (`pg_extrusora`)
- g_turno: 3 cores de turno (#4FC3F7/#FFD54F/#34D399) trocadas por cores do tema (azul, verde-azulado, âmbar).
- g_bitola: título 'Metros extrudados por bitola' -> 'Quais bitolas mais saíram da extrusora (m)?'
- g_dia: título 'Metros extrudados por dia' -> 'Quantos metros a extrusora fez por dia?'
- g_ref_causa: título 'Refugo (kg) por tipo de erro' -> 'Quais erros geram mais refugo (kg)?'
- g_ref_dia: título 'Refugo (kg) por dia' -> 'Quanto refugo a extrusora gerou por dia (kg)?'
- g_turno: título 'Metros extrudados por turno' -> 'Qual turno extrudou mais metros?'
- Fontes explícitas de 8/9 pt -> 12 pt em 16 propriedades (só a fonte; nav e Visão Geral intocados). Texto alternativo acrescentado em 11 visuais de dado.

### Fluxo - Etapas (`pg_fluxo_1`)
- seg_ano + seg_mes + seg_dia (grupos fluxo_ano/mes/dia) substituídos por UM seg_data (Ano/Mês/Dia, grupo gms_data) em x=1014 w=250; seg_turno: fHoraHora[Turno] -> dTurno[Turno], grupo gms_turno, x=834 w=168; seg_maquina (grupo fluxo_maquina, ficha_producao[Trançadeira]) movido para x=666 w=156. y=16 e altura 64 mantidos (a página não tem faixa).
- Fontes explícitas de 8/9 pt -> 12 pt em 7 propriedades (só a fonte; nav e Visão Geral intocados). Texto alternativo acrescentado em 0 visuais de dado.

### Fluxo - Mão de obra (`pg_fluxo_2`)
- seg_ano + seg_mes + seg_dia (grupos fluxo_ano/mes/dia) substituídos por UM seg_data (Ano/Mês/Dia, grupo gms_data) em x=1014 w=250; seg_turno: fHoraHora[Turno] -> dTurno[Turno], grupo gms_turno, x=834 w=168; seg_maquina (grupo fluxo_maquina, ficha_producao[Trançadeira]) movido para x=666 w=156. y=16 e altura 64 mantidos (a página não tem faixa).
- g_metros: título 'Metros por dia · média dos dias produtivos, por mês' -> 'Quantos metros por dia a trançagem e a cabine movem em cada mês?'
- g_pessoas: título 'Pessoas por dia · média dos dias produtivos, por mês' -> 'Quantas pessoas por dia a trançagem e a cabine usam em cada mês?'
- Fontes explícitas de 8/9 pt -> 12 pt em 10 propriedades (só a fonte; nav e Visão Geral intocados). Texto alternativo acrescentado em 0 visuais de dado.

### Refugo PPM (`pg_refugo_ppm`)
- Fontes explícitas de 8/9 pt -> 12 pt em 7 propriedades (só a fonte; nav e Visão Geral intocados). Texto alternativo acrescentado em 9 visuais de dado.

### Refugo PPM Cortes (`pg_refugo_ppm_cortes`)
- Fontes explícitas de 8/9 pt -> 12 pt em 16 propriedades (só a fonte; nav e Visão Geral intocados). Texto alternativo acrescentado em 5 visuais de dado.

### Visão Geral (`pg_visao_geral`) e `nav`
- Não tocados. Só vale para ela o tema global.

## Posição da faixa de filtros (B5): o que mudou de lugar
Padrão (x, largura): Período 1014/250, Turno 834/168, 3º filtro (Máquina, Célula ou Motivo) 666/156, 4º filtro (Motivo da Montagem) 498/156; y=52, altura 63 (Fluxo fica em y=16, altura 64).
- Hora-Hora: Período 672->1014, Turno 934->834, Máquina 1114->666. Paradas: Período 622->1014, Turno 884->834, Motivo 1064->666.
- Produção Mont.: Período 654->1014, Turno 916->834, Célula 1096->666. Paradas Mont.: Período 509->1014, Turno 736->834, Célula 916->666, Motivo 1096->498.
- Fluxo 1 e 2: três caixas de período (596/732/868) viraram uma em 1014; Turno 1004->834; Máquina 1140->666.
- Já estavam em 1014: Extrusora, Refugo PPM e Cortes (Período). Refugo e Cortes mantêm y=52 e altura 46 porque há cartões logo abaixo.

## Pendências e dúvidas
1. `g_motivo2` (Hora-Hora) continua em fHoraHora[Motivo 2 Padrão]: a fHoraCheia da especificação não tem essa coluna. Sem ela o gráfico quebra. Preciso da coluna no modelo (e troco a referência) ou tiro o gráfico.
2. Relação esperada no modelo: fHoraCheia[Data BI] -> dCalendario[Date] (usada pelo `PA Δ` e pelo período); dTurno[Turno] -> fHoraCheia, Producao_Montagem e Paradas_Montagem [Turno BI]. `PA Tempo Parado por Tipo (h)` usa TREATAS e não depende de relação com dMotivoParada.
3. Turno na Fluxo: o slicer passou a dTurno[Turno]; as medidas de Fluxo leem ficha_producao e não filtram por turno (já era assim com fHoraHora). Turno Erro (Cortes) e Turno da Extrusora ficaram nas colunas próprias: dTurno não se liga a elas.
4. Períodos de Refugo e Cortes são por Date (intervalo) e o resto é Ano/Mês/Dia: estão no mesmo grupo gms_data, mas só sincronizam entre slicers do mesmo campo. Os da Montagem passaram para Ano/Mês/Dia de dCalendario para sincronizar com Hora-Hora, Paradas e Extrusora.
5. Cores do `g_motivo` da Montagem: sem legenda própria (série única); seguem as cores das séries do `g_celula`, que tem legenda. Fonte 12 pt em visuais pequenos (cartões de variação 28 px, slicers de 63 px) pode cortar: conferir no Desktop.
6. Diferença de formatação: o dump JSON do Python reescreve alguns arquivos com poucos bytes de diferença (espaços/escapes) além do que mudou.


# Etapa 3: Visão Geral (B1), celular (B3), navegação Mangueira x Montagem e g_motivo2

Data: 11/11/2026. Só `GMS/PowerBI/GMS_Painel.Report`. Sem commit, sem publicação, modelo intocado.

## Hora-Hora (`pg_horahora`)
- g_motivo2 passou a ler `fHoraCheia[Motivo 2 Padrão]` (eixo, ordenação e filtros; 6 referências trocadas). A pendência 1 da etapa anterior fecha quando a coluna existir no modelo.

## Visão Geral (`pg_visao_geral`), refeita
- Sai a tabela `Hora-Hora`, sai o filtro escondido de Almoço, saem os 15 visuais antigos (6 cartões, 4 deltas, g_etapa, g_tendencia, g_ppm, g_motivo). Filtro de página agora: Célula não vazia na `fHoraCheia`.
- 8 visuais de dado: 5 cartões (kpi0..kpi4), `g_maquina` (principal), `g_motivo` e `g_dia` (apoio). Mantidos faixa, título, logo, "Dado atualizado até" (12 pt) e o Período (seg0, 1014/52/250x63). Novo Turno (seg1 = dTurno[Turno], 834/52/168x63, grupo gms_turno).
- Cartões (240x110, y=122): título = o que é; subtítulo = seta + texto de estado (medida); valor 28 pt; borda de 3 px na cor de estado (verde #16A34A, laranja #E67E22, vermelho #C0392B, cinza sem dado). Estado nunca só pela cor.
  1. Metragem trançada: HH Real (m) contra a meta (HH Meta Útil): verde >= 100%, laranja 90-99%, vermelho < 90%.
  2. Aderência: HH Aderência, mesmos limites.
  3. Parado (min): HH Parado (min); estado pela fatia do tempo parado (cópia da expressão do PA Tempo Parado %): verde <= 5%, laranja <= 10%, vermelho acima. **Os 5% e 10% são provisórios; o William define a meta de parado.**
  4. Refugo PPM: [Refugo PPM] contra 3900 (cópia do valor da medida Meta Refugo PPM): verde <= 3900, laranja até +10%, vermelho acima. O +10% também é provisório.
  5. Montagem: [% Montagem] (modelo, tabela Producao_Montagem) contra 100%, limites como a Aderência.
- g_maquina "Qual máquina está mais longe da meta?": barras Real x Meta útil por `fHoraCheia[Célula]`, ordenado por HH Aderência crescente (pior no topo); o Real da pior fica vermelho (medida `VG Cor Máquina`, regra de cor por campo) e o nome dela vai no subtítulo (`VG Pior Máquina`).
- g_motivo "Quais motivos mais pararam as máquinas (min)?" (copia o da Hora-Hora, com os filtros de refeição) e g_dia "A produção acompanhou a meta hora a hora?" (linhas HH Real x HH Meta por `fHoraCheia[Hora]`).
- Títulos em pergunta, texto alternativo em todos, fonte >= 12 pt. 12 medidas novas `VG *` em `reportExtensions.json` (cada uma com a expressão copiada, sem referenciar medida de relatório; só [Refugo PPM] e [% Montagem], do modelo).

## Celular (B3): `visuals/<visual>/mobile.json`
- Visão Geral e Hora-Hora, canvas de 320 px: filtros no topo, 4 cartões em 2x2 + o 5º em linha inteira, depois os gráficos empilhados, "Dado atualizado até" no fim. Nos cartões da Visão Geral o título e o subtítulo quebram linha. O layout de mesa não foi tocado. Visuais sem mobile.json (faixa, título, logo, botões) não entram no celular.

## Navegação Mangueira x Montagem
- Forma escolhida: **botões de navegação de página, sem indicadores/bookmarks.** Cada página tem os dois botões de modo e o menu da sua família; "Mangueira" leva à Visão Geral, "Montagem" leva à Produção Mont. Assim, ao abrir página de montagem aparece o menu de montagem e vice-versa, e não existe bookmark para quebrar quando uma página nascer. Diferença para o pedido: o menu do outro lado só aparece depois do clique (que muda de página).
- Removidos os 10 visuais `nav` (pageNavigator). Em cada página: `mod_mangueira`, `mod_montagem` e um `sub_<página>` por página da família (actionButton, `visualLink` tipo `PageNavigation`, formato dos botões de Desktop do Modelo_PBIP). Botão ativo: azul #2C6FBF com texto branco e negrito (modo ativo na faixa vermelha: branco com texto escuro). Texto 12 pt.
- Páginas com faixa: modos em x=614 e 720 (106x32, y=8); título com largura 590; "Dado atualizado até" em x=836 w=256 e 12 pt; menu em y=58 (34 de altura), começa em x=16 e termina em x=638 (antes das segmentações, que começam em 666). Montagem: 2 botões, termina em x=266.
- Rótulos encurtados para caber: Visão Geral, Hora-Hora, Paradas, Refugo, Cortes, Extrusora, Etapas, Pessoas (Fluxo Etapas e Fluxo Mão de obra) e, na Montagem, Produção Mont. e Paradas Mont. O texto alternativo de cada botão traz o nome completo.
- Fluxo (sem faixa e com o menu antes embaixo): título só com a 1ª linha em 16 pt (y=10, w=400); modos em x=424 e 532 (104x32); menu em y=48; a 2ª linha do título (método da ficha) virou a caixa `subtitulo` no rodapé (x=608, y=664, 12 pt, onde ficava o menu).

## Conferir no Desktop
1. Abrir o `.pbip` sem erro de formato (botões com `visualLink`, mobile.json, medidas `VG *`). Aplicar o TMDL antes (fHoraCheia, dTurno).
2. Regra de cor por campo no g_maquina (série Real): se não aceitar, a pior máquina continua no subtítulo.
3. Títulos e subtítulos dos cartões não cortados em 240 px; o menu de 8 botões sem texto cortado; fundo e destaque dos botões.
4. Camada celular: abrir "Layout para celular" nas duas páginas e ver a ordem dos visuais.
5. [% Montagem] responde ao Turno (dTurno liga em `Turno BI`, a medida cruza por TREATAS em `Turno`); se o cartão 5 ficar sem valor com Turno marcado, é isso.
6. A faixa vermelha das páginas segue #E30613 (o tema só trocou a cor das séries).
