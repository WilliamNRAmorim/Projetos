# Patch de 06/11/2026: Refugo de fio aceita vírgula e ponto (scr_RefugoBobinadeira_1)

Problema (vídeo de 06/11): no campo "Quantidade refugada", digitar "3." vira "3" e "3.6" vira "36". Causa: `Format: TextFormat.Number` descarta o separador antes de a fórmula ler, e `Value()` sem cultura lê conforme o aparelho. A v0.4.0 de 06/10 já tinha a correção, mas a tela publicada voltou à versão antiga (commit 9bb0f44).

Padrão igual ao da cabine e do mandril: campo em texto, leitura por `fx_Num` (vírgula e ponto valem igual) e `fx_EhNum` para validar.

Ordem: colar cada propriedade inteira no Studio, na barra de fórmulas, por cima da atual. Nenhum controle muda de lugar. Depois publicar.

## 1. scr_RefugoBobinadeira_1 · inp_QtdBob · Format

```
=TextFormat.Text
```

## 2. scr_RefugoBobinadeira_1 · inp_QtdBob · BorderColor

```
=If(fx_EhNum(Self.Text) && fx_Num(Self.Text) > 0, fx_CorBorda, fx_CorErro)
```

## 3. scr_RefugoBobinadeira_1 · btn_RegistrarBob · DisplayMode

```
=If(
    !varProcessando &&
    !IsBlank(cmb_OperadorBob.Selected.Nome) &&
    !IsBlank(cmb_MaquinaBob.Selected.Value) &&
    !IsBlank(cmb_FioBob.Selected.Value) &&
    !IsBlank(cmb_MotivoBob.Selected.Value) &&
    fx_EhNum(inp_QtdBob.Text) &&
    fx_Num(inp_QtdBob.Text) > 0,
    DisplayMode.Edit,
    DisplayMode.Disabled
)
```

## 4. scr_RefugoBobinadeira_1 · btn_RegistrarBob · OnSelect

Única mudança: `_qtd` passa a ser `Coalesce(fx_Num(inp_QtdBob.Text), 0)`.

```
=Set(varProcessando, true);
With(
    {
        _agora: Now(),
        _qtd: Coalesce(fx_Num(inp_QtdBob.Text), 0),
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
        Notify("A quantidade refugada precisa ser maior que zero.", NotificationType.Warning, 6000);
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
            Notify("Refugo de " & _qtd & " registrado em " & _maquina & ".", NotificationType.Success, 4000)
        )
    )
)
```

## Teste no tablet depois de publicar

Digitar `3,6`, `3.6` e `36`: devem gravar 3,6 / 3,6 / 36. Texto como `abc` deixa a borda vermelha e o Registrar desabilitado.

O arquivo `Telas/scr_RefugoBobinadeira_1.txt` já foi regravado com as mesmas 4 propriedades.
