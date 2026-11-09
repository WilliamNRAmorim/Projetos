# Roteiro da Hora-Hora: como a lista funciona e como saber se está certa

Base de conhecimento do Uiu. Fonte: roteiro escrito em 28/10/2026 e atualizado em 30/10/2026 (revisão de 09/11/2026 para os 21h45). Serve para explicar, conferir e diagnosticar a lista Hora-Hora do GMS.

Turnos do hose cell: 1º 05:20–13:57; 2º de 13:57 (hora extra até 23:20); 3º 22:20–05:20. A Hora-Hora da Montagem não troca de turno sozinha.

Tempo Parado do Hora-Hora é automático e não editável (decidido em 27/10, publicado em 29/10/2026, MEL-255); Motivo obrigatório marcado em vermelho.

Correção na lista: só com confirmação do William, backup antes, apagar só para a lixeira, nunca em definitivo. O Uiu não corrige nada: aponta o problema e orienta quem pode corrigir.

## 1. O que é a Hora-Hora

- Lista SharePoint chamada **Hora-Hora**, no site OperationsGuaratingueta. É o "banco de dados" do apontamento hora a hora da produção.
- Cada linha é uma janela de tempo (uma hora ou parte dela) de uma célula/máquina, em um turno, em um dia, com a meta, o real produzido, o tempo parado e o motivo.
- O Power BI lê essa lista no modelo `(GMS)`, tabela `fHoraHora`.
- O app só mostra o dia corrente; o histórico se vê na lista e no BI.

## 2. Colunas da lista (nome interno e significado)

- `Title`: texto "DD/MM/AAAA - Nº Turno - CÉLULA".
- `field_0`: Data. É a data de produção do turno, gravada como meia-noite local (aparece como `...T03:00:00Z` na API). O 3º turno fica com a Data do dia em que começa.
- `field_2`: Célula (máquina, ex.: TH07).
- `field_3`: Hora, o rótulo da janela (ex.: "06:00 - 07:00").
- `field_4`: Mangueira.
- `field_5`: Meta Hora (meta da janela).
- `field_6`: Meta Acum (meta acumulada no turno, na ordem das janelas).
- `field_7`: Real. Hora (produzido na janela).
- `field_8`: Real. Acum (real acumulado).
- `field_9`: Diferença = Meta − Real.
- `field_11`: Tempo Parado, em minutos.
- `field_12`: Motivo (da parada ou da perda).
- `field_13`: Motivo 2.
- `field_14`: Comentário.
- `field_15`: Rendimento (%) = Real ÷ Meta × 100.
- `TurnoH`: Turno ("1º Turno", "2º Turno", "3º Turno").
- `Status`: "Finalizado" quando a janela foi fechada.
- `Minutos`: duração da janela, em minutos.

Motivos oficiais: vêm da lista de motivos de parada do app (ex.: "Amostra", "Refeição", "Almoço", "Motivo Não Declarado"). Em outubro os motivos são sem número; em setembro tinham número na frente (ex.: "21 - Refeição").

## 3. Dia produtivo, turnos, janelas e minutos

O dia de produção vai de **05:20 a 05:20**. O 3º turno fica com a Data do dia em que começa.

Janelas de um dia (rótulo: minutos). A grade mudou pela NORMA de 27/10/2026 (MEL-250); use a do período da linha:

**Depois da publicação da v3.0.15 (27/10 ou ~29/10/2026, data a confirmar com o William; linhas de 27 a 29/10 "a conferir"). Vigente: T1 05:20 = minuto 320, T2 13:57 = 837, T3 22:20 = 1340:**
- **1º turno** (517 min): 05:20 - 06:00: 40; de 06:00 - 07:00 até 12:00 - 13:00: 60 cada; 13:00 - 13:57: 57.
- **2º turno** (503 min): 13:47 - 15:00: 63 (rótulo antigo, janela começa 13:57); de 15:00 - 16:00 até 21:00 - 22:00: 60 cada; 22:00 - 22:20: **20**.
- **3º turno** (420 min): 22:20 - 23:00: **40**; de 23:00 - 00:00 até 04:00 - 05:00: 60 cada; 05:00 - 05:20: 20.

**De 05/10/2026 até a publicação da v3.0.15 (o app virava o 3º turno às 22:41, MEL-198, revogado):**
- 2º turno 524 min, com a janela 22:00 - 22:20 de **41** min; 3º turno 399 min, com 22:20 - 23:00 de **19** min.
- Por isso, apontamentos feitos entre 22:20 e 22:40 nesse período estão gravados como 2º Turno (146 linhas de Hora-Hora, IDs 28835 a 31767, e 46 fins de etapa na ficha, contagem de 29/10). A regravação para 3º Turno depende do William (ver Manual_BO, receita 2). Ao comparar turnos desse período, avise que a fronteira mudou.
- Antes de 05/10, parte do app virava o 2º turno às 13:47/13:48.

