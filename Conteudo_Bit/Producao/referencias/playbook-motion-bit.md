# Playbook de motion do Bit (estudo de 513 prompts de terceiros)

Base: `opus55-videos-estudo.md` e 21 prompts originais lidos por inteiro, entre eles os das notas mais altas de cada fatia (astrothewizard, brainextends, annacher, gdgtify, techhalla, raphaelaubryy, ik-builds e parkerrex). São textos de terceiros, parafraseados aqui.

## 1. O que vale mais

1. **Quadro como função pura do tempo.** Os melhores prompts pedem `seek(t)` sem timers, sem transição CSS e sem estado guardado entre quadros. O aleatório é semeado e as molas são calculadas em forma fechada. Isso permite pedir qualquer quadro em qualquer ordem e conferir antes de renderizar. O nosso motor já segue esse padrão (`frame(tt)` e `rnd()` no `ep_kit.js`, `?t=` e `?sheet` no `reel_pt.html`).
2. **A especificação fecha cada instante.** brainextends, howdevelop e gdgtify descrevem o que acontece em cada janela de 0,6 a 3 s, com o texto exato que entra na tela. Quando o prompt não traz essa lista, o arco sai vago.
3. **Uma ideia formal por cena, ligada a um elemento que não sai da tela.** Pode ser a barra do player (brainextends), uma forma única que muda de tamanho, raio e cor (annacher) ou palavras que viram estrutura (gdgtify). A transição mostra a ideia, em vez de só trocar um cartão por outro.
4. **Simular o fenômeno em vez de desenhá-lo.** O passeio aleatório de astrothewizard é calculado de verdade, e parkerrex anima o token bucket a partir do próprio algoritmo. Para engenharia, é isso que dá credibilidade.
5. **Conferir antes do render.** Os prompts pedem um still por batida, um contact sheet com cerca de 20 quadros e oito quadros representativos. O render completo só vem depois.
6. **Proibições e texto travados.** Os prompts fortes trazem a lista do que é proibido e a mensagem exata, na ordem, sem slogan a mais.
7. **O vídeo tem que funcionar sem som.** A legenda é queimada no vídeo e medida na fonte real. No áudio, o pico de cada efeito cai sobre o evento, a mixagem fica em -14 LUFS e a música abaixa sob a voz.

## 2. Adaptação para reels 9:16 de ~30 s

- **Formato.** 1080x1920 a 30 fps, como no motor atual. 60 fps só se o teste 1 mostrar ganho visível.
- **Grade de tempo.** 120 BPM dá 2 s por compasso e 15 compassos em 30 s. Os cortes caem no tempo forte. Cada ideia fica pelo menos 2 s na tela (bilimfili1 usa 2,5 s), porque a legenda em português é mais longa.
- **Arco.** Gancho até 1,5 s, problema real, como foi resolvido em 3 passos visuais, prova mostrada (tela, foto ou simulação, sem número inventado) e fechamento. O tom é de quem mostra o trabalho, sem aula e sem chamada pra ação.
- **O Bit.** Entra como personagem pequeno que reage ou aponta, sem dublar com boca tremendo. No LinkedIn o vídeo vai sem Bit.
- **Loop.** O último quadro é igual ao primeiro, com mesma posição e velocidade. No Reels, o vídeo recomeça sem que se perceba o corte.
- **Uma base, vários cortes.** Os cortes de 30 s, 15 s e 6 s são listas diferentes de cenas no mesmo HTML, como em l3d1c.

## 3. Modelo de especificação reaproveitável

