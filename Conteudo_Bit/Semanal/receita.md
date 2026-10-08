# A receita (o que prende, o que dá alcance) · caderno de experimentos

Objetivo: descobrir, com dados, o formato que mais segura o usuário e mais alcança. Cada post é um experimento: anote a hipótese antes e o resultado depois (24 h e 72 h). Atualize as "Regras da receita" só quando um padrão aparecer em 3+ posts.

## Métricas que importam (nesta ordem)
1. **Retenção / tempo médio assistido** (TikTok Studio: "tempo médio" e "% que viu inteiro"; Instagram: tempo médio de reprodução). É o que destrava o alcance.
2. **Compartilhamentos e salvamentos** (sinal de valor).
3. **Comentários** (sinal de conversa; pergunta no fim ajuda).
4. **Visualizações e % de não seguidores** (alcance).
5. Seguidores ganhos por post.

## Regras da receita (versão 0, 08/10/2026)
- **Visual que a pessoa aprovou ("de genérico para bom", 08/10):** layout montado no código (faixa de baixo com etiqueta + manchete + virada) + cena rica e colorida do tema + **Bit fantasiado do tema** e **objetos de cena desenhados no Gemini no traço do Bit**, recortados e reposicionados. Gemini gerando a cena inteira ficou genérico; cena só em código ficou "sem sal". O meio-termo é o certo.
- História com arco > apresentação ou informação solta (rejeição do Ep. 0 e do "vírgula 27 s"; a pessoa aprovou o arco completo).
- Gancho com mistério nos 2 primeiros segundos; legenda acima de y≈1500.
- Bit como narrador seco, não como protagonista fofo.
- TikTok: várzea + pergunta no fim. Instagram: moderado. LinkedIn: profissional, ângulo novo.
- (a confirmar com dados) fatos rápidos sem voz seguram tanto quanto com voz?
- (a confirmar) myth-busting rende mais visualização completa que fato "olha que curioso".

## Experimentos
| # | Data/hora | Rede | Vídeo | Formato | Hipótese | 24 h | 72 h | Aprendizado |
|---|---|---|---|---|---|---|---|---|
| 1 | 07/10 08:30 | LinkedIn | GMS + MESA-11 (78 s) | texto profissional + vídeo sem voz | ângulo de autocrítica técnica gera alcance fora da rede | 13 h: 346 impr., 60% fora da rede, 4,3% engaj., 26 s de média (de 78) | | autocrítica técnica funciona no LinkedIn; metade do vídeo não é vista |
| 2 | 07/10 19:00 | Instagram | GMS 30 s | texto na tela, sem voz | — | 3 h: 0 visualizações (conta nova, 0 seguidores) | | conta nova precisa de empurrão (compartilhar no perfil pessoal) |
| 3 | 07/10 19:00 | TikTok | GMS 30 s | texto na tela, sem voz | — | 3 h: 40 vis., 2 curtidas; 4 h: 53 vis. | | conta com histórico de outro nicho; acompanhar |
| 4 | 08/10 11:00 | TikTok (+IG 12h) | Wi-Fi não significa nada (25 s) | myth-busting, sem voz | myth-busting segura mais que fato comum | | | |
| 5 | 08/10 15:00 | TikTok | IA nos games (19 s) | número + contradição + pergunta, sem voz | pergunta final gera mais comentários | | | |
| 6 | 08/10 19:00 | Instagram + TikTok | A vírgula das 5 da manhã (62 s) | história com arco, narrada | arco narrado tem a maior retenção da semana | | | |
| 6b | 08/10 16:00 | Instagram | Bit News: satélite de IA do Google (imagem única) | imagem-manchete + legenda longa com dica | formato estático 'manchete' rende salvamentos/alcance perto de Reel (benchmark @elidicastech 80K) | | | |
| 7 | 10/10 11:00 | Instagram | Carrossel Mario 40 KB (7 itens) | carrossel história | carrossel com gancho meta ("menos que esta imagem") gera salvamentos | | | |

## Benchmarks (amostra de ~20 vídeos do mesmo tema antes de postar)
### Wi-Fi não significa nada · 08/10/2026 · 24 vídeos (12 PT, 12 EN) no TikTok
| Faixa | Quem | Curtidas | Como tratou |
|---|---|---|---|
| Topo | Stupid Little Genius (EN) | 18K (1.849 salvos, 854 compart.) | rosto + atuação exagerada, placa escrita na mão, 135 s, conta o PORQUÊ (o nome técnico IEEE 802.11b assustava o cliente) |
| Topo | Vin Explains (EN) | 10,2K (1.491 salvos) | rosto, "professor" em sala de aula (fundo de lousa), 38 s, gancho "people think…" |
| Meio | Eric Guidry, Doxael, Andrew Grant (EN) | 925–1.358 | rosto falando para a câmera, 36 s, tom "odeio te dizer" |
| Base | maioria dos vídeos em PT (Tech Oculto, Universo Tech, Fatos Surpreendentes, TechLab…) | 1–103 | sem rosto e sem voz: texto genérico "você sabia?", sem história, sem o porquê |
**O que roubar (e fazer melhor) dos que deram certo:**
| Elemento | Quem fez | Como o Bit faz melhor |
|---|---|---|
| Gancho falado "people think…" / "hate to break it to ya…" | Vin Explains, Eric Guidry | "Odeio te contar isso, mas…" / "Todo mundo acha que…" na voz do Bit, já no 1º segundo |
| Expressão desconfiada (olho semicerrado + dedo levantado "bom…") antes da revelação | Stupid Little Genius | pose `bit_desconfiado` (Gemini) na hora da virada |
| Placa escrita à mão como objeto de cena ("WiFi means nothing?") | Stupid Little Genius | o Bit segurando uma plaquinha de papel com a frase-chave (pose `bit_placa`, texto desenhado no código) |
| "Professor" com lousa: autoridade leve | Vin Explains | cenário de lousa/terminal no fundo, o Bit apontando |
| Legenda = a pergunta simples ("What does WiFi stand for?") | Vin Explains (1.491 salvos) | 1ª linha da legenda sempre a pergunta que a pessoa digitaria na busca |
| O porquê + bastidor (802.11b assustava cliente) | Stupid Little Genius (854 compart.) | sempre explicar o porquê com um detalhe de bastidor |
| Hashtags enxutas do nicho: #TechTok #WiFi #NowYouKnow | Eric Guidry | #techtok + tema + #curiosidades (3–5, nada de #fyp) |

