# Colar no Studio: kill switch Composto (MEL-274)

Gerado de `GMS/Telas/*.txt` (commit 40a0d342). Ordem: 1) tela scr_Composto, 2) OnStart, 3) BackEnabled, 4) as 23 telas, 5) App Checker, 6) Publicar.

> **Cuidado antes de substituir (OnStart e OnVisible):** o texto aqui vem dos arquivos locais. Se no Studio a fórmula original tiver algo que não está aqui (ex.: mangueira nova no OnStart), **não perca**: cole o bloco `IfError(...)` no começo e coloque a fórmula original do Studio como último argumento do `If(` (no OnStart, dentro de `If(varCompostoPermitida, ...)`; nas telas, depois de `Navigate(scr_Composto),`). Na dúvida, me mande a fórmula que está no Studio.
>
> **Menu_1 é a tela inicial:** o Studio não deixa `Navigate` no OnVisible dela ("Navigate cannot be used here..."). Por isso o OnVisible do Menu_1 não navega: quem desvia para `scr_Composto` é o timer `tmr_Composto_Menu_1_Gate` (100 ms, dispara quando `varCompostoPermitida` vira false). Se outra tela der o mesmo erro, me avise: o conserto é o mesmo.

## 1. Tela nova scr_Composto

Nova tela em branco, renomeie para `scr_Composto`, propriedade **Fill** = `fx_CorFundo`. Depois clique na tela, Ctrl+V com o bloco abaixo (rótulo da mensagem):

```yaml
- lbl_MensagemComposto:
    Control: Label@2.5.1
    Properties:
      Align: =Align.Center
      Color: =fx_CorTexto
      Font: =fx_FonteFamilia
      FontWeight: =FontWeight.Bold
      Height: =200
      Size: =fx_FonteTitulo
      Text: =Coalesce(varCompostoMensagem, "Acesso bloqueado.")
      VerticalAlign: =VerticalAlign.Middle
      Width: =900
      X: =233
      Y: =284
```

## 2. App → OnStart

Substitua a fórmula inteira do OnStart por:

```
IfError(
    With(
        {resComposto: Flow_Composto.Run()},
        Set(varCompostoPermitida, resComposto.permitido);
        Set(varCompostoMensagem, resComposto.mensagem)
    ),
    Set(varCompostoPermitida, false);
    Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
);

If(varCompostoPermitida,
    Set(varMapa, LookUp(MapeamentoSetor, EmailComputador = User().Email));
    Set(varAcessoRestrito, Coalesce(varMapa.AcessoRestrito, false));
    Set(varCelulaMontagem, varMapa.Celula);
    Concurrent(
        ClearCollect(
            colTrancadeiras,
            [
                "Spiral", "TH01", "TH02", "TH03", "TH04", "TH05", "TH06", "TH07",
                "TM04", "TO04", "TM01"
            ]
        ),
        ClearCollect(
            colMangueiras,
            ForAll(
                [
                    "2583-12", "2556-10", "2556-12", "2556-16", "2556-3", "2556-4", "2807-10", "2807-12",
                    "2556-5", "2556-6", "2556-8", "EC115-04L", "EC115-06L", "EC115-08L", "EC115-10L", "EC115-12L",
                    "EC115-16L", "EC118-04L", "EC118-06L", "EC118-08L", "EC118-10L", "EC600-16", "EC118-12L",
                    "EC118-16L", "EC215-06L", "EC215-08L", "EC215-04", "EC215-08LRL", "EC215-10L",
                    "EC215-12L", "EC215-16L", "EC415-12", "EC415-16", "FC598-08", "FC598-10",
                    "FC598-12", "FC735-04", "FC735-06", "FC735-08", "FC735-10", "FC735-12",
                    "FC839B-04", "FC839B-06", "FC839B-08", "FC849-08", "GH493-10", "GH493-12",
                    "GH493-16", "GH493-6", "GH493-8", "GH681-12", "GH681-16", "GH681-4",
                    "GH681-6", "GH681-8", "GH681-10", "GH781-10", "GH781-12", "GH781-16", "GH781-4",
                    "GH781-6", "GH781-6-2", "GH781-8", "H28004-250R", "H28006-250R", "H28008-250R",
                    "HC101-4", "HC101-6", "HC101-8", "HC139-7", "HC139-7_S-GX"
                ],
                { NomeMangueira: Value }
            )
        ),
        ClearCollect(
            Turno,
            ["1", "2", "3"]
        ),
        ClearCollect(colDM_MANDREL, DM_MANDREL),
        ClearCollect(colDM_BANDAGEM, DM_BANDAGEM),
        ClearCollect(colDM_LAYLINE, DM_LAYLINE)
    );
    ClearCollect(colMangEscTubo, colMangueiras, {NomeMangueira: fx_MangueiraOutra})
)
```

## 3. App → BackEnabled

```
App.ActiveScreen.Name <> "scr_Composto"
```

## 3b. App → OnError (esconde só as faixas vermelhas combinadas)

Ficam silenciosos (vão só para o Monitor): erro do `Flow_Composto` e o erro `[DM_TUBE_EXTRUSION] Expression "PARTNUMBER eq null"` (LookUp com o campo de mangueira vazio nos 11 campos da tela de extrusão do tubo: TXT_Matriz3, TextInput1_63..72). Qualquer outro erro do app continua aparecendo em vermelho.

```
If(
    "Flow_Composto" in FirstError.Message
        || ("DM_TUBE_EXTRUSION" in FirstError.Message && "PARTNUMBER eq null" in FirstError.Message),
    Trace(
        "Erro silenciado: " & FirstError.Source,
        TraceSeverity.Warning,
        {Mensagem: FirstError.Message, Origem: FirstError.Source}
    ),
    Notify(FirstError.Message, NotificationType.Error)
)
```

## 4. As 23 telas

Em cada tela: (a) selecione a tela, propriedade **OnVisible**, apague tudo e cole a fórmula; (b) clique na tela e Ctrl+V com o bloco do timer (ele fica invisível).

### 4.1 Menu_1

OnVisible:

