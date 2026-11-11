# fFluxoBase: base única das figuras da página Fluxo — PENDENTE DE APLICAR (só com o "Libero" do William, no TMDL view do modelo vivo)

Tabela calculada oculta com o UNION das 7 etapas que cada medida "Fluxo · ..." montava na VAR `__B` (7 x `SELECTCOLUMNS ( FILTER ( ALL ( ficha_producao ), ...` a cada clique). Agora é calculada 1 vez por refresh. Expressão idêntica à antiga, com duas diferenças propositais: `ficha_producao` no lugar de `ALL ( ficha_producao )` (os dois ignoram o contexto) e **sem** o filtro `[@Dia] IN __Datas` de cada etapa, que depende da tela e continua dentro das medidas.

## Antes de colar
- Mesmas regras da seção 7 e 11 do `GMS/Analises/Higienizacao_HoraHora/COMO_ARRUMAR_HORAHORA.md`: digite no TMDL view sem indentação à esquerda, `Tab`/`shift+Tab` para a estrutura, `Escape` depois de cada linha (fecha o autocompletar), botão **Apply**. Todas as linhas da expressão ficam no mesmo nível (4 tabs) de propósito.
- A tabela só tem valor depois de um **refresh**; antes disso a consulta dá "needs to be recalculated or refreshed". **Não aplique a troca das medidas (`reportExtensions.json`) antes do refresh e da conferência.**
- Sem relacionamentos: as medidas leem com `ALL ( fFluxoBase )`.
- Depende de `ficha_producao` (colunas `Trançadeira` e `Bitola`, `data_hora_final_*`, `quantidade_*`, `operador_tubo`). Se o refresh falhar por ordem de cálculo, rode de novo.
- Backup das medidas antigas (nome → expressão): `GMS/Analises/BI_HoraCheia/fluxo_medidas_antes.json`.

