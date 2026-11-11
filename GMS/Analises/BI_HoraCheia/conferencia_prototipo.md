# Conferência do protótipo da hora cheia (MEL-267)

Gerado por `prototipo_hora_cheia.py` (`python -I`) sobre `HoraHora_backup_2026-09-01_a_2026-10-15.csv`. Regra: seção 1 de `PLANO.md`. Não altera nada no modelo nem no relatório.

- Linhas da base: 4024. Linhas da fHoraCheia (janela × hora cheia): 4244. Máquinas: Spiral, TH01, TH02, TH03, TH05, TH06, TH07, TM01, TM04, TO04.
- Dias da base (Data): 2026-09-14 a 2026-10-15. Dias BI gerados: 2026-09-14 a 2026-10-16.

## 1. Invariantes

Por máquina e dia (231 pares máquina × dia). Esperado do dia D = base(D) − janela 05:00-05:20 de D + janela 05:00-05:20 de D−1; as 60 janelas 05:00-05:20 da base são a única coisa que muda de dia.

| Grandeza | Σ base (sem desconto) | Σ depois | Maior desvio por máquina × dia vs esperado |
|---|---:|---:|---:|
| Minutos | 227020.00 | 227020.00 | 0.00e+00 |
| Real | 200380.00 | 200380.00 | 7.11e-15 |
| Parado (min) | 87896.30 | 87896.30 | 0.00e+00 |
| Meta (depois do desconto do almoço) | 496835.43 | 496835.43 | 0.00e+00 |

Σ minutos, real e parado antes × depois: diferença total 0.00e+00, 0.00e+00, 0.00e+00 (o total geral não muda; muda só o dia, por causa da fronteira das 05:00).
Parado cortado pelo limite dos minutos da fatia: 0.0000 min no total (nenhuma fatia estourou).

**Meta.** Σ meta base = 525845.00; desconto do almoço = 29009.57 (293 janelas com Motivo Padrão Almoço); base − desconto = 496835.43; Σ meta depois = 496835.43; diferença 0.00e+00.
Janelas de Almoço com Minutos ≤ 45 (meta vai a zero): 0. Janelas de Almoço com Minutos > 45: 293.
Almoço por janela de origem: 02:00 - 03:00: 44; 11:00 - 12:00: 72; 12:00 - 13:00: 17; 13:00 - 13:57: 23; 18:00 - 19:00: 55; 19:00 - 20:00: 82.

## 2. Colisões

- Hora extra `22:20 - 23:20` na mesma máquina e dia (Data) de linhas do 3º turno `22:20 - 23:00`/`23:00 - 00:00`: **6** de 30 máquinas × dia com hora extra (hora extra em 30 linhas).
- Horas cheias 22:00 e 23:00 (3º turno) com fatia da hora extra E fatia do 3º turno: 12 (22:00-23:00: 6; 23:00-00:00: 6). Nelas as duas somam (rateio proporcional).
- Janelas duplicadas na base (mesma máquina, Data e Hora): **123** combinações (123 linhas a mais). Entram duas vezes no rateio, como entram hoje na fHoraHora; é sujeira da lista (MEL-104/155), não da regra.
  Por janela: 05:00 - 05:20: 1; 05:20 - 06:00: 7; 06:00 - 07:00: 7; 07:00 - 08:00: 7; 08:00 - 09:00: 8; 09:00 - 10:00: 11; 10:00 - 11:00: 12; 11:00 - 12:00: 14; 12:00 - 13:00: 16; 13:00 - 13:57: 20; 13:47 - 15:00: 2; 15:00 - 16:00: 2; 16:00 - 17:00: 2; 17:00 - 18:00: 2; 18:00 - 19:00: 2; 19:00 - 20:00: 2; 20:00 - 21:00: 2; 21:00 - 22:00: 3; 22:00 - 22:20: 3.
- Horas cheias (máquina × dia × hora) com mais de 60 minutos somados: **135**. Causa: janelas `22:00 - 22:20` com Minutos 41 e `22:20 - 23:00` com Minutos 19 na base, mais duplicatas e a hora extra (22:20-23:20) somada ao 3º turno. O protótipo rateia pelo rótulo (20 e 40 min) e carrega o Minutos da linha; não corrigi.
  Minutos por janela 22:xx na base: 22:00 - 22:20 = 20: 133 linhas; 22:00 - 22:20 = 41: 54 linhas; 22:20 - 23:00 = 19: 20 linhas; 22:20 - 23:00 = 40: 34 linhas.

