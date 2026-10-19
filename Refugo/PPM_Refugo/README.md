# PPM de refugo — análise de 01/10/2026

Fonte: planilhas `Apontamento de Produção de Mangueiras` 2024 e 2025_1 (jan/2024 a 30/09/2026) e a medida `Refugo PPM` do modelo Power BI (análise de 05/08). PPM = refugo / (aprovado + refugo) x 1.000.000.

| Período | Aprovado (m) | PPM |
|---|---|---|
| 2024 | 2,02 mi | 13.535 |
| 2025 | 1,85 mi | 3.876 |
| Jan-Abr/2026 | 0,66 mi | 3.823 |
| Mai-Set/2026 | 0,65 mi | 10.090 |

## Achados
- Base real ≈ 3.900 PPM (2025 e jan-abr/26). Em maio/26 quebra e volta ao patamar de 2024.
- Causas que mais cresceram (base 2025 -> mai-set/26): C carroço/ondulação 644 -> 2.778; O pontas 888 -> 2.199; A quebra de fio 394 -> 1.337; E trança aparente 400 -> 1.134; F bolhas 13 -> 830 (quase só jun/26).
- Alta nos 3 turnos e em todas as famílias de mangueira; top-10 linhas = 17% do refugo; sem linhas >= 100 m o PPM ainda é 9.034 (base 3.417).
- Linhas com algum refugo: 48% -> 77%; mediana por linha 0 -> 2 m. Pode ser mudança de registro (papel saiu em maio) e não só piora real.
- GMS x planilha divergem de mar a jun/26 e convergem em jul/26. Jul/26 na planilha tem só 86 linhas (~23% do volume).

## Em aberto
- Quem preenche a planilha desde maio: operador à parte ou cópia do GMS? Define se as séries são independentes.
- Agosto e setembro do GMS (não tenho o modelo desde 05/08).
- Para público externo (deck EUA) não mostrar PPM de refugo (GMS_Licoes 7.6).

## Arquivos
- `PPM_2024_2026.png` — série mensal planilha + GMS
- `ppm_mensal.csv` — PPM por mês (separador ;)
- `ppm_por_causa.csv` — PPM por causa A-P por período
