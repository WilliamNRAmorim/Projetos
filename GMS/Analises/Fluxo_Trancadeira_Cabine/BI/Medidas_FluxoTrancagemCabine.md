# Medidas: Fluxo Trançagem → Cabine (página-piloto do BI) — PENDENTE DE APLICAR

Fonte do desenho e das fórmulas: `../painel_template.html` (KPIs) e `../ilustracao_headcount.html` (cartões aprovados).
Lógica de dados: `../extrair_dados.py`. As medidas SVG estão em `Medidas_SVG_FluxoTrancagemCabine.md`; layout e
conferência em `LEIAME_Pagina.md`.

Pasta de exibição de tudo: **`Fluxo Tranç→Cabine`** (subpastas `Leitura`, `Séries`, `Auxiliares` e `Conferência`).
A única exceção é `Metros Produzidos` (K01 do catálogo), que fica em `Produção`.

---

## 0. O que falta no modelo hoje (ler antes de colar)

O catálogo (`GMS_Mestre_BI.md`, Parte C) escreve as medidas sobre a `fEtapaOP` (1 linha = OP × etapa, com
`Quantidade (m)`, `Fim da Etapa`, `Data de Referência` e `Operador`). No modelo real essa tabela **ainda não existe**:
a MEL-116 ("construir fEtapaOP por unpivot") está aberta, e a emenda v1.1 aponta a `Etapas` e a `fFluxoEtapas` como as
tabelas por etapa. Não foi possível ler as colunas da `Etapas` daqui: o repositório não tem o TMDL do modelo e o `.pbix`
guarda o modelo compactado. Nenhum relatório versionado usa coluna de operador da `Etapas`.

**O que falta, portanto:** a coluna **`Operador`** por etapa, junto com `Quantidade (m)`, `Fim da Etapa` e
`Data de Referência` no grão ficha × etapa. Sem ela não existe "pessoas por etapa e dia". O Bloco 1 abaixo cria isso
completo, direto da `ficha_producao` que já está no modelo (mesmas colunas que o `extrair_dados.py` lê):

| Etapa (dEtapa) | Fim | Quantidade | Operador |
|---|---|---|---|
| Trançagem | `data_hora_final_trancadeira` | `quantidade_trancagem` | `operador_trancagem` |
| Cobertura | `data_hora_final_cobertura` | `quantidade_cobertura` | `operador_cobertura` |
| Bandagem | `data_hora_final_bandagem` | `quantidade_bandagem` | `operador_bandagem` |
| Vulcanização | `data_hora_final_vulcanizacao` | `quantidade_vulcanizacao` | `operador_vulcanizacao` |
| Debandagem | `data_hora_final_debandagem` | `quantidade_debandagem` | `operador_debandagem` |
| Extração/Teste (Cabine) | `data_hora_final_extracao` | `quantidade_extracao` | `operador_extracao` |

Mandril e Tubo entram também, para a tabela servir a MEL-116 inteira. A página filtra o trecho pela coluna
`dEtapa[Trecho Tranç-Cabine]`.

**Se a `Etapas` já tiver** operador, quantidade, fim e data de referência por etapa, não crie a `fEtapaOP`: troque
`fEtapaOP[...]` pelos nomes da `Etapas` nas medidas (são só 4 colunas: `Quantidade (m)`, `Operador`,
`Lead Time Tranç→Cabine (h)` e as datas dos relacionamentos) e me diga os nomes, que eu devolvo o bloco ajustado.

**Antes de colar:**
- Se o TMDL recusar com "duplicate"/"already exists" em `dEtapa`, `fEtapaOP` ou `Metros Produzidos`, o nome já existe
  no modelo. Não sobrescreva: me avise.
- A partição da `fEtapaOP` lê a consulta `ficha_producao` pelo nome. Se o serviço recusar a referência, copie os passos
  `Origem` e `Lista` da partição da `ficha_producao` no lugar de `Origem = ficha_producao`.
- Turno não entra nesta página (pedido do briefing). A `fEtapaOP` sai sem a coluna `Turno`, que a §A.3 exige para
  fato do modelo. Isso fica como pendência para o `revisor` (ver LEIAME).

---

## Bloco 1 — Tabelas `dEtapa` e `fEtapaOP` (TMDL view → colar → Aplicar → Atualizar)

