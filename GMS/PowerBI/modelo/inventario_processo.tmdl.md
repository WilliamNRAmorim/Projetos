# Inventário de material em processo no modelo (GMS): script TMDL da página de inventário (MEL-278) - NÃO APLICADO (escrito em 27/11/2026, para colar no TMDL view do modelo vivo só com o "sim" do William)

Só BI. Cria a base do inventário de material em processo (WIP em metros e insumo em kg e m) para todas as fichas abertas da `ficha_producao`: situação pela etapa atual, metros da última etapa fechada, insumo = BOM por metro × metros. Regra e protótipo: `GMS/Analises/Inventario_Processo/gerar_inventario_processo.py` e `inventario_template.html`. As medidas SVG da página ficam fora deste script (vão no `reportExtensions.json` depois). **Depende** da lista SharePoint `GMS_BOM_Mangueira` (300 linhas, mesma origem da BOM do protótipo, `bom_mangueira_sap.csv`) e das tabelas `ficha_producao` e `RegistrosInspeção`.

## Antes de colar (ordem obrigatória)
1. **Lista `GMS_BOM_Mangueira`** (site `OperationsGuaratingueta`, o mesmo da `GMS_PlanoMangueira`). Colunas pelo nome interno: `Title` (= Mangueira), `Material`, `Camada` (tubo, trama, cobertura, bandagem), `PartNumber`, `Descricao`, `BOM_por_metro` (número), `Unidade` (kg ou m), `Fonte`, `OPs`, `Dispersao`. Se algum nome interno diferir, o M devolve a coluna vazia (`MissingField.UseNull`) e a linha some por falta de `PartNumber`: confira a verificação 6.
2. Credencial da lista: a mesma conta organizacional da `dMetaMensal` e da `dPlanoMangueira` (privacidade Organizacional).
3. **Confira os valores reais de etapa e status** antes de colar (o DAX compara com acento): 
```
EVALUATE
SUMMARIZECOLUMNS (
    ficha_producao[processo],
    ficha_producao[status_processo],
    "Fichas", COUNTROWS ( ficha_producao )
)
ORDER BY ficha_producao[processo], ficha_producao[status_processo]
```
   Esperado: `Trançadeira`, `Cobertura`, `Bandagem`, `Vulcanização`, `Debandagem`, `Extr./Teste` (entram) e `Mandril`, `Tubo` (ficam fora). Status `Aguardando` e `Em processo` entram. Se algum texto vier diferente, pare e avise.
4. **Conferir nomes livres** (as duas consultas devem voltar com 0 linhas):
```
EVALUATE
FILTER ( INFO.TABLES (), [Name] IN { "dBOMMangueira", "fInventarioOP", "fInventarioInsumo" } )
```
```
EVALUATE
FILTER ( INFO.MEASURES (), LEFT ( [Name], 3 ) = "IP " || LEFT ( [Name], 4 ) = "_IP " )
```
   E, por precaução, `EVALUATE FILTER ( INFO.COLUMNS (), [ExplicitName] IN { "Metros Suspeito", "Dias Parada" } )` só pode listar colunas das tabelas novas.
5. Cole os **4 passos abaixo, um de cada vez**, na ordem, **Apply** em cada um (regras de digitação do `plano_mangueira.tmdl.md`: sem indentação extra, `Escape` depois de cada linha). Depois do passo 1 **atualize `dBOMMangueira`**; depois dos passos 2 e 3 **atualize o modelo** (são tabelas calculadas e só enchem no refresh; se falhar por ordem de cálculo, rode o refresh de novo). O passo 4 só depois do refresh.
6. **Reabra o projeto** (`GMS_Painel.pbip`) depois de aplicar no modelo e antes de publicar a página.

