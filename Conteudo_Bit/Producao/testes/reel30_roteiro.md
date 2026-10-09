# Reel 30 s com o Bit: "Meu sistema não cobre tudo" (GMS x MESA-11)

Destino: Instagram (@uiu.engenharia) e TikTok (@uiloumusk). LinkedIn não recebe este corte (tem o Bit). Rascunho para aprovação; nada publicado, nada renderizado, nenhum áudio gerado.

## Por que este tema
- Ainda não virou reel: o MESA-11 só existiu como post de LinkedIn com o vídeo longo (`Videos/Publicar/posts_prontos.md`, seção LinkedIn). O reel de 30 s do GMS é sobre outro assunto (ninguém sabia o que acontecia na produção; mesmo arquivo, seção Instagram). Will Station já tem carrossel e roteiro de TikTok; vírgula das 5h e Wi-Fi estão em `Semanal/temas_usados.md`.
- Tem arco natural (promessa de lacuna, contagem, sentido) e todos os fatos estão num único arquivo.
- Seguro: só dado do TCC, sem Kaizen, sem empresa, sem nome de pessoa.

## Fatos usados (todos de `Conteudo_Bit/Videos/Publicar/posts_prontos.md`, texto do LinkedIn)
| Fato | Onde |
|---|---|
| GMS avaliado contra o MESA-11, "modelo de referência para sistemas de execução da manufatura" | LinkedIn, parágrafo 1 |
| Ele não cobre tudo | LinkedIn, linha 3 |
| 11 funções: 6 implementadas, 1 em expansão, 2 parciais, 2 fora do escopo (6+1+2+2 = 11) | LinkedIn, lista |
| A análise está no TCC em Engenharia de Computação | LinkedIn, parágrafo 3 |
| 100% low-code: Power Apps, Microsoft Lists, Power Automate e Power BI, porque a governança de TI permitia | LinkedIn, parágrafo 4 |
| "Saber o que deixar de fora também foi engenharia" | LinkedIn, parágrafo 4 |
| Regra do GMS contado pelo TCC | `Conteudo_Bit/LEIA-ME.md`, regras de conteúdo |

Não uso "9 meses", "1 a 2 dias" nem a frase "Não criamos o dado": ficam para outro corte. Nada de número fora da tabela.

## Direção (playbook, seção 3)
- 1080x1920, 30 fps, 120 BPM: 1 batida = 0,5 s, 1 compasso = 2 s, 15 compassos (C1 = 0-2 s ... C15 = 28-30 s).
- Fundo ink #0C0C0D, texto paper, secundário mute #8C8B86, destaque #FF3B1F (no máximo 1 por quadro), Geist 800/900 (tracking -0,03 em) para display, Geist Mono 500 para rótulos, cantos retos, grão 0,07 com semente fixa. Sem glitch ciano.
- Objeto-guia (nunca sai da tela): grade de 11 quadrados retos (3 + 4 + 4), 140 px por lado, folga 24 px, centrada em x 540, faixa y 760-1100. Cada quadrado é uma função do MESA-11. Os estados mudam por mola, sem corte:
  - vazio: só contorno mute 3 px
  - implementada: preenchido paper
  - em expansão: preenchido paper com um segundo contorno 12 px por fora
  - parcial: metade de baixo preenchida
  - fora do escopo: contorno #FF3B1F
- Bit: pequeno (cerca de 220 px de altura), `bit_rig.js`, sem boca tremendo, sempre fora do objeto-guia. Posição de repouso x 760-940, y 1200-1420 (dentro da área segura). Só reage (olho semicerrado, cabeça inclina, aponta); não narra.
- Texto de tela: sem ponto final, dentro de x 90-940 e y 250-1480. Legendas do Bit em balão reto, baseline ~1470.

