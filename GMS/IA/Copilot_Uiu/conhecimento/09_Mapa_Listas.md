# 09 · Mapa das fontes de dados do GMS (nomes internos)

Lido direto do SharePoint pela API em 09/11/2026 (campos visíveis e editáveis de cada lista; contagem de itens do dia). Site: `https://danfoss.sharepoint.com/sites/OperationsGuaratingueta` (Imagens Fitas fica em `/sites/DelineamentoHM`). São todas as fontes do painel Data do app: 31 listas SharePoint + tabelas Excel (seção final).

Formato de cada coluna: `nome_interno` = nome de exibição (tipo). **IDX** = coluna indexada.

## Regras de consulta (valem para todas as listas)
- No `$filter`, `$select` e `$orderby` use o **nome interno**, nunca o de exibição. Ex.: `status_processo` é exibição; o interno é `field_11`.
- Caracteres especiais viram código no nome interno: `ç` = `_x00e7_`, `ã` = `_x00e3_`, `.` = `_x002e_`, `/` = `_x002f_`, espaço = `_x0020_`, `°` = `_x00b0_`. Ex.: Trançadeira = `Tran_x00e7_adeira`.
- **Limite de 5.000 itens:** listas acima disso (Hora-Hora, Eventos_Producao, RegistrosInspeção, Historico_Carretel, TiposErros chega perto) só aceitam filtro cujo **primeiro critério é coluna IDX** e devolve menos de 5.000. Filtro por coluna sem índice nessas listas falha: filtre por coluna IDX (data) ou por faixa de `ID` (`ID ge A and ID lt A+1500`) e filtre o resto no resultado.
- Data: `campo ge datetime'AAAA-MM-DDT00:00:00Z' and campo lt datetime'AAAA-MM-DD+1T00:00:00Z'`. Nunca `eq` com data. Horários em UTC: Brasília = UTC − 3 h. Data "só dia" da Hora-Hora = `AAAA-MM-DDT03:00:00Z`.
- Choice: no filtro compare com o texto (`tipo eq 'Fim'`). Valor fora da lista de escolhas pode existir (ex.: `tipo` = 'Cancelado').
- Sempre Top 50 ou menos. Nunca leia a lista inteira. Nunca filtre por `Modified`.
- Dia produtivo começa 05:20 (Brasília); o 3º turno fica com a data do dia em que começou.
- Se um nome daqui der erro, não invente: leia 1 item sem filtro e veja os nomes.

---

## A. Produção da célula de mangueiras

