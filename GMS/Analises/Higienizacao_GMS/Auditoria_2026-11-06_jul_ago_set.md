# Auditoria: julho, agosto e setembro/2026 (06/11/2026)
Aprovado pelo William ("sim, os 88", olhando CP, SAP, GMS e BD Packing List). Sem nomes e sem linhas de produção; valores antigos em `C:\Users\U445131\Downloads\Jul_Ago_Set_propostas.md` e conciliação em `Conciliacao_fontes_jan_set_2026.md` (fora do Git, com metros).
## Gravação
- Lote Q: 88 campos de quantidade em 50 fichas Finalizado (julho 20 em 9, agosto 29 em 17, setembro 39 em 24): etapa anterior = seguinte + refugo; valor digitado errado = etapa seguinte; tolerância 1,5x o lote. 0 recusas, 0 falhas; conferência 88/88; nenhum evento nem histórico gerado.
- Julho teve parada de férias coletivas (nenhuma etapa terminou de 04 a 26/07): tratada como parada real, sem ajuste nem reconstrução. Nenhuma OP do SAP de julho sem ficha; em agosto e setembro a extração da ficha é 114% e 112% do SAP.
## Saúde
| Indicador | Julho | Agosto | Setembro |
|---|---|---|---|
| Operador com nome válido | 100% | 100% | 100% |
| Quantidade coerente | 88,5% → 100% | 93,3% → 98,4% | 92,3% → 98,5% |
| Datas de fim em ordem | 100% | 99,4% | 100% |
| Ficha 100% saudável | 88,5% → 100% | 93,3% → 98,4% | 92,3% → 98,5% |
## Conciliação das 4 fontes (percentuais; metros no arquivo fora do Git)
| Mês | GMS/CP | GMS/SAP | Packing/SAP | Packing/GMS |
|---|---|---|---|---|
| jan | 88% | 87% | — | — |
| fev | 98% | 103% | — | — |
| mar | 99% | 107% | — | — |
| abr | 99% | 112% | — | — |
| mai | 90% | 97% | 86% | 89% |
| jun | 93% | 101% | 91% | 90% |
| jul | — | 122% | 103% | 84% |
| ago | — | 114% | 108% | 95% |
| set | — | 112% | 107% | 95% |
- De fevereiro a abril CP, SAP e GMS ficam entre 98% e 112% um do outro. Janeiro é o mais fraco do GMS (fichas apagadas); maio e junho ficam em 90 a 93% do CP.
- Fora (decisão): agosto 3150, 3173, 3201 e 3362; setembro 3523, 3588, 3644 e 3705 (valor novo acima de 1,5x o lote).
## Fichas pendentes (grupo 1), aprovado "Sim, os 25"
- 25 campos de quantidade em 23 fichas (jan a set) em que um único valor destoava dos vizinhos da própria ficha (zero a mais, 1 digitado, valor alto isolado), trazidos ao nível dos vizinhos. 0 recusas, 0 falhas; conferência 25/25. Valores antigos em `ficha_undo_2026-11-06_grupo1.md` (Downloads).
- Restam 16 fichas ambíguas (1315, 1438, 1470, 1499, 1608, 1954, 2525, 2570, 2611, 2682, 2735, 3150, 3523, 4036, 4054, 4166) para decisão do William.
## Fichas pendentes (grupo 2), aprovado "Sim, os 35"
- 35 campos de quantidade em 15 fichas ambíguas (1315, 1438, 1470, 1499, 1608, 1954, 2525, 2570, 2682, 2735, 3150, 3523, 4036, 4054, 4166), alinhando o valor discrepante ao bloco coerente da própria ficha; defeito_* nunca alterado. 0 recusas, 0 falhas; conferência 35/35. Valores antigos em `ficha_undo_2026-11-06_grupo2.md` (Downloads).
- Fica para o William: ficha 2611 (sem palpite seguro) e a conferência de 2735 e 4036, que têm quantidades idênticas em meses diferentes (possível cópia).
## Pendentes finais (06/11/2026), aprovado "Sim, os 169"
- 27 fichas de janeiro que paravam na vulcanização (a OP tem lançamento no SAP em janeiro: a debandagem e a extração aconteceram e não foram registradas; 11 delas fechadas em lote no mesmo minuto): debandagem = vulcanização, extração = vulcanização x 0,97, fim da debandagem = fim da vulcanização + 271 min, fim da extração = fim da debandagem + 175 min, operadores estimados pelo turno (marca com os originais na observação). Mais a ficha 2611 alinhada ao SAP (7 quantidades). Total 169 campos em 28 fichas; 0 recusas, 0 falhas; conferência 169/169. Fora: ficha 1047 (OP sem lançamento no SAP).
- Janeiro agora: operadores 99,3%, quantidade coerente 99,3%, datas em ordem 272 de 292 (93,2%; 20 sem data), ficha 100% saudável 92,5%; extração (originais + reconstruídas) a 96,6% do CP.
- Resta para o William: conferir 2735 e 4036 (quantidades idênticas em meses diferentes) e os códigos de operador (hoje estimados pelo turno).
