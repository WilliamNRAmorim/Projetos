# Extrusora de Mandril no modelo (GMS) — APLICADO em 20/10/2026 (com 3 ajustes)

Estado do modelo em 20/10/2026 (lido no TMDL view do serviço):
- `ControleExtrusora_estrutura` JÁ existe (115 linhas, 05/06 a 19/10/2026), com 3 medidas na pasta
  "11 Extrusora Mandril": `Qtd Extrusora Mandril` (ok), `Refugo Extrusora Mandril` e `% Refugo Extrusora`
  (as duas com ERRO: apontam para `RefugoExtrusora_estrutura`, que não existe no modelo).
- Não há tabela de refugo da extrusora. Também não há `TiposErros` (o Mestre BI descreve `fRefugo`, mas ele não existe).
- Sem relacionamento com `dCalendario`: o padrão é a data virtual por `INT(datetime) IN VALUES(dCalendario[Date])`
  (já usado na medida existente). Mantido.

## Problema de regra encontrado
Produção da extrusora está em **metros** (`quantidade`); o refugo é lançado em **kg** (`Quantidade`, tela
scr_ExtrusoraMandril_1). A medida `% Refugo Extrusora` existente faz `refugo / (produzido + refugo)`, somando kg com
metros. Isso dá um número sem sentido. Proposta: apagar essa medida e usar **kg de refugo por 1.000 m extrudados**.

## 1) Tabela nova (colunas das lists, mesma origem SharePoint)
```
createOrReplace

	table RefugoExtrusora_estrutura
		lineageTag: 6b0f2c1e-3a54-4d7e-9f10-2d5c8a7e4b01

		/// Refugo lançado na tela da Extrusora de Mandril (unidade: kg). Fonte: lista RefugoExtrusora_estrutura.
		column Title
			dataType: string
			summarizeBy: none
			sourceColumn: Title
		column Bitola
			dataType: double
			summarizeBy: none
			sourceColumn: Bitola
		column cod_mandril
			dataType: string
			summarizeBy: none
			sourceColumn: cod_mandril
		column CodigoErro
			dataType: string
			summarizeBy: none
			sourceColumn: CodigoErro
		column Quantidade
			dataType: double
			summarizeBy: sum
			sourceColumn: Quantidade
		column operador
			dataType: string
			summarizeBy: none
			sourceColumn: operador
		column DataHoraRefugo
			dataType: dateTime
			formatString: General Date
			summarizeBy: none
			sourceColumn: DataHoraRefugo
		column Turno
			dataType: string
			summarizeBy: none
			sourceColumn: Turno
		column Observacao
			dataType: string
			summarizeBy: none
			sourceColumn: Observacao
		column ID
			dataType: int64
			formatString: 0
			summarizeBy: none
			sourceColumn: ID

		partition RefugoExtrusora_estrutura = m
			mode: import
			source =
				let
				  Origem = SharePoint.Tables("https://danfoss.sharepoint.com/sites/OperationsGuaratingueta", [Implementation = "2.0", ViewMode = "All"]),
				  Lista = Origem{[Name = "RefugoExtrusora_estrutura"]}[Items],
				  Colunas = Table.SelectColumns(Lista, {"Title","Bitola","cod_mandril","CodigoErro","Quantidade","operador","DataHoraRefugo","Turno","Observacao","ID"}, MissingField.UseNull),
				  Tipos = Table.TransformColumnTypes(Colunas, {{"Bitola", type number}, {"Quantidade", type number}, {"DataHoraRefugo", type datetime}, {"ID", Int64.Type}})
				in
				  Tipos
```

## 2) Medidas (em `ControleExtrusora_estrutura`, pasta "11 Extrusora Mandril")
- `Refugo Extrusora Mandril` (kg): já existe; volta a funcionar com a tabela nova. Passo a rotular "(kg)" no formato `#,##0.0`.
- Apagar `% Refugo Extrusora` (mistura kg e m).
- `Refugo kg por 1000 m` = `DIVIDE([Refugo Extrusora Mandril], [Qtd Extrusora Mandril]) * 1000`
- `Extrusões Mandril` = contagem de extrusões com data no recorte (mesmo padrão de data virtual)
- `Metros por Dia Extrusora` = `DIVIDE([Qtd Extrusora Mandril], DISTINCTCOUNT(dCalendario[Date]))` sob filtro de calendário

## 3) Verificação planejada (depois de aplicar)
- 115 linhas e 05/06–19/10 em `ControleExtrusora_estrutura`.
- Contagem e soma de kg de `RefugoExtrusora_estrutura` contra a lista no SharePoint.
- Soma de metros por bitola = total.

## O que foi aplicado de fato (TMDL view do serviço, com o sim do William)
1. Tabela `RefugoExtrusora_Mandril` (não `RefugoExtrusora_estrutura`: o documento M do modelo já tinha um membro com esse
   nome e recusava a tabela com "duplicate member"). Partição `RefugoExtrusora_Mandril`, mesma lista do SharePoint.
2. Medidas em `ControleExtrusora_estrutura` (pasta 11 Extrusora Mandril): `Refugo Extrusora Mandril` (agora aponta para a
   tabela nova, kg), `Refugo kg por 1000 m`, `Extrusoes Mandril`, `Dias com Extrusao`, `Metros por Dia Extrusora`.
3. `% Refugo Extrusora` não pôde ser apagada por script; ficou oculta, `BLANK()` e marcada como descontinuada.
4. Verificado no modelo: produção = 115 linhas, 91.609,2 m, 55 dias com extrusão, 1.666 m/dia; `Extrusoes Mandril` = 115.
5. NÃO verificado: refugo. A partição ficou em estado "sem dados" mesmo após atualização manual (9h42–9h50). Falta uma
   atualização que processe a tabela (a agendada de 10h30 ou o Atualizar do Desktop) e conferir contagem e soma de kg
   contra a lista do SharePoint.

## Correção do refugo em branco (20/10/2026, 11h)
- Causa: o `SharePoint.Tables` não achou a lista por `[Name = "RefugoExtrusora_estrutura"]` (Key didn't match any rows),
  porque o Name interno difere do título. A tabela de produção usa o Id da lista; a de refugo passou a usar o Id
  `a89c744f-95a8-4007-944b-d3faafcb8aca` (lido na API do SharePoint; Title RefugoExtrusora_estrutura, 124 itens).
- Resultado após atualizar o modelo: estado Ready, 124 linhas (= itens da lista), 1.420,9 kg, 21/05 a 20/10/2026,
  0 linhas sem data, 15,51 kg por 1.000 m no total.
- Atenção: `CodigoErro` tem prefixo numérico repetido com textos diferentes: "2 - Defeito superficial" e "2- Set-Up";
  "6 - Outros" e "7 - Outros". É o mesmo problema de posição de dropdown que mudou, visto na MEL-107. Não padronizado.
