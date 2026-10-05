# GMS — DOCUMENTO MESTRE DO BI
### Constituição da camada analítica do Guaratinguetá Manufacturing System
**Versão 1.0 · 31/08/2026 · norma estável**

> **Este arquivo é a NORMA do Power BI.** Ele é irmão do `GMS_Mestre.md` — mesma gramática, mesmo
> protocolo, mesma hierarquia de prioridade. O que muda é o objeto: lá é o app que **captura**,
> aqui é o modelo que **explica**.
>
> **Relação com os outros arquivos do projeto:**
>
> | Arquivo | O que é |
> |---|---|
> | `GMS_Mestre.md` | norma do Power Apps / SharePoint / captura |
> | `GMS_Mestre_BI.md` (este) | norma do modelo semântico, do DAX e dos relatórios |
> | `GMS_Diario.md` | append-only: entregas, decisões, lições, pendências, MEL-xxx |
> | `gms.py` | gera backlog/estado a partir do diário |
>
> **Regra de precedência:** onde os dois Mestres tratarem do mesmo assunto (turno, data de
> referência, tokens de cor, proibição do `Modified`), **a definição é única e nasce no
> `GMS_Mestre.md`**. Este documento a traduz para DAX/M, nunca a reinventa. Divergência entre os
> dois é bug de documentação e vira linha `NORMA` no diário no mesmo dia.
>
> **Base factual desta v1.0:** ~28 fontes SharePoint + 3 fontes Excel (`DM_MANDREL`, `DM_BANDAGEM`,
> `DM_LAYLINE`) mapeadas na auditoria do `.msapp` v2026-06-22; `ficha_producao` com 103 colunas;
> `RegistrosInspeção` ~6.000 registros; `TiposErros` 1.574 registros; modelo semântico atual com
> **102 medidas** e 10 relacionamentos; ~6 meses de dado de produção acumulado (mar→ago/2026).
>
> **⚠ Marcação de estado:** trechos marcados **[A AUDITAR]** são norma escrita antes da leitura do
> modelo semântico real. Assim que o `.pbip`/TMDL for lido, cada um vira **[CONFORME]** ou vira
> linha `MEL-xxx` no diário. Norma não muda; o que muda é o quanto o modelo atual já a cumpre.
>
> **[v1.1 · 31/08/2026] A auditoria foi feita** — leitura ao vivo do modelo no Desktop via MCP.
> Resultado em `GMS_Auditoria_BI_2026-08-31.md`. Números reais: 109 tabelas (86 automáticas),
> 1.321 colunas, **138 medidas** (3 em erro), 100 relacionamentos (85 automáticos). A emenda que
> a auditoria produziu está na §A.3.

---

# PARTE 0 — PROTOCOLO DE TRABALHO DO BI

**BI1. A verdade única é a mesma dos dois lados.** Se o número do painel diverge do número da tela
do operador, **um dos dois está errado e a discussão para até descobrir qual** — não existe
"arredondamento do BI". Isso é o pilar 1 do `GMS_Mestre.md` aplicado ao BI. Toda medida nova nasce
com um caso de conferência: um dia, um turno, uma etapa, conferido contra o app e contra o CSV.

**BI2. Uma definição por indicador, no modelo — nunca no visual.** Qualquer número exibido é
**medida DAX nomeada**. Proibido: agregação implícita arrastando coluna para o visual, cálculo em
"campo rápido", e a mesma conta escrita duas vezes com nomes diferentes. Um KPI tem uma fórmula só
no GMS inteiro, e ela está na Parte C.

**BI3. Transformação mora na camada mais barata que resolve.** Ordem obrigatória de tentativa:
(1) na origem/fluxo (Power Automate, C29) → (2) em Power Query com *query folding* → (3) em coluna
calculada DAX → (4) em medida DAX. Subir um degrau exige justificativa escrita no comentário.

**BI4. Modelo estrela é inegociável.** Fato no meio, dimensões em volta, relacionamento
1→N de sentido único. Tabela larga ligada em tabela larga é rejeitada de saída, por melhor que
"funcione".

**BI5. Patch cirúrgico, nunca rewrite.** Igual ao P3 do Mestre: entrega-se a medida completa, a
etapa M completa, o bloco de tema completo — não o modelo inteiro refeito.

**BI6. Prioridade de raciocínio (a mesma do P7, adaptada):** 1º confiabilidade do dado → 2º tempo
até a resposta (o supervisor tem 15 s, não 5 min) → 3º poder de decisão → 4º estética.

**BI7. Medida quebrada é bug de produção, não dívida técnica.** Número errado na tela que a
liderança olha custa mais do que tela feia. Evidência viva: **MEL-087** (Meta HH, Real HH e
Mangueira do Turno quebradas). Medida com erro fica **oculta ou removida** enquanto não for
corrigida — nunca visível dando resultado errado.

**BI8. Em dúvida, uma pergunta diagnóstica** — não três hipóteses.

**BI9. Todo ciclo de BI termina em linhas de diário.** Mesma regra do P10: entrega o DAX/M **e** as
linhas prontas para colar no `GMS_Diario.md`.

**BI10. O que o BI descobre volta para o app.** Se uma medida só fecha com `IF(ISBLANK(...))`
tapando buraco de dado, isso não é solução — é diagnóstico. Vira MEL de captura no app, e o
remendo no DAX carrega o comentário `-- remendo temporário de MEL-xxx`.

---

# PARTE A — ARQUITETURA DA CAMADA ANALÍTICA

## A.1 O problema estrutural (por que não basta "conectar e arrastar")

A `ficha_producao` é **um passaporte linear da OP**: 1 linha por OP, 103 colunas, com
`data_hora_final_<etapa>`, `quantidade_<etapa>`, `operador_<etapa>` repetidos oito vezes lado a
lado. Isso é a modelagem certa para o app (é o que o `GMS_Mestre.md` chama de passaporte) e é a
modelagem **errada** para análise: perguntar "quanto cada etapa produziu por turno" numa tabela
assim exige oito medidas quase idênticas, e é exatamente daí que nasce a proliferação de medidas
frágeis.

**Decisão de arquitetura ⛔:** o BI **não consome a `ficha_producao` no formato dela**. Consome uma
tabela-fato derivada, **`fEtapaOP`, com grão de 1 linha por OP × etapa**, produzida por unpivot em
Power Query. As oito colunas viram oito linhas com uma coluna `Etapa`. Uma medida passa a servir
as oito etapas.

```
ficha_producao (103 col, 1 linha/OP)     →  unpivot  →   fEtapaOP (1 linha/OP × etapa)
OP | qtd_tubo | qtd_trancagem | ...                      OP | Etapa | Quantidade | Fim | Operador
```

Consequência direta: **o número de medidas cai**, o `dEtapa` vira dimensão de verdade (com ordem
de fluxo), e o Radar de Gargalo (C3), o Diário de Bordo (C25) e o Lead Time (C4) deixam de ser
oito consultas e viram uma.

## A.2 As três camadas