## Decisões do script (para o revisor)
- **Revisão (27/11/2026, chefe Opus 5.5, por escolha do William: revisor fora da sessão):** aprovado. Conferido no snapshot: `ficha_producao[ID]` int64, `[OP]` double e `RegistrosInspeção[OP_ID]` double (a comparação não mistura texto e número); `RegistrosInspeção[Quantidade]` existe; nomes internos da lista conferidos na criação (Title, Material, Camada, PartNumber, Descricao, BOM_por_metro, Unidade, Fonte); `OP_ID` = número da OP conferido na lista viva (OP 30974903: 5 lances, 377,1 m). Medidas no mesmo padrão `createOrReplace` + `ref table Medidas` dos scripts já aplicados. Dias Parada vazio conta como dentro do limite (blank <= 15 é verdadeiro no DAX), como decidido.
- **Grão: 1 linha por registro da ficha (coluna `ID`), não por OP** (correção da revisão). A ficha pode ter registro filho com a mesma OP (divisão de carretel com sobra, C38 do Mestre). `OP` é atributo; "OPs" é `DISTINCTCOUNT` de `OP`; metros e insumo somam por registro. Registro sem OP vira `(sem OP)`.
- **Quem entra:** `status_processo` = `Aguardando` ou `Em processo` e `processo` em Trançadeira, Cobertura, Bandagem, Vulcanização, Debandagem, Extr./Teste. Mandril e Tubo ficam fora (ainda não há mangueira para contar). Igual ao protótipo, entra também registro com mangueira vazia ou digitada errada (ex. `0`, `1`): vira `vazio (inválida)` ou `<texto> (inválida)`, sem BOM, e aparece na lista de mangueiras sem BOM. O código SAP digitado no lugar do nome (alias do `aliases_mangueira.csv`) **não** é resolvido aqui: cai em "sem BOM" (pendência).
- **Situação e metros:** regra do prompt (Trançadeira→Tubo interno; Cobertura→Trançada / Espiralada; Bandagem→Coberta; Vulcanização, Debandagem e Extr./Teste→Bandada; metros da última etapa fechada com fallback, primeiro valor > 0, senão 0).
- **Cabine (Extr./Teste em Em processo):** `quantidade_extracao` só é preenchida no fim, então os lances já testados ainda contam nos metros base. `Metros` = metros base − soma de `RegistrosInspeção[Quantidade]` com `OP_ID` = OP, mínimo 0. Se a OP tem mais de um registro aberto na Cabine, o desconto vai **só no registro de maior ID** (os outros ficam sem desconto: limitação, pode superestimar). Se a inspeção passar dos metros do registro, o excesso não é levado a outro registro. `Aguardando` na Cabine não desconta. Premissa: `OP_ID` da inspeção é o número da OP (ver verificação 8). `Metros Base` e `Metros Inspecionados` ficam como colunas ocultas para auditar.
- **Metros suspeito:** coluna `Metros Suspeito` = `Metros` > 1,5 × `quantidade_tubo` (só se o tubo > 0). Não tira da conta; a página sinaliza na tabela (ex. real: OP 31003282, tubo 250 e trançagem 500).
- **Dias Parada** = agora BR − maior `data_hora_final_<etapa>` (mandril, tubo, trancadeira, cobertura, bandagem, vulcanizacao, debandagem, como o protótipo). **Fuso:** o padrão do modelo para "agora" é `UTCNOW () - 3 / 24` (Máscara SAP, `SAP Hoje (BR)`; carimbo do `dAtualizacao`), e as datas da `ficha_producao` já são lidas como horário da fábrica (a `fFluxoBase` calcula o dia produtivo das 05:20 direto delas). Uso as duas premissas; a verificação 7 prova (a maior data da ficha não pode passar de agora).
- **Limite de dias:** `_IP Limite Dias` = 15 (constante numa medida oculta, é o único lugar para trocar). OP com `Dias Parada` > limite sai dos totais (armadilha da OP zumbi, K04/K09 do Mestre BI) e aparece em `IP OPs Paradas`. Registro sem nenhuma data final (`Dias Parada` vazio) **fica** na conta (não dá para provar que é zumbi). Dias é calculado no refresh, não é `Now()` em medida (B.4.1).
- **Mangueira sem BOM** sai dos totais (`IP OPs na Conta`, `IP Metros`, insumo) e tem medidas próprias (`IP OPs sem BOM`, `IP Metros sem BOM`, `IP Mangueiras sem BOM`) para o aviso da página. Zumbi sem BOM também sai.
- **Casamento mangueira x BOM:** chave normalizada = maiúsculas, sem espaços, `-0` seguido de dígito vira `-` (FC598-08 → FC598-8; `-00` colapsa para `-0`, como o `re.sub` do protótipo). Lado da ficha: `ficha_producao[Mangueira_Limpa]` (já maiúscula, sem espaço nas pontas e sem zero à esquerda) normalizada em DAX; lado da BOM: o `Title` normalizado em M **com os mesmos passos e a mesma ordem**. Verificação 6 prova que nenhuma chave guarda `-0<dígito>`.
- **BOM:** `dBOMMangueira` (M, oculta) lê a lista, normaliza a chave, põe `Ordem da Camada` (tubo 1, trama 2, cobertura 3, bandagem 4, outro 99 = nunca entra) e mantém **1 linha por Chave + PartNumber** (a primeira da lista, `Table.Distinct`). Linha sem `PartNumber`, sem `Title` ou sem `BOM_por_metro` é descartada. `BOM_por_metro` vem do requisito da OP no SAP e **inclui o fator de perda do componente** (ex. fita 1,022 m/m), coerente com o que o SAP baixa; por isso o insumo não é "teórico puro".
- **Insumo de uma linha** = `BOM_por_metro × Metros`, só das linhas da BOM com `Ordem da Camada` ≤ `Ordem da Situação` (Tubo interno = tubo; Trançada = tubo, trama; Coberta = + cobertura; Bandada = as 4). kg e m em medidas separadas pela coluna `Unidade`.
- **Tabelas calculadas, não M.** `fInventarioOP` e `fInventarioInsumo` são calculadas porque as duas leem tabelas que o modelo já carrega (`ficha_producao`, `dBOMMangueira`, `RegistrosInspeção`): não leem a lista da ficha de novo (a lista é grande), não pedem merge entre consultas (Formula.Firewall e privacidade) e recalculam sozinhas em todo refresh depois das fontes. `UTCNOW ()` dentro da tabela é o momento do refresh, o equivalente do `puxado_em` do protótipo. Custo: poucas centenas de linhas. Contra: `Dias Parada` fica congelado entre refreshes (aceito: a ficha também só muda no refresh). Como são calculadas, a primeira vez só têm valor depois do refresh.
- **Sem relacionamento novo.** `fInventarioOP` e `fInventarioInsumo` não se relacionam. As medidas de insumo repassam o filtro da `fInventarioOP` (situação, OP, mangueira) para a `fInventarioInsumo` com `TREATAS ( VALUES ( fInventarioOP[ID] ), fInventarioInsumo[ID] )`, só quando a `fInventarioOP` está filtrada (`ISCROSSFILTERED`). Assim o cartão de uma situação (filtro de visual em `fInventarioOP[Situação]`) mostra metros, OPs e kg juntos. A `fInventarioInsumo` leva `Dias Parada` e `Situação` próprios para as barras por PartNumber. Se o revisor preferir, um relacionamento 1:N `fInventarioOP[ID]` para `fInventarioInsumo[ID]` (filtro numa direção só) faria o mesmo mais simples.
- **Não é comparável 1:1 com K04.** K04 (WIP em Processo) conta Início sem Fim por etapa em `fEtapaOP`; aqui a etapa vem de `processo` e `status_processo` da ficha e a unidade é metro/kg, não OP por etapa. Os números não precisam bater.
- **Nomes:** medidas visíveis `IP ...` e ocultas `_IP ...`, pasta `Inventário Processo`, na tabela `Medidas`. Comentário `--` na 1ª linha com o MEL-278.

