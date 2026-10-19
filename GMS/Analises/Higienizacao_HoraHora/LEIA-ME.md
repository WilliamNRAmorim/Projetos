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

## Aplicado em 19/10/2026
Gravado na lista Hora-Hora em lotes; cada item só era alterado se o `Modified` continuasse igual ao da leitura.
O que entrou está em `HoraHora_operacoes_a_aplicar_2026-09-01_a_2026-10-15.csv` (linhas ATUALIZAR e LIXEIRA):
27 Célula/Title (1 teste + 24 em lote; 2 viraram duplicados excluídos), 4 datas, 2 fusões de campos nos registros mantidos,
acumulados de 53 linhas e 69 duplicados enviados à lixeira do SharePoint (restauráveis).
Conferência depois da gravação: 3.955 itens (4.024 − 69), 0 Title≠Célula, 0 Data≠Title, 0 acumulados divergentes em 436 grupos de turno.
NÃO aplicados (decisão item a item): 33 duplicados com Real ou mangueira diferentes (linhas NAO_APLICADO_REVISAR) e 308 mangueiras
divergentes da OP (relatório de mudanças).
