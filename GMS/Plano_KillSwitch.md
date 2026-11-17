# Plano: Kill Switch do GMS (validação externa via SharePoint) — codinome "Composto"

Status: **REPROVADO no segundo passe do revisor (Opus, esforço alto, 17/11/2026) — não implementar ainda.**
As 8 decisões do primeiro passe foram incorporadas, mas o segundo passe achou que o gate do `StartScreen`
continua sem funcionar (por outro motivo) e mais problemas novos (seção 8). Nada implementado no Power
Apps/Power Automate ainda. 4 novas decisões do William pendentes.

Nomenclatura (a pedido do William): todo o mecanismo — lista, Flow e variáveis — usa o codinome
**Composto** em vez de nomes como "ConfiguracaoApp"/"Validacao"/"Permissao".

## Decisões do William (17/11/2026) — todas resolvidas

1. **Se o Flow falhar:** bloqueia (seguro). Erro de rede/Flow = tratado como `permitido = false`.
2. **Corte:** `06/01/2027 13:59` horário de Brasília.
3. **Escopo de telas:** sim, ajustar as ~12 telas de destino do `StartScreen.txt`.
4. **Timer:** 30 minutos.
5. **Perder digitação ao bloquear no meio do uso:** aceito, sem proteção de `varProcessando`.
6. **Permissão da lista:** só o William edita (quebra herança do site).
7. **Reativar exige reabrir o app:** aceito (opção recomendada).
8. **Diário:** linha `DECISÃO`, não `NORMA`.

## Objetivo

Mecanismo de desligamento remoto do app GMS (Power Apps), controlado por uma lista do SharePoint, sem
precisar republicar o app nem o Flow para ativar/desativar. Corte definitivo em **06/01/2027 às 13:59**
(horário de Brasília) — depois dessa data a operação migra para outro sistema.

## 1. Lista SharePoint `Composto`

| Campo | Tipo | Observação |
|---|---|---|
| `Ativo` | Sim/Não (Yes/No) | Chave principal: Não = bloqueia na hora |
| `DataBloqueio` | Data e hora | **06/01/2027 13:59**, horário de Brasília (ver seção 2 sobre fuso) |
| `Mensagem` | Texto | **William digita aqui manualmente** o texto de bloqueio. Sem código, sem Flow, sem Studio — só editar o item da lista |

Um único item na lista (ou `First()` sobre ela). Lista nova, criada no mesmo site SharePoint das outras
listas do GMS — mas com **herança de permissão quebrada**: leitura para todo mundo (o Flow precisa ler
como o usuário corrente ou via conexão dedicada), **edição só para o William**. Sem isso, qualquer
operador pode desligar o mecanismo.

## 2. Flow `Flow_Composto` (Power Automate)

- Gatilho: **Power Apps (V2)**.
- Ação: `Obter itens` em `Composto`, com `Top Count = 1` (ou `Obter item` pelo ID fixo) — **nunca** assumir
  que a lista tem exatamente 1 item sem checar lista vazia.
- Lógica (Condição):
  ```
  agoraBR = convertFromUtc(utcNow(), 'E. South America Standard Time')
  item = first(outputs('Obter_itens')?['body/value'])

  Se item é nulo -> permitido = false  (lista vazia = fail-safe bloqueia)
  Senão se item.Ativo = false -> permitido = false
  Senão se agoraBR >= item.DataBloqueio -> permitido = false
  Senão -> permitido = true
  ```
  `DataBloqueio` é comparado como horário local de Brasília (`item.DataBloqueio` já gravado como
  06/01/2027 13:59 nesse fuso), contra `agoraBR` convertido de UTC. Não comparar `utcNow()` direto com
  `DataBloqueio` sem converter — isso cortaria 3h antes/depois do horário certo.
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
**antes** desse bloco, com `IfError` — **fail-safe: erro = bloqueia** (decisão 1):

