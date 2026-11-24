# Fluxos do Uiu v4 (criados em 24/11/2026, DPS - Non Prod)

| Fluxo | ID | Estado |
|---|---|---|
| Consultar GMS | `24f9a73a-fde7-f111-84e7-7ced8dc3b05d` | ativo, sem ligação com o Uiu |
| Ler linhas | `4043a040-fde7-f111-84e7-7ced8dc3b05d` | ativo, sem ligação com o Uiu |
| Perguntar ao BI | `831a9b46-fde7-f111-84e7-7ced8dc3b05d` | ativo, sem ligação com o Uiu |
| TESTE Uiu portão Power BI (temporário) | `a25ae3fd-64e7-f111-84e9-7ced8dc5f589` | desligado |

- Fonte única: `gerar_fluxos.py`. Os JSON são a saída dele; o que foi gravado no ambiente confere por hash.
- O Perguntar ao BI usa a referência de conexão `cra6eb_teste_uiu_powerbi`: **não apagar**.
- Só leitura: SharePoint só GET; Power BI só consulta.

## Resultado do lote (24/11, no fluxo temporário)
- 38 casos: 33 certos na primeira versão entre os 35 lidos; os 2 errados (consulta por OP sem data) foram corrigidos e passaram na confirmação, junto com os 3 que faltavam ler.
- Números iguais ao GABARITO_40.md: 1 a 22 e 23 (blocos sem total), 24, 25 e 26. `ops_em_processo` é foto do momento e o caso "Trançagem de outubro só GH781-8" (21.045 m) não tinham gabarito.
- Tempo por consulta: 13 a 40 s. Mês de Hora-Hora (4.442 linhas) em 26 s. Limite do agente: 100 s.
- Perguntar ao BI: SAP 7.915,86; Cabine 7.985,1 (igual ao Consultar GMS); aderência geral 68,0% em 13/11. Medida inexistente devolve o erro do Power BI; texto que não é consulta é recusado.
- Ler linhas: OP 30803591 certa; lista fora da permitida recusada; pedido de 900 linhas virou 50.

## Pendências antes de publicar
1. `perc_refugo` sem inspeção no recorte dá 100%: devolver nulo com aviso.
2. Testar 3 meses e um caso com `completo=false`.
3. Indicador `op` e "na etapa desde" (especificação, seção 4) ficaram fora: o modelo combina `inspecao_boa` e `refugo` com `op=` e usa Ler linhas para a ficha.
