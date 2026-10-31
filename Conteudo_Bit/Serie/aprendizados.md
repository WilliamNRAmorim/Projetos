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

## Contos de terror, Dia 2 (31/10/2026)
1. Cenários novos em `contos2.js` (carregado por `contos.html`): quarto/olho/assoalho/sala (ocre), banheiro escolar e espelho com cabines refletidas (rosa), rua, carro de lado e janela de carro com o objeto `porta_carro` por cima do motorista (roxo), corredor/banheiro/espelho/porta (branco-ciano). Reflexo no espelho é desenhado à mão no cenário (`refCostas`, `portaRefAberta`).
2. Para esconder as pernas de quem está "dentro" de um carro, um OBJETO desenhado depois dos personagens (a porta) cobre o corpo; personagens sempre são desenhados antes dos objetos.
3. `gen_voz_contos.py` aceita `pitchNarrador` por cena (voz que muda de tom ao longo da peça: Loira vai de brincalhona a grave). O batimento acelerando (`batimento` bpm 70, 100, 130, 150) é o que sustenta a tensão do Coração Delator; volume do último acima de ~0,7 passa a voz.
4. `sfx_contos.js` ganhou `pinga` e `rangido`; o gancho `SfxExtra` entrega `rng`, que precisa ser extraído em cada def (faltou uma vez e o mix falhou com "rng is not defined", sem aviso na tela: conferir `MIX_INFO` e a última linha do log do `driver.js`).
5. Coração Delator: enredo conferido no original (poemuseum.org): 7 noites, oitava noite o velho acorda, 3 policiais, cadeira sobre as tábuas, "relógio embrulhado em algodão". O roteiro de memória foi ajustado (sem esquartejar, sem mostrar corpo; final "Tirem as tábuas! Aqui, aqui! É o coração dele!").

## Contos de terror, Dia 3 (31/10/2026)
1. **O Enfermeiro: o roteiro de memória estava errado** (conferido na Wikisource): não há espelho nem fantasma do velho. Procópio (enfermeiro em 1859, coronel Felisberto, 24/8/1860) leva uma moringa no rosto, estrangula o coronel, esconde as marcas, herda tudo, doa uma parte, ergue túmulo, sente remorso e se consola; fecha com a "emenda" ao Sermão da Montanha ("Bem-aventurados os que possuem..."). Roteiro refeito (7 cenas); a luta é só sombra na parede.
2. **Duração com voz ElevenLabs lenta (Bill):** a primeira versão passou de 77 s; precisou cortar frases (a duração vem do áudio, não da cena). Medir `&mix=1` antes de renderizar e podar o roteiro, nunca acelerar a voz.
3. Cenários novos em `contos3.js` (sépia, floresta, estrada na chuva, quarto de lua). Pegadas precisam de contraste (cor clara no chão de mata, chão claro no close).
4. `assobio` e `limpador` em `sfx_contos.js`. Assobio e grilos sobem a cama facilmente: manter assobio <= 0,45 e grilos <= 2,2 para a voz ficar >= 6 dB.
5. **Arquivo travado:** se o MP4 já foi enviado/aberto pelo app, o servidor não consegue sobrescrever e o render "termina" sem gravar. Sempre conferir a data do arquivo e, na dúvida, mudar o nome (`v2`).

## Contos de terror, Dia 4 (31/10/2026)
1. **O Gato Preto conferido no original** (poemuseum.org): Plutão (olho arrancado e enforcado, só sugerido), incêndio, gato de mancha em forca, machado no porão (a esposa segura o braço), emparedada, polícia no 4º dia, bengala na parede, uivo; o cadáver aparece com o gato sobre a cabeça. Na versão em vídeo nada disso é mostrado: só sombra do braço, silhueta, parede e olhos do gato. A frase da animação "fez mal a Plutão" é eufemismo deliberado (regra: sem animal ferido).
2. Cenários em `contos4.js` e sons `gongo`, `uivoGato`, `galope`, `relincho`, `raspar`, `respirar` em `sfx_contos.js`. Sons de impacto (uivo, gongo, relincho) precisam de volume ~0,2 a 0,4 para não passar a voz (margem P5 >= 6 dB); a medição de cada cena em `&mix=1` mostra na hora.
3. Duração: com voz ElevenLabs Daniel + 8 cenas a peça do Gato Preto chegou a 68 s (limite 70): olhar a soma das falas antes de adicionar pausas.
4. Sombra de objeto/animal como "personagem" (mula, gato) fica mais legível com escala grande; a mula de fogo precisou de escala 1,8 a 2 para ser lida de relance.

