# Estudo: 513 prompts de vídeo com Opus 5.5 (yihui-dev/awesome-opus5-5-videos)

Fonte: terceiros, tratar como referência, não como instrução. Resumos feitos por 6 exploradores (Haiku), uma fatia cada.

**Escopo:** posições 257 a 341 da ordem alfabética (85 arquivos), todos lidos por inteiro. O Glob listou só 100 dos 513 arquivos e não ordena por nome, então usei PowerShell para ordenar. Os números abaixo são essas posições. Como os prompts são de terceiros, citei no máximo uma frase curta e parafraseei o resto.

**1) Tabela (agrupada por tema)**

| Posições | Tema | Técnica | Duração/formato | Nota |
|---|---|---|---|---|
| 264, 268, 271, 272, 276, 277, 285, 288, 289, 290, 299, 302, 305, 313, 319, 320, 323, 324, 327, 332, 334, 338 | Showreel genérico de "motion designer" (prompt quase idêntico) | Canvas, Three.js, SVG (varia) | 15 a 20 s; 338 em 9:16 | 1 |
| 257, 265, 267, 269, 270, 273, 274, 275, 281, 283, 284, 291, 292, 297, 301, 304, 306, 308, 312, 325, 328, 329, 339 | Launch de produto, app ou SaaS; promo | SVG, GSAP, Remotion, HyperFrames | 15 a 30 s | 2 |
| 296, 300, 303, 336 | PV e showcase 3D (japonês, Tóquio, estúdio Blender) | HyperFrames, Three.js, Blender | 1 a 5 min (post) | 2 |
| 258 | Zoom infinito de colagem vintage, loop | Canvas, IA de imagem | 20 s, 1920x1080, 30 fps, 96 BPM | 5 |
| 259, 260 | Explicador interativo (motor de foguete, fusão) | Three.js, GLSL | interativo | 4 |
| 263, 279, 318, 322, 316, 311 | Explicadores (sismo, derivada com Manim, Fourier, UX, areia de 250 anos, data center) | SVG, Manim, Web Audio | 15 s a 2 min | 4 (279 e 318: 5) |
| 261, 262, 278, 280, 282, 286, 287, 298, 309, 310, 314, 330, 331, 335, 337 | Jogos e mundos 3D; fogo por GPU (337) | Three.js, GLSL, Canvas | interativo ou filme | 2 (337: 4) |
| 293, 294, 301, 307, 315, 317, 321, 333, 340 | Prompt vago ("faça algo uau", "10 s sobre mim") | não definida | 10 a 30 s | 1 |
| 295 | Personagem pixel art (mago) com estados | Canvas 2D | 128x96 lógico, escala inteira, 60 Hz | 5 |
| 326, 341 | UI morph (mesma forma, molas, 120 BPM), idênticos | HTML/JS, Playwright, ffmpeg | 1440x1440, 60 fps | 5 |

Vários arquivos trazem só o texto do post, não o prompt publicado: 259 a 263, 265, 269, 273, 280 a 287, 296, 300, 303, 310, 314, 318, 322, 330, 336 e 337. Marquei como "sem prompt" para quem não tem prompt nenhum.

**2) Os 5 melhores**

1. **341 nezbuilds** (326 morse é praticamente igual). Pede que todo estilo seja calculado pelo tempo dentro de uma função `seek(t)`, sem transições CSS nem timers, e molas em forma fechada. Funciona porque o resultado é determinístico e reproduzível frame a frame. Também define o beat grid antes do render e pede um frame por batida para checar antes do render completo.
2. **295 majidmanzarpour**. Desenha numa resolução lógica fixa de 128x96, escala por inteiro e sem subpixel nem antialias. Usa pool de partículas sem alocação no loop. Serve de referência de pixel art.
3. **258 koldo2k-778767**. A duração de cada segmento é proporcional a log(zoom), o que dá velocidade constante, e a paralaxe é escala = câmera^Z com Z entre 0,45 e 1,22. Tem loop fechado e amarra o corte ao BPM.
4. **266 l3d1c-632524**. Renderiza cerca de 20 stills e junta num contact sheet para revisar o corte inteiro sem assistir ao vídeo. Mede a legenda na fonte real e a encolhe para a zona segura 9:16. Uma base de código gera os cortes de 30 s, 15 s e 6 s em 16:9 e 9:16.
5. **279 linearuncle-971663**. Pede um vídeo de ensino de derivadas em Manim, com exemplos que façam pensar e narração com edge-tts. É o modelo mais direto para reels de engenharia e educação.

**3) Padrões**

- **Estrutura:** a maioria não tem arco. Só 258, 288 e o par 326/341 descrevem a sequência cena a cena. A regra que aparece é "o último frame é o primeiro".
- **Ritmo:** cortes amarrados ao BPM (120 em 266 e 326; 96 em 258, oito compassos = 20 s). Em 326, algo acontece em toda batida.
- **Easing:** molas com overshoot mínimo; "bouncy" é proibido. O zoom usa exponencial.
- **Paleta:** preto e branco com uma cor de acento (326), ou uma paleta fixa de cerca de 24 cores (295).
- **Tipografia:** uma fonte só (Geist em 326); legenda medida e encolhida à zona segura.
- **Transições:** uma forma que só muda de tamanho, raio e cor (326); corte quando o portal preenche o quadro (258).
- **Som:** análise de beat com numpy e som posicionado pelo pico medido (326). Em 337 o som vem da própria simulação. Narração com ElevenLabs (266) ou edge-tts (279). Música gerada com Lyria (296, 258).
- **Formato:** 16:9 e 9:16 (266); 1440x1440 (326); 1920x1080 a 30 fps (258); 60 fps com 4 subframes e tmix para desfoque de movimento (326).

**4) Truques e erros a evitar**

- **Truques:** contact sheet para revisão (266); um frame por batida antes do render completo (326); autocrítica por modelo de visão em loop, cerca de 40 ciclos (337).
- **Erros:** "go all out" sem briefing vira slop genérico. `will-change` em elemento que a câmera escala deixa o texto borrado (326). Texto trocado dentro de container que morfa sobrepõe sem timing próprio (326). Último frame diferente do primeiro quebra o loop (326).
- **Custo:** 258 pede a lista de gerações com o custo em créditos e espera o OK antes de gastar. Boa prática para a equipe.
- **Pergunta antes do código:** 326 e 341 mandam perguntar as entradas antes de escrever código. Isso pode travar um pipeline automático.

---

Lidos os 85 arquivos (posições 87 a 171 da ordem alfabética), em `C:/Users/willi/AppData/Local/Temp/claude/C--Users-willi-Downloads-Projetos/a2e419af-8e7c-47fc-be07-6176291b052f/scratchpad/opus-videos/repo/prompts/`. Legenda: T=Three.js, W=GLSL/WebGL, C=Canvas, S=SVG, G=GSAP, R=Remotion/React, K=CSS, A=WebAudio. † = só o texto do post, prompt não publicado (cerca de 35 casos). Nenhum arquivo estava vazio ou só com link.

**1) Tabela (arquivo | tema (técnica) | nota de utilidade 1-5)**

