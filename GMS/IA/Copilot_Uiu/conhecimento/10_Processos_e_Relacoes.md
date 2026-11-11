# 10 · Processos do GMS e as relações entre eles

Fonte: GMS/CLAUDE.md, GMS_Mestre_BI.md (K01 a K20), linhas NORMA e DECISÃO do GMS_Diario.md até 09/11/2026, 09_Mapa_Listas.md, Analises/OEE2_HoraHora/PLANO_OEE2.md e Simulador_Celula/LEIAME.md. Escrito em 10/11/2026 para o Uiu. A NORMA mais nova do Diário (08_Normas_Diario.md) vence este arquivo. Onde o texto diz "hipótese", não é regra.

## 1. A célula em uma página

- Fluxo da mangueira: Mandril → Tubo → Trançagem → Cobertura → Bandagem → Vulcanização → Debandagem → Extração/Teste. Apoio: Extrusora de mandril, Bobinadeira (fio) e Catenária. Depois da célula vem a Montagem (conjuntos, por OT).
- Uma OP (ordem do SAP) vira uma ficha na ficha_producao e anda de etapa em etapa. Cada etapa grava na ficha início, fim, metros, operador e turno, e grava um evento em Eventos_Producao.
- A OP liga tudo: OP da ficha = OP_ID da inspeção e do refugo = Title do Plano_OPs = OP da Conferencia_SAP. O ID da ficha liga os eventos (origem_ID), os pallets (FichaID) e as bobinas de fio (FichaID_Consumo).
- Uma OP pode ter mais de uma ficha: o Tubo divide a ficha quando sobra tubo e nasce uma ficha filha "(devolvida)". A identidade da ficha é o ID, não a OP. Em soma por OP, confira quantas fichas a OP tem.
- O comprimento muda ao longo do fluxo (exemplo: 800 m na trançagem e 1.050 m na debandagem). Metros de etapas diferentes não se comparam um a um, e a debandagem não é teto da extração.
- Lote padrão por bitola: 3, 4 e 5 → 800 m; 6, 7 e 8 → 680 m; 10 → 460 m; 12 → 400 m; 16 → 250 m. Valores 111, 1111 e 11111 na ficha são preenchimento, não metragem.
- Trançadeiras: o cadastro do app tem 11 (é o número que o TCU usa). Na Hora-Hora de setembro a novembro de 2026 aparecem 10: TH01, TH02, TH03, TH05, TH06, TH07, TM01, TM04, TO04 e Spiral (no delineamento a Spiral é TE01).
- Produção da célula conta uma vez por OP, na etapa final. Somar as 8 etapas conta a mesma mangueira 8 vezes.

## 2. As etapas, uma a uma

Para cada etapa: o que faz, que engenharia manda, que dado mede. Colunas internas completas em 09_Mapa_Listas.md.

