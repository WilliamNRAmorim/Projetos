# 09 · Mapa das listas SharePoint do GMS (nomes internos)

Fontes: instruções atuais do Uiu no Copilot Studio (09/11/2026), roteiro da Hora-Hora (06), método de limpeza da ficha, lições (03) e linhas do Diário (08). Se um nome daqui der erro, não invente outro: leia 1 item sem filtro (Top 1) e veja os nomes que vierem.

## Regras de consulta (valem para todas as listas)
- No `$filter`, `$select` e `$orderby` use o **nome interno** (field_N etc.), nunca o nome de exibição. `status_processo` e `data_hora_inicio_tubo` são nomes de exibição e não funcionam no filtro: use `field_11`, `field_16`.
- Data em filtro: `field_0 ge datetime'AAAA-MM-DDT00:00:00Z' and field_0 lt datetime'AAAA-MM-DD+1T00:00:00Z'`. Nunca `eq` com data.
- Data "só dia" na Hora-Hora é gravada como meia-noite local = `AAAA-MM-DDT03:00:00Z`. Horários vêm em UTC: Brasília = UTC − 3 h. Avise ao citar horário.
- Sempre Top 50 (ou menos). Nunca leia a lista inteira.
- Limite de visualização do SharePoint = 5.000 itens: filtro por coluna não indexada (ex.: `field_0` da Hora-Hora) numa lista grande pode falhar. Saída: filtrar por **faixa de ID** (`ID ge A and ID lt A+1500`) e filtrar o resto no resultado.
- Coluna de escolha (Choice) volta como registro: o texto está em `.Value`. No filtro OData compare com o texto (`tipo eq 'Fim'`).
- Dia produtivo começa 05:20: apontamento antes das 05:20 pertence ao dia anterior (`data_ref`). O 3º turno fica com a data do dia em que começou.

## 1) ficha_producao — uma linha por OP/lote (ficha)
- `ID` = ID da ficha (é o `origem_ID` dos eventos). `OP` = número da OP. `Mangueira` = nome da mangueira no GMS (não é o nome do SAP). `Qtd_x002e_Planejada` = quantidade planejada. Bitola e Trançadeira têm nome interno próprio (leia 1 item para ver).
- Situação (`status_processo`) = `field_11`: 'Em processo', 'Aguardando', 'Finalizado', 'Cancelado'. OPs ativas: `field_11 ne 'Finalizado' and field_11 ne 'Cancelado'`.
- Etapa atual (`processo`) = `field_10`: Mandril, Tubo, Trançadeira, Cobertura, Vulcanização, Extr./Teste (Bandagem e Debandagem também aparecem nas datas).
- Início / fim por etapa: Mandril `data_hora_inicio_mandril` / `field_9`; Tubo `field_16` / `field_17`; Trançadeira `field_19` / `field_20`; Cobertura `field_25` / `field_26`; Bandagem `field_31` / `field_32`; Vulcanização `field_35` / `field_36`; Debandagem `field_39` / `field_40`; Extração `field_43` / `field_44`.
- Quantidade (m) por etapa: Mandril `field_6`; Tubo `field_14`; Trançagem `field_22`; Cobertura `field_28`; Bandagem `field_33`; Vulcanização `field_37`; Debandagem `field_41`; Extração `field_46` (= produção boa do GMS).
- Operador por etapa: `field_8`, `field_18`, `field_24`, `field_30`, `field_34`, `field_38`, `field_42`, `field_47`. Defeito: tubo `field_15`, trançagem `field_23`, cobertura `field_29`.
- Turno por etapa: `Turno_mandril`, `Turno_Tubo`, `Turno_Cobertura`, `Turno_Bandagem`, `Turno_Debandagem` (misturam "3" e "Turno 3"). Quantidade por turno da ficha mãe: `Qtd_Turno1`, `Qtd_Turno2`, `Qtd_Turno3`.
- Mês da ficha = `Created`. Nunca filtrar por `Modified`.
- Pegadinhas: o Tubo divide a ficha quando sobra tubo (split): `Quantidade_mandril` da ficha é reduzida (500 vira 250) e nasce ficha filha "(devolvida)"; o gabarito do Mandril é `Qtd_Turno1+2+3` da ficha mãe. Valores 111, 1111, 11111 são digitação de preenchimento. Lote padrão do carretel por bitola: 3/4/5 → 800 m; 6/7/8 → 680; 10 → 460; 12 → 400; 16 → 250 (mandril pode ter até o dobro; acima de 130% do lote nas outras etapas é suspeito).

