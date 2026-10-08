# Patch ConsultaOP v0.4.0 + TelaImpressao: reimprimir packlist registrado (08/10/2026)

Botão "Packlists da OP" na Consulta de OP. Abre a lista de pallets **já registrados** em `Packing_Pallets` daquela OP e reimprime o escolhido pela `TelaImpressao`, igual ao original (mesma data, mesmo pallet, mesmos lances).
Não reconstrói nada pelo registro de inspeção: os metros vêm só dos IDs de lance gravados no pallet. Sem pallet registrado, o botão fica desabilitado ("Packlist não registrado"). Reimprimir não grava nada.

Base: `Telas/scr_ConsultaOP_1.txt` v0.3.1 (a do repositório, com os chips de recentes). Fonte de dados `Packing_Pallets` já está no app.

## ATENÇÃO (09/10): a busca da v0.3.1 foi trocada
A v0.3.1 buscava a OP dentro do `Items` da galeria e devolvia "0 OPs" para a 30424231 (a 0.3.0 achava). A lista voltou ao padrão que funcionava: o `OnChange` do campo, os chips de recentes, o X e o recarregar carregam `colConsultaOP`, e a galeria só lê essa coleção. **Por isso o caminho mais seguro é colar o arquivo inteiro `Telas/scr_ConsultaOP_1.txt`** (os blocos A1–A5 abaixo ficam como referência do botão de packlist).

## Ordem de colagem (importa)
1. **scr_ConsultaOP_1** (ela define `varReimpressaoImp` e `varDataImp`).
2. **TelaImpressao**.

## A. scr_ConsultaOP_1: 4 passos
**A1. OnVisible da tela** (troque só a primeira linha):
```
=UpdateContext({ctxAbaCOP: 1, ctxBuscaCOP: "", ctxModalPackCOP: false});
```
**A2. Rótulo de versão** `lbl_VersaoCOP.Text`: `="Versão 0.4.0"`

