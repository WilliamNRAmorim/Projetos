# Carga da lista Historico_Apontamento (plano por sessões)

Objetivo: levar para o BI o apontamento de produção que não está no GMS (2018 a 2026), numa lista do SharePoint
`Historico_Apontamento` (site OperationsGuaratingueta). Decisão do William (30/10 e 03/11/2026): carregar **em blocos, um ano por sessão**,
para não pesar o contexto. Prioridade: 2025.

## Arquivos
- `Historico_Apontamento_carga_completa.csv`: 29.049 linhas, ordenadas por data (fonte da verdade da carga).
- `enc.json`: as mesmas linhas codificadas (`M` = lista de mangueiras; `rows` = uma string por linha). Gerado por `enc.py` (copie de
  `scratchpad` se precisar; a lógica está abaixo).
- Linhas por ano (número da linha = campo `Title` do item, 1 a 29049): 2018: 1-2138 · 2019: 2139-6064 · 2020: 6065-8806 · 2021: 8807-13693 ·
  2022: 13694-18138 · 2023: 18139-21675 · 2024: 21676-24868 · 2025: 24869-28874 · 2026: 28875-29049.
- Origem dos dados: planilhas em `origem/` (2019 a 2024) e `Refugo/Apontamento de Produção de Mangueiras 2025-2026.xlsm` (2025 e 2026, só OPs que o GMS não tem).

## Codificação da linha (`enc.json`)
`dias,turno,idxMangueira,OP,aprovado,defeitos,reprovado,extras` — `dias` = dias desde 01/01/2018; `defeitos` = letra+valor colado (ex.: `A0.5O1`);
`extras` = `CO15~MIGO~numeroDelivery` (só 2025/26). Valores arredondados a 2 casas.

## Colunas da lista
Title (nº da linha) · Data (data) · Turno (nº) · OP · Mangueira · QtdAprovada · Defeito_A..Defeito_P · QtdReprovada · CO15 · MIGO · Delivery.

## Estado em 03/11/2026
Lista `Historico_Apontamento` CRIADA com todas as colunas; teste de 3 linhas OK. Ferramentas prontas nesta pasta: `carregador.js` (colar no `javascript_tool`;
define `__carregar(tituloInicial, linhas)` e `__conferir(a,b)`), `bloco.py` (imprime as linhas codificadas de um bloco com a soma esperada) e `enc.py`.
O nome interno da coluna CO15 e `OData__x0043_O15` (o carregador ja trata).
Blocos de ~600 linhas por chamada; depois de cada bloco rode `__conferir` e compare com a soma que o `bloco.py` imprimiu.

## Como carregar um ano (cada sessão)
1. Navegador do app em `danfoss.sharepoint.com` (se pedir login, é com o William). Ler `Progresso` abaixo.
2. Reler a lista pela API: contar itens do ano (filtrar `Title` por faixa) para não duplicar; só carregar o que falta.
3. Enviar os blocos por `$batch` (cerca de 100 itens por requisição), blocos de ~1.000 linhas por chamada do `javascript_tool`.
4. Conferir: contagem do ano = linhas do ano; soma de `QtdAprovada` e `QtdReprovada` igual à do CSV.
5. Atualizar `Progresso`, commit só dos arquivos do assunto, `pull --rebase --autostash`, push na main.

Regras: nunca apagar em definitivo (só lixeira); um "sim" do William vale para uma ação; a pasta `Historico_Apontamento_carga` na biblioteca
`Manufatura` está vazia e vai para a lixeira ao fim.

## Progresso
| Ano | Linhas | Status |
|---|---|---|
| 2025 | 4.006 | CONCLUÍDO em 03/11/2026: Title 24869 a 28874 (4.006 itens, sem duplicatas), QtdAprovada 1.837.314,9 e QtdReprovada 7.195,5 conferidas |
| 2026 | 175 | pendente |
| 2024 | 3.193 | CONCLUÍDO em 03/11/2026: Title 21676 a 24868 (3.193 itens, sem duplicatas), QtdAprovada 2.012.173,3 e QtdReprovada 27.675,2 conferidas com o CSV; lista com 7.199 itens |
| 2023 | 3.537 | CONCLUÍDO em 04/11/2026: Title 18139 a 21675 (3.537 itens, sem duplicatas), QtdAprovada 2.308.208,9 e QtdReprovada 8.440,3 conferidas com o CSV; lista com 10.736 itens |
| 2022 | 4.445 | CONCLUÍDO em 04/11/2026: Title 13694 a 18138 (4.445 itens, sem duplicatas), QtdAprovada 2.536.867,0 e QtdReprovada 9.382,3 conferidas com o CSV; lista com 15.181 itens |
| 2021 | 4.887 | pendente |
| 2020 | 2.742 | pendente |
| 2019 | 3.926 | pendente |
| 2018 | 2.138 | pendente |
