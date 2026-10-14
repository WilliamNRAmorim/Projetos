"""Conferência lance a lance por OP: GMS (inspeção + refugo) x MB51 (101/102 em metros).

Rodar na raiz do repositório:  python Producao_GMS_x_MB51/conferir_lances_por_op.py
Entradas (pasta Producao_GMS_x_MB51):
  dados/inspecao_14out.csv  -> lista RegistrosInspeção (query (49).iqy, exportada pelo Excel)
  dados/refugo_14out.csv    -> lista TiposErros       (query (48).iqy)
  mb51 (5).xlsx             -> export da MB51 (com código do material e Order)
  ../GMS/Sharepoint Data GMS/ficha_producao.csv -> mangueira da OP quando a inspeção vem sem nome
Saídas: Conferencia_Lances_por_OP.xlsx e aliases_mangueira.csv (nome GMS x material SAP, aprendido pela OP).
"""
import csv, sys, re, itertools, collections, datetime as dt
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "Refugo_por_Material"))
from gms_dados import norm_material, USUARIOS_REFUGO

TOL = 0.05          # metros: mesmo valor
TOL_SOMA = 0.10     # metros: soma de lances
JANELA_SOMA = (-15, 3)  # dias do lance GMS em relação à data do lançamento SAP, para casar por soma
MAX_K = 5           # até 5 lances numa soma


def num(s):
    s = str(s).strip()
    if not s:
        return None
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    else:
        s = s.replace(",", ".")
    return float(s)


def data_br(s):
    s = str(s).strip()
    for fmt in ("%d/%m/%Y %H:%M", "%d/%m/%Y"):
        try:
            return dt.datetime.strptime(s, fmt)
        except ValueError:
            pass
    return None


def ler_csv(p, delim=";"):
    for enc in ("utf-8-sig", "latin-1"):
        try:
            return list(csv.DictReader(open(p, encoding=enc), delimiter=delim))
        except UnicodeDecodeError:
            pass


def nome_gms(s):
    s = str(s).strip().upper()
    return norm_material(s).upper() if s.startswith("HOSE") else s


class Lance:
    __slots__ = ("lado", "op", "tipo", "q", "data", "ref", "info", "mat", "desc", "status", "grupo", "par", "dif", "obs")

    def __init__(s, lado, op, tipo, q, data, ref, info="", mat="", desc=""):
        s.lado, s.op, s.tipo, s.q, s.data, s.ref, s.info, s.mat, s.desc = lado, op, tipo, q, data, ref, info, mat, desc
        s.status, s.grupo, s.par, s.dif, s.obs = "", "", None, None, ""


# ---------------- GMS ----------------
ficha = {}
for r in ler_csv(AQUI.parent / "GMS" / "Sharepoint Data GMS" / "ficha_producao.csv", ","):
    if r.get("OP") and r.get("Mangueira"):
        ficha[r["OP"].strip()] = nome_gms(r["Mangueira"])

gms = collections.defaultdict(list)
nome_insp = collections.defaultdict(collections.Counter)
zerados = 0
for i, r in enumerate(ler_csv(AQUI / "dados" / "inspecao_14out.csv"), start=2):
    op, q = r["OP_ID"].strip(), num(r["Quantidade"])
    if not q:
        zerados += 1; continue
    d = data_br(r["DataHoraInspecao"]) or data_br(r["Created"])
    if r["Mangueira"].strip():
        nome_insp[op][nome_gms(r["Mangueira"])] += 1
    gms[op].append(Lance("GMS", op, "boa", q, d, f"Inspeção linha {i}", r.get("Trançadeira", "")))
for i, r in enumerate(ler_csv(AQUI / "dados" / "refugo_14out.csv"), start=2):
    op, q = r["OP_ID"].strip(), num(r["Quantidade"])
    if not q:
        zerados += 1; continue
    d = data_br(r["Created"]) or data_br(r["DataHoraRefugo"])
    gms[op].append(Lance("GMS", op, "refugo", q, d, f"Refugo linha {i}", r["CodigoErro"]))


