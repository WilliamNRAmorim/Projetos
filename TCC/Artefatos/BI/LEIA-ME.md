# GMS_Painel_TCC: cópia fictícia do Power BI do GMS (artefato do TCC)

Projeto Power BI (formato PBIP) com a marca do GMS e dados inteiramente inventados: nenhuma OP, mangueira, operador ou número é da operação, e não há fonte externa. Serve para você abrir no Power BI Desktop e fazer "Salvar como" `.pbix`.

## O que tem na pasta

| Item | O que é |
|---|---|
| `GMS_Painel_TCC.pbip` | Arquivo que você abre no Desktop. Liga o relatório ao modelo local. |
| `GMS_Painel_TCC.Report/` | As 14 páginas do painel (4 ocultas, ver abaixo), logo do GMS no lugar da antiga. |
| `GMS_Painel_TCC.SemanticModel/` | Modelo semântico: tabelas, relações e medidas do GMS. As tabelas que vinham de listas do SharePoint (17, contando `fHoraHora` e `RefugoExtrusora_Mandril`) agora trazem os dados fictícios embutidos no próprio M (`#table`). |
| `gerar_fakedata.py` | Gera os dados fictícios e reescreve o M das tabelas. Semente fixa; pode rodar de novo. |
| `ESQUEMA_MODELO.md` | Tabela → colunas das 21 tabelas reais (referência). |

## Como abrir e atualizar

1. No Power BI Desktop: Arquivo → Abrir → Procurar → `GMS_Painel_TCC.pbip`. Se ele pedir para habilitar o recurso de visualização "Formato de projeto do Power BI (PBIP)" e "Formato de relatório do Power BI (PBIR)", habilite em Opções e reabra.
2. Clique em Atualizar (Home → Atualizar). Não pede credencial nem arquivo: os dados estão dentro do modelo. As tabelas calculadas (calendário, Etapas, Fluxo e outras) são recalculadas por cima.
3. Se aparecer aviso de "privacidade de dados" ou "fonte desconhecida", é falso alarme; não há fonte.
4. Confira as páginas visíveis (lista abaixo).
5. Arquivo → Salvar como → `GMS_Painel_TCC.pbix`.

## Páginas

Visíveis (10): Visão Geral, Refugo PPM, Refugo PPM · Cortes, Hora-Hora Trançagem, Paradas, Produção Mont., Paradas Mont., Extrusora, Fluxo · Etapas, Fluxo · Mão de obra.

Ocultas (4, o TCC não cita): Produção x meta (SAP) `pg_mascara_sap`, OEE2 Trançagem `pg_oee2`, Plano de mangueira x SAP `pg_plano_mangueira`, Detalhe por mangueira `pg_plano_mangueira_detalhe`. Para ver, clique com o botão direito na aba da página e desmarque "Ocultar página".

Logo: `GMS-Logo.png` (variante para fundo ESCURO, texto branco), porque o logo fica sobre a faixa preta `#1E1E1E` do cabeçalho de todas as páginas.

## O que o modelo tem a mais que o instantâneo de 03/11

Para as páginas do TCC renderizarem, foram trazidas do modelo vivo (definições em `GMS/PowerBI/modelo/*.tmdl.md`) cinco tabelas, todas sem rede:

- `dTurno` (calculada, "1º/2º/3º Turno"), com a coluna calculada `Turno BI` em `Producao_Montagem` e `Paradas_Montagem` e relações para elas e para `fHoraCheia`.
- `fHoraCheia` (calculada, Hora-Hora em hora cheia) sobre `fHoraHora`, com relações para `dCalendario` (Data BI) e `dTurno` (Turno BI).
- `fFluxoBase` (calculada, 8 etapas) sobre `ficha_producao`; oculta, sem relações.
- `fHoraHora` (dados fictícios embutidos): trançadeiras TR01 a TR04, 21/09 a 30/10, 24 janelas por dia produtivo; relação com `dCalendario`. A tabela `Hora-Hora` (só linhas com motivo) é derivada dela.
- `RefugoExtrusora_Mandril` (dados fictícios embutidos, refugo em kg), sem relação (as medidas usam a data virtual `INT(DataHoraRefugo)`, como no modelo vivo). Em `ControleExtrusora_estrutura` entraram as medidas `Extrusoes Mandril`, `Dias com Extrusao`, `Metros por Dia Extrusora` e `Refugo kg por 1000 m`, e `Refugo Extrusora Mandril` passou a ler essa tabela.

Atenção: as tabelas calculadas só ganham valor depois do primeiro Atualizar.

## Limitações conhecidas

- Nas 10 páginas visíveis, nenhum visual aponta para tabela, coluna ou medida ausente (conferido por script). Quem confirma o desenho é o Desktop.
- As 83 medidas do relatório ficam em `GMS_Painel_TCC.Report/definition/reportExtensions.json` (eram medidas de relatório sobre o modelo publicado). Se o Desktop recusar abrir o projeto por causa desse arquivo, feche, apague `reportExtensions.json` e abra de novo; as medidas somem e muitos visuais ficam em erro.
- Só nas 4 páginas ocultas há dependências ausentes: `dProdutoSAP`, `dClasseMangueira`, `dPlanoDiario`, `fProducaoSAP`, `dEtapaOEE` e colunas de `dMotivoParada` (Família, Categoria). Por isso elas continuam ocultas.
- Medidas antigas do modelo (não usadas nas páginas visíveis) ainda citam `Hora-Hora[Mangueira]`, `[Meta Hora]`, `[Real.Hora]` e a tabela `Refugo_Bobinadeira`, que não existem; podem aparecer como erro na lista de campos.
- Os números fictícios não reproduzem os valores reais (por exemplo, o 1.295/1.440 do cartão da meta depende de dados que o fictício não tem).

## Validação feita

- Todos os JSON e TMDL editados passam no parse; as 15 tabelas com `#table` embutido foram conferidas (delimitadores balanceados, número de campos por linha igual ao de colunas, sem fonte externa). O refresh em si só o Desktop confirma.
- Nenhuma credencial, URL do SharePoint ou cache de dados reais: o `cache.abf`, as configurações locais e os metadados de Perguntas e Respostas (que citavam dados reais) foram removidos.
