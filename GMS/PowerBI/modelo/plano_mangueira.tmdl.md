# Plano de mangueira x SAP no modelo (GMS): script TMDL da página `pg_plano_mangueira` — APLICADO no modelo vivo em 23/11/2026 (TMDL view, refresh 10:09)

Só BI. Leva o plano mensal de mangueira do planejamento (planilha `Novembro-10.xlsm`, aba Dados) para o relatório oficial `GMS_Painel`, comparado com a produção do SAP que a página Máscara SAP já lê (`fProducaoSAP`). A página nova é `GMS_Painel.Report/definition/pages/pg_plano_mangueira`; as cinco medidas SVG (`HP · SVG ...`) estão no `reportExtensions.json`. Conferência dos números: `GMS/Analises/Plano_Mangueira/conferir.py`; prévia visual: `GMS/Analises/Plano_Mangueira/prototipo.html`. **Depende do `mascara_producao.tmdl.md` já aplicado** (usa `fProducaoSAP`, `dProdutoSAP`, `dMetaMensal`, `dCalendario[AnoMês]` e as medidas `SAP ...`).

## Antes de colar (ordem obrigatória)
1. **Lista `GMS_PlanoMangueira`** (já criada, Id `34631d40-3ad8-4226-82d6-8d5f8fd1ce0a`, site `OperationsGuaratingueta`). Colunas pelo nome interno: `Title` (= Mangueira), `Mes` (**só data**, dia 1), `CStandard`, `Tipo`, `Arame` (texto) e `Volume` (número, metros do mês). 1 linha por mangueira e mês; o planejamento cola o bloco da planilha. Itens de novembro: `GMS/Analises/Plano_Mangueira/nov_2026_lista.csv`. Sem item no mês, a página mostra "Plano de <mês> não cadastrado".
2. Credencial da lista: a mesma conta organizacional da `dMetaMensal` (privacidade Organizacional).
3. Cole os **3 passos abaixo, um de cada vez**, na ordem, **Apply** em cada um (mesmas regras de digitação do Mascara: sem indentação extra, `Escape` depois de cada linha). Depois do passo 1, **atualize `dPlanoMangueira`**; depois do passo 2, atualize o modelo (a `dClasseMangueira` é calculada e só enche no refresh).
4. Conferir nomes livres antes: `EVALUATE INFO.TABLES()` não deve listar `dPlanoMangueira` nem `dClasseMangueira`; `EVALUATE INFO.MEASURES()` não deve ter nome começando por `HP ` nem `_HP ` (conferido no `Modelo_PBIP` offline em 19/11: livre).
5. **Reabra o projeto** (`GMS_Painel.pbip`) depois de aplicar no modelo e antes de publicar: a página só abre sem erro depois que as medidas existem. O botão novo do menu aparece em todas as páginas e leva a uma página que depende dessas medidas.