## Medidas
| Medida | Formato | O que é |
|---|---|---|
| `IP OPs na Conta` | #,0 | OPs distintas com BOM e dias parada dentro do limite, no contexto. |
| `IP Metros` | #,0 | Metros dos registros na conta (com BOM, dentro do limite). |
| `IP Insumo kg` | #,0.0 | Insumo em kg (BOM × metros, camadas da situação), na conta. |
| `IP Insumo m` | #,0.0 | Insumo em metros (fita e filme), na conta. |
| `IP OPs sem BOM` | #,0 | OPs distintas sem BOM, dentro do limite (aviso da página). |
| `IP Metros sem BOM` | #,0 | Metros dessas OPs. |
| `IP Mangueiras sem BOM` | #,0 | Mangueiras distintas sem BOM. |
| `IP OPs Paradas` | #,0 | OPs distintas com dias parada acima do limite (fora dos totais). |
| `IP Metros Paradas` | #,0 | Metros dessas OPs. |
| `IP Registros Metros Suspeito` | #,0 | Registros na conta com `Metros Suspeito`. |
| `IP Metros Descontados Cabine` | #,0.0 | Metros inspecionados descontados na Cabine, na conta. |
| `IP Dias Parada` | 0.0 | Maior `Dias Parada` no contexto (por OP, na tabela). |
| `IP Na Conta` | 0 | 1 se a OP do contexto está na conta, 0 se não (filtro de visual). |
| `IP Motivo Fora` | texto | "Sem BOM" ou "Parada > N dias" (vazio se está na conta). |
| `IP Alerta Metros` | texto | "Conferir metros" se há registro com `Metros Suspeito`. |
| `_IP Limite Dias` | 0 | Oculta: limite de dias parada (15). |

## 1) Passo 1: tabela `dBOMMangueira` (cole inteiro, depois Apply e atualize a tabela)
```
createOrReplace

	table dBOMMangueira

		isHidden

		/// Espelho da lista SharePoint GMS_BOM_Mangueira (BOM por metro de cada mangueira, requisito da OP no SAP, com fator de perda): 1 linha por Chave + PartNumber. Chave = nome da mangueira normalizado (maiúsculas, sem espaço, -0N vira -N). MEL-278.
		column Chave
			dataType: string
			isHidden
			summarizeBy: none
			sourceColumn: Chave

		column Mangueira
			dataType: string
			isHidden
			summarizeBy: none
			sourceColumn: Mangueira

		column Material
			dataType: string
			isHidden
			summarizeBy: none
			sourceColumn: Material

		column Camada
			dataType: string
			isHidden
			summarizeBy: none
			sourceColumn: Camada

		column 'Ordem da Camada'
			dataType: int64
			isHidden
			formatString: 0
			summarizeBy: none
			sourceColumn: Ordem da Camada

		column PartNumber
			dataType: string
			isHidden
			summarizeBy: none
			sourceColumn: PartNumber

		column Descricao
			dataType: string
			isHidden
			summarizeBy: none
			sourceColumn: Descricao

		column BOM_por_metro
			dataType: double
			isHidden
			formatString: #,0.000000
			summarizeBy: none
			sourceColumn: BOM_por_metro

		column Unidade
			dataType: string
			isHidden
			summarizeBy: none
			sourceColumn: Unidade

		column Fonte
			dataType: string
			isHidden
			summarizeBy: none
			sourceColumn: Fonte

		partition dBOMMangueira = m
			mode: import
			source =
				let
				// Lista SharePoint GMS_BOM_Mangueira (site OperationsGuaratingueta, mesmo da GMS_PlanoMangueira). Nomes internos: Title = Mangueira, Material, Camada, PartNumber, Descricao, BOM_por_metro, Unidade, Fonte. Navega pelo Title como a dPlanoMangueira.
				// Chave: maiúsculas, sem espaço, "-00" colapsa para "-0" (3 passadas) e depois "-0N" vira "-N" (N de 1 a 9). Mesmos passos e mesma ordem da coluna Chave da fInventarioOP em DAX.
				// Se a mesma Chave + PartNumber repetir, fica a primeira linha da lista (Table.Distinct). Camada fora de tubo/trama/cobertura/bandagem recebe ordem 99 e nunca entra no inventário.
				Origem = SharePoint.Tables("https://danfoss.sharepoint.com/sites/OperationsGuaratingueta", [Implementation = "2.0", ViewMode = "All"]),
				Lista = Origem{[Title = "GMS_BOM_Mangueira"]}[Items],
				Colunas = Table.SelectColumns(Lista, {"Title", "Material", "Camada", "PartNumber", "Descricao", "BOM_por_metro", "Unidade", "Fonte"}, MissingField.UseNull),
				Tipos = Table.TransformColumnTypes(Colunas, {{"Title", type text}, {"Material", type text}, {"Camada", type text}, {"PartNumber", type text}, {"Descricao", type text}, {"BOM_por_metro", type number}, {"Unidade", type text}, {"Fonte", type text}}),
				Limpo = Table.TransformColumns(Tipos, {{"Title", each Text.Trim(_ ?? ""), type text}, {"Material", each Text.Trim(_ ?? ""), type text}, {"Camada", each Text.Lower(Text.Trim(_ ?? "")), type text}, {"PartNumber", each Text.Trim(_ ?? ""), type text}, {"Descricao", each Text.Trim(_ ?? ""), type text}, {"Unidade", each Text.Lower(Text.Trim(_ ?? "")), type text}, {"Fonte", each Text.Trim(_ ?? ""), type text}}),
				SoLinhas = Table.SelectRows(Limpo, each [Title] <> "" and [PartNumber] <> "" and [BOM_por_metro] <> null),
				Norm = (t as text) as text => let s0 = Text.Replace(Text.Upper(t), " ", ""), s1 = List.Accumulate({1, 2, 3}, s0, (s, _) => Text.Replace(s, "-00", "-0")), s2 = List.Accumulate({"1", "2", "3", "4", "5", "6", "7", "8", "9"}, s1, (s, d) => Text.Replace(s, "-0" & d, "-" & d)) in s2,
				ComChave = Table.AddColumn(SoLinhas, "Chave", each Norm([Title]), type text),
				ComOrdem = Table.AddColumn(ComChave, "Ordem da Camada", each if [Camada] = "tubo" then 1 else if [Camada] = "trama" then 2 else if [Camada] = "cobertura" then 3 else if [Camada] = "bandagem" then 4 else 99, Int64.Type),
				Unico = Table.Distinct(ComOrdem, {"Chave", "PartNumber"}),
				Nomes = Table.RenameColumns(Unico, {{"Title", "Mangueira"}}),
				Final = Table.SelectColumns(Nomes, {"Chave", "Mangueira", "Material", "Camada", "Ordem da Camada", "PartNumber", "Descricao", "BOM_por_metro", "Unidade", "Fonte"})
				in
				Final
```

