# Como o GMS_Defesa.pptx é montado

O deck é gerado por script, com o PowerPoint dirigido pelo COM do Windows (PowerShell 5.1). Nada é editado à mão: mudou o slide, muda o script e roda de novo.

- `gms_lib.ps1`: funções reutilizáveis (novo deck, carretel com progresso, fio, texto, notas, salvar com os ajustes de XML, exportar).
- `cap1.ps1`: os 10 slides do capítulo 1 (gera o deck do zero). `-SemVideo` pula o vídeo de revisão.
- `cap2.ps1`: os slides 11 a 14 (capítulo 2, quadros 7 a 10). Rode DEPOIS do cap1: não regera o cap1, abre `GMS_Defesa.pptx`, apaga o que houver além do slide 10 (pode rodar de novo à vontade), acrescenta os 4 slides e salva. O arquivo não pode estar aberto no PowerPoint (o script avisa e para; nunca fecha o PowerPoint do usuário).
- `cap3.ps1`: os slides 15 a 24 (capítulo 3, quadros 11 a 15: 11a–11d, 12, 13a–13c, 14, 15 = 10 slides; o deck fecha em 24, não 25). Rode DEPOIS do cap2 (ordem: cap1, cap2, cap3; cada um abre o deck e acrescenta). Idempotente como o cap2. O `cap3.mp4` começa no slide 14; `cap3.pdf` tem o deck inteiro (24 slides).
- `cap4.ps1`: os slides 25 a 35 (capítulo 4, quadros 16 a 18: 16a–16f, 17, 18 e 18B1–18B3 ocultos = 11 slides; o deck fecha em 35). Rode DEPOIS do cap3 (ordem: cap1, cap2, cap3, cap4). Idempotente: apaga o que passar de 24. `cap4.mp4` começa no slide 24 e mostra também os ocultos (só no vídeo); `cap4.pdf` tem o deck inteiro.
- `cap5.ps1`: os slides 36 a 41 (capítulo 5, quadros 19 a 23: 19, 20, 21a, 21b, 22 e 23 = 6 slides; o deck fecha em 41). Rode DEPOIS do cap4 (ordem: cap1 a cap5; todos com `-SemVideo` menos o cap5 gera o deck inteiro em poucos minutos). Idempotente: apaga o que passar de 35. `cap5.mp4` começa no slide 35 (último oculto do plano B, desocultado só no vídeo); `cap5_entrada32.mp4` mostra 32 → 36 → 37 sem os ocultos (a outra entrada do capítulo); `cap5.pdf` tem o deck inteiro.
- As notas do apresentador saem de `../roteiro.md` na hora da montagem.
- Saídas: `../GMS_Defesa.pptx`, `../previa/capN/slide_NN.png` (1920×1080; no cap2 só os slides novos, com a numeração do deck inteiro: `slide_11` a `slide_14`), `../previa/capN/capN.pdf` (o deck inteiro até o capítulo) e `../previa/capN/capN.mp4` (vídeo de revisão das transições, 3 s por slide; não entra no deck; o `cap2.mp4` começa no slide 10, último do cap1, para mostrar a transição 10→11).

## Regras aprendidas no capítulo 1 (valem para todos os capítulos)

1. **Morph não entra pelo COM.** `EntryEffect = 3954` dá erro. O script salva, edita o XML de cada slide (`p159:morph option="byObject"`, 1,2 s) e reabre. Avanço só por clique.
2. **Continuidade é pelo nome.** O objeto que passa de um slide ao seguinte tem o mesmo nome nos dois, começando com `!!`.
3. **Nunca use forma livre em objeto que participa do Morph.** O PowerPoint interpola a forma livre como contorno fechado e preenchido: aparece uma mancha da cor da linha no meio da transição.
4. **Arco que cresce: a mesma caixa nos dois slides, e só o ângulo muda.** Um arco achatado (caixa com 1 pt de altura) é uma barra sólida; o Morph estica essa imagem até a caixa final e aparece um bloco cheio. O carretel e o fio seguem esta regra. O estado inicial é um toco de 1 grau escondido sob a linha ou sob o ponto.
5. **Ângulo monotônico.** O Morph interpola o valor do ajuste em linha reta. Para fechar em 360 graus use 21540000, não 0, senão o arco dá a volta pelo lado errado.
6. **Ponta redonda e sem preenchimento vão no XML.** O COM não grava `cap="rnd"` nem `<a:noFill/>` em arco; `Save-GmsDeck` faz isso para todo `!!arco*` e `!!fio*`.
7. **Animação de entrada só em objeto sem `!!`.** Entrada em objeto que participa do Morph briga com a transição.
8. **Os PNGs não mostram defeito de transição.** O quadro parado sai certo mesmo com mancha no meio do Morph. Confira sempre o vídeo de revisão.

