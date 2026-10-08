/**
 * GMS_LerPlanoOPs  v1.1.0  (08/10/2026)
 * v1.1.0: recebe existentesJson (itens atuais de Plano_OPs: Id,Title,PN,Trancadeira,QtdPlanejada,Tipo,StatusSAP,Encerrada,Origem)
 *   e devolve SO as linhas novas (id 0) ou alteradas (id do item); o fluxo grava so essas, sem varrer 500 OPs a cada salvamento.
 *   Linha que sumiu da planilha nao e apagada (OP encerrada continua valendo como historico).
 * Office Script - le o PL_<MES>_Trançadeira.xlsx (somente leitura) e devolve as OPs validas em JSON para o fluxo
 * GMS_PlanoOPs_Sync gravar na lista Plano_OPs. Nada e escrito na planilha.
 *   Abas TE.01 TH.01..TH.07 TM.01 TM.04 TO.04: D=Ordem(OP), E=Mangueira(PN), F=Plano-Quant(m)      -> tipo Tubo,      origem Plano
 *   Aba Extrusora de Mandril:                   D=Ordem(OP), C=Mandril, E=Bitola, H=Plano-Quant    -> tipo Extrusora, origem PlanoMandril
 *   Aba COOIS (export SAP): A=Material, B=Order(OP), C=Qtd, N=System Status (TECO = encerrada)     -> tipo Tubo,      origem COOIS
 * OP so vale com 8 digitos. ES5 (sem for-of em Map/Set). mes = "OUTUBRO" (nome da aba Extrusora/Mes) ou "" para todos.
 */
interface Existente { Id: number; Title: string; PN?: string; Trancadeira?: string; QtdPlanejada?: number; Tipo?: string; StatusSAP?: string; Encerrada?: boolean; Origem?: string; }
interface OPSaida { id: number; op: string; pn: string; tr: string; mes: string; qtd: number; tipo: string; origem: string; status: string; enc: boolean; }
interface OPLinha { op: string; pn: string; tr: string; mes: string; qtd: number; tipo: string; origem: string; status: string; enc: boolean; }

function soOP(v: string | number | boolean): string {
  const s = String(v === undefined || v === null ? "" : v).trim().split(".")[0];
  return /^\d{8}$/.test(s) ? s : "";
}
function num(v: string | number | boolean): number { return typeof v === "number" ? v : 0; }

function main(workbook: ExcelScript.Workbook, mes: string, existentesJson: string): string {
  const out: OPLinha[] = [];
  const achada: { [op: string]: number } = {};   // op -> indice em out
  const alvoMes = String(mes || "").trim().toUpperCase();
  const abas = workbook.getWorksheets();
  for (let i = 0; i < abas.length; i++) {
    const nome = abas[i].getName();
    if (/^T[EHMO]\.\d\d$/.test(nome)) {
      const u = abas[i].getUsedRange(true);
      if (!u) { continue; }
      const v = abas[i].getRangeByIndexes(4, 0, Math.max(u.getRowCount() - 4, 1), 7).getValues();
      for (let r = 0; r < v.length; r++) {
        const op = soOP(v[r][3]);
        if (op === "") { continue; }
        achada[op] = out.length;
        out.push({ op: op, pn: String(v[r][4] || "").trim(), tr: nome, mes: String(v[r][1] || "").trim(), qtd: num(v[r][5]), tipo: "Tubo", origem: "Plano", status: "", enc: false });
      }
    } else if (nome === "Extrusora de Mandril") {
      const u = abas[i].getUsedRange(true);
      if (!u) { continue; }
      const v = abas[i].getRangeByIndexes(5, 0, Math.max(u.getRowCount() - 5, 1), 9).getValues();
      for (let r = 0; r < v.length; r++) {
        const op = soOP(v[r][3]);
        if (op === "") { continue; }
        const m = String(v[r][1] || "").trim().toUpperCase();
        if (alvoMes !== "" && m !== alvoMes) { continue; }
        achada[op] = out.length;
        out.push({ op: op, pn: String(v[r][4] || "").trim(), tr: String(v[r][2] || "").trim(), mes: m, qtd: num(v[r][7]), tipo: "Extrusora", origem: "PlanoMandril", status: "", enc: false });
      }
    }
  }
  const coois = workbook.getWorksheet("COOIS");
  if (coois) {
    const u = coois.getUsedRange(true);
    if (u) {
      const v = coois.getRangeByIndexes(1, 0, Math.max(u.getRowCount() - 1, 1), 14).getValues();
      for (let r = 0; r < v.length; r++) {
        const op = soOP(v[r][1]);
        if (op === "") { continue; }
        const st = String(v[r][13] || "").trim().split(/\s+/)[0];
        const idx = achada[op];
        if (idx === undefined) {
          achada[op] = out.length;
          out.push({ op: op, pn: String(v[r][0] || "").trim(), tr: "", mes: alvoMes, qtd: num(v[r][2]), tipo: "Tubo", origem: "COOIS", status: st, enc: st === "TECO" });
        } else {
          out[idx].status = st; out[idx].enc = st === "TECO";
        }
      }
    }
  }
  // so o que mudou em relacao a lista atual
  let ex: Existente[] = [];
  try { ex = JSON.parse(existentesJson || "[]") as Existente[]; } catch (e) { ex = []; }
  const porOP: { [op: string]: Existente } = {};
  for (let k = 0; k < ex.length; k++) { porOP[String(ex[k].Title)] = ex[k]; }
  const saida: OPSaida[] = [];
  for (let n = 0; n < out.length; n++) {
    const a = out[n];
    const b = porOP[a.op];
    const igual = b !== undefined && String(b.PN || "") === a.pn && String(b.Trancadeira || "") === a.tr && Number(b.QtdPlanejada || 0) === a.qtd
      && String(b.Tipo || "") === a.tipo && String(b.StatusSAP || "") === a.status && !!b.Encerrada === a.enc && String(b.Origem || "") === a.origem;
    if (!igual) { saida.push({ id: b === undefined ? 0 : b.Id, op: a.op, pn: a.pn, tr: a.tr, mes: a.mes, qtd: a.qtd, tipo: a.tipo, origem: a.origem, status: a.status, enc: a.enc }); }
  }
  return JSON.stringify(saida);
}
