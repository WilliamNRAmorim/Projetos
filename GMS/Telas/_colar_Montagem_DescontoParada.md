# Colar: Montagem Hora-Hora — desconto de parada só do próprio lançamento

Tela `scr_Montagem_HoraHora`. Origem: 26/11, OT 30959679 (AXE40579-BRA1) rodou duas vezes no 1º turno e os dois lançamentos descontaram os mesmos 36 min de parada; a lista mostrava só 21 min.

**Causa:** o desconto somava todas as paradas com a mesma chave `PN (OT n)` dos últimos 2 dias, de qualquer turno, sem olhar se a parada aconteceu dentro do período daquele lançamento. OT que roda duas vezes (ou que rodou ontem) herdava as paradas da outra vez.

**Correção:** só desconta a parada registrada entre o início e o fim daquele lançamento (`RegistradoEm >= InicioEm`, e `<= FimEm` ao finalizar). Como o dropdown de OP só mostra OP em andamento, toda parada vinculada nasce dentro desse intervalo.

Base: o código que está publicado no Studio em 26/11 (colado pelo William). Nenhum controle teve X, Y, Width ou Height alterado. A `colDescM` continua sendo montada no OnVisible, timer, atualizar, registrar parada e faixa de turno, mas deixa de ser usada (limpeza fica para depois).

## Passo a passo

1. Colar cada fórmula abaixo na barra de fórmulas do controle e da propriedade indicados (substitui a fórmula inteira).
2. Conferir que não ficou sublinhado vermelho.
3. Publicar.

## Roteiro de teste

1. Iniciar uma OT, registrar parada de 5 min vinculada a ela. REAL. mostra `bruto − 5` com `*`.
2. Finalizar e iniciar de novo a MESMA OT. O lançamento novo começa sem desconto (sem `*`).
3. Registrar parada de 3 min vinculada à OT nova. O lançamento novo desconta só 3; o antigo continua com 5.
4. Parada com motivo TE não desconta.
5. Lançamento de outro turno aparece com `· 3º Turno` depois do P/N; do turno atual, só o P/N.

Lançamentos já finalizados guardam o `DescontoMin` antigo e não mudam com este patch.

## Fórmulas

### 1. lbl_prow_pn_m_1 → Text

```powerfx
=ThisItem.PN &
 If(ThisItem.Data <> varDataTela || ThisItem.Turno <> varTurnoTela,
    "  · " & ThisItem.Turno, "")
```

### 2. lbl_prow_real_m_1 → Color

```powerfx
=With(
    {
        _real: If(ThisItem.Status = "EmAndamento",
            Max(
                DateDiff(ThisItem.InicioEm, varAgora, TimeUnit.Minutes) -
                Coalesce(
                    Sum(
                        Filter(colParadasM,
                            OPVinculada = ThisItem.PN & " (OT " & Text(ThisItem.OT, "[$-en-US]0") & ")" &&
                            Motivo <> "TE - Tempo Excedido" &&
                            RegistradoEm >= ThisItem.InicioEm
                        ),
                        TempoParadoMin
                    ),
                    0
                ),
                0
            ),
            Coalesce(ThisItem.DuracaoRealMin, ThisItem.DuracaoMin)),
        _meta: With(
            {_t: LookUp(Tempos, Material = Upper(Trim(ThisItem.PN))).TempoMinPc},
            If(Coalesce(_t, 0) <= 0, -1, ThisItem.QtdOT * _t)
        )
    },
    If(_meta > 0 && _real > _meta,
        ColorFade(fx_CorAlerta, -30%),
        fx_CorTexto
    )
)
```

### 3. lbl_prow_real_m_1 → Text

```powerfx
=With(
    {
        _desc: If(ThisItem.Status = "EmAndamento",
            Coalesce(
                Sum(
                    Filter(colParadasM,
                        OPVinculada = ThisItem.PN & " (OT " & Text(ThisItem.OT, "[$-en-US]0") & ")" &&
                        Motivo <> "TE - Tempo Excedido" &&
                        RegistradoEm >= ThisItem.InicioEm
                    ),
                    TempoParadoMin
                ),
                0
            ),
            Coalesce(ThisItem.DescontoMin, 0))
    },
    With(
        {
            _real: If(ThisItem.Status = "EmAndamento",
                Max(DateDiff(ThisItem.InicioEm, varAgora, TimeUnit.Minutes) - _desc, 0),
                Coalesce(ThisItem.DuracaoRealMin, ThisItem.DuracaoMin))
        },
        Text(_real, "0") & " min" & If(_desc > 0, "*", "")
    )
)
```