### ficha_producao (3.114 itens) — uma linha por OP/lote
- Identidade: `ID` (= `origem_ID` dos eventos) · `OP` = OP (número, **IDX**) · `field_1` = ordem_producao · `Mangueira` = Mangueira (**IDX**) · `field_2` = cod_mangueira · `Bitola` · `Tran_x00e7_adeira` = Trançadeira · `maquina_mandril` (**IDX**) · `cabine_teste` · `Qtd_x002e_Planejada` = Qtd. Planejada · `field_12` = lote · `Processo` · `Title`.
- Estado: `field_10` = processo (etapa atual: Mandril, Tubo, Trançadeira, Cobertura, Bandagem, Vulcanização, Debandagem, Extr./Teste) · `field_11` = status_processo ('Em processo', 'Aguardando', 'Finalizado', 'Cancelado') · `DataFinalizacao`.
- Início / fim por etapa: Mandril `data_hora_inicio_mandril` / `field_9` · Tubo `field_16` / `field_17` · Trançadeira `field_19` / `field_20` · Cobertura `field_25` / `field_26` · Bandagem `field_31` / `field_32` · Vulcanização `field_35` / `field_36` (+ `InicioResfriamento_Vulcanizacao`) · Debandagem `field_39` / `field_40` · Extração `field_43` / `field_44`.
- Entrada na fila e início em processo por etapa (ótimo para OP travada): `InicioAguardando_Tubo`, `InicioAguardando_Mandril` (exibição diz "InicioAguardando_Trançadeira": é a fila da Trançagem), `InicioAguardandoCobertura`, `InicioAguardando_bandagem0`, `InicioAguardando_Vulcaniza_x00e7`, `InicioAguardando_Debandagem`, `InicioAguardando_Extr_x002e__x00`; `InicioEmProcesso_Mandril`, `_Tubo`, `_Tran_x00e7_agem`, `_Cobertura`, `_Bandagem`, `_Vulcaniza_x00e7`, `_Debandagem`, `_Extr_x002e__x00` (todos com o prefixo `InicioEmProcesso`).
- Quantidade (m): Mandril `field_6` · Tubo `field_14` · Trançagem `field_22` · Cobertura `field_28` · Bandagem `field_33` · Vulcanização `field_37` · Debandagem `field_41` · Extração `field_46` (= produção boa do GMS).
- Defeito (m): tubo `field_15` · trançagem `field_23` · cobertura `field_29`. `RegistrodeDefeitos` (texto).
- Operador: mandril `field_8` · tubo `field_18` · trançagem `field_24` · cobertura `field_30` · bandagem `field_34` · vulcanização `field_38` · debandagem `field_42` · extração `field_47`.
- Turno: `Turno` · `Turno_mandril` · `Turno_Tubo` · `Turno_Tran_x00e7_agem` · `Turno_Cobertura` · `Turno_Bandagem` · `Turno_Vulcaniza_x00e7__x00e3_o` · `Turno_Debandagem` (texto, misturam "3" e "Turno 3") · `Turno_Extr_x002f_Teste` (número).
- Quantidade por turno: `Qtd_Turno1/2/3` (ficha mãe; gabarito do Mandril) e `Qtd_Turno1/2/3_Cobertura`, `_Bandagem`, `_Vulcanizacao`, `_Debandagem`.
- Carretel: `de_para_carretel` = Carretel Entrada · `CarretelSaida`.
- Materiais e rastreio: `field_4` cod_mandril · `field_5` diametro_mandril · `field_13` diametro_tubo · `field_27` diametro_cobertura · `Diametro_Tran_x00e7_agem` · `lote_mandril` · `Desmoldante` · `Cod_x002e_CompostoTubo` · `LoteCompostoTubo` · `DatadeValidadedoComposto` · `Cod_Tran_x00e7_agem` · `Lote_Tran_x00e7_agem` · `N_x00b0_Picks` · `QTran_x00e7_as_x003f_` (Choice 1/2/3) · `Cod_Tranc_1aTrama`, `Lote_Tranc_1aTrama`, `Picks_Tranc_1aTrama`, `Diam_Tranc_1aTrama` · `Cod_x002e_Cobertura` · `Lote_cobertura` · `DatadeValidadedocompostocobertur` · `C_x00f3_d_Fita_Bandagem` · `C_x00f3_digo_Filme_UHMWPE` · `PostCureQtd`, `PostCureData`, `PostcureHorariodetermino` · `board_x0020_choice1` (Choice Mandril/Tubo) · `PackListCabine` (link).
- Observações (Note): `Observa_x00e7__x00e3_o_mandril`, `_tubo`, `_Tran_x00e`, `_Cobertura`, `_Bandagem`, `_Debandage` (prefixo `Observa_x00e7__x00e3_o`).
- Pegadinhas: o Tubo divide a ficha quando sobra tubo (`field_6` reduzido, ficha filha "(devolvida)"); 111/1111/11111 são preenchimento; lote padrão por bitola 3/4/5 → 800 m, 6/7/8 → 680, 10 → 460, 12 → 400, 16 → 250. Mês da ficha = `Created`.

