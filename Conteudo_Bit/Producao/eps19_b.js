// Semana 19–25/10 · fatos rápidos / humor (12h). Textos em falas_2026-10-19.json.
const EPSB = {};

// ================= Seg19 · 12h · o barulho do modem =================
EPSB.modem = { out: 'Sex23_1_TikTok_Instagram_ModemDiscado.mp4', falas: [
  { cena: 'gancho', acc: ['defeito.', 'conversa.'] },
  { cena: 'conversa', acc: ['apresentavam,', 'testavam'] },
  { cena: 'chiado', acc: ['chiado', 'aguentava.'] },
  { cena: 'fim', acc: ['calava.', 'internet'] },
  { cena: 'fecho', acc: ['ouviu'], corte: false },
], cenas: {
  gancho(g, u, k) { et(g, 'KSHHHHH · BIP · BIP · TRRRR', X0, 330, A, 34); for (let i = 0; i < 6; i++) { const r = ((u * 200 + i * 70) % 420); g.strokeStyle = `rgba(238,237,232,${1 - r / 420})`; g.lineWidth = 6; g.beginPath(); g.arc(X0 + 250, 700, 60 + r, -0.9, 0.9); g.stroke(); } painel(g, X0, 620, 300, 160, MU); et(g, 'MODEM', X0 + 90, 715, P, 36); bit(g, 'bit_pensando', 830, 1300, 200); },
  conversa(g, u, k) { painel(g, X0, 640, 300, 150, MU); et(g, 'MODEM A', X0 + 70, 725, P, 30); painel(g, XR - 300, 640, 300, 150, MU); et(g, 'MODEM B', XR - 230, 725, P, 30); ['“OI, SOU UM MODEM”', '“QUE VELOCIDADE?”', '“VAMOS TESTAR A LINHA”'].forEach((s, i) => fade(g, ap(k, 0.08 + i * 0.28, 0.08), () => { painel(g, i % 2 ? XR - 620 : X0, 360 + i * 85, 620, 70, i === 2 ? A : MU); et(g, s, (i % 2 ? XR - 620 : X0) + 20, 408 + i * 85, P, 28); })); bit(g, 'bit_apontando', 830, 1300, 170); },
  chiado(g, u, k) { et(g, 'TESTE DE RUÍDO DA LINHA', X0, 330, A, 28); painel(g, X0, 380, CW, 400, MU, '#000'); g.strokeStyle = OK; g.lineWidth = 5; g.beginPath(); for (let x = 0; x <= CW - 40; x += 6) { const a = (rnd(Math.floor(u * 20) * 31 + x) - 0.5) * 300 * (0.3 + 0.7 * clamp(k / 0.5)); const y = 580 + a * Math.sin(x * 0.05); x ? g.lineTo(X0 + 20 + x, y) : g.moveTo(X0 + 20 + x, y); } g.stroke(); fade(g, ap(k, 0.6), () => txt(g, 'A LINHA AGUENTA?', X0, 960, 80, P)); bit(g, 'bit_lupa', 840, 1300, 170); },
  fim(g, u, k) { painel(g, X0, 400, CW, 260, MU); txt(g, 'CONECTADO', X0 + CW / 2, 570, 120, OK, { align: 'center' }); et(g, 'ALTO-FALANTE: MUDO', X0, 760, MU, 36); fade(g, ap(k, 0.45), () => { txt(g, '56 kbps', X0, 940, 150, P); et(g, 'NO MÁXIMO, NA TEORIA', X0, 1000, MU, 28); }); bit(g, 'bit_joinha', 840, 1300, 170); },
  fecho(g, u, k) { txt(g, '♪', X0 + 400, 700, 420, A, { align: 'center' }); bit(g, 'bit_rindo', 800, 1300, 280); },
} };

