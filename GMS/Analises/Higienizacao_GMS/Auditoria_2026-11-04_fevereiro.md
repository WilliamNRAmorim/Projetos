# Auditoria: fevereiro/2026 na ficha_producao (04/11/2026)
Sem nomes e sem linhas de produção (listas em `GMS/Analises/Tratamento_Ficha_2026-11/`: `Fevereiro_propostas.md` e `ficha_undo_2026-11-04_fevereiro.md`).
## Gravação (aprovada pelo William: "Sim, os 5 lotes")
- Lotes 1 a 4: 211 campos em 162 fichas (operadores por nome parcial com único candidato: 165; quantidades por placeholder e cadeia anterior = seguinte + refugo: 34; bitola da ficha vazia pelo sufixo da mangueira: 1; extração estimada nas fichas de confiança alta: 11). 0 falhas, 0 recusas pela guarda; conferência 211/211; nenhum outro campo das fichas tocadas mudou.
- Lote 5: 15 fichas reconstruídas (IDs 4327 a 4341), mesmas regras de janeiro; 0 OPs duplicadas; conferência sem divergência real (só formato de data com ou sem milissegundos). 4 OPs sem ficha modelo ficaram de fora.
- Fluxos automáticos: nenhum disparado (Eventos_Producao, Historico_Carretel e Hora-Hora com as mesmas contagens). Total de itens: 3.102.
- Desfazer: voltar os campos aos valores antigos do arquivo de desfazer (lotes 1 a 4) e apagar os itens `RECONSTRUIDA_SAP` (lote 5), ou restaurar a versão anterior do item.
## Saúde de fevereiro (295 originais; 310 com as reconstruídas)
| Indicador | Antes | Depois (com reconstruídas) |
|---|---|---|
| Operador com nome válido | 32,6% | 42,4% |
| Quantidade coerente | 91,5% | 97,4% |
| Bitola na tabela | 99,7% | 100% |
| Ficha 100% saudável | 0% | 4,8% |
| Volume ficha/CP: trançagem, bandagem, debandagem, extração | 73,9 / 85,2 / 88,8 / 90,5% | 79,2 / 92,0 / 92,9 / 98,2% |
## Achados
- O SAP bate com o CP na extração (149,6 mil m contra 156,4 mil m); o CP da trançagem é maior porque conta o que está em processo e o refugo. A trançagem não chega a 100% do CP.
- Só 19 OPs do SAP de fevereiro não têm ficha.
- Maior problema que sobra: datas de fim (214 de 295 sem fim da debandagem; em 182 o fim da cobertura vem antes do fim da trançagem). Aguarda regra do William.
