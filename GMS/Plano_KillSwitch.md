# Plano: Kill Switch do GMS (validação externa via SharePoint) — codinome "Composto"

Status: **plano revisado após 2 reprovações — rodada 2 de decisões do William respondida (17/11/2026).
Aguardando terceiro passe do revisor antes de implementar.** Nada foi implementado no Power
Apps/Power Automate ainda.

Nomenclatura (a pedido do William): todo o mecanismo — lista, Flow e variáveis — usa o codinome
**Composto** em vez de nomes como "ConfiguracaoApp"/"Validacao"/"Permissao".

## Histórico de decisões do William

**Rodada 1 (17/11/2026):**
1. Se o Flow falhar: **bloqueia** (fail-safe).
2. Corte: **06/01/2027 13:59** horário de Brasília.
3. Escopo de telas: aceita ajustar as telas de produção (ver rodada 2, item 1 — escopo final fechado em
   **todas**).
4. Timer: **30 minutos**.
5. Perder digitação ao bloquear no meio do uso: **aceito**.
6. Permissão da lista: **só o William edita**.
7. Reativar exige reabrir o app: **aceito**.
8. Diário: linha **DECISÃO**, não NORMA.

**Rodada 2 (17/11/2026, após 2ª reprovação):**
9. Gate/Timer em **todas as ~22 telas com `Patch`/`SubmitForm` + `Menu_1`** (23 telas) — cobertura
   completa, sem o furo de quem fica parado em Hora-Hora/Conferência SAP.
10. Conexão do `Flow_Composto` com a lista: **a do William, embutida no Flow** — operadores não
    precisam de acesso à lista.
11. Site SharePoint da lista `Composto`: **confirmado no fuso de Brasília (UTC-03:00)**.
12. Autorizado trocar `App.BackEnabled` (propriedade do app inteiro) para bloquear o botão voltar do
    Android saindo de `scr_Composto`.

## Objetivo

Mecanismo de desligamento remoto do app GMS (Power Apps), controlado por uma lista do SharePoint, sem
precisar republicar o app nem o Flow para ativar/desativar. Corte definitivo em **06/01/2027 às 13:59**
(horário de Brasília) — depois dessa data a operação migra para outro sistema.

## 1. Lista SharePoint `Composto`

| Campo | Tipo | Observação |
|---|---|---|
| `Ativo` | Sim/Não (Yes/No) | Chave principal: Não = bloqueia na hora |
| `DataBloqueio` | Data e hora | **06/01/2027 13:59**, horário de Brasília — site confirmado nesse fuso (decisão 11) |
| `Mensagem` | Texto | **William digita aqui manualmente** o texto de bloqueio. Sem código, sem Flow, sem Studio — só editar o item da lista |

Um único item na lista. Lista nova, no mesmo site SharePoint das outras listas do GMS, com **herança de
permissão quebrada**: edição só para o William (decisão 6). Como o Flow usa a conexão do William,
embutida (decisão 10), os operadores não precisam de acesso de leitura à lista — evita o risco de
alguém sem permissão ficar bloqueado por engano.

## 2. Flow `Flow_Composto` (Power Automate)

- Gatilho: **Power Apps (V2)**.
- Conexão com a lista: **do William**, embutida no Flow (decisão 10) — não roda com a conta de quem
  chama o Flow.
- Ação: `Obter itens` em `Composto`, `Top Count = 1`. Tratar explicitamente o caso de lista vazia.
- Lógica (Condição), comparando sempre em **UTC** (sem `convertFromUtc` — correção do 2º passe):
  ```
  item = first(outputs('Obter_itens')?['body/value'])

  Se item é nulo -> permitido = false  (lista vazia = fail-safe bloqueia)
  Senão se not(equals(item?['Ativo'], true)) -> permitido = false   (cobre Ativo=Não E Ativo vazio)
  Senão se greaterOrEquals(ticks(utcNow()), ticks(item?['DataBloqueio'])) -> permitido = false
  Senão -> permitido = true
  ```
  `item.DataBloqueio` grava **06/01/2027 13:59 horário de Brasília**; como o conector do SharePoint
  devolve a data já em UTC e o site está confirmado no fuso de Brasília (decisão 11), comparar direto
  `ticks(utcNow())` com `ticks(item.DataBloqueio)` sem conversão adicional é o correto — a conversão de
  fuso já acontece na gravação/leitura do próprio SharePoint.
- Resposta ao Power Apps (`Responder a um PowerApp ou fluxo`):
  ```json
  {
    "permitido": true,
    "mensagem": "texto opcional"
  }
  ```
  `permitido` como campo **Sim/Não** (boolean), não texto.

## 3. Power Fx — onde entra no app

### 3.1 `App.OnStart` — com tratamento de falha

Hoje o `OnStart` (`Telas/OnStart.txt`) faz `Concurrent(...)` carregando coleções (`colTrancadeiras`,
`colMangueiras`, `Turno`, `colDM_*`) e depois `ClearCollect(colMangEscTubo, ...)`. A validação entra
**antes** desse bloco, com `IfError` — fail-safe: erro = bloqueia (decisão 1):

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

**Importante (achado do 2º passe):** `App.StartScreen` é uma propriedade que só *retorna* qual tela
abrir — não aceita `Navigate()`, e não é garantido que variáveis do `OnStart` já estejam disponíveis ali
quando ela é avaliada. Por isso o gate **não** vai em `StartScreen.txt` (correção da versão anterior
deste plano); vai no `OnVisible` de cada tela de destino, seção 3.2.