// ================= Ter20 · 12h · Suspeito: o estagiário (formato "Suspect") =================
EPSB.suspeito = { out: 'Ter20_1_TikTok_Instagram_SuspeitoEstagiario.mp4', falas: [
  { cena: 'ficha', acc: ['estagiário.'] },
  { cena: 'palavras', acc: ['push', 'rapidinho.'] },
  { cena: 'arma', acc: ['force.'] },
  { cena: 'cena', acc: ['main,', 'sexta-feira,'] },
  { cena: 'alibi', acc: ['Álibi:', 'máquina', 'funcionava.'], corte: false },
], cenas: {
  ficha(g, u, k) { et(g, 'FICHA POLICIAL · TI', X0, 330, A, 30); painel(g, X0, 380, 380, 480, P, P); g.fillStyle = INK; g.beginPath(); g.arc(X0 + 190, 560, 90, 0, 7); g.fill(); g.fillRect(X0 + 80, 650, 220, 200); txt(g, 'SUSPEITO', X0 + 420, 470, 66, A); txt(g, 'O ESTAGIÁRIO', X0 + 420, 560, 56, P); et(g, 'IDADE: 19', X0 + 420, 640, MU, 30); et(g, 'CRACHÁ: VISITANTE', X0 + 420, 690, MU, 30); et(g, 'ÚLTIMA VEZ VISTO: NO GIT', X0 + 420, 740, MU, 26); bit(g, 'bit_lupa', 830, 1300, 190); },
  palavras(g, u, k) { et(g, 'ÚLTIMAS PALAVRAS', X0, 330, A, 30); painel(g, X0, 380, CW, 480, MU); txt(g, '“É SÓ UM', X0 + 40, 560, 110, P); fade(g, ap(k, 0.35), () => txt(g, 'PUSH', X0 + 40, 690, 150, A)); fade(g, ap(k, 0.6), () => txt(g, 'RAPIDINHO.”', X0 + 40, 790, 100, P)); bit(g, 'bit_apontando', 830, 1300, 170); },
  arma(g, u, k) { et(g, 'ARMA DO CRIME', X0, 330, A, 30); terminal(g, X0, 380, CW, 300, [['$ git push --force', A], ['+ origin/main (forced update)', MU]], k, 0.1, 0.3, 40); fade(g, ap(k, 0.6), () => { txt(g, '− −', X0, 960, 260, A); et(g, 'DOIS TRACINHOS E A PALAVRA FORCE', X0, 1030, P, 26); }); bit(g, 'bit_surpreso', 840, 1300, 150); },
  cena(g, u, k) { for (let i = -2; i < 12; i++) { g.save(); g.translate(X0 + i * 90 + 40, 420); g.rotate(-0.4); g.fillStyle = i % 2 ? INK : A; g.fillRect(0, 0, 90, 120); g.restore(); } painel(g, X0, 560, CW, 280, MU); et(g, 'CENA DO CRIME', X0 + 30, 620, A, 30); txt(g, 'BRANCH main', X0 + 30, 730, 90, P); et(g, 'SEXTA-FEIRA · 17:00', X0 + 30, 800, MU, 34); bit(g, 'bit_confuso', 840, 1300, 160); },
  alibi(g, u, k) { et(g, 'ÁLIBI', X0, 360, A, 34); txt(g, '“na minha máquina funcionava”', X0, 470, 60, P); bit(g, 'bit_dev_alibi', 600, 1300, 600); },
} };

