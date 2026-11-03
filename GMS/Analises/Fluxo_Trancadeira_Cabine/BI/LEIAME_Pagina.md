# Página-piloto "Fluxo Trançagem → Cabine": como montar e conferir

Arquivos desta pasta:

| Arquivo | O que é |
|---|---|
| `Medidas_FluxoTrancagemCabine.md` | Blocos 1–3 em TMDL: tabelas `dEtapa` e `fEtapaOP` (com o M), relacionamentos e as medidas dos KPIs |
| `Medidas_SVG_FluxoTrancagemCabine.md` | Bloco 4: cartões SVG por etapa (layout da `ilustracao_headcount.html`) e as barras/ícones avulsos |
| `Tema_FluxoTrancagem.json` | tema escuro (padrão da página) |
| `Tema_FluxoTrancagem_Claro.json` | mesmo tema com as cores claras do `painel_template.html` |
| este LEIAME | ordem de aplicação, layout com X/Y/L/A e checklist de conferência |

## 1. Onde montar

Num **relatório-piloto separado**, com conexão dinâmica ao modelo (GMS) (Obter dados → Modelos semânticos do Power BI → GMS).
Motivo: no Power BI o tema vale para o relatório inteiro, não por página. Importar o tema escuro no `GMS_Painel`
recoloriria as 6 páginas que já existem, e o layout salvo delas não pode mudar. Aprovado o piloto, a página é copiada
para o `GMS_Painel` com as cores postas à mão só nela (fundo da página e dos visuais), sem importar o tema lá.

**Claro/escuro automático não existe no Power BI.** O relatório não lê o modo do sistema
(`prefers-color-scheme`). Fica um tema por relatório: o escuro é o padrão. Para trocar, importe
`Tema_FluxoTrancagem_Claro.json` e troque as cores das VARs das medidas SVG (lista no fim do arquivo SVG), porque
imagem SVG não segue o tema.

## 2. Ordem de aplicação

1. Modelo (GMS), TMDL view: colar o **Bloco 1** (tabelas) → Aplicar → **Atualizar** o modelo.
2. Colar o **Bloco 2** (relacionamentos) → Aplicar.
3. Colar o **Bloco 3** (medidas) e o **Bloco 4** (SVG) → Aplicar.
4. Conferir que as 4 medidas `SVG ...` ficaram com Categoria de dados = **URL da imagem**.
5. Relatório-piloto: **Exibir → Temas → Procurar temas → `Tema_FluxoTrancagem.json`**.
6. **Formatar página → Configurações da tela**: Tipo **Personalizado**, **1280 × 1212**, alinhamento vertical em cima.
7. Montar os visuais da tabela da seção 3, na ordem.
8. Rodar a conferência da seção 5 antes de mostrar para alguém.

## 3. Layout (posições em px; Formatar → Geral → Propriedades → Tamanho e posição)

Grade de 16 px, largura útil 1248 px.

| # | Visual | Campos | X | Y | L | A |
|---|---|---|---|---|---|---|
| 1 | Caixa de texto (título) | texto fixo, ver 4.1 | 16 | 16 | 720 | 56 |
| 2 | Segmentação Ano | `dCalendario[Ano]` | 784 | 16 | 152 | 56 |
| 3 | Segmentação Mês | `dCalendario[Mês]` (classificado por `Mês Nº`) | 948 | 16 | 152 | 56 |
| 4 | Segmentação Dia | `dCalendario[Dia]` | 1112 | 16 | 152 | 56 |
| 5 | Cartão (novo), 9 medidas | ver 4.3 | 16 | 88 | 1248 | 104 |
| 6 | Matriz dos 6 cartões de etapa | `dEtapa[Etapa no Fluxo]` em Colunas, `SVG Cartão Etapa` em Valores | 16 | 208 | 1248 | 372 |
| 7 | Tabela de conteúdo de mão de obra | `dEtapa[Etapa no Fluxo]`, `SVG Conteúdo` | 16 | 596 | 616 | 300 |
| 8 | Caixa de texto (leitura automática) | `Leitura 1` a `Leitura 5` como valor dinâmico | 648 | 596 | 616 | 300 |
| 9 | Gráfico de linhas: metros por dia | eixo `dCalendario[Date]`; `Metros Trançagem no Dia`, `Metros Cabine no Dia` | 16 | 912 | 616 | 240 |
| 10 | Gráfico de linhas: pessoas por dia | eixo `dCalendario[Date]`; `Pessoas Trançagem no Dia`, `Pessoas Cabine no Dia` | 648 | 912 | 616 | 240 |
| 11 | Caixa de texto (rodapé: definição) | texto fixo, ver 4.7 | 16 | 1168 | 960 | 28 |
| 12 | Cartão (carimbo de atualização) | medida `Dado Atualizado até` (a que as outras páginas já usam) | 992 | 1168 | 272 | 28 |

