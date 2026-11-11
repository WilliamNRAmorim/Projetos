# Gabarito do teste "qual foi meu volume nos processos ontem" (dia produtivo 10/11/2026)

Calculado em 11/11/2026 pela API REST do SharePoint (só leitura), com as regras das instruções v3.1:

- Eventos_Producao: `data_ref ge 2026-11-10T00:00:00Z and lt 2026-11-11T00:00:00Z`. São 218 eventos, sem Parcial nem Cancelado no dia.
- Hora-Hora: `field_0` do mesmo dia. São 163 janelas, em 9 máquinas.

| Etapa | Metros | Regra | Eventos |
|---|---|---|---|
| Mandril | 4.450 | Fim | 14 |
| Tubo | 7.510 | Fim | 16 |
| Trançagem | 7.544 | Hora-Hora `field_7` (os eventos Fim somam 7.210) | 163 janelas |
| Cobertura | 7.970 (42 m de refugo) | Fim | 15 |
| Bandagem | 7.585 | Fim | 14 |
| Vulcanização | 6.575 | Início (MEL-247); o Fim soma 4.905 | 13 |
| Debandagem | 6.155 | Fim | 11 |
| Extração (produção da célula) | 6.720 | Fim | 13 |

## Rodada 1 (11/11, 12:17): Claude Opus 4.8 + v3.1, sem Code interpreter

Ele leu as 218 linhas e respondeu com tabela, mas fez a conta de cabeça e errou:

| Etapa | Resposta do Uiu | Real |
|---|---|---|
| Extração | 12.457 | 6.720 |
| Tubo | 11.700 | 7.510 |
| Trançagem | 13.950, pelos eventos | 7.544, pela Hora-Hora |

Também inventou uma explicação ("OPs termofusão/vibracional"). **Reprovado.** O próximo passo é a rodada 2, com o Code interpreter.

## Erro meu no diagnóstico de 11/11

No primeiro gabarito usei `data_ref` de 08:20Z a 08:20Z. Essa faixa pega o dia 11, porque o `data_ref` é gravado como D às 03:00Z. A faixa certa é 00:00Z a 00:00Z. Na resposta ruim que o Uiu deu no Teams, ele cometeu o mesmo erro.

## Rodada 2 (11/11, 12:37): Opus 4.8 + v3.1 + Code interpreter ligado

Ele usou o Code (Preview) e a conta em Python bate com os números que ele pôs no código. Esses números, porém, já entram abaixo do real: o modelo copia as linhas da ferramenta para dentro do código e perde parte delas.

| Etapa | Uiu | Real |
|---|---|---|
| Tubo | 7.260 | 7.510 |
| Trançagem | 5.210, pelos eventos | 7.544 pela Hora-Hora (os eventos somam 7.210) |
| Cobertura | 6.000 | 7.970 |
| Bandagem | 6.480 | 7.585 |
| Extração | 5.893 | 6.720 |
| Vulcanização | 5.440 | 6.575 |

**Reprovado nos números; aprovado em comportamento** (filtro certo, regra certa, português, não desistiu). Conclusão: com o conector Get items, total não pode depender de o modelo copiar linhas. O total tem de chegar pronto (lista `Uiu_Agregados`, F2/E2 do plano), e o Uiu só lê e explica.
