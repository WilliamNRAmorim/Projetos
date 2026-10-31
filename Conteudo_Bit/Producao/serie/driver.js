// Driver do Edge headless (CDP) para os contos. Uso: node driver.js <modo> <url> [saida.png] [--w=1080 --h=1920]
// modos: shot (espera title "ready", salva PNG da página) | info (espera title "ready", imprime MOTOR_INFO/MIX_INFO) | render (idem, espera até 15 min)
const { spawn } = require('child_process'), fs = require('fs'), path = require('path');
const [modo, url, saida] = process.argv.slice(2).filter(a => !a.startsWith('--'));
const opt = k => (process.argv.find(a => a.startsWith('--' + k + '=')) || '').split('=')[1];
const w = +(opt('w') || 1080), h = +(opt('h') || 1920), port = +(opt('port') || 9340 + Math.floor(Math.random() * 50));
const prof = path.join(__dirname, 'preview', 'edgeprof-contos-' + port);
const e = spawn('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', ['--headless=new', '--disable-extensions', '--user-data-dir=' + prof, '--remote-debugging-port=' + port, `--window-size=${w},${h}`,
  '--disable-background-timer-throttling', '--disable-renderer-backgrounding', '--disable-backgrounding-occluded-windows', '--autoplay-policy=no-user-gesture-required', url], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  let pg; for (let i = 0; i < 40 && !pg; i++) { await sleep(500); try { pg = (await (await fetch(`http://127.0.0.1:${port}/json`)).json()).find(x => x.type === 'page'); } catch {} }
  const ws = new WebSocket(pg.webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
  let id = 0; const call = (method, params = {}) => new Promise(res => { const i = ++id, hd = m => { const d = JSON.parse(m.data); if (d.id === i) { ws.removeEventListener('message', hd); res(d.result); } }; ws.addEventListener('message', hd); ws.send(JSON.stringify({ id: i, method, params })); });
  const ev = async x => (await call('Runtime.evaluate', { expression: x, returnByValue: true, awaitPromise: true })).result.value;
  const lim = +(opt('lim') || (modo === 'render' ? 900 : 120)); let t = '';
  for (let k = 0; k < lim * 2; k++) { t = await ev('document.title'); if (/^ready|^erro/.test(t)) break; if (modo === 'render' && k % 20 === 0) process.stderr.write('.' + t + ' '); await sleep(500); }
  console.log('title:', t);
  if (modo === 'shot' && saida) { await ev('window.scrollTo(0,0)'); const r = await call('Page.captureScreenshot', { format: 'png' }); fs.writeFileSync(saida, Buffer.from(r.data, 'base64')); const inf = await ev('JSON.stringify(window.INFO||null)'); if (inf && inf !== 'null') console.log(inf); }
  else console.log(JSON.stringify({ motor: await ev('JSON.stringify(window.MOTOR_INFO||null)'), mix: await ev('JSON.stringify(window.MIX_INFO||null)') }));
  const errs = await ev('document.body.innerText.slice(0,300)'); if (/ERRO/.test(errs)) console.log(errs);
  ws.close(); e.kill(); await sleep(800); try { fs.rmSync(prof, { recursive: true, force: true }); } catch {}
})();
