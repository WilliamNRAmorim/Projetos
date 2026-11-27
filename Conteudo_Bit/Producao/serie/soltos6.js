// Cenários e som do Short solto 06 (a mãe chamando). Só ACRESCENTA ao Motor. Prefixo mc_ = sala à luz azul da TV, cozinha amarela e o vermelho da marca no avental.
(() => {
  const { CENARIOS } = Motor, W = Motor.W, H = Motor.H, { rect, circ, line, rrect, glow, vgrad, vinheta, lerp, clamp, out, P } = Motor.H_;
  const TAU = Math.PI * 2, BREU = '#070D22', PAREDE = '#13265A', PAREDE2 = '#24478C', TV = '#8CCBFF', AMARELO = '#FFD23F', CREME = '#FFF0B0', SOFA = '#2B3F74', SOFA2 = '#1B2A54', PELE = '#C98F6A', PELE2 = '#8E5F55', CABELO = '#120C14', OSSO = '#EAF4FF', BLUSA = '#7D5BA6', PIJAMA = '#3E9C9A', MADEIRA = '#4A2E3A';
  const elipse = (g, x, y, rx, ry, c, a = 1, rot = 0) => { g.globalAlpha = a; g.fillStyle = c; g.beginPath(); g.ellipse(x, y, rx, ry, rot, 0, TAU); g.fill(); g.globalAlpha = 1; };
  const forma = (g, c, fn, a = 1) => { g.globalAlpha = a; g.fillStyle = c; g.beginPath(); fn(g); g.closePath(); g.fill(); g.globalAlpha = 1; };
  const curva = (g, c, lw, fn, a = 1) => { g.globalAlpha = a; g.strokeStyle = c; g.lineWidth = lw; g.lineCap = 'round'; g.lineJoin = 'round'; g.beginPath(); fn(g); g.stroke(); g.globalAlpha = 1; };
  const poli = (g, c, pts, a = 1) => forma(g, c, q => pts.forEach(([x, y], i) => i ? q.lineTo(x, y) : q.moveTo(x, y)), a);
  const pisca = t => 0.82 + 0.1 * Math.sin(t * 7.3) + 0.08 * Math.sin(t * 17.1);
  const fim = g => vinheta(g, 0.34);

  // ───── peças
  function parede(g, t, chao = 1230) { vgrad(g, 0, chao, BREU, PAREDE); for (let x = 60; x < W; x += 170) rect(g, x, 0, 5, chao, PAREDE2, 0.35); vgrad(g, chao, H, '#101C42', '#040817'); rect(g, 0, chao - 14, W, 16, PAREDE2); }
  // silhueta de avental: (x,y) = pés
  function sombra(g, x, y, s, o = {}) { g.save(); g.translate(x, y); g.scale(s, s); const p = Math.sin((o.passo || 0) * 6) * 30, C = '#0A0610';
    for (const d of [-1, 1]) curva(g, C, 44, q => { q.moveTo(d * 30, -180); q.lineTo(d * 40 + p * d, -10); });
    poli(g, C, [[-70, -520], [70, -520], [120, -150], [-120, -150]]); for (const d of [-1, 1]) curva(g, C, 38, q => { q.moveTo(d * 66, -490); q.lineTo(d * 120, -290); });
    circ(g, 0, -600, 70, C); circ(g, -40, -660, 40, C);
    poli(g, P.accent, [[-36, -450], [36, -450], [46, -350], [82, -170], [-82, -170], [-46, -350]]); curva(g, P.accent, 9, q => { q.moveTo(-34, -448); q.lineTo(-24, -535); q.moveTo(34, -448); q.lineTo(24, -535); q.moveTo(-46, -350); q.lineTo(-96, -340); q.moveTo(46, -350); q.lineTo(96, -340); });
    g.restore(); }
  // porta da cozinha. o.luz 0..1, o.sombra = posição -1..1
  function porta(g, t, x, y, w, h, o = {}) { const L = o.luz ?? 0.12;
    rect(g, x - 26, y - 26, w + 52, h + 26, MADEIRA); rect(g, x, y, w, h, '#05070F');
    g.save(); g.beginPath(); g.rect(x, y, w, h); g.clip();
    if (L > 0.3) { rect(g, x, y, w, h, AMARELO, L); rect(g, x, y + h * 0.55, w, h * 0.05, '#C8861E', L); for (let i = 0; i < 3; i++) rect(g, x + w * (0.08 + i * 0.32), y + h * 0.14, w * 0.2, h * 0.2, CREME, L); rect(g, x, y + h * 0.85, w, h * 0.15, '#B8741C', L); for (let i = 0; i < 4; i++) { line(g, x + w * (0.15 + i * 0.22), y, x + w * (0.15 + i * 0.22), y + h * 0.07, MADEIRA, 6); circ(g, x + w * (0.15 + i * 0.22), y + h * 0.09, w * 0.05, '#8A4A22', L); } }
    else { poli(g, AMARELO, [[x + w * 0.76, y], [x + w * 0.83, y], [x + w * 0.9, y + h], [x + w * 0.7, y + h]], 0.35 + L); }
    if (o.sombra != null) sombra(g, x + w / 2 + o.sombra * w * 0.85, y + h * 1.02, h / 760, { passo: t });
    g.restore();
    if (L > 0.3) { glow(g, x + w / 2, y + h / 2, w * 1.5, AMARELO, 0.35 * L); poli(g, AMARELO, [[x, y + h], [x + w, y + h], [x + w + 260, H], [x - 260, H]], 0.22 * L); } }
  // busto/rosto: (x,y) = centro da cabeça. o.mae, o.olho (-1..1), o.medo, o.boca ('o' aberta), o.cansada, o.vermelho (olhos)
  function pessoa(g, t, x, y, s, o = {}) { g.save(); g.translate(x, y); g.scale(s, s); const mae = o.mae, pele = o.pele || PELE;
    if (mae) { circ(g, 0, -118, 58, CABELO); elipse(g, 0, 6, 122, 128, CABELO); } else { forma(g, CABELO, q => { q.moveTo(0, -130); q.bezierCurveTo(-160, -120, -120, 80, -150, 220); q.lineTo(150, 220); q.bezierCurveTo(120, 80, 160, -120, 0, -130); }); }
    rect(g, -32, 80, 64, 80, PELE2); forma(g, o.roupa || (mae ? BLUSA : PIJAMA), q => { q.moveTo(-210, 430); q.quadraticCurveTo(-190, 140, 0, 135); q.quadraticCurveTo(190, 140, 210, 430); });
    elipse(g, 0, 0, 96, 116, pele); forma(g, TV, q => q.ellipse(0, 0, 96, 116, 0, -1.3, 1.3), 0.22);
    forma(g, CABELO, q => { q.moveTo(-104, 10); q.quadraticCurveTo(-110, -130, 0, -128); q.quadraticCurveTo(110, -130, 104, 10); q.quadraticCurveTo(70, -72, mae ? 0 : 30, -78); q.quadraticCurveTo(-60, -60, -104, 10); });
    const ol = (o.olho || 0) * 11, pisc = (t % 3.1) > 2.95 && !o.fixo;
    for (const d of [-1, 1]) { if (o.vermelho) { glow(g, d * 36, -8, 56, P.accent, 0.85 * o.vermelho); circ(g, d * 36, -8, 11, P.accent); continue; }
      elipse(g, d * 36, -8, 23, pisc ? 2 : o.medo ? 20 : 13, OSSO); if (!pisc) { circ(g, d * 36 + ol, -8, o.medo ? 7 : 10, CABELO); circ(g, d * 36 + ol + 4, -12, 3, TV); }
      curva(g, CABELO, 6, q => { q.moveTo(d * 12, o.medo ? -50 : -34); q.lineTo(d * 60, o.medo ? -38 : -36); });
      if (o.cansada) curva(g, PELE2, 5, q => { q.moveTo(d * 18, 15); q.quadraticCurveTo(d * 36, 24, d * 56, 14); }, 0.9); }
    curva(g, PELE2, 5, q => { q.moveTo(2, 8); q.lineTo(-8, 36); q.lineTo(6, 38); });
    if (o.boca === 'o') elipse(g, 0, 70, 22, 18 + 10 * Math.abs(Math.sin(t * 8)), '#3A0E18'); else if (o.sorri) curva(g, '#4A1420', 6, q => { q.moveTo(-44, 58); q.quadraticCurveTo(0, 96, 44, 58); }); else curva(g, '#6A2430', 7, q => { q.moveTo(-28, 68); q.lineTo(28, 68); });
    g.restore(); }
  // sofá visto de frente com as duas
  function sofa(g, t, y, a, b) { rrect(g, 20, y - 120, 760, 420, 60, SOFA2);
    pessoa(g, t, 240, y - 150, 0.95, a); pessoa(g, t, 560, y - 175, 1.05, Object.assign({ mae: 1 }, b));
    rrect(g, 10, y + 150, 780, 200, 50, SOFA); for (const x of [-20, 720]) rrect(g, x, y + 40, 130, 330, 50, '#38508F'); line(g, 400, y + 165, 400, y + 330, SOFA2, 8); }
  function ondas(g, t, x, y, k = 1, c = AMARELO, a = 1, dir = -1) { for (let i = 0; i < 3; i++) { const f = (t * 1.3 + i / 3) % 1; curva(g, c, 13 * k, q => q.arc(x, y, (50 + f * 240) * k, dir < 0 ? Math.PI - 0.75 : -0.75, dir < 0 ? Math.PI + 0.75 : 0.75), (1 - f) * a); } }
  const luzTV = (g, t, a = 0.35) => glow(g, 260, 1750, 1100, TV, a * pisca(t));
  // televisão; o.vol = nível da barra
  function telona(g, t, x, y, w, h, o = {}) { glow(g, x + w / 2, y + h / 2, w * 0.95, TV, 0.5 * pisca(t)); rrect(g, x - 22, y - 22, w + 44, h + 44, 14, '#03050C'); const f = Math.floor(t * 2.2);
    g.save(); g.beginPath(); g.rect(x, y, w, h); g.clip(); rect(g, x, y, w, h, ['#BFE6FF', '#7FB8F5', '#A9D2FF'][f % 3]); rect(g, x, y + h * 0.7, w, h * 0.3, '#2F66B8');
    elipse(g, x + w * (0.3 + 0.2 * (f % 3)), y + h * 0.55, w * 0.09, h * 0.2, PAREDE2); elipse(g, x + w * (0.3 + 0.2 * (f % 3)), y + h * 0.98, w * 0.2, h * 0.26, PAREDE2); for (let i = 0; i < 12; i++) rect(g, x, y + ((i * 47 + t * 90) % h), w, 3, OSSO, 0.18);
    if (o.vol != null) { rect(g, x, y + h * 0.5, w, h * 0.5, '#0A1A44', 0.85); for (let i = 0; i < 12; i++) rect(g, x + w * 0.08 + i * w * 0.071, y + h * 0.8 - i * h * 0.018, w * 0.045, h * 0.1 + i * h * 0.018, i < o.vol * 12 ? (i > 8 ? P.accent : OSSO) : '#25427E'); }
    g.restore(); }
  function costas(g, t, y, s = 1) { for (const [x, mae] of [[360, 0], [720, 1]]) { elipse(g, x, y + 190, 175 * s, 160 * s, '#050918'); circ(g, x, y, 108 * s, '#050918'); if (mae) circ(g, x, y - 105 * s, 52 * s, '#050918'); curva(g, TV, 6, q => q.arc(x, y, 108 * s, -2.7, -0.45), 0.8 * pisca(t)); } rrect(g, 70, y + 200, 940, 500, 70, '#0B1334'); rect(g, 110, y + 214, 860, 8, TV, 0.35); }

  // ───── cenários
  const sala = (g, t, o = {}) => { parede(g, t); porta(g, t, 700, 420, 320, 810, o); luzTV(g, t, 0.4); };
  // gancho e volta: as duas no sofá, a voz sai da porta
  CENARIOS.mc_gancho = (g, t) => { sala(g, t, { luz: 0.2 }); sofa(g, t, 1060, { medo: 1, olho: 1 }, { fixo: 1, olho: -0.2 }); ondas(g, t, 960, 640, 1, AMARELO, clamp(0.4 + t * 3)); fim(g); };
  CENARIOS.mc_lado = (g, t) => { parede(g, t, 1500); luzTV(g, t, 0.55); rrect(g, -60, 940, 1200, 700, 80, SOFA2); pessoa(g, t, 285, 940, 1.7, { medo: 1, olho: 1 }); pessoa(g, t, 775, 870, 1.85, { mae: 1, fixo: 1 }); const a = clamp((t - 0.35) * 2.5); if (a > 0) curva(g, P.accent, 14, q => q.ellipse(775, 850, 255, 320, 0, -1.6, -1.6 + TAU * a)); fim(g); };
  CENARIOS.mc_tv = (g, t) => { parede(g, t, 1260); porta(g, t, 790, 360, 230, 900, { luz: 0.14 }); telona(g, t, 90, 520, 600, 420); rect(g, 130, 990, 520, 120, '#0A1130'); costas(g, t, 1150); const a = clamp((t - 2.2) * 3); if (a > 0) ondas(g, t, 950, 620, 0.9, AMARELO, a); fim(g); };
  CENARIOS.mc_voz = (g, t) => { parede(g, t, 1420); porta(g, t, 290, 330, 500, 1090, { luz: 0.26 }); ondas(g, t, 700, 780, 1.4, CREME, 1, -1); ondas(g, t, 380, 780, 1.4, CREME, 1, 1); fim(g); };
  CENARIOS.mc_igual = (g, t) => { parede(g, t, 1500); luzTV(g, t, 0.45); porta(g, t, 780, 250, 250, 640, { luz: 0.26 }); pessoa(g, t, 370, 850, 2.25, { mae: 1, cansada: 1, fixo: 1 }); ondas(g, t, 900, 560, 0.85); const a = clamp((t - 1.2) * 2); g.save(); g.setLineDash([26, 24]); g.lineDashOffset = -t * 60; curva(g, P.accent, 12, q => { q.moveTo(850, 400); q.quadraticCurveTo(640, 230, 430, 460); }, a); g.restore(); fim(g); };
  CENARIOS.mc_olhei = (g, t) => { parede(g, t, 1500); luzTV(g, t, 0.55); const k = out(clamp((t - 0.15) / 0.6)); pessoa(g, t, 540, 820, 3.1, { medo: 1, olho: lerp(-0.8, 1.25, k), fixo: 1 }); fim(g); };
  CENARIOS.mc_parada = (g, t) => { parede(g, t, 1500); luzTV(g, t, 0.6); pessoa(g, t, 540, 800, 3.0, { mae: 1, fixo: 1 }); for (const d of [-1, 1]) rect(g, 540 + d * 108 - 22, 750, 26, 20, TV, pisca(t)); fim(g); };
  CENARIOS.mc_pulso = (g, t) => { rect(g, 0, 0, W, H, SOFA2); for (let y = 80; y < H; y += 260) curva(g, SOFA, 30, q => { q.moveTo(-50, y); q.quadraticCurveTo(540, y + 90, 1130, y); }); luzTV(g, t, 0.55); const k = out(clamp((t - 0.1) / 0.45)), aperta = 1 - 0.08 * clamp((t - 0.7) * 3);
    curva(g, PIJAMA, 270, q => { q.moveTo(-150, 1180); q.lineTo(250, 1010); }); curva(g, PELE, 170, q => { q.moveTo(250, 1010); q.lineTo(760, 820); }); elipse(g, 830, 795, 140, 100, PELE, 1, -0.35); for (let i = 0; i < 4; i++) curva(g, PELE, 44, q => { q.moveTo(880, 740 + i * 40); q.lineTo(1030, 660 + i * 66); });
    g.save(); g.translate(lerp(420, 0, k), lerp(-420, 0, k)); curva(g, BLUSA, 260, q => { q.moveTo(1180, 260); q.lineTo(720, 640); }); elipse(g, 610, 760, 130, 105, '#E0A584', 1, -0.5); for (let i = 0; i < 4; i++) curva(g, '#E0A584', 56 * aperta, q => { const x = 470 + i * 74, y = 800 - i * 30; q.moveTo(x + 60, y - 50); q.quadraticCurveTo(x - 50, y + 20, x + 5, y + 200 * aperta); }); g.restore();
    if (t > 0.65) for (let i = 0; i < 4; i++) { const x = 200 + i * 55; curva(g, P.accent, 14, q => { q.moveTo(x, 700 - i * 50); q.lineTo(x + 70, 760 - i * 45); }, clamp((t - 0.65) * 5) * (1 - i * 0.18)); } fim(g); };
  CENARIOS.mc_boca = (g, t) => { parede(g, t, 1500); luzTV(g, t, 0.55); pessoa(g, t, 540, 640, 3.7, { mae: 1, fixo: 1, olho: -0.1 }); const a = clamp((t - 0.2) * 3); if (a > 0) curva(g, P.accent, 13, q => q.ellipse(540, 892, 215, 100, 0, 0, TAU * a)); fim(g); };
  CENARIOS.mc_conta = (g, t) => { parede(g, t, 1500); luzTV(g, t, 0.65); pessoa(g, t, 540, 860, 5.4, { mae: 1, fixo: 1, olho: t < 0.9 ? 0 : -0.5 }); for (const d of [-1, 1]) rect(g, 540 + d * 195 - 36, 760, 44, 34, TV, pisca(t)); fim(g); };
  CENARIOS.mc_insiste = (g, t) => { parede(g, t, 1420); porta(g, t, 390, 300, 560, 1120, { luz: 0.22 }); ondas(g, t, 770, 760, 1.5, P.accent, 1, -1); luzTV(g, t, 0.25); pessoa(g, t, 200, 880, 1.3, { medo: 1, olho: 1, fixo: 1 }); fim(g); };
  CENARIOS.mc_acende = (g, t) => { const L = t < 0.55 ? 0.1 : t < 0.68 ? 1 : t < 0.78 ? 0.15 : 1; parede(g, t, 1260); porta(g, t, 310, 330, 460, 930, { luz: L }); luzTV(g, t, 0.2); costas(g, t, 1250, 0.9); fim(g); };
  CENARIOS.mc_sombra = (g, t) => { parede(g, t, 1420); porta(g, t, 230, 260, 620, 1160, { luz: 1, sombra: lerp(-0.5, 0.5, clamp(t / 3.4)) }); fim(g); };
  CENARIOS.mc_gritar = (g, t) => { parede(g, t, 1500); glow(g, 1080, 700, 800, AMARELO, 0.55); luzTV(g, t, 0.4); const tr = Math.sin(t * 55) * 6; pessoa(g, t, 540 + tr, 770, 3.0, { medo: 1, boca: 'o', olho: 0.9, fixo: 1 }); fim(g); };
  CENARIOS.mc_volume = (g, t) => { parede(g, t, 1260); const v = clamp(0.3 + t * 0.4); telona(g, t, 110, 330, 860, 600, { vol: v }); ondas(g, t, 130, 630, 0.6 + v, TV, 0.8, -1); ondas(g, t, 950, 630, 0.6 + v, TV, 0.8, 1);
    curva(g, BLUSA, 190, q => { q.moveTo(1180, 1650); q.lineTo(760, 1300); }); g.save(); g.translate(600, 1190); g.rotate(-0.5); rrect(g, -75, -190, 150, 390, 34, '#0A0C14'); circ(g, 0, -135, 22, P.accent); for (let i = 0; i < 6; i++) circ(g, -28 + (i % 2) * 56, -60 + Math.floor(i / 2) * 60, 17, '#59637E'); circ(g, -28, -60, 22, (t * 4) % 1 > 0.5 ? OSSO : '#59637E'); g.restore();
    elipse(g, 700, 1260, 105, 80, PELE, 1, -0.5); curva(g, PELE, 52, q => { q.moveTo(660, 1230); q.quadraticCurveTo(560, 1140, 572, 1110 + Math.abs(Math.sin(t * 12)) * 14); }); fim(g); };
  CENARIOS.mc_cansar = (g, t) => { const a = 1 - clamp((t - 0.4) / 1.8); parede(g, t, 1260); porta(g, t, 750, 330, 280, 930, { luz: 1 }); telona(g, t, 80, 560, 540, 390); if (a > 0) ondas(g, t * 0.6, 890, 640, a, P.accent, a); costas(g, t, 1160);
    const cx = 360, cy = 270; circ(g, cx, cy, 150, OSSO); circ(g, cx, cy, 128, BREU); line(g, cx, cy, cx + Math.sin(t * 3.4) * 105, cy - Math.cos(t * 3.4) * 105, OSSO, 12); line(g, cx, cy, cx + Math.sin(t * 0.6 + 1) * 70, cy - Math.cos(t * 0.6 + 1) * 70, P.accent, 16); fim(g); };
  CENARIOS.mc_apagou = (g, t) => { const L = t < 0.4 ? 1 : 0.05; parede(g, t, 1420); porta(g, t, 290, 330, 500, 1090, { luz: L }); const k = clamp((t - 0.75) * 3); if (k > 0) for (const d of [-1, 1]) { glow(g, 500 + d * 40, 660, 52, P.accent, 0.85 * k); g.globalAlpha = k; circ(g, 500 + d * 40, 660, 10, P.accent); g.globalAlpha = 1; } luzTV(g, t, 0.3); fim(g); };
  // fechadura da porta da rua; a chave gira
  CENARIOS.mc_chave = (g, t) => { vgrad(g, 0, H, '#1B3270', '#0A1233'); for (const x of [90, 570]) for (const y of [150, 1020]) { rrect(g, x, y, 420, 780, 20, '#23408A'); rrect(g, x + 40, y + 40, 340, 700, 14, '#172C66'); }
    rrect(g, 340, 480, 400, 760, 60, '#C99B2E'); circ(g, 540, 780, 130, AMARELO); circ(g, 540, 780, 92, '#8A6518'); const k = out(clamp((t - 0.35) / 0.5)), a = k * Math.PI / 2, ent = out(clamp(t / 0.3));
    g.save(); g.translate(540, 780); g.rotate(a); g.scale(lerp(1.7, 1, ent), lerp(1.7, 1, ent)); rrect(g, -105, -40, 210, 80, 36, OSSO); circ(g, 60, 0, 16, '#7C879E'); rect(g, -150, -18, 60, 36, '#DDE6F2'); curva(g, '#AAB6CC', 12, q => q.arc(150, 40, 60, 0, TAU)); rrect(g, 170, 80, 90, 150, 24, P.accent); g.restore();
    if (k > 0.05) curva(g, CREME, 14, q => q.arc(540, 780, 270, -2.6, -2.6 + 2.2 * k), 0.9); fim(g); };
  // a mãe de verdade chega com as sacolas
  function sacola(g, x, y, s) { g.save(); g.translate(x, y); g.scale(s, s); curva(g, OSSO, 12, q => q.arc(0, 0, 55, Math.PI, TAU)); for (const [dx, c] of [[-45, '#5DA64C'], [10, '#F28C28'], [55, '#E9DDB8']]) circ(g, dx, -8, 38, c); poli(g, '#D9A86C', [[-110, 0], [110, 0], [88, 240], [-88, 240]]); rect(g, -100, 60, 200, 14, '#B07F48'); g.restore(); }
  CENARIOS.mc_mercado = (g, t) => { parede(g, t, 1330); const k = out(clamp(t / 0.7)); rect(g, 190, 230, 700, 1100, MADEIRA); vgrad(g, 260, 1330, '#7A5AC8', '#F29A6B', 220, 640); circ(g, 740, 420, 55, CREME); glow(g, 540, 800, 700, '#F7B58A', 0.4 * k);
    const y = 590 - Math.abs(Math.sin(t * 5)) * 14 * (1 - clamp(t - 2)), s = lerp(1.2, 1.5, k); pessoa(g, t, 540, y, s, { mae: 1, cansada: 1 }); for (const d of [-1, 1]) { curva(g, BLUSA, 66, q => { q.moveTo(540 + d * 200, y + 300); q.lineTo(540 + d * 290, 920); }); circ(g, 540 + d * 290, 920, 40, PELE); sacola(g, 540 + d * 290, 970, 1.15); }
    poli(g, '#2A1C30', [[220, 260], [lerp(220, 70, k), 190], [lerp(220, 70, k), 1380], [220, 1330]]); fim(g); };
  CENARIOS.mc_filha = (g, t) => { vgrad(g, 0, H, '#5A3F9A', '#241A55'); rect(g, 0, 0, 120, H, MADEIRA); rect(g, 960, 0, 120, H, MADEIRA); glow(g, 540, 700, 800, '#F7B58A', 0.45); pessoa(g, t, 540, 780, 2.8, { mae: 1, cansada: 1, medo: t > 1.1, boca: t < 0.8 ? 'o' : null }); fim(g); };
  // o que ela vê: a filha e a outra no sofá, virando
  CENARIOS.mc_quem = (g, t) => { sala(g, t, { luz: 0.1 }); const k = clamp((t - 0.7) / 0.5); sofa(g, t, 1060, { medo: 1, olho: 1, fixo: 1 }, { roupa: BLUSA, pele: '#AFC2DC', fixo: 1, vermelho: k, sorri: k > 0.5, olho: -1 });
    poli(g, P.accent, [[505, 1060], [615, 1060], [675, 1215], [445, 1215]]); curva(g, P.accent, 12, q => { q.moveTo(510, 1065); q.lineTo(488, 1005); q.moveTo(610, 1065); q.lineTo(632, 1005); }); fim(g); };

  // ───── som: televisão, interruptor, chave e sacolas
  const ant = window.SfxExtra;
  window.SfxExtra = function (defs, h) {
    ant && ant(defs, h); const { G, F, N, C, dec, bus, rnd: r } = h;
    // tvFala: murmúrio de televisão (ruído em formantes, ritmo de sílabas)
    defs.tvFala = function (t, p) { const dur = p.dur || 6, T = t + dur, out = G(0.5 * (p.vol == null ? 1 : p.vol)), n = N(t, T, true), bp = F('bandpass', 800, 3), lp = F('lowpass', p.corte || 2400), g = G(0);
      for (let s = t; s < T - 0.2; s += r(0.12, 0.3)) { bp.frequency.setValueAtTime(r(350, 1500), s); g.gain.setValueAtTime(0, s); g.gain.linearRampToValueAtTime(r(0.3, 1), s + 0.04); g.gain.linearRampToValueAtTime(0, s + 0.11); }
      C(n, bp, lp, g, out); bus(out, true); return { t: t, fim: T }; };
    defs.interruptor = function (t, p) { const out = G(0.6 * (p.vol == null ? 1 : p.vol)); for (const d of [0, 0.05]) { const n = N(t + d, t + d + 0.05), hp = F('highpass', 1800), g = G(0); dec(g.gain, t + d, 0.001, d ? 0.5 : 1, 0.012); C(n, hp, g, out); } bus(out, false); return { t: t, fim: t + 0.2 }; };
    defs.chaveGira = function (t, p) { const out = G(0.5 * (p.vol == null ? 1 : p.vol)); for (const [d, f, a] of [[0, 3200, 0.6], [0.12, 2500, 0.5], [0.3, 2900, 0.5], [0.58, 900, 1], [0.66, 600, 0.8]]) { const n = N(t + d, t + d + 0.12), bp = F('bandpass', f, 6), g = G(0); dec(g.gain, t + d, 0.001, a * 2, 0.025); C(n, bp, g, out); } bus(out, false); return { t: t, fim: t + 1 }; };
    defs.sacolas = function (t, p) { const dur = p.dur || 1.5, T = t + dur, out = G(0.35 * (p.vol == null ? 1 : p.vol)), n = N(t, T, true), hp = F('highpass', 2600), g = G(0);
      for (let s = t; s < T - 0.1; s += r(0.03, 0.14)) { g.gain.setValueAtTime(0, s); g.gain.linearRampToValueAtTime(r(0.2, 1), s + 0.004); g.gain.linearRampToValueAtTime(0, s + 0.03); } C(n, hp, g, out); bus(out, false); return { t: t, fim: T }; };
  };
})();
