# Patch · Painel da Célula v0.10.3 → v0.11.0 (Fase 2 da Auditoria 26)

Tela publicada com layout ajustado à mão: **colar por bloco na barra de fórmulas, nunca reimportar**. Tela completa (referência e QA): `GMS/Telas/scr_PainelCelula_1.txt` (a cópia de staging ainda não foi para `Telas/`).

Como colar:
- Cada bloco abaixo é o texto da propriedade **inteira, sem o `=` inicial** (a barra de fórmulas já tem o `=`). Selecione o controle (ou, nas galerias, o controle dentro do modelo da galeria), escolha a propriedade e cole.
- Ordem: itens 1 → 7, como estão aqui. Pré-requisito: `Formulas.txt` v3.0.13 (§18) já colada no App.Formulas.
- Variáveis e coleções novas nascem sozinhas no `Set`/`ClearCollect`: `varAgoraPnl`, `varTruncaPnl`, `varCargaOkPnl`, `varCargaSegPnl`, `varAndonPagPnl`, `colEvDiaPnl`, `colBobFifoPnl`. As antigas `colEvVulcPnl`, `colEvMandPnl`, `colEvSaidaPnl` continuam existindo (agora recortadas localmente).
- `btn_RecarregarPnl.OnSelect` é uma propriedade só que os itens 1 a 5 alteram. Para não colar 5 vezes a mesma fórmula, ela entra **uma vez, consolidada, no item 1**, e o log de cada item diz quais trechos dela são dele. Os arquivos `scratchpad\work\snap_item1..7.txt` guardam a tela depois de cada item, caso se queira colar em etapas.
- Toda propriedade citada abaixo que não aparece em nenhum bloco **não mudou**.

---

## Item 1 · Janela atual e início da parada pela grade oficial (A1, M3, M4, M10)

Revisor: sim (turno).

### O que mudou (dentro de `btn_RecarregarPnl.OnSelect`)
- `Set(varAgoraPnl, Now())` é a primeira leitura do ciclo. Todos os `Now()` e `ctxAgoraPnl` que estavam no OnSelect viraram `varAgoraPnl`. Restam 2 `Now()` no OnSelect: o do instante do ciclo e o do medidor de duração (item 2), que só mede, não decide nada.
- `colHHJanPnl` deixou de ler o texto da chave (`"22:00 - 22:20"`). Para cada janela da lista: acha a linha da `fx_GradeHoraHora` pela chave `Hora` + `Turno` e calcula `Ini`/`Fim` com `fx_JanelaHHIni` / `fx_JanelaHHFim` (data de referência do ciclo). `Atual` = ciclo dentro de `[Ini, Fim)`. `Fechada` = ciclo ≥ `Fim`.
- Janela duplicada na lista: fica a de **maior ID** por (Célula, Hora), o mesmo critério do consumo (`colHHConsPnl`).
- `InicioParada` = `Ini` da janela atual (13:57 e 22:41 nas fronteiras), sem `Today() - 1` e sem `IniMin`. A coluna `IniMin` saiu.

### Tabela de conferência para o revisor
Colunas: horário do relógio → turno (`fx_Turno`) → dia de referência (`D` = dia do calendário, `D-1` = ainda é o dia produtivo anterior) → chave `Hora` da janela atual → janela pela grade (início a fim) → o que a v0.10.3 achava como "atual" lendo o texto da chave.

| Relógio | Turno | Dia ref. | Chave Hora (grade) | Janela pela grade | v0.10.3 (texto da chave) |
|---|---|---|---|---|---|
| 05:19 | 3º | D-1 | 05:00 - 05:20 | 05:00 a 05:20 | 05:00 - 05:20 |
| 05:21 | 1º | D | 05:20 - 06:00 | 05:20 a 06:00 | 05:20 - 06:00 |
| 13:56 | 1º | D | 13:00 - 13:57 | 13:00 a 13:57 | 13:00 - 13:57 |
| 13:58 | 2º | D | 13:47 - 15:00 | 13:57 a 15:00 | 13:47 - 15:00 |
| 22:30 | 2º | D | 22:00 - 22:20 | 22:00 a 22:41 | nenhuma |
| 22:42 | 3º | D | 22:20 - 23:00 | 22:41 a 23:00 | 22:20 - 23:00 |
| 23:59 | 3º | D | 23:00 - 00:00 | 23:00 a 00:00 | 23:00 - 00:00 |
| 00:01 | 3º | D-1 | 00:00 - 01:00 | 00:00 a 01:00 | 00:00 - 01:00 |

Leitura: das 22:20 às 22:40 (caso 22:30) a v0.10.3 não achava nenhuma janela atual; agora a de chave `22:00 - 22:20` vai de 22:00 a 22:41. No 13:58 o início da parada passa de 13:47 para 13:57.

### Propriedade (consolidada: contém também os itens 2, 3, 4 e 5)

**`btn_RecarregarPnl` · OnSelect**

