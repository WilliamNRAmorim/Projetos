/**
 * GMS_LerTemposMontagem  v1.0.0  (28/10/2026)
 * Office Script - le a tabela Tempos_montagem (aba "Tempos Montagem": Material, "Tempo (min) / pc") do
 * "PN prod time.xlsx" (somente leitura) e devolve em JSON so o que mudou em relacao a lista Tempos_Montagem,
 * para o fluxo GMS_Tempos_Sync gravar. Nada e escrito na planilha.
 *   existentesJson = itens atuais da lista, um por Material: [{"id":123,"m":"71401756","t":1.5172}, ...]
 *   saida          = {"total":3995,"novos":[{"m","t"}],"alterados":[{"id","m","t"}],"duplicados":0,"invalidos":0}
 * Material que sumiu da planilha NAO e apagado da lista (historico). Material repetido na planilha: vale a ultima linha.
 * Tempo vazio, texto ou <= 0 e ignorado (conta em "invalidos"). Compara com tolerancia de 1e-9. ES5 (sem for-of em Map/Set).
 */
interface Existente { id: number; m: string; t: number; }

function chave(v: string | number | boolean): string {
  return String(v === undefined || v === null ? "" : v).trim().toUpperCase();
}

function main(workbook: ExcelScript.Workbook, existentesJson: string): string {
  let tabela = workbook.getTable("Tempos_montagem");
  if (!tabela) {
    const aba = workbook.getWorksheet("Tempos Montagem");
    if (!aba) { throw new Error("Tabela Tempos_montagem e aba 'Tempos Montagem' nao encontradas"); }
    tabela = aba.getTables()[0];
    if (!tabela) { throw new Error("A aba 'Tempos Montagem' nao tem tabela"); }
  }
  const v = tabela.getRangeBetweenHeaderAndTotal().getValues();

  const ultimo: { [k: string]: { m: string; t: number } } = {};
  let duplicados = 0;
  let invalidos = 0;
  for (let r = 0; r < v.length; r++) {
    const k = chave(v[r][0]);
    if (k === "") { continue; }
    const t = typeof v[r][1] === "number" ? (v[r][1] as number) : NaN;
    if (!(t > 0)) { invalidos++; continue; }
    if (ultimo[k] !== undefined) { duplicados++; }
    ultimo[k] = { m: String(v[r][0]).trim(), t: t };
  }

  const atuais: { [k: string]: Existente } = {};
  let lista: Existente[] = [];
  try { lista = JSON.parse(existentesJson || "[]") as Existente[]; } catch (e) { lista = []; }
  for (let i = 0; i < lista.length; i++) { atuais[chave(lista[i].m)] = lista[i]; }

  const novos: { m: string; t: number }[] = [];
  const alterados: { id: number; m: string; t: number }[] = [];
  let total = 0;
  for (const k in ultimo) {
    if (!Object.prototype.hasOwnProperty.call(ultimo, k)) { continue; }
    total++;
    const a = atuais[k];
    if (!a) { novos.push(ultimo[k]); }
    else if (Math.abs(Number(a.t) - ultimo[k].t) > 1e-9) { alterados.push({ id: a.id, m: ultimo[k].m, t: ultimo[k].t }); }
  }
  return JSON.stringify({ total: total, novos: novos, alterados: alterados, duplicados: duplicados, invalidos: invalidos });
}
