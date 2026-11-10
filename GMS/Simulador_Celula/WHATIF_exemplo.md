# What-if de exemplo: demanda de 8000 m/dia de saída boa

Gerado por `python simulador.py`. 40 dias úteis simulados, 300 réplicas, plano típico dos últimos 60 dias do histórico.
Pessoas de referência = mediana de quem apontou na ficha (provisório).

| Cenário | saída boa m/dia (média) | p10–p90 do dia | % dos dias ≥ demanda | % das semanas ≥ demanda | gargalo (menor capacidade, m/dia equivalentes na extração) |
|---|---|---|---|---|---|
| Base: 2 turnos, pessoas de referência | 6371 | 4293–8674 | 16 | 12 | trancagem (5969) |
| 3º turno só na trançagem | 7298 | 5159–9491 | 33 | 20 | cobertura (7071) |
| 3º turno em todas as etapas | 7665 | 5487–9973 | 39 | 28 | trancagem (7324) |
| Base com 1 pessoa a menos por turno na extração | 6147 | 4794–7422 | 2 | 0 | trancagem (5969) |
| Base com 1 pessoa a mais por turno na extração | 6372 | 4286–8618 | 16 | 12 | trancagem (5969) |
| 3º turno em todas as etapas e 1 pessoa a mais na extração | 7666 | 5465–9967 | 39 | 27 | trancagem (7324) |
| Base sem falta de tubo e de fio na trançagem | 6935 | 4798–9175 | 25 | 14 | trancagem (6586) |
| Base com metade das trocas de mangueira (sequenciamento) | 6431 | 4338–8761 | 17 | 12 | trancagem (6029) |
| Base com 1 trançadeira a menos por turno (falta de operador) | 5546 | 3707–7739 | 9 | 10 | trancagem (5121) |