## Continuar um deck existente (cap2 em diante)

- `Open-GmsDeckForAppend $pptx` abre o deck sem janela e ajusta `$script:slideN` para a contagem atual; `New-GmsSlide` segue dali. `Export-GmsSlides $dir 1920 1080 @(11,12,13,14)` exporta só alguns slides.
- `Save-GmsDeck` agora salva num temporário e troca o arquivo (funciona com o deck aberto do próprio caminho) e é idempotente: ao reabrir, o PowerPoint regrava o Morph dentro de `mc:AlternateContent`; a função apaga toda transição antiga (AlternateContent, `p:transition` vazia ou não) antes de inserir a sua. Conferido: slides 2 a 14 com uma transição Morph cada, slide 1 sem.
- Elo entre capítulos: o último slide do capítulo anterior tem objetos `!!`; o primeiro do seguinte recria os MESMOS nomes (no cap2, `!!e1` a `!!e8`, círculo de 36 px, forma 5 com ajuste 0,5) em outras posições, e o Morph faz o caminho. Objeto do slide anterior que não existe no seguinte some em fade.
- Fio que nasce de um anel: arcos (`!!arcoTurno1..3`, mesma caixa em todos os slides, só o ângulo muda; no slide do fio os três recolhem a um toco de 1 grau em 179–180°, escondido sob uma bolinha) e linha-semente `!!fioL1` de 2 px escondida sob o arco do turno 2, que no slide seguinte estica até virar o fio. Nenhuma forma livre.
- Nomes `!!arco*` e `!!fio*` ganham ponta redonda e noFill no XML; use esse prefixo para todo arco/linha que participa de Morph. `!!passagem` (retângulo) vira, no quadro 10, a tela do tablet: mesmo tipo de forma, só muda a caixa.
- Rodapé muito longo invade a área do carretel (x até 1695): no máximo ~58 caracteres de citação.

## Como medir as transições do vídeo (mapa de tempo resolvido)

Cada slide dura 4,2 a 4,4 s no mp4: 3 s parado, e a transição para o seguinte começa em ≈3,0 s (slide 10 do deck como primeiro quadro) e depois a cada ≈4,3 s (cap2: 3,0 / 7,4 / 11,6 / 16,0 s; 20 s no total). O slide 10 do vídeo mostra por volta de 0,8–2,6 s as animações de clique dele (fade das frases), que o vídeo dispara sozinho. Para não depender de tempo: suba um servidor local só de leitura (`python -m http.server 8766` em `previa/`; encerre depois), abra `http://127.0.0.1:8766/cap2/cap2.mp4` no Browser pane, faça `fetch` do vídeo como blob, passe `currentTime` de 0,2 em 0,2 s e some, num canvas 192×108, os pixels ciano e a diferença entre quadros. A transição aparece como pico de diferença e o ciano deve ficar entre os valores de antes e depois (a contagem inclui texto ciano que entra e sai). Para ver um quadro, ponha o `<video>` em tela cheia (`position:fixed`) e tire um screenshot.

Medição do cap2: 10→11 ciano 0→269 monótono; 11→12 e 12→13 caem no meio (os arcos recolhem e o texto ciano sai) e voltam abaixo do valor final; 13→14 177→528 sem pico acima do final. Nenhuma mancha; a transição 10→11 (pontos em fila viram o anel) sem defeito.

## Onde o deck roda e como ver fora do PowerPoint

