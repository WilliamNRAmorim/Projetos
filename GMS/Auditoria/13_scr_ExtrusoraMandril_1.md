# Auditoria GMS — 13 · `scr_ExtrusoraMandril_1` (v0.2.1 → v0.3.0)

Lida por inteiro (3.124 linhas, 155 controles). QA do projeto idêntico ao baseline; nenhum X/Y/Width/Height mudou; mesma lista de controles; parênteses balanceados.
A tela já estava no padrão: `Errors()` depois de cada gravação, início desfeito se o carretel não reserva, relógio de 120 s só ocioso, conferência de `Modified`. O que ficou:

## Aplicado (v0.3.0)
| # | Onde | Problema | Correção |
|---|---|---|---|
| 1 | `inp_OpExt` | `HintText: =` com fórmula vazia (inválida). | `="Número da OP"`. |
| 2 | Quantidade | `Coalesce(fx_Num(...),0) > 0` espalhado; campo abria com "0". | `fx_MetragemOk` na borda, no botão e no `OnSelect`; campo começa vazio. |
| 3 | Aviso novo | Extrudar bem mais que o lote padrão do delineamento (`_34REEL_QTT`) passava calado. | Alerta âmbar acima da margem de 10%. Só avisa. |
| 4 | Refugo | `Title` ficava em branco quando a OP da extrusão não era digitada (coluna obrigatória no SharePoint: o refugo podia falhar). | `Coalesce(OP, carretel)`. |
| 5 | Cargas | 3 `Refresh` em fila a cada atualização e 2 `Refresh` + 2 `ClearCollect` ao confirmar início; `DM_MANDREL` sem tratar falha. | `Concurrent` e `IfError` com aviso. |
| 6 | Metros | `Text(x, "[$-pt-BR]#.##0") & " m"` em 5 pontos (depende do idioma, "0 m" em carretel sem metragem). | `fx_MetrosUn`, `fx_QtdBR`. |
| 7 | Visual | `Size: 10` solto. | `fx_FonteApoio`. Versão 0.3.0. |

## Não aplicado
- Mandril é a primeira etapa: não há metragem de etapa anterior para a regra de margem (só o lote padrão do delineamento, item 3).
- `Courier New` nos códigos PN: escolha de design, mantida.
- OP da extrusão continua opcional e só numérica (outras telas pedem 8 dígitos); decisão do William se quiser igualar.
- A11Y (rodada final): "MENU LATERAL", caracteres invisíveis nos botões do menu lateral.
- Layout: menu lateral e rodapé seguem iguais (mock da Debandagem em discussão).
