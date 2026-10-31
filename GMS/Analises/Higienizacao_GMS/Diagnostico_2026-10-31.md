# Diagnóstico do GMS — Fase 1 (só leitura) · 2026-10-31

Gerado por `diagnostico_gms.py` (nesta pasta). **Só contagens e IDs de amostra; nenhuma linha de produção.** Nada foi gravado no SharePoint nem em `GMS/IA/dados`. Plano: `PLANO.md`. Regras de turno: NORMA de 27/10/2026 (MEL-250).

## 0. Fontes e pares duplicados

| Arquivo | Linhas | Primeira data | Última data | Arquivo gravado em |
|---|---|---|---|---|
| ficha_producao.csv | 2694 | 2025-11-29 | 2026-10-06 | 2026-10-09 |
| RegistrosInspeção.csv | 16542 | 2025-11-11 | 2026-10-02 | 2026-10-06 |
| TiposErros.csv | 5434 | 2025-11-11 | 2026-10-02 | 2026-10-06 |
| mb51.xlsx (Sheet1) | 113122 | 2024-11-04 | 2026-10-21 | 2026-10-24 |
| BD Packing List.xlsx | 9965 | 2026-05-04 | 2026-10-02 | 2026-10-06 |

**Os exports são fotografias antigas:** a ficha vai só até 06/10, a inspeção e os erros até 02/10 e a MB51 até 21/10. A janela da NORMA (05 a 27/10) só está coberta de verdade na ficha por 05 e 06/10.

**Pares `.txt` / `.csv` / `.xlsx`:** os `.txt` da pasta têm 190 a 260 bytes e guardam só o link do SharePoint; não há conteúdo para comparar. Pares com conteúdo de verdade: nenhum com `.csv` e `.xlsx` do mesmo nome. Único caso de dado repetido em dois arquivos: a MB51 está em `mb51.xlsx` (24/10) e na aba `MB51` da `Máscara de produção.xlsx` (06/10). Comparação abaixo.
| Medida | Valor |
|---|---|
| Itens na aba MB51 da Máscara (documento+item) | 109953 |
| Itens no mb51.xlsx | 113120 |
| Só na Máscara | 0 |
| Só no mb51.xlsx | 3167 |
| Período da Máscara | 2024-11-04 a 2026-10-01 |
| Período do mb51.xlsx | 2024-11-04 a 2026-10-21 |

Dos 109953 itens em comum, **0** têm quantidade diferente. Conclusão: usar o `mb51.xlsx` (mais novo e mais completo); a diferença é de período, não de conteúdo, se o número acima for 0.

## 1. Duplicados

Packing List: `ID` sozinho se repete por desenho (um ID tem várias fatias), por isso a chave é ID+Slice.
| Fonte | Chave | Grupos repetidos | Linhas a mais | Amostra de IDs |
|---|---|---|---|---|
| ficha_producao | ID | 0 | 0 | — |
| ficha_producao | OP | 0 | 0 | — |
| RegistrosInspeção (linha inteira) | OP_ID+Quantidade+Diametro_Interno+Diametro_Externo+Concentricidade+DataHoraInspecao+TurnoTeste+Criado+Mangueira+CodigoDefeito+Trançadeira+cabine_teste | 0 | 0 | — |
| RegistrosInspeção (OP+hora+qtd+cabine) | OP_ID+DataHoraInspecao+Quantidade+cabine_teste | 18 | 18 | 27611918, 27770004, 27796424, 28205089, 28467640 … (+13) |
| TiposErros (linha inteira) | OP_ID+CodigoErro+Quantidade+Criado+DataHoraRefugo+Trançadeira+Turno Erro+cabine_teste | 84 | 92 | 27611918, 27613224, 27654980, 27673912, 27719543 … (+62) |
| TiposErros (OP+código+qtd+criado) | OP_ID+CodigoErro+Quantidade+Criado | 84 | 92 | 27611918, 27613224, 27654980, 27673912, 27719543 … (+62) |
| MB51 (documento+item) | Material Document+Material Doc.Item | 0 | 0 | — |
| Packing List (ID+Slice) | ID+Slice | 0 | 0 | — |

