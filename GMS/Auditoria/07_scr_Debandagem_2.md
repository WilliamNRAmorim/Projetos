# Auditoria GMS — 07 · `scr_Debandagem_2` (v0.3.0 → v0.3.1)

Lida por inteiro (2.309 linhas, 120 controles → 125). QA do projeto idêntico ao baseline; nenhum X/Y/Width/Height existente mudou;
parênteses, colchetes e chaves balanceados.

## Aplicado (v0.3.1)

| # | Onde | Problema | Correção |
|---|---|---|---|
| 1 | Fila | Só atualizava no ícone de refresh. | `tmr_AutoRefreshDeband` (120 s) aperta o refresh só com operador ocioso (sem gravação e sem modal aberto). |
| 2 | Salvar parcial / Enviar / Confirmar | Metragem `<= 0` por `Coalesce(...,0)` em quatro pontos. | `fx_MetragemOk` em todos. Parcial grava a metragem sem `Coalesce`. |
| 3 | Início da debandagem | Iniciava OP sem metragem recebida da Vulcanização. | Bloqueia com aviso (norma "sem metragem, não segue"). |
| 4 | Balanço / alerta / saldo / modal | Vermelho e alerta para qualquer excesso, mesmo 1 m. | `fx_MetragemSubiu` (margem de `fx_MargemMetragemPct`); alerta mostra o % e a margem; modal avisa "acima da margem". |
| 5 | Turno | `_min` + `fx_Turno(_min)` em 11 pontos, com `Now()` repetido. | Um instante (`_agora`) e `fx_TurnoEm(_agora)`; `_min` removido. |
| 6 | 6 labels de metragem | `Coalesce(x,0) & " m"` mostrava "0 m" inexistente. | `fx_MetrosUn` ("—" quando vazio). |
| 7 | Editar OP | Mangueira em texto livre. | `cmb_MangueiraEditarDeband` (colMangueiras + "OUTRA") + `inp_OutraMangDeband` (caixa alta); salvar desabilitado sem mangueira/código; `Trim` nos três campos. Mesmo X/Y/W/H do campo antigo. |
| 8 | Fontes e chip | `Arial`, `Segoe UI` ×4, raio 5 e tamanho 14 soltos. | `fx_FonteFamilia`, `fx_RaioS`, `fx_FonteCorpo`. |
| 9 | Ícone do set-up | `ico_SetupLateralDeband` (Classic, feio). | `img_SetupLateralDeband` com Lucide `drafting-compass` (já importado). **Avisar o William.** |
| 10 | Versão | 0.3.0. | 0.3.1. |

Depende do `Formulas.txt` v3.0.8: colar **antes** da tela.

## Não aplicado
- Tensão de debandagem: a tela só mostra o delineamento (`TensaodeDebandagem`); não há valor digitado para comparar. Fica se a engenharia pedir o campo.
- `Coalesce(quantidade_vulcanizacao, 0)` gravado em custódia/evento no envio: protegido pela guarda de início (OP sem metragem não começa).
- A11Y (rodada final): "MENU LATERAL" como texto, "ㅤㅤEditar Plano" com caracteres invisíveis, `AccessibleLabel` nos botões.