```
createOrReplace

	table dEtapa

		/// 1 linha = 1 etapa do roteiro da célula (8). Ordem_Fluxo = posição no fluxo físico.
		column Etapa
			dataType: string
			summarizeBy: none
			sortByColumn: Ordem_Fluxo
			sourceColumn: Etapa

		/// Rótulo da página de fluxo (Extração/Teste aparece como "Cabine (teste)").
		column 'Etapa no Fluxo'
			dataType: string
			summarizeBy: none
			sortByColumn: Ordem_Fluxo
			sourceColumn: Etapa no Fluxo

		column Ordem_Fluxo
			dataType: int64
			isHidden
			formatString: 0
			summarizeBy: none
			sourceColumn: Ordem_Fluxo

		/// Verdadeiro para as 6 etapas da trançagem até a cabine.
		column 'Trecho Tranç-Cabine'
			dataType: boolean
			summarizeBy: none
			sourceColumn: Trecho Tranç-Cabine

		partition dEtapa = m
			mode: import
			source =
				let
				    Etapas = #table(
				        type table [Etapa = text, #"Etapa no Fluxo" = text, Ordem_Fluxo = Int64.Type, #"Trecho Tranç-Cabine" = logical],
				        {
				            {"Mandril",        "Mandril",        1, false},
				            {"Tubo",           "Tubo",           2, false},
				            {"Trançagem",      "Trançagem",      3, true},
				            {"Cobertura",      "Cobertura",      4, true},
				            {"Bandagem",       "Bandagem",       5, true},
				            {"Vulcanização",   "Vulcanização",   6, true},
				            {"Debandagem",     "Debandagem",     7, true},
				            {"Extração/Teste", "Cabine (teste)", 8, true}
				        })
				in
				    Etapas

	table fEtapaOP

		/// 1 linha = 1 ficha × 1 etapa concluída (Fim da Etapa preenchido). Fonte: ficha_producao (unpivot das 8 etapas). MEL-116.
		column 'ID Ficha'
			dataType: int64
			isHidden
			formatString: 0
			summarizeBy: none
			sourceColumn: ID Ficha

		column OP
			dataType: string
			summarizeBy: none
			sourceColumn: OP

		column Etapa
			dataType: string
			isHidden
			summarizeBy: none
			sourceColumn: Etapa

		column 'Fim da Etapa'
			dataType: dateTime
			formatString: dd/mm/yyyy hh:nn
			summarizeBy: none
			sourceColumn: Fim da Etapa

		/// Dia de produção: antes das 05:20 o fim pertence ao dia anterior (fn_DataRef, §B.3.3).
		column 'Data de Referência'
			dataType: dateTime
			isHidden
			formatString: dd/mm/yyyy
			summarizeBy: none
			sourceColumn: Data de Referência

		/// Data civil do fim. Só para conferir contra o painel HTML (relacionamento inativo).
		column 'Data do Fim'
			dataType: dateTime
			isHidden
			formatString: dd/mm/yyyy
			summarizeBy: none
			sourceColumn: Data do Fim

		column 'Quantidade (m)'
			dataType: double
			isHidden
			formatString: #,0
			summarizeBy: none
			sourceColumn: Quantidade (m)

		/// Operador que apontou a etapa. Usado só em contagem distinta; nunca exibir em visual.
		column Operador
			dataType: string
			isHidden
			summarizeBy: none
			sourceColumn: Operador

		/// Só na linha da Extração/Teste: horas do fim da Trançagem ao fim da Extração da mesma ficha.
		column 'Lead Time Tranç→Cabine (h)'
			dataType: double
			isHidden
			formatString: #,0.0
			summarizeBy: none
			sourceColumn: Lead Time Tranç→Cabine (h)

		partition fEtapaOP = m
			mode: import
			source =
				let
				    // Grão de entrada: ficha_producao, 1 linha por ficha. Saída: 1 linha por ficha × etapa concluída.
				    // Não há junção; conferência de contagem: linhas da saída = soma, por etapa, das fichas com data_hora_final preenchida.
				    Origem = ficha_producao,
				    Mapa = {
				        {"Mandril",        "data_hora_final_mandril",      "quantidade_mandril",      "operador_mandril"},
				        {"Tubo",           "data_hora_final_tubo",         "quantidade_tubo",         "operador_tubo"},
				        {"Trançagem",      "data_hora_final_trancadeira",  "quantidade_trancagem",    "operador_trancagem"},
				        {"Cobertura",      "data_hora_final_cobertura",    "quantidade_cobertura",    "operador_cobertura"},
				        {"Bandagem",       "data_hora_final_bandagem",     "quantidade_bandagem",     "operador_bandagem"},
				        {"Vulcanização",   "data_hora_final_vulcanizacao", "quantidade_vulcanizacao", "operador_vulcanizacao"},
				        {"Debandagem",     "data_hora_final_debandagem",   "quantidade_debandagem",   "operador_debandagem"},
				        {"Extração/Teste", "data_hora_final_extracao",     "quantidade_extracao",     "operador_extracao"}
				    },
				    Colunas = Table.SelectColumns(Origem, {"ID", "OP"} & List.Combine(List.Transform(Mapa, each List.Skip(_, 1))), MissingField.UseNull),
				    // Data-hora: aceita datetime, datetimezone (vira UTC-3), date ou texto pt-BR.
				    ParaDataHora = (v as any) as nullable datetime =>
				        if v = null then null
				        else if Value.Is(v, type datetimezone) then DateTimeZone.RemoveZone(DateTimeZone.SwitchZone(v, -3))
				        else if Value.Is(v, type datetime) then v
				        else if Value.Is(v, type date) then DateTime.From(v)
				        else try DateTime.FromText(Text.From(v), "pt-BR") otherwise null,
				    // Número: aceita número ou texto com vírgula decimal (armadilha do NumeroBR, §B.3.4).
				    ParaNumero = (v as any) as nullable number =>
				        if v = null then null
				        else if Value.Is(v, type number) then v
				        else
				            let
				                t = Text.Trim(Text.From(v)),
				                u = if Text.Contains(t, ",") then Text.Replace(Text.Remove(t, {"."}), ",", ".") else t
				            in
				                try Number.FromText(u, "en-US") otherwise null,
				    ParaTexto = (v as any) as nullable text =>
				        if v = null then null
				        else let t = Text.Trim(Text.From(v)) in if t = "" then null else t,
				    // Lead time por ficha no formato largo (BI3: camada mais barata). Vai só na linha da Extração/Teste.
				    ComLead = Table.AddColumn(Colunas, "_LT", each
				        let
				            a = ParaDataHora([data_hora_final_trancadeira]),
				            b = ParaDataHora([data_hora_final_extracao])
				        in
				            if a = null or b = null then null else Duration.TotalHours(b - a),
				        type nullable number),
				    PorEtapa = List.Transform(Mapa, (e) =>
				        let
				            t = Table.SelectColumns(ComLead, {"ID", "OP", e{1}, e{2}, e{3}, "_LT"}),
				            r = Table.RenameColumns(t, {{e{1}, "_Fim"}, {e{2}, "_Qtd"}, {e{3}, "_Op"}}),
				            c = Table.AddColumn(r, "Etapa", each e{0}, type text),
				            l = Table.TransformColumns(c, {{"_LT", (x) => if e{0} = "Extração/Teste" then x else null, type nullable number}})
				        in
				            l),
				    Empilhada = Table.Combine(PorEtapa),
				    Tipada = Table.TransformColumns(Empilhada, {
				        {"_Fim", ParaDataHora, type nullable datetime},
				        {"_Qtd", ParaNumero, type nullable number},
				        {"_Op", ParaTexto, type nullable text}}),
				    Concluidas = Table.SelectRows(Tipada, each [_Fim] <> null),
				    ComDataRef = Table.AddColumn(Concluidas, "Data de Referência", each
				        if Time.Hour([_Fim]) * 60 + Time.Minute([_Fim]) < 320
				            then Date.AddDays(DateTime.Date([_Fim]), -1)
				            else DateTime.Date([_Fim]),
				        type date),
				    ComDataFim = Table.AddColumn(ComDataRef, "Data do Fim", each DateTime.Date([_Fim]), type date),
				    Renomeada = Table.RenameColumns(ComDataFim, {
				        {"ID", "ID Ficha"}, {"_Fim", "Fim da Etapa"}, {"_Qtd", "Quantidade (m)"},
				        {"_Op", "Operador"}, {"_LT", "Lead Time Tranç→Cabine (h)"}}),
				    Selecionada = Table.SelectColumns(Renomeada, {"ID Ficha", "OP", "Etapa", "Fim da Etapa",
				        "Data de Referência", "Data do Fim", "Quantidade (m)", "Operador", "Lead Time Tranç→Cabine (h)"}),
				    Tipos = Table.TransformColumnTypes(Selecionada, {{"ID Ficha", Int64.Type}, {"OP", type text}})
				in
				    Tipos
```

