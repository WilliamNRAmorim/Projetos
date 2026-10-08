# Auditoria pós-publicação (08/10/2026, durante o almoço do William)

Somente leitura. Nada foi alterado no app, nos fluxos ou no SharePoint.

## Packing_Pallets
- 29 linhas (28 reconstruídas 06-08/10 + OP 30424228). Nenhuma linha nova gravada pelo app ainda (última Id 29, 08/10 13:29Z).
- Fichas Finalizadas modificadas hoje sem linha em Packing_Pallets: **3884 / OP 30421665** (Modified 13:49Z, antes da publicação da nova versão).
  Ação: reimprimir pela Finalização na versão publicada. O bloco do pallet 1 registra sozinho; ou o William confirma se foi packing manual.

## Pendências por MEL
- MEL-239: encerrada (diário). Reabre se o app não gravar linha ao imprimir; falta indexar FichaID.
- MEL-237: subir PDFs em PackLists, chamar GMS_PackListParaFicha depois do Print() (só com aprovação do William), bipar 1 PDF de cada pasta.
- MEL-240: fluxo validado por REST em 08/10 (5 OPs com +110 min exatos); falta o teste do William no app (badge Resfriando).
- MEL-231: antes de desligar o fluxo do Monitor Mandril, descobrir quem grava Status=Manutencao em Estado_Trancadeiras.
