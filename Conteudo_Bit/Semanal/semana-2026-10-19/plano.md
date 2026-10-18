# Semana 19–25/10: 14 posts em lote (2 por dia) + 1 LinkedIn

Produzido no sábado 17/10/2026. No domingo 18/10 agendar tudo com o Claude (TikTok Studio e Meta Business Suite).
**Todos os 14 vídeos saíram SEM voz**: a API do ElevenLabs devolve 401 para qualquer fala com mais de uma palavra (cota da chave "bit-conteudo" esgotada; um teste de 3 caracteres passou). Roteiros prontos em `Producao/falas_2026-10-19.json` e `Producao/gen_voz.ps1` gera as vozes quando houver crédito; depois basta trocar `semVoz: true` por `stems: '/w/stems/s19_<ep>'` em `ep_semana_2026-10-19.html` e renderizar de novo.
Reaproveitamento: nenhum vídeo pronto sem postar sobrou (a semana 12–18 foi agendada 28/28).

| Dia | 12h (fato rápido / humor) | 19h (história A) |
|---|---|---|
| Seg 19 | Tesla Roadster, apresentado em 15/10 (`Seg19_1_…TeslaRoadster`, 27 s) | Larry Tesler e o "sem modos" (`Seg19_2_…Tesler`, 52 s) |
| Ter 20 | Suspeito: o estagiário (`Ter20_1_…SuspeitoEstagiario`, 16 s) | Knight Capital, US$ 440 mi em 45 min (`Ter20_2_…KnightCapital`, 53 s) |
| Qua 21 | Win+V (`Qua21_1_…WinV`, 20 s) | Dyn/Mirai, 10 anos (`Qua21_2_…DynMirai`, 57 s) |
| Qui 22 | QWERTY, o mito (`Qui22_1_…QWERTY`, 28 s) | O botão que não apertava de luva, dramatização (`Qui22_2_…BotaoDeLuva`, 48 s) |
| Sex 23 | O barulho do modem (`Sex23_1_…ModemDiscado`, 24 s) | iPod, 25 anos (`Sex23_2_…iPod`, 55 s) |
| Sáb 24 | Pac-Man / Puck-Man (`Sab24_1_…PacMan`, 27 s) | E.T. do Atari enterrado (`Sab24_2_…ETdoAtari`, 51 s) |
| Dom 25 | Bliss, a foto real do XP (`Dom25_1_…BlissWallpaper`, 28 s) | Windows XP, 25 anos (`Dom25_2_…WindowsXP`, 50 s) |

LinkedIn (1 post): **Ter 20/10, 08:30**, Knight Capital (texto fiel aos fatos, ângulo novo: práticas de deploy). `LinkedIn_Ter20_Knight_texto.txt`.
Pilares: fatos e datas em alta 9 (Tesla, Dyn 10 anos, iPod 25, XP 25, Bliss, Pac-Man, E.T., QWERTY, modem), histórias de projeto 1 (luva, dramatização sem dado real), dia a dia dev 4 (Tesler, Knight, Suspeito, Win+V).
Reserva (renderizado e removido da grade por causa do Tesla): CC = cópia carbono (reproduzir com `?ep=cc`, roteiro no JSON).
Datas casadas: Dyn em 21/10 (10 anos), iPod em 23/10 (25 anos), XP em 25/10 (25 anos).
Arquivo de produção: `Producao/ep_semana_2026-10-19.html?ep=tesla|tesler|suspeito|knight|winv|dyn|qwerty|luva|modem|ipod|pacman|et|bliss|xp|cc` (cenas em `eps19_a.js` e `eps19_b.js`).

## Fontes dos fatos (WebSearch em 17/10/2026)
- **Tesla Roadster:** apresentado em 15/10/2026 perto de Waco, Texas (adiado de 1/10 por clima), desenvolvido com a SpaceX; 0–60 mph em menos de 1 s na demonstração (Tesla lista < 1,6 s na versão base e < 0,9 s com propulsores de gás frio); sem preço; produção em 2028 segundo Musk (CNBC 15/10/2026; Detroit News 15/10/2026; Teslarati). No vídeo: só "menos de 1 s, segundo a própria Tesla", gás frio, sem preço, 2028.
- **Tesler:** Larry Tesler e Tim Mott, Gypsy (modeless), Xerox PARC desde 1973; nomes e fluxo recortar/copiar/colar; placa "NO MODES" (Wikipedia, TNW, TechRadar; relatos variam, por isso "dizem"). Morreu em fevereiro de 2020. Ctrl-X/C/V não aparece no vídeo.
- **Knight Capital:** 1/8/2012, perda pré-impostos de US$ 440 mi em ~45 min (algumas fontes dizem 460), 8 servidores com 1 desatualizado, flag reaproveitada que acordou a função "Power Peg", sem kill switch, resgate de emergência (Wikipedia, bad.technology, SmartBear). Ações afetadas: "mais de cem" (fontes: 148 ou 154).
- **Dyn/Mirai:** 21/10/2016, DNS da Dyn, Mirai em câmeras, DVRs, babás eletrônicas, senhas padrão, "dezenas de milhões de IPs" (Dyn) (Wikipedia, APNIC, PCWorld). Sites no ar, ninguém resolvia o DNS.
- **Luva:** dramatização, nada de dado real. Tela touch comum não responde a luva grossa (conhecimento geral).
- **iPod:** 23/10/2001, 5 GB, 1.000 músicas, US$ 399, só Mac, roda mecânica, descontinuado em 2022 (iPod touch, maio/2022) (Apple press release, ABC News, MacTrast). "Centenas de milhões": ordem de grandeza (Apple vendeu mais de 400 mi, conhecimento público).
- **E.T. Atari:** 1983, aterro de Alamogordo, escavação em 26/4/2014, achados de E.T., Centipede, Asteroids; Howard Warshaw estimou até 750 mil cartuchos (Xbox News, Prima Games, Snopes, Time). "5 semanas": relato recorrente do próprio Warshaw (não conferido de novo nesta busca).
- **XP:** retail em 25/10/2001 (conhecimento geral, não confirmado na busca), fim do suporte em 8/4/2014 (12,5 anos). Exigência de ativação e visual criticado: contexto conhecido. Caixas eletrônicos com XP: amplamente reportado.
- **Bliss:** janeiro de 1996, perto da divisa Napa–Sonoma, Charles O'Rear, Mamiya RZ67 e Velvia, sem retoque segundo ele; Microsoft comprou os direitos (Wikipedia, Creative Bloq, UCR). O vídeo usa ilustração em código (a foto tem direitos).
- **Modem:** handshake em etapas V.8/treinamento de linha, calar do alto-falante ao fim (goughlui.com, metafilter).
- **QWERTY:** teoria de "travar" é debatida; ajuste com ajuda de telegrafistas (Science Focus, Wisconsin; The Star, QuickCheck de 6/10/2026).
- **Pac-Man:** Puck-Man (Japão, 1980), paku-paku, troca por medo de vandalismo, pizza segundo Iwatani (conhecimento geral, amplamente documentado; não reconferido).
- **Suspeito, Win+V:** humor; Win+V existe no Windows 10 (versão 1809) em diante e pede ativação na primeira vez.

## Reconferido depois da produção
XP em 25/10/2001 (Wikipedia, Redmond Mag 2001), E.T. em pouco mais de 5 semanas (Warshaw, NPR/Engadget) e Puck-Man trocado por medo de vandalismo (Midway; a explicação repousa em relatos de 1983 e livro de 2002, por isso o vídeo diz apenas 'medo de vandalismo'). A pizza do Pac-Man segue como relato do criador ('contava').