- **Extrusora de mandril (apoio).** Produz o mandril, o núcleo sobre o qual a mangueira é construída. Engenharia: DM_MANDREL (por PN do mandril, não da mangueira). Dado: ControleExtrusora_estrutura (produção), RefugoExtrusora_estrutura (refugo), CarreteisMandril e lista_carreteis (carretéis).
- **Mandril.** Prepara e solda o mandril da OP no carretel. Ficha: metros em field_6, início em data_hora_inicio_mandril, fim em field_9, lote_mandril, Desmoldante, código e diâmetro do mandril (field_4, field_5). Qtd_Turno1/2/3 da ficha mãe é o gabarito do Mandril.
- **Tubo.** Extrusão do tubo interno sobre o mandril. Engenharia: DM_TUBE_EXTRUSION. Ficha: metros em field_14, defeito em field_15, início e fim em field_16 e field_17, composto (Cod_x002e_CompostoTubo), lote do composto (LoteCompostoTubo) e validade (DatadeValidadedoComposto), diâmetro em field_13.
- **Trançagem.** Aplica o reforço de arame (1, 2 ou 3 tranças). Engenharia: DM_TRANÇAGEM (construção), DM_ENGRENAGENS (velocidade teórica em m/h por máquina e construção), DESVIO (desvio temporário aprovado), DM_FIOS. Ficha: metros em field_22, defeito em field_23, código e lote do fio, número de picks, 1ª trama. Hora a hora: lista Hora-Hora. Qualidade em processo: AMDM02 (diâmetro e picks, piloto) e Controle_Catenaria (fios). Material: FifoBobinadeira (fila de bobinas) e Refugo_Bobinadeira.
- **Cobertura.** Extrusão da cobertura sobre a trança. Engenharia: DM_EXTRUSAO_COBERTURA (SPEEDY_mpm em m/min; o app multiplica por 60). Ficha: metros em field_28, defeito em field_29, início e fim em field_25 e field_26, composto, lote e validade da cobertura, diâmetro em field_27. De 11/10 a 09/11/2026 a Cobertura não aparece na lista Hora-Hora.
- **Bandagem.** Aplica a fita e a marcação (layline em alto-relevo e inkjet). Engenharia: DM_BANDAGEM e DM_LAYLINE. Ficha: metros em field_33, início e fim em field_31 e field_32, código da fita e do filme.
- **Vulcanização.** Cura em autoclave, por batelada. Ficha: metros em field_37, início e fim em field_35 e field_36, InicioResfriamento_Vulcanizacao, pós-cura (PostCure). O fluxo GMS_AutoResfriamentoVulca marca o resfriamento aos 110 min. O Fim só é gravado depois da cura.
- **Debandagem.** Retira a fita. Engenharia: DM_LAYLINE (TensaodeDebandagem). Ficha: metros em field_41, início e fim em field_39 e field_40.
- **Extração/Teste.** Retira o mandril, testa, inspeciona e separa os lances. Engenharia: DM_TESTE_INSP. Ficha: field_46 é a produção boa do GMS. RegistrosInspeção guarda cada inspeção boa (metros, diâmetro interno e externo, concentricidade, cabine). TiposErros guarda o refugo. Packing_Pallets guarda os pallets da cabine.
- **Montagem.** Monta conjuntos por OT. Producao_Montagem (uma linha por OT, com a MetaHora gravada) e Paradas_Montagem.

Qual dado conta produção por turno no Painel da Célula: Trançagem pela Hora-Hora (MEL-263); Vulcanização pela soma dos eventos Início, porque o Fim só vem depois da cura (MEL-247); as demais etapas por Fim e Parcial. OP cancelada não conta produção e os Parciais dela ficam com 0 m (MEL-260).

## 3. Onde o defeito nasce e onde aparece

O refugo é registrado onde foi achado, quase sempre na Extração/Teste, com a data do registro (DataHoraRefugo). A etapa que gerou pode ter rodado dias antes. Toda análise de refugo guarda as duas datas: a do refugo e a da etapa suspeita na ficha.

A tabela abaixo é **hipótese de partida, escrita em 10/11/2026 e não validada pela qualidade**. Serve para escolher o que conferir primeiro, nunca para afirmar causa.

| Código | Defeito | Etapa a investigar primeiro | O que cruzar |
|---|---|---|---|
| A | Quebra de fio | Trançagem | motivo "Quebra de fio" na Hora-Hora da mesma máquina, lote do fio, Refugo_Bobinadeira |
| B | Set up / alimentação de fio | Trançagem e Bobinadeira | trocas de mangueira no dia, FifoBobinadeira |
| C | Caroço / ondulação | Tubo ou Cobertura | lote do composto, operador e turno da etapa |
| D | Marcação errada | Bandagem | DM_LAYLINE da mangueira, operador da bandagem |
| E | Trança aparente | Cobertura | diâmetro da cobertura (field_27), lote do composto |
| F | Bolhas | Cobertura ou Vulcanização | lote e validade do composto, batelada da autoclave |
| G | Falha na bandagem | Bandagem | código da fita, operador |
| H | Eject test | Extração/Teste | cabine, desmoldante do mandril |
| I, J | Diâmetro externo maior / menor | Cobertura | field_27, DM_EXTRUSAO_COBERTURA |
| K, L | Diâmetro interno maior / menor | Tubo e Mandril | field_13, field_5, DM_TUBE_EXTRUSION |
| M | Excentricidade | Tubo ou Cobertura | concentricidade na inspeção |
| N | Torção na autoclave | Vulcanização | batelada, carretel |
| O | Pontas | Extração/Teste | lances do pallet |
| P | Não identificado | sem hipótese | pedir reclassificação |

