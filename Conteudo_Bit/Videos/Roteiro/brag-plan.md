# GMS: filme vertical v2 ("A Linha")

**Formato:** 1080×1920 · 30 fps · 62 s · H.264 + AAC · trilha `music.wav` + `sfx.wav` originais, sem voz.
**Ângulo:** papel → dado ao vivo, contado por um único elemento que só anda pra frente. O ponto vermelho vira linha, a linha vira a régua de 8 meses, a régua vira o carretel de 8 etapas e o carretel assina GMS.

## O que mudou em relação à prévia
- **S03 corrigida:** sai "1 month / 5 months / 2 months". Entra uma régua de 8 meses com contador Month 1 → 8 e trechos proporcionais (Diagnose 1 · Build 5 · Harden 2). No "Today", a régua se enrola no carretel.
- **Nativo vertical:** nada de print horizontal espremido. As telas foram redesenhadas como cards grandes, legíveis no celular, com dados fictícios.
- **Sem legenda atrasada:** o texto na tela é o próprio roteiro, sincronizado com os efeitos.
- **Números legíveis:** a contagem dura 0,6 s e cada número fica parado ~1,1 s (antes eram ~0,6 s).
- **Zona segura do Instagram:** o conteúdo fica entre y 250 e 1560, longe dos botões e da legenda do app.
- **Sem nome da empresa:** o rodapé diz só "Kaizen Award submission · Q3 2026".

## Cenas (os tempos batem com a trilha)
| Cena | Tempo | O que acontece |
|---|---|---|
| S01 | 0–4 | Gancho: "387 paper sheets. Every month." sobre fichas manuscritas → o ponto vermelho queima o papel → "From paper to live data." |
| S02 | 4–10 | 6 flashes (1 por batida); a linha ganha uma cor de etapa a cada palavra |
| S03 | 10–20 | Régua de 8 meses: Diagnose → Build (chips 2,854 / 20 nos "dings") → Harden → Today (digitação nos 18 cliques) |
| S04 | 20–26 | Ficha da Trançagem: digita a OP (8 teclas), escolhe o carretel, Start, "Saved" |
| S05 | 26–32 | Painel da célula: 8 postos ao vivo; TH-07 para sem motivo nos dois bipes |
| S06 | 32–38 | Uma ordem rastreada: as 8 etapas acendem nas 8 notas |
| S07 | 38–44 | Hora a hora: alerta → "Why did it stop?" → Reel change → Shift closed |
| S08 | 44–52 | Prova: 36× · –97% · 100% (era 0%) · €0 |
| S09 | 52–62 | O carretel se desenha em 8 tempos → "Paper forgets." → G·M·S → "remembers." |

## Pra colocar a voz depois
Os blocos S01…S09 continuam nos mesmos tempos do storyboard, e o `mix.py` encaixa sua voz sem mudar nada. O texto de S03 no `COMO_GRAVAR_COM_ENERGIA.md` já foi atualizado.

## Como renderizar de novo
`05_Producao_videos/render.html` é o código do vídeo. Cada quadro é uma função pura do tempo, e as eases vêm do GSAP. Abra com `?t=12.5,30` pra ver quadros parados ou `?render=1` pra gerar o MP4 (precisa do servidor local que serve os stems).