## 1) Script TMDL (cole inteiro)
```
createOrReplace

	table fFluxoBase

		isHidden

		/// Base da página Fluxo: 1 linha por tubo x etapa (E 1 a 7) com dia produtivo (05:20), turno, quantidade (>2000 vira vazio), máquina normalizada, operador sem acento, carretéis e cobertura. Substitui a VAR __B das medidas Fluxo.
		column E
			dataType: int64
			formatString: 0
			summarizeBy: none
			sourceColumn: [E]

		column Dia
			dataType: dateTime
			formatString: dd/mm/yyyy
			summarizeBy: none
			sourceColumn: [Dia]

		column T
			dataType: int64
			formatString: 0
			summarizeBy: none
			sourceColumn: [T]

		column Q
			dataType: double
			formatString: #,0.0
			summarizeBy: none
			sourceColumn: [Q]

		column M
			dataType: string
			summarizeBy: none
			sourceColumn: [M]

		column Op
			dataType: string
			summarizeBy: none
			sourceColumn: [Op]

		column Car
			dataType: double
			formatString: #,0.000
			summarizeBy: none
			sourceColumn: [Car]

		column Cob
			dataType: double
			formatString: #,0.0
			summarizeBy: none
			sourceColumn: [Cob]

		partition fFluxoBase = calculated
			mode: import
			source =
				UNION (
				SELECTCOLUMNS (
				FILTER ( ALL ( ficha_producao ), NOT ISBLANK ( ficha_producao[data_hora_final_tubo] ) ),
				"E", 1,
				"Dia", VAR __fS1 = ficha_producao[data_hora_final_tubo] - 320 / 1440 RETURN DATE ( YEAR ( __fS1 ), MONTH ( __fS1 ), DAY ( __fS1 ) ),
				"T", VAR __mS1 = HOUR ( ficha_producao[data_hora_final_tubo] ) * 60 + MINUTE ( ficha_producao[data_hora_final_tubo] ) RETURN IF ( __mS1 >= 320 && __mS1 < 837, 1, IF ( __mS1 >= 837 && __mS1 < 1340, 2, 3 ) ),
				"Q", VAR __qS1 = ficha_producao[quantidade_tubo] RETURN IF ( __qS1 > 2000, BLANK (), __qS1 ),
				"M", VAR __mqS1 = UPPER ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( ficha_producao[Trançadeira], ".", "" ), "-", "" ), " ", "" ), "_", "" ) ) RETURN IF ( __mqS1 IN { "SPIRAL", "TE01", "TE0" }, "SPIRAL", __mqS1 ),
				"Op", SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER ( ficha_producao[operador_tubo] ),"Á","A"),"À","A"),"Â","A"),"Ã","A"),"Ä","A"),"É","E"),"È","E"),"Ê","E"),"Ë","E"),"Í","I"),"Ì","I"),"Î","I"),"Ï","I"),"Ó","O"),"Ò","O"),"Ô","O"),"Õ","O"),"Ö","O"),"Ú","U"),"Ù","U"),"Û","U"),"Ü","U"),"Ç","C"),"Ñ","N"),".",""),",",""),"-",""),"_",""),"/","|"),
				"Car", VAR __cS1Car = ficha_producao[quantidade_tubo] VAR __cvS1Car = IF ( __cS1Car > 2000, BLANK (), __cS1Car ) VAR __mcS1Car = SWITCH ( ficha_producao[Bitola], 4, 800, 6, 680, 8, 680, 10, 460, 12, 400, 16, 250 ) RETURN DIVIDE ( __cvS1Car, __mcS1Car ),
				"Cob", VAR __cS1Cob = ficha_producao[quantidade_tubo] VAR __cvS1Cob = IF ( __cS1Cob > 2000, BLANK (), __cS1Cob ) VAR __mcS1Cob = SWITCH ( ficha_producao[Bitola], 4, 800, 6, 680, 8, 680, 10, 460, 12, 400, 16, 250 ) RETURN IF ( NOT ISBLANK ( __mcS1Cob ), __cvS1Cob )
				),
				SELECTCOLUMNS (
				FILTER ( ALL ( ficha_producao ), NOT ISBLANK ( ficha_producao[data_hora_final_trancadeira] ) ),
				"E", 2,
				"Dia", VAR __fS2 = ficha_producao[data_hora_final_trancadeira] - 320 / 1440 RETURN DATE ( YEAR ( __fS2 ), MONTH ( __fS2 ), DAY ( __fS2 ) ),
				"T", VAR __mS2 = HOUR ( ficha_producao[data_hora_final_trancadeira] ) * 60 + MINUTE ( ficha_producao[data_hora_final_trancadeira] ) RETURN IF ( __mS2 >= 320 && __mS2 < 837, 1, IF ( __mS2 >= 837 && __mS2 < 1340, 2, 3 ) ),
				"Q", VAR __qS2 = ficha_producao[quantidade_trancagem] RETURN IF ( __qS2 > 2000, BLANK (), __qS2 ),
				"M", VAR __mqS2 = UPPER ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( ficha_producao[Trançadeira], ".", "" ), "-", "" ), " ", "" ), "_", "" ) ) RETURN IF ( __mqS2 IN { "SPIRAL", "TE01", "TE0" }, "SPIRAL", __mqS2 ),
				"Op", SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER ( ficha_producao[operador_trancagem] ),"Á","A"),"À","A"),"Â","A"),"Ã","A"),"Ä","A"),"É","E"),"È","E"),"Ê","E"),"Ë","E"),"Í","I"),"Ì","I"),"Î","I"),"Ï","I"),"Ó","O"),"Ò","O"),"Ô","O"),"Õ","O"),"Ö","O"),"Ú","U"),"Ù","U"),"Û","U"),"Ü","U"),"Ç","C"),"Ñ","N"),".",""),",",""),"-",""),"_",""),"/","|"),
				"Car", VAR __cS2Car = ficha_producao[quantidade_trancagem] VAR __cvS2Car = IF ( __cS2Car > 2000, BLANK (), __cS2Car ) VAR __mcS2Car = SWITCH ( ficha_producao[Bitola], 4, 800, 6, 680, 8, 680, 10, 460, 12, 400, 16, 250 ) RETURN DIVIDE ( __cvS2Car, __mcS2Car ),
				"Cob", VAR __cS2Cob = ficha_producao[quantidade_trancagem] VAR __cvS2Cob = IF ( __cS2Cob > 2000, BLANK (), __cS2Cob ) VAR __mcS2Cob = SWITCH ( ficha_producao[Bitola], 4, 800, 6, 680, 8, 680, 10, 460, 12, 400, 16, 250 ) RETURN IF ( NOT ISBLANK ( __mcS2Cob ), __cvS2Cob )
				),
				SELECTCOLUMNS (
				FILTER ( ALL ( ficha_producao ), NOT ISBLANK ( ficha_producao[data_hora_final_cobertura] ) ),
				"E", 3,
				"Dia", VAR __fS3 = ficha_producao[data_hora_final_cobertura] - 320 / 1440 RETURN DATE ( YEAR ( __fS3 ), MONTH ( __fS3 ), DAY ( __fS3 ) ),
				"T", VAR __mS3 = HOUR ( ficha_producao[data_hora_final_cobertura] ) * 60 + MINUTE ( ficha_producao[data_hora_final_cobertura] ) RETURN IF ( __mS3 >= 320 && __mS3 < 837, 1, IF ( __mS3 >= 837 && __mS3 < 1340, 2, 3 ) ),
				"Q", VAR __qS3 = ficha_producao[quantidade_cobertura] RETURN IF ( __qS3 > 2000, BLANK (), __qS3 ),
				"M", VAR __mqS3 = UPPER ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( ficha_producao[Trançadeira], ".", "" ), "-", "" ), " ", "" ), "_", "" ) ) RETURN IF ( __mqS3 IN { "SPIRAL", "TE01", "TE0" }, "SPIRAL", __mqS3 ),
				"Op", SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER ( ficha_producao[operador_cobertura] ),"Á","A"),"À","A"),"Â","A"),"Ã","A"),"Ä","A"),"É","E"),"È","E"),"Ê","E"),"Ë","E"),"Í","I"),"Ì","I"),"Î","I"),"Ï","I"),"Ó","O"),"Ò","O"),"Ô","O"),"Õ","O"),"Ö","O"),"Ú","U"),"Ù","U"),"Û","U"),"Ü","U"),"Ç","C"),"Ñ","N"),".",""),",",""),"-",""),"_",""),"/","|"),
				"Car", VAR __cS3Car = ficha_producao[quantidade_cobertura] VAR __cvS3Car = IF ( __cS3Car > 2000, BLANK (), __cS3Car ) VAR __mcS3Car = SWITCH ( ficha_producao[Bitola], 4, 800, 6, 680, 8, 680, 10, 460, 12, 400, 16, 250 ) RETURN DIVIDE ( __cvS3Car, __mcS3Car ),
				"Cob", VAR __cS3Cob = ficha_producao[quantidade_cobertura] VAR __cvS3Cob = IF ( __cS3Cob > 2000, BLANK (), __cS3Cob ) VAR __mcS3Cob = SWITCH ( ficha_producao[Bitola], 4, 800, 6, 680, 8, 680, 10, 460, 12, 400, 16, 250 ) RETURN IF ( NOT ISBLANK ( __mcS3Cob ), __cvS3Cob )
				),
				SELECTCOLUMNS (
				FILTER ( ALL ( ficha_producao ), NOT ISBLANK ( ficha_producao[data_hora_final_bandagem] ) ),
				"E", 4,
				"Dia", VAR __fS4 = ficha_producao[data_hora_final_bandagem] - 320 / 1440 RETURN DATE ( YEAR ( __fS4 ), MONTH ( __fS4 ), DAY ( __fS4 ) ),
				"T", VAR __mS4 = HOUR ( ficha_producao[data_hora_final_bandagem] ) * 60 + MINUTE ( ficha_producao[data_hora_final_bandagem] ) RETURN IF ( __mS4 >= 320 && __mS4 < 837, 1, IF ( __mS4 >= 837 && __mS4 < 1340, 2, 3 ) ),
				"Q", VAR __qS4 = ficha_producao[quantidade_bandagem] RETURN IF ( __qS4 > 2000, BLANK (), __qS4 ),
				"M", VAR __mqS4 = UPPER ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( ficha_producao[Trançadeira], ".", "" ), "-", "" ), " ", "" ), "_", "" ) ) RETURN IF ( __mqS4 IN { "SPIRAL", "TE01", "TE0" }, "SPIRAL", __mqS4 ),
				"Op", SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER ( ficha_producao[operador_bandagem] ),"Á","A"),"À","A"),"Â","A"),"Ã","A"),"Ä","A"),"É","E"),"È","E"),"Ê","E"),"Ë","E"),"Í","I"),"Ì","I"),"Î","I"),"Ï","I"),"Ó","O"),"Ò","O"),"Ô","O"),"Õ","O"),"Ö","O"),"Ú","U"),"Ù","U"),"Û","U"),"Ü","U"),"Ç","C"),"Ñ","N"),".",""),",",""),"-",""),"_",""),"/","|"),
				"Car", VAR __cS4Car = ficha_producao[quantidade_bandagem] VAR __cvS4Car = IF ( __cS4Car > 2000, BLANK (), __cS4Car ) VAR __mcS4Car = SWITCH ( ficha_producao[Bitola], 4, 800, 6, 680, 8, 680, 10, 460, 12, 400, 16, 250 ) RETURN DIVIDE ( __cvS4Car, __mcS4Car ),
				"Cob", VAR __cS4Cob = ficha_producao[quantidade_bandagem] VAR __cvS4Cob = IF ( __cS4Cob > 2000, BLANK (), __cS4Cob ) VAR __mcS4Cob = SWITCH ( ficha_producao[Bitola], 4, 800, 6, 680, 8, 680, 10, 460, 12, 400, 16, 250 ) RETURN IF ( NOT ISBLANK ( __mcS4Cob ), __cvS4Cob )
				),
				SELECTCOLUMNS (
				FILTER ( ALL ( ficha_producao ), NOT ISBLANK ( ficha_producao[data_hora_final_vulcanizacao] ) ),
				"E", 5,
				"Dia", VAR __fS5 = ficha_producao[data_hora_final_vulcanizacao] - 320 / 1440 RETURN DATE ( YEAR ( __fS5 ), MONTH ( __fS5 ), DAY ( __fS5 ) ),
				"T", VAR __mS5 = HOUR ( ficha_producao[data_hora_final_vulcanizacao] ) * 60 + MINUTE ( ficha_producao[data_hora_final_vulcanizacao] ) RETURN IF ( __mS5 >= 320 && __mS5 < 837, 1, IF ( __mS5 >= 837 && __mS5 < 1340, 2, 3 ) ),
				"Q", VAR __qS5 = ficha_producao[quantidade_vulcanizacao] RETURN IF ( __qS5 > 2000, BLANK (), __qS5 ),
				"M", VAR __mqS5 = UPPER ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( ficha_producao[Trançadeira], ".", "" ), "-", "" ), " ", "" ), "_", "" ) ) RETURN IF ( __mqS5 IN { "SPIRAL", "TE01", "TE0" }, "SPIRAL", __mqS5 ),
				"Op", SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER ( ficha_producao[operador_vulcanizacao] ),"Á","A"),"À","A"),"Â","A"),"Ã","A"),"Ä","A"),"É","E"),"È","E"),"Ê","E"),"Ë","E"),"Í","I"),"Ì","I"),"Î","I"),"Ï","I"),"Ó","O"),"Ò","O"),"Ô","O"),"Õ","O"),"Ö","O"),"Ú","U"),"Ù","U"),"Û","U"),"Ü","U"),"Ç","C"),"Ñ","N"),".",""),",",""),"-",""),"_",""),"/","|"),
				"Car", VAR __cS5Car = ficha_producao[quantidade_vulcanizacao] VAR __cvS5Car = IF ( __cS5Car > 2000, BLANK (), __cS5Car ) VAR __mcS5Car = SWITCH ( ficha_producao[Bitola], 4, 800, 6, 680, 8, 680, 10, 460, 12, 400, 16, 250 ) RETURN DIVIDE ( __cvS5Car, __mcS5Car ),
				"Cob", VAR __cS5Cob = ficha_producao[quantidade_vulcanizacao] VAR __cvS5Cob = IF ( __cS5Cob > 2000, BLANK (), __cS5Cob ) VAR __mcS5Cob = SWITCH ( ficha_producao[Bitola], 4, 800, 6, 680, 8, 680, 10, 460, 12, 400, 16, 250 ) RETURN IF ( NOT ISBLANK ( __mcS5Cob ), __cvS5Cob )
				),
				SELECTCOLUMNS (
				FILTER ( ALL ( ficha_producao ), NOT ISBLANK ( ficha_producao[data_hora_final_debandagem] ) ),
				"E", 6,
				"Dia", VAR __fS6 = ficha_producao[data_hora_final_debandagem] - 320 / 1440 RETURN DATE ( YEAR ( __fS6 ), MONTH ( __fS6 ), DAY ( __fS6 ) ),
				"T", VAR __mS6 = HOUR ( ficha_producao[data_hora_final_debandagem] ) * 60 + MINUTE ( ficha_producao[data_hora_final_debandagem] ) RETURN IF ( __mS6 >= 320 && __mS6 < 837, 1, IF ( __mS6 >= 837 && __mS6 < 1340, 2, 3 ) ),
				"Q", VAR __qS6 = ficha_producao[quantidade_debandagem] RETURN IF ( __qS6 > 2000, BLANK (), __qS6 ),
				"M", VAR __mqS6 = UPPER ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( ficha_producao[Trançadeira], ".", "" ), "-", "" ), " ", "" ), "_", "" ) ) RETURN IF ( __mqS6 IN { "SPIRAL", "TE01", "TE0" }, "SPIRAL", __mqS6 ),
				"Op", SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER ( ficha_producao[operador_debandagem] ),"Á","A"),"À","A"),"Â","A"),"Ã","A"),"Ä","A"),"É","E"),"È","E"),"Ê","E"),"Ë","E"),"Í","I"),"Ì","I"),"Î","I"),"Ï","I"),"Ó","O"),"Ò","O"),"Ô","O"),"Õ","O"),"Ö","O"),"Ú","U"),"Ù","U"),"Û","U"),"Ü","U"),"Ç","C"),"Ñ","N"),".",""),",",""),"-",""),"_",""),"/","|"),
				"Car", VAR __cS6Car = ficha_producao[quantidade_debandagem] VAR __cvS6Car = IF ( __cS6Car > 2000, BLANK (), __cS6Car ) VAR __mcS6Car = SWITCH ( ficha_producao[Bitola], 4, 800, 6, 680, 8, 680, 10, 460, 12, 400, 16, 250 ) RETURN DIVIDE ( __cvS6Car, __mcS6Car ),
				"Cob", VAR __cS6Cob = ficha_producao[quantidade_debandagem] VAR __cvS6Cob = IF ( __cS6Cob > 2000, BLANK (), __cS6Cob ) VAR __mcS6Cob = SWITCH ( ficha_producao[Bitola], 4, 800, 6, 680, 8, 680, 10, 460, 12, 400, 16, 250 ) RETURN IF ( NOT ISBLANK ( __mcS6Cob ), __cvS6Cob )
				),
				SELECTCOLUMNS (
				FILTER ( ALL ( ficha_producao ), NOT ISBLANK ( ficha_producao[data_hora_final_extracao] ) ),
				"E", 7,
				"Dia", VAR __fS7 = ficha_producao[data_hora_final_extracao] - 320 / 1440 RETURN DATE ( YEAR ( __fS7 ), MONTH ( __fS7 ), DAY ( __fS7 ) ),
				"T", VAR __mS7 = HOUR ( ficha_producao[data_hora_final_extracao] ) * 60 + MINUTE ( ficha_producao[data_hora_final_extracao] ) RETURN IF ( __mS7 >= 320 && __mS7 < 837, 1, IF ( __mS7 >= 837 && __mS7 < 1340, 2, 3 ) ),
				"Q", VAR __qS7 = ficha_producao[quantidade_extracao] RETURN IF ( __qS7 > 2000, BLANK (), __qS7 ),
				"M", VAR __mqS7 = UPPER ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( ficha_producao[Trançadeira], ".", "" ), "-", "" ), " ", "" ), "_", "" ) ) RETURN IF ( __mqS7 IN { "SPIRAL", "TE01", "TE0" }, "SPIRAL", __mqS7 ),
				"Op", SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER ( ficha_producao[operador_extracao] ),"Á","A"),"À","A"),"Â","A"),"Ã","A"),"Ä","A"),"É","E"),"È","E"),"Ê","E"),"Ë","E"),"Í","I"),"Ì","I"),"Î","I"),"Ï","I"),"Ó","O"),"Ò","O"),"Ô","O"),"Õ","O"),"Ö","O"),"Ú","U"),"Ù","U"),"Û","U"),"Ü","U"),"Ç","C"),"Ñ","N"),".",""),",",""),"-",""),"_",""),"/","|"),
				"Car", VAR __cS7Car = ficha_producao[quantidade_extracao] VAR __cvS7Car = IF ( __cS7Car > 2000, BLANK (), __cS7Car ) VAR __mcS7Car = SWITCH ( ficha_producao[Bitola], 4, 800, 6, 680, 8, 680, 10, 460, 12, 400, 16, 250 ) RETURN DIVIDE ( __cvS7Car, __mcS7Car ),
				"Cob", VAR __cS7Cob = ficha_producao[quantidade_extracao] VAR __cvS7Cob = IF ( __cS7Cob > 2000, BLANK (), __cS7Cob ) VAR __mcS7Cob = SWITCH ( ficha_producao[Bitola], 4, 800, 6, 680, 8, 680, 10, 460, 12, 400, 16, 250 ) RETURN IF ( NOT ISBLANK ( __mcS7Cob ), __cvS7Cob )
				)
				)
```

