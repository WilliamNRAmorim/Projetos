// Boneco 2D articulado do Bit: corpo e antena vêm da arte gerada (Marca/bit/bit_corpo.jpg);
// olhos, boca, braços, pernas e o anel do GMS são desenhados por cima, no mesmo traço, e animados por tempo.
// Uso: await BitRig.load('/Marca/bit/bit_corpo.jpg'); BitRig.draw(ctx, t, {x, y, s, pose, face, ring}).
(function () {
  const GMS = ['#3B82F6', '#06B6D4', '#6366F1', '#8B5CF6', '#F59E0B', '#EF4444', '#F97316', '#10B981'];
  const R = { body: null, antenna: null, col: {}, box: null };
  const PIVOT = { x: 697, y: 238 }, BALL = { x: 642, y: 120 };   // base da antena e centro da bolinha (coords da imagem)
  // ---------- recorte: tira o fundo branco ligado às bordas, com borda suave ----------
  function cutout(img) {
    const W = img.naturalWidth, H = img.naturalHeight, c = document.createElement('canvas'); c.width = W; c.height = H;
    const x = c.getContext('2d'); x.drawImage(img, 0, 0); const id = x.getImageData(0, 0, W, H), d = id.data;
    const white = i => d[i] > 225 && d[i + 1] > 225 && d[i + 2] > 225, seen = new Uint8Array(W * H), st = [];
    for (let i = 0; i < W; i++) { st.push(i, (H - 1) * W + i); } for (let j = 0; j < H; j++) { st.push(j * W, j * W + W - 1); }
    while (st.length) { const p = st.pop(); if (seen[p]) continue; const i = p * 4; if (!white(i)) continue; seen[p] = 1; d[i + 3] = 0; const px = p % W, py = (p / W) | 0; if (px > 0) st.push(p - 1); if (px < W - 1) st.push(p + 1); if (py > 0) st.push(p - W); if (py < H - 1) st.push(p + W); }
    for (let p = 0; p < W * H; p++) { const i = p * 4; if (!d[i + 3]) continue; const px = p % W, py = (p / W) | 0, near = (px > 0 && seen[p - 1]) || (px < W - 1 && seen[p + 1]) || (py > 0 && seen[p - W]) || (py < H - 1 && seen[p + W]); if (near) { const lum = (d[i] + d[i + 1] + d[i + 2]) / 3; d[i + 3] = Math.max(0, Math.min(255, (255 - lum) * 3)); } }
    x.putImageData(id, 0, 0); return [c, x];
  }
  function split(c) { // antena = tudo acima do topo do corpo; corpo = o resto
    const W = c.width, H = c.height, a = document.createElement('canvas'), b = document.createElement('canvas'); a.width = b.width = W; a.height = b.height = H;
    a.getContext('2d').drawImage(c, 0, 0, W, PIVOT.y - 2, 0, 0, W, PIVOT.y - 2);
    b.getContext('2d').drawImage(c, 0, PIVOT.y - 2, W, H - PIVOT.y + 2, 0, PIVOT.y - 2, W, H - PIVOT.y + 2); return [a, b];
  }
  R.load = async (src) => {
    const img = new Image(); img.src = src; await img.decode();
    const [c, x] = cutout(img); const px = (X, Y) => { const p = x.getImageData(X, Y, 1, 1).data; return `rgb(${p[0]},${p[1]},${p[2]})`; };
    R.col = { body: px(740, 420), shade: px(560, 420), line: px(536, 430) };
    [R.antenna, R.body] = split(c); return R;
  };
  // ---------- peças desenhadas (mesmo traço: contorno escuro + cor do corpo) ----------
  const OUT = 7;
  function tube(ctx, pts, w) { for (const [col, lw] of [[R.col.line, w + OUT * 2], [R.col.body, w]]) { ctx.strokeStyle = col; ctx.lineWidth = lw; ctx.lineCap = 'round'; ctx.lineJoin = 'round'; ctx.beginPath(); ctx.moveTo(...pts[0]); if (pts.length === 3) ctx.quadraticCurveTo(...pts[1], ...pts[2]); else ctx.lineTo(...pts[1]); ctx.stroke(); } }
  function fill(ctx, col) { ctx.fillStyle = col; ctx.fill(); ctx.strokeStyle = R.col.line; ctx.lineWidth = OUT; ctx.lineJoin = 'round'; ctx.stroke(); }
  function hand(ctx, x, y, ang, open) { // luva em forma de mitene: palma + polegar; aberta = 4 dedos, nunca um dedo isolado
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang);
    if (open) for (const dx of [-21, -7, 7, 21]) { ctx.beginPath(); ctx.ellipse(dx, -30, 9, 16, 0, 0, 7); fill(ctx, R.col.body); }
    ctx.beginPath(); ctx.ellipse(0, 0, 30, 26, 0, 0, 7); fill(ctx, R.col.body);
    ctx.beginPath(); ctx.ellipse(-27, 4, 11, 15, -0.6, 0, 7); fill(ctx, R.col.body);
    ctx.restore();
  }
  // rosto no estilo da folha v1: olhos grandes e juntos, sobrancelhas, bocas variadas, bochechas
  const EX = { // expressões da folha v1
    acenando: { look: [4, -2], mouth: 'aberta', blush: true },
    feliz: { closed: true, mouth: 'grande', blush: true },
    pensando: { look: [9, -13], browR: 'alta', browL: 'reta', mouth: 'lado' },
    surpreso: { look: [0, 0], wide: true, browR: 'alta', browL: 'alta', mouth: 'o' },
    comemorando: { look: [0, 3], mouth: 'grande', blush: true },
    confuso: { look: [11, 4], lid: 0.42, browL: 'baixa', browR: 'alta', mouth: 'onda' },
    neutro: { look: [0, 0], mouth: 'reta' }, // reel30: repouso, boca fechada (linha), sem bochecha; olhar e pálpebra vêm de face.look/face.lid
  };
  const EYE = [[660, 362], [750, 362]];
  function eye(ctx, cx, cy, e, look, blink) {
    if (e.closed) { ctx.strokeStyle = R.col.line; ctx.lineWidth = 10; ctx.lineCap = 'round'; ctx.beginPath(); ctx.arc(cx, cy + 16, 28, Math.PI * 1.15, Math.PI * 1.85); ctx.stroke(); return; }
    const rx = e.wide ? 43 : 40, ry = (e.wide ? 50 : 46) * (1 - 0.94 * blink);
    ctx.beginPath(); ctx.ellipse(cx, cy, rx, Math.max(ry, 3), 0, 0, 7); fill(ctx, '#FFFFFF');
    if (blink > 0.6) return;
    ctx.save(); ctx.beginPath(); ctx.ellipse(cx, cy, rx - 3, Math.max(ry - 3, 1), 0, 0, 7); ctx.clip();
    const pr = e.wide ? [13, 16] : [22, 28], px = cx + look[0], py = cy + look[1] + 3;
    ctx.fillStyle = '#121214'; ctx.beginPath(); ctx.ellipse(px, py, pr[0], pr[1], 0, 0, 7); ctx.fill();
    ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(px - pr[0] * 0.35, py - pr[1] * 0.4, pr[0] * 0.38, 0, 7); ctx.fill(); ctx.beginPath(); ctx.arc(px + pr[0] * 0.3, py + pr[1] * 0.25, pr[0] * 0.16, 0, 7); ctx.fill();
    if (e.lid) { const ly = cy - ry + 2 * ry * e.lid; ctx.fillStyle = R.col.body; ctx.fillRect(cx - rx, cy - ry - 4, rx * 2, ly - (cy - ry) + 4); ctx.restore(); ctx.save(); ctx.beginPath(); ctx.ellipse(cx, cy, rx, ry, 0, 0, 7); ctx.clip(); ctx.strokeStyle = R.col.line; ctx.lineWidth = 7; ctx.beginPath(); ctx.moveTo(cx - rx, ly); ctx.lineTo(cx + rx, ly - 3); ctx.stroke(); }
    ctx.restore(); ctx.beginPath(); ctx.ellipse(cx, cy, rx, ry, 0, 0, 7); ctx.strokeStyle = R.col.line; ctx.lineWidth = OUT; ctx.stroke();
  }
  function brow(ctx, cx, cy, kind, side) {
    if (!kind) return; ctx.strokeStyle = R.col.line; ctx.lineWidth = 9; ctx.lineCap = 'round'; ctx.beginPath();
    if (kind === 'alta') { ctx.moveTo(cx - 26, cy - 66); ctx.quadraticCurveTo(cx, cy - 84, cx + 26, cy - 68); }
    else if (kind === 'baixa') { ctx.moveTo(cx - 26 * side, cy - 64); ctx.lineTo(cx + 24 * side, cy - 54); }
    else { ctx.moveTo(cx - 24, cy - 62); ctx.lineTo(cx + 24, cy - 62); }
    ctx.stroke();
  }
  function mouth(ctx, kind) {
    const mx = 705, my = 448; ctx.strokeStyle = R.col.line; ctx.lineWidth = 7; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    const open = (w, h) => { ctx.beginPath(); ctx.moveTo(mx - w, my - 4); ctx.quadraticCurveTo(mx, my - 10, mx + w, my - 4); ctx.quadraticCurveTo(mx + w * 0.8, my + h, mx, my + h); ctx.quadraticCurveTo(mx - w * 0.8, my + h, mx - w, my - 4); ctx.closePath(); fill(ctx, '#7A1C14'); ctx.save(); ctx.clip(); ctx.fillStyle = '#FF8A8A'; ctx.beginPath(); ctx.ellipse(mx, my + h - 4, w * 0.62, h * 0.38, 0, 0, 7); ctx.fill(); ctx.restore(); };
    if (kind === 'aberta') open(26, 30);
    else if (kind === 'grande') open(42, 52);
    else if (kind === 'o') { ctx.beginPath(); ctx.ellipse(mx, my + 14, 18, 26, 0, 0, 7); fill(ctx, '#7A1C14'); }
    else if (kind === 'lado') { ctx.beginPath(); ctx.moveTo(mx - 8, my + 8); ctx.quadraticCurveTo(mx + 12, my + 2, mx + 28, my + 8); ctx.stroke(); }
    else if (kind === 'onda') { ctx.beginPath(); ctx.moveTo(mx - 30, my + 10); for (let i = 1; i <= 6; i++) ctx.quadraticCurveTo(mx - 30 + i * 10 - 5, my + (i % 2 ? 0 : 20), mx - 30 + i * 10, my + 10); ctx.stroke(); }
    else { ctx.beginPath(); ctx.moveTo(mx - 30, my); ctx.quadraticCurveTo(mx, my + 28, mx + 30, my); ctx.stroke(); }
  }
  function face(ctx, t, f) {
    const e0 = EX[f.expr] || EX.acenando, e = f.lid != null ? { ...e0, lid: f.lid } : e0, look = f.look || [e.look ? e.look[0] + Math.sin(t * 1.3) * 3 : 0, e.look ? e.look[1] : 0], blink = f.blink || 0;
    if (e.blush) { ctx.fillStyle = 'rgba(255,140,140,.5)'; for (const x of [612, 798]) { ctx.beginPath(); ctx.ellipse(x, 425, 24, 13, 0, 0, 7); ctx.fill(); } }
    EYE.forEach(([cx, cy], i) => { eye(ctx, cx, cy, e, look, blink); brow(ctx, cx, cy, i ? e.browR : e.browL, i ? 1 : -1); });
    mouth(ctx, e.mouth);
  }
  R.EXPRS = Object.keys(EX);
  function gmsRing(ctx, t, on) { // o logo do GMS se forma em volta da bolinha da antena
    if (on <= 0) return; ctx.save(); ctx.translate(BALL.x, BALL.y); ctx.rotate(t * Math.PI); ctx.lineCap = 'round'; ctx.lineWidth = 13;
    GMS.forEach((c, k) => { const f = Math.max(0, Math.min(1, on * 8 - k)); if (!f) return; const a0 = (-90 + 45 * k + 4) * Math.PI / 180; ctx.strokeStyle = c; ctx.beginPath(); ctx.arc(0, 0, 58, a0, a0 + 37 * f * Math.PI / 180); ctx.stroke(); });
    ctx.restore();
  }
  // poses: [ombro, cotovelo, mão, ângulo da mão, aberta?] por braço
  const POSES = {
    tranquilo: t => ({ L: [[548, 470], [500, 545], [505, 610], 0.3, false], R: [[862, 470], [910, 545], [905, 610], -0.3, false] }),
    tchau: t => { const w = Math.sin(t * Math.PI * 2 * 2) * 0.35; return { L: [[548, 470], [500, 545], [505, 610], 0.3, false], R: [[862, 455], [950 + 20 * w, 400], [960 + 60 * w, 300], -0.2 + w, true] }; },
    comemora: t => { const b = Math.sin(t * Math.PI * 4) * 12; return { L: [[548, 455], [470, 380], [470, 280 + b], 0.25, true], R: [[862, 455], [940, 380], [940, 280 + b], -0.25, true] }; },
    aponta: t => ({ L: [[548, 470], [462, 438], [388, 392], -1.05, false], R: [[862, 470], [910, 545], [905, 610], -0.3, false] }), // braço esquerdo (lado do leitor) estendido, mão fechada
  };
  const lerpArm = (a, b, k) => [0, 1, 2].map(i => [a[i][0] + (b[i][0] - a[i][0]) * k, a[i][1] + (b[i][1] - a[i][1]) * k]).concat([a[3] + (b[3] - a[3]) * k, k < 0.5 ? a[4] : b[4]]);
  // opcionais (reel30): o.poseB + o.mix (0..1) misturam duas poses; o.tilt (rad) inclina o tronco no quadril; o.amp (0..1) escala balanço, respiração e antena (0 = parado)
  R.draw = (ctx, t, o = {}) => {
    const { x = 0, y = 0, s = 1, pose = 'tranquilo', ring = 0 } = o, amp = o.amp ?? 1;
    const bob = Math.sin(t * Math.PI * 2) * 7 * amp, sq = 1 + Math.sin(t * Math.PI * 2 + 0.6) * 0.015 * amp, P0 = POSES[pose](t);
    const P = o.poseB && o.mix ? (Q => ({ L: lerpArm(P0.L, Q.L, o.mix), R: lerpArm(P0.R, Q.R, o.mix) }))(POSES[o.poseB](t)) : P0;
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.translate(-705, -770);   // origem = entre os pés
    // pernas e pés (não balançam com o corpo)
    for (const [hx, fx] of [[650, 630], [760, 780]]) { tube(ctx, [[hx, 620], [hx, 690], [fx, 735]], 26); ctx.beginPath(); ctx.ellipse(fx + (fx < 705 ? -10 : 10), 752, 44, 22, 0, 0, 7); fill(ctx, R.col.body); }
    ctx.translate(0, bob); ctx.translate(705, 630); ctx.scale(1 / sq, sq); if (o.tilt) ctx.rotate(o.tilt); ctx.translate(-705, -630);
    // braço de trás, corpo, antena (balança com atraso), rosto, braço da frente
    const arm = a => { tube(ctx, [a[0], a[1], a[2]], 24); hand(ctx, a[2][0], a[2][1], a[3], a[4]); };
    arm(P.L);
    ctx.drawImage(R.body, 0, 0);
    ctx.save(); ctx.translate(PIVOT.x, PIVOT.y); ctx.rotate(Math.sin(t * Math.PI * 2 - 0.9) * 0.1 * amp); ctx.translate(-PIVOT.x, -PIVOT.y); ctx.drawImage(R.antenna, 0, 0); gmsRing(ctx, t, ring); ctx.restore();
    face(ctx, t, o.face || {});
    arm(P.R);
    ctx.restore();
  };
  R.GMS = GMS; window.BitRig = R;
})();
