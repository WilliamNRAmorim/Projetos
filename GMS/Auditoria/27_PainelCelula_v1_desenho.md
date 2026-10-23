# Auditoria 27 — Painel da Célula v1.0 (`scr_PainelCelula_2`): desenho

23/10/2026 · só desenho · nenhuma tela, `Formulas.txt` ou lista foi alterada · aguarda o OK do William no mockup

Mockup: `GMS/Mockups/painel_celula_v1_layout.html` (1366×768, dados fictícios, AO VIVO e HISTÓRICO de 21/10, 2º turno). Fecha a Fase 5 da Auditoria 26 (§7). Mesma linguagem do mockup da Montagem: tokens 20/24/28/40/48 pt, cores de texto de parede, seletor AO VIVO · ‹dia› · 1º · 2º · 3º · DIA · HORA.

## 1. Por que tela nova

- A fonte de TV (mínimo 20 pt, números 40 a 48 pt) não cabe na geometria da `scr_PainelCelula_1`, que tem texto em 10 a 13 pt (A4). Mexer em X/Y/Width/Height de centenas de controles viola a regra "layout salvo é o vigente" e não é patch por bloco.
- A carga atual lê o status ATUAL da ficha (`Em processo` / `Aguardando`). O passado não existe nesse status, então o seletor de dia/turno/hora não pode ser enxertado na v0.x.
- A v0.x (com o patch v0.11.0) fica publicada até a v1.0 ser validada na TV; depois sai do app.

## 2. O que a tela mostra (mockup)

| Bloco | Conteúdo | Observação |
|---|---|---|
| Cabeçalho | seletor de período, relógio, idade do dado | histórico: borda laranja, "HISTÓRICO", contagem "volta 4:30" |
| 4 KPIs | GARGALO (etapa com menor % do ritmo e o %), PARADA REAL, PAUSA, EXCEDIDO | parada real, pausa e excedido nunca se somam |
| Produção do turno | 8 etapas em metros, realizado / meta, barra, %, traço branco = ritmo esperado agora | trançagem destacada como gargalo (borda laranja) |
| Postos | 11 trançadeiras + 7 etapas | cor, palavra e minutos; fonte mínima 27 px = 20 pt |
| Onde olhar | páginas de 3 a 5 itens, 30 s por página, contador "1/2" | o contador é o total real; nada é cortado em silêncio (A2) |

Regras de leitura:
- Barra: verde se o realizado está em 95% ou mais do ritmo esperado, laranja de 80% a 95%, vermelha abaixo. Ritmo = % do turno decorrido (hora H ou agora; no turno fechado, 100%). Evita pintar de vermelho a produção no começo do turno.
- Gargalo = menor realizado ÷ ritmo entre as 8 etapas. Hoje a Auditoria 26 trata a trançagem como gargalo; o mockup deixa a regra "menor relação" para o painel não ter nome fixo. PENDÊNCIA de decisão: fixar trançagem ou usar a menor relação.
- Estados do posto (chaves que `fx_CorEstadoPosto` já usa): PRODUZINDO, COM FILA, PARADA, RESFRIANDO, AGUARDANDO, LIVRE. Mais um: PAUSA (decisão 1 da Auditoria 26). Nos cartões a palavra é curta (RODANDO/RODA, FILA, RESFR.) porque 27 px não cabe PRODUZINDO em 154 px: criar `fx_RotuloEstadoTV` quando for codar.
- Idade do dado: selo "dados hh:mm", verde até `fx_PainelIdadeAlertaMin` (5 min), vermelho depois (Fase 1 da Auditoria 26).
- Refugo: NÃO está no mockup. Não há fonte confirmada por etapa no painel (a Auditoria 26 §3 item 5 pede). Vira pendência (seção 8).

## 3. Fontes de dados e como reconstruir o passado

Só nomes de coluna vistos em telas existentes (`scr_PainelCelula_1`, `scr_Bandagem_1`, `scr_Cobertura_2`, `scr_Debandagem_2`, `scr_ConsultaOP_1`, `scr_FichaImpressao`, `Formulas.txt` §11/§12).

