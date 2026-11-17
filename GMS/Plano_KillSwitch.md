# Plano: Kill Switch do GMS (validação externa via SharePoint) — codinome "Composto"

Status: **APROVADO pelo revisor no quarto passe (Opus, esforço alto, 17/11/2026), com ressalvas de forma
(sem problema grave) e 1 decisão final do William já respondida (rodada 4).** Pronto para ir ao
`executor`. Nada foi implementado no Power Apps/Power Automate ainda.

Nomenclatura (a pedido do William): todo o mecanismo — lista, Flow e variáveis — usa o codinome
**Composto** em vez de nomes como "ConfiguracaoApp"/"Validacao"/"Permissao".

## Histórico de decisões do William

**Rodada 1 (17/11/2026):**
1. Se o Flow falhar: **bloqueia** (fail-safe).
2. Corte: **06/01/2027 13:59** horário de Brasília.
3. Escopo de telas: aceita ajustar as telas de produção (fechado na rodada 2/3 — ver abaixo).
4. Timer: **30 minutos**.
5. Perder digitação ao bloquear no meio do uso: **aceito**.
6. Permissão da lista: **só o William edita**.
7. Reativar exige reabrir o app: **aceito**.
8. Diário: linha **DECISÃO**, não NORMA.

**Rodada 2 (17/11/2026, após 2ª reprovação):**
9. Gate/Timer em **todas as telas com `Patch`/`SubmitForm` + `Menu_1`** — cobertura completa.
10. Conexão do `Flow_Composto`: **a do William, embutida no Flow**.
11. Site SharePoint da lista `Composto`: **confirmado no fuso de Brasília (UTC-03:00)**.
12. Autorizado trocar `App.BackEnabled` para bloquear o botão voltar saindo de `scr_Composto`.

**Rodada 3 (17/11/2026, após 3ª reprovação):**
13. **Painéis de TV** (`scr_PainelCelula_1`, `scr_PainelMontagem_1`, `scr_Monitor_Mandril`) — **ficam de
    fora** do bloqueio (não têm `Patch`, continuam exibindo depois do corte até alguém fechar o app
    manualmente).
14. **Falha passageira do Flow** (ex.: 1s de instabilidade de rede): **aceito como está** — qualquer
    falha bloqueia (decisão 1) e só sai reabrindo o app, sem Timer de recuperação extra.
15. **Telas de `Moldes/` (`scr_HoraHora_Mandril_2`, `scr_HoraHora_Tubo_2`) e `scr_Trancagem_3`**: William
    vai checar no Studio quais estão publicadas de fato — fica como pendência do `executor` confirmar
    antes de aplicar (ver seção 6).

**Rodada 4 (17/11/2026, após aprovação com ressalvas):**
16. **6 telas de leitura** (`scr_SelecaoGestao_1`, `scr_ConsultaOP_1`, `scr_FichaImpressao`,
    `scr_FichaTecnica_1`, `scr_HistoricoTurno_Tubo`, `scr_HistoricoTurno_Mandril`) — **ficam de fora**
    do bloqueio, igual aos painéis de TV (recomendação do revisor: não escrevem no SharePoint, e quem
    reabrir o app depois do corte é sempre barrado).

## Objetivo

Mecanismo de desligamento remoto do app GMS (Power Apps), controlado por uma lista do SharePoint, sem
precisar republicar o app nem o Flow para ativar/desativar. Corte definitivo em **06/01/2027 às 13:59**
(horário de Brasília) — depois dessa data a operação migra para outro sistema.

## 1. Lista SharePoint `Composto`

| Campo | Tipo | Observação |
|---|---|---|
| `Ativo` | Sim/Não (Yes/No) | Chave principal: Não = bloqueia na hora |
| `DataBloqueio` | Data e hora | **06/01/2027 13:59**, horário de Brasília |
| `Mensagem` | Texto | **William digita aqui manualmente** o texto de bloqueio |

Um único item na lista. Herança de permissão quebrada: edição só para o William (decisão 6). Conexão do
Flow embutida (decisão 10) — operadores não precisam de acesso à lista.

