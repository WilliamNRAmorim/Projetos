# Patch de 05/11/2026: divisão por zero e "Sem conexão" (MEL-262)

Causa medida no rastro do Monitor. Nenhum controle muda de lugar. Depois de colar os dois itens, publicar.

## 1. scr_tubo_1 · lbl_AlertaBalancoTubo_1 · Text

```
=If(
    Coalesce(gal_FilaTubo_1.Selected.quantidade_mandril, 0) <= 0,
    "",
    "⚠ Produzido + refugo passa " &
    Text(
        Round(
            ((Coalesce(fx_Num(inp_QtdTubo_1.Text), 0) + Coalesce(fx_Num(inp_RefugoTubo_1.Text), 0)) / gal_FilaTubo_1.Selected.quantidade_mandril - 1) * 100,
            0
        ),
        "[$-en-US]0"
    ) & "% do que entrou (margem " & fx_MargemMetragemPct & "%). Confira a digitação."
)
```

## 2. App.Formulas · trocar o bloco inteiro de fx_DesvioAtivo por este

```
// [v3.0.17 · MEL-262] Inicio/Fim entram como Text: o conector Excel entrega "31/12/2026", e como Number isso dava
// erro em toda leitura (o painel acusava "Sem conexão" e não carregava a velocidade). Aceita dd/mm/aaaa, serial do
// Excel (46387) e milissegundos desde 1970. Linha vazia ou data ruim = desvio inativo, nunca erro.
fx_DesvioData(v: Text): Number =
    With(
        { _p: Split(Trim(v), "/") },
        If(
            CountRows(_p) = 3,
            DateDiff(
                Date(1899, 12, 30),
                Date(
                    Value(Last(_p).Value, "en-US"),
                    Value(Index(_p, 2).Value, "en-US"),
                    Value(First(_p).Value, "en-US")
                ),
                TimeUnit.Days
            ),
            With(
                { _n: Value(Trim(v), "en-US") },
                If(_n > 1000000, Int(_n / 86400000) + 25569, _n)
            )
        )
    );

fx_DesvioAtivo(desvio: Number, inicio: Text, fim: Text, hoje: Date): Boolean =
    If(
        desvio <> 1 || IsBlank(desvio),
        false,
        IfError(
            With(
                {
                    _h: DateDiff(Date(1899, 12, 30), hoje, TimeUnit.Days),
                    _i: fx_DesvioData(inicio),
                    _f: fx_DesvioData(fim)
                },
                !IsBlank(_i) && !IsBlank(_f) && _h >= _i && _h <= _f
            ),
            false
        )
    );
```
