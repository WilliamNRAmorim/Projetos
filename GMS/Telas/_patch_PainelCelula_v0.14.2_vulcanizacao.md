# Patch · scr_PainelCelula_1 v0.14.1 → v0.14.2 · Vulcanização produz pelo Início (27/10/2026)

O Fim da Vulcanização só é gravado depois da cura; o Início é gravado quando o carretel entra na autoclave. Para 'o que passou por ela hoje', a Vulcanização soma os eventos Início (revisor aprovou); as outras etapas continuam com Fim e Parcial. Cole a propriedade inteira, sem o `=` inicial, e o texto da versão.

**`btn_AgregaPnl` · OnSelect**

```
With(
    { _src: If(ctxModoPnl = "VIVO", colEvDiaPnl, colEvHistPnl) },
    // UMA agregacao para os dois modos: colEvDiaPnl (AO VIVO) ou colEvHistPnl (dia escolhido), mesmo esquema de colunas.
    // Soma de `metros` dos eventos Fim e Parcial; na VULCANIZACAO, dos eventos Inicio (o que entrou na autoclave: o Fim so sai depois da cura). Sem evento no turno = Blank() (a tela mostra "—", nunca 0).
    ClearCollect(
        colProdEtapaTurnoPnl,
        ForAll(
            fx_EtapasLinha As _pe,
            With(
                {
                    _ev: Filter(
                        _src As _pv,
                        _pv.EtapaTxt = _pe.Etapa && If(_pe.Etapa = "Vulcanização", _pv.TipoTxt = "Início", _pv.TipoTxt = "Fim" || _pv.TipoTxt = "Parcial")
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

**`lbl_VersaoTelaPnl` · Text**

```
"Versão 0.14.2"
```
