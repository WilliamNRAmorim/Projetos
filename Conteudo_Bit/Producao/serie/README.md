# Motor de episódios (animação 2D flat, 1080x1920, 30 fps)

Um episódio é um JSON em `ep/`. O motor (`motor.js`) desenha cenário, personagens e objetos em vetor (canvas), com câmera lenta, entrada/saída, balanço, tremor no susto, faixa "EPISÓDIO N · NOME" no começo, legenda de 2-3 palavras no centro (Oswald bold, branca, com contorno) e faixa final "PARTE N+1 VEM AÍ". Reaproveita `brand.js`, `serve.ps1`, a trilha `stems/music.wav` e o `tts.ps1` da pasta `Producao/`.

## Como rodar
1. `Producao/serve.ps1` (serve em `http://127.0.0.1:5178`).
2. Quadros parados: `http://127.0.0.1:5178/Producao/serie/serie.html?ep=00&t=2` (vários: `&t=1,5,9` vira uma folha; `&safe=1` mostra a área segura).
3. Voz (edge-tts, gratuito): `python Producao\serie\gen_voz_serie_edge.py 01 [--force]` grava `Producao/stems/serie/epXX/cenaN_K.mp3` (K = ordem da fala: `narracao` do narrador primeiro, depois `falas`: `[{"quem":"bia|dalva|osmar|sete|narrador","texto":"..."}]`). O motor toca em fila (sem sobrepor), corta o silêncio das pontas, estica a cena para caber e troca a legenda a cada fala. Vozes em `VOZES` do .py; volume por falante e eco da Dalva em `VOL`/`ECO` do motor. Camadas de áudio no JSON do episódio: `"camadas": {"voz":1,"trilha":0,"efeitos":1}` (trilha 0 = sem música; efeitos por cena: `"efeitos":[{"arquivo":"x.wav","t":1.2,"vol":0.5}]` lidos de `stems/serie/fx/`). O `gen_voz_serie.ps1` (ElevenLabs) ficou obsoleto.
4. MP4: `...serie.html?ep=00&render=1` (H.264+AAC via WebCodecs). Grava em `Semanal/serie/ep00.mp4`. Sem voz ainda: `&render=1&semvoz=1`.
5. Episódio novo: criar `ep/epXX_nome.json` e registrar em `ep/indice.json` (`"01": "ep01_nome.json"`).

