# Teste (fase 1) do indicador "pallet parado na PROD-GR-HOSE". So leitura: nao grava em SharePoint nem SAP.
# Uso:  python teste_pallet_parado.py            (processa todas as fotos de GMS/Analises/ProdHose_Teste)
#       python teste_pallet_parado.py --simular  (casos simulados)
# Na pasta, por dia:  EXPORT_AAAAMMDD_HHMMSS.xlsx (PROD-GR-HOSE)  +  mb51_AAAAMMDD.xlsx  +  gms_AAAAMMDD.json
#   gms: {"pallets": [{"id","op","n","imp","lances"}], "lances": {"id": metros}}   (imp em UTC; exportado pelo Claude)
# A hora do nome EXPORT_ e CET (UTC+1), conferida em 24/11: 14:09 do arquivo = 10:09 em Brasilia.
# Base = saldo livre da 1a foto (tudo antigo, inclusive o que estava em transito) e so desce. Enquanto a base do material
# nao desceu, o que podia estar em transito na 1a foto (pallet ate 1 dia util, refugo ate 7 dias) entra como SAIDA possivel.
# Fora isso, saida da base coberta por pallet novo do mesmo material da 'nao identificado' ou fica escondida.
import json, re, sys
from datetime import datetime, timedelta
from itertools import combinations
from pathlib import Path

PASTA = Path(__file__).resolve().parent.parent / "Analises" / "ProdHose_Teste"
REFUGO = {"U452021", "U445131"}
NAO_IMPRESSOS = set(range(531, 541))      # registrados em 23/11 sem packlist impresso
TOL = 0.1
MAX_CAND = 12
FERIADOS = {"2026-11-20", "2026-12-25", "2027-01-01"}


def util(d):
    return d.weekday() < 5 and d.strftime("%Y-%m-%d") not in FERIADOS


def prazo(t):
    """1 dia util depois: mesma hora do proximo dia util."""
    x = t + timedelta(days=1)
    while not util(x):
        x += timedelta(days=1)
    return x


def casar(sobra, pallets, refugos, saidas=()):
    """Devolve (situacao, lista de pallets). pallets: id, m, lances(frozenset). refugos: metros por lote/dia."""
    if sobra <= TOL and not (saidas and pallets):
        return "ok", []
    unicos = {}
    for p in sorted(pallets, key=lambda p: p["id"]):
        unicos[p["lances"]] = p            # mesmos lances = reimpressao: fica o mais novo
    c = [("P", p["m"], p) for p in unicos.values()] + [("R", m, None) for m in refugos] + [("S", -m, None) for m in saidas]
    if len(c) > MAX_CAND:
        return "ambiguo", [p for t, _, p in c if t == "P"]
    sol = {}
    if abs(sobra) <= TOL:
        sol[frozenset()] = []              # nada mudou tambem e uma resposta
    for k in range(1, len(c) + 1):
        for comb in combinations(c, k):
            if abs(sum(m for _, m, _ in comb) - sobra) > TOL + 1e-9:
                continue
            ps = [p for t, _, p in comb if t == "P"]
            uniao = frozenset().union(*[p["lances"] for p in ps]) if ps else frozenset()
            if len(uniao) != sum(len(p["lances"]) for p in ps):
                continue                   # lance em dois pallets: nao conta duas vezes
            sol.setdefault(uniao, ps)
    if not sol:
        return ("nao identificado" if sobra > TOL else "base caiu"), []
    if len(sol) > 1:
        return "ambiguo", sorted({p["id"]: p for ps in sol.values() for p in ps}.values(), key=lambda p: p["id"])
    ps = next(iter(sol.values()))
    return ("identificado" if ps else "refugo" if sobra > TOL else "ok"), ps


def ler(caminho):
    import openpyxl
    it = openpyxl.load_workbook(caminho, read_only=True, data_only=True).worksheets[0].iter_rows(values_only=True)
    cab = [str(x or "").strip() for x in next(it)]
    ix = {}
    for i, n in enumerate(cab):
        ix.setdefault(n, i)
    return ix, it


def saldo_livre(caminho):
    ix, it = ler(caminho)
    livre, fora = {}, {}
    for r in it:
        if not r[ix["Product"]]:
            continue
        ok = r[ix["Stock Type"]] == "F2" and not r[ix["Document Category"]]
        d = livre if ok else fora
        d[r[ix["Product"]]] = d.get(r[ix["Product"]], 0) + float(r[ix["Quantity"]])
    return livre, fora


