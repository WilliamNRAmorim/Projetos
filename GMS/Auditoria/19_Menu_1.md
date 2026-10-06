# Auditoria 19 — Menu_1 (508 → 489 linhas)

Leitura completa. Geometria inalterada, exceto a remoção do botão duplicado.

- **Falha aberta corrigida:** se a consulta de setor (`MapeamentoSetor`) falhasse, as variáveis de área ficavam em branco e o menu mostrava TODOS os cartões e botões. Agora cai em "Gestão" (só o Painel) e avisa.
- **Botão duplicado removido:** `btnSetoresMontagem_1` ficava 1 px acima de `btnSetoresMontagem`, com a mesma função.
- Data do cabeçalho sem `Today()` volátil (`ctxHoje` lido uma vez ao abrir).
- Cores/fonte de Image/Button migradas para tokens; sobram só os RGBA translúcidos do tema escuro do menu (sem token).

Mantido: nomes sem prefixo de tipo, ícone 'git-pull-request-draft' dos Setores Montagem (só ícones já importados; trocar quando importar a chave inglesa), rótulos de acessibilidade na rodada final.
