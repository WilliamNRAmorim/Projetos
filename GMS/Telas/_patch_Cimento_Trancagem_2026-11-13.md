# Patch: cimento na Trançagem (TH05) · 13/11/2026

Plano aprovado pelo William em 13/11/2026. Arquivos gravados em `GMS/Telas/`: `Formulas.txt` (v3.0.18), `scr_Trancagem_4.txt` (versão da tela 0.3.2 → 0.4.0), `scr_PainelCelula_1.txt` e `scr_HoraHora_Trancagem_2.txt` (0.7.2 → 0.7.3). Revisão de 13/11: máquina ativa da Hora-Hora, sem evento Cimento-Fim, `_g7` do Painel. Nada foi publicado, commitado nem criado no SharePoint.

Regra da ordem: crie as 3 colunas, cole o `Formulas.txt` (App.Formulas) e só depois cole as telas. Sem as colunas, o Studio acusa erro de nome em todo `Cimento_Maquina`, `InicioCimento_Trancagem` e `FimCimento_Trancagem`.

## 1. Colunas a criar na `ficha_producao` (o William cria)

| Nome interno exato | Tipo | Quem grava |
|---|---|---|
| `InicioCimento_Trancagem` | Data e hora | botão "Terminar trança → aplicar cimento" (TH05, trança própria) e "Iniciar cimento" (OP só cimento) |
| `FimCimento_Trancagem` | Data e hora | Enviar normal da TH05 (quando há InicioCimento) e "Enviar para Cobertura" da OP só cimento |
| `Cimento_Maquina` | Texto de uma linha | Enviar da TM04 (qualquer trançadeira ≠ TH05) grava `TH05` |

Sem ç e sem espaço nos nomes. As três ficam em branco nas OPs de hoje, e em branco = comportamento de antes.

## 2. App.Formulas (`Formulas.txt`, v3.0.18)

Acrescentar na §6 (depois de `fx_InicioCronoVulca`):

```powerfx

// [v3.0.18 · cimento da Trançagem · 13/11/2026] A mangueira do delineamento (DM_TRANÇAGEM, _51OBSERVACAO)
// pede cimento? Hoje: HC101-4, HC101-6, HC139-7 e HC139-7_S-GX. Só a TH05 aplica; a TM04 às vezes trança e
// manda para a TH05 só passar o cimento. Mesma chave da tela (fx_NormCodigo(PARTNUMBER)); qualquer linha da
// mangueira com "CIMENTO" na observação vale (a construção não entra: o cimento é da mangueira).
// Sem delineamento ou observação vazia = false.
// ⚠ EXCEÇÃO À REGRA 4 DO CABEÇALHO (só a §10 toca fonte): lê DM_TRANÇAGEM aqui por pedido do desenho aprovado
// (como fx_VelocidadeTeorica, §11). O LookUp não é delegável (fx_NormCodigo): vale para as linhas que o
// conector devolve (limite de linhas do app).
fx_PrecisaCimento(bitola: Text): Boolean =
    !IsBlank(
        LookUp(
            DM_TRANÇAGEM,
            fx_NormCodigo(PARTNUMBER) = fx_NormCodigo(bitola) &&
            "CIMENTO" in Upper(Text(_51OBSERVACAO))
        ).PARTNUMBER
    );

// Estado da Trançagem com a fase do cimento (carimbo de hora, igual Vulcanização · C39).
// status_processo continua "Em processo" durante o cimento: Hora-Hora, painel e BI não mudam.
// fx_EstadoContinuo NÃO é alterada: as outras etapas seguem com ela.
fx_EstadoTranc(status: Text, inicioCimento: DateTime): Text =
    If(
        status <> "Em processo", "AGUARDANDO",
        IsBlank(inicioCimento),  "TRANÇANDO",
        "CIMENTO"
    );
```

Na `fx_CorEstadoPosto` (§12), acrescentar a linha `"CIMENTO",      fx_CorGelo,` logo depois da linha `"RESFRIANDO",   fx_CorGelo,`. Cabeçalho do arquivo: `v3.0.18 · 2026-11-13` e a frase "v3.0.18 só ACRESCENTA…" no fim da linha de histórico (só comentário). `fx_EstadoContinuo` não foi alterada.

## 3. scr_Trancagem_4 — propriedades alteradas (cole a fórmula inteira)

Cada item abaixo é controle → propriedade → fórmula completa (sem o `=` inicial).


### 3.1 Fila

**`gal_FilaTr3_1` → `Items`** (delegável: Filter externo só com `processo`, `Trançadeira`, `Cimento_Maquina`; o `Cancelado` continua no Filter de fora, como era)

```powerfx
If(
    IsBlank(cmb_FiltroTr3_1.Selected.Filtro) || cmb_FiltroTr3_1.Selected.Filtro = "Todas",
    Sort(
        Filter(Filter(ficha_producao, processo = "Trançadeira"), Coalesce(status_processo, "") <> "Cancelado"),
        OP,
        SortOrder.Ascending
    ),
    Sort(
        Filter(
            Filter(
                ficha_producao,
                processo = "Trançadeira",
                (Trançadeira = cmb_FiltroTr3_1.Selected.Filtro && IsBlank(Cimento_Maquina)) ||
                Cimento_Maquina = cmb_FiltroTr3_1.Selected.Filtro
            ),
            Coalesce(status_processo, "") <> "Cancelado"
        ),
        OP,
        SortOrder.Ascending
    )
)
```

**`btn_EstadoFilaTr3_1` → `Color`**

```powerfx
Switch(
    fx_EstadoTranc(ThisItem.status_processo, ThisItem.InicioCimento_Trancagem),
    "TRANÇANDO", fx_CorOK,
    "CIMENTO",   fx_CorGelo,
    fx_CorAlerta
)
```

**`btn_EstadoFilaTr3_1` → `Fill`**

```powerfx
Switch(
    fx_EstadoTranc(ThisItem.status_processo, ThisItem.InicioCimento_Trancagem),
    "TRANÇANDO", fx_CorOKSuave,
    "CIMENTO",   fx_CorGeloSuave,
    fx_CorAlertaSuave
)
```

**`btn_EstadoFilaTr3_1` → `Text`**

```powerfx
Switch(
    fx_EstadoTranc(ThisItem.status_processo, ThisItem.InicioCimento_Trancagem),
    "TRANÇANDO", "Produzindo",
    "CIMENTO",   "Cimento",
    "Aguardando"
)
```

**`lbl_CronoFilaTr3_1` → `Text`**

```powerfx
fx_Crono(
    If(
        fx_EstadoTranc(ThisItem.status_processo, ThisItem.InicioCimento_Trancagem) = "CIMENTO",
        ThisItem.InicioCimento_Trancagem,
        fx_InicioCronoContinuo(
            fx_EstadoContinuo(ThisItem.status_processo),
            ThisItem.InicioAguardando_Trançadeira,
            ThisItem.data_hora_inicio_trancadeira,
            ThisItem.Created
        )
    ),
    ctxAgora
)
```

Controle novo dentro da galeria `gal_FilaTr3_1` (marca "SÓ CIMENTO"). Em "Inserir" crie um botão clássico dentro do template, ou cole o YAML no template:

**`btn_SoCimentoFilaTr3_1`**

```yaml
    - btn_SoCimentoFilaTr3_1:
        Control: Classic/Button@2.2.0
        Properties:
          BorderColor: =Color.Transparent
          BorderThickness: =0
          Color: =If(ThisItem.IsSelected, fx_CorSuperficie, fx_CorGelo)
          Fill: =If(ThisItem.IsSelected, fx_CorChip, fx_CorGeloSuave)
          Font: =fx_FonteFamilia
          FontWeight: =FontWeight.Bold
          Height: =26
          HoverFill: =Self.Fill
          OnSelect: =Select(Parent)
          PressedFill: =Self.Fill
          RadiusBottomLeft: =fx_RaioS
          RadiusBottomRight: =fx_RaioS
          RadiusTopLeft: =fx_RaioS
          RadiusTopRight: =fx_RaioS
          Size: =fx_FonteApoio
          Text: ="SÓ CIMENTO"
          Visible: =!IsBlank(ThisItem.Cimento_Maquina)
          Width: =84
          X: =122
          Y: =66
```


### 3.2 Situação no detalhe da OP

**`lbl_RotSituacaoTr3_1` → `Text`**

```powerfx
"SITUAÇÃO" &
If(
    fx_EstadoTranc(gal_FilaTr3_1.Selected.status_processo, gal_FilaTr3_1.Selected.InicioCimento_Trancagem) = "CIMENTO",
    "  ·  " & fx_Crono(gal_FilaTr3_1.Selected.InicioCimento_Trancagem, ctxAgora),
    ""
)
```

**`lbl_RotSituacaoTr3_1` → `Width`**

```powerfx
170
```

**`lbl_ValSituacaoTr3_1` → `Color`**

```powerfx
Switch(
    fx_EstadoTranc(gal_FilaTr3_1.Selected.status_processo, gal_FilaTr3_1.Selected.InicioCimento_Trancagem),
    "TRANÇANDO", fx_CorOK,
    "CIMENTO",   fx_CorGelo,
    fx_CorAlerta
)
```

**`lbl_ValSituacaoTr3_1` → `Text`**

```powerfx
Switch(
    fx_EstadoTranc(gal_FilaTr3_1.Selected.status_processo, gal_FilaTr3_1.Selected.InicioCimento_Trancagem),
    "TRANÇANDO", "Produzindo",
    "CIMENTO",   "Aplicando cimento",
    "Aguardando"
)
```

**`lbl_ValSituacaoTr3_1` → `Width`**

```powerfx
170
```


### 3.3 Campos da trança travados quando a OP é só cimento

Mesma mudança no `DisplayMode` de 9 controles: `inp_LiTr3_1`, `inp_FioTr3_1`, `btn_SugFioTr3_1`, `inp_QtdTr3_1`, `inp_RefugoTr3_1`, `inp_PicksTr3_1`, `inp_DiametroTr3_1`, `cmb_OperadorTr3_1`, `inp_ObsTr3_1`. O valor mostrado (Default) continua o gravado pela TM04, só para leitura.

```powerfx
If(
    fx_EstadoContinuo(gal_FilaTr3_1.Selected.status_processo) = "PRODUZINDO" && !varProcessando &&
    IsBlank(gal_FilaTr3_1.Selected.Cimento_Maquina),
    DisplayMode.Edit,
    DisplayMode.Disabled
)
```


### 3.4 Avisos

**`lbl_AvisoInicieTr3_1` → `Text`**

```powerfx
If(
    IsBlank(gal_FilaTr3_1.Selected.Cimento_Maquina),
    "Selecione a OP na fila e toque em Iniciar Trançagem — primeiro o delineamento, depois o carretel de saída. Os campos abrem quando a OP estiver produzindo.",
    "OP já trançada na " & Coalesce(gal_FilaTr3_1.Selected.Trançadeira, "—") & ". Toque em Iniciar cimento para passar o cimento na " & gal_FilaTr3_1.Selected.Cimento_Maquina & " e depois envie para a Cobertura."
)
```

**`lbl_AlertaTr3_1` → `Visible`**

```powerfx
!IsBlank(Self.Text) &&
fx_EstadoContinuo(gal_FilaTr3_1.Selected.status_processo) = "PRODUZINDO" &&
IsBlank(gal_FilaTr3_1.Selected.Cimento_Maquina)
```


### 3.5 Rodapé

**`btn_IniciarTr3_1` → `Text`**

```powerfx
If(IsBlank(gal_FilaTr3_1.Selected.Cimento_Maquina), "Iniciar Trançagem", "Iniciar cimento")
```

**`btn_IniciarTr3_1` → `OnSelect`**

```powerfx
If(
    !IsBlank(gal_FilaTr3_1.Selected.Cimento_Maquina),
    Set(varProcessando, true);
    Refresh(ficha_producao);
    With(
        {
            _r: LookUp(ficha_producao, ID = gal_FilaTr3_1.Selected.ID),
            _agora: Now()
        },
        With(
            {_min: fx_MinutosDoDia(_agora)},
            If(
                _r.Modified <> gal_FilaTr3_1.Selected.Modified,
                Notify("Este registro foi alterado por outro usuário. A fila foi recarregada.", NotificationType.Error, 8000);
                Select(btn_RecarregarTr3_1);
                Set(varProcessando, false),
                _r.status_processo = "Em processo",
                Notify("Esta OP já foi iniciada por outro operador. Atualize a fila.", NotificationType.Error, 8000);
                Select(btn_RecarregarTr3_1);
                Set(varProcessando, false),
                Patch(
                    ficha_producao,
                    _r,
                    {
                        status_processo: "Em processo",
                        InicioCimento_Trancagem: _agora
                    }
                );
                If(
                    !IsEmpty(Errors(ficha_producao)),
                    Notify("Falha ao iniciar o cimento: " & First(Errors(ficha_producao)).Message, NotificationType.Error, 12000);
                    Set(varProcessando, false),
                    Patch(
                        Eventos_Producao,
                        Defaults(Eventos_Producao),
                        {
                            Title: Text(_r.ID) & "-Trancagem-Cimento-Inicio",
                            origem: {Value: "ficha_producao"},
                            origem_ID: _r.ID,
                            etapa: {Value: "Trançagem"},
                            tipo: {Value: "Início"},
                            data_hora: _agora,
                            data_ref: fx_DataRefEm(_agora),
                            turno: fx_Turno(_min),
                            bitola: _r.Bitola,
                            recurso: _r.Cimento_Maquina,
                            operador: User().FullName
                        }
                    );
                    If(
                        !IsEmpty(Errors(Eventos_Producao)),
                        Notify("Evento de início do cimento não gravou: " & First(Errors(Eventos_Producao)).Message, NotificationType.Error, 10000)
                    );
                    Select(btn_RecarregarTr3_1);
                    Set(varProcessando, false);
                    Notify("Cimento iniciado na " & _r.Cimento_Maquina & ".", NotificationType.Success, 5000)
                )
            )
        )
    ),
    If(IsEmpty(colSpecTr3), ClearCollect(colSpecTr3, DM_TRANÇAGEM));
    UpdateContext({ctxDelinModoInicioTr3: true, ctxModalDelinTr3: true})
)
```

**`btn_SalvarTr3_1` → `Visible`**

```powerfx
fx_EstadoContinuo(gal_FilaTr3_1.Selected.status_processo) = "PRODUZINDO" &&
IsBlank(gal_FilaTr3_1.Selected.Cimento_Maquina)
```

**`btn_SalvarTr3_1` → `Width`**

```powerfx
If(btn_CimentoTr3_1.Visible, 140, 230)
```

**`btn_SalvarTr3_1` → `X`**

```powerfx
If(btn_CimentoTr3_1.Visible, 800, 560)
```

**`btn_EnviarTr3_1` → `Text`**

```powerfx
If(
    gal_FilaTr3_1.Selected.Trançadeira <> "TH05" &&
    fx_PrecisaCimento(gal_FilaTr3_1.Selected.Mangueira),
    "Enviar para cimento na TH05",
    "Enviar p/ Cobertura"
)
```

**`btn_EnviarTr3_1` → `Visible`**

```powerfx
fx_EstadoContinuo(gal_FilaTr3_1.Selected.status_processo) = "PRODUZINDO" &&
IsBlank(gal_FilaTr3_1.Selected.Cimento_Maquina)
```

**`btn_EnviarTr3_1` → `Width`**

```powerfx
If(btn_CimentoTr3_1.Visible, 180, 290)
```

**`btn_EnviarTr3_1` → `X`**

```powerfx
If(btn_CimentoTr3_1.Visible, 950, 810)
```

**`btn_CancelarOpTr3_1` → `Visible`**

```powerfx
fx_EstadoContinuo(gal_FilaTr3_1.Selected.status_processo) = "PRODUZINDO" &&
IsBlank(gal_FilaTr3_1.Selected.Cimento_Maquina)
```

Controles novos no rodapé (YAML completo; ficam logo depois do `btn_EnviarTr3_1`):

**`btn_CimentoTr3_1`**

