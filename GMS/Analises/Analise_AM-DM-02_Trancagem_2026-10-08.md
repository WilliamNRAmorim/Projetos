# AM-DM-02 Controle de Trançagem: análise (08/10/2026)

Arquivo: `Engenharia/Trancagem/AM-DM-02 - CONTROLE DE TRANÇAGEM.xlsm` (REV. 5, 31/10/2023; responsável: Ricardo Almeida).
Comparado com `Engenharia/DM_DATABASE/DM_TRANÇAGEM.xlsx` e com `Telas/scr_Trancagem_3.txt`. Nada foi alterado no app.

## 1. O que a planilha é
Folha de controle estatístico de diâmetro, uma aba por trançadeira (16 abas visíveis: TH01, TH02, TH03, TH04, TH06 e TM01/TM02 com 1ª e 2ª trança, mais TH05, TM04 e TO04). Três abas ocultas: `Dados Mang`, `Listas` e `Planilha1`.

Cada aba tem:
- **Cabeçalho:** código do produto (H5), data (`=TODAY()`), máquina, trança (1ª/2ª).
- **Especificação:** ∅ ext LIE / média / LSE (I7, K7, M7) e picks LIE/LSE (I9, M9), digitados à mão ("consultar o delineamento").
- **Medição de 2 em 2 horas** (00h a 22h, 12 colunas): 5 amostras de diâmetro por horário, com soma, média (X̄) e amplitude (R) calculados. Dois gráficos (X̄ com LIE/média/LSE e R).
- **Tensão nas bonecas:** 5 linhas com tensão, nº de fios e ∅ ext do tubo (P12:R16).
- **Fios sobrepostos em 150 mm** (linha 20), **picks medidos** (5 valores, linha 62), **picks real** (G59) e **observações**.

A macro `Lançamento` (botão) confirma, abre `Banco de dados diametros.xlsx` no SharePoint da Operações, grava as medidas nas abas `porHora` e `porSetUp`, limpa a folha e salva. Exige mangueira preenchida (H5).

## 2. Comparação com o delineamento (`DM_TRANÇAGEM`)
- **`Dados Mang` (58 mangueiras) × DM_TRANÇAGEM:** os 6 diâmetros (1ª e 2ª trama, mín/méd/máx) batem em **58 de 58**. Nenhuma divergência.
- **34 PNs do DM não estão em `Dados Mang`** (EC115-*, EC118-04L…16L, EC215-*, EC415-*, H28004…H28008, FC849-08, GH493-10, 2583-12 etc.). Se a folha só consulta a lista oculta, esses PNs saem sem limites.
- **Valores digitados nas abas conferidos contra o DM:**
  - TH02 (GH781-8), 1ª e 2ª trança: diâmetros e picks 39–41 batem.
  - TM04 (EC118-08LRL): diâmetros e picks 40–42 batem.
  - **TO04 (GH781-16): erro de unidade e de trama.** Está digitado 1300 / 1315 / 1330 (milésimos) e picks 31–33; o DM tem 1,300 / 1,315 / 1,330 pol, mas na **2ª trama**. A 1ª trama do GH781-16 é 1,225 / 1,240 / 1,255. A aba TO04 não distingue 1ª e 2ª trança, então a folha usa só a trama final.
- Confirma o que o GMS já faz: a `scr_Trancagem_3` busca a faixa de picks e diâmetro direto do DM (1ª e 2ª trama) e avisa se estiver fora.

## 3. O que o GMS já cobre e o que falta
| Item da planilha | GMS hoje |
|---|---|
| Limites de diâmetro e picks do delineamento | Sim, automático (sem digitar) |
| 1ª e 2ª trama (LI, fio, picks) | Sim (MEL-205, MEL-214) |
| Picks e diâmetro do lote | Sim (grava `N°Picks` e `Diametro_Trançagem` por OP) |
| **5 amostras de diâmetro por horário (2 em 2 h)** | **Não** |
| **X̄ e R, gráficos de controle, ponto fora de LIE/LSE** | **Não** |
| **Tensão nas bonecas** (tensão, nº de fios, ∅ tubo) | **Não** |
| **Fios sobrepostos em 150 mm** | **Não** |
| Observações gerais da folha | Parcial (observação por OP) |
| Registro histórico | Em Excel (`Banco de dados diametros.xlsx`), fora do SharePoint List |

A amostragem horária é o único bloco sem equivalente. Ela rodaria bem dentro do Hora-Hora da Trançagem (`scr_HoraHora_Trancagem_2`), que já tem a cadência de horário e a seleção de máquina.

## 4. Proposta (MEL-241, não implementada)
- **Lista SharePoint `Controle_Trancagem`:** Data, Máquina, Mangueira, Trama (1ª/2ª), Horário, Amostra1..5, LIE/Média/LSE (copiados do DM no ato), X̄, R, Fios sobrepostos, Observação, Operador, FichaID/OP.
- **Lista `Controle_Trancagem_Bonecas`** (ou colunas na mesma): tensão, nº de fios e ∅ tubo por boneca.
- **Painel na Hora-Hora da Trançagem:** operador digita 5 medidas no horário; app calcula X̄/R, pinta fora do LIE/LSE e mostra o gráfico do turno. Nada de macro, nada de Excel (norma P6: sem fonte Excel nova).
- **Ganho imediato:** elimina erros como o do TO04 (limites vêm do DM, não digitados) e junta o histórico no SharePoint.

## 5. Decisões necessárias do William
1. **Qualidade aceita a folha digital como registro válido do AM-DM-02?** (É a pendência C5 de 27/08, ainda aberta; a REV. 5 é de 2023.)
2. A amostragem de 2 em 2 h continua, ou muda (a cada hora, por troca de bobina)?
3. Tensão nas bonecas e fios sobrepostos entram no app agora ou só o diâmetro/picks?
4. O que fazer com os 34 PNs que não estão em `Dados Mang` (usar o DM diretamente resolve)?
5. Corrigir a aba TO04 da planilha (unidade e trama) enquanto o app não substitui a folha.
