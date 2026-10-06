# Auditoria 21 — scr_SelecaoGestao_1 (v0.2.0 → 0.3.0) e scr_ConferenciaSAP (v0.1.1 → 0.1.2)

Leitura linha a linha (451 e 1.114 linhas). Geometria inalterada; QA sem novos achados.

## scr_SelecaoGestao_1
Tela limpa. Só uma melhoria: selo no card da Conferência com o número de pendências abertas ("3 abertas" em vermelho, "Em dia" em verde, escondido se a consulta falhar). Um controle novo (`lbl_BadgeConfGest`) em área vazia do card.

## scr_ConferenciaSAP
- Carga das duas listas em `Concurrent` com `IfError` e aviso (antes falhava calada e a tela ficava vazia).
- Salvar tratativa e Justificar/Reabrir relêem o Status no servidor antes de gravar: se outra pessoa mexeu (ou a conferência da manhã fechou a pendência) enquanto a tela estava aberta, avisa e recarrega em vez de sobrescrever.
- Sem auto-refresh de propósito: recarregar apagaria a tratativa que está sendo digitada.

## Tirar a conferência do Power Automate (análise)
O motor não é o fluxo: é o Office Script que lê o MB51 inteiro (31 blocos de 20 mil linhas, ~600 mil linhas) e o BD Packing List (Excel sem tabela formatada). O Canvas App não lê esses arquivos e não aguenta esse volume; o fluxo só agenda e liga as pontas. Como o Painel da Célula, só dá para calcular dentro do app se as três fontes forem listas SharePoint pequenas:
1. GMS (ficha_producao, RegistrosInspeção, TiposErros): já são listas.
2. Packing: precisa que a cabine grave numa lista (hoje grava no Excel).
3. SAP: precisa chegar filtrado (só movimentos 101/102 do depósito GRT4, ~100 linhas/dia) numa lista, em vez do MB51 completo.
Com as três em lista, a conta (hoje no script) vira UDFs no Formulas.txt e a tela grava as pendências, sem fluxo agendado. Pergunta pendente para o William: a cabine do Packing pode passar a gravar em lista, e o SAP/supervisor consegue entregar o MB51 já filtrado como lista ou tabela?
