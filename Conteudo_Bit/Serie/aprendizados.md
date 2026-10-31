# Aprendizados da série Plantão Noturno (para a próxima história)

Pedidos do William em 25/10/2026 e problemas que apareceram. Ler antes de planejar a próxima série.

1. **Roteiro e clímax melhores.** A primeira série foi aceita "como é", mas a próxima precisa de roteiro com mais detalhes e clímax mais fortes em cada episódio. Propor o arco e o clímax de cada ep. para aprovação antes de produzir.
2. **Capas prontas, chamativas e virais.** O William pediu capas chamativas e com cara de viral: rosto ou objeto grande, título curto de impacto, contraste forte, pergunta ou ameaça visível; nunca um quadro qualquer do vídeo. Preparar uma capa (miniatura 1080x1920, com título curto) para cada episódio ANTES de agendar, e subir já com ela. No TikTok Studio, post agendado não pode ser editado; a capa tem de entrar no momento do upload. No Meta Business Suite a miniatura se escolhe em "More edit options".
3. **Personagem andando.** O motor não anda personagem: a Bia "voava" na escada (Ep. 6, corrigido com a opção `sobe`). O Ep. 3 tem o mesmo defeito (Bia e hóspedes flutuam na escada) e não foi corrigido. Usar `sobe` ou keyframes de posição antes de gravar cenas de movimento.
4. **Voz.** Evitar contrações na fala dos personagens ("tô", "tava", "pro"): o edge-tts embola, principalmente a Dalva lenta (Ep. 4, "Tô encharcada"). Escrever "estou", "estava", "para o".
5. **Elenco nos cenários especiais.** Cenários com câmera própria (olho_magico, espelho, punho) precisam receber o elenco do episódio; sem isso o personagem sai com o visual padrão (Dalva careca no Ep. 4).
6. **Ritmo.** Cenas com mais de ~1,5 s de silêncio depois da fala parecem lentas (Ep. 5). Deixar ar só onde for silêncio dramático deliberado.
7. **Duração.** Manter 62 a 78 s por episódio (monetização exige 60 s ou mais).
8. **Quem posta.** O William sobe e agenda no TikTok. Nenhum agente publica; só preenche legenda e miniatura no Meta Business Suite quando ele pede.

## Arquivo de semanas antigas
- As semanas 05, 12 e 19 de outubro de 2026 do canal Bit foram arquivadas em 25/10/2026 no Release `arquivo-bit-2026-10` do repositório (github.com/WilliamNRAmorim/Projetos/releases/tag/arquivo-bit-2026-10), como zips conferidos por hash, e apagadas do PC.
- Para recuperar: `gh release download arquivo-bit-2026-10 --dir <pasta>` e extrair em `Conteudo_Bit\Semanal`.
- Regra do William: o que já foi publicado e não será usado vai para um Release do GitHub e sai do PC; só volta para o PC o que for usar. A pasta `Semanal\serie` (Eps. 1 a 7) pode ser arquivada assim depois de 31/10.

## Publicação multiplataforma (25/10/2026)
- **TikTok:** o William agendou os 7 episódios (25 a 31/10, 18h). Post agendado não pode ser editado; capa só no upload.
- **YouTube Shorts:** os 7 foram programados no canal William Amorim (UCTWAo94qLHpdaXU6blEh2pA), 25 a 31/10 às 18h, fuso GMT-3, título com `#Shorts`, "não é conteúdo para crianças", playlist PLANTÃO NOTURNO. No YouTube Studio o upload de arquivo é rápido; o William seleciona os arquivos e o agente preenche título, descrição, playlist e programação. Textos prontos em `Serie\epNN.md` (TikTok) e no histórico desta sessão (YouTube).
- **Instagram (Meta Business Suite):** o upload ficou em 0% duas vezes (envio em lote e "Create reel"). Não foi publicado. Para a próxima série, subir pelo app do celular ou testar outra rede. A conta aberta era uiu.engenharia (canal de engenharia), não a da série.
- **Limite de ferramenta:** a ferramenta de upload do navegador aceita no máximo 10 MB por chamada; os vídeos têm 27 a 31 MB. O William seleciona o arquivo na janela do Windows. Para a próxima série, considerar renderizar uma versão leve (menos de 10 MB) só para upload automatizado, se a qualidade permitir.
- **Monetização (confirmada no TikTok Studio e na Academia de Criadores):** Programa de Recompensas do Criador pede conta pessoal, 18 anos ou mais, 10 mil seguidores e 100 mil visualizações em 30 dias, vídeo de mais de 1 minuto, original e com pelo menos 1.080p. Conteúdo "perturbador" pode ser inelegível. Notificação de elegibilidade ligada para todos os programas.
- **YouTube Shorts:** monetização exige 1.000 inscritos e 10 milhões de visualizações de Shorts em 90 dias (fontes de terceiros); nível de fãs com 500 inscritos e 3 milhões.

