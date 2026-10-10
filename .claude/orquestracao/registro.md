# Registro do chefe

Uma linha por demanda: data | demanda | time e modelo de cada um | por quê | custo estimado.

2026-10-08 | Estudo de 513 prompts de vídeo Opus 5.5 para a equipe de arte | 6 exploradores (Haiku, ~700k tokens) + produtor-de-artes (Opus, ~78k tokens) | leitura volumosa e barata em Haiku, síntese em Opus | ver relatório uso_2026-10-08
2026-10-08 | Troca do ciano do glitch, semente do grão e teste 1 (forma em loop 6 s, 30 vs 60 fps) | eu (Sonnet) nas edições + produtor-de-artes (Opus, ~70k tokens, ~US$ 1) | edição pequena direta; render exige Opus | ~US$ 1
2026-10-08 | Teste 2: ?safe=1 e ?sheet=compasso no ep_kit.js | eu (Sonnet), sem subagente | edição pequena em um arquivo, sem regra de negócio; verificado no navegador | ~US$ 0,3
2026-10-08 | Teste 5: áudio por código 10 s, sincronia por pico e medição LUFS/dBTP | produtor-de-artes (Opus, ~250k tokens) | áudio é sempre Opus | ~US$ 1,5
2026-10-08 | Testes 3 (debounce conceitual), 4 (frase cinética), teste5_v2 (swoosh descendente + ducking) | bit (16k tokens) + 2 produtor-de-artes (Opus, ~110k + ~?), em paralelo | texto no bit; render e áudio sempre Opus | ~US$ 3 a 4
2026-10-08 | Análise de desempenho dos posts de hoje (TikTok e Instagram) | eu (Sonnet) coletei métricas no navegador + tit e insta em paralelo | coleta exige login e os agentes não têm navegador; análise barata e independente | ~US$ 0,5
2026-10-08 | Reel completo de 30 s (GMS x MESA-11) com desafio ao produtor | bit (45k tokens) + produtor-de-artes (Opus, ~315k tokens, retomado após limite de uso) + revisor-leve (Sonnet, 68k) | tema e roteiro no bit; render/áudio no Opus; conferência independente barata no Sonnet | ~US$ 9 a 13
2026-10-08 | Fusão das extensões do reel30 nos kits compartilhados (bit_rig.js, testes/audio_kit.js) e molde reel30.html | eu (Sonnet), sem subagente | edição mecânica, extensões opcionais; verificado carregando reel30, teste3 e bit_teste sem erros | ~US$ 0,5
2026-10-09 | Diagnóstico: dropdown de OP do Tubo vazio e 'fora da grade' no kanban | chefe (Opus) sozinho, sem subagente | leitura direta da lista e do YAML bastou | ver uso_2026-10-09.md
2026-10-09 | Teste no Studio: DisplayFields do combo de OP do Tubo | chefe (Opus) sozinho, via navegador | teste direto no Studio, sem salvar nem publicar | ver uso_2026-10-09.md
2026-10-09 | Hora-Hora do Mandril fora do padrão: diagnóstico (já existe molde MEL-224) | chefe sozinho (Opus) | consulta curta, sem subagente | ver uso_2026-10-09.md
2026-10-09 | Corrige erro PA1001 (fórmulas multilinha sem '=') na tela de Trançagem | chefe sozinho (Opus) | ajuste pequeno em 1 arquivo, sem subagente | baixo
2026-10-09 | Corrige erro de tipo (IfError Boolean x Table) na Trançagem e registra lições | chefe sozinho (Opus) | 1 tela + diário/lições, sem subagente | baixo
2026-10-09 | Commit geral do repositório (pasta Missão Manutenção e relatório de uso) | chefe sozinho (Opus) | só git, sem subagente | baixo
2026-10-09 | .gitattributes marcando binários para não corromper PDF no checkout | chefe sozinho (Opus) | config git, sem subagente | baixo
2026-10-09 | Testes 16 e 17 no QA de YAML (= no início e IfError Collect/Notify) | chefe sozinho (Opus) | script pequeno, plano já aprovado pelo William | baixo
2026-10-09 | Banco de 18 artes (Bit, Ficha, Carretel, cenários, objetos, personagens novos) gerado no Gemini via Chrome | chefe (Sonnet 5.5) dirigiu o Gemini; produtor-de-artes (Opus) escreveu os 30 prompts | Chrome é do chefe (subagente sem navegador); Opus só no texto dos prompts | total do dia US$ 32,61 (uso.ps1; parte deste pedido não separada)
2026-10-09 | Preparar posts/vídeos de amanhã (sáb 10/10): só conferi, já estavam prontos e no Drive (hash igual) | chefe sozinho, Sonnet 5.5, sem subagente | trabalho já feito pela rotina das 20h | custo ~US$ 0,1 (estimado)
2026-10-09 | Tetris refeito com voz (produtor-de-artes) + benchmark IG/TikTok + agendado QR Code no Instagram (sab 10/10 19h) pelo Meta | chefe (Sonnet 5.5) + produtor-de-artes (Opus 5.5, ~15 min, 118k tokens de subagente) | pedido do William; sim dado por item | custo: ver uso.ps1 do dia
2026-10-09 | Tetris v3 (estalo corrigido) trocado no Instagram; QR 19h agendado; Mario IG feito pelo William; TikTok Studio travou no upload (3 tentativas) | chefe (Sonnet 5.5) + produtor-de-artes (Opus 5.5, 3 rodadas) | sim do William por item; erro meu: abri menu da linha errada ao apagar, fechei sem escolher | custo: ver uso.ps1 do dia
2026-10-09 | Limpar banco de fotos do Bit (apagar o que não é Bit, manter cenários) | chefe sozinho (Sonnet 5.5), sem subagente | tarefa pequena, só olhar contact sheets e git rm | custo: uso.ps1 não rodado
2026-10-09 | Revisão do repositório em busca de lixo (só leitura, lista para o William decidir) | chefe sozinho (Opus 5.5 nesta sessão), sem subagente | levantamento por git ls-files/hash; subagente sairia mais caro | custo: ver uso_2026-10-09.md (sessão curta)