| Fonte | Colunas usadas | Papel |
|---|---|---|
| `Eventos_Producao` | `data_hora`, `data_ref`, `turno`, `etapa` (Choice, `.Value`), `tipo` (Choice: Início, Fim, Parcial, Cancelado), `metros`, `origem_ID` | Metros produzidos por etapa e período; Início/Fim para o estado dos postos. Grão: 1 linha por OP × etapa × tipo |
| `ficha_producao` | `status_processo`, `processo`, `cabine_teste`, `data_hora_inicio_<etapa>` e `data_hora_final_<etapa>` com `<etapa>` = mandril, tubo, trancadeira, cobertura, bandagem, vulcanizacao, debandagem, extracao | Fallback do estado dos postos; idade da OP; fila |
| `Hora-Hora` | `Data`, `Turno`, `Hora`, `Célula`, `Real. Hora`, `Meta Hora`, `Tempo Parado (min)`, `Motivo`, `ID` | Meta e real da trançagem; paradas por janela |
| `fx_MotivosParada` | `Motivo`, `Tipo` (Programada, Falha, Processo, Material, Organizacional, Engenharia) | Separa PAUSA (Programada) de PARADA REAL |
| `fx_GradeHoraHora`, `fx_PeriodoIniEm`, `fx_PeriodoFimEm`, `fx_TurnoNum`, `fx_DataRefEm` | já em `Formulas.txt` (§4, §11, §18) | Limites de período sem hora escrita à mão |

### 3.1 Produção por etapa (metros)

- Realizado = soma de `metros` dos eventos da etapa com `data_hora` no período `[fx_PeriodoIniEm, fx_PeriodoFimEm)`. Que tipos entram na soma (Fim, Parcial, ou ambos) é PENDÊNCIA: o painel atual só usa Eventos para Vulcanização, Mandril e Extração e não soma `Parcial`.
- Meta por etapa:
  - Mandril: `fx_MetaTurnoMandril` (5.000 m, turno completo). A Auditoria 26 M13 aponta que 5.000 vale só para turno completo; o histórico precisa da meta proporcional aos minutos do turno (`Fim` da grade: 517, 524, 399). PENDÊNCIA de decisão.
  - Trançagem: soma de `Meta Hora` do Hora-Hora no período (já feito no painel atual, `HHMeta`).
  - Tubo, Cobertura, Bandagem, Vulcanização, Debandagem, Extração: NÃO há fonte de meta confirmada. No mockup as metas são placeholder. PENDÊNCIA (depende de dado novo ou de decisão; ver seção 8).

### 3.2 Reconstruir o estado dos postos na hora H

Hora H = fim do período escolhido (ou agora no AO VIVO). Por etapa, por OP:
- **Processando:** existe evento `Início` da etapa com `data_hora` ≤ H e não existe `Fim` da mesma `origem_ID` + etapa com `data_hora` ≤ H.
- **Na fila:** existe `Fim` da etapa anterior (ordem de `fx_EtapasLinha`) com `data_hora` ≤ H e não existe `Início` da etapa atual com `data_hora` ≤ H.
- **Livre:** nem uma nem outra.
- **Cancelado:** `tipo = Cancelado` anula o par; ignorar a OP daquela etapa.
- Parada e pausa vêm do Hora-Hora: a janela que contém H (`fx_GradeHoraHora` + `fx_JanelaHHIni/Fim`, a mesma correção da v0.11.0 item 1) com `Tempo Parado (min)` > 0 ou `Motivo` não vazio; `Tipo = Programada` vira PAUSA.
- Qual trançadeira está com qual OP: o evento não traz a máquina nos nomes confirmados nas telas. A coluna `recurso` aparece só em comentário da `Formulas.txt` §12, não em consulta de tela. PENDÊNCIA: confirmar o nome interno da coluna de máquina em `Eventos_Producao` (e se `ficha_producao` guarda a trançadeira) antes de codar o mapa por posto. Sem isso o mapa de trançadeiras no histórico usa só o Hora-Hora (Célula + janela), sem OP.
- `ficha_producao` serve de conferência: `data_hora_inicio_<etapa>` ≤ H e `data_hora_final_<etapa>` vazio ou > H dá o mesmo "processando" e valida o evento. Divergência entre os dois é tela de auditoria, não do painel.

### 3.3 Paradas do turno

- PARADA REAL = minutos de `Tempo Parado (min)` das janelas do período cujo `Motivo` não é `Tipo = Programada` e não é tempo excedido.
- PAUSA = minutos das janelas com `Tipo = Programada`.
- EXCEDIDO = tempo produzindo acima da meta. Na Montagem vem do motivo "TE - Tempo Excedido" (`fx_MotivoTempoExcedido`). Na célula a fonte é PENDÊNCIA: o Hora-Hora da trançagem não tem coluna de tempo excedido confirmada. Opção sem coluna nova: derivar de `Real. Hora` > `Meta Hora` (minutos equivalentes). Decisão do William, passa pelo `revisor` (regra de parada).
- Regra do CLAUDE.md do GMS: parada real nunca soma com excedido. A tela exibe os três números separados e nenhum total.