Altura de 1212 px em vez dos 1280 × 720 da §B.6.3: a página reproduz o HTML, que é uma página longa. São 6 visuais de
análise (5 a 10). Título, segmentações e rodapé não contam. Se a regra dos 720 px tiver de valer, os visuais 7 a 10 vão
para uma segunda página com as mesmas segmentações sincronizadas.

## 4. Configuração de cada visual

### 4.1 Título (1)
Linha 1: "Fluxo da trançagem até a cabine" (Segoe UI Semibold 20, cor de texto do tema).
Linha 2: "Volume, pessoas e KPIs por etapa · fonte: ficha de produção · dia produtivo de 05:20 a 05:20" (Segoe UI 11, cor suave).
Sem borda e sem fundo (Formatar → Geral → Efeitos: fundo e borda desligados).

### 4.2 Segmentações (2 a 4)
- Estilo **Lista suspensa**. Cabeçalho ligado com o nome ("Ano", "Mês", "Dia"), Segoe UI 10, cor suave.
- **Seleção única desligada** e **"Mostrar opção Selecionar tudo" ligada** (equivale ao "Todos" do HTML).
- Itens Segoe UI 11; fundo, borda de 1 px e cantos de 12 vêm do tema.
- Sincronização: só nesta página (Exibir → Sincronizar segmentações). Não sincronizar com as páginas do `GMS_Painel`.
- `Dia` é o dia do mês. Com Mês = Todos, escolher "15" pega todo dia 15. É o mesmo efeito do HTML, onde a lista de
  dias depende do mês.

### 4.3 Cartão dos KPIs (5)
Visual **Cartão** (o novo, que aceita várias medidas). Layout horizontal, 9 por linha, sem borda entre eles.
Renomeie cada campo para este visual (duplo clique no campo):

| Ordem | Medida | Rótulo no cartão | Rótulo de referência (opcional) |
|---|---|---|---|
| 1 | `Vazão Cabine (m/dia)` | m/dia na cabine | vazão da linha (TH) |
| 2 | `Pessoas por Dia no Trecho` | pessoas somando as 6 etapas | por dia, média |
| 3 | `Pessoas Trançagem / Cabine` | pessoas: trançagem / cabine | média diária |
| 4 | `m por Pessoa Cabine` | m por pessoa na cabine | produtividade da mão de obra |
| 5 | `Eficiência de Balanceamento` | eficiência de balanceamento | `Perda de Balanceamento` |
| 6 | `Lead Time Tranç→Cabine (h)` | lead time trançagem→cabine (h) | mediana por ficha, média dos dias |
| 7 | `WIP Little (m)` | m em processo (Little) | TH × lead time |
| 8 | `CV Vazão Trançagem` | variabilidade (CV) da vazão | trançagem, entre dias |
| 9 | `Rendimento de Fluxo` | rendimento de fluxo | cabine ÷ trançagem |

