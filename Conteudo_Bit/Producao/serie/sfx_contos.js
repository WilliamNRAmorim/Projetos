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
    // assobio: duas notas deslizando (uma pessoa assobiando ao longe)
    defs.assobio = function (t, p) {
      const out = G(0.35 * (p.vol == null ? 1 : p.vol)); const o = O('sine', 1700, t, t + 1.3), g = G(0), lf = O('sine', 6, t, t + 1.3), lg = G(25); C(lf, lg); lg.connect(o.frequency);
      glide(o.frequency, 1700, 2400, t, t + 0.5); o.frequency.setValueAtTime(2400, t + 0.5); o.frequency.exponentialRampToValueAtTime(1500, t + 1.2); g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(0.7, t + 0.08); g.gain.setValueAtTime(0.7, t + 1.0); g.gain.linearRampToValueAtTime(0, t + 1.3); C(o, g, out);
      eco(out, out, 0.25, 0.4, 3000, 0.5); bus(out, false); return { t: t, fim: t + 1.8 };
    };
    // limpador de para-brisa: varredura de ruído com batida de borracha a cada ciclo
    defs.limpador = function (t, p) {
      const dur = p.dur || 8, T = t + dur, out = G(0.5 * (p.vol == null ? 1 : p.vol));
      for (let s = t + 0.4; s < T - 0.6; s += 1.25) { const n = N(s, s + 0.6), bp = F('bandpass', 1800, 0.8), g = G(0); bp.frequency.setValueAtTime(1400, s); bp.frequency.linearRampToValueAtTime(2200, s + 0.5); g.gain.setValueAtTime(0, s); g.gain.linearRampToValueAtTime(0.45, s + 0.25); g.gain.linearRampToValueAtTime(0, s + 0.55); C(n, bp, g, out); const o = O('sine', 120, s + 0.5, s + 0.7), g2 = G(0); dec(g2.gain, s + 0.5, 0.003, 0.5, 0.08); C(o, g2, out); }
      bus(out, true); return { t: t, fim: T };
    };
    // gongo seco e grave (parciais inarmônicos, decaimento longo)
    defs.gongo = function (t, p) {
      const out = G(0.5 * (p.vol == null ? 1 : p.vol)); let fim = t;
      [[98, 1, 5], [147, 0.6, 4], [231, 0.5, 3.2], [303, 0.35, 2.4], [416, 0.25, 1.6]].forEach(function (h) { const o = O('sine', h[0], t, t + h[2] + 0.5), g = G(0); fim = Math.max(fim, dec(g.gain, t, 0.004, h[1], h[2])); C(o, g, out); });
      const n = N(t, t + 0.3), bp = F('bandpass', 900, 0.8), gn = G(0); dec(gn.gain, t, 0.002, 0.5, 0.2); C(n, bp, gn, out);
      bus(out, false); return { t: t, fim: fim + 0.2 };
    };
    // uivo/miado longo e agudo de gato (glide com vibrato)
    defs.uivoGato = function (t, p) {
      const dur = p.dur || 2.2, T = t + dur, out = G(0.4 * (p.vol == null ? 1 : p.vol)), o = O('sawtooth', 600, t, T), lp = F('lowpass', 2200, 1.5), g = G(0), lf = O('sine', 7, t, T), lg = G(30); C(lf, lg); lg.connect(o.frequency);
      o.frequency.setValueAtTime(520, t); o.frequency.linearRampToValueAtTime(980, t + dur * 0.45); o.frequency.linearRampToValueAtTime(560, T);
      g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(0.8, t + 0.25); g.gain.setValueAtTime(0.8, T - 0.5); g.gain.linearRampToValueAtTime(0, T); C(o, lp, g, out); eco(out, out, 0.22, 0.45, 2600, 0.5);
      bus(out, false); return { t: t, fim: T + 0.6 };
    };
    // galope: grupos de três batidas de casco; volume sobe de p.de a p.para
    defs.galope = function (t, p) {
      const dur = p.dur || 6, T = t + dur, out = G(0.7 * (p.vol == null ? 1 : p.vol)), de = p.de == null ? 0.2 : p.de, pa = p.para == null ? 1 : p.para, per = 0.3;
      for (let s = t; s < T - 0.1; s += per) { const k = (s - t) / dur, v = de + (pa - de) * k; [0, 0.09, 0.17].forEach(function (d, i) { const a = s + d, n = N(a, a + 0.12), lp = F('lowpass', 1400), g = G(0); dec(g.gain, a, 0.002, v * (i === 2 ? 1 : 0.7), 0.05); C(n, lp, g, out); const o = O('sine', 170, a, a + 0.15), g2 = G(0); dec(g2.gain, a, 0.002, v * 0.8, 0.07); C(o, g2, out); }); }
      bus(out, false); return { t: t, fim: T };
    };
    // relincho: ruído com formante deslizando, vibrato e queda
    defs.relincho = function (t, p) {
      const dur = 1.3, T = t + dur, out = G(0.45 * (p.vol == null ? 1 : p.vol)), o = O('sawtooth', 500, t, T), bp = F('bandpass', 1200, 3), g = G(0), lf = O('sine', 11, t, T), lg = G(40); C(lf, lg); lg.connect(o.frequency);
      o.frequency.setValueAtTime(420, t); o.frequency.linearRampToValueAtTime(1100, t + 0.35); o.frequency.linearRampToValueAtTime(700, t + 0.8); o.frequency.linearRampToValueAtTime(350, T);
      g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(0.9, t + 0.1); g.gain.setValueAtTime(0.8, t + 0.9); g.gain.linearRampToValueAtTime(0, T); C(o, bp, g, out); const n = N(t, T), hp = F('highpass', 2500), gn = G(0.2); C(n, hp, gn, out);
      bus(out, false); return { t: t, fim: T };
    };
    // unha raspando (ruído agudo em arrastos curtos)
    defs.raspar = function (t, p) {
      const dur = p.dur || 4, T = t + dur, out = G(0.35 * (p.vol == null ? 1 : p.vol)), n = N(t, T), hp = F('highpass', 3500), g = G(0); C(n, hp, g, out); g.gain.setValueAtTime(0, t);
      for (let s = t + 0.3; s < T - 0.6; s += rnd(0.9, 1.8)) { const d = rnd(0.25, 0.55); g.gain.setValueAtTime(0, s); g.gain.linearRampToValueAtTime(rnd(0.4, 1), s + d * 0.5); g.gain.linearRampToValueAtTime(0, s + d); }
      bus(out, false); return { t: t, fim: T };
    };
    // respirar: inspira e expira lentas (ruído rosa filtrado)
    defs.respirar = function (t, p) {
      const dur = p.dur || 8, T = t + dur, out = G(0.5 * (p.vol == null ? 1 : p.vol)), n = N(t, T, true), bp = F('bandpass', 500, 0.6), g = G(0), per = p.ritmo || 3.2; C(n, bp, g, out); g.gain.setValueAtTime(0, t);
      for (let s = t; s < T - per; s += per) { g.gain.setValueAtTime(0, s); g.gain.linearRampToValueAtTime(0.8, s + per * 0.35); g.gain.linearRampToValueAtTime(0, s + per * 0.55); g.gain.linearRampToValueAtTime(0.55, s + per * 0.7); g.gain.linearRampToValueAtTime(0, s + per * 0.95); }
      bus(out, true); return { t: t, fim: T };
    };
  };
})(typeof window !== 'undefined' ? window : globalThis);
