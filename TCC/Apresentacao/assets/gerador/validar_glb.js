// Valida um .glb (estrutura glTF 2.0) e conta triangulos. Uso: node validar_glb.js ../mangueira.glb
const fs = require('fs');
const arq = process.argv[2] || __dirname + '/../mangueira.glb';
const d = fs.readFileSync(arq);
const erro = (m) => { console.error('ERRO:', m); process.exitCode = 1; };
if (d.readUInt32LE(0) !== 0x46546C67) erro('magic');
if (d.readUInt32LE(4) !== 2) erro('versao');
if (d.readUInt32LE(8) !== d.length) erro('tamanho total');
const jl = d.readUInt32LE(12); if (d.readUInt32LE(16) !== 0x4E4F534A) erro('chunk JSON');
const gl = JSON.parse(d.slice(20, 20 + jl).toString('utf8'));
const bl = d.readUInt32LE(20 + jl); if (d.readUInt32LE(24 + jl) !== 0x004E4942) erro('chunk BIN');
const bin = d.slice(28 + jl, 28 + jl + bl);
if (gl.buffers[0].byteLength > bin.length) erro('buffer maior que o chunk BIN');
const NC = { SCALAR: 1, VEC2: 2, VEC3: 3, VEC4: 4 }, BY = { 5126: 4, 5125: 4, 5123: 2, 5121: 1 };
gl.bufferViews.forEach((v, i) => { if ((v.byteOffset || 0) + v.byteLength > bin.length) erro('bufferView ' + i + ' fora do buffer'); });
gl.accessors.forEach((a, i) => {
  const v = gl.bufferViews[a.bufferView];
  if (a.count * NC[a.type] * BY[a.componentType] > v.byteLength) erro('accessor ' + i + ' maior que a view');
});
let tri = 0; const porNo = {};
for (const no of gl.nodes) {
  if (no.mesh === undefined) continue;
  let t = 0;
  for (const p of gl.meshes[no.mesh].primitives) {
    const pos = gl.accessors[p.attributes.POSITION], ia = gl.accessors[p.indices];
    if (!pos.min || !pos.max) erro('POSITION sem min/max');
    for (const k of ['NORMAL', 'TEXCOORD_0', 'TANGENT']) if (p.attributes[k] !== undefined && gl.accessors[p.attributes[k]].count !== pos.count) erro(k + ' com contagem diferente');
    const v = gl.bufferViews[ia.bufferView];
    const idx = new Uint32Array(bin.buffer, bin.byteOffset + (v.byteOffset || 0), ia.count);
    let mx = 0; for (const x of idx) if (x > mx) mx = x;
    if (mx >= pos.count) erro('indice fora do intervalo em ' + no.name);
    if (ia.count % 3) erro('indices nao multiplos de 3');
    t += ia.count / 3;
    const m = gl.materials[p.material];
    if (!m || m.name !== no.name) erro('material de ' + no.name + ' com outro nome: ' + (m && m.name));
  }
  porNo[no.name] = t; tri += t;
  if (no.translation || no.rotation || no.scale || no.matrix) erro('no ' + no.name + ' com transformacao (deveria ser identidade)');
}
(gl.images || []).forEach((im, i) => {
  const v = gl.bufferViews[im.bufferView]; const s = bin.slice(v.byteOffset, v.byteOffset + 8);
  if (s.readUInt32BE(0) !== 0x89504E47) erro('imagem ' + i + ' nao e PNG');
});
let mn = [1e9, 1e9, 1e9], mx = [-1e9, -1e9, -1e9];
for (const me of gl.meshes) for (const p of me.primitives) { const a = gl.accessors[p.attributes.POSITION]; for (let k = 0; k < 3; k++) { mn[k] = Math.min(mn[k], a.min[k]); mx[k] = Math.max(mx[k], a.max[k]); } }
console.log(JSON.stringify({ arquivo: arq, bytes: d.length, gerador: gl.asset.generator, triangulos: tri, porCamada: porNo,
  materiais: gl.materials.map(m => m.name), texturas: (gl.images || []).length,
  caixa: { min: mn.map(x => +x.toFixed(3)), max: mx.map(x => +x.toFixed(3)) },
  ok: !process.exitCode }, null, 1));
