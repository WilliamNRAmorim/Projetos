# exportar_treino.py - monta o pacote para treinar por reforco a IA local (Colab/Kaggle).
# Uso: python exportar_treino.py [pasta_dados] [treino1.md treino2.md ...] [--memoria arquivo.md] [--saida pasta]
# Le IA/memoria.md (perguntas validadas e erros a evitar) e arquivos com blocos P:/R: (e "SQL:" opcional).
# Gera sft.jsonl, dpo.jsonl, grpo.jsonl, eval.jsonl e pacote_treino.zip (com os parquet do cache).
import argparse
import hashlib
import json
import re
import sys
import tempfile
import zipfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent))
sys.path.insert(0, str(AQUI))
import gms_ia  # noqa: E402
import recompensa  # noqa: E402

FRACAO_EVAL = 0.2
SEMENTE = 42
MIN_SFT, MIN_EVAL = 100, 30


def chave(p):
    return re.sub(r"\s+", " ", recompensa.sem_acento(p)).strip(" ?.!")


def ler_treino(arquivo):
    """Blocos P:/R:/SQL: (continuam nas linhas seguintes). Devolve lista de dicts."""
    blocos, atual, campo = [], None, None
    for l in Path(arquivo).read_text(encoding="utf-8").splitlines():
        if l.lstrip().startswith("#"):
            continue
        m = re.match(r"^\s*(P|R|SQL):\s*(.*)", l)
        if m:
            c, v = m.group(1), m.group(2).strip()
            if c == "P":
                atual = {"P": v, "R": "", "SQL": ""}
                blocos.append(atual)
            elif atual is None:
                continue
            else:
                atual[c] = v
            campo = c
        elif atual is not None and campo and l.strip():
            atual[campo] += " " + l.strip()
    return blocos


def sql_de(texto):
    """Aceita SQL puro ou entre crases/```; devolve o SQL validado pela guarda do gms_ia ou None."""
    t = texto.strip().strip("`").strip()
    t = re.sub(r"^sql\s", "", t, flags=re.I)
    try:
        return gms_ia.extrai_sql(t)
    except ValueError:
        return None


def ler_memoria(arquivo):
    linhas = Path(arquivo).read_text(encoding="utf-8").splitlines()
    ok, erros = [], []
    for _, t in gms_ia.entradas(linhas, gms_ia.SEC_VAL):
        m = re.match(r"^\[(.+?)\] P: (.*?) SQL: `(.*)`$", t)
        if m:
            ok.append((m.group(2), m.group(3)))
    for _, t in gms_ia.entradas(linhas, gms_ia.SEC_ERR):
        m = re.match(r"^\[(.+?)\] P: (.*?) ERRADO: `(.*?)` CORRECAO: (.*)$", t)
        if m:
            erros.append((m.group(2), m.group(3)))
    return ok, erros


def bloco(sql):
    return "```sql\n" + sql + "\n```"


def gravar_jsonl(caminho, itens):
    with open(caminho, "w", encoding="utf-8", newline="\n") as f:
        for it in itens:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")


