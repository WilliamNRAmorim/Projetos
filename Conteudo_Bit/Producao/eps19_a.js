// Semana 19–25/10 · histórias A (19h). Cada episódio: falas [{cena, acc}] (texto em falas_2026-10-19.json) e cenas desenhadas em código.
const EPSA = {};

// ================= Seg19 · 19h · Larry Tesler e o "sem modos" =================
EPSA.tesler = { out: 'Seg19_2_TikTok_Instagram_Tesler.mp4', falas: [
  { cena: 'gancho', acc: ['apagava', 'inteiro.'] },
  { cena: 'modos', acc: ['modos.', 'tudo.'] },
  { cena: 'tesler', acc: ['Tesler', 'absurdo.'] },
  { cena: 'teste', acc: ['nunca', 'perdia'] },
  { cena: 'gypsy', acc: ['Gypsy,', 'sem'] },
  { cena: 'cola', acc: ['recortar,', 'copiar', 'colar.'] },
  { cena: 'placa', acc: ['NO', 'MODES.'] },
  { cena: 'licao', acc: ['não', 'exige'] },
  { cena: 'fecho', acc: ['2020.', 'cola,'], corte: false },
], cenas: {
  gancho(g, u, k) { et(g, 'ANOS 70 · EDITOR DE TEXTO', X0, 330, A, 28); painel(g, X0, 380, CW, 460, MU, '#000'); const s = 'O RATO ROEU A ROUPA DO REI';
    const n = Math.max(0, Math.round(s.length * (1 - ap(k, 0.5, 0.35)))); et(g, '> ' + s.slice(0, n) + (Math.floor(u * 3) % 2 ? '_' : ''), X0 + 30, 470, OK, 34);
    fade(g, ap(k, 0.45, 0.05), () => { tecla(g, X0 + 30, 600, 160, 'd', true, 70, 130); txt(g, 'APAGOU TUDO', X0 + 240, 700, 70, A); }); bit(g, 'bit_surpreso', 830, 1300, 200); },
  modos(g, u, k) { painel(g, X0, 360, 400, 360, OK); et(g, 'MODO INSERIR', X0 + 24, 420, OK, 28); txt(g, 'i', X0 + 200, 640, 200, P, { align: 'center' });
    fade(g, ap(k, 0.3), () => { painel(g, X0 + 450, 360, 400, 360, A); et(g, 'MODO APAGAR', X0 + 474, 420, A, 28); txt(g, 'd', X0 + 650, 640, 200, P, { align: 'center' }); });
    fade(g, ap(k, 0.6), () => { txt(g, 'ERROU O MODO,', X0, 900, 90, MU); txt(g, 'ERROU TUDO.', X0, 1010, 110, A); }); bit(g, 'bit_confuso', 830, 1300, 190); },
  tesler(g, u, k) { et(g, 'XEROX PARC · 1973', X0, 330, A, 28); txt(g, 'LARRY', X0, 640, 230, P); txt(g, 'TESLER', X0, 830, 230, P); fade(g, ap(k, 0.45), () => { g.save(); g.translate(X0 + 80, 1010); g.rotate(-0.04); caixa(g, 0, -70, 640, 110, A, 7); txt(g, 'ISSO É UM ABSURDO', 320, 10, 62, A, { align: 'center' }); g.restore(); }); bitEsq(g, 'bit_lupa', 850, 1300, 200); },
  teste(g, u, k) { et(g, 'TESTE COM QUEM NUNCA USOU COMPUTADOR', X0, 330, A, 26); for (let i = 0; i < 6; i++) fade(g, ap(k, 0.08 + i * 0.1, 0.06), () => { const x = X0 + (i % 3) * 290, y = 400 + Math.floor(i / 3) * 330; painel(g, x, y, 260, 290, MU); txt(g, '?', x + 130, y + 210, 190, i % 2 ? A : P, { align: 'center' }); });
    fade(g, ap(k, 0.7), () => txt(g, 'TODO MUNDO SE PERDIA', X0, 1120, 66, P)); },
  gypsy(g, u, k) { et(g, 'GYPSY · SEM MODOS', X0, 330, OK, 30); painel(g, X0, 380, CW, 460, MU, '#000'); const s = 'Você clica onde quer escrever.'; const n = Math.round(s.length * clamp(k / 0.7));
    et(g, s.slice(0, n), X0 + 30, 470, P, 32); const cx = X0 + 30 + Math.min(n, 30) * 19.2; cursor(g, cx - 4, 500 + 40 * (1 - ap(k, 0, 0.25)), 1.2);
    fade(g, ap(k, 0.75), () => { txt(g, 'SEM MODO.', X0, 980, 110, OK); }); bit(g, 'bit_joinha', 830, 1300, 190); },
  cola(g, u, k) { ['RECORTAR', 'COPIAR', 'COLAR'].forEach((s, i) => fade(g, ap(k, 0.08 + i * 0.22, 0.08), () => { painel(g, X0, 360 + i * 230, CW, 190, i === 2 ? A : MU); txt(g, s, X0 + 40, 490 + i * 230, 100, P); })); bit(g, 'bit_apontando', 830, 1300, 180); },
  placa(g, u, k) { et(g, 'PLACA DO CARRO · CALIFÓRNIA', X0, 330, MU, 28); g.fillStyle = P; g.fillRect(X0, 420, CW, 330); g.strokeStyle = INK; g.lineWidth = 10; g.strokeRect(X0 + 16, 436, CW - 32, 298); txt(g, 'NO MODES', X0 + CW / 2, 630, 130, INK, { align: 'center' });
    fade(g, ap(k, 0.4), () => et(g, 'SEGUNDO RELATOS · NOMODES.COM', X0, 830, A, 28)); bit(g, 'bit_rindo', 830, 1300, 200); },
  licao(g, u, k) { linhas(g, [['A MELHOR', MU, 110], ['TECNOLOGIA', P, 130], ['NÃO EXIGE QUE', MU, 90], ['VOCÊ ENTENDA', P, 100], ['A TECNOLOGIA.', A, 100]], X0, 460, k, 0.05, 0.14); },
  fecho(g, u, k) { tecla(g, X0, 420, 300, 'CTRL', false, 70); tecla(g, X0 + 340, 420, 190, 'V', Math.floor(u * 2) % 2 === 0, 90); et(g, 'LARRY TESLER · 1945–2020', X0, 800, MU, 30); et(g, 'TODA VEZ QUE VOCÊ COLA', X0, 860, P, 30); bit(g, 'bit_joinha', 800, 1300, 230); },
} };

