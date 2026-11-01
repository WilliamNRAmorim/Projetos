# Backtest do simulador de headcount x demanda (trancagem -> cabine)

Gerado por `backtest_simulador.py` (dados ate 2026-10-06). Headcount **PROVISORIO (operadores distintos que apontaram a etapa no data_ref-turno)**.

## Modelo
- `capacidade_turno = min(pessoas x prod_mediana(etapa,turno) x minutos_turno, teto_p95_turno)`; dia = soma dos 3 turnos, limitada ao teto p95 do dia.
- Cadeia: demanda do dia = metros reais de trancagem do data_ref. `saida(etapa,dia) = min(capacidade_dia, estoque + entrada)`; entrada = saida da etapa anterior (com atraso em dias quando melhora o acerto). Volume da cabine = saida da ultima.
- Turnos pela hora do apontamento final (NORMA 27/10/2026, MEL-250): T1 05:20-13:56 (517 min), T2 13:57-22:19 (503), T3 22:20-05:19 (420); data_ref comeca 05:20.
- Janela: a partir de 2026-03-01 (antes, debandagem/cabine nao tinham apontamento completo). Fichas Canceladas fora.
- Treino: ate 2026-08-12 (98 dias uteis); teste fora da amostra: 42 dias ate 2026-10-06.
- Fator de escala da produtividade (k x mediana), escolhido no treino: **1.2** (candidatos 1.0 a 1.5; k=1 e a mediana pura; k>1 compensa o vies de subestimar dias fortes). Variantes V0-V4 usam esse k.
- Configuracao final (escolhida pelo WAPE de treino da cabine): **V1 + estoque entre etapas**; atraso em dias por etapa: nao usado.

## Fora da amostra (teste, ~30% finais; parametros do treino, mas headcount e demanda de trancagem observados no proprio dia: nao e previsao pura) - modelo final
| Etapa | dias | MAPE diario % | WAPE % | Vies % | MAPE semanal % | dias com erro <=15 % |
|---|---|---|---|---|---|---|
| Trancagem | 42 | 14.6 | 14.6 | 3.4 | 6.5 | 55 |
| Cobertura | 42 | 14.7 | 13.6 | 2.1 | 4.4 | 64 |
| Bandagem | 42 | 20.2 | 19.4 | 2.6 | 9.1 | 45 |
| Vulcanizacao | 42 | 25.4 | 23.5 | 5.4 | 12.3 | 45 |
| Debandagem | 42 | 22.2 | 20.1 | 3.8 | 9.9 | 60 |
| Cabine (extracao) | 42 | 24.2 | 22.5 | 6.6 | 12.5 | 40 |

## Dentro da amostra (treino, ~70% iniciais) - modelo final
| Etapa | dias | MAPE diario % | WAPE % | Vies % | MAPE semanal % | dias com erro <=15 % |
|---|---|---|---|---|---|---|
| Trancagem | 98 | 8.9 | 7.8 | -1.7 | 4.4 | 80 |
| Cobertura | 98 | 16.0 | 14.9 | 1.1 | 7.8 | 60 |
| Bandagem | 98 | 30.8 | 26.4 | 2.8 | 18.5 | 31 |
| Vulcanizacao | 97 | 26.5 | 24.5 | -0.4 | 15.9 | 37 |
| Debandagem | 98 | 26.9 | 23.8 | -2.6 | 14.4 | 40 |
| Cabine (extracao) | 98 | 21.8 | 20.8 | -1.0 | 14.2 | 54 |

## Leave-one-month-out (PARCIALMENTE dentro da amostra: k e atrasos escolhidos com treino que inclui os meses testados)
| Etapa | dias | MAPE diario % | WAPE % | Vies % | MAPE semanal % | dias com erro <=15 % |
|---|---|---|---|---|---|---|
| Trancagem | 140 | 8.6 | 8.4 | -0.5 | 4.2 | 74 |
| Cobertura | 140 | 15.3 | 14.4 | 1.5 | 7.0 | 60 |
| Bandagem | 140 | 29.4 | 25.4 | 3.8 | 18.7 | 31 |
| Vulcanizacao | 139 | 30.5 | 27.8 | -0.1 | 18.4 | 34 |
| Debandagem | 140 | 26.1 | 23.6 | -2.2 | 16.4 | 45 |
| Cabine (extracao) | 140 | 23.4 | 22.5 | -2.6 | 13.7 | 47 |