Pontos de atenção:

- O 2º turno tem 9 janelas e o 3º tem 8 (17 linhas por máquina por tarde+noite).
- Não "corrigir" minutos de janela antigos para a grade nova sem decisão do William.
- A Hora-Hora da Montagem não troca de turno automaticamente.

## 4. Regra do "Fechar turno" (ND, NT, CAP)

Vale para janelas **fechadas**, com `Minutos` > 0 e Meta > 0. "Abaixo da meta" significa Real < Meta.

- **ND (Não Declarado)**: abaixo da meta e Motivo vazio. O Motivo vira "Motivo Não Declarado" e o Tempo Parado vira o menor entre Minutos e o proporcional: arredondar(Minutos × (Meta − Real) ÷ Meta).
- **NT** (sigla do roteiro; parado sem tempo): abaixo da meta, Motivo preenchido e Tempo Parado ≤ 0. O Tempo Parado vira o mesmo proporcional; o motivo fica como está. Exceção: motivo do tipo Programada (Refeição, Almoço, Reunião, Set-up, Manut. Preventiva, Check List, Amostra, MPT, TESTE ENGENHARIA) é pausa e não entra em parada real (MEL-247); o que fazer com essas linhas é decisão do William.
- **CAP**: Tempo Parado maior que Minutos. O Tempo Parado é limitado a Minutos.

Exemplo ilustrativo (números de conta, não de uma linha real): uma janela de 60 min com meta 116 e real 103 dá 60 × 13 ÷ 116 = 7 min de parado proporcional (arredondado).

## 5. Como identificar problemas na lista

### Linha com valor errado (saúde do apontamento)

Procure janelas fechadas (dias anteriores a hoje) com:

- Real abaixo da meta e Motivo vazio (caso ND).
- Real abaixo da meta, Motivo preenchido e Tempo Parado zero ou vazio (caso NT).
- Tempo Parado maior que os Minutos da janela (caso CAP).

Histórico: em 23/10 foram achados 80 casos (30/09 a 22/10) e 79 (04 a 29/09); depois da correção a conferência deu zero.

Casos que **não** são correção automática (o William decide item a item):

- **Velocidade errada**: meta por minuto fora do padrão da mesma máquina e mangueira. Em outubro, todas as 95 linhas eram de TH01 e TO04 (duas passadas, MEL-241). A decisão da meta das duas passadas está adiada pelo William.
- Mangueira diferente da OP em processo; duplicados com conteúdo diferente; Title diferente da Célula; Data diferente do Title (MEL-243, ver LEIA-ME da pasta de higienização).
- **Janeiro até 03/09/2026**: não tem `Minutos` (a coluna nasceu em 03/09, MEL-100) e a meta antiga era inflada (MEL-106). Não há base para recalcular; não alterar.
- **O dia de hoje**: janelas ainda abertas, não entram na conferência.

### Linha faltante

Um turno completo sem registro (ex.: máquina parada na noite e ninguém apontou). Como conferir:

- Para cada máquina e dia, devem existir o 1º turno (soma de 517 min), o 2º e o 3º (503 e 420 depois da v3.0.15; 524 e 399 de 05/10 até ela), cada um com todas as janelas.
- Faltou uma combinação Data + Turno + Célula, ou o turno tem menos janelas que o esperado (2º: 9; 3º: 8).
- A soma de minutos do dia por máquina deve fechar 1.440 no BI (valores do BI no roteiro de 28/10, grade antiga: 1º 507, 2º 534, 3º 399; confira com a grade vigente).
- Antes de afirmar que falta, confirmar que realmente não existe registro daquela Data + Turno + Célula.

Como se cria uma noite faltante (quem faz é o William ou quem ele autorizar): usa-se como modelo a noite anterior da mesma máquina (mangueira e meta por janela); Meta Acum e Real Acum acumulam na ordem das janelas; Diferença = Meta − Real; em parada total, Real = 0, Tempo Parado = Minutos da janela, só o Motivo preenchido (Motivo 2 vazio) e Status "Finalizado". Exemplos já feitos: TH06, noite de 23/10 (Motivo "Amostra"); TH07, 2º e 3º turno de 26/10 (Motivo "Manutenção Preventiva", 17 linhas).

