# fHoraHora: dia produtivo do BI, 10 min de 13:47–13:57 e meta proporcional à refeição — APLICADO em 23/10/2026

Só BI. O app, a lista do SharePoint e as colunas `Data`, `Turno`, `Minutos`, `Meta Hora`, `Real. Hora` não mudam.

## Regras (decisão do William, 23/10/2026)
1. **Dia produtivo do BI** = 3º turno da noite anterior + 1º + 2º. O 3º turno que começa 22:20 do dia 21 entra no dia 22;
   o do dia 22 entra no dia 23. Na base, as duas metades do 3º turno ficam com a `Data` do dia em que ele começa.
2. **13:47–13:57**: a janela `13:00 - 13:57` (1º turno) perde 10 min e a `13:47 - 15:00` (2º turno) ganha 10 min.
   Hoje os minutos já somam 120 (57 + 63): o que se sobrepõe são os rótulos, não os minutos.
3. **Hora do jantar conta**: a linha com `Motivo Padrão = Almoço` entra com o real inteiro e a meta só dos minutos fora
   da refeição (TH07, 22/10, 19:00–20:00: meta 228 × (60 − 46)/60 ≈ 53; real 52). Refeição fica fora de Parado e de Principal parada.

## Janelas do 3º turno (HoraOrdem ≥ 1340)
`22:20 - 23:00` … `05:00 - 05:20`. A janela `22:20 - 23:20` é hora extra do 2º turno e fica de fora (mesmo HoraOrdem 1340).
Usa-se o rótulo da hora e não a coluna `Turno`, porque há linhas soltas com turno trocado.

## Colunas e relacionamentos aplicados (TMDL view)
```
createOrReplace
	ref table fHoraHora
		column 'Data BI' =
				VAR h = fHoraHora[HoraOrdem]
				VAR noite = NOT ISBLANK(h) && h >= 1340 && fHoraHora[Hora] <> "22:20 - 23:20"
				RETURN IF(noite, fHoraHora[Data] + 1, fHoraHora[Data])
			dataType: dateTime
			formatString: dd/mm/yyyy
			summarizeBy: none
		column 'HoraOrdem BI' =     // oculta; mesma condição, devolve h - 1440 para o 3º turno
			...
		column 'Minutos BI' =
				fHoraHora[Minutos] + SWITCH(fHoraHora[Hora], "13:00 - 13:57", -10, "13:47 - 15:00", 10, 0)
		column 'Meta Hora BI' =
				VAR m = fHoraHora[Minutos]
				VAR ref = IF(fHoraHora[Motivo Padrão] = "Almoço", COALESCE(fHoraHora[Tempo Parado (min)], 0), 0)
				RETURN IF(m > 0, fHoraHora[Meta Hora] * MAX(0, fHoraHora[Minutos BI] - ref) / m, fHoraHora[Meta Hora])
		column 'Hora BI' =          // cópia da Hora, ordenada por 'HoraOrdem BI'
				fHoraHora[Hora]
			sortByColumn: 'HoraOrdem BI'
	relationship 7c1e5b2a-4d36-4f9b-a8e0-2b6d9c3f1a47     // era fHoraHora[Data] → dCalendario[Date]; ficou INATIVO
		isActive: false
	relationship fHoraHora_DataBI                         // ATIVO: fHoraHora[Data BI] → dCalendario[Date]
```
`Hora` não pode ordenar por `HoraOrdem BI` (dependência circular: a ordem lê a `Hora`); por isso existe a `Hora BI`.
Os visuais da página Hora-Hora usam `Hora BI` no eixo.

## Pendente depois de aplicar
- (feito 23/10) Refresh do modelo e medida `'Hora-Hora'[Meta HH]` = `SUM(fHoraHora[Meta Hora BI])`.
  Conferência TH07, dia produtivo 22/10: minutos BI 507 (1º) + 534 (2º) + 399 (3º) = 1.440; meta BI 1.698,93 / 1.854,14 / 1.516; real 834 / 1.044 / 726.
- Publicar o relatório (medidas `HH Meta`, `HH Meta Útil`, `HH Aderência`, `HH Parado`, `HH Principal Parada` já editadas
  em `GMS_Painel.Report`; o filtro de página `f_refeicao_hh` saiu).
- Conferir um dia × um turno × uma célula contra o rodapé do Hora-Hora do app.

## ATUALIZAÇÃO 26/10/2026 — regra nova do dia produtivo (substitui a regra 1 acima)
O dia produtivo do BI vai das **05:20 do dia D às 05:20 do dia D+1**; o 3º turno que começa 22:41 do dia D fica no dia D, como a base já grava a `Data`.
Aplicado no modelo: `'Data BI' = fHoraHora[Data]` e `'HoraOrdem BI' = fHoraHora[HoraOrdem]` (as demais colunas BI e os relacionamentos ficam como estavam).
Texto do relatório: "Dia produtivo D: de D 05:20 até D+1 05:20". Depende de refresh para as colunas recalcularem.
