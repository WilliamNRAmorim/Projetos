# Produção x meta (SAP) no modelo (GMS): script TMDL da página `pg_mascara_sap` (MEL-273) — PENDENTE DE APLICAR (só com o "Libero" do William, no TMDL view do modelo vivo)

Só BI. Leva a "Máscara de produção" (produção SAP x meta do mês, com carinhas) para o relatório oficial `GMS_Painel`, lendo **direto** os exports do SAP (`mb51.xlsx` e `coois.xlsx` em `.../2_Production_Planning/Relatórios/`), sem passar pela planilha. A página nova é `GMS_Painel.Report/definition/pages/pg_mascara_sap`; as três medidas SVG estão no `reportExtensions.json` do relatório. Conferência dos números: `GMS/PowerBI/Mascara_Producao/conferir_sap.py`.

## Antes de colar (ordem obrigatória)
1. **Crie a lista SharePoint `GMS_MetaMensal`** no site `OperationsGuaratingueta` (o chefe cria). Colunas pelo nome interno: `Title` (= Produto: Mangueira, Montagem ou Fittings), `Mes` (**só data**, dia 1 do mês), `MetaDiaria` (número), `DiasUteis` (número). 1 linha por produto e mês (nov/2026: 6600, 2517 e 800, 22 dias úteis). Sem a lista, o refresh da `dMetaMensal` falha; as outras tabelas atualizam normal (atualize tabela por tabela).
2. Credenciais: as duas fontes do `fProducaoSAP` são arquivos no SharePoint da Danfoss e a lista também. Em Configurações da fonte de dados, use **conta organizacional** e privacidade **Organizacional** nas três (o join mistura MB51 e COOIS; com privacidade diferente o Power Query bloqueia a mistura).
3. Cole os **3 passos abaixo, um de cada vez**, na ordem, botão **Apply** em cada um. Digite/cole **sem indentação à esquerda** além da estrutura e use `Escape` depois de cada linha digitada (seção 7 do `COMO_ARRUMAR_HORAHORA.md`): cada expressão (DAX e M) está toda em linhas no mesmo nível (4 tabs) de propósito.
4. Depois do passo 1, **atualize** `fProducaoSAP` (e `dMetaMensal` quando a lista existir). Medidas só calculam depois do refresh.
5. Se já existir objeto com esses nomes no modelo vivo, o `createOrReplace` o substitui. Confira antes: `EVALUATE INFO.TABLES()` não deve listar `fProducaoSAP`, `dProdutoSAP` nem `dMetaMensal`; e `EVALUATE INFO.MEASURES()` não deve ter nome começando por `SAP ` nem `_SAP `.
6. O Desktop sobrescreve o que mudou nos arquivos: **reabra o projeto** (`GMS_Painel.pbip`) depois de aplicar no modelo e antes de publicar; a página só abre sem erro depois que as medidas existem.

