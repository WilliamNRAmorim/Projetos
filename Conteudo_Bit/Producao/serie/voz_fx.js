/* voz_fx.js - efeitos de voz offline (JS puro, sem Web Audio), para o motor da série.
 * VozFx.sussurro(x, sr, opts) -> Float32Array: sussurro v2 (o edge-tts não tem estilo de sussurro): ~45% voz original em passa-alta 850 Hz + ~55% ruído
 *   com os formantes da voz (LPC), sopro antes da palavra, compressão leve, reverb curto, sem chiado acima de 8 kHz. Opções descritas na função.
 * VozFx.sussurroV1: a v1 (vocoder de 18 bandas), reprovada pelo William em 25/10 (chiado, pouco inteligível); fica para comparação.
 * VozFx.inteligibilidade(original, resultado, sr, offset): correlação de envelope 1-4 kHz, contraste do envelope, fidelidade espectral (formantes) e fração de chiado > 6 kHz.
 * VozFx.medir(x, sr) -> { rmsDb, picoDb, tonal (0..1, autocorrelação máxima 80-400 Hz nos trechos com voz), agudos (fração da energia acima de 2 kHz) }
 * Uso no JSON do episódio: "falas": [{ "quem": "sete", "texto": "Bia...", "efeito": "sussurro" }]
 */