Linhas a mais = linhas que sobrariam se cada grupo ficasse com uma. OP_ID/Order são identificadores de ordem, não dado pessoal.
**Hora-Hora: NÃO EXECUTADO** (sem export local; ver seção 10).

## 2. Campos obrigatórios vazios

| Fonte | Campo | Linhas | Vazios | % | Amostra de IDs/linha |
|---|---|---|---|---|---|
| ficha (todas) | OP | 2694 | 13 | 0.5% | 2305, 3076, 3171, 3201, 3839 … (+8) |
| ficha (todas) | Mangueira | 2694 | 9 | 0.3% | 3171, 3839, 3840, 3850, 3892 … (+4) |
| ficha (todas) | status_processo | 2694 | 0 | 0.0% | — |
| ficha (todas) | Bitola | 2694 | 2 | 0.1% | 833, 1215 |
| ficha (Finalizado) | data_hora_final_mandril | 2647 | 2 | 0.1% | 3116, 3120 |
| ficha (Finalizado) | data_hora_final_trancadeira | 2647 | 6 | 0.2% | 686, 2419, 2654, 2656, 2864 … (+1) |
| ficha (Finalizado) | data_hora_final_cobertura | 2647 | 4 | 0.2% | 686, 2169, 2172, 2864 |
| ficha (Finalizado) | data_hora_final_vulcanizacao | 2647 | 4 | 0.2% | 2365, 2619, 2850, 2864 |
| ficha (Finalizado) | data_hora_final_debandagem | 2647 | 548 | 20.7% | 686, 691, 693, 695, 697 … (+543) |
| ficha (Finalizado) | data_hora_final_extracao | 2647 | 283 | 10.7% | 784, 791, 797, 799, 824 … (+278) |
| ficha (Finalizado) | quantidade_mandril | 2647 | 1 | 0.0% | 2887 |
| ficha (Finalizado) | quantidade_extracao | 2647 | 211 | 8.0% | 686, 691, 693, 695, 697 … (+206) |
| ficha (Finalizado) | Turno_mandril | 2647 | 2 | 0.1% | 3116, 3120 |
| ficha (Finalizado) | Turno_Extr/Teste | 2647 | 1870 | 70.6% | 686, 691, 693, 695, 697 … (+1865) |
| RegistrosInspeção | OP_ID | 16542 | 0 | 0.0% | — |
| RegistrosInspeção | Quantidade | 16542 | 0 | 0.0% | — |
| RegistrosInspeção | DataHoraInspecao | 16542 | 0 | 0.0% | — |
| RegistrosInspeção | TurnoTeste | 16542 | 21 | 0.1% | 0, 1, 2, 3, 4 … (+16) |
| RegistrosInspeção | Mangueira | 16542 | 2141 | 12.9% | 0, 1, 2, 3, 4 … (+2136) |
| RegistrosInspeção | cabine_teste | 16542 | 15862 | 95.9% | 0, 1, 2, 3, 4 … (+15857) |
| TiposErros | OP_ID | 5434 | 0 | 0.0% | — |
| TiposErros | CodigoErro | 5434 | 0 | 0.0% | — |
| TiposErros | Quantidade | 5434 | 1 | 0.0% | 183 |
| TiposErros | Criado | 5434 | 0 | 0.0% | — |
| TiposErros | DataHoraRefugo | 5434 | 358 | 6.6% | 0, 1, 2, 3, 4 … (+353) |
| TiposErros | Turno Erro | 5434 | 971 | 17.9% | 0, 1, 2, 3, 4 … (+966) |
| TiposErros | Trançadeira | 5434 | 935 | 17.2% | 0, 1, 2, 3, 4 … (+930) |
| MB51 | Order | 113122 | 380 | 0.3% | 5019527628, 5019897103, 5019897161, 5019897169, 5019971507 … (+172) |
| MB51 | Material | 113122 | 3 | 0.0% | — |
| MB51 | Posting Date | 113122 | 3 | 0.0% | — |
| MB51 | Quantity | 113122 | 0 | 0.0% | — |
| MB51 | Unit of Entry | 113122 | 0 | 0.0% | — |
| MB51 | User Name | 113122 | 3 | 0.0% | — |
| Packing List | PN | 9965 | 0 | 0.0% | — |
| Packing List | QTd (m) | 9965 | 0 | 0.0% | — |
| Packing List | Timestamp | 9965 | 0 | 0.0% | — |
| Packing List | Cabine | 9965 | 9965 | 100.0% | 0, 1, 2, 3, 4 … (+1491) |

