# OEE2 da Trançagem no modelo (GMS): script TMDL, conferência e volta (MEL-266, passo 1) — PENDENTE DE APLICAR (só com o "libero" do William, no TMDL view do modelo vivo, depois da revisão do `revisor`)

Só BI. O app, a lista Hora-Hora e a `fHoraHora` não mudam. Regras: `Analises/OEE2_HoraHora/PLANO_OEE2.md` (atualização de 12/11, seções A, B e D). Referência de números: `Analises/OEE2_HoraHora/conferir_oee2.py` e `oee2_referencia_2026-09-04_a_11-06.csv`. Página: `PowerBI/GMS_Painel.Report/definition/pages/pg_oee2` (`Painel_Redesign/build_oee2.py`).

## Objetos criados ou alterados
| Objeto | Tipo | Ação | O que é |
|---|---|---|---|
| `dMotivoParada` | tabela calculada | **alterada** (`createOrReplace`) | Mesmas colunas `Motivo` e `Tipo` (44 motivos antigos intactos) mais 15 motivos novos e 6 colunas: `Família`, `Categoria Danfoss`, `No OEE2`, `Componente`, `Ordem Família` (oculta) e `Cor`. Os 3 relacionamentos com `Hora-Hora` e `Paradas_Montagem` são declarados de novo no script. Fonte: `modelo/dMotivoParada.csv` (gerado por `gerar_mapa_motivos.py`). |
| `fHoraCheia` | tabela calculada | **alterada** (`createOrReplace`) | Só uma coluna nova, `Meta Cheia` (= Meta Hora x Fração, sem o desconto da refeição). O resto é o script vigente de 11/11, igual; os 2 relacionamentos (`Data BI` e `Turno BI`) são declarados de novo. |
| `dEtapaOEE` | tabela calculada | **nova** | Eixo desconectado da cascata (5 etapas). |
| `OEE2 Janela` | medida | nova | Minutos da janela (soma de fHoraCheia[Minutos]); dia produtivo 05:00-05:00, 24 h por máquina com linha lançada. |
| `OEE2 Planejada` | medida | nova | Azul + cinza, com a pausa fixa: por Célula x Data BI x Turno BI com Real > 0 e pelo menos 240 min de janela, 45 min no lugar da refeição declarada; turno sem produção ou com menos de 4 h (só hora extra) não recebe pausa e mantém a refeição declarada como cinza (William, 12/11). |
| `OEE2 Produção` | medida | nova | Tempo de produção = Janela - Planejada. |
| `OEE2 Amarela` | medida | nova | Σ P (parado capado na fatia) dos motivos de família Amarela: troca de lote, perda de disponibilidade. |
| `OEE2 Valorizado` | medida | nova | Valorizado = Janela - Σ P de todas as linhas (caminho oficial). A pausa fixa não entra: não desconta duas vezes. |
| `OEE2 Vermelha` | medida | nova | Perdas na operação = resíduo (Produção - Amarela - Valorizado). Inclui refeição declarada acima de 45 min, pausa lançada em outro motivo e linhas sem família; pode sair negativa num recorte onde a pausa fixa é maior que o parado declarado. |
| `OEE2 Valorizado (Real)` | medida | nova | Medida de controle: Σ MIN(Real, Meta Cheia) x Minutos ÷ Meta Cheia (segundo caminho do valorizado, por velocidade). Compare com OEE2 Valorizado: a diferença total tem de ficar abaixo de 2%. |
| `OEE2 Disponibilidade` | medida | nova | Disponibilidade = (Produção - Amarela) ÷ Produção. Em branco (nunca 0) sem produção ou sem tempo de produção. |
| `OEE2 Performance` | medida | nova | Performance = Valorizado ÷ (Produção - Amarela). Em branco sem produção. |
| `OEE2 Refugo (m)` | medida | nova | Refugo da trançadeira, na data do refugo (o Período filtra pela relação TiposErros[DataRefugo] -> dCalendario) e, com turno filtrado, no Turno Erro igual. Trançadeira normalizada (TH-02 = TH02, TM.01 = TM01). Refugo sem trançadeira fica fora. |
| `OEE2 Qualidade` | medida | nova | Qualidade = 1 - refugo ÷ Real (m). Aproximação declarada: a data é a do refugo, não a da trança. |
| `OEE2` | medida | nova | OEE2 = D x P x Q = Valorizado ÷ Produção x Q. Consolidado ponderado pelo tempo (Σ valorizado ÷ Σ produção), nunca média das máquinas; máquina sem produção fica em branco. |
| `OEE2 TCU` | medida | nova | TCU = Valorizado x Q ÷ (minutos do turno x dias do filtro x máquinas), 24/7 e fixo: 11 máquinas da fx_CelulasTrancagem (a TH04 entra); com turno filtrado o dia vale os minutos desse turno (540/480/420); dias = primeiro ao último Data BI do período. |
| `OEE2 Cascata` | medida | nova | Passos da cascata (minutos, com sinal): Janela, - Parada planejada, - Troca de lote, - Perdas na operação, - Refugo (valorizado x (1 - Q)). O total que o gráfico de cascata soma no fim é o valorizado bom. |
| `OEE2 Aviso Velocidade` | medida | nova | Texto de aviso por máquina (só na linha de total do turno): Real acima da meta (velocidade validada abaixo do real) ou Valorizado (Real) acima do Valorizado em mais de 2%. Não capa em silêncio. Vários na mesma linha: conta as máquinas. |
| `OEE2 Minutos Parados` | medida | nova | Pareto: minutos parados (P capado) do motivo declarado, cortados pela Categoria/Família da dMotivoParada. Mostra o motivo declarado, inclusive a refeição. |
| `OEE2 Cor Família` | medida | nova | Cor hex da família do motivo, para colorir o Pareto por formatação condicional. |
| `OEE2 Ref. OEE2` | medida | nova | Texto fixo da referência de partida do GMS (Q3 de 09/11): sem meta fixa. |
| `OEE2 Ref. TCU` | medida | nova | Texto fixo da referência de partida do GMS (Q3 de 09/11): sem meta fixa. |

Pasta de exibição das 19 medidas novas: **OEE2**, na tabela `Medidas` existente. Nenhuma medida existente muda (`HH ...`, `PA ...`, `VG ...`, `Refugo (m)`, `Disponibilidade` etc. ficam como estão). Os nomes levam o prefixo `OEE2 ` porque `Disponibilidade` já existe como medida de relatório (não pode haver nome repetido) e para a pasta ficar legível; a medida do índice final se chama só `OEE2`.