Como confirmar uma hipótese: o mesmo código se concentra numa máquina, num lote de material, num operador ou num turno da etapa suspeita? Se o refugo se espalha por tudo, a etapa suspeita está errada ou a causa é do produto.

A coluna Tran_x00e7_adeira da TiposErros é a trançadeira de origem da OP. Ranking de refugo por trançadeira mostra onde a OP foi trançada, não prova que a trança causou o defeito.

## 4. Turno e dia produtivo

- Norma vigente (NORMA de 27/10/2026, MEL-250): 1º turno de 05:20 a 13:56 (517 min); 2º turno de 13:57 a 22:19 (503 min); 3º turno de 22:20 a 05:19 do dia seguinte (420 min). Soma: 1.440 min.
- A hora extra do 2º turno pode ir até 23:20. Ela não muda a fronteira do 3º turno.
- O dia produtivo começa às 05:20. Apontamento antes das 05:20 pertence ao dia anterior. O 3º turno inteiro fica com a data do dia em que começou. Exemplo: 23:50 de segunda e 04:30 de terça são 3º turno de segunda.
- A mesma fronteira vale no app (fx_Turno, fx_InicioTurnoMin, fx_GradeHoraHora) e no dTurno do BI. O BI não calcula turno: lê o carimbo gravado.
- Janelas da Hora-Hora por máquina e dia: 9 no 1º turno, 9 no 2º e 8 no 3º, 26 no total. As janelas das pontas não são hora cheia (40, 57, 63, 20, 40 e 20 min). A meta é sempre pelos minutos da janela.
- Histórico: de 05/10/2026 até a publicação da v3.0.15 (entre 27 e 29/10/2026, data a confirmar com o William) o app virava o 3º turno às 22:41. O que foi apontado entre 22:20 e 22:40 nesse período está gravado como 2º turno (146 linhas de Hora-Hora e 46 fins de etapa, contagem de 29/10). Antes de 05/10 parte do app virava o 2º turno às 13:47 ou 13:48. Ao comparar turnos desses períodos, avise que a fronteira mudou e não corrija o dado por conta própria.
- A tela Hora-Hora da Montagem não troca de turno sozinha.

## 5. Parada, pausa, tempo excedido e o Tempo Parado da Hora-Hora

- São três coisas diferentes e nunca se somam: nem no painel, nem no andon, nem numa "perda total" (MEL-247):
  - **Parada real:** a célula está incapaz de produzir.
  - **Pausa programada:** motivo do tipo "Programada" (Refeição, Reunião, Set-up, Manut. Preventiva, Check List, Amostra, MPT, TESTE ENGENHARIA). É pausa, não parada (DECISÃO de 22/10/2026, MEL-247).
  - **Tempo excedido:** a célula está produzindo, mas gastou mais tempo que o padrão. Texto da norma no GMS/CLAUDE.md: "produzindo acima da meta". Na Montagem é o motivo TE.
- O **Tempo Parado da Hora-Hora** (field_11) nas etapas de mangueira é automático e não editável (DECISÃO de 27/10/2026, publicada em 29/10, MEL-255). O sistema calcula pelo que faltou para a meta: Real 0 = janela inteira; senão proporcional ao que faltou. É tempo equivalente perdido, não cronômetro de máquina parada. Parada, microparada e ritmo baixo chegam misturados; quem separa é o Motivo (field_12).
- Na Cobertura o mesmo campo se chama OCIOSO: minutos da janela sem carretel rodando.
- Motivo "Divergência do Tempo Padrão": limiar de 7 min por janela de 60 min (11,7% da meta), com Real maior que zero e o déficit se repetindo em pelo menos 2 outras janelas do mesmo turno (±1,5 min) (DECISÃO de 06/11/2026, MEL-264). Abaixo da meta sem motivo continua "Motivo Não Declarado".
- OP aguardando etapa é fila (WIP), não parada de máquina. Diga "na etapa X desde", nunca "parada desde".
- Montagem: parada real = Paradas_Montagem sem TE (tempo excedido) e sem RF (refeição), o mesmo critério do BI (MEL-246).
- MTBF e MTTR só fazem sentido com motivo do tipo falha. Sem separar falha de pausa programada, o número existe e não quer dizer nada (K17).
- O OEE2 (seção 8) não é exceção a essa regra (decisão do William em 10/11/2026). No OEE2 cada minuto de perda fica em uma família só (amarela ou vermelha), no padrão Danfoss (MEL-266). Mostre as famílias separadas e nunca apresente a soma delas como "tempo parado" nem como "perda total".

