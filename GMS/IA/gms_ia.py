# gms_ia.py - pergunte em portugues aos Excel da manufatura. Tudo local (Ollama + DuckDB).
# Uso:  python gms_ia.py [pasta_dados]                 (padrao: dados)
#       python gms_ia.py [pasta] --treinar treino.md   (perguntas P:/R: para treinar a memoria)
#       python gms_ia.py --limpar                      (limpa a memoria.md)
# Modelo: variavel GMS_MODELO (padrao qwen3:8b). Nada vai para a internet.
import argparse
import json
import os
import re
import sys
import threading
import time
import unicodedata
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

import duckdb
import gms_mapear

AQUI = Path(__file__).resolve().parent
MEMORIA = AQUI / "memoria.md"
MODELO_ARQ = AQUI / "memoria_modelo.md"
GLOSSARIO = AQUI / "glossario.md"
MODELO = os.environ.get("GMS_MODELO", "qwen3:8b")
URL = "http://localhost:11434/api/chat"
PROIBIDO = re.compile(r"\b(insert|update|delete|drop|create|alter|copy|attach|detach|install|load|export|pragma|set|call"
                      r"|read_\w+|glob)\b", re.I)

SEC_FATOS, SEC_VAL, SEC_ERR, SEC_PLAC = "Fatos", "Perguntas validadas", "Erros a evitar", "Placar"
MODELO_MINIMO = "# Memoria da IA da manufatura\n\n## Fatos\n\n## Perguntas validadas\n\n## Erros a evitar\n\n## Placar\n"
ESTADO = {"esquema": "", "mapa": "", "con": None}
TEMPO_MAX = 60


class ErroOllama(Exception):
    pass


def hoje():
    return date.today().isoformat()


def uma_linha(texto):
    return re.sub(r"\s+", " ", str(texto)).strip()


def cr(sql):
    """SQL em uma linha e sem crase (a crase delimita o SQL na memoria)."""
    return uma_linha(sql).replace("`", '"')


def sem_acento(t):
    t = unicodedata.normalize("NFKD", t)
    return "".join(c for c in t if not unicodedata.combining(c)).lower()


# ---------------------------------------------------------------- modelo de linguagem
def chat(mensagens):
    corpo = json.dumps({"model": MODELO, "messages": mensagens, "stream": False,
                        "think": False, "options": {"temperature": 0, "num_ctx": 8192}}).encode()
    req = urllib.request.Request(URL, corpo, {"Content-Type": "application/json"})
    try:
        texto = json.loads(urllib.request.build_opener(urllib.request.ProxyHandler({})).open(req, timeout=900).read())["message"]["content"]
    except (urllib.error.URLError, ConnectionError, TimeoutError) as e:
        raise ErroOllama(str(e))
    return re.sub(r"<think>.*?</think>", "", texto, flags=re.S).strip()


def sem_literais(sql):
    """Tira textos entre aspas e comentarios, so para conferir as palavras proibidas."""
    t = re.sub(r"'(?:[^']|'')*'", "''", sql)
    t = re.sub(r'"(?:[^"]|"")*"', '""', t)
    t = re.sub(r"/\*.*?\*/", " ", t, flags=re.S)
    return re.sub(r"--[^\n]*", " ", t).strip()


def extrai_sql(texto):
    m = re.search(r"```(?:sql)?\s*(.*?)```", texto, re.S | re.I)
    sql = (m.group(1) if m else texto).strip().rstrip(";").strip()
    t = sem_literais(sql).rstrip(";").strip()
    if ";" in t or not re.match(r"(select|with)\b", t, re.I) or PROIBIDO.search(t):
        raise ValueError("so aceito uma consulta SELECT de leitura")
    return sql


# ---------------------------------------------------------------- memoria em .md
def ler_memoria():
    if not MEMORIA.exists():
        modelo = MODELO_ARQ.read_text(encoding="utf-8") if MODELO_ARQ.exists() else MODELO_MINIMO
        MEMORIA.write_text(modelo, encoding="utf-8", newline="\n")
    return MEMORIA.read_text(encoding="utf-8").splitlines()


def gravar_memoria(linhas):
    tmp = MEMORIA.with_suffix(".tmp")
    tmp.write_text("\n".join(linhas).rstrip("\n") + "\n", encoding="utf-8", newline="\n")
    for _ in range(3):
        try:
            os.replace(tmp, MEMORIA)
            return True
        except PermissionError:
            time.sleep(0.5)
    print(f"AVISO: nao consegui gravar {MEMORIA.name} (esta aberto em outro programa?).")
    return False


