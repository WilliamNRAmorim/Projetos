# DAX do simulador de headcount x demanda (trançagem -> cabine)

Para colar no PC do Power BI. Segue o `GMS/GMS_Mestre_BI.md` (nomes humanos, estrela, filtro em sentido único, sem bidirecional).
**Os nomes de tabela e coluna abaixo são os do simulador (tabelas novas e isoladas, sem relacionamento com o modelo).** Nada aqui depende de coluna do modelo do William; quando ele mandar o export/TMDL, só a seção 5 (backtest no BI) precisa de ajuste.

**Estado: PROVISÓRIO.** A calibração usa "quem apontou" (operadores distintos) como headcount. O backtest fora da amostra não atingiu a meta de 10-15% por dia e perde para a mediana ingênua na maioria das etapas (números atuais em `backtest_simulador.md`, que se atualiza a cada rodada). **Não usar o resultado como promessa de entrega até recalibrar com a escala real.** Mostrar no visual o rótulo "calibração provisória".

## 1. Tabelas

### 1.1 `tCalibracao` (importar `parametros_simulador.csv`, UTF-8)
Colunas: `tipo`, `etapa`, `familia`, `turno`, `metrica`, `valor` (decimal), `n`, `obs`. Tipar `turno` como texto ("1", "2", "3", "todos") e `valor` como número decimal. Atualiza rodando `calibrar_simulador.py` e recarregando o CSV.

Códigos de `etapa`: `tranc`, `cob`, `band`, `vulc`, `deb`, `cab`.

### 1.2 `tEtapaSim` (Enter Data, 6 linhas)
| Etapa | Ordem | Código |
|---|---|---|
| Trançagem | 1 | tranc |
| Cobertura | 2 | cob |
| Bandagem | 3 | band |
| Vulcanização | 4 | vulc |
| Debandagem | 5 | deb |
| Extração/Cabine | 6 | cab |

Ordenar `Etapa` por `Ordem`.

### 1.3 `tCenario` (Enter Data, 18 linhas: etapa x turno): é o "e se" de pessoas
Colunas `Código` (texto), `Turno` (texto "1","2","3"), `Pessoas` (inteiro). Preencher com o cenário (começa com a mediana de pessoas do histórico ou a escala real). O usuário edita no Power Query (Enter Data) ou troca por uma tabela da escala real. Sem relacionamento.

### 1.4 Parâmetros "e se" (Modelagem > Novo parâmetro, ou DAX)
```dax
p_Demanda = GENERATESERIES( 0, 60000, 500 )     -- metros por dia
p_Fator   = GENERATESERIES( 0.8, 1.5, 0.05 )    -- fator k de produtividade (padrão 1,20 = calibrado)
```
O Power BI cria as medidas `p_Demanda Valor` e `p_Fator Valor`. Defina o padrão do `p_Fator` no k que o `backtest_simulador.md` reporta como escolhido (1,2 na rodada atual; atualizar à mão quando recalibrar) e o de `p_Demanda` no valor da demanda do dia. Se preferir 6 parâmetros de pessoas em vez da `tCenario`, crie `GENERATESERIES(0, 40, 1)` por etapa e troque `[Pessoas Etapa Turno]` abaixo.

## 2. Medidas (pasta de exibição `Simulador`)