## Bloco 2 — Relacionamentos (muitos-para-um, sentido único)

```
createOrReplace

	relationship fEtapaOP_Etapa
		fromColumn: fEtapaOP.Etapa
		toColumn: dEtapa.Etapa

	relationship fEtapaOP_DataRef
		fromColumn: fEtapaOP.'Data de Referência'
		toColumn: dCalendario.Date

	relationship fEtapaOP_DataDoFim
		isActive: false
		fromColumn: fEtapaOP.'Data do Fim'
		toColumn: dCalendario.Date
```

O ativo é o da `Data de Referência` (regra de ligação da §A.3). O inativo só é usado pelas medidas da pasta
`Conferência`, para bater 1:1 com o HTML, que conta o dia pela data civil do fim.

## Bloco 3 — Medidas (tabela `Medidas`)

Regras aplicadas: `DIVIDE` sempre; nenhuma `COALESCE(x, 0)` em exibição (sem dado = BLANK). O `+ 0` que aparece dentro
de `AVERAGEX` é cálculo, não exibição: um dia produtivo sem apontamento na etapa conta 0, como no HTML.

**Dia produtivo:** dia (Data de Referência) com Trançagem ≥ 3.000 m. Quando o filtro deixa um dia só, ele entra sempre
(se tiver qualquer apontamento no trecho). Esse padrão aparece como `VAR UmDia` / `VAR Dias` em cada medida de média.

