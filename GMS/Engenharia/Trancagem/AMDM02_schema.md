# AM-DM-02 · Controle de Trançagem: listas SharePoint (MEL-114)

Tela: `GMS/Telas/scr_AMDM02_Trancagem_1.txt` (v0.1.0). Fórmulas novas: `Telas/Formulas.txt` §17 (v3.0.12).
Coleta digital em paralelo ao papel. Diâmetro sempre em **polegada**, como no formulário.
Criar as 3 listas à mão, com os **nomes internos exatos** abaixo (sem acento, sem espaço). Os nomes das listas no app são `AMDM02_Folha`, `AMDM02_Janela` e `AMDM02_Spec`.

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

O app só **lê** esta lista (carrega em `colSpecAM` ao abrir a tela). Manutenção: atualizar quando a Engenharia mudar o DM_TRANÇAGEM (regerar o CSV pelo mesmo cruzamento e reimportar).

## 2. AMDM02_Folha (uma por Data + Máquina + Trança)

| Coluna (nome interno) | Tipo | Quem grava |
|---|---|---|
| Title | Texto (padrão) | App, na abertura. Chave `yyyy-mm-dd|Maquina|Tranca` (ex.: `2026-10-20|TH02|1`). **Impor valores exclusivos: Sim.** Indexada |
| Data | Data (só data) | App, na abertura. Indexada |
| Maquina | Texto | App, na abertura. Indexada. TH01…TO04 (11 máquinas) |
| Tranca | Número, 0 casas | App, na abertura. 1 ou 2 (máquina de trança única = 1) |
| PN | Texto | App, na abertura (código de produto) |
| BRDCode | Texto | App, na abertura |
| Caracteristica | Texto | App, na abertura ("Diâmetro") |
| Responsavel | Texto | App, na abertura e em cada Salvar (nome da lista `Colaboradores`) |
| ODLie, ODNom, ODLse | Número, 3 casas | App, na abertura: spec copiada da AMDM02_Spec (OD1 ou OD2, conforme a trança). Não muda depois |
| PickLie, PickLse | Número, 1 casa | App, na abertura (vem da AMDM02_Spec; se vier vazio, o operador digita) |
| Tensao1 … Tensao5 | Número, 2 casas | App, em cada Salvar (tabela lateral, tensão nas bonecas) |
| Fios1 … Fios5 | Número, 0 casas | App, em cada Salvar (nº de fios) |
| ODTubo1 … ODTubo5 | Número, 3 casas | App, em cada Salvar (∅ ext. do tubo, polegada) |
| FiosSobrepostos | Número, 0 casas | App, em cada Salvar (fios sobrepostos em 150 mm) |
| NPicks | Número, 1 casa | App, em cada Salvar (nº de picks medido) |
| ODTranca1 … ODTranca5 | Número, 3 casas | App, em cada Salvar (5 medidas de ∅ ext. da trança, polegada) |
| Observacoes | Várias linhas de texto (texto simples) | App, em cada Salvar |

Criado em / Criado por (colunas do sistema) registram quem abriu a folha. Índices: Title, Data, Maquina.

## 3. AMDM02_Janela (uma por folha + janela de 2 h, criada no 1º Salvar com amostra)

| Coluna (nome interno) | Tipo | Quem grava |
|---|---|---|
| Title | Texto (padrão) | App. Chave `IdFolha|Janela` (ex.: `57|3`). **Impor valores exclusivos: Sim** |
| IdFolha | Número, 0 casas | App. ID do item da AMDM02_Folha. **Indexada** |
| Janela | Número, 0 casas | App. 0 a 11 (0 = 00:00, 1 = 02:00 … 11 = 22:00). **Indexada** |
| Turno | Número, 0 casas | App. 1, 2 ou 3 = `fx_Turno` aplicado ao minuto de INÍCIO da janela (00:00, 02:00 e 04:00 = 3º; 06:00 a 12:00 = 1º; 14:00 a 22:00 = 2º). Nenhuma regra nova |
| Amostra1 … Amostra5 | Número, 3 casas | App. ∅ ext. em polegada; vazio = não medida |
| Soma | Número, 3 casas | App. Soma das amostras preenchidas |
| Media | Número, 4 casas | App. X̄ = Soma ÷ nº de amostras preenchidas |
| Amplitude | Número, 3 casas | App. R = máximo − mínimo das amostras preenchidas |
| LancadoPor | Texto | App. Responsável escolhido na tela (cai para o usuário do app) |
| LancadoEm | Data e hora | App. Carimbo do último Salvar da janela |

Fora de LIE/LSE não é gravado: é calculado na tela e no BI a partir de Amostra/Media e das colunas ODLie/ODLse da folha.

## Conferência de cálculo

Aba "TH02 (1ª Trança)" da planilha, janelas 06:00, 08:00, 10:00 e 12:00 (colunas F, G, H, I): Soma 3,372 / 3,372 / 3,375 / 3,370; X̄ 0,6744 / 0,6744 / 0,6750 / 0,6740; R 0,006 nas quatro. É a mesma conta de `fx_AMDM02_Soma`, `fx_AMDM02_Media` e `fx_AMDM02_Amp`.

## Pendências de dados

- TM02 não consta no cadastro `fx_LayoutBalizas` nem em `fx_CelulasTrancagem` (a TH07 e a Spiral constam, mas não têm folha no AM-DM-02). A lista das 16 folhas está em `fx_AMDM02_Folhas`, copiada do formulário.
- Na planilha, a aba TO04 (GH781-16) tem a spec digitada como 1300 / 1315 / 1330 (o ∅ da 2ª trança ×1000, não o da 1ª). A tela usa a 1ª trança (1,225 / 1,240 / 1,255) para máquina de trança única. William confirma qual vale na TO04.
- Pick da Spiral (GH493-6/-8/-12/-16) não existe no DM_TRANÇAGEM: o operador digita ao abrir a folha.
