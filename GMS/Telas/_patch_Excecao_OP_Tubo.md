# Exceção de OP no tubo: como aplicar (14/10/2026)

O arquivo `Telas/scr_tubo_1.txt` já está com tudo. Se preferir não colar a tela inteira, são 6 pontos pequenos abaixo.

## 0. Antes
No Studio, **Dados > Adicionar dados > `Excecoes_OP`** (site Operations Guaratingueta). Sem isso dá "Name isn't valid". Se mexer em colunas da lista, use **Atualizar** nos dados.

## 1. `cmb_OpTubo_1` > `Items` (substituir a fórmula inteira)
```
Ungroup(
    Table(
        {
            t: Filter(
                colPlanoTubo,
                (!(OPnum in colOPsUsadasTubo.OP) || OPnum = gal_FilaTubo_1.Selected.OP) &&
                (
                    IsBlank(cmb_MangueiraTubo_1.Selected.NomeMangueira) ||
                    cmb_MangueiraTubo_1.Selected.NomeMangueira = fx_MangueiraOutra ||
                    IsBlank(PN) ||
                    PN = cmb_MangueiraTubo_1.Selected.NomeMangueira
                ) &&
                (
                    IsBlank(drp_TrancadeiraTubo_1.Selected.Value) ||
                    IsBlank(Trancadeira) ||
                    TrDrp = drp_TrancadeiraTubo_1.Selected.Value
                )
            )
        },
        {t: Table({OPnum: -1, OPtxt: "Outra OP (pedir exceção)"})}
    ),
    t
)
```

## 2. `cmb_OpTubo_1` > `OnChange` (substituir a fórmula inteira)
```
If(
    Self.Selected.OPnum = -1,
    Reset(inp_ExcOpTubo);
    Reset(inp_ExcMotivoTubo);
    UpdateContext({ctxModalExcecaoTubo: true});
    Reset(cmb_OpTubo_1),
    IsBlank(Self.Selected.OPnum),
    Set(varTrPlanoTubo, Blank());
    Set(varQtdPlanoTubo, Blank()),
    Set(varMangueiraEscolhidaTubo, Coalesce(Self.Selected.PN, varMangueiraEscolhidaTubo));
    Set(varTrPlanoTubo, If(IsBlank(Self.Selected.Trancadeira), Blank(), Self.Selected.TrDrp));
    Set(varQtdPlanoTubo, If(Self.Selected.QtdPlanejada > 0, Self.Selected.QtdPlanejada, Blank()));
    Reset(cmb_MangueiraTubo_1);
    Reset(drp_TrancadeiraTubo_1);
    Reset(inp_QtdTubo_1)
)
```