Valor em Segoe UI Semibold 24; rótulo Segoe UI 10, cor suave. Sem dado, o cartão fica em branco (nunca 0).

### 4.4 Matriz dos cartões (6)
Passo a passo em `Medidas_SVG_FluxoTrancagemCabine.md` ("Montar os 6 cartões"). Resumo: filtro do visual
`Trecho Tranç-Cabine` = Verdadeiro; subtotais desligados; grade desligada; **Tamanho da imagem 304 (altura) × 208
(largura)**; preenchimento do visual 0, sem fundo e sem borda; título por fx = `Título Cartões`.
Texto alternativo: "Seis cartões, da trançagem à cabine: pessoas por dia, metros por dia e pessoas a cada 1.000 m de cada etapa."

### 4.5 Tabela de conteúdo (7)
Colunas: `dEtapa[Etapa no Fluxo]` (largura 130) e `SVG Conteúdo` (renomear para "Pessoas a cada 1.000 m").
Tamanho da imagem 32 × 440. Classificar por `Etapa no Fluxo` crescente (ordem do fluxo; aqui a ordem física manda,
não o valor). Filtro do visual `Trecho Tranç-Cabine` = Verdadeiro. Título por fx = `Título Conteúdo`.
Texto alternativo: "Pessoas a cada 1.000 m por etapa; laranja são as duas etapas com mais gente por metro; tracejado é a média."

### 4.6 Leitura automática (8)
Caixa de texto: "Leitura automática" em Segoe UI Semibold 12 na primeira linha. Depois, um parágrafo por medida,
inserida com **+ Valor** (digite o nome da medida): `Leitura 1 Restrição`, `Leitura 2 Mão de Obra`,
`Leitura 3 Balanceamento`, `Leitura 4 Little`, `Leitura 5 Dia Único`. Segoe UI 12. Borda esquerda laranja da
ilustração não existe na caixa de texto; use a borda do tema.
(`Leitura Automática` junta as cinco num texto só, para tooltip ou cartão; a quebra de linha `UNICHAR(10)` não
aparece na caixa de texto, por isso aqui vão as cinco separadas.)

### 4.7 Gráficos de linha (9 e 10) e rodapé (11, 12)
- Eixo X `dCalendario[Date]`, tipo **Contínuo**, sem hierarquia de data. Eixo Y começa em 0. Marcadores desligados.
- (9) Título "Quanto a trançagem e a cabine fazem por dia (m)?". Cores: trançagem = cor 1 do tema (azul),
  cabine = cor 2 (verde).
- (10) Título "Quantas pessoas a trançagem e a cabine usam por dia?". Trançagem = cor 3 do tema (laranja),
  cabine = cor 2 (verde).
- Dia fora da média (trançagem < 3.000 m) fica em branco nas séries, como no HTML. Com um dia só escolhido, ele aparece.
- (11) Texto fixo, Segoe UI 9, cor suave: "Pessoas = operadores distintos que apontaram a etapa no dia (estimativa,
  não é escala oficial). Médias só dos dias com trançagem ≥ 3.000 m."
- (12) `Dado Atualizado até`, Segoe UI 9, sem rótulo de categoria (§B.8.3).

Cor só pelo tema (escolher a cor do tema no seletor, nunca digitar hex no visual). O SVG é a única exceção, porque
imagem não lê o tema.

## 5. Checklist de validação

### 5.1 Antes dos números
- [ ] `fEtapaOP` atualizou sem erro. Conferência de contagem: para cada etapa, linhas da `fEtapaOP` = fichas da
      `ficha_producao` com `data_hora_final_<etapa>` preenchido (não há junção; se der diferente, é o tipo da data).
- [ ] **Fuso:** abra uma ficha conhecida no app e compare o `Fim da Etapa` da `fEtapaOP`. Se vier 3 h adiantado, a
      lista entregou UTC sem fuso: no M, troque `else if Value.Is(v, type datetime) then v` por
      `else if Value.Is(v, type datetime) then v - #duration(0, 3, 0, 0)` e atualize de novo.