def mb51(caminho, desde):
    ix, it = ler(caminho)
    out = []
    for r in it:
        if r[ix["Unit of Entry"]] != "M" or r[ix["Storage Location"]] != "GRT4" or str(r[ix["Movement Type"]]) not in ("101", "102"):
            continue
        d = r[ix["Posting Date"]]
        if not isinstance(d, datetime) or d < desde:
            continue
        out.append((str(r[ix["Material"]]), str(r[ix["Order"]]), d, float(r[ix["Quantity"]]), str(r[ix["User Name"]]).strip().upper()))
    return out


def tudo_no_sap(ids, metros, docs):
    """Todos os lances do pallet tem lancamento liquido no SAP, na mesma OP."""
    pos = sorted(q for q in docs if q > 0)
    for n in (q for q in docs if q < 0):
        p = next((x for x in pos if abs(x + n) <= 0.05), None)
        if p is not None:
            pos.remove(p)
    for i in ids:
        q = metros.get(str(i))
        p = next((x for x in pos if q is not None and abs(x - q) <= 0.05), None)
        if p is None:
            return False
        pos.remove(p)
    return True


def rodar():
    fotos = []
    for f in PASTA.glob("EXPORT_*.xlsx"):
        m = re.match(r"EXPORT_(\d{8})_(\d{6})", f.name)
        if m:
            fotos.append((datetime.strptime(m[1] + m[2], "%Y%m%d%H%M%S") - timedelta(hours=4), f))
    fotos.sort()
    if not fotos:
        print("Sem foto em", PASTA)
        return
    t0, f0 = fotos[0]
    base, fora = saldo_livre(f0)
    print(f"Base {t0:%d/%m %H:%M}: livre {sum(base.values()):.1f} m; fora da conta {sum(fora.values()):.1f} m")
    base0 = dict(base)
    for t, f in fotos[1:]:
        dia = t.strftime("%Y%m%d")
        fm, fg = PASTA / f"mb51_{dia}.xlsx", PASTA / f"gms_{dia}.json"
        livre, fora = saldo_livre(f)
        for k in set(base) | set(livre):   # a base so desce
            base[k] = min(base.get(k, 0), livre.get(k, 0))
        print(f"\n=== {t:%d/%m %H:%M}: livre {sum(livre.values()):.1f} m; base {sum(base.values()):.1f} m; fora da conta {sum(fora.values()):.1f} m")
        if not fm.exists() or not fg.exists():
            print("NAO MEDIDO: falta", ", ".join(x.name for x in (fm, fg) if not x.exists()))
            continue
        docs = mb51(fm, t0 - timedelta(days=10))
        pn, porop, lotes, lotes0 = {}, {}, {}, {}
        for mat, op, d, q, u in docs:
            if u in REFUGO:
                if d.date() > t0.date():
                    lotes[(mat, d)] = lotes.get((mat, d), 0) + q
                elif d.date() >= (t0 - timedelta(days=7)).date():
                    lotes0[(mat, d)] = lotes0.get((mat, d), 0) + q
            else:
                pn[op] = mat
                porop.setdefault(op, []).append(q)
        g = json.loads(fg.read_text(encoding="utf-8"))
        cand, cand0, espera = {}, {}, []
        for p in g["pallets"]:
            imp = datetime.strptime(p["imp"][:19], "%Y-%m-%dT%H:%M:%S") - timedelta(hours=3)
            if p["id"] in NAO_IMPRESSOS or imp > t or t0 > prazo(imp):
                continue
            if imp <= t0:                  # podia estar em transito na 1a foto
                if p["op"] in pn:
                    cand0.setdefault(pn[p["op"]], {})[frozenset(p["lances"])] = round(sum(g["lances"].get(str(i), 0) for i in p["lances"]), 2)
                continue
            if p["op"] not in pn or not tudo_no_sap(p["lances"], g["lances"], porop[p["op"]]):
                espera.append(p["id"])
                continue
            cand.setdefault(pn[p["op"]], []).append(dict(id=p["id"], op=p["op"], imp=imp, lances=frozenset(p["lances"]),
                                                         m=round(sum(g["lances"][str(i)] for i in p["lances"]), 2)))
        if espera:
            print("Pallets ainda sem lancamento completo no MB51:", espera)
        tot = ident = preso = 0
        for mat in sorted(livre):
            sobra = round(livre[mat] - base.get(mat, 0), 3)
            sai = []
            if base.get(mat, 0) >= base0.get(mat, 0) - TOL:
                sai = [m for m in list(cand0.get(mat, {}).values()) + [m for (k, _), m in lotes0.items() if k == mat] if 0 < m <= base.get(mat, 0) + TOL]
            if sobra <= TOL and not (sai and cand.get(mat)):
                continue
            ref = [m for (k, _), m in lotes.items() if k == mat]
            sit, ps = casar(sobra, cand.get(mat, []), ref, sai)
            peso = max(sobra, sum(p["m"] for p in ps) if sit == "identificado" else 0)
            tot += peso
            if sit in ("identificado", "refugo"):
                ident += peso
            linha = []
            for p in ps:
                parado = sit == "identificado" and t > prazo(p["imp"])
                preso += p["m"] if parado else 0
                linha.append(f"{'PRESO ' if parado else ''}{p['id']} OP {p['op']} {p['m']:.1f} m ({p['imp']:%d/%m %H:%M})")
            print(f"  {mat:14s} sobra {sobra:8.1f}  {sit:16s} {'; '.join(linha)}")
        print(f"  PRESO: {preso:.1f} m | sobra {tot:.1f} m, identificada {100 * ident / tot if tot else 100:.0f}% (criterio 90%)")


