# Manual de B.O. do GMS (o jeito do William de achar e corrigir problema)

Versão 1.0 · 09/11/2026 · para o Uiu (Detetive e Mecânico). Nomes internos das colunas: 09_Mapa_Listas.md. Regras de turno e janelas: 06_Roteiro_HoraHora.md. SAP x GMS: 07_Dados_SAP_x_GMS.md.

## Como o William trabalha (vale para toda receita)
1. **Dado antes de opinião.** Toda afirmação sai de uma consulta, com OP, ID do item, etapa, turno e data de referência. Sem dado: "não encontrei".
2. **SAP é a verdade de quantidade.** O GMS é ajustado para bater com o SAP, nunca o contrário.
3. **Nunca zerar nem descartar por falta de match.** Nome que não bate se liga pela OP.
4. **Mostrar antes de mexer.** Toda correção mostra uma tabela antes → depois (lista, ID, campo, valor antigo, valor novo) e espera o "sim" do William. Um "sim" vale para um lote. Lote grande: de 5 em 5, os piores primeiro.
5. **Reler antes de gravar.** Só grava se o valor atual ainda é o que foi lido; senão pula e avisa. Depois de gravar, relê e confere.
6. **Guardar o valor antigo.** Cada correção gera uma linha no `Log_Uiu` (quando, item, campo, antes, depois, receita).
7. **Apagar nunca é definitivo.** Duplicado vai para a lixeira (restaurável), e quem apaga é o William. O Uiu não cria nem apaga item.
8. **Uma pergunta diagnóstica.** Em dúvida, uma pergunta objetiva ao William, não três hipóteses.
9. **Espera não é parada.** OP na fila é "aguardando desde", nunca "parada desde". Parada de máquina vem da Hora-Hora (`field_11`) e da Paradas_Montagem.
10. **Parada, pausa e tempo excedido nunca se somam.** Motivo do tipo Programada (Refeição, Reunião, Set-up, Manut. Preventiva, Check List, Amostra, MPT, TESTE ENGENHARIA) é pausa.
11. **Horário em UTC.** Brasília = UTC − 3 h. Dia produtivo começa 05:20 de Brasília (08:20 UTC). O 3º turno fica com a data do dia em que começa: 00:00–05:19 pertence ao dia anterior.
12. **Fronteiras de turno vigentes (NORMA 27/10/2026, MEL-250):** 1º 05:20–13:56 (min 320–836), 2º 13:57–22:19 (837–1339), 3º 22:20–05:19 (1340–319).

Cada receita traz: **Sintoma · Consulta · Como confirmar · Causa provável · Correção · Catálogo F3** (se o Mecânico pode corrigir sozinho com "sim" ou se é só relato).

---

## 1. OP travada na etapa
**Sintoma.** "Cadê a OP X?", OP que não aparece na fila da etapa seguinte, painel com OP há muitas horas na mesma etapa.

**Consulta.**
1. `ficha_producao` com `OP eq X` → `ID`, `field_10` (etapa atual), `field_11` (situação), início e fim da etapa atual (ex.: Trançadeira `field_19`/`field_20`), quantidade da etapa.
2. `Eventos_Producao` com `origem_ID eq <ID da ficha>`, ordenado por `data_hora` desc, Top 20.
3. Se a etapa usa carretel: `lista_carreteis` / `Historico_Carretel` pelo carretel do último evento.

**Como confirmar.**
- Início preenchido, fim vazio, último evento é Início ou Parcial, e nenhum Hora-Hora da máquina com essa mangueira depois → **etapa esquecida aberta** (operador não fechou).
- Existe evento Fim da etapa, mas a ficha não avançou (`field_10` ainda na etapa, fim vazio) → **gravação parcial** (o evento foi e a ficha não; acontece em lote quando um Patch falha no meio).
- `field_11` = 'Aguardando' na etapa seguinte → não está travada: **está na fila**. Responda "aguardando na etapa X desde ...".
- Ficha com quantidade menor que o lote e ficha irmã "(devolvida)" → foi **dividida pelo Tubo** (split), não sumiu.
- Evento Parcial no fim do turno é normal: é fechamento de turno com a etapa aberta.

**Causa provável.** Operador esqueceu de fechar; falha de gravação no lote (Vulcanização em lote já duplicou e perdeu Fim); carretel de saída não liberado.