## 6. Setup

- Definição da norma (GMS/CLAUDE.md): setup é o intervalo entre a última peça boa de uma OAP e a primeira peça boa da próxima. Nunca se mede por cliques do operador.
- Na Hora-Hora, "Set-up" é um motivo do tipo Programada: no painel conta como pausa, não como parada (MEL-247).
- No OEE2 (seção 8) o Set-up é da família amarela, troca de lote, e entra como perda de Disponibilidade.
- As duas coisas valem ao mesmo tempo, cada uma no seu indicador. Ao responder, diga de qual indicador está falando.
- Cuidado com a cor: no Painel da Célula o motivo programado vira "PAUSA cinza" (MEL-247). O cinza do painel não é o cinza do OEE2: no OEE2, cinza é atividade não produtiva, e Set-up e Check List são amarelos.
- O amarelo do OEE2 é o "Set-up declarado no Hora-Hora". O KPI de setup continua sendo o da definição acima.
- Os minutos com motivo Set-up na Hora-Hora são déficit contra a meta com esse motivo (seção 5). Não são o setup da definição, que pede a hora das peças boas.
- O simulador da célula usa uma aproximação de setup por troca de mangueira entre turnos. É regra do simulador, não a norma (12_Diagnostico_e_Simulador.md).

## 7. Velocidade teórica, Meta Hora e aderência

- Velocidade teórica da trançagem: tabela DM_ENGRENAGENS, coluna _13TEORICA_M_H, em m/h, por máquina e construção. Com desvio ativo na tabela DESVIO, a velocidade oficial é a do desvio (MEL-256).
- Meta Hora (field_5) = velocidade × minutos da janela ÷ 60. Real (field_7) = metros apontados na janela. Aderência = Real ÷ Meta. Não use a coluna Rendimento: ela mistura 3 escalas.
- Velocidade real da janela = Real ÷ (minutos da janela ÷ 60). Diferença para a teórica, sem motivo de parada, é ritmo.
- No BI (decisões vigentes): Meta Hora BI = meta cheia × Minutos BI ÷ Minutos. As barras por hora usam a meta cheia. O cartão Meta (HH Meta Útil) e a HH Aderência usam o fator de dia útil 1305 ÷ 1440 (21h45: pausa de 45 min em cada um dos 3 turnos), só quando não há hora filtrada. Vale desde 09/11/2026 (MEL-266); antes era 1295 ÷ 1440. O painel publicado só muda quando o William publicar.
- Tempo útil por turno com a pausa de 45 min: 472, 458 e 375 min, 1.305 no dia.
- O fator de dia útil nunca entra no OEE2: descontaria a pausa duas vezes.
- Mangueira de duas passadas (construção DD, double deck; observação "DUAS PASS" na DM_ENGRENAGENS): o operador digita o total e o app grava Real ÷ 2 (MEL-241). Meta de TH01 e TO04: o William decidiu em 10/11/2026 dividir a meta por 2, desde que a divisão por 2 bata com o valor. A conferência com o dado está pendente e nada mudou no app nem no BI. Até lá, aderência de duas passadas nessas duas máquinas leva ressalva.
- Cobertura: velocidade da DM_EXTRUSAO_COBERTURA. Montagem: meta pela MetaHora gravada na própria OT (MEL-246).
- Há duas fontes de velocidade: a lista DM_Velocidade (usada pelo fluxo Monitor Solda Mandril) e a DM_ENGRENAGENS com desvio (usada pela Hora-Hora e pelo painel). A da meta é a DM_ENGRENAGENS com desvio. Se as duas divergirem, é achado a relatar.
- O Uiu não lê as tabelas DM (são Excel). Ele lê a Meta Hora já gravada. Para saber a velocidade cadastrada, peça ao William ou deduza pela meta: velocidade = Meta Hora × 60 ÷ minutos da janela, e diga que é dedução.

## 8. OEE2 e TCU

Padrão Danfoss adotado para a Hora-Hora de mangueira (MEL-266, 09/11/2026). Fonte: Analises/OEE2_HoraHora/PLANO_OEE2.md. A Montagem está fora.

