# 04 · Glossário da fábrica

Fonte: GMS/IA/glossario.md (cópia para o Uiu, 09/11/2026). A NORMA mais nova do Diário vence (ver 08_Normas_Diario.md).


Texto copiado de `GMS/CLAUDE.md`, `GMS/GMS_Mestre.md` e das linhas NORMA/DECISAO do `GMS/GMS_Diario.md`
(a NORMA mais nova vence). Nao acrescente regra aqui sem fonte. Nao ha dado de producao neste arquivo.

## Etapas da celula (GMS/CLAUDE.md, abertura)

Celula de mangueiras hidraulicas, 8 etapas: Mandril -> Tubo -> Trancagem -> Cobertura -> Bandagem ->
Vulcanizacao -> Debandagem -> Extracao/Teste, mais Extrusora/Bobinadeira/Catenaria e Montagem.

(Grafia original do arquivo: Trançagem, Vulcanização, Extração/Teste, Extrusora/Bobinadeira/Catenária.)

## Regras de negocio

- Parada real (celula incapaz de produzir) nunca e somada com tempo excedido (produzindo acima da meta). (GMS/CLAUDE.md)
- Setup = intervalo entre a ultima peca boa de uma OAP e a primeira peca boa da proxima. Nunca por cliques do operador. (GMS/CLAUDE.md)
- A tela Hora-Hora da Montagem nao troca de turno automaticamente. (GMS/CLAUDE.md)
- No Hora-Hora das etapas de mangueira o "Tempo Parado" e calculado pelo sistema a partir do que faltou
  para a meta (Real 0 = janela inteira; senao proporcional). Nao e medicao de maquina parada. Na Cobertura
  o mesmo campo se chama OCIOSO (minutos da janela sem carretel rodando). (Diario: DECISAO 27/10 MEL-255;
  NORMA 21/09)
- Evento "Cancelado": OP descartada no posto. metros = 0 e sobra = metragem que virou refugo.
  Nunca conta como producao nem entra na meta. (Diario, NORMA 02/09)
- Evento "Parcial": fechamento de turno com a etapa ainda aberta. Nao e "Fim" e nao conta carretel
  como pronto para a etapa seguinte. (Diario, NORMA 01/09)

Parada real e setup: definicao do GMS/CLAUDE.md; o Tempo Parado do Hora-Hora e outra coisa (ver acima).

## Turnos (NORMA do GMS_Diario.md de 27/10/2026, MEL-250; vale sobre o Mestre e o CLAUDE.md)

- 1o turno: 05:20 a 13:56 (minuto do dia 320 a 836), 517 min.
- 2o turno: 13:57 a 22:19 (837 a 1339), 503 min.
- 3o turno: 22:20 a 05:19 do dia seguinte (1340 a 319), 420 min.
- Dia produtivo (data_ref): comeca as 05:20. Apontamento antes das 05:20 pertence ao dia anterior.
- Mesma fronteira em fx_Turno, fx_InicioTurnoMin, fx_GradeHoraHora e dTurno do BI.
- Historico: ate 27/10/2026 o app usou 3o turno a partir de 22:41 (o problema vem de antes de 05/10). Registros desse periodo
  feitos entre 22:20 e 22:40 estao gravados como Turno 2 (janela "22:00 - 22:20" com 41 min).
  Antes de 05/10 a virada do 1o para o 2o turno ja foi 13:47/13:48 em parte do app.
  Para comparar turnos nesses periodos, avise que a fronteira mudou.
