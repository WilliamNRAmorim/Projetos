# Plano: BI em hora cheia, refeição fora da meta e mudanças do Fable (MEL-267)

Data: 11/11/2026. Status: **aprovado pelo William em 11/11/2026** (com a navegação Mangueira × Montagem acrescentada).
Vale só para o Power BI. O app, a lista Hora-Hora e o jeito de apontar não mudam.

## 1. Decisões do William (11/11)
1. **Hora-Hora do BI por hora cheia.** 1º turno 05:00–14:00 (9 h), 2º 14:00–22:00 (8 h), 3º 22:00–05:00 (7 h). Dia produtivo do BI: 05:00 de D até 05:00 de D+1.
2. **Janelas quebradas são compensadas pelo que o operador apontou**, na proporção dos minutos:
   | Hora cheia | Vem de |
   |---|---|
   | 05:00–06:00 (1º) | `05:00 - 05:20` (3º turno da noite anterior) + `05:20 - 06:00` |
   | 13:00–14:00 (1º) | `13:00 - 13:57` + 3/63 de `13:47 - 15:00` |
   | 14:00–15:00 (2º) | 60/63 de `13:47 - 15:00` (a janela vale 13:57–15:00) |
   | 22:00–23:00 (3º) | `22:00 - 22:20` + `22:20 - 23:00` + 40/60 da hora extra `22:20 - 23:20` |
   | 23:00–00:00 (3º) | `23:00 - 00:00` + 20/60 da hora extra `22:20 - 23:20` |
   As demais janelas já são hora cheia e passam inteiras. Meta, real e parado seguem a mesma proporção; parado nunca passa dos minutos da fatia.
3. **Refeição sai da meta.** Na janela com Motivo Padrão Almoço, a meta perde 45 min: `Meta Hora × máx(0, Minutos − 45) ÷ Minutos`. O real fica inteiro: quem produziu na refeição fica acima da meta. Turno sem Almoço lançado fica com meta cheia. Refeição continua fora de Parado e de Principal parada.
4. **Cartão Meta e Aderência voltam para 21h35 (1295/1440)**, só sem hora filtrada. ⚠ Com a regra 3, o turno com Almoço lançado perde a refeição duas vezes no cartão (45 min na janela e mais a fatia do 21h35). Você pediu assim mesmo; fica registrado e o `revisor` aponta o tamanho do efeito.
5. **Montagem: tempo excedido (TE) da OT com refeição.** Se a OT tem parada `RF - Refeição` vinculada (mesma `OPVinculada`), o TE dela vira `máx(0, TE − 45)`. TE sem OT vinculada fica como está. Refeição segue fora da parada real.
   - Leitura que vou usar: a meta diária da Montagem (`dMetaMontagem[MetaDia]`) já é do turno sem refeição e **não muda**; "tirar a refeição" na Montagem é o desconto no TE e ela continuar fora da parada. Se a MetaDia for do turno cheio, me diga os minutos do turno da Montagem e eu desconto os 45 min nos turnos com RF.
6. **Fable (missão L), todos os itens do BI:** tema (B2+B4), acabamento (B7), Visão Geral nova e layout de celular (B1+B3), `dTurno` e tabela única (B5+B6). Isso muda o layout salvo da Visão Geral (a regra de 26/10 de não mexer no layout cede a este pedido).

## 2. O que muda no modelo (GMS)
Script TMDL em `GMS/PowerBI/modelo/fHoraCheia.tmdl.md`, aplicado no modelo vivo pelo TMDL view só com o seu "Libero".
- **Tabela calculada `fHoraCheia`** (uma linha por máquina × dia produtivo × hora cheia × janela de origem), a partir da `fHoraHora`:
  `Célula`, `Mangueira`, `Data BI`, `Turno BI` (pela hora: 1º, 2º, 3º), `Hora` ("05:00 - 06:00"...), `HoraOrdem` (0 = 05:00 ... 23 = 04:00), `Minutos`, `Meta`, `Real`, `Parado`, `Motivo`, `Motivo Padrão`, `ID Origem`, `Fração`.
  O início absoluto da janela sai da `HoraOrdem` da base (pós-meia-noite = 1440+), com `13:47 - 15:00` tratada como 13:57.
