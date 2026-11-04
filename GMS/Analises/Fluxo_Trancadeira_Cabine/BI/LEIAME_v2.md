# Fluxo v2 (tubo → cabine, filtro de máquina, carretéis) no GMS_Painel · como gerar e conferir

Status (04/11/2026, 4ª geração): **gerado só na cópia local** `GMS/PowerBI/Painel_PBIP_teste` (fora do git). Nada foi
gravado no `GMS_Painel.Report`, no `Modelo_PBIP`, no `Modelo_PBIP_teste` nem no modelo publicado. Falta reabrir no
Desktop, rodar a conferência e a revisão (`revisor`, Opus: turno, máquina e contexto de filtro).
Plano: `PLANO_v2_tubo_espiral_carreteis.md` (a Espiral deixou de ser etapa e virou filtro de máquina: William, 04/11).

| Arquivo | O que é |
|---|---|
| `gerar_medidas_paginas_fluxo.py` | gera as medidas do relatório e as 2 páginas na cópia, grava a consulta de conferência e valida |
| `Consulta_Conferencia_v2.dax` | **gerado** pelo script (não editar): 5 EVALUATE para rodar no Desktop |
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
- **Medida do relatório não pode chamar outra medida do relatório** (erro semântico no serviço). Cada medida
  `Fluxo · ...` é escrita por extenso a partir do mesmo núcleo DAX, montado pelo script (`nucleo()`): uma regra mudou,
  muda no script e regera tudo. Nunca edite a medida à mão no Desktop.
- Prefixo `Fluxo · ` em todas (23 medidas); a validação confere colisão com o TMDL e com as medidas do relatório.
- SVG: `dataType` Text com `dataCategory` = `ImageUrl` (se o Desktop não aceitar a categoria pelo arquivo, marcar à mão:
  Ferramentas de medida → Categoria de dados → URL da imagem).
- **Nomes de VAR:** o DAX não diferencia maiúsculas e recusa repetir um nome na mesma medida, mesmo em escopo aninhado
  (erro do Desktop em 04/11: `__La` da paleta × `__LA` do núcleo). O script dá nome único a cada VAR (sufixo por fonte:
  `__qS1`, `__fLT`, `__mqS2`, `__cvS7Car`…; cores `__cor...`; laços `__iPe`, `__iCa`) e a validação falha listando,
  por medida, as VAR repetidas e as que têm nome de tabela do modelo.

## 3. Regras de cálculo (todas direto da `ficha_producao` e do `dCalendario`)
- **Etapas em série (7):** Tubo, Trançagem, Cobertura, Bandagem, Vulcanização, Debandagem, Cabine (Extração/Teste).
  **Mandril fora.** A Espiral **não é etapa**: é uma máquina da Trançagem e entra pelo filtro de máquina (seção 5).
  Restrição, eficiência de balanceamento, conteúdo médio, rendimento e WIP usam as 7.
- **Dia** = data do fim da etapa menos 05:20. **Dia produtivo** = Trançagem da **linha inteira** (toda máquina, todo
  turno) ≥ 3.000 m no dia. Turno e máquina escolhidos não mudam os dias; as médias são do recorte nesses dias. Com 1
  dia filtrado, ele entra sempre se houver apontamento.
- **Contexto:** as seleções (datas do `dCalendario`, turnos da `fHoraHora[Turno]`, máquinas da
  `ficha_producao[Trançadeira]`) são guardadas em VAR antes de tudo; a ficha é lida com `ALL ( ficha_producao )`
  (ignora o relacionamento ativo `DataProducao → dCalendario` e a própria segmentação de máquina); o dia é a data de
  referência calculada na medida, e turno e máquina são reaplicados por linha.
- **Quantidade** > 2.000 m por ficha e etapa = erro de digitação, vira vazio (a pessoa continua contada).
- **Pessoas** = operadores distintos normalizados (maiúsculas, sem acento, sem `.`, `,`, `-`, `_`, espaço único) por
  dia e etapa; "A / B" conta 2 pessoas. Média nos dias produtivos (dia sem apontamento conta 0). "pessoas no trecho" =
  soma das 7 etapas (a mesma pessoa em 2 etapas conta nas 2).
