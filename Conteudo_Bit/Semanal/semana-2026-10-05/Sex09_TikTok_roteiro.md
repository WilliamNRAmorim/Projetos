# Sex 09/10 · TikTok @uiloumusk · Will Station · ~30 s

## Escolha (2 linhas)
Proposta B (objeto real + marco pessoal) com o fecho de A ("não é só arrumar impressora"); descartei a C (dramatização de erro).
Motivo: o benchmark põe o parente mais próximo no #6 (marco pessoal de hardware, 16,6K em 46 s) e a proposta B é essa estrutura; A entra só como frase final, porque "engenharia vs TI" já existe em PT com ~5K (#10, #11) e o que nos diferencia é o objeto real. C depende de piada interna (#16, #19 perdem) e esbarra na regra de não falar do erro.

## Formato
Vertical 9:16, 30 s, sem footage novo: as 3 fotos reais em movimento (zoom, corte, texto) + Bit pequeno animado por `bit_rig.js` e `ep_kit.js` (modelo `ep_virgula5h.html`). Visual: tela escura, Geist, destaque #FF3B1F, grão, glitch nos cortes. Bit nunca cobre o fliperama.

## Gancho (0–2 s)
Foto 1 (fliperama inteiro na cadeira), punch-in rápido + glitch. Texto, branco com "PEÇAS" em #FF3B1F: **TIVE QUE DEVOLVER AS PEÇAS.** Sem fala. Padrão Confession + Open Loop (HookMafia, evidência fraca, de fornecedor).

## Cena a cena
| Tempo | Imagem | Texto na tela (exato) | Fala do Bit |
|---|---|---|---|
| 0–2 | Foto 1, punch-in + glitch | TIVE QUE DEVOLVER AS PEÇAS. | (som de impacto, sem fala) |
| 2–7 | Foto 1, recuo lento; Bit pequeno no canto inferior, olho semicerrado | WILL STATION · 3 MESES | "Foram três meses." |
| 7–13 | Foto 3 (terminal), zoom na linha "Arduino SA Uno R3" | MONTA. DESMONTA. ERRO NO CÓDIGO. (uma linha por batida) | "Monta. Desmonta. Erro no código." |
| 13–19 | Foto 2 (joystick shield vermelho com botões), pan do joystick até a tela | CURTO-CIRCUITO. / CHOQUE. (glitch no segundo) | "Teve curto-circuito. Teve choque." |
| 19–25 | Foto 2 sobe para a tela (Super Mario World), depois corta em preto | ENGENHARIA ≠ TI | "O choque de realidade foi descobrir a diferença entre engenharia e TI." |
| 25–30 | Foto 1 de novo (loop com o gancho); lista entra em 3 linhas pequenas: ARDUINO UNO R3 · RETROPIE · SHIELD JOYSTICK. Bit aparece só no fecho, 1 s | NÃO É SÓ ARRUMAR IMPRESSORA. | "Devolvi as peças. Fiquei com a lição." |

Sem pergunta final nem chamada pra ação (regra do canal). A última imagem é a do gancho, o que ajuda o replay.

## Voz
Fala total ~30 palavras. Gerar por `tts.ps1`/ElevenLabs só depois de o William aprovar o texto e a voz (nada foi gerado). Alternativa sem voz: as mesmas falas viram legenda do Bit.

## Som sugerido
Trilha instrumental baixa já existente em `Producao/stems/` + um hit de impacto no 0 s e um estalo seco no "choque". Som de tendência: **não verificado**; o William checa no Creative Center (Brasil, 7 dias, uso comercial) e troca se achar um que sirva.

## Legenda
Devolvi as peças do Will Station. Foram 3 meses de mini vitórias e descobri que engenharia não é só arrumar impressora.

## Hashtags
#engenhariadecomputacao #raspberrypi #retrogaming #arduino #retropie
(as 3 primeiras foram as usadas no benchmark; não há dado de alcance delas)

## Precisa de confirmação do William
1. Texto e voz do Bit (falas acima) antes de gerar áudio.
2. [inferência minha] "Devolvi as peças" = fim do projeto físico; o texto diz só que teve que devolver as peças.
3. [inferência minha] O fliperama da foto 1 é o Will Station, e a tela da foto 2 (Super Mario World) é ele rodando por RetroPie; confirmar também se pode mostrar o jogo.
4. [inferência minha] Foto 3 mostra o Arduino Uno R3 reconhecido pelo Linux/RetroPie (aparece num `lsusb`); só uso o nome da peça, que está no texto-base.
5. [inferência minha] "Foi o choque que mostrou a diferença" parafraseia "choque de realidade para saber o que era engenharia e o que era TI". "Fiquei com a lição" é fecho meu.
6. Fotos e prints têm interface do Instagram nas bordas (setas, pontos): recortar. Confirmar se alguém aparece nelas (não vi pessoas).
7. Ordem do vídeo (peças → montagem → choque → lição) é minha, o texto não dá cronologia.
8. Não cito professor nem tempo/efeito do erro, e não repito a frase do último slide do sábado.

## Footage real e motor generativo (3 linhas)
Funciona sem footage novo, mas ficaria mais forte com um clipe de 3 a 5 s do fliperama ligando ou do joystick respondendo (celular, vertical): prova de que funciona e vence foto estática.
Gerativo (Veo/Gemini) só para cenas do Bit (Bit mexendo no Arduino, gesto de choque); como o rig 2D já anima o Bit, o ganho é pequeno e arrisca quebrar o estilo da marca, então eu não usaria agora.
Nunca para o fliperama real: seria inventar footage.
