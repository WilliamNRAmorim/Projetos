# AM-DM-02 · Controle de Trançagem: listas SharePoint (MEL-114)

Tela: `GMS/Telas/scr_AMDM02_Trancagem_1.txt` (v0.2.0). Fórmulas novas: `Telas/Formulas.txt` §17 (v3.0.12). A folha (AMDM02_Folha) tem a spec da ÚLTIMA trança e as janelas/carta X̄-R; o registro de pick, ∅ da trança e foto é POR TRANÇA (1ª ou 2ª) na `AMDM02_Registro` (MEL-114, v0.2.0).
Coleta digital em paralelo ao papel. Diâmetro sempre em **polegada**, como no formulário.
Criar as 4 listas à mão, com os **nomes internos exatos** abaixo (sem acento, sem espaço). Os nomes das listas no app são `AMDM02_Folha`, `AMDM02_Janela`, `AMDM02_Spec` e `AMDM02_Registro`.

## 1. AMDM02_Spec (cadastro de especificação, 58 linhas)

Gerada da aba oculta "Dados Mang" da planilha, com o pick vindo do `DM_TRANÇAGEM.xlsx` (casa por PN + BRD CODE). Arquivo de carga: `AMDM02_Spec.csv` (UTF-8 com BOM, separador `;`, decimal vírgula, 58 linhas).

| Coluna (nome interno) | Tipo | Observação |
|---|---|---|
| Title | Texto (padrão) | Chave `PN|BRD_CODE`. **Impor valores exclusivos: Sim.** Indexada |
| PARTNUMBER | Texto | Ex.: GH781-8 |
| BRD_CODE | Texto | Ex.: DD240801. A chave é PN x BRD CODE, nunca só PN |
| OD1_MIN, OD1_MED, OD1_MAX | Número, 3 casas | ∅ ext. da 1ª trança, polegada (LIE, nominal, LSE) |
| OD2_MIN, OD2_MED, OD2_MAX | Número, 3 casas | ∅ ext. da 2ª trança. Vazio quando a mangueira só tem 1 trança (a planilha tem "-") |
| PICK1_MIN, PICK1_MAX | Número, 1 casa | Pick LIE/LSE da 1ª trança (`_15PICKS_1ST_MIN_5` e `_17PICKS_1ST_MAX_5` do DM_TRANÇAGEM). Vazio nos 4 Spiral (GH493-6/-8/-12/-16) |
| PICK2_MIN, PICK2_MAX | Número, 1 casa | Pick da 2ª trança (`_35...` e `_37...`). Vazio quando não há 2ª trança |

Cada linha traz as duas tranças; o app escolhe a da última (OD2_MED > 0 → OD2/PICK2; senão OD1/PICK1). O app só **lê** esta lista (carrega em `colSpecAM` ao abrir a tela). Manutenção: atualizar quando a Engenharia mudar o DM_TRANÇAGEM (regerar o CSV pelo mesmo cruzamento e reimportar).

## 2. AMDM02_Folha (uma por Data + Máquina)

| Coluna (nome interno) | Tipo | Quem grava |
|---|---|---|
| Title | Texto (padrão) | App, na abertura. Chave `yyyy-mm-dd|Maquina` (ex.: `2026-10-20|TH02`). **Impor valores exclusivos: Sim.** Indexada |
| Data | Data (só data) | App, na abertura. Indexada |
| Maquina | Texto | App, na abertura. Indexada. Nome da trançadeira como no cadastro (`fx_LayoutBalizas`, `tranc = true`) |
| PN | Texto | App, na abertura (código de produto) |
| BRDCode | Texto | App, na abertura |
| Caracteristica | Texto | App, na abertura ("Diâmetro") |
| Responsavel | Texto | App, na abertura e em cada Salvar (nome da lista `Colaboradores`) |
| ODLie, ODNom, ODLse | Número, 3 casas | App, na abertura: spec da ÚLTIMA trança copiada da AMDM02_Spec (OD2 se o produto tem 2ª trança, senão OD1). Não muda depois |
| PickLie, PickLse | Número, 1 casa | App, na abertura (vem da AMDM02_Spec; se vier vazio, o operador digita) |
| Tensao1 … Tensao5 | Número, 2 casas | App, em cada Salvar (tabela lateral, tensão nas bonecas) |
| Fios1 … Fios5 | Número, 0 casas | App, em cada Salvar (nº de fios) |
| ODTubo1 … ODTubo5 | Número, 3 casas | App, em cada Salvar (∅ ext. do tubo, polegada) |
| FiosSobrepostos | Número, 0 casas | App, em cada Salvar (fios sobrepostos em 150 mm) |
| NPicks | Número, 1 casa | **OBSOLETA desde v0.2.0** (agora na AMDM02_Registro). Não apagar; sem uso |
| ODTranca1 … ODTranca5 | Número, 3 casas | **OBSOLETAS desde v0.2.0** (agora na AMDM02_Registro). Não apagar; sem uso |
| Observacoes | Várias linhas de texto (texto simples) | App, em cada Salvar |

Criado em / Criado por (colunas do sistema) registram quem abriu a folha. Índices: Title, Data, Maquina.