A defesa roda no **PowerPoint** (decisão do William em 13/11). O Google Slides não serve nem para conferir: ele não tem a fonte Bahnschrift nem a letra manuscrita da ficha, troca por letras mais largas e o texto invade o que está ao lado; e não tem Morph, então o carretel não fecha e os slides não se ligam. Para ver em outro aparelho, cada capítulo exporta também um PDF em `../previa/capN/capN.pdf`, além dos PNGs e do vídeo de revisão.

## Distribuição dos objetos no slide

Slide de 1920×1080 px. Regras para todos os capítulos:

1. Nada a menos de 96 px da borda, fora o carretel do canto e o que sai do slide de propósito (ficha em zoom, caixa de arco).
2. Pelo menos 32 px entre objetos que não se tocam de propósito. O fio pode passar por trás de cartões e estações.
3. O carretel do canto ocupa de x 1735 a 1865 e de y 920 a 1050: nenhum texto entra nessa área nem a menos de 40 px dela.
4. O conteúdo fica equilibrado na altura: não deixe metade do slide vazia com tudo espremido na outra metade.
5. Um objeto não repete a informação de outro no mesmo slide (ex.: cartão "SAP" e rótulo "SAP").

### Moldura fixa (o que o pitch do TCC I fazia bem)

O pitch da qualificação, que tirou nota 10, tinha a mesma moldura em todo slide: título no alto à esquerda, uma frase-guia logo abaixo com as palavras-chave em cor, conteúdo em fileiras de caixas iguais alinhadas pela mesma margem, citação ao lado da afirmação e contador de página. A defesa mantém o visual escuro e o Morph, e adota essa disciplina:

1. **Rótulo do capítulo** no alto à esquerda (x 96, y 64): Bahnschrift SemiBold Condensed 28 pt, maiúsculas, na cor do capítulo (O PROBLEMA, O MÉTODO, A CONSTRUÇÃO, A EXPANSÃO, OS RESULTADOS, AS LIMITAÇÕES, FOREST CITY E O FUTURO, A TESE). Nome `!!rotulo`, para ficar parado dentro do capítulo.
2. **Frase-guia** logo abaixo (x 96, y 120), alinhada à esquerda, 44 a 54 pt, largura máxima de 1500 px, com as palavras-chave na cor do capítulo. No slide de número-herói, o número entra no lugar da frase-guia, centralizado.
3. **Área de conteúdo** de y 260 a y 900, numa grade de 12 colunas entre x 96 e x 1824 (coluna de 122 px, vão de 24 px). Toda caixa começa e termina em borda de coluna. Fileiras de caixas têm a mesma largura, a mesma altura e o mesmo vão.
4. **Rodapé** à esquerda (x 96, y 1000), Consolas 20 pt, cinza: o contador "n / 28" (o número do slide no storyboard; passos de Morph repetem o número) e, depois de um ponto médio, a citação da afirmação do slide, como no TCC (ex.: "5 / 28 · Jesus et al. (2025); Wu, Xu e Zheng (2024)"). É a única exceção ao mínimo de 28 pt.
5. **Alinhamento à esquerda** por padrão. Centralizado só no número-herói, na tese e no fechamento.
6. **Sem moldura:** os cinco passos da abertura (1a a 1e), a capa e o slide final. Neles vale só a margem.

O pitch original fica fora do repositório, porque tem nomes que não podem ir a público: `C:\Users\willi\Downloads\GMS_Qualificacao_Pitch_v3.pptx`. Abra só para consulta, em modo leitura, e não copie para cá.