## Decisões do script (para o revisor)
- **Nomes das medidas** levam o prefixo `SAP ` (pasta de exibição `Máscara SAP`) porque `Dias Restantes` já existe no modelo (`ficha_producao`, pasta "05 Hose Plan\Ritmo") e o nome de medida é único no modelo inteiro. Auxiliares ocultas começam com `_`. A medida `Feliz` da Máscara não foi levada (nenhum visual a usa).
- **Mês da página.** Vem da segmentação de mês (dCalendario). Se não houver **um único** mês selecionado, vale o mês de ontem (BR). **Corte** = maior `Data` da `fProducaoSAP` (todos os produtos) menor ou igual a MIN(último dia do mês escolhido, ontem), e vazio se cair antes do dia 1 do mês (mês sem dado). **Dias contabilizados** = datas distintas da `fProducaoSAP` (ignora produto e material) no mês, até o corte. Meta diária e dias úteis vêm da `dMetaMensal` (mês + produto do contexto).
- **Mês fechado.** `SAP Ritmo para Fechar` fica vazio e o cartão diz "Mês fechado" quando `Dias Restantes <= 0` **ou** o último dia do mês já passou (`_SAP Mês Encerrado`). A segunda condição é acréscimo meu: sem ela, um mês passado com menos dias de movimento que dias úteis mostraria um "ritmo" sem sentido. O rótulo "Meta até ontem" vira "Meta até dd/mm" quando o corte não é ontem.
- **`SAP Hoje (BR)`** usa `UTCNOW() - 3/24`: exceção declarada à B.4.1 (a âncora de "hoje" por dado não serve porque o corte é "ontem" de calendário). Igual à Máscara aprovada.
- **Relacionamentos** (muitos-para-um, sentido único): `fProducaoSAP[Data]` → `dCalendario[Date]`, `fProducaoSAP[Produto]` → `dProdutoSAP[Produto]`, `dMetaMensal[Produto]` → `dProdutoSAP[Produto]`. Nenhum bidirecional. Dados anteriores a 2025 (a MB51 vai até 2024) ficam sem linha na `dCalendario`; as medidas filtram por data da própria fato, então não afeta.
- **Coluna nova em `dCalendario`**: `Mês e Ano` (texto "nov/2026", ordenada por `AnoMês`) para a segmentação mostrar mês legível em vez de 202611. As medidas usam `AnoMês` (um valor = um mês). Se o editor recusar o passo 2, a página abre com a segmentação sem campo: troque o campo dela para `dCalendario[AnoMês]` no Desktop (mostra 202611).
- **Linhas de total do SAP.** O export termina com linhas de total (KG, M, PC, TS; a de M dobraria os metros). O M faz `RemoveLastN(3)` **antes** do filtro de Material vazio (a Máscara faz depois, o que tira 3 linhas reais dos lançamentos mais antigos, de 2024) e o filtro de Material vazio tira as restantes. Para o mês corrente o resultado é igual ao da Máscara.
- **Order repetida na COOIS** duplica a linha da MB51 no join (a Máscara faz igual; mantido). Na COOIS de 29/10 há 0 Orders repetidas (`conferir_sap.py` mede).

## Medidas
| Medida | Formato | O que é |
|---|---|---|
| `SAP Hoje (BR)` | dd/mm/yyyy | Hoje no Brasil (UTC-3), só a data. Única medida que consulta o relógio (exceção declarada à B.4.1: o corte é "ontem" real). Âncora do mês padrão e do corte. |
| `_SAP Mês` | oculta, dd/mm/yyyy | Primeiro dia do mês da página: o mês único selecionado em dCalendario; sem seleção única, o mês de ontem (BR). |
| `_SAP Mês Encerrado` | oculta, texto | Verdadeiro quando o último dia do mês da página já passou (mês fechado: sem ritmo para fechar). |
| `SAP Data de Corte` | dd/mm/yyyy | Maior data da fProducaoSAP (todos os produtos) até o menor entre o fim do mês da página e ontem; vazio se não houver dado no mês. |
| `SAP Dias Contabilizados` | 0 | Datas distintas da fProducaoSAP (todos os produtos, ignora produto e material) no mês da página, até o corte. Automático (a planilha digita). |
| `SAP Meta Diária` | #,0 | Meta diária do produto no contexto, no mês da página (lista GMS_MetaMensal); vazio se mais de um produto. |
| `SAP Dias Úteis` | 0 | Dias úteis do mês da página (lista GMS_MetaMensal; no contexto sem produto, o maior entre os produtos). |
| `SAP Produzido` | #,0.0 | Soma da quantidade do produto no mês da página, até o corte (todos os tipos de movimento, como a Máscara: 101 entra, 102 estorna). |
| `SAP Meta Acumulada` | #,0 | Meta diária x dias contabilizados. |
| `SAP Saldo` | +#,0.0;-#,0.0;0.0 | Produzido menos meta acumulada (negativo = atrasado). |
| `SAP % da Meta` | 0.0% | Produzido sobre meta acumulada. |
| `SAP Dias Restantes` | 0 | Dias úteis menos dias contabilizados (mês fechado pode dar 0 ou negativo). |
| `SAP Ritmo para Fechar` | #,0.0 | Quanto por dia falta produzir nos dias restantes para fechar a meta do mês; vazio se não há dias restantes ou o mês já fechou. |

