# Higienização da lista Hora-Hora · 01/09 a 15/10/2026 (MEL-243)

Gerado em 16/10/2026 por leitura da lista no SharePoint. **Nada foi aplicado.** Os dois CSVs ficam só neste computador
(dado de produção, fora do git por `.gitignore`).

- `HoraHora_backup_2026-09-01_a_2026-10-15.csv` — cópia de 4.024 itens (IDs 26000 a 30037) antes de qualquer mudança.
- `HoraHora_relatorio_mudancas_2026-09-01_a_2026-10-15.csv` — 566 mudanças propostas (Tipo, ID, Campo, Antes, Depois, Confiança, Motivo).

| Tipo | Linhas | Confiança | Regra |
|---|---|---|---|
| CELULA_TITLE | 27 | AUTO | Title ≠ Célula. A célula certa é a que NÃO tem a hora em outro registro; empate decide a OP da ficha_producao |
| DATA | 4 | AUTO | Data ≠ data do Title. Vale a data de produção pela criação (antes das 05:20 = dia anterior) |
| DUPLICADO | 102 | 21 AUTO (idênticos) · 81 REVISAR (conteúdo diferente) | Mesma data+turno+célula+hora. Fica o Finalizado, depois o mais completo, depois o mais recente; o outro vai para a lixeira |
| MANGUEIRA | 308 | REVISAR | Mangueira diferente da OP em processo na máquina naquela janela (ficha_producao). Sufixo -N e 2583-12 já tratados como a mesma mangueira |
| ACUMULADO | 125 | AUTO | Meta Acum, Real. Acum, Diferença e Rendimento recalculados na ordem das janelas do turno |

Aplicação (quando William aprovar a lista): PATCH em lotes pelo navegador logado, log por ID, duplicados para a lixeira
(restaurável), nunca exclusão permanente. 898 janelas não têm OP na ficha e não entram em MANGUEIRA.
