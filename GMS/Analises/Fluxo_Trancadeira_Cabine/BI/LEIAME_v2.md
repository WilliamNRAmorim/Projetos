# Fluxo v2 (tubo → cabine, espiral separada, carretéis) no GMS_Painel · como gerar e conferir

Status (04/11/2026): **gerado só na cópia local** `GMS/PowerBI/Painel_PBIP_teste` (fora do git). Nada foi gravado no
`GMS_Painel.Report`, no `Modelo_PBIP`, no `Modelo_PBIP_teste` nem no modelo publicado. Falta abrir no Desktop, rodar a
conferência e a revisão (`revisor`, Opus: turno e contexto de filtro). Plano: `PLANO_v2_tubo_espiral_carreteis.md`.

| Arquivo | O que é |
|---|---|
| `gerar_medidas_paginas_fluxo.py` | gera as medidas do relatório e as 2 páginas na cópia, grava a consulta de conferência e valida |
| `Consulta_Conferencia_v2.dax` | **gerado** pelo script (não editar): 3 EVALUATE para rodar no Desktop |
| `gerar_paginas_fluxo.py` | gerador v1 (piloto com `dEtapa`/`fPessoasEtapaOP`); o v2 importa dele só o estilo (paleta, segmentação, navegador, rodapé) |
| este LEIAME | regras, limites, layout e conferência |

## 1. Como regenerar
1. Feche o `GMS_PainelTeste.pbip` no Desktop.
2. Nesta pasta: `python gerar_medidas_paginas_fluxo.py` (padrão: `..\..\..\PowerBI\Painel_PBIP_teste\GMS_Painel.Report`).
   Outro `.Report` vai como 1º argumento; fora de pasta `*_teste` o script recusa, salvo `--forcar`. `--validar` só confere.
3. O script tira do `reportExtensions.json` só as medidas `Fluxo · ...` e põe as novas no fim; apaga e recria só
   `pg_fluxo_1` e `pg_fluxo_2`, põe as 2 no fim do `pages.json` (a página ativa não muda); não mexe no `report.json`,
   no tema nem nas outras páginas. Regera `Consulta_Conferencia_v2.dax`. Rodar 2 vezes dá os mesmos arquivos.
4. Ajuste feito à mão no Desktop nessas 2 páginas some na próxima geração: leve o ajuste para o script.
5. Cópia de trabalho refeita do zero: copiar `GMS_Painel.pbip` (como `GMS_PainelTeste.pbip`) e `GMS_Painel.Report`
   sem `.pbi`, com `.gitignore` = `*` dentro da pasta.

## 2. Medida do relatório (o que é e o que muda)
- O `GMS_Painel` é relatório **ligado ao vivo** ao modelo `(GMS)`. Nele não dá para criar tabela, coluna nem
  relacionamento; só **medidas do relatório**, gravadas em `definition/reportExtensions.json` (entidade `Medidas`).
  No visual, a referência leva `"Schema": "extension"`.
- **Medida do relatório não pode chamar outra medida do relatório** (erro semântico no serviço). Por isso cada medida
  `Fluxo · ...` é escrita por extenso a partir do mesmo núcleo DAX, montado pelo script (`nucleo()`): uma regra mudou,
  muda no script e regera tudo. Nunca edite a medida à mão no Desktop.
- Prefixo `Fluxo · ` em todas (23 medidas); a validação confere colisão com o TMDL e com as medidas do relatório.
- SVG: `dataType` Text com `dataCategory` = `ImageUrl` (se o Desktop não aceitar a categoria pelo arquivo, marcar à mão:
  Ferramentas de medida → Categoria de dados → URL da imagem).

## 3. Regras de cálculo (todas direto da `ficha_producao` e do `dCalendario`)
- **Etapas (8):** Tubo, Trançagem, Espiral, Cobertura, Bandagem, Vulcanização, Debandagem, Cabine (Extração/Teste).
  **Mandril fora** (decisão do William). Trançagem e Espiral leem `data_hora_final_trancadeira`, `quantidade_trancagem`
  e `operador_trancagem` e se separam por `ficha_producao[Trançadeira]` normalizada (maiúsculas, sem ponto, hífen,
  espaço e sublinhado): TH01–TH07, TM01, TM04, TO04 = Trançagem; SPIRAL, TE01, TE0 = Espiral. Máquina vazia ou lixo
  (0, 1, T004, 4…) fica fora dos cartões, mas entra no total "trançagem + espiral" (dia produtivo, CV, rendimento,
  gráficos mensais).
