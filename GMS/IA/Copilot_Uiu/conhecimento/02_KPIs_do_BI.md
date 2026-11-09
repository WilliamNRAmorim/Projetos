# GMS: KPIs do BI (Power BI)

Fonte: GMS_Mestre_BI.md (resumo para o Uiu, 09/11/2026)

Este arquivo resume a norma do Power BI do GMS e o catálogo de KPIs. Onde houver conflito, a seção final "Decisões vigentes da meta" vale mais que o resto do Mestre_BI. O Mestre_BI é a norma; o catálogo de KPIs é a única definição válida de cada indicador (divergiu, é bug).

## 1. Arquitetura em poucas linhas

- O BI explica; o app (Power Apps + SharePoint) captura. Se o número do painel diverge da tela do operador, um dos dois está errado e a conversa para até descobrir qual. Não existe "arredondamento do BI".
- Camadas: Bronze (origem, prefixo `src_`, não carrega no modelo), Prata (preparo, `stg_`, não carrega: tipagem, unpivot, Data de Referência e Turno, deduplicação) e Ouro (modelo semântico, só o que o usuário vê).
- Tabelas: prefixo `f` é fato, `d` é dimensão, `b` é ponte, `_` é tabela só de medidas. Modelo estrela, relacionamento 1 para N em sentido único, sem bidirecional.
- A `ficha_producao` (1 linha por OP, 103 colunas) não é consumida direto. O BI usa o unpivot: `Etapas` (1 etapa concluída por ficha, 13.256 linhas na auditoria de 31/08) e `fFluxoEtapas` (1 etapa por ficha, com fila e processamento separados, 16.314 linhas). Outros fatos: `fRefugo`, `fInspecao`, `fHoraHora`, `fParada`, `fCarretel`, `fEvento`.
- Dimensões: `dCalendario`, `dTurno`, `dEtapa`, `dOP`, `dMangueira`, `dPosto`, `dColaborador`, `dMotivoParada`, `dCausaRefugo`, `dDelineamento`.
- Todo fato liga em `dCalendario` pela coluna **Data de Referência** e em `dTurno` pela coluna **Turno**. Nunca pela data-hora bruta e nunca por `Modified`.
- **O BI não calcula turno.** A camada Prata carimba `Turno` e `Data de Referência` uma vez; o BI só lê. A única exceção é a medida `Turno Agora`, para painel ao vivo.
- **O dia produtivo começa às 05:20.** Antes das 05:20 o dia de produção ainda é o anterior. Fronteiras do dTurno: 1º turno 05:20 a 13:56; 2º turno 13:57 a 22:19; 3º turno 22:20 a 05:19. Exemplo: uma OP que termina às 23:50 de segunda e outra que termina às 04:30 de terça pertencem ao 3º turno da segunda-feira.
- Nunca filtrar, ordenar nem fazer atualização incremental por `Modified`: OP que avança de etapa atualiza o `Modified` e some do histórico da etapa anterior. Usar `data_hora_final_<etapa>` e a Data de Referência.
- Não usar `TODAY()`/`NOW()` como âncora de "hoje". Em modelo Import o dado só existe até o último refresh, e o painel mostraria "hoje sem produção" às 6h. A âncora é `MAX(Data de Referência)` do dado.
- Import é obrigatório para SharePoint/Excel (nada de DirectQuery). Capacidade Pro: até 8 atualizações por dia, então o painel não é "ao vivo" e todo relatório mostra "Atualizado em dd/mm/aaaa hh:mm" no rodapé.
- Proibido: divisão com `/` (usar `DIVIDE`), agregação implícita (arrastar coluna), `IFERROR` tapando buraco de dado. Medida quebrada fica oculta, nunca visível dando resultado errado (MEL-087).
- Junção: declarar o grão dos dois lados e conferir a contagem de linhas antes e depois. Uma junção com divergência de granularidade já inflou a quantidade em cerca de 20%. A chave dos dados mestres de mangueira é PARTNUMBER x BRD CODE, não só PARTNUMBER.
- Locale: leitura de número com cultura explícita. Sem ela, `675,5` vira erro ou `6755`.

## 2. Catálogo de KPIs

### K01 Metros Produzidos
- Fórmula: soma da metragem concluída na etapa (com `Fim da Etapa` preenchido), no período e turno selecionados.
- DAX curto: `CALCULATE(SUM(fEtapaOP[Quantidade (m)]), NOT ISBLANK(fEtapaOP[Fim da Etapa]))`.
- Recorte certo: sempre com filtro de etapa explícito, ou use o K02.
- Armadilha: sem filtro de etapa, soma a mesma mangueira oito vezes (uma por etapa). É o erro número 1 do primeiro painel.