```
If(
    IsBlank(varCompostoPermitida),
    IfError(
        With(
            {resComposto: Flow_Composto.Run()},
            Set(varCompostoPermitida, resComposto.permitido);
            Set(varCompostoMensagem, resComposto.mensagem)
        ),
        Set(varCompostoPermitida, false);
        Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
    )
);
If(
    varCompostoPermitida,
    UpdateContext({ctxHoje: Today()});
    Set(
        varAreaUsuario,
        IfError(
            Coalesce(
                LookUp(
                    MapeamentoSetor,
                    Lower(EmailComputador) = Lower(User().Email)
                ).Area,
                "Gestao"
            ),
            Notify("Não consegui confirmar seu setor. Só o Painel de Gestão foi liberado — confira a rede e reabra o menu.", NotificationType.Error, 10000);
            "Gestao"
        )
    );
    Set(varSomenteMontagem, varAreaUsuario = "Montagem");
    Set(varAmbasAreas, varAreaUsuario = "Ambos");
    Set(varSomenteGestao, varAreaUsuario = "Gestao")
)
```

Timers (Ctrl+V na tela, os dois juntos):

```yaml
- tmr_Composto_Menu_1_Gate:
    Control: Timer@2.1.0
    Properties:
      Duration: =100
      Fill: =fx_CorInfo
      Font: =fx_FonteFamilia
      OnTimerEnd: =Navigate(scr_Composto)
      Start: =!IsBlank(varCompostoPermitida) && !varCompostoPermitida
      Visible: =false
- tmr_Composto_Menu_1:
    Control: Timer@2.1.0
    Properties:
      AutoStart: =true
      Duration: =1800000
      Fill: =fx_CorInfo
      Font: =fx_FonteFamilia
      OnTimerEnd: |-
        =IfError(
            With(
                {resComposto: Flow_Composto.Run()},
                Set(varCompostoPermitida, resComposto.permitido);
                Set(varCompostoMensagem, resComposto.mensagem)
            ),
            Set(varCompostoPermitida, false);
            Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
        );
        If(!varCompostoPermitida, Navigate(scr_Composto))
      Repeat: =true
      Visible: =false
```

### 4.2 scr_selecaosetor_1

OnVisible:

```
If(
    IsBlank(varCompostoPermitida),
    IfError(
        With(
            {resComposto: Flow_Composto.Run()},
            Set(varCompostoPermitida, resComposto.permitido);
            Set(varCompostoMensagem, resComposto.mensagem)
        ),
        Set(varCompostoPermitida, false);
        Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
    )
);
If(
    !varCompostoPermitida,
    Navigate(scr_Composto),
    UpdateContext({ctxAgora: Now()});
    Select(btn_RecarregarMenu_1)
)
```

Timer (Ctrl+V na tela):

```yaml
- tmr_Composto_scr_selecaosetor_1:
    Control: Timer@2.1.0
    Properties:
      AutoStart: =true
      Duration: =1800000
      Fill: =fx_CorInfo
      Font: =fx_FonteFamilia
      OnTimerEnd: |-
        =IfError(
            With(
                {resComposto: Flow_Composto.Run()},
                Set(varCompostoPermitida, resComposto.permitido);
                Set(varCompostoMensagem, resComposto.mensagem)
            ),
            Set(varCompostoPermitida, false);
            Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
        );
        If(!varCompostoPermitida, Navigate(scr_Composto))
      Repeat: =true
      Visible: =false
```

### 4.3 scr_selecaosetor_Montagem

OnVisible:

```
If(
    IsBlank(varCompostoPermitida),
    IfError(
        With(
            {resComposto: Flow_Composto.Run()},
            Set(varCompostoPermitida, resComposto.permitido);
            Set(varCompostoMensagem, resComposto.mensagem)
        ),
        Set(varCompostoPermitida, false);
        Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
    )
);
If(
    !varCompostoPermitida,
    Navigate(scr_Composto),
    Select(btn_RecarregarSelM)
)
```

Timer (Ctrl+V na tela):

```yaml
- tmr_Composto_scr_selecaosetor_Montagem:
    Control: Timer@2.1.0
    Properties:
      AutoStart: =true
      Duration: =1800000
      Fill: =fx_CorInfo
      Font: =fx_FonteFamilia
      OnTimerEnd: |-
        =IfError(
            With(
                {resComposto: Flow_Composto.Run()},
                Set(varCompostoPermitida, resComposto.permitido);
                Set(varCompostoMensagem, resComposto.mensagem)
            ),
            Set(varCompostoPermitida, false);
            Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
        );
        If(!varCompostoPermitida, Navigate(scr_Composto))
      Repeat: =true
      Visible: =false
```

### 4.4 scrHoraHora_Mandril

OnVisible:

```
If(
    IsBlank(varCompostoPermitida),
    IfError(
        With(
            {resComposto: Flow_Composto.Run()},
            Set(varCompostoPermitida, resComposto.permitido);
            Set(varCompostoMensagem, resComposto.mensagem)
        ),
        Set(varCompostoPermitida, false);
        Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
    )
);
If(
    !varCompostoPermitida,
    Navigate(scr_Composto),
    UpdateContext({varDadosSalvos1: Blank()}); 
    Set(varProcessando1, false);
    UpdateContext({
        varDataProducao1: If(Hour(Now()) < 6, Today() - 1, Today()),
        varTurnoAtual1: 
    If(
        Hour(Now()) >= 5 && Hour(Now()) < 14, 
            "1º Turno",
        Hour(Now()) >= 14 || Hour(Now()) < 5,
            "2º Turno"
    )
    });
    Clear(colProducao1)
)
```

Timer (Ctrl+V na tela):

```yaml
- tmr_Composto_scrHoraHora_Mandril:
    Control: Timer@2.1.0
    Properties:
      AutoStart: =true
      Duration: =1800000
      Fill: =fx_CorInfo
      Font: =fx_FonteFamilia
      OnTimerEnd: |-
        =IfError(
            With(
                {resComposto: Flow_Composto.Run()},
                Set(varCompostoPermitida, resComposto.permitido);
                Set(varCompostoMensagem, resComposto.mensagem)
            ),
            Set(varCompostoPermitida, false);
            Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
        );
        If(!varCompostoPermitida, Navigate(scr_Composto))
      Repeat: =true
      Visible: =false
```

### 4.5 scrHoraHora_Tubo

OnVisible:

