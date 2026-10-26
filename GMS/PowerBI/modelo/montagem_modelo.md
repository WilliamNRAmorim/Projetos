# Montagem no modelo (GMS): passos para colar no Desktop

26/10/2026 · gerado a partir da leitura do modelo publicado "(GMS)" (somente leitura) · **nada disto foi aplicado**.

## O que o modelo já tem (conferido no modelo publicado)

- `Producao_Montagem[Data]` → `dCalendario[Date]` ativo, 1:N. `Paradas_Montagem[Data]` → `dCalendario[Date]` ativo. Ou seja, **a Data já liga**; o que faltava era o filtro de período no relatório (feito: `SEG_MES` nas páginas da Montagem).
- `Paradas_Montagem[Motivo]` → `dMotivoParada[Motivo]` ativo.
- `InicioEm`, `FimEm` e `RegistradoEm` ligam em tabelas de data automáticas (`LocalDateTable_…`). Pode desligar a data automática do modelo depois.
- `dMetaMontagem` (11 linhas: Celula, Turno, Meta) **não tem relacionamento nenhum**. As medidas `Real Montagem`, `Meta Montagem Dia`, `Tempo Parado Montagem (min)` e `% Montagem` cruzam por `TREATAS(VALUES(dMetaMontagem[…]))`.
- Não existe `dTurno` nem dimensão de célula.
- Não existe Hora-Hora da Montagem neste modelo (só existe o modelo separado "Hora-Hora Montagem (GMS)", sem atualização desde 13/07).

## Causa de "só aparece FF1 1º turno" / `Real Montagem` vazio

`Producao_Montagem[Celula]` e `[Turno]` chegam com **espaço à esquerda** (`[ FF2]`, `[ 2º Turno]`); `dMetaMontagem` vem sem espaço (`[HIGH]`, `[2º Turno]`). O `TREATAS` não casa. Também há `Fire`/`FIRE` e `Bundle`/`BUNDLE`.

## Passo 1 — Power Query: limpar o texto (3 tabelas)

Em **`Producao_Montagem`**, **`Paradas_Montagem`** e **`dMetaMontagem`**: Transformar dados → Editor Avançado → na **última linha**, troque `in <UltimoPasso>` por (o nome do passo continua o mesmo):

```m
in
    Table.TransformColumns(<UltimoPasso>, {{"Turno", each Text.Upper(Text.Trim(_)), type text}, {"Celula", each Text.Upper(Text.Trim(_)), type text}})
```

Se a tabela já tiver o passo com `Text.Trim` (MEL-141), troque só o `Text.Trim(_)` por `Text.Upper(Text.Trim(_))`.
Depois: Fechar e aplicar.

## Passo 2 — Dimensões (tabelas calculadas, Modelagem → Nova tabela)

```dax
dTurno =
DATATABLE ( "Turno", STRING, "Ordem", INTEGER,
    { { "1º TURNO", 1 }, { "2º TURNO", 2 }, { "3º TURNO", 3 } } )
```

```dax
dCelulaMontagem =
DISTINCT (
    UNION (
        SELECTCOLUMNS ( Producao_Montagem, "Celula", Producao_Montagem[Celula] ),
        SELECTCOLUMNS ( Paradas_Montagem, "Celula", Paradas_Montagem[Celula] ),
        SELECTCOLUMNS ( dMetaMontagem, "Celula", dMetaMontagem[Celula] )
    )
)
```

Observação: com `Text.Upper` o rótulo do turno vira `1º TURNO`. Se preferir manter `1º Turno`, use só `Text.Trim` no Passo 1 e escreva a dimensão com `"1º Turno"`; o que importa é a dimensão e as três tabelas terem exatamente o mesmo texto.

## Passo 3 — Relacionamentos (Visão de modelo, todos 1:N, filtro em um sentido, da dimensão para o fato)

| Dimensão | Fato | Coluna |
|---|---|---|
| `dTurno[Turno]` | `Producao_Montagem[Turno]` | Turno |
| `dTurno[Turno]` | `Paradas_Montagem[Turno]` | Turno |
| `dTurno[Turno]` | `dMetaMontagem[Turno]` | Turno |
| `dCelulaMontagem[Celula]` | `Producao_Montagem[Celula]` | Celula |
| `dCelulaMontagem[Celula]` | `Paradas_Montagem[Celula]` | Celula |
| `dCelulaMontagem[Celula]` | `dMetaMontagem[Celula]` | Celula |

Marque `dTurno[Ordem]` como "Classificar por" em `dTurno[Turno]`.

## Passo 4 — Medidas (substituem as atuais, mesmo nome, sem `TREATAS`)

Confirme o nome da coluna de meta em `dMetaMontagem` (abaixo: `[Meta]`).

```dax
Real Montagem = SUM ( Producao_Montagem[QtdProduzida] )
```

```dax
Meta Montagem Dia =
-- soma a meta (célula × turno) uma vez por dia COM produção no contexto; dia sem produção não gera meta
SUMX (
    FILTER ( VALUES ( dCalendario[Date] ), [Real Montagem] > 0 ),
    CALCULATE ( SUM ( dMetaMontagem[Meta] ) )
)
```

```dax
% Montagem = DIVIDE ( [Real Montagem], [Meta Montagem Dia] )
```

```dax
Tempo Parado Montagem (min) =
CALCULATE (
    SUM ( Paradas_Montagem[TempoParadoMin] ),
    NOT ( Paradas_Montagem[Motivo] IN { "RF - Refeição", "TE - Tempo Excedido" } )
)
```

`Horas Decimais Montagem`, `Célula Gargalo Montagem`, `Motivo Mais Frequente Montagem` e `% Montagem c/ Seta` não foram alteradas aqui; revise-as depois do Passo 4, porque lêem as medidas acima.

## Passo 5 — Decisões suas

1. **Metas faltando** em `dMetaMontagem`: FIRE, AUW, AGCO, BUNDLE no 2º turno e o 3º turno de todas. Sem linha de meta, essas células ficam sem meta (não somem mais do Real).
2. **"Dia com produção"** na `Meta Montagem Dia`: é regra de negócio (dia sem produção não gera meta). O `revisor` deve conferir; não rodou nesta sessão.
3. **Hora-Hora da Montagem**: incluir a lista `HoraHora_Montagem` neste modelo (mesmo padrão de `fHoraHora`) é um passo à parte, não feito.
4. **Tempo Excedido "31M"**: ainda sem causa. Depois do Passo 1, rode no Desktop a consulta DAX de diagnóstico (maior TempoParadoMin por Motivo).

## Relatório (já no `gerar_relatorio.py`)

- Páginas "Produção Mont." (nova) e "Paradas Mont." com período pelo `dCalendario` (mesmo grupo de sincronização das outras páginas), Turno e Célula.
- Medidas de relatório novas (`reportExtensions.json`): `OTs Montagem`, `Horas de OT Montagem`, `Peças por Hora Montagem`, `Parada Real Montagem (min)`, `Minutos Brutos Montagem`.
- Aderência e meta ficam fora do relatório até o Passo 3 e o Passo 4 serem aplicados.
