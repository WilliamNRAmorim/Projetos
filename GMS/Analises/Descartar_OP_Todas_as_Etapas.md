# Descartar OP e desfazer início em qualquer etapa (MEL-222): como ficou

Tela nova `Telas/scr_DescartarOP_1.txt` (v0.1.0, 08/10/2026) + botão "Descartar OP" nas 7 telas de etapa. O Mandril continua com o fluxo dele (lápis da bitola).
**Status: escrito e passou na bateria `gms_qa_yaml.py`; NÃO foi aberto nem testado no Studio.**

## Decisão que seguiu (diário, 06/10)
Descartar = tirar do processo. O material apontado vira não conforme e sai (não volta para a etapa anterior); só os carretéis da OP são liberados. Não pede PIN; o freio é motivo obrigatório + nome de quem descartou.

## Como funciona
1. Em cada tela de etapa (Tubo, Trançagem, Cobertura, Bandagem, Vulcanização, Debandagem, Extração/Finalização) aparece, na faixa "Ordem", o botão vermelho **Descartar OP** quando a OP selecionada está **Em processo**. Ele guarda `varDescarteID` e `varDescarteEtapa` e abre `scr_DescartarOP_1`.
2. A tela mostra OP, mangueira, quanto foi apontado na etapa (vira refugo) e o operador, com um aviso do que acontece.
3. O operador escolhe o motivo (OP aberta por engano, Mudança de plano, Material não conforme ou Outro com detalhe obrigatório) e quem está descartando. O botão só habilita com tudo preenchido.
4. Ao confirmar, a tela confere antes de gravar: OP existe, ninguém alterou o registro, ainda está Em processo.
5. Grava na `ficha_producao`: `status_processo = "Cancelado"` e `processo = "Cancelado"` (o `processo` sai da fila da etapa, como o Finalizado faz), data/hora final, turno, operador e a nota "[OP DESCARTADA dd/mm hh:mm na ETAPA por NOME - motivo - X m viraram refugo]" no campo de observação da etapa.
6. Libera todo carretel com `op = ID` da OP em `lista_carreteis` (`op` e `etapa_processo` em branco, `mangueira_atual` em branco, `metros_restantes = 0`), igual à limpeza que a Cobertura já faz.
7. Grava o evento `<ID>-<Etapa>-Cancelado` em `Eventos_Producao` (tipo Cancelado, sobra = metros apontados) e volta para a tela da etapa.

## Campos usados por etapa (todos já existem em uso no app, exceto os marcados)
| Etapa | Final | Turno | Operador | Observação |
|---|---|---|---|---|
| Tubo | data_hora_final_tubo | Turno_Tubo | operador_tubo | Observação_tubo |
| Trançagem | data_hora_final_trancadeira | Turno_Trançagem | operador_trancagem | Observação_Trançagem |
| Cobertura | data_hora_final_cobertura | Turno_Cobertura | operador_cobertura | Observação_Cobertura |
| Bandagem | data_hora_final_bandagem | Turno_Bandagem | operador_bandagem | **Observação_Bandagem** (existe na lista, mas nenhuma tela usa ainda) |
| Vulcanização | data_hora_final_vulcanizacao | Turno_Vulcanização | operador_vulcanizacao | **sem campo próprio**: a nota vai em Observação_Bandagem |
| Debandagem | data_hora_final_debandagem | Turno_Debandagem | operador_debandagem | Observação_Debandagem |
| Extração | data_hora_final_extracao | (não grava; o nome é `Turno_Extr/Teste`) | operador_extracao | **sem campo próprio**: a nota vai em Observação_Debandagem |

## O que testar no Studio (primeiro uso)
- Colar `scr_DescartarOP_1.txt` e colar os blocos novos das 7 telas (ou colar as telas inteiras). Se o Studio reclamar de um nome de coluna, é nesta tabela.
- Descartar uma OP de teste em cada etapa e conferir: a OP some da fila, o carretel fica livre, o evento Cancelado grava, a nota aparece no histórico.
- Ver se o Painel da Célula, o Hora-Hora e o BI aceitam `processo = "Cancelado"` sem acusar (todos filtram por `status_processo` Em processo/Aguardando, então não deveriam contar).
- Vulcanização: descartar uma OP dentro de um lote de até 5 carretéis. A tela só mexe na OP escolhida; os outros carretéis do lote seguem.
- Depois do descarte a tela da etapa precisa recarregar a fila no `OnVisible`. Se ainda aparecer a OP, falta um `Select` do botão de carregar.

## Limites (fora desta versão)
- Só descarta OP **Em processo**. OP na fila (Aguardando) ainda não tem o botão; para engano de plano use Editar a OP.
- Mandril não usa esta tela.
- A liberação de carretel de mandril (`CarreteisMandril`) continua só no fluxo do Mandril.

## Desfazer o início (v0.2.0)
Na mesma tela (`scr_DescartarOP_1`) há duas abas no cabeçalho: **Descartar a OP** e **Desfazer o início**. O botão nas telas de etapa agora se chama "Descartar / desfazer início".
Serve para quando o operador apertou Iniciar por engano: a OP volta para **Aguardando** (fila da etapa), como se nada tivesse acontecido.

O que o "Desfazer o início" faz, na ordem:
1. Só vale com OP **Em processo** e **sem metros apontados** na etapa. Com metros apontados a tela manda usar Descartar.
2. `ficha_producao`: `status_processo = "Aguardando"`, apaga data/hora de início, início em processo, turno e `Carretel Saida` da etapa (na Trançagem só apaga o início se foi este Iniciar que o gravou, porque ali um segundo Iniciar preserva o primeiro) e acrescenta a nota "[INÍCIO DESFEITO ...]" na observação da etapa.
3. `lista_carreteis`: libera o carretel reservado por esta etapa (`op` e `etapa_processo` em branco).
4. `Historico_Carretel`: apaga a linha de custódia criada por este início (mesma OP, etapa e hora de entrada do evento).
5. `Eventos_Producao`: apaga o evento "Início" da OP nesta etapa, para o Hora-Hora e o painel não contarem dois inícios quando a OP for iniciada de novo.

**Não volta sozinho:** se ao iniciar o operador usou a **sobra de um carretel** (Tubo, Trançagem, Cobertura), os metros dessa sobra foram zerados naquele momento. A tela avisa o carretel e os metros (guardados no evento de início) para ajustar na tela de carretéis.