## Baseline ingenuo (mediana de metros/dia do treino) - fora da amostra
| Etapa | dias | MAPE diario % | WAPE % | Vies % | MAPE semanal % | dias com erro <=15 % |
|---|---|---|---|---|---|---|
| Trancagem | 42 | 18.2 | 17.0 | 3.5 | 8.2 | 48 |
| Cobertura | 42 | 13.9 | 12.3 | 4.6 | 7.6 | 74 |
| Bandagem | 42 | 16.6 | 15.6 | -0.8 | 6.0 | 55 |
| Vulcanizacao | 42 | 18.9 | 16.0 | 4.2 | 7.3 | 57 |
| Debandagem | 42 | 16.2 | 13.5 | 6.7 | 8.1 | 67 |
| Cabine (extracao) | 42 | 17.7 | 14.6 | 11.5 | 12.7 | 55 |

## O que foi ajustado (cabine, MAPE/WAPE %: treino | teste)
| Variante | treino MAPE/WAPE | teste MAPE/WAPE | vies teste % |
|---|---|---|---|
| V0 base (prod. mediana etapa x turno, sem estoque) | 26.8 / 28.7 | 22.1 / 21.8 | -16.5 |
| V1 + estoque entre etapas | 21.8 / 20.8 | 24.2 / 22.5 | 6.6 |
| V2 + mix por bitola | 35.2 / 36.9 | 28.9 / 29.5 | -24.9 |
| V3 + atraso entre etapas | 36.9 / 38.3 | 28.9 / 29.5 | -24.9 |
| V4 estoque + atraso (sem mix) | 23.7 / 22.3 | 24.2 / 22.5 | 6.6 |


Leitura: o estoque entre etapas ajuda no treino (reduz o vies); o mix por bitola PIORA (a produtividade por familia vem de celulas dominadas por uma bitola, poucas e ruidosas, e o headcount provisorio confunde); o atraso em dias nao melhorou o acerto (lead time mediano e de horas, menor que 1 dia). O modelo calibrado NAO bate o baseline ingenuo (mediana do dia) na maioria das etapas: com o headcount provisorio, a capacidade pessoas x produtividade nao explica o volume diario melhor que a mediana.

## 10 dias que mais erraram na cabine (maior erro absoluto em metros; motivo = heuristica a partir dos dados)
| data_ref | periodo | real m | previsto m | erro % | motivo provavel |
|---|---|---|---|---|---|
| 2026-05-23 | treino | 8591 | 2418 | -72 | mix de bitola (fator 0.84) |
| 2026-08-03 | treino | 11887 | 6409 | -46 | estoque acumulado na entrada da cabine |
| 2026-05-20 | treino | 7889 | 2418 | -69 | lote/hora de apontamento da cabine desacoplado da trancagem do dia (lead time), sem causa unica nos dados |
| 2026-05-22 | treino | 7844 | 2418 | -69 | lote/hora de apontamento da cabine desacoplado da trancagem do dia (lead time), sem causa unica nos dados |
| 2026-05-25 | treino | 8010 | 3276 | -59 | mix de bitola (fator 1.21) |
| 2026-05-19 | treino | 7019 | 2418 | -66 | mix de bitola (fator 0.82) |
| 2026-07-02 | treino | 3552 | 7542 | 112 | estoque acumulado na entrada da cabine |
| 2026-03-09 | treino | 8566 | 4677 | -45 | estoque acumulado na entrada da cabine |
| 2026-05-29 | treino | 7843 | 4350 | -45 | mix de bitola (fator 0.72) |
| 2026-06-19 | treino | 5009 | 8333 | 66 | estoque acumulado na entrada da cabine; mix de bitola (fator 0.69) |


