# fHoraCheia, dTurno e Turno BI da Montagem: BI em hora cheia (MEL-267) — PENDENTE DE APLICAR (só com o "Libero" do William, no TMDL view do modelo vivo)

Só BI. O app, a lista Hora-Hora e a `fHoraHora` não mudam. Regra: seção 1 de `GMS/Analises/BI_HoraCheia/PLANO.md`; protótipo e números de conferência em `GMS/Analises/BI_HoraCheia/prototipo_hora_cheia.py` e `conferencia_prototipo.md`.

## Como o início absoluto da janela é calculado
Cada linha da `fHoraHora` é uma janela (`Hora` = "hh:mm - hh:mm"). O início sai do rótulo em minutos desde 00:00 do dia `Data` (`I0`); se for menor que 05:20 é madrugada do 3º turno e soma 1440 (a mesma regra da `HoraOrdem` da base), exceto `13:47 - 15:00`, que vale 13:57 (837). Subtraindo 300 (05:00) o início vira um deslocamento `S` dentro do dia produtivo que começa às 05:00 de `Data`; o fim `E` sai do mesmo jeito e, se ficar menor ou igual a `S`, soma 1440. A hora cheia `k` = `INT(S/60)` até `INT((E−1)/60)`: cada `k` é uma fatia, com `Fração` = minutos de sobreposição ÷ (`E − S`). `Data BI` = `Data + INT(k/24)` e `HoraOrdem` = `MOD(k, 24)` (0 = 05:00 … 23 = 04:00). Por isso a janela `05:00 - 05:20`, que a base grava com a `Data` do dia em que o 3º turno começou, tem `S = 1440`, cai em `k = 24` e vai para o dia D+1, hora 05:00-06:00, junto com a `05:20 - 06:00` desse dia; as outras janelas da madrugada (00:00 a 05:00) ficam no dia D. A janela `13:47 - 15:00` (63 min) dá 3/63 à hora 13:00 e 60/63 à 14:00; a hora extra `22:20 - 23:20` dá 40/60 à hora 22:00 e 20/60 à 23:00. Meta, Real e Parado são multiplicados pela `Fração`; o Parado nunca passa dos minutos da fatia; a Meta da janela com `Motivo Padrão` = "Almoço" perde 45 min antes do rateio (`Meta Hora × máx(0, Minutos − 45) ÷ Minutos`). O `Turno BI` vem da `HoraOrdem`: 0-8 = 1º, 9-16 = 2º, 17-23 = 3º.

## Antes de colar
- Digite no TMDL view **sem indentação à esquerda** e use `Tab`/`shift+Tab` para a estrutura (seção 7 do `COMO_ARRUMAR_HORAHORA.md`). A expressão DAX abaixo está toda em linhas sem recuo interno de propósito: cada linha vai no mesmo nível (4 tabs). `Escape` depois de cada linha digitada fecha o autocompletar; não use Enter sobre a sugestão.
- Se o editor reclamar de "Turno BI" não resolvido nas colunas novas ou de `dTurno` nos relacionamentos, é esperado: as peças nascem no mesmo script.
- Se já existir uma `dTurno` no modelo vivo (a `montagem_modelo.md` propunha uma; no TMDL local ela não existe), o `createOrReplace` a substitui e pode soltar os relacionamentos dela com `dMetaMontagem`: confira antes com o botão direito na tabela e refaça se houver.
- A tabela calculada só tem valor depois de um **refresh**. Consulta antes dá "needs to be recalculated or refreshed".
- Sem `IFERROR` em volta de `VALUE` o refresh quebra se algum `Hora` vier malformado; aqui já está protegido (`IFERROR(..., -1)` e o filtro descarta a linha).

