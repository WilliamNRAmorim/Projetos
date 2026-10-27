# Patch Painel da Célula v0.14.0 · produção por turno DENTRO da ficha de consulta

Base: Telas/scr_PainelCelula_1.txt v0.13.0 (tela publicada com layout ajustado à mão: patch por bloco, nunca reimport).
Staging: scratchpad/stage4/scr_PainelCelula_1.txt (QA sem FALHOU). Nenhuma fx_ nova, Formulas.txt intocado. Nenhum X/Y/Width/Height de controle existente muda. Seletor de dia/turno (btn_Sel*), coleção colProdEtapaTurnoPnl e z-order da ficha da v0.13.0 ficam como estão.

## O que muda
- Ficha de consulta ganha o bloco "PRODUÇÃO DO PROCESSO · dd/mm · m" no cabeçalho (1º, 2º, 3º e DIA), lendo `LookUp(colProdEtapaTurnoPnl, Etapa = varDetEtapaPnl)`: fonte única que já respeita o dia escolhido. "—" quando Blank ou turno que ainda não começou (AO VIVO). Turno corrente em destaque (bold), igual aos cards.
- `varDetEtapaPnl` (nova, global) é gravada por btn_DetAbrirPnl a partir de varDetReqPnl: TRANC→Trançagem, TUBO→Tubo, EXTR→Extração, BOB→Bobinadeira; ACAB, VULC, MAND e TRANCP trazem a etapa na Chave.
- 3 botões transparentes novos abrem a MESMA ficha em "modo processo" (Tipo MAND, TRANCP, BOB; sem OP tocada): Mandril (card inteiro), Trançagem (faixa do título do card) e Bobinagem (card inteiro). Mandril e Trançagem listam as OPs em curso; Bobinagem mostra "Sem registro de produção da Bobinagem" no lugar dos números.

## Ordem de colar
1. Tela scr_PainelCelula_1 → btn_DetAbrirPnl → OnSelect (item 1, inteira).
2. Colar o YAML dos 3 botões (item 2) e depois o do bloco da ficha (item 3), na tela.
3. lbl_VersaoTelaPnl → Text (item 4).
4. Z-ORDER: os 3 botões btn_Ficha*Pnl têm de ficar ABAIXO de btn_DetScrimPnl (a ficha tem de cobri-los) e ACIMA dos cards: selecione btn_DetScrimPnl e todos os controles da ficha (btn_DetCardPnl em diante, inclusive os 6 lbl_DetProd*Pnl) e use "Trazer para frente". Os 6 lbl_DetProd*Pnl têm de ficar ACIMA de lbl_DetTituloPnl.
5. Preview (F5): tocar a Solda de Mandril, a faixa TRANÇAGEM e a Bobinagem; tocar um card de Tubo/Cobertura/Extração e uma bolinha de trançadeira (bloco de produção na ficha); trocar de turno/dia e abrir a ficha de novo.