## Antes de colar
1. **Revisor.** A regra de parada e a pausa de 45 min (seção B do plano) passam pelo `revisor` antes do "libero". Pontos que ele tem de olhar estão no fim deste arquivo.
2. **Nomes que o script supõe** (conferir no modelo vivo, DAX query view, devem rodar sem erro; os nomes vêm do snapshot de 05/11):
```
EVALUATE
ROW (
    "Refugo", SUM ( TiposErros[Quantidade] ),
    "Datas", COUNTROWS ( FILTER ( TiposErros, NOT ISBLANK ( TiposErros[DataRefugo] ) ) ),
    "Tranç.", COUNTROWS ( FILTER ( TiposErros, NOT ISBLANK ( TiposErros[Trançadeira] ) ) ),
    "Turno", COUNTROWS ( FILTER ( TiposErros, NOT ISBLANK ( TiposErros[Turno Erro] ) ) ),
    "Parado", SUM ( fHoraCheia[Parado] ),
    "Motivos", COUNTROWS ( dMotivoParada )
)
```
3. **Nomes dos 3 relacionamentos da `dMotivoParada`.** O script os declara de novo pelos nomes do snapshot (`c7bff530...`, `2ecc65ff...`, `eab0ca5a...`). Confira com `EVALUATE INFO.RELATIONSHIPS()` (coluna `Name`). Se o nome for outro, troque no script, senão o modelo ficaria com relacionamento em dobro. Se o `createOrReplace` da tabela soltar algum, o próprio script o recria.
4. Digite/cole no TMDL view **sem indentação à esquerda além da estrutura** (seção 7 do `COMO_ARRUMAR_HORAHORA.md`): cada expressão DAX está toda em linhas no mesmo nível (4 tabs), de propósito. `Escape` depois de cada linha digitada fecha o autocompletar. Se o editor reclamar de coluna ou medida que nasce no mesmo script, é esperado.
5. Se o editor recusar o script inteiro, aplique em 3 passes, na ordem: (a) `dMotivoParada` e `dEtapaOEE`; (b) `fHoraCheia` e relacionamentos, depois **refresh**; (c) `ref table Medidas`. As medidas só calculam depois do refresh.
6. O relatório (`pg_oee2`) só abre sem erro depois que as medidas existem. O William precisa reabrir o projeto no Desktop antes de publicar (o Desktop sobrescreve o que mudou nos arquivos).

