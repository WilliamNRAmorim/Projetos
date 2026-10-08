# Patch: OP vira dropdown do plano (scr_tubo_1 e scr_ExtrusoraMandril_1) — 08/10/2026

Decisão do William: nada de digitar OP. O operador escolhe numa lista com as OPs do plano que **não estão encerradas** (TECO no SAP) e **ainda não estão em nenhuma ficha**. OP obrigatória.
Fonte: lista SharePoint `Plano_OPs` (carga automática pelo fluxo `GMS_PlanoOPs_Sync`). Campos: `Title` (OP, texto 8 dígitos), `PN`, `Trancadeira`, `QtdPlanejada`, `Tipo` (Tubo | Extrusora), `StatusSAP`, `Encerrada` (Sim/Não), `Origem`.

NÃO colar antes de: (1) o fluxo `GMS_PlanoOPs_Sync` ter rodado com sucesso uma vez (lista conferida) e (2) William aprovar. Os `.txt` de `Telas/` NÃO foram alterados ainda.

## 0. Antes de colar (Studio)
Dados > Adicionar dados > `Plano_OPs` (site Operations Guaratingueta). Sem isso as fórmulas abaixo dão "Name isn't valid".

## 1. scr_tubo_1

### 1.1 Carregar o plano — `ico_RefreshTubo_1.OnSelect`
Dentro do primeiro `IfError(Concurrent(...` acrescente `Refresh(Plano_OPs)` na lista do Concurrent:
```
Refresh(ficha_producao),
Refresh(lista_carreteis),
Refresh('Hora-Hora'),
Refresh(Plano_OPs)
```
E logo depois do `Concurrent( ClearCollect(colCarreteisTubo ...` (antes do `ClearCollect(colKanbanTrancTubo`), cole:
```
IfError(
    ClearCollect(
        colPlanoTubo,
        AddColumns(
            Filter(Plano_OPs, Tipo = "Tubo", Encerrada = false),
            "OPnum", Value(Title),
            "Rotulo", Title & "  ·  " & Coalesce(PN, "") & If(!IsBlank(Trancadeira), "  ·  " & Trancadeira, "") & If(QtdPlanejada > 0, "  ·  " & Text(QtdPlanejada, "0") & " m", "")
        )
    ),
    Notify("Não consegui ler o plano de OPs. Toque em atualizar.", NotificationType.Error, 8000)
);
With(
    { _min: Coalesce(Min(colPlanoTubo, OPnum), 0) },
    ClearCollect(colOPsUsadasTubo, ShowColumns(Filter(ficha_producao, OP >= _min), "OP"))
);
```
(`OP >= _min` é delegável; evita o limite de linhas. `Encerrada = false` também.)

### 1.2 Trocar o campo — apagar `inp_OpTubo_1` e colar no mesmo lugar (X531 Y544):
```
      - cmb_OpTubo_1:
          Control: Classic/ComboBox@2.4.0
          Properties:
            AccessibleLabel: ="Ordem de produção do plano"
            BorderColor: |-
              =If(
                  fx_EstadoContinuo(gal_FilaTubo_1.Selected.status_processo) = "PRODUZINDO" && IsBlank(Self.Selected.OPnum),
                  fx_CorErro,
                  fx_CorBorda
              )
            ChevronBackground: =fx_CorInfo
            ChevronFill: =fx_CorSuperficie
            ChevronHoverBackground: =ColorFade(fx_CorInfo, -20%)
            ChevronHoverFill: =fx_CorSuperficie
            DefaultSelectedItems: =Filter(colPlanoTubo, OPnum = gal_FilaTubo_1.Selected.OP)
            DisplayFields: =["Rotulo"]
            DisplayMode: |-
              =If(
                  fx_EstadoContinuo(gal_FilaTubo_1.Selected.status_processo) = "PRODUZINDO" && !varProcessando,
                  DisplayMode.Edit,
                  DisplayMode.Disabled
              )
            Font: =fx_FonteFamilia
            Height: =fx_AlturaCampo
            HoverFill: =fx_CorInfoSuave
            InputTextPlaceholder: ="Escolha a OP do plano"
            IsSearchable: =true
            Items: |-
              =Filter(
                  colPlanoTubo,
                  !(OPnum in colOPsUsadasTubo.OP) || OPnum = gal_FilaTubo_1.Selected.OP
              )
            PressedColor: =fx_CorSuperficie
            PressedFill: =fx_CorInfo
            SearchFields: =["Title", "PN"]
            SelectMultiple: =false
            SelectionColor: =fx_CorSuperficie
            SelectionFill: =fx_CorInfo
            Width: =148
            X: =531
            Y: =544
```
Largura 148 só mostra "30424231 · GH781-…"; se cortar, aumentar `Width` (cuidado com vizinhos) ou deixar `DisplayFields: =["Title"]` e conferir PN/metros no card.