```
Set(varFalhaPnl, false);
Set(varTruncaPnl, false);
// v0.11.0 · UM instante por ciclo: toda a carga (turno, janela, data de referencia, consumo,
// andon) usa varAgoraPnl. Antes eram ~25 leituras de Now() misturadas com ctxAgoraPnl.
Set(varAgoraPnl, Now());
// v0.11.0 (item 5 · M11): os Refresh rodam em PARALELO, e nao mais 3 em serie. Cada um fecha
// o IfError com "true" / "false" (licao 2.23: valor e fallback do mesmo tipo).
// v0.11.1: cada ramo do Concurrent grava a SUA flag (varR1..R3Pnl); varFalhaPnl so e escrita
// FORA do Concurrent (o Studio nao aceita a mesma variavel escrita em varios ramos paralelos).
Set(varR1Pnl, false);
Set(varR2Pnl, false);
Set(varR3Pnl, false);
Concurrent(
    IfError(Refresh(ficha_producao); true, Set(varR1Pnl, true); false),
    IfError(Refresh(Eventos_Producao); true, Set(varR2Pnl, true); false),
    IfError(Refresh('Hora-Hora'); true, Set(varR3Pnl, true); false)
);
If(varR1Pnl || varR2Pnl || varR3Pnl, Set(varFalhaPnl, true));
If(
    IsBlank(varVelDiaPnl) || varVelDiaPnl <> fx_DataRefEm(varAgoraPnl),
    IfError(Refresh(DM_TRANÇAGEM); Refresh(DM_ENGRENAGENS); true, Set(varFalhaPnl, true); false)
);
// v0.10.0 · AUTONOMIA DE TUBO (C10 · C23). Velocidade pelo MESMO caminho do Hora-Hora v0.5.9:
// mangueira -> DM_TRANCAGEM._2BRD_CODE -> DM_ENGRENAGENS (maquina + construcao) -> _13TEORICA_M_H.
// Cadastro carregado 1x por dia (ou ao abrir a tela) numa colecao local: o calculo por maquina
// abaixo nao faz NENHUMA chamada de rede. Nunca chamar fx_VelocidadeTeorica aqui: e LookUp no
// SharePoint por linha (11 maquinas x a cada 2 min).
// Ordem externa = DM_TRANCAGEM, igual ao colMangMaqHHT: mangueira com duas construcoes na mesma
// maquina pega a MESMA velocidade que o Hora-Hora pega.
// v0.11.0: (item 5) a chave da DM_TRANCAGEM e normalizada UMA vez por linha, antes do laco, e nao
// a cada linha da DM_ENGRENAGENS; (item 2) o cadastro so e TROCADO se a leitura nova vier cheia
// (antes um ClearCollect com leitura vazia apagava as velocidades) e a leitura grande demais
// acende o aviso de truncamento.
If(
    IsBlank(varVelDiaPnl) || varVelDiaPnl <> fx_DataRefEm(varAgoraPnl),
    IfError(
        With(
            {
                _eng: ForAll(
                    DM_ENGRENAGENS As _e,
                    {
                        MaqN: fx_NormCodigo(_e._4MAQUINA),
                        ConsN: fx_NormCodigo(_e._1CONSTRUCAO),
                        MFG: fx_NumVelocidade(Text(_e._13TEORICA_M_H))
                    }
                ),
                _trc: ForAll(
                    DM_TRANÇAGEM As _d0,
                    {
                        Chave: fx_MangCanon(_d0.PARTNUMBER),
                        ConsN: fx_NormCodigo(_d0._2BRD_CODE)
                    }
                )
            },
            With(
                {
                    _novo: Filter(
                        Ungroup(
                            ForAll(
                                Filter(_trc As _t1, !IsBlank(_t1.Chave) && !IsBlank(_t1.ConsN)) As _d,
                                {
                                    Linhas: ForAll(
                                        Filter(_eng As _e2, _e2.ConsN = _d.ConsN) As _e3,
                                        {
                                            MaqN: _e3.MaqN,
                                            Chave: _d.Chave,
                                            MFG: _e3.MFG
                                        }
                                    )
                                }
                            ),
                            Linhas
                        ),
                        MFG > 0
                    )
                },
                // Leitura vazia (rede caiu): mantem o cadastro anterior, NAO marca o dia e o proximo
                // ciclo de 2 min tenta de novo.
                If(
                    IsEmpty(_novo),
                    Set(varFalhaPnl, true),
                    ClearCollect(colVelTrPnl, _novo);
                    Set(varVelDiaPnl, fx_DataRefEm(varAgoraPnl))
                );
                If(
                    CountRows(_eng) >= fx_PainelLinhasAlerta || CountRows(_trc) >= fx_PainelLinhasAlerta,
                    Set(varTruncaPnl, true)
                );
                true
            )
        ),
        Set(varFalhaPnl, true); false
    )
);
Set(varC1Pnl, false);
Set(varC2Pnl, false);
Set(varC3Pnl, false);
Set(varC4Pnl, false);
Set(varC5Pnl, false);
Set(varC6Pnl, false);
With(
    { _hoje: fx_DataRefEm(varAgoraPnl) },
    // v0.11.0 (item 2 · A3): cada ClearCollect do Concurrent fecha o IfError com "true" / "false".
    // Antes so os Refresh estavam protegidos: carga que falhava deixava varSincPnl avancar e o
    // andon dizia "celula em dia" sem dado.
    Concurrent(
        // v0.10.1: Hora-Hora de ONTEM e de HOJE, uma consulta por dia, em paralelo. Um dia cheio
        // chega a ~300 linhas; dois dias numa consulta so passariam do limite de linhas e a
        // lista viria CORTADA sem aviso. O turno atual (colHHPnl) sai daqui, local, logo abaixo.
        IfError(
            ClearCollect(
                colHHOntemPnl,
                Filter(
                    'Hora-Hora',
                    Data = DateAdd(_hoje, -1, TimeUnit.Days)
                )
            );
            true,
            Set(varC1Pnl, true); false
        ),
        IfError(
            ClearCollect(
                colHHHojePnl,
                Filter(
                    'Hora-Hora',
                    Data = _hoje
                )
            );
            true,
            Set(varC2Pnl, true); false
        ),
        IfError(
            ClearCollect(
                colAtivasPnl,
                Filter(ficha_producao, status_processo = "Em processo")
            );
            true,
            Set(varC3Pnl, true); false
        ),
        IfError(
            ClearCollect(
                colAguardPnl,
                Filter(ficha_producao, status_processo = "Aguardando")
            );
            true,
            Set(varC4Pnl, true); false
        ),
        // v0.11.0 (item 5 · M11): Eventos numa consulta SO (antes 3, com a mesma data). Os tres
        // recortes por etapa (Vulcanizacao, Mandril, Extracao) saem daqui, locais, logo abaixo.
        IfError(
            ClearCollect(
                colEvDiaPnl,
                AddColumns(
                    Filter(
                        Eventos_Producao,
                        data_ref = _hoje
                    ),
                    EtapaTxt,
                    Text(etapa.Value),
                    TipoTxt,
                    Text(tipo.Value),
                    TurnoTxt,
                    Text(turno)
                )
            );
            true,
            Set(varC5Pnl, true); false
        ),
        // v0.11.0 (item 5 · M11): FifoBobinadeira numa consulta so (EP + AB), DENTRO do Concurrent.
        // Falhou = "sem fonte" de verdade (antes varBobSemFontePnl era sempre false).
        IfError(
            ClearCollect(
                colBobFifoPnl,
                Filter(FifoBobinadeira, Status = "EP" || Status = "AB")
            );
            Set(varBobSemFontePnl, false);
            true,
            Set(varBobSemFontePnl, true);
            Set(varC6Pnl, true);
            false
        )
    )
);
If(varC1Pnl || varC2Pnl || varC3Pnl || varC4Pnl || varC5Pnl || varC6Pnl, Set(varFalhaPnl, true));
ClearCollect(colEvVulcPnl, Filter(colEvDiaPnl, EtapaTxt = "Vulcanização"));
ClearCollect(colEvMandPnl, Filter(colEvDiaPnl, EtapaTxt = "Mandril"));
ClearCollect(colEvSaidaPnl, Filter(colEvDiaPnl, EtapaTxt = "Extração"));
// v0.11.0 (item 2 · M12): guarda de truncamento. Lista lida com fx_PainelLinhasAlerta linhas ou
// mais = suspeita de corte no limite do conector: a carga deixa de contar como "ok".
If(
    CountRows(colHHOntemPnl) >= fx_PainelLinhasAlerta ||
    CountRows(colHHHojePnl) >= fx_PainelLinhasAlerta ||
    CountRows(colAtivasPnl) >= fx_PainelLinhasAlerta ||
    CountRows(colAguardPnl) >= fx_PainelLinhasAlerta ||
    CountRows(colEvDiaPnl) >= fx_PainelLinhasAlerta,
    Set(varTruncaPnl, true)
);
ClearCollect(colHH2dPnl, colHHOntemPnl, colHHHojePnl);
ClearCollect(
    colHHPnl,
    Filter(
        colHH2dPnl As _z,
        _z.Data = fx_DataRefEm(varAgoraPnl) && _z.Turno = fx_TurnoLabelEm(varAgoraPnl)
    )
);
// v0.10.1 · CONSUMO DO CARRETEL PELO HORA-HORA (C13 · C10).
// Uma linha por janela de trancadeira: a ULTIMA salva (maior ID) quando a lista tem registro
// duplicado. So fica a janela APONTADA: metro, parada ou motivo. Linha salva vazia (o botao
// repetir pre-preenche a mangueira) nao e apontamento.
ClearCollect(
    colHHConsPnl,
    Filter(
        ForAll(
            GroupBy(
                AddColumns(
                    Filter(colHH2dPnl As _x, Text(_x.Célula) in fx_CelulasTrancagem.Celula),
                    ChaveJan,
                    Text(Célula) & "|" & Text(Data, "yyyy-mm-dd") & "|" & Text(Turno) & "|" & Hora
                ),
                ChaveJan,
                LinhasJan
            ) As _gj,
            With(
                { _r: First(Sort(_gj.LinhasJan, ID, SortOrder.Descending)) },
                {
                    Celula: Text(_r.Célula),
                    DataRef: _r.Data,
                    Turno: fx_TurnoNum(Text(_r.Turno)),
                    Hora: _r.Hora,
                    Real: Coalesce(_r.'Real. Hora', 0),
                    Apontada: Coalesce(_r.'Real. Hora', 0) > 0 ||
                        Coalesce(_r.'Tempo Parado (min)', 0) > 0 ||
                        !IsBlank(Text(_r.Motivo))
                }
            )
        ),
        Apontada
    )
);
// Turnos que tiveram QUALQUER linha no Hora-Hora (criterio ANTIGO da v0.10.3, inclui linha pre-preenchida):
// so o CONSUMO de tubo usa esta colecao (colJanTrPnl.Trabalhado), para a autonomia ficar igual a v0.10.3.
ClearCollect(
    colTurnosHHConsPnl,
    Distinct(
        ForAll(
            colHH2dPnl As _y0,
            { K: Text(_y0.Data, "yyyy-mm-dd") & "|" & Text(fx_TurnoNum(Text(_y0.Turno)), "[$-en-US]0") }
        ),
        K
    )
);
// Turnos TRABALHADOS para o ANDON: tiveram janela APONTADA (metro, parada ou motivo) numa trancadeira.
// Turno sem apontamento nenhum = a fabrica nao rodou (3o turno de 29/09): calam as regras de FILA.
// v0.11.0 (item 3 · M5). NAO e usada no consumo de tubo (ali vale colTurnosHHConsPnl, acima).
ClearCollect(
    colTurnosHHPnl,
    Distinct(
        ForAll(
            colHHConsPnl As _y,
            { K: Text(_y.DataRef, "yyyy-mm-dd") & "|" & Text(_y.Turno, "[$-en-US]0") }
        ),
        K
    )
);
// Grade de janelas de ONTEM e HOJE, com instante de abertura e fechamento. O turno de agora
// conta sempre como trabalhado (as 05:25 ainda ninguem apontou, mas a fabrica esta rodando).
With(
    {
        _dh: fx_DataRefEm(varAgoraPnl),
        _ta: fx_TurnoEm(varAgoraPnl)
    },
    ClearCollect(
        colJanTrPnl,
        ForAll(
            fx_GradeHoraHora As _g1,
            With(
                { _dr1: DateAdd(_dh, -1, TimeUnit.Days) },
                {
                    DataRef: _dr1,
                    Turno: _g1.Turno,
                    Hora: _g1.Hora,
                    Minutos: _g1.Minutos,
                    Ini: fx_JanelaHHIni(_dr1, _g1.Turno, _g1.Fim, _g1.Minutos),
                    Fim: fx_JanelaHHFim(_dr1, _g1.Turno, _g1.Fim),
                    Trabalhado: (Text(_dr1, "yyyy-mm-dd") & "|" & Text(_g1.Turno, "[$-en-US]0")) in colTurnosHHConsPnl.Value
                }
            )
        )
    );
    Collect(
        colJanTrPnl,
        ForAll(
            fx_GradeHoraHora As _g2,
            {
                DataRef: _dh,
                Turno: _g2.Turno,
                Hora: _g2.Hora,
                Minutos: _g2.Minutos,
                Ini: fx_JanelaHHIni(_dh, _g2.Turno, _g2.Fim, _g2.Minutos),
                Fim: fx_JanelaHHFim(_dh, _g2.Turno, _g2.Fim),
                Trabalhado: _g2.Turno = _ta ||
                    (Text(_dh, "yyyy-mm-dd") & "|" & Text(_g2.Turno, "[$-en-US]0")) in colTurnosHHConsPnl.Value
            }
        )
    )
);
// v0.11.0 · JANELA ATUAL PELA GRADE OFICIAL (A1, M3, M4). Antes a janela "atual" era achada lendo o
// TEXTO da chave ("22:00 - 22:20"), que desde a v3.0.5 dura ate 22:41: das 22:20 as 22:40 nenhuma
// janela era "atual" e a trancadeira parada sumia. Agora Ini/Fim vem de fx_GradeHoraHora +
// fx_JanelaHHIni/Fim (mesma regua do Hora-Hora), o instante e o do ciclo (varAgoraPnl) e a janela
// duplicada na lista fica so com a de MAIOR ID (igual ao colHHConsPnl).
With(
    { _dh: fx_DataRefEm(varAgoraPnl) },
    ClearCollect(
        colHHJanPnl,
        ForAll(
            GroupBy(
                AddColumns(colHHPnl, ChaveJan, Text(Célula) & "|" & Hora),
                ChaveJan,
                LinhasJan
            ) As _gj,
            With(
                {
                    _h: First(Sort(_gj.LinhasJan, ID, SortOrder.Descending))
                },
                With(
                    {
                        _gr: LookUp(
                            fx_GradeHoraHora As _gr0,
                            _gr0.Hora = _h.Hora && _gr0.Turno = fx_TurnoNum(Text(_h.Turno))
                        )
                    },
                    With(
                        {
                            _ini: fx_JanelaHHIni(_dh, _gr.Turno, _gr.Fim, _gr.Minutos),
                            _fim: fx_JanelaHHFim(_dh, _gr.Turno, _gr.Fim)
                        },
                        {
                            Celula: Text(_h.Célula),
                            Ini: _ini,
                            Fim: _fim,
                            Atual: !IsBlank(_gr.Fim) && varAgoraPnl >= _ini && varAgoraPnl < _fim,
                            Motivo: Coalesce(Text(_h.Motivo), ""),
                            // v0.11.0 (item 4 · M2): motivo com Tipo "Programada" na fx_MotivosParada
                            // (Refeicao, Reuniao, Set-up, Preventiva, Check List, Amostra, MPT, Teste
                            // Engenharia) e PAUSA, nao parada real.
                            Prog: !IsBlank(Trim(Text(_h.Motivo))) &&
                                LookUp(fx_MotivosParada As _mp, Trim(_mp.Motivo) = Trim(Text(_h.Motivo))).Tipo = "Programada",
                            Parado: Coalesce(_h.'Tempo Parado (min)', 0),
                            // v0.9.0: meta e real da janela para a ficha de consulta.
                            // Janela fechada = o instante do ciclo passou do fim da janela da grade.
                            Meta: Coalesce(_h.'Meta Hora', 0),
                            Real: Coalesce(_h.'Real. Hora', 0),
                            Fechada: !IsBlank(_gr.Fim) && varAgoraPnl >= _fim
                        }
                    )
                )
            )
        )
    )
);
ClearCollect(
    colPostosTrancPnl,
    ForAll(
        Filter(fx_LayoutBalizas, tranc) As _b,
        With(
            {
                _f: LookUp(
                    colAtivasPnl As _a,
                    _a.processo = "Trançadeira" && _a.Trançadeira = _b.Trançadeira
                ),
                // v0.8.1: fila POR CARRETEL, nao por OP. Um carretel de tubo pode
                // levar 2 OPs; contar OP mostrava "tubo atras" quando a 2a OP estava
                // no MESMO carretel que ja roda na maquina. Agrupa pelo 'Carretel
                // Entrada', tira o carretel montado (o da OP Em processo) e cada
                // grupo vira uma bolinha com a soma dos metros. OP sem carretel
                // apontado vira carretel proprio (ID-n): nunca some da fila.
                _fila: With(
                    {
                        _carMaq: Coalesce(
                            Upper(
                                Trim(
                                    LookUp(
                                        colAtivasPnl As _a0,
                                        _a0.processo = "Trançadeira" && _a0.Trançadeira = _b.Trançadeira
                                    ).'Carretel Entrada'
                                )
                            ),
                            ""
                        )
                    },
                    Sort(
                        AddColumns(
                            GroupBy(
                                Filter(
                                    AddColumns(
                                        Filter(
                                            colAguardPnl As _g,
                                            _g.processo = "Trançadeira" && _g.Trançadeira = _b.Trançadeira
                                        ),
                                        CarKey,
                                        Coalesce(
                                            Upper(Trim('Carretel Entrada')),
                                            "ID-" & Text(ID, "[$-en-US]0")
                                        )
                                    ) As _o,
                                    _o.CarKey <> _carMaq
                                ),
                                CarKey,
                                OpsCar
                            ),
                            QtdAnterior,
                            Sum(OpsCar, quantidade_tubo),
                            PrimID,
                            Min(OpsCar, ID),
                            NOps,
                            CountRows(OpsCar)
                        ),
                        PrimID,
                        SortOrder.Ascending
                    )
                )
            },
            With(
                {
                    _n: CountRows(_fila),
                    _ult: LookUp(
                        colHHJanPnl As _j,
                        _j.Celula = _b.Trançadeira && _j.Atual
                    ),
                    // v0.11.0 (item 4): "parado no turno" soma so parada REAL; a pausa programada
                    // (Refeicao, Reuniao...) tem soma propria e nunca entra na parada.
                    _parMin: Sum(
                        Filter(colHHJanPnl As _j2, _j2.Celula = _b.Trançadeira && !_j2.Prog),
                        Parado
                    ),
                    _pauMin: Sum(
                        Filter(colHHJanPnl As _j3, _j3.Celula = _b.Trançadeira && _j3.Prog),
                        Parado
                    ),
                    _maqN: fx_NormCodigo(fx_MaquinaEngrenagens(_b.Trançadeira))
                },
                With(
                {
                    // v0.11.0 (item 4 · M1 · M2 · decisao 1 de 22/10): parada apontada no Hora-Hora
                    // na janela de agora vira PARADA mesmo com OP aberta; motivo Programado vira PAUSA.
                    _est: If(
                        !IsBlank(_ult.Motivo) && _ult.Prog,
                        "PAUSA",
                        !IsBlank(_ult.Motivo),
                        "PARADA",
                        fx_EstadoPosto(!IsBlank(_f.ID), _n)
                    ),
                    // v0.10.0: velocidade da mangueira que esta NA MAQUINA (m/h).
                    // Mesmo envelope do Hora-Hora: sem delineamento, cai no fallback da Spiral.
                    _vAtiva: If(
                        IsBlank(_f.ID),
                        0,
                        Coalesce(
                            LookUp(
                                colVelTrPnl As _v1,
                                _v1.MaqN = _maqN &&
                                _v1.Chave = fx_MangCanon(Text(_f.Mangueira))
                            ).MFG,
                            fx_VelocidadeFallbackSpiral(Text(_f.Mangueira))
                        )
                    ),
                    // v0.10.1: janelas APONTADAS desta maquina (ontem e hoje).
                    _hhMaq: Filter(colHHConsPnl As _hc, _hc.Celula = _b.Trançadeira)
                },
                With(
                {
                    // v0.10.1 · METROS JA CONSUMIDOS do carretel montado, do Inicio da OP ate agora,
                    // janela por janela da grade:
                    //   janela aberta agora ............ velocidade x minutos decorridos
                    //   janela fechada APONTADA ........ o Real apontado (rateado se a OP comecou no meio)
                    //   fechada SEM apontamento, turno
                    //   trabalhado ..................... velocidade x minutos (nao apontou = conta como rodou)
                    //   turno sem linha nenhuma ........ 0 (a fabrica nao rodou)
                    // Antes de ontem 05:20 o Hora-Hora nao foi carregado: ali vale velocidade x relogio.
                    _consM: If(
                        IsBlank(_f.ID) || _vAtiva <= 0 || IsBlank(_f.data_hora_inicio_trancadeira),
                        0,
                        With(
                            {
                                _I: _f.data_hora_inicio_trancadeira,
                                _N: varAgoraPnl,
                                _C: DateAdd(fx_JanelaInicioEm(varAgoraPnl), -1, TimeUnit.Days)
                            },
                            If(_I < _C, _vAtiva * DateDiff(_I, _C, TimeUnit.Minutes) / 60, 0) +
                            Sum(
                                ForAll(
                                    Filter(colJanTrPnl As _w, _w.Fim > _I && _w.Ini < _N) As _w2,
                                    With(
                                        {
                                            _ov: fx_OverlapMin(_w2.Ini, _w2.Fim, _I, _N),
                                            _r: LookUp(
                                                _hhMaq As _hm,
                                                _hm.DataRef = _w2.DataRef && _hm.Turno = _w2.Turno && _hm.Hora = _w2.Hora
                                            )
                                        },
                                        {
                                            M: If(
                                                _w2.Fim > _N,      _vAtiva * _ov / 60,
                                                !IsBlank(_r.Hora), fx_RateioCob(_r.Real, _ov, _w2.Minutos),
                                                _w2.Trabalhado,    _vAtiva * _ov / 60,
                                                0
                                            )
                                        }
                                    )
                                ),
                                M
                            )
                        )
                    ),
                    // Minutos de TODA OP Aguardando desta maquina: a fila por carretel E as OPs que
                    // dividem o carretel montado (saem da fila desde a v0.8.1, mas sao tubo na
                    // maquina). Cada OP na velocidade da propria mangueira; sem velocidade cadastrada,
                    // usa a da mangueira montada.
                    _minFila: Sum(
                        ForAll(
                            Filter(
                                colAguardPnl As _g7,
                                _g7.processo = "Trançadeira" && _g7.Trançadeira = _b.Trançadeira
                            ) As _o7,
                            With(
                                {
                                    _v7: Coalesce(
                                        LookUp(
                                            colVelTrPnl As _v2,
                                            _v2.MaqN = _maqN && _v2.Chave = fx_MangCanon(Text(_o7.Mangueira))
                                        ).MFG,
                                        fx_VelocidadeFallbackSpiral(Text(_o7.Mangueira))
                                    )
                                },
                                With(
                                    { _v8: If(_v7 > 0, _v7, _vAtiva) },
                                    { M: If(_v8 > 0, Coalesce(_o7.quantidade_tubo, 0) * 60 / _v8, 0) }
                                )
                            )
                        ),
                        M
                    )
                },
                With(
                {
                    _restM: If(
                        IsBlank(_f.ID),
                        0,
                        Max(0, Coalesce(_f.quantidade_tubo, 0) - _consM)
                    )
                },
                {
                    Posto: _b.Trançadeira,
                    Rotulo: _b.nome,
                    OP: Coalesce(_f.OP, 0),
                    Mangueira: Coalesce(Text(_f.Mangueira), ""),
                    Inicio: _f.data_hora_inicio_trancadeira,
                    Produzindo: !IsBlank(_f.ID),
                    Estado: _est,
                    Cor: If(_est = "PARADA", fx_CorErro, fx_CorEstadoPosto(_est)),
                    Motivo: If(_est = "PARADA" || _est = "PAUSA", _ult.Motivo, ""),
                    ParadoMin: _parMin,
                    PausaMin: _pauMin,
                    // Inicio da janela parada pela grade oficial (v0.11.0): 13:57 e 22:41 nas fronteiras de turno.
                    InicioParada: If(_est = "PARADA" || _est = "PAUSA", _ult.Ini, Blank()),
                    // Fila = CARRETEIS atras. OpsFila so alimenta o detalhe do andon.
                    Fila: _n,
                    OpsFila: Sum(_fila, NOps),
                    Q1: If(_n >= 1, Last(FirstN(_fila, 1)).QtdAnterior, Blank()),
                    Q2: If(_n >= 2, Last(FirstN(_fila, 2)).QtdAnterior, Blank()),
                    Q3: If(_n >= 3, Last(FirstN(_fila, 3)).QtdAnterior, Blank()),
                    Q4: If(_n >= 4, Last(FirstN(_fila, 4)).QtdAnterior, Blank()),
                    Q5: If(_n >= 5, Last(FirstN(_fila, 5)).QtdAnterior, Blank()),
                    Q6: If(_n >= 6, Last(FirstN(_fila, 6)).QtdAnterior, Blank()),
                    Mais: If(_n > fx_PainelSlotsTranc, _n - fx_PainelSlotsTranc, 0),
                    // v0.9.0: chaves da ficha de consulta. FilaTab guarda os carreteis
                    // (com as OPs dentro) na mesma ordem das bolinhas.
                    IDAtiva: _f.ID,
                    FilaTab: _fila,
                    // v0.10.1: autonomia de tubo no instante da carga (varSincPnl). O label desconta
                    // o relogio da tela (fx_AutonomiaAgora). Blank = sem velocidade cadastrada.
                    VelAtiva: _vAtiva,
                    ConsumidoM: Round(_consM, 0),
                    RestanteM: Round(_restM, 0),
                    // v0.10.2: janelas JA FECHADAS do turno atual sem apontamento desta maquina.
                    SemApontar: CountRows(
                        Filter(
                            colJanTrPnl As _w5,
                            _w5.DataRef = fx_DataRefEm(varAgoraPnl) &&
                            _w5.Turno = fx_TurnoEm(varAgoraPnl) &&
                            _w5.Fim <= varAgoraPnl &&
                            IsBlank(
                                LookUp(
                                    _hhMaq As _hm5,
                                    _hm5.DataRef = _w5.DataRef && _hm5.Turno = _w5.Turno && _hm5.Hora = _w5.Hora
                                ).Hora
                            )
                        )
                    ),
                    AutonomiaMin: If(
                        _vAtiva > 0,
                        Round(_restM * 60 / _vAtiva + _minFila, 0),
                        Blank()
                    )
                }
                )
                )
                )
            )
        )
    )
);
ClearCollect(
    colBitolasPnl,
    ForAll(
        fx_BitolasMandril As _bt,
        With(
            {
                _q: CountRows(
                    Filter(
                        colAguardPnl As _g2,
                        _g2.processo = "Tubo" &&
                        _g2.Bitola = _bt.Bitola &&
                        !IsBlank(_g2.'Carretel Entrada')
                    )
                )
            },
            {
                Bitola: _bt.Bitola,
                Qtd: _q,
                Cor: fx_SemaforoKanban(_q)
            }
        )
    )
);
ClearCollect(
    colAcabPnl,
    ForAll(
        fx_EtapasAcabPainel As _e,
        With(
            {
                _f: LookUp(colAtivasPnl As _a2, _a2.processo = _e.Processo),
                _fila: AddColumns(
                    Sort(
                        Filter(colAguardPnl As _g3, _g3.processo = _e.Processo),
                        ID,
                        SortOrder.Ascending
                    ),
                    QtdAnterior,
                    Switch(
                        _e.Processo,
                        "Cobertura",    quantidade_trancagem,
                        "Bandagem",     quantidade_cobertura,
                        "Vulcanização", quantidade_bandagem,
                        "Debandagem",   quantidade_vulcanizacao
                    )
                )
            },
            With(
                {
                    _n: CountRows(_fila),
                    _ini: Switch(
                        _e.Processo,
                        "Cobertura",    _f.data_hora_inicio_cobertura,
                        "Bandagem",     _f.data_hora_inicio_bandagem,
                        "Vulcanização", _f.data_hora_inicio_vulcanizacao,
                        "Debandagem",   _f.data_hora_inicio_debandagem
                    )
                },
                With(
                    {
                        _est: If(
                            _e.Processo = "Vulcanização" && !IsBlank(_f.ID),
                            fx_EstadoVulca(
                                Text(_f.status_processo),
                                _f.InicioResfriamento_Vulcanizacao,
                                varAgoraPnl
                            ),
                            fx_EstadoPosto(!IsBlank(_f.ID), _n)
                        )
                    },
                    {
                        Ord: _e.Ord,
                        Processo: _e.Processo,
                        Rotulo: _e.Rotulo,
                        OP: Coalesce(_f.OP, 0),
                        Mangueira: Coalesce(Text(_f.Mangueira), ""),
                        Produzindo: !IsBlank(_f.ID),
                        Estado: _est,
                        InicioCrono: If(
                            _est = "RESFRIANDO",
                            _f.InicioResfriamento_Vulcanizacao,
                            _ini
                        ),
                        Fila: _n,
                        Q1: If(_n >= 1, Last(FirstN(_fila, 1)).QtdAnterior, Blank()),
                        Q2: If(_n >= 2, Last(FirstN(_fila, 2)).QtdAnterior, Blank()),
                        Q3: If(_n >= 3, Last(FirstN(_fila, 3)).QtdAnterior, Blank()),
                        Q4: If(_n >= 4, Last(FirstN(_fila, 4)).QtdAnterior, Blank()),
                        Q5: If(_n >= 5, Last(FirstN(_fila, 5)).QtdAnterior, Blank()),
                        Q6: If(_n >= 6, Last(FirstN(_fila, 6)).QtdAnterior, Blank()),
                        Q7: If(_n >= 7, Last(FirstN(_fila, 7)).QtdAnterior, Blank()),
                        Q8: If(_n >= 8, Last(FirstN(_fila, 8)).QtdAnterior, Blank()),
                        Q9: If(_n >= 9, Last(FirstN(_fila, 9)).QtdAnterior, Blank()),
                        Q10: If(_n >= 10, Last(FirstN(_fila, 10)).QtdAnterior, Blank()),
                        Q11: If(_n >= 11, Last(FirstN(_fila, 11)).QtdAnterior, Blank()),
                        Q12: If(_n >= 12, Last(FirstN(_fila, 12)).QtdAnterior, Blank()),
                        Mais: If(_n > fx_PainelSlotsAcab, _n - fx_PainelSlotsAcab, 0),
                        // v0.9.0: chaves da ficha de consulta, na ordem das bolinhas.
                        IDAtiva: _f.ID,
                        FilaTab: ForAll(_fila As _w, { ID: _w.ID })
                    }
                )
            )
        )
    )
);
With(
    {
        _fm: LookUp(colAtivasPnl As _a3, _a3.processo = "Mandril"),
        _ft: LookUp(colAtivasPnl As _a4, _a4.processo = "Tubo"),
        _fe: LookUp(colAtivasPnl As _a5, _a5.processo = "Extr./Teste")
    },
    Set(varMandAtivoPnl, !IsBlank(_fm.ID));
    Set(varTuboOPPnl, Coalesce(_ft.OP, 0));
    Set(varTuboMangPnl, Coalesce(Text(_ft.Mangueira), ""));
    Set(varTuboInicioPnl, _ft.data_hora_inicio_tubo);
    Set(varTuboAtivoPnl, !IsBlank(_ft.ID));
    Set(varTuboIDPnl, _ft.ID);
    Set(varExtrAtivoPnl, !IsBlank(_fe.ID))
);
ClearCollect(
    colFilaExtrPnl,
    Sort(
        Filter(colAguardPnl As _g4, _g4.processo = "Extr./Teste"),
        ID,
        SortOrder.Ascending
    )
);
Set(varFilaExtrPnl, CountRows(colFilaExtrPnl));
// Solda de Mandril e Extracao POR POSTO (v0.8.0, C37). A etapa tem duas
// maquinas fisicas; LookUp de uma OP so mostrava a primeira que achasse.
// Mandril nao tem fila propria (e a 1a etapa): estado = PRODUZINDO ou LIVRE.
ClearCollect(
    colPostosMandPnl,
    ForAll(
        Table(
            { Ord: 1, Posto: "TERMOFUSAO",  Curto: "Quente" },
            { Ord: 2, Posto: "VIBRACIONAL", Curto: "Vibracional" }
        ) As _m,
        With(
            {
                _f: LookUp(
                    colAtivasPnl As _a9,
                    _a9.processo = "Mandril" && _a9.maquina_mandril = _m.Posto
                )
            },
            {
                Ord: _m.Ord,
                Posto: _m.Posto,
                Curto: _m.Curto,
                OP: Coalesce(_f.OP, 0),
                Bitola: Coalesce(_f.Bitola, 0),
                Inicio: _f.data_hora_inicio_mandril,
                Produzindo: !IsBlank(_f.ID),
                Estado: fx_EstadoPosto(!IsBlank(_f.ID), 0)
            }
        )
    )
);
// Extracao: a fila e UMA so para as duas cabines; o estado e por cabine
// (parada com fila acende so na que esta parada).
ClearCollect(
    colPostosExtrPnl,
    ForAll(
        fx_CabinesTeste As _c,
        With(
            {
                _f: LookUp(
                    colAtivasPnl As _a8,
                    _a8.processo = "Extr./Teste" && _a8.cabine_teste = _c.Posto
                )
            },
            {
                Posto: _c.Posto,
                Rotulo: _c.Rotulo,
                Curto: Substitute(_c.Rotulo, "Cabine ", ""),
                OP: Coalesce(_f.OP, 0),
                Mangueira: Coalesce(Text(_f.Mangueira), ""),
                Inicio: _f.data_hora_inicio_extracao,
                Produzindo: !IsBlank(_f.ID),
                Estado: fx_EstadoPosto(!IsBlank(_f.ID), varFilaExtrPnl),
                IDAtiva: _f.ID
            }
        )
    )
);
Set(
    varMandProduzidoPnl,
    Sum(
        Filter(
            colEvMandPnl As _m1,
            _m1.TurnoTxt = Text(fx_TurnoEm(varAgoraPnl), "[$-en-US]0") &&
            (_m1.TipoTxt = "Fim" || _m1.TipoTxt = "Parcial")
        ),
        metros
    )
);
Set(
    varKanbanTuboPnl,
    CountRows(
        Filter(
            colAguardPnl As _g5,
            _g5.processo = "Tubo" && !IsBlank(_g5.'Carretel Entrada')
        )
    )
);
ClearCollect(
    colFilaTuboPnl,
    AddColumns(
        Sort(
            Filter(colAguardPnl As _g6, _g6.processo = "Tubo"),
            ID,
            SortOrder.Ascending
        ),
        QtdAnterior,
        quantidade_mandril
    )
);
Set(varFilaTuboPnl, CountRows(colFilaTuboPnl));
Set(varQT1Pnl, If(varFilaTuboPnl >= 1, Last(FirstN(colFilaTuboPnl, 1)).QtdAnterior, Blank()));
Set(varQT2Pnl, If(varFilaTuboPnl >= 2, Last(FirstN(colFilaTuboPnl, 2)).QtdAnterior, Blank()));
Set(varQT3Pnl, If(varFilaTuboPnl >= 3, Last(FirstN(colFilaTuboPnl, 3)).QtdAnterior, Blank()));
Set(varQT4Pnl, If(varFilaTuboPnl >= 4, Last(FirstN(colFilaTuboPnl, 4)).QtdAnterior, Blank()));
Set(varQT5Pnl, If(varFilaTuboPnl >= 5, Last(FirstN(colFilaTuboPnl, 5)).QtdAnterior, Blank()));
Set(varQT6Pnl, If(varFilaTuboPnl >= 6, Last(FirstN(colFilaTuboPnl, 6)).QtdAnterior, Blank()));
// Bobinagem (v0.7.0) — FifoBobinadeira. AB = pedido aberto, EP = bobinando,
// BC = bobinado, CO = consumido. BC ainda NAO entra: o consumo nao e gravado
// (OP_Consumo vazio), entao BC acumula desde junho. Carrinho fisico entra depois.
// v0.11.0 (item 5): EP e AB vem da UMA consulta da FifoBobinadeira feita no Concurrent (colBobFifoPnl);
// aqui so o recorte local. Falha da consulta = varBobSemFontePnl true (setado la).
ClearCollect(
    colBobEPPnl,
    Sort(Filter(colBobFifoPnl, Status = "EP"), DataHoraInicio, SortOrder.Ascending)
);
Set(varBobAbertosPnl, CountRows(Filter(colBobFifoPnl, Status = "AB")));
Set(varBobCarrinhoPnl, CountRows(colBobEPPnl));
Set(varBobInicioPnl, First(colBobEPPnl).DataHoraInicio);
// Estado no vocabulario do fx_CorEstadoPosto: cor igual as outras etapas.
Set(
    varBobStatusPnl,
    If(varBobCarrinhoPnl > 0, "PRODUZINDO", varBobAbertosPnl > 0, "COM FILA", "LIVRE")
);
Set(
    varBobBadgePnl,
    If(varBobCarrinhoPnl > 0, "BOBINANDO", varBobAbertosPnl > 0, "COM PEDIDO", "LIVRE")
);
Set(
    varBobFioPnl,
    With(
        { _o: First(colBobEPPnl) },
        If(
            varBobCarrinhoPnl > 0,
            _o.Mangueira & " · " & Text(_o.NFios, "[$-en-US]0") & " fios" &
            If(varBobAbertosPnl > 0, "  ·  " & Text(varBobAbertosPnl, "[$-en-US]0") & " aberto(s)", ""),
            varBobAbertosPnl > 0,
            Text(varBobAbertosPnl, "[$-en-US]0") & " pedido(s) aberto(s)",
            "sem pedido na fila"
        )
    )
);
ClearCollect(
    colVulcAtivasPnl,
    AddColumns(
        Sort(
            Filter(colAtivasPnl As _v1, _v1.processo = "Vulcanização"),
            ID,
            SortOrder.Ascending
        ),
        QtdAnterior,
        quantidade_bandagem
    )
);
Set(varVulcQtdPnl, CountRows(colVulcAtivasPnl));
Set(varVQ1Pnl, If(varVulcQtdPnl >= 1, Last(FirstN(colVulcAtivasPnl, 1)).QtdAnterior, Blank()));
Set(varVQ2Pnl, If(varVulcQtdPnl >= 2, Last(FirstN(colVulcAtivasPnl, 2)).QtdAnterior, Blank()));
Set(varVQ3Pnl, If(varVulcQtdPnl >= 3, Last(FirstN(colVulcAtivasPnl, 3)).QtdAnterior, Blank()));
Set(varVQ4Pnl, If(varVulcQtdPnl >= 4, Last(FirstN(colVulcAtivasPnl, 4)).QtdAnterior, Blank()));
Set(varVQ5Pnl, If(varVulcQtdPnl >= 5, Last(FirstN(colVulcAtivasPnl, 5)).QtdAnterior, Blank()));
Set(varVQ6Pnl, If(varVulcQtdPnl >= 6, Last(FirstN(colVulcAtivasPnl, 6)).QtdAnterior, Blank()));
Set(varVQ7Pnl, If(varVulcQtdPnl >= 7, Last(FirstN(colVulcAtivasPnl, 7)).QtdAnterior, Blank()));
Set(varVQ8Pnl, If(varVulcQtdPnl >= 8, Last(FirstN(colVulcAtivasPnl, 8)).QtdAnterior, Blank()));
Set(varVQ9Pnl, If(varVulcQtdPnl >= 9, Last(FirstN(colVulcAtivasPnl, 9)).QtdAnterior, Blank()));
Set(varVQ10Pnl, If(varVulcQtdPnl >= 10, Last(FirstN(colVulcAtivasPnl, 10)).QtdAnterior, Blank()));
Set(varVQ11Pnl, If(varVulcQtdPnl >= 11, Last(FirstN(colVulcAtivasPnl, 11)).QtdAnterior, Blank()));
Set(varVQ12Pnl, If(varVulcQtdPnl >= 12, Last(FirstN(colVulcAtivasPnl, 12)).QtdAnterior, Blank()));
// Bateladas REAIS da Vulcanizacao (v0.6.0).
// Batelada = grupo de "Início" colados no tempo: um Início abre batelada nova
// quando nao houve outro Início nos 30 min anteriores (as 5 OPs de 08:23/08:24
// entram juntas). Maximo de 5 bateladas no dia e 5 carreteis por batelada.
// colGradeVulcPnl so rotula as colunas que ainda nao aconteceram.
ClearCollect(
    colGradeVulcPnl,
    { Ord: 1, Hora: "05:50" },
    { Ord: 2, Hora: "09:20" },
    { Ord: 3, Hora: "12:50" },
    { Ord: 4, Hora: "16:20" },
    { Ord: 5, Hora: "19:50" }
);
With(
    { _dr: fx_DataRefEm(varAgoraPnl) },
    // v0.9.2: cada bolinha e UM carretel, e cada carretel vem de UMA fonte so.
    // Na autoclave agora (ficha Em processo) -> entra pelo inicio gravado na ficha e
    // fica AZUL. Ja saiu -> entra pelo evento de Inicio do dia. Antes a grade lia so
    // evento e o numero lia so ficha: 6 bolinhas contra 5 na autoclave em 25/09.
    ClearCollect(
        colIniVulcPnl,
        ForAll(
            Filter(
                colEvVulcPnl As _ev0,
                _ev0.TipoTxt = "Início" && !(_ev0.origem_ID in colVulcAtivasPnl.ID)
            ) As _ev1,
            { MinIni: DateDiff(_dr, _ev1.data_hora, TimeUnit.Minutes), NaAuto: false }
        )
    );
    Collect(
        colIniVulcPnl,
        ForAll(
            colVulcAtivasPnl As _va,
            {
                MinIni: DateDiff(_dr, Coalesce(_va.data_hora_inicio_vulcanizacao, varAgoraPnl), TimeUnit.Minutes),
                NaAuto: true
            }
        )
    );
    ClearCollect(
        colCabVulcPnl,
        FirstN(
            Sort(
                Distinct(
                    Filter(
                        colIniVulcPnl As _i,
                        IsEmpty(
                            Filter(
                                colIniVulcPnl As _k,
                                _k.MinIni < _i.MinIni && _k.MinIni >= _i.MinIni - 30
                            )
                        )
                    ),
                    MinIni
                ),
                Value,
                SortOrder.Ascending
            ),
            5
        )
    );
    With(
        { _nCab: CountRows(colCabVulcPnl) },
        ClearCollect(
            colBatVulcPnl,
            ForAll(
                Sequence(5) As _s,
                With(
                    {
                        _existe: _s.Value <= _nCab,
                        _de: If(_s.Value <= _nCab, Last(FirstN(colCabVulcPnl, _s.Value)).Value, 0),
                        _ate: If(_s.Value < _nCab, Last(FirstN(colCabVulcPnl, _s.Value + 1)).Value, 99999)
                    },
                    {
                        Ord: _s.Value,
                        Hora: If(
                            _existe,
                            Text(DateAdd(_dr, _de, TimeUnit.Minutes), "hh:mm"),
                            LookUp(colGradeVulcPnl As _gb, _gb.Ord = _s.Value).Hora
                        ),
                        // Autoclave comporta no maximo 5 carreteis por batelada.
                        Qtd: If(
                            _existe,
                            Min(
                                CountRows(
                                    Filter(
                                        colIniVulcPnl As _i2,
                                        _i2.MinIni >= _de && _i2.MinIni < _ate
                                    )
                                ),
                                5
                            ),
                            0
                        ),
                        // v0.9.2: quantos carreteis DESTA batelada ainda estao na autoclave.
                        QtdAuto: If(
                            _existe,
                            Min(
                                CountRows(
                                    Filter(
                                        colIniVulcPnl As _i3,
                                        _i3.NaAuto && _i3.MinIni >= _de && _i3.MinIni < _ate
                                    )
                                ),
                                5
                            ),
                            0
                        ),
                        // v0.9.2: ATUAL = batelada com carretel ainda na autoclave, venha
                        // de onde vier. Batelada antiga com carretel dentro acende azul
                        // tambem: e OP que nao teve o Fim apontado.
                        Estado: If(
                            !_existe, "FUTURA",
                            CountRows(
                                Filter(
                                    colIniVulcPnl As _i4,
                                    _i4.NaAuto && _i4.MinIni >= _de && _i4.MinIni < _ate
                                )
                            ) > 0, "ATUAL",
                            "CONCLUIDA"
                        )
                    }
                )
            )
        )
    )
);
Set(
    varSaidaT1Pnl,
    Sum(
        Filter(
            colEvSaidaPnl As _e1,
            _e1.TurnoTxt = "1" && (_e1.TipoTxt = "Fim" || _e1.TipoTxt = "Parcial")
        ),
        metros
    )
);
Set(
    varSaidaT2Pnl,
    Sum(
        Filter(
            colEvSaidaPnl As _e2,
            _e2.TurnoTxt = "2" && (_e2.TipoTxt = "Fim" || _e2.TipoTxt = "Parcial")
        ),
        metros
    )
);
Set(
    varSaidaT3Pnl,
    Sum(
        Filter(
            colEvSaidaPnl As _e3,
            _e3.TurnoTxt = "3" && (_e3.TipoTxt = "Fim" || _e3.TipoTxt = "Parcial")
        ),
        metros
    )
);
Set(varSaidaDiaPnl, varSaidaT1Pnl + varSaidaT2Pnl + varSaidaT3Pnl);
Set(
    varMaiorFilaPnl,
    Coalesce(
        Text(First(Sort(colAcabPnl, Fila, SortOrder.Descending)).Processo),
        ""
    )
);
// ONDE OLHAR AGORA (v0.11.0 · itens 3 e 4). Todo item leva as mesmas 7 colunas:
//   Sev, Titulo, Detalhe, IdadeMin (ha quantos min o problema existe; 0 = nao medido) e
//   Tipo/Chave/N, que dizem a ficha de consulta o que abrir quando o item e tocado (Tipo vazio = sem ficha).
// Regras de FILA (sem OP + carretel esperando) ficam caladas em turno NAO trabalhado: sem janela
// apontada no turno de agora (criterio "Apontada", mesmo do consumo de tubo). Na 1a janela do turno
// vale a tolerancia (ainda ninguem apontou). Parada apontada, tubo, metragem e OP zumbi nao calam.
With(
    {
        _ta: fx_TurnoEm(varAgoraPnl),
        _dh: fx_DataRefEm(varAgoraPnl)
    },
    With(
        {
            _trab: ((Text(_dh, "yyyy-mm-dd") & "|" & Text(_ta, "[$-en-US]0")) in colTurnosHHPnl.Value) ||
                (fx_MinNoTurno(varAgoraPnl, _ta) < LookUp(fx_GradeHoraHora As _gt, _gt.Turno = _ta && _gt.Ord = 2).Fim)
        },
        // 1 · PARADA apontada no Hora-Hora (com ou sem OP aberta). Pausa programada NAO entra.
        ClearCollect(
            colAndonPnl,
            ForAll(
                Filter(colPostosTrancPnl As _p1, _p1.Estado = "PARADA") As _q1,
                {
                    Sev: 1,
                    Titulo: _q1.Rotulo & " · " & _q1.Motivo,
                    Detalhe: "Parada nesta janela há " & fx_CronoLongo(_q1.InicioParada, varAgoraPnl) &
                    If(_q1.Produzindo, " · OP " & Text(_q1.OP, "[$-en-US]0") & " aberta", "") &
                    If(
                        _q1.Fila > 0,
                        " · " & Text(_q1.Fila, "[$-en-US]0") &
                        If(_q1.Fila = 1, " carretel esperando", " carretéis esperando"),
                        ""
                    ),
                    IdadeMin: Max(0, DateDiff(_q1.InicioParada, varAgoraPnl, TimeUnit.Minutes)),
                    Tipo: "TRANC",
                    Chave: _q1.Posto,
                    N: 0
                }
            )
        );
        // 2 · Trancadeira SEM OP e COM FILA (sem parada nem pausa apontada).
        Collect(
            colAndonPnl,
            ForAll(
                Filter(
                    colPostosTrancPnl As _p1b,
                    _trab && !_p1b.Produzindo && _p1b.Estado = "COM FILA"
                ) As _q1b,
                {
                    Sev: 1,
                    Titulo: _q1b.Rotulo & " sem OP · com fila",
                    Detalhe: Text(_q1b.Fila, "[$-en-US]0") &
                    If(_q1b.Fila = 1, " carretel esperando", " carretéis esperando") &
                    If(
                        _q1b.OpsFila > _q1b.Fila,
                        " · " & Text(_q1b.OpsFila, "[$-en-US]0") & " OPs",
                        ""
                    ),
                    IdadeMin: 0,
                    Tipo: "TRANC",
                    Chave: _q1b.Posto,
                    N: 0
                }
            )
        );
        // 3 · Tubo esgotado pela conta (carretel montado consumido, fila vazia, OP Em processo).
        // O detalhe diz a causa mais provavel: janela do turno sem Hora-Hora.
        Collect(
            colAndonPnl,
            ForAll(
                Filter(
                    colPostosTrancPnl As _p4,
                    _p4.Produzindo && _p4.Estado <> "PARADA" && !IsBlank(_p4.AutonomiaMin) && _p4.AutonomiaMin <= 0
                ) As _q4,
                {
                    Sev: 1,
                    Titulo: _q4.Rotulo & " · tubo esgotado pela conta",
                    Detalhe: If(
                        _q4.SemApontar > 0,
                        Text(_q4.SemApontar, "[$-en-US]0") &
                        If(_q4.SemApontar = 1, " janela sem Hora-Hora", " janelas sem Hora-Hora") &
                        " no turno · apontar e conferir o carretel",
                        "Conferir o carretel na máquina e o Fim da OP"
                    ),
                    IdadeMin: 0,
                    Tipo: "TRANC",
                    Chave: _q4.Posto,
                    N: 0
                }
            )
        );
        // 4 · Mandril abaixo do minimo: UM item so para todas as bitolas (antes eram ate 6, e podiam
        // ocupar os 3 lugares da tela e esconder uma trancadeira parada).
        If(
            CountRows(Filter(colBitolasPnl, Qtd < fx_KanbanMinimo)) > 0,
            Collect(
                colAndonPnl,
                {
                    Sev: 1,
                    Titulo: "Mandril abaixo do mínimo · bitola " &
                    Concat(Filter(colBitolasPnl, Qtd < fx_KanbanMinimo), Text(Bitola, "[$-en-US]0"), ", "),
                    Detalhe: "Fila do Tubo com menos de " & Text(fx_KanbanMinimo, "[$-en-US]0") & " carretéis por bitola",
                    IdadeMin: 0,
                    Tipo: "TUBO",
                    Chave: "Tubo",
                    N: 0
                }
            )
        );
        // 5 · Etapas de acabamento SEM OP e COM FILA.
        Collect(
            colAndonPnl,
            ForAll(
                Filter(colAcabPnl As _a6, _trab && !_a6.Produzindo && _a6.Fila > 0) As _c2,
                {
                    Sev: 2,
                    Titulo: _c2.Rotulo & " sem OP · com fila",
                    Detalhe: Text(_c2.Fila, "[$-en-US]0") & " OP(s) esperando esta etapa",
                    IdadeMin: 0,
                    Tipo: "ACAB",
                    Chave: _c2.Processo,
                    N: 0
                }
            )
        );
        // 6 · Cabine da Extracao sem OP enquanto a fila espera (v0.8.0).
        Collect(
            colAndonPnl,
            ForAll(
                Filter(colPostosExtrPnl As _x1, _trab && !_x1.Produzindo && varFilaExtrPnl > 0) As _c4,
                {
                    Sev: 2,
                    Titulo: _c4.Rotulo & " sem OP · com fila",
                    Detalhe: Text(varFilaExtrPnl, "[$-en-US]0") & " OP(s) esperando a Extração",
                    IdadeMin: 0,
                    Tipo: "EXTR",
                    Chave: "Extr./Teste",
                    N: 0
                }
            )
        );
        // 7 · Tubo para MENOS DE UM TURNO UTIL (substitui a regra "rodando sem carretel atras" da
        // MEL-190, que disparava mesmo com horas de autonomia). Pausa e parada tem regra propria.
        Collect(
            colAndonPnl,
            ForAll(
                Filter(
                    colPostosTrancPnl As _p2,
                    _p2.Produzindo && _p2.Estado <> "PARADA" &&
                    (
                        (!IsBlank(_p2.AutonomiaMin) && _p2.AutonomiaMin > 0 && _p2.AutonomiaMin < fx_TurnoUtilMin) ||
                        (IsBlank(_p2.AutonomiaMin) && _p2.Fila = 0)
                    )
                ) As _q2,
                {
                    Sev: 2,
                    Titulo: _q2.Rotulo & If(IsBlank(_q2.AutonomiaMin), " · sem carretel atrás", " · tubo para menos de 1 turno"),
                    Detalhe: If(
                        IsBlank(_q2.AutonomiaMin),
                        "Sem velocidade cadastrada · sem carretel atrás",
                        "Autonomia " & fx_AutonomiaTexto(_q2.AutonomiaMin) & " · turno útil = " &
                        fx_AutonomiaTexto(fx_TurnoUtilMin)
                    ),
                    IdadeMin: 0,
                    Tipo: "TRANC",
                    Chave: _q2.Posto,
                    N: 0
                }
            )
        );
        // 8 · Metragem do carretel que espera: VAZIA (nao apontada) e IMPLAUSIVEL (apontada, abaixo do
        // minimo) sao problemas diferentes e viram itens diferentes. O metro da bolinha e o que a etapa
        // ANTERIOR apontou; o detalhe diz onde corrigir.
        With(
            {
                _mq: AddColumns(
                    Filter(
                        colAguardPnl As _mq0,
                        _mq0.processo in ["Tubo", "Trançadeira", "Cobertura", "Bandagem", "Vulcanização", "Debandagem"]
                    ),
                    MetrosBol,
                    Switch(
                        processo,
                        "Tubo",         quantidade_mandril,
                        "Trançadeira",  quantidade_tubo,
                        "Cobertura",    quantidade_trancagem,
                        "Bandagem",     quantidade_cobertura,
                        "Vulcanização", quantidade_bandagem,
                        "Debandagem",   quantidade_vulcanizacao
                    ),
                    EtapaAnt,
                    Switch(
                        processo,
                        "Tubo",         "Mandril",
                        "Trançadeira",  "Tubo",
                        "Cobertura",    "Trançagem",
                        "Bandagem",     "Cobertura",
                        "Vulcanização", "Bandagem",
                        "Debandagem",   "Vulcanização"
                    )
                )
            },
            Collect(
                colAndonPnl,
                ForAll(
                    Filter(_mq As _m1, IsBlank(_m1.MetrosBol)) As _c6,
                    {
                        Sev: 2,
                        Titulo: If(_c6.processo = "Trançadeira", Coalesce(Text(_c6.Trançadeira), "Trançagem"), _c6.processo) &
                        " · carretel sem metragem",
                        Detalhe: "OP " & Text(_c6.OP, "[$-en-US]0") & " · metragem do " & _c6.EtapaAnt & " não apontada",
                        IdadeMin: 0,
                        Tipo: Switch(_c6.processo, "Tubo", "TUBO", "Trançadeira", If(IsBlank(Text(_c6.Trançadeira)), "", "TRANC"), "ACAB"),
                        Chave: Switch(_c6.processo, "Tubo", "Tubo", "Trançadeira", Text(_c6.Trançadeira), _c6.processo),
                        N: 0
                    }
                )
            );
            Collect(
                colAndonPnl,
                ForAll(
                    Filter(_mq As _m2, !IsBlank(_m2.MetrosBol) && _m2.MetrosBol < fx_MetrosMinCarretel) As _c5,
                    {
                        Sev: 2,
                        Titulo: If(_c5.processo = "Trançadeira", Coalesce(Text(_c5.Trançadeira), "Trançagem"), _c5.processo) &
                        " · carretel com " & Text(_c5.MetrosBol, "[$-en-US]0") & " m",
                        Detalhe: "OP " & Text(_c5.OP, "[$-en-US]0") & " · metragem do " & _c5.EtapaAnt & " a corrigir na ficha",
                        IdadeMin: 0,
                        Tipo: Switch(_c5.processo, "Tubo", "TUBO", "Trançadeira", If(IsBlank(Text(_c5.Trançadeira)), "", "TRANC"), "ACAB"),
                        Chave: Switch(_c5.processo, "Tubo", "Tubo", "Trançadeira", Text(_c5.Trançadeira), _c5.processo),
                        N: 0
                    }
                )
            )
        );
        // 9 · OP zumbi: acima do teto de horas na mesma etapa.
        Collect(
            colAndonPnl,
            ForAll(
                Filter(
                    colPostosTrancPnl As _p3,
                    _p3.Produzindo &&
                    !IsBlank(_p3.Inicio) &&
                    DateDiff(_p3.Inicio, varAgoraPnl, TimeUnit.Hours) > fx_TetoOPHoras
                ) As _q3,
                {
                    Sev: 3,
                    Titulo: "OP " & Text(_q3.OP, "[$-en-US]0") & " há " & Text(DateDiff(_q3.Inicio, varAgoraPnl, TimeUnit.Hours), "[$-en-US]0") & " h na " & _q3.Rotulo,
                    Detalhe: "Acima do teto de " & Text(fx_TetoOPHoras, "[$-en-US]0") & " h na mesma etapa",
                    IdadeMin: DateDiff(_q3.Inicio, varAgoraPnl, TimeUnit.Minutes),
                    Tipo: "TRANC",
                    Chave: _q3.Posto,
                    N: 0
                }
            )
        );
        Collect(
            colAndonPnl,
            ForAll(
                Filter(
                    colAcabPnl As _a7,
                    _a7.Produzindo &&
                    !IsBlank(_a7.InicioCrono) &&
                    DateDiff(_a7.InicioCrono, varAgoraPnl, TimeUnit.Hours) > fx_TetoOPHoras
                ) As _c3,
                {
                    Sev: 3,
                    Titulo: "OP " & Text(_c3.OP, "[$-en-US]0") & " há " & Text(DateDiff(_c3.InicioCrono, varAgoraPnl, TimeUnit.Hours), "[$-en-US]0") & " h na " & _c3.Rotulo,
                    Detalhe: "Acima do teto de " & Text(fx_TetoOPHoras, "[$-en-US]0") & " h na mesma etapa",
                    IdadeMin: DateDiff(_c3.InicioCrono, varAgoraPnl, TimeUnit.Minutes),
                    Tipo: "ACAB",
                    Chave: _c3.Processo,
                    N: 0
                }
            )
        )
    )
);
Set(varAndonQtdPnl, CountRows(colAndonPnl));
// v0.11.0 (item 2 · A3 · M12): varSincPnl e a ANCORA do calculo (autonomia, retrato da ficha) e
// avanca sempre; a IDADE DO DADO e varUltOkPnl, que so avanca em carga 100% ok (sem falha e sem
// truncamento). "Celula em dia" e o rodape leem varCargaOkPnl / varUltOkPnl.
Set(varSincPnl, varAgoraPnl);
Set(varCargaOkPnl, !varFalhaPnl && !varTruncaPnl);
If(varCargaOkPnl, Set(varUltOkPnl, varAgoraPnl));
// Medidor do ciclo: duracao da carga em segundos (unica leitura de relogio fora do instante do ciclo).
Set(varCargaSegPnl, DateDiff(varAgoraPnl, Now(), TimeUnit.Seconds))
```

