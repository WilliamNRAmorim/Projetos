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

## Divergência do período 20/05 a 20/09/2026 (por mangueira, SAP − GMS)

| | SAP a mais | SAP a menos | Total em módulo | Líquido |
|---|---|---|---|---|
| Antes das tratativas | 2.960,1 m | −1.571,1 m | 4.531,2 m | +1.389,0 m |
| Depois das tratativas (OPs de `ops_tratadas.csv` zeradas) | 2.475,8 m | −804,9 m | 3.280,7 m | +1.670,9 m |

Script: `divergencia_periodo.py`. As OPs 30276453 e 30337761 são depois de 20/09 e ficam fora desse período.

## Segundo lote (15/10): tratativas combinadas com o William

Lances um a um em `tratativas_lote2.csv`; pendências em `pendencias_lancar.csv`.

| OP | O que é e o que fazer |
|---|---|
| 29733210 (EC215-08L) | **Pendente (William).** Os 4 lances do SAP (454,9 m, 03/08, docs 3023117833, 3023118150, 3023119144, 3023119428) não estão no GMS em outra OP: lançar no GMS. Os 2 refugos do GMS (1,2 + 1,1 m, 03/08 10:17) não existem no SAP, nessa OP nem em outra |
| 29963502 → 29963530 (EC215-10L) | GMS: trocar a OP dos 4 lances de 25/08 (415,2 m, linhas 4632, 4635, 4639, 4640) para 29963530. Os 3 lances de 26/08 que o GMS tem na 29963530 (109,4 / 103,1 / 98,8 m) estão no SAP em **29894895**, **29894896** e **29878655** (EC118-10L, mangueira diferente: conferir). O refugo de 0,8 m da 29963530 está certo. O refugo da 29963502 (0,6 + 0,9 + 0,8 = 2,3 m) está no SAP na **29963527** (doc 3024755763, 27/08) |
| 29259769 ↔ 29259772 (FC839B-04) | Troca de 6 lances (508,1 m): GMS 29259769 → 29259772 (linhas 1488, 1489, 1491, 1492, 1493, 1494). Falta fechar: o lance de 120,6 m (linha 1546, 24/06 00:16) do GMS na 29259772 está no SAP na **29259769**, e o de 35,5 m (linha 1487, 23/06 11:57) do GMS na **29259771** também está no SAP na 29259769. Refugo da 29259772 duplicado no SAP (1,5 m a mais) |
| 29788415 (EC118-06L) | GMS: linhas 3182 (122,6) e 3186 (142,2) → OP 29774167; linhas 3187 (49,5), 3188 (34,2), 3189 (38,5) → OP 29774166 |
| 29048968 (GH681-6) | GMS: linha 16627 (177,4 m) → OP 28913388; linha 16625 (151,4 m) → OP 28913387 |
| 29788884 (HC139-7) | GMS: 5 lances de 30078414 (linhas 5601 a 5605, 224,3 m) → OP 29788884. Sobram 51,0 m do SAP na 29788884 sem par (o SAP tem dois lançamentos de 51 m, um em cada OP) |
| 30092889 (HC139-7_S-GX) | **Pendente (William).** 7 lances do SAP de 24/09 (313,5 m) sem lance no GMS: lançar no GMS |
| 29260119 (EC215-08L) | **Pendente (William).** 6 lances do SAP de 27/06 (270,1 m) sem lance no GMS: lançar no GMS |

Divergência depois das tratativas dos dois lotes: SAP a mais 2.273,5 m, SAP a menos −701,9 m, total 2.975,4 m (as pendentes continuam contando).

## Correções gravadas no GMS (15/10/2026)

Os 80 lances de `correcoes_gms_2026-10-15.csv` tiveram o OP_ID trocado na lista RegistrosInspeção (conferido depois: 80 de 80 na OP nova). A boa do GMS agora é igual à boa do SAP em todas as OPs tocadas, exceto: 29788884 / 30078414 (51,0 m de lançamento duplicado no SAP) e 29963530 (−98,8 m: o SAP lançou o lance na 29878655, EC118-10L). Ficaram de fora: 30337761, 29878642, refugos e as pendentes 29733210, 30092889 e 29260119.

## Refugo e fichas (15/10, fim do dia)

