# recompensa.py - compara o resultado de um SQL com o esperado e pontua. Usado pelo caderno (Colab) e pelo avaliar.py.
# Usa a MESMA guarda de SQL do gms_ia.py (extrai_sql). Estar na mesma pasta que gms_ia.py e gms_mapear.py.
import json
import re
import threading
import unicodedata
from decimal import Decimal
from pathlib import Path

import duckdb
import gms_ia

TEMPO = 10          # segundos por consulta no treino/avaliacao
TOLERANCIA = 0.01   # 1%
_CACHE = {}


def abrir(pasta):
    """Conexao DuckDB so-leitura com uma view por parquet de <pasta>/.cache (mesma trava do gms_ia)."""
    pasta = Path(pasta)
    con = duckdb.connect()
    for p in sorted((pasta / ".cache").glob("*.parquet")):
        caminho = p.resolve().as_posix().replace("'", "''")
        con.execute(f'CREATE VIEW "{p.stem}" AS SELECT * FROM read_parquet(\'{caminho}\')')
    gms_ia.travar(con, pasta)
    return con


def executar(con, sql, tempo=TEMPO):
    """Roda o SQL com limite de tempo (mesmo LIMIT 200 do gms_ia). Devolve a lista de linhas."""
    cron = threading.Timer(tempo, con.interrupt)
    cron.start()
    try:
        return con.execute(f"SELECT * FROM (\n{sql}\n) LIMIT 200").fetchall()
    finally:
        cron.cancel()


def celula(v):
    if v is None:
        return None
    if isinstance(v, bool):
        return str(v)
    if isinstance(v, (int, float, Decimal)):
        return float(v)
    return str(v)


def linhas_json(linhas):
    return [[celula(v) for v in l] for l in linhas]


def sem_acento(t):
    t = unicodedata.normalize("NFKD", str(t))
    return "".join(c for c in t if not unicodedata.combining(c)).lower()


