# Patch scr_Finalização_1: "Imprimir Ficha" passa a registrar o pallet 1 (08/10/2026)

Antes: só o botão "Imprimir este pallet" (Dividir pallet) gravava em `Packing_Pallets`. O "Imprimir Ficha" normal só abria a TelaImpressao e o packlist da OP ficava sem registro (caso da OP 30424228).

Agora o `btn_ImprimirExt` grava a linha do **pallet 1** antes de abrir a TelaImpressao, **somente se**:
- a OP tem de 1 a 26 lances (acima de 26 mantém o aviso de sempre e não registra; usar Dividir pallet);
- a ficha ainda **não tem nenhum pallet** em `Packing_Pallets` (reimprimir não duplica nem sobrescreve, e uma OP já dividida não é tocada).
Se a gravação falhar, a impressão segue e a TelaImpressao mostra "Não registrou no sistema (sem rede?)...".

## Onde colar
`btn_ImprimirExt` > propriedade `OnSelect`: cole o bloco abaixo **logo depois da linha** `Set(varPalletTxt, "");` e antes de `Set(VarMangueiraOP, ...)`. Não muda mais nada do botão.

```
              If(
                  CountRows(colLancesExt) > 0
                  && CountRows(colLancesExt) <= 26
                  && IsBlank(LookUp(Packing_Pallets, FichaID = gal_FilaExt.Selected.ID).ID),
                  Set(varProcessando, true);
                  IfError(
                      Patch(
                          Packing_Pallets,
                          Defaults(Packing_Pallets),
                          {
                              Title: Text(gal_FilaExt.Selected.OP, "[$-en-US]0"),
                              FichaID: gal_FilaExt.Selected.ID,
                              Pallet: 1,
                              LanceIDs: Concat(colLancesExt, Text(ID, "[$-en-US]0"), ";"),
                              QtdLances: CountRows(colLancesExt),
                              TotalM: Sum(colLancesExt, Quantidade),
                              Turno: fx_TurnoEm(Now()),
                              DataHoraImp: Now()
                          }
                      );
                      true,
                      Set(varFalhaRegManual, true);
                      true
                  );
                  Set(varProcessando, false)
              );
```

## Teste
1. Finalização > uma OP com até 26 lances e sem pallet > Imprimir Ficha > na lista `Packing_Pallets` surge 1 linha (Pallet 1, LanceIDs sem HTML, QtdLances = nº de lances, TotalM = total).
2. Voltar e imprimir de novo a mesma OP: não cria 2ª linha.
3. Na Consulta de OP, o botão "Packlists da OP" lista esse pallet e reimprime.
