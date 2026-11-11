# Revisão das regras: BI em hora cheia (MEL-267)

Data: 11/11/2026. O agente `revisor` não estava disponível nesta sessão (igual a 09/11). A revisão foi feita pelo chefe, rodando em Opus 5.5, sobre `fHoraCheia.tmdl.md`, `conferencia_prototipo.md` e as medidas `HH *`, `PA *` e `Minutos Excedidos Montagem` do `reportExtensions.json`.

## 1. Tabela fHoraCheia (DAX)
Aprovado, com uma correção aplicada.
- Bordas conferidas na mão: `05:20 - 06:00` vai para a hora 05 do dia D; `05:00 - 05:20` vai para a hora 05 do dia D+1; `00:00 - 01:00` e `04:00 - 05:00` ficam no dia D (3º turno); `23:00 - 00:00` cruza a meia-noite sem erro; `13:47 - 15:00` rateia 3/63 e 60/63; `22:20 - 23:20` rateia 40/60 e 20/60; `22:00 - 22:20` fica inteira na hora 22 (3º turno).
- **Corrigido:** rótulo com início igual ao fim (ex.: `06:00 - 06:00`) virava uma janela de 24 h e se espalhava em 24 fatias. Agora a tabela só aceita janela de 1 a 120 min (`FILTER ( Jan2, ... <= 120 )`).
- **Corrigido:** faltavam `Motivo 2` e `Motivo 2 Padrão`, que o visual `g_motivo2` da Hora-Hora usa.
- Dado, não regra: 54 linhas `22:00 - 22:20` com Minutos 41 e 123 janelas duplicadas na base continuam como estão. O rateio usa o rótulo, e os minutos vêm da linha.

## 2. Medidas HH e PA
Aprovado.
- Refeição fora de Parado e de Principal parada (`KEEPFILTERS(Motivo Padrão <> "Almoço")`).
- Fator 1295/1440 só sem hora filtrada.
- **Efeito da dupla contagem pedida pelo William** (setembro e outubro, protótipo): meta cheia de 525.845 m; com os 45 min do almoço, 496.835 m (94,5%); no cartão, com o 21h35 por cima, 446.800 m (85,0%). Uma máquina que lança almoço nos 3 turnos fica com cerca de 81,5% da meta cheia no cartão; uma que não lança, com 89,9%.
- Limite: o desconto só vale quando o Almoço está no Motivo (1). Almoço lançado só no Motivo 2 não desconta a meta.

## 3. Minutos Excedidos Montagem
Aprovado.
- O TE é somado por OP vinculada. A OP com parada RF perde 45 min, sem ficar negativa. O TE sem OP fica inteiro.
- Com Motivo no eixo, a barra de TE acha a RF porque a medida tira o filtro de Motivo só para procurá-la.
- O desconto é por OP **dentro do filtro**: OT que atravessa dois dias só desconta no dia em que a RF foi lançada.
- Parada real (`Parada Real Montagem`) continua sem TE e sem RF: as duas nunca se somam.

## 4. dTurno e relacionamentos
Risco a conferir na aplicação.
- Antes do `createOrReplace`, ver no TMDL view se já existe `dTurno` no modelo vivo. Se existir, anotar os relacionamentos dela e refazê-los.
- `Turno BI = TRIM(Turno)` resolve o espaço à esquerda da Montagem. Turno escrito fora do padrão "1º Turno" fica sem turno no filtro: conferir com `VALUES(Producao_Montagem[Turno BI])` depois do refresh.
- `dCalendario` é `CALENDAR` fixo (2025 a 2027), sem `CALENDARAUTO`, então não há risco de dependência circular com a tabela nova.