Funções da lib para isso (`gms_lib.ps1`):
- `Add-Moldura $s $rotulo $corCap $fraseGuia $contador $citacao`: cria `!!rotulo`, `!!frase` (trechos `{{assim}}` na cor do capítulo; `''` para número-herói) e `!!rodape`. Tamanhos em pt reais. Se a frase cabe numa linha, a caixa encolhe ao texto.
- `Get-Grade $col $span`: devolve `x`, `w`, `x2`, `y0`, `y1` da grade de 12 colunas.
- `Add-ReelCap $s $cx $cy $r $cap $frac`: carretel do capítulo `$cap` (1 a 8). Cada capítulo acende o seu segmento de 37° (passo de 45°); os dos capítulos anteriores ficam cheios na cor deles (`!!arcoLuz` = cap. 1 azul, `!!arcoLuz2` = cap. 2 ciano, `!!arcoLuz3` = cap. 3 índigo...). Mesmos nomes e mesmas caixas em todos os slides; só muda `$frac`. Nos capítulos 2 em diante, troque o `Reel-Small` por `Add-ReelCap $s 1800 985 62 N $frac` em todos os slides do capítulo. `cap 1` é idêntico a `Add-Reel`.
- `Export-GmsPdf $caminho`: PDF do deck aberto.
- `Test-GmsLayout [-Slides] [-Except @{indice=@(regex)}] [-ExceptAll] [-Families]`: confere margem de 96 px, vão de 32 px e a área do carretel (+40 px); imprime a tabela e devolve a contagem. Ignora `!!arco*`, `!!ponto*`, `!!fio*`, `!!ponta*`; `!!rotulo` e `!!rodape` ficam fora da regra de margem vertical (são da moldura) e o par `!!rotulo`/`!!frase` pode se tocar. `-Families` lista regex de objetos que se cobrem de propósito (ficha e seus números, placa e logo). Os scripts de capítulo rodam o teste antes de fechar.

A capa leva o logo da instituição (`assets/unisal_logo.png`) sobre placa branca no alto à direita, só nela.

## Como conferir uma transição sem assistir

Abra o `capN.mp4` num navegador e, pelo console, desenhe quadros do vídeo num canvas pequeno no meio de cada transição (um slide a cada 4,2 s: 3 s parado e 1,2 s de Morph). Conte os pixels da cor do fio antes, no meio e depois. Se o meio tiver muito mais pixels que os dois extremos, há mancha. No capítulo 1 a mancha dava cerca de 10 vezes o valor de repouso; corrigido, o meio fica entre os dois extremos.

## Sigilo

Nenhum nome de empresa ou de pessoa (fora o autor na capa) em slide, nota, nome de forma ou propriedade do arquivo. As propriedades de autor e empresa ficam vazias.

## Capítulo 3: mangueira, linha do tempo e o que se aprendeu

- **Mangueira 3D: o COM não aceita.** `Shapes.Add3DModel` (o nome COM correto é esse, não `AddModel3D`) falha com "o valor especificado está fora dos limites" nesta máquina, até com um .glb mínimo de um triângulo; o `mangueira.glb` e os `camadas/*.glb` ficam como ativos para quem inserir à mão (Inserir > Modelos 3D). O deck usa **imagens**: `assets/gerador/recortar_pecas.py` recorta as PNGs de reserva em `assets/pecas/pc_<camada>_{on,off}.png` (acesa e apagada, mesma tela por camada, brilho que some devagar na borda da vizinha). Cada camada é um objeto `!!mgTerminal`, `!!mgTubo`, `!!mgTranca`, `!!mgCobertura` com o mesmo nome em todos os slides: o Morph move a peça (montada no 11a, explodida no 11b–d, deitada na faixa do 12) e faz fade entre a imagem apagada e a acesa. Não gira (imagem parada).
- **Slide a mais ou a menos:** o storyboard dá 5 quadros (4+1+3+1+1 passos = 10 slides), logo o capítulo vai de 15 a 24 e o deck tem 24 slides.
- Elo 14→15: `tablet` do cap2 passou a se chamar `!!tablet` (senão o Morph não o liga ao tablet pequeno do 11a); `!!passagem`, `!!fioL1` e `!!pontaFio` também seguem.
- Linha do tempo (13a–c): `!!faixa3` (a faixa do meio do 12) vira o fio; `!!barraDev` (2 meses) e `!!barraPar` (7 meses) são retângulos sobre o fio e viram as duas barras do 14 e depois dois dos três cartões do 15. A câmera "voa" deslocando todos os objetos (`!!mk*`, `!!t*`, `!!d*`, fio, barras) entre os passos; o que está fora da tela fica fora do `Test-GmsLayout` (nomes passados em `-Except`). A tela tem 1920 px: texto que começa em x ≥ 1920 está fora; entre 1824 e 1920 ainda aparece. A ponta tracejada é `!!fioFut` (linha com `DashStyle`) + `!!pontaFio`. A posição dos cinco marcos de jun a out/2026 dentro do trecho é só ordem, sem mês.
- Medição do cap3 (mesmo método): 14→15 ciano 533→6 sem pico, índigo 0→155; 15→16, 16→17, 17→18 só acendem peças e rótulos; 18→19 as peças se juntam e entram nas faixas; 19→20 a faixa vira fio; 20→21 e 21→22 a câmera voa; 22→23 e 23→24 as barras viram cartões. Quadros do meio conferidos (peças, fio, barras): sem mancha. Picos de pixels claros nas transições 19→20 e 23→24 são texto em cross-fade (dois textos a 50% ao mesmo tempo), não mancha.

