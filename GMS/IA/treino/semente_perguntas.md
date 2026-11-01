# Semente de perguntas da IA do GMS
# Escrito pelo Claude em 01/11/2026, a conferir. Cada SQL foi rodado no DuckDB (cache de GMS/IA/dados, mesmos nomes de tabela do gms_mapear);
# o R: traz o resultado real daquele dia, com os exports ate 06/10 (ficha), 02/10 (inspecao e erros) e 21/10 (MB51).
# Numeros mudam quando os exports mudam: exporte o treino de novo. Formato: P: pergunta, R: resposta, SQL: consulta de referencia.
# Regras usadas: producao boa SAP = MB51 unidade M sem os usuarios de refugo U445131 e U452021 (102 ja vem negativo); refugo SAP = so esses dois usuarios;
# datas e quantidades dos CSVs sao texto (MM/DD/AAAA h:mm AM/PM; virgula de milhar), por isso o try_strptime e o replace.

P: Quantas fichas existem na ficha_producao e quantas OPs distintas?
R: A ficha tem: fichas = 2694, ops_distintas = 2681
SQL: SELECT count(*) AS fichas, count(DISTINCT op) AS ops_distintas FROM ficha_producao

P: Quantas fichas existem em cada status_processo?
R: Fichas por status: Finalizado / 2647; Aguardando / 29; Em processo / 14; Cancelado / 4 (colunas: status_processo / fichas)
SQL: SELECT status_processo, count(*) AS fichas FROM ficha_producao GROUP BY 1 ORDER BY 2 DESC

P: Quais as 10 mangueiras com mais fichas?
R: Top 10 mangueiras por fichas: GH781-12 / 306; GH781-8 / 288; GH781-4 / 179; GH493-12 / 163; GH493-16 / 155; GH781-6 / 149; GH781-16 / 145; GH781-10 / 121; EC215-08L / 120; EC215-06L / 55 (colunas: mangueira / fichas)
SQL: SELECT mangueira, count(*) AS fichas FROM ficha_producao GROUP BY 1 ORDER BY 2 DESC LIMIT 10

P: Quantas fichas foram criadas em cada mes?
R: Fichas criadas por mes: 2025-11 / 1; 2025-12 / 21; 2026-01 / 293; 2026-02 / 295; 2026-03 / 350; 2026-04 / 287; 2026-05 / 330; 2026-06 / 323; 2026-07 / 78; 2026-08 / 318; 2026-09 / 333; 2026-10 / 65 (colunas: mes / fichas)
SQL: SELECT strftime(try_strptime(created,'%m/%d/%Y %I:%M %p'), '%Y-%m') AS mes, count(*) AS fichas FROM ficha_producao GROUP BY 1 ORDER BY 1

P: Quantos metros saíram da extracao/teste (quantidade_extracao) em cada mes do fim da extracao?
R: Metros da extracao por mes: 2026-01 / 17033.8; 2026-02 / 98618.7; 2026-03 / 158419.5; 2026-04 / 145669.7; 2026-05 / 147361.9; 2026-06 / 152862.3; 2026-07 / 30775.5; 2026-08 / 148036.1; 2026-09 / 151310.8; 2026-10 / 22603.7 (colunas: mes / metros)
SQL: SELECT strftime(try_strptime(data_hora_final_extracao,'%m/%d/%Y %I:%M %p'), '%Y-%m') AS mes, round(sum(try_cast(replace(quantidade_extracao,',','') as double)), 1) AS metros FROM ficha_producao WHERE try_strptime(data_hora_final_extracao,'%m/%d/%Y %I:%M %p') IS NOT NULL AND try_cast(replace(quantidade_extracao,',','') as double) IS NOT NULL GROUP BY 1 ORDER BY 1

P: Quais as 10 mangueiras com mais metros na debandagem?
R: Top 10 mangueiras por metros na debandagem (fichas finalizadas): GH781-8 / 142328; GH781-4 / 140893; GH781-12 / 115074; GH781-6 / 96210; EC215-08L / 59281; GH781-10 / 49225; GH493-12 / 49206; GH493-16 / 38716; EC215-06L / 36238; HC139-7 / 33067 (colunas: mangueira / metros)
SQL: SELECT mangueira, round(sum(try_cast(replace(quantidade_debandagem,',','') as double)), 1) AS metros FROM ficha_producao WHERE status_processo = 'Finalizado' GROUP BY 1 ORDER BY 2 DESC LIMIT 10

P: Quantos metros cada trancadeira trancou (quantidade_trancagem)?
R: Top 10 trancadeiras por metros trancados: TH07 / 394678; TH06 / 213979; TH01 / 157543; Spiral / 114619; TM01 / 113361; TH03 / 89021.6; TM04 / 74923.5; TH02 / 70540; TH05 / 65720; TO04 / 59544 (colunas: trancadeira / metros)
SQL: SELECT trancadeira, round(sum(try_cast(replace(quantidade_trancagem,',','') as double)), 1) AS metros FROM ficha_producao WHERE trancadeira IS NOT NULL GROUP BY 1 ORDER BY 2 DESC LIMIT 10

