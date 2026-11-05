# Dados_Historicos

Dados de produção de antes do GMS e planilhas de controle usadas como referência (a "verdade" de conferência).

| Pasta | O que tem | Como ler |
|---|---|---|
| `HoraHora_pre_GMS/` | Hora-Hora de antes do GMS. `Banco_de_Dados_Hora_Hora_2023-08_a_2025-09.xlsx` (aba `Dados`, 31.878 linhas, 1 linha por célula × data × turno × hora: meta, real, tempo parado, motivo). `Banco_de_Dados_Espiral_2024-03_a_2026-01.xlsx` (aba `Dados`, 7.320 linhas, só a máquina Spiral). | Colunas: Data, Turno, Célula, Hora, Mangueira, MFG/META, Meta Acum, Real. Hora, Real. Acum, Diferença, Tempo Parado (min), Motivo, Motivo 2, Comentário/Ação. A aba `Sheet1` do banco geral é rascunho. |
| `HoraHora_pre_GMS/ferramenta_excel/` | `Hora-Hora_Spiral_2024_v388_15-01-2026.xlsm`: a planilha antiga com macros (modelo, uma aba por máquina, consulta e resumo semanal). Guardada como referência da regra antiga; não tem série histórica. | Só consulta. |
| `Eficiencia_Processo/2026/` | `Eficiencia-<Mês>2026.xlsx` (jan a nov): "Controle do Processo Mangueira", **uma aba por dia** (`01`, `02`, ...). Cada aba traz, por máquina de trançagem (TH1..TH7, TM1, TM4, TO4, Spiral) e por turno: horas, mangueira, planejado, real e % e o motivo da parada; e o bloco por etapa (Bobinadeira 1 e 2, Trançadeiras, Extrusora 1 (tubo), Extrusora 2 (cobertura), Bandagem, Debandagem, Solda de Mandril, Extrusora 3, Extração): planejado e real por turno e total. | `Eficiencia-Set2026b.xlsx` é a versão corrigida de setembro (o "b" é de William). As abas `Planilha1..3` e `Planilha2` dos primeiros meses são resumos; a aba `01` de alguns meses tem linhas extras de resumo. |

Notas: o William considera as planilhas de Eficiência a fonte de conferência (cerca de 99% de confiança) para o BI e a ficha de produção. Nada aqui é lixo: nada foi apagado na reorganização de 05/11/2026 (a pasta `9_HORA HORA` foi movida e renomeada para `HoraHora_pre_GMS`).
