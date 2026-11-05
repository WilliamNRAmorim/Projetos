# Patch de 05/11/2026: Trançagem pela Hora-Hora no Painel (MEL-263)

Colar as duas propriedades inteiras no Studio e publicar. Nenhum controle muda de lugar.

## 1. scr_PainelCelula_1 · btn_AgregaPnl · OnSelect

```
=With(
    {
        _src: If(ctxModoPnl = "VIVO", colEvDiaPnl, colEvHistPnl),
        _ins: If(ctxModoPnl = "VIVO", colInspDiaPnl, colInspHistPnl),
        // v0.15.1 (MEL-263): Trancagem = Real apontado no Hora-Hora, ultima linha de cada janela. TH01 e TO04 ja gravam mangueira pronta.
        _trc: If(
            ctxModoPnl = "VIVO",
            ShowColumns(
                AddColumns(
                    Filter(colHHConsPnl As _hc0, _hc0.DataRef = fx_DataRefEm(varAgoraPnl)),
                    TurnoTxt,
                    Text(Turno, "[$-en-US]0"),
                    metros,
                    Real
                ),
                TurnoTxt,
                metros
            ),
            colHHHistPnl
        )
    },
    // UMA agregacao para os dois modos: colEvDiaPnl (AO VIVO) ou colEvHistPnl (dia escolhido), mesmo esquema de colunas.
    // Soma de `metros` dos eventos Fim e Parcial; na VULCANIZACAO, dos eventos Inicio (o que entrou na autoclave: o Fim so sai depois da cura); na EXTRACAO, dos lances inspecionados (v0.15.0). Sem registro no turno = Blank() (a tela mostra "—", nunca 0).
    ClearCollect(
        colProdEtapaTurnoPnl,
        ForAll(
            fx_EtapasLinha As _pe,
            With(
                {
                    _ev: If(
                        _pe.Etapa = "Extração",
                        ShowColumns(_ins, TurnoTxt, metros),
                        _pe.Etapa = "Trançagem",
                        _trc,
                        ShowColumns(
                            Filter(
                                _src As _pv,
                                _pv.EtapaTxt = _pe.Etapa && If(_pe.Etapa = "Vulcanização", _pv.TipoTxt = "Início", _pv.TipoTxt = "Fim" || _pv.TipoTxt = "Parcial")
                            ),
                            TurnoTxt,
                            metros
                        )
                    )
                },
                {
                    Etapa: _pe.Etapa,
                    T1: If(CountRows(Filter(_ev As _q1, _q1.TurnoTxt = "1")) > 0, Sum(Filter(_ev As _r1, _r1.TurnoTxt = "1"), metros), Blank()),
                    T2: If(CountRows(Filter(_ev As _q2, _q2.TurnoTxt = "2")) > 0, Sum(Filter(_ev As _r2, _r2.TurnoTxt = "2"), metros), Blank()),
                    T3: If(CountRows(Filter(_ev As _q3, _q3.TurnoTxt = "3")) > 0, Sum(Filter(_ev As _r3, _r3.TurnoTxt = "3"), metros), Blank()),
                    Dia: With({ _t: Filter(_ev As _qd, _qd.TurnoTxt in ["1", "2", "3"]) }, If(CountRows(_t) > 0, Sum(_t, metros), Blank()))
                }
            )
        )
    )
);
// Cabecalho T1/T2/T3/Total e "SAIDA DO nº TURNO" da Extracao leem a linha da Extracao da MESMA colecao.
With(
    { _x: LookUp(colProdEtapaTurnoPnl As _pt, _pt.Etapa = "Extração") },
    Set(varSaidaT1Pnl, _x.T1);
    Set(varSaidaT2Pnl, _x.T2);
    Set(varSaidaT3Pnl, _x.T3);
    Set(varSaidaDiaPnl, _x.Dia)
)
```

## 2. scr_PainelCelula_1 · btn_HistPnl · OnSelect

```
=With(
    {
        _d: ctxDiaPnl,
        _iniIns: fx_PeriodoIniEm(ctxDiaPnl, "DIA", 1),
        _fimIns: fx_PeriodoFimEm(ctxDiaPnl, "DIA", 1)
    },
    // Historico: UMA consulta delegavel por escolha de DIA (trocar de turno no mesmo dia nao consulta de novo).
    // Hoje (ou falha anterior) sempre le de novo. Sem timer de carga, sem Refresh.
    If(
        IsBlank(ctxHistDiaPnl) || ctxHistDiaPnl <> _d || _d >= fx_DataRefEm(ctxAgoraPnl) || ctxHistFalhaPnl,
        UpdateContext({ ctxHistFalhaPnl: false });
        IfError(
            ClearCollect(
                colEvHistPnl,
                AddColumns(
                    Filter(Eventos_Producao, data_ref = _d),
                    EtapaTxt,
                    Text(etapa.Value),
                    TipoTxt,
                    Text(tipo.Value),
                    TurnoTxt,
                    Text(turno)
                )
            );
            ClearCollect(
                colInspHistPnl,
                AddColumns(
                    Filter(
                        RegistrosInspeção,
                        Created >= _iniIns,
                        Created < _fimIns
                    ),
                    TurnoTxt,
                    Text(TurnoTeste),
                    metros,
                    Quantidade
                )
            );
            // v0.15.1 (MEL-263): Hora-Hora do dia escolhido, ultima linha de cada janela apontada.
            ClearCollect(
                colHHHistPnl,
                ForAll(
                    GroupBy(
                        AddColumns(
                            Filter(
                                Filter('Hora-Hora', Data = _d) As _x,
                                Text(_x.Célula) in fx_CelulasTrancagem.Celula
                            ),
                            ChaveJan,
                            Text(Célula) & "|" & Text(Turno) & "|" & Hora
                        ),
                        ChaveJan,
                        LinhasJan
                    ) As _gh,
                    With(
                        { _r: First(Sort(_gh.LinhasJan, ID, SortOrder.Descending)) },
                        {
                            TurnoTxt: Text(fx_TurnoNum(Text(_r.Turno)), "[$-en-US]0"),
                            metros: Coalesce(_r.'Real. Hora', 0)
                        }
                    )
                )
            );
            UpdateContext({ ctxHistDiaPnl: _d });
            true,
            UpdateContext({ ctxHistFalhaPnl: true, ctxHistDiaPnl: Blank() });
            Clear(colEvHistPnl);
            Clear(colInspHistPnl);
            Clear(colHHHistPnl);
            false
        );
        UpdateContext({ ctxHistTruncPnl: CountRows(colEvHistPnl) >= fx_PainelLinhasAlerta || CountRows(colInspHistPnl) >= fx_PainelLinhasAlerta || CountRows(colHHHistPnl) >= fx_PainelLinhasAlerta })
    );
    Select(btn_AgregaPnl)
)
```
