# Páginas-piloto "Fluxo Trançagem → Cabine": como montar e conferir · v0.2 (revisão aplicada)

Arquivos desta pasta:

| Arquivo | O que é |
|---|---|
| `Medidas_FluxoTrancagemCabine.md` | Bloco 0 (funções e `dTurno`, só se faltarem), Bloco 1 (`dEtapa` e `fPessoasEtapaOP`), Bloco 2 (relacionamentos), Bloco 3 (medidas) e a DECISÃO sobre `Etapas` × tabela nova |
| `Medidas_SVG_FluxoTrancagemCabine.md` | Bloco 4: cartões SVG por etapa (layout da `ilustracao_headcount.html`) e barras/ícones avulsos |
| `Tema_FluxoTrancagem.json` | tema escuro do piloto (padrão), paleta da ilustração |
| `Tema_FluxoTrancagem_Claro.json` | tema claro do piloto, paleta do `painel_template.html` |
| este LEIAME | onde montar, ordem de aplicação, layout das 2 páginas com X/Y/L/A e checklist de conferência |

## 1. Onde montar e qual tema

- **Relatório-piloto separado**, com conexão dinâmica ao modelo (GMS) (Obter dados → Modelos semânticos do Power BI →
  GMS). No Power BI o tema vale para o relatório inteiro, não por página. Importar este tema no `GMS_Painel`
  recoloriria as 6 páginas existentes, cujo layout salvo não pode mudar.
- **O piloto usa a paleta do HTML** aprovado (escuro da ilustração; claro do `painel_template.html`).
- **A versão final, quando for para o `GMS_Painel`, usa os tokens `fx_` da §B.6.1 no tema claro** (`GMS_Tema_BI.json`):
  série principal `fx_CorInfo #2C6FBF`, OK `#16A34A`, alerta `#E67E22`, erro `#C0392B`, fundo `#F5F7FA`, cartão
  `#FFFFFF`, texto `#0F172A`/`#64748B`, borda `#E2E8F0`. Contraste conferido sobre branco: `#2C6FBF` 5,1:1, `#C0392B`
  5,4:1 e `#64748B` 4,8:1 servem para texto. `#16A34A` (3,3:1), `#E67E22` (2,8:1) e `fx_CorRotulo #94A3B8` (2,6:1) só
  servem para barra, linha e borda. Nesses papéis, texto de estado usa o tom escuro: verde `#1E7B34`, laranja `#B83D0C`.
- **Claro/escuro automático não existe no Power BI.** O relatório não lê o modo do sistema (`prefers-color-scheme`):
  é um tema por relatório. Para trocar, importe o outro JSON e troque as cores das VARs das medidas SVG (tabela no fim
  do arquivo SVG). O selo laranja com texto escuro é o mesmo nos dois.

Contraste conferido nos dois temas do piloto (texto ≥ 4,5:1; série ≥ 3:1):

| | Escuro | Claro |
|---|---|---|
| Texto principal / rótulo sobre o cartão | 13,5 / 6,5 | 18,6 / 7,7 |
| good / neutral / bad como texto | 8,2 / 6,9 / 5,2 | 5,3 / 5,7 / 4,8 |
| Séries 1 a 5 sobre o cartão | 5,7 · 8,2 · 6,9 · 5,2 · 6,5 | 4,4 · 3,4 · 3,2 · 4,8 · 3,6 |
| SVG: suave, laranja e verde nas caixas, selo | 6,5 · 6,2 · 6,9 · 7,8 | 5,1 · 4,8 · 4,7 · 7,8 |

## 2. Ordem de aplicação

1. Modelo (GMS), TMDL view: **Bloco 0** só com o que faltar (`fn_MinutoDoDia`, `fn_Turno`, `fn_DataRef`, `dTurno`).
2. **Checar o fuso** (seção "Fuso" do arquivo de medidas) e ajustar `FichaJaEmHoraLocal` se precisar.
3. **Bloco 1** → Aplicar → **Atualizar** o modelo. **Bloco 2** → Aplicar.
4. **Bloco 3** e **Bloco 4** → Aplicar. Conferir que as 4 medidas `SVG ...` ficaram com Categoria de dados = **URL da imagem**.
5. Relatório-piloto: **Exibir → Temas → Procurar temas → `Tema_FluxoTrancagem.json`**.
6. Criar as 2 páginas, cada uma com **Formatar página → Configurações da tela: 16:9, 1280 × 720**.
7. Montar os visuais das seções 3 e 4. Depois, **Exibir → Sincronizar segmentações**: Ano, Mês, Dia e Turno
   sincronizados **e** visíveis nas 2 páginas do piloto (mesmo grupo de sincronização).