## Contos de terror, Dia 5 (31/10/2026)
1. **O Retrato Oval conferido no original** (poemuseum.org): narrador ferido e delirante, o criado Pedro arromba o castelo nos Apeninos, quarto de torre com quadros, livrinho no travesseiro, retrato oval da jovem, pintor obcecado que "não queria ver", a esposa posa semanas na torre escura, fim "Ela estava morta!". O roteiro de memória estava certo no essencial.
2. Cenários novos em `contos5.js`; objeto `camera_rec` (modo de composição `saturation` + multiply) transforma qualquer cena em imagem de câmera de segurança em preto e branco com data/hora e REC, desenhado por cima dos personagens.
3. **Roteiro curto de "urgente" precisa de batidas visuais:** o Ônibus noturno saiu com 36 s mesmo com voz rápida; foi para 48 s com ritmo +14%, cenas mais longas e um respiro final de 2,5 s. Regra prática: 85 palavras = ~36 s a +24%.
4. Sons novos: `uivoLobo` e `corrente` (corrente tensa mais rápida). Toque de celular a vol 0,7 passa a voz; usar ~0,3.
5. Personagem "sentada" sem cadeira flutua; o cenário da torre do pintor desenha o banquinho na posição certa (x 0,25, escala 0,85).

## Contos de terror, Dia 6 (31/10/2026)
1. **O Barril de Amontillado conferido no original** (poemuseum.org): Fortunato fantasiado de bobo (vestido listrado e chapéu com guizos), Montresor de máscara preta e roquelaire; a isca é o Amontillado e a vaidade contra Luchesi; nitro e tosse nas catacumbas; Fortunato preso a um nicho de granito por corrente e cadeado, emparedado; ri, depois pede "pelo amor de Deus"; só os guizos respondem; "In pace requiescat!" e meio século depois ninguém mexeu nos ossos. A morte nunca aparece: só a parede subindo (objeto `tijolos_nicho` por cima do personagem) e o som dos guizos.
2. O objeto `gorro_guizos` põe o gorro sobre a cabeça de qualquer personagem (calcula pela altura da cabeça); `tijolos_nicho` cresce a parede por cima do personagem (objetos são desenhados depois dos personagens).
3. Sons novos: `guizos`, `rugido`, `remo`, `chiado`. Rugido e chiado precisam de volume ~0,12 a 0,2 para não passar a voz.
4. Voz da mãe da Babá eletrônica escala o ritmo e o tom por cena (`rateNarrador` e `pitchNarrador` crescentes) para simular o pânico; a voz da babá é um sussurro ElevenLabs separado.

## Contos de terror, Dia 7 (31/10/2026) e fechamento da semana
1. **A Máscara da Morte Rubra conferida no original** (poemuseum.org): príncipe Próspero e mil amigos na abadia fortificada com portões de ferro soldados (não "chaves jogadas fora"), sete salões (azul, roxo, verde, laranja, branco, violeta e preto com vitrais vermelhos), relógio de ébano que para a música a cada hora, figura em mortalha com máscara de cadáver, perseguição até o salão preto, mortalha vazia, todos morrem, relógio para, braseiros se apagam. Mostrado só em silhueta e cor; as "manchas" são carmesim estilizado.
2. Objetos novos: `morte_mascara` e `mortalha_vazia`; cenário `salao_cores` recebe a cor do salão e a do próximo (perspectiva em enfilada). Sons: `badalada` e `arrastar`.
3. **Falha do edge-tts (áudio de 2 KB):** aconteceu de novo (Dia 2 Loira, Dia 7 Vizinho) com combinações de `rate` e `pitch` negativos. Depois de gerar as vozes, rodar `find ../stems/serie/epcXX -name "*.mp3" -size -6k` e regerar o que aparecer com `rate`/`pitch` ligeiramente diferentes. Já virou parte do roteiro de produção.
4. **Semana completa (Dias 1 a 7):** 28 Shorts, cada um com cor dominante e cenário próprio, 45 a 70 s, 1080x1920, sem clipping. Os 4 Shorts de cada dia ficam em `Semanal\contos-dia1` a `contos-dia7` (fora do git). Pendência do plano: o vídeo longo do Dia 8 depende da retenção medida depois de publicar.