def mangueira_gms(op):
    if nome_insp[op]:
        return nome_insp[op].most_common(1)[0][0]
    return ficha.get(op, "")


# ---------------- MB51 ----------------
mb = collections.defaultdict(list)
ws = openpyxl.load_workbook(AQUI / "mb51 (5).xlsx", read_only=True, data_only=True).worksheets[0]
for r in ws.iter_rows(min_row=2, values_only=True):
    mat, op, desc, mvt, d, un, q, usr = r[0], r[1], r[2], str(r[5]), r[9], r[11], r[14], r[15]
    if un != "M" or mvt not in ("101", "102") or not op or q is None:
        continue
    tipo = "refugo" if usr in USUARIOS_REFUGO else "boa"
    if mvt == "102":
        tipo = "estorno"
    mb[str(op).strip()].append(Lance("MB51", str(op).strip(), tipo, float(q), d, f"Doc {r[7]}/{r[8]}", usr, str(mat), str(desc)))

# ---------------- nomes: GMS x SAP pela OP ----------------
def mat_sap(op):
    c = collections.Counter((l.mat, l.desc) for l in mb.get(op, []))
    return c.most_common(1)[0][0] if c else ("", "")

alias = collections.defaultdict(lambda: collections.Counter())
for op in set(gms) & set(mb):
    g = mangueira_gms(op)
    if g:
        alias[g][mat_sap(op)] += 1
alias_top = {g: c.most_common(1)[0][0] for g, c in alias.items()}


def classe_nome(g, code):
    """igual / alias (mesmo produto com outro nome no SAP) / mangueira diferente na OP."""
    if not g:
        return "GMS sem nome de mangueira"
    if code.upper() == g:
        return "igual"
    if g in alias_top and alias_top[g][0] == code:
        return "alias: mesmo produto, nome diferente no SAP"
    esperado = alias_top.get(g, ("?",))[0]
    return f"MANGUEIRA DIFERENTE: GMS diz {g} (no SAP costuma ser {esperado}), OP no SAP é {code}"


# ---------------- casamento ----------------
def dias(a, b):
    if not a or not b:
        return 99
    return abs((a.date() - b.date()).days)


def marcar(gs, ss, status, grupo):
    tg, ts = sum(x.q for x in gs), sum(x.q for x in ss)
    for x in gs:
        x.status, x.grupo, x.par, x.dif = status, grupo, round(ts, 2), round(ts - tg, 2)
    for x in ss:
        x.status, x.grupo, x.par, x.dif = status, grupo, round(tg, 2), round(x.q - tg if len(ss) == 1 else ts - tg, 2)


def soma_combo(alvo, cands, dmax_ref, kmax):
    """menor combinação (2..kmax) de cands cuja soma bate com alvo; desempate pela distância de datas."""
    cands = [c for c in cands if c.q <= alvo + TOL_SOMA]
    if len(cands) > 22:
        kmax = min(kmax, 3)
    for k in range(2, kmax + 1):
        melhor = None
        for comb in itertools.combinations(cands, k):
            if abs(sum(c.q for c in comb) - alvo) <= TOL_SOMA:
                dd = sum(dias(c.data, dmax_ref) for c in comb)
                if melhor is None or dd < melhor[0]:
                    melhor = (dd, comb)
        if melhor:
            return list(melhor[1])
    return None


def na_janela(g, s):
    if not g.data or not s.data:
        return True
    d = (g.data.date() - s.data.date()).days
    return JANELA_SOMA[0] <= d <= JANELA_SOMA[1]