### 4. lbl_prow_real_m_1 → Tooltip

```powerfx
=With(
    {
        _bruto: If(ThisItem.Status = "EmAndamento",
            DateDiff(ThisItem.InicioEm, varAgora, TimeUnit.Minutes),
            ThisItem.DuracaoMin),
        _desc: If(ThisItem.Status = "EmAndamento",
            Coalesce(
                Sum(
                    Filter(colParadasM,
                        OPVinculada = ThisItem.PN & " (OT " & Text(ThisItem.OT, "[$-en-US]0") & ")" &&
                        Motivo <> "TE - Tempo Excedido" &&
                        RegistradoEm >= ThisItem.InicioEm
                    ),
                    TempoParadoMin
                ),
                0
            ),
            Coalesce(ThisItem.DescontoMin, 0))
    },
    If(_desc <= 0,
        "Tempo real: " & Text(_bruto, "0") & " min",
        "Bruto " & Text(_bruto, "0") & " min - " & Text(_desc, "0") &
        " min de paradas vinculadas = " & Text(Max(_bruto - _desc, 0), "0") & " min"
    )
)
```

### 5. lbl_prow_meta_m_1 → Color

```powerfx
=With(
    {
        _real: If(ThisItem.Status = "EmAndamento",
            Max(
                DateDiff(ThisItem.InicioEm, varAgora, TimeUnit.Minutes) -
                Coalesce(
                    Sum(
                        Filter(colParadasM,
                            OPVinculada = ThisItem.PN & " (OT " & Text(ThisItem.OT, "[$-en-US]0") & ")" &&
                            Motivo <> "TE - Tempo Excedido" &&
                            RegistradoEm >= ThisItem.InicioEm
                        ),
                        TempoParadoMin
                    ),
                    0
                ),
                0
            ),
            Coalesce(ThisItem.DuracaoRealMin, ThisItem.DuracaoMin)),
        _meta: With(
            {_t: LookUp(Tempos, Material = Upper(Trim(ThisItem.PN))).TempoMinPc},
            If(Coalesce(_t, 0) <= 0, -1, ThisItem.QtdOT * _t)
        )
    },
    If(_meta > 0 && _real > _meta,
        ColorFade(fx_CorAlerta, -30%),
        fx_CorTexto
    )
)
```

### 6. btn_prow_finalizar_m_1 → OnSelect

Também relê as paradas do servidor antes de calcular, para pegar parada lançada há menos de 30 s ou em outro tablet.

```powerfx
=Set(varPNAtivo, ThisItem);
Refresh(Paradas_Montagem);
ClearCollect(colParadasM,
    Filter(Paradas_Montagem,
        Celula = varCelulaMontagem &&
        Data >= DateAdd(varDataTela, -2, TimeUnit.Days)
    )
);
With(
    {
        _t: Coalesce(LookUp(Tempos, Material = Upper(Trim(ThisItem.PN))).TempoMinPc, 0),
        _bruto: RoundDown(DateDiff(ThisItem.InicioEm, Now(), TimeUnit.Minutes), 0),
        _desc: Coalesce(
            Sum(
                Filter(colParadasM,
                    OPVinculada = ThisItem.PN & " (OT " & Text(ThisItem.OT, "[$-en-US]0") & ")" &&
                    Motivo <> "TE - Tempo Excedido" &&
                    RegistradoEm >= ThisItem.InicioEm
                ),
                TempoParadoMin
            ),
            0
        )
    },
    Set(varBrutoPop, _bruto);
    Set(varDescontoPop, _desc);
    Set(varDuracaoPop, Max(_bruto - _desc, 0));
    Set(varMetaPop, If(_t <= 0, -1, RoundDown(ThisItem.QtdOT * _t, 0)));
    UpdateContext({
        ctxPopExcesso: _t > 0 &&
            Max(_bruto - _desc, 0) > RoundDown(ThisItem.QtdOT * _t, 0)
    })
);
Reset(txt_pop_qtd_m_1);
Reset(txt_pop_obs_m_1);
Set(varPopupFinalizar_M, true)
```

