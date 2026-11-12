# Gêmeo digital da célula GMS: backtest (gerado por `gemeo_backtest.py`)

Dados: `ficha_producao.csv` (export de 06/10/2026, 2689 OPs não canceladas). Treino: 01/03 a 12/08/2026 (100 dias válidos). Teste fora da amostra: 13/08 a 05/10/2026 (42 dias). Fora: parada de 03 a 27/07 e dias com volume abaixo de 30% da mediana (mesmo critério do backtest de 01/11).

## Como o gêmeo funciona
- Cada OP entra no Mandril na hora real de liberação e percorre as 8 etapas. Em cada etapa espera na fila, ocupa um servidor (máquina com gente) e sai; a saída vira chegada da próxima.
- Turnos pela NORMA de 27/10/2026 (MEL-250): 1º 05:20–13:57 (517 min), 2º 13:57–22:20 (503), 3º 22:20–05:20 (420); dia produtivo começa 05:20. Lote aberto na virada continua no turno seguinte.
- Tempo de processo = metros ÷ taxa mediana da etapa e da família de bitola (na Trançagem, por máquina e família), vezes um fator `kappa` ajustado no treino. Vulcanização tem ciclo fixo por família.
- Trançagem e Vulcanização rodam em todo turno com a fábrica aberta. As outras etapas só rodam nos turnos em que alguém apontou nelas, com servidores = mín(máquinas, pessoas).
- Refugo e perda entram como rendimento de metros de uma etapa para a seguinte.
- Setup da Trançagem: intervalo mediano entre lotes seguidos na mesma máquina; mesma mangueira 22 min (n = 816), troca de mangueira na mesma bitola 120 min (n = 200), troca de bitola 547 min (n = 84). Medido só quando o lote seguinte já estava pronto no Tubo. É por apontamento (clique), não pela peça boa: provisório.
- Paradas não entram dia a dia (o Hora-Hora da era GMS não está exportado neste PC). Elas estão dentro da taxa efetiva. No Hora-Hora antigo (2023-08-01 a 2026-07-28, 34878 janelas) o parado soma 41% dos minutos das janelas registradas; serve só de referência para o cenário de redução de parada.

## Erro fora da amostra (teste), gêmeo com as pessoas que apontaram no turno
| Etapa | dias | MAPE dia % | WAPE dia % | Viés % | MAPE semana % | dias com erro ≤15 % |
|---|---|---|---|---|---|---|
| Mandril | 42 | 2.5 | 2.5 | -0.1 | 0.2 | 98 |
| Tubo | 42 | 15.6 | 15.8 | -11.8 | 11.7 | 55 |
| Trançagem | 42 | 28.6 | 29.2 | -13.5 | 14.2 | 17 |
| Cobertura | 42 | 17.1 | 17.0 | -9.2 | 10.3 | 57 |
| Bandagem | 42 | 19.7 | 19.2 | -9.8 | 10.3 | 50 |
| Vulcanização | 42 | 18.1 | 18.0 | -8.9 | 10.6 | 48 |
| Debandagem | 42 | 22.3 | 21.6 | -9.5 | 13.6 | 31 |
| Extração/Teste | 42 | 22.0 | 21.9 | -8.3 | 12.5 | 38 |

## Erro fora da amostra, gêmeo com equipe típica (mediana por dia da semana e turno)
| Etapa | dias | MAPE dia % | WAPE dia % | Viés % | MAPE semana % | dias com erro ≤15 % |
|---|---|---|---|---|---|---|
| Mandril | 42 | 3.6 | 3.5 | 0.1 | 0.1 | 95 |
| Tubo | 42 | 16.0 | 16.2 | -12.0 | 12.4 | 52 |
| Trançagem | 42 | 28.0 | 28.5 | -13.7 | 14.5 | 19 |
| Cobertura | 42 | 16.6 | 16.4 | -9.2 | 10.3 | 55 |
| Bandagem | 42 | 18.6 | 18.1 | -10.0 | 9.6 | 57 |
| Vulcanização | 42 | 17.7 | 17.4 | -9.1 | 9.6 | 45 |
| Debandagem | 42 | 21.4 | 20.9 | -9.4 | 13.5 | 43 |
| Extração/Teste | 42 | 21.9 | 21.7 | -8.2 | 12.4 | 43 |