---

## Item 2 · Falha visível, idade do dado e medidor do ciclo (A3, M12)

### O que mudou
- (no OnSelect acima) Todo `ClearCollect` do `Concurrent` e os `Refresh` estão em `IfError(...; true, Set(varFalhaPnl, true); false)`: valor e fallback Boolean (lição 2.23, sem `Collect` no fallback).
- Cadastro de velocidade (`colVelTrPnl`, de DM_TRANÇAGEM/DM_ENGRENAGENS): só troca se a leitura nova vier cheia; vazia mantém o cadastro anterior, marca falha e tenta no próximo ciclo.
- Guarda de truncamento com `fx_PainelLinhasAlerta` (1.800) nas listas lidas (Hora-Hora ontem e hoje, ficha Em processo/Aguardando, Eventos do dia, DM_TRANÇAGEM e DM_ENGRENAGENS): `varTruncaPnl`.
- `varCargaOkPnl = !varFalhaPnl && !varTruncaPnl`. `varUltOkPnl` (idade do dado) só avança com carga ok; `varSincPnl` continua sendo a âncora do cálculo (autonomia, retrato da ficha). `varCargaSegPnl` = duração da carga em segundos.
- `OnVisible` zera `varCargaOkPnl`/`varUltOkPnl`: ao abrir o painel diz "carregando…", nunca "célula em dia".
- "Célula em dia" só com carga ok. Sem carga ok: "SEM DADO" (vermelho) ou "carregando…".
- Rodapé: "Dados de HH:mm (há N min) · carga de N s", vermelho quando falha, truncamento ou idade acima de `fx_PainelIdadeAlertaMin`.
- Bobinagem: `varBobSemFontePnl` agora é real (falha da consulta da Fifo). Textos: "SEM DADO DA FIFO" e "Fifo sem resposta · última leitura".
- Sem `Coalesce(x, 0)` em exibição (ver item 3, metragem, e a ficha no item 6), sem `ShowColumns`, sem `Patch` em Timer.