def limites_secao(linhas, secao):
    ini = next((i for i, l in enumerate(linhas) if l.strip().lower() == f"## {secao}".lower()), None)
    if ini is None:
        return None, None
    fim = next((j for j in range(ini + 1, len(linhas)) if linhas[j].startswith("## ")), len(linhas))
    return ini, fim


def anexar(secao, texto):
    """Acrescenta uma linha no fim da secao. Nao mexe em mais nada do arquivo."""
    linhas = ler_memoria()
    ini, fim = limites_secao(linhas, secao)
    if ini is None:
        linhas += ["", f"## {secao}", ""]
        ini, fim = len(linhas) - 2, len(linhas)
    pos = fim
    while pos > ini + 1 and not linhas[pos - 1].strip():
        pos -= 1
    linhas.insert(pos, "- " + uma_linha(texto))
    if pos + 1 < len(linhas) and linhas[pos + 1].strip():
        linhas.insert(pos + 1, "")
    if not gravar_memoria(linhas):
        print(f"Copie a mao para a secao '{secao}' da memoria.md:\n- {uma_linha(texto)}")


def entradas(linhas, secao):
    ini, fim = limites_secao(linhas, secao)
    if ini is None:
        return []
    return [(i, linhas[i][2:]) for i in range(ini + 1, fim) if linhas[i].startswith("- ")]


def palavras(texto):
    return {w for w in re.findall(r"[a-z0-9]{3,}", sem_acento(texto))}


def parecidas(pergunta, itens, n):
    """itens: lista de (texto_para_comparar, texto_completo). Devolve as n com mais palavras em comum."""
    alvo = palavras(pergunta)
    pont = []
    for ordem, (comparar, completo) in enumerate(itens):
        s = len(alvo & palavras(comparar))
        if s > 0:
            pont.append((s, ordem, completo))
    pont.sort(key=lambda x: (-x[0], -x[1]))
    return [c for _, _, c in pont[:n]]


def memoria_para_prompt(pergunta):
    linhas = ler_memoria()
    fatos = [t for _, t in entradas(linhas, SEC_FATOS)][-30:]
    validas = []
    for _, t in entradas(linhas, SEC_VAL):
        m = re.match(r"^\[(.+?)\] P: (.*?) SQL: `(.*)`$", t)
        if m:
            validas.append((m.group(2), f"Pergunta: {m.group(2)}\nSQL: {m.group(3)}"))
    erros = []
    for _, t in entradas(linhas, SEC_ERR):
        m = re.match(r"^\[(.+?)\] P: (.*?) ERRADO: `(.*?)` CORRECAO: (.*)$", t)
        if m:
            erros.append((m.group(2), f"Pergunta: {m.group(2)}\nSQL errado: {m.group(3)}\nCorrecao: {m.group(4)}"))
    partes = []
    if fatos:
        partes.append("Fatos ja conhecidos:\n" + "\n".join("- " + f for f in fatos))
    ex = parecidas(pergunta, validas, 8)
    if ex:
        partes.append("Exemplos aprovados (use o mesmo estilo):\n" + "\n\n".join(ex))
    er = parecidas(pergunta, erros, 4)
    if er:
        partes.append("Erros a evitar:\n" + "\n\n".join(er))
    return "\n\n".join(partes)


# ---------------------------------------------------------------- dados
def esquema_texto(con, tabelas):
    partes = []
    for t in tabelas:
        cols = con.execute(f'DESCRIBE "{t}"').fetchall()
        exemplo = [tuple(str(v)[:30] for v in r) for r in con.execute(f'SELECT * FROM "{t}" LIMIT 3').fetchall()]
        partes.append(f"Tabela {t}: " + ", ".join(f'"{c[0]}" {c[1]}' for c in cols) + f"\n  exemplo de linhas: {exemplo}")
    return "\n".join(partes)


def travar(con, pasta):
    """Limites de memoria/tempo e acesso so ao cache. A IA nao consegue abrir outros arquivos."""
    cache = (Path(pasta) / ".cache").resolve().as_posix().replace("'", "''")
    con.execute("SET memory_limit='4GB'")
    con.execute("SET threads=2")
    con.execute(f"SET allowed_directories=['{cache}']")
    con.execute("SET enable_external_access=false")
    con.execute("SET lock_configuration=true")


