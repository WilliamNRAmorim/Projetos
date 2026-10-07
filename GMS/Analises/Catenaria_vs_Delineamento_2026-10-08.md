# Catenária: Tabela 1 oficial × DM_WIREWINDING (08/10/2026)

Fontes: `Engenharia/Catenaria/Tabela1_catenaria_oficial.csv` × `Engenharia/DM_DATABASE/DM_WIREWINDING.xlsx` (59 linhas).
Chave: nº de fios (`WIRES_YARN`) → peso (`CATENARY_kg`) e distância D (`CATENARYD_mm`). Tolerância: 0,05 kg e 0,06 mm.
O app lê `CATENARY_kg` e `CATENARYD_mm` em `scr_Bobinadeira_1` (via `colDM_WIREWINDING`).

## Resultado
| Grupo | Linhas |
|---|---|
| Fio de aço (W...), conferem com a Tabela 1 | 24 |
| Fio de aço, divergem | 10 |
| Sem catenária ("-"): todas são fio têxtil (RT15210/15221/15252/15254, 01–06 fios), não se aplica | 25 |

Nenhum nº de fios do DM fica fora da faixa da tabela (3–22).

## Divergências (todas na distância D; o peso confere em todas)
| ID | PARTNUMBER | Fios | D no DM | D na tabela | Tipo |
|---|---|---|---|---|---|
| 27 | TOW0000210 | 10 | 114,1 | 114,3 | digitação (114,1 ≠ 114,3) |
| 32 | TMW0000210 | 10 | 114,1 | 114,3 | digitação |
| 47 | TMW0000209 | 9 | 50,80 | 101,6 | metade |
| 48 | THW0000209 | 9 | 50,80 | 101,6 | metade |
| 50 | TRW0000209 | 9 | 50,80 | 101,6 | metade |
| 49 | TRW0000208 | 8 | 44,45 | 88,9 | metade |
| 56 | TRW0000110 | 10 | 57,15 | 114,3 | metade |
| 57 | TRW0000210 | 10 | 57,15 | 114,3 | metade |
| 58 | THW0000210 | 10 | 57,15 | 114,3 | metade |
| 59 | THW0000210 (2ª linha) | 10 | 57,15 | 114,3 | metade; PN duplicado com o ID 58 |

## Leitura
1. **8 das 10 têm exatamente metade do D oficial** (44,45 = 88,9/2; 50,8 = 101,6/2; 57,15 = 114,3/2). Padrão de erro sistemático (possível valor de meia distância ou outra regra), não de digitação. Os IDs 47–50 e 56–59 são todos de bobina com ferramenta RB/LB/UB diferente: **perguntar à engenharia se esses PNs têm uma regra própria** antes de corrigir.
2. **IDs 27 e 32**: 114,1 no DM. A Tabela 1 diz 114,13 na imagem, mas a progressão (12,7 mm por fio) indica **114,3**. O DM não bate com nenhum dos dois. Confirmar o valor com a fonte original da tabela.
3. **IDs 58 e 59** têm o mesmo PN (THW0000210) e células com quebras de linha ("\n\n") no DM, sinal de linha duplicada ou colada da web. Limpar.
4. Células com quebra de linha (IDs 47, 48 e 59) podem quebrar comparações de texto no app (`PARTNUMBER`, `HOSE`).

## Impacto no app
`scr_Bobinadeira_1` usa `CATENARY_kg` e `CATENARYD_mm` do DM. Para os 8 PNs com D pela metade, a tela mostra uma distância máxima menor que a oficial. O peso não é afetado.

## Próximos passos
- William/Engenharia: confirmar o D oficial dos 8 PNs (metade é regra ou erro?) e o valor 114,3 da Tabela 1.
- Corrigir no SharePoint (`DM_WIREWINDING`) apenas depois dessa confirmação. Nada foi alterado no app nem nos dados.

## Decisão do William (08/10/2026)
1. D pela metade nos IDs 47-50 e 56-59: **erro**, corrigir para o valor da Tabela 1.
2. Valor correto é o que está na imagem da Tabela 1: **114,13** para 10 fios (vale também para os IDs 27 e 32, hoje 114,1). A hipótese de 114,3 fica descartada.

Lista pronta para aplicar no SharePoint: `Catenaria_correcoes_DM_WIREWINDING.csv` (ID, PN, D atual, D correto). Falta só aplicar na lista `DM_WIREWINDING` (e decidir o que fazer com a linha duplicada THW0000210, IDs 58 e 59).