## 4. Consultas delegáveis necessárias

Todas com data como primeiro filtro, sem `Search`, `in` sobre fonte ou `ClearCollect(col, Fonte)` sem `Filter`. Janela = `fx_PeriodoIniEm(dataRef, periodo, hora)` a `fx_PeriodoFimEm(...)`. Estimativas de volume saem de números já medidos: Hora-Hora ≈ 300 linhas por dia produtivo (comentário v0.10.1, L84-86); Eventos 6.240 linhas em ~45 dias, ≈ 140 por dia (Formulas §12), ou ≈ 25 por etapa por dia. São estimativas; medir antes de fechar.

| Consulta | Filtro | Volume estimado | Quando |
|---|---|---|---|
| Eventos do dia | `data_ref = dataRef` (sem filtrar etapa; filtrar etapa localmente) | ≈ 140 | AO VIVO a cada 2 min; histórico 1× por escolha |
| Eventos do dia anterior | `data_ref = dataRef - 1` | ≈ 140 | só para fila que atravessa a virada do dia (OP com Início ontem, Fim hoje) |
| Hora-Hora do dia | `Data = dataRef` | ≈ 300 | igual; ontem só se o período cruzar o dia |
| ficha_producao ao vivo | `status_processo = "Em processo"` e `"Aguardando"` | o atual (2 consultas) | só no AO VIVO |
| ficha_producao histórica | NÃO consultar na v1.0 | — | o passado vem dos Eventos |

Observações:
- Filtrar `data_ref` (igual) é delegável e respeita a fronteira das 05:20 em 100% das linhas conferidas (Formulas §12). Filtrar `data_hora` contra `fx_PeriodoIniEm`/`FimEm` também delega, mas só é necessário para HORA (janela menor que o dia). Para turno e dia, `data_ref` + filtro local pelos limites do período é mais barato.
- Hora H precisa de TODOS os Início do dia (Início sem Fim até H): por isso a consulta é do dia inteiro e o corte em H é local. Um Início do dia anterior sem Fim no dia anterior exige a consulta de D-1.
- 3º turno termina em D+1 05:20: `fx_PeriodoFimEm` devolve `dataRef + 1360 + 399 min`; os eventos depois da meia-noite já têm `data_ref = dataRef` (dia produtivo), então a consulta de D+1 não é necessária.

## 5. O que muda na carga em relação à v0.11.0

- Sai: lógica baseada em status atual como única fonte; os 3 filtros de Eventos viram 1 consulta (a v0.11.0 já faz isso) com filtro de etapa local.
- Entra: janela de período (`fx_PeriodoIniEm/FimEm`) em vez de "hoje", uma variável de período única (dia, período, hora) e `ClearCollect` por escolha no histórico, sem timer.
- AO VIVO: mesmo ciclo de 2 min e mesmas 3 a 4 consultas da v0.11.0 (Hora-Hora, Eventos, ficha ×2) em `Concurrent`, com `IfError` de ramo fechado e idade do dado.
- Histórico: carga única por toque (Hora-Hora do dia + Eventos do dia, no máximo D-1), sem ficha. Volta ao vivo sozinho em `fx_HistVoltaMin` (5 min) sem toque.
- Um único instante de referência por ciclo (M10): H = agora no ao vivo, H = fim do período no histórico.
- Fora da carga nova: DM_TRANÇAGEM × DM_ENGRENAGENS e a autonomia de tubo (laço N × M). Não aparecem no mockup; ver seção 8.

## 6. Riscos