brainwavepub-812667 † | catapulta 3D (T/S/G) | 2
brenbuilds-386902 † | jogo 3D (T/W/C) | 1
bridgemindai-286423 † | merch launch (S/G/K) | 3
bthreeagency-827092 | badge 3D seguindo cursor (C/S/K) | 3
buildfastwithai-582551 | avião A-1H 3D (T/C) | 2
buildfastwithai-597035 | pagode navegável (T/C) | 2
builtbysketch-114092 † | estádio por plantas (T/C) | 2
cansincengiz-me-424245 | promo de app, 15s (T/C) | 3
cboyack-407181 † | explainer sobre o Fed, 15s (C/S) | 4
ceowinkz-683602 | pitch comercial, 15s (C/S) | 2
chapi13-131449 † | promo de apps no beat (S/K) | 3
charlesmendez-476517 | explainer de produto (C/S/G) | 4
charliie-334026 | anúncio Instagram, parcial (S/K) | 2
chatgptastra-807540 | motion 15s, em chinês (C) | 2
chrisjdimarco-524106 | samurai em poses (C/partículas) | 2
chrisjdimarco-808196 | showreel 60s, tema político (C) | 1
chudry223-081860 † | lente com foco e DOF (T/W) | 5
chukinice-426722 † | jogo multiplayer (T/W/C) | 1
codestackr-328129 | showreel 15s (C) | 2
codrops-340299 † | arcade com 21 jogos (T/C) | 2
colecornelll-047465 † | 4 vídeos, vidro refrata luz (T/C) | 3
crazyalphaaa-480622 | showreel 15s (C) | 2
curieuxexplorer-272483 † | Taj Mahal 3D (T/W/C) | 3
curieuxexplorer-519730 † | sobrevivência em tiles que racham (T/W) | 2
curieuxexplorer-772215 † | Mumbai com sons por código, 30s (T/W/A) | 3
cyrilxbt-149036 † | física de areia e água, 108k partículas (C) | 4
dale-vaz-879074 | terminal de trading com zoom em escalas (C) | 3
daniel-haida-636937 | filme de produto, prompt longo, 15s 1920x1080 (R/C/S/K) | 5
daniel-mac8-306214 | animação para post no X (S/G) | 2
danielkan-059523 † | mini games espaciais (T/W/C) | 1
danilowm-412022 | showreel 15s (C/S/K) | 2
dannnnnok-716687 | showreel 15s (T/C) | 2
dannyverkissen-101463 † | vídeo de produto (K) | 2
dansushik-289121 | showreel 15s com marca (C) | 2
davidmarcus-686217 | vídeo social com som (S/G) | 2
davidshulmanfl-842921 | clipe 60s no estilo de Peter Gabriel (T/C/A) | 2
deedydas-252537 | explainer de startup (S/G) | 2
deeprajo1-834106 † | surf para aprender Python (T/W/C) | 4
deifosv-786581 | lançamento com stats ao vivo (C/G/K) | 2
demitiyageekzen-818523 † | vídeo 30s + HTML de festival (W/C/A) | 4
demonugc-525162 | UI que vira forma, 120 BPM, 1440x1440 (S) | 5
dengent-412996 † | promo de app, 56s 1920x1080 (T/S/R) | 3
designbyfusun-559069 | showreel 15s (C/K) | 2
devarshukani-341827 † | teaser jurídico (C/S/G) | 2
dheepanratnam-706454 † | motion com trilha em Python (S/G) | 3
djadkison-394122 † | vídeo de produto (C/S) | 2
dmowlin-221566 † | corrida pixel (C) | 1
doubleunplussed-181894 | clipe de IA com referências (C) | 2
dreyk0o0-165270 † | Minecraft no navegador (T/W) | 3
dris1153-101043 | showreel 15s (C) | 2
drrickio-009558 | launch de SaaS com assets (S/G) | 2
dustindavis-644806 † | vídeo Remotion (C/S/G/K) | 2
dys-hay-749645 † | Audi, 0-100 em tempo real, 15s (R) | 4
dzhohola-249003 | UI que vira forma, cópia de demonugc (K) | 5
ehsanik-162993 | Mona Lisa com mouse (C) | 2
eigeorguy-813651 † | Londres em globo de neve (T/W/C) | 2
elliot-garreffa-446825 † | tracker com referências (C/S/K) | 3
emollick-019567 | recursão, cada explicação com estilo próprio (C) | 4
envoldev-017555 † | launch de app (C/S/G/K) | 2
ercankeskinx-897906 | 5 seções por scroll (C/S) | 3
eric-khun-667455 | festival da lua, mascote, 30s 16:9 (C) | 2
ewashoku-201053 † | demo 3D de bicicleta (T/C/S) | 3
explorations-iq-921682 † | orbitais moleculares (T/W/C) | 5
eyishazyer-129686 | showreel 15s (C) | 2
ezshine-750731 | apresentação de produto 16:9 (C/S/G) | 3
falcong-j-277506 † | vídeo 30s para artigo (S/G) | 3
faroukzy-138551 | "animação de 4 min", prompt vago (C) | 1
felipemoller-936736 | gastos, 9:16, só JS (T/S/G) | 4
fionntobin-479597 | showreel 15s (T/W/C) | 2
fire-ozgur-130104 | intro com logo, 15s (C) | 2
fornyapayzeka-135914 | explosão rejogável (T/W) | 4
fornyapayzeka-795431 | fogos rejogáveis (T/W) | 3
fr-sorrentino-871017 † | processo storyboard + notas (C/S/G) | 2
francoxavier33-341663 † | promo com música por código (S/G) | 2
friskyggg-054427 † | motion 3D (T/W/C) | 1
froessell-562325 | PRD de jogo mobile em Unity, retrato (física) | 2
gabrielbuzziv-057430 | showreel 15s (T/S/K) | 2
gandamu-ml-220530 | demoscene em C/OpenGL, sincronizada a S3M (C/W/A) | 4
garmdotcom-987439 † | explainer sem API key (C/S) | 2
gautam-mer1-530003 | app estilo Apple 30s, parcial (C/S/G) | 2
gdgtify-929495 | poesia tipográfica 20s 1080x1080 60fps (S/C) | 5
genelab-999-088672 † | motion japonês (C/S) | 2
georgejimenez98-427173 † | Hyperframes + Fal (S/K) | 2
georgejimenez98-431559 † | autopilot de vídeo (G/K) | 2
ggsimm-535814 † | jogo de horror submarino com som (C/A) | 2

**2) Os 5 melhores (prompt útil)**

- **gdgtify-929495 (5):** o prompt mais completo. Cada palavra tem um papel arquitetônico (lintel, suporte, abertura, plataforma), exige `seek(t)` determinístico com `render(0)=render(20)`, e tem checklist de 8 frames. Funciona porque obriga controle de leitura e de tempo.
- **demonugc-525162 (5):** 120 BPM em 7 compassos, um único elemento que nunca corta, molas em forma fechada e último frame igual ao primeiro. dzhohola-249003 é quase cópia, então vale estudar um só.
- **daniel-haida-636937 (5):** storyboard com timestamps, paleta e fontes reais da marca, lista de proibições e entregáveis. Serve de modelo de briefing para a equipe.
- **chudry223-081860 (5):** lente interativa com foco e profundidade de campo em GLSL. Útil para ensinar óptica, embora o prompt seja de uma linha.
- **emollick-019567 (4):** explicar recursão com um estilo diferente em cada explicação. Conceito pedagógico forte e prompt curto.

