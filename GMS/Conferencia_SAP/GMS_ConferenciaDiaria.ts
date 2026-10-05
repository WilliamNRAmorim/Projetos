/**
 * GMS_ConferenciaDiaria  v1.0.2  (05/10/2026)  MEL-196  C29
 * v1.0.2: o runtime do Office Script compila para ES5 sem iterador: nada de spread/for-of em Map ou Set
 * (deu "Invalid array length" no 1o teste do fluxo). Map/Set so via chavesMap/valoresMap/chavesSet.
 * Office Script — roda pelo Power Automate em cima do mb51.xlsx (somente leitura).
 *
 * Confere, lance a lance, as tres pontas da cabine de teste:
 *   GMS  (RegistrosInspeção = lance aprovado, TiposErros = refugo)
 *   SAP  (MB51: 101/102, unidade M, deposito GRT4 — lido direto desta planilha)
 *   Packing (BD Packing List — vem do script GMS_LerPacking)
 *
 * Regra de OP conforme:  GMS aprovado + GMS refugo = SAP (101 - 102), tolerancia 0,5 m.
 * Packing e SAP: saem no mesmo dia do lance; o 3o turno pode virar o dia. Domingo nao trabalha,
 * entao o 3o turno de sabado pode terminar na segunda: lance de sabado/domingo e cobrado na segunda
 * (diaCobranca). O fluxo roda de terca a sabado as 08:00 e confere o dia util anterior (seg–sex).
 * Refugo: nao vai para o packing. O SAP lanca em lote: seg->ter, ter/qua->qui, qui->sex, sex/sab->seg
 * (William + medido em ago-set/26). Refugo so e cobrado depois do dia de lancamento dele (prazoRefugo).
 * Base medida em 15–30/09/2026: 99,8% dos lances entram no SAP no mesmo dia do GMS,
 * 98% casam exato por metragem, e 280 de 331 OPs fecham com diferenca zero.
 *
 * Devolve: assunto + HTML do e-mail + lista de itens para a lista Conferencia_SAP.
 * Nao escreve nada na planilha.
 */

// ───────────────────────── contrato com o fluxo ─────────────────────────

interface ItemConferencia {
  chave: string;          // OP, ou "PL <romaneio>" para divergencia so de packing
  idLista: number;        // ID do item na lista Conferencia_SAP (0 = criar novo)
  op: string;
  pn: string;
  categoria: string;
  prioridade: number;     // 1 = mais grave
  status: string;         // Aberto | Justificado | Resolvido
  gmsM: number;           // GMS aprovado (m)
  refugoGmsM: number;     // GMS refugo (m)
  sapM: number;           // SAP 101-102 (m)
  packingM: number;       // packing casado com os lances da OP (m)
  difM: number;           // GMS aprovado + refugo - SAP
  provavelOP: string;
  detalhe: string;
  acao: string;
  quemResolve: string;
  cabine: string;
  dataRef: string;        // yyyy-mm-dd da conferencia
  corpoSP: string;        // JSON pronto para MERGE no item idLista (o fluxo só repassa)
  corpoSPNovo: string;    // JSON pronto para POST de item novo (inclui DataDeteccao)
}

interface Resultado {
  assunto: string;
  html: string;
  dataRef: string;
  mb51Atualizado: boolean;
  opsConferidas: number;
  naoConformes: number;
  resolvidos: number;
  metrosEmJogo: number;
  refugoAguardandoM: number;
  itens: ItemConferencia[];
}

// entradas: aceita o corpo CRU do "Enviar uma solicitação HTTP ao SharePoint" (odata=nometadata,
// nomes internos das listas) ou o formato curto {id, op, q, dt...}. Nomes internos conferidos em 02/10.
type Val = string | number | boolean | null;
interface InspIn { id?: Val; op?: Val; q?: Val; dt?: Val; cab?: Val;
  ID?: Val; OP_ID?: Val; Quantidade_Inspe_x00e7__x00e3_o?: Val; DataHoraInspecao?: Val; cabine_teste?: Val; }
interface RefIn { id?: Val; op?: Val; q?: Val; dt?: Val; cod?: Val; cab?: Val;
  ID?: Val; OP_ID?: Val; _x0043_?: Val; Created?: Val; A?: Val; cabine_teste?: Val; }
interface FichaIn { op?: Val; pn?: Val; OP?: Val; Mangueira?: Val; }
interface PackIn { id: number; sl: number; pn: string; q: number; ts: string; c: boolean; }
interface AbertoIn { chave?: Val; id?: Val; status?: Val; desde?: Val; categoria?: Val;
  Title?: Val; ID?: Val; Status?: Val; DataDeteccao?: Val; Categoria?: Val; }
interface Aberto { chave: string; id: number; status: string; categoria: string; }

// ───────────────────────── modelo interno ─────────────────────────

interface Lance { id: number; op: string; q: number; t: number; dia: string; cab: string; usado: boolean; slice: string; }
interface Refugo { id: number; op: string; q: number; t: number; dia: string; cod: string; usado: boolean; }
interface DocSap { op: string; pn: string; doc: string; q: number; dia: string; mvt: string; user: string; usado: boolean; papel: string; }
interface Slice { id: number; sl: number; pn: string; q: number; t: number; dia: string; casou: string; opCasada: string; difQ: number; }
interface AnaliseOP {
  op: string; pn: string; gms: number; ref: number; sap: number; dif: number;
  ug: Lance[]; us: DocSap[]; ur: Refugo[]; dup: DocSap[];
  temSap: boolean; temGms: boolean; cab: string; provavel: string; refGraca: number;
}

const MIN_H = 3600000;
const TOL_LANCE = 0.05;
const PACK_ANTES_H = 96;   // janela de CASAMENTO (acha packing atrasado); a COBRANCA e no mesmo dia
const PACK_DEPOIS_H = 2;   // relogio do packing pode estar ate 2 h atras do GMS
const PACK_JANELA_DIAS = 6;
const FUSO_H = -3;         // Brasilia, sem horario de verao
let packingSemDia = false;