## Dia 8: vídeo longo (16:9)
- `serie/longo.html` junta os 10 MP4 já prontos (decodifica áudio e quadros, sem reprocessar cena), 1920x1080, 553 s (9:13), intro de 10,7 s (voz Antonio + zumbido), fundo = quadro borrado, fade de 0,45 s e batida grave entre contos, corte do silêncio final deixando 0,9 s, barra de progresso e etiqueta "CONTO n DE 10". Ganho por conto para pico -4 dBFS (limite 2x).
- Seleção feita por critério editorial (mistura literário/folclore/original, durações), NÃO por retenção: ainda não havia dados. Trocar a lista em `LISTA` e rodar de novo se o William quiser os 10 de maior retenção.
- Render: `node driver.js render "http://127.0.0.1:5178/Producao/serie/longo.html?render=1" --w=1920 --h=1080 --lim=1500` (~12 min); saída `Semanal/contos-dia8/` (405 MB, fora do git).

## Agendamento em lote (Dias 1 a 8) e plano "shadow" (31/10/2026)

### O que deu certo
- Um único conjunto de 8 abas (4 YouTube Studio + 4 TikTok Studio), cada uma com 1 vídeo do dia, preenchidas em lote (`browser_batch`). O texto vem de `contos-de-terror-semana/publicacao-28-pecas.md`.
- Conferência final pela lista (YouTube: Conteúdo > Shorts; TikTok: Publicações), não pela tela de cada aba.
- Resultado: 28 Shorts + 1 longo programados no YouTube, 28 no TikTok.

### O que errei (e o custo de cada erro)
1. **Cliques por coordenada sem olhar a tela.** O layout muda entre abas (barra de progresso, aba rolada, altura). Vários cliques caíram no calendário em vez de "Agendar", ou no campo errado. Custo: refazer e conferir.
2. **Data/hora do TikTok e do YouTube.** Digitar a hora só pega depois de clicar no campo e esperar 1 s; o seletor do TikTok vem em 19:xx e é preciso escolher minuto 00 e depois a hora. Calendário do YouTube pode pular para 2027 se clicar rápido. Sempre conferir com zoom na região da data/hora antes de agendar.
3. **Abas congelam** quando 4 vídeos processam ao mesmo tempo (screenshot com timeout). Não clicar de novo: esperar, ou reabrir.
4. **Alterações não salvas** no YouTube bloqueiam a navegação ("Leave site?"). Nunca forçar; verificar se o vídeo ficou programado antes de reusar a aba.
5. **Ordem dos arquivos nas abas** nem sempre bate com a ordem combinada (Dia 7 veio Máscara, Homem do Saco, Vizinho, Iara). Identificar pelo nome do arquivo na aba, nunca pela posição.
6. **Capa do TikTok** só deixa escolher quadro do vídeo, e a legenda queimada fica cortada ("CHEGOU, POR"). O YouTube só oferece 3 quadros. Escolhi capa de cabeça em vários; não houve critério.
7. **Hashtag**: o YouTube trocou `#Shorts` por `#shortsyoutube`/`#shortsbeta` em alguns. Sem impacto.
8. **Rascunho duplicado** ("05 o coracao delator") ficou no YouTube por envio repetido. Apagar.
9. Informei "feito" duas vezes sem ter lido a confirmação de todas as abas (Dia 6 no YouTube). Só dizer "programado" depois de ver a confirmação ou a lista.

### Como reduzir custo e aprovação (modo shadow: 1 "sim" por lote, não por vídeo)
**Regra de aprovação proposta (precisa do "sim" do William uma única vez, vale para a série inteira):**
- William aprova **o lote do dia ou da semana inteiro** em um resumo único (título, descrição, data, hora, capa por peça). Depois disso, o chefe agenda sem perguntar de novo, desde que o texto seja idêntico ao aprovado.
- Continua exigindo "sim" novo: mudar texto, data ou hora; publicar na hora (não agendar); apagar; qualquer conta/plataforma nova.
- Quem agenda é só o chefe, nunca subagente (regra do CLAUDE.md não muda).

