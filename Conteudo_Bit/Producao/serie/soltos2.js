// Cenários dos Shorts soltos, semana 1. Só ACRESCENTA ao Motor. Prefixo ab_ = Assobio dentro de casa (verde-petróleo, menta fria e o vermelho da marca).
(() => {
  const { CENARIOS } = Motor, W = Motor.W, H = Motor.H, { rect, poly, circ, line, rrect, glow, vgrad, vinheta, rnd, lerp, clamp, out, P } = Motor.H_;
  const TAU = Math.PI * 2, MENTA = '#CFEBDD', BREU = '#020807';
  const elipse = (g, x, y, rx, ry, c, a = 1, rot = 0) => { g.globalAlpha = a; g.fillStyle = c; g.beginPath(); g.ellipse(x, y, rx, ry, rot, 0, TAU); g.fill(); g.globalAlpha = 1; };
  const forma = (g, c, fn, a = 1) => { g.globalAlpha = a; g.fillStyle = c; g.beginPath(); fn(g); g.closePath(); g.fill(); g.globalAlpha = 1; };
  const curva = (g, c, lw, fn, a = 1) => { g.globalAlpha = a; g.strokeStyle = c; g.lineWidth = lw; g.lineCap = 'round'; g.lineJoin = 'round'; g.beginPath(); fn(g); g.stroke(); g.globalAlpha = 1; };
  // ondas do assobio: arcos que abrem a partir de (x,y). ini = instante(s); duas notas = dois pulsos
  function ondas(g, t, ini, x, y, o = {}) {
    if (ini == null) return; const r0 = o.r0 || 40, r1 = o.r1 || 340, cor = o.cor || P.accent;
    for (const s0 of [].concat(ini)) for (const dt of [0, 0.44]) { const u = t - s0 - dt; if (u < 0 || u > 1.3) continue;
      for (let i = 0; i < 3; i++) { const k = clamp(u * 1.15 - i * 0.17); if (k <= 0 || k >= 1) continue;
        for (const lado of o.lados || [0, Math.PI]) curva(g, cor, lerp(14, 5, k), q => q.arc(x, y, r0 + k * (r1 - r0), lado - 0.7, lado + 0.7), (1 - k) * 0.95); } }
  }
  const tabuas = (g, y0, cor, junta) => { vgrad(g, y0, H, cor, BREU); for (let i = -9; i <= 9; i++) line(g, 540 + i * 70, y0, 540 + i * 330, H, junta, 4, 0.7); for (let i = 1; i < 8; i++) rect(g, 0, y0 + Math.pow(i / 8, 1.7) * (H - y0), W, 3, junta, 0.5); };

  // ───── corredor da casa com a porta da cozinha ao fundo. c.ondas (s), c.vulto (s para atravessar), c.vultoEm
  CENARIOS.ab_corredor = (g, t, c = {}) => {
    const L = 340, R = 740, T = 520, B = 1220, f = 0.92 + 0.08 * Math.sin(t * 13) * Math.sin(t * 2.3);
    rect(g, 0, 0, W, H, BREU);
    poly(g, [[0, 0], [W, 0], [R, T], [L, T]], '#04120F'); poly(g, [[0, 0], [L, T], [L, B], [0, H]], '#0E332D'); poly(g, [[W, 0], [R, T], [R, B], [W, H]], '#0A2723');
    poly(g, [[0, H], [W, H], [R, B], [L, B]], '#14201C'); for (let i = -4; i <= 4; i++) line(g, 540 + i * 50, B, 540 + i * 250, H, BREU, 4, 0.8);
    poly(g, [[470, B], [610, B], [830, H], [250, H]], '#3A1612'); poly(g, [[488, B], [592, B], [740, H], [340, H]], '#4A1C16');
    for (let i = 1; i < 6; i++) { const k = i / 6; line(g, lerp(0, L, k), lerp(0, T, k), lerp(0, L, k), lerp(H, B, k), BREU, 5, 0.45); line(g, lerp(W, R, k), lerp(0, T, k), lerp(W, R, k), lerp(H, B, k), BREU, 5, 0.45); }
    const lat = (x0, x1, esq) => { const q = x => { const k = esq ? x / L : (W - x) / (W - R); return [lerp(0, T, k), lerp(H, B, k)]; }; const a = q(x0), b = q(x1), h0 = a[1] - a[0], h1 = b[1] - b[0]; poly(g, [[x0, a[0] + h0 * 0.28], [x1, b[0] + h1 * 0.28], [x1, b[1]], [x0, a[1]]], '#06100E'); circ(g, esq ? x1 - 16 : x1 + 16, b[0] + h1 * 0.66, 9, '#8FB8A4', 0.7); };
    lat(60, 210, true); lat(1020, 880, false);
    for (const [x, y, w, h] of [[250, 700, 56, 90], [776, 720, 50, 80]]) { rect(g, x, y, w, h, '#2E5A4C'); rect(g, x + 7, y + 7, w - 14, h - 14, '#071512'); }
    rect(g, L, T, R - L, B - T, '#0B2420'); rect(g, 424, 640, 232, 580, '#1C4A3F');
    g.save(); g.beginPath(); g.rect(442, 658, 196, 562); g.clip(); vgrad(g, 658, 1220, '#BFE6D2', '#3E7A66', 442, 196); g.globalAlpha = 1 - f; rect(g, 442, 658, 196, 562, BREU); g.globalAlpha = 1;
    rect(g, 442, 960, 120, 26, '#0E2A23'); rect(g, 458, 986, 14, 190, '#0E2A23'); rect(g, 600, 760, 38, 460, '#16403A'); rect(g, 442, 1176, 196, 44, '#1E4A3E');
    if (c.vulto) { const u = t - (c.vultoEm || 0); if (u > 0) { const x = lerp(720, 380, clamp(u / c.vulto)); elipse(g, x, 800, 42, 52, BREU); forma(g, BREU, q => { q.moveTo(x - 70, 1220); q.quadraticCurveTo(x - 90, 850, x, 850); q.quadraticCurveTo(x + 90, 850, x + 70, 1220); }); } }
    g.restore();
    glow(g, 540, 900, 520, '#9FE8C8', 0.34 * f); poly(g, [[442, B], [638, B], [880, H], [200, H]], MENTA, 0.12 * f);
    ondas(g, t, c.ondas, 540, 880, { r0: 60, r1: 440 });
    vinheta(g, 0.6);
  };

  // ───── a mesa de quem mora sozinho: uma cadeira, um prato, uma caneca
  CENARIOS.ab_mesa = (g, t) => {
    vgrad(g, 0, 1300, '#0F3A32', '#061815'); for (let y = 0; y < 900; y += 120) rect(g, 0, y, W, 3, BREU, 0.4); for (let x = 0; x < W; x += 120) rect(g, x, 0, 3, 900, BREU, 0.4);
    const bx = 540 + Math.sin(t * 1.1) * 12; line(g, 540, 0, bx, 420, BREU, 7); poly(g, [[bx - 110, 500], [bx - 46, 400], [bx + 46, 400], [bx + 110, 500]], '#1E4A3E'); elipse(g, bx, 508, 70, 24, '#F0FFF6'); glow(g, bx, 520, 600, '#BFF0D6', 0.35); poly(g, [[bx - 90, 505], [bx + 90, 505], [960, 1120], [120, 1120]], MENTA, 0.07);
    tabuas(g, 1380, '#10241F', BREU);
    rect(g, 400, 700, 280, 40, '#2A5A4A'); for (const x of [400, 652]) rect(g, x, 700, 28, 460, '#2A5A4A'); rect(g, 428, 810, 224, 24, '#2A5A4A'); // a única cadeira
    poly(g, [[170, 1080], [910, 1080], [1010, 1190], [70, 1190]], '#5E8A76'); rect(g, 70, 1190, 940, 44, '#2E5446'); for (const x of [120, 920]) rect(g, x, 1234, 42, 330, '#142E27');
    elipse(g, 470, 1134, 150, 42, '#DCEFE5'); elipse(g, 470, 1130, 104, 28, '#B2D2C3'); line(g, 650, 1108, 680, 1170, '#DCEFE5', 12);
    rrect(g, 730, 1010, 100, 124, 16, '#DCEFE5'); curva(g, '#DCEFE5', 16, q => q.arc(836, 1070, 34, -1.3, 1.3)); elipse(g, 780, 1014, 50, 14, '#0A201B');
    for (let i = 0; i < 2; i++) curva(g, MENTA, 6, q => { q.moveTo(760 + i * 34, 990); for (let k = 1; k <= 5; k++) q.lineTo(760 + i * 34 + Math.sin(t * 2 + k + i * 2) * 14, 990 - k * 30); }, 0.3);
    vinheta(g, 0.6);
  };

  // ───── despertador no criado-mudo. c.hora
  CENARIOS.ab_relogio = (g, t, c = {}) => {
    vgrad(g, 0, H, '#092420', '#020A09'); rect(g, 90, 190, 360, 520, BREU); vgrad(g, 210, 690, '#0E3A33', '#1F5A4E', 110, 320); rect(g, 264, 210, 12, 480, BREU); rect(g, 110, 444, 320, 12, BREU);
    poly(g, [[60, 1180], [1020, 1180], [1150, 1290], [-70, 1290]], '#17362E'); rect(g, 0, 1290, W, 60, '#0C201B'); rect(g, 0, 1350, W, H - 1350, '#051210');
    rrect(g, 150, 780, 780, 400, 44, '#12302A'); rrect(g, 178, 808, 724, 344, 28, '#010403'); for (const x of [260, 760]) rect(g, x, 1176, 70, 26, '#081614'); rrect(g, 400, 752, 280, 36, 16, '#1E4A3E');
    const pisca = t % 1 < 0.62;
    g.font = '700 210px "Geist Mono"'; g.letterSpacing = '0px'; g.textAlign = 'center'; g.textBaseline = 'middle';
    const h = c.hora || '02:07'; g.fillStyle = P.accent; g.shadowColor = P.accent; g.shadowBlur = 34; g.fillText(pisca ? h : h.replace(':', ' '), 540, 985); g.shadowBlur = 0; g.textAlign = 'left'; g.textBaseline = 'alphabetic';
    glow(g, 540, 990, 700, P.accent, 0.16);
    vinheta(g, 0.65);
  };

  // ───── a cama, de lado: ele deitado. c.abreEm (olhos abrem), c.vira (olha para a porta), c.ondas
  CENARIOS.ab_cama = (g, t, c = {}) => {
    vgrad(g, 0, 1300, '#0D332C', '#061916'); rect(g, 150, 250, 400, 500, BREU); vgrad(g, 270, 730, '#2A6A5A', '#12403A', 170, 360); circ(g, 440, 390, 54, MENTA, 0.9); glow(g, 440, 390, 330, '#BFF0D6', 0.3); rect(g, 344, 270, 12, 460, BREU); rect(g, 170, 494, 360, 12, BREU);
    rect(g, 830, 420, 220, 880, '#04100E'); rect(g, 852, 442, 176, 858, '#0A201B'); circ(g, 878, 880, 14, '#8FB8A4');
    poly(g, [[170, 750], [530, 750], [1000, 1300], [420, 1300]], MENTA, 0.07); tabuas(g, 1300, '#0E221D', BREU);
    rrect(g, 20, 830, 70, 560, 20, '#1C4034'); rect(g, 60, 1130, 960, 110, '#245244'); rect(g, 60, 1240, 960, 60, '#0C201B'); rect(g, 980, 1040, 50, 340, '#1C4034'); rect(g, 90, 1300, 40, 90, '#0C201B');
    rrect(g, 90, 1030, 330, 120, 56, '#C4E0D2');
    const hx = 285, hy = 985, resp = Math.sin(t * 2.2) * 6;
    elipse(g, hx - 12, hy - 8, 112, 100, '#0B0F0E'); elipse(g, hx + 6, hy + 6, 92, 90, '#9A7A66');
    forma(g, '#0B0F0E', q => { q.moveTo(hx - 90, hy); q.quadraticCurveTo(hx - 90, hy - 120, hx + 40, hy - 96); q.quadraticCurveTo(hx + 90, hy - 78, hx + 94, hy - 34); q.quadraticCurveTo(hx + 30, hy - 64, hx - 20, hy - 40); });
    const ab = c.abreEm == null ? 1 : out(clamp((t - c.abreEm) / 0.18)), olhar = c.vira ? lerp(-6, 9, out(clamp((t - 0.3) / 0.5))) : Math.sin(t * 0.8) * 3;
    for (const ex of [hx - 22, hx + 46]) { if (ab > 0.1) { elipse(g, ex, hy + 2, 21, 16 * ab, '#EAF6F0'); circ(g, ex + olhar, hy + 2, 9 * ab, '#07100D'); circ(g, ex + olhar + 4, hy - 2, 3 * ab, '#FFF'); } else curva(g, '#2A1C14', 6, q => q.arc(ex, hy - 4, 18, 0.2, Math.PI - 0.2)); curva(g, '#1A100C', 8, q => { q.moveTo(ex - 22, hy - 28 - 6 * ab); q.lineTo(ex + 20, hy - 30 - 6 * ab); }); }
    curva(g, '#5A3A30', 6, q => { q.moveTo(hx + 14, hy + 16); q.lineTo(hx + 24, hy + 36); q.lineTo(hx + 8, hy + 38); }); curva(g, '#3A1E1A', 7, q => { q.moveTo(hx - 6, hy + 62); q.lineTo(hx + 30, hy + 62); });
    forma(g, '#2E6A5A', q => { q.moveTo(250, 1090); q.quadraticCurveTo(420, 960 - resp, 600, 1010 - resp); q.quadraticCurveTo(760, 1056, 860, 1020); q.quadraticCurveTo(960, 1000, 1000, 1070); q.lineTo(1000, 1200); q.lineTo(250, 1200); });
    for (let i = 0; i < 4; i++) curva(g, '#143A30', 12, q => { q.moveTo(380 + i * 160, 1040 - resp * 0.5); q.quadraticCurveTo(420 + i * 160, 1110, 390 + i * 160, 1190); }, 0.8);
    for (let i = 0; i < 4; i++) rrect(g, 330 + i * 26, 1062 - resp, 22, 54, 10, '#9A7A66');
    ondas(g, t, c.ondas, 935, 800, { lados: [Math.PI], r1: 430 });
    vinheta(g, 0.6);
  };

  // ───── a cozinha escura: pia, geladeira, janela. c.ondas
  CENARIOS.ab_cozinha = (g, t, c = {}) => {
    vgrad(g, 0, 1300, '#0C2E28', '#051512'); for (let y = 640; y < 1000; y += 90) rect(g, 0, y, W, 3, BREU, 0.5); for (let x = 0; x < W; x += 90) rect(g, x, 640, 3, 360, BREU, 0.5);
    rect(g, 360, 300, 320, 320, BREU); vgrad(g, 316, 604, '#1F5A4E', '#0E3A33', 376, 288); rect(g, 515, 316, 10, 288, BREU); rect(g, 376, 455, 288, 10, BREU);
    for (const x of [30, 750]) { rect(g, x, 330, 300, 250, '#0A221D'); line(g, x + 150, 340, x + 150, 570, BREU, 5); for (const dx of [124, 176]) rect(g, x + dx - 5, 470, 10, 60, '#5E9A84'); }
    rect(g, 0, 1000, 760, 40, '#4A7A68'); rect(g, 0, 1040, 760, 280, '#0E2C25'); for (let i = 0; i < 3; i++) { rect(g, 30 + i * 245, 1080, 215, 210, '#12372E'); rect(g, 100 + i * 245, 1100, 76, 12, '#5E9A84'); }
    curva(g, '#8FC0AC', 18, q => { q.moveTo(250, 1000); q.lineTo(250, 880); q.quadraticCurveTo(260, 840, 330, 848); q.lineTo(332, 876); });
    const u = (t * 0.9) % 1; circ(g, 332, 886 + u * u * 110, 7, MENTA, 1 - u * 0.5);
    rrect(g, 800, 640, 260, 690, 22, '#5E8A76'); rect(g, 800, 866, 260, 8, '#12302A'); rect(g, 828, 760, 14, 80, '#BFE0D2'); rect(g, 828, 900, 14, 130, '#BFE0D2');
    tabuas(g, 1320, '#112620', BREU); poly(g, [[376, 1320], [664, 1320], [880, H], [200, H]], MENTA, 0.07); glow(g, 520, 460, 520, '#9FE8C8', 0.2);
    ondas(g, t, c.ondas, 540, 800, { r0: 50, r1: 450 });
    vinheta(g, 0.6);
  };

  // ───── a janela fechada, noite parada. c.treme (vidro balança)
  CENARIOS.ab_janela = (g, t, c = {}) => {
    vgrad(g, 0, H, '#0B2A24', '#041210'); const j = c.treme ? Math.sin(t * 31) * 4 * Math.max(0, Math.sin(t * 3)) : 0;
    rect(g, 170, 330, 740, 880, BREU); g.save(); g.translate(j, 0); vgrad(g, 360, 1180, '#1B5648', '#08241F', 200, 680); circ(g, 700, 540, 90, MENTA); glow(g, 700, 540, 460, '#BFF0D6', 0.3);
    for (let i = 0; i < 26; i++) { const x = 250 + rnd(i) * 310, y = 930 + rnd(i + 9) * 210; elipse(g, x + Math.sin(t * 0.8 + i) * 4, y, 70, 48, '#04100D'); } rect(g, 340, 980, 36, 200, '#04100D');
    rect(g, 522, 360, 36, 820, '#7FAE9A'); rect(g, 200, 750, 680, 26, '#7FAE9A'); for (const x of [200, 856]) rect(g, x, 360, 24, 820, '#7FAE9A'); rect(g, 200, 360, 680, 24, '#7FAE9A'); rect(g, 200, 1156, 680, 24, '#7FAE9A');
    rrect(g, 484, 822, 112, 44, 10, '#E4F2EA'); rrect(g, 524, 800, 34, 130, 14, '#E4F2EA'); circ(g, 541, 844, 14, '#1C4034'); line(g, 250, 460, 430, 400, MENTA, 10, 0.25); line(g, 250, 540, 360, 502, MENTA, 6, 0.2); g.restore();
    rect(g, 130, 1196, 820, 46, '#24564A');
    for (const e of [-1, 1]) { const x = 540 + e * 450, sw = Math.sin(t * 1.4 + e) * (c.treme ? 24 : 5); forma(g, '#3A1612', q => { q.moveTo(x - 140, 260); q.lineTo(x + 140, 260); q.quadraticCurveTo(x + 90, 800, x + 140 + sw, 1420); q.lineTo(x - 140 + sw, 1420); q.quadraticCurveTo(x - 80, 800, x - 140, 260); }); for (let i = -2; i <= 2; i++) curva(g, BREU, 10, q => { q.moveTo(x + i * 48, 280); q.quadraticCurveTo(x + i * 36, 800, x + i * 52 + sw, 1400); }, 0.45); }
    rect(g, 0, 236, W, 30, '#12201C'); vinheta(g, 0.6);
  };

  // ───── o trinco: a mão confere. c.testaEm (puxa e não abre)
  CENARIOS.ab_trinco = (g, t, c = {}) => {
    vgrad(g, 0, H, '#14463B', '#06181A'); for (let i = 0; i < 9; i++) line(g, 90 + i * 120, 0, 60 + i * 120, H, BREU, 4, 0.3);
    rect(g, 0, 380, W, 26, '#7FAE9A'); rect(g, 0, 1320, W, 26, '#7FAE9A'); vgrad(g, 406, 1320, '#0F3C34', '#071E1B'); poly(g, [[0, 560], [460, 406], [560, 406], [0, 700]], MENTA, 0.08);
    const u = t - (c.testaEm ?? 0.7), pux = u > 0 && u < 1.2 ? Math.abs(Math.sin(u * 12)) * 18 * (1 - u / 1.2) : 0;
    rrect(g, 200, 760, 300, 220, 18, '#7FAE9A'); rrect(g, 640, 790, 190, 160, 14, '#7FAE9A'); for (const [x, y] of [[232, 792], [232, 946], [468, 792], [468, 946], [800, 820], [800, 918]]) { circ(g, x, y, 13, '#2A5044'); line(g, x - 8, y - 8, x + 8, y + 8, '#0A201B', 4); }
    g.save(); g.translate(pux, 0); rrect(g, 330, 836, 420, 66, 30, '#E4F2EA'); rect(g, 330, 882, 420, 14, '#8FB8A4'); rrect(g, 392, 760, 52, 100, 24, '#E4F2EA'); g.restore();
    const e = out(clamp(t / 0.5)); g.save(); g.translate(418 + pux - (1 - e) * 300, 750 - (1 - e) * 500);
    line(g, -200, -170, -640, -480, '#12100F', 260); line(g, -120, -110, -230, -190, '#9A7A66', 160); elipse(g, -90, -80, 125, 96, '#A8866F', 1, 0.6);
    curva(g, '#A8866F', 66, q => { q.moveTo(-80, -60); q.quadraticCurveTo(10, -50, 10, 40); }); curva(g, '#A8866F', 62, q => { q.moveTo(-140, -20); q.quadraticCurveTo(-90, 60, -40, 76); });
    for (let i = 0; i < 3; i++) curva(g, '#8A6A56', 50, q => { q.moveTo(-60 + i * 38, -140 + i * 24); q.quadraticCurveTo(70 + i * 24, -150 + i * 40, 86 + i * 14, -60 + i * 44); });
    g.restore(); vinheta(g, 0.62);
  };

  // ───── a lembrança do avô: varanda de tábua e candeeiro (verde antigo)
  CENARIOS.ab_memoria = (g, t) => {
    const f = 0.85 + 0.15 * Math.sin(t * 9) * Math.sin(t * 3.7);
    vgrad(g, 0, 1300, '#4E5A3A', '#222A1C'); for (let x = 0; x < W; x += 108) { rect(g, x, 0, 8, 1300, BREU, 0.4); rect(g, x + 12, 0, 3, 1300, '#E8E4B8', 0.08); }
    rect(g, 90, 330, 330, 430, '#12180F'); vgrad(g, 348, 742, '#1E3A30', '#2E5040', 108, 294); circ(g, 210, 450, 40, '#DCE8C0'); rect(g, 250, 348, 10, 394, '#12180F'); rect(g, 108, 540, 294, 10, '#12180F');
    line(g, 850, 0, 850, 520, BREU, 5); rrect(g, 810, 600, 80, 76, 14, '#6A5A30'); rrect(g, 818, 520, 64, 86, 26, '#F4EBB0', 0.55); forma(g, '#FFF3B8', q => { q.moveTo(850, 532 - 8 * f); q.quadraticCurveTo(874, 580, 850, 598); q.quadraticCurveTo(826, 580, 850, 532 - 8 * f); }); glow(g, 850, 580, 700, '#E8E08A', 0.32 * f);
    tabuas(g, 1300, '#2A301C', BREU); rect(g, 700, 1010, 340, 26, '#171C10'); for (const x of [720, 1000]) rect(g, x, 1036, 26, 280, '#171C10');
    vinheta(g, 0.6);
  };

  // ───── planta da casa: o caminho da cozinha até a cama se desenha em vermelho. c.de, c.dura
  CENARIOS.ab_planta = (g, t, c = {}) => {
    vgrad(g, 0, H, '#0C2A25', '#04100E'); for (let x = 0; x < W; x += 60) rect(g, x, 0, 2, H, MENTA, 0.07); for (let y = 0; y < H; y += 60) rect(g, 0, y, W, 2, MENTA, 0.07);
    const parede = (a, b, d, e) => line(g, a, b, d, e, MENTA, 14, 0.9);
    parede(120, 320, 960, 320); parede(120, 320, 120, 1250); parede(960, 320, 960, 1250); parede(120, 1250, 960, 1250); parede(120, 660, 360, 660); parede(500, 660, 960, 660); parede(120, 880, 560, 880); parede(700, 880, 960, 880); parede(620, 320, 620, 520);
    rect(g, 170, 370, 200, 70, MENTA, 0.25); for (const x of [215, 305]) circ(g, x, 405, 22, BREU, 0.8); rect(g, 830, 370, 80, 160, MENTA, 0.25); rect(g, 180, 960, 220, 240, MENTA, 0.22); rect(g, 196, 974, 188, 60, MENTA, 0.5); rect(g, 700, 400, 130, 130, MENTA, 0.18);
    g.font = '700 38px "Geist Mono"'; g.letterSpacing = '4px'; g.fillStyle = MENTA; g.textAlign = 'center'; g.fillText('COZINHA', 255, 615); g.fillText('CORREDOR', 770, 785); g.fillText('QUARTO', 650, 1140); g.textAlign = 'left'; g.letterSpacing = '0px';
    const pts = [[290, 470], [430, 590], [430, 720], [580, 790], [630, 880], [620, 990], [470, 1075], [370, 1090]], k = clamp((t - (c.de ?? 0.15)) / (c.dura ?? 2.2)); let tot = 0; const seg = pts.slice(1).map((p, i) => { const d = Math.hypot(p[0] - pts[i][0], p[1] - pts[i][1]); tot += d; return d; });
    let r = k * tot, px = pts[0][0], py = pts[0][1]; g.setLineDash([34, 26]); curva(g, P.accent, 18, q => { q.moveTo(px, py); for (let i = 0; i < seg.length && r > 0; i++) { const f = Math.min(1, r / seg[i]); px = lerp(pts[i][0], pts[i + 1][0], f); py = lerp(pts[i][1], pts[i + 1][1], f); q.lineTo(px, py); r -= seg[i]; } }); g.setLineDash([]);
    circ(g, px, py, 24, P.accent); glow(g, px, py, 160, P.accent, 0.55);
    vinheta(g, 0.55);
  };

  // ───── olhos no escuro, só o rosto. c.lado (olha para a porta)
  CENARIOS.ab_olhos = (g, t, c = {}) => {
    vgrad(g, 0, H, '#081F1B', '#020807'); glow(g, 980, 800, 900, '#9FE8C8', 0.24);
    elipse(g, 540, 880, 430, 470, '#6A5A4C'); elipse(g, 590, 870, 370, 440, '#8C7464'); forma(g, '#0A0E0D', q => { q.moveTo(80, 900); q.quadraticCurveTo(60, 330, 540, 350); q.quadraticCurveTo(1020, 340, 1000, 920); q.quadraticCurveTo(900, 590, 760, 620); q.lineTo(690, 690); q.lineTo(600, 580); q.lineTo(500, 670); q.lineTo(400, 590); q.quadraticCurveTo(190, 610, 80, 900); });
    const olhar = (c.lado == null ? 0 : lerp(0, 48, out(clamp((t - c.lado) / 0.4)))) + Math.sin(t * 23) * 2.5;
    for (const ex of [375, 705]) { const d = ex < 540 ? -1 : 1;
      curva(g, '#150E0B', 26, q => { q.moveTo(ex - 108, 726 + (d < 0 ? 14 : -26)); q.lineTo(ex + 108, 726 + (d < 0 ? -26 : 14)); });
      g.save(); g.beginPath(); g.ellipse(ex, 850, 124, 102, 0, 0, TAU); g.clip(); rect(g, ex - 140, 720, 280, 260, '#E6F4EC'); circ(g, ex + olhar, 854, 58, '#2A3E30'); circ(g, ex + olhar, 854, 28, '#030605'); circ(g, ex + olhar + 24, 828, 13, '#FFF'); g.restore();
      curva(g, '#150E0B', 13, q => q.ellipse(ex, 850, 124, 102, 0, Math.PI, TAU)); }
    curva(g, '#4A342A', 16, q => { q.moveTo(548, 920); q.lineTo(520, 1040); q.lineTo(566, 1056); });
    for (let i = 0; i < 4; i++) { const u = (t * 0.35 + i * 0.27) % 1; elipse(g, [255, 830, 770, 320][i], 640 + u * 360, 9, 15, MENTA, 0.8 * (1 - u)); }
    forma(g, '#1F5346', q => { q.moveTo(-60, 1180); q.quadraticCurveTo(300, 1090, 540, 1130); q.quadraticCurveTo(800, 1080, W + 60, 1190); q.lineTo(W + 60, H + 60); q.lineTo(-60, H + 60); });
    for (const x of [280, 800]) for (let i = 0; i < 4; i++) rrect(g, x - 76 + i * 40, 1090 + (i % 3 ? 0 : 16), 36, 110, 17, '#8C7464');
    for (let i = 0; i < 5; i++) line(g, 80 + i * 230, 1240, i * 270, H, BREU, 16, 0.4);
    vinheta(g, 0.65);
  };

  // ───── a porta do quarto vista por dentro, luz na fresta. c.chegaEm (pés chegam), c.saiEm (vão embora), c.ondas, c.semPes
  CENARIOS.ab_porta = (g, t, c = {}) => {
    vgrad(g, 0, 1350, '#0A2822', '#04100E'); tabuas(g, 1330, '#0C1E1A', BREU);
    rect(g, 220, 330, 640, 1000, '#245244'); vgrad(g, 360, 1322, '#143A31', '#0A201B', 250, 580);
    for (const [y, h] of [[420, 300], [790, 190], [1030, 220]]) for (const x of [300, 570]) { rect(g, x, y, 210, h, '#061511'); rect(g, x + 14, y + 14, 182, h - 28, '#12342C'); }
    rrect(g, 726, 880, 56, 130, 20, '#8FC0AC'); rrect(g, 640, 920, 130, 36, 18, '#DCEFE5');
    const luz = '#D8FFEA'; rect(g, 250, 1300, 580, 36, luz); glow(g, 540, 1325, 520, '#9FE8C8', 0.42); poly(g, [[250, 1336], [830, 1336], [1040, 1760], [40, 1760]], luz, 0.13);
    if (!c.semPes) { const ch = c.chegaEm == null ? 1 : out(clamp((t - c.chegaEm) / 0.6)), sai = c.saiEm == null ? 0 : clamp((t - c.saiEm) / 1.6);
      for (const [i, dx] of [[0, -80], [1, 80]]) { const passo = sai > 0 ? Math.max(0, Math.sin(sai * 11 + i * Math.PI)) * 14 : 0, x = 540 + dx * (1 - sai * 0.45) + lerp(-420, 0, ch) + sai * 330, w = 108 * (1 - sai * 0.45), a = ch * (1 - Math.pow(sai, 1.5));
        rect(g, x - w / 2, 1298 - passo, w, 40, BREU, a); poly(g, [[x - w / 2, 1336], [x + w / 2, 1336], [x + w / 2 + dx * 1.2 + 24, 1620], [x - w / 2 + dx * 1.2 - 24, 1620]], BREU, 0.6 * a); } }
    ondas(g, t, c.ondas, 540, 640, { r0: 70, r1: 480 });
    vinheta(g, 0.6);
  };

  // ───── close da maçaneta. c.desceEm/c.desce (desce devagar), c.voltaEm/c.volta
  CENARIOS.ab_macaneta = (g, t, c = {}) => {
    vgrad(g, 0, H, '#17463A', '#05140F'); rect(g, 790, 0, 60, H, BREU, 0.85); rect(g, 850, 0, 230, H, '#08201B'); rect(g, 850, 0, 10, H, MENTA, 0.35);
    for (const [y, h] of [[120, 500], [1280, 520]]) { rect(g, 90, y, 580, h, '#0A261F'); rect(g, 124, y + 34, 512, h - 68, '#143C32'); }
    let a = 0; if (c.desce) a = clamp((t - (c.desceEm || 0)) / c.desce); if (c.volta) a = 1 - clamp((t - (c.voltaEm || 0)) / c.volta);
    a = a * a * (3 - 2 * a); const treme = c.desce && a > 0.02 && a < 0.98 ? Math.sin(t * 40) * 0.006 : 0;
    rrect(g, 550, 720, 180, 520, 80, '#7FAE9A'); rrect(g, 566, 736, 148, 488, 66, '#A9CDBD'); circ(g, 640, 1120, 30, BREU); rect(g, 628, 1120, 24, 70, BREU);
    g.save(); g.translate(640, 880); g.rotate(-a * 0.72 + treme); rrect(g, -440 + 26, -34 + 46, 480, 80, 38, BREU, 0.45); rrect(g, -440, -44, 480, 82, 40, '#DCEFE5'); rect(g, -400, 14, 400, 14, '#6A9A86'); rect(g, -396, -28, 340, 9, '#FFFFFF', 0.8); circ(g, -2, -2, 74, '#C4E0D2'); circ(g, -2, -2, 40, '#6A9A86'); g.restore();
    glow(g, 400, 760, 560, '#9FE8C8', 0.2); vinheta(g, 0.68);
  };

  // ───── a boca no escuro. c.preso (segura o ar), c.soltaEm (ar sai), c.ondas (o ar assobia)
  CENARIOS.ab_boca = (g, t, c = {}) => {
    vgrad(g, 0, H, '#07201B', '#020807'); glow(g, 940, 620, 900, '#9FE8C8', 0.22);
    forma(g, '#6A5A4C', q => { q.moveTo(60, 0); q.lineTo(1020, 0); q.quadraticCurveTo(1040, 900, 760, 1190); q.quadraticCurveTo(540, 1340, 320, 1190); q.quadraticCurveTo(40, 900, 60, 0); });
    forma(g, '#8C7464', q => { q.moveTo(230, 0); q.lineTo(960, 0); q.quadraticCurveTo(980, 860, 740, 1130); q.quadraticCurveTo(540, 1270, 380, 1120); q.quadraticCurveTo(200, 880, 230, 0); });
    if (c.preso) for (const [x, d] of [[300, -1], [780, 1]]) { elipse(g, x, 850, 150, 130, '#9C8070', 0.75); curva(g, '#5A4438', 9, q => q.arc(x - d * 10, 850, 128, d < 0 ? 0.5 : Math.PI - 1.7, d < 0 ? 1.7 : Math.PI - 0.5), 0.6); }
    curva(g, '#4A342A', 22, q => { q.moveTo(486, 330); q.quadraticCurveTo(470, 520, 430, 590); q.quadraticCurveTo(460, 650, 505, 630); q.quadraticCurveTo(540, 668, 580, 630); q.quadraticCurveTo(624, 650, 650, 590); q.quadraticCurveTo(610, 520, 596, 330); }); for (const x of [482, 598]) elipse(g, x, 612, 30, 15, '#150C09');
    curva(g, '#5A4034', 8, q => { q.moveTo(512, 690); q.lineTo(520, 760); q.moveTo(568, 690); q.lineTo(560, 760); }, 0.7);
    const bico = c.soltaEm == null ? 0 : out(clamp((t - c.soltaEm) / 0.5));
    if (c.preso) { forma(g, '#6A2E28', q => { q.moveTo(400, 860); q.quadraticCurveTo(470, 830, 540, 848); q.quadraticCurveTo(610, 830, 680, 860); q.quadraticCurveTo(540, 900, 400, 860); }); curva(g, '#1E0A08', 12, q => { q.moveTo(386, 860); q.lineTo(694, 860); }); }
    else { const w = lerp(160, 104, bico), up = lerp(40, 70, bico), dn = lerp(50, 88, bico), ab = lerp(6, 26, bico); // bico de assobio: dois lábios franzidos e uma abertura pequena
      forma(g, '#6A2E28', q => { q.moveTo(540 - w, 860); q.bezierCurveTo(540 - w * 0.75, 860 - up, 540 - w * 0.28, 860 - up * 1.15, 540, 860 - up * 0.72); q.bezierCurveTo(540 + w * 0.28, 860 - up * 1.15, 540 + w * 0.75, 860 - up, 540 + w, 860); q.quadraticCurveTo(540, 880, 540 - w, 860); });
      forma(g, '#8A3E34', q => { q.moveTo(540 - w, 860); q.quadraticCurveTo(540, 850, 540 + w, 860); q.bezierCurveTo(540 + w * 0.66, 860 + dn * 1.15, 540 - w * 0.66, 860 + dn * 1.15, 540 - w, 860); });
      elipse(g, 540, 862, lerp(96, 34, bico), ab, '#0C0302'); curva(g, '#2A0E0A', 8, q => { q.moveTo(540 - w, 860); q.lineTo(540 - lerp(92, 34, bico), 862); q.moveTo(540 + lerp(92, 34, bico), 862); q.lineTo(540 + w, 860); });
      for (const dx of [-54, -22, 22, 54]) { curva(g, '#3A140F', 6, q => { q.moveTo(540 + dx * 0.7, 862 - ab - 8); q.lineTo(540 + dx, 862 - up * 0.72); q.moveTo(540 + dx * 0.7, 862 + ab + 8); q.lineTo(540 + dx, 862 + dn * 0.66); }, bico * 0.75); }
      curva(g, '#D8A090', 8, q => { q.moveTo(540 - w * 0.4, 860 + dn * 0.7); q.quadraticCurveTo(540 - w * 0.05, 860 + dn * 0.86, 540 + w * 0.22, 860 + dn * 0.72); }, 0.45); }
    if (c.soltaEm != null && t > c.soltaEm) for (let i = 0; i < 46; i++) { const u = (((t - c.soltaEm) * 0.55 + rnd(i)) % 1 + 1) % 1, k = clamp((t - c.soltaEm) / 0.6); circ(g, 540 + (rnd(i + 20) - 0.5) * (60 + u * 640), 890 + u * 520, 12 + u * 60, MENTA, 0.16 * (1 - u) * k); }
    ondas(g, t, c.ondas, 540, 860, { r0: 130, r1: 500 });
    vinheta(g, 0.65);
  };

  // ───── debaixo da cama: o estrado em cima, o breu e dois olhos. c.olhosEm, c.ondas, c.dedos (s)
  CENARIOS.ab_embaixo = (g, t, c = {}) => {
    vgrad(g, 0, H, '#0B2A24', '#04100E'); tabuas(g, 1130, '#2A5A4A', BREU); glow(g, 540, 1560, 760, '#9FE8C8', 0.22);
    rect(g, 70, 560, 940, 640, '#010302'); const sombra = g.createLinearGradient(0, 1120, 0, 1380); sombra.addColorStop(0, '#010302'); sombra.addColorStop(1, 'rgba(1,3,2,0)'); g.fillStyle = sombra; g.fillRect(70, 1195, 940, 185);
    for (let i = 0; i < 9; i++) rect(g, 100 + i * 105, 560, 34, 70, '#12342C', 0.7);
    forma(g, '#2E6A5A', q => { q.moveTo(0, 210); q.lineTo(W, 210); q.lineTo(W, 500); for (let i = 8; i >= 0; i--) q.quadraticCurveTo(i * 135 + 70, 600 + (i % 3) * 34 + Math.sin(t + i) * 5, i * 135, 500); q.lineTo(0, 500); });
    for (let i = 0; i < 8; i++) curva(g, '#143A30', 14, q => { q.moveTo(70 + i * 135, 240); q.lineTo(80 + i * 135, 520); }, 0.7);
    rect(g, 0, 120, W, 110, '#C4E0D2', 0.5); rect(g, 0, 480, W, 22, '#0A201B', 0.5);
    for (const x of [40, 980]) { rect(g, x, 420, 62, 900, '#1C4034'); rect(g, x + 8, 420, 8, 900, MENTA, 0.25); }
    const o = c.olhosEm == null ? 0 : out(clamp((t - c.olhosEm) / 0.45)), pisca = c.olhosEm != null && t > c.olhosEm + 1.7 && t < c.olhosEm + 1.82 ? 0.1 : 1;
    if (o > 0) for (const ex of [450, 630]) { glow(g, ex, 860, 190, P.accent, 0.6 * o); elipse(g, ex, 860, 40, 24 * o * pisca, P.accent); elipse(g, ex, 860, 8, 18 * o * pisca, '#FFE2DA'); }
    if (c.dedos != null) { const e = out(clamp((t - c.dedos) / 0.9)); if (e > 0) for (const [bx, d] of [[270, -1], [810, 1]]) { g.save(); g.translate(bx, 1040 + e * 90);
      forma(g, '#4A6A5C', q => { q.moveTo(-70, -150); q.lineTo(70, -150); q.quadraticCurveTo(118, -20, 96, 34); q.lineTo(-96, 34); q.quadraticCurveTo(-118, -20, -70, -150); }, e); // dorso da mão saindo do breu
      [-72, -26, 22, 68].forEach((x, i) => { const L = [112, 150, 160, 124][d < 0 ? i : 3 - i], jx = x * 1.22, jy = 30 + L * 0.5, px = x * 1.12 + d * 6, py = 30 + L;
        curva(g, '#7FA896', 38, q => { q.moveTo(x, 14); q.lineTo(jx, jy); }, e); curva(g, '#7FA896', 28, q => { q.moveTo(jx, jy); q.lineTo(px, py); }, e); circ(g, jx, jy, 21, '#8FB8A6', e); circ(g, x, 20, 22, '#8FB8A6', e); elipse(g, px, py + 2, 9, 17, '#17302A', e); });
      g.restore(); } }
    ondas(g, t, c.ondas, 540, 1000, { r0: 80, r1: 500 });
    vinheta(g, 0.6);
  };

  Motor.AB = { ondas };
})();