interface Categoria { nome: string; prio: number; acao: string; quem: string; }
const CAT: { [k: string]: Categoria } = {
  OP_ERRADA: { nome: "OP digitada errada no GMS", prio: 1, acao: "Corrigir a OP dos lances no GMS para a provável OP correta", quem: "Apontamento GMS" },
  SAP_SEM_GMS: { nome: "SAP lançou, GMS não tem a OP", prio: 2, acao: "Conferir se a OP foi produzida fora do GMS; apontar no GMS ou estornar no SAP", quem: "Supervisão + PCP" },
  GMS_SEM_SAP: { nome: "GMS apontou, SAP não lançou a OP", prio: 3, acao: "Lançar no SAP (MIGO 101) os lances apontados no GMS", quem: "SAP / Logística" },
  LANCE_OP_ERRADA: { nome: "Lance apontado na OP errada", prio: 4, acao: "Mover o lance para a OP certa (no GMS ou no SAP, onde estiver errado)", quem: "Apontamento GMS / SAP" },
  METRAGEM: { nome: "Metragem digitada diferente (GMS × SAP)", prio: 5, acao: "Conferir a etiqueta do lance e corrigir o lado errado", quem: "Apontamento GMS / SAP" },
  SAP_LANCE: { nome: "SAP lançou lance que o GMS não tem", prio: 6, acao: "Apontar o lance no GMS ou estornar (102) no SAP", quem: "Apontamento GMS / SAP" },
  GMS_LANCE: { nome: "GMS apontou lance que o SAP não tem", prio: 7, acao: "Lançar o lance no SAP (MIGO 101) ou excluir do GMS se não existe", quem: "SAP / Logística" },
  REF_MAIS: { nome: "Refugo a mais no SAP (duplicado/excesso)", prio: 8, acao: "Estornar no SAP o refugo lançado em duplicidade", quem: "SAP / Qualidade" },
  REF_FALTA: { nome: "Refugo faltando no SAP", prio: 9, acao: "Lançar no SAP o refugo apontado no GMS", quem: "SAP / Qualidade" },
  OUTRA: { nome: "Outra divergência de metragem", prio: 10, acao: "Abrir a OP e conferir lance a lance", quem: "Análise manual" },
  PACK_SEM_GMS: { nome: "Packing sem lance no GMS", prio: 11, acao: "Conferir o romaneio: lance sem apontamento ou metragem digitada diferente", quem: "Logística / Cabine" },
  PACK_DUP: { nome: "Romaneio duplicado no Packing", prio: 12, acao: "Cancelar o romaneio duplicado no Packing List", quem: "Logística / Cabine" },
  PACK_ID: { nome: "ID de romaneio repetido no Packing", prio: 12, acao: "Corrigir o ID do romaneio no Packing List (um ID por romaneio)", quem: "Logística / Cabine" },
  SEM_PACK: { nome: "Lance aprovado sem packing", prio: 13, acao: "Registrar o lance no Packing List ou confirmar onde está o material", quem: "Logística / Cabine" }
};

// ───────────────────────── main (Power Automate) ─────────────────────────

function main(
  workbook: ExcelScript.Workbook,
  dataRef: string,
  inspecoesJson: string,
  refugosJson: string,
  fichaJson: string,
  packingJson: string,
  abertosJson: string,
  toleranciaM: number,
  janelaDias: number
): Resultado {
  const tol = toleranciaM > 0 ? toleranciaM : 0.5;
  const janela = janelaDias > 0 ? janelaDias : 35;
  const d = dataRef && dataRef.length >= 10 ? dataRef.substring(0, 10) : diaUtilAnterior(diaDe(agoraLocal()));
  const inicio = somaDias(d, -janela);
  const sap = lerMB51(workbook, inicio);
  return conferir(d, sap, parseLista<InspIn>(inspecoesJson), parseLista<RefIn>(refugosJson),
    parseLista<FichaIn>(fichaJson), parseLista<PackIn>(packingJson), parseLista<AbertoIn>(abertosJson), tol, inicio);
}

function parseLista<T>(s: string): T[] {
  if (!s || s.trim().length === 0) { return []; }
  const v = JSON.parse(s) as T[] | { value?: T[]; d?: { results?: T[] } };
  if (Array.isArray(v)) { return v; }
  if (v && Array.isArray(v.value)) { return v.value; }
  if (v && v.d && Array.isArray(v.d.results)) { return v.d.results; }
  return [];
}
function pega(a: Val | undefined, b: Val | undefined): Val { return a !== undefined && a !== null && a !== "" ? a : (b === undefined ? null : b); }
function txt(v: Val): string { return v === null || v === undefined ? "" : String(v); }

// ───────────────────────── leitura do MB51 ─────────────────────────

/**
 * Le so as colunas usadas, em blocos de 20 mil linhas (limite de 5 MB por chamada).
 * O supervisor recria o mb51.xlsx todo dia a partir do export do SAP: o script NAO assume aba nem
 * linha. Procura, em cada aba, a linha (entre as 15 primeiras) que tem os cabecalhos do MB51, e acha
 * cada coluna pelo nome (ordem nao importa, maiusculas/espacos nao importam).
 */
function lerMB51(workbook: ExcelScript.Workbook, inicio: string): DocSap[] {
  const precisa = ["Material", "Order", "Storage location", "Movement type", "Material Document",
    "Material Doc.Item", "Posting Date", "Unit of Entry", "Quantity", "User Name"];
  const chave = (v: string | number | boolean) => String(v).trim().toLowerCase().replace(/\s+/g, " ");
  let ws: ExcelScript.Worksheet | null = null;
  let linCab = -1;
  let nLin = 0;
  let nCol = 0;
  const idx: { [k: string]: number } = {};
  for (const w of workbook.getWorksheets()) {
    const u = w.getUsedRange(true);
    if (!u) { continue; }
    const nl = u.getRowCount();
    const nc = Math.min(u.getColumnCount(), 80);
    const topo = w.getRangeByIndexes(0, 0, Math.min(15, nl), nc).getValues();
    for (let r = 0; r < topo.length && !ws; r++) {
      const cab = topo[r].map(chave);
      if (cab.indexOf("order") < 0 || cab.indexOf("posting date") < 0 || cab.indexOf("quantity") < 0) { continue; }
      const faltando = precisa.filter(n => cab.indexOf(chave(n)) < 0);
      if (faltando.length) { throw new Error("MB51 (aba " + w.getName() + ") sem a(s) coluna(s): " + faltando.join(", ") + ". O export do SAP mudou?"); }
      for (const n of precisa) { idx[n] = cab.indexOf(chave(n)); }
      ws = w; linCab = r; nLin = nl; nCol = u.getColumnCount();
    }
    if (ws) { break; }
  }
  if (!ws) { throw new Error("Nenhuma aba do mb51.xlsx tem o cabeçalho do MB51 (Order, Posting Date, Quantity) nas 15 primeiras linhas."); }
  // agrupa colunas contiguas para ler menos vezes
  const cols = precisa.map(n => idx[n]).sort((a, b) => a - b);
  const grupos: number[][] = [];
  for (const c of cols) {
    const g = grupos.length ? grupos[grupos.length - 1] : null;
    if (g && c === g[g.length - 1] + 1) { g.push(c); } else if (!g || c !== g[g.length - 1]) { grupos.push([c]); }
  }
  const serialInicio = serialDe(inicio);
  const out: DocSap[] = [];
  const BLOCO = 20000;
  for (let r0 = linCab + 1; r0 < nLin; r0 += BLOCO) {
    const n = Math.min(BLOCO, nLin - r0);
    const linha: (string | number | boolean)[][] = [];
    for (let k = 0; k < n; k++) { linha.push(new Array<string | number | boolean>(nCol)); }
    for (const g of grupos) {
      const vals = ws.getRangeByIndexes(r0, g[0], n, g.length).getValues();
      for (let k = 0; k < n; k++) { for (let j = 0; j < g.length; j++) { linha[k][g[j]] = vals[k][j]; } }
    }
    for (const L of linha) {
      if (String(L[idx["Unit of Entry"]]).trim() !== "M") { continue; }
      if (String(L[idx["Storage location"]]).trim() !== "GRT4") { continue; }
      const mvt = String(L[idx["Movement type"]]).trim();
      if (mvt !== "101" && mvt !== "102") { continue; }
      const serial = serialDeCelula(L[idx["Posting Date"]]);
      if (serial < serialInicio) { continue; }
      const op = textoOP(L[idx["Order"]]);
      if (!op) { continue; }
      out.push({
        op: op,
        pn: normPN(String(L[idx["Material"]])),
        doc: String(L[idx["Material Document"]]).trim() + "/" + String(L[idx["Material Doc.Item"]]).trim(),
        q: num(L[idx["Quantity"]]),
        dia: diaDeSerial(serial),
        mvt: mvt,
        user: String(L[idx["User Name"]]).trim(),
        usado: false,
        papel: ""
      });
    }
  }
  return out;
}