def casar(op, G, S):
    n = [0]
    def gid(p):
        n[0] += 1
        return f"{p}{n[0]}"
    # 1) estorno 102 anula um 101 de mesmo valor
    for e in [s for s in S if s.tipo == "estorno"]:
        cand = [s for s in S if s.tipo != "estorno" and not s.status and abs(s.q + e.q) <= TOL]
        if cand:
            c = min(cand, key=lambda s: dias(s.data, e.data))
            g = gid("E")
            for x in (c, e):
                x.status, x.grupo = "Estornado (101 + 102 se anulam)", g
        else:
            e.status, e.obs = "", "102 sem 101 de mesmo valor: abate do total da OP"
    S = [s for s in S if not s.status and s.tipo != "estorno"]
    # 2) mesmo valor, mesmo tipo; 3) mesmo valor, tipo trocado
    for mesmo_tipo in (True, False):
        pares = sorted(((dias(g.data, s.data), g, s) for g in G for s in S
                        if abs(g.q - s.q) <= TOL and (g.tipo == s.tipo) == mesmo_tipo), key=lambda t: t[0])
        for _, g, s in pares:
            if g.status or s.status:
                continue
            marcar([g], [s], "Casado (mesmo valor)" if mesmo_tipo else "Casado (mesmo valor; GMS e SAP com tipo trocado boa/refugo)", gid("C"))
    # 4) um lançamento SAP = soma de lances GMS
    for s in sorted([s for s in S if not s.status], key=lambda x: -x.q):
        livres = [g for g in G if not g.status and na_janela(g, s)]
        comb = soma_combo(s.q, livres, s.data, MAX_K)
        if comb:
            marcar(comb, [s], f"Casado por soma ({len(comb)} lances GMS = 1 lançamento SAP)", gid("S"))
    # 5) um lance GMS = soma de lançamentos SAP
    for g in sorted([g for g in G if not g.status], key=lambda x: -x.q):
        livres = [s for s in S if not s.status and na_janela(g, s)]
        comb = soma_combo(g.q, livres, g.data, MAX_K)
        if comb:
            marcar([g], comb, f"Casado por soma (1 lance GMS = {len(comb)} lançamentos SAP)", gid("S"))
    # 6) sobras que fecham entre si no total da OP
    rg, rs = [g for g in G if not g.status], [s for s in S if not s.status]
    if rg and rs and abs(sum(x.q for x in rg) - sum(x.q for x in rs)) <= TOL_SOMA:
        marcar(rg, rs, "Fecha no total da OP (agrupado diferente nos dois lados)", gid("T"))
        return
    # 7) valor parecido (diferença até 1 m ou 2%)
    pares = sorted(((abs(g.q - s.q), dias(g.data, s.data), g, s) for g in rg for s in rs
                    if abs(g.q - s.q) <= max(1.0, 0.02 * max(g.q, s.q))), key=lambda t: (t[0], t[1]))
    for _, _, g, s in pares:
        if g.status or s.status:
            continue
        marcar([g], [s], "VALOR DIFERENTE", gid("D"))
    for g in G:
        if not g.status:
            g.status = "SÓ NO GMS (falta lançar no SAP?)"
    for s in S:
        if not s.status:
            s.status = "SÓ NA MB51 (sobra no SAP?)"


todas_ops = sorted(set(gms) | {op for op in mb if op in gms})
for op in todas_ops:
    casar(op, gms.get(op, []), mb.get(op, []))

# 8) lance que foi para outra OP (mesmo material SAP, mesmo valor, até 7 dias)
def material_da_op(op):
    m = mat_sap(op)[0]
    if m:
        return m
    return alias_top.get(mangueira_gms(op), ("", ""))[0]

so_sap = collections.defaultdict(list)
for op in todas_ops:
    for s in mb.get(op, []):
        if s.status.startswith("SÓ NA MB51"):
            so_sap[s.mat].append(s)
cruz = []
for op in todas_ops:
    m = material_da_op(op)
    for g in gms.get(op, []):
        if not g.status.startswith("SÓ NO GMS"):
            continue
        cand = [s for s in so_sap.get(m, []) if s.op != op and abs(s.q - g.q) <= TOL and dias(s.data, g.data) <= 7 and "outra OP" not in s.obs]
        if cand:
            s = min(cand, key=lambda x: dias(x.data, g.data))
            g.obs = f"Provável lance lançado na OP {s.op} ({s.ref}, {s.data:%d/%m})"
            s.obs = f"Provável lance da OP {op} lançado nesta OP (GMS {g.ref})"
            cruz.append((m, op, g, s))

