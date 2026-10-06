// Mascotes: a Ficha (papel dramático e esquecido) e o Carretel (GMS, tranquilo, lembra de tudo).
// Formas simples, contorno grosso, olhos grandes; cada um desenha numa caixa 600×800.
(function () {
  const L = '#1A1410', OUT = 7;
  const ST = ['#3B82F6', '#06B6D4', '#6366F1', '#8B5CF6', '#F59E0B', '#EF4444', '#F97316', '#10B981'];
  const ink = (ctx, fill) => { if (fill) { ctx.fillStyle = fill; ctx.fill(); } ctx.strokeStyle = L; ctx.lineWidth = OUT; ctx.lineJoin = 'round'; ctx.lineCap = 'round'; ctx.stroke(); };
  function hose(ctx, pts, w = 12) { // membro "mangueira de borracha"
    ctx.save(); ctx.strokeStyle = L; ctx.lineWidth = w; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    ctx.beginPath(); ctx.moveTo(...pts[0]); if (pts.length === 3) ctx.quadraticCurveTo(...pts[1], ...pts[2]); else ctx.bezierCurveTo(...pts[1], ...pts[2], ...pts[3]); ctx.stroke(); ctx.restore();
  }
  function glove(ctx, x, y, r = 26, fill = '#FFFFFF') { ctx.beginPath(); ctx.arc(x, y, r, 0, 7); ink(ctx, fill); }
  function shoe(ctx, x, y, d, fill) { ctx.beginPath(); ctx.ellipse(x + d * 14, y, 46, 24, 0, 0, 7); ink(ctx, fill); }
  function eye(ctx, x, y, r, { look = [0, 0], lid = 0, kind = 'open', pr = 0.42 } = {}) {
    if (kind === 'spiral') { ctx.beginPath(); ctx.arc(x, y, r, 0, 7); ink(ctx, '#FFFFFF'); ctx.beginPath(); for (let a = 0; a < 14; a += 0.2) { const rr = a / 14 * r * 0.85; ctx.lineTo(x + Math.cos(a) * rr, y + Math.sin(a) * rr); } ctx.strokeStyle = L; ctx.lineWidth = 4; ctx.stroke(); return; }
    if (kind === 'happy') { ctx.beginPath(); ctx.arc(x, y + r * 0.3, r * 0.7, Math.PI * 1.1, Math.PI * 1.9); ctx.strokeStyle = L; ctx.lineWidth = 8; ctx.stroke(); return; }
    if (kind === 'x') { ctx.strokeStyle = L; ctx.lineWidth = 8; ctx.beginPath(); ctx.moveTo(x - r * .5, y - r * .5); ctx.lineTo(x + r * .5, y + r * .5); ctx.moveTo(x + r * .5, y - r * .5); ctx.lineTo(x - r * .5, y + r * .5); ctx.stroke(); return; }
    ctx.beginPath(); ctx.arc(x, y, r, 0, 7); ink(ctx, '#FFFFFF');
    ctx.save(); ctx.beginPath(); ctx.arc(x, y, r - 3, 0, 7); ctx.clip();
    ctx.fillStyle = L; ctx.beginPath(); ctx.arc(x + look[0], y + look[1], r * pr, 0, 7); ctx.fill();
    ctx.fillStyle = '#FFFFFF'; ctx.beginPath(); ctx.arc(x + look[0] - r * .15, y + look[1] - r * .17, r * .13, 0, 7); ctx.fill();
    if (lid > 0) { ctx.fillStyle = arguments[2] && ctx._lidColor || '#E9E4D8'; ctx.fillRect(x - r, y - r, r * 2, r * 2 * lid); ctx.strokeStyle = L; ctx.lineWidth = 6; ctx.beginPath(); ctx.moveTo(x - r, y - r + r * 2 * lid); ctx.lineTo(x + r, y - r + r * 2 * lid); ctx.stroke(); }
    ctx.restore(); ctx.beginPath(); ctx.arc(x, y, r, 0, 7); ctx.strokeStyle = L; ctx.lineWidth = OUT; ctx.stroke();
  }

  // ---------------- A FICHA ----------------
  const FICHA = {
    dramatica: { eyes: [{ look: [6, -10] }, { look: [6, -10] }], mouth: 'wail', L: [[150, 470], [110, 360], [210, 300]], R: [[450, 470], [500, 360], [392, 300]], brows: 'sad' },
    esquecida: { eyes: [{ kind: 'spiral' }, { kind: 'spiral' }], mouth: 'wobble', L: [[150, 470], [90, 520], [120, 600]], R: [[450, 470], [520, 400], [470, 300]], q: true },
    chocada: { eyes: [{ pr: 0.22 }, { pr: 0.22 }], mouth: 'o', L: [[150, 470], [70, 430], [100, 330]], R: [[450, 470], [530, 430], [500, 330]], brows: 'up' },
    chorando: { eyes: [{ kind: 'happy' }, { kind: 'happy' }], mouth: 'wail', L: [[150, 470], [110, 560], [150, 620]], R: [[450, 470], [490, 560], [450, 620]], tears: true, brows: 'sad' },
    brava: { eyes: [{ lid: 0.38, look: [0, 6] }, { lid: 0.38, look: [0, 6] }], mouth: 'grr', L: [[150, 470], [90, 500], [150, 560]], R: [[450, 470], [510, 500], [450, 560]], brows: 'angry' },
    amassada: { eyes: [{ kind: 'x' }, { kind: 'x' }], mouth: 'flat', L: [[150, 500], [100, 600], [80, 650]], R: [[450, 500], [500, 600], [520, 650]], crumple: true },
  };
  function ficha(ctx, expr = 'dramatica') {
    const F = FICHA[expr] || FICHA.dramatica;
    ctx.save();
    // pernas + sapatos (vermelhos: o "ponto vermelho" mudou de lado e virou tênis)
    hose(ctx, [[245, 640], [240, 690], [230, 740]]); hose(ctx, [[355, 640], [360, 690], [370, 740]]);
    shoe(ctx, 222, 748, -1, '#2B2B2B'); shoe(ctx, 378, 748, 1, '#2B2B2B');
    // braços atrás? não: na frente, depois do corpo. Corpo:
    ctx.save(); ctx.translate(300, 400); ctx.rotate(F.crumple ? 0.06 : -0.03); ctx.translate(-300, -400);
    const body = () => { ctx.beginPath(); ctx.moveTo(170, 170); ctx.lineTo(370, 165); ctx.lineTo(440, 230); ctx.lineTo(432, 640); ctx.quadraticCurveTo(300, 655, 168, 642); ctx.closePath(); };
    body(); ink(ctx, '#F4EFE3');
    ctx.save(); body(); ctx.clip();
    // linhas da tabela
    ctx.strokeStyle = 'rgba(100,116,139,.45)'; ctx.lineWidth = 3; for (let y = 260; y < 640; y += 38) { ctx.beginPath(); ctx.moveTo(185, y); ctx.lineTo(425, y); ctx.stroke(); }
    ctx.beginPath(); ctx.moveTo(240, 230); ctx.lineTo(240, 640); ctx.stroke();
    // cabeçalho impresso
    ctx.fillStyle = 'rgba(26,20,16,.8)'; ctx.fillRect(188, 192, 120, 16); ctx.fillRect(188, 214, 70, 10);
    // rabiscos de caneta azul (embaixo do rosto)
    ctx.strokeStyle = 'rgba(30,58,138,.8)'; ctx.lineWidth = 4;
    for (const [y, x1] of [[540, 400], [578, 360], [616, 395]]) { ctx.beginPath(); let x = 252; ctx.moveTo(x, y); while (x < x1) { const nx = x + 16; ctx.quadraticCurveTo(x + 8, y - 12, nx, y); x = nx; } ctx.stroke(); }
    ctx.strokeStyle = 'rgba(220,38,38,.75)'; ctx.lineWidth = 5; ctx.beginPath(); ctx.moveTo(250, 572); ctx.lineTo(370, 566); ctx.stroke();
    // mancha de café
    ctx.strokeStyle = 'rgba(120,72,30,.55)'; ctx.lineWidth = 9; ctx.beginPath(); ctx.arc(220, 600, 42, 0.3, 5.9); ctx.stroke();
    ctx.fillStyle = 'rgba(150,95,45,.18)'; ctx.beginPath(); ctx.arc(220, 600, 38, 0, 7); ctx.fill();
    if (F.crumple) { ctx.strokeStyle = 'rgba(26,20,16,.35)'; ctx.lineWidth = 4; for (const [a, b, c, d] of [[180, 300, 300, 360], [300, 360, 420, 280], [190, 480, 320, 430], [320, 430, 430, 520], [260, 250, 330, 640]]) { ctx.beginPath(); ctx.moveTo(a, b); ctx.lineTo(c, d); ctx.stroke(); } }
    ctx.restore();
    body(); ctx.strokeStyle = L; ctx.lineWidth = OUT; ctx.stroke();
    // orelha dobrada
    ctx.beginPath(); ctx.moveTo(370, 165); ctx.lineTo(372, 232); ctx.lineTo(440, 230); ctx.closePath(); ink(ctx, '#DCD4C2');
    // rosto
    ctx._lidColor = '#F4EFE3';
    const ex = [[255, 330], [355, 325]];
    F.eyes.forEach((o, i) => eye(ctx, ex[i][0], ex[i][1], i ? 44 : 50, o));   // olhos de tamanhos diferentes: feio-fofo
    ctx.strokeStyle = L; ctx.lineWidth = 9; ctx.lineCap = 'round';
    if (F.brows === 'sad') { ctx.beginPath(); ctx.moveTo(215, 262); ctx.lineTo(285, 280); ctx.moveTo(320, 278); ctx.lineTo(392, 262); ctx.stroke(); }
    if (F.brows === 'angry') { ctx.beginPath(); ctx.moveTo(210, 270); ctx.lineTo(290, 296); ctx.moveTo(318, 294); ctx.lineTo(396, 266); ctx.stroke(); }
    if (F.brows === 'up') { ctx.beginPath(); ctx.moveTo(215, 252); ctx.quadraticCurveTo(255, 236, 292, 252); ctx.moveTo(318, 248); ctx.quadraticCurveTo(355, 232, 392, 248); ctx.stroke(); }
    const m = F.mouth;
    if (m === 'wail') { ctx.beginPath(); ctx.moveTo(262, 440); ctx.quadraticCurveTo(305, 380, 348, 440); ctx.quadraticCurveTo(305, 425, 262, 440); ctx.closePath(); ink(ctx, '#7A1F1F'); ctx.fillStyle = '#FFFFFF'; ctx.fillRect(296, 410, 14, 12); }
    if (m === 'o') { ctx.beginPath(); ctx.ellipse(305, 425, 24, 32, 0, 0, 7); ink(ctx, '#7A1F1F'); }
    if (m === 'wobble') { ctx.beginPath(); ctx.moveTo(262, 420); for (let i = 1; i <= 8; i++) ctx.lineTo(262 + i * 11, 420 + (i % 2 ? -8 : 8)); ctx.strokeStyle = L; ctx.lineWidth = 7; ctx.stroke(); }
    if (m === 'grr') { ctx.beginPath(); ctx.roundRect(262, 405, 88, 34, 8); ink(ctx, '#FFFFFF'); ctx.beginPath(); ctx.moveTo(262, 422); ctx.lineTo(350, 422); for (let x = 284; x < 350; x += 22) { ctx.moveTo(x, 405); ctx.lineTo(x, 439); } ctx.lineWidth = 4; ctx.stroke(); }
    if (m === 'flat') { ctx.beginPath(); ctx.moveTo(270, 425); ctx.lineTo(340, 420); ctx.strokeStyle = L; ctx.lineWidth = 8; ctx.stroke(); }
    if (F.tears) { ctx.fillStyle = 'rgba(96,165,250,.85)'; for (const x of [235, 375]) { ctx.beginPath(); ctx.roundRect(x - 12, 340, 24, 230, 12); ctx.fill(); } }
    ctx.restore();
    // braços (mangueira de borracha) + luvas
    hose(ctx, F.L); hose(ctx, F.R); glove(ctx, ...F.L[2]); glove(ctx, ...F.R[2]);
    if (F.q) { ctx.font = '800 120px "Open Sans"'; ctx.fillStyle = '#F5F7FA'; ctx.strokeStyle = L; ctx.lineWidth = 10; ctx.textAlign = 'center'; ctx.strokeText('?', 470, 150); ctx.fillText('?', 470, 150); }
    ctx.restore();
  }

  // ---------------- O CARRETEL ----------------
  const CARRETEL = {
    tranquilo: { eyes: { lid: 0.42 }, mouth: 'smirk', L: [[205, 470], [180, 560], [230, 600]], R: [[395, 470], [420, 560], [370, 600]], pockets: true },
    joinha: { eyes: { look: [0, 0] }, mouth: 'grin', L: [[205, 470], [180, 560], [230, 600]], R: [[395, 470], [500, 450], [500, 340]], thumb: true },
    lembra: { eyes: { look: [-8, -10] }, mouth: 'smirk', L: [[205, 470], [180, 560], [230, 600]], R: [[395, 470], [470, 380], [430, 250]], finger: true },
    comemora: { eyes: { kind: 'happy' }, mouth: 'grin', L: [[205, 460], [110, 380], [130, 260]], R: [[395, 460], [490, 380], [470, 260]] },
  };
  function carretel(ctx, expr = 'tranquilo', ring = ST) { // ring: cores do anel (o anel muda por projeto)
    const F = CARRETEL[expr] || CARRETEL.tranquilo;
    ctx.save();
    hose(ctx, [[260, 600], [255, 670], [245, 730]]); hose(ctx, [[340, 600], [345, 670], [355, 730]]);
    shoe(ctx, 236, 742, -1, '#E2231A'); shoe(ctx, 364, 742, 1, '#E2231A');   // tênis vermelhos (o ponto do logo)
    // corpo: disco do carretel com o anel de 8 cores
    ctx.beginPath(); ctx.arc(300, 400, 210, 0, 7); ink(ctx, '#0F172A');
    ctx.save(); ctx.lineCap = 'round'; ctx.lineWidth = 44;
    const n = ring.length, step = 360 / n, span = step * 0.82;
    for (let k = 0; k < n; k++) { const a0 = (-90 + step * (1 - 0.82) / 2 + step * k) * Math.PI / 180; ctx.strokeStyle = ring[k]; ctx.beginPath(); ctx.arc(300, 400, 176, a0, a0 + span * Math.PI / 180); ctx.stroke(); }
    ctx.restore();
    ctx.beginPath(); ctx.arc(300, 400, 138, 0, 7); ink(ctx, '#F5F7FA');
    // o ponto vermelho: um topete
    ctx.beginPath(); ctx.arc(300, 186, 30, 0, 7); ink(ctx, '#E2231A');
    // rosto
    ctx._lidColor = '#F5F7FA';
    for (const [x, r] of [[250, 40], [350, 40]]) eye(ctx, x, 380, r, F.eyes);
    // sem bochecha rosada no Bit (visual pastel)
    if (F.mouth === 'smirk') { ctx.beginPath(); ctx.moveTo(268, 462); ctx.quadraticCurveTo(310, 482, 342, 452); ctx.strokeStyle = L; ctx.lineWidth = 8; ctx.lineCap = 'round'; ctx.stroke(); }
    if (F.mouth === 'grin') { ctx.beginPath(); ctx.moveTo(260, 450); ctx.quadraticCurveTo(300, 452, 340, 450); ctx.quadraticCurveTo(334, 505, 300, 506); ctx.quadraticCurveTo(266, 505, 260, 450); ctx.closePath(); ink(ctx, '#7A1F1F'); ctx.fillStyle = '#FFFFFF'; ctx.fillRect(268, 452, 64, 14); }
    if (F.pockets) { // braços "no bolso": somem atrás do corpo
      hose(ctx, [[150, 430], [120, 520], [190, 560]]); hose(ctx, [[450, 430], [480, 520], [410, 560]]);
    } else {
      hose(ctx, F.L); hose(ctx, F.R); glove(ctx, ...F.L[2]); glove(ctx, ...F.R[2]);
      if (F.thumb) { ctx.beginPath(); ctx.roundRect(490, 278, 22, 50, 11); ink(ctx, '#FFFFFF'); }
      if (F.finger) { ctx.beginPath(); ctx.roundRect(420, 192, 20, 52, 10); ink(ctx, '#FFFFFF'); }
    }
    ctx.restore();
  }
  window.FICHA_EXPR = Object.keys(FICHA); window.CARRETEL_EXPR = Object.keys(CARRETEL);
  window.drawFicha = ficha; window.drawCarretel = carretel;
})();
