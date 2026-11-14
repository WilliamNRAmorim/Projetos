# Como o GMS_Defesa.pptx é montado

O deck é gerado por script, com o PowerPoint dirigido pelo COM do Windows (PowerShell 5.1). Nada é editado à mão: mudou o slide, muda o script e roda de novo.

- `gms_lib.ps1`: funções reutilizáveis (novo deck, carretel com progresso, fio, texto, notas, salvar com os ajustes de XML, exportar).
- `cap1.ps1`: os 10 slides do capítulo 1. `-SemVideo` pula o vídeo de revisão.
- As notas do apresentador saem de `../roteiro.md` na hora da montagem.
- Saídas: `../GMS_Defesa.pptx`, `../previa/capN/slide_NN.png` (1920×1080) e `../previa/capN/capN.mp4` (vídeo de revisão das transições, 3 s por slide; não entra no deck).

## Regras aprendidas no capítulo 1 (valem para todos os capítulos)

1. **Morph não entra pelo COM.** `EntryEffect = 3954` dá erro. O script salva, edita o XML de cada slide (`p159:morph option="byObject"`, 1,2 s) e reabre. Avanço só por clique.
2. **Continuidade é pelo nome.** O objeto que passa de um slide ao seguinte tem o mesmo nome nos dois, começando com `!!`.
3. **Nunca use forma livre em objeto que participa do Morph.** O PowerPoint interpola a forma livre como contorno fechado e preenchido: aparece uma mancha da cor da linha no meio da transição.
4. **Arco que cresce: a mesma caixa nos dois slides, e só o ângulo muda.** Um arco achatado (caixa com 1 pt de altura) é uma barra sólida; o Morph estica essa imagem até a caixa final e aparece um bloco cheio. O carretel e o fio seguem esta regra. O estado inicial é um toco de 1 grau escondido sob a linha ou sob o ponto.
5. **Ângulo monotônico.** O Morph interpola o valor do ajuste em linha reta. Para fechar em 360 graus use 21540000, não 0, senão o arco dá a volta pelo lado errado.
6. **Ponta redonda e sem preenchimento vão no XML.** O COM não grava `cap="rnd"` nem `<a:noFill/>` em arco; `Save-GmsDeck` faz isso para todo `!!arco*` e `!!fio*`.
7. **Animação de entrada só em objeto sem `!!`.** Entrada em objeto que participa do Morph briga com a transição.
8. **Os PNGs não mostram defeito de transição.** O quadro parado sai certo mesmo com mancha no meio do Morph. Confira sempre o vídeo de revisão.

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
