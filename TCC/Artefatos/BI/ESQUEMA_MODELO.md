# Esquema do modelo GMS (tabelas reais) — para gerar dados fictícios


## ControleExtrusora_estrutura  (34 colunas; mode: import)
colunas: OP_ID:string, OP:double, Bitola:double, cod_mandril:string, desmoldante:string, quantidade:double, operador:string, lote_mandril:string, data_hora_inicio:dateTime, data_hora_final:dateTime, Turno:string, Observacao:string, Criado:string, Color Tag:string, Compliance Asset Id:string, ID:int64, Content Type:string, Modified:dateTime, Created:dateTime, Created By:string, Modified By:string, Version:string, Attachments:string, Edit:string, Type:string, Item Child Count:string, Folder Child Count:string, Label setting:string, Retention label:string, Retention label Applied:string, Label applied by:string, Item is a Record:string, App Created By:string, App Modified By:string

## Controle_Catenaria  (34 colunas; mode: import)
colunas: Title:string, DataHora:dateTime, Maquina:string, Mangueira:string, NFios:double, DiamEspecPol:string, DiamEspecMM:string, DiamAtualMM:string, TensaoPol:string, Aprovado:boolean, ENumber:string, Observacoes:string, Turno:double, Color Tag:string, Compliance Asset Id:string, ID:int64, Content Type:string, Modified:dateTime, Created:dateTime, Created By:string, Modified By:string, Version:string, Attachments:string, Edit:string, Type:string, Item Child Count:string, Folder Child Count:string, Label setting:string, Retention label:string, Retention label Applied:string, Label applied by:string, Item is a Record:string, App Created By:string, App Modified By:string

## Etapas  (9 colunas; mode: import)
colunas: OP:?, Mangueira:?, Etapa:?, OrdemEtapa:?, DataHora:?, Metragem:?, Data:?, Turno:?, AnoMes:?

## Eventos_Producao  (15 colunas; mode: import)
colunas: Eventos:string, origem:string, origem_ID:double, etapa:string, tipo:string, data_hora:dateTime, data_ref:dateTime, turno:double, bitola:double, metros:double, refugo:double, operador:string, recurso:string, carretel:string, sobra:double

## FifoBobinadeira  (47 colunas; mode: import)
colunas: Title:string, Linha:double, Mangueira:string, Trancadeira:string, Quantidade:string, Status:string, CodProduto:string, QtdBobinas:double, Metragem:double, NFios:double, RT:string, LI:string, Operador:string, Turno:double, DataHoraInicio:dateTime, DataHoraSalvo:dateTime, DataHoraFinal:dateTime, Maquina de Bobinagem:string, Observa:?, Color Tag:string, Compliance Asset Id:string, ID:int64, Content Type:string, Modified:dateTime, Created:dateTime, Created By:string, Modified By:string, Version:string, Attachments:string, Edit:string, Type:string, Item Child Count:string, Folder Child Count:string, Label setting:string, Retention label:string, Retention label Applied:string, Label applied by:string, Item is a Record:string, App Created By:string, App Modified By:string, OP_Consumo:string, FichaID_Consumo:double, DataHoraConsumo:dateTime, Carrinho:double, MotivoCancelamento:string, CanceladoPor:string, DataHoraCancelamento:dateTime

## Historico_Carretel  (31 colunas; mode: import)
colunas: carretel_id:string, OP_ID:double, etapa:string, mangueira:string, metros_entrada:double, metros_saida:double, data_hora_entrada:dateTime, data_hora_saida:dateTime, operador:string, status:string, Color Tag:string, Compliance Asset Id:string, ID:int64, Content Type:string, Modified:dateTime, Created:dateTime, Created By:string, Modified By:string, Version:string, Attachments:string, Edit:string, Type:string, Item Child Count:string, Folder Child Count:string, Label setting:string, Retention label:string, Retention label Applied:string, Label applied by:string, Item is a Record:string, App Created By:string, App Modified By:string

## Hora-Hora  (10 colunas; mode: import)
colunas: Turno:string, Data:dateTime, C:?, Tempo Parado (min):double, Motivo:string, Motivo 2:string, Comentário / Ação:string, Minutos:double, Motivo Padrão:?, Motivo 2 Padrão:?

## HosePlanMensal  (26 colunas; mode: import)
colunas: Title:string, Construction:string, PlanMes:double, MTD:double, Atraso:double, Color Tag:string, Compliance Asset Id:string, ID:int64, Content Type:string, Modified:dateTime, Created:dateTime, Created By:string, Modified By:string, Version:string, Attachments:string, Edit:string, Type:string, Item Child Count:string, Folder Child Count:string, Label setting:string, Retention label:string, Retention label Applied:string, Label applied by:string, Item is a Record:string, App Created By:string, App Modified By:string

## Medidas  (0 colunas; mode: import)
colunas: 

