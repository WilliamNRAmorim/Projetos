// Saga "Porto Sereno", Dia 7 (versão Opus, eps o25 a o28). Só ACRESCENTA ao Motor (cenários, objetos, sons e o filtro de gravador).
// Carregado apenas por saga_o.html. Nada de violência aparece: os Ocos são silhuetas sem rosto, curvadas e de costas.
(() => {
  const { CENARIOS, OBJETOS, W, H, GY } = Motor, { rect, poly, circ, line, rrect, text, glow, vgrad, rgba, vinheta, rnd, lerp, clamp, out } = Motor.H_;
  const VERDE = '#9BC43A', VELA = '#7FB8FF', GIZ = '#F4F1E6';
  const anim = (v, t, def = 0) => { // número fixo, ou [de, ate, em, dura] animado no tempo da cena
    if (v == null) return def; if (!Array.isArray(v)) return v; const [a, b, em = 0, d = 1] = v; return lerp(a, b, out(clamp((t - em) / d)));
  };
  const lin = (v, t, def = 0) => { if (v == null) return def; if (!Array.isArray(v)) return v; const [a, b, em = 0, d = 1] = v; return lerp(a, b, clamp((t - em) / d)); };

  // ───────── o círculo de giz no chão (elipse em perspectiva) ─────────
  const CX = 540, CY = 1300, RX = 330, RY = 86;
  function arcoGiz(g, k, metade, t, brilho = 1) { // metade: 'tras' (y < CY), 'frente' (y > CY) ou 'tudo'; k = 0..1 (quanto do traço já foi feito)
    if (k <= 0) return; const a0 = -Math.PI / 2, a1 = a0 + Math.PI * 2 * clamp(k), passo = 0.02;
    g.save(); g.lineCap = 'round';
    for (const [lw, al, cor] of [[34, 0.10 * brilho, VERDE], [16, 0.35 * brilho, GIZ], [7, 0.95, GIZ]]) {
      g.strokeStyle = rgba(cor, al); g.lineWidth = lw; g.beginPath(); let on = false;
      for (let a = a0; a <= a1 + 1e-6; a += passo) { const s = Math.sin(a), y = CY + s * RY, x = CX + Math.cos(a) * RX + (rnd(Math.floor(a * 40)) - 0.5) * 3;
        const ok = metade === 'tudo' || (metade === 'tras' ? s <= 0.02 : s >= -0.02); if (ok) { on ? g.lineTo(x, y) : g.moveTo(x, y); on = true; } else on = false; }
      g.stroke(); }
    if (k < 1) { const a = a1, x = CX + Math.cos(a) * RX, y = CY + Math.sin(a) * RY; const vis = metade === 'tudo' || (metade === 'tras' ? Math.sin(a) <= 0 : Math.sin(a) > 0); if (vis) { glow(g, x, y, 60, GIZ, 0.5 + 0.2 * Math.sin(t * 20)); circ(g, x, y, 7, '#FFFFFF'); } } // a ponta do giz
    g.restore();
  }
  function simbolos(g, k, t, brilho = 1) { // traços estranhos dentro do círculo (aparecem com o traço)
    const a = clamp((k - 0.15) / 0.6); if (a <= 0) return; g.save(); g.globalAlpha = a * 0.85; g.strokeStyle = GIZ; g.lineWidth = 6; g.lineCap = 'round';
    const tr = [[-200, -20, -110, 40], [-110, 40, -40, -30], [60, -40, 150, 30], [150, 30, 220, -10], [-30, 50, 40, 60], [-170, 10, -150, 55], [110, -10, 120, 52]];
    tr.forEach(([x1, y1, x2, y2], i) => { if (i / tr.length < a) { g.beginPath(); g.moveTo(CX + x1, CY + y1 * 0.9); g.lineTo(CX + x2, CY + y2 * 0.9); g.stroke(); } });
    g.globalAlpha = a * 0.25 * brilho; glow(g, CX, CY, 420, VERDE, 0.25 * brilho); g.restore();
  }

  // ───────── os Ocos: silhuetas sem rosto, curvadas, de costas ─────────
  function oco(g, x, yb, s, t, seed, alfa, flip = 1, cor = '#020604') { // de costas, corcunda, cabeça pendurada à frente abaixo do ombro, braços até os joelhos
    if (alfa <= 0.01) return; const bal = Math.sin(t * 1.3 + seed) * 5, br = Math.sin(t * 0.9 + seed * 2) * 8; g.save(); g.globalAlpha = alfa; g.translate(x, yb); g.scale(s * flip, s);
    const corpo = () => { g.beginPath();
      g.moveTo(-48, -250); g.quadraticCurveTo(-92, -400, -10, -488 + bal); g.quadraticCurveTo(60, -520 + bal, 96, -440 + bal); // costas curvas até o ombro
      g.quadraticCurveTo(70, -330, 40, -250); g.lineTo(34, -6); g.lineTo(14, -6); g.lineTo(4, -230); g.lineTo(-14, -230); g.lineTo(-30, -6); g.lineTo(-52, -6); g.closePath(); // peito e pernas finas
      g.moveTo(132, -418 + bal); g.ellipse(104, -418 + bal, 28, 36, 0.5, 0, Math.PI * 2); }; // cabeça baixa, sem rosto
    g.fillStyle = cor; corpo(); g.fill();
    g.lineCap = 'round'; g.strokeStyle = cor; g.lineWidth = 22; g.beginPath(); g.moveTo(78, -452 + bal); g.lineTo(98, -430 + bal); g.stroke(); // pescoço curto, dobrado
    g.lineWidth = 12; g.beginPath(); g.moveTo(76, -440 + bal); g.quadraticCurveTo(122, -300, 98 + br * 0.3, -130); g.stroke(); g.beginPath(); g.moveTo(-6, -470 + bal); g.quadraticCurveTo(-40, -300, -22 - br * 0.3, -140); g.stroke(); // braços compridos
    g.lineWidth = 5; for (const [hx, hy] of [[98 + br * 0.3, -130], [-22 - br * 0.3, -140]]) for (let k = -1; k <= 1; k++) { g.beginPath(); g.moveTo(hx, hy); g.lineTo(hx + k * 9, hy + 34); g.stroke(); } // dedos
    g.strokeStyle = rgba(VERDE, 0.42); g.lineWidth = 4; corpo(); g.stroke(); // contorno de luz verde
    g.restore();
  }
  function silhuetaMaos(g, x, yb, s, alfa, seed, t) { // os esquecidos: silhuetas pálidas, de frente, de mãos dadas (sem rosto)
    if (alfa <= 0.01) return; const r = Math.sin(t * 0.9 + seed) * 3; g.save(); g.globalAlpha = alfa; g.translate(x, yb); g.scale(s, s); const cor = '#8FA8A0';
    g.fillStyle = cor; g.beginPath(); g.ellipse(0, -330 + r, 40, 48, 0, 0, Math.PI * 2); g.fill(); g.beginPath(); g.moveTo(-60, -270 + r); g.lineTo(60, -270 + r); g.lineTo(52, -90); g.lineTo(-52, -90); g.closePath(); g.fill();
    rect(g, -44, -96, 34, 96, cor); rect(g, 10, -96, 34, 96, cor); line(g, -56, -250 + r, -130, -150, cor, 22); line(g, 56, -250 + r, 130, -150, cor, 22);
    g.restore();
  }

  // ───────── POÇO DA MARÉ (fundo do poço: paredes de pedra em cilindro) ─────────
  CENARIOS.poco_mare = (g, t, c = {}) => {
    vgrad(g, 0, H, '#0A1A16', '#020605'); glow(g, 540, -120, 900, '#9FB8C8', c.fechado ? 0.04 : 0.16); // luar fraco lá de cima (some com a boca fechada)
    if (c.velasAlto) glow(g, 540, -60, 760, VELA, 0.22 + 0.03 * Math.sin(t * 7));
    for (let i = 0; i < 17; i++) { const y = 40 + i * 74, ry = 30 + i * 3.2, sh = (i % 2) * 60; g.strokeStyle = 'rgba(0,0,0,0.55)'; g.lineWidth = 5; g.beginPath(); g.ellipse(540, y, 760, ry, 0, 0, Math.PI); g.stroke(); // fiadas de pedra (o fundo curvo)
      for (let k = -6; k <= 6; k++) { const ang = (k * 0.24 + sh / 400), x = 540 + Math.sin(ang) * 760; if (Math.abs(ang) < 1.45) line(g, x, y + Math.cos(ang) * ry, x, y + 74 + Math.cos(ang) * ry, 'rgba(0,0,0,0.45)', 4); }
      rect(g, 0, y + 6, W, 3, 'rgba(155,196,58,0.03)'); }
    for (let i = 0; i < 24; i++) { const x = rnd(i * 3) * W, y = 120 + rnd(i * 5) * 1000; rrect(g, x, y, 18 + rnd(i) * 40, 60 + rnd(i + 2) * 120, 10, '#1E3A22', 0.35); } // musgo escorrendo
    for (const sx of [0, W]) { const gr = g.createLinearGradient(sx, 0, sx ? sx - 360 : 360, 0); gr.addColorStop(0, 'rgba(0,0,0,0.85)'); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr; g.fillRect(sx ? sx - 360 : 0, 0, 360, H); } // curvatura escura nas laterais
    // chão (areia molhada) em elipse
    g.fillStyle = '#121C17'; g.beginPath(); g.ellipse(540, 1330, 760, 230, 0, 0, Math.PI * 2); g.fill(); rect(g, 0, 1330, W, H - 1330, '#0C1410');
    if (c.cal) { const k = anim(c.cal, t, 1); g.save(); g.globalAlpha = 0.7 * k; g.strokeStyle = '#DCDCD0'; g.lineWidth = 30; g.setLineDash([60, 18, 30, 12]); g.beginPath(); g.ellipse(540, 1300, 470 * (0.6 + 0.4 * k), 125 * (0.6 + 0.4 * k), 0, 0, Math.PI * 2); g.stroke(); g.restore(); } // círculo de cal
    if (c.buracos) for (const [x, y] of [[300, 1360], [760, 1390], [560, 1440]]) { g.fillStyle = '#060A08'; g.beginPath(); g.ellipse(x, y, 90, 26, 0, 0, Math.PI * 2); g.fill(); } // areia cavada
    const gk = anim(c.giz, t, 0), bri = c.fechou ? 1 + 1.5 * Math.exp(-(t - (c.fechou || 0)) * 0.6) * (t >= c.fechou ? 1 : 0) : 1;
    arcoGiz(g, gk, 'tras', t, bri); simbolos(g, gk, t, bri);
    // os esquecidos de mãos dadas (fundo)
    if (c.maos) { const a = clamp((t - (c.maosEm || 0)) / 2.2); const n = 14; for (let i = 0; i < n; i++) { const f = i / (n - 1), ang = Math.PI * (0.08 + 0.84 * f), x = 540 - Math.cos(ang) * 470, yb = 1150 - Math.sin(ang) * 60, s = 0.62 - Math.sin(ang) * 0.12; silhuetaMaos(g, x, yb, s, a * clamp((a * n - i * 0.5) / 2) * 0.75 * (c.maosSome != null ? 1 - clamp((t - c.maosSome) / 1.5) : 1), i, t); }
      if (a > 0.3) { g.save(); g.globalAlpha = 0.55 * a; g.strokeStyle = '#8FA8A0'; g.lineWidth = 12; for (let i = 0; i < n - 1; i++) { const f0 = i / (n - 1), f1 = (i + 1) / (n - 1), a0 = Math.PI * (0.08 + 0.84 * f0), a1 = Math.PI * (0.08 + 0.84 * f1); const s0 = 0.62 - Math.sin(a0) * 0.12; g.beginPath(); g.moveTo(540 - Math.cos(a0) * 470 + 120 * s0, 1150 - Math.sin(a0) * 60 - 150 * s0); g.lineTo(540 - Math.cos(a1) * 470 - 120 * s0, 1150 - Math.sin(a1) * 60 - 150 * s0); g.stroke(); } g.restore(); } }
    // os Ocos
    if (c.ocos) { const n = c.ocos, em = c.ocosEm || 0, perto = anim(c.ocosPerto, t, 0), po = c.ocosPo;
      for (let i = 0; i < n; i++) { const lado = i % 2 ? 1 : -1, ord = Math.floor(i / 2), base = [[150, 1180, 1.05], [930, 1180, 1.05], [320, 1120, 0.84], [760, 1120, 0.84], [40, 1250, 1.25], [1040, 1250, 1.25], [450, 1090, 0.7], [630, 1090, 0.7]][i % 8];
        const ai = clamp((t - em - ord * 0.45) / 1.0); let x = lerp(base[0], 540 + (base[0] - 540) * 0.55, perto), yb = base[1], s = base[2] * (0.85 + 0.15 * out(ai)) * (1 + perto * 0.12); x += (1 - out(ai)) * lado * 120; // saem de dentro da parede
        let al = ai, sy = 1; if (po != null && t >= po) { const kp = clamp((t - po - ord * 0.12) / 1.1); al *= 1 - kp; sy = 1 - kp * 0.6; for (let p = 0; p < 26; p++) { const px = x + (rnd(i * 50 + p) - 0.5) * 220 * s, py = yb - rnd(i * 50 + p + 9) * 420 * s * (1 - kp) + kp * kp * 200 * rnd(p + 3); circ(g, px, py, 3 + rnd(p + i) * 6, '#1A2A20', clamp(kp * 3) * (1 - kp)); } }
        g.save(); g.translate(x, yb); g.scale(1, sy); g.translate(-x, -yb); oco(g, x, yb, s, t, i, al, lado < 0 ? 1 : -1); g.restore(); } }
    if (c.radio) { const r = c.radio, x = r.x * W, y = r.y || 1230, cai = r.caido ? 1 : 0; g.save(); g.translate(x, y); g.rotate(cai * 1.35); rrect(g, -90, -110, 180, 110, 14, '#2A2A26'); circ(g, -40, -55, 34, '#121210'); for (let k = 0; k < 4; k++) rect(g, 14, -90 + k * 18, 60, 6, '#4A4A42'); line(g, 60, -110, 120, -260, '#3A3A34', 6); circ(g, 50, -22, 7, r.on ? VERDE : '#3A0A0A'); g.restore();
      if (r.on && !cai) for (let k = 0; k < 4; k++) { const ph = ((t * 1.6 + k / 4) % 1); g.save(); g.globalAlpha = (1 - ph) * 0.6; g.strokeStyle = VERDE; g.lineWidth = 8; g.beginPath(); g.arc(x, y - 60, 80 + ph * 520, Math.PI * 1.05, Math.PI * 1.95); g.stroke(); g.restore(); } }
    if (c.feixe) { const a = c.feixe === true ? 1 : c.feixe; poly(g, [[200, 0], [380, 0], [760, 1300], [300, 1320]], '#F2EBC8', 0.07 * a); glow(g, 520, 1290, 260, '#F2EBC8', 0.18 * a); }
    if (c.vapor) { const v = c.vapor, k = clamp((t - v.em) / (v.dura || 3)); if (k > 0) for (let p = 0; p < 70; p++) { const px = v.x * W + (rnd(p) - 0.5) * 240 + Math.sin(t * 1.5 + p) * 30 * k, py = 1240 - rnd(p + 2) * 650 - k * (200 + rnd(p + 5) * 500); circ(g, px, py, 4 + rnd(p + 7) * 9, '#E8F0E0', clamp(k * 4) * (1 - k) * 0.7); } }
    vinheta(g, 0.6);
    if (c.clarao != null && t >= c.clarao) { const k = t - c.clarao; rect(g, 0, 0, W, H, '#FFFFFF', Math.pow(clamp(1 - k / 2.4), 1.6) * 0.96); glow(g, CX, CY, 1300, '#FFFFFF', 0.4 * clamp(1 - k / 4)); }
    if (c.luzBranca) glow(g, CX, CY - 200, 1100, '#F4FFF0', c.luzBranca);
  };
  CENARIOS.poco_mare.giz = true;

  // ───────── DEGRAUS (de pedra, descendo para dentro da terra; a água sobe) ─────────
  CENARIOS.degraus_poco = (g, t, c = {}) => {
    vgrad(g, 0, H, '#08130F', '#010302'); const n = 10, nivel = lin(c.agua, t, 99); // nivel = índice do degrau até onde a água chegou (de baixo, o mais fundo = n-1)
    if (c.luzFundo) glow(g, 600, 470, 520, VELA, (0.12 + 0.05 * Math.sin(t * 5)) * c.luzFundo);
    for (let i = n - 1; i >= 0; i--) { const k = i / (n - 1), y = lerp(1750, 470, Math.pow(k, 0.8)), w = lerp(980, 210, k), x = lerp(540, 610, k) + Math.sin(k * 3) * 40, h = lerp(150, 34, k);
      poly(g, [[x - w / 2, y], [x + w / 2, y], [x + w / 2 * 0.94, y - h], [x - w / 2 * 0.94, y - h]], lerp(0, 1, 1) ? (i === 4 && c.quinto ? '#2E4A30' : '#22302A') : '#22302A'); // pisada
      rect(g, x - w / 2, y, w, h * 0.55, '#121A16'); rect(g, x - w / 2, y, w, 4, 'rgba(255,255,255,0.05)'); // espelho do degrau
      if (i === 4 && c.quinto) text(g, '5', x - w / 2 + 30, y - h * 0.25, 34 * (1 - k * 0.5) + 10, rgba(VERDE, 0.7), { w: 800 });
      if (i >= nivel) { poly(g, [[x - w / 2 - 20, y + h * 0.55], [x + w / 2 + 20, y + h * 0.55], [x + w / 2 * 0.94 + 20, y - h - 6], [x - w / 2 * 0.94 - 20, y - h - 6]], '#0E3A38', 0.86); for (let r = 0; r < 3; r++) line(g, x - w * 0.4 + rnd(i * 7 + r) * w * 0.5, y - h * 0.5 + r * 6, x - w * 0.2 + rnd(i * 7 + r) * w * 0.5 + Math.sin(t * 3 + r + i) * 20, y - h * 0.5 + r * 6, '#5AA8A0', 3, 0.35); } }
    const fr = nivel - Math.floor(nivel); if (nivel < n && nivel >= 0) { const i = Math.floor(nivel), k = i / (n - 1), y = lerp(1750, 470, Math.pow(k, 0.8)); glow(g, 560, y - 40, 300, '#5AA8A0', 0.12 + 0.1 * fr); }
    for (const sx of [0, W]) { const gr = g.createLinearGradient(sx, 0, sx ? sx - 420 : 420, 0); gr.addColorStop(0, 'rgba(0,0,0,0.92)'); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr; g.fillRect(sx ? sx - 420 : 0, 0, 420, H); }
    if (c.feixe) { poly(g, [[440, H], [640, H], [700, 460], [560, 460]], '#F2EBC8', 0.08); glow(g, 620, 900, 380, '#F2EBC8', 0.12); }
    vinheta(g, 0.66);
  };

  // ───────── BOCA DO POÇO vista de baixo: os capuzes brancos com velas azuladas fecham o céu ─────────
  CENARIOS.boca_poco = (g, t, c = {}) => {
    vgrad(g, 0, H, '#030806', '#0A1612'); const cx = 540, cy = 660, R = 300;
    for (let i = 9; i >= 0; i--) { const r = R + 80 + i * 110; g.fillStyle = i % 2 ? '#14221C' : '#101C17'; g.beginPath(); g.ellipse(cx, cy + i * 70, r, r * 0.94, 0, 0, Math.PI * 2); g.fill(); g.strokeStyle = `rgba(0,0,0,${0.9 - i * 0.07})`; g.lineWidth = 8; g.stroke(); } // fiadas de pedra
    const tampa = anim(c.tampa, t, 0), k = anim(c.capuzes, t, 0);
    g.save(); g.beginPath(); g.ellipse(cx, cy, R + 40, (R + 40) * 0.94, 0, 0, Math.PI * 2); g.clip(); vgrad(g, cy - R, cy + R, '#1A2A40', '#0A1424');
    for (let s2 = 0; s2 < 34; s2++) circ(g, cx + (rnd(s2) - 0.5) * R * 1.8, cy + (rnd(s2 + 3) - 0.5) * R * 1.7, 2 + rnd(s2 + 1) * 2, '#E8F0FF', 0.7 * (0.5 + 0.5 * Math.sin(t * 2 + s2)));
    circ(g, cx + 70, cy - 90, 60, '#E8EEDF', 0.9); glow(g, cx + 70, cy - 90, 200, '#C8D8E8', 0.2); rect(g, cx - R - 40, cy - R - 40, 2 * R + 80, 2 * R + 80, '#020403', tampa); // lua; a tampa escurece o céu
    const angs = [-1.62, -0.95, -0.2, 0.62, 1.38, 2.2, 2.95, 3.75], tams = [1.05, 0.9, 1.0, 0.85, 1.1, 0.92, 1.0, 0.88];
    for (let i = 0; i < angs.length; i++) { const ai = clamp(k * angs.length - [3, 5, 1, 6, 0, 4, 7, 2][i]), a = angs[i], sz = tams[i]; if (ai <= 0) continue; const ent = out(ai), rr2 = R * (1.2 - 0.3 * ent), x = cx + Math.cos(a) * rr2, y = cy + Math.sin(a) * rr2 * 0.94;
      g.save(); g.translate(x, y); g.rotate(a - Math.PI / 2); g.scale(sz * 0.72, sz * 0.72);
      g.fillStyle = '#D8D4C8'; g.beginPath(); g.ellipse(0, 150, 170, 120, 0, 0, Math.PI * 2); g.fill(); // ombros (atrás da borda)
      g.fillStyle = '#E6E2D6'; g.beginPath(); g.moveTo(-92, -70); g.bezierCurveTo(-110, 60, -60, 120, 0, 122); g.bezierCurveTo(60, 120, 110, 60, 92, -70); g.closePath(); g.fill(); // capuz arredondado (o alto do capuz fica para fora)
      g.fillStyle = 'rgba(0,0,0,0.18)'; g.beginPath(); g.ellipse(30, 0, 50, 100, 0, 0, Math.PI * 2); g.fill();
      g.fillStyle = '#040706'; g.beginPath(); g.ellipse(0, 4, 54, 72, 0, 0, Math.PI * 2); g.fill(); // sem rosto: o escuro do capuz
      const f = 1 + 0.15 * Math.sin(t * 12 + i), fy = -112; rect(g, -6, fy + 4, 12, 36, '#D8DCE8'); glow(g, 0, fy, 110 * f, VELA, 0.6); g.fillStyle = '#BFE0FF'; g.beginPath(); g.moveTo(0, fy - 30 * f); g.quadraticCurveTo(11, fy - 6, 0, fy + 6); g.quadraticCurveTo(-11, fy - 6, 0, fy - 30 * f); g.fill(); // vela segura à frente, para dentro do poço
      g.strokeStyle = rgba(VELA, 0.5); g.lineWidth = 5; g.beginPath(); g.ellipse(0, 4, 56, 74, 0, Math.PI * 1.15, Math.PI * 1.85); g.stroke(); // a vela acende a borda do capuz
      g.restore(); }
    g.restore();
    g.strokeStyle = '#1C2C24'; g.lineWidth = 90; g.beginPath(); g.ellipse(cx, cy, R + 85, (R + 85) * 0.94, 0, 0, Math.PI * 2); g.stroke(); // a borda de pedra cobre os corpos
    g.strokeStyle = 'rgba(0,0,0,0.5)'; g.lineWidth = 6; g.beginPath(); g.ellipse(cx, cy, R + 40, (R + 40) * 0.94, 0, 0, Math.PI * 2); g.stroke();
    glow(g, cx, cy, 760, VELA, 0.16 * k); vinheta(g, 0.55);
  };

  // ───────── PRAIA À NOITE com o poço de pedra na areia (c.dia = de manhã; c.carro = carro com porta-malas aberto) ─────────
  CENARIOS.areia_poco = (g, t, c = {}) => {
    const d = c.dia ? 1 : 0; vgrad(g, 0, 900, d ? '#9FB4BC' : '#06101A', d ? '#E8D8B8' : '#14283A'); if (!d) { for (let s = 0; s < 40; s++) circ(g, rnd(s) * W, rnd(s + 2) * 700, 1.5 + rnd(s + 1) * 2, '#E8F0FF', 0.6); circ(g, 820, 260, 70, '#E8EEDF'); glow(g, 820, 260, 400, '#C8D8E8', 0.25); } else glow(g, 300, 880, 600, '#FFE0A8', 0.5);
    vgrad(g, 880, 1020, d ? '#5A8090' : '#0A1E2A', d ? '#7A98A0' : '#0E2630'); for (let i = 0; i < 14; i++) { const y = 900 + i * 9 + Math.sin(t * 0.8 + i) * 3; line(g, rnd(i) * 600, y, rnd(i) * 600 + 200 + rnd(i + 2) * 300, y, d ? '#E8F0F0' : '#9FB8C8', 2, d ? 0.35 : 0.25); }
    const mare = 1010 + Math.sin(t * 0.6) * 8; vgrad(g, mare, H, d ? '#C8B48C' : '#1E2A28', d ? '#8A7454' : '#0A0F0E'); line(g, 0, mare, W, mare + 6, d ? '#F2F0E6' : '#6A8A8A', 4, 0.4);
    if (c.carro) { g.save(); g.translate(150, 1080); rrect(g, -160, -120, 320, 110, 30, d ? '#4A5058' : '#141A1E'); rrect(g, -110, -190, 200, 80, 26, d ? '#3A4048' : '#0E1216'); circ(g, -100, -6, 30, '#050606'); circ(g, 100, -6, 30, '#050606'); poly(g, [[140, -120], [230, -210], [250, -196], [160, -110]], d ? '#5A6068' : '#1A2226'); glow(g, 150, -90, 120, '#F2E0B0', 0.35); g.restore(); } // carro com o porta-malas aberto, luz de dentro
    const wx = 600, wy = 1080; g.fillStyle = d ? '#6A645A' : '#2A302C'; g.beginPath(); g.ellipse(wx, wy + 70, 250, 70, 0, 0, Math.PI); g.lineTo(wx - 250, wy); g.ellipse(wx, wy, 250, 66, 0, Math.PI, 0, true); g.fill(); // parede externa do poço
    for (let k = 0; k < 9; k++) line(g, wx - 230 + k * 58, wy + 10, wx - 230 + k * 58, wy + 110, 'rgba(0,0,0,0.3)', 4);
    g.fillStyle = d ? '#7A7468' : '#3A423C'; g.beginPath(); g.ellipse(wx, wy, 250, 66, 0, 0, Math.PI * 2); g.fill(); g.fillStyle = '#020403'; g.beginPath(); g.ellipse(wx, wy + 4, 200, 48, 0, 0, Math.PI * 2); g.fill(); // a boca, preta
    if (!d) glow(g, wx, wy, 300, VERDE, 0.08 + 0.04 * Math.sin(t * 2.4)); // o poço "respira" um verde fraco
    vinheta(g, d ? 0.3 : 0.6);
  };

  // ───────── GRAVADOR de fita na mesa da pousada (c.play: segundos em que o play é apertado; c.rec: luz vermelha acesa) ─────────
  CENARIOS.gravador_mesa = (g, t, c = {}) => {
    vgrad(g, 0, H, '#3A3226', '#16120C'); glow(g, 860, 300, 900, '#FFE2A8', 0.28); poly(g, [[620, 0], [1080, 0], [1080, 1400], [200, 1500]], '#FFE8B8', 0.05); // luz de manhã pela janela
    vgrad(g, 1020, H, '#5A3E24', '#2A1C10'); for (let y = 1060; y < H; y += 70) line(g, 0, y, W, y + 10, 'rgba(0,0,0,0.18)', 3); // tampo de madeira
    const tocando = c.play != null && t >= c.play, x0 = 170, y0 = 640, w = 740, h = 430;
    rrect(g, x0 + 20, y0 + 30, w, h, 34, '#000', 0.45); rrect(g, x0, y0, w, h, 34, '#2C2C2A'); rrect(g, x0, y0, w, 30, 20, 'rgba(255,255,255,0.06)');
    for (let i = 0; i < 6; i++) { const bx = x0 + 60 + i * 104, down = (i === 1 && tocando) ? 14 : 0; rrect(g, bx, y0 - 46 + down, 84, 60, 10, i === 0 ? '#8A2A20' : '#4A4A46'); } // teclas: REC, PLAY...
    rrect(g, x0 + 60, y0 + 70, 420, 220, 18, '#121210'); rrect(g, x0 + 80, y0 + 90, 380, 180, 12, '#3A3428'); rect(g, x0 + 100, y0 + 110, 340, 40, '#D8CCB0'); text(g, c.etiqueta || 'P. SERENO · DIA 7', x0 + 270, y0 + 142, 28, '#2A2018', { align: 'center', w: 700, mono: 1 }); // a fita, com etiqueta à mão
    for (const rx of [x0 + 170, x0 + 370]) { circ(g, rx, y0 + 210, 46, '#1A1610'); circ(g, rx, y0 + 210, 18, '#D8D0C0'); const a = tocando ? (t - c.play) * 4 : 0; for (let k = 0; k < 6; k++) { const aa = a + k * Math.PI / 3; line(g, rx, y0 + 210, rx + Math.cos(aa) * 16, y0 + 210 + Math.sin(aa) * 16, '#1A1610', 5); } }
    for (let i = 0; i < 9; i++) for (let j = 0; j < 7; j++) circ(g, x0 + 540 + i * 18, y0 + 90 + j * 26, 5, '#121210'); // alto-falante
    const led = c.rec || tocando, pis = c.piscar ? (Math.sin(t * 5) > 0 ? 1 : 0.25) : 1; circ(g, x0 + 640, y0 + 340, 14, led ? '#FF3020' : '#3A1410', led ? pis : 1); if (led) glow(g, x0 + 640, y0 + 340, 90, '#FF3020', 0.5 * pis);
    if (tocando) for (let i = 0; i < 10; i++) { const v = 0.3 + 0.7 * Math.abs(Math.sin(t * (6 + i) + i * 2)); rect(g, x0 + 80 + i * 40, y0 + 380 - v * 50, 28, v * 50, i > 7 ? '#E8A030' : VERDE, 0.85); } // VU
    vinheta(g, 0.5);
  };

  // ───────── PORTO SERENO AMANHECE (mar, casas no morro, o sol subindo) ─────────
  CENARIOS.porto_manha = (g, t, c = {}) => {
    const k = clamp(t / 8); vgrad(g, 0, 980, '#6A7A9A', '#F2C48A'); const sy = 900 - k * 140; glow(g, 640, sy, 700, '#FFD890', 0.6); circ(g, 640, sy, 90, '#FFF0C8');
    vgrad(g, 900, 1300, '#6A88A0', '#3A5A70'); for (let i = 0; i < 22; i++) { const y = 920 + i * 16, x = 640 + Math.sin(t * 0.7 + i) * 30; line(g, x - 40 - i * 8, y, x + 40 + i * 8, y, '#FFE8B8', 3, 0.5 - i * 0.02); } // reflexo do sol
    poly(g, [[0, 980], [0, 560], [160, 520], [300, 640], [420, 760], [520, 980]], '#2A3440'); for (let i = 0; i < 9; i++) { const x = 30 + i * 52, y = 640 + i * 30 - rnd(i) * 40; rect(g, x, y, 46, 56, '#E8D8C0'); poly(g, [[x - 6, y], [x + 23, y - 26], [x + 52, y], [x - 6, y]], '#A85A3A'); rect(g, x + 16, y + 20, 14, 18, '#3A3A44', 0.8); } // casinhas no morro
    rect(g, 600, 1080, 480, 26, '#4A3A2A'); for (let i = 0; i < 6; i++) rect(g, 620 + i * 80, 1106, 14, 200, '#3A2A1E'); // trapiche
    g.save(); g.translate(400 + Math.sin(t * 0.5) * 8, 1150); poly(g, [[-120, 0], [120, 0], [90, 46], [-90, 46]], '#E8E2D0'); rect(g, -4, -170, 8, 170, '#3A2A1E'); poly(g, [[4, -160], [90, -20], [4, -20]], '#F2EEE0'); g.restore(); // barquinho
    vgrad(g, 1300, H, '#C8B08A', '#8A7050'); line(g, 0, 1300 + Math.sin(t * 0.6) * 6, W, 1306, '#F8F4EA', 5, 0.6);
    for (let i = 0; i < 3; i++) { const x = (200 + i * 160 + t * 30) % 1200, y = 380 + i * 50 + Math.sin(t * 2 + i) * 10; g.strokeStyle = '#2A2A30'; g.lineWidth = 5; g.beginPath(); g.moveTo(x - 22, y); g.quadraticCurveTo(x - 10, y - 12 * Math.abs(Math.sin(t * 4 + i)), x, y); g.quadraticCurveTo(x + 10, y - 12 * Math.abs(Math.sin(t * 4 + i)), x + 22, y); g.stroke(); } // gaivotas
    vinheta(g, 0.3);
  };

  // ───────── PAREDE DO QUARTO com o círculo de giz; a caixa de madeira (c.close: de perto, aberta, com o bilhete) ─────────
  CENARIOS.parede_giz = (g, t, c = {}) => {
    if (c.close) { vgrad(g, 0, H, '#4A3A2A', '#1E160E'); glow(g, 540, 700, 800, '#FFE2B0', 0.2);
      rrect(g, 120, 420, 840, 720, 20, '#5A3A1E'); rrect(g, 160, 460, 760, 640, 14, '#2A1A0C'); for (let i = 0; i < 6; i++) line(g, 160, 500 + i * 110, 920, 510 + i * 110, 'rgba(0,0,0,0.2)', 3); // caixa aberta, vista de cima
      const b = anim(c.bilhete, t, 1); g.save(); g.translate(540, 780); g.rotate(-0.06); g.scale(lerp(0.85, 1, b), lerp(0.85, 1, b)); g.globalAlpha = 0.4 + 0.6 * b; rect(g, -300, -170, 620, 360, '#000', 0.35); rect(g, -310, -180, 620, 360, '#EEE6D0'); for (let i = 0; i < 4; i++) rect(g, -280, -100 + i * 70, 560, 2, '#9AA8B0', 0.45);
      if (c.texto !== false) { g.font = 'italic 700 92px Georgia'; g.textAlign = 'center'; g.fillStyle = '#2A2A3A'; g.globalAlpha = (0.4 + 0.6 * b) * clamp((t - (c.textoEm || 0)) / 0.8); g.fillText('Não apague.', 0, 30); g.textAlign = 'left'; } g.restore();
      vinheta(g, 0.5); return; }
    vgrad(g, 0, 1240, '#7A8478', '#4A5248'); for (let i = 0; i < 30; i++) rect(g, rnd(i) * W, rnd(i + 3) * 1200, 3, 40 + rnd(i) * 80, 'rgba(0,0,0,0.05)'); rect(g, 0, 1240, W, H - 1240, '#3A3026'); for (let y = 1290; y < H; y += 90) rect(g, 0, y, W, 3, 'rgba(0,0,0,0.25)');
    glow(g, 200, 300, 700, '#FFE8C0', 0.18);
    const cx = 560, cy = 600, r = 250; g.save(); g.lineCap = 'round'; for (const [lw, al] of [[22, 0.15], [9, 0.9]]) { g.strokeStyle = rgba(GIZ, al); g.lineWidth = lw; g.beginPath(); for (let a = 0; a <= Math.PI * 2 + 0.02; a += 0.03) { const x = cx + Math.cos(a) * r + (rnd(Math.floor(a * 33)) - 0.5) * 5, y = cy + Math.sin(a) * r; a ? g.lineTo(x, y) : g.moveTo(x, y); } g.stroke(); }
    g.strokeStyle = rgba(GIZ, 0.85); g.lineWidth = 7; for (const [a, b2, c2, d2] of [[-150, -60, -60, 40], [-60, 40, 20, -80], [40, -40, 140, 60], [-100, 110, 90, 120], [-20, -170, 30, -110]]) { g.beginPath(); g.moveTo(cx + a, cy + b2); g.lineTo(cx + c2, cy + d2); g.stroke(); } g.restore();
    glow(g, cx, cy, 420, VERDE, 0.06 + 0.03 * Math.sin(t * 1.6));
    rect(g, 760, 1060, 260, 26, '#4A3420'); rrect(g, 800, 970, 180, 92, 8, '#6A4628'); poly(g, [[800, 972], [980, 972], [1000, 900], [820, 900]], '#7A5634'); // a caixinha na prateleira, tampa aberta
    vinheta(g, 0.45);
  };

  // ───────── objeto: a ÁGUA por cima dos personagens (cobre pés e joelhos); repete a metade da frente do círculo de giz ─────────
  OBJETOS.agua = (g, o, u) => {
    const nv = lin(o.nivel, u, 50), y = GY - nv; g.save();
    vgrad(g, y, H, 'rgba(14,52,50,0.78)', 'rgba(4,16,16,0.92)'); for (let i = 0; i < 7; i++) { const yy = y + 8 + i * 22, a = 0.28 - i * 0.03; g.strokeStyle = `rgba(150,210,200,${a})`; g.lineWidth = 3; g.beginPath(); for (let x = 0; x <= W; x += 30) { const yw = yy + Math.sin(x * 0.02 + u * 2.2 + i) * 4; x ? g.lineTo(x, yw) : g.moveTo(x, yw); } g.stroke(); }
    line(g, 0, y, W, y, '#BFE8E0', 4, 0.4); g.restore();
    if (o.giz) { const k = anim(o.giz, u, 0); arcoGiz(g, k, 'frente', u, o.fechou != null && u >= o.fechou ? 1 + 1.5 * Math.exp(-(u - o.fechou) * 0.6) : 1); }
  };

  // pose: segura o gravador contra o peito e sorri, de olhos apertados (EP 28)
  Motor.POSES.segura_sorri = t => ({ al: [46, 112], ar: [-46, 112], fl: [-30, 235], fr: [30, 235], olho: 'apertado', boca: 'sorrisinho', sobr: 0, cabeca: 0.05, item: 'caderno' });

  // ───────── objeto: CAPUZ branco dos Contadores (sobre a cabeça do personagem: o.x, o.escala, o.y); o rosto some no escuro do capuz ─────────
  OBJETOS.capuz = (g, o, u) => {
    const e = o.escala || 1, cx = o.x * W, top = GY + (o.y || 0) - 520 * e; g.save(); g.translate(cx, top); g.scale(e, e);
    g.fillStyle = '#E6E2D6'; g.beginPath(); g.moveTo(-130, 230); g.quadraticCurveTo(-120, 150, -78, 128); g.quadraticCurveTo(-96, 20, -40, -60); g.quadraticCurveTo(0, -110, 10, -150); g.quadraticCurveTo(40, -90, 70, -40); g.quadraticCurveTo(100, 30, 78, 128); g.quadraticCurveTo(120, 150, 130, 230); g.closePath(); g.fill(); // capuz pontudo e capa nos ombros
    g.fillStyle = 'rgba(0,0,0,0.14)'; g.beginPath(); g.moveTo(10, -150); g.quadraticCurveTo(40, -90, 70, -40); g.quadraticCurveTo(100, 30, 78, 128); g.lineTo(30, 128); g.closePath(); g.fill();
    g.fillStyle = '#040706'; g.beginPath(); g.ellipse(0, 50, 50, 66, 0, 0, Math.PI * 2); g.fill(); // sem rosto
    g.restore();
  };

  // ───────── sons extras (água subindo, rádio invertido, procissão, clarão, pó, fita, mar) ─────────
  const antes = window.SfxExtra;
  window.SfxExtra = function (defs, h) {
    if (antes) antes(defs, h);
    const { G, F, O, N, C, dec, trap, glide, eco, rnd: rr, rng, bus } = h, V = p => (p.vol == null ? 1 : p.vol);
    defs.aguaSobe = function (t, p) { // água subindo: rumor líquido grave + bolhas
      const dur = p.dur || 6, T = t + dur, out = G(0); out.gain.setValueAtTime(0, t); out.gain.linearRampToValueAtTime(0.5 * V(p), T - 0.3); out.gain.linearRampToValueAtTime(0, T);
      const n = N(t, T, true), lp = F('lowpass', 300); lp.frequency.setValueAtTime(260, t); lp.frequency.linearRampToValueAtTime(900, T); C(n, lp, out);
      for (let s = t + 0.2; s < T - 0.2; s += rr(0.08, 0.35)) { const o = O('sine', 300, s, s + 0.09), g2 = G(0); glide(o.frequency, rr(250, 450), rr(600, 1100), s, s + 0.08); dec(g2.gain, s, 0.004, 0.25, 0.05); C(o, g2, out); }
      bus(out, true); return { t: t, fim: T };
    };
    defs.reverso = function (t, p) { // o rádio tocando a frequência ao contrário: sopros que crescem e cortam seco + tom que desliza
      const dur = p.dur || 5, T = t + dur, out = G(0.6 * V(p)); let s = t;
      while (s < T - 0.3) { const L = rr(0.35, 0.8), n = N(s, s + L), bp = F('bandpass', rr(600, 2400), 1.2), g2 = G(0); g2.gain.setValueAtTime(0.0001, s); g2.gain.exponentialRampToValueAtTime(0.9, s + L - 0.01); g2.gain.setValueAtTime(0, s + L); C(n, bp, g2, out);
        const o = O('sawtooth', 200, s, s + L), lp = F('lowpass', 1500), go = G(0); glide(o.frequency, rr(120, 200), rr(500, 900), s, s + L); go.gain.setValueAtTime(0.0001, s); go.gain.exponentialRampToValueAtTime(0.25, s + L - 0.01); go.gain.setValueAtTime(0, s + L); C(o, lp, go, out); s += L + rr(0.02, 0.12); }
      bus(out, true); return { t: t, fim: T };
    };
    defs.procissao = function (t, p) { // procissão cantando baixinho, longe (vozes graves em uníssono, eco de poço)
      const dur = p.dur || 8, T = t + dur, out = G(0), wet = G(1); trap(out.gain, t, dur, Math.min(2.5, dur * 0.4), 1.5, 0.3 * V(p));
      const seq = [0, 0, 3, 2, 0, -2, -4, -2, 0, 3, 5, 3], step = 1.3, f0 = 130.8;
      for (const det of [-6, 0, 5, 11]) { const o = O('sawtooth', f0, t, T); o.detune.value = det; const bp = F('bandpass', 620, 3), bp2 = F('bandpass', 1150, 4), g2 = G(0.5); C(o, bp, g2, out); C(o, bp2, G(0.25), out);
        let fa = f0; for (let i = 0; t + i * step < T; i++) { const s = t + i * step, f = f0 * Math.pow(2, seq[i % seq.length] / 12); o.frequency.setValueAtTime(fa, s); o.frequency.linearRampToValueAtTime(f, s + 0.25); fa = f; } }
      eco(out, wet, 0.31, 0.45, 1800, 0.6); bus(out, true); bus(wet, true); return { t: t, fim: T + 1.5 };
    };
    defs.estouro = function (t, p) { // o clarão: sopro que cresce 1,2 s, estoura e cai com um grave
      const sobe = p.sobe || 1.2, T = t + sobe + 3, out = G(0.7 * V(p)), n = N(t, T), hp = F('highpass', 400), g2 = G(0); g2.gain.setValueAtTime(0.0001, t); g2.gain.exponentialRampToValueAtTime(0.7, t + sobe); g2.gain.exponentialRampToValueAtTime(0.0001, T); C(n, hp, g2, out);
      const o = O('sine', 55, t + sobe, T), go = G(0); glide(o.frequency, 70, 38, t + sobe, T); dec(go.gain, t + sobe, 0.01, 1, 2.2); C(o, go, out);
      const o2 = O('sine', 880, t + sobe, T), go2 = G(0); dec(go2.gain, t + sobe, 0.005, 0.18, 2.6); C(o2, go2, out);
      bus(out, true); return { t: t, fim: T };
    };
    defs.po = function (t, p) { // os Ocos desabando em pó: areia escorrendo
      const dur = p.dur || 2.5, T = t + dur, out = G(0), n = N(t, T), bp = F('bandpass', 3200, 0.7), g2 = G(0); out.gain.setValueAtTime(0.5 * V(p), t); out.gain.linearRampToValueAtTime(0, T); C(n, bp, g2, out); g2.gain.setValueAtTime(0, t);
      for (let s = t; s < T; s += rr(0.01, 0.06)) { g2.gain.setValueAtTime(rr(0.1, 1), s); g2.gain.linearRampToValueAtTime(0, s + 0.03); }
      const n2 = N(t, T, true), lp = F('lowpass', 160), g3 = G(0.6); C(n2, lp, g3, out); bus(out, true); return { t: t, fim: T };
    };
    defs.fita = function (t, p) { // tecla do gravador (clique mecânico) + motor e chiado de fita
      const dur = p.dur || 4, T = t + dur, out = G(V(p)); const n = N(t, t + 0.05), bp = F('bandpass', 1800, 1.5), g2 = G(0); dec(g2.gain, t, 0.001, 0.9, 0.03); C(n, bp, g2, out);
      const o = O('sine', 90, t + 0.05, t + 0.12), go = G(0); dec(go.gain, t + 0.05, 0.002, 0.5, 0.04); C(o, go, out);
      if (!p.soClique) { const h2 = N(t + 0.1, T), hp = F('highpass', 4000), gh = G(0); trap(gh.gain, t + 0.1, dur - 0.1, 0.15, 0.2, 0.06); C(h2, hp, gh, out); const m = O('triangle', 50, t + 0.1, T), gm = G(0); trap(gm.gain, t + 0.1, dur - 0.1, 0.2, 0.2, 0.02); C(m, gm, out); }
      bus(out, true); return { t: t, fim: T };
    };
    defs.mar = function (t, p) { // ondas na praia, devagar
      const dur = p.dur || 10, T = t + dur, out = G(0), n = N(t, T, true), lp = F('lowpass', 700); trap(out.gain, t, dur, 1.2, 1.2, 0.4 * V(p)); const g2 = G(0.2); C(n, lp, g2, out);
      for (let s = t; s < T; s += rr(4.5, 6.5)) { g2.gain.setValueAtTime(0.15, s); g2.gain.linearRampToValueAtTime(1, s + 1.8); g2.gain.linearRampToValueAtTime(0.15, s + 4.2); }
      bus(out, true); return { t: t, fim: T };
    };
  };

  // ───────── filtro de GRAVADOR: nesta página, a fala com "efeito": "sussurro" vira voz saindo do gravador de fita ─────────
  // (banda de 300 a 3400 Hz, leve saturação, chiado de fita e o clique da tecla). Nenhum ep da versão Opus usa o sussurro real (o Credor é ElevenLabs).
  if (window.VozFx) window.VozFx.sussurro = (x, sr) => {
    const pre = Math.round(0.2 * sr), pos = Math.round(0.35 * sr), y = new Float32Array(x.length + pre + pos); let pk0 = 0; for (const v of x) pk0 = Math.max(pk0, Math.abs(v));
    const hp = (f) => { const a = Math.exp(-2 * Math.PI * f / sr); let px = 0, py = 0; return v => { py = a * (py + v - px); px = v; return py; }; }, lp = (f) => { const a = Math.exp(-2 * Math.PI * f / sr); let py = 0; return v => (py = (1 - a) * v + a * py); };
    const h1 = hp(300), h2 = hp(300), l1 = lp(3400), l2 = lp(3400), lh = lp(5000); let s = 12345; const rn = () => { s = (s * 1103515245 + 12345) & 0x7fffffff; return s / 0x7fffffff - 0.5; };
    let pk = 0; for (let i = 0; i < y.length; i++) { const v = i >= pre && i < pre + x.length ? x[i - pre] : 0; let w = l2(l1(h2(h1(v)))); w = Math.tanh(w * 2.2) / Math.tanh(2.2); y[i] = w; pk = Math.max(pk, Math.abs(w)); }
    const g = pk > 0 ? (pk0 * 0.95) / pk : 1; for (let i = 0; i < y.length; i++) { y[i] = y[i] * g + lh(rn()) * 0.022 * pk0; }
    for (let i = 0; i < Math.round(0.012 * sr); i++) y[i] += (rn() * 0.5) * pk0 * Math.exp(-i / (0.003 * sr)); // clique da tecla
    return y;
  };
})();
