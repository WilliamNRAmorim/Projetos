# Plano: Kill Switch do GMS (validação externa via SharePoint) — codinome "Composto"

Status: **REPROVADO pelo revisor (Opus, esforço alto, 17/11/2026) — não implementar ainda.** A ideia geral
está certa, mas tem 3 problemas graves (ver seção 7) que podem travar a fábrica ou simplesmente não
bloquear nada. Nada foi implementado no Power Apps/Power Automate.

Nomenclatura (a pedido do William, 17/11/2026): todo o mecanismo — lista, Flow e variáveis — usa o
codinome **Composto** em vez de nomes como "ConfiguracaoApp"/"Validacao"/"Permissao".

## Nota sobre a data

William confirmou no chat (17/11/2026): **06/01/2027 é a data real da chave de validação** — depois dela
o GMS para de ser usado porque a operação migra para outro sistema. `DataBloqueio` na lista `Composto`
deve ser preenchida com **06/01/2027**.

## Objetivo

Mecanismo de desligamento remoto do app GMS (Power Apps), controlado por uma lista do SharePoint, sem
precisar republicar o app nem o Flow para ativar/desativar.

## 1. Lista SharePoint `Composto`

| Campo | Tipo | Observação |
|---|---|---|
| `Ativo` | Sim/Não (Yes/No) | Chave principal: Não = bloqueia na hora |
| `DataBloqueio` | Data | A partir dessa data, bloqueia mesmo com `Ativo = Sim`. Valor: **06/01/2027** |
| `Mensagem` | Texto | **William digita aqui manualmente** o texto de bloqueio. Sem código, sem Flow, sem Studio — só editar o item da lista |

Um único item na lista (ou `First()` sobre ela). Lista nova, criada no mesmo site SharePoint das outras
listas do GMS (confirmado pelo William, 17/11/2026) — mesmo local de `ficha_producao`, `MapeamentoSetor`
etc.

## 2. Flow `Flow_Composto` (Power Automate)

- Gatilho: **Power Apps (V2)**.
- Ação: `Obter itens` (ou `Obter item`) em `Composto`.
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
**antes** desse bloco, para decidir se o app deve nem carregar o resto. Variáveis seguem o padrão `var`
já usado no OnStart atual (`varMapa`, `varAcessoRestrito`):