## 3. Divergências do plano com os dados

- Rótulo `Turno` da base diferente do turno pela hora: 493 linhas (soltas, já conhecidas). O `Turno BI` sai só da hora, como o plano manda.
- `HoraOrdem` da fHoraHora (minutos desde 00:00, +1440 se < 05:20) confere: `05:00 - 05:20` = 1740 (D+1 05:00 na conta); `05:20 - 06:00` = 320; `13:47 - 15:00` = 827, tratada como 837 (13:57).
- Todas as linhas têm Hora no formato `hh:mm - hh:mm`; nenhum rótulo fora dos que o plano lista.
- Janelas 22:xx: na base a `22:00 - 22:20` tem Minutos 41 em 54 linhas e a `22:20 - 23:00` tem Minutos 19 em 20 linhas (o 2º turno fecha 524 min e o 3º 399 min, soma do dia 1.440). O plano não prevê isso; mantive o Minutos da linha (sem inventar regra).
- `13:47 - 15:00`: pelo rótulo seriam 73 min, mas a janela vale 13:57–15:00 = 63 min (igual ao Minutos da base): 3/63 vai à hora 13:00 e 60/63 à 14:00, como no plano.
- Meta do almoço usa 45 fixo (plano), mesmo quando o Tempo Parado da linha de Almoço é outro (ex.: 46).

## 4. Dia completo da TH07: antes (por janela) × depois (por hora cheia)

Dia escolhido: **TH07, dia produtivo 2026-09-24** (05:00 de 2026-09-24 até 05:00 de 2026-09-25), com hora extra, almoço e a janela 05:00-05:20 da noite anterior (se existir na base).

**Antes: por janela da base (Data = 2026-09-24)**

| Turno (base) | Hora (janela) | Min | Meta Hora | Real | Parado | Motivo Padrão |
|---|---|---:|---:|---:|---:|---|
| 1º Turno | 05:20 - 06:00 | 40 | 152.00 | 152 | 0.0 |  |
| 1º Turno | 06:00 - 07:00 | 60 | 228.00 | 228 | 0.0 |  |
| 1º Turno | 07:00 - 08:00 | 60 | 228.00 | 0 | 60.0 | Alimentação de fio |
| 1º Turno | 08:00 - 09:00 | 60 | 228.00 | 228 | 0.0 |  |
| 1º Turno | 09:00 - 10:00 | 60 | 228.00 | 228 | 0.0 |  |
| 1º Turno | 10:00 - 11:00 | 60 | 228.00 | 0 | 60.0 | Alimentação de fio |
| 1º Turno | 11:00 - 12:00 | 60 | 228.00 | 0 | 60.0 | Alimentação de fio |
| 1º Turno | 12:00 - 13:00 | 60 | 228.00 | 0 | 60.0 | Almoço |
| 1º Turno | 13:00 - 13:57 | 57 | 217.00 | 217 | 0.0 |  |
| 2º Turno | 13:47 - 15:00 | 63 | 239.00 | 0 | 60.0 | Reunião |
| 2º Turno | 15:00 - 16:00 | 60 | 228.00 | 0 | 60.0 | Reunião |
| 2º Turno | 16:00 - 17:00 | 60 | 228.00 | 0 | 60.0 | Falta de fio - Bobinadeira |
| 2º Turno | 17:00 - 18:00 | 60 | 228.00 | 200 | 0.0 | Execução Check List Lean |
| 2º Turno | 18:00 - 19:00 | 60 | 228.00 | 200 | 0.0 | Emenda de Fita |
| 2º Turno | 19:00 - 20:00 | 60 | 228.00 | 46 | 45.0 | Almoço |
| 2º Turno | 20:00 - 21:00 | 60 | 228.00 | 100 | 30.0 | Falta de insulation |
| 2º Turno | 21:00 - 22:00 | 60 | 228.00 | 200 | 0.0 | Falta de insulation |
| 2º Turno | 22:00 - 22:20 | 20 | 76.00 | 60 | 0.0 | Ajuste da Máquina |
| 2º Turno | 22:20 - 23:20 | 60 | 228.00 | 0 | 0.0 |  |
| 3º Turno | 22:20 - 23:00 | 40 | 152.00 | 152 | 0.0 |  |
| 3º Turno | 23:00 - 00:00 | 60 | 228.00 | 70 | 0.0 | Alimentação de fio |
| 3º Turno | 00:00 - 01:00 | 60 | 228.00 | 0 | 0.0 | Alimentação de fio |
| 3º Turno | 01:00 - 02:00 | 60 | 228.00 | 228 | 0.0 |  |
| 3º Turno | 02:00 - 03:00 | 60 | 228.00 | 0 | 0.0 | Almoço |
| 3º Turno | 03:00 - 04:00 | 60 | 228.00 | 228 | 0.0 |  |
| 3º Turno | 04:00 - 05:00 | 60 | 228.00 | 152 | 0.0 | Troca de Carretel |
| 3º Turno | 05:00 - 05:20 | 20 | 76.00 | 70 | 0.0 |  |
| **Total** | | 1500 | 5700.00 | 2759 | 495.0 | |

