# Auditoria 18 — scr_HoraHora_Cobertura_1 (v0.1.0 → v0.2.0) + scr_Cobertura_2 (v0.3.2 → v0.3.3)

Leitura linha a linha (1.936 linhas). A tela já seguia o padrão da Trançagem (célula única "Cobertura", grade por turno, replicar, Fechar turno, falhas sem duplicar). Geometria inalterada nas duas telas; QA sem novos achados.

## Tela órfã resolvida
Nenhuma tela chamava o Hora-Hora da Cobertura. Em `scr_Cobertura_2` entrou o botão **Hora a Hora** no menu lateral (X 1168, Y 280, mesmo desenho do Tubo e do Mandril; ícone clock-3 já importado).

## Corrigido no Hora-Hora (mesmos achados da Trançagem)
- Salvar rebaixava linha já Finalizada para Rascunho; agora preserva.
- Real acima da meta em mais de 10%: borda laranja + aviso no rodapé (só aviso).
- Refresh de Hora-Hora e ficha em `Concurrent` com `IfError`; carga da velocidade (DM_EXTRUSAO_COBERTURA) com aviso se falhar (antes a meta ficava em branco sem explicação).
- Data inicial por `fx_DataRefEm(Now())`; fonte do título por token.

## Observação
Diferença para a Trançagem: não tem seletor de máquina nem quadro de pendências da célula, porque a Cobertura é uma célula só.
