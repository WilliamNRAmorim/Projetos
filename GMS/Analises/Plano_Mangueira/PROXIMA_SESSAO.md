# Plano de mangueira x SAP: estado em 23/11/2026

Modelo vivo **aplicado e conferido** (TMDL view 10:04–10:14, refresh 10:09). Falta só o William reabrir o `GMS_Painel.pbip` no Desktop, conferir a página e publicar.

- Lista `GMS_PlanoMangueira` com novembro: 45 itens, 162.016 m (gravado em 23/11 com o sim do William).
- Conferência no DAX query view (corte 20/11): plano 162.016; produzido no plano 96.576,8 = SAP Mangueira 96.576,8 (0 fora do plano); 59,6% do plano; ritmo 68,2% (15 de 22 dias com planejado na GMS_PlanoDiario); atraso 13.889 m; para fechar 9.348 m/dia (plano 7.364/dia); 0 medidas em erro.
- Correção feita ao aplicar: a Mangueira não tem mais linha na GMS_MetaMensal (usa a GMS_PlanoDiario). Dias úteis, dias restantes e ritmo passaram a contar os dias com planejado > 0, como a Máscara SAP.
- Revisão: feita pelo chefe a pedido do William (o agente revisor não carregou na sessão).
- Todo mês: o planejamento cola o bloco de mangueiras da planilha na lista (1 linha por mangueira e mês) e o refresh leva para a página.
