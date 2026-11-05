# Patch de 05/11/2026: OP descartada não conta produção (MEL-260)

Colar a propriedade inteira no Studio e publicar. Nenhum controle muda de lugar.

## scr_mandril_1 · btn_DescartarCorrMand_1 · OnSelect

```
=Set(varProcessando, true);
Refresh(ficha_producao);
Refresh(lista_carreteis);
With(
    {
        _r: LookUp(ficha_producao, ID = varFichaAtiva.ID),
        _agora: Now(),
        _motivo: Trim(
            ctxMotivoCorrMand &
            If(
                !IsBlank(Trim(inp_MotivoCorrMand_1.Text)),
                " - " & Trim(inp_MotivoCorrMand_1.Text),
                ""
            )
        )
    },
    With(
        {
            _turno: fx_TurnoEm(_agora),
            _refugo: Max(
                Coalesce(_r.quantidade_mandril, 0),
                Coalesce(_r.Qtd_Turno1, 0) +
                Coalesce(_r.Qtd_Turno2, 0) +
                Coalesce(_r.Qtd_Turno3, 0)
            ),
            _carretel: _r.'Carretel Saida',
            _posto: Coalesce(_r.maquina_mandril, varPostoAtivo),
            _quem: Coalesce(cmb_OperadorMand_2.Selected.Nome, _r.operador_mandril)
        },
        If(
            IsBlank(_r.ID),
            Notify("Esta OP não existe mais no servidor. Atualize a tela.", NotificationType.Error, 8000);
            Select(btn_CarregarPostoMand_2);
            Set(varProcessando, false),
            _r.Modified <> varFichaAtiva.Modified,
            Notify("Este registro foi alterado por outro usuário. A tela foi recarregada.", NotificationType.Error, 8000);
            Select(btn_CarregarPostoMand_2);
            Set(varProcessando, false),
            fx_EstadoContinuo(_r.status_processo) <> "PRODUZINDO",
            Notify("Esta OP não está mais em processo. Atualize a tela.", NotificationType.Error, 8000);
            Select(btn_CarregarPostoMand_2);
            Set(varProcessando, false),
            IsBlank(_motivo),
            Notify("Escolha o motivo antes de descartar.", NotificationType.Warning, 6000);
            Set(varProcessando, false),
            Patch(
                ficha_producao,
                _r,
                {
                    status_processo: "Cancelado",
                    data_hora_final_mandril: _agora,
                    Turno_mandril: Text(_turno),
                    operador_mandril: _quem,
                    Observação_mandril: Trim(
                        Coalesce(_r.Observação_mandril, "") &
                        "  [OP DESCARTADA " & Text(_agora, "[$-pt-BR]dd/mm hh:mm") &
                        " por " & Coalesce(_quem, "—") & " - " & _motivo &
                        If(
                            _refugo > 0,
                            " - " & Text(_refugo, "[$-pt-BR]#.##0") & " m viraram refugo",
                            ""
                        ) & "]"
                    )
                }
            );
            If(
                !IsEmpty(Errors(ficha_producao)),
                Notify("Não descartou a OP: " & First(Errors(ficha_producao)).Message, NotificationType.Error, 15000);
                Set(varProcessando, false),
                If(
                    !IsBlank(LookUp(lista_carreteis, op = _r.ID)),
                    Patch(
                        lista_carreteis,
                        LookUp(lista_carreteis, op = _r.ID),
                        {op: Blank(), etapa_processo: Blank()}
                    );
                    If(
                        !IsEmpty(Errors(lista_carreteis)),
                        Notify(
                            "OP descartada, mas o carretel " & Coalesce(_carretel, "—") &
                            " NÃO foi liberado — libere na tela de carretéis: " &
                            First(Errors(lista_carreteis)).Message,
                            NotificationType.Error,
                            15000
                        )
                    )
                );
                With(
                    { _mpUso: LookUp(CarreteisMandril, Status = "Em uso" && OP_solda = Text(_r.ID)) },
                    If(
                        !IsBlank(_mpUso.ID),
                        If(
                            Coalesce(_mpUso.quantidade_metros, 0) - _refugo <= 0,
                            Patch(
                                CarreteisMandril,
                                _mpUso,
                                {
                                    Status: "Vazio",
                                    quantidade_metros: Blank(),
                                    cod_mandril: Blank(),
                                    Bitola: Blank(),
                                    OP_extrusora: Blank(),
                                    operador_extrusora: Blank(),
                                    data_consumo: _agora
                                }
                            ),
                            Patch(
                                CarreteisMandril,
                                _mpUso,
                                {
                                    Status: "Cheio",
                                    quantidade_metros: Coalesce(_mpUso.quantidade_metros, 0) - _refugo,
                                    data_consumo: _agora
                                }
                            )
                        );
                        If(
                            !IsEmpty(Errors(CarreteisMandril)),
                            Notify(
                                "OP descartada, mas o mandril novo " & _mpUso.Title &
                                " NÃO voltou para o estoque — ajuste na tela da Extrusora (Carretéis): " &
                                First(Errors(CarreteisMandril)).Message,
                                NotificationType.Error,
                                15000
                            )
                        )
                    )
                );
                Patch(
                    Eventos_Producao,
                    Defaults(Eventos_Producao),
                    {
                        Title: Text(_r.ID) & "-Mandril-Cancelado",
                        origem: {Value: "ficha_producao"},
                        origem_ID: _r.ID,
                        etapa: {Value: "Mandril"},
                        tipo: {Value: "Cancelado"},
                        data_hora: _agora,
                        data_ref: fx_DataRefEm(_agora),
                        turno: _turno,
                        bitola: Coalesce(_r.Bitola, 0),
                        metros: 0,
                        sobra: _refugo,
                        carretel: _carretel,
                        recurso: _posto,
                        operador: _quem
                    }
                );
                If(
                    !IsEmpty(Errors(Eventos_Producao)),
                    Notify(
                        "OP descartada, mas o evento de cancelamento NÃO gravou — o histórico vai ficar sem o motivo: " &
                        First(Errors(Eventos_Producao)).Message,
                        NotificationType.Error,
                        15000
                    )
                );
                // MEL-260: OP descartada nao conta como producao. Parcial ja gravado fica com 0 m.
                ClearCollect(
                    colParcCancMand,
                    Filter(
                        Filter(Eventos_Producao, origem_ID = _r.ID) As _e0,
                        _e0.tipo.Value = "Parcial" && _e0.etapa.Value = "Mandril"
                    )
                );
                ForAll(
                    colParcCancMand As _ep,
                    Patch(Eventos_Producao, LookUp(Eventos_Producao, ID = _ep.ID), {metros: 0})
                );
                If(
                    !IsEmpty(Errors(Eventos_Producao)),
                    Notify(
                        "OP descartada, mas os parciais NÃO foram zerados e seguem no painel: " &
                        First(Errors(Eventos_Producao)).Message,
                        NotificationType.Error,
                        15000
                    )
                );
                Patch(
                    colPostosMandril,
                    LookUp(colPostosMandril, Posto = _posto),
                    {
                        FichaID:    0,
                        Inicio:     Blank(),
                        CodMandril: Blank(),
                        Bitola:     0,
                        Produzindo: false
                    }
                );
                Set(varCarretelMpMand, "");
                Set(varProduzindo, false);
                Set(varFichaAtiva, Blank());
                UpdateContext({ctxModalCorrigirMand: false, ctxMotivoCorrMand: ""});
                Reset(inp_MotivoCorrMand_1);
                Select(btn_CarregarPostoMand_2);
                Select(btn_KanbanMand_2);
                Set(varProcessando, false);
                Notify(
                    "OP " & Text(_r.ID) & " descartada (" & _motivo & "). Carretel " &
                    Coalesce(_carretel, "—") & " liberado e " &
                    Coalesce(LookUp(colMaquinasMandril, Posto = _posto).Rotulo, "solda") &
                    " livre." &
                    If(
                        _refugo > 0,
                        " " & Text(_refugo, "[$-pt-BR]#.##0") & " m registrados como refugo.",
                        ""
                    ),
                    NotificationType.Success,
                    10000
                )
            )
        )
    )
)
```