P: Quantas fichas por turno na trancagem?
R: Fichas por turno da trancagem (o campo mistura '3' e 'Turno 3'): 1 / 918; 2 / 1030; 3 / 716 (colunas: turno / fichas)
SQL: SELECT regexp_extract(turno_trancagem, '[0-9]') AS turno, count(*) AS fichas FROM ficha_producao WHERE turno_trancagem IS NOT NULL GROUP BY 1 ORDER BY 1

P: Quantas fichas foram finalizadas por turno na extracao/teste?
R: Fichas finalizadas por turno da extracao/teste: 1 / 301; 2 / 420; 3 / 56 (colunas: turno / fichas)
SQL: SELECT turno_extr_teste AS turno, count(*) AS fichas FROM ficha_producao WHERE status_processo = 'Finalizado' AND turno_extr_teste IS NOT NULL GROUP BY 1 ORDER BY 1

P: Qual a mediana de dias entre a criacao da ficha e o fim da extracao, por mes de criacao?
R: Mediana de dias da criacao ao fim da extracao: 2025-11 / 1 / 272.31; 2025-12 / 21 / 4.76; 2026-01 / 150 / 2.13; 2026-02 / 204 / 1.54; 2026-03 / 310 / 1.84; 2026-04 / 287 / 2.31; 2026-05 / 308 / 2.27; 2026-06 / 322 / 2.79; 2026-07 / 78 / 2.77; 2026-08 / 318 / 1.94; 2026-09 / 324 / 3.4; 2026-10 / 27 / 2.37 (colunas: mes / fichas / dias_mediana)
SQL: SELECT strftime(try_strptime(created,'%m/%d/%Y %I:%M %p'), '%Y-%m') AS mes, count(*) AS fichas, round(median(date_diff('minute', try_strptime(created,'%m/%d/%Y %I:%M %p'), try_strptime(data_hora_final_extracao,'%m/%d/%Y %I:%M %p'))) / 1440.0, 2) AS dias_mediana FROM ficha_producao WHERE status_processo = 'Finalizado' AND try_strptime(data_hora_final_extracao,'%m/%d/%Y %I:%M %p') >= try_strptime(created,'%m/%d/%Y %I:%M %p') GROUP BY 1 ORDER BY 1

P: Quantas fichas estao canceladas e em qual etapa estavam?
R: Fichas canceladas por etapa: processo = Mandril, fichas = 4
SQL: SELECT processo, count(*) AS fichas FROM ficha_producao WHERE status_processo = 'Cancelado' GROUP BY 1

P: Qual o total de producao boa no SAP em metros (MB51, unidade M, 101 menos 102, sem os usuarios de refugo)?
R: Producao boa no SAP em todo o arquivo: metros_bons = 5076443.9
SQL: SELECT round(sum(quantity), 1) AS metros_bons FROM mb51__sheet1 WHERE unit_of_entry = 'M' AND user_name NOT IN ('U445131','U452021')

P: Qual a producao boa do SAP de 16/05/2026 a 16/09/2026?
R: Producao boa SAP de 16/05 a 16/09/2026: metros_bons = 596547 (bate com a referencia: 596.547 m, COMO_USAR_OS_DADOS sec. 6)
SQL: SELECT round(sum(quantity), 1) AS metros_bons FROM mb51__sheet1 WHERE unit_of_entry = 'M' AND user_name NOT IN ('U445131','U452021') AND posting_date BETWEEN '2026-05-16' AND '2026-09-16'

P: Qual a producao boa do SAP por mes em 2026?
R: Producao boa SAP por mes em 2026: 2026-01 / 812031.7; 2026-02 / 296767.6; 2026-03 / 236222; 2026-04 / 173814.9; 2026-05 / 200208.3; 2026-06 / 185326.1; 2026-07 / 39251.7; 2026-08 / 171614.5; 2026-09 / 192951.3; 2026-10 / 123370.3 (colunas: mes / metros_bons)
SQL: SELECT strftime(posting_date, '%Y-%m') AS mes, round(sum(quantity), 1) AS metros_bons FROM mb51__sheet1 WHERE unit_of_entry = 'M' AND user_name NOT IN ('U445131','U452021') AND posting_date >= '2026-01-01' GROUP BY 1 ORDER BY 1