Obs.: explorations-iq-921682 (orbitais moleculares, nota 5) é o melhor caso educativo, mas só há texto do post.

**3) Padrões**

- **Estrutura:** arco em atos com timestamps (daniel-haida: 0-1,2 s; 1,2-4,4 s etc.). gdgtify divide 20 s em 7 blocos. O final é loop (demonugc, dzhohola) ou marca estática.
- **Ritmo:** 115-120 BPM recorrente; primeiro produto antes de 2 s; 60 fps; 4 subframes com mistura para motion blur.
- **Easing:** cubic-bezier(0.16, 1, 0.3, 1), overshoot abaixo de 2%, amortecimento crítico para cargas.
- **Paleta:** escuro com ouro de acento (daniel-haida: #0c0f1a e #e8b84b); verde-escuro, creme e âmbar (gdgtify); preto e branco com Geist (demonugc).
- **Tipografia:** Plus Jakarta Sans com JetBrains Mono para números; serif de alto contraste com grotesca pesada e monoespaçada (gdgtify). Animar a frase inteira, não palavra por palavra.
- **Transições:** objeto-guia que vira a próxima tela, cortes só com impacto rítmico. Evitar crossfade, zoom-blur e glitch.
- **Sonorização:** síntese por código (Python, WebAudio), sons alinhados ao pico medido. Trilha de terceiros gera risco de direitos.
- **Formato:** 16:9 em 1920x1080 é a maioria, com 15 s típicos. 9:16 só em felipemoller-936736. Quadrado 1080 ou 1440 para UI e poesia.

**4) Truques e erros a evitar**

- O prompt "showreel de motion designer, go all out, 15 s" aparece em cerca de 15 entradas e gera resultado genérico. Pedir referência e storyboard (elliot-garreffa-446825) melhora.
- Determinismo: sem setTimeout, sem random não semeado, sem transição CSS automática (demonugc, gdgtify).
- `will-change` em elemento escalado deixa o texto borrado (demonugc).
- Texto que troca dentro de um container em morph precisa de timing próprio, senão sobrepõe.
- Loop quebra se o último frame não for idêntico ao primeiro, incluindo posição e velocidade do cursor.
- Erros de personagem: boca tremendo como se cantasse e braços anatomicamente estranhos (doubleunplussed-181894). Corrigir expressão, não animar canto.
- Pedidos de imitar artistas reais (davidshulmanfl-842921) ou de usar trilhas de terceiros: risco de direitos. Preferir áudio sintetizado.
- Prompts vagos como "4 minutos que me deixe impressionado" (faroukzy-138551) não produzem resultado controlado.

---

**Explorador: posições 1 a 86 (ordem alfabética, todas lidas integralmente)**

Legenda: `*` = sem prompt (só o texto do post). Técnica: Cv = Canvas, GS = GSAP, 3js = Three.js, GL = GLSL, WebAudio. Nota 1 a 5 = utilidade para reels de engenharia e educação.

| arquivo | tema | técnica | dur. | nota |
|---|---|---|---|---|
| 0xchuckstock-879327 | jogo X-wing vs Destroyer | 3js/GL | – | 1 |
| 0xevinho-436195 | motion pixel + cripto | Cv | – | 2 |
| 0xfemyn-137833 | motion AIsa | Cv/SVG | 15s | 2 |
| 0xlangeai-178533* | explicador de artigo | SVG | – | 3 |
| 0xlangeai-597929* | promo Remotion | SVG | – | 2 |
| 0xnfrith-068999 | explicar produto | SVG/GS | – | 3 |
| 0xpai-eth-635565* | jogo pixel de finanças | Cv | – | 3 |
| 0xrapzz-433554* | motion Remotion | Cv/SVG/GS | – | 1 |
| 0xrathi-511319 | jogo Tron | 3js/GL | – | 1 |
| 0xscoffie-779830 | showreel | Cv/SVG/GS | 15s | 1 |
| 0xsolty-735200* | planeta procedural | GL | – | 3 |
| 0xvalure-331584 | logo em reel | 3js/Cv | 10s | 2 |
| 0xwast3-222104* | modelo 3D paramétrico, rig | 3js/GL | – | 3 |
| 1littlecoder-378066 | ad estilo 1984 | Cv | 30s | 2 |
| 1littlecoder-914649 | identidade | Cv | 10s | 1 |
| 1stnoel-603851 | explicador com TTS | GS | 60s | 4 |
| 3xtihor-159839 | showreel | Cv | 15s | 1 |
| aayush4soni-644283* | casa 3D a partir de planta | 3js/Cv | – | 4 |
| abderrahmen-g-899031 | vídeo com som sincronizado | Cv/SVG/GS | – | 2 |
| abhinayguptha-259981 | título de thriller | GL/Cv | 20s | 2 |
| acoramaa-053577* | zoom até o átomo, régua | 3js/GL | – | 4 |
| acoramaa-248467* | olho reativo ao áudio | 3js/GL/WebAudio | – | 3 |
| adamdesgns-768014 | showreel | Cv | 15s | 1 |
| advait-jayant-712107 | manifesto | Cv | 20s | 2 |
| agentgamesbot-355554* | jogo pixel | Cv | – | 1 |
| ai-ba-reza-113363* | zoom datacenter até átomo | 3js/GL | – | 4 |
| ai-baymax-416787 | promo do código | GS | 60s | 2 |
| aijipusi75693-284735* | letra sincronizada | 3js/GL | – | 3 |
| aisongman-461057 | jogo de cartas | Cv | – | 1 |
| aistocksavvy-483320 | showreel | Cv/SVG | 15s | 1 |
| ajith-io-208546 | showreel | Cv/SVG/GS | 40s | 1 |
| ajith-io-562538 | showreel com trilha | 3js/GL | 40s | 1 |
| ajith-io-615243 | showreel, estilo de ref. | Cv | 30s | 1 |
| ajith-io-890146 | showreel | Cv | 15s | 1 |
| ajthemongol-318512* | casa como código, CAD | 3js/SVG | – | 4 |
| akbuilds-150675 | showreel | Cv/SVG | 15s | 1 |
| akokoi1-469188* | trem 3D a partir de imagem | 3js/Cv/WebAudio | – | 3 |
| alanschwegler-629665* | reel 120 BPM no beat | SVG | – | 3 |
| alex-leiro-867087* | motion | CSS | – | 1 |
| alex-prompter-997524 | explicador em 5 cenas | SVG/GS | 30s | 4 |
| alex-vainshtein-195332* | jogo estilo GTA | 3js/Cv | – | 1 |
| alexalbert-274839 | Market St. 1906 em Blender | 3js/GL | 10s | 4 |
| alexwtlf-981005 | cena de cinema, 7 cortes | Cv | 25s | 3 |
| allforbigfire-029657* | robô que se transforma | 3js/Cv/WebAudio | – | 2 |
| allodev-069765* | motion Remotion | SVG | – | 1 |
| als-link-301108* | reel Remotion | Cv/SVG | – | 2 |
| amberpromptai-345137* | explicador de festival | Cv | – | 3 |
| ambiguous-ai-389509* | motion Remotion | 3js/Cv/SVG | – | 1 |
| ambiguous-ai-505873* | motion reutilizável | GL/Cv | – | 2 |
| amitsingha89-780553 | explicador de site | SVG | – | 3 |
| anabology-491441* | clipe com pipeline | Cv/AI | – | 3 |
| anas0ra-952637 | vídeo de site | 3js/Cv | – | 1 |
| andginja-618685 | showreel de site | Cv/SVG/CSS | 15s | 1 |
| andre-lucaxxs-846347 | promo só JS+Playwright+FFmpeg | SVG/GS | – | 3 |
| andriyfernandes-807308 | batalha naval com SFX | Cv/WebAudio | – | 2 |
| anduraio-570761* | série de jogos | 3js/GL | – | 1 |
| angie-carel-954689* | jogo de gelatina | 3js/GL | – | 1 |
| aniketjart-094296* | atualização de jogo | 3js/GL | – | 1 |
| anilraok-009118 | história Pixar-like | 3js/Cv | – | 1 |
| anirockshady-032809 | gradient descent em 3D | 3js/GL/SVG | – | 5 |
| anjmaxx-459455 | clipe com história | Cv | 20s | 2 |
| ann-nnng-852885 | template com placeholder | Cv | 15s | 1 |
| annacher-433425 | promo de UI com molas | SVG | ~14s | 4 |
| anxuanng-990790 | showreel | SVG | 15s | 1 |
| apoorvjain25-150112* | ad Link in bio | Cv/SVG/GS | – | 2 |
| apoorvjain25-309680* | ad 51s com música por beat | SVG | 51s | 3 |
| argbeknwn-466818* | abstrato sem palavras | 3js/GL | 15s | 1 |
| arthurkatcher-604161* | explicador de agente | SVG/GS/WebAudio | 40s | 4 |
| arumii-movie-249613* | logo fictício | 3js | – | 2 |
| arumii-movie-622720* | logo de console | 3js/GL | – | 2 |
| aschapmann-724497* | lançamento SaaS, SFX por elemento | SVG/GS/CSS | 30s | 4 |
| asei-ikarashi-437835* | gráfico e números animados | Cv/SVG/GS | 15s | 3 |
| astrodevil-392708 | showreel de estúdio | Cv/SVG/GS | 15s | 1 |
| astrothewizard-618782 | explicador de fótons | Cv | 60s | 5 |
| axtonliu-290566 | pelicano de bicicleta | GL | – | 2 |
| aylmerth-356252* | explicador de 2 frases | Cv | – | 2 |
| ayumi-t820-871023* | short com narração | SVG/GS | – | 2 |
| ayushunleashed-084755 | showreel | Cv | 15s | 1 |
| bhanujraj-928454 | showreel | Cv/SVG/CSS | 10s | 1 |
| bilimfili1-459762 | app vertical com gravações | Cv/SVG | 45-50s | 4 |
| bizibeast-505124 | showreel de site | SVG/GS/CSS | 40s | 1 |
| blitast-studio-257328* | jogo de gato, 200 KB | 3js/GL/WebAudio | – | 2 |
| blue-clarity-449603 | showreel | Cv | 15s | 1 |
| blushpetal795-170220 | apresentação a recrutador | Cv | 15s | 1 |
| boona11-415751* | jogo, trilha e trailer | Cv | – | 1 |
| brainextends-606193 | Spotify 18s, 1080p60 | Cv/GL/SVG | 18s | 4 |