### 7. btn_pop_confirmar_m_1 → OnSelect

```powerfx
=Set(varProcM, true);
Set(varFimM, Now());
Set(varDuracaoFim, RoundDown(DateDiff(varPNAtivo.InicioEm, varFimM, TimeUnit.Minutes), 0));
Set(varDescontoFim,
    Coalesce(
        Sum(
            Filter(colParadasM,
                OPVinculada = varPNAtivo.PN & " (OT " & Text(varPNAtivo.OT, "[$-en-US]0") & ")" &&
                Motivo <> "TE - Tempo Excedido" &&
                RegistradoEm >= varPNAtivo.InicioEm &&
                RegistradoEm <= varFimM
            ),
            TempoParadoMin
        ),
        0
    )
);
Set(varLiquidoFim, Max(varDuracaoFim - varDescontoFim, 0));
Set(varMetaFim,
    With(
        {_t: LookUp(Tempos, Material = Upper(Trim(varPNAtivo.PN))).TempoMinPc},
        If(Coalesce(_t, 0) <= 0, 0, RoundDown(varPNAtivo.QtdOT * _t, 0))
    )
);
Set(varObsFim, Trim(txt_pop_obs_m_1.Text));
Patch(Producao_Montagem, varPNAtivo,
    {
        FimEm: varFimM,
        QtdProduzida: Value(txt_pop_qtd_m_1.Text),
        DuracaoMin: varDuracaoFim,
        DuracaoSeg: DateDiff(varPNAtivo.InicioEm, varFimM, TimeUnit.Seconds),
        DescontoMin: varDescontoFim,
        DuracaoRealMin: varLiquidoFim,
        Status: "Finalizado"
    }
);
If(!IsEmpty(Errors(Producao_Montagem)),
    Notify("Erro: " & First(Errors(Producao_Montagem)).Message, NotificationType.Error, 10000);
    Set(varProcM, false),
    If(ctxPopExcesso,
        Patch(Paradas_Montagem, Defaults(Paradas_Montagem),
            {
                Title: Text(varDataTela, "dd/mm/yyyy") & " - " & varTurnoTela & " - " & varCelulaMontagem,
                Data: varDataTela,
                Turno: varTurnoTela,
                Celula: varCelulaMontagem,
                RegistradoEm: Now(),
                Motivo: "TE - Tempo Excedido",
                TempoParadoMin: Max(varLiquidoFim - varMetaFim, 0),
                Observacao: varObsFim,
                OPVinculada: varPNAtivo.PN & " (OT " & Text(varPNAtivo.OT, "[$-en-US]0") & ")"
            }
        );
        If(!IsEmpty(Errors(Paradas_Montagem)),
            Notify("OP finalizada, mas a parada NÃO gravou: " & First(Errors(Paradas_Montagem)).Message, NotificationType.Error, 10000)
        )
    );
    Reset(txt_pop_qtd_m_1);
    Reset(txt_pop_obs_m_1);
    Set(varPopupFinalizar_M, false);
    Set(varPNAtivo, Blank());
    UpdateContext({ctxPopExcesso: false});
    Set(varAgora, Now());
    Concurrent(
        Refresh(Producao_Montagem),
        Refresh(Paradas_Montagem)
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
                    Motivo <> "TE - Tempo Excedido" && !IsBlank(OPVinculada)
                ),
                OPVinculada
            ) As d,
            {
                Chave: d.Value,
                MinDesc: Sum(
                    Filter(colParadasM,
                        OPVinculada = d.Value && Motivo <> "TE - Tempo Excedido"
                    ),
                    TempoParadoMin
                )
            }
        )
    );
    Set(varProcM, false);
    Notify("Produção finalizada!", NotificationType.Success, 2500)
)
```