(function (root) {
  'use strict';
  function rng(a) { return function () { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  function biquad(type, f, q, sr) { // RBJ
    const w = 2 * Math.PI * f / sr, cs = Math.cos(w), al = Math.sin(w) / (2 * q); let b0, b1, b2;
    if (type === 'bp') { b0 = al; b1 = 0; b2 = -al; }
    else if (type === 'hp') { b0 = (1 + cs) / 2; b1 = -(1 + cs); b2 = (1 + cs) / 2; }
    else { b0 = (1 - cs) / 2; b1 = 1 - cs; b2 = (1 - cs) / 2; }
    const a0 = 1 + al; return { b0: b0 / a0, b1: b1 / a0, b2: b2 / a0, a1: -2 * cs / a0, a2: (1 - al) / a0 };
  }
  function filtra(x, c, vezes) { let y = x; for (let v = 0; v < (vezes || 1); v++) { const o = new Float32Array(y.length); let x1 = 0, x2 = 0, y1 = 0, y2 = 0;
      for (let i = 0; i < y.length; i++) { const s = y[i], r = c.b0 * s + c.b1 * x1 + c.b2 * x2 - c.a1 * y1 - c.a2 * y2; x2 = x1; x1 = s; y2 = y1; y1 = r; o[i] = r; } y = o; } return y; }
  const rms = a => { let s = 0; for (let i = 0; i < a.length; i++) s += a[i] * a[i]; return Math.sqrt(s / Math.max(1, a.length)); };
  function envelope(y, sr, atk, rel) { const ka = Math.exp(-1 / (atk * sr)), kr = Math.exp(-1 / (rel * sr)), e = new Float32Array(y.length); let v = 0;
    for (let i = 0; i < y.length; i++) { const a = Math.abs(y[i]); v = a > v ? ka * v + (1 - ka) * a : kr * v + (1 - kr) * a; e[i] = v; } return e; }

  function sussurroV1(x, sr, o) { // v1 (25/10, reprovada: chiado, pouco inteligível); fica para comparação
    o = o || {}; const nivel = o.nivel ?? 0.5, ar = o.ar ?? 0.12, rv = o.reverb ?? 0.22, cauda = o.cauda ?? 0.35, rand = rng(o.seed || 7070);
    const n = x.length + Math.round(cauda * sr), xin = new Float32Array(n); xin.set(x);
    const ruido = new Float32Array(n); for (let i = 0; i < n; i++) ruido[i] = rand() * 2 - 1;
    const NB = 18, f0 = 250, f1 = 9000, Q = 5.5, out = new Float32Array(n);
    for (let k = 0; k < NB; k++) {
      const fc = f0 * Math.pow(f1 / f0, k / (NB - 1)); if (fc > sr * 0.45) break;
      const c = biquad('bp', fc, Q, sr), mod = filtra(xin, c, 2), env = envelope(mod, sr, 0.004, 0.025), car = filtra(ruido, c, 2), cr = rms(car) || 1;
      const incl = fc < 500 ? 0.3 : fc < 1200 ? 0.7 : fc < 3000 ? 1.15 : 1.4; // sussurro: quase sem graves, agudos na frente
      for (let i = 0; i < n; i++) out[i] += car[i] / cr * env[i] * 1.25 * incl;
    }
    // ar / respiração: ruído agudo seguindo o envelope geral da fala
    const envG = envelope(xin, sr, 0.01, 0.06), arN = filtra(ruido.map((v, i) => ruido[(i * 7 + 13) % n]), biquad('hp', 2500, 0.7, sr), 1), ar0 = rms(arN) || 1, er = rms(envG) || 1;
    const ro = rms(out) || 1; for (let i = 0; i < n; i++) out[i] += arN[i] / ar0 * (envG[i] / er) * ro * ar;
    let y = filtra(out, biquad('hp', 320, 0.7, sr), 2);
    // reverb curto: reflexões iniciais + um pente com realimentação, abafado
    const wet = new Float32Array(n), ER = [[0.011, 0.36], [0.017, 0.28], [0.023, 0.22], [0.031, 0.16], [0.043, 0.11]];
    for (const [d, gn] of ER) { const D = Math.round(d * sr); for (let i = D; i < n; i++) wet[i] += y[i - D] * gn; }
    const D2 = Math.round(0.047 * sr); for (let i = D2; i < n; i++) wet[i] += wet[i - D2] * 0.42;
    const wl = filtra(wet, biquad('lp', 5000, 0.7, sr), 1); for (let i = 0; i < n; i++) y[i] = y[i] * (1 - rv * 0.5) + wl[i] * rv;
    // nível: RMS final = nivel x RMS da voz original (só nos trechos com som)
    const alvo = rms(x) * nivel, atual = rms(y.subarray(0, x.length)) || 1, g = alvo / atual; for (let i = 0; i < n; i++) y[i] *= g;
    const F = Math.round(0.01 * sr); for (let i = 0; i < F; i++) { y[i] *= i / F; y[n - 1 - i] *= i / F; } // sem estalo nas pontas
    return y;
  }

  // v2 (25/10): inteligível. Mistura voz original em passa-alta (~850 Hz, baixa) + vocoder de ruído de 28 bandas com envelope rápido (3/8 ms),
  // bandas de 1-4 kHz preservadas, ar bem baixo e sem chiado (tudo cortado acima de ~8 kHz), sopro de respiração antes da palavra, compressão leve e reverb curto.
  // Ruído modulado: modo 'lpc' (padrão; formantes de cada quadro sobre ruído, mais inteligível) ou 'banco' (28 filtros + seguidores de envelope).
  // opts: { modo = 'lpc', voz = 0.45 (parte da voz original), ruido = 0.55 (parte do ruído modulado), ar = 0.03, sopro = 0.35 s (0 = sem), reverb = 0.15, nivel = 0.55, cauda = 0.3, seed }
  // Retorna Float32Array; y.preRoll = amostras do sopro antes da palavra (para alinhar medições).
  function sussurro(x, sr, o) {
    o = o || {}; const wv = o.voz ?? 0.45, wn = o.ruido ?? 0.55, ar = o.ar ?? 0.03, sopro = o.sopro ?? 0.35, rv = o.reverb ?? 0.15, nivel = o.nivel ?? 0.55, cauda = o.cauda ?? 0.3, rand = rng(o.seed || 7070);
    const n = x.length + Math.round(cauda * sr), xin = new Float32Array(n); xin.set(x);
    const ruido = new Float32Array(n); for (let i = 0; i < n; i++) ruido[i] = rand() * 2 - 1;
    const NB = 28, f0 = 200, f1 = 7600, Q = 7; let voc = new Float32Array(n);
    if ((o.modo ?? 'lpc') === 'lpc') voc = lpcSussurro(xin, sr, rand); else for (let k = 0; k < NB; k++) {
      const fc = f0 * Math.pow(f1 / f0, k / (NB - 1)); if (fc > sr * 0.45) break;
      const c = biquad('bp', fc, Q, sr), env = envelope(filtra(xin, c, 2), sr, 0.003, 0.008), car = filtra(ruido, c, 2), cr = rms(car) || 1;
      const peso = fc < 500 ? 0.2 : fc < 900 ? 0.6 : fc <= 4200 ? 1.3 : 0.8; // 1-4 kHz (o "B" e o "ia") na frente
      for (let i = 0; i < n; i++) voc[i] += car[i] / cr * env[i] * 1.25 * peso;
    }
    const vh = filtra(xin, biquad('hp', 850, 0.7, sr), 2); // voz original sem os graves (sem altura tonal forte)
    const rV = rms(vh) || 1, rN = rms(voc) || 1, y = new Float32Array(n);
    for (let i = 0; i < n; i++) y[i] = wv * vh[i] / rV + wn * voc[i] / rN;
    const envG = envelope(xin, sr, 0.01, 0.06), er = rms(envG) || 1, arN = filtra(filtra(ruido.map((v, i) => ruido[(i * 7 + 13) % n]), biquad('hp', 2000, 0.7, sr), 1), biquad('lp', 6000, 0.7, sr), 1), a0 = rms(arN) || 1, ry = rms(y);
    for (let i = 0; i < n; i++) y[i] += arN[i] / a0 * (envG[i] / er) * ry * ar;
    let z = filtra(filtra(y, biquad('hp', 300, 0.7, sr), 1), biquad('lp', 8000, 0.7, sr), 2); // sem chiado acima de 8 kHz
    // compressão leve (RMS 10 ms, 3:1 acima de -12 dB do pico do envelope, ataque 5 ms, solta 80 ms)
    const ce = envelope(z, sr, 0.005, 0.08); let pkE = 0; for (let i = 0; i < n; i++) pkE = Math.max(pkE, ce[i]); const th = pkE * 0.25;
    for (let i = 0; i < n; i++) if (ce[i] > th) z[i] *= Math.pow(ce[i] / th, 1 / 3 - 1);
    // reverb curto
    const wet = new Float32Array(n), ER = [[0.009, 0.3], [0.015, 0.24], [0.022, 0.18], [0.03, 0.12]];
    for (const [d, gn] of ER) { const D = Math.round(d * sr); for (let i = D; i < n; i++) wet[i] += z[i - D] * gn; }
    const D2 = Math.round(0.041 * sr); for (let i = D2; i < n; i++) wet[i] += wet[i - D2] * 0.35;
    const wl = filtra(wet, biquad('lp', 4500, 0.7, sr), 1); for (let i = 0; i < n; i++) z[i] = z[i] * (1 - rv * 0.5) + wl[i] * rv;
    const alvo = rms(x) * nivel, g = alvo / (rms(z.subarray(0, x.length)) || 1); for (let i = 0; i < n; i++) z[i] *= g;
    const F = Math.round(0.01 * sr); for (let i = 0; i < F; i++) { z[i] *= i / F; z[n - 1 - i] *= i / F; }
    // sopro (inspiração curta) antes da palavra: ruído em 900-3000 Hz, sobe e cai, bem baixo
    const P = Math.round(sopro * sr), out = new Float32Array(P + n);
    if (P > 0) { const b = filtra(filtra(Float32Array.from({ length: P }, () => rand() * 2 - 1), biquad('bp', 1700, 0.9, sr), 2), biquad('lp', 5000, 0.7, sr), 1), rb = rms(b) || 1;
      for (let i = 0; i < P; i++) { const k = i / P, e = Math.sin(Math.PI * Math.min(1, k * 1.15)) ** 2; out[i] = b[i] / rb * e * alvo * 0.35; } }
    out.set(z, P); out.preRoll = P; return out;
  }
  // ruído com o envelope espectral (formantes) de cada quadro da voz: LPC ordem 40, quadros de 25 ms com 50% de sobreposição (Hann), excitação = ruído branco
  function lpcSussurro(x, sr, rand) {
    const N = Math.round(0.025 * sr), H = N >> 1, ORD = 40, n = x.length, out = new Float32Array(n + N), win = Float32Array.from({ length: N }, (_, i) => 0.5 - 0.5 * Math.cos(2 * Math.PI * i / N));
    const pe = new Float32Array(n); for (let i = 0; i < n; i++) pe[i] = x[i] - 0.9 * (i ? x[i - 1] : 0); // pré-ênfase
    const WU = 256, nz = new Float32Array(N + WU);
    for (let s0 = 0; s0 < n; s0 += H) {
      const fr = new Float32Array(N); for (let i = 0; i < N; i++) fr[i] = (pe[s0 + i] || 0) * win[i];
      const R = new Float64Array(ORD + 1); for (let k = 0; k <= ORD; k++) { let a = 0; for (let i = k; i < N; i++) a += fr[i] * fr[i - k]; R[k] = a * Math.exp(-0.5 * (2 * Math.PI * 60 * k / sr) ** 2); } // janela de lag (60 Hz)
      if (R[0] < 1e-9) continue; R[0] *= 1.0001;
      const A = new Float64Array(ORD + 1); A[0] = 1; let E = R[0];
      for (let i = 1; i <= ORD; i++) { let acc = R[i]; for (let j = 1; j < i; j++) acc += A[j] * R[i - j]; const k = -acc / E, T = A.slice(); for (let j = 1; j < i; j++) A[j] = T[j] + k * T[i - j]; A[i] = k; E *= (1 - k * k); if (E <= 0) break; }
      const gain = Math.sqrt(Math.max(E, 0) / N) * 1.6; for (let i = 0; i < nz.length; i++) nz[i] = rand() * 2 - 1;
      const y = new Float64Array(N + WU); for (let i = 0; i < N + WU; i++) { let v = nz[i] * gain; for (let j = 1; j <= ORD && j <= i; j++) v -= A[j] * y[i - j]; y[i] = v; }
      for (let i = 0; i < N; i++) out[s0 + i] += y[i + WU] * win[i];
    }
    let p = 0; for (let i = 0; i < n; i++) { p = out[i] + 0.5 * p; out[i] = p; } // de-ênfase parcial (sussurro fica mais claro que a voz)
    return out.subarray(0, n);
  }
  // inteligibilidade objetiva (bandas de 1-4 kHz): correlação do envelope (100 Hz) da voz original com o do resultado, e contraste do envelope (dB entre os 30% mais fortes e os 30% mais fracos quadros com fala) no resultado
  function inteligibilidade(x, y, sr, off) {
    off = off || 0; const bandas = [1000, 1260, 1590, 2000, 2520, 3170, 4000], hop = Math.round(sr / 100), res = [];
    for (const fc of bandas) { const c = biquad('bp', fc, 4.3, sr), ex = envelope(filtra(x, c, 2), sr, 0.003, 0.012), ey = envelope(filtra(y.subarray(off, off + x.length), c, 2), sr, 0.003, 0.012);
      const A = [], B = []; for (let i = 0; i + hop <= x.length; i += hop) { A.push(ex[i]); B.push(ey[i]); }
      const ma = A.reduce((s, v) => s + v, 0) / A.length, mb = B.reduce((s, v) => s + v, 0) / B.length; let sab = 0, saa = 0, sbb = 0; for (let i = 0; i < A.length; i++) { sab += (A[i] - ma) * (B[i] - mb); saa += (A[i] - ma) ** 2; sbb += (B[i] - mb) ** 2; }
      const fala = A.map((v, i) => [v, B[i]]).filter(p => p[0] > ma * 0.3).map(p => p[1]).sort((p, q) => p - q), k = Math.max(1, Math.floor(fala.length * 0.3)), lo = fala.slice(0, k), hi = fala.slice(-k), mm = a => a.reduce((s, v) => s + v, 0) / a.length;
      res.push({ fc, corr: +(sab / Math.sqrt(saa * sbb + 1e-20)).toFixed(2), contrasteDb: +(20 * Math.log10(mm(hi) / Math.max(mm(lo), 1e-9))).toFixed(1) }); }
    const media = k => +(res.reduce((s, r) => s + r[k], 0) / res.length).toFixed(2);
    // fidelidade espectral (formantes = a vogal): por quadro de 20 ms com fala, correlação entre os espectros em dB (1/6 de oitava, 300-5000 Hz) da original e do resultado
    const fcs = []; for (let f = 300; f <= 5000; f *= Math.pow(2, 1 / 6)) fcs.push(f);
    const yy = y.subarray(off, off + x.length), Wq = Math.round(0.02 * sr), Ex = [], Ey = [];
    for (const f of fcs) { const c = biquad('bp', f, 8.6, sr), bx = filtra(x, c, 2), by = filtra(yy, c, 2), ax = [], ay = [];
      for (let s0 = 0; s0 + Wq <= x.length; s0 += Wq) { let e1 = 0, e2 = 0; for (let i = s0; i < s0 + Wq; i++) { e1 += bx[i] * bx[i]; e2 += (by[i] || 0) ** 2; } ax.push(10 * Math.log10(e1 + 1e-12)); ay.push(10 * Math.log10(e2 + 1e-12)); } Ex.push(ax); Ey.push(ay); }
    const nq = Ex[0].length, tot = []; for (let q = 0; q < nq; q++) tot.push(Math.max(...Ex.map(b => b[q]))); const mx = Math.max(...tot); let sc = 0, nc = 0;
    for (let q = 0; q < nq; q++) { if (tot[q] < mx - 25) continue; const A = Ex.map(b => b[q]), B = Ey.map(b => b[q]), ma = A.reduce((s, v) => s + v, 0) / A.length, mb = B.reduce((s, v) => s + v, 0) / B.length; let ab = 0, aa = 0, bb = 0;
      for (let i = 0; i < A.length; i++) { ab += (A[i] - ma) * (B[i] - mb); aa += (A[i] - ma) ** 2; bb += (B[i] - mb) ** 2; } sc += ab / Math.sqrt(aa * bb + 1e-12); nc++; }
    const hi6 = filtra(yy, biquad('hp', 6000, 0.7, sr), 2), chiado = (rms(hi6) / (rms(yy) || 1)) ** 2;
    return { corrMedia: media('corr'), contrasteMedioDb: media('contrasteDb'), espectral: +(sc / Math.max(1, nc)).toFixed(2), chiado6k: +chiado.toFixed(3), bandas: res };
  }

  function medir(x, sr) {
    let pk = 0; for (let i = 0; i < x.length; i++) pk = Math.max(pk, Math.abs(x[i]));
    const hi = filtra(x, biquad('hp', 2000, 0.7, sr), 2), r = rms(x), db = v => v > 0 ? 20 * Math.log10(v) : -Infinity;
    const W = Math.round(0.04 * sr), L0 = Math.floor(sr / 400), L1 = Math.ceil(sr / 80), lim = r * 0.5; let soma = 0, nf = 0;
    for (let s = 0; s + W + L1 < x.length; s += W) { let e = 0; for (let i = 0; i < W; i++) e += x[s + i] * x[s + i]; if (Math.sqrt(e / W) < lim) continue;
      let best = 0; for (let L = L0; L <= L1; L += 2) { let c = 0, e2 = 0; for (let i = 0; i < W; i++) { c += x[s + i] * x[s + i + L]; e2 += x[s + i + L] * x[s + i + L]; } best = Math.max(best, c / Math.sqrt(e * e2 + 1e-12)); }
      soma += best; nf++; }
    return { rmsDb: +db(r).toFixed(1), picoDb: +db(pk).toFixed(1), tonal: +(nf ? soma / nf : 0).toFixed(2), agudos: +((rms(hi) / (r || 1)) ** 2).toFixed(2) };
  }
  root.VozFx = { sussurro, sussurroV1, medir, inteligibilidade };
  if (typeof module !== 'undefined' && module.exports) module.exports = root.VozFx;
})(typeof window !== 'undefined' ? window : globalThis);