| Camada | Onde vive | Prefixo | Carrega no modelo? | Regra |
|---|---|---|---|---|
| **Bronze — origem** | Power Query | `src_` | ❌ não | Conexão crua. Zero transformação além do necessário para autenticar. Uma consulta por lista/arquivo. |
| **Prata — preparo** | Power Query | `stg_` | ❌ não | Tipagem, renomeação humana, unpivot, `Data de Referência` e `Turno`, deduplicação, junções validadas. |
| **Ouro — modelo** | Modelo semântico | `f` / `d` | ✅ sim | Só o que o usuário vê. Nome humano, tipo certo, formato pt-BR, pasta de exibição. |

Parâmetros (`p_`) e funções (`fn_`) ficam em grupo próprio. **Nenhuma URL de site, caminho de
arquivo ou data de corte escrita dentro de uma etapa** — tudo em parâmetro.

## A.3 O mapa do modelo alvo

**Fatos:**

| Tabela | Grão (1 linha =) | Origem |
|---|---|---|
| `fEtapaOP` | 1 OP × etapa | `ficha_producao` (unpivot) |
| `fRefugo` | 1 registro de refugo | `TiposErros` + `Refugo_Bobinadeira` + `RefugoExtrusora_estrutura` (append) |
| `fInspecao` | 1 medição de inspeção | `RegistrosInspeção` |
| `fHoraHora` | 1 célula hora × processo | `HoraHora_Montagem` + hora-hora das linhas |
| `fParada` | 1 parada | `Paradas_Montagem` + paradas das linhas |
| `fCarretel` | 1 movimento de carretel | `Historico_Carretel` |
| `fEvento` | 1 evento de processo | `Eventos_Producao` |

**Dimensões:**

`dCalendario` · `dTurno` · `dEtapa` (com `Ordem_Fluxo`, vinda da `fFluxoEtapas` — C40) ·
`dOP` · `dMangueira` (PN) · `dPosto` (máquina física — C37) · `dColaborador` ·
`dMotivoParada` · `dCausaRefugo` · `dDelineamento` (spec — C26).

> **⚠ Emenda v1.1 (31/08/2026) — os nomes canônicos já existem.** A auditoria encontrou o unpivot
> **já feito** no modelo. A norma **não cria** `fEtapaOP`: adota o que existe.
>
> | Nome na norma v1.0 | Nome real e canônico | Grão | Linhas |
> |---|---|---|---|
> | `fEtapaOP` | **`Etapas`** | 1 etapa concluída por ficha | 13.256 |
> | *(não previsto)* | **`fFluxoEtapas`** | 1 etapa por ficha, com fila **e** processamento separados | 16.314 |
>
> `fFluxoEtapas` vai além do que a norma pedia: separar espera de trabalho efetivo é o insumo
> direto do C3 (Radar de Gargalo) e da eficiência de fluxo Lean. Tabela nova de fato deve seguir
> **esse** padrão, não o da v1.0.

**Regra de ligação ⛔:** todo fato liga em `dCalendario` pela coluna **`Data de Referência`**
(nunca pela data-hora bruta, nunca por `Modified`) e em `dTurno` pela coluna `Turno`. Um fato que
não tem essas duas colunas não entra no modelo — ele volta para a camada Prata.

**Grão declarado ⛔:** toda tabela de fato carrega, na descrição do modelo, a frase
"1 linha = ___". Sem essa frase escrita, a tabela não passa no checklist (§B.9).

## A.4 Relação com a Frente 2

A Frente 2 (consolidação das ~28 fontes) é a solução estrutural; o unpivot da camada Prata é a
**ponte** até lá. Quando a Frente 2 entregar o modelo normalizado (evento por linha), a camada
Bronze troca de origem e **a camada Ouro não muda** — é justamente para isso que existe a
separação. Nenhum relatório deve precisar ser refeito por causa da Frente 2.

---

# PARTE B — NORMAS TÉCNICAS OBRIGATÓRIAS

⛔ = bloqueante para modelo/relatório novo · ⚠️ = migração progressiva (aplicar quando tocar).

## B.1 Nomenclatura

### 1.1 Norma ⛔ — Tabelas

| Prefixo | Tipo | Exemplo |
|---|---|---|
| `f` | Fato | `fEtapaOP`, `fRefugo` |
| `d` | Dimensão | `dCalendario`, `dEtapa`, `dOP` |
| `b` | Ponte (bridge) N:N | `bGenealogia` |
| `_` | Tabela só de medidas (sem dados) | `_Medidas Produção` |
| `src_` / `stg_` | Consulta Bronze / Prata (não carregada) | `src_ficha_producao` |
| `p_` / `fn_` | Parâmetro / função M | `p_SiteURL`, `fn_TurnoDeMinuto` |

Sem espaço, sem acento, PascalCase depois do prefixo. **O prefixo é do desenvolvedor; o usuário vê
a coluna, não a tabela** — e as tabelas de fato ficam com colunas técnicas ocultas.

### 1.2 Norma ⛔ — Colunas em PT-BR humano; schema nunca aparece

Tradução direta da §5.3 do `GMS_Mestre.md`: `quantidade_debandagem` e `data_hora_final_tubo` são
nomes de banco. No modelo eles chegam como **"Quantidade (m)"** e **"Fim da Etapa"**. O nome
técnico só existe na camada Bronze/Prata.

Formato: `Nome do Campo` em Capitalização de Título, com unidade entre parênteses quando houver
(`Quantidade (m)`, `Tempo de Ciclo (min)`, `Custo (R$)`).

### 1.3 Norma ⛔ — Medidas

- Nome de negócio em PT-BR, **sem prefixo de tipo**, sem tabela na referência: `[Metros Produzidos]`.
- **Medida auxiliar/intermediária começa com `_` e fica oculta**: `_Metros Base`.
- Toda medida vive numa **tabela de medidas** (`_Medidas <Domínio>`), nunca solta numa tabela de fato.
- **Pasta de exibição obrigatória**, por domínio: `Produção`, `Qualidade`, `Refugo`, `Paradas`,
  `Tempo`, `Auxiliares`.
- Variação temporal vira sufixo padronizado: `[Metros Produzidos AA]` (ano anterior),
  `[Metros Produzidos MTD]`, `[Δ Metros vs. Meta]`.

**[A AUDITAR]** — as 102 medidas atuais provavelmente não seguem isso. A migração é ⚠️ progressiva:
tocou na medida, renomeia e move para a pasta. Renomear em massa quebra visual e bookmark.

## B.2 Modelagem

### 2.1 Norma ⛔ — Estrela, sentido único, sem bidirecional

Relacionamento **1→N, filtro em sentido único**, da dimensão para o fato. Bidirecional é proibido
(ambiguidade silenciosa e resultado que muda conforme o visual). Precisa cruzar? `TREATAS`,
`CROSSFILTER` local dentro de `CALCULATE`, ou tabela-ponte explícita.

### 2.2 Norma ⛔ — `dCalendario` própria, contínua, marcada como tabela de data