## Decisões do script (para o revisor)
- **Produzido** = `fProducaoSAP` com `Produto = "Mangueira"`, unidade `M`, todos os tipos de movimento (101 entra, 102 estorna), por `Material` = código da mangueira, entre o dia 1 do mês da página e `[SAP Data de Corte]`. Reusa `_SAP Mês`, `SAP Data de Corte`, `SAP Dias Contabilizados` e `SAP Dias Úteis` (dias úteis dentro de `CALCULATE ( ..., dProdutoSAP[Produto] = "Mangueira" )` para não pegar o maior entre produtos). O filtro de unidade `M` é acréscimo meu: na conferência local todas as linhas AIH são M (diferença 0), mas protege o plano em metros caso apareça PC.
- **Classificação pelo plano do mês.** C.Standard, Tipo e Arame vêm da linha do plano do próprio mês, não de um cadastro fixo (a mesma mangueira pode mudar de classe de um mês para outro). Mangueira produzida no mês sem linha no plano vai para `Fora do plano` (C.Standard, Tipo e Arame iguais a `Fora do plano`, plano 0), para o total bater com o SAP.
- **Tabelas e relacionamentos.** `dPlanoMangueira` (M, oculta) é o espelho da lista com chave `Chave` = código em maiúsculas. `dClasseMangueira` (DAX calculada) é a dimensão no grão mangueira x mês: linhas do plano mais as linhas `SAP sem plano`. **Sem relacionamento**: o produzido é buscado com `TREATAS ( chaves da dClasseMangueira filtrada, fProducaoSAP[Material] )`. Motivo: a classe depende do mês, então não existe relacionamento simples `Material` → classe sem tornar a chave composta (mês é parte da chave) nem bidirecional; com `TREATAS` o filtro de C.Standard/Tipo/Arame/Mangueira passa só pelas chaves do mês escolhido, e a segmentação de mês (que filtra `dCalendario`) é desligada com `REMOVEFILTERS ( dCalendario )`, como a `SAP Produzido`. Nenhum relacionamento novo, nenhum bidirecional.
- **Caixa do código.** Join e `Table.Group` em M são sensíveis à caixa (`ec215-06L` no plano, `EC215-06L` no SAP). A `Chave` é `UPPER ( TRIM ( ) )` dos dois lados; o `TREATAS` entre texto no DAX não diferencia caixa. Verificação 3 abaixo prova com `ec215-06L`.
- **Fora do plano na conta.** `HP Produzido` (total) = no plano + fora do plano e bate com o SAP. `HP % do Plano`, `HP Atraso` e `HP Para Fechar por dia` usam só `HP Produzido no Plano` (mesma base da planilha: MTD 85.671 m = 52,9%); o fora do plano aparece só como nota pequena no cartão Produzido. Mangueira com Volume 0 mas com linha no plano conta como no plano (a planilha também soma o produzido dela no grupo).
- **Ritmo esperado** (2ª decisão do William em 23/11: atraso igual ao da Produção x meta) = planejado acumulado da GMS_PlanoDiario até o corte ÷ plano total da lista (no total, ritmo × plano = Meta até dd/mm da Produção x meta); Para fechar e Plano Diário escalam o plano pelo planejado do mês ÷ plano total. Antes (1ª decisão) = planejado acumulado da GMS_PlanoDiario até o corte ÷ planejado do mês (nov, corte 20/11: 100.118 ÷ 161.040 = 62,2%), aplicado ao plano por mangueira; sem plano diário no mês, cai na conta por dias. Histórico: (correção de 23/11, ao aplicar: a Mangueira saiu da GMS_MetaMensal e usa a GMS_PlanoDiario) = (dias úteis − dias restantes) / dias úteis, com dias úteis = dias com planejado > 0 na GMS_PlanoDiario e restantes = esses dias depois do corte (mesma base da Máscara SAP); sem plano diário no mês, cai na GMS_MetaMensal e em dias contabilizados do SAP. Versão anterior: dias contabilizados / dias úteis, limitado a 100%; em mês encerrado vale 100% (acréscimo meu, na linha do `_SAP Mês Encerrado`: sem ele um mês passado com menos dias de movimento que dias úteis pareceria adiantado/atrasado sem sentido). **Dias úteis**: o modelo usa a `GMS_MetaMensal` (novembro = 22); a planilha digita 23. Por isso o atraso do modelo difere do da planilha (conferir.py mostra as duas contas). A planilha também digita os dias contabilizados (13); o modelo conta as datas com movimento no SAP.
- **Atraso** = (ritmo − %) × plano, positivo = atrasado. **Para fechar por dia** = (plano − produzido) / (úteis − contab.); é igual a plano/úteis + atraso/(restantes) (a planilha usa a meta planejada digitada em K38, por isso 7.953 lá). Negativo = plano já atingido (o SVG mostra "Plano atingido").
- **Nomes** com prefixo `HP ` (pasta `Plano Mangueira`); auxiliares ocultas `_HP `. `Atraso` e `Dias Restantes` já existem em `ficha_producao`, então os nomes sem prefixo não servem. HSTD, OTIF e Decks ficam fora.
- **Duplicidade na lista.** O M soma o `Volume` e mantém a primeira classificação se a mesma mangueira repetir no mês; classe vazia vira `Sem cadastro`.
- **Escopo do mês.** O plano e o produzido seguem a mesma segmentação de mês da página Máscara SAP (`_SAP Mês`): sem mês único, vale o mês de ontem (BR).