- **Carretéis** por ficha = metros ÷ metros do carretel da `Bitola`: 4 → 800 · 6 → 680 · 8 → 680 · 10 → 460 ·
  12 → 400 · 16 → 250. Bitola fora da tabela (7, 3, 5, 17, vazia): os metros contam, o carretel fica **n/d** e o
  cartão mostra a fatia coberta ("carretéis em 96% dos metros"). Carretéis/dia = média dos dias produtivos; por pessoa
  = carretéis/dia ÷ pessoas/dia.
- KPIs: vazão, m/pessoa, pessoas por 1.000 m, eficiência de balanceamento (Σ conteúdo ÷ (n × maior), 7 etapas),
  restrição (menor m/dia), lead time (mediana única por ficha, fim da trançagem → fim da cabine, 0,5 a 720 h, fichas
  que saíram da cabine em dia produtivo), WIP de Little (vazão da cabine por dia de calendário × lead time médio ÷ 24),
  CV da vazão da Trançagem, rendimento (cabine ÷ trançagem). Destaque "mais gente/metro" = as 2 etapas de maior
  conteúdo entre as 7.
- Leitura automática: com filtro de máquina, abre com "Filtro de máquina: TH05, SPIRAL. Cada ficha que passou nessa(s)
  máquina(s) entra com o fluxo inteiro dela…"; depois restrição, mão de obra (comparada com a média das 7), balanceamento
  ("Cada etapa tem uma natureza de trabalho; a diferença só vira espaço de realocação onde há ociosidade."), Little e
  aviso de dia único. O nome da Trançagem no texto segue o filtro (Trançagem + Espiral / Trançagem / Espiral).

## 4. Turno (segmentação `fHoraHora[Turno]`)
- O modelo ao vivo não tem `dTurno`. A segmentação **Turno** usa **`fHoraHora[Turno]`**, a mesma coluna da página
  Hora-Hora (grupo de sincronização próprio `fluxo_turno`).
- As medidas só **leem** a escolha: `ISFILTERED ( fHoraHora[Turno] )` e os turnos escolhidos (sem o filtro de data),
  convertidos em {1, 2, 3} pelo **primeiro algarismo 1, 2 ou 3** do texto. Sem filtro direto, nenhum turno é aplicado.
- O turno é aplicado **por linha de ficha**, pela hora do **fim** de cada etapa: 05:20–13:56 = 1; 13:57–22:19 = 2;
  22:20–05:19 = 3 (minutos 320/837/1340, norma). Lead time e Little: fichas que saíram da cabine no turno.
- Não usa `ficha_producao[Turno_*]`, `Turno_Producao` nem `Etapas[Turno]` (a validação recusa).
- **Dependência:** `fHoraHora[Turno]` precisa existir no modelo ao vivo (existe: a página Hora-Hora usa) e ter linhas
  nas datas escolhidas. A lista mostra só os turnos com Hora-Hora no período.

## 5. Máquina (segmentação `ficha_producao[Trançadeira]`)
- Segmentação **Máquina** (lista suspensa, várias escolhas, "Selecionar tudo", sem "(Em branco)") sobre a coluna
  existente `ficha_producao[Trançadeira]`, sincronizada nas 2 páginas (`fluxo_maquina`).
- As medidas leem `ISFILTERED ( ficha_producao[Trançadeira] )` e os valores escolhidos com `FILTERS` (só a escolha da
  segmentação, sem o filtro cruzado das datas), **em VAR antes de limpar a ficha** com `ALL`. Cada valor e a máquina de
  cada ficha são **normalizados** (maiúsculas, sem ponto, hífen, espaço e sublinhado); `SPIRAL`, `TE01` e `TE0` viram a
  mesma máquina `SPIRAL`; as demais ficam como estão (TH01–TH07, TM01, TM04, TO04…).