```yaml
    - btn_CimentoTr3_1:
        Control: Classic/Button@2.2.0
        Properties:
          BorderColor: =Color.Transparent
          BorderThickness: =0
          Color: =fx_CorSuperficie
          DisabledFill: =fx_CorBorda
          DisplayMode: |-
            =If(
                IsBlank(gal_FilaTr3_1.Selected.ID) || varProcessando,
                DisplayMode.Disabled,
                DisplayMode.Edit
            )
          Fill: =fx_CorInfo
          Font: =fx_FonteFamilia
          FontWeight: =FontWeight.Bold
          Height: =fx_AlturaAcao
          HoverFill: =ColorFade(Self.Fill, -20%)
          OnSelect: |-
            =Set(varProcessando, true);
            Refresh(ficha_producao);
            With(
                {
                    _r: LookUp(ficha_producao, ID = gal_FilaTr3_1.Selected.ID),
                    _agora: Now()
                },
                With(
                    {_min: fx_MinutosDoDia(_agora)},
                    If(
                        _r.Modified <> gal_FilaTr3_1.Selected.Modified,
                        Notify("Este registro foi alterado por outro usuário. A fila foi recarregada.", NotificationType.Error, 8000);
                        Select(btn_RecarregarTr3_1);
                        Set(varProcessando, false),
                        _r.status_processo <> "Em processo",
                        Notify("Esta OP não está em processo. Atualize a fila.", NotificationType.Error, 8000);
                        Select(btn_RecarregarTr3_1);
                        Set(varProcessando, false),
                        !IsBlank(_r.InicioCimento_Trancagem),
                        Notify("O cimento desta OP já foi iniciado. Atualize a fila.", NotificationType.Warning, 6000);
                        Select(btn_RecarregarTr3_1);
                        Set(varProcessando, false),
                        Patch(
                            ficha_producao,
                            _r,
                            {InicioCimento_Trancagem: _agora}
                        );
                        If(
                            !IsEmpty(Errors(ficha_producao)),
                            Notify("Falha ao iniciar o cimento: " & First(Errors(ficha_producao)).Message, NotificationType.Error, 12000);
                            Set(varProcessando, false),
                            Patch(
                                Eventos_Producao,
                                Defaults(Eventos_Producao),
                                {
                                    Title: Text(_r.ID) & "-Trancagem-Cimento-Inicio",
                                    origem: {Value: "ficha_producao"},
                                    origem_ID: _r.ID,
                                    etapa: {Value: "Trançagem"},
                                    tipo: {Value: "Início"},
                                    data_hora: _agora,
                                    data_ref: fx_DataRefEm(_agora),
                                    turno: fx_Turno(_min),
                                    bitola: _r.Bitola,
                                    recurso: _r.Trançadeira,
                                    operador: Coalesce(cmb_OperadorTr3_1.Selected.Nome, _r.operador_trancagem, User().FullName)
                                }
                            );
                            If(
                                !IsEmpty(Errors(Eventos_Producao)),
                                Notify("Evento de início do cimento não gravou: " & First(Errors(Eventos_Producao)).Message, NotificationType.Error, 10000)
                            );
                            Select(btn_RecarregarTr3_1);
                            Set(varProcessando, false);
                            Notify("Cimento iniciado. Quando terminar, toque em Enviar p/ Cobertura.", NotificationType.Success, 6000)
                        )
                    )
                )
            )
          PressedFill: =ColorFade(Self.Fill, -30%)
          RadiusBottomLeft: =fx_RaioS
          RadiusBottomRight: =fx_RaioS
          RadiusTopLeft: =fx_RaioS
          RadiusTopRight: =fx_RaioS
          Size: =fx_FonteCorpo
          Text: ="Terminar trança → aplicar cimento"
          Visible: |-
            =gal_FilaTr3_1.Selected.Trançadeira = "TH05" &&
            IsBlank(gal_FilaTr3_1.Selected.Cimento_Maquina) &&
            fx_EstadoTranc(gal_FilaTr3_1.Selected.status_processo, gal_FilaTr3_1.Selected.InicioCimento_Trancagem) = "TRANÇANDO" &&
            fx_PrecisaCimento(gal_FilaTr3_1.Selected.Mangueira)
          Width: =236
          X: =556
          Y: =700
```

**`btn_EnviarCimentoTr3_1`**

```yaml
    - btn_EnviarCimentoTr3_1:
        Control: Classic/Button@2.2.0
        Properties:
          BorderColor: =Color.Transparent
          BorderThickness: =0
          Color: =fx_CorSuperficie
          DisabledFill: =fx_CorBorda
          DisplayMode: |-
            =If(
                IsBlank(gal_FilaTr3_1.Selected.ID) || varProcessando,
                DisplayMode.Disabled,
                DisplayMode.Edit
            )
          Fill: =fx_CorOK
          Font: =fx_FonteFamilia
          FontWeight: =FontWeight.Bold
          Height: =fx_AlturaAcao
          HoverFill: =ColorFade(fx_CorOK, -20%)
          OnSelect: |-
            =Set(varProcessando, true);
            Refresh(ficha_producao);
            With(
                {
                    _r: LookUp(ficha_producao, ID = gal_FilaTr3_1.Selected.ID),
                    _agora: Now()
                },
                With(
                    {_min: fx_MinutosDoDia(_agora)},
                    If(
                        _r.Modified <> gal_FilaTr3_1.Selected.Modified,
                        Notify("Este registro foi alterado por outro usuário. A fila foi recarregada.", NotificationType.Error, 8000);
                        Select(btn_RecarregarTr3_1);
                        Set(varProcessando, false),
                        _r.status_processo <> "Em processo",
                        Notify("Esta OP não está em processo. Atualize a fila.", NotificationType.Error, 8000);
                        Select(btn_RecarregarTr3_1);
                        Set(varProcessando, false),
                        IsBlank(_r.'Carretel Saida'),
                        Notify("Esta OP está sem carretel de saída. Corrija em Editar OP antes de enviar.", NotificationType.Warning, 8000);
                        Set(varProcessando, false),
                        Patch(
                            ficha_producao,
                            _r,
                            {
                                'Carretel Entrada': _r.'Carretel Saida',
                                'Carretel Saida': Blank(),
                                processo: "Cobertura",
                                status_processo: "Aguardando",
                                FimCimento_Trancagem: _agora,
                                InicioAguardandoCobertura: _agora
                            }
                        );
                        If(
                            !IsEmpty(Errors(ficha_producao)),
                            Notify("Falha ao gravar a ficha: " & First(Errors(ficha_producao)).Message, NotificationType.Error, 12000);
                            Set(varProcessando, false),
                            Reset(gal_FilaTr3_1);
                            Select(btn_RecarregarTr3_1);
                            Set(varProcessando, false);
                            Notify("Cimento concluído. Carretel enviado para a Cobertura.", NotificationType.Success, 6000)
                        )
                    )
                )
            )
          PressedFill: =ColorFade(fx_CorOK, -30%)
          RadiusBottomLeft: =fx_RaioS
          RadiusBottomRight: =fx_RaioS
          RadiusTopLeft: =fx_RaioS
          RadiusTopRight: =fx_RaioS
          Size: =fx_FonteDestaque
          Text: ="Enviar para Cobertura"
          Visible: |-
            =fx_EstadoContinuo(gal_FilaTr3_1.Selected.status_processo) = "PRODUZINDO" &&
            !IsBlank(gal_FilaTr3_1.Selected.Cimento_Maquina)
          Width: =290
          X: =810
          Y: =700
```


### 3.6 Modal de envio

**`lbl_TituloEnviarTr3_1` → `Text`**

```powerfx
If(
    gal_FilaTr3_1.Selected.Trançadeira <> "TH05" &&
    IsBlank(gal_FilaTr3_1.Selected.Cimento_Maquina) &&
    fx_PrecisaCimento(gal_FilaTr3_1.Selected.Mangueira),
    "Confirmar envio para cimento na TH05",
    "Confirmar envio para a Cobertura"
)
```

**`btn_ConfirmarEnviarTr3_1` → `OnSelect`**

```powerfx
Set(varProcessando, true);
Refresh(ficha_producao);
With(
    {
        _r: LookUp(ficha_producao, ID = gal_FilaTr3_1.Selected.ID),
        _agora: Now(),
        _q: Coalesce(Value(inp_QtdTr3_1.Text), 0),
        _ref: Coalesce(Value(inp_RefugoTr3_1.Text), 0),
        _sobra: Coalesce(Value(inp_SobraTr3_1.Text), 0)
    },
    With(
        {
            _min: fx_MinutosDoDia(_agora),
            _ja: Coalesce(_r.Qtd_Turno1, 0) + Coalesce(_r.Qtd_Turno2, 0) + Coalesce(_r.Qtd_Turno3, 0),
            _saida: _r.'Carretel Saida',
            _cim: _r.Trançadeira <> "TH05" && IsBlank(_r.Cimento_Maquina) && fx_PrecisaCimento(_r.Mangueira)
        },
        If(
            _r.Modified <> gal_FilaTr3_1.Selected.Modified,
            Notify("Este registro foi alterado por outro usuário. A fila foi recarregada.", NotificationType.Error, 8000);
            Select(btn_RecarregarTr3_1);
            Set(varProcessando, false),
            _r.status_processo <> "Em processo",
            Notify("Esta OP não está em processo. Atualize a fila.", NotificationType.Error, 8000);
            Select(btn_RecarregarTr3_1);
            Set(varProcessando, false),
            IsBlank(cmb_OperadorTr3_1.Selected.Nome) ||
            IsBlank(Trim(inp_LiTr3_1.Text)) ||
            IsBlank(Trim(inp_FioTr3_1.Text)) ||
            _q <= 0 ||
            Coalesce(Value(inp_PicksTr3_1.Text), 0) <= 0,
            Notify("Preencha LI, código do fio, quantidade, nº de picks e operador antes de enviar.", NotificationType.Warning, 6000);
            Set(varProcessando, false),
            Patch(
                ficha_producao,
                _r,
                {
                    quantidade_trancagem: _q,
                    defeito_trancagem: _ref,
                    'N°Picks': Coalesce(Value(inp_PicksTr3_1.Text), Blank()),
                    Diametro_Trançagem: fx_NumMedida(inp_DiametroTr3_1.Text),
                    Lote_Trançagem: Trim(inp_LiTr3_1.Text),
                    Cod_Trançagem: Trim(inp_FioTr3_1.Text),
                    operador_trancagem: cmb_OperadorTr3_1.Selected.Nome,
                    Observação_Trançagem: inp_ObsTr3_1.Text,
                    'Carretel Entrada': If(_cim, _r.'Carretel Entrada', _saida),
                    'Carretel Saida': If(_cim, _r.'Carretel Saida', Blank()),
                    processo: If(_cim, "Trançadeira", "Cobertura"),
                    status_processo: "Aguardando",
                    Cimento_Maquina: If(_cim, "TH05", _r.Cimento_Maquina),
                    InicioAguardando_Trançadeira: If(_cim, _agora, _r.InicioAguardando_Trançadeira),
                    data_hora_final_trancadeira: _agora,
                    InicioAguardandoCobertura: If(_cim, _r.InicioAguardandoCobertura, _agora),
                    FimCimento_Trancagem: If(!_cim && !IsBlank(_r.InicioCimento_Trancagem), _agora, _r.FimCimento_Trancagem),
                    Qtd_Turno1: If(fx_Turno(_min) = 1, Coalesce(_r.Qtd_Turno1, 0) + (_q - _ja), _r.Qtd_Turno1),
                    Qtd_Turno2: If(fx_Turno(_min) = 2, Coalesce(_r.Qtd_Turno2, 0) + (_q - _ja), _r.Qtd_Turno2),
                    Qtd_Turno3: If(fx_Turno(_min) = 3, Coalesce(_r.Qtd_Turno3, 0) + (_q - _ja), _r.Qtd_Turno3),
                    Turno_Trançagem: Text(fx_Turno(_min))
                }
            );
            If(
                !IsEmpty(Errors(ficha_producao)),
                Notify("Falha ao gravar a ficha: " & First(Errors(ficha_producao)).Message, NotificationType.Error, 12000);
                Set(varProcessando, false),
                Patch(
                    Historico_Carretel,
                    Coalesce(
                        LookUp(
                            Historico_Carretel As _h,
                            _h.etapa = "Trançagem" && _h.Title = _saida && _h.OP_ID = _r.OP
                        ),
                        Defaults(Historico_Carretel)
                    ),
                    {
                        Title: _saida,
                        OP_ID: _r.OP,
                        etapa: "Trançagem",
                        mangueira: Text(_r.Bitola),
                        metros_entrada: Coalesce(_r.quantidade_tubo, 0),
                        metros_saida: _q,
                        data_hora_entrada: Coalesce(_r.data_hora_inicio_trancadeira, _agora),
                        data_hora_saida: _agora,
                        operador: cmb_OperadorTr3_1.Selected.Nome
                    }
                );
                If(
                    !IsEmpty(Errors(Historico_Carretel)),
                    Notify("Ficha enviada, mas o histórico do carretel NÃO gravou: " & First(Errors(Historico_Carretel)).Message, NotificationType.Error, 10000)
                );
                Patch(
                    Eventos_Producao,
                    Defaults(Eventos_Producao),
                    {
                        Title: Text(_r.ID) & "-Trancagem-Fim",
                        origem: {Value: "ficha_producao"},
                        origem_ID: _r.ID,
                        etapa: {Value: "Trançagem"},
                        tipo: {Value: "Fim"},
                        data_hora: _agora,
                        data_ref: fx_DataRefEm(_agora),
                        turno: fx_Turno(_min),
                        bitola: _r.Bitola,
                        metros: _q,
                        refugo: _ref,
                        recurso: _r.Trançadeira,
                        operador: cmb_OperadorTr3_1.Selected.Nome
                    }
                );
                If(
                    !IsEmpty(Errors(Eventos_Producao)),
                    Notify("Evento de fim não gravou: " & First(Errors(Eventos_Producao)).Message, NotificationType.Error, 10000)
                );
                If(
                    !IsBlank(_r.'Carretel Entrada'),
                    Patch(
                        lista_carreteis,
                        LookUp(lista_carreteis, Title = _r.'Carretel Entrada'),
                        {
                            op: Blank(),
                            etapa_processo: Blank(),
                            lote: Blank(),
                            metros_restantes: If(ctxUsouTudoTr3, 0, _sobra),
                            mangueira_atual: If(ctxUsouTudoTr3, Blank(), _r.Bitola)
                        }
                    )
                );
                Reset(inp_SobraTr3_1);
                UpdateContext({
                    ctxModalEnviarTr3: false,
                    ctxUsouTudoTr3: true,
                    ctxLiSugTr3: "",
                    ctxFioSugTr3: ""
                });
                Select(btn_RecarregarTr3_1);
                Reset(gal_FilaTr3_1);
                Set(varProcessando, false);
                Notify(
                    If(
                        _cim,
                        "Apontamento registrado. A mangueira segue no carretel " & Coalesce(_saida, "—") & " para o cimento na TH05.",
                        "Apontamento registrado. Carretel enviado para a Cobertura."
                    ),
                    NotificationType.Success,
                    6000
                )
            )
        )
    )
)
```


### 3.7 Recarregar e versão

**`btn_RecarregarTr3_1` → `OnSelect`** (só muda uma linha, a do `ClearCollect(colHHPendTr3…)`: `_f.Trançadeira = _cc.Celula && IsBlank(_f.Cimento_Maquina) && _f.status_processo = "Em processo"`; o resto é igual ao de hoje)

```powerfx
Refresh(ficha_producao);
Refresh(lista_carreteis);
Refresh(FifoBobinadeira);
ClearCollect(colCarreteisTr3, lista_carreteis);
ClearCollect(
    colFilaBaseTr3,
    Filter(ficha_producao, processo = "Trançadeira")
);
With(
    {_a: Now()},
    With(
        {_ini: fx_JanelaInicioEm(_a), _fim: fx_JanelaFimEm(_a)},
        ClearCollect(
            colTrancDiaTr3,
            Filter(
                ficha_producao,
                data_hora_final_trancadeira >= _ini,
                data_hora_final_trancadeira < _fim
            )
        )
    );
    With(
        {_t: fx_TurnoEm(_a), _tl: fx_TurnoLabelEm(_a), _d: fx_DataRefEm(_a)},
        ClearCollect(
            colHHTr3,
            Filter('Hora-Hora', Data = _d, Turno = _tl)
        );
        ClearCollect(
            colHHPendTr3,
            ForAll(
                fx_CelulasTrancagem As _cc,
                With(
                    {
                        _lin: Filter(colHHTr3 As _h, _h.Célula = _cc.Celula)
                    },
                    With(
                        {
                            _ativa:
                                CountRows(
                                    Filter(
                                        _lin As _h0,
                                        Coalesce(_h0.'Real. Hora', 0) > 0 || !IsBlank(_h0.Mangueira)
                                    )
                                ) > 0 ||
                                CountRows(
                                    Filter(
                                        colFilaBaseTr3 As _f,
                                        ((_f.Trançadeira = _cc.Celula && IsBlank(_f.Cimento_Maquina)) || _f.Cimento_Maquina = _cc.Celula) && _f.status_processo = "Em processo"
                                    )
                                ) > 0
                        },
                        With(
                            {
                                _diag: ForAll(
                                    Filter(fx_GradeHoraHora, Turno = _t) As _g,
                                    With(
                                        {
                                            _r: First(
                                                Sort(
                                                    Filter(_lin As _h2, _h2.Hora = _g.Hora),
                                                    ID,
                                                    SortOrder.Descending
                                                )
                                            )
                                        },
                                        {
                                            P: fx_PendenciaMaqHH(
                                                _ativa,
                                                fx_FaixaVencida(_g.Fim, _t, _a),
                                                Coalesce(Text(_r.Mangueira), ""),
                                                Coalesce(_r.'Meta Hora', 0),
                                                Coalesce(_r.'Real. Hora', 0),
                                                Coalesce(Text(_r.Motivo), "")
                                            )
                                        }
                                    )
                                )
                            },
                            {
                                Celula: _cc.Celula,
                                Ativa: _ativa,
                                SemApontar: CountRows(Filter(_diag As _d1, _d1.P = "SEM_APONTAMENTO")),
                                SemMotivo: CountRows(Filter(_diag As _d2, _d2.P = "SEM_MOTIVO"))
                            }
                        )
                    )
                )
            )
        )
    )
);
UpdateContext({ctxAgora: Now()})
```

**`lbl_VersaoTelaTr3_1` → `Text`**

```powerfx
"Versão 0.4.0"
```


## 4. scr_PainelCelula_1 — propriedades alteradas

Mudança mínima: o posto da trançadeira ganha o estado `CIMENTO` (cor gelo, cronômetro desde `InicioCimento_Trancagem`) e uma OP com `Cimento_Maquina = X` conta no posto X (e sai do posto que trançou). A fórmula de `colPostosTrancPnl` está no `OnSelect` do controle abaixo; as linhas novas estão marcadas pelos comentários "Cimento" e pelas variáveis `_cim` e `_so`.

**`btn_RecarregarPnl` → `OnSelect`** (propriedade inteira, pronta para colar; muda só o bloco `colPostosTrancPnl`)

