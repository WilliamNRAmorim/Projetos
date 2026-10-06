# Auditoria 15 — scr_RefugoBobinadeira_1 (v0.3.0 → v0.4.0)

Leitura linha a linha (892 linhas). Geometria inalterada; QA sem novos achados.

## Aplicado
- Quantidade refugada por `fx_EhNum`/`fx_Num` (aceita "," e "."), sem `Coalesce(x,0)`; vazio ou lixo bloqueia o Registrar e a borda fica vermelha.
- Carga inicial e botão atualizar com `IfError` e aviso (antes falhavam em silêncio).
- Formatos de quantidade com `[$-pt-BR]` (não dependem da cultura do tablet); mensagem de sucesso formatada.
- Observação com `Trim`; título com `fx_FonteFamilia`.

## Mantido
- Listas fixas de máquinas, fios e motivos (cadastro vem da Qualidade; mudar exige decisão do William). Tamanho 11 da coluna Operador na galeria (cabe no espaço atual).
- Sem auto-refresh: a tela é de lançamento, não de fila.