// ================= Ter20 · 19h · Knight Capital =================
EPSA.knight = { out: 'Ter20_2_TikTok_Instagram_KnightCapital.mp4', falas: [
  { cena: 'gancho', acc: ['440', '45'] },
  { cena: 'quem', acc: ['maiores', 'corretoras'] },
  { cena: 'deploy', acc: ['oito', 'velho.'] },
  { cena: 'chave', acc: ['esquecida,', 'chave'] },
  { cena: 'abertura', acc: ['acordou', 'sem', 'parar.'] },
  { cena: 'ordens', acc: ['milhões', 'desligar.'] },
  { cena: 'perda', acc: ['440', 'resgate'] },
  { cena: 'licao', acc: ['espera.'] },
  { cena: 'fecho', acc: ['oitavo', 'servidor.'], corte: false },
], cenas: {
  gancho(g, u, k) { et(g, '01/08/2012 · ABERTURA DO MERCADO', X0, 330, A, 26); const m = Math.min(45, Math.floor(45 * clamp(k / 0.8))); txt(g, '00:' + String(m).padStart(2, '0'), X0, 600, 220, P); const v = Math.round(440 * clamp(k / 0.8)); fade(g, ap(k, 0.1), () => { txt(g, '−US$ ' + v + ' MI', X0, 860, 150, A); }); et(g, 'EM 45 MINUTOS', X0, 930, MU, 34); bit(g, 'bit_surpreso', 830, 1300, 190); },
  quem(g, u, k) { et(g, 'KNIGHT CAPITAL · CORRETORA DE AÇÕES · EUA', X0, 330, MU, 26); const pts = [0.2, 0.3, 0.25, 0.4, 0.5, 0.45, 0.6, 0.7, 0.68, 0.8]; painel(g, X0, 380, CW, 460, MU); g.strokeStyle = OK; g.lineWidth = 8; g.beginPath(); pts.forEach((v, i) => { const x = X0 + 30 + i * (CW - 60) / 9, y = 800 - v * 380; if (i / 9 <= clamp(k / 0.7)) i ? g.lineTo(x, y) : g.moveTo(x, y); }); g.stroke(); fade(g, ap(k, 0.5), () => txt(g, 'GIGANTE', X0, 980, 150, P)); bit(g, 'bit_apontando', 830, 1300, 180); },
  deploy(g, u, k) { et(g, 'CÓDIGO NOVO → 8 SERVIDORES', X0, 330, A, 28); for (let i = 0; i < 8; i++) { const x = X0 + (i % 4) * 215, y = 400 + Math.floor(i / 4) * 280; const on = ap(k, 0.05 + i * 0.07, 0.06); const velho = i === 7; fade(g, on, () => servidor(g, x, y, 190, 170, velho && k > 0.55 ? A : OK, String(i + 1))); }
    fade(g, ap(k, 0.6), () => { txt(g, '1 FICOU COM O', X0, 1050, 90, P); txt(g, 'CÓDIGO VELHO.', X0, 1160, 100, A); }); },
  chave(g, u, k) { terminal(g, X0, 360, CW, 460, [['# há anos sem uso', MU], ['def poder_peg():', MU], ['   comprar_sem_parar()', MU], ['', P], ['if FLAG == 1:', P]], k, 0.05, 0.12, 34);
    fade(g, ap(k, 0.55), () => { g.save(); g.translate(X0 + 30, 900); txt(g, 'MESMA CHAVE', 0, 80, 110, A); et(g, 'REAPROVEITADA PRA OUTRA COISA', 0, 140, P, 30); g.restore(); caixa(g, X0 + 20, 735, 330, 80, A, 6); }); bitEsq(g, 'bit_lupa', 850, 1300, 190); },
  abertura(g, u, k) { relogio(g, X0 + 190, 600, 170, 9, 30, P); et(g, '09:30 · ABRE O MERCADO', X0 + 30, 820, A, 28); fade(g, ap(k, 0.35), () => { servidor(g, X0 + 520, 440, 300, 300, A); et(g, 'SERVIDOR 8', X0 + 530, 800, A, 30); }); fade(g, ap(k, 0.6), () => txt(g, 'COMPRA. VENDE. COMPRA.', X0, 1050, 64, P)); bit(g, 'bit_surpreso', 840, 1300, 170); },
  ordens(g, u, k) { for (let i = 0; i < 14; i++) { const y = 360 + i * 44 + ((u * 300) % 44); const s = ['COMPRA', 'VENDE'][Math.floor(rnd(i + Math.floor(u * 9)) * 2)] + ' ' + (100 + Math.floor(rnd(i * 5 + Math.floor(u * 9)) * 900)); fade(g, 1 - Math.abs(i - 7) / 8, () => et(g, s, X0, y, i % 3 ? MU : P, 30)); }
    txt(g, 'MILHÕES', X0, 1030, 130, A); et(g, 'DE ORDENS · 100+ AÇÕES · SEM BOTÃO DE DESLIGAR', X0, 1090, P, 24); },
  perda(g, u, k) { g.save(); tremor(g, u, 0.05, 14); txt(g, '−440 MI', X0, 650, 240, A); g.restore(); et(g, 'US$ · PERDA ANTES DOS IMPOSTOS', X0, 720, P, 28); fade(g, ap(k, 0.5), () => { painel(g, X0, 810, CW, 150, MU); et(g, 'RESGATE DE EMERGÊNCIA', X0 + 30, 905, OK, 36); }); bit(g, 'bit_pensando', 830, 1300, 190); },
  licao(g, u, k) { linhas(g, [['CÓDIGO VELHO', P, 120], ['ESQUECIDO', P, 130], ['NÃO SOME.', MU, 130], ['ELE ESPERA.', A, 150]], X0, 520, k, 0.05, 0.2); },
  fecho(g, u, k) { for (let i = 0; i < 8; i++) servidor(g, X0 + (i % 4) * 215, 420 + Math.floor(i / 4) * 280, 190, 170, i === 7 ? A : OK, String(i + 1)); fade(g, ap(k, 0.4), () => { g.save(); g.strokeStyle = A; g.lineWidth = 8; g.beginPath(); g.arc(X0 + 3 * 215 + 95, 420 + 280 + 95, 140, 0, 7); g.stroke(); g.restore(); }); bit(g, k > 0.5 ? 'bit_rindo' : 'bit_lupa', 830, 1300, 220); },
} };

