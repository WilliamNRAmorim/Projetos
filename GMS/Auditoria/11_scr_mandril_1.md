# Auditoria GMS — 11 · `scr_mandril_1` (v0.5.4 → v0.5.5)

Lida por inteiro (3.937 linhas, 169 controles). QA do projeto idêntico ao baseline; nenhum X/Y/Width/Height mudou; mesma lista de controles; parênteses balanceados.
O Mandril é a primeira etapa: não recebe metragem de etapa anterior, e a "fila" é a lista de bitolas (PN). Por isso a regra de margem vale contra o saldo do mandril novo.

## Aplicado (v0.5.5)
| # | Onde | Problema | Correção |
|---|---|---|---|
| 1 | Carga do posto (`btn_CarregarPostoMand_2`) | ~12 chamadas ao servidor em fila (3 `Refresh` e 3 `ClearCollect` um depois do outro) a cada abertura da tela e a cada atualização. | `Concurrent` nos três `Refresh` e nos três `ClearCollect`, com aviso se o servidor falhar. Mesmos dados, menos espera. |
| 2 | Relógio do kanban | 180 s e rodava com o operador no meio de um modal. | 120 s e só com operador ocioso (sem gravação e sem modal aberto). Lê só o kanban; não mexe nos campos digitados. |
| 3 | Salvar Parcial | Aceitava quantidade vazia (gravava 0) e a diferença negativa podia deixar o turno negativo; não carimbava `Turno_mandril`. | `fx_MetragemOk` com aviso; turno nunca abaixo de zero (`Max(0, ...)`); carimba o turno como as outras telas. |
| 4 | Enviar p/ Tubo | Mesma lacuna: enviava com `Coalesce(...,0)`; baixa do carretel marcava `Tubo` sem checar `Errors`. | `fx_MetragemOk` (botão e `OnSelect`), turno nunca negativo e `Errors(lista_carreteis)` com aviso. |
| 5 | Aviso novo | Soldar mais metros do que o mandril novo tinha passava calado. | Alerta âmbar quando a quantidade passa do saldo do carretel de mandril novo (margem 10%). Só avisa. |
| 6 | Confirmar início | Lia o estoque de mandril novo sem `Refresh` (dois operadores podiam pegar o mesmo carretel); `_min` + `fx_Turno(_min)`. | `Refresh(CarreteisMandril)` antes de conferir; `fx_TurnoEm(_agora)`. |
| 7 | Estado da OP | `_r.status_processo <> "Em processo"` em 5 pontos. | `fx_EstadoContinuo(...) <> "PRODUZINDO"`. |
| 8 | Exibição | Quantidade inicial aparecia "0" e metros do mandril usavam `Coalesce(...,0)`. | Campo começa vazio; `fx_MetrosUn` ("—" quando vazio) em 3 pontos. |
| 9 | Carga de DM_MANDREL | Falha de leitura virava "sem set-up". | `IfError` + aviso. |
| 10 | Padrão visual | `Arial`, `Segoe UI`, tamanhos 15 (×2) e 12 soltos. | `fx_FonteFamilia`, `fx_FonteSecao`, `fx_FonteCorpo`. Lote com `Trim`. Versão 0.5.5. |

## Não aplicado
- **Ø do mandril** vem do PN (FM00480 → 0,480) e não é digitado; nada a conferir com o delineamento.
- Fonte `Courier New` nos códigos PN: parece escolha de design para código de peça, mantida.
- A11Y (rodada final): "MENU LATERAL", caracteres invisíveis nos botões do menu lateral e `AccessibleLabel` nos botões.
- Layout: menu lateral e rodapé seguem iguais (mock da Debandagem em discussão).