```powerfx
Set(varFalhaPnl, false);
Set(varTruncaPnl, false);
// v0.11.0 · UM instante por ciclo: toda a carga (turno, janela, data de referencia, consumo,
// andon) usa varAgoraPnl. Antes eram ~25 leituras de Now() misturadas com ctxAgoraPnl.
Set(varAgoraPnl, Now());
// v0.11.0 (item 5 · M11): os Refresh rodam em PARALELO, e nao mais 3 em serie. Cada um fecha
// o IfError com "true" / "false" (licao 2.23: valor e fallback do mesmo tipo).
// v0.11.1: cada ramo do Concurrent grava a SUA flag (varR1..R3Pnl); varFalhaPnl so e escrita
// FORA do Concurrent (o Studio nao aceita a mesma variavel escrita em varios ramos paralelos).
Set(varR1Pnl, false);
Set(varR2Pnl, false);
Set(varR3Pnl, false);
Concurrent(
    IfError(Refresh(ficha_producao); true, Set(varR1Pnl, true); false),
    IfError(Refresh(Eventos_Producao); true, Set(varR2Pnl, true); false),
    IfError(Refresh('Hora-Hora'); true, Set(varR3Pnl, true); false)
);
If(varR1Pnl || varR2Pnl || varR3Pnl, Set(varFalhaPnl, true));
If(
    IsBlank(varVelDiaPnl) || varVelDiaPnl <> fx_DataRefEm(varAgoraPnl),
    IfError(Refresh(DM_TRANÇAGEM); Refresh(DM_ENGRENAGENS); Refresh(DESVIO); true, Set(varFalhaPnl, true); false)
);
// v0.10.0 · AUTONOMIA DE TUBO (C10 · C23). Velocidade pelo MESMO caminho do Hora-Hora v0.5.9:
// mangueira -> DM_TRANCAGEM._2BRD_CODE -> DM_ENGRENAGENS (maquina + construcao) -> _13TEORICA_M_H.
// Cadastro carregado 1x por dia (ou ao abrir a tela) numa colecao local: o calculo por maquina
// abaixo nao faz NENHUMA chamada de rede. Nunca chamar fx_VelocidadeTeorica aqui: e LookUp no
// SharePoint por linha (11 maquinas x a cada 2 min).
// Ordem externa = DM_TRANCAGEM, igual ao colMangMaqHHT: mangueira com duas construcoes na mesma
// maquina pega a MESMA velocidade que o Hora-Hora pega.
// v0.11.0: (item 5) a chave da DM_TRANCAGEM e normalizada UMA vez por linha, antes do laco, e nao
// a cada linha da DM_ENGRENAGENS; (item 2) o cadastro so e TROCADO se a leitura nova vier cheia
// (antes um ClearCollect com leitura vazia apagava as velocidades) e a leitura grande demais
// acende o aviso de truncamento.
If(
    IsBlank(varVelDiaPnl) || varVelDiaPnl <> fx_DataRefEm(varAgoraPnl),
    IfError(
        With(
            {
                _eng: ForAll(
                    DM_ENGRENAGENS As _e,
                    {
                        MaqN: fx_NormCodigo(_e._4MAQUINA),
                        ConsN: fx_NormCodigo(_e._1CONSTRUCAO),
                        MFG: fx_NumVelocidade(Text(_e._13TEORICA_M_H))
                    }
                ),
                _trc: ForAll(
                    DM_TRANÇAGEM As _d0,
                    {
                        Chave: fx_MangCanon(_d0.PARTNUMBER),
                        ConsN: fx_NormCodigo(_d0._2BRD_CODE)
                    }
                ),
                // [DESVIO] só as linhas do desvio que estão valendo hoje (Inicio..Fim).
                _dsv: ForAll(
                    Filter(
                        DESVIO,
                        fx_DesvioAtivo(Desvio, Inicio, Fim, fx_DataRefEm(varAgoraPnl))
                    ) As _x,
                    {
                        MaqN: fx_NormCodigo(_x._4MAQUINA),
                        ConsN: fx_NormCodigo(_x._1CONSTRUCAO),
                        MFG: fx_NumVelocidade(Text(_x._13TEORICA_M_H))
                    }
                )
            },
            With(
                {
                    // Desvio ativo SUBSTITUI a linha normal da mesma máquina+construção.
                    _engOk: Ungroup(
                        Table(
                            {
                                L: Filter(
                                    _eng As _a,
                                    CountRows(Filter(_dsv As _b, _b.MaqN = _a.MaqN && _b.ConsN = _a.ConsN)) = 0
                                )
                            },
                            { L: _dsv }
                        ),
                        L
                    )
                },
            With(
                {
                    _novo: Filter(
                        Ungroup(
                            ForAll(
                                Filter(_trc As _t1, !IsBlank(_t1.Chave) && !IsBlank(_t1.ConsN)) As _d,
                                {
                                    Linhas: ForAll(
                                        Filter(_engOk As _e2, _e2.ConsN = _d.ConsN) As _e3,
                                        {
                                            MaqN: _e3.MaqN,
                                            Chave: _d.Chave,
                                            MFG: _e3.MFG
                                        }
                                    )
                                }
                            ),
                            Linhas
                        ),
                        MFG > 0
                    )
                },
                // Leitura vazia (rede caiu): mantem o cadastro anterior, NAO marca o dia e o proximo
                // ciclo de 2 min tenta de novo.
                If(
                    IsEmpty(_novo),
                    Set(varFalhaPnl, true),
                    ClearCollect(colVelTrPnl, _novo);
                    Set(varVelDiaPnl, fx_DataRefEm(varAgoraPnl))
                );
                If(
                    CountRows(_eng) >= fx_PainelLinhasAlerta || CountRows(_trc) >= fx_PainelLinhasAlerta,
                    Set(varTruncaPnl, true)
                );
                true
            )
            )
        ),
        Set(varFalhaPnl, true); false
    )
);
Set(varC1Pnl, false);
Set(varC2Pnl, false);
Set(varC3Pnl, false);
Set(varC4Pnl, false);
Set(varC5Pnl, false);
Set(varC6Pnl, false);
Set(varC7Pnl, false);
With(
    {
        _hoje: fx_DataRefEm(varAgoraPnl),
        _iniIns: fx_PeriodoIniEm(fx_DataRefEm(varAgoraPnl), "DIA", 1),
        _fimIns: fx_PeriodoFimEm(fx_DataRefEm(varAgoraPnl), "DIA", 1)
    },
    // v0.11.0 (item 2 · A3): cada ClearCollect do Concurrent fecha o IfError com "true" / "false".
    // Antes so os Refresh estavam protegidos: carga que falhava deixava varSincPnl avancar e o
    // andon dizia "celula em dia" sem dado.
    Concurrent(
        // v0.10.1: Hora-Hora de ONTEM e de HOJE, uma consulta por dia, em paralelo. Um dia cheio
        // chega a ~300 linhas; dois dias numa consulta so passariam do limite de linhas e a
        // lista viria CORTADA sem aviso. O turno atual (colHHPnl) sai daqui, local, logo abaixo.
        IfError(
            ClearCollect(
                colHHOntemPnl,
                Filter(
                    'Hora-Hora',
                    Data = DateAdd(_hoje, -1, TimeUnit.Days)
                )
            );
            true,
            Set(varC1Pnl, true); false
        ),
        IfError(
            ClearCollect(
                colHHHojePnl,
                Filter(
                    'Hora-Hora',
                    Data = _hoje
                )
            );
            true,
            Set(varC2Pnl, true); false
        ),
        IfError(
            ClearCollect(
                colAtivasPnl,
                Filter(ficha_producao, status_processo = "Em processo")
            );
            true,
            Set(varC3Pnl, true); false
        ),
        IfError(
            ClearCollect(
                colAguardPnl,
                Filter(ficha_producao, status_processo = "Aguardando")
            );
            true,
            Set(varC4Pnl, true); false
        ),
        // v0.11.0 (item 5 · M11): Eventos numa consulta SO (antes 3, com a mesma data). Os tres
        // recortes por etapa (Vulcanizacao, Mandril, Extracao) saem daqui, locais, logo abaixo.
        IfError(
            ClearCollect(
                colEvDiaPnl,
                AddColumns(
                    Filter(
                        Eventos_Producao,
                        data_ref = _hoje
                    ),
                    EtapaTxt,
                    Text(etapa.Value),
                    TipoTxt,
                    Text(tipo.Value),
                    TurnoTxt,
                    Text(turno)
                )
            );
            true,
            Set(varC5Pnl, true); false
        ),
        // v0.11.0 (item 5 · M11): FifoBobinadeira numa consulta so (EP + AB), DENTRO do Concurrent.
        // Falhou = "sem fonte" de verdade (antes varBobSemFontePnl era sempre false).
        IfError(
            ClearCollect(
                colBobFifoPnl,
                Filter(FifoBobinadeira, Status = "EP" || Status = "AB")
            );
            Set(varBobSemFontePnl, false);
            true,
            Set(varBobSemFontePnl, true);
            Set(varC6Pnl, true);
            false
        ),
        // v0.15.0 (MEL-261): saida da Extracao = lances inspecionados do dia, a mesma conta da tela da Cabine.
        IfError(
            ClearCollect(
                colInspDiaPnl,
                AddColumns(
                    Filter(
                        RegistrosInspeção,
                        Created >= _iniIns,
                        Created < _fimIns
                    ),
                    TurnoTxt,
                    Text(TurnoTeste),
                    metros,
                    Quantidade
                )
            );
            true,
            Set(varC7Pnl, true); false
        )
    )
);
If(varC1Pnl || varC2Pnl || varC3Pnl || varC4Pnl || varC5Pnl || varC6Pnl || varC7Pnl, Set(varFalhaPnl, true));
ClearCollect(colEvVulcPnl, Filter(colEvDiaPnl, EtapaTxt = "Vulcanização"));
ClearCollect(colEvMandPnl, Filter(colEvDiaPnl, EtapaTxt = "Mandril"));
ClearCollect(colEvSaidaPnl, Filter(colEvDiaPnl, EtapaTxt = "Extração"));
// v0.13.0: a agregacao da metragem por turno (colProdEtapaTurnoPnl) e a saida da Extracao (varSaida*) foram
// para o botao oculto btn_AgregaPnl (chamado no fim deste ciclo e a cada escolha do seletor), que le a
// fonte do modo: colEvDiaPnl (AO VIVO) ou colEvHistPnl (dia escolhido). Uma formula so.
// v0.11.0 (item 2 · M12): guarda de truncamento. Lista lida com fx_PainelLinhasAlerta linhas ou
// mais = suspeita de corte no limite do conector: a carga deixa de contar como "ok".
If(
    CountRows(colHHOntemPnl) >= fx_PainelLinhasAlerta ||
    CountRows(colHHHojePnl) >= fx_PainelLinhasAlerta ||
    CountRows(colAtivasPnl) >= fx_PainelLinhasAlerta ||
    CountRows(colAguardPnl) >= fx_PainelLinhasAlerta ||
    CountRows(colEvDiaPnl) >= fx_PainelLinhasAlerta ||
    CountRows(colInspDiaPnl) >= fx_PainelLinhasAlerta,
    Set(varTruncaPnl, true)
);
ClearCollect(colHH2dPnl, colHHOntemPnl, colHHHojePnl);
ClearCollect(
    colHHPnl,
    Filter(
        colHH2dPnl As _z,
        _z.Data = fx_DataRefEm(varAgoraPnl) && _z.Turno = fx_TurnoLabelEm(varAgoraPnl)
    )
);
// v0.10.1 · CONSUMO DO CARRETEL PELO HORA-HORA (C13 · C10).
// Uma linha por janela de trancadeira: a ULTIMA salva (maior ID) quando a lista tem registro
// duplicado. So fica a janela APONTADA: metro, parada ou motivo. Linha salva vazia (o botao
// repetir pre-preenche a mangueira) nao e apontamento.
ClearCollect(
    colHHConsPnl,
    Filter(
        ForAll(
            GroupBy(
                AddColumns(
                    Filter(colHH2dPnl As _x, Text(_x.Célula) in fx_CelulasTrancagem.Celula),
                    ChaveJan,
                    Text(Célula) & "|" & Text(Data, "yyyy-mm-dd") & "|" & Text(Turno) & "|" & Hora
                ),
                ChaveJan,
                LinhasJan
            ) As _gj,
            With(
                { _r: First(Sort(_gj.LinhasJan, ID, SortOrder.Descending)) },
                {
                    Celula: Text(_r.Célula),
                    DataRef: _r.Data,
                    Turno: fx_TurnoNum(Text(_r.Turno)),
                    Hora: _r.Hora,
                    Real: Coalesce(_r.'Real. Hora', 0),
                    Apontada: Coalesce(_r.'Real. Hora', 0) > 0 ||
                        Coalesce(_r.'Tempo Parado (min)', 0) > 0 ||
                        !IsBlank(Text(_r.Motivo))
                }
            )
        ),
        Apontada
    )
);
// Turnos que tiveram QUALQUER linha no Hora-Hora (criterio ANTIGO da v0.10.3, inclui linha pre-preenchida):
// so o CONSUMO de tubo usa esta colecao (colJanTrPnl.Trabalhado), para a autonomia ficar igual a v0.10.3.
ClearCollect(
    colTurnosHHConsPnl,
    Distinct(
        ForAll(
            colHH2dPnl As _y0,
            { K: Text(_y0.Data, "yyyy-mm-dd") & "|" & Text(fx_TurnoNum(Text(_y0.Turno)), "[$-en-US]0") }
        ),
        K
    )
);
// Turnos TRABALHADOS para o ANDON: tiveram janela APONTADA (metro, parada ou motivo) numa trancadeira.
// Turno sem apontamento nenhum = a fabrica nao rodou (3o turno de 29/09): calam as regras de FILA.
// v0.11.0 (item 3 · M5). NAO e usada no consumo de tubo (ali vale colTurnosHHConsPnl, acima).
ClearCollect(
    colTurnosHHPnl,
    Distinct(
        ForAll(
            colHHConsPnl As _y,
            { K: Text(_y.DataRef, "yyyy-mm-dd") & "|" & Text(_y.Turno, "[$-en-US]0") }
        ),
        K
    )
);
// Grade de janelas de ONTEM e HOJE, com instante de abertura e fechamento. O turno de agora
// conta sempre como trabalhado (as 05:25 ainda ninguem apontou, mas a fabrica esta rodando).
With(
    {
        _dh: fx_DataRefEm(varAgoraPnl),
        _ta: fx_TurnoEm(varAgoraPnl)
    },
    ClearCollect(
        colJanTrPnl,
        ForAll(
            fx_GradeHoraHora As _g1,
            With(
                { _dr1: DateAdd(_dh, -1, TimeUnit.Days) },
                {
                    DataRef: _dr1,
                    Turno: _g1.Turno,
                    Hora: _g1.Hora,
                    Minutos: _g1.Minutos,
                    Ini: fx_JanelaHHIni(_dr1, _g1.Turno, _g1.Fim, _g1.Minutos),
                    Fim: fx_JanelaHHFim(_dr1, _g1.Turno, _g1.Fim),
                    Trabalhado: (Text(_dr1, "yyyy-mm-dd") & "|" & Text(_g1.Turno, "[$-en-US]0")) in colTurnosHHConsPnl.Value
                }
            )
        )
    );
    Collect(
        colJanTrPnl,
        ForAll(
            fx_GradeHoraHora As _g2,
            {
                DataRef: _dh,
                Turno: _g2.Turno,
                Hora: _g2.Hora,
                Minutos: _g2.Minutos,
                Ini: fx_JanelaHHIni(_dh, _g2.Turno, _g2.Fim, _g2.Minutos),
                Fim: fx_JanelaHHFim(_dh, _g2.Turno, _g2.Fim),
                Trabalhado: _g2.Turno = _ta ||
                    (Text(_dh, "yyyy-mm-dd") & "|" & Text(_g2.Turno, "[$-en-US]0")) in colTurnosHHConsPnl.Value
            }
        )
    )
);
// v0.11.0 · JANELA ATUAL PELA GRADE OFICIAL (A1, M3, M4). Antes a janela "atual" era achada lendo o
// TEXTO da chave ("22:00 - 22:20"), que na v3.0.5 durou ate 22:41 (revertido na v3.0.15, 22:20): das 22:20 as 22:40 nenhuma
// janela era "atual" e a trancadeira parada sumia. Agora Ini/Fim vem de fx_GradeHoraHora +
// fx_JanelaHHIni/Fim (mesma regua do Hora-Hora), o instante e o do ciclo (varAgoraPnl) e a janela
// duplicada na lista fica so com a de MAIOR ID (igual ao colHHConsPnl).
With(
    { _dh: fx_DataRefEm(varAgoraPnl) },
    ClearCollect(
        colHHJanPnl,
        ForAll(
            GroupBy(
                AddColumns(colHHPnl, ChaveJan, Text(Célula) & "|" & Hora),
                ChaveJan,
                LinhasJan
            ) As _gj,
            With(
                {
                    _h: First(Sort(_gj.LinhasJan, ID, SortOrder.Descending))
                },
                With(
                    {
                        _gr: LookUp(
                            fx_GradeHoraHora As _gr0,
                            _gr0.Hora = _h.Hora && _gr0.Turno = fx_TurnoNum(Text(_h.Turno))
                        )
                    },
                    With(
                        {
                            _ini: fx_JanelaHHIni(_dh, _gr.Turno, _gr.Fim, _gr.Minutos),
                            _fim: fx_JanelaHHFim(_dh, _gr.Turno, _gr.Fim)
                        },
                        {
                            Celula: Text(_h.Célula),
                            Ini: _ini,
                            Fim: _fim,
                            Atual: !IsBlank(_gr.Fim) && varAgoraPnl >= _ini && varAgoraPnl < _fim,
                            Motivo: Coalesce(Text(_h.Motivo), ""),
                            // v0.11.0 (item 4 · M2): motivo com Tipo "Programada" na fx_MotivosParada
                            // (Refeicao, Reuniao, Set-up, Preventiva, Check List, Amostra, MPT, Teste
                            // Engenharia) e PAUSA, nao parada real.
                            Prog: !IsBlank(Trim(Text(_h.Motivo))) &&
                                LookUp(fx_MotivosParada As _mp, Trim(_mp.Motivo) = Trim(Text(_h.Motivo))).Tipo = "Programada",
                            Parado: Coalesce(_h.'Tempo Parado (min)', 0),
                            // v0.9.0: meta e real da janela para a ficha de consulta.
                            // Janela fechada = o instante do ciclo passou do fim da janela da grade.
                            Meta: Coalesce(_h.'Meta Hora', 0),
                            Real: Coalesce(_h.'Real. Hora', 0),
                            Fechada: !IsBlank(_gr.Fim) && varAgoraPnl >= _fim
                        }
                    )
                )
            )
        )
    )
);
ClearCollect(
    colPostosTrancPnl,
    ForAll(
        Filter(fx_LayoutBalizas, tranc) As _b,
        With(
            {
                // Cimento (13/11): OP trançada em outra máquina e só passando cimento na TH05
                // (Cimento_Maquina = X) conta no posto X, não no posto que trançou.
                _f: LookUp(
                    colAtivasPnl As _a,
                    _a.processo = "Trançadeira" &&
                    ((_a.Trançadeira = _b.Trançadeira && IsBlank(_a.Cimento_Maquina)) || _a.Cimento_Maquina = _b.Trançadeira)
                ),
                // v0.8.1: fila POR CARRETEL, nao por OP. Um carretel de tubo pode
                // levar 2 OPs; contar OP mostrava "tubo atras" quando a 2a OP estava
                // no MESMO carretel que ja roda na maquina. Agrupa pelo 'Carretel
                // Entrada', tira o carretel montado (o da OP Em processo) e cada
                // grupo vira uma bolinha com a soma dos metros. OP sem carretel
                // apontado vira carretel proprio (ID-n): nunca some da fila.
                _fila: With(
                    {
                        _carMaq: Coalesce(
                            Upper(
                                Trim(
                                    LookUp(
                                        colAtivasPnl As _a0,
                                        _a0.processo = "Trançadeira" &&
                                        ((_a0.Trançadeira = _b.Trançadeira && IsBlank(_a0.Cimento_Maquina)) || _a0.Cimento_Maquina = _b.Trançadeira)
                                    ).'Carretel Entrada'
                                )
                            ),
                            ""
                        )
                    },
                    Sort(
                        AddColumns(
                            GroupBy(
                                Filter(
                                    AddColumns(
                                        Filter(
                                            colAguardPnl As _g,
                                            _g.processo = "Trançadeira" &&
                                            ((_g.Trançadeira = _b.Trançadeira && IsBlank(_g.Cimento_Maquina)) || _g.Cimento_Maquina = _b.Trançadeira)
                                        ),
                                        CarKey,
                                        Coalesce(
                                            Upper(Trim('Carretel Entrada')),
                                            "ID-" & Text(ID, "[$-en-US]0")
                                        )
                                    ) As _o,
                                    _o.CarKey <> _carMaq
                                ),
                                CarKey,
                                OpsCar
                            ),
                            QtdAnterior,
                            Sum(OpsCar, quantidade_tubo),
                            PrimID,
                            Min(OpsCar, ID),
                            NOps,
                            CountRows(OpsCar)
                        ),
                        PrimID,
                        SortOrder.Ascending
                    )
                )
            },
            With(
                {
                    _n: CountRows(_fila),
                    _ult: LookUp(
                        colHHJanPnl As _j,
                        _j.Celula = _b.Trançadeira && _j.Atual
                    ),
                    // v0.11.0 (item 4): "parado no turno" soma so parada REAL; a pausa programada
                    // (Refeicao, Reuniao...) tem soma propria e nunca entra na parada.
                    _parMin: Sum(
                        Filter(colHHJanPnl As _j2, _j2.Celula = _b.Trançadeira && !_j2.Prog),
                        Parado
                    ),
                    _pauMin: Sum(
                        Filter(colHHJanPnl As _j3, _j3.Celula = _b.Trançadeira && _j3.Prog),
                        Parado
                    ),
                    _maqN: fx_NormCodigo(fx_MaquinaEngrenagens(_b.Trançadeira)),
                    // Cimento: _cim = passando cimento agora (InicioCimento preenchido, FimCimento vazio);
                    // _so = OP so-cimento (trancada em outra maquina): nao consome tubo aqui.
                    _cim: !IsBlank(_f.InicioCimento_Trancagem) && IsBlank(_f.FimCimento_Trancagem),
                    _so: !IsBlank(_f.Cimento_Maquina)
                },
                With(
                {
                    // v0.11.0 (item 4 · M1 · M2 · decisao 1 de 22/10): parada apontada no Hora-Hora
                    // na janela de agora vira PARADA mesmo com OP aberta; motivo Programado vira PAUSA.
                    _est: If(
                        !IsBlank(_ult.Motivo) && _ult.Prog,
                        "PAUSA",
                        !IsBlank(_ult.Motivo),
                        "PARADA",
                        _cim,
                        "CIMENTO",
                        fx_EstadoPosto(!IsBlank(_f.ID), _n)
                    ),
                    // v0.10.0: velocidade da mangueira que esta NA MAQUINA (m/h).
                    // Mesmo envelope do Hora-Hora: sem delineamento, cai no fallback da Spiral.
                    _vAtiva: If(
                        IsBlank(_f.ID),
                        0,
                        Coalesce(
                            LookUp(
                                colVelTrPnl As _v1,
                                _v1.MaqN = _maqN &&
                                _v1.Chave = fx_MangCanon(Text(_f.Mangueira))
                            ).MFG,
                            fx_VelocidadeFallbackSpiral(Text(_f.Mangueira))
                        )
                    ),
                    // v0.10.1: janelas APONTADAS desta maquina (ontem e hoje).
                    _hhMaq: Filter(colHHConsPnl As _hc, _hc.Celula = _b.Trançadeira)
                },
                With(
                {
                    // v0.10.1 · METROS JA CONSUMIDOS do carretel montado, do Inicio da OP ate agora,
                    // janela por janela da grade:
                    //   janela aberta agora ............ velocidade x minutos decorridos
                    //   janela fechada APONTADA ........ o Real apontado (rateado se a OP comecou no meio)
                    //   fechada SEM apontamento, turno
                    //   trabalhado ..................... velocidade x minutos (nao apontou = conta como rodou)
                    //   turno sem linha nenhuma ........ 0 (a fabrica nao rodou)
                    // Antes de ontem 05:20 o Hora-Hora nao foi carregado: ali vale velocidade x relogio.
                    _consM: If(
                        IsBlank(_f.ID) || _so || _vAtiva <= 0 || IsBlank(_f.data_hora_inicio_trancadeira),
                        0,
                        With(
                            {
                                _I: _f.data_hora_inicio_trancadeira,
                                _N: varAgoraPnl,
                                _C: DateAdd(fx_JanelaInicioEm(varAgoraPnl), -1, TimeUnit.Days)
                            },
                            If(_I < _C, _vAtiva * DateDiff(_I, _C, TimeUnit.Minutes) / 60, 0) +
                            Sum(
                                ForAll(
                                    Filter(colJanTrPnl As _w, _w.Fim > _I && _w.Ini < _N) As _w2,
                                    With(
                                        {
                                            _ov: fx_OverlapMin(_w2.Ini, _w2.Fim, _I, _N),
                                            _r: LookUp(
                                                _hhMaq As _hm,
                                                _hm.DataRef = _w2.DataRef && _hm.Turno = _w2.Turno && _hm.Hora = _w2.Hora
                                            )
                                        },
                                        {
                                            M: If(
                                                _w2.Fim > _N,      _vAtiva * _ov / 60,
                                                !IsBlank(_r.Hora), fx_RateioCob(_r.Real, _ov, _w2.Minutos),
                                                _w2.Trabalhado,    _vAtiva * _ov / 60,
                                                0
                                            )
                                        }
                                    )
                                ),
                                M
                            )
                        )
                    ),
                    // Minutos de TODA OP Aguardando desta maquina: a fila por carretel E as OPs que
                    // dividem o carretel montado (saem da fila desde a v0.8.1, mas sao tubo na
                    // maquina). Cada OP na velocidade da propria mangueira; sem velocidade cadastrada,
                    // usa a da mangueira montada.
                    _minFila: Sum(
                        ForAll(
                            Filter(
                                colAguardPnl As _g7,
                                _g7.processo = "Trançadeira" &&
                                // OP so-cimento nao entra na autonomia: nao e tubo a trancar nesta maquina.
                                _g7.Trançadeira = _b.Trançadeira && IsBlank(_g7.Cimento_Maquina)
                            ) As _o7,
                            With(
                                {
                                    _v7: Coalesce(
                                        LookUp(
                                            colVelTrPnl As _v2,
                                            _v2.MaqN = _maqN && _v2.Chave = fx_MangCanon(Text(_o7.Mangueira))
                                        ).MFG,
                                        fx_VelocidadeFallbackSpiral(Text(_o7.Mangueira))
                                    )
                                },
                                With(
                                    { _v8: If(_v7 > 0, _v7, _vAtiva) },
                                    { M: If(_v8 > 0, Coalesce(_o7.quantidade_tubo, 0) * 60 / _v8, 0) }
                                )
                            )
                        ),
                        M
                    )
                },
                With(
                {
                    _restM: If(
                        IsBlank(_f.ID) || _so,
                        0,
                        Max(0, Coalesce(_f.quantidade_tubo, 0) - _consM)
                    )
                },
                {
                    Posto: _b.Trançadeira,
                    Rotulo: _b.nome,
                    OP: Coalesce(_f.OP, 0),
                    Mangueira: Coalesce(Text(_f.Mangueira), ""),
                    Inicio: _f.data_hora_inicio_trancadeira,
                    InicioCimento: If(_cim, _f.InicioCimento_Trancagem, Blank()),
                    Produzindo: !IsBlank(_f.ID),
                    Estado: _est,
                    Cor: If(_est = "PARADA", fx_CorErro, fx_CorEstadoPosto(_est)),
                    Motivo: If(_est = "PARADA" || _est = "PAUSA", _ult.Motivo, ""),
                    ParadoMin: _parMin,
                    PausaMin: _pauMin,
                    // Inicio da janela parada pela grade oficial (v0.11.0): 13:57 e 22:20 nas fronteiras de turno.
                    InicioParada: If(_est = "PARADA" || _est = "PAUSA", _ult.Ini, Blank()),
                    // Fila = CARRETEIS atras. OpsFila so alimenta o detalhe do andon.
                    Fila: _n,
                    OpsFila: Sum(_fila, NOps),
                    Q1: If(_n >= 1, Last(FirstN(_fila, 1)).QtdAnterior, Blank()),
                    Q2: If(_n >= 2, Last(FirstN(_fila, 2)).QtdAnterior, Blank()),
                    Q3: If(_n >= 3, Last(FirstN(_fila, 3)).QtdAnterior, Blank()),
                    Q4: If(_n >= 4, Last(FirstN(_fila, 4)).QtdAnterior, Blank()),
                    Q5: If(_n >= 5, Last(FirstN(_fila, 5)).QtdAnterior, Blank()),
                    Q6: If(_n >= 6, Last(FirstN(_fila, 6)).QtdAnterior, Blank()),
                    Mais: If(_n > fx_PainelSlotsTranc, _n - fx_PainelSlotsTranc, 0),
                    // v0.9.0: chaves da ficha de consulta. FilaTab guarda os carreteis
                    // (com as OPs dentro) na mesma ordem das bolinhas.
                    IDAtiva: _f.ID,
                    FilaTab: _fila,
                    // v0.10.1: autonomia de tubo no instante da carga (varSincPnl). O label desconta
                    // o relogio da tela (fx_AutonomiaAgora). Blank = sem velocidade cadastrada.
                    VelAtiva: _vAtiva,
                    ConsumidoM: Round(_consM, 0),
                    RestanteM: Round(_restM, 0),
                    // v0.10.2: janelas JA FECHADAS do turno atual sem apontamento desta maquina.
                    SemApontar: CountRows(
                        Filter(
                            colJanTrPnl As _w5,
                            _w5.DataRef = fx_DataRefEm(varAgoraPnl) &&
                            _w5.Turno = fx_TurnoEm(varAgoraPnl) &&
                            _w5.Fim <= varAgoraPnl &&
                            IsBlank(
                                LookUp(
                                    _hhMaq As _hm5,
                                    _hm5.DataRef = _w5.DataRef && _hm5.Turno = _w5.Turno && _hm5.Hora = _w5.Hora
                                ).Hora
                            )
                        )
                    ),
                    AutonomiaMin: If(
                        _vAtiva > 0 && !_cim,
                        Round(_restM * 60 / _vAtiva + _minFila, 0),
                        Blank()
                    )
                }
                )
                )
                )
            )
        )
    )
);
ClearCollect(
    colBitolasPnl,
    ForAll(
        fx_BitolasMandril As _bt,
        With(
            {
                _q: CountRows(
                    Filter(
                        colAguardPnl As _g2,
                        _g2.processo = "Tubo" &&
                        _g2.Bitola = _bt.Bitola &&
                        !IsBlank(_g2.'Carretel Entrada')
                    )
                )
            },
            {
                Bitola: _bt.Bitola,
                Qtd: _q,
                Cor: fx_SemaforoKanban(_q)
            }
        )
    )
);
ClearCollect(
    colAcabPnl,
    ForAll(
        fx_EtapasAcabPainel As _e,
        With(
            {
                _f: LookUp(colAtivasPnl As _a2, _a2.processo = _e.Processo),
                _fila: AddColumns(
                    Sort(
                        Filter(colAguardPnl As _g3, _g3.processo = _e.Processo),
                        ID,
                        SortOrder.Ascending
                    ),
                    QtdAnterior,
                    Switch(
                        _e.Processo,
                        "Cobertura",    quantidade_trancagem,
                        "Bandagem",     quantidade_cobertura,
                        "Vulcanização", quantidade_bandagem,
                        "Debandagem",   quantidade_vulcanizacao
                    )
                )
            },
            With(
                {
                    _n: CountRows(_fila),
                    _ini: Switch(
                        _e.Processo,
                        "Cobertura",    _f.data_hora_inicio_cobertura,
                        "Bandagem",     _f.data_hora_inicio_bandagem,
                        "Vulcanização", _f.data_hora_inicio_vulcanizacao,
                        "Debandagem",   _f.data_hora_inicio_debandagem
                    )
                },
                With(
                    {
                        _est: If(
                            _e.Processo = "Vulcanização" && !IsBlank(_f.ID),
                            fx_EstadoVulca(
                                Text(_f.status_processo),
                                _f.InicioResfriamento_Vulcanizacao,
                                varAgoraPnl
                            ),
                            fx_EstadoPosto(!IsBlank(_f.ID), _n)
                        )
                    },
                    {
                        Ord: _e.Ord,
                        Processo: _e.Processo,
                        Rotulo: _e.Rotulo,
                        OP: Coalesce(_f.OP, 0),
                        Mangueira: Coalesce(Text(_f.Mangueira), ""),
                        Produzindo: !IsBlank(_f.ID),
                        Estado: _est,
                        InicioCrono: If(
                            _est = "RESFRIANDO",
                            _f.InicioResfriamento_Vulcanizacao,
                            _ini
                        ),
                        Fila: _n,
                        Q1: If(_n >= 1, Last(FirstN(_fila, 1)).QtdAnterior, Blank()),
                        Q2: If(_n >= 2, Last(FirstN(_fila, 2)).QtdAnterior, Blank()),
                        Q3: If(_n >= 3, Last(FirstN(_fila, 3)).QtdAnterior, Blank()),
                        Q4: If(_n >= 4, Last(FirstN(_fila, 4)).QtdAnterior, Blank()),
                        Q5: If(_n >= 5, Last(FirstN(_fila, 5)).QtdAnterior, Blank()),
                        Q6: If(_n >= 6, Last(FirstN(_fila, 6)).QtdAnterior, Blank()),
                        Q7: If(_n >= 7, Last(FirstN(_fila, 7)).QtdAnterior, Blank()),
                        Q8: If(_n >= 8, Last(FirstN(_fila, 8)).QtdAnterior, Blank()),
                        Q9: If(_n >= 9, Last(FirstN(_fila, 9)).QtdAnterior, Blank()),
                        Q10: If(_n >= 10, Last(FirstN(_fila, 10)).QtdAnterior, Blank()),
                        Q11: If(_n >= 11, Last(FirstN(_fila, 11)).QtdAnterior, Blank()),
                        Q12: If(_n >= 12, Last(FirstN(_fila, 12)).QtdAnterior, Blank()),
                        Mais: If(_n > fx_PainelSlotsAcab, _n - fx_PainelSlotsAcab, 0),
                        // v0.9.0: chaves da ficha de consulta, na ordem das bolinhas.
                        IDAtiva: _f.ID,
                        FilaTab: ForAll(_fila As _w, { ID: _w.ID })
                    }
                )
            )
        )
    )
);
With(
    {
        _fm: LookUp(colAtivasPnl As _a3, _a3.processo = "Mandril"),
        _ft: LookUp(colAtivasPnl As _a4, _a4.processo = "Tubo"),
        _fe: LookUp(colAtivasPnl As _a5, _a5.processo = "Extr./Teste")
    },
    Set(varMandAtivoPnl, !IsBlank(_fm.ID));
    Set(varTuboOPPnl, Coalesce(_ft.OP, 0));
    Set(varTuboMangPnl, Coalesce(Text(_ft.Mangueira), ""));
    Set(varTuboInicioPnl, _ft.data_hora_inicio_tubo);
    Set(varTuboAtivoPnl, !IsBlank(_ft.ID));
    Set(varTuboIDPnl, _ft.ID);
    Set(varExtrAtivoPnl, !IsBlank(_fe.ID))
);
ClearCollect(
    colFilaExtrPnl,
    Sort(
        Filter(colAguardPnl As _g4, _g4.processo = "Extr./Teste"),
        ID,
        SortOrder.Ascending
    )
);
Set(varFilaExtrPnl, CountRows(colFilaExtrPnl));
// Solda de Mandril e Extracao POR POSTO (v0.8.0, C37). A etapa tem duas
// maquinas fisicas; LookUp de uma OP so mostrava a primeira que achasse.
// Mandril nao tem fila propria (e a 1a etapa): estado = PRODUZINDO ou LIVRE.
ClearCollect(
    colPostosMandPnl,
    ForAll(
        Table(
            { Ord: 1, Posto: "TERMOFUSAO",  Curto: "Quente" },
            { Ord: 2, Posto: "VIBRACIONAL", Curto: "Vibracional" }
        ) As _m,
        With(
            {
                _f: LookUp(
                    colAtivasPnl As _a9,
                    _a9.processo = "Mandril" && _a9.maquina_mandril = _m.Posto
                )
            },
            {
                Ord: _m.Ord,
                Posto: _m.Posto,
                Curto: _m.Curto,
                OP: Coalesce(_f.OP, 0),
                Bitola: Coalesce(_f.Bitola, 0),
                Inicio: _f.data_hora_inicio_mandril,
                Produzindo: !IsBlank(_f.ID),
                Estado: fx_EstadoPosto(!IsBlank(_f.ID), 0)
            }
        )
    )
);
// Extracao: a fila e UMA so para as duas cabines; o estado e por cabine
// (parada com fila acende so na que esta parada).
ClearCollect(
    colPostosExtrPnl,
    ForAll(
        fx_CabinesTeste As _c,
        With(
            {
                _f: LookUp(
                    colAtivasPnl As _a8,
                    _a8.processo = "Extr./Teste" && _a8.cabine_teste = _c.Posto
                )
            },
            {
                Posto: _c.Posto,
                Rotulo: _c.Rotulo,
                Curto: Substitute(_c.Rotulo, "Cabine ", ""),
                OP: Coalesce(_f.OP, 0),
                Mangueira: Coalesce(Text(_f.Mangueira), ""),
                Inicio: _f.data_hora_inicio_extracao,
                Produzindo: !IsBlank(_f.ID),
                Estado: fx_EstadoPosto(!IsBlank(_f.ID), varFilaExtrPnl),
                IDAtiva: _f.ID
            }
        )
    )
);
Set(
    varMandProduzidoPnl,
    Sum(
        Filter(
            colEvMandPnl As _m1,
            _m1.TurnoTxt = Text(fx_TurnoEm(varAgoraPnl), "[$-en-US]0") &&
            (_m1.TipoTxt = "Fim" || _m1.TipoTxt = "Parcial")
        ),
        metros
    )
);
Set(
    varKanbanTuboPnl,
    CountRows(
        Filter(
            colAguardPnl As _g5,
            _g5.processo = "Tubo" && !IsBlank(_g5.'Carretel Entrada')
        )
    )
);
ClearCollect(
    colFilaTuboPnl,
    AddColumns(
        Sort(
            Filter(colAguardPnl As _g6, _g6.processo = "Tubo"),
            ID,
            SortOrder.Ascending
        ),
        QtdAnterior,
        quantidade_mandril
    )
);
Set(varFilaTuboPnl, CountRows(colFilaTuboPnl));
Set(varQT1Pnl, If(varFilaTuboPnl >= 1, Last(FirstN(colFilaTuboPnl, 1)).QtdAnterior, Blank()));
Set(varQT2Pnl, If(varFilaTuboPnl >= 2, Last(FirstN(colFilaTuboPnl, 2)).QtdAnterior, Blank()));
Set(varQT3Pnl, If(varFilaTuboPnl >= 3, Last(FirstN(colFilaTuboPnl, 3)).QtdAnterior, Blank()));
Set(varQT4Pnl, If(varFilaTuboPnl >= 4, Last(FirstN(colFilaTuboPnl, 4)).QtdAnterior, Blank()));
Set(varQT5Pnl, If(varFilaTuboPnl >= 5, Last(FirstN(colFilaTuboPnl, 5)).QtdAnterior, Blank()));
Set(varQT6Pnl, If(varFilaTuboPnl >= 6, Last(FirstN(colFilaTuboPnl, 6)).QtdAnterior, Blank()));
// Bobinagem (v0.7.0) — FifoBobinadeira. AB = pedido aberto, EP = bobinando,
// BC = bobinado, CO = consumido. BC ainda NAO entra: o consumo nao e gravado
// (OP_Consumo vazio), entao BC acumula desde junho. Carrinho fisico entra depois.
// v0.11.0 (item 5): EP e AB vem da UMA consulta da FifoBobinadeira feita no Concurrent (colBobFifoPnl);
// aqui so o recorte local. Falha da consulta = varBobSemFontePnl true (setado la).
ClearCollect(
    colBobEPPnl,
    Sort(Filter(colBobFifoPnl, Status = "EP"), DataHoraInicio, SortOrder.Ascending)
);
Set(varBobAbertosPnl, CountRows(Filter(colBobFifoPnl, Status = "AB")));
Set(varBobCarrinhoPnl, CountRows(colBobEPPnl));
Set(varBobInicioPnl, First(colBobEPPnl).DataHoraInicio);
// Estado no vocabulario do fx_CorEstadoPosto: cor igual as outras etapas.
Set(
    varBobStatusPnl,
    If(varBobCarrinhoPnl > 0, "PRODUZINDO", varBobAbertosPnl > 0, "COM FILA", "LIVRE")
);
Set(
    varBobBadgePnl,
    If(varBobCarrinhoPnl > 0, "BOBINANDO", varBobAbertosPnl > 0, "COM PEDIDO", "LIVRE")
);
Set(
    varBobFioPnl,
    With(
        { _o: First(colBobEPPnl) },
        If(
            varBobCarrinhoPnl > 0,
            _o.Mangueira & " · " & Text(_o.NFios, "[$-en-US]0") & " fios" &
            If(varBobAbertosPnl > 0, "  ·  " & Text(varBobAbertosPnl, "[$-en-US]0") & " aberto(s)", ""),
            varBobAbertosPnl > 0,
            Text(varBobAbertosPnl, "[$-en-US]0") & " pedido(s) aberto(s)",
            "sem pedido na fila"
        )
    )
);
ClearCollect(
    colVulcAtivasPnl,
    AddColumns(
        Sort(
            Filter(colAtivasPnl As _v1, _v1.processo = "Vulcanização"),
            ID,
            SortOrder.Ascending
        ),
        QtdAnterior,
        quantidade_bandagem
    )
);
Set(varVulcQtdPnl, CountRows(colVulcAtivasPnl));
Set(varVQ1Pnl, If(varVulcQtdPnl >= 1, Last(FirstN(colVulcAtivasPnl, 1)).QtdAnterior, Blank()));
Set(varVQ2Pnl, If(varVulcQtdPnl >= 2, Last(FirstN(colVulcAtivasPnl, 2)).QtdAnterior, Blank()));
Set(varVQ3Pnl, If(varVulcQtdPnl >= 3, Last(FirstN(colVulcAtivasPnl, 3)).QtdAnterior, Blank()));
Set(varVQ4Pnl, If(varVulcQtdPnl >= 4, Last(FirstN(colVulcAtivasPnl, 4)).QtdAnterior, Blank()));
Set(varVQ5Pnl, If(varVulcQtdPnl >= 5, Last(FirstN(colVulcAtivasPnl, 5)).QtdAnterior, Blank()));
Set(varVQ6Pnl, If(varVulcQtdPnl >= 6, Last(FirstN(colVulcAtivasPnl, 6)).QtdAnterior, Blank()));
Set(varVQ7Pnl, If(varVulcQtdPnl >= 7, Last(FirstN(colVulcAtivasPnl, 7)).QtdAnterior, Blank()));
Set(varVQ8Pnl, If(varVulcQtdPnl >= 8, Last(FirstN(colVulcAtivasPnl, 8)).QtdAnterior, Blank()));
Set(varVQ9Pnl, If(varVulcQtdPnl >= 9, Last(FirstN(colVulcAtivasPnl, 9)).QtdAnterior, Blank()));
Set(varVQ10Pnl, If(varVulcQtdPnl >= 10, Last(FirstN(colVulcAtivasPnl, 10)).QtdAnterior, Blank()));
Set(varVQ11Pnl, If(varVulcQtdPnl >= 11, Last(FirstN(colVulcAtivasPnl, 11)).QtdAnterior, Blank()));
Set(varVQ12Pnl, If(varVulcQtdPnl >= 12, Last(FirstN(colVulcAtivasPnl, 12)).QtdAnterior, Blank()));
// Bateladas REAIS da Vulcanizacao (v0.6.0).
// Batelada = grupo de "Início" colados no tempo: um Início abre batelada nova
// quando nao houve outro Início nos 30 min anteriores (as 5 OPs de 08:23/08:24
// entram juntas). Maximo de 5 bateladas no dia e 5 carreteis por batelada.
// colGradeVulcPnl so rotula as colunas que ainda nao aconteceram.
ClearCollect(
    colGradeVulcPnl,
    { Ord: 1, Hora: "05:50" },
    { Ord: 2, Hora: "09:20" },
    { Ord: 3, Hora: "12:50" },
    { Ord: 4, Hora: "16:20" },
    { Ord: 5, Hora: "19:50" }
);
With(
    { _dr: fx_DataRefEm(varAgoraPnl) },
    // v0.9.2: cada bolinha e UM carretel, e cada carretel vem de UMA fonte so.
    // Na autoclave agora (ficha Em processo) -> entra pelo inicio gravado na ficha e
    // fica AZUL. Ja saiu -> entra pelo evento de Inicio do dia. Antes a grade lia so
    // evento e o numero lia so ficha: 6 bolinhas contra 5 na autoclave em 25/09.
    ClearCollect(
        colIniVulcPnl,
        ForAll(
            Filter(
                colEvVulcPnl As _ev0,
                _ev0.TipoTxt = "Início" && !(_ev0.origem_ID in colVulcAtivasPnl.ID)
            ) As _ev1,
            { MinIni: DateDiff(_dr, _ev1.data_hora, TimeUnit.Minutes), NaAuto: false }
        )
    );
    Collect(
        colIniVulcPnl,
        ForAll(
            colVulcAtivasPnl As _va,
            {
                MinIni: DateDiff(_dr, Coalesce(_va.data_hora_inicio_vulcanizacao, varAgoraPnl), TimeUnit.Minutes),
                NaAuto: true
            }
        )
    );
    ClearCollect(
        colCabVulcPnl,
        FirstN(
            Sort(
                Distinct(
                    Filter(
                        colIniVulcPnl As _i,
                        IsEmpty(
                            Filter(
                                colIniVulcPnl As _k,
                                _k.MinIni < _i.MinIni && _k.MinIni >= _i.MinIni - 30
                            )
                        )
                    ),
                    MinIni
                ),
                Value,
                SortOrder.Ascending
            ),
            5
        )
    );
    With(
        { _nCab: CountRows(colCabVulcPnl) },
        ClearCollect(
            colBatVulcPnl,
            ForAll(
                Sequence(5) As _s,
                With(
                    {
                        _existe: _s.Value <= _nCab,
                        _de: If(_s.Value <= _nCab, Last(FirstN(colCabVulcPnl, _s.Value)).Value, 0),
                        _ate: If(_s.Value < _nCab, Last(FirstN(colCabVulcPnl, _s.Value + 1)).Value, 99999)
                    },
                    {
                        Ord: _s.Value,
                        Hora: If(
                            _existe,
                            Text(DateAdd(_dr, _de, TimeUnit.Minutes), "hh:mm"),
                            LookUp(colGradeVulcPnl As _gb, _gb.Ord = _s.Value).Hora
                        ),
                        // Autoclave comporta no maximo 5 carreteis por batelada.
                        Qtd: If(
                            _existe,
                            Min(
                                CountRows(
                                    Filter(
                                        colIniVulcPnl As _i2,
                                        _i2.MinIni >= _de && _i2.MinIni < _ate
                                    )
                                ),
                                5
                            ),
                            0
                        ),
                        // v0.9.2: quantos carreteis DESTA batelada ainda estao na autoclave.
                        QtdAuto: If(
                            _existe,
                            Min(
                                CountRows(
                                    Filter(
                                        colIniVulcPnl As _i3,
                                        _i3.NaAuto && _i3.MinIni >= _de && _i3.MinIni < _ate
                                    )
                                ),
                                5
                            ),
                            0
                        ),
                        // v0.9.2: ATUAL = batelada com carretel ainda na autoclave, venha
                        // de onde vier. Batelada antiga com carretel dentro acende azul
                        // tambem: e OP que nao teve o Fim apontado.
                        Estado: If(
                            !_existe, "FUTURA",
                            CountRows(
                                Filter(
                                    colIniVulcPnl As _i4,
                                    _i4.NaAuto && _i4.MinIni >= _de && _i4.MinIni < _ate
                                )
                            ) > 0, "ATUAL",
                            "CONCLUIDA"
                        )
                    }
                )
            )
        )
    )
);
Set(
    varMaiorFilaPnl,
    Coalesce(
        Text(First(Sort(colAcabPnl, Fila, SortOrder.Descending)).Processo),
        ""
    )
);
// ONDE OLHAR AGORA (v0.11.0 · itens 3 e 4). Todo item leva as mesmas 7 colunas:
//   Sev, Titulo, Detalhe, IdadeMin (ha quantos min o problema existe; 0 = nao medido) e
//   Tipo/Chave/N, que dizem a ficha de consulta o que abrir quando o item e tocado (Tipo vazio = sem ficha).
// Regras de FILA (sem OP + carretel esperando) ficam caladas em turno NAO trabalhado: sem janela
// apontada no turno de agora (criterio "Apontada", mesmo do consumo de tubo). Na 1a janela do turno
// vale a tolerancia (ainda ninguem apontou). Parada apontada, tubo, metragem e OP zumbi nao calam.
With(
    {
        _ta: fx_TurnoEm(varAgoraPnl),
        _dh: fx_DataRefEm(varAgoraPnl)
    },
    With(
        {
            _trab: ((Text(_dh, "yyyy-mm-dd") & "|" & Text(_ta, "[$-en-US]0")) in colTurnosHHPnl.Value) ||
                (fx_MinNoTurno(varAgoraPnl, _ta) < LookUp(fx_GradeHoraHora As _gt, _gt.Turno = _ta && _gt.Ord = 2).Fim)
        },
        // 1 · PARADA apontada no Hora-Hora (com ou sem OP aberta). Pausa programada NAO entra.
        ClearCollect(
            colAndonPnl,
            ForAll(
                Filter(colPostosTrancPnl As _p1, _p1.Estado = "PARADA") As _q1,
                {
                    Sev: 1,
                    Titulo: _q1.Rotulo & " · " & _q1.Motivo,
                    Detalhe: "Parada nesta janela há " & fx_CronoLongo(_q1.InicioParada, varAgoraPnl) &
                    If(_q1.Produzindo, " · OP " & Text(_q1.OP, "[$-en-US]0") & " aberta", "") &
                    If(
                        _q1.Fila > 0,
                        " · " & Text(_q1.Fila, "[$-en-US]0") &
                        If(_q1.Fila = 1, " carretel esperando", " carretéis esperando"),
                        ""
                    ),
                    IdadeMin: Max(0, DateDiff(_q1.InicioParada, varAgoraPnl, TimeUnit.Minutes)),
                    Tipo: "TRANC",
                    Chave: _q1.Posto,
                    N: 0
                }
            )
        );
        // 2 · Trancadeira SEM OP e COM FILA (sem parada nem pausa apontada).
        Collect(
            colAndonPnl,
            ForAll(
                Filter(
                    colPostosTrancPnl As _p1b,
                    _trab && !_p1b.Produzindo && _p1b.Estado = "COM FILA"
                ) As _q1b,
                {
                    Sev: 1,
                    Titulo: _q1b.Rotulo & " sem OP · com fila",
                    Detalhe: Text(_q1b.Fila, "[$-en-US]0") &
                    If(_q1b.Fila = 1, " carretel esperando", " carretéis esperando") &
                    If(
                        _q1b.OpsFila > _q1b.Fila,
                        " · " & Text(_q1b.OpsFila, "[$-en-US]0") & " OPs",
                        ""
                    ),
                    IdadeMin: 0,
                    Tipo: "TRANC",
                    Chave: _q1b.Posto,
                    N: 0
                }
            )
        );
        // 3 · Tubo esgotado pela conta (carretel montado consumido, fila vazia, OP Em processo).
        // O detalhe diz a causa mais provavel: janela do turno sem Hora-Hora.
        Collect(
            colAndonPnl,
            ForAll(
                Filter(
                    colPostosTrancPnl As _p4,
                    _p4.Produzindo && _p4.Estado <> "PARADA" && !IsBlank(_p4.AutonomiaMin) && _p4.AutonomiaMin <= 0
                ) As _q4,
                {
                    Sev: 1,
                    Titulo: _q4.Rotulo & " · tubo esgotado pela conta",
                    Detalhe: If(
                        _q4.SemApontar > 0,
                        Text(_q4.SemApontar, "[$-en-US]0") &
                        If(_q4.SemApontar = 1, " janela sem Hora-Hora", " janelas sem Hora-Hora") &
                        " no turno · apontar e conferir o carretel",
                        "Conferir o carretel na máquina e o Fim da OP"
                    ),
                    IdadeMin: 0,
                    Tipo: "TRANC",
                    Chave: _q4.Posto,
                    N: 0
                }
            )
        );
        // 4 · Mandril abaixo do minimo: UM item so para todas as bitolas (antes eram ate 6, e podiam
        // ocupar os 3 lugares da tela e esconder uma trancadeira parada).
        If(
            CountRows(Filter(colBitolasPnl, Qtd < fx_KanbanMinimo)) > 0,
            Collect(
                colAndonPnl,
                {
                    Sev: 1,
                    Titulo: "Mandril abaixo do mínimo · bitola " &
                    Concat(Filter(colBitolasPnl, Qtd < fx_KanbanMinimo), Text(Bitola, "[$-en-US]0"), ", "),
                    Detalhe: "Fila do Tubo com menos de " & Text(fx_KanbanMinimo, "[$-en-US]0") & " carretéis por bitola",
                    IdadeMin: 0,
                    Tipo: "TUBO",
                    Chave: "Tubo",
                    N: 0
                }
            )
        );
        // 5 · Etapas de acabamento SEM OP e COM FILA.
        Collect(
            colAndonPnl,
            ForAll(
                Filter(colAcabPnl As _a6, _trab && !_a6.Produzindo && _a6.Fila > 0) As _c2,
                {
                    Sev: 2,
                    Titulo: _c2.Rotulo & " sem OP · com fila",
                    Detalhe: Text(_c2.Fila, "[$-en-US]0") & " OP(s) esperando esta etapa",
                    IdadeMin: 0,
                    Tipo: "ACAB",
                    Chave: _c2.Processo,
                    N: 0
                }
            )
        );
        // 6 · Cabine da Extracao sem OP enquanto a fila espera (v0.8.0).
        Collect(
            colAndonPnl,
            ForAll(
                Filter(colPostosExtrPnl As _x1, _trab && !_x1.Produzindo && varFilaExtrPnl > 0) As _c4,
                {
                    Sev: 2,
                    Titulo: _c4.Rotulo & " sem OP · com fila",
                    Detalhe: Text(varFilaExtrPnl, "[$-en-US]0") & " OP(s) esperando a Extração",
                    IdadeMin: 0,
                    Tipo: "EXTR",
                    Chave: "Extr./Teste",
                    N: 0
                }
            )
        );
        // 7 · Tubo para MENOS DE UM TURNO UTIL (substitui a regra "rodando sem carretel atras" da
        // MEL-190, que disparava mesmo com horas de autonomia). Pausa e parada tem regra propria.
        Collect(
            colAndonPnl,
            ForAll(
                Filter(
                    colPostosTrancPnl As _p2,
                    _p2.Produzindo && _p2.Estado <> "PARADA" &&
                    (
                        (!IsBlank(_p2.AutonomiaMin) && _p2.AutonomiaMin > 0 && _p2.AutonomiaMin < fx_TurnoUtilMin) ||
                        (IsBlank(_p2.AutonomiaMin) && _p2.Fila = 0)
                    )
                ) As _q2,
                {
                    Sev: 2,
                    Titulo: _q2.Rotulo & If(IsBlank(_q2.AutonomiaMin), " · sem carretel atrás", " · tubo para menos de 1 turno"),
                    Detalhe: If(
                        IsBlank(_q2.AutonomiaMin),
                        "Sem velocidade cadastrada · sem carretel atrás",
                        "Autonomia " & fx_AutonomiaTexto(_q2.AutonomiaMin) & " · turno útil = " &
                        fx_AutonomiaTexto(fx_TurnoUtilMin)
                    ),
                    IdadeMin: 0,
                    Tipo: "TRANC",
                    Chave: _q2.Posto,
                    N: 0
                }
            )
        );
        // 8 · Metragem do carretel que espera: VAZIA (nao apontada) e IMPLAUSIVEL (apontada, abaixo do
        // minimo) sao problemas diferentes e viram itens diferentes. O metro da bolinha e o que a etapa
        // ANTERIOR apontou; o detalhe diz onde corrigir.
        With(
            {
                _mq: AddColumns(
                    Filter(
                        colAguardPnl As _mq0,
                        _mq0.processo in ["Tubo", "Trançadeira", "Cobertura", "Bandagem", "Vulcanização", "Debandagem"]
                    ),
                    MetrosBol,
                    Switch(
                        processo,
                        "Tubo",         quantidade_mandril,
                        "Trançadeira",  quantidade_tubo,
                        "Cobertura",    quantidade_trancagem,
                        "Bandagem",     quantidade_cobertura,
                        "Vulcanização", quantidade_bandagem,
                        "Debandagem",   quantidade_vulcanizacao
                    ),
                    EtapaAnt,
                    Switch(
                        processo,
                        "Tubo",         "Mandril",
                        "Trançadeira",  "Tubo",
                        "Cobertura",    "Trançagem",
                        "Bandagem",     "Cobertura",
                        "Vulcanização", "Bandagem",
                        "Debandagem",   "Vulcanização"
                    )
                )
            },
            Collect(
                colAndonPnl,
                ForAll(
                    Filter(_mq As _m1, IsBlank(_m1.MetrosBol)) As _c6,
                    {
                        Sev: 2,
                        Titulo: If(_c6.processo = "Trançadeira", Coalesce(Text(_c6.Trançadeira), "Trançagem"), _c6.processo) &
                        " · carretel sem metragem",
                        Detalhe: "OP " & Text(_c6.OP, "[$-en-US]0") & " · metragem do " & _c6.EtapaAnt & " não apontada",
                        IdadeMin: 0,
                        Tipo: Switch(_c6.processo, "Tubo", "TUBO", "Trançadeira", If(IsBlank(Text(_c6.Trançadeira)), "", "TRANC"), "ACAB"),
                        Chave: Switch(_c6.processo, "Tubo", "Tubo", "Trançadeira", Text(_c6.Trançadeira), _c6.processo),
                        N: 0
                    }
                )
            );
            Collect(
                colAndonPnl,
                ForAll(
                    Filter(_mq As _m2, !IsBlank(_m2.MetrosBol) && _m2.MetrosBol < fx_MetrosMinCarretel) As _c5,
                    {
                        Sev: 2,
                        Titulo: If(_c5.processo = "Trançadeira", Coalesce(Text(_c5.Trançadeira), "Trançagem"), _c5.processo) &
                        " · carretel com " & Text(_c5.MetrosBol, "[$-en-US]0") & " m",
                        Detalhe: "OP " & Text(_c5.OP, "[$-en-US]0") & " · metragem do " & _c5.EtapaAnt & " a corrigir na ficha",
                        IdadeMin: 0,
                        Tipo: Switch(_c5.processo, "Tubo", "TUBO", "Trançadeira", If(IsBlank(Text(_c5.Trançadeira)), "", "TRANC"), "ACAB"),
                        Chave: Switch(_c5.processo, "Tubo", "Tubo", "Trançadeira", Text(_c5.Trançadeira), _c5.processo),
                        N: 0
                    }
                )
            )
        );
        // 9 · OP zumbi: acima do teto de horas na mesma etapa.
        Collect(
            colAndonPnl,
            ForAll(
                Filter(
                    colPostosTrancPnl As _p3,
                    _p3.Produzindo &&
                    !IsBlank(_p3.Inicio) &&
                    DateDiff(_p3.Inicio, varAgoraPnl, TimeUnit.Hours) > fx_TetoOPHoras
                ) As _q3,
                {
                    Sev: 3,
                    Titulo: "OP " & Text(_q3.OP, "[$-en-US]0") & " há " & Text(DateDiff(_q3.Inicio, varAgoraPnl, TimeUnit.Hours), "[$-en-US]0") & " h na " & _q3.Rotulo,
                    Detalhe: "Acima do teto de " & Text(fx_TetoOPHoras, "[$-en-US]0") & " h na mesma etapa",
                    IdadeMin: DateDiff(_q3.Inicio, varAgoraPnl, TimeUnit.Minutes),
                    Tipo: "TRANC",
                    Chave: _q3.Posto,
                    N: 0
                }
            )
        );
        Collect(
            colAndonPnl,
            ForAll(
                Filter(
                    colAcabPnl As _a7,
                    _a7.Produzindo &&
                    !IsBlank(_a7.InicioCrono) &&
                    DateDiff(_a7.InicioCrono, varAgoraPnl, TimeUnit.Hours) > fx_TetoOPHoras
                ) As _c3,
                {
                    Sev: 3,
                    Titulo: "OP " & Text(_c3.OP, "[$-en-US]0") & " há " & Text(DateDiff(_c3.InicioCrono, varAgoraPnl, TimeUnit.Hours), "[$-en-US]0") & " h na " & _c3.Rotulo,
                    Detalhe: "Acima do teto de " & Text(fx_TetoOPHoras, "[$-en-US]0") & " h na mesma etapa",
                    IdadeMin: DateDiff(_c3.InicioCrono, varAgoraPnl, TimeUnit.Minutes),
                    Tipo: "ACAB",
                    Chave: _c3.Processo,
                    N: 0
                }
            )
        )
    )
);
Set(varAndonQtdPnl, CountRows(colAndonPnl));
// v0.11.0 (item 2 · A3 · M12): varSincPnl e a ANCORA do calculo (autonomia, retrato da ficha) e
// avanca sempre; a IDADE DO DADO e varUltOkPnl, que so avanca em carga 100% ok (sem falha e sem
// truncamento). "Celula em dia" e o rodape leem varCargaOkPnl / varUltOkPnl.
Set(varSincPnl, varAgoraPnl);
Set(varCargaOkPnl, !varFalhaPnl && !varTruncaPnl);
If(varCargaOkPnl, Set(varUltOkPnl, varAgoraPnl));
Select(btn_AgregaPnl);
// Medidor do ciclo: duracao da carga em segundos (unica leitura de relogio fora do instante do ciclo).
Set(varCargaSegPnl, DateDiff(varAgoraPnl, Now(), TimeUnit.Seconds))
```