## 2. Flow `Flow_Composto` (Power Automate)

- Gatilho: **Power Apps (V2)**. Conexão: **do William**, embutida (decisão 10).
- Ação: `Obter itens` em `Composto`, `Top Count = 1`.
- Lógica (Condição), comparando em **UTC** (confirmado correto no 3º passe — o conector do SharePoint já
  devolve a data em UTC; o fuso só importa na hora de digitar o valor na lista):
  ```
  item = first(outputs('Obter_itens')?['body/value'])

  Se item é nulo -> permitido = false                              (lista vazia)
  Senão se not(equals(item?['Ativo'], true)) -> permitido = false  (Ativo=Não OU vazio)
  Senão se item?['DataBloqueio'] é nulo -> permitido = false        (tratamento explícito — ticks(null) erraria)
  Senão se greaterOrEquals(ticks(utcNow()), ticks(item?['DataBloqueio'])) -> permitido = false
  Senão -> permitido = true
  ```
- Resposta ao Power Apps: `{ "permitido": <Sim/Não>, "mensagem": "texto opcional" }`.
- **Teste antes de publicar:** rodar o Flow uma vez com `DataBloqueio = 06/01/2027 13:59` e confirmar que
  o valor chega como `2027-01-06T16:59:00Z` (16:59 UTC = 13:59 Brasília). Se o perfil do William no
  SharePoint usar outro fuso ao digitar, o valor gravado muda — confirmar na prática, não só no plano.

## 3. Power Fx — onde entra no app

### 3.1 `App.OnStart` — com tratamento de falha

A validação entra **antes** dos três `Set` iniciais (`varMapa`, `varAcessoRestrito`, `varCelulaMontagem`)
e do bloco `Concurrent(...)` que já existem em `Telas/OnStart.txt`:

```powerfx
IfError(
    With(
        {resComposto: Flow_Composto.Run()},
        Set(varCompostoPermitida, resComposto.permitido);
        Set(varCompostoMensagem, resComposto.mensagem)
    ),
    Set(varCompostoPermitida, false);
    Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
);

If(varCompostoPermitida,
    Set(varMapa, LookUp(MapeamentoSetor, EmailComputador = User().Email));
    Set(varAcessoRestrito, Coalesce(varMapa.AcessoRestrito, false));
    Set(varCelulaMontagem, varMapa.Celula);
    Concurrent(
        ClearCollect(colTrancadeiras, [...]),
        ClearCollect(colMangueiras, ...),
        ClearCollect(Turno, ["1", "2", "3"]),
        ClearCollect(colDM_MANDREL, DM_MANDREL),
        ClearCollect(colDM_BANDAGEM, DM_BANDAGEM),
        ClearCollect(colDM_LAYLINE, DM_LAYLINE)
    );
    ClearCollect(colMangEscTubo, colMangueiras, {NomeMangueira: fx_MangueiraOutra})
)
```

Sintaxe alinhada ao padrão já usado no app (`If(cond, a; b; c)`, como em `TelaImpressao`), sem parênteses
extras ao redor do bloco encadeado (achado do 3º passe).

### 3.2 Gate + Timer no `OnVisible` de cada tela afetada

`App.StartScreen` é uma propriedade que só *retorna* qual tela abrir — não aceita `Navigate()` e pode
rodar antes de `varCompostoPermitida` existir. Por isso o gate vai no `OnVisible` de cada tela de
destino, não no `StartScreen`.

**Telas afetadas (fechado no 3º passe, contadas em `Telas/*.txt`, fora `_colar`/`_patch`):**
`scrHoraHora_Mandril`, `scrHoraHora_Tubo`, `scr_AMDM02_Trancagem_1`, `scr_Bandagem_1`,
`scr_Bobinadeira_1`, `scr_Catenaria_1`, `scr_Cobertura_2`, `scr_ConferenciaSAP`, `scr_Debandagem_2`,
`scr_ExtrusoraMandril_1`, `scr_Finalização_1`, `scr_HoraHora_Cobertura_1`, `scr_HoraHora_Trancagem_2`,
`scr_mandril_1`, `scr_Montagem_HoraHora`, `scr_RefugoBobinadeira_1`, `scr_Trancagem_4`, `scr_tubo_1`,
`scr_Vulcanizacao_1`, `TelaImpressao` (20 telas) **+ `Menu_1`** (21 no total) **+ `scr_selecaosetor_1`**
e **`scr_selecaosetor_Montagem`** (achado do 3º passe: ficavam sem gate, mostrando dado ao vivo antes do
operador escolher a tela — 23 no total).

