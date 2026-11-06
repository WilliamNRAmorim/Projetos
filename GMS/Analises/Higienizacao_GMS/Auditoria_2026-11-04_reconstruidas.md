# Auditoria: fichas reconstruídas de janeiro/2026 e limpeza correlata (04/11/2026)
Sem nomes e sem linhas de produção (listas completas em `C:\Users\U445131\Downloads\`).
## Gravação (aprovada pelo William)
- 59 fichas na `ficha_producao` (IDs 4268 a 4326): 3 de teste atualizadas e 56 criadas, 0 falhas, 0 OPs duplicadas, 0 campos divergentes do planejado na conferência. Total de itens: 3.087 (3.033 − 2 apagadas + 56).
- Regra: OP sem ficha no SAP/MB51 de janeiro (66 OPs de mangueira; 60 com ficha modelo da mesma mangueira; 59 gravadas; a de modelo a 46 dias e as 6 sem modelo ficaram de fora). Herdam da ficha modelo mangueira, bitola, compostos, trançadeira, defeitos e turnos; datas deslocadas em dias inteiros (horário preservado); turno por horário (NORMA); operador só entre os mais frequentes daquela etapa, turno e período (até 2 nomes); quantidade = saldo SAP (aprovado + reprovado) e cadeia anterior = seguinte + defeito; `Title = RECONSTRUIDA_SAP <OP>` e observação da trançagem avisando que é estimativa.
- Fluxos automáticos: nenhum disparado (contagens de Eventos_Producao, Historico_Carretel e Hora-Hora iguais ao antes).
- Desfazer: apagar os itens com Title começando em `RECONSTRUIDA_SAP` (lixeira 93 dias).
- BI: decisão do William (06/11): sem filtros, as fichas `RECONSTRUIDA_SAP` entram normalmente; `Created` dessas fichas é 04/11 (o mês certo vem das datas de fim).
## Outras ações do dia
- Fichas 4009 e 4138 (ativas com mangueira e máquina numéricas, defeito do app) apagadas para a lixeira a pedido do William (restauráveis em 93 dias).
- `GMS/PowerBI/modelo/limpeza_ficha_producao.m.md` corrigido: TE0/TE01 = Spiral (commit 0d3cb79).
## Extração estimada (aprovada: "Sim, as 112")
- 112 fichas de janeiro com `quantidade_extracao` vazia receberam a quantidade da última etapa preenchida (debandagem 86, vulcanização 16, bandagem 10) vezes 0,97; as 28 com última etapa em tubo, cobertura ou trançagem ficaram de fora (decisão pendente).
- Guarda: valor atual relido (vazio) e status Finalizado; 112 gravadas, 0 recusas, 0 falhas; conferência 112/112.
- Cobertura de janeiro contra o CP com as 59 reconstruídas incluídas: trançagem 85%, bandagem 96,6%, debandagem 86,8%, extração 88,4%.
