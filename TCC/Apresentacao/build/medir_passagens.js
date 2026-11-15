// medir_passagens.js - mede as passagens (Morph) de um mp4 de revisao: pixels claros e "com cor" antes/pico/depois + mosaico dos quadros do meio.
// Uso: servidor local so de leitura (python -m http.server 8766 em previa/), abra http://127.0.0.1:8766/ no Browser pane e cole este arquivo no console.
// Depois: await medirPassagens('/cap5/cap5.mp4', {larguraMosaico:800, cor:'ambar'}); (cor: 'ambar' | funcao (r,g,b)=>bool com a cor do capitulo).
// Passo de 0,1 s, canvas 160x90; janela de transicao = diferenca entre quadros > 4 (milhares); criterio: pico <= 1,15 x maior ponta + 60 (claros e cor).
// O contador nao pega bloco cheio: OLHE o mosaico (canvas position:fixed; window.innerWidth vem 0 no pane escondido, por isso a largura vai a mao).
async function medirPassagens(url, o = {}) {
  const W = 160, H = 90, passo = 0.1, lim = o.limiteDiff ?? 4;
  const corFn = (o.cor && typeof o.cor === 'function') ? o.cor : (r, g, b) => r > 180 && g > 90 && g < 200 && b < 90 && r - b > 120;   // ambar do cap. 5
  const blob = await (await fetch(url)).blob();
  const v = document.createElement('video'); v.muted = true; v.src = URL.createObjectURL(blob);
  await new Promise(r => v.onloadedmetadata = r);
  const c = document.createElement('canvas'); c.width = W; c.height = H; const x = c.getContext('2d', { willReadFrequently: true });
  const S = [], dur = v.duration; let prev = null;
  for (let t = 0; t <= dur - 0.05; t += passo) {
    v.currentTime = t; await new Promise(r => v.onseeked = r);
    x.drawImage(v, 0, 0, W, H); const d = x.getImageData(0, 0, W, H).data;
    let cl = 0, co = 0, df = 0;
    for (let i = 0; i < d.length; i += 4) {
      const r = d[i], g = d[i + 1], b = d[i + 2];
      if (r + g + b > 450) cl++; if (corFn(r, g, b)) co++;
      if (prev) df += Math.abs(r - prev[i]) + Math.abs(g - prev[i + 1]) + Math.abs(b - prev[i + 2]);
    }
    S.push({ t: +t.toFixed(1), cl, co, df: prev ? df / 1000 : 0 }); prev = d.slice();
  }
  // janelas: corridas de df > lim (une lacunas de ate 2 amostras); ignora corridas de 1-2 amostras (pulso)
  const J = []; let i = 1;
  while (i < S.length) {
    if (S[i].df > lim) { let a = i, b = i, k = i + 1, gap = 0; while (k < S.length && gap <= 2) { if (S[k].df > lim) { b = k; gap = 0; } else gap++; k++; } if (b - a >= 2) J.push([a, b]); i = b + 1; } else i++;
  }
  const out = [];
  for (const [a, b] of J) {
    const ant = S[Math.max(0, a - 1)], dep = S[Math.min(S.length - 1, b + 1)], mid = S[Math.round((a + b) / 2)], seg = S.slice(a, b + 1);
    const pkCl = Math.max(...seg.map(s => s.cl)), pkCo = Math.max(...seg.map(s => s.co));
    const limCl = 1.15 * Math.max(ant.cl, dep.cl) + 60, limCo = 1.15 * Math.max(ant.co, dep.co) + 60;
    out.push({ t0: S[a].t, t1: S[b].t, tMeio: mid.t, claros: `${ant.cl}/${pkCl}/${dep.cl}`, cor: `${ant.co}/${pkCo}/${dep.co}`, limite: `${Math.round(limCl)} | ${Math.round(limCo)}`, ok: pkCl <= limCl && pkCo <= limCo });
  }
  console.table(out);
  // mosaico dos quadros do meio (3 por linha)
  const mw = o.larguraMosaico ?? 800, cw = Math.floor(mw / 3), ch = Math.round(cw * 9 / 16), rows = Math.ceil(J.length / 3);
  const m = document.createElement('canvas'); m.width = cw * 3; m.height = ch * rows;
  m.style.cssText = 'position:fixed;left:0;top:0;z-index:99999;background:#000'; document.body.appendChild(m);
  const mx = m.getContext('2d');
  for (let n = 0; n < J.length; n++) { v.currentTime = out[n].tMeio; await new Promise(r => v.onseeked = r); mx.drawImage(v, (n % 3) * cw, Math.floor(n / 3) * ch, cw, ch); mx.fillStyle = '#0f0'; mx.font = '14px monospace'; mx.fillText(out[n].tMeio + 's', (n % 3) * cw + 4, Math.floor(n / 3) * ch + 16); }
  window.__passagens = out; window.__serie = S;
  return JSON.stringify(out);
}