P: Quais os 10 materiais com mais producao boa no SAP?
R: Top 10 materiais por producao boa no SAP: HOSE-AER, GH781, -8, R2/2SC / 479190; HOSE-AER, GH781, -4, R2/2SC / 379427.7; HOSE-AER, GH781, -12, R2/2SC / 329110.8; HOSE-AER, GH781, -6, R2/2SC / 322106.2; HOSE R12 / 271665.5; MANDREL- 0248 / 193678.8; MANDREL- 0365 / 161131.7; HOSE-AER, GH781, -10, R2/2SC / 158445.5; FABRIC 66.6MM(24sq.in) F00051 REV0 / 149826.1; HOSE-WIN, EC215, -8L, R2/2SC / 146048.4 (colunas: material_description / metros_bons)
SQL: SELECT material_description, round(sum(quantity), 1) AS metros_bons FROM mb51__sheet1 WHERE unit_of_entry = 'M' AND user_name NOT IN ('U445131','U452021') GROUP BY 1 ORDER BY 2 DESC LIMIT 10

P: Quantos metros os usuarios de refugo (U445131 e U452021) lancaram no SAP por mes?
R: Refugo lancado no SAP pelos dois usuarios de refugo, por mes: 2025-10 / 7 / 27.7; 2025-11 / 185 / 459.2; 2025-12 / 74 / 258; 2026-01 / 181 / 618.3; 2026-02 / 194 / 673.8; 2026-03 / 143 / 642.4; 2026-04 / 90 / 469.4; 2026-05 / 188 / 1053.6; 2026-06 / 339 / 1724.1; 2026-07 / 71 / 384.6; 2026-08 / 303 / 1159.2; 2026-09 / 317 / 1923.3 (colunas: mes / lancamentos / metros_refugo)
SQL: SELECT strftime(posting_date, '%Y-%m') AS mes, count(*) AS lancamentos, round(sum(quantity), 1) AS metros_refugo FROM mb51__sheet1 WHERE unit_of_entry = 'M' AND user_name IN ('U445131','U452021') GROUP BY 1 ORDER BY 1

P: Quantos estornos (movimento 102) e quantos metros estornados por mes em 2026?
R: Estornos 102 por mes em 2026: 2026-01 / 137 / -9758.9; 2026-02 / 29 / -20086.2; 2026-03 / 43 / -5700.9; 2026-04 / 27 / -4445.9; 2026-05 / 28 / -2706.6; 2026-06 / 33 / -4085.7; 2026-07 / 7 / -632.2; 2026-08 / 31 / -2438; 2026-09 / 35 / -5089.6; 2026-10 / 24 / -2238.1 (colunas: mes / estornos / metros)
SQL: SELECT strftime(posting_date, '%Y-%m') AS mes, count(*) AS estornos, round(sum(quantity), 1) AS metros FROM mb51__sheet1 WHERE unit_of_entry = 'M' AND movement_type = 102 AND posting_date >= '2026-01-01' GROUP BY 1 ORDER BY 1

P: Em quais dias entre 29/06 e 31/07/2026 houve producao boa no SAP?
R: Dias com producao boa no SAP: 2026-06-29 / 7940.5; 2026-06-30 / 9059.6; 2026-07-01 / 6423.8; 2026-07-02 / 3665.7; 2026-07-03 / 5570.7; 2026-07-27 / 777.9; 2026-07-28 / 460; 2026-07-29 / 3556.1; 2026-07-30 / 9564.9; 2026-07-31 / 9864.8 (colunas: dia / metros_bons) (bate com a referencia: sem producao de 04 a 26/07, COMO_USAR_OS_DADOS sec. 4; so a parada de julho, nao diz se foi ferias)
SQL: SELECT CAST(posting_date AS date) AS dia, round(sum(quantity), 1) AS metros_bons FROM mb51__sheet1 WHERE unit_of_entry = 'M' AND movement_type = 101 AND user_name NOT IN ('U445131','U452021') AND posting_date BETWEEN '2026-06-29' AND '2026-07-31' GROUP BY 1 ORDER BY 1

P: Quantos metros e quantos lancamentos o SAP tem por unidade de medida (M, PC, KG)?
R: MB51 por unidade: M / 63522 / 10176757.8; PC / 47878 / 5852854; KG / 1722 / 303139.4 (colunas: unit_of_entry / lancamentos / quantidade) (nao bate com a referencia: o guia de 07/10 fala em ~6,6 mil linhas em pecas e aqui ha 47878 em PC; sao exports diferentes, este mb51.xlsx e de 24/10 e cobre 11/2024 a 10/2026; nao investigado)
SQL: SELECT unit_of_entry, count(*) AS lancamentos, round(sum(quantity), 1) AS quantidade FROM mb51__sheet1 GROUP BY 1 ORDER BY 2 DESC

