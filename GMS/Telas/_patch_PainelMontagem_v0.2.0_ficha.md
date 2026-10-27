# Patch Painel da Montagem v0.2.0 - ficha de consulta da celula (STAGING, nao gravado em GMS\Telas)

**Fonte de verdade: `scr_PainelMontagem_1.txt` desta pasta (QA sem FALHOU).** A tela e nova e ainda nao tem layout ajustado a mao: cole a tela INTEIRA pelo YAML. O que segue so serve para patch por bloco, se preferir a barra de formulas. Colar antes: nada novo em Formulas (usa fx_DetFechaSeg, fx_PeriodoIniEm/FimEm, fx_TurnoNum, fx_DataRefEm, fx_MetaMontagemMin, fx_ExcedeuMeta, fx_ParadaRealMontagem, fx_MotivoTempoExcedido, fx_CronoLongo, fx_RotuloCelulaTV, fx_CorOverlay: todas ja existem na v3.0.14).

Ordem de colar: (1) Screen.OnVisible, (2) btn_FichaAbrirMon (controle novo), (3) tmr_RelogioMon.OnTimerEnd, (4) gal_CardsMon: DisplayMode (apagar a linha) + OnSelect, (5) btn_ToqueCardMon (novo, DENTRO do template, por ultimo = por cima), (6) lbl_VersaoTelaMon.Text, (7) controles da ficha, NA ORDEM, no fim da lista de controles da tela (por cima de tudo, inclusive do seletor).

## 1. Screen OnVisible
```
=UpdateContext({ ctxModoMon: "VIVO", ctxCarregouMon: false, ctxFalhaMon: false, ctxTruncMon: false, ctxHoraMon: 1, ctxFichaAbertaMon: false, ctxFichaMon: "" });
Select(btn_RecarregarMon)
```

## 2. Controle novo btn_FichaAbrirMon (1x1 em X 1352, Y 2; botao oculto de logica)
```yaml
      - btn_FichaAbrirMon:
          Control: Classic/Button@2.2.0
          Properties:
            BorderColor: =Color.Transparent
            BorderThickness: =0
            Color: =fx_CorPainelTexto
            Fill: =Color.Transparent
            Font: =fx_FonteFamilia
            Height: =1
            HoverFill: =Color.Transparent
            OnSelect: |-
              =With(
                  // v0.2.0: monta as listas da ficha da celula tocada (ctxFichaMon). Nenhuma rede: so le colProdMon e colParMon,
                  // com os MESMOS filtros de periodo do btn_CalcMon (fx_PeriodoIniEm/FimEm, fx_TurnoNum, fx_DataRefEm).
                  {
                      _vivo: ctxModoMon = "VIVO",
                      _cel:  Upper(Trim(ctxFichaMon))
                  },
                  With(
                      {
                          _per: If(_vivo, Text(fx_TurnoEm(ctxAgoraMon), "[$-en-US]0"), ctxModoMon),
                          _dia: If(_vivo, fx_DataRefEm(ctxAgoraMon), ctxDiaMon)
                      },
                      With(
                          {
                              _ini: fx_PeriodoIniEm(_dia, _per, ctxHoraMon),
                              _fim: fx_PeriodoFimEm(_dia, _per, ctxHoraMon)
                          },
                          // OTs FECHADAS do periodo (turno/dia: carimbo Data + Turno; hora: FimEm na janela) com meta pela MetaHora da OT.
                          ClearCollect(
                              colFichaFechMon,
                              AddColumns(
                                  AddColumns(
                                      Filter(
                                          colProdMon As _b,
                                          Upper(Trim(_b.Celula)) = _cel && _b.Status = "Finalizado" &&
                                          If(
                                              _per = "HORA",
                                              !IsBlank(_b.FimEm) && _b.FimEm >= _ini && _b.FimEm < _fim,
                                              _b.Data = _dia && (_per = "DIA" || fx_TurnoNum(_b.Turno) = fx_TurnoNum(_per))
                                          )
                                      ),
                                      MetaMin,
                                      fx_MetaMontagemMin(QtdOT, MetaHora)
                                  ),
                                  Excede,
                                  fx_ExcedeuMeta(DuracaoRealMin, MetaMin),
                                  Pct,
                                  If(MetaMin > 0 && DuracaoRealMin > 0, Round(MetaMin / DuracaoRealMin * 100, 0), Blank())
                              )
                          );
                          // PARADAS do periodo (hora: RegistradoEm na janela; turno/dia: Data + Turno). Rot = motivo sem o codigo; Tag separa PARADA, TE e o resto.
                          ClearCollect(
                              colFichaParMon,
                              AddColumns(
                                  Filter(
                                      colParMon As _p,
                                      Upper(Trim(_p.Celula)) = _cel &&
                                      If(
                                          _per = "HORA",
                                          !IsBlank(_p.RegistradoEm) && _p.RegistradoEm >= _ini && _p.RegistradoEm < _fim,
                                          _p.Data = _dia && (_per = "DIA" || fx_TurnoNum(_p.Turno) = fx_TurnoNum(_per))
                                      )
                                  ),
                                  Rot,
                                  If(
                                      IsBlank(Trim(Motivo)), "Sem motivo",
                                      IsBlank(Find(" - ", Motivo)), Trim(Motivo),
                                      Trim(Mid(Motivo, Find(" - ", Motivo) + 3, 200))
                                  ),
                                  Tag,
                                  If(
                                      IsBlank(Trim(Motivo)), "—",
                                      fx_ParadaRealMontagem(Motivo), "PARADA",
                                      Motivo = fx_MotivoTempoExcedido, "TE",
                                      If(StartsWith(Upper(Trim(Motivo)), "RF"), "REFEIÇÃO", "OUTRO")
                                  )
                              )
                          );
                          // PRODUCAO POR TURNO da celula no dia produtivo (OTs Finalizadas carimbadas Data + Turno).
                          ClearCollect(
                              colFichaTurMon,
                              ForAll(
                                  Table({ T: 1 }, { T: 2 }, { T: 3 }) As _t,
                                  With(
                                      {
                                          _f: AddColumns(
                                              Filter(
                                                  colProdMon As _b2,
                                                  Upper(Trim(_b2.Celula)) = _cel && _b2.Status = "Finalizado" &&
                                                  _b2.Data = _dia && fx_TurnoNum(_b2.Turno) = _t.T
                                              ),
                                              MetaMin,
                                              fx_MetaMontagemMin(QtdOT, MetaHora)
                                          )
                                      },
                                      With(
                                          {
                                              _sM: Sum(Filter(_f, MetaMin > 0), MetaMin),
                                              _sR: Sum(Filter(_f, MetaMin > 0), DuracaoRealMin)
                                          },
                                          {
                                              T:     _t.T,
                                              NF:    CountRows(_f),
                                              Pecas: Sum(_f, QtdProduzida),
                                              Eff:   If(_sR > 0, _sM / _sR * 100, Blank())
                                          }
                                      )
                                  )
                              )
                          );
                          Reset(gal_FichaFechMon);
                          Reset(gal_FichaParMon);
                          UpdateContext({
                              ctxFichaDiaMon:   _dia,
                              ctxFichaSincMon:  ctxAgoraMon,
                              ctxFichaRefMon:   If(_per = "HORA" && _fim <= ctxAgoraMon, _fim, Blank()),
                              ctxFichaSubMon:   If(
                                                    _vivo, "AO VIVO · " & _per & "º turno · dia " & Text(_dia, "dd/mm"),
                                                    _per = "DIA", "DIA INTEIRO · " & Text(_dia, "dd/mm"),
                                                    _per = "HORA", "HORA " & Left(Index(fx_GradeHoraHora, Max(1, Min(CountRows(fx_GradeHoraHora), ctxHoraMon))).Rotulo, 2) & "h · dia " & Text(_dia, "dd/mm"),
                                                    _per & "º turno · dia " & Text(_dia, "dd/mm")
                                                ),
                              ctxFichaToqueMon: Now(),
                              ctxFichaAbertaMon: true
                          })
                      )
                  )
              )
            PressedFill: =Color.Transparent
            RadiusBottomLeft: =0
            RadiusBottomRight: =0
            RadiusTopLeft: =0
            RadiusTopRight: =0
            Text: =""
            Width: =1
            X: =1352
            Y: =2
```