// ================= Qua21 · 19h · Dyn / Mirai, 10 anos =================
EPSA.dyn = { out: 'Qua21_2_TikTok_Instagram_DynMirai.mp4', falas: [
  { cena: 'gancho', acc: ['Twitter,', 'Netflix,', 'Spotify.'] },
  { cena: 'endereco', acc: ['endereço', 'deles.'] },
  { cena: 'dns', acc: ['DNS,', 'Dyn,'] },
  { cena: 'ataque', acc: ['câmeras', 'babás'] },
  { cena: 'mirai', acc: ['Mirai', 'admin,'] },
  { cena: 'exercito', acc: ['soldado.', 'Dezenas'] },
  { cena: 'sala', acc: ['câmera', 'Twitter.'] },
  { cena: 'licao', acc: ['computador', 'senha.'] },
  { cena: 'fecho', acc: ['dez', 'senha'], corte: false },
], cenas: {
  gancho(g, u, k) { et(g, '21/10/2016 · SEXTA-FEIRA', X0, 330, A, 28); ['TWITTER', 'NETFLIX', 'SPOTIFY', 'GITHUB', 'REDDIT', 'PAYPAL'].forEach((s, i) => fade(g, ap(k, 0.05 + i * 0.1, 0.06), () => { const x = X0 + (i % 2) * 430, y = 380 + Math.floor(i / 2) * 200; painel(g, x, y, 410, 170, MU); txt(g, s, x + 24, y + 105, 58, P); xis(g, x + 355, y + 85, 22, A, 10); })); bit(g, 'bit_surpreso', 830, 1300, 170); },
  endereco(g, u, k) { painel(g, X0, 400, CW, 160, P); et(g, 'twitter.com', X0 + 30, 500, P, 48); fade(g, ap(k, 0.3), () => { txt(g, '↓', X0 + 80, 700, 120, MU); painel(g, X0, 740, CW, 160, A); et(g, 'ENDEREÇO: ???', X0 + 30, 840, P, 48); }); fade(g, ap(k, 0.65), () => txt(g, 'O SITE ESTAVA NO AR.', X0, 1060, 76, MU)); bitEsq(g, 'bit_confuso', 850, 1300, 170); },
  dns(g, u, k) { painel(g, X0, 380, 330, 200, MU); et(g, 'NOME DO SITE', X0 + 24, 490, P, 28); fade(g, ap(k, 0.2), () => { txt(g, '→', X0 + 350, 500, 100, MU); painel(g, X0 + 450, 380, 170, 200, A); txt(g, 'DNS', X0 + 535, 510, 60, P, { align: 'center' }); txt(g, '→', X0 + 620, 500, 100, MU); });
    fade(g, ap(k, 0.55), () => { txt(g, 'DYN', X0, 880, 240, P); et(g, 'FAZIA O DNS PRA MUITA GENTE GRANDE', X0, 950, A, 26); }); bit(g, 'bit_apontando', 830, 1300, 180); },
  ataque(g, u, k) { et(g, 'TRÁFEGO VINDO DE', X0, 330, A, 28); [['CÂMERA DE SEGURANÇA', 0], ['GRAVADOR DE VÍDEO (DVR)', 1], ['BABÁ ELETRÔNICA', 2]].forEach(([s, i]) => fade(g, ap(k, 0.1 + i * 0.22, 0.08), () => { painel(g, X0, 380 + i * 220, CW, 190, MU); g.fillStyle = P; g.fillRect(X0 + 30, 420 + i * 220, 110, 100); g.fillStyle = INK; g.beginPath(); g.arc(X0 + 85, 470 + i * 220, 28, 0, 7); g.fill(); txt(g, s, X0 + 180, 495 + i * 220, 46, P); })); bit(g, 'bit_surpreso', 840, 1300, 150); },
  mirai(g, u, k) { et(g, 'MIRAI · VARRENDO A INTERNET', X0, 330, A, 28); const L = [['> tentando admin:admin   ✓', OK], ['> tentando root:1234    ✕', MU], ['> tentando admin:admin   ✓', OK], ['> tentando admin:admin   ✓', OK], ['> tentando 12345:12345   ✕', MU], ['> tentando admin:admin   ✓', OK]]; terminal(g, X0, 380, CW, 440, L, k, 0.05, 0.12, 32);
    fade(g, ap(k, 0.6), () => { txt(g, 'SENHA DE FÁBRICA.', X0, 960, 90, P); }); bit(g, 'bit_lupa', 840, 1300, 180); },
  exercito(g, u, k) { const n = Math.round(160 * clamp(k / 0.7)); for (let i = 0; i < n; i++) { const a = rnd(i) * 6.28, r = 420 + rnd(i * 3) * 360 * (1 - clamp(k, 0, 1) * 0.6); const x = 515 + Math.cos(a) * r * 0.55, y = 690 + Math.sin(a) * r * 0.75; g.fillStyle = i % 5 ? MU : A; g.fillRect(x, y, 10, 10); }
    painel(g, 515 - 110, 690 - 60, 220, 120, A); txt(g, 'DYN', 515, 710, 64, P, { align: 'center' }); et(g, 'DEZENAS DE MILHÕES DE IPs · SEGUNDO A DYN', X0, 1190, P, 24); },
  sala(g, u, k) { g.fillStyle = P; g.fillRect(X0 + 80, 440, 340, 220); g.fillStyle = INK; g.beginPath(); g.arc(X0 + 250, 550, 70, 0, 7); g.fill(); g.fillStyle = A; g.beginPath(); g.arc(X0 + 250 + Math.sin(u * 2) * 18, 550, 26, 0, 7); g.fill(); g.fillStyle = MU; g.fillRect(X0 + 230, 660, 40, 100);
    et(g, 'CÂMERA DA SALA', X0 + 80, 810, P, 30); fade(g, ap(k, 0.35), () => { txt(g, 'vs', X0 + 480, 590, 70, MU); painel(g, X0 + 570, 450, 280, 200, A); txt(g, 'TWITTER', X0 + 710, 570, 56, P, { align: 'center' }); }); bit(g, 'bit_rindo', 830, 1300, 200); },
  licao(g, u, k) { linhas(g, [['TODO APARELHO', MU, 90], ['NA INTERNET', MU, 90], ['É UM', P, 110], ['COMPUTADOR.', P, 116], ['PRECISA DE SENHA.', A, 80]], X0, 460, k, 0.05, 0.16); },
  fecho(g, u, k) { et(g, 'ROTEADOR', X0, 340, MU, 28); painel(g, X0, 380, CW, 150, MU); et(g, 'senha: admin', X0 + 30, 475, P, 44); fade(g, ap(k, 0.4), () => { g.strokeStyle = A; g.lineWidth = 10; g.beginPath(); g.moveTo(X0 + 20, 460); g.lineTo(X0 + 420, 460); g.stroke(); painel(g, X0, 580, CW, 150, OK); et(g, 'senha: ••••••••••••', X0 + 30, 675, P, 44); }); et(g, '21/10/2016 → 21/10/2026', X0, 860, A, 34); bit(g, 'bit_joinha', 820, 1300, 230); },
} };

