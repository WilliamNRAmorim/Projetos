# Prompt para o GitHub Copilot: carregar o Hora-Hora histórico (pré-GMS)

Cole o texto abaixo no Copilot (modo agente, com este repositório aberto). Ele usa o **navegador nativo dele** (a ferramenta de navegador do agente): abre a página, executa JavaScript nela e lê o resultado. Ninguém precisa abrir o console nem colar código.

---

Tarefa: carregar o histórico do Hora-Hora (de antes do GMS) na lista do SharePoint `HoraHora_Historico` (site https://danfoss.sharepoint.com/sites/OperationsGuaratingueta). A lista já existe e tem as colunas prontas; só falta gravar as linhas. Leia primeiro `GMS/Analises/Historico_HoraHora/PLANO_HORAHORA.md`.

**Material (tudo em `GMS/Analises/Historico_HoraHora/`)**
- `carregador_hh.js`: define `__carregarHH(linhas)` e `__conferirHH(tituloIni, tituloFim)`. Grava por REST, 8 requisições em paralelo. **O `__carregarHH` pula os Title que já existem na lista**, então repetir um bloco não duplica.
- `dados/hh_01.js` a `dados/hh_20.js`: 20 arquivos de até 2.000 linhas. Cada um faz `window.__R = [ ...linhas... ];`. O Title da linha é o primeiro valor dela (1 a 39.198).
- `hh_manifest.json`: para cada arquivo, a faixa de Title, o número de linhas e as somas esperadas de `real`, `meta` e `parado`. O campo `total` traz o total geral (39.198 linhas; real 1.811.514,39; meta 4.670.179,95; parado 918.099,70).
- Já estão gravadas na lista as linhas de Title 1 a 3 (teste). O resto falta.

**Como fazer (tudo pelo seu navegador, sem me pedir para colar nada)**
1. Abra no seu navegador nativo uma página de `danfoss.sharepoint.com` (por exemplo `https://danfoss.sharepoint.com/sites/OperationsGuaratingueta/Lists/HoraHora_Historico/AllItems.aspx`). Os scripts precisam rodar **nessa origem**, senão o `fetch` para a API falha. Se cair no login da Microsoft, pare e me peça para entrar; não digite senha.
2. Use a ferramenta do seu navegador que executa JavaScript na página e devolve o resultado. Rode o conteúdo de `carregador_hh.js` (uma vez por página carregada; se a página for recarregada, rode de novo).
3. Para cada arquivo de `hh_01.js` a `hh_20.js`, em ordem:
   a. Rode o conteúdo do arquivo (define `window.__R`; se a sua ferramenta limitar o tamanho do script, divida em 2 partes e acumule com `window.__R = (window.__R||[]).concat([...])`). Confirme `__R.length` = `linhas` do manifesto.
   b. Grave em blocos de ~500 linhas: `await __carregarHH(__R.slice(0,500))`, `__R.slice(500,1000)`, `__R.slice(1000,1500)`, `__R.slice(1500)`. Cada chamada leva uns 20 s; não passe de ~700 linhas por chamada.
   c. Se algum bloco vier com `nerr > 0`, rode o mesmo bloco de novo (ele só grava o que falta).
   d. Confira: `await __conferirHH(titulo_ini, titulo_fim)` deve dar `n` = linhas do manifesto, `dup: 0` e `real`, `meta` e `parado` iguais aos do manifesto (diferença de até 0,05 por arredondamento). Se não bater, pare e me avise com os números.
4. No fim: `await __conferirHH(1, 39198)` deve dar `n: 39198`, `dup: 0`, `real: 1811514.39`, `meta: 4670179.95`, `parado: 918099.7` e `totalLista: 39198`.
5. Se a sua ferramenta de navegador não executa JavaScript na página, ou não consegue manter a sessão logada, pare e diga exatamente o que faltou; não peça para eu colar código no console.

**Regras (obrigatórias)**
- Só grave nessa lista (`HoraHora_Historico`). **Não toque na lista `Hora-Hora`** (a do app) nem em qualquer outra. Nunca apague nada em definitivo (duplicado só vai para a lixeira da lista, e só com meu OK).
- Não mude `carregador_hh.js`, `dados/*` nem `hh_manifest.json`.
- Responda curto, em português.

**Ao terminar**
Atualize só a tabela `Progresso` do `PLANO_HORAHORA.md` (marque cada arquivo como concluído com a data e a conferência), faça commit só desse arquivo (liste o que está staged antes: não use `git add` em pasta), `git pull --rebase --autostash origin main` e `git push origin HEAD:main`.