## Timeline (texto exato, na ordem)
| Tempo | Compasso | Cena | Texto de tela (exato) | Bit |
|---|---|---|---|---|
| 0,0-1,5 | C1 | Gancho. Grade de 11 quadrados vazios. Texto entra por máscara em 0,0-0,5 s e fica | MEU SISTEMA NÃO COBRE TUDO (a palavra TUDO em #FF3B1F) | Em repouso, olho aberto, olhando a grade |
| 1,5-2,0 | C1 | Texto sai por máscara para cima, antes de o novo entrar | | |
| 2,0-4,0 | C2 | Problema: os 11 quadrados contornados entram em cascata (0,1 s entre cada, 2,0-3,1 s) | rótulo mono: AVALIEI O GMS CONTRA O MESA-11 | Inclina a cabeça para a grade |
| 4,0-6,0 | C3 | Virada: a câmera dá punch-in 1,00 para 1,06 e um marcador vermelho (quadrado de 140 px) desliza sobre o 1º quadrado | rótulo mono: 11 FUNÇÕES / texto grande: O MODELO DE REFERÊNCIA DA MANUFATURA | Aponta |
| 6,0-9,0 | C4-C5 (1ª metade) | Passo 1: os 6 primeiros quadrados enchem de paper, um por batida e meia, descendo da linha de cima para a de baixo | 6 IMPLEMENTADAS | Joinha pequeno em 8,0 s (se o rig já tiver; senão só o olho aberto) |
| 9,0-12,0 | C5 (2ª) - C6 | Passo 2: o 7º ganha o contorno externo e os 8º e 9º enchem pela metade | 1 EM EXPANSÃO / 2 PARCIAIS (em duas linhas, uma por batida) | Olho semicerrado |
| 12,0-16,0 | C7-C8 | Passo 3: os dois últimos ficam só contorno; a cor muda sem corte para #FF3B1F, o único vermelho do quadro | 2 FORA DO ESCOPO | Fica parado e olha para os dois |
| 16,0-19,0 | C9-C10 (1ª) | Prova 1: a grade completa, com os estados todos; ao lado, soma mono 6 + 1 + 2 + 2 = 11, calculada na tela a partir dos estados (não digitada) | rótulo mono: ANÁLISE DO TCC EM ENGENHARIA DE COMPUTAÇÃO | Em repouso |
| 19,0-22,0 | C10 (2ª) - C11 | Prova 2: a grade encolhe para o canto superior; quatro linhas mono entram, uma por batida | 100% LOW-CODE / POWER APPS · MICROSOFT LISTS / POWER AUTOMATE · POWER BI / RESTRIÇÃO, NÃO PREFERÊNCIA | Inclina a cabeça |
| 22,0-26,0 | C12-C13 | Fechamento: grade volta ao centro; frase em duas linhas, DEIXAR DE FORA em #FF3B1F | SABER O QUE DEIXAR DE FORA / TAMBÉM FOI ENGENHARIA | Olho semicerrado |
| 24,0-26,0 | C13 | Fecho seco do Bit, em balão reto, mute | DOIS DE FORA, ANOTADO (tom do Bit, não é fato; aprovar) | Único momento de destaque do Bit |
| 26,0-27,6 | C14 | O balão sai; a grade desce de volta ao estado do quadro 0 (todos os 11 viram contorno mute, em cascata inversa) | | Volta à pose de repouso do C1 |
| 27,6-28,0 | C14 | Respiro de 0,4 s: tudo parado | | Parado |
| 28,0-30,0 | C15 | Loop: o texto do gancho entra e fica; quadro 30 = quadro 0 | MEU SISTEMA NÃO COBRE TUDO | Igual ao C1 |

Observações:
- Cada ideia fica 2 s ou mais, exceto os cortes de texto de 0,5 s que são trocas de máscara, não ideias novas.
- Ponto final: o balão do Bit tem "DOIS DE FORA, ANOTADO" com um ponto no meio da frase, que é pontuação interna; se for lida como ponto final, trocar por "DOIS DE FORA, ANOTADO".
- Loop: render(0) == render(30): mesma posição da grade, mesmo estado dos quadrados, mesma pose do Bit; conferir diferença de pixels = 0 antes do grão.

## Mapa de som (eventos por compasso/batida; picos exatos, não o início)
Mix: trilha de `Producao/stems/` baixa, abaixa -10 dB sob os efeitos (ducking como no teste 5 v2). Sem voz, sem serviço externo. Todos os efeitos sintetizados por código (`AudioKit`). Alvo -14 LUFS e -1 dBTP, medidos depois do AAC.

| Tempo (s) | Compasso.batida | Evento sonoro | Movimento que sincroniza |
|---|---|---|---|
| 0,0 | C1.1 | Hit seco curto (grave) | Texto entra por máscara |
| 1,5 | C1.4 | Whoosh curto, sobe | Texto sai |
| 2,0-3,1 | C2.1 em diante | 11 estalos secos, 1 a cada 0,1 s, afinação sobe a cada estalo | Quadrados entram em cascata |
| 4,0 | C3.1 | Hit grave + estalo | Punch-in e marcador vermelho |
| 6,0 | C4.1 | Tick de preenchimento, tom médio, 1 por quadrado, 6 vezes (a cada 0,5 s, 6,0-8,5) | Cada quadrado enche |
| 9,0 | C5.3 | Tick, tom médio-alto | 7º ganha o contorno externo |
| 10,5 e 11,0 | C6.1 e C6.2 | 2 ticks mais agudos | 8º e 9º enchem pela metade |
| 12,0 | C7.1 | Hit grave, pico exatamente na troca de cor | Os dois últimos viram contorno vermelho |
| 12,0 | C7.1 | Swoosh descendente curto (pitch em queda), pico na chegada | Quadrado vermelho assenta |
| 16,0 | C9.1 | Tick agudo e soma contada: 4 ticks a cada 0,25 s | Soma 6 + 1 + 2 + 2 = 11 |
| 19,0 | C10.3 | Whoosh curto | Grade encolhe |
| 19,5, 20,0, 20,5, 21,0 | C10.4 a C11.3 | 4 ticks de teclado seco | As quatro linhas mono |
| 22,0 | C12.1 | Hit grave | Grade volta ao centro, frase entra |
| 24,0 | C13.1 | Estalo curto | Balão do Bit |
| 26,0-27,6 | C14.1 em diante | Swoosh descendente longo (1,6 s), cascata inversa de 11 estalos graves, 1 a cada 0,1 s | Grade desce e esvazia |
| 27,6-28,0 | C14 | Silêncio total, trilha em -inf dB | Respiro |
| 28,0 | C15.1 | Mesmo hit seco do C1.1 | Texto entra |

## Movimentos que descem (ligados aos swooshes descendentes)
1. Passo 1 (6,0-8,5 s): os quadrados enchem na ordem da linha de cima para a de baixo; o preenchimento "cai" (escala y de 0 para 1 a partir da borda de cima). Som: tick, sem swoosh.
2. 12,0 s: quadrado vermelho assenta 24 px para baixo por mola amortecida (w = 14). Som: swoosh descendente curto, pico na chegada.
3. 26,0-27,6 s: a grade inteira desce 40 px e esvazia em cascata inversa até o estado do quadro 0, depois sobe de volta ao centro em 0,3 s antes do respiro (para o quadro 28 ser igual ao 0). Som: swoosh descendente longo.
Os movimentos de subida (saída de texto por máscara, whoosh sobe) usam out cúbico; os de descida usam mola fechada com w 12-18.

## Verificação antes do render
1. `?sheet=compasso`: 15 quadros e `?safe=1` para conferir área segura.
2. 8 quadros: C1 (gancho), C3 (virada), C4 (passo 1), C6 (passo 2), C8 (passo 3), C10 (prova), C13 (fechamento) e C15/quadro 899.
3. Diferença de pixels quadro 0 x quadro 899 = 0.
4. Ler as legendas na ordem; nada sob a interface (topo 0-250, base 1480-1920, lateral direita 940-1080 a partir de y 900).

## Legenda do post (rascunho)
Instagram: "Avaliei o GMS contra o MESA-11. Das 11 funções, 6 estão implementadas. A análise está no meu TCC." (sem chamada pra ação)
TikTok: "meu sistema não cobre tudo. e eu mostrei onde" 
Hashtags: #engenhariadecomputacao #powerapps #industria40 #manufatura #lowcode

## Precisa de confirmação do William
1. Aprovar o fecho do Bit "DOIS DE FORA, ANOTADO" (tom, não é fato) ou trocar.
2. Aprovar "MEU SISTEMA NÃO COBRE TUDO": o texto original diz "Ele não cobre tudo" sobre o GMS; "meu sistema" é a minha paráfrase.
3. Joinha do Bit em 8,0 s depende de a pose existir no rig (`bit_joinha` está na lista de faltas em `Marca/bit/STATUS.md`); sem a pose, o Bit só mantém o olho aberto.
4. Nomear Power Apps, Microsoft Lists, Power Automate e Power BI na tela é nome de produto, já usado no post de LinkedIn.
5. A frase "porque a governança de TI permitia" ficou fora do vídeo por tamanho; "RESTRIÇÃO, NÃO PREFERÊNCIA" a resume.