## 1) Passo 1: tabelas e relacionamentos (cole inteiro, depois Apply e refresh)
```
createOrReplace

	table dProdutoSAP

		/// Produtos da página Produção x meta (SAP): unidade, casas decimais e ordem de exibição. Chave dos relacionamentos com fProducaoSAP e dMetaMensal.
		column Produto
			dataType: string
			summarizeBy: none
			sortByColumn: Ordem
			sourceColumn: [Produto]

		column Unidade
			dataType: string
			isHidden
			summarizeBy: none
			sourceColumn: [Unidade]

		column Casas
			dataType: int64
			isHidden
			formatString: 0
			summarizeBy: none
			sourceColumn: [Casas]

		column Ordem
			dataType: int64
			isHidden
			formatString: 0
			summarizeBy: none
			sourceColumn: [Ordem]

		partition dProdutoSAP = calculated
			mode: import
			source =
				DATATABLE (
				"Produto", STRING,
				"Unidade", STRING,
				"Casas", INTEGER,
				"Ordem", INTEGER,
				{
				{ "Mangueira", "m", 1, 1 },
				{ "Montagem", "pç", 0, 2 },
				{ "Fittings", "pç", 0, 3 }
				}
				)

	table fProducaoSAP

		/// Produção diária por produto, material, tipo de movimento e unidade. Fonte: MB51 + COOIS do SAP (SharePoint), sem KG. Mesma regra da Máscara de produção.
		column Data
			dataType: dateTime
			isHidden
			formatString: dd/mm/yyyy
			summarizeBy: none
			sourceColumn: Data

		column Produto
			dataType: string
			isHidden
			summarizeBy: none
			sourceColumn: Produto

		column Material
			dataType: string
			isHidden
			summarizeBy: none
			sourceColumn: Material

		column 'Tipo de movimento'
			dataType: int64
			isHidden
			formatString: 0
			summarizeBy: none
			sourceColumn: Tipo de movimento

		column Unidade
			dataType: string
			isHidden
			summarizeBy: none
			sourceColumn: Unidade

		column Quantidade
			dataType: double
			isHidden
			formatString: #,0.00
			summarizeBy: none
			sourceColumn: Quantidade

		partition fProducaoSAP = m
			mode: import
			source =
				let
				// Fonte: exports do SAP lidos direto do SharePoint (mesma origem e mesma transformação da planilha Máscara de produção, MEL-273).
				// Grão: MB51 = 1 linha por item de documento de material; COOIS = 1 linha por Order. Join esperado N:1 (MB51 x COOIS) por Order.
				// Se a COOIS repetir uma Order, o join duplica a linha da MB51 (a Máscara faz igual): GMS/PowerBI/Mascara_Producao/conferir_sap.py mede.
				OrigemCoois = Excel.Workbook(Web.Contents("https://danfoss.sharepoint.com/sites/OperationsGuaratingueta/Shared%20Documents/Manufatura/Production%20planning/2_Production_Planning/Relat%C3%B3rios/coois.xlsx"), null, true),
				DadosCoois = OrigemCoois{0}[Data],
				CabCoois = Table.PromoteHeaders(DadosCoois, [PromoteAllScalars = true]),
				ColCoois = Table.SelectColumns(CabCoois, {"Order", "MRP controller"}),
				TiposCoois = Table.TransformColumnTypes(ColCoois, {{"Order", Int64.Type}, {"MRP controller", type text}}),
				OrigemMb51 = Excel.Workbook(Web.Contents("https://danfoss.sharepoint.com/sites/OperationsGuaratingueta/Shared%20Documents/Manufatura/Production%20planning/2_Production_Planning/Relat%C3%B3rios/mb51.xlsx"), null, true),
				DadosMb51 = OrigemMb51{0}[Data],
				CabMb51 = Table.PromoteHeaders(DadosMb51, [PromoteAllScalars = true]),
				Renomeado = Table.RenameColumns(CabMb51, {{"Storage Location", "Storage location"}, {"Movement Type", "Movement type"}}, MissingField.Ignore),
				// O SAP termina o export com linhas de total (KG, M, PC, TS). RemoveLastN(3) como na Máscara; as que sobrarem (Material vazio) saem no filtro abaixo.
				// A linha de total em unidade M dobraria os metros se ficasse.
				SemTotais = Table.RemoveLastN(Renomeado, 3),
				Colunas = Table.SelectColumns(SemTotais, {"Material", "Order", "Movement type", "Posting Date", "Qty in unit of entry", "Unit of Entry"}),
				Tipos = Table.TransformColumnTypes(Colunas, {{"Material", type text}, {"Order", Int64.Type}, {"Movement type", Int64.Type}, {"Posting Date", type date}, {"Qty in unit of entry", type number}, {"Unit of Entry", type text}}),
				SoMaterial = Table.SelectRows(Tipos, each [Material] <> null and Text.Trim([Material]) <> "" and not Text.StartsWith(Text.Upper(Text.Trim([Material])), "FM")),
				Unido = Table.NestedJoin(SoMaterial, {"Order"}, TiposCoois, {"Order"}, "COOIS", JoinKind.LeftOuter),
				Expandido = Table.ExpandTableColumn(Unido, "COOIS", {"MRP controller"}, {"MRP controller"}),
				SemKg = Table.SelectRows(Expandido, each [Unit of Entry] <> "KG"),
				ComProduto = Table.AddColumn(SemKg, "Produto", each let m = Text.Trim(Text.From([MRP controller] ?? "")) in if m = "AIH" then "Mangueira" else if m = "Z35" or m = "AWE" then "Montagem" else if m = "AO0" then "Fittings" else null, type text),
				SoProduto = Table.SelectRows(ComProduto, each [Produto] <> null and [Posting Date] <> null),
				Agrupado = Table.Group(SoProduto, {"Posting Date", "Produto", "Material", "Movement type", "Unit of Entry"}, {{"Quantidade", each List.Sum([Qty in unit of entry]), type nullable number}}),
				Nomes = Table.RenameColumns(Agrupado, {{"Posting Date", "Data"}, {"Movement type", "Tipo de movimento"}, {"Unit of Entry", "Unidade"}}),
				Final = Table.ReorderColumns(Nomes, {"Data", "Produto", "Material", "Tipo de movimento", "Unidade", "Quantidade"})
				in
				Final

	table dMetaMensal

		/// Meta diária e dias úteis por produto e mês, da lista SharePoint GMS_MetaMensal (preenchida pelo planejamento).
		column Produto
			dataType: string
			isHidden
			summarizeBy: none
			sourceColumn: Produto

		column Mês
			dataType: dateTime
			isHidden
			formatString: mmm/yyyy
			summarizeBy: none
			sourceColumn: Mês

		column 'Meta diária'
			dataType: double
			isHidden
			formatString: #,0
			summarizeBy: none
			sourceColumn: Meta diária

		column 'Dias úteis'
			dataType: int64
			isHidden
			formatString: 0
			summarizeBy: none
			sourceColumn: Dias úteis

		partition dMetaMensal = m
			mode: import
			source =
				let
				// Lista nova GMS_MetaMensal (nomes internos: Title = Produto, Mes = dia 1 do mês, MetaDiaria, DiasUteis). Grão: 1 linha por Produto x Mês.
				// Navega pelo Title da lista porque ainda não há Id; lista criada em 16/11/2026, Id a51e5bf5-4f06-473d-9a6a-2b1d0c4e9f9b (pode trocar a navegação por [Id = "a51e5bf5-4f06-473d-9a6a-2b1d0c4e9f9b"]).
				Origem = SharePoint.Tables("https://danfoss.sharepoint.com/sites/OperationsGuaratingueta", [Implementation = "2.0", ViewMode = "All"]),
				Lista = Origem{[Title = "GMS_MetaMensal"]}[Items],
				Colunas = Table.SelectColumns(Lista, {"Title", "Mes", "MetaDiaria", "DiasUteis"}),
				Tipos = Table.TransformColumnTypes(Colunas, {{"MetaDiaria", type number}, {"DiasUteis", Int64.Type}}),
				Normalizado = Table.TransformColumns(Tipos, {{"Mes", each Date.StartOfMonth(Date.From(_)), type date}, {"Title", each Text.Proper(Text.Trim(_)), type text}}),
				SoLinhas = Table.SelectRows(Normalizado, each [Mes] <> null and [Title] <> null and [Title] <> ""),
				Nomes = Table.RenameColumns(SoLinhas, {{"Title", "Produto"}, {"Mes", "Mês"}, {"MetaDiaria", "Meta diária"}, {"DiasUteis", "Dias úteis"}}),
				Final = Table.ReorderColumns(Nomes, {"Produto", "Mês", "Meta diária", "Dias úteis"})
				in
				Final

	relationship fProducaoSAP_dCalendario
		fromColumn: fProducaoSAP.Data
		toColumn: dCalendario.Date

	relationship fProducaoSAP_dProdutoSAP
		fromColumn: fProducaoSAP.Produto
		toColumn: dProdutoSAP.Produto

	relationship dMetaMensal_dProdutoSAP
		fromColumn: dMetaMensal.Produto
		toColumn: dProdutoSAP.Produto
```