## 3. AMDM02_Janela (uma por folha + coleta de 5 amostras, na hora real do operador; criada no 1º Salvar com amostra)

| Coluna (nome interno) | Tipo | Quem grava |
|---|---|---|
| Title | Texto (padrão) | App. Chave `IdFolha|Janela` (ex.: `57|3`). **Impor valores exclusivos: Sim** |
| IdFolha | Número, 0 casas | App. ID do item da AMDM02_Folha. **Indexada** |
| Janela | Número, 0 casas | App. **Número de ordem da coleta na folha** (0, 1, 2…, sem limite). Desde a v0.3.0 NÃO é mais a janela fixa de 2 h; linhas antigas (0 a 11) seguem válidas. Não é renumerado depois de gravado. **Indexada** |
| HoraColeta | Data e hora | App. **Hora real da coleta** (`Now()` no momento do lançamento). Se a linha já existe, a hora original é preservada. A carta X̄-R e o prazo de +2 h usam esta coluna. Linha antiga sem HoraColeta cai em 00:00 + Janela × 2 h na tela. **Indexada** |
| Turno | Número, 0 casas | App. 1, 2 ou 3 = `fx_TurnoEm` aplicado à HoraColeta. Nenhuma regra nova |
| Amostra1 … Amostra5 | Número, 3 casas | App. ∅ ext. em polegada; vazio = não medida |
| Soma | Número, 3 casas | App. Soma das amostras preenchidas |
| Media | Número, 4 casas | App. X̄ = Soma ÷ nº de amostras preenchidas |
| Amplitude | Número, 3 casas | App. R = máximo − mínimo das amostras preenchidas |
| LancadoPor | Texto | App. Responsável escolhido na tela (cai para o usuário do app) |
| LancadoEm | Data e hora | App. Carimbo do último Salvar da janela |

O dia da folha (coluna Data de AMDM02_Folha) é o dia produtivo do GMS, de 05:20 a 05:20 (`fx_DataRefEm`); coletas depois da meia-noite e antes das 05:20 pertencem à folha do dia anterior.

Fora de LIE/LSE não é gravado: é calculado na tela e no BI a partir de Amostra/Media e das colunas ODLie/ODLse da folha.

## 4. AMDM02_Registro (uma por folha + trança; seção "3. REGISTROS" do formulário em papel)

Criada à mão (nomes internos exatos). Chave `IdFolha|Tranca` (ex.: `57|2`). Criada no 1º Salvar com algum dado ou foto daquela trança; depois só atualizada (o app lê pelo Title antes de gravar, então não duplica). **Anexos habilitados**: a foto da mangueira com o pickômetro vai como anexo do item.

| Coluna (nome interno) | Tipo | Quem grava |
|---|---|---|
| Title | Texto (padrão) | App. `IdFolha|Tranca`. **Impor valores exclusivos: Sim** |
| IdFolha | Número, 0 casas | App. ID da AMDM02_Folha. **Indexada** |
| Tranca | Número, 0 casas | App. 1 ou 2 |
| PickLie, PickLse | Número, 1 casa | App. Pick especificado da trança (vem da AMDM02_Spec; se vazio, o operador digita) |
| ODLie, ODNom, ODLse | Número, 3 casas | App. ∅ ext. especificado da trança, polegada (OD1_* na 1ª, OD2_* na 2ª) |
| NPicks | Número, 1 casa | App. "Raspadinha": nº de picks medido em 5 pol |
| ODTranca1 … ODTranca5 | Número, 3 casas | App. 5 medidas de ∅ ext. da trança, polegada |
| Operador | Texto | App. Responsável da folha (cmb_RespAM) |
| LancadoEm | Data e hora | App. Carimbo do último Salvar da trança |
| Anexos | (do sistema) | App, pelo controle de anexos do formulário `frm_RegAM`; mostra a última foto na parte de baixo da aba |

A 2ª trança só é habilitada se o PN da folha tiver 2ª trança (`OD2_MED > 0` na AMDM02_Spec, casando por PN + BRD CODE). Fora de LIE/LSE (pick e ∅) é calculado na tela, não gravado.

## Conferência de cálculo

Aba "TH02 (1ª Trança)" da planilha, janelas 06:00, 08:00, 10:00 e 12:00 (colunas F, G, H, I): Soma 3,372 / 3,372 / 3,375 / 3,370; X̄ 0,6744 / 0,6744 / 0,6750 / 0,6740; R 0,006 nas quatro. É a mesma conta de `fx_AMDM02_Soma`, `fx_AMDM02_Media` e `fx_AMDM02_Amp`.

## Pendências de dados

- TM02 não consta no cadastro `fx_LayoutBalizas`: por isso não aparece na lista de máquinas da tela. Se a TM02 precisar de folha, entra primeiro no cadastro (William decide).
- A lista de máquinas da tela é `Filter(fx_LayoutBalizas, tranc)`: inclui TH07 e Spiral, que não tinham folha no formulário em papel.
- Pick da Spiral (GH493-6/-8/-12/-16) não existe no DM_TRANÇAGEM: o operador digita ao abrir a folha.