- **Dia** = data do fim da etapa menos 05:20. **Dia produtivo** = trançagem + espiral (com lixo) ≥ 3.000 m no dia
  inteiro, qualquer turno escolhido. Com 1 dia filtrado, ele entra sempre se houver apontamento.
- **Contexto:** a seleção do `dCalendario` é guardada em VAR antes de tudo; a ficha é lida com `ALL ( ficha_producao )`
  (ignora o relacionamento ativo `DataProducao → dCalendario` e qualquer outro filtro) e o dia é a data de referência
  calculada na medida.
- **Quantidade** > 2.000 m por ficha e etapa = erro de digitação, vira vazio (a pessoa continua contada).
- **Pessoas** = operadores distintos normalizados (maiúsculas, sem acento, sem `.`, `,`, `-`, `_`, espaço único) por
  dia e etapa; "A / B" conta 2 pessoas. Média nos dias produtivos (dia sem apontamento conta 0).
- **Carretéis** por ficha = metros ÷ metros do carretel da `Bitola`: 4 → 800 · 6 → 680 · 8 → 680 · 10 → 460 ·
  12 → 400 · 16 → 250. Bitola fora da tabela (7, 3, 5, 17, vazia): os metros contam, o carretel fica **n/d** e o
  cartão mostra a fatia coberta ("carretéis em 96% dos metros"). Carretéis/dia = média dos dias produtivos; por pessoa
  = carretéis/dia ÷ pessoas/dia.
- **Série × cartões (William, 04/11):** Trançagem (braiders) e Espiral são máquinas **paralelas** da mesma etapa
  original, não etapas em série (a espiral é pequena porque só roda a família GH493). Nos cálculos de **série** elas
  viram **uma etapa "Trançagem+Espiral"** (com a máquina lixo): série = Tubo, Trançagem+Espiral, Cobertura, Bandagem,
  Vulcanização, Debandagem, Cabine (7). Valem pela série: restrição (menor m/dia), eficiência de balanceamento,
  conteúdo médio do trecho (tracejado da página 2), rendimento e WIP. Nos **cartões** continuam separadas (metros,
  pessoas e carretéis próprios), e o destaque "mais gente/metro" é entre os 8 cartões individuais; a barra de cada
  etapa na página 2 também é individual (8 barras) com o tracejado na média da série.
- KPIs: vazão, m/pessoa, pessoas por 1.000 m, eficiência de balanceamento (Σ conteúdo ÷ (n × maior), na série de 7),
  restrição (menor m/dia na série de 7), lead time (mediana única por ficha, fim da trançagem/espiral → fim da cabine, 0,5 a 720 h,
  fichas que saíram da cabine em dia produtivo), WIP de Little (vazão da cabine por dia de calendário × lead time médio
  ÷ 24), CV da vazão de trançagem + espiral, rendimento (cabine ÷ trançagem + espiral).
- **Pessoas tranç./cab.** e os gráficos de pessoas: "trançagem" = trançagem + espiral + lixo como um grupo só (a mesma
  pessoa nas duas máquinas no mesmo dia conta 1). "pessoas no trecho" = soma das 8 etapas (a mesma pessoa em 2 etapas
  conta nas 2).
- Leitura automática: texto do piloto; a restrição fala em "Trançagem+Espiral" quando for o caso (nunca "Espiral"
  sozinha); a frase de mão de obra cita a etapa individual de mais gente por 1.000 m (pode ser a Espiral) e compara com
  a média do trecho (7 etapas). No balanceamento a frase de "espaço para realocação" virou "Cada etapa tem uma natureza
  de trabalho; a diferença só vira espaço de realocação onde há ociosidade."
- **Nomes de VAR:** o DAX não diferencia maiúsculas e recusa repetir um nome dentro da mesma medida, mesmo em escopo
  aninhado de iterador (erro do Desktop em 04/11: `__La` da paleta × `__LA` do núcleo). O script dá nome único a cada
  VAR (sufixo por fonte: `__qS1`, `__fLT`, `__cvS8Car`…; cores `__cor...`; laços `__iPe`, `__iCa`) e a validação
  falha listando, por medida, as VAR repetidas e as que têm nome de tabela do modelo.

## 4. Turno (segmentação `fHoraHora[Turno]`)
- O modelo ao vivo não tem `dTurno`. A segmentação **Turno** das 2 páginas usa **`fHoraHora[Turno]`**, a mesma coluna da
  página Hora-Hora do `GMS_Painel` (grupo de sincronização próprio `fluxo_turno`, não sincroniza com a Hora-Hora).
