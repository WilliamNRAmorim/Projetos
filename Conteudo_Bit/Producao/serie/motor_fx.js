// Camada visual opcional do motor (11/2026): atmosfera, personagens em vetor v2, composição e movimento.
// Só entra em cena quando o JSON traz a chave "visual" (no episódio ou na cena). Sem a chave, o motor.js não chama nada daqui
// e nenhum pixel muda (provado por linha_base.js). Como pedir cada efeito: MOTOR_GUIA.md.
// Tudo é função do tempo e de sementes fixas (sem Math.random): o mesmo JSON dá sempre o mesmo vídeo.
(() => {
  const M = window.Motor, { W, H, GY } = M, { rect, circ, line, rrect, poly, rgba, rnd, lerp, clamp, P } = M.H_;
  const TAU = Math.PI * 2, LUZ = '#E8DFC8', suave = x => x * x * (3 - 2 * x);
  const ruido = (t, s = 0) => Math.sin(t * 1.3 + s) * 0.5 + Math.sin(t * 2.9 + s * 1.7) * 0.3 + Math.sin(t * 5.3 + s * 0.3) * 0.2; // -1..1, suave
  const hex = c => [parseInt(c.slice(1, 3), 16), parseInt(c.slice(3, 5), 16), parseInt(c.slice(5, 7), 16)];
  const mix = (a, b, k) => { const x = hex(a), y = hex(b); return '#' + x.map((v, i) => Math.round(lerp(v, y[i], k)).toString(16).padStart(2, '0')).join(''); };
  const tela = (w, h) => { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; };
  const px = (v, tam) => v == null ? null : (Math.abs(v) <= 2 ? v * tam : v); // até 2 = fração da tela; acima = pixels
  const lista = x => x == null || x === false ? [] : Array.isArray(x) ? x : [x];
  const elipse = (g, x, y, rx, ry, c, a = 1, rot = 0) => { g.globalAlpha = a; g.fillStyle = c; g.beginPath(); g.ellipse(x, y, Math.max(0.01, rx), Math.max(0.01, ry), rot, 0, TAU); g.fill(); g.globalAlpha = 1; };

  // ───────────── configuração: episódio (padrão) + cena (sobrescreve campo a campo; false desliga) ─────────────
  const PRESETS = { // atalhos: "visual": "terror" no episódio ou na cena
    terror: { vinheta: 0.55, grao: 0.4, poeira: 0.35, neblina: 0.3, brilho: 0.35, personagens: true, movimento: true, sombra: true, legenda: 'auto' },
    noite: { vinheta: 0.6, grao: 0.45, neblina: 0.45, cor: 'luar', brilho: 0.3, personagens: true, movimento: true, sombra: true, legenda: 'auto' },
    vela: { vinheta: 0.6, grao: 0.4, poeira: 0.5, cor: 'quente', brilho: 0.45, escuro: 0.5, luz: { tipo: 'vela', x: 0.5, y: 0.55 }, personagens: true, movimento: true, sombra: true, legenda: 'auto' },
    limpo: { vinheta: 0.3, grao: 0.25, personagens: true, movimento: true, sombra: true, legenda: 'auto' },
  };
  const FASE = +new URLSearchParams(location.search).get('fase') || 0, FASES = { personagens: 2, sombra: 2, camera: 3, chao: 3, primeiroPlano: 3, legenda: 3, legendaFundo: 3, movimento: 4 };
  const abre = v => typeof v === 'string' ? (PRESETS[v] || {}) : v === true ? PRESETS.limpo : v;
  function cfg(ep, c) {
    if (c._vis !== undefined) return c._vis;
    const a = ep.visual, b = c.visual; let v = null;
    if (b === false) v = null; else if (a || b) { v = Object.assign({}, abre(a) || {}, abre(b) || {}); if (v.preset) v = Object.assign({}, PRESETS[v.preset] || {}, v); }
    if (v && FASE) for (const k of Object.keys(v)) if ((FASES[k] || 1) > FASE) delete v[k]; // &fase=N na URL: mostra só até a fase N (conferência)
    return (c._vis = v && Object.keys(v).length ? v : null);
  }

  // ───────────── FASE 1 · ATMOSFERA (pós-render, abaixo do texto e da legenda) ─────────────
  const CORES = { frio: '#3A5A8C', quente: '#C9772E', sepia: '#8A6A3A', verde: '#3F6B4F', sangue: '#8C1F1F', luar: '#4A5FA0', roxo: '#5A3F8C' };
  let tGrao, tNevoa, tEscuro, tBrilho;
  function grao(g, a, fr) {
    if (!tGrao) { tGrao = tela(256, 256); const x = tGrao.getContext('2d'), d = x.createImageData(256, 256); for (let i = 0; i < d.data.length; i += 4) { const v = 128 + (rnd(i * 0.37 + 11) - 0.5) * 230; d.data[i] = d.data[i + 1] = d.data[i + 2] = v; d.data[i + 3] = 255; } x.putImageData(d, 0, 0); }
    const k = Math.floor(fr / 2), ox = Math.floor(rnd(k + 3) * 256), oy = Math.floor(rnd(k + 71) * 256); // troca a cada 2 quadros
    g.save(); g.globalAlpha = a * 0.2; g.globalCompositeOperation = 'overlay'; g.translate(-ox, -oy); g.fillStyle = g.createPattern(tGrao, 'repeat'); g.fillRect(0, 0, W + 256, H + 256); g.restore();
  }
  function nevoa(g, a, t, cor) {
    if (!tNevoa) { tNevoa = tela(1024, 256); const x = tNevoa.getContext('2d'); // manchas macias que emendam na horizontal
      for (let i = 0; i < 30; i++) { const cx = rnd(i + 1) * 1024, cy = 40 + rnd(i + 50) * 176, r = 60 + rnd(i + 90) * 120;
        for (const dx of [-1024, 0, 1024]) { const gr = x.createRadialGradient(cx + dx, cy, 0, cx + dx, cy, r); gr.addColorStop(0, 'rgba(255,255,255,0.11)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); x.fillStyle = gr; x.fillRect(cx + dx - r, cy - r, 2 * r, 2 * r); } } }
    if (!nevoa.tinta || nevoa.cor !== cor) { nevoa.cor = cor; nevoa.tinta = tela(1024, 256); const x = nevoa.tinta.getContext('2d'); x.drawImage(tNevoa, 0, 0); x.globalCompositeOperation = 'source-in'; x.fillStyle = cor; x.fillRect(0, 0, 1024, 256); }
    g.save();
    [[1050, 620, 16, 0.55], [1240, 560, -26, 0.8], [1420, 620, 40, 1], [820, 520, -11, 0.3], [1600, 520, 60, 0.9]].forEach(([y, h, vel, f], i) => { // 5 faixas lentas, mais densas embaixo
      const larg = 2600, off = (((t * vel + i * 370) % larg) + larg) % larg; g.globalAlpha = clamp(a * f * 0.7);
      g.drawImage(nevoa.tinta, -off, y, larg, h); g.drawImage(nevoa.tinta, -off + larg, y, larg, h); });
    g.restore();
  }
  function poeira(g, a, t, luzes) {
    g.save(); g.fillStyle = LUZ;
    for (let i = 0; i < 70; i++) { const v = 8 + rnd(i + 5) * 22, x = rnd(i + 1) * W + Math.sin(t * 0.35 + i) * 46, y = (((rnd(i + 9) * H - t * v) % H) + H) % H, r = 1.4 + rnd(i + 13) * 3.2;
      let perto = 0.45; for (const L of luzes) perto = Math.max(perto, 1 - Math.hypot(x - L.x, y - L.y) / (L.r * 1.1)); // brilha mais perto da luz
      g.globalAlpha = clamp(a * perto * (0.35 + 0.65 * (0.5 + 0.5 * Math.sin(t * 1.7 + i * 2.3)))); g.beginPath(); g.arc(x, y, r, 0, TAU); g.fill(); }
    g.restore();
  }
  function pisca(tipo, t, i) { // intensidade 0..1 da luz no tempo
    if (tipo === 'vela') return 0.84 + 0.16 * ruido(t * 6.5, i * 9);
    if (tipo === 'lanterna') { const k = (t + i * 1.3) % 3.7; return k > 3.52 ? 0.35 : 1; } // firme, cai de vez em quando
    if (tipo === 'lampada') { const q = Math.floor(t * 14) + i * 31; return (rnd(Math.floor(t * 0.9) + i * 7) > 0.45 && rnd(q) > 0.55 ? 0.3 : 1) * (0.96 + 0.04 * Math.sin(t * 60)); } // pisca em rajadas
    if (tipo === 'tv') return 0.7 + 0.3 * rnd(Math.floor(t * 9) + i);
    if (tipo === 'raio') { const k = (t + i * 2.1) % 5.3; return k < 0.08 || (k > 0.16 && k < 0.3) ? 1 : 0; } // relâmpago: dois clarões e some
    return 1; // "fixa"
  }
  function luzes(v, t) {
    return lista(v.luz).map((L, i) => { const f = pisca(L.tipo || 'vela', t, i), tr = (L.tipo || 'vela') === 'vela' ? 7 : 0;
      return { x: px(L.x ?? 0.5, W) + ruido(t * 5, i) * tr, y: px(L.y ?? 0.5, H) + ruido(t * 4.1, i + 5) * tr, r: (L.raio || 500) * (0.94 + 0.06 * f), f: f * (L.intensidade ?? 0.7), cor: L.cor || (L.tipo === 'tv' || L.tipo === 'raio' ? '#BFD4FF' : L.tipo === 'lanterna' ? '#EAF0FF' : '#FFC98A') }; });
  }
  function atmos(g, v, c, t, fr, cv) {
    const Ls = luzes(v, t), esc = v.escuro ?? (Ls.length ? 0.45 : 0);
    if (esc > 0) { // escuridão com buracos de luz, em 1/4 da resolução (barato e macio)
      if (!tEscuro) tEscuro = tela(W / 4, H / 4); const x = tEscuro.getContext('2d'); x.globalCompositeOperation = 'source-over'; x.clearRect(0, 0, W / 4, H / 4); x.fillStyle = rgba(v.escuroCor || '#06060C', clamp(esc)); x.fillRect(0, 0, W / 4, H / 4);
      x.globalCompositeOperation = 'destination-out';
      for (const L of Ls) { const gr = x.createRadialGradient(L.x / 4, L.y / 4, 0, L.x / 4, L.y / 4, L.r / 4); gr.addColorStop(0, `rgba(0,0,0,${clamp(L.f * 1.25)})`); gr.addColorStop(0.55, `rgba(0,0,0,${clamp(L.f * 0.55)})`); gr.addColorStop(1, 'rgba(0,0,0,0)'); x.fillStyle = gr; x.fillRect(0, 0, W / 4, H / 4); }
      g.save(); g.imageSmoothingEnabled = true; g.imageSmoothingQuality = 'high'; g.drawImage(tEscuro, 0, 0, W, H); g.restore(); }
    for (const L of Ls) { g.save(); g.globalCompositeOperation = 'screen'; const gr = g.createRadialGradient(L.x, L.y, 0, L.x, L.y, L.r); gr.addColorStop(0, rgba(L.cor, 0.3 * L.f)); gr.addColorStop(0.4, rgba(L.cor, 0.12 * L.f)); gr.addColorStop(1, rgba(L.cor, 0)); g.fillStyle = gr; g.fillRect(L.x - L.r, L.y - L.r, 2 * L.r, 2 * L.r); g.restore(); }
    if (v.neblina > 0) nevoa(g, v.neblina, t, /^#[0-9a-f]{6}$/i.test(v.neblinaCor || '') ? v.neblinaCor : '#B9B4C0');
    if (v.poeira > 0) poeira(g, v.poeira, t, Ls);
    if (v.brilho > 0 && cv) { // brilho (bloom): cópia pequena e contrastada, somada por cima
      if (!tBrilho) tBrilho = tela(W / 8, H / 8); const x = tBrilho.getContext('2d'); x.globalCompositeOperation = 'source-over'; x.drawImage(cv, 0, 0, W / 8, H / 8); x.globalCompositeOperation = 'multiply'; x.drawImage(tBrilho, 0, 0); x.drawImage(tBrilho, 0, 0);
      g.save(); g.globalCompositeOperation = 'screen'; g.globalAlpha = clamp(v.brilho * 0.75); g.imageSmoothingEnabled = true; g.imageSmoothingQuality = 'high'; g.drawImage(tBrilho, -8, -8, W + 16, H + 16); g.restore(); }
    if (v.cor) { const o = typeof v.cor === 'string' ? { cor: v.cor } : v.cor, cc = CORES[o.cor] || o.cor; if (/^#[0-9a-f]{6}$/i.test(cc)) { g.save(); g.globalCompositeOperation = 'soft-light'; g.globalAlpha = clamp(o.forca ?? 0.45); g.fillStyle = cc; g.fillRect(0, 0, W, H); g.restore(); } }
    if (v.vinheta > 0) { g.save(); g.translate(W / 2, H * 0.47); g.scale(1, 1.5); const gr = g.createRadialGradient(0, 0, 330, 0, 0, 800); gr.addColorStop(0, 'rgba(4,4,8,0)'); gr.addColorStop(0.6, `rgba(4,4,8,${0.35 * v.vinheta})`); gr.addColorStop(1, `rgba(4,4,8,${clamp(0.95 * v.vinheta)})`); g.fillStyle = gr; g.fillRect(-W, -H, 2 * W, 2 * H); g.restore(); }
    if (v.grao > 0) grao(g, v.grao, fr);
  }

  // ───────────── FASE 3 · COMPOSIÇÃO: câmera (close, plongée, contraplongée, câmera na mão), chão, primeiro plano, legenda ─────────────
  const PLANOS = { aberto: [1, 0], medio: [1.6, -330], close: [2.7, -405], detalhe: [3.6, -468] }; // [zoom, altura do foco acima dos pés]
  function alvo(o, c, k) { // ponto de foco em coordenadas da cena
    if (o.foco && typeof o.foco === 'string') { const p = (c.personagens || []).find(x => x.id === o.foco); if (p) return [p.x * W, GY + (p.y || 0) + (PLANOS[o.plano] || PLANOS.medio)[1] * (p.escala || 1)]; }
    if (Array.isArray(o.foco)) return [px(o.foco[0], W), px(o.foco[1], H)];
    return [px(o.x ?? 0.5, W), px(o.y ?? 0.5, H)];
  }
  function camera(v, c, u, kk, z) { // devolve o enquadramento extra desta cena, ou null
    const o = v.camera; if (!o) return null; const a = typeof o === 'string' ? { plano: o } : o, b = a.ate ? Object.assign({}, a, typeof a.ate === 'string' ? { plano: a.ate } : a.ate) : a;
    const e = suave(clamp(a.ate ? (u - (a.espera || 0)) / Math.max(0.3, (a.dura || c.dur * 0.7)) : 0)), ka = a.zoom || (PLANOS[a.plano] || PLANOS.aberto)[0], kb = b.zoom || (PLANOS[b.plano] || PLANOS.aberto)[0];
    const fa = alvo(a, c), fb = alvo(b, c), mao = a.mao || 0, rot = (a.inclina || 0) + ruido(u * 0.9, 3) * 0.006 * mao;
    let k = lerp(ka, kb, e) * (1 + Math.abs(rot) * 1.4 + mao * 0.02); const hw = W / (2 * z * k) * 1.05 + mao * 6, hh = H / (2 * z * k) * 1.05 + mao * 6 + 2 * Math.abs((c.pan || [0, 0])[0]) / k;
    const fx = clamp(lerp(fa[0], fb[0], e) + ruido(u * 0.8, 1) * 9 * mao, Math.min(hw, W / 2), Math.max(W - hw, W / 2)), fy = clamp(lerp(fa[1], fb[1], e) + ruido(u * 0.7, 2) * 9 * mao, Math.min(hh, H / 2), Math.max(H - hh, H / 2));
    const ang = a.angulo === 'plongee' ? 1 : a.angulo === 'contra' || a.angulo === 'contraplongee' ? -1 : 0;
    return { k, fx: k <= 1.001 ? W / 2 : fx, fy: k <= 1.001 ? H / 2 : fy, rot, key: ang * (a.forca ?? 0.26) };
  }
  const olhar = (g, cam) => { g.translate(W / 2, H / 2); g.rotate(cam.rot); g.scale(cam.k, cam.k); g.translate(-cam.fx, -cam.fy); };
  let tMundo;
  function keystone(g, mundo, cam) { // plongée (visto de cima: topo largo) / contraplongée (visto de baixo: base larga), em tiras
    if (!tMundo) tMundo = tela(W, H); const x = tMundo.getContext('2d'); x.setTransform(1, 0, 0, 1, 0, 0); x.clearRect(0, 0, W, H); mundo(x);
    const a = Math.abs(cam.key), N = 6; g.save(); g.imageSmoothingEnabled = true;
    for (let y = 0; y < H; y += N) { const f = cam.key > 0 ? 1 - y / H : y / H, s = 1 + a * f, yy = cam.key > 0 ? y : y; g.drawImage(tMundo, 0, y, W, N, W / 2 - W * s / 2, yy, W * s, N + 0.6); }
    g.restore();
  }
  function chao(g, v, c, u) { // ocupa a metade de baixo: piso em perspectiva + poça de luz + escurecer para a borda
    const o = v.chao; if (!o) return; const a = typeof o === 'string' ? { tipo: o } : o, y0 = a.y ?? GY + 6, cor = a.cor || '#1B1719', lin = a.linha || mix(cor, '#000000', 0.45), vx = px(a.fuga ?? 0.5, W), hh = H - y0 + 420;
    const gr = g.createLinearGradient(0, y0, 0, H); gr.addColorStop(0, mix(cor, '#000000', 0.28)); gr.addColorStop(0.25, cor); gr.addColorStop(1, mix(cor, '#000000', 0.5)); g.fillStyle = gr; g.fillRect(-400, y0, W + 800, hh);
    g.save(); g.beginPath(); g.rect(-400, y0, W + 800, hh); g.clip(); g.strokeStyle = lin; g.lineCap = 'butt';
    const tipo = a.tipo || 'tabua', fy = y0 - 260; // ponto de fuga acima da linha do chão
    if (tipo === 'tabua' || tipo === 'ladrilho') { g.lineWidth = 3; g.globalAlpha = 0.55; for (let i = -14; i <= 14; i++) { const xb = vx + i * 190; g.beginPath(); g.moveTo(lerp(vx, xb, (y0 - fy) / (H + 420 - fy)), y0); g.lineTo(xb, H + 420); g.stroke(); } }
    if (tipo === 'ladrilho' || tipo === 'tabua') { g.globalAlpha = tipo === 'ladrilho' ? 0.5 : 0.22; for (let i = 0; i < 9; i++) { const yy = y0 + 14 + Math.pow(i / 8, 1.9) * (H + 380 - y0); g.lineWidth = 2 + i * 0.5; g.beginPath(); g.moveTo(-400, yy); g.lineTo(W + 400, yy); g.stroke(); } }
    if (tipo === 'terra' || tipo === 'asfalto') { for (let i = 0; i < 90; i++) { const d = rnd(i + 3), yy = y0 + 10 + d * d * (H + 300 - y0), xx = rnd(i + 40) * (W + 600) - 300, w = 10 + d * 46; g.globalAlpha = 0.25 + 0.3 * rnd(i + 80); g.fillStyle = rnd(i) > 0.5 ? lin : mix(cor, '#FFFFFF', 0.08); g.fillRect(xx, yy, w, 2 + d * 5); } }
    if (a.tapete) { const t = typeof a.tapete === 'string' ? a.tapete : '#5A1F1A', cx = px(a.tapeteX ?? 0.5, W), w1 = 300, w2 = 520, ya = y0 + 70, yb = y0 + 420; g.globalAlpha = 1; poly(g, [[cx - w1, ya], [cx + w1, ya], [cx + w2, yb], [cx - w2, yb]], t); poly(g, [[cx - w1 + 26, ya + 16], [cx + w1 - 26, ya + 16], [cx + w2 - 44, yb - 26], [cx - w2 + 44, yb - 26]], mix(t, '#000000', 0.28)); }
    g.globalAlpha = 1; g.restore();
    const Ls = luzes(v, u); for (const L of Ls) { g.save(); g.translate(L.x, Math.max(y0 + 120, Math.min(L.y + 300, H))); g.scale(1, 0.32); const r = L.r * 1.1, p = g.createRadialGradient(0, 0, 0, 0, 0, r); p.addColorStop(0, rgba(L.cor, 0.16 * L.f)); p.addColorStop(1, rgba(L.cor, 0)); g.fillStyle = p; g.fillRect(-r, -r, 2 * r, 2 * r); g.restore(); }
    g.fillStyle = 'rgba(0,0,0,0.22)'; g.fillRect(-400, y0, W + 800, 10); // encontro da parede com o chão
  }
  const PP = { // primeiro plano: silhuetas escuras na frente da cena (desenhadas uma vez, desfocadas, com paralaxe)
    batente: (g, o) => { const e = o.lado === 'dir' ? 1 : -1, x = e > 0 ? W - 150 : 150; poly(g, e > 0 ? [[x, -200], [W + 300, -200], [W + 300, H + 300], [x + 40, H + 300]] : [[x, -200], [-300, -200], [-300, H + 300], [x - 40, H + 300]], o.cor); line(g, x - e * 10, -200, x + e * 28, H + 300, mix(o.cor, '#FFFFFF', 0.07), 10); },
    moldura: (g, o) => { PP.batente(g, Object.assign({}, o, { lado: 'esq' })); PP.batente(g, Object.assign({}, o, { lado: 'dir' })); g.fillStyle = o.cor; g.fillRect(-300, -300, W + 600, 430); },
    cortina: (g, o) => { const e = o.lado === 'dir' ? 1 : -1; g.fillStyle = o.cor; for (let i = 0; i < 5; i++) { const x0 = e > 0 ? W + 60 - i * 62 : -60 + i * 62, w = 96; g.beginPath(); g.moveTo(x0 - w / 2, -200); g.quadraticCurveTo(x0 - w / 2 - e * 24, H * 0.5, x0 - w / 2 + e * 10, H + 300); g.lineTo(x0 + w / 2 + e * 10, H + 300); g.quadraticCurveTo(x0 + w / 2 - e * 24, H * 0.5, x0 + w / 2, -200); g.fill(); line(g, x0 - e * w / 2, -200, x0 - e * w / 2 - e * 14, H + 300, mix(o.cor, '#FFFFFF', 0.06), 6); } },
    planta: (g, o) => { const e = o.lado === 'dir' ? 1 : -1, bx = e > 0 ? W - 40 : 40; g.fillStyle = o.cor; for (let i = 0; i < 9; i++) { const a = -Math.PI / 2 - e * (0.9 - i * 0.24), L = 520 + rnd(i + 2) * 320, tx = bx + Math.cos(a) * L, ty = H + 60 + Math.sin(a) * L, nx = Math.cos(a + Math.PI / 2) * (46 + rnd(i) * 30), ny = Math.sin(a + Math.PI / 2) * (46 + rnd(i) * 30);
      g.beginPath(); g.moveTo(bx, H + 80); g.quadraticCurveTo((bx + tx) / 2 + nx, (H + 60 + ty) / 2 + ny, tx, ty); g.quadraticCurveTo((bx + tx) / 2 - nx, (H + 60 + ty) / 2 - ny, bx, H + 80); g.fill(); } },
    galhos: (g, o) => { const e = o.lado === 'dir' ? 1 : -1; const ramo = (x, y, a, L, w, n) => { const x2 = x + Math.cos(a) * L, y2 = y + Math.sin(a) * L; line(g, x, y, x2, y2, o.cor, w); if (n > 0) { ramo(x2, y2, a + 0.5 + rnd(n + L) * 0.3, L * 0.68, w * 0.62, n - 1); ramo(x2, y2, a - 0.42 - rnd(n * 3 + L) * 0.3, L * 0.6, w * 0.6, n - 1); } };
      ramo(e > 0 ? W + 80 : -80, -60, e > 0 ? Math.PI * 0.82 : Math.PI * 0.18, 330, 46, 4); ramo(e > 0 ? W + 60 : -60, 380, e > 0 ? Math.PI * 0.95 : Math.PI * 0.05, 230, 30, 3); },
    grade: (g, o) => { g.fillStyle = o.cor; for (let x = -60; x < W + 120; x += 190) g.fillRect(x, -300, 44, H + 600); g.fillRect(-300, 250, W + 600, 40); g.fillRect(-300, H - 330, W + 600, 46); },
    mesa: (g, o) => { g.fillStyle = o.cor; g.beginPath(); g.moveTo(-300, H - 250); g.quadraticCurveTo(W / 2, H - 330, W + 300, H - 250); g.lineTo(W + 300, H + 300); g.lineTo(-300, H + 300); g.fill(); line(g, -300, H - 246, W + 300, H - 246, mix(o.cor, '#FFFFFF', 0.08), 8); },
    ombro: (g, o) => { const e = o.lado === 'dir' ? 1 : -1, cx = e > 0 ? W - 170 : 170; g.fillStyle = o.cor; g.beginPath(); g.ellipse(cx, H - 470, 210, 250, 0, 0, TAU); g.fill(); g.beginPath(); g.ellipse(cx - e * 20, H + 40, 520, 330, 0, 0, TAU); g.fill(); }, // alguém de costas, bem perto da câmera
    degraus: (g, o) => { g.fillStyle = o.cor; for (let i = 0; i < 4; i++) g.fillRect(-300, H - 90 - i * 84, W + 600 - i * 0, 300); for (let i = 0; i < 4; i++) line(g, -300, H - 88 - i * 84, W + 300, H - 88 - i * 84, mix(o.cor, '#FFFFFF', 0.07), 6); },
  };
  const cachePP = {};
  function frente(g, v, c, u, kk) {
    lista(v.primeiroPlano).forEach((it, i) => { const o = Object.assign({ cor: '#08070A', desfoque: 7, alfa: 0.96, lado: i % 2 ? 'dir' : 'esq' }, typeof it === 'string' ? { tipo: it } : it), f = PP[o.tipo]; if (!f) return;
      const ch = [o.tipo, o.lado, o.cor, o.desfoque].join('|'); let t = cachePP[ch];
      if (!t) { t = cachePP[ch] = tela(W / 2, H / 2); const x = t.getContext('2d'); x.filter = `blur(${o.desfoque / 2}px)`; x.scale(0.5, 0.5); f(x, o); }
      const e = o.lado === 'dir' ? 1 : -1, s = (o.escala || 1) * (1.06 + 0.07 * kk), dx = e * (36 - 70 * kk) + (o.x || 0), dy = (o.y || 0) + 16 * kk; // paralaxe: anda mais que o fundo
      g.save(); g.globalAlpha = o.alfa; g.translate(W / 2 + dx, H / 2 + dy); g.scale(s, s); g.imageSmoothingEnabled = true; g.drawImage(t, -W / 2, -H / 2, W, H); g.restore(); });
  }
  function legendaY(ep, c, v) { // legenda que se adapta: escolhe a altura que não cobre nenhum rosto (uma vez por cena, com o zoom de 60% da cena: não depende do quadro pedido)
    if (c._legY !== undefined) return c._legY; const zz = c.zoom || [1, 1.07], z = lerp(zz[0], zz[1], 0.6);
    const tam = c.legendaTam ?? ep.legendaTam ?? 110, base = ep.legendaY ?? 1030, cam = v.camera ? camera(v, c, c.dur * 0.6, 0.6, z) : null;
    const caras = (c.personagens || []).filter(p => !p.costas).map(p => { let x = p.x * W, y = GY + (p.y || 0) - 468 * (p.escala || 1), r = 100 * (p.escala || 1);
      if (cam) { x = W / 2 + (x - cam.fx) * cam.k; y = H / 2 + (y - cam.fy) * cam.k; r *= cam.k; } x = W / 2 + (x - W / 2) * z; y = H / 2 + (y - H / 2) * z; return [x, y, r * z]; });
    const cobre = Y => caras.reduce((a, [x, y, r]) => a + Math.max(0, Math.min(Y + tam * 0.45, y + r) - Math.max(Y - tam * 1.05, y - r)) * (x + r > 120 && x - r < W - 120 ? 1 : 0), 0);
    let melhor = base, m = cobre(base); for (const Y of [base, 1380, 1440, 1240, 1100, 960, 780, 620]) { if (Y - tam < 300 || Y > 1460) continue; const k = cobre(Y) + Math.abs(Y - base) * 0.02; if (k < m - 0.5) { m = k; melhor = Y; } }
    return (c._legY = melhor);
  }
  function fundoLegenda(g, v, Y, tam) { const a = v.legendaFundo; if (!(a > 0)) return; const gr = g.createLinearGradient(0, Y - tam * 1.7, 0, Y + tam * 1.1); gr.addColorStop(0, 'rgba(6,6,8,0)'); gr.addColorStop(0.35, `rgba(6,6,8,${clamp(a)})`); gr.addColorStop(0.7, `rgba(6,6,8,${clamp(a)})`); gr.addColorStop(1, 'rgba(6,6,8,0)'); g.fillStyle = gr; g.fillRect(0, Y - tam * 1.7, W, tam * 2.8); }

  // ───────────── FASES 2 e 4 · PERSONAGENS EM VETOR v2 E MOVIMENTO ─────────────
  // prepara o personagem da cena: lado da luz, para onde olha, se está falando agora
  function pers(p, c, v, u) {
    const Ls = lista(v.luz), L = Ls[0], ld = L ? (px(L.x ?? 0.5, W) >= p.x * W ? 1 : -1) * (p.flip ? -1 : 1) : 1;
    let alvoX = null; if (p.olha != null) { const q = typeof p.olha === 'string' ? (c.personagens || []).find(x => x.id === p.olha) : null; alvoX = q ? q.x : typeof p.olha === 'number' ? p.olha : null; }
    let fala = 0; for (const s of c._segs || []) if (u >= s.ini && u <= s.ini + s.dur && (s.quem === p.id || s.quem === p.voz)) fala = Math.min(1, (u - s.ini) / 0.08, (s.ini + s.dur - u) / 0.12);
    return Object.assign({}, p, { _fx: v, _ld: ld, _alvo: alvoX, _fala: fala, _u: u });
  }
  const SEM_PISCAR = { fixo: 1, cego: 1 };
  function vida(s, o, t, sd) { // Fase 4: piscar, respirar, virar a cabeça, olhar que muda (só com "movimento")
    const v = o._fx, r = Object.assign({}, s); r._ld = o._ld; r._fala = o._fala || 0;
    if (o._alvo != null) { const d = (o._alvo - o.x) * (o.flip ? -1 : 1); r.olhar = clamp(d * 34, -10, 10); r.rosto = (r.rosto || 0) + clamp(d * 26, -9, 9); }
    if (!v.movimento) return r;
    const per = 3.1 + rnd(sd) * 2.6, k = (t + rnd(sd + 1) * per) % per, dupla = rnd(Math.floor((t + rnd(sd + 1) * per) / per) + sd) > 0.72; // pisca a cada 3-6 s, às vezes duas vezes
    const fecha = x => x < 0 || x > 0.17 ? 0 : x < 0.06 ? x / 0.06 : 1 - (x - 0.06) / 0.11; r.pisca = SEM_PISCAR[s.olho] ? 0 : Math.max(fecha(k), dupla ? fecha(k - 0.3) : 0);
    const per2 = 4.3 + rnd(sd + 2) * 3, k2 = (t + rnd(sd + 3) * per2) % per2, olhada = k2 < 1.1 ? suave(clamp(k2 / 0.22)) * suave(clamp((1.1 - k2) / 0.3)) : 0, lado = rnd(Math.floor((t + rnd(sd + 3) * per2) / per2) + sd + 9) > 0.5 ? 1 : -1; // olhada de lado de vez em quando
    if (o._alvo == null && !SEM_PISCAR[s.olho] && s.olhar == null) { r.olhar = lado * 7 * olhada; r.rosto = (r.rosto || 0) + lado * 4 * olhada; }
    r.rosto = (r.rosto || 0) + ruido(t * 0.45, sd) * 3.5; r.cabeca = (r.cabeca || 0) + ruido(t * 0.38, sd + 4) * 0.022; r.inclina = (r.inclina || 0) + Math.sin(t * 0.8 + sd) * 0.007; // cabeça e peso do corpo nunca param
    const solto = a => a && a[1] > 150 && Math.abs(a[0]) < 40; if (solto(s.al)) r.al = [s.al[0] + Math.sin(t * 1.25 + sd) * 4, s.al[1]]; if (solto(s.ar)) r.ar = [s.ar[0] + Math.sin(t * 1.25 + sd + 1.4) * 4, s.ar[1]]; // braços soltos balançam
    r._resp = 1.9; return r;
  }
  function sombra(g, o, s, esc) { // sombra de contato + sombra projetada para o lado oposto ao da luz; segue os pés e encolhe no pulo
    const ld = (o._ld || 1) * (o.flip ? -1 : 1), q = clamp(1 - (s.quica || 0) / 60, 0.45, 1), cx = s.fl && s.fr && !s.sentado ? (s.fl[0] + s.fr[0]) / 2 * esc * (o.flip ? -1 : 1) : 0;
    g.save(); g.translate(cx, 6); g.transform(1, 0, -ld * 1.5, 1, 0, 0); g.scale(1, 0.2); const R = 250 * esc * q, gr = g.createRadialGradient(-ld * 20 * esc, 0, 0, -ld * 20 * esc, 0, R); gr.addColorStop(0, 'rgba(0,0,0,0.42)'); gr.addColorStop(0.6, 'rgba(0,0,0,0.2)'); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr; g.fillRect(-R * 1.4, -R, R * 2.8, R * 2); g.restore();
    elipse(g, cx, 5, 104 * esc * q, 15 * esc * q, '#000', 0.4);
  }
  function roupa(g, v, s, sy, res, costas) { // tronco: lado na sombra, gola, dobra e fio de luz na borda
    const ld = s._ld || 1, h = 172 + res * 0.3;
    g.save(); g.beginPath(); g.roundRect(-72, sy - 14, 144, h, 28); g.clip();
    rect(g, ld > 0 ? -72 : 14, sy - 14, 58, h, '#000', 0.16); rect(g, -72, sy + 128, 144, 40, '#000', 0.1); // sombra lateral e dobra na barra
    if (!costas && !v.capuz) { if (v.blusa) rect(g, -24, sy - 14, 48, 26, '#000', 0.12); else poly(g, [[-26, sy - 14], [26, sy - 14], [0, sy + 20]], v.pele); poly(g, [[-30, sy - 14], [-22, sy - 14], [0, sy + 22], [22, sy - 14], [30, sy - 14], [0, sy + 34]], mix(v.camisa, '#000000', 0.3)); } // gola em V
    rect(g, ld > 0 ? 64 : -72, sy - 6, 8, h - 30, '#FFF', 0.09); g.restore();
    rect(g, -72, sy + 150, 144, 7, mix(v.calca, '#000000', 0.45)); if (!costas) rrect(g, -9, sy + 148, 18, 12, 3, mix(v.calca, '#FFFFFF', 0.3)); // cinto e fivela
  }
  function cabecaBase(g, v, s, cy, costas) { // orelha, sombra do lado oposto à luz e sombra do queixo no pescoço
    const ld = s._ld || 1, esc = mix(v.pele, '#3A1D14', 0.3);
    g.save(); g.beginPath(); g.arc(0, cy, 70, 0, TAU); g.clip(); g.fillStyle = esc; g.globalAlpha = 0.5; g.fillRect(-80, cy - 80, 160, 160); g.globalAlpha = 1; circ(g, ld * 15, cy - 9, 71, v.pele); g.restore();
    if (!costas) { circ(g, -66, cy + 8, 15, v.pele); circ(g, -66, cy + 8, 8, esc, 0.55); } // orelha (o rosto olha para a direita do desenho)
  }
  function cabelo(g, v, cy) { // silhueta de cabelo com franja, costeleta e mecha de brilho
    const c = v.cabelo, cl = mix(c, '#FFFFFF', 0.16); g.fillStyle = c;
    if (v.estilo === 'longo') { g.beginPath(); g.arc(0, cy, 76, Math.PI * 0.94, Math.PI * 2.06); g.quadraticCurveTo(74, cy + 30, 60, cy + 44); g.quadraticCurveTo(64, cy - 26, 30, cy - 38); g.quadraticCurveTo(-4, cy - 52, -30, cy - 30); g.quadraticCurveTo(-56, cy - 12, -62, cy + 40); g.quadraticCurveTo(-78, cy + 28, -76, cy + 6); g.fill(); }
    else if (v.estilo === 'coque') { g.beginPath(); g.arc(0, cy, 75, Math.PI * 0.99, Math.PI * 2.01); g.quadraticCurveTo(58, cy - 34, 22, cy - 46); g.quadraticCurveTo(-4, cy - 30, -34, cy - 40); g.quadraticCurveTo(-64, cy - 30, -75, cy + 2); g.fill(); g.strokeStyle = mix(c, '#000000', 0.35); g.lineWidth = 4; g.beginPath(); g.moveTo(-2, cy - 74); g.quadraticCurveTo(6, cy - 56, 20, cy - 46); g.stroke(); }
    else { g.beginPath(); g.arc(0, cy, 75, Math.PI * 0.97, Math.PI * 2.03); g.quadraticCurveTo(70, cy - 30, 52, cy - 34); g.lineTo(44, cy - 20); g.lineTo(30, cy - 40); g.lineTo(18, cy - 24); g.lineTo(2, cy - 42); g.lineTo(-12, cy - 26); g.quadraticCurveTo(-44, cy - 34, -58, cy - 12); g.lineTo(-62, cy + 22); g.quadraticCurveTo(-78, cy + 14, -75, cy + 2); g.fill(); } // curto: franja em pontas e costeleta
    g.strokeStyle = cl; g.globalAlpha = 0.5; g.lineWidth = 7; g.lineCap = 'round'; g.beginPath(); g.arc(0, cy, 60, Math.PI * 1.52, Math.PI * 1.8); g.stroke(); g.globalAlpha = 1;
  }
  const OLHOS = { // abertura (0-1,3), raio do branco, raio da íris, sobrancelha: [altura, inclinação] (inclinação > 0 = bravo, < 0 = triste/medo)
    ponto: [0.82, 14, 8.5, [0, 0]], fixo: [1.08, 16, 6.5, [0.5, 0]], meio: [0.42, 14, 8.5, [-0.2, -0.25]], baixoAberto: [0.6, 14, 8, [0.2, -0.5]], cego: [1.1, 17, 0, [0.3, 0]],
    grande: [1.3, 18, 7.5, [1, -0.5]], lado: [0.86, 14, 8, [0.3, 0]], firme: [0.62, 13, 8, [-0.5, 0.8]],
  };
  function rosto(g, s, v, fx, ey, cy, t) {
    const d = OLHOS[s.olho], lk = s.olhar || 0, ly = s.olharY || 0, pele2 = mix(v.pele, '#3A1D14', 0.34), tinta = '#17120F', iris = v.olhos || '#4A3222', sob = mix(v.cabelo, '#000000', v.estilo === 'careca' || v.estilo === 'calvo' ? 0 : 0.25);
    const fech = s.pisca || 0; g.lineCap = 'round'; g.lineJoin = 'round';
    const olho = ex => {
      if (!d || fech > 0.85) { // fechado (pose ou piscada): cílio em arco
        const cima = s.olho === 'baixo' || (d && fech > 0.85); g.strokeStyle = tinta; g.lineWidth = 6; g.beginPath(); if (cima) g.arc(ex, ey - 6, 13, Math.PI * 0.15, Math.PI * 0.85); else g.arc(ex, ey + 5, 13, Math.PI * 1.1, Math.PI * 1.9); g.stroke(); return; }
      const ab = d[0] * (1 - fech), rx = d[1], ry = Math.max(2, d[1] * 0.92 * Math.min(1.12, ab + 0.12));
      g.save(); g.beginPath(); g.ellipse(ex, ey, rx, ry, 0, 0, TAU); g.clip();
      rect(g, ex - 30, ey - 30, 60, 60, s.olho === 'cego' ? '#DAD9D6' : '#FBF8F2'); rect(g, ex - 30, ey - 30, 60, 30 - ry * 0.55, '#3A2A2A', 0.16); // branco + sombra da pálpebra
      if (d[2]) { const ix = ex + clamp(lk, -rx + d[2] * 0.7, rx - d[2] * 0.7) * 0.75, iy = ey + clamp(ly, -6, 7) + (s.olho === 'baixoAberto' ? 5 : s.olho === 'meio' ? 2 : 0); circ(g, ix, iy, d[2], iris); circ(g, ix, iy, d[2] * 0.52, '#0B0908'); circ(g, ix - d[2] * 0.4, iy - d[2] * 0.45, d[2] * 0.3, '#FFF', 0.95); }
      else circ(g, ex, ey, 15, 'rgba(150,170,190,0.4)');
      g.restore();
      g.strokeStyle = tinta; g.lineWidth = 5; g.beginPath(); g.ellipse(ex, ey, rx, ry, 0, Math.PI * 1.04, Math.PI * 1.96); g.stroke(); // cílio de cima
      g.strokeStyle = pele2; g.lineWidth = 2.5; g.globalAlpha = 0.7; g.beginPath(); g.ellipse(ex, ey, rx, ry, 0, Math.PI * 0.15, Math.PI * 0.85); g.stroke(); g.globalAlpha = 1;
      if (s.brilho) { circ(g, ex - 5, ey - 4, 4, '#FFF', 0.95); g.strokeStyle = 'rgba(207,230,245,0.9)'; g.lineWidth = 4; g.beginPath(); g.arc(ex, ey + 2, 14, Math.PI * 0.2, Math.PI * 0.8); g.stroke(); }
    };
    olho(fx - 24); olho(fx + 24);
    // sobrancelhas: sempre desenhadas; a expressão vem da pose (olho) e de "sobr"
    const [alt0, inc0] = d ? d[3] : [0, s.boca === 'triste' ? -0.6 : 0], alt = 8 * alt0 + 12 * (s.sobr || 0) * (inc0 > 0 ? 0.2 : 1), inc = inc0 + (s.boca === 'triste' && inc0 <= 0 ? -0.35 : 0), by = ey - 31 - alt - fech * -3;
    g.strokeStyle = sob; g.lineWidth = 8; for (const e of [-1, 1]) { const xi = fx + e * 9, xo = fx + e * 43; g.beginPath(); g.moveTo(xi, by + inc * 11); g.quadraticCurveTo(fx + e * 26, by - 6 - inc * 2, xo, by - inc * 5 + 3); g.stroke(); }
    line(g, fx + 7, cy + 12, fx + 12, cy + 21, pele2, 5, 0.75); line(g, fx + 12, cy + 21, fx + 4, cy + 22, pele2, 5, 0.75); // nariz
    const my = cy + 38, fl = s._fala || 0, sil = fl * (0.5 + 0.5 * Math.sin(t * 19)) * (0.55 + 0.45 * Math.sin(t * 6.7 + 1)); g.strokeStyle = tinta; g.fillStyle = tinta; g.lineWidth = 7;
    const boca = (w, h) => { g.fillStyle = '#1B0F10'; g.beginPath(); g.ellipse(fx + 2, my + h * 0.2, w, h, 0, 0, TAU); g.fill(); g.save(); g.clip(); circ(g, fx + 2, my + h * 1.15, w * 0.9, '#8C3B3B'); if (h > 9) rect(g, fx - w, my - h, w * 2, h * 0.45, '#F4F0E6'); g.restore(); };
    if (fl > 0.05 && s.boca !== 'sorriso' && s.boca !== 'O') boca(13 + 3 * sil, 3 + 13 * Math.abs(sil)); // falando: a boca abre e fecha
    else if (s.boca === 'reta') { g.beginPath(); g.moveTo(fx - 13, my); g.quadraticCurveTo(fx, my + 3, fx + 13, my - 1); g.stroke(); }
    else if (s.boca === 'O') boca(13, 19 + Math.sin(t * 14) * 2);
    else if (s.boca === 'aberta') boca(16, 11);
    else if (s.boca === 'pequena') { g.beginPath(); g.ellipse(fx - 6, my, 7, 5.5, 0, 0, TAU); g.fill(); }
    else if (s.boca === 'triste') { g.beginPath(); g.arc(fx, my + 15, 20, Math.PI * 1.17, Math.PI * 1.83); g.stroke(); }
    else if (s.boca === 'sorrisinho') { g.beginPath(); g.arc(fx, my - 11, 17, Math.PI * 0.18, Math.PI * 0.82); g.stroke(); line(g, fx + 15, my - 2, fx + 19, my - 7, tinta, 4); }
    else if (s.boca === 'sorriso') { g.beginPath(); g.moveTo(fx - 34, my - 8); g.quadraticCurveTo(fx, my + 46, fx + 34, my - 8); g.closePath(); g.fill(); g.fillStyle = '#F4F0E6'; g.beginPath(); g.moveTo(fx - 28, my - 4); g.lineTo(fx + 28, my - 4); g.quadraticCurveTo(fx, my + 10, fx - 28, my - 4); g.fill(); }
    g.save(); g.globalAlpha = 0.1; g.fillStyle = '#C0392B'; g.beginPath(); g.ellipse(fx - 40, cy + 22, 13, 8, 0, 0, TAU); g.ellipse(fx + 44, cy + 22, 11, 8, 0, 0, TAU); g.fill(); g.restore(); // cor nas bochechas
  }

  M.FX = { cfg, atmos, camera, olhar, keystone, chao, frente, legendaY, fundoLegenda, pers, vida, sombra, roupa, cabecaBase, cabelo, rosto, PRESETS, PP, CORES };
})();