## 1) Script TMDL (cole inteiro)
```
createOrReplace

	table dMotivoParada

		/// Dimensão de motivo padronizado (MEL-107) com a família do padrão Danfoss (MEL-266). Fonte: gerar_mapa_motivos.py. Motivos da Montagem ficam sem família.
		column Motivo
			dataType: string
			summarizeBy: none
			sourceColumn: [Motivo]

		column Tipo
			dataType: string
			summarizeBy: none
			sourceColumn: [Tipo]

		column 'Família'
			dataType: string
			summarizeBy: none
			sortByColumn: 'Ordem Família'
			sourceColumn: [Família]

		column 'Categoria Danfoss'
			dataType: string
			summarizeBy: none
			sourceColumn: [Categoria Danfoss]

		column 'No OEE2'
			dataType: string
			summarizeBy: none
			sourceColumn: [No OEE2]

		column Componente
			dataType: string
			summarizeBy: none
			sourceColumn: [Componente]

		column 'Ordem Família'
			dataType: int64
			isHidden
			formatString: 0
			summarizeBy: none
			sourceColumn: [Ordem Família]

		column Cor
			dataType: string
			summarizeBy: none
			sourceColumn: [Cor]

		partition dMotivoParada = calculated
			mode: import
			source =
				DATATABLE (
				"Motivo", STRING,
				"Tipo", STRING,
				"Família", STRING,
				"Categoria Danfoss", STRING,
				"No OEE2", STRING,
				"Componente", STRING,
				"Ordem Família", INTEGER,
				"Cor", STRING,
				{
				{ "Falta de Demanda", "Organizacional", "Azul", "Sem atividade / sem produção planejada", "Não", "—", 1, "#2C6FBF" },
				{ "Inventário", "Programada", "Azul", "Sem atividade / sem produção planejada", "Não", "—", 1, "#2C6FBF" },
				{ "Manutenção Preventiva", "Programada", "Cinza", "Manutenção planejada", "Não", "—", 2, "#8A8F96" },
				{ "Manutenção Preventiva (Fora do Prazo)", "Programada", "Cinza", "Manutenção planejada", "Não", "—", 2, "#8A8F96" },
				{ "Manut. Prod. Total (MPT)", "Programada", "Cinza", "Manutenção planejada / autônoma", "Não", "—", 2, "#8A8F96" },
				{ "Almoço", "Programada", "Cinza", "Pessoal: pausa", "Não", "—", 2, "#8A8F96" },
				{ "Reunião", "Programada", "Cinza", "Pessoal: reunião / treinamento", "Não", "—", 2, "#8A8F96" },
				{ "Reunião/Treinamento", "Programada", "Cinza", "Pessoal: reunião / treinamento", "Não", "—", 2, "#8A8F96" },
				{ "Amostra", "Programada", "Cinza", "Validação (teste de produto)", "Não", "—", 2, "#8A8F96" },
				{ "TESTE ENGENHARIA", "Programada", "Cinza", "Validação (teste de produto)", "Não", "—", 2, "#8A8F96" },
				{ "Execução Check List Lean", "Programada", "Amarela", "Partida / início de turno", "Sim", "Disponibilidade", 3, "#F2B01E" },
				{ "Alimentação de fio", "Processo", "Amarela", "Reabastecimento", "Sim", "Disponibilidade", 3, "#F2B01E" },
				{ "Emenda de Fita", "Processo", "Amarela", "Reabastecimento", "Sim", "Disponibilidade", 3, "#F2B01E" },
				{ "Troca de Carretel", "Processo", "Amarela", "Reabastecimento", "Sim", "Disponibilidade", 3, "#F2B01E" },
				{ "Troca de Lenon", "Processo", "Amarela", "Reabastecimento", "Sim", "Disponibilidade", 3, "#F2B01E" },
				{ "Troca de boneca", "Processo", "Amarela", "Reabastecimento", "Sim", "Disponibilidade", 3, "#F2B01E" },
				{ "Bobinagem de Arame Espiral", "Processo", "Amarela", "Reabastecimento (preparo de material)", "Sim", "Disponibilidade", 3, "#F2B01E" },
				{ "Puxada do Insulation", "Processo", "Amarela", "Reabastecimento (preparo de material)", "Sim", "Disponibilidade", 3, "#F2B01E" },
				{ "Registro de Peck", "Processo", "Amarela", "Troca de lote: checagem de qualidade", "Sim", "Disponibilidade", 3, "#F2B01E" },
				{ "Registro de Pick", "Processo", "Amarela", "Troca de lote: checagem de qualidade", "Sim", "Disponibilidade", 3, "#F2B01E" },
				{ "Set-up", "Programada", "Amarela", "Troca de lote: preparação / troca de ferramenta", "Sim", "Disponibilidade", 3, "#F2B01E" },
				{ "Troca de Ferramental (fieira/matriz)", "Processo", "Amarela", "Troca de lote: preparação / troca de ferramenta", "Sim", "Disponibilidade", 3, "#F2B01E" },
				{ "Troca de composto", "Processo", "Amarela", "Troca de lote: preparação / troca de ferramenta", "Sim", "Disponibilidade", 3, "#F2B01E" },
				{ "Manutenção Corretiva", "Falha", "Vermelha", "Defeito de máquina", "Sim", "Performance", 4, "#E2000F" },
				{ "Ajuste da Máquina", "Processo", "Vermelha", "Defeito de máquina (re-set)", "Sim", "Performance", 4, "#E2000F" },
				{ "Problemas com composto", "Material", "Vermelha", "Defeito de processo", "Sim", "Performance", 4, "#E2000F" },
				{ "Problemas de qualidade", "Processo", "Vermelha", "Defeito de processo", "Sim", "Performance", 4, "#E2000F" },
				{ "Resto de fio", "Material", "Vermelha", "Defeito de processo", "Sim", "Performance", 4, "#E2000F" },
				{ "Falta de programação", "Organizacional", "Vermelha", "Defeito de processo: OP faltando", "Sim", "Performance", 4, "#E2000F" },
				{ "Análise/Problema no tubo", "Falha", "Vermelha", "Defeito de processo: material ruim", "Sim", "Performance", 4, "#E2000F" },
				{ "Quebra de fio", "Falha", "Vermelha", "Defeito de processo: quebra de material", "Sim", "Performance", 4, "#E2000F" },
				{ "Falta de Carretel", "Material", "Vermelha", "Espera: material", "Sim", "Performance", 4, "#E2000F" },
				{ "Falta de Lenon", "Material", "Vermelha", "Espera: material", "Sim", "Performance", 4, "#E2000F" },
				{ "Falta de Mandril", "Material", "Vermelha", "Espera: material", "Sim", "Performance", 4, "#E2000F" },
				{ "Falta de Mandril Soldado", "Material", "Vermelha", "Espera: material", "Sim", "Performance", 4, "#E2000F" },
				{ "Falta de Mangueira", "Material", "Vermelha", "Espera: material", "Sim", "Performance", 4, "#E2000F" },
				{ "Falta de Mangueira Trançada", "Material", "Vermelha", "Espera: material", "Sim", "Performance", 4, "#E2000F" },
				{ "Falta de composto", "Material", "Vermelha", "Espera: material", "Sim", "Performance", 4, "#E2000F" },
				{ "Falta de desmoldante", "Material", "Vermelha", "Espera: material", "Sim", "Performance", 4, "#E2000F" },
				{ "Falta de fio - Bobinadeira", "Material", "Vermelha", "Espera: material", "Sim", "Performance", 4, "#E2000F" },
				{ "Falta de insulation", "Material", "Vermelha", "Espera: material", "Sim", "Performance", 4, "#E2000F" },
				{ "Falta de tubo", "Material", "Vermelha", "Espera: material", "Sim", "Performance", 4, "#E2000F" },
				{ "Falta de operador", "Organizacional", "Vermelha", "Espera: operador", "Sim", "Performance", 4, "#E2000F" },
				{ "Motivo Não Declarado", "Organizacional", "Vermelha", "Não declarado", "Sim", "Performance", 4, "#E2000F" },
				{ "Sem apontamento", "Organizacional", "Vermelha", "Não declarado", "Sim", "Performance", 4, "#E2000F" },
				{ "Falta de energia / ar", "Falha", "Vermelha", "Utilidades", "Sim", "Performance", 4, "#E2000F" },
				{ "Divergência do Tempo Padrão", "Organizacional", "Vermelha", "Velocidade reduzida", "Sim", "Performance", 4, "#E2000F" },
				{ "AP - Alteracao de Planejamento", "Organizacional", "", "", "", "", 9, "" },
				{ "AU - Auditoria (Qualidade / Seguranca)", "Programada", "", "", "", "", 9, "" },
				{ "CA - Calibracao / Verificacao de Instrumento", "Programada", "", "", "", "", 9, "" },
				{ "FC - Falta de Componentes (O-ring, sleeve, mola, adaptador...)", "Material", "", "", "", "", 9, "" },
				{ "FI - Falta de Embalagem / Termoencolhível", "Material", "", "", "", "", 9, "" },
				{ "IT - Aguardando Instrucao de Trabalho / liberacao Engenharia", "Organizacional", "", "", "", "", 9, "" },
				{ "LI - 5S", "Programada", "", "", "", "", 9, "" },
				{ "RF - Refeição", "Programada", "", "", "", "", 9, "" },
				{ "RT - Retrabalho", "Processo", "", "", "", "", 9, "" },
				{ "TE - Tempo Excedido", "Excedido", "", "", "", "", 9, "" },
				{ "TU - Troca de Turno", "Programada", "", "", "", "", 9, "" },
				{ "VR - Velocidade Reduzida", "Processo", "", "", "", "", 9, "" }
				}
				)

	relationship c7bff530-b6e0-4649-bce4-7cecd6ed92ea
		fromColumn: 'Hora-Hora'.'Motivo Padrão'
		toColumn: dMotivoParada.Motivo

	relationship 2ecc65ff-ea99-4ae8-8358-30586480ca5f
		isActive: false
		fromColumn: 'Hora-Hora'.'Motivo 2 Padrão'
		toColumn: dMotivoParada.Motivo

	relationship eab0ca5a-394e-4adc-b15a-f81458e7e550
		fromColumn: Paradas_Montagem.Motivo
		toColumn: dMotivoParada.Motivo

	table dEtapaOEE

		/// Eixo desconectado da cascata do OEE2 (nenhum relacionamento): cada etapa é um passo da conta Janela até o valorizado bom.
		column Etapa
			dataType: string
			summarizeBy: none
			sortByColumn: Ordem
			sourceColumn: [Etapa]

		column Ordem
			dataType: int64
			isHidden
			formatString: 0
			summarizeBy: none
			sourceColumn: [Ordem]

		partition dEtapaOEE = calculated
			mode: import
			source =
				DATATABLE (
				"Etapa", STRING,
				"Ordem", INTEGER,
				{
				{ "Janela", 1 },
				{ "Parada planejada", 2 },
				{ "Troca de lote", 3 },
				{ "Perdas na operação", 4 },
				{ "Refugo", 5 }
				}
				)

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

		column 'Meta Cheia'
			dataType: double
			formatString: #,0.0
			summarizeBy: none
			sourceColumn: [Meta Cheia]

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
				"Fr", DIVIDE ( MIN ( [Efim], ( [Value] + 1 ) * 60 ) - MAX ( [Sini], [Value] * 60 ), [Efim] - [Sini] ),
				"Mn", IF ( COALESCE ( [Min], 0 ) > 0, [Min], [Efim] - [Sini] )
				)
				VAR Calc2 =
				ADDCOLUMNS (
				Calc,
				"DataBI", [Data] + INT ( [Value] / 24 ),
				"HO", MOD ( [Value], 24 ),
				"TurnoBI", IF ( MOD ( [Value], 24 ) < 9, "1º Turno", IF ( MOD ( [Value], 24 ) < 17, "2º Turno", "3º Turno" ) )
				)
				VAR ComAlmoco =
				DISTINCT ( SELECTCOLUMNS ( FILTER ( Calc2, [Motivo Padrão] = "Almoço" ), "C", [Célula], "D", [DataBI], "T", [TurnoBI] ) )
				VAR Calc3 =
				ADDCOLUMNS (
				Calc2,
				"Refeicao", [Motivo Padrão] = "Almoço" || ( [HO] = SWITCH ( [TurnoBI], "1º Turno", 6, "2º Turno", 14, 21 ) && NOT ( ( [Célula], [DataBI], [TurnoBI] ) IN ComAlmoco ) )
				)
				RETURN
				SELECTCOLUMNS (
				Calc3,
				"Célula", [Célula],
				"Mangueira", [Mangueira],
				"Data BI", [DataBI],
				"Turno BI", [TurnoBI],
				"Hora", FORMAT ( MOD ( 5 + MOD ( [Value], 24 ), 24 ), "00" ) & ":00 - " & FORMAT ( MOD ( 6 + MOD ( [Value], 24 ), 24 ), "00" ) & ":00",
				"HoraOrdem", MOD ( [Value], 24 ),
				"Minutos", [Mn] * [Fr],
				"Meta", COALESCE ( [MetaHora], 0 ) * IF ( [Refeicao] && [Mn] > 0, MAX ( 0, [Mn] - 45 ) / [Mn], 1 ) * [Fr],
				"Meta Cheia", COALESCE ( [MetaHora], 0 ) * [Fr],
				"Real", COALESCE ( [Real0], 0 ) * [Fr],
				"Parado", MIN ( COALESCE ( [Par0], 0 ) * [Fr], [Mn] * [Fr] ),
				"Motivo", [Motivo],
				"Motivo Padrão", [Motivo Padrão],
				"Motivo 2", [Motivo 2],
				"Motivo 2 Padrão", [Motivo 2 Padrão],
				"ID Origem", [ID Origem],
				"Fração", [Fr]
				)

	relationship fHoraCheia_DataBI
		fromColumn: fHoraCheia.'Data BI'
		toColumn: dCalendario.Date

	relationship dTurno_fHoraCheia
		fromColumn: fHoraCheia.'Turno BI'
		toColumn: dTurno.Turno

	ref table Medidas

		measure 'OEE2 Janela' =
				SUM ( fHoraCheia[Minutos] )
			formatString: #,0
			displayFolder: OEE2

		measure 'OEE2 Planejada' =
				VAR Sem =
				CALCULATETABLE (
				VALUES ( dMotivoParada[Motivo] ),
				REMOVEFILTERS ( dMotivoParada ),
				dMotivoParada[Família] IN { "Azul", "Cinza" },
				dMotivoParada[Motivo] <> "Almoço"
				)
				VAR Turnos =
				ADDCOLUMNS (
				SUMMARIZE ( fHoraCheia, fHoraCheia[Célula], fHoraCheia[Data BI], fHoraCheia[Turno BI] ),
				"@min", CALCULATE ( SUM ( fHoraCheia[Minutos] ) ),
				"@real", CALCULATE ( SUM ( fHoraCheia[Real] ) ),
				"@pl", CALCULATE ( SUM ( fHoraCheia[Parado] ), KEEPFILTERS ( TREATAS ( Sem, fHoraCheia[Motivo Padrão] ) ) ),
				"@ref", CALCULATE ( SUM ( fHoraCheia[Parado] ), KEEPFILTERS ( fHoraCheia[Motivo Padrão] = "Almoço" ) )
				)
				RETURN
				SUMX ( Turnos, [@pl] + IF ( [@real] > 0 && [@min] >= 240, 45, [@ref] ) )
			formatString: #,0
			displayFolder: OEE2

		measure 'OEE2 Produção' =
				[OEE2 Janela] - [OEE2 Planejada]
			formatString: #,0
			displayFolder: OEE2

		measure 'OEE2 Amarela' =
				VAR Am =
				CALCULATETABLE ( VALUES ( dMotivoParada[Motivo] ), REMOVEFILTERS ( dMotivoParada ), dMotivoParada[Família] = "Amarela" )
				RETURN
				CALCULATE ( SUM ( fHoraCheia[Parado] ), KEEPFILTERS ( TREATAS ( Am, fHoraCheia[Motivo Padrão] ) ) )
			formatString: #,0
			displayFolder: OEE2

		measure 'OEE2 Valorizado' =
				[OEE2 Janela] - SUM ( fHoraCheia[Parado] )
			formatString: #,0
			displayFolder: OEE2

		measure 'OEE2 Vermelha' =
				[OEE2 Produção] - [OEE2 Amarela] - [OEE2 Valorizado]
			formatString: #,0
			displayFolder: OEE2

		measure 'OEE2 Valorizado (Real)' =
				SUMX (
				fHoraCheia,
				IF (
				fHoraCheia[Meta Cheia] > 0,
				DIVIDE ( MIN ( fHoraCheia[Real], fHoraCheia[Meta Cheia] ), fHoraCheia[Meta Cheia] ) * fHoraCheia[Minutos],
				IF ( fHoraCheia[Real] > 0, fHoraCheia[Minutos], 0 )
				)
				)
			formatString: #,0
			displayFolder: OEE2

		measure 'OEE2 Disponibilidade' =
				VAR p = [OEE2 Produção]
				RETURN
				IF ( p > 0 && SUM ( fHoraCheia[Real] ) > 0, DIVIDE ( p - [OEE2 Amarela], p ) )
			formatString: 0.0%
			displayFolder: OEE2

		measure 'OEE2 Performance' =
				VAR op = [OEE2 Produção] - [OEE2 Amarela]
				RETURN
				IF ( op > 0 && SUM ( fHoraCheia[Real] ) > 0, DIVIDE ( [OEE2 Valorizado], op ) )
			formatString: 0.0%
			displayFolder: OEE2

		measure 'OEE2 Refugo (m)' =
				VAR Cels = VALUES ( fHoraCheia[Célula] )
				VAR TemTurno = ISFILTERED ( dTurno[Turno] )
				VAR Turnos = VALUES ( dTurno[Turno] )
				RETURN
				SUMX (
				FILTER (
				TiposErros,
				NOT ISBLANK ( TiposErros[Trançadeira] )
				&& SUBSTITUTE ( SUBSTITUTE ( TRIM ( TiposErros[Trançadeira] ), "-", "" ), ".", "" ) IN Cels
				&& ( NOT TemTurno || ( TiposErros[Turno Erro] & "º Turno" ) IN Turnos )
				),
				TiposErros[Quantidade]
				)
			formatString: #,0
			displayFolder: OEE2

		measure 'OEE2 Qualidade' =
				VAR r = SUM ( fHoraCheia[Real] )
				RETURN
				IF ( r > 0, MAX ( 0, 1 - DIVIDE ( [OEE2 Refugo (m)], r ) ) )
			formatString: 0.0%
			displayFolder: OEE2

		measure 'OEE2' =
				VAR p = [OEE2 Produção]
				VAR q = [OEE2 Qualidade]
				RETURN
				IF ( p > 0 && NOT ISBLANK ( q ), DIVIDE ( [OEE2 Valorizado], p ) * q )
			formatString: 0.0%
			displayFolder: OEE2

		measure 'OEE2 TCU' =
				VAR Lista = { "TH01", "TH02", "TH03", "TH04", "TH05", "TH06", "TH07", "TO04", "TM01", "TM04", "Spiral" }
				VAR CelSel = CALCULATETABLE ( VALUES ( fHoraCheia[Célula] ), REMOVEFILTERS ( dCalendario ), REMOVEFILTERS ( dTurno ) )
				VAR NMaq = COUNTROWS ( FILTER ( Lista, [Value] IN CelSel ) )
				VAR D0 = CALCULATE ( MIN ( fHoraCheia[Data BI] ), REMOVEFILTERS ( fHoraCheia[Célula] ), REMOVEFILTERS ( dTurno ) )
				VAR D1 = CALCULATE ( MAX ( fHoraCheia[Data BI] ), REMOVEFILTERS ( fHoraCheia[Célula] ), REMOVEFILTERS ( dTurno ) )
				VAR Dias = INT ( D1 - D0 ) + 1
				VAR MinTurnos = SUMX ( VALUES ( dTurno[Turno] ), SWITCH ( dTurno[Turno], "1º Turno", 540, "2º Turno", 480, 420 ) )
				VAR Den = MinTurnos * Dias * NMaq
				VAR Num = IF ( SUM ( fHoraCheia[Real] ) > 0, [OEE2 Valorizado] * [OEE2 Qualidade], 0 )
				RETURN
				IF ( Den > 0 && COUNTROWS ( fHoraCheia ) > 0, DIVIDE ( Num, Den ) )
			formatString: 0.0%
			displayFolder: OEE2

		measure 'OEE2 Cascata' =
				VAR o = SELECTEDVALUE ( dEtapaOEE[Ordem] )
				RETURN
				SWITCH (
				o,
				1, [OEE2 Janela],
				2, - [OEE2 Planejada],
				3, - [OEE2 Amarela],
				4, - [OEE2 Vermelha],
				5, - [OEE2 Valorizado] * ( 1 - COALESCE ( [OEE2 Qualidade], 1 ) )
				)
			formatString: #,0
			displayFolder: OEE2

		measure 'OEE2 Aviso Velocidade' =
				VAR T =
				ADDCOLUMNS (
				VALUES ( fHoraCheia[Célula] ),
				"@pv", DIVIDE ( CALCULATE ( SUM ( fHoraCheia[Real] ), fHoraCheia[Real] > 0 ), CALCULATE ( SUM ( fHoraCheia[Meta Cheia] ), fHoraCheia[Real] > 0 ) ),
				"@vr", [OEE2 Valorizado (Real)],
				"@vo", [OEE2 Valorizado]
				)
				VAR Flag = FILTER ( T, [@pv] > 1 || [@vr] > [@vo] * 1.02 )
				VAR N = COUNTROWS ( Flag )
				VAR PV = MAXX ( Flag, [@pv] )
				VAR DV = MAXX ( Flag, DIVIDE ( [@vr], [@vo] ) - 1 )
				VAR Txt1 = IF ( PV > 1, "Real " & FORMAT ( PV, "0%" ) & " da meta: velocidade validada abaixo do real", "" )
				VAR Txt2 = IF ( DV > 0.02, "valorizado pela velocidade " & FORMAT ( DV, "0%" ) & " acima do apontado", "" )
				RETURN
				IF (
				ISINSCOPE ( dTurno[Turno] ) || N = 0,
				BLANK (),
				IF ( N = 1, Txt1 & IF ( Txt1 <> "" && Txt2 <> "", " · ", "" ) & Txt2, N & " máquinas com aviso de velocidade" )
				)
			displayFolder: OEE2

		measure 'OEE2 Minutos Parados' =
				CALCULATE ( SUM ( fHoraCheia[Parado] ), KEEPFILTERS ( TREATAS ( VALUES ( dMotivoParada[Motivo] ), fHoraCheia[Motivo Padrão] ) ) )
			formatString: #,0
			displayFolder: OEE2

		measure 'OEE2 Cor Família' =
				COALESCE ( SELECTEDVALUE ( dMotivoParada[Cor] ), "#8A8F96" )
			displayFolder: OEE2

		measure 'OEE2 Ref. OEE2' =
				"Ref. set–nov: 54%"
			displayFolder: OEE2

		measure 'OEE2 Ref. TCU' =
				"Ref. set–nov: 19%"
			displayFolder: OEE2

```

