/**
 * GMS_LerPacking  v1.0.0  (02/10/2026)  MEL-196  C29
 * Office Script — roda pelo Power Automate em cima do "BD Packing List.xlsx" (somente leitura).
 * Devolve, em JSON, os lances (slices) do packing dos ultimos N dias para o GMS_ConferenciaDiaria.
 * Nao precisa de tabela formatada: le a aba "Data Base" pelo cabecalho.
 */

interface SlicePacking { id: number; sl: number; pn: string; q: number; ts: string; c: boolean; }

function main(workbook: ExcelScript.Workbook, janelaDias: number): string {
  const janela = janelaDias > 0 ? janelaDias : 35;
  const ws = workbook.getWorksheet("Data Base") || workbook.getWorksheets()[0];
  const usado = ws.getUsedRange(true);
  const nLin = usado.getRowCount();
  const nCol = usado.getColumnCount();
  const cab = ws.getRangeByIndexes(0, 0, 1, nCol).getValues()[0].map(v => String(v).trim());
  const col = (nome: string): number => {
    const i = cab.indexOf(nome);
    if (i < 0) { throw new Error("Packing List sem a coluna '" + nome + "'. Cabeçalho mudou?"); }
    return i;
  };
  const cId = col("ID"), cPn = col("PN"), cSl = col("Slice"), cQ = col("QTd (m)"), cTs = col("Timestamp"), cCan = col("Cancelled");
  // corte: hoje (relogio de Brasilia) menos a janela, em serial do Excel
  const hojeSerial = Math.floor((Date.now() - 3 * 3600000) / 86400000) + 25569;
  const corte = hojeSerial - janela;
  const out: SlicePacking[] = [];
  const BLOCO = 20000;
  for (let r0 = 1; r0 < nLin; r0 += BLOCO) {
    const n = Math.min(BLOCO, nLin - r0);
    const vals = ws.getRangeByIndexes(r0, 0, n, nCol).getValues();
    for (const L of vals) {
      const ts = L[cTs];
      if (typeof ts !== "number" || ts < corte) { continue; }
      const id = Number(L[cId]);
      const q = typeof L[cQ] === "number" ? (L[cQ] as number) : parseFloat(String(L[cQ]).replace(",", "."));
      if (!(id > 0) || !(q > 0)) { continue; }
      const can = L[cCan];
      out.push({
        id: id,
        sl: Number(L[cSl]),
        pn: String(L[cPn]).trim(),
        q: Math.round(q * 100) / 100,
        ts: new Date(Math.round((ts - 25569) * 86400000)).toISOString().substring(0, 19),   // relogio local, sem Z
        c: can === true || can === 1 || String(can).toUpperCase() === "TRUE" || String(can).toUpperCase() === "VERDADEIRO"
      });
    }
  }
  return JSON.stringify(out);
}