// ───────────────────────── motor (funcao pura) ─────────────────────────

function conferir(
  d: string, sapDocs: DocSap[], inspIn: InspIn[], refIn: RefIn[], fichaIn: FichaIn[],
  packIn: PackIn[], abertosIn: AbertoIn[], tol: number, inicio: string
): Resultado {
  // 1) normaliza
  const lances: Lance[] = inspIn.map(r => {
    const t = instanteUTC(txt(pega(r.dt, r.DataHoraInspecao)));
    return { id: Number(pega(r.id, r.ID)), op: textoOP(pega(r.op, r.OP_ID)), q: num(pega(r.q, r.Quantidade_Inspe_x00e7__x00e3_o)), t: t, dia: diaDe(t), cab: limpo(txt(pega(r.cab, r.cabine_teste))), usado: false, slice: "" };
  }).filter(l => l.op !== "" && l.dia >= inicio && l.dia <= d);
  const refugos: Refugo[] = refIn.map(r => {
    const t = instanteUTC(txt(pega(r.dt, r.Created)));
    return { id: Number(pega(r.id, r.ID)), op: textoOP(pega(r.op, r.OP_ID)), q: num(pega(r.q, r._x0043_)), t: t, dia: diaDe(t), cod: limpo(txt(pega(r.cod, r.A))), usado: false };
  }).filter(x => x.op !== "" && x.dia >= inicio && x.dia <= d);
  const sap = sapDocs.filter(s => s.dia <= d);
  const slices: Slice[] = packIn.filter(p => !p.c).map(p => {
    const t = instanteLocal(p.ts);
    return { id: Number(p.id), sl: Number(p.sl), pn: normPN(p.pn), q: num(p.q), t: t, dia: diaDe(t), casou: "", opCasada: "", difQ: 0 };
  }).filter(s => s.id > 0 && s.q > 0 && s.dia >= inicio && s.dia <= d);

  const pnPorOP = new Map<string, string>();
  for (const f of fichaIn) { const o = textoOP(pega(f.op, f.OP)); const pn = txt(pega(f.pn, f.Mangueira)); if (o && pn) { pnPorOP.set(o, normPN(pn)); } }
  for (const s of sap) { if (s.pn) { pnPorOP.set(s.op, s.pn); } }   // SAP manda no PN

  const lancesOP = agruparPorOP(lances);
  const refOP = agruparPorOP(refugos);
  const sapOP = agruparPorOP(sap);

  // 2) analisa TODA OP da janela (o pool de sobras alimenta a deteccao de OP trocada)
  const todas = unicos(chavesMap(lancesOP).concat(chavesMap(refOP), chavesMap(sapOP)));
  const analise = new Map<string, AnaliseOP>();
  for (const op of todas) {
    analise.set(op, analisarOP(op, lancesOP.get(op) || [], refOP.get(op) || [], sapOP.get(op) || [], pnPorOP.get(op) || "", tol));
  }
  // OP trocada: sobra de lance do GMS numa OP casa com sobra de doc SAP de outra OP
  const poolSap = new Map<string, DocSap[]>();
  for (const a of valoresMap(analise)) { for (const s of a.us) { const k = chaveQ(s.q); const l = poolSap.get(k); if (l) { l.push(s); } else { poolSap.set(k, [s]); } } }
  const poolGms = new Map<string, Lance[]>();
  for (const a of valoresMap(analise)) { for (const l of a.ug) { const k = chaveQ(l.q); const x = poolGms.get(k); if (x) { x.push(l); } else { poolGms.set(k, [l]); } } }
  for (const a of valoresMap(analise)) {
    if (Math.abs(a.dif) <= tol) { continue; }
    if (a.ug.length) { a.provavel = melhorCandidato(a.op, a.pn, a.ug.map(l => ({ q: l.q, dia: l.dia })), poolSap, pnPorOP); }
    if (!a.provavel && a.us.length) { a.provavel = melhorCandidato(a.op, a.pn, a.us.map(s => ({ q: s.q, dia: s.dia })), poolGms, pnPorOP); }
  }

  for (const a of valoresMap(analise)) { a.refGraca = soma(a.ur.filter(r => prazoRefugo(r.dia) > d).map(r => r.q)); }

  // 3) packing × GMS (global, por PN + metragem + tempo)
  casarPacking(slices, lances, pnPorOP, sap);
  const packingPorOP = new Map<string, number>();
  for (const s of slices) { if (s.opCasada) { packingPorOP.set(s.opCasada, (packingPorOP.get(s.opCasada) || 0) + s.q); } }

  // 4) escopo do dia: atividade em D (GMS, SAP ou packing) + tudo que esta aberto na lista
  const abertos = new Map<string, Aberto>();
  for (const a of abertosIn) {
    const k = txt(pega(a.chave, a.Title)).trim();
    if (k) { abertos.set(k, { chave: k, id: Number(pega(a.id, a.ID)) || 0, status: txt(pega(a.status, a.Status)), categoria: txt(pega(a.categoria, a.Categoria)) }); }
  }
  const escopo = new Set<string>();
  for (const l of lances) { if (diaCobranca(l.dia) === d) { escopo.add(l.op); } }
  for (const r of refugos) { if (diaCobranca(r.dia) === d) { escopo.add(r.op); } }
  for (const s of sap) { if (diaCobranca(s.dia) === d) { escopo.add(s.op); } }
  for (const s of slices) { if (diaCobranca(s.dia) === d && s.opCasada) { escopo.add(s.opCasada); } }
  // prazo do refugo vencendo hoje: o lote de lancamento do SAP desse refugo e D
  for (const r of refugos) { if (prazoRefugo(r.dia) === d) { escopo.add(r.op); } }
  for (const k of chavesMap(abertos)) { if (!k.startsWith("PL ")) { escopo.add(k); } }

  const itens: ItemConferencia[] = [];
  let conferidas = 0;
  let metros = 0;
  let refAguardando = 0;
  const diaMinPack = somaDias(d, -PACK_JANELA_DIAS);

  for (const op of chavesSet(escopo)) {
    const a = analise.get(op);
    const ab = abertos.get(op);
    if (!a) {
      // aberto que saiu da janela de leitura: nao da para reconferir, mantem como esta
      continue;
    }
    conferidas++;
    refAguardando += a.refGraca;
    const cat = classificar(a, tol);
    const pack = packingPorOP.get(op) || 0;
    let catFinal = cat;
    let detalhe = cat ? detalharOP(a, cat) : "";
    if (!cat) {
      // GMS x SAP ok: cobra packing de lance cujo dia de cobranca ja chegou
      const semPack = (lancesOP.get(op) || []).filter(l => !l.slice && l.dia >= diaMinPack && diaCobranca(l.dia) <= d);
      if (semPack.length) {
        catFinal = CAT.SEM_PACK;
        detalhe = "Lances sem packing: " + listar(semPack.map(l => fmt(l.q) + " m (" + dm(l.dia) + " " + hm(l.t) + ", Id " + l.id + ")"), 6);
      }
    }
    if (catFinal) {
      if (catFinal.prio <= 10) { metros += Math.abs(a.dif - a.refGraca); }
      const it = montarItem(op, ab, a, catFinal, detalhe, pack, d, "Aberto");
      if (catFinal.prio > 10) { it.difM = 0; }
      itens.push(it);
    } else if (ab) {
      itens.push(montarItem(op, ab, a, { nome: ab.categoria || "Conforme", prio: 99, acao: "", quem: "" },
        "Conferido em " + dm(d) + ": GMS e SAP batem.", pack, d, "Resolvido"));
    }
  }

  // 5) packing sem par (slices de D) e romaneio duplicado
  const romaneios = new Map<number, Slice[]>();
  for (const s of slices) { const r = romaneios.get(s.id); if (r) { r.push(s); } else { romaneios.set(s.id, [s]); } }
  const plFeitos = new Set<string>();
  for (const id of chavesMap(romaneios)) {
    const ss = romaneios.get(id) || [];
    const pns = unicos(ss.map(s => s.pn));
    const t0 = Math.min(...ss.map(s => s.t)), t1 = Math.max(...ss.map(s => s.t));
    if (pns.length < 2 && t1 - t0 <= MIN_H) { continue; }
    const chave = "PL " + id;
    if (!ss.some(s => s.dia === d) && !abertos.has(chave)) { continue; }
    plFeitos.add(chave);
    const grupos = pns.map(pn => { const g = ss.filter(s => s.pn === pn); return pn + " (" + g.length + " lances, " + fmt(soma(g.map(s => s.q))) + " m, " + dm(g[0].dia) + " " + hm(g[0].t) + ")"; });
    itens.push(itemPacking(chave, abertos.get(chave), ss, CAT.PACK_ID, "O ID " + id + " foi usado em mais de um romaneio: " + grupos.join(" e "), d));
  }
  const assinatura = new Map<string, number[]>();
  for (const id of chavesMap(romaneios)) {
    const ss = romaneios.get(id) || [];
    const sig = ss[0].pn + "|" + ss.map(s => s.q.toFixed(1)).sort().join(";");
    const l = assinatura.get(sig); if (l) { l.push(id); } else { assinatura.set(sig, [id]); }
  }
  for (const ids of valoresMap(assinatura)) {
    if (ids.length < 2) { continue; }
    ids.sort((x, y) => x - y);
    for (let i = 1; i < ids.length; i++) {
      const ss = romaneios.get(ids[i]) || [];
      const chave = "PL " + ids[i];
      if (plFeitos.has(chave) || !ss.length || (ss[0].dia !== d && !abertos.has(chave))) { continue; }
      plFeitos.add(chave);
      itens.push(itemPacking(chave, abertos.get(chave), ss, CAT.PACK_DUP,
        "Romaneio " + ids[i] + " repete o romaneio " + ids[0] + " (mesmo PN, mesmos " + ss.length + " lances, " + fmt(soma(ss.map(s => s.q))) + " m)", d));
    }
  }
  for (const id of chavesMap(romaneios)) {
    const ss = romaneios.get(id) || [];
    const chave = "PL " + id;
    if (plFeitos.has(chave)) { continue; }
    const doDia = ss[0].dia === d;
    const ab = abertos.get(chave);
    if (!doDia && !ab) { continue; }
    const sem = ss.filter(s => s.casou !== "GMS");
    if (sem.length) {
      const txt = sem.map(s => "lance " + s.sl + " " + fmt(s.q) + " m" +
        (s.casou === "GMS~" ? " (no GMS está " + fmt(s.q - s.difQ) + " m, OP " + s.opCasada + ")" :
          s.casou === "SAP" ? " (está no SAP na OP " + s.opCasada + ", não no GMS)" : " sem par"));
      itens.push(itemPacking(chave, ab, ss, CAT.PACK_SEM_GMS, "Romaneio " + id + " " + ss[0].pn + ": " + listar(txt, 8), d));
    } else if (ab) {
      itens.push(itemPacking(chave, ab, ss, { nome: ab.categoria, prio: 99, acao: "", quem: "" }, "Conferido em " + dm(d) + ": romaneio bate com o GMS.", d, "Resolvido"));
    }
  }
  // aberto de packing cujo romaneio sumiu (cancelado) = resolvido
  for (const k of chavesMap(abertos)) {
    const ab = abertos.get(k) as Aberto;
    if (k.startsWith("PL ") && !romaneios.has(Number(k.substring(3)))) {
      itens.push({
        chave: k, idLista: Number(ab.id) || 0, op: "", pn: "", categoria: ab.categoria || "", prioridade: 99, status: "Resolvido",
        gmsM: 0, refugoGmsM: 0, sapM: 0, packingM: 0, difM: 0, provavelOP: "",
        detalhe: "Conferido em " + dm(d) + ": romaneio cancelado ou fora do Packing.", acao: "", quemResolve: "", cabine: "", dataRef: d, corpoSP: "", corpoSPNovo: ""
      });
    }
  }

  // corpo pronto para o "Enviar uma solicitação HTTP ao SharePoint" (lista Conferencia_SAP).
  // Data só-data vai ao meio-dia UTC para nunca cair no dia anterior no fuso de Brasília.
  // Tratativa, Responsavel e DataTratativa são da tela: o fluxo nunca escreve neles.
  for (const it of itens) {
    const campos: { [k: string]: string | number } = {
      Title: it.chave, OP: it.op, PN: it.pn, Categoria: it.categoria, Prioridade: it.prioridade, Status: it.status,
      DataRef: it.dataRef + "T12:00:00Z", GMS_m: it.gmsM, Refugo_m: it.refugoGmsM, SAP_m: it.sapM, Packing_m: it.packingM,
      Dif_m: it.difM, ProvavelOP: it.provavelOP, Detalhe: it.detalhe, Acao: it.acao.substring(0, 255),
      QuemResolve: it.quemResolve, Cabine: it.cabine
    };
    it.corpoSP = JSON.stringify(campos);
    campos["DataDeteccao"] = it.dataRef + "T12:00:00Z";
    it.corpoSPNovo = JSON.stringify(campos);
  }
  itens.sort((x, y) => (x.status === "Resolvido" ? 1 : 0) - (y.status === "Resolvido" ? 1 : 0) || x.prioridade - y.prioridade || Math.abs(y.difM) - Math.abs(x.difM));
  const abertosHoje = itens.filter(i => i.status !== "Resolvido");
  const resolvidos = itens.filter(i => i.status === "Resolvido").length;
  const mb51Ok = sap.some(s => s.dia === d) || diaSemana(d) === 0;
  packingSemDia = lances.some(l => l.dia === d) && !slices.some(s => s.dia === d || s.dia === somaDias(d, 1));
  const ncOP = abertosHoje.filter(i => i.prioridade <= 10).length;
  const res: Resultado = {
    assunto: "Conferência GMS × SAP × Packing " + dm(d) + " — " + (abertosHoje.length ? abertosHoje.length + " pendência(s)" : "tudo conforme") +
      (mb51Ok ? "" : " — MB51 SEM LANÇAMENTO NO DIA"),
    html: "",
    dataRef: d,
    mb51Atualizado: mb51Ok,
    opsConferidas: conferidas,
    naoConformes: ncOP,
    resolvidos: resolvidos,
    metrosEmJogo: arred(metros),
    refugoAguardandoM: arred(refAguardando),
    itens: itens
  };
  res.html = montarHtml(res, sap, d);
  return res;
}