Os campos de ficha só são obrigatórios na etapa já feita; `data_hora_final_*` e `quantidade_*` vazios em ficha Finalizado indicam etapa pulada ou ficha aberta direto numa etapa seguinte (a regra de quais etapas cada mangueira usa é a Fase 2). `TiposErros.DataHoraRefugo` vazio é antigo e não é erro (a data vale por `Criado`).

## 3. Datas impossíveis

| Verificação | Futuras / fim<início / longas | Antes de 11/2025 | Amostra de IDs |
|---|---|---|---|
| ficha.data_hora_final_mandril | 0 | 0 | — |
| ficha: final antes do início (mandril) | 1 | — | 1463 |
| ficha: etapa com mais de 7 dias (mandril) | 0 | — | — |
| ficha.data_hora_final_tubo | 0 | 0 | — |
| ficha: final antes do início (tubo) | 0 | — | — |
| ficha: etapa com mais de 7 dias (tubo) | 1 | — | 654 |
| ficha.data_hora_final_trancadeira | 0 | 0 | — |
| ficha: final antes do início (trançagem) | 0 | — | — |
| ficha: etapa com mais de 7 dias (trançagem) | 5 | — | 791, 2710, 3612, 3619, 3754 |
| ficha.data_hora_final_cobertura | 0 | 0 | — |
| ficha: final antes do início (cobertura) | 1 | — | 3787 |
| ficha: etapa com mais de 7 dias (cobertura) | 0 | — | — |
| ficha.data_hora_final_bandagem | 0 | 0 | — |
| ficha: final antes do início (bandagem) | 1 | — | 697 |
| ficha: etapa com mais de 7 dias (bandagem) | 0 | — | — |
| ficha.data_hora_final_vulcanizacao | 0 | 0 | — |
| ficha: final antes do início (vulcanização) | 0 | — | — |
| ficha: etapa com mais de 7 dias (vulcanização) | 0 | — | — |
| ficha.data_hora_final_debandagem | 0 | 0 | — |
| ficha: final antes do início (debandagem) | 0 | — | — |
| ficha: etapa com mais de 7 dias (debandagem) | 0 | — | — |
| ficha.data_hora_final_extracao | 0 | 0 | — |
| ficha: final antes do início (extração/teste) | 110 | — | 654, 686, 691, 743, 744 … (+105) |
| ficha: etapa com mais de 7 dias (extração/teste) | 1 | — | 1165 |
| inspeção.DataHoraInspecao | 0 | 0 | — |
| TiposErros.Criado | 0 | 0 | — |
| MB51.Posting Date (antes de 2000 em vez de 11/2025: a MB51 começa em 11/2024) | 0 | 0 | — |
| PackingList.Timestamp | 0 | 0 | — |

Datas que não viram data (não preenchem o formato `MM/DD/AAAA h:mm AM/PM`): ficha (Created) = 0; inspeção = 0; TiposErros.Criado = 0.
`data_ref` fora do dia produtivo de 05:20 só existe na Hora-Hora (`field_0` x `Title` x hora de criação): **NÃO EXECUTADO** (sem export).

## 4. Turno x horário (NORMA de 27/10, MEL-250: T1 320–836, T2 837–1339, T3 1340–319)

