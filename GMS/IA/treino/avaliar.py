# avaliar.py - compara modelos do Ollama no eval.jsonl: executa o SQL de cada um e confere com o esperado.
# Uso: python avaliar.py [pasta_dados] eval.jsonl --modelos qwen3:8b gms-qwen
# Roda cada modelo em dois modos: "sem memoria" (o prompt do eval.jsonl) e "com memoria" (montar_sistema normal do
# gms_ia, lendo a memoria.md, mas SEM as linhas da propria pergunta avaliada). Grava uma linha de Placar por modo.
import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent))
sys.path.insert(0, str(AQUI))
import gms_ia  # noqa: E402
import gms_mapear  # noqa: E402
import recompensa  # noqa: E402

MODOS = ("sem memoria", "com memoria")


def chave(p):
    return re.sub(r"\s+", " ", recompensa.sem_acento(p)).strip(" ?.!")


def prompt_com_memoria(it, memoria_real, tmp):
    """Sistema normal do gms_ia, com a memoria sem as linhas desta pergunta (senao a resposta vazaria)."""
    linhas = memoria_real.read_text(encoding="utf-8").splitlines() if memoria_real.exists() else []
    def da_pergunta(l):
        m = re.match(r"^- \[.+?\] P: (.*?) (?:SQL|ERRADO):", l)
        return bool(m) and chave(m.group(1)) == chave(it["pergunta"])

    ficam = [l for l in linhas if not da_pergunta(l)]
    tmp.write_text("\n".join(ficam) + "\n", encoding="utf-8", newline="\n")
    real, gms_ia.MEMORIA = gms_ia.MEMORIA, tmp
    try:
        return [{"role": "system", "content": gms_ia.montar_sistema(it["pergunta"])},
                {"role": "user", "content": it["pergunta"]}]
    finally:
        gms_ia.MEMORIA = real


def avaliar_modelo(modelo, itens, con, modo, memoria_real, tmp):
    gms_ia.MODELO = modelo
    ok = execu = 0
    for k, it in enumerate(itens, 1):
        prompt = it["prompt"] if modo == MODOS[0] else prompt_com_memoria(it, memoria_real, tmp)
        try:
            texto = gms_ia.chat(prompt)
        except gms_ia.ErroOllama as e:
            sys.exit(f"Nao consegui falar com o Ollama ({e}). Ele esta aberto e o modelo {modelo} baixado?")
        r = recompensa.analisar(con, texto, it)
        execu += r["executa"]
        ok += r["bate"]
        print(f"  [{modelo} | {modo}] {k}/{len(itens)} {'CERTO' if r['bate'] else 'executou' if r['executa'] else 'falhou'}")
    return ok, execu


def principal(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("itens", nargs="+", help="[pasta_dados] eval.jsonl")
    ap.add_argument("--modelos", nargs="+", required=True)
    a = ap.parse_args(argv)
    pasta, arq = ("dados", a.itens[0]) if len(a.itens) == 1 else (a.itens[0], a.itens[1])
    memoria_real = gms_ia.MEMORIA
    gms_ia.preparar(pasta)  # esquema/mapa para o modo "com memoria"; atualiza o cache se preciso
    gms_ia.MEMORIA = memoria_real
    con = recompensa.abrir(pasta)
    itens = [json.loads(l) for l in Path(arq).read_text(encoding="utf-8").splitlines() if l.strip()]
    if not itens:
        sys.exit("eval.jsonl vazio.")
    tmp = Path(tempfile.mkdtemp()) / "mem_sem_pergunta.md"
    n = len(itens)
    placar = {(m, modo): avaliar_modelo(m, itens, con, modo, memoria_real, tmp) for m in a.modelos for modo in MODOS}
    print(f"\n{'Modelo':<22}{'Modo':<14}{'Acerto':>16}{'Executa':>10}")
    for (m, modo), (ok, ex) in placar.items():
        print(f"{m:<22}{modo:<14}{f'{ok}/{n} ({100 * ok // n}%)':>16}{f'{ex}/{n}':>10}")
    for modo in MODOS:
        resumo = " | ".join(f"{m} {placar[(m, modo)][0]}/{n}" for m in a.modelos)
        gms_ia.anexar(gms_ia.SEC_PLAC, f"[{gms_ia.hoje()}] eval modo {modo}: {resumo} (acerto por execucao)")
    print("Gravado em Placar da memoria.md (uma linha por modo).")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    principal()
