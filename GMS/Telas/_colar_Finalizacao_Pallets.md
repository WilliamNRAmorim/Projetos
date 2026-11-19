# Colar: Finalização (cabine) — pallets e exclusão de lance (v0.4.4)

Tela `scr_Finalização_1`. Origem: OP 30842762 (lances novos gravados por cima do pallet 1 já impresso e lançado no SAP).

## Passo a passo

1. No SharePoint, criar a lista **Lances_Excluidos** com as colunas: `Title` (OP, texto), `LanceID` (número), `Metros` (número), `Pallet` (número; 0 = sem pallet), `PalletID` (número), `Cabine` (texto), `Operador` (texto), `DataHoraLance` (data e hora).
2. No Power Apps Studio (app GMS): Dados > Adicionar dados > SharePoint > lista **Lances_Excluidos**. O nome da fonte no app tem que ser exatamente `Lances_Excluidos`.
3. Colar as fórmulas abaixo, uma por uma, na barra de fórmulas do controle e da propriedade indicados (substitui a fórmula inteira). Ordem sugerida: C1, C2, C4, C3, C5, A, B, versão.
4. Verificar que não ficou sublinhado vermelho (se `Lances_Excluidos` aparecer em erro, a fonte do passo 2 não foi adicionada).
5. Publicar.

Nenhum controle teve X, Y, Width ou Height alterado. Coleções novas (criadas pelas fórmulas, sem declarar): `colPalletImpExt` e `colPalletExcExt`.

## Roteiro de teste

1. OP com pallet 1 impresso + um lance novo: tocar Imprimir Ficha. Esperado: aviso amarelo e abre o modal Dividir com só o lance novo marcado; o pallet 1 não muda. Imprimir o pallet 2.
2. Na mesma OP, excluir um lance que está no pallet 1: o modal avisa "Este lance está no pallet 1...". Confirmar. Esperado: aviso de reimprimir o pallet 1 e pedir estorno; o pallet 1 em Packing_Pallets fica com o lance fora, QtdLances e TotalM menores; nova linha em Lances_Excluidos com Pallet = 1.
3. Excluir um lance que NÃO está em pallet: modal com o texto antigo, linha em Lances_Excluidos com Pallet = 0 e PalletID vazio, Packing_Pallets intacto.
4. OP nova (sem pallet), com lances: Imprimir Ficha cria o pallet 1 e imprime. Reimprimir a mesma OP sem lance novo: imprime e não grava nada.
5. Finalizar OP sem pallet (impressão falhou): cria o pallet 1. Finalizar OP com pallet: não altera pallet.

## Fórmulas

### btn_ImprimirExt → OnSelect

A. Imprimir Ficha: se a OP já tem pallet e há lance fora de pallet, abre o Dividir; só cria o pallet 1 quando a OP não tem pallet.