## Teste da conta inversa (pessoas necessarias vs capacidade direta)
`pessoas_necessarias(demanda, etapa, turno, params)` = ceil(demanda_turno / (prod_mediana x k x minutos)). Isto e VERIFICACAO ARITMETICA (verdadeira por construcao), nao validacao do modelo. Para cada celula etapa x turno x dia valido (1927 celulas), rodou-se a capacidade direta com essas pessoas: capacidade >= demanda em **1927/1927** celulas (sem teto) e, com o teto de maquina, capacidade >= min(demanda, teto) em **1927/1927**. Demandas acima do teto p95 do turno sao inviaveis pelo teto empirico mesmo com mais gente (o modelo sinaliza gargalo de maquina).

## Dias excluidos (janela a partir de 01/03/2026)
- volume < 30% da mediana (tranc ou cabine): 19 dias: 2026-03-01, 2026-03-06, 2026-03-08, 2026-03-13, 2026-03-14, 2026-03-18, 2026-04-12, 2026-04-26, 2026-05-09, 2026-05-10, 2026-05-11, 2026-05-24, 2026-06-14, 2026-06-28, 2026-07-28, 2026-09-13, 2026-09-27, 2026-10-04, 2026-10-06
- sem producao (folga/fim de semana): 34 dias (nao listados).
- domingo de baixo volume: 2 dias: 2026-03-15, 2026-03-29
- parada (2026-07-03 a 2026-07-27, 25 dias): 25 dias: 2026-07-03, 2026-07-04, 2026-07-05, 2026-07-06, 2026-07-07, 2026-07-08, 2026-07-09, 2026-07-10, 2026-07-11, 2026-07-12, 2026-07-13, 2026-07-14, 2026-07-15, 2026-07-16, 2026-07-17, 2026-07-18, 2026-07-19, 2026-07-20, 2026-07-21, 2026-07-22, 2026-07-23, 2026-07-24, 2026-07-25, 2026-07-26, 2026-07-27
- Antes de 01/03/2026: excluido por falta de apontamento completo de debandagem/cabine (inclui a parada de dez/2025-jan/2026).

## Meta (erro diario <= 10-15%) e o que falta
- Cabine fora da amostra: MAPE 24.2%, WAPE 22.5%, 40% dos dias com erro <= 15%. **Meta NAO atingida** no diario.
- Limitacoes sem maquiagem: (1) headcount provisorio = quem apontou, nao quem estava escalado (pessoas que apontam por colega, ou escalados que nao apontam, distorcem pessoa x minuto e criam circularidade: mais fichas => mais operadores distintos); (2) a demanda usada e a trancagem realizada, nao a demanda real do cliente; (3) o apontamento e em lotes/ fichas fechadas por hora, entao a producao do dia na cabine depende de quando a ficha e fechada, nao so da capacidade; (4) sem horas extras, paradas de maquina e setups por dia no modelo.
- Proximo passo para fechar a meta: `escala_real.csv` (data_ref,turno,etapa,pessoas) com a escala real de alguns meses, e a demanda real; basta soltar o arquivo na pasta e rodar `calibrar_simulador.py` e `backtest_simulador.py`.


## Ressalvas da revisao (Opus)
- Fora da amostra o estoque entre etapas nao melhora o erro diario da cabine; so ajuda no treino.
- A trancagem 'ganha' do baseline em parte porque a demanda e a propria trancagem real do dia e o headcount e o de quem apontou no dia: nao e previsao pura.
- Produtividade vem de fichas com operador; o real inclui fichas sem operador. Celulas com metros e sem operador ficam com capacidade 0 e o k pode compensar erro de dado.
- parametros_simulador.csv e calibrado com todos os dias (inclui o teste); o k foi escolhido sobre parametros so de treino.
- Produtividade (m/pessoa*min) NAO e a Meta HH do BI (velocidade x minutos); nao chamar de meta.
- Pendente do William: hora extra do T2 (ate 23:20) cai no T3 pela fronteira 22:20 da NORMA; confirmar se serve ou se a escala real separa.