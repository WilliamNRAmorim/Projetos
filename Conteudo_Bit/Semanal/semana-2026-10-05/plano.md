# Semana 05–11/10: estreia

> Estreia adiada de terça 06/10 para **quarta 07/10**: o GMS sai no LinkedIn de manhã e no Instagram e TikTok às 19h.

## Situação em 06/10 à noite
- **Quarta 07/10, tudo agendado:** LinkedIn 08:30 (texto MESA-11), story-teaser 12:00 (Meta Business Suite), Reel 19:00 (Meta Business Suite), TikTok @uiloumusk 19:00 (TikTok Studio). Manual: às 19h, compartilhar o Reel no story pelo app.
- **Quinta 08/10 (Episódio 1): NÃO agendado.** Vai ser refeito com o Bit e a Ficha do Gemini (prompts 5 e 6 do `Marca/bit/PROMPTS_GEMINI.md`) e com as vozes do ElevenLabs (`Producao/tts.ps1`). Faltam as artes; a geração no Gemini web travou no modo Pro. Se não sair a tempo, o episódio vai pra semana seguinte.
- **Sábado 10/10:** carrossel ainda não agendado; teaser `Sab10_Story_Mario.mp4` pronto (story às 09:00). O carrossel usa o Bit antigo nos slides.

**Ideia da semana:** apresentar o trabalho e o personagem. O GMS entra primeiro, como prova de que o trabalho é real. Depois aparece o Bit, que vai ser a cara de todos os próximos projetos.

**Fio condutor:** "a fábrica não via o que acontecia, agora vê tudo ao vivo", e o Bit (que lembra de tudo) contra a Ficha (o papel, que esquece tudo).

| # | Dia | Rede | Horário | O quê | Arquivo |
|---|---|---|---|---|---|
| 1 | Qua 07/10 | LinkedIn | 8h–10h | O projeto completo | `04_Videos/Publicar/GMS_Reel_PT_78s.mp4` + texto do LinkedIn em `posts_prontos.md` |
| 1 | Qua 07/10 | Instagram | 19h | O projeto, versão curta | `04_Videos/Publicar/GMS_Reel_PT_30s.mp4` + texto do Instagram em `posts_prontos.md` |
| 1 | Qua 07/10 | TikTok | 19h | O projeto, versão curta | `GMS_Reel_PT_30s.mp4` + texto do TikTok em `posts_prontos.md` |
| 2 | Qui 08/10 | Instagram + TikTok | 19h | **Episódio 1 do Bit:** "POV: você é uma ficha de papel e a fábrica comprou um tablet" | vídeo novo (15–20 s), feito pela tarefa de sábado nesta pasta |
| 3 | Sáb 10/10 | Instagram (carrossel) + TikTok | 11h / 19h | **Curiosidade de games apresentada pelo Bit:** o primeiro slide apresenta o Bit, e os seguintes trazem uma curiosidade real e verificada sobre videogames (tema em alta, que puxa o Will Station nas próximas semanas) | imagens 1080×1350 feitas pela tarefa nesta pasta |

Pilares da semana: post 1 = projeto (GMS) · post 2 = dia a dia/humor (Ficha × Bit) · post 3 = curiosidade/tema em alta (games).

## Episódio 1 (roteiro base, 15–20 s)
1. **Gancho (0–2 s):** a Ficha, toda feliz na prancheta: "POV: você é uma ficha de papel numa fábrica"
2. **Virada (2–6 s):** chega um tablet. A Ficha fica chocada.
3. **Conflito (6–12 s):** alguém pergunta "quanto produziu ontem?". A Ficha faz olhos em espiral ("?"). O Bit responde na hora, tranquilo, com o número na tela.
4. **Fecho (12–18 s):** a Ficha amassada, o Bit dá um joinha. Texto final: "O papel esquece."

Trilha: stems da produção. Sem chamada pra seguir, só o episódio.

---
## Sexta 09/10 (rotina diária, gerada em 08/10 à noite)
Pilares: A = fato histórico em história com arco (Apollo 11) · B = fato rápido/myth-busting (primeiro bug) · C = humor dia a dia (dev).
O carrossel do Will Station de sexta (Sex09_Instagram_WillStation_*) vem de outra sessão; por isso nenhum vídeo de hoje fala de projeto.
**Benchmark e métricas de 24 h/72 h: não feitos nesta execução** (TikTok sem login no navegador do app; Meta e LinkedIn não consultados). Roteiros aplicam as regras atuais da receita: voz do Bit no A, porquê por trás do fato, tensão, virada; B e C sem voz, com mini-arco.

| # | Horário | Vídeo | Tema | Redes |
|---|---|---|---|---|
| A | TikTok 11h · Instagram 12h | `Sex09_A_Instagram_TikTok_Apollo1202.mp4` | O alarme 1202 da Apollo 11 (história, narrada, ~73 s) | TikTok + Instagram |
| B | TikTok 15h | `Sex09_B_TikTok_Instagram_PrimeiroBug.mp4` | O primeiro bug era um inseto, mas a palavra já existia (myth-busting, ~20 s) | TikTok (+ Instagram se quiser) |
| C | TikTok 19h · Instagram 19h | `Sex09_C_TikTok_FuncionaNaMinhaMaquina.mp4` | "Funciona na minha máquina" e o Docker (humor, ~20 s) | TikTok + Instagram |

### Fontes dos fatos
- **A (Apollo 11):** alarme 1202 por sobrecarga do computador de guiagem (AGC) a ~5 min do início da descida motorizada; tarefas começavam mais do que terminavam e a memória temporária acabou; o computador reiniciava e descartava tarefas de baixa prioridade; Steve Bales (guiagem, Houston) deu GO; o alarme repetiu; a tripulação não tinha visto o alarme nas simulações; ~2.048 palavras de memória apagável (~4 KB). Fontes: Discover Magazine "Apollo 11's 1202 Alarm Explained"; MIT News 2009 (Apollo Eyles); Science Museum blog "Apollo 11 moon landing: the most difficult moments". Não afirmei "pior que uma calculadora" (não confirmado). Não afirmei a idade de Bales nem causa exata do radar.
- **B (primeiro bug):** mariposa achada no relé #70, painel F, do Harvard Mark II em 9/9/1947, colada no caderno com a nota "First actual case of bug being found"; hoje no Smithsonian (NMAH). O termo "bug" já era usado antes (carta de Edison, 1878). Não atribuí a nota a ninguém (autoria disputada: Hopper x Bill Burke). Fontes: National Geographic Education "World's First Computer Bug"; Science Notes (9 set).
- **C:** piada/humor (sem dado). Afirmação técnica: Docker empacota código, bibliotecas e dependências do ambiente num container.