## Capítulo 4: núcleo, mosaico, tablet e plano B

- **Carretel vira núcleo.** Nos slides 25 a 30 `Add-ReelCap $s 960 580 140 4 frac` (mesmos nomes, caixa maior): o Morph escala o anel do canto até o centro; nos 31 em diante volta a (1800,985,r62). `frac` = k/8 nos 8 slides visíveis (25..32); os 3 ocultos ficam em 1,0.
- **Fios que nascem do anel.** `!!fio1..5` são linhas (`Add-FioLine`) criadas ANTES do carretel (ficam por baixo). Apagada, a linha é um toco de 2 px no ponto do anel que fica no centro de um segmento (ângulos -67,5+45k: o traço do anel, 18 a 31 px, cobre o toco de 6 px; no vão entre segmentos ele apareceria). Acesa, vai do mesmo ponto até o centro do nó. Escolha o ângulo do toco pelo segmento mais próximo da direção do nó.
- **Cartões do 24 viram discos.** `!!barraDev`, `!!barraPar`, `!!card3` (retângulos) encolhem a quadrados de 12 px sob o anel nos passos 16a–16f (menores que o traço, invisíveis) e somem em fade no 17.
- **Nós.** `!!no1..5` são `type 5` com ajuste 0,5 (círculo): apagado 16 px cinza, aceso 36 px violeta. No 17 viram os retângulos dos cartões (ajuste 0,04) e no 18 `!!no1` cresce e vira o tablet (944×590, ajuste 0,05). `!!nt1..3` (tracejados) nascem no 16f por fade; os fios `fioT*` e os itens de texto não têm `!!` e entram/saem por fade. Os fios `fioT` devem sair de ângulos para baixo (67,5 e 112,5): vindos do lado direito cruzam os itens da Logística.
- **Medidas do texto.** Bahnschrift Light a 56 px dá ~23 caracteres em 614 px; por isso os itens são curtos. Título 64 px + 2 linhas de 56 px com `SpaceWithin=0,9` fecham em ~190 px por bloco; passo vertical de 232 px entre blocos (topos 260, 492, 724) para manter 32 px de vão. Título e itens do mesmo bloco são objetos separados e entram em `-Families` (`^(!!pt1|it1)$`...).
- **Mosaico 4×2.** Cartão 408×255 (proporção 800×500 das imagens), vão 32, x = 96 + 440·col, y = 305 / 592. Grade plana (sem perspectiva, para não quebrar o Morph). Imagens `img_*` (sem `!!`) por cima dos quadros e em `-Families`.
- **Pulso do ponto vermelho.** `Timeline.MainSequence.AddEffect($anel,59,0,2)` (Grow/Shrink, com o anterior) com `Timing.RepeatCount=60` e `Duration=1,2` grava `repeatCount` no XML e sobrevive ao `Save-GmsDeck`. O efeito fica no anel (`pulso_anel`, sem `!!`).
- **Hiperlink para o slide oculto.** `$shape.ActionSettings.Item(1).Action=7` e `.Hyperlink.SubAddress="<SlideID>,<SlideIndex>,Plano B"` (é preciso criar o slide 33 antes). No XML sai `hlinkClick action="ppaction://hlinksldjump"` e a relação aponta para `slide33.xml`. O SlideID não muda ao salvar/reabrir. O ponto `ligaPlanoB` (24 px, canto inferior esquerdo, x 96, y 920) cumpre margem e vão.
- **Ocultos.** `SlideShowTransition.Hidden=-1` nos 33 a 35 (`show="0"` no XML); o Morph e o avanço por clique continuam. O `!!no1` do 18 é a mesma moldura nos 33 a 35 (944×590 ou 944×531 para a tela 16:9) e `!!passo1..3` (os textos do 18) ficam só o do passo corrente, em violeta claro. O vídeo de revisão desoculta os três na cópia temporária para mostrar as transições.
- **Arquivos .ps1 com acento** precisam de BOM UTF-8 (o PowerShell 5.1 lê como ANSI sem ele e o texto sai quebrado).
- **Preenchimento que muda no Morph aparece como bloco cheio:** mantenha o preenchimento igual nos dois slides e mude só o contorno. Mas objeto minúsculo com contorno grande não vai ao Morph; deixe-o desaparecer em fade e crie o destino com outro nome. Por isso, no cap4, os cartões do 24 (`!!barraDev`, `!!barraPar`, `!!card3`) não têm destino no 25 e somem em fade; os nós dos slides 25 a 30 se chamam `!!nd1..5` (círculos), e no 31 os cinco cartões acesos são `!!no1..5` novos (só o `!!no1` casa com o do 32). Os títulos dos cartões tracejados do 31 são texto do PowerPoint (`tt1..3`), não imagem. O pulso do 32 usa `repeatCount="indefinite"` (gravado no XML pelo cap4 depois do `Save-GmsDeck`); com número fixo o CreateVideo esticava o slide a 72 s.