### Propriedades

**`TELA` · OnVisible**

```
UpdateContext({ctxAgoraPnl: Now()});
Set(varDetAbertoPnl, false);
// v0.10.0: abrir a tela recarrega o cadastro de velocidade (DM_*). TV aberta recarrega 1x por dia.
Set(varVelDiaPnl, Blank());
// v0.11.0: ao abrir, o painel NAO esta em dia ate a 1a carga terminar ("carregando", nunca "celula em dia").
Set(varCargaOkPnl, false);
Set(varUltOkPnl, Blank());
Set(varAndonPagPnl, 0);
Select(btn_RecarregarPnl)
```

**`lbl_AndonQtdPnl` · Color**

```
If(
    !varCargaOkPnl, fx_CorPainelTextoErro,
    varAndonQtdPnl > 0, fx_CorPainelTextoAlerta,
    fx_CorPainelTextoOK
)
```

**`lbl_AndonQtdPnl` · Text**

```
If(
    !varCargaOkPnl,
    If(IsBlank(varUltOkPnl) && !varFalhaPnl && !varTruncaPnl, "carregando…", "SEM DADO"),
    varAndonQtdPnl = 0,
    "célula em dia",
    With(
        { _pgs: RoundUp(varAndonQtdPnl / 3, 0) },
        Text(varAndonQtdPnl, "[$-en-US]0") & " abertas" &
        If(
            _pgs > 1,
            " " & Text(Min(If(IsBlank(varAndonPagPnl), 0, varAndonPagPnl), _pgs - 1) + 1, "[$-en-US]0") & "/" & Text(_pgs, "[$-en-US]0"),
            ""
        )
    )
)
```