- As medidas só **leem** a escolha: `ISFILTERED ( fHoraHora[Turno] )` diz se há filtro direto; `VALUES` dos turnos
  escolhidos (sem o filtro de data) vira o conjunto {1, 2, 3} pelo **primeiro algarismo 1, 2 ou 3** do texto
  ("1º Turno", "1º TURNO", "1" funcionam). Sem filtro direto, nenhum turno é aplicado.
- O turno é aplicado **por linha de ficha**, pela hora do **fim** de cada etapa: 05:20–13:56 = 1; 13:57–22:19 = 2;
  22:20–05:19 = 3 (minutos 320/837/1340, norma). O dia continua pela virada 05:20 e o corte de 3.000 m é do dia inteiro;
  as médias são dos metros, pessoas e carretéis do turno nos dias produtivos. Lead time e Little: fichas que saíram da
  cabine no turno.
- Não usa `ficha_producao[Turno_*]`, `Turno_Producao` nem `Etapas[Turno]` (a validação recusa). A data das medidas é
  capturada com `REMOVEFILTERS ( fHoraHora[Turno] )`, para o turno não cortar dias se o relacionamento da `fHoraHora`
  for de 2 sentidos.
- **Dependência:** a coluna `fHoraHora[Turno]` precisa existir no modelo ao vivo (existe: a página Hora-Hora usa) e ter
  linhas nas datas escolhidas. A lista da segmentação mostra só os turnos com Hora-Hora no período: se um dia não teve
  Hora-Hora no 3º turno, o 3º turno não aparece para escolher naquele dia, mesmo com ficha nesse turno.

## 5. Limites (o que não dá sem mexer no modelo)
- **Sem Mês/Ano:** não existe `dCalendario[Mês/Ano]` no modelo ao vivo. Os gráficos mensais usam a hierarquia de datas
  automática do `dCalendario[Date]` (níveis Ano e Mês, expandidos; o mês sai pelo `MonthNo`, em ordem). Se o modelo
  publicado não tiver data/hora automática para o `dCalendario`, os 2 gráficos quebram (campo inexistente).
- **Sem `dTurno`:** turno pela `fHoraHora[Turno]` (seção 4).
- **n/d de bitola:** carretéis só onde a bitola está na tabela; a fatia coberta aparece no cartão.
- **Mês da segmentação** em ordem alfabética (`dCalendario[Mês]` sem classificar por `Mês Nº`; pendência antiga).
- **Navegadores das páginas antigas** mostram todas as páginas: com 2 páginas a mais podem apertar os botões delas.

## 6. Layout (px, 1280 × 720, margem 16, sem rolagem)
Faixa comum (2 páginas): título 16,16 588×64 · Ano 620,16 · Mês 784,16 · Dia 948,16 · **Turno 1112,16** (152×64 cada) ·
rodapé 16,672 576×32 · navegador 608,672 368×32 · carimbo `Dado Atualizado até` 992,672 272×32.

Página 1 "Fluxo · Etapas":

| Visual | X | Y | L | A |
|---|---|---|---|---|
| Cartão novo, 9 KPIs `Fluxo · ...` | 16 | 92 | 1248 | 96 |
| `cartao_1` Tubo · `cartao_2` Trançagem · `cartao_3` Espiral · `cartao_4` Cobertura | 16 · 331 · 646 · 961 | 200 | 303 | 206 |
| `cartao_5` Bandagem · `cartao_6` Vulcanização · `cartao_7` Debandagem · `cartao_8` Cabine | 16 · 331 · 646 · 961 | 418 | 303 | 206 |
| Legenda | 16 | 636 | 1248 | 24 |

Cada cartão é uma tabela com 1 medida `Fluxo · SVG n Etapa` (imagem 272 × 184, cabeçalho invisível: fonte 1 na cor do
fundo). SVG: "ETAPA n", nome, ícones de pessoa (até 12, cinza até o máximo do dia, "+N"), pessoas/dia e máx, ícones de
carretel (dois flanges e núcleo, azul `#2A78D6`/apagado `#CFD6DF`, o último pela fração, até 12 e "+N"),
"X carretéis/dia · Y por pessoa" (ou "n/d"), fatia coberta quando < 100%, barra de m/dia (escala = maior etapa) e
caixa de m/pessoa com pessoas por 1.000 m. Borda e selo laranja "mais gente/metro" nas 2 etapas com mais gente por
1.000 m; as demais com caixa verde.

Página 2 "Fluxo · Mão de obra":