### Medição fina das passagens (capítulo 4)
Passo de 0,1 s, canvas 160×90, contando pixels "com cor" (a cor do capítulo, B>180, R 100–200, G 50–140) e pixels claros (R+G+B>450). Janelas de transição = diferença entre quadros acima de 4 (em milhares, soma de |ΔRGB|). Critério: no meio da passagem, a contagem não passa de 1,15 × a maior das duas pontas, mais 60. Com passo de 0,2 s a primeira medição deixou passar dois blocos cheios; use 0,1 s e confira a passagem de entrada do capítulo (24→25). Medição final do cap4 (antes/pico/depois, cor): 24→25 349/194/154; 30→31 213/289/287; 31→32 308/258/135; 32→33 135/441/437; 33→34 436/439/191; 34→35 191/247/185. Nenhuma excede o critério.

## Capítulo 5: resultados (antes × depois, dossiê, 8,3×, barras e o anel do MESA-11)

- **Quadro 21 em dois passos (21a e 21b).** A barra de 74% (`!!barra1`) passa ao quadro 22 pelo Morph, e objeto de Morph não pode ter animação de clique. Então o "depois, uma barra" virou um passo de Morph (um clique = uma passagem), e o capítulo tem 6 slides, com o arco âmbar de 1/6 a 6/6. O contador do rodapé repete "21 / 28" nos dois.
- **Morph casa também objetos SEM `!!` quando se parecem.** O retângulo `tela_tab` (a tela do tablet do 36, retângulo cheio sem nome) foi casado com a faixa `faixa_est` do 37 e apareceu como faixa cheia no meio da passagem (quadro 7,8 s do vídeo); o contador de pixels não pega isso. Solução: objetos sem nome que não devem se encontrar usam tipos de forma diferentes (a tela e as linhas do tablet são retângulos arredondados; a faixa é retângulo reto). A faixa também ganhou preenchimento na cor do fundo e o `pulso_anel` preenchimento transparente, por precaução: forma só com contorno herda o preenchimento do estilo durante o Morph. Veja sempre os quadros do meio, não só os números.
- **Cores com sentido.** Âmbar = o que o sistema mediu (8,3×, 74%, 96,4%, até 6%, o anel). Os três números do dossiê (36×, 87,5%, 97%) ficam em cinza claro, sem âmbar, com a faixa fixa sépia "estimativas da equipe, sem cronometragem" (só no 37; no 38 o 36× vira 8,3× e a faixa sai).
- **Entradas do capítulo.** O tablet `!!no1` do 32 e do 35 (mesma caixa, 944×590) encolhe à direita do 36, contorno violeta → âmbar; a ficha (`Add-Ficha`, a mesma da abertura, 240 px, sem textos) entra por fade, porque nenhum slide entre o 5 e o 35 tem `!!ficha`. As três linhas do 36 (`!!lin1..3`) viram os três cartões do 37, e `!!lab1..3` viram as legendas dos cartões. O `!!num1` ("36×") vira o "8,3×" do 38 (tamanho 190 → 400 px, cinza → âmbar) e depois desce e encolhe no 39.
- **Barras (39 → 40).** `!!trilho1` + `!!barra1` (retângulos retos, mesmo preenchimento) ficam no mesmo lugar e só crescem (74% → 96,4%); `!!pct1` e `!!desc1` trocam o texto. A segunda barra (`trilho2`, `barra2`, `pct2`, `desc2`) nasce por fade, sem `!!`. A barra de "até 6%" mostra a diferença, não a cobertura; o texto diz "de diferença".
- **Anel de 11 arcos (40 → 41).** `!!arcoM1..11`: 24 graus de arco em fatias de 32,7, traço de 30 px, nenhum arco cruza 0/360 (regra do ângulo monotônico) e as pontas redondas não se tocam (vão de 8,7 graus > traço). No 40 são tocos de 1 grau na COR DO FUNDO, por baixo das barras; no 41 crescem para âmbar (6 acesas), âmbar (a que pulsa), âmbar a 55% (2 parciais) e cinza (2 fora do escopo). Arco de contorno que muda de cor ao crescer não gera bloco. As barras do 40 somem em fade (sem `!!` no destino), como manda a lição do capítulo 4. O pulso é um anel `pulso_anel` (sem `!!`, Grow/Shrink com repeatCount "indefinite" gravado no XML depois do `Save-GmsDeck`, como no 32).
- **Rodapés.** 19: seções 4.5 e 4.6; 20: seção 4.5 e Quadro 6; 21: seções 4.3 e 4.6; 22: "Resumo; seção 4.4 e Tabela 2" (96,4% e até 6% só aparecem no Resumo do TCC; o corpo diz "próximo do medido"); 23: seção 4.7, Quadro 7.
- **Armadilha do PowerShell.** Aspas curvas (“ ”) dentro de string com aspas duplas fecham a string. Use `[char]0x201C` e `[char]0x201D` (`$LQ`, `$RQ` no cap5).

