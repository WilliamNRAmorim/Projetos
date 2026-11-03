# Medidas: Fluxo Trançagem → Cabine (página-piloto do BI) — PENDENTE DE APLICAR · v0.2 (revisão aplicada)

Fonte do desenho e das fórmulas: `../painel_template.html` (KPIs) e `../ilustracao_headcount.html` (cartões aprovados).
Lógica de dados: `../extrair_dados.py`. As medidas SVG estão em `Medidas_SVG_FluxoTrancagemCabine.md`; layout e
conferência em `LEIAME_Pagina.md`.

Pastas de exibição pelos domínios da §B.1.3:
- `Produção\Fluxo Tranç→Cabine`: vazão, pessoas, m/pessoa, conteúdo, balanceamento, WIP, CV, rendimento, restrições
  (subpasta `Visual` para títulos, leitura, séries e SVG).
- `Tempo\Fluxo Tranç→Cabine`: lead time.
- `Auxiliares\Fluxo Tranç→Cabine`: medidas `_` ocultas.
- `Auxiliares\Conferência Fluxo Tranç→Cabine`: conferência contra o HTML, ocultas.

**ID:** não há MEL aberta para este piloto. Toda medida leva `MEL-???` na primeira linha, e o ID real sai do
`python gms.py --novo` quando o William registrar a entrega. Os `Cxx` vêm do catálogo: K01 → C13, K04/K05 → C3 e
C1, K07/K08 → C4.

---

## 0. Decisão: `Etapas` × tabela nova

**Evidência** (TMDL do modelo, snapshot de 03/11/2026 em
`GMS/PowerBI/Modelo_PBIP/GMS_Modelo.SemanticModel/definition`):
- `tables/Etapas.tmdl`: a `Etapas` é **tabela calculada** (`UNION` de `SELECTCOLUMNS` sobre a `ficha_producao`) com
  as colunas `OP`, `Mangueira`, `Etapa`, `OrdemEtapa`, `DataHora`, `Metragem`, `Data`, `Turno` e `AnoMes`.
  - **Não tem operador.**
  - `Metragem` é a `Metragem_Extracao` repetida em todas as etapas. Não mede a vazão de cada etapa.
  - Não tem Vulcanização.
  - `Data` é a data civil de `DataHora`, sem a virada das 05:20.
  - `Turno` usa as fronteiras 320/820/1340.
- O modelo publicado não tem `fEtapaOP`, `dTurno` nem as funções `fn_*`.

**Decisão (provada):** a `Etapas` não serve para pessoas nem para vazão por etapa. O piloto usa a tabela própria
**`fPessoasEtapaOP`**, montada da `ficha_producao`, que tem `quantidade_*`, `operador_*` e `data_hora_final_*` de
cada etapa. O nome canônico `fEtapaOP` fica livre para a MEL-116. A `Metros Produzidos` (K01) também **não** é criada
aqui: o piloto usa a auxiliar `_Metros Fluxo`, com a mesma definição, para não deixar a K01 numa tabela provisória.

Linha para o diário (colar quando aplicar):
```
2026-11-03 | DECISÃO | PowerBI/fPessoasEtapaOP | v0.1 | MEL-116 A.3 | Piloto Fluxo Tranç→Cabine usa tabela própria fPessoasEtapaOP (ficha × etapa com Quantidade, Operador, Turno e Data de Referência) montada da ficha_producao. Provado no TMDL de 03/11: a Etapas é tabela calculada sem operador, com Metragem = Metragem_Extracao repetida em todas as etapas (não mede vazão por etapa), sem Vulcanização e com data civil sem a virada das 05:20. O nome canônico fEtapaOP fica livre para a MEL-116
```

---

## Bloco 0 — Funções da §B.3.3 e `dTurno` da §B.2.3 (necessário)

**Este bloco é obrigatório.** O modelo publicado não tem `fn_MinutoDoDia`, `fn_Turno`, `fn_DataRef` nem `dTurno`:
o `expressions.tmdl` só tem `Refugo_Bobinadeira` e `RefugoExtrusora_estrutura`, e a lista de tabelas do servidor
não tem `dTurno`. As funções estão copiadas da §B.3.3 com as fronteiras da norma (MEL-250: T1 320–836, T2 837–1339,
T3 1340–319). Não mexa nas fronteiras aqui: mudança de turno passa pelo `revisor`.

**Divergência de turno no modelo atual (não alterar, só registrar):**

| Onde | Fronteiras |
|---|---|
| `Etapas[Turno]` e `ficha_producao[Turno_Producao]` | 320 / **820** / 1340 (2º turno às 13:40) |
| medida `ficha_producao[Turno Atual]` | 320 / **828** / **1361** (2º às 13:48, 3º às 22:41) |
| Norma (`GMS/CLAUDE.md`, §B.2.3 após a MEL-250) e este piloto | 320 / **837** / 1340 (2º às 13:57, 3º às 22:20) |

Um mesmo fim entre 13:40 e 13:56 cai no 2º turno nas páginas atuais e no 1º turno no piloto. Pendência para o
`revisor`/William (linha no fim do arquivo).

**Atenção:** o `PowerBI/modelo/montagem_modelo.md` propõe uma `dTurno` com chave de texto ("1º TURNO") para a
Montagem. Ela não foi aplicada: não está na lista do servidor. Se um dia for, terá de usar esta `dTurno` (chave
numérica da §B.2.3) em vez de criar outra.