## 1) Script TMDL (cole inteiro)
```
createOrReplace

	table fHoraCheia

		/// Hora-Hora do BI por hora cheia: 1 linha por Célula x Data BI x hora cheia x janela de origem (fHoraHora). Dia produtivo 05:00 a 05:00.
		column 'Célula'
			dataType: string
			summarizeBy: none
			sourceColumn: [Célula]

		column Mangueira
			dataType: string
			summarizeBy: none
			sourceColumn: [Mangueira]

		column 'Data BI'
			dataType: dateTime
			formatString: dd/mm/yyyy
			summarizeBy: none
			sourceColumn: [Data BI]

		column 'Turno BI'
			dataType: string
			summarizeBy: none
			sourceColumn: [Turno BI]

		column Hora
			dataType: string
			summarizeBy: none
			sortByColumn: HoraOrdem
			sourceColumn: [Hora]

		column HoraOrdem
			dataType: int64
			isHidden
			formatString: 0
			summarizeBy: none
			sourceColumn: [HoraOrdem]

		column Minutos
			dataType: double
			formatString: #,0.0
			summarizeBy: none
			sourceColumn: [Minutos]

		column Meta
			dataType: double
			formatString: #,0.0
			summarizeBy: none
			sourceColumn: [Meta]

		column Real
			dataType: double
			formatString: #,0.0
			summarizeBy: none
			sourceColumn: [Real]

		column Parado
			dataType: double
			formatString: #,0.0
			summarizeBy: none
			sourceColumn: [Parado]

		column Motivo
			dataType: string
			summarizeBy: none
			sourceColumn: [Motivo]

		column 'Motivo Padrão'
			dataType: string
			summarizeBy: none
			sourceColumn: [Motivo Padrão]

		column 'Motivo 2'
			dataType: string
			summarizeBy: none
			sourceColumn: [Motivo 2]

		column 'Motivo 2 Padrão'
			dataType: string
			summarizeBy: none
			sourceColumn: [Motivo 2 Padrão]

		column 'ID Origem'
			dataType: int64
			formatString: 0
			summarizeBy: none
			sourceColumn: [ID Origem]

		column Fração
			dataType: double
			formatString: 0.000
			summarizeBy: none
			sourceColumn: [Fração]

		partition fHoraCheia = calculated
			mode: import
			source =
				VAR Linhas =
				SELECTCOLUMNS (
				fHoraHora,
				"ID Origem", fHoraHora[ID],
				"Célula", fHoraHora[Célula],
				"Mangueira", fHoraHora[Mangueira],
				"Data", fHoraHora[Data],
				"Hora", fHoraHora[Hora],
				"Min", fHoraHora[Minutos],
				"MetaHora", fHoraHora[Meta Hora],
				"Real0", fHoraHora[Real. Hora],
				"Par0", fHoraHora[Tempo Parado (min)],
				"Motivo", fHoraHora[Motivo],
				"Motivo Padrão", fHoraHora[Motivo Padrão],
				"Motivo 2", fHoraHora[Motivo 2],
				"Motivo 2 Padrão", fHoraHora[Motivo 2 Padrão]
				)
				VAR Ini =
				ADDCOLUMNS (
				FILTER ( Linhas, LEN ( [Hora] ) = 13 ),
				"I0", IFERROR ( VALUE ( LEFT ( [Hora], 2 ) ) * 60 + VALUE ( MID ( [Hora], 4, 2 ) ), -1 ),
				"F0", IFERROR ( VALUE ( MID ( [Hora], 9, 2 ) ) * 60 + VALUE ( MID ( [Hora], 12, 2 ) ), -1 )
				)
				VAR Jan1 =
				ADDCOLUMNS (
				FILTER ( Ini, [I0] >= 0 && [F0] >= 0 ),
				"Sini", IF ( [Hora] = "13:47 - 15:00", 837, IF ( [I0] < 320, [I0] + 1440, [I0] ) ) - 300
				)
				VAR Jan2 =
				ADDCOLUMNS (
				Jan1,
				"Efim", IF ( [F0] - 300 <= [Sini], [F0] - 300 + 1440, [F0] - 300 )
				)
				VAR Fatias =
				GENERATE (
				FILTER ( Jan2, [Efim] - [Sini] > 0 && [Efim] - [Sini] <= 120 ),
				GENERATESERIES ( INT ( [Sini] / 60 ), INT ( ( [Efim] - 1 ) / 60 ) )
				)
				VAR Calc =
				ADDCOLUMNS (
				Fatias,
				"Fr", DIVIDE ( MIN ( [Efim], ( [Value] + 1 ) * 60 ) - MAX ( [Sini], [Value] * 60 ), [Efim] - [Sini] )
				)
				RETURN
				SELECTCOLUMNS (
				Calc,
				"Célula", [Célula],
				"Mangueira", [Mangueira],
				"Data BI", [Data] + INT ( [Value] / 24 ),
				"Turno BI", IF ( MOD ( [Value], 24 ) < 9, "1º Turno", IF ( MOD ( [Value], 24 ) < 17, "2º Turno", "3º Turno" ) ),
				"Hora", FORMAT ( MOD ( 5 + MOD ( [Value], 24 ), 24 ), "00" ) & ":00 - " & FORMAT ( MOD ( 6 + MOD ( [Value], 24 ), 24 ), "00" ) & ":00",
				"HoraOrdem", MOD ( [Value], 24 ),
				"Minutos", COALESCE ( [Min], 0 ) * [Fr],
				"Meta", COALESCE ( [MetaHora], 0 ) * IF ( [Motivo Padrão] = "Almoço" && COALESCE ( [Min], 0 ) > 0, MAX ( 0, [Min] - 45 ) / [Min], 1 ) * [Fr],
				"Real", COALESCE ( [Real0], 0 ) * [Fr],
				"Parado", MIN ( COALESCE ( [Par0], 0 ) * [Fr], COALESCE ( [Min], 0 ) * [Fr] ),
				"Motivo", [Motivo],
				"Motivo Padrão", [Motivo Padrão],
				"Motivo 2", [Motivo 2],
				"Motivo 2 Padrão", [Motivo 2 Padrão],
				"ID Origem", [ID Origem],
				"Fração", [Fr]
				)

	table dTurno

		/// Dimensão de turno do BI (mesmo texto de fHoraCheia[Turno BI], Producao_Montagem[Turno BI] e Paradas_Montagem[Turno BI]).
		column Turno
			dataType: string
			summarizeBy: none
			sortByColumn: Ordem
			sourceColumn: [Turno]

		column Ordem
			dataType: int64
			isHidden
			formatString: 0
			summarizeBy: none
			sourceColumn: [Ordem]

		partition dTurno = calculated
			mode: import
			source =
				DATATABLE (
				"Turno", STRING,
				"Ordem", INTEGER,
				{
				{ "1º Turno", 1 },
				{ "2º Turno", 2 },
				{ "3º Turno", 3 }
				}
				)

	ref table Producao_Montagem

		/// Turno sem o espaço à esquerda que chega da fonte.
		column 'Turno BI' =
				TRIM ( Producao_Montagem[Turno] )
			dataType: string
			summarizeBy: none

	ref table Paradas_Montagem

		/// Turno sem o espaço à esquerda que chega da fonte.
		column 'Turno BI' =
				TRIM ( Paradas_Montagem[Turno] )
			dataType: string
			summarizeBy: none

	relationship fHoraCheia_DataBI
		fromColumn: fHoraCheia.'Data BI'
		toColumn: dCalendario.Date

	relationship dTurno_fHoraCheia
		fromColumn: fHoraCheia.'Turno BI'
		toColumn: dTurno.Turno

	relationship dTurno_Producao_Montagem
		fromColumn: Producao_Montagem.'Turno BI'
		toColumn: dTurno.Turno

	relationship dTurno_Paradas_Montagem
		fromColumn: Paradas_Montagem.'Turno BI'
		toColumn: dTurno.Turno
```
Os quatro relacionamentos ficam muitos-para-um (do lado da `fHoraCheia`/Montagem para a dimensão) e filtro único (dimensão filtra a fato), que é o padrão do TMDL sem `crossFilteringBehavior`.