## 2) Passo 2: tabela calculada `fInventarioOP` (depois Apply e atualize o modelo)
```
createOrReplace

	table fInventarioOP

		/// Inventário de material em processo: 1 linha por registro (ID) da ficha_producao com status Aguardando ou Em processo e etapa Trançadeira a Extr./Teste (Mandril e Tubo ficam fora). Situação pela etapa atual, Metros da última etapa fechada (Cabine desconta o inspecionado), Dias Parada até o refresh. Calculada no refresh. MEL-278.
		column ID
			dataType: int64
			isHidden
			formatString: 0
			summarizeBy: none
			sourceColumn: [ID]

		column OP
			dataType: string
			summarizeBy: none
			sourceColumn: [OP]

		column Mangueira
			dataType: string
			summarizeBy: none
			sourceColumn: [Mangueira]

		column Chave
			dataType: string
			isHidden
			summarizeBy: none
			sourceColumn: [Chave]

		column Etapa
			dataType: string
			summarizeBy: none
			sourceColumn: [Etapa]

		column Status
			dataType: string
			summarizeBy: none
			sourceColumn: [Status]

		column 'Situação'
			dataType: string
			summarizeBy: none
			sortByColumn: 'Ordem da Situação'
			sourceColumn: [Situação]

		column 'Ordem da Situação'
			dataType: int64
			isHidden
			formatString: 0
			summarizeBy: none
			sourceColumn: [Ordem da Situação]

		column 'Metros Base'
			dataType: double
			isHidden
			formatString: #,0.0
			summarizeBy: none
			sourceColumn: [Metros Base]

		column 'Metros Inspecionados'
			dataType: double
			isHidden
			formatString: #,0.0
			summarizeBy: none
			sourceColumn: [Metros Inspecionados]

		column Metros
			dataType: double
			formatString: #,0.0
			summarizeBy: none
			sourceColumn: [Metros]

		column 'Metros Suspeito'
			dataType: boolean
			summarizeBy: none
			sourceColumn: [Metros Suspeito]

		column 'Última Etapa Fechada'
			dataType: dateTime
			formatString: dd/mm/yyyy hh:mm
			summarizeBy: none
			sourceColumn: [Última Etapa Fechada]

		column 'Dias Parada'
			dataType: double
			formatString: 0.0
			summarizeBy: none
			sourceColumn: [Dias Parada]

		column 'Tem BOM'
			dataType: boolean
			summarizeBy: none
			sourceColumn: [Tem BOM]

		partition fInventarioOP = calculated
			mode: import
			source =
				VAR __Agora = UTCNOW () - 3 / 24
				VAR __Base =
				FILTER (
				ficha_producao,
				TRIM ( ficha_producao[status_processo] ) IN { "Aguardando", "Em processo" }
				&& TRIM ( ficha_producao[processo] ) IN { "Trançadeira", "Cobertura", "Bandagem", "Vulcanização", "Debandagem", "Extr./Teste" }
				)
				VAR __Pre =
				SELECTCOLUMNS (
				__Base,
				"ID", ficha_producao[ID],
				"OPn", ficha_producao[OP],
				"Limpa", ficha_producao[Mangueira_Limpa],
				"Etapa", TRIM ( ficha_producao[processo] ),
				"Status", IF ( TRIM ( ficha_producao[status_processo] ) = "Aguardando", "Aguardando", "Em processo" ),
				"t", COALESCE ( ficha_producao[quantidade_tubo], 0 ),
				"tr", COALESCE ( ficha_producao[quantidade_trancagem], 0 ),
				"c", COALESCE ( ficha_producao[quantidade_cobertura], 0 ),
				"b", COALESCE ( ficha_producao[quantidade_bandagem], 0 ),
				"v", COALESCE ( ficha_producao[quantidade_vulcanizacao], 0 ),
				"d", COALESCE ( ficha_producao[quantidade_debandagem], 0 ),
				"Ult", MAX ( MAX ( MAX ( ficha_producao[data_hora_final_mandril], ficha_producao[data_hora_final_tubo] ), MAX ( ficha_producao[data_hora_final_trancadeira], ficha_producao[data_hora_final_cobertura] ) ), MAX ( MAX ( ficha_producao[data_hora_final_bandagem], ficha_producao[data_hora_final_vulcanizacao] ), ficha_producao[data_hora_final_debandagem] ) ),
				"EmCabine", TRIM ( ficha_producao[processo] ) = "Extr./Teste" && TRIM ( ficha_producao[status_processo] ) = "Em processo"
				)
				VAR __Pos =
				SELECTCOLUMNS (
				__Pre,
				"ID", [ID],
				"OPn", [OPn],
				"Limpa", [Limpa],
				"Etapa", [Etapa],
				"Status", [Status],
				"Tubo", [t],
				"Ult", [Ult],
				"EmCabine", [EmCabine],
				"Chave",
				VAR __s0 = SUBSTITUTE ( UPPER ( [Limpa] ), " ", "" )
				VAR __s1 = SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( __s0, "-00", "-0" ), "-00", "-0" ), "-00", "-0" )
				VAR __s2 = SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( __s1, "-01", "-1" ), "-02", "-2" ), "-03", "-3" )
				VAR __s3 = SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( __s2, "-04", "-4" ), "-05", "-5" ), "-06", "-6" )
				RETURN
				SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( __s3, "-07", "-7" ), "-08", "-8" ), "-09", "-9" ),
				"Base",
				SWITCH (
				[Etapa],
				"Trançadeira", IF ( [t] > 0, [t], 0 ),
				"Cobertura", IF ( [tr] > 0, [tr], IF ( [t] > 0, [t], 0 ) ),
				"Bandagem", IF ( [c] > 0, [c], IF ( [tr] > 0, [tr], IF ( [t] > 0, [t], 0 ) ) ),
				"Vulcanização", IF ( [b] > 0, [b], IF ( [c] > 0, [c], 0 ) ),
				"Debandagem", IF ( [v] > 0, [v], IF ( [b] > 0, [b], IF ( [c] > 0, [c], 0 ) ) ),
				"Extr./Teste", IF ( [d] > 0, [d], IF ( [v] > 0, [v], IF ( [b] > 0, [b], 0 ) ) ),
				0
				)
				)
				VAR __Desc =
				SELECTCOLUMNS (
				__Pos,
				"ID", [ID],
				"OPn", [OPn],
				"Limpa", [Limpa],
				"Etapa", [Etapa],
				"Status", [Status],
				"Tubo", [Tubo],
				"Ult", [Ult],
				"Chave", [Chave],
				"Base", [Base],
				"Desc",
				VAR __op = [OPn]
				VAR __id = [ID]
				RETURN
				IF (
				[EmCabine] && NOT ISBLANK ( __op ) && __id = MAXX ( FILTER ( __Pos, [OPn] = __op && [EmCabine] ), [ID] ),
				SUMX ( FILTER ( 'RegistrosInspeção', 'RegistrosInspeção'[OP_ID] = __op ), 'RegistrosInspeção'[Quantidade] ),
				0
				)
				)
				RETURN
				SELECTCOLUMNS (
				__Desc,
				"ID", [ID],
				"OP", IF ( ISBLANK ( [OPn] ), "(sem OP)", FORMAT ( [OPn], "0" ) ),
				"Mangueira", IF ( LEN ( [Limpa] ) < 3, IF ( [Limpa] = "", "vazio", [Limpa] ) & " (inválida)", [Limpa] ),
				"Chave", [Chave],
				"Etapa", [Etapa],
				"Status", [Status],
				"Situação", SWITCH ( [Etapa], "Trançadeira", "Tubo interno", "Cobertura", "Trançada / Espiralada", "Bandagem", "Coberta", "Bandada" ),
				"Ordem da Situação", SWITCH ( [Etapa], "Trançadeira", 1, "Cobertura", 2, "Bandagem", 3, 4 ),
				"Metros Base", [Base],
				"Metros Inspecionados", [Desc],
				"Metros", MAX ( 0, [Base] - [Desc] ),
				"Metros Suspeito", [Tubo] > 0 && MAX ( 0, [Base] - [Desc] ) > 1.5 * [Tubo],
				"Última Etapa Fechada", [Ult],
				"Dias Parada", IF ( ISBLANK ( [Ult] ), BLANK (), MAX ( 0, ROUND ( __Agora - [Ult], 1 ) ) ),
				"Tem BOM",
				VAR __k = [Chave]
				RETURN
				COUNTROWS ( FILTER ( dBOMMangueira, dBOMMangueira[Chave] = __k ) ) > 0
				)
```

