// Gera as 28 capas em um único Edge headless, só da página capas-saga.html. Uso: node shot_capas.js
const { spawn } = require('child_process'), fs = require('fs'), path = require('path'), os = require('os');
const port = 9500 + Math.floor(Math.random() * 50), prof = path.join(os.tmpdir(), 'edgeprof-capas-' + port);
const out = path.join(__dirname, '..', 'serie-semana-2', 'capas-png'); fs.mkdirSync(out, { recursive: true });
const base = 'file:///' + path.join(__dirname, 'capas-saga.html').split(path.sep).join('/');
const e = spawn('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', ['--headless=new', '--disable-extensions', '--disable-sync', '--no-first-run', '--no-default-browser-check', '--user-data-dir=' + prof, '--remote-debugging-port=' + port, '--window-size=1080,1920', base + '?n=0'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  let pg; for (let i = 0; i < 40 && !pg; i++) { await sleep(500); try { pg = (await (await fetch(`http://127.0.0.1:${port}/json`)).json()).find(x => x.type === 'page' && x.url.includes('capas-saga')); } catch {} }
  const ws = new WebSocket(pg.webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
  let id = 0; const call = (method, params = {}) => new Promise(res => { const i = ++id, hd = m => { const d = JSON.parse(m.data); if (d.id === i) { ws.removeEventListener('message', hd); res(d.result); } }; ws.addEventListener('message', hd); ws.send(JSON.stringify({ id: i, method, params })); });
  const ev = async x => (await call('Runtime.evaluate', { expression: x, returnByValue: true, awaitPromise: true })).result.value;
  await call('Emulation.setDeviceMetricsOverride', { width: 1080, height: 1920, deviceScaleFactor: 1, mobile: false });
  for (let n = 0; n < 28; n++) {
    await call('Page.navigate', { url: base + '?n=' + n });
    for (let k = 0; k < 80; k++) { await sleep(250); if ((await ev('document.title')) === 'ready') break; }
    const r = await call('Page.captureScreenshot', { format: 'png', clip: { x: 0, y: 0, width: 1080, height: 1920, scale: 1 } });
    fs.writeFileSync(path.join(out, `capa_ep${String(n + 1).padStart(2, '0')}.png`), Buffer.from(r.data, 'base64'));
  }
  console.log('FIM'); ws.close(); e.kill(); await sleep(800); try { fs.rmSync(prof, { recursive: true, force: true }); } catch {}
})();