```dax
Demanda (m/dia) =
-- Demanda escolhida no parâmetro. Provisório.
SELECTEDVALUE( p_Demanda[p_Demanda], 0 )

Fator k =
SELECTEDVALUE( p_Fator[p_Fator], 1.2 )

Minutos do Turno =
-- NORMA 27/10/2026 (MEL-250): T1 517, T2 503, T3 420. Vêm da tCalibracao.
VAR _t = SELECTEDVALUE( tCenario[Turno] )
RETURN
    CALCULATE(
        MAX( tCalibracao[valor] ),
        tCalibracao[tipo] = "turno",
        tCalibracao[metrica] = "minutos",
        tCalibracao[turno] = _t
    )

Pessoas Etapa Turno =
SUM( tCenario[Pessoas] )

Produtividade (m/pessoa·min) =
-- Mediana calibrada da etapa e do turno em contexto.
VAR _e = SELECTEDVALUE( tEtapaSim[Código] )
VAR _t = SELECTEDVALUE( tCenario[Turno] )
RETURN
    CALCULATE(
        MAX( tCalibracao[valor] ),
        tCalibracao[tipo] = "produtividade",
        tCalibracao[etapa] = _e,
        tCalibracao[familia] = "todas",
        tCalibracao[turno] = _t,
        tCalibracao[metrica] = "mediana_m_pessoa_min"
    )

Teto Turno (m) =
-- Teto empírico (p95 de metros por data_ref-turno). Não é limite físico medido.
VAR _e = SELECTEDVALUE( tEtapaSim[Código] )
RETURN
    CALCULATE(
        MAX( tCalibracao[valor] ),
        tCalibracao[tipo] = "teto",
        tCalibracao[etapa] = _e,
        tCalibracao[metrica] = "p95_metros_data_ref_turno"
    )

Teto Dia (m) =
VAR _e = SELECTEDVALUE( tEtapaSim[Código] )
RETURN
    CALCULATE(
        MAX( tCalibracao[valor] ),
        tCalibracao[tipo] = "teto",
        tCalibracao[etapa] = _e,
        tCalibracao[metrica] = "p95_metros_data_ref"
    )
```
> Se a coluna `familia` do CSV não contiver exatamente `todas` para a mediana por turno, ajuste o filtro olhando `tCalibracao`.

```dax
Capacidade Etapa Turno (m) =
-- Pessoas x produtividade x minutos x k, limitado ao teto do turno. Cálculo por linha da tCenario.
SUMX(
    tCenario,
    VAR _cod = tCenario[Código]
    VAR _t   = tCenario[Turno]
    VAR _prod =
        CALCULATE(
            MAX( tCalibracao[valor] ),
            tCalibracao[tipo] = "produtividade",
            tCalibracao[etapa] = _cod,
            tCalibracao[familia] = "todas",
            tCalibracao[turno] = _t,
            tCalibracao[metrica] = "mediana_m_pessoa_min"
        )
    VAR _min =
        CALCULATE(
            MAX( tCalibracao[valor] ),
            tCalibracao[tipo] = "turno",
            tCalibracao[metrica] = "minutos",
            tCalibracao[turno] = _t
        )
    VAR _teto =
        CALCULATE(
            MAX( tCalibracao[valor] ),
            tCalibracao[tipo] = "teto",
            tCalibracao[etapa] = _cod,
            tCalibracao[metrica] = "p95_metros_data_ref_turno"
        )
    RETURN
        MIN( tCenario[Pessoas] * _prod * _min * [Fator k], _teto )
)

Capacidade Etapa (m/dia) =
-- Soma dos turnos, limitada ao teto do dia. Respeita o filtro de tEtapaSim.
-- tCenario é filtrada pela etapa via TREATAS (sem relacionamento no modelo).
VAR _soma =
    CALCULATE(
        [Capacidade Etapa Turno (m)],
        TREATAS( VALUES( tEtapaSim[Código] ), tCenario[Código] )
    )
VAR _teto = [Teto Dia (m)]
RETURN
    MIN( _soma, _teto )
```

```dax
Capacidade Cabine (m/dia) =
-- Volume que a cadeia consegue entregar na cabine, sem demanda: o menor entre as etapas (gargalo).
MINX( ALL( tEtapaSim[Etapa] ), [Capacidade Etapa (m/dia)] )

Volume Previsto Cabine (m/dia) =
-- Regime de fluxo contínuo: demanda e capacidade de cada etapa. O estoque do backtest não entra aqui.
MIN( [Demanda (m/dia)], [Capacidade Cabine (m/dia)] )

Gargalo =
-- Etapa de menor capacidade.
VAR _t =
    TOPN(
        1,
        ADDCOLUMNS( ALL( tEtapaSim[Etapa], tEtapaSim[Ordem] ), "@cap", [Capacidade Etapa (m/dia)] ),
        [@cap], ASC,
        tEtapaSim[Ordem], ASC
    )
RETURN
    MAXX( _t, tEtapaSim[Etapa] )

Aderência à Demanda =
DIVIDE( [Volume Previsto Cabine (m/dia)], [Demanda (m/dia)] )

Demanda Atendida? =
IF( [Capacidade Cabine (m/dia)] >= [Demanda (m/dia)], "Atendida", "Não atendida" )

Déficit (m/dia) =
MAX( [Demanda (m/dia)] - [Capacidade Cabine (m/dia)], 0 )
```

