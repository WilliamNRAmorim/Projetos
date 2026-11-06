# Auditoria: padronização da coluna Trançadeira da ficha_producao (04/11/2026)
Aprovado pelo William ("Sim, as 13"), a pedido da sessão do volume diário (filtro Máquina do GMS_Painel). IDs e valores antigos ficam em `GMS/Analises/Tratamento_Ficha_2026-11/ficha_undo_2026-11-04_trancadeira.md`, fora do Git.
- Gravado: 13 itens, só o campo Trançadeira (`Tran_x00e7_adeira`): 10 padronizações (TH-02, TH-07, TH.05, TM-01, TM.01 e 5 TO-04), 2 para Spiral (TE0 e TE01, mangueira GH493-12, família que só roda na Spiral) e 1 inferência (T004 para TO04, mesma mangueira 6 de 6 na TO04 nas fichas vizinhas).
- Guarda: cada item relido antes e só gravado se o valor atual fosse o esperado. 0 falhas, 0 recusas.
- Conferência: 13/13 com o valor novo.
- Distribuição depois (3.033 itens): TH01 249, TH02 189, TH03 223, TH04 49, TH05 117, TH06 345, TH07 710, TM01 228, TM04 171, TO04 285, Spiral 442; resíduo: 23 vazios (18 Canceladas e 5 Aguardando ainda no mandril/tubo, sem máquina definida; legítimo) e 2 itens `1` e `4` (fichas ativas com mangueira também numérica, aguardam o William).
- Desfazer: voltar o campo ao valor antigo do arquivo de desfazer, ou restaurar a versão anterior do item (50 versões).
- Nota: `GMS/PowerBI/modelo/limpeza_ficha_producao.m.md` ainda trata TE0/TE01 como lixo (errado); é da sessão do BI, não alterado aqui.