`Turno` do registro x turno que a NORMA dá ao horário do FIM da etapa (`data_hora_final_*`). Coluna "T2 em 22:20–22:40" = registro T2 com horário entre 22:20 e 22:40 e data de 05 a 27/10.
| Origem | Com turno e hora | Turno ≠ NORMA no fim | ≠ no fim e no início | Registrado T2 mas NORMA diz T3 | T2 em 22:20–22:40 (05–27/10) | Amostra de IDs |
|---|---|---|---|---|---|---|
| ficha mandril | 2691 | 710 | 701 | 20 | 0 | — |
| ficha tubo | 2678 | 983 | 975 | 3 | 1 | 3908 |
| ficha trançagem | 2651 | 918 | 473 | 29 | 0 | — |
| ficha cobertura | 2653 | 1177 | 1168 | 10 | 0 | — |
| ficha bandagem | 2648 | 989 | 979 | 9 | 1 | 3843 |
| ficha vulcanização | 2415 | 258 | 244 | 8 | 4 | 3865, 3874, 3875, 3889 |
| ficha debandagem | 2103 | 546 | 520 | 14 | 0 | — |
| ficha extração/teste | 777 | 11 | 0 | 10 | 1 | 3860 |
| inspeção (TurnoTeste x DataHoraInspecao) | 16521 | 488 | — | 96 | 0 | — |
| TiposErros (Turno Erro x Criado) | 4463 | 37 | — | 37 | 0 | — |

**Aceite:** esperado 46 fins de etapa da ficha com T2 entre 22:20 e 22:40 de 05 a 27/10 (contagem de 29/10 na lista viva). Neste export (ficha até 06/10) deu **7**. **ACEITE NÃO ATINGIDO.** Provável causa: o arquivo termina em 06/10 (só 05 e 06/10 dentro da janela), mas isso não está provado. Para reproduzir 46 é preciso um export novo da `ficha_producao`. Os 146 da Hora-Hora não dá para conferir: o export da Hora-Hora não está na pasta (seção 10).
Formato do campo turno na ficha: {'número N': 15889, "texto 'Turno N'": 3293}. Mistura de `3` e `Turno 3` para o mesmo valor; a limpeza da Fase 3 normaliza para `N`.
| Faixa de horário (fim da etapa, ficha) | Período | Registros | Gravados T1 | Gravados T2 | Gravados T3 |
|---|---|---|---|---|---|
| 13:47–13:56 | 05 a 27/10 | 0 | 0 | 0 | 0 |
| 13:47–13:56 | antes de 05/10 | 45 | 10 | 22 | 13 |
| 13:47–13:56 | depois de 27/10 | 0 | 0 | 0 | 0 |
| 22:20–22:40 | 05 a 27/10 | 7 | 0 | 7 | 0 |
| 22:20–22:40 | antes de 05/10 | 56 | 2 | 44 | 10 |
| 22:20–22:40 | depois de 27/10 | 0 | 0 | 0 | 0 |

Leitura: em 13:47–13:56 a NORMA dá T1; em 22:20–22:40 dá T3. Antes de 05/10 a regra do app já era outra para 13:47 (T2 a partir de 13:47) mas, segundo o glossário, a virada para T3 era 22:20; então os registros T2 em 22:20–22:40 antes de 05/10 também divergem da NORMA e NÃO se pode dizer que "só 05 a 27/10 precisa de correção": se os registros anteriores a 05/10 entram na correção é decisão do William. A janela 05 a 27/10 está fixa no script (o glossário fala em "~29/10" para a volta; data real a confirmar). O fim da etapa vale como horário de turno só onde o app gravava o turno no fim (app atual); no histórico, parte das divergências (mandril, tubo, cobertura: 26 a 44% não batem nem com início nem com fim) tem outra causa que este diagnóstico não explica, e não há tabela de divergência total por período. Os campos Qtd_Turno1/2/3 da ficha não foram conferidos.

## 5. Lacunas (dias sem registro por máquina)