8. Rodar a conferência da seção 6 antes de mostrar para alguém.

## 3. Layout (px; Formatar → Geral → Propriedades → Tamanho e posição)

Grade de 16 px, largura útil 1248. Segmentações e rodapé **nas mesmas posições nas duas páginas** (§B.6.5).

### Faixa comum (as duas páginas)

| Visual | Campos | X | Y | L | A |
|---|---|---|---|---|---|
| Caixa de texto (título) | texto fixo, ver 5.1 | 16 | 16 | 588 | 56 |
| Segmentação Ano | `dCalendario[Ano]` | 620 | 16 | 152 | 56 |
| Segmentação Mês | `dCalendario[Mês]` (classificado por `Mês Nº`) | 784 | 16 | 152 | 56 |
| Segmentação Dia | `dCalendario[Dia]` | 948 | 16 | 152 | 56 |
| Segmentação Turno | `dTurno[Rótulo]` (classificado por `Turno`) | 1112 | 16 | 152 | 56 |
| Caixa de texto (rodapé: definição) | texto fixo, ver 5.6 | 16 | 676 | 720 | 28 |
| Navegador de páginas | Inserir → Botões → Navegador → Navegador de página (só as 2 páginas do piloto) | 752 | 672 | 224 | 36 |
| Cartão (carimbo de atualização) | medida `Dado Atualizado até` (a que as outras páginas já usam) | 992 | 676 | 272 | 28 |

### Página 1 — "Fluxo · Etapas" (título, segmentações, KPIs, cartões)

| Visual | Campos | X | Y | L | A |
|---|---|---|---|---|---|
| Cartão (novo), 9 medidas | ver 5.3 | 16 | 88 | 1248 | 104 |
| Matriz dos 6 cartões de etapa | `dEtapa[Etapa no Fluxo]` em Colunas, `SVG Cartão Etapa` em Valores | 16 | 208 | 1248 | 372 |

Visuais de análise: 2 (limite da §B.6.3: 8).

### Página 2 — "Fluxo · Mão de obra" (conteúdo, leitura, gráficos)

| Visual | Campos | X | Y | L | A |
|---|---|---|---|---|---|
| Tabela de conteúdo de mão de obra | `dEtapa[Etapa no Fluxo]`, `SVG Conteúdo` | 16 | 88 | 616 | 300 |
| Tabela da leitura automática | `Leitura Automática` (uma coluna) | 648 | 88 | 616 | 300 |
| Gráfico de linhas: metros por dia | eixo `dCalendario[Date]`; `Metros Trançagem no Dia`, `Metros Cabine no Dia` | 16 | 404 | 616 | 256 |
| Gráfico de linhas: pessoas por dia | eixo `dCalendario[Date]`; `Pessoas Trançagem no Dia`, `Pessoas Cabine no Dia` | 648 | 404 | 616 | 256 |

Visuais de análise: 4.

## 4. Turno nas medidas

- A `fPessoasEtapaOP` leva `Turno` (pela `fn_Turno`) e liga em `dTurno`. O turno é o do **fim** da etapa.
- **O dia produtivo continua sendo do dia inteiro** (Trançagem ≥ 3.000 m somando os 3 turnos). Com um turno escolhido,
  vazão, pessoas e conteúdo são a média daquele turno nos dias produtivos. Sem isso quase nenhum dia passaria do corte
  num turno só.
- Lead time com turno: fichas que saíram da cabine naquele turno.
- Para conferir contra o HTML (seção 6), Turno = Selecionar tudo.

## 5. Configuração de cada visual

### 5.1 Título
Página 1: "Fluxo da trançagem até a cabine · etapas". Página 2: "Fluxo da trançagem até a cabine · mão de obra e evolução".
Linha 2 nas duas: "Fonte: ficha de produção · dia produtivo de 05:20 a 05:20 · médias dos dias com trançagem ≥ 3.000 m"
(Segoe UI 11, cor suave). Linha 1 em Segoe UI Semibold 20. Sem fundo e sem borda (Formatar → Geral → Efeitos).

### 5.2 Segmentações (Ano, Mês, Dia, Turno)
- Estilo **Lista suspensa**. Cabeçalho ligado ("Ano", "Mês", "Dia", "Turno"), Segoe UI 10, cor suave.
- **Seleção única desligada** e **"Mostrar opção Selecionar tudo" ligada** (equivale ao "Todos" do HTML).
- Fundo, borda de 1 px e cantos de 12 vêm do tema.
- Sincronizar só entre as 2 páginas do piloto (passo 7 da seção 2).
- `Dia` é o dia do mês. Com Mês = Todos, escolher "15" pega todo dia 15, mesmo efeito do HTML.