### Conta inversa: pessoas necessárias
Distribui a demanda do dia entre os turnos na proporção dos minutos e arredonda para cima (o Python recebe a demanda já por turno; o DAX reparte a do dia pelos minutos; ambos usam o fator k).
```dax
Pessoas Necessárias Etapa Turno =
-- Demanda do dia x (minutos do turno / 1440) / (produtividade x minutos x k), arredondado para cima.
SUMX(
    tCenario,
    VAR _cod = tCenario[Código]
    VAR _t   = tCenario[Turno]
    VAR _prod =
        CALCULATE(
            MAX( tCalibracao[valor] ),
            tCalibracao[tipo] = "produtividade",
            tCalibracao[etapa] = _cod,
            tCalibracao[familia] = "todas",
            tCalibracao[turno] = _t,
            tCalibracao[metrica] = "mediana_m_pessoa_min"
        )
    VAR _min =
        CALCULATE(
            MAX( tCalibracao[valor] ),
            tCalibracao[tipo] = "turno",
            tCalibracao[metrica] = "minutos",
            tCalibracao[turno] = _t
        )
    VAR _dem = [Demanda (m/dia)] * DIVIDE( _min, 1440 )
    RETURN
        IF( _prod > 0 && _min > 0, ROUNDUP( DIVIDE( _dem, _prod * _min * [Fator k] ), 0 ), 0 )
)

Pessoas Necessárias Dia =
CALCULATE(
    [Pessoas Necessárias Etapa Turno],
    TREATAS( VALUES( tEtapaSim[Código] ), tCenario[Código] )
)

Pessoas a Mais (+) ou a Menos (-) =
CALCULATE(
    SUM( tCenario[Pessoas] ),
    TREATAS( VALUES( tEtapaSim[Código] ), tCenario[Código] )
) - [Pessoas Necessárias Dia]
```
Observação: 1440 = 517 + 503 + 420. O arredondamento por turno pode dar um total ligeiramente maior que a conta direta; é o comportamento esperado (pessoa inteira por turno).

## 3. Visuais sugeridos
- Barras por `tEtapaSim[Etapa]` (ordenadas por `Ordem`): `Capacidade Etapa (m/dia)` contra uma linha `Demanda (m/dia)`; destacar o `Gargalo`.
- Cartões: `Volume Previsto Cabine (m/dia)`, `Aderência à Demanda`, `Demanda Atendida?`, `Déficit (m/dia)`.
- Matriz Etapa x `Pessoas Necessárias Dia` ao lado de `Pessoas a Mais (+) ou a Menos (-)`.
- Segmentadores: `p_Demanda`, `p_Fator`. Rótulo fixo: "Calibração provisória (headcount = quem apontou)".

## 4. Limites do simulador no BI
- Produtividade (m/pessoa·min) não é a Meta HH do K15 (velocidade × minutos): não exibir junto nem chamar de meta.
- O k do `p_Fator` foi escolhido sobre parâmetros de treino; o CSV é calibrado com todos os dias. Atualizar o k a cada recalibração.
- É estático por dia: não carrega estoque entre etapas nem atraso (o backtest tem estoque, o regime contínuo do DAX não). Por isso a `Capacidade Cabine` é o menor valor entre as etapas.
- O teto é empírico (p95), não a capacidade física da máquina. A velocidade por mangueira (`DM_Velocidade`) e o número de trançadeiras não foram usados por falta de export local.
- Mix de bitola não entrou: piorou o backtest.

## 5. Backtest no BI (quando houver o modelo)
Pendente do export/TMDL do William: medida `Real Cabine (m)` sobre `fEtapaOP` filtrando `dEtapa[Etapa] = "Extração/Teste"` (ou o nome real) por `Data de Referência`, e a comparação com a capacidade do dia para mostrar a aderência real x simulada. Os nomes reais de tabela e coluna precisam ser confirmados.
