# scr_Finalização_1 — botões "Packing manual" e "Dividir pallet" no padrão da tela (08/10/2026)

Base: YAML vivo colado pelo William em 08/10 (Pack manual X1164/Y688/H36/W181; Dividir pallet X987/Y706/W121, sem Height).
Padrão copiado de: Editar Plano / Imprimir Ficha (lateral: H62, fx_Raio, texto com espaço invisível + ícone) e Finalizar Ordem (rodapé: fx_AlturaAcao, fx_RaioS).

## 1. btn_PackingManualExt (lateral, abaixo do card "Aprovado nesta OP"). Só mudar estas propriedades:
| Propriedade | Valor |
|---|---|
| Height | `=44` |
| Width | `=183` |
| X | `=1168` |
| Y | `=690` |
| Color | `=fx_CorTexto` |
| Size | `=fx_FonteCorpo` |
| RadiusTopLeft / TopRight / BottomLeft / BottomRight | `=fx_Raio` (as 4) |
| Text | `="ㅤㅤPacking manual"` (copie o "ㅤㅤ" do texto do botão Editar Plano: é o espaço invisível que abre lugar pro ícone) |

## 2. btn_DividirPalletExt (rodapé, à direita de "Finalizar Ordem"). Só mudar:
| Propriedade | Valor |
|---|---|
| Height | `=fx_AlturaAcao` |
| Width | `=165` |
| X | `=961` |
| Y | `=700` |
| FontWeight | `=FontWeight.Semibold` |
| Size | `=fx_FonteCorpo` |
| BorderColor | `=If(Self.DisplayMode = DisplayMode.Edit, fx_CorInfo, fx_CorBorda)` |
| Color | `=If(Self.DisplayMode = DisplayMode.Edit, fx_CorInfo, fx_CorRotulo)` |
| Text | `="ㅤㅤDividir pallet"` |

(raios continuam fx_RaioS, que já é o que está)

## 3. Dois ícones novos (inserir > Ícones, tipo Modern icon; colocar por cima dos botões)
**ico_PackingManualExt**
```
Icon: ="Add"          IconColor: =fx_CorInfo        Width: =24   Height: =24   X: =1186   Y: =700
DisplayMode: =btn_PackingManualExt.DisplayMode      OnSelect: =Select(btn_PackingManualExt)
```
**ico_DividirPalletExt**
```
Icon: ="Cut"          Width: =24   Height: =24   X: =977   Y: =716
IconColor: =If(btn_DividirPalletExt.DisplayMode = DisplayMode.Edit, fx_CorInfo, fx_CorRotulo)
DisplayMode: =btn_DividirPalletExt.DisplayMode      OnSelect: =Select(btn_DividirPalletExt)
```
Se algum nome de ícone não aparecer, escolha outro pelo painel de propriedades (ex.: "Copy" no lugar de "Cut").

## 4. Rótulo de versão (opcional): `lbl_VersaoExt.Text` → `="Versão 0.4.3"`
