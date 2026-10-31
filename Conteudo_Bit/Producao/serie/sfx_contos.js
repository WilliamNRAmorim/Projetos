// Sons extras dos contos (sintetizados; só ACRESCENTA tipos ao sfx.js pelo gancho root.SfxExtra). Sem arquivos, sem licença.
(function (root) {
  root.SfxExtra = function (defs, h) {
    const { G, F, O, N, C, dec, trap, glide, eco, rnd, rng, bus } = h;
    // grilos: vários grilos, cada um um oscilador contínuo (~4,5 kHz) com envelope de "cri-cri-cri" repetido
    defs.grilos = function (t, p) {
      const dur = p.dur || 8, T = t + dur, out = G(0), n = p.n || 4;
      trap(out.gain, t, dur, 1.2, 1.2, 0.05 * (p.vol == null ? 1 : p.vol));
      for (let i = 0; i < n; i++) {
        const f = rnd(4200, 5200), o = O('sine', f, t, T), g = G(0), per = rnd(0.42, 0.7); C(o, g, out);
        for (let s = t + rnd(0, 0.5); s < T - 0.3; s += per * rnd(0.9, 1.1)) for (let j = 0; j < 4; j++) { const a = s + j * 0.052; g.gain.setValueAtTime(0, a); g.gain.linearRampToValueAtTime(rnd(0.5, 1) * 0.5, a + 0.012); g.gain.linearRampToValueAtTime(0, a + 0.04); }
      }
      bus(out, true); return { t: t, fim: T };
    };
    // crepitar: fogo estalando (estalos de ruído filtrado em intervalos aleatórios) + sopro grave
    defs.crepitar = function (t, p) {
      const dur = p.dur || 6, T = t + dur, out = G(0), v = (p.vol == null ? 1 : p.vol);
      trap(out.gain, t, dur, p.sobe ? dur * 0.8 : 0.4, 0.6, 0.5 * v);
      const n = N(t, T), hp = F('highpass', 1800), g = G(0); C(n, hp, g, out); g.gain.setValueAtTime(0, t);
      for (let s = t; s < T; s += rnd(0.02, 0.22)) { const pk = rnd(0.2, 1), e = (s - t) / dur, k = p.sobe ? 0.2 + 0.8 * e : 1; g.gain.setValueAtTime(0, s); g.gain.linearRampToValueAtTime(pk * k, s + 0.002); g.gain.linearRampToValueAtTime(0, s + rnd(0.008, 0.03)); }
      const n2 = N(t, T, true), lp = F('lowpass', 240), g2 = G(0.9); C(n2, lp, g2, out);
      bus(out, true); return { t: t, fim: T };
    };
    // rumor: ronco grave que cresce (calor, pressão); p.de/p.para = ganho relativo inicial/final
    defs.rumor = function (t, p) {
      const dur = p.dur || 6, T = t + dur, out = G(0), v = (p.vol == null ? 1 : p.vol);
      out.gain.setValueAtTime(0, t); out.gain.linearRampToValueAtTime(0.45 * v * (p.de ?? 0.2), t + 0.3); out.gain.linearRampToValueAtTime(0.45 * v * (p.para ?? 1), T - 0.1); out.gain.linearRampToValueAtTime(0, T);
      const n = N(t, T, true), lp = F('lowpass', 90); lp.frequency.setValueAtTime(90, t); lp.frequency.linearRampToValueAtTime(420, T); C(n, lp, out);
      const o = O('sine', 48, t, T), go = G(0.5); glide(o.frequency, 48, 62, t, T); C(o, go, out);
      bus(out, true); return { t: t, fim: T };
    };
    // elevador: zumbido do motor (60 Hz + harmônicos, leve variação) e roldana
    defs.elevadorZumbido = function (t, p) {
      const dur = p.dur || 6, T = t + dur, out = G(0), v = (p.vol == null ? 1 : p.vol);
      trap(out.gain, t, dur, 0.6, 0.8, 0.3 * v);
      [[60, 1], [120, 0.5], [181, 0.25]].forEach(function (h) { const o = O('sawtooth', h[0], t, T), g = G(h[1] * 0.35), lp = F('lowpass', 420); o.frequency.setValueAtTime(h[0], t); o.frequency.linearRampToValueAtTime(h[0] * (p.sobe ? 1.06 : 1.0), T); C(o, g, lp, out); });
      const n = N(t, T, true), bp = F('bandpass', 300, 0.7), g2 = G(0.5); C(n, bp, g2, out);
      bus(out, true); return { t: t, fim: T };
    };
    // ding de chegada do elevador (dois tons: sino curto)
    defs.ding = function (t, p) {
      const out = G(0.5 * (p.vol == null ? 1 : p.vol)); let fim = t;
      [[1318.5, 0], [987.8, 0.32]].forEach(function (h) { const o = O('sine', h[0], t + h[1], t + h[1] + 1.8), o2 = O('sine', h[0] * 2.76, t + h[1], t + h[1] + 1.0), g = G(0), g2 = G(0); fim = Math.max(fim, dec(g.gain, t + h[1], 0.003, 0.7, 1.2)); dec(g2.gain, t + h[1], 0.003, 0.18, 0.5); C(o, g, out); C(o2, g2, out); });
      bus(out, false); return { t: t, fim: fim + 0.2 };
    };
    // porta de elevador deslizando (ruído filtrado com varredura + batida surda no fim)
    defs.portaElevador = function (t, p) {
      const dur = p.dur || 1.3, T = t + dur, out = G(0), v = (p.vol == null ? 1 : p.vol);
      out.gain.setValueAtTime(0, t); out.gain.linearRampToValueAtTime(0.5 * v, t + 0.15); out.gain.setValueAtTime(0.5 * v, T - 0.2); out.gain.linearRampToValueAtTime(0, T);
      const n = N(t, T), bp = F('bandpass', 700, 1.2); bp.frequency.setValueAtTime(500, t); bp.frequency.linearRampToValueAtTime(1500, T); C(n, bp, out);
      const o = O('sine', 90, T - 0.05, T + 0.3), g = G(0); dec(g.gain, T - 0.05, 0.004, 0.8 * v, 0.2); C(o, g, out);
      bus(out, false); return { t: t, fim: T + 0.3 };
    };
    // pinga: gotas caindo em intervalo (com eco de banheiro)
    defs.pinga = function (t, p) {
      const dur = p.dur || 8, T = t + dur, out = G(0.4 * (p.vol == null ? 1 : p.vol)), esp = p.intervalo || 1.7;
      for (let s = t + 0.3; s < T - 0.3; s += esp * (0.8 + 0.4 * rng())) { const o = O('sine', 1400, s, s + 0.25), g = G(0); glide(o.frequency, 1700, 900, s, s + 0.08); dec(g.gain, s, 0.002, 0.7, 0.07); C(o, g, out); }
      eco(out, out, 0.19, 0.4, 2600, 0.5); bus(out, true); return { t: t, fim: T };
    };
    // rangido de porta abrindo devagar
    defs.rangido = function (t, p) {
      const dur = p.dur || 2.2, T = t + dur, out = G(0), v = (p.vol == null ? 1 : p.vol);
      out.gain.setValueAtTime(0, t); out.gain.linearRampToValueAtTime(0.35 * v, t + 0.3); out.gain.linearRampToValueAtTime(0.25 * v, T - 0.4); out.gain.linearRampToValueAtTime(0, T);
      const o = O('sawtooth', 220, t, T), lp = F('bandpass', 900, 6); glide(o.frequency, 180, 420, t, T); lp.frequency.setValueAtTime(700, t); lp.frequency.linearRampToValueAtTime(1300, T); C(o, lp, out);
      bus(out, false); return { t: t, fim: T };
    };
  };
})(typeof window !== 'undefined' ? window : globalThis);