```
If(
    IsBlank(varCompostoPermitida),
    IfError(
        With(
            {resComposto: Flow_Composto.Run()},
            Set(varCompostoPermitida, resComposto.permitido);
            Set(varCompostoMensagem, resComposto.mensagem)
        ),
        Set(varCompostoPermitida, false);
        Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
    )
);
If(
    !varCompostoPermitida,
    Navigate(scr_Composto),
    UpdateContext({varDadosSalvos1: Blank()}); 
    Set(varProcessando1, false);
    UpdateContext({
        varDataProducao1: If(Hour(Now()) < 6, Today() - 1, Today()),
        varTurnoAtual1: 
    If(
        Hour(Now()) >= 5 && Hour(Now()) < 14, 
            "1º Turno",
        Hour(Now()) >= 14 || Hour(Now()) < 5,
            "2º Turno"
    )
    });
    Clear(colProducao1)
)
```

Timer (Ctrl+V na tela):

```yaml
- tmr_Composto_scrHoraHora_Tubo:
    Control: Timer@2.1.0
    Properties:
      AutoStart: =true
      Duration: =1800000
      Fill: =fx_CorInfo
      Font: =fx_FonteFamilia
      OnTimerEnd: |-
        =IfError(
            With(
                {resComposto: Flow_Composto.Run()},
                Set(varCompostoPermitida, resComposto.permitido);
                Set(varCompostoMensagem, resComposto.mensagem)
            ),
            Set(varCompostoPermitida, false);
            Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
        );
        If(!varCompostoPermitida, Navigate(scr_Composto))
      Repeat: =true
      Visible: =false
```

### 4.6 scr_AMDM02_Trancagem_1

OnVisible:

```
If(
    IsBlank(varCompostoPermitida),
    IfError(
        With(
            {resComposto: Flow_Composto.Run()},
            Set(varCompostoPermitida, resComposto.permitido);
            Set(varCompostoMensagem, resComposto.mensagem)
        ),
        Set(varCompostoPermitida, false);
        Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
    )
);
If(
    !varCompostoPermitida,
    Navigate(scr_Composto),
    UpdateContext({
        ctxAgoraAM: Now(),
        ctxDataAM: fx_DataRefEm(Now()),
        ctxAbaAM: 1,
        ctxAlteradoAM: false,
        ctxCarregandoAM: false,
        ctxIdFolhaAM: 0,
        ctxMaqAM: Coalesce(
            LookUp(Filter(fx_LayoutBalizas, tranc), Trançadeira = varMaqAM).Trançadeira,
            First(Filter(fx_LayoutBalizas, tranc)).Trançadeira
        ),
        ctxRespAM: "",
        ctxPNAM: "",
        ctxBRDAM: "",
        ctxFiosSobAM: "",
        ctxNPicksAM: "",
        ctxObsAM: "",
        ctxPickLieNovoAM: "",
        ctxPickLseNovoAM: "",
        ctxTrAM: 1,
        ctxTem2AM: false,
        ctxRegAM: Blank(),
        ctxRPkDigAM: false,
        ctxRPkLieAM: "",
        ctxRPkLseAM: "",
        ctxFotoZoomAM: false,
        ctxZoomAM: 1,
        ctxPanXAM: 0,
        ctxPanYAM: 0,
        ctxPenAM: false
    });
    ClearCollect(colODTrAM, ForAll(Sequence(5) As _o0, {Ord: _o0.Value, T: ""}));
    Set(varProcessando, false);
    Reset(cmb_MaqTrAM);
    Select(btn_CarregarAM)
)
```

Timer (Ctrl+V na tela):

```yaml
- tmr_Composto_scr_AMDM02_Trancagem_1:
    Control: Timer@2.1.0
    Properties:
      AutoStart: =true
      Duration: =1800000
      Fill: =fx_CorInfo
      Font: =fx_FonteFamilia
      OnTimerEnd: |-
        =IfError(
            With(
                {resComposto: Flow_Composto.Run()},
                Set(varCompostoPermitida, resComposto.permitido);
                Set(varCompostoMensagem, resComposto.mensagem)
            ),
            Set(varCompostoPermitida, false);
            Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
        );
        If(!varCompostoPermitida, Navigate(scr_Composto))
      Repeat: =true
      Visible: =false
```

### 4.7 scr_Bandagem_1

OnVisible:

```
If(
    IsBlank(varCompostoPermitida),
    IfError(
        With(
            {resComposto: Flow_Composto.Run()},
            Set(varCompostoPermitida, resComposto.permitido);
            Set(varCompostoMensagem, resComposto.mensagem)
        ),
        Set(varCompostoPermitida, false);
        Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
    )
);
If(
    !varCompostoPermitida,
    Navigate(scr_Composto),
    UpdateContext({
        ctxAgora: Now(),
        ctxModalSetupBand: false,
        ctxModalEnviarBand: false,
        ctxModalEditarBand: false
    });
    Set(varProcessando, false);
    Concurrent(
        ClearCollect(colDM_BANDAGEM, DM_BANDAGEM),
        ClearCollect(colDM_LAYLINE, DM_LAYLINE),
        ClearCollect(colImagensFitas, 'Imagens Fitas')
    )
)
```

Timer (Ctrl+V na tela):

```yaml
- tmr_Composto_scr_Bandagem_1:
    Control: Timer@2.1.0
    Properties:
      AutoStart: =true
      Duration: =1800000
      Fill: =fx_CorInfo
      Font: =fx_FonteFamilia
      OnTimerEnd: |-
        =IfError(
            With(
                {resComposto: Flow_Composto.Run()},
                Set(varCompostoPermitida, resComposto.permitido);
                Set(varCompostoMensagem, resComposto.mensagem)
            ),
            Set(varCompostoPermitida, false);
            Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
        );
        If(!varCompostoPermitida, Navigate(scr_Composto))
      Repeat: =true
      Visible: =false
```

### 4.8 scr_Bobinadeira_1

OnVisible:

```
If(
    IsBlank(varCompostoPermitida),
    IfError(
        With(
            {resComposto: Flow_Composto.Run()},
            Set(varCompostoPermitida, resComposto.permitido);
            Set(varCompostoMensagem, resComposto.mensagem)
        ),
        Set(varCompostoPermitida, false);
        Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
    )
);
If(
    !varCompostoPermitida,
    Navigate(scr_Composto),
    UpdateContext({
        ctxAgora: Now(),
        ctxModalDelinBob: false,
        ctxModalEnviarBob: false,
        ctxModalCancelarBob: false,
        ctxConsultaBob: false,
        ctxVersaoBob: "",
        ctxBaseBob: ""
    });
    Set(varProcessando, false);
    Concurrent(
        ClearCollect(colDM_LIST_BOBINAGEM, DM_LIST_BOBINAGEM),
        ClearCollect(colDM_WIREWINDING, DM_WIREWINDING),
        ClearCollect(colDM_FIOS, DM_FIOS)
    )
)
```