// ================= Qua21 · 12h · Win+V =================
EPSB.winv = { out: 'Qua21_1_TikTok_Instagram_WinV.mp4', falas: [
  { cena: 'copia', acc: ['copia,', 'perde'] },
  { cena: 'teclas', acc: ['Windows', 'V.'] },
  { cena: 'historico', acc: ['fixar'] },
  { cena: 'ativar', acc: ['ativar.', 'Aceita.'], corte: false },
], cenas: {
  copia(g, u, k) { ['rascunho do e-mail', 'link do vídeo', 'número do pedido'].forEach((s, i) => { const gone = k > 0.25 + i * 0.2; painel(g, X0, 380 + i * 150, CW, 120, gone ? I2 : MU); et(g, s, X0 + 30, 455 + i * 150, gone ? '#444' : P, 34); if (gone) xis(g, XR - 70, 440 + i * 150, 20, A, 8); }); fade(g, ap(k, 0.7), () => txt(g, 'SÓ O ÚLTIMO FICA.', X0, 960, 80, A)); bit(g, 'bit_confuso', 830, 1300, 170); },
  teclas(g, u, k) { tecla(g, X0, 420, 260, 'WIN', Math.floor(u * 2) % 2 === 0, 64); txt(g, '+', X0 + 300, 560, 100, P); tecla(g, X0 + 380, 420, 260, 'V', Math.floor(u * 2) % 2 === 0, 130); fade(g, ap(k, 0.5), () => et(g, 'HISTÓRICO DA ÁREA DE TRANSFERÊNCIA', X0, 800, A, 28)); bit(g, 'bit_apontando', 830, 1300, 180); },
  historico(g, u, k) { painel(g, X0, 360, CW, 640, MU, '#000'); ['rascunho do e-mail', 'link do vídeo', 'número do pedido', 'senha do wifi'].forEach((s, i) => fade(g, ap(k, 0.05 + i * 0.12, 0.06), () => { painel(g, X0 + 20, 390 + i * 150, CW - 40, 120, MU); et(g, s, X0 + 50, 465 + i * 150, P, 32); if (i === 3) { g.fillStyle = A; g.beginPath(); g.arc(XR - 60, 450 + i * 150, 18, 0, 7); g.fill(); et(g, 'FIXADO', XR - 220, 460 + i * 150, A, 22); } })); bit(g, 'bit_joinha', 840, 1300, 140); },
  ativar(g, u, k) { painel(g, X0, 420, CW, 200, MU); et(g, 'HISTÓRICO DA ÁREA DE TRANSFERÊNCIA', X0 + 30, 490, P, 28); const on = k > 0.4; g.fillStyle = on ? OK : MU; g.fillRect(XR - 190, 530, 140, 56); g.fillStyle = P; g.fillRect(XR - (on ? 100 : 190) + 4, 534, 48, 48); et(g, on ? 'ATIVADO' : 'DESATIVADO', X0 + 30, 580, on ? OK : MU, 34); fade(g, ap(k, 0.55), () => txt(g, 'DE NADA.', X0, 900, 130, P)); bit(g, 'bit_rindo', 830, 1300, 220); },
} };

// ================= Qui22 · 12h · QWERTY =================
EPSB.qwerty = { out: 'Qui22_1_TikTok_Instagram_QWERTY.mp4', falas: [
  { cena: 'gancho', acc: ['mito.'] },
  { cena: 'travar', acc: ['travar.'] },
  { cena: 'telegrafo', acc: ['telegrafistas,', 'rápido.'] },
  { cena: 'inercia', acc: ['inércia:'] },
  { cena: 'fecho', acc: ['robô', 'QWERTY.'], corte: false },
], cenas: {
  gancho(g, u, k) { et(g, 'MITO OU VERDADE?', X0, 330, A, 30); 'QWERTYUIOP'.split('').forEach((c, i) => { const hi = i < 6; g.fillStyle = hi ? A : P; g.fillRect(X0 + i * 85, 480, 76, 110); txt(g, c, X0 + i * 85 + 38, 560, 56, INK, { align: 'center' }); }); fade(g, ap(k, 0.4), () => txt(g, 'FEITO PRA TE', X0, 800, 100, P)); fade(g, ap(k, 0.55), () => txt(g, 'DEIXAR LENTO?', X0, 910, 100, A)); bit(g, 'bit_confuso', 840, 1300, 150); },
  travar(g, u, k) { et(g, 'MÁQUINA DE ESCREVER', X0, 330, A, 28); for (let i = 0; i < 5; i++) { const a = -0.5 + i * 0.25, t = Math.min(1, k / 0.6 * 1.2); g.strokeStyle = i === 2 && k > 0.6 ? A : P; g.lineWidth = 12; g.beginPath(); g.moveTo(X0 + 200 + (i - 2) * 140, 1000); g.lineTo(X0 + 425 - Math.sin(a) * -10 + (i - 2) * 140 * (1 - t), 1000 - 520 * t); g.stroke(); } fade(g, ap(k, 0.65), () => { txt(g, 'TRAVOU.', X0, 1110, 110, A); }); bit(g, 'bit_pensando', 840, 1300, 140); },
  telegrafo(g, u, k) { et(g, 'TELEGRAFISTAS', X0, 330, A, 28); [[1, 3, 1, 1], [3, 1, 3], [1, 1, 3, 1]].forEach((row, r) => { let x = X0; row.forEach(n => { g.fillStyle = P; g.fillRect(x, 440 + r * 120, n === 1 ? 40 : 130, 40); x += (n === 1 ? 40 : 130) + 30; }); }); fade(g, ap(k, 0.45), () => { txt(g, 'QUERIAM', X0, 880, 100, P); txt(g, 'MAIS RÁPIDO.', X0, 990, 120, OK); }); bit(g, 'bit_apontando', 840, 1300, 150); },
  inercia(g, u, k) { ['ESCOLAS ENSINARAM', 'EMPRESAS COMPRARAM', 'NINGUÉM MUDOU'].forEach((s, i) => fade(g, ap(k, 0.08 + i * 0.25, 0.08), () => { painel(g, X0, 380 + i * 200, CW, 160, i === 2 ? A : MU); txt(g, s, X0 + 30, 490 + i * 200, 60, P); })); bit(g, 'bit_rindo', 840, 1300, 150); },
  fecho(g, u, k) { 'QWERTY'.split('').forEach((c, i) => { g.fillStyle = P; g.fillRect(X0 + i * 140, 540, 120, 150); txt(g, c, X0 + i * 140 + 60, 650, 90, INK, { align: 'center' }); }); et(g, 'SEM ESCAPATÓRIA', X0, 800, A, 34); bit(g, 'bit_joinha', 800, 1300, 260); },
} };