## Medidas
| Medida | Formato | O que é |
|---|---|---|
| `HP Plano do Mês` | #,0 | Volume planejado (lista) do mês da página no contexto C.Standard / Tipo / Arame / Mangueira. |
| `HP Produzido no Plano` | #,0.0 | Metros de mangueira (SAP) até o corte das mangueiras com linha no plano do mês. Igual ao MTD da planilha. |
| `HP Produzido Fora do Plano` | #,0.0 | Metros do mês de mangueiras sem linha no plano (grupo `Fora do plano`). |
| `HP Produzido` | #,0.0 | No plano + fora do plano; no total bate com `SAP Produzido` da Mangueira. |
| `HP % do Plano` | 0.0% | Produzido no plano sobre o plano. |
| `HP % Ritmo Esperado` | 0.0% | Dias contabilizados / dias úteis (máx. 100%; mês fechado 100%). |
| `HP Atraso` | +#,0;-#,0;0 | (ritmo − %) × plano; positivo = atrasado (igual à planilha). |
| `HP Plano Diário` | #,0 | Plano / dias úteis. |
| `HP Para Fechar por dia` | #,0.0 | (plano − produzido) / (úteis − contab.); vazio se mês fechado ou sem dias restantes. |
| `HP Devia até Corte` | #,0 | Ritmo esperado × plano (página de detalhe). |
| `HP Diferença` | #,0 | Plano do mês − produzido (quanto falta; coluna da tabela do detalhe). |
| `HP Produzido no Dia` | #,0 | Produzido do SAP no dia do contexto, para a grade dia a dia (página de detalhe). |
| `_HP Dias Úteis`, `_HP Dias Restantes` | 0 | Ocultas: dias úteis da Mangueira (GMS_MetaMensal) e dias que faltam. |

## 1) Passo 1: tabela `dPlanoMangueira` (cole inteiro, depois Apply e atualize a tabela)
```
createOrReplace

	table dPlanoMangueira

		isHidden

		/// Espelho da lista SharePoint GMS_PlanoMangueira (plano mensal de mangueira do planejamento): 1 linha por mangueira e mês. Chave = código em maiúsculas. Alimenta a dClasseMangueira.
		column Chave
			dataType: string
			isHidden
			summarizeBy: none
			sourceColumn: Chave

		column 'Mês'
			dataType: dateTime
			isHidden
			formatString: mmm/yyyy
			summarizeBy: none
			sourceColumn: Mês

		column Mangueira
			dataType: string
			isHidden
			summarizeBy: none
			sourceColumn: Mangueira

		column 'C.Standard'
			dataType: string
			isHidden
			summarizeBy: none
			sourceColumn: C.Standard

		column Tipo
			dataType: string
			isHidden
			summarizeBy: none
			sourceColumn: Tipo

		column Arame
			dataType: string
			isHidden
			summarizeBy: none
			sourceColumn: Arame

		column Volume
			dataType: double
			isHidden
			formatString: #,0
			summarizeBy: none
			sourceColumn: Volume

		partition dPlanoMangueira = m
			mode: import
			source =
				let
				// Lista SharePoint GMS_PlanoMangueira (Id 34631d40-3ad8-4226-82d6-8d5f8fd1ce0a, criada em 19/11/2026). Nomes internos: Title = Mangueira, Mes = dia 1 do mês, CStandard, Tipo, Arame, Volume (metros do mês). Grão da lista: 1 linha por Mangueira x Mês.
				// Navega pelo Title como a dMetaMensal (pode trocar por [Id = "34631d40-3ad8-4226-82d6-8d5f8fd1ce0a"]).
				// Chave = código em maiúsculas e sem espaço nas pontas (o join em M é sensível à caixa, o DAX não; ex.: ec215-06L no plano e EC215-06L no SAP).
				// Se a mesma Mangueira repetir no mesmo mês, soma o Volume e fica com a primeira classificação (a lista deve ter 1 linha por mangueira e mês).
				Origem = SharePoint.Tables("https://danfoss.sharepoint.com/sites/OperationsGuaratingueta", [Implementation = "2.0", ViewMode = "All"]),
				Lista = Origem{[Title = "GMS_PlanoMangueira"]}[Items],
				Colunas = Table.SelectColumns(Lista, {"Title", "Mes", "CStandard", "Tipo", "Arame", "Volume"}),
				Tipos = Table.TransformColumnTypes(Colunas, {{"Title", type text}, {"CStandard", type text}, {"Tipo", type text}, {"Arame", type text}, {"Volume", type number}}),
				Rotulo = (t as nullable text) as text => if t = null or Text.Trim(t) = "" then "Sem cadastro" else Text.Trim(t),
				Limpo = Table.TransformColumns(Tipos, {{"Mes", each Date.StartOfMonth(Date.From(_)), type date}, {"Title", each Text.Trim(_ ?? ""), type text}, {"CStandard", Rotulo, type text}, {"Tipo", Rotulo, type text}, {"Arame", Rotulo, type text}, {"Volume", each _ ?? 0, type number}}),
				SoLinhas = Table.SelectRows(Limpo, each [Mes] <> null and [Title] <> ""),
				ComChave = Table.AddColumn(SoLinhas, "Chave", each Text.Upper([Title]), type text),
				Agrupado = Table.Group(ComChave, {"Chave", "Mes"}, {{"Mangueira", each List.First([Title]), type text}, {"C.Standard", each List.First([CStandard]), type text}, {"Tipo", each List.First([Tipo]), type text}, {"Arame", each List.First([Arame]), type text}, {"Volume", each List.Sum([Volume]), type number}}),
				Nomes = Table.RenameColumns(Agrupado, {{"Mes", "Mês"}}),
				Final = Table.ReorderColumns(Nomes, {"Chave", "Mês", "Mangueira", "C.Standard", "Tipo", "Arame", "Volume"})
				in
				Final
```

