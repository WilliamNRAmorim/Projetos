# Consultar GMS: especificação dos indicadores (23/11/2026)

Passo 1 do `PLANO_PATCH_GERAL_2026-11-23.md`. Nada construído. Versão 2, corrigida depois da revisão das regras (seção 9).

## 1. Regra de ouro: cada indicador tem um dono

| Dono | Responde |
|---|---|
| **Consultar GMS** (listas SharePoint, agora) | fato apontado: inspeção, refugo, evento de etapa, real da Hora-Hora, Montagem, OP em processo |
| **Perguntar ao BI** (modelo `(GMS)`) | o que tem regra de cálculo: meta, aderência, parada oficial, OEE2, TCU, PPM, SAP, plano, ritmo |

Pergunta de meta, aderência ou tempo parado com o BI fora do ar: devolver o fato gravado com o aviso "não é o número do painel". Nunca refazer a regra do BI no fluxo.

## 2. Entradas

`indicador` (seção 4) · `de`, `ate` (DD/MM/AAAA, inclusive) · `corte` (`civil` ou `produtivo`) · `agrupar` (0 a 2 dimensões) · `onde` (dimensão=valor, opcional).

Erro claro, sem adivinhar: indicador inexistente, data inválida, `de` maior que `ate`, dimensão que o indicador não tem.

## 3. Tipos de data (medido nas listas em 23/11)

| Tipo | Colunas | Filtro do dia D | Corte |
|---|---|---|---|
| **Só data, dia produtivo** | Eventos_Producao.data_ref e Hora-Hora.field_0 (400 de 400 linhas às 03:00Z) | D 00:00Z a D+1 00:00Z | só produtivo |
| **Só data, dia do registro** | TiposErros.DataHoraRefugo (399 de 400; a tela grava a hora, a coluna guarda só o dia) | D 00:00Z a D+1 00:00Z | só civil; pedido produtivo responde em civil e avisa |
| **Só data** | Producao_Montagem.field_1 e Paradas_Montagem.field_1 | D 00:00Z a D+1 00:00Z | o gravado pela tela |
| **Instante UTC** | RegistrosInspeção.DataHoraInspecao, Refugo_Bobinadeira.field_2, RefugoExtrusora_estrutura.field_7, Controle_Catenaria.DataHora | civil: D 03:00Z a D+1 03:00Z; produtivo: D 08:20Z a D+1 08:20Z | os dois; turno no agrupamento **força o produtivo** (o dia civil parte o 3º turno) e avisa |

Brasília = UTC−3, fixo. Sem dizer o corte: **produtivo** quando a coluna permite. Se ele disser "00h a 23h59" ou "dia civil": **civil**. O agrupamento por dia usa o mesmo corte. A resposta sempre escreve o período em Brasília.

## 4. Indicadores

| Indicador | Fonte e conta | Dimensões | Avisos |
|---|---|---|---|
| `inspecao_boa` (m) | RegistrosInspeção, soma Quantidade. É a "Metragem na cabine" do painel (DECISÃO de 16/11, MEL-273) | dia, turno **pela hora da inspeção** (1º 08:20Z, 2º 16:57Z, 3º 01:20Z), mangueira, trançadeira, cabine, OP | lance lançado depois muda dia já respondido |
| `refugo` (m) | TiposErros, soma OData__x0043_ | dia, código (A a P), trançadeira, cabine, OP, turno gravado | separa as linhas com mais de 60 dias entre a data e o Created (dia e mês trocados) e avisa que saem do mês errado, mas não voltam ao certo; troca próxima (09/10 por 10/09) passa; com turno, avisa que o dia civil mistura dois 3ºs turnos; repetidos são sinalizados, nunca excluídos |
| `perc_refugo` | refugo (sem as linhas trocadas) ÷ (inspecao_boa + refugo), as duas no corte civil e no mesmo período | trançadeira, cabine, OP | é da cabine por dia de registro; não é o "% Refugo Cabine" do BI, que usa a ficha |
| `producao_etapa` (m) | Eventos_Producao, `origem eq 'ficha_producao'`, tipo Fim ou Parcial. **Vulcanização = Início** (MEL-247). **Trançagem = Hora-Hora** (MEL-263), como `trancagem_real`. **Extração = `inspecao_boa` produtivo** (DECISÃO de 16/11, MEL-273). **Cancelada (MEL-260):** desconta Fim, Parcial e Início da Vulcanização só da mesma ficha **e mesma etapa**, com ID menor que o do evento Cancelado, buscado sem limite de período | dia, turno, etapa | etapas nunca se somam: sem etapa, uma linha por etapa e nenhum total; ficha com field_11 Cancelado e sem evento vira aviso **com a ficha e os metros**, que seguem somados até correção; na Trançagem a Hora-Hora não tem ficha: cancelamento lá não é descontável, e o aviso diz isso |
| `trancagem_real` (m) | Hora-Hora field_7, só células da `fx_CelulasTrancagem` e **a última linha (maior ID) de cada janela** (data, célula, turno e janela), como o painel | dia, turno, célula, mangueira | duas passadas: metade gravada (MEL-241); o BI usa hora cheia (05:00), por dia não bate |
| `trancagem_meta_gravada` (m) | Hora-Hora field_5, mesma regra da última linha | dia, turno, célula | **não é a meta do painel** (refeição, Preventiva, Reunião, Amostra e 21h35 só existem no BI) |
| `deficit_hora_hora` (min) | Hora-Hora field_11, última linha da janela, **só trançadeiras** (na Cobertura o campo é OCIOSO, outra conta). Antes de classificar: tirar prefixo numérico ("21 - "), Refeição = Almoço, Problema no tubo = Análise/Problema no tubo. **Três blocos sem total geral:** Tipo Programada do `dMotivoParada`; Divergência do Tempo Padrão; demais. Motivo vazio ou fora do cadastro fica em linha própria | dia, turno, célula, motivo | déficit contra a meta, não cronômetro; parada oficial = BI |
| `montagem_pecas` | Producao_Montagem field_9 | dia, turno, célula, status | limpar espaço e caixa de célula e turno antes de agrupar |
| `montagem_paradas` (min) | Paradas_Montagem field_6 em três blocos: parada real (sem TE e sem RF), TE, RF. **Nunca somados** (MEL-246). TE = exatamente `fx_MotivoTempoExcedido`; AU, CA, LI e TU ficam em parada real, como no BI | dia, turno, célula, motivo | o desconto da OT com RF (MEL-267) é do BI |
| `refugo_fio` | Refugo_Bobinadeira field_6 | dia, máquina, motivo | unidade a confirmar; não soma com metros |
| `refugo_mandril` (kg) | RefugoExtrusora_estrutura field_5 | dia, código | kg; nunca percentual sobre metros (MEL-244) |
| `ops_em_processo` | ficha_producao com field_11 = Em processo, por etapa (field_10) | etapa, trançadeira, mangueira | foto de agora; diga "na etapa desde", nunca "parada" |
| `op` | uma OP: ficha, inspeção, refugo e eventos | — | a identidade da ficha é o ID; a OP pode ter mais de uma |