Gerada em Power Query (ou DAX `CALENDAR`), **sem buracos**, cobrindo do primeiro ao último dia com
dado, e marcada como Tabela de Data pela coluna `Data`. Sem isso, nenhuma função de inteligência
temporal (`DATEADD`, `SAMEPERIODLASTYEAR`, `TOTALYTD`) é confiável.

Colunas mínimas: `Data`, `Ano`, `Mês` (nome PT-BR), `Mês Nº` (para ordenação — **`Sort by Column`
obrigatório**), `Ano-Mês`, `Semana ISO`, `Dia da Semana`, `Dia Útil?`, `Ano-Semana`.

### 2.3 Norma ⛔ — `dTurno` é dimensão, não texto no fato

Três linhas, e as fronteiras reais do GMS escritas **uma vez**:

| Turno | Rótulo | Início | Fim | Minuto inicial | Minuto final |
|---|---|---|---|---|---|
| 1 | 1º Turno | 05:20 | 13:47 | 320 | 827 |
| 2 | 2º Turno | 13:48 | 22:40 | 828 | 1360 |
| 3 | 3º Turno | 22:41 | 05:19 | 1361 | 319 |

### 2.4 Norma ⛔ — Ocultar tudo que não é para o usuário

Chaves estrangeiras, colunas técnicas, colunas de ordenação e tabelas Bronze/Prata ficam
**ocultas**. Campo visível que ninguém deve arrastar sozinho não existe: ou vira medida, ou some.

### 2.5 Norma ⚠️ — Cardinalidade e integridade declaradas

Todo relacionamento com cardinalidade explícita (1:N) e, quando a integridade referencial for
garantida na Prata, **"Assumir integridade referencial" ligado** (troca `LEFT JOIN` por `INNER
JOIN` no SQL gerado — ganho real de performance).

## B.3 Power Query

### 3.1 Norma ⛔ — Nunca filtrar, ordenar ou fazer incremental por `Modified`

Mesma norma do app (`GMS_Mestre.md` §3.3), mesma causa: OP que avança de etapa tem `Modified`
atualizado e **some do histórico da etapa anterior**. Filtro e atualização incremental usam
`data_hora_final_<etapa>` → `Data de Referência`.

### 3.2 Norma ⛔ — Toda junção declara o grão e é validada por contagem

**Evidência GMS:** o pipeline `Apontamento GMS` teve uma divergência de granularidade numa junção
que **inflou a quantidade em ~20%** — número errado que passou despercebido porque a tabela
"parecia certa". Norma decorrente, em três partes:

1. Antes do `Table.NestedJoin`, escrever em comentário o grão dos dois lados e o resultado
   esperado ("esquerda 1 linha/OP × etapa; direita 1 linha/PN × BRD CODE; espera-se N:1").
2. **A chave da direita tem de ser única** — validar com `Table.Distinct` + contagem, ou usar
   `Table.Group` antes de juntar.
3. Depois do `Table.ExpandTableColumn`, **conferir `Table.RowCount` antes e depois**. Se aumentou,
   a junção duplicou linhas e o número está inflado. Isso não é opcional: é a checagem que teria
   pego os 20%.

**Lição de chave, já paga duas vezes (AM-DM-02 e `DM_TRANCAGEM`):** a granularidade dos dados
mestres de mangueira é **PARTNUMBER × BRD CODE**, não PARTNUMBER. Junção só por PARTNUMBER está
errada em qualquer lugar que ainda exista.

### 3.3 Norma ⛔ — Turno e Data de Referência resolvidos na Prata, uma vez

A virada das 05:20 é a regra mais cara de errar do GMS. Ela é resolvida **uma vez**, em M, e vira
duas colunas materializadas em todo fato. Nunca em medida, nunca no visual.

```m
// fn_MinutoDoDia — minutos desde a meia-noite
(carimbo as nullable datetime) as nullable number =>
    if carimbo = null then null
    else Time.Hour(DateTime.Time(carimbo)) * 60 + Time.Minute(DateTime.Time(carimbo))

// fn_Turno — fronteiras reais do GMS (B§2.3)
(minutos as nullable number) as nullable number =>
    if minutos = null then null
    else if minutos >= 320 and minutos < 828 then 1
    else if minutos >= 828 and minutos < 1361 then 2
    else 3

// fn_DataRef — antes das 05:20 o dia de produção ainda é o anterior
(carimbo as nullable datetime) as nullable date =>
    if carimbo = null then null
    else if fn_MinutoDoDia(carimbo) < 320
        then Date.AddDays(DateTime.Date(carimbo), -1)
        else DateTime.Date(carimbo)
```

Aplicação padrão em toda consulta `stg_`:

```m
adicionaTurno =
    Table.AddColumn(passoAnterior, "Turno",
        each fn_Turno(fn_MinutoDoDia([Fim da Etapa])), Int64.Type),
adicionaDataRef =
    Table.AddColumn(adicionaTurno, "Data de Referência",
        each fn_DataRef([Fim da Etapa]), type date)
```

### 3.4 Norma ⛔ — Tipos explícitos e locale pt-BR

Toda coluna tipada explicitamente na Prata (`Int64.Type`, `type number`, `type date`, `type text`).
Conversão de texto para número/data com locale: `Table.TransformColumnTypes(t, {{"Quantidade",
type number}}, "pt-BR")`. **Evidência GMS:** o app já pagou o bug de vírgula × ponto na
`quantidade_extracao` (patch `NumeroBR`) — a mesma armadilha existe no M e é silenciosa: sem
locale, `675,5` vira erro ou `6755`.

### 3.5 Norma ⛔ — Sem fonte Excel nova; DM_* é dimensão, nunca fato

Espelha §2.2 do `GMS_Mestre.md`. Os três `DM_*` continuam como dados mestres até a Frente 2. Nenhum
Excel novo entra no modelo, sob nenhuma justificativa — inclusive "só para o BI".

### 3.6 Norma ⚠️ — Preservar *query folding* enquanto der

Etapas dobráveis primeiro (filtro de linha, seleção de coluna, remoção), etapas não dobráveis
depois (índice, colunas customizadas com função própria). Verificar "Exibir consulta nativa"/
diagnóstico de etapa antes de aceitar consulta lenta. Colunas nunca usadas são **removidas na
Bronze** — coluna carregada é memória gasta para sempre.

### 3.7 Norma ⚠️ — Atualização incremental sobre `Data de Referência`

Quando a `fEtapaOP` passar de ~1 milhão de linhas (hoje está longe), configurar incremental com
`RangeStart`/`RangeEnd` sobre `Data de Referência`. Impossível sobre `Modified` (§3.1) — mais um
motivo para a norma.

## B.4 DAX

### 4.1 Norma ⛔ — Proibições

