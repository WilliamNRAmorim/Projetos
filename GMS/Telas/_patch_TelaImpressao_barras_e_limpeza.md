# Patch TelaImpressao: barras do total igual ao Excel + limpeza da folha (08/10/2026)

## 1. App > Formulas (colar no FINAL do App.Formulas, antes de salvar)

```
fx_TotalBarras(n: Number): Text =
    With(
        { _s: Text(Round(n, 6), "[$-en-US]0.######") },
        Substitute(If(Right(_s, 1) = ".", Left(_s, Len(_s) - 1), _s), ".", ",")
    );

fx_C128BitsA(txt: Text): Text =
    If(
        IsBlank(txt),
        "",
        With(
            { _n: Len(txt) },
            With(
                {
                    _chk: Mod(
                        103 + Sum(
                            ForAll(
                                Sequence(_n) As _i,
                                fx_C128Val(Mid(txt, _i.Value, 1)) * _i.Value
                            ),
                            Value
                        ),
                        103
                    )
                },
                fx_C128Pat(103)
                & Concat(
                    ForAll(
                        Sequence(_n) As _i,
                        fx_C128Pat(fx_C128Val(Mid(txt, _i.Value, 1)))
                    ),
                    Value
                )
                & fx_C128Pat(_chk)
                & fx_C128Pat(106)
            )
        )
    );

fx_CodigoBarras128A(txt: Text, alt: Number): Text =
    If(
        IsBlank(Trim(txt)),
        "",
        With(
            { _bits: fx_C128BitsA(txt) },
            With(
                { _n: Max(1, RoundDown(520 / Len(_bits), 0)) },
                With(
                    { _x0: RoundDown((560 - Len(_bits) * _n) / 2, 0) },
                    "<svg xmlns='http://www.w3.org/2000/svg' width='560' height='" & Text(alt, "[$-en-US]0")
                    & "' viewBox='0 0 560 " & Text(alt, "[$-en-US]0") & "' shape-rendering='crispEdges'>"
                    & "<rect width='100%' height='100%' fill='white'/>"
                    & "<path fill='black' d='"
                    & Concat(
                        ForAll(
                            Sequence(Len(_bits)) As _i,
                            If(
                                Mid(_bits, _i.Value, 1) = "1",
                                "M" & Text(_x0 + (_i.Value - 1) * _n, "[$-en-US]0")
                                & " 6h" & Text(_n, "[$-en-US]0")
                                & "v" & Text(alt - 12, "[$-en-US]0")
                                & "h-" & Text(_n, "[$-en-US]0") & "z",
                                ""
                            )
                        ),
                        Value
                    )
                    & "'/></svg>"
                )
            )
        )
    );
```

## 2. TelaImpressao > `img_barcode_total_1` > propriedade Image (substituir TUDO)

```
=With(
    { _t: If(varPackingManual, Sum(colLancesMan, Coalesce(fx_Num(Txt), 0)), If(IsBlank(varTotalImp), 0, fx_Num(varTotalImp))) },
    If(
        _t <= 0,
        "",
        "data:image/svg+xml," & EncodeUrl(fx_CodigoBarras128A(fx_TotalBarras(_t), 130))
    )
)
```

## 3. TelaImpressao > limpeza da folha
- APAGAR só 2 controles: `lbl_valOperadorManualImp` e `lbl_valMotivoManualImp` (eram a cópia impressa do que está nas caixas).
- `lbl_rotOperadorManualImp` e `lbl_rotMotivoManualImp` (legendas "OPERADOR" e "MOTIVO") FICAM, mas na propriedade Visible de cada um coloque: `=varPackingManual && !Parent.Printing` (aparecem na tela, não na impressão).
- As caixas de seleção `cmb_OperadorManualImp` e `cmb_MotivoManualImp` não mudam (Y 688, só na tela).
- `lbl_tarja_manual_1` > propriedade Y: `=664`

## Teste
Packing manual com lances que somem 15,5 (ex.: 10 + 5,5): o texto do código é `15,5`; bipar e comparar com o Excel antigo (mesmo total). Com total inteiro (ex.: 15) o texto é `15`.
