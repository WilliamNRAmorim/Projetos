# Recuperado do branch de 07/10/2026

Arquivos trazidos em 31/10/2026 do branch `ccr-1735351a-pfguf1` do GitHub, que nunca entrou na `main`.

**Atenção: isto é histórico, não é a versão vigente.**
- As telas, o Diário e o Índice desse branch **não** foram trazidos. A `main` já mudou essas partes depois, e mesclar dava conflito em 10 arquivos.
- O que estas análises dizem sobre telas (ex.: `scr_ControleTrancagem_1`, `scr_DescartarOP_1`) pode não estar no app publicado. A verdade das telas continua sendo `GMS/Telas/`.
- Use como pista e confira contra `GMS/Telas/` e o `GMS_Diario.md` antes de aplicar qualquer coisa.

`gms_qa_patch.py` (auditoria MEL-009: Patch sem checagem de erro) roda nas telas atuais. Rode de dentro da pasta `GMS`:

```bash
python Analises/Recuperado_branch_2026-10-07/gms_qa_patch.py
```