# ---------------- planilha ----------------
VERM, AMAR, VERDE, CINZA = "F8CBAD", "FFE699", "C6EFCE", "D9D9D9"
def cor(st):
    if st.startswith(("SÓ", "VALOR")):
        return VERM
    if "tipo trocado" in st or st.startswith("Fecha no total"):
        return AMAR
    if st.startswith("Estornado"):
        return CINZA
    return VERDE

wb = openpyxl.Workbook()
res = wb.active; res.title = "Resumo por OP"
lin = wb.create_sheet("Linha a linha")
cr = wb.create_sheet("Lance em outra OP")
nm = wb.create_sheet("Nomes de mangueira")
sg = wb.create_sheet("MB51 sem GMS")
pmat = wb.create_sheet("Por material")
pm = wb.create_sheet("Premissas")

res.append(["OP", "Mangueira no GMS", "Material SAP", "Descrição SAP", "Nome", "1º lance GMS", "Último lance GMS",
            "GMS boa (m)", "GMS refugo (m)", "GMS total (m)", "MB51 líquido (m)", "Dif. MB51 - GMS (m)",
            "Lances GMS", "Lanç. MB51", "Casados", "Valor diferente", "Só GMS (n)", "Só GMS (m)", "Só MB51 (n)", "Só MB51 (m)", "Situação"])
lin.append(["OP", "Mangueira GMS", "Material SAP", "Lado", "Tipo", "Data", "Qtd (m)", "Referência", "Trançadeira / usuário SAP / defeito",
            "Situação", "Grupo", "Qtd do outro lado (m)", "Dif. SAP - GMS (m)", "Observação"])

linhas_res = []
for op in todas_ops:
    G, S = gms.get(op, []), mb.get(op, [])
    gname = mangueira_gms(op)
    mcode, mdesc = mat_sap(op)
    inferido = False
    if not mcode and gname in alias_top:
        (mcode, mdesc), inferido = alias_top[gname], True
    nome = classe_nome(gname, mcode) if mcode else "sem material SAP"
    if inferido:
        nome += " / material inferido pelo nome (OP sem MB51)"
    boa = sum(g.q for g in G if g.tipo == "boa"); ref = sum(g.q for g in G if g.tipo == "refugo")
    liq = sum(s.q for s in S)
    cas = sum(1 for x in G if x.status.startswith(("Casado", "Fecha")))
    vd = sum(1 for x in G if x.status == "VALOR DIFERENTE")
    sg_ = [x for x in G if x.status.startswith("SÓ")]; ss_ = [x for x in S if x.status.startswith("SÓ")]
    datas = [g.data for g in G if g.data]
    if not S:
        sit = "OP sem lançamento na MB51"
    elif sg_ or ss_ or vd:
        sit = "DIVERGE"
    elif any("tipo trocado" in x.status or x.status.startswith("Fecha") for x in G):
        sit = "Bate (com ressalva)"
    else:
        sit = "Bate lance a lance"
    linhas_res.append([op, gname, mcode, mdesc, nome, min(datas) if datas else None, max(datas) if datas else None,
                       round(boa, 2), round(ref, 2), round(boa + ref, 2), round(liq, 2), round(liq - boa - ref, 2),
                       len(G), len(S), cas, vd, len(sg_), round(sum(x.q for x in sg_), 2), len(ss_), round(sum(x.q for x in ss_), 2), sit])
    ordem = sorted(G + S, key=lambda x: (x.grupo or "zz", x.lado, x.data or dt.datetime(2000, 1, 1)))
    for x in ordem:
        lin.append([op, gname, mcode, x.lado, x.tipo, x.data, x.q, x.ref, x.info, x.status, x.grupo, x.par, x.dif, x.obs])
        lin.cell(lin.max_row, 10).fill = PatternFill("solid", fgColor=cor(x.status))

