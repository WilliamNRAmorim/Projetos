# Patch · scr_PainelCelula_1 v0.14.2 → v0.14.3 · ficha sem depender da variável varDetEtapaPnl (27/10/2026)

O Studio acusava `varDetEtapaPnl` não reconhecida (a variável só nasce no `btn_DetAbrirPnl.OnSelect` da v0.14.0). Estas propriedades passam a deduzir a etapa de `varDetReqPnl`, que já existe em toda a tela; a ordem de colar deixa de importar. Cole cada propriedade inteira, sem o `=` inicial.

**`lbl_DetProdRotPnl` · Text**

```
"PRODUÇÃO DO PROCESSO · " & Text(If(ctxModoPnl = "VIVO", fx_DataRefEm(ctxAgoraPnl), ctxDiaPnl), "dd/mm") & " · m" &
If(ctxModoPnl <> "VIVO" && ctxHistFalhaPnl, " · sem histórico", "")
```

**`lbl_DetProdRotPnl` · Visible**

```
varDetAbertoPnl
```

**`lbl_DetProdT1Pnl` · Text**

```
With(
    { _v: LookUp(colProdEtapaTurnoPnl As _pt, _pt.Etapa = Switch(varDetReqPnl.Tipo, "TRANC", "Trançagem", "TUBO", "Tubo", "EXTR", "Extração", varDetReqPnl.Chave)).T1 },
    "1º " & If(
        (ctxModoPnl = "VIVO" && 1 > fx_TurnoEm(ctxAgoraPnl)) || IsBlank(_v),
        "—",
        Substitute(Text(_v, "[$-en-US]#,##0"), ",", ".")
    )
)
```

**`lbl_DetProdT1Pnl` · Visible**

```
varDetAbertoPnl && Switch(varDetReqPnl.Tipo, "TRANC", "Trançagem", "TUBO", "Tubo", "EXTR", "Extração", varDetReqPnl.Chave) <> "Bobinadeira"
```

**`lbl_DetProdT2Pnl` · Text**

```
With(
    { _v: LookUp(colProdEtapaTurnoPnl As _pt, _pt.Etapa = Switch(varDetReqPnl.Tipo, "TRANC", "Trançagem", "TUBO", "Tubo", "EXTR", "Extração", varDetReqPnl.Chave)).T2 },
    "2º " & If(
        (ctxModoPnl = "VIVO" && 2 > fx_TurnoEm(ctxAgoraPnl)) || IsBlank(_v),
        "—",
        Substitute(Text(_v, "[$-en-US]#,##0"), ",", ".")
    )
)
```

**`lbl_DetProdT2Pnl` · Visible**

```
varDetAbertoPnl && Switch(varDetReqPnl.Tipo, "TRANC", "Trançagem", "TUBO", "Tubo", "EXTR", "Extração", varDetReqPnl.Chave) <> "Bobinadeira"
```

**`lbl_DetProdT3Pnl` · Text**

```
With(
    { _v: LookUp(colProdEtapaTurnoPnl As _pt, _pt.Etapa = Switch(varDetReqPnl.Tipo, "TRANC", "Trançagem", "TUBO", "Tubo", "EXTR", "Extração", varDetReqPnl.Chave)).T3 },
    "3º " & If(
        (ctxModoPnl = "VIVO" && 3 > fx_TurnoEm(ctxAgoraPnl)) || IsBlank(_v),
        "—",
        Substitute(Text(_v, "[$-en-US]#,##0"), ",", ".")
    )
)
```

**`lbl_DetProdT3Pnl` · Visible**

```
varDetAbertoPnl && Switch(varDetReqPnl.Tipo, "TRANC", "Trançagem", "TUBO", "Tubo", "EXTR", "Extração", varDetReqPnl.Chave) <> "Bobinadeira"
```

**`lbl_DetProdDiaPnl` · Text**

```
With(
    { _v: LookUp(colProdEtapaTurnoPnl As _pt, _pt.Etapa = Switch(varDetReqPnl.Tipo, "TRANC", "Trançagem", "TUBO", "Tubo", "EXTR", "Extração", varDetReqPnl.Chave)).Dia },
    "DIA " & If(IsBlank(_v), "—", Substitute(Text(_v, "[$-en-US]#,##0"), ",", "."))
)
```

**`lbl_DetProdDiaPnl` · Visible**

```
varDetAbertoPnl && Switch(varDetReqPnl.Tipo, "TRANC", "Trançagem", "TUBO", "Tubo", "EXTR", "Extração", varDetReqPnl.Chave) <> "Bobinadeira"
```

**`lbl_DetProdSemPnl` · Text**

```
"Sem registro de produção da Bobinagem"
```

**`lbl_DetProdSemPnl` · Visible**

```
varDetAbertoPnl && Switch(varDetReqPnl.Tipo, "TRANC", "Trançagem", "TUBO", "Tubo", "EXTR", "Extração", varDetReqPnl.Chave) = "Bobinadeira"
```

**`lbl_VersaoTelaPnl` · Text**

```
"Versão 0.14.3"
```