```
createOrReplace

	expression fn_MinutoDoDia =
			// minutos desde a meia-noite (§B.3.3)
			(carimbo as nullable datetime) as nullable number =>
			    if carimbo = null then null
			    else Time.Hour(DateTime.Time(carimbo)) * 60 + Time.Minute(DateTime.Time(carimbo))

	expression fn_Turno =
			// fronteiras reais do GMS (§B.2.3, MEL-250): T1 05:20–13:56, T2 13:57–22:19, T3 22:20–05:19
			(minutos as nullable number) as nullable number =>
			    if minutos = null then null
			    else if minutos >= 320 and minutos < 837 then 1
			    else if minutos >= 837 and minutos < 1340 then 2
			    else 3

	expression fn_DataRef =
			// antes das 05:20 o dia de produção ainda é o anterior (§B.3.3)
			(carimbo as nullable datetime) as nullable date =>
			    if carimbo = null then null
			    else if fn_MinutoDoDia(carimbo) < 320
			        then Date.AddDays(DateTime.Date(carimbo), -1)
			        else DateTime.Date(carimbo)

	table dTurno

		/// 1 linha = 1 turno do hose cell (§B.2.3). Fronteiras escritas uma vez.
		column Turno
			dataType: int64
			formatString: 0
			summarizeBy: none
			sourceColumn: Turno

		column Rótulo
			dataType: string
			summarizeBy: none
			sortByColumn: Turno
			sourceColumn: Rótulo

		column Início
			dataType: string
			summarizeBy: none
			sourceColumn: Início

		column Fim
			dataType: string
			summarizeBy: none
			sourceColumn: Fim

		column 'Minuto Inicial'
			dataType: int64
			isHidden
			formatString: 0
			summarizeBy: none
			sourceColumn: Minuto Inicial

		column 'Minuto Final'
			dataType: int64
			isHidden
			formatString: 0
			summarizeBy: none
			sourceColumn: Minuto Final

		partition dTurno = m
			mode: import
			source =
				#table(
				    type table [Turno = Int64.Type, #"Rótulo" = text, #"Início" = text, Fim = text, #"Minuto Inicial" = Int64.Type, #"Minuto Final" = Int64.Type],
				    {
				        {1, "1º Turno", "05:20", "13:56", 320, 836},
				        {2, "2º Turno", "13:57", "22:19", 837, 1339},
				        {3, "3º Turno", "22:20", "05:19", 1340, 319}
				    })
```

## Bloco 1 — Tabelas `dEtapa` e `fPessoasEtapaOP` (TMDL view → colar → Aplicar → Atualizar)

### Fuso (regra no M, não no checklist)

**Padrão: `FichaJaEmHoraLocal = true`** (a data-hora da `ficha_producao` já está na hora da fábrica; não subtrai 3 h).

É uma hipótese, tirada do uso do modelo atual (TMDL de 03/11):
- A partição da `ficha_producao` não converte fuso: `SharePoint.Tables` → `Origem` → renomeia/remove colunas, sem
  `DateTimeZone` nem `#duration`. As `data_hora_final_*` chegam como `dateTime`.
- O modelo trata esses valores como hora local. `Etapas[Turno]` e `ficha_producao[Turno_Producao]` aplicam
  `HOUR()`/`MINUTE()` direto sobre eles, com o 1º turno a partir de 05:20 (320 min), e `DataProducao` é a data civil
  do mesmo valor. Se fosse UTC, todos os turnos das páginas atuais estariam 3 h deslocados.

**O William confere numa ficha conhecida antes de aplicar:** na prévia da `ficha_producao` (Transformar dados), pegue
uma ficha e compare `data_hora_final_extracao` com a hora da mesma ficha no app (Consulta OP).
- Igual: deixe `true`.
- 3 h adiantada: os valores estão em UTC. Troque para `FichaJaEmHoraLocal = false` (a `ParaDataHora` passa a subtrair
  3 h) e registre isso no diário, porque aí as colunas de turno do modelo atual também estão erradas.

O que a `ParaDataHora` faz em cada caso: valor com fuso (`datetimezone`) sempre vira UTC−3 e perde o fuso, sem depender
do padrão. Valor sem fuso (`datetime`) ou texto só recebe −3 h quando `FichaJaEmHoraLocal = false`.