- Quatro famílias de parada:
  - Azul, sem atividade: fim de semana, feriado, sem produção planejada.
  - Cinza, atividade não produtiva: manutenção planejada, validação (teste), pessoal (pausa, reunião, treinamento).
  - Amarela, troca de lote: preparação, troca de ferramenta, checagem de qualidade, partida, reabastecimento, limpeza.
  - Vermelha, perda durante a operação: defeito de máquina, defeito de processo (OP faltando, material faltando, quebra de material), espera, utilidades.
- OEE2 = tempo valorizado ÷ tempo de produção. Tempo de produção = tempo de equipamento menos azul e cinza.
- Disponibilidade = perdas amarelas. Performance = perdas vermelhas, e aqui a quebra de máquina fica em Performance (diferente do OEE clássico). Qualidade = refugo e retrabalho.
- TCU = tempo valorizado ÷ tempo total do equipamento, 24 horas por 7 dias. Azul e cinza entram. O TCU conta as 11 máquinas.
- Pausa de refeição planejada: 45 min fixos em cada um dos 3 turnos, 135 min por dia e por máquina.
- A fonte é o GMS, sem Factbird (que só cobre a TH07). Por isso o OEE2 é estimativa de apontamento, não de sensor: a separação entre disponibilidade e performance vem só da classificação do motivo.
- Referência de 01/09 a 06/11/2026 na Trançagem, em duas contas:
  - Antes da pausa fixa (é a referência que o cartão mostra, OEE2 ≈ 54% e TCU ≈ 19%): OEE2 perto de 54% sem qualidade e 52,9% com qualidade; Disponibilidade 84,0%, Performance 64,0%, Qualidade perto de 98,5%.
  - Com a pausa fixa de 45 min por turno, que é a regra vigente: OEE2 ≈ 55,1% sem qualidade e ≈ 54,3% com qualidade; Disponibilidade 83,5%, Performance 66,0%. A pausa fixa não muda o TCU.
  - Por máquina, na conta anterior à pausa fixa: TH06 67%, TM01 63%, TO04 63%, TH01 60%, TH02 60%, TH07 58%, TH05 54%, TH03 41%, TM04 36%, Spiral 18%.
  - O cartão OEE2 não tem meta fixa. Ao citar um desses números, diga de qual conta ele é.
- A refeição só é declarada em 59% dos turnos de máquina com produção. No resto ela cai em Motivo Não Declarado ou em motivo vermelho e piora a Performance.
- A conciliação Hora-Hora x ficha foi adiada pelo William: os metros fecham no total (razão 1,02), mas só 54% das OPs ficam em ±20%.
- O OEE2 não é exceção à regra de que parada, pausa e tempo excedido nunca se somam (decisão do William em 10/11/2026): as perdas aparecem por família, em linhas separadas.
- O "OEE-lite" (K18 do Mestre_BI: Disponibilidade × Performance × Qualidade com outra definição) é outra fórmula. Não misture os dois.

## 9. Refugo, % de refugo, PPM e GMS x SAP

- Refugo do GMS na linha: lista TiposErros, em metros, com código de erro (A a P), OP e trançadeira de origem. Há também refugo de fio (Refugo_Bobinadeira) e de mandril (RefugoExtrusora_estrutura). São naturezas e unidades diferentes: não some as três sem conferir a unidade. O K10 do BI consolida as três.
- A TiposErros tem grupos repetidos por OP + erro + quantidade + data (84 grupos, 92 linhas a mais na foto de outubro). Repetição não prova duplicata: sinalize, não exclua.
- % de refugo = refugo ÷ (bom + refugo), com numerador e denominador do mesmo recorte de etapa (K11). Refugo da trançagem sobre produção de todas as etapas dá número bonito e falso.
- PPM = metros errados ÷ metros de produção boa × 1.000.000. A base de produção é o SAP. É de uso interno. Material de produção pequena infla o PPM.
- Produção boa no GMS = inspeção (field_46 da ficha, RegistrosInspeção). Produção boa no SAP = movimento 101 menos 102, sem os lançamentos dos usuários de refugo.
- GMS x SAP: o SAP é a verdade. Variação = SAP menos GMS; negativa = faltou lançar no SAP; positiva = sobrou no SAP. Faltou e sobrou se somam separados, por material. Material não compensa material.
- Lance lançado em outra OP do mesmo material é costume: falta numa OP e sobra igual na vizinha.
- Nome de mangueira do GMS não é o do SAP. Ligue pela OP. Nunca descarte uma mangueira por não achar o nome.
- Referência de refugo do GMS de abril a agosto de 2026: 0,79% (5.034 m em 634.516 m). É número do GMS, não do SAP.
- Detalhe e pegadinhas: 07_Dados_SAP_x_GMS.md.