## 2) Passo 2: coluna `Mês e Ano` na `dCalendario`
```
createOrReplace

	ref table dCalendario

		/// Mês e ano para a segmentação da página Produção x meta (SAP); ordena pelo AnoMês.
		column 'Mês e Ano' =
				FORMAT ( [Date], "mmm/yyyy", "pt-BR" )
			dataType: string
			sortByColumn: AnoMês
			summarizeBy: none
```

## 3) Passo 3: medidas (depois do refresh)
```
createOrReplace

	ref table Medidas

		measure 'SAP Hoje (BR)' =
				-- Hoje no Brasil (UTC-3), só a data. Única medida que consulta o relógio (exceção declarada à B.4.1: o corte é "ontem" real). Âncora do mês padrão e do corte. · MEL-273
				VAR __Agora = UTCNOW () - 3 / 24
				RETURN
				DATE ( YEAR ( __Agora ), MONTH ( __Agora ), DAY ( __Agora ) )
			formatString: dd/mm/yyyy
			displayFolder: Máscara SAP

		measure '_SAP Mês' =
				-- Primeiro dia do mês da página: o mês único selecionado em dCalendario; sem seleção única, o mês de ontem (BR). · MEL-273
				VAR __Meses = VALUES ( dCalendario[AnoMês] )
				VAR __Ontem = [SAP Hoje (BR)] - 1
				RETURN
				IF (
				COUNTROWS ( __Meses ) = 1,
				DATE ( INT ( MAX ( dCalendario[AnoMês] ) / 100 ), MOD ( MAX ( dCalendario[AnoMês] ), 100 ), 1 ),
				DATE ( YEAR ( __Ontem ), MONTH ( __Ontem ), 1 )
				)
			formatString: dd/mm/yyyy
			displayFolder: Máscara SAP
			isHidden

		measure '_SAP Mês Encerrado' =
				-- Verdadeiro quando o último dia do mês da página já passou (mês fechado: sem ritmo para fechar). · MEL-273
				EOMONTH ( [_SAP Mês], 0 ) < [SAP Hoje (BR)]
			displayFolder: Máscara SAP
			isHidden

		measure 'SAP Data de Corte' =
				-- Maior data da fProducaoSAP (todos os produtos) até o menor entre o fim do mês da página e ontem; vazio se não houver dado no mês. · MEL-273
				VAR __Ini = [_SAP Mês]
				VAR __Fim = MIN ( EOMONTH ( __Ini, 0 ), [SAP Hoje (BR)] - 1 )
				VAR __Corte = CALCULATE ( MAX ( fProducaoSAP[Data] ), REMOVEFILTERS (), fProducaoSAP[Data] <= __Fim )
				RETURN
				IF ( __Corte >= __Ini, __Corte )
			formatString: dd/mm/yyyy
			displayFolder: Máscara SAP

		measure 'SAP Dias Contabilizados' =
				-- Datas distintas da fProducaoSAP (todos os produtos, ignora produto e material) no mês da página, até o corte. Automático (a planilha digita). · MEL-273
				VAR __Ini = [_SAP Mês]
				VAR __Corte = [SAP Data de Corte]
				RETURN
				IF (
				NOT ISBLANK ( __Corte ),
				CALCULATE ( DISTINCTCOUNT ( fProducaoSAP[Data] ), REMOVEFILTERS (), fProducaoSAP[Data] >= __Ini, fProducaoSAP[Data] <= __Corte )
				)
			formatString: 0
			displayFolder: Máscara SAP

		measure 'SAP Meta Diária' =
				-- Meta diária do produto no contexto, no mês da página (lista GMS_MetaMensal); vazio se mais de um produto. · MEL-273
				VAR __Mes = [_SAP Mês]
				RETURN
				IF ( HASONEVALUE ( dProdutoSAP[Produto] ), CALCULATE ( MAX ( dMetaMensal[Meta diária] ), dMetaMensal[Mês] = __Mes ) )
			formatString: #,0
			displayFolder: Máscara SAP

		measure 'SAP Dias Úteis' =
				-- Dias úteis do mês da página (lista GMS_MetaMensal; no contexto sem produto, o maior entre os produtos). · MEL-273
				VAR __Mes = [_SAP Mês]
				RETURN
				CALCULATE ( MAX ( dMetaMensal[Dias úteis] ), dMetaMensal[Mês] = __Mes )
			formatString: 0
			displayFolder: Máscara SAP

		measure 'SAP Produzido' =
				-- Soma da quantidade do produto no mês da página, até o corte (todos os tipos de movimento, como a Máscara: 101 entra, 102 estorna). · MEL-273
				VAR __Ini = [_SAP Mês]
				VAR __Corte = [SAP Data de Corte]
				RETURN
				IF (
				NOT ISBLANK ( __Corte ),
				CALCULATE ( SUM ( fProducaoSAP[Quantidade] ), REMOVEFILTERS ( dCalendario ), fProducaoSAP[Data] >= __Ini, fProducaoSAP[Data] <= __Corte )
				)
			formatString: #,0.0
			displayFolder: Máscara SAP

		measure 'SAP Meta Acumulada' =
				-- Meta diária x dias contabilizados. · MEL-273
				[SAP Meta Diária] * [SAP Dias Contabilizados]
			formatString: #,0
			displayFolder: Máscara SAP

		measure 'SAP Saldo' =
				-- Produzido menos meta acumulada (negativo = atrasado). · MEL-273
				VAR __Meta = [SAP Meta Acumulada]
				RETURN
				IF ( NOT ISBLANK ( __Meta ), [SAP Produzido] - __Meta )
			formatString: +#,0.0;-#,0.0;0.0
			displayFolder: Máscara SAP

		measure 'SAP % da Meta' =
				-- Produzido sobre meta acumulada. · MEL-273
				DIVIDE ( [SAP Produzido], [SAP Meta Acumulada] )
			formatString: 0.0%
			displayFolder: Máscara SAP

		measure 'SAP Dias Restantes' =
				-- Dias úteis menos dias contabilizados (mês fechado pode dar 0 ou negativo). · MEL-273
				[SAP Dias Úteis] - [SAP Dias Contabilizados]
			formatString: 0
			displayFolder: Máscara SAP

		measure 'SAP Ritmo para Fechar' =
				-- Quanto por dia falta produzir nos dias restantes para fechar a meta do mês; vazio se não há dias restantes ou o mês já fechou. · MEL-273
				VAR __Rest = [SAP Dias Restantes]
				RETURN
				IF (
				__Rest > 0 && NOT [_SAP Mês Encerrado],
				DIVIDE ( [SAP Meta Diária] * [SAP Dias Úteis] - [SAP Produzido], __Rest )
				)
			formatString: #,0.0
			displayFolder: Máscara SAP
```