## 2) O que cada peça faz
**Regras (seção B do plano, adaptadas à `fHoraCheia`)**
- Grão: a linha da `fHoraCheia` (hora cheia, dia produtivo 05:00-05:00, `Turno BI` 05-14, 14-22 e 22-05). `P` = `fHoraCheia[Parado]`, que já vem capado na fatia.
- Turno de máquina = `Célula x Data BI x Turno BI`. Com `Real > 0` e **pelo menos 240 min de janela** ele recebe **pausa planejada de 45 min** (turno com menos de 4 h, que em geral é só a hora extra do 2º turno caindo no 3º Turno BI, não recebe pausa: William, 12/11), que entra em Planejada (cinza); os minutos declarados como Almoço (refeição) saem do cinza e ficam absorvidos pela pausa. Turno sem produção: a refeição declarada segue cinza.
- **Valorizado = Janela - Σ P** de todas as linhas (pausa não entra: não desconta duas vezes). **Vermelha** é o resíduo (Produção - Amarela - Valorizado): inclui a refeição declarada acima de 45 min, a pausa lançada em outro motivo e linhas sem família.
- **O 21h45 não entra.** A regra dos 135 min/dia segue só em `HH Meta Útil (m)` e `HH Aderência`.
- OEE2 = D x P x Q, consolidado ponderado pelo tempo; sem tempo de produção ou sem metro produzido o resultado é **em branco**, nunca 0. TCU entra com 0 para máquina parada, porque é sobre as 24 h.

