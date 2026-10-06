# Conteúdo do canal (Bit)

Conteúdo de Instagram, TikTok e LinkedIn sobre Engenharia de Computação, com os projetos do GMS e do Will Station, apresentado pelo mascote **Bit**.

| Pasta | O que tem |
|---|---|
| `Marca/` | Logos do GMS e conceito dos mascotes (Bit e Ficha) |
| `Videos/Publicar/` | Reels do GMS em PT (1min18 pro LinkedIn, 30 s pro Instagram/TikTok), capas e `posts_prontos.md` |
| `Videos/Roteiro/` | Conceito visual, storyboard, revisão e guia de gravação |
| `Videos/Arquivo_nao_publicar/` | Versões antigas e em inglês (têm números do Kaizen, não publicar) |
| `Producao/` | Motor de render: `brand.js` (sistema visual), `mascots.js` (Bit/Ficha), reels, episódios, carrossel, `willstation3d.html` (Three.js), `serve.ps1` e a trilha (`stems/`) |
| `Semanal/` | Entregas de cada semana (`semana-AAAA-MM-DD`) e `ideias.md` |
| `WillStation/` | História do fliperama da faculdade e fotos |

## Regras de conteúdo
- O tom é de quem mostra o trabalho: nada de aula nem de chamada pra ação.
- Nada de números do Kaizen nem dados reais da empresa nos posts. O GMS é contado pelo TCC: 9 meses, 2 de desenvolvimento e 7 de implantação.
- Sistema visual: monocromático com um único destaque (#FF3B1F), fonte Geist, cantos retos e grão.

## Como renderizar
1. Rode `Producao/serve.ps1`. Ele serve em `http://127.0.0.1:5178`; os caminhos `$root` e `$work` no topo do arquivo apontam pra pasta local.
2. Abra um HTML de `Producao/` com `?t=1,2,3` pra ver quadros parados ou `?render=1` pra gerar o MP4 (WebCodecs, H.264 + AAC).

A rotina semanal ("Conteúdo semanal (Bit)", todo sábado às 20h) roda a partir da pasta local `C:\Users\willi\Downloads\GMS`.