def principal(argv=None):
    ap = argparse.ArgumentParser(description="Exporta o pacote de treino por reforco")
    ap.add_argument("itens", nargs="*", help="[pasta_dados] [arquivos de treino .md]")
    ap.add_argument("--memoria", default=str(gms_ia.AQUI / "memoria.md"))
    ap.add_argument("--saida", default=str(AQUI))
    a = ap.parse_args(argv)
    pasta, arquivos = "dados", []
    for i, x in enumerate(a.itens):
        if i == 0 and Path(x).is_dir():
            pasta = x
        else:
            arquivos.append(x)
    saida = Path(a.saida)
    saida.mkdir(parents=True, exist_ok=True)

    # prompt de sistema = o do gms_ia, SEM a memoria (para a resposta nao aparecer dentro do proprio prompt)
    gms_ia.MEMORIA = Path(tempfile.mkdtemp()) / "vazia.md"
    gms_ia.preparar(pasta)
    con = gms_ia.ESTADO["con"]

    qs = {}

    def q(p):
        return qs.setdefault(chave(p), {"P": p.strip(), "ok": None, "ref": None, "R": "", "erros": []})

    memoria = Path(a.memoria)
    mem_ok, mem_err = ler_memoria(memoria) if memoria.exists() else ([], [])
    if not memoria.exists():
        print(f"AVISO: {memoria} nao existe; sigo so com os arquivos de treino.")
    for p, sql in mem_ok:
        q(p)["ok"] = sql
    for p, sql in mem_err:
        q(p)["erros"].append(sql)
    for arq in arquivos:
        for b in ler_treino(arq):
            d = q(b["P"])
            d["R"] = b["R"] or d["R"]
            if b["SQL"]:
                d["ref"] = b["SQL"]

    invalidas = 0
    itens = []
    for d in qs.values():
        d["ref_json"] = None
        for campo in ("ref", "ok"):
            if d[campo]:
                sql = sql_de(d[campo])
                try:
                    if not sql:
                        raise ValueError("fora da guarda")
                    rj = json.dumps(recompensa.linhas_json(recompensa.executar(con, sql, 60)), ensure_ascii=False)
                    if rj != "[]" and not d["ref_json"]:  # gabarito vazio nao serve de gabarito
                        d["ref_json"] = rj
                    d[campo] = sql
                except Exception as e:
                    print(f"AVISO: SQL {campo} descartado ({str(e)[:80]}): {d['P'][:60]}")
                    d[campo] = None
                    invalidas += 1
        d["erros"] = [s for s in (sql_de(e) for e in d["erros"]) if s]
        d["certo"] = d["ref"] or d["ok"]
        d["gab"] = recompensa.tem_gabarito({"ref_json": d["ref_json"], "esperado": d["R"]})
        itens.append(d)

    # eval estavel: eval_ids.txt so cresce; quem ja esteve no eval nunca vai ao treino
    ids_arq = saida / "eval_ids.txt"
    ids = [l.strip() for l in ids_arq.read_text(encoding="utf-8").splitlines() if l.strip()] if ids_arq.exists() else []
    itens.sort(key=lambda d: chave(d["P"]))
    elegiveis = [d for d in itens if d["gab"]]
    ja = [d for d in elegiveis if chave(d["P"]) in set(ids)]
    meta = max(1, round(len(elegiveis) * FRACAO_EVAL)) if len(elegiveis) >= 3 else 0
    novos = sorted((d for d in elegiveis if chave(d["P"]) not in set(ids)),
                   key=lambda d: hashlib.sha1((str(SEMENTE) + chave(d["P"])).encode()).hexdigest())
    for d in novos[:max(0, meta - len(ja))]:
        ids.append(chave(d["P"]))
    if ids:
        ids_arq.write_text("\n".join(ids) + "\n", encoding="utf-8", newline="\n")
    conj_ids = set(ids)
    em_eval = {chave(d["P"]) for d in elegiveis if chave(d["P"]) in conj_ids}

    sft, dpo, grpo, ev = [], [], [], []
    sem_par = 0
    for d in itens:
        prompt = [{"role": "system", "content": gms_ia.montar_sistema(d["P"])}, {"role": "user", "content": d["P"]}]
        base = {"pergunta": d["P"], "esperado": d["R"], "sql_ref": d["certo"] or "", "ref_json": d["ref_json"] or ""}
        if chave(d["P"]) in em_eval:
            ev.append({"prompt": prompt, **base})
        if chave(d["P"]) in conj_ids:
            continue
        if d["certo"]:
            sft.append({"prompt": prompt, "completion": [{"role": "assistant", "content": bloco(d["certo"])}]})
        if d["erros"]:
            if d["certo"]:
                for e in d["erros"]:
                    dpo.append({"prompt": prompt, "chosen": [{"role": "assistant", "content": bloco(d["certo"])}],
                                "rejected": [{"role": "assistant", "content": bloco(e)}]})
            else:
                sem_par += len(d["erros"])
        if d["gab"]:
            grpo.append({"prompt": prompt, **base})

    gravar_jsonl(saida / "sft.jsonl", sft)
    gravar_jsonl(saida / "dpo.jsonl", dpo)
    gravar_jsonl(saida / "grpo.jsonl", grpo)
    gravar_jsonl(saida / "eval.jsonl", ev)

    pacote = saida / "pacote_treino.zip"
    with zipfile.ZipFile(pacote, "w", zipfile.ZIP_DEFLATED) as z:
        for n in ("sft", "dpo", "grpo", "eval"):
            z.write(saida / f"{n}.jsonl", f"{n}.jsonl")
        for p in sorted((Path(pasta) / ".cache").glob("*.parquet")):
            z.write(p, f"dados/.cache/{p.name}")
        mapa = Path(pasta) / "mapa_dados.md"
        if mapa.exists():
            z.write(mapa, "dados/mapa_dados.md")
        if gms_ia.GLOSSARIO.exists():
            z.write(gms_ia.GLOSSARIO, "glossario.md")
        for f in (gms_ia.AQUI / "gms_ia.py", gms_ia.AQUI / "gms_mapear.py", AQUI / "recompensa.py"):
            z.write(f, f.name)

    print(f"\nPerguntas unicas: {len(itens)} (SQL descartado por erro/guarda: {invalidas})")
    print(f"sft.jsonl:  {len(sft)}")
    print(f"dpo.jsonl:  {len(dpo)}  (erros sem SQL certo para formar par, pulados: {sem_par})")
    print(f"grpo.jsonl: {len(grpo)}")
    print(f"eval.jsonl: {len(ev)}")
    print(f"Pacote: {pacote}")
    if len(sft) < MIN_SFT:
        print(f"AVISO: so {len(sft)} exemplos de SFT (< {MIN_SFT}). Pouco para treinar; junte mais perguntas validadas.")
    if len(ev) < MIN_EVAL:
        print(f"AVISO: so {len(ev)} perguntas de avaliacao (< {MIN_EVAL}). O placar vai oscilar muito.")
    if not dpo:
        print("AVISO: sem pares para DPO; o caderno vai pular essa etapa.")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    principal()