- `TiposErros` ids 4311, 4312 e 4313 (refugo 0,6 + 0,9 + 0,8 m de 25/08): OP_ID trocado de 29963502 para 29963527, igual ao SAP (doc 3024755763). Para desfazer, voltar o OP_ID para 29963502.
- 29115542: o refugo de 1,0 m (O - Pontas, 02/06 17:36) não foi lançado no SAP, nem na 29115542 nem na 29133080. Pendente de lançamento no SAP.
- 29733210: refugos do GMS (1,2 + 1,1 m) aguardam o aprendiz lançar no SAP; falta definir a OP.

- Refugos sem par no SAP excluídos do GMS (lixeira do SharePoint, `TiposErros`): id 2643 (29115542, 1,0 m O - Pontas, 02/06), id 3763 (29733210, 1,2 m O - Pontas) e id 3764 (29733210, 1,1 m A - Quebra de Fio, 03/08). Conferi que não há refugo de 1,2 ou 1,1 m dessa mangueira em 04/08, no GMS nem no SAP. Para restaurar: lixeira do site.
- Com isso, os lances de produção boa e os refugos dos lotes 1 e 2 ficaram espelhando o SAP, exceto o que é do SAP (refugo duplicado, 51 m, 98,8 m) e as pendentes de lançar no GMS (29733210, 30092889 e 29260119).

## P03 e P06 corrigidos no GMS (15/10, noite)

- P03: item 14424 de `RegistrosInspeção` (98,8 m, 26/08 17:45) passou de OP 29963530 para 29878655 e a Mangueira do lance de EC215-10L para EC118-10L. Fichas: 3391 de 616,1 para 517,3 m; 3351 de 425,1 para 523,9 m. Para desfazer: OP_ID 29963530, Mangueira EC215-10L e as quantidades antigas.
- P06: itens 14479, 14480, 14481, 14482 e 14483 (574,0 m, 27/08) passaram de OP 29878642 para 29820550. Fichas 3309 e 3213 aguardam decisão (P13).
- P07: sem ação; o GMS já espelha o SAP (10,5 m na 29791112).

## P13: fichas 3309 e 3213 (15/10)

Ficha 3309 passou da OP 29878642 para 29820550 (574 m e packing mantidos). Ficha 3213 (500 m, sem lances e sem lançamento do SAP) foi para a lixeira; backup em `backup_ficha_3213_29820550.json`. O refugo de 1,5 m segue em `TiposErros` na 29878642, igual ao SAP (material FC735-08, pendência P05).

## Divergência geral de 20/05 a 20/09/2026, recalculada com o GMS de 15/10

Reconferência feita com os CSVs corrigidos (`aplicar_correcoes_gms_nos_csv.py`: 86 lances movidos de OP, 3 refugos movidos e 3 excluídos). A divergência concreta mantém os erros do SAP.

| | 14/10 (antes) | 15/10 (agora) |
|---|---|---|
| SAP a mais | 2.960,1 m | 2.725,9 m |
| SAP a menos | −1.571,1 m | −706,1 m |
| Total em módulo | 4.531,2 m | 3.432,0 m (−24%) |
| OPs divergentes | 235 | 216 |

Do que sobrou: 733,9 m são da OP 27002870 (OP de dez/2025 que entra no período só por causa de 1 m de refugo do GMS em 28/08; não é divergência real); cerca de 1.684 m são lances do SAP que você vai lançar no GMS (P08 454,9, P09 313,5, P10 270,1 e P16 645,3).

Fichas: 3168 (OP corrigida de 28788420 para 29788420) e 3076 (OP vazia preenchida com 29733207).

## Lote 3 de lances (15/10, noite): 57 de 68 gravados

57 lances de `tratativas_lote3_lances.csv` já tiveram o OP_ID trocado no SharePoint; o sistema de permissões bloqueou os 11 restantes (itens 14984, 14986, 14352, 14355, 14357, 14401, 14406, 14408, 14760, 15186 e 14924: OPs 29963522, 29963533, 29994196, 30007593, 30063656 e 30063851). Os itens pendentes só serão gravados se a OP atual ainda for a de origem. Ficam pendentes também as exclusões do P22 e o ajuste de `quantidade_extracao` das fichas das 59 OPs envolvidas.

