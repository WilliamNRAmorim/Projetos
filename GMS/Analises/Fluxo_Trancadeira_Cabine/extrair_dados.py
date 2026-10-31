"""Extrai serie diaria por etapa da ficha_producao (metros, pessoas distintas, lead time) -> dados_diarios.json.
Pessoas = operadores distintos que apontaram a etapa no dia (estimativa; nomes NAO sao gravados)."""
import pandas as pd, json, pathlib
src = pathlib.Path(__file__).resolve().parents[2] / "Sharepoint Data GMS" / "ficha_producao.csv"
d = pd.read_csv(src, encoding="utf-8-sig", low_memory=False)
d.columns = [c.encode("latin1").decode("utf8") if "Ã" in c else c for c in d.columns]
ST = {"tranc": ("data_hora_final_trancadeira", "quantidade_trancagem", "operador_trancagem"),
      "cob": ("data_hora_final_cobertura", "quantidade_cobertura", "operador_cobertura"),
      "band": ("data_hora_final_bandagem", "quantidade_bandagem", "operador_bandagem"),
      "vulc": ("data_hora_final_vulcanizacao", "quantidade_vulcanizacao", "operador_vulcanizacao"),
      "deb": ("data_hora_final_debandagem", "quantidade_debandagem", "operador_debandagem"),
      "cab": ("data_hora_final_extracao", "quantidade_extracao", "operador_extracao")}
out = {}
for k, (t, q, o) in ST.items():
    x = d[[t, q, o]].copy(); x.columns = ["t", "q", "o"]
    x["t"] = pd.to_datetime(x.t, errors="coerce", format="mixed"); x["q"] = pd.to_numeric(x.q, errors="coerce")
    x = x.dropna(subset=["t"]); x["dia"] = x.t.dt.strftime("%Y-%m-%d")
    g = x.groupby("dia").agg(m=("q", "sum"), f=("q", "size"), hc=("o", lambda s: s.dropna().nunique()))
    for dia, r in g.iterrows():
        out.setdefault(dia, {})[k] = [round(float(r.m), 1), int(r.f), int(r.hc)]
# lead time trancagem -> cabine por ficha (horas), mediana por dia da saida na cabine
a = pd.to_datetime(d.data_hora_final_trancadeira, errors="coerce", format="mixed")
b = pd.to_datetime(d.data_hora_final_extracao, errors="coerce", format="mixed")
lt = ((b - a).dt.total_seconds() / 3600); ok = lt.between(0.5, 24 * 30)
s = pd.DataFrame({"dia": b[ok].dt.strftime("%Y-%m-%d"), "lt": lt[ok]}).groupby("dia").lt.median()
for dia, v in s.items():
    if dia in out: out[dia]["lt"] = round(float(v), 1)
out = dict(sorted(out.items()))
pathlib.Path(__file__).with_name("dados_diarios.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(len(out), min(out), max(out))