prio = {"DIVERGE": 0, "OP sem lançamento na MB51": 1, "Bate (com ressalva)": 2, "Bate lance a lance": 3}
for row in sorted(linhas_res, key=lambda r: (prio[r[-1]], -abs(r[11]))):
    res.append(row)
    res.cell(res.max_row, 21).fill = PatternFill("solid", fgColor=VERDE if row[-1].startswith("Bate lance") else AMAR if row[-1].startswith("Bate") else VERM)

cr.append(["Material SAP", "OP do GMS", "Lance GMS", "Data GMS", "Qtd (m)", "OP onde foi lançado", "Lançamento SAP", "Data SAP"])
for m, op, g, s in cruz:
    cr.append([m, op, g.ref, g.data, g.q, s.op, s.ref, s.data])

nm.append(["Nome no GMS", "Material SAP", "Descrição SAP", "OPs com esse par", "Situação", "OPs"])
for g in sorted(alias):
    for (code, desc), n in alias[g].most_common():
        ops_par = [op for op in set(gms) & set(mb) if mangueira_gms(op) == g and mat_sap(op)[0] == code]
        nm.append([g, code, desc, n, classe_nome(g, code), ", ".join(sorted(ops_par)) if n <= 10 else "(muitas)"])

# OPs da MB51 de materiais que o GMS produz, depois do início do GMS, sem nenhum lance no GMS
mats_gms = {c for c, _ in alias_top.values()}
ini_gms = min(g.data for L in gms.values() for g in L if g.data)
sg.append(["OP", "Material SAP", "Descrição SAP", "1º lançamento", "Último lançamento", "Lançamentos", "MB51 líquido (m)"])
for op, S in sorted(mb.items()):
    if op in gms or not S or S[0].mat not in mats_gms:
        continue
    ds = [s.data for s in S if s.data]
    if not ds or max(ds) < ini_gms:
        continue
    sg.append([op, S[0].mat, S[0].desc, min(ds), max(ds), len(S), round(sum(s.q for s in S), 2)])

for l in [
    "Fontes: listas RegistrosInspeção e TiposErros do SharePoint puxadas em 14/10/2026 pelas query (49).iqy e query (48).iqy; MB51 = mb51 (5).xlsx (lançamentos até 14/10/2026).",
    "MB51: só unidade M, movimentos 101 e 102, com Order preenchida. Usuários U445131 e U452021 = lançamento de refugo; demais = produção boa; 102 = estorno (vem negativo).",
    "GMS: cada linha da inspeção é um lance de produção boa; cada linha do TiposErros é um lance de refugo. Linhas com quantidade 0 ou vazia foram ignoradas (" + str(zerados) + ").",
    "Ordem do casamento dentro da OP: (1) cada 102 anula um 101 de mesmo valor; (2) mesmo valor (±0,05 m) e mesmo tipo, pela data mais próxima; (3) mesmo valor com tipo trocado (boa x refugo);",
    "(4) um lançamento SAP = soma de 2 a 5 lances GMS (±0,10 m; lances GMS de 15 dias antes até 3 dias depois da data SAP). Ex.: lances de 10, 20 e 30 m no GMS e um de 60 m na MB51 = casados;",
    "(5) o contrário: um lance GMS = soma de lançamentos SAP; (6) se o que sobrou dos dois lados fecha no total da OP (±0,10 m), marca 'Fecha no total da OP';",
    "(7) sobra com valor parecido (até 1 m ou 2%) = VALOR DIFERENTE; (8) o resto = SÓ NO GMS ou SÓ NA MB51.",
    "Lance em outra OP: lance 'só no GMS' com o mesmo valor (±0,05 m) de um lançamento 'só na MB51' de outra OP do mesmo material SAP, até 7 dias de diferença. É costume da fábrica; confirmar antes de corrigir.",
    "Dif. = MB51 - GMS: negativa = falta lançar no SAP; positiva = sobra no SAP. SAP é a fonte da verdade. Material não compensa com material.",
    "Nome da mangueira: o material SAP vem da própria OP na MB51 (código + descrição), não do nome. O nome do GMS foi ligado ao material SAP pelas OPs que existem nos dois lados (aba Nomes e aliases_mangueira.csv).",
    "OP sem lançamento na MB51 pode ser OP ainda em produção (veja a data do último lance) ou OP que nunca foi apontada no SAP.",
    "Casamento por soma é uma inferência. Teste em 14/10: trocando o valor SAP por um valor falso (±4 a 5 m), só ~5% das somas ainda fechariam; ou seja, ~95% das somas são reais. Confira o grupo na aba Linha a linha.",
    "Lance de produção: 99% dos lances casados 1 a 1 têm a mesma data no GMS e no SAP; os casados por soma foram lançados no SAP 1 a 6 dias depois, quase sempre lances do mesmo turno (menos de 6 h entre o primeiro e o último).",
]:
    pm.append([l])
