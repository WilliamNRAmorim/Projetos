# fHoraHora: Hora-Hora completo no modelo (GMS) — PENDENTE DE APLICAR (William cola no TMDL view do serviço)

## Por que
A tabela `Hora-Hora` do modelo só guarda as linhas COM motivo de parada e não tem Hora, Meta Hora, Real. Hora nem
Mangueira. A página "Hora-Hora Trançagem" precisa da hora inteira (todas as janelas, com ou sem parada).
A `Hora-Hora` não é alterada: ela segue servindo o Pareto (Disponibilidade, % Tempo Parado, Paradas).

## Antes de colar
- A partição abaixo busca a lista por `Name = "Hora-Hora"`. Se der "Key didn't match any rows" (já aconteceu na
  Extrusora, MEL-244), troque pelo Id da lista, o mesmo que está na partição da `Hora-Hora`:
  `Origem{[Id = "<id da lista>"]}[Items]`.
- Se o nome `fHoraHora` já existir no documento M, recusa com "duplicate member": use `fHoraHora2` e me avise.

## 1) Tabela e colunas
```
createOrReplace

	table fHoraHora
		lineageTag: 3d0e7a52-9b14-4c68-8f21-6a5b0c1d7e90

		/// Hora-Hora completo (1 linha por Célula x Data x Turno x Hora), com ou sem parada. Fonte: lista Hora-Hora.
		column ID
			dataType: int64
			formatString: 0
			summarizeBy: none
			sourceColumn: ID
		column Data
			dataType: dateTime
			formatString: dd/mm/yyyy
			summarizeBy: none
			sourceColumn: Data
		column Turno
			dataType: string
			summarizeBy: none
			sourceColumn: Turno
		column Célula
			dataType: string
			summarizeBy: none
			sourceColumn: Célula
		column Hora
			dataType: string
			summarizeBy: none
			sortByColumn: HoraOrdem
			sourceColumn: Hora
		column Mangueira
			dataType: string
			summarizeBy: none
			sourceColumn: Mangueira
		column Minutos
			dataType: double
			summarizeBy: none
			sourceColumn: Minutos
		column 'Meta Hora'
			dataType: double
			formatString: #,0
			summarizeBy: none
			sourceColumn: Meta Hora
		column 'Real. Hora'
			dataType: double
			formatString: #,0
			summarizeBy: none
			sourceColumn: Real. Hora
		column 'Tempo Parado (min)'
			dataType: double
			formatString: #,0.0
			summarizeBy: none
			sourceColumn: Tempo Parado (min)
		column Motivo
			dataType: string
			summarizeBy: none
			sourceColumn: Motivo
		column 'Motivo 2'
			dataType: string
			summarizeBy: none
			sourceColumn: Motivo 2
		column Status
			dataType: string
			summarizeBy: none
			sourceColumn: Status

		/// Ordem da janela dentro do turno (minutos desde 00:00; madrugada do 3º turno soma 24h).
		column HoraOrdem
			dataType: int64
			isHidden
			summarizeBy: none
			expression =
				VAR h = VALUE ( LEFT ( 'fHoraHora'[Hora], 2 ) ) * 60 + VALUE ( MID ( 'fHoraHora'[Hora], 4, 2 ) )
				RETURN IF ( h < 5 * 60 + 20, h + 1440, h )

		/// Igual à Hora-Hora[Motivo Padrão], mas texto vazio vira BLANK (a Hora-Hora só tem linhas com motivo).
		column 'Motivo Padrão'
			dataType: string
			summarizeBy: none
			expression =
				VAR t = TRIM ( 'fHoraHora'[Motivo] )
				VAR p = IFERROR ( SEARCH ( "-", t ), 0 )
				VAR pre = IF ( p > 1, TRIM ( LEFT ( t, p - 1 ) ), "" )
				VAR limpo = IF ( IFERROR ( VALUE ( pre ), -1 ) >= 0, TRIM ( MID ( t, p + 1, 300 ) ), t )
				RETURN
				    IF (
				        t = "" || ISBLANK ( t ), BLANK (),
				        SWITCH ( TRUE (),
				            limpo = "Refeição", "Almoço",
				            limpo = "Problema no tubo", "Análise/Problema no tubo",
				            limpo )
				    )

		column 'Motivo 2 Padrão'
			dataType: string
			summarizeBy: none
			expression =
				VAR t = TRIM ( 'fHoraHora'[Motivo 2] )
				VAR p = IFERROR ( SEARCH ( "-", t ), 0 )
				VAR pre = IF ( p > 1, TRIM ( LEFT ( t, p - 1 ) ), "" )
				VAR limpo = IF ( IFERROR ( VALUE ( pre ), -1 ) >= 0, TRIM ( MID ( t, p + 1, 300 ) ), t )
				RETURN
				    IF (
				        t = "" || ISBLANK ( t ), BLANK (),
				        SWITCH ( TRUE (),
				            limpo = "Refeição", "Almoço",
				            limpo = "Problema no tubo", "Análise/Problema no tubo",
				            limpo )
				    )

		partition fHoraHora = m
			mode: import
			source =
				let
				  Origem = SharePoint.Tables("https://danfoss.sharepoint.com/sites/OperationsGuaratingueta", [Implementation = "2.0", ViewMode = "All"]),
				  Lista = Origem{[Name = "Hora-Hora"]}[Items],
				  Colunas = Table.SelectColumns(Lista, {"ID","Data","Turno","Célula","Hora","Mangueira","Minutos","Meta Hora","Real. Hora","Tempo Parado (min)","Motivo","Motivo 2","Status"}, MissingField.UseNull),
				  Tipos = Table.TransformColumnTypes(Colunas, {{"ID", Int64.Type}, {"Data", type date}, {"Minutos", type number}, {"Meta Hora", type number}, {"Real. Hora", type number}, {"Tempo Parado (min)", type number}})
				in
				  Tipos
```

## 2) Relacionamento (muitos-para-um, sentido único)
- `fHoraHora[Data]` → `dCalendario[Date]` (o filtro "Período" da página usa o calendário).

## 3) Verificação depois de aplicar e atualizar
- Linhas de `fHoraHora` ≥ linhas de `Hora-Hora` (o diário cita ~23,8 mil contra ~10,2 mil em 31/08).
- Uma máquina, um dia, um turno: Meta, Real e Parado da página batem com o resumo do app (rodapé do Hora-Hora).
- Cuidado conhecido: MEL-243 (Meta Hora com um zero a mais em 47 linhas do 2º turno, set/2026) e duplicatas
  históricas na lista (MEL-104/155). Os números de set/2026 podem divergir do app por causa disso.