// ================= Qui22 · 19h · o botão que não apertava de luva (dramatização, pilar projeto) =================
EPSA.luva = { out: 'Qui22_2_TikTok_Instagram_BotaoDeLuva.mp4', falas: [
  { cena: 'gancho', acc: ['pronto.', 'ninguém'] },
  { cena: 'pergunta', acc: ['por', 'quê.'] },
  { cena: 'olhar', acc: ['olhando', 'operador'] },
  { cena: 'luva', acc: ['luva', 'Nada.'] },
  { cena: 'custo', acc: ['dez', 'segundos.'] },
  { cena: 'eu', acc: ['mim:', 'mão'] },
  { cena: 'refiz', acc: ['enormes,', 'luva.'] },
  { cena: 'licao', acc: ['sistema', 'perto.'] },
  { cena: 'fecho', acc: ['Olhar', 'resolveu.'], corte: false },
], cenas: {
  gancho(g, u, k) { et(g, 'DRAMATIZAÇÃO · CHÃO DE FÁBRICA', X0, 330, A, 26); painel(g, X0, 380, CW, 300, OK); txt(g, 'APROVADO', X0 + 40, 540, 112, P); et(g, 'OK', XR - 120, 540, P, 60); fade(g, ap(k, 0.45), () => { et(g, 'USUÁRIOS NA LINHA:', X0, 800, MU, 34); txt(g, '0', X0, 1000, 240, A); }); bit(g, 'bit_confuso', 830, 1300, 190); },
  pergunta(g, u, k) { ['TÁ RUIM DE USAR', 'TÁ LENTO', 'NÃO FUNCIONA'].forEach((s, i) => fade(g, ap(k, 0.08 + i * 0.25, 0.08), () => { painel(g, X0 + (i % 2) * 90, 380 + i * 200, 650, 160, MU); txt(g, '“' + s + '”', X0 + 30 + (i % 2) * 90, 485 + i * 200, 54, P); })); fade(g, ap(k, 0.8), () => et(g, 'TODA SEMANA, A MESMA RESPOSTA', X0, 1080, A, 28)); bitEsq(g, 'bit_pensando', 850, 1300, 190); },
  olhar(g, u, k) { relogio(g, X0 + 190, 560, 170, 14, 0, P); fade(g, ap(k, 0.3), () => { et(g, '1 HORA', X0 + 420, 520, A, 60); et(g, 'SÓ OBSERVANDO', X0 + 420, 590, P, 32); }); g.strokeStyle = P; g.lineWidth = 10; g.beginPath(); g.arc(X0 + 300, 1000, 120, 0, 7); g.stroke(); g.beginPath(); g.moveTo(X0 + 385, 1085); g.lineTo(X0 + 470, 1170); g.stroke(); et(g, 'OPERADOR', X0 + 220, 1010, MU, 28); bit(g, 'bit_lupa', 830, 1300, 190); },
  luva(g, u, k) { painel(g, X0, 360, 420, 520, MU, '#000'); g.fillStyle = A; g.fillRect(X0 + 60, 520, 300, 120); txt(g, 'REGISTRAR', X0 + 210, 600, 46, INK, { align: 'center' });
    const on = Math.floor(u * 1.6) % 2 === 0, gx = on ? X0 + 560 : X0 + 120, gy = on ? 540 : 520; if (on) { g.fillStyle = MU; g.fillRect(X0 + 560, 520, 140, 160); [0, 1, 2, 3].forEach(i => g.fillRect(X0 + 556 + i * 36, 470 + (i % 2) * 14, 30, 70)); g.fillStyle = INK; g.fillRect(X0 + 560, 640, 140, 14); } else { g.fillStyle = P; g.fillRect(gx + 40, gy - 60, 100, 40); }
    fade(g, ap(k, 0.35), () => { txt(g, on ? 'NADA.' : 'FUNCIONA.', X0 + 480, 820, 90, on ? A : OK); }); et(g, on ? 'COM LUVA' : 'SEM LUVA', X0 + 480, 880, P, 30); bit(g, 'bit_surpreso', 840, 1300, 150); },
  custo(g, u, k) { txt(g, '10 s', X0, 580, 280, A); et(g, 'POR REGISTRO', X0, 650, P, 34); fade(g, ap(k, 0.4), () => { txt(g, '× CENTENAS', X0, 860, 130, P); et(g, 'DE PEÇAS POR TURNO', X0, 920, MU, 32); }); for (let i = 0; i < 30; i++) fade(g, ap(k, 0.5 + i * 0.012, 0.03), () => { g.fillStyle = i % 4 ? MU : A; g.fillRect(X0 + (i % 15) * 56, 1000 + Math.floor(i / 15) * 60, 44, 44); }); },
  eu(g, u, k) { et(g, 'DESENHEI PRA MIM', X0, 330, A, 28); painel(g, X0, 380, 600, 380, MU); g.fillStyle = P; g.fillRect(X0 + 80, 430, 440, 250); g.fillStyle = MU; g.fillRect(X0 + 40, 700, 520, 30);
    ['SENTADO', 'DE MOUSE', 'DE MÃO LIMPA'].forEach((s, i) => fade(g, ap(k, 0.15 + i * 0.2, 0.08), () => { et(g, '✓ ' + s, X0, 880 + i * 80, i === 2 ? OK : P, 44); })); bit(g, 'bit_apontando', 840, 1300, 170); },
  refiz(g, u, k) { g.fillStyle = A; g.fillRect(X0, 400, CW, 420); txt(g, 'REGISTRAR', X0 + CW / 2, 660, 130, INK, { align: 'center' }); fade(g, ap(k, 0.4), () => { g.fillStyle = 'rgba(140,139,134,0.85)'; g.fillRect(X0 + 450, 520, 340, 260); [0, 1, 2, 3].forEach(i => g.fillRect(X0 + 450 + i * 84, 450 + (i % 2) * 20, 70, 90)); });
    fade(g, ap(k, 0.65), () => txt(g, '1 TOQUE. SEM DIGITAR.', X0, 960, 70, P)); bit(g, 'bit_joinha', 830, 1300, 190); },
  licao(g, u, k) { linhas(g, [['QUEM USA', MU, 110], ['NÃO É QUEM', MU, 110], ['DESENHA O', P, 120], ['SISTEMA.', A, 150], ['VÁ VER DE PERTO.', P, 76]], X0, 460, k, 0.05, 0.15); },
  fecho(g, u, k) { g.strokeStyle = MU; g.lineWidth = 10; g.beginPath(); g.arc(X0 + 220, 640, 150, 0, 7); g.stroke(); txt(g, 'PERGUNTAR', X0, 940, 64, MU); xis(g, X0 + 220, 640, 100, A, 12); fade(g, ap(k, 0.5), () => { g.strokeStyle = OK; g.lineWidth = 12; g.beginPath(); g.arc(X0 + 640, 640, 150, 0, 7); g.stroke(); g.fillStyle = OK; g.beginPath(); g.arc(X0 + 640, 640, 60, 0, 7); g.fill(); txt(g, 'OLHAR', X0 + 560, 940, 64, OK); }); bit(g, 'bit_pensando', 830, 1300, 200); },
} };

