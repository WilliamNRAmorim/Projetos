# Plano: Kill Switch do GMS (validação externa via SharePoint)

Status: **plano fechado, aguardando aprovação final para implementar** — nada foi implementado no Power
Apps/Power Automate ainda. Todas as 5 pendências originais foram resolvidas (seção 4).

## Nota sobre a data

William confirmou no chat (17/11/2026): **06/01/2027 é a data real da chave de validação** — depois dela
o GMS para de ser usado porque a operação migra para outro sistema. `DataBloqueio` na lista
`ConfiguracaoApp` deve ser preenchida com **06/01/2027**.

## Objetivo

Mecanismo de desligamento remoto do app GMS (Power Apps), controlado por uma lista do SharePoint, sem
precisar republicar o app nem o Flow para ativar/desativar.

## 1. Lista SharePoint `ConfiguracaoApp`

| Campo | Tipo | Observação |
|---|---|---|
| `Ativo` | Sim/Não (Yes/No) | Chave principal: Não = bloqueia na hora |
| `DataBloqueio` | Data | A partir dessa data, bloqueia mesmo com `Ativo = Sim`. Sem valor cravado — William define |
| `Mensagem` | Texto | **William digita aqui manualmente** o texto de bloqueio. Sem código, sem Flow, sem Studio — só editar o item da lista |

Um único item na lista (ou `First()` sobre ela). Lista nova, criada no mesmo site SharePoint das outras
listas do GMS (confirmado pelo William, 17/11/2026) — mesmo local de `ficha_producao`, `MapeamentoSetor`
etc.

## 2. Flow `Flow_Validacao` (Power Automate)

- Gatilho: **Power Apps (V2)**.
- Ação: `Obter itens` (ou `Obter item`) em `ConfiguracaoApp`.
- Lógica (Condição / Switch):
  ```
  Se Ativo = Não  -> permitido = false
  Senão se Hoje >= DataBloqueio -> permitido = false
  Senão -> permitido = true
  ```
  Usar a expressão de data do Flow (`utcNow()` vs. a data do item), não comparação de texto.
- Resposta ao Power Apps (`Responder a um PowerApp ou fluxo`):
  ```json
  {
    "permitido": true,
    "mensagem": "texto opcional"
  }
  ```

## 3. Power Fx — onde entra no app

### 3.1 `App.OnStart`

Hoje o `OnStart` (`Telas/OnStart.txt`) faz `Concurrent(...)` carregando coleções (`colTrancadeiras`,
`colMangueiras`, `Turno`, `colDM_*`) e depois `ClearCollect(colMangEscTubo, ...)`. A validação entra
**antes** desse bloco, para decidir se o app deve nem carregar o resto:

```powerfx
Set(gblPermissao, Flow_Validacao.Run().permitido);
Set(gblMensagemBloqueio, Flow_Validacao.Run().mensagem);

If(
    gblPermissao,
    (
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
)
```

Nota: chamar `Flow_Validacao.Run()` duas vezes gasta uma chamada extra; melhor capturar o resultado uma
vez com `With({res: Flow_Validacao.Run()}, Set(gblPermissao, res.permitido); Set(gblMensagemBloqueio,
res.mensagem))`. Isso é só um ponto de gravação — ajusto antes de aplicar, se aprovado.

### 3.2 Tela de bloqueio

Tela nova (`scr_Bloqueado`, nasce do template padrão, B §6) ou um container sobre a tela atual:

```powerfx
Visible = !gblPermissao
```

Padrão do GMS para mensagem de erro (`GMS_Mestre.md` §3.7): `Notify(texto, NotificationType.Error)` com a
cor `fx_CorErro`. A tela/mensagem de bloqueio segue o mesmo padrão visual:

```powerfx
Notify(Coalesce(gblMensagemBloqueio, "Acesso bloqueado."), NotificationType.Error)
```

`gblMensagemBloqueio` vem direto do campo `Mensagem` da lista (seção 1) — **William escreve o texto ali,
na lista, não no código**. Trocar a mensagem depois é só editar aquele item, sem tocar em Power Fx/Flow.

### 3.3 Proteção contra sessão aberta por semanas — decidido: Timer, não guarda por tela

Levantamento em `Telas/*.txt`: **22 telas atuais** (`scr_*`) têm `Patch`/`SubmitForm` de produção —
Mandril, Tubo, Trançagem, Cobertura, Bandagem, Vulcanização, Debandagem, Catenária,
Extrusora/Bobinadeira, Montagem, Hora-Hora de cada etapa, Conferência SAP, Impressão, Refugo Bobinadeira.

Envolver `If(gblPermissao, Patch(...))` em cada Patch dessas 22 telas violaria a norma de "patch
cirúrgico, nunca rewrite" (volume grande de mudança simultânea em telas de produção, risco alto).

**Solução escolhida:** um `Timer` oculto numa tela sempre visível (ou num componente global), revalidando
periodicamente sem tocar em `Patch`:

```powerfx
// OnTimerEnd do Timer global (ex.: a cada 30–60 min, Duration configurável)
With(
    {res: Flow_Validacao.Run()},
    Set(gblPermissao, res.permitido);
    Set(gblMensagemBloqueio, res.mensagem);
    If(!gblPermissao, Navigate(scr_Bloqueado))
)
```

Isso é permitido pela norma (só proíbe `Patch` dentro de `Timer`, não `Set`/chamada de Flow). Cobre o caso
de alguém deixar o app aberto por semanas, sem tocar nas 22 telas de produção — só `App.OnStart` + 1 tela
de bloqueio + 1 `Timer`.

## 4. Pendências para fechar o plano

1. ~~Local da lista~~ — resolvido: mesmo site SharePoint das listas atuais do GMS.
2. ~~Revalidação~~ — resolvido (seção 3.3): `Timer` global, sem tocar nas 22 telas de produção.
3. ~~Quais telas têm ação crítica~~ — resolvido (seção 3.3): 22 telas levantadas.
4. ~~Mensagem de bloqueio~~ — resolvido (seção 3.2): campo `Mensagem` da lista, William digita.
5. ~~`DataBloqueio`~~ — resolvido: 06/01/2027 (confirmado pelo William).

## 5. Processo (regra do repositório)

- Isso é mudança em mais de um "arquivo" (lista nova + Flow novo + `OnStart` + N telas) → **plano aprovado
  antes de implementar** (este documento).
- É mudança de **arquitetura** do app (controla se o app inteiro roda) → depois de aprovado o escopo,
  recomendo passar pelo `revisor` (Opus) antes de aplicar, não pelo `revisor-leve`, porque:
  - toca lógica que pode travar o app inteiro em produção (risco alto se mal implementado).
- Implementação (depois do plano aprovado + revisor): `executor` monta o YAML das telas/Flow afetados;
  **William publica** no Studio/Power Automate — não cola YAML diretamente, conforme regra do GMS.
- Diário: ao fechar, linhas `NORMA` (confirmando o mecanismo) e `ENTREGUE`/`PUBLICADO` conforme o ciclo.

## 6. "Botão mágico" de reativar

Confirmado do texto original: só mudar `Ativo = Sim` ou `DataBloqueio` para o futuro na lista
`ConfiguracaoApp`. Sem republicar app nem Flow.

## Fora de escopo deste plano

A sugestão de trocar o proprietário dos fluxos/conexões/app para uma conta de serviço (para sobreviver à
saída de alguém da empresa) é uma decisão de governança de identidade do tenant Microsoft 365 — não é
implementação de app/Flow e não está neste plano. Fica para decisão separada com quem administra o tenant.