## 2) Conferência depois do refresh (DAX query view)
Compara o `__B` antigo (copiado inline, só com o filtro `IN __Datas` trocado por `>= DATE ( 2000, 1, 1 )` para valer sem tela) com a `fFluxoBase`, por etapa (`E`) e mês: linhas, soma de `Q`, contagem distinta de `Op`, soma de `Car` e de `Cob`. Esperado: `Dif` = 0 em todas as linhas.
```dax
EVALUATE
VAR __Old =
UNION (
FILTER (
SELECTCOLUMNS (
FILTER ( ALL ( ficha_producao ), NOT ISBLANK ( ficha_producao[data_hora_final_tubo] ) ),
"@E", 1,
"@Dia", VAR __fS1 = ficha_producao[data_hora_final_tubo] - 320 / 1440 RETURN DATE ( YEAR ( __fS1 ), MONTH ( __fS1 ), DAY ( __fS1 ) ),
"@T", VAR __mS1 = HOUR ( ficha_producao[data_hora_final_tubo] ) * 60 + MINUTE ( ficha_producao[data_hora_final_tubo] ) RETURN IF ( __mS1 >= 320 && __mS1 < 837, 1, IF ( __mS1 >= 837 && __mS1 < 1340, 2, 3 ) ),
"@Q", VAR __qS1 = ficha_producao[quantidade_tubo] RETURN IF ( __qS1 > 2000, BLANK (), __qS1 ),
"@M", VAR __mqS1 = UPPER ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( ficha_producao[Trançadeira], ".", "" ), "-", "" ), " ", "" ), "_", "" ) ) RETURN IF ( __mqS1 IN { "SPIRAL", "TE01", "TE0" }, "SPIRAL", __mqS1 ),
"@Op", SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER ( ficha_producao[operador_tubo] ),"Á","A"),"À","A"),"Â","A"),"Ã","A"),"Ä","A"),"É","E"),"È","E"),"Ê","E"),"Ë","E"),"Í","I"),"Ì","I"),"Î","I"),"Ï","I"),"Ó","O"),"Ò","O"),"Ô","O"),"Õ","O"),"Ö","O"),"Ú","U"),"Ù","U"),"Û","U"),"Ü","U"),"Ç","C"),"Ñ","N"),".",""),",",""),"-",""),"_",""),"/","|"),
"@Car", VAR __cS1Car = ficha_producao[quantidade_tubo] VAR __cvS1Car = IF ( __cS1Car > 2000, BLANK (), __cS1Car ) VAR __mcS1Car = SWITCH ( ficha_producao[Bitola], 4, 800, 6, 680, 8, 680, 10, 460, 12, 400, 16, 250 ) RETURN DIVIDE ( __cvS1Car, __mcS1Car ),
"@Cob", VAR __cS1Cob = ficha_producao[quantidade_tubo] VAR __cvS1Cob = IF ( __cS1Cob > 2000, BLANK (), __cS1Cob ) VAR __mcS1Cob = SWITCH ( ficha_producao[Bitola], 4, 800, 6, 680, 8, 680, 10, 460, 12, 400, 16, 250 ) RETURN IF ( NOT ISBLANK ( __mcS1Cob ), __cvS1Cob )
),
[@Dia] >= DATE ( 2000, 1, 1 )
),
FILTER (
SELECTCOLUMNS (
FILTER ( ALL ( ficha_producao ), NOT ISBLANK ( ficha_producao[data_hora_final_trancadeira] ) ),
"@E", 2,
"@Dia", VAR __fS2 = ficha_producao[data_hora_final_trancadeira] - 320 / 1440 RETURN DATE ( YEAR ( __fS2 ), MONTH ( __fS2 ), DAY ( __fS2 ) ),
"@T", VAR __mS2 = HOUR ( ficha_producao[data_hora_final_trancadeira] ) * 60 + MINUTE ( ficha_producao[data_hora_final_trancadeira] ) RETURN IF ( __mS2 >= 320 && __mS2 < 837, 1, IF ( __mS2 >= 837 && __mS2 < 1340, 2, 3 ) ),
"@Q", VAR __qS2 = ficha_producao[quantidade_trancagem] RETURN IF ( __qS2 > 2000, BLANK (), __qS2 ),
"@M", VAR __mqS2 = UPPER ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( ficha_producao[Trançadeira], ".", "" ), "-", "" ), " ", "" ), "_", "" ) ) RETURN IF ( __mqS2 IN { "SPIRAL", "TE01", "TE0" }, "SPIRAL", __mqS2 ),
"@Op", SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER ( ficha_producao[operador_trancagem] ),"Á","A"),"À","A"),"Â","A"),"Ã","A"),"Ä","A"),"É","E"),"È","E"),"Ê","E"),"Ë","E"),"Í","I"),"Ì","I"),"Î","I"),"Ï","I"),"Ó","O"),"Ò","O"),"Ô","O"),"Õ","O"),"Ö","O"),"Ú","U"),"Ù","U"),"Û","U"),"Ü","U"),"Ç","C"),"Ñ","N"),".",""),",",""),"-",""),"_",""),"/","|"),
"@Car", VAR __cS2Car = ficha_producao[quantidade_trancagem] VAR __cvS2Car = IF ( __cS2Car > 2000, BLANK (), __cS2Car ) VAR __mcS2Car = SWITCH ( ficha_producao[Bitola], 4, 800, 6, 680, 8, 680, 10, 460, 12, 400, 16, 250 ) RETURN DIVIDE ( __cvS2Car, __mcS2Car ),
"@Cob", VAR __cS2Cob = ficha_producao[quantidade_trancagem] VAR __cvS2Cob = IF ( __cS2Cob > 2000, BLANK (), __cS2Cob ) VAR __mcS2Cob = SWITCH ( ficha_producao[Bitola], 4, 800, 6, 680, 8, 680, 10, 460, 12, 400, 16, 250 ) RETURN IF ( NOT ISBLANK ( __mcS2Cob ), __cvS2Cob )
),
[@Dia] >= DATE ( 2000, 1, 1 )
),
FILTER (
SELECTCOLUMNS (
FILTER ( ALL ( ficha_producao ), NOT ISBLANK ( ficha_producao[data_hora_final_cobertura] ) ),
"@E", 3,
"@Dia", VAR __fS3 = ficha_producao[data_hora_final_cobertura] - 320 / 1440 RETURN DATE ( YEAR ( __fS3 ), MONTH ( __fS3 ), DAY ( __fS3 ) ),
"@T", VAR __mS3 = HOUR ( ficha_producao[data_hora_final_cobertura] ) * 60 + MINUTE ( ficha_producao[data_hora_final_cobertura] ) RETURN IF ( __mS3 >= 320 && __mS3 < 837, 1, IF ( __mS3 >= 837 && __mS3 < 1340, 2, 3 ) ),
"@Q", VAR __qS3 = ficha_producao[quantidade_cobertura] RETURN IF ( __qS3 > 2000, BLANK (), __qS3 ),
"@M", VAR __mqS3 = UPPER ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( ficha_producao[Trançadeira], ".", "" ), "-", "" ), " ", "" ), "_", "" ) ) RETURN IF ( __mqS3 IN { "SPIRAL", "TE01", "TE0" }, "SPIRAL", __mqS3 ),
"@Op", SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER ( ficha_producao[operador_cobertura] ),"Á","A"),"À","A"),"Â","A"),"Ã","A"),"Ä","A"),"É","E"),"È","E"),"Ê","E"),"Ë","E"),"Í","I"),"Ì","I"),"Î","I"),"Ï","I"),"Ó","O"),"Ò","O"),"Ô","O"),"Õ","O"),"Ö","O"),"Ú","U"),"Ù","U"),"Û","U"),"Ü","U"),"Ç","C"),"Ñ","N"),".",""),",",""),"-",""),"_",""),"/","|"),
"@Car", VAR __cS3Car = ficha_producao[quantidade_cobertura] VAR __cvS3Car = IF ( __cS3Car > 2000, BLANK (), __cS3Car ) VAR __mcS3Car = SWITCH ( ficha_producao[Bitola], 4, 800, 6, 680, 8, 680, 10, 460, 12, 400, 16, 250 ) RETURN DIVIDE ( __cvS3Car, __mcS3Car ),
"@Cob", VAR __cS3Cob = ficha_producao[quantidade_cobertura] VAR __cvS3Cob = IF ( __cS3Cob > 2000, BLANK (), __cS3Cob ) VAR __mcS3Cob = SWITCH ( ficha_producao[Bitola], 4, 800, 6, 680, 8, 680, 10, 460, 12, 400, 16, 250 ) RETURN IF ( NOT ISBLANK ( __mcS3Cob ), __cvS3Cob )
),
[@Dia] >= DATE ( 2000, 1, 1 )
),
FILTER (
SELECTCOLUMNS (
FILTER ( ALL ( ficha_producao ), NOT ISBLANK ( ficha_producao[data_hora_final_bandagem] ) ),
"@E", 4,
"@Dia", VAR __fS4 = ficha_producao[data_hora_final_bandagem] - 320 / 1440 RETURN DATE ( YEAR ( __fS4 ), MONTH ( __fS4 ), DAY ( __fS4 ) ),
"@T", VAR __mS4 = HOUR ( ficha_producao[data_hora_final_bandagem] ) * 60 + MINUTE ( ficha_producao[data_hora_final_bandagem] ) RETURN IF ( __mS4 >= 320 && __mS4 < 837, 1, IF ( __mS4 >= 837 && __mS4 < 1340, 2, 3 ) ),
"@Q", VAR __qS4 = ficha_producao[quantidade_bandagem] RETURN IF ( __qS4 > 2000, BLANK (), __qS4 ),
"@M", VAR __mqS4 = UPPER ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( ficha_producao[Trançadeira], ".", "" ), "-", "" ), " ", "" ), "_", "" ) ) RETURN IF ( __mqS4 IN { "SPIRAL", "TE01", "TE0" }, "SPIRAL", __mqS4 ),
"@Op", SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER ( ficha_producao[operador_bandagem] ),"Á","A"),"À","A"),"Â","A"),"Ã","A"),"Ä","A"),"É","E"),"È","E"),"Ê","E"),"Ë","E"),"Í","I"),"Ì","I"),"Î","I"),"Ï","I"),"Ó","O"),"Ò","O"),"Ô","O"),"Õ","O"),"Ö","O"),"Ú","U"),"Ù","U"),"Û","U"),"Ü","U"),"Ç","C"),"Ñ","N"),".",""),",",""),"-",""),"_",""),"/","|"),
"@Car", VAR __cS4Car = ficha_producao[quantidade_bandagem] VAR __cvS4Car = IF ( __cS4Car > 2000, BLANK (), __cS4Car ) VAR __mcS4Car = SWITCH ( ficha_producao[Bitola], 4, 800, 6, 680, 8, 680, 10, 460, 12, 400, 16, 250 ) RETURN DIVIDE ( __cvS4Car, __mcS4Car ),
"@Cob", VAR __cS4Cob = ficha_producao[quantidade_bandagem] VAR __cvS4Cob = IF ( __cS4Cob > 2000, BLANK (), __cS4Cob ) VAR __mcS4Cob = SWITCH ( ficha_producao[Bitola], 4, 800, 6, 680, 8, 680, 10, 460, 12, 400, 16, 250 ) RETURN IF ( NOT ISBLANK ( __mcS4Cob ), __cvS4Cob )
),
[@Dia] >= DATE ( 2000, 1, 1 )
),
FILTER (
SELECTCOLUMNS (
FILTER ( ALL ( ficha_producao ), NOT ISBLANK ( ficha_producao[data_hora_final_vulcanizacao] ) ),
"@E", 5,
"@Dia", VAR __fS5 = ficha_producao[data_hora_final_vulcanizacao] - 320 / 1440 RETURN DATE ( YEAR ( __fS5 ), MONTH ( __fS5 ), DAY ( __fS5 ) ),
"@T", VAR __mS5 = HOUR ( ficha_producao[data_hora_final_vulcanizacao] ) * 60 + MINUTE ( ficha_producao[data_hora_final_vulcanizacao] ) RETURN IF ( __mS5 >= 320 && __mS5 < 837, 1, IF ( __mS5 >= 837 && __mS5 < 1340, 2, 3 ) ),
"@Q", VAR __qS5 = ficha_producao[quantidade_vulcanizacao] RETURN IF ( __qS5 > 2000, BLANK (), __qS5 ),
"@M", VAR __mqS5 = UPPER ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( ficha_producao[Trançadeira], ".", "" ), "-", "" ), " ", "" ), "_", "" ) ) RETURN IF ( __mqS5 IN { "SPIRAL", "TE01", "TE0" }, "SPIRAL", __mqS5 ),
"@Op", SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER ( ficha_producao[operador_vulcanizacao] ),"Á","A"),"À","A"),"Â","A"),"Ã","A"),"Ä","A"),"É","E"),"È","E"),"Ê","E"),"Ë","E"),"Í","I"),"Ì","I"),"Î","I"),"Ï","I"),"Ó","O"),"Ò","O"),"Ô","O"),"Õ","O"),"Ö","O"),"Ú","U"),"Ù","U"),"Û","U"),"Ü","U"),"Ç","C"),"Ñ","N"),".",""),",",""),"-",""),"_",""),"/","|"),
"@Car", VAR __cS5Car = ficha_producao[quantidade_vulcanizacao] VAR __cvS5Car = IF ( __cS5Car > 2000, BLANK (), __cS5Car ) VAR __mcS5Car = SWITCH ( ficha_producao[Bitola], 4, 800, 6, 680, 8, 680, 10, 460, 12, 400, 16, 250 ) RETURN DIVIDE ( __cvS5Car, __mcS5Car ),
"@Cob", VAR __cS5Cob = ficha_producao[quantidade_vulcanizacao] VAR __cvS5Cob = IF ( __cS5Cob > 2000, BLANK (), __cS5Cob ) VAR __mcS5Cob = SWITCH ( ficha_producao[Bitola], 4, 800, 6, 680, 8, 680, 10, 460, 12, 400, 16, 250 ) RETURN IF ( NOT ISBLANK ( __mcS5Cob ), __cvS5Cob )
),
[@Dia] >= DATE ( 2000, 1, 1 )
),
FILTER (
SELECTCOLUMNS (
FILTER ( ALL ( ficha_producao ), NOT ISBLANK ( ficha_producao[data_hora_final_debandagem] ) ),
"@E", 6,
"@Dia", VAR __fS6 = ficha_producao[data_hora_final_debandagem] - 320 / 1440 RETURN DATE ( YEAR ( __fS6 ), MONTH ( __fS6 ), DAY ( __fS6 ) ),
"@T", VAR __mS6 = HOUR ( ficha_producao[data_hora_final_debandagem] ) * 60 + MINUTE ( ficha_producao[data_hora_final_debandagem] ) RETURN IF ( __mS6 >= 320 && __mS6 < 837, 1, IF ( __mS6 >= 837 && __mS6 < 1340, 2, 3 ) ),
"@Q", VAR __qS6 = ficha_producao[quantidade_debandagem] RETURN IF ( __qS6 > 2000, BLANK (), __qS6 ),
"@M", VAR __mqS6 = UPPER ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( ficha_producao[Trançadeira], ".", "" ), "-", "" ), " ", "" ), "_", "" ) ) RETURN IF ( __mqS6 IN { "SPIRAL", "TE01", "TE0" }, "SPIRAL", __mqS6 ),
"@Op", SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER ( ficha_producao[operador_debandagem] ),"Á","A"),"À","A"),"Â","A"),"Ã","A"),"Ä","A"),"É","E"),"È","E"),"Ê","E"),"Ë","E"),"Í","I"),"Ì","I"),"Î","I"),"Ï","I"),"Ó","O"),"Ò","O"),"Ô","O"),"Õ","O"),"Ö","O"),"Ú","U"),"Ù","U"),"Û","U"),"Ü","U"),"Ç","C"),"Ñ","N"),".",""),",",""),"-",""),"_",""),"/","|"),
"@Car", VAR __cS6Car = ficha_producao[quantidade_debandagem] VAR __cvS6Car = IF ( __cS6Car > 2000, BLANK (), __cS6Car ) VAR __mcS6Car = SWITCH ( ficha_producao[Bitola], 4, 800, 6, 680, 8, 680, 10, 460, 12, 400, 16, 250 ) RETURN DIVIDE ( __cvS6Car, __mcS6Car ),
"@Cob", VAR __cS6Cob = ficha_producao[quantidade_debandagem] VAR __cvS6Cob = IF ( __cS6Cob > 2000, BLANK (), __cS6Cob ) VAR __mcS6Cob = SWITCH ( ficha_producao[Bitola], 4, 800, 6, 680, 8, 680, 10, 460, 12, 400, 16, 250 ) RETURN IF ( NOT ISBLANK ( __mcS6Cob ), __cvS6Cob )
),
[@Dia] >= DATE ( 2000, 1, 1 )
),
FILTER (
SELECTCOLUMNS (
FILTER ( ALL ( ficha_producao ), NOT ISBLANK ( ficha_producao[data_hora_final_extracao] ) ),
"@E", 7,
"@Dia", VAR __fS7 = ficha_producao[data_hora_final_extracao] - 320 / 1440 RETURN DATE ( YEAR ( __fS7 ), MONTH ( __fS7 ), DAY ( __fS7 ) ),
"@T", VAR __mS7 = HOUR ( ficha_producao[data_hora_final_extracao] ) * 60 + MINUTE ( ficha_producao[data_hora_final_extracao] ) RETURN IF ( __mS7 >= 320 && __mS7 < 837, 1, IF ( __mS7 >= 837 && __mS7 < 1340, 2, 3 ) ),
"@Q", VAR __qS7 = ficha_producao[quantidade_extracao] RETURN IF ( __qS7 > 2000, BLANK (), __qS7 ),
"@M", VAR __mqS7 = UPPER ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( ficha_producao[Trançadeira], ".", "" ), "-", "" ), " ", "" ), "_", "" ) ) RETURN IF ( __mqS7 IN { "SPIRAL", "TE01", "TE0" }, "SPIRAL", __mqS7 ),
"@Op", SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER ( ficha_producao[operador_extracao] ),"Á","A"),"À","A"),"Â","A"),"Ã","A"),"Ä","A"),"É","E"),"È","E"),"Ê","E"),"Ë","E"),"Í","I"),"Ì","I"),"Î","I"),"Ï","I"),"Ó","O"),"Ò","O"),"Ô","O"),"Õ","O"),"Ö","O"),"Ú","U"),"Ù","U"),"Û","U"),"Ü","U"),"Ç","C"),"Ñ","N"),".",""),",",""),"-",""),"_",""),"/","|"),
"@Car", VAR __cS7Car = ficha_producao[quantidade_extracao] VAR __cvS7Car = IF ( __cS7Car > 2000, BLANK (), __cS7Car ) VAR __mcS7Car = SWITCH ( ficha_producao[Bitola], 4, 800, 6, 680, 8, 680, 10, 460, 12, 400, 16, 250 ) RETURN DIVIDE ( __cvS7Car, __mcS7Car ),
"@Cob", VAR __cS7Cob = ficha_producao[quantidade_extracao] VAR __cvS7Cob = IF ( __cS7Cob > 2000, BLANK (), __cS7Cob ) VAR __mcS7Cob = SWITCH ( ficha_producao[Bitola], 4, 800, 6, 680, 8, 680, 10, 460, 12, 400, 16, 250 ) RETURN IF ( NOT ISBLANK ( __mcS7Cob ), __cvS7Cob )
),
[@Dia] >= DATE ( 2000, 1, 1 )
)
)
VAR __Chaves =
DISTINCT (
SELECTCOLUMNS (
__Old,
"E", [@E],
"Mes", DATE ( YEAR ( [@Dia] ), MONTH ( [@Dia] ), 1 )
)
)
VAR __Res =
ADDCOLUMNS (
__Chaves,
"LinhasAntes", VAR __e = [E] VAR __m = [Mes] RETURN COUNTROWS ( FILTER ( __Old, [@E] = __e && DATE ( YEAR ( [@Dia] ), MONTH ( [@Dia] ), 1 ) = __m ) ),
"LinhasDepois", VAR __e = [E] VAR __m = [Mes] RETURN COUNTROWS ( FILTER ( fFluxoBase, fFluxoBase[E] = __e && DATE ( YEAR ( fFluxoBase[Dia] ), MONTH ( fFluxoBase[Dia] ), 1 ) = __m ) ),
"QAntes", VAR __e = [E] VAR __m = [Mes] RETURN SUMX ( FILTER ( __Old, [@E] = __e && DATE ( YEAR ( [@Dia] ), MONTH ( [@Dia] ), 1 ) = __m ), [@Q] ),
"QDepois", VAR __e = [E] VAR __m = [Mes] RETURN SUMX ( FILTER ( fFluxoBase, fFluxoBase[E] = __e && DATE ( YEAR ( fFluxoBase[Dia] ), MONTH ( fFluxoBase[Dia] ), 1 ) = __m ), fFluxoBase[Q] ),
"OpAntes", VAR __e = [E] VAR __m = [Mes] RETURN COUNTROWS ( DISTINCT ( SELECTCOLUMNS ( FILTER ( __Old, [@E] = __e && DATE ( YEAR ( [@Dia] ), MONTH ( [@Dia] ), 1 ) = __m ), "x", [@Op] ) ) ),
"OpDepois", VAR __e = [E] VAR __m = [Mes] RETURN COUNTROWS ( DISTINCT ( SELECTCOLUMNS ( FILTER ( fFluxoBase, fFluxoBase[E] = __e && DATE ( YEAR ( fFluxoBase[Dia] ), MONTH ( fFluxoBase[Dia] ), 1 ) = __m ), "x", fFluxoBase[Op] ) ) ),
"CarAntes", VAR __e = [E] VAR __m = [Mes] RETURN SUMX ( FILTER ( __Old, [@E] = __e && DATE ( YEAR ( [@Dia] ), MONTH ( [@Dia] ), 1 ) = __m ), [@Car] ),
"CarDepois", VAR __e = [E] VAR __m = [Mes] RETURN SUMX ( FILTER ( fFluxoBase, fFluxoBase[E] = __e && DATE ( YEAR ( fFluxoBase[Dia] ), MONTH ( fFluxoBase[Dia] ), 1 ) = __m ), fFluxoBase[Car] ),
"CobAntes", VAR __e = [E] VAR __m = [Mes] RETURN SUMX ( FILTER ( __Old, [@E] = __e && DATE ( YEAR ( [@Dia] ), MONTH ( [@Dia] ), 1 ) = __m ), [@Cob] ),
"CobDepois", VAR __e = [E] VAR __m = [Mes] RETURN SUMX ( FILTER ( fFluxoBase, fFluxoBase[E] = __e && DATE ( YEAR ( fFluxoBase[Dia] ), MONTH ( fFluxoBase[Dia] ), 1 ) = __m ), fFluxoBase[Cob] )
)
RETURN
ADDCOLUMNS (
__Res,
"Dif", ABS ( [LinhasAntes] - [LinhasDepois] ) + ABS ( [QAntes] - [QDepois] ) + ABS ( [OpAntes] - [OpDepois] ) + ABS ( [CarAntes] - [CarDepois] ) + ABS ( [CobAntes] - [CobDepois] )
)
ORDER BY [E], [Mes]
```

Conferência extra: `EVALUATE ROW ( "Linhas", COUNTROWS ( fFluxoBase ) )` deve bater com a soma de `LinhasAntes`.