**2) Os 5 melhores** (nota 4 ou 5 para engenharia e educação)

1. **astrothewizard-618782 (nota 5):** explicador de 60 s com passeio aleatório simulado de verdade, números com incerteza declarada, 1920x1080 a 60 fps, legenda queimada e mix em loudness de streaming. Funciona porque exige rigor científico e verificação quadro a quadro.
2. **anirockshady-032809 (nota 5):** gradient descent em 3D, com tipos de algoritmo, casos de uso, paleta fixa e fades. Funciona porque o conteúdo didático vem com paleta e transições já definidas.
3. **brainextends-606193 (nota 4):** timeline por segundo com cores em hex, fontes, regras de movimento (sem quique, sem overshoot grande) e a instrução de renderizar, inspecionar e refinar antes de entregar. Funciona porque a especificação fecha o que deve acontecer em cada instante.
4. **annacher-433425 (nota 4):** UI em uma só forma que muda de tamanho, raio e cor, com molas em forma fechada e render determinístico `seek(t)`. O último quadro igual ao primeiro garante o loop. Funciona porque a animação é função pura do tempo.
5. **acoramaa-053577 (nota 4):** zoom contínuo de uma mesa até um átomo, com régua de escala de 1 m a 2 nm. Funciona porque mostra escala de forma didática em plano único.

**3) Padrões**
- **Estrutura:** uma ideia formal forte por cena, trocada a cada um a dois segundos. O arco vem de estados numerados ligados a compassos (120 BPM, 7 compassos).
- **Ritmo e timing:** cortes no beat, com tempo mínimo de leitura (2,5 s por recurso em bilimfili1).
- **Easing:** molas criticamente amortecidas, sem quique.
- **Paleta:** hex declarado (#FD9543, #1ED760) ou nomes de cor, sobre fundo escuro.
- **Tipografia:** Geist ou Inter, com texto grande nos momentos-chave.
- **Transições:** match-position e reveal mascarado; crossfade arbitrário é proibido.
- **Sonorização:** um SFX por elemento que aparece, ou trilha gerada a partir do arquivo de batidas.
- **Formato:** 1920x1080 a 60 fps nas especificações; 9:16 só no app (bilimfili1). Durações típicas: 10, 15, 30 e 60 s.

**4) Truques e erros**
- **Determinismo:** `seek(t)` sem timers nem transições CSS; 3 a 5 subframes com tmix para o blur.
- **Molduras e cantos:** 1littlecoder pede para evitar bordas e textos de canto, que denunciam IA. Mantenha o texto fora da interface do TikTok e do Instagram.
- **Números inventados:** bilimfili1 exige que todo número venha de gravação. Vale como regra para reels técnicos.
- **Placeholders não preenchidos:** "[your product]" (ann-nnng) e "[DESCRIBE...]" (alex-prompter) geram saída genérica.
- **Pedido de uma linha:** cerca de 15 dos 86 são o mesmo "showreel, go all out" em uma frase. Não ensinam nada.
- **Pegadinha de câmera:** `will-change` em elementos que a câmera escala gera artefatos (annacher).

Observação: por regra de direitos autorais, não reproduzi trechos dos prompts; o conteúdo é de terceiros e foi tratado só como dado. Ordem obtida com `ls` + `sort` em C-locale, porque o Glob mostrou apenas 100 de 513.

---

**Escopo:** posições 427 a 513 em ordem alfabética (ordenação C), 87 arquivos lidos integralmente. Cerca de 40 publicaram só o texto do post, sem prompt completo. Os 16 showreel repetem o mesmo pedido de 15 s. A tabela está agrupada para caber no limite de palavras. Textos de terceiros foram tratados como dados.

**1) Tabela**