| Fonte | Máquina | Período da máquina | Dias úteis esperados | Dias sem registro | Primeiros dias sem registro |
|---|---|---|---|---|---|
| ficha (fim trançagem) | SPIRAL | 2025-12-06 a 2026-10-05 | 188 | 56 | 2026-01-07, 2026-01-09, 2026-01-10, 2026-01-14 … |
| ficha (fim trançagem) | TH01 | 2025-12-04 a 2026-10-06 | 189 | 45 | 2025-12-05, 2026-01-14, 2026-01-22, 2026-01-29 … |
| ficha (fim trançagem) | TH02 | 2025-12-05 a 2026-10-03 | 188 | 62 | 2026-01-13, 2026-01-21, 2026-01-26, 2026-01-27 … |
| ficha (fim trançagem) | TH03 | 2025-12-05 a 2026-10-05 | 189 | 46 | 2026-01-22, 2026-01-26, 2026-01-31, 2026-02-10 … |
| ficha (fim trançagem) | TH04 | 2025-12-05 a 2026-08-10 | 145 | 107 | 2026-01-07, 2026-01-09, 2026-01-10, 2026-01-12 … |
| ficha (fim trançagem) | TH05 | 2026-01-10 a 2026-10-05 | 186 | 96 | 2026-01-12, 2026-01-13, 2026-01-14, 2026-01-15 … |
| ficha (fim trançagem) | TH06 | 2026-01-09 a 2026-10-05 | 187 | 34 | 2026-01-13, 2026-01-19, 2026-01-20, 2026-01-31 … |
| ficha (fim trançagem) | TH07 | 2025-12-04 a 2026-10-06 | 189 | 10 | 2026-01-22, 2026-04-02, 2026-04-07, 2026-04-08 … |
| ficha (fim trançagem) | TM01 | 2025-12-08 a 2026-10-06 | 188 | 32 | 2026-01-10, 2026-01-12, 2026-01-13, 2026-01-30 … |
| ficha (fim trançagem) | TM04 | 2025-12-09 a 2026-10-02 | 186 | 77 | 2026-01-07, 2026-01-10, 2026-01-16, 2026-01-26 … |
| ficha (fim trançagem) | TO04 | 2026-01-09 a 2026-10-06 | 187 | 51 | 2026-01-12, 2026-01-14, 2026-01-15, 2026-01-16 … |
| ficha (fim mandril) | TERMOFUSAO | 2026-08-14 a 2026-10-06 | 40 | 0 |  |
| ficha (fim mandril) | VIBRACIONAL | 2026-08-17 a 2026-10-05 | 40 | 0 |  |
| inspeção (cabine) | CABINE_L1 | 2026-09-25 a 2026-10-02 | 7 | 0 |  |
| inspeção (cabine) | CABINE_L2 | 2026-09-26 a 2026-10-02 | 6 | 0 |  |

Dia útil = dia em que a fábrica toda lançou pelo menos 40% da mediana diária; lacuna = dia útil dentro do período da máquina em que ela não lançou nada. Máquina que parou por manutenção também aparece aqui; é lacuna a registrar, nunca dado a inventar. Mandril por máquina usa só o fim de etapa. Lacunas da Hora-Hora (janelas faltando por célula e turno): **NÃO EXECUTADO**.

## 6. OP do GMS que não existe na MB51

MB51 do arquivo vai de 2024-11-04 a 2026-10-21; 29260 ordens distintas. OP do GMS sem ordem na MB51 só é falha de dado depois que o SAP lança, então a conta exclui fichas Canceladas e fichas criadas depois de 2026-10-06.
| Origem | OPs avaliadas | OPs sem ordem na MB51 | % | Amostra |
|---|---|---|---|---|
| ficha (OP) | 2680 | 32 | 1.2% | 722, 723, 784, 794, 812 … (+27) |
| inspeção (OP_ID) | 2226 | 14 | 0.6% | 0, 889911, 2435733, 12055040, 20185934 … (+9) |
| TiposErros (OP_ID) | 1612 | 10 | 0.6% | 0, 889911, 2435733, 20185934, 20650388 … (+5) |

