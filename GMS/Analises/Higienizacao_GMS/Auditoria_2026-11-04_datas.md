# Auditoria: datas de fim, janeiro a março/2026 (04/11/2026)
Aprovado pelo William ("Sim, as 4 regras" e "Sim, gravar"). Sem nomes e sem linhas de produção; valores antigos em `C:\Users\U445131\Downloads\ficha_undo_2026-11-04_datas.md` (fora do Git).
- Regras: R1 fim da trançagem limitado ao início da cobertura menos 5 min (416); R2 fim da debandagem ausente (431); R3 hora real na extração com só a data (04:00:00Z, 456); R4 fim da extração ausente (218). Detalhe em `Metodo_mensal_ficha.md`.
- Gravado: 1.521 campos de data de fim (field_20, field_40, field_44) em 729 fichas Finalizado de jan a mar, sem as reconstruídas. 0 falhas, 0 recusas pela guarda.
- Conferência: 1.521/1.521 com o valor novo; nenhum outro campo das fichas tocadas mudou; total de itens 3.102; Eventos_Producao, Historico_Carretel e Hora-Hora sem mudança.
- Resultado (fichas com as datas de fim em ordem): janeiro 23 para 254 de 292; fevereiro 11 para 262 de 295; março 191 para 347 de 349. Ficam fora de ordem 73 fichas (para decisão) e 23 ainda sem alguma data (20 em janeiro, 3 em fevereiro).
- Desfazer: R2 e R4 limpar o campo; R3 voltar para 04:00:00Z do mesmo dia local; R1 pelos valores antigos (arquivo de desfazer e versões do item).
