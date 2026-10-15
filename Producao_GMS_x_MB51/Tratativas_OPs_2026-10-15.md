# Tratativas das 10 OPs mais divergentes (GMS x MB51), a partir de 20/05/2026

Atualizado em 15/10/2026. Lance a lance em `tratativas_op.csv` (OP, referência da inspeção, data, metros, doc SAP, ação). As correções no GMS são do William; aqui só fica o registro.

| OP | Situação | O que fazer |
|---|---|---|
| 30276453 | Arrumada (William, 15/10) | Nada |
| 29118867 (2556-4) | Boa: 987,2 m = 181,1 na própria OP + 806,1 na **29147685** (SAP, 16 lançamentos de 11 e 12/06 que no GMS estão na 29118867). Refugo: o GMS tem 54,5 m no total; o SAP lançou 13,1 + 54,5 + 54,5 = 122,1 m (refugo em duplicidade, sobra 67,6 m) | No SAP: estornar 67,6 m de refugo (o 54,5 duplicado e o 13,1, docs 3019774697, 3019776810, 3019777623 em 15/06; confirmar qual par). No GMS: lances boa de 11 e 12/06 passam para a 29147685 |
| 27002870 (FC839B-04) | OP de dez/2025: os 8 lances (734,9 m) são de 05/12/2025 no SAP. No GMS só existe 1 m de refugo (Marcação Errada) de 28/08/2026 lançado nessa OP antiga | Fora do período (20/05). O refugo de 1 m de 28/08 está na OP errada: achar a OP certa |
| 29115542 (EC215-06L) | **Cancelada, virou 29133080.** Confere lance a lance: 7 lances boa (627,7 m) iguais aos 7 lançamentos da 29133080 em 02/06. O SAP lançou 680 + 151,2 na 29115542 e estornou (102) os dois. Refugo de 1,0 m (O - Pontas, 02/06 17:36) não foi lançado em nenhuma das duas | GMS: trocar a OP dos 7 lances para 29133080. SAP: lançar o refugo de 1,0 m |
| 29878642 (GH781-8) | No GMS é GH781-8 (inspeção, ficha 3309 e packing 574 m de 27/08 dizem isso). No SAP o refugo de 1,5 m foi lançado na 29878642 com material **FC735-08** (errado) e a boa (5 lances, 574 m) foi lançada na **29820550** (GH781-8) | Erro no SAP, não no GMS. SAP: estornar o refugo FC735-08 e lançar como GH781-8; boa: 29820550 → 29878642 (a 29820550 é de ficha 3213, finalizada em 08/2026, sem lance no GMS) |
| 29059118 (GH781-4) | Refugo (7,5 m) lançado nela no SAP e confere. A boa (10 lances, 572,5 m, 28/05) está no SAP na **29072012** | GMS: lances boa passam para 29072012 (confirmar se a OP certa é a 29072012) |
| 30337761 (GH781-8) | Todos os lances conferem em outras OPs: boa 509,9 m (7 lances de 04/10) = **30421672**; refugo 12,12 m (0,82+3,2+7,2+0,9) = 1 lançamento na **30406738** (que no GMS tem só 3,4 de refugo, e o 12,12 sobra lá) | Detalhe feito, só falta o William decidir em qual OP cada parte deve ficar |
| 29774579 e 29788690 (GH781-4) | Troca entre as duas: 13 lances (521,1 m) feitos na 29788690 em 05/08 19:38 a 20:43 (TH06) foram lançados no SAP na 29774579. Refugos e demais lances batem | GMS: passar os 13 lances da 29788690 para 29774579 (lista abaixo) |
| 29791112 (GH781-8) | No SAP só tem 10,5 m de boa e 2,7 m de refugo. Os outros 8 lances (508,4 m, 10/08, TM01) estão no SAP na **29805524**, que não existe no GMS | GMS: passar os 8 lances para 29805524 (OP precisa existir no GMS) |

## Lances a trocar de OP: 29788690 → 29774579

| Lance GMS | Data/hora | Metros | Doc SAP |
|---|---|---|---|
| Inspeção linha 3134 | 05/08/2026 19:38 | 36.7 | 3023323290/1 |
| Inspeção linha 3135 | 05/08/2026 19:43 | 46.6 | 3023323468/1 |
| Inspeção linha 3139 | 05/08/2026 19:55 | 56.5 | 3023323785/1 |
| Inspeção linha 3140 | 05/08/2026 19:58 | 42.1 | 3023323846/1 |
| Inspeção linha 3141 | 05/08/2026 20:02 | 35.3 | 3023323955/1 |
| Inspeção linha 3142 | 05/08/2026 20:04 | 26.5 | 3023324045/1 |
| Inspeção linha 3144 | 05/08/2026 20:13 | 87.6 | 3023324239/1 |
| Inspeção linha 3146 | 05/08/2026 20:21 | 12.6 | 3023324735/1 |
| Inspeção linha 3148 | 05/08/2026 20:28 | 84.6 | 3023325052/1 |
| Inspeção linha 3150 | 05/08/2026 20:35 | 15.3 | 3023325191/1 |
| Inspeção linha 3151 | 05/08/2026 20:38 | 36 | 3023325302/1 |
| Inspeção linha 3153 | 05/08/2026 20:41 | 30.2 | 3023325306/1 |
| Inspeção linha 3154 | 05/08/2026 20:43 | 11.1 | 3023325487/1 |

Total: 13 lances, 521,1 m. Os demais lances (inclusive para 29059118, 29115542, 29118867, 29791112 e 30337761) estão em `tratativas_op.csv`.