// ================= Sex23 · 19h · iPod, 25 anos =================
EPSA.ipod = { out: 'Sex23_2_TikTok_Instagram_iPod.mp4', falas: [
  { cena: 'gancho', acc: ['23', '2001.'] },
  { cena: 'specs', acc: ['iPod.', 'Mil', '399'] },
  { cena: 'critica', acc: ['caro'] },
  { cena: 'mac', acc: ['Mac,'] },
  { cena: 'roda', acc: ['roda.', 'mil'] },
  { cena: 'achar', acc: ['achar', 'certa.'] },
  { cena: 'vendas', acc: ['centenas', 'iPhone.'] },
  { cena: 'licao', acc: ['importa.'] },
  { cena: 'fecho', acc: ['2022.', 'roda'], corte: false },
], cenas: {
  gancho(g, u, k) { et(g, 'KEYNOTE · 23/10/2001', X0, 330, A, 28); painel(g, X0, 380, CW, 500, MU, '#000'); const s = 1 - out(clamp(k / 0.7)); g.save(); g.translate(0, s * 300); ipodDesenho(g, X0 + 280, 460, 0.8, 0); g.restore(); fade(g, ap(k, 0.6), () => txt(g, 'UM APARELHO PEQUENO', X0, 1020, 70, P)); bit(g, 'bit_surpreso', 830, 1300, 190); },
  specs(g, u, k) { ipodDesenho(g, X0, 360, 0.95, 0); [['5 GB', 0], ['1.000 MÚSICAS', 1], ['US$ 399', 2]].forEach(([s, i]) => fade(g, ap(k, 0.1 + i * 0.25, 0.08), () => { painel(g, X0 + 340, 380 + i * 190, 510, 160, i === 2 ? A : MU); txt(g, s, X0 + 370, 485 + i * 190, i === 1 ? 50 : 76, P); })); bit(g, 'bit_apontando', 830, 1300, 160); },
  critica(g, u, k) { ['CARO DEMAIS', 'SÓ PRA MAC', 'PRA QUÊ?'].forEach((s, i) => fade(g, ap(k, 0.08 + i * 0.25, 0.08), () => { painel(g, X0 + (i % 2) * 120, 380 + i * 210, 640, 170, MU); txt(g, '“' + s + '”', X0 + 30 + (i % 2) * 120, 490 + i * 210, 64, P); })); bit(g, 'bit_confuso', 830, 1300, 180); },
  mac(g, u, k) { painel(g, X0, 400, CW, 380, MU); g.fillStyle = MU; g.fillRect(X0 + 20, 420, CW - 40, 340); txt(g, 'COMPUTADORES', X0 + 40, 520, 56, INK); fade(g, ap(k, 0.35), () => { g.fillStyle = A; g.fillRect(X0 + 20, 640, 160, 120); txt(g, 'MAC', X0 + 100, 725, 44, P, { align: 'center' }); }); fade(g, ap(k, 0.6), () => { txt(g, 'SÓ FUNCIONAVA', X0, 920, 80, P); txt(g, 'COM ELE.', X0, 1010, 110, A); }); },
  roda(g, u, k) { ipodDesenho(g, X0 + 20, 340, 1.1, u * 5); const L = ['Música ' + (Math.floor(u * 9) + 1), 'Música ' + (Math.floor(u * 9) + 2), 'Música ' + (Math.floor(u * 9) + 3)]; et(g, 'GIRA O DEDO', X0 + 420, 440, A, 34); L.forEach((s, i) => et(g, s, X0 + 420, 520 + i * 70, i === 0 ? P : MU, 38)); fade(g, ap(k, 0.5), () => txt(g, '1.000 MÚSICAS', X0 + 420, 800, 56, P)); bit(g, 'bit_joinha', 840, 1300, 170); },
  achar(g, u, k) { painel(g, X0, 380, CW, 220, MU); et(g, 'OUTROS PLAYERS', X0 + 30, 450, MU, 28); txt(g, 'MUITA MÚSICA ✓', X0 + 30, 560, 80, P); fade(g, ap(k, 0.4), () => { painel(g, X0, 660, CW, 220, A); et(g, 'ACHAR A MÚSICA CERTA', X0 + 30, 730, P, 28); txt(g, 'NINGUÉM TINHA.', X0 + 30, 840, 80, P); }); bitEsq(g, 'bit_pensando', 850, 1300, 170); },
  vendas(g, u, k) { txt(g, 'CENTENAS', X0, 600, 160, A); txt(g, 'DE MILHÕES', X0, 780, 140, P); et(g, 'DE UNIDADES VENDIDAS', X0, 850, MU, 32); fade(g, ap(k, 0.55), () => { txt(g, '→ iPhone', X0, 1030, 110, P); }); bit(g, 'bit_comemorando', 830, 1300 - Math.abs(Math.sin(u * 6)) * 18, 190); },
  licao(g, u, k) { linhas(g, [['BOA TECNOLOGIA', MU, 90], ['NÃO É A QUE', MU, 90], ['GUARDA MAIS.', P, 120], ['É A QUE DEIXA', MU, 90], ['CHEGAR RÁPIDO', P, 100], ['NO QUE IMPORTA.', A, 90]], X0, 440, k, 0.04, 0.13); },
  fecho(g, u, k) { txt(g, '2001', X0, 560, 220, P); txt(g, '→ 2022', X0 + 20, 760, 220, A); et(g, 'DESCONTINUADO', X0, 840, MU, 32); ipodDesenho(g, X0 + 690, 420, 0.4, u * 4, false); bit(g, 'bit_rindo', 820, 1300, 220); },
} };

