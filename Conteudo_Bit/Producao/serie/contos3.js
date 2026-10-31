// Cenários do Dia 3 dos contos (O Enfermeiro, Curupira, Criança pede carona, Cuca). Só ACRESCENTA ao Motor.
(() => {
  const { CENARIOS, POSES, OBJETOS, W, H, GY } = Motor, { rect, poly, circ, line, rrect, text, glow, vgrad, rgba, vinheta, rnd, lerp, clamp, out } = Motor.H_;
  const fundoGrad = (g, a, b) => vgrad(g, 0, H, a, b);

  // ───────── O ENFERMEIRO (sépia) ─────────
  CENARIOS.varanda_vila = (g, t, c = {}) => { // casa de vila do interior (1859) no fim da tarde; varanda com colunas
    vgrad(g, 0, 1000, '#6A5A3A', '#D8B070'); glow(g, 840, 900, 700, '#FFE0A0', 0.35); circ(g, 840, 900, 90, '#FFE9B8', 0.7);
    poly(g, [[0, 960], [300, 880], [640, 950], [1080, 900], [1080, 1010], [0, 1010]], '#5A4426'); rect(g, 0, 1000, W, 240, '#7A5E36'); rect(g, 0, 1240, W, H - 1240, '#4A3820');
    rect(g, 140, 560, 800, 520, '#B89060'); rect(g, 140, 560, 800, 16, '#8A6A40'); poly(g, [[100, 560], [540, 380], [980, 560]], '#5A3A22'); for (let i = 0; i < 9; i++) line(g, 200 + i * 80, 540, 360 + i * 40, 420, 'rgba(0,0,0,0.25)', 3);
    rect(g, 440, 740, 200, 340, '#3A2616'); rect(g, 452, 752, 176, 328, '#5A3A22'); circ(g, 600, 920, 9, '#E8C880'); for (const x of [200, 760]) { rect(g, x, 700, 130, 160, '#2A1A0E'); rect(g, x + 10, 710, 110, 140, '#E8C070', 0.8); rect(g, x + 60, 710, 8, 140, '#2A1A0E'); }
    for (const x of [130, 330, 530, 730, 930]) rect(g, x - 14, 700, 28, 540, '#D8B888'); rect(g, 100, 1190, 880, 50, '#8A6A40'); rect(g, 100, 690, 880, 22, '#8A6A40'); vinheta(g, 0.5);
  };
  CENARIOS.quarto_coronel = (g, t, c = {}) => { // quarto do coronel: papel de parede, relógio de parede (c.hora = [h,m]), cama com o coronel; c.grita, c.luta (sombras), c.lencol (corpo coberto)
    vgrad(g, 0, 1240, '#6A5030', '#3A2A18'); for (let x = 0; x < W; x += 90) rect(g, x, 0, 30, 1240, 'rgba(0,0,0,0.12)'); rect(g, 0, 1240, W, H - 1240, '#241810'); for (let y = 1280; y < H; y += 90) rect(g, 0, y, W, 3, '#150E08'); rect(g, 0, 900, W, 14, '#2A1A0E');
    const cx = 200, cy = 520, hh = (c.hora?.[0] ?? 11) % 12, mm = c.hora?.[1] ?? 50; circ(g, cx, cy, 120, '#2A1A0E'); circ(g, cx, cy, 108, '#E8DCB8'); for (let i = 0; i < 12; i++) { const a = i / 12 * Math.PI * 2; line(g, cx + Math.sin(a) * 90, cy - Math.cos(a) * 90, cx + Math.sin(a) * 102, cy - Math.cos(a) * 102, '#2A1A0E', 5); }
    const am = mm / 60 * Math.PI * 2, ah = (hh + mm / 60) / 12 * Math.PI * 2; line(g, cx, cy, cx + Math.sin(am) * 84, cy - Math.cos(am) * 84, '#2A1A0E', 6); line(g, cx, cy, cx + Math.sin(ah) * 56, cy - Math.cos(ah) * 56, '#2A1A0E', 9); rect(g, cx - 6, cy + 120, 12, 200, '#2A1A0E'); circ(g, cx, cy + 300 + Math.sin(t * 3.1) * 0, 32, '#8A6A3A'); const ps = Math.sin(t * Math.PI) * 24; circ(g, cx + ps, cy + 320, 26, '#B8924C'); line(g, cx, cy + 130, cx + ps, cy + 320, '#8A6A3A', 5);
    rect(g, 760, 360, 230, 360, '#1A100A'); vgrad(g, 376, 704, c.dia ? '#B8C8D8' : '#1A2038', c.dia ? '#E8E0C8' : '#0E1224', 776, 198); rect(g, 868, 376, 8, 328, '#1A100A');
    rect(g, 360, 1010, 640, 230, '#E8DCC0'); rect(g, 330, 760, 36, 480, '#2A1A0E'); rect(g, 330, 760, 36, 30, '#8A6A3A'); rect(g, 980, 960, 34, 280, '#2A1A0E'); rrect(g, 380, 940, 280, 80, 30, '#F2EAD4'); // cama
    if (!c.luta) {
      if (c.lencol) { poly(g, [[380, 1030], [660, 940], [980, 1000], [1000, 1240], [370, 1240]], '#F6F0DE'); poly(g, [[420, 1040], [660, 960], [900, 1010], [900, 1030], [660, 990], [420, 1070]], 'rgba(0,0,0,0.08)'); }
      else { circ(g, 520, 960, 80, '#D8B890'); g.fillStyle = '#E8E4DA'; g.beginPath(); g.arc(520, 940, 86, Math.PI, Math.PI * 2); g.fill(); rect(g, 440, 930, 30, 60, '#E8E4DA'); rect(g, 570, 930, 30, 60, '#E8E4DA'); // cabelo branco
        g.fillStyle = '#E8E4DA'; g.beginPath(); g.ellipse(500, 1005, 28, 12, 0.15, 0, Math.PI * 2); g.ellipse(542, 1005, 28, 12, -0.15, 0, Math.PI * 2); g.fill(); line(g, 478, 962, 506, 958 + (c.grita ? 6 : 0), '#2A1A0E', 6); line(g, 540, 958 + (c.grita ? 6 : 0), 570, 962, '#2A1A0E', 6);
        if (c.grita) { const mo = 14 + 8 * Math.abs(Math.sin(t * 12)); g.fillStyle = '#3A1410'; g.beginPath(); g.ellipse(522, 1028, 26, mo, 0, 0, Math.PI * 2); g.fill(); line(g, 440, 880, 400, 860, '#F2EAD4', 4, 0.6); line(g, 600, 880, 640, 860, '#F2EAD4', 4, 0.6); } else line(g, 495, 1040, 548, 1040, '#6A4A38', 5);
        poly(g, [[390, 1060], [660, 1040], [900, 1090], [900, 1240], [390, 1240]], '#CFC4A6'); if (c.grita) { line(g, 640, 1060, 700, 880 - 20 * Math.abs(Math.sin(t * 9)), '#D8B890', 38); circ(g, 700, 868 - 20 * Math.abs(Math.sin(t * 9)), 30, '#D8B890'); } } // braço e punho erguidos
    } else { g.save(); g.fillStyle = '#0A0604'; g.globalAlpha = 0.92; const sh = Math.sin(t * 14) * 14; for (const [x, y, r] of [[560 + sh, 560, 100], [800 - sh, 600, 92]]) { g.beginPath(); g.ellipse(x, y, r * 0.9, r, 0, 0, Math.PI * 2); g.fill(); } poly(g, [[440 + sh, 660], [680 + sh, 640], [700, 940], [420, 940]], '#0A0604'); poly(g, [[700 - sh, 700], [940 - sh, 680], [960, 940], [700, 940]], '#0A0604'); g.lineCap = 'round'; g.strokeStyle = '#0A0604'; g.lineWidth = 40; g.beginPath(); g.moveTo(660 + sh, 700); g.lineTo(760, 660 + sh); g.stroke(); g.restore(); // sombras que lutam na parede (nada é mostrado)
      rrect(g, 120, 1190, 120, 50, 18, '#8A6A3A'); rrect(g, 190, 1175, 70, 22, 8, '#8A6A3A'); } // moringa caída
    const lz = 0.9 + 0.1 * Math.sin(t * 8); rect(g, 880, 1012, 24, 40, '#E8DCC0'); chamaC(g, 892, 1012, t); glow(g, 892, 980, 560 * lz, '#FFB45A', 0.2); vinheta(g, 0.6);
  };
  const chamaC = (g, x, y, t) => { const f = 1 + 0.12 * Math.sin(t * 13); glow(g, x, y - 18, 110 * f, '#FFB45A', 0.5); g.fillStyle = '#FF9A2E'; g.beginPath(); g.moveTo(x, y - 52 * f); g.quadraticCurveTo(x + 18, y - 12, x, y + 4); g.quadraticCurveTo(x - 18, y - 12, x, y - 52 * f); g.fill(); g.fillStyle = '#FFE9A8'; g.beginPath(); g.moveTo(x, y - 28 * f); g.quadraticCurveTo(x + 8, y - 8, x, y + 2); g.quadraticCurveTo(x - 8, y - 8, x, y - 28 * f); g.fill(); };
  CENARIOS.tumulo = (g, t, c = {}) => { // cemitério da vila: túmulo de mármore com cruz, ciprestes
    vgrad(g, 0, 1100, '#5A4A32', '#D8B880'); glow(g, 220, 880, 600, '#FFE0A0', 0.3); rect(g, 0, 1060, W, 180, '#4A3A22'); rect(g, 0, 1240, W, H - 1240, '#3A2C18');
    for (const x of [90, 960]) { poly(g, [[x, 380], [x + 60, 1100], [x - 60, 1100]], '#1E2A18'); rect(g, x - 8, 1100, 16, 70, '#2A1A0E'); }
    for (const [x, y] of [[300, 1070], [820, 1060]]) { rect(g, x - 5, y - 130, 10, 130, '#3A2C18'); rect(g, x - 36, y - 100, 72, 10, '#3A2C18'); }
    rect(g, 340, 940, 400, 300, '#E8E2D4'); rect(g, 320, 1200, 440, 60, '#CFC8B8'); rect(g, 340, 940, 400, 24, '#F6F2E8'); rect(g, 340, 960, 400, 8, 'rgba(0,0,0,0.12)'); rect(g, 520, 700, 40, 250, '#E8E2D4'); rect(g, 460, 760, 160, 40, '#E8E2D4'); poly(g, [[340, 964], [740, 964], [740, 1240], [340, 1240]], 'rgba(120,100,70,0.12)');
    for (let i = 0; i < 5; i++) circ(g, 380 + i * 80, 940 + (i % 2) * 6, 14, '#F6F0DE'); vinheta(g, 0.5);
  };

  // ───────── CURUPIRA (verde-floresta) ─────────
  const tronco = (g, x, w, cor, topo = 0) => { rect(g, x - w / 2, topo, w, 1260 - topo, cor); for (let k = 0; k < 4; k++) line(g, x - w / 3 + k * w / 4, topo, x - w / 3 + k * w / 4 + 6, 1240, 'rgba(0,0,0,0.25)', 4); };
  const pegada = (g, x, y, s, toesBaixo, cor = '#0A1A10', realce = false) => { // pegada de pé nu; toesBaixo = dedos virados para baixo (para trás, vista de quem segue)
    const d = toesBaixo ? 1 : -1; g.fillStyle = cor; g.beginPath(); g.ellipse(x, y, 26 * s, 52 * s, 0, 0, Math.PI * 2); g.fill(); g.beginPath(); g.ellipse(x - 2 * s, y - d * 58 * s, 22 * s, 18 * s, 0, 0, Math.PI * 2); g.fill();
    for (let i = 0; i < 5; i++) { g.beginPath(); g.arc(x - 26 * s + i * 13 * s, y + d * (62 + Math.abs(i - 2) * 5) * s, (7 - i * 0.3) * s, 0, Math.PI * 2); g.fill(); } if (realce) { g.strokeStyle = '#7CFFA8'; g.lineWidth = 3 * s; g.beginPath(); g.ellipse(x, y + d * 62 * s, 44 * s, 18 * s, 0, 0, Math.PI * 2); g.stroke(); }
  };
  CENARIOS.mata_noite = (g, t, c = {}) => { // floresta ao entardecer; c.clareira, c.galho (galho com criança em cima), c.pegadas = [x,y,esc,toesBaixo]
    const e = c.noite ? 0 : 1; vgrad(g, 0, 1000, '#06140C', c.noite ? '#0E2A1A' : '#2A5A34'); if (e) glow(g, 820, 520, 700, '#FFB45A', 0.22); if (c.clareira) glow(g, 540, 860, 520, '#E8FFB0', 0.35);
    for (const [x, w, col] of [[120, 120, '#0C1E12'], [330, 90, '#10281A'], [760, 100, '#10281A'], [980, 130, '#0C1E12'], [540, 60, '#14301F']]) tronco(g, x + 10 * Math.sin(t * 0.5 + x), w, col);
    for (let i = 0; i < 40; i++) { const x = rnd(i) * W, y = 1000 + rnd(i + 7) * 260; line(g, x, y, x + 20 + 10 * Math.sin(t + i), y - 70 - rnd(i + 3) * 60, '#1A4A28', 8, 0.8); }
    rect(g, 0, 1240, W, H - 1240, '#0B1D12'); vgrad(g, 1240, H, '#10281A', '#06100A'); rect(g, 0, 1030, W, 210, 'rgba(180,230,190,0.07)');
    if (c.galho) { rect(g, 260, 700, 760, 40, '#1A0E08'); rect(g, 560, 740, 30, 100, '#1A0E08'); for (let k = 0; k < 6; k++) circ(g, 300 + k * 120, 690 + Math.sin(k) * 10, 40, '#14301F'); }
    for (const [x, y, s, tb] of c.pegadas || []) pegada(g, x, y, s, tb, 'rgba(190,225,160,0.5)', c.realce);
    vinheta(g, 0.55);
  };
  CENARIOS.pegadas_close = (g, t, c = {}) => { // chão de lama visto de perto; c.reverso (dedos para trás), c.duas (duas trilhas), c.realce
    vgrad(g, 0, H, '#5A4A30', '#2A200F'); for (let i = 0; i < 160; i++) circ(g, rnd(i) * W, rnd(i + 9) * H, 3 + rnd(i + 3) * 8, 'rgba(0,0,0,0.22)'); for (let i = 0; i < 40; i++) line(g, rnd(i + 50) * W, 1100 + rnd(i + 2) * 800, rnd(i + 50) * W + 8, 1030 + rnd(i + 2) * 700, '#2A5A34', 7, 0.7);
    const xs = c.duas ? [330, 760] : [540]; xs.forEach((x, k) => [0, 1, 2].forEach(i => pegada(g, x + (i % 2 ? 40 : -40), 520 + i * 360 + k * 90, 1.9, !!c.reverso, '#120A04', c.realce))); glow(g, 540, 900, 760, '#E8FFB0', 0.12); vinheta(g, 0.6);
  };

  // ───────── CRIANÇA PEDE CARONA (vermelho de lanterna, chuva) ─────────
  const chuvaR = (g, t, n = 160, a = 0.3) => { g.save(); g.strokeStyle = '#B8C8E8'; g.lineWidth = 3; g.lineCap = 'round'; for (let i = 0; i < n; i++) { const sp = 1700 + rnd(i + 1) * 600, y = ((rnd(i + 2) * (H + 200) + t * sp) % (H + 200)) - 100, x = rnd(i) * (W + 200) - 60 - y * 0.1; g.globalAlpha = a * (0.4 + rnd(i + 3)); g.beginPath(); g.moveTo(x, y); g.lineTo(x - 8, y + 54); g.stroke(); } g.restore(); };
  CENARIOS.volante_pov = (g, t, c = {}) => { // pelo para-brisa à noite na chuva; c.retro = retrovisor (c.menino = menino no banco, c.vazio = banco molhado), c.passageiro = silhueta pequena ao lado
    fundoGrad(g, '#05070C', '#101828'); const vx = 540, vy = 780; poly(g, [[vx - 40, vy], [vx + 40, vy], [W + 400, 1500], [-400, 1500]], '#0C121C'); for (let i = 0; i < 9; i++) { const k = ((t * 0.9 + i / 9) % 1), y = lerp(vy, 1480, Math.pow(k, 2.2)), w = lerp(4, 44, Math.pow(k, 2.2)); rect(g, vx - w / 2, y, w, lerp(8, 90, Math.pow(k, 2.2)), '#D8D8C8', 0.7); }
    for (const sg of [-1, 1]) for (let i = 0; i < 6; i++) { const k = ((t * 0.5 + i / 6) % 1), y = lerp(vy, 1300, Math.pow(k, 2.2)), x = vx + sg * lerp(70, 900, Math.pow(k, 2.2)); rect(g, x - 4, y - lerp(20, 300, Math.pow(k, 2.2)), 8 * (1 + k), lerp(20, 300, Math.pow(k, 2.2)), '#02040A'); circ(g, x, y - lerp(10, 170, Math.pow(k, 2.2)), lerp(3, 16, Math.pow(k, 2.2)), '#E03A3A', 0.9); }
    glow(g, vx, vy + 60, 520, '#E8E8C8', 0.22); poly(g, [[vx - 30, vy + 10], [vx + 30, vy + 10], [vx + 560, 1500], [vx - 560, 1500]], '#E8E8C8', 0.05); chuvaR(g, t, 180, 0.32);
    const sw = Math.sin(t * 2.6) * 0.9; for (const bx of [380, 740]) { g.save(); g.translate(bx, 1420); g.rotate(-0.2 + sw * 0.8); g.strokeStyle = '#02040A'; g.lineWidth = 9; g.lineCap = 'round'; g.beginPath(); g.moveTo(0, 0); g.lineTo(0, -460); g.stroke(); g.restore(); }
    rect(g, 0, 1380, W, H - 1380, '#05070C'); rect(g, 0, 1370, W, 14, '#1A2236'); circ(g, 540, 1980, 560, '#0A0E18'); circ(g, 540, 1980, 560, '#E03A3A', 0.0); g.strokeStyle = '#1E2638'; g.lineWidth = 46; g.beginPath(); g.arc(540, 1990, 540, Math.PI * 1.12, Math.PI * 1.88); g.stroke(); circ(g, 140, 1480, 10, '#E03A3A'); circ(g, 190, 1480, 10, '#E8B03A'); glow(g, 160, 1480, 140, '#E03A3A', 0.3);
    rrect(g, 340, 70, 400, 150, 24, '#02040A'); if (c.retro) { g.save(); g.beginPath(); g.roundRect(352, 82, 376, 126, 16); g.clip(); rect(g, 352, 82, 376, 126, '#202A3C'); rect(g, 430, 96, 220, 110, '#3A4660'); rect(g, 430, 96, 220, 20, '#4A5670'); for (let i = 0; i < 14; i++) circ(g, 440 + rnd(i) * 200, 120 + rnd(i + 4) * 80, 2.5, '#9AB0D8', 0.5);
      if (c.menino) { circ(g, 540, 150, 34, '#E0D8D0'); circ(g, 528, 146, 5, '#0A0E16'); circ(g, 552, 146, 5, '#0A0E16'); poly(g, [[470, 206], [610, 206], [590, 176], [490, 176]], '#8AA0C8'); g.fillStyle = '#1A1410'; g.beginPath(); g.arc(540, 140, 38, Math.PI, Math.PI * 2); g.fill(); } g.restore(); }
    if (c.passageiro) { const a = clamp(t / 1.2); g.save(); g.globalAlpha = a; g.fillStyle = '#02040A'; g.beginPath(); g.ellipse(930, 1290, 50, 58, 0, 0, Math.PI * 2); g.fill(); poly(g, [[870, 1340], [990, 1340], [1020, 1500], [850, 1500]], '#02040A'); g.restore(); }
    vinheta(g, 0.55);
  };
  CENARIOS.estrada_chuva = (g, t, c = {}) => { // BR na curva, chuva, faróis vindos da esquerda; c.menino (acenando em x ~ 0.72)
    fundoGrad(g, '#05070C', '#0E1626'); poly(g, [[-200, 1240], [1280, 1240], [1280, 1900], [-200, 1900]], '#0A101A'); poly(g, [[0, 1100], [W, 980], [W, 1240], [0, 1240]], '#0C121C'); for (let i = 0; i < 6; i++) rect(g, i * 190, 1110 - i * 14, 100, 10, '#D8D8C8', 0.5); rect(g, 0, 1050, W, 14, '#3A4A5A'); for (let i = 0; i < 9; i++) { rect(g, i * 130 + 20, 1040, 14, 80, '#2A3A4A'); circ(g, i * 130 + 27, 1070, 8, '#E03A3A', 0.9); }
    poly(g, [[-100, 1160], [W, 760], [W, 1240], [-100, 1240]], '#E8E8C8', 0.1); glow(g, 40, 1160, 520, '#E8E8C8', 0.3); for (let k = 0; k < 4; k++) rect(g, 150 + k * 280, 700 + k * 40, 8, 340, '#02040A'); chuvaR(g, t, 200, 0.34); vinheta(g, 0.55);
  };
  CENARIOS.portao_cemiterio = (g, t, c = {}) => { // portão de ferro enorme e enferrujado; c.manha = amanhecer cinza-azulado com o carro parado (faróis acesos, porta aberta)
    const m = c.manha ? 1 : 0; vgrad(g, 0, 1240, m ? '#7A8AA0' : '#060810', m ? '#C8D0DC' : '#1A2236'); rect(g, 0, 1240, W, H - 1240, m ? '#3A4250' : '#0A0E18'); rect(g, 0, 1000, 260, 240, m ? '#5A6272' : '#0A0E18'); rect(g, W - 260, 1000, 260, 240, m ? '#5A6272' : '#0A0E18'); rect(g, 40, 560, 160, 560, m ? '#4A5262' : '#080C14'); rect(g, W - 200, 560, 160, 560, m ? '#4A5262' : '#080C14'); poly(g, [[30, 560], [120, 480], [210, 560]], m ? '#3A4252' : '#05070C'); poly(g, [[W - 210, 560], [W - 120, 480], [W - 30, 560]], m ? '#3A4252' : '#05070C');
    for (let i = 0; i < 18; i++) { const x = 220 + i * 38; rect(g, x, 640 + Math.abs(i - 9) * 8, 10, 600 - Math.abs(i - 9) * 8, '#2A1E18'); rect(g, x - 2, 630 + Math.abs(i - 9) * 8, 14, 22, '#4A2A1A'); } rect(g, 220, 700, 680, 14, '#2A1E18'); rect(g, 220, 1120, 680, 14, '#2A1E18'); g.strokeStyle = '#2A1E18'; g.lineWidth = 12; g.beginPath(); g.arc(540, 700, 330, Math.PI, Math.PI * 2); g.stroke();
    for (let i = 0; i < 40; i++) rect(g, 232 + rnd(i) * 660, 700 + rnd(i + 4) * 520, 10 + rnd(i) * 20, 4, 'rgba(160,80,30,0.55)'); for (const [x, y] of [[420, 520], [660, 480]]) { rect(g, x - 5, y - 70, 10, 70, '#0A0E18'); rect(g, x - 26, y - 52, 52, 8, '#0A0E18'); }
    rect(g, 0, 1060, W, 160, m ? 'rgba(220,230,240,0.35)' : 'rgba(120,140,190,0.12)'); if (m) { const k = Motor.H_.carro; k(g, 330, 1500, 0.9, '#B8BCC8', true); rect(g, 280, 1330, 6, 6, '#fff'); glow(g, 640, 1380, 200, '#FFF0B0', 0.5); } chuvaR(g, t, m ? 0 : 140, 0.28); vinheta(g, 0.55);
  };

  // ───────── CUCA (prata-azulada) ─────────
  CENARIOS.quarto_lua = (g, t, c = {}) => { // quarto de criança; c.jan 0..1 (janela aberta), c.vulto 0..1 (a Cuca na janela), c.olhos 'abertos'|'fechados', c.escamas, c.manha
    const m = c.manha ? 1 : 0; vgrad(g, 0, 1240, m ? '#A0A8B8' : '#2A3450', m ? '#6A7084' : '#141A2C'); rect(g, 0, 1240, W, H - 1240, m ? '#4A4458' : '#0C101C'); for (let y = 1280; y < H; y += 90) rect(g, 0, y, W, 3, 'rgba(0,0,0,0.3)');
    const wx = 560, wy = 260, ww = 400, wh = 560; rect(g, wx - 24, wy - 24, ww + 48, wh + 48, '#0A0E1A'); vgrad(g, wy, wy + wh, m ? '#E8E0C8' : '#0A1228', m ? '#F8E8C0' : '#2A3A68', wx, ww); if (!m) { circ(g, wx + 280, wy + 150, 70, '#E8EEFF'); circ(g, wx + 300, wy + 135, 62, '#0F1838', 0.0); glow(g, wx + 280, wy + 150, 360, '#C8D8FF', 0.3); }
    if (c.vulto && !m) { const a = clamp(c.vulto), s = 0.7 + 0.5 * a; g.save(); g.globalAlpha = a; g.translate(wx + ww / 2, wy + wh); g.scale(s, s); g.fillStyle = '#04060C'; g.beginPath(); g.ellipse(0, -150, 120, 150, 0, 0, Math.PI * 2); g.fill(); poly(g, [[-30, -230], [-230, -190], [-240, -150], [-30, -130]], '#04060C'); for (let i = 0; i < 6; i++) poly(g, [[-60 - i * 28, -190 + i * 1], [-48 - i * 28, -168], [-72 - i * 28, -168]], '#E8EEFF'); circ(g, -10, -250, 16, '#E8E060'); circ(g, -10, -250, 7, '#04060C'); for (let i = 0; i < 7; i++) line(g, 40 + i * 14, -300, 90 + i * 22, -200 + i * 24, '#04060C', 9); poly(g, [[-100, -40], [100, -40], [180, 60], [-180, 60]], '#04060C'); g.restore(); }
    const op = c.jan ? out(clamp(c.jan)) : 0, sash = op * 300; rect(g, wx + ww / 2 - 6, wy, 12, wh, '#0A0E1A'); rect(g, wx, wy + wh / 2 - 6, ww, 12, '#0A0E1A'); if (op < 0.98) rect(g, wx, wy, ww / 2 + 6, wh, 'rgba(10,14,26,0.0)'); poly(g, [[wx - 24, wy - 30], [wx + 70, wy - 30], [wx + 60 - op * 40, wy + wh + 40], [wx - 24, wy + wh + 40]], m ? '#8A7AA0' : '#3A4676'); poly(g, [[wx + ww + 24, wy - 30], [wx + ww - 70, wy - 30], [wx + ww - 60 + op * 40, wy + wh + 40], [wx + ww + 24, wy + wh + 40]], m ? '#8A7AA0' : '#3A4676'); void sash;
    if (!m) poly(g, [[wx, wy + wh], [wx + ww, wy + wh], [wx + ww + 200, 1500], [wx - 300, 1500]], '#C8D8FF', 0.07);
    rect(g, 40, 1000, 520, 240, m ? '#6A5A6A' : '#1A2038'); rect(g, 20, 900, 30, 340, '#0A0E1A'); rrect(g, 70, 950, 260, 80, 34, m ? '#F2EEE8' : '#CFD8EC', 0.9); const hx = 200; circ(g, hx, 975, 70, '#D8B890'); g.fillStyle = '#3A2A22'; g.beginPath(); g.arc(hx, 968, 74, Math.PI, Math.PI * 2); g.fill();
    if (c.olhos === 'abertos') for (const dx of [-24, 24]) { circ(g, hx + dx, 982, 15, '#FFF'); circ(g, hx + dx + 3, 984, 6, '#10140F'); line(g, hx + dx - 14, 958, hx + dx + 12, 954, '#2A1E18', 5); } else for (const dx of [-24, 24]) line(g, hx + dx - 14, 984, hx + dx + 14, 984, '#2A1E18', 5); line(g, hx - 12, 1022, hx + 12, 1022, '#6A4038', 5);
    poly(g, [[110, 1040], [320, 1030], [560, 1060], [560, 1240], [100, 1240]], m ? '#CFC8D8' : '#5A6A9A'); if (c.escamas) { for (let r = 0; r < 4; r++) for (let k = 0; k < 6; k++) { g.strokeStyle = 'rgba(40,50,30,0.55)'; g.lineWidth = 3; g.beginPath(); g.arc(160 + k * 60 + (r % 2) * 30, 1100 + r * 30, 20, 0, Math.PI); g.stroke(); } for (let i = 0; i < 6; i++) circ(g, 200 + i * 55, 1190 + (i % 2) * 18, 10, 'rgba(60,50,30,0.5)'); }
    if (m) glow(g, wx + ww / 2, wy + wh / 2, 800, '#FFE0A0', 0.35); vinheta(g, m ? 0.35 : 0.55);
  };
  POSES.avoSenta = t => ({ al: [52, 160], ar: [-52, 160], fl: [0, 0], fr: [0, 0], olho: 'meio', boca: 'pequena', sobr: 0.2, sentado: true });
})();