- O filtro vale **por ficha em todas as etapas**: a ficha que passou na máquina escolhida carrega o fluxo inteiro dela
  (tubo, cobertura, …, cabine). Sem filtro direto, **todas** as fichas entram, inclusive máquina vazia/lixo: os números
  sem filtro são os mesmos da 2ª geração (cabine ≈ 5.679 m/dia, pessoas 6,7 / 4,9; trançagem ≈ 6.055 + 669 ≈ 6.724).
- Título do cartão 2: **"Trançagem + Espiral"** sem filtro (ou com braiders e espiral), **"Trançagem"** sem espiral
  escolhida, **"Espiral"** só com a espiral. O 8º cartão (Linha) mostra a máquina escolhida ou "todas".
- **Botões rápidos por favoritos (Com/Sem/Só Spiral): não feitos.** O favorito em PBIR (`definition/bookmarks`) guarda o
  estado da segmentação pelo nome do visual e um filtro com os valores literais da coluna (`explorationState`); a cópia
  do `GMS_Painel` não tem pasta de favoritos e os valores exatos da coluna (grafias de Spiral/TE01) só existem no modelo
  ao vivo. Formato incerto: o uso é pela segmentação (Sem Spiral = marcar os TH/TM/TO; Só Spiral = marcar Spiral, TE01,
  TE0). Se o William quiser os botões, o caminho seguro é criá-los à mão no Desktop e o script passar a preservá-los.
- A lista da segmentação segue as datas pela `DataProducao` (data civil da extração): ficha sem extração não aparece
  na lista quando há data escolhida (as máquinas se repetem, o efeito é pequeno).

## 6. Imagens SVG: visual Imagem nativo (sem o texto bruto ao passar o mouse)
- **Decisão (teste no Desktop, 04/11):** os 9 SVG (7 cartões, Linha e a barra de conteúdo) ficam em **visual Imagem
  nativo** (`visualType` `image`), com `objects.image` = `sourceType` `'imageUrl'` e `sourceUrl` = a medida SVG por
  formatação condicional (fx → valor do campo, medida do relatório com `Schema: extension`), dica de ferramenta desligada
  (`visualContainerObjects.visualTooltip.show = false`). Sem modo de ajuste: o SVG traz `width`/`height` iguais ao
  tamanho do visual e `viewBox` com o desenho na mesma proporção, então preenche o visual sem sobra nem corte.
- **Por quê:** em **tabela/matriz**, passar o mouse na célula mostra o texto bruto `data:image/svg+xml…` — é o atributo
  `title` nativo da **célula**, não a dica de ferramenta do Power BI, e `visualTooltip.show = false` não resolve. O
  **cartão novo** (`cardVisual`), com a imagem pela URL ou só com o valor ImageUrl, também mostrou o texto bruto. A
  página de teste `pg_teste_tooltip` (4 variantes: cartão novo com imagem, cartão novo só valor, Imagem nativa, tabela)
  foi removida; o gerador a apaga se ainda existir.
- O esquema oficial (`formattingObjectDefinitions` 1.5.0) não lista as propriedades por tipo de visual: os nomes
  `sourceType`/`sourceUrl` foram provados no Desktop, não no esquema. A validação exige o visual Imagem com essas
  propriedades, a medida SVG existente, a dica desligada e o tamanho do SVG igual ao do visual.
- A Leitura automática continua em tabela (é texto, o `title` da célula repete o próprio texto).

## 7. Limites (o que não dá sem mexer no modelo)
- **Sem Mês/Ano:** os gráficos mensais usam a hierarquia de datas automática do `dCalendario[Date]` (Ano e Mês,
  expandidos). Se o modelo publicado não tiver data/hora automática para o `dCalendario`, os 2 gráficos quebram.
- **Sem `dTurno`:** turno pela `fHoraHora[Turno]` (seção 4).
- **n/d de bitola:** carretéis só onde a bitola está na tabela; a fatia coberta aparece no cartão.
- **Mês da segmentação** em ordem alfabética (`dCalendario[Mês]` sem classificar por `Mês Nº`; pendência antiga).
- **Navegadores das páginas antigas** mostram todas as páginas: com 2 páginas a mais podem apertar os botões delas.