### 5.3 Cartão dos KPIs (página 1)
Visual **Cartão** (o novo, com várias medidas). Layout horizontal, 9 por linha. Renomeie cada campo para este visual:

| Ordem | Medida | Rótulo no cartão | Rótulo de referência |
|---|---|---|---|
| 1 | `Vazão Cabine (m/dia)` | m/dia na cabine | vazão da linha (TH) |
| 2 | `Pessoas por Dia no Trecho` | pessoas somando as 6 etapas | por dia, média |
| 3 | `Pessoas Trançagem / Cabine` | pessoas: trançagem / cabine | média diária |
| 4 | `m por Pessoa Cabine` | m por pessoa na cabine | produtividade da mão de obra |
| 5 | `Eficiência de Balanceamento` | eficiência de balanceamento | `Perda de Balanceamento` |
| 6 | `Lead Time Tranç→Cabine (h)` | lead time trançagem→cabine (h) | mediana por ficha |
| 7 | `WIP Little (m)` | m em processo (Little) | vazão de calendário × lead time médio |
| 8 | `CV Vazão Trançagem` | variabilidade (CV) da vazão | trançagem, entre dias |
| 9 | `Rendimento de Fluxo` | rendimento de fluxo | cabine ÷ trançagem |

Valor em Segoe UI Semibold 24, rótulo em Segoe UI 10 na cor suave. Sem dado, o cartão fica em branco (nunca 0).
Texto alternativo: "Nove indicadores do trecho trançagem→cabine no filtro escolhido."

### 5.4 Matriz dos cartões (página 1)
Passo a passo em `Medidas_SVG_FluxoTrancagemCabine.md` ("Montar os 6 cartões"). Resumo: filtro do visual
`Trecho Tranç-Cabine` = Verdadeiro; subtotais desligados; grade desligada; **Tamanho da imagem 304 (altura) × 208
(largura)**; preenchimento 0, sem fundo e sem borda; título por fx = `Título Cartões`. Etapa sem apontamento e com
0 m no filtro some (BLANK).
Texto alternativo: "Seis cartões, da trançagem à cabine: pessoas por dia, metros por dia e pessoas a cada 1.000 m de cada etapa."

### 5.5 Página 2
- **Tabela de conteúdo:** colunas `Etapa no Fluxo` (largura 130) e `SVG Conteúdo` (renomear para
  "Pessoas a cada 1.000 m"). Tamanho da imagem 32 × 440. Classificar por `Etapa no Fluxo` crescente (ordem física do
  fluxo). Filtro do visual `Trecho Tranç-Cabine` = Verdadeiro. Título por fx = `Título Conteúdo`.
  Texto alternativo: "Pessoas a cada 1.000 m por etapa; laranja são as duas etapas com mais gente por metro; tracejado é a média."
- **Leitura automática:** visual **Tabela** com **uma coluna só**, a medida `Leitura Automática` (renomear para
  "Leitura automática"). Valores: **Quebra automática de texto ligada**, Segoe UI 12; largura da coluna 584; grade
  desligada; totais desligados. A medida separa os parágrafos com quebra de linha (`UNICHAR(10)`), que a tabela mostra
  com a quebra automática ligada. Sem dado: "Sem dados no filtro."
- **Linha, metros por dia:** título "Quanto a trançagem e a cabine fazem por dia (m)?". Eixo X `dCalendario[Date]`
  **contínuo**, sem hierarquia; Y a partir de 0; marcadores desligados. Trançagem = cor 1 do tema (azul), cabine = cor 2 (verde).
- **Linha, pessoas por dia:** título "Quantas pessoas a trançagem e a cabine usam por dia?". Trançagem = cor 3 do
  tema (laranja), cabine = cor 2 (verde).
- Dia fora da média (trançagem < 3.000 m) fica em branco nas séries, como no HTML. Com um dia só escolhido, ele aparece.
- Cor só pelo tema (escolher a cor do tema no seletor, nunca digitar hex). O SVG é a única exceção.

### 5.6 Rodapé
Texto fixo (Segoe UI 9, cor suave): "Pessoas = operadores distintos que apontaram a etapa no dia (estimativa, não é
escala oficial)." Carimbo `Dado Atualizado até` ao lado, Segoe UI 9, sem rótulo de categoria (§B.8.3).

