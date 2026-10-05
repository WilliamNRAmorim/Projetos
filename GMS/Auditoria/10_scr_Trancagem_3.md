# Auditoria GMS — 10 · `scr_Trancagem_3` (v0.3.1 → v0.4.0)

Lida por inteiro (4.770 linhas, 220 controles → 243). QA do projeto idêntico ao baseline (a única falha do QA, `spr_ProcessandoTr3` com `ModernSpinner@1.1.0` fora da lista, já existia). Nenhum X/Y/Width/Height existente mudou; parênteses balanceados.

## Duas tramas (MEL-205, pedido do William)
**Antes:** a ficha tinha um conjunto só de LI, fio, picks e Ø ("ÚLT. TRANÇA"). Mangueira de 2 tramas gravava só a última e a 1ª se perdia.
**Agora:**
- O delineamento da construção escolhida diz se há 2ª trama (`_30WIRE_PN_2ST` preenchido). **Premissa a confirmar:** fio da 2ª trama em branco = construção de uma trama só.
- Os campos da tela principal passam a ser da **trama final** (2ª, quando há duas). Rótulos mudam sozinhos ("Nº PICKS — 2ª TRAMA", "Ø 2ª TRAMA").
- Novo botão **"1ª trama"** no rodapé (X 420, entre o refresh e o Salvar; só aparece em construção de 2 tramas). Mostra ⚠ até a 1ª trama ter LI, fio e picks, e ✓ depois. Abre uma janela com LI, fio, picks, Ø e o botão "Buscar LI e fio" (mesma lista de bobinas do carrinho; ao copiar, volta para a janela).
- **Enviar p/ Cobertura exige** LI, fio e picks da 1ª trama quando há duas (botão desabilitado e mensagem que reabre a janela).
- **Conferência estrita por trama:** o fio da 2ª trama é comparado só com o fio da 2ª trama do delineamento, e o da 1ª só com o da 1ª (antes aceitava qualquer um dos dois).
- Picks e Ø de cada trama ganham borda âmbar fora da faixa do delineamento; a faixa de alerta explica qual.
- Gravação em 4 colunas novas de `ficha_producao` (precisam existir antes de colar a tela):

| Coluna (nome interno) | Tipo | Conteúdo |
|---|---|---|
| `Lote_Tranc_1aTrama` | Texto de uma linha | LI da 1ª trama |
| `Cod_Tranc_1aTrama` | Texto de uma linha | código do fio da 1ª trama |
| `Picks_Tranc_1aTrama` | Número (0 casas) | picks da 1ª trama |
| `Diam_Tranc_1aTrama` | Número (3 casas) | Ø da 1ª trama em polegada |

As colunas antigas (`Lote_Trançagem`, `Cod_Trançagem`, `N°Picks`, `Diametro_Trançagem`) continuam sendo a trama final: histórico e BI não mudam de significado.

## Outras correções
| # | Onde | Correção |
|---|---|---|
| 1 | Quantidade | Lia com `Value` (depende do idioma) e Salvar Parcial aceitava vazio (gravava 0 e o delta negativo subtraía do turno). Agora `fx_Num` + `fx_MetragemOk`, com aviso. |
| 2 | Margem | "Quantidade maior que o recebido do Tubo" era aviso vermelho para qualquer excesso. Agora respeita a margem de 10% (`fx_MetragemSubiu`), em âmbar, com o % na mensagem. |
| 3 | Iniciar | Não inicia OP sem metragem recebida do Tubo; estado por `fx_EstadoContinuo`; `Coalesce(...,0)` removido das gravações de custódia e evento. |
| 4 | Turno | `_min` + `fx_Turno(_min)` em 7 pontos viraram `fx_TurnoEm(_agora)` (um instante só). |
| 5 | Carretel | Liberar o carretel de entrada e ocupar o de saída não conferiam `Errors` nem tratavam carretel não encontrado. Agora avisam. |
| 6 | Cargas | `DM_TRANÇAGEM`, `DM_ENGRENAGENS`, `DM_FIOS` e `DM_WIREWINDING` em `IfError` + aviso (falha não vira "sem delineamento"). |
| 7 | Diâmetro | Gravava com `fx_NumMedida`; agora `fx_DiametroPol` (milésimo digitado vira polegada) e ganhou aviso de faixa. |
| 8 | Delineamento | Sem delineamento (amostra ou mangueira nova) deixava o botão de continuar desabilitado. Agora avisa em âmbar e **deixa iniciar**. **Extensão da decisão do William para amostras; fácil de reverter.** |
| 9 | Editar OP | Mangueira em texto livre virou lista + "OUTRA (amostra ou nova)" com código em caixa alta (campo de código em X 413, Y 490). |
| 10 | Tokens | Tamanhos 15, 12, 12 e 11 soltos viraram `fx_FonteSecao`, `fx_FonteApoio`, `fx_FonteCorpo` e `fx_FonteApoio`. HintText "Ex: P" corrigido para "Ex: 500". Versão 0.4.0. |

## Não aplicado
- **Tela de impressão e ConsultaOP/FichaImpressao/PainelCelula** ainda mostram só a trama final. Mostrar a 1ª trama entra depois que as colunas existirem.
- A11Y (rodada final): caracteres invisíveis nos botões do menu lateral e `AccessibleLabel`.
- Layout: coluna lateral e rodapé seguem iguais (mock da Debandagem em discussão).
