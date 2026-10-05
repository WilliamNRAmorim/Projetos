# Auditoria GMS — 02 · `scr_Vulcanizacao_1` (v0.3.0 → v0.3.1)

Lida por inteiro (1.857 linhas, 104 controles). Dados conferidos em `ficha_producao.csv` (2.648 linhas, export de 02/10/2026).
QA do projeto: sem nenhum achado novo (`gms_qa_yaml.py`, idêntico ao baseline). Nenhum X/Y/Width/Height mudou; mesma lista de controles.

## Aplicado (v0.3.1)

| # | Onde | Problema | Correção |
|---|---|---|---|
| 1 | `btn_ConfirmarLoteVulca.OnSelect` | O lote não conferia `Errors(Historico_Carretel)`: falha na custódia do carretel passava calada (no início da vulcanização já era avisada). | Confere os três destinos (ficha, eventos, custódia). |
| 2 | idem | Em falha parcial, as OPs já lançadas continuavam na seleção e o modal ficava aberto; reenviar gravava **evento "Fim" duplicado** em `Eventos_Producao`. | Em falha: `Refresh`, zera a seleção e recarrega `colProntasVulca` (as OPs já lançadas saem da lista); mensagem diz o que fazer. |
| 3 | `btn_ConfirmarLoteVulca`, `btn_ConfirmarSetupVulca` | `_min: Hour(Now())*60+Minute(Now())` e `_agora: Now()` eram dois instantes diferentes; `data_ref` e `turno` recalculados à mão. | Um instante só (`agora`) e `fx_TurnoEm` / `fx_DataRefEm` (mesma regra, uma implementação). Removida a global `varQtdLote` (só alimentava um Notify). |
| 4 | `btn_AcaoVulca` | Não ficava desabilitado durante a gravação: toque duplo rodava a ação duas vezes (a conferência de `Modified` só mascarava com um erro confuso). | `DisplayMode` inclui `!varProcessando`. |
| 5 | `btn_ConfirmarSetupVulca` | Habilitava por `status_processo = "Aguardando"` (texto cru), enquanto o resto da tela usa `fx_EstadoVulca` (B §3.10). | Usa `fx_EstadoVulca(...) = "AGUARDANDO"` e `!varProcessando`. |
| 6 | `btn_SalvarEditarVulca` | Dava para salvar `Mangueira` em branco: o receita vira "n/d", a spec some e o Hora-Hora perde a mangueira. | Salvar desabilitado com mangueira vazia; os três campos vão com `Trim()`. |
| 7 | 6 labels de metragem | `Coalesce(campo, 0) & " m"` mostrava metragem inexistente como "0 m" (regra proibida do projeto). | `fx_MetrosUn(campo)`: vazio mostra "—". |
| 8 | 5 pontos | Capacidade da autoclave "5" escrita à mão (limite, texto do aviso, `/5`, DisplayMode, OnSelect). | `fx_AutoclaveMax` (Formulas §10). |
| 9 | 5 labels | Fontes `Arial` e `Segoe UI` soltas (a tela é Open Sans). | `fx_FonteFamilia`. |
| 10 | `lbl_TotalFilaVulca` | `Size: 14` e raio `5` literais. | `fx_FonteCorpo` e `fx_RaioS` (muda 1 px de tamanho e 3 px de raio). |

`Formulas.txt` v3.0.7 só **acrescenta** `fx_MetrosUn` e `fx_AutoclaveMax`. **Colar o Formulas no Studio antes da tela.**

## Não aplicado — precisa de decisão ou de teste no app real

1. **[DADO] Metragem herdada vazia ou zero.** `Coalesce(quantidade_bandagem, 0)` é *gravado* em `metros_entrada`, `quantidade_vulcanizacao` e nos eventos.
   Histórico: 222 de 2.606 OPs que concluíram a Vulcanização (8,5%) têm `quantidade_bandagem` em branco ou 0, e 205 saíram com
   `quantidade_vulcanizacao` 0/branco (parte é de antes da herança automática). Travar o início quando a metragem é 0 evitaria o zero calado,
   mas **deixa a OP presa em Aguardando** até alguém corrigir a Bandagem. William decide: travar, só avisar, ou deixar.
2. **[DADO] `Mangueira` editável em texto livre** (`inp_MangueiraEditarVulca`): erro de digitação cria uma mangueira que não existe em
   `colMangueiras`. Trocar por combo da `colMangueiras` muda o layout do modal, então fica para você ver.
3. **[DADO] `recurso` dos eventos = `_r.Trançadeira`.** O recurso físico da Vulcanização é a autoclave, não a trançadeira de origem; o
   ranking de recurso do BI mistura os dois. Pergunta: existe (ou vai existir) campo de autoclave na ficha?
4. **[PERF/UX] A fila só atualiza no ícone de refresh.** O timer de 30 s só move o relógio; uma OP que chega da Bandagem não aparece até
   alguém tocar em refresh. Um `Refresh(ficha_producao)` no `OnTimerEnd` é leitura (permitido, B §3.4), mas multiplica leituras por tablet;
   decidir junto com as demais telas de fila (Bandagem, Debandagem, Cobertura).
5. **[PERF] Receita lida 5 vezes** (`LookUp(colDM_BANDAGEM, fx_NormCodigo(...))`, 2 chamadas por label, e o `ctxAgora` de 30 s as
   reavalia). Coleção pequena, impacto baixo; vale um `ctx` calculado ao selecionar a OP quando a Bandagem for refeita.
6. **[A11Y] Nenhum controle tem `AccessibleLabel`** (B §5.4/5.5), e o botão "Editar Plano" usa caracteres invisíveis (`ㅤㅤ`) como
   espaçamento para o ícone. É padrão do app inteiro: tratar numa rodada única depois da leitura das 26 telas.
7. **[UI] `lbl_MenuLateralVulca` = "MENU LATERAL"** é texto de desenho, não de operador.
8. **[ESTILO] Versão em `Courier New`** (`lbl_VersaoVulca`): fixo por convenção? Confirmar nas demais telas.

## Leitura sem problemas
Estados por `fx_EstadoVulca` (função pura), `OnSelect: =Select(Parent)` em todo filho de galeria, conferência de `Modified` antes de
escrever, `Errors()` em toda gravação principal, relógio de tela por `ctxAgora` (sem `Now()` em exibição), `DelayOutput` nos campos
de texto, overlay de gravação por cima de tudo, tokens `fx_` em cor/raio/fonte (exceto os itens 9 e 10 acima, já corrigidos).
