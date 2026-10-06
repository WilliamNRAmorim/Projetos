# Auditoria 20 — scr_HistoricoTurno_Mandril e scr_HistoricoTurno_Tubo

Leitura linha a linha das duas (600 linhas cada). Geometria inalterada; QA sem novos achados (o ACHOU de Now() zerou nas duas).

## Corrigido
- **Mandril abria vazio:** o OnVisible usava `ctxAgora`, que não existe nessa tela, então a data de referência saía em branco e a consulta voltava sem linhas. O Tubo setava a variável, mas o relógio do rodapé usava `Now()` solto. Agora as duas usam `ctxHistAgora` (set ao abrir e a cada 30 s); botões Hoje e Próximo também.
- **Consulta pesada:** baixava os eventos de TODAS as etapas do dia e filtrava a etapa na tela (estourava o limite de 500 linhas). Agora o filtro de data e de etapa vai junto para o servidor.
- **Falha de rede** na carga agora avisa; antes a tela ficava vazia sem explicação.
- **Eventos Cancelado** (novo, do descarte de OP) aparecem em vermelho; cores por tipo vêm de `fx_CorTipoEvento`.
- Janela dos turnos: T1 termina e T2 começa às **13:57** (estava 13:48; a régua oficial é 05:20 / 13:57 / 22:41).

Mantido: filtros de turno por rótulo; coluna de balanço só nos eventos Fim.
