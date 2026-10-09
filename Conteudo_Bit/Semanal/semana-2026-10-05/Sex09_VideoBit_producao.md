# Curta do Bit (pixel art): ficha de produção

Estado em 08/10/2026. Nada produzido. **A arte está em espera**: o William pediu para esperar o estudo da equipe de arte da outra conversa.

## Origem e direitos
- Vídeo feito pelo William para um cliente, a KSH Partners (cartão final com "KSH Partners · ksh-partners.cz"). Ele autorizou o uso no canal.
- A fonte (HTML/projeto do editor) foi perdida. Só existem o MP4 (`Downloads/WhatsApp Video 2026-10-08 at 18.28.52.mp4`, 478x850, 58 s) e o roteiro.
- Destino: TikTok @uiloumusk e Instagram @uiu.engenharia. **Não vai ao LinkedIn.**

## Cenas do original (vistas em 08/10)
| Cap. | Rótulo original | Cena | Personagens |
|---|---|---|---|
| I | the question | banco numa colina sob estrelas | humano + bichinho rosa de pixels (o "Claude") |
| II | the work | anel rosa (buraco negro) com faixa | sem personagem |
| III | the wanting | grade de ícones pixel (T, coração, alien, xícara...) | sem personagem |
| IV | the weight | ampulheta com luz | sem personagem |
| V | the point | o mesmo banco ao amanhecer, depois preto; "AI can carry the work." e, em vermelho, "The point stays human."; rodapé KSH Partners | humano + bichinho |

Layout do original: faixa preta no topo com o rótulo do capítulo e faixa preta embaixo com a fala (nome do personagem pequeno em cima da fala). O que fica entre as faixas é a imagem.
Áudio: trilha de fundo contínua (de ~1,5 s a ~57 s) mais uma voz para o "Você" e outra para o "Claude". Não foi possível separar nem identificar as vozes originais.

## Plano de refazer
1. Reaproveitar o vídeo original nos capítulos II, III e IV (sem personagem), cobrindo as duas faixas pretas e redesenhando rótulo e fala em português.
2. Recriar em código (motor do canal) os capítulos I e V com o Bit sentado no banco no lugar do bichinho rosa, usando o MP4 como referência de visual.
3. Cartão final: mensagem em português (forte: "A máquina leva o trabalho. O motivo é de gente."). **Decidido pelo William em 08/10: o crédito da KSH Partners sai e o vídeo vira do canal.** Nenhum quadro leva o nome ou o site da KSH.
4. Texto em português: `Sex09_VideoBit_roteiro_PT.md` (falas aprovadas pelo William, com "voltar a ela" no capítulo IV).

## Áudio
- Voz do Bit: voz "Bit" da conta ElevenLabs (`Producao/tts.ps1`, chave em `~/.elevenlabs` já existe).
- Voz do "Você": a escolher. Amostras em `Producao/stems/curta_amostras/` (Will, Chris, Eric).
- Trilha: o arquivo original não está separado; usar `stems/music.wav` do canal ou outro arquivo que o William tenha.

## Pendências
- Estudo da equipe de arte (outra conversa).
- Escolha da voz do "Você" e da trilha.
- (resolvido) Crédito da KSH Partners removido, a pedido do William.
- Marcar como conteúdo de IA nas redes (confirmar com o William).
- Publicação: só com o "sim" do William, com a legenda e o horário à vista.
