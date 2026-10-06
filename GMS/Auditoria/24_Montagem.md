# Auditoria 24 — Montagem: scr_selecaosetor_Montagem e scr_Montagem_HoraHora

Leitura linha a linha (593 e 1.831 linhas). Geometria inalterada nas duas; QA sem novos achados. Nota: `scr_selecaosetor_Montagem` é o menu novo (o diário o chamava de scr_SelecaoMontagem_2).

## scr_Montagem_HoraHora
- **Fecha o MEL-195:** o literal "TE - Tempo Excedido" (20 ocorrências, inclusive na lista de motivos) virou `fx_MotivoTempoExcedido`; a conta do real líquido (2 trechos repetidos nas cores e 1 no texto) virou `fx_RealMontagemMin`. O menu e o Hora-Hora passam a usar a MESMA conta.
- **Bug do rótulo:** toda linha de lançamento mostrava "…Turno" colado no P/N ("FC735-08Turno"). Agora só mostra o turno quando a OT é de outro turno.
- **Finalizar OT com travas:** relê o Status no servidor; se a OT já foi finalizada em outro tablet, avisa e fecha o quadro em vez de gravar por cima.
- **Números por `fx_Num`/`fx_EhNum`** (vírgula e ponto, inválido não vira 0): quantidade da OT, tempo parado e quantidade produzida. OT segue por `Value` (8 dígitos).
- **Falha de rede:** carga, timer e botão atualizar com `IfError`; o cabeçalho mostra "⚠ sem conexão".
- Fonte do título por token.

## scr_selecaosetor_Montagem
- Falha de Refresh deixa de parecer tudo certo: o subtítulo vira "⚠ Sem conexão com o servidor — dados das HH:MM".

## Não mexido
- Barcode readers invisíveis (Visible=false): decisão anterior, depende do tablet.
- OT aberta em outra célula não bloqueia o início (só a mesma célula): precisa de regra do William.