**`btn_DetAbrirPnl` → `OnSelect`** (propriedade inteira; muda só o ramo `_p.Estado = "CIMENTO"` do `Sub`)

```powerfx
Set(varDetToquePnl, Now());
// v0.9.0 · FICHA DE CONSULTA (C36 · C1 · C21). Toda a busca e LOCAL: le so as colecoes
// que a carga de 2 min ja trouxe (colAtivasPnl, colAguardPnl, colPostos*, colHHJanPnl).
// Zero chamada ao SharePoint no toque, por isso abre na hora. Zero Patch: e consulta.
// Cada controle clicavel so grava varDetReqPnl {Tipo, Chave, N} e chama este botao;
// a logica mora num lugar so.
Set(varDetSincPnl, varSincPnl);
Set(varDetIDPnl, Blank());
// v0.14.0: etapa tocada = chave de colProdEtapaTurnoPnl (bloco PRODUCAO DO PROCESSO da ficha).
// TRANC/TUBO/EXTR/BOB tem nome proprio; ACAB, VULC, MAND e TRANCP trazem a etapa na Chave.
Set(
    varDetEtapaPnl,
    Switch(
        varDetReqPnl.Tipo,
        "TRANC", "Trançagem",
        "TUBO",  "Tubo",
        "EXTR",  "Extração",
        "BOB",   "Bobinadeira",
        varDetReqPnl.Chave
    )
);
Clear(colDetListaPnl);
With(
    { _q: varDetReqPnl },
    If(
        _q.Tipo = "TRANC",
        With(
            { _p: LookUp(colPostosTrancPnl As _x1, _x1.Posto = _q.Chave) },
            If(
                _q.N = 0,
                // MAQUINA: a OP montada + a fila inteira, OP por OP, na ordem dos carreteis.
                If(
                    !IsBlank(_p.IDAtiva),
                    Collect(colDetListaPnl, { ID: _p.IDAtiva, Tag: "Na máquina agora", Ord: 0 })
                );
                // OP que divide o carretel com a OP montada NAO e tubo atras: entra em seguida,
                // do mesmo carretel (o caso que motivou a v0.8.1). Aparece logo abaixo da montada.
                With(
                    {
                        _carMaq: Upper(Trim(LookUp(colAtivasPnl As _a9, _a9.ID = _p.IDAtiva).'Carretel Entrada'))
                    },
                    If(
                        !IsBlank(_p.IDAtiva) && !IsBlank(_carMaq),
                        Collect(
                            colDetListaPnl,
                            ForAll(
                                Filter(
                                    colAguardPnl As _g9,
                                    _g9.processo = "Trançadeira" &&
                                    ((_g9.Trançadeira = _p.Posto && IsBlank(_g9.Cimento_Maquina)) || _g9.Cimento_Maquina = _p.Posto) &&
                                    Upper(Trim(_g9.'Carretel Entrada')) = _carMaq
                                ) As _m9,
                                { ID: _m9.ID, Tag: "Mesmo carretel · entra em seguida", Ord: 0.5 }
                            )
                        )
                    )
                );
                Collect(
                    colDetListaPnl,
                    ForAll(
                        Ungroup(_p.FilaTab, OpsCar) As _u,
                        {
                            ID: _u.ID,
                            Tag: If(
                                StartsWith(_u.CarKey, "ID-"),
                                "Sem carretel apontado",
                                "Carretel " & _u.CarKey
                            ) & " · " & Text(
                                CountRows(Filter(_p.FilaTab As _k1, _k1.PrimID <= _u.PrimID)),
                                "[$-en-US]0"
                            ) & "º atrás",
                            Ord: _u.PrimID
                        }
                    )
                );
                With(
                    { _hh: Filter(colHHJanPnl As _j1, _j1.Celula = _p.Posto && _j1.Fechada) },
                    Set(
                        varDetPnl,
                        {
                            Titulo: _p.Rotulo & " · Trançadeira",
                            // v0.11.0 (item 4): PARADA e PAUSA vem antes de "Trancando", porque a trancadeira pode
                            // estar parada COM OP aberta.
                            Sub: If(
                                _p.Estado = "PARADA",
                                "Parada · " & _p.Motivo & " · nesta janela há " & fx_CronoLongo(_p.InicioParada, ctxAgoraPnl),
                                _p.Estado = "PAUSA",
                                "Pausa programada · " & _p.Motivo & " · há " & fx_CronoLongo(_p.InicioParada, ctxAgoraPnl),
                                _p.Estado = "CIMENTO",
                                "Aplicando cimento há " & fx_CronoLongo(_p.InicioCimento, ctxAgoraPnl),
                                _p.Produzindo,
                                "Trançando há " & fx_CronoLongo(_p.Inicio, ctxAgoraPnl),
                                _p.Fila > 0,
                                "Sem OP, com fila",
                                "Livre"
                            ) & "  ·  " & Text(_p.Fila, "[$-en-US]0") &
                            If(_p.Fila = 1, " carretel atrás", " carretéis atrás"),
                            Estado: _p.Estado,
                            Cor: _p.Cor,
                            Lado: "NA MÁQUINA E NA FILA",
                            Maquina: _p.Posto,
                            Motivo: _p.Motivo,
                            ParadoMin: _p.ParadoMin,
                            PausaMin: _p.PausaMin,
                            HHReal: Sum(_hh, Real),
                            HHMeta: Sum(_hh, Meta)
                        }
                    )
                ),
                // CARRETEL: as OPs que ele carrega (v0.8.1: um carretel pode levar mais de uma).
                With(
                    { _c: Index(_p.FilaTab, _q.N) },
                    Collect(
                        colDetListaPnl,
                        ForAll(_c.OpsCar As _o, { ID: _o.ID, Tag: "Neste carretel", Ord: 1 })
                    );
                    Set(
                        varDetPnl,
                        {
                            Titulo: If(
                                StartsWith(_c.CarKey, "ID-"),
                                "Carretel não apontado",
                                "Carretel " & _c.CarKey
                            ),
                            Sub: "Esperando a " & _p.Rotulo & "  ·  " & Text(_q.N, "[$-en-US]0") & "º de " &
                            Text(_p.Fila, "[$-en-US]0") & "  ·  " & Text(_c.NOps, "[$-en-US]0") &
                            If(_c.NOps = 1, " OP", " OPs") & "  ·  " & Text(_c.QtdAnterior, "[$-en-US]0") & " m",
                            Estado: "AGUARDANDO",
                            Cor: fx_CorEstadoPosto("AGUARDANDO"),
                            Lado: "OPS NESTE CARRETEL",
                            Maquina: "",
                            Motivo: "",
                            ParadoMin: 0,
                            PausaMin: 0,
                            HHReal: 0,
                            HHMeta: 0
                        }
                    )
                )
            )
        ),
        _q.Tipo = "ACAB" || _q.Tipo = "VULC",
        With(
            { _a: LookUp(colAcabPnl As _x2, _x2.Processo = _q.Chave) },
            If(
                _a.Processo = "Vulcanização",
                Collect(
                    colDetListaPnl,
                    ForAll(colVulcAtivasPnl As _v1, { ID: _v1.ID, Tag: "Na autoclave", Ord: 0 })
                ),
                !IsBlank(_a.IDAtiva),
                Collect(colDetListaPnl, { ID: _a.IDAtiva, Tag: "Em processo", Ord: 0 })
            );
            Collect(
                colDetListaPnl,
                ForAll(
                    Sequence(CountRows(_a.FilaTab)) As _s1,
                    {
                        ID: Index(_a.FilaTab, _s1.Value).ID,
                        Tag: Text(_s1.Value, "[$-en-US]0") & "º na fila",
                        Ord: _s1.Value
                    }
                )
            );
            If(
                _q.Tipo = "VULC",
                Set(varDetIDPnl, Index(colVulcAtivasPnl, _q.N).ID),
                _q.N > 0,
                Set(varDetIDPnl, Index(_a.FilaTab, _q.N).ID)
            );
            Set(
                varDetPnl,
                {
                    Titulo: _a.Rotulo,
                    Sub: If(
                        _a.Processo = "Vulcanização",
                        Text(varVulcQtdPnl, "[$-en-US]0") & " na autoclave",
                        _a.Produzindo,
                        "Em processo há " & fx_CronoLongo(_a.InicioCrono, ctxAgoraPnl),
                        "Sem OP em processo"
                    ) & "  ·  " & Text(_a.Fila, "[$-en-US]0") & " na fila",
                    Estado: _a.Estado,
                    Cor: fx_CorEstadoPosto(_a.Estado),
                    Lado: If(_a.Processo = "Vulcanização", "NA AUTOCLAVE E NA FILA", "EM PROCESSO E NA FILA"),
                    Maquina: "",
                    Motivo: "",
                    ParadoMin: 0,
                    PausaMin: 0,
                    HHReal: 0,
                    HHMeta: 0
                }
            )
        ),
        _q.Tipo = "TUBO",
        If(
            varTuboAtivoPnl,
            Collect(colDetListaPnl, { ID: varTuboIDPnl, Tag: "Na extrusora agora", Ord: 0 })
        );
        Collect(
            colDetListaPnl,
            ForAll(
                Sequence(varFilaTuboPnl) As _s2,
                With(
                    { _t: Index(colFilaTuboPnl, _s2.Value) },
                    {
                        ID: _t.ID,
                        Tag: "Carretel " & fx_Ou(Text(_t.'Carretel Entrada')) & " · " &
                        Text(_s2.Value, "[$-en-US]0") & "º na fila",
                        Ord: _s2.Value
                    }
                )
            )
        );
        If(_q.N > 0, Set(varDetIDPnl, Index(colFilaTuboPnl, _q.N).ID));
        Set(
            varDetPnl,
            {
                Titulo: "Extrusão de Tubo",
                Sub: If(
                    varTuboAtivoPnl,
                    "Extrudando há " & fx_CronoLongo(varTuboInicioPnl, ctxAgoraPnl),
                    "Sem OP em processo"
                ) & "  ·  " & Text(varFilaTuboPnl, "[$-en-US]0") & " na fila",
                Estado: fx_EstadoPosto(varTuboAtivoPnl, varFilaTuboPnl),
                Cor: fx_CorEstadoPosto(fx_EstadoPosto(varTuboAtivoPnl, varFilaTuboPnl)),
                Lado: "NA EXTRUSORA E NA FILA",
                Maquina: "",
                Motivo: "",
                ParadoMin: 0,
                PausaMin: 0,
                HHReal: 0,
                HHMeta: 0
            }
        ),
        _q.Tipo = "EXTR",
        Collect(
            colDetListaPnl,
            ForAll(
                Filter(colPostosExtrPnl As _e1, _e1.Produzindo) As _e2,
                { ID: _e2.IDAtiva, Tag: _e2.Rotulo & " · testando", Ord: 0 }
            )
        );
        Collect(
            colDetListaPnl,
            ForAll(
                Sequence(varFilaExtrPnl) As _s3,
                {
                    ID: Index(colFilaExtrPnl, _s3.Value).ID,
                    Tag: Text(_s3.Value, "[$-en-US]0") & "º na fila",
                    Ord: _s3.Value
                }
            )
        );
        Set(
            varDetPnl,
            {
                Titulo: "Extração / Teste",
                Sub: Text(CountRows(Filter(colPostosExtrPnl As _e3, _e3.Produzindo)), "[$-en-US]0") & " de " &
                Text(CountRows(colPostosExtrPnl), "[$-en-US]0") & " cabines testando  ·  " &
                Text(varFilaExtrPnl, "[$-en-US]0") & " na fila",
                Estado: fx_EstadoPosto(varExtrAtivoPnl, varFilaExtrPnl),
                Cor: fx_CorEstadoPosto(fx_EstadoPosto(varExtrAtivoPnl, varFilaExtrPnl)),
                Lado: "NAS CABINES E NA FILA",
                Maquina: "",
                Motivo: "",
                ParadoMin: 0,
                PausaMin: 0,
                HHReal: 0,
                HHMeta: 0
            }
        ),
        // v0.14.0 · MODO PROCESSO (sem OP tocada): Solda de Mandril, cabecalho da Trancagem e Bobinagem.
        // A ficha abre com o bloco de producao por turno e, quando ha, as OPs em curso do processo.
        _q.Tipo = "MAND",
        Collect(
            colDetListaPnl,
            ForAll(
                Filter(colAtivasPnl As _m2, _m2.processo = "Mandril") As _m3,
                {
                    ID: _m3.ID,
                    Tag: Switch(
                        Text(_m3.maquina_mandril),
                        "TERMOFUSAO", "Quente",
                        "VIBRACIONAL", "Vibracional",
                        "Posto não informado"
                    ) & " · soldando",
                    Ord: 0
                }
            )
        );
        Set(
            varDetPnl,
            {
                Titulo: "Solda de Mandril",
                Sub: Text(CountRows(Filter(colPostosMandPnl As _m4, _m4.Produzindo)), "[$-en-US]0") & " de " &
                Text(CountRows(colPostosMandPnl), "[$-en-US]0") & " soldando",
                Estado: fx_EstadoPosto(varMandAtivoPnl, 0),
                Cor: fx_CorEstadoPosto(fx_EstadoPosto(varMandAtivoPnl, 0)),
                Lado: "SOLDANDO AGORA",
                Maquina: "",
                Motivo: "",
                ParadoMin: 0,
                PausaMin: 0,
                HHReal: 0,
                HHMeta: 0
            }
        ),
        _q.Tipo = "TRANCP",
        Collect(
            colDetListaPnl,
            ForAll(
                Filter(colPostosTrancPnl As _t5, _t5.Produzindo) As _t6,
                {
                    ID: _t6.IDAtiva,
                    Tag: _t6.Rotulo & If(
                        _t6.Estado = "PARADA", " · parada com OP",
                        _t6.Estado = "PAUSA",  " · em pausa",
                        " · trançando"
                    ),
                    Ord: 0
                }
            )
        );
        With(
            {
                _nP: CountRows(Filter(colPostosTrancPnl As _t7, _t7.Estado = "PRODUZINDO")),
                _nX: CountRows(Filter(colPostosTrancPnl As _t8, _t8.Estado = "PARADA"))
            },
            With(
                { _eT: If(_nP > 0, "PRODUZINDO", _nX > 0, "PARADA", "LIVRE") },
                Set(
                    varDetPnl,
                    {
                        Titulo: "Trançagem",
                        Sub: Text(_nP, "[$-en-US]0") & " de " & Text(CountRows(colPostosTrancPnl), "[$-en-US]0") & " trançando" &
                        If(_nX > 0, "  ·  " & Text(_nX, "[$-en-US]0") & " parada(s)", ""),
                        Estado: _eT,
                        Cor: fx_CorEstadoPosto(_eT),
                        Lado: "TRANÇANDO AGORA",
                        Maquina: "",
                        Motivo: "",
                        ParadoMin: 0,
                        PausaMin: 0,
                        HHReal: 0,
                        HHMeta: 0
                    }
                )
            )
        ),
        _q.Tipo = "BOB",
        // Bobinagem nao tem OP na ficha_producao nem evento de producao: so o estado da fifo.
        Set(
            varDetPnl,
            {
                Titulo: "Bobinagem",
                Sub: If(varBobSemFontePnl, "Fifo sem resposta · última leitura", varBobFioPnl) &
                If(IsBlank(varBobInicioPnl), "", "  ·  bobinando há " & fx_CronoLongo(varBobInicioPnl, ctxAgoraPnl)),
                Estado: If(varBobSemFontePnl, "SEM DADO DA FIFO", varBobBadgePnl),
                Cor: If(varBobSemFontePnl, fx_CorTextoSuave, fx_CorEstadoPosto(varBobStatusPnl)),
                Lado: "BOBINAGEM",
                Maquina: "",
                Motivo: "",
                ParadoMin: 0,
                PausaMin: 0,
                HHReal: 0,
                HHMeta: 0
            }
        )
    )
);
// Foco: a bolinha tocada; sem bolinha, o primeiro da lista (quem esta na maquina).
If(
    IsBlank(varDetIDPnl),
    Set(varDetIDPnl, First(Sort(colDetListaPnl, Ord * 1000000 + ID, SortOrder.Ascending)).ID)
);
// Retrato das OPs, com REGISTRO EXPLICITO e UM salto so a partir das colecoes da carga.
// ShowColumns na ficha_producao quebra nome interno (licao v0.7.1 do menu) e coluna que
// passa por colecao e variavel pode ser cortada pelo Explicit Column Selection (doc MS).
// A mesma lista de campos vale para as duas fontes: mexeu numa, mexa na outra.
ClearCollect(
    colDetOPsPnl,
    ForAll(
        Filter(colAtivasPnl As _z1, _z1.ID in colDetListaPnl.ID) As _r,
        {
            ID: _r.ID,
            OP: _r.OP,
            Mangueira: Text(_r.Mangueira),
            Bitola: _r.Bitola,
            Processo: Text(_r.processo),
            Status: Text(_r.status_processo),
            Carretel: Text(_r.'Carretel Entrada'),
            Trancadeira: Text(_r.Trançadeira),
            MaqMand: Text(_r.maquina_mandril),
            Cabine: Text(_r.cabine_teste),
            IniMand: _r.data_hora_inicio_mandril,
            FimMand: _r.data_hora_final_mandril,
            QMand: _r.quantidade_mandril,
            OpMand: Text(_r.operador_mandril),
            LoteMand: Text(_r.lote_mandril),
            IniTubo: _r.data_hora_inicio_tubo,
            FimTubo: _r.data_hora_final_tubo,
            QTubo: _r.quantidade_tubo,
            RefTubo: _r.defeito_tubo,
            OpTubo: Text(_r.operador_tubo),
            CodTubo: Text(_r.'Cod.CompostoTubo'),
            LoteTubo: Text(_r.'Lote Composto Tubo'),
            ValTubo: _r.'Data de Validade do Composto Tubo',
            IniTr: _r.data_hora_inicio_trancadeira,
            FimTr: _r.data_hora_final_trancadeira,
            QTr: _r.quantidade_trancagem,
            RefTr: _r.defeito_trancagem,
            OpTr: Text(_r.operador_trancagem),
            Fio: Text(_r.Cod_Trançagem),
            LI: Text(_r.Lote_Trançagem),
            IniCob: _r.data_hora_inicio_cobertura,
            FimCob: _r.data_hora_final_cobertura,
            QCob: _r.quantidade_cobertura,
            RefCob: _r.defeito_cobertura,
            OpCob: Text(_r.operador_cobertura),
            CodCob: Text(_r.'Cod.Cobertura'),
            LoteCob: Text(_r.Lote_cobertura),
            ValCob: _r.'Data de Validade  do composto cobertura',
            IniBand: _r.data_hora_inicio_bandagem,
            FimBand: _r.data_hora_final_bandagem,
            QBand: _r.quantidade_bandagem,
            OpBand: Text(_r.operador_bandagem),
            IniVulc: _r.data_hora_inicio_vulcanizacao,
            FimVulc: _r.data_hora_final_vulcanizacao,
            QVulc: _r.quantidade_vulcanizacao,
            OpVulc: Text(_r.operador_vulcanizacao),
            IniDeb: _r.data_hora_inicio_debandagem,
            FimDeb: _r.data_hora_final_debandagem,
            QDeb: _r.quantidade_debandagem,
            OpDeb: Text(_r.operador_debandagem),
            IniExt: _r.data_hora_inicio_extracao,
            FimExt: _r.data_hora_final_extracao,
            QExt: Value(Text(_r.quantidade_extracao)),
            OpExt: Text(_r.operador_extracao),
            Obs: Coalesce(_r.Observação_Cobertura, _r.Observação_Trançagem, _r.Observação_tubo, _r.Observação_mandril)
        }
    )
);
Collect(
    colDetOPsPnl,
    ForAll(
        Filter(colAguardPnl As _z2, _z2.ID in colDetListaPnl.ID) As _r,
        {
            ID: _r.ID,
            OP: _r.OP,
            Mangueira: Text(_r.Mangueira),
            Bitola: _r.Bitola,
            Processo: Text(_r.processo),
            Status: Text(_r.status_processo),
            Carretel: Text(_r.'Carretel Entrada'),
            Trancadeira: Text(_r.Trançadeira),
            MaqMand: Text(_r.maquina_mandril),
            Cabine: Text(_r.cabine_teste),
            IniMand: _r.data_hora_inicio_mandril,
            FimMand: _r.data_hora_final_mandril,
            QMand: _r.quantidade_mandril,
            OpMand: Text(_r.operador_mandril),
            LoteMand: Text(_r.lote_mandril),
            IniTubo: _r.data_hora_inicio_tubo,
            FimTubo: _r.data_hora_final_tubo,
            QTubo: _r.quantidade_tubo,
            RefTubo: _r.defeito_tubo,
            OpTubo: Text(_r.operador_tubo),
            CodTubo: Text(_r.'Cod.CompostoTubo'),
            LoteTubo: Text(_r.'Lote Composto Tubo'),
            ValTubo: _r.'Data de Validade do Composto Tubo',
            IniTr: _r.data_hora_inicio_trancadeira,
            FimTr: _r.data_hora_final_trancadeira,
            QTr: _r.quantidade_trancagem,
            RefTr: _r.defeito_trancagem,
            OpTr: Text(_r.operador_trancagem),
            Fio: Text(_r.Cod_Trançagem),
            LI: Text(_r.Lote_Trançagem),
            IniCob: _r.data_hora_inicio_cobertura,
            FimCob: _r.data_hora_final_cobertura,
            QCob: _r.quantidade_cobertura,
            RefCob: _r.defeito_cobertura,
            OpCob: Text(_r.operador_cobertura),
            CodCob: Text(_r.'Cod.Cobertura'),
            LoteCob: Text(_r.Lote_cobertura),
            ValCob: _r.'Data de Validade  do composto cobertura',
            IniBand: _r.data_hora_inicio_bandagem,
            FimBand: _r.data_hora_final_bandagem,
            QBand: _r.quantidade_bandagem,
            OpBand: Text(_r.operador_bandagem),
            IniVulc: _r.data_hora_inicio_vulcanizacao,
            FimVulc: _r.data_hora_final_vulcanizacao,
            QVulc: _r.quantidade_vulcanizacao,
            OpVulc: Text(_r.operador_vulcanizacao),
            IniDeb: _r.data_hora_inicio_debandagem,
            FimDeb: _r.data_hora_final_debandagem,
            QDeb: _r.quantidade_debandagem,
            OpDeb: Text(_r.operador_debandagem),
            IniExt: _r.data_hora_inicio_extracao,
            FimExt: _r.data_hora_final_extracao,
            QExt: Value(Text(_r.quantidade_extracao)),
            OpExt: Text(_r.operador_extracao),
            Obs: Coalesce(_r.Observação_Cobertura, _r.Observação_Trançagem, _r.Observação_tubo, _r.Observação_mandril)
        }
    )
);
// Rota: 8 etapas por OP, do retrato. A galeria so filtra pela OP em foco.
ClearCollect(
    colDetRotaPnl,
    // v0.9.1: OperCurto = primeiro + ultimo nome, para caber na TV.
    AddColumns(
    Ungroup(
        ForAll(
            colDetOPsPnl As _d,
            {
                Linhas: Table(
                    { ID: _d.ID, Ord: 1, Etapa: "Mandril", Proc: "Mandril", Local: Switch(_d.MaqMand, "TERMOFUSAO", "Quente", "VIBRACIONAL", "Vibracional", ""), Ini: _d.IniMand, Fim: _d.FimMand, Mov: Coalesce(_d.FimMand, _d.IniMand), Qtd: _d.QMand, Ref: Blank(), Oper: _d.OpMand },
                    { ID: _d.ID, Ord: 2, Etapa: "Tubo", Proc: "Tubo", Local: "", Ini: _d.IniTubo, Fim: _d.FimTubo, Mov: Coalesce(_d.FimTubo, _d.IniTubo), Qtd: _d.QTubo, Ref: _d.RefTubo, Oper: _d.OpTubo },
                    { ID: _d.ID, Ord: 3, Etapa: "Trançagem", Proc: "Trançadeira", Local: _d.Trancadeira, Ini: _d.IniTr, Fim: _d.FimTr, Mov: Coalesce(_d.FimTr, _d.IniTr), Qtd: _d.QTr, Ref: _d.RefTr, Oper: _d.OpTr },
                    { ID: _d.ID, Ord: 4, Etapa: "Cobertura", Proc: "Cobertura", Local: "", Ini: _d.IniCob, Fim: _d.FimCob, Mov: Coalesce(_d.FimCob, _d.IniCob), Qtd: _d.QCob, Ref: _d.RefCob, Oper: _d.OpCob },
                    { ID: _d.ID, Ord: 5, Etapa: "Bandagem", Proc: "Bandagem", Local: "", Ini: _d.IniBand, Fim: _d.FimBand, Mov: Coalesce(_d.FimBand, _d.IniBand), Qtd: _d.QBand, Ref: Blank(), Oper: _d.OpBand },
                    { ID: _d.ID, Ord: 6, Etapa: "Vulcanização", Proc: "Vulcanização", Local: "", Ini: _d.IniVulc, Fim: _d.FimVulc, Mov: Coalesce(_d.FimVulc, _d.IniVulc), Qtd: _d.QVulc, Ref: Blank(), Oper: _d.OpVulc },
                    { ID: _d.ID, Ord: 7, Etapa: "Debandagem", Proc: "Debandagem", Local: "", Ini: _d.IniDeb, Fim: _d.FimDeb, Mov: Coalesce(_d.FimDeb, _d.IniDeb), Qtd: _d.QDeb, Ref: Blank(), Oper: _d.OpDeb },
                    { ID: _d.ID, Ord: 8, Etapa: "Extração", Proc: "Extr./Teste", Local: Coalesce(LookUp(fx_CabinesTeste As _ct, _ct.Posto = _d.Cabine).Rotulo, ""), Ini: _d.IniExt, Fim: _d.FimExt, Mov: Coalesce(_d.FimExt, _d.IniExt), Qtd: _d.QExt, Ref: Blank(), Oper: _d.OpExt }
                )
            }
        ),
        Linhas
    ),
    OperCurto,
    With(
        { _nm: Split(Trim(Oper), " ") },
        If(
            IsBlank(Trim(Oper)),
            "",
            Proper(First(_nm).Value & If(CountRows(_nm) > 1, " " & Last(_nm).Value, ""))
        )
    )
    )
);
Reset(gal_DetListaPnl);
Set(varDetAbertoPnl, true)
```

