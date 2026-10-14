/**
 * GMS_MarcaProdTubo  v1.0.0  (14/10/2026)
 * Office Script chamado pelo fluxo GMS_MarcaProdTubo quando a ficha da trancadeira e criada em ficha_producao.
 * Procura a OP (8 digitos) nas abas T?.?? do PL_<MES>_Trançadeira.xlsx (coluna D) e escreve "OK" na coluna J (Prod. Tubo).
 * Nao sobrescreve valor ja preenchido na J. Devolve JSON: { marcado: bool, aba, linha, motivo }.
 * ES5 (sem for-of em Map/Set).
 */
function main(workbook: ExcelScript.Workbook, op: string): string {
  const alvo = String(op || "").trim().split(".")[0];
  if (!/^\d{8}$/.test(alvo)) { return JSON.stringify({ marcado: false, aba: "", linha: 0, motivo: "OP invalida" }); }
  const abas = workbook.getWorksheets();
  for (let i = 0; i < abas.length; i++) {
    const nome = abas[i].getName();
    if (!/^T[EHMO]\.\d\d$/.test(nome)) { continue; }
    const u = abas[i].getUsedRange(true);
    if (!u) { continue; }
    const n = Math.max(u.getRowCount() - 4, 1);
    const v = abas[i].getRangeByIndexes(4, 3, n, 1).getValues();
    for (let r = 0; r < v.length; r++) {
      if (String(v[r][0] === undefined || v[r][0] === null ? "" : v[r][0]).trim().split(".")[0] !== alvo) { continue; }
      const cel = abas[i].getRangeByIndexes(4 + r, 9, 1, 1);
      const atual = String(cel.getValue() || "").trim();
      if (atual === "") { cel.setValue("OK"); return JSON.stringify({ marcado: true, aba: nome, linha: 5 + r, motivo: "" }); }
      return JSON.stringify({ marcado: false, aba: nome, linha: 5 + r, motivo: "J ja preenchida: " + atual });
    }
  }
  return JSON.stringify({ marcado: false, aba: "", linha: 0, motivo: "OP nao encontrada neste arquivo" });
}