// ================= Sex23 · 12h · CC = cópia carbono =================
EPSB.cc = { out: 'Sex23_1_TikTok_Instagram_CopiaCarbono.mp4', falas: [
  { cena: 'gancho', acc: ['CC?'] },
  { cena: 'carbono', acc: ['Carbon', 'carbono.'] },
  { cena: 'oculta', acc: ['blind', 'carbon', 'copy.'] },
  { cena: 'fecho', acc: ['2026', 'séculos'], corte: false },
], cenas: {
  gancho(g, u, k) { painel(g, X0, 380, CW, 420, MU); et(g, 'Para:  chefe@empresa', X0 + 30, 450, P, 34); fade(g, ap(k, 0.3), () => { g.fillStyle = A; g.fillRect(X0 + 20, 490, 520, 70); et(g, 'CC:', X0 + 30, 540, INK, 40); et(g, 'time@empresa', X0 + 120, 540, INK, 34); }); fade(g, ap(k, 0.6), () => { txt(g, '?', X0 + 700, 760, 200, A); }); bit(g, 'bit_confuso', 840, 1300, 170); },
  carbono(g, u, k) { g.fillStyle = P; g.fillRect(X0, 400, 700, 120); g.fillStyle = '#000'; g.fillRect(X0 + 20, 540, 700, 120); g.fillStyle = P; g.fillRect(X0 + 40, 680, 700, 120); et(g, 'ORIGINAL', X0 + 20, 470, INK, 32); et(g, 'PAPEL CARBONO', X0 + 40, 610, P, 32); et(g, 'CÓPIA', X0 + 60, 750, INK, 32); fade(g, ap(k, 0.4), () => { txt(g, 'CARBON COPY', X0, 960, 110, A); et(g, '= CÓPIA CARBONO', X0, 1020, P, 34); }); bit(g, 'bit_lupa', 840, 1300, 150); },
  oculta(g, u, k) { et(g, 'CCO / BCC', X0, 330, A, 30); painel(g, X0, 380, CW, 260, MU); et(g, 'BLIND CARBON COPY', X0 + 30, 470, P, 40); g.strokeStyle = P; g.lineWidth = 8; g.beginPath(); g.arc(X0 + 200, 800, 90, 0, 7); g.stroke(); g.fillStyle = P; g.beginPath(); g.arc(X0 + 200, 800, 30, 0, 7); g.fill(); fade(g, ap(k, 0.4), () => { g.strokeStyle = A; g.lineWidth = 14; g.beginPath(); g.moveTo(X0 + 90, 900); g.lineTo(X0 + 310, 700); g.stroke(); txt(g, 'O OUTRO NÃO VÊ', X0 + 360, 820, 56, P); }); bit(g, 'bit_surpreso', 840, 1300, 150); },
  fecho(g, u, k) { txt(g, '2026', X0, 560, 220, P); et(g, 'E-MAIL', X0, 620, A, 34); txt(g, '+ PAPEL', X0, 800, 140, MU); txt(g, 'DE SÉCULOS', X0, 930, 120, MU); txt(g, 'ATRÁS', X0, 1050, 120, A); bit(g, 'bit_rindo', 830, 1300, 190); },
} };