**`lbl_FontePnl` · Color**

```
If(
    varFalhaPnl || varTruncaPnl ||
    (!IsBlank(varUltOkPnl) && DateDiff(varUltOkPnl, ctxAgoraPnl, TimeUnit.Minutes) > fx_PainelIdadeAlertaMin),
    fx_CorPainelTextoErro,
    fx_CorPainelTextoRotulo
)
```

**`lbl_FontePnl` · Text**

```
If(
    varFalhaPnl || varTruncaPnl,
    "⚠ " & If(varTruncaPnl && !varFalhaPnl, "Lista cortada no limite do conector", "Sem conexão com o servidor") &
    If(IsBlank(varUltOkPnl), "", " — dados de " & Text(varUltOkPnl, "hh:mm")) &
    "  ·  tentando de novo a cada 2 min",
    IsBlank(varUltOkPnl),
    "Carregando os dados…",
    "Dados de " & Text(varUltOkPnl, "hh:mm") & " (há " & Text(DateDiff(varUltOkPnl, ctxAgoraPnl, TimeUnit.Minutes), "[$-en-US]0") &
    " min)  ·  carga de " & Text(varCargaSegPnl, "[$-en-US]0") & " s  ·  toque para detalhar"
)
```

**`lbl_BobNomePnl` · Color**

```
If(varBobSemFontePnl, fx_CorPainelTextoRotulo, fx_CorPainelTexto)
```

**`lbl_BobEstadoPnl` · Color**

```
If(
    varBobSemFontePnl,
    fx_CorPainelTextoErro,
    fx_CorEstadoTextoPainel(varBobStatusPnl)
)
```

**`lbl_BobEstadoPnl` · Text**

```
If(
    varBobSemFontePnl,
    "SEM DADO DA FIFO",
    varBobBadgePnl
)
```

**`lbl_BobFioPnl` · Text**

```
If(
    varBobSemFontePnl,
    "Fifo sem resposta · última leitura",
    varBobFioPnl
)
```

**`lbl_BobCronoPnl` · Color**

```
If(varBobSemFontePnl, fx_CorPainelTextoRotulo, fx_CorPainelTexto)
```

**`lbl_BobCronoPnl` · Text**

```
If(IsBlank(varBobInicioPnl), "--:--", fx_CronoLongo(varBobInicioPnl, ctxAgoraPnl))
```

