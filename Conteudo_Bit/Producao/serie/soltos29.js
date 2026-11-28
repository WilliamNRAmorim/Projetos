// Cenários e som do Short solto 29 (Anhangá). Só ACRESCENTA ao Motor. Prefixo an_ = oliva escuro, mostarda de névoa, marfim e o vermelho da marca (brasa).
// Desenho próprio. Nenhum animal ferido: o veado nunca é atingido e o clarão do tiro é pequeno e local (nada de piscada em tela cheia).
(() => {
  const { CENARIOS } = Motor, W = Motor.W, { rect, circ, glow, vgrad, vinheta, lerp, clamp, out, rnd } = Motor.H_, RED = Motor.H_.P.accent;
  const TAU = Math.PI * 2, BREU = '#0C0E02', MUSGO = '#242905', OLIVA = '#5E6A10', MOST = '#E0C81C', NEVOA = '#F1E68C', MARF = '#FFFBE8', SOMBRA = '#CFC9A8', PELE = '#B9784C', COURO = '#7A3F14';
  const elipse = (g, x, y, rx, ry, c, a = 1) => { g.globalAlpha = a; g.fillStyle = c; g.beginPath(); g.ellipse(x, y, Math.max(0, rx), Math.max(0, ry), 0, 0, TAU); g.fill(); g.globalAlpha = 1; };
  const poli = (g, c, pts, a = 1) => { g.globalAlpha = a; g.fillStyle = c; g.beginPath(); pts.forEach(([x, y], i) => i ? g.lineTo(x, y) : g.moveTo(x, y)); g.closePath(); g.fill(); g.globalAlpha = 1; };
  const linha = (g, c, lw, pts, a = 1) => { g.globalAlpha = a; g.strokeStyle = c; g.lineWidth = lw; g.lineCap = 'square'; g.lineJoin = 'miter'; g.beginPath(); pts.forEach(([x, y], i) => i ? g.lineTo(x, y) : g.moveTo(x, y)); g.stroke(); g.globalAlpha = 1; };
  // palavra grande: encolhe sozinha para caber em `max` (margem lateral mesmo com o zoom da câmera)
  const texto = (g, s, x, y, tam, c, a = 1, borda = BREU, max = 840) => { if (a <= 0) return; g.save(); g.globalAlpha = a; g.font = `900 ${tam}px Geist`; const m = g.measureText(s).width; if (m > max) { tam = Math.floor(tam * max / m); g.font = `900 ${tam}px Geist`; } g.textAlign = 'center'; g.textBaseline = 'middle'; g.lineJoin = 'round'; if (borda) { g.strokeStyle = borda; g.lineWidth = tam * 0.17; g.strokeText(s, x, y); } g.fillStyle = c; g.fillText(s, x, y); g.restore(); };
  const fim = g => vinheta(g, 0.14);
  const C = (n, fn) => { fn.claro = true; CENARIOS['an_' + n] = fn; };
  const zoom = (g, k, cx, cy, fn) => { g.save(); g.translate(cx, cy); g.scale(k, k); g.translate(-cx, -cy); fn(); g.restore(); };
  const em = (g, x, y, s, fn, vira = 1) => { g.save(); g.translate(x, y); g.scale(s * vira, s); fn(); g.restore(); };
  const todo = (g, c, a = 1) => { g.globalAlpha = a; rect(g, -300, -700, W + 600, 3320, c); g.globalAlpha = 1; };
  const titulo = (g, a, b, t, d = 0.4, cb = MOST) => { texto(g, a, 540, 290, 170, '#FFFFFF'); if (b) texto(g, b, 540, 480, 180, cb, clamp((t - d) * 6)); };

  // ───── peças
  const tronco = (g, x, y, w, c) => { rect(g, x - w / 2, -400, w, y + 400, c); poli(g, c, [[x - w, y], [x - w / 2, y - w], [x + w / 2, y - w], [x + w, y]]); linha(g, c, w * 0.28, [[x, y - 800], [x + (x < 540 ? 1 : -1) * w * 1.7, y - 960]]); };
  function mata(g, t, o = {}) { todo(g, BREU); vgrad(g, 0, 1300, MUSGO, o.ceu || OLIVA, -300, W + 600); glow(g, 540, 960, 760, MOST, o.luz == null ? 0.5 : o.luz);
    for (let i = 0; i < 9; i++) tronco(g, i * 150 - 60 + rnd(i + 5) * 60, 1250, 24 + rnd(i + 9) * 18, '#3D460A');
    rect(g, -300, 1250, W + 600, 1500, MUSGO); for (const [x, w] of [[20, 90], [1065, 100]]) tronco(g, x, 1320, w, BREU);
    for (let i = 0; i < 46; i++) { const x = rnd(i + 70) * 1300 - 110, y = 1270 + rnd(i + 30) * 300; poli(g, BREU, [[x - 34, y], [x - 8, y - 50], [x, y - 8], [x + 12, y - 62], [x + 32, y]]); } }
  const nevoa = (g, t, a = 1) => { for (let i = 0; i < 7; i++) elipse(g, ((rnd(i + 3) * 1400 + t * (18 + i * 5)) % 1500) - 200, 1080 + i * 55, 380, 34 + rnd(i) * 26, NEVOA, 0.13 * a); };
  const olho = (g, x, y, r, a = 1) => { glow(g, x, y, r * 3.6, RED, 0.55 * a); elipse(g, x, y, r * 1.3, r, RED, a); circ(g, x, y, r * 0.38, '#FFD9A0', a); };
  const galhada = (g, k, c) => { for (const [a, b] of [[[40, 0], [150, -80]], [[150, -80], [165, -190]], [[110, -52], [90, -150]], [[150, -80], [235, -125]], [[162, -140], [215, -210]]]) linha(g, c, 20, [[k * a[0], a[1]], [k * b[0], b[1]]]); };
  // cabeça de frente; (0,0) = entre os olhos
  const cabeca = (g, cor = MARF, ol = 1) => { for (const k of [-1, 1]) { g.save(); g.translate(0, -90); galhada(g, k, cor); g.restore(); poli(g, cor, [[k * 75, -60], [k * 215, -105], [k * 105, 5]]); poli(g, SOMBRA, [[k * 100, -55], [k * 180, -82], [k * 108, -20]]); }
    poli(g, cor, [[-100, -105], [100, -105], [112, -20], [48, 150], [30, 190], [-30, 190], [-48, 150], [-112, -20]]); poli(g, SOMBRA, [[-38, 135], [38, 135], [24, 178], [-24, 178]]); rect(g, -24, 148, 48, 22, BREU); if (ol) for (const k of [-1, 1]) olho(g, k * 55, 0, 17, ol); };
  // veado; (x,y) = patas; vira = cabeça de perfil (0) a de frente (1)
  function veado(g, x, y, s, o = {}) { const v = o.vira == null ? 1 : o.vira, cor = o.cor || MARF; em(g, x, y, s, () => {
    glow(g, 0, -300, 460, MARF, o.brilho == null ? 0.35 : o.brilho);
    for (const [px, c] of [[-150, SOMBRA], [105, SOMBRA], [-95, cor], [160, cor]]) { poli(g, c, [[px - 24, -270], [px + 24, -270], [px + 12, -130], [px + 14, 0], [px - 14, 0], [px - 10, -130]]); rect(g, px - 17, -18, 34, 18, BREU); }
    poli(g, cor, [[-200, -340], [-120, -390], [150, -380], [215, -300], [170, -225], [-150, -230], [-210, -280]]); poli(g, cor, [[-200, -340], [-250, -385], [-205, -290]]);
    poli(g, cor, [[75, -350], [120, -520], [200, -520], [215, -300]]);
    if (v < 0.5) { em(g, 175, -545, 0.8, () => { g.save(); g.translate(-30, -70); galhada(g, -1, SOMBRA); galhada(g, 0.5, cor); g.restore(); poli(g, cor, [[-70, -75], [50, -70], [175, 15], [170, 60], [40, 55], [-60, 35]]); poli(g, cor, [[-60, -55], [-150, -110], [-40, -5]]); rect(g, 150, 22, 28, 26, BREU); if (o.olhos !== 0) olho(g, 35, -15, 18); }); }
    else em(g, 165, -540, 0.72, () => cabeca(g, cor, o.olhos === 0 ? 0 : 1)); }, o.lado || 1); }
  // cão de blocos; (x,y) = patas; olha para a direita. o.corre / o.bravo / o.baixo
  function cao(g, x, y, s, o = {}) { const c = o.cor || COURO, p = o.corre == null ? 0 : Math.sin(o.corre); em(g, x, y, s, () => { elipse(g, 0, 4, 170, 20, BREU, 0.55);
    [-110, -60, 70, 120].forEach((px, i) => { const dx = p * (i % 2 ? 55 : -55); linha(g, c, 30, [[px, -140], [px + dx, -14]]); });
    poli(g, c, [[-150, -215], [120, -220], [150, -130], [-130, -120]]); linha(g, c, 24, [[-140, -200], o.baixo ? [-170, -90] : [-215, -270]]);
    em(g, 150, o.baixo ? -170 : -245, 1, () => { poli(g, c, [[-75, -60], [30, -65], [60, -15], [145, -5], [145, 30], [40, 35], [-50, 50]]); poli(g, BREU, o.baixo ? [[-55, -45], [-120, 30], [-35, 5]] : [[-55, -55], [-45, -135], [0, -55]]); rect(g, 125, -8, 24, 22, BREU);
      if (o.bravo) { poli(g, c, [[35, 62], [135, 78], [128, 105], [20, 90]]); poli(g, '#3A0A04', [[40, 35], [145, 30], [135, 78], [35, 62]]); for (let i = 0; i < 4; i++) { poli(g, MARF, [[55 + i * 23, 33], [75 + i * 23, 32], [65 + i * 23, 55]]); poli(g, MARF, [[50 + i * 23, 65 + i * 3], [70 + i * 23, 68 + i * 3], [62 + i * 23, 45 + i * 3]]); } linha(g, MARF, 7, [[-5, -38], [40, -20]]); }
      circ(g, 12, -20, 9, o.bravo ? MOST : MARF); }); }, o.lado || 1); }
  // Orlando; (x,y) = pés; o.arma: 'ombro' | 'mira' ; o.corre
  function homem(g, x, y, s, o = {}) { const p = o.corre == null ? 0 : Math.sin(o.corre); em(g, x, y, s, () => { elipse(g, 0, 5, 130, 20, BREU, 0.55);
    for (const k of [-1, 1]) { linha(g, BREU, 58, [[k * 42, -230], [k * 50 + k * p * 90, -20]]); rect(g, k * 50 + k * p * 90 - 38, -34, 88, 34, '#050600'); }
    poli(g, COURO, [[-105, -470], [105, -470], [90, -215], [-90, -215]]); rect(g, -92, -270, 184, 28, BREU); rect(g, -12, -470, 24, 200, '#9A5620');
    rect(g, -62, -590, 124, 122, PELE); poli(g, '#E9E4D0', [[-62, -520], [62, -520], [45, -462], [-45, -462]]); for (const k of [-1, 1]) rect(g, k * 30 - 8, -560, 16, o.riso ? 7 : 18, BREU); if (o.riso) { rect(g, -34, -515, 68, 34, BREU); rect(g, -28, -515, 56, 11, MARF); }
    poli(g, MOST, [[-70, -590], [-55, -665], [55, -665], [70, -590]]); rect(g, -135, -600, 270, 24, MOST); rect(g, -62, -622, 124, 20, BREU);
    if (o.arma === 'mira') { linha(g, PELE, 34, [[-80, -440], [40, -400], [130, -430]]); linha(g, '#3B1E08', 34, [[-60, -400], [90, -432]]); linha(g, '#B7B7A8', 18, [[80, -440], [330, -462]]); }
    else if (o.arma === 'ombro') { linha(g, '#3B1E08', 34, [[130, -300], [100, -420]]); linha(g, '#B7B7A8', 18, [[103, -410], [55, -760]]); linha(g, PELE, 34, [[85, -440], [150, -340], [115, -320]]); }
    else for (const k of [-1, 1]) linha(g, PELE, 34, [[k * 90, -440], [k * 150 - k * p * 60, -300]]); }, o.lado || 1); }
  // olho gigante com o reflexo; u = quanto o reflexo aparece
  function olhao(g, t, u) { todo(g, BREU); glow(g, 540, 960, 760, RED, 0.45); poli(g, MARF, [[30, 960], [250, 730], [540, 640], [830, 730], [1050, 960], [830, 1170], [540, 1255], [250, 1170]]); poli(g, SOMBRA, [[30, 960], [250, 730], [540, 640], [830, 730], [1050, 960], [800, 790], [540, 710], [280, 790]]);
    circ(g, 540, 955, 280, RED); circ(g, 540, 955, 215, '#8E1206'); circ(g, 540, 955, 175, '#1A0300'); circ(g, 690, 820, 34, '#FFD9A0', 0.9); if (u > 0) { g.globalAlpha = u; encolhido(g, 540, 1075, 0.82); g.globalAlpha = 1; } }
  // reflexo: figura pequena, encolhida, de orelhas caídas, com o chapéu de Orlando
  function encolhido(g, x, y, s) { const c = MOST; g.save(); g.translate(x, y); g.scale(s, s); g.fillStyle = c; g.beginPath(); g.ellipse(0, -55, 105, 62, 0, 0, TAU); g.fill(); g.beginPath(); g.arc(0, -135, 66, 0, TAU); g.fill();
    for (const k of [-1, 1]) { g.fillStyle = c; g.fillRect(k * 28 - 10, -145, 20, 26); g.fillRect(k * 55 - 24, -14, 48, 22); g.fillStyle = '#A9780A'; g.beginPath(); g.moveTo(k * 38, -188); g.lineTo(k * 105, -178); g.lineTo(k * 150, -95); g.lineTo(k * 140, -20); g.lineTo(k * 102, -28); g.lineTo(k * 88, -105); g.lineTo(k * 52, -150); g.closePath(); g.fill(); }
    g.fillStyle = '#1A0300'; for (const k of [-1, 1]) g.fillRect(k * 28 - 9, -140, 18, 18); g.fillRect(-14, -105, 28, 16); g.fillStyle = c; g.fillRect(-85, -208, 170, 14); g.fillRect(-45, -245, 90, 40); g.restore(); }
  function varanda(g) { todo(g, '#8A6A12'); vgrad(g, 0, 1200, OLIVA, NEVOA, -300, W + 600); circ(g, 880, 820, 120, MARF); glow(g, 880, 820, 380, MOST, 0.8); rect(g, -300, 640, W + 600, 70, BREU); poli(g, BREU, [[-300, 640], [540, 560], [1380, 640]]); for (const x of [55, 1025]) rect(g, x - 25, 690, 50, 640, BREU); rect(g, -300, 1260, W + 600, 1500, COURO); rect(g, -300, 1260, W + 600, 18, BREU); for (let i = 0; i < 9; i++) rect(g, i * 160 - 100, 1275, 8, 700, BREU); }

  // ───── cenários (no gancho o texto fica abaixo da cartela de abertura)
  C('gancho', (g, t) => { mata(g, t); zoom(g, lerp(1, 1.06, clamp(t / 2.5)), 580, 1100, () => veado(g, 430, 1345, 0.82)); nevoa(g, t); texto(g, 'VEADO BRANCO?', 540, 560, 150, '#FFFFFF', 1, BREU, 900); texto(g, 'NÃO ATIRE', 540, 735, 180, RED, clamp((t - 0.25) * 6), MARF, 880); fim(g); });
  C('anhanga', (g, t) => { mata(g, t, { luz: 0.7 }); zoom(g, lerp(1, 1.1, clamp(t / 2)), 540, 960, () => { glow(g, 540, 940, 420, MARF, 0.7); em(g, 540, 980, 1.15, () => cabeca(g)); }); nevoa(g, t); titulo(g, 'ANHANGÁ', 'DOS TUPIS', t, 0.4); fim(g); });
  C('protege', (g, t) => { mata(g, t, { luz: 0.75 }); veado(g, 560, 1120, 0.72, { lado: -1 });
    // capivara, tatu e aves, todos tranquilos
    em(g, 245, 1290, 1, () => { poli(g, COURO, [[-150, -30], [-135, -150], [60, -165], [90, -200], [190, -195], [200, -115], [110, -95], [100, -30]]); rect(g, 80, -215, 28, 30, COURO); rect(g, 140, -165, 18, 18, BREU); for (const x of [-120, -60, 35, 70]) rect(g, x, -40, 28, 40, COURO); });
    em(g, 820, 1330, 1, () => { elipse(g, 0, -60, 125, 70, '#8F7A3C'); for (let i = -2; i < 3; i++) rect(g, i * 38 - 5, -125, 10, 110, BREU); poli(g, '#B49B52', [[95, -80], [200, -45], [95, -20]]); rect(g, 115, -65, 14, 14, BREU); for (const x of [-80, 45]) rect(g, x, -20, 30, 24, BREU); });
    for (const [x, y, f] of [[170, 720, 0], [900, 780, 2], [790, 660, 4]]) { const a = Math.sin(t * 7 + f) * 35; poli(g, MARF, [[x - 80, y - a], [x - 15, y], [x, y + 26], [x + 15, y], [x + 80, y - a], [x, y + 4]]); } nevoa(g, t); titulo(g, 'PROTETOR', 'DA MATA', t, 0.5); fim(g); });
  C('brasa', (g, t) => { todo(g, BREU); glow(g, 540, 940, 700, MOST, 0.35); zoom(g, lerp(1, 1.18, clamp(t / 3)), 540, 960, () => em(g, 540, 960, 2.1, () => cabeca(g))); nevoa(g, t, 0.7); titulo(g, 'OLHOS', 'DE BRASA', t, 1.2, RED); fim(g); });
  C('orlando', (g, t) => { mata(g, t, { ceu: '#8A7A14' }); zoom(g, lerp(1, 1.07, clamp(t / 2.5)), 540, 1100, () => homem(g, 540, 1350, 1.05)); texto(g, 'SEU ORLANDO', 540, 290, 150, '#FFFFFF'); texto(g, '30 ANOS', 540, 450, 150, MOST, clamp((t - 0.7) * 6)); texto(g, 'DE CAÇA', 540, 590, 110, MARF, clamp((t - 1) * 6)); fim(g); });
  C('arma', (g, t) => { mata(g, t, { ceu: '#2E3A12', luz: 0.3 }); circ(g, 870, 700, 80, MARF); glow(g, 870, 700, 300, MARF, 0.5); const x = lerp(0, 70, clamp(t / 3)); homem(g, 380 + x, 1290, 0.85, { arma: 'ombro', corre: t * 3 }); cao(g, 700 + x, 1300, 0.72, { corre: t * 6 }); cao(g, 190 + x, 1370, 0.78, { corre: t * 6 + 2, cor: '#C9A45A' }); titulo(g, 'ESPINGARDA', 'E DOIS CÃES', t, 0.9); fim(g); });
  C('neblina', (g, t) => { mata(g, t, { luz: 0.65 }); const a = clamp((t - 0.5) / 1.6); veado(g, 480, 1230, 0.62, { cor: NEVOA, olhos: 0, brilho: 0.6 * a }); for (let i = 0; i < 9; i++) elipse(g, 540 + Math.sin(t * 0.8 + i) * 120, 760 + i * 70, 620, 70, NEVOA, lerp(0.22, 0.09, a)); titulo(g, 'NA', 'NEBLINA', t, 0.4); fim(g); });
  C('veado', (g, t) => { mata(g, t); zoom(g, lerp(1.12, 1, out(clamp(t / 0.4))), 540, 1050, () => veado(g, 420, 1340, 1)); nevoa(g, t); titulo(g, 'UM VEADO', 'BRANCO', t, 0.2, MARF); fim(g); });
  C('olhos', (g, t) => { todo(g, BREU); const a = clamp(t * 3); em(g, 540, 960, 2.3, () => cabeca(g, '#4A4A30', 0)); for (const k of [-1, 1]) olho(g, 540 + k * 127, 960, 52 + Math.sin(t * 5) * 3, a); titulo(g, 'OLHOS', 'ACESOS', t, 0.5, RED); fim(g); });
  C('fugiram', (g, t) => { mata(g, t, { luz: 0.35 }); const x = t * 190; cao(g, 700 - x, 1220, 0.85, { lado: -1, corre: t * 14, baixo: true }); cao(g, 940 - x, 1370, 0.95, { lado: -1, corre: t * 14 + 2, baixo: true, cor: '#C9A45A' }); for (let i = 0; i < 6; i++) linha(g, NEVOA, 10, [[860 + (i % 3) * 60, 960 + i * 75], [1010 + (i % 3) * 60, 960 + i * 75]], 0.75); titulo(g, 'OS CÃES', 'FUGIRAM', t, 0.4); fim(g); });
  C('riu', (g, t) => { mata(g, t, { ceu: '#8A7A14' }); zoom(g, lerp(1, 1.08, clamp(t / 1.3)), 540, 1000, () => homem(g, 540, 1720 + Math.sin(t * 22) * 8, 1.75, { riso: true })); titulo(g, 'ORLANDO', 'RIU', t, 0.2); fim(g); });
  C('atirou', (g, t) => { mata(g, t, { luz: 0.35 }); const atirou = t > 1.35, k = atirou ? Math.max(0, 1 - (t - 1.35) * 5) : 0; homem(g, 330 - k * 22, 1340, 0.98, { arma: 'mira' }); const bx = 330 - k * 22 + 340, by = 1340 - 454;
    if (atirou) { const u = clamp((t - 1.35) / 1.2); for (let i = 0; i < 5; i++) elipse(g, bx + 40 + i * 38 * u, by - i * 28 * u, 34 + 60 * u, 28 + 42 * u, SOMBRA, 0.5 * (1 - u * 0.7)); if (k > 0) { poli(g, MOST, [[bx - 5, by], [bx + 75, by - 55], [bx + 62, by - 12], [bx + 150, by], [bx + 62, by + 14], [bx + 75, by + 55]], k); glow(g, bx + 40, by, 200, MOST, 0.8 * k); } }
    texto(g, 'ERGUEU', 540, 290, 170, '#FFFFFF'); texto(g, 'ATIROU', 540, 490, 200, RED, atirou ? 1 : 0, MARF); fim(g); });
  C('parado', (g, t) => { mata(g, t, { luz: 0.7 }); veado(g, 420, 1340, 0.95, { vira: 0 }); for (let i = 0; i < 4; i++) elipse(g, 130 + i * 70 + t * 40, 900 + i * 45, 120, 60, SOMBRA, 0.25 * (1 - clamp(t / 2.5))); nevoa(g, t); titulo(g, 'NEM SE', 'MEXEU', t, 0.6, MARF); fim(g); });
  C('virou', (g, t) => { const v = clamp((t - 0.5) / 1.8); mata(g, t, { luz: lerp(0.6, 0.2, v) }); zoom(g, lerp(1, 1.14, clamp(t / 3)), 650, 950, () => veado(g, 390, 1340, 1, { vira: v < 0.55 ? 0 : 1 })); nevoa(g, t); titulo(g, 'VIROU A', 'CABEÇA', t, 0.5); texto(g, 'DEVAGAR', 540, 660, 110, MARF, clamp((t - 1.2) * 4)); fim(g); });
  C('pupilas', (g, t) => { zoom(g, lerp(0.92, 1.08, clamp(t / 3)), 540, 960, () => olhao(g, t, clamp((t - 2) / 1.2) * 0.5)); titulo(g, 'NAS', 'PUPILAS', t, 0.4, RED); fim(g); });
  C('reflexo', (g, t) => { zoom(g, lerp(1.08, 1.28, clamp(t / 3.2)), 540, 980, () => olhao(g, t, clamp(0.5 + t * 2))); titulo(g, 'O PRÓPRIO', 'REFLEXO', t, 0.2); fim(g); });
  C('galho', (g, t) => { mata(g, t, { ceu: '#2E3A12', luz: 0.25 }); homem(g, 280, 1330, 0.8, { arma: 'ombro' }); const u = out(clamp((t - 0.45) / 0.25)); g.save(); g.translate(760, 1120); linha(g, COURO, 46, [[-210, -u * 20], [-8, u * 70]]); linha(g, COURO, 46, [[8 + u * 40, u * 85], [230, -20 + u * 30]]); linha(g, COURO, 20, [[-120, 0], [-150, -90]]); linha(g, COURO, 20, [[120, 20], [170, -80]]); if (u > 0) for (let i = 0; i < 7; i++) { const a = i / 7 * TAU; linha(g, MARF, 12, [[Math.cos(a) * 70, 40 + Math.sin(a) * 70], [Math.cos(a) * (95 + 40 * u), 40 + Math.sin(a) * (95 + 40 * u)]]); } g.restore(); texto(g, 'CRAC', 540, 340, 300, MOST, clamp((t - 0.45) * 8)); texto(g, 'ATRÁS DELE', 540, 550, 130, '#FFFFFF', clamp((t - 0.9) * 5)); fim(g); });
  C('correu', (g, t) => { const u = clamp(t / 2.2); mata(g, t, { ceu: u > 0.5 ? '#B89418' : '#4A540E', luz: lerp(0.2, 0.9, u) }); circ(g, 840, lerp(1180, 760, u), 105, MARF); glow(g, 840, lerp(1180, 760, u), 360, MOST, 0.8); g.save(); g.translate(500, 1100); g.rotate(0.18); homem(g, 0, 240, 0.9, { corre: t * 13 }); g.restore(); for (let i = 0; i < 5; i++) linha(g, NEVOA, 12, [[60, 880 + i * 95], [250 - (i % 2) * 60, 880 + i * 95]], 0.7); titulo(g, 'CORREU ATÉ', 'AMANHECER', t, 0.6); fim(g); });
  C('varanda', (g, t) => { varanda(g); homem(g, 230, 1340, 0.82); const a = lerp(80, 0, out(clamp(t / 1.2))); cao(g, 800 + a, 1270, 0.82, { lado: -1, bravo: true, cor: '#4A2408' }); cao(g, 760 + a, 1390, 0.9, { lado: -1, bravo: true, cor: '#2A1604' }); titulo(g, 'OS CÃES', 'ROSNARAM', t, 1.4, RED); fim(g); });
  C('dentes', (g, t) => { todo(g, '#8A6A12'); glow(g, 540, 960, 700, NEVOA, 0.7); const j = Math.sin(t * 20) * 7; zoom(g, lerp(1, 1.1, clamp(t / 2.5)), 540, 1050, () => { cao(g, 770 + j, 1500, 2.2, { lado: -1, bravo: true, cor: '#3A1E06' }); }); titulo(g, 'DENTES', 'À MOSTRA', t, 0.7, MOST); fim(g); });
  C('caca', (g, t) => { varanda(g); todo(g, BREU, lerp(0.05, 0.3, clamp(t / 1.5))); const u = out(clamp((t - 0.5) / 0.8));
    zoom(g, lerp(1, 1.08, clamp(t / 2.5)), 540, 1050, () => { homem(g, 540, 1300, 1.05);
      // as orelhas caídas aparecem nele
      if (u > 0) for (const k of [-1, 1]) { const x = 540 + k * 70, y = 705; poli(g, COURO, [[x, y], [x + k * 90 * u, y + 15], [x + k * 135 * u, y + 90 * u], [x + k * 115 * u, y + 200 * u], [x + k * 60 * u, y + 180 * u], [x + k * 40 * u, y + 65 * u], [x - k * 10, y + 35]]); linha(g, BREU, 9, [[x + k * 90 * u, y + 15], [x + k * 135 * u, y + 90 * u], [x + k * 115 * u, y + 200 * u]]); }
      cao(g, 185, 1290, 0.8, { bravo: true, cor: '#3A1E06' }); cao(g, 895, 1290, 0.8, { lado: -1, bravo: true, cor: '#3A1E06' }); });
    titulo(g, 'COMO SE FOSSE', 'A CAÇA', t, 0.7, RED); fim(g); });
  // arte da capa (sem texto): o veado branco de frente na névoa; fundo contínuo até o topo
  C('capaarte', g => { todo(g, BREU); vgrad(g, -100, 1500, BREU, '#8E8A14', -300, W + 600); glow(g, 540, 1100, 720, MOST, 0.75); for (let i = 0; i < 8; i++) { const x = i < 4 ? i * 85 - 20 : 775 + (i - 4) * 100; rect(g, x, 640 + rnd(i) * 80, 30, 900, BREU, 0.8); } rect(g, -300, 1500, W + 600, 900, MUSGO); glow(g, 540, 1020, 420, MARF, 0.75); em(g, 540, 1080, 1.9, () => cabeca(g)); for (let i = 0; i < 4; i++) elipse(g, 200 + i * 250, 1440 + (i % 2) * 60, 360, 50, NEVOA, 0.18); });

  // ───── som: tiro abafado, estalo de galho, choro e rosnado dos cães, sintetizados aqui
  const ant = window.SfxExtra;
  window.SfxExtra = function (defs, h) {
    ant && ant(defs, h); const { G, F, O, N, C: L, dec, bus } = h, vol = p => p.vol == null ? 1 : p.vol;
    defs.tiroSeco = function (t, p) { const saida = G(vol(p)), nz = N(t, t + 0.9), lp = F('lowpass', 1800, 0.7), e = G(0), o = O('sine', 110, t, t + 0.5), eo = G(0); lp.frequency.setValueAtTime(3200, t); lp.frequency.exponentialRampToValueAtTime(220, t + 0.6); dec(e.gain, t, 0.002, 1, 0.16); o.frequency.setValueAtTime(110, t); o.frequency.exponentialRampToValueAtTime(38, t + 0.3); dec(eo.gain, t, 0.004, 0.9, 0.14); L(nz, lp, e, saida); L(o, eo, saida); bus(saida, false); return { t, fim: t + 0.9 }; };
    defs.galhoSeco = function (t, p) { const saida = G(vol(p)); [[0, 2600], [0.07, 1500], [0.1, 3400]].forEach(([a, f]) => { const nz = N(t + a, t + a + 0.12), bp = F('bandpass', f, 2), e = G(0); dec(e.gain, t + a, 0.001, 1, 0.018); L(nz, bp, e, saida); }); bus(saida, false); return { t, fim: t + 0.4 }; };
    defs.choroCao = function (t, p) { const saida = G(vol(p)); for (let i = 0; i < 3; i++) { const a = t + i * 0.32, o = O('triangle', 900, a, a + 0.26), e = G(0); o.frequency.setValueAtTime(760 - i * 50, a); o.frequency.linearRampToValueAtTime(1080 - i * 60, a + 0.08); o.frequency.exponentialRampToValueAtTime(520, a + 0.24); e.gain.setValueAtTime(0, a); e.gain.linearRampToValueAtTime(1, a + 0.04); e.gain.linearRampToValueAtTime(0, a + 0.25); L(o, e, saida); } bus(saida, false); return { t, fim: t + 1 }; };
    defs.rosnado = function (t, p) { const d = p.dur || 2, saida = G(vol(p)), env = G(0), lp = F('lowpass', 520, 3), am = G(0.65), lfo = O('square', 27, t, t + d), prof = G(0.35); env.gain.setValueAtTime(0, t); env.gain.linearRampToValueAtTime(1, t + 0.25); env.gain.setValueAtTime(1, t + d - 0.25); env.gain.linearRampToValueAtTime(0, t + d); L(lfo, prof); prof.connect(am.gain); for (const f of [71, 96]) { const o = O('sawtooth', f, t, t + d); L(o, lp); } L(lp, am, env, saida); bus(saida, false); return { t, fim: t + d }; };
  };
})();
