# src/ui: base visual do FinAgent

Importe de `@/src/ui`. Tema escuro. Nunca use cor solta: use `cores`/`paleta`.

Tokens: `cores` (fundo, superficie, superficie2, borda, texto, texto2, primaria, sucesso, alerta, perigo, info), `paleta` (6 cores de categoria), `espaco` (xs..xl), `raio` (sm 8, md 12, lg 16, pill), `fonte` (pequena, corpo, titulo, numero, heroi), `Variante` = 'info' | 'alerta' | 'sucesso' | 'perigo'.

| Componente | Props |
|---|---|
| `Card` | `children, style?, borda?` (cor da borda) |
| `MetricCard` | `rotulo, valor, nota?, cor?` (flex: 1, use dentro de `Linha`) |
| `ProgressBar` | `pct (0-100), cor?, faixas?, altura?` (padrão: verde <=30, amarelo <=60, vermelho acima) |
| `corDaFaixa` | `(pct, faixas?) => cor` |
| `StackedBar` | `segmentos: {rotulo, valor, cor, texto?}[], altura?` (legenda embutida) |
| `BarChart` | `dados: {rotulo, a, b}[], rotuloA, rotuloB, corA?, corB?, altura?` |
| `DonutChart` | `fatias: {rotulo, valor, cor, texto?}[], tamanho?, espessura?, centro?: ReactNode, legenda?` |
| `SectionHeader` | `titulo, acao?, aoAcao?` |
| `Badge` | `texto, variante?` |
| `InsightCard` | `texto, variante?, icone?` (nome Ionicons) |
| `EmptyState` | `icone?, titulo, texto?, botao?, aoBotao?` |
| `Botao` | `texto, aoPressionar?, secundario?, icone?, desabilitado?` |
| `Linha` | `children` (linha horizontal com gap) |

Gráficos usam `react-native-svg` e medem a largura sozinhos. Textos de insight vêm de `src/insights.ts` (funções puras).