- [ ] Virada das 05:20 (§B.9.3): um fim às 05:19 cai na `Data de Referência` do dia anterior; um às 05:21, no próprio dia.
- [ ] `Quantidade (m)` sem erro de vírgula: soma da Trançagem de um dia bate com o rodapé do app.
- [ ] As 4 medidas SVG aparecem como imagem (se aparecer o texto `data:image...`, falta a categoria URL da imagem).

### 5.2 Mesmo período do HTML
O HTML tem dados de **03/12/2025 a 06/10/2026**. O modelo tem mais. Para comparar, ponha no painel de filtros da
página um filtro temporário `dCalendario[Date]` entre essas datas, segmentações em "Selecionar tudo". Tire o filtro depois.

### 5.3 Conferência 1:1 (medidas da pasta `Conferência`, dia pela data civil do fim, igual ao HTML)
Arraste num cartão provisório. Tem de bater com o HTML (tolerância: arredondamento, e até ±0,05 pessoa porque o BI
tira espaço sobrando do nome do operador e o HTML não):

| HTML (todos os dias) | Medida de conferência | Esperado |
|---|---|---|
| cabine 5.499 m/dia | `Conf HTML · Vazão Cabine (m/dia)` | 5.499 |
| pessoas 6,9 / 5,0 | `Conf HTML · Pessoas Trançagem / Cabine` | 6,9 / 5,0 |
| eficiência 57% | `Conf HTML · Eficiência de Balanceamento` | 57,5% |
| lead time 31 h | `Conf HTML · Lead Time (h)` | 31,4 |
| WIP ~7.196 m | `Conf HTML · WIP Little (m)` | 7.196 |
| CV 23% | `Conf HTML · CV Vazão Trançagem` | 22,6% |
| rendimento 85% | `Conf HTML · Rendimento de Fluxo` | 84,7% |

Se essas não baterem, o problema está na `fEtapaOP` (fuso, tipo, coluna faltando), não na regra do dia.

### 5.4 Números oficiais da página (dia pela Data de Referência, 05:20 a 05:20)
Simulados com o mesmo CSV do HTML e a regra da `fn_DataRef`. São estes que a página mostra:

| KPI | HTML (data civil) | Página do BI (Data de Referência) |
|---|---|---|
| Dias produtivos | 184 | 185 |
| Vazão cabine (m/dia) | 5.499 | ≈ 5.296 |
| Vazão trançagem (m/dia) | 6.489 | ≈ 6.472 |
| Pessoas trançagem / cabine | 6,9 / 5,0 | ≈ 6,9 / 4,9 |
| Pessoas somando as 6 etapas | 22,2 | ≈ 21,9 |
| m por pessoa na cabine | 1.091 | ≈ 1.089 |
| Eficiência de balanceamento | 57% | ≈ 58% |
| Lead time (média das medianas diárias) | 31 h | ≈ 26 h |
| Lead time mediano do período (`Lead Time Mediano do Período (h)`) | 22 h | ≈ 22 h |
| WIP de Little | 7.196 m | ≈ 5.716 m |
| CV da vazão da trançagem | 23% | ≈ 22,5% |
| Rendimento de fluxo | 85% | ≈ 82% |
| Menor vazão / maior conteúdo | Debandagem / Trançagem | Debandagem / Trançagem |
| Cartões laranja | Trançagem e Cabine | Trançagem e Cabine |

Cartões de etapa esperados na página (Data de Referência, mesmo período):

