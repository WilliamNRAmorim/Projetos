# Prompt para o GitHub Copilot: terminar a carga de 2021 (usando o navegador do próprio agente)

Cole o texto abaixo no Copilot (modo agente, com este repositório aberto). Ele deve usar o **navegador nativo dele** (a ferramenta de navegador do agente), do mesmo jeito que o Claude faz aqui: abrir a página, rodar JavaScript nela e ler o resultado. Ninguém precisa abrir o console nem colar código.

---

Tarefa: terminar de carregar o ano de 2021 na lista do SharePoint `Historico_Apontamento` (site https://danfoss.sharepoint.com/sites/OperationsGuaratingueta). Leia primeiro `GMS/Analises/Historico_Apontamento/PLANO_CARGA.md`.

**Situação (conferida em 05/11/2026 pela API)**
- A lista tem 16.781 itens, sem duplicatas. De 2021 existem os Title 8807 a 10406 (1.600 itens). **Faltam os Title 10407 a 13693 (3.287 linhas).** Não recarregue o que já existe.
- Fonte: `GMS/Analises/Historico_Apontamento/enc.json` (campo `rows`; o Title da linha N é N e a linha é `rows[N-1]`). Já deixei pronto `rows2021_falta.js` na mesma pasta: ele define `window.__R` com as 3.287 linhas que faltam (Title 10407 em `__R[0]`, Title 13693 em `__R[3286]`). Soma esperada só dessas linhas: QtdAprovada 1.747.013,6 e QtdReprovada 12.141,7.
- Totais esperados da faixa 8807–13693 inteira (4.887 itens): QtdAprovada 2.791.569,7 e QtdReprovada 20.470,1.

**Como fazer (tudo pelo seu navegador, sem me pedir para colar nada)**
1. Abra no seu navegador nativo uma página de `danfoss.sharepoint.com` (por exemplo `https://danfoss.sharepoint.com/sites/OperationsGuaratingueta/Lists/Historico_Apontamento/AllItems.aspx`). Os scripts precisam rodar **nessa origem**, senão o `fetch` para a API falha. Se cair no login da Microsoft, pare e me peça para entrar; não digite senha.
2. Use a ferramenta do seu navegador que executa JavaScript na página e devolve o resultado. Rode o conteúdo de `carregador.js` (ele define `__carregar(tituloInicial, arrayDeLinhas)` e `__conferir(a, b)`; grava por REST, 8 requisições em paralelo).
3. Rode o conteúdo de `rows2021_falta.js` (define `window.__R`). Se a sua ferramenta limitar o tamanho do script, divida em 3 partes de ~1.100 linhas, acumulando em `window.__R = (window.__R||[]).concat([...])`. Confirme `__R.length === 3287`.
4. Antes de gravar: `await __conferir(8807, 13693)` e confirme `n = 1600`. Se não for 1600, pare e me avise.
5. Grave em blocos de ~400 linhas: `await __carregar(10407, __R.slice(0,400))`, depois `__carregar(10807, __R.slice(400,800))`, e assim por diante (Title do bloco = 10407 + índice inicial). Cada chamada leva uns 20 s; não passe de ~800 linhas por chamada.
6. Se um bloco vier com `nerr > 0`, não repita o bloco: releia a lista, descubra quais Title da faixa ainda não existem e carregue só esses (senão duplica).
7. No fim: `await __conferir(8807, 13693)` deve dar `n: 4887`, `dup: 0`, `aprov: 2791569.7`, `rep: 20470.1`. Confira também que o total da lista é 20.068.
8. Se a sua ferramenta de navegador não executa JavaScript na página, ou não consegue manter a sessão logada, pare e me diga exatamente o que faltou; não peça para eu colar código no console.

**Regras (obrigatórias)**
- Só grave nessa lista. Nunca apague nada em definitivo (duplicados vão só para a lixeira da lista, e só com meu OK).
- Não mude `carregador.js`, `enc.json`, `rows2021_falta.js` nem as outras faixas de Title.
- Responda curto, em português.

**Ao terminar**
Atualize só a linha de 2021 da tabela `Progresso` em `PLANO_CARGA.md` (modelo: a linha de 2022: "CONCLUÍDO em <data>: Title 8807 a 13693 (4.887 itens, sem duplicatas), QtdAprovada 2.791.569,7 e QtdReprovada 20.470,1 conferidas com o CSV; lista com 20.068 itens"), faça commit só desse arquivo e do `rows2021_falta.js` se ainda não estiver commitado, `git pull --rebase --autostash origin main` e `git push origin HEAD:main`.
