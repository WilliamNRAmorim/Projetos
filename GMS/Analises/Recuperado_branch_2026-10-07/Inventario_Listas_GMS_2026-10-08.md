# Inventário de listas e fontes de dados do GMS (08/10/2026)

Fonte: `References/DataSources.json` do `.msapp` de 01/10/2026 (40 fontes) cruzado com o uso real em `Telas/*.txt`.
"Escrita" = quantas chamadas de `Patch/Collect/Remove/UpdateIf` apontam para a fonte. Fontes criadas depois de 01/10 não estão neste levantamento (Packing_Manual, Packing_Pallets e Avisos_GMS ainda não existem no app).

## Resumo
| Grupo | Fontes |
|---|---|
| Listas SharePoint reais (conectadas) | 27 (13 delas são `DM_*`, 3 em Excel) |
| Exemplos de template (lixo) | 5 (`ComboBoxSample`, `RadioSample`, `DropDownSample`, `ListboxSample`, `CustomGallerySample`) |
| Estática | 1 (`Tempos`) |
| Sem nenhuma referência nas telas | 1 (`Baixa de Composto`) |

## Uso real (fontes de escrita e núcleo da operação)
| Fonte | Refs | Telas | Escrita | Observação |
|---|---|---|---|---|
| `ficha_producao` | 260 | 18 | 34 | Núcleo. Lida 7 vezes na abertura (MEL-014). |
| `lista_carreteis` | 107 | 6 | 18 | Família carretel (ver abaixo). |
| `Eventos_Producao` | 86 | 12 | 19 | Log de eventos. |
| `Historico_Carretel` | 64 | 7 | 14 | Família carretel. |
| `CarreteisMandril` | 49 | 3 | 9 | Família carretel. |
| `FifoBobinadeira` | 48 | 4 | 5 | |
| `Hora-Hora` | 33 | 6 | 5 | Célula, Data, Turno, Hora, Mangueira, Minutos, Meta, Real, Motivo. |
| `ControleExtrusora_estrutura` | 26 | 2 | 5 | Extrusora. |
| `Producao_Montagem` / `Paradas_Montagem` | 25 / 25 | 3 | 2 / 2 | Montagem. |
| `RegistrosInspeção` / `TiposErros` | 23 / 17 | 2 | 2 / 2 | Inspeção. |
| `Controle_Catenaria` | 13 | 1 | 2 | Medição de diâmetro e tensão. |
| `Hora_Hora_Mandril` / `Hora_Hora_Tubo` | 7 / 7 | 1 / 1 | 2 / 2 | Só as telas antigas (`scrHoraHora_Mandril/Tubo`). |
| `Refugo_Bobinadeira` | 7 | 1 | 1 | |
| `RefugoExtrusora_estrutura` | 4 | 1 | 1 | |
| `Estado_Trancadeiras` | 3 | 1 | 0 | Só lida; gravada por fluxo (MEL-231). |
| `Colaboradores`, `MapeamentoSetor`, `Imagens Fitas` | 17 / 5 / 2 | | 0 | Cadastros só de leitura. |
| `DM_*` (13) | 1 a 14 cada | | 0 | Só leitura. Estão em Excel/arquivo (Frente 2 quer consolidar). |

## Candidatas a mesclar ou remover
| # | Candidata | Motivo | Ação sugerida | Risco |
|---|---|---|---|---|
| 1 | `Hora_Hora_Mandril` + `Hora_Hora_Tubo` → `Hora-Hora` | Mesmo formato (Data, Hora, Turno, Motivo, Status). A `Hora-Hora` já distingue por `Célula`. Só são usadas pelas telas antigas, que a MEL-224 manda refazer no padrão da Trançagem. | Migrar quando a MEL-224 refizer as telas; depois apagar as duas listas. | Médio: migração de histórico. |
| 2 | `Refugo_Bobinadeira` + `RefugoExtrusora_estrutura` → uma lista `Refugo` com coluna `Processo` | Mesmos campos (DataHoraRefugo, Quantidade, Turno, Observacao, motivo, operador). Hoje cada máquina tem a sua. | Unir, com `Processo` = Bobinadeira ou Extrusora. | Médio. |
| 3 | Família carretel: `lista_carreteis`, `CarreteisMandril`, `Historico_Carretel` | Três listas para o mesmo objeto (carretel), 220 refs e 41 gravações. Verificar se `CarreteisMandril` (carretel de mandril) cabe em `lista_carreteis` com `Tipo`. Pendência MEL-142 já pergunta isso. | Decidir com o William; só então planejar a migração. | Alto: é o núcleo do fluxo de carretéis. |
| 4 | `Producao_Montagem` + `Paradas_Montagem` | Mesma célula e turno, mas produção e parada têm formatos diferentes. A `Hora-Hora` já tem `Motivo` (parada). | Manter separadas por enquanto (formato diferente). | Baixo se mantidas. |
| 5 | `Controle_Catenaria` | Medição de diâmetro e tensão por máquina. Os números estão em texto (`DiamAtualMM`) e 1 amostra por registro. Tem forma de uma `Controle_Medicao`. | Migrar para `Controle_Medicao` (nova lista, ver abaixo) quando a catenária for tocada; não mexer agora. | Baixo. |
| 6 | `Estado_Trancadeiras` | Escrita por fluxo Power Automate; a tela só lê. A MEL-231 quer o cálculo dentro do app. | Remover junto com o fluxo (MEL-231). | Médio. |
| 7 | `Baixa de Composto` | Nenhuma referência nas telas. | Remover do app (Studio > Dados). | Baixo. |
| 8 | 5 `*Sample` + `Tempos` | Lixo de template (norma 2.1 do Mestre já pede remover). | Remover do app. | Nenhum. |
| 9 | `DM_*` (13 fontes) | Excel como fonte viva é proibido pela norma 2.2; todos somente leitura. | Frente 2: consolidar em lista/Dataverse. Não pertence a este ciclo. | Alto (13 telas). |

Ganho imediato sem risco: remover os itens 7 e 8 (7 fontes a menos no app, sem tocar em nenhuma tela).

## Decisão para o AM-DM-02 (norma de banco de dados de 08/10)
- **Dá para mesclar com alguma existente?** Avaliei `Hora-Hora` (janelas de turno diferentes dos horários de 2 em 2 h, coluna de meta/real sem relação) e `Controle_Catenaria` (números em texto, 1 amostra por registro, tela que lista todas as linhas e ficaria poluída). Nenhuma cabe sem quebrar outra tela.
- **Por isso, uma lista nova e genérica**: `Controle_Medicao`, com a coluna `Processo` (Trançagem hoje; Catenária e outros depois). Substitui o Excel `Banco de dados diametros.xlsx` (que não está no app), então o saldo de fontes do app é +1, mas o arquivo Excel solto deixa de existir.
- **Impacto na carga do app:** a lista só é lida na tela de Controle (filtro por Data, Máquina, Mangueira e Trama; no máximo 12 linhas), não no `OnStart`.
- **Volume:** até 10 máquinas × 2 tramas × 12 horários por dia, ou seja, no máximo cerca de 240 linhas por dia (cerca de 88 mil por ano). Precisa de índice em `DataHora` e `Maquina`.
