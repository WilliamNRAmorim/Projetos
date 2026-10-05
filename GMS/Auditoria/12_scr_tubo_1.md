# Auditoria GMS — 12 · `scr_tubo_1` (v0.4.0 → v0.5.0)

Lida por inteiro (3.595 linhas, 176 controles → 185). QA do projeto idêntico ao baseline; nenhum X/Y/Width/Height existente mudou; parênteses balanceados.
Dados: `ficha_producao.csv`, 2.629 OPs com tubo produzido.

## O que os dados mostraram
- **Diâmetro do tubo é gravado em polegada** (mediana 0,73), mas a tela dizia "DIÂMETRO (mm)". 60 valores (2,3%) estão acima de 5, ou seja, milésimo digitado (ex. 900); 6 são 0 ou negativos; 1 em branco.
- **Composto:** 2.123 de 2.629 usam `640-99`; o resto tem variantes (`64099`, `64-99`, `640-099`, `H028`, `H-028`, `2023`). Só 3 sem código e 3 sem validade.

## Aplicado (v0.5.0)
| # | Onde | Problema | Correção |
|---|---|---|---|
| 1 | Diâmetro | Rótulo "mm" errado; sem conferência com o delineamento; milésimo entrava como 900 pol. | "DIÂMETRO (pol.) *"; `fx_DiametroPol` na gravação (milésimo vira polegada); borda âmbar fora de `MIN_OD`–`MAX_OD`; obrigatório para enviar. |
| 2 | Composto e validade | Validade vencida em vermelho com "chame a supervisão" (parece bloqueio). Comparava data com data/hora. | Só avisa (âmbar), comparando com a data de hoje. Código do composto inválido ("0") e diferente do `TUBE_PN` do delineamento também só avisam. **Código do composto passa a ser obrigatório para enviar** (o diâmetro e a validade também). |
| 3 | Metragem | `Value()` em 10 pontos (depende do idioma); enviava com `Coalesce(...,0)`; iniciava OP sem metragem do Mandril. | `fx_Num` e `fx_MetragemOk`; não inicia sem metragem recebida do Mandril; salvar parcial grava vazio em vez de 0. |
| 4 | Balanço | "Produzido + refugo passou do que entrou" em vermelho para qualquer excesso. | Respeita a margem de 10% (`fx_MetragemSubiu`), em âmbar, com o % na mensagem; saldo só fica vermelho acima da margem. |
| 5 | Salvar parcial | Podia apagar mangueira, trançadeira e operador se o campo estivesse em branco. | `Coalesce(campo, valor já gravado)`. |
| 6 | Mangueira de amostra | A lista só tinha o cadastro; amostra ou mangueira nova não dava para escolher (e é aqui, no Tubo, que a mangueira nasce). | Opção "OUTRA (amostra ou nova)" na lista; abre uma janela para digitar o código (caixa alta). Delineamento sem cadastro também deixa continuar (aviso âmbar). |
| 7 | Carretéis | Ocupar, liberar e devolver sobra (`lista_carreteis`) sem `Errors` e sem tratar carretel não encontrado. | Conferem e avisam. |
| 8 | Turno | `_min` + `fx_Turno(_min)` em 7 pontos. | `fx_TurnoEm` (um instante). |
| 9 | Cargas | `DM_TUBE_EXTRUSION` e 3 `Refresh` + 3 `ClearCollect` em fila. | `IfError` + aviso; `Concurrent`. Relógio de 120 s também respeita as janelas de delineamento e de mangueira. |
| 10 | Padrão visual | `Arial`, `Segoe UI` ×5, chip com raio 5 e tamanho 14. | Tokens; `fx_MetrosUn` nas metragens. |
| 11 | **Ícone trocado** | "Histórico do turno" usava o ícone `send` (avião de papel). | `clipboard-list` (já importado). |
| 12 | Editar plano | Salvava bitola vazia/0. | Desabilita sem bitola. `Trim` nos carretéis. |

## Fora desta tela, no mesmo ciclo
- `scr_Cobertura_2`: a validade vencida comparava com `DateValue(ctxAgora)` (data/hora virando texto). Trocado por `Date(Year, Month, Day)`; comportamento igual, sem depender do idioma.

## Atenção ao testar no Studio
- A lista de mangueira do Tubo usa `Ungroup(Table(...), "t")` para incluir uma mangueira fora do cadastro; se o Studio reclamar dessa fórmula (propriedade `Items` do `cmb_MangueiraTubo_1`), me avise.
- O aviso ao William de mangueira fora do cadastro continua pendente da lista `Avisos_GMS`.

## Não aplicado
- A11Y (rodada final): "MENU LATERAL", caracteres invisíveis nos botões do menu lateral, `AccessibleLabel` nos botões.
- Layout: menu lateral e rodapé seguem iguais (mock da Debandagem em discussão).