## 10. Cadeias de causa e efeito entre as áreas

Cada linha: causa → efeito → onde ver. São relações para investigar; a prova é o dado do caso.

1. Tubo atrasado ou sem mandril → trançadeira sem material → janela com Real baixo e motivo de falta de material (vermelha, Performance) → Hora-Hora (field_12) e fila na ficha (colunas InicioAguardando).
2. Bobina de fio fora de ordem ou em falta → parada por alimentação de fio na trançadeira → FifoBobinadeira e Refugo_Bobinadeira.
3. Troca de mangueira no plano → set-up → menos tempo valorizado. O mix do dia também muda a meta: máquina que roda construção lenta produz menos metros com a mesma aderência. Queda de metros sem queda de aderência é mix, não desempenho.
4. Velocidade cadastrada errada na DM_ENGRENAGENS → aderência sempre baixa ou sempre alta numa máquina e construção. A Spiral a 18% de OEE2 sugere velocidade validada errada: é assunto de engenharia, não de operação.
5. Quebra de fio → aparece duas vezes: como motivo na Hora-Hora (produção) e como código A na TiposErros (qualidade). A mesma causa, em duas listas e em datas diferentes.
6. Lote ou validade do composto → defeito de extrusão (bolha, caroço, diâmetro) → ligue a TiposErros à ficha pela OP e agrupe por lote de composto.
7. Diâmetro ou picks fora na trançagem (AMDM02, Catenária) → risco de refugo dimensional no teste dias depois.
8. Vulcanização em batelada → o Fim é gravado depois da cura. Produção por turno pela data do Fim desloca a etapa; por isso o painel usa o Início.
9. Ficha esquecida aberta (OP zumbi, mais de 72 h na etapa) → WIP inflado → gargalo fantasma. Todo WIP vem com a idade da OP mais velha.
10. Inspeção cadastrada com atraso → produção da Extração cai no dia errado se a conta usar Created em vez de DataHoraInspecao.
11. Lance lançado em outra OP → divergência GMS x SAP que se anula dentro do material.
12. Refeição não declarada → vira Motivo Não Declarado → Performance pior que a real.
13. Turno gravado com fronteira antiga (até 29/10/2026) → comparação entre 2º e 3º turno distorcida.
14. Plano_OPs desatualizado (o fluxo de sincronismo depende da pasta e do mês) → OP não aparece para o operador → pedido em Excecoes_OP.

## 11. Rastreabilidade: da OP ao lote

Para responder "o que aconteceu com esta OP" ou "o que esta mangueira tem em comum com as outras que falharam", siga a OP:

1. ficha_producao pela OP: etapa atual, metros, início e fim, operador e turno de cada etapa, trançadeira, cabine de teste.
2. Materiais na mesma ficha: lote do mandril e desmoldante, composto e lote do tubo com validade, código e lote do fio, picks, composto e lote da cobertura com validade, fita e filme da bandagem.
3. Eventos_Producao pelo ID da ficha (origem_ID): Início, Fim, Parcial e Cancelado de cada etapa, com data_ref e turno.
4. FifoBobinadeira por FichaID_Consumo: as bobinas de fio consumidas. Historico_Carretel pelo OP_ID: a custódia do carretel por etapa (lista sem índice, só por faixa de ID).
5. RegistrosInspeção pelo OP_ID: metros bons, diâmetros, concentricidade, cabine, data da inspeção.
6. TiposErros pelo OP_ID: refugo por código.
7. Packing_Pallets pelo FichaID: pallets e lances.
8. Plano_OPs e Conferencia_SAP pela OP: plano, situação no SAP e casos de divergência.

Para achar o que várias OPs com o mesmo defeito têm em comum, monte a tabela OP × (máquina, lote de composto, lote de fio, operador, turno, data da etapa suspeita) e procure a coluna que se repete.
