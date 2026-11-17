# Passo a passo: criar a lista, o Flow e publicar o kill switch "Composto"

Guia prático pra você executar no SharePoint, Power Automate e Power Apps Studio. O código já está
pronto em `Telas/` (ver `Plano_KillSwitch.md`); aqui é só a parte que só você pode fazer.

## 1. Criar a lista SharePoint `Composto`

1. Abra o mesmo site SharePoint onde estão as outras listas do GMS (`ficha_producao`,
   `MapeamentoSetor` etc.).
2. **+ Novo → Lista → Lista em branco**. Nome: `Composto`.
3. Adicionar colunas:
   - `Ativo` — tipo **Sim/Não**. Valor padrão: **Sim**.
   - `DataBloqueio` — tipo **Data e hora** (inclua a hora, não só a data). Valor: **06/01/2027 13:59**.
   - `Mensagem` — tipo **Uma linha de texto** (ou **Várias linhas**, sem formatação). Deixe em branco
     por agora, ou já escreva o texto que vai aparecer quando bloquear (ex.: "Acesso ao GMS encerrado —
     fale com o William").
4. Crie **um único item** na lista com esses 3 valores preenchidos.
5. **Quebrar herança de permissão** (importante — sem isso qualquer operador pode desligar o mecanismo):
   - Na lista `Composto`: **Configurações (engrenagem) → Configurações da lista → Permissões para
     esta lista**.
   - **Parar de herdar Permissões**.
   - Deixe **Colaborar/Editar** só para você (William). Para os demais (grupo dos operadores), deixe
     **Leitura** — ou nenhum acesso, já que a conexão do Flow vai ser a sua, embutida (ver seção 2),
     então os operadores nem precisam ler a lista diretamente.

## 2. Criar o Flow `Flow_Composto` (Power Automate)

1. **Power Automate → Criar → Flow de nuvem instantâneo**.
2. Gatilho: **PowerApps (V2)**.
3. Nome do fluxo: `Flow_Composto`.
4. Ação: **SharePoint → Obter itens**.
   - Endereço do site: o mesmo site da lista `Composto`.
   - Nome da lista: `Composto`.
   - **Top Count**: `1`.
   - **Conexão**: confirme que está usando **a sua conta** (William) — essa é a conexão embutida que o
     plano pede, pra os operadores não precisarem de acesso à lista.
5. Ação: **Condição** (ou **Switch**), com esta lógica (seção 2 do `Plano_KillSwitch.md`):
   ```
   item = first(outputs('Obter_itens')?['body/value'])

   Se item é nulo -> permitido = false
   Senão se not(equals(item?['Ativo'], true)) -> permitido = false
   Senão se item?['DataBloqueio'] é nulo -> permitido = false
   Senão se greaterOrEquals(ticks(utcNow()), ticks(item?['DataBloqueio'])) -> permitido = false
   Senão -> permitido = true
   ```
   Pode montar como `Condição` simples encadeada ou como expressão única num `Compor`; o importante é
   não usar `convertFromUtc` (o conector já devolve a data em UTC).
6. Ação final: **Responder a um PowerApp ou fluxo**, com duas saídas:
   - `permitido` — tipo **Sim/Não**, valor = o resultado da lógica acima.
   - `mensagem` — tipo **Texto**, valor = `item?['Mensagem']` (ou texto fixo se `item` for nulo).
7. Salvar. **Ligar o Flow** (Status = Ativado).

### Testar antes de publicar

1. No próprio editor do Flow, **Testar → Manualmente**, preenchendo um valor de teste pro gatilho
   PowerApps (ele pede, mesmo sem o app ainda).
2. Confira na execução: o valor de `DataBloqueio` que chegou do SharePoint deve aparecer como
   `2027-01-06T16:59:00Z` (16:59 UTC = 13:59 Brasília). **Se vier diferente**, o site SharePoint não está
   no fuso de Brasília que você confirmou no plano — me avise antes de publicar o app, porque o corte vai
   acontecer na hora errada.
3. Teste também com `Ativo = Não` na lista, e confirme que a resposta vem `permitido: false`.
4. Volte `Ativo = Sim` depois do teste.

## 3. Publicar no Power Apps Studio

**Antes de tudo:** no Studio, adicione o Flow `Flow_Composto` como fonte de dados do app (painel
Dados → Adicionar dados → Power Automate → selecionar `Flow_Composto`), senão as fórmulas que o
`executor` escreveu não vão reconhecer `Flow_Composto.Run()`.

Depois, cole/aplique nesta ordem (os `.txt` já estão prontos em `Telas/`, cada um com o patch
correspondente):

1. **`App.OnStart`** — cole o conteúdo de `Telas/OnStart.txt`.
2. **`App.BackEnabled`** — cole o conteúdo de `Telas/BackEnabled.txt`.
3. **Tela nova `scr_Composto`** — crie a tela e aplique `Telas/scr_Composto.txt`.
4. **As 23 telas com gate+Timer** — para cada uma, abra o `OnVisible` e o Timer novo
   (`tmr_Composto_<NomeDaTela>`) a partir do `.txt` correspondente em `Telas/`. Lista completa na seção
   3.2 do `Plano_KillSwitch.md`.
5. Rode o **App Checker** do Studio (ícone de verificação) — deve dar zero erros novos.
6. **Salvar e Publicar.**

## 4. Testar depois de publicar

1. Abra o app num tablet real (ou no navegador) com `Ativo = Sim` e `DataBloqueio` no futuro —
   confirme que tudo carrega normal.
2. Mude `Ativo` para **Não** na lista, abra o app de novo (ou espere o Timer de até 30 min numa sessão
   já aberta) — confirme que cai em `scr_Composto` com a mensagem certa.
3. Nessa tela de bloqueio, aperte o **botão voltar do Android** — confirme que **não sai** da tela
   (é o que o `App.BackEnabled` deve garantir).
4. Volte `Ativo = Sim`, **feche e reabra o app** (reativação exige isso, conforme o plano) — confirme
   que volta a funcionar normal.
5. Deixe assim: `Ativo = Sim`, `DataBloqueio = 06/01/2027 13:59` — é o estado final até o dia do corte.

## 5. No dia 06/01/2027

Nada a fazer — o corte é automático. Se quiser adiar, troque `DataBloqueio` na lista pra uma data
futura antes das 13:59 desse dia. Se quiser reativar depois do corte, mude `DataBloqueio` para o futuro
ou `Ativo = Sim` com data futura — cada tablet precisa reabrir o app pra voltar a funcionar.