## OrdensPlanejadas  (27 colunas; mode: import)
colunas: M:?, Tran:?, OP:double, Mangueira:string, Qtd.Planejada:double, Data:dateTime, Color Tag:string, Compliance Asset Id:string, ID:int64, Content Type:string, Modified:dateTime, Created:dateTime, Created By:string, Modified By:string, Version:string, Attachments:string, Edit:string, Type:string, Item Child Count:string, Folder Child Count:string, Label setting:string, Retention label:string, Retention label Applied:string, Label applied by:string, Item is a Record:string, App Created By:string, App Modified By:string

## Paradas_Montagem  (8 colunas; mode: import)
colunas: Data:dateTime, Turno:string, Celula:string, RegistradoEm:dateTime, Motivo:string, TempoParadoMin:double, Observacao:string, OPVinculada:string

## Part Number x Construction  (21 colunas; mode: import)
colunas: Title:string, Dash size:double, Wide Braiders:string, Construction:string, Braider:string, ID:int64, Modified:dateTime, Created:dateTime, Created By:string, Modified By:string, Version:string, Attachments:string, Edit:string, Type:string, Retention label Applied:string, Label applied by:string, Item is a Record:string, C_Standard_Plan:?, Decks_Plan:?, Wires_Plan:?, Tipo_Plan:?

## Producao_Montagem  (16 colunas; mode: import)
colunas: Data:dateTime, Turno:string, Celula:string, PN:string, OT:int64, QtdOT:double, InicioEm:dateTime, FimEm:dateTime, QtdProduzida:double, MetaHora:double, DuracaoMin:double, DuracaoSeg:double, Status:string, Cracha:string, DuracaoRealMin:double, DescontoMin:double

## RegistrosInspeção  (35 colunas; mode: import)
colunas: OP_ID:double, Quantidade:double, Diametro_Interno:double, Diametro_Externo:double, Concentricidade:string, DataHoraInspecao:dateTime, TurnoTeste:double, Created:dateTime, Mangueira:string, CodigoDefeito:string, Tran:?, Title:string, Color Tag:string, Compliance Asset Id:string, Defeito_Inspe:?, Modified:dateTime, ID:int64, Content Type:string, Created By:string, Modified By:string, Version:string, Attachments:string, Edit:string, Type:string, Item Child Count:string, Folder Child Count:string, Label setting:string, Retention label:string, Retention label Applied:string, Label applied by:string, Item is a Record:string, App Created By:string, App Modified By:string, DataInspecao:?, cabine_teste:string

## TiposErros  (32 colunas; mode: import)
colunas: OP_ID:double, CodigoErro:string, Quantidade:double, Created:dateTime, DataHoraRefugo:dateTime, Tran:?, Turno Erro:string, Title:string, Color Tag:string, Compliance Asset Id:string, OP_refugo:double, ID_RegistroInspecao:string, Modified:dateTime, ID:int64, Content Type:string, Created By:string, Modified By:string, Version:string, Attachments:string, Edit:string, Type:string, Item Child Count:string, Folder Child Count:string, Label setting:string, Retention label:string, Retention label Applied:string, Label applied by:string, Item is a Record:string, App Created By:string, App Modified By:string, DataRefugo:?, cabine_teste:string

## dCalendario  (9 colunas; mode: import)
colunas: Date:?, Ano:?, Mês Nº:?, M:?, AnoM:?, Dia:?, Dia Semana:?, Semana:?, Trimestre:?

## dMetaMontagem  (3 colunas; mode: import)
colunas: Celula:?, Turno:?, MetaDia:?

## dMotivoParada  (2 colunas; mode: import)
colunas: Motivo:string, Tipo:string

## fFluxoEtapas  (14 colunas; mode: import)
colunas: ID_Ficha:?, Ordem_Etapa:?, Etapa:?, Ini_Fila:?, Ini_Proc:?, Fim:?, Fila_Medida:?, Data_Fim:?, Fila_h:?, Proc_h:?, Lead_h:?, Valida:?, Mangueira:?, Bitola:?

