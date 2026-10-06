# Auditoria 22 — scr_FichaTecnica_1 (v1.2.1 → v1.2.2)

Leitura linha a linha (1.208 linhas). Tela somente leitura, já no padrão; geometria inalterada, QA sem novos achados.

- **Carga das 13 tabelas do delineamento** com `IfError` e aviso (antes, se uma falhasse, a etapa aparecia vazia e o texto dizia "sem delineamento cadastrado", o que acusa a Engenharia por um problema de rede).
- Cache mantido: as tabelas só carregam se a coleção estiver vazia; mudança da Engenharia aparece depois de reabrir o app.

## Não mexido de propósito
Nenhuma lógica das abas; códigos de mandril, bobinagem e trançagem continuam escolhidos à mão. Ideia para depois (precisa de dado para validar): pré-selecionar o código quando a mangueira só tem uma opção.

## Observação sobre a conferência
`scr_ConferenciaSAP` foi devolvida ao estado v0.1.1 (sem as travas de status e sem IfError) a pedido do William: a lógica dela não se mexe. O selo de pendências abertas na Gestão continua.