function analisarOP(op: string, ls: Lance[], rs: Refugo[], ss: DocSap[], pn: string, tol: number): AnaliseOP {
  const docs = ss.map(s => s);
  // estorno 102 anula o 101 de mesma metragem
  for (const neg of docs.filter(s => s.q < 0)) {
    const par = docs.find(p => !p.usado && p.q > 0 && Math.abs(p.q + neg.q) <= TOL_LANCE && p.dia <= neg.dia);
    if (par) { par.usado = true; par.papel = "estornado"; neg.usado = true; neg.papel = "estorno"; }
  }
  // lance aprovado x doc 101 (mesma metragem, mesmo dia primeiro)
  const ord = ls.slice().sort((a, b) => a.t - b.t);
  for (const l of ord) {
    let melhor: DocSap | null = null;
    let dist = 1e9;
    for (const p of docs) {
      if (p.usado || p.q <= 0 || Math.abs(p.q - l.q) > TOL_LANCE) { continue; }
      const dd = Math.abs(difDias(p.dia, l.dia));
      if (dd < dist) { dist = dd; melhor = p; }
    }
    if (melhor) { melhor.usado = true; melhor.papel = "lance"; l.usado = true; }
  }
  // sobra do SAP x refugo do GMS
  let sobra = docs.filter(p => !p.usado);
  for (const r of rs) {
    const p = sobra.find(x => !x.usado && Math.abs(x.q - r.q) <= TOL_LANCE);
    if (p) { p.usado = true; p.papel = "refugo"; r.usado = true; }
  }
  // SAP costuma lancar o refugo SOMADO (ex.: 5,4 m = 4,5 + 0,9): casa doc com subconjunto do refugo
  sobra = docs.filter(p => !p.usado && p.q > 0).sort((a, b) => b.q - a.q);
  for (const p of sobra) {
    const sub = subconjunto(p.q, rs.filter(r => !r.usado));
    if (sub) { p.usado = true; p.papel = "refugo"; sub.forEach(r => r.usado = true); }
  }
  sobra = docs.filter(p => !p.usado);
  let refRest = rs.filter(r => !r.usado);
  if (refRest.length && sobra.length && Math.abs(soma(sobra.map(p => p.q)) - soma(refRest.map(r => r.q))) <= tol) {
    sobra.forEach(p => { p.usado = true; p.papel = "refugo"; });
    refRest.forEach(r => r.usado = true);
  }
  sobra = docs.filter(p => !p.usado);
  refRest = rs.filter(r => !r.usado);
  // duplicidade: sobra igual a refugo ja casado
  const refQs = docs.filter(p => p.papel === "refugo").map(p => p.q).concat(rs.map(r => r.q));
  const dup = sobra.filter(p => p.q > 0 && refQs.some(q => Math.abs(q - p.q) <= TOL_LANCE));
  const us = sobra.filter(p => dup.indexOf(p) < 0);
  const g = soma(ls.map(l => l.q));
  const r = soma(rs.map(x => x.q));
  const s = soma(ss.map(x => x.q));
  const cabs = ls.map(l => l.cab).filter(c => c);
  return {
    op: op, pn: pn, gms: arred(g), ref: arred(r), sap: arred(s), dif: arred(g + r - s),
    ug: ls.filter(l => !l.usado), us: us, ur: refRest, dup: dup,
    temSap: ss.length > 0, temGms: ls.length + rs.length > 0,
    cab: cabs.length ? cabs[cabs.length - 1].replace("CABINE_", "") : "", provavel: "", refGraca: 0
  };
}