| ⛔ Proibido | ✅ Em vez disso |
|---|---|
| `a / b` | `DIVIDE(a, b)` — divisão por zero silenciosa vira número errado |
| Agregação implícita (arrastar coluna) | Medida nomeada (BI2) |
| `TODAY()` / `NOW()` como âncora de "hoje" | `[Data de Referência]` = `MAX(fEtapaOP[Data de Referência])` |
| Comparar data-hora com número | Colunas `Turno` / `Data de Referência` da Prata (§3.3) |
| `FILTER(fEtapaOP, ...)` (tabela inteira) | `KEEPFILTERS(VALUES(...))` ou filtro de coluna |
| Coluna sem tabela (`[Quantidade]`) | `fEtapaOP[Quantidade (m)]` |
| Medida com tabela (`_Medidas[Metros]`) | `[Metros Produzidos]` |
| Relacionamento bidirecional | `TREATAS` / `CROSSFILTER` local |
| `IFERROR` tapando buraco de dado sem MEL | Corrigir a captura (BI10) |
| Coluna calculada que poderia ser M | Fazer na Prata (BI3) |

**Sobre `TODAY()` — a armadilha mais cara:** em modelo Import, o dado só existe até o último
refresh. Uma medida que compara com `TODAY()` mostra "hoje sem produção" às 6h da manhã porque o
refresh ainda não rodou, e o supervisor conclui que a fábrica parou. A âncora é sempre o dado:

```dax
Data de Referência =
-- Último dia de produção que existe no modelo. Âncora de TODA lógica de "hoje".
CALCULATE( MAX( fEtapaOP[Data de Referência] ), REMOVEFILTERS() )
```

### 4.2 Norma ⛔ — Formatação e comentário

Toda medida: variáveis com `VAR`/`RETURN`, indentação de bloco, e **primeira linha `--` com a
definição de negócio + o MEL/Cxx de origem**. Medida sem comentário não passa no checklist.

```dax
% Refugo =
-- Refugo sobre produção boa + refugo, no mesmo recorte. Fonte: C15/C16 · MEL-xxx
VAR Bom    = [Metros Produzidos]
VAR Refugo = [Metros Refugados]
RETURN
    DIVIDE( Refugo, Bom + Refugo )
```

### 4.3 Norma ⛔ — Formato e unidade declarados na medida

Formato pt-BR definido na propriedade da medida, não no visual: `#.##0` para metros, `0,0%` para
percentual, `R$ #.##0,00` para dinheiro, `#.##0` min para tempo. Unidade no nome quando houver
ambiguidade. Isso mata a divergência entre dois visuais mostrando o mesmo número diferente.

### 4.4 Norma ⛔ — Medida quebrada sai da vista

Regra do BI7. Enquanto **MEL-087** (Meta HH, Real HH, Mangueira do Turno) não for corrigida, essas
medidas ficam ocultas e o visual exibe "indisponível", nunca um número plausível e errado.

### 4.5 Norma ⚠️ — Travessia de grafo é DAX, nunca Power Fx

Espelha o C40: `PATH()`, `PATHITEM()`, `PATHCONTAINS()` sobre a tabela de arestas
(`fFluxoEtapas` / `bGenealogia`) resolvem "por onde essa OP passou" e "que OPs usaram o lote X".
Power Fx não tem recursão — proposta de travessia no app é recusada de saída.

## B.5 Tempo, turno e a virada das 05:20

Esta seção existe porque **é o erro mais provável do BI inteiro**, e porque o app já sangrou por
ele (20 ocorrências da classe `Now() >= 6` na auditoria).

**Regra única ⛔:** o BI nunca calcula turno. Ele **lê** `Turno` e `Data de Referência`, que a
camada Prata carimbou. Uma OP que termina às 23:50 de segunda pertence ao **3º turno da
segunda-feira**; uma que termina às 04:30 de terça pertence ao **3º turno da segunda-feira**
também. É isso que a `fn_DataRef` garante e é isso que o teste do checklist verifica.

**Turno atual (para painel ao vivo)** — o único lugar onde a hora do relógio entra, e mesmo assim
isolada numa medida só:

```dax
Turno Agora =
-- Único ponto do modelo que consulta o relógio. Painel ao vivo apenas.
VAR Min = HOUR( NOW() ) * 60 + MINUTE( NOW() )
RETURN
    SWITCH( TRUE(),
        Min >= 320  && Min < 828,  1,
        Min >= 828  && Min < 1361, 2,
        3
    )
```

## B.6 Visual e tema

### 6.1 Norma ⛔ — Tema JSON único, derivado dos tokens `fx_`

O design system do GMS já existe (`GMS_Mestre.md` §5.2). O BI **não inventa paleta**: importa
`GMS_Tema_BI.json`, gerado a partir dos mesmos tokens. Hardcode de cor em visual é proibido, igual
a hardcode de `RGBA()` em controle.

Mapeamento canônico:

| Papel | Token `fx_` | Hex | Uso no BI |
|---|---|---|---|
| Marca / alerta máximo | `fx_CorPrimaria` | `#E2231A` | Só marca e exceção crítica — **nunca** cor de série padrão |
| Ação / informativo | `fx_CorInfo` | `#2C6FBF` | Série principal, links, seleção |
| OK | `fx_CorOK` | `#16A34A` | Dentro da meta |
| Alerta | `fx_CorAlerta` | `#E67E22` | Atenção |
| Erro / refugo | `fx_CorErro` | `#C0392B` | Refugo, falha |
| Processo físico | `fx_CorGelo` | `#0284C7` | Resfriamento/cura (C39) |
| Fundo | `fx_CorFundo` | `#F5F7FA` | Fundo de página |
| Superfície | `fx_CorSuperficie` | `#FFFFFF` | Cartão |
| Texto / suave / rótulo | `fx_CorTexto` / `Suave` / `Rotulo` | `#0F172A` / `#64748B` / `#94A3B8` | Hierarquia tipográfica |
| Borda | `fx_CorBorda` | `#E2E8F0` | Divisor, contorno de cartão |

**Armadilha herdada, repetida aqui de propósito:** vermelho Danfoss em gráfico de barras lê como
"tudo errado". Série padrão é `fx_CorInfo`. O vermelho é reservado.

### 6.2 Norma ⛔ — Título de visual é a pergunta respondida

"Metros por Turno" é rótulo. **"Quanto cada turno produziu esta semana?"** é título. O leitor tem
de saber o que está olhando sem legenda mental. Subtítulo carrega o recorte ativo (período,
etapa) quando não for óbvio pelo filtro.

### 6.3 Norma ⛔ — Densidade e hierarquia de página

- Máximo **8 visuais por página**; acima disso a página está fazendo o trabalho de duas.
- Canvas **1280 × 720** (16:9), grid de 12 colunas, gutter de 16 px (`fx_EspacoM`).
- **Cartões de KPI no topo**, em faixa; detalhe abaixo; tabela de auditoria por último ou em
  drill-through.
- Ordenação **sempre por valor**, decrescente — nunca alfabética, salvo eixo temporal.
- ⛔ Proibido: pizza/rosca com mais de 5 fatias, qualquer 3D, eixo Y truncado (não começando em
  zero) em gráfico de barras, gauge decorativo sem meta real.

