"""Gera painel_kpi.html (autossuficiente) a partir de painel_template.html + dados_diarios.json.
Uso: python extrair_dados.py && python gerar_painel.py"""
import pathlib
p = pathlib.Path(__file__).parent
html = (p / "painel_template.html").read_text(encoding="utf-8").replace("__DATA__", (p / "dados_diarios.json").read_text(encoding="utf-8"))
(p / "painel_kpi.html").write_text(html, encoding="utf-8")
print("ok", len(html))