**Leitura:** o tema funciona (até 18K), mas quem ganha tem (1) uma PESSOA/personagem com voz e expressão, (2) o porquê por trás (802.11b feio → marketing), (3) duração maior (36–135 s) com tensão, (4) humor de reação. Os vídeos mudos em PT, só com texto, quase não saem do zero. **Risco do nosso vídeo B (mudo, 25 s): cair na faixa de baixo.** Ajuste: narração do Bit + o porquê do 802.11b + o Bit reagindo em cena.

### Curiosidades tech no INSTAGRAM · 08/10/2026 · 26 posts de #curiosidadestech (Reels, imagem e carrossel)
| Faixa | Quem | Curtidas | Formato e tratamento |
|---|---|---|---|
| Topo | @securiters | 262K, 5,2K coment. | Reel com rosto pensativo + título proibido/secreto ("Cómo entrar a la D3EP WEB", palavra censurada pra passar no filtro) |
| Topo | @elidicastech | 80K, 3,8K coment. | **imagem única estilo manchete de notícia**: foto forte + etiqueta amarela ("Saúde") + frase entre aspas em vermelho ("Sentir raiva" ao ouvir alguém mastigando…); a LEGENDA LONGA explica e dá dica (vira salvamento) |
| Meio | @abelezadosdados | 7,5K | Reel: pessoa + tela dividida contando história com ano e personagem ("Em 1961, um professor de matemática entrou num cassino…") |
| Meio | @ohomem.resolve, @davision.eth, @coisa_de_dev | 0,8–2,4K | utilidade ("funções escondidas do celular"), ironia visual (braço robótico clicando no "não sou um robô"), segredo de big tech (bunker da OpenAI) |
| Base | franquias (@supergeeks…: 0–2), "Descubra os segredos…", "5 curiosidades sobre a Apple" | 0–23 | texto institucional igual em vários perfis, lista genérica, sem gancho emocional |
**O que muda do TikTok para o Instagram:** no Instagram **imagem única ou carrossel estilo manchete** compete com Reel (80K num post estático!); a **legenda longa** com explicação + dica pesa mais (salvamento); ganchos de **segredo/proibido** e **emoção do dia a dia** ("você sente raiva…") puxam muito; história com ano + personagem funciona nas duas.
**O que roubar:** cartão-manchete (foto/arte forte + etiqueta de categoria + frase entre aspas com a palavra-chave em vermelho) → formato "Bit News"; legenda longa no Instagram com 1 dica prática no fim; títulos de segredo ("o que a fábrica não te conta", "o botão que ninguém usa").

### Espaço/astronomia no INSTAGRAM · 08/10/2026 (#espaco, #astronomia) · para o Bit News do satélite
Topo: "A NASA LIBEROU PESSOAL!!" (63K), "SE ANDRÔMEDA É VISÍVEL, POR QUE NÃO CONSEGUIMOS VÊ-LA A OLHO NU? 👀", "É ASSIM QUE UM BURACO NEGRO…". **Padrão:** 1ª linha curta, em CAIXA ALTA, com novidade/exclusividade ou contradição; explicação depois. Aplicado na legenda: "O GOOGLE MANDOU UMA IA PRO ESPAÇO. E ELA PASSA CALOR."
**Erro corrigido:** a 1ª legenda foi escrita só com base nas hashtags gerais e abria com "Você sabia que…" (padrão da base). A amostra tem que ser do TEMA específico em cada plataforma.

## Regra de benchmark (pedido em 08/10/2026)
- **20 amostras POR PLATAFORMA onde o post vai sair** (TikTok, Instagram e LinkedIn), porque o que funciona numa não funciona na outra. No Instagram, a busca por palavra não funciona na web: use as páginas de hashtag (instagram.com/explore/tags/<tag>/) e leia curtidas/comentários pelo og:description de cada post.
- Inclua **carrosséis e imagens**, não só vídeos: carrossel informativo ou engraçado também viraliza.

## Como atualizar (rotina diária e conversas de análise)
- Antes de produzir cada tema: busque o tema no TikTok (PT e EN), anote ~20 vídeos (curtidas, salvos, duração, rosto/voz/texto, gancho, se conta o porquê) numa tabela de benchmark aqui, e decida o que o nosso precisa ter para ficar no topo. Depois de 24/72 h, compare o nosso com a amostra.
- Todo dia, antes de produzir: puxe as métricas dos posts de 24 h e 72 h atrás (TikTok Studio → Publicações/Análise; Meta Business Suite → Conteúdo/Insights; LinkedIn → Ver análise), preencha a tabela e escreva 1 linha de aprendizado.
- Uma vez por semana (sábado): releia a tabela, promova padrões confirmados a "Regras da receita" e ajuste o plano da semana.
