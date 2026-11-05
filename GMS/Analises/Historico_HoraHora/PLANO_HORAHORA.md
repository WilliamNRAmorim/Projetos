# Carga da lista HoraHora_Historico (Hora-Hora pré-GMS)

Objetivo: levar para o BI o Hora-Hora de antes do GMS (pasta `9_HORA HORA`, hoje `Dados_Historicos/HoraHora_pre_GMS/`), numa lista do SharePoint
`HoraHora_Historico` (site OperationsGuaratingueta). A carga é feita pelo GitHub Copilot com o navegador nativo dele; o Claude preparou a lista, os dados e o prompt.
Pedido do William em 05/11/2026. A lista original `Hora-Hora` (do app, 2026 em diante) **não é tocada**.

## Fontes (cópia só leitura, não alteradas)
- `Dados_Historicos/HoraHora_pre_GMS/Banco_de_Dados_Hora_Hora_2023-08_a_2025-09.xlsx`, aba `Dados`: 31.878 linhas. Cobertura: ago/2023 a mar/2024 completa, **buraco de abr/2024 a jun/2025**, depois jul a set/2025 parcial.
- `Dados_Historicos/HoraHora_pre_GMS/Banco_de_Dados_Espiral_2024-03_a_2026-01.xlsx`, aba `Dados`: 7.320 linhas, só a máquina Spiral (mar/2024 a jan/2026, mais 10 linhas de jul/2026).

## Lista `HoraHora_Historico`
Colunas: `Title` (nº da linha, 1 a 39.198; 1 a 31.878 = banco geral, 31.879 a 39.198 = Spiral) · `Data` (só data) · `Turno` ("1º", "2º", "3º") · `Celula` · `Hora` (janela) ·
`Mangueira` · `Meta` · `MetaAcum` · `RealHora` · `RealAcum` · `Diferenca` · `TempoParado` (min) · `Motivo` · `Motivo2` · `Comentario` · `Origem` ("Banco geral" ou "Espiral") · `Alerta`.
Valores arredondados a 2 casas. Em `Comentario` da Spiral foram juntados "Comentário / Ação", "Ação" e "Comentário" separados por " | ".

## Tratamentos (nada foi descartado)
- 126 linhas da TH-07 (21/08/2025 a 05/09/2025) vinham com "TH-07" na coluna Turno e Célula vazia: ficou `Celula = TH07`, `Turno` vazio e `Alerta` "Turno nao informado...".
- 9 linhas da TH-7 vinham deslocadas (sem Data): `Data` vazia, `Celula = TH07` e `Alerta` "Sem data...".
- Linhas totalmente vazias foram ignoradas. 135 linhas têm `Alerta`.
- Meta e Real do histórico não passaram pelas regras de higienização do GMS (Minutos, motivo ND/NT etc.): são o dado bruto da planilha. Não somar com a `Hora-Hora` sem tratar.

## Arquivos desta pasta
- `carregador_hh.js`: `__carregarHH(linhas)` (pula Title existentes) e `__conferirHH(a, b)`.
- `dados/hh_01.js` a `hh_20.js`: 2.000 linhas cada (a última tem 1.198), geradas por `hh.py` a partir das duas planilhas.
- `hh_manifest.json`: faixa de Title, linhas e somas esperadas por arquivo, e o total.
- `PROMPT_COPILOT_HORAHORA.md`: o prompt para o Copilot.

## Totais esperados
39.198 linhas; RealHora 1.811.514,39; Meta 4.670.179,95; TempoParado 918.099,70.

## Progresso
| Arquivos | Status |
|---|---|
| Teste (Title 1 a 3) | gravado e conferido em 05/11/2026 pelo Claude |
| hh_01 a hh_20 (Title 4 a 39.198) | pendente (Copilot) |

Depois da carga: ligar a lista ao modelo (`fHoraHora` histórica separada, sem mexer na `Hora-Hora`) e ao `dCalendario`; refresh e publicação são do William, no Desktop.