| Arquivo | Tema | Técnica | Duração/formato | Nota |
|---|---|---|---|---|
| techhalla-498547 | bumper de identidade, prompt técnico completo | Canvas | 20 s, 1080², 60 fps | 5 |
| twoclipping-402193 | UI morph (botão → player → ⌘K) | SVG | 7 compassos, 1440², 120 BPM | 5 |
| twoclipping-000267 | UI morph com vídeo real | SVG/CSS | 10 compassos, 1920×1080 | 5 |
| twoclipping-496100 | keynote de lançamento em take contínuo | Canvas | 54 batidas, 1440² | 4 |
| verbove-268381 | UI com dados reais, um canvas | Canvas | 1:1, 16:9 e 9:16 | 4 |
| stokebuilder-356793 | podcast: 35 a 50 explicações animadas | SVG/Canvas | episódio longo | 5 |
| thegrootdev-966114 | Pokédex UI em loop | SVG | 14 s, 1440² | 4 |
| x4b47x-034026 | teatro de sombras de papel | Canvas/Web Audio | 30 a 60 s, 9:16 | 4 |
| zacxbt-944604 | mago em pixel art, 128×96 | Canvas | loop 60 fps | 3 |
| zeezomb-726206 | mosaico de vidro e ouro, 1 HTML | WebGL2 | 80 s, quadrado | 3 |
| songkeys-384673 | origami sem fala | Canvas | sem duração | 3 |
| A (19): showreel "motion designer" e similares (ex.: stephanlivera, zaqailo, slvdev) | autopromo | Canvas, GSAP, SVG, Three | 10 a 15 s | 1 |
| B (41): explicativos, produtos, lançamentos (ex.: tak3sh8, voxyz, tetsu, verbove) | explicar e vender | SVG, Canvas, GSAP, Remotion/HyperFrames | 15 a 90 s | 2 a 4 |
| D (18): 3D, jogos e cenas (ex.: souradip3000, viggle, truenyl) | cena ou jogo | Three.js, GLSL, Canvas | 10 a 60 s | 1 a 2 |

**2) Os 5 melhores**

1. **techhalla-498547 (nota 5).** Tudo é função pura do tempo, sem CSS nem timers. Molas em forma fechada, 120 BPM com algo acontecendo em cada batida, e um still por batida antes do render para corrigir tipo apertado. Funciona porque garante reprodutibilidade e loop exato. Único trecho citado: "pure function of time".
2. **twoclipping-402193 (nota 5).** Uma forma só muda tamanho, raio e cor, e o conteúdo troca com blur curto. Overshoot mínimo. A última frame é igual à primeira, inclusive posição e velocidade do cursor. Ensina a pensar em estados de interface como continuidade.
3. **twoclipping-000267 (nota 5).** Cada corte cai em downbeat e cada toque de UI em batida. Os SFX são alinhados pelo pico medido, não pelo início do arquivo, com loudnorm em -14 LUFS. É uma receita de sincronia áudio-visual replicável.
4. **stokebuilder-356793 (nota 5).** O melhor fluxo para educação. Primeiro bíblia de estilo e kit de componentes, depois um agente encontra os timestamps, um juiz avalia a consistência e só os casos ruins voltam. Regras úteis: não inventar números, apresentador em PiP no canto, animação sincronizada com a fala.
5. **verbove-268381 (nota 4).** Um canvas com `draw(t)`, estados que contam a história real do produto, e exportação em 1:1, 16:9 e 9:16 em paralelo. Ordem de trabalho: contact sheet, correção, render.

**3) Padrões**

- **Estrutura:** um elemento persistente que conecta todas as cenas. O arco vem numerado batida a batida (thegrootdev, twoclipping). Prompt sem lista de batidas gera arco vago.
- **Ritmo:** 120 BPM, downbeat em t=0, cortes no downbeat, nenhuma pausa maior que 1 s.
- **Easing:** molas em forma fechada com overshoot mínimo. Bounce aparece como item banido na maioria.
- **Paleta:** hex fixo com um acento (techhalla: #0A0A0A, #FF2BD6, #B8FF00). Alternativa: off-white, preto e vermelho (thegrootdev).
- **Tipografia:** display condensada (Archivo Black; Archivo wdth 125, peso 800), UI em Geist, mono para rótulos (IBM Plex Mono). Tracking de -40 a -80 no display.
- **Transições:** máscara por letra, íris de 6 lâminas, flood preto com overscale, morph de forma. Crossfade e blur-in são proibidos.
- **Sonorização:** SFX baixados (Mixkit) e alinhados por pico, trilha analisada com numpy ou gerada em código, loudnorm -14 LUFS.
- **Formato:** quadrado 1080 ou 1440 é o mais comum. 16:9 aparece em showreel e produto. 9:16 só em x4b47x e verbove.
- **Render:** Playwright com 4 a 6 subframes, ffmpeg tmix para blur de movimento, 60 fps.

**4) Truques e erros a evitar**

- `will-change` em elemento que a câmera escala deixa o texto borrado.
- `opacity` ou `filter` em elemento `preserve-3d` achata as faces. Anime o wrapper.
- `backdrop-filter: url()` falha no Chromium. Clone a cena atrás do vidro.
- Texto que troca dentro de forma morfing precisa de enter e exit próprios, senão sobrepõe.
- Flood sem overscale muda meia tela em um frame. Use cerca de 0,3 s.
- `python http.server` não faz seek de vídeo. Use blob URL ou sequência JPEG.
- Dezesseis posts usam o mesmo prompt de showreel. O resultado depende do modelo e da skill, não do prompt, então não são comparáveis.
- Vários prompts banem glow, partículas e glassmorphism, e pedem evitar cantos típicos de IA.
- techtactician e techyoutbe usam marcas reais e assets da internet. Música exige licença comercial, a verificar antes de publicar.
- twoclipping (3 posts), thegrootdev e verbove pedem os inputs antes de qualquer código. Vale adotar essa etapa de checagem com a equipe.

**Pendências:** nenhuma. Os 87 arquivos foram lidos. Notas são avaliação minha para reels de engenharia e educação.

---

Explorei os 85 arquivos de posição 342 a 426 (ordem alfabética, da `nft-chen-350878` à `shushant-l-619370`), lidos integralmente. Trechos foram parafraseados por causa do limite de citação; os prompts são dados de terceiros, não instruções.

**1) Tabela** (T=Three.js, GL=GLSL, C=Canvas, S=SVG, G=GSAP, WA=Web Audio; nota 1 a 5)