### 1.3 Trocar as referências a `inp_OpTubo_1` (use Localizar do Studio)
| Onde | Antes | Depois |
|---|---|---|
| gal_FilaTubo_1.OnSelect (l.139) e l.2279, l.2797 | `Reset(inp_OpTubo_1)` | `Reset(cmb_OpTubo_1)` |
| l.2346 texto do resumo | `Trim(inp_OpTubo_1.Text)` | `Text(cmb_OpTubo_1.Selected.OPnum, "00000000")` |
| DisplayMode dos 2 botões de enviar (l.1630-1631 e l.2567) | `Len(Trim(inp_OpTubo_1.Text)) = 8 && Coalesce(Value(inp_OpTubo_1.Text), 0) > 0` (e só o `Len(...) = 8` na l.2567) | `!IsBlank(cmb_OpTubo_1.Selected.OPnum)` |
| OnSelect do enviar (l.2586) | `_op: Value(Trim(inp_OpTubo_1.Text)),` | `_op: Coalesce(cmb_OpTubo_1.Selected.OPnum, 0),` |
| l.2595 teste | `Len(Trim(inp_OpTubo_1.Text)) <> 8 \|\| _op <= 0,` e mensagem | `_op <= 0,` com `Notify("Escolha a OP na lista do plano.", NotificationType.Warning, 8000);` |

Trava extra (cole como novo ramo logo depois do ramo `_op <= 0`, antes de `IsBlank(_operador)`):
```
IsBlank(LookUp(Plano_OPs, Title = Text(_op, "00000000") && Encerrada = false).ID),
Notify("Esta OP saiu do plano ou já foi encerrada. Toque em atualizar e escolha de novo.", NotificationType.Error, 10000);
Set(varProcessando, false),
```
O teste `_dup` (OP já em outra ficha) continua valendo.

## 2. scr_ExtrusoraMandril_1
O registro fica em `ControleExtrusora_estrutura` (campo `OP`, número). "Em uso" = OP já em outro registro dessa lista.

### 2.1 `btn_CarregarExt.OnSelect`
No `Concurrent(` do `Refresh`, acrescente `Refresh(Plano_OPs)`. E no segundo `Concurrent(` (onde ficam os `ClearCollect(colCarrExt`, `colAbertosExt`, ...) acrescente estes dois itens:
```
ClearCollect(
    colPlanoExt,
    AddColumns(
        Filter(Plano_OPs, Tipo = "Extrusora", Encerrada = false),
        "OPnum", Value(Title),
        "Rotulo", Title & "  ·  " & Coalesce(PN, "") & If(!IsBlank(Trancadeira), "  ·  " & Trancadeira, "")
    )
),
ClearCollect(
    colOPsUsadasExt,
    ShowColumns(Filter(ControleExtrusora_estrutura, OP >= 28000000), "OP", "ID")
)
```
(piso 28000000 = OP do mandril em 2026 começa em 28,4 milhões; ajuste se aparecer OP menor.)

