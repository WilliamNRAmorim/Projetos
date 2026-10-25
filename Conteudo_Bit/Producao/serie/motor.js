// Motor de episódios de animação 2D flat (vertical 1080x1920, 30 fps). Data-driven: um episódio é um JSON (ver README.md).
// Usa brand.js (BRAND, grain, loadBrandFonts) da pasta Producao. Cenários, personagens e objetos são formas vetoriais no canvas;
// PNGs em assets/ são opcionais (se existirem, entram como camadas; se não, vale o vetor).
window.Motor = (() => {
  const W = 1080, H = 1920, FPS = 30, GY = 1240; // GY = linha dos pés dos personagens
  const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x)), out = x => 1 - Math.pow(1 - x, 3), lerp = (a, b, k) => a + (b - a) * k;
  const back = x => { const c = 1.9; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); }; // entrada com leve estouro
  const rnd = n => { const s = Math.sin(n * 127.1) * 43758.5453; return s - Math.floor(s); };
  // paleta de terror: tons escuros quentes + UM destaque (o vermelho da marca); papel = fundo bege de infográfico
  const P = { wall: '#1A1819', wall2: '#221F23', floor: '#111012', deep: '#0C0C0D', mid: '#2E2B31', lite: '#6F6B72', paper: '#EEEDE8', moon: '#CFCBC0', accent: '#FF3B1F', orange: '#FF8A1F', bege: '#E6D9C3' };
  const rect = (g, x, y, w, h, c, a = 1) => { g.globalAlpha = a; g.fillStyle = c; g.fillRect(x, y, w, h); g.globalAlpha = 1; };
  const poly = (g, pts, c, a = 1) => { g.globalAlpha = a; g.fillStyle = c; g.beginPath(); pts.forEach(([x, y], i) => i ? g.lineTo(x, y) : g.moveTo(x, y)); g.closePath(); g.fill(); g.globalAlpha = 1; };
  const circ = (g, x, y, r, c, a = 1) => { g.globalAlpha = a; g.fillStyle = c; g.beginPath(); g.arc(x, y, r, 0, Math.PI * 2); g.fill(); g.globalAlpha = 1; };
  const line = (g, x1, y1, x2, y2, c, w, a = 1) => { g.globalAlpha = a; g.strokeStyle = c; g.lineWidth = w; g.lineCap = 'round'; g.beginPath(); g.moveTo(x1, y1); g.lineTo(x2, y2); g.stroke(); g.globalAlpha = 1; };
  const rrect = (g, x, y, w, h, r, c, a = 1) => { g.globalAlpha = a; g.fillStyle = c; g.beginPath(); g.roundRect(x, y, w, h, r); g.fill(); g.globalAlpha = 1; };
  const text = (g, s, x, y, size, c, o = {}) => { g.font = `${o.w || 900} ${size}px ${o.mono ? '"Geist Mono"' : 'Geist'}`; g.letterSpacing = o.mono ? '0px' : `${-0.03 * size}px`; g.textAlign = o.align || 'left'; g.textBaseline = 'alphabetic'; g.fillStyle = c; g.fillText(s, x, y); g.textAlign = 'left'; };
  // luz e sombra suaves (gradientes) para os cenários de terror
  const rgba = (h, a) => `rgba(${parseInt(h.slice(1, 3), 16)},${parseInt(h.slice(3, 5), 16)},${parseInt(h.slice(5, 7), 16)},${a})`;
  const vgrad = (g, y0, y1, c0, c1, x = 0, w = W) => { const gr = g.createLinearGradient(0, y0, 0, y1); gr.addColorStop(0, c0); gr.addColorStop(1, c1); g.fillStyle = gr; g.fillRect(x, y0, w, y1 - y0); };
  const glow = (g, x, y, r, c, a) => { const gr = g.createRadialGradient(x, y, 0, x, y, r); gr.addColorStop(0, rgba(c, a)); gr.addColorStop(1, rgba(c, 0)); g.fillStyle = gr; g.fillRect(x - r, y - r, 2 * r, 2 * r); };
  const vinheta = (g, a = 0.6) => { const gr = g.createRadialGradient(W / 2, H * 0.45, 300, W / 2, H * 0.5, 1250); gr.addColorStop(0, 'rgba(8,8,10,0)'); gr.addColorStop(1, `rgba(8,8,10,${a})`); g.fillStyle = gr; g.fillRect(0, 0, W, H); };
  const chuva = (g, t, n = 110, a = 0.2, y0 = 0, y1 = H) => { g.save(); g.strokeStyle = '#A9B2C3'; g.lineWidth = 3; g.lineCap = 'round'; const span = y1 - y0 + 200;
    for (let i = 0; i < n; i++) { const sp = 1500 + rnd(i + 1) * 700, y = y0 - 100 + ((rnd(i + 2) * span + t * sp) % span), x = rnd(i) * (W + 300) - (y - y0) * 0.12; g.globalAlpha = a * (0.45 + rnd(i + 4) * 0.55); g.beginPath(); g.moveTo(x, y); g.lineTo(x - 6, y + 46); g.stroke(); }
    g.restore(); };
  const LUZ = '#E8DFC8'; // luz de lâmpada (quente, clara); o vermelho fica só para o quarto 7
  const AMBAR = '#F2B33D', CINZA = '#9C9A98', SOL = '#FFD98A'; // lâmpada de emergência, pele gelada da Dalva, amanhecer
  function chaveCorda(g, x, y, s, rot = 0, cor = '#C9B38A') { // chave de dar corda no relógio: borboleta em cima (origem), haste para baixo
    g.save(); g.translate(x, y); g.rotate(rot); g.scale(s, s);
    g.fillStyle = cor; g.beginPath(); g.ellipse(-34, 0, 34, 22, 0, 0, Math.PI * 2); g.ellipse(34, 0, 34, 22, 0, 0, Math.PI * 2); g.fill();
    circ(g, -38, 0, 9, '#2A211B'); circ(g, 38, 0, 9, '#2A211B'); rect(g, -9, -6, 18, 70, cor); rect(g, -14, 58, 28, 26, cor); rect(g, -6, 64, 12, 12, '#2A211B');
    g.restore();
  }
  function sofaFrente(g, cx, base, s = 1, cor = '#3B2A2E') { // sofá do saguão de frente (quem senta é desenhado por cima, pose 'sentada' com a mesma escala)
    g.save(); g.translate(cx, base); g.scale(s, s);
    g.fillStyle = 'rgba(0,0,0,0.4)'; g.beginPath(); g.ellipse(0, 6, 480, 26, 0, 0, Math.PI * 2); g.fill();
    rrect(g, -400, -470, 800, 360, 26, cor); rrect(g, -400, -470, 800, 40, 20, 'rgba(255,255,255,0.05)');
    for (const k of [-1, 0, 1]) { rrect(g, k * 262 - 122, -444, 244, 296, 18, 'rgba(0,0,0,0.13)'); circ(g, k * 262, -300, 7, 'rgba(0,0,0,0.3)'); }
    rrect(g, -380, -152, 760, 100, 16, '#4A353A'); rect(g, -380, -60, 760, 52, '#2C1F23');
    rrect(g, -462, -300, 112, 292, 24, '#45313A'); rrect(g, 350, -300, 112, 292, 24, '#45313A'); rrect(g, -462, -300, 112, 30, 14, 'rgba(255,255,255,0.05)'); rrect(g, 350, -300, 112, 30, 14, 'rgba(255,255,255,0.05)');
    rect(g, -432, -10, 24, 14, '#120E10'); rect(g, 408, -10, 24, 14, '#120E10'); g.restore();
  }
  function sofaCostas(g, cx, base, s = 1, vulto = true, t = 0) { // sofá visto por trás; o vulto (cabeça com coque) aparece acima do encosto, quase parado
    g.save(); g.translate(cx, base); g.scale(s, s);
    if (vulto) { const r = Math.sin(t * 0.8) * 2;
      rrect(g, -160, -560 + r, 320, 220, 80, '#0C0A0D'); circ(g, 0, -640 + r, 84, '#0C0A0D'); circ(g, -6, -732 + r, 40, '#1C191E');
      g.strokeStyle = rgba(LUZ, 0.18); g.lineWidth = 5; g.beginPath(); g.arc(0, -640 + r, 86, Math.PI * 1.1, Math.PI * 1.6); g.stroke(); }
    rrect(g, -450, -450, 900, 450, 30, '#2E2125'); rrect(g, -450, -450, 900, 36, 24, 'rgba(255,255,255,0.05)');
    for (let x = -390; x <= 390; x += 130) line(g, x, -400, x, -40, 'rgba(0,0,0,0.22)', 5);
    rect(g, -420, -4, 26, 14, '#120E10'); rect(g, 394, -4, 26, 14, '#120E10'); g.restore();
  }
  function maoNoPonteiro(g, r, seg, cor = '#D9A441', pele = '#C99A74') { // mão da Bia segurando o ponteiro dos minutos (relógio de raio r na origem)
    const a = ((seg / 60) % 60) / 60 * Math.PI * 2, px = Math.sin(a) * r * 0.5, py = -Math.cos(a) * r * 0.5;
    line(g, px + 40, py + 60, px + 330, py + 520, cor, 96); line(g, px + 30, py + 40, px + 90, py + 130, pele, 60);
    circ(g, px, py, 40, pele); for (let i = 0; i < 4; i++) rrect(g, px - 44 + i * 22, py - 54, 20, 50, 10, '#B88A66'); rrect(g, px + 26, py - 20, 22, 48, 11, '#B88A66');
  }
  function onibus(g, x, yb, e, o = {}) { // ônibus de lado, origem no meio da base (rodas no chão)
    g.save(); g.translate(x, yb); g.scale(e, e);
    g.fillStyle = 'rgba(0,0,0,0.45)'; g.beginPath(); g.ellipse(0, 6, 420, 26, 0, 0, Math.PI * 2); g.fill();
    rect(g, -380, -300, 760, 270, '#2B2E37'); rect(g, -380, -300, 760, 24, '#353843'); rect(g, -380, -78, 760, 40, '#22242B');
    if (o.faixa) { rect(g, -380, -144, 760, 10, '#4A4E5C'); rect(g, -380, -296, 760, 4, '#565B6B'); } // friso lateral e reflexo da lua no teto
    for (let i = 0; i < 6; i++) { const wx = -350 + i * 104; rect(g, wx, -256, 90, 104, '#14161C'); rect(g, wx + 4, -252, 82, 96, LUZ, o.luz ?? 0.16); if (o.bancos && o.bia !== i) { rrect(g, wx + 14, -196, 26, 40, 8, '#0E0F14', 0.8); rrect(g, wx + 52, -196, 26, 40, 8, '#0E0F14', 0.8); } // encostos vazios
      if (o.bia === i) { // Bia na janela: janela acesa (o.biaLuz), ombros de moletom amarelo, rosto encostado no vidro olhando para fora
        g.save(); g.beginPath(); g.rect(wx + 4, -252, 82, 96); g.clip(); rect(g, wx + 4, -252, 82, 96, LUZ, o.biaLuz ?? 0.3); glow(g, wx + 45, -200, 90, '#FFE9B8', 0.35 * (o.biaLuz ?? 0.3) / 0.3);
        rrect(g, wx + 6, -178, 78, 40, 14, '#D9A441'); rect(g, wx + 6, -178, 78, 40, 'rgba(0,0,0,0.12)'); // ombros
        rrect(g, wx + 18, -240, 60, 80, 26, '#2B1D16'); // cabelo comprido (atrás da cabeça)
        circ(g, wx + 48, -206, 27, '#C99A74'); g.fillStyle = '#2B1D16'; g.beginPath(); g.arc(wx + 48, -208, 29, Math.PI * 0.98, Math.PI * 2.02); g.quadraticCurveTo(wx + 60, -232, wx + 40, -228); g.fill();
        circ(g, wx + 58, -204, 3.4, P.deep); circ(g, wx + 72, -204, 3.4, P.deep); line(g, wx + 60, -190, wx + 70, -191, P.deep, 2.4); // olhando para fora, séria
        rect(g, wx + 4, -252, 82, 96, '#FFFFFF', 0.06); line(g, wx + 10, -246, wx + 40, -170, '#FFFFFF', 3, 0.12); g.restore(); } } // reflexo no vidro
    rect(g, 262, -256, 70, 226, '#14161C'); rect(g, 266, -252, 62, 218, LUZ, o.porta ? 0.6 : 0.12); // porta
    poly(g, [[340, -256], [380, -256], [380, -120], [340, -120]], '#1C1F27'); // para-brisa
    circ(g, -250, -26, 46, '#0A0A0C'); circ(g, -250, -26, 18, '#3A3A40'); circ(g, 250, -26, 46, '#0A0A0C'); circ(g, 250, -26, 18, '#3A3A40');
    glow(g, 384, -70, 120, LUZ, 0.5); circ(g, 380, -70, 12, LUZ); poly(g, [[384, -90], [1100, -200], [1100, 120], [384, -50]], LUZ, 0.05); // farol
    rect(g, -386, -96, 10, 34, P.accent, 0.9); glow(g, -386, -80, 70, P.accent, 0.25); // lanterna
    g.restore();
  }
  function relogioFace(g, cx, cy, r, seg, flash = 0) { // relógio de parede: seg = segundos desde a meia-noite
    circ(g, cx + 10, cy + 14, r + 22, '#000', 0.35); circ(g, cx, cy, r + 22, '#3A2E26'); circ(g, cx, cy, r + 10, '#2A211B'); circ(g, cx, cy, r, '#E8E1CF');
    glow(g, cx - r * 0.3, cy - r * 0.35, r * 0.9, '#FFFFFF', 0.25);
    for (let i = 0; i < 60; i++) { const a = i / 60 * Math.PI * 2, big = i % 5 === 0, r1 = r * (big ? 0.8 : 0.88); line(g, cx + Math.sin(a) * r1, cy - Math.cos(a) * r1, cx + Math.sin(a) * r * 0.93, cy - Math.cos(a) * r * 0.93, big ? '#1A1819' : '#6F6B72', big ? r * 0.045 : r * 0.015); }
    g.font = `900 ${r * 0.2}px Geist`; g.letterSpacing = '0px'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillStyle = flash > 0 ? P.accent : '#1A1819'; g.fillText('12', cx, cy - r * 0.62); g.textBaseline = 'alphabetic'; g.textAlign = 'left';
    const h = (seg / 3600) % 12, m = (seg / 60) % 60, s = Math.floor(seg) % 60, hand = (a, L, w, c) => line(g, cx - Math.sin(a) * L * 0.15, cy + Math.cos(a) * L * 0.15, cx + Math.sin(a) * L, cy - Math.cos(a) * L, c, w);
    hand(h / 12 * Math.PI * 2, r * 0.5, r * 0.07, '#1A1819'); hand(m / 60 * Math.PI * 2, r * 0.76, r * 0.05, '#1A1819'); hand(s / 60 * Math.PI * 2, r * 0.82, r * 0.018, P.accent); circ(g, cx, cy, r * 0.06, '#1A1819');
    if (flash > 0) { g.globalAlpha = flash; g.strokeStyle = P.accent; g.lineWidth = r * 0.06; g.beginPath(); g.arc(cx, cy, r + 30, 0, Math.PI * 2); g.stroke(); g.globalAlpha = 1; glow(g, cx, cy, r * 1.8, P.accent, 0.3 * flash); }
  }
  function painelDesenho(g, cx, cy, w, acesa = 0, alvo = 7) { // painel de campainhas dos 7 quartos; acesa = brilho da luz do quarto "alvo"
    const h = w * 0.42, x0 = cx - w / 2, y0 = cy - h / 2, cw = w / 7;
    rect(g, x0 + 12, y0 + 16, w, h, '#000', 0.35); rect(g, x0 - 10, y0 - 10, w + 20, h + 20, '#4A3B30'); rect(g, x0, y0, w, h, '#211B18');
    for (let i = 0; i < 7; i++) { const bx = x0 + cw * (i + 0.5), on = i + 1 === alvo ? acesa : 0;
      circ(g, bx, y0 + h * 0.24, cw * 0.16, on ? P.accent : '#3A332E'); if (on) glow(g, bx, y0 + h * 0.24, cw * 1.1, P.accent, 0.55 * on);
      circ(g, bx, y0 + h * 0.55, cw * 0.3, '#8C7A5E'); circ(g, bx - cw * 0.08, y0 + h * 0.5, cw * 0.1, '#C9B38A', 0.7);
      g.font = `800 ${cw * 0.34}px Geist`; g.letterSpacing = '0px'; g.textAlign = 'center'; g.fillStyle = on ? P.accent : '#BDB3A0'; g.fillText(String(i + 1), bx, y0 + h * 0.93); g.textAlign = 'left'; }
  }

  // ───────────── CENÁRIOS (cada um desenha o quadro inteiro; t = segundos desde o início da cena) ─────────────
  const CENARIOS = {
    quarto_noite(g, t) {
      rect(g, 0, 0, W, 1120, P.wall); rect(g, 0, 1120, W, H - 1120, P.floor);
      for (let i = 0; i < 9; i++) rect(g, 0, 1140 + i * 90, W, 3, P.deep);
      rect(g, 0, 1090, W, 30, P.deep);
      poly(g, [[660, 1120], [980, 1120], [1080, 1500], [560, 1500]], P.moon, 0.05); // luz da lua no chão
      rect(g, 636, 296, 332, 472, P.deep); rect(g, 652, 312, 300, 440, '#20232B'); // janela
      circ(g, 850, 440, 52, P.moon); circ(g, 872, 424, 46, '#20232B'); // lua crescente
      rect(g, 800, 312, 12, 440, P.deep); rect(g, 652, 520, 300, 12, P.deep);
      const sway = Math.sin(t * 0.8) * 6; poly(g, [[600, 270], [700 + sway, 270], [690 + sway, 1000], [600, 1000]], '#2A2023'); // cortina
      for (let i = 0; i < 4; i++) line(g, 622 + i * 20 + sway * 0.5, 280, 618 + i * 20 + sway, 990, P.deep, 4, 0.6);
      rect(g, 0, 760, 36, 360, P.deep); rect(g, 0, 940, 440, 180, '#2B2830'); rect(g, 0, 900, 150, 70, '#4A4650'); rect(g, 150, 940, 290, 90, '#3A2E33'); // cama
      rect(g, 470, 980, 150, 140, P.mid); rect(g, 470, 972, 150, 12, '#3A363D'); // criado-mudo
      rect(g, 490, 910, 110, 62, P.deep); text(g, Math.floor(t * 1.6) % 2 ? '03 17' : '03:17', 545, 958, 38, P.accent, { mono: 1, w: 700, align: 'center' });
      circ(g, 545, 940, 90, P.accent, 0.04);
    },
    corredor(g, t) {
      const L = 380, R = 700, T = 560, B = 960;
      rect(g, 0, 0, W, H, P.deep);
      poly(g, [[0, 0], [W, 0], [R, T], [L, T]], '#0E0D0F'); poly(g, [[0, H], [W, H], [R, B], [L, B]], '#16141A');
      poly(g, [[0, 0], [L, T], [L, B], [0, H]], P.wall); poly(g, [[W, 0], [R, T], [R, B], [W, H]], P.wall2);
      rect(g, L, T, R - L, B - T, '#0A0A0B');
      for (let i = -3; i <= 3; i++) line(g, 540 + i * 120, 960, 540 + i * 420, H, '#1E1B22', 3);
      const wallL = x => [lerp(0, T, x / L), lerp(H, B, x / L)], wallR = x => [lerp(0, T, (W - x) / (W - R)), lerp(H, B, (W - x) / (W - R))];
      const door = (wall, sgn, x1, x2, glow) => { const [t1, b1] = wall(x1), [t2, b2] = wall(x2), h1 = b1 - t1, h2 = b2 - t2;
        poly(g, [[x1, t1 + h1 * 0.2], [x2, t2 + h2 * 0.2], [x2, b2], [x1, b1]], '#0E0D0F'); poly(g, [[x1 + 8 * sgn, t1 + h1 * 0.23], [x2 - 4 * sgn, t2 + h2 * 0.23], [x2 - 4 * sgn, b2 - 4], [x1 + 8 * sgn, b1 - 6]], '#2A2124');
        if (glow) poly(g, [[x1, b1 - 8], [x2, b2 - 4], [x2, b2], [x1, b1]], P.accent, 0.9); };
      door(wallL, 1, 40, 190, false); door(wallL, 1, 250, 330, true); door(wallR, -1, 890, 1040, false); door(wallR, -1, 760, 830, false);
      const on = rnd(Math.floor(t * 10)) > 0.25 ? 1 : 0.35; // lâmpada do fundo falhando
      rect(g, 500, 600, 80, 14, P.paper, 0.9 * on); poly(g, [[500, 614], [580, 614], [760, 1500], [320, 1500]], P.paper, 0.045 * on);
      rect(g, 505, 800, 70, 160, '#15141A');
    },
    casa_fora_noite(g, t) {
      rect(g, 0, 0, W, 1100, '#0F0F13'); rect(g, 0, 1100, W, H - 1100, '#0D0D0F');
      for (let i = 0; i < 40; i++) circ(g, rnd(i) * W, rnd(i + 99) * 700, 1.5 + rnd(i + 5) * 2, P.paper, 0.2 + 0.5 * rnd(i + 9) * (0.7 + 0.3 * Math.sin(t * 2 + i)));
      circ(g, 200, 300, 150, P.moon, 0.05); circ(g, 200, 300, 96, P.moon); circ(g, 236, 280, 90, '#0F0F13');
      for (let i = 0; i < 6; i++) { const x = 20 + i * 200 + rnd(i) * 40, h = 380 + rnd(i + 3) * 220; poly(g, [[x - 90, 1100], [x, 1100 - h], [x + 90, 1100]], '#08080A'); rect(g, x - 10, 1100, 20, 40, '#08080A'); }
      rect(g, 470, 560, 560, 540, '#1E1B1F'); poly(g, [[430, 570], [750, 320], [1070, 570]], '#121013');
      [[520, 640], [820, 640], [520, 860]].forEach(([x, y]) => { rect(g, x, y, 150, 140, P.deep); rect(g, x + 8, y + 8, 134, 124, '#171519'); });
      const lit = 0.55 + 0.45 * Math.sin(t * 3.1) * Math.sin(t * 1.3); rect(g, 820, 860, 150, 140, P.accent, 0.35 + 0.5 * lit); rect(g, 892, 860, 6, 140, P.deep); // janela acesa
      rect(g, 690, 900, 110, 200, '#141214'); circ(g, 780, 1010, 7, P.lite);
      poly(g, [[690, 1100], [800, 1100], [900, 1500], [440, 1500]], '#19171B');
      for (let x = 0; x < W; x += 70) { rect(g, x, 1040, 18, 100, '#0A0A0C'); poly(g, [[x, 1040], [x + 9, 1020], [x + 18, 1040]], '#0A0A0C'); }
      for (let i = 0; i < 3; i++) rect(g, ((t * 14 + i * 400) % 1500) - 300, 1000 + i * 70, 600, 40, P.paper, 0.035); // névoa
    },
    cozinha(g, t) {
      rect(g, 0, 0, W, 1050, '#1D1C1F'); rect(g, 0, 1050, W, H - 1050, P.floor);
      for (let x = 0; x < W; x += 90) rect(g, x, 0, 3, 1050, '#161517'); for (let y = 0; y < 1050; y += 90) rect(g, 0, y, W, 3, '#161517');
      for (let i = 0; i < 6; i++) rect(g, i * 200, 1050, 3, H - 1050, P.deep, 0.7);
      rect(g, 0, 380, 520, 260, '#222025'); rect(g, 258, 380, 4, 260, P.deep); rect(g, 0, 380, 520, 6, P.deep); rect(g, 240, 500, 12, 60, P.lite); rect(g, 268, 500, 12, 60, P.lite);
      rect(g, 0, 820, 520, 230, '#2A272C'); rect(g, 0, 800, 520, 24, '#3A363D'); rect(g, 258, 830, 4, 220, P.deep); rect(g, 120, 760, 90, 40, P.deep);
      rect(g, 740, 330, 300, 720, '#2C2A30'); rect(g, 740, 700, 300, 6, P.deep); rect(g, 760, 440, 14, 120, P.lite); rect(g, 760, 780, 14, 140, P.lite);
      rect(g, 745, 696, 290, 14, P.accent, clamp(0.55 + 0.4 * Math.sin(t * 5) * Math.sin(t * 2.3), 0, 1)); // fresta de luz da geladeira
      g.save(); g.translate(540, 0); g.rotate(Math.sin(t * 1.2) * 0.06); line(g, 0, 0, 0, 260, P.deep, 5);
      poly(g, [[-70, 330], [70, 330], [40, 260], [-40, 260]], P.deep); poly(g, [[-60, 335], [60, 335], [300, 1100], [-300, 1100]], P.paper, 0.045); circ(g, 0, 340, 14, P.paper, 0.8); g.restore();
    },
    porta_luz(g, t) {
      rect(g, 0, 0, W, 1100, '#17151A'); rect(g, 0, 1100, W, H - 1100, P.floor);
      for (let i = 0; i < 8; i++) rect(g, 0, 1130 + i * 100, W, 3, P.deep);
      rect(g, 306, 306, 468, 794, P.deep); rect(g, 330, 330, 420, 770, '#241F22');
      rect(g, 370, 380, 150, 280, '#1A1618'); rect(g, 560, 380, 150, 280, '#1A1618'); rect(g, 370, 710, 150, 300, '#1A1618'); rect(g, 560, 710, 150, 300, '#1A1618');
      circ(g, 700, 780, 24, P.lite); circ(g, 696, 776, 8, P.paper, 0.5);
      const f = 0.7 + 0.3 * Math.sin(t * 7) * Math.sin(t * 3.3);
      poly(g, [[330, 1100], [750, 1100], [1000, 1500], [80, 1500]], P.accent, 0.16 * f); rect(g, 330, 1090, 420, 12, P.accent, 0.95 * f); // luz embaixo da porta
      if (Math.sin(t * 1.7) > 0.2) { rect(g, 470 + Math.sin(t * 1.7) * 14, 1090, 38, 12, P.deep); rect(g, 560 + Math.sin(t * 1.7) * 14, 1090, 38, 12, P.deep); } // sombra de pés do outro lado
    },
    papel(g, t) { // fundo bege de infográfico: gradiente suave de papel, luz e sombra de chão suaves
      const gr = g.createRadialGradient(W / 2, 800, 150, W / 2, 900, 1300); gr.addColorStop(0, '#F2E9D8'); gr.addColorStop(1, '#D8C9AE'); g.fillStyle = gr; g.fillRect(0, 0, W, H);
      const fl = g.createLinearGradient(0, GY - 40, 0, GY + 260); fl.addColorStop(0, 'rgba(120,95,60,0.0)'); fl.addColorStop(0.15, 'rgba(120,95,60,0.18)'); fl.addColorStop(1, 'rgba(120,95,60,0.05)'); g.fillStyle = fl; g.fillRect(0, GY - 40, W, 300);
      rect(g, 0, GY - 2, W, 3, '#B9A885', 0.7);
    },
    // ── Plantão Noturno (ep01+): vetor flat, gradientes suaves, vermelho só no que é do quarto 7 ──
    ponto_onibus(g, t) { // ponto de ônibus à noite, chuva fina, poste com luz
      vgrad(g, 0, 1130, '#0A0C12', '#1C2030');
      for (let i = 0; i < 9; i++) { const x = i * 128 - 30, h = 110 + rnd(i + 11) * 210; rect(g, x, 1130 - h, 118, h, '#11131A');
        for (let j = 0; j < 6; j++) if (rnd(i * 7 + j) > 0.72) rect(g, x + 14 + (j % 3) * 34, 1130 - h + 24 + Math.floor(j / 3) * 46, 18, 24, LUZ, 0.14); }
      vgrad(g, 1130, 1300, '#1C1B20', '#141317'); rect(g, 0, 1296, W, 16, '#26242B'); vgrad(g, 1312, H, '#0F0F13', '#0A0A0C');
      const on = rnd(Math.floor(t * 8)) > 0.1 ? 1 : 0.55;
      poly(g, [[600, 330], [690, 330], [960, 1300], [330, 1300]], LUZ, 0.05 * on); glow(g, 645, 1250, 420, LUZ, 0.10 * on); glow(g, 645, 340, 300, LUZ, 0.22 * on);
      rect(g, 748, 300, 26, 1000, '#24232A'); rect(g, 640, 296, 134, 12, '#24232A'); poly(g, [[598, 308], [692, 308], [680, 336], [610, 336]], '#2E2D35'); rect(g, 612, 334, 66, 6, LUZ, on);
      g.fillStyle = 'rgba(0,0,0,0.4)'; g.beginPath(); g.ellipse(762, 1302, 70, 10, 0, 0, Math.PI * 2); g.fill();
      rect(g, 800, 1150, 150, 12, '#2A2930'); rect(g, 808, 1162, 10, 90, '#2A2930'); rect(g, 930, 1162, 10, 90, '#2A2930'); // banco do ponto
      glow(g, 645, 1560, 260, LUZ, 0.07 * on); // reflexo no asfalto molhado
      chuva(g, t, 130, 0.2); vinheta(g, 0.55);
    },
    estrada(g, t) { // estrada escura à noite: ônibus grande de lado ocupando o quadro, Bia sozinha na janela acesa; asfalto e acostamento preenchem o terço de baixo
      vgrad(g, 0, 980, '#0B0E16', '#222738'); glow(g, 860, 230, 420, '#9AA3B5', 0.1); circ(g, 860, 230, 54, P.moon, 0.85); circ(g, 884, 214, 50, '#141826'); // lua entre nuvens
      for (let i = 0; i < 3; i++) rect(g, ((i * 520 - t * 18) % 1600 + 1600) % 1600 - 400, 300 + i * 120, 520, 40, '#9AA3B5', 0.05);
      poly(g, [[0, 980], [0, 820], [260, 760], [520, 840], [800, 740], [1080, 820], [1080, 980]], '#121521');
      for (let i = 0; i < 11; i++) { const x = ((i * 160 - t * 90) % 1760 + 1760) % 1760 - 200, h = 190 + rnd(i + 3) * 170; poly(g, [[x - 74, 985], [x, 985 - h], [x + 74, 985]], '#0B0D13'); }
      vgrad(g, 980, 1400, '#1C1D24', '#141519'); rect(g, 0, 980, W, 6, '#2C2C35'); for (let x = -((t * 900) % 240); x < W; x += 240) rect(g, x, 1352, 130, 12, LUZ, 0.34); // faixa da estrada
      glow(g, 560, 1330, 520, LUZ, 0.07); // luz do ônibus no asfalto molhado
      vgrad(g, 1400, H, '#101114', '#0A0A0C'); rect(g, 0, 1400, W, 8, '#24242B');
      const bob = Math.sin(t * 9) * 2.5, BX = 330 + t * 8, BY = 1290 + bob, E = 1.85;
      onibus(g, BX, BY, E, { bia: 4, luz: 0.1, biaLuz: 0.75, bancos: true, faixa: true });
      for (let i = 0; i < 5; i++) { const x = ((i * 330 - t * 1400) % 1650 + 1650) % 1650 - 250; rect(g, x, 1420, 30, 330, '#050506'); rect(g, x - 60, 1470, 330, 16, '#050506'); rect(g, x - 60, 1560, 330, 12, '#050506'); } // cerca do acostamento passando rápido (primeiro plano)
      for (let i = 0; i < 26; i++) { const x = ((rnd(i) * 1300 - t * 1600) % 1300 + 1300) % 1300 - 110, hh = 50 + rnd(i + 2) * 90; poly(g, [[x - 14, 1760], [x + 14, 1760], [x + 4, 1760 - hh]], '#0B0D0B'); } // mato
      rect(g, 0, 1760, W, H - 1760, '#070708');
      chuva(g, t, 100, 0.17); vinheta(g, 0.5);
    },
    pousada_fora(g, t) { // fachada da Pousada Vale Verde, 22h, letreiro com uma letra apagada
      vgrad(g, 0, 1240, '#080A10', '#181B26');
      for (let i = 0; i < 5; i++) { const lx = i < 2 ? 30 + i * 70 : 900 + (i - 2) * 70, h = 520 + rnd(i) * 200; poly(g, [[lx - 110, 1250], [lx, 1250 - h], [lx + 110, 1250]], '#0B0C11'); }
      glow(g, 540, 430, 520, '#9AA3B5', 0.08); vgrad(g, 560, 1250, '#2E2A33', '#1E1B22', 120, 840); poly(g, [[80, 580], [540, 430], [1000, 580]], '#141217'); line(g, 80, 578, 540, 430, '#3A3540', 4); line(g, 540, 430, 1000, 578, '#3A3540', 4); rect(g, 80, 572, 920, 14, '#0F0D11');
      const win = (x, y, a, c = LUZ) => { rect(g, x, y, 130, 150, '#0F0E12'); rect(g, x + 8, y + 8, 114, 134, '#18171C'); if (a) { rect(g, x + 8, y + 8, 114, 134, c, a); glow(g, x + 65, y + 75, 170, c, a * 0.35); } rect(g, x + 62, y + 8, 6, 134, '#0F0E12'); };
      win(170, 720, 0); win(370, 720, 0.18); win(580, 720, 0); win(780, 720, 0.25 + 0.15 * Math.sin(t * 2.3), P.accent); // a janela do 7, vermelha e fraca
      rect(g, 250, 600, 580, 84, '#121014'); rect(g, 250, 600, 580, 4, '#3A3540'); glow(g, 540, 642, 340, LUZ, 0.09);
      g.font = '900 46px Geist'; g.letterSpacing = '0px'; g.textBaseline = 'middle'; const S = 'POUSADA VALE VERDE', apag = S.lastIndexOf('R'), tw = g.measureText(S).width + (S.length - 1) * 3; let lx = 540 - tw / 2;
      for (let i = 0; i < S.length; i++) { g.globalAlpha = i === apag ? (rnd(Math.floor(t * 9)) > 0.8 ? 0.5 : 0.12) : 1; g.fillStyle = LUZ; g.fillText(S[i], lx, 644); lx += g.measureText(S[i]).width + 3; } g.globalAlpha = 1; g.textBaseline = 'alphabetic';
      rect(g, 420, 990, 240, 260, '#100E12'); vgrad(g, 1000, 1250, rgba(LUZ, 0.75), rgba(LUZ, 0.4), 432, 216); poly(g, [[390, 990], [690, 990], [660, 960], [420, 960]], '#0F0D11');
      vgrad(g, 1250, H, '#141217', '#0B0B0D'); poly(g, [[432, 1250], [648, 1250], [820, 1700], [260, 1700]], LUZ, 0.06); rect(g, 380, 1250, 320, 18, '#26232A');
      glow(g, 540, 1120, 380, LUZ, 0.12); chuva(g, t, 120, 0.18); vinheta(g, 0.6);
    },
    saguao(g, t, c = {}) { // recepção: relógio de pêndulo, painel das 7 campainhas, balcão e escada
      vgrad(g, 0, 1090, '#2A2421', '#1B1819'); for (let x = 0; x < W; x += 54) rect(g, x, 0, 18, 820, '#FFFFFF', 0.018);
      rect(g, 0, 820, W, 270, '#181516'); rect(g, 0, 812, W, 12, '#2E2725'); for (let x = 40; x < W; x += 180) rect(g, x, 860, 120, 190, '#1E1A1A');
      vgrad(g, 1090, H, '#16131A', '#0C0B0D'); for (let i = 0; i < 9; i++) { const y = 1090 + Math.pow(i / 9, 1.6) * 830; rect(g, 0, y, W, 3, '#0A090B', 0.8); }
      line(g, 610, 0, 610, 230, '#0E0D10', 4); poly(g, [[560, 226], [660, 226], [690, 280], [530, 280]], '#141216'); rect(g, 560, 278, 100, 6, LUZ, 0.9);
      glow(g, 610, 330, 700, LUZ, 0.13); glow(g, 640, 1250, 520, LUZ, 0.07);
      const hora = (c.hora || '22:10').split(':').map(Number), seg = hora[0] * 3600 + hora[1] * 60 + (c.parado ? 0 : t); // c.parado: relógio e pêndulo parados
      const RX = 440; rect(g, RX - 68, 700, 136, 290, '#2A211B'); rect(g, RX - 54, 740, 108, 230, '#15110F'); const pa = c.parado ? 0 : Math.sin(t * Math.PI) * 0.3;
      if (!c.caixaAberta) { line(g, RX, 740, RX + Math.sin(pa) * 170, 740 + Math.cos(pa) * 170, '#8C7A5E', 5); circ(g, RX + Math.sin(pa) * 180, 740 + Math.cos(pa) * 180, 22, '#C9B38A'); }
      else poly(g, [[RX + 68, 700], [RX + 150, 680], [RX + 150, 1010], [RX + 68, 990]], '#3A2E26'); // caixa do relógio aberta e vazia (cadê a chave?)
      relogioFace(g, RX, 600, 110, seg);
      painelDesenho(g, 800, 610, 380, c.sete ? (Math.sin(t * 9) > 0 ? 1 : 0.25) : 0);
      rect(g, 560, 1000, 520, 240, '#251E1B'); rect(g, 546, 984, 534, 22, '#3B302A'); for (let x = 590; x < W; x += 170) rect(g, x, 1040, 130, 160, '#1D1816');
      circ(g, 980, 984, 26, '#C9B38A'); rect(g, 950, 980, 60, 6, '#8C7A5E'); circ(g, 980, 956, 6, '#C9B38A'); // sineta do balcão
      for (let i = 0; i < 8; i++) rect(g, 0, 1240 - (i + 1) * 62, 330 - i * 36, 62, i % 2 ? '#211C1C' : '#1C1818'); // escada
      line(g, 340, 1000, 50, 520, '#3B302A', 12); for (let i = 0; i < 6; i++) { const k = i / 5; line(g, lerp(330, 60, k), lerp(1000, 540, k), lerp(330, 60, k), lerp(1240, 1000 - 6 * 62 * k, k), '#2E2622', 6); }
      if (c.luzEscada && t >= (c.luzEm || 0)) { const a = clamp((t - (c.luzEm || 0)) / 0.5) * (rnd(Math.floor(t * 14)) > 0.08 ? 1 : 0.6); // a luz vermelha acende no alto da escada (quarto 7)
        rect(g, 70, 430, 60, 40, '#2A211B'); circ(g, 100, 482, 18, P.accent, a); glow(g, 100, 482, 420, P.accent, 0.5 * a); poly(g, [[60, 490], [140, 490], [420, 1240], [0, 1240]], P.accent, 0.07 * a); }
      if (c.sofa === 'vulto') sofaCostas(g, 250, 1330, 0.42, t >= (c.sofaEm || 0), t); else if (c.sofa) sofaFrente(g, 230, 1240, 0.45);
      if (c.emergencia) { const d = t < 0.7 ? 0 : t < 1.4 ? 0.3 : t < 2.1 ? 0.55 : 0.74; // as luzes apagam uma a uma; só a de emergência (âmbar) fica
        rect(g, 0, 0, W, H, '#050406', d); if (t > 2.1) { rect(g, 880, 150, 120, 44, '#3A3530'); rect(g, 892, 194, 96, 16, AMBAR); glow(g, 940, 210, 900, AMBAR, 0.22); }
        const sx = 120 + t * 70; g.fillStyle = 'rgba(3,2,3,0.85)'; g.beginPath(); g.moveTo(0, 1240); g.lineTo(sx, 1240); for (let i = 0; i <= 6; i++) g.lineTo(sx + (i % 2 ? 60 : 0) - i * 6, 1240 + i * 110); g.lineTo(0, H); g.fill(); } // a sombra avança pelo chão
      if (c.pisca && t < c.pisca) rect(g, 0, 0, W, H, '#050406', rnd(Math.floor(t * 11) + 3) > 0.62 ? 0.62 : 0); // ep03: luzes falhando (c.pisca = segundos)
      vinheta(g, 0.55);
    },
    parede(g, t) { // parede do saguão de perto (para o relógio e o painel grandes)
      vgrad(g, 0, H, '#2A2421', '#15121A'); for (let x = 0; x < W; x += 72) rect(g, x, 0, 24, H, '#FFFFFF', 0.02);
      glow(g, 300, 200, 900, LUZ, 0.12); vinheta(g, 0.65);
    },
    mesa(g, t) { // tampo do balcão de perto, com a luz da lâmpada (fundo do caderno)
      vgrad(g, 0, H, '#2A211C', '#120E0C'); for (let i = 0; i < 26; i++) { const y = i * 76 + rnd(i) * 30; g.globalAlpha = 0.09; g.strokeStyle = '#000'; g.lineWidth = 4; g.beginPath(); g.moveTo(0, y); g.bezierCurveTo(300, y + 20, 700, y - 24, W, y + 8); g.stroke(); }
      g.globalAlpha = 1; glow(g, 560, 620, 1000, LUZ, 0.16); vinheta(g, 0.7);
    },
    varanda(g, t, c = {}) { // porta da frente/varanda na chuva, o ônibus esperando na estrada (c.semOnibus tira o ônibus)
      vgrad(g, 0, 1060, '#080A10', '#171A25'); poly(g, [[0, 1060], [0, 900], [300, 860], [640, 920], [1080, 850], [1080, 1060]], '#0D0F15');
      rect(g, 0, 1040, W, 40, '#17171C'); if (!c.semOnibus) { const ob = c.onibus || {}; onibus(g, ob.x ?? 520, ob.y ?? 1058, ob.escala ?? 0.62, { porta: true, luz: 0.22 }); // c.onibus = {x, y, escala}
        if (ob.portaLuz) { const s = ob.escala ?? 0.62, px = (ob.x ?? 520) + 297 * s, py = (ob.y ?? 1058) - 140 * s; glow(g, px, py, 260 * s, LUZ, 0.35); poly(g, [[px - 35 * s, (ob.y ?? 1058) - 30 * s], [px + 35 * s, (ob.y ?? 1058) - 30 * s], [px + 140 * s, (ob.y ?? 1058) + 60], [px - 140 * s, (ob.y ?? 1058) + 60]], LUZ, 0.12); } } // luz da porta aberta no chão
      chuva(g, t, 120, 0.22, 300, 1240);
      vgrad(g, 0, 300, '#0E0C0E', '#141114'); rect(g, 0, 290, W, 34, '#1E191B'); for (let x = 20; x < W; x += 60) { const k = (t * 0.9 + rnd(x)) % 1; circ(g, x, 330 + k * 120, 5, '#A9B2C3', 0.4 * (1 - k)); } // beiral com gotas
      rect(g, 30, 320, 70, 940, '#1D191B'); rect(g, 980, 320, 70, 940, '#1D191B');
      for (const [a, b] of [[100, 380], [790, 980]]) { rect(g, a, 1040, b - a, 16, '#2A2326'); for (let x = a + 30; x < b; x += 52) rect(g, x, 1056, 12, 184, '#221D1F'); }
      vgrad(g, 1240, H, '#1E1916', '#0F0C0B'); for (let i = 0; i < 8; i++) rect(g, 0, 1270 + i * 80, W, 3, '#0B0909');
      line(g, 300, 324, 300, 420, '#0E0C0E', 3); poly(g, [[270, 416], [330, 416], [346, 452], [254, 452]], '#1A1719'); glow(g, 300, 470, 620, LUZ, 0.2); glow(g, 300, 1260, 360, LUZ, 0.08);
      vinheta(g, 0.5);
    },
    preto(g, t) { rect(g, 0, 0, W, H, '#070708'); glow(g, W / 2, H * 0.55, 700, P.accent, 0.05 + 0.03 * Math.sin(t * 4)); }, // corte seco
    // ── Plantão Noturno (ep02-07) ──
    escada(g, t, c = {}) { // escada de madeira do saguão ao 2º andar (sobe da direita para a esquerda); c.luzVermelha (lâmpada do alto), c.degrausVermelhos (cada degrau acende), c.ritmo
      const SW = 100, SH = 66, N = 8, Y0 = 1560, YL = Y0 - N * SH, XL = W - N * SW; // degrau k: x em [W-(k+1)SW, W-kSW], topo em Y0-kSH; patamar à esquerda de XL
      vgrad(g, 0, H, '#241E1F', '#110F11'); for (let x = 0; x < W; x += 60) rect(g, x, 0, 20, H, '#FFFFFF', 0.015);
      rect(g, 0, 300, XL - 20, YL - 300, '#0B0A0C'); vgrad(g, 300, YL, '#060507', '#151215', 0, XL - 20); rect(g, XL - 30, 290, 20, YL - 290, '#2E2622'); rect(g, 0, 286, XL - 10, 18, '#2E2622'); // vão escuro do corredor do 2º andar
      const lv = c.luzVermelha ? clamp(t / 0.4) * (rnd(Math.floor(t * 14)) > 0.08 ? 1 : 0.55) : 0, cor = lv ? P.accent : LUZ;
      rect(g, 120, 200, 70, 40, '#2A211B'); circ(g, 155, 252, 16, cor, lv ? lv : 0.8); glow(g, 155, 252, lv ? 560 : 380, cor, lv ? 0.5 * lv : 0.16);
      const pts = [[W, H], [W, Y0]]; for (let k = 0; k < N; k++) { const x1 = W - (k + 1) * SW, y = Y0 - k * SH; pts.push([x1 + SW, y], [x1, y], [x1, y - SH]); } pts.push([0, YL], [0, H]);
      poly(g, pts, '#1E1718'); vgrad(g, YL, H, 'rgba(0,0,0,0)', 'rgba(0,0,0,0.5)');
      const nAcesos = c.degrausVermelhos ? Math.floor(t * (c.ritmo || 1.6)) + 1 : 0;
      for (let k = 0; k < N; k++) { const x1 = W - (k + 1) * SW, y = Y0 - k * SH; rect(g, x1 - 6, y - 4, SW + 6, 14, '#3A2D27'); rect(g, x1 - 6, y + 10, 6, SH - 10, '#140F10');
        if (k < nAcesos) { rect(g, x1 + 8, y + 18, SW - 16, 8, P.accent); glow(g, x1 + SW / 2, y + 20, 170, P.accent, 0.35); } }
      rect(g, 0, YL - 4, XL, 14, '#3A2D27');
      line(g, W + 20, Y0 - 300, XL, YL - 300, '#4A3B30', 14); for (let k = 0; k <= N; k++) { const x = W - k * SW - SW / 2, y = Y0 - k * SH; line(g, x, y, x, y - 300 + (SH / SW) * (SW / 2) * 0, '#2E2622', 7); } // corrimão
      if (lv) poly(g, [[110, 270], [200, 270], [W, Y0], [W, H], [0, H]], P.accent, 0.05 * lv);
      vinheta(g, 0.55);
    },
    corredor_andar(g, t, c = {}) { // corredor do 2º andar: portas 1-6 nas laterais, porta 7 no fundo com luz vermelha por baixo; c.porta7 = 'fechada' | 'abrindo' (c.abre s) | 'aberta'
      const L = 360, R = 720, T = 520, B = 1000;
      rect(g, 0, 0, W, H, P.deep); poly(g, [[0, 0], [W, 0], [R, T], [L, T]], '#0F0E10'); poly(g, [[0, H], [W, H], [R, B], [L, B]], '#1A1517');
      poly(g, [[230, H], [850, H], [600, B], [480, B]], '#2A1F1E'); for (let i = 0; i < 7; i++) { const y = B + Math.pow(i / 7, 1.7) * (H - B); line(g, lerp(480, 230, (y - B) / (H - B)), y, lerp(600, 850, (y - B) / (H - B)), y, '#1E1615', 3); }
      poly(g, [[0, 0], [L, T], [L, B], [0, H]], '#221D20'); poly(g, [[W, 0], [R, T], [R, B], [W, H]], '#1D191C');
      const wallL = x => [T * x / L, H - (H - B) * x / L], wallR = x => [T * (W - x) / (W - R), H - (H - B) * (W - x) / (W - R)];
      const porta = (wall, x1, x2, n) => { const [t1, b1] = wall(x1), [t2, b2] = wall(x2), h1 = b1 - t1, h2 = b2 - t2, sg = x2 > x1 ? 1 : -1;
        poly(g, [[x1, t1 + h1 * 0.22], [x2, t2 + h2 * 0.22], [x2, b2], [x1, b1]], '#120F11'); poly(g, [[x1 + 6 * sg, t1 + h1 * 0.25], [x2 - 3 * sg, t2 + h2 * 0.25], [x2 - 3 * sg, b2 - 3], [x1 + 6 * sg, b1 - 5]], '#2C2326');
        const xm = (x1 + x2) / 2, hm = (h1 + h2) / 2, ym = (t1 + t2) / 2 + hm * 0.36, sz = Math.max(16, Math.abs(x2 - x1) * 0.32);
        rect(g, xm - sz * 0.55, ym - sz * 0.9, sz * 1.1, sz * 1.15, '#8C7A5E'); text(g, String(n), xm, ym + sz * 0.05, sz, '#1A1416', { align: 'center' }); };
      porta(wallL, 20, 150, 1); porta(wallL, 200, 272, 3); porta(wallL, 300, 342, 5); porta(wallR, 1060, 930, 2); porta(wallR, 880, 808, 4); porta(wallR, 780, 738, 6);
      rect(g, L, T, R - L, B - T, '#141113');
      const k = c.porta7 === 'aberta' ? 1 : c.porta7 === 'abrindo' ? out(clamp(t / (c.abre || 4))) : 0, DX = 490, DW = 100, DT = 770, DB = 1000;
      rect(g, DX - 10, DT - 12, DW + 20, DB - DT + 12, '#0B090A');
      if (k > 0) { rect(g, DX, DT, DW, DB - DT, '#1A0605'); rect(g, DX, DT, DW, DB - DT, P.accent, 0.28 * k); glow(g, DX + DW / 2, DT + 120, 260, P.accent, 0.45 * k); }
      poly(g, [[DX, DT], [DX + DW * (1 - k * 0.82), DT - 12 * k], [DX + DW * (1 - k * 0.82), DB + 10 * k], [DX, DB]], '#2E2427'); // folha da porta girando na dobradiça
      if (k < 0.3) { rect(g, DX + 30, DT + 26, 40, 34, '#3B302A'); text(g, '7', DX + 50, DT + 54, 30, P.accent, { align: 'center' }); }
      const fl = 0.75 + 0.25 * Math.sin(t * 6) * Math.sin(t * 2.3); rect(g, DX, DB - 6, DW, 8, P.accent, 0.95 * fl); glow(g, DX + DW / 2, DB, 300, P.accent, 0.3 * fl); poly(g, [[DX, DB], [DX + DW, DB], [DX + DW + 260, H], [DX - 260, H]], P.accent, (0.05 + 0.12 * k) * fl);
      const on = rnd(Math.floor(t * 10)) > 0.2 ? 1 : 0.35; rect(g, 500, 560, 80, 12, P.paper, 0.85 * on); poly(g, [[500, 572], [580, 572], [760, 1500], [320, 1500]], P.paper, 0.04 * on);
      vinheta(g, 0.6);
    },
    porta7(g, t, c = {}) { // a porta do 7 de perto: placa, maçaneta, chave de corda pendurada num barbante (c.chave), fresta escura (c.fresta px)
      vgrad(g, 0, H, '#1C1719', '#0E0C0D'); const fr = c.fresta ?? 0;
      rect(g, 130, 0, 60, H, '#2B2224'); rect(g, 890, 0, 70, H, '#2B2224');
      if (fr > 0) { rect(g, 890 - fr, 0, fr, H, '#050405'); glow(g, 890 - fr / 2, 1250, 340, P.accent, 0.22); rect(g, 888 - fr / 2, 200, 4, H - 200, P.accent, 0.3); }
      if (fr > 0 && c.dentro) { g.save(); g.beginPath(); g.rect(890 - fr, 0, fr, H); g.clip(); rect(g, 890 - fr, 1180, fr, H, '#2A1F22'); rect(g, 890 - fr, 1150, fr, 40, '#4F4046'); rect(g, 890 - fr, 1190, fr * 0.5, 120, '#5E4E55'); // ep03: pela fresta, a cama arrumada, a mesinha e o caderno
        rect(g, 890 - fr * 0.55, 1060, fr * 0.55, 320, '#3E2F33'); rect(g, 890 - fr * 0.5, 1030, fr * 0.42, 30, '#3A2F2B'); rect(g, 890 - fr * 0.5, 1030, 14, 30, P.accent); glow(g, 890 - fr * 0.3, 1000, 300, P.accent, 0.2); g.restore(); }
      rect(g, 190, 0, 700 - fr, H, '#2E2427'); rect(g, 250, 140, 580 - fr, 620, '#271F22'); rect(g, 250, 880, 580 - fr, 860, '#271F22');
      for (let i = 0; i < 14; i++) { const x = 210 + rnd(i + 3) * (660 - fr); line(g, x, 0, x + rnd(i) * 20, H, '#000', 2, 0.12); }
      rect(g, 440, 300, 200, 160, '#3B302A'); rect(g, 452, 312, 176, 136, '#1A1416'); text(g, '7', 540, 432, 120, P.accent, { align: 'center' }); glow(g, 540, 380, 220, P.accent, 0.12);
      const mx = 770 - fr, my = 1020; rect(g, mx - 34, my - 110, 68, 240, '#4A3B30'); circ(g, mx, my, 46, '#C9B38A'); circ(g, mx - 12, my - 12, 16, '#EFE3C4', 0.6); circ(g, mx, my + 80, 10, '#0B090A');
      if (c.chave !== false && !(c.pega != null && t > c.pega)) { const a = Math.sin(t * 1.4) * 0.14 + 0.05, L2 = 250, ex = mx + Math.sin(a) * L2, ey = my + 36 + Math.cos(a) * L2;
        line(g, mx, my + 36, ex, ey, '#BDB3A0', 3); chaveCorda(g, ex, ey + 22, 1.25, -a); }
      vinheta(g, 0.6);
    },
    quarto7(g, t, c = {}) { // quarto 7 por dentro: janela tabuada, espelho, cama arrumada, mesinha com c.cadernos empilhados e a página (c.pagina)
      vgrad(g, 0, 1100, '#231A1D', '#17121A'); for (let x = 0; x < W; x += 64) rect(g, x, 0, 6, 1100, '#000', 0.14);
      vgrad(g, 1100, H, '#1A1314', '#0C0A0B'); for (let i = 0; i < 9; i++) rect(g, 0, 1130 + i * 95, W, 3, '#080607', 0.8); rect(g, 0, 1090, W, 18, '#120E10');
      rect(g, 380, 230, 340, 430, '#120E10'); rect(g, 396, 246, 308, 398, '#0B0A10'); for (let i = 0; i < 4; i++) rect(g, 396, 296 + i * 100, 308, 5, '#9AA3B5', 0.12);
      for (const [y, a] of [[290, -0.06], [390, 0.05], [490, -0.03], [590, 0.07]]) { g.save(); g.translate(550, y); g.rotate(a); rect(g, -195, -28, 390, 54, '#3A2D27'); rect(g, -195, -28, 390, 6, '#4A3A31'); circ(g, -165, 0, 6, '#8C7A5E'); circ(g, 165, 0, 6, '#8C7A5E'); g.restore(); }
      rect(g, 60, 300, 230, 640, '#3B302A'); vgrad(g, 316, 924, '#2C2A33', '#141419', 76, 198); line(g, 100, 360, 240, 600, '#FFFFFF', 14, 0.05); glow(g, 175, 700, 160, P.accent, 0.08);
      rect(g, 680, 800, 380, 300, '#2E2226'); rect(g, 680, 800, 380, 16, '#3E3033'); rect(g, 640, 1010, 440, 230, '#3E2F33'); rect(g, 640, 1050, 440, 140, '#4F4046'); rect(g, 640, 1050, 440, 10, '#5E4E55'); rrect(g, 700, 952, 190, 70, 22, '#CFC6B8'); rect(g, 650, 1240, 16, 40, '#120E10'); rect(g, 1050, 1240, 16, 40, '#120E10');
      rect(g, 290, 1030, 320, 26, '#3B2E28'); rect(g, 310, 1056, 16, 200, '#2A201C'); rect(g, 574, 1056, 16, 200, '#2A201C');
      rect(g, 540, 940, 10, 90, '#2A201C'); poly(g, [[505, 900], [585, 900], [600, 950], [490, 950]], '#5A2A24'); glow(g, 545, 960, 520, P.accent, 0.14 + 0.03 * Math.sin(t * 3)); // abajur de cúpula vermelha
      const n = c.cadernos ?? 1; for (let i = 0; i < n; i++) { const x = 330 + (rnd(i + 5) - 0.5) * 18, y = 1030 - (i + 1) * 22; rect(g, x, y, 170, 21, '#3A2F2B'); rect(g, x, y, 14, 21, P.accent, 0.9); rect(g, x + 14, y + 17, 156, 4, '#E9E3D3', 0.7); }
      if (c.pagina) { g.save(); g.translate(420, 1030 - n * 22 - 6); g.rotate(-0.1); poly(g, [[-70, -8], [80, -14], [86, 6], [-64, 10], [-72, 2]], '#E9E3D3'); line(g, -50, -2, 60, -6, '#1A1819', 2, 0.6); g.restore(); }
      vinheta(g, 0.62);
    },
    espelho(g, t, c = {}) { // o espelho do quarto 7 de perto: o reflexo da Bia (c.reflexo = {pose, x, escala, y}) segura a página e não pisca
      vgrad(g, 0, H, '#231A1D', '#120E10'); for (let x = 0; x < W; x += 64) rect(g, x, 0, 6, H, '#000', 0.14);
      const x0 = 170, y0 = 200, w = 740, h = 1180; rect(g, x0 - 44, y0 - 44, w + 88, h + 88, '#3B302A'); rect(g, x0 - 22, y0 - 22, w + 44, h + 44, '#2A211B');
      g.save(); g.beginPath(); g.rect(x0, y0, w, h); g.clip(); vgrad(g, y0, y0 + h, '#2A262C', '#121014', x0, w);
      rect(g, 380, 330, 300, 360, '#120E10'); for (let i = 0; i < 4; i++) rect(g, 370, 360 + i * 84, 320, 44, '#2E241F'); glow(g, 760, 1000, 500, P.accent, 0.12);
      const r = c.reflexo || {}; personagem(g, { id: 'bia', pose: r.pose || 'lendo', x: r.x ?? 0.5, escala: r.escala || 1.7, y: r.y ?? 300, flip: r.flip ?? true, semEntrada: true, fica: true }, t, 99, c._elenco);
      rect(g, x0, y0, w, h, '#9AA3B5', 0.07); poly(g, [[x0 + 60, y0], [x0 + 200, y0], [x0 + 520, y0 + h], [x0 + 380, y0 + h]], '#FFFFFF', 0.035); g.restore();
      vinheta(g, 0.5);
    },
    porta_frente(g, t, c = {}) { // porta da frente por dentro: olho mágico, trinco, janelinha com chuva (c.semChuva), c.batida = 3 batidas (a porta treme)
      vgrad(g, 0, 1240, '#262022', '#1A1618'); for (let x = 0; x < W; x += 54) rect(g, x, 0, 18, 1240, '#FFFFFF', 0.015); rect(g, 0, 820, W, 420, '#1D1819'); rect(g, 0, 812, W, 10, '#2E2725');
      vgrad(g, 1240, H, '#17131A', '#0B0A0C'); for (let i = 0; i < 8; i++) rect(g, 0, 1270 + i * 85, W, 3, '#0A090B', 0.8);
      const jx = 850, jy = 380, jw = 190, jh = 480; rect(g, jx - 16, jy - 16, jw + 32, jh + 32, '#2E2522'); g.save(); g.beginPath(); g.rect(jx, jy, jw, jh); g.clip(); vgrad(g, jy, jy + jh, '#0A0C14', '#151925', jx, jw); if (!c.semChuva) chuva(g, t, 70, 0.4, jy, jy + jh); g.restore(); rect(g, jx + jw / 2 - 4, jy, 8, jh, '#2E2522'); rect(g, jx, jy + jh / 2 - 4, jw, 8, '#2E2522');
      const bat = c.batida ? (Array.isArray(c.batida) ? c.batida : [0.5, 1.15, 1.8]).reduce((a, b) => a + (t > b ? Math.sin((t - b) * 60) * Math.exp(-(t - b) * 9) * 8 : 0), 0) : 0;
      g.save(); g.translate(bat, 0); rect(g, 270, 250, 540, 1000, '#3A2D27'); rect(g, 290, 270, 500, 976, '#2E2420'); rect(g, 330, 330, 420, 330, '#271E1B'); rect(g, 330, 720, 420, 470, '#271E1B');
      circ(g, 540, 560, 24, '#C9B38A'); circ(g, 540, 560, 12, '#0B0A0C'); circ(g, 535, 555, 4, '#9AA3B5', 0.6); // olho mágico
      rect(g, 630, 856, 130, 54, '#8C7A5E'); rect(g, 600, 866, 110, 34, '#C9B38A'); circ(g, 646, 858, 13, '#C9B38A'); rect(g, 600, 866, 110, 6, '#EFE3C4', 0.5); // trinco fechado
      rect(g, 702, 950, 40, 100, '#8C7A5E'); circ(g, 722, 990, 28, '#C9B38A'); circ(g, 714, 982, 9, '#EFE3C4', 0.6); g.restore();
      rect(g, 290, 1238, 500, 6, '#9AA3B5', 0.22); rect(g, 140, 470, 40, 70, '#2A211B'); glow(g, 160, 470, 420, LUZ, 0.16); glow(g, 540, 700, 700, LUZ, 0.06);
      vinheta(g, 0.55);
    },
    olho_magico(g, t, c = {}) { // vista pelo olho mágico (lente fish-eye): a varanda na chuva, com a Dalva (c.dalva) ou vazia
      const S = 0.5, ow = W * S, oh = H * S, R = 440, D = 2 * R, z = CENARIOS.olho_magico;
      if (!z.oc) { z.oc = Object.assign(document.createElement('canvas'), { width: ow, height: oh }); z.out = Object.assign(document.createElement('canvas'), { width: D, height: D }); z.og = z.oc.getContext('2d', { willReadFrequently: true });
        const map = new Int32Array(D * D).fill(-1), cx0 = ow / 2, cy0 = oh * 0.4, Rs = ow * 0.62;
        for (let y = 0; y < D; y++) for (let x = 0; x < D; x++) { const dx = (x - R) / R, dy = (y - R) / R, r = Math.hypot(dx, dy); if (r > 1) continue; const rs = (0.5 * r + 0.5 * r * r * r) * Rs, a = Math.atan2(dy, dx), sx = Math.round(cx0 + Math.cos(a) * rs), sy = Math.round(cy0 + Math.sin(a) * rs); if (sx >= 0 && sx < ow && sy >= 0 && sy < oh) map[y * D + x] = (sy * ow + sx) * 4; }
        z.map = map; }
      const og = z.og; og.setTransform(S, 0, 0, S, 0, 0); CENARIOS.varanda(og, t, { semOnibus: true });
      if (c.dalva) personagem(og, { id: 'dalva', pose: c.pose || 'sorrindo', x: 0.5, escala: c.escalaD ?? 1.15, y: c.yD ?? 40, semEntrada: true, fica: true, semSombra: true }, t, 99, c._elenco);
      chuva(og, t + 3, 60, 0.25);
      const src = og.getImageData(0, 0, ow, oh).data, o2 = z.out.getContext('2d'), img = o2.createImageData(D, D), d = img.data, map = z.map;
      for (let i = 0; i < map.length; i++) { const m = map[i]; if (m < 0) continue; const j = i * 4; d[j] = src[m]; d[j + 1] = src[m + 1]; d[j + 2] = src[m + 2]; d[j + 3] = 255; }
      o2.putImageData(img, 0, 0);
      rect(g, 0, 0, W, H, '#070607'); for (let i = 0; i < 12; i++) line(g, 0, rnd(i) * H, W, rnd(i) * H + 30, '#1A1416', 3, 0.5);
      const X = W / 2, Y = 860; g.drawImage(z.out, X - R, Y - R);
      const gr = g.createRadialGradient(X, Y, R * 0.5, X, Y, R); gr.addColorStop(0, 'rgba(0,0,0,0)'); gr.addColorStop(1, 'rgba(0,0,0,0.9)'); g.fillStyle = gr; g.beginPath(); g.arc(X, Y, R, 0, Math.PI * 2); g.fill();
      g.strokeStyle = '#241D1A'; g.lineWidth = 60; g.beginPath(); g.arc(X, Y, R + 26, 0, Math.PI * 2); g.stroke(); g.strokeStyle = 'rgba(255,255,255,0.07)'; g.lineWidth = 10; g.beginPath(); g.arc(X, Y, R - 40, Math.PI * 1.1, Math.PI * 1.45); g.stroke();
    },
    gaveta(g, t, c = {}) { // gaveta do balcão vista de cima: celular antigo aceso, 'DONA DALVA' chamando, ao lado do caderno
      vgrad(g, 0, H, '#2A211C', '#120E0C'); rect(g, 90, 420, 900, 1160, '#3B2E26'); rect(g, 120, 450, 840, 1100, '#15100E'); vgrad(g, 450, 640, 'rgba(0,0,0,0.6)', 'rgba(0,0,0,0)', 120, 840);
      line(g, 190, 1420, 420, 1350, '#8C7A5E', 14); line(g, 600, 1460, 760, 1480, '#6F6B72', 8); g.strokeStyle = '#9C9A98'; g.lineWidth = 4; g.beginPath(); g.ellipse(880, 1420, 20, 34, 0.4, 0, Math.PI * 2); g.stroke();
      g.save(); g.translate(330, 900); g.rotate(-0.08); rect(g, -150, -206, 300, 420, '#000', 0.35); rect(g, -160, -220, 300, 420, '#3A2F2B'); rect(g, -160, -220, 26, 420, P.accent); rect(g, -100, -120, 180, 40, '#EDE4D3', 0.85); g.restore();
      const toca = c.tocando !== false, on = toca && Math.sin(t * 7) > -0.3, vib = on ? Math.sin(t * 70) * 6 : 0;
      g.save(); g.translate(700 + vib, 960); g.rotate(0.12 + vib * 0.004); glow(g, 0, -100, 460, '#DCE3C8', toca ? 0.16 + 0.06 * Math.sin(t * 6) : 0.04);
      rrect(g, -124, -276, 260, 580, 40, '#000', 0.4); rrect(g, -130, -290, 260, 580, 40, '#26262B'); rrect(g, -116, -276, 232, 552, 30, '#2F2F35');
      rect(g, -96, -232, 192, 204, '#0D0F0E'); rect(g, -88, -224, 176, 188, '#DCE3C8', toca ? 0.95 : 0.15);
      if (toca) { text(g, 'DONA', 0, -168, 34, '#1A1E14', { align: 'center', mono: 1, w: 700 }); text(g, 'DALVA', 0, -128, 34, '#1A1E14', { align: 'center', mono: 1, w: 700 }); text(g, 'chamando...', 0, -72, 20, '#1A1E14', { align: 'center', mono: 1, w: 700 }); }
      for (let r = 0; r < 4; r++) for (let k = 0; k < 3; k++) rrect(g, -84 + k * 60, 20 + r * 62, 48, 44, 12, '#3E3E46'); g.restore();
      vinheta(g, 0.65);
    },
    sofa(g, t, c = {}) { // o sofá do saguão de perto: c.costas = visto por trás com o vulto (c.vulto:false = vazio); de frente, quem senta vem como personagem (pose 'sentada', escala 1, x 0.5)
      vgrad(g, 0, 1240, '#2A2421', '#1B1819'); for (let x = 0; x < W; x += 54) rect(g, x, 0, 18, 820, '#FFFFFF', 0.018); rect(g, 0, 820, W, 420, '#181516'); rect(g, 0, 812, W, 12, '#2E2725');
      vgrad(g, 1240, H, '#16131A', '#0C0B0D'); glow(g, 300, 300, 800, LUZ, 0.1);
      if (c.costas) sofaCostas(g, 540, 1420, 1, c.vulto !== false, t); else sofaFrente(g, 540, 1240, 1);
      vinheta(g, 0.6);
    },
    chao(g, t, c = {}) { // rente ao chão do saguão: a sombra do sétimo sai do sofá e se estica até o pé da Bia, que recua
      vgrad(g, 0, 640, '#1B1819', '#141114'); rect(g, 40, 520, 320, 100, '#2E2125'); rect(g, 60, 620, 20, 22, '#120E10'); rect(g, 320, 620, 20, 22, '#120E10');
      vgrad(g, 640, H, '#211B1C', '#0E0C0D'); for (let i = -8; i <= 8; i++) line(g, 540 + i * 40, 640, 540 + i * 260, H, '#0A0909', 3, 0.7); for (let j = 1; j < 9; j++) rect(g, 0, 640 + Math.pow(j / 9, 1.8) * 1280, W, 2, '#0A0909', 0.5);
      glow(g, 700, 300, 700, LUZ, 0.08);
      const Dd = c.dur || 6, k = out(clamp(t / (Dd * 0.6))), rec = out(clamp((t - Dd * 0.6) / 0.7)), tx = lerp(240, 700, k), ty = lerp(680, 1420, k);
      g.fillStyle = 'rgba(3,2,3,0.88)'; g.beginPath(); g.moveTo(70, 642); g.lineTo(330, 642); g.lineTo(tx + 70, ty - 60); for (let i = 0; i < 4; i++) { g.lineTo(tx + 50 - i * 30 + 40, ty + 10 + i * 6); g.lineTo(tx + 40 - i * 30, ty - 20 + i * 8); } g.lineTo(tx - 80, ty - 30); g.closePath(); g.fill();
      const bia = (c._elenco || {}).bia || {}, cal = bia.calca || '#2F3A52', bx = 820 + rec * 160;
      for (const [dx, h] of [[-120, 0], [40, 30]]) { rect(g, bx + dx, 900 + h, 120, 520, cal); rect(g, bx + dx, 900 + h, 120, 520, 'rgba(0,0,0,0.15)'); rrect(g, bx + dx - 36, 1400 + h, 186, 90, 34, '#D8D4C9'); rect(g, bx + dx - 36, 1466 + h, 186, 22, '#8E8A80'); }
      vinheta(g, 0.6);
    },
    punho(g, t, c = {}) { // a mão gelada da Dalva fecha no punho da Bia; o cinza se espalha pela pele
      vgrad(g, 0, H, '#1E1A1C', '#0C0B0D'); glow(g, 540, 900, 900, LUZ, 0.08);
      const bia = (c._elenco || {}).bia || {}, dal = (c._elenco || {}).dalva || {}, pele = bia.pele || '#C99A74', tr = (rnd(Math.floor(t * 20)) - 0.5) * 5, k = clamp(t / 4);
      g.save(); g.translate(tr, 0);
      rrect(g, -120, 800, 580, 320, 70, bia.camisa || '#D9A441'); rect(g, 400, 810, 64, 300, 'rgba(0,0,0,0.18)');
      rrect(g, 440, 868, 340, 200, 90, pele); circ(g, 810, 960, 124, pele); for (let i = 0; i < 4; i++) rrect(g, 846, 878 + i * 46, 74, 40, 20, '#B88A66');
      const gr = g.createRadialGradient(610, 960, 20, 610, 960, 80 + 260 * k); gr.addColorStop(0, rgba(CINZA, 0.75)); gr.addColorStop(1, rgba(CINZA, 0)); g.fillStyle = gr; g.fillRect(380, 820, 560, 300);
      g.save(); g.translate(610, 960); g.rotate(-0.15); const ap = 1 - 0.06 * out(clamp(t / 0.6));
      rrect(g, -150, -960, 300, 660, 80, dal.camisa || '#6B4C8A'); rrect(g, -150, -960, 300, 660, 80, 'rgba(0,0,0,0.15)'); rect(g, -150, -330, 300, 40, dal.blusa || '#D8D2C4');
      rrect(g, -150, -320, 300, 250, 110, CINZA); for (let i = 0; i < 4; i++) rrect(g, -130 + i * 68, -120, 58, 236 * ap, 29, '#8C8A88'); rrect(g, -196, -220, 72, 210, 36, '#8C8A88'); g.restore();
      g.restore(); vinheta(g, 0.6);
    },
    clarao(g, t, c = {}) { // as luzes estouram em branco; a Dalva se desfaz em pó (c.vulto:false tira)
      const k = clamp(t / 3); vgrad(g, 0, H, '#2A2724', '#141213'); glow(g, W / 2, H * 0.42, 1200, '#FFFFFF', 0.45 * (1 - k) + 0.12);
      if (c.vulto !== false) { g.globalAlpha = 0.85 * (1 - k); g.fillStyle = '#0D0B0E'; g.beginPath(); g.ellipse(540, 640, 82, 96, 0, 0, Math.PI * 2); g.ellipse(532, 540, 40, 36, 0, 0, Math.PI * 2); g.fill(); g.beginPath(); g.moveTo(450, 730); g.lineTo(630, 730); g.lineTo(700, 1300); g.lineTo(380, 1300); g.fill(); g.globalAlpha = 1;
        for (let i = 0; i < 90; i++) { const px = 540 + (rnd(i) - 0.5) * 360 + Math.sin(t * 2 + i) * 20 * t, py = 560 + rnd(i + 1) * 740 - t * (60 + rnd(i + 2) * 220); circ(g, px, py, 3 + rnd(i + 3) * 6, '#0D0B0E', clamp(k * 1.6) * (1 - k) * 0.9); } }
      rect(g, 0, 0, W, H, '#FFFFFF', Math.pow(1 - clamp((t - (c.branco || 0)) / 1.6), 2) * 0.95); // c.branco = segundos de tela toda branca antes de clarear (ep07)
    },
    amanhecer(g, t, c = {}) { // o sol nasce na janela do saguão: tudo esquenta e clareia
      const k = clamp(t / 6); vgrad(g, 0, 1240, '#3A302A', '#2A221E'); for (let x = 0; x < W; x += 54) rect(g, x, 0, 18, 1240, '#FFFFFF', 0.02);
      const x0 = 140, y0 = 240, w = 800, h = 760; rect(g, x0 - 26, y0 - 26, w + 52, h + 52, '#4A3A30');
      g.save(); g.beginPath(); g.rect(x0, y0, w, h); g.clip(); vgrad(g, y0, y0 + h, '#4A5878', '#F2C46B', x0, w); const sy = y0 + h + 60 - k * 240;
      glow(g, 540, sy, 640, SOL, 0.7); circ(g, 540, sy, 120, '#FFEBC0'); poly(g, [[x0, y0 + h], [x0, y0 + h - 120], [300, y0 + h - 170], [520, y0 + h - 110], [760, y0 + h - 190], [x0 + w, y0 + h - 130], [x0 + w, y0 + h]], '#3A3A44'); g.restore();
      rect(g, x0 + w / 2 - 9, y0, 18, h, '#4A3A30'); rect(g, x0, y0 + h / 2 - 9, w, 18, '#4A3A30');
      vgrad(g, 1240, H, '#3A2E26', '#1E1814'); poly(g, [[x0, y0 + h], [x0 + w, y0 + h], [W + 260, H], [-260, H]], SOL, 0.08 + 0.08 * k); glow(g, 540, 1000, 1100, SOL, 0.12 + 0.18 * k);
    },
    ruina(g, t, c = {}) { // a pousada de manhã: ruína, teto caído, mato alto, letreiro 'VALE VER'
      vgrad(g, 0, 1150, '#6E7684', '#B9B6AA'); glow(g, 820, 860, 700, '#F3E3B8', 0.25);
      poly(g, [[0, 1150], [0, 880], [260, 820], [520, 900], [800, 800], [1080, 870], [1080, 1150]], '#4B5150');
      rect(g, 140, 640, 800, 520, '#5A534C'); for (let i = 0; i < 9; i++) line(g, 160 + rnd(i) * 760, 660 + rnd(i + 1) * 300, 160 + rnd(i) * 760 + 40, 700 + rnd(i + 1) * 300 + 80, '#3B3632', 4);
      for (const x of [200, 380, 700]) { rect(g, x, 760, 130, 150, '#1E1C1B'); poly(g, [[x, 760], [x + 50, 760], [x + 20, 820]], '#3B3A3A'); }
      rect(g, 780, 760, 130, 150, '#1E1C1B'); rect(g, 470, 900, 170, 260, '#151312');
      poly(g, [[110, 650], [300, 520], [360, 600], [520, 470], [560, 560], [700, 500], [960, 650], [940, 690], [140, 690]], '#2E2A28'); for (const [a, b, d] of [[260, 540, 680], [520, 480, 700], [760, 560, 650]]) line(g, a, b, d, 650, '#3B3430', 10);
      g.save(); g.translate(540, 720); g.rotate(-0.13); line(g, -190, -44, -190, -90, '#2A2624', 4); rect(g, -260, -44, 440, 84, '#2A2624'); text(g, 'VALE VER', -232, 18, 54, '#A39C90'); g.restore();
      vgrad(g, 1150, H, '#5B5E4E', '#2F3229'); poly(g, [[440, 1150], [640, 1150], [920, H], [160, H]], '#6A645A');
      for (let i = 0; i < 160; i++) { const x = rnd(i) * W, b = 1150 + rnd(i + 9) * 760, hh = 60 + rnd(i + 4) * 160, sw = Math.sin(t * 1.3 + i) * 10; if (x > 380 && x < 700 && b < 1500) continue; poly(g, [[x - 8, b], [x + 8, b], [x + sw, b - hh]], rnd(i + 2) > 0.5 ? '#4A5543' : '#3A4436'); }
      for (let i = 0; i < 3; i++) rect(g, ((t * 16 + i * 400) % 1500) - 300, 1000 + i * 60, 600, 40, '#FFFFFF', 0.06);
    },
    ponto_manha(g, t) { // o mesmo ponto de ônibus, de manhã, sem chuva, poste apagado
      vgrad(g, 0, 1130, '#5B6578', '#D2C2A2'); glow(g, 900, 1100, 600, '#F3E3B8', 0.3);
      for (let i = 0; i < 9; i++) { const x = i * 128 - 30, h = 110 + rnd(i + 11) * 210; rect(g, x, 1130 - h, 118, h, '#3E4250'); for (let j = 0; j < 6; j++) if (rnd(i * 7 + j) > 0.72) rect(g, x + 14 + (j % 3) * 34, 1130 - h + 24 + Math.floor(j / 3) * 46, 18, 24, '#2A2D38'); }
      vgrad(g, 1130, 1300, '#4A474B', '#3A383C'); rect(g, 0, 1296, W, 16, '#56535A'); vgrad(g, 1312, H, '#2E2D31', '#232226');
      rect(g, 748, 300, 26, 1000, '#2E2D35'); rect(g, 640, 296, 134, 12, '#2E2D35'); poly(g, [[598, 308], [692, 308], [680, 336], [610, 336]], '#3A3942'); rect(g, 612, 334, 66, 6, '#8E8A80');
      rect(g, 800, 1150, 150, 12, '#3A3940'); rect(g, 808, 1162, 10, 90, '#3A3940'); rect(g, 930, 1162, 10, 90, '#3A3940'); vinheta(g, 0.35);
    },
  };
  CENARIOS.escada.piso = x => { const k = Math.floor((W - x) / 100); return 1560 - Math.max(0, Math.min(8, k)) * 66; }; // altura do degrau sob x (personagem com "noPiso")
  CENARIOS.papel.claro = true;

  // ───────────── PERSONAGENS (formas simples; origem nos pés; altura ~540 px na escala 1) ─────────────
  const POSES = {
    neutro: t => ({ al: [-8, 195], ar: [8, 195], fl: [-30, 235], fr: [30, 235], olho: 'ponto', boca: 'reta', sobr: 0 }),
    assustado: t => ({ al: [-52, -150], ar: [52, -150], fl: [-44, 226], fr: [44, 226], olho: 'grande', boca: 'O', sobr: 1, tremer: 5, olhar: Math.sin(t * 9) * 4 }),
    correndo: t => { const s = Math.sin(t * 14), c = Math.cos(t * 14); return { al: [-30 + 90 * s, 150 - 30 * c], ar: [30 - 90 * s, 150 + 30 * c], fl: [-70 * s, 235 - 22 * Math.max(0, c)], fr: [70 * s, 235 - 22 * Math.max(0, -c)], olho: 'firme', boca: 'aberta', sobr: 0, inclina: 0.2, quica: Math.abs(c) * 16, olhar: 6 }; },
    olhando: t => ({ al: [-8, 195], ar: [190, -30], fl: [-30, 235], fr: [30, 235], olho: 'lado', boca: 'reta', sobr: 0, olhar: 10, cabeca: 0.08 }),
    sussurrando: t => ({ al: [10, 150], ar: [-24, -62], fl: [-30, 235], fr: [30, 235], olho: 'lado', boca: 'pequena', sobr: 0.5, olhar: 9, cabeca: 0.1 }),
    chorando: t => ({ al: [-22, -88], ar: [22, -88], fl: [-30, 235], fr: [30, 235], olho: 'fechado', boca: 'triste', sobr: 1, tremer: 3, cabeca: 0.22, lagrimas: true, quica: -10 }),
    cansada: t => ({ al: [-8, 195], ar: [8, 195], fl: [-30, 235], fr: [30, 235], olho: 'meio', boca: 'reta', sobr: 0.2, cabeca: 0.05 }),
    hesitante: t => ({ al: [34, 118], ar: [-34, 118], fl: [-26, 235], fr: [26, 235], olho: 'lado', boca: 'pequena', sobr: 0.5, olhar: 8 }),
    sorrindo: t => ({ al: [-6, 195], ar: [6, 195], fl: [-26, 235], fr: [26, 235], olho: 'fixo', boca: 'sorriso', sobr: 0 }), // Dona Dalva: sorriso largo, não pisca
    entregando: t => ({ al: [-6, 195], ar: [150, 40], fl: [-26, 235], fr: [26, 235], olho: 'fixo', boca: 'sorriso', sobr: 0, itemR: 'chave' }),
    segurando: t => ({ al: [46, 112], ar: [-46, 112], fl: [-30, 235], fr: [30, 235], olho: 'lado', boca: 'pequena', sobr: 0.3, olhar: 2, item: 'caderno' }),
    acenando: t => ({ al: [-8, 195], ar: [70 + 34 * Math.sin(t * 8), -170], fl: [-30, 235], fr: [30, 235], olho: 'ponto', boca: 'sorrisinho', sobr: 0.6 }),
    cumprimentando: t => ({ al: [-8, 195], ar: [160, 30 + 8 * Math.sin(t * 6)], fl: [-30, 235], fr: [30, 235], olho: 'ponto', boca: 'sorrisinho', sobr: 0 }),
    lamentando: t => t < 1.1 ? ({ al: [-8, 195], ar: [8, 195], fl: [-30, 235], fr: [30, 235], olho: 'ponto', boca: 'sorrisinho', sobr: 0 }) // o sorriso some e ele fecha os olhos
      : ({ al: [-8, 195], ar: [8, 195], fl: [-30, 235], fr: [30, 235], olho: 'baixo', boca: 'triste', sobr: 1, cabeca: 0.09 * clamp((t - 1.1) / 0.6) }),
    // ── ep02-07 ──
    pegando: t => { const k = clamp((t - 2.2) / 0.6); return { al: [-8, 195], ar: [lerp(190, 150, k), lerp(-30, 40, k)], fl: [-30, 235], fr: [30, 235], olho: 'lado', olhar: 10, boca: 'pequena', sobr: 0.7, itemR: k > 0.4 ? 'chave' : undefined }; }, // ep03: estica a mão à chave e a traz (a chave some da porta em c.pega = 2.2)
    aliviadaMedo: t => t < 1.6 ? POSES.aliviada(t) : POSES.medo(t - 1.6), // ep03: alívio e, de repente, olhos grandes
    medo: t => ({ al: [-52, -150], ar: [52, -150], fl: [-44, 226], fr: [44, 226], olho: 'grande', boca: 'O', sobr: 1, tremer: 4, olhar: Math.sin(t * 9) * 4 }), // como 'assustado', sem tremer a câmera
    orelhas: t => ({ al: [-12, -95], ar: [12, -95], fl: [-30, 235], fr: [30, 235], olho: 'apertado', boca: 'triste', sobr: 1, tremer: 2 }), // mãos tapando as orelhas
    telefone: t => ({ al: [-8, 195], ar: [6, -96], fl: [-30, 235], fr: [30, 235], olho: 'lado', boca: 'pequena', sobr: 0.6, olhar: 7, itemR: 'fone' }),
    aliviada: t => ({ al: [-14, 196], ar: [14, 196], fl: [-30, 235], fr: [30, 235], olho: 'apertado', boca: 'sorrisinho', sobr: 0, cabeca: 0.05, quica: -6 }),
    apontandoCima: t => ({ al: [-8, 195], ar: [30, -205], fl: [-30, 235], fr: [30, 235], olho: 'lado', olhar: 6, olharY: -6, boca: 'reta', sobr: 0.5 }),
    apontando: t => ({ al: [-8, 195], ar: [205, -40], fl: [-30, 235], fr: [30, 235], olho: 'fixo', boca: 'sorriso', sobr: 0 }),
    negando: t => ({ al: [-8, 195], ar: [8, 195], fl: [-30, 235], fr: [30, 235], olho: 'ponto', boca: 'reta', sobr: 0.7, rosto: Math.sin(t * 7) * 11, cabeca: Math.sin(t * 7) * 0.03 }), // balança a cabeça: não
    assentindo: t => ({ al: [-8, 195], ar: [8, 195], fl: [-30, 235], fr: [30, 235], olho: 'ponto', boca: 'reta', sobr: 0.3, cabY: Math.max(0, Math.sin(t * 5)) * 10 }),
    encarando: t => ({ al: [-6, 195], ar: [6, 195], fl: [-30, 235], fr: [30, 235], olho: 'fixo', boca: 'reta', sobr: 0 }), // hóspedes: olham sem piscar
    silencio: t => ({ al: [-8, 195], ar: [-46, -50], fl: [-30, 235], fr: [30, 235], olho: 'lado', olhar: 6, boca: 'reta', sobr: 0.7 }), // dedo nos lábios
    procurando: t => ({ al: [40, 205], ar: [96, 180 + Math.sin(t * 6) * 14], fl: [-30, 235], fr: [30, 235], olho: 'lado', olhar: 8, olharY: 5, boca: 'pequena', sobr: 0.8, inclina: 0.12 }),
    lanterna: t => ({ al: [-8, 195], ar: [150, -10], fl: [-30, 235], fr: [30, 235], olho: 'grande', olhar: 5, olharY: -4, boca: 'pequena', sobr: 0.8, itemR: 'lanterna' }),
    sentada: t => ({ al: [52, 160], ar: [-52, 160], fl: [0, 0], fr: [0, 0], olho: 'fixo', boca: 'sorriso', sobr: 0, sentado: true }), // Dalva no sofá, mãos no colo
    sentadaSeria: t => ({ al: [52, 160], ar: [-52, 160], fl: [0, 0], fr: [0, 0], olho: 'fixo', boca: 'reta', sobr: 0, sentado: true, cabeca: -0.1 * clamp(t / 2.5), rosto: -12 * clamp(t / 2.5) }), // ep06: Dalva sentada para de sorrir e vira a cabeça
    olhandoBaixo: t => ({ al: [-8, 195], ar: [8, 195], fl: [-30, 235], fr: [30, 235], olho: 'baixoAberto', boca: 'reta', sobr: 0.9, tremer: 1.5, cabeca: 0.06 }),
    levantandoOlhar: t => ({ al: [-8, 195], ar: [8, 195], fl: [-30, 235], fr: [30, 235], olho: 'grande', olharY: lerp(9, -3, clamp(t / 4)), boca: 'pequena', sobr: 1, tremer: 2.5 }),
    abracando: t => ({ al: [70, 118], ar: [-70, 118], fl: [-30, 235], fr: [30, 235], olho: 'grande', boca: 'O', sobr: 1, tremer: 2 }),
    seria: t => ({ al: [-6, 195], ar: [6, 195], fl: [-26, 235], fr: [26, 235], olho: 'fixo', boca: 'reta', sobr: 0, cabeca: -0.1 * clamp(t / 2.5), rosto: -12 * clamp(t / 2.5) }), // Dalva para de sorrir e vira a cabeça
    maoRelogio: t => ({ al: [-6, 195], ar: [40, -235], fl: [-26, 235], fr: [26, 235], olho: 'fixo', boca: 'sorriso', sobr: 0 }),
    rachado: t => ({ al: [-6, 195], ar: [6, 195], fl: [-26, 235], fr: [26, 235], olho: 'fixo', boca: 'sorriso', sobr: 0, rachado: true, tremer: 1 }), // o sorriso volta, rachado
    maosDadas: t => ({ al: [-62, 175], ar: [62, 175], fl: [-30, 235], fr: [30, 235], olho: 'ponto', boca: 'sorrisinho', sobr: 0, cabY: Math.max(0, Math.sin(t * 4)) * 6 }),
    decidida: t => ({ al: [-10, 195], ar: [10, 195], fl: [-30, 235], fr: [30, 235], olho: 'firme', boca: 'reta', sobr: 0, brilho: true }), // olhos marejados, firme
    dandoCorda: t => ({ al: [-8, 195], ar: [60, -215], fl: [-30, 235], fr: [30, 235], olho: 'firme', boca: 'reta', sobr: 0 }),
    lendo: t => ({ al: [46, 112], ar: [-46, 112], fl: [-30, 235], fr: [30, 235], olho: 'fixo', boca: 'reta', sobr: 0, item: 'pagina' }), // segura a página (o reflexo não pisca)
    gravida: t => ({ al: [70, 104], ar: [-56, 100], fl: [-30, 235], fr: [30, 235], olho: 'ponto', boca: 'reta', sobr: 0.4 }), // mãos na barriga
  };
  // visuais por personagem: camisa, calça, cabelo, pele, estilo do cabelo. Sem "elenco" no JSON, sai uma combinação fixa pelo id.
  const CAMISAS = ['#C8553D', '#3E6A8A', '#6B8E4E', '#8A5A9A', '#D9A441', '#4A4650'], CALCAS = ['#2F3A52', '#3B3330', '#4A4650', '#2A3B33'], CABELOS = ['#1B1412', '#4A2E1E', '#B8782E', '#8C8B86', '#2A1F3A'], PELES = ['#D8B08C', '#B98A63', '#8C5E3F', '#EAC9A5'], ESTILOS = ['curto', 'longo', 'coque', 'careca'];
  const hash = s => [...s].reduce((a, c) => (a * 31 + c.charCodeAt(0)) >>> 0, 7);
  function visual(o, elenco) {
    const h = hash(o.id), e = Object.assign({}, elenco && elenco[o.id], o);
    return { camisa: e.camisa || e.cor || CAMISAS[h % CAMISAS.length], calca: e.calca || CALCAS[(h >> 3) % CALCAS.length], cabelo: e.cabelo || CABELOS[(h >> 5) % CABELOS.length], pele: e.pele || PELES[(h >> 7) % PELES.length], estilo: e.estilo || ESTILOS[(h >> 9) % ESTILOS.length],
      mochila: e.mochila, capuz: e.capuz, blusa: e.blusa, listras: e.listras, bigode: e.bigode, oculos: e.oculos, chinelo: e.chinelo, // detalhes opcionais (true ou cor)
      bobes: e.bobes, fone: e.fone, barriga: e.barriga, dino: e.dino, touca: e.touca, semSombra: e.semSombra, luz: e.luz }; // hóspedes: bobes, fone de ouvido, grávida, pijama de dinossauro, touca de enfermeira; sem sombra; 'luz' = contorno de luz (amanhecer)
  }
  function membro(g, ax, ay, tx, ty, L, w, c, lado, wy, wx) { // braço/perna de dois segmentos (cinemática inversa simples)
    let dx = tx - ax, dy = ty - ay, d = Math.hypot(dx, dy); const mx = d > 2 * L - 0.5 ? 2 * L - 0.5 : d; dx *= mx / (d || 1); dy *= mx / (d || 1); d = mx;
    const h = Math.sqrt(Math.max(0, L * L - d * d / 4)), nx = -dy / (d || 1), ny = dx / (d || 1), mxm = ax + dx / 2, mym = ay + dy / 2;
    const e1 = [mxm + nx * h, mym + ny * h], e2 = [mxm - nx * h, mym - ny * h], sc = e => e[1] * wy + e[0] * lado * wx, e = sc(e1) >= sc(e2) ? e1 : e2;
    g.strokeStyle = c; g.lineWidth = w; g.lineCap = 'round'; g.lineJoin = 'round'; g.beginPath(); g.moveTo(ax, ay); g.lineTo(e[0], e[1]); g.lineTo(ax + dx, ay + dy); g.stroke();
    return [ax + dx, ay + dy];
  }
  // transformação comum (entrada, saída, balanço, tremor) e depois o corpo vetorial ou o PNG.
  // Com transparência (entrada/saída, 'some', 'alfa') ou 'luz', o corpo é desenhado numa camada à parte e composto com globalAlpha (rect/circ zeram o alpha).
  let camada = null;
  function personagem(g, o, t, dur, elenco, img) { // o: { id, pose, x(0..1), flip, escala, y, arquivo, costas, some, alfa, semEntrada, fica }
    const v = visual(o, elenco), ent = o.semEntrada ? 1 : back(clamp(t / 0.4)), sai = o.fica ? 1 : clamp((dur - t) / 0.25), fade = o.some != null ? clamp((t - o.some) / 1.2) : 0;
    const alfa = Math.min(o.semEntrada ? 1 : clamp(t / 0.25), sai) * (1 - fade) * (o.alfa ?? 1);
    if (alfa <= 0.004) return;
    if (alfa > 0.996 && !v.luz) return corpo(g, o, t, v, img, ent, sai, fade);
    if (!camada) { camada = document.createElement('canvas'); camada.width = W; camada.height = H; }
    const lg = camada.getContext('2d'); lg.setTransform(1, 0, 0, 1, 0, 0); lg.clearRect(0, 0, W, H); corpo(lg, o, t, v, img, ent, sai, fade);
    if (v.luz) { lg.globalCompositeOperation = 'source-atop'; lg.globalAlpha = 0.84; lg.fillStyle = typeof v.luz === 'string' ? v.luz : '#FFF1CC'; lg.fillRect(0, 0, W, H); lg.globalAlpha = 1; lg.globalCompositeOperation = 'source-over'; }
    g.save(); g.globalAlpha = alfa; if (v.luz) { g.shadowColor = 'rgba(255,222,140,0.95)'; g.shadowBlur = 60; } g.drawImage(camada, 0, 0); g.restore();
  }
  function corpo(g, o, t, v, img, ent, sai, fade) {
    const pf = POSES[o.pose] || POSES.neutro, s = pf(o._tp ?? t), seed = hash(o.id), esc = o.escala || 1, dir = o.flip ? -1 : 1, costas = o.costas || s.costas;
    const tr = s.tremer ? (rnd(Math.floor(t * 30) + seed) - 0.5) * s.tremer * 2 : 0, balanco = o.pose === 'correndo' ? 0 : Math.sin(t * 1.7 + seed) * 0.012, res = Math.sin(t * 2.2 + seed) * 3;
    g.save(); g.translate(o.x * W + tr + (o.semEntrada ? 0 : (1 - clamp(t / 0.4)) * 60 * dir) - (1 - sai) * 50 * dir, GY + (o.y || 0) + (1 - ent) * 40 - fade * 140 * esc);
    if (!v.semSombra && !v.luz) { g.fillStyle = 'rgba(0,0,0,0.38)'; g.beginPath(); g.ellipse(0, 4, 120 * esc, 18 * esc, 0, 0, Math.PI * 2); g.fill(); } // sombra no chão (os hóspedes não têm)
    g.scale(esc * dir * (0.94 + 0.06 * ent), esc * (0.94 + 0.06 * ent));
    g.translate(0, -(s.quica || 0)); g.rotate((s.inclina || 0) + balanco);
    if (img) { const hgt = (o.altura || 760), wd = img.width * hgt / img.height; g.drawImage(img, -wd / 2, -hgt + res, wd, hgt); g.restore(); return; }
    const hy = -235, sy = -385, D = s.sentado ? 118 : 0;
    const pe = (x, y) => { g.fillStyle = v.chinelo ? v.pele : P.deep; g.beginPath(); g.ellipse(x + 14, y + 4, 36, 15, 0, 0, Math.PI * 2); g.fill();
      if (v.chinelo) { rect(g, x - 22, y + 12, 72, 8, P.deep); line(g, x + 4, y - 6, x + 24, y + 2, typeof v.chinelo === 'string' ? v.chinelo : '#3E6A8A', 7); } };
    if (s.sentado) { for (const k of [-1, 1]) { line(g, 28 * k, hy + D, 48 * k, -104, v.calca, 46); line(g, 48 * k, -104, 44 * k, -12, v.calca, 40); pe(44 * k - 14, -8); } g.translate(0, D); } // sentada de frente: coxa curta (em escorço) e canela até o chão
    else { const foL = [-28 + s.fl[0], hy + Math.min(s.fl[1], 235)]; membro(g, -28, hy, foL[0], foL[1], 118, 42, v.calca, 1, 0.1, 1);
      const foR = membro(g, 28, hy, 28 + s.fr[0], hy + Math.min(s.fr[1], 235), 118, 42, v.calca, 1, 0.1, 1); [foL, foR].forEach(f => pe(f[0], f[1])); }
    const mc = typeof v.mochila === 'string' ? v.mochila : '#2E3440';
    if (v.mochila && !costas) rrect(g, -88, sy - 2, 176, 150, 20, mc); // mochila atrás do corpo (aparece dos lados)
    const bl = membro(g, -62, sy + 10, -62 + s.al[0], sy + 10 + s.al[1], 105, 34, v.camisa, -1, 1, 0.6);
    rrect(g, -72, sy - 14, 144, 172 + res * 0.3, 28, v.camisa); rrect(g, -72, sy + 150, 144, 44, 12, v.calca); // tronco + cós da calça
    if (v.listras || v.blusa) { g.save(); g.beginPath(); g.roundRect(-72, sy - 14, 144, 172 + res * 0.3, 28); g.clip();
      if (v.blusa && !costas) { rect(g, -24, sy - 14, 48, 180, v.blusa); line(g, -24, sy - 10, -24, sy + 160, 'rgba(0,0,0,0.25)', 4); line(g, 24, sy - 10, 24, sy + 160, 'rgba(0,0,0,0.25)', 4); } // cardigã aberto sobre a blusa
      if (v.listras) for (let x = -66; x < 72; x += 26) rect(g, x, sy - 14, 9, 190, '#FFFFFF', 0.22); // pijama listrado
      g.restore(); }
    if (v.dino && !costas) rrect(g, -40, sy + 30, 80, 110, 30, '#A9B98F'); // barriga clara do pijama de dinossauro
    if (v.barriga && !costas) { g.fillStyle = v.camisa; g.beginPath(); g.ellipse(10, sy + 122, 76, 60, 0, 0, Math.PI * 2); g.fill(); g.fillStyle = 'rgba(255,255,255,0.08)'; g.beginPath(); g.ellipse(-4, sy + 104, 40, 26, 0, 0, Math.PI * 2); g.fill(); }
    rrect(g, -72, sy - 14, 144, 30, 14, 'rgba(0,0,0,0.12)');
    if (v.mochila && !costas) { rect(g, -52, sy - 12, 16, 130, mc); rect(g, 36, sy - 12, 16, 130, mc); } // alças
    if (v.mochila && costas) { rrect(g, -80, sy + 4, 160, 176, 24, mc); rrect(g, -56, sy + 96, 112, 70, 16, 'rgba(0,0,0,0.25)'); } // de costas: a mochila inteira
    if (v.capuz) { rrect(g, -62, sy - 34, 124, costas ? 80 : 44, 22, v.camisa); rrect(g, -62, sy - 34, 124, costas ? 80 : 44, 22, 'rgba(0,0,0,0.22)'); if (!costas) { line(g, -12, sy + 8, -14, sy + 60, '#EDE4D3', 5); line(g, 12, sy + 8, 14, sy + 60, '#EDE4D3', 5); } } // capuz do moletom
    const br = membro(g, 62, sy + 10, 62 + s.ar[0], sy + 10 + s.ar[1], 105, 34, v.camisa, 1, 1, 0.6);
    if (s.item === 'caderno') { const mx = (bl[0] + br[0]) / 2, my2 = (bl[1] + br[1]) / 2; g.save(); g.translate(mx, my2 - 10); g.rotate(-0.06); rect(g, -66, -50, 132, 96, '#000', 0.3); rect(g, -70, -56, 132, 96, '#EDE4D3'); rect(g, -70, -56, 132, 90, '#3A2F2B'); rect(g, -70, -56, 16, 90, P.accent); rect(g, -40, -36, 80, 18, '#EDE4D3', 0.85); g.restore(); }
    if (s.item === 'pagina') { const mx = (bl[0] + br[0]) / 2, my2 = (bl[1] + br[1]) / 2; g.save(); g.translate(mx, my2 - 30); g.rotate(0.05); poly(g, [[-62, -80], [58, -84], [64, 70], [-54, 74], [-60, 40], [-66, 10], [-58, -20]], '#E4DCC8'); for (let i = 0; i < 5; i++) rect(g, -44, -56 + i * 24, 88 - (i % 2) * 20, 5, '#2A2626', 0.5); rect(g, -44, 64 - 8, 70, 6, P.accent, 0.8); g.restore(); }
    if (s.itemR === 'chave') { g.save(); g.translate(br[0] + 24, br[1] - 6); g.rotate(0.4); g.strokeStyle = '#C9B38A'; g.lineWidth = 7; g.beginPath(); g.arc(0, 0, 16, 0, Math.PI * 2); g.stroke(); rect(g, 14, -4, 54, 8, '#C9B38A'); rect(g, 52, 4, 8, 14, '#C9B38A'); rect(g, 38, 4, 8, 10, '#C9B38A'); g.restore(); }
    if (s.itemR === 'fone') { g.save(); g.translate(br[0] + 4, br[1] - 4); g.rotate(-0.35); rrect(g, -14, -62, 28, 124, 12, '#2A272D'); rrect(g, -22, -70, 44, 32, 10, '#2A272D'); rrect(g, -22, 40, 44, 32, 10, '#2A272D'); g.restore(); } // fone do interfone/telefone fixo
    if (s.itemR === 'lanterna') { poly(g, [[br[0] + 10, br[1] - 16], [br[0] + 520, br[1] - 420], [br[0] + 620, br[1] - 60]], LUZ, 0.13); glow(g, br[0] + 14, br[1] - 14, 90, LUZ, 0.6); rrect(g, br[0] - 10, br[1] - 40, 34, 62, 6, '#1E1E22'); } // lanterna do celular
    circ(g, bl[0], bl[1], 19, v.pele); circ(g, br[0], br[1], 19, v.pele);
    g.save(); g.translate(0, sy + 4 + (s.cabY || 0)); g.rotate((s.cabeca || 0) + Math.sin(t * 1.5 + seed) * 0.01); g.translate(0, -(sy + 4));
    const cy = -468 + res * 0.4; rect(g, -22, sy - 24, 44, 40, v.pele);
    if (v.estilo === 'longo') { rrect(g, -84, cy - 30, 56, 150, 26, v.cabelo); rrect(g, 28, cy - 30, 56, 150, 26, v.cabelo); } // cabelo comprido caindo dos lados (sem cobrir o queixo)
    if (v.estilo === 'coque') circ(g, -6, cy - 80, 32, v.cabelo);
    if (v.estilo === 'calvo') { circ(g, -66, cy - 2, 20, v.cabelo); circ(g, 66, cy - 6, 13, v.cabelo); } // só os lados, por trás da cabeça
    circ(g, 0, cy, 70, v.pele);
    if (costas) { // de costas: o cabelo cobre a cabeça, sem rosto
      if (v.estilo !== 'calvo' && v.estilo !== 'careca') { circ(g, 0, cy - 2, 74, v.cabelo); if (v.estilo === 'longo') rrect(g, -76, cy - 10, 152, 150, 40, v.cabelo); if (v.estilo === 'coque') circ(g, 0, cy - 74, 34, v.cabelo); }
      if (v.capuz) rrect(g, -70, cy + 40, 140, 50, 24, v.camisa); }
    else if (v.estilo !== 'calvo' && v.estilo !== 'careca') { g.fillStyle = v.cabelo; g.beginPath(); g.arc(0, cy, 74, Math.PI * 0.98, Math.PI * 2.02); g.quadraticCurveTo(46, cy - 44, -10, cy - 36); g.quadraticCurveTo(-52, cy - 28, -74, cy + 6); g.fill(); }
    if (v.bobes) for (let i = 0; i < 5; i++) rrect(g, -62 + i * 26, cy - 96 + Math.abs(i - 2) * 9, 22, 34, 8, '#C7BBAE');
    if (v.touca) { rect(g, -46, cy - 102, 92, 34, '#F2F0EA'); rect(g, -46, cy - 74, 92, 6, '#CFCBC0'); }
    if (v.dino) { const dc = typeof v.dino === 'string' ? v.dino : '#4E6B4A'; for (let i = -1; i <= 1; i++) poly(g, [[i * 40 - 18, cy - 62 + Math.abs(i) * 10], [i * 40, cy - 104 + Math.abs(i) * 14], [i * 40 + 18, cy - 62 + Math.abs(i) * 10]], dc); }
    if (v.fone) { g.strokeStyle = '#26252B'; g.lineWidth = 12; g.beginPath(); g.arc(0, cy, 82, Math.PI * 1.05, Math.PI * 1.95); g.stroke(); rrect(g, -94, cy - 26, 26, 56, 10, '#26252B'); rrect(g, 68, cy - 26, 26, 56, 10, '#26252B'); }
    if (costas) { g.restore(); g.restore(); return; }
    const fx = 16 + (s.rosto || 0), ey = cy - 4, lk = (s.olhar || 0), ly = (s.olharY || 0); g.lineCap = 'round';
    const eye = ex => {
      if (s.olho === 'ponto') circ(g, ex, ey, 7, P.deep);
      else if (s.olho === 'fixo') { circ(g, ex, ey, 17, '#FFF'); circ(g, ex + 2, ey + ly, 5, P.deep); } // arregalado e parado (não pisca)
      else if (s.olho === 'meio') { circ(g, ex, ey, 12, '#FFF'); circ(g, ex + 2, ey + 3, 6, P.deep); g.fillStyle = v.pele; g.beginPath(); g.arc(ex, ey, 14, Math.PI, 0); g.fill(); line(g, ex - 13, ey, ex + 13, ey, P.deep, 4); } // pálpebra caída (cansada)
      else if (s.olho === 'baixo') { g.strokeStyle = P.deep; g.lineWidth = 6; g.beginPath(); g.arc(ex, ey - 4, 12, Math.PI * 0.15, Math.PI * 0.85); g.stroke(); } // olho fechado de pesar
      else if (s.olho === 'baixoAberto') { circ(g, ex, ey, 13, '#FFF'); circ(g, ex, ey + 6, 6, P.deep); g.fillStyle = v.pele; g.beginPath(); g.arc(ex, ey - 2, 15, Math.PI, 0); g.fill(); line(g, ex - 14, ey - 2, ex + 14, ey - 2, P.deep, 4); } // olhando o chão
      else if (s.olho === 'grande') { circ(g, ex, ey, 19, '#FFF'); circ(g, ex + lk, ey + ly, 7, P.deep); }
      else if (s.olho === 'lado') { circ(g, ex, ey, 13, '#FFF'); circ(g, ex + lk * 0.9, ey + ly * 0.8, 6, P.deep); }
      else if (s.olho === 'firme') { circ(g, ex, ey, 10, '#FFF'); circ(g, ex + lk, ey, 6, P.deep); line(g, ex - 16, ey - 20, ex + 14, ey - 12, P.deep, 7); }
      else { g.strokeStyle = P.deep; g.lineWidth = 6; g.beginPath(); g.arc(ex, ey + 4, 13, Math.PI * 1.1, Math.PI * 1.9); g.stroke(); }
      if (s.brilho) { circ(g, ex - 4, ey - 4, 4, '#FFF', 0.95); g.strokeStyle = 'rgba(207,230,245,0.9)'; g.lineWidth = 4; g.beginPath(); g.arc(ex, ey + 2, 14, Math.PI * 0.2, Math.PI * 0.8); g.stroke(); } // olhos cheios d'água
    };
    eye(fx - 24); eye(fx + 24);
    if (s.sobr) { const a = 12 * s.sobr; line(g, fx - 42, ey - 34 - a * 0.6, fx - 10, ey - 34 - a * 1.4, P.deep, 6); line(g, fx + 10, ey - 34 - a * 1.4, fx + 42, ey - 34 - a * 0.6, P.deep, 6); }
    const my = cy + 38; g.strokeStyle = P.deep; g.fillStyle = P.deep; g.lineWidth = 7;
    if (s.boca === 'reta') line(g, fx - 12, my, fx + 12, my, P.deep, 7);
    else if (s.boca === 'O') { g.beginPath(); g.ellipse(fx, my + 2, 14, 20 + Math.sin(t * 14) * 2, 0, 0, Math.PI * 2); g.fill(); } // boca em "o" no susto
    else if (s.boca === 'aberta') { g.beginPath(); g.ellipse(fx + 4, my, 16, 11, 0, 0, Math.PI * 2); g.fill(); }
    else if (s.boca === 'pequena') circ(g, fx - 8, my, 6, P.deep);
    else if (s.boca === 'triste') { g.beginPath(); g.arc(fx, my + 14, 20, Math.PI * 1.15, Math.PI * 1.85); g.stroke(); }
    else if (s.boca === 'sorrisinho') { g.beginPath(); g.arc(fx, my - 10, 16, Math.PI * 0.2, Math.PI * 0.8); g.stroke(); }
    else if (s.boca === 'sorriso') { g.beginPath(); g.moveTo(fx - 34, my - 8); g.quadraticCurveTo(fx, my + 46, fx + 34, my - 8); g.closePath(); g.fill(); g.fillStyle = '#F4F0E6'; g.beginPath(); g.moveTo(fx - 28, my - 4); g.lineTo(fx + 28, my - 4); g.quadraticCurveTo(fx, my + 10, fx - 28, my - 4); g.fill(); } // sorriso largo demais
    if (s.rachado) { const rc = (pts) => { g.strokeStyle = '#2A2226'; g.lineWidth = 3.5; g.beginPath(); pts.forEach(([a, b], i) => i ? g.lineTo(fx + a, b) : g.moveTo(fx + a, b)); g.stroke(); }; // rachaduras saindo do sorriso
      rc([[-34, my - 8], [-50, my - 26], [-46, my - 46], [-60, my - 70]]); rc([[34, my - 8], [52, my - 22], [48, my - 40], [62, my - 56]]); rc([[-50, my - 26], [-64, my - 20]]); rc([[6, cy - 66], [16, cy - 46], [4, cy - 30]]); }
    if (v.bigode) { g.fillStyle = typeof v.bigode === 'string' ? v.bigode : v.cabelo; g.beginPath(); g.ellipse(fx - 13, my - 14, 18, 9, 0.15, 0, Math.PI * 2); g.ellipse(fx + 13, my - 14, 18, 9, -0.15, 0, Math.PI * 2); g.fill(); }
    if (v.oculos) { g.strokeStyle = '#2A2626'; g.lineWidth = 5; g.beginPath(); g.arc(fx - 24, ey, 21, 0, Math.PI * 2); g.moveTo(fx + 45, ey); g.arc(fx + 24, ey, 21, 0, Math.PI * 2); g.moveTo(fx - 3, ey); g.lineTo(fx + 3, ey); g.stroke(); }
    if (s.lagrimas) for (let i = 0; i < 4; i++) { const k = (t * 1.1 + i * 0.27) % 1, ex = fx + (i % 2 ? 24 : -24) + (i > 1 ? 4 : 0); circ(g, ex, ey + 14 + k * 90, 6 * (1 - k * 0.4), '#CFE6F5', 0.9 * (1 - k)); }
    g.restore(); g.restore();
  }

  // ───────────── OBJETOS GRANDES E INFOGRÁFICOS (entram por cima da cena) ─────────────
  const OBJETOS = {
    celular(g, o, u) { // celular vermelho com alerta: entra de baixo, inclina e vibra
      const k = back(clamp(u / 0.5)), inc = (o.inclina ?? -0.18) * k, vib = u > 0.6 ? Math.sin(u * 60) * 0.012 * Math.exp(-(u - 0.6) * 0.8) * 3 : 0;
      g.save(); g.translate(o.x * W, lerp(H + 600, (o.y ?? 0.45) * H, k)); g.rotate(inc + vib); g.scale(o.escala || 1, o.escala || 1);
      rrect(g, -190, -340, 380, 680, 56, 'rgba(0,0,0,0.25)'); g.translate(-8, -8);
      rrect(g, -190, -340, 380, 680, 56, P.accent); rrect(g, -168, -318, 336, 636, 40, '#1B1A1D'); rrect(g, -40, -306, 80, 14, 7, P.accent);
      rrect(g, -142, -190, 284, 230, 28, P.paper); circ(g, -92, -120, 34, P.accent); text(g, '!', -92, -100, 62, P.paper, { align: 'center' });
      text(g, (o.titulo || 'ALERTA').toUpperCase(), -40, -112, 40, P.deep); text(g, (o.texto || 'nova mensagem'), -40, -62, 24, P.lite, { w: 700 });
      rrect(g, -142, 70, 284, 18, 9, '#3A363D'); rrect(g, -142, 108, 200, 18, 9, '#3A363D'); g.restore();
    },
    predio(g, o, u) { // corte de prédio com andares numerados e destaque laranja no andar do protagonista
      const n = o.andares || 8, fh = 100, w = 520, k = out(clamp(u / 0.5)), x0 = (o.x ?? 0.5) * W - w / 2, y0 = (o.y ?? 0.2) * H;
      g.save(); g.globalAlpha = k; g.translate(0, (1 - k) * 60); rrect(g, x0 - 16, y0 - 40, w + 32, n * fh + 56, 10, '#3B3330');
      poly(g, [[x0 - 30, y0 - 40], [x0 + w / 2, y0 - 110], [x0 + w + 30, y0 - 40]], '#2A2320');
      for (let i = 0; i < n; i++) { const num = n - i, y = y0 + i * fh, dest = num === o.destaque; rect(g, x0, y, w, fh - 8, dest ? P.orange : '#EDE4D3');
        text(g, String(num), x0 + 24, y + 66, 52, dest ? '#FFF' : '#8A7F6C', { w: 800 }); for (let j = 0; j < 3; j++) rect(g, x0 + 190 + j * 110, y + 22, 80, 52, dest ? '#FFD9A8' : '#C9D8E0');
        if (dest) { circ(g, x0 + 150, y + 62, 14, P.deep); rect(g, x0 + 136, y + 70, 28, 22, P.deep); } }
      g.restore();
    },
    seta(g, o, u) { // seta apontando com nome
      const k = out(clamp(u / 0.4)), x1 = o.x * W, y1 = o.y * H, x2 = lerp(x1, o.x2 * W, k), y2 = lerp(y1, o.y2 * H, k), a = Math.atan2(y2 - y1, x2 - x1);
      g.save(); line(g, x1, y1, x2, y2, P.accent, 14); poly(g, [[x2, y2], [x2 - 46 * Math.cos(a - 0.45), y2 - 46 * Math.sin(a - 0.45)], [x2 - 46 * Math.cos(a + 0.45), y2 - 46 * Math.sin(a + 0.45)]], P.accent);
      g.font = '700 54px Oswald, Impact, sans-serif'; const tw = g.measureText((o.texto || '').toUpperCase()).width + 50; g.globalAlpha = k; rrect(g, x1 - tw / 2, y1 - 50, tw, 76, 14, P.deep);
      g.letterSpacing = '0px'; g.fillStyle = '#FFF'; g.textAlign = 'center'; g.fillText((o.texto || '').toUpperCase(), x1, y1 + 8); g.textAlign = 'left'; g.restore();
    },
    cartaz(g, o, u) { // cartaz de papel colado (ex.: vaga de emprego): linhas [{t, tam, cor:'accent'}], tiras destacáveis embaixo
      const k = back(clamp(u / 0.5)), w = o.w || 440, ls = o.linhas || [{ t: o.texto || 'AVISO', tam: 80 }];
      g.font = '900 10px Geist'; const pre = ls.map(l => { g.font = `900 ${l.tam || 60}px Geist`; g.letterSpacing = `${-0.02 * (l.tam || 60)}px`; return { ...l, ls: quebra(g, String(l.t).toUpperCase().split(' '), w - 60) }; });
      const h = 50 + pre.reduce((a, l) => a + l.ls.length * (l.tam || 60) * 1.04 + 22, 0) + (o.tiras ? 110 : 20);
      g.save(); g.translate(o.x * W, (o.y ?? 0.4) * H); g.rotate((o.inclina ?? 0.035) + Math.sin(u * 2.2) * 0.006); g.scale(lerp(0.5, 1, k), lerp(0.5, 1, k)); g.globalAlpha = clamp(u / 0.2);
      rect(g, -w / 2 + 14, -h / 2 + 18, w, h, '#000', 0.4); rect(g, -w / 2, -h / 2, w, h, '#E9E3D3'); vgrad(g, -h / 2, h / 2, 'rgba(255,255,255,0.10)', 'rgba(80,60,30,0.18)', -w / 2, w);
      rect(g, -w / 2 - 20, -h / 2 - 16, 110, 34, '#CFC8B4', 0.75); rect(g, w / 2 - 90, -h / 2 - 16, 110, 34, '#CFC8B4', 0.75); // fita adesiva
      let y = -h / 2 + 44; pre.forEach(l => { const sz = l.tam || 60; l.ls.forEach(ln => { y += sz * 0.86; text(g, ln.join(' '), 0, y, sz, l.cor === 'accent' ? P.accent : '#1A1819', { align: 'center', w: l.w || 900 }); y += sz * 0.18; }); y += 22; });
      if (o.tiras) { rect(g, -w / 2 + 20, h / 2 - 104, w - 40, 3, '#1A1819', 0.4); for (let i = 0; i < 7; i++) { const tx = -w / 2 + 20 + i * (w - 40) / 7; rect(g, tx, h / 2 - 100, 3, 100, '#1A1819', 0.3); g.save(); g.translate(tx + (w - 40) / 14, h / 2 - 50); g.rotate(-Math.PI / 2); text(g, '9 9999', 0, 8, 20, '#1A1819', { align: 'center', w: 700, mono: 1 }); g.restore(); } }
      g.restore();
    },
    regras(g, o, u, cx) { // caderno de regras como cartão grande; cada regra entra quando a narração chega na palavra de "gatilhos"
      const k = out(clamp(u / 0.45)), w = o.w || 860, x0 = o.x * W - w / 2, y0 = (o.y ?? 0.16) * H, h = o.h || 880, rs = o.itens || [];
      const tIni = rs.map((_, i) => o.gatilhos && cx ? cx.inicio(o.gatilhos[i]) - (cx.u - u) : (o.tempos ? o.tempos[i] : 0.6 + i * 2.4));
      g.save(); g.globalAlpha = k; g.translate(0, (1 - k) * 120); g.translate(o.x * W, y0 + h / 2); g.rotate(-0.012); g.translate(-o.x * W, -(y0 + h / 2));
      const pts = o.topoRasgado ? [[x0, y0 + h], [x0, y0 + 12 + rnd(3) * 16]] : [[x0, y0], [x0 + w, y0]]; if (o.topoRasgado) { for (let x = 0; x <= w; x += 22) pts.push([x0 + x, y0 + 4 + rnd(x + 5) * 24]); pts.push([x0 + w, y0 + h]); } else for (let x = w; x >= 0; x -= 26) pts.push([x0 + x, y0 + h - 4 - rnd(x + 7) * 20]); // borda de baixo rasgada (a regra 6 foi arrancada); ep06: topoRasgado = a página arrancada (borda rasgada em cima)
      poly(g, pts.map(([a, b]) => [a + 18, b + 26]), '#000', 0.45); poly(g, pts, '#ECE6D6'); g.save(); g.beginPath(); pts.forEach(([a, b], i) => i ? g.lineTo(a, b) : g.moveTo(a, b)); g.closePath(); g.clip();
      vgrad(g, y0, y0 + h, 'rgba(255,255,255,0.08)', 'rgba(90,70,40,0.16)', x0, w);
      for (let y = y0 + 190; y < y0 + h; y += 66) rect(g, x0, y, w, 2, '#8FA6B8', 0.35); rect(g, x0 + 96, y0, 3, h, P.accent, 0.55); g.restore(); // pauta e margem
      text(g, (o.titulo || 'REGRAS DA POUSADA').toUpperCase(), x0 + 130, y0 + 112, 54, '#1A1819'); rect(g, x0 + 130, y0 + 132, 300, 8, '#1A1819');
      let y = y0 + 236; rs.forEach((r, i) => { const a = clamp((u - tIni[i]) / 0.35); g.font = '800 54px Geist'; g.letterSpacing = '-1.6px'; const ls = quebra(g, r.split(' '), w - 230), hh = ls.length * 68 + 30;
        if (a > 0) { g.save(); g.globalAlpha = k * a; g.translate((1 - out(a)) * 70, 0); g.translate(x0 + 130, y); g.rotate((rnd(i + 31) - 0.5) * 0.03); g.translate(-(x0 + 130), -y);
          const atual = u >= tIni[i] && (i === rs.length - 1 || u < tIni[i + 1]); if (atual) rect(g, x0 + 104, y - 56, w - 104, hh, P.accent, 0.12);
          const vm = o.ultimaVermelha && i === rs.length - 1; text(g, o.semNumeros ? '' : `${i + 1}.`, x0 + 130, y, 58, P.accent); ls.forEach((ln, j) => text(g, ln.join(' '), x0 + (o.semNumeros ? 130 : 200), y + j * 68, 54, vm ? P.accent : '#1A1819', { w: vm ? 900 : 800 })); g.restore(); }
        y += hh; });
      if (o.costura) { g.save(); g.translate(x0 + 18, y0 + h - 150); g.rotate(-0.05); poly(g, [[-30, -70], [46, -62], [40, -34], [52, -6], [44, 30], [-30, 40]], '#D9D2BE'); for (let k = 0; k < 6; k++) rect(g, -4, -90 + k * 34, 6, 18, '#3A2D27', 0.8); g.restore(); } // pedaço de papel preso na costura
      g.restore();
    },
    relogio(g, o, u) { // relógio de parede grande; de/ate "HH:MM:SS" em o.dura s, depois pisca em vermelho
      const k = back(clamp(u / 0.45)), sec = s => { const [a, b, c] = s.split(':').map(Number); return a * 3600 + b * 60 + (c || 0); }, s0 = sec(o.de || '23:59:52'); let s1 = sec(o.ate || '00:00:00'); if (s1 < s0) s1 += 86400;
      const d = o.dura || 2.4, seg = s0 + Math.floor((s1 - s0) * clamp(u / d) + 1e-6), fl = u > d ? Math.max(0, Math.cos((u - d) * 9)) * Math.exp(-(u - d) * 0.5) : 0;
      g.save(); g.translate(o.x * W, o.y * H); g.scale((o.escala || 1) * k, (o.escala || 1) * k); relogioFace(g, 0, 0, 140, seg, fl); if (o.mao != null && u >= o.mao) { const km = out(clamp((u - o.mao) / 0.35)); g.save(); g.translate((1 - km) * 90, (1 - km) * 160); maoNoPonteiro(g, 140, seg); g.restore(); } g.restore(); // o.mao = segundos em que a mão da Bia entra e segura o ponteiro dos minutos (ep07)
    },
    painel(g, o, u) { // painel das campainhas; a luz do quarto o.acesa (padrão 7) pisca a partir de o.pisca s
      const k = out(clamp(u / 0.4)), p = u - (o.pisca ?? 1e9), on = p >= 0 ? (Math.sin(p * 12) > -0.2 ? 1 : 0.2) : 0;
      g.save(); g.globalAlpha = k; g.translate(o.x * W, o.y * H + (1 - k) * 60); g.scale(o.escala || 1, o.escala || 1); painelDesenho(g, 0, 0, 760, on, o.acesa || 7); g.restore();
    },
    interfone(g, o, u) { // interfone de parede com o LED vermelho
      const k = back(clamp(u / 0.4)); g.save(); g.translate(o.x * W, o.y * H); g.scale((o.escala || 1) * k, (o.escala || 1) * k);
      rect(g, -70, -110, 150, 236, '#000', 0.4); rect(g, -80, -120, 150, 236, '#3A363D'); rect(g, -66, -104, 122, 204, '#2A272D');
      for (let i = 0; i < 6; i++) rect(g, -46, -80 + i * 22, 82, 8, '#151417'); rect(g, -32, 60, 54, 26, '#4A4650');
      const led = Math.sin(u * 10) > 0 ? 1 : 0.3; circ(g, -5, -94, 7, P.accent, led); glow(g, -5, -94, 60, P.accent, 0.4 * led); g.restore();
    },
    chamada(g, o, u) { // ep07: celular de frente, tela acesa com o nome de quem liga (o.nome), vibra
      const k = back(clamp(u / 0.45)), vib = Math.sin(u * 55) * 0.018 * (Math.sin(u * 6) > -0.3 ? 1 : 0.15);
      g.save(); g.translate(o.x * W, (o.y ?? 0.45) * H); g.rotate((o.inclina ?? -0.05) + vib); g.scale((o.escala || 1) * k, (o.escala || 1) * k);
      rrect(g, -200, -360, 400, 740, 60, '#000', 0.4); g.translate(-8, -8);
      rrect(g, -200, -360, 400, 740, 60, '#2A272D'); rrect(g, -182, -342, 364, 704, 46, '#0B0B0E'); glow(g, 0, -20, 520, '#DCE3FF', 0.1 + 0.05 * Math.sin(u * 8));
      text(g, 'CHAMADA RECEBIDA', 0, -250, 24, '#9AA3B5', { align: 'center', mono: 1, w: 700 });
      circ(g, 0, -140, 70, '#3A363D'); circ(g, 0, -158, 24, '#8A8691'); rrect(g, -42, -122, 84, 46, 24, '#8A8691');
      text(g, o.nome || 'Dona Dalva', 0, -10, 52, P.paper, { align: 'center', w: 800 }); text(g, 'chamando...', 0, 40, 26, '#9AA3B5', { align: 'center', mono: 1, w: 700 });
      if (o.rodape) text(g, o.rodape, 0, -400, 34, P.accent, { align: 'center', mono: 1, w: 700 });
      circ(g, -90, 230, 52, '#D8402F'); circ(g, 90, 230, 52, '#3FAE5A'); g.restore();
    },
    fone_toque(g, o, u) { // ep04: ícone de telefone tocando (círculo vermelho, fone e ondas), vibra
      const k = back(clamp(u / 0.35)), vib = Math.sin(u * 50) * 0.05 * (Math.sin(u * 7) > 0 ? 1 : 0.2);
      g.save(); g.translate(o.x * W, (o.y ?? 0.4) * H); g.rotate(vib); g.scale((o.escala || 1) * k, (o.escala || 1) * k);
      circ(g, 0, 0, 130, '#000', 0.35); circ(g, -6, -6, 130, P.accent); g.strokeStyle = '#FFF'; g.lineCap = 'round'; g.lineWidth = 34; g.beginPath(); g.arc(0, 8, 56, Math.PI * 1.15, Math.PI * 1.85); g.stroke();
      rrect(g, -78, 8, 40, 56, 12, '#FFF'); rrect(g, 38, 8, 40, 56, 12, '#FFF');
      for (let i = 0; i < 3; i++) { const a = ((u * 1.6 + i / 3) % 1); g.globalAlpha = 1 - a; g.lineWidth = 8; g.strokeStyle = P.accent; g.beginPath(); g.arc(0, 0, 150 + a * 90, 0, Math.PI * 2); g.stroke(); } g.restore();
    },
    balao(g, o, u) { // balão de fala/sussurro (cantos retos), com rabicho para (px,py)
      const k = back(clamp(u / 0.35)), s = (o.texto || '').toUpperCase(), sz = o.tam || 120; g.save(); g.font = `700 ${sz}px Oswald, Impact, sans-serif`; g.letterSpacing = '4px';
      const tw = g.measureText(s).width + 90, th = sz * 1.35, cx = o.x * W, cy = o.y * H, j = (rnd(Math.floor(u * 20)) - 0.5) * 6;
      g.translate(cx + j, cy); g.scale(k, k); const c = o.cor === 'claro' ? P.paper : P.accent;
      if (o.px != null) poly(g, [[-30, th / 2 - 4], [30, th / 2 - 4], [o.px * W - cx, o.py * H - cy]], c);
      rect(g, -tw / 2 + 12, -th / 2 + 16, tw, th, '#000', 0.35); rect(g, -tw / 2, -th / 2, tw, th, c);
      g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillStyle = o.cor === 'claro' ? P.deep : '#FFF'; g.fillText(s, 0, 6); g.restore();
    },
  };

  // ───────────── LEGENDAS E FAIXAS ─────────────
  function quebra(g, palavras, maxW) { const ls = [[]]; let w = 0; for (const p of palavras) { const pw = g.measureText(p + ' ').width; if (w + pw > maxW && ls.at(-1).length) { ls.push([]); w = 0; } ls.at(-1).push(p); w += pw; } return ls; }
  function grupos(tx) { // 2 a 3 palavras por vez (no máximo ~16 letras), cada grupo com seu peso de tempo
    const ps = tx.split(/\s+/).filter(Boolean), gs = []; let cur = [];
    for (const p of ps) { if (cur.length && (cur.length >= 3 || (cur.join(' ') + ' ' + p).length > 16)) { const fraca = cur.length > 1 && cur.at(-1).length <= 2 && !/[.,!?…:]$/.test(cur.at(-1)) ? [cur.pop()] : []; gs.push(cur); cur = fraca; } cur.push(p); if (/[.!?…]$/.test(p)) { gs.push(cur); cur = []; } } // não termina grupo em artigo/preposição solta
    if (cur.length) gs.push(cur); return gs.map(w => ({ w, peso: w.join(' ').length + 3 }));
  }
  function inicioGrupo(c, palavra, ini, dur) { // segundo da cena em que a legenda mostra o grupo que começa com "palavra" (sincroniza objetos com a fala)
    const gs = c._gs || (c._gs = grupos(c.narracao || '')), tot = gs.reduce((a, x) => a + x.peso, 0) || 1, n = s => s.toLowerCase().replace(/[.,!?…:]/g, ''); let acc = 0;
    const eq = /[.,!?…:]$/.test(palavra) ? w => w.toLowerCase() === palavra.toLowerCase() : w => n(w) === n(palavra); // com pontuação = palavra exata
    for (const gr of gs) { if (gr.w.some(eq)) return ini + acc / tot * dur; acc += gr.peso; } return ini;
  }
  function legendaPalavras(g, c, u, ini, dur, destaque) { // estilo Filme FLIX: branca, condensada bold, contorno e sombra, centro da tela
    const gs = c._gs || (c._gs = grupos(c.narracao)), tot = gs.reduce((a, x) => a + x.peso, 0); let acc = 0, gi = gs.length - 1, t0 = 0; const k = clamp((u - ini) / dur) * tot;
    for (let i = 0; i < gs.length; i++) { if (k < acc + gs[i].peso) { gi = i; t0 = (k - acc) / gs[i].peso * dur * (gs[i].peso / tot); break; } acc += gs[i].peso; }
    if (u < ini - 0.05) return; const gr = gs[gi], pop = back(clamp(((k - acc) / gs[gi].peso * dur * gs[gi].peso / tot + 0.0001) / 0.12)), s = gr.w.join(' ').toUpperCase();
    const base = c.legendaTam || 175, size = s.length > 13 ? Math.round(base * 0.86) : base; g.save(); g.font = `700 ${size}px Oswald, Impact, "Arial Narrow", sans-serif`; g.letterSpacing = '2px'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.lineJoin = 'round';
    const ls = quebra(g, s.split(' '), 900), lh = size * 1.02, y0 = (c.legendaY || 1030) - (ls.length - 1) * lh / 2; g.translate(W / 2, y0); // legendaY/legendaTam por cena (ex.: cartão grande ocupando o centro)
 const sc = 0.82 + 0.18 * Math.min(1.1, pop); g.scale(sc, sc);
    ls.forEach((ln, i) => { const txt = ln.join(' '), y = i * lh, dest = ln.some(w => destaque.some(d => w.toLowerCase().replace(/[.,!?…]/g, '') === d.toLowerCase()));
      g.shadowColor = 'rgba(0,0,0,0.55)'; g.shadowBlur = 0; g.shadowOffsetY = 10; g.strokeStyle = '#111'; g.lineWidth = size * 0.17; g.strokeText(txt, 0, y);
      g.shadowColor = 'transparent'; g.fillStyle = dest ? '#FFD23F' : '#FFF'; g.fillText(txt, 0, y); });
    g.restore();
  }
  function legendaFrase(g, tx, k, destaque) { // opção "legenda":"frase": frase inteira embaixo, palavra a palavra, acima da faixa coberta pela interface (fim em y=1470)
    const size = tx.length > 110 ? 56 : tx.length > 70 ? 62 : 70, lh = size * 1.18; g.font = `800 ${size}px Geist`; g.letterSpacing = `${-0.03 * size}px`; g.textBaseline = 'alphabetic';
    const pals = tx.split(' '), ls = quebra(g, pals, W - 200), n = pals.length, y0 = 1470 - (ls.length - 1) * lh;
    rect(g, 50, y0 - size - 10, W - 100, ls.length * lh + 40, P.deep, 0.62); let idx = 0, y = y0; g.lineJoin = 'round';
    for (const ln of ls) { const tw = ln.reduce((a, w) => a + g.measureText(w + ' ').width, 0); let x = (W - tw) / 2;
      for (const p of ln) { const a = clamp((k * n * 1.1 - idx) * 3), dest = destaque.some(d => p.toLowerCase().replace(/[.,!?…]/g, '') === d.toLowerCase());
        g.globalAlpha = 0.25 + 0.75 * a; g.strokeStyle = P.deep; g.lineWidth = size * 0.12; g.strokeText(p, x, y); g.fillStyle = a > 0.5 && dest ? P.accent : P.paper; g.fillText(p, x, y); x += g.measureText(p + ' ').width; idx++; }
      y += lh; }
    g.globalAlpha = 1;
  }
  function textoTela(g, tx, u, y0 = 470, mono = false) { // texto de tela grande (letreiro/mensagem), em caixa alta, na parte de cima; a caixa se ajusta ao texto
    const a = out(clamp((u - 0.25) / 0.25)); if (a <= 0) return; const s = tx.toUpperCase(), size = s.length > 28 ? 70 : 92; g.font = mono ? `700 ${size}px "Geist Mono"` : `900 ${size}px Geist`; g.letterSpacing = mono ? '0px' : `${-0.03 * size}px`;
    const ls = quebra(g, s.split(' '), 820), lh = size * 1.1, bh = ls.length * lh + 56, bw = Math.min(900, Math.max(...ls.map(l => g.measureText(l.join(' ')).width)) + 130), bx = (W - bw) / 2; g.save(); g.globalAlpha = a; g.translate(W / 2, y0 + bh / 2); g.scale(0.92 + 0.08 * a, 0.92 + 0.08 * a); g.translate(-W / 2, -(y0 + bh / 2));
    rect(g, bx, y0, bw, bh, P.deep, 0.85); rect(g, bx, y0, 14, bh, P.accent);
    ls.forEach((ln, i) => text(g, ln.join(' '), W / 2 + 7, y0 + 28 + size * 0.9 + i * lh, size, P.paper, { align: 'center', mono, w: mono ? 700 : 900 })); g.restore(); // mono = números (0 diferente de O)
  }
  function faixaTitulo(g, ep, tt) { // "EPISÓDIO N · NOME" no começo
    const D = 2.6; if (tt > D) return; const a = tt < 0.3 ? out(tt / 0.3) : tt > D - 0.35 ? out((D - tt) / 0.35) : 1;
    g.save(); g.translate((1 - a) * -W * 0.4, 0); g.globalAlpha = Math.min(1, a * 1.5); rect(g, 0, 290, W, 150, P.deep, 0.92); rect(g, 0, 290, 20, 150, P.accent);
    text(g, `EPISÓDIO ${ep.numero} ·`, 60, 345, 34, P.accent, { mono: 1, w: 700 }); text(g, ep.nome.toUpperCase(), 60, 412, 64, P.paper); g.restore();
  }
  function faixaFinal(g, ep, tt, DUR) { // "PARTE N+1 VEM AÍ" nos últimos segundos
    const D = Math.min(2.6, DUR * 0.5), u = tt - (DUR - D); if (u < 0) return; const a = out(clamp(u / 0.4));
    rect(g, 0, 0, W, H, P.deep, 0.55 * a); g.save(); g.globalAlpha = a; g.translate(0, (1 - a) * 40); rect(g, 0, 800, W, 220, P.deep, 0.95); rect(g, 0, 800, W, 8, P.accent); rect(g, 0, 1012, W, 8, P.accent);
    text(g, `PARTE ${ep.numero + 1}`, W / 2, 930, 118, P.paper, { align: 'center' }); text(g, 'VEM AÍ', W / 2, 1000, 56, P.accent, { align: 'center' });
    if (ep.segue) { const s = (ep.segue === true ? `Segue pra ver a parte ${ep.numero + 1}` : ep.segue).toUpperCase(); rect(g, 0, 1060, W, 100, P.deep, 0.9); text(g, s, W / 2, 1126, 46, P.paper, { align: 'center', w: 800 }); }
    g.restore();
  }

  // ───────────── PNGs OPCIONAIS (assets/cenarios/NOME.png, assets/personagens/NOME_POSE.png) ─────────────
  const imgCache = {};
  function carrega(url) { return imgCache[url] || (imgCache[url] = new Promise(res => { const im = new Image(); im.onload = () => res(im); im.onerror = () => res(null); im.src = url; })); }

  // ───────────── EXECUÇÃO ─────────────
  async function run(opts) { // opts: { ep (json), id ('00'), voz (url base dos mp3 por cena), assets (url base dos PNGs) }
    const q = new URLSearchParams(location.search), ep = opts.ep, cenas = ep.cenas, render = q.has('render'), comVoz = (render || q.has('mix')) ? !q.has('semvoz') : q.has('voz');
    ep.numero = ep.numero ?? +opts.id; if (ep.proxima === undefined) ep.proxima = true;
    cenas.forEach((c, i) => { const png = /\.png$/i.test(c.cenario); if (!png && !CENARIOS[c.cenario]) throw new Error(`cena ${i + 1}: cenário "${c.cenario}" não existe (${Object.keys(CENARIOS).join(', ')}, ou um arquivo .png)`);
      (c.personagens || []).forEach(p => { if (!POSES[p.pose || 'neutro']) throw new Error(`cena ${i + 1}: pose "${p.pose}" não existe (${Object.keys(POSES).join(', ')})`); });
      (c.objetos || []).forEach(ob => { if (!OBJETOS[ob.tipo]) throw new Error(`cena ${i + 1}: objeto "${ob.tipo}" não existe (${Object.keys(OBJETOS).join(', ')})`); }); });
    await loadBrandFonts(); await document.fonts.load('700 100px "Oswald"', 'ÁÉÍçãõ…'); // Oswald = legenda estilo Filme FLIX
    for (const c of cenas) { // PNGs opcionais: se não existir, fica o vetor
      if (/\.png$/i.test(c.cenario)) c._img = await carrega(`${opts.assets}/cenarios/${c.cenario}`);
      for (const p of c.personagens || []) { p.id = p.id || 'x'; p.pose = p.pose || 'neutro'; p.x = p.x ?? 0.5; if (p.arquivo) p._img = await carrega(`${opts.assets}/personagens/${p.arquivo}_${p.pose}.png`); }
    }
    const SR = 48000, ac = new OfflineAudioContext(2, SR, SR);
    // Falas por cena: 'narracao' (narrador) primeiro, depois 'falas' [{quem, texto}] em ordem; um mp3 por fala (cenaN_K.mp3). Cada fala vira um segmento {quem, texto, buf, ini, dur}.
    // Respiros (s): LEAD antes da 1ª fala, GAP entre falas, TAIL depois da última. Ajustáveis no episódio ("respiros": {lead, gap, tail}) e a cena pode pedir "respiro" extra no fim.
    const RS = Object.assign({ lead: 0.08, gap: 0.1, tail: 0.15 }, ep.respiros || {}), GAP = RS.gap, TAIL = RS.tail, LEAD = RS.lead;
    cenas.forEach((c, i) => { const lista = []; if (c.narracao) lista.push({ quem: 'narrador', texto: c.narracao }); (c.falas || []).forEach(f => lista.push({ quem: f.quem || 'narrador', texto: f.texto, efeito: f.efeito, arquivo: f.arquivo })); c._segs = lista; });
    await Promise.all(cenas.map(async (c, i) => Promise.all(c._segs.map(async (sg, k) => { if (!comVoz) return;
      const r = await fetch(sg.arquivo ? `${opts.voz}/${sg.arquivo}` : `${opts.voz}/cena${i + 1}_${k + 1}.mp3`); if (!r.ok) throw new Error(`voz da cena ${i + 1} fala ${k + 1} não encontrada (rode gen_voz_serie_edge.py, ou use &semvoz=1)`); sg.buf = await ac.decodeAudioData(await r.arrayBuffer());
      const d = sg.buf.getChannelData(0); if (sg.arquivo) { sg.a0 = 0; sg.len = sg.buf.duration; return; } let a = 0, b = d.length - 1; while (a < b && Math.abs(d[a]) < 0.012) a++; while (b > a && Math.abs(d[b]) < 0.012) b--; // corta o silêncio das pontas do edge-tts
      sg.a0 = Math.max(0, a / sg.buf.sampleRate - 0.03); sg.len = Math.min(sg.buf.duration, (b + 1) / sg.buf.sampleRate + 0.05) - sg.a0;
      if (sg.efeito === 'sussurro' && window.VozFx) { // sussurro: vocoder de ruído (voz_fx.js); a cauda do reverb entra na duração
        const sr = sg.buf.sampleRate, x = d.slice(Math.round(sg.a0 * sr), Math.round((sg.a0 + sg.len) * sr)), y = VozFx.sussurro(x, sr, sg.efeitoOpts || {});
        sg.buf = new AudioBuffer({ length: y.length, numberOfChannels: 1, sampleRate: sr }); sg.buf.copyToChannel(y, 0); sg.a0 = 0; sg.len = y.length / sr; } }))));
    let t0 = 0; cenas.forEach((c, i) => { c.t0 = t0; let acc = LEAD; // áudios em fila, sem sobrepor; a cena estica para caber tudo
      c._segs.forEach(sg => { sg.ini = acc; sg.dur = sg.buf ? sg.len : Math.max(0.5, (c.duracao || 4) - LEAD - TAIL) / c._segs.length; acc += sg.dur + GAP; sg.obj = { narracao: sg.texto }; });
      c.dur = Math.max(c.duracao || 4, c._segs.some(x => x.buf) ? acc - GAP + TAIL + (c.respiro || 0) : 0); t0 += c.dur; });
    const DUR = Math.ceil(t0 * FPS) / FPS, dest = ep.destaque || [], elenco = ep.elenco || {}, modoFrase = ep.legenda === 'frase';
    const cv = document.createElement('canvas'); cv.width = W; cv.height = H; const g = cv.getContext('2d');
    const idxEm = tt => { const i = cenas.findIndex(c => tt < c.t0 + c.dur); return i < 0 ? cenas.length - 1 : i; };
    function frame(tt) {
      const i = idxEm(tt), c = cenas[i], u = tt - c.t0, fr = Math.round(tt * FPS), tr = out(clamp(u / 0.3)), claro = !c._img && CENARIOS[c.cenario] && CENARIOS[c.cenario].claro, kk = clamp(u / c.dur);
      g.fillStyle = claro ? P.bege : P.deep; g.fillRect(0, 0, W, H);
      // câmera: zoom lento (Ken Burns) + pan vertical; susto = tremor no começo da cena
      const [z0, z1] = c.zoom || [1, 1.07], [p0, p1] = c.pan || [0, 0], zmin = 1 + 2 * Math.max(Math.abs(p0), Math.abs(p1)) / H, z = Math.max(lerp(z0, z1, kk), zmin), pan = lerp(p0, p1, kk);
      const susto = (c.personagens || []).some(p => p.pose === 'assustado') ? Math.exp(-u * 5) : 0, sx = (rnd(fr) - 0.5) * 40 * susto, sy2 = (rnd(fr + 7) - 0.5) * 40 * susto;
      g.save(); g.translate(W / 2 + sx + (1 - tr) * 50 * (i % 2 ? -1 : 1), H / 2 + pan + sy2); g.scale(z, z); g.translate(-W / 2, -H / 2);
            if (c.desfoque) g.filter = `blur(${c.desfoque}px)`; // fundo desfocado nos closes
      if (c.cenario === 'olho_magico' || c.cenario === 'espelho' || c.cenario === 'punho') c._elenco = elenco; if (c._img) g.drawImage(c._img, 0, 0, W, H); else CENARIOS[c.cenario](g, u, c);
      g.filter = 'none'; if (c.desfoque) rect(g, 0, 0, W, H, P.deep, 0.25);
      (c.personagens || []).forEach(p => { if (p.ate == null || u < p.ate) personagem(g, p, u - (p.entra || 0), c.dur, elenco, p._img); }); // p.entra = segundos de atraso da entrada
      const s0 = c._segs[0], cx = { u, inicio: palavra => s0 ? inicioGrupo(s0.obj, palavra, s0.ini, s0.dur) : 0 }; // gatilhos de objetos seguem a primeira fala
      (c.objetos || []).forEach(ob => { const uu = u - (ob.entra ?? 0.3); if (uu >= 0) OBJETOS[ob.tipo](g, ob, uu, cx); });
      g.restore();
      if (!claro) rect(g, 0, 0, W, H, P.deep, c.escurece ?? ep.escurece ?? 0.12); // escurece o conjunto (noite)
      if (c.textoTela) textoTela(g, c.textoTela, u - (c.textoEntra || 0), c.textoY ?? ep.textoY ?? 470, c.textoMono);
      faixaTitulo(g, ep, tt); if (ep.proxima) faixaFinal(g, ep, tt, DUR);
      let sg = null; for (const x of c._segs) if (u >= x.ini - 0.05) sg = x; // fala ativa (a anterior continua na tela até a próxima começar)
      if (sg) { Object.assign(sg.obj, { legendaY: c.legendaY ?? ep.legendaY, legendaTam: c.legendaTam ?? ep.legendaTam }); if (modoFrase) legendaFrase(g, sg.texto, clamp((u - sg.ini) / sg.dur), dest); else legendaPalavras(g, sg.obj, u, sg.ini, sg.dur, dest); } // legenda por cima das faixas
      const k = 1 - tr; if (k > 0) { rect(g, 0, 0, W, H, claro ? P.bege : P.deep, Math.pow(k, 1.5)); if (u < 0.1 && i > 0) { rect(g, 0, rnd(fr) * H, W, 6, P.accent, 0.8); rect(g, 0, rnd(fr + 3) * H, W, 3, P.paper, 0.5); } }
      grain(g, W, H, claro ? 0.04 : 0.07);
      if (c.glitch && u < c.glitch) { const ga = 1 - u / c.glitch; for (let q2 = 0; q2 < 5; q2++) { const gy = rnd(fr * 7 + q2) * H, gh = 16 + rnd(fr + q2 * 3) * 80, gdx = (rnd(fr * 3 + q2) - 0.5) * 140 * ga; g.drawImage(cv, 0, gy, W, gh, gdx, gy, W, gh); } rect(g, 0, rnd(fr + 11) * H, W, 5, P.accent, 0.7 * ga); } // glitch de recap (c.glitch = segundos)
      if (tt > DUR - 0.3) rect(g, 0, 0, W, H, '#0C0C0D', clamp((tt - (DUR - 0.3)) / 0.3));
      if (q.has('safe') && !render) { g.save(); g.fillStyle = 'rgba(255,59,31,0.18)'; g.fillRect(0, 0, W, 250); g.fillRect(0, 1480, W, H - 1480); g.fillRect(940, 900, W - 940, 580); g.restore(); }
    }
    window.MOTOR_INFO = { dur: DUR, cenas: cenas.map(c => [+c.t0.toFixed(2), +c.dur.toFixed(2)]), falas: cenas.map(c => c._segs.map(s => [+(c.t0 + s.ini).toFixed(2), +s.dur.toFixed(2)])) };
    // ───── ÁUDIO: camadas voz / trilha / efeitos, cue-sheet sintetizada (sfx.js), ducking sob a voz, limitador e medição por cena ─────
    async function mixar() {
      const len = Math.round(SR * DUR), VL = new Float32Array(len), VR = new Float32Array(len), BL = new Float32Array(len), BR = new Float32Array(len);
      // Camadas (ganho próprio): ep.camadas = { voz, trilha, efeitos, musicaWav }. trilha = cues musicais da cue-sheet (piano, caixinha, drone, pulso...); efeitos = demais cues e "efeitos" .wav por cena; musicaWav = stems/music.wav em loop (0 = desligado).
      const CAM = Object.assign({ voz: 1, trilha: 0, efeitos: 1, musicaWav: 0 }, ep.camadas || {}), VOL = { narrador: 1.0, bia: 0.82, dalva: 0.82, osmar: 0.82, sete: 0.82 };
      const ECO = { dalva: [[0.11, 0.22], [0.23, 0.12], [0.37, 0.06]] }; // reverb leve: ecos curtos que caem
      function mixa(b, off, ganho, ecos, a0 = 0, tam = b.duration, L = BL, R = BR) { const d0 = b.getChannelData(0), d1 = b.numberOfChannels > 1 ? b.getChannelData(1) : d0, r = b.sampleRate / SR, n = Math.round(tam * SR), s0 = Math.round(a0 * b.sampleRate), nn = Math.round(0.005 * SR);
        for (const [atraso, g2] of [[0, 1], ...(ecos || [])]) { const o = off + Math.round(atraso * SR);
          for (let i = 0; i < n && o + i < len; i++) { const w = Math.min(1, i / nn, (n - i) / nn), j = s0 + Math.floor(i * r); L[o + i] += (d0[j] || 0) * ganho * g2 * w; R[o + i] += (d1[j] || 0) * ganho * g2 * w; } } }
      for (const c of cenas) for (const sg of c._segs) if (sg.buf) mixa(sg.buf, Math.round((c.t0 + sg.ini) * SR), 0.95 * CAM.voz * (VOL[sg.quem] ?? 0.85), ECO[sg.quem], sg.a0, sg.len, VL, VR);
      if (CAM.musicaWav > 0) { const mus = await new OfflineAudioContext(2, SR, SR).decodeAudioData(await (await fetch('/w/stems/music.wav')).arrayBuffer()), m0 = mus.getChannelData(0), m1 = mus.getChannelData(1), ml = m0.length;
        for (let i = 0; i < len; i++) { const ti = i / SR, fade = Math.min(1, ti / 0.4, (DUR - ti) / 0.8), j = Math.floor(ti * mus.sampleRate) % ml; BL[i] += m0[j] * CAM.musicaWav * fade; BR[i] += m1[j] * CAM.musicaWav * fade; } }
      for (const c of cenas) for (const fx of c.efeitos || []) { if (!CAM.efeitos) continue; const r = await fetch(`/w/stems/serie/fx/${fx.arquivo}`); if (r.ok) mixa(await ac.decodeAudioData(await r.arrayBuffer()), Math.round((c.t0 + (fx.t || 0)) * SR), (fx.vol ?? 0.5) * CAM.efeitos); }
      // cue-sheet (ep.sons = arquivo em ep/): cada cue {cena, offset, tipo, params, fala?, gatilho?, ateCena?}; params.dur "cena" = até o fim da cena; tipo "corte" = silencia trilha e efeitos dali em diante (corte seco); tipo "silencio" (params.dur) = silencia só esse trecho
      let corte = null; const mudos = [], cuesT = [], cuesE = [], MUSICA = ['pianoBia', 'acordeBia', 'caixinha', 'drone', 'pulso', 'batimento', 'cantarolar'];
      if (ep.sons && window.Sfx) { const folha = await (await fetch(`ep/${ep.sons}`)).json();
        for (const cu of folha.cues || []) { const c = cenas[cu.cena - 1]; if (!c) continue; let t = c.t0 + (cu.offset || 0);
          if (cu.fala) t += (c._segs[cu.fala - 1] || {}).ini || 0;
          if (cu.gatilho && c._segs[0]) t += inicioGrupo(c._segs[0].obj, cu.gatilho, c._segs[0].ini, c._segs[0].dur);
          const p = Object.assign({}, cu.params || {}); const fimC = n => { const cc = cenas[n - 1] || cenas.at(-1); return cc.t0 + cc.dur; };
          if (p.dur === 'cena') p.dur = fimC(cu.cena) - t; if (cu.ateCena) p.dur = fimC(cu.ateCena) - t + (cu.passa || 0);
          if (cu.tipo === 'corte') { corte = t; mudos.push([t, Infinity]); continue; } if (cu.tipo === 'silencio') { mudos.push([t, t + (p.dur || 1)]); continue; }
          (MUSICA.includes(cu.tipo) ? cuesT : cuesE).push({ t: Math.max(0, t), tipo: cu.tipo, params: p }); }
        for (const [cues, g] of [[cuesT, CAM.trilha], [cuesE, CAM.efeitos]]) { if (!cues.length || !g) continue;
          const b = await Sfx.renderOffline(cues, DUR, { sampleRate: SR, seed: 20261025 }), b0 = b.getChannelData(0), b1 = b.getChannelData(1);
          for (let i = 0; i < len; i++) { BL[i] += b0[i] * g; BR[i] += b1[i] * g; } } }
      for (const [ta, tb] of mudos) { const s = Math.round(ta * SR), e = Math.min(len, Math.round(tb * SR)), F = Math.round(0.04 * SR); // 40 ms de rampa nas pontas (sem estalo)
        for (let i = Math.max(0, s - F); i < Math.min(len, e + F); i++) { const k = i < s ? (s - i) / F : i >= e ? (i - e) / F : 0; BL[i] *= k; BR[i] *= k; } }
      // ducking: janela de 20 ms; com voz ativa (> -42 dBFS) a cama vai a ep.duck (padrão 0,4 = -8 dB), ataque 60 ms, solta em 350 ms (segura 120 ms)
      const DK = ep.duck ?? 0.4, Wn = Math.round(0.02 * SR), nw = Math.ceil(len / Wn), ativo = new Uint8Array(nw), ka = Math.exp(-1 / (0.06 * SR)), kr = Math.exp(-1 / (0.35 * SR)), HOLD = Math.round(0.12 * SR);
      for (let w = 0; w < nw; w++) { let e = 0; const a = w * Wn, b = Math.min(len, a + Wn); for (let i = a; i < b; i++) e += VL[i] * VL[i]; ativo[w] = Math.sqrt(e / Math.max(1, b - a)) > 0.008 ? 1 : 0; }
      let gk = 1, hold = 0; for (let i = 0; i < len; i++) { if (ativo[Math.floor(i / Wn)]) hold = HOLD; else if (hold > 0) hold--; const alvo = hold > 0 ? DK : 1; gk = alvo < gk ? ka * gk + (1 - ka) * alvo : kr * gk + (1 - kr) * alvo; BL[i] *= gk; BR[i] *= gk; }
      // soma + limitador simples: se o pico passar de -1,5 dBFS, a mix inteira desce (sem saturar)
      const L = new Float32Array(len), R = new Float32Array(len); let pk = 0; for (let i = 0; i < len; i++) { L[i] = VL[i] + BL[i]; R[i] = VR[i] + BR[i]; pk = Math.max(pk, Math.abs(L[i]), Math.abs(R[i])); }
      const TETO = 0.84, ganhoMix = pk > TETO ? TETO / pk : 1; if (ganhoMix < 1) for (let i = 0; i < len; i++) { L[i] *= ganhoMix; R[i] *= ganhoMix; }
      // medição por cena: RMS da voz x RMS de trilha+efeitos (já com ducking) nos trechos com voz, e da cama nos trechos sem voz
      const db = v => v > 1e-9 ? +(20 * Math.log10(v)).toFixed(1) : -120, porCena = cenas.map((c, i) => { let ev = 0, eb = 0, n = 0, eb2 = 0, n2 = 0; const mj = [];
        const a = Math.round(c.t0 * SR), b = Math.min(len, Math.round((c.t0 + c.dur) * SR));
        for (let w = Math.floor(a / Wn); w < Math.floor(b / Wn); w++) { let v = 0, g2 = 0; for (let k = w * Wn; k < (w + 1) * Wn && k < len; k++) { v += VL[k] * VL[k]; g2 += BL[k] * BL[k]; }
          if (ativo[w]) { ev += v; eb += g2; n += Wn; if (v / Wn > 6.3e-4) mj.push(10 * Math.log10(v / Math.max(g2, 1e-12))); } else { eb2 += g2; n2 += Wn; } } // mj: só janelas com fala de fato (> -32 dBFS)
        return { cena: i + 1, vozDb: db(Math.sqrt(ev / Math.max(1, n)) * ganhoMix), camaSobVozDb: db(Math.sqrt(eb / Math.max(1, n)) * ganhoMix), margemDb: n ? +(10 * Math.log10(ev / Math.max(eb, 1e-12))).toFixed(1) : null, margemP5Db: mj.length ? +mj.sort((x, y) => x - y)[Math.floor(mj.length * 0.05)].toFixed(1) : null, janelasAbaixo6dB: mj.filter(x => x < 6).length, janelasFala: mj.length, camaSemVozDb: db(Math.sqrt(eb2 / Math.max(1, n2)) * ganhoMix) }; });
      let clip = 0, pk2 = 0; for (let i = 0; i < len; i++) { const m = Math.max(Math.abs(L[i]), Math.abs(R[i])); pk2 = Math.max(pk2, m); if (m >= 0.999) clip++; }
      return { L, R, info: { dur: +DUR.toFixed(2), picoDb: db(pk2), clip, ganhoMix: +ganhoMix.toFixed(3), duck: DK, cues: cuesT.length + cuesE.length, corte, porCena } };
    }
    if (q.has('mix')) { const m = await mixar(); window.MIX_INFO = m.info;
      if (q.has('wav')) { const b = new AudioBuffer({ length: m.L.length, numberOfChannels: 2, sampleRate: SR }); b.copyToChannel(m.L, 0); b.copyToChannel(m.R, 1); window.MIX_WAV = Sfx.toWav(b); }
      document.title = 'ready ' + DUR.toFixed(2); return; }
    if (!render) {
      const ts = (q.get('t') || '1').split(',').map(Number);
      if (ts.length === 1) { frame(ts[0]); cv.style.cssText = 'width:360px'; document.body.append(cv); }
      else { const sw = 270, sh = 480, cols = Math.min(6, ts.length), sheet = document.createElement('canvas'); sheet.width = sw * cols; sheet.height = sh * Math.ceil(ts.length / cols); const sg = sheet.getContext('2d');
        ts.forEach((tt, n) => { frame(tt); sg.drawImage(cv, (n % cols) * sw, Math.floor(n / cols) * sh, sw, sh); }); sheet.style.cssText = 'width:100%'; document.body.append(sheet); }
      document.title = 'ready ' + DUR.toFixed(2); return;
    }
    document.body.append(cv); cv.style.cssText = 'width:270px';
    const { L, R, info } = await mixar(); window.MIX_INFO = info; const len = L.length;
    const mux = new Mp4Muxer.Muxer({ target: new Mp4Muxer.ArrayBufferTarget(), video: { codec: 'avc', width: W, height: H, frameRate: FPS }, audio: { codec: 'aac', numberOfChannels: 2, sampleRate: SR }, fastStart: 'in-memory' });
    let err = null;
    const ve = new VideoEncoder({ output: (c, m) => mux.addVideoChunk(c, m), error: e => { err = e; console.error('VideoEncoder:', e.message); } }); let vcfg = null; for (const codec of ['avc1.640032', 'avc1.4d0032', 'avc1.42003e', 'avc1.420034']) { const cf = { codec, width: W, height: H, bitrate: 3.5e6, framerate: FPS, bitrateMode: 'variable', hardwareAcceleration: q.get('hw') || 'prefer-software' }; // software por padrão: o encoder de hardware travou/fechou no Edge headless (25/10) // High; sem encoder de hardware (headless) cai para Main/Baseline
      if ((await VideoEncoder.isConfigSupported(cf)).supported) { vcfg = cf; break; } } if (!vcfg) throw new Error('nenhum perfil H.264 suportado neste navegador'); ve.configure(vcfg); window.MOTOR_INFO.codec = vcfg.codec;
    const ae = new AudioEncoder({ output: (c, m) => mux.addAudioChunk(c, m), error: e => err = e }); ae.configure({ codec: 'mp4a.40.2', sampleRate: SR, numberOfChannels: 2, bitrate: 160000 });
    for (let i = 0; i < len; i += 1024) { const n = Math.min(1024, len - i), d = new Float32Array(n * 2); d.set(L.subarray(i, i + n), 0); d.set(R.subarray(i, i + n), n); const ad = new AudioData({ format: 'f32-planar', sampleRate: SR, numberOfFrames: n, numberOfChannels: 2, timestamp: Math.round(i * 1e6 / SR), data: d }); ae.encode(ad); ad.close(); }
    const total = Math.round(DUR * FPS);
    for (let fr = 0; fr < total; fr++) { frame(fr / FPS); const vf = new VideoFrame(cv, { timestamp: Math.round(fr * 1e6 / FPS) }); ve.encode(vf, { keyFrame: fr % 60 === 0 }); vf.close();
      if (err) throw err; for (let w = 0; ve.encodeQueueSize > 10; w++) { if (w > 2000) throw new Error('encoder parado (fila não esvazia)'); await new Promise(r => setTimeout(r, 5)); } if (fr % 15 === 0) document.title = `${fr}/${total}`; }
    await ve.flush(); await ae.flush(); if (err) throw err; mux.finalize();
    await fetch(`/save?dir=serie&name=ep${opts.id}.mp4`, { method: 'POST', body: mux.target.buffer }); // grava em Semanal/serie/epXX.mp4
    document.title = 'ready ' + DUR.toFixed(2);
  }
  return { run, CENARIOS, POSES, OBJETOS, W, H, FPS };
})();