| Visual | X | Y | L | A |
|---|---|---|---|---|
| Tabela com `Fluxo · SVG Conteúdo` (1 SVG com as 8 barras, título e tracejado da média; imagem 560 × 286) | 16 | 92 | 616 | 340 |
| Tabela `Fluxo · Leitura Automática` (quebra de linha, fonte 11) | 648 | 92 | 616 | 340 |
| Colunas: metros/dia por mês (trançagem + espiral azul, cabine laranja) | 16 | 444 | 616 | 216 |
| Colunas: pessoas/dia por mês | 648 | 444 | 616 | 216 |

## 7. Validação
**Estática (o script, sempre):** JSON válido; campos no TMDL do snapshot ou já usados pelas páginas atuais do
`GMS_Painel` (caso da `fHoraHora[Turno]`, que o snapshot não tem); nível de hierarquia existe no TMDL; medidas do
relatório existem e são chamadas com `Schema: extension`; nomes únicos (medidas e visuais); DAX com parênteses,
chaves, colchetes e aspas balanceados, VAR só no padrão `__Nome`, **nenhuma VAR repetida na medida (sem diferenciar
maiúsculas) nem com nome de tabela do modelo** (também na tabela por etapa da conferência), colunas da ficha existentes, nenhuma chamada a outra
medida do relatório, leitura de `ISFILTERED ( fHoraHora[Turno] )` em toda medida que filtra turno, sem `Turno_*` nem
`Etapas`; tudo dentro de 1280 × 720 com margem 16, laterais simétricas, sem sobreposição; segmentação Turno nas 2
páginas com o mesmo `syncGroup`; SVG cabe no visual; idempotência (nova geração não muda nenhum arquivo).

**No Desktop (William):**
1. Abrir `GMS/PowerBI/Painel_PBIP_teste/GMS_PainelTeste.pbip`. Se reclamar do `reportExtensions.json`, a mensagem diz a
   medida e a posição do erro: me passe o texto.
2. Conferir que as 9 medidas SVG aparecem como imagem (senão, categoria URL da imagem à mão).
3. Exibição de consulta DAX → colar `Consulta_Conferencia_v2.dax` → Executar. Esperado (dias ≤ 06/10/2026):
   - linha "Tranç+Esp com máquina lixo" ≈ Trançagem do piloto (6.654 m/dia · 6,8 pessoas); Trançagem e Espiral dos
     cartões somam um pouco menos (sem a máquina lixo); Cabine ≈ 5.508 m/dia e 4,8 pessoas;
   - consulta 2: a leitura automática não aponta "Espiral" como restrição (piloto: Debandagem); eficiência na série de 7;
   - consulta 3 (turno 1): cabine ≈ 1.920 m/dia e ≈ 1,6 pessoa; dias produtivos iguais aos da consulta 1.

**Teste no Desktop de 04/11 (1ª geração):** KPIs, gráficos mensais (eixo hierárquico) e leitura calcularam; Turno
apareceu. Os 8 cartões e o SVG de conteúdo falharam por VAR repetida (`__La`/`__LA`): corrigido na 2ª geração, que
também passou restrição, balanceamento e conteúdo médio para a série de 7. Falta reabrir e conferir.
4. Performance Analyzer nas 2 páginas (seção 8).
5. Segmentações: trocar de página mantém Ano, Mês, Dia e Turno; dia sem produção apaga cartões e KPIs.

## 8. Riscos
- **Desempenho:** cada medida relê a ficha inteira (8 leituras com normalização de nome) e não reaproveita a das
  outras; a página 1 dispara 9 KPIs + 8 cartões. Com ~3 mil fichas deve ficar em segundos, mas é medido no Desktop.
  Se passar de ~3 s por visual, o caminho é levar o núcleo para o modelo (tabela `fPessoasEtapaOP` do piloto), o que é
  mudança de modelo e precisa do "sim" do William.
- **Sintaxe do `reportExtensions.json`:** medidas longas (até ~25 mil caracteres) com quebras de linha. O núcleo
  (inclusive `PATHITEM`/`GENERATE` das pessoas) já calculou no Desktop nos KPIs; o SVG (laços `CONCATENATEX`,
  gradientes) e o `dataCategory` ImageUrl só serão provados na próxima abertura. O script garante JSON, balanceamento
  e nomes únicos, não a semântica do DAX.
- Hierarquia de datas automática e `fHoraHora[Turno]` vêm do modelo ao vivo (o snapshot de 18 dias não tem a
  `fHoraHora`); `quantidade_*` tratadas como número (double no TMDL).
- O cabeçalho da tabela fica "invisível" por fonte 1 e cor do fundo; se o Desktop impuser fonte mínima, sobra uma
  faixa de ~12 px (há folga de 8 px no cartão e 16 px no conteúdo).