## 1. btn_DetAbrirPnl · OnSelect (inteira, sem o "=" inicial)
```
Set(varDetToquePnl, Now());
// v0.9.0 · FICHA DE CONSULTA (C36 · C1 · C21). Toda a busca e LOCAL: le so as colecoes
// que a carga de 2 min ja trouxe (colAtivasPnl, colAguardPnl, colPostos*, colHHJanPnl).
// Zero chamada ao SharePoint no toque, por isso abre na hora. Zero Patch: e consulta.
// Cada controle clicavel so grava varDetReqPnl {Tipo, Chave, N} e chama este botao;
// a logica mora num lugar so.
Set(varDetSincPnl, varSincPnl);
Set(varDetIDPnl, Blank());
// v0.14.0: etapa tocada = chave de colProdEtapaTurnoPnl (bloco PRODUCAO DO PROCESSO da ficha).
// TRANC/TUBO/EXTR/BOB tem nome proprio; ACAB, VULC, MAND e TRANCP trazem a etapa na Chave.
Set(
    varDetEtapaPnl,
    Switch(
        varDetReqPnl.Tipo,
        "TRANC", "Trançagem",
        "TUBO",  "Tubo",
        "EXTR",  "Extração",
        "BOB",   "Bobinadeira",
        varDetReqPnl.Chave
    )
);
Clear(colDetListaPnl);
With(
    { _q: varDetReqPnl },
    If(
        _q.Tipo = "TRANC",
        With(
            { _p: LookUp(colPostosTrancPnl As _x1, _x1.Posto = _q.Chave) },
            If(
                _q.N = 0,
                // MAQUINA: a OP montada + a fila inteira, OP por OP, na ordem dos carreteis.
                If(
                    !IsBlank(_p.IDAtiva),
                    Collect(colDetListaPnl, { ID: _p.IDAtiva, Tag: "Na máquina agora", Ord: 0 })
                );
                // OP que divide o carretel com a OP montada NAO e tubo atras: entra em seguida,
                // do mesmo carretel (o caso que motivou a v0.8.1). Aparece logo abaixo da montada.
                With(
                    {
                        _carMaq: Upper(Trim(LookUp(colAtivasPnl As _a9, _a9.ID = _p.IDAtiva).'Carretel Entrada'))
                    },
                    If(
                        !IsBlank(_p.IDAtiva) && !IsBlank(_carMaq),
                        Collect(
                            colDetListaPnl,
                            ForAll(
                                Filter(
                                    colAguardPnl As _g9,
                                    _g9.processo = "Trançadeira" && _g9.Trançadeira = _p.Posto &&
                                    Upper(Trim(_g9.'Carretel Entrada')) = _carMaq
                                ) As _m9,
                                { ID: _m9.ID, Tag: "Mesmo carretel · entra em seguida", Ord: 0.5 }
                            )
                        )
                    )
                );
                Collect(
                    colDetListaPnl,
                    ForAll(
                        Ungroup(_p.FilaTab, OpsCar) As _u,
                        {
                            ID: _u.ID,
                            Tag: If(
                                StartsWith(_u.CarKey, "ID-"),
                                "Sem carretel apontado",
                                "Carretel " & _u.CarKey
                            ) & " · " & Text(
                                CountRows(Filter(_p.FilaTab As _k1, _k1.PrimID <= _u.PrimID)),
                                "[$-en-US]0"
                            ) & "º atrás",
                            Ord: _u.PrimID
                        }
                    )
                );
                With(
                    { _hh: Filter(colHHJanPnl As _j1, _j1.Celula = _p.Posto && _j1.Fechada) },
                    Set(
                        varDetPnl,
                        {
                            Titulo: _p.Rotulo & " · Trançadeira",
                            // v0.11.0 (item 4): PARADA e PAUSA vem antes de "Trancando", porque a trancadeira pode
                            // estar parada COM OP aberta.
                            Sub: If(
                                _p.Estado = "PARADA",
                                "Parada · " & _p.Motivo & " · nesta janela há " & fx_CronoLongo(_p.InicioParada, ctxAgoraPnl),
                                _p.Estado = "PAUSA",
                                "Pausa programada · " & _p.Motivo & " · há " & fx_CronoLongo(_p.InicioParada, ctxAgoraPnl),
                                _p.Produzindo,
                                "Trançando há " & fx_CronoLongo(_p.Inicio, ctxAgoraPnl),
                                _p.Fila > 0,
                                "Sem OP, com fila",
                                "Livre"
                            ) & "  ·  " & Text(_p.Fila, "[$-en-US]0") &
                            If(_p.Fila = 1, " carretel atrás", " carretéis atrás"),
                            Estado: _p.Estado,
                            Cor: _p.Cor,
                            Lado: "NA MÁQUINA E NA FILA",
                            Maquina: _p.Posto,
                            Motivo: _p.Motivo,
                            ParadoMin: _p.ParadoMin,
                            PausaMin: _p.PausaMin,
                            HHReal: Sum(_hh, Real),
                            HHMeta: Sum(_hh, Meta)
                        }
                    )
                ),
                // CARRETEL: as OPs que ele carrega (v0.8.1: um carretel pode levar mais de uma).
                With(
                    { _c: Index(_p.FilaTab, _q.N) },
                    Collect(
                        colDetListaPnl,
                        ForAll(_c.OpsCar As _o, { ID: _o.ID, Tag: "Neste carretel", Ord: 1 })
                    );
                    Set(
                        varDetPnl,
                        {
                            Titulo: If(
                                StartsWith(_c.CarKey, "ID-"),
                                "Carretel não apontado",
                                "Carretel " & _c.CarKey
                            ),
                            Sub: "Esperando a " & _p.Rotulo & "  ·  " & Text(_q.N, "[$-en-US]0") & "º de " &
                            Text(_p.Fila, "[$-en-US]0") & "  ·  " & Text(_c.NOps, "[$-en-US]0") &
                            If(_c.NOps = 1, " OP", " OPs") & "  ·  " & Text(_c.QtdAnterior, "[$-en-US]0") & " m",
                            Estado: "AGUARDANDO",
                            Cor: fx_CorEstadoPosto("AGUARDANDO"),
                            Lado: "OPS NESTE CARRETEL",
                            Maquina: "",
                            Motivo: "",
                            ParadoMin: 0,
                            PausaMin: 0,
                            HHReal: 0,
                            HHMeta: 0
                        }
                    )
                )
            )
        ),
        _q.Tipo = "ACAB" || _q.Tipo = "VULC",
        With(
            { _a: LookUp(colAcabPnl As _x2, _x2.Processo = _q.Chave) },
            If(
                _a.Processo = "Vulcanização",
                Collect(
                    colDetListaPnl,
                    ForAll(colVulcAtivasPnl As _v1, { ID: _v1.ID, Tag: "Na autoclave", Ord: 0 })
                ),
                !IsBlank(_a.IDAtiva),
                Collect(colDetListaPnl, { ID: _a.IDAtiva, Tag: "Em processo", Ord: 0 })
            );
            Collect(
                colDetListaPnl,
                ForAll(
                    Sequence(CountRows(_a.FilaTab)) As _s1,
                    {
                        ID: Index(_a.FilaTab, _s1.Value).ID,
                        Tag: Text(_s1.Value, "[$-en-US]0") & "º na fila",
                        Ord: _s1.Value
                    }
                )
            );
            If(
                _q.Tipo = "VULC",
                Set(varDetIDPnl, Index(colVulcAtivasPnl, _q.N).ID),
                _q.N > 0,
                Set(varDetIDPnl, Index(_a.FilaTab, _q.N).ID)
            );
            Set(
                varDetPnl,
                {
                    Titulo: _a.Rotulo,
                    Sub: If(
                        _a.Processo = "Vulcanização",
                        Text(varVulcQtdPnl, "[$-en-US]0") & " na autoclave",
                        _a.Produzindo,
                        "Em processo há " & fx_CronoLongo(_a.InicioCrono, ctxAgoraPnl),
                        "Sem OP em processo"
                    ) & "  ·  " & Text(_a.Fila, "[$-en-US]0") & " na fila",
                    Estado: _a.Estado,
                    Cor: fx_CorEstadoPosto(_a.Estado),
                    Lado: If(_a.Processo = "Vulcanização", "NA AUTOCLAVE E NA FILA", "EM PROCESSO E NA FILA"),
                    Maquina: "",
                    Motivo: "",
                    ParadoMin: 0,
                    PausaMin: 0,
                    HHReal: 0,
                    HHMeta: 0
                }
            )
        ),
        _q.Tipo = "TUBO",
        If(
            varTuboAtivoPnl,
            Collect(colDetListaPnl, { ID: varTuboIDPnl, Tag: "Na extrusora agora", Ord: 0 })
        );
        Collect(
            colDetListaPnl,
            ForAll(
                Sequence(varFilaTuboPnl) As _s2,
                With(
                    { _t: Index(colFilaTuboPnl, _s2.Value) },
                    {
                        ID: _t.ID,
                        Tag: "Carretel " & fx_Ou(Text(_t.'Carretel Entrada')) & " · " &
                        Text(_s2.Value, "[$-en-US]0") & "º na fila",
                        Ord: _s2.Value
                    }
                )
            )
        );
        If(_q.N > 0, Set(varDetIDPnl, Index(colFilaTuboPnl, _q.N).ID));
        Set(
            varDetPnl,
            {
                Titulo: "Extrusão de Tubo",
                Sub: If(
                    varTuboAtivoPnl,
                    "Extrudando há " & fx_CronoLongo(varTuboInicioPnl, ctxAgoraPnl),
                    "Sem OP em processo"
                ) & "  ·  " & Text(varFilaTuboPnl, "[$-en-US]0") & " na fila",
                Estado: fx_EstadoPosto(varTuboAtivoPnl, varFilaTuboPnl),
                Cor: fx_CorEstadoPosto(fx_EstadoPosto(varTuboAtivoPnl, varFilaTuboPnl)),
                Lado: "NA EXTRUSORA E NA FILA",
                Maquina: "",
                Motivo: "",
                ParadoMin: 0,
                PausaMin: 0,
                HHReal: 0,
                HHMeta: 0
            }
        ),
        _q.Tipo = "EXTR",
        Collect(
            colDetListaPnl,
            ForAll(
                Filter(colPostosExtrPnl As _e1, _e1.Produzindo) As _e2,
                { ID: _e2.IDAtiva, Tag: _e2.Rotulo & " · testando", Ord: 0 }
            )
        );
        Collect(
            colDetListaPnl,
            ForAll(
                Sequence(varFilaExtrPnl) As _s3,
                {
                    ID: Index(colFilaExtrPnl, _s3.Value).ID,
                    Tag: Text(_s3.Value, "[$-en-US]0") & "º na fila",
                    Ord: _s3.Value
                }
            )
        );
        Set(
            varDetPnl,
            {
                Titulo: "Extração / Teste",
                Sub: Text(CountRows(Filter(colPostosExtrPnl As _e3, _e3.Produzindo)), "[$-en-US]0") & " de " &
                Text(CountRows(colPostosExtrPnl), "[$-en-US]0") & " cabines testando  ·  " &
                Text(varFilaExtrPnl, "[$-en-US]0") & " na fila",
                Estado: fx_EstadoPosto(varExtrAtivoPnl, varFilaExtrPnl),
                Cor: fx_CorEstadoPosto(fx_EstadoPosto(varExtrAtivoPnl, varFilaExtrPnl)),
                Lado: "NAS CABINES E NA FILA",
                Maquina: "",
                Motivo: "",
                ParadoMin: 0,
                PausaMin: 0,
                HHReal: 0,
                HHMeta: 0
            }
        ),
        // v0.14.0 · MODO PROCESSO (sem OP tocada): Solda de Mandril, cabecalho da Trancagem e Bobinagem.
        // A ficha abre com o bloco de producao por turno e, quando ha, as OPs em curso do processo.
        _q.Tipo = "MAND",
        Collect(
            colDetListaPnl,
            ForAll(
                Filter(colAtivasPnl As _m2, _m2.processo = "Mandril") As _m3,
                {
                    ID: _m3.ID,
                    Tag: Switch(
                        Text(_m3.maquina_mandril),
                        "TERMOFUSAO", "Quente",
                        "VIBRACIONAL", "Vibracional",
                        "Posto não informado"
                    ) & " · soldando",
                    Ord: 0
                }
            )
        );
        Set(
            varDetPnl,
            {
                Titulo: "Solda de Mandril",
                Sub: Text(CountRows(Filter(colPostosMandPnl As _m4, _m4.Produzindo)), "[$-en-US]0") & " de " &
                Text(CountRows(colPostosMandPnl), "[$-en-US]0") & " soldando",
                Estado: fx_EstadoPosto(varMandAtivoPnl, 0),
                Cor: fx_CorEstadoPosto(fx_EstadoPosto(varMandAtivoPnl, 0)),
                Lado: "SOLDANDO AGORA",
                Maquina: "",
                Motivo: "",
                ParadoMin: 0,
                PausaMin: 0,
                HHReal: 0,
                HHMeta: 0
            }
        ),
        _q.Tipo = "TRANCP",
        Collect(
            colDetListaPnl,
            ForAll(
                Filter(colPostosTrancPnl As _t5, _t5.Produzindo) As _t6,
                {
                    ID: _t6.IDAtiva,
                    Tag: _t6.Rotulo & If(
                        _t6.Estado = "PARADA", " · parada com OP",
                        _t6.Estado = "PAUSA",  " · em pausa",
                        " · trançando"
                    ),
                    Ord: 0
                }
            )
        );
        With(
            {
                _nP: CountRows(Filter(colPostosTrancPnl As _t7, _t7.Estado = "PRODUZINDO")),
                _nX: CountRows(Filter(colPostosTrancPnl As _t8, _t8.Estado = "PARADA"))
            },
            With(
                { _eT: If(_nP > 0, "PRODUZINDO", _nX > 0, "PARADA", "LIVRE") },
                Set(
                    varDetPnl,
                    {
                        Titulo: "Trançagem",
                        Sub: Text(_nP, "[$-en-US]0") & " de " & Text(CountRows(colPostosTrancPnl), "[$-en-US]0") & " trançando" &
                        If(_nX > 0, "  ·  " & Text(_nX, "[$-en-US]0") & " parada(s)", ""),
                        Estado: _eT,
                        Cor: fx_CorEstadoPosto(_eT),
                        Lado: "TRANÇANDO AGORA",
                        Maquina: "",
                        Motivo: "",
                        ParadoMin: 0,
                        PausaMin: 0,
                        HHReal: 0,
                        HHMeta: 0
                    }
                )
            )
        ),
        _q.Tipo = "BOB",
        // Bobinagem nao tem OP na ficha_producao nem evento de producao: so o estado da fifo.
        Set(
            varDetPnl,
            {
                Titulo: "Bobinagem",
                Sub: If(varBobSemFontePnl, "Fifo sem resposta · última leitura", varBobFioPnl) &
                If(IsBlank(varBobInicioPnl), "", "  ·  bobinando há " & fx_CronoLongo(varBobInicioPnl, ctxAgoraPnl)),
                Estado: If(varBobSemFontePnl, "SEM DADO DA FIFO", varBobBadgePnl),
                Cor: If(varBobSemFontePnl, fx_CorTextoSuave, fx_CorEstadoPosto(varBobStatusPnl)),
                Lado: "BOBINAGEM",
                Maquina: "",
                Motivo: "",
                ParadoMin: 0,
                PausaMin: 0,
                HHReal: 0,
                HHMeta: 0
            }
        )
    )
);
// Foco: a bolinha tocada; sem bolinha, o primeiro da lista (quem esta na maquina).
If(
    IsBlank(varDetIDPnl),
    Set(varDetIDPnl, First(Sort(colDetListaPnl, Ord * 1000000 + ID, SortOrder.Ascending)).ID)
);
// Retrato das OPs, com REGISTRO EXPLICITO e UM salto so a partir das colecoes da carga.
// ShowColumns na ficha_producao quebra nome interno (licao v0.7.1 do menu) e coluna que
// passa por colecao e variavel pode ser cortada pelo Explicit Column Selection (doc MS).
// A mesma lista de campos vale para as duas fontes: mexeu numa, mexa na outra.
ClearCollect(
    colDetOPsPnl,
    ForAll(
        Filter(colAtivasPnl As _z1, _z1.ID in colDetListaPnl.ID) As _r,
        {
            ID: _r.ID,
            OP: _r.OP,
            Mangueira: Text(_r.Mangueira),
            Bitola: _r.Bitola,
            Processo: Text(_r.processo),
            Status: Text(_r.status_processo),
            Carretel: Text(_r.'Carretel Entrada'),
            Trancadeira: Text(_r.Trançadeira),
            MaqMand: Text(_r.maquina_mandril),
            Cabine: Text(_r.cabine_teste),
            IniMand: _r.data_hora_inicio_mandril,
            FimMand: _r.data_hora_final_mandril,
            QMand: _r.quantidade_mandril,
            OpMand: Text(_r.operador_mandril),
            LoteMand: Text(_r.lote_mandril),
            IniTubo: _r.data_hora_inicio_tubo,
            FimTubo: _r.data_hora_final_tubo,
            QTubo: _r.quantidade_tubo,
            RefTubo: _r.defeito_tubo,
            OpTubo: Text(_r.operador_tubo),
            CodTubo: Text(_r.'Cod.CompostoTubo'),
            LoteTubo: Text(_r.'Lote Composto Tubo'),
            ValTubo: _r.'Data de Validade do Composto Tubo',
            IniTr: _r.data_hora_inicio_trancadeira,
            FimTr: _r.data_hora_final_trancadeira,
            QTr: _r.quantidade_trancagem,
            RefTr: _r.defeito_trancagem,
            OpTr: Text(_r.operador_trancagem),
            Fio: Text(_r.Cod_Trançagem),
            LI: Text(_r.Lote_Trançagem),
            IniCob: _r.data_hora_inicio_cobertura,
            FimCob: _r.data_hora_final_cobertura,
            QCob: _r.quantidade_cobertura,
            RefCob: _r.defeito_cobertura,
            OpCob: Text(_r.operador_cobertura),
            CodCob: Text(_r.'Cod.Cobertura'),
            LoteCob: Text(_r.Lote_cobertura),
            ValCob: _r.'Data de Validade  do composto cobertura',
            IniBand: _r.data_hora_inicio_bandagem,
            FimBand: _r.data_hora_final_bandagem,
            QBand: _r.quantidade_bandagem,
            OpBand: Text(_r.operador_bandagem),
            IniVulc: _r.data_hora_inicio_vulcanizacao,
            FimVulc: _r.data_hora_final_vulcanizacao,
            QVulc: _r.quantidade_vulcanizacao,
            OpVulc: Text(_r.operador_vulcanizacao),
            IniDeb: _r.data_hora_inicio_debandagem,
            FimDeb: _r.data_hora_final_debandagem,
            QDeb: _r.quantidade_debandagem,
            OpDeb: Text(_r.operador_debandagem),
            IniExt: _r.data_hora_inicio_extracao,
            FimExt: _r.data_hora_final_extracao,
            QExt: Value(Text(_r.quantidade_extracao)),
            OpExt: Text(_r.operador_extracao),
            Obs: Coalesce(_r.Observação_Cobertura, _r.Observação_Trançagem, _r.Observação_tubo, _r.Observação_mandril)
        }
    )
);
Collect(
    colDetOPsPnl,
    ForAll(
        Filter(colAguardPnl As _z2, _z2.ID in colDetListaPnl.ID) As _r,
        {
            ID: _r.ID,
            OP: _r.OP,
            Mangueira: Text(_r.Mangueira),
            Bitola: _r.Bitola,
            Processo: Text(_r.processo),
            Status: Text(_r.status_processo),
            Carretel: Text(_r.'Carretel Entrada'),
            Trancadeira: Text(_r.Trançadeira),
            MaqMand: Text(_r.maquina_mandril),
            Cabine: Text(_r.cabine_teste),
            IniMand: _r.data_hora_inicio_mandril,
            FimMand: _r.data_hora_final_mandril,
            QMand: _r.quantidade_mandril,
            OpMand: Text(_r.operador_mandril),
            LoteMand: Text(_r.lote_mandril),
            IniTubo: _r.data_hora_inicio_tubo,
            FimTubo: _r.data_hora_final_tubo,
            QTubo: _r.quantidade_tubo,
            RefTubo: _r.defeito_tubo,
            OpTubo: Text(_r.operador_tubo),
            CodTubo: Text(_r.'Cod.CompostoTubo'),
            LoteTubo: Text(_r.'Lote Composto Tubo'),
            ValTubo: _r.'Data de Validade do Composto Tubo',
            IniTr: _r.data_hora_inicio_trancadeira,
            FimTr: _r.data_hora_final_trancadeira,
            QTr: _r.quantidade_trancagem,
            RefTr: _r.defeito_trancagem,
            OpTr: Text(_r.operador_trancagem),
            Fio: Text(_r.Cod_Trançagem),
            LI: Text(_r.Lote_Trançagem),
            IniCob: _r.data_hora_inicio_cobertura,
            FimCob: _r.data_hora_final_cobertura,
            QCob: _r.quantidade_cobertura,
            RefCob: _r.defeito_cobertura,
            OpCob: Text(_r.operador_cobertura),
            CodCob: Text(_r.'Cod.Cobertura'),
            LoteCob: Text(_r.Lote_cobertura),
            ValCob: _r.'Data de Validade  do composto cobertura',
            IniBand: _r.data_hora_inicio_bandagem,
            FimBand: _r.data_hora_final_bandagem,
            QBand: _r.quantidade_bandagem,
            OpBand: Text(_r.operador_bandagem),
            IniVulc: _r.data_hora_inicio_vulcanizacao,
            FimVulc: _r.data_hora_final_vulcanizacao,
            QVulc: _r.quantidade_vulcanizacao,
            OpVulc: Text(_r.operador_vulcanizacao),
            IniDeb: _r.data_hora_inicio_debandagem,
            FimDeb: _r.data_hora_final_debandagem,
            QDeb: _r.quantidade_debandagem,
            OpDeb: Text(_r.operador_debandagem),
            IniExt: _r.data_hora_inicio_extracao,
            FimExt: _r.data_hora_final_extracao,
            QExt: Value(Text(_r.quantidade_extracao)),
            OpExt: Text(_r.operador_extracao),
            Obs: Coalesce(_r.Observação_Cobertura, _r.Observação_Trançagem, _r.Observação_tubo, _r.Observação_mandril)
        }
    )
);
// Rota: 8 etapas por OP, do retrato. A galeria so filtra pela OP em foco.
ClearCollect(
    colDetRotaPnl,
    // v0.9.1: OperCurto = primeiro + ultimo nome, para caber na TV.
    AddColumns(
    Ungroup(
        ForAll(
            colDetOPsPnl As _d,
            {
                Linhas: Table(
                    { ID: _d.ID, Ord: 1, Etapa: "Mandril", Proc: "Mandril", Local: Switch(_d.MaqMand, "TERMOFUSAO", "Quente", "VIBRACIONAL", "Vibracional", ""), Ini: _d.IniMand, Fim: _d.FimMand, Mov: Coalesce(_d.FimMand, _d.IniMand), Qtd: _d.QMand, Ref: Blank(), Oper: _d.OpMand },
                    { ID: _d.ID, Ord: 2, Etapa: "Tubo", Proc: "Tubo", Local: "", Ini: _d.IniTubo, Fim: _d.FimTubo, Mov: Coalesce(_d.FimTubo, _d.IniTubo), Qtd: _d.QTubo, Ref: _d.RefTubo, Oper: _d.OpTubo },
                    { ID: _d.ID, Ord: 3, Etapa: "Trançagem", Proc: "Trançadeira", Local: _d.Trancadeira, Ini: _d.IniTr, Fim: _d.FimTr, Mov: Coalesce(_d.FimTr, _d.IniTr), Qtd: _d.QTr, Ref: _d.RefTr, Oper: _d.OpTr },
                    { ID: _d.ID, Ord: 4, Etapa: "Cobertura", Proc: "Cobertura", Local: "", Ini: _d.IniCob, Fim: _d.FimCob, Mov: Coalesce(_d.FimCob, _d.IniCob), Qtd: _d.QCob, Ref: _d.RefCob, Oper: _d.OpCob },
                    { ID: _d.ID, Ord: 5, Etapa: "Bandagem", Proc: "Bandagem", Local: "", Ini: _d.IniBand, Fim: _d.FimBand, Mov: Coalesce(_d.FimBand, _d.IniBand), Qtd: _d.QBand, Ref: Blank(), Oper: _d.OpBand },
                    { ID: _d.ID, Ord: 6, Etapa: "Vulcanização", Proc: "Vulcanização", Local: "", Ini: _d.IniVulc, Fim: _d.FimVulc, Mov: Coalesce(_d.FimVulc, _d.IniVulc), Qtd: _d.QVulc, Ref: Blank(), Oper: _d.OpVulc },
                    { ID: _d.ID, Ord: 7, Etapa: "Debandagem", Proc: "Debandagem", Local: "", Ini: _d.IniDeb, Fim: _d.FimDeb, Mov: Coalesce(_d.FimDeb, _d.IniDeb), Qtd: _d.QDeb, Ref: Blank(), Oper: _d.OpDeb },
                    { ID: _d.ID, Ord: 8, Etapa: "Extração", Proc: "Extr./Teste", Local: Coalesce(LookUp(fx_CabinesTeste As _ct, _ct.Posto = _d.Cabine).Rotulo, ""), Ini: _d.IniExt, Fim: _d.FimExt, Mov: Coalesce(_d.FimExt, _d.IniExt), Qtd: _d.QExt, Ref: Blank(), Oper: _d.OpExt }
                )
            }
        ),
        Linhas
    ),
    OperCurto,
    With(
        { _nm: Split(Trim(Oper), " ") },
        If(
            IsBlank(Trim(Oper)),
            "",
            Proper(First(_nm).Value & If(CountRows(_nm) > 1, " " & Last(_nm).Value, ""))
        )
    )
    )
);
Reset(gal_DetListaPnl);
Set(varDetAbertoPnl, true)
```