```powerfx
=IfError(
    ClearCollect(colPalletImpExt, Filter(Packing_Pallets, FichaID = gal_FilaExt.Selected.ID)); true,
    Clear(colPalletImpExt);
    Notify("Não consegui ler os pallets já impressos desta OP. Confira os lances antes de imprimir.", NotificationType.Warning, 6000)
);
If(
    !IsEmpty(colPalletImpExt)
    && !IsEmpty(
        Filter(
            colLancesExt As _l,
            IsEmpty(Filter(colPalletImpExt, !IsBlank(Find(";" & Text(_l.ID, "[$-en-US]0") & ";", ";" & LanceIDs & ";"))))
        )
    ),
    Notify("Esta OP já tem pallet impresso. Os lances novos vão num pallet separado: confira os lances marcados e imprima.", NotificationType.Warning, 8000);
    Select(btn_DividirPalletExt),
    If(
        CountRows(colLancesExt) > 26,
        Notify("Esta OP tem mais de 26 lances. A ficha impressa mostra os 26 primeiros; o total impresso continua sendo o total real.", NotificationType.Warning, 10000)
    );
    Set(varFichaIDImp, gal_FilaExt.Selected.ID);
    Set(varFalhaRegManual, false);
    Set(varPackingManual, false);
    Set(varPalletTxt, "");
    If(
        CountRows(colLancesExt) > 0
        && CountRows(colLancesExt) <= 26
        && IsEmpty(colPalletImpExt),
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
            Notify("A impressão segue. O registro do pallet será feito ao finalizar. (" & FirstError.Message & ")", NotificationType.Warning, 8000);
            true
        );
        Set(varProcessando, false)
    );
    Set(varImpQtd, CountRows(colLancesExt));
    Set(varImpTotal, Sum(colLancesExt, Quantidade));
    Set(VarMangueiraOP, gal_FilaExt.Selected.OP);
    Set(varMangueiraImp, gal_FilaExt.Selected.Mangueira);
    Set(varTotalImp, fx_QtdBR(Coalesce(Sum(colLancesExt, Quantidade), 0)));
    Set(
        varHTMLLances,
        "<table style='border-collapse:collapse;width:100%'>"
        & "<tr style='background:#d0d0d0'><th style='border:1px solid #000;padding:10px 12px;font-size:20px;width:8%'>N°</th><th style='border:1px solid #000;padding:10px 12px;font-size:20px;width:27%'>QTY (m)</th><th style='border:1px solid #000;padding:10px 12px;font-size:20px;width:8%'>N°</th><th style='border:1px solid #000;padding:10px 12px;font-size:20px'>QTY (m)</th></tr>"
        & Concat(
            ForAll(
                Sequence(13) As _i,
                {
                    linha:
                        "<tr><td style='border:1px solid #000;padding:10px 12px;font-size:20px'>"
                        & Text(_i.Value, "[$-en-US]0")
                        & "</td><td style='border:1px solid #000;padding:10px 12px;font-size:20px'>"
                        & If(
                            CountRows(colLancesExt) >= _i.Value,
                            fx_QtdBR(Index(colLancesExt, _i.Value).Quantidade),
                            "0,00"
                        )
                        & "</td><td style='border:1px solid #000;padding:10px 12px;font-size:20px'>"
                        & Text(_i.Value + 13, "[$-en-US]0")
                        & "</td><td style='border:1px solid #000;padding:10px 12px;font-size:20px'>"
                        & If(
                            CountRows(colLancesExt) >= _i.Value + 13,
                            fx_QtdBR(Index(colLancesExt, _i.Value + 13).Quantidade),
                            "0,00"
                        )
                        & "</td></tr>"
                }
            ),
            linha
        )
        & "</table>"
    );
    Navigate(TelaImpressao, ScreenTransition.None)
)
```

### btn_ConfirmarFinalizarExt → OnSelect

B. Finalizar: só cria o pallet 1 quando a OP não tem nenhum pallet; nunca sobrescreve.