### K02 Metros Equivalentes (produção da célula)
- Fórmula: metragem contada uma vez por OP, na etapa terminal (Finalização).
- DAX curto: `CALCULATE([Metros Produzidos], KEEPFILTERS(dEtapa[Etapa] = "Finalização"))`.
- Recorte certo: comparação entre turnos, semanas e produção da célula usa K02, nunca K01.
- Armadilha: muda se o roteiro mudar (família que pula etapa). Quando a `fFluxoEtapas` virar autoritativa, a etapa terminal será lida da tabela.

### K03 OPs Concluídas
- Fórmula: contagem distinta de OPs que fecharam a etapa terminal (Finalização) no recorte.
- Recorte certo: Finalização com `Fim da Etapa` preenchido.
- Armadilha: contar OP em outra etapa conta a mesma OP várias vezes.

### K04 WIP em Processo (por etapa)
- Fórmula: OPs que iniciaram a etapa e ainda não fecharam. É foto, não fluxo, então ignora o recorte de data (`REMOVEFILTERS(dCalendario)`).
- Armadilha: OP zumbi. A auditoria achou OP parada há 4.162 h, que infla o WIP para sempre e aponta gargalo fantasma. Todo visual de WIP deve vir junto do K09 (OPs Zumbi).

### K05 Vazão do Turno
- Fórmula: Metros Produzidos dividido pelo número de turnos distintos, na etapa selecionada. Denominador do Radar de Gargalo.
- Recorte certo: uma etapa selecionada.

### K06 Índice de Gargalo (Radar de Gargalo)
- Fórmula: WIP vezes metragem média por OP, dividido pela vazão média das últimas 3 datas de produção. A etapa com maior índice é o gargalo do dia.
- Armadilha: com menos de 3 dias de dado na etapa o índice oscila. Só exibir quando a vazão recente for maior que zero, senão o painel elege gargalo por divisão instável.

### K07 Tempo de Ciclo da Etapa (mediana)
- Fórmula: mediana (não média) do tempo entre início e fim da etapa, por OP, em minutos (`MEDIANX` + `DATEDIFF`), só com início e fim preenchidos.
- Armadilha: média sempre mente aqui. Uma OP esquecida aberta por 4.162 h desloca a média e não a mediana. Todo lead time do GMS é mediana, com P90 ao lado quando a decisão depende da cauda.

### K08 Lead Time Total da OP
- Fórmula: da primeira entrada à última saída da OP, em horas (`DATEDIFF` em minutos dividido por 60).
- Recorte certo: por OP, todas as etapas dela.

### K09 Idade da OP na Etapa e OPs Zumbi
- Fórmula: Idade na Etapa (h) é o tempo desde o início da etapa atual até agora. OPs Zumbi conta as OPs com idade acima do teto configurado (padrão 72 h).
- Armadilha: é exceção, não estatística. Alimenta o Andon. Usa `NOW()` de propósito, por ser indicador de painel ao vivo.

### K10 Metros Refugados
- Fórmula: soma do refugo consolidado de três origens (linha, bobinadeira e extrusora), na `fRefugo`.
- DAX curto: `SUM(fRefugo[Quantidade (m)])`.

### K11 % Refugo
- Fórmula: refugo dividido por (produção boa mais refugo), no mesmo recorte.
- DAX curto: `DIVIDE(Refugo, Bom + Refugo)`.
- Armadilha: numerador e denominador precisam ser do mesmo recorte de etapa. Refugo da Trançagem sobre produção de todas as etapas dá percentual bonito e falso.

### K12 Custo do Refugo (R$)
- Fórmula: metros refugados vezes custo padrão por metro da família (`SUMX` com `RELATED` em `dMangueira`).
- Estado: a tabela de custo padrão por família ainda não existe. Enquanto não existir, a medida fica oculta, não estimada.

### K13 Pareto de Causa (% acumulado)
- Fórmula: curva de Pareto sobre a causa de refugo: refugo das causas até a atual, dividido pelo total.
- Recorte certo: segmentações por período, etapa, máquina, turno e mangueira. Pareto, nunca pizza.

### K14 Cpk do Diâmetro
- Fórmula: `MIN(LSE - média, média - LIE)` dividido por 3 vezes o desvio padrão, com a spec vinda do Delineamento. Abaixo de 1,33 o processo não é capaz.
- Armadilha: unidade. A spec dos dados mestres está em polegada e o operador pode digitar em milímetro. Enquanto a pendência de unidade (MEL-091/MEL-097) estiver aberta, o KPI fica oculto e o SPC bloqueado.