## 8. Layout (px, 1280 × 720, margem 16, sem rolagem)
Faixa comum (2 páginas): título 16,16 568×64 · Ano 596 · Mês 732 · Dia 868 · Turno 1004 · **Máquina 1140** (y 16,
124×64 cada) · rodapé 16,672 576×32 · navegador 608,672 368×32 · carimbo `Dado Atualizado até` 992,672 272×32.

Página 1 "Fluxo · Etapas":

| Visual | X | Y | L | A |
|---|---|---|---|---|
| Cartão novo, 9 KPIs `Fluxo · ...` | 16 | 92 | 1248 | 96 |
| `cartao_1` Tubo · `cartao_2` Trançagem · `cartao_3` Cobertura · `cartao_4` Bandagem | 16 · 331 · 646 · 961 | 200 | 303 | 205 |
| `cartao_5` Vulcanização · `cartao_6` Debandagem · `cartao_7` Cabine · `cartao_linha` Linha | 16 · 331 · 646 · 961 | 417 | 303 | 205 |
| Legenda | 16 | 634 | 1248 | 26 |

Cada cartão é um visual Imagem com a medida `Fluxo · SVG n Etapa` (SVG 303 × 205, desenho 272 × 184 na mesma
proporção, sem dica de ferramenta; seção 6): "ETAPA n", nome, ícones de pessoa (até 12, cinza até o máximo do dia, "+N"), pessoas/dia e máx, ícones de
carretel (dois flanges e núcleo, azul `#2A78D6`/apagado `#CFD6DF`, o último pela fração, até 12 e "+N"),
"X carretéis/dia · Y por pessoa" (ou "n/d"), fatia coberta quando < 100%, barra de m/dia (escala = maior etapa) e caixa
de m/pessoa com pessoas por 1.000 m. Borda e selo laranja "mais gente/metro" nas 2 etapas com mais gente por 1.000 m.
**Linha** (`Fluxo · SVG Linha`, 8º slot): m/dia na cabine, carretéis/dia na cabine, pessoas/dia nas 7 etapas, dias
produtivos e máquina do filtro.

Página 2 "Fluxo · Mão de obra":

| Visual | X | Y | L | A |
|---|---|---|---|---|
| Visual Imagem com `Fluxo · SVG Conteúdo` (SVG 616 × 340 com o cartão branco, as 7 barras, título e tracejado da média) | 16 | 92 | 616 | 340 |
| Tabela `Fluxo · Leitura Automática` (quebra de linha, fonte 11) | 648 | 92 | 616 | 340 |
| Colunas: metros/dia por mês (trançagem azul, cabine laranja) | 16 | 444 | 616 | 216 |
| Colunas: pessoas/dia por mês | 648 | 444 | 616 | 216 |

## 9. Validação
**Estática (o script, sempre):** JSON válido; campos no TMDL do snapshot ou já usados pelas páginas atuais do
`GMS_Painel` (caso da `fHoraHora[Turno]`); nível de hierarquia existe no TMDL; medidas do relatório existem e são
chamadas com `Schema: extension`; nomes únicos (medidas e visuais); DAX balanceado, VAR só no padrão `__Nome`,
**nenhuma VAR repetida na medida (sem diferenciar maiúsculas) nem com nome de tabela**, colunas da ficha existentes,
nenhuma chamada a outra medida do relatório, `ISFILTERED ( fHoraHora[Turno] )` **e** `ISFILTERED`/`FILTERS` da
`ficha_producao[Trançadeira]` com o filtro por ficha em toda medida que soma, sem `Turno_*` nem `Etapas`, nenhuma medida
de "Espiral" como etapa; tudo em 1280 × 720 com margem 16, laterais simétricas, sem sobreposição; segmentações **Turno e
Máquina** nas 2 páginas com o mesmo `syncGroup`; **todo SVG em visual Imagem (`image.sourceType` `'imageUrl'`,
`image.sourceUrl` = medida), nenhum em tabela, dica desligada, `width`/`height` do SVG = tamanho do visual e mesma
proporção do desenho**; página de teste ausente; idempotência.