## Lote 3 concluído e divergência de 20/05 a 20/09 (15/10, noite)

Gravados no SharePoint: 68 lances com OP trocada, 57 fichas com `quantidade_extracao` ajustada (`correcoes_ficha_lote3_2026-10-15.csv`), refugo 4377 e fichas 654 e 2775 na lixeira. Reconferência com o GMS corrigido:

| | 14/10 | 15/10 (agora) |
|---|---|---|
| SAP a mais | 2.960,1 m | 1.992,0 m |
| SAP a menos | −1.571,1 m | −705,1 m |
| Total em módulo | 4.531,2 m | 2.697,1 m (−40%) |
| OPs divergentes | 235 | 181 |

## Lote 5 (15/10): casamento por lance nas OPs com lances nos dois lados

43 lances trocados de OP no GMS (`tratativas_lote5_lances.csv`), 21 OPs, 15 fichas com `quantidade_extracao` ajustada; ficha 3050 passou para a OP 29701289 (SAP, 233,4 m); ficha 2612 (29086344) foi para a lixeira (todos os lances foram para outras OPs). Foram deixados fora 14 lances de 22/09 (OPs 30206907, 30206908, 30206915, 30206916), porque a OP é posterior a 20/09.

Divergência bruta por OP (soma do módulo de cada OP, incluindo OPs só no SAP), 20/05 a 20/09: 37.087 m (14/10) para 13.383 m (agora), −64%. SAP a mais 26.960 → 12.356 m; SAP a menos −10.128 → −1.027 m.

## 19/10 - 29847619 / 29847701
Troca de 4 lances entre as duas OPs corrigida no GMS (itens 13538, 13539 -> 29847701; 13525, 13528 -> 29847619). Fichas 3239 = 524,1 m e 3249 = 475,1 m. Confere com SAP e BD Packing List (958 e 960).

## Conferencia_SAP: trocas aplicadas em 19/10/2026

29 lances de RegistrosInspeção e 4 refugos (TiposErros 6026 a 6029) trocaram de OP para espelhar o SAP; fichas ajustadas (3919, 3924, 3932, 3921, 3973, 3895, 3958, 3940).
- 30433523 ↔ 30433525: lances 18152 a 18160 (6) para a 30433525; 18063 a 18072 (8) para a 30433523.
- 30447656 → 30424228: lance 18017 (137,6 m).
- 30479026 → 30424233: lances 18468, 18506 a 18510, 18513, 18515, 18518, 18520 (231,8 m).
- 30462708 → 30447069: 18339, 18340; → 30433752: 18337, 18338; refugos 6026 a 6029 de 30433752 para 30462708.
Para desfazer, voltar o OP_ID ao de origem. Pendentes: lance 17870 (86,8 m, OP 30447770) e SAP 67,8 m na 30406468; troca 17734/17735/17869 não aplicada; 21 OPs finalizadas sem packlist (cabine).

### Segunda rodada Conferencia_SAP (19/10/2026)
- 17734, 17735 (30406468 → 30447770) e 17869 (30447770 → 30406468). Fichas 3888 e 3902. Pendente: 17870 (86,8 m) e SAP 67,8 m na 30406468.
- Troca completa 30424231 ↔ 30351277: 31 lances (676,0 m) e 14 lances (506,5 m). Fichas 3887 e 3806.
- Lance 18709 (30529216): 16,9 → 16,1 m, igual ao SAP. Ficha 3996 (532,0 m).
- Fora: 126/109 (SAP lançou refugo de 12,5 m como boa na 30223117), 140, 147 e os 21 sem packlist.

## Rodada de 28/10/2026 (conferência refeita com SharePoint e MB51 de 28/10)

Regra do William (28/10): **sempre corrigir o GMS, nunca o SAP.** Só corrigir o que tem prova e paralelo no histórico; o resto fica aqui para ele ajudar e para a próxima vez sair certo.

