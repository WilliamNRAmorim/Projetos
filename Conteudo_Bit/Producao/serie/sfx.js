/* sfx.js - efeitos sonoros e música SINTETIZADOS (Web Audio) para "Plantão Noturno".
 * Sem arquivos externos, sem licença. Módulo autônomo: <script src="sfx.js"></script> -> window.Sfx
 * (ou require('./sfx.js') com um polyfill de Web Audio). Veja SFX_README.md.
 *
 * Uso:  const s = Sfx.create(audioCtx, audioCtx.destination);
 *       s.chuva(t, 30, {zinco:true});  s.stinger(t+10, 1);  // t em segundos do contexto
 * Todos os métodos retornam {t, fim} (início e fim, em segundos do contexto).
 * Opções comuns: vol (multiplicador, padrão 1).
 * silencioDuck mexe na automação da "cama": chame os ducks em ordem cronológica.
 */
(function (root) {
  'use strict';

  // Nível-alvo de pico (dBFS) de cada som quando tocado sozinho. CAL calibrado por medição offline.
  const ALVO_DB = {
    drone: -15, pulso: -15, tiquetaque: -15, tiquetaquePara: -12, stinger: -6, chuva: -15,
    campainha: -12, passosChinelo: -14, cantarolar: -16, batidas: -12, celularToque: -14,
    zumbidoLuz: -16, papelRasgando: -14, passaros: -17, vento: -16, caixinha: -15,
    pianoBia: -15, acordeBia: -15, batimento: -14
  };
  // Ganho de calibração (preenchido pela medição; ver SFX_README.md).
  const CAL = {
    drone: 0.172,
    pulso: 0.188,
    tiquetaque: 0.135,
    stinger: 0.302,
    chuva: 0.339,
    campainha: 0.136,
    passosChinelo: 0.441,
    cantarolar: 0.389,
    batidas: 0.194,
    celularToque: 0.393,
    zumbidoLuz: 0.105,
    papelRasgando: 0.136,
    passaros: 0.266,
    vento: 0.676,
    caixinha: 0.301,
    pianoBia: 0.302,
    acordeBia: 0.149,
    batimento: 0.188,
    tiquetaquePara: 0.176
  };

  // Argumentos posicionais de cada método (também usados pelo formato de cue-sheet: params é um objeto).
  const POS = {
    drone: ['dur'], pulso: ['dur', 'bpm'], tiquetaque: ['dur'], tiquetaquePara: [], stinger: ['intensidade'],
    chuva: ['dur'], campainha: [], passosChinelo: ['n'], cantarolar: ['dur'], batidas: ['n', 'espacamento'],
    celularToque: ['abafado'], zumbidoLuz: ['dur'], papelRasgando: [], passaros: ['dur'], vento: ['dur'],
    caixinha: ['dur'], pianoBia: ['notas'], acordeBia: [], batimento: ['dur', 'bpm'], silencioDuck: ['dur']
  };

  function mulberry32(a) {
    return function () {
      a |= 0; a = a + 0x6D2B79F5 | 0;
      let t = Math.imul(a ^ a >>> 15, 1 | a);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }
  const mtof = (m) => 440 * Math.pow(2, (m - 69) / 12);
  const NOTAS = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 };
  function midi(n) {
    if (typeof n === 'number') return n;
    const m = /^([A-Ga-g])([#b]?)(-?\d)$/.exec(String(n));
    if (!m) return 57;
    return NOTAS[m[1].toUpperCase()] + (m[2] === '#' ? 1 : m[2] === 'b' ? -1 : 0) + (parseInt(m[3], 10) + 1) * 12;
  }
  const isObj = (x) => x && typeof x === 'object' && !Array.isArray(x);

  function create(ctx, dest, opts) {
    opts = opts || {};
    const sr = ctx.sampleRate;
    const rng = mulberry32(opts.seed || 20261025);
    const rnd = (a, b) => a + (b - a) * rng();

    const cama = ctx.createGain();   // barramento da "cama" (duckável)
    cama.gain.value = 1;
    cama.connect(dest);

    // buffers de ruído branco e rosa (determinísticos)
    const len = Math.floor(sr * 3);
    const WB = ctx.createBuffer(1, len, sr), NB = ctx.createBuffer(1, len, sr);
    {
      const w = WB.getChannelData(0), d = NB.getChannelData(0);
      let b0 = 0, b1 = 0, b2 = 0, b3 = 0, b4 = 0, b5 = 0, b6 = 0;
      for (let i = 0; i < len; i++) {
        const x = rng() * 2 - 1; w[i] = x;
        b0 = 0.99886 * b0 + x * 0.0555179; b1 = 0.99332 * b1 + x * 0.0750759;
        b2 = 0.96900 * b2 + x * 0.1538520; b3 = 0.86650 * b3 + x * 0.3104856;
        b4 = 0.55000 * b4 + x * 0.5329522; b5 = -0.7616 * b5 - x * 0.0168980;
        d[i] = (b0 + b1 + b2 + b3 + b4 + b5 + b6 + x * 0.5362) * 0.11; b6 = x * 0.115926;
      }
    }

    const G = (v) => { const g = ctx.createGain(); g.gain.value = v; return g; };
    const F = (type, f, q) => { const n = ctx.createBiquadFilter(); n.type = type; n.frequency.value = f; if (q != null) n.Q.value = q; return n; };
    function O(type, f, t0, t1) { const o = ctx.createOscillator(); o.type = type; o.frequency.value = f; o.start(t0); o.stop(t1); return o; }
    function N(t0, t1, pink) { const s = ctx.createBufferSource(); s.buffer = pink ? NB : WB; s.loop = true; s.start(t0, rng() * 1.5); s.stop(t1); return s; }
    function C() { const a = arguments; for (let i = 0; i < a.length - 1; i++) a[i].connect(a[i + 1]); return a[a.length - 1]; }

    // envelope: ataque curto, decaimento exponencial, fecha em zero (sem estalo). Retorna o fim.
    function dec(p, t, a, peak, ln) {
      a = Math.max(a, 0.004); peak = Math.max(peak, 1e-5);
      p.setValueAtTime(0, t); p.linearRampToValueAtTime(peak, t + a);
      p.exponentialRampToValueAtTime(peak * 0.001, t + a + ln);
      p.linearRampToValueAtTime(0, t + a + ln + 0.03);
      return t + a + ln + 0.03;
    }
    // envelope trapezoidal (fade in / sustenta / fade out)
    function trap(p, t, dur, a, r, peak) {
      a = Math.max(0.01, Math.min(a, dur / 2)); r = Math.max(0.01, Math.min(r, dur / 2));
      p.setValueAtTime(0, t); p.linearRampToValueAtTime(peak, t + a);
      p.setValueAtTime(peak, Math.max(t + a, t + dur - r)); p.linearRampToValueAtTime(0, t + dur);
    }
    function glide(p, f0, f1, t0, t1) { p.setValueAtTime(f0, t0); p.exponentialRampToValueAtTime(f1, t1); }
    function eco(inp, out, delay, fb, lp, wet) {
      const d = ctx.createDelay(1); d.delayTime.value = delay;
      const f = G(fb), l = F('lowpass', lp), w = G(wet);
      inp.connect(d); d.connect(l); l.connect(f); f.connect(d); l.connect(w); w.connect(out);
    }
    const lvl = (tipo, p) => (CAL[tipo] || 1) * (p.vol == null ? 1 : p.vol);
    const bus = (g, usaCama) => g.connect(usaCama ? cama : dest);

    const defs = {};

    defs.drone = function (t, p) {
      const dur = p.dur || 8, f0 = p.tomInicial || 55, sub = p.subida == null ? 3 : p.subida, T = t + dur;
      const f1 = f0 * Math.pow(2, sub / 12);
      const out = G(0); trap(out.gain, t, dur, Math.min(2, dur * 0.3), Math.min(2.5, dur * 0.35), lvl('drone', p));
      const lp = F('lowpass', 220, 0.7), mix = G(0.5);
      [['sawtooth', 1, 0.5], ['sawtooth', 1.006, 0.4], ['sine', 0.5, 0.8], ['sine', 1, 0.6]].forEach(function (c) {
        const o = O(c[0], f0 * c[1], t, T); glide(o.frequency, f0 * c[1], f1 * c[1], t, T);
        C(o, G(c[2]), mix);
      });
      C(mix, lp, out); bus(out, true);
      return { t: t, fim: T };
    };

    defs.pulso = function (t, p) {
      const dur = p.dur || 8, bpm = p.bpm || 60, per = 60 / bpm, T = t + dur;
      const out = G(lvl('pulso', p)); let fim = t;
      for (let b = 0; t + b * per < T - 0.05; b++) {
        const s = t + b * per, o = O('sine', 90, s, s + 0.5), g = G(0);
        glide(o.frequency, 90, 38, s, s + 0.14);
        fim = dec(g.gain, s, 0.006, 1, 0.3);
        C(o, g, out);
      }
      bus(out, true);
      return { t: t, fim: fim };
    };

    defs.batimento = function (t, p) {
      const dur = p.dur || 8, bpm = p.bpm || 70, per = 60 / bpm, T = t + dur;
      const out = G(lvl('batimento', p)), lp = F('lowpass', 160, 0.7); lp.connect(out); let fim = t;
      for (let b = 0; t + b * per < T - 0.05; b++) {
        [[0, 1, 62], [0.28 * per + 0.02, 0.65, 52]].forEach(function (h) {
          const s = t + b * per + h[0], o = O('sine', h[2], s, s + 0.4), g = G(0);
          glide(o.frequency, h[2], h[2] * 0.62, s, s + 0.16);
          fim = Math.max(fim, dec(g.gain, s, 0.012, h[1], 0.2));
          C(o, g, lp);
        });
      }
      bus(out, true);
      return { t: t, fim: fim };
    };

    function tick(s, tac, forca, lpf, out) {
      const f = tac ? 1250 : 1700, ln = 0.05;
      const n = N(s, s + 0.2), bp = F('bandpass', f * 1.4, 3), gn = G(0), lp = F('lowpass', lpf, 0.5);
      dec(gn.gain, s, 0.002, 0.7 * forca, 0.03); C(n, bp, gn, lp, out);
      const o = O('sine', f * 0.55, s, s + 0.3), go = G(0);
      dec(go.gain, s, 0.002, 0.6 * forca, ln); C(o, go, lp);
      const o2 = O('sine', tac ? 120 : 150, s, s + 0.4), g2 = G(0);
      dec(g2.gain, s, 0.003, 0.7 * forca, 0.1); C(o2, g2, out);
    }
    defs.tiquetaque = function (t, p) {
      const dur = p.dur || 10, len0 = p.lentidao || 0, iv0 = p.intervalo || p.param || 1, T = t + dur;
      const out = G(lvl('tiquetaque', p)); let i = 0, s = t, fim = t;
      while (s < T - 0.1) {
        const pr = (s - t) / dur;
        tick(s, i % 2 === 1, 1 - 0.4 * len0 * pr, 4500 * (1 - 0.8 * len0 * pr), out);
        fim = s + 0.35; s += iv0 * (1 + len0 * 2 * pr); i++;
      }
      bus(out, true);
      return { t: t, fim: fim };
    };

    defs.tiquetaquePara = function (t, p) {
      const out = G(lvl('tiquetaquePara', p));
      tick(t, true, 1.2, 2200, out);
      const o = O('sine', 70, t, t + 0.6), g = G(0); dec(g.gain, t, 0.005, 0.5, 0.25); C(o, g, out);
      bus(out, false);
      const sil = p.silencio == null ? 2.5 : p.silencio;
      if (sil > 0) defs.silencioDuck(t + 0.08, { dur: sil });
      return { t: t, fim: t + 0.6 + sil };
    };

    defs.stinger = function (t, p) {
      const it = Math.max(0, Math.min(1.2, p.intensidade == null ? 1 : p.intensidade));
      const out = G(lvl('stinger', p) * (0.35 + 0.65 * Math.min(1, it)));
      const wet = G(1);
      // ruído descendo
      const n = N(t, t + 1.5), bp = F('bandpass', 6000, 1.2), gn = G(0);
      glide(bp.frequency, 6000, 400, t, t + 0.7); dec(gn.gain, t, 0.004, 0.9, 0.6); C(n, bp, gn, wet);
      // aglomerado dissonante
      const lp = F('lowpass', 1800, 0.7), gc = G(0); const fim = dec(gc.gain, t, 0.006, 0.7, 2.2);
      [196, 207.7, 277.2, 293.7, 415.3].forEach(function (f, k) {
        const o = O('sawtooth', f, t, fim + 0.1); o.detune.value = (k - 2) * 7; C(o, G(0.25), lp);
      });
      C(lp, gc, wet);
      // sub
      const so = O('sine', 62, t, t + 1.6), gs = G(0); glide(so.frequency, 62, 34, t, t + 0.5); dec(gs.gain, t, 0.004, 1, 1.0); C(so, gs, wet);
      wet.connect(out); eco(wet, out, 0.19, 0.35, 2500, 0.45);
      bus(out, false);
      return { t: t, fim: fim + 1.2 };
    };

    defs.chuva = function (t, p) {
      const dur = p.dur || 20, T = t + dur, zinco = !!p.zinco;
      const out = G(0);
      trap(out.gain, t, dur, 1.5, p.corte ? 0.04 : 1.5, lvl('chuva', p));
      const n = N(t, T, true), n2 = N(t, T);
      if (zinco) {
        const hp = F('highpass', 600), bp = F('bandpass', 3200, 0.6), g1 = G(0.55), g2 = G(0.25), lp = F('lowpass', 7000);
        C(n, hp, lp, g1, out); C(n2, bp, g2, out);
        const k = Math.floor(dur * 16);
        for (let i = 0; i < k; i++) {
          const s = t + rnd(0.1, dur - 0.15), o = O('sine', rnd(2400, 5200), s, s + 0.1), g = G(0);
          dec(g.gain, s, 0.002, rnd(0.04, 0.16), 0.03); C(o, g, out);
        }
      } else {
        C(n, F('highpass', 300), F('lowpass', 1800), G(0.9), out);
        C(n2, F('bandpass', 900, 0.5), G(0.12), out);
      }
      bus(out, true);
      return { t: t, fim: T };
    };

    defs.campainha = function (t, p) {
      const out = G(lvl('campainha', p)), mix = G(1);
      const R = [1, 2.32, 4.25, 6.63], A = [1, 0.5, 0.3, 0.15], L = [1.8, 1.2, 0.8, 0.5]; let fim = t;
      R.forEach(function (r, k) {
        const o = O('sine', 2090 * r, t, t + 2.2), g = G(0); fim = Math.max(fim, dec(g.gain, t, 0.002, A[k], L[k])); C(o, g, mix);
      });
      const n = N(t, t + 0.1), bp = F('bandpass', 5000, 1), gn = G(0); dec(gn.gain, t, 0.001, 0.4, 0.01); C(n, bp, gn, mix);
      mix.connect(out); eco(mix, out, 0.13, 0.32, 3500, 0.5);
      bus(out, false);
      return { t: t, fim: fim + 1.0 };
    };

    defs.passosChinelo = function (t, p) {
      const n = p.n || 4, passo = p.passo || 0.75, out = G(lvl('passosChinelo', p)); let fim = t;
      for (let i = 0; i < n; i++) {
        const s = t + i * passo * (1 + rnd(-0.08, 0.08)), f = rnd(0.85, 1.15);
        const a = N(s, s + 0.4, true), lp = F('lowpass', 700 * f, 0.6), g = G(0);
        fim = Math.max(fim, dec(g.gain, s, 0.05, 0.7, 0.16)); C(a, lp, g, out);
        const s2 = s + 0.15, b = N(s2, s2 + 0.2), bp = F('bandpass', 420 * f, 1), g2 = G(0);
        dec(g2.gain, s2, 0.003, 0.9, 0.05); C(b, bp, g2, out);
        const o = O('sine', 110 * f, s2, s2 + 0.2), g3 = G(0); dec(g3.gain, s2, 0.003, 0.35, 0.08); C(o, g3, out);
      }
      bus(out, false);
      return { t: t, fim: fim };
    };

    defs.cantarolar = function (t, p) {
      const dur = p.dur || 6, T = t + dur, step = 1.1;
      const out = G(0); trap(out.gain, t, dur, 0.8, 1, lvl('cantarolar', p));
      const o = O('sawtooth', 220, t, T), lfo = O('sine', 5, t, T), lg = G(5), vib = G(0);
      lfo.connect(lg); lg.connect(o.frequency);
      const amp = G(0); const seq = [0, 3, 2, 0, -2, 0, 3, 5, 3, 2, 0, -2]; // A menor em torno de A3
      for (let i = 0; t + i * step < T; i++) {
        const s = t + i * step, f = 220 * Math.pow(2, seq[i % seq.length] / 12);
        if (i === 0) o.frequency.setValueAtTime(f, s); else { o.frequency.setValueAtTime(220 * Math.pow(2, seq[(i - 1) % seq.length] / 12), s); o.frequency.linearRampToValueAtTime(f, s + 0.15); }
        amp.gain.setValueAtTime(0.35, s); amp.gain.linearRampToValueAtTime(1, s + 0.2); amp.gain.linearRampToValueAtTime(0.35, s + step - 0.05);
      }
      const f1 = F('bandpass', 300, 4), f2 = F('bandpass', 1500, 6), lp = F('lowpass', 2200), m = G(1), g1 = G(1), g2 = G(0.25);
      o.connect(amp); amp.connect(f1); amp.connect(f2); f1.connect(g1); f2.connect(g2); g1.connect(lp); g2.connect(lp); lp.connect(out);
      const br = N(t, T), bf = F('bandpass', 1800, 1), bg = G(0.01); C(br, bf, bg, out);
      bus(out, false);
      return { t: t, fim: T };
    };

    defs.batidas = function (t, p) {
      const n = p.n || 3, esp = p.espacamento || 1.5, out = G(0), mix = G(lvl('batidas', p)); let fim = t;
      out.gain.value = 1;
      for (let i = 0; i < n; i++) {
        const s = t + i * esp, f = rnd(0.95, 1.05);
        const a = N(s, s + 0.3), lp = F('lowpass', 900, 0.7), g = G(0); dec(g.gain, s, 0.002, 0.6, 0.07); C(a, lp, g, out);
        const o = O('sine', 150 * f, s, s + 0.5), g2 = G(0); glide(o.frequency, 150 * f, 95, s, s + 0.2); fim = Math.max(fim, dec(g2.gain, s, 0.002, 1, 0.22)); C(o, g2, out);
        const o2 = O('sine', 310 * f, s, s + 0.3), g3 = G(0); dec(g3.gain, s, 0.002, 0.35, 0.09); C(o2, g3, out);
      }
      out.connect(mix); eco(out, mix, 0.11, 0.3, 1500, 0.4);
      bus(mix, false);
      return { t: t, fim: fim + 0.8 };
    };

    defs.celularToque = function (t, p) {
      const ab = p.abafado == null ? true : !!p.abafado, out = G(lvl('celularToque', p));
      const lp = F('lowpass', ab ? 650 : 5000, 0.7), mix = G(1); C(lp, mix, out);
      if (ab) { const r = F('peaking', 260, 2); r.gain.value = 6; C(lp, r, out); }
      let s = t, fim = t;
      for (let rep = 0; rep < 2; rep++) {
        for (let b = 0; b < 4; b++) {
          const f = (b % 2 ? 1318.5 : 1046.5), o = O('square', f, s, s + 0.15), g = G(0);
          trap(g.gain, s, 0.11, 0.008, 0.03, 0.5); C(o, g, lp); fim = s + 0.11; s += 0.18;
        }
        s += 0.5;
      }
      bus(out, false);
      return { t: t, fim: fim };
    };

    defs.zumbidoLuz = function (t, p) {
      const dur = p.dur || 6, T = t + dur, out = G(0);
      trap(out.gain, t, dur, 0.05, 0.2, lvl('zumbidoLuz', p));
      const fl = G(1);
      const o = O('sawtooth', 120, t, T), o2 = O('sawtooth', 240.6, t, T), lp = F('lowpass', 1400, 0.8), g2 = G(0.4);
      C(o, lp); C(o2, g2, lp); C(lp, fl, out);
      fl.gain.setValueAtTime(1, t);
      for (let s = t; s < T; s += rnd(0.05, 0.12)) fl.gain.linearRampToValueAtTime(rnd(0.7, 1), s + 0.02);
      // estalo no início
      const n = N(t, t + 0.1), hp = F('highpass', 1500), gn = G(0); dec(gn.gain, t, 0.001, 1.6, 0.012); C(n, hp, gn, out);
      bus(out, true);
      return { t: t, fim: T };
    };

    defs.papelRasgando = function (t, p) {
      const dur = 0.9, out = G(lvl('papelRasgando', p)), g = G(0);
      const n = N(t, t + dur + 0.1), hp = F('highpass', 1800), bp = F('peaking', 4500, 1); bp.gain.value = 4;
      C(n, hp, bp, g, out);
      const n2 = N(t, t + dur + 0.1), lp = F('lowpass', 600), g2 = G(0.15); C(n2, lp, g2, out);
      g.gain.setValueAtTime(0, t);
      for (let s = t; s < t + dur; s += 0.018) {
        const x = (s - t) / dur, env = Math.sin(Math.PI * Math.pow(x, 0.7));
        g.gain.linearRampToValueAtTime(Math.max(0, env * rnd(0.15, 1)), s + 0.018);
      }
      g.gain.linearRampToValueAtTime(0, t + dur + 0.05);
      bus(out, false);
      return { t: t, fim: t + dur + 0.05 };
    };

    defs.passaros = function (t, p) {
      const dur = p.dur || 8, T = t + dur, out = G(lvl('passaros', p));
      const k = Math.floor(dur * 1.2);
      for (let i = 0; i < k; i++) {
        const s0 = t + rnd(0.2, dur - 0.8), ns = 1 + Math.floor(rng() * 3), base = rnd(2800, 4800);
        for (let j = 0; j < ns; j++) {
          const s = s0 + j * 0.17, d = rnd(0.07, 0.14), o = O('sine', base, s, s + d + 0.05), g = G(0);
          glide(o.frequency, base * rnd(0.8, 1.0), base * rnd(1.1, 1.5), s, s + d);
          trap(g.gain, s, d, 0.02, 0.04, rnd(0.2, 0.5)); C(o, g, out);
        }
      }
      const fade = G(0); trap(fade.gain, t, dur, 0.8, 1, 1); out.connect(fade); bus(fade, true);
      return { t: t, fim: T };
    };

    defs.vento = function (t, p) {
      const dur = p.dur || 8, T = t + dur, out = G(0);
      trap(out.gain, t, dur, 2, 2, lvl('vento', p));
      const n = N(t, T, true), bp = F('bandpass', 500, 0.8), lv = G(0.7);
      C(n, bp, lv, out);
      bp.frequency.setValueAtTime(500, t); lv.gain.setValueAtTime(0.5, t);
      for (let s = t + 1.2; s < T; s += rnd(1, 2)) {
        bp.frequency.linearRampToValueAtTime(rnd(300, 900), s); lv.gain.linearRampToValueAtTime(rnd(0.3, 1), s);
      }
      bus(out, true);
      return { t: t, fim: T };
    };

    defs.caixinha = function (t, p) {
      const dur = p.dur || 8, T = t + dur, step = 0.38 * (p.lenta ? 1.7 : 1);
      const MEL = [69, 72, 76, 74, 72, 71, 69, 72, 69, 68, 71, 68, 69, null];
      const out = G(lvl('caixinha', p)), mix = G(1); mix.connect(out); eco(mix, out, 0.17, 0.3, 4000, 0.35);
      const master = G(0); trap(master.gain, t, dur, 0.05, Math.min(0.6, dur / 3), 1); // não deixa cortar seco
      if (p.afasta) { // se afastando: volume cai até ~-18 dB e o som abafa ao longo de dur
        const lp = F('lowpass', 5000, 0.5), ga = G(1); glide(lp.frequency, 5000, 700, t, T); ga.gain.setValueAtTime(1, t); ga.gain.linearRampToValueAtTime(0.12, T);
        out.connect(lp); lp.connect(ga); ga.connect(master);
      } else out.connect(master);
      let i = 0;
      for (let s = t; s < T - 0.35; s += step, i++) {
        let m = MEL[i % MEL.length]; if (m == null) continue; if (p.tom) m += p.tom; // p.tom: transpõe em semitons (ep07: caixinha meio tom errada)
        let cents = 0;
        if (p.desafinada) { cents = -18 + rnd(-30, 30); if (i % 4 === 3) cents += rnd(-60, 60); }
        const ln = Math.min(1.1, step * 2.2);
        [[1, 1, 1.0], [2.01, 0.18, 0.5], [5.4, 0.1, 0.22]].forEach(function (h) {
          const o = O('sine', mtof(m) * h[0], s, s + ln * h[2] + 0.4), g = G(0); o.detune.value = cents;
          if (p.reversa) {
            const e = ln * h[2] * 0.85; g.gain.setValueAtTime(0, s); g.gain.linearRampToValueAtTime(0.3 * h[1], s + e); g.gain.linearRampToValueAtTime(0, s + e + 0.04);
          } else dec(g.gain, s, 0.003, 0.3 * h[1], ln * h[2]);
          C(o, g, mix);
        });
      }
      bus(master, true);
      return { t: t, fim: T + 0.5 };
    };

    defs.pianoBia = function (t, p) {
      const notas = p.notas && p.notas.length ? p.notas : [57], passo = p.passo || 1.2;
      const out = G(lvl('pianoBia', p)), lp = F('lowpass', 3500, 0.5), mix = G(1); C(lp, mix, out); eco(mix, out, 0.21, 0.28, 2800, 0.3);
      let fim = t;
      notas.forEach(function (nt, i) {
        const s = t + i * passo, ac = Array.isArray(nt) ? nt : [nt];
        ac.forEach(function (x) {
          const f = mtof(midi(x));
          [[1, 1, 2.4], [2, 0.35, 1.5], [3, 0.15, 1.0], [4, 0.06, 0.6]].forEach(function (h) {
            if (f * h[0] > 9000) return;
            const o = O('sine', f * h[0], s, s + h[2] + 0.3), g = G(0); fim = Math.max(fim, dec(g.gain, s, 0.007, 0.5 * h[1] / ac.length, h[2])); C(o, g, lp);
          });
        });
      });
      bus(out, false);
      return { t: t, fim: fim + 0.8 };
    };

    defs.acordeBia = function (t, p) {
      const dur = p.dur || 3.2, T = t + dur, out = G(0), lp = F('lowpass', 1800, 0.5);
      trap(out.gain, t, dur, 0.6, 1.6, lvl('acordeBia', p)); C(lp, out);
      (p.notas || [45, 52, 57, 60, 64]).forEach(function (m, k) { // p.notas: acorde alternativo em MIDI (ep07: tom maior)
        const f = mtof(m);
        [['sine', 1, 0.5], ['triangle', 1.004, 0.3]].forEach(function (c) { C(O(c[0], f * c[1], t, T), G(c[2] / 2), lp); });
      });
      bus(out, false);
      return { t: t, fim: T };
    };

    defs.silencioDuck = function (t, p) {
      const dur = p.dur || 2, nivel = p.nivel == null ? 0.03 : p.nivel, g = cama.gain;
      g.setValueAtTime(1, t); g.linearRampToValueAtTime(nivel, t + 0.12);
      g.setValueAtTime(nivel, t + dur); g.linearRampToValueAtTime(1, t + dur + 0.6);
      return { t: t, fim: t + dur + 0.6 };
    };

    // API pública: métodos posicionais + tocar(tipo, t, params)
    const api = { ctx: ctx, cama: cama, TIPOS: Object.keys(POS) };
    Object.keys(POS).forEach(function (tipo) {
      api[tipo] = function (t) {
        const p = {};
        for (let i = 1; i < arguments.length; i++) {
          const a = arguments[i];
          if (isObj(a)) Object.assign(p, a); else if (i - 1 < POS[tipo].length && a !== undefined) p[POS[tipo][i - 1]] = a;
        }
        return defs[tipo](t, p);
      };
    });
    api.tocar = function (tipo, t, params) {
      if (!defs[tipo]) throw new Error('Sfx: tipo desconhecido: ' + tipo);
      return defs[tipo](t, params || {});
    };
    return api;
  }

  // ---- cue-sheet ----
  // { versao:1, episodio:"ep01", cues:[ {cena:3, offset:0.5, tipo:"chuva", params:{dur:30, zinco:true}} ] }
  // inicios: {cena: segundosDoInicioDaCena} ou function(cena). Devolve [{t, tipo, params}] ordenado.
  function resolverFolha(folha, inicios, t0) {
    t0 = t0 || 0;
    const ini = typeof inicios === 'function' ? inicios : function (c) { return (inicios || {})[c] || 0; };
    return (folha.cues || []).map(function (c) {
      return { t: t0 + ini(c.cena) + (c.offset || 0), tipo: c.tipo, params: c.params || {} };
    }).sort(function (a, b) { return a.t - b.t; });
  }
  function agendar(inst, cues, t0) {
    t0 = t0 || 0;
    cues.slice().sort(function (a, b) { return a.t - b.t; }).forEach(function (c) { inst.tocar(c.tipo, t0 + c.t, c.params); });
  }

  // cues: [{t, tipo, params}] (ou uma cue-sheet + opts.inicios). Devolve Promise<AudioBuffer>.
  function renderOffline(cues, duracao, o) {
    o = o || {};
    if (cues && !Array.isArray(cues) && cues.cues) cues = resolverFolha(cues, o.inicios);
    const sr = o.sampleRate || 44100, OAC = root.OfflineAudioContext || root.webkitOfflineAudioContext;
    const ctx = new OAC(2, Math.ceil(duracao * sr), sr);
    const master = ctx.createGain(); master.connect(ctx.destination);
    agendar(create(ctx, master, { seed: o.seed }), cues);
    return ctx.startRendering();
  }

  // ---- análise e WAV ----
  function analisar(buf) {
    let pico = 0, soma = 0, n = 0, nan = 0, clip = 0, salto = 0;
    const bordas = { ini: 0, fim: 0 };
    for (let c = 0; c < buf.numberOfChannels; c++) {
      const d = buf.getChannelData(c); let ant = 0;
      for (let i = 0; i < d.length; i++) {
        const x = d[i]; if (x !== x || !isFinite(x)) { nan++; continue; }
        const a = Math.abs(x); if (a > pico) pico = a; if (a >= 0.999) clip++;
        soma += x * x; n++; const j = Math.abs(x - ant); if (j > salto) salto = j; ant = x;
      }
      bordas.ini = Math.max(bordas.ini, Math.abs(d[0] || 0)); bordas.fim = Math.max(bordas.fim, Math.abs(d[d.length - 1] || 0));
    }
    const db = (v) => v > 0 ? 20 * Math.log10(v) : -Infinity;
    return { dur: buf.length / buf.sampleRate, picoDb: db(pico), rmsDb: db(Math.sqrt(soma / Math.max(1, n))), nan: nan, clip: clip,
      silencioTotal: pico < 1e-4, saltoMax: salto, bordaIni: bordas.ini, bordaFim: bordas.fim };
  }
  function toWav(bufs, gap) {
    if (!Array.isArray(bufs)) bufs = [bufs];
    const sr = bufs[0].sampleRate, g = Math.round((gap || 0) * sr);
    let total = 0; bufs.forEach(function (b, i) { total += b.length + (i < bufs.length - 1 ? g : 0); });
    const ab = new ArrayBuffer(44 + total * 4), v = new DataView(ab);
    const w = function (o, s) { for (let i = 0; i < s.length; i++) v.setUint8(o + i, s.charCodeAt(i)); };
    w(0, 'RIFF'); v.setUint32(4, 36 + total * 4, true); w(8, 'WAVE'); w(12, 'fmt ');
    v.setUint32(16, 16, true); v.setUint16(20, 1, true); v.setUint16(22, 2, true); v.setUint32(24, sr, true);
    v.setUint32(28, sr * 4, true); v.setUint16(32, 4, true); v.setUint16(34, 16, true); w(36, 'data'); v.setUint32(40, total * 4, true);
    let o = 44;
    bufs.forEach(function (b, k) {
      const l = b.getChannelData(0), r = b.numberOfChannels > 1 ? b.getChannelData(1) : l;
      for (let i = 0; i < b.length; i++) {
        v.setInt16(o, Math.max(-1, Math.min(1, l[i])) * 32767, true); v.setInt16(o + 2, Math.max(-1, Math.min(1, r[i])) * 32767, true); o += 4;
      }
      if (k < bufs.length - 1) o += g * 4;
    });
    return ab;
  }

  // Demos (um por som/variação), usadas pelo sfx_demo.html e pela verificação.
  const DEMOS = [
    { nome: 'drone', dur: 10, cues: [{ t: 0.2, tipo: 'drone', params: { dur: 9, tomInicial: 55, subida: 3 } }] },
    { nome: 'pulso', dur: 8, cues: [{ t: 0.2, tipo: 'pulso', params: { dur: 7, bpm: 60 } }] },
    { nome: 'tiquetaque', dur: 10, cues: [{ t: 0.2, tipo: 'tiquetaque', params: { dur: 9 } }] },
    { nome: 'tiquetaque_lento', dur: 14, cues: [{ t: 0.2, tipo: 'tiquetaque', params: { dur: 13, lentidao: 1 } }] },
    { nome: 'tiquetaquePara', dur: 8, cues: [{ t: 0.2, tipo: 'tiquetaque', params: { dur: 3 } }, { t: 3.3, tipo: 'tiquetaquePara', params: {} }, { t: 0.2, tipo: 'drone', params: { dur: 7.5 } }] },
    { nome: 'stinger', dur: 5, cues: [{ t: 0.3, tipo: 'stinger', params: { intensidade: 1 } }] },
    { nome: 'stinger_leve', dur: 5, cues: [{ t: 0.3, tipo: 'stinger', params: { intensidade: 0.4 } }] },
    { nome: 'chuva_zinco', dur: 12, cues: [{ t: 0.2, tipo: 'chuva', params: { dur: 11, zinco: true } }] },
    { nome: 'chuva_abafada', dur: 12, cues: [{ t: 0.2, tipo: 'chuva', params: { dur: 11 } }] },
    { nome: 'campainha', dur: 5, cues: [{ t: 0.2, tipo: 'campainha', params: {} }] },
    { nome: 'passosChinelo', dur: 6, cues: [{ t: 0.2, tipo: 'passosChinelo', params: { n: 5 } }] },
    { nome: 'cantarolar', dur: 8, cues: [{ t: 0.2, tipo: 'cantarolar', params: { dur: 7 } }] },
    { nome: 'batidas', dur: 7, cues: [{ t: 0.3, tipo: 'batidas', params: { n: 3, espacamento: 1.6 } }] },
    { nome: 'celularToque', dur: 5, cues: [{ t: 0.2, tipo: 'celularToque', params: { abafado: true } }] },
    { nome: 'zumbidoLuz', dur: 7, cues: [{ t: 0.2, tipo: 'zumbidoLuz', params: { dur: 6 } }] },
    { nome: 'papelRasgando', dur: 2.5, cues: [{ t: 0.2, tipo: 'papelRasgando', params: {} }] },
    { nome: 'passaros', dur: 9, cues: [{ t: 0.2, tipo: 'passaros', params: { dur: 8 } }] },
    { nome: 'vento', dur: 9, cues: [{ t: 0.2, tipo: 'vento', params: { dur: 8 } }] },
    { nome: 'caixinha', dur: 10, cues: [{ t: 0.2, tipo: 'caixinha', params: { dur: 9 } }] },
    { nome: 'caixinha_desafinada_lenta', dur: 14, cues: [{ t: 0.2, tipo: 'caixinha', params: { dur: 13, desafinada: true, lenta: true } }] },
    { nome: 'caixinha_reversa', dur: 10, cues: [{ t: 0.2, tipo: 'caixinha', params: { dur: 9, reversa: true } }] },
    { nome: 'pianoBia', dur: 9, cues: [{ t: 0.2, tipo: 'pianoBia', params: { notas: ['A3', 'A3', 'A3', 'A3'], passo: 1.6 } }] },
    { nome: 'acordeBia', dur: 5, cues: [{ t: 0.2, tipo: 'acordeBia', params: {} }] },
    { nome: 'batimento', dur: 8, cues: [{ t: 0.2, tipo: 'batimento', params: { dur: 7, bpm: 70 } }] },
    { nome: 'silencioDuck', dur: 9, cues: [{ t: 0.2, tipo: 'drone', params: { dur: 8.5 } }, { t: 0.2, tipo: 'chuva', params: { dur: 8.5, zinco: true } }, { t: 3, tipo: 'silencioDuck', params: { dur: 2.5 } }, { t: 5.5, tipo: 'stinger', params: { intensidade: 0.8 } }] }
  ];

  root.Sfx = { create: create, renderOffline: renderOffline, resolverFolha: resolverFolha, agendar: agendar,
    analisar: analisar, toWav: toWav, DEMOS: DEMOS, ALVO_DB: ALVO_DB, CAL: CAL, POS: POS };
  if (typeof module !== 'undefined' && module.exports) module.exports = root.Sfx;
})(typeof window !== 'undefined' ? window : globalThis);