**Correção.**
- Etapa esquecida: fechar com fim = `data_hora` do último evento Fim/Parcial ou do último Hora-Hora da OP. Sem horário com evidência, perguntar ao William o horário real. Nunca inventar.
- Gravação parcial: alinhar a ficha ao evento Fim (fim da etapa = `data_hora` do Fim, quantidade = `metros` do Fim, `field_10` = etapa seguinte, `field_11` = 'Aguardando').
- Falta o evento Fim: o Uiu não cria evento. Relatar ao William para lançar pelo app.

**Catálogo F3.** Sim: "fechar etapa esquecida" (só campos de fim, etapa e situação da ficha).

---

## 2. Turno T2 que devia ser T3 (22:20–22:40, de 05/10 a 27/10/2026)
**Sintoma.** 2º turno com produção "a mais" e 3º "a menos" nesse período; janela "22:00 - 22:20" com 41 minutos na Hora-Hora; fim de etapa às 22:2x/22:3x marcado como turno 2.

**De onde vem.** De 05/10 (MEL-198) a 27/10/2026 (MEL-250) o app virava o 3º turno às 22:41. A NORMA vigente diz 22:20. Tudo o que foi gravado entre 22:20 e 22:40 (horário de Brasília) nesse período ficou como Turno 2.

**Consulta.**
- Hora-Hora: `TurnoH eq '2º Turno'` e `field_3 eq '22:00 - 22:20'` e `Minutos eq 41`, por faixa de ID (a contagem de 29/10 achou 146 linhas, IDs 28835 a 31767, todas Finalizado).
- ficha_producao: fichas com fim de etapa (`field_9`, `field_17`, `field_20`, `field_26`, `field_32`, `field_36`, `field_40`, `field_44`) entre 22:20 e 22:40 de Brasília (01:20–01:40 UTC do dia seguinte) de 05/10 a 27/10 e turno da etapa = 2 (contagem de 29/10: 46 fins de etapa).
- Eventos_Producao: `turno eq 2` com `data_hora` entre 01:20 e 01:40 UTC do dia seguinte (= 22:20–22:40 de Brasília), de 05/10 a 27/10.

**Como confirmar.**
- Converter o horário de UTC para Brasília antes de comparar.
- Só entra o que caiu em 22:20–22:40 **e** com data de 05/10 a 27/10. Antes de 05/10 também há divergência, mas por outra regra: não misture.
- Na ficha, o turno vale o horário do **fim** da etapa (gravação feita no fim).

**Causa provável.** Regra antiga do app (22:41), não erro do operador.

**Correção (proposta, aguarda o William).**
- Ficha: T2 → T3 só se o fim da etapa caiu em 22:20–22:40 nesse período; mover junto a quantidade de `Qtd_Turno2` para `Qtd_Turno3`; guardar o valor antigo.
- Hora-Hora: **não** trocar o `TurnoH` da janela de 41 min inteira, porque ela tem 20 min de T2 (22:00–22:19) e 21 min de T3 (22:20–22:40). Dividir a janela ou marcar "a conferir", conforme decisão do William. Não recalcular Tempo Parado sem a regra aprovada (Tempo Parado é automático desde MEL-255).
- Decisões que faltam do William: data exata da volta para 22:20 (27/10 ou ~29/10); se registros antes de 05/10 entram; como dividir a janela de 41 min (inclusive o Tempo Parado calculado sobre os 41 min).
- Até lá: ao comparar turnos desse período, **avise que a fronteira mudou** e não corrija.

**Catálogo F3.** Sim ("corrigir turno"), mas só depois da decisão escrita do William sobre as regras acima e da revisão do `revisor`.

---

## 3. Mangueira do GMS sem match no SAP
**Sintoma.** Na conferência GMS x MB51 uma mangueira "não existe" no SAP, ou aparece com produção zero de um lado.

**Consulta.**
1. Pegue as OPs dessa mangueira na `ficha_producao` (`Mangueira eq '...'`).
2. Para cada OP: `Plano_OPs` com `Title eq '<OP>'` → `PN`; no export da MB51, a mesma OP (`Order`) → `Material` e `Material Description`.

**Como confirmar.**
- Mesma OP nos dois lados e material SAP com descrição parecida → é **apelido** (alias). Exemplos conhecidos: GH493-6/8/10/12/16 = "HOSE R12"; GH781-6 = "HOSE-AER, GH781, -6, R2/2SC"; 2583-12 = código 12055040; HC101-6 tem descrição "-5" no SAP. A tabela de apelidos aprovados é mantida pelo William fora do Uiu; na dúvida, pergunte se o par já está nela.
- Mesma OP, mas o SAP diz outra mangueira (outro produto) → **divergência real da OP**, não alias. Relatar.
- OP do GMS que não existe no SAP → digitação de OP (ver receita 4).