### Eventos_Producao (16.243) — um evento por etapa
- `origem` (Choice: ficha_producao, ControleExtrusora, FifoBobinadeira) · `origem_ID` (ID na lista de origem; **sem índice**) · `etapa` (Choice **IDX**: Mandril, Tubo, Trançagem, Cobertura, Bandagem, Vulcanização, Debandagem, Extração, Extrusora, Bobinadeira) · `tipo` (Choice **IDX**: Início, Fim, Parcial; 'Cancelado' também é gravado) · `data_hora` (**IDX**) · `data_ref` (**IDX**) · `turno` (número) · `bitola` · `metros` · `refugo` · `sobra` · `operador` · `recurso` · `carretel` · `Title`.
- Para achar os eventos de uma ficha: filtre primeiro por `data_ref` (IDX) numa faixa de datas e depois `origem_ID eq <ID>`; só `origem_ID` falha pelo limite de 5.000.
- Fim = etapa concluída. Parcial = fechamento de turno com a etapa aberta. Cancelado = OP descartada: `metros` = 0 e `sobra` = refugo; nunca é produção.
- `recurso` é a trançadeira de ORIGEM da ficha, não a máquina da etapa; tem grafias diferentes (TH07/TH-07, TO04/TO-04, TH05/TH.05).

### Hora-Hora (32.452) — produção hora a hora por máquina
- `Title` (**IDX**, "DD/MM/AAAA - Nº Turno - CÉLULA") · `field_0` = Data (**IDX**) · `field_2` = Célula (**IDX**) · `field_3` = Hora (janela) · `field_4` = Mangueira · `field_5` = Meta Hora · `field_6` = Meta Acum · `field_7` = Real. Hora · `field_8` = Real. Acum · `field_9` = Diferença · `field_11` = Tempo Parado (min) · `field_12` = Motivo · `field_13` = Motivo 2 · `field_14` = Comentário / Ação · `field_15` = Rendimento · `TurnoH` = Turno (**IDX**: '1º Turno', '2º Turno', '3º Turno') · `Status` · `Minutos`.
- Filtro por dia: `field_0` (IDX) numa faixa de 1 dia funciona; período longo, por faixa de ID. Grade de janelas: 06_Roteiro_HoraHora.md.

### Hora_Hora_Mandril (2) e Hora_Hora_Tubo (0) — legadas, quase vazias; não use
- Mandril: `Data`, `Hora`, `Turno`, `Motivo`, `Motivo2`, `TempoParado`, `Coment_x00e1_rio`, `Status`. Tubo: `field_1` Hora … `field_8` Status (`field_7` Data é texto).

### lista_carreteis (110) — carretéis de mandril em estoque/uso
- `Title` · `field_1` = op · `field_2` = lote · `field_3` = etapa_processo · `OP` (número) · `Status` · `Bitola` · `cod_mandril` · `Material` · `mangueira_atual` · `quantidade_metros` · `metros_restantes` · `OP_extrusora` · `operador_extrusora` · `data_enchimento` · `data_consumo` · `desmoldante`.

### CarreteisMandril (20) — carretéis da extrusora para a solda do mandril
- `field_1` Status · `field_2` Bitola · `field_3` cod_mandril · `field_4` quantidade_metros · `field_5` OP_extrusora · `field_6` operador_extrusora · `field_7` data_enchimento · `field_8` OP_solda · `field_9` data_consumo · `field_10` desmoldante.

### Historico_Carretel (11.106, sem índice) — custódia do carretel por etapa
- `field_1` = OP_ID · `field_2` = etapa · `field_3` = mangueira · `field_4` = metros_entrada (guarda o original do Tubo no split) · `field_5` = metros_saida · `field_6` = data_hora_entrada · `field_7` = data_hora_saida · `field_8` = operador · `status`. Consulta só por faixa de ID.

### Estado_Trancadeiras (10) — uma linha por trançadeira (alimentada por fluxo)
- `Title` (máquina) · `Status` · `Mangueira_Atual` · `Bitola` · `Velocidade` · `Maquina_Vel` · `Quantidade_m` · `Hora_Parada` · `Proxima_Mangueira` · `Critico` · `Alerta_Enviado` · `Ultimo_Fingerprint` · `Atualizado_Em`.

## B. Qualidade e refugo

### RegistrosInspeção (19.778) — inspeção boa (teste)
- `OP_ID` (**IDX**) · `Quantidade_Inspe_x00e7__x00e3_o` = Quantidade (m) · `Defeito_Inspe_x00e7__x00e3_o` · `CodigoDefeito` (Choice A–P: A Quebra de fio, B Set up/alimentação de fio, C Caroço/ondulação, D Marcação errada, E Trança aparente, F Bolhas, G Falha na bandagem, H Eject test, I/J Diâmetro externo maior/menor, K/L Diâmetro interno maior/menor, M Excentricidade, N Torção na autoclave, O Pontas, P Não identificado) · `DataHoraInspecao` (**IDX**) · `TurnoTeste` · `Mangueira` (**IDX**) · `Tran_x00e7_adeira` · `cabine_teste` · `Diametro_Interno` · `Diametro_Externo` · `Concentricidade`.

