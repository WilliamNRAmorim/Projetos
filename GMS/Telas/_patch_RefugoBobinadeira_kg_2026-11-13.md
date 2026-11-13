# Patch de 13/11/2026: refugo de fio em kg, vírgula e ponto sempre decimal (scr_RefugoBobinadeira_1 v0.4.3)

Pedido do William: 0,8 e 0.8 têm que ser 800 g. A `fx_Num` lia separador + 3 dígitos como milhar, então "0,800" e "0.800" gravavam 800 kg. A tela passa a usar `fx_NumKg` (vírgula e ponto sempre decimal; dois separadores ou lixo deixam o campo vermelho), mostra ao lado do título do campo como o número foi lido ("= 0,8 kg = 800 g") e bloqueia acima de 100 kg (o maior lançamento do histórico é 70,3 kg). De quebra: a lista recarrega sozinha na virada do dia, o aviso de sucesso sai com vírgula, a zebra da galeria segue a posição e dois valores fixos viraram token.

Histórico conferido em 13/11 (1.330 lançamentos, 0,7 a 70,3 kg): nenhum valor inflado pela regra de milhar.

## Ordem

1. Colar o `Telas/Formulas.txt` inteiro (v3.0.19) no App.Formulas. Ele já inclui a v3.0.18 do cimento.
2. Criar o controle novo `lbl_LeituraQtdBob` (seção A), na tela, depois do `inp_QtdBob`.
3. Colar cada propriedade da seção B por cima da atual, na barra de fórmulas. Nenhum controle existente muda de lugar.
4. Publicar e testar no tablet: digitar 0,8 · 0.8 · 0,800 · 1.234,5 · 150.

Testes da regra: "0,8", "0.8", "0,800", "0.800" = 0,8 kg · "12" = 12 · "3,6" e "3.6" = 3,6 · ",5" = 0,5 · "1,250" = 1,25 · "1.234,5", "8," e "abc" = inválido.

## A. Controle novo: lbl_LeituraQtdBob

```yaml
- lbl_LeituraQtdBob:
    Control: Label@2.5.1
    Properties:
      Align: =Align.Right
      Color: |-
        =If(
            fx_NumKg(inp_QtdBob.Text) > 0 && fx_NumKg(inp_QtdBob.Text) <= fx_RefugoFioMaxKg,
            fx_CorTextoSuave,
            fx_CorErro
        )
      Font: =fx_FonteFamilia
      FontWeight: =FontWeight.Semibold
      Height: =18
      Size: =fx_FonteApoio
      Text: |-
        =With(
            {_kg: fx_NumKg(inp_QtdBob.Text)},
            If(
                IsBlank(Trim(inp_QtdBob.Text)), "",
                IsBlank(_kg) || _kg <= 0, "número inválido",
                _kg > fx_RefugoFioMaxKg, "acima de " & fx_RefugoFioMaxKg & " kg: confira",
                "= " & fx_KgTexto(_kg)
            )
        )
      Width: =200
      X: =225
      Y: =444
```

## B. Propriedades alteradas

### tmr_RelogioBob · OnTimerEnd