**Causa provável.** O nome no GMS é o do chão (PN curto), o do SAP é a descrição do material.

**Correção.** Nunca zerar, nunca descartar a mangueira. Ligar pela OP e comparar por material. Se for alias novo, propor a linha para a tabela de aliases (o William aprova).

**Catálogo F3.** Não (é regra de análise, não gravação).

---

## 4. Divergência GMS x MB51 (produção boa)
**Sintoma.** Produção do GMS não bate com o SAP por mangueira, por OP ou no mês.

**Consulta.**
- GMS: produção boa = `field_46` (quantidade da Extração) da `ficha_producao`, por OP; refugo GMS = `TiposErros` pela OP.
- SAP (export MB51): por OP (`Order`), só unidade **M**, movimento 101 menos 102, **sem** os lançamentos dos usuários de refugo (U445131 e U452021).
- Somar por mangueira: divergência = **soma SAP − soma GMS**. Negativa = faltou lançar no SAP; positiva = sobrou no SAP.

**Como confirmar.**
- Faltou e sobrou se somam **separados**, por material. Material não compensa com material.
- Lance mandado na OP vizinha é costume: falta numa OP e sobra igual em outra OP do mesmo material, e se anulam dentro do material.
- Comparação lance a lance por OP aceita soma de lances (10 + 20 + 30 = 60).
- OP que só existe no SAP entra na conta da mangueira **só se diminuir** a divergência dela.
- Período: os exports são fotografias (diga a data de corte). Mês pequeno e troca de OP que atravessa meses distorcem.

**Causa provável.** OP digitada errada no GMS, lance mandado em outra OP, ficha sem extração lançada, estorno 102 esquecido.

**Correção.**
- Objetivo: o GMS é espelho do SAP. A OP do SAP manda.
- Ficha de OP que só existe no GMS e corresponde a uma OP só do SAP (mesmo material, mesma metragem, mesmo período): trocar a OP da ficha pela do SAP (regra de 15/10); a metragem do SAP fica na ficha.
- Reconstruir de 5 em 5 OPs, as piores primeiro, mostrando antes de pedir o lote todo. A fonte dos lances perdidos é o BD Packing List.

**Catálogo F3.** Sim: "trocar OP pela do SAP na ficha só-SAP". O resto é relato.

---

## 5. Hora-Hora sem apontamento
**Sintoma.** Janela vencida sem linha, turno inteiro faltando para uma máquina, ou linha abaixo da meta sem motivo.

**Consulta.**
- Hora-Hora da máquina e do dia: `field_2 eq '<máquina>'` e `field_0` do dia (ou por faixa de ID se estourar 5.000), Top 50.
- Contar janelas por turno e somar `Minutos`: grade 517 / 524 / 399 de 05/10 até a publicação da v3.0.15; 517 / 503 / 420 (2º com 9 janelas, 3º com 8) depois. A data da publicação (27/10 ou ~29/10) falta o William confirmar: linhas de 27 a 29/10 são "a conferir".
- `ficha_producao`: havia OP em processo na máquina nesse horário?

**Como confirmar.**
- Falta a combinação Data + Turno + Célula, ou o turno tem menos janelas que a grade → **lacuna**.
- Turno sem nenhuma linha e sem OP na ficha → provável máquina parada / turno não trabalhado. Com OP rodando na ficha → apontamento perdido.
- Linha com Real abaixo da Meta e Motivo vazio → **ND** (Motivo Não Declarado). Motivo preenchido e Tempo Parado ≤ 0 → **NT**. Tempo Parado maior que os Minutos da janela → **CAP**.
- Repetição da mesma Data + Turno + Célula + Hora → duplicado (ver receita 6).

**Causa provável.** Operador não apontou; turno parado sem registro; janela fechada sem apontamento.

**Correção.**
- Regra do Fechar turno (só janelas de dias passados, `Minutos` > 0 e `Meta` > 0):
  - ND: `field_12` = "Motivo Não Declarado" e `field_11` = min(Minutos, arredondar(Minutos × (Meta − Real) ÷ Meta)).
  - NT: mesmo `field_11` proporcional; o motivo fica. **Exceção:** se o motivo for do tipo Programada (Refeição, Almoço, Reunião, Set-up, Manut. Preventiva, Check List, Amostra, MPT, TESTE ENGENHARIA), o tempo é pausa: não entra em parada real nem em "parado no turno" (o BI tira Almoço do Parado). Linha NT de motivo Programada já gravada com `field_11` proporcional: relatar; zerar ou só excluir na análise é decisão do William.
  - CAP: `field_11` = Minutos.