```
createOrReplace

	ref table Medidas

		/// K01 do catálogo. Metragem concluída na etapa. Nunca somar etapas diferentes (sempre com recorte de etapa).
		measure 'Metros Produzidos' =
				-- Metragem concluída por etapa no recorte. Base de quase todo o resto. K01 · C13 · MEL-116
				CALCULATE (
				    SUM ( fEtapaOP[Quantidade (m)] ),
				    NOT ISBLANK ( fEtapaOP[Fim da Etapa] )
				)
			formatString: #,0
			displayFolder: Produção

		measure 'Pessoas Distintas' =
				-- Operadores distintos que apontaram a etapa no recorte. Estimativa pelos apontamentos, não é escala oficial.
				DISTINCTCOUNTNOBLANK ( fEtapaOP[Operador] )
			formatString: #,0
			displayFolder: Fluxo Tranç→Cabine

		measure '_Metros Trançagem Dia' =
				-- Metros da Trançagem no contexto, ignorando a etapa da linha/coluna do visual. Define o dia produtivo.
				CALCULATE (
				    [Metros Produzidos],
				    REMOVEFILTERS ( dEtapa ),
				    dEtapa[Etapa] = "Trançagem"
				)
			formatString: #,0
			isHidden
			displayFolder: Fluxo Tranç→Cabine\Auxiliares

		measure '_Metros Trecho Dia' =
				-- Metros de qualquer etapa do trecho no contexto (só para saber se o dia tem apontamento).
				CALCULATE (
				    [Metros Produzidos],
				    REMOVEFILTERS ( dEtapa ),
				    dEtapa[Trecho Tranç-Cabine] = TRUE ()
				)
			formatString: #,0
			isHidden
			displayFolder: Fluxo Tranç→Cabine\Auxiliares

		measure 'Dias Produtivos (Fluxo)' =
				-- Quantos dias entram nas médias: Trançagem >= 3.000 m; com um dia escolhido, ele mesmo.
				VAR UmDia = HASONEVALUE ( dCalendario[Date] )
				VAR Dias =
				    FILTER (
				        VALUES ( dCalendario[Date] ),
				        IF ( UmDia, NOT ISBLANK ( [_Metros Trecho Dia] ), [_Metros Trançagem Dia] >= 3000 )
				    )
				RETURN
				    COUNTROWS ( Dias )
			formatString: #,0
			displayFolder: Fluxo Tranç→Cabine

		measure 'Vazão por Etapa (m/dia)' =
				-- Vazão (TH) da etapa: média de metros/dia nos dias produtivos. Dia produtivo sem apontamento na etapa conta 0 (igual ao HTML).
				VAR UmDia = HASONEVALUE ( dCalendario[Date] )
				VAR Dias =
				    FILTER (
				        VALUES ( dCalendario[Date] ),
				        IF ( UmDia, NOT ISBLANK ( [_Metros Trecho Dia] ), [_Metros Trançagem Dia] >= 3000 )
				    )
				RETURN
				    IF (
				        HASONEVALUE ( dEtapa[Ordem_Fluxo] ) && NOT ISEMPTY ( Dias ),
				        AVERAGEX ( Dias, [Metros Produzidos] + 0 )
				    )
			formatString: #,0
			displayFolder: Fluxo Tranç→Cabine

		measure 'Vazão Trançagem (m/dia)' =
				-- Vazão da Trançagem (entrada do trecho).
				CALCULATE ( [Vazão por Etapa (m/dia)], REMOVEFILTERS ( dEtapa ), dEtapa[Etapa] = "Trançagem" )
			formatString: #,0
			displayFolder: Fluxo Tranç→Cabine

		measure 'Vazão Cabine (m/dia)' =
				-- Vazão da Extração/Teste (cabine): a vazão da linha (TH).
				CALCULATE ( [Vazão por Etapa (m/dia)], REMOVEFILTERS ( dEtapa ), dEtapa[Etapa] = "Extração/Teste" )
			formatString: #,0
			displayFolder: Fluxo Tranç→Cabine

		measure 'Pessoas por Dia' =
				-- Média, nos dias produtivos, das pessoas distintas que apontaram a etapa no dia. Dia sem apontamento na etapa conta 0.
				VAR UmDia = HASONEVALUE ( dCalendario[Date] )
				VAR Dias =
				    FILTER (
				        VALUES ( dCalendario[Date] ),
				        IF ( UmDia, NOT ISBLANK ( [_Metros Trecho Dia] ), [_Metros Trançagem Dia] >= 3000 )
				    )
				RETURN
				    IF (
				        HASONEVALUE ( dEtapa[Ordem_Fluxo] ) && NOT ISEMPTY ( Dias ),
				        AVERAGEX ( Dias, [Pessoas Distintas] + 0 )
				    )
			formatString: #,0.0
			displayFolder: Fluxo Tranç→Cabine

		measure 'Pessoas Máx no Dia' =
				-- Maior número de pessoas distintas num dia produtivo, na etapa (o "máx" do cartão).
				VAR UmDia = HASONEVALUE ( dCalendario[Date] )
				VAR Dias =
				    FILTER (
				        VALUES ( dCalendario[Date] ),
				        IF ( UmDia, NOT ISBLANK ( [_Metros Trecho Dia] ), [_Metros Trançagem Dia] >= 3000 )
				    )
				RETURN
				    IF ( HASONEVALUE ( dEtapa[Ordem_Fluxo] ), MAXX ( Dias, [Pessoas Distintas] ) )
			formatString: #,0
			displayFolder: Fluxo Tranç→Cabine

		measure 'Pessoas por Dia no Trecho' =
				-- Soma das pessoas/dia médias das 6 etapas (o mesmo operador em duas etapas conta nas duas).
				CALCULATE (
				    SUMX ( VALUES ( dEtapa[Ordem_Fluxo] ), [Pessoas por Dia] ),
				    REMOVEFILTERS ( dEtapa ),
				    dEtapa[Trecho Tranç-Cabine] = TRUE ()
				)
			formatString: #,0.0
			displayFolder: Fluxo Tranç→Cabine

		measure 'Pessoas Trançagem (por dia)' =
				-- Pessoas/dia na Trançagem.
				CALCULATE ( [Pessoas por Dia], REMOVEFILTERS ( dEtapa ), dEtapa[Etapa] = "Trançagem" )
			formatString: #,0.0
			displayFolder: Fluxo Tranç→Cabine

		measure 'Pessoas Cabine (por dia)' =
				-- Pessoas/dia na Extração/Teste (cabine).
				CALCULATE ( [Pessoas por Dia], REMOVEFILTERS ( dEtapa ), dEtapa[Etapa] = "Extração/Teste" )
			formatString: #,0.0
			displayFolder: Fluxo Tranç→Cabine

		measure 'Pessoas Trançagem / Cabine' =
				-- Texto do cartão "pessoas: trançagem / cabine" (ex.: 6,9 / 5,0). Sem dado: BLANK.
				VAR T = [Pessoas Trançagem (por dia)]
				VAR C = [Pessoas Cabine (por dia)]
				RETURN
				    IF (
				        NOT ISBLANK ( T ) || NOT ISBLANK ( C ),
				        IF ( ISBLANK ( T ), "–", FORMAT ( T, "0.0", "pt-BR" ) ) & " / "
				            & IF ( ISBLANK ( C ), "–", FORMAT ( C, "0.0", "pt-BR" ) )
				    )
			displayFolder: Fluxo Tranç→Cabine

		measure 'm por Pessoa' =
				-- Produtividade da mão de obra: vazão ÷ pessoas/dia (m por pessoa·dia).
				DIVIDE ( [Vazão por Etapa (m/dia)], [Pessoas por Dia] )
			formatString: #,0
			displayFolder: Fluxo Tranç→Cabine

		measure 'm por Pessoa Cabine' =
				-- m por pessoa na cabine (cartão do topo).
				CALCULATE ( [m por Pessoa], REMOVEFILTERS ( dEtapa ), dEtapa[Etapa] = "Extração/Teste" )
			formatString: #,0
			displayFolder: Fluxo Tranç→Cabine

		measure 'Conteúdo de Mão de Obra (pessoas/1.000 m)' =
				-- Pessoas por 1.000 m da etapa (Yamazumi com pessoa no lugar do tempo).
				DIVIDE ( [Pessoas por Dia], DIVIDE ( [Vazão por Etapa (m/dia)], 1000 ) )
			formatString: 0.00
			displayFolder: Fluxo Tranç→Cabine

		measure 'Conteúdo Médio do Trecho (pessoas/1.000 m)' =
				-- Média simples do conteúdo de mão de obra das etapas do trecho que têm valor (linha tracejada).
				VAR T =
				    CALCULATETABLE (
				        ADDCOLUMNS ( VALUES ( dEtapa[Ordem_Fluxo] ), "@c", [Conteúdo de Mão de Obra (pessoas/1.000 m)] ),
				        REMOVEFILTERS ( dEtapa ),
				        dEtapa[Trecho Tranç-Cabine] = TRUE ()
				    )
				RETURN
				    AVERAGEX ( FILTER ( T, NOT ISBLANK ( [@c] ) ), [@c] )
			formatString: 0.00
			displayFolder: Fluxo Tranç→Cabine

		measure '_Maior Conteúdo do Trecho' =
				-- Maior conteúdo de mão de obra entre as etapas do trecho (escala das barras SVG).
				VAR T =
				    CALCULATETABLE (
				        ADDCOLUMNS ( VALUES ( dEtapa[Ordem_Fluxo] ), "@c", [Conteúdo de Mão de Obra (pessoas/1.000 m)] ),
				        REMOVEFILTERS ( dEtapa ),
				        dEtapa[Trecho Tranç-Cabine] = TRUE ()
				    )
				RETURN
				    MAXX ( T, [@c] )
			formatString: 0.00
			isHidden
			displayFolder: Fluxo Tranç→Cabine\Auxiliares

		measure '_Posição Conteúdo' =
				-- 1 = etapa com mais gente por metro no trecho. As posições 1 e 2 ficam laranja nos cartões.
				VAR Atual = [Conteúdo de Mão de Obra (pessoas/1.000 m)]
				VAR T =
				    CALCULATETABLE (
				        ADDCOLUMNS ( VALUES ( dEtapa[Ordem_Fluxo] ), "@c", [Conteúdo de Mão de Obra (pessoas/1.000 m)] ),
				        REMOVEFILTERS ( dEtapa ),
				        dEtapa[Trecho Tranç-Cabine] = TRUE ()
				    )
				RETURN
				    IF (
				        HASONEVALUE ( dEtapa[Ordem_Fluxo] ) && NOT ISBLANK ( Atual ),
				        COUNTROWS ( FILTER ( T, [@c] > Atual ) ) + 1
				    )
			formatString: 0
			isHidden
			displayFolder: Fluxo Tranç→Cabine\Auxiliares

		measure '_Maior Vazão do Trecho' =
				-- Maior vazão entre as etapas do trecho (escala da barra de metros do cartão).
				VAR T =
				    CALCULATETABLE (
				        ADDCOLUMNS ( VALUES ( dEtapa[Ordem_Fluxo] ), "@v", [Vazão por Etapa (m/dia)] ),
				        REMOVEFILTERS ( dEtapa ),
				        dEtapa[Trecho Tranç-Cabine] = TRUE ()
				    )
				RETURN
				    MAXX ( T, [@v] )
			formatString: #,0
			isHidden
			displayFolder: Fluxo Tranç→Cabine\Auxiliares

		measure '_Menor Vazão do Trecho' =
				-- Menor vazão positiva entre as etapas do trecho (valor da restrição).
				VAR T =
				    CALCULATETABLE (
				        ADDCOLUMNS ( VALUES ( dEtapa[Ordem_Fluxo] ), "@v", [Vazão por Etapa (m/dia)] ),
				        REMOVEFILTERS ( dEtapa ),
				        dEtapa[Trecho Tranç-Cabine] = TRUE ()
				    )
				RETURN
				    MINX ( FILTER ( T, [@v] > 0 ), [@v] )
			formatString: #,0
			isHidden
			displayFolder: Fluxo Tranç→Cabine\Auxiliares

		measure 'Eficiência de Balanceamento' =
				-- Σ conteúdo ÷ (n etapas × maior conteúdo), nas etapas com valor (Scholl, 1999). 100% = mesma gente por metro em todas.
				VAR T =
				    CALCULATETABLE (
				        ADDCOLUMNS ( VALUES ( dEtapa[Ordem_Fluxo] ), "@c", [Conteúdo de Mão de Obra (pessoas/1.000 m)] ),
				        REMOVEFILTERS ( dEtapa ),
				        dEtapa[Trecho Tranç-Cabine] = TRUE ()
				    )
				VAR Validas = FILTER ( T, NOT ISBLANK ( [@c] ) )
				VAR N = COUNTROWS ( Validas )
				VAR Maior = MAXX ( Validas, [@c] )
				VAR Soma = SUMX ( Validas, [@c] )
				RETURN
				    DIVIDE ( Soma, N * Maior )
			formatString: 0%
			displayFolder: Fluxo Tranç→Cabine

		measure 'Perda de Balanceamento' =
				-- 1 − eficiência de balanceamento.
				VAR E = [Eficiência de Balanceamento]
				RETURN
				    IF ( NOT ISBLANK ( E ), 1 - E )
			formatString: 0%
			displayFolder: Fluxo Tranç→Cabine

		measure 'Lead Time Tranç→Cabine (h)' =
				-- Mediana por ficha (fim da Trançagem → fim da Extração, entre 0,5 h e 720 h) em cada dia produtivo da saída na cabine; média entre os dias. Mesmo cálculo do HTML. C4
				VAR UmDia = HASONEVALUE ( dCalendario[Date] )
				VAR Dias =
				    FILTER (
				        VALUES ( dCalendario[Date] ),
				        IF ( UmDia, NOT ISBLANK ( [_Metros Trecho Dia] ), [_Metros Trançagem Dia] >= 3000 )
				    )
				RETURN
				    AVERAGEX (
				        Dias,
				        CALCULATE (
				            MEDIAN ( fEtapaOP[Lead Time Tranç→Cabine (h)] ),
				            REMOVEFILTERS ( dEtapa ),
				            fEtapaOP[Lead Time Tranç→Cabine (h)] >= 0.5,
				            fEtapaOP[Lead Time Tranç→Cabine (h)] <= 720
				        )
				    )
			formatString: #,0
			displayFolder: Fluxo Tranç→Cabine

		measure 'Lead Time Mediano do Período (h)' =
				-- Uma mediana só, de todas as fichas que saíram da cabine nos dias produtivos (K07/C4 ao pé da letra). Fica ao lado do de cima para comparar.
				VAR UmDia = HASONEVALUE ( dCalendario[Date] )
				VAR Dias =
				    FILTER (
				        VALUES ( dCalendario[Date] ),
				        IF ( UmDia, NOT ISBLANK ( [_Metros Trecho Dia] ), [_Metros Trançagem Dia] >= 3000 )
				    )
				RETURN
				    CALCULATE (
				        MEDIAN ( fEtapaOP[Lead Time Tranç→Cabine (h)] ),
				        Dias,
				        REMOVEFILTERS ( dEtapa ),
				        fEtapaOP[Lead Time Tranç→Cabine (h)] >= 0.5,
				        fEtapaOP[Lead Time Tranç→Cabine (h)] <= 720
				    )
			formatString: #,0
			displayFolder: Fluxo Tranç→Cabine

		measure 'WIP Little (m)' =
				-- Lei de Little (1961): metros em processo entre trançagem e cabine = vazão da cabine × lead time em dias.
				VAR TH = [Vazão Cabine (m/dia)]
				VAR LT = [Lead Time Tranç→Cabine (h)]
				RETURN
				    IF ( NOT ISBLANK ( TH ) && NOT ISBLANK ( LT ), TH * LT / 24 )
			formatString: #,0
			displayFolder: Fluxo Tranç→Cabine

		measure 'CV Vazão Trançagem' =
				-- Coeficiente de variação (desvio amostral ÷ média) dos metros/dia da Trançagem nos dias produtivos. Precisa de 2 dias ou mais.
				VAR Dias =
				    FILTER ( VALUES ( dCalendario[Date] ), [_Metros Trançagem Dia] >= 3000 )
				RETURN
				    IF (
				        COUNTROWS ( Dias ) >= 2,
				        DIVIDE (
				            STDEVX.S ( Dias, [_Metros Trançagem Dia] ),
				            AVERAGEX ( Dias, [_Metros Trançagem Dia] )
				        )
				    )
			formatString: 0%
			displayFolder: Fluxo Tranç→Cabine

		measure 'Rendimento de Fluxo' =
				-- Metros/dia da cabine ÷ metros/dia da trançagem no período.
				DIVIDE ( [Vazão Cabine (m/dia)], [Vazão Trançagem (m/dia)] )
			formatString: 0%
			displayFolder: Fluxo Tranç→Cabine

		measure 'Etapa de Menor Vazão' =
				-- Restrição de vazão (Teoria das Restrições): etapa do trecho com menor m/dia positivo. Empate: a primeira no fluxo.
				VAR T =
				    CALCULATETABLE (
				        ADDCOLUMNS ( VALUES ( dEtapa[Ordem_Fluxo] ), "@v", [Vazão por Etapa (m/dia)] ),
				        REMOVEFILTERS ( dEtapa ),
				        dEtapa[Trecho Tranç-Cabine] = TRUE ()
				    )
				VAR Menor = TOPN ( 1, FILTER ( T, [@v] > 0 ), [@v], ASC, dEtapa[Ordem_Fluxo], ASC )
				VAR Ordem = MAXX ( Menor, dEtapa[Ordem_Fluxo] )
				RETURN
				    IF (
				        NOT ISBLANK ( Ordem ),
				        CALCULATE ( MAX ( dEtapa[Etapa no Fluxo] ), REMOVEFILTERS ( dEtapa ), dEtapa[Ordem_Fluxo] = Ordem )
				    )
			displayFolder: Fluxo Tranç→Cabine

		measure 'Etapa de Maior Conteúdo' =
				-- Restrição de mão de obra: etapa do trecho com mais pessoas por 1.000 m. Empate: a primeira no fluxo.
				VAR T =
				    CALCULATETABLE (
				        ADDCOLUMNS ( VALUES ( dEtapa[Ordem_Fluxo] ), "@c", [Conteúdo de Mão de Obra (pessoas/1.000 m)] ),
				        REMOVEFILTERS ( dEtapa ),
				        dEtapa[Trecho Tranç-Cabine] = TRUE ()
				    )
				VAR Maior = TOPN ( 1, FILTER ( T, [@c] > 0 ), [@c], DESC, dEtapa[Ordem_Fluxo], ASC )
				VAR Ordem = MAXX ( Maior, dEtapa[Ordem_Fluxo] )
				RETURN
				    IF (
				        NOT ISBLANK ( Ordem ),
				        CALCULATE ( MAX ( dEtapa[Etapa no Fluxo] ), REMOVEFILTERS ( dEtapa ), dEtapa[Ordem_Fluxo] = Ordem )
				    )
			displayFolder: Fluxo Tranç→Cabine

		measure 'Título Cartões' =
				-- Título dinâmico da matriz de cartões (formatação condicional do título).
				VAR N = [Dias Produtivos (Fluxo)]
				RETURN
				    "Quanta gente e quanto metro cada etapa usa por dia?"
				        & IF ( NOT ISBLANK ( N ), "  ·  " & FORMAT ( N, "#,0", "pt-BR" ) & IF ( N = 1, " dia", " dias produtivos" ) )
			displayFolder: Fluxo Tranç→Cabine\Leitura

		measure 'Título Conteúdo' =
				-- Título dinâmico da tabela de conteúdo de mão de obra.
				VAR M = [Conteúdo Médio do Trecho (pessoas/1.000 m)]
				RETURN
				    "Quais etapas usam mais gente por 1.000 m?"
				        & IF ( NOT ISBLANK ( M ), "  ·  tracejado = média " & FORMAT ( M, "0.00", "pt-BR" ) )
			displayFolder: Fluxo Tranç→Cabine\Leitura

		measure 'Leitura 1 Restrição' =
				-- Frase da restrição de vazão.
				VAR E = [Etapa de Menor Vazão]
				VAR V = [_Menor Vazão do Trecho]
				RETURN
				    IF (
				        NOT ISBLANK ( E ),
				        "A etapa que mais limita a vazão é " & E & " (" & FORMAT ( V, "#,0", "pt-BR" )
				            & " m/dia). Pela Teoria das Restrições, só o que melhora ali aumenta a entrega da linha."
				    )
			displayFolder: Fluxo Tranç→Cabine\Leitura

		measure 'Leitura 2 Mão de Obra' =
				-- Frase da restrição de mão de obra.
				VAR E = [Etapa de Maior Conteúdo]
				VAR C = [_Maior Conteúdo do Trecho]
				VAR M = [Conteúdo Médio do Trecho (pessoas/1.000 m)]
				RETURN
				    IF (
				        NOT ISBLANK ( E ),
				        "A etapa que mais consome gente por metro é " & E & " (" & FORMAT ( C, "0.00", "pt-BR" )
				            & " pessoas por 1.000 m, " & FORMAT ( DIVIDE ( C, M ), "0.0", "pt-BR" )
				            & "× a média). É onde está a maior movimentação de pessoas."
				    )
			displayFolder: Fluxo Tranç→Cabine\Leitura

		measure 'Leitura 3 Balanceamento' =
				-- Frase da eficiência de balanceamento.
				VAR B = [Eficiência de Balanceamento]
				RETURN
				    IF (
				        NOT ISBLANK ( B ),
				        "Eficiência de balanceamento de " & FORMAT ( B, "0%", "pt-BR" )
				            & " (100% seria o mesmo número de pessoas por metro em todas as etapas). Quanto menor, mais desigual a distribuição de gente entre as etapas, o que indica espaço para realocação."
				    )
			displayFolder: Fluxo Tranç→Cabine\Leitura

		measure 'Leitura 4 Little' =
				-- Frase da Lei de Little.
				VAR W = [WIP Little (m)]
				VAR LT = [Lead Time Tranç→Cabine (h)]
				RETURN
				    IF (
				        NOT ISBLANK ( W ),
				        "Pela Lei de Little, cerca de " & FORMAT ( W, "#,0", "pt-BR" )
				            & " m ficam em processo entre a trançagem e a cabine (" & FORMAT ( LT, "#,0", "pt-BR" )
				            & " h de lead time). Reduzir lead time ou variabilidade reduz esse estoque sem mexer na vazão."
				    )
			displayFolder: Fluxo Tranç→Cabine\Leitura

		measure 'Leitura 5 Dia Único' =
				-- Aviso quando o filtro deixa um dia só.
				IF (
				    HASONEVALUE ( dCalendario[Date] ) && NOT ISBLANK ( [_Metros Trecho Dia] ),
				    "Dia único: a média é o próprio dia, então a leitura de variabilidade não se aplica."
				)
			displayFolder: Fluxo Tranç→Cabine\Leitura

		measure 'Leitura Automática' =
				-- Leitura completa conforme o filtro, um parágrafo por linha. Sem dado: "Sem dados no filtro."
				VAR Partes =
				    {
				        ( 1, [Leitura 1 Restrição] ),
				        ( 2, [Leitura 2 Mão de Obra] ),
				        ( 3, [Leitura 3 Balanceamento] ),
				        ( 4, [Leitura 4 Little] ),
				        ( 5, [Leitura 5 Dia Único] )
				    }
				VAR Texto =
				    CONCATENATEX ( FILTER ( Partes, [Value2] <> "" ), [Value2], UNICHAR ( 10 ), [Value1], ASC )
				RETURN
				    IF ( Texto = "", "Sem dados no filtro.", Texto )
			displayFolder: Fluxo Tranç→Cabine\Leitura

		measure 'Metros Trançagem no Dia' =
				-- Série diária do gráfico (eixo dCalendario[Date]). Dia não produtivo fica em branco, salvo quando a segmentação deixa um dia só.
				VAR UmDiaSelecionado = COUNTROWS ( ALLSELECTED ( dCalendario[Date] ) ) = 1
				VAR Dias =
				    FILTER ( VALUES ( dCalendario[Date] ), UmDiaSelecionado || [_Metros Trançagem Dia] >= 3000 )
				RETURN
				    CALCULATE ( [Metros Produzidos], Dias, REMOVEFILTERS ( dEtapa ), dEtapa[Etapa] = "Trançagem" )
			formatString: #,0
			displayFolder: Fluxo Tranç→Cabine\Séries

		measure 'Metros Cabine no Dia' =
				-- Série diária da cabine (mesma regra de dia produtivo da série da Trançagem).
				VAR UmDiaSelecionado = COUNTROWS ( ALLSELECTED ( dCalendario[Date] ) ) = 1
				VAR Dias =
				    FILTER ( VALUES ( dCalendario[Date] ), UmDiaSelecionado || [_Metros Trançagem Dia] >= 3000 )
				RETURN
				    CALCULATE ( [Metros Produzidos], Dias, REMOVEFILTERS ( dEtapa ), dEtapa[Etapa] = "Extração/Teste" )
			formatString: #,0
			displayFolder: Fluxo Tranç→Cabine\Séries

		measure 'Pessoas Trançagem no Dia' =
				-- Série diária de pessoas distintas na Trançagem.
				VAR UmDiaSelecionado = COUNTROWS ( ALLSELECTED ( dCalendario[Date] ) ) = 1
				VAR Dias =
				    FILTER ( VALUES ( dCalendario[Date] ), UmDiaSelecionado || [_Metros Trançagem Dia] >= 3000 )
				RETURN
				    CALCULATE ( [Pessoas Distintas], Dias, REMOVEFILTERS ( dEtapa ), dEtapa[Etapa] = "Trançagem" )
			formatString: #,0
			displayFolder: Fluxo Tranç→Cabine\Séries

		measure 'Pessoas Cabine no Dia' =
				-- Série diária de pessoas distintas na cabine.
				VAR UmDiaSelecionado = COUNTROWS ( ALLSELECTED ( dCalendario[Date] ) ) = 1
				VAR Dias =
				    FILTER ( VALUES ( dCalendario[Date] ), UmDiaSelecionado || [_Metros Trançagem Dia] >= 3000 )
				RETURN
				    CALCULATE ( [Pessoas Distintas], Dias, REMOVEFILTERS ( dEtapa ), dEtapa[Etapa] = "Extração/Teste" )
			formatString: #,0
			displayFolder: Fluxo Tranç→Cabine\Séries

		measure 'Conf HTML · Vazão Cabine (m/dia)' =
				-- Conferência: mesma medida contando o dia pela data civil do fim, como o painel HTML. Não exibir na página.
				CALCULATE ( [Vazão Cabine (m/dia)], USERELATIONSHIP ( fEtapaOP[Data do Fim], dCalendario[Date] ) )
			formatString: #,0
			isHidden
			displayFolder: Fluxo Tranç→Cabine\Conferência

		measure 'Conf HTML · Pessoas Trançagem / Cabine' =
				-- Conferência pela data civil do fim.
				CALCULATE ( [Pessoas Trançagem / Cabine], USERELATIONSHIP ( fEtapaOP[Data do Fim], dCalendario[Date] ) )
			isHidden
			displayFolder: Fluxo Tranç→Cabine\Conferência

		measure 'Conf HTML · Eficiência de Balanceamento' =
				-- Conferência pela data civil do fim.
				CALCULATE ( [Eficiência de Balanceamento], USERELATIONSHIP ( fEtapaOP[Data do Fim], dCalendario[Date] ) )
			formatString: 0.0%
			isHidden
			displayFolder: Fluxo Tranç→Cabine\Conferência

		measure 'Conf HTML · Lead Time (h)' =
				-- Conferência pela data civil do fim.
				CALCULATE ( [Lead Time Tranç→Cabine (h)], USERELATIONSHIP ( fEtapaOP[Data do Fim], dCalendario[Date] ) )
			formatString: #,0.0
			isHidden
			displayFolder: Fluxo Tranç→Cabine\Conferência

		measure 'Conf HTML · WIP Little (m)' =
				-- Conferência pela data civil do fim.
				CALCULATE ( [WIP Little (m)], USERELATIONSHIP ( fEtapaOP[Data do Fim], dCalendario[Date] ) )
			formatString: #,0
			isHidden
			displayFolder: Fluxo Tranç→Cabine\Conferência

		measure 'Conf HTML · CV Vazão Trançagem' =
				-- Conferência pela data civil do fim.
				CALCULATE ( [CV Vazão Trançagem], USERELATIONSHIP ( fEtapaOP[Data do Fim], dCalendario[Date] ) )
			formatString: 0.0%
			isHidden
			displayFolder: Fluxo Tranç→Cabine\Conferência

		measure 'Conf HTML · Rendimento de Fluxo' =
				-- Conferência pela data civil do fim.
				CALCULATE ( [Rendimento de Fluxo], USERELATIONSHIP ( fEtapaOP[Data do Fim], dCalendario[Date] ) )
			formatString: 0.0%
			isHidden
			displayFolder: Fluxo Tranç→Cabine\Conferência
```