| Mês de criação da ficha | OPs | Sem MB51 | % |
|---|---|---|---|
| 2025-11 | 1 | 0 | 0% |
| 2025-12 | 21 | 2 | 10% |
| 2026-01 | 293 | 6 | 2% |
| 2026-02 | 295 | 2 | 1% |
| 2026-03 | 350 | 0 | 0% |
| 2026-04 | 287 | 4 | 1% |
| 2026-05 | 329 | 5 | 2% |
| 2026-06 | 323 | 3 | 1% |
| 2026-07 | 77 | 0 | 0% |
| 2026-08 | 316 | 2 | 1% |
| 2026-09 | 330 | 5 | 2% |
| 2026-10 | 58 | 3 | 5% |

Se o percentual por mês for alto só nos meses antigos, a MB51 exportada não cobre o período (a MB51 vai de 11/2024, mas só traz ordens com lançamento). A conferência fina (casar nome da mangueira por OP) é a seção 9.

## 7. Unidades e valores fora de faixa

| Campo | Válidos | Não numéricos | Negativos | Zeros | Muito acima (cerca de 6×IQR) | Faixa | Amostra de IDs |
|---|---|---|---|---|---|---|---|
| ficha.quantidade_mandril | 2693 | 0 | 0 | 4 | 1 | 0 … 2700 | 1942 |
| ficha.quantidade_tubo | 2683 | 0 | 0 | 7 | 4 | 0 … 7000 | 944, 1173, 1211, 2204 |
| ficha.quantidade_trancagem | 2663 | 0 | 0 | 140 | 2 | 0 … 115052 | 3258, 3647 |
| ficha.quantidade_cobertura | 2568 | 0 | 0 | 60 | 1 | 0 … 2.09979e+06 | 3686 |
| ficha.quantidade_bandagem | 2468 | 0 | 0 | 35 | 2 | 0 … 4.00018e+07 | 2838, 3306 |
| ficha.quantidade_vulcanizacao | 2490 | 0 | 0 | 46 | 1 | 0 … 4.00018e+07 | 3306 |
| ficha.quantidade_debandagem | 2531 | 0 | 0 | 40 | 0 | 0 … 1220 | — |
| ficha.quantidade_extracao | 2436 | 0 | 0 | 10 | 0 | 0 … 1180 | — |
| inspeção.Quantidade | 16542 | 0 | 0 | 4 | 15 | 0 … 7750 | 60, 63, 418, 809, 810 … (+10) |
| inspeção.Diametro_Interno | 16532 | 0 | 0 | 8 | 636 | 0 … 1030 | 0, 1, 2, 4, 22 … (+631) |
| inspeção.Diametro_Externo | 16532 | 0 | 0 | 9 | 682 | 0 … 1511 | 0, 1, 2, 22, 31 … (+677) |
| inspeção.Concentricidade | 16531 | 0 | 0 | 20 | 10 | 0 … 1501 | 0, 3729, 5278, 5825, 9553 … (+5) |
| TiposErros.Quantidade | 5433 | 0 | 0 | 2 | 226 | 0 … 750 | 0, 75, 126, 197, 211 … (+221) |
| PackingList.QTd (m) | 9965 | 0 | 0 | 1 | 2 | 0 … 5205 | 1, 254 |
| PackingList.ID Total Length (m) | 9965 | 0 | 0 | 112 | 8 | 0 … 5416 | 1 |

"Muito acima" é heurística estatística (Q3 + 6×IQR); não é limite de negócio. Os limites reais (comprimento máximo de lance, diâmetro por mangueira) saem do DM_* e são decisão da Fase 2.
| MB51: verificação | Linhas |
|---|---|
| 101 com quantidade ≤ 0 | 0 |
| 102 com quantidade > 0 | 0 |
| Unidade diferente de M, PC, KG | 0 |
| Unidade vazia | 0 |

MB51 por unidade e movimento: KG/101 = 1682; KG/102 = 39; M/101 = 61706; M/102 = 1815; PC/101 = 47547; PC/102 = 330. Metros de mangueira = só unidade `M`.
Extração maior que a debandagem: 642 fichas (amostra de IDs: 1009, 1016, 1021, 1023, 1026 … (+637)). Não é erro por si (COMO_USAR_OS_DADOS §4); fica só como informação.

## 8. Nomes de máquina e mangueira escritos de jeitos diferentes