## 2) Passo 2: tabela calculada `dClasseMangueira` (depois Apply e atualize o modelo)
```
createOrReplace

	table dClasseMangueira

		/// Mangueira x mês com a classe (C.Standard, Tipo, Arame) e o plano do mês: linhas do plano + 'Fora do plano' (produzida no SAP sem linha no plano). Sem relacionamento: as medidas HP ligam ao fProducaoSAP por TREATAS na chave.
		column Chave
			dataType: string
			isHidden
			summarizeBy: none
			sourceColumn: [Chave]

		column 'Mês'
			dataType: dateTime
			isHidden
			formatString: mmm/yyyy
			summarizeBy: none
			sourceColumn: [Mês]

		column Mangueira
			dataType: string
			summarizeBy: none
			sourceColumn: [Mangueira]

		column 'C.Standard'
			dataType: string
			summarizeBy: none
			sourceColumn: [C.Standard]

		column Tipo
			dataType: string
			summarizeBy: none
			sourceColumn: [Tipo]

		column Arame
			dataType: string
			summarizeBy: none
			sourceColumn: [Arame]

		column Plano
			dataType: double
			isHidden
			formatString: #,0
			summarizeBy: none
			sourceColumn: [Plano]

		column Origem
			dataType: string
			isHidden
			summarizeBy: none
			sourceColumn: [Origem]

		partition dClasseMangueira = calculated
			mode: import
			source =
				VAR __Plano =
				SELECTCOLUMNS (
				dPlanoMangueira,
				"Chave", dPlanoMangueira[Chave],
				"Mês", dPlanoMangueira[Mês],
				"Mangueira", dPlanoMangueira[Mangueira],
				"C.Standard", dPlanoMangueira[C.Standard],
				"Tipo", dPlanoMangueira[Tipo],
				"Arame", dPlanoMangueira[Arame],
				"Plano", dPlanoMangueira[Volume],
				"Origem", "Plano"
				)
				VAR __Prod =
				DISTINCT (
				SELECTCOLUMNS (
				FILTER ( fProducaoSAP, fProducaoSAP[Produto] = "Mangueira" && fProducaoSAP[Unidade] = "M" ),
				"Chave", UPPER ( TRIM ( fProducaoSAP[Material] ) ),
				"Mês", DATE ( YEAR ( fProducaoSAP[Data] ), MONTH ( fProducaoSAP[Data] ), 1 )
				)
				)
				VAR __Sem =
				EXCEPT ( __Prod, SELECTCOLUMNS ( dPlanoMangueira, "Chave", dPlanoMangueira[Chave], "Mês", dPlanoMangueira[Mês] ) )
				RETURN
				UNION (
				__Plano,
				SELECTCOLUMNS (
				__Sem,
				"Chave", [Chave],
				"Mês", [Mês],
				"Mangueira", [Chave],
				"C.Standard", "Fora do plano",
				"Tipo", "Fora do plano",
				"Arame", "Fora do plano",
				"Plano", CONVERT ( 0, DOUBLE ),
				"Origem", "SAP sem plano"
				)
				)
```

