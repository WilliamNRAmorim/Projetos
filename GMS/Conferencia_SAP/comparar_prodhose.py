"""Compara duas fotos da ProdHose pela mesma regra do gerar_tripla.py.
Uso: python -I comparar_prodhose.py dados_tripla_A.json dados_tripla_B.json"""
import json, sys
REF = {"GH781-10", "GH681-12", "FC839B-08", "2556-12"}
ANT = {"EC215-08LRL","EC215-08L","FC735-08","HC101-8","2556-8","EC118-10L","EC115-10L","GH493-10","2556-10","12078544","2556-3","2556-6",
       "FC639-16","GH681-10","FC598-10","FC598-12","GH681-16","FC350-20","EC600-12","FC254-08","12055040"}
def cls(arq):
    out = {}
    for r in json.load(open(arq, encoding="utf-8")):
        p = r["ph"]
        if p <= 0.05: continue
        g = {"fluxo":0,"semPallet":0,"refugo":0,"parado":0,"antigo":0}
        if r["m"] in REF: g["refugo"] = p
        else:
            s = p; f = min(s, r["pal48"]); s -= f; c = min(s, r["semPal"]); s -= c
            g["fluxo"], g["semPallet"] = f, c
            if r["ops"] == 0 or r["m"] in ANT: g["antigo"] = s
            else: g["parado"] = s
        out[r["m"]] = g
    return out
A, B = cls(sys.argv[1]), cls(sys.argv[2])
ks = ["fluxo","semPallet","refugo","parado","antigo"]
print("grupo        18/11      19/11      dif")
for k in ks:
    a = sum(v[k] for v in A.values()); b = sum(v[k] for v in B.values())
    print(f"{k:10s} {a:9.1f} {b:9.1f} {b-a:+9.1f}")
ta = sum(sum(v.values()) for v in A.values()); tb = sum(sum(v.values()) for v in B.values())
print(f"{'total':10s} {ta:9.1f} {tb:9.1f} {tb-ta:+9.1f}")
print("\nmudanças no que é divergência (refugo+parado+antigo):")
for m in sorted(set(A)|set(B)):
    a = A.get(m, {}); b = B.get(m, {})
    da = sum(a.get(k,0) for k in ("refugo","parado","antigo")); db = sum(b.get(k,0) for k in ("refugo","parado","antigo"))
    if abs(db-da) > 0.5: print(f"  {m:14s} {da:8.1f} -> {db:8.1f} ({db-da:+.1f})")
