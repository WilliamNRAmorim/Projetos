// Cenários e sons do Short solto 04 (Cachorros). Só ACRESCENTA ao Motor. Prefixo cc_ = sépia, mostarda de lâmpada de sódio e o vermelho da marca.
(() => {
  const { CENARIOS } = Motor, W = Motor.W, H = Motor.H, { rect, circ, line, rrect, glow, vgrad, vinheta, rnd, lerp, clamp, out, P } = Motor.H_;
  const TAU = Math.PI * 2, BREU = '#0A0703', SODIO = '#E8A317', CLARO = '#FFE3A0', OSSO = '#F4EEDC', PELE = '#9A6A44';
  const elipse = (g, x, y, rx, ry, c, a = 1, rot = 0) => { g.globalAlpha = a; g.fillStyle = c; g.beginPath(); g.ellipse(x, y, rx, ry, rot, 0, TAU); g.fill(); g.globalAlpha = 1; };
  const forma = (g, c, fn, a = 1) => { g.globalAlpha = a; g.fillStyle = c; g.beginPath(); fn(g); g.closePath(); g.fill(); g.globalAlpha = 1; };
  const curva = (g, c, lw, fn, a = 1) => { g.globalAlpha = a; g.strokeStyle = c; g.lineWidth = lw; g.lineCap = 'round'; g.lineJoin = 'round'; g.beginPath(); fn(g); g.stroke(); g.globalAlpha = 1; };
  const poli = (g, c, pts, a = 1) => forma(g, c, q => pts.forEach(([x, y], i) => i ? q.lineTo(x, y) : q.moveTo(x, y)), a);

  // ───── peças
  // cachorro sentado de perfil; (x,y) = patas. o.late 0..1 (boca e cabeça), o.flip, o.olho
  function cao(g, x, y, s, o = {}) {
    g.save(); g.translate(x, y); g.scale(s * (o.flip ? -1 : 1), s); const c = o.cor || BREU, l = o.late || 0;
    forma(g, c, q => { q.moveTo(-120, 0); q.quadraticCurveTo(-150, -130, -40, -170); q.quadraticCurveTo(10, -230, 30, -270); q.lineTo(100, -250); q.quadraticCurveTo(110, -130, 90, 0); q.lineTo(55, 0); q.lineTo(45, -90); q.quadraticCurveTo(30, -20, 0, 0); });
    curva(g, c, 22, q => { q.moveTo(-110, -20); q.quadraticCurveTo(-190, -20, -185, -90); });
    g.translate(60, -270); g.rotate(-0.55 * l);
    elipse(g, 0, -20, 66, 56, c); poli(g, c, [[20, -55], [140, -22 - 14 * l], [138, -6 - 12 * l], [30, 6]]); poli(g, c, [[22, 4], [118, 6 + 36 * l], [106, 24 + 38 * l], [0, 34]]);
    poli(g, c, [[-52, -40], [-46, -140], [-4, -68]]); poli(g, c, [[-6, -66], [26, -128], [34, -54]]);
    if (o.olho) { circ(g, 28, -34, 8, o.olho); glow(g, 28, -34, 36, o.olho, 0.6); }
    g.restore();
    if (l > 0.35) for (let i = 1; i <= 3; i++) { const d = o.flip ? -1 : 1; curva(g, CLARO, 6 * s + 2, q => { const cx = x + d * 170 * s, cy = y - 390 * s, r = (40 + i * 34) * s; d > 0 ? q.arc(cx, cy, r, -0.9, 0.35) : q.arc(cx, cy, r, Math.PI - 0.35, Math.PI + 0.9); }, 0.75 * l * (1 - i * 0.22)); }
  }
  const latir = (t, fase, per = 1.1) => Math.max(0, Math.sin(((t / per + fase) % 1) * TAU * 1.5)) ** 0.6;
  function ceu(g, t, y1) { vgrad(g, 0, y1, '#070503', '#4A3108'); for (let i = 0; i < 50; i++) circ(g, rnd(i + 7) * W, rnd(i + 33) * y1 * 0.55, 1.5 + rnd(i) * 1.6, OSSO, 0.25 + 0.25 * Math.sin(t * 2 + i)); }
  function lua(g, x, y, r) { glow(g, x, y, r * 4, CLARO, 0.25); circ(g, x, y, r, '#F3E2AE'); circ(g, x + r * 0.42, y - r * 0.25, r * 0.9, '#1A1105', 0.94); }
  function casa(g, x, y, w, h, o = {}) {
    rect(g, x, y - h, w, h, o.cor || '#1C1307'); poli(g, '#0F0A03', [[x - 22, y - h + 6], [x + w / 2, y - h - w * 0.32], [x + w + 22, y - h + 6]]);
    const ac = o.acesa; rect(g, x + w * 0.16, y - h * 0.68, w * 0.3, h * 0.34, ac ? SODIO : '#060402'); rect(g, x + w * 0.3, y - h * 0.68, 7, h * 0.34, '#0F0A03'); rect(g, x + w * 0.16, y - h * 0.52, w * 0.3, 7, '#0F0A03');
    if (ac) glow(g, x + w * 0.31, y - h * 0.5, w * 0.7, SODIO, 0.3); rect(g, x + w * 0.62, y - h * 0.55, w * 0.22, h * 0.55, '#0A0602');
  }
  function muro(g, y, h, cor = '#120C04') { rect(g, 0, y, W, h, cor); rect(g, 0, y, W, 14, '#3A2708'); for (let i = 0; i < 12; i++) rect(g, i * 98 + 20, y + 14, 5, h, '#060401', 0.6); }
  function poste(g, t, x, y, ap = 1) {
    rect(g, x - 11, y, 22, H - y, BREU); curva(g, BREU, 18, q => { q.moveTo(x, y + 10); q.quadraticCurveTo(x + 20, y - 40, x + 100, y - 30); });
    const f = ap * (0.9 + 0.1 * Math.sin(t * 17) * Math.sin(t * 5)); poli(g, SODIO, [[x + 66, y - 20], [x + 136, y - 20], [x + 420, 1450], [x - 210, 1450]], 0.11 * f); glow(g, x + 100, y - 12, 360, SODIO, 0.55 * f); elipse(g, x + 100, y - 20, 44, 18, CLARO, f);
  }
  function rua(g, t, o = {}) {
    ceu(g, t, 1000); lua(g, 860, 330, 70);
    casa(g, -30, 980, 300, 280, { acesa: o.luz }); casa(g, 300, 960, 240, 220); casa(g, 590, 985, 270, 300, { acesa: o.luz }); casa(g, 880, 960, 260, 240);
    curva(g, BREU, 4, q => { q.moveTo(-10, 560); q.quadraticCurveTo(540, 660, 1090, 520); q.moveTo(-10, 610); q.quadraticCurveTo(540, 700, 1090, 575); });
    vgrad(g, 960, H, '#3A2708', '#080502'); poli(g, '#1A1105', [[400, 985], [680, 985], [1100, H], [-20, H]]);
    for (let i = 0; i < 40; i++) rect(g, rnd(i + 61) * W, 1010 + rnd(i + 99) * 800, 30 + rnd(i) * 70, 5, SODIO, 0.14);
  }
  // telefone com as mensagens. msgs = textos da vizinha; digitando = três pontos; eu = pergunta do narrador
  function fone(g, t, c) {
    vgrad(g, 0, H, '#1A1105', BREU); glow(g, 540, 760, 900, SODIO, 0.2);
    const treme = c.vibra && t < 0.9 ? Math.sin(t * 90) * 14 * (1 - t / 0.9) : 0;
    g.save(); g.translate(540 + treme, 720); g.rotate(-0.035 + treme * 0.001);
    elipse(g, -330, 520, 150, 270, '#5A3A24', 1, 0.35);
    rrect(g, -360, -590, 720, 1190, 18, '#050301'); rrect(g, -336, -560, 672, 1130, 6, '#17130B');
    rect(g, -336, -560, 672, 150, '#241C0E'); circ(g, -262, -485, 42, SODIO);
    g.textBaseline = 'middle'; g.textAlign = 'left'; g.fillStyle = OSSO; g.font = '700 48px Geist'; g.fillText('Dona Célia', -195, -505); g.font = '500 32px "Geist Mono"'; g.fillStyle = SODIO; g.fillText('vizinha  01:15', -195, -455);
    let y = -360;
    const bolha = (linhas, o = {}) => { const h = linhas.length * 66 + 52, x = o.eu ? -40 : -300, w = o.eu ? 340 : 600; g.save(); const k = o.ap ?? 1; g.globalAlpha = k; g.translate(0, (1 - k) * 30); g.fillStyle = o.eu ? '#4A3A14' : o.nova ? OSSO : '#8F8874'; g.fillRect(x, y, w, h); if (o.nova) { g.fillStyle = P.accent; g.fillRect(x, y, 12, h); }
      g.fillStyle = o.eu ? OSSO : BREU; g.font = '700 48px Geist'; linhas.forEach((l, i) => g.fillText(l, x + 42, y + 58 + i * 66)); g.restore(); y += h + 28; };
    for (const m of c.antigas || []) bolha(m.l, { eu: m.eu });
    const ap = out(clamp((t - (c.em || 0)) / 0.25));
    if (c.nova && t >= (c.em || 0)) bolha(c.nova, { nova: true, ap, eu: false });
    else if (c.digitando && t >= (c.digitaEm || 0)) { g.fillStyle = '#4A4230'; g.fillRect(-300, y, 200, 100); for (let i = 0; i < 3; i++) circ(g, -250 + i * 50, y + 50 - Math.max(0, Math.sin(t * 7 - i)) * 14, 13, OSSO); }
    g.restore();
    elipse(g, 900 + treme, 1330, 120, 250, '#6A4630', 1, -0.5);
    if (c.vibra && t < 0.9) for (const d of [-1, 1]) for (let i = 0; i < 3; i++) curva(g, SODIO, 10, q => q.arc(540 + d * (320 + i * 45), 720, 90 + i * 20, d > 0 ? -0.6 : Math.PI - 0.6, d > 0 ? 0.6 : Math.PI + 0.6), 0.8 - i * 0.2);
    vinheta(g, 0.62);
  }
  // sala: janela com o lado de fora. fora(g) desenha o que há atrás do vidro
  function janela(g, t, fora) {
    vgrad(g, 0, H, '#241906', BREU); for (let x = 40; x < W; x += 110) rect(g, x, 0, 4, 1320, '#3A2A0C', 0.5);
    g.save(); g.beginPath(); g.rect(180, 330, 720, 850); g.clip(); vgrad(g, 330, 1180, '#150E04', '#6A4508'); glow(g, 830, 470, 520, SODIO, 0.55); fora && fora(g); g.restore();
    for (const x of [180, 540, 900]) rect(g, x - 16, 314, 32, 882, '#0C0803'); for (const y of [330, 700, 1180]) rect(g, 164, y - 16, 752, 32, '#0C0803');
    rect(g, 130, 1196, 820, 40, '#4A340E');
    for (const d of [-1, 1]) forma(g, '#4A2E10', q => { const x = 540 + d * 470; q.moveTo(x + d * 90, 260); q.lineTo(x - d * 90, 260); q.quadraticCurveTo(x - d * 20 + Math.sin(t) * 8, 800, x - d * 70, 1280); q.lineTo(x + d * 90, 1280); });
    rect(g, 60, 240, 960, 24, '#0C0803'); rect(g, 0, 1320, W, H - 1320, '#0C0803');
  }
  // a figura do lado de fora: silhueta de mulher de lenço. o.olhos, o.boca 0..1, o.cao 0..1 (focinho e orelhas)
  function vulto(g, t, x, y, s, o = {}) {
    g.save(); g.translate(x, y); g.scale(s, s); const k = o.cao || 0, b = o.boca || 0;
    forma(g, BREU, q => { q.moveTo(-330, 760); q.quadraticCurveTo(-300, 190, -100, 140); q.lineTo(100, 140); q.quadraticCurveTo(300, 190, 330, 760); });
    elipse(g, 0, 0, 150, 185, BREU); forma(g, BREU, q => { q.moveTo(-165, 0); q.quadraticCurveTo(-150, -240, 0, -225); q.quadraticCurveTo(150, -240, 165, 0); q.quadraticCurveTo(200, 150, 90, 190); q.lineTo(-90, 190); q.quadraticCurveTo(-200, 150, -165, 0); });
    if (k) { for (const d of [-1, 1]) poli(g, BREU, [[d * 60, -190], [d * (150 + 40 * k), -190 - 200 * k], [d * 165, -80]]); elipse(g, 0, 70, 80 * k, 105 * k, BREU); }
    if (o.olhos) for (const d of [-1, 1]) { circ(g, d * 56, -30, 13 * o.olhos, P.accent); glow(g, d * 56, -30, 80, P.accent, 0.55 * o.olhos); }
    if (b > 0.05) { elipse(g, 0, 90 + 40 * k, 62, 8 + 62 * b, '#3A0804'); for (let i = 0; i < 6; i++) { const px = -48 + i * 19; poli(g, OSSO, [[px, 90 + 40 * k - 60 * b], [px + 14, 90 + 40 * k - 60 * b], [px + 7, 90 + 40 * k - 60 * b + 28 * b]]); poli(g, OSSO, [[px, 90 + 40 * k + 60 * b], [px + 14, 90 + 40 * k + 60 * b], [px + 7, 90 + 40 * k + 60 * b - 26 * b]]); } }
    g.restore();
  }
  function relogio(g, x, y, r) { circ(g, x, y, r + 22, BREU); circ(g, x, y, r, '#E9DDB8'); for (let i = 0; i < 12; i++) { const a = i / 12 * TAU; line(g, x + Math.sin(a) * r * 0.82, y - Math.cos(a) * r * 0.82, x + Math.sin(a) * r * 0.93, y - Math.cos(a) * r * 0.93, BREU, 12); } }

  // ───── cenários
  // a rua com os cachorros nos muros (primeiro e último plano). c.calaEm = momento em que todos calam
  CENARIOS.cc_rua = (g, t, c = {}) => {
    rua(g, t, { luz: true }); poste(g, t, 120, 520);
    const q = c.calaEm != null && t >= c.calaEm;
    muro(g, 1240, 90); cao(g, 300, 1245, 0.95, { late: q ? 0 : latir(t, 0.1), olho: q ? CLARO : 0 }); cao(g, 820, 1245, 0.8, { flip: true, late: q ? 0 : latir(t, 0.55), olho: q ? CLARO : 0 });
    cao(g, 560, 1060, 0.38, { late: q ? 0 : latir(t, 0.8) }); vgrad(g, 1330, H, '#120C04', BREU); vinheta(g, 0.58);
  };
  CENARIOS.cc_chegou = (g, t) => {
    rua(g, t, {}); poste(g, t, 120, 520, t < 0.5 ? 1 : 0.55); const k = out(clamp(t / 1.6));
    poli(g, BREU, [[500, 1010], [585, 1010], [lerp(700, 1000, k), lerp(1150, H, k)], [lerp(420, 120, k), lerp(1150, H, k)]], 0.85); vulto(g, t, 545, 900, lerp(0.14, 0.24, k), { olhos: clamp((t - 0.6) * 2) }); vinheta(g, 0.62);
  };
  CENARIOS.cc_bairro = (g, t) => {
    ceu(g, t, 900); lua(g, 220, 300, 90);
    for (let f = 0; f < 4; f++) { const y = 800 + f * 230; for (let i = 0; i < 5; i++) casa(g, i * 250 - 80 + (f % 2) * 110, y, 190 + rnd(f * 7 + i) * 50, 130 + rnd(f + i * 3) * 80, { acesa: rnd(f * 11 + i) > 0.55, cor: ['#2A1C08', '#221706', '#1A1105', '#120C04'][f] });
      const cx = 170 + rnd(f + 40) * 740; cao(g, cx, y + 40, 0.28 + f * 0.07, { flip: f % 2, late: latir(t, f * 0.23, 0.9), cor: BREU }); }
    vgrad(g, 1560, H, 'rgba(10,7,3,0)', BREU); vinheta(g, 0.55);
  };
  CENARIOS.cc_responde = (g, t) => {
    ceu(g, t, 1100); lua(g, 540, 300, 76); casa(g, -80, 1000, 380, 330, { acesa: true }); casa(g, 780, 1000, 380, 330, { acesa: true });
    vgrad(g, 1000, H, '#3A2708', BREU); muro(g, 1250, 120); const vez = Math.floor(t / 0.75) % 2;
    cao(g, 230, 1255, 1.25, { late: vez === 0 ? latir(t, 0, 0.75) : 0, olho: CLARO }); cao(g, 850, 1255, 1.25, { flip: true, late: vez === 1 ? latir(t, 0, 0.75) : 0, olho: CLARO });
    const k = clamp((t - 2.6) / 1.4); if (k > 0) { g.save(); g.globalCompositeOperation = 'lighter'; vgrad(g, 500, 1000, 'rgba(0,0,0,0)', `rgba(150,90,10,${0.55 * k})`, 0, W); g.restore(); }
    vinheta(g, 0.58);
  };
  CENARIOS.cc_relogio = (g, t, c = {}) => {
    vgrad(g, 0, H, '#2A1C08', BREU); glow(g, 540, 780, 800, SODIO, 0.3); relogio(g, 540, 780, 370);
    const para = t >= (c.paraEm ?? 2.2), s = para ? (c.paraEm ?? 2.2) : t;
    const mao = (a, l, w, cor) => line(g, 540, 780, 540 + Math.sin(a) * l, 780 - Math.cos(a) * l, cor, w);
    mao(1.25 / 12 * TAU, 190, 34, BREU); mao(15 / 60 * TAU, 290, 22, BREU); mao(Math.floor(s * 1.0 + 56) / 60 * TAU, 320, 8, P.accent); circ(g, 540, 780, 24, P.accent);
    g.textAlign = 'center'; g.textBaseline = 'middle'; g.font = '700 62px "Geist Mono"'; g.fillStyle = para ? P.accent : SODIO; g.fillText('TERÇA  01:15', 540, 270); vinheta(g, 0.62);
  };
  CENARIOS.cc_calados = (g, t, c = {}) => {
    ceu(g, t, H); glow(g, 540, 620, 600, SODIO, 0.18);
    const v = out(clamp((t - 0.2) / 0.5));
    for (const [x, y, s, f] of [[190, 620, 0.75, 0], [880, 640, 0.75, 1], [330, 920, 0.95, 0], [780, 950, 0.95, 1]]) { rect(g, x - 200, y, 400, 26, '#3A2708'); cao(g, x, y, s, { flip: f, olho: v > 0.5 ? CLARO : 0 }); }
    if (c.meu) { const k = out(clamp((t - (c.meuEm ?? 1.2)) / 0.4)); rect(g, 0, 0, W, H, BREU, 0.8 * k); g.save(); g.globalAlpha = k; cao(g, 500, 1320, 2.1, { cor: '#6A4A1C', olho: OSSO }); curva(g, P.accent, 30, q => { q.moveTo(560, 800); q.lineTo(700, 835); }); g.restore(); }
    vinheta(g, 0.62);
  };
  CENARIOS.cc_mesa = (g, t) => {
    vgrad(g, 0, H, '#2A1C08', BREU); g.save(); g.translate(560, 40); g.scale(0.5, 0.5); janela(g, t, q => poste(q, t, 560, 600)); g.restore();
    vgrad(g, 700, 900, 'rgba(26,17,5,0)', '#1A1105', 0, W); rect(g, 0, 900, W, H - 900, '#1A1105');
    for (let i = 0; i < 9; i++) line(g, 540 + (i - 4) * 90, 900, 540 + (i - 4) * 330, H, '#3A2708', 5);
    poli(g, SODIO, [[620, 590], [980, 590], [700, 1500], [80, 1500]], 0.13);
    const tr = Math.sin(t * 38) * 5; g.save(); g.translate(tr, 0); cao(g, 400, 1330, 1.35, { cor: '#050301', olho: OSSO }); g.restore();
    for (const d of [-1, 1]) curva(g, SODIO, 8, q => { const x = 390 + d * 320; q.moveTo(x, 1050); q.quadraticCurveTo(x + d * 40 + tr, 1100, x, 1150); }, 0.7);
    rect(g, 40, 720, 880, 62, '#6A4510'); rect(g, 40, 782, 880, 22, BREU); for (const x of [80, 830]) rect(g, x, 790, 52, 580, '#4A300C');
    vinheta(g, 0.6);
  };
  CENARIOS.cc_fone = (g, t, c = {}) => fone(g, t, c);
  // unhas descendo pelo vidro
  CENARIOS.cc_unhas = (g, t) => {
    janela(g, t, q => { vulto(q, t, 640, 780, 1.05); });
    const k = clamp(t / 1.9);
    for (let i = 0; i < 4; i++) { const x = 330 + i * 105, y0 = 500 + Math.abs(i - 1.5) * 45, y = y0 + 420 * k + Math.sin(t * 23 + i) * 8;
      curva(g, OSSO, 7, q => { q.moveTo(x - 20, y0 - 40); q.quadraticCurveTo(x + 8, (y0 + y) / 2, x, y); }, 0.75);
      curva(g, BREU, 52, q => { q.moveTo(x + 150, y + 330); q.quadraticCurveTo(x + 20, y + 190, x, y + 40); }); poli(g, '#C9B784', [[x - 17, y + 45], [x + 17, y + 40], [x - 6, y - 12]]); }
    vinheta(g, 0.6);
  };
  CENARIOS.cc_vulto = (g, t, c = {}) => {
    const k = out(clamp(t / 0.9)), fala = c.fala ? Math.abs(Math.sin(t * 11)) * 0.5 : 0;
    janela(g, t, q => { poste(q, t, 690, 470, 0.7); vulto(q, t, 500, c.perto ? 720 : lerp(900, 780, k), c.perto ? 1.35 : 0.95, { boca: fala, olhos: c.olhos || 0 }); });
    if (c.fala) for (let i = 0; i < 3; i++) elipse(g, 540, 840, 90 + i * 70 + ((t * 60) % 70), 50 + i * 40, CLARO, 0.05);
    curva(g, OSSO, 5, q => { q.moveTo(270, 560); q.lineTo(300, 940); q.moveTo(340, 540); q.lineTo(366, 900); }, 0.3);
    vinheta(g, 0.6);
  };
  // a mão no trinco. c.solta: a mão recua a partir de c.soltaEm
  CENARIOS.cc_trinco = (g, t, c = {}) => {
    vgrad(g, 0, H, '#3A2708', '#0F0A03'); rect(g, 0, 0, 470, H, '#150E04'); vulto(g, t, 200, 560, 1.25, { olhos: c.solta ? 0.8 : 0 }); rect(g, 0, 0, 470, H, SODIO, 0.07);
    rect(g, 470, 0, 110, H, '#0A0602'); rect(g, 592, 0, 14, H, '#6A4A10');
    const sol = c.solta ? out(clamp((t - (c.soltaEm ?? 0.35)) / 0.5)) : 0;
    rrect(g, 430, 780, 300, 150, 8, '#8F7A48'); for (const [x, y] of [[462, 806], [698, 806], [462, 904], [698, 904]]) circ(g, x, y, 13, BREU);
    const gira = c.solta ? -0.12 * (1 - sol) : -0.35 * out(clamp(t / 2.2));
    g.save(); g.translate(580, 855); g.rotate(gira); rrect(g, -30, -32, 330, 64, 8, '#D8C488'); rect(g, -20, -22, 300, 10, '#FFF3C8'); circ(g, 300, 0, 46, '#D8C488'); g.restore();
    const tr = Math.sin(t * 31) * 5 * (1 - sol), mx = 790 + sol * 190 + (1 - out(clamp(t / 0.6))) * (c.solta ? 0 : 180), my = 810 + sol * 330 + tr;
    curva(g, '#4A2A14', 190, q => { q.moveTo(mx + 520, my + 640); q.lineTo(mx + 110, my + 90); }); elipse(g, mx + 40, my + 20, 130, 100, PELE, 1, 0.5);
    for (let i = 0; i < 4; i++) curva(g, PELE, 48, q => { const y = my - 55 + i * 47; q.moveTo(mx + 20, y + 15); q.quadraticCurveTo(mx - 70 - sol * 40, y - 20, mx - 105 - sol * 60, y + 25 - sol * 40); });
    vinheta(g, 0.62);
  };
  // a voz cala e começa a latir. c.late
  CENARIOS.cc_late = (g, t, c = {}) => {
    const em = c.lateEm ?? 99, k = c.late ? out(clamp((t - em) / 0.35)) : 0, l = k * (0.45 + 0.55 * latir(Math.max(0, t - em), 0, 0.62)), tr = k * Math.sin(t * 55) * 10;
    janela(g, t, q => { poste(q, t, 690, 470, 0.5); vulto(q, t, 540 + tr, 730, 1.5, { olhos: c.late ? 0.6 + 0.4 * k : clamp(t / 1.2), boca: l, cao: k }); });
    if (l > 0.4) for (let i = 1; i <= 3; i++) for (const d of [-1, 1]) curva(g, P.accent, 12, q => q.arc(540, 860, 260 + i * 80, d > 0 ? -0.35 : Math.PI - 0.35, d > 0 ? 0.35 : Math.PI + 0.35), l * (0.9 - i * 0.2));
    vinheta(g, 0.62);
  };

  // ───── sons: latido, vibração de telefone
  const ant = window.SfxExtra;
  window.SfxExtra = function (defs, h) {
    ant && ant(defs, h); const { G, F, O, N, C, bus, eco, rnd } = h;
    // latido: p.dur, p.intervalo, p.tom, p.abafa (corte do passa-baixa), p.n limita a quantidade
    defs.latido = function (t, p) {
      const dur = p.dur || 2, T = t + dur, out = G(0.5 * (p.vol == null ? 1 : p.vol)), per = p.intervalo || 0.6, tom = p.tom || 1; let n = 0;
      for (let s = t; s < T - 0.05 && n < (p.n || 99); s += per * rnd(0.8, 1.2), n++) for (const d of [0, p.duplo === false ? null : 0.17]) { if (d === null) continue; const a = s + d, o = O('sawtooth', 300 * tom, a, a + 0.18), nz = N(a, a + 0.18, true), bp = F('bandpass', 750 * tom, 1.6), lp = F('lowpass', p.abafa || 2600), g = G(0), gn = G(0.35);
        o.frequency.setValueAtTime(280 * tom, a); o.frequency.linearRampToValueAtTime(470 * tom, a + 0.035); o.frequency.exponentialRampToValueAtTime(190 * tom, a + 0.15);
        g.gain.setValueAtTime(0, a); g.gain.linearRampToValueAtTime(1, a + 0.015); g.gain.linearRampToValueAtTime(0.5, a + 0.08); g.gain.linearRampToValueAtTime(0, a + 0.16); C(o, bp); C(nz, gn, bp); C(bp, lp, g, out); }
      eco(out, out, 0.21, 0.28, 1500, p.eco == null ? 0.4 : p.eco); bus(out, false); return { t: t, fim: T + 0.6 };
    };
    // vibra: telefone vibrando na madeira (p.n pulsos)
    defs.vibra = function (t, p) {
      const n = p.n || 2, out = G(0.35 * (p.vol == null ? 1 : p.vol));
      for (let i = 0; i < n; i++) { const a = t + i * 0.42, o = O('square', 165, a, a + 0.28), am = O('square', 31, a, a + 0.28), lp = F('lowpass', 700), g = G(0), mod = G(0.5), v = G(0.5), ag = G(0.45); C(am, ag); ag.connect(v.gain); g.gain.setValueAtTime(0, a); g.gain.linearRampToValueAtTime(1, a + 0.02); g.gain.setValueAtTime(1, a + 0.24); g.gain.linearRampToValueAtTime(0, a + 0.28); C(o, lp, v, g, out); }
      bus(out, false); return { t: t, fim: t + n * 0.42 };
    };
  };
})();