| Etapa | m/dia | pessoas/dia | máx | m/pessoa | pessoas por 1.000 m |
|---|---|---|---|---|---|
| Trançagem | ≈ 6.472 | 6,9 | 11 | ≈ 938 | 1,07 |
| Cobertura | ≈ 6.364 | 2,7 | 6 | ≈ 2.369 | 0,42 |
| Bandagem | ≈ 6.126 | 3,2 | 8 | ≈ 1.905 | 0,53 |
| Vulcanização | ≈ 6.194 | 2,2 | 5 | ≈ 2.850 | 0,35 |
| Debandagem | ≈ 5.200 | 2,1 | 7 | ≈ 2.479 | 0,40 |
| Cabine (teste) | ≈ 5.296 | 4,9 | 12 | ≈ 1.089 | 0,92 |

**Por que muda:**
1. O HTML conta o dia pela data civil do fim de cada etapa. O BI conta pela `Data de Referência` (§A.3): 7,3% dos fins
   caem entre 00:00 e 05:20 e vão para o dia anterior.
2. Isso muda quais dias passam no corte de 3.000 m. O caso típico é a cabine trabalhando de madrugada depois de um dia
   sem trançagem (domingo à noite, feriado). No BI esses metros caem num dia que não entra na média, e a vazão da cabine
   cai uns 200 m/dia. O rendimento de fluxo cai junto (85% → 82%).
3. Pessoas: no HTML, o operador do 3º turno que aponta antes e depois da meia-noite conta em dois dias. No BI conta
   uma vez, no dia produtivo dele. Por isso a cabine cai de 5,0 para 4,9.
4. Lead time: o HTML faz a **média das medianas diárias**, e a página copia isso. Essa média é sensível a dia com
   poucas fichas e muda bastante com a troca de dia (31 → 26 h), e o WIP de Little vai junto (7.196 → 5.716 m). A
   mediana única de todas as fichas é bem mais estável: 22 h nas duas regras de data. Ela está em
   `Lead Time Mediano do Período (h)`, para comparar.
5. Período: sem o filtro da 5.2, o BI inclui os dias depois de 06/10 e todos os números mudam.

### 5.5 Comportamento dos filtros
- [ ] Escolhendo um dia sem produção: cartões e KPIs em branco; leitura "Sem dados no filtro."
- [ ] Escolhendo um dia com trançagem < 3.000 m: o dia entra assim mesmo (dia único sempre entra) e a leitura mostra o
      aviso de dia único; CV em branco.
- [ ] Mês com um só dia produtivo: CV em branco (precisa de 2 dias).
- [ ] Os 2 cartões laranja mudam conforme o filtro, sempre as 2 etapas de maior conteúdo do recorte.

### 5.6 Checklist pré-publicação (§B.9) que se aplica aqui
- [ ] Zero agregação implícita: só medidas nos valores (as colunas de `dEtapa` e `dCalendario` só como eixo/categoria).
- [ ] Formato pt-BR (milhar com ponto, decimal com vírgula) em cartões, tabela e tooltip.
- [ ] Contraste ≥ 4,5:1 (paleta conferida: texto suave 6,5:1, laranja na caixa 6,2:1, verde na caixa 6,9:1, selo
      escuro sobre laranja 7,6:1) e texto alternativo nos visuais 5 a 10.
- [ ] Performance Analyzer: a matriz dos cartões (6 SVG, cada um calcula a posição de conteúdo das 6 etapas) abaixo de ~3 s.
- [ ] Carimbo de atualização visível no rodapé.
- [ ] Linhas de diário (no fim de `Medidas_FluxoTrancagemCabine.md`) coladas depois de conferido.

## 6. Pendências
- `fEtapaOP` sem coluna `Turno` (fora do escopo do piloto). Para virar fato oficial (§A.3), o `revisor` define o turno.
- As cores do tema seguem o HTML aprovado, não os tokens `fx_` da §B.6.1 (`#2C6FBF`, `#16A34A`, `#E67E22`, `#C0392B`).
  Antes de levar a página para o `GMS_Painel`, decidir se o piloto vira o `GMS_Tema_BI.json` ou se troca para os tokens.
- Se a `Etapas` do modelo já tiver operador por etapa, a `fEtapaOP` sobra: ver a seção 0 do arquivo de medidas.
