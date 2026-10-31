# Patch · scr_PainelMontagem v0.2.0 → v0.2.1 · carga que não depende do filtro por Data no servidor (27/10/2026)

Causa: pelo rodapé de diagnóstico, a carga trazia 7 OTs (as EmAndamento) e 0 paradas / 0 fechadas: o `Filter(..., Data >= ...)` direto no SharePoint voltava vazio. Agora a carga busca as 2000 linhas mais novas por ID (ordenação por ID é delegável) e corta por Data localmente. Os KPIs de soma vazia mostram 0 em vez de ficar em branco; as galerias vazias da ficha somem; 'sem meta' sem a palavra 'meta' repetida. Cole cada propriedade inteira, sem o `=` inicial.

**`btn_RecarregarMon` · OnSelect**

```
With(
    { _agora: Now() },
    With(
        { _dia: fx_DataRefEm(_agora) },
        UpdateContext({ ctxFalhaMon: false, ctxModoMon: "VIVO", ctxDiaMon: _dia, ctxHoraMon: 1, ctxAgoraMon: _agora, ctxToqueMon: _agora });
        // Atualiza o cache do conector. Ramos fechados: valor "; true", falha "; false" (mesmo tipo).
        IfError(
            Refresh(Producao_Montagem);
            Refresh(Paradas_Montagem);
            true,
            UpdateContext({ ctxFalhaMon: true });
            false
        );
        // 3 consultas DELEGAVEIS, em paralelo. Sem Search, sem "in", sem ShowColumns.
        // colAbertasMon pega a OT esquecida de dias anteriores; colDiaMon pega o dia produtivo (fechadas).
        IfError(
            Concurrent(
                ClearCollect(colAbertasMon, Filter(Producao_Montagem, Status = "EmAndamento")),
                // v0.2.1: as OTs/paradas MAIS NOVAS por ID (ordenacao por ID e delegavel) e o corte por Data e LOCAL.
                // O Filter por Data direto no SharePoint voltou 0 linhas na TV (27/10); isto funciona nos dois casos.
                ClearCollect(colDiaMon, Filter(FirstN(SortByColumns(Producao_Montagem, "ID", SortOrder.Descending), 2000) As _pd, _pd.Data >= _dia)),
                ClearCollect(colParMon, Filter(FirstN(SortByColumns(Paradas_Montagem, "ID", SortOrder.Descending), 2000) As _pp, _pp.Data >= DateAdd(_dia, -2, TimeUnit.Days)))
            );
            true,
            UpdateContext({ ctxFalhaMon: true });
            false
        );
        // Uniao LOCAL (sem rede): aberta de qualquer dia + o dia produtivo, sem repetir a mesma OT.
        ClearCollect(colProdMon, colAbertasMon);
        Collect(colProdMon, Filter(colDiaMon As _d, IsBlank(LookUp(colAbertasMon As _a, _a.ID = _d.ID))));
        UpdateContext({
            ctxTruncMon: CountRows(colAbertasMon) >= fx_PainelLinhasAlerta || CountRows(colDiaMon) >= fx_PainelLinhasAlerta || CountRows(colParMon) >= fx_PainelLinhasAlerta,
            ctxCarregouMon: true,
            ctxSincMon: _agora,
            ctxUltOkMon: If(ctxFalhaMon, ctxUltOkMon, _agora)
        });
        Select(btn_CalcMon)
    )
)
```

**`btn_HistMon` · OnSelect**

```
With(
    { _d: ctxDiaMon },
    // Historico: as mesmas 2 listas, Data entre D-2 e D, UMA vez por escolha. Sem timer de carga, sem Refresh.
    UpdateContext({ ctxFalhaMon: false });
    IfError(
        Concurrent(
            // v0.2.1: mais novas por ID (delegavel) e corte por Data LOCAL (ver btn_RecarregarMon).
            ClearCollect(colProdMon, Filter(FirstN(SortByColumns(Producao_Montagem, "ID", SortOrder.Descending), 2000) As _pd, _pd.Data >= DateAdd(_d, -2, TimeUnit.Days) && _pd.Data <= _d)),
            ClearCollect(colParMon, Filter(FirstN(SortByColumns(Paradas_Montagem, "ID", SortOrder.Descending), 2000) As _pp, _pp.Data >= DateAdd(_d, -2, TimeUnit.Days) && _pp.Data <= _d))
        );
        true,
        UpdateContext({ ctxFalhaMon: true });
        false
    );
    UpdateContext({
        ctxTruncMon: CountRows(colProdMon) >= fx_PainelLinhasAlerta || CountRows(colParMon) >= fx_PainelLinhasAlerta,
        ctxCarregouMon: true,
        ctxSincMon: ctxAgoraMon
    });
    Select(btn_CalcMon)
)
```

**`lbl_KpiValMon3` · Text**

```
If(!ctxCarregouMon || ctxFalhaMon, "—", With({ _v: Sum(colEstMon, Pecas) }, If(IsBlank(_v), "0", Text(_v, "[$-en-US]0")) & " pç"))
```

**`lbl_KpiValMon5` · Text**

```
If(!ctxCarregouMon || ctxFalhaMon, "—", With({ _v: Sum(colEstMon, ParadaReal) }, If(IsBlank(_v), "0", Text(_v, "[$-en-US]0")) & " min"))
```

**`lbl_KpiValMon6` · Text**

```
If(!ctxCarregouMon || ctxFalhaMon, "—", With({ _v: Sum(colEstMon, Excedido) }, If(IsBlank(_v), "0", Text(_v, "[$-en-US]0")) & " min"))
```

**`lbl_FichaOTRealMon` · Text**

```
With(
    { _s: LookUp(colEstMon As _e, _e.Celula = ctxFichaMon) },
    If(
        (ctxModoMon = "VIVO" || ctxModoMon = "HORA") && _s.Abertas > 0,
        "Real " & Text(_s.RealMin, "[$-en-US]0") & " min  ·  " &
        If(_s.MetaMin > 0, "meta " & Text(_s.MetaMin, "[$-en-US]0") & " min", "sem meta") &
        If(_s.Excede, "  ·  +" & Text(_s.RealMin - _s.MetaMin, "[$-en-US]0") & " min acima", ""),
        ""
    )
)
```

**`lbl_FichaParValMon` · Text**

```
With({ _v: Sum(Filter(colFichaParMon, Tag = "PARADA"), TempoParadoMin) }, If(IsBlank(_v), "0", Text(_v, "[$-en-US]0")) & " min")
```

**`lbl_FichaTeValMon` · Text**

```
With({ _v: Sum(Filter(colFichaParMon, Tag = "TE"), TempoParadoMin) }, If(IsBlank(_v), "0", Text(_v, "[$-en-US]0")) & " min")
```

**`gal_FichaFechMon` · Visible**

```
ctxFichaAbertaMon && !IsEmpty(colFichaFechMon)
```

**`gal_FichaParMon` · Visible**

```
ctxFichaAbertaMon && !IsEmpty(colFichaParMon)
```

**`lbl_VersaoTelaMon` · Text**

```
"Versão 0.2.1"
```