### Medição fina das passagens (capítulo 5)
Mesmo método do capítulo 4 (passo de 0,1 s, 160×90). Pixels "com cor" = âmbar (R>180, G 90–200, B<90, R−B>120); claros = R+G+B>450; janela de transição = diferença entre quadros acima de 4. Antes/pico/depois (claros | cor); o limite é 1,15 × a maior ponta + 60:
- 35 → 36: 202/739/739 | 0/175/175 (limite 910 | 261).
- 32 → 36 (vídeo `cap5_entrada32.mp4`, sem os ocultos): 138/742/742 | 0/175/175 (913 | 261).
- 36 → 37: 747/748/665 | 178/177/66 (919 | 265).
- 37 → 38: 671/444/67 | 66/486/486 (832 | 619).
- 38 → 39: 66/311/309 | 486/547/546 (415 | 688).
- 39 → 40: 310/372/372 | 546/681/681 (488 | 843).
- 40 → 41: 378/295/279 | 682/668/319 (495 | 844).
Nenhuma passa do limite. Os quadros do meio das sete passagens foram vistos (mosaico de quadros num canvas `position:fixed` de 800 px de largura no Browser pane, mesmo escondido; `window.innerWidth` vem 0, então passe a largura): sem bloco cheio, sem mancha; cross-fade de texto (frase-guia, rodapé, 36× → 8,3×) é o esperado. As pequenas janelas de 0,2 s depois de cada transição são o pulso do 32 e do 41.
