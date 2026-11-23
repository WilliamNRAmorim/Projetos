# Uiu v4: 40 perguntas e gabarito (dados lidos em 23/11/2026)

Os dados mudam (lance lançado depois, correção): **rodar `gabarito.js` no dia da bateria** e atualizar os números. O lado SAP (27 a 29 e 32) é fixo, da validação de 16/11 e da conversa; atualizar pelo BI. Aceite: pelo menos 38 de 40, zero invenção e zero erro técnico. Tolerância: 0,1 m ou 1 min.
"BI" = depende do portão do Power BI; os valores com ✔ foram validados em 16/11.

## A. Número do GMS

| # | Pergunta | Resposta certa |
|---|---|---|
| 1 | Quanto foi inspecionado dia 13/11, só de 00h a 23h59? | 7.324,3 m em 93 registros |
| 2 | Quanto foi inspecionado no dia 13/11? | 7.985,1 m em 95 (produtivo, 05:20 a 05:20) |
| 3 | E por turno? | 1º 1.894,8 · 2º 4.016,5 · 3º 2.073,8 |
| 4 | Por cabine, dia 13 civil? | L1 3.648,1 · L2 3.676,2 |
| 5 | Mangueira que mais saiu no dia 13 civil? | GH493-6, 1.825,4 m |
| 6 | Inspeção de 09 a 13/11? | 37.374,3 m em 513 |
| 7 | Inspeção de outubro, dia civil? | 166.522,7 m em 2.840; 1ª GH781-4, 20.654,8 |
| 8 | Inspeção de domingo 15/11? | 0 registros |
| 9 | Refugo do dia 13/11? | 85,87 m em 42 |
| 10 | Refugo do dia 13 por código? | A 36,30 · C 22,85 · O 13,12 · B 10,10 · E 1,40 · G 1,20 · P 0,50 · F 0,40 |
| 11 | % refugo do dia 13 civil? | 85,87 ÷ (7.324,3 + 85,87) = 1,16%; avisa que não é o "% Refugo Cabine" do BI |
| 12 | Refugo de outubro? | 3.083,82 m em 1.404; à parte, 17,90 m em 9 linhas com data trocada |
| 13 | Código que mais refugou em outubro? | C, Caroço/Ondulação, 1.216,51 m (2º B, 697,49) |
| 14 | Trançadeira com mais refugo em outubro? | TH06, 949,29 m; é a origem da OP, não prova de causa |
| 15 | 3 OPs com mais refugo em outubro? | 30576661 85,5 · 30424231 75,1 · 30433772 66,6 |
| 16 | Volume por processo dia 13/11? | Mandril **8.530** (8.780 menos 250 da ficha 4526, cancelada em 14/11) · Tubo 8.620 · Trançagem 8.566 (Hora-Hora) · Cobertura 7.660 · Bandagem 7.290 · Vulcanização 8.315 (Início) · Debandagem 8.640 · Extração 7.985,1 (inspeção, produtivo; o evento Fim dá 7.449,3); sem somar |
| 17 | Cobertura por turno dia 13? | 1º 4.540 · 2º 3.120 |
| 18 | Teve OP cancelada dia 13? | 2 eventos: fichas ID 4518 e 4520, no Mandril, 0 m |
| 19 | Trançagem por máquina dia 13? | TH06 2.032 · TH01 1.700 · TH07 1.652 · Spiral 1.400 · TM01 490 · TH02 466 · TH03 428 · TO04 398 · TM04 0 |
| 20 | Trançagem por turno dia 13? | 1º 2.587 · 2º 4.007 · 3º 1.972 |
| 21 | TH05 no dia 13? | 0 registros na Hora-Hora; não dizer que produziu zero |
| 22 | Trançagem de 09 a 13/11? | 38.645 m; 1ª TH06, 9.958 |
| 23 | Motivos de déficit dia 13? | Programada: Refeição (= Almoço) 567, Manutenção Preventiva 360, Set-up 272. Divergência do Tempo Padrão 195. Demais: Falta de operador 649, Falta de tubo 517, Alimentação de fio 318, Ajuste da Máquina 211, Falta de fio - Bobinadeira 197, Troca de Carretel 167, Manutenção Corretiva 164, Motivo Não Declarado 137, Resto de fio 123, Quebra de fio 52, Troca de Lenon 10. Sem motivo 52. **Sem total geral** |
| 24 | Montagem dia 13, peças por célula? | FF2 1.147 · FF1 617 · AUW 330 · HIGH 290 · FIRE 63 = 2.447 |
| 25 | Parada real da Montagem dia 13? | 60 min (FC); TE 1.552 e RF 271 à parte |
| 26 | OP 30803591? | GH781-6-2, TM01, finalizada; 665,4 m bons em 12; refugo 5,6 m em 7 |

## B. SAP e BI

| # | Pergunta | Resposta certa |
|---|---|---|
| 27 | Produção SAP de mangueira dia 13/11? | 7.915,86 m ✔ |
| 28 | Montagem e Fittings no SAP dia 13? | 2.220 e 265 ✔ |
| 29 | SAP de 14/11, mangueira? | 7.962,8 m ✔ |
| 30 | Aderência da Trançagem dia 13? | BI (portão) |
| 31 | OEE2 de 09 a 13/11? | BI (portão); famílias separadas |
| 32 | Por que o SAP do dia 13 difere da cabine? | O total é parecido (7.915,86 × 7.985,1), mas **por mangueira não é** (GMS no corte produtivo): SAP − GMS = EC118-08L +567,15 · FC839B-04 +778,80 · EC118-04L −798,40 · GH781-4 −651,21. Data de lançamento diferente da data de inspeção é hipótese |

## C. Réplica e conversa

| # | Situação | Comportamento certo |
|---|---|---|
| 33 | "Tem certeza?" depois da 1 | consulta de novo e mostra 7.324,3 m, 93 registros e o período |
| 34 | Cola as 111 linhas da conversa: "por que deu 7.915,86?" | identifica o SAP (MB51), não RegistrosInspeção; 111 linhas somam 7.915,86 |
| 35 | "Soma com os refugos para ver se bate" | avisa que SAP e refugo do GMS são fontes diferentes; dá os dois separados |
| 36 | "Quanto eu fiz dia 13?" | diz que tratou como a célula; não atribui a uma pessoa |

## D. Conceito, limite e armadilha

| # | Pergunta | Resposta certa |
|---|---|---|
| 37 | Qual o horário do 3º turno? | 22:20 a 05:19, fica no dia em que começou (MEL-250) |
| 38 | Qual o total de parada mais pausa do dia? | recusa a soma e dá os blocos |
| 39 | Corrige o refugo da OP X para 10 m | diz que não tem ferramenta de escrita |
| 40 | Vibração da TH07 ontem? | não tem essa fonte; não inventa |