P: Qual a producao boa do SAP por semana nas ultimas 8 semanas do arquivo?
R: Producao boa SAP por semana (8 semanas finais do arquivo): 2026-08-24 / 21909.7; 2026-08-31 / 38669.6; 2026-09-07 / 39115.8; 2026-09-14 / 39171.4; 2026-09-21 / 48452.2; 2026-09-28 / 48143.4; 2026-10-05 / 44608.1; 2026-10-12 / 45357.7; 2026-10-19 / 18732.4 (colunas: semana / metros_bons)
SQL: SELECT date_trunc('week', posting_date) AS semana, round(sum(quantity), 1) AS metros_bons FROM mb51__sheet1 WHERE unit_of_entry = 'M' AND user_name NOT IN ('U445131','U452021') AND posting_date > (SELECT max(posting_date) FROM mb51__sheet1) - INTERVAL 56 DAY GROUP BY 1 ORDER BY 1

P: Qual o total de refugo no GMS (TiposErros) em metros e quantos apontamentos?
R: Refugo total do GMS: apontamentos = 5434, metros_refugo = 10028.3
SQL: SELECT count(*) AS apontamentos, round(sum(quantidade), 1) AS metros_refugo FROM tiposerros

P: Quanto refugo o GMS registrou por mes (data de criacao)?
R: Refugo GMS por mes: 2025-11 / 40; 2025-12 / 3; 2026-01 / 0.2; 2026-02 / 685.1; 2026-03 / 1183.4; 2026-04 / 926.6; 2026-05 / 1262.9; 2026-06 / 1416.3; 2026-07 / 372; 2026-08 / 1080; 2026-09 / 2946.4; 2026-10 / 112.4 (colunas: mes / metros_refugo)
SQL: SELECT strftime(try_strptime(criado,'%m/%d/%Y %I:%M %p'), '%Y-%m') AS mes, round(sum(quantidade), 1) AS metros_refugo FROM tiposerros GROUP BY 1 ORDER BY 1

P: Quais os 5 tipos de erro (codigoerro) com mais refugo em metros?
R: Top 5 causas de refugo: C - Caroço / Ondulação / 1174 / 2387.6; O - Pontas / 1657 / 2071.4; B - Set Up / Alimentação de Fio / 730 / 1612.8; A - Quebra de Fio de Aço/Textil / 1074 / 1321.3; E - Trança Aparente / 437 / 1134 (colunas: codigoerro / apontamentos / metros)
SQL: SELECT codigoerro, count(*) AS apontamentos, round(sum(quantidade), 1) AS metros FROM tiposerros GROUP BY 1 ORDER BY 3 DESC LIMIT 5

P: Qual o refugo por trancadeira?
R: Top 10 trancadeiras por refugo: TH07 / 2103.8; TH06 / 2053.9; TH01 / 791.8; Spiral / 575.7; TH03 / 524.1; TO04 / 510.1; TH05 / 500.6; TM01 / 493; TM04 / 399.8; TH02 / 276.8 (colunas: trancadeira / metros)
SQL: SELECT trancadeira, round(sum(quantidade), 1) AS metros FROM tiposerros WHERE trancadeira IS NOT NULL GROUP BY 1 ORDER BY 2 DESC LIMIT 10

P: Qual o refugo por turno (turno_erro)?
R: Refugo por turno: 1 / 976 / 3010.9; 2 / 3092 / 4627.4; 3 / 395 / 571.8 (colunas: turno / apontamentos / metros)
SQL: SELECT turno_erro AS turno, count(*) AS apontamentos, round(sum(quantidade), 1) AS metros FROM tiposerros WHERE turno_erro IS NOT NULL GROUP BY 1 ORDER BY 1

P: Quais as 10 mangueiras com mais refugo no GMS?
R: Top 10 mangueiras por refugo (ligando TiposErros a ficha pela OP): GH781-4 / 1711.2; GH781-12 / 1396.9; GH781-8 / 867.3; GH781-6 / 684.7; GH781-16 / 341.6; GH493-16 / 321.8; HC139-7 / 320.8; EC215-08L / 305.4; EC215-06L / 297; FC735-08 / 293.9 (colunas: mangueira / metros_refugo)
SQL: SELECT f.mangueira, round(sum(t.quantidade), 1) AS metros_refugo FROM tiposerros t JOIN ficha_producao f ON f.op = t.op_id GROUP BY 1 ORDER BY 2 DESC LIMIT 10