## Comparação 1: "só desloca" (cada OP sai com o atraso mediano, sem fila nem capacidade), teste
| Etapa | dias | MAPE dia % | WAPE dia % | Viés % | MAPE semana % | dias com erro ≤15 % |
|---|---|---|---|---|---|---|
| Mandril | 42 | 3.1 | 3.2 | -0.1 | 0.2 | 98 |
| Tubo | 42 | 14.1 | 14.6 | -11.9 | 12.2 | 62 |
| Trançagem | 42 | 34.2 | 35.5 | -29.7 | 36.5 | 43 |
| Cobertura | 42 | 31.7 | 31.7 | -27.9 | 33.6 | 38 |
| Bandagem | 42 | 34.6 | 34.8 | -30.3 | 33.8 | 29 |
| Vulcanização | 42 | 36.1 | 36.8 | -30.3 | 31.3 | 24 |
| Debandagem | 42 | 37.8 | 38.6 | -33.1 | 28.0 | 38 |
| Extração/Teste | 42 | 37.4 | 37.2 | -32.3 | 27.9 | 40 |

## Comparação 2: mediana de metros por dia do treino, teste
| Etapa | dias | MAPE dia % | WAPE dia % | Viés % | MAPE semana % | dias com erro ≤15 % |
|---|---|---|---|---|---|---|
| Mandril | 42 | 33.0 | 28.0 | 26.3 | 29.0 | 33 |
| Tubo | 42 | 24.3 | 20.2 | 12.4 | 18.1 | 50 |
| Trançagem | 42 | 19.1 | 18.2 | 2.3 | 10.5 | 45 |
| Cobertura | 42 | 14.3 | 12.5 | 5.7 | 8.9 | 74 |
| Bandagem | 42 | 15.6 | 14.3 | 0.6 | 6.3 | 64 |
| Vulcanização | 42 | 19.1 | 15.9 | 5.0 | 6.8 | 62 |
| Debandagem | 42 | 16.3 | 13.3 | 7.6 | 10.0 | 69 |
| Extração/Teste | 42 | 17.1 | 14.1 | 10.5 | 11.0 | 60 |

## Dentro da amostra (treino), gêmeo com as pessoas que apontaram
| Etapa | dias | MAPE dia % | WAPE dia % | Viés % | MAPE semana % | dias com erro ≤15 % |
|---|---|---|---|---|---|---|
| Mandril | 99 | 1.9 | 2.1 | 0.0 | 0.0 | 99 |
| Tubo | 97 | 15.7 | 14.9 | 2.3 | 5.5 | 59 |
| Trançagem | 100 | 23.5 | 21.8 | -0.5 | 6.6 | 45 |
| Cobertura | 100 | 26.3 | 21.8 | 2.7 | 7.1 | 44 |
| Bandagem | 100 | 26.1 | 23.4 | 2.1 | 7.2 | 37 |
| Vulcanização | 98 | 27.0 | 24.1 | -0.2 | 6.8 | 45 |
| Debandagem | 100 | 25.3 | 21.8 | 1.2 | 6.9 | 41 |
| Extração/Teste | 100 | 28.7 | 27.4 | 1.2 | 12.6 | 33 |

## Parâmetros calibrados
| Etapa | servidores | kappa | ocupação % | rendimento vs etapa anterior | espera mínima (min) |
|---|---|---|---|---|---|
| Mandril | 2 | 0.5 | 8 | 1.0 | 0 |
| Tubo | 2 | 1.0 | 40 | 0.8683 | 1 |
| Trançagem | 11 | 1.75 | 51 | 0.9738 | 57 |
| Cobertura | 2 | 1.0 | 24 | 0.9902 | 14 |
| Bandagem | 2 | 1.0 | 21 | 0.9951 | 7 |
| Vulcanização | 5 | 1.0 | 24 | 0.9986 | 1 |
| Debandagem | 2 | 1.0 | 32 | 0.9939 | 91 |
| Extração/Teste | 3 | 1.0 | 55 | 0.9685 | 5 |

Lead time da liberação ao fim da Extração (h), real × gêmeo: mediana 56 × 57; p25 36 × 29; p75 90 × 120.

## Dias em que a Extração mais errou no teste
| data_ref | real (m) | gêmeo (m) | erro (m) |
|---|---|---|---|
| 2026-09-16 | 7022 | 3444 | -3578 |
| 2026-09-30 | 6862 | 3716 | -3146 |
| 2026-09-02 | 6711 | 9762 | +3051 |
| 2026-08-28 | 6580 | 3644 | -2936 |
| 2026-09-29 | 8324 | 5638 | -2686 |
| 2026-10-02 | 4893 | 2418 | -2475 |
