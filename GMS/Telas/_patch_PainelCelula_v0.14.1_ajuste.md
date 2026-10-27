# Patch · scr_PainelCelula_1 v0.14.0 → v0.14.1 · ajuste de texto que quebrava em linha (27/10/2026)

Só tamanho de fonte, quebra de linha e texto; nenhum X, Y, Width ou Height muda. Cole cada propriedade, sem o `=` inicial. Os 3 `lbl_ProdT*AcPnl` ficam dentro do template de `gal_AcabPnl` e o `btn_CircBitPnl` dentro de `gal_BitolasPnl`.

**`lbl_ProdT1TuboPnl` · Wrap**

```
false
```

**`lbl_ProdT2TuboPnl` · Wrap**

```
false
```

**`lbl_ProdT3TuboPnl` · Wrap**

```
false
```

**`lbl_ProdT1AcPnl` · Wrap**

```
false
```

**`lbl_ProdT2AcPnl` · Wrap**

```
false
```

**`lbl_ProdT3AcPnl` · Wrap**

```
false
```

**`lbl_TotalRotPnl` · Wrap**

```
false
```

**`lbl_LegParadaPnl` · Wrap**

```
false
```

**`lbl_VersaoTelaPnl` · Wrap**

```
false
```

**`lbl_DetProdT1Pnl` · Wrap**

```
false
```

**`lbl_DetProdT2Pnl` · Wrap**

```
false
```

**`lbl_DetProdT3Pnl` · Wrap**

```
false
```

**`lbl_DetProdDiaPnl` · Wrap**

```
false
```

**`lbl_TuboNomePnl` · Size**

```
fx_FonteCorpo
```

**`btn_CircBitPnl` · Size**

```
fx_FonteApoio
```

**`lbl_BatH1Pnl` · Text**

```
Left(LookUp(colBatVulcPnl, Ord = 1).Hora, 2) & "h" & Char(10) & Right(LookUp(colBatVulcPnl, Ord = 1).Hora, 2)
```

**`lbl_BatH2Pnl` · Text**

```
Left(LookUp(colBatVulcPnl, Ord = 2).Hora, 2) & "h" & Char(10) & Right(LookUp(colBatVulcPnl, Ord = 2).Hora, 2)
```

**`lbl_BatH3Pnl` · Text**

```
Left(LookUp(colBatVulcPnl, Ord = 3).Hora, 2) & "h" & Char(10) & Right(LookUp(colBatVulcPnl, Ord = 3).Hora, 2)
```

**`lbl_BatH4Pnl` · Text**

```
Left(LookUp(colBatVulcPnl, Ord = 4).Hora, 2) & "h" & Char(10) & Right(LookUp(colBatVulcPnl, Ord = 4).Hora, 2)
```

**`lbl_BatH5Pnl` · Text**

```
Left(LookUp(colBatVulcPnl, Ord = 5).Hora, 2) & "h" & Char(10) & Right(LookUp(colBatVulcPnl, Ord = 5).Hora, 2)
```

**`lbl_VersaoTelaPnl` · Text**

```
"Versão 0.14.1"
```
