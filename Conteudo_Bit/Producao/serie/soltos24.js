// Cenários e som do Short solto 24 (Pisca-pisca). Só ACRESCENTA ao Motor. Prefixo pk_ = noite azul-ultramar elétrico, lâmpadas verde-menta, branco quente, silhuetas azul-breu e o vermelho da marca.
// Retrato: irmãos só em silhueta, sem ferimento. Nenhuma piscada em tela cheia; lâmpadas trocam no máximo 1,5 vez por segundo.
(() => {
  const { CENARIOS } = Motor, W = Motor.W, { rect, circ, glow, vgrad, vinheta, lerp, clamp, out, rnd } = Motor.H_, RED = Motor.H_.P.accent;
  const TAU = Math.PI * 2, AZUL = '#2130D8', AZUL2 = '#121A86', NOITE = '#0A0F4C', BREU = '#03041A', VULTO = '#0C1160', MENTA = '#2CF28C', LUZ = '#FFF4E4', LAV = '#8E9BFF';
  const elipse = (g, x, y, rx, ry, c, a = 1, rot = 0) => { g.globalAlpha = a; g.fillStyle = c; g.beginPath(); g.ellipse(x, y, Math.max(0, rx), Math.max(0, ry), rot, 0, TAU); g.fill(); g.globalAlpha = 1; };
  const forma = (g, c, fn, a = 1) => { g.globalAlpha = a; g.fillStyle = c; g.beginPath(); fn(g); g.closePath(); g.fill(); g.globalAlpha = 1; };
  const curva = (g, c, lw, fn, a = 1) => { g.globalAlpha = a; g.strokeStyle = c; g.lineWidth = lw; g.lineCap = 'round'; g.lineJoin = 'round'; g.beginPath(); fn(g); g.stroke(); g.globalAlpha = 1; };
  const poli = (g, c, pts, a = 1) => forma(g, c, q => pts.forEach(([x, y], i) => i ? q.lineTo(x, y) : q.moveTo(x, y)), a);
  // palavra grande: encolhe sozinha para caber em `max` (margem lateral mesmo com o zoom da câmera)
  const texto = (g, s, x, y, tam, c, a = 1, borda = BREU, max = 840) => { if (a <= 0) return; g.save(); g.globalAlpha = a; g.font = `900 ${tam}px Geist`; const m = g.measureText(s).width; if (m > max) { tam = Math.floor(tam * max / m); g.font = `900 ${tam}px Geist`; } g.textAlign = 'center'; g.textBaseline = 'middle'; g.lineJoin = 'round'; if (borda) { g.strokeStyle = borda; g.lineWidth = tam * 0.17; g.strokeText(s, x, y); } g.fillStyle = c; g.fillText(s, x, y); g.restore(); };
  const fim = g => vinheta(g, 0.14);
  const C = (n, fn) => { fn.claro = true; CENARIOS['pk_' + n] = fn; };
  const zoom = (g, k, cx, cy, fn) => { g.save(); g.translate(cx, cy); g.scale(k, k); g.translate(-cx, -cy); fn(); g.restore(); };
  const todo = (g, c, a = 1) => { g.globalAlpha = a; rect(g, -300, -700, W + 600, 3320, c); g.globalAlpha = 1; };
  const titulo = (g, a, b, t, em = 0.4, y = 290, cb = MENTA) => { texto(g, a, 540, y, 170, LUZ); if (b) texto(g, b, 540, y + 190, 180, cb, clamp((t - em) * 6)); };
  const passo = (t, d = 0.7) => Math.floor(Math.max(0, t) / d);
  const COR3 = [MENTA, RED, MENTA];

  // ───── peças
  function ceu(g) { todo(g, AZUL); vgrad(g, 0, 1300, AZUL, AZUL2, -300, W + 600); rect(g, -300, 1300, W + 600, 1400, AZUL2); for (let i = 0; i < 40; i++) circ(g, rnd(i + 2) * 1080, rnd(i + 31) * 900, 2 + rnd(i + 7) * 3, LUZ, 0.5); }
  const chao = (g, y = 1270, c = BREU) => rect(g, -300, y, W + 600, 2600 - y, c);
  function lampada(g, x, y, r, c, a = 1) { if (a > 0.3) glow(g, x, y, r * 5, c, 0.55 * a); elipse(g, x, y, r, r * 1.3, a > 0.3 ? c : NOITE); }
  // cordão em arco; as cores trocam de vizinha a cada 0,7 s
  function cordao(g, x0, y0, x1, y1, n, t, o = {}) { const cai = o.cai == null ? 40 : o.cai; curva(g, BREU, 8, q => { q.moveTo(x0, y0); q.quadraticCurveTo((x0 + x1) / 2, (y0 + y1) / 2 + cai * 2, x1, y1); }); const k = passo(t); for (let i = 0; i < n; i++) { const u = (i + 0.5) / n, x = lerp(x0, x1, u), y = lerp(y0, y1, u) + 4 * cai * u * (1 - u) + 18; lampada(g, x, y, o.r || 13, [MENTA, RED, LUZ][(i + k) % 3], o.a == null ? 0.85 : o.a); } }
  // casa de frente; (x,y) = meio da base; o.letra acesa na fachada
  function casa(g, x, y, s, t, o = {}) { g.save(); g.translate(x, y); g.scale(s, s); rect(g, -150, -300, 300, 300, BREU); poli(g, BREU, [[-185, -290], [0, -450], [185, -290]]); rect(g, 70, -430, 42, 90, BREU);
    const a = o.a == null ? 1 : o.a;
    if (o.letra) { const c = o.cor || MENTA; if (a > 0) { glow(g, 0, -150, 230, c, 0.7 * a); texto(g, o.letra, 0, -140, 250, c, a, null); } else texto(g, o.letra, 0, -140, 250, NOITE, 1, null); }
    else for (const k of [-1, 1]) rect(g, k * 70 - 35, -200, 70, 90, a > 0 ? LAV : NOITE);
    const luz = a > 0 ? null : 0; cordao(g, -185, -290, 0, -450, 5, t, { cai: 6, r: 12, a: luz }); cordao(g, 0, -450, 185, -290, 5, t, { cai: 6, r: 12, a: luz }); g.restore(); }
  const rua = (g, t, ac = () => 1, y = 1200, s = 0.95) => ['B', 'I', 'A'].forEach((l, i) => casa(g, 540 + (i - 1) * 368 * s, y + (i === 1 ? -40 : 0), s, t, { letra: l, cor: COR3[i], a: ac(i) }));
  // cabeça e tronco; (x,y) = base; o.olhos = [cor esquerda, cor direita]; o.letras = nas pupilas
  function gente(g, x, y, s, o = {}) { const c = o.cor || BREU; g.save(); g.translate(x, y); g.scale(s, s);
    forma(g, c, q => { q.moveTo(-160, 0); q.quadraticCurveTo(-160, -225, 0, -228); q.quadraticCurveTo(160, -225, 160, 0); }); rect(g, -34, -260, 68, 50, c); circ(g, 0, -330, 105, c);
    for (let i = -2; i <= 2; i++) poli(g, c, [[i * 38 - 30, -415], [i * 44, -465 - (i % 2 ? 14 : 0)], [i * 38 + 30, -415]]); for (const k of [-1, 1]) elipse(g, k * 108, -325, 18, 30, c);
    if (o.olhos) o.olhos.forEach((cor, i) => { const px = (i ? 1 : -1) * 44, py = -325; if (!cor) return; glow(g, px, py, 80, cor, 0.85); circ(g, px, py, 26, cor); if (o.letras && o.letras[i]) texto(g, o.letras[i], px, py + 2, 40, BREU, 1, null); else circ(g, px - 8, py - 9, 7, LUZ); });
    if (o.boca === 'sorri') curva(g, LUZ, 8, q => { q.moveTo(-34, -272); q.quadraticCurveTo(0, -248, 34, -272); });
    if (o.boca === 'fala') elipse(g, 0, -264, 18, 7 + 12 * Math.abs(Math.sin(o.t * 13)), LUZ);
    g.restore(); }
  const sala = g => { todo(g, NOITE); vgrad(g, 200, 1300, NOITE, AZUL2, -300, W + 600); };
  function janela(g, x, y, w, h, fn) { rect(g, x - 22, y - 22, w + 44, h + 44, BREU); g.save(); g.beginPath(); g.rect(x, y, w, h); g.clip(); rect(g, x, y, w, h, AZUL); fn && fn(); g.restore(); rect(g, x - 40, y + h + 18, w + 80, 26, BREU); }
  // pano da cortina: f = quanto fechou (0 a 1)
  function cortina(g, x, y, w, h, f) { for (const k of [-1, 1]) { const lw = lerp(70, w / 2 + 14, f), bx = k < 0 ? x - 20 : x + w + 20 - lw; rect(g, bx, y - 30, lw, h + 70, LAV); for (let i = 1; i < 5; i++) rect(g, bx + i * lw / 5 - 7, y - 30, 14, h + 70, AZUL, 0.9); } rect(g, x - 60, y - 52, w + 120, 24, BREU); }
  function celular(g, t, msgs) { rect(g, 190, 580, 700, 720, BREU); rect(g, 215, 610, 650, 665, LUZ); rect(g, 215, 610, 650, 100, AZUL2); texto(g, 'GRUPO DA RUA', 540, 663, 60, LUZ, 1, null, 580); msgs.forEach(([linhas, em, y]) => { const k = out(clamp((t - em) / 0.25)); if (k <= 0) return; const h = linhas.length * 78 + 40, yy = y + 40 * (1 - k); g.globalAlpha = k; rect(g, 250, yy, 580, h, NOITE); rect(g, 250, yy, 14, h, RED); g.globalAlpha = 1; linhas.forEach((l, i) => texto(g, l, 548, yy + 59 + i * 78, 62, LUZ, k, null, 520)); }); }
  const escuro = g => { todo(g, BREU); glow(g, 540, 950, 720, AZUL2, 0.9); };
  const irmao = (g, o) => gente(g, 540, o.y, o.s, Object.assign({ cor: VULTO }, o));

  // ───── cenários (os primeiros deixam o texto abaixo da cartela de abertura)
  C('gancho', (g, t) => { ceu(g); rua(g, t, () => 1, 1230, 0.84); chao(g, 1220); texto(g, 'SEU NOME', 540, 600, 180, LUZ); texto(g, 'NAS LUZES', 540, 765, 170, MENTA); fim(g); });
  C('tv', (g, t) => { sala(g); rect(g, 100, 880, 880, 360, BREU); rect(g, 135, 912, 810, 296, AZUL2); ['B', 'I', 'A'].forEach((l, i) => { glow(g, 290 + i * 250, 1060, 130, COR3[i], 0.5); g.save(); g.translate(290 + i * 250, 1060); g.scale(-1, 1); texto(g, l, 0, 0, 200, COR3[i], 0.9, null); g.restore(); }); poli(g, LUZ, [[180, 912], [330, 912], [135, 1170], [135, 990]], 0.12); chao(g, 1262); titulo(g, 'NO REFLEXO', 'DA TV', t, 0.25, 580); fim(g); });
  C('letras', (g, t) => { ceu(g); rua(g, t, i => t > 0.15 + i * 0.67 ? 1 : 0, 1215); chao(g, 1205); titulo(g, 'CADA CASA', 'UMA LETRA', t, 0.35, 520); fim(g); });
  C('bia', (g, t) => { todo(g, BREU); ['B', 'I', 'A'].forEach((l, i) => { const a = out(clamp((t - i * 0.4) / 0.2)), y = 500 + i * 320; if (a <= 0) return; glow(g, 540, y, 330, COR3[i], 0.55 * a); texto(g, l, 540, y, 350, COR3[i], a, null); }); });
  C('vizinho', (g, t) => { ceu(g); casa(g, 540, 1220, 1.35, t); janela(g, 435, 900, 210, 220, () => { glow(g, 540, 1010, 200, LUZ, 0.9); gente(g, 540, 1150, 0.45); }); curva(g, RED, 16, q => { q.moveTo(665, 1110); q.bezierCurveTo(900, 1140, 800, 1220, 960, 1235); }); rect(g, 940, 1205, 70, 55, RED); chao(g, 1215); curva(g, RED, 16, q => { q.moveTo(840, 1190); q.quadraticCurveTo(880, 1235, 950, 1232); }); titulo(g, 'COISA DO', 'VIZINHO?', t, 0.3); fim(g); });
  C('grupo', (g, t) => { sala(g); const s = Math.sin(t * 55) * 14 * (1 - clamp(t / 0.8)); g.save(); g.translate(s, 0); celular(g, t, [[['1 mensagem'], 0.15, 880]]); g.restore(); chao(g, 1320); titulo(g, 'O GRUPO', 'APITOU', t, 0.3, 240); fim(g); });
  C('quem', (g, t) => { sala(g); celular(g, t, [[['Quem ainda', 'está olhando?'], 0, 810]]); chao(g, 1320); titulo(g, 'QUEM AINDA', 'ESTÁ OLHANDO?', t, 0.5, 240); fim(g); });
  C('seguida', (g, t) => { sala(g); celular(g, t, [[['Quem ainda', 'está olhando?'], -1, 750], [['...'], 0.15, 1000]]); chao(g, 1320); titulo(g, 'EM', 'SEGUIDA', t, 0.2, 240); fim(g); });
  C('feche', (g, t) => { sala(g); celular(g, t, [[['Quem ainda', 'está olhando?'], -1, 750], [['Feche a cortina.', 'Não olhe direto.'], 0, 1000]]); chao(g, 1320); titulo(g, 'NÃO OLHE', 'DIRETO', t, 1, 240, RED); fim(g); });
  C('fechei', (g, t) => { sala(g); janela(g, 190, 640, 700, 560, () => rua(g, t, () => 1, 1195, 0.62)); cortina(g, 190, 640, 700, 560, out(clamp(t / 0.55))); chao(g); texto(g, 'FECHEI', 540, 380, 230, LUZ); fim(g); });
  C('pano', (g, t) => { sala(g); cortina(g, 190, 640, 700, 560, 1); ['B', 'I', 'A'].forEach((l, i) => { const a = passo(t, 0.67) % 3 === i ? 1 : 0.25, x = 330 + i * 210; glow(g, x, 920, 220, COR3[i], 0.75 * a); texto(g, l, x, 920, 210, COR3[i], a, a > 0.5 ? BREU : null); }); chao(g); titulo(g, 'ATRAVESSAVA', 'O PANO', t, 0.3); fim(g); });
  C('escada', (g, t) => { sala(g); for (let i = 0; i < 7; i++) rect(g, -60 + i * 170, 620 + i * 100, 175, 900, i % 2 ? BREU : '#060928'); const u = out(clamp(t / 1.8)); gente(g, lerp(280, 710, u), lerp(830, 1125, u) - Math.abs(Math.sin(t * 9)) * 20 * (1 - u), 0.8, { cor: LAV, olhos: t > 1.1 ? [MENTA, MENTA] : null }); chao(g); titulo(g, 'MEU IRMÃO', 'DESCEU', t, 0.3); fim(g); });
  C('lindo', (g, t) => { sala(g); glow(g, 540, 950, 650, LAV, 0.8); zoom(g, lerp(1, 1.08, clamp(t / 2.5)), 540, 1000, () => irmao(g, { y: 1500, s: 1.65, cor: BREU, olhos: [LUZ, LUZ], boca: 'fala', t })); chao(g, 1320); titulo(g, 'QUE LINDO!', 'SEU NOME', t, 0.9); fim(g); });
  C('saia', (g, t) => { todo(g, RED); const s = Math.sin(t * 55) * 14 * (1 - clamp(t / 0.8)); g.save(); g.translate(s, -s); janela(g, 190, 660, 700, 540, () => { glow(g, 540, 900, 500, LUZ, 0.7); gente(g, 540, 1300, 1.2); }); g.restore(); chao(g); texto(g, 'SAIA DA', 540, 270, 220, LUZ); texto(g, 'JANELA!', 540, 490, 230, LUZ, clamp((t - 0.25) * 6)); fim(g); });
  C('naosaiu', (g, t) => { sala(g); janela(g, 190, 660, 700, 540, () => { rua(g, t, () => 1, 1195, 0.62); gente(g, 540, 1310, 1.2); }); chao(g); titulo(g, 'ELE NÃO', 'SAIU', t, 0.4, 290, RED); fim(g); });
  C('olhos', (g, t) => { escuro(g); const c = passo(t, 0.75) % 2 ? RED : MENTA; zoom(g, lerp(1, 1.15, out(clamp(t / 1.2))), 540, 950, () => irmao(g, { y: 1750, s: 2.4, olhos: [c, c] })); chao(g, 1320); titulo(g, 'OS OLHOS', 'DELE', t, 0.4); });
  C('cores', (g, t) => { escuro(g); const i = passo(t, 0.75) % 3, c = COR3[i]; irmao(g, { y: 1920, s: 2.9, olhos: [c, c] }); chao(g, 1320); texto(g, i === 1 ? 'VERMELHO' : 'VERDE', 540, 380, 230, c); });
  C('disjuntor', (g, t) => { sala(g); rect(g, 250, 600, 580, 640, BREU); rect(g, 290, 640, 500, 560, LAV); const d = out(clamp((t - 0.7) / 0.18)); for (let i = 0; i < 3; i++) { const x = 380 + i * 160; rect(g, x - 45, 770, 90, 280, NOITE); rect(g, x - 38, 780 + (i === 1 ? d * 160 : 0), 76, 100, i === 1 ? RED : LUZ); } const my = lerp(810, 970, d); curva(g, VULTO, 96, q => { q.moveTo(1180, 1260); q.quadraticCurveTo(820, my + 220, 600, my + 40); }); circ(g, 570, my + 30, 66, VULTO); chao(g); titulo(g, 'ARRANQUEI O', 'DISJUNTOR', t, 0.5, 270, RED); fim(g); });
  C('apagou', (g, t) => { ceu(g); todo(g, BREU, 0.65 * clamp((t - 0.3) / 1.4)); rua(g, t, i => t < 0.4 + i * 0.55 ? 1 : 0, 1215); chao(g, 1205); titulo(g, 'A RUA', 'APAGOU', t, 0.8, 380); fim(g); });
  C('calmo', (g, t) => { escuro(g); irmao(g, { y: 1500, s: 1.7, cor: BREU }); chao(g, 1320); titulo(g, 'NO ESCURO', 'CALMO', t, 1, 290, LAV); });
  C('tomada', (g, t) => { escuro(g); const o = [t > 0.5 ? MENTA : null, t > 1.2 ? RED : null]; zoom(g, lerp(1, 1.1, clamp(t / 2.5)), 540, 950, () => irmao(g, { y: 1500, s: 1.7, cor: BREU, olhos: o, boca: 'fala', t })); chao(g, 1320); titulo(g, 'SEM', 'TOMADA', t, 1.1, 290, RED); });
  C('acendendo', (g, t) => { escuro(g); const k = passo(t, 0.75) % 2; irmao(g, { y: 1800, s: 2.5, olhos: k ? [RED, MENTA] : [MENTA, RED], boca: 'sorri' }); chao(g, 1320); titulo(g, 'CONTINUARAM', 'ACENDENDO', t, 0.7); });
  C('letra', (g, t) => { escuro(g); const i = Math.min(2, passo(t, 0.6)), l = 'BIA'[i], c = COR3[i]; irmao(g, { y: 2100, s: 3.4, olhos: [c, c], letras: [l, l], boca: 'sorri' }); chao(g, 1320); texto(g, ['B', 'B  I', 'B  I  A'][i], 540, 380, 250, LUZ); });
  // arte da capa (sem texto): o irmão de olhos acesos diante das casas; céu contínuo até o topo
  C('capaarte', g => { todo(g, AZUL); vgrad(g, 0, 1920, AZUL, AZUL2, -300, W + 600); glow(g, 540, 1200, 720, LAV, 0.6); cordao(g, -40, 750, 1120, 750, 12, 0, { cai: 25, r: 18, a: 1 }); rua(g, 0, () => 1, 1150, 0.98); chao(g, 1145); gente(g, 540, 1940, 1.85, { cor: VULTO, olhos: [MENTA, RED], boca: 'sorri' }); });

  // ───── som: estalo de lâmpada, apito do grupo, cortina e disjuntor, sintetizados aqui
  const ant = window.SfxExtra;
  window.SfxExtra = function (defs, h) {
    ant && ant(defs, h); const { G, F, O, N, C: L, dec, bus } = h, vol = p => p.vol == null ? 1 : p.vol;
    defs.estaloLuz = function (t, p) { const n = p.n || 3, per = p.passo || 0.65, out = G(0.4 * vol(p)); for (let i = 0; i < n; i++) { const s = t + i * per, nz = N(s, s + 0.08), hp = F('highpass', 2500), q = G(0), o = O('sine', [988, 784, 880][i % 3], s, s + 0.6), go = G(0); dec(q.gain, s, 0.001, 0.8, 0.02); dec(go.gain, s, 0.004, 0.45, 0.28); L(nz, hp, q, out); L(o, go, out); } bus(out, true); return { t, fim: t + n * per + 0.5 }; };
    defs.apitoGrupo = function (t, p) { const out = G(0.35 * vol(p)); [[1175, 0], [1568, 0.13]].forEach(([f, d]) => { const s = t + d, o = O('sine', f, s, s + 0.4), q = G(0); dec(q.gain, s, 0.004, 0.8, 0.16); L(o, q, out); }); bus(out, false); return { t, fim: t + 0.6 }; };
    defs.cortinaCorre = function (t, p) { const out = G(0.5 * vol(p)), nz = N(t, t + 0.7, true), bp = F('bandpass', 1600, 0.8), q = G(0); q.gain.setValueAtTime(0, t); q.gain.linearRampToValueAtTime(0.9, t + 0.12); q.gain.linearRampToValueAtTime(0, t + 0.6); bp.frequency.setValueAtTime(2400, t); bp.frequency.exponentialRampToValueAtTime(700, t + 0.6); L(nz, bp, q, out); bus(out, false); return { t, fim: t + 0.8 }; };
    defs.disjuntor = function (t, p) { const out = G(0.55 * vol(p)), nz = N(t, t + 0.12), q = G(0), o = O('sine', 130, t, t + 0.5), go = G(0), z = O('sawtooth', 120, t, t + 1.4), lp = F('lowpass', 900), gz = G(0); dec(q.gain, t, 0.001, 1, 0.03); o.frequency.setValueAtTime(130, t); o.frequency.exponentialRampToValueAtTime(40, t + 0.3); dec(go.gain, t, 0.004, 1, 0.22); z.frequency.setValueAtTime(120, t); z.frequency.exponentialRampToValueAtTime(30, t + 1.2); gz.gain.setValueAtTime(0.35, t); gz.gain.linearRampToValueAtTime(0, t + 1.3); L(nz, q, out); L(o, go, out); L(z, lp, gz, out); bus(out, false); return { t, fim: t + 1.5 }; };
  };
})();