## 2. Controles NOVOS (YAML, colar na tela): botões transparentes que abrem a ficha em modo processo
Geometria: btn_FichaMandPnl 16/72 370x140 (card inteiro; nenhum controle clicável por baixo) · btn_FichaTrancPnl 394/72 306x36 (faixa do título; a galeria de postos começa em Y=108) · btn_FichaBobPnl 16/502 181x222 (card inteiro; nenhum controle clicável por baixo).
```yaml
Screens:
  scr_PainelCelula_1:
    Children:
      - btn_FichaMandPnl:
          Control: Classic/Button@2.2.0
          Properties:
            BorderColor: =Color.Transparent
            BorderThickness: =0
            Color: =fx_CorPainelTexto
            Fill: =Color.Transparent
            FocusedBorderThickness: =0
            Font: =fx_FonteFamilia
            Height: =140
            HoverFill: =Color.Transparent
            OnSelect: |-
              =Set(varDetReqPnl, {Tipo: "MAND", Chave: "Mandril", N: 0});
              Select(btn_DetAbrirPnl)
            PressedFill: =fx_CorHoverSutil
            RadiusBottomLeft: =fx_Raio
            RadiusBottomRight: =fx_Raio
            RadiusTopLeft: =fx_Raio
            RadiusTopRight: =fx_Raio
            Text: =""
            Width: =370
            X: =16
            Y: =72
      - btn_FichaTrancPnl:
          Control: Classic/Button@2.2.0
          Properties:
            BorderColor: =Color.Transparent
            BorderThickness: =0
            Color: =fx_CorPainelTexto
            Fill: =Color.Transparent
            FocusedBorderThickness: =0
            Font: =fx_FonteFamilia
            Height: =36
            HoverFill: =Color.Transparent
            OnSelect: |-
              =Set(varDetReqPnl, {Tipo: "TRANCP", Chave: "Trançagem", N: 0});
              Select(btn_DetAbrirPnl)
            PressedFill: =fx_CorHoverSutil
            RadiusBottomLeft: =fx_Raio
            RadiusBottomRight: =fx_Raio
            RadiusTopLeft: =fx_Raio
            RadiusTopRight: =fx_Raio
            Text: =""
            Width: =306
            X: =394
            Y: =72
      - btn_FichaBobPnl:
          Control: Classic/Button@2.2.0
          Properties:
            BorderColor: =Color.Transparent
            BorderThickness: =0
            Color: =fx_CorPainelTexto
            Fill: =Color.Transparent
            FocusedBorderThickness: =0
            Font: =fx_FonteFamilia
            Height: =222
            HoverFill: =Color.Transparent
            OnSelect: |-
              =Set(varDetReqPnl, {Tipo: "BOB", Chave: "Bobinadeira", N: 0});
              Select(btn_DetAbrirPnl)
            PressedFill: =fx_CorHoverSutil
            RadiusBottomLeft: =fx_Raio
            RadiusBottomRight: =fx_Raio
            RadiusTopLeft: =fx_Raio
            RadiusTopRight: =fx_Raio
            Text: =""
            Width: =181
            X: =16
            Y: =502
```

