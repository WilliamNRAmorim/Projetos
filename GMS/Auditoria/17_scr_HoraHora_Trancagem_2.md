# Auditoria 17 — scr_HoraHora_Trancagem_2 (v0.5.8 → v0.6.0) — TELA-PADRÃO dos Hora-Hora

Leitura linha a linha (2.379 linhas). Tela madura; geometria inalterada, QA sem novos achados. É o modelo para Mandril, Tubo, Cobertura e demais etapas de mangueira.

## Corrigido
- **Salvar rebaixava linha fechada:** depois de "Fechar turno" (Status = Finalizado), qualquer Salvar voltava a linha para Rascunho. Agora preserva Finalizado.
- **Real digitado fora de escala:** borda laranja quando Real passa da meta em mais de `fx_MargemMetragemPct` (10%) e aviso no rodapé; só aviso, não bloqueia (meta ausente nunca alerta).
- **Carga dos dados:** os 4 Refresh (Hora-Hora, ficha, DM_TRANÇAGEM, DM_ENGRENAGENS) agora em `Concurrent` com `IfError` e aviso; antes eram sequenciais e falhavam em silêncio.
- Data inicial por `fx_DataRefEm(Now())` (3º turno cruza a meia-noite) em vez de `Today()`; fonte do título por token.

## Mantido de propósito
- Sem auto-refresh: a tela guarda digitação não salva e recarregar apagaria.
- A data de referência é sempre a do momento atual: não dá para reabrir o 3º turno da noite anterior depois que o dia virou (limitação conhecida).
- Cancelar OP (descarte) não precisa de código aqui: a lista de OPs ativas filtra "Em processo", então OP "Cancelado" sai sozinha.

## Contrato do padrão (o que as outras telas Hora-Hora precisam ter)
Cabeçalho turno+célula+Abrir; faixa de pendências; grade `fx_GradeHoraHora` por turno; coluna Mangueira (combo da DM) com ↓ replicar; Real, Parado, Motivo, 2º motivo, Ação; Salvar (rascunho) e Fechar turno (bloqueado com pendência); quadro de pendências de todas as células; "turno sem produção"; gravação linha a linha com `colFalhasHHT` (não duplica); aviso de duplicados; timer de guarda de 90 s.
