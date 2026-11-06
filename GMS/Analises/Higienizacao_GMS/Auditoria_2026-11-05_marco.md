# Auditoria: março/2026 (05/11/2026)
Aprovado pelo William ("Estime por turno" e "Sim, os 4 lotes"). Sem nomes e sem linhas de produção; desfazer em `GMS/Analises/Tratamento_Ficha_2026-11/ficha_undo_2026-11-05_marco.md` e `Marco_propostas.md` (fora do Git).
## Gravação
- Lote Q: 26 quantidades corrigidas (regra anterior = seguinte + refugo; tolerância 1,5x o lote).
- Lote E: 122 quantidades estimadas em etapas com data de fim e quantidade vazia (etapa anterior; extração = última etapa x 0,97).
- Lote Op: 1.881 células de operador em 349 fichas: 149 nomes parciais com candidato único e 1.732 códigos, zeros, duplas, vazios e parciais ambíguos estimados pelo turno do horário real do fim da etapa, entre os nomes mais frequentes daquela etapa e período (até 2 nomes). **66% dos operadores de março passam a ser estimativa.** Cada ficha foi marcada na observação da trançagem ("[Operadores estimados pelo turno em 05/11/2026; nao e registro. Originais: ...]"), com os valores originais para desfazer.
- Lote R: 22 fichas reconstruídas (IDs 4356 a 4377, `RECONSTRUIDA_SAP`); 24 OPs do SAP de março sem ficha; ficaram de fora 1 sem ficha modelo e 1 com modelo a 60,7 dias.
- Guarda: cada item relido antes; 0 recusas, 0 falhas. Conferência 2.029/2.029 campos; nenhuma OP duplicada; nenhum evento nem histórico de carretel gerado pelas novas fichas.
## Saúde de março (349 originais)
| Indicador | Antes | Depois |
|---|---|---|
| Operador com nome válido | 33,9% | 100% (66% estimado) |
| Quantidade coerente | 92,0% | 97,4% |
| Datas de fim em ordem | 99,4% (após regras de datas) | 98,3% |
| Ficha 100% saudável | 0% | 95,7% |
| Volume contra o CP (tr / ba / de / ex), com as 22 reconstruídas | 86,0 / 92,6 / 86,3 / 91,5% | 97,6 / 103 / 93,8 / 98,5% |
- Fora (decisão): fichas 1608, 1663 e 1751 (valor novo acima de 1,5x o lote).