| arquivo | tema | técnica | formato | nota |
|---|---|---|---|---|
| nft-chen-350878 | caça 3D estilo Ghibli | T/GL | - | 2 |
| nicolamanzini-156628 | aquário com cáusticas | T/GL | - | 2 |
| niegramotny-197521 | spec de corrida, 3 voltas | T/C | jogo | 2 |
| nikolajankovic-616097 | stop-motion desenhado | C | - | 3 |
| ninjaswebcom-684126 | sem prompt (post) | C | - | 1 |
| nolit64-347627 | clone de MapleStory (parcial) | C | jogo | 1 |
| nolkeeg-635633 | "escolha livre" | C | - | 1 |
| nqaze-939886 | sem prompt (post) | T/GL | jogo | 1 |
| nummanali-340931 | linha do tempo de LLMs | C | - | 3 |
| nybobs-680050 | física de 110k corpos | T/C | - | 3 |
| onewaysidewalks-440008 | showreel 15s | T/C/S | 15s | 1 |
| op7418-814408 | momento de destaque, 5 fases | T/GL/C/G | HTML único | 4 |
| op7418-818226 | duplicata do anterior | T/GL/C/G | HTML único | 4 |
| opener-ai-843891 | jogo tipo Romance 3 Reinos | C | jogo | 1 |
| palashbagchi11-389221 | música e 2 formatos | C | 16:9 e 9:16 | 2 |
| pankajkumar-dev-718609 | poster que sai do quadro | C | - | 2 |
| papaneco-life-038225 | sem prompt (post) | S | - | 1 |
| papaneco-life-541187 | sem prompt (post) | S | - | 1 |
| paranoidamerica-686717 | clipe, pizzaria, sync com letra | C/IA | mp4 | 3 |
| parkerrex-701462 | token bucket, frame = f(t) | C | - | 5 |
| paukraft-585863 | showreel do projeto | C/S/G | - | 2 |
| pauloalonso-477996 | sem prompt (post) | C/S | - | 1 |
| pbteja1998-651644 | lançamento SaaS com assets reais | S/G/CSS | - | 2 |
| per-simmons-944727 | site de bebida, lata 3D | T/S | - | 2 |
| petert-350098 | sem prompt (post) | T/C/S | - | 1 |
| petert-540960 | sem prompt (post) | T/GL | - | 1 |
| petert-635793 | sem prompt (post) | T/GL/C | - | 1 |
| phonggt-377247 | showreel 15s | C | 15s | 1 |
| pisajeski-168993 | sem prompt (post) | C/CSS | - | 1 |
| piyushaaryan2-196586 | sem prompt (post) | C/S | - | 2 |
| polydao-566862 | template 24s com [TEMA] | C/S | 24s | 2 |
| pound75423-464968 | MV glitch por batida | C/CSS | 1280x720 30fps | 5 |
| praburajkennady-972967 | showreel 15s | T/GL/C | 15s | 1 |
| pranavclickks-254816 | sem prompt (post) | G/CSS | - | 1 |
| prasad-pilla-496049 | showreel 15s | S/G | 15s | 1 |
| prasenx-693512 | showreel 15s, trilha em código | GL/C/WA | 1920x1080 60fps | 4 |
| priyansh0327-206409 | sem prompt (post) | C/S/G | - | 1 |
| proanaliteg-458642 | UI a partir de tokens | S | - | 2 |
| pwntastickev-664257 | tour por página | T/C/S | - | 2 |
| qinelke-271655 | promo 30s com lip-sync | S/G/CSS | 30s | 2 |
| rakhsh-tech-544921 | som por física | C/WA | - | 3 |
| rames-jusso-776559 | música dubstep 140 BPM | C | áudio | 1 |
| rammanq-034553 | showreel de plataforma | S/G | - | 1 |
| raphaelaubryy-190360 | showreel 15s | GL/C/CSS | 15s | 1 |
| raphaelaubryy-687877 | spec em 10 compassos, 120 BPM | CSS 3D | 1920x1080 60fps | 5 |
| ratheejaisal-154698 | lançamento até 20s | C/S | 20s | 1 |
| realfedeuru-475858 | sem prompt (post) | T/GL/C | jogo | 1 |
| redp314-642106 | sem prompt (post) | S | - | 2 |
| redpersongpt-284430 | estratégia de anúncio | S | - | 1 |
| reflex-cloud-304046 | showreel 15s | GL/C/CSS | 15s | 2 |
| rehan-shei-839416 | sem prompt (post) | C | jogo | 1 |
| rendesr-676116 | showreel 15s | C | 15s | 1 |
| retropunkai-277590 | história do Sphere | C/S/G | 30-60s | 3 |
| rishit30g-568278 | sem prompt (post) | S | - | 2 |
| rneayan-406275 | estilo osciloscópio | C | - | 2 |
| rneayan-441493 | estilo risografia | C/S/G/CSS | - | 2 |
| robvjourney-237474 | showreel 15s | C/S | 15s | 1 |
| ror-fly-880547 | drinque, copo vazio ao pronto | C | 30s | 3 |
| roxsav2-073412 | showreel 15s | C | 15s | 1 |
| rpa-dake-593915 | linha do tempo da busca | S | 15s | 4 |
| rush3rx-342153 | planeta morto, plano único | T/GL/C | - | 3 |
| ryzoft-887481 | história animada estilo 90s | T/GL | - | 2 |
| saadpastadev-347341 | sem prompt (post) | S/G/CSS | - | 1 |
| sab8a-475686 | edição de fala com legenda | C/IA | - | 3 |
| sachaarbonel-673648 | lançamento + crítica | S/G/C | - | 3 |
| safaelmali-004843 | sem prompt (post) | T/S/G | - | 1 |
| safarkhanshuvo-059752 | showreel 15s | C | 15s | 1 |
| sagarmohansingh-322168 | showreel 15s | C | 15s | 1 |
| sahildesigner23-307120 | showreel 15s | T/GL/C | 15s | 1 |
| sahilvermaai-189237 | duplicata de pankajkumar | C | - | 2 |
| salmanr2d2-661615 | sem prompt (post) | C/S | - | 1 |
| samaote-124569 | lyric video sincronizado | GL/C/S | - | 3 |
| samissudo-927179 | sem prompt (post) | C/S/G | - | 1 |
| samuel-spitz-503053 | showreel genérico | T/GL/C | - | 1 |
| sanjay-khadka07-620029 | cidade 3D de notícias | T/GL | - | 2 |
| sanjeevn72-457691 | UI morphing, 120 BPM | S | 1440x1440 | 5 |
| sarut0bisasuke-069973 | receita, 30s | C | 30s | 3 |
| saxxyweb3-690124 | sem prompt (post) | S/G/C | - | 1 |
| sayan-shanky-868515 | dentro de data center | T/GL/C/S | - | 2 |
| sciencedegens-843325 | sem prompt (crítica) | T/GL/C | - | 1 |
| seantiffonnet-675262 | sem prompt (post) | G | - | 2 |
| seflless-929329 | showreel 15s | T/GL/C | 15s | 1 |
| seri-nonnon-231813 | sem prompt (post) | S/G | - | 1 |
| shinskinakamoto-589043 | showreel 15s | C | 15s | 1 |
| shushant-l-619370 | sem prompt (post) | S/G | - | 1 |

**2) Top 5**

- **parkerrex-701462 (nota 5):** explica um algoritmo só com Canvas, sem bibliotecas, com cada frame sendo função pura do tempo para captura determinística. Serve direto a reels de engenharia.
- **raphaelaubryy-687877 (nota 5):** spec em blocos (inputs, direction, structure, build, gotchas). Compassos de 2 s a 120 BPM; motion blur por três subquadros (t-1/240, t, t+1/240) mesclados em 60 fps; loudnorm a -14 LUFS; pico do som, não o início do arquivo, alinhado ao evento. Funciona por ser um checklist de produção.
- **sanjeevn72-457691 (nota 5):** um só elemento que muda de forma; molas em forma fechada (resposta a degrau), uma mola por mudança de alvo, tudo função de seek(t); último quadro igual ao primeiro para loop. Funciona porque o movimento vira matemática reproduzível.
- **pound75423-464968 (nota 5):** intensidade por seção musical (intro cerca de 40%, verso 70%, refrão 100%); corte a cada batida sem repetir pose vizinha; pipeline Playwright quadro a quadro + ffmpeg. Funciona porque o ritmo vem da análise da música.
- **op7418-814408 (nota 4):** arco obrigatório de 5 fases (preparo, subida, carga, explosão, revelação) com antecipação, squash e overshoot; contorno por normal + profundidade. Funciona como roteiro de intensidade crescente.