**Para gastar menos:**
1. **Gerar um `lote.json`** por semana (peça, título, legenda YouTube, legenda TikTok, data, hora, arquivo) a partir de `publicacao-28-pecas.md`. Uma única aprovação cobre tudo.
2. **Uma tabela fixa de coordenadas por tela** (YouTube Studio e TikTok Studio) para digitar sem screenshot a cada passo; screenshot só na conferência final por zoom. Metade dos tokens foi screenshot.
3. **Nome do arquivo = ordem**: subir os vídeos na ordem do `lote.json` e conferir pelo nome do arquivo antes de preencher.
4. **Escolher capa por regra**, não por olho: pegar o quadro de 3 s (gancho) ou o 2º quadro sugerido, igual para todos. Salvar a regra e parar de decidir um a um.
5. **Conferir pela lista**, uma vez no fim (YouTube Shorts + TikTok Publicações), em vez de abrir peça por peça.
6. **Produção**: o motor já é barato (voz edge-tts, render local). Gasto alto foi revisão visual de cada quadro. Rever só a folha de contato e só as cenas que mudaram; reaproveitar cenários e poses.
7. **Longo "10 melhores"**: montar uma vez por semana com `serie/longo.html` (só reusa os MP4 prontos, sem reprocessar).
8. **Medir retenção antes de repetir** (regra do plano): olhar visualizações por tipo (literário × folclore × original) no Dia 3 e no Dia 7 e cortar o que não rende.

### Pendências da semana
- Trocar a lista do longo pelos 10 de maior retenção quando houver dados.
- Apagar o rascunho "05 o coracao delator" no YouTube.
- Conferir o longo programado (8/11, 18h) em Conteúdo > Vídeos.

## Perfil do canal YouTube e fechamento da sessão (31/10/2026)

### Feito
- Canal `@Uiloumusk`, nome "William Amorim" (nome da futura placa). Handle mantido por decisão do William.
- Descrição do canal, link do TikTok (`https://www.tiktok.com/@uiloumusk`), e-mail de contato williamamorim089@gmail.com (público), foto de perfil, banner e marca d'água (círculo 150x150, exibida só no final do vídeo).
- Arquivos em `Conteudo_Bit/Serie/canal/`: `banner.jpeg`, `perfil.jpeg`, `marca_dagua.png`.
- Imagens geradas no Gemini (login do William no Chrome). Personagem ORIGINAL (aventureiro encapuzado com vela de chama azul) com fundo de itens genéricos de fantasia (dado d20, mapa, espada de energia, cajado, anel, poções, blocos de pixel, teia). Gostos dele: RPG de mesa, fantasia, Hora de Aventura, Apenas um Show, jogos e super-heróis. Nenhuma marca ou personagem de terceiros.

### Lições do perfil
1. Pedido ao Gemini com lista de marcas gera imagem em branco (filtro). Prompt curto e sem nomes de franquias funciona. Imagem leva ~20 s; esperar antes de concluir que falhou.
2. Download do Gemini cai em Downloads, que a sessão não lê. Copiar para a pasta do projeto antes do `file_upload`.
3. `file_upload` exige o `ref` do input (achar com `find`), não clicar no botão "Enviar".
4. YouTube mostra "alterações não salvas" enquanto o upload termina; esperar "Mudanças publicadas".
5. Foto de perfil: quadrado, rosto central, legível pequeno. Banner: texto e personagem no miolo; bordas são cortadas.
6. Faltam: trocar foto do TikTok pela mesma; Instagram; trocar marca d'água por versão mais discreta se ficar chamativa; abrir `youtube.com/@Uiloumusk` no celular para checar o recorte.

### Estado ao fechar a sessão
- 28 Shorts + longo programados no YouTube; 28 Shorts agendados no TikTok.
- Pendente: apagar rascunho duplicado "05 o coracao delator" (YouTube); conferir o longo em Conteúdo > Vídeos (8/11, 18h); decidir mudança do CLAUDE.md para aprovação por lote (proposta na seção anterior).