## 3) Passo 3: tabela calculada `fInventarioInsumo` (depois Apply e atualize o modelo)
```
createOrReplace

	table fInventarioInsumo

		/// Insumo em processo: 1 linha por registro da fInventarioOP x linha da BOM das camadas da situação (Tubo interno = tubo; Trançada = tubo, trama; Coberta = + cobertura; Bandada = + bandagem). Quantidade = BOM por metro x Metros, na unidade da BOM (kg ou m). Só registros com BOM. Calculada no refresh. MEL-278.
		column ID
			dataType: int64
			isHidden
			formatString: 0
			summarizeBy: none
			sourceColumn: [ID]

		column OP
			dataType: string
			summarizeBy: none
			sourceColumn: [OP]

		column Mangueira
			dataType: string
			summarizeBy: none
			sourceColumn: [Mangueira]

		column ChaveOP
			dataType: string
			isHidden
			summarizeBy: none
			sourceColumn: [ChaveOP]

		column 'Situação'
			dataType: string
			summarizeBy: none
			sortByColumn: 'Ordem da Situação'
			sourceColumn: [Situação]

		column 'Ordem da Situação'
			dataType: int64
			isHidden
			formatString: 0
			summarizeBy: none
			sourceColumn: [Ordem da Situação]

		column Metros
			dataType: double
			isHidden
			formatString: #,0.0
			summarizeBy: none
			sourceColumn: [Metros]

		column 'Dias Parada'
			dataType: double
			isHidden
			formatString: 0.0
			summarizeBy: none
			sourceColumn: [Dias Parada]

		column Camada
			dataType: string
			summarizeBy: none
			sortByColumn: 'Ordem da Camada'
			sourceColumn: [Camada]

		column 'Ordem da Camada'
			dataType: int64
			isHidden
			formatString: 0
			summarizeBy: none
			sourceColumn: [Ordem da Camada]

		column PartNumber
			dataType: string
			summarizeBy: none
			sourceColumn: [PartNumber]

		column Material
			dataType: string
			summarizeBy: none
			sourceColumn: [Material]

		column Descricao
			dataType: string
			summarizeBy: none
			sourceColumn: [Descricao]

		column Unidade
			dataType: string
			summarizeBy: none
			sourceColumn: [Unidade]

		column 'BOM por Metro'
			dataType: double
			isHidden
			formatString: #,0.000000
			summarizeBy: none
			sourceColumn: [BOM por Metro]

		column Quantidade
			dataType: double
			formatString: #,0.0
			summarizeBy: none
			sourceColumn: [Quantidade]

		partition fInventarioInsumo = calculated
			mode: import
			source =
				ADDCOLUMNS (
				GENERATE (
				SELECTCOLUMNS (
				fInventarioOP,
				"ID", fInventarioOP[ID],
				"OP", fInventarioOP[OP],
				"Mangueira", fInventarioOP[Mangueira],
				"ChaveOP", fInventarioOP[Chave],
				"Situação", fInventarioOP[Situação],
				"Ordem da Situação", fInventarioOP[Ordem da Situação],
				"Metros", fInventarioOP[Metros],
				"Dias Parada", fInventarioOP[Dias Parada]
				),
				SELECTCOLUMNS (
				FILTER ( dBOMMangueira, dBOMMangueira[Chave] = [ChaveOP] && dBOMMangueira[Ordem da Camada] <= [Ordem da Situação] ),
				"Camada", dBOMMangueira[Camada],
				"Ordem da Camada", dBOMMangueira[Ordem da Camada],
				"PartNumber", dBOMMangueira[PartNumber],
				"Material", dBOMMangueira[Material],
				"Descricao", dBOMMangueira[Descricao],
				"Unidade", dBOMMangueira[Unidade],
				"BOM por Metro", dBOMMangueira[BOM_por_metro]
				)
				),
				"Quantidade", [Metros] * [BOM por Metro]
				)
```