### K15 Meta, Real e Aderência Hora-Hora (HH)
- Fórmula: Real HH é a soma de metros apontados na janela. Meta HH é a velocidade da mangueira vezes os minutos da janela. Aderência HH é Real dividido por Meta.
- Estado: o Mestre_BI registra as três medidas como quebradas (MEL-087) em 31/08; a versão restaurada tem de bater com a tela do Hora-Hora do app. As decisões atuais de meta (ver seção 4) valem mais que a fórmula do Mestre_BI.
- Armadilha: a janela horária não é uma hora cheia; a meta é sempre calculada por linha com os minutos da janela. A coluna `Rendimento` do Hora-Hora mistura 3 escalas; use Real / Meta.

### K16 Aderência ao Plano
- Fórmula: OPs concluídas até a data planejada, dividido pelo total de OPs concluídas. É o "E" do SQDC.
- Recorte certo: precisa da Data Planejada na `dOP`.

### K17 Tempo Parado, MTBF e MTTR
- Fórmulas: Tempo Parado é a soma da duração das paradas. MTTR é Tempo Parado dividido pelo número de eventos de parada. MTBF é (minutos programados menos tempo parado) dividido por (falhas vezes 60), contando só motivos do tipo "Falha".
- Armadilha: MTBF só significa algo se `dMotivoParada` distinguir falha de parada programada (setup, refeição, preventiva). Sem essa classificação o número existe e não quer dizer nada.

### K18 OEE-lite
- Fórmula: Disponibilidade x Performance x Qualidade. Disponibilidade = (minutos programados menos parada) / minutos programados. Performance = Real HH / Meta HH. Qualidade = 1 menos % Refugo.
- Armadilha: enquanto a Meta HH depender de velocidade cadastrada (não medida por sensor) e as paradas não estiverem completas, deve ser rotulado "OEE-lite" no visual. Vira OEE de verdade quando o Factbird entrar.
- Observação: o "OEE2" citado nas decisões da seção 4 é o OEE vigente do painel; ele é diferente desta fórmula do Mestre_BI.

### K19 Furo de FIFO
- Fórmula: consumos fora da ordem de chegada dividido pelo total de consumos da bobinadeira (`fCarretel`, coluna `Fora de Ordem`).

### K20 OP Health Score
- Fórmula: nota de 0 a 100 com quatro fatores: idade na etapa (peso 0,4), refugo (0,3), validade do composto (0,2) e retrabalho/edições na ficha (0,1). Os pesos são proposta inicial e ficam numa tabela de configuração, não na medida.

## 3. Relatórios (visão rápida)

- Uma página, uma decisão, um público. Três arquivos: Operação (supervisão e líderes), Gestão (liderança, SQDC) e Qualidade (SPC e Pareto), todos sobre o mesmo modelo semântico compartilhado.
- Operação, página 1: como está o turno agora (KPIs de metros, aderência HH, % refugo, WIP, OPs zumbi; Radar de Gargalo e Andon). Recorte padrão é o turno atual, não "hoje".
- Gestão: quadro SQDC e tendência. Comparação entre turnos usa K02.
- Alerta de aderência só abaixo de 90%. Série padrão em azul (`fx_CorInfo`); o vermelho Danfoss é reservado para marca e exceção crítica.
- Painel de TV não tem segmentação: página fixa, recorte travado. Há uma página oculta de auditoria (drill-through) com a tabela crua e exportação.

## 4. Decisões vigentes da meta (valem mais que o Mestre_BI)

- Meta Hora BI = meta cheia × Minutos BI ÷ Minutos. Sem meta proporcional à refeição (revogada em 30/10/2026).
- As barras por hora usam a meta cheia.
- Desde 09/11/2026, o cartão Meta (HH Meta Útil) e a HH Aderência usam o fator de dia útil 21h45 = 1305/1440 (pausa fixa de 45 min em cada um dos 3 turnos, a mesma do OEE2), só quando não há hora filtrada (ISFILTERED na Hora BI). Com hora selecionada, a meta é a cheia.
- O fator de dia útil nunca entra no OEE2, porque descontaria a pausa duas vezes.
- O TCU do OEE2 conta as 11 máquinas.
- A produção da Trançagem no painel vem da Hora-Hora, não do evento Fim.
- OP cancelada não conta produção. Ao descartar, os eventos Parcial da ficha ficam com 0 m.