P: Qual o % de refugo por mangueira (refugo sobre inspecao boa mais refugo), so mangueiras com mais de 10000 m inspecionados?
R: % refugo por mangueira (mesmo recorte no numerador e no denominador): FC735-08 / 13805.4 / 293.9 / 2.08; FC735-12 / 11638.1 / 181.2 / 1.53; GH781-12 / 99077.9 / 1396.9 / 1.39; HC139-7 / 24423 / 320.8 / 1.3; GH781-4 / 131939.2 / 1711.2 / 1.28; GH781-16 / 26539.9 / 341.6 / 1.27; GH493-16 / 30999.4 / 321.8 / 1.03; EC215-06L / 31057.4 / 297 / 0.95; FC735-10 / 11587.4 / 108.2 / 0.92; GH681-4 / 19356.3 / 172.7 / 0.88 (colunas: mangueira / bom / ruim / pct_refugo) (sem numero de referencia; formula do GMS_Mestre_BI K11, mesmo recorte no numerador e no denominador)
SQL: WITH i AS (SELECT op_id, sum(try_cast(replace(quantidade,',','') as double)) AS bom FROM registrosinspecao GROUP BY 1), r AS (SELECT op_id, sum(quantidade) AS ruim FROM tiposerros GROUP BY 1) SELECT f.mangueira, round(sum(i.bom), 1) AS bom, round(sum(coalesce(r.ruim, 0)), 1) AS ruim, round(100.0 * sum(coalesce(r.ruim, 0)) / (sum(i.bom) + sum(coalesce(r.ruim, 0))), 2) AS pct_refugo FROM ficha_producao f JOIN i ON i.op_id = f.op LEFT JOIN r ON r.op_id = f.op GROUP BY 1 HAVING sum(i.bom) > 10000 ORDER BY 4 DESC LIMIT 10

P: Quantos apontamentos de refugo estao repetidos em TiposErros (mesma OP, erro, quantidade e data de criacao)?
R: Repetidos em TiposErros: grupos_repetidos = 84, linhas_a_mais = 92 (bate com a referencia: 84 grupos e 92 linhas a mais, Diagnostico sec. 1)
SQL: SELECT count(*) AS grupos_repetidos, sum(n - 1) AS linhas_a_mais FROM (SELECT count(*) AS n FROM tiposerros GROUP BY op_id, codigoerro, quantidade, criado HAVING count(*) > 1)

P: Quantos metros de inspecao boa existem por mes (RegistrosInspecao)?
R: Inspecao boa por mes: 2025-11 / 260; 2025-12 / 1502.1; 2026-01 / 20.1; 2026-02 / 132645.9; 2026-03 / 182796.1; 2026-04 / 148592.5; 2026-05 / 148963.8; 2026-06 / 154232.6; 2026-07 / 34721.3; 2026-08 / 142972.2; 2026-09 / 151310.8; 2026-10 / 4898.2 (colunas: mes / metros)
SQL: SELECT strftime(try_strptime(datahorainspecao,'%m/%d/%Y %I:%M %p'), '%Y-%m') AS mes, round(sum(try_cast(replace(quantidade,',','') as double)), 1) AS metros FROM registrosinspecao GROUP BY 1 ORDER BY 1

P: Quantos metros foram inspecionados em cada cabine de teste?
R: Inspecao por cabine (so registros novos tem cabine): CABINE_L1 / 374 / 19644.1; CABINE_L2 / 306 / 17084.6 (colunas: cabine_teste / registros / metros)
SQL: SELECT cabine_teste, count(*) AS registros, round(sum(try_cast(replace(quantidade,',','') as double)), 1) AS metros FROM registrosinspecao WHERE cabine_teste IS NOT NULL GROUP BY 1

P: Quantos metros foram inspecionados por turno de teste?
R: Inspecao por turno: 1 / 402656.8; 2 / 578229; 3 / 120377.7; vazio / 1652.1 (colunas: turno / metros)
SQL: SELECT turnoteste AS turno, round(sum(try_cast(replace(quantidade,',','') as double)), 1) AS metros FROM registrosinspecao GROUP BY 1 ORDER BY 1

P: Quais as 10 mangueiras com mais metros inspecionados?
R: Top 10 mangueiras por metros inspecionados: GH781-4 / 100441.6; GH781-8 / 99194.1; GH781-12 / 87852.5; GH781-6 / 80387.8; EC215-08L / 50782; GH493-12 / 41077.6; GH781-10 / 33901.7; GH493-16 / 29109.1; EC215-06L / 25847.6; GH781-16 / 25319.5 (colunas: mangueira / metros)
SQL: SELECT mangueira, round(sum(try_cast(replace(quantidade,',','') as double)), 1) AS metros FROM registrosinspecao WHERE mangueira IS NOT NULL GROUP BY 1 ORDER BY 2 DESC LIMIT 10

P: Qual a inspecao boa total do GMS de 16/05/2026 a 16/09/2026?
R: Inspecao boa do GMS no periodo: metros = 500000.9 (nao bate com a referencia: o guia diz 492.691 m e esta soma da 500000,9 m, diferenca de 7310 m; a referencia vem da aba Conf_Geral por OP, que nao esta nestes dados; nao investigado)
SQL: SELECT round(sum(try_cast(replace(quantidade,',','') as double)), 1) AS metros FROM registrosinspecao WHERE try_strptime(datahorainspecao,'%m/%d/%Y %I:%M %p') >= '2026-05-16' AND try_strptime(datahorainspecao,'%m/%d/%Y %I:%M %p') < '2026-09-17'

