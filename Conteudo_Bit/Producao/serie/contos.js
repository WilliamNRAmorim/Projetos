// Cenários, poses e objetos extras dos Shorts de terror (Dia 1). Só ACRESCENTA ao Motor; nenhum cenário/pose/objeto antigo é alterado.
(() => {
  const { CENARIOS, POSES, OBJETOS, W, H, GY } = Motor, { rect, poly, circ, line, rrect, text, glow, vgrad, rgba, vinheta, rnd, lerp, clamp, out } = Motor.H_;
  const chama = (g, x, y, s, t, seed = 0) => { // chama de vela/lampião: gota com tremida
    const f = 1 + 0.12 * Math.sin(t * 13 + seed * 7) + 0.07 * Math.sin(t * 29 + seed), dx = 3 * Math.sin(t * 9 + seed * 3);
    glow(g, x, y - 20 * s, 150 * s * f, '#FFB45A', 0.5);
    g.fillStyle = '#FF9A2E'; g.beginPath(); g.moveTo(x, y - 62 * s * f); g.quadraticCurveTo(x + 24 * s + dx, y - 14 * s, x, y + 6 * s); g.quadraticCurveTo(x - 24 * s + dx, y - 14 * s, x, y - 62 * s * f); g.fill();
    g.fillStyle = '#FFE9A8'; g.beginPath(); g.moveTo(x, y - 34 * s * f); g.quadraticCurveTo(x + 11 * s, y - 10 * s, x, y + 3 * s); g.quadraticCurveTo(x - 11 * s, y - 10 * s, x, y - 34 * s * f); g.fill();
  };
  const vela = (g, x, y, h, t, seed) => { rrect(g, x - 14, y - h, 28, h, 4, '#E8DFC8'); rect(g, x - 14, y - h, 28, 8, '#CFC4A6'); line(g, x, y - h, x, y - h - 10, '#241812', 3); chama(g, x, y - h - 8, 0.8, t, seed); };
  const fundoGrad = (g, a, b) => vgrad(g, 0, H, a, b);

  // ───────── genérico: fundo de uma cor com brilho (closes) ─────────
  CENARIOS.fundo_cor = (g, t, c = {}) => { fundoGrad(g, c.topo || '#2A0E18', c.base || '#14060B'); glow(g, W / 2, c.brilhoY || 800, 900, c.brilho || '#8E2F4B', 0.3 + 0.04 * Math.sin(t * 1.3)); rect(g, 0, 1240, W, H - 1240, 'rgba(0,0,0,0.35)'); vinheta(g, 0.55); };

  // ───────── A CAUSA SECRETA (bordô) ─────────
  CENARIOS.rio_rua = (g, t, c = {}) => { // rua do Rio antigo à noite, casarões, lampião a gás; c.porta = casa de saúde com a porta acesa
    fundoGrad(g, '#12060C', '#3A1222'); circ(g, 880, 260, 70, '#6A3A4A', 0.5); circ(g, 905, 244, 62, '#1C0A12', 0.9);
    const prd = [[-20, 640, 300, '#2A0F1B'], [250, 540, 260, '#341424'], [490, 690, 330, '#2A0F1B'], [800, 600, 320, '#381727']];
    prd.forEach(([x, y, w, col], i) => { rect(g, x, y, w, 1240 - y, col); poly(g, [[x - 14, y], [x + w / 2, y - 90], [x + w + 14, y]], '#1B0A12'); // telhado
      for (let j = 0; j < 2; j++) for (let k = 0; k < 2; k++) { const wx = x + 34 + j * (w / 2 - 20), wy = y + 70 + k * 190, ac = rnd(i * 9 + j * 3 + k) > 0.72; rect(g, wx, wy, 70, 110, ac ? '#C9873E' : '#12060C'); if (ac) glow(g, wx + 35, wy + 55, 120, '#FFB45A', 0.22); rect(g, wx - 6, wy - 6, 82, 6, '#4A2234'); } });
    if (c.porta) { rect(g, 560, 700, 340, 540, '#3A1626'); rect(g, 610, 760, 190, 480, '#F2B36B'); glow(g, 705, 1000, 420, '#FFB45A', 0.4); rect(g, 600, 750, 12, 490, '#1B0A12'); rect(g, 798, 750, 12, 490, '#1B0A12'); rect(g, 600, 744, 210, 12, '#1B0A12'); }
    rect(g, 0, 1240, W, H - 1240, '#1A0B12'); rect(g, 0, 1240, W, 54, '#3A1B28'); // calçada
    for (let r = 0; r < 14; r++) for (let k = -1; k < 12; k++) { const y = 1300 + r * 46, o = (r % 2) * 48, x = k * 96 + o - (r * 6); rrect(g, x, y, 90, 40, 12, r % 3 ? '#26101A' : '#2E1521'); }
    rect(g, 168, 560, 16, 680, '#0D0508'); rect(g, 140, 1210, 72, 34, '#0D0508'); rect(g, 140, 520, 72, 54, '#0D0508'); rect(g, 148, 530, 56, 36, '#FFD79A', 0.9 - 0.12 * Math.abs(Math.sin(t * 11)));
    glow(g, 176, 548, 300, '#FFB45A', 0.32); poly(g, [[150, 580], [200, 580], [520, 1300], [-150, 1300]], '#FFB45A', 0.06);
    rect(g, 0, 1100, W, 180, 'rgba(120,50,70,0.10)'); vinheta(g, 0.55);
  };
  CENARIOS.gabinete = (g, t, c = {}) => { // gabinete da casa de saúde: parede bordô, frascos, mesa com vela. c.sombra = sombra gigante na parede (nunca o bicho); c.fresta = visto pela fresta da porta
    fundoGrad(g, '#2C0F1B', '#180810'); rect(g, 0, 880, W, 360, '#3A1626'); rect(g, 0, 870, W, 14, '#12060C'); rect(g, 0, 1240, W, H - 1240, '#12060C');
    for (let s = 0; s < 3; s++) { rect(g, 80, 360 + s * 150, 330, 12, '#12060C'); for (let j = 0; j < 5; j++) { const hh = 60 + rnd(s * 5 + j) * 36; rrect(g, 100 + j * 62, 360 + s * 150 - hh, 44, hh, 8, '#5A2A38'); rect(g, 108 + j * 62, 360 + s * 150 - hh - 10, 28, 10, '#C9B38A'); } } // frascos
    rect(g, 700, 330, 260, 330, '#0C0508'); rect(g, 712, 342, 236, 306, '#241830'); // janela
    rect(g, 270, 1060, 700, 36, '#4A2230'); rect(g, 300, 1096, 640, 150, '#2A111C'); rect(g, 320, 1230, 40, 20, '#0C0508'); rect(g, 880, 1230, 40, 20, '#0C0508'); // mesa
    const fx = 640, fy = 1060; vela(g, fx, fy, 70, t, 2);
    if (c.sombra) { const k = 0.8 + 0.06 * Math.sin(t * 8); g.save(); g.globalAlpha = 0.85; g.fillStyle = '#07030A'; const sx = 640, sy = 700; // sombra de um homem de perfil, braço erguido segurando um fio
      g.beginPath(); g.ellipse(sx - 150, sy - 150, 82 * k, 96 * k, 0, 0, Math.PI * 2); g.fill(); g.beginPath(); g.moveTo(sx - 300, sy + 30); g.quadraticCurveTo(sx - 150, sy - 70, sx + 10, sy + 30); g.lineTo(sx + 60, sy + 330); g.lineTo(sx - 360, sy + 330); g.closePath(); g.fill();
      g.lineCap = 'round'; g.strokeStyle = '#07030A'; g.lineWidth = 46; g.beginPath(); g.moveTo(sx - 30, sy + 40); g.lineTo(sx + 130, sy - 70); g.lineTo(sx + 205, sy + 90); g.stroke(); g.restore(); // fio: sai da mão e desce por trás da mesa
      line(g, 830, 840, 830, 1060, '#07030A', 4, 0.9); }
    glow(g, fx, fy - 40, 640, '#FFB45A', 0.2); poly(g, [[fx - 40, fy], [fx + 40, fy], [fx + 300, 1240], [fx - 300, 1240]], '#FFB45A', 0.05);
    if (c.fresta) { rect(g, 0, 0, 230, H, '#050204'); rect(g, W - 190, 0, 190, H, '#050204'); rect(g, 230, 0, 14, H, '#4A2230'); rect(g, W - 204, 0, 14, H, '#4A2230'); }
    vinheta(g, 0.6);
  };
  CENARIOS.velorio = (g, t, c = {}) => { // sala do velório: cortinas pretas, velas, caixão (c.semCaixao), porta ao fundo (c.porta)
    fundoGrad(g, '#1A0810', '#2C101C'); rect(g, 0, 1240, W, H - 1240, '#10050A'); rect(g, 0, 1236, W, 8, '#4A2234');
    for (const [x0, dir] of [[0, 1], [W, -1]]) { for (let i = 0; i < 4; i++) poly(g, [[x0 + dir * i * 70, 0], [x0 + dir * (i * 70 + 80), 0], [x0 + dir * (i * 70 + 60 + 14 * Math.sin(t + i)), 1240], [x0 + dir * (i * 70 - 10), 1240]], i % 2 ? '#0A0407' : '#120609'); }
    if (c.porta) { rect(g, 800, 560, 190, 680, '#0A0407'); rect(g, 814, 580, 162, 660, '#E0A25A', 0.9); glow(g, 895, 900, 380, '#FFB45A', 0.3); }
    [[230, 1236], [850, 1236]].forEach(([x, y], i) => { rect(g, x - 8, y - 520, 16, 520, '#8A7448'); rect(g, x - 40, y - 24, 80, 24, '#8A7448'); rect(g, x - 52, y - 540, 104, 16, '#8A7448'); vela(g, x - 28, y - 540, 56, t, i); vela(g, x + 28, y - 540, 56, t, i + 3); }); // castiçais
    if (!c.semCaixao) { const bx = 250, by = 1130; rect(g, bx + 30, by + 60, 40, 110, '#0A0407'); rect(g, bx + 560, by + 60, 40, 110, '#0A0407'); rrect(g, bx, by - 10, 640, 80, 14, '#2A140C'); rect(g, bx + 10, by - 10, 620, 12, '#4A2A18'); // caixão de madeira aberto
      rrect(g, bx + 18, by - 60, 604, 62, 8, '#F0EADC'); circ(g, bx + 88, by - 64, 54, '#E8C6A8'); g.fillStyle = '#1C1210'; g.beginPath(); g.ellipse(bx + 70, by - 80, 62, 50, 0, Math.PI, Math.PI * 2); g.fill(); rect(g, bx + 8, by - 76, 26, 70, '#1C1210'); line(g, bx + 74, by - 62, bx + 102, by - 62, '#3A2A24', 4); // cabeça sobre o travesseiro, olhos fechados
      poly(g, [[bx + 150, by - 56], [bx + 590, by - 66], [bx + 600, by - 6], [bx + 150, by - 4]], '#F6F1E6'); for (let i = 0; i < 5; i++) circ(g, bx + 300 + i * 54, by - 52 + (i % 2) * 6, 17, i % 2 ? '#EDE4D3' : '#D8CFBA'); } // lençol e flores brancas
    glow(g, W / 2, 1000, 900, '#FFB45A', 0.12); vinheta(g, 0.62);
  };

  // ───────── BOITATÁ (azul-noite) ─────────
  const estrelas = (g, t, n, ymax) => { for (let i = 0; i < n; i++) circ(g, rnd(i) * W, rnd(i + 77) * ymax, 1.4 + rnd(i + 5) * 2, '#CFE3FF', 0.25 + 0.5 * rnd(i + 9) * (0.6 + 0.4 * Math.sin(t * 1.7 + i))); };
  const boitata = (g, t, k, esc = 1, cx = W / 2, yA = 930, yB = 1600) => { // cobra de fogo azul vindo do fundo (k 0 = horizonte, 1 = em cima da casa); luz, nunca criatura ferida
    const N = 20; for (let i = N - 1; i >= 0; i--) { const s = k - i * 0.03; if (s < 0) continue; const e = Math.pow(clamp(s), 1.5), y = lerp(yA, yB, e), sc = lerp(0.25, 1.7, e) * esc, x = cx + Math.sin(s * 11 + t * 2.4 + i * 0.25) * (260 * lerp(0.2, 1, e)) * esc, a = 1 - i / N * 0.8;
      glow(g, x, y, 150 * sc, '#3F8CFF', 0.35 * a); circ(g, x, y, 34 * sc, '#6FB8FF', 0.75 * a); circ(g, x, y, 18 * sc, '#E8F6FF', 0.95 * a);
      if (i === 0) { glow(g, x, y, 260 * sc, '#4FA8FF', 0.5); circ(g, x, y, 52 * sc, '#8CCBFF', 0.9); circ(g, x - 18 * sc, y - 6 * sc, 9 * sc, '#06122E'); circ(g, x + 18 * sc, y - 6 * sc, 9 * sc, '#06122E'); } } // cabeça com dois olhos escuros
  };
  const capim = (g, t, y0, y1, cor, n = 260) => { for (let i = 0; i < n; i++) { const y = lerp(y0, y1, Math.pow(rnd(i + 3), 1.6)), s = lerp(0.5, 2.2, (y - y0) / (y1 - y0)), x = rnd(i) * W, sw = Math.sin(t * 1.5 + i) * 4 * s; line(g, x, y, x + sw, y - 26 * s, cor, 3 * s, 0.7); } };
  CENARIOS.pasto_noite = (g, t, c = {}) => { // pasto à noite; c.fogo = posição inicial (0..1) da cobra de fogo, c.fogoV = velocidade (k/s); c.casaLonge
    vgrad(g, 0, 940, '#040A1C', '#14306A'); estrelas(g, t, 70, 800); circ(g, 170, 250, 54, '#9DB8E8', 0.25);
    poly(g, [[0, 900], [260, 820], [560, 880], [820, 800], [W, 870], [W, 960], [0, 960]], '#08122B'); poly(g, [[0, 940], [380, 880], [700, 930], [W, 900], [W, 980], [0, 980]], '#0B1A3C');
    vgrad(g, 960, H, '#0A1B38', '#040A18'); capim(g, t, 975, 1900, '#1A3A66');
    for (let i = 0; i < 6; i++) { const y = 1000 + i * 12, x0 = 60 + i * 190; rect(g, x0, y - 60, 14, 80, '#050A16'); } line(g, 0, 985, W, 985, '#050A16', 5); line(g, 0, 1005, W, 1005, '#050A16', 4); // cerca
    if (c.casaLonge) { rect(g, 800, 880, 110, 70, '#0A1226'); poly(g, [[790, 880], [855, 840], [920, 880]], '#050A16'); rect(g, 836, 905, 22, 28, '#F2B35C'); glow(g, 847, 919, 60, '#F2B35C', 0.4); }
    const k = (c.fogo ?? -1) + (c.fogoV || 0) * t;
    if (k >= 0) { boitata(g, t, Math.min(k, 1.15), c.fogoEsc || 1, c.fogoX || W / 2); for (let i = 0; i < 30; i++) { const s = clamp(k) - i * 0.022 - 0.06; if (s < 0) continue; const e = Math.pow(s, 1.5); circ(g, W / 2 + Math.sin(s * 11 + i) * 220 * e, lerp(930, 1600, e) + 14, 3 + 5 * e, '#FF8A2A', 0.5 * (0.4 + 0.6 * Math.abs(Math.sin(t * 6 + i)))); } } // brasas no rastro do capim queimado
    vinheta(g, 0.55);
  };
  CENARIOS.quarto_roca = (g, t, c = {}) => { // quarto da casa de roça: tábuas, cama, janela (c.fogoJ = posição da luz azul lá fora), cortina (c.cortinaT = s para fechar), c.calor 0..1, c.manha
    const m = c.manha ? 1 : 0; vgrad(g, 0, 1240, m ? '#6A5A58' : '#151F3C', m ? '#8A6A58' : '#1C2848');
    for (let x = 0; x < W; x += 90) rect(g, x, 0, 4, 1240, m ? '#4A3A38' : '#0C1328'); rect(g, 0, 1240, W, H - 1240, m ? '#3A2A26' : '#0B1226'); for (let y = 1260; y < H; y += 80) rect(g, 0, y, W, 3, m ? '#241814' : '#070C1A');
    rect(g, 40, 1000, 460, 240, m ? '#5A4A4A' : '#1A2442'); rrect(g, 60, 940, 420, 110, 26, m ? '#9A7A6A' : '#2C3C6A'); rect(g, 40, 880, 30, 360, m ? '#3A2A22' : '#0A1022'); rect(g, 470, 940, 30, 300, m ? '#3A2A22' : '#0A1022'); // cama de roça com colcha
    const wx = 580, wy = 360, ww = 380, wh = 520;
    rect(g, wx - 24, wy - 24, ww + 48, wh + 48, m ? '#3A2A22' : '#090E1E'); vgrad(g, wy, wy + wh, m ? '#F2C98A' : '#06122E', m ? '#FFE3B0' : '#16346E', wx, ww);
    if (!m) { g.save(); g.beginPath(); g.rect(wx, wy, ww, wh); g.clip(); estrelas(g, t, 18, wy + wh); if (c.fogoJ != null) { boitata(g, t, c.fogoJ, 0.3, wx + ww / 2, wy + wh * 0.5, wy + wh * 0.97); } g.restore(); }
    rect(g, wx + ww / 2 - 6, wy, 12, wh, m ? '#3A2A22' : '#090E1E'); rect(g, wx, wy + wh / 2 - 6, ww, 12, m ? '#3A2A22' : '#090E1E');
    const fech = c.cortinaT ? clamp((t - 0.4) / c.cortinaT) : (c.cortina ?? 0), cw = lerp(70, ww / 2 + 24, out(fech)), cor = m ? '#B08A6A' : '#4A3F6E';
    rect(g, wx - 40, wy - 40, ww + 80, 16, '#050A16'); poly(g, [[wx - 40, wy - 28], [wx - 40 + cw, wy - 28], [wx - 40 + cw - 10 + 6 * Math.sin(t * 1.3), wy + wh + 40], [wx - 40, wy + wh + 40]], cor); poly(g, [[wx + ww + 40, wy - 28], [wx + ww + 40 - cw, wy - 28], [wx + ww + 40 - cw + 10 - 6 * Math.sin(t * 1.3), wy + wh + 40], [wx + ww + 40, wy + wh + 40]], cor);
    for (let i = 0; i < 5; i++) { line(g, wx - 40 + i * (cw / 5), wy - 20, wx - 40 + i * (cw / 5) - 6, wy + wh + 30, 'rgba(0,0,0,0.25)', 4); line(g, wx + ww + 40 - i * (cw / 5), wy - 20, wx + ww + 40 - i * (cw / 5) + 6, wy + wh + 30, 'rgba(0,0,0,0.25)', 4); }
    const luz = (c.luz ?? (c.fogoJ != null ? 0.5 : 0.25)) * (0.85 + 0.15 * Math.sin(t * 7)); if (!m) { poly(g, [[wx, wy + wh], [wx + ww, wy + wh], [wx + ww + 200, 1500], [wx - 340, 1500]], '#3F8CFF', 0.12 * luz); glow(g, wx + ww / 2, wy + wh / 2, 560, '#3F8CFF', 0.28 * luz); }
    if (m) { poly(g, [[wx, wy + wh], [wx + ww, wy + wh], [wx + ww + 260, 1500], [wx - 300, 1500]], '#FFE0A0', 0.14); glow(g, wx + ww / 2, wy + wh / 2, 640, '#FFD08A', 0.3); }
    if (c.calor) { const a = c.calor * clamp(t / (c.calorT || 3)); g.save(); g.globalAlpha = 0.34 * a; g.fillStyle = '#FF7A2A'; g.fillRect(0, 0, W, H); g.restore(); glow(g, wx + ww / 2, wy + wh / 2, 800, '#FF8A3A', 0.35 * a); for (let i = 0; i < 6; i++) { g.strokeStyle = `rgba(255,170,90,${0.12 * a})`; g.lineWidth = 6; g.beginPath(); for (let y = 0; y <= H; y += 40) { const x = 80 + i * 190 + Math.sin(y * 0.02 + t * 5 + i) * 14 * a; y ? g.lineTo(x, y) : g.moveTo(x, y); } g.stroke(); } } // calor atravessando a parede
    vinheta(g, 0.55);
  };
  CENARIOS.roca_fora = (g, t, c = {}) => { // casa de roça por fora; c.manha = amanhecer; c.queimado 0..1 = capim queimado até a parede
    const m = c.manha ? 1 : 0; vgrad(g, 0, 980, m ? '#2A4A7A' : '#040A1C', m ? '#F2B07A' : '#14306A'); if (!m) { estrelas(g, t, 60, 700); circ(g, 190, 240, 52, '#9DB8E8', 0.25); } else glow(g, 200, 960, 700, '#FFD08A', 0.5);
    poly(g, [[0, 920], [300, 850], [620, 910], [900, 840], [W, 900], [W, 990], [0, 990]], m ? '#2A3A5A' : '#08122B'); vgrad(g, 980, H, m ? '#3A4A3A' : '#0A1B38', m ? '#1A2A22' : '#040A18'); if (!c.queimado) capim(g, t, 1000, 1900, m ? '#3F6A4A' : '#1A3A66');
    if (c.queimado) { const q = c.queimado; capim(g, t, 1000, 1500, m ? '#3F6A4A' : '#1A3A66', 120); poly(g, [[0, 1500 - 480 * q], [W, 1500 - 480 * q - 60], [W, H], [0, H]], '#07060A', 0.97); for (let i = 0; i < 70; i++) circ(g, rnd(i + 40) * W, 1300 + rnd(i + 11) * 580, 3 + rnd(i) * 4, '#FF6A2A', 0.18 + 0.2 * Math.abs(Math.sin(t * 3 + i))); for (let i = 0; i < 5; i++) { const sx = 160 + i * 200, k = (t * 0.2 + i * 0.3) % 1; circ(g, sx + Math.sin(k * 6 + i) * 30, 1500 - k * 520, 40 + k * 80, '#8A8A96', 0.14 * (1 - k)); } } // fumaça fina e brasas
    const hx = 360, hy = 700, hw = 620; rect(g, hx, hy, hw, 560, m ? '#6A4A46' : '#1C2A4E'); poly(g, [[hx - 50, hy], [hx + hw / 2, hy - 190], [hx + hw + 50, hy]], m ? '#2A1A1A' : '#0A0F20'); for (let i = 0; i < 7; i++) rect(g, hx + 40 + i * 84, hy - 6, 4, 12, 'rgba(0,0,0,0.3)');
    rect(g, hx + 80, hy + 190, 190, 370, '#0A0F20'); rect(g, hx + 92, hy + 202, 166, 358, m ? '#3A2A22' : '#2A1F1C'); rect(g, hx + 380, hy + 120, 170, 190, '#090E1E'); rect(g, hx + 390, hy + 130, 150, 170, m ? '#F2C98A' : (c.luzJanela === false ? '#0B1630' : '#F2B35C'));
    if (!m && c.luzJanela !== false) glow(g, hx + 465, hy + 215, 300, '#F2B35C', 0.35);
    rect(g, hx + 460, hy + 130, 10, 170, '#090E1E'); rect(g, hx + 390, hy + 210, 150, 10, '#090E1E'); rect(g, hx - 30, 1260, hw + 60, 26, m ? '#2A1A1A' : '#050A16'); // soleira
    vinheta(g, 0.5);
  };
  OBJETOS.maos_olhos = (g, o, u) => { // mãos da avó cobrindo os olhos de quem está em (o.x, o.escala); braços vêm de trás (o.lado = 1 direita, -1 esquerda)
    const k = out(clamp(u / 0.35)), e = o.escala || 1, lado = o.lado || 1, cx = o.x * W + 16 * e, cy = GY + (o.y || 0) - 472 * e, sl = o.manga || '#7A5A8A', pele = o.pele || '#B98560';
    g.save(); g.globalAlpha = k; g.translate(lado * (1 - k) * 60, 0);
    for (const dx of [-24, 24]) { const om = o.ombro ? [o.ombro[0] + dx * 1.6, o.ombro[1]] : [cx + lado * 210 * e + dx * e * 1.4, cy + 190 * e]; line(g, cx + dx * e, cy + 4 * e, om[0], om[1], sl, 46 * e); }
    rrect(g, cx - 66 * e, cy - 34 * e, 132 * e, 70 * e, 30 * e, pele); for (let i = 1; i < 4; i++) line(g, cx - 66 * e + i * 33 * e, cy - 24 * e, cx - 66 * e + i * 33 * e, cy + 8 * e, 'rgba(0,0,0,0.18)', 3);
    g.restore();
  };
  // ───────── SEU NOME NA MADRUGADA (verde-musgo acinzentado) ─────────
  CENARIOS.quarto_musgo = (g, t, c = {}) => { // quarto à noite visto dos pés da cama: Lucas (olhos abertos) e a mãe dormindo; c.close = rostos grandes, c.olhar -1..1, c.boca 0..1, c.olhosFechados, c.somenteMae
    vgrad(g, 0, 1240, '#3A4638', '#1E271F'); rect(g, 0, 1240, W, H - 1240, '#10150F'); for (let y = 1270; y < H; y += 84) rect(g, 0, y, W, 3, '#0A0E0A'); rect(g, 0, 1100, W, 14, '#161C16');
    rect(g, 70, 340, 300, 470, '#0B0F0C'); vgrad(g, 360, 790, '#7E9A88', '#4A6454', 90, 260); rect(g, 215, 360, 10, 430, '#0B0F0C'); rect(g, 90, 560, 260, 10, '#0B0F0C'); // janela com lua
    poly(g, [[90, 790], [350, 790], [760, 1250], [-80, 1250]], '#B8C8B0', 0.06 + 0.015 * Math.sin(t * 0.9)); glow(g, 220, 560, 420, '#B8C8B0', 0.12);
    rect(g, 820, 520, 200, 720, '#0A0F0B'); rect(g, 836, 540, 168, 700, '#131A14'); if (c.portaFria) glow(g, 920, 900, 300, '#9DBB8E', 0.18); // porta do corredor
    rect(g, 0, 330, 20, 20, 'rgba(0,0,0,0)'); rect(g, 800, 430, 240, 56, '#2A342B'); rect(g, 806, 436, 228, 44, '#9AA08C', 0.12);
    g.save(); const S = c.close ? 2.15 : 1, cx = c.close ? 480 : 540; g.translate(540, 1010); g.scale(S, S); g.translate(-cx, -1010);
    rect(g, 220, 930, 640, 300, '#1F281F'); rect(g, 200, 880, 40, 360, '#141A14'); rect(g, 840, 880, 40, 360, '#141A14'); rrect(g, 250, 940, 580, 70, 28, '#CDD6C8', 0.55); // cabeceira e travesseiro
    const hx = [400, 660], ey = 980, cabe = (x, who) => { circ(g, x, 978, 74, who ? '#C9AE92' : '#D3B79B'); g.fillStyle = who ? '#2B2018' : '#3A2A22'; g.beginPath(); g.arc(x, 972, 78, Math.PI * 0.95, Math.PI * 2.05); g.fill(); rect(g, x - 82, 960, 22, 70, who ? '#2B2018' : '#3A2A22'); rect(g, x + 60, 960, 22, 70, who ? '#2B2018' : '#3A2A22'); };
    cabe(hx[0], 0); cabe(hx[1], 1);
    const fecha = c.olhosFechados, pis = (Math.floor(t * 0.5) % 5 === 0 && (t * 0.5) % 1 < 0.08);
    for (const dx of [-26, 26]) { // Lucas: olhos abertos, olhando para a porta (olhar > 0) ou para a mãe (olhar < 0)
      if (fecha || pis) line(g, hx[0] + dx - 14, 984, hx[0] + dx + 14, 984, '#2A1E18', 5); else { circ(g, hx[0] + dx, 980, 17, '#F4F4EE'); circ(g, hx[0] + dx + (c.olhar ?? 0.8) * 9, 982, 7, '#10140F'); }
      line(g, hx[1] + dx - 14, 986, hx[1] + dx + 14, 986, '#2A1E18', 5); } // mãe: olhos fechados
    for (const dx of [-26, 26]) { line(g, hx[0] + dx - 14, 950, hx[0] + dx + 12, 946 - (fecha ? 0 : 5), '#2A1E18', 5); }
    const ab = c.boca || 0; if (ab > 0) { g.fillStyle = '#3A1E1E'; g.beginPath(); g.ellipse(hx[0], 1030, 12, 4 + 16 * ab, 0, 0, Math.PI * 2); g.fill(); } else line(g, hx[0] - 12, 1030, hx[0] + 12, 1030, '#6A4038', 5);
    line(g, hx[1] - 10, 1032, hx[1] + 10, 1032, '#6A4038', 5);
    const resp = Math.sin(t * 1.6) * 5; poly(g, [[270, 1070 + resp], [540, 1048 + resp], [830, 1070 + resp], [840, 1240], [260, 1240]], '#4A5A48'); poly(g, [[290, 1070 + resp], [520, 1056 + resp], [540, 1056 + resp], [540, 1240], [280, 1240]], '#56684F', 0.5); rect(g, 260, 1066, 580, 8, '#2E3A2D'); // coberta
    g.restore(); vinheta(g, 0.6);
  };
  CENARIOS.cozinha_musgo = (g, t, c = {}) => { // cozinha escura; c.vulto 0..1 = silhueta alta na porta do corredor (vultoT s para aparecer)
    vgrad(g, 0, 1240, '#2E3A2D', '#1B241C'); for (let y = 140; y < 1000; y += 90) rect(g, 0, y, W, 3, '#1A221B'); for (let x = 0; x < W; x += 90) rect(g, x, 140, 3, 860, '#1A221B');
    rect(g, 0, 1240, W, H - 1240, '#0F140F'); rect(g, 0, 1000, W, 240, '#222B22'); rect(g, 0, 990, W, 18, '#3A463A'); for (let x = 140; x < W; x += 300) line(g, x, 1010, x, 1240, '#10150F', 4);
    rect(g, 40, 420, 270, 820, '#AEB9AB'); rect(g, 40, 420, 270, 820, 'rgba(0,0,0,0.45)'); rect(g, 40, 780, 270, 8, '#10150F'); rect(g, 262, 520, 12, 180, '#4A564A'); rect(g, 262, 840, 12, 220, '#4A564A'); glow(g, 175, 700, 340, '#9DBB8E', 0.06); // geladeira
    rect(g, 400, 340, 230, 300, '#0B0F0C'); vgrad(g, 356, 624, '#6E8A78', '#3E5446', 414, 202); rect(g, 508, 356, 8, 268, '#0B0F0C'); poly(g, [[414, 624], [616, 624], [760, 1250], [250, 1250]], '#B8C8B0', 0.05); // janela
    rect(g, 780, 420, 240, 820, '#0A0F0B'); vgrad(g, 440, 1240, '#2A362C', '#0E140F', 796, 208); glow(g, 900, 860, 260, '#9DBB8E', 0.12); // porta do corredor com luz fria de fundo
    if (c.vulto) { const a = clamp(c.vultoT ? t / c.vultoT : 1) * c.vulto, vx = 900, sw = Math.sin(t * 0.7) * 3; g.save(); g.globalAlpha = a; g.fillStyle = '#020302'; g.beginPath(); g.ellipse(vx + sw, 560, 44, 56, 0, 0, Math.PI * 2); g.fill(); poly(g, [[vx - 28 + sw, 610], [vx + 28 + sw, 610], [vx + 62, 1240], [vx - 62, 1240]], '#020302'); circ(g, vx - 16 + sw, 552, 6, '#E8F0E0'); circ(g, vx + 16 + sw, 552, 6, '#E8F0E0'); g.restore(); }
    rect(g, 560, 1130, 160, 20, '#3A463A'); rect(g, 600, 1150, 14, 90, '#3A463A'); rect(g, 668, 1150, 14, 90, '#3A463A'); // mesa baixa ao fundo
    const k = (t * 0.6) % 1; if (c.pinga) circ(g, 530, 990 - 60 + k * 60, 5, '#B8D0C0', 0.8 * (1 - k * 0.3)); vinheta(g, 0.62);
  };
  // ───────── ELEVADOR NO 13º (âmbar) ─────────
  const botao = (g, x, y, r, rot, ace, t, cor = '#FFC25A') => { circ(g, x, y, r + 6, '#120A04'); circ(g, x, y, r, ace ? cor : '#6A5A48'); if (ace) { glow(g, x, y, r * 3.2, cor, 0.45 * (0.8 + 0.2 * Math.sin(t * 5))); circ(g, x, y, r * 0.78, '#FFE9B0', 0.55); } text(g, rot, x, y + r * 0.36, r * 1.05, ace ? '#4A2A06' : '#241A10', { align: 'center', w: 800 }); };
  CENARIOS.predio_noite = (g, t, c = {}) => { // fachada do prédio de 12 andares à noite, janelas âmbar
    vgrad(g, 0, 1240, '#120A04', '#4A2A0C'); for (let i = 0; i < 40; i++) circ(g, rnd(i) * W, rnd(i + 99) * 260, 1.4 + rnd(i + 5) * 1.6, '#FFE9B0', 0.3 + 0.3 * rnd(i + 3));
    rect(g, 200, 250, 680, 990, '#2E1D10'); rect(g, 200, 250, 680, 14, '#4A2E18'); rect(g, 700, 190, 120, 60, '#241508'); rect(g, 690, 180, 140, 14, '#4A2E18');
    for (let r = 0; r < 12; r++) { const y = 1130 - r * 74; for (let k = 0; k < 4; k++) { const ac = rnd(r * 4 + k + 3) > 0.45; rect(g, 250 + k * 160, y, 100, 52, '#120A04'); if (ac) { rect(g, 254 + k * 160, y + 4, 92, 44, '#FFC25A', 0.85); glow(g, 300 + k * 160, y + 26, 90, '#FFB45A', 0.2); } } text(g, String(r + 1), 150, y + 40, 34, r === 11 ? '#FFC25A' : '#8A6A3A', { mono: 1, w: 700, align: 'right' }); }
    rect(g, 440, 1160, 200, 80, '#120A04'); rect(g, 450, 1170, 180, 70, '#FFC25A', 0.8); glow(g, 540, 1210, 260, '#FFB45A', 0.3); rect(g, 535, 1170, 10, 70, '#120A04');
    rect(g, 0, 1240, W, H - 1240, '#0C0804'); rect(g, 0, 1240, W, 20, '#2A1A0C'); rect(g, 880, 700, 14, 540, '#0C0804'); rect(g, 860, 690, 60, 20, '#FFE9B0', 0.9); glow(g, 890, 700, 360, '#FFB45A', 0.25);
    vinheta(g, 0.55);
  };
  const corredorFundo = (g, x0, y0, w, h, t, luz = 1) => { // corredor visto pela porta aberta do elevador (retângulo x0,y0,w,h)
    g.save(); g.beginPath(); g.rect(x0, y0, w, h); g.clip(); vgrad(g, y0, y0 + h, '#F2A93B', '#8A4A14', x0, w); rect(g, x0 + w * 0.3, y0 + h * 0.2, w * 0.4, h * 0.62, '#4A2808'); rect(g, x0 + w * 0.34, y0 + h * 0.26, w * 0.32, h * 0.56, '#C77A1E');
    rect(g, x0 + w * 0.5 - 4, y0 + h * 0.26, 8, h * 0.56, '#FFE9B0', 0.7 * luz); glow(g, x0 + w * 0.5, y0 + h * 0.55, w, '#FFE9B0', 0.2 * luz); g.restore(); };
  CENARIOS.elevador = (g, t, c = {}) => { // interior do elevador de frente para a porta; c.andar (texto do visor), c.abreEm/c.abreT/c.fecha (porta), c.fora ('corredor'), c.botao13
    vgrad(g, 0, 1240, '#8A6A3A', '#4A3318'); for (let x = 0; x < W; x += 120) rect(g, x, 0, 3, 1240, 'rgba(0,0,0,0.18)'); rect(g, 0, 1240, W, H - 1240, '#1A0F06'); for (let y = 1280; y < H; y += 90) rect(g, 0, y, W, 3, '#0C0804');
    rect(g, 0, 0, W, 70, '#2A1A0C'); rect(g, 80, 24, 920, 30, '#FFF0C4', 0.9); glow(g, W / 2, 40, 700, '#FFE0A0', 0.3 * (0.92 + 0.08 * Math.sin(t * 30)));
    const dx = 340, dw = 400, dy = 420, dh = 820, ab = c.abreEm != null ? clamp((t - c.abreEm) / (c.abreT || 1.0)) : (c.abre ?? 0), k = c.fecha ? 1 - ab : ab, op = out(k) * (dw / 2 - 6);
    rect(g, dx - 20, dy - 20, dw + 40, dh + 20, '#2A1A0C'); if (k > 0.001) { if (c.fora === 'corredor') corredorFundo(g, dx, dy, dw, dh, t, 1); else rect(g, dx, dy, dw, dh, '#0A0603'); }
    for (const s of [-1, 1]) { const x = s < 0 ? dx - op : dx + dw / 2 + op; rect(g, x, dy, dw / 2, dh, '#B8A58A'); rect(g, x, dy, dw / 2, dh, 'rgba(0,0,0,0.08)'); rect(g, x + (s < 0 ? dw / 2 - 30 : 10), dy, 20, dh, 'rgba(255,255,255,0.18)'); rect(g, x + (s < 0 ? 0 : dw / 2 - 3), dy, 3, dh, '#4A3A28'); } // portas de aço
    rect(g, 430, 300, 220, 90, '#0C0804'); const dsp = c.andar ?? '12', fl = (c.pisca && Math.floor(t * 8) % 5 === 0) ? 0.35 : 1; text(g, String(dsp), 540, 372, 78, '#FFB02A', { mono: 1, w: 700, align: 'center' }); rect(g, 430, 300, 220, 90, `rgba(12,8,4,${1 - fl})`); glow(g, 540, 345, 160, '#FFB02A', 0.25 * fl);
    const bx = 880, by = 480; rect(g, bx - 70, by - 120, 140, 700, '#2A1A0C'); rect(g, bx - 58, by - 108, 116, 676, '#6A5A48', 0.55);
    for (let i = 0; i < 6; i++) for (let j = 0; j < 2; j++) botao(g, bx - 26 + j * 52, by + 20 + i * 86, 20, String(12 - i * 2 - j), false, t); if (c.botao13) botao(g, bx, by - 66, 24, '13', true, t);
    vinheta(g, 0.55);
  };
  CENARIOS.corredor_ambar = (g, t, c = {}) => { // corredor do prédio igual ao do narrador: portas, luz âmbar; porta 1301 entreaberta no fundo
    const L = 380, R = 700, T = 520, B = 980; rect(g, 0, 0, W, H, '#120A04'); poly(g, [[0, 0], [W, 0], [R, T], [L, T]], '#2A1A0C'); poly(g, [[0, H], [W, H], [R, B], [L, B]], '#3A1F0C'); poly(g, [[0, 0], [L, T], [L, B], [0, H]], '#6A4620'); poly(g, [[W, 0], [R, T], [R, B], [W, H]], '#7A5226'); rect(g, L, T, R - L, B - T, '#241408');
    for (let i = -3; i <= 3; i++) line(g, 540 + i * 100, B, 540 + i * 460, H, '#5A2E10', 3);
    const wallL = x => [lerp(0, T, x / L), lerp(H, B, x / L)], wallR = x => [lerp(0, T, (W - x) / (W - R)), lerp(H, B, (W - x) / (W - R))];
    const porta = (wall, sgn, x1, x2, n) => { const [t1, b1] = wall(x1), [t2, b2] = wall(x2), h1 = b1 - t1, h2 = b2 - t2; poly(g, [[x1, t1 + h1 * 0.2], [x2, t2 + h2 * 0.2], [x2, b2], [x1, b1]], '#1A0F06'); poly(g, [[x1 + 8 * sgn, t1 + h1 * 0.23], [x2 - 4 * sgn, t2 + h2 * 0.23], [x2 - 4 * sgn, b2 - 4], [x1 + 8 * sgn, b1 - 6]], '#8A5A28'); circ(g, (x1 + x2) / 2, (t1 + b1) / 2 + h1 * 0.15, 8 * (h2 / h1), '#FFE9B0'); };
    porta(wallL, 1, 40, 190); porta(wallL, 1, 250, 330); porta(wallR, -1, 890, 1040); porta(wallR, -1, 760, 830);
    rect(g, 470, 580, 140, 380, '#0A0603'); const ab = 14 + 8 * Math.sin(t * 2); rect(g, 470, 580, 140, 380, '#8A5A28'); poly(g, [[470, 580], [470 + 100, 590], [470 + 100, 950], [470, 960]], '#0A0603'); rect(g, 560 - ab, 590, 10 + ab, 360, '#FFE9B0', 0.9); glow(g, 565, 770, 360, '#FFE9B0', 0.25 + 0.05 * Math.sin(t * 5)); text(g, '1301', 540, 560, 36, '#FFC25A', { mono: 1, w: 700, align: 'center' }); // porta 1301 entreaberta
    for (const y of [140, 340]) { rect(g, 440, y, 200, 14, '#FFF0C4', 0.9); poly(g, [[440, y + 14], [640, y + 14], [820, y + 300], [260, y + 300]], '#FFE0A0', 0.04); }
    vinheta(g, 0.55);
  };
  CENARIOS.portaria_ambar = (g, t, c = {}) => { // portaria do prédio de manhã: caixas de correio, balcão, janela com sol
    vgrad(g, 0, 1240, '#F2D9A8', '#C79A58'); rect(g, 0, 1240, W, H - 1240, '#6A4A2A'); for (let y = 1260; y < H; y += 100) rect(g, 0, y, W, 3, '#4A3018'); for (let x = 0; x < W; x += 100) rect(g, x, 1240, 3, H - 1240, '#4A3018');
    rect(g, 60, 360, 300, 480, '#8A6A3A'); for (let i = 0; i < 5; i++) for (let j = 0; j < 3; j++) { rect(g, 76 + j * 94, 376 + i * 92, 84, 80, '#B8A58A'); rect(g, 96 + j * 94, 404 + i * 92, 44, 8, '#4A3A28'); circ(g, 118 + j * 94, 436 + i * 92, 6, '#4A3A28'); } // caixas de correio
    rect(g, 600, 300, 380, 420, '#3A2410'); vgrad(g, 316, 704, '#FFF0C4', '#F2D9A8', 616, 348); rect(g, 786, 316, 8, 388, '#3A2410'); rect(g, 616, 500, 348, 8, '#3A2410'); poly(g, [[616, 704], [964, 704], [980, 1250], [320, 1250]], '#FFF0C4', 0.12); glow(g, 790, 510, 560, '#FFE0A0', 0.3);
    rect(g, 0, 1040, 1080, 200, '#5A3A1C'); rect(g, 0, 1024, W, 30, '#8A5A28'); rect(g, 0, 1040, W, 200, 'rgba(0,0,0,0.12)'); rrect(g, 780, 940, 70, 90, 12, '#2A6A3A'); circ(g, 815, 930, 54, '#3A8A4A'); circ(g, 780, 960, 40, '#2A6A3A'); // planta no balcão
    vinheta(g, 0.4);
  };
  CENARIOS.painel_botoes = (g, t, c = {}) => { // painel do elevador de perto; o botão 13 (novo) aceso e pulsando
    vgrad(g, 0, H, '#3A2410', '#150D06'); for (let x = 0; x < W; x += 120) rect(g, x, 0, 3, H, 'rgba(0,0,0,0.2)'); rect(g, 280, 280, 520, 1090, '#120A04'); rect(g, 296, 296, 488, 1058, '#7A6A52'); rect(g, 296, 296, 488, 1058, 'rgba(0,0,0,0.25)');
    for (let i = 0; i < 6; i++) for (let j = 0; j < 2; j++) botao(g, 440 + j * 200, 600 + i * 108, 40, String(12 - i * 2 - j), false, t); botao(g, 540, 1290, 40, 'T', c.terreoAceso ?? false, t);
    const a = c.novo === false ? 0 : 1; if (a) { botao(g, 540, 430, 46, '13', true, t); glow(g, 540, 430, 520, '#FFB02A', 0.35 * (0.7 + 0.3 * Math.sin(t * 4))); } vinheta(g, 0.5);
  };
  POSES.curioso = t => ({ al: [-8, 195], ar: [8, 195], fl: [-30, 235], fr: [30, 235], olho: 'grande', olhar: 10, boca: 'pequena', sobr: 0.9, cabeca: 0.06 });
  POSES.cega = t => ({ al: [-8, 195], ar: [8, 195], fl: [-30, 235], fr: [30, 235], olho: 'cego', boca: 'reta', sobr: 0.2, cabeca: 0.04 });
})();