## 3. tmr_RelogioMon (controle inteiro)
```yaml
      - tmr_RelogioMon:
          Control: Timer@2.1.0
          Properties:
            AutoStart: =true
            Duration: =30000
            Fill: =Color.Transparent
            Font: =fx_FonteFamilia
            Height: =1
            OnTimerEnd: |-
              =With(
                  { _n: Now() },
                  // Um Now() por tick. Sem Patch. Fora do AO VIVO, volta sozinho depois de fx_HistVoltaMin sem toque.
                  UpdateContext({ ctxAgoraMon: _n });
                  If(
                      ctxModoMon <> "VIVO" && DateDiff(ctxToqueMon, _n, TimeUnit.Minutes) >= fx_HistVoltaMin,
                      UpdateContext({ ctxFichaAbertaMon: false });
                      Select(btn_RecarregarMon),
                      Select(btn_CalcMon)
                  );
                  // v0.2.0: a ficha de consulta fecha sozinha (fx_DetFechaSeg s sem toque). Sem Patch.
                  If(
                      ctxFichaAbertaMon && DateDiff(ctxFichaToqueMon, _n, TimeUnit.Seconds) >= fx_DetFechaSeg,
                      UpdateContext({ ctxFichaAbertaMon: false })
                  )
              )
            Repeat: =true
            Text: =""
            Visible: =false
            Width: =1
            X: =1362
            Y: =2
```

## 4. gal_CardsMon (propriedades; Children inalterados exceto o item 5)
Apagar `DisplayMode: =DisplayMode.View` e acrescentar OnSelect. Controle e propriedades:
```yaml
      - gal_CardsMon:
          Control: Gallery@2.15.0
          Variant: Vertical
          Properties:
            BorderColor: =fx_CorPainelBorda
            Fill: =Color.Transparent
            Height: =576
            Items: =fx_CelulasMontagem
            OnSelect: |-
              =If(
                  ctxCarregouMon && !IsBlank(ctxAgoraMon),
                  UpdateContext({ ctxFichaMon: gal_CardsMon.Selected.Celula });
                  Select(btn_FichaAbrirMon)
              )
            ShowScrollbar: =false
            TemplateFill: =Color.Transparent
            TemplatePadding: =0
            TemplateSize: =192
            Width: =984
            WrapCount: =4
            X: =16
            Y: =180
```

