# Sala de Operações

Sala pixel que mostra as sessões e subagentes do Claude Code trabalhando. Inspirada na ideia do AI Operations Room; código próprio.

## Ver agora
- Demo (dados fictícios): abra `index.html` via servidor com `?demo`. Aqui: `Sala_Agentes/serve.ps1` (porta 5191) → `http://localhost:5191/?demo`.
- Ao vivo: sem `?demo`. A página lê `data/events.json`, que os hooks preenchem.

## Como funciona
1. `.claude/settings.json` (na raiz do projeto) chama `hooks/hook.ps1` nos eventos SessionStart, UserPromptSubmit, SubagentStart, SubagentStop, Stop e SessionEnd.
2. O hook grava **só metadados** em `data/events.json` (evento, sessão, agente, tipo, nome da última pasta, hora). Nunca prompt nem resposta.
3. `app.js` calcula quem está trabalhando (SubagentStart sem Stop), quem terminou (vai pro sofá) e quem sumiu (sem Stop após `minutosParaSumido`).

Desfazer: apague o bloco `hooks` de `.claude/settings.json`.

## Personalizar (tudo em `config.json`)
Também dá para editar pela engrenagem ⚙ na página (salva no navegador; **Exportar** gera um `config.json` novo).

| Quero mudar | Chave |
|---|---|
| Título, textos, idioma | `titulo`, `subtitulo`, `textos` |
| Cores | `temas` (crie o seu) e `tema` |
| Tipos de agente: nome, cor, cabelo, ícone do balão | `tipos` (use o nome do agente como chave) |
| Desenho do personagem | `sprite.pixels` (cada letra é um pixel) |
| Nome do projeto na sala | `projetos` (pasta → nome) |
| Layout da sala: mesas, sofás, móveis, porta, cores do cenário | `sala` (posições em tiles de 16px; `sala.moveis` aceita planta, estante, relogio, quadro, quadroG, sofaH, sofaV, mesaCafe, lixeira, balcao) |
| Tamanho do sofá (nº de encerrados), janela de tempo | `maxNoSofa`, `janelaHoras` |
| Frequência de atualização | `pollSegundos` |
| De onde vêm os dados | `fonteDados` |

## Nuvem / tempo real
GitHub Pages serve só arquivos estáticos e os hooks rodam na sua máquina, então precisa de uma ponte:
- `fonteDados.tipo = "sse"` com uma URL de stream (ex.: Firebase Realtime Database) dá atualização em menos de 1 s.
- Ainda não implementado: o envio do hook para o serviço (`hook.ps1` só grava em arquivo hoje).