**A3. Botão dentro do container `ctn_AbasCOP`** (cole como filho, depois de `btn_AbaErrosCOP`/`rct_LinhaAbaErrosCOP`; nenhum controle existente muda de X/Y/tamanho):
```yaml
            - btn_PackListCOP:
                Control: Classic/Button@2.2.0
                Properties:
                  BorderColor: =Color.Transparent
                  BorderThickness: =0
                  Color: =fx_CorSuperficie
                  DisabledFill: =fx_CorBorda
                  DisplayMode: |-
                    =If(
                        IsBlank(LookUp(Packing_Pallets, FichaID = gal_FilaCOP.Selected.ID).ID),
                        DisplayMode.Disabled,
                        DisplayMode.Edit
                    )
                  Fill: =fx_CorInfo
                  Font: =fx_FonteFamilia
                  FontWeight: =FontWeight.Bold
                  Height: =36
                  HoverFill: =ColorFade(fx_CorInfo, -20%)
                  OnSelect: |-
                    =UpdateContext({ctxModalPackCOP: true})
                  PressedFill: =ColorFade(fx_CorInfo, -30%)
                  RadiusBottomLeft: =fx_RaioS
                  RadiusBottomRight: =fx_RaioS
                  RadiusTopLeft: =fx_RaioS
                  RadiusTopRight: =fx_RaioS
                  Size: =fx_FonteApoio
                  Text: =If(IsBlank(LookUp(Packing_Pallets, FichaID = gal_FilaCOP.Selected.ID).ID), "Packlist não registrado", "Packlists da OP")
                  Width: =190
                  X: =840
                  Y: =4
```
**A4. Modal no nível da tela** (cole no fim da lista de controles da tela, depois de `ctn_ErrosCOP`):
```yaml
      - rct_OverlayPackCOP:
          Control: Rectangle@2.3.0
          Properties:
            Fill: =fx_CorOverlay
            Height: =768
            OnSelect: |-
              =UpdateContext({ctxModalPackCOP: false})
            Visible: =ctxModalPackCOP
            Width: =1366
      - rct_CardPackCOP:
          Control: Rectangle@2.3.0
          Properties:
            BorderColor: =fx_CorBorda
            BorderThickness: =1
            Fill: =fx_CorSuperficie
            Height: =520
            Visible: =ctxModalPackCOP
            Width: =760
            X: =303
            Y: =124
      - lbl_TituloPackCOP:
          Control: Label@2.5.1
          Properties:
            Color: =fx_CorTexto
            Font: =fx_FonteFamilia
            FontWeight: =FontWeight.Bold
            Height: =34
            Size: =fx_FonteTitulo
            Text: ="Packlists da OP " & Text(gal_FilaCOP.Selected.OP, "[$-en-US]0")
            Visible: =ctxModalPackCOP
            Width: =600
            X: =327
            Y: =140
      - lbl_SubPackCOP:
          Control: Label@2.5.1
          Properties:
            Color: =fx_CorTextoSuave
            Font: =fx_FonteFamilia
            Height: =22
            Size: =fx_FonteApoio
            Text: ="Só aparecem pallets já registrados. A reimpressão sai igual à original e não grava nada."
            Visible: =ctxModalPackCOP
            Width: =712
            X: =327
            Y: =176
      - gal_PalletsPackCOP:
          Control: Gallery@2.15.0
          Variant: Vertical
          Properties:
            Fill: =Color.Transparent
            Height: =370
            Items: =Sort(Filter(Packing_Pallets, FichaID = gal_FilaCOP.Selected.ID), Pallet)
            TemplateSize: =76
            Visible: =ctxModalPackCOP
            Width: =712
            X: =327
            Y: =210
          Children:
            - rct_ItemPackCOP:
                Control: Rectangle@2.3.0
                Properties:
                  BorderColor: =fx_CorBorda
                  BorderThickness: =1
                  Fill: =fx_CorSuperficie
                  Height: =68
                  Width: =712
                  Y: =4
            - lbl_PalletPackCOP:
                Control: Label@2.5.1
                Properties:
                  Color: =fx_CorInfo
                  Font: =fx_FonteFamilia
                  FontWeight: =FontWeight.Bold
                  Height: =26
                  Size: =fx_FonteDestaque
                  Text: ="Pallet " & Text(ThisItem.Pallet, "[$-en-US]0")
                  Width: =160
                  X: =16
                  Y: =12
            - lbl_DetPackCOP:
                Control: Label@2.5.1
                Properties:
                  Color: =fx_CorTextoSuave
                  Font: =fx_FonteFamilia
                  Height: =22
                  Size: =fx_FonteApoio
                  Text: |-
                    =Text(ThisItem.QtdLances, "[$-en-US]0") & " lances   ·   " &
                    fx_QtdBR(ThisItem.TotalM) & " m   ·   impresso em " &
                    fx_DataHoraBR(Text(ThisItem.DataHoraImp))
                  Width: =470
                  X: =16
                  Y: =40
            - btn_ReimprimirPackCOP:
                Control: Classic/Button@2.2.0
                Properties:
                  BorderColor: =Color.Transparent
                  BorderThickness: =0
                  Color: =fx_CorSuperficie
                  Fill: =fx_CorInfo
                  Font: =fx_FonteFamilia
                  FontWeight: =FontWeight.Bold
                  Height: =fx_AlturaAcaoS
                  HoverFill: =ColorFade(fx_CorInfo, -20%)
                  OnSelect: |-
                    =IfError(
                        ClearCollect(colInspPackCOP, Filter(RegistrosInspeção, OP_ID = gal_FilaCOP.Selected.OP));
                        ClearCollect(
                            colPalletImp,
                            ForAll(
                                MatchAll(ThisItem.LanceIDs, "\d+") As _l,
                                { ID: Value(_l.FullMatch), Qtd: LookUp(colInspPackCOP, ID = Value(_l.FullMatch)).Quantidade }
                            )
                        );
                        If(
                            CountRows(Filter(colPalletImp, IsBlank(Qtd))) > 0,
                            Notify("Não achei " & CountRows(Filter(colPalletImp, IsBlank(Qtd))) & " lance(s) deste pallet. Avise a supervisão.", NotificationType.Error, 8000),
                            Set(varFichaIDImp, gal_FilaCOP.Selected.ID);
                            Set(varFalhaRegManual, false);
                            Set(varPackingManual, false);
                            Set(varReimpressaoImp, true);
                            Set(varDataImp, Text(ThisItem.DataHoraImp, "yyyy-mm-dd hh:mm"));
                            Set(VarMangueiraOP, gal_FilaCOP.Selected.OP);
                            Set(varMangueiraImp, gal_FilaCOP.Selected.Mangueira);
                            Set(varPalletTxt, "  ·  PALLET " & Text(ThisItem.Pallet, "[$-en-US]0"));
                            Set(varTotalImp, fx_QtdBR(Coalesce(Sum(colPalletImp, Qtd), 0)));
                            Set(
                                varHTMLLances,
                                "<table style='border-collapse:collapse;width:100%'>"
                                & "<tr style='background:#d0d0d0'><th style='border:1px solid #000;padding:10px 12px;font-size:20px;width:8%'>N°</th><th style='border:1px solid #000;padding:10px 12px;font-size:20px;width:27%'>QTY (m)</th><th style='border:1px solid #000;padding:10px 12px;font-size:20px;width:8%'>N°</th><th style='border:1px solid #000;padding:10px 12px;font-size:20px'>QTY (m)</th></tr>"
                                & Concat(
                                    ForAll(
                                        Sequence(13) As _i,
                                        {
                                            linha:
                                                "<tr><td style='border:1px solid #000;padding:10px 12px;font-size:20px'>"
                                                & Text(_i.Value, "[$-en-US]0")
                                                & "</td><td style='border:1px solid #000;padding:10px 12px;font-size:20px'>"
                                                & If(
                                                    CountRows(colPalletImp) >= _i.Value,
                                                    fx_QtdBR(Index(colPalletImp, _i.Value).Qtd),
                                                    "0,00"
                                                )
                                                & "</td><td style='border:1px solid #000;padding:10px 12px;font-size:20px'>"
                                                & Text(_i.Value + 13, "[$-en-US]0")
                                                & "</td><td style='border:1px solid #000;padding:10px 12px;font-size:20px'>"
                                                & If(
                                                    CountRows(colPalletImp) >= _i.Value + 13,
                                                    fx_QtdBR(Index(colPalletImp, _i.Value + 13).Qtd),
                                                    "0,00"
                                                )
                                                & "</td></tr>"
                                        }
                                    ),
                                    linha
                                )
                                & "</table>"
                            );
                            UpdateContext({ctxModalPackCOP: false});
                            Navigate(TelaImpressao, ScreenTransition.None)
                        ),
                        Notify("Não consegui montar o packlist. Confira a rede e tente de novo.", NotificationType.Error, 8000)
                    )
                  PressedFill: =ColorFade(fx_CorInfo, -30%)
                  RadiusBottomLeft: =fx_RaioS
                  RadiusBottomRight: =fx_RaioS
                  RadiusTopLeft: =fx_RaioS
                  RadiusTopRight: =fx_RaioS
                  Size: =fx_FonteCorpo
                  Text: ="Reimprimir"
                  Width: =200
                  X: =496
                  Y: =10
      - btn_FecharPackCOP:
          Control: Classic/Button@2.2.0
          Properties:
            BorderColor: =fx_CorBorda
            BorderThickness: =1
            Color: =fx_CorTexto
            Fill: =fx_CorSuperficie
            Font: =fx_FonteFamilia
            FontWeight: =FontWeight.Semibold
            Height: =fx_AlturaAcaoS
            HoverFill: =fx_CorFundo
            OnSelect: |-
              =UpdateContext({ctxModalPackCOP: false})
            PressedFill: =fx_CorInfoSuave
            RadiusBottomLeft: =fx_RaioS
            RadiusBottomRight: =fx_RaioS
            RadiusTopLeft: =fx_RaioS
            RadiusTopRight: =fx_RaioS
            Size: =fx_FonteCorpo
            Text: ="Fechar"
            Visible: =ctxModalPackCOP
            Width: =160
            X: =879
            Y: =592
```

