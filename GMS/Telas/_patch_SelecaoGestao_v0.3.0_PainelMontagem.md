# Patch · scr_SelecaoGestao_1 v0.2.0 → v0.3.0 · card "Painel da Montagem" (27/10/2026)

Ordem de colar: (1) o Painel da Montagem (`scr_PainelMontagem_1`) tem que existir no app antes do botão; (2) os 6 ajustes de largura abaixo; (3) os 8 controles novos (YAML no fim de `Telas/scr_SelecaoGestao_1.txt`, a partir de `btn_CardMontGest`); (4) `lbl_VersaoGest.Text`.

## Controles existentes que mudam X/Y/Width/Height (necessidade: abrir espaço para o card novo; o card da Conferência passa de 1160 para 560 de largura)
| Controle | Propriedade | Antes | Depois |
|---|---|---|---|
| btn_CardConfGest | Width | 1160 | 560 |
| btn_FaixaConfGest | Width | 1160 | 560 |
| btn_NavConfGest | Width | 1160 | 560 |
| lbl_TituloConfGest | Width | 1000 | 400 |
| lbl_DescConfGest | Width / Height | 1000 / 48 | 400 / 64 |
| lbl_AcaoConfGest | Width | 1000 | 400 |

`lbl_VersaoGest` · Text: `"Versão 0.3.0"`

Cada propriedade nova dos 8 controles (btn_CardMontGest, btn_FaixaMontGest, btn_IconeMontGest, ico_MontGest, lbl_TituloMontGest, lbl_DescMontGest, lbl_AcaoMontGest, btn_NavMontGest) está no .txt; o único que navega é `btn_NavMontGest.OnSelect`: `Navigate(scr_PainelMontagem_1, ScreenTransition.Fade)`.