```powerfx
IfError(
    With(
        {resComposto: Flow_Composto.Run()},
        Set(varCompostoPermitida, resComposto.permitido);
        Set(varCompostoMensagem, resComposto.mensagem)
    ),
    (
        Set(varCompostoPermitida, false);
        Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
    )
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

Se `varCompostoPermitida = false`, as coleções de produção não carregam — combinado com o gate do
`StartScreen` (seção 3.2), ninguém chega a uma tela de produção com dado incompleto.

### 3.2 Gate no `StartScreen.txt` — resolve o furo apontado pelo revisor

`GMS/Telas/StartScreen.txt` hoje manda quem tem `AcessoRestrito` direto para ~12 telas de produção
(`scr_tubo_1`, `scr_Bandagem_1`, `scr_Montagem_HoraHora` etc.), sem passar pelo menu — por isso o
bloqueio original não funcionava: o roteamento ignorava `varCompostoPermitida`.

**Correção:** envolver a lógica de roteamento existente do `StartScreen` com uma checagem única no topo
(1 arquivo, não 12):

```powerfx
If(
    !varCompostoPermitida,
    Navigate(scr_Composto),
    // roteamento original do StartScreen, inalterado
    If(varAcessoRestrito, Navigate(<tela da célula de varMapa>), Navigate(Menu_1))
)
```

Isso garante que **nenhuma** rota (restrita ou não) escapa do bloqueio, resolvendo o problema 2 da
revisão com uma única mudança no `StartScreen`, não em 12 arquivos.

### 3.3 Tela de bloqueio `scr_Composto`

Tela nova (`scr_Composto`, nasce do template padrão, B §6), destino de `Navigate` tanto do `StartScreen`
quanto do Timer (seção 3.4). Mostra `varCompostoMensagem` num rótulo fixo (não `Notify`, que é
passageiro e já teria sumido se o operador não estiver olhando no momento certo):

```powerfx
lbl_MensagemComposto.Text = Coalesce(varCompostoMensagem, "Acesso bloqueado.")
```

`varCompostoMensagem` vem direto do campo `Mensagem` da lista (seção 1) — **William escreve o texto
ali, na lista, não no código**. Trocar a mensagem depois é só editar aquele item, sem tocar em
Power Fx/Flow.

### 3.4 Timer de revalidação (sessão aberta por semanas) — 30 min, nas 12 telas de destino

O app não tem um componente/header compartilhado entre as ~12 telas de produção (`rct_Header*` nas
telas são retângulos de estilo, não `Component`), então o `Timer` não pode morar num único lugar central
além do `StartScreen` — e o `StartScreen` só aparece na abertura, não durante o turno. **Decisão do
William: ajustar as 12 telas** (decisão 3), então o Timer entra em cada uma delas, idêntico:

```powerfx
// Timer.Duration = 1800000 (30 min); Timer.AutoStart = true; Timer.Repeat = true
// OnTimerEnd:
IfError(
    With(
        {resComposto: Flow_Composto.Run()},
        Set(varCompostoPermitida, resComposto.permitido);
        Set(varCompostoMensagem, resComposto.mensagem)
    ),
    (
        Set(varCompostoPermitida, false);
        Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")
    )
);
If(!varCompostoPermitida, Navigate(scr_Composto))
```

Sem `Patch` dentro do `Timer` (conforme norma) — só `Set`/chamada de Flow. Decisão 5 aceita: se o Timer
disparar no meio de um apontamento, o que estava sendo digitado se perde (sem checagem de
`varProcessando`). Decisão 1 aplicada aqui também: erro no Flow = bloqueia.

**Nota de implementação:** os 22 `Patch`/`SubmitForm` levantados antes (todas as telas de produção)
continuam **sem guarda individual** — só as ~12 telas de destino do `StartScreen` recebem o Timer; as
demais telas (Hora-Hora, Conferência SAP etc.) são alcançadas a partir dessas 12 e ficam cobertas pelo
mesmo ciclo de 30 min.

## 4. Reativação

Confirmado (decisão 7): mudar `Ativo = Sim` ou `DataBloqueio` para o futuro na lista `Composto`
**exige fechar e reabrir o app** em cada tablet/computador — o `OnStart` só recarrega as coleções de
produção na abertura. O Timer, por si, não refaz esse carregamento ao voltar para `permitido = true`
(ele só navega para fora de `scr_Composto`; quem já estava numa tela de produção quando o Flow caiu
precisa reabrir mesmo assim, por segurança). Avisar os operadores disso ao reativar.

## 5. Processo (regra do repositório)

- Mudança em mais de um arquivo (lista nova + Flow novo + `OnStart` + `StartScreen` + 12 telas + tela
  nova) → **plano aprovado antes de implementar**.
- Mudança de arquitetura → passa pelo `revisor` (ou equivalente, ver nota abaixo) antes de implementar.
  **Este plano já foi reprovado uma vez; precisa de novo passe do revisor confirmando as correções antes
  de ir ao `executor`.**
- Nesta sessão o agente `revisor` não apareceu disponível pelo nome (bug de listagem); a revisão foi
  feita por `general-purpose` com modelo Opus e esforço alto, seguindo ao pé da letra o papel de
  `.claude/agents/revisor.md`. Investigar a causa antes do próximo passe, se possível usar o `revisor`
  de fato.
- Implementação (depois do novo aprovado): `executor` monta o YAML das telas/Flow afetados — `OnStart`,
  `StartScreen`, `scr_Composto` (nova) e as ~12 telas de destino; sincronizar `Telas/` no mesmo ciclo
  (norma de 01/10/2026) e rodar `gms_qa_yaml.py` em cada `.txt` tocado. **William publica** no
  Studio/Power Automate — não cola YAML diretamente, conforme regra do GMS.
- Diário: linha `DECISÃO` (não `NORMA`, decisão 8) registrando o mecanismo, mais `ENTREGUE`/`PUBLICADO`
  conforme o ciclo de implementação.

## 8. Segundo passe do revisor (Opus, esforço alto, 17/11/2026) — REPROVADO

Resolvido desde o primeiro passe: `IfError` no OnStart/Timer; Timer sem `Patch`; mensagem em rótulo fixo
(não `Notify`); permissão de edição só do William; perda de digitação e reabrir para reativar, ambos
aceitos; diário `DECISÃO`; data e regra do `CLAUDE.md` respeitadas.

**Graves:**
1. **O gate da seção 3.2 não funciona**: `App.StartScreen` é uma propriedade que só *retorna* qual tela
   abrir (`With`/`LookUp`/`Switch`) — não aceita `Navigate()`, e variáveis do `OnStart` podem não estar
   disponíveis ali ainda. O roteamento real tem 13 ramos via `registroMapeamento.TelaSetor`, não é o
   `If(varAcessoRestrito, ...)` simplificado que o plano descreveu. **Correção:** o gate vai no `OnVisible`
   de cada uma das ~12 telas de destino **+ `Menu_1`** (13 telas), como primeira instrução, envolvendo o
   `OnVisible` que já existe: `If(!varCompostoPermitida, Navigate(scr_Composto), <OnVisible atual>)`.
   Isso é junção com o que já existe, não substituição — mas é 13 arquivos tocados, não 1.
2. **Fuso do Flow invertido**: o SharePoint guarda `DataBloqueio` em UTC. Comparar
   `convertFromUtc(utcNow(), ...)` (hora local, sem fuso) com um valor UTC corta 3h errado. **Correção:**
   comparar direto em UTC — `greaterOrEquals(ticks(utcNow()), ticks(item?['DataBloqueio']))` — sem
   `convertFromUtc`. Isso só bate certo com 13:59 de Brasília se o **site SharePoint estiver configurado
   no fuso de Brasília (UTC-03:00)** — precisa confirmar.
3. **Cobertura real do Timer é menor do que a seção 3.4 afirmava**: Timer de tela só conta enquanto
   aquela tela está visível e reinicia a cada troca de tela. Quem fica em Hora-Hora, Conferência SAP ou
   alterna de tela antes de 30 min nunca revalida; `Menu_1` nem está nas 12. A frase "as demais telas
   ficam cobertas pelo mesmo ciclo" (seção 3.4 original) está incorreta e foi removida.

**Médios novos:**
4. `Telas/BackEnabled.txt = true` deixa escapar de `scr_Composto` pelo botão voltar do Android —
   precisa trocar `App.BackEnabled` (propriedade do **app inteiro**, não da tela) para
   `App.ActiveScreen <> scr_Composto`.
5. `item.Ativo = false` deixa passar `Ativo` vazio (nulo ≠ false, libera por engano) — corrigir para
   `not(equals(item?['Ativo'], true))`.
6. Conexão do Flow indefinida: se for a conexão de cada usuário, quem não tiver acesso de leitura à
   lista fica bloqueado para sempre (fail-safe trata isso como bloqueio) — decisão de qual conexão usar.
7. Verificar no Studio se o app usa OnStart bloqueante; se não, a 1ª tela pode rodar com
   `varCompostoPermitida` ainda em branco.
8. (Baixo) `StartScreen.txt` referencia `scr_Trancagem_3`, mas `Telas/` só tem `scr_Trancagem_4.txt` —
   confirmar qual está publicada.

**Novas decisões do William antes de implementar:**
1. Gate/Timer em todas as ~22 telas com `Patch` + `Menu_1`, ou só nas 12 + `Menu_1` (aceitando o furo do
   item 3)?
2. Conexão do Flow: a do William (embutida) ou a de cada operador?
3. Confirma que o site SharePoint está no fuso de Brasília (UTC-03:00)?
4. Autoriza trocar `App.BackEnabled` (propriedade do app inteiro) para bloquear o botão voltar?

## Fora de escopo deste plano

A sugestão de trocar o proprietário dos fluxos/conexões/app para uma conta de serviço (para sobreviver à
saída de alguém da empresa) é uma decisão de governança de identidade do tenant Microsoft 365 — não é
implementação de app/Flow e não está neste plano. Fica para decisão separada com quem administra o tenant.