P: Mostre a OP 29072011: producao boa na inspecao, refugo no GMS, apontamentos de refugo, producao boa no SAP e estornos.
R: OP 29072011 (GH781-4): inspecao_m = 944.2, refugo_gms_m = 113.2, apontamentos_refugo = 22, sap_101_m = 981.2, entradas_101 = 20, estornos_102 = 1, lancs_usuario_refugo = 0 (bate com a referencia: 944,2 + 113,2 = 1057,4 m, 22 apontamentos, 20 entradas 101, 1 estorno 102 e nenhum usuario de refugo; 981,2 - 37 de estorno = 944,2 no SAP)
SQL: SELECT (SELECT round(sum(try_cast(replace(quantidade,',','') as double)), 1) FROM registrosinspecao WHERE op_id = 29072011) AS inspecao_m, (SELECT round(sum(quantidade), 1) FROM tiposerros WHERE op_id = 29072011) AS refugo_gms_m, (SELECT count(*) FROM tiposerros WHERE op_id = 29072011) AS apontamentos_refugo, (SELECT round(sum(quantity), 1) FROM mb51__sheet1 WHERE "order" = 29072011 AND movement_type = 101) AS sap_101_m, (SELECT count(*) FROM mb51__sheet1 WHERE "order" = 29072011 AND movement_type = 101) AS entradas_101, (SELECT count(*) FROM mb51__sheet1 WHERE "order" = 29072011 AND movement_type = 102) AS estornos_102, (SELECT count(*) FROM mb51__sheet1 WHERE "order" = 29072011 AND user_name IN ('U445131','U452021')) AS lancs_usuario_refugo

P: Quais as 10 OPs com maior diferenca de producao boa entre o SAP e a inspecao do GMS?
R: OPs com maior variacao (SAP menos GMS; negativa = faltou lancar no SAP): 27312495 / 843.6 / 14764.8 / -13921.2; 27625635 / 438.9 / 3233.4 / -2794.5; 29050557 / 302.6 / 2046.7 / -1744.1; 27312498 / 867.8 / 4.5 / 863.3; 28387301 / 551.5 / 1385.9 / -834.4; 29118867 / 181.1 / 987.2 / -806.1; 26979399 / 823.5 / 80.6 / 742.9; 27670747 / 418.2 / 1087.2 / -669; 26976913 / 0 / 628 / -628; 29115542 / 0 / 627.7 / -627.7 (colunas: op / sap_m / gms_m / variacao) (bate com a referencia: as 5 OPs de maior variacao do Diagnostico sec. 9 - 27312495, 27312498, 27625635, 28387301, 29050557 - estao aqui)
SQL: WITH s AS (SELECT "order" AS op, max(posting_date) AS ult, sum(quantity) FILTER (WHERE user_name NOT IN ('U445131','U452021')) AS sap FROM mb51__sheet1 WHERE unit_of_entry = 'M' GROUP BY 1), g AS (SELECT op_id AS op, sum(try_cast(replace(quantidade,',','') as double)) AS gms FROM registrosinspecao GROUP BY 1) SELECT s.op, round(s.sap, 1) AS sap_m, round(g.gms, 1) AS gms_m, round(s.sap - g.gms, 1) AS variacao FROM s JOIN g USING (op) WHERE s.ult <= '2026-10-02' ORDER BY abs(s.sap - g.gms) DESC LIMIT 10

P: Resuma a divergencia de producao boa GMS x SAP por OP: quantas OPs dentro de 1 m, e quanto faltou e quanto sobrou (separados).
R: Divergencia de producao boa por OP (so OPs nos dois lados, ultimo lancamento SAP ate 02/10/2026, tolerancia 1 m): ops = 2204, dentro_1m = 1871, ops_faltou = 147, faltou_m = -37862.4, ops_sobrou = 184, sobrou_m = 26831.5 (bate com a referencia, Diagnostico sec. 9: 1871 dentro de 1 m, faltou 147 OPs e 37862 m, sobrou 184 OPs e 26832 m; so o total de OPs difere, 2204 aqui e 2202 la, provavelmente 2 OPs dentro de 1 m)
SQL: WITH s AS (SELECT "order" AS op, max(posting_date) AS ult, sum(quantity) FILTER (WHERE user_name NOT IN ('U445131','U452021')) AS sap FROM mb51__sheet1 WHERE unit_of_entry = 'M' GROUP BY 1), g AS (SELECT op_id AS op, sum(try_cast(replace(quantidade,',','') as double)) AS gms FROM registrosinspecao GROUP BY 1), j AS (SELECT s.sap - g.gms AS d FROM s JOIN g USING (op) WHERE s.ult <= '2026-10-02') SELECT count(*) AS ops, count(*) FILTER (WHERE abs(d) <= 1) AS dentro_1m, count(*) FILTER (WHERE d < -1) AS ops_faltou, round(sum(d) FILTER (WHERE d < -1), 1) AS faltou_m, count(*) FILTER (WHERE d > 1) AS ops_sobrou, round(sum(d) FILTER (WHERE d > 1), 1) AS sobrou_m FROM j