Verificação (Preview): rede desligada → rodapé vermelho "Sem conexão…" e andon "SEM DADO"; religada → no ciclo seguinte volta ao normal. A cada ciclo o rodapé mostra a duração da carga em segundos (é o medidor para comparar com o item 5).

---

## Item 3 · Andon que não esconde (A2, M5 a M9)

### O que mudou
- (no OnSelect) `colAndonPnl` ganhou 4 colunas: `IdadeMin`, `Tipo`, `Chave`, `N` (esta tríade é o `varDetReqPnl` que a ficha já entende). Regras, nesta ordem: 1 parada apontada · 2 trançadeira sem OP com fila · 3 tubo esgotado · 4 mandril abaixo do mínimo (**um item só** com todas as bitolas) · 5 etapa de acabamento sem OP com fila · 6 cabine da Extração sem OP com fila · 7 tubo para menos de 1 turno útil (**substitui a MEL-190**, `fx_TurnoUtilMin` = 440 min) · 8 metragem **vazia** (item próprio, "carretel sem metragem") e **implausível** (abaixo de `fx_MetrosMinCarretel`, "carretel com N m") · 9 OP zumbi.
- Regras de **fila** (2, 5, 6) ficam caladas em turno não trabalhado. Critério "Apontada": `colTurnosHHPnl` (nova montagem) vem das janelas apontadas (`colHHConsPnl`: metro, parada ou motivo) e serve **só** para calar as regras de fila. O consumo de tubo (autonomia) usa a coleção separada `colTurnosHHConsPnl`, com o critério antigo da v0.10.3 (qualquer linha do turno), então a autonomia não muda. Tolerância: até o fim da 2ª janela do turno (`Ord = 2`) ainda vale como trabalhado.
- Idade do problema: o detalhe da PARADA diz "Parada há hh:mm"; a lista é ordenada por severidade, depois por `IdadeMin` (mais velho primeiro), depois pelo título.
- Páginas: a galeria mostra 3 itens por página e gira a cada 30 s (no `tmr_RelogioPnl`, `varAndonPagPnl`). O contador diz "7 abertas 1/3". Altura, largura e `TemplateSize` da galeria não mudaram.
- Item clicável: toque no item chama a ficha (`varDetReqPnl` + `Select(btn_DetAbrirPnl)`). Para isso, na galeria e nos 2 botões do modelo, `DisplayMode` deixa de ser `View`: **trocar para `DisplayMode.Edit`** em `gal_AndonPnl`, `btn_FundoAnPnl` e `btn_BarraAnPnl` (propriedade removida do YAML = padrão Edit).

### Propriedades (o `OnSelect` consolidado já foi colado no item 1; o contador `lbl_AndonQtdPnl` no item 2)

**`tmr_RelogioPnl` · OnTimerEnd**

```
UpdateContext({ctxAgoraPnl: Now()});
// v0.11.0 (item 3 · A2): o "Onde olhar" gira de 3 em 3 itens a cada 30 s (este timer), em vez de
// cortar em 3 sem avisar. Sem item a mais, fica na pagina 0.
With(
    { _pgs: RoundUp(If(IsBlank(varAndonQtdPnl), 0, varAndonQtdPnl) / 3, 0) },
    Set(
        varAndonPagPnl,
        If(
            _pgs <= 1 || IsBlank(varAndonPagPnl) || varAndonPagPnl + 1 >= _pgs,
            0,
            varAndonPagPnl + 1
        )
    )
);
// v0.9.0: a ficha de consulta fecha sozinha. A TV nao pode ficar presa num modal.
If(
    varDetAbertoPnl && DateDiff(varDetToquePnl, Now(), TimeUnit.Seconds) >= fx_DetFechaSeg,
    Set(varDetAbertoPnl, false)
)
```

**`gal_AndonPnl` · Items**

```
With(
    {
        _ord: SortByColumns(
            colAndonPnl,
            "Sev", SortOrder.Ascending,
            "IdadeMin", SortOrder.Descending,
            "Titulo", SortOrder.Ascending
        )
    },
    With(
        { _n: CountRows(_ord) },
        With(
            { _pg: Min(If(IsBlank(varAndonPagPnl), 0, varAndonPagPnl), Max(0, RoundUp(_n / 3, 0) - 1)) },
            LastN(FirstN(_ord, Min(_n, (_pg + 1) * 3)), Max(0, Min(3, _n - _pg * 3)))
        )
    )
)
```

**`gal_AndonPnl` · OnSelect**

```
If(
    !IsBlank(gal_AndonPnl.Selected.Tipo),
    Set(
        varDetReqPnl,
        {
            Tipo: gal_AndonPnl.Selected.Tipo,
            Chave: gal_AndonPnl.Selected.Chave,
            N: gal_AndonPnl.Selected.N
        }
    );
    Select(btn_DetAbrirPnl)
)
```

**`btn_FundoAnPnl` (controle dentro da galeria `gal_AndonPnl`) · OnSelect**

```
Select(Parent)
```

**`btn_BarraAnPnl` (controle dentro da galeria `gal_AndonPnl`) · OnSelect**

```
Select(Parent)
```

**`lbl_TitAnPnl` (controle dentro da galeria `gal_AndonPnl`) · OnSelect**

```
Select(Parent)
```

**`lbl_DetAnPnl` (controle dentro da galeria `gal_AndonPnl`) · OnSelect**

```
Select(Parent)
```

Também: `gal_AndonPnl.DisplayMode`, `gal_AndonPnl > btn_FundoAnPnl.DisplayMode` e `gal_AndonPnl > btn_BarraAnPnl.DisplayMode` → `DisplayMode.Edit`. Opcional (some o falso positivo do QA): `FocusedBorderThickness` = `0` nos dois botões.

---

## Item 4 · PARADA com OP aberta e PAUSA programada (M1, M2 · decisão 1 do William, 22/10)

Revisor: sim (parada/setup).

### O que mudou
- (no OnSelect) `colHHJanPnl` ganhou `Prog` = o motivo da janela tem `Tipo = "Programada"` na `fx_MotivosParada` (Amostra, Manut. Prod. Total (MPT), Manutenção Preventiva, Set-up, Refeição, Reunião, Execução Check List Lean, TESTE ENGENHARIA). Comparação pelo texto do motivo, com `Trim`.
- Estado da trançadeira: motivo apontado na janela de agora + `Prog` → **PAUSA** (cinza); motivo apontado sem `Prog` → **PARADA**, **com ou sem OP aberta** (antes só sem OP); sem motivo → `fx_EstadoPosto` como sempre. `Produzindo` continua = OP aberta.
- "Parado no turno" (`ParadoMin`) soma só parada real; a pausa tem soma própria (`PausaMin`) e aparece à parte na ficha ("pausa programada: N min"). Parada real nunca soma com pausa. Tempo excedido é conceito da Montagem e não existe nesta tela.
- Andon: PAUSA não gera item. PARADA gera item Sev 1 (item 3, regra 1) com o motivo e há quanto tempo; "tubo esgotado" e "tubo para menos de 1 turno" valem para trançadeira com OP aberta fora de PARADA (inclui PAUSA com OP aberta: nada some do andon).
- Card da trançadeira: cronômetro mostra o tempo parado (vermelho em PARADA, cinza em PAUSA) antes da autonomia; a linha de baixo mostra o motivo (e a OP quando há OP aberta); bolinhas de fila com texto claro sobre fundo vermelho/cinza; "N de 11 trançando" conta só PRODUZINDO.
- Ficha: o subtítulo checa PARADA/PAUSA antes de "Trançando".

### Propriedades (o `OnSelect` consolidado já foi colado no item 1)

**`lbl_TrancResumoPnl` · Text**

```
Text(CountRows(Filter(colPostosTrancPnl, Estado = "PRODUZINDO")), "[$-en-US]0")
& " de "
& Text(CountRows(colPostosTrancPnl), "[$-en-US]0")
& " trançando"
```

**`btn_C1TrPnl` (controle dentro da galeria `gal_TrancPnl`) · Color**

```
If(ThisItem.Estado = "PARADA" || ThisItem.Estado = "PAUSA", fx_CorPainelTexto, fx_CorTexto)
```

**`btn_C2TrPnl` (controle dentro da galeria `gal_TrancPnl`) · Color**

```
If(ThisItem.Estado = "PARADA" || ThisItem.Estado = "PAUSA", fx_CorPainelTexto, fx_CorTexto)
```

**`btn_C3TrPnl` (controle dentro da galeria `gal_TrancPnl`) · Color**

```
If(ThisItem.Estado = "PARADA" || ThisItem.Estado = "PAUSA", fx_CorPainelTexto, fx_CorTexto)
```

**`btn_C4TrPnl` (controle dentro da galeria `gal_TrancPnl`) · Color**

```
If(ThisItem.Estado = "PARADA" || ThisItem.Estado = "PAUSA", fx_CorPainelTexto, fx_CorTexto)
```

**`btn_C5TrPnl` (controle dentro da galeria `gal_TrancPnl`) · Color**

```
If(ThisItem.Estado = "PARADA" || ThisItem.Estado = "PAUSA", fx_CorPainelTexto, fx_CorTexto)
```

**`btn_C6TrPnl` (controle dentro da galeria `gal_TrancPnl`) · Color**

```
If(ThisItem.Estado = "PARADA" || ThisItem.Estado = "PAUSA", fx_CorPainelTexto, fx_CorTexto)
```

**`lbl_CronoTrPnl` (controle dentro da galeria `gal_TrancPnl`) · Color**

```
If(
    ThisItem.Estado = "PARADA",
    fx_CorPainelTextoErro,
    ThisItem.Estado = "PAUSA",
    fx_CorPainelTextoRotulo,
    ThisItem.Produzindo && !IsBlank(ThisItem.AutonomiaMin),
    With(
        { _m: fx_AutonomiaAgora(ThisItem.AutonomiaMin, varSincPnl, ctxAgoraPnl) },
        If(
            _m >= 2 * fx_TurnoUtilMin, fx_CorPainelTextoOK,
            _m >= fx_TurnoUtilMin,     fx_CorPainelTextoAlerta,
            fx_CorPainelTextoErro
        )
    ),
    fx_CorPainelTexto
)
```

**`lbl_CronoTrPnl` (controle dentro da galeria `gal_TrancPnl`) · Text**

```
If(
    (ThisItem.Estado = "PARADA" || ThisItem.Estado = "PAUSA") && !IsBlank(ThisItem.InicioParada),
    fx_CronoLongo(ThisItem.InicioParada, ctxAgoraPnl),
    ThisItem.Produzindo && !IsBlank(ThisItem.AutonomiaMin),
    fx_AutonomiaTexto(fx_AutonomiaAgora(ThisItem.AutonomiaMin, varSincPnl, ctxAgoraPnl)),
    ThisItem.Produzindo,
    "—",
    ""
)
```

**`lbl_SubTrPnl` (controle dentro da galeria `gal_TrancPnl`) · Color**

```
If(
    ThisItem.Estado = "PARADA",   fx_CorPainelTextoErro,
    ThisItem.Estado = "COM FILA", fx_CorPainelTextoAlerta,
    fx_CorPainelTextoRotulo
)
```

**`lbl_SubTrPnl` (controle dentro da galeria `gal_TrancPnl`) · Size**

```
fx_FonteApoio
```

**`lbl_SubTrPnl` (controle dentro da galeria `gal_TrancPnl`) · Text**

```
If(
    ThisItem.Estado = "PARADA" || ThisItem.Estado = "PAUSA",
    ThisItem.Motivo & If(ThisItem.Produzindo, "  ·  OP " & Text(ThisItem.OP, "[$-en-US]0"), ""),
    ThisItem.Produzindo,
    fx_Ou(ThisItem.Mangueira) & "  ·  OP " & Text(ThisItem.OP, "[$-en-US]0"),
    ThisItem.Estado = "COM FILA",
    "Sem OP, com fila",
    "Sem produção no turno"
)
```

**`btn_DetAbrirPnl` · OnSelect**

