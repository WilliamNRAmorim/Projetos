# GUIA DOS VÍDEOS SEMANAIS (para qualquer IA ou pessoa assumir a produção)

Escrito em 07/11/2026 pelo Claude, a pedido do William, para outro modelo (ex.: GPT) continuar o trabalho sem esta conversa. Tudo aqui está no repositório `C:\Users\willi\Downloads\Projetos`. Para os detalhes técnicos de cada armadilha, leia `Conteudo_Bit\Serie\aprendizados.md` (é o livro de lições de verdade).

---

## 1. O que é o produto
- **Canal:** YouTube `@Uiloumusk` (nome exibido "William Amorim") e TikTok `@uiloumusk`. Nada disso vai ao LinkedIn.
- **Formato semanal:** 28 Shorts verticais (4 por dia, 7 dias) + 1 vídeo longo horizontal no Dia 8.
  - Semana 1 (02 a 08/11): 28 contos de terror soltos (literário em domínio público, folclore brasileiro e originais). Pasta `contos-de-terror-semana\`.
  - Semana 2 (09 a 16/11): **uma série única, "PORTO SERENO"**, com 28 episódios de RPG de investigação + terror, no universo de Ordem Paranormal liberado pelo Cellbit. Personagens, cidade e enredo são originais. Pasta `contos-de-terror-semana\serie-semana-2\`.
- **Horários:** 9h, 13h, 18h e 21h (horário de Brasília), nas duas plataformas.
- **Cada Short:** 45 a 70 s, 1080x1920, 30 fps, H.264 + AAC, legenda queimada de 2 a 3 palavras por vez (Oswald branca com contorno).

## 2. Regras do William (não negociáveis)
1. **Quem posta é o William.** Nenhuma IA publica, agenda, envia, curte, comenta ou apaga nada sem o "sim" dele **para aquela ação**, com o texto final e o horário à vista. Um "sim" vale para uma única ação.
2. **Sem sangue explícito e sem violência com animal nas imagens.** Sugira, nunca mostre: use sombra, silhueta, som ou corte.
3. **Só material sem direito autoral:** imagens desenhadas por código (motor vetorial) e sons sintetizados. Banco externo só depois de conferir a licença de cada arquivo e avisar o William.
4. **Conto literário:** antes de gravar, confira o enredo no texto original (Wikisource, Domínio Público, poemuseum.org). Os roteiros feitos de memória erraram várias vezes (A Causa Secreta, O Enfermeiro). Para Poe, escreva uma versão própria, sem copiar tradução moderna.
5. **Variação:** nunca use o mesmo tom de voz em duas peças seguidas. Cada peça tem fundo e cor dominante próprios (na série, uma cor por ato ou dia).
6. **Capas** prontas e chamativas **antes do upload**, porque o TikTok não deixa editar post agendado. No YouTube a capa sai de um quadro do vídeo.
7. **Desempenho:** não conclua "formato X ganha de Y" sem benchmark de ~20 vídeos por plataforma. Os 5 ou 6 posts da própria conta não bastam.
8. **Roteiro e clímax precisam ser fortes.** Na série Plantão Noturno o William cobrou roteiro, detalhes e clímax melhores. Numa série, as pistas plantadas cedo são pagas depois, cada episódio se entende sozinho (gancho de 3 s, recap de uma linha) e termina em cliffhanger.
9. **Toda alteração:** commit por assunto e push na main. Os MP4 ficam **fora do git**.

## 3. Onde fica cada coisa
| O quê | Onde |
|---|---|
| Motor de animação (canvas vetorial → MP4) | `Conteudo_Bit\Producao\serie\motor.js` (documentado em `README.md` da mesma pasta) |
| Páginas de render | `serie.html` (série antiga), `contos.html` (contos e saga), `longo.html` (vídeo longo 16:9), `contato.html` (folha de contato do MP4) |
| Cenários e objetos extras por semana | `contos.js` a `contos7.js`, `contosO.js` (saga) |
| Sons sintetizados | `sfx.js`, `sfx_contos.js` (manual em `SFX_README.md`) |
| Episódio = JSON | `Producao\serie\ep\<id>.json` + `<id>_sons.json`; registre o id em `ep\indice.json` |
| Voz grátis (edge-tts) | `gen_voz_contos.py <id>` (perfis em `"vozes"` do JSON) |
| Voz ElevenLabs (sussurro, falas críticas) | `gen_voz_eleven.py <id>` (bloco `"eleven"` do JSON). A chave fica em `~/.elevenlabs`: nunca imprima nem commite. O plano Starter tem poucos créditos. |
| Driver do Edge headless | `Producao\serie\driver.js` (modos `shot`, `info`, `render`) |
| Servidor local | `Conteudo_Bit\Producao\serve.ps1` → `http://127.0.0.1:5178` |
| Saída dos MP4 | `Conteudo_Bit\Semanal\<pasta>\` (ex.: `contos-dia1`, `saga-dia1`); fora do git |
| Plano, roteiros e publicação (semana 1) | `contos-de-terror-semana\plano-7-dias-contos-de-terror.md`, `roteiros-dias-2-a-7.md`, `publicacao-28-pecas.md`, `BRIEFING_PRODUCAO.md` |
| Série Porto Sereno (semana 2) | `serie-semana-2\biblia.md` (mundo, personagens, pistas e arco), `roteiros-saga.md`, `publicacao-saga.md` (data, hora, título, legenda e capa de cada ep), `build\build_saga.py` (gera os JSON dos eps a partir do roteiro) |
| Lições acumuladas | `Conteudo_Bit\Serie\aprendizados.md` |
| Identidade do canal | `Conteudo_Bit\Serie\canal\` (banner, perfil, marca d'água) |

## 4. Pipeline de uma peça (passo a passo)
1. **Roteiro:** 130 a 170 palavras, na ordem gancho (0 a 3 s) → cenário → regra ou aviso → virada → frase final seca. Escreva sem contrações ("estou", "para o"; nunca "tô", "pro"), porque o edge-tts embola.
2. **JSON do episódio** em `ep\`: cenas, cenário, personagens (`elenco` fixo por personagem), objetos, câmera (`zoom`, `pan`), `cartela`, `cor`, `saida`, `arquivo` e `vozes`. Na saga, use `python build_saga.py N`.
3. **Cenário novo**, se a peça pedir: acrescente no `contosN.js`, sempre como opção ligada por parâmetro. **Nunca mude o comportamento das peças antigas.** Confira os quadros antigos com `?t=` e rode `node --check`.
4. **Vozes:** `python -X utf8 gen_voz_contos.py <id>`. Em seguida, procure arquivos com falha (áudio de 2 KB acontece com `rate` e `pitch` negativos) e gere de novo o que aparecer com valores um pouco diferentes:
   `find Conteudo_Bit/Producao/stems/serie/ep<id> -name "*.mp3" -size -6k`
5. **Sons:** cue-sheet `<id>_sons.json`. Sons de impacto (uivo, gongo, rugido, celular) ficam em volume de ~0,12 a 0,4; acima disso passam por cima da voz.
6. **Medir antes de renderizar:** `node driver.js info "http://127.0.0.1:5178/Producao/serie/contos.html?ep=<id>&mix=1"`. Alvos:
   - duração entre 45 e 70 s;
   - margem P5 da voz ≥ 6 dB sobre a cama em todas as cenas;
   - sem clipping.

   Se passar de 70 s, corte frases; não acelere a voz.
7. **Render:** `node driver.js render "http://127.0.0.1:5178/Producao/serie/contos.html?ep=<id>&render=1"`. Leva alguns minutos por peça. No Edge headless use `--disable-extensions` e **não** use `--disable-gpu`, que trava o desfoque. Apague os perfis `edgeprof-*` que criar.
8. **Conferir o MP4 final:** `node driver.js shot "http://127.0.0.1:5178/Producao/serie/contato.html?f=<pasta>/<arq>.mp4&n=12" folha.png --h=1100 --lim=400`. Olhe a folha: legenda legível, nada cortado, personagem com os pés no chão. Se o MP4 estiver aberto em outro programa, o render "termina" sem gravar: confira a data do arquivo ou mude o nome (`v2`).
9. **O que só o ouvido do William valida:** pronúncia, sotaque e o peso do sussurro. Diga isso a ele ao entregar.
10. **Vídeo longo (Dia 8):** `longo.html` junta MP4 prontos sem reprocessar as cenas: `node driver.js render ".../longo.html?render=1" --w=1920 --h=1080 --lim=1500` (~12 min). Escolha os vídeos de maior retenção quando houver dado; sem dado, use critério editorial e avise.

Não há ffmpeg nesta máquina. O áudio é medido pelo próprio Edge. Python: `C:\Users\willi\AppData\Local\Programs\Python\Python312\python.exe` (rode com `-X utf8`).

## 5. Publicação (só com o "sim" do William)
- **Texto pronto** em `publicacao-28-pecas.md` (semana 1) ou `publicacao-saga.md` (semana 2). No YouTube, o título vai como está, e a descrição leva a legenda + `#Shorts`, com "não é conteúdo para crianças" e a playlist da série. No TikTok, a legenda vai com as hashtags.
- **Porto Sereno:** mencione nas legendas "Inspirado no universo de Ordem Paranormal (liberado publicamente pelo Cellbit)", por decisão do William. Ainda falta conferir o texto da liberação.
- **Upload:** o William seleciona os arquivos na janela do Windows (o upload automático aceita só 10 MB e os MP4 têm ~30 MB). Depois disso, a IA pode preencher título, descrição, data e hora, mas só agenda com o "sim".
- **Armadilhas que já custaram caro:**
  - Clique por coordenada sem olhar a tela: o layout muda entre abas.
  - Data e hora: no TikTok, escolha o minuto 00 e depois a hora; o calendário do YouTube pode pular para 2027 se clicar rápido. Confira com zoom antes de agendar.
  - Identifique o vídeo pelo **nome do arquivo** na aba, nunca pela posição.
  - Só diga "programado" depois de ver a lista: YouTube em Conteúdo > Shorts, TikTok em Publicações.
  - Com "alterações não salvas" no YouTube, nunca force a navegação.