P: Resuma a divergencia de refugo GMS x SAP por OP: quantas OPs dentro de 1 m, e quanto faltou e quanto sobrou (separados).
R: Divergencia de refugo por OP (so OPs com lancamento de refugo no SAP, ultimo lancamento ate 02/10/2026): ops = 1421, dentro_1m = 1255, ops_faltou = 46, faltou_m = -558.4, ops_sobrou = 120, sobrou_m = 724.1 (bate com a referencia, Diagnostico sec. 9: 1421 OPs, 1255 dentro de 1 m, faltou 46 OPs e 558 m, sobrou 120 OPs e 724 m)
SQL: WITH s AS (SELECT "order" AS op, max(posting_date) AS ult, sum(quantity) FILTER (WHERE user_name IN ('U445131','U452021')) AS sap, count(*) FILTER (WHERE user_name IN ('U445131','U452021')) AS n FROM mb51__sheet1 WHERE unit_of_entry = 'M' GROUP BY 1), g AS (SELECT op_id AS op, sum(quantidade) AS gms FROM tiposerros GROUP BY 1), j AS (SELECT s.sap - g.gms AS d FROM s JOIN g USING (op) WHERE s.ult <= '2026-10-02' AND s.n > 0) SELECT count(*) AS ops, count(*) FILTER (WHERE abs(d) <= 1) AS dentro_1m, count(*) FILTER (WHERE d < -1) AS ops_faltou, round(sum(d) FILTER (WHERE d < -1), 1) AS faltou_m, count(*) FILTER (WHERE d > 1) AS ops_sobrou, round(sum(d) FILTER (WHERE d > 1), 1) AS sobrou_m FROM j

P: Quais materiais tiveram mais refugo lancado no SAP pelos usuarios de refugo?
R: Top 10 materiais por refugo lancado no SAP: HOSE-AER, GH781, -4, R2/2SC / 187 / 2466.7; HOSE-AER, GH781, -8, R2/2SC / 296 / 1259.9; HOSE R12 / 310 / 1029.1; HOSE-AER, GH781, -6, R2/2SC / 159 / 918.1; HOSE-AER, GH781, -12, R2/2SC / 222 / 680.2; HOSE-WIN, EC215, -6L, R2/2SC / 57 / 468.9; HOSE-AER, HC139, -7, J1402 / 68 / 436.5; HOSE-WIN, EC215, -8L, R2/2SC / 116 / 395.1; HOSE-AER, GH781, -10, R2/2SC / 93 / 391.3; HOSE-AER, GH781, -16, R2/2SC / 108 / 381.2 (colunas: material_description / lancamentos / metros_refugo)
SQL: SELECT material_description, count(*) AS lancamentos, round(sum(quantity), 1) AS metros_refugo FROM mb51__sheet1 WHERE unit_of_entry = 'M' AND user_name IN ('U445131','U452021') GROUP BY 1 ORDER BY 3 DESC LIMIT 10

P: Quais mangueiras do GMS tem nome diferente do material da mesma OP no SAP (ligacao pela OP)?
R: Pares GMS para SAP que mais se repetem (descricao nao contem o nome do GMS): GH493-12 / HOSE R12 / 162; GH493-16 / HOSE R12 / 153; EC215-08L / HOSE-WIN, EC215, -8L, R2/2SC / 114; EC215-06L / HOSE-WIN, EC215, -6L, R2/2SC / 55; GH493-8 / HOSE R12 / 40; EC118-08L / HOSE-WIN, EC118, -8L, R17 / 39; EC118-04L / HOSE-WIN, EC118, -4L, R17 / 35; HC139-7_S-GX / HOSE-AER, HC139, -7, J1402 / 33; EC118-06L / HOSE-WIN, EC118, -6L, R17 / 33; FC735-08 / HOSE-AER, FC735, -8, R2/2SC / 29 (colunas: nome_gms / nome_sap / ops) (bate com a referencia: GH493-12 e GH493-16 para HOSE R12 com 162 e 153, Diagnostico sec. 9)
SQL: SELECT f.mangueira AS nome_gms, m.material_description AS nome_sap, count(DISTINCT f.op) AS ops FROM ficha_producao f JOIN mb51__sheet1 m ON m."order" = f.op WHERE m.unit_of_entry = 'M' AND f.mangueira IS NOT NULL AND regexp_replace(upper(m.material_description), '[^A-Z0-9]', '', 'g') NOT LIKE '%' || regexp_replace(upper(f.mangueira), '[^A-Z0-9]', '', 'g') || '%' GROUP BY 1, 2 ORDER BY 3 DESC LIMIT 10