def datas_de(texto):
    """Datas do texto em ISO (aceita 2026-10-01 e 01/10/2026). Devolve (texto_sem_datas, [iso])."""
    iso = []

    def dmy(m):
        iso.append(f"{m.group(3)}-{int(m.group(2)):02d}-{int(m.group(1)):02d}")
        return " "

    def ymd(m):
        iso.append(m.group(0))
        return " "

    t = re.sub(r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b", dmy, str(texto))
    t = re.sub(r"\b\d{4}-\d{2}-\d{2}\b", ymd, t)
    return t, iso


def numeros(texto):
    """Numeros de um texto, aceitando 1.234,5 (BR) e 1234.5. '-' colado a um digito antes nao e sinal."""
    saida = []
    texto = re.sub(r"(?<=\d)-(?=\d)", " ", str(texto))  # '-' colado a digito anterior nao e sinal (5-2, datas)
    for m in re.findall(r"-?\d[\d.,]*", texto):
        m = m.rstrip(".,")
        if "," in m:
            m = m.replace(".", "").replace(",", ".")
        elif re.fullmatch(r"-?\d{1,3}(\.\d{3})+", m):
            m = m.replace(".", "")
        try:
            saida.append(float(m))
        except ValueError:
            pass
    return saida


def _igual(a, b):
    return abs(a - b) <= TOLERANCIA * max(abs(a), abs(b)) if (a or b) else True


def _casa_numeros(esperados, candidatos):
    pool = list(candidatos)
    for e in esperados:
        for i, c in enumerate(pool):
            if _igual(e, c):
                del pool[i]
                break
        else:
            return False
    return True


def _ref(item):
    """Linhas do gabarito (lista nao vazia) ou None. Gabarito vazio nao conta."""
    try:
        r = json.loads(item["ref_json"]) if item.get("ref_json") else None
    except ValueError:
        return None
    return r if r else None


def tem_gabarito(item):
    if _ref(item):
        return True
    esp = str(item.get("esperado") or "")
    return bool(numeros(esp)) or (bool(esp.strip()) and "conferir" not in esp.lower())


def _linha_casa(ref_linha, cand_linha):
    rn = [v for v in ref_linha if isinstance(v, float)]
    rt = [sem_acento(v).strip() for v in ref_linha if isinstance(v, str)]
    cn = [v for v in cand_linha if isinstance(v, float)]
    ct = {sem_acento(v).strip() for v in cand_linha if isinstance(v, str)}
    return _casa_numeros(rn, cn) and all(t in ct for t in rt)


def bate(linhas, item):
    """True se o resultado (linhas do DuckDB) tem a forma e os valores do esperado.
    Com SQL de referencia: mesmo numero de linhas, cada linha casa com uma linha do gabarito e no maximo 2x as celulas.
    Sem ele: numeros do texto esperado (tolerancia de 1%), no maximo (numeros + 1) linhas. Resultado vazio nunca vale."""
    if not linhas:
        return False
    cand = linhas_json(linhas)
    ref = _ref(item)
    if ref is not None:
        if len(cand) != len(ref) or sum(len(l) for l in cand) > 2 * sum(len(l) for l in ref):
            return False
        livres = list(range(len(cand)))
        for rl in ref:
            for i in livres:
                if _linha_casa([v for v in rl if v is not None], [v for v in cand[i] if v is not None]):
                    livres.remove(i)
                    break
            else:
                return False
        return True
    esp, datas = datas_de(item.get("esperado") or "")
    nums = numeros(esp)
    cel = [v for l in cand for v in l if v is not None]
    if nums or datas:
        if len(cand) > len(nums) + len(datas) + 1:
            return False
        alvo = " ".join(v for v in cel if isinstance(v, str))
        return _casa_numeros(nums, [v for v in cel if isinstance(v, float)]) and all(d in alvo for d in datas)
    palavras = re.findall(r"[a-z0-9]{4,}", sem_acento(esp))
    alvo = sem_acento(" ".join(v for v in cel if isinstance(v, str)))
    return bool(palavras) and all(w in alvo for w in palavras)


def texto_da(c):
    """Texto de uma completion do TRL (string ou lista de mensagens), sem <think>."""
    if isinstance(c, list):
        c = c[0].get("content", "") if c else ""
    return re.sub(r"<think>.*?</think>", "", str(c), flags=re.S).strip()


def tem_bloco(texto):
    return bool(re.search(r"```(?:sql)?\s*\S.*?```", texto, re.S | re.I))


def usa_tabela(con, sql):
    """Exige FROM numa tabela do cache (bloqueia SELECT 42, unnest(range(...)) e afins)."""
    chave = (id(con), "tabelas")
    if chave not in _CACHE:
        _CACHE[chave] = [r[0].lower() for r in con.execute("SELECT table_name FROM information_schema.tables").fetchall()]
    t = gms_ia.sem_literais(sql).lower()
    sql_l = sql.lower()
    return bool(re.search(r"\bfrom\b", t)) and any(nome in sql_l for nome in _CACHE[chave])


def analisar(con, texto, item, tempo=TEMPO):
    """Devolve dict(formato, leitura, executa, bate) para uma resposta do modelo."""
    chave = (id(con), texto, item.get("pergunta"))
    if chave in _CACHE:
        return _CACHE[chave]
    r = {"formato": tem_bloco(texto), "leitura": False, "executa": False, "bate": False, "erro": ""}
    try:
        sql = gms_ia.extrai_sql(texto)
        r["leitura"] = True
        linhas = executar(con, sql, tempo)
        r["executa"] = True
        r["bate"] = usa_tabela(con, sql) and bate(linhas, item)
    except Exception as e:
        r["erro"] = str(e)[:200]
    if len(_CACHE) > 5000:
        _CACHE.clear()
    _CACHE[chave] = r
    return r