```powerfx
=Set(varProcessando, true);
IfError(ClearCollect(colLancesExt, Filter(RegistrosInspeção, OP_ID = gal_FilaExt.Selected.OP)); true, Notify("Não consegui ler os lances desta OP. Toque em atualizar antes de continuar.", NotificationType.Error, 8000));
Refresh(ficha_producao);
Refresh(Packing_Pallets);
With(
    {
        _r: LookUp(ficha_producao, ID = gal_FilaExt.Selected.ID),
        _agora: Now(),
        _operador: cmb_OperadorExt.Selected.Nome,
        _total: Coalesce(Sum(colLancesExt, Quantidade), 0)
    },
    If(
        IsBlank(ctxCabineExt.Posto),
        Notify("Cabine não identificada. Volte ao menu e entre pelo card da sua cabine.", NotificationType.Error, 8000);
        Set(varProcessando, false),
        IsBlank(_operador),
        Notify("Selecione o U-Number do operador antes de finalizar.", NotificationType.Warning, 6000);
        Set(varProcessando, false),
        With(
            { _pks: Filter(Packing_Pallets, FichaID = gal_FilaExt.Selected.ID) },
            (IsEmpty(_pks) || Sum(_pks, QtdLances) <> CountRows(colLancesExt) || Abs(Sum(_pks, TotalM) - _total) > 0.005)
            && !(varFichaIDImp = gal_FilaExt.Selected.ID && varImpQtd = CountRows(colLancesExt) && Abs(varImpTotal - _total) <= 0.005)
        ),
        Notify("Imprima o pack list desta OP antes de finalizar (ou imprima de novo, se entrou lance depois da última impressão). Toque em Imprimir, confirme e volte.", NotificationType.Error, 10000);
        Set(varProcessando, false),
        !fx_MetragemOk(_total),
        Notify("Nenhum lance aprovado nesta OP. Registre a inspeção antes de finalizar — a ficha não pode fechar com zero.", NotificationType.Error, 10000);
        Set(varProcessando, false),
        _r.Modified <> gal_FilaExt.Selected.Modified,
        Notify("Registro desatualizado. A fila foi recarregada, tente de novo.", NotificationType.Error, 8000);
        Set(varProcessando, false),
        !IsBlank(_r.cabine_teste) && _r.cabine_teste <> varPostoAtivo,
        Notify("Esta OP está sendo inspecionada na " & LookUp(fx_CabinesTeste, Posto = _r.cabine_teste).Rotulo & ". Finalize por lá.", NotificationType.Error, 8000);
        Set(varProcessando, false),
        With(
            { _carretel: _r.'Carretel Entrada' },
            If(
                IsEmpty(Filter(Packing_Pallets, FichaID = gal_FilaExt.Selected.ID)),
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
                            TotalM: _total,
                            Turno: fx_TurnoEm(_agora),
                            DataHoraImp: _agora
                        }
                    );
                    true,
                    Notify("OP finalizada, mas o pallet NÃO foi registrado: " & FirstError.Message & ". Avise a supervisão.", NotificationType.Warning, 12000);
                    true
                )
            );
            Set(
                gvarRegistroExtracao,
                Patch(
                    ficha_producao,
                    _r,
                    {
                        'Carretel Entrada': Blank(),
                        'Carretel Saida': Blank(),
                        operador_extracao: _operador,
                        quantidade_extracao: _total,
                        cabine_teste: Coalesce(_r.cabine_teste, varPostoAtivo),
                        DataFinalizacao: Today(),
                        data_hora_final_extracao: _agora,
                        status_processo: "Finalizado",
                        processo: "Finalizado",
                        'Turno_Extr/Teste': fx_TurnoEm(_agora)
                    }
                )
            );
            If(
                !IsEmpty(Errors(ficha_producao)),
                Notify("Falha ao finalizar: " & First(Errors(ficha_producao)).Message, NotificationType.Error, 12000);
                Set(varProcessando, false),
                With(
                    { _cust: LookUp(Historico_Carretel, etapa = "Extração" && Title = _carretel && OP_ID = gvarRegistroExtracao.OP) },
                    Patch(
                        Historico_Carretel,
                        Coalesce(_cust, Defaults(Historico_Carretel)),
                        {
                            Title: _carretel,
                            OP_ID: gvarRegistroExtracao.OP,
                            etapa: "Extração",
                            mangueira: Text(gvarRegistroExtracao.Bitola),
                            metros_entrada: Coalesce(gvarRegistroExtracao.quantidade_debandagem, 0),
                            metros_saida: _total,
                            data_hora_entrada: Coalesce(_cust.data_hora_entrada, gvarRegistroExtracao.data_hora_inicio_extracao),
                            data_hora_saida: _agora,
                            operador: _operador
                        }
                    )
                );
                If(
                    !IsEmpty(Errors(Historico_Carretel)),
                    Notify("Ficha salva, mas o histórico do carretel NÃO gravou: " & First(Errors(Historico_Carretel)).Message, NotificationType.Error, 10000)
                );
                Patch(
                    Eventos_Producao,
                    Defaults(Eventos_Producao),
                    {
                        Title: Text(gvarRegistroExtracao.ID) & "-Extracao-Fim",
                        origem: {Value: "ficha_producao"},
                        origem_ID: gvarRegistroExtracao.ID,
                        etapa: {Value: "Extração"},
                        tipo: {Value: "Fim"},
                        data_hora: _agora,
                        data_ref: fx_DataRefEm(_agora),
                        turno: fx_TurnoEm(_agora),
                        bitola: gvarRegistroExtracao.Bitola,
                        metros: _total,
                        recurso: gvarRegistroExtracao.cabine_teste,
                        operador: _operador
                    }
                );
                If(
                    !IsEmpty(Errors(Eventos_Producao)),
                    Notify("Evento de fim não gravou: " & First(Errors(Eventos_Producao)).Message, NotificationType.Error, 10000)
                );
                If(
                    !IsBlank(_carretel),
                    With(
                        { _c: LookUp(lista_carreteis, Title = Text(_carretel)) },
                        If(
                            IsBlank(_c),
                            Notify("Ficha salva, mas o carretel " & Text(_carretel) & " não foi encontrado para liberar. Avise a Supervisão.", NotificationType.Warning, 10000),
                            Patch(lista_carreteis, _c, {op: Blank(), etapa_processo: Blank()});
                            If(
                                !IsEmpty(Errors(lista_carreteis)),
                                Notify("Ficha salva, mas o carretel NÃO foi liberado: " & First(Errors(lista_carreteis)).Message, NotificationType.Error, 10000)
                            )
                        )
                    )
                );
                Refresh(ficha_producao);
                Reset(cmb_OperadorExt);
                UpdateContext({ctxModalFinalizarExt: false, ctxAgora: _agora, ctxSincExt: _agora});
                Set(varProcessando, false);
                Notify("Ordem finalizada com " & fx_QtdBR(_total) & " m aprovados.", NotificationType.Success, 6000)
            )
        )
    )
)
```

