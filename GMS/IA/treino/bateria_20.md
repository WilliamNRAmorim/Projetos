# Bateria de 20 perguntas com resposta conhecida (IA local do GMS)
# Preparada pelo Claude em 01/11/2026 para a pendencia MEL-258 (testar antes de mostrar a supervisao). Respostas calculadas direto dos arquivos de GMS/IA/dados.
# Fotografias: ficha ate 06/10/2026, inspecao e erros ate 02/10/2026, MB51 ate 21/10/2026. Se os exports mudarem, recalcule (os numeros sao destes arquivos).
# Cada R: tem o numero e o status. VALIDADO = DuckDB mais uma segunda conta (pandas direto do arquivo original ou numero de referencia dos guias). CONFERIR NO BI = ainda sem validacao independente.
# Sem pergunta de turno nem de parada/setup (essas pedem o revisor). Formato igual ao treino_exemplo.md (P:/R:/SQL:), serve para: python gms_ia.py dados --treinar treino/bateria_20.md
# Como corrigir: a IA acerta se o numero dela bate com o R: (tolerancia de arredondamento 0,1). Nome de tabela: o mesmo do gms_mapear (ficha_producao, mb51__sheet1, registrosinspecao, tiposerros).
# Regras: producao boa SAP = MB51 unidade M sem os usuarios de refugo U445131 e U452021 (102 ja vem negativo); a MB51 tem uma linha de total no fim da planilha (sem tipo de movimento) que deve ser ignorada.

P: Quantas fichas existem na ficha_producao e quantas OPs distintas?
R: fichas = 2694, ops_distintas = 2681 (VALIDADO (DuckDB e pandas direto do CSV))
SQL: SELECT count(*) AS fichas, count(DISTINCT op) AS ops_distintas FROM ficha_producao

P: Quantas fichas existem em cada status_processo?
R: Finalizado 2647; Aguardando 29; Em processo 14; Cancelado 4 (VALIDADO (DuckDB e pandas direto do CSV))
SQL: SELECT status_processo, count(*) AS fichas FROM ficha_producao GROUP BY 1 ORDER BY 2 DESC

P: Quais as 5 mangueiras com mais fichas?
R: GH781-12 / 306; GH781-8 / 288; GH781-4 / 179; GH493-12 / 163; GH493-16 / 155 (VALIDADO (DuckDB e pandas; sem empate no corte))
SQL: SELECT mangueira, count(*) AS fichas FROM ficha_producao GROUP BY 1 ORDER BY 2 DESC, 1 LIMIT 5

P: Quantas fichas estao canceladas e em qual etapa (processo) estavam?
R: 4 fichas canceladas, todas na etapa Mandril (VALIDADO (DuckDB e pandas))
SQL: SELECT processo, count(*) AS fichas FROM ficha_producao WHERE status_processo = 'Cancelado' GROUP BY 1

P: Qual o total de producao boa no SAP em metros (MB51, unidade M, sem os usuarios de refugo U445131 e U452021)?
R: metros_bons = 5076443.9 (VALIDADO (DuckDB e pandas direto do mb51.xlsx; a linha de total da planilha foi excluida; = 5.088.378,9 m de unidade M menos 11.935,0 de refugo))
SQL: SELECT round(sum(quantity), 1) AS metros_bons FROM mb51__sheet1 WHERE unit_of_entry = 'M' AND user_name NOT IN ('U445131','U452021')

P: Qual a producao boa do SAP de 16/05/2026 a 16/09/2026?
R: metros_bons = 596547 (596.547 m) (VALIDADO contra a referencia do COMO_USAR_OS_DADOS sec. 6 (596.547 m) e pandas)
SQL: SELECT round(sum(quantity), 1) AS metros_bons FROM mb51__sheet1 WHERE unit_of_entry = 'M' AND user_name NOT IN ('U445131','U452021') AND posting_date BETWEEN '2026-05-16' AND '2026-09-16'

P: Qual a producao boa do SAP em setembro de 2026?
R: metros_bons = 192951.3 (VALIDADO (DuckDB e pandas))
SQL: SELECT round(sum(quantity), 1) AS metros_bons FROM mb51__sheet1 WHERE unit_of_entry = 'M' AND user_name NOT IN ('U445131','U452021') AND posting_date >= '2026-09-01' AND posting_date < '2026-10-01'

P: Quantos estornos (movimento 102) e quantos metros estornados existem na MB51 em 2026?
R: estornos = 394, metros = -57182.1 (negativo) (VALIDADO (DuckDB e pandas))
SQL: SELECT count(*) AS estornos, round(sum(quantity), 1) AS metros FROM mb51__sheet1 WHERE unit_of_entry = 'M' AND movement_type = 102 AND posting_date >= '2026-01-01'

