# Saúde do dado — ficha_producao (export de 06/10/2026 08:19)

2.694 linhas (46 novas desde o export de 05/10; nenhuma sumiu) · 2.647 Finalizado · 29 Aguardando · 14 Em processo · 4 Cancelado.
As 4 colunas novas da Trançagem (`Lote_Tranc_1aTrama`, `Cod_Tranc_1aTrama`, `Picks_Tranc_1aTrama`, `Diam_Tranc_1aTrama`) já existem e estão vazias: começam a encher quando a Trançagem v0.4.1 for colada.

## Conclusão
**O dado novo está saudável; o problema é o histórico anterior a ~15/09.** Nas 214 OPs finalizadas depois de 15/09: zero "Turno N" em texto, zero datas faltando, quantidade vazia em 2 de 1.700 campos, composto/lote da Cobertura 100% preenchido, saltos de metragem >10% em 0 a 13 de ~214 por etapa. As normas do app (metragem obrigatória, fx_Num, diâmetro) funcionam; a sujeira é legado.

## Frentes (da mais valiosa para a menos)
| # | Frente | Tamanho | Onde resolver |
|---|---|---|---|
| 1 | **Diâmetro digitado em milésimo** (valor > 5 pol.): Trançagem 1.482, Cobertura 388, Tubo 60 (todos pré-15/09). Diâmetro ≤ 0 ou vazio: Trançagem 80, Cobertura 151, Tubo 13 | ~1.900 campos | BI (Power Query): se > 5 então ÷ 1000; ≤ 0 vira vazio. Não mexer na lista |
| 2 | **Turno em dois formatos**: "1/2/3" e "Turno 1/2/3" (949 OPs pré-15/09; Vulcanização ainda tem "Turno 1/2" em 826) | 949 OPs | BI: extrair o dígito. App já grava só número |
| 3 | **Duração de etapa > 24 h**: Trançagem 504, Vulcanização 54, Extração 31, Debandagem 17… (24 na Trançagem pós-15/09: OP aberta e esquecida) | ~620 | BI: excluir da média de ciclo; pós-15/09 olhar caso a caso |
| 4 | **Extração fim < início** (110) e **sem datas** (Extração 708, Debandagem 548, Vulcanização 51): todos pré-15/09, antes de a tela gravar as datas | ~1.400 | BI: tratar como "sem tempo medido" |
| 5 | **Quantidade vazia ou 0 em OP finalizada** por etapa (pré-15/09): Trançagem 146, Cobertura 149, Bandagem 224, Vulcanização 209, Debandagem 160, Extração 246 | ~1.100 | Só histórico; não corrigir. O BI não soma metragem dessas etapas sem avisar |
| 6 | **OPs presas ou de teste** (abaixo) | 6 linhas | Cancelar quando o descarte de OP existir nas etapas, ou editar na tela |
| 7 | **Mangueira**: `gh781-6` em minúsculo (1) e 9 linhas sem mangueira (Tubo na fila, normal) | 1 | `fx_MangCanon` no app; Upper/Trim no BI |
| 8 | **Qtd_Turno1/2/3 ≠ quantidade_mandril** em 916 de 2.266 OPs com os dois preenchidos | 916 | Investigar: pode ser OP que atravessa turno (encerramento parcial) e não erro. Definir qual campo o BI usa |
| 9 | Cód. Fita Bandagem vazio em 1.893 | — | Esperado: a fita só vale quando a mangueira leva fita ("-" = não leva) |

## OPs que merecem decisão (não finalizadas)
- **3571** OP 45693212, Trançadeira, Aguardando desde 23/09, mangueira "0"
- **3714** OP 45698721, Trançadeira, Em processo desde 24/09, mangueira "1"
- **3845** OP 75632568, Trançadeira, Em processo desde 30/09, mangueira "0"
- **3861** OP 10010000, Trançadeira, Aguardando desde 01/10, mangueira "0"
- **3864** OP 30407181, Trançadeira, Em processo desde 03/10, mangueira "2583-12" (código estranho)
- **3754** OP 30307302, Cobertura, Aguardando desde 03/10
Os quatro primeiros têm cara de teste (OP fora do padrão 30xxxxxx e mangueira 0/1). Confirmar com a produção antes de cancelar.

## Cancelados (4) — IDs 3839, 3840, 3850, 3892
Todos no Mandril, sem OP, carretéis 33, 33, 72 e 9. Conferir na lista de carretéis que os quatro voltaram para "livre".

## Conferido
- OP com 8 dígitos em 100% das linhas com OP (13 vazias: 4 cancelados do Mandril, Tubo/Mandril ainda na fila). Nenhuma OP repetida.