## 3. Controles NOVOS (YAML, colar na tela): bloco de produção da ficha
Geometria (zona livre do cabeçalho da ficha, à direita do título e à esquerda do selo de estado em X=945): caption 597/78 340x16 · 1º 597/96 78x20 · 2º 675/96 78x20 · 3º 753/96 78x20 · DIA 831/96 106x20 · mensagem da Bobinagem 597/96 340x20. Os rótulos ficam por cima do lbl_DetTituloPnl (que tem 760 de largura, mas o texto do título só chega a uns 400 px): confira a olho um título comprido (ex. "Carretel" com código longo). Se encostar, mova os 6 juntos para a direita em até 40 px.
```yaml
Screens:
  scr_PainelCelula_1:
    Children:
      - lbl_DetProdRotPnl:
          Control: Label@2.5.1
          Properties:
            BorderColor: =fx_CorPainelBorda
            Color: =fx_CorRotulo
            Font: =fx_FonteFamilia
            FontWeight: =FontWeight.Bold
            Height: =16
            OnSelect: =Set(varDetToquePnl, Now())
            PaddingLeft: =0
            Size: =fx_FonteApoio
            Text: |-
              ="PRODUÇÃO DO PROCESSO · " & Text(If(ctxModoPnl = "VIVO", fx_DataRefEm(ctxAgoraPnl), ctxDiaPnl), "dd/mm") & " · m" &
              If(ctxModoPnl <> "VIVO" && ctxHistFalhaPnl, " · sem histórico", "")
            Visible: =varDetAbertoPnl
            Width: =340
            X: =597
            Y: =78
      - lbl_DetProdT1Pnl:
          Control: Label@2.5.1
          Properties:
            BorderColor: =fx_CorPainelBorda
            Color: =If((If(ctxModoPnl = "VIVO", fx_TurnoEm(ctxAgoraPnl), fx_TurnoNum(ctxModoPnl)) = 1 || ctxModoPnl = "DIA"), fx_CorPainelTexto, fx_CorPainelTextoRotulo)
            Font: =fx_FonteFamilia
            FontWeight: =If((If(ctxModoPnl = "VIVO", fx_TurnoEm(ctxAgoraPnl), fx_TurnoNum(ctxModoPnl)) = 1 || ctxModoPnl = "DIA"), FontWeight.Bold, FontWeight.Semibold)
            Height: =20
            OnSelect: =Set(varDetToquePnl, Now())
            PaddingLeft: =0
            Size: =fx_FonteCorpo
            Text: |-
              =With(
                  { _v: LookUp(colProdEtapaTurnoPnl As _pt, _pt.Etapa = varDetEtapaPnl).T1 },
                  "1º " & If(
                      (ctxModoPnl = "VIVO" && 1 > fx_TurnoEm(ctxAgoraPnl)) || IsBlank(_v),
                      "—",
                      Substitute(Text(_v, "[$-en-US]#,##0"), ",", ".")
                  )
              )
            Visible: =varDetAbertoPnl && varDetEtapaPnl <> "Bobinadeira"
            Width: =78
            X: =597
            Y: =96
      - lbl_DetProdT2Pnl:
          Control: Label@2.5.1
          Properties:
            BorderColor: =fx_CorPainelBorda
            Color: =If((If(ctxModoPnl = "VIVO", fx_TurnoEm(ctxAgoraPnl), fx_TurnoNum(ctxModoPnl)) = 2 || ctxModoPnl = "DIA"), fx_CorPainelTexto, fx_CorPainelTextoRotulo)
            Font: =fx_FonteFamilia
            FontWeight: =If((If(ctxModoPnl = "VIVO", fx_TurnoEm(ctxAgoraPnl), fx_TurnoNum(ctxModoPnl)) = 2 || ctxModoPnl = "DIA"), FontWeight.Bold, FontWeight.Semibold)
            Height: =20
            OnSelect: =Set(varDetToquePnl, Now())
            PaddingLeft: =0
            Size: =fx_FonteCorpo
            Text: |-
              =With(
                  { _v: LookUp(colProdEtapaTurnoPnl As _pt, _pt.Etapa = varDetEtapaPnl).T2 },
                  "2º " & If(
                      (ctxModoPnl = "VIVO" && 2 > fx_TurnoEm(ctxAgoraPnl)) || IsBlank(_v),
                      "—",
                      Substitute(Text(_v, "[$-en-US]#,##0"), ",", ".")
                  )
              )
            Visible: =varDetAbertoPnl && varDetEtapaPnl <> "Bobinadeira"
            Width: =78
            X: =675
            Y: =96
      - lbl_DetProdT3Pnl:
          Control: Label@2.5.1
          Properties:
            BorderColor: =fx_CorPainelBorda
            Color: =If((If(ctxModoPnl = "VIVO", fx_TurnoEm(ctxAgoraPnl), fx_TurnoNum(ctxModoPnl)) = 3 || ctxModoPnl = "DIA"), fx_CorPainelTexto, fx_CorPainelTextoRotulo)
            Font: =fx_FonteFamilia
            FontWeight: =If((If(ctxModoPnl = "VIVO", fx_TurnoEm(ctxAgoraPnl), fx_TurnoNum(ctxModoPnl)) = 3 || ctxModoPnl = "DIA"), FontWeight.Bold, FontWeight.Semibold)
            Height: =20
            OnSelect: =Set(varDetToquePnl, Now())
            PaddingLeft: =0
            Size: =fx_FonteCorpo
            Text: |-
              =With(
                  { _v: LookUp(colProdEtapaTurnoPnl As _pt, _pt.Etapa = varDetEtapaPnl).T3 },
                  "3º " & If(
                      (ctxModoPnl = "VIVO" && 3 > fx_TurnoEm(ctxAgoraPnl)) || IsBlank(_v),
                      "—",
                      Substitute(Text(_v, "[$-en-US]#,##0"), ",", ".")
                  )
              )
            Visible: =varDetAbertoPnl && varDetEtapaPnl <> "Bobinadeira"
            Width: =78
            X: =753
            Y: =96
      - lbl_DetProdDiaPnl:
          Control: Label@2.5.1
          Properties:
            BorderColor: =fx_CorPainelBorda
            Color: =fx_CorPainelTexto
            Font: =fx_FonteFamilia
            FontWeight: =FontWeight.Bold
            Height: =20
            OnSelect: =Set(varDetToquePnl, Now())
            PaddingLeft: =0
            Size: =fx_FonteCorpo
            Text: |-
              =With(
                  { _v: LookUp(colProdEtapaTurnoPnl As _pt, _pt.Etapa = varDetEtapaPnl).Dia },
                  "DIA " & If(IsBlank(_v), "—", Substitute(Text(_v, "[$-en-US]#,##0"), ",", "."))
              )
            Visible: =varDetAbertoPnl && varDetEtapaPnl <> "Bobinadeira"
            Width: =106
            X: =831
            Y: =96
      - lbl_DetProdSemPnl:
          Control: Label@2.5.1
          Properties:
            BorderColor: =fx_CorPainelBorda
            Color: =fx_CorRotulo
            Font: =fx_FonteFamilia
            FontWeight: =FontWeight.Semibold
            Height: =20
            OnSelect: =Set(varDetToquePnl, Now())
            PaddingLeft: =0
            Size: =fx_FonteCorpo
            Text: ="Sem registro de produção da Bobinagem"
            Visible: =varDetAbertoPnl && varDetEtapaPnl = "Bobinadeira"
            Width: =340
            X: =597
            Y: =96
```

## 4. lbl_VersaoTelaPnl · Text
```
"Versão 0.14.0"
```