### Linha duplicada

- Mesma Data + Turno + Célula + Hora aparecendo mais de uma vez.
- Se o conteúdo é idêntico, é cópia; se o conteúdo é diferente, é divergência que o William precisa decidir.
- Depois de uma gravação que "pareceu falhar", releia a lista antes de repetir, para não duplicar.
- A exclusão só vai para a lixeira (recuperável por 93 dias) e só com confirmação do William.

## 6. O modelo `(GMS)` no Power BI (visão geral)

A tabela `fHoraHora` tem colunas calculadas que ajustam a leitura:

- `Data BI` = Data, pela regra do dia 05:20 a 05:20. O relacionamento ativo com o calendário usa `Data BI`.
- `Hora BI` = cópia da Hora, ordenada por `HoraOrdem BI`.
- `Minutos BI`: tira 10 minutos da janela 13:00-13:57 e põe na 13:47-15:00 (os 10 min de 13:47 a 13:57 pertencem ao 2º turno).
- `Real BI` e `Parado BI`: 10/57 do real e do parado da janela 13:00-13:57 passam para a janela 13:47-15:00 da mesma máquina e dia.
- `Meta Hora BI`: ver decisão vigente abaixo.
- As colunas calculadas só têm valor depois de um refresh do modelo.
- O agendamento de atualização tem limite de 8 horários por dia na capacidade compartilhada. Horários atuais: 08:00, 10:30, 13:00, 13:30, 14:00, 16:00, 17:30 e 20:00. O William preferiu manter assim.
- O relatório só vale depois que o William reabre o projeto no Desktop e publica; o modelo só vale depois do refresh.

## 7. Decisões vigentes (a seção 11 do roteiro substitui a seção 10)

A seção 10 do roteiro original trazia decisões de 23/10. A seção 11 (30/10, com a atualização de 09/11) **substitui a 10**. Vale apenas o que está abaixo.

- **Meta do BI NÃO é proporcional à refeição.** `Meta Hora BI` = Meta Hora × Minutos BI ÷ Minutos. A hora do jantar mostra a meta cheia. A decisão de 23/10 ("meta proporcional") foi revogada pelo William em 30/10.
- **Regra dos 21h45 (1305/1440)**: vale só nas medidas do relatório "HH Meta Útil (m)" (cartão Meta) e "HH Aderência", e só quando nenhuma hora está filtrada. A pausa é de 45 min em cada um dos 3 turnos (135 min por dia), a mesma do OEE2. Era 21h35 (1295/1440) até 09/11/2026, quando o William alinhou a regra com a pausa do OEE2 (MEL-266). As barras por hora usam a meta cheia.
- **Parado e Principal parada** seguem sem a refeição (o motivo "Almoço" do Motivo Padrão fica fora).
- Dia produtivo: 05:20 a 05:20.
- Os 10 min de 13:47 a 13:57 vão para o 2º turno (minutos, meta, real e parado).
- Janeiro até 03/09/2026: não se mexe.
- Meta das duas passadas (TH01 e TO04, MEL-241): decisão adiada.
- Atualização do modelo com 8 horários por dia.
- Pendências conhecidas do roteiro: refresh e publicação do relatório com `Real BI` e `Parado BI`; depois do refresh, a medida do modelo `'Hora-Hora'[Real HH]` passa a somar `Real BI`; decisão da meta das duas passadas.

## 8. Como explicar um número do painel

- Mostrar a linha da lista que o gera. Exemplo: 116 × 13 ÷ 60 = 25.
- O Tempo Parado do BI exclui "Almoço"; o campo bruto da lista não exclui.
- Validação típica com um caso real (ex.: TH07 em um dia): comparar Minutos BI por turno (grade antiga do roteiro: 1º 507, 2º 534, 3º 399, total 1.440; confira com a grade vigente), a meta, o real e o parado com o rodapé do app.
- Se a pessoa pergunta "por que mudou a lógica de X", a resposta está no histórico do diário do GMS; não invente a razão.

## 9. Como responder (orientação para o Uiu)

- Pedido curto e coloquial (ex.: "TH7 só o 1º turno está sem manutenção") é pedido para ler a lista e achar a lacuna.
- Use o que está nos dados, não o que a pessoa lembra: já houve "corretiva" dito e "preventiva" na lista.
- Diga de qual dia, turno e máquina vem cada número, e avise que os dados de hoje podem estar incompletos (janelas abertas).
- Qualquer correção de dados na lista passa pelo William: backup antes, só lixeira, nunca apagar em definitivo.
