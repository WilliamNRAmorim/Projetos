// Cenários e som do Short solto 05 (Comadre Fulozinha). Só ACRESCENTA ao Motor. Prefixo cf_ = mata de entardecer: céu creme e pêssego, verdes de folha, preto do cabelo e o vermelho da marca.
(() => {
  const { CENARIOS } = Motor, W = Motor.W, H = Motor.H, { rect, circ, line, rrect, glow, vgrad, vinheta, rnd, lerp, clamp, out, P } = Motor.H_;
  const TAU = Math.PI * 2, CEU = '#F6E7B4', PESSEGO = '#EFA766', FOLHA = '#7FA23C', MUSGO = '#4C7330', SOMBRA = '#22401F', NOITE = '#0F1E10', CABELO = '#0A0B08', TRONCO = '#5B3A22', CASCA = '#3A2415', TERRA = '#C08A52', PELE = '#A8714A', OSSO = '#F7F1DC', FUMO = '#4A2A12';
  const elipse = (g, x, y, rx, ry, c, a = 1, rot = 0) => { g.globalAlpha = a; g.fillStyle = c; g.beginPath(); g.ellipse(x, y, rx, ry, rot, 0, TAU); g.fill(); g.globalAlpha = 1; };
  const forma = (g, c, fn, a = 1) => { g.globalAlpha = a; g.fillStyle = c; g.beginPath(); fn(g); g.closePath(); g.fill(); g.globalAlpha = 1; };
  const curva = (g, c, lw, fn, a = 1) => { g.globalAlpha = a; g.strokeStyle = c; g.lineWidth = lw; g.lineCap = 'round'; g.lineJoin = 'round'; g.beginPath(); fn(g); g.stroke(); g.globalAlpha = 1; };
  const poli = (g, c, pts, a = 1) => forma(g, c, q => pts.forEach(([x, y], i) => i ? q.lineTo(x, y) : q.moveTo(x, y)), a);

  // ───── peças
  function copa(g, t, x, y, r, c, s) { for (let i = 0; i < 9; i++) elipse(g, x + (rnd(s + i) - 0.5) * r * 2 + Math.sin(t * 0.9 + i + s) * 6, y + (rnd(s + i + 31) - 0.5) * r, r * (0.4 + 0.35 * rnd(s + i + 7)), r * (0.28 + 0.25 * rnd(s + i + 11)), c); }
  function tronco(g, x, y, w, h, c = TRONCO) { forma(g, c, q => { q.moveTo(x - w * 0.9, y); q.quadraticCurveTo(x - w * 0.4, y - 40, x - w * 0.42, y - h); q.lineTo(x + w * 0.38, y - h); q.quadraticCurveTo(x + w * 0.45, y - 50, x + w * 0.95, y); }); curva(g, CASCA, w * 0.08, q => { q.moveTo(x - w * 0.12, y - 30); q.quadraticCurveTo(x - w * 0.2, y - h / 2, x - w * 0.08, y - h); q.moveTo(x + w * 0.17, y - 90); q.lineTo(x + w * 0.15, y - h * 0.6); }, 0.8); }
  function folhagem(g, t, y, n, c, s, k = 1) { for (let i = 0; i < n; i++) { const x = rnd(s + i) * W, yy = y + rnd(s + i + 50) * 90; for (let j = -2; j <= 2; j++) elipse(g, x + j * 34 * k, yy - (40 - Math.abs(j) * 12) * k, 16 * k, 66 * k, c, 1, j * 0.42 + Math.sin(t + i) * 0.04); } }
  // mata: céu claro, três camadas de árvores, trilha de terra. o.abre 0..1 = trilha iluminada
  function mata(g, t, o = {}) {
    vgrad(g, 0, 1100, o.ceu || CEU, o.ceu2 || PESSEGO); glow(g, 540, 620, 620, '#FFF6D0', 0.75); circ(g, 540, 640, 105, '#FFF4C4');
    for (let i = 0; i < 9; i++) { const x = i * 135 + rnd(i + 2) * 60; tronco(g, x, 1040, 34, 760, '#9AA35A'); copa(g, t, x, 330 + rnd(i) * 220, 130, '#A9B75E', i * 13); }
    rect(g, 0, 960, W, H - 960, MUSGO); folhagem(g, t, 990, 16, FOLHA, 5, 0.8);
    poli(g, TERRA, [[495, 975], [585, 975], [800, 1250], [1040, H], [40, H], [330, 1250]]); if (o.abre) poli(g, CEU, [[505, 975], [575, 975], [880, H], [200, H]], 0.55 * o.abre);
    for (const [x, w, s] of [[150, 80, 3], [945, 90, 8], [30, 120, 17], [1070, 110, 23]]) { tronco(g, x, 1300 + w, w, 1500); copa(g, t, x, 120 + rnd(s) * 150, 240, s % 2 ? MUSGO : SOMBRA, s); }
    copa(g, t, 360, -40, 220, SOMBRA, 41); copa(g, t, 760, -60, 240, MUSGO, 57);
    folhagem(g, t, 1330, 5, SOMBRA, 77, 1.3); for (let i = 0; i < 22; i++) { const y = (rnd(i + 90) * 1300 + t * (25 + rnd(i) * 30)) % 1500, x = rnd(i + 44) * W + Math.sin(t * 1.3 + i) * 40; elipse(g, x, y, 11, 5, i % 3 ? FOLHA : CEU, 0.8, t + i); }
  }
  // Comadre Fulozinha: (x,y) = pés. o.olhos 0..1, o.vento
  function menina(g, t, x, y, s, o = {}) {
    g.save(); g.translate(x, y); g.scale(s, s); const v = Math.sin(t * 1.4) * 14 * (o.vento ?? 1);
    elipse(g, 0, 6, 190, 22, NOITE, 0.4);
    // cabelo de trás, até o chão
    forma(g, CABELO, q => { q.moveTo(0, -668); q.bezierCurveTo(-150, -660, -110, -480, -130, -360); q.bezierCurveTo(-170, -220, -140 + v, -100, -178 + v, 4); q.lineTo(-110 + v, -14); q.lineTo(-62 + v, 8); q.lineTo(0, -26); q.lineTo(62 + v, 8); q.lineTo(110 + v, -14); q.lineTo(178 + v, 4); q.bezierCurveTo(140 + v, -100, 170, -220, 130, -360); q.bezierCurveTo(110, -480, 150, -660, 0, -668); });
    for (const d of [-1, 1]) curva(g, PELE, 30, q => { q.moveTo(d * 34, -170); q.lineTo(d * 38, -8); });
    poli(g, '#E9DDB8', [[-58, -450], [58, -450], [108, -150], [-108, -150]]);
    for (const d of [-1, 1]) forma(g, CABELO, q => { q.moveTo(d * 40, -520); q.bezierCurveTo(d * 120, -420, d * 90, -260, d * 130 + v, -60); q.quadraticCurveTo(d * 60, -240, d * 38, -450); });
    elipse(g, 0, -528, 64, 76, PELE); forma(g, CABELO, q => { q.moveTo(-76, -520); q.quadraticCurveTo(-80, -630, 0, -632); q.quadraticCurveTo(80, -630, 76, -520); q.quadraticCurveTo(50, -588, 6, -586); q.quadraticCurveTo(-45, -570, -76, -520); });
    for (const d of [-1, 1]) { if (o.olhos) { elipse(g, d * 25, -526, 11, 12, CABELO); glow(g, d * 25, -526, 44, P.accent, 0.7 * o.olhos); circ(g, d * 25, -526, 8 * o.olhos, P.accent); } else elipse(g, d * 25, -526, 8, 10, CABELO); }
    curva(g, '#5A2A18', 5, q => { q.moveTo(-18, -488); q.quadraticCurveTo(0, -482, 18, -490); });
    for (let i = 0; i < 6; i++) { const d = i % 2 ? 1 : -1; curva(g, '#39402C', 4, q => { q.moveTo(d * (60 + i * 8), -540 + i * 30); q.quadraticCurveTo(d * (130 + i * 6), -320, d * (110 + i * 12) + v, -20); }, 0.8); }
    g.restore();
  }
  // Zeca: (x,y) = pés. o.passo (fase), o.arma, o.ri, o.medo, o.costas, o.joelho
  function zeca(g, t, x, y, s, o = {}) {
    g.save(); g.translate(x, y); g.scale(s * (o.flip ? -1 : 1), s); const p = o.passo != null ? Math.sin(o.passo * 5.5) : 0, dy = o.joelho ? 170 : 0;
    elipse(g, 0, 6, 150, 20, NOITE, 0.35);
    for (const d of [-1, 1]) curva(g, '#2C3A4A', 54, q => { q.moveTo(d * 34, -300 + dy); if (o.joelho) { q.lineTo(d * 120, -50); q.lineTo(d * 40, -14); } else q.lineTo(d * (48 + p * 40 * d), -16 - Math.max(0, p * d) * 24); });
    g.translate(0, dy);
    if (o.arma) { curva(g, CASCA, 24, q => { q.moveTo(-190, -330); q.lineTo(60, -540); }); curva(g, '#2A2C2E', 13, q => { q.moveTo(20, -508); q.lineTo(190, -650); }); }
    poli(g, '#B8552E', [[-84, -510], [84, -510], [70, -290], [-70, -290]]);
    for (const d of [-1, 1]) curva(g, '#B8552E', 40, q => { q.moveTo(d * 70, -480); if (o.medo) { q.lineTo(d * 160, -520); q.lineTo(d * 100, -630); } else if (o.joelho) { q.lineTo(d * 90, -380); q.lineTo(d * 6, -430); } else { q.lineTo(d * 112, -380 + p * 30 * d); q.lineTo(d * 104, -300 + p * 40 * d); } });
    circ(g, 0, -590, 66, o.costas ? '#2A1A10' : PELE); elipse(g, 0, -648, 112, 26, '#8A6A36'); elipse(g, 0, -668, 60, 38, '#A8854A');
    if (!o.costas) { for (const d of [-1, 1]) { circ(g, d * 24, -598, o.medo ? 14 : 7, o.medo ? OSSO : CABELO); if (o.medo) circ(g, d * 24, -598, 6, CABELO); }
      if (o.ri) forma(g, '#3A1408', q => { const a = 18 + Math.abs(Math.sin(t * 13)) * 18; q.moveTo(-32, -566); q.lineTo(32, -566); q.quadraticCurveTo(0, -566 + a * 2, -32, -566); }); else if (o.medo) elipse(g, 0, -555, 15, 20, '#3A1408'); else line(g, -20, -558, 20, -558, '#3A1408', 7); }
    g.restore();
  }
  function rolo(g, x, y, s, a = 0) { g.save(); g.translate(x, y); g.rotate(a); g.scale(s, s); rrect(g, -64, -24, 128, 48, 20, FUMO); for (let i = -2; i <= 2; i++) curva(g, '#8A5A2A', 6, q => { q.moveTo(i * 24 - 8, -22); q.lineTo(i * 24 + 10, 22); }); g.restore(); }
  function toco(g, x, y, s) { g.save(); g.translate(x, y); g.scale(s, s); tronco(g, 0, 0, 220, 190); elipse(g, 0, -190, 92, 34, '#C99A62'); for (const r of [62, 38, 14]) curva(g, TRONCO, 4, q => q.ellipse(0, -190, r, r * 0.36, 0, 0, TAU)); g.restore(); }
  function ondas(g, t, x, y, k = 1, c = P.accent) { for (let i = 0; i < 3; i++) { const f = (t * 1.5 + i / 3) % 1; for (const d of [-1, 1]) curva(g, c, 12 * k, q => q.arc(x, y, (40 + f * 190) * k, d > 0 ? -0.6 : Math.PI - 0.6, d > 0 ? 0.6 : Math.PI + 0.6), (1 - f) * 0.95); } }
  // mecha de cabelo estalando: pts = origem, controle, ponta. Só o rastro e a faísca; nada de ferimento na tela.
  function chicote(g, t, em, pts) { const k = clamp((t - em) / 0.16); if (k <= 0) return; const a = 1 - clamp((t - em - 0.9) / 0.4); if (a <= 0) return; const [x0, y0, cx, cy, x1, y1] = pts, e = out(k);
    for (let i = 0; i < 9; i++) { const o = (i - 4) * 18; curva(g, CABELO, 30 - i * 3, q => { q.moveTo(x0, y0 + o * 2); q.quadraticCurveTo(lerp(x0, cx, k), lerp(y0, cy, k) + o, lerp(x0, x1, e), lerp(y0, y1, e) + o * 0.4); }, a); }
    const f = clamp(1 - (t - em - 0.16) / 0.3); if (k >= 1 && f > 0) for (let i = 0; i < 10; i++) { const an = i / 10 * TAU, r = 110 + 90 * (1 - f); line(g, x1 + Math.cos(an) * 60, y1 + Math.sin(an) * 60, x1 + Math.cos(an) * r, y1 + Math.sin(an) * r, i % 2 ? P.accent : OSSO, 12 * f + 2); } }
  const fim = g => vinheta(g, 0.34);

  // ───── cenários
  // primeiro e último plano: a trilha, o toco vazio e a menina que surge
  CENARIOS.cf_mata = (g, t) => { mata(g, t); const k = out(clamp((t - 0.25) / 0.6)); g.save(); g.globalAlpha = k; menina(g, t, 540, 1190, 0.9, { olhos: clamp((t - 1) * 2.5) }); g.restore(); toco(g, 210, 1330, 0.9); fim(g); };
  CENARIOS.cf_olhos = (g, t) => { mata(g, t, { ceu2: '#E07A45' }); menina(g, t, 540, 2150, 2.6, { olhos: out(clamp(t / 0.5)) }); fim(g); };
  // o pai contando na varanda, ao entardecer
  CENARIOS.cf_pai = (g, t) => { vgrad(g, 0, 1100, '#F7D58A', '#E2774A'); glow(g, 830, 780, 500, '#FFF1B8', 0.8); circ(g, 830, 800, 95, '#FFEDB0');
    for (let i = 0; i < 12; i++) copa(g, t, i * 100, 930 + rnd(i) * 60, 110, MUSGO, i * 9);
    rect(g, 0, 980, W, H - 980, SOMBRA); rect(g, 0, 1180, W, H - 1180, '#8A5A34'); for (let i = 0; i < 8; i++) rect(g, i * 150, 1180, 6, H - 1180, CASCA); rect(g, 40, 230, 40, 960, CASCA); poli(g, '#7A3522', [[0, 130], [W, 200], [W, 290], [0, 250]]);
    rect(g, 140, 1080, 380, 34, CASCA); for (const x of [165, 465]) rect(g, x, 1110, 28, 160, CASCA);
    zeca(g, t, 320, 1270, 1.15, { joelho: 1 }); elipse(g, 320, 1270 - 480, 24, 5 + Math.abs(Math.sin(t * 9)) * 10, '#3A1408');
    zeca(g, t, 790, 1330, 0.66, { joelho: 1, flip: 1 }); fim(g); };
  CENARIOS.cf_menina = (g, t) => { mata(g, t); const k = out(clamp(t / 2.4)); g.save(); g.translate(0, lerp(-420, 0, k)); menina(g, t, 540, 1300, 1.45, { vento: 2 }); g.restore(); fim(g); };
  // passarinhos, tatu e veado em segurança ao redor dela
  CENARIOS.cf_bichos = (g, t) => { mata(g, t); menina(g, t, 540, 1220, 1.05);
    for (const [x, y, s, d] of [[250, 520, 1, 1], [820, 440, 0.85, -1], [760, 700, 0.7, -1], [330, 760, 0.65, 1]]) { const yy = y + Math.sin(t * 3 + x) * 18, a = Math.sin(t * 14 + x) * 36; g.save(); g.translate(x, yy); g.scale(s * d, s); elipse(g, 0, 0, 44, 28, '#E9C23C'); circ(g, 38, -20, 22, '#E9C23C'); poli(g, CASCA, [[56, -26], [86, -16], [56, -10]]); circ(g, 44, -24, 5, CABELO); poli(g, '#B8862A', [[-14, -10], [-70, -10 - a], [12, 8]]); g.restore(); }
    g.save(); g.translate(220, 1240); for (const x of [-70, 60]) rect(g, x, -20, 28, 40, CASCA); elipse(g, 0, -60, 130, 74, '#8A7052'); for (let i = -3; i <= 3; i++) curva(g, CASCA, 6, q => q.ellipse(i * 26, -60, 20, 70, 0, -2.6, -0.5)); elipse(g, 140, -40, 52, 28, '#A88A68', 1, 0.3); poli(g, '#A88A68', [[118, -66], [124, -112], [146, -68]]); circ(g, 154, -46, 6, CABELO); g.restore();
    g.save(); g.translate(870, 1220); for (const x of [-70, -35, 30, 62]) rect(g, x, -150, 17, 150, '#8A4E26'); elipse(g, 0, -180, 110, 62, '#B8723A'); curva(g, '#B8723A', 48, q => { q.moveTo(-70, -200); q.lineTo(-110, -310); }); elipse(g, -135, -330, 56, 34, '#B8723A', 1, 0.25); for (const d of [-14, 22]) elipse(g, -100 + d, -382, 14, 38, '#B8723A', 1, d / 40); circ(g, -140, -338, 7, CABELO); for (let i = 0; i < 6; i++) circ(g, -50 + i * 22, -195 + (i % 2) * 24, 6, OSSO); g.restore(); fim(g); };
  // a mão deixa o fumo no toco
  CENARIOS.cf_toco = (g, t) => { mata(g, t); toco(g, 540, 1300, 2.1); const k = out(clamp((t - 0.4) / 1.4)), y = lerp(430, 862, k), volta = out(clamp((t - 2.4) / 0.8)), my = volta ? 862 : y;
    rolo(g, 540, y, 1.9); g.save(); g.translate(volta * 420, -volta * 420); curva(g, '#B8552E', 150, q => { q.moveTo(1180, my - 420); q.lineTo(760, my - 130); }); elipse(g, 690, my - 90, 100, 74, PELE, 1, 0.6); for (let i = 0; i < 3; i++) curva(g, PELE, 40, q => { q.moveTo(680 - i * 46, my - 120 + i * 18); q.quadraticCurveTo(600 - i * 40, my - 80, 610 - i * 48, my - 24); }); g.restore();
    if (k >= 1) glow(g, 540, 862, 260, '#FFF1B8', 0.35 * clamp((t - 1.8) * 2)); fim(g); };
  CENARIOS.cf_zeca = (g, t) => { mata(g, t); zeca(g, t, 540, 1950 + Math.abs(Math.sin(t * 13)) * 14, 2.1, { ri: 1, arma: 1 }); fim(g); };
  // passa pelo toco vazio (círculo vermelho)
  CENARIOS.cf_entra = (g, t) => { mata(g, t); const k = clamp(t / 3); zeca(g, t, lerp(760, 560, k), lerp(1420, 1070, k), lerp(1.2, 0.55, k), { passo: t, arma: 1, costas: 1 }); toco(g, 250, 1290, 1.25); const a = clamp((t - 0.9) * 3); if (a > 0) curva(g, P.accent, 12, q => q.ellipse(250, 1050, 150, 70, 0, 0, TAU * a)); fim(g); };
  CENARIOS.cf_longe = (g, t) => { mata(g, t); menina(g, t, 705, 985, 0.2, { olhos: clamp(t - 0.8) }); ondas(g, t, 705, 850, 0.7); zeca(g, t, 400, 1420, 1.15, { arma: 1, costas: 1 }); fim(g); };
  CENARIOS.cf_anda = (g, t) => { g.save(); g.translate(540, 960); g.scale(1 + t * 0.12, 1 + t * 0.12); g.translate(-540, -960); mata(g, t); g.restore(); zeca(g, t, 540, 1360 - Math.abs(Math.sin(t * 5.5)) * 22, 1.25, { passo: t, arma: 1 }); fim(g); };
  CENARIOS.cf_lado = (g, t) => { mata(g, t, { ceu: '#EBD79A', ceu2: '#D9683C' }); const k = out(clamp((t - 0.45) / 0.4));
    zeca(g, t, 330, 2050, 2.2, { medo: t > 0.5, arma: 1 }); g.save(); g.translate(lerp(520, 0, k), 0); menina(g, t, 890, 1900, 1.75, { olhos: k }); g.restore(); if (k > 0.6) ondas(g, t, 640, 720, 0.9); fim(g); };
  CENARIOS.cf_pequeno = (g, t) => { mata(g, t, { abre: 0.7, ceu2: '#F4C77A' }); const k = clamp(t / 3); curva(g, OSSO, 10, q => { q.moveTo(540, 1000); q.quadraticCurveTo(300, 1250, 640, 1500); q.quadraticCurveTo(800, 1650, 560, H); }, 0.75); zeca(g, t, lerp(440, 520, k), lerp(1340, 1170, k), lerp(0.62, 0.46, k), { passo: t, costas: 1 }); fim(g); };
  // a mesma árvore, três vezes
  CENARIOS.cf_arvore = (g, t) => { const v = Math.min(2, Math.floor(t / 0.8)), u = clamp((t - v * 0.8) / 0.8); mata(g, t, { ceu2: ['#EFA766', '#DB7444', '#B4503A'][v] });
    tronco(g, 540, 1280, 250, 1400); copa(g, t, 540, 130, 330, SOMBRA, 99); curva(g, P.accent, 22, q => { q.moveTo(490, 690); q.lineTo(600, 800); q.moveTo(600, 690); q.lineTo(490, 800); });
    zeca(g, t, lerp(-60, 1140, u), 1370, 0.95, { passo: t, arma: 1, medo: v === 2 });
    g.textAlign = 'center'; g.textBaseline = 'middle'; g.font = '900 190px Geist'; g.lineJoin = 'round'; g.lineWidth = 26; g.strokeStyle = NOITE; g.strokeText(`${v + 1}x`, 540, 430); g.fillStyle = v === 2 ? P.accent : OSSO; g.fillText(`${v + 1}x`, 540, 430); fim(g); };
  CENARIOS.cf_pernas = (g, t) => { mata(g, t, { ceu: '#E6C98A', ceu2: '#C45A38' }); const tr = t > 0.75 && t < 1.3 ? Math.sin(t * 60) * 16 : 0;
    g.save(); g.translate(tr, 0); zeca(g, t, 580, 1120, 1.75, { medo: 1 }); g.restore(); chicote(g, t, 0.6, [-60, 420, 120, 1080, 470, 930]); fim(g); };
  CENARIOS.cf_costas = (g, t) => { mata(g, t, { ceu: '#DDBA7E', ceu2: '#A8462F' }); const tr = t > 0.25 && t < 0.8 ? Math.sin(t * 60) * 18 : 0;
    g.save(); g.translate(tr, 0); zeca(g, t, 520, 1600, 1.75, { costas: 1, medo: 1 }); g.restore(); chicote(g, t, 0.1, [1150, 360, 800, 480, 640, 860]); fim(g); };
  CENARIOS.cf_chicote = (g, t) => { mata(g, t, { ceu: '#D7AE74', ceu2: '#8E3828' }); menina(g, t, 540, 1260, 1.2, { olhos: 1, vento: 4 });
    for (let i = 0; i < 4; i++) { const d = i % 2 ? 1 : -1; chicote(g, t % 1.6, 0.05 + i * 0.3, [540 + d * 90, 720, 540 + d * 620, 280 + i * 120, 540 + d * (330 + i * 20), 460 + i * 190]); } fim(g); };
  // larga a espingarda e joga o fumo
  CENARIOS.cf_joga = (g, t) => { mata(g, t, { ceu2: '#C45A38' }); zeca(g, t, 540, 1330, 1.45, { medo: 1 });
    const q = out(clamp((t - 0.35) / 0.6)); g.save(); g.translate(lerp(380, 210, q), lerp(760, 1340, q)); g.rotate(lerp(-0.6, 0.05, q)); curva(g, CASCA, 40, c => { c.moveTo(-170, 0); c.lineTo(40, 0); }); curva(g, '#2A2C2E', 20, c => { c.moveTo(20, -6); c.lineTo(250, -6); }); g.restore();
    for (let i = 0; i < 7; i++) { const k = clamp((t - 1.5 - i * 0.12) / 0.55); if (k <= 0) continue; rolo(g, lerp(640, 270 + i * 100, k), lerp(750, 1230 + (i % 3) * 55, k) - Math.sin(k * Math.PI) * 220, 0.85, k * 5 + i); } fim(g); };
  CENARIOS.cf_perdao = (g, t) => { mata(g, t, { ceu2: '#B4503A' }); zeca(g, t, 540 + Math.sin(t * 40) * 5, 1420, 1.6, { joelho: 1, medo: 1 }); for (let i = 0; i < 5; i++) rolo(g, 150 + i * 195, 1440 + (i % 2) * 50, 1.1, i);
    for (let i = 0; i < 3; i++) for (const d of [-1, 1]) curva(g, OSSO, 12, q => { const x = 540 + d * (230 + i * 70); q.moveTo(x, 800 - i * 20); q.lineTo(x + d * 50, 750 - i * 60); }, 0.8 - i * 0.2); fim(g); };
  CENARIOS.cf_parou = (g, t) => { mata(g, t, { ceu: '#F2DFA6', ceu2: '#E39058' }); const a = 1 - out(clamp((t - 0.4) / 0.9)); g.save(); g.globalAlpha = a; menina(g, t, 540, 1180, 0.85, { vento: 0.3 }); g.restore(); for (let i = 0; i < 4; i++) rolo(g, 240 + i * 200, 1300 + (i % 2) * 45, 0.8, i * 1.3); fim(g); };
  CENARIOS.cf_abre = (g, t) => { const k = out(clamp(t / 1.1)), u = clamp(t / 2); mata(g, t, { abre: k, ceu2: '#F4C77A' }); glow(g, 540, 960, 700, '#FFF6D0', 0.55 * k); zeca(g, t, 540, lerp(1480, 1200, u), lerp(0.95, 0.6, u), { passo: t, costas: 1 }); fim(g); };
  // a espingarda esquecida na parede, juntando teia
  CENARIOS.cf_nunca = (g, t) => { vgrad(g, 0, H, '#E8CE94', '#B88450'); for (let x = 30; x < W; x += 150) rect(g, x, 0, 6, 1330, '#9A6C40', 0.6); rect(g, 0, 1330, W, H - 1330, '#7A4C2A');
    for (const x of [230, 850]) { rect(g, x - 18, 720, 36, 70, CASCA); circ(g, x, 720, 26, CASCA); }
    curva(g, CASCA, 70, q => { q.moveTo(150, 730); q.lineTo(500, 690); }); curva(g, '#2A2C2E', 34, q => { q.moveTo(470, 680); q.lineTo(960, 660); });
    const k = clamp(t / 1.8); for (let i = 0; i < 6; i++) line(g, 960, 660, 960 - Math.cos(i * 0.32 - 0.3) * 330 * k, 660 - Math.sin(i * 0.32 - 0.3) * 330 * k, OSSO, 4);
    for (let r = 1; r <= 4; r++) curva(g, OSSO, 3, q => q.arc(960, 660, r * 70 * k, Math.PI - 0.3, Math.PI + 1.3), 0.85);
    elipse(g, 330, 1160, 200, 40, '#A8854A'); elipse(g, 330, 1125, 105, 66, '#8A6A36'); fim(g); };
  // crina trançada de manhã; o cavalo está bem e tranquilo
  CENARIOS.cf_crina = (g, t) => { vgrad(g, 0, 1100, '#BFE0D8', '#F8E2A4'); glow(g, 190, 520, 520, '#FFF8D8', 0.9); circ(g, 190, 540, 90, '#FFF6C8');
    for (let i = 0; i < 12; i++) copa(g, t, i * 100, 1000 + rnd(i) * 60, 110, FOLHA, i * 7); rect(g, 0, 1060, W, H - 1060, MUSGO);
    const C = '#9A5A30'; g.save(); g.translate(0, Math.sin(t * 1.6) * 3);
    forma(g, C, q => { q.moveTo(560, 470); q.quadraticCurveTo(870, 640, 1000, 1000); q.lineTo(1100, 1500); q.lineTo(430, 1500); q.quadraticCurveTo(520, 1050, 470, 800); q.quadraticCurveTo(360, 900, 200, 910); q.quadraticCurveTo(110, 870, 150, 790); q.quadraticCurveTo(300, 650, 420, 490); });
    poli(g, C, [[430, 500], [440, 320], [520, 470]]); poli(g, C, [[520, 480], [600, 330], [610, 520]]); poli(g, '#5A2E18', [[455, 470], [458, 380], [500, 465]]);
    elipse(g, 225, 845, 96, 66, '#C9906A', 1, -0.6); circ(g, 195, 850, 13, CASCA); elipse(g, 420, 640, 28, 18, CABELO, 1, -0.5); circ(g, 412, 634, 6, OSSO);
    for (let i = 0; i < 4; i++) { const a = i / 3, x = lerp(600, 940, a), y = lerp(500, 860, a * a * 0.3 + a * 0.7), ap = out(clamp((t - 0.4 - i * 0.4) / 0.35)), L = 340 - i * 12;
      if (ap < 1) curva(g, CABELO, 60, q => { q.moveTo(x - 10, y); q.quadraticCurveTo(x + 120, y + 80, x + 80, y + L * 0.8); }, 1 - ap);
      if (ap > 0) { curva(g, CABELO, 34, q => { q.moveTo(x - 20, y); q.lineTo(x + 50, y + 20); }, ap);
        for (let j = 0; j < 6; j++) { const xx = x + 50 + j * 9 + Math.sin(t * 1.6 + i) * j, yy = y + 28 + j * L / 6.4, d = j % 2 ? 1 : -1; elipse(g, xx + d * 11, yy, 38 - j * 2, 22 - j, CABELO, ap, d * 0.75); curva(g, '#6B4A32', 5, q => { q.moveTo(xx - d * 8, yy - 16); q.quadraticCurveTo(xx + d * 14, yy - 6, xx + d * 28, yy + 12); }, ap); }
        const px = x + 104 + Math.sin(t * 1.6 + i) * 6, py = y + 28 + L * 0.94; rect(g, px - 24, py - 10, 48, 18, P.accent, ap); for (let j = -1; j <= 1; j++) curva(g, CABELO, 9, q => { q.moveTo(px, py + 8); q.lineTo(px + j * 22, py + 62); }, ap); } }
    curva(g, CABELO, 34, q => { q.moveTo(470, 470); q.quadraticCurveTo(540, 440, 610, 500); q.lineTo(700, 580); }); g.restore();
    rect(g, 0, 1240, W, 44, TRONCO); rect(g, 0, 1370, W, 44, TRONCO); for (let x = 40; x < W; x += 330) rect(g, x, 1190, 55, 420, CASCA); fim(g); };

  // ───── som: açoite de cabelo (ar subindo e estalo seco)
  const ant = window.SfxExtra;
  window.SfxExtra = function (defs, h) {
    ant && ant(defs, h); const { G, F, N, C, dec, bus, eco } = h;
    defs.acoite = function (t, p) {
      const out = G(0.5 * (p.vol == null ? 1 : p.vol)), n = N(t, t + 0.2), bp = F('bandpass', 700, 2), g = G(0); bp.frequency.setValueAtTime(500, t); bp.frequency.exponentialRampToValueAtTime(4200, t + 0.17);
      g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(0.6, t + 0.15); g.gain.linearRampToValueAtTime(0, t + 0.19); C(n, bp, g, out);
      const n2 = N(t + 0.17, t + 0.34), hp = F('highpass', 1800), g2 = G(0); dec(g2.gain, t + 0.17, 0.001, 1, 0.025); C(n2, hp, g2, out);
      eco(out, out, 0.13, 0.25, 2800, 0.35); bus(out, false); return { t: t, fim: t + 0.8 };
    };
  };
})();