## 4) Passo 4: medidas (depois do refresh)
```
createOrReplace

	ref table Medidas

		measure '_IP Limite Dias' =
					-- Limite de dias parada: OP parada há mais que isto sai dos totais do inventário (OP zumbi). Único lugar para trocar. · MEL-278
					15
			formatString: 0
			displayFolder: Inventário Processo
			isHidden

		measure 'IP OPs na Conta' =
					-- OPs distintas em processo com BOM e parada há no máximo o limite de dias. Dias vazio fica na conta. · MEL-278
					VAR __Lim = [_IP Limite Dias]
					RETURN
					CALCULATE ( DISTINCTCOUNT ( fInventarioOP[OP] ), fInventarioOP[Tem BOM] = TRUE (), fInventarioOP[Dias Parada] <= __Lim ) + 0
			formatString: #,0
			displayFolder: Inventário Processo

		measure 'IP Metros' =
					-- Metros em processo (última etapa fechada; Cabine sem o inspecionado) dos registros com BOM e dentro do limite de dias. · MEL-278
					VAR __Lim = [_IP Limite Dias]
					RETURN
					CALCULATE ( SUM ( fInventarioOP[Metros] ), fInventarioOP[Tem BOM] = TRUE (), fInventarioOP[Dias Parada] <= __Lim )
			formatString: #,0
			displayFolder: Inventário Processo

		measure 'IP Insumo kg' =
					-- Insumo em kg em processo: BOM por metro x metros das camadas da situação (unidade kg), dentro do limite de dias. Repassa o filtro da fInventarioOP (situação, OP, mangueira) por TREATAS no ID. · MEL-278
					VAR __Lim = [_IP Limite Dias]
					RETURN
					IF (
					ISCROSSFILTERED ( fInventarioOP ),
					CALCULATE ( SUM ( fInventarioInsumo[Quantidade] ), fInventarioInsumo[Unidade] = "kg", fInventarioInsumo[Dias Parada] <= __Lim, TREATAS ( VALUES ( fInventarioOP[ID] ), fInventarioInsumo[ID] ) ),
					CALCULATE ( SUM ( fInventarioInsumo[Quantidade] ), fInventarioInsumo[Unidade] = "kg", fInventarioInsumo[Dias Parada] <= __Lim )
					)
			formatString: #,0.0
			displayFolder: Inventário Processo

		measure 'IP Insumo m' =
					-- Insumo em metros em processo (fita e filme da bandagem, unidade m), dentro do limite de dias. Mesmo repasse de filtro da IP Insumo kg. · MEL-278
					VAR __Lim = [_IP Limite Dias]
					RETURN
					IF (
					ISCROSSFILTERED ( fInventarioOP ),
					CALCULATE ( SUM ( fInventarioInsumo[Quantidade] ), fInventarioInsumo[Unidade] = "m", fInventarioInsumo[Dias Parada] <= __Lim, TREATAS ( VALUES ( fInventarioOP[ID] ), fInventarioInsumo[ID] ) ),
					CALCULATE ( SUM ( fInventarioInsumo[Quantidade] ), fInventarioInsumo[Unidade] = "m", fInventarioInsumo[Dias Parada] <= __Lim )
					)
			formatString: #,0.0
			displayFolder: Inventário Processo

		measure 'IP OPs sem BOM' =
					-- OPs distintas em processo cuja mangueira não tem BOM (fora dos totais), dentro do limite de dias. Aviso da página. · MEL-278
					VAR __Lim = [_IP Limite Dias]
					RETURN
					CALCULATE ( DISTINCTCOUNT ( fInventarioOP[OP] ), fInventarioOP[Tem BOM] = FALSE (), fInventarioOP[Dias Parada] <= __Lim ) + 0
			formatString: #,0
			displayFolder: Inventário Processo

		measure 'IP Metros sem BOM' =
					-- Metros em processo das OPs sem BOM, dentro do limite de dias. · MEL-278
					VAR __Lim = [_IP Limite Dias]
					RETURN
					CALCULATE ( SUM ( fInventarioOP[Metros] ), fInventarioOP[Tem BOM] = FALSE (), fInventarioOP[Dias Parada] <= __Lim )
			formatString: #,0
			displayFolder: Inventário Processo

		measure 'IP Mangueiras sem BOM' =
					-- Mangueiras distintas sem BOM com OP em processo, dentro do limite de dias (lista de aviso da página). · MEL-278
					VAR __Lim = [_IP Limite Dias]
					RETURN
					CALCULATE ( DISTINCTCOUNT ( fInventarioOP[Mangueira] ), fInventarioOP[Tem BOM] = FALSE (), fInventarioOP[Dias Parada] <= __Lim ) + 0
			formatString: #,0
			displayFolder: Inventário Processo

		measure 'IP OPs Paradas' =
					-- OPs distintas paradas há mais que o limite de dias (OP zumbi): fora dos totais, contadas à parte. · MEL-278
					VAR __Lim = [_IP Limite Dias]
					RETURN
					CALCULATE ( DISTINCTCOUNT ( fInventarioOP[OP] ), fInventarioOP[Dias Parada] > __Lim ) + 0
			formatString: #,0
			displayFolder: Inventário Processo

		measure 'IP Metros Paradas' =
					-- Metros das OPs paradas há mais que o limite de dias (fora dos totais). · MEL-278
					VAR __Lim = [_IP Limite Dias]
					RETURN
					CALCULATE ( SUM ( fInventarioOP[Metros] ), fInventarioOP[Dias Parada] > __Lim )
			formatString: #,0
			displayFolder: Inventário Processo

		measure 'IP Registros Metros Suspeito' =
					-- Registros na conta com Metros acima de 1,5 x a quantidade do tubo (dado a conferir; não sai da conta). · MEL-278
					VAR __Lim = [_IP Limite Dias]
					RETURN
					CALCULATE ( COUNTROWS ( fInventarioOP ), fInventarioOP[Metros Suspeito] = TRUE (), fInventarioOP[Tem BOM] = TRUE (), fInventarioOP[Dias Parada] <= __Lim ) + 0
			formatString: #,0
			displayFolder: Inventário Processo

		measure 'IP Metros Descontados Cabine' =
					-- Metros já inspecionados na Cabine (Extr./Teste Em processo) descontados dos metros base, dentro da conta. · MEL-278
					VAR __Lim = [_IP Limite Dias]
					RETURN
					CALCULATE ( SUM ( fInventarioOP[Metros Inspecionados] ), fInventarioOP[Tem BOM] = TRUE (), fInventarioOP[Dias Parada] <= __Lim )
			formatString: #,0.0
			displayFolder: Inventário Processo

		measure 'IP Dias Parada' =
					-- Dias parados da OP no contexto: agora BR (no refresh) menos a maior data final de etapa; maior valor se houver mais de um registro. · MEL-278
					MAX ( fInventarioOP[Dias Parada] )
			formatString: 0.0
			displayFolder: Inventário Processo

		measure 'IP Na Conta' =
					-- 1 se a OP do contexto entra nos totais (tem BOM e dias parada dentro do limite), 0 se não. Para filtro de visual da tabela de OPs. · MEL-278
					VAR __Lim = [_IP Limite Dias]
					RETURN
					IF ( NOT ISEMPTY ( fInventarioOP ), IF ( COUNTROWS ( FILTER ( fInventarioOP, fInventarioOP[Tem BOM] = TRUE () && fInventarioOP[Dias Parada] <= __Lim ) ) > 0, 1, 0 ) )
			formatString: 0
			displayFolder: Inventário Processo

		measure 'IP Motivo Fora' =
					-- Por que a OP do contexto está fora dos totais: parada acima do limite ou mangueira sem BOM. Vazio se está na conta. · MEL-278
					VAR __Lim = [_IP Limite Dias]
					VAR __Paradas = COUNTROWS ( FILTER ( fInventarioOP, fInventarioOP[Dias Parada] > __Lim ) )
					VAR __SemBom = COUNTROWS ( FILTER ( fInventarioOP, fInventarioOP[Tem BOM] = FALSE () ) )
					RETURN
					IF ( __Paradas > 0, "Parada > " & FORMAT ( __Lim, "0" ) & " dias", IF ( __SemBom > 0, "Sem BOM" ) )
			displayFolder: Inventário Processo

		measure 'IP Alerta Metros' =
					-- "Conferir metros" se a OP do contexto tem registro com Metros acima de 1,5 x tubo. Coluna de alerta da tabela. · MEL-278
					IF ( COUNTROWS ( FILTER ( fInventarioOP, fInventarioOP[Metros Suspeito] = TRUE () ) ) > 0, "Conferir metros" )
			displayFolder: Inventário Processo

```