function classificar(a: AnaliseOP, tol: number): Categoria | null {
  if (Math.abs(a.dif - a.refGraca) <= tol) { return null; }   // so falta refugo ainda no prazo
  if (!a.temSap) { return a.provavel ? CAT.OP_ERRADA : CAT.GMS_SEM_SAP; }
  if (!a.temGms) { return CAT.SAP_SEM_GMS; }
  if (a.provavel && (a.ug.length > 0 || a.us.length > 0)) { return CAT.LANCE_OP_ERRADA; }
  if (a.ug.length && a.us.length) { return CAT.METRAGEM; }
  if (a.us.length) { return CAT.SAP_LANCE; }
  if (a.ug.length) { return CAT.GMS_LANCE; }
  if (a.dup.length || a.dif < 0) { return CAT.REF_MAIS; }
  if (a.ur.length > 0 || a.dif > 0) { return CAT.REF_FALTA; }
  return CAT.OUTRA;
}

function detalharOP(a: AnaliseOP, c: Categoria): string {
  const partes: string[] = [];
  const dif = (a.dif > 0 ? "+" : "") + fmt(a.dif) + " m";
  partes.push("GMS " + fmt(a.gms) + " + refugo " + fmt(a.ref) + " × SAP " + fmt(a.sap) + " (" + dif + ")");
  if (a.provavel) { partes.push("Provável OP: " + a.provavel); }
  if (a.ug.length) { partes.push("No GMS e não no SAP: " + listar(a.ug.map(l => fmt(l.q) + " m (" + dm(l.dia) + " " + hm(l.t) + ", Id " + l.id + ")"), 6)); }
  if (a.us.length) { partes.push("No SAP e não no GMS: " + listar(a.us.map(s => fmt(s.q) + " m (doc " + s.doc + ", " + dm(s.dia) + ", " + s.user + ")"), 6)); }
  if (a.dup.length) { partes.push("Refugo repetido no SAP: " + listar(a.dup.map(s => fmt(s.q) + " m (doc " + s.doc + ", " + dm(s.dia) + ", " + s.user + ")"), 6)); }
  if (a.ur.length) { partes.push("Refugo do GMS sem lançamento: " + listar(a.ur.map(r => fmt(r.q) + " m " + r.cod.substring(0, 1) + " (" + dm(r.dia) + ")"), 6)); }
  if (a.refGraca) { partes.push(fmt(a.refGraca) + " m desse refugo ainda está no prazo de lançamento do SAP"); }
  return partes.join(" | ");
}