**No Desktop (William):**
1. Abrir `GMS/PowerBI/Painel_PBIP_teste/GMS_PainelTeste.pbip` (ou "Aplicar alterações externas"). Erro no
   `reportExtensions.json`: a mensagem diz a medida e a posição; me passe o texto.
2. As 9 imagens SVG aparecem inteiras (visual Imagem) e não mostram texto nenhum ao passar o mouse.
3. Exibição de consulta DAX → colar `Consulta_Conferencia_v2.dax` → Executar (dias ≤ 06/10/2026):
   - consulta 1 (sem filtro): Cabine ≈ 5.679 m/dia e 4,9 pessoas; Trançagem ≈ 6.724 m/dia e 6,7 pessoas;
   - consulta 3 (turno 1): cabine ≈ 1.920 m/dia e ≈ 1,6 pessoa; dias produtivos iguais aos da consulta 1;
   - consulta 4 (só Spiral): Trançagem ≈ 669 m/dia; consulta 5 (sem Spiral): Trançagem ≈ 6.055 m/dia; dias iguais.
4. Segmentação Máquina: escolher só Spiral muda o título do cartão 2 para "Espiral" e a Linha mostra "máquina: SPIRAL".
5. Performance Analyzer nas 2 páginas (seção 10).

**Histórico dos testes no Desktop (04/11):** 1ª geração: KPIs, gráficos mensais (eixo hierárquico) e leitura
calcularam; os cartões e o SVG de conteúdo falharam por VAR repetida (`__La`/`__LA`), corrigido na 2ª. 3ª geração
Espiral virou filtro de máquina, 7 etapas + Linha (filtro, Linha, título dinâmico e totais conferidos no Desktop); o
texto bruto do SVG continuava (célula da tabela). Teste de 4 visuais: o visual Imagem nativo venceu. 4ª geração (esta):
os 9 SVG em visual Imagem. Falta reabrir e conferir.

## 10. Riscos
- **Desempenho:** cada medida relê a ficha inteira (7 leituras com normalização de nome e de máquina) e não reaproveita
  a das outras; a página 1 dispara 9 KPIs + 8 imagens. Com ~3 mil fichas deve ficar em segundos, mas é medido no
  Desktop. Se passar de ~3 s por visual, o caminho é levar o núcleo para o modelo (tabela `fPessoasEtapaOP` do piloto),
  mudança de modelo que precisa do "sim" do William.
- **Segmentação de máquina e o resto do modelo:** ela filtra a `ficha_producao` de verdade; as medidas Fluxo a leem e
  limpam, mas qualquer outro visual que um dia for posto nessas páginas sobre a ficha será filtrado também.
  Se o relacionamento `ficha_producao → dCalendario` for de 2 sentidos no modelo ao vivo, as datas são protegidas
  (`REMOVEFILTERS ( ficha_producao[Trançadeira] )` na captura das datas).
- **Sintaxe do `reportExtensions.json`:** medidas longas (até ~26 mil caracteres). O núcleo já calculou no Desktop nos
  KPIs; `FILTERS` sobre a coluna da ficha, o nome dinâmico do cartão 2 e `visualTooltip` só serão provados na próxima
  abertura. O script garante JSON, balanceamento e nomes únicos, não a semântica do DAX.
- **Visual Imagem com URL por medida:** provado no Desktop com o cartão Tubo; nos outros 8 é a mesma técnica. O visual
  Imagem não tem estado de "sem dados": medida em branco deixa o espaço vazio (é o esperado).
- Hierarquia de datas automática e `fHoraHora[Turno]` vêm do modelo ao vivo (o snapshot de 18 dias não tem a
  `fHoraHora`); `quantidade_*` tratadas como número (double no TMDL).