| Campo | Valores distintos | Grupos com mais de uma grafia | Exemplos (grafia(contagem)) |
|---|---|---|---|
| Mangueira (ficha) | 70 | 1 | GH781-6(149)/gh781-6(1) |
| Mangueira (inspeção) | 62 | 1 | GH781-6(1063)/gh781-6(6) |
| Trançadeira (ficha) | 23 | 5 | TH07(647)/TH-07(1); TO04(250)/TO-04(4); TM01(207)/TM-01(1); TH02(162)/TH-02(1); TE01(3)/TE-01(1) |
| Trançadeira (inspeção) | 18 | 3 | TH07(2556)/TH-07(6); TO04(1026)/TO-04(29); TH02(620)/TH-02(6) |
| Trançadeira (TiposErros) | 18 | 3 | TH07(936)/TH-07(1); TO04(313)/TO-04(5); TH02(201)/TH-02(3) |
| maquina_mandril (ficha) | 2 | 0 | — |
| cabine_teste (inspeção) | 2 | 0 | — |

Grupo = mesmo texto depois de maiúscula, espaços, `-` e `_` removidos. Grafias que diferem de outro jeito (`GH781-6-2` x `GH781-6`, `TO04` x `TO-04`, `-N` de sufixo) ficam para a tabela de equivalência da Fase 2.
Mangueiras da ficha (distintas: 70) cujo nome não aparece em nenhuma `Material Description` da MB51 (busca por contém, normalizada): **42**. Lista: 2556-10, 2556-12, 2556-16, 2556-3, 2556-4, 2556-5, 2556-6, 2583-12, EC115-04L, EC115-06L, EC115-08L, EC115-10L, EC115-12L, EC115-16L, EC118-04L …. É o caso conhecido de nome do GMS diferente do SAP; liga-se pela OP (seção 9).

## 9. Divergência GMS x MB51 por OP (SAP é a verdade)

Período em comum entre GMS e SAP: GMS (inspeção/erros) vai até 2026-10-02; MB51 até 2026-10-21. Só entram OPs que existem nos dois lados e cujo último lançamento SAP é até 2026-10-02. Boa = 101 − 102 sem os usuários de refugo; refugo = lançamentos dos usuários de refugo. Metros, tolerância 1 m. Convenção: variação = SAP − GMS (negativa = faltou lançar no SAP; positiva = sobrou no SAP).
| Medida | OPs nos dois lados | Dentro de 1 m | OPs que faltou | Faltou (m) | OPs que sobrou | Sobrou (m) | Materiais com falta / com sobra | OPs de maior variação (IDs) |
|---|---|---|---|---|---|---|---|---|
| Produção boa | 2202 | 1871 | 147 | -37862 | 184 | 26832 | 36 / 41 | 27312495, 27312498, 27625635, 28387301, 29050557 |
| Refugo | 1421 | 1255 | 46 | -558 | 120 | 724 | 26 / 36 | 28403902, 28975588, 29118867, 29367063, 30063850 |

Faltou e sobrou NÃO se compensam entre materiais (regra do COMO_USAR_OS_DADOS §3): os totais acima ficam separados e a coluna de materiais conta onde cada um ocorre. Compensação só dentro do mesmo material, e troca de OP entre OPs vizinhas do mesmo material é costume da fábrica (Fase 2 decide). OP que existe só num lado está na seção 6.
Mangueira da ficha x material da mesma OP no SAP (2648 fichas com OP nos dois lados): igual = **2167**; alias já conhecido em `aliases_mangueira.csv` = **18**; **diverge = 463** em 24 pares distintos (IDs de ficha: 654, 702, 711, 740, 819 … (+458)). Pares que mais se repetem (GMS → SAP, fichas): GH493-12→HOSE R12 (162); GH493-16→HOSE R12 (153); GH493-8→HOSE R12 (40); HC139-7_S-GX→HC139-7 (33); HC101-6→HC101-5 (24); EC215-16L→HOSE-WIN, 2SC/EN857, -16, NBR/NBR, BK (16); GH493-6→HOSE R12 (11); GH493-10→HOSE R12 (5). Parte desses é alias novo (grafia do mesmo material, ex.: sufixo `-2`); parte é divergência real de OP. A Fase 2 separa as duas.