## Formato do JSON
```json
{ "numero": 1, "nome": "Sala 4", "proxima": true, "legenda": "palavras",
  "destaque": ["luz"],
  "elenco": { "ana": { "camisa": "#C8553D", "calca": "#2F3A52", "cabelo": "#1B1412", "pele": "#D8B08C", "estilo": "longo" } },
  "cenas": [ { "cenario": "porta_luz", "duracao": 6, "narracao": "texto falado",
      "textoTela": "03:17", "zoom": [1, 1.1], "pan": [0, -120],
      "personagens": [ { "id": "ana", "pose": "assustado", "x": 0.3, "escala": 1, "flip": false, "y": 0 } ],
      "objetos": [ { "tipo": "celular", "x": 0.7, "y": 0.5, "titulo": "Alerta", "texto": "msg", "entra": 0.8 } ] } ] }
```
- `legenda`: `"palavras"` (padrão, 2-3 palavras por vez no centro, estilo Filme FLIX) ou `"frase"` (frase inteira embaixo).
- `destaque`: palavras que ficam amarelas na legenda. `proxima:false` tira a faixa final.
- Cenários: `quarto_noite`, `corredor`, `casa_fora_noite`, `cozinha`, `porta_luz` (paleta escura, destaque #FF3B1F) e `papel` (fundo bege de infográfico). Ou um `.png` (ver abaixo).
- Poses: `neutro`, `assustado`, `correndo`, `olhando`, `sussurrando`, `chorando`. `x` vai de 0 a 1 (centro dos pés). Sem `elenco`, a roupa/cabelo saem de uma combinação fixa pelo `id` (o mesmo `id` é sempre o mesmo personagem entre cenas). Estilos de cabelo: `curto`, `longo`, `coque`, `careca`.
- Objetos: `celular` (entra de baixo, inclina e vibra), `predio` (`andares`, `destaque` = andar laranja, `x`, `y`), `seta` (`x,y` -> `x2,y2`, `texto`). `entra` = segundos após o início da cena.
- Câmera: `zoom` `[início, fim]` (padrão `[1,1.07]`), `pan` em pixels verticais `[início, fim]`; o zoom sobe sozinho para não aparecer borda.
- Susto: cena com personagem `assustado` treme a câmera no começo.

## Acréscimos do Plantão Noturno (ep01)
- Cenários: `ponto_onibus`, `estrada`, `pousada_fora`, `saguao` (opções na cena: `hora` "HH:MM", `sete:true` pisca a campainha 7), `parede`, `mesa`, `varanda`, `preto`.
- Poses: `cansada`, `hesitante`, `sorrindo` (sorriso largo, olho parado), `entregando` (chave), `segurando` (caderno), `acenando`, `cumprimentando`, `lamentando` (sorri e fecha os olhos após 1,1 s).
- Elenco: `mochila`, `capuz`, `blusa` (cardigã aberto), `listras`, `bigode`, `oculos`, `chinelo`; estilo de cabelo `calvo`.
- Objetos: `cartaz` (`linhas`), `regras` (`itens` + `gatilhos`: cada regra entra quando a legenda chega na palavra), `relogio` (`de`/`ate`/`dura`), `painel` (`acesa`, `pisca`), `interfone`, `balao` (`texto`, rabicho em `px,py`).
- Cena: `desfoque` (px, fundo desfocado nos closes), `escurece`, `legendaY`/`legendaTam`, `textoY`, `textoEntra`, `textoMono`. No episódio: `legendaY`, `legendaTam`, `textoY` padrão e `segue:true` (linha "Segue pra ver a parte N+1" na faixa final).

## Som e ritmo (ep01 final, 25/10)
- **Respiros**: `"respiros": {"lead":0.08,"gap":0.1,"tail":0.15}` no episódio (antes/entre/depois das falas); `"respiro": s` extra no fim de uma cena; `duracao` da cena é só o mínimo (a voz estica). Ritmo do narrador por cena: `"rateNarrador": "+16%"` (lido pelo `gen_voz_serie_edge.py`; o padrão do narrador é +10%).
- **Sussurro**: fala com `"efeito": "sussurro"` passa pelo vocoder de ruído de `voz_fx.js` (18 bandas, sem altura tonal, ar, passa-alta, reverb curto, -6 a -8 dB). Serve para Dalva e outros.
- **Cue-sheet**: `"sons": "ep01_sons.json"` (em `ep/`) toca os sons sintetizados do `sfx.js`. Cue: `{cena, offset, tipo, params}` + `fala` (a partir da fala N), `gatilho` (palavra da legenda), `ateCena` (dura até o fim da cena N), `params.dur: "cena"`; tipos extras do motor: `silencio` (params.dur) e `corte` (silencia trilha e efeitos dali ao fim).
- **Camadas**: `"camadas": {"voz":1,"trilha":1,"efeitos":1,"musicaWav":0}`. trilha = cues musicais (piano, caixinha, drone, pulso...); efeitos = o resto + `efeitos` .wav por cena; `musicaWav` = `stems/music.wav` em loop.
- **Ducking**: com voz ativa, trilha+efeitos descem a `"duck"` (padrão 0,4; ep01 usa 0,3 = -10,5 dB), ataque 60 ms, solta em 350 ms. Limitador: se o pico passar de -1,5 dBFS a mix inteira desce.
- **Medição**: `serie.html?ep=01&mix=1` só monta o áudio e deixa em `window.MIX_INFO` o pico, clipping e, por cena, RMS da voz x RMS da cama sob a voz (margem média e percentil 5 em janelas de 20 ms).
- **Visual**: `escurece` padrão 0,12 (ou `ep.escurece`); varanda aceita `"onibus": {x, y, escala, portaLuz}`.

## PNGs opcionais (se o arquivo não existir, vale o vetor)
- Cenário: `"cenario": "NOME.png"` lê `assets/cenarios/NOME.png`, **1080x1920** px.
- Personagem: com `"arquivo": "NOME"` lê `assets/personagens/NOME_POSE.png` (POSE = nome da pose), PNG com **fundo transparente**, personagem inteiro de pé e de frente/3/4, pés encostados na borda de baixo e centralizado na horizontal; qualquer proporção, vai escalado para altura 760 px (ajuste com `"altura"`). Entrada, saída, balanço e tremor valem igual.

## Pendências conhecidas
- A qualidade da voz atual (ElevenLabs "Bit") não foi ouvida neste teste: nenhum áudio foi gerado.
- Cenários de papel além do fundo liso (cidade, escritório) ainda não existem; PNG ou novo cenário em `CENARIOS`.

## Contos de terror (31/10/2026)
`contos.html` carrega o motor + `contos.js` (cenários novos por peça, poses `curioso` e `cega`, objeto `maos_olhos`) + `sfx_contos.js` (grilos, crepitar, rumor, elevadorZumbido, ding, portaElevador). JSON da peça: `ep/c0N_*.json` (`cartela`, `cor`, `saida`, `arquivo`, `vozes`, `eleven`). Detalhes e armadilhas em `Serie/aprendizados.md` (seção "Contos de terror").

## Atmosfera opcional (`visual`, 07/11/2026)
Camada de pós-render ligada só pela chave `"visual"`. Sem a chave nada muda em nenhum pixel. Fica **abaixo** do texto de tela, das faixas de título/final e da legenda (entra logo depois do `escurece`). Vale no episódio (padrão) e na cena (sobrescreve campo a campo; `"visual": false` na cena desliga tudo nela; `"luz": null` desliga só a luz).
```json
"visual": { "vinheta": 0.6, "grao": 0.4, "neblina": 0.5, "poeira": 0.5,
            "luz": { "tipo": "vela", "x": 0.2, "y": 0.6, "raio": 500, "intensidade": 0.7 } }
```
- `vinheta`, `grao`, `neblina`, `poeira`: intensidade 0 a 1 (0 ou ausente = desligado).
- `grao`: textura de ruído gerada uma vez e reaproveitada, deslocada a cada 2 quadros (determinístico pelo número do quadro).
- `neblina`: 5 faixas lentas na metade de baixo. `poeira`: 70 partículas lentas com semente fixa.
- `luz`: objeto ou lista deles. `tipo` = `vela` (treme), `lanterna` (firme, cai de vez em quando), `lampada` (pisca). `x`,`y` até 2 = fração da tela, acima disso = pixels. `raio` (padrão 500) e `intensidade` (0-1, padrão 0,7).
- Tudo é função do tempo/quadro e de sementes fixas (nada de `Math.random`), então o render sai igual toda vez.