def preparar(pasta):
    tabelas = gms_mapear.atualizar_cache(pasta)
    if not tabelas:
        sys.exit(f"Nenhum .xlsx, .xlsm ou .csv em {pasta}")
    mapa = Path(pasta) / "mapa_dados.md"
    manifesto = Path(pasta) / ".cache" / "manifest.json"
    if not mapa.exists() or mapa.stat().st_mtime < manifesto.stat().st_mtime:
        print("Os dados mudaram (ou nao ha mapa). Atualizando o mapa_dados.md ...")
        gms_mapear.principal(pasta)
    con = gms_mapear.abrir(pasta, tabelas)
    texto = mapa.read_text(encoding="utf-8")
    i = texto.find("## Ligacoes candidatas")
    j = texto.find(gms_mapear.NOTAS)
    if i >= 0 and j > i:
        contexto = texto[i:j][:8000] + "\n" + texto[j:]
    else:
        contexto = texto[-8000:]
    ESTADO.update(con=con, esquema=esquema_texto(con, tabelas), mapa=contexto)
    travar(con, pasta)
    return tabelas


def montar_sistema(pergunta):
    glos = GLOSSARIO.read_text(encoding="utf-8") if GLOSSARIO.exists() else ""
    return ("Voce escreve UMA consulta SQL do DuckDB que responde a pergunta. Use so as tabelas e colunas abaixo, "
            "com nomes entre aspas duplas. Para cruzar tabelas use as ligacoes do mapa. "
            "Responda so com o SQL dentro de ```sql```.\n\n"
            f"{ESTADO['esquema']}\n\nMapa de ligacoes e notas:\n{ESTADO['mapa']}\n\n"
            f"Glossario da fabrica:\n{glos}\n\n{memoria_para_prompt(pergunta)}")


# ---------------------------------------------------------------- uma pergunta
def executar(sql):
    con = ESTADO["con"]
    cronometro = threading.Timer(TEMPO_MAX, con.interrupt)
    cronometro.start()
    try:
        cur = con.execute(f"SELECT * FROM (\n{sql}\n) LIMIT 200")
        return [d[0] for d in cur.description], cur.fetchall()
    except duckdb.InterruptException:
        raise RuntimeError(f"a consulta passou de {TEMPO_MAX} segundos e foi cancelada; peca algo mais simples")
    finally:
        cronometro.cancel()



def perguntar(pergunta):
    """Devolve dict com sql, resposta e licao (texto ou None); None se nao deu para montar a consulta."""
    msgs = [{"role": "system", "content": montar_sistema(pergunta)}, {"role": "user", "content": pergunta}]
    falha = None
    for tentativa in range(2):
        bruto, sql = "", ""
        try:
            bruto = chat(msgs)
            sql = extrai_sql(bruto)
            print(f"\nSQL:\n{sql}")
            colunas, linhas = executar(sql)
            break
        except ErroOllama:
            raise
        except Exception as e:
            print(f"(erro: {e})")
            if tentativa == 0:
                falha = (sql or uma_linha(bruto)[:300], str(e))
            msgs += [{"role": "assistant", "content": bruto},
                     {"role": "user", "content": f"Deu erro: {e}. Corrija e mande so o SQL."}]
    else:
        print("Nao consegui montar a consulta. Reescreva a pergunta ou melhore o glossario.")
        return None
    resultado = "\n".join([" | ".join(colunas)] + [" | ".join(map(str, l)) for l in linhas])
    print(f"\nResultado ({len(linhas)} linhas):\n{resultado[:2000]}")
    resposta = chat([{"role": "user", "content":
        f"Pergunta: {pergunta}\nSQL usado: {sql}\nResultado:\n{resultado[:6000]}\n\n"
        "Responda em portugues, curto, usando SO os numeros do resultado. Se o resultado estiver vazio, diga isso."}])
    print(f"\nResposta: {resposta}")
    licao = None
    if falha:
        licao = (f"[{hoje()}] Pergunta \"{uma_linha(pergunta)}\": o SQL `{uma_linha(falha[0])}` deu erro "
                 f"({uma_linha(falha[1])[:200]}); funcionou: `{uma_linha(sql)}` (a conferir)")
        anexar(SEC_FATOS, licao)
        print("(Anotei uma licao em Fatos, marcada a conferir.)")
    return {"sql": sql, "resposta": resposta, "licao": licao}


def pedir_nota(pergunta, sql):
    """True = certo (gravado), False = errado (gravado), None = nao gravou."""
    r = input("\nCerto? '+' grava como certo, '- texto' grava a correcao, Enter nao grava: ").strip()
    if r == "+":
        anexar(SEC_VAL, f"[{hoje()}] P: {uma_linha(pergunta)} SQL: `{cr(sql)}`")
        print("Gravado em Perguntas validadas.")
        return True
    if r.startswith("-"):
        corr = r[1:].strip() or input("Qual era o certo? ").strip()
        if not corr:
            print("Sem correcao, nao gravei.")
            return None
        anexar(SEC_ERR, f"[{hoje()}] P: {uma_linha(pergunta)} ERRADO: `{cr(sql)}` CORRECAO: {corr}")
        print("Gravado em Erros a evitar.")
        return False
    return None


