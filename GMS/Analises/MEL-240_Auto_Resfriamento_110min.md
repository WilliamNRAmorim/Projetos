# MEL-240 — Vulcanização: virar RESFRIANDO sozinho aos 1h50 (110 min)

## Decisão de desenho
O estado da Vulcanização já é **derivado** de `InicioResfriamento_Vulcanizacao` (`fx_EstadoVulca`: vazio = VULCANIZANDO, preenchido = RESFRIANDO).
Então o jeito certo é **gravar esse campo sozinho** aos 110 min, não criar um segundo cálculo na tela:

- Verdade única (P7 pilar 1): Debandagem, Diário de Bordo da Autoclave (MEL-074) e BI leem o mesmo campo.
- O cronômetro do RESFRIANDO nasce em `inicio + 110 min` (hora exata, mesmo que o fluxo rode atrasado).
- `Patch` dentro de Timer é PROIBIDO (norma), então quem grava é um fluxo agendado (C29).
- **Nenhuma mudança na `scr_Vulcanizacao_1`**: ela já relê a lista a cada 120 s e o botão manual "Iniciar Resfriamento" continua valendo se o operador acionar antes dos 110 min (a checagem de `Modified` já resolve a corrida entre os dois).

## Fluxo `GMS_AutoResfriamentoVulca` (Power Automate, nuvem, agendado)
1. **Recurrence**: a cada 5 min (24 h).
2. **Get items** (`ficha_producao`), Filter Query:
   `processo eq 'Vulcanização' and status_processo eq 'Em processo' and InicioResfriamento_Vulcanizacao eq null and data_hora_inicio_vulcanizacao ne null and data_hora_inicio_vulcanizacao le '@{addMinutes(utcNow(), -110)}'`
   - Top Count 50. Se o Studio reclamar de coluna não indexada, indexar `status_processo`.
3. **Apply to each** → **Update item** (mesma lista, Id do item):
   - `InicioResfriamento_Vulcanizacao` = `addMinutes(items('Apply_to_each')?['data_hora_inicio_vulcanizacao'], 110)`
   - Não mexer em mais nenhum campo (nem Status, nem operador).
4. Sem Condition de re-checagem: o filtro já exige o campo vazio; se o operador apertou o botão no meio, o item some do filtro.
5. Fuso: gravar o valor que veio da lista + 110 min direto (ambos UTC no SharePoint). **Não** usar convertTimeZone.

## Teste (no app publicado, OP de teste)
1. Iniciar uma vulcanização e, no SharePoint, recuar `data_hora_inicio_vulcanizacao` em 111 min.
2. Rodar o fluxo na mão: o campo `InicioResfriamento_Vulcanizacao` deve ficar = início + 110 min.
3. Na tela, em até 2 min: badge vira "Resfriando", cronômetro mostra ~1 min, botão de envio para Debandagem aparece.
4. Repetir com OP cujo resfriamento já foi acionado à mão: o fluxo não pode tocar nela.

## Decisões do William
- 110 min é **fixo para todas as mangueiras** (06/10/2026): o filtro do fluxo fica como está, sem consultar a receita.
- Em aberto (não bloqueia): o aviso "⚠ Ciclo acima do tempo de receita" só aparece em VULCANIZANDO; com receita > 110 min ele nunca vai aparecer. Se quiser, o aviso passa a valer também em RESFRIANDO.
