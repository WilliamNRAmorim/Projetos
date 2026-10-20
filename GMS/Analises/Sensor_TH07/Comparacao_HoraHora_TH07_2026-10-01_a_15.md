# TH07 — GMS x Factbird, hora a hora, 01 a 15/10/2026

**Fonte GMS:** export Hora-Hora (`Tempo Parado (min)` por hora). **Fonte Factbird:** lista de paradas (Register Stops) da linha TH07, horário de Brasília, paradas com 1 min ou mais (tira o ruído de 5 s). Dias incluídos: todos os com TH07 apontada de 01 a 15/10, inclusive turno em Rascunho. Linhas duplicadas no GMS (16) foram descartadas. Detalhe por hora: `Comparacao_HoraHora_TH07_2026-10-01_a_15.csv`.

Dif. = Factbird − GMS. 'Bate' = diferença de até 5 min na hora.

## Resumo

- 251 horas comparadas em 11 dias; **121 (48%) batem** na hora, 91 em que o sensor viu mais parada e 39 em que o GMS apontou mais.
- **1º e 2º turnos (Finalizados): o total do turno fecha**, mas a distribuição por hora não. 1º: GMS 2000 min x sensor 1906. 2º: GMS 2026 x sensor 2151. Só 34 de 83 horas batem no 1º e 61 de 99 no 2º.
- **3º turno: o GMS nunca tem parada apontada.** Nas 56 horas dos 3º turnos do período o `Tempo Parado` é 0 em todas e o status é Rascunho, enquanto o sensor viu 979 min parados.
- **Horas com GMS = 0 parado (153):** em 60 delas (39%) o sensor viu 10 min ou mais de parada. Média do sensor nessas horas: 12,4 min. É parada curta que o operador não digita.
- **Parada longa apontada bate com o sensor.** Das 43 horas com 45 min ou mais de parada no GMS, em 34 (79%) o sensor viu 40 min ou mais.
- **30 horas têm motivo preenchido e tempo parado 0** (o operador escolheu o motivo, mas deixou o tempo zerado).

## Por turno

| Turno | Status GMS | Horas | Bate | GMS parado (min) | Factbird ≥1 min (min) |
|---|---|---|---|---|---|
| 1º | Finalizado | 83 | 34 | 2000 | 1906 |
| 1º | Rascunho | 13 | 3 | 40 | 267 |
| 2º | Finalizado | 99 | 61 | 2026 | 2151 |
| 3º | Rascunho | 56 | 23 | 0 | 979 |

## Por dia (total apontado x total do sensor)

| Dia | GMS parado (min) | Factbird ≥1 min (min) |
|---|---|---|
| 01/10 | 400 | 716 |
| 02/10 | 317 | 461 |
| 03/10 | 455 | 373 |
| 05/10 | 453 | 576 |
| 06/10 | 392 | 537 |
| 07/10 | 220 | 500 |
| 08/10 | 178 | 288 |
| 09/10 | 402 | 398 |
| 13/10 | 377 | 491 |
| 14/10 | 375 | 355 |
| 15/10 | 497 | 608 |

## Limites

- O sensor da TH07 só mede ligado/desligado: não diz o motivo da parada nem a peça boa.
- A janela 13:47 a 15:00 do 2º turno sobrepõe 10 min com a do 1º; esses minutos aparecem nas duas linhas.
- O corte de 1 min e o limite de 5 min para 'bate' são escolhas da análise.
- Dias com turno aberto (3º em Rascunho) entram porque o William informou que os turnos muitas vezes não são fechados.