Observações do script:
- Colunas além das pedidas: `HoraOrdem` (oculta, necessária para ordenar `Hora`; não lê `Hora`, então não há a dependência circular da `Hora BI`) e `Ordem` na `dTurno` (oculta, ordena o `Turno`).
- `Parado` mantém o valor da linha de Almoço (os minutos da refeição). A refeição sai de Parado e de Principal parada nas **medidas**, filtrando `fHoraCheia[Motivo Padrão]` com `KEEPFILTERS`, como hoje.
- `Meta` já vem com o desconto do almoço; o 1295/1440 do cartão continua nas medidas, só sem hora filtrada.
- Se a `Producao_Montagem` ou a `Paradas_Montagem` chegar com `Turno` em maiúsculas (passo `Text.Upper` da `montagem_modelo.md`), o relacionamento ainda casa (a comparação do modelo não diferencia caixa); a `dTurno` mostra "1º Turno".

## 2) Verificação depois do refresh
1. DAX query view: a conferência abaixo, comparada com a tabela "Depois" do `conferencia_prototipo.md` (TH07, dia produtivo 24/09/2026). O backup do protótipo é de 15/10; se a lista foi corrigida depois (MEL-243, duplicatas), os números do BI podem divergir só por isso: rode também a consulta de totais para ver a diferença contra a `fHoraHora`.
2. `INFO.COLUMNS()` e `INFO.MEASURES()` com `[State] <> 1` devem devolver 0 linhas.