pm.column_dimensions["A"].width = 160

def formatar(ws, larg):
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor="C8102E")
        c.alignment = Alignment(wrap_text=True, horizontal="center", vertical="center")
    for i, w in enumerate(larg, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "B2"
    ws.auto_filter.ref = ws.dimensions
    for row in ws.iter_rows(min_row=2):
        for c in row:
            if isinstance(c.value, dt.datetime):
                c.number_format = "dd/mm/yyyy hh:mm"
            elif isinstance(c.value, float):
                c.number_format = "#,##0.00"

agg = collections.defaultdict(lambda: [0, 0.0, 0.0, 0, 0.0, 0, 0.0, 0])
for r in linhas_res:
    a = agg[(r[2], r[3])]
    a[0] += 1; a[1] += r[9]; a[2] += r[10]; a[3] += r[16]; a[4] += r[17]; a[5] += r[18]; a[6] += r[19]; a[7] += r[-1] == "DIVERGE"
pmat.append(["Material SAP", "Descrição SAP", "OPs", "OPs que divergem", "GMS total (m)", "MB51 líquido (m)", "Só GMS (n)", "Só GMS (m) = falta no SAP", "Só MB51 (n)", "Só MB51 (m) = sobra no SAP"])
for (c, d), a in sorted(agg.items(), key=lambda kv: -(kv[1][4] + kv[1][6])):
    pmat.append([c, d, a[0], a[7], round(a[1], 2), round(a[2], 2), a[3], round(a[4], 2), a[5], round(a[6], 2)])
formatar(pmat, [14, 36, 7, 10, 13, 13, 9, 14, 9, 14])
formatar(res, [11, 14, 12, 30, 22, 15, 15, 11, 11, 11, 11, 11, 8, 8, 8, 9, 8, 10, 8, 10, 22])
formatar(lin, [11, 14, 12, 7, 8, 15, 10, 18, 22, 40, 7, 11, 11, 50])
formatar(cr, [14, 11, 18, 15, 10, 13, 20, 15])
formatar(nm, [16, 14, 36, 10, 60, 40])
formatar(sg, [11, 14, 36, 15, 15, 11, 13])

out = AQUI / "Conferencia_Lances_por_OP.xlsx"
wb.save(out)

with open(AQUI / "aliases_mangueira.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["nome_gms", "material_sap", "descricao_sap", "ops", "situacao"])
    for g in sorted(alias):
        for (code, desc), n in alias[g].most_common():
            w.writerow([g, code, desc, n, classe_nome(g, code)])

st = collections.Counter(r[-1] for r in linhas_res)
print("salvo", out.name, "| OPs:", len(linhas_res), dict(st))
tot = collections.Counter()
for L in list(gms.values()) + [mb[o] for o in todas_ops if o in mb]:
    for x in L:
        tot[(x.lado, x.status.split(" (")[0])] += 1
for k, v in sorted(tot.items()):
    print(k, v)
print("lance em outra OP:", len(cruz), "| aliases:", sum(1 for g in alias for k in alias[g] if norm_material(k[1]).upper() != g and k[0].upper() != g))
