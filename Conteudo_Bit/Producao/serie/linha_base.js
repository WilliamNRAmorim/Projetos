// Linha de base do motor: prova que nenhum episódio publicado mudou de pixel, e gera folhas de contato.
// Precisa do Producao/serve.ps1 rodando (http://127.0.0.1:5178). Usa o Edge headless por CDP (perfil temporário fora do repositório).
//   node linha_base.js gravar              grava linha_base.json (hash de 3 quadros por cena de c01-c28, s01-s28, o25-o28)
//   node linha_base.js conferir [ids...]   compara com linha_base.json; sai com código 1 se algum quadro mudou
//   node linha_base.js folha <id> <saida.png> [t]   folha de contato (t = "auto" = meio de cada cena, ou "1,5,9")
//   node linha_base.js hash <ids...>        imprime o hash de qualquer episódio (teste de determinismo)
//   node linha_base.js tempo <id> [n]      mede ms por quadro (n quadros espalhados, padrão 60), sem codificar vídeo
const { spawn } = require('child_process'), fs = require('fs'), path = require('path'), os = require('os');
const BASE = 'http://127.0.0.1:5178/Producao/serie/', ARQ = path.join(__dirname, 'linha_base.json');
const pad = n => String(n).padStart(2, '0');
const PUBLICADOS = [...Array.from({ length: 28 }, (_, i) => 'c' + pad(i + 1)), ...Array.from({ length: 28 }, (_, i) => 's' + pad(i + 1)), 'o25', 'o26', 'o27', 'o28'];
const pagina = id => /^(s|o|t_s)\d/.test(id) || /^t_s/.test(id) ? 'saga_o.html' : 'contos.html';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const [modo, ...args] = process.argv.slice(2).filter(a => !a.startsWith("--")), EXTRA = (process.argv.find(a => a.startsWith("--q=")) || "").slice(4); // --q=fase=2 acrescenta parâmetros à URL

async function edge() {
  const port = 9400 + Math.floor(Math.random() * 400), prof = fs.mkdtempSync(path.join(os.tmpdir(), 'motor-edge-'));
  const e = spawn('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', ['--headless=new', '--disable-extensions', '--user-data-dir=' + prof, '--remote-debugging-port=' + port, '--window-size=1200,900',
    '--disable-background-timer-throttling', '--disable-renderer-backgrounding', 'about:blank'], { stdio: 'ignore' });
  let pg; for (let i = 0; i < 40 && !pg; i++) { await sleep(500); try { pg = (await (await fetch(`http://127.0.0.1:${port}/json`)).json()).find(x => x.type === 'page'); } catch {} }
  if (!pg) throw new Error('Edge não abriu');
  const ws = new WebSocket(pg.webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
  let id = 0; const call = (method, params = {}) => new Promise(res => { const i = ++id, hd = m => { const d = JSON.parse(m.data); if (d.id === i) { ws.removeEventListener('message', hd); res(d.result); } }; ws.addEventListener('message', hd); ws.send(JSON.stringify({ id: i, method, params })); });
  const ev = async x => { const r = await call('Runtime.evaluate', { expression: x, returnByValue: true, awaitPromise: true }); return r && r.result ? r.result.value : undefined; };
  const abre = async (url, lim = 180) => { await call('Page.navigate', { url: 'about:blank' }); await call('Page.navigate', { url }); let t = '';
    for (let k = 0; k < lim * 4; k++) { await sleep(250); t = await ev('document.title'); if (/^ready|^erro/.test(t || '')) break; }
    if (!/^ready/.test(t || '')) throw new Error(`${url}: ${t}`); return t; };
  const fecha = async () => { ws.close(); e.kill(); await sleep(600); try { fs.rmSync(prof, { recursive: true, force: true }); } catch {} };
  return { ev, abre, fecha };
}

(async () => {
  const b = await edge(); let cod = 0;
  try {
    if (modo === 'gravar' || modo === 'conferir') {
      const ids = args.length ? args : PUBLICADOS, ant = fs.existsSync(ARQ) ? JSON.parse(fs.readFileSync(ARQ, 'utf8')) : {}, novo = {}, dif = [];
      for (const id of ids) { await b.abre(`${BASE}${pagina(id)}?ep=${id}&hash=1`); const h = JSON.parse(await b.ev('JSON.stringify(window.HASH_INFO)')); novo[id] = h;
        if (modo === 'conferir') { const a = ant[id]; if (!a) dif.push(`${id}: sem linha de base`); else if (a.hash !== h.hash) dif.push(`${id}: mudou (quadros ${h.quadros.map((x, i) => x !== a.quadros[i] ? i : null).filter(x => x != null).join(',')})`); }
        process.stderr.write(id + ' '); }
      process.stderr.write('\n');
      if (modo === 'gravar') { fs.writeFileSync(ARQ, JSON.stringify(Object.assign(ant, novo), null, 0).replace(/},"/g, '},\n"')); console.log(`gravado: ${ids.length} episódios, ${Object.values(novo).reduce((a, x) => a + x.n, 0)} quadros`); }
      else if (dif.length) { console.log('DIFERENTE:\n' + dif.join('\n')); cod = 1; } else console.log(`IGUAL: ${ids.length} episódios, ${Object.values(novo).reduce((a, x) => a + x.n, 0)} quadros conferidos`);
    } else if (modo === 'folha') {
      const [id, saida, t = 'auto'] = args; await b.abre(`${BASE}${pagina(id)}?ep=${id}&t=${t}${EXTRA ? "&" + EXTRA : ""}`);
      fs.writeFileSync(saida, Buffer.from((await b.ev('document.querySelector("canvas").toDataURL("image/png")')).split(',')[1], 'base64')); console.log('folha:', saida);
    } else if (modo === 'hash') { // imprime o hash de um episódio qualquer (rodar duas vezes prova que o render é determinístico)
      for (const id of args) { await b.abre(`${BASE}${pagina(id)}?ep=${id}&hash=1`); const h = JSON.parse(await b.ev('JSON.stringify(window.HASH_INFO)')); console.log(id, h.hash, h.n + ' quadros'); }
    } else if (modo === 'tempo') {
      const [id, n = 60] = args; await b.abre(`${BASE}${pagina(id)}?ep=${id}&tempo=${n}${EXTRA ? "&" + EXTRA : ""}`); console.log(await b.ev('JSON.stringify(window.TEMPO_INFO)'));
    } else console.log('uso: node linha_base.js gravar | conferir [ids] | folha <id> <saida.png> [t] | tempo <id> [n]');
  } catch (e) { console.error('ERRO:', e.message); cod = 2; }
  await b.fecha(); process.exit(cod);
})();