```
Set(varDetToquePnl, Now());
// v0.9.0 · FICHA DE CONSULTA (C36 · C1 · C21). Toda a busca e LOCAL: le so as colecoes
// que a carga de 2 min ja trouxe (colAtivasPnl, colAguardPnl, colPostos*, colHHJanPnl).
// Zero chamada ao SharePoint no toque, por isso abre na hora. Zero Patch: e consulta.
// Cada controle clicavel so grava varDetReqPnl {Tipo, Chave, N} e chama este botao;
// a logica mora num lugar so.
Set(varDetSincPnl, varSincPnl);
Set(varDetIDPnl, Blank());
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

**`lbl_DetHHPnl` · Text**

```
If(
    varDetPnl.HHMeta > 0,
    "Real " & Text(varDetPnl.HHReal, "[$-en-US]0") & " de " & Text(varDetPnl.HHMeta, "[$-en-US]0") &
    " m nas janelas fechadas  ·  " & Text(fx_RendimentoHH(varDetPnl.HHMeta, varDetPnl.HHReal), "[$-en-US]0") & "%",
    "Nenhuma janela fechada com meta neste turno"
) & Char(10) & "Parado no turno: " & Text(varDetPnl.ParadoMin, "[$-en-US]0") & " min" &
If(varDetPnl.PausaMin > 0, "  ·  pausa programada: " & Text(varDetPnl.PausaMin, "[$-en-US]0") & " min", "") &
If(IsBlank(Trim(varDetPnl.Motivo)), "", "  ·  agora: " & varDetPnl.Motivo)
```

---

## Item 5 · Rede mais leve (M11)

Tudo está dentro do `btn_RecarregarPnl.OnSelect` do item 1; nenhuma outra propriedade muda.
- 3 `Refresh` em série (+ 2 do cadastro, 1× por dia) → **um `Concurrent`** com os 3 (e os 2 do cadastro, quando é dia de recarregar).
- Eventos_Producao: **1 consulta** (`data_ref = dia`, colunas `EtapaTxt`, `TipoTxt`, `TurnoTxt`) em `colEvDiaPnl`; `colEvVulcPnl`, `colEvMandPnl` e `colEvSaidaPnl` saem dela com `Filter` local.
- FifoBobinadeira: **1 consulta** (`Status = "EP" || Status = "AB"`) em `colBobFifoPnl`, **dentro** do `Concurrent`; `colBobEPPnl` e `varBobAbertosPnl` saem dela, locais.
- Chave do DM normalizada **antes** do laço: `fx_MangCanon(PARTNUMBER)` e `fx_NormCodigo(_2BRD_CODE)` uma vez por linha da DM_TRANÇAGEM (`_trc`), e o laço compara só texto já normalizado.
- Removidos os 6 `Set` sem leitor: `varMandOPPnl`, `varMandBitolaPnl`, `varMandInicioPnl`, `varExtrOPPnl`, `varExtrMangPnl`, `varExtrInicioPnl`.
- Chamadas por ciclo: de 12 (3 Refresh em série + 7 consultas + 2 da Fifo) para 9 (3 Refresh em paralelo + 6 consultas no `Concurrent`: Hora-Hora ×2, ficha ×2, Eventos ×1, Fifo ×1). O cadastro DM (2 Refresh + 2 leituras) segue 1× por dia. Mesmos números da v0.10.3 esperados em Preview, com exceção da PARADA com OP aberta (item 4) e das regras novas do andon (itens 3 e 4).

---

## Item 6 · Contraste e rótulos, sem mexer em geometria (A5, M14, M15, parte de M20, baixas de norma)

### O que mudou
- Texto escuro-sobre-escuro: toda propriedade `Color` de texto que usava `fx_CorErro/Alerta/OK/Gelo/Info/TextoSuave/Primaria` ou `fx_CorEstadoPosto(...)` passou para `fx_CorPainelTexto*` / `fx_CorEstadoTextoPainel(...)` (§18). `fx_CorRotulo` ficou (mesmo valor de `fx_CorPainelTextoRotulo`).
- Turno ativo do cabeçalho em branco e negrito; os outros em cinza legível. Valores de T1/T2/T3 com " m" e "—" no turno futuro.
- Card da Extração: "SAÍDA DA CÉLULA NO DIA" → "SAÍDA DO nº TURNO" (turno corrente, mesmo label de 28 pt) com os metros do turno corrente. O "TOTAL DO DIA" do cabeçalho continua o total.
- Legenda: "PARADA COM FILA" → "COM FILA"; 2 controles novos (bolinha vermelha + "PARADA"), YAML abaixo. **PAUSA ficou sem item na legenda**: o espaço livre da legenda existente só comporta um par. A PAUSA se identifica pelo cinza + texto "Pausa programada" na ficha; se o William quiser PAUSA na legenda, precisa de mais 2 controles e de mover um existente (decisão dele).
- Tamanhos escritos à mão trocados por token (sem mudar para fonte de parede, A4 fica fora): 10 → `fx_FonteApoio`, 12 → `fx_FonteCorpo`, 11 → `fx_FonteApoio`; `lbl_TuboNomePnl` ganhou `Size: fx_FonteDestaque` (irmãos estão em 16).
- Timers: NÃO ficam com `Visible: false` (revertido em 27/10: a TV parou de carregar; lição 6.2/MEL-139 não confirmou timer invisível). Voltam ao padrão da v0.10.3 (visível, 1×1 px, X 1360).
- Cronômetros dos cards e da ficha: `fx_Crono` → `fx_CronoLongo` ("3 d 04 h" em vez de travar em "+24 h").
- Ficha: toda label e as 2 galerias de fatos/rota passaram a reiniciar a contagem de fechamento ao toque (`Set(varDetToquePnl, Now())`), não só o fundo.
- `Coalesce(x, 0)` na ficha (condições "vazio ou zero") trocado por `IsBlank(x) || x = 0`.
- Versão: "Versão 0.11.1".

### YAML dos 2 controles novos da legenda
Inserir depois de `lbl_LegFilaPnl`, sem mover nenhum controle existente. Cabem no vão entre o fim do texto "COM FILA" (≈ X 250) e a bolinha "RESFRIANDO" (X 342); a caixa de `lbl_LegFilaPnl` (largura 140) se sobrepõe a eles, mas o texto dela termina antes.

```yaml
      - btn_LegParadaPnl:
          Control: Classic/Button@2.2.0
          Properties:
            BorderColor: =Color.Transparent
            BorderThickness: =0
            DisplayMode: =DisplayMode.View
            Fill: =fx_CorErro
            Font: =fx_FonteFamilia
            Height: =12
            HoverFill: =fx_CorErro
            PressedFill: =fx_CorErro
            RadiusBottomLeft: =fx_RaioG
            RadiusBottomRight: =fx_RaioG
            RadiusTopLeft: =fx_RaioG
            RadiusTopRight: =fx_RaioG
            Text: =""
            Width: =12
            X: =262
            Y: =740
      - lbl_LegParadaPnl:
          Control: Label@2.5.1
          Properties:
            BorderColor: =fx_CorPainelBorda
            Color: =fx_CorPainelTexto
            Font: =fx_FonteFamilia
            FontWeight: =FontWeight.Semibold
            Height: =20
            PaddingLeft: =0
            Size: =fx_FonteApoio
            Text: ="PARADA"
            Width: =62
            X: =280
            Y: =736
