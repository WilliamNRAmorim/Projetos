# Plano v2: tubo, espiral e carretéis no GMS_Painel (04/11/2026)

Status: **proposta, nada executado.** Substitui o "Fase 2" do PLANO_levar_ao_GMS_Painel.md. Quem publica é o William.

## Pedidos novos (do William)
1. Adicionar tudo na lógica.
2. Número de carretéis além dos metros de mangueira.
3. Separar espiral de trançadeira.
4. Pôr o **Tubo** na visão por pessoa.
5. Desenho de carretel na visualização.
Tabela de metros por carretel (bitola): 4 → 800 · 6 → 680 · 8 → 680 · 10 → 460 · 12 → 400 · 16 → 250. Ex.: a cada 250 m é 1 carretel de bitola 16.

## O que o dado mostra
- **Espiral = `Spiral` no app = `TE01` na planilha.** `Formulas.txt` (linhas ~1073-1075) e o diário (MEL-159) dizem isso. Na ficha: `Spiral` 433 fichas; `TE01` 3 e `TE0` 1 (digitação). A família de mangueira `GH493` só roda na espiral (431 de 433; as 3 `TE01` com GH493 também). Então **espiral = Spiral + TE01 + TE0 (+ variações com ponto/hífen)**. O arquivo `PowerBI/modelo/limpeza_ficha_producao.m.md` trata `TE0`/`TE01` como lixo (vira vazio): isso está errado e deve ser corrigido quando a limpeza for aplicada.
- **Trançadeiras** (braiders) = TH01 a TH07, TM01, TM04, TO04.
- **Bitola na ficha:** 12 (719), 8, 16, 6, 4, 10 cobrem a maioria. Fora da sua tabela: 7 (106 fichas), 3 (19), 5 (3), 17 (1) e vazio (2).
- O `GMS_Painel` é relatório ligado ao vivo ao modelo `(GMS)`. Nele só dá para criar **medidas do relatório** (arquivo `reportExtensions.json`); não dá para criar tabela, coluna nem relacionamento no modelo. O projeto já usa isso (existe `reportExtensions.json`).

## Desenho da solução (sem mexer no modelo publicado)
- **Medidas do relatório geradas por script** (`gerar_medidas_fluxo.py`), uma por etapa, calculadas direto da `ficha_producao` e do `dCalendario`:
  - Etapas: Tubo, Trançagem, Espiral, Cobertura, Bandagem, Vulcanização, Debandagem, Cabine (Extração/Teste). Trançagem e Espiral são a mesma etapa original separada pela máquina.
  - Por etapa: metros/dia (dias produtivos), pessoas/dia (operadores distintos, normalizados), m/pessoa, pessoas por 1.000 m, **carretéis/dia** (metros ÷ metros do carretel da bitola, ficha a ficha) e **carretéis por pessoa**.
  - Dia pela data de referência (virada 05:20), `Turno` por `fn` na própria medida, mesma regra do piloto.
  - Sem tabela de etapas: cada cartão é um visual próprio (8 cartões), com uma medida SVG por etapa.
- **KPIs gerais** (vazão da cabine, eficiência, CV, Little, rendimento) recalculados com as 8 etapas.
- **Desenho de carretel:** ícone SVG de carretel (dois flanges e o núcleo), um por carretel do dia, o último preenchido pela fração, como os ícones de pessoa; cor pela bitola mais frequente.
- **Layout da página 1:** 8 cartões em 2 linhas de 4, cada um com pessoas, carretéis, barra de metros e caixa de m/pessoa (mantém o estilo aprovado, tema claro). Página 2 mantém conteúdo de mão de obra, leitura e gráficos mensais; o eixo do mês passa a usar a hierarquia de datas (sem coluna nova no modelo).
- **Bitolas fora da tabela (7, 3, 5, 17):** os metros contam, mas o carretel fica sem número ("n/d") e o cartão mostra a fatia coberta (ex.: "carretéis em 96% dos metros").

## Passos
0. **Retrato de volta:** commit do estado atual do `GMS_Painel.Report` (com as suas alterações, 26 arquivos) antes de qualquer escrita.
1. Gerar as medidas e as 2 páginas numa **cópia** do `GMS_Painel.Report`, validar no Desktop (números por etapa contra o piloto: Trançagem+Espiral = Trançagem anterior; cabine igual) e revisor (Opus) nas regras de turno e contexto de filtro.
2. Você aprova e eu gravo no `GMS_Painel.Report` (não regerar por cima do que está salvo; só acrescento as 2 páginas e as medidas); você publica.
3. Atualizar `limpeza_ficha_producao.m.md` (TE0/TE01 = Spiral) quando essa limpeza for aplicada no modelo.

## Decisões do William
1. **"Adicionar tudo na lógica":** proponho Tubo → Cabine nos KPIs. O **Mandril** entra também? (padrão: não, porque a quantidade do mandril é de lance longo e fica de fora do fluxo por pessoa.)
2. **Metros por carretel** das bitolas 7, 3, 5 e 17 (ou deixar "n/d").
3. Pode eu fazer o commit-retrato do `GMS_Painel.Report` (passo 0)?
4. Layout 2 linhas × 4 cartões está bom?

## Riscos
- Desempenho: medidas varrem a `ficha_producao` (cerca de 3 mil linhas) com normalização de nome; deve ficar rápido, mas é medido no Desktop.
- Nada de tabela nova: sem `dEtapa`, cada etapa é uma medida e um visual (manutenção maior; por isso o gerador).
- Pessoas continuam estimativa pelos apontamentos (operadores distintos), com códigos antigos nos meses antes de maio.
- A ordem do mês no eixo depende da hierarquia de datas do `dCalendario`.

## Estimativa
3 a 4 horas até o primeiro resultado na cópia (gerador + medidas + validação), mais a revisão e a sua conferência.
