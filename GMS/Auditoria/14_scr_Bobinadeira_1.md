# Auditoria 14 — scr_Bobinadeira_1 (v0.4.1 → v0.5.0)

Leitura linha a linha das 3.312 linhas. Geometria (X/Y/Width/Height) inalterada em todos os controles; QA sem novos achados.

## Aplicado
- **Atualização automática da fila a cada 120 s** (`tmr_AutoRefreshBob`): só roda com operador ocioso (sem processamento e sem modal aberto); aciona o mesmo botão de refresh.
- **Refresh manual com aviso** se a rede falhar; **carga do delineamento (OnVisible) com IfError** e aviso claro.
- **Metragem (norma "sem enviar com metragem em branco/0")**: `fx_MetragemOk(fx_Num(...))` na borda do campo, no botão Concluir, no modal de conclusão e como trava dentro do OnSelect da confirmação.
- **Números digitados** passam a usar `fx_Num`/`fx_EhNum` (aceita "," e "."); Salvar Parcial e Concluir não gravam mais lixo/branco como 0 (gravam Blank).
- **Resumo do modal de conclusão** sem `Coalesce(x,0)`: mostra "—" quando vazio.
- **Fontes** `Font.Arial` / `Font.'Segoe UI'` trocadas por `fx_FonteFamilia`.

## Mantido de propósito
- Alerta de metragem fora da spec em 5% (aviso, não bloqueia). A margem de 10% da norma vale entre etapas, não contra o delineamento.
- Rótulo de versão em Courier New (convenção das telas).

## Pendente
- Acessibilidade (AccessibleLabel) na rodada final.
- Validar no Studio: Select(ico_RefreshBob_1) dentro do Timer.