function montarItem(op: string, ab: Aberto | undefined, a: AnaliseOP, c: Categoria, detalhe: string, pack: number, d: string, status: string): ItemConferencia {
  const st = status === "Resolvido" ? "Resolvido" : (ab && ab.status === "Justificado" ? "Justificado" : "Aberto");
  return {
    chave: op, idLista: ab ? Number(ab.id) || 0 : 0, op: op, pn: a.pn, categoria: c.nome, prioridade: c.prio, status: st,
    gmsM: a.gms, refugoGmsM: a.ref, sapM: a.sap, packingM: arred(pack), difM: a.dif, provavelOP: a.provavel,
    detalhe: detalhe, acao: c.acao, quemResolve: c.quem, cabine: a.cab, dataRef: d, corpoSP: "", corpoSPNovo: ""
  };
}

function itemPacking(chave: string, ab: Aberto | undefined, ss: Slice[], c: Categoria, detalhe: string, d: string, status: string = "Aberto"): ItemConferencia {
  const ops = unicos(ss.map(s => s.opCasada).filter(o => o));
  const st = status === "Resolvido" ? "Resolvido" : (ab && ab.status === "Justificado" ? "Justificado" : "Aberto");
  return {
    chave: chave, idLista: ab ? Number(ab.id) || 0 : 0, op: ops.join(" "), pn: ss.length ? ss[0].pn : "", categoria: c.nome, prioridade: c.prio,
    status: st, gmsM: 0, refugoGmsM: 0, sapM: 0, packingM: arred(soma(ss.map(s => s.q))), difM: 0, provavelOP: "",
    detalhe: detalhe, acao: c.acao, quemResolve: c.quem, cabine: "", dataRef: d, corpoSP: "", corpoSPNovo: ""
  };
}

/** Candidato = OP do MESMO PN que tem, na sobra do outro sistema, lances de mesma metragem (±1 dia). */
function melhorCandidato<T extends { op: string; q: number; dia: string }>(op: string, pn: string, alvo: { q: number; dia: string }[], pool: Map<string, T[]>, pnPorOP: Map<string, string>): string {
  const votos = new Map<string, number>();
  for (const x of alvo) {
    const usados = new Set<string>();
    for (const c of pool.get(chaveQ(x.q)) || []) {
      if (c.op === op || usados.has(c.op) || Math.abs(difDias(c.dia, x.dia)) > 1) { continue; }
      const pnC = pnPorOP.get(c.op) || "";
      if (pn && pnC && pn !== pnC) { continue; }
      usados.add(c.op);
      votos.set(c.op, (votos.get(c.op) || 0) + 1);
    }
  }
  let melhor = "";
  let n = 0;
  votos.forEach((v, o) => { if (v > n) { n = v; melhor = o; } });
  return n >= Math.max(1, Math.ceil(alvo.length / 2)) ? melhor : "";
}

function casarPacking(slices: Slice[], lances: Lance[], pnPorOP: Map<string, string>, sap: DocSap[]): void {
  const idx = new Map<string, Lance[]>();
  for (const l of lances) {
    const pn = pnPorOP.get(l.op) || "";
    if (!pn) { continue; }
    const k = pn + "|" + chaveQ(l.q);
    const a = idx.get(k); if (a) { a.push(l); } else { idx.set(k, [l]); }
  }
  const ordem = slices.slice().sort((a, b) => a.t - b.t);
  const dentro = (s: Slice, l: Lance) => s.t - l.t <= PACK_ANTES_H * MIN_H && l.t - s.t <= PACK_DEPOIS_H * MIN_H;
  // 1a passada: metragem exata
  for (const s of ordem) {
    let melhor: Lance | null = null;
    for (const l of idx.get(s.pn + "|" + chaveQ(s.q)) || []) {
      if (l.slice || !dentro(s, l)) { continue; }
      if (!melhor || Math.abs(s.t - l.t) < Math.abs(s.t - melhor.t)) { melhor = l; }
    }
    if (melhor) { melhor.slice = s.id + "/" + s.sl; s.casou = "GMS"; s.opCasada = melhor.op; }
  }
  // 2a passada: mesma peca com metragem digitada diferente (ate 1 m)
  const porPN = new Map<string, Lance[]>();
  for (const l of lances) {
    if (l.slice) { continue; }
    const pn = pnPorOP.get(l.op) || "";
    const a = porPN.get(pn); if (a) { a.push(l); } else { porPN.set(pn, [l]); }
  }
  for (const s of ordem) {
    if (s.casou) { continue; }
    let melhor: Lance | null = null;
    for (const l of porPN.get(s.pn) || []) {
      if (l.slice || !dentro(s, l) || Math.abs(l.q - s.q) > 1) { continue; }
      if (!melhor || Math.abs(l.q - s.q) < Math.abs(melhor.q - s.q)) { melhor = l; }
    }
    if (melhor) { melhor.slice = s.id + "/" + s.sl; s.casou = "GMS~"; s.opCasada = melhor.op; s.difQ = arred(s.q - melhor.q); }
  }
  // 3a passada: achou no SAP (OP sem apontamento no GMS)
  const sapIdx = new Map<string, DocSap[]>();
  for (const p of sap) { if (p.q > 0) { const k = p.pn + "|" + chaveQ(p.q); const a = sapIdx.get(k); if (a) { a.push(p); } else { sapIdx.set(k, [p]); } } }
  for (const s of ordem) {
    if (s.casou) { continue; }
    const p = (sapIdx.get(s.pn + "|" + chaveQ(s.q)) || []).find(x => Math.abs(difDias(x.dia, s.dia)) <= 1);
    if (p) { s.casou = "SAP"; s.opCasada = p.op; }
  }
}

// ───────────────────────── e-mail ─────────────────────────