### 6.4 Norma ⛔ — Acessibilidade e formato BR

Contraste ≥ **4.5:1** (mesma §5.5 do Mestre). Todo visual com **texto alternativo**. Nunca só cor
para codificar estado — cor + ícone/rótulo. Ordem de tabulação definida nas páginas principais.
Datas `dd/mm/aaaa`, decimal com vírgula, milhar com ponto (§B.4.3).

### 6.5 Norma ⚠️ — Filtros: o mínimo, sempre nos mesmos lugares

Painel de filtros escondido para o usuário final; segmentações visíveis apenas para
**Período**, **Turno** e **Etapa**, sempre na mesma posição (faixa superior). Sincronização de
segmentação entre páginas configurada explicitamente — segmentação que reseta ao navegar é o
motivo nº 1 de o supervisor achar que "o painel mente".

## B.7 Performance

- **Import obrigatório** para SharePoint/Excel. DirectQuery sobre SharePoint não é opção.
- Coluna não usada é **removida na Bronze**, não ocultada.
- Coluna de alta cardinalidade (data-hora completa, GUID, texto livre) é o maior custo de memória:
  data-hora separa em `Data` + `Hora` quando a granularidade de segundo não for necessária.
- ⛔ Nenhuma coluna calculada DAX que possa ser coluna M (BI3).
- Visual lento se diagnostica com o **Performance Analyzer** antes de culpar a fonte — espelha a
  norma do Monitor (§7.5 do Mestre): medir antes de acusar.
- Capacidade Pro: até **8 atualizações/dia**. Painel "ao vivo" em Pro é uma promessa que o modelo
  não cumpre — o rótulo de "atualizado às HH:MM" é obrigatório (§B.8.3).

## B.8 Governança, publicação e segurança

### 8.1 Norma ⛔ — Dois workspaces, um app

`GMS — Desenvolvimento` (edição) e `GMS — Produção` (publicação). O usuário final consome pelo
**app do Power BI**, nunca pelo workspace. Ninguém edita em produção.

### 8.2 Norma ⛔ — Arquivo em formato `.pbip` + Git

Espelha §7.4 do `GMS_Mestre.md` (Git integration como ALM oficial): o relatório é salvo em
**`.pbip`** (modelo em TMDL, relatório em JSON), versionado em Git. Diff legível de medida é o que
torna possível revisar mudança de número. `.pbix` binário sem histórico é o equivalente BI do
publish sem commit message.

### 8.3 Norma ⛔ — Todo relatório declara sua idade e seu dono

Rodapé fixo em toda página: **"Atualizado em: dd/mm/aaaa hh:mm"** (medida sobre a hora do refresh,
convertida para America/Sao_Paulo) + nome do responsável. Painel sem carimbo de atualização perde
a confiança na primeira vez que alguém duvida dele.

```dax
Última Atualização =
-- Carimbo de refresh convertido para o fuso da fábrica (UTC-3).
"Atualizado em " & FORMAT( MAX( dAtualizacao[Horário UTC] ) - (3/24), "dd/mm/yyyy hh:mm" )
```

(`dAtualizacao` é uma consulta Prata de uma linha com `DateTime.FixedLocalNow()` em UTC.)

### 8.4 Norma ⚠️ — RLS por área, testada antes de publicar

Papéis mínimos: `Célula Mangueiras`, `Montagem`, `Qualidade`, `Liderança` (sem filtro).
Testar com "Exibir como" antes de publicar — RLS não testada é vazamento ou tela vazia, e as duas
descobrem no pior momento.

### 8.5 Norma ⚠️ — Um dono por relatório, escrito no diário

Relatório sem dono nomeado vira relatório abandonado com número errado. O dono entra como linha
`NORMA` no `GMS_Diario.md` quando o relatório é publicado.

## B.9 Checklist pré-publicação ⛔

Espelha o §7.2 do `GMS_Mestre.md`. Verde em todos, sempre:

1. **Grão declarado** — toda tabela de fato tem a frase "1 linha = ___" na descrição.
2. **Contagem de junção** — nenhuma junção aumentou linha sem justificativa escrita (§B.3.2).
3. **Teste da virada de turno** — um registro às 05:19 e outro às 05:21 caem em dias de produção
   diferentes; um às 23:50 e outro às 04:30 caem no mesmo `Data de Referência`.
4. **Conferência numérica contra a origem** — um dia × um turno × uma etapa conferido contra a tela
   do app e contra o CSV. Sem isso a publicação não acontece (BI1).
5. **Zero agregação implícita** — nenhum visual com coluna arrastada direto.
6. **Zero medida quebrada visível** (BI7 / MEL-087).
7. **Formato pt-BR** em toda medida numérica, data e percentual.
8. **Tema aplicado**, zero cor hardcoded, contraste ≥ 4.5:1, texto alternativo presente.
9. **Performance Analyzer** rodado: nenhum visual acima de ~3 s na página principal.
10. **RLS testada** com "Exibir como" para cada papel.
11. **Carimbo de atualização e dono** visíveis no rodapé.
12. **Linhas de diário escritas** (BI9).

---

# PARTE C — CATÁLOGO DE KPIs

**Como ler:** cada KPI traz **Pergunta que responde → Definição de negócio → DAX canônico → Grão e
fonte → Armadilha (o que faz esse número mentir) → Conceito** do `GMS_Mestre.md`.

**Regra de ouro do catálogo ⛔:** o que está aqui é a **única** definição válida no GMS. Divergiu,
não é "outra visão do indicador" — é bug. Alteração de definição vira linha `NORMA` no diário.

As colunas usadas abaixo assumem o modelo alvo da Parte A. Onde o modelo atual divergir, a
adaptação é da consulta, nunca da definição.

## C.1 Produção

### K01 · Metros Produzidos
**Pergunta:** quanto a célula entregou no recorte?
**Definição:** soma da metragem registrada como concluída na etapa, no período/turno selecionado.
Etapa não concluída não conta.

```dax
Metros Produzidos =
-- Metragem concluída por etapa no recorte. Base de quase todo o resto. C13
CALCULATE(
    SUM( fEtapaOP[Quantidade (m)] ),
    NOT ISBLANK( fEtapaOP[Fim da Etapa] )
)
```

**Grão/fonte:** `fEtapaOP` (1 OP × etapa) ← `ficha_producao`.
**Armadilha:** sem filtro de etapa, isso **soma a mesma mangueira oito vezes** (uma por etapa) — é
o erro nº 1 de quem monta o primeiro painel. Todo visual de metros carrega recorte de etapa
explícito, ou usa K02.
**Conceito:** C13.

### K02 · Metros Equivalentes (produção da célula)
**Pergunta:** quanto a célula produziu *de verdade*, sem contar oito vezes?
**Definição:** metragem contada **uma única vez por OP**, na etapa de referência da célula
(Finalização — a última do fluxo).