**Pendência do executor (decisão 15):** confirmar no Studio se `scr_HoraHora_Mandril_2`,
`scr_HoraHora_Tubo_2` (pasta `Moldes/`) e `scr_Trancagem_3` (referenciada em `StartScreen.txt` mas sem
arquivo em `Telas/`) estão publicadas; se sim, entram na lista acima antes de implementar.

**Decisão 13: painéis de TV (`scr_PainelCelula_1`, `scr_PainelMontagem_1`, `scr_Monitor_Mandril`) ficam
de fora. Decisão 16: as 6 telas de leitura (`scr_SelecaoGestao_1`, `scr_ConsultaOP_1`,
`scr_FichaImpressao`, `scr_FichaTecnica_1`, `scr_HistoricoTurno_Tubo`, `scr_HistoricoTurno_Mandril`)
também ficam de fora**, pelo mesmo motivo: não escrevem no SharePoint, e reabrir o app depois do corte
já barra o acesso.

Cada tela também ganha um `Timer` oculto, com **nome único** `tmr_Composto_<NomeDaTela>` (prefixo `tmr_`
do Mestre + sufixo por tela — 23 nomes distintos, evita conflito de nome de controle no app):

```powerfx
// tmr_Composto_<NomeDaTela> — Duration = 1800000 (30 min); AutoStart = true; Repeat = true
// OnTimerEnd:
IfError(
    With(
        {resComposto: Flow_Composto.Run()},
        Set(varCompostoPermitida, resComposto.permitido);
        Set(varCompostoMensagem, resComposto.mensagem)
    ),
    Set(varCompostoPermitida, false);
    Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
);
If(!varCompostoPermitida, Navigate(scr_Composto))
```

**Limite aceito (decisão 14, consistente com o 3º passe):** o Timer de uma tela só conta enquanto ela
está visível (`AutoPause` padrão). Quem alterna entre telas antes de completar 30 min pode demorar para
revalidar. William aceitou esse limite — sem Timer de recuperação nem checagem de tempo acumulado entre
telas.

Controle adicionado por **patch no YAML da tela** (colar o bloco do Timer), nunca reimportando a tela
inteira (`GMS_Mestre.md`, padrão de versão de controle).

**Gate completo (única versão — uma só melhor solução, sem variante opcional):** se o app não usa OnStart
bloqueante, `varCompostoPermitida` pode estar `Blank()` quando o `OnVisible` da primeira tela roda.
`!Blank()` avalia `true`, então o gate simples já *bloquearia* todo mundo na primeira visita (não libera
por engano — correção do texto do 3º passe, que estava invertido). Para não depender de o OnStart ser
bloqueante, o gate sempre valida antes de decidir quando a variável ainda não existe:

```powerfx
// OnVisible da tela — versão única, usada em todas as telas da lista:
If(
    IsBlank(varCompostoPermitida),
    // ainda não validou nesta sessão — valida agora, síncrono, antes de decidir
    IfError(
        With(
            {resComposto: Flow_Composto.Run()},
            Set(varCompostoPermitida, resComposto.permitido);
            Set(varCompostoMensagem, resComposto.mensagem)
        ),
        Set(varCompostoPermitida, false);
        Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
    )
);
If(
    !varCompostoPermitida,
    Navigate(scr_Composto),
    // <OnVisible original da tela, sem mudança — em scr_selecaosetor_Montagem isso inclui
    // Select(btn_RecarregarSelM), que deve ficar dentro deste Else>
)
```