function montarHtml(r: Resultado, sap: DocSap[], d: string): string {
  const C = { header: "#1E293B", fundo: "#F5F7FA", borda: "#E2E8F0", texto: "#0F172A", suave: "#64748B", ok: "#16A34A", alerta: "#E67E22", erro: "#C0392B", info: "#2C6FBF", marca: "#E2231A", erroSuave: "#FEE2E2", okSuave: "#D1FAE5", alertaSuave: "#FEF3C7" };
  const abertos = r.itens.filter(i => i.status !== "Resolvido");
  const resolvidos = r.itens.filter(i => i.status === "Resolvido");
  const conformes = r.opsConferidas - r.naoConformes;
  const pct = r.opsConferidas ? Math.round(100 * conformes / r.opsConferidas) : 100;
  const metrosSapDia = soma(sap.filter(s => s.dia === d).map(s => s.q));
  const td = "padding:6px 8px;border-bottom:1px solid " + C.borda + ";font-size:12px;vertical-align:top;";
  const kpi = (rot: string, val: string, cor: string) =>
    "<td style=\"padding:10px 14px;background:#FFFFFF;border:1px solid " + C.borda + ";\"><div style=\"font-size:11px;color:" + C.suave + ";\">" + rot +
    "</div><div style=\"font-size:24px;font-weight:bold;color:" + cor + ";\">" + val + "</div></td>";
  let h = "<div style=\"font-family:Segoe UI,Arial,sans-serif;color:" + C.texto + ";background:" + C.fundo + ";padding:12px;\">";
  h += "<table cellpadding=\"0\" cellspacing=\"0\" width=\"100%\" style=\"border-collapse:collapse;\"><tr><td style=\"background:" + C.header + ";color:#FFFFFF;padding:12px 14px;border-left:6px solid " + C.marca + ";\">" +
    "<div style=\"font-size:18px;font-weight:bold;\">Conferência GMS × SAP × Packing</div><div style=\"font-size:12px;color:#CBD5E1;\">" +
    nomeDia(d) + ", " + dm(d) + "/" + d.substring(0, 4) + " · MB51 com " + fmt(metrosSapDia) + " m lançados no dia</div></td></tr></table>";
  if (!r.mb51Atualizado) {
    h += "<p style=\"background:" + C.erroSuave + ";color:" + C.erro + ";padding:8px 10px;font-weight:bold;\">O MB51 não tem nenhum lançamento em " + dm(d) +
      ". A extração da manhã rodou? Sem o MB51 do dia, toda OP do GMS aparece como \"SAP não lançou\".</p>";
  }
  h += "<table cellpadding=\"0\" cellspacing=\"6\" width=\"100%\" style=\"margin-top:8px;\"><tr>" +
    kpi("OPs conferidas", String(r.opsConferidas), C.texto) +
    kpi("Conformes", conformes + " (" + pct + "%)", C.ok) +
    kpi("Não conformes (GMS × SAP)", String(r.naoConformes), r.naoConformes ? C.erro : C.ok) +
    kpi("Metros em jogo", fmt(r.metrosEmJogo) + " m", r.metrosEmJogo ? C.alerta : C.ok) +
    kpi("Resolvidas hoje", String(r.resolvidos), C.info) + "</tr></table>";
  if (packingSemDia) {
    h += "<p style=\"background:" + C.erroSuave + ";color:" + C.erro + ";padding:8px 10px;font-weight:bold;\">O Packing List não tem nenhum romaneio em " + dm(d) +
      ", mas o GMS tem lances aprovados no dia. O arquivo foi salvo? Todo lance do dia aparece como \"sem packing\".</p>";
  }
  if (!abertos.length) {
    h += "<p style=\"background:" + C.okSuave + ";color:" + C.ok + ";padding:10px;font-weight:bold;\">Tudo conforme: cada lance do GMS está no SAP e no Packing.</p>";
  }
  const grupos = new Map<string, ItemConferencia[]>();
  for (const i of abertos) { const g = grupos.get(i.categoria); if (g) { g.push(i); } else { grupos.set(i.categoria, [i]); } }
  for (const cat of chavesMap(grupos)) {
    const its = grupos.get(cat) || [];
    const cor = its[0].prioridade <= 5 ? C.erro : its[0].prioridade <= 10 ? C.alerta : C.info;
    h += "<div style=\"margin-top:14px;border-left:4px solid " + cor + ";padding-left:8px;\"><div style=\"font-size:14px;font-weight:bold;\">" + esc(cat) +
      " <span style=\"color:" + cor + ";\">(" + its.length + ")</span></div><div style=\"font-size:11px;color:" + C.suave + ";\">O que fazer: " + esc(its[0].acao) +
      " · Quem resolve: " + esc(its[0].quemResolve) + "</div></div>";
    h += "<table cellpadding=\"0\" cellspacing=\"0\" width=\"100%\" style=\"border-collapse:collapse;background:#FFFFFF;margin-top:4px;\"><tr style=\"background:" + C.header + ";color:#FFFFFF;font-size:11px;\">" +
      ["OP / romaneio", "PN", "GMS", "Refugo", "SAP", "Packing", "Dif.", "Detalhe"].map(x => "<td style=\"padding:5px 8px;\">" + x + "</td>").join("") + "</tr>";
    for (const i of its) {
      const nums = i.prioridade <= 10 || i.prioridade === 13;
      h += "<tr><td style=\"" + td + "font-weight:bold;white-space:nowrap;\">" + esc(i.chave) + (i.status === "Justificado" ? "<br><span style=\"font-weight:normal;color:" + C.suave + ";\">justificado</span>" : "") +
        "</td><td style=\"" + td + "white-space:nowrap;\">" + esc(i.pn) + "</td>" +
        "<td style=\"" + td + "text-align:right;\">" + (nums ? fmt(i.gmsM) : "") + "</td>" +
        "<td style=\"" + td + "text-align:right;\">" + (nums ? fmt(i.refugoGmsM) : "") + "</td>" +
        "<td style=\"" + td + "text-align:right;\">" + (nums ? fmt(i.sapM) : "") + "</td>" +
        "<td style=\"" + td + "text-align:right;\">" + (i.packingM ? fmt(i.packingM) : "") + "</td>" +
        "<td style=\"" + td + "text-align:right;font-weight:bold;color:" + (i.difM ? cor : C.suave) + ";\">" + (i.prioridade <= 10 ? (i.difM > 0 ? "+" : "") + fmt(i.difM) : "") + "</td>" +
        "<td style=\"" + td + "\">" + esc(i.detalhe) + "</td></tr>";
    }
    h += "</table>";
  }
  if (r.refugoAguardandoM > 0) {
    h += "<p style=\"font-size:12px;color:" + C.suave + ";margin-top:12px;\">" + fmt(r.refugoAguardandoM) + " m de refugo apontado no GMS ainda não está no SAP, " +
      "mas está dentro do prazo do lote (seg→ter, ter/qua→qui, qui→sex, sex/sáb→seg). Só vira pendência se passar do prazo.</p>";
  }
  if (resolvidos.length) {
    h += "<div style=\"margin-top:14px;font-size:13px;font-weight:bold;color:" + C.ok + ";\">Resolvidas desde a última conferência (" + resolvidos.length + ")</div><div style=\"font-size:12px;color:" + C.suave + ";\">" +
      esc(resolvidos.map(i => i.chave + " (" + i.categoria + ")").join(" · ")) + "</div>";
  }
  h += "<p style=\"font-size:11px;color:" + C.suave + ";margin-top:16px;\">Tratativa no GMS: Gestão → Conferência SAP. Regra: GMS aprovado + refugo = SAP 101−102 (unidade M, GRT4), tolerância " +
    "0,5 m por OP; refugo cobrado no dia do lote do SAP (seg→ter, ter/qua→qui, qui→sex, sex/sáb→seg; refugo não vai para o packing); lance aprovado no SAP e packing cobrados no mesmo dia (3º turno pode virar o dia; sábado é cobrado na segunda). Gerado pelo fluxo GMS_Conferencia_Diaria.</p></div>";
  return h;
}

// ───────────────────────── utilitarios ─────────────────────────