## 5. Novo filho do template de gal_CardsMon (o ULTIMO filho, 238 x 186 em 0,0)
```yaml
            - btn_ToqueCardMon:
                Control: Classic/Button@2.2.0
                Properties:
                  BorderColor: =Color.Transparent
                  BorderThickness: =0
                  Color: =fx_CorPainelTexto
                  Fill: =Color.Transparent
                  FocusedBorderThickness: =0
                  Font: =fx_FonteFamilia
                  Height: =186
                  HoverFill: =Color.Transparent
                  OnSelect: =Select(Parent)
                  PressedFill: =fx_CorHoverSutil
                  RadiusBottomLeft: =fx_Raio
                  RadiusBottomRight: =fx_Raio
                  RadiusTopLeft: =fx_Raio
                  RadiusTopRight: =fx_Raio
                  Text: =""
                  Width: =238
                  X: =0
                  Y: =0
```

## 6. lbl_VersaoTelaMon.Text
`="Versão 0.2.0"`

## 7. Controles da ficha (colar nesta ordem, no fim da lista de Children da tela)
```yaml
      - btn_FichaScrimMon:
          Control: Classic/Button@2.2.0
          Properties:
            BorderColor: =Color.Transparent
            BorderThickness: =0
            Fill: =fx_CorOverlay
            FocusedBorderThickness: =0
            Font: =fx_FonteFamilia
            Height: =768
            HoverFill: =fx_CorOverlay
            OnSelect: |-
              =UpdateContext({ ctxFichaAbertaMon: false })
            PressedFill: =fx_CorOverlay
            RadiusBottomLeft: =0
            RadiusBottomRight: =0
            RadiusTopLeft: =0
            RadiusTopRight: =0
            Text: =""
            Visible: =ctxFichaAbertaMon
            Width: =1366
            X: =0
            Y: =0
      - btn_FichaCardMon:
          Control: Classic/Button@2.2.0
          Properties:
            BorderColor: =fx_CorPainelBorda
            BorderThickness: =1
            Fill: =fx_CorPainelSuperficie
            FocusedBorderThickness: =0
            Font: =fx_FonteFamilia
            Height: =640
            HoverFill: =fx_CorPainelSuperficie
            OnSelect: |-
              =UpdateContext({ ctxFichaToqueMon: Now() })
            PressedFill: =fx_CorPainelSuperficie
            RadiusBottomLeft: =fx_RaioG
            RadiusBottomRight: =fx_RaioG
            RadiusTopLeft: =fx_RaioG
            RadiusTopRight: =fx_RaioG
            Text: =""
            Visible: =ctxFichaAbertaMon
            Width: =1140
            X: =113
            Y: =64
      - btn_FichaBarraMon:
          Control: Classic/Button@2.2.0
          Properties:
            BorderColor: =Color.Transparent
            BorderThickness: =0
            DisplayMode: =DisplayMode.View
            Fill: =fx_CorEstadoTextoPainel(Coalesce(LookUp(colEstMon As _e, _e.Celula = ctxFichaMon).Estado, "CARREGANDO"))
            Font: =fx_FonteFamilia
            Height: =640
            HoverFill: =Self.Fill
            PressedFill: =Self.Fill
            RadiusBottomLeft: =fx_RaioG
            RadiusBottomRight: =0
            RadiusTopLeft: =fx_RaioG
            RadiusTopRight: =0
            Text: =""
            Visible: =ctxFichaAbertaMon
            Width: =6
            X: =113
            Y: =64
      - lbl_FichaTituloMon:
          Control: Label@2.5.1
          Properties:
            BorderColor: =fx_CorPainelBorda
            Color: =fx_CorPainelTexto
            Font: =fx_FonteFamilia
            FontWeight: =FontWeight.Bold
            Height: =40
            OnSelect: |-
              =UpdateContext({ ctxFichaToqueMon: Now() })
            PaddingLeft: =0
            Size: =fx_FontePainelRotulo
            Text: =fx_RotuloCelulaTV(ctxFichaMon)
            Visible: =ctxFichaAbertaMon
            Width: =560
            X: =137
            Y: =76
      - lbl_FichaSubMon:
          Control: Label@2.5.1
          Properties:
            BorderColor: =fx_CorPainelBorda
            Color: =fx_CorPainelTextoRotulo
            Font: =fx_FonteFamilia
            FontWeight: =FontWeight.Semibold
            Height: =30
            OnSelect: |-
              =UpdateContext({ ctxFichaToqueMon: Now() })
            PaddingLeft: =0
            Size: =fx_FontePainelApoio
            Text: =ctxFichaSubMon
            Visible: =ctxFichaAbertaMon
            Width: =760
            X: =137
            Y: =116
      - btn_FichaEstadoMon:
          Control: Classic/Button@2.2.0
          Properties:
            BorderColor: =Color.Transparent
            BorderThickness: =0
            Color: =fx_CorPainelFundo
            DisplayMode: =DisplayMode.View
            Fill: =fx_CorEstadoTextoPainel(Coalesce(LookUp(colEstMon As _e, _e.Celula = ctxFichaMon).Estado, "CARREGANDO"))
            Font: =fx_FonteFamilia
            FontWeight: =FontWeight.Bold
            Height: =40
            HoverFill: =Self.Fill
            PressedFill: =Self.Fill
            RadiusBottomLeft: =100
            RadiusBottomRight: =100
            RadiusTopLeft: =100
            RadiusTopRight: =100
            Size: =fx_FontePainelApoio
            Text: =Coalesce(LookUp(colEstMon As _e, _e.Celula = ctxFichaMon).Estado, "CARREGANDO")
            Visible: =ctxFichaAbertaMon
            Width: =220
            X: =945
            Y: =84
      - btn_FichaFecharMon:
          Control: Classic/Button@2.2.0
          Properties:
            BorderColor: =fx_CorPainelBorda
            BorderThickness: =1
            Color: =fx_CorPainelTexto
            Fill: =fx_CorPainelFundo
            FocusedBorderThickness: =0
            Font: =fx_FonteFamilia
            FontWeight: =FontWeight.Bold
            Height: =56
            HoverFill: =fx_CorPainelBorda
            OnSelect: |-
              =UpdateContext({ ctxFichaAbertaMon: false })
            PressedFill: =fx_CorPainelBorda
            RadiusBottomLeft: =fx_RaioS
            RadiusBottomRight: =fx_RaioS
            RadiusTopLeft: =fx_RaioS
            RadiusTopRight: =fx_RaioS
            Size: =fx_FontePainelRotulo
            Text: ="✕"
            Visible: =ctxFichaAbertaMon
            Width: =56
            X: =1181
            Y: =76
      - rct_FichaDivMon:
          Control: Rectangle@2.3.0
          Properties:
            BorderColor: =fx_CorPainelBorda
            Fill: =fx_CorPainelBorda
            Height: =1
            Visible: =ctxFichaAbertaMon
            Width: =1092
            X: =137
            Y: =150
      - lbl_FichaOTRotMon:
          Control: Label@2.5.1
          Properties:
            BorderColor: =fx_CorPainelBorda
            Color: =fx_CorPainelTextoRotulo
            Font: =fx_FonteFamilia
            FontWeight: =FontWeight.Bold
            Height: =30
            OnSelect: |-
              =UpdateContext({ ctxFichaToqueMon: Now() })
            PaddingLeft: =0
            Size: =fx_FontePainelApoio
            Text: |-
              =With(
                  { _s: LookUp(colEstMon As _e, _e.Celula = ctxFichaMon) },
                  "OT ABERTA" & If((ctxModoMon = "VIVO" || ctxModoMon = "HORA") && _s.Abertas > 1, "  ·  +" & Text(_s.Abertas - 1, "[$-en-US]0") & " outra(s)", "")
              )
            Visible: =ctxFichaAbertaMon
            Width: =520
            X: =137
            Y: =160
      - lbl_FichaOTMon:
          Control: Label@2.5.1
          Properties:
            BorderColor: =fx_CorPainelBorda
            Color: =fx_CorPainelTexto
            Font: =fx_FonteFamilia
            FontWeight: =FontWeight.Bold
            Height: =38
            OnSelect: |-
              =UpdateContext({ ctxFichaToqueMon: Now() })
            PaddingLeft: =0
            Size: =fx_FontePainelRotulo
            Text: |-
              =With(
                  { _s: LookUp(colEstMon As _e, _e.Celula = ctxFichaMon) },
                  If(
                      !(ctxModoMon = "VIVO" || ctxModoMon = "HORA"), "Só no AO VIVO ou por HORA",
                      _s.Abertas > 0, _s.PN & "  ·  OT " & Text(_s.OT, "[$-en-US]0"),
                      "Nenhuma OT aberta"
                  )
              )
            Visible: =ctxFichaAbertaMon
            Width: =520
            X: =137
            Y: =190
      - lbl_FichaOTLinhaMon:
          Control: Label@2.5.1
          Properties:
            BorderColor: =fx_CorPainelBorda
            Color: =fx_CorPainelTexto
            Font: =fx_FonteFamilia
            FontWeight: =FontWeight.Semibold
            Height: =30
            OnSelect: |-
              =UpdateContext({ ctxFichaToqueMon: Now() })
            PaddingLeft: =0
            Size: =fx_FontePainelApoio
            Text: |-
              =With(
                  { _s: LookUp(colEstMon As _e, _e.Celula = ctxFichaMon) },
                  If(
                      (ctxModoMon = "VIVO" || ctxModoMon = "HORA") && _s.Abertas > 0,
                      With(
                          { _q: LookUp(colProdMon As _o, Upper(Trim(_o.Celula)) = Upper(Trim(ctxFichaMon)) && _o.OT = _s.OT && _o.InicioEm = _s.Inicio).QtdOT },
                          If(IsBlank(_q), "", "Qtd " & Text(_q, "[$-en-US]0") & " pç  ·  ") &
                          "início " & Text(_s.Inicio, If(_s.Ontem, "dd/mm hh:mm", "hh:mm")) &
                          "  ·  " & fx_CronoLongo(_s.Inicio, Coalesce(ctxFichaRefMon, ctxAgoraMon))
                      ),
                      ""
                  )
              )
            Visible: =ctxFichaAbertaMon
            Width: =520
            X: =137
            Y: =230
      - lbl_FichaOTRealMon:
          Control: Label@2.5.1
          Properties:
            BorderColor: =fx_CorPainelBorda
            Color: =If(LookUp(colEstMon As _e, _e.Celula = ctxFichaMon).Excede, fx_CorPainelTextoAlerta, fx_CorPainelTexto)
            Font: =fx_FonteFamilia
            FontWeight: =FontWeight.Bold
            Height: =30
            OnSelect: |-
              =UpdateContext({ ctxFichaToqueMon: Now() })
            PaddingLeft: =0
            Size: =fx_FontePainelApoio
            Text: |-
              =With(
                  { _s: LookUp(colEstMon As _e, _e.Celula = ctxFichaMon) },
                  If(
                      (ctxModoMon = "VIVO" || ctxModoMon = "HORA") && _s.Abertas > 0,
                      "Real " & Text(_s.RealMin, "[$-en-US]0") & " min  ·  meta " &
                      If(_s.MetaMin > 0, Text(_s.MetaMin, "[$-en-US]0") & " min", "sem meta") &
                      If(_s.Excede, "  ·  +" & Text(_s.RealMin - _s.MetaMin, "[$-en-US]0") & " min acima", ""),
                      ""
                  )
              )
            Visible: =ctxFichaAbertaMon
            Width: =520
            X: =137
            Y: =260
      - lbl_FichaParRotMon:
          Control: Label@2.5.1
          Properties:
            BorderColor: =fx_CorPainelBorda
            Color: =fx_CorPainelTextoRotulo
            Font: =fx_FonteFamilia
            FontWeight: =FontWeight.Bold
            Height: =30
            OnSelect: |-
              =UpdateContext({ ctxFichaToqueMon: Now() })
            PaddingLeft: =0
            Size: =fx_FontePainelApoio
            Text: ="PARADA REAL"
            Visible: =ctxFichaAbertaMon
            Width: =262
            X: =681
            Y: =160
      - lbl_FichaParValMon:
          Control: Label@2.5.1
          Properties:
            BorderColor: =fx_CorPainelBorda
            Color: =If(Sum(Filter(colFichaParMon, Tag = "PARADA"), TempoParadoMin) > 0, fx_CorPainelTextoErro, fx_CorPainelTexto)
            Font: =fx_FonteFamilia
            FontWeight: =FontWeight.Bold
            Height: =56
            OnSelect: |-
              =UpdateContext({ ctxFichaToqueMon: Now() })
            PaddingLeft: =0
            Size: =fx_FontePainelNumero
            Text: =Text(Sum(Filter(colFichaParMon, Tag = "PARADA"), TempoParadoMin), "[$-en-US]0") & " min"
            Visible: =ctxFichaAbertaMon
            Width: =262
            X: =681
            Y: =190
      - lbl_FichaTeRotMon:
          Control: Label@2.5.1
          Properties:
            BorderColor: =fx_CorPainelBorda
            Color: =fx_CorPainelTextoRotulo
            Font: =fx_FonteFamilia
            FontWeight: =FontWeight.Bold
            Height: =30
            OnSelect: |-
              =UpdateContext({ ctxFichaToqueMon: Now() })
            PaddingLeft: =0
            Size: =fx_FontePainelApoio
            Text: ="TEMPO EXCEDIDO"
            Visible: =ctxFichaAbertaMon
            Width: =268
            X: =961
            Y: =160
      - lbl_FichaTeValMon:
          Control: Label@2.5.1
          Properties:
            BorderColor: =fx_CorPainelBorda
            Color: =If(Sum(Filter(colFichaParMon, Tag = "TE"), TempoParadoMin) > 0, fx_CorPainelTextoAlerta, fx_CorPainelTexto)
            Font: =fx_FonteFamilia
            FontWeight: =FontWeight.Bold
            Height: =56
            OnSelect: |-
              =UpdateContext({ ctxFichaToqueMon: Now() })
            PaddingLeft: =0
            Size: =fx_FontePainelNumero
            Text: =Text(Sum(Filter(colFichaParMon, Tag = "TE"), TempoParadoMin), "[$-en-US]0") & " min"
            Visible: =ctxFichaAbertaMon
            Width: =268
            X: =961
            Y: =190
      - lbl_FichaResumoMon:
          Control: Label@2.5.1
          Properties:
            BorderColor: =fx_CorPainelBorda
            Color: =fx_CorPainelTexto
            Font: =fx_FonteFamilia
            FontWeight: =FontWeight.Semibold
            Height: =30
            OnSelect: |-
              =UpdateContext({ ctxFichaToqueMon: Now() })
            PaddingLeft: =0
            Size: =fx_FontePainelApoio
            Text: |-
              =With(
                  {
                      _sM: Sum(Filter(colFichaFechMon, MetaMin > 0), MetaMin),
                      _sR: Sum(Filter(colFichaFechMon, MetaMin > 0), DuracaoRealMin)
                  },
                  Text(CountRows(colFichaFechMon), "[$-en-US]0") & " OT fechadas  ·  " &
                  Text(Sum(colFichaFechMon, QtdProduzida), "[$-en-US]0") & " pç  ·  eficiência " &
                  If(_sR > 0, Text(Round(_sM / _sR * 100, 0), "[$-en-US]0") & "%", "—")
              )
            Visible: =ctxFichaAbertaMon
            Width: =548
            X: =681
            Y: =252
      - lbl_FichaFechTitMon:
          Control: Label@2.5.1
          Properties:
            BorderColor: =fx_CorPainelBorda
            Color: =fx_CorPainelTextoRotulo
            Font: =fx_FonteFamilia
            FontWeight: =FontWeight.Bold
            Height: =30
            OnSelect: |-
              =UpdateContext({ ctxFichaToqueMon: Now() })
            PaddingLeft: =0
            Size: =fx_FontePainelApoio
            Text: ="OTs FECHADAS NO PERÍODO  ·  " & Text(CountRows(colFichaFechMon), "[$-en-US]0")
            Visible: =ctxFichaAbertaMon
            Width: =400
            X: =137
            Y: =296
      - lbl_FichaFechMaisMon:
          Control: Label@2.5.1
          Properties:
            Align: =Align.Right
            BorderColor: =fx_CorPainelBorda
            Color: =fx_CorPainelTextoRotulo
            Font: =fx_FonteFamilia
            FontWeight: =FontWeight.Bold
            Height: =30
            OnSelect: |-
              =UpdateContext({ ctxFichaToqueMon: Now() })
            PaddingLeft: =0
            Size: =fx_FontePainelApoio
            Text: =If(CountRows(colFichaFechMon) > 6, "+" & Text(CountRows(colFichaFechMon) - 6, "[$-en-US]0") & " mais", "")
            Visible: =ctxFichaAbertaMon
            Width: =190
            X: =547
            Y: =296
      - gal_FichaFechMon:
          Control: Gallery@2.15.0
          Variant: Vertical
          Properties:
            BorderColor: =fx_CorPainelBorda
            Fill: =Color.Transparent
            Height: =264
            Items: =FirstN(Sort(colFichaFechMon, FimEm, SortOrder.Descending), 6)
            OnSelect: |-
              =UpdateContext({ ctxFichaToqueMon: Now() })
            ShowScrollbar: =false
            TemplateFill: =Color.Transparent
            TemplatePadding: =0
            TemplateSize: =44
            Visible: =ctxFichaAbertaMon
            Width: =600
            X: =137
            Y: =328
          Children:
            - btn_FichaFechFundoMon:
                Control: Classic/Button@2.2.0
                Properties:
                  BorderColor: =If(ThisItem.Excede, fx_CorPainelTextoAlerta, fx_CorPainelBorda)
                  BorderThickness: =1
                  Fill: =fx_CorPainelFundo
                  FocusedBorderThickness: =0
                  Font: =fx_FonteFamilia
                  Height: =40
                  HoverFill: =fx_CorPainelFundo
                  OnSelect: =Select(Parent)
                  PressedFill: =fx_CorPainelFundo
                  RadiusBottomLeft: =fx_RaioS
                  RadiusBottomRight: =fx_RaioS
                  RadiusTopLeft: =fx_RaioS
                  RadiusTopRight: =fx_RaioS
                  Text: =""
                  Width: =588
                  X: =0
                  Y: =2
            - lbl_FichaFechOTMon:
                Control: Label@2.5.1
                Properties:
                  BorderColor: =fx_CorPainelBorda
                  Color: =fx_CorPainelTexto
                  Font: =fx_FonteFamilia
                  FontWeight: =FontWeight.Bold
                  Height: =40
                  OnSelect: =Select(Parent)
                  PaddingLeft: =0
                  Size: =fx_FontePainelApoio
                  Text: ="OT " & Text(ThisItem.OT, "[$-en-US]0") & " · " & ThisItem.PN
                  Width: =250
                  Wrap: =false
                  X: =10
                  Y: =2
            - lbl_FichaFechPcMon:
                Control: Label@2.5.1
                Properties:
                  Align: =Align.Right
                  BorderColor: =fx_CorPainelBorda
                  Color: =fx_CorPainelTexto
                  Font: =fx_FonteFamilia
                  FontWeight: =FontWeight.Semibold
                  Height: =40
                  OnSelect: =Select(Parent)
                  PaddingLeft: =0
                  Size: =fx_FontePainelApoio
                  Text: =If(IsBlank(ThisItem.QtdProduzida), "—", Text(ThisItem.QtdProduzida, "[$-en-US]0") & " pç")
                  Width: =86
                  Wrap: =false
                  X: =262
                  Y: =2
            - lbl_FichaFechRMMon:
                Control: Label@2.5.1
                Properties:
                  Align: =Align.Right
                  BorderColor: =fx_CorPainelBorda
                  Color: =fx_CorPainelTexto
                  Font: =fx_FonteFamilia
                  FontWeight: =FontWeight.Semibold
                  Height: =40
                  OnSelect: =Select(Parent)
                  PaddingLeft: =0
                  Size: =fx_FontePainelApoio
                  Text: =Text(ThisItem.DuracaoRealMin, "[$-en-US]0") & " / " & If(ThisItem.MetaMin > 0, Text(ThisItem.MetaMin, "[$-en-US]0"), "—") & " min"
                  Width: =140
                  Wrap: =false
                  X: =350
                  Y: =2
            - lbl_FichaFechPctMon:
                Control: Label@2.5.1
                Properties:
                  Align: =Align.Right
                  BorderColor: =fx_CorPainelBorda
                  Color: =If(ThisItem.Excede, fx_CorPainelTextoAlerta, IsBlank(ThisItem.Pct), fx_CorPainelTextoRotulo, fx_CorPainelTextoOK)
                  Font: =fx_FonteFamilia
                  FontWeight: =FontWeight.Bold
                  Height: =40
                  OnSelect: =Select(Parent)
                  PaddingLeft: =0
                  Size: =fx_FontePainelApoio
                  Text: =If(IsBlank(ThisItem.Pct), "sem meta", If(ThisItem.Excede, "▲ ", "") & Text(ThisItem.Pct, "[$-en-US]0") & "%")
                  Width: =94
                  Wrap: =false
                  X: =492
                  Y: =2
      - lbl_FichaFechVazioMon:
          Control: Label@2.5.1
          Properties:
            BorderColor: =fx_CorPainelBorda
            Color: =fx_CorPainelTextoRotulo
            Font: =fx_FonteFamilia
            FontWeight: =FontWeight.Semibold
            Height: =40
            OnSelect: |-
              =UpdateContext({ ctxFichaToqueMon: Now() })
            PaddingLeft: =0
            Size: =fx_FontePainelApoio
            Text: ="Nenhuma OT fechada no período"
            Visible: =ctxFichaAbertaMon && CountRows(colFichaFechMon) = 0
            Width: =560
            X: =147
            Y: =340
      - lbl_FichaParTitMon:
          Control: Label@2.5.1
          Properties:
            BorderColor: =fx_CorPainelBorda
            Color: =fx_CorPainelTextoRotulo
            Font: =fx_FonteFamilia
            FontWeight: =FontWeight.Bold
            Height: =30
            OnSelect: |-
              =UpdateContext({ ctxFichaToqueMon: Now() })
            PaddingLeft: =0
            Size: =fx_FontePainelApoio
            Text: ="PARADAS NO PERÍODO  ·  " & Text(CountRows(colFichaParMon), "[$-en-US]0")
            Visible: =ctxFichaAbertaMon
            Width: =300
            X: =761
            Y: =296
      - lbl_FichaParMaisMon:
          Control: Label@2.5.1
          Properties:
            Align: =Align.Right
            BorderColor: =fx_CorPainelBorda
            Color: =fx_CorPainelTextoRotulo
            Font: =fx_FonteFamilia
            FontWeight: =FontWeight.Bold
            Height: =30
            OnSelect: |-
              =UpdateContext({ ctxFichaToqueMon: Now() })
            PaddingLeft: =0
            Size: =fx_FontePainelApoio
            Text: =If(CountRows(colFichaParMon) > 6, "+" & Text(CountRows(colFichaParMon) - 6, "[$-en-US]0") & " mais", "")
            Visible: =ctxFichaAbertaMon
            Width: =150
            X: =1079
            Y: =296
      - gal_FichaParMon:
          Control: Gallery@2.15.0
          Variant: Vertical
          Properties:
            BorderColor: =fx_CorPainelBorda
            Fill: =Color.Transparent
            Height: =264
            Items: =FirstN(Sort(colFichaParMon, TempoParadoMin, SortOrder.Descending), 6)
            OnSelect: |-
              =UpdateContext({ ctxFichaToqueMon: Now() })
            ShowScrollbar: =false
            TemplateFill: =Color.Transparent
            TemplatePadding: =0
            TemplateSize: =44
            Visible: =ctxFichaAbertaMon
            Width: =468
            X: =761
            Y: =328
          Children:
            - btn_FichaParFundoMon:
                Control: Classic/Button@2.2.0
                Properties:
                  BorderColor: =If(ThisItem.Tag = "PARADA", fx_CorPainelTextoErro, ThisItem.Tag = "TE", fx_CorPainelTextoAlerta, fx_CorPainelBorda)
                  BorderThickness: =1
                  Fill: =fx_CorPainelFundo
                  FocusedBorderThickness: =0
                  Font: =fx_FonteFamilia
                  Height: =40
                  HoverFill: =fx_CorPainelFundo
                  OnSelect: =Select(Parent)
                  PressedFill: =fx_CorPainelFundo
                  RadiusBottomLeft: =fx_RaioS
                  RadiusBottomRight: =fx_RaioS
                  RadiusTopLeft: =fx_RaioS
                  RadiusTopRight: =fx_RaioS
                  Text: =""
                  Width: =456
                  X: =0
                  Y: =2
            - lbl_FichaParMotMon:
                Control: Label@2.5.1
                Properties:
                  BorderColor: =fx_CorPainelBorda
                  Color: =fx_CorPainelTexto
                  Font: =fx_FonteFamilia
                  FontWeight: =FontWeight.Bold
                  Height: =40
                  OnSelect: =Select(Parent)
                  PaddingLeft: =0
                  Size: =fx_FontePainelApoio
                  Text: =ThisItem.Rot
                  Width: =214
                  Wrap: =false
                  X: =10
                  Y: =2
            - lbl_FichaParTagMon:
                Control: Label@2.5.1
                Properties:
                  Align: =Align.Center
                  BorderColor: =fx_CorPainelBorda
                  Color: =If(ThisItem.Tag = "PARADA", fx_CorPainelTextoErro, ThisItem.Tag = "TE", fx_CorPainelTextoAlerta, fx_CorPainelTextoRotulo)
                  Font: =fx_FonteFamilia
                  FontWeight: =FontWeight.Bold
                  Height: =40
                  OnSelect: =Select(Parent)
                  PaddingLeft: =0
                  Size: =fx_FontePainelApoio
                  Text: =ThisItem.Tag
                  Width: =112
                  Wrap: =false
                  X: =226
                  Y: =2
            - lbl_FichaParMinMon:
                Control: Label@2.5.1
                Properties:
                  Align: =Align.Right
                  BorderColor: =fx_CorPainelBorda
                  Color: =fx_CorPainelTexto
                  Font: =fx_FonteFamilia
                  FontWeight: =FontWeight.Semibold
                  Height: =40
                  OnSelect: =Select(Parent)
                  PaddingLeft: =0
                  Size: =fx_FontePainelApoio
                  Text: =If(IsBlank(ThisItem.TempoParadoMin), "—", Text(ThisItem.TempoParadoMin, "[$-en-US]0") & " min")
                  Width: =108
                  Wrap: =false
                  X: =340
                  Y: =2
      - lbl_FichaParVazioMon:
          Control: Label@2.5.1
          Properties:
            BorderColor: =fx_CorPainelBorda
            Color: =fx_CorPainelTextoRotulo
            Font: =fx_FonteFamilia
            FontWeight: =FontWeight.Semibold
            Height: =40
            OnSelect: |-
              =UpdateContext({ ctxFichaToqueMon: Now() })
            PaddingLeft: =0
            Size: =fx_FontePainelApoio
            Text: ="Nenhuma parada no período"
            Visible: =ctxFichaAbertaMon && CountRows(colFichaParMon) = 0
            Width: =440
            X: =771
            Y: =340
      - lbl_FichaTurTitMon:
          Control: Label@2.5.1
          Properties:
            BorderColor: =fx_CorPainelBorda
            Color: =fx_CorPainelTextoRotulo
            Font: =fx_FonteFamilia
            FontWeight: =FontWeight.Bold
            Height: =28
            OnSelect: |-
              =UpdateContext({ ctxFichaToqueMon: Now() })
            PaddingLeft: =0
            Size: =fx_FontePainelApoio
            Text: ="PRODUÇÃO POR TURNO NO DIA " & Text(ctxFichaDiaMon, "dd/mm")
            Visible: =ctxFichaAbertaMon
            Width: =700
            X: =137
            Y: =600
      - gal_FichaTurMon:
          Control: Gallery@2.15.0
          Variant: Vertical
          Properties:
            BorderColor: =fx_CorPainelBorda
            Fill: =Color.Transparent
            Height: =70
            Items: =Sort(colFichaTurMon, T, SortOrder.Ascending)
            OnSelect: |-
              =UpdateContext({ ctxFichaToqueMon: Now() })
            ShowScrollbar: =false
            TemplateFill: =Color.Transparent
            TemplatePadding: =0
            TemplateSize: =70
            Visible: =ctxFichaAbertaMon
            Width: =1092
            WrapCount: =3
            X: =137
            Y: =630
          Children:
            - btn_FichaTurFundoMon:
                Control: Classic/Button@2.2.0
                Properties:
                  BorderColor: =fx_CorPainelBorda
                  BorderThickness: =1
                  Fill: =fx_CorPainelFundo
                  FocusedBorderThickness: =0
                  Font: =fx_FonteFamilia
                  Height: =66
                  HoverFill: =fx_CorPainelFundo
                  OnSelect: =Select(Parent)
                  PressedFill: =fx_CorPainelFundo
                  RadiusBottomLeft: =fx_RaioS
                  RadiusBottomRight: =fx_RaioS
                  RadiusTopLeft: =fx_RaioS
                  RadiusTopRight: =fx_RaioS
                  Text: =""
                  Width: =352
                  X: =0
                  Y: =2
            - lbl_FichaTurRotMon:
                Control: Label@2.5.1
                Properties:
                  BorderColor: =fx_CorPainelBorda
                  Color: =fx_CorPainelTextoRotulo
                  Font: =fx_FonteFamilia
                  FontWeight: =FontWeight.Bold
                  Height: =28
                  OnSelect: =Select(Parent)
                  PaddingLeft: =0
                  Size: =fx_FontePainelApoio
                  Text: =Text(ThisItem.T, "[$-en-US]0") & "º TURNO"
                  Width: =330
                  Wrap: =false
                  X: =12
                  Y: =6
            - lbl_FichaTurValMon:
                Control: Label@2.5.1
                Properties:
                  BorderColor: =fx_CorPainelBorda
                  Color: =If(ThisItem.NF = 0, fx_CorPainelTextoRotulo, IsBlank(ThisItem.Eff), fx_CorPainelTexto, ThisItem.Eff >= 100, fx_CorPainelTextoOK, fx_CorPainelTextoAlerta)
                  Font: =fx_FonteFamilia
                  FontWeight: =FontWeight.Bold
                  Height: =34
                  OnSelect: =Select(Parent)
                  PaddingLeft: =0
                  Size: =fx_FontePainelRotulo
                  Text: =If(ThisItem.NF = 0, "sem OT fechada", Text(ThisItem.Pecas, "[$-en-US]0") & " pç  ·  efic. " & If(IsBlank(ThisItem.Eff), "—", Text(Round(ThisItem.Eff, 0), "[$-en-US]0") & "%"))
                  Width: =330
                  Wrap: =false
                  X: =12
                  Y: =32
      - lbl_FichaDicaMon:
          Control: Label@2.5.1
          Properties:
            Align: =Align.Center
            BorderColor: =fx_CorPainelBorda
            Color: =fx_CorPainelTextoRotulo
            Font: =fx_FonteFamilia
            FontWeight: =FontWeight.Semibold
            Height: =30
            PaddingLeft: =0
            Size: =fx_FontePainelApoio
            Text: |-
              ="listas: retrato das " & Text(ctxFichaSincMon, "hh:mm") & "  ·  fecha em " & Text(fx_DetFechaSeg, "[$-en-US]0") & " s sem toque"
            Visible: =ctxFichaAbertaMon
            Width: =1092
            X: =137
            Y: =712
```