**Depois: por hora cheia (Data BI = 2026-09-24)**

| Turno BI | Hora | Min | Meta | Real | Parado | Origem (ID: janela × fração) |
|---|---|---:|---:|---:|---:|---|
| 1º Turno | 05:00 - 06:00 | 60.00 | 228.00 | 183.00 | 0.00 | 27168: 05:00 - 05:20 × 1.000; 27240: 05:20 - 06:00 × 1.000 |
| 1º Turno | 06:00 - 07:00 | 60.00 | 228.00 | 228.00 | 0.00 | 27241: 06:00 - 07:00 × 1.000 |
| 1º Turno | 07:00 - 08:00 | 60.00 | 228.00 | 0.00 | 60.00 | 27242: 07:00 - 08:00 × 1.000 |
| 1º Turno | 08:00 - 09:00 | 60.00 | 228.00 | 228.00 | 0.00 | 27243: 08:00 - 09:00 × 1.000 |
| 1º Turno | 09:00 - 10:00 | 60.00 | 228.00 | 228.00 | 0.00 | 27244: 09:00 - 10:00 × 1.000 |
| 1º Turno | 10:00 - 11:00 | 60.00 | 228.00 | 0.00 | 60.00 | 27245: 10:00 - 11:00 × 1.000 |
| 1º Turno | 11:00 - 12:00 | 60.00 | 228.00 | 0.00 | 60.00 | 27246: 11:00 - 12:00 × 1.000 |
| 1º Turno | 12:00 - 13:00 | 60.00 | 57.00 | 0.00 | 60.00 | 27247: 12:00 - 13:00 × 1.000 |
| 1º Turno | 13:00 - 14:00 | 60.00 | 228.38 | 217.00 | 2.86 | 27248: 13:00 - 13:57 × 1.000; 27297: 13:47 - 15:00 × 0.048 |
| 2º Turno | 14:00 - 15:00 | 60.00 | 227.62 | 0.00 | 57.14 | 27297: 13:47 - 15:00 × 0.952 |
| 2º Turno | 15:00 - 16:00 | 60.00 | 228.00 | 0.00 | 60.00 | 27204: 15:00 - 16:00 × 1.000 |
| 2º Turno | 16:00 - 17:00 | 60.00 | 228.00 | 0.00 | 60.00 | 27205: 16:00 - 17:00 × 1.000 |
| 2º Turno | 17:00 - 18:00 | 60.00 | 228.00 | 200.00 | 0.00 | 27206: 17:00 - 18:00 × 1.000 |
| 2º Turno | 18:00 - 19:00 | 60.00 | 228.00 | 200.00 | 0.00 | 27207: 18:00 - 19:00 × 1.000 |
| 2º Turno | 19:00 - 20:00 | 60.00 | 57.00 | 46.00 | 45.00 | 27208: 19:00 - 20:00 × 1.000 |
| 2º Turno | 20:00 - 21:00 | 60.00 | 228.00 | 100.00 | 30.00 | 27209: 20:00 - 21:00 × 1.000 |
| 2º Turno | 21:00 - 22:00 | 60.00 | 228.00 | 200.00 | 0.00 | 27210: 21:00 - 22:00 × 1.000 |
| 3º Turno | 22:00 - 23:00 | 100.00 | 380.00 | 212.00 | 0.00 | 27211: 22:00 - 22:20 × 1.000; 27212: 22:20 - 23:20 × 0.667; 27340: 22:20 - 23:00 × 1.000 |
| 3º Turno | 23:00 - 00:00 | 80.00 | 304.00 | 70.00 | 0.00 | 27212: 22:20 - 23:20 × 0.333; 27341: 23:00 - 00:00 × 1.000 |
| 3º Turno | 00:00 - 01:00 | 60.00 | 228.00 | 0.00 | 0.00 | 27342: 00:00 - 01:00 × 1.000 |
| 3º Turno | 01:00 - 02:00 | 60.00 | 228.00 | 228.00 | 0.00 | 27343: 01:00 - 02:00 × 1.000 |
| 3º Turno | 02:00 - 03:00 | 60.00 | 57.00 | 0.00 | 0.00 | 27344: 02:00 - 03:00 × 1.000 |
| 3º Turno | 03:00 - 04:00 | 60.00 | 228.00 | 228.00 | 0.00 | 27345: 03:00 - 04:00 × 1.000 |
| 3º Turno | 04:00 - 05:00 | 60.00 | 228.00 | 152.00 | 0.00 | 27346: 04:00 - 05:00 × 1.000 |
| **Total** | | 1500.00 | 5187.00 | 2720.00 | 495.00 | |