---

## Mapa: KPI do HTML → medida

| Cartão do HTML | Medida |
|---|---|
| m/dia na cabine (vazão da linha) | `Vazão Cabine (m/dia)` |
| pessoas somando as 6 etapas | `Pessoas por Dia no Trecho` |
| pessoas: trançagem / cabine | `Pessoas Trançagem / Cabine` (texto) |
| m por pessoa na cabine | `m por Pessoa Cabine` |
| eficiência de balanceamento (perda) | `Eficiência de Balanceamento` / `Perda de Balanceamento` |
| lead time trançagem→cabine | `Lead Time Tranç→Cabine (h)` |
| m em processo (Little) | `WIP Little (m)` |
| variabilidade (CV) da vazão | `CV Vazão Trançagem` |
| rendimento de fluxo | `Rendimento de Fluxo` |
| tag "menor vazão" / "mais mão de obra" | `Etapa de Menor Vazão` / `Etapa de Maior Conteúdo` |
| leitura automática | `Leitura Automática` (ou `Leitura 1..5` no textbox) |
| gráficos de evolução | `Metros/Pessoas Trançagem no Dia`, `Metros/Pessoas Cabine no Dia` |

## Reuso e o que não foi duplicado

- `Metros Produzidos` é o K01 do catálogo, escrito igual. Ele só nasce agora porque a `fEtapaOP` não existia.
  As medidas do modelo com nome parecido (`Metragem Produzida` da `ficha_producao`, `Realizado Etapa` da `Etapas`,
  `Produção por Etapa` da `Eventos_Producao`) usam outra tabela e outra regra de dia. Não servem para o grão ficha × etapa.
