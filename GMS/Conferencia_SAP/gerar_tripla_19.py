# Roda o gerar_tripla.py com os textos de 19/11 (mesma regra, data e causas novas).
import sys
s = open("gerar_tripla.py", encoding="utf-8").read()
rep = [("16 a 18/11", "17 a 19/11"), ("16-18/11", "17-19/11"), ("18/11/2026", "19/11/2026"), ("MB51 de 18/11 08:06", "MB51 de 19/11 08:06"),
       ("colado às ~09h", "colado em 19/11"), ('"= 32 últimos refugos (15/09 a 17/11)"', '"= 30 refugos de 15/09 a 22/10 (13 m de 16-17/11 já baixados)"'),
       ('"30860014": ("Em fluxo", "Produzida hoje; o MB51 é das 08:06"),', '"30885835": ("Em fluxo", "SAP lançou depois do MB51 das 08:06 (já está na ProdHose)"), "30885836": ("Em fluxo", "SAP lançou depois do MB51 das 08:06 (já está na ProdHose)"), "30856399": ("Em fluxo", "SAP lançou depois do MB51 das 08:06; ainda sem pallet no GMS"),'),
       ("as 6 restantes", "as restantes")]
for a, b in rep:
    s = s.replace(a, b)
sys.argv = ["gerar_tripla.py", "dados_tripla_2026-11-19.json", "Conferencia_SAPxGMSxProdHose_2026-11-19.html"]
exec(compile(s, "gerar_tripla.py", "exec"))