## 3) Passo 3: medidas (depois do refresh)
```
createOrReplace

	ref table Medidas

		measure '_HP Dias Úteis' =
						-- Dias úteis da Mangueira no mês da página: dias com planejado > 0 na lista GMS_PlanoDiario (mesma base da Máscara SAP); sem plano diário no mês, a linha da Mangueira na GMS_MetaMensal. · Plano mangueira x SAP
						VAR __Ini = [_SAP Mês]
						VAR __Plano = CALCULATE ( DISTINCTCOUNT ( dPlanoDiario[Data] ), REMOVEFILTERS ( dCalendario ), dProdutoSAP[Produto] = "Mangueira", dPlanoDiario[Data] >= __Ini, dPlanoDiario[Data] <= EOMONTH ( __Ini, 0 ), dPlanoDiario[Planejado] > 0 )
						RETURN
						IF ( __Plano > 0, __Plano, CALCULATE ( [SAP Dias Úteis], dProdutoSAP[Produto] = "Mangueira" ) )
			formatString: 0
			displayFolder: Plano Mangueira
			isHidden

		measure '_HP Dias Restantes' =
						-- Dias úteis que faltam depois do corte: com plano diário, dias com planejado > 0 depois do corte; sem, dias úteis menos dias contabilizados do SAP. · Plano mangueira x SAP
						VAR __Ini = [_SAP Mês]
						VAR __Corte = [SAP Data de Corte]
						VAR __Plano = CALCULATE ( DISTINCTCOUNT ( dPlanoDiario[Data] ), REMOVEFILTERS ( dCalendario ), dProdutoSAP[Produto] = "Mangueira", dPlanoDiario[Data] >= __Ini, dPlanoDiario[Data] <= EOMONTH ( __Ini, 0 ), dPlanoDiario[Planejado] > 0 )
						VAR __Uteis = [_HP Dias Úteis]
						RETURN
						IF ( __Plano > 0, CALCULATE ( DISTINCTCOUNT ( dPlanoDiario[Data] ), REMOVEFILTERS ( dCalendario ), dProdutoSAP[Produto] = "Mangueira", dPlanoDiario[Data] > __Corte, dPlanoDiario[Data] <= EOMONTH ( __Ini, 0 ), dPlanoDiario[Planejado] > 0 ) + 0, IF ( NOT ISBLANK ( __Uteis ), __Uteis - [SAP Dias Contabilizados] ) )
			formatString: 0
			displayFolder: Plano Mangueira
			isHidden

		measure 'HP Plano do Mês' =
					-- Soma do volume planejado (lista GMS_PlanoMangueira) no mês da página, no contexto de C.Standard, Tipo, Arame ou Mangueira. · Plano mangueira x SAP
					VAR __Mes = [_SAP Mês]
					RETURN
					CALCULATE ( SUM ( dClasseMangueira[Plano] ), dClasseMangueira[Mês] = __Mes )
			formatString: #,0
			displayFolder: Plano Mangueira

		measure 'HP Produzido no Plano' =
					-- Metros de mangueira produzidos (fProducaoSAP, Produto = Mangueira, unidade M, todos os tipos de movimento) até o corte, só das mangueiras que têm linha no plano do mês. É o produzido comparável ao plano (igual ao MTD da planilha). · Plano mangueira x SAP
					VAR __Ini = [_SAP Mês]
					VAR __Corte = [SAP Data de Corte]
					VAR __Chaves = CALCULATETABLE ( VALUES ( dClasseMangueira[Chave] ), dClasseMangueira[Mês] = __Ini, dClasseMangueira[Origem] = "Plano" )
					RETURN
					IF (
					NOT ISBLANK ( __Corte ),
					CALCULATE ( SUM ( fProducaoSAP[Quantidade] ), REMOVEFILTERS ( dCalendario ), fProducaoSAP[Produto] = "Mangueira", fProducaoSAP[Unidade] = "M", fProducaoSAP[Data] >= __Ini, fProducaoSAP[Data] <= __Corte, TREATAS ( __Chaves, fProducaoSAP[Material] ) )
					)
			formatString: #,0.0
			displayFolder: Plano Mangueira

		measure 'HP Produzido Fora do Plano' =
					-- Metros produzidos no mês de mangueiras SEM linha no plano do mês (grupo 'Fora do plano'). · Plano mangueira x SAP
					VAR __Ini = [_SAP Mês]
					VAR __Corte = [SAP Data de Corte]
					VAR __Chaves = CALCULATETABLE ( VALUES ( dClasseMangueira[Chave] ), dClasseMangueira[Mês] = __Ini, dClasseMangueira[Origem] = "SAP sem plano" )
					RETURN
					IF (
					NOT ISBLANK ( __Corte ),
					CALCULATE ( SUM ( fProducaoSAP[Quantidade] ), REMOVEFILTERS ( dCalendario ), fProducaoSAP[Produto] = "Mangueira", fProducaoSAP[Unidade] = "M", fProducaoSAP[Data] >= __Ini, fProducaoSAP[Data] <= __Corte, TREATAS ( __Chaves, fProducaoSAP[Material] ) )
					)
			formatString: #,0.0
			displayFolder: Plano Mangueira

		measure 'HP Produzido' =
					-- Produzido total de mangueira no contexto = no plano + fora do plano; no total bate com [SAP Produzido] da Mangueira. · Plano mangueira x SAP
					[HP Produzido no Plano] + [HP Produzido Fora do Plano]
			formatString: #,0.0
			displayFolder: Plano Mangueira

		measure 'HP % do Plano' =
					-- Produzido no plano sobre o plano do mês. · Plano mangueira x SAP
					DIVIDE ( [HP Produzido no Plano], [HP Plano do Mês] )
			formatString: 0.0%
			displayFolder: Plano Mangueira

		measure '_HP Planejado Mês' =
						-- Planejado do mês da Mangueira na GMS_PlanoDiario (o mesmo da Produção x meta). · Plano mangueira x SAP
						VAR __Ini = [_SAP Mês]
						RETURN
						CALCULATE ( SUM ( dPlanoDiario[Planejado] ), REMOVEFILTERS ( dCalendario ), dProdutoSAP[Produto] = "Mangueira", dPlanoDiario[Data] >= __Ini, dPlanoDiario[Data] <= EOMONTH ( __Ini, 0 ) )
			formatString: #,0
			displayFolder: Plano Mangueira
			isHidden

		measure '_HP Planejado até Corte' =
						-- Planejado acumulado da Mangueira na GMS_PlanoDiario até o corte (a "Meta até dd/mm" da Produção x meta). · Plano mangueira x SAP
						VAR __Ini = [_SAP Mês]
						VAR __Corte = [SAP Data de Corte]
						RETURN
						IF ( NOT ISBLANK ( __Corte ), CALCULATE ( SUM ( dPlanoDiario[Planejado] ), REMOVEFILTERS ( dCalendario ), dProdutoSAP[Produto] = "Mangueira", dPlanoDiario[Data] >= __Ini, dPlanoDiario[Data] <= __Corte ) + 0 )
			formatString: #,0
			displayFolder: Plano Mangueira
			isHidden

		measure '_HP Plano Total' =
						-- Plano do mês da lista GMS_PlanoMangueira somado em todas as mangueiras (ignora C.Standard, tipo, arame e mangueira do contexto). · Plano mangueira x SAP
						CALCULATE ( [HP Plano do Mês], REMOVEFILTERS ( dClasseMangueira ) )
			formatString: #,0
			displayFolder: Plano Mangueira
			isHidden

		measure 'HP % Ritmo Esperado' =
						-- Fração do plano que devia estar feita no corte, igual à Produção x meta: planejado acumulado da GMS_PlanoDiario ÷ plano total da lista. No total, ritmo × plano = a "Meta até dd/mm" da Produção x meta, e o atraso fica igual nas duas páginas (decisão do William, 23/11). Sem plano diário no mês: (dias úteis − restantes) ÷ dias úteis. · Plano mangueira x SAP
						VAR __Mes = [_HP Planejado Mês]
						VAR __Uteis = [_HP Dias Úteis]
						VAR __Rest = [_HP Dias Restantes]
						RETURN
						IF ( ISBLANK ( [SAP Data de Corte] ), BLANK (), IF ( __Mes > 0, MAX ( 0, MIN ( 1, DIVIDE ( [_HP Planejado até Corte], [_HP Plano Total] ) ) ), IF ( [_SAP Mês Encerrado], 1, IF ( __Uteis > 0 && NOT ISBLANK ( __Rest ), MAX ( 0, MIN ( 1, DIVIDE ( __Uteis - __Rest, __Uteis ) ) ) ) ) ) )
			formatString: 0.0%
			displayFolder: Plano Mangueira

		measure 'HP Plano Diário' =
						-- Planejado por dia nos dias que faltam, no contexto: plano × (planejado do mês − planejado até o corte) ÷ plano total ÷ dias restantes. No total é o "(planejado X)" da Produção x meta. Sem plano diário: plano ÷ dias úteis. · Plano mangueira x SAP
						VAR __Mes = [_HP Planejado Mês]
						VAR __Rest = [_HP Dias Restantes]
						RETURN
						IF ( __Mes > 0, IF ( __Rest > 0, DIVIDE ( [HP Plano do Mês] * DIVIDE ( __Mes - [_HP Planejado até Corte], [_HP Plano Total] ), __Rest ) ), DIVIDE ( [HP Plano do Mês], [_HP Dias Úteis] ) )
			formatString: #,0
			displayFolder: Plano Mangueira

		measure 'HP Para Fechar por dia' =
						-- Quanto por dia falta produzir nos dias que faltam, igual à Produção x meta: (plano × planejado do mês ÷ plano total − produzido) ÷ dias restantes. Vazio sem dias restantes ou com o mês fechado. Negativo = plano já atingido. · Plano mangueira x SAP
						VAR __Mes = [_HP Planejado Mês]
						VAR __Rest = [_HP Dias Restantes]
						VAR __Alvo = IF ( __Mes > 0, [HP Plano do Mês] * DIVIDE ( __Mes, [_HP Plano Total] ), [HP Plano do Mês] )
						RETURN
						IF ( __Rest > 0 && NOT [_SAP Mês Encerrado], DIVIDE ( __Alvo - [HP Produzido no Plano], __Rest ) )
			formatString: #,0.0
			displayFolder: Plano Mangueira

		measure 'HP Devia até Corte' =
						-- Metros que deviam estar feitos até o corte no contexto (ritmo esperado × plano). No total = Meta até dd/mm da Produção x meta. · Plano mangueira x SAP
						[HP % Ritmo Esperado] * [HP Plano do Mês]
			formatString: #,0
			displayFolder: Plano Mangueira

		measure 'HP Produzido no Dia' =
						-- Metros de mangueira do SAP no dia do contexto (dCalendario), de mangueiras com linha no plano do mês ou fora do plano, até o corte. Para a grade dia a dia da página de detalhe. · Plano mangueira x SAP
						VAR __Ini = [_SAP Mês]
						VAR __Corte = [SAP Data de Corte]
						VAR __Chaves = CALCULATETABLE ( VALUES ( dClasseMangueira[Chave] ), dClasseMangueira[Mês] = __Ini )
						RETURN
						IF ( NOT ISBLANK ( __Corte ), CALCULATE ( SUM ( fProducaoSAP[Quantidade] ), fProducaoSAP[Produto] = "Mangueira", fProducaoSAP[Unidade] = "M", fProducaoSAP[Data] >= __Ini, fProducaoSAP[Data] <= __Corte, TREATAS ( __Chaves, fProducaoSAP[Material] ) ) )
			formatString: #,0
			displayFolder: Plano Mangueira

		measure 'HP Diferença' =
						-- Plano do mês menos produzido: quanto falta para fechar o plano da mangueira (negativo = já passou do plano). Pedido do William, 23/11. · Plano mangueira x SAP
						[HP Plano do Mês] - [HP Produzido]
			formatString: #,0;-#,0;0
			displayFolder: Plano Mangueira

		measure 'HP Atraso' =
					-- (ritmo esperado - % do plano) x plano, igual à planilha: positivo = atrasado, negativo = adiantado. Vazio sem plano. · Plano mangueira x SAP
					VAR __Plano = [HP Plano do Mês]
					VAR __Ritmo = [HP % Ritmo Esperado]
					RETURN
					IF ( __Plano > 0 && NOT ISBLANK ( __Ritmo ), __Ritmo * __Plano - ( [HP Produzido no Plano] + 0 ) )
			formatString: +#,0;-#,0;0
			displayFolder: Plano Mangueira

```