```powerfx
With(
    {resComposto: Flow_Composto.Run()},
    Set(varCompostoPermitida, resComposto.permitido);
    Set(varCompostoMensagem, resComposto.mensagem)
);

If(
    varCompostoPermitida,
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

### 3.2 Tela de bloqueio `scr_Composto`

Tela nova (`scr_Composto`, nasce do template padrão, B §6) ou um container sobre a tela atual:

```powerfx
Visible = !varCompostoPermitida
```

Padrão do GMS para mensagem de erro (`GMS_Mestre.md` §3.7): `Notify(texto, NotificationType.Error)` com a
cor `fx_CorErro`. A tela/mensagem de bloqueio segue o mesmo padrão visual:

```powerfx
Notify(Coalesce(varCompostoMensagem, "Acesso bloqueado."), NotificationType.Error)
```

`varCompostoMensagem` vem direto do campo `Mensagem` da lista (seção 1) — **William escreve o texto
ali, na lista, não no código**. Trocar a mensagem depois é só editar aquele item, sem tocar em
Power Fx/Flow.

### 3.3 Proteção contra sessão aberta por semanas — decidido: Timer, não guarda por tela

Levantamento em `Telas/*.txt`: **22 telas atuais** (`scr_*`) têm `Patch`/`SubmitForm` de produção —
Mandril, Tubo, Trançagem, Cobertura, Bandagem, Vulcanização, Debandagem, Catenária,
Extrusora/Bobinadeira, Montagem, Hora-Hora de cada etapa, Conferência SAP, Impressão, Refugo Bobinadeira.

Envolver `If(varCompostoPermitida, Patch(...))` em cada Patch dessas 22 telas violaria a norma de
"patch cirúrgico, nunca rewrite" (volume grande de mudança simultânea em telas de produção, risco alto).

**Solução escolhida:** um `Timer` oculto numa tela sempre visível (ou num componente global), revalidando
periodicamente sem tocar em `Patch`:

```powerfx
// OnTimerEnd do Timer global (ex.: a cada 30–60 min, Duration configurável)
With(
    {resComposto: Flow_Composto.Run()},
    Set(varCompostoPermitida, resComposto.permitido);
    Set(varCompostoMensagem, resComposto.mensagem);
    If(!varCompostoPermitida, Navigate(scr_Composto))
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
6. ~~Nome do mecanismo~~ — resolvido: codinome "Composto" em lista, Flow e variáveis.

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
`Composto`. Sem republicar app nem Flow.

## 7. Revisão (Opus, esforço alto, 17/11/2026) — REPROVADO

Pontos confirmados OK: Timer sem `Patch` (só `Set`/`Flow.Run()`), sem `UpdateContext`, sem `Coalesce(x,0)`
em exibição, data 06/01/2027 conforme `GMS/CLAUDE.md`.

**Graves:**
1. Sem `IfError` no `OnStart`/Timer — Flow fora do ar deixa `varCompostoPermitida` em branco/erro: o app
   não carrega as coleções e não mostra o bloqueio (abre em branco), ou bloqueia todo mundo à toa numa
   queda de Wi-Fi.
2. O bloqueio do `OnStart` não funciona como escrito: `GMS/Telas/StartScreen.txt` manda quem tem acesso
   restrito direto para ~12 telas de produção (`scr_tubo_1`, `scr_Bandagem_1`, `scr_Montagem_HoraHora`
   etc.), sem passar pelo menu — o operador cai na tela de produção com as coleções vazias, mesmo
   bloqueado.
3. O plano não diz em qual tela o `Timer` fica. Sem uma tela/componente que toda sessão visita, ele pode
   nunca rodar.

**Médios:**
4. `utcNow()` vs `DataBloqueio` sem fuso corta no meio do 2º ou 3º turno em Brasília — falta decidir a
   hora exata do corte.
5. Lista `Composto` no mesmo site onde operadores gravam — sem quebrar herança de permissão, qualquer
   operador pode desligar o mecanismo.
6. `Navigate` do Timer no meio de um apontamento perde o que estava sendo digitado; `BackEnabled = true`
   deixa o botão voltar do Android escapar da tela de bloqueio.
7. Reativar (`Ativo = Sim`) só funciona depois de reabrir o app — não estava escrito no plano.

**Baixos:** Flow precisa de `First()`/Top 1 e tratar lista vazia; `permitido` como Sim/Não; `Notify` não
aceita cor (ajustar a mensagem); contradição entre §3.3 ("1 tela + 1 Timer") e §5 ("N telas"); falta
sincronizar `Telas/` e rodar `gms_qa_yaml.py`; decidir `NORMA` vs `DECISÃO` no diário.

**Decisões do William antes de reescrever o plano:**
1. Se o Flow falhar, libera ou bloqueia?
2. Corte às 00h00, no meio do 3º turno, ou 05h20 (fim do 3º turno)?
3. Aceita tocar nas ~12 telas do `StartScreen` em vez de "1 tela + 1 Timer"?
4. Intervalo do Timer e aceita perder o que o operador estava digitando?
5. Quem pode editar a lista `Composto`?
6. Reativar exige reabrir o app — ok?
7. Diário: `NORMA` ou `DECISÃO`?

## Fora de escopo deste plano

A sugestão de trocar o proprietário dos fluxos/conexões/app para uma conta de serviço (para sobreviver à
saída de alguém da empresa) é uma decisão de governança de identidade do tenant Microsoft 365 — não é
implementação de app/Flow e não está neste plano. Fica para decisão separada com quem administra o tenant.