**Peças**
- `dMotivoParada`: cada motivo ganha Família (Azul, Cinza, Amarela, Vermelha), Categoria Danfoss, `No OEE2` (azul e cinza saem do tempo de produção), `Componente` (amarela = Disponibilidade, vermelha = Performance), ordem e cor. Entraram os motivos que faltavam: Registro de Pick e Peck, TESTE ENGENHARIA, Bobinagem de Arame Espiral, Puxada do Insulation, Manutenção Preventiva (Fora do Prazo), Reunião/Treinamento, Falta de Mangueira Trançada e os da Cobertura (composto, ferramental, desmoldante, qualidade, inventário). Montagem (TE, AU, CA, LI, RT, VR, FC, FI, AP, IT, TU, RF) fica sem família.
- `fHoraCheia[Meta Cheia]`: meta da fatia sem o desconto de 45 min da refeição. A coluna `Meta` (que já desconta) não muda. A medida de controle precisa da meta cheia: com a descontada, a janela da refeição contaria como tempo valorizado.
- `dEtapaOEE`: Janela, Parada planejada, Troca de lote, Perdas na operação e Refugo. O gráfico nativo de cascata soma tudo e mostra o **total final = valorizado bom** (Valorizado x Q). A Produção e o Valorizado aparecem nos cartões e nas medidas, não como barra (o gráfico nativo não tem subtotal no meio).
- `OEE2 Planejada` é a única medida que itera por turno de máquina (`SUMMARIZE` + `CALCULATE`); as outras somam direto. As medidas ficam no modelo porque medida de relatório não pode chamar outra medida de relatório (seção 11 do roteiro).
- `OEE2 Refugo (m)`: `TiposErros` não tem relação com a `fHoraCheia`; o corte de máquina é pelo texto da trançadeira normalizada (tira "-" e ".") e o de período é pela relação que já existe com `dCalendario[DataRefugo]`. Com turno filtrado, usa o `Turno Erro`.
- `OEE2 TCU`: 11 máquinas da `fx_CelulasTrancagem` fixas na medida; com a segmentação de Máquina, conta só as selecionadas.
- `OEE2 Aviso Velocidade`: não capa em silêncio. Avisa quando Real ÷ Meta Cheia (janelas com produção) passa de 100% (velocidade validada abaixo do real, o caso da TH01 nas duas passadas, MEL-241) ou quando `OEE2 Valorizado (Real)` passa de `OEE2 Valorizado` em mais de 2%. Só aparece na linha de total do turno da matriz.
- Extras além da lista pedida (precisam estar no modelo para a página funcionar): `OEE2 Refugo (m)`, `OEE2 Minutos Parados` (Pareto), `OEE2 Cor Família` (cor do Pareto), `OEE2 Ref. OEE2` e `OEE2 Ref. TCU` (texto fixo "Ref. set–nov: 54%" e "19%").