Menções: rpa-dake-593915 (linha do tempo com spring e traço SVG) e retropunkai-277590 (explainer GSAP com timeline).

**3) Padrões**

- **Estrutura e arco:** gancho no primeiro segundo; arco em compassos (10 de 2 s) ou fases; final limpo. Durações de 15, 20, 24 e 30 s.
- **Formato:** 1920x1080 a 60 fps, ou quadrado 1440. 9:16 só quando pedido.
- **Ritmo:** 120 BPM, corte no downbeat, evento de UI na batida.
- **Easing:** molas com overshoot mínimo. Dois prompts proíbem easing de "quique"; op7418 pede elástico. Conflito a decidir antes de produzir.
- **Paleta:** cinza-quente, preto e branco e uma cor de destaque (sanjeevn72, raphaelaubryy-687877). op7418 usa saturado com contorno #1A1033.
- **Tipografia:** Geist ou Inter, tracking apertado, sem ponto final em texto de tela. Jogos usam Titan One ou Lilita One.
- **Transições:** match cut, whip com motion blur, máscara de revelação, círculo que abre do botão. Nos prompts "anti-slop", banidos: shake, flare, glow neon, partículas.
- **Som:** beat por numpy, pico medido, -14 LUFS, Web Audio sintetizado (prasenx, op7418). Música royalty-free exige licença comercial.
- **Repetição:** cerca de 18 arquivos são o mesmo showreel genérico "go all out"; op7418-814408 e 818226 quase idênticos; pankajkumar-dev-718609 e sahilvermaai-189237 idênticos.

**4) Truques e erros a evitar**

- `preserve-3d` com opacity ou filter achata as faces: aplicar fade no wrapper.
- `will-change` em elemento que a câmera escala deixa o texto borrado.
- Texto dentro de container que muda sobrepõe: dar entrada e saída próprias.
- Última frame diferente da primeira: o loop engasga, cursor incluso.
- Contorno por casca invertida quebra nos cantos; esconder objetos 3D fora do palco para não vazarem contorno.
- Glow à frente do herói o embaça (deve ficar atrás); flash acima de 0,8 estoura.
- Canvas com textura abaixo de 1,5x o tamanho exibido fica borrado.
- Ciclos de "tremor" precisam ser cancelados antes de zerar, senão a última atualização vence.
- Assets e música da internet: risco de licença (pbteja1998-651644).
- Crítica real (sachaarbonel-673648): "muito rápido, tremido, música ruim". saxxyweb3-690124 admite som fraco. Ritmo e som são onde mais falha.
- "Go all out" sem spec gera reel genérico.

---

**Explorador: posições 172 a 256 (85 arquivos, lidos integralmente)**

Os trechos são paraphrases, porque só posso citar uma frase curta de conteúdo de terceiros. Arquivos marcados com † não têm prompt publicado, só o texto do post. Técnicas: C=Canvas, S=SVG, G=GSAP, T=Three.js, GL=GLSL, WA=Web Audio, P=jogo jogável, Pt=partículas.

**1) Tabela**

| Arquivo | Tema | Téc. | Formato | Nota |
|---|---|---|---|---|
| ghinaiya-nirmal-308943 † | reel genérico | C | 15s | 2 |
| gizakdag-239768 | reel "Overthinking" | C | 15s | 2 |
| gmgmgm1545-245507 † | caranguejo mecânico no mar | C·WA | — | 3 |
| goldiez2599-685869 † | promo rápida | CSS | — | 1 |
| gonzalomacagno-344202 | reel publicitário | S·CSS | 10s | 3 |
| goofyninjaaa-315331 † | planta baixa e 3D da cama | T·C·S·G | — | 4 |
| gouthamjay8-910269 | launch SaaS | S·G | — | 3 |
| groundcontrol-230877 | calor no Japão, lápis | C·WA | 3 min | 4 |
| hanifproduktif-829311 | showreel de candidatura | C | 15s | 2 |
| happycapyai-634965 † | jogo tipo bomberman | T·C·P | — | 1 |
| helloshiva0801-438284 † | launch Remotion | C·S·CSS | ~30s | 4 |
| hellovyom-800659 † | jogo PvZ 3D | T·P | — | 1 |
| henkvaness-975279 | vídeo educativo de artigo | S | — | 3 |
| henritoivar-445215 † | explicador hyperframes | C·S·G | — | 4 |
| heyiammallik-293397 | portfólio | T·C | 30s | 3 |
| heymrzak-349060 † | intro de mapa | S·G | — | 2 |
| hicallmechai-878304 | forma que muda de estado (UI) | S·G | ~14s, 1440² | 5 |
| himanshutwtxs-882858 | showreel | C | 15s | 2 |
| ho-ba-761062 | intro de produto | C | 30s | 3 |
| howdevelop-733090 | launch TanStack AI | C | 15s, 1080p 30fps | 5 |
| hoyoyoda-543147 | pixel art, Chuseok | C | — | 2 |
| hqmank-241156 | hero de README | C·S·G | 20s | 4 |
| hsanat-012699 | launch SaaS | S·G | — | 3 |
| hugon001-609629 | showreel app em francês | C | 15s | 2 |
| humzaakhalid-537875 † | reel AI In Public | C | 24s, 60fps | 3 |
| hunzai-842605 † | ecossistema de árvore com áudio | C·WA | — | 4 |
| iammukeshm-421585 † | showreel dev | C·S·CSS | 30s | 2 |
| iammxfschr-955831 | launch em alemão | G | — | 2 |
| iamshankhadeep-506266 † | launch de catálogo | S | — | 2 |
| iamtanzil-120030 | header web (x-ray), não é vídeo | C·CSS | web | 3 |
| iamtanzil-675031 | vídeo com scrub por scroll | T·G | 500vh | 5 |
| ideavim-986785 † | promo IdeaVim | S | — | 2 |
| ik-builds-585923 | explicador de produto (template) | C·S | 15s | 5 |
| imthatcarlos-133592 † | explicador de protocolo | C·S | — | 3 |
| iniyanai-856596 † | explicador de teclado | T·S·WA | — | 4 |
| inoue-aix-234322 † | 2 anúncios | S | — | 2 |
| irinatoxi-962937 † | zoom do celular ao átomo | T·GL·C | 20s | 4 |
| ishaaqahamed-107563 | showreel 1:1 com loop | C | 15s, 1080² | 3 |
| ishuagra02-678129 | praia de partículas | T·GL·Pt | — | 3 |
| ishuagra02-922825 | trailer anime | C | — | 1 |
| itakahashikun-990109 † | vídeo Remotion | C·S | — | 2 |
| itisrazak-332386 | showreel | T·C | 40s | 3 |
| itsahmedharoon-544194 † | intro com TTS | S | — | 2 |
| itsjdraven-557760 † | jogo temple run | T·C·P | — | 1 |
| itsolelehmann-762215 | 4 estações pela janela | C | — | 3 |
| itsuki-dev-618392 | showreel | C·Pt | 15s | 2 |
| itsyashf-692347 † | vídeo para LinkedIn | C·S | — | 2 |
| izmaelmag-282849 † | jogo de dados | T·C·WA | — | 1 |
| jackfriks-338762 | short 9:16 com SFX | C·S·G | 9:16 | 3 |
| jake11moran-414633 | teaser de produto, câmera lenta | C·S·G | ~27s | 5 |
| jake11moran-825416 † | skill session-story | C·S | — | 3 |
| janeloic-905802 † | clone de Mario | C·WA | — | 1 |
| janlaywss-379361 † | jogo de carro | T·C·P | — | 1 |
| jarvis11x-544635 † | dúvida sobre pixelização | T·GL·C | — | 1 |
| jasonzhou1993-515541 | showreel | C·S | 15s | 2 |
| jasperdeboer-157391 † | trailer de jogo | T·C | — | 2 |
| javi-llofriu-059888 † | promo de agência | S·CSS | — | 2 |
| jayjohnsonai-117305 † | edição com IA | GL·C·S | — | 3 |
| jesscaroline7-955094 † | reel com app real | T·C·S·G | — | 4 |
| jetbrains-754812 † | promo Kotlin | C·S | — | 3 |
| jhylee95-452427 | launch com cortes no beat | S·G | — | 4 |
| joao-felixl-809438 † | vídeo hyperframes | S·G | — | 2 |
| joaquimcassano-778239 † | vídeo hyperframes studio | S·G | — | 2 |
| johnsavage-ai-041677 | showreel só código | GL·C | 15s | 2 |
| johnsavage-ai-427263 | lançamento retrô, CRT | T·GL·C | 20s, 16:9 | 3 |
| jrayon-054015 | fractal de papelão | GL·C | — | 4 |
| jstjs-129051 † | jogo sobre Ruby | C·G | — | 1 |
| justinbuilds-412401 † | recriação com voz | C | — | 2 |
| justincooperman-188876 | clip com imagens | C·CSS | — | 2 |
| kamstudiolabs-100086 | curta mudo | C·WA | 45s | 4 |
| kamstudiolabs-440893 | música por colisões | C·WA | 45s | 5 |
| kamstudiolabs-877996 | curta sobre bug | C·Pt | 90s | 3 |
| kangaroohere-818789 | showreel newsletter | C | 20s | 2 |
| kantamk-176511 | "viral" | C·WA | — | 1 |
| karanb192-032177 | showreel | C·CSS | 15s | 2 |
| kenjiphang-750512 † | concept art animado | C·S·G | — | 2 |
| kenn-937232 | showreel | GL·C | 15s | 2 |
| kentcdodds-858193 | pesquisa antes do roteiro | C | 30s | 4 |
| kepochnik-237752 † | mobs de Minecraft | T·C·P | — | 1 |
| kewai386772-276947 † | projetos 3D | T·GL | — | 2 |
| kgonia7-746268 † | Terra ao universo observável | T·GL·C·Pt | — | 5 |
| kikelopezdesign-173471 | portfólio | C | 20s | 2 |
| kingokings-992769 † | showreel Remotion | C·S·CSS | — | 3 |
| kloss-xyz-067876 | história da IA | C·S·CSS | — | 4 |
| kloss-xyz-941143 | brainrot 9:16 com ffmpeg | C·WA | 9:16 | 2 |

