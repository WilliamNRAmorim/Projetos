# Passo 2: portão do Power BI (23/11/2026)

Modelo `(GMS)`: workspace `629ca442-8019-47e0-83e4-0d48b2d30974`, dataset `b48699da-af0b-4f0e-9b2e-f89cc657dbc1`. Ambiente do Uiu: DPS - Non Prod.

## Ordem
1. William cria a conexão (Power Automate, ambiente DPS - Non Prod, conector **Power BI**, botão +).
2. Conferir se a conexão ficou Connected e se a política de DLP deixa usá-la.
3. Rodar as consultas abaixo pela ação "Run a query against a dataset".
4. Passou = a ferramenta "Perguntar ao BI" segue. Falhou = lista `GMS_SAP_Dia`.

## Consultas de teste

```dax
EVALUATE
ROW (
    "Mangueira", CALCULATE ( SUM ( fProducaoSAP[Quantidade] ), fProducaoSAP[Data] = DATE ( 2026, 11, 13 ), fProducaoSAP[Produto] = "Mangueira" ),
    "Montagem", CALCULATE ( SUM ( fProducaoSAP[Quantidade] ), fProducaoSAP[Data] = DATE ( 2026, 11, 13 ), fProducaoSAP[Produto] = "Montagem" ),
    "Fittings", CALCULATE ( SUM ( fProducaoSAP[Quantidade] ), fProducaoSAP[Data] = DATE ( 2026, 11, 13 ), fProducaoSAP[Produto] = "Fittings" )
)
```

Esperado (validado em 16/11): 7.915,86 · 2.220 · 265. Se a MB51 mudou depois, registrar o valor novo.

```dax
DEFINE
    MEASURE Medidas[_Uiu Aderencia] =
        DIVIDE ( SUM ( fHoraCheia[Real] ), SUM ( fHoraCheia[Meta] ) * 1295 / 1440 )
EVALUATE
CALCULATETABLE (
    ADDCOLUMNS ( VALUES ( fHoraCheia[Célula] ), "Aderencia", [_Uiu Aderencia] ),
    fHoraCheia[Data BI] = DATE ( 2026, 11, 13 )
)
```

## Achado
`HH Aderência`, `HH Meta Útil (m)`, `HH Real (m)`, `HH Parado (min)` e `VG Cabine (m)` são medidas **do relatório** (`GMS_Painel.Report/definition/reportExtensions.json`), não do modelo. A consulta DAX não as enxerga. A ferramenta leva essas fórmulas dentro da consulta (`DEFINE MEASURE`, como acima), copiadas do arquivo do relatório. Se o relatório mudar, a cópia precisa mudar junto.

## Resultado
Pendente: conexão do William.
