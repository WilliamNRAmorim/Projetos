// Cenários do Dia 4 dos contos (O Gato Preto, Mula sem cabeça, GPS, Pisadeira). Só ACRESCENTA ao Motor. Nada de violência aparece: só sombra, silhueta e som.
(() => {
  const { CENARIOS, POSES, OBJETOS, W, H, GY } = Motor, { rect, poly, circ, line, rrect, text, glow, vgrad, rgba, vinheta, rnd, lerp, clamp, out } = Motor.H_;
  const fundoGrad = (g, a, b) => vgrad(g, 0, H, a, b);
  const gato = (g, x, y, s, t, o = {}) => { // gato preto sentado de frente (y = chão); o.forca = mancha branca no peito em forma de forca; o.olhos 0..1
    g.save(); g.translate(x, y); g.scale(s, s); g.fillStyle = '#05060A'; g.beginPath(); g.ellipse(0, -90, 80, 100, 0, 0, Math.PI * 2); g.fill(); circ(g, 0, -230, 62, '#05060A'); poly(g, [[-52, -260], [-30, -330], [-8, -272]], '#05060A'); poly(g, [[52, -260], [30, -330], [8, -272]], '#05060A');
    g.strokeStyle = '#05060A'; g.lineWidth = 26; g.lineCap = 'round'; g.beginPath(); g.moveTo(70, -40); g.quadraticCurveTo(190, -40 + 10 * Math.sin(t * 2), 160, -170); g.stroke();
    const oa = o.olhos ?? 1; if (oa > 0) for (const dx of [-24, 24]) { glow(g, dx, -234, 50, '#C8E83A', 0.35 * oa); g.fillStyle = `rgba(200,232,58,${oa})`; g.beginPath(); g.ellipse(dx, -234, 11, 17, 0, 0, Math.PI * 2); g.fill(); circ(g, dx, -234, 5, '#05060A', oa); }
    if (o.forca) { g.strokeStyle = '#E8EAF0'; g.lineWidth = 9; g.beginPath(); g.moveTo(-16, -130); g.lineTo(-16, -50); g.moveTo(-34, -50); g.lineTo(16, -50); g.moveTo(-16, -130); g.lineTo(24, -130); g.lineTo(24, -108); g.stroke(); } g.restore();
  };
  const tijolos = (g, x0, y0, w, h, cor, escuro, k = 0) => { rect(g, x0, y0, w, h, cor); for (let r = 0; r * 46 < h; r++) { line(g, x0, y0 + r * 46, x0 + w, y0 + r * 46, escuro, 4); for (let c = (r % 2) * 55; c < w; c += 110) line(g, x0 + c, y0 + r * 46, x0 + c, y0 + (r + 1) * 46, escuro, 4); } };

  // ───────── O GATO PRETO (cinza-ferro) ─────────
  CENARIOS.taberna = (g, t, c = {}) => { // taberna escura; c.gato (barril com o gato), c.forca (mancha no peito), c.close
    fundoGrad(g, '#2A2E38', '#0E1016'); for (let x = 0; x < W; x += 120) rect(g, x, 0, 6, 1240, 'rgba(0,0,0,0.3)'); rect(g, 0, 1240, W, H - 1240, '#0A0C10'); for (let y = 1280; y < H; y += 90) rect(g, 0, y, W, 3, '#05060A');
    rect(g, 0, 900, W, 340, '#3A404E'); rect(g, 0, 880, W, 30, '#5A6274'); for (let i = 0; i < 3; i++) { rrect(g, 700 + i * 130, 1000, 110, 240, 20, '#4A3A2A'); rect(g, 700 + i * 130, 1050, 110, 10, '#1A1008'); rect(g, 700 + i * 130, 1160, 110, 10, '#1A1008'); }
    for (let i = 0; i < 4; i++) { rect(g, 60 + i * 90, 700, 60, 180, '#1A1E28'); rrect(g, 70 + i * 90, 640, 40, 70, 10, '#3A5A4A'); } rect(g, 40, 880, 400, 14, '#1A1008');
    const k = 0.9 + 0.1 * Math.sin(t * 9); rect(g, 520, 790, 20, 90, '#E8DCC0'); g.fillStyle = '#FF9A2E'; g.beginPath(); g.moveTo(530, 730); g.quadraticCurveTo(552, 770, 530, 790); g.quadraticCurveTo(508, 770, 530, 730); g.fill(); glow(g, 530, 760, 520 * k, '#FFB45A', 0.3);
    if (c.gato) { const es = c.close ? 2.0 : 1.0; rrect(g, 280 - 20 * es, 1080 - 70 * es, 200 * es, 160 * es, 10, '#4A3A2A'); gato(g, 380, 1080 - (c.close ? 70 : 0), es * 1.0, t, { forca: c.forca }); } vinheta(g, 0.6);
  };
  CENARIOS.casa_queimada = (g, t, c = {}) => { // ruína: só uma parede, com a silhueta de um gato gigante no reboco; brasas
    fundoGrad(g, '#0A0C12', '#2A1A14'); glow(g, 540, 1100, 900, '#FF7A2A', 0.22); rect(g, 0, 1240, W, H - 1240, '#0A0806');
    for (const [x, w, h] of [[40, 160, 280], [220, 80, 200], [840, 200, 340]]) poly(g, [[x, 1240], [x + 10, 1240 - h], [x + w * 0.5, 1240 - h * 1.1], [x + w, 1240 - h * 0.8], [x + w, 1240]], '#1A1410');
    rect(g, 300, 380, 480, 860, '#8A8478'); rect(g, 300, 380, 480, 860, 'rgba(0,0,0,0.35)'); for (let i = 0; i < 30; i++) rect(g, 300 + rnd(i) * 440, 380 + rnd(i + 5) * 820, 20 + rnd(i) * 40, 6, 'rgba(0,0,0,0.3)');
    g.save(); g.translate(540, 900); g.fillStyle = '#2A2824'; g.beginPath(); g.ellipse(0, 110, 150, 180, 0, 0, Math.PI * 2); g.fill(); circ(g, 0, -120, 100, '#2A2824'); poly(g, [[-90, -170], [-55, -290], [-10, -200]], '#2A2824'); poly(g, [[90, -170], [55, -290], [10, -200]], '#2A2824'); g.strokeStyle = '#2A2824'; g.lineWidth = 8; g.beginPath(); g.moveTo(-40, -30); g.quadraticCurveTo(0, 20, 40, -30); g.stroke(); g.restore(); // gato em relevo + corda no pescoço (só linha fina)
    for (let i = 0; i < 40; i++) { const k = (t * 0.2 + rnd(i)) % 1; circ(g, 100 + rnd(i + 3) * 880, 1200 - k * 700, 3 + rnd(i) * 3, '#FF8A2A', 0.6 * (1 - k)); } vinheta(g, 0.6);
  };
  CENARIOS.porao = (g, t, c = {}) => { // porão de pedra com lanterna; c.sombra = sombra de um braço com machado; c.parede = 'nova' | 'desaba' (c.desabaEm); sempre sem corpo
    fundoGrad(g, '#14161E', '#06070A'); rect(g, 0, 1240, W, H - 1240, '#0A0B0E'); for (let y = 1290; y < H; y += 100) rect(g, 0, y, W, 4, '#05060A');
    tijolos(g, 0, 160, W, 1080, '#2A2E3A', '#12141A'); for (let i = 0; i < 12; i++) rect(g, 40 + rnd(i) * 900, 200 + rnd(i + 3) * 1000, 70, 36, 'rgba(255,255,255,0.03)');
    poly(g, [[0, 0], [360, 0], [360, 640], [0, 1240]], '#1A1C24'); for (let i = 0; i < 8; i++) poly(g, [[i * 45, 640 + i * 76 - 40], [i * 45 + 45, 640 + i * 76 - 40], [i * 45 + 45, 640 + i * 76 + 36], [i * 45, 640 + i * 76 + 36]], '#3A3E4A'); // escada
    const k = 0.88 + 0.12 * Math.sin(t * 8); rect(g, 690, 280, 8, 120, '#05060A'); rrect(g, 664, 400, 60, 80, 8, '#4A4A52'); rect(g, 676, 410, 36, 60, '#FFD890', 0.9); glow(g, 694, 440, 620 * k, '#FFB45A', 0.3);
    if (c.parede) { const d = c.parede === 'desaba' ? clamp((t - (c.desabaEm ?? 1)) / 2.2) : 0, x0 = 420, y0 = 560, w = 560, h = 680; tijolos(g, x0, y0, w, h, c.parede === 'nova' || c.parede === 'desaba' ? '#4A4F5E' : '#2A2E3A', '#1A1C24');
      if (c.parede === 'desaba') { rect(g, x0 + w * 0.2, y0 + h * 0.15, w * 0.6 * out(d), h * 0.8 * out(d), '#020304'); const ex = x0 + w * 0.5, ey = y0 + h * 0.5; if (d > 0.3) { const a = clamp((d - 0.3) / 0.4); g.save(); g.globalAlpha = a; gato(g, ex, ey + 220, 0.9, t, {}); poly(g, [[ex - 160, ey + 330], [ex - 60, ey + 120], [ex + 60, ey + 120], [ex + 160, ey + 330]], '#040506'); g.restore(); } for (let i = 0; i < 14; i++) { const kk = clamp(d * 1.2 - i * 0.04); if (kk > 0 && kk < 1) rect(g, x0 + 60 + rnd(i) * 440, y0 + rnd(i + 2) * 200 + kk * 700, 60, 30, '#4A4F5E'); } } }
    if (c.sombra) { g.save(); g.globalAlpha = 0.88; g.fillStyle = '#020304'; g.lineCap = 'round'; g.lineWidth = 46; g.strokeStyle = '#020304'; g.beginPath(); g.moveTo(520, 900); g.lineTo(640 + 14 * Math.sin(t * 6), 560); g.stroke(); g.beginPath(); g.moveTo(600, 560); g.lineTo(700, 480); g.stroke(); poly(g, [[660, 400], [800, 380], [830, 470], [700, 500]], '#020304'); g.beginPath(); g.ellipse(470, 980, 110, 130, 0, 0, Math.PI * 2); g.fill(); g.restore(); }
    vinheta(g, 0.65);
  };

  // ───────── MULA SEM CABEÇA (laranja-fogo) ─────────
  const mula = (g, x, y, s, t) => { // mula de fogo galopando (corpo escuro, pescoço em chamas, sem cabeça); x = centro, y = chão
    g.save(); g.translate(x, y); g.scale(s, s); const ph = t * 12; g.fillStyle = '#0A0604'; g.beginPath(); g.ellipse(0, -150, 160, 70, 0, 0, Math.PI * 2); g.fill(); g.strokeStyle = '#0A0604'; g.lineWidth = 26; g.lineCap = 'round';
    for (const [lx, p] of [[-110, 0], [-70, 2], [90, 1], [130, 3]]) { const a = Math.sin(ph + p) * 0.7; g.beginPath(); g.moveTo(lx, -110); g.lineTo(lx + 50 * Math.sin(a), -40); g.lineTo(lx + 80 * Math.sin(a), -5 + 20 * Math.max(0, Math.cos(ph + p))); g.stroke(); } poly(g, [[110, -190], [200, -300], [170, -190]], '#0A0604');
    for (let i = 0; i < 9; i++) { const f = 1 + 0.4 * Math.sin(t * 17 + i * 2); glow(g, 190 + 10 * Math.sin(t * 9 + i), -300 - i * 22, 90 * f, '#FF6A1A', 0.5); g.fillStyle = i % 2 ? '#FFB43A' : '#FF5A14'; g.beginPath(); g.ellipse(190 + 14 * Math.sin(t * 11 + i), -300 - i * 18, 28 - i * 2, 40 * f, 0, 0, Math.PI * 2); g.fill(); } glow(g, 190, -330, 400, '#FF7A1A', 0.35); g.restore();
  };
  CENARIOS.vila_noite = (g, t, c = {}) => { // rua da vila à noite, casas de janelas fechadas; c.mula = {x0,x1,dur} atravessa, c.mulaParada = x; c.brilho 0..1 laranja
    fundoGrad(g, '#080A18', '#2A2038'); for (let i = 0; i < 40; i++) circ(g, rnd(i) * W, rnd(i + 99) * 500, 1.4 + rnd(i + 5) * 1.6, '#FFE9C8', 0.3 + 0.3 * rnd(i + 3));
    for (const [x, w, h, col] of [[-40, 330, 520, '#2A2030'], [300, 300, 440, '#201828'], [600, 280, 560, '#2A2030'], [860, 280, 480, '#201828']]) { rect(g, x, 1240 - h, w, h, col); poly(g, [[x - 14, 1240 - h], [x + w / 2, 1240 - h - 100], [x + w + 14, 1240 - h]], '#120C18'); rect(g, x + 40, 1240 - h + 90, 90, 130, '#0A0610'); rect(g, x + 44, 1240 - h + 94, 82, 122, '#3A2A3A'); rect(g, x + w - 140, 1240 - 250, 90, 250, '#0A0610'); }
    rect(g, 0, 1240, W, H - 1240, '#1A1210'); poly(g, [[200, 1240], [880, 1240], [1100, H], [-120, H]], '#2A1E18'); for (let i = 0; i < 30; i++) circ(g, rnd(i) * W, 1260 + rnd(i + 3) * 600, 4 + rnd(i) * 6, 'rgba(0,0,0,0.2)');
    const gl = c.brilho ?? 0; if (gl) { glow(g, 80, 1100, 900, '#FF7A1A', 0.4 * gl); poly(g, [[0, 1240], [W, 1240], [W, H], [0, H]], 'rgba(255,120,30,' + 0.12 * gl + ')'); }
    if (c.mula) { const u = clamp((t - (c.mula.ini || 0)) / c.mula.dur), x = lerp(c.mula.x0, c.mula.x1, u); if (u > 0 && u < 1) { glow(g, x, 1100, 700, '#FF7A1A', 0.45); mula(g, x, 1330, c.mula.esc || 1.2, t); } }
    if (c.mulaParada != null) { glow(g, c.mulaParada, 1100, 800, '#FF7A1A', 0.5); mula(g, c.mulaParada, 1340, 2.0, t * 0.2); }
    vinheta(g, 0.55);
  };
  CENARIOS.janela_quarto = (g, t, c = {}) => { // quarto do Seu João: janela com venezianas (c.fresta 0..1), cama com ele (c.olhos), brilho laranja de fora (c.fogo), c.mulaJanela
    vgrad(g, 0, 1240, '#3A2A22', '#1E1410'); for (let x = 0; x < W; x += 100) rect(g, x, 0, 4, 1240, 'rgba(0,0,0,0.25)'); rect(g, 0, 1240, W, H - 1240, '#120C08'); for (let y = 1280; y < H; y += 90) rect(g, 0, y, W, 3, '#0A0604');
    const wx = 560, wy = 240, ww = 400, wh = 600; rect(g, wx - 24, wy - 24, ww + 48, wh + 48, '#0A0604'); vgrad(g, wy, wy + wh, '#0A1028', '#1A2848', wx, ww); const fr = clamp(c.fresta ?? 0);
    g.save(); g.beginPath(); g.rect(wx, wy, ww, wh); g.clip(); if (c.fogo) { glow(g, wx + ww / 2, wy + wh * 0.7, 700, '#FF7A1A', 0.5 * c.fogo); rect(g, wx, wy, ww, wh, 'rgba(255,120,30,' + 0.25 * c.fogo + ')'); } if (c.mulaJanela) { const u = (t * 0.6) % 1; mula(g, lerp(wx + ww + 200, wx - 300, u), wy + wh - 20, 0.9, t); } g.restore();
    const gap = 6 + fr * 150; rect(g, wx, wy, ww / 2 - gap / 2, wh, '#2A1A10'); rect(g, wx + ww / 2 + gap / 2, wy, ww / 2 - gap / 2, wh, '#2A1A10'); for (let i = 0; i < 8; i++) { rect(g, wx, wy + 20 + i * 70, ww / 2 - gap / 2, 8, '#120A06'); rect(g, wx + ww / 2 + gap / 2, wy + 20 + i * 70, ww / 2 - gap / 2, 8, '#120A06'); }
    rect(g, 40, 1000, 520, 240, '#4A3028'); rect(g, 20, 900, 30, 340, '#120A06'); rrect(g, 70, 950, 260, 80, 34, '#E8DCC8', 0.85); circ(g, 200, 975, 70, '#C99A74'); g.fillStyle = '#2A1E14'; g.beginPath(); g.arc(200, 968, 74, Math.PI, Math.PI * 2); g.fill();
    for (const dx of [-24, 24]) { if (c.olhos === 'abertos') { circ(g, 200 + dx, 982, 15, '#FFF'); circ(g, 200 + dx + 8, 984, 6, '#10140F'); line(g, 200 + dx - 14, 958, 200 + dx + 12, 954, '#2A1E18', 5); } else line(g, 200 + dx - 14, 984, 200 + dx + 14, 984, '#2A1E18', 5); } line(g, 188, 1022, 212, 1022, '#6A4038', 5); poly(g, [[110, 1040], [320, 1030], [560, 1060], [560, 1240], [100, 1240]], '#8A5A3A');
    if (c.fogo) glow(g, 600, 700, 800, '#FF7A1A', 0.2 * c.fogo); vinheta(g, 0.55);
  };
  CENARIOS.porta_ferradura = (g, t, c = {}) => { // porta de madeira de manhã com uma ferradura queimada na madeira
    vgrad(g, 0, 1240, '#C8B8A8', '#8A7A68'); rect(g, 0, 1240, W, H - 1240, '#4A3A2A'); rect(g, 280, 260, 520, 980, '#2A1A10'); rect(g, 310, 290, 460, 940, '#6A4A30'); for (let i = 0; i < 5; i++) rect(g, 310 + i * 92, 290, 4, 940, 'rgba(0,0,0,0.3)'); rect(g, 310, 700, 460, 14, '#2A1A10'); circ(g, 720, 800, 14, '#C9B38A');
    g.save(); g.translate(540, 560); g.strokeStyle = '#0A0604'; g.lineWidth = 56; g.lineCap = 'round'; g.beginPath(); g.arc(0, 0, 130, Math.PI * 0.15, Math.PI * 0.85, true); g.stroke(); g.strokeStyle = '#FF6A1A'; g.lineWidth = 22; g.globalAlpha = 0.55 + 0.25 * Math.sin(t * 3); g.beginPath(); g.arc(0, 0, 130, Math.PI * 0.15, Math.PI * 0.85, true); g.stroke(); g.restore(); for (let i = 0; i < 5; i++) circ(g, 540 + (i - 2) * 56, 560 + 130 * 0.9 - (i % 2) * 6, 7, '#0A0604');
    glow(g, 540, 600, 520, '#FF7A1A', 0.12); rect(g, 0, 0, 220, H, 'rgba(255,255,255,0.08)'); vinheta(g, 0.4);
  };

  // ───────── GPS (verde-radar) ─────────
  CENARIOS.estrada_gps = (g, t, c = {}) => { // estrada de madrugada, mato à direita; HUD verde do GPS; c.mato (destaca o mato)
    fundoGrad(g, '#020806', '#0A1A12'); const vx = 540, vy = 820; poly(g, [[vx - 30, vy], [vx + 30, vy], [W + 300, 1500], [-300, 1500]], '#0A100E'); for (let i = 0; i < 9; i++) { const k = ((t * 0.9 + i / 9) % 1), y = lerp(vy, 1480, Math.pow(k, 2.2)), w = lerp(4, 40, Math.pow(k, 2.2)); rect(g, vx - w / 2, y, w, lerp(8, 90, Math.pow(k, 2.2)), '#D8E8D8', 0.7); }
    for (let i = 0; i < 70; i++) { const k = ((t * 0.5 + rnd(i)) % 1), e = Math.pow(k, 2.2), x = vx + lerp(60, 1100, e) * (c.mato && i % 2 ? 1 : (i % 2 ? 1 : 0.0)), y = lerp(vy, 1400, e); if (i % 2 || c.mato) { line(g, vx + lerp(70, 900, e), y, vx + lerp(70, 900, e) + 12, y - lerp(20, 260, e), '#1A4A2A', lerp(3, 18, e), 0.9); void x; } }
    poly(g, [[vx - 30, vy + 10], [vx + 30, vy + 10], [vx + 520, 1500], [vx - 520, 1500]], '#D8E8D8', 0.05); glow(g, vx, vy + 60, 480, '#D8E8D8', 0.2); rect(g, 0, 1380, W, H - 1380, '#020605'); rect(g, 0, 1370, W, 12, '#0A2A18');
    rrect(g, 340, 1450, 400, 280, 28, '#020605'); rrect(g, 354, 1464, 372, 252, 20, '#04140A'); for (let i = 0; i < 6; i++) line(g, 354, 1464 + i * 42, 726, 1464 + i * 42, 'rgba(57,255,136,0.15)', 2); line(g, 420, 1700, 560, 1560, '#39FF88', 8); line(g, 560, 1560, 620, 1500, '#39FF88', 8); circ(g, 420, 1700, 12, '#39FF88'); glow(g, 540, 1590, 340, '#39FF88', 0.2); vinheta(g, 0.55);
  };
  CENARIOS.gps_tela = (g, t, c = {}) => { // tela do GPS de perto; c.linha1/c.linha2 (texto), c.erro
    fundoGrad(g, '#020806', '#061A10'); rrect(g, 80, 360, 920, 1000, 50, '#010403'); rrect(g, 110, 390, 860, 940, 36, '#03150C'); for (let i = 0; i < 16; i++) line(g, 110, 400 + i * 58, 970, 400 + i * 58, 'rgba(57,255,136,0.1)', 2); for (let i = 0; i < 12; i++) line(g, 120 + i * 72, 390, 120 + i * 72, 1330, 'rgba(57,255,136,0.08)', 2);
    line(g, 300, 1250, 300, 900, '#39FF88', 14); line(g, 300, 900, 520, 760, '#39FF88', 14); line(g, 520, 760, 520, 520, '#39FF88', 14); circ(g, 300, 1250, 24, '#39FF88'); glow(g, 300, 1250, 300, '#39FF88', 0.3); const k = 0.7 + 0.3 * Math.sin(t * 6); poly(g, [[760, 940], [800, 1030], [760, 1010], [720, 1030]], '#39FF88', k); text(g, c.linha1 || '', 540, 480, 74, '#39FF88', { align: 'center', w: 800, mono: 1 }); text(g, c.linha2 || '', 540, 580, 46, 'rgba(57,255,136,0.8)', { align: 'center', w: 700, mono: 1 }); glow(g, 540, 860, 760, '#39FF88', 0.12); vinheta(g, 0.5);
  };
  CENARIOS.casa_dois_andares = (g, t, c = {}) => { // casa de dois andares desconhecida à noite; c.garagem (carro), c.janela (silhueta de costas)
    fundoGrad(g, '#020806', '#0A1A14'); for (let i = 0; i < 30; i++) circ(g, rnd(i) * W, rnd(i + 99) * 400, 1.4 + rnd(i + 5) * 1.6, '#D8FFE8', 0.3); rect(g, 0, 1240, W, H - 1240, '#06100C'); rect(g, 120, 360, 840, 880, '#1A2A22'); poly(g, [[80, 360], [540, 160], [1000, 360]], '#0A1410'); rect(g, 120, 800, 840, 14, '#0A1410');
    rect(g, 170, 940, 360, 300, '#0A1410'); rect(g, 600, 940, 120, 300, '#0A1410'); circ(g, 700, 1100, 8, '#9AB8A8'); for (const x of [200, 700]) { rect(g, x, 480, 150, 200, '#0A1410'); rect(g, x + 8, 488, 134, 184, c.janela && x === 200 ? '#F2E8B0' : '#0E1C16'); rect(g, x + 70, 488, 8, 184, '#0A1410'); }
    if (c.janela) { glow(g, 275, 580, 420, '#F2E8B0', 0.35); g.fillStyle = '#070A08'; g.beginPath(); g.ellipse(275, 560, 38, 46, 0, 0, Math.PI * 2); g.fill(); poly(g, [[225, 672], [325, 672], [310, 600], [240, 600]], '#070A08'); }
    if (c.garagem) { rect(g, 190, 960, 320, 280, '#12201A'); Motor.H_.carro(g, 350, 1230, 0.42, '#B8BCC8', true); glow(g, 480, 1190, 120, '#FFF0B0', 0.25); }
    vinheta(g, 0.55);
  };

  // ───────── PISADEIRA (terracota) ─────────
  CENARIOS.quarto_terra = (g, t, c = {}) => { // quarto à noite visto do pé da cama, tons de terracota; c.olhos 'abertos'|'fechados', c.peso (silhueta de unhas sobre o peito), c.manha, c.marcas (4 riscos), c.telha (telha quebrada no teto)
    const m = c.manha ? 1 : 0; vgrad(g, 0, 1240, m ? '#B88A68' : '#4A2A20', m ? '#7A5038' : '#1E100C'); rect(g, 0, 1240, W, H - 1240, m ? '#3A2218' : '#120806'); for (let y = 1280; y < H; y += 90) rect(g, 0, y, W, 3, 'rgba(0,0,0,0.3)');
    rect(g, 0, 0, W, 200, m ? '#5A3A28' : '#2A1410'); for (let x = 0; x < W; x += 180) rect(g, x, 0, 24, 200, m ? '#3A2218' : '#120806'); if (c.telha) { rect(g, 520, 20, 160, 140, '#0A0604'); poly(g, [[520, 160], [680, 160], [760, 1240], [440, 1240]], 'rgba(255,240,200,' + (m ? 0.18 : 0.08) + ')'); glow(g, 600, 90, 380, '#FFF0C8', 0.4); }
    rect(g, 70, 340, 300, 460, '#0A0604'); vgrad(g, 356, 784, m ? '#E8D8B0' : '#14102A', m ? '#F8E8C0' : '#2A2A58', 86, 268); rect(g, 224, 356, 10, 428, '#0A0604'); if (!m) { circ(g, 300, 470, 46, '#E8EEFF', 0.9); glow(g, 300, 470, 300, '#C8D8FF', 0.25); }
    rect(g, 220, 940, 640, 300, m ? '#8A6A58' : '#2A1612'); rect(g, 200, 860, 40, 380, '#0A0604'); rect(g, 840, 900, 40, 340, '#0A0604'); rrect(g, 330, 930, 420, 90, 36, m ? '#F2EEE0' : '#D8D0C0', 0.8); const hx = 540; circ(g, hx, 970, 76, '#C99A74'); g.fillStyle = '#2A1E14'; g.beginPath(); g.arc(hx, 962, 80, Math.PI, Math.PI * 2); g.fill();
    for (const dx of [-26, 26]) { if (c.olhos === 'abertos') { circ(g, hx + dx, 978, 16, '#FFF'); circ(g, hx + dx, 980, 6, '#10140F'); line(g, hx + dx - 14, 952, hx + dx + 12, 948, '#2A1E18', 5); } else line(g, hx + dx - 14, 980, hx + dx + 14, 980, '#2A1E18', 5); } line(g, hx - 12, 1020, hx + 12, 1020, '#6A4038', 5);
    poly(g, [[260, 1050], [540, 1030], [830, 1050], [840, 1240], [250, 1240]], m ? '#C8A888' : '#8A4A32'); poly(g, [[280, 1050], [520, 1040], [520, 1240], [270, 1240]], 'rgba(255,255,255,0.07)');
    if (c.marcas) for (let i = 0; i < 4; i++) line(g, 470 + i * 26, 1075, 482 + i * 26, 1150, '#E88A8A', 5, 0.8);
    if (c.peso) { g.save(); g.fillStyle = '#04030A'; g.globalAlpha = 0.9; g.beginPath(); g.ellipse(540, 1080, 190, 80, 0, 0, Math.PI * 2); g.fill(); for (let i = 0; i < 4; i++) { poly(g, [[420 + i * 70, 1100], [440 + i * 70, 1100], [430 + i * 70 + (i - 1.5) * 14, 1200]], '#04030A'); } g.restore(); }
    if (m) glow(g, 220, 560, 800, '#FFE0A0', 0.3); vinheta(g, m ? 0.35 : 0.6);
  };
  CENARIOS.telhado_noite = (g, t, c = {}) => { // telhados de telha à noite com a lua; a Pisadeira (silhueta de unhas compridas) anda no telhado
    fundoGrad(g, '#0A0814', '#2A1A30'); circ(g, 800, 360, 120, '#F2E8D8', 0.9); glow(g, 800, 360, 500, '#F2E8D8', 0.25);
    for (const [x, y, w] of [[-100, 1100, 700], [500, 1000, 700]]) { poly(g, [[x, y + 240], [x + w * 0.5, y], [x + w, y + 240]], '#5A2A1A'); for (let r = 0; r < 6; r++) line(g, x + r * 20, y + 40 + r * 40, x + w - r * 20, y + 40 + r * 40, '#2A120A', 6); }
    rect(g, 780, 880, 60, 160, '#3A1A10'); rect(g, 0, 1340, W, H - 1340, '#120A0C'); const x = lerp(160, 760, (t * 0.12) % 1) , y = 1030 - (x - 160) * 0.16; g.save(); g.translate(x, y); g.fillStyle = '#04030A'; g.beginPath(); g.ellipse(0, -140, 55, 90, 0.1, 0, Math.PI * 2); g.fill(); circ(g, 0, -260, 50, '#04030A'); for (let i = 0; i < 9; i++) line(g, -30 + i * 8, -300, -60 + i * 12, -150 + i * 6, '#04030A', 6); g.lineWidth = 12; g.strokeStyle = '#04030A'; g.lineCap = 'round'; g.beginPath(); g.moveTo(-40, -180); g.lineTo(-130, -110); g.stroke(); g.beginPath(); g.moveTo(40, -180); g.lineTo(130, -120); g.stroke(); for (const sx of [-1, 1]) for (let i = 0; i < 4; i++) line(g, sx * 130, -112 + (sx > 0 ? -8 : 0), sx * (160 + i * 6), -60 + i * 14, '#B8A8A0', 4); circ(g, -16, -266, 6, '#E8E060'); circ(g, 16, -266, 6, '#E8E060'); g.restore(); vinheta(g, 0.55);
  };
  CENARIOS.olhos_fechados = (g, t, c = {}) => { // o escuro de olhos fechados: avermelhado, com pontos de luz; c.unhas = duas unhas finas subindo para o queixo
    fundoGrad(g, '#2A0A06', '#0A0202'); glow(g, 540, 800, 900, '#8A2A18', 0.25 + 0.05 * Math.sin(t * 1.3)); for (let i = 0; i < 40; i++) circ(g, rnd(i) * W, rnd(i + 5) * H, 2 + rnd(i) * 3, '#FF8A5A', 0.15 + 0.2 * Math.abs(Math.sin(t * 0.8 + i)));
    if (c.unhas) { const u = clamp((t - (c.unhasEm ?? 0)) / 2.5), y = lerp(H + 100, 1180, out(u)); for (const dx of [-60, 60]) { g.fillStyle = '#D8CCC0'; g.beginPath(); g.moveTo(540 + dx - 14, y + 600); g.lineTo(540 + dx + 14, y + 600); g.lineTo(540 + dx * 0.6 + 4, y); g.closePath(); g.fill(); g.fillStyle = 'rgba(0,0,0,0.25)'; g.fillRect(540 + dx - 14, y + 300, 28, 300); } }
    vinheta(g, 0.7);
  };
})();
