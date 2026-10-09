// Kit de áudio por código dos testes de motion (extraído do teste 5 e ampliado depois do pedido do William):
// - efeitos sintetizados (OfflineAudioContext) alinhados pelo PICO no quadro do evento;
// - swoosh DESCENDENTE (pitch em queda) para tudo que desce na tela;
// - DUCKING: a trilha abaixa sob os efeitos (sidechain com lookahead), em vez de o limitador cortar os efeitos;
// - mix em -14 LUFS / -1 dBTP medidos DEPOIS do AAC (BS.1770-4, true peak 4x), erro de pico por evento medido em stem isolado codificado.
// Uso: AudioKit.render({ prefixo, W, H, FPS, DUR, frame(g, t), eventos: [{ nome, tipo, t, nivel, visual, semente?, dur?, folha? }], extra? })
window.AudioKit = (() => {
  const SR = 48000, ALVO_LUFS = -14, TETO_LIMITADOR = -2.0, BITRATE = 192000;
  const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x)), dB = v => 20 * Math.log10(v);
  const seed = a => () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };

  // ---------- síntese ----------
  function ruido(ac, dur, s) { const r = seed(s), b = ac.createBuffer(1, Math.ceil(dur * SR), SR), d = b.getChannelData(0); for (let i = 0; i < d.length; i++) d[i] = r() * 2 - 1; const n = ac.createBufferSource(); n.buffer = b; return n; }
  async function sintetiza(tipo, o = {}) {
    const dur = { clique: 0.15, impacto: 0.5, whoosh: 0.65, tique: 0.04, swooshDesce: o.dur || 0.55 }[tipo], ac = new OfflineAudioContext(1, Math.ceil(dur * SR), SR), s = o.semente || 0;
    if (tipo === 'clique') {
      const n = ruido(ac, dur, 11 + s), bp = ac.createBiquadFilter(), g1 = ac.createGain(); bp.type = 'bandpass'; bp.frequency.value = o.freq ? o.freq * 1.6 : 3500; bp.Q.value = 1.2; // o.freq (opcional): afinação do estalo
      g1.gain.setValueAtTime(0, 0); g1.gain.linearRampToValueAtTime(1, 0.0015); g1.gain.exponentialRampToValueAtTime(0.001, 0.05);
      const os = ac.createOscillator(), g2 = ac.createGain(); os.frequency.value = o.freq || 2200; g2.gain.setValueAtTime(0, 0); g2.gain.linearRampToValueAtTime(0.5, 0.001); g2.gain.exponentialRampToValueAtTime(0.001, 0.07);
      n.connect(bp).connect(g1).connect(ac.destination); os.connect(g2).connect(ac.destination); n.start(0); os.start(0);
    } else if (tipo === 'impacto') {
      const os = ac.createOscillator(), g1 = ac.createGain(); os.frequency.setValueAtTime(150, 0); os.frequency.exponentialRampToValueAtTime(42, 0.18);
      g1.gain.setValueAtTime(0, 0); g1.gain.linearRampToValueAtTime(1, 0.004); g1.gain.exponentialRampToValueAtTime(0.001, 0.42);
      const n = ruido(ac, dur, 22 + s), lp = ac.createBiquadFilter(), g2 = ac.createGain(); lp.type = 'lowpass'; lp.frequency.value = 900;
      g2.gain.setValueAtTime(0, 0); g2.gain.linearRampToValueAtTime(0.35, 0.002); g2.gain.exponentialRampToValueAtTime(0.001, 0.035);
      os.connect(g1).connect(ac.destination); n.connect(lp).connect(g2).connect(ac.destination); os.start(0); n.start(0);
    } else if (tipo === 'whoosh') { // sobe: banda 400 -> 3200 Hz, pico ~0,45 s depois do início
      const n = ruido(ac, dur, 33 + s), bp = ac.createBiquadFilter(), g1 = ac.createGain(); bp.type = 'bandpass'; bp.Q.value = 0.9;
      bp.frequency.setValueAtTime(400, 0); bp.frequency.exponentialRampToValueAtTime(3200, 0.45);
      g1.gain.setValueAtTime(0.001, 0); g1.gain.exponentialRampToValueAtTime(1, 0.45); g1.gain.linearRampToValueAtTime(0, 0.53);
      n.connect(bp).connect(g1).connect(ac.destination); n.start(0);
    } else if (tipo === 'swooshDesce') { // desce: banda 3000 -> 260 Hz e um tom 1100 -> 170 Hz, os dois em queda; pico na chegada, corte em 70 ms
      const P = dur - 0.08, n = ruido(ac, dur, 44 + s), bp = ac.createBiquadFilter(), g1 = ac.createGain(); bp.type = 'bandpass'; bp.Q.value = 1.1;
      bp.frequency.setValueAtTime(3000, 0); bp.frequency.exponentialRampToValueAtTime(260, P);
      g1.gain.setValueAtTime(0.001, 0); g1.gain.exponentialRampToValueAtTime(1, P); g1.gain.linearRampToValueAtTime(0, P + 0.07);
      const os = ac.createOscillator(), g2 = ac.createGain(); os.type = 'triangle'; os.frequency.setValueAtTime(1100, 0); os.frequency.exponentialRampToValueAtTime(170, P);
      g2.gain.setValueAtTime(0.0005, 0); g2.gain.exponentialRampToValueAtTime(0.35, P); g2.gain.linearRampToValueAtTime(0, P + 0.07);
      const ck = ac.createOscillator(), g3 = ac.createGain(); ck.frequency.value = 900; g3.gain.setValueAtTime(0, 0); g3.gain.setValueAtTime(0, P - 0.0008); g3.gain.linearRampToValueAtTime(1.6, P); g3.gain.exponentialRampToValueAtTime(0.001, P + 0.012); ck.connect(g3).connect(ac.destination); ck.start(0); // reel30: transiente de chegada no pico (o pico de ruído puro mudava de lugar no AAC)
      n.connect(bp).connect(g1).connect(ac.destination); os.connect(g2).connect(ac.destination); n.start(0); os.start(0);
    } else if (tipo === 'tique') { // quique do contato: estalo curto e agudo
      const n = ruido(ac, dur, 55 + s), hp = ac.createBiquadFilter(), g1 = ac.createGain(); hp.type = 'highpass'; hp.frequency.value = 4500;
      g1.gain.setValueAtTime(0, 0); g1.gain.linearRampToValueAtTime(1, 0.0008); g1.gain.exponentialRampToValueAtTime(0.001, 0.009);
      const os = ac.createOscillator(), g2 = ac.createGain(); os.frequency.value = o.freq || 3600 + 400 * seed(s + 7)(); g2.gain.setValueAtTime(0, 0); g2.gain.linearRampToValueAtTime(0.35, 0.0006); g2.gain.exponentialRampToValueAtTime(0.001, 0.014);
      n.connect(hp).connect(g1).connect(ac.destination); os.connect(g2).connect(ac.destination); n.start(0); os.start(0);
    } else throw new Error('tipo de efeito desconhecido: ' + tipo);
    return (await ac.startRendering()).getChannelData(0).slice();
  }
  const picoAmostra = (x, a = 0, b = x.length) => { let m = 0, k = a; for (let i = Math.max(0, a); i < Math.min(x.length, b); i++) { const v = Math.abs(x[i]); if (v > m) { m = v; k = i; } } return { k, v: m }; };
  function picoEnvelope(x, a = 0, b = x.length, jan = 480) { // RMS em 10 ms, centrado
    let s = 0, m = 0, k = a; const h = jan >> 1;
    for (let i = Math.max(0, a - h); i < Math.min(x.length, a + h); i++) s += x[i] * x[i];
    for (let i = a; i < b; i++) { const add = i + h, sub = i - h; if (add < x.length) s += x[add] * x[add]; if (sub >= 0) s -= x[sub] * x[sub]; if (s > m) { m = s; k = i; } }
    return { k, rms: Math.sqrt(Math.max(m, 0) / jan) };
  }

  // ---------- medição: BS.1770-4 e true peak ----------
  function biquad(x, b, a) { const y = new Float32Array(x.length); let x1 = 0, x2 = 0, y1 = 0, y2 = 0; for (let i = 0; i < x.length; i++) { const v = b[0] * x[i] + b[1] * x1 + b[2] * x2 - a[1] * y1 - a[2] * y2; x2 = x1; x1 = x[i]; y2 = y1; y1 = v; y[i] = v; } return y; }
  function lufs(chs) {
    const K = c => biquad(biquad(c, [1.53512485958697, -2.69169618940638, 1.19839281085285], [1, -1.69065929318241, 0.73248077421585]), [1, -2, 1], [1, -1.99004745483398, 0.99007225036621]);
    const kw = chs.map(K), bl = 0.4 * SR, st = 0.1 * SR, z = [];
    for (let s = 0; s + bl <= kw[0].length; s += st) { let e = 0; for (const c of kw) { let a = 0; for (let i = s; i < s + bl; i++) a += c[i] * c[i]; e += a / bl; } z.push(e); }
    const L = e => -0.691 + 10 * Math.log10(e), g1 = z.filter(e => L(e) > -70); if (!g1.length) return -Infinity;
    const rel = L(g1.reduce((a, b) => a + b, 0) / g1.length) - 10, g2 = g1.filter(e => L(e) > rel);
    return L(g2.reduce((a, b) => a + b, 0) / g2.length);
  }
  const FIR = (() => { const T = 48, P = 4, h = new Float32Array(T * P); for (let i = 0; i < T * P; i++) { const n = i - (T * P - 1) / 2, x = n / P, s = x === 0 ? 1 : Math.sin(Math.PI * x) / (Math.PI * x), w = 0.42 - 0.5 * Math.cos(2 * Math.PI * i / (T * P - 1)) + 0.08 * Math.cos(4 * Math.PI * i / (T * P - 1)); h[i] = s * w; } return { h, T, P }; })();
  function truePeakSerie(c) {
    const { h, T, P } = FIR, out = new Float32Array(c.length);
    for (let n = 0; n < c.length; n++) { let m = Math.abs(c[n]); for (let p = 0; p < P; p++) { let y = 0; for (let k = 0; k < T; k++) { const j = n - k + (T >> 1); if (j >= 0 && j < c.length) y += c[j] * h[k * P + p]; } if (Math.abs(y) > m) m = Math.abs(y); } out[n] = m; }
    return out;
  }
  const truePeak = chs => dB(Math.max(...chs.map(c => truePeakSerie(c).reduce((a, b) => b > a ? b : a, 0))));
  const picoAmostraDb = chs => dB(Math.max(...chs.map(c => picoAmostra(c).v)));
  function limita(chs, tetoDb) { // lookahead 5 ms sobre o true peak (igual ao teste 5)
    const teto = Math.pow(10, tetoDb / 20), n = chs[0].length, L = 240, rel = 1 - Math.exp(-1 / (0.1 * SR));
    const tp = chs.map(truePeakSerie), req = new Float32Array(n);
    for (let i = 0; i < n; i++) { const p = Math.max(tp[0][i], tp[1][i]); req[i] = p > teto ? teto / p : 1; }
    const m = new Float32Array(n); for (let i = 0; i < n; i++) { let v = 1; for (let k = i; k < Math.min(n, i + L); k++) if (req[k] < v) v = req[k]; m[i] = v; }
    let env = 1; for (let i = 0; i < n; i++) { env = Math.min(m[i], env + (1 - env) * rel); m[i] = env; }
    const g = new Float32Array(n); let s = 0; for (let i = 0; i < n; i++) { s += m[i]; if (i >= L) s -= m[i - L]; g[i] = Math.min(m[i], s / Math.min(i + 1, L)); }
    let red = 1; for (let i = 0; i < n; i++) if (g[i] < red) red = g[i];
    return { out: chs.map(c => c.map((v, i) => v * g[i])), reducaoMaxDb: dB(red), g };
  }
  // ducking: envelope de pico do stem de efeitos com lookahead de 15 ms (ataque instantâneo, soltura 180 ms),
  // ganho da trilha = maxDb * min(1, env/ref), suavizado em 6 ms. A trilha já está baixa quando o pico chega.
  function ducking(sfx, maxDb, ref) {
    const n = sfx.length, look = Math.round(0.015 * SR), rel = Math.exp(-1 / (0.18 * SR)), sm = 1 - Math.exp(-1 / (0.006 * SR)), g = new Float32Array(n);
    const ab = Float32Array.from(sfx, Math.abs), adiante = new Float32Array(n); // máximo deslizante em [i, i+look] (deque monotônico)
    const dq = []; let h = 0; for (let i = n - 1; i >= 0; i--) { while (dq.length > h && ab[dq[dq.length - 1]] <= ab[i]) dq.pop(); dq.push(i); while (dq[h] > i + look) h++; adiante[i] = ab[dq[h]]; }
    let env = 0, gs = 1; for (let i = 0; i < n; i++) { env = Math.max(adiante[i], env * rel); const alvo = Math.pow(10, maxDb * Math.min(1, env / ref) / 20); gs += (alvo - gs) * (alvo < gs ? sm * 4 : sm); g[i] = gs; }
    return g;
  }

  // ---------- AAC ----------
  async function codificaAAC(chs, N, video) {
    const mux = new Mp4Muxer.Muxer({ target: new Mp4Muxer.ArrayBufferTarget(), ...(video ? { video: { codec: 'avc', width: video.W, height: video.H, frameRate: video.FPS } } : {}), audio: { codec: 'aac', numberOfChannels: 2, sampleRate: SR }, fastStart: 'in-memory' });
    let err = null;
    const ae = new AudioEncoder({ output: (c, m) => mux.addAudioChunk(c, m), error: e => err = e }); ae.configure({ codec: 'mp4a.40.2', sampleRate: SR, numberOfChannels: 2, bitrate: BITRATE });
    const [L, R] = chs;
    for (let i = 0; i < N; i += 1024) { const n = Math.min(1024, N - i), d = new Float32Array(n * 2); d.set(L.subarray(i, i + n), 0); d.set(R.subarray(i, i + n), n); const ad = new AudioData({ format: 'f32-planar', sampleRate: SR, numberOfFrames: n, numberOfChannels: 2, timestamp: Math.round(i * 1e6 / SR), data: d }); ae.encode(ad); ad.close(); }
    if (video) {
      const { W, H, FPS, DUR, frame } = video, cv = document.createElement('canvas'); cv.width = W; cv.height = H; const g = cv.getContext('2d');
      const ve = new VideoEncoder({ output: (c, m) => mux.addVideoChunk(c, m), error: e => err = e }); ve.configure({ codec: 'avc1.640032', width: W, height: H, bitrate: video.bitrate || 3.2e6, framerate: FPS });
      for (let f = 0; f < Math.round(DUR * FPS); f++) { frame(g, f / FPS); const vf = new VideoFrame(cv, { timestamp: Math.round(f * 1e6 / FPS) }); ve.encode(vf, { keyFrame: f % 60 === 0 }); vf.close(); if (ve.encodeQueueSize > 10) await new Promise(r => setTimeout(r, 5)); document.title = `video ${f}`; }
      await ve.flush();
    }
    await ae.flush(); if (err) throw err; mux.finalize(); return mux.target.buffer;
  }
  async function decodifica(buf) { const b = await new OfflineAudioContext(2, SR, SR).decodeAudioData(buf.slice(0)); return { chs: [b.getChannelData(0).slice(), b.getChannelData(b.numberOfChannels > 1 ? 1 : 0).slice()], sr: b.sampleRate, len: b.length }; }
  function atraso(ref, x, centro, meia = 12000, busca = 3000) {
    let best = -Infinity, lag = 0; const a = Math.max(0, centro - meia), b = Math.min(ref.length, centro + meia);
    let nr = 0; for (let i = a; i < b; i++) nr += ref[i] * ref[i];
    for (let l = -busca; l <= busca; l++) { let s = 0, nx = 0; for (let i = a; i < b; i++) { const j = i + l; if (j < 0 || j >= x.length) continue; s += ref[i] * x[j]; nx += x[j] * x[j]; } const c = s / Math.sqrt(nr * nx + 1e-20); if (c > best) { best = c; lag = l; } }
    return { lag, corr: best };
  }
  const salvar = (name, body) => fetch(`/save?name=${name}`, { method: 'POST', body });
  function wav(chs) { const n = chs[0].length, b = new ArrayBuffer(44 + n * 4), v = new DataView(b), s = (o, t) => [...t].forEach((c, i) => v.setUint8(o + i, c.charCodeAt(0)));
    s(0, 'RIFF'); v.setUint32(4, 36 + n * 4, true); s(8, 'WAVEfmt '); v.setUint32(16, 16, true); v.setUint16(20, 1, true); v.setUint16(22, 2, true); v.setUint32(24, SR, true); v.setUint32(28, SR * 4, true); v.setUint16(32, 4, true); v.setUint16(34, 16, true); s(36, 'data'); v.setUint32(40, n * 4, true);
    for (let i = 0; i < n; i++) for (let c = 0; c < 2; c++) v.setInt16(44 + i * 4 + c * 2, Math.round(clamp(chs[c][i], -1, 1) * 32767), true); return b; }

  async function render(cfg) {
    const { prefixo, W, H, FPS, DUR, frame } = cfg, N = SR * DUR, EV = cfg.eventos, DUCK = cfg.duck || { maxDb: -10, ref: 0.2 };
    const R = { alvo: { lufs: ALVO_LUFS, dbtp: -1, medidoDepoisDoAAC: true }, aac: { codec: 'mp4a.40.2', bitrate: BITRATE, sr: SR }, ducking: { ...DUCK, lookahead_ms: 15, soltura_ms: 180, nota: 'trilha abaixa sob os efeitos; o limitador fica só como rede' }, ...(cfg.extra || {}) };
    // 1) efeitos: pico de cada um e posição de início para o PICO cair no quadro do evento
    for (const e of EV) {
      const qf = e.t * FPS; if (Math.abs(qf - Math.round(qf)) > 1e-6) throw new Error(`evento ${e.nome} fora de quadro inteiro`);
      const x = await sintetiza(e.tipo, e), p = picoAmostra(x); for (let i = 0; i < x.length; i++) x[i] *= e.nivel / p.v;
      e._x = x; e.quadroAlvo = Math.round(qf); e.picoNoEfeito_ms = +(p.k / SR * 1000).toFixed(2); e.picoEnvelopeNoEfeito_ms = +(picoEnvelope(x).k / SR * 1000).toFixed(2);
      e.inicioAmostra = Math.round(e.t * SR) - p.k; e.inicio_s = +(e.inicioAmostra / SR).toFixed(5);
    }
    const sfx = new Float32Array(N); for (const e of EV) for (let i = 0; i < e._x.length; i++) { const j = e.inicioAmostra + i; if (j >= 0 && j < N) sfx[j] += e._x[i]; }
    // 2) trilha: 0-DUR s de stems/music.wav, entrada 0,05 s e saída 0,4 s, cama em -16 LUFS, depois ducking
    const mus = await new OfflineAudioContext(2, SR, SR).decodeAudioData(await (await fetch('/w/stems/music.wav')).arrayBuffer());
    let m;
    if (cfg.trilha) { // opcional (reel30): cfg.trilha.pos(t) = posição na música em s (null = silêncio) e cfg.trilha.ganho(t) = envelope; interpolação linear
      const src = [0, 1].map(c => mus.getChannelData(Math.min(c, mus.numberOfChannels - 1))), msr = mus.sampleRate; m = [new Float32Array(N), new Float32Array(N)];
      for (let i = 0; i < N; i++) { const t = i / SR, p = cfg.trilha.pos(t); if (p == null) continue; const x = p * msr, j = Math.floor(x), fr = x - j, gn = cfg.trilha.ganho(t); if (j + 1 >= src[0].length) continue;
        for (let c = 0; c < 2; c++) m[c][i] = (src[c][j] * (1 - fr) + src[c][j + 1] * fr) * gn; }
    } else {
      m = [0, 1].map(c => mus.getChannelData(Math.min(c, mus.numberOfChannels - 1)).slice(0, N));
      for (let i = 0; i < N; i++) { const t = i / SR, f = Math.min(1, t / 0.05, (DUR - t) / 0.4); m[0][i] *= f; m[1][i] *= f; }
    }
    R.trilha = { arquivo: 'stems/music.wav', trecho: cfg.trilha ? cfg.trilha.descricao : `0-${DUR} s`, lufsOriginal: +lufs(m).toFixed(2) };
    const gm = Math.pow(10, (-16 - R.trilha.lufsOriginal) / 20); m.forEach(c => { for (let i = 0; i < N; i++) c[i] *= gm; }); R.trilha.ganhoCama_dB = +dB(gm).toFixed(2);
    const gd = ducking(sfx, DUCK.maxDb, DUCK.ref); m.forEach(c => { for (let i = 0; i < N; i++) c[i] *= gd[i]; });
    R.trilha.lufsDepoisDoDucking = +lufs(m).toFixed(2);
    const mixBruto = [m[0].map((v, i) => v + sfx[i]), m[1].map((v, i) => v + sfx[i])];
    R.mixBruto = { lufs: +lufs(mixBruto).toFixed(2) };
    // 3) ganho para -14, limitador TP em -1,5 dBTP, AAC, decodifica, mede; corrige e repete
    let ganho = ALVO_LUFS - R.mixBruto.lufs, final = null; R.iteracoes = [];
    for (let it = 0; it < 6; it++) {
      const g = Math.pow(10, ganho / 20), pre = mixBruto.map(c => c.map(v => v * g)), lim = limita(pre, TETO_LIMITADOR);
      const dec = await decodifica(await codificaAAC(lim.out, N, null)), L = lufs(dec.chs), tp = truePeak(dec.chs);
      R.iteracoes.push({ ganho_dB: +ganho.toFixed(2), reducaoLimitadorMax_dB: +lim.reducaoMaxDb.toFixed(2), posAAC_lufs: +L.toFixed(2), posAAC_dbtp: +tp.toFixed(2) });
      document.title = `iteracao ${it} ${L.toFixed(2)} LUFS ${tp.toFixed(2)} dBTP`;
      final = { g, lim }; if (Math.abs(L - ALVO_LUFS) <= 0.1 && tp <= -1) break; ganho += ALVO_LUFS - L;
    }
    // 4) render final com vídeo; medido no mp4 decodificado
    const mp4 = await codificaAAC(final.lim.out, N, { W, H, FPS, DUR, frame, bitrate: cfg.bitrateVideo });
    await salvar(`${prefixo}_30fps.mp4`, new Blob([mp4]));
    const dec = await decodifica(mp4);
    R.final = { arquivo: `${prefixo}_30fps.mp4`, bytes: mp4.byteLength, srDecodificado: dec.sr, amostrasDecodificadas: dec.len, amostrasEsperadas: N,
      lufsIntegrado: +lufs(dec.chs).toFixed(2), dbtp: +truePeak(dec.chs).toFixed(2), picoAmostra_dBFS: +picoAmostraDb(dec.chs).toFixed(2) };
    R.final.metaLUFS_ok = Math.abs(R.final.lufsIntegrado - ALVO_LUFS) <= 0.5; R.final.metaDBTP_ok = R.final.dbtp <= -1;
    const mixRef = final.lim.out[0], lagGlobal = atraso(mixRef, dec.chs[0], Math.round(DUR / 2 * SR), 2 * SR, 3000);
    R.atrasoGlobalAAC = { amostras: lagGlobal.lag, ms: +(lagGlobal.lag / SR * 1000).toFixed(2), correlacao: +lagGlobal.corr.toFixed(4) };
    // 5) por evento: stem ISOLADO (com o mesmo ganho e a mesma curva do limitador), codificado em AAC e decodificado; pico medido em ±100 ms
    for (const e of EV) {
      const c = Math.round(e.t * SR), so = new Float32Array(N); for (let i = 0; i < e._x.length; i++) { const j = e.inicioAmostra + i; if (j >= 0 && j < N) so[j] = e._x[i] * final.g * final.lim.g[j]; }
      const d = await decodifica(await codificaAAC([so, so], N, null)), a = c - 0.1 * SR, b = c + 0.1 * SR;
      const pPre = picoAmostra(so, a, b), pA = picoAmostra(d.chs[0], a, b), pE = picoEnvelope(d.chs[0], a, b), xm = atraso(mixRef, dec.chs[0], c, 0.1 * SR, 2400);
      Object.assign(e, { erroPicoAmostra_ms_antesDoAAC: +((pPre.k - c) / SR * 1000).toFixed(3), erroPicoAmostra_ms_depoisDoAAC: +((pA.k - c) / SR * 1000).toFixed(3),
        erroPicoEnvelope10ms_ms_depoisDoAAC: +((pE.k - c) / SR * 1000).toFixed(3), deslocamentoCorrelacao_ms_mix: +(xm.lag / SR * 1000).toFixed(3),
        reducaoLimitadorNoPico_dB: +dB(final.lim.g[c]).toFixed(2), duckingTrilhaNoPico_dB: +dB(gd[c]).toFixed(2), picoEfeitoFinal_dBFS: +dB(pA.v).toFixed(2) });
      document.title = `evento ${e.nome}`;
    }
    R.eventos = EV.map(({ _x, ...r }) => r);
    R.resumo = { eventos: EV.length, maxErroPicoAmostraDepoisDoAAC_ms: Math.max(...EV.map(e => Math.abs(e.erroPicoAmostra_ms_depoisDoAAC))), maxReducaoLimitadorNoPicoDeEfeito_dB: Math.min(...EV.map(e => e.reducaoLimitadorNoPico_dB)) };
    R.video = { fps: FPS, quadros: Math.round(DUR * FPS), nota: 'eventos em quadro inteiro; 1 quadro = 33,3 ms' };
    // 6) folha: 4 quadros por evento marcado (f-2..f+1) + forma de onda decodificada ±200 ms (vermelho = alvo)
    const FEtodos = EV.filter(e => e.folha !== false), porParte = cfg.folhaPorParte || FEtodos.length, sw = 270, sh = 480, wh = 150; // cfg.folhaPorParte (opcional): divide a folha em arquivos _1, _2...
    for (let parte = 0; parte * porParte < FEtodos.length; parte++) {
    const FE = FEtodos.slice(parte * porParte, (parte + 1) * porParte), sheet = document.createElement('canvas'); sheet.width = sw * 4; sheet.height = (sh + wh) * FE.length; const sg = sheet.getContext('2d');
    const cv = document.createElement('canvas'); cv.width = W; cv.height = H; const cg = cv.getContext('2d');
    sg.fillStyle = BRAND.ink; sg.fillRect(0, 0, sheet.width, sheet.height);
    FE.forEach((e, r) => {
      const y0 = r * (sh + wh);
      for (let k = 0; k < 4; k++) { const f = e.quadroAlvo - 2 + k; frame(cg, f / FPS); sg.drawImage(cv, k * sw, y0, sw, sh); sg.font = '700 18px "Geist Mono"'; sg.fillStyle = f === e.quadroAlvo ? BRAND.accent : BRAND.mute; sg.fillText(`q${f}  ${(f / FPS).toFixed(3)} s`, k * sw + 8, y0 + 24); }
      const c = Math.round(e.t * SR), a = c - 0.2 * SR, d = dec.chs[0], yy = y0 + sh + wh / 2;
      sg.strokeStyle = BRAND.paper; sg.globalAlpha = 0.85; sg.beginPath();
      for (let px = 0; px < sheet.width; px++) { const i0 = a + Math.floor(px / sheet.width * 0.4 * SR), i1 = a + Math.floor((px + 1) / sheet.width * 0.4 * SR); let mn = 0, mx = 0; for (let i = i0; i < i1; i++) { if (d[i] < mn) mn = d[i]; if (d[i] > mx) mx = d[i]; } sg.moveTo(px + 0.5, yy - mx * 60); sg.lineTo(px + 0.5, yy - mn * 60 + 1); }
      sg.stroke(); sg.globalAlpha = 1; sg.fillStyle = BRAND.accent; sg.fillRect(sheet.width / 2 - 1, y0 + sh + 6, 3, wh - 12);
      sg.font = '700 18px "Geist Mono"'; sg.fillStyle = BRAND.paper;
      sg.fillText(`${e.nome}  alvo ${e.t.toFixed(3)} s  erro pico ${e.erroPicoAmostra_ms_depoisDoAAC} ms  limitador ${e.reducaoLimitadorNoPico_dB} dB  trilha ${e.duckingTrilhaNoPico_dB} dB`, 8, y0 + sh + 22);
    });
    await salvar(porParte < FEtodos.length ? `${prefixo}_folha_eventos_${parte + 1}.png` : `${prefixo}_folha_eventos.png`, await new Promise(r => sheet.toBlob(r, 'image/png')));
    }
    if (cfg.depois) await cfg.depois(R, dec, final); // opcional (reel30): medições extras no mp4 decodificado antes de gravar o json
    await salvar(`${prefixo}_mix_preAAC.wav`, new Blob([wav(final.lim.out)]));
    await salvar(`${prefixo}_medicoes.json`, new Blob([JSON.stringify(R, null, 2)]));
    document.body.insertAdjacentHTML('beforeend', `<pre>${JSON.stringify(R.final)}</pre>`); document.title = 'DONE';
    return R;
  }
  return { SR, seed, sintetiza, lufs, truePeak, render, salvar };
})();