**Colunas da `ficha_producao` usadas (conferidas no `tables/ficha_producao.tmdl`):** `ID` (int64), `OP` (double,
convertida para texto) e, para cada etapa, `data_hora_final_*` (dateTime), `quantidade_*` (double no snapshot; a
`ParaNumero` aceita número ou texto) e `operador_*` (string). As 8 trincas do `Mapa` batem exatamente com os nomes do
modelo. A coluna da Trançagem é `data_hora_final_trancadeira`, mas a quantidade e o operador são
`quantidade_trancagem` e `operador_trancagem`. As colunas `Turno_mandril`, `Turno_Tubo`, `Turno_Trançagem`,
`Turno_Cobertura`, `Turno_Bandagem`, `Turno_Vulcanização`, `Turno_Debandagem`, `Turno_Extr/Teste` e `Turno_Producao`
**não são usadas**: o turno sai da `fn_Turno` sobre o fim da etapa.

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

	table fPessoasEtapaOP

		/// 1 linha = 1 ficha × 1 etapa concluída (Fim da Etapa preenchido). Fonte: ficha_producao (unpivot das 8 etapas). Piloto Fluxo Tranç→Cabine.
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

		/// Dia de produção (fn_DataRef): antes das 05:20 o fim pertence ao dia anterior.
		column 'Data de Referência'
			dataType: dateTime
			isHidden
			formatString: dd/mm/yyyy
			summarizeBy: none
			sourceColumn: Data de Referência

		/// Turno do fim da etapa (fn_Turno sobre fn_MinutoDoDia).
		column Turno
			dataType: int64
			isHidden
			formatString: 0
			summarizeBy: none
			sourceColumn: Turno

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

		partition fPessoasEtapaOP = m
			mode: import
			source =
				let
				    // Fuso: true = data_hora_final_* já está na hora da fábrica (como o modelo atual usa). Se a ficha conferida estiver 3 h adiantada (UTC), troque para false.
				    FichaJaEmHoraLocal = true,
				    // Quantidade acima disto por ficha e etapa é erro de digitação (máximo limpo observado: 995 m; achados de 03/11: fichas 3306, 3686, 3647, 4010 com milhões de m).
				    // Vira vazio e sai das somas; a pessoa continua contada. Corrigir na origem e conferir com a consulta de maiores quantidades do LEIAME.
				    QtdMaxFicha = 2000,
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
				    // Sem fuso: mantém (FichaJaEmHoraLocal = true) ou trata como UTC e passa para UTC−3 (false).
				    DeUTC = (d as datetime) as datetime => if FichaJaEmHoraLocal then d else d - #duration(0, 3, 0, 0),
				    // Data-hora: datetimezone vira UTC−3; datetime e texto sem fuso seguem o DeUTC; date fica como está.
				    ParaDataHora = (v as any) as nullable datetime =>
				        if v = null then null
				        else if Value.Is(v, type datetimezone) then DateTimeZone.RemoveZone(DateTimeZone.SwitchZone(v, -3))
				        else if Value.Is(v, type datetime) then DeUTC(v)
				        else if Value.Is(v, type date) then DateTime.From(v)
				        else
				            let
				                t = Text.Trim(Text.From(v)),
				                comFuso = try DateTimeZone.RemoveZone(DateTimeZone.SwitchZone(DateTimeZone.FromText(t), -3)) otherwise null,
				                semFuso = try DeUTC(DateTime.FromText(t, "pt-BR")) otherwise null
				            in
				                if Text.EndsWith(t, "Z") or Text.Contains(t, "+") then comFuso else semFuso,
				    // Número: aceita número ou texto pt-BR (§B.3.4). "675,5" → 675,5; "1.200" e "1.200,5" → milhar com ponto;
				    // "12.5" (ponto decimal, sem grupos de 3 dígitos) → 12,5.
				    ParaNumero = (v as any) as nullable number =>
				        if v = null then null
				        else if Value.Is(v, type number) then v
				        else
				            let
				                t = Text.Remove(Text.Trim(Text.From(v)), {" "}),
				                partes = Text.Split(t, "."),
				                pontoEhMilhar =
				                    List.Count(partes) > 1
				                        and Text.Length(partes{0}) >= 1 and Text.Length(partes{0}) <= 3
				                        and List.AllTrue(List.Transform(List.Skip(partes, 1), each Text.Length(Text.BeforeDelimiter(_, ",")) = 3)),
				                u =
				                    if Text.Contains(t, ",") or pontoEhMilhar
				                        then Text.Replace(Text.Remove(t, {"."}), ",", ".")
				                        else t
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
				        {"_Qtd", (q) => let n = ParaNumero(q) in if n <> null and n > QtdMaxFicha then null else n, type nullable number},
				        {"_Op", ParaTexto, type nullable text}}),
				    Concluidas = Table.SelectRows(Tipada, each [_Fim] <> null),
				    // Turno e Data de Referência carimbados uma vez, pelas funções do modelo (§B.3.3).
				    ComTurno = Table.AddColumn(Concluidas, "Turno", each fn_Turno(fn_MinutoDoDia([_Fim])), Int64.Type),
				    ComDataRef = Table.AddColumn(ComTurno, "Data de Referência", each fn_DataRef([_Fim]), type date),
				    ComDataFim = Table.AddColumn(ComDataRef, "Data do Fim", each DateTime.Date([_Fim]), type date),
				    Renomeada = Table.RenameColumns(ComDataFim, {
				        {"ID", "ID Ficha"}, {"_Fim", "Fim da Etapa"}, {"_Qtd", "Quantidade (m)"},
				        {"_Op", "Operador"}, {"_LT", "Lead Time Tranç→Cabine (h)"}}),
				    Selecionada = Table.SelectColumns(Renomeada, {"ID Ficha", "OP", "Etapa", "Fim da Etapa", "Data de Referência",
				        "Turno", "Data do Fim", "Quantidade (m)", "Operador", "Lead Time Tranç→Cabine (h)"}),
				    Tipos = Table.TransformColumnTypes(Selecionada, {{"ID Ficha", Int64.Type}, {"OP", type text}})
				in
				    Tipos
```

**Antes de colar:**
- Se o TMDL recusar com "duplicate"/"already exists" em `dEtapa` ou `fPessoasEtapaOP`, o nome já existe: não
  sobrescreva, me avise.
- A partição lê a consulta `ficha_producao` e as funções `fn_*` (Bloco 0) pelo nome. Se o serviço recusar a
  referência à `ficha_producao`, troque `Origem = ficha_producao` pelos 4 passos da partição dela (`Fonte`, `Origem`
  com o `Id` da lista, `Renomeado`, `Limpo`) e chame o resultado de `Origem`.
- Os relacionamentos do Bloco 2 usam `dCalendario[Date]`, que existe no modelo (calculada, 2025–2027).

## Bloco 2 — Relacionamentos (muitos-para-um, sentido único, da dimensão para o fato)

```
createOrReplace

	relationship fPessoasEtapaOP_Etapa
		fromColumn: fPessoasEtapaOP.Etapa
		toColumn: dEtapa.Etapa

	relationship fPessoasEtapaOP_DataRef
		fromColumn: fPessoasEtapaOP.'Data de Referência'
		toColumn: dCalendario.Date

	relationship fPessoasEtapaOP_Turno
		fromColumn: fPessoasEtapaOP.Turno
		toColumn: dTurno.Turno

	relationship fPessoasEtapaOP_DataDoFim
		isActive: false
		fromColumn: fPessoasEtapaOP.'Data do Fim'
		toColumn: dCalendario.Date