```
// 2a) TH07, dia produtivo 24/09/2026, por hora cheia (comparar com o protótipo)
EVALUATE
CALCULATETABLE (
    SUMMARIZECOLUMNS (
        fHoraCheia[Turno BI],
        fHoraCheia[HoraOrdem],
        fHoraCheia[Hora],
        "Min", SUM ( fHoraCheia[Minutos] ),
        "Meta", SUM ( fHoraCheia[Meta] ),
        "Real", SUM ( fHoraCheia[Real] ),
        "Parado", SUM ( fHoraCheia[Parado] )
    ),
    fHoraCheia[Célula] = "TH07",
    fHoraCheia[Data BI] = DATE ( 2026, 9, 24 )
)
ORDER BY fHoraCheia[HoraOrdem]

// 2b) mesmo dia por turno BI (protótipo: 1º min 540 meta 1881,4 real 1084 parado 242,9; 2º min 480 meta 1652,6 real 746 parado 252,1; 3º min 480 meta 1653 real 890 parado 0)
EVALUATE
CALCULATETABLE (
    SUMMARIZECOLUMNS (
        dTurno[Turno],
        "Min", SUM ( fHoraCheia[Minutos] ),
        "Meta", SUM ( fHoraCheia[Meta] ),
        "Real", SUM ( fHoraCheia[Real] ),
        "Parado", SUM ( fHoraCheia[Parado] )
    ),
    fHoraCheia[Célula] = "TH07",
    fHoraCheia[Data BI] = DATE ( 2026, 9, 24 )
)
ORDER BY dTurno[Turno]

// 2c) totais gerais: Real, Parado e Minutos devem ser iguais; Meta = base menos o desconto do almoço (45 min por janela de Almoço)
EVALUATE
ROW (
    "Real HC", SUM ( fHoraCheia[Real] ),
    "Real HH", SUM ( fHoraHora[Real. Hora] ),
    "Parado HC", SUM ( fHoraCheia[Parado] ),
    "Parado HH", SUM ( fHoraHora[Tempo Parado (min)] ),
    "Min HC", SUM ( fHoraCheia[Minutos] ),
    "Min HH", SUM ( fHoraHora[Minutos] ),
    "Meta HC", SUM ( fHoraCheia[Meta] ),
    "Meta HH", SUM ( fHoraHora[Meta Hora] ),
    "Linhas HC", COUNTROWS ( fHoraCheia ),
    "Linhas HH", COUNTROWS ( fHoraHora )
)

// 2d) objetos com problema (deve voltar vazio)
EVALUATE FILTER ( INFO.COLUMNS (), [State] <> 1 )
```
No backup de set–out/2026 o protótipo deu 4.024 linhas na base e 4.244 na `fHoraCheia`; no modelo vivo o total é maior (a lista tem ~23,8 mil linhas), então compare os números por dia e máquina, não o total.