### ico_ExcluirLanceExt → OnSelect

C1. Ícone de excluir lance: carrega o pallet que contém o lance.

```powerfx
=IfError(
    ClearCollect(
        colPalletExcExt,
        Filter(
            Filter(Packing_Pallets, FichaID = gal_FilaExt.Selected.ID),
            !IsBlank(Find(";" & Text(ThisItem.ID, "[$-en-US]0") & ";", ";" & LanceIDs & ";"))
        )
    ); true,
    Clear(colPalletExcExt);
    Notify("Não consegui conferir os pallets desta OP. Confira com a supervisão se o lance já foi impresso antes de excluir.", NotificationType.Warning, 8000)
);
UpdateContext({
    ctxLanceExcluirExt: ThisItem,
    ctxTipoExcluirExt: "LANCE",
    ctxModalExcluirExt: true
})
```

### ico_ExcluirRefugoExt → OnSelect

C2. Ícone de excluir reprovado: limpa a coleção do pallet.

```powerfx
=Clear(colPalletExcExt);
UpdateContext({
    ctxRefugoExcluirExt: ThisItem,
    ctxTipoExcluirExt: "REFUGO",
    ctxModalExcluirExt: true
})
```

### lbl_DetalheExcluirExt → Text

C3. Texto do modal: avisa quando o lance está em pallet.

```powerfx
=If(
    ctxTipoExcluirExt = "LANCE",
    If(
        IsEmpty(colPalletExcExt),
        "Lance de " & ctxLanceExcluirExt.Quantidade & " m sai do total aprovado da OP. A exclusão é definitiva.",
        "Lance no pallet " & Text(First(colPalletExcExt).Pallet, "[$-en-US]0") & " (já impresso, talvez já no SAP). Reimprima o pallet e peça estorno de " & ctxLanceExcluirExt.Quantidade & " m no SAP."
    ),
    "Reprovado de " & ctxRefugoExcluirExt.Quantidade & " m (" & ctxRefugoExcluirExt.CodigoErro & ") sai do refugo da OP. A exclusão é definitiva."
)
```

### btn_CancelarExcluirExt → OnSelect

C4. Cancelar do modal: limpa a coleção do pallet.

```powerfx
=Clear(colPalletExcExt);
UpdateContext({
    ctxModalExcluirExt: false,
    ctxTipoExcluirExt: "",
    ctxLanceExcluirExt: Blank(),
    ctxRefugoExcluirExt: Blank()
})
```

### btn_ConfirmarExcluirExt → OnSelect

C5/D. Confirmar exclusão: registra em Lances_Excluidos, corrige o pallet e avisa reimpressão e estorno.