## 4) Verificação depois do refresh (DAX query view)
1. Classe e plano do mês (esperado em nov/2026: 45 linhas no plano com o CSV, plano total 162.016; mais as linhas `SAP sem plano` se houver):
```
EVALUATE
ROW (
    "Linhas plano", COUNTROWS ( FILTER ( dClasseMangueira, dClasseMangueira[Mês] = DATE ( 2026, 11, 1 ) && dClasseMangueira[Origem] = "Plano" ) ),
    "Fora do plano", COUNTROWS ( FILTER ( dClasseMangueira, dClasseMangueira[Mês] = DATE ( 2026, 11, 1 ) && dClasseMangueira[Origem] <> "Plano" ) ),
    "Plano total", CALCULATE ( SUM ( dClasseMangueira[Plano] ), dClasseMangueira[Mês] = DATE ( 2026, 11, 1 ) )
)
```
2. Por C.Standard, Tipo e Arame (compare com `conferir.py --hoje <corte+1>`; a planilha usa 23 dias úteis, o modelo 22):
```
EVALUATE
SUMMARIZECOLUMNS (
    dClasseMangueira[C.Standard],
    "Plano", [HP Plano do Mês],
    "Produzido", [HP Produzido no Plano],
    "% do plano", [HP % do Plano],
    "Ritmo", [HP % Ritmo Esperado],
    "Atraso", [HP Atraso],
    "Para fechar", [HP Para Fechar por dia]
)
ORDER BY [Plano] DESC
```
3. Caixa do código: `EVALUATE ROW ( "ec215-06L", CALCULATE ( [HP Produzido no Plano], dClasseMangueira[Mangueira] = "ec215-06L" ) )` deve dar o mesmo valor que `SUMX` do `fProducaoSAP[Material] = "EC215-06L"`; se der vazio com produção no SAP, o `TREATAS` está diferenciando caixa e a `Chave` precisa ser igualada também no `fProducaoSAP` (avisar).
4. Total do SAP: `[HP Produzido]` sem filtro deve ser igual a `CALCULATE ( [SAP Produzido], dProdutoSAP[Produto] = "Mangueira" )`.
5. `INFO.COLUMNS()` e `INFO.MEASURES()` com `[State] <> 1` devem devolver 0 linhas.
6. Segmentação: trocar o mês muda o plano, o produzido, os cartões e todas as barras juntos; mês sem item na lista mostra "Plano de <mês> não cadastrado".

## 5) Onde mexer depois
- Plano do mês: **só na lista `GMS_PlanoMangueira`** (1 linha por mangueira e mês); vale no próximo refresh, sem republicar o relatório. Mangueira nova produzida antes de entrar na lista aparece como `Fora do plano`.
- Dias úteis: na `GMS_MetaMensal` (linha da Mangueira), como na Máscara SAP.