function num(v: string | number | boolean | null | undefined): number {
  if (typeof v === "number") { return isFinite(v) ? v : 0; }
  if (v === null || v === undefined || typeof v === "boolean") { return 0; }
  let s = String(v).trim();
  if (!s) { return 0; }
  if (s.indexOf(",") >= 0 && s.indexOf(".") < 0) { s = s.replace(",", "."); } else { s = s.replace(/,/g, ""); }
  const n = parseFloat(s);
  return isFinite(n) ? n : 0;
}
/** 0/1 knapsack em decimos de metro: subconjunto do refugo cuja soma bate com o doc (±0,1 m). */
function subconjunto(alvo: number, rs: Refugo[]): Refugo[] | null {
  const T = Math.round(alvo * 10) + 1;
  if (rs.length === 0 || rs.length > 60 || T > 30000 || alvo <= 0) { return null; }
  const w = rs.map(r => Math.round(r.q * 10));
  const de = new Array<number>(T + 1).fill(-2);
  const item = new Array<number>(T + 1).fill(-1);
  de[0] = -1;
  for (let i = 0; i < w.length; i++) {
    if (w[i] <= 0 || w[i] > T) { continue; }
    for (let s = T; s >= w[i]; s--) {
      if (de[s] === -2 && de[s - w[i]] !== -2) { de[s] = s - w[i]; item[s] = i; }
    }
  }
  const base = Math.round(alvo * 10);
  for (const s of [base, base - 1, base + 1]) {
    if (s <= 0 || s > T || de[s] === -2) { continue; }
    const out: Refugo[] = [];
    let k = s;
    while (k > 0) { out.push(rs[item[k]]); k = de[k]; }
    return out;
  }
  return null;
}
/** Map/Set -> array sem iterador (o runtime do Office Script e ES5: for-of em Map itera zero vezes). */
function chavesMap<K, V>(m: Map<K, V>): K[] { const out: K[] = []; m.forEach((_v, k) => { out.push(k); }); return out; }
function valoresMap<K, V>(m: Map<K, V>): V[] { const out: V[] = []; m.forEach(v => { out.push(v); }); return out; }
function chavesSet<T>(st: Set<T>): T[] { const out: T[] = []; st.forEach(v => { out.push(v); }); return out; }
function unicos(xs: string[]): string[] { const vis: { [k: string]: boolean } = {}; const out: string[] = []; for (const x of xs) { if (!vis[x]) { vis[x] = true; out.push(x); } } return out; }
function agruparPorOP<T extends { op: string }>(xs: T[]): Map<string, T[]> {
  const m = new Map<string, T[]>();
  for (const x of xs) { const a = m.get(x.op); if (a) { a.push(x); } else { m.set(x.op, [x]); } }
  return m;
}
function arred(n: number): number { return Math.round(n * 100) / 100; }
function soma(xs: number[]): number { let t = 0; for (const x of xs) { t += x; } return arred(t); }
function chaveQ(q: number): string { return String(Math.round(q * 10)); }
function limpo(s: string | null | undefined): string { return s ? String(s).trim() : ""; }
function textoOP(v: string | number | boolean | null | undefined): string {
  if (v === null || v === undefined) { return ""; }
  const s = String(v).trim().replace(/\.0+$/, "");
  return /^\d{6,}$/.test(s) ? s : "";
}
function normPN(s: string | null | undefined): string { return s ? String(s).trim().toUpperCase().replace(/\s+/g, "") : ""; }
function fmt(n: number): string {
  const neg = n < 0;
  const v = Math.abs(Math.round(n * 10) / 10);
  const inteiro = Math.floor(v);
  const dec = Math.round((v - inteiro) * 10);
  const milhar = String(inteiro).replace(/\B(?=(\d{3})+(?!\d))/g, ".");
  return (neg ? "-" : "") + milhar + "," + dec;
}
function esc(s: string): string { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"); }
function listar(xs: string[], max: number): string { return xs.length <= max ? xs.join("; ") : xs.slice(0, max).join("; ") + " e mais " + (xs.length - max); }

/** ISO do SharePoint (UTC, com Z) -> instante "local" (ms, relogio de Brasilia tratado como UTC). */
function instanteUTC(iso: string): number {
  if (!iso) { return 0; }
  const s = String(iso).trim();
  const tem = /Z$|[+-]\d\d:?\d\d$/.test(s);
  const t = Date.parse(tem ? s : s + "Z");
  return isNaN(t) ? 0 : t + FUSO_H * MIN_H * (tem ? 1 : 0);
}
/** Data/hora que ja vem no relogio local (packing) -> mesmo eixo de instanteUTC. */
function instanteLocal(iso: string): number {
  if (!iso) { return 0; }
  const s = String(iso).trim().replace(" ", "T").replace(/Z$/, "");
  const t = Date.parse(s + "Z");
  return isNaN(t) ? 0 : t;
}
function agoraLocal(): number { return Date.now() + FUSO_H * MIN_H; }
function diaDe(t: number): string { return new Date(t).toISOString().substring(0, 10); }
function hm(t: number): string { return new Date(t).toISOString().substring(11, 16); }
function somaDias(dia: string, n: number): string { return diaDe(Date.parse(dia + "T00:00:00Z") + n * 24 * MIN_H); }
function difDias(a: string, b: string): number { return Math.round((Date.parse(a + "T00:00:00Z") - Date.parse(b + "T00:00:00Z")) / (24 * MIN_H)); }
/** Dia em que o lance passa a ser cobrado: sabado e domingo vao para segunda (3o turno de sabado termina na segunda). */
function diaCobranca(dia: string): string { const w = diaSemana(dia); return w === 6 ? somaDias(dia, 2) : w === 0 ? somaDias(dia, 1) : dia; }
/** Dia do lote de refugo no SAP: seg->ter, ter->qui, qua->qui, qui->sex, sex->seg, sab->seg, dom->seg. */
function prazoRefugo(dia: string): string { return somaDias(dia, [1, 1, 2, 1, 1, 3, 2][diaSemana(dia)]); }
/** Conferencia padrao: dia util anterior (seg–sex). Rodando seg/dom, confere a sexta. */
function diaUtilAnterior(hoje: string): string { let x = somaDias(hoje, -1); while (diaSemana(x) === 0 || diaSemana(x) === 6) { x = somaDias(x, -1); } return x; }
function diaSemana(dia: string): number { return new Date(dia + "T00:00:00Z").getUTCDay(); }
function nomeDia(dia: string): string { return ["domingo", "segunda", "terça", "quarta", "quinta", "sexta", "sábado"][diaSemana(dia)]; }
function dm(dia: string): string { return dia.substring(8, 10) + "/" + dia.substring(5, 7); }
function serialDe(dia: string): number { return Math.round(Date.parse(dia + "T00:00:00Z") / (24 * MIN_H)) + 25569; }
function diaDeSerial(serial: number): string { return diaDe((Math.floor(serial) - 25569) * 24 * MIN_H); }
function serialDeCelula(v: string | number | boolean): number {
  if (typeof v === "number") { return v; }
  const s = String(v).trim();
  let m = /^(\d{2})\.(\d{2})\.(\d{4})/.exec(s);                 // 18.09.2026 (SAP)
  if (m) { return serialDe(m[3] + "-" + m[2] + "-" + m[1]); }
  m = /^(\d{4})-(\d{2})-(\d{2})/.exec(s);
  if (m) { return serialDe(m[1] + "-" + m[2] + "-" + m[3]); }
  m = /^(\d{1,2})\/(\d{1,2})\/(\d{4})/.exec(s);                 // dd/mm/yyyy
  if (m) { return serialDe(m[3] + "-" + ("0" + m[2]).slice(-2) + "-" + ("0" + m[1]).slice(-2)); }
  return 0;
}
