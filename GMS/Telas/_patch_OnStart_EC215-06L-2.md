# OnStart: EC215-06L-2 em colMangueiras (MEL-254, 01/11/2026)

Motivo: EC215-06L-2 já tem faixa na DM_TUBE_EXTRUSION (Identity 97, 0,455 a 0,475), mas não estava em `colMangueiras`, então o operador não conseguia escolher e a ficha do Tubo comparava com a faixa da EC215-06L. Mesmo caso do GH781-6-2 (publicado em 29/10).

Arquivo: `Telas/OnStart.txt` não foi alterado por esta sessão (aplicar o mesmo texto lá depois que o William colar, norma de manutenção do `Telas/`).

## Onde colar
Studio > **App** > propriedade **OnStart** > dentro de `ClearCollect(colMangueiras, ForAll([ ... ], ...))`, 4ª linha de nomes (a que começa em `"EC118-16L"`).

## Trecho a substituir
Troque esta linha:
```
                "EC118-16L", "EC215-06L", "EC215-08L", "EC215-04", "EC215-08LRL", "EC215-10L",
```
por esta (só acrescenta `"EC215-06L-2"` depois de `"EC215-06L"`):
```
                "EC118-16L", "EC215-06L", "EC215-06L-2", "EC215-08L", "EC215-04", "EC215-08LRL", "EC215-10L",
```

## Depois de colar
1. Salvar, **publicar** e reabrir o app (OnStart só roda na abertura).
2. Conferir: no Tubo, a lista de mangueiras mostra `EC215-06L-2` e a ficha usa a faixa 0,455 a 0,475.
3. `colMangEscTubo` herda sozinho (`ClearCollect(colMangEscTubo, colMangueiras, ...)`).