- **Proposta pendente (o William não aprovou):** aprovar a semana por lote, com um `lote.json` e um "sim" só para todos. Até ele aprovar, vale um "sim" por ação.

## 6. Custo e limite (o William usa o plano Pro; o limite semanal acaba rápido)
- A produção cabe num modelo médio (Sonnet ou equivalente). Modelo caro só para um elemento visual novo e difícil.
- O que mais gastou foi a revisão visual quadro a quadro e as screenshots no agendamento. Revise só a folha de contato e só as cenas que mudaram. Reaproveite cenários e poses.
- Use no máximo 1 a 2 rodadas de correção por peça. Antes de render grande, dê ao William a estimativa de tempo e de custo, inclusive caracteres da ElevenLabs.
- Em 07/11, várias sessões da semana 2 caíram no limite no meio do trabalho. Antes de refazer, confira o que já existe em `Semanal\saga-dia*` e `ep\s*.json` / `ep\o*.json`.

## 7. Estado em 07/11/2026 (confira antes de continuar)
- **Semana 1:** 28 Shorts + o longo programados no YouTube, 28 agendados no TikTok.
  - Pendente: apagar o rascunho duplicado "05 o coracao delator" no YouTube.
  - Pendente: trocar a lista do longo pelos de maior retenção.
- **Semana 2, Porto Sereno:** bíblia, roteiros e publicação escritos.
  - A publicação vai de seg 09/11 (eps. 1 a 4) a dom 15/11 (eps. 25 a 28); o filme com os 28 fica para seg 16/11.
  - Render e capas estavam em andamento, em `Conteudo_Bit\Semanal\saga-dia1` a `saga-dia7`.
  - A pasta `saga-dia7-opus` é uma tentativa paralela; compare antes de escolher.
  - Nada foi postado nem agendado.
- **Ao terminar cada dia:** entregue os MP4, o que foi medido e as escolhas que o William pode mudar. Registre as lições novas em `Serie\aprendizados.md`.