P: Quantos lancamentos e quantos metros de refugo os usuarios U445131 e U452021 lancaram no SAP no total?
R: lancamentos = 2337, metros_refugo = 11935.0 (VALIDADO (DuckDB e pandas))
SQL: SELECT count(*) AS lancamentos, round(sum(quantity), 1) AS metros_refugo FROM mb51__sheet1 WHERE unit_of_entry = 'M' AND user_name IN ('U445131','U452021')

P: Em quantos dias de julho de 2026 houve producao boa no SAP, e quantos deles caem entre 04/07 e 26/07?
R: 8 dias com producao boa em julho (01, 02, 03, 27, 28, 29, 30 e 31); 0 dias entre 04/07 e 26/07 (VALIDADO contra a referencia (sem producao de 04 a 26/07, COMO_USAR_OS_DADOS sec. 4); a causa (ferias) nao esta nos dados)
SQL: SELECT count(DISTINCT CAST(posting_date AS date)) AS dias_com_producao_em_julho, count(DISTINCT CAST(posting_date AS date)) FILTER (WHERE posting_date BETWEEN '2026-07-04' AND '2026-07-26') AS dias_entre_04_e_26 FROM mb51__sheet1 WHERE unit_of_entry = 'M' AND movement_type = 101 AND user_name NOT IN ('U445131','U452021') AND posting_date >= '2026-07-01' AND posting_date < '2026-08-01'

P: Quantos lancamentos e quantos metros a MB51 tem por unidade de medida?
R: M / 63521 / 5088378.9; PC / 47877 / 2926427.0; KG / 1721 / 151569.7 (sem a linha de total da planilha) (VALIDADO (DuckDB e pandas). ARMADILHA: a MB51 traz uma linha de total (material, OP, usuario e tipo de movimento vazios, unidade M, 5.088.378,9) que dobra o M se nao for excluida; sem o filtro movement_type IS NOT NULL a resposta sai M / 63522 / 10176757.8)
SQL: SELECT unit_of_entry, count(*) AS lancamentos, round(sum(quantity), 1) AS quantidade FROM mb51__sheet1 WHERE movement_type IS NOT NULL GROUP BY 1 ORDER BY 2 DESC

P: Qual o total de refugo no GMS (TiposErros) em metros e quantos apontamentos?
R: apontamentos = 5434, metros_refugo = 10028.3 (VALIDADO (DuckDB e pandas direto do CSV). Inclui os 92 apontamentos repetidos (pergunta 14))
SQL: SELECT count(*) AS apontamentos, round(sum(quantidade), 1) AS metros_refugo FROM tiposerros

P: Quais as 3 causas (codigoerro) com mais refugo em metros no GMS?
R: C - Caroço / Ondulação / 1174 apontamentos / 2387.6 m; O - Pontas / 1657 / 2071.4; B - Set Up / Alimentação de Fio / 730 / 1612.8 (VALIDADO (DuckDB e pandas). Inclui repetidos)
SQL: SELECT codigoerro, count(*) AS apontamentos, round(sum(quantidade), 1) AS metros FROM tiposerros GROUP BY 1 ORDER BY 3 DESC LIMIT 3

P: Quantos apontamentos de refugo estao repetidos em TiposErros (mesma OP, erro, quantidade e data de criacao)?
R: grupos_repetidos = 84, linhas_a_mais = 92 (VALIDADO contra a referencia (Diagnostico sec. 1: 84 grupos, 92 linhas a mais))
SQL: SELECT count(*) AS grupos_repetidos, sum(n - 1) AS linhas_a_mais FROM (SELECT count(*) AS n FROM tiposerros GROUP BY op_id, codigoerro, quantidade, criado HAVING count(*) > 1)

P: Quantos metros de inspecao boa existem no total em RegistrosInspecao?
R: metros = 1102915.7 em 16542 registros (VALIDADO (DuckDB e pandas direto do CSV))
SQL: SELECT round(sum(try_cast(replace(quantidade,',','') as double)), 1) AS metros, count(*) AS registros FROM registrosinspecao