## 3. `ico_RefreshTubo_1` > `OnSelect` (substituir a fórmula inteira)
```
IfError(
    Concurrent(
        Refresh(ficha_producao),
        Refresh(lista_carreteis),
        Refresh('Hora-Hora'),
        Refresh(Plano_OPs),
        Refresh(Excecoes_OP)
    ),
    Notify("Não consegui atualizar do servidor. Confira a conexão e toque em atualizar.", NotificationType.Error, 8000)
);
Concurrent(
    ClearCollect(colCarreteisTubo, lista_carreteis),
    ClearCollect(
        colFilaTrancTubo,
        AddColumns(
            Filter(ficha_producao, processo = "Trançadeira"),
            TrN, If(Trançadeira = "TE-01" || Trançadeira = "TE.01", "Spiral", Trançadeira)
        )
    ),
    ClearCollect(
        colHHDiaTubo,
        Filter('Hora-Hora', Data = fx_DataRefEm(Now()))
    )
);
IfError(
    ClearCollect(
        colPlanoTubo,
        AddColumns(
            Filter(Plano_OPs, Tipo = "Tubo", Encerrada = false),
            OPnum, Value(Title),
            OPtxt, Title,
            TrDrp, If(Trancadeira = "TE.01", "Spiral", Substitute(Trancadeira, ".", ""))
        )
    );
    true,
    Notify("Não consegui ler o plano de OPs. Toque em atualizar.", NotificationType.Error, 8000);
    false
);
IfError(
    ForAll(
        Filter(Excecoes_OP, Status = "Aprovada", Tela = "Tubo") As _e,
        If(
            IsBlank(LookUp(colPlanoTubo, OPtxt = _e.Title)),
            Collect(
                colPlanoTubo,
                {
                    Title: _e.Title,
                    OPnum: Value(_e.Title),
                    OPtxt: _e.Title,
                    PN: _e.PN,
                    Tipo: "Tubo",
                    Encerrada: false,
                    Origem: "Exceção"
                }
            )
        )
    );
    true,
    Notify("Não consegui ler as exceções de OP. Toque em atualizar.", NotificationType.Warning, 6000);
    false
);
With(
    { _min: Coalesce(Min(colPlanoTubo, OPnum), 0) },
    ClearCollect(
        colOPsUsadasTubo,
        ShowColumns(Filter(ficha_producao, OP >= _min, processo <> "Tubo", status_processo <> "Cancelado", status_processo <> "Cancelada"), OP)
    )
);
ClearCollect(
    colKanbanTrancTubo,
    ForAll(
        fx_CelulasTrancagem As _c,
        With(
            {
                _rodando: CountRows(
                    Filter(
                        colFilaTrancTubo As _f,
                        _f.TrN = _c.Celula &&
                        _f.status_processo = "Em processo"
                    )
                ) > 0,
                _qtd: CountRows(
                    Filter(
                        colFilaTrancTubo As _g,
                        _g.TrN = _c.Celula &&
                        _g.status_processo = "Aguardando" &&
                        !IsBlank(_g.'Carretel Entrada')
                    )
                ),
                _hh: CountRows(
                    Filter(
                        colHHDiaTubo As _h,
                        _h.Célula = _c.Celula &&
                        (Coalesce(_h.'Real. Hora', 0) > 0 || !IsBlank(_h.Mangueira))
                    )
                ) > 0
            },
            {
                Celula:  _c.Celula,
                Tipo:    "MAQ",
                Rodando: _rodando,
                Qtd:     _qtd,
                Ativa:   _rodando || _hh
            }
        )
    )
);
With(
    {
        _orf: CountRows(
            Filter(
                colFilaTrancTubo As _o,
                _o.status_processo = "Aguardando" &&
                !IsBlank(_o.'Carretel Entrada') &&
                IsBlank(
                    LookUp(fx_CelulasTrancagem As _c2, _c2.Celula = _o.TrN).Celula
                )
            )
        )
    },
    If(
        _orf > 0,
        Collect(
            colKanbanTrancTubo,
            { Celula: "fora da grade", Tipo: "ORF", Rodando: false, Qtd: _orf, Ativa: true }
        )
    )
);
UpdateContext({ctxAgora: Now()})
```

## 4. Timer do tubo > `OnTimerEnd`
Trocar `!ctxModalDelinTubo && !ctxModalOutraMangTubo,` por `!ctxModalDelinTubo && !ctxModalOutraMangTubo && !ctxModalExcecaoTubo,`.

## 5. `scr_tubo_1` > `OnVisible`
No `UpdateContext({ ... })`, depois de `ctxModalOutraMangTubo: false` coloque uma vírgula e `ctxModalExcecaoTubo: false`.

## 6. `btn_ConfirmarEnviarTubo_1` > `OnSelect`
Trocar a condição `IsBlank(LookUp(Plano_OPs, Title = Text(_op, "00000000") && Encerrada = false).ID),` por:
```
IsBlank(LookUp(Plano_OPs, Title = Text(_op, "00000000") && Encerrada = false).ID) &&
IsBlank(LookUp(Excecoes_OP, Title = Text(_op, "00000000") && Tela = "Tubo" && Status = "Aprovada").ID),
```
E o texto do Notify seguinte por: `"Esta OP saiu do plano ou já foi encerrada. Toque em atualizar e escolha de novo. Se for OP fora do plano, peça a exceção."`