## 3) Consultas de conferência (DAX query view, depois do refresh)
Critério: **±0,5 ponto** em D, P, Q, OEE2 e TCU contra o `oee2_referencia_2026-09-04_a_11-06.csv` (mesmo período, mesmo filtro); minutos iguais ao inteiro. Os números vêm do `conferir_oee2.py` (CSV de 06/11 e `TiposErros` de 06/11; o modelo vivo tem dados mais novos, então **filtre até 06/11**, como abaixo, ou compare por dia). Se a lista foi corrigida depois de 06/11, diferenças pequenas são esperadas.

```
// 3a) total, 04/09 a 06/11, todas as máquinas e turnos
EVALUATE
CALCULATETABLE (
    ROW (
        "Janela", [OEE2 Janela],
        "Planejada", [OEE2 Planejada],
        "Produção", [OEE2 Produção],
        "Amarela", [OEE2 Amarela],
        "Vermelha", [OEE2 Vermelha],
        "Valorizado", [OEE2 Valorizado],
        "Valorizado (Real)", [OEE2 Valorizado (Real)],
        "D", [OEE2 Disponibilidade],
        "P", [OEE2 Performance],
        "Q", [OEE2 Qualidade],
        "OEE2", [OEE2],
        "TCU", [OEE2 TCU]
    ),
    dCalendario[Date] >= DATE ( 2026, 9, 4 ),
    dCalendario[Date] <= DATE ( 2026, 11, 6 ),
    fHoraCheia[Célula] <> BLANK ()
)

// 3b) por máquina
EVALUATE
SUMMARIZECOLUMNS (
    fHoraCheia[Célula],
    FILTER ( ALL ( dCalendario[Date] ), dCalendario[Date] >= DATE ( 2026, 9, 4 ) && dCalendario[Date] <= DATE ( 2026, 11, 6 ) ),
    FILTER ( ALL ( fHoraCheia[Célula] ), fHoraCheia[Célula] <> BLANK () ),
    "Janela", [OEE2 Janela],
    "Planejada", [OEE2 Planejada],
    "Produção", [OEE2 Produção],
    "Amarela", [OEE2 Amarela],
    "Vermelha", [OEE2 Vermelha],
    "Valorizado", [OEE2 Valorizado],
    "D", [OEE2 Disponibilidade],
    "P", [OEE2 Performance],
    "Q", [OEE2 Qualidade],
    "OEE2", [OEE2],
    "TCU", [OEE2 TCU],
    "Aviso", [OEE2 Aviso Velocidade]
)
ORDER BY fHoraCheia[Célula]

// 3c) por turno BI
EVALUATE
SUMMARIZECOLUMNS (
    dTurno[Turno],
    FILTER ( ALL ( dCalendario[Date] ), dCalendario[Date] >= DATE ( 2026, 9, 4 ) && dCalendario[Date] <= DATE ( 2026, 11, 6 ) ),
    FILTER ( ALL ( fHoraCheia[Célula] ), fHoraCheia[Célula] <> BLANK () ),
    "Janela", [OEE2 Janela],
    "Planejada", [OEE2 Planejada],
    "Produção", [OEE2 Produção],
    "Amarela", [OEE2 Amarela],
    "Vermelha", [OEE2 Vermelha],
    "Valorizado", [OEE2 Valorizado],
    "D", [OEE2 Disponibilidade],
    "P", [OEE2 Performance],
    "Q", [OEE2 Qualidade],
    "OEE2", [OEE2],
    "TCU", [OEE2 TCU]
)
ORDER BY dTurno[Turno]

// 3d) a matriz da página: máquina x turno (as 30 linhas esperadas estão no CSV, corte "Máquina x Turno BI")
EVALUATE
SUMMARIZECOLUMNS (
    fHoraCheia[Célula],
    dTurno[Turno],
    FILTER ( ALL ( dCalendario[Date] ), dCalendario[Date] >= DATE ( 2026, 9, 4 ) && dCalendario[Date] <= DATE ( 2026, 11, 6 ) ),
    FILTER ( ALL ( fHoraCheia[Célula] ), fHoraCheia[Célula] <> BLANK () ),
    "OEE2", [OEE2],
    "Valorizado", [OEE2 Valorizado],
    "Produção", [OEE2 Produção]
)
ORDER BY fHoraCheia[Célula], dTurno[Turno]

// 3e) cascata (minutos com sinal: Janela, -Planejada, -Amarela, -Vermelha, -Refugo; a soma é o valorizado bom)
EVALUATE
SUMMARIZECOLUMNS (
    dEtapaOEE[Ordem],
    dEtapaOEE[Etapa],
    FILTER ( ALL ( dCalendario[Date] ), dCalendario[Date] >= DATE ( 2026, 9, 4 ) && dCalendario[Date] <= DATE ( 2026, 11, 6 ) ),
    FILTER ( ALL ( fHoraCheia[Célula] ), fHoraCheia[Célula] <> BLANK () ),
    "Cascata", [OEE2 Cascata]
)
ORDER BY dEtapaOEE[Ordem]

// 3f) controle do valorizado e fechamento por família (Σ P = parado total; Valorizado (Real) dentro de 2% do Valorizado no total)
EVALUATE
CALCULATETABLE (
    ROW (
        "Valorizado", [OEE2 Valorizado],
        "Valorizado (Real)", [OEE2 Valorizado (Real)],
        "Diferença", DIVIDE ( [OEE2 Valorizado (Real)], [OEE2 Valorizado] ) - 1,
        "Parado total", SUM ( fHoraCheia[Parado] ),
        "Amarela", [OEE2 Amarela],
        "Refugo (m)", [OEE2 Refugo (m)],
        "Real (m)", SUM ( fHoraCheia[Real] ),
        "Aviso", [OEE2 Aviso Velocidade]
    ),
    dCalendario[Date] >= DATE ( 2026, 9, 4 ),
    dCalendario[Date] <= DATE ( 2026, 11, 6 ),
    fHoraCheia[Célula] <> BLANK ()
)

// 3g) objetos com problema (deve voltar vazio)
EVALUATE FILTER ( INFO.MEASURES (), [State] <> 1 )
EVALUATE FILTER ( INFO.COLUMNS (), [State] <> 1 )
```