### TiposErros (6.906) — refugo do GMS
- `A` = CodigoErro · `_x0043_` = Quantidade (m) · `OP_ID` (**IDX**) · `OP_refugo` · `ID_RegistroInspecao` · `DataHoraRefugo` · `Tran_x00e7_adeira` · `TurnoErro` · `cabine_teste`. Sem nome de mangueira: ligar à ficha pela OP. Há grupos repetidos por OP + erro + quantidade + data.

### Refugo_Bobinadeira (1.261)
- `field_2` DataHoraRefugo · `field_3` Operador · `field_4` Turno · `field_5` CodigoFio · `field_6` QuantidadeRefugo · `Maquina` · `Motivos` · `Observacao`.

### RefugoExtrusora_estrutura (142) — refugo da extrusora de mandril
- `field_2` Bitola · `field_3` cod_mandril · `field_4` CodigoErro · `field_5` Quantidade · `field_6` operador · `field_7` DataHoraRefugo · `field_8` Turno · `field_9` Observacao · `field_10` Criado (texto).

### Baixa de Composto (0 itens) — refugo de composto (ainda sem uso)
- `Data_do_refugo` · `Turno` (Choice 1°/2°/3° Turno) · `Composto` (Choice) · `Local` (Choice) · `Operador` (Lookup) · `Massa_x0028_Kg_x0029_` · `Motivo` (MultiChoice).

### Controle_Catenaria (466) — controle de fios na catenária
- `DataHora` · `Maquina` · `Mangueira` · `NFios` · `DiamEspecPol` · `DiamEspecMM` · `DiamAtualMM` · `TensaoPol` · `Aprovado` (sim/não) · `ENumber` · `Turno` · `Observacoes`.

### AMDM02_* — controle de diâmetro e picks da trançagem (formulário AM-DM-02, piloto)
- `AMDM02_Folha` (4): uma folha por máquina e dia: `Data` (**IDX**), `Maquina` (**IDX**), `Tranca` (**IDX**), `PN`, `BRDCode`, `Caracteristica`, `Responsavel`, limites `ODLie`/`ODNom`/`ODLse`, `PickLie`/`PickLse`, `Tensao1..5`, `Fios1..5`, `ODTubo1..5`, `FiosSobrepostos`, `NPicks`, `ODTranca1..5`, `Observacoes`.
- `AMDM02_Janela` (3): medições por janela: `IdFolha` (**IDX**), `Janela` (**IDX**), `Turno`, `Amostra1..5`, `Soma`, `Media`, `Amplitude`, `LancadoPor`, `LancadoEm`, `HoraColeta` (**IDX**).
- `AMDM02_Registro` (2): `IdFolha` (**IDX**), `Tranca`, limites, `NPicks`, `ODTranca1..5`, `Operador`, `LancadoEm`.
- `AMDM02_Spec` (58): especificação por PN: `PARTNUMBER`, `BRD_CODE`, `OD1_MIN/MED/MAX`, `OD2_MIN/MED/MAX`, `PICK1_MIN/MAX`, `PICK2_MIN/MAX`.

## C. Extrusora e bobinadeira

### ControleExtrusora_estrutura (121) — produção da extrusora de mandril
- `field_2` OP · `field_4` Bitola · `field_5` cod_mandril · `field_6` desmoldante · `field_7` quantidade · `field_8` operador · `field_9` lote_mandril · `field_10` data_hora_inicio · `field_11` data_hora_final · `field_12` Turno · `field_13` Observacao · `field_14` Criado (texto).

