<!-- AUTO:INICIO (regenerado a cada execucao, nao edite aqui) -->
# Mapa dos dados

Gerado em 2026-11-01 00:17 a partir de `dados`. Nomes de tabela e coluna estao em minusculo e sem acento.

## Tabelas e colunas

### bd_packing_list__data_base (9965 linhas)

| coluna | tipo | vazio % | distintos | exemplos | min | max |
|---|---|---|---|---|---|---|
| id | BIGINT | 0 | 1496 | 0, 1, 2 | 0 | 1496 |
| pn | VARCHAR | 0 | 93 | 0, GH781-6, GH781-10 | - | - |
| slice | BIGINT | 0 | 27 | 0, 1, 2 | 0 | 26 |
| qtd_m | DOUBLE | 0 | 1630 | 0.0, 50.0, 5205.0 | 0.0 | 5205.0 |
| id_total_length_m | DOUBLE | 0 | 1324 | 0.0, 5416.0, 725.8 | 0.0 | 5416.0 |
| timestamp | VARCHAR | 0 | 1532 | 0, 2026-05-04 14:02:24, 2026-05-04 16:55:30 | - | - |
| created_by | VARCHAR | 44 | 38 | 0, 38534548443191, 38532221990079 | - | - |
| cancelled | BIGINT | 96 | 2 | 0, 1 | 0 | 1 |
| cancelled_date | VARCHAR | 96 | 68 | 0, 2026-05-04 14:03:29, 2026-05-05 15:36:06 | - | - |
| cancelled_by | VARCHAR | 96 | 19 | 0, 38534548443191, 38534824871995 | - | - |

### ficha_producao (2694 linhas)

| coluna | tipo | vazio % | distintos | exemplos | min | max |
|---|---|---|---|---|---|---|
| id | BIGINT | 0 | 2694 | 654, 686, 691 | 654 | 3915 |
| processo | VARCHAR | 0 | 9 | Finalizado, Trançadeira, Cobertura | - | - |
| carretel_entrada | BIGINT | 98 | 37 | 0, 5, 40 | 0 | 86 |
| carretel_saida | BIGINT | 96 | 57 | 40, 2, 63 | 0 | 101 |
| bitola | BIGINT | 0 | 10 | 4, 6, 8 | 3 | 17 |
| mangueira | VARCHAR | 0 | 70 | FC598-08, GH781-6, EC215-08L | - | - |
| op | BIGINT | 0 | 2681 | 27002870, 27025403, 27055217 | 10010000 | 75632568 |
| status_processo | VARCHAR | 0 | 4 | Finalizado, Aguardando, Em processo | - | - |
| trancadeira | VARCHAR | 0 | 23 | TH07, TH06, TH04 | - | - |
| cod_mandril | VARCHAR | 0 | 11 | FM00248, FM00365, FM00500 | - | - |
| maquina_mandril | VARCHAR | 78 | 2 | TERMOFUSAO, VIBRACIONAL | - | - |
| turno_mandril | VARCHAR | 0 | 4 | 1, 2, Turno 3 | - | - |
| data_hora_inicio_mandril | VARCHAR | 0 | 2539 | 11/29/2025 3:07 AM, 12/2/2025 1:19 AM, 12/2/2025 8:48 AM | - | - |
| data_hora_final_mandril | VARCHAR | 0 | 2521 | 11/29/2025 7:08 AM, 12/2/2025 5:20 AM, 12/2/2025 12:49 PM | - | - |
| lote_mandril | VARCHAR | 0 | 125 | 2509B00624, 2508B00006, 2509B00006 | - | - |
| desmoldante_mandril | VARCHAR | 0 | 2 | Sim, Não | - | - |
| diametro_mandril | DOUBLE | 0 | 11 | 0.248, 0.365, 0.5 | 0.195 | 0.98 |
| operador_mandril | VARCHAR | 0 | 76 | 875670, 388557, 8750670 | - | - |
| quantidade_mandril | VARCHAR | 0 | 153 | 400, 680, 520 | - | - |
| turno_tubo | VARCHAR | 0 | 4 | 1, 2, 3 | - | - |
| data_hora_inicio_tubo | VARCHAR | 0 | 2673 | 11/29/2025 4:24 AM, 12/2/2025 9:01 AM, 12/2/2025 11:38 AM | - | - |
| data_hora_final_tubo | VARCHAR | 1 | 2652 | 8/14/2026 8:26 AM, 12/2/2025 1:02 PM, 12/2/2025 3:46 PM | - | - |
| diametro_tubo | VARCHAR | 0 | 88 | 0.306, 0.5, 0.62 | - | - |
| defeito_tubo | VARCHAR | 1 | 12 | 0, 1, 2 | - | - |
| quantidade_tubo | VARCHAR | 0 | 96 | 400, 680, 520 | - | - |
| operador_tubo | VARCHAR | 1 | 33 | DIEGO LUIZ DA SILVA..., 9891545, 8761254 | - | - |
| turno_trancagem | VARCHAR | 1 | 4 | 1, 2, 3 | - | - |
| data_hora_final_trancadeira | VARCHAR | 1 | 2595 | 12/5/2025 8:42 PM, 12/4/2025 9:35 PM, 12/5/2025 11:41 PM | - | - |
| data_hora_inicio_trancadeira | VARCHAR | 1 | 2623 | 11/29/2025 9:09 AM, 12/3/2025 10:33 PM, 12/3/2025 6:23 AM | - | - |
| diametro_trancagem | VARCHAR | 2 | 421 | 412, 743, 1,028 | - | - |
| quantidade_trancagem | VARCHAR | 1 | 128 | 800, 520, 400 | - | - |
| defeito_trancagem | VARCHAR | 1 | 21 | 5, 3, 4 | - | - |
| operador_trancagem | VARCHAR | 2 | 117 | 379967, ALMIR, ANDERSON | - | - |
| turno_cobertura | VARCHAR | 1 | 4 | 2, 3, 1 | - | - |
| data_hora_inicio_cobertura | VARCHAR | 1 | 2636 | 12/5/2025 9:01 AM, 2/5/2026 1:02 PM, 12/4/2025 5:47 AM | - | - |
| data_hora_final_cobertura | VARCHAR | 2 | 2630 | 12/5/2025 9:03 AM, 12/4/2025 9:48 AM, 12/5/2025 9:45 AM | - | - |
| diametro_cobertura | VARCHAR | 5 | 347 | 0.48, 0.817, 1.08 | - | - |
| defeito_cobertura | VARCHAR | 5 | 49 | 1, 0, 2 | - | - |
| quantidade_cobertura | VARCHAR | 5 | 111 | 750, 680, 520 | - | - |
| operador_cobertura | VARCHAR | 7 | 50 | E8761071, E9895339, E0644532 | - | - |
| turno_bandagem | VARCHAR | 2 | 4 | 1, 2, 3 | - | - |
| data_hora_inicio_bandagem | VARCHAR | 2 | 2497 | 2/5/2026 1:15 PM, 12/4/2025 6:12 AM, 12/5/2025 3:18 PM | - | - |
| data_hora_final_bandagem | VARCHAR | 2 | 2507 | 2/5/2026 1:15 PM, 12/4/2025 10:12 AM, 12/5/2025 3:18 PM | - | - |
| operador_bandagem | VARCHAR | 10 | 43 | 8754252, 727, E8750754 | - | - |
| cod_fita_bandagem | VARCHAR | 72 | 68 | 000000000012100749, T03482, T03212 | - | - |
| codigo_filme_uhmwpe | VARCHAR | 86 | 26 | T0014GB, ., , | - | - |
| quantidade_bandagem | VARCHAR | 8 | 192 | 650, 530, 420 | - | - |
| data_hora_final_vulcanizacao | VARCHAR | 2 | 1644 | 5/10/2026 8:30 PM, 12/4/2025 9:24 PM, 12/4/2025 11:13 AM | - | - |
| data_hora_inicio_vulcanizacao | VARCHAR | 3 | 1637 | 5/8/2026 11:37 AM, 12/4/2025 5:23 PM, 12/4/2025 7:12 AM | - | - |
| turno_vulcanizacao | VARCHAR | 10 | 6 | Turno 2, 2, 1 | - | - |
| inicioresfriamento_vulcanizacao | VARCHAR | 73 | 328 | 6/23/2026 11:17 AM, 7/3/2026 12:07 PM, 7/3/2026 12:10 PM | - | - |
| quantidade_vulcanizacao | VARCHAR | 8 | 204 | 500, 650, 530 | - | - |
| operador_vulcanizacao | VARCHAR | 10 | 31 | SIRLEY CLAUDINEI DA..., 8754252, 727 | - | - |
| turno_debandagem | BIGINT | 2 | 3 | 2, 1, 3 | 1 | 3 |
| data_hora_inicio_debandagem | VARCHAR | 2 | 2588 | 8/28/2026 2:38 PM, 12/5/2025 2:35 AM, 12/4/2025 9:35 PM | - | - |
| data_hora_final_debandagem | VARCHAR | 22 | 2054 | 8/28/2026 2:39 PM, 6/23/2026 7:58 PM, 2/26/2026 12:05 PM | - | - |
| quantidade_debandagem | VARCHAR | 6 | 230 | 500, 650, 530 | - | - |
| operador_debandagem | VARCHAR | 12 | 47 | WILLIAM NATHAN RIBE..., E8750754, 080 | - | - |
| turno_extr_teste | BIGINT | 71 | 3 | 1, 2, 3 | 1 | 3 |
| cabine_teste | VARCHAR | 95 | 2 | CABINE_L1, CABINE_L2 | - | - |
| data_hora_inicio_extracao | VARCHAR | 26 | 1978 | 9/25/2026 1:44 PM, 12/9/2025 5:47 PM, 12/9/2025 6:00 PM | - | - |
| data_hora_final_extracao | VARCHAR | 12 | 1864 | 8/28/2026 2:40 PM, 12/9/2025 1:00 AM, 1/7/2026 1:00 AM | - | - |
| quantidade_extracao | VARCHAR | 10 | 1909 | 10.00, 245.00, 156.00 | - | - |
| operador_extracao | VARCHAR | 11 | 138 | WILLIAM NATHAN RIBE..., 0, DIEGO LUIZ DA SILVA... | - | - |
| cod_cobertura | VARCHAR | 4 | 51 | 500-01, 500.03, 98746 | - | - |
| cod_compostotubo | VARCHAR | 0 | 38 | 640-99, 640-33, 2023 | - | - |
| created | VARCHAR | 0 | 2657 | 11/29/2025 7:07 AM, 12/2/2025 5:20 AM, 12/2/2025 12:48 PM | - | - |
| data_de_validade_do_composto_cobertura | VARCHAR | 7 | 216 | 1/16/2026, 12/24/2025, 12/12/2025 | - | - |
| data_de_validade_do_composto_tubo | VARCHAR | 0 | 169 | 12/24/2025, 12/1/2025, 12/11/2025 | - | - |
| lote_composto_tubo | VARCHAR | 0 | 556 | 2044934008, 1232121, 2044934005 | - | - |
| lote_cobertura | VARCHAR | 5 | 426 | 20461810, 2029146, 2032793 | - | - |
| cod_trancagem | VARCHAR | 1 | 70 | W00001, W00002, w00002 | - | - |
| lote_trancagem | VARCHAR | 1 | 257 | 16191518, 16022107, 16031366 | - | - |
| n_picks | VARCHAR | 1 | 98 | 42, 40, 29 | - | - |
| inicioaguardando_trancadeira | VARCHAR | 1 | 2651 | 8/14/2026 8:26 AM, 12/2/2025 1:02 PM, 12/2/2025 3:46 PM | - | - |
| inicioaguardando_tubo | VARCHAR | 0 | 2632 | 11/29/2025 7:08 AM, 12/2/2025 5:20 AM, 12/2/2025 12:49 PM | - | - |
| inicioaguardando_bandagem | VARCHAR | 2 | 2626 | 12/5/2025 9:03 AM, 2/5/2026 1:02 PM, 12/5/2025 9:45 AM | - | - |
| inicioaguardando_vulcanizacao | VARCHAR | 2 | 2508 | 5/8/2026 11:36 AM, 2/5/2026 1:15 PM, 12/4/2025 10:12 AM | - | - |
| inicioaguardando_debandagem | VARCHAR | 2 | 1645 | 5/10/2026 8:30 PM, 12/4/2025 9:24 PM, 12/4/2025 11:13 AM | - | - |
| inicioaguardando_extr_teste | VARCHAR | 2 | 2572 | 8/28/2026 2:39 PM, 12/5/2025 2:35 AM, 12/4/2025 9:35 PM | - | - |
| inicioemprocesso_tubo | VARCHAR | 1 | 2652 | 12/8/2025 9:29 AM, 12/8/2025 10:27 AM, 1/5/2026 1:29 PM | - | - |
| inicioemprocesso_trancagem | VARCHAR | 1 | 2624 | 11/29/2025 9:09 AM, 12/2/2025 5:06 PM, 12/3/2025 10:33 PM | - | - |
| inicioemprocesso_cobertura | VARCHAR | 2 | 2631 | 12/5/2025 9:01 AM, 2/5/2026 1:02 PM, 12/5/2025 9:43 AM | - | - |
| inicioemprocesso_bandagem | VARCHAR | 2 | 2493 | 8/17/2026 8:40 AM, 2/5/2026 1:15 PM, 12/5/2025 3:18 PM | - | - |
| inicioemprocesso_vulcanizacao | VARCHAR | 3 | 1637 | 5/8/2026 11:37 AM, 12/4/2025 9:23 PM, 12/4/2025 11:12 AM | - | - |
| inicioemprocesso_debandagem | VARCHAR | 2 | 2588 | 8/28/2026 2:38 PM, 12/5/2025 2:35 AM, 12/4/2025 9:35 PM | - | - |
| inicioemprocesso_extr_teste | VARCHAR | 25 | 2004 | 9/25/2026 1:44 PM, 6/25/2026 3:08 PM, 2/25/2026 1:16 PM | - | - |
| inicioaguardandocobertura | VARCHAR | 15 | 2272 | 12/1/2025 6:59 AM, 12/3/2025 5:07 AM, 12/4/2025 4:39 AM | - | - |
| qtd_turno1 | VARCHAR | 0 | 108 | 580, 0, 232 | - | - |
| qtd_turno2 | VARCHAR | 0 | 113 | 0, 412, 568 | - | - |
| qtd_turno3 | VARCHAR | 0 | 62 | 0, 268, 520 | - | - |
| modified | VARCHAR | 0 | 1425 | 9/25/2026 1:45 PM, 9/3/2026 9:00 AM, 6/25/2026 3:08 PM | - | - |
| qtd_turno1_cobertura | VARCHAR | 62 | 85 | 0, 800, 545 | - | - |
| qtd_turno2_cobertura | VARCHAR | 61 | 60 | 0, 800, 700 | - | - |
| qtd_turno3_cobertura | BIGINT | 98 | 9 | 800, 0, 420 | 0 | 800 |
| qtd_turno1_bandagem | VARCHAR | 63 | 147 | 999, 650, 560 | - | - |
| qtd_turno2_bandagem | VARCHAR | 62 | 136 | 400, 700, 200 | - | - |
| qtd_turno3_bandagem | VARCHAR | 97 | 38 | 500, 520, 330 | - | - |
| qtd_turno1_vulcanizacao | VARCHAR | 59 | 167 | 650, 400, 727 | - | - |
| qtd_turno2_vulcanizacao | VARCHAR | 66 | 148 | 500, 400, 1,400 | - | - |
| qtd_turno3_vulcanizacao | BIGINT | 96 | 37 | 500, 800, 250 | 0 | 960 |
| qtd_turno1_debandagem | VARCHAR | 72 | 126 | 0, 800, 650 | - | - |
| qtd_turno2_debandagem | VARCHAR | 57 | 136 | 500, 412, 0 | - | - |
| qtd_turno3_debandagem | BIGINT | 93 | 44 | 0, 800, -500 | -750 | 900 |
| datafinalizacao | VARCHAR | 37 | 151 | 8/28/2026, 6/25/2026, 3/3/2026 | - | - |
| observacao_mandril | VARCHAR | 89 | 175 | Descartado - sessao..., Descartado - sessao..., CARRETEL 101 | - | - |
| observacao_tubo | VARCHAR | 99 | 23 | AMOSTRA, TUBO COM DUAS PONTAS, JA OK | - | - |
| observacao_trancagem | VARCHAR | 98 | 45 | -, Perdido no Sabado, 0 | - | - |
| observacao_cobertura | VARCHAR | 93 | 99 | SEM SIKORA E NINA, SEM SIKORA NINA, COMPOSTO AIRANDO | - | - |
| observacao_debandagem | VARCHAR | 100 | 2 | PROBLEMA IMPRESSORA..., VELOCIDADE REDUZIDA... | - | - |
| packlist_cabine | VARCHAR | 100 | 2 | <div style='font-fa..., Extr./Teste | - | - |