Essa é a única versão do gate — sem alternativa "simples" em paralelo, para respeitar a norma de "uma
única melhor solução" do `GMS/CLAUDE.md`. Isso também elimina a pendência "confirmar se o OnStart é
bloqueante" da seção 6 — o gate funciona nos dois casos.

### 3.3 Tela de bloqueio `scr_Composto`

Tela nova (`scr_Composto`, nasce do template padrão, B §6), sem os botões de navegação do template.
Mostra `varCompostoMensagem` num rótulo fixo:

```powerfx
lbl_MensagemComposto.Text = Coalesce(varCompostoMensagem, "Acesso bloqueado.")
```

`varCompostoMensagem` vem do campo `Mensagem` da lista — **William escreve o texto ali, não no código**.

**Sem Timer nesta tela** (decisão 14: falha passageira aceita como está). A única saída é reabrir o app,
igual à reativação (seção 4) — texto alinhado com a decisão real, corrigindo a versão anterior do plano
que prometia uma saída automática que não existia.

### 3.4 `App.BackEnabled` — impedir escapar pelo botão voltar

```powerfx
App.BackEnabled = (App.ActiveScreen.Name <> "scr_Composto")
```

Corrigido para comparar `.Name` com texto (achado do 3º passe), não a tela diretamente. Testar num
tablet Android antes de publicar, para confirmar que a propriedade é reavaliada a cada troca de tela.

## 4. Reativação

Mudar `Ativo = Sim` ou `DataBloqueio` para o futuro na lista `Composto` **exige fechar e reabrir o app**
em cada tablet/computador — é a única saída de `scr_Composto` (decisão 7 e 14, seção 3.3). Avisar os
operadores disso ao reativar.

## 5. Processo (regra do repositório)

- Mudança em muitos arquivos (lista nova + Flow novo + `OnStart` + 23 telas + `App.BackEnabled` + tela
  nova) → **plano aprovado antes de implementar**.
- Mudança de arquitetura → passa pelo `revisor` antes de implementar. **Aprovado no 4º passe
  (17/11/2026), depois de 3 reprovações. Pronto para o `executor`.**
- Nesta sessão o agente `revisor` não apareceu disponível pelo nome (bug de listagem); as 4 revisões
  foram feitas por `general-purpose` com modelo Opus e esforço alto, seguindo ao pé da letra o papel de
  `.claude/agents/revisor.md`. Investigar a causa antes de usar o `revisor` de fato numa próxima revisão
  (ex.: validação do resultado implementado).
- Diário: linha `DECISÃO` (decisão 8), mais `ENTREGUE`/`PUBLICADO` conforme o ciclo de implementação.

## 6. Pendências do `executor` antes de aplicar (não são decisões do William, são checagens técnicas)

1. Confirmar se `scr_HoraHora_Mandril_2`, `scr_HoraHora_Tubo_2` (`Moldes/`) e `scr_Trancagem_3` estão
   publicadas (decisão 15) — se sim, aplicar o mesmo bloco de gate+Timer nelas.
2. Rodar o Flow uma vez e confirmar que `DataBloqueio` chega em UTC como esperado (seção 2).
3. Testar `App.BackEnabled` num tablet Android de fato, e testar o `Navigate` dentro do `OnVisible` nas
   23 telas (inclusive `scr_selecaosetor_Montagem`, onde `Select(btn_RecarregarSelM)` precisa ficar no
   `Else` do gate).
4. Sincronizar `Telas/` no mesmo ciclo (norma de 01/10/2026): `Telas/OnStart.txt`, `Telas/BackEnabled.txt`
   (hoje `true`), o novo `Telas/scr_Composto.txt`, os `.txt` das 23 telas tocadas e `GMS_Indice.md`.
   Rodar `gms_qa_yaml.py` em cada `.txt` tocado. **William publica** no Studio/Power Automate — não cola
   YAML diretamente.

## Fora de escopo deste plano

A sugestão de trocar o proprietário dos fluxos/conexões/app para uma conta de serviço (para sobreviver à
saída de alguém da empresa) é uma decisão de governança de identidade do tenant Microsoft 365 — não é
implementação de app/Flow e não está neste plano. Fica para decisão separada com quem administra o tenant.