## ficha_producao  (150 colunas; mode: import)
colunas: ID:int64, processo:string, Carretel Entrada:string, Carretel Saida:string, Bitola:double, Mangueira:string, OP:double, status_processo:string, Tran:?, cod_mandril:string, Turno_mandril:string, data_hora_inicio_mandril:dateTime, data_hora_final_mandril:dateTime, lote_mandril:string, desmoldante_mandril:string, diametro_mandril:double, operador_mandril:string, quantidade_mandril:double, Turno_Tubo:string, data_hora_inicio_tubo:dateTime, data_hora_final_tubo:dateTime, diametro_tubo:double, defeito_tubo:double, quantidade_tubo:double, operador_tubo:string, Turno_Tran:?, data_hora_final_trancadeira:dateTime, data_hora_inicio_trancadeira:dateTime, Diametro_Tran:?, quantidade_trancagem:double, defeito_trancagem:double, operador_trancagem:string, Turno_Cobertura:string, data_hora_inicio_cobertura:dateTime, data_hora_final_cobertura:dateTime, diametro_cobertura:double, defeito_cobertura:double, quantidade_cobertura:double, operador_cobertura:string, Turno_Bandagem:string, data_hora_inicio_bandagem:dateTime, data_hora_final_bandagem:dateTime, operador_bandagem:string, C:?, C:?, quantidade_bandagem:double, data_hora_final_vulcanizacao:dateTime, data_hora_inicio_vulcanizacao:dateTime, Turno_Vulcaniza:?, InicioResfriamento_Vulcanizacao:dateTime, quantidade_vulcanizacao:double, operador_vulcanizacao:string, Turno_Debandagem:string, data_hora_inicio_debandagem:dateTime, data_hora_final_debandagem:dateTime, quantidade_debandagem:double, operador_debandagem:string, Turno_Extr:?, data_hora_inicio_extracao:dateTime, data_hora_final_extracao:dateTime, quantidade_extracao:double, operador_extracao:string, Cod.Cobertura:string, Cod.CompostoTubo:string, Created:dateTime, Data de Validade  do composto cobertura:dateTime, Data de Validade do Composto Tubo:dateTime, Lote Composto Tubo:string, Lote_cobertura:string, Lote_Tran:?, N:?, Cod_Tran:?, InicioAguardando_Tran:?, InicioAguardando_Tubo:dateTime, InicioAguardando_bandagem:dateTime, InicioAguardando_Vulcaniza:?, InicioAguardando_Debandagem:dateTime, InicioAguardando_Extr./Teste:dateTime, InicioEmProcesso_Mandril:dateTime, InicioEmProcesso_Tubo:dateTime, InicioEmProcesso_Tran:?, InicioEmProcesso_Cobertura:dateTime, InicioEmProcesso_Bandagem:dateTime, InicioEmProcesso_Vulcaniza:?, InicioEmProcesso_Debandagem:dateTime, InicioEmProcesso_Extr./Teste:dateTime, InicioAguardandoCobertura:dateTime, Qtd_Turno1:double, Qtd_Turno2:double, Qtd_Turno3:double, Modified:dateTime, Qtd_Turno1_Cobertura:double, Qtd_Turno2_Cobertura:double, Qtd_Turno3_Cobertura:double, Qtd_Turno1_Bandagem:double,  Qtd_Turno2_Bandagem:double,  Qtd_Turno3_Bandagem:double, Qtd_Turno1_Vulcanizacao:double, Qtd_Turno2_Vulcanizacao:double, Qtd_Turno3_Vulcanizacao:double, Qtd_Turno1_Debandagem:double, Qtd_Turno2_Debandagem:double, Qtd_Turno3_Debandagem:double, DataFinalizacao:dateTime, Observa:?, Observa:?, Observa:?, Observa:?, PackList Cabine:string, ordem_producao:double, cod_mangueira:string, lote:string, Processo.1:string, PostCure Qtd:string, PostCure Data:string, Postcure Horario de termino:string, Registro Defeito:string, Qtd. Planejada:double, Turno:string, board choice1:string, QTran:?, Created By:string, Modified By:string, Version:string, Attachments:string, Edit:string, Type:string, Retention label Applied:string, Label applied by:string, Item is a Record:string, Mangueira_Limpa:?, Bitola_Corrigida:?, Flag_Data_Invertida:?, OP_Texto:?, Metragem_Extracao:?, Turno_Extracao_Limpo:?, TempoCiclo_Horas:?, defeito_trancagem_trat:?, defeito_cobertura_trat:?, defeito_tubo_trat:?, Esta_Ativa:?, Flag_Qualidade_Bitola:?, AnoMes_Producao:?, MesProducao:?, Turno_Producao:?, DataProducao:?, maquina_mandril:string, Observa:?, Observa:?, cabine_teste:string

## lista_carreteis  (38 colunas; mode: import)
colunas: ID:int64, T:?, op:string, etapa_processo:string, metros_restantes:double, mangueira_atual:string, Material:string, Status:string, Bitola:double, cod_mandril:string, desmoldante:string, quantidade_metros:double, OP_extrusora:string, operador_extrusora:string, data_enchimento:dateTime, data_consumo:dateTime, Color Tag:string, Compliance Asset Id:string, lote:string, OP.1:double, Content Type:string, Modified:dateTime, Created:dateTime, Created By:string, Modified By:string, Version:string, Attachments:string, Edit:string, Type:string, Item Child Count:string, Folder Child Count:string, Label setting:string, Retention label:string, Retention label Applied:string, Label applied by:string, Item is a Record:string, App Created By:string, App Modified By:string
