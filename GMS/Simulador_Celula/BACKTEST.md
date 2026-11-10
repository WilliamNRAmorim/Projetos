# Backtest do simulador da célula

Gerado por `python simulador.py`. Não editar à mão.

Fonte do real: planilhas de Eficiência (`Dados_Historicos/Eficiencia_Processo/2026`), 148 dias com produção de 2026-04-01 a 2026-11-04.
Calibração (treino): dias antes de 2026-09-01. Teste: de 2026-09-01 em diante; nenhum parâmetro viu esses dias.
Entradas dadas ao simulador em cada dia: plano da trançagem (máquina, mangueira, velocidade cadastrada) e turnos planejados por etapa. Todo o resto é sorteado.
Simulado = média de 300 réplicas; o estoque entre etapas é o simulado desde o primeiro dia, não o real.

## TESTE (fora da amostra): 2026-09-01 a 2026-11-04, 49 dias

| Etapa | dias | real m/dia | simulado m/dia | MAPE dia % | WAPE % | viés % | MAPE semana % | real dentro de p10–p90 % | WAPE mediana do treino % | WAPE planejado da planilha % |
|---|---|---|---|---|---|---|---|---|---|---|
| mandril | 49 | 7354 | 7200 | 17.8 | 16.4 | -2.1 | 9.8 | 73 | 15.2 | 16.4 |
| tubo | 49 | 6971 | 7154 | 18.2 | 16.1 | +2.6 | 10.2 | 65 | 19.4 | 20.6 |
| trancagem | 49 | 7762 | 7511 | 18.6 | 16.0 | -3.2 | 12.8 | 55 | 14.9 | 23.9 |
| cobertura | 49 | 7112 | 7039 | 17.1 | 15.8 | -1.0 | 9.3 | 71 | 17.8 | 20.3 |
| bandagem | 49 | 6927 | 6951 | 15.8 | 14.4 | +0.3 | 10.7 | 84 | 16.5 | 20.4 |
| vulcanizacao (real = ficha, até 06/10) | 28 | 6311 | 6440 | 21.0 | 15.5 | +2.0 | 9.0 | 93 | 18.3 | nan |
| debandagem | 49 | 7223 | 7357 | 20.2 | 15.1 | +1.9 | 12.2 | 90 | 18.1 | 18.4 |
| **extracao (saída da célula)** | 49 | 6717 | 6931 | 18.8 | 14.8 | +3.2 | 12.3 | 92 | 17.1 | 16.5 |
| SOMA DAS 7 ETAPAS DA PLANILHA | 49 | 50067 | 50143 | 8.8 | 8.4 | +0.2 | 6.7 | 71 | nan | nan |

Cinco dias de teste em que a extração simulada mais errou (m): 2026-10-01 real 2537 x simulado 6840; 2026-10-10 real 2654 x simulado 38; 2026-09-04 real 5006 x simulado 7164; 2026-11-04 real 4325 x simulado 6410; 2026-10-02 real 4892 x simulado 6814.

## TREINO (dentro da amostra): 2026-04-01 a 2026-08-31, 99 dias

| Etapa | dias | real m/dia | simulado m/dia | MAPE dia % | WAPE % | viés % | MAPE semana % | real dentro de p10–p90 % | WAPE mediana do treino % | WAPE planejado da planilha % |
|---|---|---|---|---|---|---|---|---|---|---|
| mandril | 99 | 7347 | 7329 | 17.3 | 16.0 | -0.2 | 10.1 | 75 | 16.6 | 16.1 |
| tubo | 99 | 7281 | 7261 | 29.9 | 14.7 | -0.3 | 12.1 | 75 | 18.4 | 22.4 |
| trancagem | 99 | 7447 | 7649 | 20.4 | 16.1 | +2.7 | 11.7 | 68 | 16.2 | 67.7 |
| cobertura | 99 | 7005 | 6854 | 31.1 | 16.2 | -2.1 | 12.2 | 74 | 18.0 | 22.2 |
| bandagem | 99 | 6913 | 6796 | 18.3 | 17.0 | -1.7 | 12.4 | 75 | 17.7 | 23.8 |
| vulcanizacao (real = ficha, até 06/10) | 99 | 6371 | 6285 | 28.2 | 22.2 | -1.4 | 15.8 | 75 | 23.9 | nan |
| debandagem | 99 | 7294 | 7215 | 20.2 | 18.4 | -1.1 | 15.5 | 83 | 19.2 | 23.2 |
| **extracao (saída da célula)** | 99 | 6877 | 6837 | 17.8 | 16.4 | -0.6 | 14.4 | 88 | 16.4 | 12.8 |
| SOMA DAS 7 ETAPAS DA PLANILHA | 99 | 50163 | 49941 | 12.5 | 11.0 | -0.4 | 10.4 | 67 | nan | nan |
