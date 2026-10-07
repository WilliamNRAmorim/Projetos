// Arte do Bit (Gemini, fundo branco) pronta pra compor: recorte, contorno escuro e o "uniforme" de cada projeto.
// Uniformes: GMS = anel de 8 cores girando em volta da bolinha da antena; Will Station = boné com W (vem do Gemini);
// Bastidores = capacete (vem do Gemini); curiosidades = Bit puro.
window.BitArt = (() => {
  const RING = ['#2F6BFF', '#22C7E8', '#4B3FD1', '#9B4DFF', '#FFB020', '#FF3B1F', '#FF7A1A', '#22C55E']; // sentido horário a partir do topo
  function cutout(img) { // tira o fundo branco e escurece a franja do contorno; devolve o canvas já aparado no personagem
    const W = img.naturalWidth, H = img.naturalHeight, c = document.createElement('canvas'); c.width = W; c.height = H; const x = c.getContext('2d'); x.drawImage(img, 0, 0);
    const id = x.getImageData(0, 0, W, H), d = id.data, seen = new Uint8Array(W * H), st = [], white = i => d[i] > 228 && d[i + 1] > 228 && d[i + 2] > 228;
    for (let i = 0; i < W; i++) st.push(i, (H - 1) * W + i); for (let j = 0; j < H; j++) st.push(j * W, j * W + W - 1);
    while (st.length) { const p = st.pop(); if (seen[p]) continue; const i = p * 4; if (!white(i)) continue; seen[p] = 1; d[i + 3] = 0; const px = p % W, py = (p / W) | 0; if (px) st.push(p - 1); if (px < W - 1) st.push(p + 1); if (py) st.push(p - W); if (py < H - 1) st.push(p + W); }
    for (let pass = 0; pass < 3; pass++) { const kill = [];
      for (let p = 0; p < W * H; p++) { const i = p * 4; if (!d[i + 3]) continue; const px = p % W, py = (p / W) | 0; const edge = (px && seen[p - 1]) || (px < W - 1 && seen[p + 1]) || (py && seen[p - W]) || (py < H - 1 && seen[p + W]); if (edge && (d[i] + d[i + 1] + d[i + 2]) / 3 > 150) kill.push(p); }
      for (const p of kill) { d[p * 4 + 3] = 0; seen[p] = 1; } }
    let x0 = W, y0 = H, x1 = 0, y1 = 0;
    for (let p = 0; p < W * H; p++) { const i = p * 4; if (!d[i + 3]) continue; const px = p % W, py = (p / W) | 0; if ((px && seen[p - 1]) || (px < W - 1 && seen[p + 1]) || (py && seen[p - W]) || (py < H - 1 && seen[p + W])) { const l = (d[i] + d[i + 1] + d[i + 2]) / 3; d[i + 3] = Math.max(0, Math.min(255, (255 - l) * 3)); d[i] = 42; d[i + 1] = 15; d[i + 2] = 10; } if (d[i + 3] > 20) { x0 = Math.min(x0, px); x1 = Math.max(x1, px); y0 = Math.min(y0, py); y1 = Math.max(y1, py); } }
    x.putImageData(id, 0, 0);
    const t = document.createElement('canvas'); t.width = x1 - x0 + 1; t.height = y1 - y0 + 1; t.getContext('2d').drawImage(c, -x0, -y0);
    t.ball = findBall(t); t.sil = silhouette(t); return t;
  }
  function findBall(t) { // a bolinha vermelha da antena: pixels bem vermelhos no topo do personagem
    const h = Math.round(t.height * 0.22), d = t.getContext('2d').getImageData(0, 0, t.width, h).data; let x0 = 1e9, y0 = 1e9, x1 = -1, y1 = -1;
    for (let y = 0; y < h; y++) for (let x = 0; x < t.width; x++) { const i = (y * t.width + x) * 4; if (d[i + 3] > 200 && d[i] > 170 && d[i + 1] < 110 && d[i + 2] < 110) { x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y); } }
    return x1 < 0 ? null : { x: (x0 + x1) / 2, y: (y0 + y1) / 2, r: Math.max(x1 - x0, y1 - y0) / 2 };
  }
  function silhouette(t) { const s = document.createElement('canvas'); s.width = t.width; s.height = t.height; const g = s.getContext('2d'); g.drawImage(t, 0, 0); g.globalCompositeOperation = 'source-in'; g.fillStyle = '#2A0F0A'; g.fillRect(0, 0, s.width, s.height); return s; }
  function ring(g, cx, cy, r, w, rot) { // 8 segmentos com respiro entre eles, contorno escuro igual ao traço do personagem
    const gap = 0.16, seg = Math.PI * 2 / 8;
    RING.forEach((col, k) => { const a0 = -Math.PI / 2 + rot + k * seg + gap / 2, a1 = a0 + seg - gap;
      g.beginPath(); g.arc(cx, cy, r, a0, a1); g.lineCap = 'round'; g.lineWidth = w + 6; g.strokeStyle = '#2A0F0A'; g.stroke(); g.lineWidth = w; g.strokeStyle = col; g.stroke(); });
  }
  // desenha o personagem com altura h, centrado em cx, pé em bottom; opts.ring = rotação do anel do GMS (rad) ou undefined
  function draw(g, art, cx, bottom, h, opts = {}) {
    const s = h / art.height, w = art.width * s, x = cx - w / 2, y = bottom - h;
    g.imageSmoothingQuality = 'high'; for (let a = 0; a < 16; a++) g.drawImage(art.sil, x + Math.cos(a / 16 * 6.283) * 3, y + Math.sin(a / 16 * 6.283) * 3, w, h);
    g.drawImage(art, x, y, w, h);
    if (opts.ring !== undefined && art.ball) { const b = art.ball; ring(g, x + b.x * s, y + b.y * s, b.r * s * 2.1, Math.max(8, b.r * s * 0.42), opts.ring); }
  }
  const load = src => { const i = new Image(); i.src = src; return i.decode().then(() => cutout(i)); };
  return { cutout, draw, load, RING };
})();