Por turno BI: 1º Turno: min 540.0, meta 1881.4, real 1084.0, parado 242.9; 2º Turno: min 480.0, meta 1652.6, real 746.0, parado 252.1; 3º Turno: min 480.0, meta 1653.0, real 890.0, parado 0.0.

Leitura: a `05:00 - 05:20` da noite anterior (Data 2026-09-23, 3º turno) entra no 05:00-06:00 do dia 2026-09-24; a `05:00 - 05:20` deste dia (Data 2026-09-24) sai para o dia 2026-09-25. Por isso o total do dia difere do da base só por essas duas janelas.

Referência para o DAX de conferência de `fHoraCheia.tmdl.md`: comparar com a tabela 'Depois' acima (dia 2026-09-24, célula TH07).

## 5. Modelo vivo (11/11/2026, depois de aplicar e do refresh)
- Script aplicado pelo TMDL view com o Libero do William. Na 1ª aplicação, o parado deu 244.465 min contra 750.491 min na base. A causa: 11.052 linhas de jan a set vêm sem `Minutos`, e o teto da fatia zerava o parado delas. Corrigido com `Mn` (Minutos da linha ou, vazio, a duração do rótulo), reaplicado e feito novo refresh.
- Totais na base inteira, depois da correção:
  - Real: 1.432.435,5 = base.
  - Parado: 722.651,6 contra 750.491,1. Os 3,7% de diferença são parado acima da duração da janela, que a regra corta; só nas linhas com Minutos são 12.891 min.
  - Meta: 3.928.649 contra 4.077.690, porque os 45 min do almoço saem agora também em jan a set.
  - 34.652 fatias, 225 horas cheias acima de 60 min (duplicatas e hora extra), 0 colunas em erro (`INFO.COLUMNS`).
- TH07, 24/09:
  - 1º e 2º turno: minutos, meta e real iguais ao protótipo.
  - 3º turno: 60 min e 228 m de meta a menos, porque a hora extra 22:20-23:20 desse dia não está no modelo vivo.
  - Parado maior que no backup (254,7, 278,0 e 185,8 min), por causa das correções de ND e NT feitas na lista depois de 15/10.
- `Minutos Excedidos Montagem` testada como medida de consulta: TE de 80.065,7 vira 72.700 min no período todo (1º turno 42.240,7 → 37.917; 2º 37.078 → 34.036; 3º 747 → 747). Todas as linhas da Montagem caem num turno da `dTurno`.