```dax
Metros Equivalentes =
-- Conta a OP uma vez só, na etapa terminal. Antídoto da contagem óctupla de K01. C22
CALCULATE(
    [Metros Produzidos],
    KEEPFILTERS( dEtapa[Etapa] = "Finalização" )
)
```

**Armadilha:** muda se o roteiro mudar (família que pula etapa). Quando a `fFluxoEtapas` virar
autoritativa (C40), a etapa terminal passa a ser lida da tabela, não escrita na medida.

### K03 · OPs Concluídas
```dax
OPs Concluídas =
-- OPs que fecharam a etapa terminal no recorte.
CALCULATE(
    DISTINCTCOUNT( fEtapaOP[OP] ),
    NOT ISBLANK( fEtapaOP[Fim da Etapa] ),
    KEEPFILTERS( dEtapa[Etapa] = "Finalização" )
)
```

### K04 · WIP em Processo (por etapa)
**Pergunta:** quantas OPs estão dentro de cada etapa agora?
```dax
WIP em Processo =
-- Iniciou a etapa e não fechou. Ignora recorte de data: WIP é foto, não fluxo.
CALCULATE(
    DISTINCTCOUNT( fEtapaOP[OP] ),
    NOT ISBLANK( fEtapaOP[Início da Etapa] ),
    ISBLANK( fEtapaOP[Fim da Etapa] ),
    REMOVEFILTERS( dCalendario )
)
```
**Armadilha:** **OP zumbi**. A auditoria achou OP parada há 4.162 h. Ela infla o WIP para sempre.
Todo visual de WIP acompanha K18 e um teto visual (§B.6.3), senão o gargalo apontado é fantasma.
**Conceito:** C3, C1.

### K05 · Vazão do Turno
```dax
Vazão do Turno =
-- Metros concluídos por turno na etapa selecionada. Denominador do Radar de Gargalo. C3
DIVIDE(
    [Metros Produzidos],
    DISTINCTCOUNT( fEtapaOP[Turno] )
)
```

### K06 · Índice de Gargalo (Radar — C3)
**Definição:** razão entre fila acumulada e vazão recente. A etapa com maior índice é o tambor do
dia.
```dax
Índice de Gargalo =
-- WIP dividido pela vazão média das últimas 3 datas de produção. Maior = restrição. C3
VAR VazaoRecente =
    CALCULATE(
        AVERAGEX( VALUES( dCalendario[Data] ), [Metros Produzidos] ),
        DATESINPERIOD( dCalendario[Data], [Data de Referência], -3, DAY )
    )
RETURN
    DIVIDE( [WIP em Processo] * [Metragem Média por OP], VazaoRecente )
```
**Armadilha:** com menos de 3 dias de dado na etapa o índice oscila. Só exibir quando a vazão
recente for maior que zero — senão o painel elege gargalo por divisão instável.

## C.2 Tempo

### K07 · Tempo de Ciclo da Etapa (mediana)
**Definição:** mediana — não média — do tempo entre início e fim da etapa, por OP.
```dax
Tempo de Ciclo (min) =
-- Mediana do início→fim por OP. Mediana porque a média é sequestrada pela OP zumbi. C19 C37
MEDIANX(
    FILTER(
        fEtapaOP,
        NOT ISBLANK( fEtapaOP[Início da Etapa] )
            && NOT ISBLANK( fEtapaOP[Fim da Etapa] )
    ),
    DATEDIFF( fEtapaOP[Início da Etapa], fEtapaOP[Fim da Etapa], MINUTE )
)
```
**Armadilha:** **média aqui mente sempre.** Uma OP esquecida aberta por 4.162 h desloca a média e
não desloca a mediana. Todo lead time do GMS é mediana, e o P90 vai ao lado quando a decisão
depende da cauda.
**Conceito:** C4, C19, C37 (por posto, o ciclo por tecnologia de solda finalmente é honesto).

### K08 · Lead Time Total da OP
```dax
Lead Time Total (h) =
-- Primeira entrada até última saída da OP, em horas. C4
VAR Inicio = MIN( fEtapaOP[Início da Etapa] )
VAR Fim    = MAX( fEtapaOP[Fim da Etapa] )
RETURN
    DIVIDE( DATEDIFF( Inicio, Fim, MINUTE ), 60 )
```

### K09 · Idade da OP na Etapa / OPs Zumbi
```dax
Idade na Etapa (h) =
-- Quanto tempo a OP está parada na etapa atual. Alimenta o Andon. C1 C2
DIVIDE( DATEDIFF( MAX( fEtapaOP[Início da Etapa] ), NOW(), MINUTE ), 60 )

OPs Zumbi =
-- OPs abertas há mais que o teto configurado (padrão 72 h). Exceção, não estatística. C1
COUNTROWS(
    FILTER(
        VALUES( fEtapaOP[OP] ),
        [Idade na Etapa (h)] > 72
    )
)
```

## C.3 Qualidade e refugo

### K10 · Metros Refugados
```dax
Metros Refugados =
-- Refugo consolidado das três origens (linha, bobinadeira, extrusora). C16
SUM( fRefugo[Quantidade (m)] )
```

### K11 · % Refugo
```dax
% Refugo =
-- Refugo sobre o total processado no mesmo recorte. C15 C16
VAR Bom = [Metros Produzidos]
VAR Ruim = [Metros Refugados]
RETURN
    DIVIDE( Ruim, Bom + Ruim )
```
**Armadilha:** numerador e denominador **têm de ser do mesmo recorte de etapa**. Refugo da
Trançagem sobre produção de todas as etapas dá um percentual bonito e falso.

### K12 · Custo do Refugo (R$) — C15
```dax
Custo do Refugo =
-- Metros refugados × custo padrão por metro da família. Metro não sensibiliza diretoria; R$ sim.
SUMX(
    fRefugo,
    fRefugo[Quantidade (m)]
        * RELATED( dMangueira[Custo Padrão (R$/m)] )
)
```
**Pendência de insumo:** a tabela de custo padrão por família **ainda não existe** — é o único
insumo que falta para o C15 sair do papel. Enquanto não existir, a medida fica oculta (BI7), não
estimada.

### K13 · Pareto de Causa (% acumulado) — C16
```dax
% Acumulado do Pareto =
-- Curva de Pareto sobre causa de refugo. Ordena a decisão da semana. C16
VAR CausaAtual = [Metros Refugados]
VAR Total = CALCULATE( [Metros Refugados], REMOVEFILTERS( dCausaRefugo ) )
VAR Acumulado =
    CALCULATE(
        [Metros Refugados],
        FILTER(
            ALL( dCausaRefugo[Causa] ),
            CALCULATE( [Metros Refugados] ) >= CausaAtual
        )
    )
RETURN
    DIVIDE( Acumulado, Total )
```