## 2) Hora-Hora — produção hora a hora por máquina (célula)
- `Title` = "DD/MM/AAAA - Nº Turno - CÉLULA". `field_0` Data · `field_2` Célula (máquina, ex.: TH07) · `field_3` Hora (rótulo da janela, ex.: "22:00 - 22:20") · `field_4` Mangueira · `field_5` Meta Hora · `field_6` Meta Acum · `field_7` Real. Hora · `field_8` Real. Acum · `field_9` Diferença (Meta − Real) · `field_11` Tempo Parado (min) · `field_12` Motivo · `field_13` Motivo 2 · `field_14` Comentário · `field_15` Rendimento (%) · `TurnoH` ('1º Turno', '2º Turno', '3º Turno') · `Status` ('Finalizado') · `Minutos` (duração da janela).
- Tempo Parado é calculado pelo app a partir do que faltou para a meta (não é máquina parada medida). Na Cobertura o mesmo campo é OCIOSO.
- Grade de janelas e minutos por turno: ver 06_Roteiro_HoraHora.md.
- `Hora_Hora_Mandril` e `Hora_Hora_Tubo` estão praticamente vazias: não use para paradas.

## 3) Eventos_Producao — um evento por etapa
- `etapa` (Choice), `tipo` (Choice: Início, Fim, Parcial, Cancelado), `data_hora`, `data_ref`, `turno` (1, 2 ou 3; não é Choice), `metros`, `refugo`, `sobra`, `operador`, `recurso`, `carretel`, `origem_ID` (= `ID` da ficha; o evento não grava a OP).
- Fim = etapa concluída. Parcial = fechamento de turno com a etapa aberta (não é Fim, não libera carretel). Cancelado = OP descartada no posto: `metros` = 0 e `sobra` = metragem que virou refugo; nunca conta como produção.
- `recurso` grava a trançadeira de ORIGEM em todos os eventos da ficha, não a máquina daquela etapa. Tem grafias diferentes para a mesma máquina (TH07/TH-07, TO04/TO-04, TH05/TH.05): normalize antes de agrupar.

## 4) Paradas_Montagem
- `field_1` Data · `field_2` Turno · `field_3` Célula · `field_5` Motivo · `field_6` TempoParadoMin · `OPVinculada`.
- Parada real da Montagem = sem TE (tempo excedido) e sem RF (refeição), mesmo critério do BI. A Hora-Hora da Montagem não troca de turno sozinha.

## 5) Plano_OPs — plano de OPs (espelho do SAP)
- `Title` = OP · `PN` (código do material) · `QtdPlanejada` · `Encerrada` · `StatusSAP`.
- Serve para ligar OP do GMS ao material SAP quando o nome da mangueira não bate.

## 6) TiposErros — refugo do GMS
- `op_id`, `codigoerro` (causa), `quantidade` (m), `criado`, `datahorarefugo`, `turno_erro`, `trancadeira`. Não tem nome da mangueira: ligar à ficha pela OP. Linhas novas (desde set/2026) vêm sem Id; há grupos repetidos por OP + erro + quantidade + criado.

## 7) RegistrosInspeção — inspeção boa
- `op_id`, `quantidade` (m, texto), `datahorainspecao`, `turnoteste`, `mangueira` (às vezes vazio), `cabine_teste`.

## 8) Listas de apoio
ControleExtrusora_estrutura, RefugoExtrusora_estrutura, Refugo_Bobinadeira, FifoBobinadeira, lista_carreteis, Historico_Carretel (`metros_entrada` guarda o original do Tubo no split), Controle_Catenaria, MapeamentoSetor. Leia 1 item antes de filtrar para ver os nomes internos.

## 9) Log_Uiu (a criar na F3)
Uma linha por correção feita pelo Uiu: quem, quando, lista, item (ID), campo, antes, depois, receita do Manual_BO.

## Fora do SharePoint
- SAP (MB51, COOIS) e BD Packing List não estão em lista: chegam como export (Excel/CSV). Ver 07_Dados_SAP_x_GMS.md.
- Ligação geral: a OP liga tudo (ficha `OP` = MB51 `Order` = TiposErros/RegistrosInspeção `op_id` = Plano_OPs `Title`).
