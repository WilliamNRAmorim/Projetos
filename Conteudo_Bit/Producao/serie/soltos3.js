// Cenários do Short solto 03 (Boto). Só ACRESCENTA ao Motor. Prefixo bt_ = ameixa, rosa-boto, ouro de lampião e o vermelho da marca.
(() => {
  const { CENARIOS } = Motor, W = Motor.W, H = Motor.H, { rect, circ, line, rrect, glow, vgrad, vinheta, rnd, lerp, clamp, out, P } = Motor.H_;
  const TAU = Math.PI * 2, BREU = '#0D0414', ROSA = '#F29BB2', OURO = '#FFC76A', BRANCO = '#F6EFE6', PELE = '#B97A58', PELE2 = '#8F5640';
  const elipse = (g, x, y, rx, ry, c, a = 1, rot = 0) => { g.globalAlpha = a; g.fillStyle = c; g.beginPath(); g.ellipse(x, y, rx, ry, rot, 0, TAU); g.fill(); g.globalAlpha = 1; };
  const forma = (g, c, fn, a = 1) => { g.globalAlpha = a; g.fillStyle = c; g.beginPath(); fn(g); g.closePath(); g.fill(); g.globalAlpha = 1; };
  const curva = (g, c, lw, fn, a = 1) => { g.globalAlpha = a; g.strokeStyle = c; g.lineWidth = lw; g.lineCap = 'round'; g.lineJoin = 'round'; g.beginPath(); fn(g); g.stroke(); g.globalAlpha = 1; };

  // ───── peças
  function ceu(g, t, y1, o = {}) {
    vgrad(g, 0, y1, o.a || '#160726', o.b || '#6A2250');
    for (let i = 0; i < 60; i++) circ(g, rnd(i + 3) * W, rnd(i + 41) * y1 * 0.6, 1.5 + rnd(i) * 2, BRANCO, (o.estrelas ?? 0.6) * (0.5 + 0.5 * Math.sin(t * 2 + i)));
  }
  function lua(g, x, y, r) { glow(g, x, y, r * 4.5, ROSA, 0.4); circ(g, x, y, r, '#FFE3D6'); circ(g, x - r * 0.3, y - r * 0.2, r * 0.18, '#EAC4BC', 0.8); circ(g, x + r * 0.25, y + r * 0.35, r * 0.24, '#EAC4BC', 0.7); }
  function mata(g, y, cor, s = 0) { forma(g, cor, q => { q.moveTo(-20, y); for (let x = -20; x <= W + 60; x += 60) q.quadraticCurveTo(x + 30, y - 60 - rnd(x + s) * 110, x + 60, y - 20 - rnd(x + s + 7) * 30); q.lineTo(W + 80, y + 6); q.lineTo(-20, y + 6); }); }
  function rio(g, t, y0, y1, o = {}) {
    vgrad(g, y0, y1, o.a || '#5C1F4A', o.b || '#12051C');
    for (let i = 0; i < 70; i++) { const k = i / 70, y = y0 + 14 + Math.pow(k, 1.4) * (y1 - y0 - 20), w = 30 + k * 150, x = ((rnd(i + 5) * 1400 + t * (14 + 30 * k)) % 1400) - 160; rect(g, x, y + Math.sin(t * 1.7 + i) * 4, w, 3 + k * 5, o.luz || ROSA, 0.1 + 0.2 * rnd(i + 2)); }
    if (o.reflexo) for (let i = 0; i < 18; i++) { const y = y0 + 20 + i * 34, w = 150 - i * 5 + Math.sin(t * 3 + i) * 40; rect(g, o.reflexo - w / 2 + Math.sin(t * 2 + i * 1.7) * 18, y, w, 9, '#FFE3D6', 0.5 - i * 0.022); }
  }
  function bandeiras(g, t, y, s = 1, ap = 1) {
    const cores = [P.accent, OURO, ROSA, BRANCO];
    curva(g, '#C9A58A', 3, q => { q.moveTo(-20, y); q.quadraticCurveTo(540, y + 120 * s, 1100, y); }, 0.7 * ap);
    for (let i = 0; i < 14; i++) { const k = (i + 0.5) / 14, x = -20 + 1120 * k, yy = y + 240 * s * k * (1 - k) + 2, b = Math.sin(t * 3 + i) * 8; forma(g, cores[i % 4], q => { q.moveTo(x - 30 * s, yy); q.lineTo(x + 30 * s, yy); q.lineTo(x + 28 * s + b, yy + 78 * s); q.lineTo(x + b, yy + 54 * s); q.lineTo(x - 28 * s + b, yy + 78 * s); }, ap); }
  }
  function luzes(g, t, y, ap = 1) { for (let i = 0; i < 11; i++) { const x = 40 + i * 100, yy = y + Math.sin(i / 10 * Math.PI) * 70; if (ap > 0.2) glow(g, x, yy, 90, OURO, 0.28 * ap * (0.85 + 0.15 * Math.sin(t * 5 + i))); circ(g, x, yy, 12, ap > 0.2 ? '#FFE9B0' : '#4A3040'); } }
  function fogueira(g, t, x, y, s) {
    glow(g, x, y - 100 * s, 460 * s, '#FF7A2A', 0.5);
    for (const [c, k] of [[P.accent, 1], ['#FF8A2A', 0.72], ['#FFE08A', 0.42]]) forma(g, c, q => { const h = 240 * s * k * (1 + 0.14 * Math.sin(t * 11 + k * 9)); q.moveTo(x - 80 * s * k, y); q.quadraticCurveTo(x - 100 * s * k, y - h * 0.5, x + Math.sin(t * 8 + k) * 20 * s, y - h); q.quadraticCurveTo(x + 100 * s * k, y - h * 0.45, x + 80 * s * k, y); });
    for (const d of [-1, 1]) line(g, x - 110 * s * d, y + 4, x + 90 * s * d, y - 40 * s, '#3A1A14', 28 * s);
    for (let i = 0; i < 12; i++) { const u = (t * 0.5 + rnd(i)) % 1; circ(g, x + (rnd(i + 8) - 0.5) * 200 * s + Math.sin(t * 3 + i) * 20, y - 160 * s - u * 360 * s, 5 * s, OURO, 1 - u); }
  }
  // chapéu branco; (x,y) = centro da aba
  function chapeu(g, x, y, s, rot = 0) {
    g.save(); g.translate(x, y); g.rotate(rot); g.scale(s, s);
    elipse(g, 0, 8, 190, 48, '#BFB2AE'); elipse(g, 0, 0, 190, 46, BRANCO);
    forma(g, BRANCO, q => { q.moveTo(-108, -4); q.quadraticCurveTo(-104, -150, -52, -146); q.quadraticCurveTo(0, -118, 52, -146); q.quadraticCurveTo(104, -150, 108, -4); q.quadraticCurveTo(0, 30, -108, -4); });
    forma(g, P.accent, q => { q.moveTo(-107, -44); q.quadraticCurveTo(0, -12, 107, -44); q.lineTo(108, -6); q.quadraticCurveTo(0, 28, -108, -6); });
    curva(g, '#D6CAC4', 7, q => { q.moveTo(-8, -126); q.quadraticCurveTo(6, -90, -2, -56); });
    g.restore();
  }
  // o rapaz de branco, corpo inteiro; (x,y) = pés. o.mao, o.copo, o.flip, o.sombra
  function rapaz(g, t, x, y, s, o = {}) {
    g.save(); g.translate(x, y); g.scale(s * (o.flip ? -1 : 1), s);
    elipse(g, 0, 4, 130, 22, BREU, 0.55);
    const paletó = o.sombra ? BREU : BRANCO, dobra = o.sombra ? BREU : '#CFC2C0', pele = o.sombra ? BREU : PELE;
    for (const d of [-1, 1]) { line(g, d * 28, -250, d * 44, -20, paletó, 52); elipse(g, d * 52, -8, 42, 18, o.sombra ? BREU : '#E8DDD6'); }
    forma(g, paletó, q => { q.moveTo(-92, -470); q.quadraticCurveTo(0, -500, 92, -470); q.lineTo(70, -230); q.lineTo(-70, -230); });
    if (!o.sombra) { forma(g, P.accent, q => { q.moveTo(-26, -482); q.lineTo(26, -482); q.lineTo(0, -380); }); curva(g, dobra, 8, q => { q.moveTo(-40, -478); q.lineTo(0, -360); q.lineTo(40, -478); q.moveTo(0, -360); q.lineTo(0, -236); }); }
    const mao = o.mao ? [210, -370] : o.copo ? [70, -520] : [112, -250];
    curva(g, paletó, 40, q => { q.moveTo(-80, -450); q.quadraticCurveTo(-130, -360, -112, -250); }); circ(g, -112, -240, 22, pele);
    curva(g, paletó, 40, q => { q.moveTo(80, -450); q.quadraticCurveTo(150, o.copo ? -360 : -370, mao[0], mao[1]); }); circ(g, mao[0] + 6, mao[1], 23, pele);
    rect(g, -22, -515, 44, 45, pele); elipse(g, 0, -560, 58, 66, pele);
    if (!o.sombra) { for (const d of [-1, 1]) { circ(g, d * 22, -562, 6, BREU); curva(g, BREU, 5, q => { q.moveTo(d * 34, -580); q.lineTo(d * 12, -578); }); } curva(g, '#FFF4EE', 8, q => q.arc(0, -546, 26, 0.3, Math.PI - 0.3)); }
    chapeu(g, 0, -605, 0.56, o.rot || 0);
    if (o.sombra) elipse(g, 0, -608, 106, 25, BRANCO, 0.9);
    if (o.copo) { rect(g, 52, -556, 50, 62, OURO); rect(g, 52, -556, 50, 10, '#FFF0C8'); }
    g.restore();
  }
  // Naiara, corpo inteiro; (x,y) = pés. o.gira (balanço), o.braco: 'alto' | 'puxa' | 'solto'
  function moca(g, t, x, y, s, o = {}) {
    const b = o.gira ? Math.sin(t * 6) : Math.sin(t * 1.6) * 0.2;
    g.save(); g.translate(x, y); g.scale(s * (o.flip ? -1 : 1), s); g.rotate(b * 0.05);
    elipse(g, 0, 4, 150, 22, BREU, 0.55);
    for (const d of [-1, 1]) line(g, d * 24, -190, d * 36, -10 - (o.gira ? Math.max(0, d * b) * 40 : 0), PELE2, 26);
    forma(g, '#5E1440', q => { q.moveTo(-90, -520); q.quadraticCurveTo(-130, -400, -66, -330); q.lineTo(-20, -540); });
    forma(g, '#E0437A', q => { q.moveTo(-50, -360); q.quadraticCurveTo(-110 - b * 40, -230, -158 - b * 55, -110); q.quadraticCurveTo(0, -150 + b * 20, 158 - b * 55, -110); q.quadraticCurveTo(110 - b * 40, -230, 50, -360); });
    for (let i = 0; i < 9; i++) circ(g, -120 + i * 30 - b * 45, -138 + Math.sin(i) * 8, 9, OURO);
    forma(g, '#E0437A', q => { q.moveTo(-56, -470); q.lineTo(56, -470); q.lineTo(46, -352); q.lineTo(-46, -352); }); rect(g, -50, -366, 100, 18, BRANCO);
    const br = o.braco || 'solto';
    curva(g, PELE, 28, q => { q.moveTo(-50, -450); if (br === 'alto') q.quadraticCurveTo(-140, -470, -150, -590 + b * 20); else q.quadraticCurveTo(-110, -380, -100, -280); });
    curva(g, PELE, 28, q => { q.moveTo(50, -450); if (br === 'puxa') q.quadraticCurveTo(140, -520, 180, -640); else if (br === 'alto') q.quadraticCurveTo(130, -400, 160, -420 - b * 20); else q.quadraticCurveTo(110, -380, 100, -280); });
    rect(g, -18, -505, 36, 40, PELE); elipse(g, -6, -552, 70, 74, '#220A12'); elipse(g, 4, -544, 50, 60, PELE);
    forma(g, '#220A12', q => { q.moveTo(-56, -548); q.quadraticCurveTo(-40, -630, 56, -590); q.quadraticCurveTo(0, -586, -34, -548); });
    for (const d of [-1, 1]) circ(g, 6 + d * 19, -546, 6, BREU); curva(g, '#6A1E24', 7, q => q.arc(6, -528, 17, 0.4, Math.PI - 0.4));
    circ(g, 46, -590, 20, P.accent); circ(g, 46, -590, 7, OURO);
    g.restore();
  }
  // rosto em close dele. o.sorri 0..1, o.dentes, o.sombra, o.chapeu (false = sem), o.sy (chapéu sobe)
  function rostoEle(g, t, o = {}) {
    forma(g, BRANCO, q => { q.moveTo(-40, H); q.quadraticCurveTo(80, 1300, 380, 1250); q.lineTo(700, 1250); q.quadraticCurveTo(1000, 1300, 1120, H); });
    forma(g, P.accent, q => { q.moveTo(450, 1262); q.lineTo(630, 1262); q.lineTo(540, 1650); });
    curva(g, '#C9BBBA', 20, q => { q.moveTo(390, 1256); q.lineTo(540, 1600); q.lineTo(690, 1256); });
    rect(g, 450, 1130, 180, 150, PELE2); elipse(g, 540, 880, 300, 360, PELE); forma(g, PELE2, q => { q.moveTo(240, 880); q.quadraticCurveTo(270, 1160, 540, 1240); q.quadraticCurveTo(330, 1080, 320, 800); }, 0.7);
    const s = o.sorri ?? 1;
    for (const d of [-1, 1]) { const x = 540 + d * 120; curva(g, '#241014', 20, q => { q.moveTo(x - 66, 770 + (1 - s) * (d < 0 ? -18 : 22)); q.quadraticCurveTo(x, 730 + (1 - s) * 22, x + 66, 770 + (1 - s) * (d < 0 ? 22 : -18)); });
      elipse(g, x, 835, 52, lerp(26, 30, s), '#F4E6E0'); circ(g, x, 835, lerp(30, 24, s), '#16060E'); circ(g, x + 9, 825, lerp(3, 8, s), '#FFF'); curva(g, '#241014', 10, q => q.ellipse(x, 835, 54, lerp(26, 32, s), 0, Math.PI, TAU)); }
    curva(g, '#6A3428', 14, q => { q.moveTo(548, 870); q.lineTo(512, 985); q.lineTo(560, 995); });
    if (s > 0.5) { const w = 150 * s; forma(g, '#3A0A12', q => { q.moveTo(540 - w, 1055); q.quadraticCurveTo(540, 1075, 540 + w, 1055); q.quadraticCurveTo(540, 1055 + 150 * s, 540 - w, 1055); }); forma(g, '#FFF4EE', q => { q.moveTo(540 - w + 22, 1062); q.quadraticCurveTo(540, 1080, 540 + w - 22, 1062); q.quadraticCurveTo(540, 1112, 540 - w + 22, 1062); }); }
    else curva(g, '#3A0A12', 16, q => { q.moveTo(430, 1092); q.quadraticCurveTo(540, 1070 + s * 60, 650, 1092); });
    if (o.sombra) { g.save(); vgrad(g, 560, 960, 'rgba(13,4,20,0.92)', 'rgba(13,4,20,0)', 230, 620); g.restore(); for (const d of [-1, 1]) { circ(g, 540 + d * 120, 835, 8, P.accent); glow(g, 540 + d * 120, 835, 70, P.accent, 0.5); } }
    if (o.chapeu !== false) chapeu(g, 540, 610 - (o.sy || 0), 2.15, o.rot ?? -0.04);
  }
  function rostoEla(g, t, o = {}) {
    elipse(g, 520, 870, 420, 470, '#220A12'); rect(g, 455, 1110, 170, 190, PELE2); elipse(g, 545, 880, 290, 340, '#C78662');
    forma(g, '#220A12', q => { q.moveTo(230, 900); q.quadraticCurveTo(230, 450, 620, 510); q.quadraticCurveTo(860, 570, 850, 840); q.quadraticCurveTo(700, 610, 520, 650); q.quadraticCurveTo(330, 690, 230, 900); });
    forma(g, '#E0437A', q => { q.moveTo(0, H); q.quadraticCurveTo(200, 1260, 450, 1250); q.quadraticCurveTo(545, 1330, 640, 1250); q.quadraticCurveTo(900, 1270, W, H); });
    const ri = o.ri || 0, oy = o.olhar || [0, 0];
    for (const d of [-1, 1]) { const x = 545 + d * 115; curva(g, '#220A12', 14, q => { q.moveTo(x - 60, 765); q.quadraticCurveTo(x, 735 - (o.alerta ? 25 : 0), x + 60, 765); });
      if (ri) curva(g, '#220A12', 16, q => q.arc(x, 860, 46, Math.PI + 0.35, TAU - 0.35)); else { elipse(g, x, 838, 56, 38, '#FBF0EA'); circ(g, x + oy[0], 838 + oy[1], 27, '#3A1A12'); circ(g, x + oy[0], 838 + oy[1], 13, BREU); circ(g, x + oy[0] + 10, 826 + oy[1], 8, '#FFF'); curva(g, '#220A12', 11, q => q.ellipse(x, 838, 58, 40, 0, Math.PI, TAU)); } }
    curva(g, '#8A4A34', 11, q => { q.moveTo(552, 880); q.lineTo(528, 970); q.lineTo(566, 978); });
    if (ri) { const a = 60 + Math.abs(Math.sin(t * 11)) * 30; forma(g, '#4A0E1A', q => { q.moveTo(430, 1040); q.quadraticCurveTo(545, 1060, 660, 1040); q.quadraticCurveTo(545, 1055 + a * 2, 430, 1040); }); rect(g, 470, 1052, 150, 22, '#FFF4EE'); }
    else if (o.o) elipse(g, 545, 1065, 40, 34, '#4A0E1A'); else curva(g, '#8A1E34', 20, q => { q.moveTo(465, 1052); q.quadraticCurveTo(545, 1095, 625, 1052); });
    circ(g, 790, 600, 84, P.accent); for (let i = 0; i < 6; i++) circ(g, 790 + Math.cos(i) * 56, 600 + Math.sin(i * 1.05) * 56, 36, P.accent); circ(g, 790, 600, 28, OURO);
  }
  function arraial(g, t, o = {}) {
    const ap = o.ap ?? 1; ceu(g, t, 900); lua(g, 850, 300, 76); mata(g, 880, '#1C0824', 3); rio(g, t, 880, 1160, { reflexo: 850 });
    vgrad(g, 1160, H, '#4A1C2A', BREU); rect(g, 0, 1156, W, 10, '#8A3A4A', 0.7);
    for (const x of [50, 1030]) rect(g, x - 12, 420, 24, 800, '#2A0E1C'); bandeiras(g, t, 450, 1, ap); bandeiras(g, t + 1, 600, 0.75, ap); luzes(g, t, 430, ap);
  }

  // ───── cenários
  // o chapéu boiando junto à margem, amanhecer rosado (primeiro e último plano)
  CENARIOS.bt_boiando = (g, t) => {
    ceu(g, t, 620, { a: '#3A1650', b: '#F2A58A', estrelas: 0.25 }); circ(g, 540, 600, 110, '#FFE3C8'); glow(g, 540, 600, 600, '#FFC7A0', 0.4); mata(g, 625, '#3A1238', 11);
    rio(g, t, 625, H, { a: '#B8587A', b: '#1E0830', luz: '#FFD0C0', reflexo: 540 });
    const bx = 540 + Math.sin(t * 0.7) * 22, by = 1060 + Math.sin(t * 1.8) * 12;
    for (let i = 0; i < 4; i++) { const k = (t * 0.3 + i / 4) % 1; curva(g, '#FFE3D6', 6, q => q.ellipse(bx, by + 26, 210 + k * 330, 50 + k * 90, 0, 0, TAU), 0.6 * (1 - k)); }
    elipse(g, bx, by + 70, 200, 40, BREU, 0.4); chapeu(g, bx, by, 1.55, Math.sin(t * 1.3) * 0.06);
    forma(g, BREU, q => { q.moveTo(-20, 1520); q.quadraticCurveTo(250, 1470, 420, 1640); q.quadraticCurveTo(700, 1780, W + 20, 1700); q.lineTo(W + 20, H); q.lineTo(-20, H); });
    for (let i = 0; i < 26; i++) { const x = i < 13 ? 10 + i * 24 : 760 + (i - 13) * 26, y = i < 13 ? 1600 : 1780; curva(g, BREU, 9, q => { q.moveTo(x, y); q.quadraticCurveTo(x + 6, y - 100, x + Math.sin(t + i) * 22 + (rnd(i) - 0.5) * 60, y - 130 - rnd(i + 4) * 150); }); }
    vinheta(g, 0.55);
  };
  CENARIOS.bt_festa = (g, t) => { arraial(g, t); fogueira(g, t, 780, 1380, 1.1); for (const [x, s, f] of [[170, 0.62, 0], [350, 0.55, 1]]) moca(g, t + x, x, 1330, s, { gira: true, flip: f, braco: 'alto' }); rapazPar(g, t, 560, 1290, 0.5); vinheta(g, 0.55); };
  function rapazPar(g, t, x, y, s) { g.save(); g.globalAlpha = 1; moca(g, t + 2, x, y, s, { gira: true }); g.restore(); }
  CENARIOS.bt_danca = (g, t) => { arraial(g, t); fogueira(g, t, 190, 1330, 0.8); moca(g, t, 590 + Math.sin(t * 3) * 90, 1480, 1.35, { gira: true, braco: 'alto', flip: Math.sin(t * 3) < -0.6 }); for (let i = 0; i < 7; i++) { const u = (t * 0.4 + i / 7) % 1, x = 140 + rnd(i) * 800, y = 1000 - u * 400; circ(g, x, y, 16, OURO, 1 - u); line(g, x + 14, y, x + 14, y - 62, OURO, 6, 1 - u); } vinheta(g, 0.55); };
  CENARIOS.bt_chegada = (g, t, c = {}) => {
    ceu(g, t, 860); lua(g, 540, 520, 200); mata(g, 850, BREU, 21); rio(g, t, 850, 1250, { reflexo: 540 }); vgrad(g, 1250, H, '#3A1424', BREU);
    const k = out(clamp(t / 2.2)); for (let i = 0; i < 3; i++) curva(g, '#FFE3D6', 5, q => q.ellipse(540, 1250, 120 + i * 90 + t * 30, 18 + i * 12, 0, 0, TAU), 0.35 - i * 0.08);
    rapaz(g, t, 540, lerp(1180, 1370, k), lerp(0.7, 1.15, k)); bandeiras(g, t, 120, 1.1, 0.8); vinheta(g, 0.6);
  };
  CENARIOS.bt_rapaz = (g, t, c = {}) => {
    ceu(g, t, H, { a: '#22082E', b: c.sombra ? '#3A0C28' : '#8A2C58' }); if (!c.sombra) for (let i = 0; i < 14; i++) { const x = rnd(i + 70) * W, y = 200 + rnd(i + 33) * 1300; glow(g, x, y, 110, i % 3 ? OURO : ROSA, 0.25); circ(g, x, y, 22, OURO, 0.35); }
    rostoEle(g, t, { sorri: c.parou != null ? 1 - out(clamp((t - c.parou) / 0.45)) : c.sorri ?? 0.75, sombra: c.sombra, sy: c.brilho ? Math.max(0, Math.sin(t * 2)) * 6 : 0 }); vinheta(g, 0.6);
  };
  CENARIOS.bt_mao = (g, t) => {
    arraial(g, t); rapaz(g, t, 330, 1500, 1.5, { mao: true }); const k = out(clamp(t / 0.9)), x = lerp(1150, 700, k);
    curva(g, PELE, 66, q => { q.moveTo(1200, 1180); q.quadraticCurveTo(x + 220, 1060, x, 970); }); circ(g, x - 14, 962, 44, PELE); glow(g, 665, 950, 220, ROSA, 0.35 * k); vinheta(g, 0.6);
  };
  CENARIOS.bt_par = (g, t, c = {}) => {
    const parou = !!c.parou, u = parou ? 0 : t; arraial(g, u, { ap: parou ? 0.15 : 1 }); if (!parou) fogueira(g, t, 900, 1300, 0.6);
    const d = parou ? 0 : Math.sin(t * 3.2) * 110;
    moca(g, u, 400 + d, 1470, 1.12, { gira: !parou, braco: parou ? 'solto' : 'alto' }); rapaz(g, u, 710 + d, 1470, 1.18, { flip: true, mao: !parou });
    if (parou) { rect(g, 0, 0, W, H, '#12062A', 0.45); glow(g, 710, 750, 260, '#FFE3D6', 0.4); }
    vinheta(g, 0.6);
  };
  CENARIOS.bt_cheiro = (g, t) => {
    vgrad(g, 0, H, '#3A1050', '#0D0414'); rostoEle(g, t, { sorri: 0.7 });
    for (let i = 0; i < 7; i++) { const x = ((t * (90 + i * 14) + rnd(i) * 1300) % 1400) - 160, y = 330 + i * 190 + Math.sin(t * 2 + i) * 40, a = 0.55;
      elipse(g, x, y, 66, 28, ROSA, a); forma(g, ROSA, q => { q.moveTo(x - 56, y); q.lineTo(x - 110, y - 34); q.lineTo(x - 110, y + 34); }, a); circ(g, x + 36, y - 6, 6, BREU, 0.8); }
    for (let i = 0; i < 5; i++) curva(g, '#FFC0D0', 8, q => { const y0 = 1250 - i * 40; q.moveTo(0, y0 + i * 90); for (let x = 0; x <= W; x += 60) q.lineTo(x, y0 + i * 90 + Math.sin(x * 0.012 + t * 3 + i) * 28); }, 0.22);
    vinheta(g, 0.6);
  };
  CENARIOS.bt_ela = (g, t, c = {}) => {
    ceu(g, t, H, { a: '#2A0A38', b: '#7A2850' }); for (let i = 0; i < 12; i++) glow(g, rnd(i + 12) * W, 250 + rnd(i + 90) * 1200, 120, OURO, 0.22);
    if (c.reparou) chapeu(g, 880, 430, 0.9, 0.12);
    rostoEla(g, t, { ri: c.ri, olhar: c.reparou ? [20 * out(clamp(t / 0.7)), -16 * out(clamp(t / 0.7))] : [0, 0], alerta: c.reparou }); vinheta(g, 0.6);
  };
  CENARIOS.bt_beber = (g, t) => { arraial(g, t); rect(g, 0, 0, W, H, BREU, 0.3); const k = out(clamp(t / 0.6)); rapaz(g, t, 520, 1850, 2.1, { copo: true, rot: -0.05 * k }); vinheta(g, 0.62); };
  CENARIOS.bt_cochicho = (g, t) => {
    ceu(g, t, H, { a: '#1A0828', b: '#4A1438' }); rapaz(g, t, 880, 760, 0.55); glow(g, 880, 450, 220, ROSA, 0.3); bandeiras(g, t, 180, 0.9, 0.7);
    g.save(); g.translate(-90, 300); g.scale(0.82, 0.82); rostoEla(g, t, { olhar: [20, -8], alerta: true, o: false }); g.restore();
    const k = out(clamp(t / 0.7)), x = lerp(-420, 0, k);
    g.save(); g.translate(x, 0); elipse(g, 40, 1090, 260, 300, '#16060E'); elipse(g, 110, 1110, 180, 230, '#8A5038'); circ(g, 190, 1050, 17, BREU); curva(g, '#16060E', 12, q => { q.moveTo(140, 990); q.lineTo(235, 1005); }); elipse(g, 262, 1190, 20, 28 + Math.abs(Math.sin(t * 9)) * 12, '#4A0E1A');
    curva(g, '#A86448', 66, q => { q.moveTo(80, 1500); q.quadraticCurveTo(330, 1360, 320, 1150); }); g.restore(); vinheta(g, 0.65);
  };
  CENARIOS.bt_margem = (g, t, c = {}) => {
    ceu(g, t, 900, { a: '#0E0420', b: '#4A1848' }); lua(g, 540, 450, 170); mata(g, 890, BREU, 40); rio(g, t, 890, 1330, { reflexo: 540 }); forma(g, BREU, q => { q.moveTo(-20, 1300); q.quadraticCurveTo(540, 1250, W + 20, 1340); q.lineTo(W + 20, H); q.lineTo(-20, H); });
    const k = c.anda ? clamp(t / 3) : 1; moca(g, t, lerp(200, 380, k), 1330, 0.8, {}); rapaz(g, t, lerp(500, 710, k), 1335, 0.85, { flip: true });
    for (let i = 0; i < 20; i++) circ(g, rnd(i + 200) * W + Math.sin(t + i) * 30, 1100 + rnd(i + 300) * 500, 5, OURO, 0.3 + 0.5 * Math.abs(Math.sin(t * 2 + i)));
    vinheta(g, 0.6);
  };
  // a mão dela vai ao chapéu; c.puxaEm: o chapéu sai e o buraco aparece
  CENARIOS.bt_puxa = (g, t, c = {}) => {
    ceu(g, t, H, { a: '#12041E', b: '#4A1038' }); lua(g, 200, 330, 90);
    const k = out(clamp(t / (c.puxaEm ?? 1.2))), v = out(clamp((t - (c.puxaEm ?? 1.2)) / 0.35));
    rostoEle(g, t, { sorri: 0, chapeu: false });
    if (v > 0) { elipse(g, 540, 585, 150 * v, 52 * v, '#4A0A18'); elipse(g, 540, 592, 112 * v, 36 * v, BREU); glow(g, 540, 585, 330, P.accent, 0.4 * v); }
    const hx = 540 + v * 300, hy = 610 - v * 400; chapeu(g, hx, hy, 2.15, -0.04 + v * 0.55);
    const mx = lerp(1250, hx + 300, k), my = lerp(1200, hy + 10, k);
    curva(g, PELE2, 110, q => { q.moveTo(1250, 1250); q.quadraticCurveTo(1120, my + 220, mx, my); }); circ(g, mx - 10, my - 4, 72, '#C78662'); for (let i = 0; i < 3; i++) line(g, mx - 30, my - 44 + i * 42, mx - 120, my - 50 + i * 44, '#C78662', 34);
    vinheta(g, 0.62);
  };
  // o alto da cabeça: o buraco que respira. c.respira
  CENARIOS.bt_buraco = (g, t, c = {}) => {
    vgrad(g, 0, H, '#2A0830', BREU); const r = c.respira ? Math.sin(t * 3.4) : Math.sin(t * 1.2) * 0.2, ab = c.respira ? 1 : out(clamp(t / 0.8)), cy = 900;
    elipse(g, 540, 1010, 520, 640, PELE2); elipse(g, 540, 960, 470, 560, PELE);
    for (let i = 0; i < 110; i++) { const a = rnd(i) * TAU, d = 1.25 + rnd(i + 5) * 0.55, x = 540 + Math.cos(a) * 300 * d, y = cy + Math.sin(a) * 250 * d; curva(g, '#1C080E', 12, q => { q.moveTo(x, y); q.quadraticCurveTo(x + Math.cos(a) * 60 + 20, y + Math.sin(a) * 50, x + Math.cos(a) * 140, y + Math.sin(a) * 120); }); }
    const rx = (230 + r * 40) * ab, ry = (180 + r * 55) * ab;
    for (const [k, cor] of [[1.35, '#8A3A38'], [1.18, '#6A1A26'], [1, '#3A0612'], [0.76, '#1C020A'], [0.5, '#050004']]) elipse(g, 540, cy, rx * k, ry * k, cor);
    curva(g, '#C8606A', 9, q => q.ellipse(540, cy, rx * 1.18, ry * 1.18, 0, 0.3, 2.8), 0.7); glow(g, 540, cy, 420, P.accent, 0.14 + 0.18 * Math.max(0, r));
    if (c.respira) for (let i = 0; i < 26; i++) { const u = (t * 0.7 + rnd(i + 30)) % 1; circ(g, 540 + (rnd(i) - 0.5) * 200 + Math.sin(t * 2 + i) * 30 * u, cy - u * 620, 8 + u * 26, '#FFD8E0', 0.45 * (1 - u) * Math.max(0.15, -Math.cos(t * 3.4))); }
    vinheta(g, 0.68);
  };
  // manhã: o terreiro vazio, fogueira apagada, bandeiras caídas
  CENARIOS.bt_manha = (g, t) => {
    ceu(g, t, 780, { a: '#6A3A6A', b: '#F6B89A', estrelas: 0 }); circ(g, 800, 760, 90, '#FFE3C8'); mata(g, 780, '#4A1C42', 55); rio(g, t, 780, 1150, { a: '#C86A88', b: '#4A1C48', luz: '#FFD8C8', reflexo: 800 });
    vgrad(g, 1150, H, '#6A3040', '#1A0818'); for (const x of [90, 980]) rect(g, x - 12, 560, 24, 700, '#2A0E1C'); bandeiras(g, t * 0.3, 620, 2.2, 0.75);
    for (const d of [-1, 1]) line(g, 330 - 120 * d, 1420, 330 + 100 * d, 1370, '#1A0A10', 30); for (let i = 0; i < 3; i++) curva(g, '#E8D0D8', 14, q => { q.moveTo(310 + i * 28, 1350); for (let k = 1; k < 8; k++) q.lineTo(310 + i * 28 + Math.sin(t + k + i) * 24 + k * 10, 1350 - k * 55); }, 0.25);
    circ(g, 760, 1400, 34, P.accent); for (let i = 0; i < 5; i++) circ(g, 760 + Math.cos(i * 1.26) * 38, 1400 + Math.sin(i * 1.26) * 38, 22, P.accent); circ(g, 760, 1400, 14, OURO);
    vinheta(g, 0.55);
  };
})();
