# Patch · scr_SelecaoGestao_1 → v0.4.0 · card do Painel da Montagem e Conferência SAP restrita (27/10/2026)

Base: o que está no Studio hoje é a v0.2.0 (sem o selo de abertas; a v0.3.0 do repositório, de 22/10, ainda não foi colada). Este patch leva a tela de v0.2.0 direto para v0.4.0.
Ordem de colar: (1) Formulas v3.0.14 (§19: `fx_EmailsConferencia`, `fx_PodeConferencia`) e o `scr_PainelMontagem_1`; (2) propriedades abaixo; (3) controles novos (YAML).
⚠ Em `Formulas.txt` §19 o e-mail do Vitor está como `vitor.PREENCHER@danfoss.com`: troque pelo e-mail real (minúsculas) antes de colar.

## 1. Propriedade da tela · OnVisible
```
Set(
    varConfAbertasGest,
    If(
        fx_PodeConferencia,
        IfError(CountRows(Filter(Conferencia_SAP, Status = "Aberto")), Blank()),
        Blank()
    )
)
```

## 2. Visible dos 8 controles da Conferência (só William e Vitor veem; os outros ficam só com Painel da Célula, Consulta de OP e Painel da Montagem)
`btn_CardConfGest`, `btn_FaixaConfGest`, `btn_IconeConfGest`, `ico_ConfGest`, `lbl_TituloConfGest`, `lbl_DescConfGest`, `lbl_AcaoConfGest`, `btn_NavConfGest` · Visible:
```
fx_PodeConferencia
```

## 3. Controles existentes que mudam X/Y/Width/Height (para abrir espaço ao card novo)
| Controle | Propriedade | Antes | Depois |
|---|---|---|---|
| btn_CardConfGest | Width | 1160 | 560 |
| btn_FaixaConfGest | Width | 1160 | 560 |
| btn_NavConfGest | Width | 1160 | 560 |
| lbl_TituloConfGest | Width | 1000 | 400 |
| lbl_DescConfGest | Width / Height | 1000 / 48 | 400 / 64 |
| lbl_AcaoConfGest | Width | 1000 | 400 |

## 4. Selo de abertas (controle NOVO em relação ao Studio; já nasce na posição nova, dentro do card da Conferência, X 503)
```yaml
      - lbl_BadgeConfGest:
          Control: Label@2.5.1
          Properties:
            Align: =Align.Center
            Color: =If(varConfAbertasGest > 0, fx_CorErro, fx_CorOK)
            Fill: =If(varConfAbertasGest > 0, fx_CorErroSuave, fx_CorOKSuave)
            Font: =fx_FonteFamilia
            FontWeight: =FontWeight.Bold
            Height: =32
            Size: =fx_FonteCorpo
            Text: =If(IsBlank(varConfAbertasGest), "—", If(varConfAbertasGest = 0, "Em dia", Text(varConfAbertasGest) & If(varConfAbertasGest = 1, " aberta", " abertas")))
            Visible: =fx_PodeConferencia && !IsBlank(varConfAbertasGest)
            Width: =140
            X: =503
            Y: =556
```

## 5. Card do Painel da Montagem (8 controles novos)
`btn_CardMontGest`, `btn_FaixaMontGest`, `btn_IconeMontGest`, `ico_MontGest`, `lbl_TituloMontGest`, `lbl_DescMontGest`, `lbl_AcaoMontGest`, `btn_NavMontGest`: YAML completo no fim de `Telas/scr_SelecaoGestao_1.txt` (a partir de `btn_CardMontGest`). `btn_NavMontGest.OnSelect`: `Navigate(scr_PainelMontagem_1, ScreenTransition.Fade)`.

## 6. `lbl_VersaoGest` · Text
```
"Versão 0.4.0"
```
