// Sistema visual do canal (Bit): monocromático + um único destaque (o vermelho do ponto), Geist, cantos retos, grão analógico.
// Regras: nada de degradê, nada de cartão arredondado, nada de cinza-azulado/pastel; o destaque é usado só onde importa.
window.BRAND = {
  ink: '#0C0C0D',      // off-black (fundo escuro e texto no claro)
  ink2: '#18181A',     // segundo tom escuro
  paper: '#EEEDE8',    // off-white (fundo claro e texto no escuro)
  mute: '#8C8B86',     // texto secundário
  accent: '#FF3B1F',   // ÚNICO destaque: o vermelho do ponto
  font: 'Geist', mono: 'Geist Mono',
  fontsCSS: 'https://fonts.googleapis.com/css2?family=Geist:wght@500;700;800;900&family=Geist+Mono:wght@500;700&display=block',
};
// grão de filme: textura gerada uma vez e aplicada em overlay por cima de cada quadro
window.grain = (() => {
  let tile;
  return (ctx, W, H, alpha = 0.09) => {
    if (!tile) {
      tile = document.createElement('canvas'); tile.width = tile.height = 300;
      const g = tile.getContext('2d'), d = g.createImageData(300, 300);
      for (let i = 0; i < d.data.length; i += 4) { const v = 128 + (Math.random() - 0.5) * 255; d.data[i] = d.data[i + 1] = d.data[i + 2] = v; d.data[i + 3] = 255; }
      g.putImageData(d, 0, 0);
    }
    ctx.save(); ctx.globalAlpha = alpha; ctx.globalCompositeOperation = 'overlay'; ctx.fillStyle = ctx.createPattern(tile, 'repeat'); ctx.fillRect(0, 0, W, H); ctx.restore();
  };
})();
window.loadBrandFonts = () => Promise.all([500, 700, 800, 900].map(w => document.fonts.load(`${w} 100px "Geist"`, 'ÁÉÍçãõ…×'))).then(() => document.fonts.load('700 40px "Geist Mono"'));
