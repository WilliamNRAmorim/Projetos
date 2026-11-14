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

## Como conferir uma transição sem assistir

Abra o `capN.mp4` num navegador e, pelo console, desenhe quadros do vídeo num canvas pequeno no meio de cada transição (um slide a cada 4,2 s: 3 s parado e 1,2 s de Morph). Conte os pixels da cor do fio antes, no meio e depois. Se o meio tiver muito mais pixels que os dois extremos, há mancha. No capítulo 1 a mancha dava cerca de 10 vezes o valor de repouso; corrigido, o meio fica entre os dois extremos.

## Sigilo

Nenhum nome de empresa ou de pessoa (fora o autor na capa) em slide, nota, nome de forma ou propriedade do arquivo. As propriedades de autor e empresa ficam vazias.