### K14 · Cpk do Diâmetro — C5
```dax
Cpk =
-- Capacidade do processo contra a spec do Delineamento. < 1,33 = processo não capaz.
VAR Media  = AVERAGE( fInspecao[Diâmetro Externo] )
VAR Desvio = STDEV.S( fInspecao[Diâmetro Externo] )
VAR LSE    = MAX( dDelineamento[Diâmetro Externo Máx] )
VAR LIE    = MIN( dDelineamento[Diâmetro Externo Mín] )
RETURN
    DIVIDE( MIN( LSE - Media, Media - LIE ), 3 * Desvio )
```
**Armadilha ⛔ de unidade:** a aba `Dados Mang` do AM-DM-02 traz a spec em **polegada**; o operador
pode estar digitando em milímetro. Enquanto a pendência de unidade (MEL-091/MEL-097) estiver
aberta, **este KPI fica oculto** — Cpk com unidade trocada é o número mais perigoso do catálogo.
**Conceito:** C5, C26.

## C.4 Aderência e paradas

### K15 · Meta / Real / Aderência Hora-Hora — C13, **MEL-087**
```dax
Real HH =
-- Metros apontados na janela horária do processo. C13
SUM( fHoraHora[Real (m)] )

Meta HH =
-- Meta da janela = velocidade da mangueira × minutos disponíveis da janela. C13
SUMX(
    fHoraHora,
    fHoraHora[Minutos Disponíveis] * RELATED( dMangueira[Velocidade (m/min)] )
)

Aderência HH =
DIVIDE( [Real HH], [Meta HH] )
```
**Estado:** as três medidas correspondentes **estão quebradas hoje** (MEL-087). Esta é a definição
canônica para a restauração; a versão que voltar tem de bater com a tela do Hora-Hora no app antes
de ser exibida.

### K16 · Aderência ao Plano — C22
```dax
Aderência ao Plano =
-- % de OPs concluídas até a data planejada. O "E" do SQDC (C7).
VAR NoPrazo =
    CALCULATE(
        DISTINCTCOUNT( dOP[OP] ),
        FILTER( dOP, dOP[Data de Conclusão] <= dOP[Data Planejada] )
    )
RETURN
    DIVIDE( NoPrazo, [OPs Concluídas] )
```

### K17 · Tempo Parado, MTBF e MTTR — C19
```dax
Tempo Parado (min) = SUM( fParada[Duração (min)] )

MTTR (min) =
-- Tempo médio de reparo por evento de parada.
DIVIDE( [Tempo Parado (min)], COUNTROWS( fParada ) )

MTBF (h) =
-- Tempo operando dividido pelo número de falhas. Só falhas, não parada programada.
VAR Falhas = CALCULATE( COUNTROWS( fParada ), dMotivoParada[Tipo] = "Falha" )
VAR MinutosDisponiveis = [Minutos Programados] - [Tempo Parado (min)]
RETURN
    DIVIDE( MinutosDisponiveis, Falhas * 60 )
```
**Armadilha:** MTBF só significa alguma coisa se `dMotivoParada` distinguir **falha** de **parada
programada** (setup, refeição, manutenção preventiva). Sem essa classificação, o número existe e
não quer dizer nada.

### K18 · OEE-lite
```dax
Disponibilidade = DIVIDE( [Minutos Programados] - [Tempo Parado (min)], [Minutos Programados] )
Performance     = DIVIDE( [Real HH], [Meta HH] )
Qualidade       = 1 - [% Refugo]
OEE             = [Disponibilidade] * [Performance] * [Qualidade]
```
**Honestidade obrigatória ⛔:** enquanto Meta HH depender de velocidade cadastrada (não medida por
sensor) e as paradas não estiverem completas em todas as etapas, **isto é OEE-lite e deve estar
rotulado assim no visual**. Chamar de OEE um número que a manutenção pode contestar queima a
confiança do painel inteiro — e confiança é o produto nº 1 (pilar 1). Vira OEE de verdade quando o
Factbird entrar (C20).

## C.5 Fluxo e material

### K19 · Furo de FIFO — C11
```dax
% Furo de FIFO =
-- Consumos fora da ordem de chegada sobre o total de consumos da bobinadeira.
DIVIDE(
    CALCULATE( COUNTROWS( fCarretel ), fCarretel[Fora de Ordem] = TRUE() ),
    COUNTROWS( fCarretel )
)
```

### K20 · OP Health Score — C2
```dax
OP Health Score =
-- 0–100. Quatro fatores, pesos em dConfiguração para a fábrica calibrar sem republicar.
VAR fIdade   = 1 - DIVIDE( [Idade na Etapa (h)], [Lead Time Alvo da Etapa (h)] )
VAR fRefugo  = 1 - DIVIDE( [% Refugo], [Tolerância de Refugo] )
VAR fValidade= IF( [Dias para Vencer o Composto] < 7, 0, 1 )
VAR fRetrab  = 1 - DIVIDE( [Edições na Ficha], 5 )
RETURN
    100 * MAX( 0,
        0.4 * fIdade + 0.3 * fRefugo + 0.2 * fValidade + 0.1 * fRetrab
    )
```
**Nota:** os pesos são a proposta inicial. Eles moram em tabela de configuração, não na medida —
calibrar peso não pode exigir republicar o modelo.

---

# PARTE D — DESENHO DOS RELATÓRIOS

**Regra de fundação ⛔:** **uma página = uma decisão = um público.** Página que serve a dois
públicos não serve a nenhum: o supervisor precisa de 15 segundos e a liderança precisa de tendência
— são desenhos diferentes do mesmo dado. Se você não consegue escrever numa frase que decisão a
página habilita, a página não deve existir.

## D.0 Estrutura do arquivo

Um `.pbip` por **público**, não por assunto. Três arquivos:

| Arquivo | Público | Ritmo |
|---|---|---|
| `GMS_Operacao.pbip` | Supervisão da célula, líderes de turno | ao longo do turno |
| `GMS_Gestao.pbip` | Liderança, reunião Tier/SQDC | diário/semanal |
| `GMS_Qualidade.pbip` | Qualidade, engenharia | por evento/semanal |

Todos consomem **o mesmo modelo semântico compartilhado** (publicado uma vez, conectado por *live
connection*). Modelo duplicado = definição duplicada = o problema que a Parte C existe para matar.

## D.1 Template de página

```
┌──────────────────────────────────────────────────────────────────────┐
│ FAIXA DE TÍTULO (56px)  logo · título-pergunta · Período · Turno · Etapa │
├──────────────────────────────────────────────────────────────────────┤
│ FAIXA DE KPI (110px)   3 a 5 cartões · valor grande · Δ vs. período   │
├───────────────────────────────────────┬──────────────────────────────┤
│ VISUAL PRINCIPAL (2/3)                │ APOIO (1/3)                  │
│ a resposta da pergunta do título      │ ranking / composição         │
├───────────────────────────────────────┴──────────────────────────────┤
│ DETALHE — tabela ou barra por categoria (drill-through para auditoria)│
├──────────────────────────────────────────────────────────────────────┤
│ RODAPÉ (24px)  Atualizado em dd/mm/aaaa hh:mm · Dono: <nome>          │
└──────────────────────────────────────────────────────────────────────┘
```

