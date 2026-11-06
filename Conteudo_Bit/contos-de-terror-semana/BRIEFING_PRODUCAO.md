# Briefing de produção: 28 Shorts de terror (contos de terror da semana)

Escrito em 31/10/2026 pela sessão anterior (série "Plantão Noturno"). Leia este arquivo, depois os 3 arquivos desta pasta, depois `Conteudo_Bit\Serie\aprendizados.md`.

## Pedido do William (resumo)
28 Shorts de terror em 7 dias (4 por dia), cada um uma história completa de 45 a 70 s, mesmo processo da série "Plantão Noturno": narração, imagens e edição até o vídeo final 9:16 para YouTube Shorts e TikTok. Começar pelo **Dia 1 (4 peças)** e **parar para o William aprovar** antes de fazer os outros 6 dias. Dia 8: vídeo longo de 8 a 10 min com os 10 Shorts de melhor retenção (retenção só existe depois de publicar; sem dado, usar os 10 que o William indicar ou os 10 mais fortes pelo roteiro, e avisar).

Arquivos desta pasta: `plano-7-dias-contos-de-terror.md` (plano e roteiros do dia 1), `roteiros-dias-2-a-7.md`, `publicacao-28-pecas.md` (título, legenda, hashtags, horário e tom de cada peça).

## Regras do William
- Sem sangue explícito e sem violência com animais nas imagens (sugerir, nunca mostrar; o rato de "A Causa Secreta" nunca aparece, só sombra e chama).
- Só imagens e músicas sem direitos autorais: tudo desenhado por código e sons sintetizados pelo motor. Nada de banco externo sem conferir a licença de cada arquivo e avisar o William.
- Imagens na mesma identidade visual da série anterior (traço plano vetorial, papel escuro, legenda branca Oswald em 2 a 3 palavras por vez), com **fundo e cor dominante diferentes por peça**.
- Tom de voz de cada peça conforme `publicacao-28-pecas.md`; nunca o mesmo tom em peças seguidas.
- Nenhum agente publica, agenda ou envia. O William posta (TikTok e YouTube). Se ele pedir, preenche-se título e descrição no YouTube Studio pela extensão do Edge; ele seleciona os arquivos (a ferramenta de upload aceita no máximo 10 MB).
- Commit por assunto e push na main. Arquivos grandes (mp4) ficam fora do git.

## Conferência dos enredos (feita e a fazer)
- **A Causa Secreta: JÁ CONFERIDA no original** (Wikisource, edição de 1896). O roteiro de memória estava errado. **Use o roteiro corrigido abaixo (aprovado pelo William).**
- Antes de cada dia com conto de Machado ou Poe (O Enfermeiro, O Coração Delator, O Gato Preto, O Retrato Oval, O Barril de Amontillado, A Máscara da Morte Rubra), conferir o enredo no texto original (agente `web-fetch`; fontes públicas: Wikisource, Portal Machado de Assis, Domínio Público) e corrigir o roteiro antes de gravar.
- Poe: versão própria, não copiar tradução moderna.

### Roteiro corrigido da peça 1, A CAUSA SECRETA (tom seco, ~140 palavras)
Rio de Janeiro, 1860. Um homem é ferido numa rua escura. Outro, Fortunato, leva o ferido para dentro, e olha tudo friamente. O estudante Garcia vê e não entende.
Anos depois, Garcia é médico, e Fortunato é seu amigo. Casado com Maria Luísa. Dono de uma casa de saúde, e todos aplaudem sua dedicação.
Garcia se apaixona por Maria Luísa, em silêncio.
Um dia, abre a porta do gabinete. Fortunato prende um rato pelo barbante. Faz o bicho sofrer, devagar. Sorrindo.
Não é raiva. É um prazer quieto e profundo.
Maria Luísa adoece e morre.
Na noite do velório, Garcia beija a testa dela e cai em soluços.
Da porta, Fortunato assiste. Saboreia, tranquilo, aquela explosão de dor.
Uma dor deliciosamente longa.
(Citações curtas do original permitidas: "um vasto prazer, quieto e profundo", "saboreou tranquilo essa explosão de dor moral", "deliciosamente longa". Garcia era estudante em 1860 e formou-se em 1861. A casa do casal fica em Catumbi. Imagem do rato proibida.)

