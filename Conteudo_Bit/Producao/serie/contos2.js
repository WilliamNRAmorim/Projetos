// Cenários e objetos do Dia 2 dos contos (Coração Delator, Loira do banheiro, Motorista de app, Luz do banheiro). Só ACRESCENTA ao Motor.
(() => {
  const { CENARIOS, POSES, OBJETOS, W, H, GY } = Motor, { rect, poly, circ, line, rrect, text, glow, vgrad, rgba, vinheta, rnd, lerp, clamp, out } = Motor.H_;
  const fundoGrad = (g, a, b) => vgrad(g, 0, H, a, b);
  const bate = (t, bpm) => { const per = 60 / bpm, k = (t % per) / per; return Math.max(Math.exp(-k * 14), 0.55 * Math.exp(-Math.max(0, k - 0.28) * 14) * (k > 0.28 ? 1 : 0)); }; // lub-dub 0..1

  // ───────── O CORAÇÃO DELATOR (ocre pálido) ─────────
  CENARIOS.quarto_velho = (g, t, c = {}) => { // quarto do velho: cama, rosto no travesseiro, olho (c.aberto), feixe de lanterna da porta (c.feixe)
    fundoGrad(g, '#2A2410', '#0E0B05'); for (let x = 0; x < W; x += 110) rect(g, x, 0, 4, 1240, 'rgba(0,0,0,0.25)'); rect(g, 0, 1240, W, H - 1240, '#0A0803'); for (let y = 1280; y < H; y += 90) rect(g, 0, y, W, 3, '#050402');
    rect(g, 700, 300, 280, 420, '#07060A'); vgrad(g, 316, 704, '#26304A', '#121830', 716, 248); circ(g, 880, 440, 40, '#C9C6D8', 0.5); rect(g, 836, 316, 8, 388, '#07060A'); // janela com lua
    rect(g, 0, 200, 240, 1040, '#050402'); rect(g, 240, 200, 14, 1040, '#4A3E1C'); // batente da porta
    rect(g, 330, 1000, 640, 240, '#3A3018'); rect(g, 310, 900, 40, 340, '#1A1408'); rect(g, 950, 940, 40, 300, '#1A1408'); rrect(g, 380, 960, 400, 70, 30, '#CFC8A8', 0.8); // cama e travesseiro
    circ(g, 560, 975, 76, '#C9B08C'); g.fillStyle = '#E8E4D0'; g.beginPath(); g.arc(560, 960, 80, Math.PI, Math.PI * 2); g.fill(); line(g, 510, 1000, 540, 1002, '#2A1E10', 5); line(g, 590, 1030, 620, 1030, '#6A4A38', 5); // rosto, touca, olho esquerdo fechado
    const ab = c.aberto; if (ab) { circ(g, 612, 988, 24, '#D6E2EC'); circ(g, 612, 988, 24, 'rgba(120,170,210,0.55)'); circ(g, 612, 988, 9, '#0A0E16'); } else line(g, 590, 990, 632, 990, '#2A1E10', 5);
    poly(g, [[340, 1060], [940, 1050], [960, 1240], [330, 1240]], '#5A4A22'); rect(g, 330, 1050, 620, 8, '#3A2E14');
    if (c.feixe) { const f = 0.22 + 0.04 * Math.sin(t * 9); poly(g, [[254, 760], [262, 770], [640, 1060], [500, 940]], '#F2E08A', f); glow(g, 612, 990, 220, '#F2E08A', 0.28); rect(g, 254, 750, 8, 40, '#F2E08A', 0.9); }
    vinheta(g, 0.62);
  };
  CENARIOS.olho_close = (g, t, c = {}) => { // o olho do velho em close (c.aberto 0..1 por c.abreEm), pulsando com c.bpm
    fundoGrad(g, '#1E1808', '#0A0803'); const bt = c.bpm ? bate(t, c.bpm) : 0, S = 1 + 0.05 * bt, ab = c.abreEm != null ? out(clamp((t - c.abreEm) / 0.5)) : (c.aberto ?? 1);
    g.save(); g.translate(W / 2, 820); g.scale(S, S); poly(g, [[-460, 60], [-200, -120], [200, -120], [460, 60], [200, 220], [-200, 220]], '#B89870');
    for (let i = 0; i < 6; i++) line(g, -420 + i * 20, 50 + i * 4, -300 + i * 10, 20 + i * 4, '#8A6A48', 4, 0.7);
    g.save(); g.beginPath(); g.moveTo(-340, 50); g.quadraticCurveTo(0, 50 - 330 * ab, 340, 50); g.quadraticCurveTo(0, 50 + 260 * ab, -340, 50); g.clip(); rect(g, -400, -300, 800, 600, '#E4EAF0'); circ(g, 0, 50, 170, '#9CB8D0'); circ(g, 0, 50, 170, 'rgba(210,225,240,0.45)');
    for (let i = 0; i < 14; i++) { const a = i / 14 * Math.PI * 2; line(g, Math.cos(a) * 90, 50 + Math.sin(a) * 90, Math.cos(a) * 168, 50 + Math.sin(a) * 168, 'rgba(70,100,130,0.5)', 3); } circ(g, 0, 50, 44 + 8 * bt, '#06080C'); circ(g, -26, 24, 12, '#FFFFFF', 0.8);
    for (let i = 0; i < 9; i++) line(g, -330 + i * 80, 50, -300 + i * 75, 30 + Math.sin(i) * 20, 'rgba(180,70,60,0.35)', 3); g.restore();
    line(g, -340, 50, 340, 50, 'rgba(0,0,0,0)', 1); g.restore(); if (c.feixe) glow(g, W / 2, 820, 760, '#F2E08A', 0.18); vinheta(g, 0.7);
  };
  CENARIOS.assoalho = (g, t, c = {}) => { // tábuas do assoalho vistas de frente; c.bpm = as três tábuas do meio pulsam; c.cadeira = pés da cadeira por cima
    fundoGrad(g, '#14100A', '#0A0803'); const bt = c.bpm ? bate(t, c.bpm) : 0;
    for (let i = 0; i < 12; i++) { const y = 200 + i * 130, mid = i >= 4 && i <= 6, dy = mid ? -10 * bt : 0; rect(g, 0, y + dy, W, 124, mid ? '#4A3A1A' : '#2E2410'); rect(g, 0, y + dy + 118, W, 6, '#0A0803'); for (const x of [90, 430, 780]) if (mid) { circ(g, x, y + dy + 28, 7, '#8A7A4A'); circ(g, x, y + dy + 96, 7, '#8A7A4A'); } for (let k = 0; k < 6; k++) line(g, rnd(i * 7 + k) * W, y + dy + 20 + k * 14, rnd(i * 7 + k) * W + 160, y + dy + 22 + k * 14, 'rgba(0,0,0,0.25)', 2); }
    glow(g, W / 2, 820, 700, '#F2D88A', 0.18 + 0.12 * bt); if (c.cadeira) { for (const x of [250, 830]) rect(g, x - 24, 0, 48, 520, '#0E0A04'); }
    vinheta(g, 0.6 + 0.2 * bt);
  };
  CENARIOS.sala_policia = (g, t, c = {}) => { // sala do velho com cadeiras (c.cadeiras = [x0..1]), c.bpm = vinheta pulsando
    fundoGrad(g, '#2E2812', '#14100A'); for (let x = 0; x < W; x += 110) rect(g, x, 0, 4, 1240, 'rgba(0,0,0,0.22)'); rect(g, 0, 1240, W, H - 1240, '#0E0B05'); for (let y = 1280; y < H; y += 90) rect(g, 0, y, W, 3, '#050402'); rect(g, 0, 880, W, 12, '#4A3E1C');
    rect(g, 60, 300, 220, 400, '#07060A'); vgrad(g, 316, 684, '#26304A', '#121830', 76, 188); rect(g, 600, 640, 380, 220, '#2A2210'); rect(g, 620, 610, 340, 40, '#4A3E1C'); // quadro/cômoda ao fundo
    const bt = c.bpm ? bate(t, c.bpm) : 0; for (const fx of c.cadeiras || []) { const x = fx * W, es = c.escCad || 0.8, sy = GY - 117 * es; rect(g, x - 85 * es, sy - 280 * es, 22, 280 * es, '#4A3418'); rect(g, x - 90 * es, sy, 180 * es, 22, '#5A4220'); rect(g, x - 80 * es, sy + 22, 18, 1240 - sy - 22, '#3A2810'); rect(g, x + 62 * es, sy + 22, 18, 1240 - sy - 22, '#3A2810'); }
    glow(g, W / 2, 700, 800, '#F2D88A', 0.12); vinheta(g, 0.5 + 0.3 * bt);
  };

  // ───────── LOIRA DO BANHEIRO (rosa) ─────────
  const cabines = (g, t, c, ox, oy, s) => { // fileira de 4 cabines; c.fechada = índice fechado (ou -1); c.abreEm = a fechada abre em T s; c.luzSob
    g.save(); g.translate(ox, oy); g.scale(s, s);
    for (let i = 0; i < 4; i++) { const x = 30 + i * 255, fe = c.fechada === i, ab = fe && c.abreEm != null ? out(clamp((t - c.abreEm) / 1.6)) : 0, y0 = 360, h = 880;
      rect(g, x - 10, y0 - 20, 240, h + 20, '#C9A0B4'); rect(g, x, y0, 220, h, '#2A1A24'); rect(g, x + 70, y0 + 540, 80, 200, '#E8DDE2'); rrect(g, x + 60, y0 + 420, 100, 130, 14, '#E8DDE2'); // vaso ao fundo
      if (fe && ab > 0.02) { glow(g, x + 110, y0 + 500, 260, '#E86FA8', 0.08); }
      const aberta = !fe || ab > 0.02, w = fe ? 210 * (1 - 0.88 * ab) : 40; if (!aberta || fe) { rect(g, x + 5, y0 + 40, w, h - 80, '#E86FA8'); rect(g, x + 5, y0 + 40, w, h - 80, 'rgba(255,255,255,0.12)'); rect(g, x + 5, y0 + h - 40 - 30, w, 30, 'rgba(0,0,0,0.2)'); if (w > 100) { circ(g, x + 175, y0 + 460, 10, '#F2F2F2'); } }
      else rect(g, x + 4, y0 + 40, 36, h - 80, '#E86FA8');
      if (fe && c.luzSob && ab < 0.02) { rect(g, x + 5, y0 + h - 40, 210, 14, '#FFE9F2', 0.9); glow(g, x + 110, y0 + h - 30, 220, '#FFE9F2', 0.25); } }
    g.restore();
  };
  CENARIOS.banheiro_escola = (g, t, c = {}) => { // banheiro da escola: azulejo rosa, quatro cabines
    fundoGrad(g, '#F3B8CF', '#E08FB0'); for (let y = 0; y < 1240; y += 110) rect(g, 0, y, W, 3, 'rgba(255,255,255,0.35)'); for (let x = 0; x < W; x += 110) rect(g, x, 0, 3, 1240, 'rgba(255,255,255,0.35)');
    rect(g, 0, 1240, W, H - 1240, '#C8A0B4'); for (let y = 1240; y < H; y += 110) for (let x = ((y / 110) % 2) * 55 - 55; x < W; x += 110) rect(g, x, y, 55, 55, '#B88CA4');
    rect(g, 0, 190, W, 150, '#FFF0F6'); rect(g, 0, 190, W, 150, 'rgba(255,255,255,0.0)'); rect(g, 120, 220, 840, 18, '#FFE9F2', 0.95); glow(g, W / 2, 240, 800, '#FFE9F2', 0.22 * (0.9 + 0.1 * Math.sin(t * 30)));
    cabines(g, t, c, 0, 0, 1); rect(g, 0, 1236, W, 6, 'rgba(60,20,40,0.5)'); vinheta(g, 0.45);
  };
  CENARIOS.espelho_pia = (g, t, c = {}) => { // espelho sobre as pias, com a fileira de cabines refletida
    fundoGrad(g, '#F3B8CF', '#E08FB0'); for (let y = 0; y < 1240; y += 110) rect(g, 0, y, W, 3, 'rgba(255,255,255,0.35)'); for (let x = 0; x < W; x += 110) rect(g, x, 0, 3, 1240, 'rgba(255,255,255,0.35)'); rect(g, 0, 1240, W, H - 1240, '#C8A0B4');
    rect(g, 100, 260, 880, 780, '#7A4A62'); rect(g, 120, 280, 840, 740, '#D8E6EA'); g.save(); g.beginPath(); g.rect(120, 280, 840, 740); g.clip(); fundoGrad(g, '#EAB0C8', '#C87AA0'); cabines(g, t, c, 120 + 2, 330, 0.74); g.restore(); poly(g, [[120, 1020], [330, 280], [480, 280], [270, 1020]], '#FFFFFF', 0.16);
    rect(g, 100, 1040, 880, 90, '#F2EAEE'); rrect(g, 160, 1040, 300, 120, 30, '#FFFFFF'); rrect(g, 620, 1040, 300, 120, 30, '#FFFFFF'); rect(g, 300, 980, 24, 70, '#B8B8C4'); rect(g, 756, 980, 24, 70, '#B8B8C4'); rect(g, 0, 190, W, 8, 'rgba(255,255,255,0.5)'); vinheta(g, 0.45);
  };

  // ───────── MOTORISTA DE APP (roxo) ─────────
  const carro = (g, x, y, s, cor, claro) => { // carro de lado (frente à direita); y = chão
    g.save(); g.translate(x, y); g.scale(s, s); g.fillStyle = 'rgba(0,0,0,0.4)'; g.beginPath(); g.ellipse(0, 0, 360, 22, 0, 0, Math.PI * 2); g.fill();
    rrect(g, -340, -150, 680, 110, 40, cor); poly(g, [[-190, -150], [-110, -250], [120, -250], [220, -150]], cor); poly(g, [[-160, -156], [-100, -236], [-8, -236], [-8, -156]], claro ? '#6A7A90' : '#2A2A40'); poly(g, [[8, -156], [8, -236], [112, -236], [194, -156]], claro ? '#6A7A90' : '#2A2A40');
    g.strokeStyle = claro ? 'rgba(0,0,0,0.35)' : '#9A7CE0'; g.lineWidth = 5; g.beginPath(); g.roundRect(-340, -150, 680, 110, 40); g.moveTo(-190, -150); g.lineTo(-110, -250); g.lineTo(120, -250); g.lineTo(220, -150); g.stroke();
    rect(g, -340, -112, 680, 10, 'rgba(255,255,255,0.15)'); rrect(g, 300, -138, 36, 24, 8, '#FFF0B0'); glow(g, 330, -126, 120, '#FFF0B0', 0.3); rrect(g, -340, -138, 20, 24, 8, '#E83A3A');
    for (const wx of [-210, 200]) { circ(g, wx, -40, 54, '#0A0810'); circ(g, wx, -40, 28, '#8A8A98'); } g.restore();
  };
  CENARIOS.rua_roxa = (g, t, c = {}) => { // rua à noite, roxo; c.carros = [{x, y?, esc, cor:'preto'|'prata'}]
    fundoGrad(g, '#0E0A1E', '#3A2A6A'); for (let i = 0; i < 4; i++) { const x = i * 300 - 40, h = 380 + rnd(i + 4) * 360; rect(g, x, 1000 - h, 280, h + 240, i % 2 ? '#1A1236' : '#140E2A'); for (let k = 0; k < 6; k++) { rect(g, x + 30 + (k % 2) * 110, 1000 - h + 50 + Math.floor(k / 2) * 120, 60, 70, rnd(i * 6 + k) > 0.6 ? '#C9A8FF' : '#0A0716', rnd(i * 6 + k) > 0.6 ? 0.6 : 1); } }
    rect(g, 760, 520, 260, 80, '#2A1A4A'); text(g, 'BAR 24H', 890, 580, 50, '#FF5AC8', { align: 'center', w: 800 }); glow(g, 890, 560, 300, '#FF5AC8', 0.3 * (0.8 + 0.2 * Math.sin(t * 6)));
    rect(g, 0, 1240, W, H - 1240, '#120C24'); rect(g, 0, 1240, W, 40, '#2A1E4A'); for (let x = 20; x < W; x += 200) rect(g, x, 1500, 110, 14, '#6A5AA0', 0.6);
    rect(g, 100, 560, 16, 700, '#07040F'); rect(g, 70, 540, 80, 24, '#07040F'); rect(g, 80, 556, 60, 10, '#FFE9B0'); glow(g, 110, 570, 360, '#C9A8FF', 0.3); poly(g, [[80, 570], [140, 570], [360, 1240], [-140, 1240]], '#C9A8FF', 0.05);
    for (const k of c.carros || []) carro(g, k.x, k.y ?? 1390, k.esc || 1, k.cor === 'prata' ? '#B8BCC8' : '#14101C', k.cor === 'prata'); vinheta(g, 0.55);
  };
  CENARIOS.carro_janela = (g, t, c = {}) => { // lateral do carro perto, janela aberta (c.cor 'preto'|'prata'); use o objeto porta_carro por cima do motorista
    const cl = c.cor === 'prata', body = cl ? '#B8BCC8' : '#14101C'; fundoGrad(g, '#0E0A1E', '#3A2A6A'); rect(g, 0, 1240, W, H - 1240, '#120C24'); rect(g, 0, 1240, W, 40, '#2A1E4A'); glow(g, 120, 600, 520, '#C9A8FF', 0.25);
    rect(g, 40, 330, 1000, 1170, body); rect(g, 40, 330, 1000, 190, cl ? '#98A0B0' : '#0A0814'); rect(g, 90, 520, 900, 420, '#0C0818'); vgrad(g, 530, 930, cl ? '#4A4660' : '#1E1838', '#0C0818', 100, 880); // janela aberta (interior)
    rect(g, 40, 940, 1000, 14, cl ? '#8A90A0' : '#2A2440'); rect(g, 90, 1500, 900, 40, '#0A0814'); circ(g, 840, 1520, 120, '#0A0810'); circ(g, 840, 1520, 62, '#8A8A98'); circ(g, 240, 1520, 120, '#0A0810'); circ(g, 240, 1520, 62, '#8A8A98'); vinheta(g, 0.5);
  };
  OBJETOS.porta_carro = (g, o, u) => { const cl = o.cor === 'prata', body = cl ? '#B8BCC8' : '#14101C'; rect(g, 40, 900, 1000, 640, body); rect(g, 40, 900, 1000, 40, cl ? '#8A90A0' : '#2A2440'); rrect(g, 700, 1040, 200, 36, 12, cl ? '#6A6E7A' : '#34304A'); rect(g, 80, 1300, 920, 8, 'rgba(255,255,255,0.1)'); };
  OBJETOS.celular_app = (g, o, u) => { // celular roxo com o carro do app (o.carro 'prata'|'preto'), o.nome (inicial)
    const k = out(clamp(u / 0.4)), e = o.escala || 1; g.save(); g.translate(o.x * W, lerp(H + 400, (o.y ?? 0.4) * H, k)); g.rotate((o.inclina ?? -0.06)); g.scale(e, e);
    rrect(g, -190, -340, 380, 680, 56, 'rgba(0,0,0,0.3)'); g.translate(-6, -6); rrect(g, -190, -340, 380, 680, 56, '#8A5CE0'); rrect(g, -170, -320, 340, 640, 40, '#120C24'); rect(g, -150, -270, 300, 120, '#2A1E4A'); text(g, 'SUA VIAGEM', -130, -200, 32, '#C9A8FF', { w: 700 }); text(g, (o.nome || 'A.') , -130, -166, 40, '#FFFFFF', { w: 800 });
    carro(g, 0, 130, 0.36, o.carro === 'preto' ? '#14101C' : '#B8BCC8', o.carro !== 'preto'); text(g, o.carro === 'preto' ? 'COROLLA PRETO' : 'GOL PRATA', 0, 190, 34, '#FFFFFF', { align: 'center', w: 800 }); rrect(g, -140, 240, 280, 56, 18, '#8A5CE0'); text(g, o.msg || 'A CAMINHO', 0, 280, 30, '#FFF', { align: 'center', w: 800 }); g.restore();
  };

  // ───────── LUZ DO BANHEIRO (branco-ciano frio) ─────────
  CENARIOS.corredor_ciano = (g, t, c = {}) => { // corredor de apartamento; luz fria saindo por baixo da porta do banheiro (c.luz pisca)
    fundoGrad(g, '#0A1418', '#142A30'); rect(g, 0, 1240, W, H - 1240, '#0A1014'); for (let y = 1280; y < H; y += 90) rect(g, 0, y, W, 3, '#050A0C');
    rect(g, 0, 880, W, 12, '#2A4A52'); rect(g, 380, 420, 320, 820, '#050A0C'); rect(g, 396, 436, 288, 804, '#3A5A62'); circ(g, 650, 860, 14, '#CFE8EE'); text(g, 'WC', 540, 520, 54, '#CFE8EE', { align: 'center', w: 800 });
    const f = (c.pisca ? (Math.floor(t * 9) % 4 === 0 ? 0.4 : 1) : 1); rect(g, 396, 1226, 288, 14, '#E8FFFF', 0.95 * f); glow(g, 540, 1240, 520, '#8FE3E8', 0.35 * f); poly(g, [[396, 1240], [684, 1240], [900, H], [180, H]], '#8FE3E8', 0.07 * f);
    vinheta(g, 0.6);
  };
  CENARIOS.banheiro_ciano = (g, t, c = {}) => { // banheiro; c.apagada/c.piscaEm (luz), c.espelho = close do espelho; c.refCostas, c.portaRefAberta, c.refSorri
    const on = c.apagada ? 0 : (c.piscaEm != null && t < c.piscaEm ? 0 : 1), fl = on * (0.92 + 0.08 * Math.sin(t * 38));
    fundoGrad(g, on ? '#CFE8EE' : '#0A1418', on ? '#8FB8C0' : '#040A0C'); if (on) for (let y = 0; y < 1240; y += 120) rect(g, 0, y, W, 3, 'rgba(255,255,255,0.4)'); rect(g, 0, 1240, W, H - 1240, on ? '#6A8A92' : '#05090A');
    const s = c.espelho ? 1 : 0.8, mx = 540, my = c.espelho ? 700 : 620, mw = 700 * s, mh = 820 * s; rect(g, mx - mw / 2 - 20, my - mh / 2 - 20, mw + 40, mh + 40, on ? '#3A5A62' : '#0A1418'); rect(g, mx - mw / 2, my - mh / 2, mw, mh, on ? '#E8F6F8' : '#0C1A1E');
    g.save(); g.beginPath(); g.rect(mx - mw / 2, my - mh / 2, mw, mh); g.clip(); g.translate(mx, my); g.scale(s, s); vgrad(g, -410, 410, on ? '#D8EEF2' : '#0C1A1E', on ? '#9ABCC4' : '#060E10', -350, 700);
    const dx = 160, dw = 240; rect(g, dx, -250, dw, 600, '#1E3238'); if (c.portaRefAberta) { rect(g, dx + 10, -240, dw - 20, 580, '#030708'); poly(g, [[dx - 120, -210], [dx + 10, -240], [dx + 10, 340], [dx - 120, 380]], '#4A6A72'); } else rect(g, dx + 10, -240, dw - 20, 580, '#4A6A72'); // porta atrás do reflexo
    const cabe = '#2B1D16', pele = '#D8B08C'; if (on) { circ(g, -40, -40, 128, cabe); if (!c.refCostas) { circ(g, -40, -30, 104, pele); g.fillStyle = cabe; g.beginPath(); g.arc(-40, -40, 112, Math.PI * 0.95, Math.PI * 2.05); g.fill(); circ(g, -84, -20, 15, '#FFF'); circ(g, 4, -20, 15, '#FFF'); circ(g, -82, -18, 6, '#10140F'); circ(g, 6, -18, 6, '#10140F'); line(g, -62, 42, -18, 42, '#6A4038', 6); if (c.refSorri) { g.strokeStyle = '#6A4038'; g.lineWidth = 7; g.beginPath(); g.arc(-40, 20, 40, 0.2, Math.PI - 0.2); g.stroke(); } } else { rect(g, -150, -30, 220, 230, cabe); } rrect(g, -190, 120, 300, 330, 60, '#9AA8C8'); }
    g.restore(); poly(g, [[mx - mw / 2, my + mh / 2], [mx - mw / 2 + 220, my - mh / 2], [mx - mw / 2 + 330, my - mh / 2], [mx - mw / 2 + 110, my + mh / 2]], '#FFFFFF', 0.12 * on);
    rect(g, 140, 1130, 800, 110, on ? '#F2F8FA' : '#101C20'); rrect(g, 340, 1120, 400, 100, 40, on ? '#FFFFFF' : '#0C1418'); rect(g, 520, 1050, 40, 80, '#8A98A0'); if (on) { rect(g, 240, 150, 600, 22, '#F8FFFF', fl); glow(g, 540, 170, 900, '#E8FFFF', 0.25 * fl); } vinheta(g, on ? 0.35 : 0.8);
  };
  CENARIOS.porta_ciano = (g, t, c = {}) => { // a porta do banheiro por dentro, fechada, com o trinco
    fundoGrad(g, '#A8CCD4', '#7AA0A8'); for (let y = 0; y < 1240; y += 120) rect(g, 0, y, W, 3, 'rgba(255,255,255,0.35)'); rect(g, 0, 1240, W, H - 1240, '#5A7A82'); rect(g, 300, 260, 480, 980, '#2A4A52'); rect(g, 330, 290, 420, 920, '#4A6A72'); rect(g, 330, 290, 420, 920, 'rgba(255,255,255,0.05)'); circ(g, 690, 780, 26, '#D8E6EA'); rect(g, 640, 700, 12, 12, '#8A98A0'); rrect(g, 640, 720, 90, 30, 10, '#B8C8CC'); rect(g, 240, 150, 600, 22, '#F8FFFF', 0.95); glow(g, 540, 170, 900, '#E8FFFF', 0.22); vinheta(g, 0.45);
  };
})();
