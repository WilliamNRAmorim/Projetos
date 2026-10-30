# Limpeza de Trançadeira e Turno (ficha_producao e TiposErros)

Colar como passos novos no fim da consulta de cada tabela no Editor do Power Query (modelo semântico "(GMS)").
Motivo: a ficha tem "TH-02", "TH.05", "TM.01", "TO-04", "TE0", "0", "1" e "Turno 3" no lugar de TH02, TH05, TM01, TO04, 3.
Troque `Anterior` pelo nome do último passo da consulta.

## ficha_producao

```
// Trançadeira: tira ponto/hífen/espaço, maiúscula; lixo (0, 1, TE0, TE01, T004) vira vazio
PassoTranc = Table.TransformColumns(Anterior, {{"Trançadeira", each
    let t = if _ = null then null else Text.Upper(Text.Remove(Text.From(_), {"-", ".", " "}))
    in if t = null or not List.Contains({"TH01","TH02","TH03","TH04","TH05","TH06","TH07","TM01","TM04","TO04","SPIRAL"}, t) then null
       else if t = "SPIRAL" then "Spiral" else t, type text}}),
// Turno: só o número (1, 2, 3)
PassoTurno = Table.TransformColumns(PassoTranc, {{"Turno_Trançagem", each
    let n = if _ = null then null else Text.Select(Text.From(_), {"1".."3"})
    in if n = null or n = "" then null else n, type text}})
```

## TiposErros

Mesmo passo de Trançadeira (coluna `Trançadeira`); `Turno Erro` já vem só com 1, 2 ou 3.