### FifoBobinadeira (1.108) — fila FIFO de bobinas de fio para as trançadeiras
- `field_1` Linha · `field_2` Mangueira · `field_3` Trancadeira · `field_4` Quantidade (texto) · `field_5` Status · `field_6` CodProduto · `field_7` QtdBobinas · `field_8` Metragem · `field_9` NFios · `field_10` RT · `field_11` LI · `field_12` Operador · `field_13` Turno · `field_14` DataHoraInicio · `field_15` DataHoraSalvo · `field_16` DataHoraFinal · `MaquinadeBobinagem` · `carrinho` · `OP_Consumo` · `FichaID_Consumo` · `DataHoraConsumo` · `MotivoCancelamento` · `CanceladoPor` · `DataHoraCancelamento` · `Observa_x00e7__x00e3_o`.

## D. Montagem

### Producao_Montagem (2.598) — uma linha por OT apontada
- `field_1` Data · `field_2` Turno · `field_3` Celula · `field_4` PN · `field_5` OT · `field_6` QtdOT · `field_7` InicioEm · `field_8` FimEm · `field_9` QtdProduzida · `field_10` MetaHora · `field_11` DuracaoMin · `field_12` DuracaoSeg · `field_13` Status · `Cracha` · `DuracaoRealMin` · `DescontoMin`.

### Paradas_Montagem (2.452)
- `field_1` Data · `field_2` Turno · `field_3` Celula · `field_4` RegistradoEm · `field_5` Motivo · `field_6` TempoParadoMin · `field_7` Observacao · `OPVinculada`.
- Parada real = sem TE (tempo excedido) e sem RF (refeição), igual ao BI. A Hora-Hora da Montagem não troca de turno sozinha.

## E. Plano, SAP e packing

### Plano_OPs (527) — plano de OPs (espelho do SAP)
- `Title` = OP · `PN` · `Trancadeira` · `Mes` · `Origem` · `Tipo` · `QtdPlanejada` · `StatusSAP` · `Encerrada` · `ProdTuboOK` · `OKPeloGMS` · `Atualizado`.

### Excecoes_OP (2) — pedidos de exceção para usar OP fora do plano
- `Tela` · `PN` · `Motivo` · `PedidoPor` · `Status` · `AprovadoPor` · `DataPedido` · `DataDecisao`.

### Conferencia_SAP (191) — casos da conferência GMS x SAP
- `Title` (**IDX**) · `OP` · `PN` · `Categoria` · `Status` (**IDX**) · `ProvavelOP` · `Acao` · `QuemResolve` · `Cabine` · `Responsavel` · `Prioridade` · `GMS_m` · `Refugo_m` · `SAP_m` · `Packing_m` · `Dif_m` · `Detalhe` · `Tratativa` · `DataRef` · `DataDeteccao` · `DataTratativa`.

### Packing_Manual (635) — lances lançados à mão para regularizar
- `Mangueira` · `Lances` (Note) · `TotalM` · `Motivo` · `Responsavel` · `Turno` · `Status` (Choice Pendente/Regularizado) · `DataHoraImp` · `OrigemBD` · `FichaCandidata`.

### Packing_Pallets (383) — pallets impressos na cabine
- `FichaID` · `Pallet` · `LanceIDs` (Note) · `QtdLances` · `TotalM` · `Turno` · `DataHoraImp` · `LinkPDF`.

## F. Cadastros e acesso

### Colaboradores (42)
- `field_1` Nome · `field_2` Cargo · `field_3` Centro de Resultado (código) · `field_4` Centro de Resultado (nome) · `field_5` U-number.

### MapeamentoSetor (46) — qual tela/setor cada computador abre
- `Title` · `TelaSetor` · `AcessoRestrito` (sim/não) · `EmailComputador` · `Area` · `Celula`.

### Imagens Fitas (53, site DelineamentoHM) — biblioteca de imagens
- `FileLeafRef` (nome do arquivo) · `Title` · `_ExtendedDescription`.

## G. Tabelas Excel (Excel Online e importada)
Tabelas de engenharia (delineamento) que o app lê por Excel Online. O Uiu não as acessa pelas ferramentas de lista: para dúvida de especificação, cite a tabela e peça o dado ao William. Colunas abaixo = as que o app lê (tiradas das telas); a planilha pode ter mais.