# ---------------------------------------------------------------- modos
def conversar():
    print(f"Modelo {MODELO}. Linha vazia para sair.")
    while True:
        pergunta = input("\nPergunta: ").strip()
        if not pergunta:
            break
        res = perguntar(pergunta)
        if res:
            pedir_nota(pergunta, res["sql"])


def ler_treino(arquivo):
    pares, atual, campo = [], None, None
    for l in Path(arquivo).read_text(encoding="utf-8").splitlines():
        if l.lstrip().startswith("#"):
            continue
        m = re.match(r"^\s*P:\s*(.*)", l)
        if m:
            atual, campo = {"P": m.group(1).strip(), "R": ""}, "P"
            pares.append(atual)
            continue
        m = re.match(r"^\s*R:\s*(.*)", l)
        if m and atual is not None:
            atual["R"], campo = m.group(1).strip(), "R"
            continue
        if atual is not None and campo and l.strip():
            atual[campo] += " " + l.strip()
    return pares


def treinar(arquivo):
    pares = ler_treino(arquivo)
    if not pares:
        sys.exit("Nao achei blocos 'P:' e 'R:' no arquivo.")
    acertos = total = 0
    for k, par in enumerate(pares, 1):
        print(f"\n===== Pergunta {k} de {len(pares)} =====\n{par['P']}")
        res = perguntar(par["P"])
        if not res:
            total += 1
            print("Contei como erro (sem consulta).")
            continue
        print(f"\nEsperado: {par['R'] or '(sem resposta esperada)'}")
        nota = pedir_nota(par["P"], res["sql"])
        if nota is not None:
            total += 1
            acertos += 1 if nota else 0
    if total:
        anexar(SEC_PLAC, f"[{hoje()}] acertos {acertos}/{total} | modelo {MODELO}")
        print(f"\nPlacar: {acertos}/{total}. Gravado em Placar.")
    else:
        print("\nNenhuma pergunta avaliada, placar nao gravado.")


def limpar():
    linhas = ler_memoria()
    remover, trocar = set(), {}

    def chave(secao, t):
        t = re.sub(r"^\[[^\]]*\]\s*", "", t)
        t = t.replace("(a conferir)", "")
        return uma_linha(t).lower()

    repetidas = 0
    for secao in (SEC_FATOS, SEC_VAL, SEC_ERR):
        vistos = set()
        for i, t in entradas(linhas, secao):
            k = chave(secao, t)
            if k in vistos:
                remover.add(i)
                repetidas += 1
            vistos.add(k)
    print(f"Repetidas a remover: {repetidas}")
    confirmadas = apagadas = 0
    for i, t in entradas(linhas, SEC_FATOS):
        if i in remover or "(a conferir)" not in t:
            continue
        print(f"\nA conferir:\n  {t}")
        r = input("  c = confirmar (vira fato), a = apagar, Enter = manter: ").strip().lower()
        if r == "c":
            trocar[i] = "- " + t.replace("(a conferir)", f"(confirmado em {hoje()})")
            confirmadas += 1
        elif r == "a":
            remover.add(i)
            apagadas += 1
    if not (remover or trocar):
        print("Nada para mudar.")
        return
    MEMORIA.with_name("memoria.bak.md").write_text("\n".join(linhas) + "\n", encoding="utf-8", newline="\n")
    novas = [trocar.get(i, l) for i, l in enumerate(linhas) if i not in remover]
    if not gravar_memoria(novas):
        print("Nada foi alterado na memoria.md.")
        return
    print(f"Pronto: {repetidas} repetidas, {confirmadas} confirmadas, {apagadas} apagadas. Copia antiga em memoria.bak.md")


def main(argv=None):
    ap = argparse.ArgumentParser(description="IA local sobre os Excel da manufatura")
    ap.add_argument("pasta", nargs="?", default="dados", help="pasta com os Excel/CSV (padrao: dados)")
    ap.add_argument("--treinar", metavar="ARQUIVO.md", help="roda as perguntas P:/R: do arquivo")
    ap.add_argument("--limpar", action="store_true", help="limpa a memoria.md")
    a = ap.parse_args(argv)
    if a.limpar:
        return limpar()
    tabelas = preparar(a.pasta)
    print(f"Tabelas: {', '.join(tabelas)}")
    try:
        treinar(a.treinar) if a.treinar else conversar()
    except ErroOllama:
        sys.exit("Nao consegui falar com o Ollama. Ele esta aberto? (rode: ollama serve) "
                 f"E o modelo {MODELO} foi baixado? (ollama pull {MODELO})")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