- **Tabela `dTurno`** (1º, 2º, 3º Turno, com ordem), ligada a `fHoraCheia[Turno BI]` e às colunas novas `Turno BI = TRIM(Turno)` de `Producao_Montagem` e `Paradas_Montagem` (hoje chegam com espaço à esquerda).
- **Medida de TE da Montagem** com o desconto da regra 5.
- `fHoraHora` e as colunas BI de hoje ficam, sem uso no relatório, até a conferência fechar. Depois saem (outro "Libero").

## 3. O que muda no relatório (`GMS_Painel.Report`)
- Página Hora-Hora: eixo e segmentações passam para `fHoraCheia[Hora]` e `dTurno`; medidas `HH Meta`, `HH Meta Útil` (1295/1440), `HH Real`, `HH Aderência` (1295/1440), `HH Parado`, `HH Principal Parada` leem a `fHoraCheia`.
- Visão Geral e Paradas deixam a tabela `Hora-Hora` e o filtro escondido "Motivo Padrão ≠ Almoço" e passam para a `fHoraCheia` (B6).
- `Minutos Excedidos Montagem` com o desconto da RF.
- B5: Período e Turno na mesma posição e no mesmo grupo de sincronização em todas as páginas (Fluxo inclusive); Turno vem da `dTurno`.
- B2+B4: `GMS_Tema.json` (1ª cor `#2C6FBF`, good `#16A34A`, neutral `#E67E22`, bad `#C0392B`; texto 12 pt). Onde o visual tem fonte de 8 ou 9 pt escrita nele, só a fonte sobe para 12; posição e tamanho não mudam.
- B7: eixo Ano-Mês no `g_ppm`, motivos da Montagem por valor com legenda de cor de verdade, títulos em forma de pergunta, texto alternativo nos visuais, filtro de máquinas da Hora-Hora sem lista à mão, cores de turno nos tokens.
- B1: Visão Geral com 5 cartões (metragem trançada × meta do dia, aderência, parado, refugo PPM × 3900, Montagem % × meta), cada um com cor de estado, seta e texto; visual principal "Qual máquina está mais longe da meta?"; motivos do dia ao lado. Até 8 visuais de dado.
- B3: layout de celular (`mobile.json`) só para Visão Geral e Hora-Hora.
- **Navegação Mangueira × Montagem (pedido de 11/11):** no lugar do menu longo, dois botões no topo de toda página, "Mangueira" e "Montagem". Clicou em Mangueira, aparece só o menu das páginas de mangueira (Visão Geral, Hora-Hora, Paradas, Refugo, Cortes, Extrusora, Fluxo); em Montagem, só Produção Mont. e Paradas Mont. Feito com indicadores (bookmarks) e grupos de botões, texto legível (12 pt ou mais).

## 4. Como verifico
- Protótipo em Python sobre `HoraHora_backup_2026-09-01_a_2026-10-15.csv` com a mesma regra: por máquina e dia, a soma de real e parado na hora cheia bate com a base (só muda o que atravessa as 05:00), e a meta bate com a base menos 45 min nas janelas de Almoço. Exemplo de um dia da TH07 lado a lado (antes × depois) para você conferir.
- Depois do refresh: o mesmo dia da TH07 no BI contra o protótipo; consulta DAX `[State] <> 1` em medidas e colunas.
- JSON do relatório válido e diff só nos visuais do assunto.

## 5. Time e ordem
| # | Etapa | Quem (modelo) |
|---|---|---|
| 1 | Protótipo Python + script TMDL da `fHoraCheia`, `dTurno` e TE | `executor` (Sonnet) |
| 1' | Em paralelo: tema, B7, B5 e troca das medidas no relatório | `executor` (Sonnet) |
| 2 | Revisão de turno, meta, refeição e TE (antes de tocar no modelo) | `revisor` (Opus) |
| 3 | B1, B3 e navegação Mangueira × Montagem, depois da 1' | `executor` (Sonnet) |
| 4 | Aplicar o TMDL no modelo vivo, com o seu "Libero" | chefe, pelo navegador do app |
| 5 | Refresh, conferência TH07, diário (MEL-267), docs, commit e push | chefe |
| 6 | Reabrir o `.pbip` no Desktop e publicar | William |

## 6. Pendências que ficam
- App e lista seguem com as janelas quebradas; só o BI vira hora cheia.
- O Painel da Célula (app) e o OEE2 (MEL-266) continuam lendo a regra antiga até decisão sua.
- A regra de turno do BI passa a ser diferente da do app (`fx_Turno`, `fx_GradeHoraHora`): vira linha DECISÃO no diário, sem mexer no `GMS_Mestre_BI.md`.