```

Os ativos são `Data de Referência` e `Turno` (regra de ligação da §A.3). O inativo só serve às medidas de
`Conferência`, para bater 1:1 com o HTML, que conta o dia pela data civil do fim.

## Bloco 3 — Medidas (tabela `Medidas`)

Regras aplicadas: `DIVIDE` sempre; nenhuma `COALESCE(x, 0)` em exibição (sem dado = BLANK). O `+ 0` dentro de
`AVERAGEX` é cálculo, não exibição: um dia produtivo sem apontamento na etapa conta 0, como no HTML.

**Dia produtivo:** dia (Data de Referência) com Trançagem ≥ 3.000 m **no dia inteiro**, qualquer que seja o turno
filtrado. Com Turno escolhido, a média é dos metros/pessoas daquele turno nos dias produtivos. Quando o filtro deixa um
dia só, ele entra sempre, se tiver qualquer apontamento no trecho. O padrão aparece como `VAR UmDia` / `VAR Dias`.

```
createOrReplace

	ref table Medidas

		measure '_Metros Fluxo' =
				-- Metragem concluída na etapa (mesma definição da K01 sobre a tabela do piloto) · MEL-??? · C13
				CALCULATE (
				    SUM ( fPessoasEtapaOP[Quantidade (m)] ),
				    NOT ISBLANK ( fPessoasEtapaOP[Fim da Etapa] )
				)
			formatString: #,0
			isHidden
			displayFolder: Auxiliares\Fluxo Tranç→Cabine

		measure '_Metros Trançagem Dia' =
				-- Metros da Trançagem no dia inteiro (ignora etapa e turno do visual). Define o dia produtivo · MEL-???
				CALCULATE (
				    [_Metros Fluxo],
				    REMOVEFILTERS ( dEtapa ),
				    REMOVEFILTERS ( dTurno ),
				    dEtapa[Etapa] = "Trançagem"
				)
			formatString: #,0
			isHidden
			displayFolder: Auxiliares\Fluxo Tranç→Cabine

		measure '_Metros Trançagem no Recorte' =
				-- Metros da Trançagem respeitando o turno filtrado (valor do CV) · MEL-???
				CALCULATE ( [_Metros Fluxo], REMOVEFILTERS ( dEtapa ), dEtapa[Etapa] = "Trançagem" )
			formatString: #,0
			isHidden
			displayFolder: Auxiliares\Fluxo Tranç→Cabine

		measure '_Metros Trecho Dia' =
				-- Metros de qualquer etapa do trecho no dia inteiro (só para saber se o dia tem apontamento) · MEL-???
				CALCULATE (
				    [_Metros Fluxo],
				    REMOVEFILTERS ( dEtapa ),
				    REMOVEFILTERS ( dTurno ),
				    dEtapa[Trecho Tranç-Cabine] = TRUE ()
				)
			formatString: #,0
			isHidden
			displayFolder: Auxiliares\Fluxo Tranç→Cabine

		measure 'Pessoas Distintas' =
				-- Operadores distintos que apontaram a etapa no recorte (estimativa pelos apontamentos, não é escala oficial) · MEL-???
				DISTINCTCOUNTNOBLANK ( fPessoasEtapaOP[Operador] )
			formatString: #,0
			displayFolder: Produção\Fluxo Tranç→Cabine

		measure 'Dias Produtivos (Fluxo)' =
				-- Dias que entram nas médias: Trançagem >= 3.000 m no dia; com um dia escolhido, ele mesmo · MEL-???
				VAR UmDia = HASONEVALUE ( dCalendario[Date] )
				VAR Dias =
				    FILTER (
				        VALUES ( dCalendario[Date] ),
				        IF ( UmDia, NOT ISBLANK ( [_Metros Trecho Dia] ), [_Metros Trançagem Dia] >= 3000 )
				    )
				RETURN
				    COUNTROWS ( Dias )
			formatString: #,0
			displayFolder: Produção\Fluxo Tranç→Cabine

		measure 'Vazão por Etapa (m/dia)' =
				-- Vazão (TH) da etapa: média de metros/dia nos dias produtivos; dia produtivo sem apontamento na etapa conta 0 · MEL-??? · C3
				VAR UmDia = HASONEVALUE ( dCalendario[Date] )
				VAR Dias =
				    FILTER (
				        VALUES ( dCalendario[Date] ),
				        IF ( UmDia, NOT ISBLANK ( [_Metros Trecho Dia] ), [_Metros Trançagem Dia] >= 3000 )
				    )
				RETURN
				    IF (
				        HASONEVALUE ( dEtapa[Ordem_Fluxo] ) && NOT ISEMPTY ( Dias ) && SUMX ( Dias, [_Metros Fluxo] ) > 0,
				        AVERAGEX ( Dias, [_Metros Fluxo] + 0 )
				    )
			formatString: #,0
			displayFolder: Produção\Fluxo Tranç→Cabine

		measure 'Vazão Trançagem (m/dia)' =
				-- Vazão da Trançagem (entrada do trecho) · MEL-??? · C3
				CALCULATE ( [Vazão por Etapa (m/dia)], REMOVEFILTERS ( dEtapa ), dEtapa[Etapa] = "Trançagem" )
			formatString: #,0
			displayFolder: Produção\Fluxo Tranç→Cabine

		measure 'Vazão Cabine (m/dia)' =
				-- Vazão da Extração/Teste (cabine): a vazão da linha (TH) · MEL-??? · C3
				CALCULATE ( [Vazão por Etapa (m/dia)], REMOVEFILTERS ( dEtapa ), dEtapa[Etapa] = "Extração/Teste" )
			formatString: #,0
			displayFolder: Produção\Fluxo Tranç→Cabine

		measure 'Pessoas por Dia' =
				-- Média, nos dias produtivos, das pessoas distintas que apontaram a etapa no dia; dia sem apontamento na etapa conta 0 · MEL-???
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
			displayFolder: Produção\Fluxo Tranç→Cabine

		measure 'Pessoas Máx no Dia' =
				-- Maior número de pessoas distintas num dia produtivo, na etapa (o "máx" do cartão) · MEL-???
				VAR UmDia = HASONEVALUE ( dCalendario[Date] )
				VAR Dias =
				    FILTER (
				        VALUES ( dCalendario[Date] ),
				        IF ( UmDia, NOT ISBLANK ( [_Metros Trecho Dia] ), [_Metros Trançagem Dia] >= 3000 )
				    )
				RETURN
				    IF ( HASONEVALUE ( dEtapa[Ordem_Fluxo] ), MAXX ( Dias, [Pessoas Distintas] ) )
			formatString: #,0
			displayFolder: Produção\Fluxo Tranç→Cabine

		measure 'Pessoas por Dia no Trecho' =
				-- Soma das pessoas/dia médias das 6 etapas (o mesmo operador em duas etapas conta nas duas) · MEL-???
				CALCULATE (
				    SUMX ( VALUES ( dEtapa[Ordem_Fluxo] ), [Pessoas por Dia] ),
				    REMOVEFILTERS ( dEtapa ),
				    dEtapa[Trecho Tranç-Cabine] = TRUE ()
				)
			formatString: #,0.0
			displayFolder: Produção\Fluxo Tranç→Cabine

		measure 'Pessoas Trançagem (por dia)' =
				-- Pessoas/dia na Trançagem · MEL-???
				CALCULATE ( [Pessoas por Dia], REMOVEFILTERS ( dEtapa ), dEtapa[Etapa] = "Trançagem" )
			formatString: #,0.0
			displayFolder: Produção\Fluxo Tranç→Cabine

		measure 'Pessoas Cabine (por dia)' =
				-- Pessoas/dia na Extração/Teste (cabine) · MEL-???
				CALCULATE ( [Pessoas por Dia], REMOVEFILTERS ( dEtapa ), dEtapa[Etapa] = "Extração/Teste" )
			formatString: #,0.0
			displayFolder: Produção\Fluxo Tranç→Cabine

		measure 'Pessoas Trançagem / Cabine' =
				-- Texto do cartão "pessoas: trançagem / cabine" (ex.: 6,9 / 5,0); sem dado nas duas: BLANK · MEL-???
				VAR T = [Pessoas Trançagem (por dia)]
				VAR C = [Pessoas Cabine (por dia)]
				RETURN
				    IF (
				        NOT ISBLANK ( T ) || NOT ISBLANK ( C ),
				        IF ( ISBLANK ( T ), "–", FORMAT ( T, "0.0", "pt-BR" ) ) & " / "
				            & IF ( ISBLANK ( C ), "–", FORMAT ( C, "0.0", "pt-BR" ) )
				    )
			displayFolder: Produção\Fluxo Tranç→Cabine

		measure 'm por Pessoa' =
				-- Produtividade da mão de obra: vazão ÷ pessoas/dia (m por pessoa·dia) · MEL-???
				DIVIDE ( [Vazão por Etapa (m/dia)], [Pessoas por Dia] )
			formatString: #,0
			displayFolder: Produção\Fluxo Tranç→Cabine

		measure 'm por Pessoa Cabine' =
				-- m por pessoa na cabine (cartão do topo) · MEL-???
				CALCULATE ( [m por Pessoa], REMOVEFILTERS ( dEtapa ), dEtapa[Etapa] = "Extração/Teste" )
			formatString: #,0
			displayFolder: Produção\Fluxo Tranç→Cabine

		measure 'Conteúdo de Mão de Obra (pessoas/1.000 m)' =
				-- Pessoas por 1.000 m da etapa (Yamazumi com pessoa no lugar do tempo) · MEL-???
				DIVIDE ( [Pessoas por Dia], DIVIDE ( [Vazão por Etapa (m/dia)], 1000 ) )
			formatString: 0.00
			displayFolder: Produção\Fluxo Tranç→Cabine

		measure 'Conteúdo Médio do Trecho (pessoas/1.000 m)' =
				-- Média simples do conteúdo de mão de obra das etapas do trecho com valor (linha tracejada) · MEL-???
				VAR T =
				    CALCULATETABLE (
				        ADDCOLUMNS ( VALUES ( dEtapa[Ordem_Fluxo] ), "@c", [Conteúdo de Mão de Obra (pessoas/1.000 m)] ),
				        REMOVEFILTERS ( dEtapa ),
				        dEtapa[Trecho Tranç-Cabine] = TRUE ()
				    )
				RETURN
				    AVERAGEX ( FILTER ( T, NOT ISBLANK ( [@c] ) ), [@c] )
			formatString: 0.00
			displayFolder: Produção\Fluxo Tranç→Cabine

		measure '_Maior Conteúdo do Trecho' =
				-- Maior conteúdo de mão de obra entre as etapas do trecho (escala das barras SVG) · MEL-???
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
			displayFolder: Auxiliares\Fluxo Tranç→Cabine

		measure '_Posição Conteúdo' =
				-- 1 = etapa com mais gente por metro no trecho; as posições 1 e 2 ficam laranja nos cartões · MEL-???
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
			displayFolder: Auxiliares\Fluxo Tranç→Cabine

		measure '_Maior Vazão do Trecho' =
				-- Maior vazão entre as etapas do trecho (escala da barra de metros do cartão) · MEL-??? · C3
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
			displayFolder: Auxiliares\Fluxo Tranç→Cabine

		measure '_Menor Vazão do Trecho' =
				-- Menor vazão positiva entre as etapas do trecho (valor da restrição) · MEL-??? · C3
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
			displayFolder: Auxiliares\Fluxo Tranç→Cabine

		measure 'Eficiência de Balanceamento' =
				-- Σ conteúdo ÷ (n etapas × maior conteúdo), nas etapas com valor (Scholl, 1999); 100% = mesma gente por metro em todas · MEL-???
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
			displayFolder: Produção\Fluxo Tranç→Cabine

		measure 'Perda de Balanceamento' =
				-- 1 − eficiência de balanceamento · MEL-???
				VAR E = [Eficiência de Balanceamento]
				RETURN
				    IF ( NOT ISBLANK ( E ), 1 - E )
			formatString: 0%
			displayFolder: Produção\Fluxo Tranç→Cabine

		measure 'Lead Time Tranç→Cabine (h)' =
				-- Mediana única, no período, das fichas que saíram da cabine em dia produtivo: fim da Trançagem → fim da Extração, 0,5 h a 720 h (K07/C4) · MEL-??? · C4
				VAR UmDia = HASONEVALUE ( dCalendario[Date] )
				VAR Dias =
				    FILTER (
				        VALUES ( dCalendario[Date] ),
				        IF ( UmDia, NOT ISBLANK ( [_Metros Trecho Dia] ), [_Metros Trançagem Dia] >= 3000 )
				    )
				RETURN
				    CALCULATE (
				        MEDIAN ( fPessoasEtapaOP[Lead Time Tranç→Cabine (h)] ),
				        Dias,
				        REMOVEFILTERS ( dEtapa ),
				        fPessoasEtapaOP[Lead Time Tranç→Cabine (h)] >= 0.5,
				        fPessoasEtapaOP[Lead Time Tranç→Cabine (h)] <= 720
				    )
			formatString: #,0
			displayFolder: Tempo\Fluxo Tranç→Cabine

		measure '_Lead Time Médio (h)' =
				-- Média do lead time trançagem→cabine das fichas que saíram da cabine nos dias do recorte (todos os dias, 0,5 h a 720 h); W da Lei de Little · MEL-??? · C4
				CALCULATE (
				    AVERAGE ( fPessoasEtapaOP[Lead Time Tranç→Cabine (h)] ),
				    REMOVEFILTERS ( dEtapa ),
				    fPessoasEtapaOP[Lead Time Tranç→Cabine (h)] >= 0.5,
				    fPessoasEtapaOP[Lead Time Tranç→Cabine (h)] <= 720
				)
			formatString: #,0.0
			isHidden
			displayFolder: Auxiliares\Fluxo Tranç→Cabine

		measure '_Vazão Cabine por Dia de Calendário (m/dia)' =
				-- Metros da cabine no recorte ÷ dias de calendário do primeiro ao último dia com apontamento no trecho; λ da Lei de Little · MEL-??? · C3
				VAR ComDado = FILTER ( VALUES ( dCalendario[Date] ), NOT ISBLANK ( [_Metros Trecho Dia] ) )
				VAR Ini = MINX ( ComDado, dCalendario[Date] )
				VAR Fim = MAXX ( ComDado, dCalendario[Date] )
				VAR DiasCalendario = IF ( NOT ISBLANK ( Ini ), INT ( Fim - Ini ) + 1 )
				VAR Metros = CALCULATE ( [_Metros Fluxo], REMOVEFILTERS ( dEtapa ), dEtapa[Etapa] = "Extração/Teste" )
				RETURN
				    DIVIDE ( Metros, DiasCalendario )
			formatString: #,0
			isHidden
			displayFolder: Auxiliares\Fluxo Tranç→Cabine

		measure 'WIP Little (m)' =
				-- Lei de Little (1961): metros em processo entre trançagem e cabine = vazão por dia de calendário × lead time médio em dias · MEL-??? · C3 C1 C4
				VAR Lambda = [_Vazão Cabine por Dia de Calendário (m/dia)]
				VAR W = [_Lead Time Médio (h)]
				RETURN
				    IF ( NOT ISBLANK ( Lambda ) && NOT ISBLANK ( W ), Lambda * W / 24 )
			formatString: #,0
			displayFolder: Produção\Fluxo Tranç→Cabine

		measure 'CV Vazão Trançagem' =
				-- Coeficiente de variação (desvio amostral ÷ média) dos metros/dia da Trançagem (do turno filtrado) nos dias produtivos; precisa de 2 dias ou mais · MEL-???
				VAR Dias =
				    FILTER ( VALUES ( dCalendario[Date] ), [_Metros Trançagem Dia] >= 3000 )
				RETURN
				    IF (
				        COUNTROWS ( Dias ) >= 2,
				        DIVIDE (
				            STDEVX.S ( Dias, [_Metros Trançagem no Recorte] + 0 ),
				            AVERAGEX ( Dias, [_Metros Trançagem no Recorte] + 0 )
				        )
				    )
			formatString: 0%
			displayFolder: Produção\Fluxo Tranç→Cabine

		measure 'Rendimento de Fluxo' =
				-- Metros/dia da cabine ÷ metros/dia da trançagem no período · MEL-???
				DIVIDE ( [Vazão Cabine (m/dia)], [Vazão Trançagem (m/dia)] )
			formatString: 0%
			displayFolder: Produção\Fluxo Tranç→Cabine

		measure 'Etapa de Menor Vazão' =
				-- Restrição de vazão (Teoria das Restrições): etapa do trecho com menor m/dia positivo; empate = a primeira no fluxo · MEL-??? · C3
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
			displayFolder: Produção\Fluxo Tranç→Cabine

		measure 'Etapa de Maior Conteúdo' =
				-- Restrição de mão de obra: etapa do trecho com mais pessoas por 1.000 m; empate = a primeira no fluxo · MEL-???
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
			displayFolder: Produção\Fluxo Tranç→Cabine

		measure 'Título Cartões' =
				-- Título dinâmico da matriz de cartões (formatação condicional do título) · MEL-???
				VAR N = [Dias Produtivos (Fluxo)]
				RETURN
				    "Quanta gente e quanto metro cada etapa usa por dia?"
				        & IF ( NOT ISBLANK ( N ), "  ·  " & FORMAT ( N, "#,0", "pt-BR" ) & IF ( N = 1, " dia", " dias produtivos" ) )
			displayFolder: Produção\Fluxo Tranç→Cabine\Visual

		measure 'Título Conteúdo' =
				-- Título dinâmico da tabela de conteúdo de mão de obra · MEL-???
				VAR M = [Conteúdo Médio do Trecho (pessoas/1.000 m)]
				RETURN
				    "Quais etapas usam mais gente por 1.000 m?"
				        & IF ( NOT ISBLANK ( M ), "  ·  tracejado = média " & FORMAT ( M, "0.00", "pt-BR" ) )
			displayFolder: Produção\Fluxo Tranç→Cabine\Visual

		measure 'Leitura Automática' =
				-- Leitura do filtro em até 5 parágrafos (restrição, mão de obra, balanceamento, Little, dia único); sem dado: "Sem dados no filtro." · MEL-??? · C3 C4
				VAR EtapaV = [Etapa de Menor Vazão]
				VAR MenorV = [_Menor Vazão do Trecho]
				VAR EtapaC = [Etapa de Maior Conteúdo]
				VAR MaiorC = [_Maior Conteúdo do Trecho]
				VAR MediaC = [Conteúdo Médio do Trecho (pessoas/1.000 m)]
				VAR Bal = [Eficiência de Balanceamento]
				VAR Wip = [WIP Little (m)]
				VAR LTMed = [_Lead Time Médio (h)]
				VAR LTMediana = [Lead Time Tranç→Cabine (h)]
				VAR UmDia = HASONEVALUE ( dCalendario[Date] ) && NOT ISBLANK ( [_Metros Trecho Dia] )
				VAR P1 =
				    IF ( NOT ISBLANK ( EtapaV ),
				        "A etapa que mais limita a vazão é " & EtapaV & " (" & FORMAT ( MenorV, "#,0", "pt-BR" )
				            & " m/dia). Pela Teoria das Restrições, só o que melhora ali aumenta a entrega da linha." )
				VAR P2 =
				    IF ( NOT ISBLANK ( EtapaC ),
				        "A etapa que mais consome gente por metro é " & EtapaC & " (" & FORMAT ( MaiorC, "0.00", "pt-BR" )
				            & " pessoas por 1.000 m, " & FORMAT ( DIVIDE ( MaiorC, MediaC ), "0.0", "pt-BR" )
				            & "× a média). É onde está a maior movimentação de pessoas." )
				VAR P3 =
				    IF ( NOT ISBLANK ( Bal ),
				        "Eficiência de balanceamento de " & FORMAT ( Bal, "0%", "pt-BR" )
				            & " (100% seria o mesmo número de pessoas por metro em todas as etapas). Quanto menor, mais desigual a distribuição de gente entre as etapas, o que indica espaço para realocação." )
				VAR P4 =
				    IF ( NOT ISBLANK ( Wip ),
				        "Pela Lei de Little, cerca de " & FORMAT ( Wip, "#,0", "pt-BR" )
				            & " m ficam em processo entre a trançagem e a cabine (lead time médio de " & FORMAT ( LTMed, "#,0", "pt-BR" )
				            & " h" & IF ( NOT ISBLANK ( LTMediana ), "; mediana de " & FORMAT ( LTMediana, "#,0", "pt-BR" ) & " h" )
				            & "). Reduzir lead time ou variabilidade reduz esse estoque sem mexer na vazão." )
				VAR P5 =
				    IF ( UmDia, "Dia único: a média é o próprio dia, então a leitura de variabilidade não se aplica." )
				VAR Partes = { ( 1, P1 ), ( 2, P2 ), ( 3, P3 ), ( 4, P4 ), ( 5, P5 ) }
				VAR Texto =
				    CONCATENATEX ( FILTER ( Partes, [Value2] <> "" ), [Value2], UNICHAR ( 10 ) & UNICHAR ( 10 ), [Value1], ASC )
				RETURN
				    IF ( Texto = "", "Sem dados no filtro.", Texto )
			displayFolder: Produção\Fluxo Tranç→Cabine\Visual

		measure 'Metros Trançagem no Dia' =
				-- Série diária (eixo dCalendario[Date]); dia não produtivo fica em branco, salvo quando a segmentação deixa um dia só · MEL-???
				VAR UmDiaSelecionado = COUNTROWS ( ALLSELECTED ( dCalendario[Date] ) ) = 1
				VAR Dias =
				    FILTER ( VALUES ( dCalendario[Date] ), UmDiaSelecionado || [_Metros Trançagem Dia] >= 3000 )
				RETURN
				    CALCULATE ( [_Metros Fluxo], Dias, REMOVEFILTERS ( dEtapa ), dEtapa[Etapa] = "Trançagem" )
			formatString: #,0
			displayFolder: Produção\Fluxo Tranç→Cabine\Visual

		measure 'Metros Cabine no Dia' =
				-- Série diária da cabine (mesma regra de dia produtivo da série da Trançagem) · MEL-???
				VAR UmDiaSelecionado = COUNTROWS ( ALLSELECTED ( dCalendario[Date] ) ) = 1
				VAR Dias =
				    FILTER ( VALUES ( dCalendario[Date] ), UmDiaSelecionado || [_Metros Trançagem Dia] >= 3000 )
				RETURN
				    CALCULATE ( [_Metros Fluxo], Dias, REMOVEFILTERS ( dEtapa ), dEtapa[Etapa] = "Extração/Teste" )
			formatString: #,0
			displayFolder: Produção\Fluxo Tranç→Cabine\Visual

		measure 'Pessoas Trançagem no Dia' =
				-- Série diária de pessoas distintas na Trançagem · MEL-???
				VAR UmDiaSelecionado = COUNTROWS ( ALLSELECTED ( dCalendario[Date] ) ) = 1
				VAR Dias =
				    FILTER ( VALUES ( dCalendario[Date] ), UmDiaSelecionado || [_Metros Trançagem Dia] >= 3000 )
				RETURN
				    CALCULATE ( [Pessoas Distintas], Dias, REMOVEFILTERS ( dEtapa ), dEtapa[Etapa] = "Trançagem" )
			formatString: #,0
			displayFolder: Produção\Fluxo Tranç→Cabine\Visual

		measure 'Pessoas Cabine no Dia' =
				-- Série diária de pessoas distintas na cabine · MEL-???
				VAR UmDiaSelecionado = COUNTROWS ( ALLSELECTED ( dCalendario[Date] ) ) = 1
				VAR Dias =
				    FILTER ( VALUES ( dCalendario[Date] ), UmDiaSelecionado || [_Metros Trançagem Dia] >= 3000 )
				RETURN
				    CALCULATE ( [Pessoas Distintas], Dias, REMOVEFILTERS ( dEtapa ), dEtapa[Etapa] = "Extração/Teste" )
			formatString: #,0
			displayFolder: Produção\Fluxo Tranç→Cabine\Visual

		measure 'Lead Time Média das Medianas Diárias (h)' =
				-- Conferência: método do painel HTML (mediana por ficha em cada dia produtivo, média entre os dias). Não é KPI · MEL-??? · C4
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
				            MEDIAN ( fPessoasEtapaOP[Lead Time Tranç→Cabine (h)] ),
				            REMOVEFILTERS ( dEtapa ),
				            fPessoasEtapaOP[Lead Time Tranç→Cabine (h)] >= 0.5,
				            fPessoasEtapaOP[Lead Time Tranç→Cabine (h)] <= 720
				        )
				    )
			formatString: #,0.0
			isHidden
			displayFolder: Auxiliares\Conferência Fluxo Tranç→Cabine

		measure 'Conf HTML · Vazão Cabine (m/dia)' =
				-- Conferência: dia pela data civil do fim, como o painel HTML. Não exibir · MEL-???
				CALCULATE ( [Vazão Cabine (m/dia)], USERELATIONSHIP ( fPessoasEtapaOP[Data do Fim], dCalendario[Date] ) )
			formatString: #,0
			isHidden
			displayFolder: Auxiliares\Conferência Fluxo Tranç→Cabine

		measure 'Conf HTML · Pessoas Trançagem / Cabine' =
				-- Conferência pela data civil do fim · MEL-???
				CALCULATE ( [Pessoas Trançagem / Cabine], USERELATIONSHIP ( fPessoasEtapaOP[Data do Fim], dCalendario[Date] ) )
			isHidden
			displayFolder: Auxiliares\Conferência Fluxo Tranç→Cabine

		measure 'Conf HTML · Eficiência de Balanceamento' =
				-- Conferência pela data civil do fim · MEL-???
				CALCULATE ( [Eficiência de Balanceamento], USERELATIONSHIP ( fPessoasEtapaOP[Data do Fim], dCalendario[Date] ) )
			formatString: 0.0%
			isHidden
			displayFolder: Auxiliares\Conferência Fluxo Tranç→Cabine

		measure 'Conf HTML · Lead Time (h)' =
				-- Conferência: média das medianas diárias pela data civil do fim (o "31 h" do HTML) · MEL-??? · C4
				CALCULATE ( [Lead Time Média das Medianas Diárias (h)], USERELATIONSHIP ( fPessoasEtapaOP[Data do Fim], dCalendario[Date] ) )
			formatString: #,0.0
			isHidden
			displayFolder: Auxiliares\Conferência Fluxo Tranç→Cabine

		measure 'Conf HTML · WIP Little (m)' =
				-- Conferência: fórmula do HTML (vazão nos dias produtivos × média das medianas diárias ÷ 24), pela data civil do fim. Não é o WIP oficial · MEL-???
				VAR TH = [Conf HTML · Vazão Cabine (m/dia)]
				VAR LT = [Conf HTML · Lead Time (h)]
				RETURN
				    IF ( NOT ISBLANK ( TH ) && NOT ISBLANK ( LT ), TH * LT / 24 )
			formatString: #,0
			isHidden
			displayFolder: Auxiliares\Conferência Fluxo Tranç→Cabine

		measure 'Conf HTML · CV Vazão Trançagem' =
				-- Conferência pela data civil do fim · MEL-???
				CALCULATE ( [CV Vazão Trançagem], USERELATIONSHIP ( fPessoasEtapaOP[Data do Fim], dCalendario[Date] ) )
			formatString: 0.0%
			isHidden
			displayFolder: Auxiliares\Conferência Fluxo Tranç→Cabine

		measure 'Conf HTML · Rendimento de Fluxo' =
				-- Conferência pela data civil do fim · MEL-???
				CALCULATE ( [Rendimento de Fluxo], USERELATIONSHIP ( fPessoasEtapaOP[Data do Fim], dCalendario[Date] ) )
			formatString: 0.0%
			isHidden
			displayFolder: Auxiliares\Conferência Fluxo Tranç→Cabine