```

### Propriedades

**`tmr_DadosPnl` · Visible** (REVERTIDO: deixar `true`, como na v0.10.3)

```
true
```

**`tmr_RelogioPnl` · Visible** (REVERTIDO: deixar `true`, como na v0.10.3)

```
true
```

**`lbl_T1RotPnl` · Color**

```
If(fx_TurnoEm(ctxAgoraPnl) = 1, fx_CorPainelTexto, fx_CorPainelTextoRotulo)
```

**`lbl_T1Pnl` · Color**

```
If(fx_TurnoEm(ctxAgoraPnl) = 1, fx_CorPainelTexto, fx_CorPainelTextoRotulo)
```

**`lbl_T1Pnl` · Text**

```
If(1 > fx_TurnoEm(ctxAgoraPnl), "—", Substitute(Text(varSaidaT1Pnl, "[$-en-US]#,##0"), ",", ".") & " m")
```

**`lbl_T2RotPnl` · Color**

```
If(fx_TurnoEm(ctxAgoraPnl) = 2, fx_CorPainelTexto, fx_CorPainelTextoRotulo)
```

**`lbl_T2Pnl` · Color**

```
If(fx_TurnoEm(ctxAgoraPnl) = 2, fx_CorPainelTexto, fx_CorPainelTextoRotulo)
```

**`lbl_T2Pnl` · Text**

```
If(2 > fx_TurnoEm(ctxAgoraPnl), "—", Substitute(Text(varSaidaT2Pnl, "[$-en-US]#,##0"), ",", ".") & " m")
```

**`lbl_T3RotPnl` · Color**

```
If(fx_TurnoEm(ctxAgoraPnl) = 3, fx_CorPainelTexto, fx_CorPainelTextoRotulo)
```

**`lbl_T3Pnl` · Color**

```
If(fx_TurnoEm(ctxAgoraPnl) = 3, fx_CorPainelTexto, fx_CorPainelTextoRotulo)
```

**`lbl_T3Pnl` · Text**

```
If(3 > fx_TurnoEm(ctxAgoraPnl), "—", Substitute(Text(varSaidaT3Pnl, "[$-en-US]#,##0"), ",", ".") & " m")
```

**`lbl_TotalRotPnl` · Size**

```
fx_FonteApoio
```

**`lbl_SoldaEstadoPnl` · Color**

```
fx_CorEstadoTextoPainel(fx_EstadoPosto(varMandAtivoPnl, 0))
```

**`lbl_SoldaAInfoPnl` · Color**

```
With(
    { _p: Index(colPostosMandPnl, 1) },
    If(
        _p.Produzindo,          fx_CorPainelTexto,
        _p.Estado = "COM FILA", fx_CorPainelTextoAlerta,
        fx_CorRotulo
    )
)
```

**`lbl_SoldaACronoPnl` · Text**

```
If(Index(colPostosMandPnl, 1).Produzindo, fx_CronoLongo(Index(colPostosMandPnl, 1).Inicio, ctxAgoraPnl), "")
```

**`lbl_SoldaBInfoPnl` · Color**

```
With(
    { _p: Index(colPostosMandPnl, 2) },
    If(
        _p.Produzindo,          fx_CorPainelTexto,
        _p.Estado = "COM FILA", fx_CorPainelTextoAlerta,
        fx_CorRotulo
    )
)
```

**`lbl_SoldaBCronoPnl` · Text**

```
If(Index(colPostosMandPnl, 2).Produzindo, fx_CronoLongo(Index(colPostosMandPnl, 2).Inicio, ctxAgoraPnl), "")
```

**`lbl_KanbanValPnl` · Color**

```
If(
    varKanbanTuboPnl >= fx_KanbanAlvo,   fx_CorPainelTextoOK,
    varKanbanTuboPnl >= fx_KanbanMinimo, fx_CorPainelTextoAlerta,
    fx_CorPainelTextoErro
)
```

**`lbl_BitTituloPnl` · Size**

```
fx_FonteApoio
```

**`btn_CircBitPnl` (controle dentro da galeria `gal_BitolasPnl`) · Size**

```
fx_FonteCorpo
```

**`lbl_QtdBitPnl` (controle dentro da galeria `gal_BitolasPnl`) · Color**

```
If(
    ThisItem.Qtd >= fx_KanbanAlvo,   fx_CorPainelTextoOK,
    ThisItem.Qtd >= fx_KanbanMinimo, fx_CorPainelTextoAlerta,
    fx_CorPainelTextoErro
)
```

**`lbl_TuboNomePnl` · Size**

```
fx_FonteDestaque
```

**`lbl_TuboEstadoPnl` · Color**

```
fx_CorEstadoTextoPainel(fx_EstadoPosto(varTuboAtivoPnl, varFilaTuboPnl))
```

**`lbl_TuboFilaValPnl` · Color**

```
If(varFilaTuboPnl > 0, fx_CorPainelTextoAlerta, fx_CorRotulo)
```

**`lbl_TuboCronoPnl` · Text**

```
If(varTuboAtivoPnl, fx_CronoLongo(varTuboInicioPnl, ctxAgoraPnl), "--:--")
```

**`lbl_EstadoAcPnl` (controle dentro da galeria `gal_AcabPnl`) · Color**

```
fx_CorEstadoTextoPainel(ThisItem.Estado)
```

**`lbl_InfoAcPnl` (controle dentro da galeria `gal_AcabPnl`) · Size**

```
fx_FonteCorpo
```

**`lbl_FilaAcPnl` (controle dentro da galeria `gal_AcabPnl`) · Color**

```
If(ThisItem.Fila > 0, fx_CorPainelTextoAlerta, fx_CorRotulo)
```

**`lbl_CronoAcPnl` (controle dentro da galeria `gal_AcabPnl`) · Text**

```
If(ThisItem.Produzindo, fx_CronoLongo(ThisItem.InicioCrono, ctxAgoraPnl), "--:--")
```

**`btn_VBadgeAcPnl` (controle dentro da galeria `gal_AcabPnl`) · Text**

```
ThisItem.Estado & If(
    ThisItem.Produzindo,
    "  " & fx_CronoLongo(ThisItem.InicioCrono, ctxAgoraPnl),
    ""
)
```

**`lbl_VFilaAcPnl` (controle dentro da galeria `gal_AcabPnl`) · Color**

```
If(ThisItem.Processo = varMaiorFilaPnl && ThisItem.Fila > 0, fx_CorPainelTextoErro, If(ThisItem.Fila > 0, fx_CorPainelTextoAlerta, fx_CorRotulo))
```

**`lbl_BatH1Pnl` · Color**

```
If(LookUp(colBatVulcPnl, Ord = 1).Estado = "ATUAL", fx_CorPainelTextoGelo, fx_CorRotulo)
```

**`lbl_BatH2Pnl` · Color**

```
If(LookUp(colBatVulcPnl, Ord = 2).Estado = "ATUAL", fx_CorPainelTextoGelo, fx_CorRotulo)
```

**`lbl_BatH3Pnl` · Color**

```
If(LookUp(colBatVulcPnl, Ord = 3).Estado = "ATUAL", fx_CorPainelTextoGelo, fx_CorRotulo)
```

**`lbl_BatH4Pnl` · Color**

```
If(LookUp(colBatVulcPnl, Ord = 4).Estado = "ATUAL", fx_CorPainelTextoGelo, fx_CorRotulo)
```

**`lbl_BatH5Pnl` · Color**

```
If(LookUp(colBatVulcPnl, Ord = 5).Estado = "ATUAL", fx_CorPainelTextoGelo, fx_CorRotulo)
```

**`lbl_BatQtdRotPnl` · Color**

```
fx_CorPainelTextoGelo
```

**`lbl_ExtrEstadoPnl` · Color**

```
If(varFilaExtrPnl > 0, fx_CorPainelTextoAlerta, fx_CorRotulo)
```

**`lbl_ExtrL1InfoPnl` · Color**

```
With(
    { _p: Index(colPostosExtrPnl, 1) },
    If(
        _p.Produzindo,          fx_CorPainelTexto,
        _p.Estado = "COM FILA", fx_CorPainelTextoAlerta,
        fx_CorRotulo
    )
)
```

**`lbl_ExtrL1InfoPnl` · Size**

```
fx_FonteApoio
```

**`lbl_ExtrL1CronoPnl` · Text**

```
If(Index(colPostosExtrPnl, 1).Produzindo, fx_CronoLongo(Index(colPostosExtrPnl, 1).Inicio, ctxAgoraPnl), "")
```

**`lbl_ExtrL2InfoPnl` · Color**

```
With(
    { _p: Index(colPostosExtrPnl, 2) },
    If(
        _p.Produzindo,          fx_CorPainelTexto,
        _p.Estado = "COM FILA", fx_CorPainelTextoAlerta,
        fx_CorRotulo
    )
)
```

**`lbl_ExtrL2InfoPnl` · Size**

```
fx_FonteApoio
```

**`lbl_ExtrL2CronoPnl` · Text**

```
If(Index(colPostosExtrPnl, 2).Produzindo, fx_CronoLongo(Index(colPostosExtrPnl, 2).Inicio, ctxAgoraPnl), "")
```

**`lbl_SaidaRotPnl` · Text**

```
"SAÍDA DO " & Text(fx_TurnoEm(ctxAgoraPnl), "[$-en-US]0") & "º TURNO"
```

**`lbl_SaidaValPnl` · Text**

```
Substitute(
    Text(
        Switch(fx_TurnoEm(ctxAgoraPnl), 1, varSaidaT1Pnl, 2, varSaidaT2Pnl, varSaidaT3Pnl),
        "[$-en-US]#,##0"
    ),
    ",", "."
) & " m"
```

**`lbl_LegFilaPnl` · Text**

```
"COM FILA"
```

**`lbl_VersaoTelaPnl` · Color**

```
fx_CorPainelTextoRotulo
```

**`lbl_VersaoTelaPnl` · Text**

```
"Versão 0.11.1"
```

**`lbl_DetTituloPnl` · OnSelect**

```
Set(varDetToquePnl, Now())
```

**`lbl_DetSubPnl` · OnSelect**

```
Set(varDetToquePnl, Now())
```

**`lbl_DetOPRotPnl` · OnSelect**

```
Set(varDetToquePnl, Now())
```

**`lbl_DetOPPnl` · OnSelect**

```
Set(varDetToquePnl, Now())
```

**`lbl_DetOPPnl` · Text**

```
With(
    { _r: LookUp(colDetOPsPnl As _d1, _d1.ID = varDetIDPnl) },
    If(
        IsBlank(_r.ID),
        "Nenhuma OP nesta posição",
        If((IsBlank(_r.OP) || _r.OP = 0), "OP não informada", "OP " & Text(_r.OP, "[$-en-US]0")) &
        "  ·  " & fx_Ou(_r.Mangueira)
    )
)
```

**`gal_DetFatosPnl` · Items**

```
With(
    { _r: LookUp(colDetOPsPnl As _d2, _d2.ID = varDetIDPnl) },
    With(
        {
            _mov: First(
                Sort(
                    Filter(colDetRotaPnl As _t3, _t3.ID = varDetIDPnl && !IsBlank(_t3.Mov)),
                    Mov,
                    SortOrder.Descending
                )
            ),
            _ref: Sum(Filter(colDetRotaPnl As _t4, _t4.ID = varDetIDPnl), Coalesce(Ref, 0)),
            // Composto usado vencido: validade ANTERIOR ao inicio da etapa que o consumiu.
            _tuboVenc: !IsBlank(_r.ValTubo) && !IsBlank(_r.IniTubo) && DateDiff(_r.ValTubo, _r.IniTubo, TimeUnit.Days) > 0,
            _cobVenc: !IsBlank(_r.ValCob) && !IsBlank(_r.IniCob) && DateDiff(_r.ValCob, _r.IniCob, TimeUnit.Days) > 0
        },
        Table(
            { Rot: "BITOLA", Val: If((IsBlank(_r.Bitola) || _r.Bitola = 0), "—", "−" & Text(_r.Bitola, "[$-en-US]0")), Alerta: false },
            { Rot: "CARRETEL", Val: fx_Ou(_r.Carretel), Alerta: false },
            {
                Rot: "ONDE ESTÁ",
                Val: If(
                    _r.Status = "Aguardando", "Fila · " & fx_Ou(_r.Processo),
                    _r.Status = "Em processo", fx_Ou(_r.Processo) & " · rodando",
                    fx_Ou(_r.Processo) & " · " & fx_Ou(_r.Status)
                ),
                Alerta: false
            },
            {
                Rot: "NESTE ESTADO HÁ",
                Val: If(IsBlank(_mov.Mov), "—", fx_CronoLongo(_mov.Mov, ctxAgoraPnl)),
                Alerta: !IsBlank(_mov.Mov) && DateDiff(_mov.Mov, ctxAgoraPnl, TimeUnit.Hours) > fx_TetoOPHoras
            },
            { Rot: "IDADE DA OP", Val: If(IsBlank(_r.IniMand), "—", fx_CronoLongo(_r.IniMand, ctxAgoraPnl)), Alerta: false },
            { Rot: "REFUGO NA ROTA", Val: If(_ref > 0, Text(_ref, "[$-en-US]0") & " m", "0"), Alerta: _ref > 0 },
            {
                Rot: If(_tuboVenc, "TUBO VENCIDO NO USO", "COMPOSTO DO TUBO"),
                Val: fx_Ou(_r.CodTubo) & If(IsBlank(_r.ValTubo), "", " · val. " & Text(_r.ValTubo, "dd/mm")),
                Alerta: _tuboVenc
            },
            { Rot: "FIO · LI", Val: fx_Ou(_r.Fio) & " · " & fx_Ou(_r.LI), Alerta: false },
            {
                Rot: If(_cobVenc, "COBERT. VENCIDA NO USO", "COMPOSTO DA COBERTURA"),
                Val: fx_Ou(_r.CodCob) & If(IsBlank(_r.ValCob), "", " · val. " & Text(_r.ValCob, "dd/mm")),
                Alerta: _cobVenc
            },
            { Rot: "LOTE DO MANDRIL", Val: fx_Ou(_r.LoteMand), Alerta: false },
            { Rot: "ÚLTIMO OPERADOR", Val: fx_Ou(_mov.OperCurto), Alerta: false },
            { Rot: "OBSERVAÇÃO", Val: fx_Ou(_r.Obs), Alerta: false }
        )
    )
)
```

**`gal_DetFatosPnl` · OnSelect**

```
Set(varDetToquePnl, Now())
```

**`lbl_DetFatoRotPnl` (controle dentro da galeria `gal_DetFatosPnl`) · Color**

```
If(ThisItem.Alerta, fx_CorPainelTextoErro, fx_CorRotulo)
```

**`lbl_DetFatoRotPnl` (controle dentro da galeria `gal_DetFatosPnl`) · Size**

```
fx_FonteApoio
```

**`lbl_DetFatoValPnl` (controle dentro da galeria `gal_DetFatosPnl`) · Color**

```
If(ThisItem.Alerta, fx_CorPainelTextoErro, fx_CorPainelTexto)
```

**`lbl_DetFatoValPnl` (controle dentro da galeria `gal_DetFatosPnl`) · Size**

```
fx_FonteApoio
```

**`lbl_DetRotaRotPnl` · OnSelect**

```
Set(varDetToquePnl, Now())
```

**`lbl_DetColQtdPnl` · OnSelect**

```
Set(varDetToquePnl, Now())
```

**`lbl_DetColRefPnl` · OnSelect**

```
Set(varDetToquePnl, Now())
```

**`lbl_DetColEspPnl` · OnSelect**

```
Set(varDetToquePnl, Now())
```

**`lbl_DetColDurPnl` · OnSelect**

```
Set(varDetToquePnl, Now())
```

**`lbl_DetColOperPnl` · OnSelect**

```
Set(varDetToquePnl, Now())
```

**`gal_DetRotaPnl` · Items**

```
With(
    { _r: LookUp(colDetOPsPnl As _d4, _d4.ID = varDetIDPnl) },
    AddColumns(
        Sort(Filter(colDetRotaPnl As _t7, _t7.ID = varDetIDPnl), Ord, SortOrder.Ascending),
        Sit,
        If(
            !IsBlank(Fim), "FEITA",
            !IsBlank(Ini), "EM CURSO",
            Proc = _r.Processo && _r.Status = "Aguardando", "NA FILA",
            ""
        ),
        // Espera = fim da etapa anterior ate o inicio desta (ou ate agora, se esta na fila dela).
        Espera,
        With(
            { _o: ThisRecord },
            With(
                { _ant: LookUp(colDetRotaPnl As _t8, _t8.ID = varDetIDPnl && _t8.Ord = _o.Ord - 1) },
                If(
                    IsBlank(_ant.Fim), "",
                    !IsBlank(_o.Ini), fx_CronoLongo(_ant.Fim, _o.Ini),
                    _o.Proc = _r.Processo, fx_CronoLongo(_ant.Fim, ctxAgoraPnl),
                    ""
                )
            )
        ),
        Dur,
        If(IsBlank(Ini), "", fx_CronoLongo(Ini, Coalesce(Fim, ctxAgoraPnl)))
    )
)
```

**`gal_DetRotaPnl` · OnSelect**

```
Set(varDetToquePnl, Now())
```

**`lbl_DetRotaQtdPnl` (controle dentro da galeria `gal_DetRotaPnl`) · Text**

```
If((!IsBlank(ThisItem.Qtd) && ThisItem.Qtd > 0), Text(ThisItem.Qtd, "[$-en-US]0"), "—")
```

**`lbl_DetRotaRefPnl` (controle dentro da galeria `gal_DetRotaPnl`) · Color**

```
If((!IsBlank(ThisItem.Ref) && ThisItem.Ref > 0), fx_CorPainelTextoErro, fx_CorRotulo)
```

**`lbl_DetRotaRefPnl` (controle dentro da galeria `gal_DetRotaPnl`) · Text**

```
If((!IsBlank(ThisItem.Ref) && ThisItem.Ref > 0), Text(ThisItem.Ref, "[$-en-US]0"), "—")
```

**`lbl_DetRotaEspPnl` (controle dentro da galeria `gal_DetRotaPnl`) · Color**

```
If(ThisItem.Sit = "NA FILA", fx_CorPainelTextoAlerta, fx_CorPainelTexto)
```

**`lbl_DetRotaDurPnl` (controle dentro da galeria `gal_DetRotaPnl`) · Color**

```
If(ThisItem.Sit = "EM CURSO", fx_CorPainelTextoOK, fx_CorPainelTexto)
```

**`lbl_DetLadoPnl` · OnSelect**

```
Set(varDetToquePnl, Now())
```

**`lbl_DetLadoPnl` · Text**

```
varDetPnl.Lado & "  ·  " & Text(CountRows(colDetListaPnl), "[$-en-US]0") & " OP(s)" &
With(
    {
        _tot: Sum(
            ForAll(
                colDetListaPnl As _l,
                {
                    Q: First(
                        Sort(
                            Filter(colDetRotaPnl As _t7, _t7.ID = _l.ID && (!IsBlank(_t7.Qtd) && _t7.Qtd > 0)),
                            Ord,
                            SortOrder.Descending
                        )
                    ).Qtd
                }
            ),
            Q
        )
    },
    If(
        _tot > 0,
        "  ·  " & Substitute(Text(_tot, "[$-en-US]#,##0"), ",", ".") & " m",
        ""
    )
)
```

**`lbl_DetLinhaL1Pnl` (controle dentro da galeria `gal_DetListaPnl`) · Text**

```
With(
    { _r: LookUp(colDetOPsPnl As _d5, _d5.ID = ThisItem.ID) },
    If((IsBlank(_r.OP) || _r.OP = 0), "OP não informada", "OP " & Text(_r.OP, "[$-en-US]0")) &
    "  ·  " & fx_Ou(_r.Mangueira)
)
```

**`lbl_DetLinhaL2Pnl` (controle dentro da galeria `gal_DetListaPnl`) · Color**

```
If(ThisItem.Ord = 0, fx_CorPainelTextoOK, fx_CorRotulo)
```

**`lbl_DetLinhaL2Pnl` (controle dentro da galeria `gal_DetListaPnl`) · Text**

```
ThisItem.Tag & "  ·  há " & fx_CronoLongo(
    First(
        Sort(
            Filter(colDetRotaPnl As _t5, _t5.ID = ThisItem.ID && !IsBlank(_t5.Mov)),
            Mov,
            SortOrder.Descending
        )
    ).Mov,
    ctxAgoraPnl
)
```

**`lbl_DetLinhaQtdPnl` (controle dentro da galeria `gal_DetListaPnl`) · Text**

```
With(
    {
        _t: First(
            Sort(
                Filter(colDetRotaPnl As _t6, _t6.ID = ThisItem.ID && (!IsBlank(_t6.Qtd) && _t6.Qtd > 0)),
                Ord,
                SortOrder.Descending
            )
        )
    },
    If(IsBlank(_t.Qtd), "—", Text(_t.Qtd, "[$-en-US]0") & " m")
)
```

**`lbl_DetHHRotPnl` · OnSelect**

```
Set(varDetToquePnl, Now())
```

**`lbl_DetHHPnl` · OnSelect**

```
Set(varDetToquePnl, Now())
```

**`lbl_DetRodapePnl` · Color**

```
fx_CorPainelTextoRotulo
```

**`lbl_DetRodapePnl` · OnSelect**

```
Set(varDetToquePnl, Now())
```

---

## Item 7 · Geometria (8 controles, e só eles)

Largura e altura não mudam; Y também não (as linhas 590 e 616 já eram as da grade). Nenhum outro controle existente mudou X/Y/Width/Height (conferido por diff geométrico contra a v0.10.3: só estes 8 mudam e só os 2 da legenda são novos).

| Controle | X antes | X depois | Y antes | Y depois | Width antes | Width depois | Height antes | Height depois |
|---|---|---|---|---|---|---|---|---|
| `lbl_BatH1Pnl` | 1066 | 1060 | 522 | 522 | 46 | 46 | 30 | 30 |
| `lbl_BatH2Pnl` | 1116 | 1096 | 522 | 522 | 46 | 46 | 30 | 30 |
| `lbl_BatH3Pnl` | 1166 | 1132 | 522 | 522 | 46 | 46 | 30 | 30 |
| `lbl_BatH4Pnl` | 1216 | 1168 | 522 | 522 | 46 | 46 | 30 | 30 |
| `lbl_BatH5Pnl` | 1266 | 1204 | 522 | 522 | 46 | 46 | 30 | 30 |
| `btn_B5BobPnl` | 166 | 134 | 590 | 590 | 48 | 48 | 22 | 22 |
| `btn_B6BobPnl` | 114 | 134 | 616 | 616 | 38 | 38 | 22 | 22 |
| `lbl_MaisBobPnl` | 114 | 134 | 616 | 616 | 38 | 38 | 22 | 22 |

Propriedade a colar (só o X):
- `btn_B5BobPnl.X` = `134`
- `btn_B6BobPnl.X` = `134`
- `lbl_BatH1Pnl.X` = `1060`
- `lbl_BatH2Pnl.X` = `1096`
- `lbl_BatH3Pnl.X` = `1132`
- `lbl_BatH4Pnl.X` = `1168`
- `lbl_BatH5Pnl.X` = `1204`
- `lbl_MaisBobPnl.X` = `134`

Bobinagem: grade 3 × 2 em colunas (B1/B2, B3/B4, B5/B6) dentro do card (X 16 a 197). O "+N" ocupa o lugar da 6ª bolinha. Cronograma: rótulo centrado na coluna da bolinha (centro = X da bolinha + 7).
Verificação: print.