```
<entradas>  (sem elas, não começa)
Tema e texto APROVADO (exato, na ordem). Fonte de cada número citado (ou "sem números").
Material real: telas, fotos, vídeos do William. Plataforma: IG/TikTok (com Bit) ou LinkedIn (sem Bit).
</entradas>

<direcao>
Fundo BRAND.ink #0C0C0D (ou paper #EEEDE8), texto paper/ink, secundário mute #8C8B86,
destaque ÚNICO #FF3B1F só na palavra/objeto que importa (no máx. 1 por quadro).
Geist 800/900 para display (tracking -0,03 a -0,04 em), Geist Mono 500/700 para rótulos (tracking 0).
Cantos retos, grão 0,07. Sem ponto final em texto de tela. Um elemento persistente: [definir].
</direcao>

<timeline>  (30,0 s, 120 BPM, tempo forte em t=0)
0,0-1,5   gancho: uma frase de até 6 palavras entra por máscara; o objeto-guia aparece
1,5-4,0   problema: o objeto-guia mostra a falha real (simulada, não ilustrada)
4,0-6,0   virada: o destaque vermelho marca o ponto da mudança
6,0-12,0  passo 1 e passo 2 (3 s cada), cada transição demonstra o passo
12,0-16,0 passo 3; o objeto-guia muda de estado sem corte
16,0-22,0 prova: tela/foto real em quadro reto, rótulo em mono
22,0-26,0 fechamento: frase final, uma palavra em #FF3B1F
26,0-28,0 respiro de 0,4 s parado (obrigatório)
28,0-30,0 o fechamento volta à composição do quadro 0 (loop)
</timeline>

<movimento>
Entrada: out cúbico (EpKit.out) ou cubic-bezier(0.16,1,0.3,1), 0,3-0,6 s.
Câmera: inout cúbico (EpKit.inout), 1,5-3 s, só punch-in de 1,00 a 1,08 e pan no tempo forte.
Mola fechada amortecida criticamente: x(t) = 1 - (1 + w*t) * exp(-w*t), w entre 12 e 18.
Para overshoot abaixo de 2%: zeta = 0,8. Cada troca de alvo soma uma mola nova.
Texto que sai some antes de o novo ocupar o lugar; texto trocado tem entrada e saída próprias.
</movimento>

<motor>
frame(t) puro: sem setTimeout/rAF/CSS transition; aleatório só por rnd(semente).
render(0) == render(30). Exporta n/30 para 900 quadros via ?render=1 (WebCodecs).
Sem will-change em elemento escalado; fade no wrapper, nunca em preserve-3d.
</motor>

<safe_area>  (1080x1920)
Texto e informação entre x 90-940 e y 250-1480.
Topo 0-250: barra do app e "Reels/Seguindo". Base 1480-1920: legenda do post,
nome e música. Lateral direita 940-1080 (a partir de y 900): botões.
Legenda da fala com baseline em ~1470 (já é o padrão do EpKit.legenda).
Capa: o centro de 1080x1350 tem que se ler sozinho (grade do perfil).
</safe_area>

<audio>
Trilha de stems/ (própria) ou sintetizada; nada de terceiros.
Efeito com o pico (não o início) no evento; voz por tts.ps1/ElevenLabs.
Música abaixa sob a voz; -14 LUFS e -1 dBTP medidos depois do AAC.
</audio>

<verificacao>
1) ?sheet com 1 quadro por compasso (15) + overlay de safe area.
2) 8 quadros: gancho, cada passo, prova, fechamento, quadro 0 e quadro 899.
3) Diferença de pixels quadro 0 x quadro final = 0 (antes do grão).
4) Ler a legenda na ordem certa, sem nada sob a interface.
</verificacao>

<proibido>  ver seção 4
```

## 4. O que não copiar

