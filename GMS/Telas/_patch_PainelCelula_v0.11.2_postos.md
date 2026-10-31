# Patch v0.11.2 · Painel da Célula · postos 2 (Skip não existe no Power Fx)

27/10/2026. `First(Skip(col, 1))` dá 'Skip is an unknown or unsupported function'. Troca: Solda de Mandril usa `LookUp(colPostosMandPnl, Ord = 2)`; Extração usa `Last(FirstN(colPostosExtrPnl, 2))` (as 2 cabines L1/L2 vêm de fx_CabinesTeste). Coleção vazia devolve vazio, sem erro de Index. Cole cada propriedade inteira, sem o `=` inicial.

**`btn_SoldaBPnl` · BorderThickness**

```
If(LookUp(colPostosMandPnl, Ord = 2).Estado = "LIVRE", 1, 0)
```

**`btn_SoldaBPnl` · Color**

```
If(LookUp(colPostosMandPnl, Ord = 2).Estado = "LIVRE", fx_CorRotulo, fx_CorTexto)
```

**`btn_SoldaBPnl` · Fill**

```
If(LookUp(colPostosMandPnl, Ord = 2).Estado = "LIVRE", Color.Transparent, fx_CorEstadoPosto(LookUp(colPostosMandPnl, Ord = 2).Estado))
```

**`btn_SoldaBPnl` · Text**

```
LookUp(colPostosMandPnl, Ord = 2).Curto
```

**`lbl_SoldaBInfoPnl` · Color**

```
With(
    { _p: LookUp(colPostosMandPnl, Ord = 2) },
    If(
        _p.Produzindo,          fx_CorPainelTexto,
        _p.Estado = "COM FILA", fx_CorPainelTextoAlerta,
        fx_CorRotulo
    )
)
```

**`lbl_SoldaBInfoPnl` · Text**

```
With(
    { _p: LookUp(colPostosMandPnl, Ord = 2) },
    If(
        _p.Produzindo,
        "OP " & Text(_p.OP, "[$-en-US]0") & "  ·  Bitola " & Text(_p.Bitola, "[$-en-US]0"),
        _p.Estado = "COM FILA",
        "Parada, com fila",
        "Livre"
    )
)
```

**`lbl_SoldaBCronoPnl` · Text**

```
If(LookUp(colPostosMandPnl, Ord = 2).Produzindo, fx_CronoLongo(LookUp(colPostosMandPnl, Ord = 2).Inicio, ctxAgoraPnl), "")
```

**`btn_ExtrL2Pnl` · BorderThickness**

```
If(Last(FirstN(colPostosExtrPnl, 2)).Estado = "LIVRE", 1, 0)
```

**`btn_ExtrL2Pnl` · Color**

```
If(Last(FirstN(colPostosExtrPnl, 2)).Estado = "LIVRE", fx_CorRotulo, fx_CorTexto)
```

**`btn_ExtrL2Pnl` · Fill**

```
If(Last(FirstN(colPostosExtrPnl, 2)).Estado = "LIVRE", Color.Transparent, fx_CorEstadoPosto(Last(FirstN(colPostosExtrPnl, 2)).Estado))
```

**`btn_ExtrL2Pnl` · Text**

```
Last(FirstN(colPostosExtrPnl, 2)).Curto
```

**`lbl_ExtrL2InfoPnl` · Color**

```
With(
    { _p: Last(FirstN(colPostosExtrPnl, 2)) },
    If(
        _p.Produzindo,          fx_CorPainelTexto,
        _p.Estado = "COM FILA", fx_CorPainelTextoAlerta,
        fx_CorRotulo
    )
)
```

**`lbl_ExtrL2InfoPnl` · Text**

```
With(
    { _p: Last(FirstN(colPostosExtrPnl, 2)) },
    If(
        _p.Produzindo,
        fx_Ou(_p.Mangueira) & "  ·  OP " & Text(_p.OP, "[$-en-US]0"),
        _p.Estado = "COM FILA",
        "Parada, com fila",
        "Livre"
    )
)
```

**`lbl_ExtrL2CronoPnl` · Text**

```
If(Last(FirstN(colPostosExtrPnl, 2)).Produzindo, fx_CronoLongo(Last(FirstN(colPostosExtrPnl, 2)).Inicio, ctxAgoraPnl), "")
```
