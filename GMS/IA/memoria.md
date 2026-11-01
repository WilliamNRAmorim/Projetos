# Memoria da IA da manufatura

Aqui fica so o que o William aprovou. A IA le este arquivo antes de cada pergunta e so escreve nele quando voce
digita + ou - . Fato que ela descobre sozinha entra marcado "(a conferir)" ate voce confirmar com `--limpar`.
Pode ler e corrigir a mao. Nao coloque dados de producao aqui.

## Fatos
- PPM = metros errados / metros de producao boa x 1.000.000; a base de producao e o SAP (fonte: COMO_USAR_OS_DADOS 3.5) (a conferir)
- PPM de refugo e para uso interno, nao mostrar a publico externo (fonte: COMO_USAR_OS_DADOS 3.6) (a conferir)
- Material de producao pequena infla o PPM (FC839B-08: 1.900 m e 32 m de erro = 16.904 ppm) (fonte: COMO_USAR_OS_DADOS 3.5) (a conferir)
- SAP e a verdade; variacao = SAP menos GMS; negativa = faltou lancar no SAP, positiva = sobrou no SAP (fonte: COMO_USAR_OS_DADOS 3.1) (a conferir)
- Faltou e sobrou se somam separados, por material; so compensa dentro do mesmo material (fonte: COMO_USAR_OS_DADOS 3.2) (a conferir)
- Refugo no SAP = lancamentos 101 dos usuarios U445131 e U452021; o SAP nao informa o tipo de defeito; estorno e 102 (fonte: COMO_USAR_OS_DADOS 2) (a conferir)
- Producao boa no SAP = 101 menos 102 sem os lancamentos dos usuarios de refugo (fonte: COMO_USAR_OS_DADOS 2) (a conferir)
- Producao boa no GMS = inspecao (quantidade_extracao da ficha); o total do GMS e boa + refugo; refugo do GMS vem da lista TiposErros (fonte: COMO_USAR_OS_DADOS 2) (a conferir)
- Metros de mangueira na MB51 = so unidade M (a MB51 mistura M, PC e KG) (fonte: COMO_USAR_OS_DADOS 4) (a conferir)
- Nome de mangueira do GMS nao e o do SAP: ligue pela OP (a mesma OP nos dois lados) e nunca descarte uma mangueira por nao achar o nome (fonte: COMO_USAR_OS_DADOS 4) (a conferir)
- Data do erro = data do lancamento no SAP; sem lancamento no SAP, a data de criacao no GMS (fonte: COMO_USAR_OS_DADOS 3.4) (a conferir)
- Lance mandado em outra OP e costume: falta numa OP e sobra igual na OP vizinha do mesmo material, e se anulam (fonte: COMO_USAR_OS_DADOS 3.3) (a conferir)
- Os CSVs do SharePoint trazem data MM/DD/AAAA h:mm AM/PM e numero com virgula de milhar na ficha ("1,050") (fonte: COMO_USAR_OS_DADOS 4) (a conferir)
- A ficha_producao tem uma linha por OP; o lote cresce por etapa e a debandagem nao e teto exato (a extracao pode passar dela) (fonte: COMO_USAR_OS_DADOS 4) (a conferir)
- Parada de julho: sem producao de 04 a 26/07/2026 no SAP e no GMS (provavel ferias, a confirmar); mes pequeno distorce o PPM (fonte: COMO_USAR_OS_DADOS 4) (a conferir)
- % Refugo = refugo / (bom + refugo), os dois no mesmo recorte de etapa (fonte: GMS_Mestre_BI K11) (a conferir)
- Metros Produzidos sem filtro de etapa conta a mesma mangueira oito vezes; Metros Equivalentes conta a OP uma vez, na etapa Finalizacao (fonte: GMS_Mestre_BI K01-K02) (a conferir)
- Meta HH = minutos disponiveis da janela x velocidade da mangueira; Aderencia HH = Real HH / Meta HH (fonte: GMS_Mestre_BI K15) (a conferir)
- MTBF so conta falhas, nao parada programada; sem distinguir falha de parada programada o numero nao quer dizer nada (fonte: GMS_Mestre_BI K17) (a conferir)
- Turnos (NORMA 27/10/2026, MEL-250): 1o 05:20 a 13:56 (517 min), 2o 13:57 a 22:19 (503 min), 3o 22:20 a 05:19 do dia seguinte (420 min) (fonte: glossario.md, GMS_Diario NORMA 27/10) (a conferir)
- Dia produtivo (data_ref) comeca as 05:20; apontamento antes das 05:20 pertence ao dia anterior (fonte: glossario.md, GMS_Diario NORMA 27/10) (a conferir)
- Ate 27/10/2026 o fx_Turno virava o 3o turno as 22:41: registros feitos entre 22:20 e 22:40 estao gravados como Turno 2 (de 05/10 a 27/10, na janela "22:00 - 22:20" com 41 min: 146 linhas de Hora-Hora e 46 fins de etapa na ficha). Ao comparar turnos desse periodo, avise que a fronteira mudou; a correcao para Turno 3 foi aprovada pelo William em 31/10 e ainda nao aplicada (fonte: GMS_Diario MEL-198 05/10, PENDENCIA 27/10 e FEITO 29/10 MEL-250) (a conferir)
- Parada real (celula incapaz de produzir) nunca e somada com tempo excedido (produzindo acima da meta) (fonte: glossario.md, GMS/CLAUDE.md) (a conferir)
- Setup = intervalo entre a ultima peca boa de uma OAP e a primeira peca boa da proxima; nunca por cliques do operador (fonte: glossario.md, GMS/CLAUDE.md) (a conferir)
- No Hora-Hora das etapas de mangueira o Tempo Parado e automatico e nao editavel, calculado a partir do que faltou para a meta (Real 0 = janela inteira; senao proporcional); nao e maquina parada. Na Cobertura o campo se chama OCIOSO e conta os minutos da janela sem carretel rodando (fonte: glossario.md, GMS_Diario DECISAO 27/10 MEL-255, NORMA 21/09) (a conferir)
- Meta Hora BI = Meta Hora x Minutos BI / Minutos; a meta do BI nao e proporcional a refeicao (decisao de 23/10 revogada pelo William em 30/10) (fonte: COMO_ARRUMAR_HORAHORA 11) (a conferir)
- Regua dos 21h35 (1295/1440): vale so no cartao Meta (HH Meta Util) e na HH Aderencia, e so sem hora filtrada; com uma hora selecionada ou nas barras por hora a meta e a cheia (fonte: GMS_Diario DECISAO 30/10 MEL-257, COMO_ARRUMAR_HORAHORA 11); em 30/10 ainda nao publicado (reportExtensions.json), o painel publicado pode mostrar a regra anterior (fonte: GMS_Diario DECISAO 30/10 MEL-257) (a conferir)
- Evento Cancelado: OP descartada no posto, metros = 0 e sobra = metragem que virou refugo; nunca conta como producao nem entra na meta (fonte: glossario.md, GMS_Diario NORMA 02/09) (a conferir)
- Parada, pausa e tempo excedido nunca se somam. Motivo do Tipo "Programada" (Refeicao, Reuniao, Set-up, Manut. Preventiva, Check List, Amostra, MPT, TESTE ENGENHARIA) e pausa, nao parada (fonte: GMS_Diario DECISAO 22/10 MEL-247) (a conferir)
- Parada real da Montagem = Paradas_Montagem sem TE (tempo excedido) e sem RF (refeicao), o mesmo criterio do BI (fonte: GMS_Diario DECISAO 22/10 MEL-246) (a conferir)
- A tela Hora-Hora da Montagem nao troca de turno sozinha (fonte: glossario.md, GMS/CLAUDE.md) (a conferir)

## Perguntas validadas

## Erros a evitar

## Placar