### 3.2 Gate + Timer juntos no `OnVisible` de 23 telas

Decisão 9 (rodada 2): cobertura completa, nas **~22 telas com `Patch`/`SubmitForm`** levantadas
anteriormente **+ `Menu_1`** (23 telas no total, incluindo quem não tem acesso restrito e navega pelo
menu).

Em cada uma dessas 23 telas, o `OnVisible` existente ganha, como primeira instrução (junção, não
substituição), o mesmo bloco de checagem + revalidação que hoje estaria num Timer central — como não há
tela/componente compartilhado entre elas, a checagem roda no próprio `OnVisible` de cada tela, e um
`Timer` oculto (30 min, decisão 4) cobre quem fica parado na mesma tela por muito tempo:

```powerfx
// OnVisible da tela (primeira instrução, antes do OnVisible original):
If(
    !varCompostoPermitida,
    Navigate(scr_Composto)
    // se varCompostoPermitida = true, segue para o OnVisible original da tela, inalterado
);

// Timer oculto na mesma tela — Duration = 1800000 (30 min); AutoStart = true; Repeat = true
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

Sem `Patch` dentro do `Timer` (norma respeitada) — só `Set`/chamada de Flow. Decisão 5 aceita: se o Timer
disparar no meio de um apontamento, o que estava sendo digitado se perde. Decisão 1: erro no Flow =
bloqueia, em qualquer uma das 23 telas.

**Volume real da mudança:** 23 telas ganham o mesmo bloco padronizado (gate + Timer) no `OnVisible`,
mais `OnStart`, `scr_Composto` (nova) e `App.BackEnabled` (seção 3.4) — maior do que a estimativa
original ("1 tela + 1 Timer"), mas é a cobertura que o William escolheu (decisão 9) depois de ver o furo
da versão anterior.

### 3.3 Tela de bloqueio `scr_Composto`

Tela nova (`scr_Composto`, nasce do template padrão, B §6), sem os botões de navegação do template
(topo/menu), para não abrir uma saída por fora do `App.BackEnabled`. Mostra `varCompostoMensagem` num
rótulo fixo (não `Notify`, que é passageiro):

```powerfx
lbl_MensagemComposto.Text = Coalesce(varCompostoMensagem, "Acesso bloqueado.")
```

`varCompostoMensagem` vem direto do campo `Mensagem` da lista (seção 1) — **William escreve o texto
ali, na lista, não no código**.

### 3.4 `App.BackEnabled` — impedir escapar pelo botão voltar

Achado do 2º passe: `Telas/BackEnabled.txt = true` deixa o botão voltar do Android tirar o operador de
`scr_Composto` de volta para a tela anterior, já com as coleções carregadas. Decisão 12 (autorizado):

```powerfx
App.BackEnabled = (App.ActiveScreen <> scr_Composto)
```

Isso é propriedade do **app inteiro** (não da tela) — único ponto de mudança, sem duplicar em cada tela.

## 4. Reativação

Confirmado (decisão 7): mudar `Ativo = Sim` ou `DataBloqueio` para o futuro na lista `Composto`
**exige fechar e reabrir o app** em cada tablet/computador — o `OnStart` só recarrega as coleções de
produção na abertura. Quem já estava em `scr_Composto` quando `Ativo` virar `Sim` só sai de lá no
próximo ciclo do Timer daquela tela (até 30 min) ou reabrindo o app; avisar os operadores disso ao
reativar.

## 5. Processo (regra do repositório)

- Mudança em muitos arquivos (lista nova + Flow novo + `OnStart` + 23 telas + `App.BackEnabled` + tela
  nova) → **plano aprovado antes de implementar**.
- Mudança de arquitetura → passa pelo `revisor` antes de implementar. **Este plano já foi reprovado duas
  vezes; precisa de um terceiro passe confirmando a versão atual antes de ir ao `executor`.**
- Nesta sessão o agente `revisor` não apareceu disponível pelo nome (bug de listagem); as revisões foram
  feitas por `general-purpose` com modelo Opus e esforço alto, seguindo ao pé da letra o papel de
  `.claude/agents/revisor.md`. Investigar a causa, se possível usar o `revisor` de fato no próximo passe.
- Implementação (depois de aprovado): `executor` monta o YAML de todos os arquivos afetados — `OnStart`,
  `App` (BackEnabled), `scr_Composto` (nova) e as 23 telas com gate+Timer; sincronizar `Telas/` no mesmo
  ciclo (norma de 01/10/2026) e rodar `gms_qa_yaml.py` em cada `.txt` tocado. **William publica** no
  Studio/Power Automate — não cola YAML diretamente, conforme regra do GMS.
- Antes de implementar, o executor também confirma no Studio se o app usa OnStart bloqueante (achado do
  2º passe, item 7) e qual tela está publicada de fato entre `scr_Trancagem_3`/`scr_Trancagem_4`
  (achado do 2º passe, item 8).
- Diário: linha `DECISÃO` (decisão 8) registrando o mecanismo, mais `ENTREGUE`/`PUBLICADO` conforme o
  ciclo de implementação.

## Fora de escopo deste plano

A sugestão de trocar o proprietário dos fluxos/conexões/app para uma conta de serviço (para sobreviver à
saída de alguém da empresa) é uma decisão de governança de identidade do tenant Microsoft 365 — não é
implementação de app/Flow e não está neste plano. Fica para decisão separada com quem administra o tenant.
