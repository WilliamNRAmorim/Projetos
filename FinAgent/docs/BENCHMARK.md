# Benchmark FinAgent (2026-10-24)

Fonte: README/páginas públicas dos projetos (leitura rasa, sem auditar código). Licença decide o que dá para copiar: MIT = código com crédito; AGPL = só ideia; sem licença = só ideia.

## O que o FinAgent já tem
Início (insights + alertas), Gastos (tetos por categoria, "pra onde foi", busca, regras), Metas (reserva, limite do cartão, fatura/renda, plano de corte), Mercado (cotações + alertas), Economista (chat Gemini), Perfil, exportação para Claude. Tudo em AsyncStorage, sem servidor.

## Lacunas do FinAgent (mapa do explorador)
1. Backup/restauração (trocar de aparelho ou limpar dados perde tudo).
2. Contas a pagar e recorrências com tela própria e lembrete de vencimento.
3. Notificações do sistema (hoje só o sino dentro do app).
4. Multi-conta/carteiras (saldo é único).
5. Exportar CSV.
6. Metas de poupança com prazo (cofrinhos).
7. Sincronização incremental do Mercado Pago (hoje repagina até achar id conhecido).

## O que cada projeto faz de melhor
| Projeto | Licença | Melhor ideia | Vale trazer? |
|---|---|---|---|
| Nami (Expo/TS) | MIT | Carteiras (dinheiro, banco, cartão) + orçamento mensal + metas num app só | Sim: modelo de carteiras |
| RN-Budgetter | não informada | Categoria com cor/ícone, barra de progresso, rosca | Só ideia (FinAgent já tem barras e rosca) |
| Actual Budget | MIT | Local-first; orçamento por envelope; sync entre aparelhos | Ideia de envelope e de backup/sync; sync completo é grande demais |
| Firefly III | AGPL-3.0 | Regras automáticas, recorrências, cofrinhos, tags, relatórios | Só ideia: recorrências, cofrinhos, tags |
| Sure (fork Maybe) | AGPL-3.0 | Patrimônio líquido, fluxo de caixa, assistente de IA | Só ideia: tela de patrimônio líquido |

## Mercado Pago: melhor uso da API
- Hoje: `GET /v1/payments/search` paginado, sem filtro de data (o filtro `range=date_created&begin_date&end_date` é o que a documentação costuma trazer, mas NÃO confirmei na referência oficial; testar antes de usar).
- Relatório de Liberações (confirmado na documentação): `POST /v1/account/release_report` gera por período (assíncrono, 202); `GET` lista; baixa por nome do arquivo; `POST .../schedule` agenda (diário/semanal/mensal). Cobre dinheiro liberado, saques, estornos e disputas. Bom para conciliação do extrato.
- Webhooks avisam só o id; exigiriam servidor próprio. Descartado (o app deve rodar sem servidor).
- Limites de taxa: não achei números. Manter cache e recuo (backoff) em 429.
- Recomendação: manter `payments/search` incremental com data de corte guardada (em vez de repaginar), e usar o relatório de Liberações só quando precisar fechar o mês.

## Ordem proposta (para o William cortar ou mudar)
1. Backup e restauração (arquivo JSON, via compartilhar) — maior risco hoje.
2. Sync incremental do Mercado Pago com data de corte.
3. Contas a pagar/recorrências com vencimento + notificação local.
4. Carteiras (multi-conta) e patrimônio líquido.
5. Cofrinhos com prazo.
6. Exportar CSV.

Perguntas em aberto: fazer 4 muda o modelo de dados (passa pelo revisor).