Timer (Ctrl+V na tela):

```yaml
- tmr_Composto_scr_Bobinadeira_1:
    Control: Timer@2.1.0
    Properties:
      AutoStart: =true
      Duration: =1800000
      Fill: =fx_CorInfo
      Font: =fx_FonteFamilia
      OnTimerEnd: |-
        =IfError(
            With(
                {resComposto: Flow_Composto.Run()},
                Set(varCompostoPermitida, resComposto.permitido);
                Set(varCompostoMensagem, resComposto.mensagem)
            ),
            Set(varCompostoPermitida, false);
            Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
        );
        If(!varCompostoPermitida, Navigate(scr_Composto))
      Repeat: =true
      Visible: =false
```

### 4.9 scr_Catenaria_1

OnVisible:

```
If(
    IsBlank(varCompostoPermitida),
    IfError(
        With(
            {resComposto: Flow_Composto.Run()},
            Set(varCompostoPermitida, resComposto.permitido);
            Set(varCompostoMensagem, resComposto.mensagem)
        ),
        Set(varCompostoPermitida, false);
        Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
    )
);
If(
    !varCompostoPermitida,
    Navigate(scr_Composto),
    Set(varProcessando, false);
    UpdateContext({ctxAgora: Now()});
    UpdateContext({
        ctxLimpar_cat: false,
        ctxExcluirCat: 0,
        locCorte_cat: DateAdd(ctxAgora, -24, TimeUnit.Hours)
    });
    ResetForm(frm_catenaria)
)
```

Timer (Ctrl+V na tela):

```yaml
- tmr_Composto_scr_Catenaria_1:
    Control: Timer@2.1.0
    Properties:
      AutoStart: =true
      Duration: =1800000
      Fill: =fx_CorInfo
      Font: =fx_FonteFamilia
      OnTimerEnd: |-
        =IfError(
            With(
                {resComposto: Flow_Composto.Run()},
                Set(varCompostoPermitida, resComposto.permitido);
                Set(varCompostoMensagem, resComposto.mensagem)
            ),
            Set(varCompostoPermitida, false);
            Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
        );
        If(!varCompostoPermitida, Navigate(scr_Composto))
      Repeat: =true
      Visible: =false
```

### 4.10 scr_Cobertura_2

OnVisible:

```
If(
    IsBlank(varCompostoPermitida),
    IfError(
        With(
            {resComposto: Flow_Composto.Run()},
            Set(varCompostoPermitida, resComposto.permitido);
            Set(varCompostoMensagem, resComposto.mensagem)
        ),
        Set(varCompostoPermitida, false);
        Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
    )
);
If(
    !varCompostoPermitida,
    Navigate(scr_Composto),
    UpdateContext({
        ctxAgora: Now(),
        ctxModalIniciarCob: false,
        ctxModalEnviarCob: false,
        ctxModalEditarCob: false,
        ctxModalDelinCob: false,
        ctxDelinModoInicioCob: false,
        ctxUsouTudoCob: true
    });
    Set(varProcessando, false);
    Concurrent(
        If(IsEmpty(colSpecCob), ClearCollect(colSpecCob, DM_EXTRUSAO_COBERTURA)),
        ClearCollect(colCarreteisCob, lista_carreteis)
    )
)
```

Timer (Ctrl+V na tela):

```yaml
- tmr_Composto_scr_Cobertura_2:
    Control: Timer@2.1.0
    Properties:
      AutoStart: =true
      Duration: =1800000
      Fill: =fx_CorInfo
      Font: =fx_FonteFamilia
      OnTimerEnd: |-
        =IfError(
            With(
                {resComposto: Flow_Composto.Run()},
                Set(varCompostoPermitida, resComposto.permitido);
                Set(varCompostoMensagem, resComposto.mensagem)
            ),
            Set(varCompostoPermitida, false);
            Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
        );
        If(!varCompostoPermitida, Navigate(scr_Composto))
      Repeat: =true
      Visible: =false
```

### 4.11 scr_ConferenciaSAP

OnVisible:

```
If(
    IsBlank(varCompostoPermitida),
    IfError(
        With(
            {resComposto: Flow_Composto.Run()},
            Set(varCompostoPermitida, resComposto.permitido);
            Set(varCompostoMensagem, resComposto.mensagem)
        ),
        Set(varCompostoPermitida, false);
        Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
    )
);
If(
    !varCompostoPermitida,
    Navigate(scr_Composto),
    UpdateContext({ctxAgoraConf: Now(), ctxFiltroConf: "Todas"});
    Select(btn_CarregarConf)
)
```

Timer (Ctrl+V na tela):

```yaml
- tmr_Composto_scr_ConferenciaSAP:
    Control: Timer@2.1.0
    Properties:
      AutoStart: =true
      Duration: =1800000
      Fill: =fx_CorInfo
      Font: =fx_FonteFamilia
      OnTimerEnd: |-
        =IfError(
            With(
                {resComposto: Flow_Composto.Run()},
                Set(varCompostoPermitida, resComposto.permitido);
                Set(varCompostoMensagem, resComposto.mensagem)
            ),
            Set(varCompostoPermitida, false);
            Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
        );
        If(!varCompostoPermitida, Navigate(scr_Composto))
      Repeat: =true
      Visible: =false
```

### 4.12 scr_Debandagem_2

OnVisible:

```
If(
    IsBlank(varCompostoPermitida),
    IfError(
        With(
            {resComposto: Flow_Composto.Run()},
            Set(varCompostoPermitida, resComposto.permitido);
            Set(varCompostoMensagem, resComposto.mensagem)
        ),
        Set(varCompostoPermitida, false);
        Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
    )
);
If(
    !varCompostoPermitida,
    Navigate(scr_Composto),
    UpdateContext({
        ctxAgora: Now(),
        ctxModalSetupDeband: false,
        ctxModalEnviarDeband: false,
        ctxModalEditarDeband: false
    });
    Set(varProcessando, false);
    Concurrent(
        ClearCollect(colDM_LAYLINE, DM_LAYLINE),
        ClearCollect(colCarreteisDeband, lista_carreteis)
    )
)
```

Timer (Ctrl+V na tela):