- Não existia medida de pessoas por etapa. `Pessoas Distintas` é nova.
- Lead time: o K08 do catálogo (`Lead Time Total (h)`) mede a OP inteira, do primeiro ao último apontamento. Aqui o
  trecho é só trançagem→cabine, então a medida é outra e tem outro nome.

## Linhas de diário (para colar depois de aplicar e conferir)

```
2026-11-03 | ENTREGUE | PowerBI/fEtapaOP | v0.1 | MEL-116 A.1 | fEtapaOP (1 linha = ficha × etapa concluída, unpivot da ficha_producao com Operador, Data de Referência 05:20 e lead time trançagem→cabine) + dEtapa (8 etapas, Ordem_Fluxo, Trecho Tranç-Cabine) em TMDL; aguarda colar no modelo (GMS)
2026-11-03 | ENTREGUE | PowerBI/Fluxo Tranç→Cabine | v0.1 | — | Medidas da página-piloto (vazão, pessoas, m/pessoa, conteúdo de MO, balanceamento, lead time, WIP de Little, CV, rendimento, restrições, leitura automática e cartões SVG por etapa) em Analises/Fluxo_Trancadeira_Cabine/BI; aguarda colar e conferir contra o HTML
2026-11-03 | PENDÊNCIA | PowerBI/fEtapaOP | — | A.3 | fEtapaOP saiu sem a coluna Turno (fora do escopo do piloto); antes de virar fato oficial, revisor define o Turno pela fn_Turno
```