1. **Delegação e 2.000 linhas:** Eventos de 1 dia (~140) e Hora-Hora de 1 dia (~300) cabem. O risco é uma consulta sem `data_ref`/`Data` virar leitura da lista inteira (6.240 e crescendo). Guarda de truncamento (`fx_PainelLinhasAlerta` = 1.800) com aviso vermelho no cabeçalho.
2. **Nomes internos não confirmados:** `ShowColumns` em `ficha_producao` já quebrou por nome interno (lição v0.7.1). Não usar `ShowColumns` na ficha nem em Eventos sem conferir o nome interno de cada coluna no schema da lista. Lista de colunas a confirmar: máquina/recurso em Eventos, trançadeira na ficha, qualquer coluna de refugo.
3. **Início sem Fim por esquecimento:** OP com Início e sem Fim "processando" para sempre. Aplicar `fx_TetoOPHoras` (72 h): acima disso o posto aparece como "OP antiga", fora do cálculo de processando.
4. **Evento duplicado ou cancelado:** duas linhas Início da mesma `origem_ID` + etapa. Usar o de maior ID (padrão do Hora-Hora) e tratar Cancelado.
5. **Hora-Hora duplicado por janela:** deduplicar pelo maior `ID` (M4).
6. **Virada de turno (22:41, 13:57) e fronteira 05:20:** toda borda por `fx_GradeHoraHora`, nada de hora escrita. Revisor confere a tabela de limites (05:19, 05:21, 13:56, 13:58, 22:30, 22:42, 23:59, 00:01).
7. **TV sem mouse:** histórico só funciona com toque ou mouse; sem isso a TV fica no AO VIVO.
8. **Geometria 1366×768:** o mockup fecha, mas a TV real é de polegada desconhecida (43" suposto). Ajuste de fonte só na §18.
9. **Onde olhar com 5 itens por página:** a página gira a cada 30 s; se a TV for lida só por 10 s, o 2º item da fila não aparece. Mitigação: ordenar por gravidade e mostrar o total no contador.
10. **Palavra curta do estado (RODA/FILA):** nos cartões pequenos; se o supervisor não gostar, mudar a largura dos cartões (decisão visual do William).

## 7. Passos de código, depois do OK no mockup

1. Formulas: adicionar o necessário (aditivo): `fx_RotuloEstadoTV`, `fx_CorEstadoPosto` com "PAUSA" (usa `fx_CorGelo`), `fx_RitmoEsperado(periodo, H)`, função de meta por etapa conforme decisão. Regra passa pelo `revisor`.
2. `Telas/scr_PainelCelula_2.txt`: novo, nascido de `fx_` e dos tokens da §18. Nada de `Set` sem leitor, nada de tamanho escrito à mão, timers com `Visible: false`.
3. Carga em `OnVisible`/botão: variável de período, `Concurrent` com ramos `IfError` fechados, medidor do ciclo (segundos) no rodapé.
4. Coleções de reconstrução: `colEvPeriodo`, estado por etapa e por posto na hora H, produção por etapa.
5. Seletor (ao vivo, dia, 1º/2º/3º, DIA, HORA) igual ao da Montagem; volta ao vivo em 5 min.
6. Onde olhar paginado, com idade do problema e total real.
7. QA (`gms_qa_yaml.py`), revisor (regra de parada/turno), revisor-leve (resto), Preview com rede desligada.
8. Print na TV real; só então tirar a `scr_PainelCelula_1` do app e do `Telas/`.
9. Diário (MEL novo pelo `gms.py --novo`), Índice, commit por assunto e push.
- Ordem de colar no Studio: Formulas, depois a tela nova, depois o botão de entrada ("Painel de TV") na tela de seleção da célula. Nada disso começa antes do OK do William.

## 8. O que depende de dado novo ou de decisão (pendências explícitas)

1. **Meta por etapa** para Tubo, Cobertura, Bandagem, Vulcanização, Debandagem, Extração (e meta proporcional do Mandril por turno). Opções: lista de configuração nova (`ConfiguracaoGMS` já é citada em `fx_TetoOPHoras`) ou usar a meta da trançagem como régua. Decisão do William.
2. **Tipos de evento que somam metros** (Fim, Parcial, ambos).
3. **Coluna de máquina/posto** em Eventos e na ficha (nome interno a confirmar no schema).
4. **Fonte de EXCEDIDO** na célula (ver 3.3).
5. **Refugo do turno**: sem coluna confirmada; fora do mockup.
6. **Gargalo**: fixo na trançagem ou menor relação ao ritmo.
7. **Autonomia de tubo** e metas por bitola (kanban do mandril) ficam de fora da v1.0 do mockup; entram como bloco opcional depois, pelas mesmas coleções da v0.11.0, se a TV tiver espaço.
8. **Número de postos por etapa** fora da trançagem (cartões pequenos mostram o estado da etapa, não de cada posto).
9. **Polegada da TV** (43" suposto, medir a diagonal).

## 9. Verificação do mockup

- Renderizado no navegador embutido (1366×768): conferidos sobreposição, estouro de cartão e texto cortado por script (largura e altura de cada texto contra o contêiner) e por screenshot. Fonte mínima 27 px (20 pt) em todos os textos da tela; só os rodapés de nota (13 a 14 px) fora da tela do app.
- Dados 100% fictícios; nenhum dado de produção foi usado nem enviado a serviço externo. A fonte do Google foi removida (Open Sans com Segoe UI de reserva).
