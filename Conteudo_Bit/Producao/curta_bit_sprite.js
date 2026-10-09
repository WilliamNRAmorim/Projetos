// Sprite do Bit sentado do curta pixel art (curta_bit_pt.html). ÚNICO ponto de troca do Bit.
// Atual: bit_sentado_nanobanana_v2.jpeg (Nano Banana/Gemini, aprovado pelo William em 08/10/2026), usado sem redesenho:
// o fundo branco é recortado por preenchimento a partir das bordas (o branco dos olhos fica, porque o contorno o fecha),
// a imagem é reduzida e ampliada sem suavização (pixel `pixel` px no vídeo) para casar com a cena em pixel art.
// Para trocar: aponte `src` para outra imagem (PNG transparente ou fundo branco liso) e ajuste `assentoY`, `olhos` e `altura`.
window.CURTA_BIT = {
  src: '/Marca/bit/bit_sentado_nanobanana_v2.jpeg',
  espelhar: false,          // a pose olha para a esquerda (para o humano, que fica à esquerda no banco)
  altura: 150,             // altura no vídeo, da bolinha da antena ao pé (px de 1080x1920)
  pixel: 3,                 // tamanho do pixel do Bit no vídeo (a cena usa 5; 3 preserva olhos e faixa)
  limiarBranco: 236,        // canal mínimo para contar como fundo branco
  assentoY: 742,            // linha da imagem original que encosta no assento do banco
  // piscada: pálpebra desenhada por cima de cada olho (coordenadas da imagem original): elipse cx, cy, rx, ry
  olhos: [[405, 397, 50, 62], [553, 427, 62, 64]],
  corPalpebra: '#E9502C', corLinha: '#5A1A10',
};