- **DM_MANDREL** — set-up do mandril por PN do mandril (não pela mangueira). Chave `_1MANDREL_PN`. Lê `_37WELD_MACHINE`, `_34REEL_QTT`, `_5MATERIAL`, `_CARRETEL_`. Telas: Mandril, Extrusora de mandril.
- **DM_TUBE_EXTRUSION** — parâmetros e faixas da extrusora de tubo (tela Tubo).
- **DM_FIOS** — fios e bitola do fio. Chave `PARTNUMBER` (código do fio); lê `WGAGE_in`. Telas: Bobinadeira, Trançagem.
- **DM_WIREWINDING** — códigos de fio por bobina; a Bobinadeira avisa "fora do DM_WIREWINDING" quando o código lido não existe.
- **DM_LIST_BOBINAGEM** — PNs ligados à bobinagem. Chave `Part_Number`.
- **DM_TRANÇAGEM** — delineamento (construção) de cada mangueira na trançagem. Liga a mangueira à construção por `_2BRD_CODE` ↔ `_1CONSTRUCAO` (normalizados).
- **DM_ENGRENAGENS** — velocidade teórica da trançagem em m/h por máquina e construção: `_13TEORICA_M_H` (texto com vírgula; "-" na Spiral), `_4MAQUINA`, `_1CONSTRUCAO`, `_15OBSERVACAO` (marca "DUAS PASS" = mangueira de duas passadas). Spiral aparece como TE01. É a base da Meta Hora da trançagem.
- **DESVIO** (`DM_ENGRENAGENS_DESVIO`) — desvio aprovado e temporário de velocidade por máquina + construção: `Inicio`, `Fim`, `Desvio` (1 = ativo). Com desvio ativo, a velocidade oficial é a do desvio (MEL-256).
- **DM_EXTRUSAO_COBERTURA** — velocidade da extrusão da cobertura `SPEEDY_mpm` (m/min; o app multiplica por 60 para m/h). Base da meta da Cobertura.
- **DM_BANDAGEM** — especificação da bandagem por mangueira (chave `PARTNUMBER`): `Código fita match-mate`, `Código film bruiser`, `Tensão bandagem`, `LARGURA DA FITA DE BAND.`, `Numero do guia da fita`, `Velocidade bandagem`, `Número do bico guia`, `Nº cone de borracha`, `Tensão fita matchmate`, `Tensão fita alto-relevo`, `PN_BANDAGEM`, `Passo`, `INKJET`, `Tensao_Bruiser`.
- **DM_LAYLINE** — layline por mangueira (chave `PARTNUMBER`): `EMB_DESC` (alto-relevo), `INKJ_DESC` (tinta jet), `TensaodeDebandagem`. Telas: Bandagem, Debandagem.
- **DM_TESTE_INSP** — especificação de teste e inspeção (tela Finalização/Extração).
- **DM_EXTRA_TESTE_INSP** — especificação extra de teste (só na Ficha Técnica).
- **Tempos** (importada de Excel, fica dentro do app) — tempo de montagem por PN: `Material` (= PN, maiúsculo), `TempoMinPc`, `TempoParadoMin`. Base da meta do Hora-Hora da Montagem. Há troca planejada para a lista `Tempos_Montagem`, ainda não publicada.
- A tela Ficha Técnica mostra todas as DM_ de uma mangueira juntas.

## Log_Uiu (a criar na F3)
Uma linha por correção feita pelo Uiu: quem, quando, lista, item (ID), campo, antes, depois, receita do Manual_BO.

## Ligações
- A OP liga tudo: ficha `OP` = MB51 `Order` = RegistrosInspeção/TiposErros `OP_ID` = Plano_OPs `Title` = Conferencia_SAP `OP` = ControleExtrusora `field_2`.
- Ficha ↔ eventos: ficha `ID` = Eventos_Producao `origem_ID` (com `origem` = ficha_producao). Ficha ↔ pallets: `FichaID`. Ficha ↔ bobinas: FifoBobinadeira `FichaID_Consumo`.
- SAP (MB51, COOIS) e BD Packing List chegam como export: ver 07_Dados_SAP_x_GMS.md.