def simular():
    P = lambda i, m, *l: dict(id=i, m=m, lances=frozenset(l))
    a, b, c = P(1, 421.0, 1, 2), P(2, 347.6, 3), P(3, 391.9, 4)
    T = [
        ("sem sobra", casar(0, [a], []), "ok", []),
        ("um pallet", casar(421.0, [a, b, c], []), "identificado", [1]),
        ("dois pallets", casar(768.6, [a, b, c], []), "identificado", [1, 2]),
        ("pallet + refugo", casar(373.6, [a, b, c], [26.0]), "identificado", [2]),
        ("so refugo", casar(26.0, [a, b], [26.0]), "refugo", []),
        ("nada fecha", casar(100.0, [a, b, c], []), "nao identificado", []),
        ("diferenca 0,6 nao passa", casar(769.2, [a, b, c], []), "nao identificado", []),
        ("duas respostas", casar(421.0, [a, P(4, 421.0, 9)], []), "ambiguo", [1, 4]),
        ("repetido conta uma vez", casar(818.7, [P(5, 818.7, 7), P(6, 818.7, 7)], []), "identificado", [6]),
        ("repetido nao soma", casar(1637.4, [P(5, 818.7, 7), P(6, 818.7, 7)], []), "nao identificado", []),
        ("inteiro ou partes", casar(349.1, [P(1, 349.1, 1, 2), P(2, 127.9, 1), P(3, 221.2, 2)], [])[0:1], "identificado", None),
        ("saida da base + pallet novo", casar(427.0, [a], [26.0], [20.0]), "identificado", [1]),
        ("saida cobre o pallet novo", casar(-347.6, [a], [], [768.6]), "identificado", [1]),
        ("parado igual nao inventa", casar(0, [a], [], [100.0]), "ok", []),
        ("saida igual a entrada", casar(0, [a], [], [421.0])[0:1], "ambiguo", None),
        ("13 candidatos", casar(421.0, [P(i, 10.0 + i, i) for i in range(13)], [])[0:1], "ambiguo", None),
    ]
    falhas = 0
    for nome, r, sit, ids in T:
        ok = r[0] == sit and (ids is None or [p["id"] for p in r[1]] == ids)
        falhas += not ok
        print("ok  " if ok else "ERRO", nome, r[0])
    x = datetime(2026, 11, 19, 15, 0)
    for nome, v, e in (("quinta com feriado na sexta", prazo(x), datetime(2026, 11, 23, 15)), ("sexta", prazo(datetime(2026, 11, 27, 9)), datetime(2026, 11, 30, 9)),
                       ("no SAP", tudo_no_sap([1, 2], {"1": 5.0, "2": 7.0}, [7.0, 5.0]), True), ("estornado", tudo_no_sap([1], {"1": 5.0}, [5.0, -5.0]), False)):
        falhas += v != e
        print("ok  " if v == e else "ERRO", nome, v)
    print("falhas:", falhas)
    return falhas


if __name__ == "__main__":
    sys.exit(simular()) if "--simular" in sys.argv else rodar()
