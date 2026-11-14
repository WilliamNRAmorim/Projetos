# Como o GMS_Defesa.pptx é montado

O deck é gerado por script, com o PowerPoint dirigido pelo COM do Windows (PowerShell 5.1). Nada é editado à mão: mudou o slide, muda o script e roda de novo.

- `gms_lib.ps1`: funções reutilizáveis (novo deck, carretel com progresso, fio, texto, notas, salvar com os ajustes de XML, exportar).
- `cap1.ps1`: os 10 slides do capítulo 1 (gera o deck do zero). `-SemVideo` pula o vídeo de revisão.
- `cap2.ps1`: os slides 11 a 14 (capítulo 2, quadros 7 a 10). Rode DEPOIS do cap1: não regera o cap1, abre `GMS_Defesa.pptx`, apaga o que houver além do slide 10 (pode rodar de novo à vontade), acrescenta os 4 slides e salva. O arquivo não pode estar aberto no PowerPoint (o script avisa e para; nunca fecha o PowerPoint do usuário).
- `cap3.ps1`: os slides 15 a 24 (capítulo 3, quadros 11 a 15: 11a–11d, 12, 13a–13c, 14, 15 = 10 slides; o deck fecha em 24, não 25). Rode DEPOIS do cap2 (ordem: cap1, cap2, cap3; cada um abre o deck e acrescenta). Idempotente como o cap2. O `cap3.mp4` começa no slide 14; `cap3.pdf` tem o deck inteiro (24 slides).
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
