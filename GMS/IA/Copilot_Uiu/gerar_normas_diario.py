#!/usr/bin/env python3
# Gera conhecimento/08_Normas_Diario.md: linhas NORMA e DECISAO do GMS_Diario.md (via gms.carrega),
# da data de corte em diante, mais novas primeiro. Rodar de novo antes de cada upload ao Uiu.
# Uso: python gerar_normas_diario.py [AAAA-MM-DD]   (padrao: 2026-09-01)
import os, sys, collections

AQUI = os.path.dirname(os.path.abspath(__file__))
GMS = os.path.abspath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, GMS)
os.chdir(GMS)
import gms  # noqa: E402

corte = sys.argv[1] if len(sys.argv) > 1 else "2026-09-01"
linhas = [e for e in gms.carrega()
          if not e.get("erro") and e["tipo"] in ("NORMA", "DECISÃO") and e["data"] >= corte]
linhas.sort(key=lambda e: (e["data"], e["n"]), reverse=True)

por_mes = collections.OrderedDict()
for e in linhas:
    por_mes.setdefault(e["data"][:7], []).append(e)

out = [
    "# Normas e decisões recentes do Diário do GMS",
    "",
    f"Gerado de `GMS_Diario.md` por `gerar_normas_diario.py` (linhas NORMA e DECISÃO desde {corte}, "
    f"{len(linhas)} linhas, mais novas primeiro).",
    "",
    "Como usar: a linha mais nova vence a mais velha e vence o Mestre (01_Norma_do_App.md). "
    "Se uma linha disser que revoga outra, vale a que revoga. MEL-xxx é o ID do item no backlog. "
    "Tags no fim (#F1, #esfM, #impA) são fase, esforço e impacto; podem ser ignoradas na resposta.",
    "",
]
for mes, es in por_mes.items():
    out.append(f"## {mes}")
    out.append("")
    for e in es:
        refs = " ".join(e["refs"]) or "—"
        out.append(f"- {e['data']} · {e['tipo']} · {e['alvo']} · {refs} — {e['texto']}")
    out.append("")

dest = os.path.join(AQUI, "conhecimento", "08_Normas_Diario.md")
with open(dest, "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print(f"{dest}: {len(linhas)} linhas, {os.path.getsize(dest)//1024} KB")
