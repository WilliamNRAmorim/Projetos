// Cenários dos Shorts soltos, semana 1 (30/11 em diante). Só ACRESCENTA ao Motor. Prefixo mt_ = Matinta Perera.
(() => {
  const { CENARIOS } = Motor, W = Motor.W, H = Motor.H, { rect, poly, circ, line, rrect, glow, vgrad, rgba, vinheta, rnd, lerp, clamp, out, P } = Motor.H_;
  const TAU = Math.PI * 2, SOMBRA = '#03040A';
  const elipse = (g, x, y, rx, ry, c, a = 1, rot = 0) => { g.globalAlpha = a; g.fillStyle = c; g.beginPath(); g.ellipse(x, y, rx, ry, rot, 0, TAU); g.fill(); g.globalAlpha = 1; };
  const forma = (g, c, fn, a = 1) => { g.globalAlpha = a; g.fillStyle = c; g.beginPath(); fn(g); g.closePath(); g.fill(); g.globalAlpha = 1; };

  // ave agourenta: silhueta de lado/frente; origem nos pés. asas 0..1, vira -1..1 (cabeça), olhos 0..1
  function ave(g, x, y, s, t, o = {}) {
    const asas = o.asas ?? 0, vira = o.vira ?? 0, cor = o.cor || SOMBRA, a = o.a ?? 1, resp = Math.sin(t * 3.1) * 4;
    g.save(); g.translate(x, y); g.scale(s, s);
    if (asas > 0.02) for (const e of [-1, 1]) { const bat = Math.sin(t * 7) * 30 * asas;
      forma(g, cor, q => { q.moveTo(e * 60, -230); q.quadraticCurveTo(e * (200 + 160 * asas), -470 - bat, e * (240 + 330 * asas), -400 - bat);
        for (let i = 0; i < 6; i++) { const k = i / 6; q.lineTo(e * (240 + 330 * asas - k * 330 * asas - 20), -300 - bat * (1 - k) + k * 150 + 70); q.lineTo(e * (240 + 330 * asas - (k + 0.1) * 360 * asas - 60), -320 - bat * (1 - k) + k * 150); }
        q.lineTo(e * 40, -90); }, a); }
    forma(g, cor, q => { q.moveTo(-40, -60); q.quadraticCurveTo(-160, 60, -300, 190); q.lineTo(-240, 180); q.lineTo(-262, 232); q.lineTo(-180, 170); q.lineTo(-170, 226); q.quadraticCurveTo(-80, 80, 30, -40); }, a); // cauda comprida
    elipse(g, 0, -150 - resp * 0.5, 118, 165, cor, a, 0.16);
    const hx = 30 + vira * 38, hy = -348 - resp;
    elipse(g, hx, hy, 92, 82, cor, a);
    for (let i = 0; i < 3; i++) forma(g, cor, q => { q.moveTo(hx - 50 + i * 28, hy - 62); q.quadraticCurveTo(hx - 110 + i * 22, hy - 150 - i * 18, hx - 150 + i * 30, hy - 168 - i * 26); q.quadraticCurveTo(hx - 70 + i * 28, hy - 120, hx - 10 + i * 26, hy - 74); }, a); // penacho
    const d = vira < -0.3 ? -1 : 1;
    forma(g, cor, q => { q.moveTo(hx + d * 66, hy - 34); q.quadraticCurveTo(hx + d * 178, hy - 20 - resp, hx + d * 172, hy + 46); q.quadraticCurveTo(hx + d * 138, hy + 12, hx + d * 72, hy + 26); }, a); // bico curvo
    for (const px of [-36, 34]) { line(g, px, -10, px + 6, 22, cor, 18, a); for (const dx of [-26, 4, 30]) line(g, px + 6, 22, px + 6 + dx, 38, cor, 9, a); }
    if (o.olhos > 0) for (const ex of [hx - 6, hx + 54]) { glow(g, ex, hy - 6, 70, P.accent, 0.6 * o.olhos); circ(g, ex, hy - 6, 13, P.accent, o.olhos); circ(g, ex + 2, hy - 6, 4, '#FFE2DA', o.olhos); }
    g.restore();
  }
  const acai = (g, x, base, h, t, cor, s = 1) => { const sw = Math.sin(t * 0.7 + x) * 10; g.strokeStyle = cor; g.lineWidth = 16 * s; g.lineCap = 'round'; g.beginPath(); g.moveTo(x, base); g.quadraticCurveTo(x + 30 * s, base - h * 0.5, x + sw, base - h); g.stroke();
    for (let i = 0; i < 8; i++) { const a = -Math.PI + i * Math.PI / 7, L = (150 + rnd(x + i) * 80) * s, tx = x + sw + Math.cos(a) * L, ty = base - h + Math.sin(a) * L * 0.5 + 90 * s * Math.abs(Math.cos(a)); g.lineWidth = 11 * s; g.beginPath(); g.moveTo(x + sw, base - h); g.quadraticCurveTo(x + sw + Math.cos(a) * L * 0.6, base - h + Math.sin(a) * L * 0.7 - 30 * s, tx, ty); g.stroke(); } };
  const lua = (g, x, y, r, ceu) => { glow(g, x, y, r * 5, '#B9C6F0', 0.28); circ(g, x, y, r, '#E6E9F5'); circ(g, x - r * 0.3, y - r * 0.2, r * 0.18, '#C5CBE0', 0.7); circ(g, x + r * 0.25, y + r * 0.3, r * 0.26, '#C5CBE0', 0.6); };
  const estrelas = (g, t, n, y1) => { for (let i = 0; i < n; i++) circ(g, rnd(i + 1) * W, rnd(i + 57) * y1, 1.5 + rnd(i + 9) * 2, '#E6E9F5', 0.15 + 0.5 * rnd(i + 3) * (0.7 + 0.3 * Math.sin(t * 2 + i))); };

  // ───── telhado: telhas de barro, lua e a sombra da ave. c.olhos, c.asas, c.canta (ondas do assobio, s), c.vazio, c.e (escala), c.x
  CENARIOS.mt_telhado = (g, t, c = {}) => {
    vgrad(g, 0, 900, '#050817', '#1B2652'); estrelas(g, t, 60, 640); lua(g, c.luaX ?? 790, 520, 190);
    for (const [x, h, s] of [[70, 480, 1], [1010, 400, 0.9], [210, 300, 0.7]]) acai(g, x, 940, h, t, '#04060F', s);
    const topo = 800; rect(g, 0, topo - 18, W, 36, '#1A0E12');
    for (let r = 0; r < 13; r++) { const y = topo + Math.pow(r, 1.18) * 62, hh = 90 + r * 9, w = 92 + r * 10, off = (r % 2) * w / 2;
      for (let x = -w + off; x < W + w; x += w) { const k = clamp(1 - Math.hypot(x - 620, (y - 1000) * 0.9) / 900), v = rnd(r * 31 + Math.round(x)) * 10;
        const cor = `rgb(${Math.round(28 + 96 * k + v)},${Math.round(20 + 60 * k + v * 0.5)},${Math.round(34 + 62 * k)})`;
        forma(g, cor, q => { q.moveTo(x + 4, y); q.lineTo(x + w - 4, y); q.lineTo(x + w - 4, y + hh - w * 0.35); q.quadraticCurveTo(x + w / 2, y + hh + w * 0.18, x + 4, y + hh - w * 0.35); });
        line(g, x + w * 0.34, y + 14, x + w * 0.34, y + hh - w * 0.4, 'rgba(255,220,220,0.07)', w * 0.16); g.strokeStyle = 'rgba(0,0,0,0.55)'; g.lineWidth = 8; g.beginPath(); g.moveTo(x + 4, y + hh - w * 0.35); g.quadraticCurveTo(x + w / 2, y + hh + w * 0.18, x + w - 4, y + hh - w * 0.35); g.stroke(); } rect(g, 0, y + 4, W, 7, 'rgba(0,0,0,0.22)'); }
    rect(g, 0, topo + 6, W, 10, 'rgba(0,0,0,0.45)');
    if (!c.vazio) {
      const x = (c.x ?? 540) + Math.sin(t * 0.6) * 8, s = c.e ?? 1.25, y = c.y ?? 1190, chega = c.chega ? out(clamp(t / c.chega)) : 1;
      g.save(); g.translate(x, y); g.transform(1, 0, -0.16, 1.08, 0, 0); // sombra deitada nas telhas
      for (const [dx, dy, a] of [[-14, 10, 0.25], [14, -8, 0.25], [0, 0, 0.93]]) ave(g, dx, dy - (1 - chega) * 500, s, t, { a, asas: c.asas ? c.asas * (0.75 + 0.25 * Math.sin(t * 2.4)) : 0, vira: c.vira ?? Math.sin(t * 1.1) * 0.35 });
      if (c.olhos) ave(g, 0, -(1 - chega) * 500, s, t, { a: 0, olhos: out(clamp((t - (c.olhosEm || 0)) / 0.5)), vira: c.vira ?? Math.sin(t * 1.1) * 0.35 });
      g.restore();
    }
    if (c.canta != null) { const bx = (c.x ?? 540) + 190, by = (c.y ?? 1190) - 360 * (c.e ?? 1.25); for (const ini of [].concat(c.canta)) { const u = t - ini; if (u < 0 || u > 1.1) continue; for (let i = 0; i < 3; i++) { const k = clamp(u * 1.3 - i * 0.18); if (k <= 0 || k >= 1) continue; g.globalAlpha = (1 - k) * 0.8; g.strokeStyle = '#E6E9F5'; g.lineWidth = 9; g.beginPath(); g.arc(bx, by, 60 + k * 360, -0.75, 0.45); g.stroke(); g.globalAlpha = 1; } } }
    vinheta(g, 0.5);
  };

  // ───── casa de madeira sobre estacas, na beira do rio (Pará)
  CENARIOS.mt_casa = (g, t, c = {}) => {
    vgrad(g, 0, 1000, '#070B1C', '#28356A'); estrelas(g, t, 50, 600); lua(g, 230, 430, 110);
    for (let i = 0; i < 14; i++) acai(g, i * 88 - 20, 1030, 260 + rnd(i + 4) * 230, t, '#081020', 0.7);
    vgrad(g, 1030, H, '#16224A', '#04060F');
    for (let i = 0; i < 24; i++) { const y = 1060 + i * 36, w = 60 + rnd(i) * 150; rect(g, 230 - w / 2 + Math.sin(t * 1.4 + i) * 18, y, w, 5, '#C9D4F5', 0.35 * (1 - i / 28)); }
    for (let i = 0; i < 6; i++) { rect(g, 420 + i * 108, 1130, 22, 300, '#0C0A12'); rect(g, 420 + i * 108, 1360, 22, 150, '#0C0A12', 0.35); }
    rect(g, 390, 1100, 640, 42, '#2A1D1A'); rect(g, 440, 780, 540, 320, '#33231F'); for (let x = 452; x < 980; x += 40) rect(g, x, 780, 4, 320, '#1C1211');
    poly(g, [[390, 800], [710, 570], [1030, 800]], '#190F14'); for (let i = 1; i < 6; i++) line(g, 390 + i * 40, 800 - i * 2, 710, 580 + i * 36, 'rgba(255,255,255,0.05)', 4);
    const f = 0.85 + 0.15 * Math.sin(t * 9) * Math.sin(t * 3.7);
    rect(g, 540, 870, 150, 160, '#0E0908'); rect(g, 552, 882, 126, 136, '#FFB45A', 0.85 * f); rect(g, 610, 882, 10, 136, '#0E0908'); rect(g, 552, 944, 126, 10, '#0E0908'); glow(g, 615, 950, 330, '#FFB45A', 0.35 * f);
    rect(g, 780, 870, 130, 230, '#150D0C'); for (let i = 0; i < 4; i++) rect(g, 790, 1142 + i * 46, 110, 14, '#22171A');
    if (c.sombra !== false) ave(g, 760, 690, 0.42, t, { vira: Math.sin(t) * 0.4, olhos: c.olhos ? 1 : 0 });
    vinheta(g, 0.55);
  };

  // ───── cozinha de tábua com fogão de barro e lamparina. c.dia
  CENARIOS.mt_cozinha = (g, t, c = {}) => {
    const d = !!c.dia, f = 0.85 + 0.15 * Math.sin(t * 11) * Math.sin(t * 4.3);
    vgrad(g, 0, 1240, d ? '#6A5A52' : '#2E1B14', d ? '#46362F' : '#170D0A');
    for (let x = 0; x < W; x += 98) { rect(g, x, 0, 7, 1240, 'rgba(0,0,0,0.35)'); rect(g, x + 9, 0, 3, 1240, 'rgba(255,220,180,0.06)'); for (let k = 0; k < 3; k++) circ(g, x + 30 + rnd(x + k) * 40, rnd(x + k + 5) * 1100, 6, 'rgba(0,0,0,0.3)'); }
    rect(g, 70, 360, 330, 360, '#120A08'); vgrad(g, 378, 702, d ? '#CFE0E8' : '#0B1430', d ? '#9DB8A8' : '#1B2A55', 88, 294); if (!d) { circ(g, 300, 450, 34, '#E6E9F5'); acai(g, 160, 702, 190, t, '#050914', 0.5); } else acai(g, 160, 702, 190, t, '#35503A', 0.5); rect(g, 230, 378, 10, 324, '#120A08'); rect(g, 88, 536, 294, 10, '#120A08');
    rect(g, 640, 470, 440, 20, '#150C08'); for (let i = 0; i < 4; i++) { rrect(g, 670 + i * 100, 400 - (i % 2) * 20, 68, 70 + (i % 2) * 20, 18, ['#5A3A28', '#3A2A22', '#6A4A30', '#44302A'][i]); }
    rect(g, 660, 960, 420, 280, '#5A2E1E'); rect(g, 640, 940, 440, 34, '#74422A'); rect(g, 760, 1060, 150, 110, '#0A0504');
    for (let i = 0; i < 5; i++) { const x = 778 + i * 28, h = 44 + 34 * Math.abs(Math.sin(t * (6 + i) + i * 2)); forma(g, i % 2 ? '#FF9A2E' : '#FF5A22', q => { q.moveTo(x - 20, 1170); q.quadraticCurveTo(x - 8, 1170 - h * 0.6, x, 1170 - h); q.quadraticCurveTo(x + 12, 1170 - h * 0.5, x + 20, 1170); }); }
    glow(g, 835, 1130, 520, '#FF7A2A', (d ? 0.18 : 0.34) * f); rrect(g, 720, 860, 120, 84, 30, '#17100E'); rect(g, 710, 856, 140, 14, '#241A16');
    line(g, 520, 0, 520, 560, '#0E0806', 5); rrect(g, 488, 600, 64, 60, 12, '#3A2A1A'); forma(g, '#FFD98A', q => { q.moveTo(520, 548 - 10 * f); q.quadraticCurveTo(546, 590, 520, 606); q.quadraticCurveTo(494, 590, 520, 548 - 10 * f); }); glow(g, 520, 590, 620, '#FFB45A', (d ? 0.15 : 0.3) * f);
    vgrad(g, 1240, H, '#22140E', '#0A0605'); for (let y = 1280; y < H; y += 92) rect(g, 0, y, W, 4, '#080403');
    vinheta(g, 0.55);
  };

  // ───── de baixo para cima: caibros e telhas, luar pelas frestas. c.passa (a sombra atravessa em s), c.pousa (fica), c.olhosEm
  CENARIOS.mt_forro = (g, t, c = {}) => {
    vgrad(g, 0, H, '#0D1230', '#05060F'); const vx = 540, vy = 520;
    for (let r = 0; r < 18; r++) { const y = 40 + r * 112; for (let x = -60 + (r % 2) * 70; x < W + 60; x += 140) { rrect(g, x, y, 132, 96, 44, rnd(r * 17 + x) > 0.5 ? '#2A2038' : '#241A30'); rect(g, x + 14, y + 84, 104, 10, 'rgba(0,0,0,0.5)'); if (rnd(r * 13 + x * 3) > 0.9) { rect(g, x + 18, y + 94, 96, 14, '#C9D4F5', 0.8); glow(g, x + 66, y + 100, 130, '#9DB0F0', 0.22); } } }
    glow(g, vx, 900, 760, '#8FA4F0', 0.32);
    if (c.pousa || c.passa) { const k = c.passa ? clamp((t - (c.passaEm || 0)) / c.passa) : 1, x = c.passa ? lerp(-420, W + 420, k) : 540 + Math.sin(t * 0.8) * 20, y = c.passa ? 1080 - Math.sin(k * Math.PI) * 250 : 1040;
      for (const [dx, a] of [[-26, 0.28], [26, 0.28], [0, 0.92]]) ave(g, x + dx, y, c.e ?? 1.35, t, { a, asas: c.passa ? 1 : 0.12, vira: Math.sin(t * 1.3) * 0.5 });
      if (c.olhosEm != null && t >= c.olhosEm) ave(g, x, y, c.e ?? 1.35, t, { a: 0, olhos: out(clamp((t - c.olhosEm) / 0.35)), vira: Math.sin(t * 1.3) * 0.5 }); }
    for (const x of [-420, 120, 960, 1500]) poly(g, [[x - 46, H + 60], [x + 46, H + 60], [vx + (x - vx) * 0.22 + 12, vy - 520], [vx + (x - vx) * 0.22 - 12, vy - 520]], '#0B070C');
    for (const y of [300, 1560]) { rect(g, 0, y, W, y > 900 ? 70 : 40, '#0B070C'); rect(g, 0, y, W, 6, 'rgba(160,180,255,0.14)'); }
    vinheta(g, 0.6);
  };

  // velha de costas: curvada, lenço, xale, saia comprida, bengala; origem nos pés
  function velha(g, x, y, s, t, o = {}) {
    const cor = o.cor || '#07060A', passo = o.anda ? Math.sin(t * 5.2) : 0; g.save(); g.translate(x, y - Math.abs(passo) * 8); g.scale(s, s); g.rotate(passo * 0.025);
    for (const e of [-1, 1]) elipse(g, e * 46, -6 - (o.anda ? Math.max(0, passo * e) * 22 : 0), 38, 16, cor);
    forma(g, cor, q => { q.moveTo(-96, -330); q.quadraticCurveTo(-130, -160, -150, -20); q.quadraticCurveTo(0, 6, 150, -20); q.quadraticCurveTo(130, -170, 100, -330); });
    forma(g, cor, q => { q.moveTo(-112, -300); q.quadraticCurveTo(-150, -470, -66, -524); q.quadraticCurveTo(10, -572, 92, -514); q.quadraticCurveTo(160, -440, 112, -300); q.lineTo(70, -240); q.lineTo(34, -296); q.lineTo(0, -216); q.lineTo(-40, -292); q.lineTo(-80, -246); }); // corcunda e xale de franjas
    elipse(g, 30, -540, 72, 70, cor); forma(g, cor, q => { q.moveTo(-40, -566); q.quadraticCurveTo(10, -650, 96, -586); q.quadraticCurveTo(122, -540, 98, -490); q.lineTo(120, -430); q.lineTo(62, -486); }); // lenço amarrado
    line(g, 112, -380, 186, -300, cor, 40); line(g, 192, -330, 214, 0, '#150E0A', 17); circ(g, 188, -306, 20, '#3A2A24');
    if (o.pacote) { rrect(g, -196, -318, 96, 80, 6, '#8A6A44'); line(g, -148, -318, -148, -238, '#3A2616', 6); line(g, -196, -278, -100, -278, '#3A2616', 6); line(g, -110, -360, -140, -286, cor, 36); }
    if (o.luz) { g.strokeStyle = rgba(o.luz, 0.7); g.lineWidth = 6; g.lineCap = 'round'; g.beginPath(); g.moveTo(-138, -90); g.quadraticCurveTo(-110, -230, -112, -300); g.quadraticCurveTo(-150, -470, -66, -524); g.stroke(); g.beginPath(); g.arc(30, -540, 78, Math.PI * 1.05, Math.PI * 1.75); g.stroke(); }
    g.restore();
  }

  // ───── a porta por dentro. c.abre (s para abrir), c.abreEm, c.manha, c.velha, c.pacoteEm (ela passa a ter o pacote)
  CENARIOS.mt_porta = (g, t, c = {}) => {
    const m = !!c.manha, ab = c.abre ? out(clamp((t - (c.abreEm || 0)) / c.abre)) : 1, x0 = 250, x1 = 830, y0 = 420, y1 = 1300;
    vgrad(g, 0, 1300, m ? '#3A2A22' : '#1E120E', '#0E0807'); for (let x = 0; x < W; x += 98) rect(g, x, 0, 7, 1300, 'rgba(0,0,0,0.4)');
    vgrad(g, 1300, H, '#1C110C', '#080504'); for (let y = 1340; y < H; y += 92) rect(g, 0, y, W, 4, '#060302');
    rect(g, x0 - 34, y0 - 34, x1 - x0 + 68, y1 - y0 + 34, '#3A2418');
    g.save(); g.beginPath(); g.rect(x0, y0, x1 - x0, y1 - y0); g.clip();
    if (m) { vgrad(g, y0, 1080, '#F2C98A', '#E8E4C8'); glow(g, 540, 780, 520, '#FFF3C8', 0.75); for (let i = 0; i < 9; i++) acai(g, x0 + i * 74, 1140, 200 + rnd(i) * 160, t, '#6A7A4A', 0.55); vgrad(g, 1080, y1, '#B89A68', '#8A6A44'); }
    else { vgrad(g, y0, y1, '#080D22', '#1E2C5C'); estrelas(g, t, 30, 800); for (let i = 0; i < 8; i++) acai(g, x0 + i * 84, 1150, 220 + rnd(i) * 200, t, '#04070F', 0.6); rect(g, x0, 1120, x1 - x0, y1 - 1120, '#060914'); if (c.olhos) for (const dx of [0, 54]) { circ(g, 640 + dx, 690, 8, P.accent); glow(g, 640 + dx, 690, 46, P.accent, 0.6); } }
    if (c.velha) velha(g, 530, 1285, c.velhaE ?? 1.22, t, { pacote: c.pacoteEm != null && t >= c.pacoteEm, luz: '#FFE4A8' });
    g.restore();
    const larg = (x1 - x0) * (1 - 0.86 * ab); poly(g, [[x0, y0], [x0 + larg, y0 + 40 * ab], [x0 + larg, y1 - 30 * ab], [x0, y1]], '#2A1A12'); for (let i = 1; i < 5; i++) line(g, x0 + larg * i / 5, y0 + 20, x0 + larg * i / 5, y1 - 20, 'rgba(0,0,0,0.45)', 5); circ(g, x0 + larg * 0.82, 900, 13 * (0.4 + 0.6 * (1 - ab)), '#8A6A3A');
    if (c.pes) { rect(g, x0, y1 - 16, x1 - x0, 20, '#FFE4A8', 0.95); glow(g, 540, y1, 420, '#FFE4A8', 0.35); for (const dx of [-74, 62]) rect(g, 540 + dx - 36 + Math.sin(t * 1.3) * 6, y1 - 17, 72, 22, '#0A0604'); }
    poly(g, [[x0 + larg, y1], [x1, y1], [x1 + 240, H], [x0 - 180, H]], m ? '#FFE4A8' : '#8FA4F0', (m ? 0.3 : 0.12) * ab);
    vinheta(g, m ? 0.45 : 0.55);
  };

  // ───── o pacote de fumo na mesa; c.maoEm = a mão enrugada entra e leva
  CENARIOS.mt_fumo = (g, t, c = {}) => {
    vgrad(g, 0, H, '#7A5434', '#2A1A10'); for (let i = 0; i < 12; i++) { const y = i * 170 + 40; rect(g, 0, y, W, 8, '#1C1008', 0.6); for (let k = 0; k < 7; k++) line(g, rnd(i * 9 + k) * W, y + 20 + k * 20, rnd(i * 9 + k) * W + 220, y + 26 + k * 20, 'rgba(0,0,0,0.2)', 3); }
    poly(g, [[0, 0], [620, 0], [W, 900], [W, 1400]], '#FFE4A8', 0.16); glow(g, 300, 420, 900, '#FFD98A', 0.28);
    const u = c.maoEm != null ? t - c.maoEm : -1, leva = u > 0.9 ? Math.pow(clamp((u - 0.9) / 1.2), 2) : 0;
    g.save(); g.translate(540 + leva * 760, 930 - leva * 420); g.rotate(-0.16 + leva * 0.2);
    rrect(g, -270, -150, 580, 360, 20, '#000', 0.4); rrect(g, -300, -190, 580, 360, 14, '#B8925E'); poly(g, [[-300, -190], [-10, -20], [280, -190]], '#C9A674'); line(g, -300, -190, -10, -20, 'rgba(60,35,10,0.5)', 5); line(g, 280, -190, -10, -20, 'rgba(60,35,10,0.5)', 5);
    for (let i = 0; i < 7; i++) { g.strokeStyle = i % 2 ? '#2E1A0A' : '#4A2A10'; g.lineWidth = 34; g.beginPath(); g.ellipse(-40, 50, 190 - i * 24, 90 - i * 11, 0.1, 0, TAU); g.stroke(); } // fumo de corda enrolado
    line(g, -80, -192, -110, 172, '#E8DCC0', 12); line(g, -302, 0, 282, -26, '#E8DCC0', 12); circ(g, -92, -14, 18, '#E8DCC0');
    g.restore();
    if (u > 0) { const e = out(clamp(u / 0.8)), mx = lerp(1500, 760, e) + leva * 760, my = lerp(380, 880, e) - leva * 420; g.save(); g.translate(mx, my); g.rotate(-0.32);
      line(g, 130, -20, 900, -140, '#141018', 230); line(g, 90, -10, 190, -30, '#8A6248', 150); elipse(g, 40, 0, 110, 92, '#9A7050');
      [[-170, -66, 50], [-215, -6, 54], [-195, 56, 50]].forEach(([fx, fy, w]) => { line(g, 10, fy * 0.7, fx * 0.62, fy, '#9A7050', w); line(g, fx * 0.62, fy, fx, fy + 26, '#9A7050', w * 0.8); circ(g, fx * 0.62, fy, w * 0.3, '#7A5038', 0.7); elipse(g, fx - 6, fy + 30, 20, 11, '#C9B09A', 1, -0.5); });
      line(g, -30, 78, -110, 118, '#9A7050', 54); for (let i = 0; i < 4; i++) line(g, 10 + i * 16, -50 + i * 8, 30 + i * 14, 40, 'rgba(60,30,20,0.45)', 4); g.restore(); }
    vinheta(g, 0.6);
  };

  // ───── caminho de manhã: a velha vai embora e a sombra dela no chão é a de uma ave
  CENARIOS.mt_caminho = (g, t, c = {}) => {
    vgrad(g, 0, 920, '#7A7F9A', '#F2C48A'); glow(g, 540, 860, 640, '#FFF0C0', 0.65); circ(g, 540, 850, 110, '#FFF0CC', 0.85);
    for (let i = 0; i < 12; i++) { const x = i < 6 ? i * 70 - 30 : 700 + (i - 6) * 80; acai(g, x, 960, 330 + rnd(i + 2) * 300, t, i % 2 ? '#3A4430' : '#242C20', 0.85); }
    vgrad(g, 900, H, '#8A7048', '#2A1E12'); poly(g, [[470, 900], [610, 900], [1060, H], [20, H]], '#B89464'); for (let i = 0; i < 90; i++) { const d = rnd(i + 3), y = 920 + d * d * 1000; circ(g, 540 + (rnd(i + 30) - 0.5) * (150 + d * 900), y, 3 + d * 16, 'rgba(60,40,20,0.35)'); }
    const k = clamp(t / (c.dura || 6)), y = lerp(1430, 1130, k), s = lerp(1.15, 0.62, k);
    g.save(); g.translate(540, y - 4); g.transform(1, 0, 0.35, -0.9, 0, 0); ave(g, 0, 0, s * 1.2, t, { a: c.sombra === false ? 0 : 0.62, cor: '#1A0E08', asas: 0.35 * out(clamp((t - 1.2) / 1.2)), vira: 0.3 }); g.restore(); // sombra projetada para a frente
    velha(g, 540, y, s, t, { anda: true, pacote: true, luz: '#FFE4A8' });
    vinheta(g, 0.5);
  };

  // ───── close do menino na cama, olhos abertos no escuro; c.reflexo = a ave refletida nos olhos
  CENARIOS.mt_olhos = (g, t, c = {}) => {
    vgrad(g, 0, H, '#10163A', '#060814'); glow(g, 880, 380, 900, '#8FA4F0', 0.22);
    elipse(g, 540, 640, 620, 330, '#8C9AC8'); elipse(g, 540, 600, 540, 250, '#AAB6DE', 0.6);
    elipse(g, 540, 900, 400, 440, '#8A6A6A'); elipse(g, 575, 880, 360, 415, '#A8827A');
    forma(g, '#161016', q => { q.moveTo(130, 830); q.quadraticCurveTo(120, 400, 540, 410); q.quadraticCurveTo(980, 420, 950, 860); q.quadraticCurveTo(870, 620, 760, 640); q.lineTo(700, 700); q.lineTo(640, 610); q.lineTo(540, 690); q.lineTo(470, 600); q.lineTo(370, 690); q.quadraticCurveTo(220, 640, 130, 830); });
    const per = 3.4, k = (t + 1.2) % per, pisca = c.semPiscar ? 0 : k < 0.16 ? Math.sin(k / 0.16 * Math.PI) : 0, olhar = Math.sin(t * 0.9) * 16 * (c.parado ? 0 : 1);
    for (const ex of [375, 705]) { const ry = 96 * (1 - 0.95 * pisca);
      line(g, ex - 110, 748, ex + 110, 742 + (ex < 540 ? -26 : 26), '#1C1216', 26);
      g.save(); g.beginPath(); g.ellipse(ex, 862, 122, Math.max(4, ry), 0, 0, TAU); g.clip(); rect(g, ex - 140, 740, 280, 240, '#E4E6F0'); circ(g, ex + olhar, 866, 66, '#3A2418'); circ(g, ex + olhar, 866, 34, '#060406');
      if (c.reflexo) ave(g, ex + olhar - 12, 890, 0.13, t, { cor: '#C9D4F5', a: out(clamp((t - (c.reflexoEm || 0)) / 0.5)), asas: 0.4 });
      circ(g, ex + olhar + 28, 836, 15, '#FFF'); g.restore();
      g.strokeStyle = '#1C1014'; g.lineWidth = 13; g.beginPath(); g.ellipse(ex, 862, 122, Math.max(4, ry), 0, Math.PI, TAU); g.stroke(); }
    line(g, 545, 930, 520, 1040, 'rgba(60,30,30,0.5)', 16); line(g, 520, 1040, 565, 1052, 'rgba(60,30,30,0.5)', 14);
    line(g, 478, 1130, 600, 1126, '#3A1C20', 18);
    forma(g, '#27386A', q => { q.moveTo(-60, 1330); q.quadraticCurveTo(300, 1160, 540, 1215); q.quadraticCurveTo(800, 1160, W + 60, 1320); q.lineTo(W + 60, H + 60); q.lineTo(-60, H + 60); });
    for (let i = 0; i < 5; i++) line(g, 80 + i * 230, 1340, i * 270, H, 'rgba(0,0,0,0.25)', 16);
    for (const x of [300, 780]) { for (let i = 0; i < 4; i++) rrect(g, x - 70 + i * 36, 1210 + (i % 3 ? 0 : 14), 32, 80, 15, '#A8827A'); }
    vinheta(g, 0.62);
  };

  // ───── quarto do menino: parede de tábua, janela com lua, cama
  CENARIOS.mt_quarto = (g, t, c = {}) => {
    vgrad(g, 0, 1240, '#1C2450', '#0C0F24'); for (let x = 0; x < W; x += 98) rect(g, x, 0, 7, 1240, 'rgba(0,0,0,0.35)');
    rect(g, 620, 330, 360, 440, '#0A0710'); vgrad(g, 350, 750, '#101C46', '#33467E', 640, 320); circ(g, 850, 460, 62, '#E6E9F5'); glow(g, 850, 460, 420, '#B9C6F0', 0.3); acai(g, 700, 750, 250, t, '#050914', 0.6);
    if (c.sombraJanela) { g.save(); g.beginPath(); g.rect(640, 350, 320, 400); g.clip(); ave(g, 800 + Math.sin(t * 0.7) * 14, 740, 0.62, t, { vira: -0.6, olhos: c.olhos ? 1 : 0 }); g.restore(); }
    rect(g, 796, 350, 10, 400, '#0A0710'); rect(g, 640, 545, 320, 10, '#0A0710');
    poly(g, [[640, 770], [960, 770], [820, 1500], [260, 1500]], '#9DB0F0', 0.08);
    vgrad(g, 1240, H, '#151022', '#06040A'); for (let y = 1280; y < H; y += 92) rect(g, 0, y, W, 4, '#05030A');
    rect(g, 0, 930, 46, 330, '#1A100E'); rect(g, 0, 1070, 400, 100, '#5A6AA0'); rrect(g, 56, 1010, 190, 76, 30, '#B8C2E4'); rect(g, 0, 1160, 400, 40, '#241612'); rect(g, 360, 1160, 30, 120, '#1A100E');
    vinheta(g, 0.55);
  };

  // ───── o retrato da avó: o rosto e o nome vão sumindo (c.de, c.apagaEm, c.dura)
  CENARIOS.mt_retrato = (g, t, c = {}) => {
    vgrad(g, 0, H, '#3A2820', '#120B09'); g.save(); g.translate(0, -220); for (let x = 0; x < W; x += 98) rect(g, x, 0, 7, H, 'rgba(0,0,0,0.35)'); glow(g, 300, 500, 900, '#FFB45A', 0.2);
    const k = clamp((t - (c.apagaEm ?? 0.8)) / (c.dura ?? 3.2)), a = 1 - k;
    rect(g, 190, 430, 740, 960, '#000', 0.45); rect(g, 160, 390, 760, 960, '#4A2E18'); rect(g, 188, 418, 704, 904, '#8A6A3A'); rect(g, 212, 442, 656, 856, '#CBB48C');
    g.save(); g.beginPath(); g.rect(212, 442, 656, 856); g.clip(); glow(g, 540, 700, 520, '#EFE0BC', 0.8);
    forma(g, '#4A3426', q => { q.moveTo(230, 1310); q.quadraticCurveTo(260, 1030, 440, 990); q.lineTo(640, 990); q.quadraticCurveTo(820, 1030, 850, 1310); }); poly(g, [[480, 990], [600, 990], [540, 1090]], '#E4D6B4'); circ(g, 540, 1112, 18, '#8A6A3A');
    circ(g, 540, 560, 84, '#7A6A5A'); elipse(g, 540, 790, 196, 220, '#A8825E'); rect(g, 490, 960, 100, 50, '#A8825E');
    forma(g, '#8C7C6A', q => { q.moveTo(340, 810); q.quadraticCurveTo(320, 540, 540, 545); q.quadraticCurveTo(765, 540, 740, 815); q.quadraticCurveTo(700, 660, 560, 640); q.quadraticCurveTo(390, 650, 340, 810); });
    // traços grandes e contrastados (lidos em tela de celular); tudo com o mesmo alfa para sumir junto
    const tinta = '#1E100A', traco = (c, lw, fn, al = 1) => { g.globalAlpha = a * al; g.strokeStyle = c; g.lineWidth = lw; g.lineCap = 'round'; g.lineJoin = 'round'; g.beginPath(); fn(g); g.stroke(); g.globalAlpha = 1; };
    for (const ex of [450, 630]) { const d = ex < 540 ? -1 : 1;
      elipse(g, ex, 786, 40, 24, '#F4EBD6', a); circ(g, ex, 788, 19, '#3A2214', a); circ(g, ex, 788, 10, '#050302', a); circ(g, ex + 7, 781, 5, '#FFFFFF', a);
      traco(tinta, 9, q => { q.moveTo(ex - 42, 786); q.quadraticCurveTo(ex, 748, ex + 42, 786); }); traco(tinta, 4, q => { q.moveTo(ex - 36, 796); q.quadraticCurveTo(ex, 820, ex + 36, 796); }); // pálpebras
      traco('#4A3A2E', 15, q => { q.moveTo(ex - 50, 722 + (d < 0 ? 8 : 0)); q.quadraticCurveTo(ex, 698, ex + 50, 722 + (d > 0 ? 8 : 0)); }); // sobrancelha
      traco(tinta, 10, q => q.arc(ex, 790, 70, 0, TAU)); traco(tinta, 8, q => { q.moveTo(ex + d * 70, 778); q.lineTo(ex + d * 150, 756); }); traco('#FFFFFF', 7, q => q.arc(ex, 790, 55, Math.PI * 1.1, Math.PI * 1.4), 0.55); // óculos, haste e reflexo
      traco('#6A4630', 4, q => { q.moveTo(ex + d * 62, 866); q.quadraticCurveTo(ex + d * 20, 884, ex - d * 14, 872); }, 0.6); } // olheira
    traco(tinta, 10, q => { q.moveTo(520, 778); q.quadraticCurveTo(540, 762, 560, 778); }); // ponte
    traco(tinta, 8, q => { q.moveTo(548, 806); q.quadraticCurveTo(556, 850, 576, 882); q.quadraticCurveTo(560, 904, 540, 892); q.quadraticCurveTo(520, 904, 504, 886); }); // nariz
    for (const d of [-1, 1]) traco('#6A4630', 5, q => { q.moveTo(540 + d * 56, 886); q.quadraticCurveTo(540 + d * 94, 920, 540 + d * 94, 958); }, 0.75); // vincos
    forma(g, '#6E241C', q => { q.moveTo(462, 934); q.quadraticCurveTo(505, 914, 540, 927); q.quadraticCurveTo(575, 914, 618, 934); q.quadraticCurveTo(540, 990, 462, 934); }, a); traco(tinta, 7, q => { q.moveTo(456, 931); q.quadraticCurveTo(540, 958, 624, 931); }); // boca
    for (let i = 0; i < 46; i++) { const q = clamp(k * 1.6 - rnd(i + 8) * 0.6); if (q > 0) circ(g, 390 + rnd(i + 1) * 300, 710 + rnd(i + 90) * 270 - q * 60 * rnd(i + 4), 10 + q * 44 * rnd(i + 20), '#A8825E', q * 0.85); } // o rosto se desmancha
    g.restore();
    rect(g, 300, 1380, 480, 110, '#8A6A3A'); rect(g, 314, 1394, 452, 82, '#D8C8A0');
    for (let i = 0; i < 9; i++) { const x = 346 + i * 44, q = clamp(1 - (k * 9 - i)); if (q <= 0) continue; g.globalAlpha = q; g.strokeStyle = '#3A2616'; g.lineWidth = 6; g.beginPath(); g.moveTo(x, 1450); g.bezierCurveTo(x + 8, 1410 + rnd(i) * 20, x + 30, 1420, x + 18, 1446); g.quadraticCurveTo(x + 26, 1462, x + 40, 1440); g.stroke(); g.globalAlpha = 1; } // nome em letra cursiva ilegível, apagando
    g.restore(); vinheta(g, 0.62);
  };

  Motor.POSES.mt_grita = t => ({ al: [-30, 150], ar: [205, -40], fl: [-30, 235], fr: [30, 235], olho: 'grande', boca: 'aberta', sobr: 1, tremer: 2, inclina: 0.07 });

  // peças reaproveitadas pela capa
  Motor.MT = { ave, velha, acai };
})();