### mascara_de_producao__analise_media (1 linhas)

| coluna | tipo | vazio % | distintos | exemplos | min | max |
|---|---|---|---|---|---|---|
| col_1 | VARCHAR | 0 | 1 | MEDIA | - | - |

### mascara_de_producao__cadastro_mangueiras (94 linhas)

| coluna | tipo | vazio % | distintos | exemplos | min | max |
|---|---|---|---|---|---|---|
| mangueira_hose | VARCHAR | 0 | 94 | HC3000-6, HC139-7_S-GX, HC139-7(S/G) | - | - |
| c_standart | VARCHAR | 0 | 8 | SD20-04/06, TEXTILE-07/08/10/12..., TEXTILE-03/04/05/06 | - | - |
| decks | VARCHAR | 0 | 7 | Wire - SD (-04 to -..., Textil, Wire - DD (-08 to -... | - | - |
| wires | VARCHAR | 0 | 5 | Wire - 20C, Textil, Wire 24C | - | - |
| bitola | BIGINT | 0 | 9 | 6, 7, 8 | 3 | 16 |
| tipo | VARCHAR | 0 | 4 | 1A, 1T, 2A | - | - |
| mat_tranca | VARCHAR | 0 | 2 | Aço, Têxtil | - | - |
| h_m | DOUBLE | 0 | 38 | 0.0, 0.027408, 0.031637 | 0.0 | 0.055493 |

### mascara_de_producao__calculo_de_horas_hose (62 linhas)

| coluna | tipo | vazio % | distintos | exemplos | min | max |
|---|---|---|---|---|---|---|
| production_supervisor | VARCHAR | 5 | 49 | Unit of Entry, Sum of horas, Row Labels | - | - |
| multiple_items | VARCHAR | 60 | 23 | M, Column Labels, 2026 | - | - |
| col_3 | VARCHAR | 77 | 13 | 2026-09-02 00:00:00, 27.058636499999995, 17.5449708 | - | - |
| col_4 | VARCHAR | 69 | 16 | 2026-09-03 00:00:00, 7.665645099999999, 32.639316124800004 | - | - |
| col_5 | VARCHAR | 74 | 15 | 2026-09-04 00:00:00, 32.2192358, 0.0506192 | - | - |
| col_6 | VARCHAR | 71 | 17 | 2026-09-08 00:00:00, 52.32434969999999, 24.745166346999998 | - | - |
| col_7 | VARCHAR | 87 | 8 | 2026-09-09 00:00:00, 15.258159000000003, 111.19103959999997 | - | - |
| col_8 | VARCHAR | 66 | 19 | 2026-09-10 00:00:00, 0.2497185, 0.26322491 | - | - |
| col_9 | VARCHAR | 76 | 14 | 2026-09-11 00:00:00, 21.701375999999996, 0.17467523920000003 | - | - |
| col_10 | VARCHAR | 85 | 9 | 2026-09-12 00:00:00, 18.762647999999995, 26.1321516 | - | - |
| col_11 | VARCHAR | 68 | 18 | 2026-09-14 00:00:00, 0.14693639999999997, 26.420217300000004 | - | - |
| col_12 | VARCHAR | 76 | 14 | 2026-09-15 00:00:00, 19.056520799999998, 0.0887888 | - | - |
| col_13 | VARCHAR | 82 | 10 | 2026-09-16 00:00:00, 26.828125200000002, 42.6088812 | - | - |
| col_14 | VARCHAR | 71 | 17 | 2026-09-17 00:00:00, 18.6595026, 15.089051399999999 | - | - |
| col_15 | VARCHAR | 81 | 12 | 2026-09-18 00:00:00, 0.49037349999999996, 0.1148184 | - | - |
| col_16 | VARCHAR | 81 | 12 | 2026-09-21 00:00:00, 16.1823255, 0.047884800000000005 | - | - |
| col_17 | VARCHAR | 82 | 11 | 2026-09-22 00:00:00, 0.10282025, 6.076445806999999 | - | - |
| col_18 | VARCHAR | 84 | 10 | 2026-09-23 00:00:00, 7.410869199999999, 7.877613 | - | - |
| col_19 | VARCHAR | 71 | 17 | 2026-09-24 00:00:00, 0.04521119999999999, 7.7763746 | - | - |
| col_20 | VARCHAR | 76 | 13 | 2026-09-25 00:00:00, 24.888927644000002, 0.23088643499999995 | - | - |
| col_21 | VARCHAR | 84 | 9 | 2026-09-26 00:00:00, 38.051129339300005, 84.537688 | - | - |
| col_22 | VARCHAR | 94 | 4 | 2026-09-27 00:00:00, 34.421240000000004, 24.217761199999998 | - | - |
| col_23 | VARCHAR | 77 | 12 | 2026-09-28 00:00:00, 12.768432941999999, 0.79071737745 | - | - |
| col_24 | VARCHAR | 71 | 13 | 2026-09-29 00:00:00, 56.991310999999996, 12.594299539999996 | - | - |
| col_25 | VARCHAR | 79 | 12 | 2026-09-30 00:00:00, 51.7694197, 14.080507877999999 | - | - |
| col_26 | VARCHAR | 8 | 45 | set Total, 0.2602269, 67.12356159999999 | - | - |
| col_27 | VARCHAR | 8 | 45 | Qtr3 Total, 0.2602269, 67.12356159999999 | - | - |
| col_28 | VARCHAR | 8 | 45 | 2026 Total, 0.2602269, 67.12356159999999 | - | - |
| col_29 | VARCHAR | 8 | 45 | Grand Total, 0.2602269, 67.12356159999999 | - | - |

### mascara_de_producao__conferencia (13 linhas)

| coluna | tipo | vazio % | distintos | exemplos | min | max |
|---|---|---|---|---|---|---|
| posting_date | TIMESTAMP | 0 | 13 | 2026-01-16 00:00:00, 2026-01-19 00:00:00, 2026-01-20 00:00:... | 2026-01-16 00:00:00 | 2026-01-31 00:00:00 |
| sistema_x_ficha | VARCHAR | 0 | 1 | OK | - | - |

### mascara_de_producao__coois (2763 linhas)

| coluna | tipo | vazio % | distintos | exemplos | min | max |
|---|---|---|---|---|---|---|
| actual_finish_date | VARCHAR | 0 | 112 | 46296, 46295, 46294 | - | - |
| order | BIGINT | 0 | 2763 | 30064244, 30079092, 30080651 | 23252390 | 30409827 |
| material | VARCHAR | 0 | 1193 | 12107952, 12101137, 91784100-BRA | - | - |
| confirmed_yield_quantity_gmein | DOUBLE | 0 | 806 | 20.0, 2000.0, 17.0 | 0.0 | 5972.9 |
| order_type | VARCHAR | 0 | 4 | ZBM1, ZBMA, ZBMC | - | - |
| mrp_controller | VARCHAR | 0 | 4 | Z35, AIH, AWE | - | - |
| production_supervisor | VARCHAR | 0 | 4 | HAS, HOS, FIT | - | - |
| plant | VARCHAR | 0 | 1 | H204 | - | - |
| order_quantity_gmein | BIGINT | 0 | 313 | 20, 2000, 17 | 1 | 5000 |
| unit_of_measure_gmein | VARCHAR | 0 | 3 | PC, KG, M | - | - |
| basic_start_date | TIMESTAMP | 0 | 132 | 2026-09-30 00:00:00, 2026-09-23 00:00:00, 2026-09-29 00:00:... | 2024-11-13 00:00:00 | 2026-12-30 00:00:00 |
| basic_finish_date | TIMESTAMP | 0 | 135 | 2026-10-01 00:00:00, 2026-09-26 00:00:00, 2026-10-05 00:00:... | 2024-11-13 00:00:00 | 2027-01-13 00:00:00 |
| system_status | VARCHAR | 0 | 35 | REL PRT CNF DLV PRC..., TECO CNF DLV PRC DI..., REL MSPT PR... | - | - |
| production_version | VARCHAR | 0 | 5 | S001, S002, S003 | - | - |
| material_description | VARCHAR | 0 | 504 | HOSE-AER, EHP519, -..., INSULATION ESPESSUR..., HOSE ASSY, ... | - | - |
| confirmation_yield_quantity_conf_unit | BIGINT | 0 | 1 | 0 | 0 | 0 |
| confirmed_finish_date | BIGINT | 16 | 97 | 46296, 46295, 46294 | 45609 | 46296 |

### mascara_de_producao__detail1 (2415 linhas)

| coluna | tipo | vazio % | distintos | exemplos | min | max |
|---|---|---|---|---|---|---|
| details_for_sum_of_qty_in_unit_of_entry_production_supervisor_hos_mrp_controller_aih_anos_posting_date_2026_unit_of_entry_m | VARCHAR | 0 | 2 | MRP controller, AIH | - | - |
| col_2 | VARCHAR | 0 | 2 | Production Supervis..., HOS | - | - |
| col_3 | VARCHAR | 0 | 40 | Material, 2556-10, HC139-7 | - | - |
| col_4 | VARCHAR | 0 | 306 | Order, 29763284, 29788884 | - | - |
| col_5 | VARCHAR | 0 | 36 | Material Description, HOSE-AER, 2556, -10..., HOSE-AER, HC1... | - | - |
| col_6 | VARCHAR | 0 | 2 | Plant, H204 | - | - |
| col_7 | VARCHAR | 0 | 2 | Storage location, GRT4 | - | - |
| col_8 | VARCHAR | 0 | 3 | Movement type, 101, 102 | - | - |
| col_9 | VARCHAR | 100 | 1 | Special Stock | - | - |
| col_10 | VARCHAR | 0 | 2411 | Material Document, 3025039662, 3025507311 | - | - |
| col_11 | VARCHAR | 0 | 11 | Material Doc.Item, 1, 5 | - | - |
| col_12 | VARCHAR | 0 | 23 | Posting Date, 2026-09-01 00:00:00, 2026-09-08 00:00:00 | - | - |
| col_13 | VARCHAR | 0 | 1136 | Qty in unit of entry, 4.2, 6.3 | - | - |
| col_14 | VARCHAR | 0 | 2 | Unit of Entry, M | - | - |
| col_15 | VARCHAR | 100 | 1 | Order Price Unit | - | - |
| col_16 | VARCHAR | 0 | 2 | Sales Value, 0 | - | - |
| col_17 | VARCHAR | 0 | 1136 | Quantity, 4.2, 6.3 | - | - |
| col_18 | VARCHAR | 0 | 10 | User Name, U452021, U395488 | - | - |
| col_19 | VARCHAR | 0 | 3 | Movement Type Text, GR for order, GR for order rev. | - | - |
| col_20 | VARCHAR | 100 | 1 | Document Header Text | - | - |
| col_21 | VARCHAR | 0 | 2122 | Amt.in Loc.Cur., 69.64, 117.68 | - | - |
| col_22 | VARCHAR | 0 | 2 | Ext. Amount in Loca..., 0 | - | - |
| col_23 | VARCHAR | 100 | 1 | Cost Center | - | - |
| col_24 | VARCHAR | 0 | 2 | Sales Value inc. VAT, 0 | - | - |
| col_25 | VARCHAR | 0 | 27 | H/m, 0.031894, 0.027408 | - | - |
| col_26 | VARCHAR | 0 | 2094 | horas, 0.1339548, 0.17267039999999997 | - | - |

### mascara_de_producao__detalhes1 (2608 linhas)

| coluna | tipo | vazio % | distintos | exemplos | min | max |
|---|---|---|---|---|---|---|
| detalhes_do_sum_of_qty_in_unit_of_entry_production_supervisor_hos_mrp_controller_aih_unit_of_entry_m | VARCHAR | 0 | 2 | MRP controller, AIH | - | - |
| col_2 | VARCHAR | 0 | 2 | Production Supervis..., HOS | - | - |
| col_3 | VARCHAR | 0 | 36 | Material, HC139-7_S-GX, HC139-7 | - | - |
| col_4 | VARCHAR | 0 | 302 | Order, 25518986, 25503100 | - | - |
| col_5 | VARCHAR | 0 | 31 | Material Description, MANG SIM. SAEJ1402 ..., MANG SIM. SAE... | - | - |
| col_6 | VARCHAR | 0 | 2 | Plant, H204 | - | - |
| col_7 | VARCHAR | 0 | 2 | Storage location, GRT4 | - | - |
| col_8 | VARCHAR | 0 | 3 | Movement type, 101, 102 | - | - |
| col_9 | VARCHAR | 100 | 1 | Special Stock | - | - |
| col_10 | VARCHAR | 0 | 2608 | Material Document, 4995630703, 4995630846 | - | - |
| col_11 | VARCHAR | 0 | 7 | Material Doc.Item, 1, 6 | - | - |
| col_12 | VARCHAR | 0 | 25 | Posting Date, 2025-07-03 00:00:00, 2025-07-04 00:00:00 | - | - |
| col_13 | VARCHAR | 0 | 1202 | Qty in unit of entry, 43.7, 19.4 | - | - |
| col_14 | VARCHAR | 0 | 2 | Unit of Entry, M | - | - |
| col_15 | VARCHAR | 100 | 1 | Order Price Unit | - | - |
| col_16 | VARCHAR | 0 | 2 | Sales Value, 0 | - | - |
| col_17 | VARCHAR | 0 | 1202 | Quantity, 43.7, 19.4 | - | - |
| col_18 | VARCHAR | 0 | 9 | User Name, U398090, U395462 | - | - |
| col_19 | VARCHAR | 0 | 3 | Movement Type Text, GR for order, GR for order rev. | - | - |
| col_20 | VARCHAR | 100 | 1 | Document Header Text | - | - |
| col_21 | VARCHAR | 0 | 2327 | Amt.in Loc.Cur., 629.72, 279.55 | - | - |
| col_22 | VARCHAR | 0 | 2 | Ext. Amount in Loca..., 0 | - | - |
| col_23 | VARCHAR | 100 | 1 | Cost Center | - | - |
| col_24 | VARCHAR | 0 | 2 | Sales Value inc. VAT, 0 | - | - |
| col_25 | VARCHAR | 0 | 23 | H/m, 0.027408, 0.038241000000000004 | - | - |
| col_26 | VARCHAR | 0 | 2257 | horas, 1.1977296, 0.5317151999999999 | - | - |

### mascara_de_producao__mascara_de_producao (12 linhas)

| coluna | tipo | vazio % | distintos | exemplos | min | max |
|---|---|---|---|---|---|---|
| unit_of_entry | VARCHAR | 25 | 9 | Sum of Qty in unit ..., Row Labels, AIH | - | - |
| multiple_items | VARCHAR | 0 | 9 | Column Labels, 2026, Qtr4 | - | - |
| col_3 | VARCHAR | 33 | 5 | out Total, 2999.17, 2017 | - | - |
| col_4 | VARCHAR | 33 | 5 | Qtr4 Total, 2999.17, 2017 | - | - |
| col_5 | VARCHAR | 33 | 5 | 2026 Total, 2999.17, 2017 | - | - |
| col_6 | VARCHAR | 33 | 5 | Grand Total, 2999.17, 2017 | - | - |

### mascara_de_producao__mb51 (109953 linhas)

| coluna | tipo | vazio % | distintos | exemplos | min | max |
|---|---|---|---|---|---|---|
| mrp_controller | VARCHAR | 92 | 4 | Z35, AWE, AO0 | - | - |
| production_supervisor | VARCHAR | 92 | 3 | HAS, FIT, HOS | - | - |
| material | VARCHAR | 0 | 2813 | 0082721300-BRA1, 0086303161-BRA1, 0086310227-BRA1 | - | - |
| order | BIGINT | 0 | 28296 | 29993940, 24776784, 24544232 | 23158071 | 30409827 |
| material_description | VARCHAR | 0 | 887 | HOSE ASSY, AER-PRM,..., HOSE ASSY, AER-PRM,..., HOSE ASSY, ... | - | - |
| plant | VARCHAR | 0 | 1 | H204 | - | - |
| storage_location | VARCHAR | 0 | 4 | GRT4, HOSE, KAN | - | - |
| movement_type | BIGINT | 0 | 2 | 101, 102 | 101 | 102 |
| material_document | BIGINT | 0 | 107966 | 3025181030, 4991069079, 4991069230 | 3000000022 | 5028210126 |
| material_doc_item | BIGINT | 0 | 90 | 1, 2, 6 | 1 | 100 |
| posting_date | TIMESTAMP | 0 | 537 | 2026-09-02 00:00:00, 2025-04-28 00:00:00, 2025-03-29 00:00:... | 2024-11-04 00:00:00 | 2026-10-01 00:00:00 |
| qty_in_unit_of_entry | DOUBLE | 0 | 4252 | 7.0, 20.0, 10.0 | -5000.0 | 126054.328 |
| unit_of_entry | VARCHAR | 0 | 3 | PC, M, KG | - | - |
| order_price_unit | VARCHAR | 100 | 2 | PC, KG | - | - |
| sales_value | BIGINT | 0 | 1 | 0 | 0 | 0 |
| quantity | DOUBLE | 0 | 4252 | 7.0, 20.0, 10.0 | -5000.0 | 126054.328 |
| user_name | VARCHAR | 0 | 68 | U395240, U401731, U395739 | - | - |
| movement_type_text | VARCHAR | 0 | 4 | GR for order, GR for order rev., GR goods receipt | - | - |
| document_header_text | VARCHAR | 100 | 1 | Ordem Mercedez | - | - |
| amt_in_loc_cur | DOUBLE | 0 | 50405 | 418.25, 1045.0, 522.5 | -571840.0 | 571840.0 |
| ext_amount_in_local_currency | BIGINT | 0 | 1 | 0 | 0 | 0 |
| sales_value_inc_vat | BIGINT | 0 | 1 | 0 | 0 | 0 |
| h_m | DOUBLE | 0 | 36 | 0.0, 0.031894, 0.029926927000000002 | 0.0 | 0.055493 |
| horas | DOUBLE | 0 | 22128 | 0.0, 0.0733562, 1.068449 | -33.4384 | 33.4384 |
| col_25 | VARCHAR | 100 | 2 |  , scrap | - | - |
| col_26 | VARCHAR | 100 | 1 | , | - | - |
| col_27 | VARCHAR | 100 | 9 | HC101-6, HC139-7, GH781-16 | - | - |
| col_28 | VARCHAR | 100 | 11 | 656.8, 180, 489.2 | - | - |
| col_29 | BIGINT | 100 | 1 | 0 | 0 | 0 |
| col_30 | BIGINT | 100 | 1 | 0 | 0 | 0 |
| col_31 | DOUBLE | 100 | 2 | 8727.5, 0.0 | 0.0 | 8727.5 |
| col_32 | BIGINT | 100 | 1 | 0 | 0 | 0 |
| col_33 | BIGINT | 100 | 1 | 0 | 0 | 0 |
| col_34 | BIGINT | 100 | 1 | 0 | 0 | 0 |
| col_35 | BIGINT | 100 | 1 | 0 | 0 | 0 |
| col_36 | BIGINT | 100 | 1 | 0 | 0 | 0 |
| col_37 | BIGINT | 100 | 1 | 0 | 0 | 0 |
| col_38 | BIGINT | 100 | 1 | 0 | 0 | 0 |
| col_39 | BIGINT | 100 | 1 | 0 | 0 | 0 |
| col_40 | BIGINT | 100 | 1 | 0 | 0 | 0 |
| col_41 | BIGINT | 100 | 1 | 0 | 0 | 0 |
| col_42 | BIGINT | 100 | 1 | 0 | 0 | 0 |
| col_43 | BIGINT | 100 | 1 | 0 | 0 | 0 |
| col_44 | BIGINT | 100 | 1 | 0 | 0 | 0 |
| col_45 | BIGINT | 100 | 1 | 0 | 0 | 0 |
| col_46 | BIGINT | 100 | 1 | 0 | 0 | 0 |
| col_47 | BIGINT | 100 | 1 | 0 | 0 | 0 |
| col_48 | BIGINT | 100 | 1 | 0 | 0 | 0 |
| col_49 | BIGINT | 100 | 1 | 0 | 0 | 0 |
| col_50 | BIGINT | 100 | 1 | 0 | 0 | 0 |
| col_51 | BIGINT | 100 | 1 | 0 | 0 | 0 |
| col_52 | BIGINT | 100 | 1 | 0 | 0 | 0 |
| col_53 | BIGINT | 100 | 1 | 0 | 0 | 0 |
| col_54 | BIGINT | 100 | 1 | 0 | 0 | 0 |
| col_55 | BIGINT | 100 | 1 | 0 | 0 | 0 |
| col_56 | BIGINT | 100 | 1 | 0 | 0 | 0 |
| col_57 | BIGINT | 100 | 1 | 0 | 0 | 0 |
| col_58 | BIGINT | 100 | 1 | 0 | 0 | 0 |
| col_59 | BIGINT | 100 | 1 | 0 | 0 | 0 |
| col_60 | BIGINT | 100 | 1 | 0 | 0 | 0 |
| col_61 | BIGINT | 100 | 1 | 0 | 0 | 0 |
| col_62 | BIGINT | 100 | 1 | 0 | 0 | 0 |
| col_63 | BIGINT | 100 | 1 | 0 | 0 | 0 |

### mascara_de_producao__plano (92 linhas)

| coluna | tipo | vazio % | distintos | exemplos | min | max |
|---|---|---|---|---|---|---|
| dash | BIGINT | 1 | 9 | 6, 4, 8 | 3 | 16 |
| wide_braiders | VARCHAR | 1 | 4 | 2 A, 1 A, 4 A | - | - |
| construction | VARCHAR | 1 | 7 | DD20-04/06, SD20-04/06, SD24-08/10/12 | - | - |
| braider | VARCHAR | 1 | 9 | TH06, TH01, TM04 | - | - |
| pn | VARCHAR | 0 | 92 | EC215-06LRL, FC735-04, FC735-06 | - | - |
| november_production | BIGINT | 0 | 23 | 0, 18460, 15640 | 0 | 128000 |
| a_produzir | BIGINT | 67 | 14 | 0, 1360, 1840 | 0 | 22770 |
| concluido | VARCHAR | 0 | 1 | - | - | - |

### mascara_de_producao__power_automate (3 linhas)

| coluna | tipo | vazio % | distintos | exemplos | min | max |
|---|---|---|---|---|---|---|
| production_supervisor | VARCHAR | 0 | 3 | HOS, HAS, FIT | - | - |
| qty_in_unit_of_entry | DOUBLE | 0 | 3 | 3215.056999999999, 2589.911, 0.0 | 0.0 | 3215.056999999999 |

### mascara_de_producao__resumo (17 linhas)

| coluna | tipo | vazio % | distintos | exemplos | min | max |
|---|---|---|---|---|---|---|
| mangueira | VARCHAR | 0 | 7 | Meta diária, Dias úteis, Dias contabilizados | - | - |
| col_2 | DOUBLE | 12 | 11 | 7500.0, 23.0, 1.0 | -7685.0 | 23000.0 |
| col_3 | VARCHAR | 82 | 2 | J, L | - | - |
| col_4 | DOUBLE | 94 | 1 | 6665.652173913043 | 6665.652173913043 | 6665.652173913043 |

### mascara_de_producao__resumo_bi (18 linhas)

| coluna | tipo | vazio % | distintos | exemplos | min | max |
|---|---|---|---|---|---|---|
| produto | VARCHAR | 0 | 3 | MANGUEIRA, Montagem, Fittings | - | - |
| tipo | VARCHAR | 0 | 6 | Meta diária, Dias úteis, Dias contabilizados | - | - |
| valor | DOUBLE | 0 | 12 | 7500.0, 23.0, 1.0 | -23000.0 | 23000.0 |
| sigla | VARCHAR | 0 | 3 | HOS, HAS, FIT | - | - |
| sigla2 | VARCHAR | 0 | 3 | AIH, Z35, AO0 | - | - |

### mb51__sheet1 (113122 linhas)

| coluna | tipo | vazio % | distintos | exemplos | min | max |
|---|---|---|---|---|---|---|
| material | VARCHAR | 0 | 2862 | 11470743, 11471183, 11471283 | - | - |
| order | BIGINT | 0 | 29260 | 30450044, 30406694, 30364950 | 23158071 | 30603553 |
| material_description | VARCHAR | 0 | 909 | HOSE ASSY, WIN-PRM,..., HOSE ASSY, WIN-PRM,..., HOSE ASSY, ... | - | - |
| plant | VARCHAR | 0 | 1 | H204 | - | - |
| storage_location | VARCHAR | 0 | 4 | GRT4, HOSE, KAN | - | - |
| movement_type | BIGINT | 0 | 2 | 101, 102 | 101 | 102 |
| material_document | BIGINT | 0 | 111097 | 3028558290, 3027710634, 3027709370 | 3000000022 | 5028494302 |
| material_doc_item | BIGINT | 0 | 90 | 1, 2, 6 | 1 | 100 |
| posting_date | TIMESTAMP | 0 | 555 | 2026-10-20 00:00:00, 2026-10-08 00:00:00, 2026-09-21 00:00:... | 2024-11-04 00:00:00 | 2026-10-21 00:00:00 |
| qty_in_unit_of_entry | DOUBLE | 0 | 4510 | 3.0, 6.0, 2.0 | -12000.0 | 5088378.898 |
| unit_of_entry | VARCHAR | 0 | 3 | PC, M, KG | - | - |
| order_price_unit | VARCHAR | 100 | 2 | PC, KG | - | - |
| sales_value | BIGINT | 0 | 1 | 0 | 0 | 0 |
| quantity | DOUBLE | 0 | 4510 | 3.0, 6.0, 2.0 | -12000.0 | 5088378.898 |
| user_name | VARCHAR | 0 | 68 | U395240, U395297, U395471 | - | - |
| movement_type_text | VARCHAR | 0 | 4 | GR for order, GR for order rev., GR goods receipt | - | - |
| document_header_text | VARCHAR | 100 | 1 | Ordem Mercedez | - | - |
| amt_in_loc_cur | DOUBLE | 0 | 51802 | 279.96, 245.46, 142.53 | -571840.0 | 187375690.97 |
| ext_amount_in_local_currency | BIGINT | 0 | 1 | 0 | 0 | 0 |
| sales_value_inc_vat | BIGINT | 0 | 1 | 0 | 0 | 0 |

### registrosinspecao (16542 linhas)

| coluna | tipo | vazio % | distintos | exemplos | min | max |
|---|---|---|---|---|---|---|
| op_id | BIGINT | 0 | 2226 | 26765298, 26707322, 26434707 | 0 | 30393874 |
| quantidade | VARCHAR | 0 | 1837 | 50, 10, 150 | - | - |
| diametro_interno | VARCHAR | 0 | 620 | 26, 10, 30 | - | - |
| diametro_externo | VARCHAR | 0 | 1278 | 32, 10, 50 | - | - |
| concentricidade | VARCHAR | 0 | 135 | 532, 10, 60 | - | - |
| datahorainspecao | VARCHAR | 0 | 15098 | 11/11/2025 11:02 AM, 11/11/2025 1:59 PM, 11/11/2025 2:00 PM | - | - |
| turnoteste | BIGINT | 0 | 3 | 1, 2, 3 | 1 | 3 |
| criado | VARCHAR | 0 | 15103 | 11/11/2025 11:02 AM, 11/11/2025 1:59 PM, 11/11/2025 2:00 PM | - | - |
| mangueira | VARCHAR | 13 | 62 | GH781-12, GH781-4, GH681-6 | - | - |
| codigodefeito | VARCHAR | 100 | 1 | A - Quebra de Fio d... | - | - |
| trancadeira | VARCHAR | 24 | 18 | TH07, TH06, TM01 | - | - |
| cabine_teste | VARCHAR | 96 | 2 | CABINE_L1, CABINE_L2 | - | - |

### tiposerros (5434 linhas)

| coluna | tipo | vazio % | distintos | exemplos | min | max |
|---|---|---|---|---|---|---|
| op_id | BIGINT | 0 | 1612 | 26707322, 27025097, 27324660 | 0 | 30393874 |
| codigoerro | VARCHAR | 0 | 16 | A - Quebra de Fio d..., M - Excentricidade, G Falha na Band... | - | - |
| quantidade | DOUBLE | 0 | 233 | 40.0, 3.0, 0.2 | 0.0 | 750.0 |
| criado | VARCHAR | 0 | 2897 | 11/11/2025 2:36 PM, 12/11/2025 10:46 AM, 1/14/2026 10:04 PM | - | - |
| datahorarefugo | VARCHAR | 7 | 163 | 2/26/2026, 2/27/2026, 2/28/2026 | - | - |
| trancadeira | VARCHAR | 17 | 18 | TH06, TM01, TH07 | - | - |
| turno_erro | BIGINT | 18 | 3 | 2, 1, 3 | 1 | 3 |
| cabine_teste | VARCHAR | 94 | 2 | CABINE_L1, CABINE_L2 | - | - |

## Ligacoes candidatas (descobertas pelos dados)

Sao palpites: confirme nas Notas do William antes de confiar.

| coluna A | coluna B | sobreposicao | em comum | motivo |
|---|---|---|---|---|
| bd_packing_list__data_base.id | ficha_producao.bitola | 100% | 10 | valores |
| bd_packing_list__data_base.id | ficha_producao.carretel_entrada | 100% | 37 | valores |
| bd_packing_list__data_base.id | ficha_producao.carretel_saida | 100% | 57 | valores |
| bd_packing_list__data_base.id | ficha_producao.qtd_turno3_cobertura | 100% | 9 | valores |
| bd_packing_list__data_base.id | ficha_producao.qtd_turno3_vulcanizacao | 100% | 37 | valores |
| bd_packing_list__data_base.id | mascara_de_producao__cadastro_mangueiras.bitola | 100% | 9 | valores |
| bd_packing_list__data_base.id | mascara_de_producao__mb51.material_doc_item | 100% | 90 | valores |
| bd_packing_list__data_base.id | mascara_de_producao__plano.dash | 100% | 9 | valores |
| bd_packing_list__data_base.id | mb51__sheet1.material_doc_item | 100% | 90 | valores |
| bd_packing_list__data_base.pn | mascara_de_producao__mb51.col_27 | 100% | 9 | valores |
| bd_packing_list__data_base.slice | ficha_producao.bitola | 100% | 10 | valores |
| bd_packing_list__data_base.slice | mascara_de_producao__cadastro_mangueiras.bitola | 100% | 9 | valores |
| bd_packing_list__data_base.slice | mascara_de_producao__plano.dash | 100% | 9 | valores |
| bd_packing_list__data_base.slice | registrosinspecao.quantidade | 100% | 27 | valores |
| ficha_producao.bitola | mascara_de_producao__cadastro_mangueiras.bitola | 100% | 9 | valores + nome |
| ficha_producao.bitola | mascara_de_producao__coois.order_quantity_gmein | 100% | 10 | valores |
| ficha_producao.bitola | mascara_de_producao__detail1.col_13 | 100% | 10 | valores |
| ficha_producao.bitola | mascara_de_producao__detail1.col_17 | 100% | 10 | valores |
| ficha_producao.bitola | mascara_de_producao__mb51.material_doc_item | 100% | 10 | valores |
| ficha_producao.bitola | mascara_de_producao__plano.dash | 100% | 9 | valores |
| ficha_producao.bitola | mb51__sheet1.material_doc_item | 100% | 10 | valores |
| ficha_producao.bitola | registrosinspecao.concentricidade | 100% | 10 | valores |
| ficha_producao.bitola | registrosinspecao.quantidade | 100% | 10 | valores |
| ficha_producao.carretel_entrada | registrosinspecao.quantidade | 100% | 37 | valores |
| ficha_producao.carretel_saida | mascara_de_producao__cadastro_mangueiras.bitola | 100% | 9 | valores |
| ficha_producao.carretel_saida | mascara_de_producao__plano.dash | 100% | 9 | valores |
| ficha_producao.carretel_saida | registrosinspecao.quantidade | 100% | 57 | valores |
| ficha_producao.defeito_cobertura | mascara_de_producao__cadastro_mangueiras.bitola | 100% | 9 | valores |
| ficha_producao.defeito_cobertura | mascara_de_producao__plano.dash | 100% | 9 | valores |
| ficha_producao.mangueira | mascara_de_producao__mb51.col_27 | 100% | 9 | valores |
| ficha_producao.trancadeira | registrosinspecao.trancadeira | 100% | 18 | valores + nome |
| ficha_producao.trancadeira | tiposerros.trancadeira | 100% | 18 | valores + nome |
| mascara_de_producao__cadastro_mangueiras.bitola | mascara_de_producao__coois.order_quantity_gmein | 100% | 9 | valores |
| mascara_de_producao__cadastro_mangueiras.bitola | mascara_de_producao__detail1.col_13 | 100% | 9 | valores |
| mascara_de_producao__cadastro_mangueiras.bitola | mascara_de_producao__detail1.col_17 | 100% | 9 | valores |
| mascara_de_producao__cadastro_mangueiras.bitola | mascara_de_producao__mb51.material_doc_item | 100% | 9 | valores |
| mascara_de_producao__cadastro_mangueiras.bitola | mascara_de_producao__plano.dash | 100% | 9 | valores |
| mascara_de_producao__cadastro_mangueiras.bitola | mb51__sheet1.material_doc_item | 100% | 9 | valores |
| mascara_de_producao__cadastro_mangueiras.bitola | registrosinspecao.concentricidade | 100% | 9 | valores |
| mascara_de_producao__cadastro_mangueiras.bitola | registrosinspecao.quantidade | 100% | 9 | valores |
| mascara_de_producao__coois.material | mb51__sheet1.material | 100% | 1193 | valores + nome |
| mascara_de_producao__coois.material_description | mb51__sheet1.material_description | 100% | 501 | valores + nome |
| mascara_de_producao__coois.mrp_controller | mascara_de_producao__mb51.mrp_controller | 100% | 4 | nome parecido |
| mascara_de_producao__coois.order | mb51__sheet1.order | 100% | 2763 | valores + nome |
| mascara_de_producao__coois.order_quantity_gmein | mascara_de_producao__plano.dash | 100% | 9 | valores |
| mascara_de_producao__coois.production_supervisor | mascara_de_producao__mb51.production_supervisor | 100% | 3 | nome parecido |
| mascara_de_producao__coois.production_supervisor | mascara_de_producao__power_automate.production_supervisor | 100% | 3 | nome parecido |
| mascara_de_producao__detail1.col_11 | mascara_de_producao__detalhes1.col_11 | 100% | 7 | valores + nome |
| mascara_de_producao__detail1.col_13 | mascara_de_producao__plano.dash | 100% | 9 | valores |
| mascara_de_producao__detail1.col_17 | mascara_de_producao__plano.dash | 100% | 9 | valores |
| mascara_de_producao__detail1.col_19 | mascara_de_producao__detalhes1.col_19 | 100% | 3 | nome parecido |
| mascara_de_producao__detail1.col_8 | mascara_de_producao__detalhes1.col_8 | 100% | 3 | nome parecido |
| mascara_de_producao__mb51.material | mb51__sheet1.material | 100% | 2813 | valores + nome |
| mascara_de_producao__mb51.material_description | mb51__sheet1.material_description | 100% | 881 | valores + nome |
| mascara_de_producao__mb51.material_doc_item | mascara_de_producao__plano.dash | 100% | 9 | valores |
| mascara_de_producao__mb51.material_doc_item | mb51__sheet1.material_doc_item | 100% | 90 | valores + nome |
| mascara_de_producao__mb51.material_doc_item | registrosinspecao.quantidade | 100% | 90 | valores |
| mascara_de_producao__mb51.material_document | mb51__sheet1.material_document | 100% | 107966 | valores + nome |
| mascara_de_producao__mb51.movement_type_text | mb51__sheet1.movement_type_text | 100% | 4 | nome parecido |
| mascara_de_producao__mb51.order | mb51__sheet1.order | 100% | 28296 | valores + nome |
| mascara_de_producao__mb51.production_supervisor | mascara_de_producao__power_automate.production_supervisor | 100% | 3 | nome parecido |
| mascara_de_producao__mb51.storage_location | mb51__sheet1.storage_location | 100% | 4 | nome parecido |
| mascara_de_producao__mb51.unit_of_entry | mb51__sheet1.unit_of_entry | 100% | 3 | nome parecido |
| mascara_de_producao__mb51.user_name | mb51__sheet1.user_name | 100% | 68 | valores + nome |
| mascara_de_producao__plano.dash | mb51__sheet1.material_doc_item | 100% | 9 | valores |
| mascara_de_producao__plano.dash | registrosinspecao.concentricidade | 100% | 9 | valores |
| mascara_de_producao__plano.dash | registrosinspecao.quantidade | 100% | 9 | valores |
| mb51__sheet1.material_doc_item | registrosinspecao.quantidade | 100% | 90 | valores |
| registrosinspecao.trancadeira | tiposerros.trancadeira | 100% | 18 | valores + nome |
| mascara_de_producao__detalhes1.col_10 | mascara_de_producao__mb51.material_document | 100% | 2607 | valores |
| mascara_de_producao__detalhes1.col_10 | mb51__sheet1.material_document | 100% | 2607 | valores |
| mascara_de_producao__detail1.col_10 | mascara_de_producao__mb51.material_document | 100% | 2410 | valores |
| mascara_de_producao__detail1.col_10 | mb51__sheet1.material_document | 100% | 2410 | valores |
| registrosinspecao.op_id | tiposerros.op_id | 100% | 1609 | valores + nome |
| ficha_producao.op | mascara_de_producao__detail1.col_4 | 100% | 305 | valores |
| mascara_de_producao__coois.order | mascara_de_producao__detail1.col_4 | 100% | 305 | valores |
| mascara_de_producao__detail1.col_4 | mascara_de_producao__mb51.order | 100% | 305 | valores |
| mascara_de_producao__detail1.col_4 | mb51__sheet1.order | 100% | 305 | valores |
| mascara_de_producao__detail1.col_4 | registrosinspecao.op_id | 100% | 305 | valores |
| mascara_de_producao__detalhes1.col_4 | mascara_de_producao__mb51.order | 100% | 301 | valores |
| mascara_de_producao__detalhes1.col_4 | mb51__sheet1.order | 100% | 301 | valores |
| mascara_de_producao__coois.order | mascara_de_producao__mb51.order | 100% | 2753 | valores + nome |
| mascara_de_producao__coois.material | mascara_de_producao__mb51.material | 99% | 1187 | valores + nome |
| mb51__sheet1.order | tiposerros.op_id | 99% | 1602 | valores |
| mb51__sheet1.order | registrosinspecao.op_id | 99% | 2212 | valores |
| mascara_de_producao__mb51.order | registrosinspecao.op_id | 99% | 2207 | valores |
| ficha_producao.op | tiposerros.op_id | 99% | 1597 | valores |
| mascara_de_producao__mb51.order | tiposerros.op_id | 99% | 1597 | valores |
| mascara_de_producao__coois.material_description | mascara_de_producao__mb51.material_description | 99% | 495 | valores + nome |
| ficha_producao.op | mb51__sheet1.order | 99% | 2648 | valores |
| ficha_producao.op | registrosinspecao.op_id | 99% | 2198 | valores |
| ficha_producao.mangueira | registrosinspecao.mangueira | 98% | 60 | valores + nome |
| mascara_de_producao__calculo_de_horas_hose.production_supervisor | mascara_de_producao__detail1.col_3 | 98% | 39 | valores |
| mascara_de_producao__coois.material | mascara_de_producao__detail1.col_3 | 98% | 39 | valores |
| mascara_de_producao__detail1.col_3 | mascara_de_producao__mb51.material | 98% | 39 | valores |
| mascara_de_producao__detail1.col_3 | mb51__sheet1.material | 98% | 39 | valores |
| bd_packing_list__data_base.id | ficha_producao.qtd_turno3_bandagem | 97% | 37 | valores |
| ficha_producao.carretel_entrada | mascara_de_producao__coois.order_quantity_gmein | 97% | 36 | valores |
| ficha_producao.mangueira | mascara_de_producao__detalhes1.col_3 | 97% | 35 | valores |
| mascara_de_producao__cadastro_mangueiras.mangueira_hose | mascara_de_producao__detalhes1.col_3 | 97% | 35 | valores |
| mascara_de_producao__coois.material_description | mascara_de_producao__detail1.col_5 | 97% | 35 | valores |
| mascara_de_producao__detail1.col_5 | mascara_de_producao__mb51.material_description | 97% | 35 | valores |
| mascara_de_producao__detail1.col_5 | mb51__sheet1.material_description | 97% | 35 | valores |
| mascara_de_producao__detalhes1.col_3 | mascara_de_producao__mb51.material | 97% | 35 | valores |
| mascara_de_producao__detalhes1.col_3 | mascara_de_producao__plano.pn | 97% | 35 | valores |
| mascara_de_producao__detalhes1.col_3 | mb51__sheet1.material | 97% | 35 | valores |
| bd_packing_list__data_base.id | mascara_de_producao__coois.order_quantity_gmein | 97% | 303 | valores |
| mascara_de_producao__coois.order_quantity_gmein | mascara_de_producao__mb51.material_doc_item | 97% | 87 | valores |
| mascara_de_producao__coois.order_quantity_gmein | mb51__sheet1.material_doc_item | 97% | 87 | valores |
| bd_packing_list__data_base.slice | mascara_de_producao__coois.order_quantity_gmein | 96% | 26 | valores |
| bd_packing_list__data_base.slice | mascara_de_producao__mb51.material_doc_item | 96% | 26 | valores |
| bd_packing_list__data_base.slice | mb51__sheet1.material_doc_item | 96% | 26 | valores |
| ficha_producao.op | mascara_de_producao__mb51.order | 96% | 2576 | valores |
| bd_packing_list__data_base.id | ficha_producao.qtd_turno3_debandagem | 95% | 42 | valores |
| bd_packing_list__data_base.id | ficha_producao.defeito_trancagem | 95% | 20 | valores |
| bd_packing_list__data_base.pn | registrosinspecao.mangueira | 95% | 58 | valores |
| mascara_de_producao__mb51.material | registrosinspecao.mangueira | 95% | 58 | valores |
| mascara_de_producao__plano.pn | registrosinspecao.mangueira | 95% | 58 | valores |
| mb51__sheet1.material | registrosinspecao.mangueira | 95% | 58 | valores |
| bd_packing_list__data_base.pn | mascara_de_producao__detail1.col_3 | 95% | 38 | valores |
| ficha_producao.mangueira | mascara_de_producao__detail1.col_3 | 95% | 38 | valores |
| mascara_de_producao__cadastro_mangueiras.mangueira_hose | mascara_de_producao__detail1.col_3 | 95% | 38 | valores |
| mascara_de_producao__detail1.col_3 | mascara_de_producao__plano.pn | 95% | 38 | valores |
| mascara_de_producao__detail1.col_3 | registrosinspecao.mangueira | 95% | 38 | valores |
| bd_packing_list__data_base.id | ficha_producao.qtd_turno2_debandagem | 95% | 129 | valores |
| ficha_producao.carretel_saida | mascara_de_producao__coois.order_quantity_gmein | 95% | 54 | valores |
| mascara_de_producao__detail1.col_13 | registrosinspecao.quantidade | 95% | 1076 | valores |
| mascara_de_producao__detail1.col_17 | registrosinspecao.quantidade | 95% | 1076 | valores |
| ficha_producao.carretel_entrada | mascara_de_producao__detail1.col_13 | 95% | 35 | valores |
| ficha_producao.carretel_entrada | mascara_de_producao__detail1.col_17 | 95% | 35 | valores |
| ficha_producao.carretel_entrada | mascara_de_producao__mb51.material_doc_item | 95% | 35 | valores |
| ficha_producao.carretel_entrada | mb51__sheet1.material_doc_item | 95% | 35 | valores |
| mascara_de_producao__cadastro_mangueiras.mangueira_hose | mascara_de_producao__plano.pn | 95% | 87 | valores |
| bd_packing_list__data_base.id | ficha_producao.qtd_turno1_debandagem | 94% | 119 | valores |
| bd_packing_list__data_base.pn | mascara_de_producao__detalhes1.col_3 | 94% | 34 | valores |
| mascara_de_producao__detalhes1.col_3 | registrosinspecao.mangueira | 94% | 34 | valores |
| bd_packing_list__data_base.id | ficha_producao.qtd_turno2_bandagem | 94% | 128 | valores |
| mascara_de_producao__detail1.col_4 | tiposerros.op_id | 94% | 288 | valores |
| mascara_de_producao__cadastro_mangueiras.mangueira_hose | registrosinspecao.mangueira | 93% | 57 | valores |
| ficha_producao.carretel_saida | mascara_de_producao__detail1.col_13 | 93% | 53 | valores |
| ficha_producao.carretel_saida | mascara_de_producao__detail1.col_17 | 93% | 53 | valores |
| ficha_producao.datafinalizacao | tiposerros.datahorarefugo | 93% | 140 | valores |
| bd_packing_list__data_base.slice | ficha_producao.carretel_saida | 93% | 25 | valores |
| bd_packing_list__data_base.slice | ficha_producao.defeito_cobertura | 93% | 25 | valores |
| bd_packing_list__data_base.slice | mascara_de_producao__detail1.col_13 | 93% | 25 | valores |
| bd_packing_list__data_base.slice | mascara_de_producao__detail1.col_17 | 93% | 25 | valores |
| bd_packing_list__data_base.id | ficha_producao.qtd_turno2_vulcanizacao | 92% | 136 | valores |
| ficha_producao.carretel_entrada | mascara_de_producao__detalhes1.col_13 | 92% | 34 | valores |
| ficha_producao.carretel_entrada | mascara_de_producao__detalhes1.col_17 | 92% | 34 | valores |
| bd_packing_list__data_base.id | ficha_producao.quantidade_trancagem | 91% | 117 | valores |
| ficha_producao.carretel_saida | mascara_de_producao__mb51.material_doc_item | 91% | 52 | valores |
| ficha_producao.carretel_saida | mb51__sheet1.material_doc_item | 91% | 52 | valores |
| bd_packing_list__data_base.id | mascara_de_producao__detail1.col_11 | 91% | 10 | valores |
| bd_packing_list__data_base.slice | mascara_de_producao__detail1.col_11 | 91% | 10 | valores |
| ficha_producao.carretel_saida | mascara_de_producao__detail1.col_11 | 91% | 10 | valores |
| ficha_producao.defeito_cobertura | mascara_de_producao__detail1.col_11 | 91% | 10 | valores |
| mascara_de_producao__coois.order_quantity_gmein | mascara_de_producao__detail1.col_11 | 91% | 10 | valores |
| mascara_de_producao__detail1.col_11 | mascara_de_producao__mb51.material_doc_item | 91% | 10 | valores |
| mascara_de_producao__detail1.col_11 | mb51__sheet1.material_doc_item | 91% | 10 | valores |
| mascara_de_producao__detail1.col_11 | registrosinspecao.concentricidade | 91% | 10 | valores |
| mascara_de_producao__detail1.col_11 | registrosinspecao.quantidade | 91% | 10 | valores |
| bd_packing_list__data_base.id | ficha_producao.qtd_turno1_cobertura | 91% | 77 | valores |
| bd_packing_list__data_base.id | ficha_producao.quantidade_bandagem | 90% | 173 | valores |
| ficha_producao.bitola | mascara_de_producao__detalhes1.col_13 | 90% | 9 | valores |
| ficha_producao.bitola | mascara_de_producao__detalhes1.col_17 | 90% | 9 | valores |
| mascara_de_producao__detail1.col_18 | mascara_de_producao__mb51.user_name | 90% | 9 | valores |
| mascara_de_producao__detail1.col_18 | mb51__sheet1.user_name | 90% | 9 | valores |
| bd_packing_list__data_base.id | ficha_producao.qtd_turno1_bandagem | 90% | 132 | valores |
| mascara_de_producao__detalhes1.col_13 | registrosinspecao.quantidade | 89% | 1073 | valores |
| mascara_de_producao__detalhes1.col_17 | registrosinspecao.quantidade | 89% | 1073 | valores |
| bd_packing_list__data_base.id | ficha_producao.quantidade_vulcanizacao | 89% | 182 | valores |
| bd_packing_list__data_base.id | ficha_producao.quantidade_debandagem | 89% | 205 | valores |
| bd_packing_list__data_base.slice | registrosinspecao.concentricidade | 89% | 24 | valores |
| ficha_producao.defeito_trancagem | mascara_de_producao__cadastro_mangueiras.bitola | 89% | 8 | valores |
| ficha_producao.defeito_trancagem | mascara_de_producao__plano.dash | 89% | 8 | valores |
| ficha_producao.trancadeira | mascara_de_producao__plano.braider | 89% | 8 | valores |
| mascara_de_producao__cadastro_mangueiras.bitola | mascara_de_producao__detalhes1.col_13 | 89% | 8 | valores |
| mascara_de_producao__cadastro_mangueiras.bitola | mascara_de_producao__detalhes1.col_17 | 89% | 8 | valores |
| mascara_de_producao__cadastro_mangueiras.mangueira_hose | mascara_de_producao__mb51.col_27 | 89% | 8 | valores |
| mascara_de_producao__detail1.col_18 | mascara_de_producao__detalhes1.col_18 | 89% | 8 | valores + nome |
| mascara_de_producao__detalhes1.col_13 | mascara_de_producao__plano.dash | 89% | 8 | valores |
| mascara_de_producao__detalhes1.col_17 | mascara_de_producao__plano.dash | 89% | 8 | valores |
| mascara_de_producao__detalhes1.col_18 | mascara_de_producao__mb51.user_name | 89% | 8 | valores |
| mascara_de_producao__detalhes1.col_18 | mb51__sheet1.user_name | 89% | 8 | valores |
| mascara_de_producao__mb51.col_27 | mascara_de_producao__plano.pn | 89% | 8 | valores |
| mascara_de_producao__mb51.col_27 | mb51__sheet1.material | 89% | 8 | valores |
| mascara_de_producao__mb51.col_27 | registrosinspecao.mangueira | 89% | 8 | valores |
| mascara_de_producao__plano.braider | registrosinspecao.trancadeira | 89% | 8 | valores |
| mascara_de_producao__plano.braider | tiposerros.trancadeira | 89% | 8 | valores |
| bd_packing_list__data_base.id | ficha_producao.qtd_turno1_vulcanizacao | 89% | 148 | valores |
| bd_packing_list__data_base.pn | ficha_producao.mangueira | 88% | 61 | valores |
| ficha_producao.mangueira | mascara_de_producao__mb51.material | 88% | 61 | valores |
| ficha_producao.mangueira | mascara_de_producao__plano.pn | 88% | 61 | valores |
| ficha_producao.mangueira | mb51__sheet1.material | 88% | 61 | valores |
| bd_packing_list__data_base.id | ficha_producao.qtd_turno2_cobertura | 88% | 53 | valores |
| mascara_de_producao__calculo_de_horas_hose.production_supervisor | mascara_de_producao__mb51.material | 88% | 43 | valores |
| mascara_de_producao__calculo_de_horas_hose.production_supervisor | mb51__sheet1.material | 88% | 43 | valores |
| bd_packing_list__data_base.id | ficha_producao.qtd_turno3 | 87% | 54 | valores |
| ficha_producao.mangueira | mascara_de_producao__cadastro_mangueiras.mangueira_hose | 87% | 60 | valores |
| mascara_de_producao__detail1.col_13 | mascara_de_producao__mb51.material_doc_item | 87% | 78 | valores |

## Ligacoes do modelo do BI

Nenhum bloco relationship encontrado nos arquivos .tmdl de GMS/PowerBI.
<!-- AUTO:FIM -->

## Notas do William

Escrito pelo Claude em 01/11/2026, a conferir. Cada nota traz a fonte entre colchetes: [CU] = Refugo/Refugo_por_Material/COMO_USAR_OS_DADOS.md, [BI] = GMS/GMS_Mestre_BI.md, [GL] = GMS/IA/glossario.md, [DG] = GMS/Analises/Higienizacao_GMS/Diagnostico_2026-10-31.md, [obs] = visto nos proprios dados, sem documento.

### Fontes e verdade
- SAP e a verdade absoluta; o GMS e ajustado para bater com o SAP. Variacao = SAP menos GMS: negativa = faltou lancar no SAP; positiva = sobrou no SAP. [CU 3.1]
- "Faltou" e "sobrou" se somam SEPARADOS por material; material nao compensa com material. So compensa dentro do mesmo material. [CU 3.2]
- Os exports sao fotografias: ficha ate 06/10/2026, inspecao e erros ate 02/10, MB51 ate 21/10. Nao afirme "de hoje". [DG 0]
- Metros de mangueira = so unidade M. A MB51 mistura M, PC e KG. [CU 4]

### Tabelas
- ficha_producao: 1 linha por OP (ficha), com o lote em cada etapa; o comprimento cresce ao longo das etapas. Chave: op. Nome da mangueira no GMS: mangueira. Status: status_processo (Finalizado, Aguardando, Em processo, Cancelado). Producao boa do GMS = quantidade_extracao (debandagem nao e teto exato). Colunas quantidade_* e datas vem como TEXTO: numero com virgula de milhar ("1,050") e data "MM/DD/AAAA h:mm AM/PM"; use try_cast(replace(x, ',', '') as double) e try_strptime(x, '%m/%d/%Y %I:%M %p'). Colunas turno_* misturam "3" e "Turno 3". [CU 1, 4; DG 4]
- mb51__sheet1: SAP, 1 linha por item de documento. order = OP; material = codigo; material_description = nome SAP; movement_type 101 = entrada de producao, 102 = estorno (vem com quantidade negativa [obs]); quantity em unit_of_entry (M, PC, KG); user_name; posting_date. Usuarios U445131 e U452021 lancam REFUGO; o SAP nao informa tipo de defeito. [CU 2]
- Producao boa no SAP = soma de quantity (unidade M) sem os dois usuarios de refugo (101 menos 102). Refugo no SAP = so os lancamentos desses dois usuarios. [CU 2]
- mascara_de_producao__mb51: copia da aba MB51 da Mascara de producao (ate 01/10). Mesmo conteudo do mb51__sheet1, so menos recente: use mb51__sheet1. [DG 0]
- registrosinspecao: inspecao boa do GMS, 1 linha por medicao. op_id, quantidade (metros, texto), datahorainspecao (texto), turnoteste, mangueira (13% vazio), cabine_teste (so registros novos). [CU 1; obs]
- tiposerros: refugo do GMS, 1 linha por apontamento. op_id, codigoerro (causa), quantidade (metros), criado (texto), datahorarefugo (texto), turno_erro, trancadeira. Linhas novas (a partir de set/2026) vem sem Id. Ha 84 grupos repetidos (92 linhas a mais) por OP+erro+quantidade+criado. [CU 2; DG 1]
- bd_packing_list__data_base: packing list; a chave e id+slice (um id tem varias fatias); pn = nome da mangueira; qtd_m; cancelled = 1 e cancelado (vazio ou 0 = valido). [DG 1; obs]
- mascara_de_producao__cadastro_mangueiras: cadastro de mangueiras (mangueira_hose, tipo, bitola, wires). [obs]
- Demais abas de mascara_de_producao__* (plano, resumo, resumo_bi, coois, detail1, detalhes1, conferencia, calculo_de_horas_hose, analise_media, mascara_de_producao, power_automate): abas de apoio da planilha de planejamento, em formato de tabela dinamica, sem documento que explique as colunas. Nao use para responder sem conferir. [obs]

### Ligacoes que valem
- A OP liga tudo: ficha_producao.op = mb51__sheet1."order" = registrosinspecao.op_id = tiposerros.op_id. [CU 4]
- Nome de mangueira: o do GMS nao e o da MB51. Nunca descarte uma mangueira por nao achar o nome; ligue o nome do GMS ao material SAP pela OP (a mesma OP nos dois lados). Ex.: GH493-6/8/10/12/16 = "HOSE R12"; GH781-6 = "HOSE-AER, GH781, -6, R2/2SC"; 2583-12 = codigo 12055040; HC101-6 tem descricao "-5" no SAP. [CU 4; DG 9]
- Quando o GMS diz uma mangueira e a OP no SAP e de outra, e divergencia real da OP, nao apelido. [CU 4]
- tiposerros nao tem o nome da mangueira: ligue a ficha pela OP. packing list: pn e o nome da mangueira (ligacao por nome). [obs]
- A lista automatica de ligacoes candidatas (acima) tem muito falso positivo, como id do packing list com bitola ou carretel; ignore as que ligam numeros pequenos sem sentido. [obs]

### Medidas do BI (como o relatorio calcula)
- Metros Produzidos soma a metragem concluida da etapa; sem filtro de etapa conta a mesma mangueira oito vezes. Metros Equivalentes conta a OP uma vez, na etapa final (Finalizacao). [BI K01, K02]
- Metros Refugados = soma da quantidade de refugo. % Refugo = refugo dividido por (bom + refugo), os dois no mesmo recorte de etapa. [BI K10, K11]
- PPM = metros errados / metros de producao boa x 1.000.000. Base de producao = SAP. Material de producao pequena infla o PPM. PPM de refugo e so para uso interno. [CU 3.5, 3.6]
- Meta HH = minutos disponiveis da janela x velocidade da mangueira; Aderencia HH = Real HH / Meta HH. [BI K15]
- Tempo Parado, MTTR e MTBF: MTBF so conta falhas, nao parada programada. OEE e "OEE-lite" enquanto a meta depender de velocidade cadastrada. [BI K17, K18]
- O BI nunca calcula turno: le Turno e Data de Referencia carimbados na camada Prata; o dia produtivo comeca as 05:20. [BI B.5; GL]

### Pegadinhas
- Lance mandado em outra OP e costume da fabrica: aparece como falta numa OP e sobra igual na OP vizinha do mesmo material. [CU 3.3]
- Data do erro = data do lancamento no SAP; sem lancamento no SAP, a data de criacao no GMS. [CU 3.4]
- Parada de julho: sem producao de 04 a 26/07/2026 no SAP e no GMS (provavel ferias, a confirmar). Mes pequeno distorce PPM. [CU 4]
- Meses somados diferem do periodo inteiro: troca de OP que atravessa meses aparece maior nos meses. [CU 4]
- Numero de referencia (16/05 a 16/09/2026): producao boa SAP 596.547 m; faltou 211,6 m + sobrou 369,3 m = 580,9 m; 974 ppm (SAP). [CU 6]
- Em SQL, prefira LEFT JOIN ... IS NULL ou NOT EXISTS para achar OP sem par; "NOT IN (subconsulta)" devolveu 0 com a MB51 deste cache. [obs]

### Triagem das ligacoes candidatas (Claude, 01/11/2026, a conferir)
Feita olhando o nome e os exemplos de cada coluna. O cabecalho das abas detail1 e detalhes1 da Mascara esta na 1a linha: col_3 = Material, col_4 = Order, col_5 = Material Description, col_10 = Material Document, col_11 = Material Doc.Item, col_13 = Qty in unit of entry, col_17 = Quantity, col_18 = User Name.

**Valem (chave real):**
- OP: ficha_producao.op = mb51__sheet1.order = mascara_de_producao__mb51.order = mascara_de_producao__coois.order = registrosinspecao.op_id = tiposerros.op_id = detail1.col_4 = detalhes1.col_4.
- Material SAP: mb51__sheet1.material = mascara_de_producao__mb51.material = coois.material = detail1.col_3 = detalhes1.col_3. Descricao: material_description nas mesmas tabelas = detail1.col_5 = detalhes1.col_5.
- Documento de material: mb51__sheet1.material_document = mascara_de_producao__mb51.material_document = detail1.col_10 = detalhes1.col_10. O item so vale junto do documento (material_document + material_doc_item); sozinho e numero pequeno.
- Usuario SAP: mb51__sheet1.user_name = mascara_de_producao__mb51.user_name = detail1.col_18 = detalhes1.col_18.
- Trancadeira: ficha_producao.trancadeira = registrosinspecao.trancadeira = tiposerros.trancadeira = mascara_de_producao__plano.braider (codigos TH/TM).

**Mesmo atributo, mas nao e chave (serve para filtrar ou agrupar, nao para juntar linha com linha):**
- Bitola: ficha_producao.bitola = cadastro_mangueiras.bitola = plano.dash (dash e a bitola).
- Nome da mangueira: ficha_producao.mangueira, registrosinspecao.mangueira, bd_packing_list.pn, plano.pn, cadastro_mangueiras.mangueira_hose e o material SAP batem de 88% a 98%. Mesmo assim, ligue pela OP (veja Ligacoes que valem). mascara_de_producao__mb51.col_27 esta 100% vazia (9 nomes soltos); nao use.
- Codigos de 3 letras repetidos entre abas: production_supervisor (HAS, FIT, HOS), mrp_controller, storage_location, unit_of_entry, movement_type_text.
- Copias: mascara_de_producao__mb51 x mb51__sheet1 e detail1 x detalhes1 tem o mesmo leiaute. Use mb51__sheet1, que e mais recente.

**Falso positivo (ignore):**
- Toda ligacao com bd_packing_list__data_base.id ou .slice; elas so batem com contagem e metragem.
- Toda ligacao entre colunas de quantidade ou de numero pequeno: bitola x quantidade, concentricidade, carretel_entrada/saida, qtd_turno*, quantidade_*, defeito_*, coois.order_quantity_gmein, material_doc_item, detail1/detalhes1 col_11, col_13 e col_17, registrosinspecao.quantidade/concentricidade.
- ficha_producao.datafinalizacao x tiposerros.datahorarefugo: sao datas do mesmo periodo, nao uma chave. Junte pela OP.
- calculo_de_horas_hose.production_supervisor x material: e uma tabela dinamica (Row Labels, Sum of horas). A coluna tem codigo de material com nome errado; nao use para juntar.
