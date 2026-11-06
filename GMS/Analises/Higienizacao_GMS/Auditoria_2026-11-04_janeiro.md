# Auditoria: limpeza da ficha_producao, janeiro/2026 (04/11/2026)
Sem nomes e sem linhas de produção. O arquivo de desfazer (com valores antigos por ficha e campo) fica em `GMS/Analises/Tratamento_Ficha_2026-11/ficha_undo_2026-11-04_janeiro.md`, fora do Git.

## Gravação (aprovada pelo William: "sim, lotes 1 a 4")
- 119 campos em 100 fichas; 0 falhas, 0 recusas pela guarda (cada item relido e só gravado se o valor vivo fosse o esperado).
- Conferência: 119/119 campos com o valor novo; nenhum outro campo das fichas tocadas mudou; total de itens 3.028.
- Lote 1: 91 células de operador (nome parcial com um único colaborador na lista). Lote 2: TE01 -> Spiral (2). Lote 3: Bitola 17 e vazio -> 12 (2). Lote 4: 24 quantidades (placeholders 111/1111/11111 na cobertura e cadeia anterior = seguinte + refugo; ficha 830 de fora).
- Desfazer: voltar cada campo ao valor antigo do arquivo de desfazer, ou restaurar a versão anterior do item (versionamento ligado, 50 versões).

## CP como verdade: por que a ficha não bate (ficha por mês de criação x CP do mês)
| Mês | Fichas | IDs que faltam na lista | Trançagem ficha/CP | Bandagem | Debandagem | Extração |
|---|---|---|---|---|---|---|
| 01 | 292 | 87 (23%) | 70% | 79% | 70% | 36% |
| 02 | 295 | 52 (15%) | 74% | 85% | 89% | 91% |
| 03 | 349 | 75 (18%) | 86% | 93% | 86% | 92% |
| 04 | 288 | 27 (9%) | 91% | 96% | 93% | 95% |
| 05 | 330 | 91 (22%) | 81% | 87% | 79% | 80% |
| 06 | 322 | 29 (8%) | 83% | 77% | 90% | 93% |

Causas encontradas:
1. **Fichas apagadas.** Há 552 IDs faltando entre 686 e 4265. A lixeira do site só guarda desde 03/08/2026 (as de janeiro a julho foram removidas de vez). Em janeiro, 87 IDs a ~650 m somam ~56 mil m, perto dos 55 mil m que faltam na trançagem. Nos outros meses os IDs faltantes explicam só uma parte.
2. **Datas de fim ausentes.** Em janeiro só 1 ficha tem data de fim da debandagem (452 com quantidade e sem data) e só 195 têm data de fim de extração; sem data não dá para casar por dia.
3. **Quantidades de extração vazias** em janeiro (154 de 292 preenchidas).
4. **Dia a dia não casa** nem na trançagem (5 de 22 dias dentro de 15%): o CP é por dia/turno de lançamento; a ficha tem o carretel inteiro numa data só.
5. Outras listas do site (Hora-Hora, Eventos_Producao, Historico_Carretel) só começam em jan (esparsa), jul e mai/2026: não recuperam janeiro a abril.
6. CP de julho tem outro layout (extração não lida) e a aba do dia 31 de janeiro está vazia.