## 5) Verificação depois do refresh (DAX query view)
1. **Por situação** (OPs, metros e kg; compare com o protótipo de 27/11 08:10, que usa a ficha daquele horário e já tem FC735-06 na BOM e o desconto da Cabine: Tubo interno 7 OPs 4.010 m; Trançada / Espiralada 11 OPs 6.140 m; Coberta 3 OPs 1.590 m; Bandada 11 OPs 4.202,9 m, sendo a OP 30974903 na Cabine com 400 − 377,1 inspecionados = 22,9 m. Os números do modelo vão diferir porque a ficha muda; kg e m do modelo comparam com o `inventario_processo.html`):
```
EVALUATE
SUMMARIZECOLUMNS (
    fInventarioOP[Ordem da Situação],
    fInventarioOP[Situação],
    "OPs", [IP OPs na Conta],
    "Metros", [IP Metros],
    "Insumo kg", [IP Insumo kg],
    "Insumo m", [IP Insumo m]
)
ORDER BY fInventarioOP[Ordem da Situação]
```
   Total geral: `EVALUATE ROW ( "OPs", [IP OPs na Conta], "Metros", [IP Metros], "kg", [IP Insumo kg], "m", [IP Insumo m] )`.
2. **Sem BOM e paradas** (protótipo: sem BOM EC215-12LRL, 12102159, 12102164; a fonte das mangueiras com número é o alias SAP, pendência):
```
EVALUATE
FILTER (
    SUMMARIZECOLUMNS ( fInventarioOP[Mangueira], "OPs", [IP OPs sem BOM], "Metros", [IP Metros sem BOM] ),
    [OPs] > 0
)
ORDER BY [Metros] DESC
```
   e `EVALUATE ROW ( "OPs paradas", [IP OPs Paradas], "Metros parados", [IP Metros Paradas], "Registros sem data", COUNTROWS ( FILTER ( fInventarioOP, ISBLANK ( fInventarioOP[Dias Parada] ) ) ) )`.
3. **Grão** (registros x OPs; registros com OP repetida são os filhos de sobra; protótipo: contagem de registros = soma das OPs do passo 1 mais as sem BOM e as paradas):
```
EVALUATE
ROW (
    "Registros", COUNTROWS ( fInventarioOP ),
    "OPs", DISTINCTCOUNT ( fInventarioOP[OP] ),
    "Registros esperados da ficha", COUNTROWS ( FILTER ( ficha_producao, TRIM ( ficha_producao[status_processo] ) IN { "Aguardando", "Em processo" } && TRIM ( ficha_producao[processo] ) IN { "Trançadeira", "Cobertura", "Bandagem", "Vulcanização", "Debandagem", "Extr./Teste" } ) ),
    "Mandril/Tubo fora", COUNTROWS ( FILTER ( ficha_producao, TRIM ( ficha_producao[status_processo] ) IN { "Aguardando", "Em processo" } && TRIM ( ficha_producao[processo] ) IN { "Mandril", "Tubo" } ) )
)
```
   "Registros" tem que ser igual a "Registros esperados da ficha".