```yaml
- tmr_Composto_scr_Debandagem_2:
    Control: Timer@2.1.0
    Properties:
      AutoStart: =true
      Duration: =1800000
      Fill: =fx_CorInfo
      Font: =fx_FonteFamilia
      OnTimerEnd: |-
        =IfError(
            With(
                {resComposto: Flow_Composto.Run()},
                Set(varCompostoPermitida, resComposto.permitido);
                Set(varCompostoMensagem, resComposto.mensagem)
            ),
            Set(varCompostoPermitida, false);
            Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
        );
        If(!varCompostoPermitida, Navigate(scr_Composto))
      Repeat: =true
      Visible: =false
```

### 4.13 scr_ExtrusoraMandril_1

OnVisible:

```
If(
    IsBlank(varCompostoPermitida),
    IfError(
        With(
            {resComposto: Flow_Composto.Run()},
            Set(varCompostoPermitida, resComposto.permitido);
            Set(varCompostoMensagem, resComposto.mensagem)
        ),
        Set(varCompostoPermitida, false);
        Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
    )
);
If(
    !varCompostoPermitida,
    Navigate(scr_Composto),
    UpdateContext({
        ctxAgora: Now(),
        ctxProcExt: false,
        ctxModalDelinExt: false,
        ctxModoInicioExt: false,
        ctxModalIniExt: false,
        ctxModalRefExt: false,
        ctxModalGestaoExt: false,
        ctxModalCancExt: false,
        ctxCarrSelExt: ""
    });
    ClearCollect(colBitolasExt, fx_PNMandril);
    If(
        IsEmpty(colMaquinasMandril),
        ClearCollect(
            colMaquinasMandril,
            { Posto: "TERMOFUSAO",  Rotulo: "Solda Quente" },
            { Posto: "VIBRACIONAL", Rotulo: "Solda Vibracional" }
        )
    );
    If(
        IsEmpty(colDM_MANDREL),
        IfError(
            ClearCollect(colDM_MANDREL, DM_MANDREL),
            Notify("Não consegui ler o set-up (DM_MANDREL). Toque em atualizar.", NotificationType.Error, 8000)
        )
    );
    UpdateContext({
        ctxBitolaExt: If(
            IsBlank(ctxBitolaExt.PartNumber),
            First(colBitolasExt),
            ctxBitolaExt
        )
    });
    Select(btn_CarregarExt)
)
```

Timer (Ctrl+V na tela):

```yaml
- tmr_Composto_scr_ExtrusoraMandril_1:
    Control: Timer@2.1.0
    Properties:
      AutoStart: =true
      Duration: =1800000
      Fill: =fx_CorInfo
      Font: =fx_FonteFamilia
      OnTimerEnd: |-
        =IfError(
            With(
                {resComposto: Flow_Composto.Run()},
                Set(varCompostoPermitida, resComposto.permitido);
                Set(varCompostoMensagem, resComposto.mensagem)
            ),
            Set(varCompostoPermitida, false);
            Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
        );
        If(!varCompostoPermitida, Navigate(scr_Composto))
      Repeat: =true
      Visible: =false
```

### 4.14 scr_Finalização_1

OnVisible:

```
If(
    IsBlank(varCompostoPermitida),
    IfError(
        With(
            {resComposto: Flow_Composto.Run()},
            Set(varCompostoPermitida, resComposto.permitido);
            Set(varCompostoMensagem, resComposto.mensagem)
        ),
        Set(varCompostoPermitida, false);
        Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
    )
);
If(
    !varCompostoPermitida,
    Navigate(scr_Composto),
    UpdateContext({
                ctxAgora: Now(),
                ctxSincExt: Now(),
                ctxIniDiaExt: fx_JanelaInicioEm(Now()),
                ctxFimDiaExt: fx_JanelaFimEm(Now()),
                ctxModalFinalizarExt: false,
                ctxModalEditarExt: false,
                ctxModalExcluirExt: false,
                ctxModalDelinExt: false,
                ctxTipoExcluirExt: "",
                ctxEditandoLanceExt: Blank(),
                ctxLanceExcluirExt: Blank(),
                ctxRefugoExcluirExt: Blank(),
                ctxCabineExt: LookUp(fx_CabinesTeste, Posto = varPostoAtivo)
            });
            Set(varProcessando, false);
            Concurrent(
                ClearCollect(colColabExt, Colaboradores),
                ClearCollect(colDefeitosExt, Choices(RegistrosInspeção.CodigoDefeito)),
                If(IsEmpty(colSpecExt), ClearCollect(colSpecExt, DM_TESTE_INSP)),
                IfError(ClearCollect(colLancesExt, Filter(RegistrosInspeção, OP_ID = gal_FilaExt.Selected.OP)); true, Notify("Não consegui ler os lances desta OP. Toque em atualizar antes de continuar.", NotificationType.Error, 8000)),
                IfError(ClearCollect(colRefugoExt, Filter(TiposErros, OP_ID = gal_FilaExt.Selected.OP)); true, Notify("Não consegui ler os reprovados desta OP. Toque em atualizar antes de continuar.", NotificationType.Error, 8000)),
                IfError(ClearCollect(
                    colInspDiaExt,
                    Filter(
                        RegistrosInspeção,
                        Created >= ctxIniDiaExt,
                        Created < ctxFimDiaExt
                    )
                ); true, Notify("Não consegui ler o total do dia. Toque em atualizar.", NotificationType.Error, 8000))
            )
)
```

Timer (Ctrl+V na tela):

```yaml
- tmr_Composto_scr_Finalizacao_1:
    Control: Timer@2.1.0
    Properties:
      AutoStart: =true
      Duration: =1800000
      Fill: =fx_CorInfo
      Font: =fx_FonteFamilia
      OnTimerEnd: |-
        =IfError(
            With(
                {resComposto: Flow_Composto.Run()},
                Set(varCompostoPermitida, resComposto.permitido);
                Set(varCompostoMensagem, resComposto.mensagem)
            ),
            Set(varCompostoPermitida, false);
            Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
        );
        If(!varCompostoPermitida, Navigate(scr_Composto))
      Repeat: =true
      Visible: =false
```

### 4.15 scr_HoraHora_Cobertura_1

OnVisible:

```
If(
    IsBlank(varCompostoPermitida),
    IfError(
        With(
            {resComposto: Flow_Composto.Run()},
            Set(varCompostoPermitida, resComposto.permitido);
            Set(varCompostoMensagem, resComposto.mensagem)
        ),
        Set(varCompostoPermitida, false);
        Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
    )
);
If(
    !varCompostoPermitida,
    Navigate(scr_Composto),
    UpdateContext({
        ctxAgoraHHC: Now(),
        ctxAlteradoHHC: false,
        ctxModalReplicaHHC: false,
        ctxSobrescreverHHC: false,
        ctxOrdOrigemHHC: 0,
        ctxCarregadoHHC: false,
        ctxFecharHHC: false,
        ctxTurnoCarregadoHHC: 0,
        ctxDataCarregadaHHC: fx_DataRefEm(Now())
    });
    Set(varProcessando, false);
    Set(varTurnoHHC, fx_TurnoLabelEm(Now()));
    Reset(cmb_TurnoHHC);
    If(
        IsEmpty(colSpecCob),
        IfError(
            ClearCollect(colSpecCob, DM_EXTRUSAO_COBERTURA),
            Notify("Não consegui carregar a velocidade das mangueiras. Sem ela a meta fica em branco — confira a rede e reabra a tela.", NotificationType.Error, 10000)
        )
    );
    Select(btn_CarregarHHC)
)
```

Timer (Ctrl+V na tela):

```yaml
- tmr_Composto_scr_HoraHora_Cobertura_1:
    Control: Timer@2.1.0
    Properties:
      AutoStart: =true
      Duration: =1800000
      Fill: =fx_CorInfo
      Font: =fx_FonteFamilia
      OnTimerEnd: |-
        =IfError(
            With(
                {resComposto: Flow_Composto.Run()},
                Set(varCompostoPermitida, resComposto.permitido);
                Set(varCompostoMensagem, resComposto.mensagem)
            ),
            Set(varCompostoPermitida, false);
            Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
        );
        If(!varCompostoPermitida, Navigate(scr_Composto))
      Repeat: =true
      Visible: =false
```

### 4.16 scr_HoraHora_Trancagem_2

OnVisible:

```
If(
    IsBlank(varCompostoPermitida),
    IfError(
        With(
            {resComposto: Flow_Composto.Run()},
            Set(varCompostoPermitida, resComposto.permitido);
            Set(varCompostoMensagem, resComposto.mensagem)
        ),
        Set(varCompostoPermitida, false);
        Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
    )
);
If(
    !varCompostoPermitida,
    Navigate(scr_Composto),
    UpdateContext({
        ctxAgoraHHT: Now(),
        ctxAlteradoHHT: false,
        ctxModalPendHHT: false,
        ctxModalReplicaHHT: false,
        ctxSobrescreverHHT: false,
        ctxOrdOrigemHHT: 0,
        ctxCelulaCarregadaHHT: "",
        ctxCarregandoHHT: false,
        ctxIniCargaHHT: Now(),
        ctxTurnoCarregadoHHT: 0,
        ctxDataCarregadaHHT: fx_DataRefEm(Now())
    });
    Set(varProcessando, false);
    Set(varTurnoHHT, fx_TurnoLabelEm(Now()));
    Reset(cmb_TurnoHHT);
    Reset(cmb_CelulaHHT);
    Select(btn_CarregarHHT)
)
```

Timer (Ctrl+V na tela):

```yaml
- tmr_Composto_scr_HoraHora_Trancagem_2:
    Control: Timer@2.1.0
    Properties:
      AutoStart: =true
      Duration: =1800000
      Fill: =fx_CorInfo
      Font: =fx_FonteFamilia
      OnTimerEnd: |-
        =IfError(
            With(
                {resComposto: Flow_Composto.Run()},
                Set(varCompostoPermitida, resComposto.permitido);
                Set(varCompostoMensagem, resComposto.mensagem)
            ),
            Set(varCompostoPermitida, false);
            Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
        );
        If(!varCompostoPermitida, Navigate(scr_Composto))
      Repeat: =true
      Visible: =false
```

### 4.17 scr_mandril_1

OnVisible:

```
If(
    IsBlank(varCompostoPermitida),
    IfError(
        With(
            {resComposto: Flow_Composto.Run()},
            Set(varCompostoPermitida, resComposto.permitido);
            Set(varCompostoMensagem, resComposto.mensagem)
        ),
        Set(varCompostoPermitida, false);
        Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
    )
);
If(
    !varCompostoPermitida,
    Navigate(scr_Composto),
    UpdateContext({
        ctxAgora: Now(),
        ctxModalSetupMand: false,
        ctxModalCarretelMand: false,
        ctxDesmoldanteMand: "",
        ctxModalTurnoMand: false,
        ctxModalCorrigirMand: false,
        ctxMotivoCorrMand: ""
    });
    Set(varProcessando, false);
    ClearCollect(ColTabelaBitolas, fx_PNMandril);
    If(
        IsEmpty(colMaquinasMandril),
        ClearCollect(colMaquinasMandril,
            { Posto: "TERMOFUSAO",  Rotulo: "Solda Quente" },
            { Posto: "VIBRACIONAL", Rotulo: "Solda Vibracional" }
        )
    );
    If(
        IsEmpty(colDM_MANDREL),
        IfError(
            ClearCollect(colDM_MANDREL, DM_MANDREL),
            Notify("Não consegui ler o set-up (DM_MANDREL). Toque em atualizar.", NotificationType.Error, 8000)
        )
    );
    Set(varPostoAtivo, If(IsBlank(varPostoAtivo), First(colMaquinasMandril).Posto, varPostoAtivo));
    Set(varModoMandril, "Velho");
    Select(btn_CarregarPostoMand_2)
)
```

Timer (Ctrl+V na tela):

```yaml
- tmr_Composto_scr_mandril_1:
    Control: Timer@2.1.0
    Properties:
      AutoStart: =true
      Duration: =1800000
      Fill: =fx_CorInfo
      Font: =fx_FonteFamilia
      OnTimerEnd: |-
        =IfError(
            With(
                {resComposto: Flow_Composto.Run()},
                Set(varCompostoPermitida, resComposto.permitido);
                Set(varCompostoMensagem, resComposto.mensagem)
            ),
            Set(varCompostoPermitida, false);
            Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
        );
        If(!varCompostoPermitida, Navigate(scr_Composto))
      Repeat: =true
      Visible: =false
```

### 4.18 scr_Montagem_HoraHora

OnVisible:

```
If(
    IsBlank(varCompostoPermitida),
    IfError(
        With(
            {resComposto: Flow_Composto.Run()},
            Set(varCompostoPermitida, resComposto.permitido);
            Set(varCompostoMensagem, resComposto.mensagem)
        ),
        Set(varCompostoPermitida, false);
        Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
    )
);
If(
    !varCompostoPermitida,
    Navigate(scr_Composto),
    Set(varAgora, Now());
    Set(varDataTela, fx_DataRefEm(varAgora));
    Set(varTurnoTela, fx_TurnoLabelEm(varAgora));
    Set(varCelulaMontagem,
        Coalesce(varCelulaMontagem, LookUp(MapeamentoSetor, EmailComputador = User().Email).Celula)
    );
    Set(varProcM, false);
    Set(varPNAtivo, Blank());
    Set(varPopupFinalizar_M, false);
    UpdateContext({ctxPopExcesso: false});
    Set(varFalhaM, false);
    IfError(
        Concurrent(
            Refresh(Producao_Montagem),
            Refresh(Paradas_Montagem)
        ),
        Set(varFalhaM, true)
    );
    ClearCollect(colOPsAbertas, Table({Value: "— Sem OP —"}));
    Collect(colOPsAbertas,
        ForAll(
            Filter(Producao_Montagem,
                Celula = varCelulaMontagem && Status = "EmAndamento"
            ) As r,
            {Value: r.PN & " (OT " & Text(r.OT, "[$-en-US]0") & ")"}
        )
    );
    ClearCollect(colParadasM,
        Filter(Paradas_Montagem,
            Celula = varCelulaMontagem &&
            Data >= DateAdd(varDataTela, -2, TimeUnit.Days)
        )
    );
    ClearCollect(colDescM,
        ForAll(
            Distinct(
                Filter(colParadasM,
                    Motivo <> fx_MotivoTempoExcedido && !IsBlank(OPVinculada)
                ),
                OPVinculada
            ) As d,
            {
                Chave: d.Value,
                MinDesc: Sum(
                    Filter(colParadasM,
                        OPVinculada = d.Value && Motivo <> fx_MotivoTempoExcedido
                    ),
                    TempoParadoMin
                )
            }
        )
    )
)
```

Timer (Ctrl+V na tela):

```yaml
- tmr_Composto_scr_Montagem_HoraHora:
    Control: Timer@2.1.0
    Properties:
      AutoStart: =true
      Duration: =1800000
      Fill: =fx_CorInfo
      Font: =fx_FonteFamilia
      OnTimerEnd: |-
        =IfError(
            With(
                {resComposto: Flow_Composto.Run()},
                Set(varCompostoPermitida, resComposto.permitido);
                Set(varCompostoMensagem, resComposto.mensagem)
            ),
            Set(varCompostoPermitida, false);
            Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
        );
        If(!varCompostoPermitida, Navigate(scr_Composto))
      Repeat: =true
      Visible: =false
```

### 4.19 scr_RefugoBobinadeira_1

OnVisible:

```
If(
    IsBlank(varCompostoPermitida),
    IfError(
        With(
            {resComposto: Flow_Composto.Run()},
            Set(varCompostoPermitida, resComposto.permitido);
            Set(varCompostoMensagem, resComposto.mensagem)
        ),
        Set(varCompostoPermitida, false);
        Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
    )
);
If(
    !varCompostoPermitida,
    Navigate(scr_Composto),
    UpdateContext({ctxAgora: Now()});
    UpdateContext({
        ctxIniBob: fx_JanelaInicioEm(ctxAgora),
        ctxFimBob: fx_JanelaFimEm(ctxAgora)
    });
    Set(varProcessando, false);
    ClearCollect(
        colRefugoBob,
        Sort(
            Filter(
                Refugo_Bobinadeira,
                DataHoraRefugo >= ctxIniBob,
                DataHoraRefugo < ctxFimBob
            ),
            DataHoraRefugo,
            SortOrder.Descending
        )
    )
)
```

Timer (Ctrl+V na tela):

```yaml
- tmr_Composto_scr_RefugoBobinadeira_1:
    Control: Timer@2.1.0
    Properties:
      AutoStart: =true
      Duration: =1800000
      Fill: =fx_CorInfo
      Font: =fx_FonteFamilia
      OnTimerEnd: |-
        =IfError(
            With(
                {resComposto: Flow_Composto.Run()},
                Set(varCompostoPermitida, resComposto.permitido);
                Set(varCompostoMensagem, resComposto.mensagem)
            ),
            Set(varCompostoPermitida, false);
            Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
        );
        If(!varCompostoPermitida, Navigate(scr_Composto))
      Repeat: =true
      Visible: =false
```

### 4.20 scr_Trancagem_4

OnVisible:

```
If(
    IsBlank(varCompostoPermitida),
    IfError(
        With(
            {resComposto: Flow_Composto.Run()},
            Set(varCompostoPermitida, resComposto.permitido);
            Set(varCompostoMensagem, resComposto.mensagem)
        ),
        Set(varCompostoPermitida, false);
        Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
    )
);
If(
    !varCompostoPermitida,
    Navigate(scr_Composto),
    UpdateContext({
        ctxAgora: Now(),
        ctxModalDelinTr3: false,
        ctxModalIniciarTr3: false,
        ctxModalEnviarTr3: false,
        ctxModalEditarTr3: false,
        ctxModalPedidoTr3: false,
        ctxModalSugFioTr3: false,
        ctxDelinModoInicioTr3: false,
        ctxUsouTudoTr3: true,
        ctxTodasBobinasTr3: false,
        ctxBobinaSelTr3: 0,
        ctxLiSugTr3: "",
        ctxFioSugTr3: "",
        ctxModalCancTr3: false
    });
    Set(varProcessando, false);
    ClearCollect(colTrancFiltroTr3, {Filtro: "Todas"});
    Collect(
        colTrancFiltroTr3,
        ForAll(fx_CelulasTrancagem As _c, {Filtro: Text(_c.Celula)})
    );
    Concurrent(
        ClearCollect(
            colColabTr3,
            Sort(
                Filter(
                    ForAll(
                        Colaboradores As _c2,
                        { Nome: Trim(Text(_c2.Nome)) }
                    ) As _n,
                    !IsBlank(_n.Nome)
                ),
                Nome,
                SortOrder.Ascending
            )
        ),
        If(IsEmpty(colSpecTr3), ClearCollect(colSpecTr3, DM_TRANÇAGEM)),
        If(IsEmpty(colEngrTr3), ClearCollect(colEngrTr3, DM_ENGRENAGENS)),
        If(IsEmpty(colFiosTr3), ClearCollect(colFiosTr3, DM_FIOS)),
        If(IsEmpty(colWireTr3), ClearCollect(colWireTr3, DM_WIREWINDING))
    );
    Select(btn_RecarregarTr3_1);
    Reset(cmb_FiltroTr3_1)
)
```

