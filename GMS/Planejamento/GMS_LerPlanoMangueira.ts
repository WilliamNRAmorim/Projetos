/**
 * GMS_LerPlanoMangueira  v1.0.0  (25/11/2026)  MEL-275
 * Office Script - le a aba "Plano" do PL_<MES>_Trançadeira.xlsx (somente leitura) e devolve, em JSON, SO as linhas da lista
 * GMS_PlanoMangueira que precisam mudar. Quem grava e o fluxo GMS_PlanoMangueira_Sync. Nada e escrito na planilha.
 *   Aba Plano: cabecalho na linha que tem "PN" na coluna F; B=Dash, C=Wide Braiders (tipo), D=Construction, F=PN, G="<MES> Production"
 *   (metros do mes) ate a linha TOTAL da coluna F.
 * Travas (ok=false, nada e gravado e o fluxo avisa): nome fora do padrao, ano fora da pasta, sem aba/cabecalho/TOTAL, mes do cabecalho
 *   diferente do mes do arquivo, volume que nao e numero ou negativo, PN repetido, construcao desconhecida, soma diferente do TOTAL,
 *   queda de mais de 40% sobre o total que ja esta na lista (plano salvo pela metade) e nenhuma mangueira com volume.
 * Nunca apaga: mangueira da lista que saiu do PL vai a Volume 0 e mantem a classificacao. Linha nova so se Volume > 0.
 * hoje = "yyyy-MM" (Sao Paulo). So aceita o mes atual e o seguinte; outro mes volta ok=true, ignorado=true, sem linhas.
 * existentesJson = itens da lista (ID, Title, Mes, CStandard, Tipo, Arame, Volume) de todos os meses.
 * ES5 (sem for-of em Map/Set). Retorno sempre string JSON: { ok, ignorado, erro, mes, total, totalAntes, linhas:[{id,title,mes,cstandard,tipo,arame,volume}] }
 */
interface ItemLista { ID?: number; Id?: number; Title: string; Mes: string; CStandard?: string; Tipo?: string; Arame?: string; Volume?: number; }
interface LinhaSaida { id: number; title: string; mes: string; cstandard: string; tipo: string; arame: string; volume: number; }
interface Saida { ok: boolean; ignorado: boolean; erro: string; mes: string; total: number; totalAntes: number; linhas: LinhaSaida[]; }

const MESES: string[] = ["JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"];

function texto(v: string | number | boolean | null | undefined): string {
  return String(v === undefined || v === null ? "" : v).trim();
}
function arameDe(cs: string): string {
  if (cs.indexOf("TEXTILE") === 0) { return "Textil"; }
  if (cs === "SPIRAL") { return "SPIRAL"; }
  if (cs === "DD20-04/06" || cs === "SD20-04/06") { return "Wire - 20C"; }
  if (cs === "DD24-08/10/12" || cs === "SD24-08/10/12") { return "Wire 24C"; }
  if (cs === "SD/DD36-16") { return "Wire 36C"; }
  return "";
}