**`lbl_CronoTrPnl` → `Color`**

```powerfx
If(
    ThisItem.Estado = "PARADA",
    fx_CorPainelTextoErro,
    ThisItem.Estado = "PAUSA",
    fx_CorPainelTextoRotulo,
    ThisItem.Estado = "CIMENTO",
    fx_CorPainelTextoGelo,
    ThisItem.Produzindo && !IsBlank(ThisItem.AutonomiaMin),
    With(
        { _m: fx_AutonomiaAgora(ThisItem.AutonomiaMin, varSincPnl, ctxAgoraPnl) },
        If(
            _m >= 2 * fx_TurnoUtilMin, fx_CorPainelTextoOK,
            _m >= fx_TurnoUtilMin,     fx_CorPainelTextoAlerta,
            fx_CorPainelTextoErro
        )
    ),
    fx_CorPainelTexto
)
```

**`lbl_CronoTrPnl` → `Text`**

```powerfx
If(
    (ThisItem.Estado = "PARADA" || ThisItem.Estado = "PAUSA") && !IsBlank(ThisItem.InicioParada),
    fx_CronoLongo(ThisItem.InicioParada, ctxAgoraPnl),
    ThisItem.Estado = "CIMENTO",
    fx_CronoLongo(ThisItem.InicioCimento, ctxAgoraPnl),
    ThisItem.Produzindo && !IsBlank(ThisItem.AutonomiaMin),
    fx_AutonomiaTexto(fx_AutonomiaAgora(ThisItem.AutonomiaMin, varSincPnl, ctxAgoraPnl)),
    ThisItem.Produzindo,
    "—",
    ""
)
```