**Esperado (pandas, 04/09 a 06/11, 64 dias; minutos e %; regra de 12/11: turno com menos de 240 min sem pausa)**

Total:

| Chave | Janela | Planejada | Produção | Amarela | Vermelha | Valorizado | D | P | Q | OEE2 | TCU |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Total | 433.737 | 61.427 | 372.310 | 61.625 | 106.964 | 203.721 | 83.5% | 65.6% | 98.5% | 53.9% | 19.8% |

Por turno BI (TCU do turno usa os minutos do turno: 540, 480 e 420):

| Chave | Janela | Planejada | Produção | Amarela | Vermelha | Valorizado | D | P | Q | OEE2 | TCU |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1º Turno | 206.534 | 30.607 | 175.926 | 27.158 | 57.804 | 90.965 | 84.6% | 61.2% | 99.1% | 51.2% | 23.7% |
| 2º Turno | 167.738 | 22.300 | 145.438 | 27.079 | 36.438 | 81.921 | 81.4% | 69.2% | 98.0% | 55.2% | 23.8% |
| 3º Turno | 59.465 | 8.520 | 50.945 | 7.388 | 12.721 | 30.836 | 85.5% | 70.8% | 98.3% | 59.5% | 10.3% |

Por máquina (TH04 não tem linha no período: o BI não a mostra na matriz; ela só entra no denominador do TCU):

| Chave | Janela | Planejada | Produção | Amarela | Vermelha | Valorizado | D | P | Q | OEE2 | TCU |
|---|---|---|---|---|---|---|---|---|---|---|---|
| TH01 | 53.429 | 5.834 | 47.595 | 4.068 | 13.888 | 29.639 | 91.5% | 68.1% | 98.9% | 61.6% | 31.8% |
| TH02 | 34.341 | 3.434 | 30.907 | 2.749 | 9.454 | 18.705 | 91.1% | 66.4% | 99.2% | 60.1% | 20.1% |
| TH03 | 39.688 | 5.174 | 34.514 | 5.698 | 13.254 | 15.561 | 83.5% | 54.0% | 98.8% | 44.5% | 16.7% |
| TH04 | 0 | 0 | 0 | 0 | 0 | 0 |  |  |  |  | 0.0% |
| TH05 | 13.109 | 1.451 | 11.658 | 1.241 | 4.443 | 5.974 | 89.3% | 57.4% | 95.2% | 48.8% | 6.2% |
| TH06 | 55.509 | 9.843 | 45.666 | 5.941 | 7.900 | 31.825 | 87.0% | 80.1% | 97.7% | 68.0% | 33.7% |
| TH07 | 59.292 | 15.776 | 43.516 | 10.917 | 6.851 | 25.748 | 74.9% | 79.0% | 98.7% | 58.4% | 27.6% |
| TO04 | 45.790 | 4.759 | 41.031 | 4.900 | 9.912 | 26.219 | 88.1% | 72.6% | 98.8% | 63.1% | 28.1% |
| TM01 | 52.505 | 7.022 | 45.483 | 7.025 | 8.757 | 29.701 | 84.5% | 77.2% | 98.8% | 64.5% | 31.8% |
| TM04 | 32.331 | 3.598 | 28.733 | 2.676 | 14.694 | 11.363 | 90.7% | 43.6% | 98.1% | 38.8% | 12.1% |
| Spiral | 47.743 | 4.536 | 43.207 | 16.410 | 17.810 | 8.987 | 62.0% | 33.5% | 98.9% | 20.6% | 9.6% |

Comparação com os "Achados" do plano (explicação das diferenças em `conferir_oee2.py`, seção de reconciliação): a mesma conta do plano, no grão linha e sem pausa, reproduz os números dele ao minuto (Janela 429.920, Planejada 51.431, Vermelha 114.532, Amarela 60.681); a diferença para o valorizado do plano (203.276 contra 202.924) são 352 min de linhas sem motivo.

## 4) Roteiro de volta
Em ordem (cada passo desfaz o anterior; nada mexe em dado do SharePoint):
1. **Relatório:** apagar a pasta `GMS_Painel.Report/definition/pages/pg_oee2`, tirar `pg_oee2` do `pages.json` e voltar o menu das 10 páginas (`git revert` do commit da página).
2. **Medidas:** apagar a pasta de exibição `OEE2` da tabela `Medidas` (19 medidas), pelo painel de dados (selecionar as medidas, "Delete from model").
3. **`dEtapaOEE`:** apagar a tabela (botão direito, "Delete from model").
4. **`fHoraCheia` sem `Meta Cheia`** (é o script vigente de 11/11; cole inteiro):
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
				"Fr", DIVIDE ( MIN ( [Efim], ( [Value] + 1 ) * 60 ) - MAX ( [Sini], [Value] * 60 ), [Efim] - [Sini] ),
				"Mn", IF ( COALESCE ( [Min], 0 ) > 0, [Min], [Efim] - [Sini] )
				)
				VAR Calc2 =
				ADDCOLUMNS (
				Calc,
				"DataBI", [Data] + INT ( [Value] / 24 ),
				"HO", MOD ( [Value], 24 ),
				"TurnoBI", IF ( MOD ( [Value], 24 ) < 9, "1º Turno", IF ( MOD ( [Value], 24 ) < 17, "2º Turno", "3º Turno" ) )
				)
				VAR ComAlmoco =
				DISTINCT ( SELECTCOLUMNS ( FILTER ( Calc2, [Motivo Padrão] = "Almoço" ), "C", [Célula], "D", [DataBI], "T", [TurnoBI] ) )
				VAR Calc3 =
				ADDCOLUMNS (
				Calc2,
				"Refeicao", [Motivo Padrão] = "Almoço" || ( [HO] = SWITCH ( [TurnoBI], "1º Turno", 6, "2º Turno", 14, 21 ) && NOT ( ( [Célula], [DataBI], [TurnoBI] ) IN ComAlmoco ) )
				)
				RETURN
				SELECTCOLUMNS (
				Calc3,
				"Célula", [Célula],
				"Mangueira", [Mangueira],
				"Data BI", [DataBI],
				"Turno BI", [TurnoBI],
				"Hora", FORMAT ( MOD ( 5 + MOD ( [Value], 24 ), 24 ), "00" ) & ":00 - " & FORMAT ( MOD ( 6 + MOD ( [Value], 24 ), 24 ), "00" ) & ":00",
				"HoraOrdem", MOD ( [Value], 24 ),
				"Minutos", [Mn] * [Fr],
				"Meta", COALESCE ( [MetaHora], 0 ) * IF ( [Refeicao] && [Mn] > 0, MAX ( 0, [Mn] - 45 ) / [Mn], 1 ) * [Fr],
				"Real", COALESCE ( [Real0], 0 ) * [Fr],
				"Parado", MIN ( COALESCE ( [Par0], 0 ) * [Fr], [Mn] * [Fr] ),
				"Motivo", [Motivo],
				"Motivo Padrão", [Motivo Padrão],
				"Motivo 2", [Motivo 2],
				"Motivo 2 Padrão", [Motivo 2 Padrão],
				"ID Origem", [ID Origem],
				"Fração", [Fr]
				)

	relationship fHoraCheia_DataBI
		fromColumn: fHoraCheia.'Data BI'
		toColumn: dCalendario.Date

	relationship dTurno_fHoraCheia
		fromColumn: fHoraCheia.'Turno BI'
		toColumn: dTurno.Turno