function calcular(v: (string | number | boolean)[][], nomeArquivo: string, pasta: string, ex: ItemLista[], hoje: string): Saida {
  const s: Saida = { ok: false, ignorado: false, erro: "", mes: "", total: 0, totalAntes: 0, linhas: [] };
  const mNome = /^PL_([A-Z]{3})_/.exec(texto(nomeArquivo).toUpperCase());
  const iMes = mNome ? MESES.indexOf(mNome[1]) : -1;
  if (iMes < 0 || !mNome) { s.erro = "Nome fora do padrao PL_<MES>_: " + nomeArquivo; return s; }
  const anos = texto(pasta).match(/20\d\d/g);
  if (!anos) { s.erro = "Ano nao encontrado na pasta: " + pasta; return s; }
  const ano = anos[anos.length - 1];
  const chaveMes = ano + "-" + (iMes < 9 ? "0" : "") + String(iMes + 1);
  s.mes = chaveMes + "-01T03:00:00Z";
  const h = /^(20\d\d)-(\d\d)$/.exec(texto(hoje));
  if (!h) { s.erro = "Data de hoje invalida: " + hoje; return s; }
  const distancia = (Number(ano) * 12 + iMes) - (Number(h[1]) * 12 + Number(h[2]) - 1);
  if (distancia !== 0 && distancia !== 1) { s.ok = true; s.ignorado = true; return s; }

  let cab = -1;
  for (let r = 0; r < v.length && r < 10; r++) { if (texto(v[r][5]).toUpperCase() === "PN") { cab = r; break; } }
  if (cab < 0) { s.erro = "Cabecalho PN nao encontrado na coluna F da aba Plano"; return s; }
  const tituloG = texto(v[cab][6]).toUpperCase();
  if (tituloG !== mNome[1] + " PRODUCTION") { s.erro = "Coluna G diz '" + tituloG + "' e o arquivo e de " + mNome[1]; return s; }

  const porPN: { [pn: string]: LinhaSaida } = {};
  const ordem: string[] = [];
  let totalPlanilha = -1;
  for (let r = cab + 1; r < v.length; r++) {
    const pn = texto(v[r][5]);
    if (pn === "") { continue; }
    if (pn.toUpperCase() === "TOTAL") {
      if (typeof v[r][6] === "number") { totalPlanilha = v[r][6] as number; }
      break;
    }
    const bruto = v[r][6];
    if (texto(bruto) !== "" && typeof bruto !== "number") { s.erro = "Volume nao numerico em " + pn + ": " + texto(bruto); return s; }
    const vol = typeof bruto === "number" ? bruto : 0;
    if (vol < 0) { s.erro = "Volume negativo em " + pn; return s; }
    const k = pn.toUpperCase();
    if (porPN[k] !== undefined) { s.erro = "PN repetido na aba Plano: " + pn; return s; }
    let cs = texto(v[r][3]).toUpperCase();
    if (cs === "TEXTILE") { cs = Number(v[r][1]) <= 6 ? "TEXTILE-03/04/05/06" : "TEXTILE-07/08/10/12/16"; }
    const arame = arameDe(cs);
    if (arame === "" && vol > 0) { s.erro = "Construcao desconhecida em " + pn + ": " + cs; return s; }
    porPN[k] = { id: 0, title: pn, mes: s.mes, cstandard: cs, tipo: texto(v[r][2]).replace(/\s/g, ""), arame: arame, volume: vol };
    ordem.push(k);
  }
  if (totalPlanilha < 0) { s.erro = "Linha TOTAL com numero nao encontrada na aba Plano"; return s; }
  let soma = 0;
  for (let n = 0; n < ordem.length; n++) { soma += porPN[ordem[n]].volume; }
  s.total = soma;
  if (soma <= 0) { s.erro = "Nenhuma mangueira com volume"; return s; }
  if (Math.abs(soma - totalPlanilha) > 0.5) { s.erro = "Soma " + soma + " diferente do TOTAL " + totalPlanilha; return s; }

  const naLista: { [pn: string]: ItemLista } = {};
  for (let e = 0; e < ex.length; e++) {
    if (texto(ex[e].Mes).substring(0, 7) !== chaveMes) { continue; }
    const kx = texto(ex[e].Title).toUpperCase();
    if (naLista[kx] !== undefined) { s.erro = "Mangueira repetida na lista no mes: " + kx; return s; }
    naLista[kx] = ex[e];
    s.totalAntes += Number(ex[e].Volume || 0);
  }
  if (s.totalAntes > 0 && soma < s.totalAntes * 0.6) { s.erro = "Total caiu de " + s.totalAntes + " para " + soma + " (mais de 40%)"; return s; }

  for (let n = 0; n < ordem.length; n++) {
    const a = porPN[ordem[n]];
    const b = naLista[ordem[n]];
    if (b === undefined) { if (a.volume > 0) { s.linhas.push(a); } continue; }
    // mangueira que ja existe: mantem Title e Arame da lista (podem ter sido ajustados) quando a construcao nao mudou
    const mesmaClasse = texto(b.CStandard) === a.cstandard && texto(b.Tipo) === a.tipo;
    const semClasse = a.arame === "";
    if (Number(b.Volume || 0) === a.volume && (mesmaClasse || semClasse)) { continue; }
    s.linhas.push({
      id: Number(b.ID !== undefined ? b.ID : b.Id), title: b.Title, mes: s.mes,
      cstandard: semClasse ? texto(b.CStandard) : a.cstandard, tipo: semClasse ? texto(b.Tipo) : a.tipo,
      arame: mesmaClasse || semClasse ? texto(b.Arame) : a.arame, volume: a.volume
    });
  }
  const chaves = Object.keys(naLista);
  for (let c = 0; c < chaves.length; c++) {
    const x = naLista[chaves[c]];
    if (porPN[chaves[c]] === undefined && Number(x.Volume || 0) !== 0) {
      s.linhas.push({ id: Number(x.ID !== undefined ? x.ID : x.Id), title: x.Title, mes: s.mes, cstandard: texto(x.CStandard), tipo: texto(x.Tipo), arame: texto(x.Arame), volume: 0 });
    }
  }
  s.ok = true;
  return s;
}

function main(workbook: ExcelScript.Workbook, nomeArquivo: string, pasta: string, existentesJson: string, hoje: string): string {
  const aba = workbook.getWorksheet("Plano");
  if (!aba) { return JSON.stringify({ ok: false, ignorado: false, erro: "Aba Plano nao encontrada em " + nomeArquivo, mes: "", total: 0, totalAntes: 0, linhas: [] }); }
  let ex: ItemLista[] = [];
  try { ex = JSON.parse(existentesJson) as ItemLista[]; } catch (e) {
    return JSON.stringify({ ok: false, ignorado: false, erro: "Lista atual ilegivel", mes: "", total: 0, totalAntes: 0, linhas: [] });
  }
  return JSON.stringify(calcular(aba.getRangeByIndexes(0, 0, 130, 8).getValues(), nomeArquivo, pasta, ex, hoje));
}
