# Plano B — Packing List manual (OP física que não chegou ao sistema) · MEL-236

Ideia do William (06/10/2026): se o operador não apontar a OP no sistema mas a OP existe no físico, a expedição não pode ficar sem packing list. Precisa de um caminho de emergência, visível e auditável.

## Desenho (a codificar)
1. Botão "Packing manual (OP fora do sistema)" no menu lateral da `scr_Finalização_1`, separado do Imprimir normal.
2. Modal: OP (8 dígitos) · mangueira (lista `colMangueiras` ou "outra") · lances (texto, uma metragem por linha, ponto ou vírgula, até 26, com contagem e total ao vivo) · motivo ("OP não chegou ao sistema", "Ficha extraviada", "Outro") · E-Number de quem imprime.
3. Confirmar: grava em `Packing_Manual` (Status "Pendente") e abre a `TelaImpressao` (A4 paisagem, já aprovada) com ID PALLET = OP digitada e tarja "PACKING MANUAL — SEM OP NO SISTEMA".
4. Visibilidade: selo na `scr_SelecaoGestao_1` ("N packings manuais pendentes", igual ao da Conferência); a supervisão marca "Regularizado" quando a OP entrar. A Conferência GMS × SAP × Packing já acusa lance sem OP.

## Lista SharePoint `Packing_Manual`
Title (OP, texto) · Mangueira (texto) · Lances (várias linhas; metragens separadas por ";") · TotalM (número) · Motivo (texto) · Responsavel (texto) · Turno (número) · Status ("Pendente" / "Regularizado") · DataHoraImp (data e hora).

## Decisões pendentes do William (com a recomendação)
1. Quem pode usar: qualquer operador com E-Number (recomendado; nunca trava a expedição e fica tudo registrado) ou só supervisão.
2. Lances: digitados à mão (recomendado) ou lidos por código de barras.
3. Alerta na Gestão a partir de N packings manuais por dia (recomendado: 3).

## Depende de
Lista `Packing_Manual` criada no SharePoint. Sem ela não há o que gravar.

## Revisão 06/10/2026 (William): sem modal, a própria TelaImpressao editável
O modal da Finalização foi removido. "Pack manual" abre a **TelaImpressao** em modo manual: a folha é a mesma, com campos editáveis por cima.
- Editáveis: OP (8 dígitos), PART-NUMBER, 26 lances (grade N° / QTY), operador (dropdown da lista Colaboradores) e motivo (dropdown).
- Não editável: DATE (hora de abertura da tela). Total e códigos de barras (Code 39) recalculam sozinhos.
- Ao imprimir a folha, os campos viram texto (sem caixas). Operador e motivo saem impressos no rodapé direito.
- **Nunca bloqueia**: se a OP já existe em `ficha_producao`, aparece só um aviso laranja na tela ("pode imprimir, fica registrado"), a tarja da folha vira "PACKING MANUAL" (sem "SEM OP NO SISTEMA") e a impressão é liberada. Se o registro em `Packing_Manual` falhar (rede), avisa e imprime mesmo assim.
- Reimprimir na mesma abertura atualiza o mesmo registro em `Packing_Manual` (não duplica).