// ================= Sáb24 · 12h · Pac-Man =================
EPSB.pacman = { out: 'Sab24_1_TikTok_Instagram_PacMan.mp4', falas: [
  { cena: 'gancho', acc: ['segurança.'] },
  { cena: 'puck', acc: ['Puck-Man,', 'paku-paku,'] },
  { cena: 'vandalismo', acc: ['vandalismo:', 'P.'] },
  { cena: 'pizza', acc: ['pizza', 'faltando.'] },
  { cena: 'fecho', acc: ['marcador'], corte: false },
], cenas: {
  gancho(g, u, k) { pac(g, X0 + 300, 640, 220, u); txt(g, 'PAC-MAN', X0, 1000, 150, P); et(g, '1980 · NAMCO', X0, 1060, MU, 30); bit(g, 'bit_pensando', 840, 1300, 150); },
  puck(g, u, k) { txt(g, 'PUCK-MAN', X0, 520, 170, P); et(g, 'JAPÃO · 1980', X0, 580, A, 32); pac(g, X0 + 200, 860, 140, u * 2); fade(g, ap(k, 0.4), () => { txt(g, 'paku-paku', X0 + 420, 880, 90, A); et(g, 'O SOM DA BOCA ABRINDO E FECHANDO', X0 + 420, 940, MU, 22); }); bit(g, 'bit_apontando', 840, 1300, 140); },
  vandalismo(g, u, k) { txt(g, 'PUCK', X0, 560, 200, P); fade(g, ap(k, 0.4), () => { g.strokeStyle = A; g.lineWidth = 18; g.beginPath(); g.moveTo(X0 + 20, 470); g.lineTo(X0 + 100, 330); g.moveTo(X0 + 20, 330); g.lineTo(X0 + 100, 470); g.stroke(); }); fade(g, ap(k, 0.6), () => { et(g, 'MEDO DE RISCAREM O P', X0, 800, A, 36); et(g, 'NAS MÁQUINAS DOS EUA', X0, 860, P, 30); }); bit(g, 'bit_surpreso', 840, 1300, 150); },
  pizza(g, u, k) { g.fillStyle = P; g.beginPath(); g.moveTo(X0 + 300, 640); g.arc(X0 + 300, 640, 220, 0.5, 5.8); g.closePath(); g.fill(); g.fillStyle = A; [[240, 560], [330, 700], [380, 560], [260, 700]].forEach(([x, y]) => { g.beginPath(); g.arc(X0 + x, y - 40 + 40, 24, 0, 7); g.fill(); }); fade(g, ap(k, 0.4), () => { txt(g, '= PAC-MAN', X0 + 540, 640, 62, P); }); et(g, 'SEGUNDO O PRÓPRIO CRIADOR', X0, 960, MU, 30); bit(g, 'bit_joinha', 840, 1300, 150); },
  fecho(g, u, k) { pac(g, X0 + 220, 640, 160, u); txt(g, 'TESTE O NOME', X0, 960, 100, P); txt(g, 'COM UM MARCADOR.', X0, 1060, 90, A); bit(g, 'bit_rindo', 830, 1300, 190); },
} };
function pac(g, cx, cy, r, u) { const m = 0.15 + 0.35 * Math.abs(Math.sin(u * 7)); g.fillStyle = A; g.beginPath(); g.moveTo(cx, cy); g.arc(cx, cy, r, m, 6.283 - m); g.closePath(); g.fill(); g.fillStyle = INK; g.beginPath(); g.arc(cx + r * 0.1, cy - r * 0.5, r * 0.09, 0, 7); g.fill(); }

