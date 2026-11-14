# Mangueira 3D (slide 11)

Modelo de autoria própria, todo gerado por código (numpy + Pillow; nada baixado, nenhum modelo de terceiros).

## Reproduzir
```
python gerar_mangueira.py     # assets/mangueira.glb e assets/camadas/mangueira_<camada>.glb
python renderizar.py          # as 6 PNGs em assets/ (rasterizador próprio, ~1 min)
node validar_glb.js ../mangueira.glb
```

## O modelo
- **123.008 triângulos** (terminal 107.648; tubo, trança e cobertura 5.120 cada). Cerca de 5,1 MB.
- 4 nós e 4 materiais com o mesmo nome: `terminal`, `tubo`, `tranca`, `cobertura`, filhos de `mangueira`. Os nós não têm transformação: todos dividem a mesma origem e o mesmo eixo.
- Eixo da mangueira = **X**; Y para cima. A caixa está centrada na origem (X de -2,85 a 2,85). O eixo passa pela origem.
- A trança é textura (cor + normal map, ladrilho de 16 portadoras por sentido a 54,7°), não geometria. O terminal é metal liso; o tubo e a cobertura são borracha (a cobertura tem uma linha longitudinal clara, sem texto).
- `camadas/` tem uma camada por arquivo, no mesmo referencial.

## Girar e explodir no PowerPoint
- Inserir > Modelos 3D > Este dispositivo, ou `Shapes.Add3DModel(caminho)`. Para girar, use a alça do centro ou, em VBA, `shape.Model3D.RotationY` (gira em torno do eixo vertical) e `RotationX` (inclina). A mangueira entra deitada (eixo X na horizontal).
- O PowerPoint trata um .glb como uma peça só: dentro de uma forma 3D as camadas não se separam. Para a vista explodida, insira os 4 arquivos de `camadas/` com a mesma rotação e o mesmo tamanho e afaste cada um ao longo da horizontal. Como cada camada é simétrica em torno do eixo, elas continuam alinhadas mesmo depois de o PowerPoint centrar cada uma na sua caixa. O tamanho tem de ser igual nas quatro (o PowerPoint ajusta cada modelo à sua caixa, por isso confira a escala).

## PNGs de reserva
Câmera fixa, 1920x1080, **fundo transparente**. A ordem da esquerda para a direita é terminal, tubo, trança e cobertura, com 0,55 de folga. A camada em destaque fica com borda e brilho índigo `#6366F1`; as outras ficam em `#10151C` com borda `#232B36`. `mangueira_inteira.png` usa a mesma câmera, com a mangueira montada no centro.