Timer (Ctrl+V na tela):

```yaml
- tmr_Composto_scr_Trancagem_4:
    Control: Timer@2.1.0
    Properties:
      AutoStart: =true
      Duration: =1800000
      Fill: =fx_CorInfo
      Font: =fx_FonteFamilia
      OnTimerEnd: |-
        =IfError(
            With(
                {resComposto: Flow_Composto.Run()},
                Set(varCompostoPermitida, resComposto.permitido);
                Set(varCompostoMensagem, resComposto.mensagem)
            ),
            Set(varCompostoPermitida, false);
            Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
        );
        If(!varCompostoPermitida, Navigate(scr_Composto))
      Repeat: =true
      Visible: =false
```

### 4.21 scr_tubo_1

OnVisible:

```
If(
    IsBlank(varCompostoPermitida),
    IfError(
        With(
            {resComposto: Flow_Composto.Run()},
            Set(varCompostoPermitida, resComposto.permitido);
            Set(varCompostoMensagem, resComposto.mensagem)
        ),
        Set(varCompostoPermitida, false);
        Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
    )
);
If(
    !varCompostoPermitida,
    Navigate(scr_Composto),
    UpdateContext({
        ctxAgora: Now(),
        ctxModalIniciarTubo: false,
        ctxModalEnviarTubo: false,
        ctxModalEditarTubo: false,
        ctxModalDelinTubo: false,
        ctxDelinModoInicio: false,
        ctxUsouTudoTubo: true,
        ctxModalOutraMangTubo: false,
        ctxModalExcecaoTubo: false,
        ctxModalCancTubo: false
    });
    Set(varProcessando, false);
    ClearCollect(colMangEscTubo, colMangueiras, {NomeMangueira: fx_MangueiraOutra});
    If(
        IsEmpty(colSpecTubo),
        IfError(
            ClearCollect(colSpecTubo, DM_TUBE_EXTRUSION);
            true,
            Notify("Não consegui ler o delineamento (DM_TUBE_EXTRUSION). Toque em atualizar.", NotificationType.Error, 8000);
            false
        )
    );
    Set(varMangueiraEscolhidaTubo, Blank());
    Set(varTrPlanoTubo, Blank());
    Set(varQtdPlanoTubo, Blank());
    Select(ico_RefreshTubo_1)
)
```

Timer (Ctrl+V na tela):

```yaml
- tmr_Composto_scr_tubo_1:
    Control: Timer@2.1.0
    Properties:
      AutoStart: =true
      Duration: =1800000
      Fill: =fx_CorInfo
      Font: =fx_FonteFamilia
      OnTimerEnd: |-
        =IfError(
            With(
                {resComposto: Flow_Composto.Run()},
                Set(varCompostoPermitida, resComposto.permitido);
                Set(varCompostoMensagem, resComposto.mensagem)
            ),
            Set(varCompostoPermitida, false);
            Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
        );
        If(!varCompostoPermitida, Navigate(scr_Composto))
      Repeat: =true
      Visible: =false
```

### 4.22 scr_Vulcanizacao_1

OnVisible:

```
If(
    IsBlank(varCompostoPermitida),
    IfError(
        With(
            {resComposto: Flow_Composto.Run()},
            Set(varCompostoPermitida, resComposto.permitido);
            Set(varCompostoMensagem, resComposto.mensagem)
        ),
        Set(varCompostoPermitida, false);
        Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
    )
);
If(
    !varCompostoPermitida,
    Navigate(scr_Composto),
    UpdateContext({
        ctxAgora: Now(),
        ctxModalSetupVulca: false,
        ctxModalLoteVulca: false,
        ctxEditarPlanoVulca: false
    });
    Clear(colLoteVulca);
    Clear(colProntasVulca)
)
```

Timer (Ctrl+V na tela):

```yaml
- tmr_Composto_scr_Vulcanizacao_1:
    Control: Timer@2.1.0
    Properties:
      AutoStart: =true
      Duration: =1800000
      Fill: =fx_CorInfo
      Font: =fx_FonteFamilia
      OnTimerEnd: |-
        =IfError(
            With(
                {resComposto: Flow_Composto.Run()},
                Set(varCompostoPermitida, resComposto.permitido);
                Set(varCompostoMensagem, resComposto.mensagem)
            ),
            Set(varCompostoPermitida, false);
            Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
        );
        If(!varCompostoPermitida, Navigate(scr_Composto))
      Repeat: =true
      Visible: =false
```

### 4.23 TelaImpressao

OnVisible:

```
If(
    IsBlank(varCompostoPermitida),
    IfError(
        With(
            {resComposto: Flow_Composto.Run()},
            Set(varCompostoPermitida, resComposto.permitido);
            Set(varCompostoMensagem, resComposto.mensagem)
        ),
        Set(varCompostoPermitida, false);
        Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
    )
);
If(
    !varCompostoPermitida,
    Navigate(scr_Composto),
    If(
        varPackingManual,
        Reset(inp_OPManualImp);
        Reset(inp_PNManualImp);
        Reset(cmb_OperadorManualImp);
        Reset(cmb_MotivoManualImp)
    )
)
```

Timer (Ctrl+V na tela):

```yaml
- tmr_Composto_TelaImpressao:
    Control: Timer@2.1.0
    Properties:
      AutoStart: =true
      Duration: =1800000
      Fill: =fx_CorInfo
      Font: =fx_FonteFamilia
      OnTimerEnd: |-
        =IfError(
            With(
                {resComposto: Flow_Composto.Run()},
                Set(varCompostoPermitida, resComposto.permitido);
                Set(varCompostoMensagem, resComposto.mensagem)
            ),
            Set(varCompostoPermitida, false);
            Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
        );
        If(!varCompostoPermitida, Navigate(scr_Composto))
      Repeat: =true
      Visible: =false
```

## 5. App Checker e publicar

Rode o App Checker (não pode ter erro novo) e publique. Depois teste no tablet: Ativo=Não bloqueia; voltar não sai de scr_Composto; Ativo=Sim + reabrir libera.