// ================= Dom25 · 12h · Bliss, o papel de parede real =================
EPSB.bliss = { out: 'Dom25_1_TikTok_Instagram_BlissWallpaper.mp4', falas: [
  { cena: 'gancho', acc: ['real.', 'Photoshop.'] },
  { cena: 'colina', acc: ['Bliss.', '1996,'] },
  { cena: 'filme', acc: ['filme', 'retocou'] },
  { cena: 'xp', acc: ['Microsoft', 'XP.'] },
  { cena: 'fecho', acc: ['primeira', 'computador.'], corte: false },
], cenas: {
  gancho(g, u, k) { colina(g, X0, 380, CW, 560); fade(g, ap(k, 0.4), () => { g.save(); g.translate(X0 + 60, 1050); g.rotate(-0.04); caixa(g, 0, -80, 600, 120, A, 7); txt(g, 'FOTO REAL', 300, 10, 80, A, { align: 'center' }); g.restore(); et(g, 'ILUSTRAÇÃO EM CÓDIGO · A FOTO TEM DIREITOS', X0, 1130, MU, 22); }); bit(g, 'bit_surpreso', 840, 1300, 150); },
  colina(g, u, k) { colina(g, X0, 380, CW, 460); et(g, 'JANEIRO DE 1996', X0, 920, A, 34); et(g, 'PERTO DE SONOMA · CALIFÓRNIA', X0, 980, P, 30); txt(g, 'BLISS', X0, 1120, 150, P); bit(g, 'bit_apontando', 840, 1300, 140); },
  filme(g, u, k) { painel(g, X0, 400, 560, 400, MU); g.fillStyle = INK; g.beginPath(); g.arc(X0 + 280, 600, 110, 0, 7); g.fill(); g.strokeStyle = P; g.lineWidth = 10; g.beginPath(); g.arc(X0 + 280, 600, 110, 0, 7); g.stroke(); g.fillStyle = A; g.beginPath(); g.arc(X0 + 280, 600, 30, 0, 7); g.fill(); et(g, 'CÂMERA DE FILME', X0, 860, P, 32); fade(g, ap(k, 0.45), () => { txt(g, '0%', X0 + 600, 560, 200, OK); et(g, 'RETOQUE', X0 + 620, 620, P, 32); }); bit(g, 'bit_lupa', 840, 1300, 150); },
  xp(g, u, k) { painel(g, X0, 380, CW, 600, MU); colina(g, X0 + 6, 386, CW - 12, 540); g.fillStyle = '#2a2a2e'; g.fillRect(X0, 940, CW, 40); g.fillStyle = OK; g.fillRect(X0, 940, 150, 40); et(g, 'start', X0 + 30, 970, INK, 26); et(g, 'WINDOWS XP · PADRÃO', X0, 1060, A, 30); bit(g, 'bit_joinha', 840, 1300, 150); },
  fecho(g, u, k) { colina(g, X0, 400, CW, 520); txt(g, 'A PRIMEIRA', X0, 1040, 100, P); txt(g, 'IMAGEM?', X0, 1140, 100, A); bit(g, 'bit_rindo', 840, 1300, 160); },
} };
function colina(g, x, y, w, h) { g.save(); g.beginPath(); g.rect(x, y, w, h); g.clip(); g.fillStyle = MU; g.fillRect(x, y, w, h); g.fillStyle = P; [[0.2, 0.18, 120], [0.6, 0.12, 160], [0.8, 0.26, 90]].forEach(([a, b, r]) => { g.globalAlpha = 0.5; g.fillRect(x + w * a, y + h * b, r * 2, 26); g.globalAlpha = 1; });
  g.fillStyle = OK; g.beginPath(); g.moveTo(x, y + h); g.lineTo(x, y + h * 0.62); g.quadraticCurveTo(x + w * 0.3, y + h * 0.3, x + w * 0.58, y + h * 0.52); g.quadraticCurveTo(x + w * 0.8, y + h * 0.66, x + w, y + h * 0.5); g.lineTo(x + w, y + h); g.closePath(); g.fill(); g.restore(); caixa(g, x, y, w, h, P, 4); }