// ================= Sáb24 · 19h · E.T. do Atari enterrado =================
EPSA.et = { out: 'Sab24_2_TikTok_Instagram_ETdoAtari.mp4', falas: [
  { cena: 'gancho', acc: ['1983,', 'enterraram'] },
  { cena: 'lenda', acc: ['30', 'lenda.'] },
  { cena: 'jogo', acc: ['E.T.', 'cinco', 'semanas'] },
  { cena: 'odio', acc: ['odiou.', 'buraco.'] },
  { cena: 'encalhe', acc: ['encalhado'] },
  { cena: 'aterro', acc: ['Alamogordo.', 'cobriu'] },
  { cena: 'dig', acc: ['2014,', 'cartucho'] },
  { cena: 'veredito', acc: ['verdade.', '750'] },
  { cena: 'fecho', acc: ['Cinco', 'Natal.'], corte: false },
], cenas: {
  gancho(g, u, k) { et(g, 'NOVO MÉXICO · 1983', X0, 330, A, 28); g.fillStyle = I2; g.fillRect(X0, 800, CW, 220); g.fillStyle = MU; g.fillRect(X0, 800, CW, 8); for (let i = 0; i < 3; i++) { const x = X0 - 300 + ((u * 260 + i * 330) % 1250); g.fillStyle = P; g.fillRect(x, 640, 180, 130); g.fillStyle = MU; g.fillRect(x + 190, 680, 80, 90); g.fillStyle = INK; g.beginPath(); g.arc(x + 40, 790, 24, 0, 7); g.arc(x + 150, 790, 24, 0, 7); g.arc(x + 240, 790, 24, 0, 7); g.fill(); }
    fade(g, ap(k, 0.4), () => txt(g, 'CARRETAS. VIDEOGAMES.', X0, 1120, 62, P)); bit(g, 'bit_surpreso', 830, 1300, 160); },
  lenda(g, u, k) { const a = 1983 + Math.round(31 * out(clamp(k / 0.6))); txt(g, String(a), X0, 560, 280, a >= 2014 ? A : P); fade(g, ap(k, 0.5), () => { txt(g, '30 ANOS', X0, 760, 150, P); g.save(); g.translate(X0 + 60, 940); g.rotate(-0.05); caixa(g, 0, -70, 560, 110, A, 7); txt(g, 'LENDA URBANA?', 280, 10, 62, A, { align: 'center' }); g.restore(); }); bitEsq(g, 'bit_lupa', 850, 1300, 180); },
  jogo(g, u, k) { g.fillStyle = MU; g.fillRect(X0, 380, 330, 400); g.fillStyle = INK; g.fillRect(X0 + 40, 420, 250, 150); txt(g, 'E.T.', X0 + 165, 530, 100, A, { align: 'center' }); g.fillStyle = I2; g.fillRect(X0 + 40, 610, 250, 120); et(g, 'ATARI 2600', X0 + 52, 680, P, 30);
    fade(g, ap(k, 0.35), () => { txt(g, '5', X0 + 400, 620, 340, A); et(g, 'SEMANAS PRA FAZER', X0 + 400, 690, P, 30); et(g, 'LICENÇA CARA DO FILME', X0 + 400, 760, MU, 26); }); bit(g, 'bit_pensando', 830, 1300, 170); },
  odio(g, u, k) { painel(g, X0, 380, CW, 560, MU, '#000'); g.fillStyle = MU; g.fillRect(X0 + 60, 600, 200, 80); g.fillRect(X0 + 360, 600, 200, 80); g.fillRect(X0 + 660, 600, 160, 80); g.fillStyle = INK; g.fillRect(X0 + 260, 600, 100, 80); g.fillRect(X0 + 560, 600, 100, 80);
    const y = 520 + (u * 140 % 160), fell = k > 0.4; g.fillStyle = OK; g.fillRect(X0 + 290, fell ? 640 : 520, 40, 70); fade(g, ap(k, 0.4), () => txt(g, 'CAIU DE NOVO.', X0, 1060, 90, A)); et(g, 'TODO MUNDO CAÍA EM BURACO', X0, 1130, P, 28); bit(g, 'bit_confuso', 840, 1300, 150); },
  encalhe(g, u, k) { const n = Math.round(48 * clamp(k / 0.8)); for (let i = 0; i < n; i++) { const x = X0 + (i % 8) * 106, y = 1000 - Math.floor(i / 8) * 90; g.fillStyle = i % 7 === 0 ? A : MU; g.fillRect(x, y, 92, 76); g.fillStyle = INK; g.fillRect(x + 10, y + 8, 72, 30); }
    txt(g, 'ENCALHADO.', X0, 400, 130, P); et(g, 'CARTUCHO SOBRANDO POR TODO LADO', X0, 460, MU, 28); },
  aterro(g, u, k) { et(g, 'ATERRO DE ALAMOGORDO', X0, 330, A, 28); g.fillStyle = MU; g.fillRect(X0, 700, CW, 14); g.fillStyle = '#000'; g.fillRect(X0 + 260, 714, 400, 280); const q = clamp(k / 0.5); for (let i = 0; i < 4; i++) { const x = X0 + 30 + i * 210, yy = 700 - 40 + (q > i / 4 ? Math.min(250, (q - i / 4) * 900) : 0); g.fillStyle = P; g.fillRect(x, yy - 90, 150, 90); g.fillStyle = A; g.fillRect(x + 20, yy - 70, 110, 24); }
    fade(g, ap(k, 0.6), () => { g.fillStyle = MU; g.fillRect(X0 + 260, 714, 400, 40); txt(g, 'COBRIRAM TUDO.', X0, 1110, 80, P); }); bit(g, 'bit_pensando', 840, 1300, 150); },
  dig(g, u, k) { et(g, 'ABRIL DE 2014 · ESCAVAÇÃO', X0, 330, A, 28); g.fillStyle = '#000'; g.fillRect(X0, 400, CW, 560); g.fillStyle = MU; g.fillRect(X0, 400, CW, 40); ['E.T.', 'CENTIPEDE', 'ASTEROIDS'].forEach((s, i) => fade(g, ap(k, 0.2 + i * 0.22, 0.08), () => { g.fillStyle = MU; g.fillRect(X0 + 40 + i * 270, 600 - Math.sin(Math.min(1, ap(k, 0.2 + i * 0.22, 0.2)) * 3) * 40, 240, 150); g.fillStyle = i === 0 ? A : INK; g.fillRect(X0 + 56 + i * 270, 616 - Math.sin(Math.min(1, ap(k, 0.2 + i * 0.22, 0.2)) * 3) * 40, 208, 60); et(g, s, X0 + 64 + i * 270, 656 - Math.sin(Math.min(1, ap(k, 0.2 + i * 0.22, 0.2)) * 3) * 40, P, 22); })); bit(g, 'bit_surpreso', 840, 1300, 170); },
  veredito(g, u, k) { txt(g, 'A LENDA ERA', X0, 500, 100, MU); txt(g, 'VERDADE.', X0, 640, 190, OK); fade(g, ap(k, 0.45), () => { et(g, 'MILHÕES?', X0, 780, MU, 36); xis(g, X0 + 270, 765, 24, A, 8); txt(g, '≤ 750 MIL', X0, 960, 170, A); et(g, 'ESTIMATIVA DO PROJETISTA DO JOGO', X0, 1020, P, 26); }); bit(g, 'bit_joinha', 840, 1300, 150); },
  fecho(g, u, k) { for (let i = 0; i < 5; i++) { g.fillStyle = i < 5 * clamp(k / 0.7) ? A : I2; g.fillRect(X0 + i * 170, 420, 150, 150); et(g, 'S' + (i + 1), X0 + i * 170 + 40, 510, INK, 40); } txt(g, '5 SEMANAS', X0, 760, 130, P); txt(g, '≠ UM JOGO.', X0, 900, 130, A); et(g, 'MORAL: NÃO PROMETA O NATAL', X0, 990, MU, 30); bit(g, 'bit_rindo', 820, 1300, 220); },
} };

