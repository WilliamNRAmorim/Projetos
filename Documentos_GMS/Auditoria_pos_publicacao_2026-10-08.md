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

## Rodada 2 (navegador)
- Versions: Live agora é a **v648** (08/10 11:44), publicada pelo William. Antes a Live era a v646.
- MEL-231: só o fluxo Monitor Solda Mandril escreve em Estado_Trancadeiras. O app (scr_Monitor_Mandril) só faz Refresh/ClearCollect, sem Patch. Nas últimas 51 versões de cada um dos 10 itens só aparecem Produzindo e SemPlano; "Manutencao" não foi gravado por ninguém. Desligar o fluxo exige a tela calcular o estado (proposta em MEL-231_Monitor_Mandril_sem_PowerAutomate.md).
- Power Automate: 5 fluxos na conta (Conferencia_Diaria, AutoResfriamentoVulca, PackListParaFicha, Conceder Acesso GMS, Monitor Solda Mandril).
- Studio não carregou (tela "Loading" por mais de 40 s); a conferência do btn_ImprimirExt na Live ficou para quando abrir.