## Motor e processo (já prontos em Conteudo_Bit\Producao\serie)
- `motor.js` + `serie.html`: motor de animação vetorial em canvas, renderizado para MP4 (WebCodecs, H.264+AAC) no Edge headless. Cenas em JSON em `ep\*.json` (modelo: `ep06_pagina.json` + `ep06_sons.json` com a lista de sons); registrar o id em `ep\indice.json`. Veja `README.md`, `SFX_README.md`.
- Servidor: `Producao\serve.ps1` em 127.0.0.1:5178. Render: `serie.html?ep=ID&render=1` no Edge headless com `--disable-extensions`, flags anti-throttling e **sem** `--disable-gpu` (ele trava o desfoque); perfil temporário próprio `edgeprof-*` (apagar só os que você criou). `?t=` mostra um quadro. Saída hoje em `Semanal\serie\epNN.mp4`; para os contos, criar `Semanal\contos\diaN\` (a pasta e o nome dos arquivos podem ser decididos, mas avise o William).
- O motor tem cenários (pousada, quarto, corredor, cozinha, estrada, ponto de ônibus, varanda, olho mágico, espelho, escada etc.), poses, objetos e personagens por cor; recursos opcionais: `entra`, `glitch`, `ate`, `pisca`, `dentro`, `sofaEm`, `batida` com lista, `sobe` (personagem subindo escada), `escalaD/yD`. Cada conto novo exige cenários/objetos novos: adicione com mudança mínima, **só opcional ligada por parâmetro**, nunca altere o comportamento dos eps antigos (confira quadros dos antigos com `?t=`; `node --check motor.js`).
- Elenco: sempre passe `elenco` do JSON a cenários com câmera própria (olho_magico, espelho, punho), senão o personagem sai com visual padrão.
- Personagem não anda sozinho: use cortes, `sobe` ou keyframes; não deixe personagem "voando" nem sem os pés no chão.
- Sons: `sfx.js` sintetizado (drone, pulso, tique-taque, chuva, vento, passos, campainha, batidas, celular, zumbido de luz, caixinha, piano etc.), ducking sob a voz, limiter. Acrescente efeitos novos opcionais (grilos, elevador, galope, canto de ninar, água, respiração).
- Voz: `gen_voz_serie_edge.py` (edge-tts, pt-BR: Antonio, Francisca, ThalitaMultilingual; velocidade e tom ajustáveis por fala). Perfis aprovados: narrador Antonio +0%; narrador da série usava +10%. Sussurro de verdade: ElevenLabs v3 com `[whispers]` (chave em `~/.elevenlabs`, nunca imprimir; créditos limitados no plano Starter, usar só para a peça sussurro e falas críticas). `voz_fx.js` (efeito de sussurro por código) foi rejeitado pelo William.
- **Escreva sem contrações ininteligíveis:** "estou", "estava", "para o" em vez de "tô", "tava", "pro" nas falas (o edge-tts embola, principalmente voz lenta).
- Ritmo: nada de mais de 1,5 s de silêncio depois da fala, exceto silêncio dramático deliberado. Cenas com zoom lento em vez de imagem parada.
- Duração 45 a 70 s, 1080x1920, 30 fps. Legenda queimada em palavras. Cartela curta inicial com o título e, se literário, autor e ano.
- Medir ao final de cada peça: duração, resolução, pico de áudio sem clipping, voz pelo menos 6 dB acima da cama, e **olhar** uma folha de contato de 12 quadros do MP4 final (legendas legíveis, nada cortado). O agente não ouve: diga ao William o que só o ouvido dele valida.

## Dia 1: 4 peças, nesta ordem e com estes tons (nenhuma repete o tom da vizinha)
| Hora | Peça | Tom | Cor dominante sugerida | Cenário |
|---|---|---|---|---|
| 9h | A Causa Secreta (Machado de Assis, 1885) | Seco: voz de documentário, ritmo médio, pausa de 1 s antes do final, drone grave baixo | vinho/bordô | rua do Rio antigo à noite, gabinete com chama, velório |
| 13h | Boitatá (folclore) | Causo: contador rural, voz quente e lenta, grilos | azul-noite | pasto e casa de roça à noite, luz azul serpenteando |
| 18h | Seu nome na madrugada (original) | Sussurro: confessional, segunda chamada em voz normal e seca, silêncio total na virada (ElevenLabs) | verde-musgo acinzentado | quarto e cozinha escura |
| 21h | Elevador no 13º (original) | Humor seco: relato casual de morador, vira frio na última linha, som de elevador | âmbar | elevador, corredor, painel com botão 13 aceso |
Título, legenda, hashtags e horário de cada peça em `publicacao-28-pecas.md`. Roteiros das peças 2, 3 e 4 em `plano-7-dias-contos-de-terror.md` (sem erros factuais apontados; o Boitatá é folclore com variações regionais).

## Recursos e limites
- Plano Pro: ao escrever este briefing, 64% do limite semanal usado; o limite semanal reseta em 01/11 às 11h UTC (8h no Brasil). O William autorizou gastar os tokens de hoje. Use **Sonnet no esforço médio** como padrão para produção (JSON de cenas, vozes, sons, render); use Opus só para um elemento visual novo e difícil em que o Sonnet não der conta (verificar olhando a imagem). O `produtor-de-artes` (Opus) custou muito mais que o `executor` (Sonnet) na série anterior.
- Um episódio da série anterior custou cerca de 175 a 190 mil tokens de agente. Faça em sequência (o `motor.js` é compartilhado); só use porta/servidor paralelo para correções pontuais.
- Disco C: ~22 GB livres; apague os `edgeprof-*` que criar.

## Ao final de cada dia
Entregar o MP4 de cada peça por `SendUserFile`, o que foi medido, escolhas que o William pode mudar e o que só o ouvido dele valida. Registrar em `.claude\orquestracao\registro.md` e novos aprendizados em `Conteudo_Bit\Serie\aprendizados.md`. Esperar a aprovação do William antes do Dia 2.