### 2.2 Trocar o campo `inp_OpExt` (X531 Y354) por:
```
      - cmb_OpExt:
          Control: Classic/ComboBox@2.4.0
          Properties:
            AccessibleLabel: ="OP da extrusão, do plano"
            BorderColor: =If(ctxProduzindoExt && IsBlank(Self.Selected.OPnum), fx_CorErro, fx_CorBorda)
            ChevronBackground: =fx_CorInfo
            ChevronFill: =fx_CorSuperficie
            ChevronHoverBackground: =ColorFade(fx_CorInfo, -20%)
            ChevronHoverFill: =fx_CorSuperficie
            DefaultSelectedItems: =Filter(colPlanoExt, OPnum = ctxRegExt.OP)
            DisplayFields: =["Rotulo"]
            DisplayMode: =If(ctxProduzindoExt && !ctxProcExt, DisplayMode.Edit, DisplayMode.Disabled)
            Font: =fx_FonteFamilia
            Height: =fx_AlturaCampo
            HoverFill: =fx_CorInfoSuave
            InputTextPlaceholder: ="Escolha a OP do plano"
            IsSearchable: =true
            Items: =Filter(colPlanoExt, !(OPnum in colOPsUsadasExt.OP) || OPnum = ctxRegExt.OP)
            PressedColor: =fx_CorSuperficie
            PressedFill: =fx_CorInfo
            SearchFields: =["Title", "PN"]
            SelectMultiple: =false
            SelectionColor: =fx_CorSuperficie
            SelectionFill: =fx_CorInfo
            Width: =148
            X: =531
            Y: =354
```

### 2.3 Referências a `inp_OpExt`
| Onde | Antes | Depois |
|---|---|---|
| l.1309 e l.1429 | `_op: Trim(inp_OpExt.Text),` | `_op: Text(cmb_OpExt.Selected.OPnum, "[$-en-US]0"),` |
| fechar a extrusão (l.1326) | `!IsBlank(_op) && !IsMatch(_op, "\d+"),` + mensagem | `IsBlank(cmb_OpExt.Selected.OPnum),` com `Notify("Escolha a OP do plano para fechar a extrusão.", NotificationType.Warning, 6000);` (OP obrigatória ao fechar) |
| salvar sem fechar (l.1440) | `!IsBlank(_op) && !IsMatch(_op, "\d+"),` | remover o ramo (salvar rascunho pode ficar sem OP; é decisão do William se também exige) |
| Patch `OP: If(IsBlank(_op), Blank(), Value(_op))` (l.1333 e 1448) | igual | sem mudança (continua válido) |
| l.1390 e l.3096 | `Reset(inp_OpExt)` | `Reset(cmb_OpExt)` |
| l.2574 (refugo) | `Coalesce(Trim(inp_OpExt.Text), ctxRegExt.Title)` | `Coalesce(Text(cmb_OpExt.Selected.OPnum, "[$-en-US]0"), ctxRegExt.Title)` |

## 3. Exceção (OP fora do plano)
Não entra nesta rodada. Proposta: botão "Pedir exceção" cria linha em `Excecoes_OP` (OP, motivo, tela, quem pediu) e só libera a OP quando william.amorim@danfoss.com ou carlos.brizon@danfoss.com marcar `Aprovado`. Até lá, OP fora do plano não passa (era o objetivo).

## 4. Teste
1. Abrir scr_tubo_1: o dropdown mostra só OP Tubo não encerrada e sem ficha; digitar parte do PN filtra.
2. Escolher uma OP, enviar: grava `OP` na ficha; reabrir o dropdown: a OP some da lista (em uso).
3. OP encerrada (TECO) e OP já usada não aparecem. OP inventada (12345678) não é mais possível.
4. scr_ExtrusoraMandril_1: igual, só com OP `Tipo = Extrusora`; fechar sem escolher OP mostra o aviso.
5. Atualizar plano: toque no ícone de atualizar depois que o PCP salvar o Excel (o fluxo leva 1-3 min).