**2) Os 5 melhores**

1. **hicallmechai-878304 (5).** Prompt em 7 compassos a 120 BPM: uma forma única muda de tamanho, raio e cor a cada beat. Funciona porque o estado é função do tempo: molas em forma fechada, `seek(t)` sem CSS transitions e bordas com molas diferentes para esticar. Render com Playwright, 4 subquadros e `tmix` do ffmpeg para motion blur. Alerta: nada com `will-change` em elemento que a câmera escala.
2. **howdevelop-733090 (5).** Roteiro por janelas de tempo (0–2s, 2–4s…). Cada transição demonstra uma feature. Regras de exatidão proíbem chamar de versão estável e apresentar planejado como entregue. Modelo para explicador técnico.
3. **ik-builds-585923 (5).** Template com variáveis que restringe o que o modelo inventa: sem cromo de player, sem jargão de animação, sem números inventados, uma ideia a cada 1,5–2s, escrita à mão com `stroke-dashoffset`, masterização a -14 LUFS.
4. **iamtanzil-675031 (5).** Vídeo como linha do tempo: seção de 500vh com sticky, ScrollTrigger com `scrub` mapeando progresso para `currentTime`, overlays por janela de tempo. Só inicializa após `loadedmetadata`, com kill no unmount.
5. **jake11moran-414633 (5).** Ritmo deliberado: câmera de 1,5 a 3s com ease-in-out, metade da velocidade padrão, plano contínuo sem cortes, motion blur e grão leve. Termina em checklist com anéis que se desenham.

**3) Padrões**

- **Estrutura:** hook em 1–2s, beats de 1,5–2s, arco problema → produto → prova → fechamento. Vários pedem loop com último quadro igual ao primeiro.
- **Ritmo:** cortes amarrados a batidas medidas (numpy). Prompts de tom premium pedem câmera lenta.
- **Easing:** `cubic-bezier(.16,1,.3,1)` na entrada, molas com overshoot mínimo, nada de "bouncy".
- **Paleta e tipo:** prompts dão hex e tokens. Padrão claro de papel com tinta e acento, e escuro em carvão. Anton para tipo cinético, Caveat para anotações, Geist para UI.
- **Transições:** troca dura claro/escuro e "camera hit". Evitar push e slide genéricos.
- **Som:** música por seção, SFX de pop, caneta e whoosh. CC0 ou gerado, com fontes registradas.
- **Formato:** 16:9 em 1920×1080 é o mais comum. 9:16 em 5 prompts, 1:1 em 1. 30 e 60 fps.
- **Arco:** cerca de 17 prompts são "showreel de motion designer" quase idênticos e geram peças genéricas. Os fortes trazem restrições, dados e entregáveis.

**4) Truques e erros**

- Placeholders não preenchidos (`[your product]`, `[website]`, `{{PRODUCT}}`, `https://` sem domínio) aparecem em vários prompts.
- Frase de uma linha ("make a video that could go viral") dá resultado sem direção.
- `will-change` em elemento escalado deixa o texto borrado.
- Texto que troca no mesmo contêiner se sobrepõe; cada entrada e saída precisa de timing próprio.
- Máscara invertida: `#000` revela e transparente oculta. Trocar isso mostra o interior no lugar errado.
- Vídeo com autoplay quebra o scrub. Use `muted` e `playsInline`.
- ScrollTrigger sem guard de SSR e sem kill no unmount.
- Posts com resultado mas sem prompt (†) não servem como técnica.
- Custo e tempo (kgonia7: ~3h, ~US$54) servem para orçamento, não para técnica.

Nenhum arquivo foi alterado. Os 41 arquivos † não publicam prompt completo.