P: Mostre a OP 29072011: inspecao boa, refugo no GMS, apontamentos de refugo, entradas 101 e estornos 102 no SAP.
R: inspecao_m = 944.2; refugo_gms_m = 113.2; apontamentos_refugo = 22; sap_101_m = 981.2; entradas_101 = 20; estornos_102 = 1 (981,2 - 37 de estorno = 944,2, bate) (VALIDADO contra a referencia (COMO_USAR_OS_DADOS))
SQL: SELECT (SELECT round(sum(try_cast(replace(quantidade,',','') as double)), 1) FROM registrosinspecao WHERE op_id = 29072011) AS inspecao_m, (SELECT round(sum(quantidade), 1) FROM tiposerros WHERE op_id = 29072011) AS refugo_gms_m, (SELECT count(*) FROM tiposerros WHERE op_id = 29072011) AS apontamentos_refugo, (SELECT round(sum(quantity), 1) FROM mb51__sheet1 WHERE "order" = 29072011 AND movement_type = 101) AS sap_101_m, (SELECT count(*) FROM mb51__sheet1 WHERE "order" = 29072011 AND movement_type = 101) AS entradas_101, (SELECT count(*) FROM mb51__sheet1 WHERE "order" = 29072011 AND movement_type = 102) AS estornos_102

P: Resuma a divergencia de producao boa por OP entre SAP e GMS (so OPs com ultimo lancamento SAP ate 02/10/2026, tolerancia 1 m): quantas OPs dentro de 1 m, quanto faltou e quanto sobrou, separados.
R: ops = 2204, dentro_1m = 1871, ops_faltou = 147, faltou_m = -37862.4, ops_sobrou = 184, sobrou_m = 26831.5 (VALIDADO contra o Diagnostico sec. 9 (1871 / 147 / 37862 / 184 / 26832); total de OPs 2204 aqui contra 2202 la (provavel 2 OPs dentro de 1 m))
SQL: WITH s AS (SELECT "order" AS op, max(posting_date) AS ult, sum(quantity) FILTER (WHERE user_name NOT IN ('U445131','U452021')) AS sap FROM mb51__sheet1 WHERE unit_of_entry = 'M' GROUP BY 1), g AS (SELECT op_id AS op, sum(try_cast(replace(quantidade,',','') as double)) AS gms FROM registrosinspecao GROUP BY 1), j AS (SELECT s.sap - g.gms AS d FROM s JOIN g USING (op) WHERE s.ult <= '2026-10-02') SELECT count(*) AS ops, count(*) FILTER (WHERE abs(d) <= 1) AS dentro_1m, count(*) FILTER (WHERE d < -1) AS ops_faltou, round(sum(d) FILTER (WHERE d < -1), 1) AS faltou_m, count(*) FILTER (WHERE d > 1) AS ops_sobrou, round(sum(d) FILTER (WHERE d > 1), 1) AS sobrou_m FROM j

P: Quais as 3 trancadeiras com mais refugo em metros no GMS?
R: TH07 / 2103.8; TH06 / 2053.9; TH01 / 791.8 (VALIDADO (DuckDB e pandas). Inclui repetidos; refugo registrado sem trancadeira fica de fora)
SQL: SELECT trancadeira, round(sum(quantidade), 1) AS metros FROM tiposerros WHERE trancadeira IS NOT NULL GROUP BY 1 ORDER BY 2 DESC LIMIT 3

P: Qual o % de refugo da mangueira FC735-08 (refugo sobre inspecao boa mais refugo, ligando pela OP)?
R: bom = 13805.4 m, ruim = 293.9 m, pct_refugo = 2.08 % (CONFERIR NO BI: conta bate com a formula do BI (K11), mas sem numero de referencia; comparar com o % Refugo do painel filtrado nessa mangueira)
SQL: WITH i AS (SELECT op_id, sum(try_cast(replace(quantidade,',','') as double)) AS bom FROM registrosinspecao GROUP BY 1), r AS (SELECT op_id, sum(quantidade) AS ruim FROM tiposerros GROUP BY 1) SELECT round(sum(i.bom), 1) AS bom, round(sum(coalesce(r.ruim, 0)), 1) AS ruim, round(100.0 * sum(coalesce(r.ruim, 0)) / (sum(i.bom) + sum(coalesce(r.ruim, 0))), 2) AS pct_refugo FROM ficha_producao f JOIN i ON i.op_id = f.op LEFT JOIN r ON r.op_id = f.op WHERE f.mangueira = 'FC735-08'

P: Qual a inspecao boa total do GMS de 16/05/2026 a 16/09/2026?
R: metros = 500000.9 (CONFERIR NO BI: o guia (COMO_USAR_OS_DADOS) diz 492.691 m para o mesmo periodo; diferenca de 7.310 m, que vem da aba Conf_Geral por OP (nao esta nos exports) e nao foi investigada. A IA deve responder 500.000,9 m e avisar que e a soma de RegistrosInspecao)
SQL: SELECT round(sum(try_cast(replace(quantidade,',','') as double)), 1) AS metros FROM registrosinspecao WHERE try_strptime(datahorainspecao,'%m/%d/%Y %I:%M %p') >= '2026-05-16' AND try_strptime(datahorainspecao,'%m/%d/%Y %I:%M %p') < '2026-09-17'
