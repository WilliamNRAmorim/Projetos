# Auditoria GMS — 08 · `scr_Finalização_1` (v0.4.0 → v0.4.1)

Lida por inteiro (3.085 linhas, 154 controles → 156). QA idêntico ao baseline; nenhum X/Y/Width/Height existente mudou; parênteses balanceados.
Dados: `RegistrosInspeção.csv` (16.542 linhas).

## Aplicado (v0.4.1)

| # | Onde | Problema | Correção |
|---|---|---|---|
| 1 | 18 cargas de `colLancesExt`, `colRefugoExt`, `colInspDiaExt` | Falha de leitura virava lista vazia, sem aviso (o operador acha que a OP não tem lance). | Cada carga em `IfError(..., Notify(...))` (7 + 6 + 5). Diagnóstico de 05/10 (Auditoria 01 §6). |
| 2 | Edição de lance | Salvar uma edição regravava `DataHoraInspecao` e `TurnoTeste` com o instante da correção: lance do 1º turno corrigido no 2º virava produção do 2º. | Edição preserva data e turno originais (`Coalesce(registro.campo, agora)`). **Decisão a confirmar** (ver abaixo). |
| 3 | Medidas | 3,2% dos Ø internos, 2,7% dos Ø externos e 5,7% das concentricidades estão > 5: milésimo digitado no lugar de polegada (a spec é polegada). | `fx_DiametroPol` nos três campos (borda, habilitar, gravar). "412" vira 0,412. |
| 4 | Rótulos de acessibilidade | Diâmetros diziam "milímetros"; a tela e a spec são polegadas. | Corrigido nos três campos. |
| 5 | Iniciar Inspeção | Iniciava OP sem metragem recebida da Debandagem; estado por texto cru. | Bloqueia sem metragem (norma); estado por `fx_EstadoContinuo`. |
| 6 | Lance / refugo / finalizar | `<= 0` à mão em três pontos. | `fx_MetragemOk`. |
| 7 | Finalizar | Liberar o carretel (`Patch(lista_carreteis, LookUp(...))`) sem checar `Errors` e sem tratar carretel não encontrado. | Confere se achou e confere `Errors`; avisa que a ficha fechou mas o carretel não foi liberado. |
| 8 | Finalizar (modal) | Aprovado maior que o recebido não aparecia. | `lbl_AlertaMargemFinalizarExt` (só avisa, margem `fx_MargemMetragemPct`). |
| 9 | Fila | Só atualizava no ícone. | `tmr_AutoRefreshExt` (120 s, só ocioso: sem gravação e sem modal). |
| 10 | Turno | `_min` + `fx_Turno(_min)` em 6 pontos, `Now()` repetido. | `fx_TurnoEm(_agora)`; `_min` removido. |
| 11 | Editar OP | Mangueira em texto livre, sem `Trim`; salvava em branco. | `Upper(Trim())`; salvar desabilitado sem mangueira. Combo com "OUTRA" **não** aplicado aqui: Extração só corrige digitação, a Supervisão cuida do plano (aviso do próprio modal). |
| 12 | Metros | `Coalesce(x,0) & " m"` em 2 pontos. | `fx_MetrosUn`. |
| 13 | Visual | `Arial`, `Segoe UI` ×5, chip com raio 5 e tamanho 14; "Ø EXTERNO*" sem espaço; texto com aspas sobrando. | Tokens e ajustes. Versão 0.4.1. |

## A confirmar com o William
- **Edição preserva o turno original do lance.** Se a intenção era "o turno de quem corrigiu", é só voltar essas duas linhas.
- **Concentricidade com milésimo:** 946 valores > 5 (ex. 7, 1501). Tratei como milésimo; se a engenharia usa outra unidade ali, avisar.

## Não aplicado
- **Impressão da ficha** (`btn_ImprimirExt`, 26 lances por folha): aguardando o William descrever o problema da `TelaImpressao`.
- A11Y (rodada final): "MENU LATERAL", caracteres invisíveis em "Editar Plano" e "Imprimir Ficha", `AccessibleLabel` nos botões e ícones.
- Layout (mock em discussão): barra de ações única embaixo.
