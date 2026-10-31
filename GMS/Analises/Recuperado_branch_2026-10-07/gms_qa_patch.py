#!/usr/bin/env python3
"""Auditoria MEL-009: todo Patch/Remove/Collect em fonte de dados de producao precisa de checagem
de erro (Errors(<fonte>) logo depois, ou IfError em volta). Uso: python gms_qa_patch.py [janela]
A janela (padrao 900 caracteres) e quanto texto depois do Patch o script olha atras de Errors(<fonte>).
Falso positivo conhecido: Patch dentro de Switch/If com a checagem unica DEPOIS do bloco inteiro
(ex.: scr_DescartarOP_1) e lote com checagem agregada depois do ForAll (scr_Vulcanizacao_1)."""
import re, glob, sys
JANELA = int(sys.argv[1]) if len(sys.argv) > 1 else 900
SRC = ["ficha_producao","Eventos_Producao","lista_carreteis","Historico_Carretel","CarreteisMandril","Hora-Hora",
       "Hora_Hora_Mandril","Hora_Hora_Tubo","Producao_Montagem","Paradas_Montagem","Controle_Catenaria","Controle_Medicao",
       "Refugo_Bobinadeira","RefugoExtrusora_estrutura","ControleExtrusora_estrutura","RegistrosInspeção","TiposErros",
       "FifoBobinadeira","Estado_Trancadeiras","Packing_Manual"]
pat = re.compile(r"\b(Patch|Remove|RemoveIf|UpdateIf|Collect|SubmitForm)\(\s*('?(?:" + "|".join(re.escape(s) for s in SRC) + r")'?)\b")

def fecha(t, i):
    d = 0
    for k in range(i, len(t)):
        if t[k] == "(": d += 1
        elif t[k] == ")":
            d -= 1
            if d == 0: return k
    return len(t)

# Justificadas: a checagem existe, mas depois do bloco inteiro (Switch/ForAll) e nao logo apos o Patch.
EXC = {("scr_DescartarOP_1", "ficha_producao"): "um Patch por etapa dentro do Switch; checagem unica depois do Switch",
       ("scr_Vulcanizacao_1", "Historico_Carretel"): "lote: checagem agregada depois do ForAll",
       ("scr_Vulcanizacao_1", "ficha_producao"): "lote: checagem agregada depois do ForAll",
       ("scr_Debandagem_2", "lista_carreteis"): "dois Patch seguidos (saida e entrada) e uma checagem depois dos dois"}
tot = 0; ruim = []; just = []
for f in sorted(glob.glob("Telas/scr*.txt") + ["Telas/TelaImpressao.txt"]):
    t = open(f, encoding="utf-8").read()
    for m in pat.finditer(t):
        tot += 1
        fn, src = m.group(1), m.group(2).strip("'")
        ini = m.start(); fim = fecha(t, t.index("(", ini))
        depois = t[fim:fim + JANELA]; antes = t[max(0, ini - 400):ini]
        ok = bool(re.search(r"Errors\(\s*'?" + re.escape(src) + r"'?\s*\)", depois)) or "IfError(" in antes
        if not ok:
            r = (f[6:-4], t.count("\n", 0, ini) + 1, fn, src)
            (just if (r[0], src) in EXC else ruim).append(r)
print(f"escritas em fonte: {tot} | sem checagem em {JANELA} caracteres: {len(ruim)} | justificadas: {len(just)}")
for r in ruim: print(f"  {r[0]:26} L{r[1]:<5} {r[2]}({r[3]})")
