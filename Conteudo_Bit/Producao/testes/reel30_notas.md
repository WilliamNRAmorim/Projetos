# Reel 30 s "Meu sistema não cobre tudo" (GMS x MESA-11): notas e auditoria

Nada publicado, nada enviado, sem commit. Produtor-de-artes (Opus 5.5).

## Arquivos (Producao/testes)
- `reel30.html`: a peça. `?t=4.5`, `&safe=1`, `?sheet=compasso[&em=meio][&safe=1]`, `?folhas=1` (folhas + auditoria), `?render=1` (mp4 + medições).
- `reel30_30fps.mp4`: 1080x1920, 30 fps, 900 quadros, H.264 8 Mbps + AAC 192 kbps.
- `reel30_medicoes.json` (áudio depois do AAC, por evento) e `reel30_auditoria.json` (vídeo sem codec, quadro a quadro).
- Folhas: `reel30_folha_compasso.png`, `_compasso_safe.png`, `_compasso_meio_safe.png`, `reel30_8quadros.png`, `reel30_contato_1..4.png` (120 quadros, 1 a cada 0,25 s), `reel30_folha_eventos_1..9.png` (50 eventos, 4 quadros + forma de onda), `reel30_mix_preAAC.wav`.
- `reel30_bit_rig.js` e `reel30_audio_kit.js`: cópias com extensões só do reel30. Os compartilhados `bit_rig.js` e `testes/audio_kit.js` foram restaurados ao commit (git status limpo), então os testes 3, 4 e 5 v2 usam o mesmo código de antes.
  - `reel30_bit_rig.js`: expressão `neutro`; `face.lid`; pose `aponta`; `o.poseB/o.mix` (mistura de poses); `o.tilt` (inclina o tronco); `o.amp` (0 = parado: balanço, respiração e antena).
  - `reel30_audio_kit.js`: `o.freq` no clique e no tique; `cfg.trilha` (posição e envelope da música); `cfg.bitrateVideo`; `cfg.folhaPorParte`; `cfg.depois`; teto do limitador -2,0 dBTP (era -1,5); transiente de 0,8 ms no pico do swoosh descendente.

## Medições finais
- Vídeo, sem codec: quadro 0 x quadro 899 = 0 px, com e sem grão; render(0) x render(30) = 0 px. Respiro 27,6-28,0 s (13 quadros) parado, 0 px. Pureza (quadro 150 fora de ordem) 0 px.
- Área segura nos 900 quadros: 0 px de texto fora de x 90-940 / y 250-1480; 0 px de grade ou Bit no topo, na base ou nos botões. Largura máxima de texto: 850 px.
- Vermelho: 0 quadros com mais de um destaque (marcador, contornos fora do escopo, TUDO e DEIXAR DE FORA nunca convivem); 0 px vermelhos no Bit.
- Sobreposições texto x texto, texto x grade, texto x Bit, balão x grade/Bit e Bit x grade: 0 quadros. Máscaras não cortam nenhuma linha parada. Nenhum texto termina em ponto.
- Leitura plena (parado e inteiro) de toda ideia: 2,0 s ou mais (C2 2,0; C3 2,0; "= 11" 2,0; linha 4 2,0; balão 2,0; demais 2,2-4,0). Textos com número são contagens do vetor e conferem com o roteiro (6/1/2/2, 11, 100%).
- Áudio depois do AAC: -14,09 LUFS, -1,36 dBTP; erro de pico máximo 0,271 ms nos 50 eventos; limitador nos picos de efeito no máximo 0,28 dB; trilha -10 dB sob cada efeito; respiro -127 dBFS RMS.

## Simulações (calculadas)
1. Varredura: o marcador percorre as funções e cada quadrado assume o estado de `FUNCOES[i]` (I/E/P/F). Os tempos e os rótulos 6, 1, 2, 2 e 11 saem desse vetor.
2. Soma: cada parcela é a contagem de quadrados num estado. Os contados pulsam no tique e o total é `FUNCOES.length`.
3. Pilha: a barra LOW-CODE enche um segmento por ferramenta de `STACK`. O "100%" é a razão calculada.
Também derivados: grade (punch-in, encolhe, volta e desce) e esvaziamento em cascata inversa.

