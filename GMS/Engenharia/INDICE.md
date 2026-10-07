# Engenharia: bases DM_ (Delineamento Hose Manufacturing)

Fonte: site SharePoint `Delineamento Hose Manufacturing` (`https://danfoss.sharepoint.com/sites/DelineamentoHM`),
biblioteca `DM_DATABASE` e listas `DM_MANDREL` e `AdminConsole`. Cópia de 08/10/2026; a fonte oficial é o SharePoint da Engenharia.

| Arquivo | Aba | Linhas × colunas | Cabeçalho (primeiras colunas) |
|---|---|---|---|
| DM_BANDAGEM.xlsx | Sheet1 | 89 × 25 | ID · PARTNUMBER · PN_BANDAGEM · LARGURA DA FITA DE BAND. · EMBOSSED · INKJET · Código fita match-mate · Código film bruiser |
| DM_COVER _EXTRUSION_REV.xlsx | Sheet1 | 67 × 38 | ID · Identificador · PARTNUMBER · COVER_PN · LUBE_PROT · MIN_OD · MED_OD · MAX_OD |
| DM_ENGRENAGENS.xlsx | Sheet1 | 68 × 17 | _1CONSTRUCAO · _2BRD_CODE · _3BITOLA · _4MAQUINA · _5RPM_MAX · _6CARRIERS · _7PUXADOR · _8DECK1 |
| DM_ESTRUTURA.xlsx | Sheet1 | 204 × 12 | ID · COMPOSTO · REV · TIPO · MATERIAL · DESCRIÇÃO · CAS_No · FORNECEDOR |
| DM_EXTRA_TESTE_INSP.xlsx | Sheet1 | 89 × 16 | ID · PARTNUMBER · MIN_BURST_PRESSURE_psi · TEST_PRESSURE_psi · TEST_PRESSURE_bar · SAFETY_PRODUCT · AUW_TEST · COMP_LANCE_50m |
| DM_EXTRUSAO_COBERTURA.xlsx | Sheet1 | 94 × 37 | ID · PARTNUMBER · COVER_PN · LUBE_PROT · MIN_OD · MED_OD · MAX_OD · EXT_PIN |
| DM_FIOS.xlsx | Sheet1 | 10 × 38 | ID · PARTNUMBER · REVISÃO · TIPO · WGAGE_in · TENSÃO_lbf · TALONG_lb_100ft · DATE |
| DM_INTRODUCTION.xlsx | Sheet1 | 92 × 12 | PARTNUMBER · CONST_PARTNUMBER · TYPE · DATE · REVISION · ENGR · STANDARDS · TEST_REQUEST |
| DM_LAYLINE.xlsx | Sheet1 | 104 × 12 | DM_LAYLINE · PARTNUMBER · NORMAS · EMB_DESC · EMB_MATERIAL · EMB_REP_LENG_in · EMB_LET_HT_in · EMB_MSHA_HT_in |
| DM_LISTA_ID.xlsx | Sheet1 | 48 × 6 | Nome · U_Number · E_Number · ID_Crachá · __PowerAppsId__ |
| DM_LIST_BOBINAGEM.xlsx | Sheet1 | 125 × 4 | ID · Part_Number · Bobbin_Code · __PowerAppsId__ |
| DM_MANDREL.xlsx | Sheet1 | 14 × 52 | ID · _1MANDREL_PN · _34REEL_QTT · _2MIN_OD_in · _3NOM_OD_in · _4MAX_OD_in · _5MATERIAL · _6MAT_SUP |
| DM_MANDREL.xlsx | Planilha1 | 10 × 4 | _1MANDREL_PN · _2MIN_OD_in · _3NOM_OD_in · _4MAX_OD_in |
| DM_PRPR_FISICAS.xlsx | Sheet1 | 16 × 39 | ID · _1COMPOSTO · _2DATA · _3REVISÃO · _4FORNECEDOR · _5RESP_SUPPLIER · _6RESP_EATON · _7DESCRIÇÃO_DO_COMPOSTO |
| DM_TESTE_INSP.xlsx | Sheet1 | 71 × 16 | ID · PARTNUMBER · MIN_BURST_PRESSURE_psi · TEST_PRESSURE_psi · TEST_PRESSURE_bar · SAFETY_PRODUCT · AUW_TEST · COMP_LANCE_50m |
| DM_TRANÇAGEM.xlsx | Sheet1 | 93 × 54 | ID · PARTNUMBER · _1BRD_PRINC · _2BRD_CODE · _3BRD_DESCRIPTION · _4BOBBIN_CODE · _5_CARRIERS · _6ENG_MAYER_1ST |
| DM_TUBE_EXTRUSION.xlsx | Sheet1 | 90 × 38 | PARTNUMBER · MANDREL · TUBE_PN · REEL_QTT · LUBE_PROT · MIN_OD · MED_OD · MAX_OD |
| DM_WIREWINDING.xlsx | Sheet1 | 60 × 13 | ID · PARTNUMBER · HOSE · WIRE_YARN_PN · WIRES_YARN · BRAID · RB_TOOL_in · LB_TOOL_in |

Listas do site (CSV em `listas/`): `DM_MANDREL` (13 itens) e `AdminConsole` (7 itens).

Não copiados (não são DM_ e são grandes): `Hose_Assembly_Database.xlsx` (9 MB), `Banco_de_Datos.xlsx` (1,2 MB), `Conexoes.xlsx`, `Dados_Prensagem.xlsx`, `PressaoeProjetil.xlsx`.

Atenção: `DM_LISTA_ID.xlsx` tem nome, U-Number, E-Number e ID de crachá de funcionários. O repositório é privado; não torná-lo público nem copiar esse arquivo para fora sem tratar os dados.
