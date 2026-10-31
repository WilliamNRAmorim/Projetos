// Cenários do Dia 7 dos contos (Máscara da Morte Rubra, Iara, Homem do Saco, Vizinho bate na parede). Só ACRESCENTA ao Motor. Nada de violência aparece.
(() => {
  const { CENARIOS, POSES, OBJETOS, W, H, GY } = Motor, { rect, poly, circ, line, rrect, text, glow, vgrad, rgba, vinheta, rnd, lerp, clamp, out } = Motor.H_;
  const fundoGrad = (g, a, b) => vgrad(g, 0, H, a, b);

  // ───────── A MÁSCARA DA MORTE RUBRA (carmesim) ─────────
  const COR7 = { azul: '#2A5AD0', roxo: '#7A3AB0', verde: '#2A9A4A', laranja: '#E8842A', branco: '#E8E8F0', violeta: '#8A2AC8', preto: '#D01030' };
  const braseiro = (g, x, y, t, on = true) => { rect(g, x - 5, y, 10, 150, '#14080A'); line(g, x - 50, y + 150, x, y, '#14080A', 8); line(g, x + 50, y + 150, x, y, '#14080A', 8); rrect(g, x - 44, y - 20, 88, 34, 14, '#2A1014'); if (on) { const f = 1 + 0.15 * Math.sin(t * 11 + x); glow(g, x, y - 40, 180 * f, '#FF6A1A', 0.45); g.fillStyle = '#FF7A1A'; g.beginPath(); g.moveTo(x, y - 90 * f); g.quadraticCurveTo(x + 30, y - 30, x, y - 16); g.quadraticCurveTo(x - 30, y - 30, x, y - 90 * f); g.fill(); } };
  CENARIOS.salao_cores = (g, t, c = {}) => { // um dos sete salões: c.cor 'azul'|'roxo'|'verde'|'laranja'|'branco'|'violeta'|'preto' (preto tem vitrais vermelhos), c.proximo (cor do salão ao fundo), c.apaga
    const cor = COR7[c.cor || 'azul'], pret = c.cor === 'preto', on = !c.apaga, fl = on ? 0.9 + 0.1 * Math.sin(t * 9) : 0.08; fundoGrad(g, pret ? '#06030A' : rgba(cor, 1), pret ? '#020104' : '#0A0610'); rect(g, 0, 0, W, H, 'rgba(0,0,0,0.55)');
    const vx = 540, vy = 720; poly(g, [[0, 0], [W, 0], [vx + 200, vy - 140], [vx - 200, vy - 140]], pret ? '#0A060E' : '#14101C'); poly(g, [[0, H], [W, H], [vx + 200, vy + 220], [vx - 200, vy + 220]], pret ? '#0C0810' : '#1A1420'); poly(g, [[0, 0], [vx - 200, vy - 140], [vx - 200, vy + 220], [0, H]], pret ? '#12060A' : rgba(cor, 0.5)); poly(g, [[W, 0], [vx + 200, vy - 140], [vx + 200, vy + 220], [W, H]], pret ? '#12060A' : rgba(cor, 0.5));
    rect(g, vx - 200, vy - 140, 400, 360, pret ? '#020104' : rgba(COR7[c.proximo || c.cor] || cor, 0.9)); g.strokeStyle = '#05030A'; g.lineWidth = 26; g.beginPath(); g.moveTo(vx - 200, vy + 220); g.lineTo(vx - 200, vy - 60); g.arc(vx, vy - 60, 200, Math.PI, 0); g.lineTo(vx + 200, vy + 220); g.stroke();
    for (const [sg, x0, x1] of [[-1, 30, 190], [1, W - 190, W - 30]]) { for (let i = 0; i < 2; i++) { const xa = sg < 0 ? x0 : x1 - 120, y0 = 360 + i * 0, w = 140, h = 520; g.save(); g.beginPath(); g.moveTo(xa, y0 + h); g.lineTo(xa, y0 + 100); g.quadraticCurveTo(xa + w / 2, y0 - 50, xa + w, y0 + 100); g.lineTo(xa + w, y0 + h); g.closePath(); g.fillStyle = pret ? `rgba(220,20,40,${fl})` : rgba(cor, fl); g.fill(); g.lineWidth = 8; g.strokeStyle = '#05030A'; g.stroke(); g.restore(); glow(g, xa + w / 2, y0 + 300, 360, pret ? '#FF2040' : cor, 0.35 * fl); } braseiro(g, sg < 0 ? 100 : W - 100, 940, t, on); }
    for (let i = 0; i < 12; i++) line(g, 0, 1300 + i * 50, W, 1300 + i * 50, 'rgba(255,255,255,0.04)', 3); vinheta(g, 0.55);
  };
  CENARIOS.relogio_ebano = (g, t, c = {}) => { // relógio de ébano no salão preto; c.hora [h,m]; c.toca (balança e clareia)
    fundoGrad(g, '#06030A', '#12060A'); rect(g, 0, 1240, W, H - 1240, '#0A040A'); const k = c.toca ? Math.max(0, 1 - (t - (c.tocaEm || 0)) * 1.2) * (t >= (c.tocaEm || 0) ? 1 : 0) : 0, sh = Math.sin(t * 60) * 5 * k;
    for (const sg of [-1, 1]) { rect(g, sg < 0 ? 0 : W - 160, 200, 160, 1040, '#1A0A10'); for (let i = 0; i < 5; i++) line(g, (sg < 0 ? 0 : W - 160) + 20 + i * 30, 200, (sg < 0 ? 0 : W - 160) + 20 + i * 30, 1240, 'rgba(0,0,0,0.5)', 5); glow(g, sg < 0 ? 80 : W - 80, 700, 420, '#FF2040', 0.2); }
    g.save(); g.translate(sh, 0); rect(g, 330, 260, 420, 980, '#050304'); rect(g, 310, 240, 460, 40, '#0A0608'); poly(g, [[330, 260], [540, 140], [750, 260]], '#0A0608'); circ(g, 540, 460, 150, '#E8E4D8'); circ(g, 540, 460, 140, '#0A0608', 0.0); for (let i = 0; i < 12; i++) { const a = i / 12 * Math.PI * 2; line(g, 540 + Math.sin(a) * 120, 460 - Math.cos(a) * 120, 540 + Math.sin(a) * 138, 460 - Math.cos(a) * 138, '#05030A', 6); }
    const hh = (c.hora?.[0] ?? 12) % 12, mm = c.hora?.[1] ?? 0, am = mm / 60 * Math.PI * 2, ah = (hh + mm / 60) / 12 * Math.PI * 2; line(g, 540, 460, 540 + Math.sin(am) * 110, 460 - Math.cos(am) * 110, '#05030A', 8); line(g, 540, 460, 540 + Math.sin(ah) * 74, 460 - Math.cos(ah) * 74, '#05030A', 12); rect(g, 430, 660, 220, 460, '#0A0608'); rect(g, 444, 674, 192, 432, '#14080C'); const ps = Math.sin(t * 3.1) * 70; line(g, 540, 700, 540 + ps, 1000, '#8A6A3A', 8); circ(g, 540 + ps, 1010, 40, '#B8924C'); g.restore();
    if (k > 0) rect(g, 0, 0, W, H, `rgba(255,255,255,${0.35 * k})`); glow(g, 540, 460, 640, '#FF2040', 0.12 + 0.2 * k); vinheta(g, 0.6);
  };
  CENARIOS.ceu_rubro = (g, t, c = {}) => { // o país tomado pela peste: céu vermelho, silhuetas de casas, lua rubra, fumaça
    fundoGrad(g, '#3A0610', '#A0182A'); circ(g, 700, 440, 150, '#E83A3A', 0.9); glow(g, 700, 440, 700, '#FF4A4A', 0.3); for (const [x, w, h] of [[-20, 240, 460], [200, 200, 340], [380, 280, 520], [680, 240, 400], [880, 260, 560]]) { rect(g, x, 1240 - h, w, h, '#14040A'); poly(g, [[x - 10, 1240 - h], [x + w / 2, 1240 - h - 90], [x + w + 10, 1240 - h]], '#0A0206'); }
    for (let i = 0; i < 9; i++) { const k = (t * 0.08 + i / 9) % 1; glow(g, 120 + i * 110, 1100 - k * 800, 200, '#2A0408', 0.4); } rect(g, 0, 1240, W, H - 1240, '#0A0206'); for (let i = 0; i < 6; i++) circ(g, 160 + i * 150, 1260, 18, '#FF7A2A', 0.6 + 0.3 * Math.sin(t * 6 + i)); vinheta(g, 0.6);
  };
  CENARIOS.abadia_muralha = (g, t, c = {}) => { // abadia fortificada: muralha alta, torres, portão de ferro soldado
    fundoGrad(g, '#0A0612', '#4A1020'); circ(g, 860, 280, 80, '#E8C8C8', 0.8); glow(g, 860, 280, 400, '#FFB0B0', 0.2); for (const x of [40, 820]) { rect(g, x, 300, 220, 940, '#1A1620'); for (let i = 0; i < 5; i++) rect(g, x + i * 46, 270, 34, 40, '#1A1620'); poly(g, [[x - 20, 300], [x + 110, 160], [x + 240, 300]], '#0E0A14'); rect(g, x + 90, 520, 40, 120, '#02010A'); }
    rect(g, 260, 560, 560, 680, '#221C2A'); for (let r = 0; r < 14; r++) for (let k = 0; k < 6; k++) rect(g, 260 + k * 94 + (r % 2) * 47, 560 + r * 48, 90, 44, r % 2 ? '#2A2432' : '#251F2D'); for (let i = 0; i < 6; i++) rect(g, 260 + i * 94, 530, 70, 36, '#221C2A');
    rect(g, 400, 760, 280, 480, '#06040A'); for (let i = 0; i < 9; i++) rect(g, 410 + i * 30, 770, 12, 460, '#3A3A44'); rect(g, 400, 760, 280, 12, '#5A5A66'); rect(g, 400, 980, 280, 12, '#5A5A66'); for (let i = 0; i < 6; i++) circ(g, 425 + i * 46, 986, 8, '#FF7A2A', 0.8); rect(g, 0, 1240, W, H - 1240, '#08060C'); vinheta(g, 0.55);
  };
  OBJETOS.morte_mascara = (g, o, u) => { // a figura alta e magra em mortalha com máscara de cadáver e manchas vermelhas (o.x, o.y chão em px, o.escala, o.costas)
    const e = o.escala || 1, x = o.x * W, y = o.y ?? 1240, a = clamp(u / 0.6); g.save(); g.globalAlpha = a; g.translate(x, y); g.scale(e, e); const sw = Math.sin(u * 1.5) * 6;
    poly(g, [[-110, 0], [-60, -520], [60, -520], [110, 0]], '#CFCBC0'); poly(g, [[-110, 0], [-60, -520], [-30, -520], [-70, 0]], 'rgba(0,0,0,0.18)'); for (const [dx, dy, r] of [[-30, -300, 26], [30, -180, 20], [-10, -120, 30], [50, -380, 14]]) circ(g, dx, dy, r, '#A01020', 0.75); poly(g, [[-60, -520], [-20, -620 + sw], [20, -620 + sw], [60, -520]], '#CFCBC0');
    if (!o.costas) { g.fillStyle = '#EDEAE0'; g.beginPath(); g.ellipse(0, -600, 42, 56, 0, 0, Math.PI * 2); g.fill(); g.fillStyle = '#0A0408'; g.beginPath(); g.ellipse(-16, -610, 10, 14, 0, 0, Math.PI * 2); g.ellipse(16, -610, 10, 14, 0, 0, Math.PI * 2); g.fill(); line(g, -18, -572, 18, -572, '#0A0408', 5); for (let i = -2; i <= 2; i++) line(g, i * 7, -576, i * 7, -566, '#0A0408', 3); } else { g.fillStyle = '#CFCBC0'; g.beginPath(); g.ellipse(0, -600, 44, 58, 0, 0, Math.PI * 2); g.fill(); }
    g.restore();
  };
  OBJETOS.mortalha_vazia = (g, o, u) => { // mortalha e máscara caídas, vazias (o.x, o.y)
    const x = o.x * W, y = o.y ?? 1240, k = out(clamp(u / 0.8)); g.save(); g.translate(x, y); poly(g, [[-220, 0], [-160, -60 * k], [-40, -110 * k], [60, -80 * k], [200, -40 * k], [240, 0]], '#CFCBC0'); poly(g, [[-220, 0], [-160, -60 * k], [-120, -20], [-150, 0]], 'rgba(0,0,0,0.2)'); for (const [dx, dy] of [[-60, -40], [90, -20]]) circ(g, dx, dy * k, 18, '#A01020', 0.7); g.fillStyle = '#EDEAE0'; g.beginPath(); g.ellipse(-30, -120 * k, 44, 52, -0.2, 0, Math.PI * 2); g.fill(); g.fillStyle = '#0A0408'; g.beginPath(); g.ellipse(-46, -128 * k, 9, 13, 0, 0, Math.PI * 2); g.ellipse(-12, -130 * k, 9, 13, 0, 0, Math.PI * 2); g.fill(); g.restore();
  };

  // ───────── IARA (turquesa) ─────────
  CENARIOS.rio_iara = (g, t, c = {}) => { // rio à noite, lua e névoa; c.manha, c.canoa (x 0..1 | false), c.gira, c.ondas, c.iara (brilho), c.margem
    const m = c.manha ? 1 : 0; vgrad(g, 0, 900, m ? '#7AB8C8' : '#031A24', m ? '#F2D8B8' : '#0E4A5A'); if (!m) { circ(g, 780, 300, 110, '#E8FFF8', 0.9); glow(g, 780, 300, 520, '#9AF2E8', 0.3); } else glow(g, 300, 800, 700, '#FFF0C8', 0.4);
    rect(g, 0, 840, W, 120, m ? '#2A5A4A' : '#04141A'); for (let i = 0; i < 20; i++) { const x = i * 60, h = 100 + rnd(i) * 160; poly(g, [[x, 880], [x + 30, 880 - h], [x + 70, 880]], m ? '#2A6A4A' : '#06222A'); }
    vgrad(g, 900, H, m ? '#4A98A8' : '#0A4A5A', m ? '#1A5868' : '#02161C'); for (let i = 0; i < 40; i++) { const y = 940 + rnd(i + 3) * 940, x = rnd(i) * W; line(g, x, y, x + 120 + 40 * Math.sin(t * 1.5 + i), y, m ? 'rgba(255,255,255,0.25)' : 'rgba(160,255,240,0.18)', 4); }
    if (!m) { glow(g, 540, 1000, 900, '#7AF2E8', 0.1); for (let i = 0; i < 6; i++) { const k = (t * 0.05 + i / 6) % 1; glow(g, 100 + i * 180, 900 + 20 * Math.sin(t + i), 260, '#9AF2E8', 0.1); } }
    if (c.ondas) for (let i = 0; i < 4; i++) { const k = (t * 0.5 + i / 4) % 1; g.strokeStyle = `rgba(160,255,240,${0.5 * (1 - k)})`; g.lineWidth = 5; g.beginPath(); g.ellipse(c.ondasX ?? 540, c.ondasY ?? 1150, 60 + k * 500, 18 + k * 120, 0, 0, Math.PI * 2); g.stroke(); }
    if (c.iara) glow(g, c.iaraX ?? 270, 1000, 520, '#9AF2E8', 0.35 * c.iara);
    if (c.canoa !== undefined && c.canoa !== false) { const cx = (typeof c.canoa === 'number' ? c.canoa : 0.69) * W, rot = c.gira ? Math.sin(t * 0.8) * 0.25 + t * 0.15 : 0; g.save(); g.translate(cx + Math.sin(t * 1.4) * 6, 1390 + Math.sin(t * 2) * 4); g.scale(Math.cos(rot), 1); poly(g, [[-420, 0], [420, 0], [320, 90], [-320, 90]], '#3A2410'); rect(g, -420, -8, 840, 10, '#5A3A20'); g.restore(); }
    if (c.margem) { poly(g, [[0, 1180], [W, 1130], [W, H], [0, H]], '#D8C098'); for (let i = 0; i < 40; i++) circ(g, rnd(i) * W, 1220 + rnd(i + 3) * 600, 3 + rnd(i) * 4, 'rgba(0,0,0,0.12)'); }
    vinheta(g, 0.5);
  };

  // ───────── HOMEM DO SACO (lilás) ─────────
  CENARIOS.quarto_lilas = (g, t, c = {}) => { // quarto de criança, noite lilás; c.mao (menina com a mão na boca), c.olhos
    fundoGrad(g, '#2A2040', '#0E0A1A'); rect(g, 0, 1240, W, H - 1240, '#08060E'); for (let y = 1280; y < H; y += 90) rect(g, 0, y, W, 3, '#050308'); rect(g, 600, 300, 340, 480, '#05030A'); vgrad(g, 316, 764, '#4A3A78', '#1A1438', 616, 308); rect(g, 766, 316, 10, 448, '#05030A'); circ(g, 840, 440, 40, '#E8E0FF', 0.7); glow(g, 840, 440, 300, '#C8B8FF', 0.2); poly(g, [[600, 780], [940, 780], [1060, 1500], [480, 1500]], '#C8B8FF', 0.05);
    rect(g, 40, 1000, 560, 240, '#4A3A6A'); rect(g, 20, 900, 30, 340, '#08060E'); rrect(g, 70, 950, 300, 80, 34, '#E8E0F8', 0.8); const hx = 230; circ(g, hx, 975, 66, '#D8B890'); g.fillStyle = '#3A2A22'; g.beginPath(); g.arc(hx, 968, 70, Math.PI, Math.PI * 2); g.fill(); rect(g, hx - 86, 960, 22, 64, '#3A2A22'); rect(g, hx + 64, 960, 22, 64, '#3A2A22');
    for (const dx of [-22, 22]) { circ(g, hx + dx, 980, 14, '#FFF'); circ(g, hx + dx + 4, 982, 6, '#10140F'); line(g, hx + dx - 14, 956, hx + dx + 12, 953, '#2A1E18', 5); } if (c.mao) { rrect(g, hx - 34, 1000, 68, 40, 18, '#D8B890'); for (let i = 0; i < 4; i++) line(g, hx - 24 + i * 16, 1004, hx - 24 + i * 16, 1034, 'rgba(0,0,0,0.2)', 3); } else line(g, hx - 12, 1010, hx + 12, 1010, '#6A4038', 5);
    poly(g, [[110, 1040], [320, 1030], [600, 1060], [600, 1240], [100, 1240]], '#7A5AA8'); vinheta(g, 0.55);
  };
  CENARIOS.rua_lilas = (g, t, c = {}) => { // rua à noite vista da janela, lilás; c.homem = x (0..1) do Homem do Saco arrastando o saco; c.arrasta
    fundoGrad(g, '#14102A', '#3A2E5A'); for (let i = 0; i < 30; i++) circ(g, rnd(i) * W, rnd(i + 99) * 400, 1.4 + rnd(i + 5) * 1.6, '#E8E0FF', 0.3); for (const [x, w, h, col] of [[-40, 320, 560, '#1A1632'], [300, 280, 440, '#221C40'], [580, 300, 620, '#1A1632'], [860, 280, 500, '#221C40']]) { rect(g, x, 1240 - h, w, h, col); poly(g, [[x - 14, 1240 - h], [x + w / 2, 1240 - h - 90], [x + w + 14, 1240 - h]], '#0E0A1E'); rect(g, x + 50, 1240 - h + 100, 80, 110, rnd(x) > 0.5 ? '#E8D8A0' : '#05030A'); }
    rect(g, 0, 1240, W, H - 1240, '#0C0818'); poly(g, [[300, 1240], [780, 1240], [1100, H], [-120, H]], '#1A1430'); rect(g, 140, 640, 14, 620, '#05030A'); rect(g, 110, 620, 80, 20, '#05030A'); rect(g, 120, 636, 60, 12, '#F2EAB0'); glow(g, 150, 646, 520, '#E8E0A0', 0.3);
    if (c.homem != null) { const x = c.homem * W + (c.arrasta ? Math.sin(t * 2) * 10 : 0), by = 1330, sk = c.arrasta ? 1 + 0.04 * Math.sin(t * 5) : 1; g.save(); g.translate(x, by); g.fillStyle = '#020104'; g.beginPath(); g.ellipse(0, -330, 54, 62, 0, 0, Math.PI * 2); g.fill(); poly(g, [[-90, -430], [90, -430], [70, -380], [-70, -380]], '#020104'); poly(g, [[-70, -290], [70, -290], [110, -60], [-110, -60]], '#020104'); rect(g, -50, -60, 36, 160, '#020104'); rect(g, 14, -60, 36, 160, '#020104'); line(g, 70, -250, 220, -120, '#020104', 44); g.fillStyle = '#6A5A3A'; g.beginPath(); g.ellipse(300, -40, 150 * sk, 120 * sk, 0, 0, Math.PI * 2); g.fill(); for (let i = 0; i < 5; i++) { const bx = 230 + i * 40, by2 = -70 + Math.sin(t * 3 + i * 2) * 14; g.fillStyle = 'rgba(0,0,0,0.25)'; g.beginPath(); g.ellipse(bx, by2, 22, 30, 0, 0, Math.PI * 2); g.fill(); } g.restore(); }
    vinheta(g, 0.55);
  };
  CENARIOS.saco_close = (g, t, c = {}) => { // o saco de aniagem de perto, com volumes (mãos e cabeças) empurrando por dentro
    fundoGrad(g, '#14102A', '#08060E'); g.fillStyle = '#7A6A44'; g.beginPath(); g.moveTo(240, 1500); g.quadraticCurveTo(120, 900, 300, 560); g.quadraticCurveTo(540, 380, 780, 560); g.quadraticCurveTo(960, 900, 840, 1500); g.closePath(); g.fill(); for (let i = 0; i < 40; i++) line(g, 240 + rnd(i) * 600, 560 + rnd(i + 3) * 900, 260 + rnd(i) * 600 + 40, 560 + rnd(i + 3) * 900 + 4, 'rgba(0,0,0,0.25)', 4);
    for (let i = 0; i < 6; i++) { const bx = 360 + (i % 3) * 180, by = 760 + Math.floor(i / 3) * 300 + Math.sin(t * 2 + i) * 18; g.fillStyle = 'rgba(0,0,0,0.22)'; g.beginPath(); g.ellipse(bx, by, 60, 80, 0, 0, Math.PI * 2); g.fill(); g.fillStyle = 'rgba(255,255,255,0.06)'; g.beginPath(); g.ellipse(bx - 14, by - 20, 30, 40, 0, 0, Math.PI * 2); g.fill(); }
    rect(g, 380, 480, 320, 60, '#4A3A24'); line(g, 360, 500, 720, 500, '#B89A5A', 10); glow(g, 540, 900, 760, '#9A8AC8', 0.15); vinheta(g, 0.6);
  };

  // ───────── VIZINHO BATE NA PAREDE (salmão) ─────────
  CENARIOS.quarto_salmao = (g, t, c = {}) => { // apartamento novo, caixas de mudança; a parede da direita recebe as batidas (c.ondas = anéis na parede)
    fundoGrad(g, '#E8A88A', '#B8705A'); rect(g, 0, 1240, W, H - 1240, '#6A3A2A'); for (let y = 1280; y < H; y += 90) rect(g, 0, y, W, 3, '#4A2418'); rect(g, 0, 880, W, 12, '#9A5A44');
    poly(g, [[W - 360, 0], [W, 0], [W, 1240], [W - 360, 1240]], '#D8886A'); poly(g, [[W - 360, 0], [W - 300, 40], [W - 300, 1200], [W - 360, 1240]], 'rgba(0,0,0,0.12)');
    for (const [x, y, w, h] of [[60, 980, 240, 260], [120, 780, 200, 200], [320, 1060, 200, 180]]) { rect(g, x, y, w, h, '#C8A070'); rect(g, x, y, w, 12, '#A88050'); rect(g, x + w / 2 - 6, y, 12, h, '#B89060'); }
    rect(g, 540, 940, 300, 300, '#F2E8E0'); rect(g, 520, 900, 30, 340, '#5A2A1A'); rrect(g, 560, 910, 200, 60, 26, '#FFF', 0.9); rect(g, 340, 340, 200, 300, '#3A2018'); rect(g, 350, 350, 180, 280, '#8A9AB0');
    if (c.ondas) for (let i = 0; i < 3; i++) { const k = (t * 1.2 + i / 3) % 1; g.strokeStyle = `rgba(255,255,255,${0.7 * (1 - k)})`; g.lineWidth = 6; g.beginPath(); g.arc(c.ondasX ?? 900, c.ondasY ?? 780, 20 + k * 200, 0, Math.PI * 2); g.stroke(); }
    vinheta(g, 0.5);
  };
  CENARIOS.predio_vazio = (g, t, c = {}) => { // fachada do prédio à noite vista de baixo; sexto andar com a janela dela acesa e, ao lado, só o vazio (a parede dá para a rua)
    fundoGrad(g, '#2A1810', '#6A3828'); for (let i = 0; i < 30; i++) circ(g, rnd(i) * W, rnd(i + 99) * 500, 1.4 + rnd(i + 5) * 1.6, '#FFE9D8', 0.3);
    rect(g, 240, 160, 600, 1080, '#8A4A38'); for (let r = 0; r < 6; r++) for (let k = 0; k < 3; k++) { const x = 290 + k * 180, y = 220 + r * 160, own = r === 1 && k === 1; rect(g, x, y, 110, 120, '#1A0A08'); rect(g, x + 8, y + 8, 94, 104, own ? '#FFD890' : (rnd(r * 3 + k) > 0.5 ? '#B8A080' : '#2A1A14')); if (own) glow(g, x + 55, y + 60, 200, '#FFB860', 0.35); } text(g, '6º', 190, 400, 44, '#FFD8B8', { align: 'right', w: 800, mono: 1 });
    rect(g, 0, 1240, W, H - 1240, '#1A0C08'); rect(g, 0, 1240, W, 24, '#3A2018'); rect(g, 840, 160, 240, 1080, 'rgba(0,0,0,0.0)'); vinheta(g, 0.55);
  };
})();