**Prontas (troca de OP do lance, prova por valor, hora e doc SAP) — em `registros/correcoes_gms_2026-10-28.csv`; fichas em `correcoes_ficha_28out_previstas.csv` (ficha = soma dos lances antes, então acompanha). Gravação no SharePoint bloqueada pelo sistema; GRAVADAS em 28/10 com o "Libero" do William, releitura conferida (6 lances e 6 fichas, tudo status 204):**
- GH781-8: 30206916 → 30206915 (65,8 m); 30406737 → 30338597 (122,5 m).
- GH781-4: 4 lances (188,8 m) 30495038 → 30495036.

**Não sei resolver (William ajuda):**
- 30495036: 30,4 m de boa (doc 3028369639) e 21,9 m de refugo (doc 3028431649, 19/10) só no SAP, sem par no GMS.
- 30495038: SAP lançou 553,9 m e estornou no mesmo dia (docs 3028368920 e 3028649234, usuário S122684, outro dos demais). No GMS ficam 2 lances de boa (36,2 e 6,9 m) e ~40 refugos que o SAP não tem. OP ainda REL no COOIS. Perguntar a S122684 o motivo do estorno.
- 30545859 (HC139-7): SAP 803,4 m, GMS 221 m (+582 m). Causa não vista.
- 30337761 (GH781-8, −522 m) e 30406478 (GH493-12, −316 m): sem lançamento na MB51. Para a 30337761 a boa pode estar na 30421672 (15/10).
- COOIS não traz várias OPs do GMS (ex. 29733203, 29118867, 30206916): motivo desconhecido.

**OP 30545859 (HC139-7, TM04) — analisada em 28/10, sem correção feita:**
- GMS tem 6 lances de boa (212,6 m, TM04, 22/10 21:00 a 21:34) e 4 refugos (8,4 m); todos batem com o SAP (docs 3028775085 a 3028776769 e refugo 3028825534).
- O SAP tem mais **12 lançamentos de boa em 27/10, 582,4 m, todos do usuário U395462** (docs 3029003870 a 3029010...). Nenhum lance do GMS tem esses valores em outra OP: as coincidências de valor (32,6; 53,2; 51,0) são acaso, em OPs de outras mangueiras.
- As OPs vizinhas de HC139-7 conferem por completo: 30549004 (TM04, 26/10, 14 lances, 652,9 m) e 30575953 (HC139-7_S-GX, TM04, 26/10, 12 lances, 631,5 m).
- COOIS: OP TECO, confirmado 803,4 m para ordem de 680 m (acima da ordem).
- Hipótese (não provada): produção de 27/10 sem apontamento de inspeção no GMS (ou apontada fora do app). Corrigir seria criar lances no GMS, e não invento lance. **William: confirmar se houve produção e quem é U395462.** A 30575954 (TH05, +143,5 m) pode ter a mesma causa.
- **Ficha_producao (28/10, resposta à hipótese acima):** a ficha 3988 (OP 30545859, mangueira "HC139-7 250 MTS", TM04, Finalizado 22/10) diz que só **230 m** chegaram à bandagem, vulcanização, debandagem e extração (a inspeção do GMS tem 221 m, coerente); mandril e trançagem fizeram 680 m, cobertura 400 m. Logo **o GMS está certo e os 582,4 m de 27/10 no SAP não são produção desta OP**. As fichas 4091 (30549004: 680/652,9) e 4106 (30575953: 680/631,5) também conferem com o SAP.
- Candidata a dona dos 582,4 m: **30592754** (ficha 4107, HC139-7, TM04, 610 m, em Extr./Teste em 28/10, ainda **sem nenhuma inspeção no GMS**). Não provado. Conferir quando ela tiver lances: se os 12 valores (51,0; 48,9; 32,8; 28,3; 42,3; 53,2; 32,6; 24,6; 68,9; 70,7; 66,5; 62,6) aparecerem nela, o erro é do SAP (lançado na OP errada) e **não se mexe no GMS**. Mesma ideia vale para a 30575954 (ficha 4094: só 330 m, GMS 329,5, SAP 473).
- **Busca dos 12 valores (28/10, feita no GMS inteiro e na MB51 desde 01/09):** nenhuma OP do GMS tem esses lançamentos (no máximo 2 valores em comum por acaso; sem OP com soma 582,4 m nem 12 lances parecidos, e a 30592754 segue sem inspeção). Na MB51 só a 30545859 tem os 12. Fica aguardando a 30592754 receber lances.