```powerfx
=Set(varProcessando, true);
If(
    ctxTipoExcluirExt = "LANCE",
    Remove(RegistrosInspeção, ctxLanceExcluirExt);
    If(
        !IsEmpty(Errors(RegistrosInspeção)),
        Notify("Falha ao excluir o lance: " & First(Errors(RegistrosInspeção)).Message, NotificationType.Error, 10000),
        IfError(
            Patch(
                Lances_Excluidos,
                Defaults(Lances_Excluidos),
                {
                    Title: Text(gal_FilaExt.Selected.OP, "[$-en-US]0"),
                    LanceID: ctxLanceExcluirExt.ID,
                    Metros: ctxLanceExcluirExt.Quantidade,
                    Pallet: Coalesce(First(colPalletExcExt).Pallet, 0),
                    PalletID: First(colPalletExcExt).ID,
                    Cabine: ctxCabineExt.Posto,
                    Operador: cmb_OperadorExt.Selected.Nome,
                    DataHoraLance: ctxLanceExcluirExt.DataHoraInspecao
                }
            ); true,
            Notify("Lance excluído, mas o registro da exclusão não foi gravado: " & FirstError.Message, NotificationType.Warning, 8000); true
        );
        If(
            !IsEmpty(colPalletExcExt),
            With(
                {
                    _pal: First(colPalletExcExt),
                    _idTxt: Text(ctxLanceExcluirExt.ID, "[$-en-US]0")
                },
                IfError(
                    Patch(
                        Packing_Pallets,
                        LookUp(Packing_Pallets, ID = _pal.ID),
                        {
                            LanceIDs: Concat(Filter(Split(_pal.LanceIDs, ";"), Value <> _idTxt), Value, ";"),
                            QtdLances: _pal.QtdLances - 1,
                            TotalM: Round(_pal.TotalM - ctxLanceExcluirExt.Quantidade, 2)
                        }
                    ); true,
                    Notify("O lance foi excluído, mas o pallet " & Text(_pal.Pallet, "[$-en-US]0") & " não foi atualizado: " & FirstError.Message & ". Avise a supervisão.", NotificationType.Warning, 12000); true
                )
            )
        );
        Concurrent(
            IfError(ClearCollect(colLancesExt, Filter(RegistrosInspeção, OP_ID = gal_FilaExt.Selected.OP)); true, Notify("Não consegui ler os lances desta OP. Toque em atualizar antes de continuar.", NotificationType.Error, 8000)),
            IfError(ClearCollect(
                colInspDiaExt,
                Filter(
                    RegistrosInspeção,
                    Created >= ctxIniDiaExt,
                    Created < ctxFimDiaExt
                )
            ); true, Notify("Não consegui ler o total do dia. Toque em atualizar.", NotificationType.Error, 8000))
        );
        If(
            IsEmpty(colPalletExcExt),
            Notify("Lance excluído.", NotificationType.Success, 3000),
            Notify("Lance excluído. Reimprima o pallet " & Text(First(colPalletExcExt).Pallet, "[$-en-US]0") & " e peça o estorno de " & ctxLanceExcluirExt.Quantidade & " m no SAP.", NotificationType.Warning, 15000)
        )
    ),
    Remove(TiposErros, ctxRefugoExcluirExt);
    If(
        !IsEmpty(Errors(TiposErros)),
        Notify("Falha ao excluir o reprovado: " & First(Errors(TiposErros)).Message, NotificationType.Error, 10000),
        IfError(ClearCollect(colRefugoExt, Filter(TiposErros, OP_ID = gal_FilaExt.Selected.OP)); true, Notify("Não consegui ler os reprovados desta OP. Toque em atualizar antes de continuar.", NotificationType.Error, 8000));
        Notify("Reprovado excluído.", NotificationType.Success, 3000)
    )
);
UpdateContext({
    ctxModalExcluirExt: false,
    ctxTipoExcluirExt: "",
    ctxLanceExcluirExt: Blank(),
    ctxRefugoExcluirExt: Blank(),
    ctxEditandoLanceExt: Blank()
});
Set(varProcessando, false)
```

### lbl_VersaoExt → Text

Versão da tela.

```powerfx
="Versão 0.4.4"
```