- O Tempo Parado automático foi decidido em 27/10 e publicado em 29/10/2026 (MEL-252/MEL-255). Antes de 29/10 vale a regra ND/NT/CAP; depois, ela só serve para linha gravada sem o cálculo.
- Turno inteiro faltando: o Uiu não cria linha. Relatar com o modelo (noite anterior da mesma máquina) para o William lançar. Lacuna sem evidência se registra, não se inventa.
- No painel, janela fechada sem apontamento em turno trabalhado conta como rodou (velocidade × minutos); turno sem nenhuma linha conta 0. Avise isso ao explicar números do painel.

**Catálogo F3.** Sim só para "reclassificar motivo de parada" (`field_12`) com o "sim" do William. Recalcular `field_11` (ND/NT/CAP) é cálculo de parada: só depois da revisão do `revisor` e com a regra acima.

---

## 6. Carretel duplicado
**Sintoma.** Mesmo carretel em duas OPs ativas, evento Fim repetido, carretel "rodando sem carretel atrás" que não acende, metragem dobrada numa etapa.

**Consulta.**
- `Eventos_Producao` com `carretel eq '<n>'`, Top 20, ordenado por `data_hora`.
- `Eventos_Producao` com `origem_ID eq <ID>` e `tipo eq 'Fim'`: mais de um Fim da mesma etapa para a mesma ficha.
- `lista_carreteis` / `Historico_Carretel` pelo carretel.

**Como confirmar.**
- Duas OPs no mesmo carretel, uma rodando e outra aguardando, é **legítimo** (a fila conta carretel, não OP).
- Dois Fim da mesma etapa e mesma ficha com os mesmos metros e horários a segundos de distância → **duplicado de gravação** (reenvio após falha parcial do lote).
- Dois Fim com metros diferentes → pode ser fechamento em duas partes: não é duplicado sem conferir a ficha.
- Hora-Hora: mesma Data + Turno + Célula + Hora com conteúdo idêntico = cópia; com conteúdo diferente = divergência para o William decidir.

**Causa provável.** Operador reenviou o lote depois de um erro; toque duplo; carretel de saída não liberado.

**Correção.** O Uiu não apaga. Listar os pares (IDs, metros, horário) e propor qual fica: o desempate (maior ID ou o Finalizado) ainda é decisão do William. O que sai vai para a lixeira pelo William, nunca exclusão definitiva.

**Catálogo F3.** Não (é apagar). Só relato.

---

## 7. Evento Cancelado contado como produção
**Sintoma.** Produção de OP cancelada aparece no painel ou na soma da etapa; ficha Cancelado com metros.

**Consulta.**
- `ficha_producao` com `field_11 eq 'Cancelado'` (por período, Top 50) → IDs.
- `Eventos_Producao` com `origem_ID eq <ID>` → eventos com `metros` > 0.

**Como confirmar.**
- Evento `tipo` = Cancelado com `metros` > 0 → errado: Cancelado tem `metros` = 0 e `sobra` = metragem que virou refugo (NORMA 02/09).
- Eventos Parcial de ficha cancelada com `metros` > 0 → errado: ao descartar, os Parcial ficam com 0 m (DECISÃO 05/11, MEL-260). OP cancelada não conta produção.
- Fim de etapas anteriores ao cancelamento é produção real daquela etapa: não zere.
- No app, filtro `status_processo <> "Cancelado"` direto no SharePoint já devolveu zero linhas (lição de 15/10): se a fila sumiu, a causa pode ser essa, não o dado.

**Causa provável.** Cancelamento feito antes da regra; descarte que não zerou os Parcial.

**Correção.** Zerar `metros` do evento Cancelado (passando o valor para `sobra` se ela estiver vazia) e dos Parcial da ficha cancelada, com antes → depois e "sim".

**Catálogo F3.** Fora do catálogo inicial (precisa liberar a ferramenta de atualizar Eventos_Producao). Até lá, relato com a tabela pronta para o William.

---

## Achados frequentes que não são B.O.
- Máquina com nomes diferentes (TH07/TH-07): normalize antes de somar.
- `recurso` do evento é a trançadeira de origem, não a máquina da etapa.
- `Quantidade_mandril` menor que o lote por split do Tubo.
- Valores 111/1111/11111 são preenchimento, não metragem.
- Factbird só cobre a TH07: não serve para conferir outras máquinas.
- Parada de 04 a 26/07/2026 sem produção (provável férias).