Regras: cartão de KPI mostra **valor + variação + microtendência**, nunca valor solto; o visual
principal responde ao título; **toda página tem drill-through para a página de auditoria** (D.9);
seleção em qualquer visual filtra a página inteira (interação cruzada explícita, nunca padrão).

## D.2 `Operação` · Página 1 — **Como está o turno agora?**
**Público:** supervisão · **Decisão:** onde gastar os próximos 15 minutos (C1, C3).

- KPIs: Metros do Turno · Aderência HH · % Refugo do Turno · WIP total · OPs Zumbi.
- Principal: **Radar de Gargalo** — barras horizontais por etapa, ordenadas por K06, a etapa do
  topo destacada em `fx_CorPrimaria` com o rótulo "Gargalo agora".
- Apoio: **Andon** — lista de exceções ordenada por severidade (OP zumbi, refugo acima do teto,
  composto vencendo, SPC fora de controle). Cada linha = 1 exceção + a ação sugerida.
- Detalhe: WIP por etapa × turno.
- Recorte padrão: turno atual (`[Turno Agora]`), não "hoje".

## D.3 `Operação` · Página 2 — **Cada etapa está no ritmo?**
**Público:** supervisão e líder de etapa · **Decisão:** onde colocar gente e hora extra.

- Pequenos múltiplos: uma mini-área por etapa, Real vs. Meta HH ao longo do turno.
- Tabela: Etapa · WIP · Vazão · Ciclo mediano · P90 · Aderência HH.
- Alerta visual só quando Aderência < 90 % — página cheia de vermelho vira ruído e o supervisor
  para de olhar (mesma lógica do C24: alerta sem contexto mata o Andon).

## D.4 `Operação` · Página 3 — **Diário de Bordo** (C25)
**Público:** supervisão, passagem de turno · **Decisão:** o turno que entra começa sabendo.

- Filtros no topo: Data de Referência · Turno · Processo.
- Tabela linha a linha: Hora · OP · Mangueira · Metragem · Diâmetros · Operador · Posto.
- Ordenada por hora, respeitando a virada 05:20.
- **Exportação habilitada nesta página** — é a página de auditoria diária.

## D.5 `Gestão` · Página 1 — **Quadro SQDC** (C7)
**Público:** liderança, reunião Tier · **Decisão:** reunião de 10 min olhando pra frente.

Quatro blocos fixos, um por letra. **S** entra manual (a única entrada humana do painel);
**Q** = % Refugo + Custo do Refugo; **D** = Aderência ao Plano; **C** = Custo do Refugo acumulado.
Cada bloco: valor do dia, tendência de 4 semanas, semáforo contra meta.

## D.6 `Gestão` · Página 2 — **Tendência e comparação**
Semana a semana e turno a turno: Metros Equivalentes, % Refugo, Aderência. Comparação **entre
turnos** é a leitura de gestão mais pedida e a mais fácil de errar — só usar K02, nunca K01.

## D.7 `Qualidade` · Página 1 — **SPC ao vivo** (C5)
Carta X̄-R por mangueira/trançadeira, limites da spec do Delineamento, alerta de tendência
(7 pontos subindo, ponto fora de 3σ). Bloqueada até a pendência de unidade fechar (K14).

## D.8 `Qualidade` · Página 2 — **Pareto de refugo** (C16)
Barras por causa + curva de % acumulado (K13). Segmentações: período, etapa, máquina, turno,
mangueira. Uma frase de destaque: *"3 causas explicam 80 % do refugo desta semana."*

## D.9 Página de auditoria (todos os arquivos)
Página **oculta**, alvo de drill-through de todas as demais. Tabela crua com a chave (OP, etapa,
carimbos, operador, posto), exportação liberada. É o que permite responder "de onde saiu esse
número" em segundos — e é o que sustenta o BI1.

## D.10 O que **não** fazer
- ⛔ Página "geral" com 20 visuais que ninguém abre duas vezes.
- ⛔ Mesmo KPI com número diferente em duas páginas (viola BI2 — sempre é filtro implícito
  esquecido).
- ⛔ Gráfico de pizza de refugo por causa: são muitas causas; é Pareto.
- ⛔ Painel de TV com segmentação — TV não tem mouse. A página de TV é fixa, recorte travado.

---

# PARTE E — REFERÊNCIAS

**Microsoft Learn:**
- Star schema and the importance for Power BI — `learn.microsoft.com/power-bi/guidance/star-schema`
- DAX best practices (DIVIDE, variáveis, contexto) — `learn.microsoft.com/dax/best-practices/`
- Date tables e Mark as date table — `learn.microsoft.com/power-bi/guidance/model-date-tables`
- Bi-directional relationship guidance — `learn.microsoft.com/power-bi/guidance/relationships-bidirectional-filtering`
- Query folding guidance / Power Query best practices — `learn.microsoft.com/power-query/best-practices`
- Incremental refresh — `learn.microsoft.com/power-bi/connect-data/incremental-refresh-overview`
- Row-level security — `learn.microsoft.com/power-bi/enterprise/service-admin-rls`
- Power BI project (.pbip) e TMDL — `learn.microsoft.com/power-bi/developer/projects/`
- Report design e acessibilidade — `learn.microsoft.com/power-bi/create-reports/desktop-accessibility-overview`

**Comunidade de referência:** SQLBI (Marco Russo / Alberto Ferrari) para padrões DAX e modelagem;
Power Query M reference para as funções de junção e validação de grão.

**Interno GMS:**
- `GMS_Mestre.md` v2.0 — Parte B (§3.3 `Modified`, §5.2 tokens, §5.5 contraste, §7.2 checklist,
  §7.4 Git), Parte C (C2, C3, C5, C13, C15, C16, C19, C22, C25, C40).
- Lição do pipeline `Apontamento GMS`: divergência de granularidade em junção → ~20 % de inflação
  de quantidade.
- Lição AM-DM-02 + `DM_TRANCAGEM`: chave de dados mestres é PARTNUMBER × BRD CODE.
- MEL-087 (3 medidas quebradas), MEL-012 (índices no SharePoint), MEL-075 (Named Formulas voláteis).

---

# ANEXO — O QUE FALTA PARA ESTE DOCUMENTO SAIR DE [A AUDITAR]

1. **Modelo semântico atual** (`.pbip`/TMDL ou `model.bim`): as 102 medidas, tabelas,
   relacionamentos e papéis RLS. Sem isso, a Parte B é norma-alvo e não diagnóstico.
2. **Tabela de custo padrão por família de mangueira** (R$/m) — único insumo que falta para K12/C15.
3. **Classificação de motivo de parada** em falha × programada — sem ela K17 (MTBF) não significa
   nada.
4. **Unidade digitada pelo operador** (polegada × milímetro) — trava K14/SPC (MEL-091/MEL-097).
5. **Velocidade por mangueira** confirmada (`DM_Velocidade`, 83 pares) — denominador da Meta HH
   (K15/MEL-087).