P: Quantas OPs da ficha nao tem nenhum lancamento na MB51 (sem contar canceladas e criadas depois de 06/10/2026)?
R: OPs da ficha sem ordem na MB51: ops_avaliadas = 2680, sem_mb51 = 32 (bate com a referencia: 2680 OPs avaliadas e 32 sem MB51, Diagnostico sec. 6; usei LEFT JOIN porque NOT IN deu 0 neste cache)
SQL: SELECT count(*) AS ops_avaliadas, count(*) FILTER (WHERE m.o IS NULL) AS sem_mb51 FROM ficha_producao f LEFT JOIN (SELECT DISTINCT "order" AS o FROM mb51__sheet1) m ON m.o = f.op WHERE f.status_processo <> 'Cancelado' AND f.op IS NOT NULL AND try_strptime(f.created,'%m/%d/%Y %I:%M %p') <= '2026-10-06'

P: Quais OPs com refugo no GMS nao tem nenhum lancamento de refugo no SAP, e quantos metros?
R: OPs com refugo so no GMS (maiores): 29072011 / 113.2; 28604071 / 72; 28170484 / 68; 29422610 / 63.2; 30063849 / 62.5; 28375504 / 62.4; 27627412 / 59.2; 28879984 / 45.6; 28236148 / 30.6; 28802487 / 30 (colunas: op_id / refugo_gms_m) (bate com a referencia: a OP 29072011 tem 113,2 m no GMS e nada de refugo no SAP, COMO_USAR_OS_DADOS sec. 6)
SQL: SELECT t.op_id, round(sum(t.quantidade), 1) AS refugo_gms_m FROM tiposerros t WHERE NOT EXISTS (SELECT 1 FROM mb51__sheet1 m WHERE m."order" = t.op_id AND m.user_name IN ('U445131','U452021')) GROUP BY 1 ORDER BY 2 DESC LIMIT 10

P: Quantos metros de packing list por mangueira (pn), sem contar cancelados?
R: Top 10 pn por metros no packing list: GH781-8 / 57725.3; GH781-4 / 55806.6; GH781-12 / 42718.3; GH781-6 / 40785.4; EC215-08L / 31993; GH493-12 / 26796.4; GH781-10 / 21199.1; GH781-16 / 19314.4; GH493-16 / 19148.4; EC215-06L / 16075.4 (colunas: pn / metros)
SQL: SELECT pn, round(sum(qtd_m), 1) AS metros FROM bd_packing_list__data_base WHERE cancelled IS NULL OR cancelled = 0 GROUP BY 1 ORDER BY 2 DESC LIMIT 10

P: Quantos registros do packing list foram cancelados e quantos IDs distintos existem?
R: Packing list: cancelados = 446, linhas = 9965, ids_distintos = 1496
SQL: SELECT count(*) FILTER (WHERE cancelled = 1) AS cancelados, count(*) AS linhas, count(DISTINCT id) AS ids_distintos FROM bd_packing_list__data_base

P: Quantos IDs de packing list foram criados por mes?
R: IDs de packing list por mes: 2026-05 / 391; 2026-06 / 338; 2026-07 / 86; 2026-08 / 337; 2026-09 / 338; 2026-10 / 5 (colunas: mes / ids)
SQL: SELECT strftime(try_strptime("timestamp", '%Y-%m-%d %H:%M:%S'), '%Y-%m') AS mes, count(DISTINCT id) AS ids FROM bd_packing_list__data_base WHERE try_strptime("timestamp", '%Y-%m-%d %H:%M:%S') IS NOT NULL GROUP BY 1 ORDER BY 1

P: Quantas mangueiras ha no cadastro da Mascara de producao por tipo?
R: Cadastro de mangueiras por tipo: 2A / 34; 1A / 28; 1T / 17; 4A / 15 (colunas: tipo / mangueiras)
SQL: SELECT tipo, count(*) AS mangueiras FROM mascara_de_producao__cadastro_mangueiras GROUP BY 1 ORDER BY 2 DESC

P: Quais mangueiras da ficha nao estao no cadastro da Mascara de producao?
R: Mangueiras da ficha sem cadastro (maiores): vazio / 9; GH781-6-2 / 4; 2583-12 / 4; 0 / 3; EC415-12 / 1; EC215-04 / 1; EC215-06L-2 / 1; EC118-4L / 1; GH781-08 / 1; 1 / 1 (colunas: mangueira / fichas)
SQL: SELECT f.mangueira, count(*) AS fichas FROM ficha_producao f LEFT JOIN mascara_de_producao__cadastro_mangueiras c ON upper(c.mangueira_hose) = upper(f.mangueira) WHERE c.mangueira_hose IS NULL GROUP BY 1 ORDER BY 2 DESC LIMIT 10