// ================= Seg19 · 12h · Tesla Roadster (apresentado em 15/10/2026) =================
function carro(g, x, y, w, col = P) { g.fillStyle = col; g.beginPath(); g.moveTo(x, y + 90); g.lineTo(x + w * 0.12, y + 60); g.lineTo(x + w * 0.32, y + 30); g.lineTo(x + w * 0.62, y + 30); g.lineTo(x + w * 0.85, y + 60); g.lineTo(x + w, y + 80); g.lineTo(x + w, y + 110); g.lineTo(x, y + 110); g.closePath(); g.fill(); g.fillStyle = INK; [0.22, 0.78].forEach(f => { g.beginPath(); g.arc(x + w * f, y + 112, 36, 0, 7); g.fill(); g.strokeStyle = col; g.lineWidth = 8; g.stroke(); }); }
EPSB.tesla = { out: 'Seg19_1_TikTok_Instagram_TeslaRoadster.mp4', falas: [
  { cena: 'gancho', acc: ['Roadster.', 'absurda.'] },
  { cena: 'zero', acc: ['segundo,', 'Tesla.'] },
  { cena: 'gas', acc: ['gás', 'SpaceX.'] },
  { cena: 'preco', acc: ['Preço?', '2028,'] },
  { cena: 'fecho', acc: ['patinete'], corte: false },
], cenas: {
  gancho(g, u, k) { et(g, 'APRESENTAÇÃO · 15/10/2026 · TEXAS', X0, 330, A, 28); carro(g, X0 + 40 - (1 - out(clamp(k / 0.5))) * 400, 560, 780); txt(g, 'ROADSTER', X0, 900, 170, P); et(g, 'TESLA', X0, 960, A, 34); bit(g, 'bit_surpreso', 830, 1300, 150); },
  zero(g, u, k) { const v = Math.round(96 * out(clamp(k / 0.35))); txt(g, String(v), X0, 640, 330, A); et(g, 'KM/H', X0 + 10, 710, P, 40); fade(g, ap(k, 0.4), () => { txt(g, '< 1 s', X0, 960, 230, P); et(g, 'SEGUNDO A PRÓPRIA TESLA · 0–60 MPH', X0, 1030, MU, 26); }); carro(g, X0 + 460, 460, 400, MU); bit(g, 'bit_joinha', 840, 1300, 150); },
  gas(g, u, k) { et(g, 'VERSÃO COM PROPULSORES', X0, 330, A, 28); carro(g, X0 + 200, 600, 640); for (let i = 0; i < 6; i++) { const f = ((u * 3 + i * 0.17) % 1); g.fillStyle = i % 2 ? A : P; g.fillRect(X0 + 200 - 40 - f * 200, 670 + i * 6 - 14, 30 + f * 120, 12); } fade(g, ap(k, 0.4), () => { txt(g, 'GÁS FRIO', X0, 960, 130, P); et(g, 'FEITO COM A SPACEX', X0, 1030, A, 34); }); bit(g, 'bit_apontando', 840, 1300, 150); },
  preco(g, u, k) { txt(g, 'US$ ???', X0, 560, 220, P); et(g, 'PREÇO: NÃO ANUNCIADO', X0, 630, A, 32); fade(g, ap(k, 0.4), () => { painel(g, X0, 760, CW, 230, MU); et(g, 'PRODUÇÃO', X0 + 30, 830, MU, 30); txt(g, '2028', X0 + 30, 950, 150, A); et(g, 'SEGUNDO MUSK', X0 + 520, 940, P, 30); }); bit(g, 'bit_confuso', 840, 1300, 150); },
  fecho(g, u, k) { g.strokeStyle = P; g.lineWidth = 12; g.beginPath(); g.arc(X0 + 160, 780, 70, 0, 7); g.arc(X0 + 560, 780, 70, 0, 7); g.stroke(); g.beginPath(); g.moveTo(X0 + 160, 780); g.lineTo(X0 + 340, 640); g.lineTo(X0 + 560, 780); g.moveTo(X0 + 340, 640); g.lineTo(X0 + 420, 560); g.stroke(); et(g, 'PATINETE ELÉTRICO', X0, 950, A, 34); bit(g, 'bit_rindo', 830, 1300, 220); },
} };