```
=UpdateContext({ctxAgora: Now()});
If(
    fx_JanelaInicioEm(ctxAgora) <> ctxIniBob,
    UpdateContext({
        ctxIniBob: fx_JanelaInicioEm(ctxAgora),
        ctxFimBob: fx_JanelaFimEm(ctxAgora)
    });
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

### lbl_TituloBob · Font

```
=fx_FonteFamilia
```

### lbl_RotQtdBob · Text

```
="QUANTIDADE REFUGADA (kg) *"
```

### inp_QtdBob · BorderColor

```
=If(fx_NumKg(Self.Text) > 0 && fx_NumKg(Self.Text) <= fx_RefugoFioMaxKg, fx_CorBorda, fx_CorErro)
```

### inp_QtdBob · HintText

```
="Em kg · ex: 0,8 (800 g)"
```

### lbl_TituloTabelaBob · Text

```
="REGISTROS DE " & Text(fx_DataRefEm(ctxAgora), "dd/mm") & "  ·  " & CountRows(colRefugoBob) & " registros  ·  " &
Text(Sum(colRefugoBob, QuantidadeRefugo), "[$-pt-BR]#.##0,0##", "pt-BR") & " kg refugados"
```

### gal_RegistrosBob · TemplateFill

```
=If(Mod(CountRows(Filter(colRefugoBob, DataHoraRefugo > ThisItem.DataHoraRefugo)), 2) = 1, fx_CorFundo, fx_CorSuperficie)
```

### lbl_RowOperadorBob · Size

```
=fx_FonteApoio
```

### lbl_RowQtdBob · Text

```
=Text(ThisItem.QuantidadeRefugo, "[$-pt-BR]#.##0,0##", "pt-BR")
```

### btn_RegistrarBob · DisplayMode

```
=If(
    !varProcessando &&
    !IsBlank(cmb_OperadorBob.Selected.Nome) &&
    !IsBlank(cmb_MaquinaBob.Selected.Value) &&
    !IsBlank(cmb_FioBob.Selected.Value) &&
    !IsBlank(cmb_MotivoBob.Selected.Value) &&
    fx_NumKg(inp_QtdBob.Text) > 0 &&
    fx_NumKg(inp_QtdBob.Text) <= fx_RefugoFioMaxKg,
    DisplayMode.Edit,
    DisplayMode.Disabled
)
```

### btn_RegistrarBob · OnSelect

```
=Set(varProcessando, true);
With(
    {
        _agora: Now(),
        _qtd: Coalesce(fx_NumKg(inp_QtdBob.Text), 0),
        _operador: cmb_OperadorBob.Selected.Nome,
        _maquina: cmb_MaquinaBob.Selected.Value,
        _fio: cmb_FioBob.Selected.Value,
        _motivo: cmb_MotivoBob.Selected.Value
    },
    If(
        IsBlank(_operador) || IsBlank(_maquina) || IsBlank(_fio) || IsBlank(_motivo),
        Notify("Preencha operador, máquina, fio e motivo antes de registrar.", NotificationType.Warning, 6000);
        Set(varProcessando, false),
        _qtd <= 0,
        Notify("Quantidade inválida. Digite o peso em kg, com vírgula ou ponto: 0,8 = 800 g.", NotificationType.Warning, 6000);
        Set(varProcessando, false),
        _qtd > fx_RefugoFioMaxKg,
        Notify("Acima de " & fx_RefugoFioMaxKg & " kg. Confira: o peso é em kg (0,8 = 800 g).", NotificationType.Warning, 8000);
        Set(varProcessando, false),
        Patch(
            Refugo_Bobinadeira,
            Defaults(Refugo_Bobinadeira),
            {
                Title: Text(_agora, "yyyymmddhhmmss"),
                DataHoraRefugo: _agora,
                Operador: _operador,
                Maquina: _maquina,
                CodigoFio: _fio,
                Motivos: _motivo,
                QuantidadeRefugo: _qtd,
                Observacao: inp_ObsBob.Text,
                Turno: fx_TurnoEm(_agora)
            }
        );
        If(
            !IsEmpty(Errors(Refugo_Bobinadeira)),
            Notify("Falha ao registrar o refugo: " & First(Errors(Refugo_Bobinadeira)).Message, NotificationType.Error, 10000);
            Set(varProcessando, false),
            Reset(cmb_FioBob);
            Reset(cmb_MotivoBob);
            Reset(inp_QtdBob);
            Reset(inp_ObsBob);
            UpdateContext({ctxAgora: Now()});
            UpdateContext({
                ctxIniBob: fx_JanelaInicioEm(ctxAgora),
                ctxFimBob: fx_JanelaFimEm(ctxAgora)
            });
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
            );
            Set(varProcessando, false);
            Notify("Refugo de " & fx_KgTexto(_qtd) & " registrado em " & _maquina & ".", NotificationType.Success, 4000)
        )
    )
)
```

### lbl_VersaoBob · Text

```
="Versão 0.4.3"
```