## Auditoria: defeitos achados e corrigidos (3 rodadas de folhas, 3 renders)
1. Frase de fecho invadia a grade (c12/c13): blocos passaram a caber por altura também.
2. Texto do C3 encostava na grade no punch-in: punch-in ancorado na borda de cima.
3. Leitura plena < 2 s (C2 1,5; C3 1,3; balão 1,5; linha 4 1,75; "= 11" 1,9): rótulos trocam por corte seco no tempo forte; encolher e voltar viraram 1 batida (18,5-19,0 e 21,5-22,0); linhas e parcelas a cada 1/3 de batida.
4. Soma mostrava "6" antes do rótulo (16,0): os dois entram juntos por corte.
5. Fragmentos de linha na saída por máscara (21,5): saída por corte.
6. Quadro 0 x 899 = 9050 px (até 2 níveis), por dois motivos. Primeiro, soma de molas em ponto flutuante: mola assentada agora devolve o valor exato. Segundo, o 1º desenho em cada canvas novo saía diferente: ele é refeito.
7. True peak -0,86 dBTP: teto do limitador -2,0.
8. Limitador cortava 2,97 dB e 2,07 dB nos hits empilhados de 12,0 e 22,0: níveis dos efeitos simultâneos reduzidos.
9. Swoosh descendente com erro de 5,8 e 6,1 ms depois do AAC (pico de ruído sem lugar fixo): transiente de chegada no pico.
10. Pulso da contagem fechava as folgas entre quadrados: escala 1,10 para 1,06.
11. A amostra "costura" do auditor pegava o Bit já respirando (1,67 s): erro do teste, corrigido.

## Desvios do roteiro (decisão humana)
- O gancho entra em 28,0 s e já está inteiro no quadro 0 (exigido por quadro 0 = quadro 899). Por isso não há hit em 0,0 s: ele tocaria sem evento na tela no loop.
- A soma e as 4 linhas vão a cada 1/3 de batida (0,1667 s), em vez de 0,25 s e 0,5 s: 0,25 s não cai em quadro inteiro, e 0,5 s deixava a linha 4 com menos de 2 s. As linhas entram de 19,0 a 19,5.
- Marcador assenta por queda acelerada que para seco em 12,0 (no lugar de mola w 14), para o pico ter instante definido.
- Rótulos por corte seco no tempo forte; máscara só no gancho, em "2 PARCIAIS" e na frase de fecho.
- Grade em y 672-1140 (a faixa 760-1100 não comporta 3 linhas de 140 px). Soma acima da grade, não "ao lado".
- Frase de fecho em 4 linhas visuais. Balão ao lado da cabeça do Bit (baseline ~1309), não em 1470.
- Bit em monocromático (filtro cinza): o corpo vermelho-laranja seria um 2º vermelho em todo quadro. Sem o anel do GMS, porque ele gira e quebraria o quadro 0 = quadro 899.
- Joinha (8,0 s) não existe no rig: usei a expressão `feliz` de 8,0 a 8,9 s.
- Trilha: na análise, a pulsação mais forte de music.wav é de 1 s (60 BPM, compatível com o meio-tempo de 120 BPM). Tempo forte em 1,996 s. Para 0-27,6 s uso o trecho 3,996-31,596 s; para 28-30 s, o trecho 1,996-3,996 s, o que deixa a música contínua na costura.
- Aprovações do roteiro continuam pendentes: "DOIS DE FORA. ANOTADO", "MEU SISTEMA" (paráfrase) e nomes de produto na tela.

## Limitações que restam
- Costura do áudio depois do AAC: salto de 0,0595 da última para a primeira amostra, contra 0,0303 entre vizinhas. Antes do AAC é contínuo (0,0208). É borda do codificador e pode dar um clique leve no loop do app.
- O AAC decodificado tem 768 amostras a mais no fim (preenchimento do codificador).
- Sem whoosh na subida de 27,3-27,6 s, para não vazar no respiro.
- Na primeira exibição, a abertura não tem som de entrada (o gancho já está na tela).
- O mono de 33 px (rótulo do TCC) é o menor texto. É legível em 1080 px, mas pequeno no celular.
- O render depende de fontes e do mp4-muxer por CDN.