**`lbl_SubTrPnl` → `Color`**

```powerfx
If(
    ThisItem.Estado = "PARADA",   fx_CorPainelTextoErro,
    ThisItem.Estado = "COM FILA", fx_CorPainelTextoAlerta,
    ThisItem.Estado = "CIMENTO",  fx_CorPainelTextoGelo,
    fx_CorPainelTextoRotulo
)
```

**`lbl_SubTrPnl` → `Text`**

```powerfx
If(
    ThisItem.Estado = "PARADA" || ThisItem.Estado = "PAUSA",
    ThisItem.Motivo & If(ThisItem.Produzindo, "  ·  OP " & Text(ThisItem.OP, "[$-en-US]0"), ""),
    ThisItem.Estado = "CIMENTO",
    "CIMENTO  ·  OP " & Text(ThisItem.OP, "[$-en-US]0"),
    ThisItem.Produzindo,
    fx_Ou(ThisItem.Mangueira) & "  ·  OP " & Text(ThisItem.OP, "[$-en-US]0"),
    ThisItem.Estado = "COM FILA",
    "Sem OP, com fila",
    "Sem produção no turno"
)
```


## 4b. scr_HoraHora_Trancagem_2 (v0.7.3)

Os dois filtros sobre `colOpsTrancHHT` estão dentro de propriedades grandes; abaixo a propriedade inteira de cada dono, pronta para colar.

