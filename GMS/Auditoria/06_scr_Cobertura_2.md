# Auditoria GMS — 06 · `scr_Cobertura_2` (v0.3.0 → v0.3.1)

Lida por inteiro (2.888 linhas, 153 controles). QA do projeto idêntico ao baseline. Nenhum controle existente mudou de X/Y/Width/Height;
5 controles novos, 1 trocado.

## Aplicado
| # | Onde | Problema → correção |
|---|---|---|
| 1 | **Salvar Parcial** | Sem trava de metragem: com o campo em branco o `_delta` virava negativo (0 − o que já estava salvo) e **subtraía** metragem de `Qtd_Turno1/2/3`. Agora exige `fx_MetragemOk` (como a Bandagem) |
| 2 | **Iniciar** | A **sobra do carretel era zerada antes** de a ficha gravar: se a gravação falhasse, a sobra (metros reais) ficava perdida. Agora só é consumida depois que a ficha gravou |
| 3 | **Iniciar / Enviar** | Falha ao reservar ou liberar o carretel (`lista_carreteis`) era silenciosa: o carretel podia ficar preso à OP. Agora avisa ("NÃO foi liberado/reservado, confira em Carretéis") |
| 4 | **Diâmetro** | O rótulo dizia **"(mm)"**, mas os dados são polegada (0,485; 1,105). Rótulo e acessibilidade corrigidos; leitura por `fx_DiametroPol` (aceita vírgula, ponto e milésimo "485" → 0,485). Antes `Value()`: em tela pt-BR "0.48" virava 48 |
| 5 | **Delineamento** | Diâmetro fora de `MIN_OD`–`MAX_OD` do Delineamento (DM_EXTRUSAO_COBERTURA): borda âmbar + aviso (não bloqueia) |
| 6 | **Margem** | Metragem produzida acima da margem sobre a recebida da Trançagem (10%): aviso no mesmo rótulo (`lbl_AlertaSpecCob`, uma linha só para os dois avisos) |
| 7 | **Validade** | O aviso de composto vencido comparava a data com `ctxAgora` (data às 00:00 < agora): composto válido **até hoje** aparecia como vencido. Agora compara com a data de hoje |
| 8 | **Metragem** | Leitura por `fx_Num` (12 pontos) e `fx_MetragemOk`; início bloqueado se a Trançagem não mandou metragem |
| 9 | **Fila** | `tmr_AutoRefreshCob`: atualiza a cada 120 s, só com o operador parado |
| 10 | **Editar OP** | Mangueira vira lista com "OUTRA (amostra ou nova)" |
| 11 | **Padrão** | Um instante só (`fx_TurnoEm`/`fx_DataRefEm`, 11 pontos); `Trim` em composto e lote; `fx_MetrosUn` ("—" em vez de "0 m"); fontes e chip por token; cargas do `OnVisible` em `Concurrent` |

## Não aplicado — precisa do delineamento ou de decisão
1. **Composto × Delineamento (`COVER_PN`).** O `Cod.Cobertura` da ficha tem 51 grafias: `500-01` (694), `500.01` (485), `12101878` (397), `500-03` / `500.03`,
   `988-50`, `98746` / `987-46`, `H029`, e **`0` em 53 fichas**. É o mesmo composto em mais de um código (talvez material SAP × código da fábrica). Comparar com
   `COVER_PN` agora geraria alarme falso. Fica para amanhã, com o delineamento: normalizar (tirar `-` `.` e espaço) e decidir se bloqueia ou avisa.
2. **Diâmetro opcional** (4,6% das OPs sem diâmetro nos últimos meses). Tornar obrigatório? Decisão do William.
3. **Validade do composto opcional** (2,7% em branco nos últimos 60 dias); o aviso de vencido já existe.
4. Espessura e concentricidade existem no Delineamento da Cobertura, mas a tela **não digita** esses valores (só o Ø).
5. `lista_carreteis` é lida inteira a cada abertura e a cada refresh (e agora a cada 2 min): confirmar o número de linhas.
6. Ícones Classic e "MENU LATERAL": mesma observação das outras telas.