## 6. Checklist de validação

### 6.1 Antes dos números
- [ ] `fPessoasEtapaOP` atualizou sem erro. Contagem: para cada etapa, linhas = fichas da `ficha_producao` com
      `data_hora_final_<etapa>` preenchido (não há junção).
- [ ] **Fuso:** uma ficha conhecida no app (Consulta OP) tem o mesmo `Fim da Etapa` na `fPessoasEtapaOP`. Diferença de
      3 h a mais = `FichaJaEmHoraLocal` deveria ser `false`. Diferença de 3 h a menos = deveria ser `true` (converteu duas vezes).
- [ ] Virada das 05:20 (§B.9.3): fim às 05:19 cai na `Data de Referência` do dia anterior; às 05:21, no próprio dia.
      Turno: 05:19 → 3; 05:21 → 1; 13:57 → 2; 22:20 → 3.
- [ ] `Quantidade (m)`: a soma da Trançagem de um dia bate com o rodapé do app (texto "1.200" tem de virar 1.200 m, não 1,2).
- [ ] As 4 medidas SVG aparecem como imagem (se aparecer o texto `data:image...`, falta a categoria URL da imagem).

### 6.2 Mesmo período do HTML
O HTML tem dados de **03/12/2025 a 06/10/2026**. Para comparar, ponha no painel de filtros das duas páginas um filtro
temporário `dCalendario[Date]` entre essas datas, segmentações em "Selecionar tudo" (Turno incluído). Tire o filtro depois.

### 6.3 Conferência 1:1 (pasta `Auxiliares\Conferência Fluxo Tranç→Cabine`, dia pela data civil do fim, igual ao HTML)
Arraste num cartão provisório. Tem de bater com o HTML (tolerância: arredondamento, e até ±0,05 pessoa porque o BI
tira espaço sobrando do nome do operador e o HTML não):

| HTML (todos os dias) | Medida de conferência | Esperado |
|---|---|---|
| cabine 5.499 m/dia | `Conf HTML · Vazão Cabine (m/dia)` | 5.499 |
| pessoas 6,9 / 5,0 | `Conf HTML · Pessoas Trançagem / Cabine` | 6,9 / 5,0 |
| eficiência 57% | `Conf HTML · Eficiência de Balanceamento` | 57,5% |
| lead time 31 h (média das medianas diárias) | `Conf HTML · Lead Time (h)` | 31,4 |
| WIP ~7.196 m (fórmula do HTML) | `Conf HTML · WIP Little (m)` | 7.196 |
| CV 23% | `Conf HTML · CV Vazão Trançagem` | 22,6% |
| rendimento 85% | `Conf HTML · Rendimento de Fluxo` | 84,7% |

Se essas não baterem, o problema está na `fPessoasEtapaOP` (fuso, tipo, coluna faltando), não na regra do dia.

### 6.4 Números oficiais das páginas (Data de Referência 05:20; lead time e WIP corrigidos)
Simulados com o mesmo CSV do HTML. São estes que as páginas mostram (Turno = todos):

| KPI | HTML | Páginas do BI | O que muda |
|---|---|---|---|
| Dias produtivos | 184 | 185 | regra do dia |
| Vazão cabine (m/dia) | 5.499 | ≈ 5.296 | regra do dia |
| Vazão trançagem (m/dia) | 6.489 | ≈ 6.472 | regra do dia |
| Pessoas trançagem / cabine | 6,9 / 5,0 | ≈ 6,9 / 4,9 | regra do dia |
| Pessoas somando as 6 etapas | 22,2 | ≈ 21,9 | regra do dia |
| m por pessoa na cabine | 1.091 | ≈ 1.089 | regra do dia |
| Eficiência de balanceamento | 57% | ≈ 58% | regra do dia |
| **Lead time** | 31 h (média das medianas diárias) | **≈ 22 h** (mediana única, K07/C4) | método |
| **WIP de Little** | 7.196 m | **≈ 5.013 m** (3.398 m/dia de calendário × 35,4 h médio ÷ 24) | método |
| CV da vazão da trançagem | 23% | ≈ 22,5% | regra do dia |
| Rendimento de fluxo | 85% | ≈ 82% | regra do dia |
| Menor vazão / maior conteúdo | Debandagem / Trançagem | Debandagem / Trançagem | — |
| Cartões laranja | Trançagem e Cabine | Trançagem e Cabine | — |

Cartões de etapa esperados (Data de Referência, mesmo período):