## Contos de terror, Dia 1 (31/10/2026): o que aprendemos produzindo 4 Shorts
Processo e arquivos em `Producao\serie`: `contos.html` (abre o motor com `contos.js` e `sfx_contos.js`), JSON `ep\c01..c04_*.json` + `c0N_sons.json` (ids `c01` a `c04` em `ep\indice.json`), vozes por `gen_voz_contos.py <id>` (edge-tts, perfis em `"vozes"` do JSON) e `gen_voz_eleven.py <id>` (ElevenLabs v3, bloco `"eleven"` do JSON). Render: `node driver.js render "http://127.0.0.1:5178/Producao/serie/contos.html?ep=c01&render=1"` (Edge headless por CDP, perfil temporário apagado no fim). Mix e medição sem render: `&mix=1` (`node driver.js info ...`). Folha de contato e medição do MP4 FINAL: `node driver.js shot ".../contato.html?f=contos-dia1/ARQ.mp4&n=12" saida.png --h=1100 --lim=400` (leva 2 a 4 min por seek de vídeo).
1. **Saída em pasta própria:** `"saida"` e `"arquivo"` no JSON do episódio (o servidor não aceita subpasta aninhada; os MP4 do Dia 1 ficam em `Semanal\contos-dia1`).
2. **Cartela de título** opcional: `"cartela": {"titulo","sub"}` + `"cor"` (acento da peça, também nas linhas de corte). Sem isso o motor mostra "EPISÓDIO N" como antes. `"proxima": false` tira a faixa final.
3. **Cor e cenário por peça:** cada conto tem seus cenários novos em `contos.js` (bordô/rio e gabinete e velório; azul-noite/pasto e roça; verde-musgo/quarto e cozinha; âmbar/prédio, elevador, corredor, portaria, painel). Cenário só existe se o JSON o pedir; os eps antigos ficam idênticos (conferi ep01 e ep06 byte a byte nos quadros).
4. **Roteiro curto pede batidas:** com 85 a 115 palavras a peça só passa de 45 s com ritmo lento (edge `-6%` a `-16%`), pausas deliberadas (`respiro`), cena de abertura só com a cartela (sussurro) e retenção final. Sem isso o Elevador ficou em 40 s.
5. **Sussurro (ElevenLabs v3):** `[whispers]` funciona na API com `eleven_v3`; o plano Starter não dá `pcm_44100`, então usei `pcm_24000` e o script recorta o silêncio das pontas e normaliza o pico (sussurro 0,5; chamada normal 0,85). A "segunda chamada" é o MESMO arquivo da primeira (mesma voz e tom). O motor não recorta arquivo de voz próprio; por isso o recorte é feito antes.
6. **Calibração dos sons novos:** `crepitar` e `rumor` com volume acima de ~0,3 ficam mais altos que a voz (margem negativa e o limitador abaixa a mix inteira). Alvo: margem P5 da voz >= 6 dB em `porCena` do `&mix=1`. `grilos` precisa de volume 3 a 4 para aparecer (soa fino).
7. **Personagem some no fim da cena** (fade de saída) se não tiver `"fica": true`; no close da fala final do porteiro isso apareceu como "fantasma". Usar `fica` em fala que termina a cena.
8. **Câmera dentro de cenário:** a cobra de fogo (`boitata`) mapeia a profundidade em `yA..yB`; na janela do quarto use uma faixa pequena (a janela não vai até o chão do pasto).
9. **Sem ferramenta de áudio:** não há ffmpeg nesta máquina; a conferência do áudio do MP4 final decodifica o arquivo pelo próprio Edge (pico, clipping, RMS e maior silêncio). O agente não ouve: pronúncia, sotaque e "peso" do sussurro só o ouvido do William valida.