**`btn_CarregarHHT` → `OnSelect`** (propriedade inteira)

```powerfx
UpdateContext({ctxCarregandoHHT: true, ctxIniCargaHHT: Now()});
IfError(
    Concurrent(
        Refresh('Hora-Hora'),
        Refresh(ficha_producao),
        Refresh(DM_TRANÇAGEM),
        Refresh(DM_ENGRENAGENS)
    ),
    Notify("Não consegui atualizar os dados do servidor. O que aparece pode estar desatualizado — confira a rede e toque em Abrir de novo.", NotificationType.Warning, 10000)
);
With(
    {
        _agora: Now(),
        _tl: varTurnoHHT,
        _c: varCelulaHHT
    },
    With(
        {
            _t: fx_TurnoNum(_tl),
            _d: fx_DataRefHH(_agora, fx_TurnoNum(_tl))
        },
        UpdateContext(
            {
                ctxAgoraHHT: _agora,
                ctxTurnoCarregadoHHT: _t,
                ctxCelulaCarregadaHHT: _c,
                ctxDataCarregadaHHT: _d,
                ctxAlteradoHHT: false
            }
        );
        ClearCollect(
            colHHTurnoHHT,
            Filter(
                'Hora-Hora',
                Data = _d,
                Turno = _tl
            )
        );
        ClearCollect(
            colOpsTrancHHT,
            Filter(
                ficha_producao,
                processo = "Trançadeira",
                status_processo = "Em processo"
            )
        );
        ClearCollect(
            colSalvasHHT,
            Sort(
                Filter(
                    colHHTurnoHHT As _s,
                    _s.Célula = _c
                ),
                ID,
                SortOrder.Descending
            )
        );
        With(
            { _maq: fx_MaquinaEngrenagens(_c) },
            ClearCollect(
                colMangMaqHHT,
                Sort(
                    ShowColumns(
                        Filter(
                            AddColumns(
                                ShowColumns(
                                    Filter(
                                        DM_TRANÇAGEM,
                                        !IsBlank(PARTNUMBER) && !IsBlank(_2BRD_CODE)
                                    ),
                                    PARTNUMBER,
                                    _2BRD_CODE
                                ),
                                Mangueira,
                                PARTNUMBER,
                                Chave,
                                fx_MangCanon(PARTNUMBER),
                                MFG,
                                fx_VelocidadeComFallback(_maq, _2BRD_CODE, PARTNUMBER) /
                                    If(fx_DuasPassagens(_maq, _2BRD_CODE), 2, 1),
                                DP,
                                fx_DuasPassagens(_maq, _2BRD_CODE)
                            ),
                            MFG > 0
                        ),
                        Mangueira,
                        Chave,
                        MFG,
                        DP
                    ),
                    Mangueira
                )
            )
        );
        Collect(
            colMangMaqHHT,
            {
                Mangueira: fx_MotivoAmostra,
                Chave: fx_MangCanon(fx_MotivoAmostra),
                MFG: 0,
                DP: false
            }
        );
        With(
            {
                _ativa:
                    CountRows(
                        Filter(
                            colSalvasHHT As _a1,
                            Coalesce(_a1.'Real. Hora', 0) > 0 || !IsBlank(_a1.Mangueira)
                        )
                    ) > 0 ||
                    CountRows(
                        Filter(
                            colOpsTrancHHT As _a2,
                            (_a2.Trançadeira = _c && IsBlank(_a2.Cimento_Maquina)) || _a2.Cimento_Maquina = _c
                        )
                    ) > 0
            },
            ClearCollect(
                colLinhasHHT,
                ForAll(
                    Sort(
                        Filter(
                            fx_GradeHoraHora,
                            Turno = _t
                        ),
                        Ord
                    ) As _g,
                    With(
                        {
                            _r: LookUp(
                                colSalvasHHT As _x,
                                _x.Hora = _g.Hora
                            ),
                            _venc: fx_FaixaVencida(
                                _g.Fim,
                                _g.Turno,
                                _agora
                            )
                        },
                        With(
                            {
                                _mfg: Coalesce(
                                    LookUp(
                                        colMangMaqHHT As _v,
                                        _v.Chave = fx_MangCanon(Text(_r.Mangueira)),
                                        _v.MFG
                                    ),
                                    0
                                )
                            },
                            {
                                Ord: _g.Ord,
                                IDsp: Coalesce(
                                    _r.ID,
                                    0
                                ),
                                Hora: _g.Hora,
                                Rotulo: _g.Rotulo,
                                Minutos: _g.Minutos,
                                Fim: _g.Fim,
                                Vencida: _venc,
                                Ativa: _ativa,
                                Mangueira: Coalesce(
                                    Text(_r.Mangueira),
                                    ""
                                ),
                                MFG: _mfg,
                                DP: Coalesce(
                                    LookUp(
                                        colMangMaqHHT As _vd,
                                        _vd.Chave = fx_MangCanon(Text(_r.Mangueira)),
                                        _vd.DP
                                    ),
                                    false
                                ),
                                Fora: !IsBlank(Text(_r.Mangueira)) &&
                                    IsBlank(
                                        LookUp(
                                            colMangMaqHHT As _vf,
                                            _vf.Chave = fx_MangCanon(Text(_r.Mangueira))
                                        )
                                    ),
                                RCelula: _c,
                                RTurno: _tl,
                                RData: _d,
                                Meta: If(
                                    _mfg > 0,
                                    fx_MetaFaixa(
                                        _mfg,
                                        _g.Minutos
                                    ),
                                    Coalesce(
                                        _r.'Meta Hora',
                                        0
                                    )
                                ),
                                Real: Coalesce(
                                    _r.'Real. Hora',
                                    0
                                ),
                                TempoParado: Coalesce(
                                    _r.'Tempo Parado (min)',
                                    0
                                ),
                                Motivo: Coalesce(
                                    Text(_r.Motivo),
                                    ""
                                ),
                                Motivo2: Coalesce(
                                    Text(_r.'Motivo 2'),
                                    ""
                                ),
                                Comentario: Coalesce(
                                    Text(_r.'Comentário / Ação'),
                                    ""
                                )
                            }
                        )
                    )
                )
            )
        );
        ClearCollect(
            colResumoHHT,
            ForAll(
                fx_CelulasTrancagem As _cc,
                With(
                    {
                        _linhas: Filter(
                            colHHTurnoHHT As _h,
                            _h.Célula = _cc.Celula
                        )
                    },
                    With(
                        {
                            _ativaC:
                                CountRows(
                                    Filter(
                                        _linhas As _b1,
                                        Coalesce(_b1.'Real. Hora', 0) > 0 || !IsBlank(_b1.Mangueira)
                                    )
                                ) > 0 ||
                                CountRows(
                                    Filter(
                                        colOpsTrancHHT As _b2,
                                        (_b2.Trançadeira = _cc.Celula && IsBlank(_b2.Cimento_Maquina)) || _b2.Cimento_Maquina = _cc.Celula
                                    )
                                ) > 0
                        },
                        With(
                            {
                                _diag: ForAll(
                                    Filter(
                                        fx_GradeHoraHora,
                                        Turno = _t
                                    ) As _g2,
                                    With(
                                        {
                                            _r2: First(
                                                Sort(
                                                    Filter(
                                                        _linhas As _h2,
                                                        _h2.Hora = _g2.Hora
                                                    ),
                                                    ID,
                                                    SortOrder.Descending
                                                )
                                            )
                                        },
                                        {
                                            P: fx_PendenciaMaqHH(
                                                _ativaC,
                                                fx_FaixaVencida(
                                                    _g2.Fim,
                                                    _t,
                                                    _agora
                                                ),
                                                Coalesce(
                                                    Text(_r2.Mangueira),
                                                    ""
                                                ),
                                                Coalesce(
                                                    _r2.'Meta Hora',
                                                    0
                                                ),
                                                Coalesce(
                                                    _r2.'Real. Hora',
                                                    0
                                                ),
                                                Coalesce(
                                                    Text(_r2.Motivo),
                                                    ""
                                                )
                                            )
                                        }
                                    )
                                )
                            },
                            {
                                Celula: _cc.Celula,
                                Ativa: _ativaC,
                                SemApontar: CountRows(
                                    Filter(
                                        _diag As _d1,
                                        _d1.P = "SEM_APONTAMENTO"
                                    )
                                ),
                                SemMotivo: CountRows(
                                    Filter(
                                        _diag As _d2,
                                        _d2.P = "SEM_MOTIVO"
                                    )
                                )
                            }
                        )
                    )
                )
            )
        );
        Reset(cmb_MotivoSemProdHHT);
        ClearCollect(colFalhasHHT, { fRotulo: "", fMsg: "" });
        Clear(colFalhasHHT);
        If(
            CountRows(colSalvasHHT) > CountRows(Distinct(colSalvasHHT, Hora)),
            Notify(
                "ATENÇÃO: esta máquina tem " &
                Text(CountRows(colSalvasHHT) - CountRows(Distinct(colSalvasHHT, Hora))) &
                " registro(s) duplicado(s) neste turno. O placar vai mentir até a lista ser limpa — avise o desenvolvimento.",
                NotificationType.Error,
                20000
            )
        );
        UpdateContext({ctxCarregandoHHT: false})
    )
)
```

