// Kit dos episódios narrados (1080×1920): falas do ElevenLabs em sequência, legenda palavra a palavra, glitch e render em mp4.
// Cada episódio só define FALAS (texto, palavras em destaque, cena) e as funções de cena: cena(g, u, k, fr, tt).
window.EpKit = (() => {
  const W = 1080, H = 1920, FPS = 30;
  const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x)), out = x => 1 - Math.pow(1 - x, 3), inout = x => x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
  const rnd = n => { const s = Math.sin(n * 127.1) * 43758.5453; return s - Math.floor(s); }; // pseudoaleatório determinístico por quadro
  function txt(g, s, x, y, size, col, o = {}) { g.font = `${o.w || 900} ${size}px ${o.mono ? '"Geist Mono"' : 'Geist'}`; g.letterSpacing = o.mono ? '0px' : `${-0.04 * size}px`; g.textAlign = o.align || 'left'; g.fillStyle = col; g.fillText(s, x, y); g.textAlign = 'left'; }
  function glitch(g, draw, amt, fr) { // aberração cromática + fatias deslocadas
    if (amt <= 0.01) return draw(0, 0, null);
    g.save(); g.globalCompositeOperation = 'lighter'; g.globalAlpha = 0.55 * amt; draw(-14 * amt, 0, '#EEEDE8'); draw(14 * amt, 0, '#FF2A00'); g.restore(); draw(0, 0, null);
    for (let i = 0, n = Math.round(3 + amt * 6); i < n; i++) { const y = rnd(fr * 7 + i) * H, h = 8 + rnd(fr * 3 + i) * 60 * amt, dx = (rnd(fr * 11 + i) - 0.5) * 90 * amt; g.drawImage(g.canvas, 0, y, W, h, dx, y, W, h); }
  }
  function wrap(g, words, maxW) { const lines = [[]]; let w = 0; for (const wd of words) { const ww = g.measureText(wd + ' ').width; if (w + ww > maxW && lines.at(-1).length) { lines.push([]); w = 0; } lines.at(-1).push(wd); w += ww; } return lines; }
  function legenda(g, f, k) { // acima da faixa que a interface do Reels/TikTok cobre
    const size = f.txt.length > 90 ? 50 : f.txt.length > 60 ? 56 : 64; g.font = `800 ${size}px Geist`; g.letterSpacing = `${-0.03 * size}px`; g.textBaseline = 'alphabetic';
    const words = f.txt.split(' '), lines = wrap(g, words, W - 180), n = words.length; let idx = 0, y = 1470 - (lines.length - 1) * size * 1.12;
    for (const ln of lines) { let x = 90; for (const wd of ln) { const a = clamp((k * n * 1.12 - idx) * 3); g.globalAlpha = 0.22 + 0.78 * a; g.fillStyle = a > 0.5 && f.acc.includes(wd) ? BRAND.accent : BRAND.paper; g.fillText(wd, x, y); x += g.measureText(wd + ' ').width; idx++; } y += size * 1.12; }
    g.globalAlpha = 1;
  }
  // opts: { falas, stems, out, dir, cenas, lead, gap, tail, musica(ti, i, u) -> volume, bitrate }
  async function run(opts) {
    const q = new URLSearchParams(location.search), F = opts.falas, LEAD = opts.lead ?? 0.2, GAP = opts.gap ?? 0.35, TAIL = opts.tail ?? 0.8;
    await loadBrandFonts(); if (opts.prep) await opts.prep();
    const SR = 48000, ac = new OfflineAudioContext(2, SR, SR);
    // sem narração (fatos rápidos): cada fala dura o tempo de leitura (~0,34 s por palavra), só texto + trilha
    const vozes = opts.semVoz ? F.map(() => null) : await Promise.all(F.map((_, i) => fetch(`${opts.stems}/fala${i + 1}.mp3`).then(r => r.arrayBuffer()).then(b => ac.decodeAudioData(b))));
    const durTexto = f => Math.max(1.6, f.txt.split(' ').length * 0.34 + 0.4);
    let t = LEAD; F.forEach((f, i) => { f.t0 = t; f.dur = vozes[i] ? vozes[i].duration : (f.dur || durTexto(f)); t += f.dur + (f.pausa ?? GAP); }); const DUR = Math.ceil((t + TAIL) * FPS) / FPS;
    const cv = document.createElement('canvas'); cv.width = W; cv.height = H; document.body.append(cv); const g = cv.getContext('2d');
    const cur = tt => { const i = F.findIndex(f => tt < f.t0 + f.dur + (f.pausa ?? GAP)); return i < 0 ? F.length - 1 : i; };
    async function frame(tt) {
      const fr = Math.round(tt * FPS), i = cur(tt), f = F[i], u = tt - f.t0, k = clamp(u / f.dur);
      g.fillStyle = BRAND.ink; g.fillRect(0, 0, W, H);
      await opts.cenas[f.cena](g, u, k, fr, tt);
      legenda(g, f, k);
      const cut = clamp(1 - u / 0.12); if (i > 0 && cut > 0 && f.corte !== false) glitch(g, () => {}, 0.7 * cut, fr + 999);
      grain(g, W, H, opts.grao ?? 0.07);
      if (tt > DUR - 0.3) { g.fillStyle = `rgba(12,12,13,${clamp((tt - (DUR - 0.3)) / 0.3)})`; g.fillRect(0, 0, W, H); }
    }
    if (q.has('sheet')) { // folha de conferência: um quadro no meio do fim de cada fala, lado a lado
      const n = F.length, sw = 270, sh = 480, sheet = document.createElement('canvas'); sheet.width = sw * 4; sheet.height = sh * Math.ceil(n / 4); const sg = sheet.getContext('2d');
      for (let i = 0; i < n; i++) { await frame(F[i].t0 + F[i].dur * 0.85); sg.drawImage(cv, (i % 4) * sw, Math.floor(i / 4) * sh, sw, sh); }
      cv.replaceWith(sheet); sheet.style.width = '100%'; document.title = 'ready ' + DUR.toFixed(1); return;
    }
    if (!q.has('save')) { await frame(+(q.get('t') || 1)); document.title = 'ready ' + DUR.toFixed(1); return; }
    const len = Math.round(SR * DUR), L = new Float32Array(len), R = new Float32Array(len);
    const mus = await new OfflineAudioContext(2, SR, SR).decodeAudioData(await (await fetch('/w/stems/music.wav')).arrayBuffer());
    const m0 = mus.getChannelData(0), m1 = mus.getChannelData(1), ml = m0.length;
    let vol = 0; for (let i = 0; i < len; i++) { const ti = i / SR, ci = cur(ti), target = opts.musica ? opts.musica(ti, ci, ti - F[ci].t0) : 0.14; vol += (target - vol) * 0.00012; // volume desliza, sem degrau
      const fade = Math.min(1, ti / 0.4, (DUR - ti) / 0.8), j = Math.floor(ti * mus.sampleRate) % ml; L[i] = m0[j] * vol * fade; R[i] = m1[j] * vol * fade; }
    vozes.forEach((b, n) => { if (!b) return; const off = Math.round(F[n].t0 * SR), d0 = b.getChannelData(0), d1 = b.numberOfChannels > 1 ? b.getChannelData(1) : d0, r = b.sampleRate / SR;
      for (let i = 0; i < b.duration * SR && off + i < len; i++) { const j = Math.floor(i * r); L[off + i] += d0[j] * 0.95; R[off + i] += d1[j] * 0.95; } });
    for (let i = 0; i < len; i++) { L[i] = Math.max(-1, Math.min(1, L[i])); R[i] = Math.max(-1, Math.min(1, R[i])); }
    const mux = new Mp4Muxer.Muxer({ target: new Mp4Muxer.ArrayBufferTarget(), video: { codec: 'avc', width: W, height: H, frameRate: FPS }, audio: { codec: 'aac', numberOfChannels: 2, sampleRate: SR }, fastStart: 'in-memory' });
    let err = null;
    const ve = new VideoEncoder({ output: (c, m) => mux.addVideoChunk(c, m), error: e => err = e }); ve.configure({ codec: 'avc1.640032', width: W, height: H, bitrate: opts.bitrate || 3.2e6, framerate: FPS });
    const ae = new AudioEncoder({ output: (c, m) => mux.addAudioChunk(c, m), error: e => err = e }); ae.configure({ codec: 'mp4a.40.2', sampleRate: SR, numberOfChannels: 2, bitrate: 160000 });
    for (let i = 0; i < len; i += 1024) { const n = Math.min(1024, len - i), d = new Float32Array(n * 2); d.set(L.subarray(i, i + n), 0); d.set(R.subarray(i, i + n), n); const ad = new AudioData({ format: 'f32-planar', sampleRate: SR, numberOfFrames: n, numberOfChannels: 2, timestamp: Math.round(i * 1e6 / SR), data: d }); ae.encode(ad); ad.close(); }
    for (let fr = 0; fr < Math.round(DUR * FPS); fr++) {
      await frame(fr / FPS); const vf = new VideoFrame(cv, { timestamp: Math.round(fr * 1e6 / FPS) }); ve.encode(vf, { keyFrame: fr % 60 === 0 }); vf.close();
      if (ve.encodeQueueSize > 10) await new Promise(r => setTimeout(r, 5)); document.title = `${fr}/${Math.round(DUR * FPS)}`;
    }
    await ve.flush(); await ae.flush(); if (err) throw err; mux.finalize();
    await fetch(`/save?dir=${opts.dir}&name=${opts.out}`, { method: 'POST', body: mux.target.buffer });
    document.title = 'ready ' + DUR.toFixed(2);
  }
  return { W, H, FPS, clamp, out, inout, rnd, txt, glitch, run };
})();