// ================= Dom25 · 19h · Windows XP, 25 anos =================
EPSA.xp = { out: 'Dom25_2_TikTok_Instagram_WindowsXP.mp4', falas: [
  { cena: 'gancho', acc: ['2001.', 'XP.'] },
  { cena: 'familias', acc: ['travava', 'sólida.'] },
  { cena: 'junta', acc: ['juntou', 'casa.'] },
  { cena: 'reclama', acc: ['brinquedo', 'ativação'] },
  { cena: 'pegou', acc: ['pegou.', 'caixa'] },
  { cena: 'versoes', acc: ['Vista,', 'XP.'] },
  { cena: 'suporte', acc: ['2014.', 'meio.'] },
  { cena: 'licao', acc: ['recusam'] },
  { cena: 'fecho', acc: ['Vinte', 'abertura.'], corte: false },
], cenas: {
  gancho(g, u, k) { et(g, '25/10/2001', X0, 330, A, 34); txt(g, 'WINDOWS', X0, 540, 170, P); txt(g, 'XP', X0, 850, 330, OK); painel(g, X0, 940, 400, 100, OK, OK); txt(g, 'start', X0 + 200, 1015, 64, INK, { align: 'center' }); fade(g, ap(k, 0.5), () => et(g, 'CHEGA ÀS LOJAS', X0, 1110, MU, 24)); bit(g, 'bit_surpreso', 840, 1300, 170); },
  familias(g, u, k) { painel(g, X0, 380, CW, 270, MU); et(g, 'LINHA DOMÉSTICA', X0 + 30, 440, MU, 28); txt(g, 'TRAVAVA', X0 + 30, 590, 110, A); fade(g, ap(k, 0.45), () => { painel(g, X0, 720, CW, 270, MU); et(g, 'LINHA PROFISSIONAL', X0 + 30, 780, MU, 28); txt(g, 'SÓLIDA', X0 + 30, 930, 110, OK); }); bit(g, 'bit_apontando', 840, 1300, 150); },
  junta(g, u, k) { const t = out(clamp(k / 0.5)); painel(g, X0 + 20 + 200 * t, 400, 250, 180, MU); painel(g, XR - 270 - 200 * t + 0, 400, 250, 180, MU); et(g, 'DOMÉSTICA', X0 + 40 + 200 * t, 500, P, 26); et(g, 'PROFISSIONAL', XR - 250 - 200 * t, 500, P, 22); fade(g, ap(k, 0.5), () => { txt(g, 'XP', X0 + CW / 2, 880, 330, OK, { align: 'center' }); et(g, 'NÚCLEO ESTÁVEL · CARA DE CASA', X0, 980, P, 28); }); bit(g, 'bit_joinha', 840, 1300, 170); },
  reclama(g, u, k) { ['“PARECE DE BRINQUEDO”', '“PEDE ATIVAÇÃO?”'].forEach((s, i) => fade(g, ap(k, 0.08 + i * 0.3, 0.08), () => { painel(g, X0, 380 + i * 250, CW, 200, MU); txt(g, s, X0 + 30, 505 + i * 250, 58, P); }));
    fade(g, ap(k, 0.7), () => { painel(g, X0, 900, CW, 130, OK, '#1a2a22'); et(g, 'ATIVAR PELA INTERNET (30 DIAS)', X0 + 30, 985, OK, 32); }); bit(g, 'bit_confuso', 840, 1300, 150); },
  pegou(g, u, k) { ['ESCOLA', 'ESCRITÓRIO', 'BANCO', 'CAIXA ELETRÔNICO'].forEach((s, i) => fade(g, ap(k, 0.08 + i * 0.2, 0.07), () => { painel(g, X0, 370 + i * 190, CW, 160, i === 3 ? A : MU); txt(g, s, X0 + 40, 480 + i * 190, 72, P); })); bit(g, 'bit_comemorando', 840, 1300 - Math.abs(Math.sin(u * 6)) * 14, 150); },
  versoes(g, u, k) { ['VISTA', '7', '8'].forEach((s, i) => fade(g, ap(k, 0.08 + i * 0.2, 0.07), () => { painel(g, X0, 380 + i * 170, 380, 140, MU); txt(g, s, X0 + 24, 485 + i * 170, 72, P); et(g, '(CHEGOU)', X0 + 230, 475 + i * 170, MU, 24); })); fade(g, ap(k, 0.6), () => { painel(g, X0 + 450, 380, 400, 480, OK); txt(g, 'XP', X0 + 650, 700, 200, OK, { align: 'center' }); et(g, 'SEGUIA AQUI', X0 + 650, 790, P, 30); g.textAlign = 'left'; }); bit(g, 'bit_pensando', 840, 1300, 150); },
  suporte(g, u, k) { et(g, 'FIM DO SUPORTE OFICIAL', X0, 330, A, 28); txt(g, '08/04/2014', X0, 580, 140, P); fade(g, ap(k, 0.35), () => { txt(g, '12,5', X0, 840, 300, A); et(g, 'ANOS DE VIDA', X0 + 20, 910, P, 40); }); g.fillStyle = I2; g.fillRect(X0, 1010, CW, 40); g.fillStyle = OK; g.fillRect(X0, 1010, CW * clamp(k / 0.8), 40); et(g, '2001', X0, 1100, MU, 26); et(g, '2014', XR - 80, 1100, MU, 26); },
  licao(g, u, k) { linhas(g, [['SOFTWARE BOM', MU, 100], ['É O QUE AS', MU, 100], ['PESSOAS', P, 120], ['SE RECUSAM', P, 120], ['A TROCAR.', A, 130]], X0, 480, k, 0.05, 0.16); },
  fecho(g, u, k) { g.fillStyle = MU; g.fillRect(X0, 380, CW, 560); g.fillStyle = OK; g.beginPath(); g.moveTo(X0, 940); g.quadraticCurveTo(X0 + 300, 600, X0 + 560, 760); g.quadraticCurveTo(X0 + 720, 840, XR, 700); g.lineTo(XR, 940); g.closePath(); g.fill(); g.fillStyle = OK; g.fillRect(X0, 940, CW, 8); caixa(g, X0, 380, CW, 560, P, 6); et(g, 'BLISS', X0 + 20, 420, INK, 28); txt(g, '25 ANOS', X0, 1090, 130, P); bit(g, 'bit_rindo', 820, 1300, 200); },
} };