## 7. Modal novo (controles novos): colar este YAML na tela `scr_tubo_1`
Fica antes do `rct_OverlayTubo_1`. Cola-se com o botão direito na tela > Colar código YAML.
```yaml
      - cntr_ExcecaoTubo:
          Control: GroupContainer@1.5.0
          Variant: ManualLayout
          Properties:
            Fill: =fx_CorOverlay
            Height: =768
            Visible: =ctxModalExcecaoTubo
            Width: =1366
          Children:
            - btn_BgExcecaoTubo:
                Control: Classic/Button@2.2.0
                Properties:
                  BorderColor: =Color.Transparent
                  BorderThickness: =0
                  Fill: =Color.Transparent
                  Font: =fx_FonteFamilia
                  Height: =768
                  HoverFill: =Color.Transparent
                  PressedFill: =Color.Transparent
                  Text: =""
                  Width: =1366
            - btn_CardExcecaoTubo:
                Control: Classic/Button@2.2.0
                Properties:
                  BorderColor: =fx_CorBorda
                  BorderThickness: =1
                  DisplayMode: =DisplayMode.View
                  Fill: =fx_CorSuperficie
                  Font: =fx_FonteFamilia
                  Height: =440
                  HoverFill: =fx_CorSuperficie
                  PressedFill: =fx_CorSuperficie
                  RadiusBottomLeft: =fx_RaioG
                  RadiusBottomRight: =fx_RaioG
                  RadiusTopLeft: =fx_RaioG
                  RadiusTopRight: =fx_RaioG
                  Text: =""
                  Width: =560
                  X: =403
                  Y: =170
            - lbl_TituloExcecaoTubo:
                Control: Label@2.5.1
                Properties:
                  Color: =fx_CorTexto
                  Font: =fx_FonteFamilia
                  FontWeight: =FontWeight.Bold
                  Height: =34
                  Size: =fx_FonteTitulo
                  Text: ="OP fora do plano"
                  Width: =500
                  X: =433
                  Y: =194
            - lbl_SubExcecaoTubo:
                Control: Label@2.5.1
                Properties:
                  Color: =fx_CorTextoSuave
                  Font: =fx_FonteFamilia
                  Height: =60
                  Size: =fx_FonteCorpo
                  Text: ="Confira o número na ordem. William ou Carlos aprovam pelo celular. Depois de aprovada, toque em atualizar e escolha a OP na lista."
                  Width: =500
                  X: =433
                  Y: =234
            - lbl_RotExcOpTubo:
                Control: Label@2.5.1
                Properties:
                  Color: =fx_CorRotulo
                  Font: =fx_FonteFamilia
                  FontWeight: =FontWeight.Semibold
                  Height: =20
                  Size: =fx_FonteApoio
                  Text: ="NÚMERO DA OP (8 DÍGITOS) *"
                  Width: =500
                  X: =433
                  Y: =304
            - inp_ExcOpTubo:
                Control: Classic/TextInput@2.3.2
                Properties:
                  AccessibleLabel: ="Número da OP fora do plano"
                  BorderColor: =If(IsMatch(Trim(Self.Text), "^\d{8}$"), fx_CorBorda, fx_CorErro)
                  Default: =""
                  DelayOutput: =true
                  Font: =fx_FonteFamilia
                  Height: =fx_AlturaCampo
                  HintText: ="Exemplo 30529216"
                  HoverFill: =fx_CorInfoSuave
                  MaxLength: =8
                  PaddingLeft: =10
                  RadiusBottomLeft: =fx_RaioS
                  RadiusBottomRight: =fx_RaioS
                  RadiusTopLeft: =fx_RaioS
                  RadiusTopRight: =fx_RaioS
                  Size: =fx_FonteCorpo
                  Width: =500
                  X: =433
                  Y: =326
            - lbl_RotExcMotivoTubo:
                Control: Label@2.5.1
                Properties:
                  Color: =fx_CorRotulo
                  Font: =fx_FonteFamilia
                  FontWeight: =FontWeight.Semibold
                  Height: =20
                  Size: =fx_FonteApoio
                  Text: ="MOTIVO *"
                  Width: =500
                  X: =433
                  Y: =392
            - inp_ExcMotivoTubo:
                Control: Classic/TextInput@2.3.2
                Properties:
                  AccessibleLabel: ="Motivo do pedido de exceção"
                  BorderColor: =If(IsBlank(Trim(Self.Text)), fx_CorErro, fx_CorBorda)
                  Default: =""
                  DelayOutput: =true
                  Font: =fx_FonteFamilia
                  Height: =fx_AlturaCampo
                  HintText: ="Exemplo OP liberada hoje, ainda fora do plano"
                  HoverFill: =fx_CorInfoSuave
                  PaddingLeft: =10
                  RadiusBottomLeft: =fx_RaioS
                  RadiusBottomRight: =fx_RaioS
                  RadiusTopLeft: =fx_RaioS
                  RadiusTopRight: =fx_RaioS
                  Size: =fx_FonteCorpo
                  Width: =500
                  X: =433
                  Y: =414
            - btn_CancelarExcecaoTubo:
                Control: Classic/Button@2.2.0
                Properties:
                  BorderColor: =fx_CorBorda
                  BorderThickness: =1
                  Color: =fx_CorTextoSuave
                  Fill: =fx_CorSuperficie
                  Font: =fx_FonteFamilia
                  Height: =fx_AlturaAcaoS
                  HoverFill: =fx_CorFundo
                  OnSelect: |-
                    =Reset(inp_ExcOpTubo);
                    Reset(inp_ExcMotivoTubo);
                    UpdateContext({ctxModalExcecaoTubo: false})
                  PressedFill: =fx_CorFundo
                  RadiusBottomLeft: =fx_RaioS
                  RadiusBottomRight: =fx_RaioS
                  RadiusTopLeft: =fx_RaioS
                  RadiusTopRight: =fx_RaioS
                  Size: =fx_FonteCorpo
                  Text: ="Cancelar"
                  Width: =180
                  X: =433
                  Y: =510
            - btn_PedirExcecaoTubo:
                Control: Classic/Button@2.2.0
                Properties:
                  BorderColor: =Color.Transparent
                  BorderThickness: =0
                  Color: =fx_CorSuperficie
                  DisabledFill: =fx_CorBorda
                  DisplayMode: =If(!varProcessando && IsMatch(Trim(inp_ExcOpTubo.Text), "^\d{8}$") && !IsBlank(Trim(inp_ExcMotivoTubo.Text)), DisplayMode.Edit, DisplayMode.Disabled)
                  Fill: =fx_CorInfo
                  Font: =fx_FonteFamilia
                  FontWeight: =FontWeight.Bold
                  Height: =fx_AlturaAcaoS
                  HoverFill: =ColorFade(fx_CorInfo, -20%)
                  OnSelect: |-
                    =Set(varProcessando, true);
                    With(
                        { _op: Trim(inp_ExcOpTubo.Text) },
                        If(
                            !IsBlank(LookUp(Plano_OPs, Title = _op && Encerrada = false).ID),
                            Notify("Esta OP já está no plano. Toque em atualizar e escolha na lista.", NotificationType.Warning, 8000),
                            !IsBlank(LookUp(Excecoes_OP, Title = _op && Tela = "Tubo" && (Status = "Pendente" || Status = "Aprovada")).ID),
                            Notify("Já existe um pedido para esta OP. Aguarde a aprovação e toque em atualizar.", NotificationType.Warning, 8000),
                            IfError(
                                Patch(
                                    Excecoes_OP,
                                    Defaults(Excecoes_OP),
                                    {
                                        Title: _op,
                                        Tela: "Tubo",
                                        PN: Coalesce(varMangueiraEscolhidaTubo, ""),
                                        Motivo: Trim(inp_ExcMotivoTubo.Text),
                                        PedidoPor: Coalesce(cmb_OperadorTubo_1.Selected.Nome, User().FullName),
                                        Status: "Pendente",
                                        DataPedido: Now()
                                    }
                                );
                                Notify("Pedido enviado. William ou Carlos vão aprovar. Depois, toque em atualizar.", NotificationType.Success, 8000);
                                UpdateContext({ctxModalExcecaoTubo: false}),
                                Notify("Não consegui enviar o pedido. Confira a conexão e tente de novo.", NotificationType.Error, 8000)
                            )
                        )
                    );
                    Set(varProcessando, false)
                  PressedFill: =ColorFade(fx_CorInfo, -30%)
                  RadiusBottomLeft: =fx_RaioS
                  RadiusBottomRight: =fx_RaioS
                  RadiusTopLeft: =fx_RaioS
                  RadiusTopRight: =fx_RaioS
                  Size: =fx_FonteCorpo
                  Text: ="Pedir exceção"
                  Width: =220
                  X: =713
                  Y: =510
```

## Como funciona
- No dropdown da OP aparece, por último, **"Outra OP (pedir exceção)"**. Ao escolher, abre o modal (OP de 8 dígitos e motivo).
- O pedido vai para `Excecoes_OP` com `Status = Pendente`. O fluxo `GMS_ExcecaoOP_Aprovacao` manda a aprovação para William e Carlos.
- Aprovada, a OP entra no dropdown no próximo atualizar e o envio aceita. A exceção vale uma vez: depois que a OP entra numa ficha além do Tubo, ela some.
- OP do plano e OP aprovada convivem no mesmo dropdown (a aprovada entra em `colPlanoTubo` com `Origem = Exceção`).