## B. TelaImpressao: 2 propriedades
**B1. `btn_voltar_impressao_1.OnSelect`** (antes: `=Navigate(scr_Finalização_1, ScreenTransition.None)`):
```
=If(
    varReimpressaoImp,
    Set(varReimpressaoImp, false);
    Navigate(scr_ConsultaOP_1, ScreenTransition.None),
    Navigate(scr_Finalização_1, ScreenTransition.None)
)
```
**B2. `lbl_date_val_1.Text`** (antes: `=Text(Now(), "yyyy-mm-dd hh:mm")`):
```
=If(varReimpressaoImp, varDataImp, Text(Now(), "yyyy-mm-dd hh:mm"))
```

## A5. Correção dos chips de recentes (só se você colar o arquivo inteiro da v0.3.1)
`btn_Recente1COP` a `btn_Recente4COP`, propriedade `Text` (troque o número 1 pelo de cada chip):
```
=If(CountRows(colRecentesCOP) >= 1, Text(Index(Sort(colRecentesCOP, Quando, SortOrder.Descending), 1).OP, "0"), "")
```
Sem isso o Studio acusa "Index cannot be called with an empty table" enquanto não há OP recente.

## Teste
1. Consulta de OP > OP **30424231** > "Packlists da OP" > deve listar Pallet 1 (26 lances, 649 m) e Pallet 2 (5 lances, 27 m).
2. Reimprimir o Pallet 1: a TelaImpressao mostra DATE 2026-10-07 18:09, ID PALLET com "PALLET 1", total 649,00 e a tabela com os 26 lances. ← Voltar volta para a Consulta de OP.
3. Entrar de novo pela Finalização: o DATE volta a ser a data/hora de agora (a flag `varReimpressaoImp` zerou no Voltar).
4. OP sem pallet registrado: botão cinza "Packlist não registrado".

Obs.: `FichaID` ainda não está indexado em `Packing_Pallets`; funciona, mas fica lento com a lista grande.
