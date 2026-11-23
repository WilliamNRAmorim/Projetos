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
**Aprovado em 23/11/2026, 14:42.** Conexão Power BI Connected no DPS - Non Prod, fluxo ativado sem bloqueio de DLP e 3 consultas com status 200 em cerca de 1 s.

| Consulta | Resultado | Esperado |
|---|---|---|
| SAP 13/11 | Mangueira 7.915,86 · Montagem 2.220 · Fittings 265 | igual |
| Aderência por trançadeira, 13/11 | TH01 94,3% · TH06 89,3% · Spiral 85,0% · TH02 65,0% · TO04 51,9% · TH07 50,4% · TH03 49,2% · TM01 43,2% · TM04 0% | não havia |
| OEE2 de 09 a 13/11 | OEE2 55,5% · TCU 27,9% (só dias úteis; a referência de 19,8% é de 04/09 a 06/11) | não havia |

- Pela hora cheia do BI, o Real de 13/11 soma 8.450 m; a Hora-Hora soma 8.566 m. É o aviso da especificação: por dia os dois não batem. A soma de 116 m de diferença não foi conciliada linha a linha.
- **Técnica:** `operationId` ExecuteDatasetQuery; o texto da consulta vai em `specification/query`. Resposta em `body/firstTableRows`.
- **Criado no ambiente:** conexão Power BI, referência de conexão `cra6eb_teste_uiu_powerbi` e fluxo "TESTE Uiu portão Power BI (temporário)" (`a25ae3fd-64e7-f111-84e9-7ced8dc5f589`), **desligado**. Apagar o fluxo e a referência pede o "sim" do William; a conexão fica para a ferramenta.