Turno gravado entre 05/10 e 29/10/2026 pode ter a fronteira antiga (22:41): o fluxo devolve esse aviso quando o período toca essas datas e há turno no agrupamento.

## 5. Saída

`valor`, `unidade`, `linhas`, `grupos`, `periodo_brasilia`, `corte`, `fonte`, `completo` (true ou false), `avisos[]`, `consultado_em`. Sem linhas: "0 registros", nunca "0 m produzidos".

## 6. Comportamento (vai às instruções v4)

1. "Tem certeza?" = nova chamada com a mesma entrada, mostrando a conta; se mudou, dizer que o dado mudou.
2. Dado colado: identificar a fonte pelas colunas antes de somar. Descrição de material ("HOSE-AER, GH781…") com data = SAP.
3. Dois totais diferentes: comparar fonte, data (lançamento ou inspeção) e mangueira a mangueira. **Total parecido não é conciliação.**
4. Nunca afirmar fuso, cobertura ou causa que a ferramenta não devolveu.
5. Sem ferramenta de escrita: não prometer gravação.

## 7. Conhecimento a corrigir junto

- `02_KPIs_do_BI.md` (fator 21h45): vale 21h35 desde 11/11 (MEL-267), com refeição, Preventiva, Reunião e Amostra fora da meta (11/11 e 18/11). `10_Processos_e_Relacoes.md` §7 tem o mesmo atraso.
- `10_Processos_e_Relacoes.md` §9 e a v3.2: a metragem na cabine é RegistrosInspeção desde 16/11.
- `09_Mapa_Listas.md`: DataHoraRefugo é só data.

## 8. Decisões do William

1. Refugo com dia e mês trocados: 44 linhas criadas em março com data de set a dez. Recomendada: a ferramenta separa e avisa já; corrigir a lista depois, com backup e o seu "sim".
2. Unidade do refugo da Bobinadeira.
3. Extração: adotei DataHoraInspecao (decisão de 16/11, a mais nova). O Painel da Célula usa Created (MEL-261); lance lançado com atraso cai em outro dia lá. Alinhar o painel é outra tarefa.
4. Ficha 4526, cancelada no Mandril em 14/11, ainda tem um Parcial de 250 m em 13/11 (o MEL-260 manda 0). A ferramenta desconta; corrigir o item pede o seu "sim".

## 9. Revisão

Revisado em 23/11 em Opus, com as instruções do `revisor` (o agente não carregou na sessão). 1º passe: reprovado. 2º passe: aprovado com ressalvas, já tratadas aqui. Fatos conferidos depois na lista:

- **Cancelada:** 48 eventos Cancelado (43 no Mandril, 5 no Tubo). As fichas 4449 e 4557 foram canceladas no Tubo e depois chegaram à Extração (318,8 e 404,7 m). Descontar a ficha inteira, como manda a v3.2, apaga produção real.
- **Hora-Hora duplicada:** 0 janelas de 09 a 13/11 (831 linhas) e 1 em outubro (4.443 linhas, sem efeito no total). A regra fica pelo histórico.
- **Datas fora de 03:00Z no refugo (44)** são as mesmas 44 linhas trocadas de março.

Testes do fluxo, além do gabarito: turno com corte civil (tem de forçar o produtivo), motivo com prefixo numérico e `perc_refugo` agrupado.