**`lbl_VersaoHHT` → `Text`**

```powerfx
"Versão 0.7.3"
```


## 5. Controles com posição ou tamanho mexidos (X/Y/Width/Height)

| Controle | Antes | Depois | Motivo |
|---|---|---|---|
| `lbl_RotSituacaoTr3_1` | sem Width | Width 170 | cabeça "SITUAÇÃO · 00:12" com o cronômetro do cimento |
| `lbl_VersaoHHT` (Hora-Hora) | texto 0.7.2 | texto 0.7.3 | só rótulo de versão |
| `lbl_ValSituacaoTr3_1` | sem Width | Width 170 | caber "Aplicando cimento" |
| `btn_SalvarTr3_1` | X 560 · W 230 | X 560 · W 230 normal; X 800 · W 140 só quando o botão de cimento aparece | abrir espaço no rodapé |
| `btn_EnviarTr3_1` | X 810 · W 290 | X 810 · W 290 normal; X 950 · W 180 só quando o botão de cimento aparece | idem |

Novos (posição própria): `btn_SoCimentoFilaTr3_1` (X 122 · Y 66 · 84×26, no template da galeria), `btn_CimentoTr3_1` (X 556 · Y 700 · W 236), `btn_EnviarCimentoTr3_1` (X 810 · Y 700 · W 290, mesmo lugar do Enviar normal; os dois nunca aparecem juntos). Nenhum outro X/Y/Width/Height foi alterado.

## 6. Como fica o fluxo

- **TH05, OP com cimento, trança própria:** PRODUZINDO → botão "Terminar trança → aplicar cimento" grava `InicioCimento_Trancagem` + evento `<ID>-Trancagem-Cimento-Inicio`; o cabeçalho passa a "Aplicando cimento" com cronômetro; o Enviar normal continua e grava `FimCimento_Trancagem` (sem evento de fim: o BI conta tipo "Fim" como Trançagem).
- **TM04 (≠ TH05), OP com cimento:** o Enviar vira "Enviar para cimento na TH05"; grava a trança como hoje, mas `processo` fica "Trançadeira", `status_processo` "Aguardando", `Cimento_Maquina` = "TH05", `InicioAguardando_Trançadeira` = agora, não grava `InicioAguardandoCobertura` e não mexe nos carretéis (Saída fica).
- **TH05, OP "SÓ CIMENTO":** botão "Iniciar cimento" (sem modal de delineamento nem carretel) → status "Em processo" + `InicioCimento_Trancagem`; campos travados; "Enviar para Cobertura" grava processo "Cobertura", status "Aguardando", `FimCimento_Trancagem`, `InicioAguardandoCobertura`, Entrada = Saída, Saída em branco, (sem evento de fim; o fim fica em `FimCimento_Trancagem`).
- **Cancelar OP** fica escondido na OP só cimento (cancelar devolveria o tubo e a OP ao plano; quem cancela é a TM04 ou a supervisão pelo Editar OP).

## 7. Riscos e conferências para o Studio

1. `fx_PrecisaCimento` lê `DM_TRANÇAGEM` dentro de UDF (exceção à regra 4 do cabeçalho do `Formulas.txt`, comentada lá) e o `LookUp` não é delegável: vale para as linhas que o conector devolve. Se a tabela passar do limite de linhas do app, a mangueira pode não achar o delineamento.
2. O filtro da fila usa `IsBlank(Cimento_Maquina)` dentro do `Filter` externo; confirme que o Studio não acusa aviso de delegação.
3. Só o evento `-Trancagem-Cimento-Inicio` (tipo Início, sem `metros`) é gravado. Não há evento Cimento-Fim: a medida "Eventos Apontados" contaria a Trançagem duas vezes.
4. O Enviar da TH05 com cimento obrigatório não é bloqueado se o operador pular o botão de cimento (o spec pediu o Enviar normal igual). Nessa hora `FimCimento_Trancagem` fica em branco.
5. No Enviar da OP só cimento, se a OP estiver sem `Carretel Saida` o app avisa e não grava (guarda a mais, para não zerar o carretel de Entrada).
6. Máquina ativa da Hora-Hora: a TH05 fica ativa durante o cimento e a TM04 deixa de ficar (filtro `(X.Trançadeira = C && IsBlank(X.Cimento_Maquina)) || X.Cimento_Maquina = C` no `btn_RecarregarTr3_1` e nos dois filtros de `colOpsTrancHHT` da Hora-Hora Trançagem). AM-DM-02 e o andon do Painel que olha `colAguardPnl` fora do posto não foram mexidos.
7. O texto "CIMENTO  ·  OP n" no posto do Painel foi escolhido curto para caber nos 162 px; "APLICANDO CIMENTO" aparece no detalhe e na Trançagem.
8. Lembrete (memória do William): isto muda só o app. O packlist/ProdHose e o BI não sabem do cimento.
