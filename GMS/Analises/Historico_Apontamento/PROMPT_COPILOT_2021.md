# Prompt para o GitHub Copilot: terminar a carga de 2021

Cole o texto abaixo no Copilot (modo agente, com este repositório aberto).

---

Tarefa: terminar de carregar o ano de 2021 na lista do SharePoint `Historico_Apontamento` (site https://danfoss.sharepoint.com/sites/OperationsGuaratingueta). Leia primeiro `GMS/Analises/Historico_Apontamento/PLANO_CARGA.md`.

**Situação**
- A lista tem as linhas de 2021 com Title 8807 a 10406 (1.600 itens). **Faltam Title 10407 a 13693 (3.287 linhas).** Não recarregue o que já existe.
- Fonte das linhas: `GMS/Analises/Historico_Apontamento/enc.json` (campo `rows`, uma string por linha; o Title da linha N é N, e `rows[N-1]` é a linha). Faixa total de 2021 = `rows[8806:13693]`.
- Totais esperados da faixa 8807–13693 inteira (4.887 itens): QtdAprovada 2.791.569,7 e QtdReprovada 20.470,1.

**Como gravar**
1. Gere um arquivo `rows2021_falta.json` com `rows[10406:13693]` (use `python -I -X utf8`).
2. Eu abro no meu navegador uma página de `danfoss.sharepoint.com` já logado, abro o console (F12) e colo o conteúdo de `carregador.js`. Ele define `__carregar(tituloInicial, arrayDeLinhas)` e `__conferir(a, b)`. Ele grava via REST (`/_api/web/lists/getbytitle('Historico_Apontamento')/items`), 8 requisições em paralelo.
3. Para passar as linhas ao console sem digitar: gere um arquivo `.js` que comece com `window.__R = [ ...as 3.287 linhas como strings... ];`. Eu colo no console (pode ser em 3 partes de ~1.100 linhas se for grande demais).
4. Antes de gravar, no console: `await __conferir(8807, 13693)` e confirme que n = 1600. Se não for 1600, pare e me avise.
5. Grave em blocos de ~400 linhas, sempre `await __carregar(<Title da primeira linha do bloco>, __R.slice(a, b))`. Primeiro bloco: `__carregar(10407, __R.slice(0, 400))`; depois 10807 com `slice(400, 800)`, e assim por diante. Cada chamada leva uns 20 s; não passe de ~800 linhas por chamada (o console pode estourar o tempo).
6. Se algum bloco vier com `nerr > 0`, não repita o bloco inteiro: releia a lista, descubra quais Title da faixa ainda não existem e carregue só esses (senão duplica).
7. No fim: `await __conferir(8807, 13693)` deve dar `n: 4887`, `dup: 0`, `aprov: 2791569.7`, `rep: 20470.1`.

**Regras (obrigatórias)**
- Só grave nessa lista. Nunca apague nada em definitivo (duplicados vão só para a lixeira da lista, e só com meu OK).
- Se cair no login da Microsoft, pare e me peça para entrar. Não digite senha.
- Não mude `carregador.js`, `enc.json` nem as outras faixas de Title.
- Responda curto, em português.

**Ao terminar**
Atualize só a linha de 2021 da tabela `Progresso` em `PLANO_CARGA.md` (modelo: a linha de 2022: "CONCLUÍDO em <data>: Title 8807 a 13693 (4.887 itens, sem duplicatas), QtdAprovada 2.791.569,7 e QtdReprovada 20.470,1 conferidas com o CSV; lista com 20.068 itens"), faça commit só desse arquivo, `git pull --rebase --autostash origin main` e `git push origin HEAD:main`.