```
5. **`dMotivoParada` de 2 colunas** (a versão aplicada em 13/10; cole inteiro):
```
createOrReplace

	table dMotivoParada

		column Motivo
			dataType: string
			summarizeBy: none
			sourceColumn: [Motivo]

		column Tipo
			dataType: string
			summarizeBy: none
			sourceColumn: [Tipo]

		partition dMotivoParada = calculated
			mode: import
			source =
				DATATABLE (
				"Motivo", STRING,
				"Tipo", STRING,
				{
				{ "TE - Tempo Excedido", "Excedido" },
				{ "Análise/Problema no tubo", "Falha" },
				{ "Falta de energia / ar", "Falha" },
				{ "Manutenção Corretiva", "Falha" },
				{ "Quebra de fio", "Falha" },
				{ "FC - Falta de Componentes (O-ring, sleeve, mola, adaptador...)", "Material" },
				{ "FI - Falta de Embalagem / Termoencolhível", "Material" },
				{ "Falta de Carretel", "Material" },
				{ "Falta de Lenon", "Material" },
				{ "Falta de Mandril", "Material" },
				{ "Falta de Mandril Soldado", "Material" },
				{ "Falta de Mangueira", "Material" },
				{ "Falta de fio - Bobinadeira", "Material" },
				{ "Falta de insulation", "Material" },
				{ "Falta de tubo", "Material" },
				{ "Resto de fio", "Material" },
				{ "AP - Alteracao de Planejamento", "Organizacional" },
				{ "Divergência do Tempo Padrão", "Organizacional" },
				{ "Falta de Demanda", "Organizacional" },
				{ "Falta de operador", "Organizacional" },
				{ "Falta de programação", "Organizacional" },
				{ "IT - Aguardando Instrucao de Trabalho / liberacao Engenharia", "Organizacional" },
				{ "Motivo Não Declarado", "Organizacional" },
				{ "Sem apontamento", "Organizacional" },
				{ "Ajuste da Máquina", "Processo" },
				{ "Alimentação de fio", "Processo" },
				{ "Emenda de Fita", "Processo" },
				{ "RT - Retrabalho", "Processo" },
				{ "Troca de Carretel", "Processo" },
				{ "Troca de Lenon", "Processo" },
				{ "Troca de boneca", "Processo" },
				{ "VR - Velocidade Reduzida", "Processo" },
				{ "AU - Auditoria (Qualidade / Seguranca)", "Programada" },
				{ "Almoço", "Programada" },
				{ "Amostra", "Programada" },
				{ "CA - Calibracao / Verificacao de Instrumento", "Programada" },
				{ "Execução Check List Lean", "Programada" },
				{ "LI - 5S", "Programada" },
				{ "Manut. Prod. Total (MPT)", "Programada" },
				{ "Manutenção Preventiva", "Programada" },
				{ "RF - Refeição", "Programada" },
				{ "Reunião", "Programada" },
				{ "Set-up", "Programada" },
				{ "TU - Troca de Turno", "Programada" }
				}
				)

	relationship c7bff530-b6e0-4649-bce4-7cecd6ed92ea
		fromColumn: 'Hora-Hora'.'Motivo Padrão'
		toColumn: dMotivoParada.Motivo

	relationship 2ecc65ff-ea99-4ae8-8358-30586480ca5f
		isActive: false
		fromColumn: 'Hora-Hora'.'Motivo 2 Padrão'
		toColumn: dMotivoParada.Motivo

	relationship eab0ca5a-394e-4adc-b15a-f81458e7e550
		fromColumn: Paradas_Montagem.Motivo
		toColumn: dMotivoParada.Motivo

```
6. Refresh e conferir `EVALUATE FILTER ( INFO.COLUMNS (), [State] <> 1 )` vazio.

## 5) O que o revisor tem de olhar
- **Pausa fixa e o 3º Turno BI.** O 3º Turno BI (22:00-05:00) de muitas máquinas só tem a hora extra do 2º turno (22:00-23:20): mediana de 41 min. A regra "todo turno de máquina com Real > 0 recebe MIN(45, minutos do turno)" dá pausa de até 45 min a esse pedaço de turno (160 turnos de máquina com menos de 240 min, 132 deles no 3º Turno BI, somam 4.335 min de pausa no período). Isso tira o pedaço do tempo de produção, mas o valorizado dele continua na conta (Janela - Σ P), então o OEE2 sem qualidade sobe cerca de 0,6 ponto (55,4% com a regra do plano contra 54,7% se turno com menos de 240 min não recebesse pausa). O plano pediu a regra assim e o script a segue; o `revisor` decide se pausa de turno curto deve ser proporcional ou se a hora extra deve ser somada ao turno de origem. O plano pediu a regra assim; o `revisor` decide se pausa de turno curto deve ser proporcional ou se a hora extra deve ser somada ao turno de origem.
- **Valorizado = Janela - Σ P** conta como valorizada a janela com meta zero, sem produção e sem parada (257 min, 0,1% da janela).
- **Vermelha residual** pode sair negativa num recorte pequeno (pausa fixa de 45 min maior que o parado declarado naquele turno); ela fecha a cascata, mas não é "parada declarada" (a declarada vermelha vai a 116.262 min no total).
- Regra de parada: o P usado é o capado na fatia (`fHoraCheia[Parado]`); o excedido (Real acima da meta) nunca abate parada de outra janela.
