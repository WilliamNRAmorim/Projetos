/**
 * GMS_LimpaProdTubo  v1.0.0  (15/10/2026)
 * Office Script chamado pelo fluxo GMS_LimpaProdTubo quando a ficha da trancadeira vira Cancelado.
 * Procura a OP (8 digitos) nas abas T?.?? do PL_<MES>_Trançadeira.xlsx (coluna D) e LIMPA a coluna J (Prod. Tubo)
 * somente se ela vale exatamente "OK" (o que o GMS_MarcaProdTubo escreve). Qualquer outro valor fica como esta.
 * Quem decide se o OK foi do fluxo (e nao digitado a mao) e o fluxo: so chama este script se Plano_OPs.OKPeloGMS = Sim.
 * Devolve JSON: { limpo: bool, aba, linha, motivo }.  ES5.
 */
function main(workbook: ExcelScript.Workbook, op: string): string {
  const alvo = String(op || "").trim().split(".")[0];
  if (!/^\d{8}$/.test(alvo)) { return JSON.stringify({ limpo: false, aba: "", linha: 0, motivo: "OP invalida" }); }
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
      if (atual.toUpperCase() === "OK") { cel.clear(ExcelScript.ClearApplyTo.contents); return JSON.stringify({ limpo: true, aba: nome, linha: 5 + r, motivo: "" }); }
      return JSON.stringify({ limpo: false, aba: nome, linha: 5 + r, motivo: atual === "" ? "J ja vazia" : "J nao e OK: " + atual });
    }
  }
  return JSON.stringify({ limpo: false, aba: "", linha: 0, motivo: "OP nao encontrada neste arquivo" });
}