| Etapa | m/dia | pessoas/dia | máx | m/pessoa | pessoas por 1.000 m |
|---|---|---|---|---|---|
| Trançagem | ≈ 6.472 | 6,9 | 11 | ≈ 938 | 1,07 |
| Cobertura | ≈ 6.364 | 2,7 | 6 | ≈ 2.369 | 0,42 |
| Bandagem | ≈ 6.126 | 3,2 | 8 | ≈ 1.905 | 0,53 |
| Vulcanização | ≈ 6.194 | 2,2 | 5 | ≈ 2.850 | 0,35 |
| Debandagem | ≈ 5.200 | 2,1 | 7 | ≈ 2.479 | 0,40 |
| Cabine (teste) | ≈ 5.296 | 4,9 | 12 | ≈ 1.089 | 0,92 |

**Por que muda:**
1. **Regra do dia.** O HTML conta o dia pela data civil do fim de cada etapa; o BI, pela `Data de Referência`
   (§A.3). 7,3% dos fins caem entre 00:00 e 05:20 e vão para o dia anterior. Com isso muda quais dias passam no corte
   de 3.000 m. Caso típico: cabine trabalhando de madrugada depois de um dia sem trançagem (domingo à noite, feriado).
   No BI esses metros caem num dia fora da média, a vazão da cabine cai uns 200 m/dia e o rendimento vai de 85% para
   82%. O operador do 3º turno que aponta antes e depois da meia-noite conta em dois dias no HTML e em um no BI; por
   isso a cabine vai de 5,0 para 4,9.
2. **Lead time.** O KPI agora é a mediana única de todas as fichas do período (K07/C4): ≈ 22 h nas duas regras de
   data. A média das medianas diárias do HTML (31 h) é sensível a dia com poucas fichas e ficou só em `Conferência`.
3. **WIP de Little.** λ = metros que saem da cabine por dia de calendário (fim de semana incluso) e W = lead time
   **médio** (35,4 h), não a mediana. O HTML usava a vazão só dos dias produtivos e a média das medianas, e chegava
   a 7.196 m. A fórmula correta dá ≈ 5.013 m.
4. **Período.** Sem o filtro da 6.2, o BI inclui os dias depois de 06/10 e todos os números mudam.

### 6.5 Comportamento dos filtros
- [ ] Dia sem produção: cartões somem, KPIs em branco, leitura "Sem dados no filtro."
- [ ] Dia com trançagem < 3.000 m: o dia entra (dia único sempre entra), a leitura mostra o aviso de dia único e o CV
      fica em branco.
- [ ] Turno escolhido: o número de dias produtivos não muda (o corte é do dia inteiro); metros e pessoas caem para os
      do turno; a soma dos 3 turnos da `Vazão Cabine` dá a vazão do dia inteiro (±arredondamento).
- [ ] Etapa sem apontamento no filtro (ex.: um turno sem cabine): o cartão dela some, não aparece zerado.
- [ ] Os 2 cartões laranja mudam conforme o filtro (sempre as 2 de maior conteúdo do recorte).
- [ ] Trocar de página mantém Ano, Mês, Dia e Turno (sincronização).

### 6.6 Checklist pré-publicação (§B.9) que se aplica aqui
- [ ] Zero agregação implícita: só medidas nos valores (`dEtapa`, `dCalendario` e `dTurno` só como eixo/categoria/segmentação).
- [ ] Formato pt-BR (milhar com ponto, decimal com vírgula) em cartões, tabelas e dicas de ferramenta.
- [ ] Contraste (tabela da seção 1) e texto alternativo em todos os visuais de análise.
- [ ] Performance Analyzer: a matriz dos cartões (6 SVG, cada um calcula a posição de conteúdo das 6 etapas) abaixo de ~3 s.
- [ ] Carimbo de atualização visível no rodapé das 2 páginas.
- [ ] Linhas de diário (fim de `Medidas_FluxoTrancagemCabine.md`) coladas depois de conferido; ID MEL real pelo `gms.py --novo`.

## 7. Pendências
- **`Etapas` × `fPessoasEtapaOP`:** o TMDL do modelo não está no repositório. Se a `Etapas` tiver operador, turno e
  data de referência por etapa, as medidas migram para ela (seção 0 do arquivo de medidas).
- **`dTurno`:** se a versão com chave de texto do `montagem_modelo.md` já foi aplicada, o Bloco 0/2 precisa de ajuste
  antes de colar.
- **Versão final no `GMS_Painel`:** trocar a paleta do piloto pelos tokens `fx_` no tema claro (seção 1) e decidir
  com o William se a página leva o tema escuro ou não.