## 4) Verificação depois do refresh (DAX query view)
1. Lado do modelo: o corte, os dias e o produzido por produto (esperado hoje = 13/11/2026 e metas 6600/2517/800, 22 dias úteis: Mangueira 57.389,37 m, Montagem 21.040 pç, Fittings 10.186 pç, 9 dias contabilizados, corte 12/11; `Hoje` real vai mudar o corte, compare com `conferir_sap.py --mascara --hoje AAAA-MM-DD`):
```
EVALUATE
SUMMARIZECOLUMNS (
    dProdutoSAP[Produto],
    "Corte", [SAP Data de Corte],
    "Dias", [SAP Dias Contabilizados],
    "Produzido", [SAP Produzido],
    "Meta acumulada", [SAP Meta Acumulada],
    "Saldo", [SAP Saldo],
    "% da meta", [SAP % da Meta],
    "Ritmo", [SAP Ritmo para Fechar]
)
ORDER BY dProdutoSAP[Produto]
```
2. Sem linha de total no fato (a de M dobraria): `EVALUATE ROW ( "Maior dia", MAX ( fProducaoSAP[Data] ), "Linhas sem produto", COUNTROWS ( FILTER ( fProducaoSAP, ISBLANK ( fProducaoSAP[Produto] ) ) ) )` deve dar 0 linhas sem produto e maior dia = último movimento da MB51.
3. Join duplicado: compare `SUM ( fProducaoSAP[Quantidade] )` de um mês fechado com a mesma conta na Máscara (aba `mb51_coois`). Se divergir para cima, a COOIS tem Order repetida.
4. `INFO.COLUMNS()` e `INFO.MEASURES()` com `[State] <> 1` devem devolver 0 linhas.
5. Segmentação: nenhum mês selecionado mostra o mês de ontem; escolher outro mês muda o título, os três cartões e as três barras juntos.

## 5) Onde mexer depois
- Meta ou dias úteis do mês: **só na lista `GMS_MetaMensal`** (1 linha por produto e mês), sem republicar o relatório; vale no próximo refresh.
- Trocar `[Title = "GMS_MetaMensal"]` por `[Id = "..."]` na `dMetaMensal` quando a lista existir (mais estável contra renomeação).