- **Números inventados.** Vários prompts de produto põem contagens e resultados na tela sem fonte, como quantidade de concorrentes, provedores ou anúncios pausados. ik-builds e bilimfili1 proíbem isso de forma explícita, e a regra vale também para nós. Nenhum número do Kaizen, nenhum dado real da empresa, e cada número na tela precisa de fonte registrada na especificação. Para o GMS, só os dados do TCC: 9 meses, sendo 2 de desenvolvimento e 7 de implantação.
- **O que denuncia IA.** Glow, neon, partículas, anéis de choque, lens flare, tremor de câmera, glassmorphism, degradê, cérebros, robôs e brilhinhos, quique elástico, crossfade de tela inteira, moldura e texto de canto, e rótulos de "HUD" falsos.
- **Rompe a nossa marca.** O palco arredondado de brainextends, as três fontes e a paleta de duas cores de techhalla, a separação RGB e o misregistration. Atenção: o `glitch()` do `ep_kit.js` usa ciano #00E5FF, que é um segundo matiz (ver decisões).
- **Prompt vago.** "Go all out" e placeholders vazios dão resultado genérico. 1stnoel e alex-prompter só funcionaram porque o modelo inventou o resto, e nós não podemos inventar.
- **Recriar apps ou marcas reais**, imitar artista ou usar trilha sem licença.
- **Créditos e chamadas falsos**, como "A Studio1 film", "link na bio" ou "siga".
- **Autonomia total.** astrothewizard manda seguir sem perguntar nada. Para nós, sem texto aprovado, o produtor pede o texto em vez de criá-lo.
- **Boca do mascote tremendo** e braços com anatomia estranha.

## 5. Cinco testes pequenos (fazer nesta ordem)

O custo é estimado pelos preços de `.claude/orquestracao/precos.json`, com o produtor-de-artes em Opus 5.5. Considerei de 20 a 40 turnos, de 1 a 2 milhões de tokens lidos do cache, de 100 a 200 mil escritos no cache e de 30 a 60 mil de saída. Nenhum teste publica nada, e os arquivos ficam em `Producao/testes/`.

| # | Teste | O que prova | Custo est. |
|---|---|---|---|
| 1 | **Forma única em loop, 6 s.** Um quadrado reto off-white muda de tamanho e de posição em 3 molas fechadas, e o vermelho aparece em um único estado. 1080x1920. | Mostra que a mola fechada, o `frame(t)` puro e o loop `render(0)==render(6)` funcionam. Também compara 30 e 60 fps. | US$ 1 a 2 |
| 2 | **Overlay de safe area e sheet por compasso.** Adiciona `?safe=1` e `?sheet=compasso` ao `ep_kit.js`. Não cria peça nova. | Dá a ferramenta de conferência a todos os reels seguintes. | US$ 0,5 a 1 |
| 3 | **Simulação real, 10 s.** Um algoritmo do Will Station animado a partir do código de verdade, por exemplo o debounce do botão ou o loop de leitura do joystick. O texto precisa vir aprovado. | Testa a regra de simular em vez de desenhar, no estilo parkerrex, com o nosso conteúdo. | US$ 2 a 3 |
| 4 | **Frase cinética travada, 8 s.** Uma frase aprovada, em que uma palavra vira o objeto-guia (técnica de gdgtify) e há o respiro de 0,4 s. | Testa a tipografia Geist com máscara e a leitura na ordem certa. | US$ 1,5 a 3 |
| 5 | **Áudio por código, 10 s.** Três efeitos sintetizados alinhados pelo pico sobre a trilha de `stems/`, mixados e medidos em LUFS e dBTP depois do AAC. | Fecha a sincronia e o volume, que é onde mais falha nos vídeos estudados. | US$ 1 a 2 |

O total fica entre US$ 6 e 11. Os testes 1 e 2 não dependem de texto. Os testes 3 e 4 só começam com o texto aprovado pelo bit ou pelo William.

## Decisões humanas pendentes

1. O glitch com ciano #00E5FF no `ep_kit.js`: manter como exceção técnica, trocar por glitch monocromático com vermelho ou remover.
2. O grão usa `Math.random` uma única vez. É estático e não quebra o loop, mas não é idêntico entre sessões. Decidir se ele passa a ser semeado.
3. 30 ou 60 fps (resposta depois do teste 1).