## 10. Hora-Hora

**NÃO EXECUTADO.** A lista Hora-Hora não tem export na pasta `Sharepoint Data GMS` (os backups de 16/10 foram só para outra pasta do PC e não estão no repositório). As verificações abaixo foram escritas e ficam prontas para rodar com `--hh <csv>`:
- duplicados por data+turno+célula+hora; campos vazios; `Title` x `field_0`/`field_2`;
- turno x janela: `TurnoH` = 2º e `field_3` = `22:00 - 22:20` (41 min) na `field_0` de 05 a 27/10 → alvo 146 linhas (referência do diário de 29/10, não lida aqui: IDs 28835 a 31767, todas Finalizado). Atenção: a janela de 41 min mistura 20 min de T2 (22:00–22:19) e 21 de T3; trocar o `TurnoH` da linha inteira move produção de T2 para T3 e o Tempo Parado foi calculado sobre 41 min (MEL-255) — a Fase 2 precisa de regra de divisão ou marca 'a conferir';
- lacunas por célula e janela do turno; Tempo Parado > Minutos; Real/Meta fora de faixa.
Para obter o export: o William exporta a lista no SharePoint (CSV) ou autoriza uma leitura por navegador logado que grave direto em arquivo local (o conteúdo não deve passar por agentes: só contagens e IDs).

## 11. Conferência do `revisor` (Opus) e decisões que faltam

*(Acrescentada à mão depois de rodar o script; se o script rodar de novo, esta seção precisa ser refeita.)*

Veredito: **método serve de base, aceite da Fase 1 NÃO atingido** (146 Hora-Hora e 46 ficha não reproduzidos: faltam export novo da `ficha_producao` e export da Hora-Hora). Sem erro em parada/setup (nada foi somado como parada real nem calculou setup). Pontos aceitos e refletidos acima: janela 05–27/10 fixa; registros anteriores a 05/10 também divergem; janela de 41 min da Hora-Hora não pode virar T3 inteira; falta/sobra do GMS x SAP aparecem por OP (infladas por troca de OP; compensar dentro do mesmo material antes de corrigir).
Fraquezas conhecidas: sem divergência de turno por período completa, sem `Qtd_Turno1/2/3`, sem `data_ref` da Hora-Hora, turno de inspeção/erros não separado por faixa.

**Regras propostas para a Fase 2 (aguardam aprovação por escrito do William):**
1. Ficha: T2→T3 só se o fim da etapa caiu em 22:20–22:40 dentro da janela das 22:41 e a gravação era feita no fim; ajustar junto `Qtd_TurnoN`; guardar o valor antigo.
2. Hora-Hora: não trocar `TurnoH` da janela de 41 min inteira; dividir (T2 22:00–22:19 / T3 22:20–22:40) ou marcar "a conferir"; não recalcular Tempo Parado sem o `revisor` (MEL-255).
3. Hora e data: só corrige com evidência no registro; senão "a conferir".
4. Duplicado: definir o desempate (maior ID x Finalizado); o outro vai à lixeira, nunca exclusão definitiva.
5. Lacuna: registrar, não inventar.
6. GMS x SAP: compensar dentro do mesmo material (troca de OP), depois valer o SAP por OP, guardando o valor antigo; lote mostrado antes.
7. Nomes e unidades: tabela de equivalência aprovada (partir de `aliases_mangueira.csv`; `TH-07`→`TH07`, `gh781-6`→`GH781-6`, `Turno 3`→`3`).
8. Nunca apagar em definitivo; todo valor trocado guarda o antigo.

**Decisões do William:** (a) data real da volta de 22:41 para 22:20 (27/10 ou ~29/10); (b) registros antes de 05/10 entram na correção?; (c) como dividir a janela de 41 min; (d) enviar export novo da `ficha_producao` e da Hora-Hora (CSV salvo local, sem passar por agentes); (e) desempate de duplicados.
