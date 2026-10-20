# TH07 — GMS x Factbird, 15/10/2026 (05:20 a 05:20)

Fonte GMS: export Hora-Hora (até 15/10). Fonte Factbird: lista de paradas (Register Stops), horário de Brasília. Minutos de parada por janela do GMS.

- **Factbird total**: soma de todas as paradas do sensor, inclusive as de 5 s.
- **Factbird ≥1 min**: só paradas com 1 min ou mais (tira o ruído de 5 s).
- **Dif.** = Factbird ≥1 min − GMS. Positivo: sensor viu mais parada que o operador apontou.

| Turno | Hora | GMS parado | FB total | FB ≥1 min | Dif. | Real GMS | Motivo GMS | Leitura |
|---|---|---|---|---|---|---|---|---|
| 1º | 05:20-06:00 | 30 | 7.5 | 6.8 | -23.2 | 15 | Reunião | diverge muito |
| 1º | 06:00-07:00 | 0 | 15.8 | 11.6 | +11.6 | 150 |  | diverge |
| 1º | 07:00-08:00 | 0 | 1.8 | 0.0 | +0.0 | 150 |  | bate |
| 1º | 08:00-09:00 | 0 | 16.2 | 13.1 | +13.1 | 150 |  | diverge |
| 1º | 09:00-10:00 | 10 | 8.1 | 4.0 | -6.0 | 132 | Resto de fio | diverge |
| 1º | 10:00-11:00 | 60 | 54.8 | 54.8 | -5.2 | 0 | Resto de fio | diverge |
| 1º | 11:00-12:00 | 60 | 60.0 | 60.0 | +0.0 | 0 | Resto de fio | bate |
| 1º | 12:00-13:00 | 60 | 59.3 | 59.3 | -0.7 | 0 | Resto de fio | bate |
| 1º | 13:00-13:57 | 57 | 43.2 | 40.8 | -16.2 | 0 | Set-up | diverge muito |
| 2º | 13:47-15:00 | 0 | 13.8 | 11.4 | +11.4 | 158 |  | diverge |
| 2º | 15:00-16:00 | 0 | 2.8 | 0.0 | +0.0 | 150 |  | bate |
| 2º | 16:00-17:00 | 0 | 6.5 | 5.2 | +5.2 | 150 |  | diverge |
| 2º | 17:00-18:00 | 60 | 60.0 | 60.0 | +0.0 | 0 | Falta de operador | bate |
| 2º | 18:00-19:00 | 60 | 60.0 | 60.0 | +0.0 | 0 | Set-up | bate |
| 2º | 19:00-20:00 | 60 | 58.5 | 57.8 | -2.2 | 0 | Set-up | bate |
| 2º | 20:00-21:00 | 40 | 42.3 | 39.6 | -0.4 | 63 | Alimentação de fio | bate |
| 2º | 21:00-22:00 | 0 | 4.6 | 2.6 | +2.6 | 190 | Divergência do Tempo Padrão | bate |
| 2º | 22:00-22:20 | 0 | 0.6 | 0.0 | +0.0 | 126 | Divergência do Tempo Padrão | bate |
| 3º | 22:20-23:00 | 0 | 1.4 | 0.0 | +0.0 | 62 |  | bate |
| 3º | 23:00-00:00 | 0 | 14.8 | 12.8 | +12.8 | 197 |  | diverge |
| 3º | 00:00-01:00 | 0 | 1.9 | 0.0 | +0.0 | 197 |  | bate |
| 3º | 01:00-02:00 | 0 | 6.1 | 4.5 | +4.5 | 197 |  | bate |
| 3º | 02:00-03:00 | 0 | 56.9 | 56.7 | +56.7 | 0 | Refeição | diverge muito |
| 3º | 03:00-04:00 | 0 | 19.5 | 17.7 | +17.7 | 197 |  | diverge muito |
| 3º | 04:00-05:00 | 0 | 13.7 | 9.8 | +9.8 | 80 | Alimentação de fio | diverge |
| 3º | 05:00-05:20 | 0 | 19.8 | 19.8 | +19.8 | 0 | Alimentação de fio | diverge muito |

## Por turno

| Turno | GMS parado | FB total | FB ≥1 min | Status GMS |
|---|---|---|---|---|
| 1º | 277 | 266.7 | 250.4 | Finalizado |
| 2º | 220 | 249.1 | 236.6 | Finalizado |
| 3º | 0 | 134.1 | 121.3 | Rascunho |