```

---

## Mapa: KPI do HTML → medida

| Cartão do HTML | Medida | Muda em relação ao HTML? |
|---|---|---|
| m/dia na cabine (vazão da linha) | `Vazão Cabine (m/dia)` | só pela regra do dia (05:20) |
| pessoas somando as 6 etapas | `Pessoas por Dia no Trecho` | idem |
| pessoas: trançagem / cabine | `Pessoas Trançagem / Cabine` (texto) | idem |
| m por pessoa na cabine | `m por Pessoa Cabine` | idem |
| eficiência de balanceamento (perda) | `Eficiência de Balanceamento` / `Perda de Balanceamento` | idem |
| lead time trançagem→cabine | `Lead Time Tranç→Cabine (h)` | **sim**: mediana única (K07/C4); o método do HTML ficou em `Conferência` |
| m em processo (Little) | `WIP Little (m)` | **sim**: vazão por dia de calendário × lead time médio |
| variabilidade (CV) da vazão | `CV Vazão Trançagem` | só pela regra do dia |
| rendimento de fluxo | `Rendimento de Fluxo` | idem |
| tag "menor vazão" / "mais mão de obra" | `Etapa de Menor Vazão` / `Etapa de Maior Conteúdo` | idem |
| leitura automática | `Leitura Automática` (uma medida só) | texto do Little cita médio e mediana |
| gráficos de evolução | `Metros/Pessoas Trançagem no Dia`, `Metros/Pessoas Cabine no Dia` | idem |

**Por que o WIP mudou:** a Lei de Little vale com médias de longo prazo: λ = metros que saem por dia de calendário
(fim de semana incluso, porque o estoque fica parado lá) e W = lead time **médio**. O HTML usava a vazão só dos dias
produtivos (λ maior) e a média de medianas diárias (W de outra natureza), e por isso dava 7.196 m. Com a fórmula certa
são cerca de 5.000 m (ver LEIAME 5.4).

## Reuso e o que não foi duplicado

- K01 (`Metros Produzidos`) não foi criada: o piloto usa `_Metros Fluxo`, oculta, com a mesma definição. Quando a tabela
  definitiva existir (`Etapas` confirmada ou `fEtapaOP` da MEL-116), as medidas passam a chamar a K01.
- As medidas parecidas do modelo (`Metragem Produzida` da `ficha_producao`, `Realizado Etapa` da `Etapas`,
  `Produção por Etapa` da `Eventos_Producao`) usam outra tabela e outra regra de dia. Não servem para o grão
  ficha × etapa.
- Não existia medida de pessoas por etapa nem de lead time do trecho. O K08 (`Lead Time Total (h)`) mede a OP inteira.

## Linhas de diário (para colar depois de aplicar e conferir)

```
2026-11-03 | DECISÃO | PowerBI/fPessoasEtapaOP | v0.1 | MEL-116 A.3 | Piloto Fluxo Tranç→Cabine usa tabela própria fPessoasEtapaOP (ficha × etapa com Quantidade, Operador, Turno e Data de Referência) montada da ficha_producao. Provado no TMDL de 03/11: a Etapas é tabela calculada sem operador, com Metragem = Metragem_Extracao repetida em todas as etapas (não mede vazão por etapa), sem Vulcanização e com data civil sem a virada das 05:20. O nome canônico fEtapaOP fica livre para a MEL-116
2026-11-03 | ENTREGUE | PowerBI/Fluxo Tranç→Cabine | v0.2 | MEL-??? | Medidas da página-piloto (vazão, pessoas, m/pessoa, conteúdo de MO, balanceamento, lead time mediano K07, WIP de Little com vazão de calendário × lead time médio, CV, rendimento, restrições, leitura automática e cartões SVG) em Analises/Fluxo_Trancadeira_Cabine/BI; aguarda colar e conferir contra o HTML
2026-11-03 | DECISÃO | PowerBI/Fluxo Tranç→Cabine | v0.2 | C4 | Lead time oficial do trecho trançagem→cabine = mediana única do período (K07/C4); a média das medianas diárias do painel HTML fica só como conferência. WIP de Little = vazão por dia de calendário × lead time médio
2026-11-03 | PENDÊNCIA | PowerBI/turno | — | MEL-250 B.2.3 | Fronteira de turno divergente no modelo: Etapas[Turno] e ficha_producao[Turno_Producao] usam 320/820/1340 (2º turno às 13:40), a medida Turno Atual usa 320/828/1361; a norma e o piloto Fluxo Tranç→Cabine (fn_Turno) usam 320/837/1340. Revisor/William decidem a correção; o piloto não altera o modelo existente
2026-11-03 | PENDÊNCIA | PowerBI/fPessoasEtapaOP | — | B.3.3 | Fuso da ficha_producao assumido como hora local (FichaJaEmHoraLocal = true), pelo uso do modelo atual; William confere numa ficha conhecida antes de aplicar
```