4. **Cabine** (protótipo: OP 30974903, 400 m base, 377,1 inspecionados, 22,9 m):
```
EVALUATE
SELECTCOLUMNS (
    FILTER ( fInventarioOP, fInventarioOP[Etapa] = "Extr./Teste" ),
    "ID", fInventarioOP[ID],
    "OP", fInventarioOP[OP],
    "Status", fInventarioOP[Status],
    "Base", fInventarioOP[Metros Base],
    "Inspecionado", fInventarioOP[Metros Inspecionados],
    "Metros", fInventarioOP[Metros]
)
ORDER BY [OP], [ID]
```
   `Aguardando` tem Inspecionado 0; OP com 2 registros em `Em processo` tem desconto só no de maior ID.
5. **Metros suspeito** (protótipo: 30830675, 30842509, 30899867, 31003282):
```
EVALUATE
SELECTCOLUMNS (
    FILTER ( fInventarioOP, fInventarioOP[Metros Suspeito] = TRUE () ),
    "OP", fInventarioOP[OP],
    "Etapa", fInventarioOP[Etapa],
    "Metros", fInventarioOP[Metros]
)
ORDER BY [OP]
```
6. **BOM** (`Linhas` por volta de 300 antes do `Distinct`; os três zeros abaixo são obrigatórios; `Mangueiras` deve ser parecido com o do protótipo):
```
EVALUATE
ROW (
    "Linhas", COUNTROWS ( dBOMMangueira ),
    "Mangueiras", DISTINCTCOUNT ( dBOMMangueira[Chave] ),
    "Camada fora do padrão", COUNTROWS ( FILTER ( dBOMMangueira, dBOMMangueira[Ordem da Camada] = 99 ) ),
    "Unidade fora de kg/m", COUNTROWS ( FILTER ( dBOMMangueira, NOT dBOMMangueira[Unidade] IN { "kg", "m" } ) ),
    "Chave com -0N (BOM)", COUNTROWS ( FILTER ( dBOMMangueira, SUMX ( { 1, 2, 3, 4, 5, 6, 7, 8, 9 }, IF ( CONTAINSSTRING ( dBOMMangueira[Chave], "-0" & [Value] ), 1, 0 ) ) > 0 ) ),
    "Chave com -0N (ficha)", COUNTROWS ( FILTER ( fInventarioOP, SUMX ( { 1, 2, 3, 4, 5, 6, 7, 8, 9 }, IF ( CONTAINSSTRING ( fInventarioOP[Chave], "-0" & [Value] ), 1, 0 ) ) > 0 ) ),
    "Chave + PartNumber repetido", COUNTROWS ( dBOMMangueira ) - COUNTROWS ( SUMMARIZE ( dBOMMangueira, dBOMMangueira[Chave], dBOMMangueira[PartNumber] ) )
)
```
   "Camada fora do padrão" e "Unidade fora de kg/m" maiores que 0 pedem ajuste na lista (a linha não entra no insumo).
7. **Fuso**: a maior data final da ficha não pode estar à frente de agora BR (se estiver ~3 h à frente, as datas do modelo estão em UTC e `Dias Parada` precisa trocar o `- 3 / 24`):
```
EVALUATE
ROW (
    "Agora BR", UTCNOW () - 3 / 24,
    "Maior data final", MAX ( fInventarioOP[Última Etapa Fechada] ),
    "Maior Dias Parada", MAX ( fInventarioOP[Dias Parada] )
)
```
8. **`OP_ID` da inspeção é a OP?** O número de achados na ficha pela OP deve ser bem maior que pelo ID:
```
EVALUATE
ROW (
    "OP_ID distintos", DISTINCTCOUNT ( 'RegistrosInspeção'[OP_ID] ),
    "Achados em ficha[OP]", COUNTROWS ( FILTER ( VALUES ( 'RegistrosInspeção'[OP_ID] ), CONTAINS ( VALUES ( ficha_producao[OP] ), ficha_producao[OP], 'RegistrosInspeção'[OP_ID] ) ) ),
    "Achados em ficha[ID]", COUNTROWS ( FILTER ( VALUES ( 'RegistrosInspeção'[OP_ID] ), CONTAINS ( VALUES ( ficha_producao[ID] ), ficha_producao[ID], 'RegistrosInspeção'[OP_ID] ) ) )
)
```
9. **Normalização**: `FC598-08` na ficha casa com `FC598-8` da BOM: `EVALUATE FILTER ( fInventarioOP, fInventarioOP[Tem BOM] = FALSE () )` com `Chave` e `Mangueira` mostra as sem BOM para conferir uma a uma com a lista.
10. `INFO.COLUMNS()` e `INFO.MEASURES()` com `[State] <> 1` devem devolver 0 linhas.
11. Filtro de situação passa para o insumo: no visual de cartão com filtro `fInventarioOP[Situação] = Coberta`, `IP Insumo kg` deve bater com a linha Coberta do passo 1.

## 6) Onde mexer depois
- BOM: **só na lista `GMS_BOM_Mangueira`** (vale no próximo refresh, sem republicar). Mangueira nova sem linha na lista aparece no aviso "sem BOM".
- Limite de dias: `_IP Limite Dias` (passo 4, trocar o `15`).
- Pendências: alias de código SAP digitado no lugar do nome da mangueira (hoje cai em sem BOM); mais de um registro na Cabine para a mesma OP desconta só no de maior ID; sem relacionamento entre as duas tabelas (TREATAS no ID). As medidas SVG da página vão no `reportExtensions.json`, não aqui.
