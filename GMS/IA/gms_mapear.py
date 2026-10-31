# gms_mapear.py - le os Excel/CSV de uma pasta, guarda em cache e escreve o mapa_dados.md.
# Uso: python gms_mapear.py [pasta_dados]      (padrao: dados)
# Tudo local. Nada vai para a internet.
import difflib
import json
import os
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path

import duckdb
import pandas as pd

EXTENSOES = {".xlsx", ".xlsm", ".csv"}
INI = "<!-- AUTO:INICIO (regenerado a cada execucao, nao edite aqui) -->"
FIM = "<!-- AUTO:FIM -->"
NOTAS = "## Notas do William"
NOTAS_PADRAO = (NOTAS + "\n\nEscreva aqui o que a IA precisa saber e o mapa nao descobre sozinho "
                "(o que e cada coluna, unidade, qual ligacao vale). Esta parte nunca e apagada.\n")
INTEIROS = ("TINYINT", "SMALLINT", "INTEGER", "BIGINT", "HUGEINT", "UTINYINT", "USMALLINT", "UINTEGER", "UBIGINT")
LIMITE_DISTINTOS = 200000


def norm(texto):
    t = unicodedata.normalize("NFKD", str(texto))
    t = "".join(c for c in t if not unicodedata.combining(c)).lower()
    t = re.sub(r"[^a-z0-9]+", "_", t).strip("_")
    return t or "x"


def nome_tabela(arquivo, aba):
    n = norm(arquivo) + (("__" + norm(aba)) if aba else "")
    return ("t_" + n) if n[0].isdigit() else n


def ler_arquivo(caminho):
    """Devolve {aba: DataFrame}. CSV usa a chave vazia."""
    if caminho.suffix.lower() == ".csv":
        ultimo = None
        for enc in ("utf-8-sig", "latin-1"):
            try:
                return {"": pd.read_csv(caminho, sep=None, engine="python", encoding=enc)}
            except UnicodeDecodeError as e:
                ultimo = e
        raise ultimo
    return pd.read_excel(caminho, sheet_name=None)


def limpar_df(df):
    df = df.dropna(how="all").dropna(axis=1, how="all").copy()
    novos, vistos = [], {}
    for i, c in enumerate(df.columns):
        n = f"col_{i + 1}" if str(c).startswith("Unnamed") else norm(c)
        base, k = n, 1
        while n in vistos:
            k += 1
            n = f"{base}_{k}"
        vistos[n] = 1
        novos.append(n)
    df.columns = novos
    for c in df.columns:
        s = df[c]
        if s.dtype == object:
            if len({type(v) for v in s.dropna()}) > 1:
                df[c] = s.map(lambda v: None if pd.isna(v) else str(v))
        elif str(s.dtype).startswith("float"):
            v = s.dropna()
            if len(v) and (v == v.round()).all() and v.abs().max() < 1e15:
                df[c] = s.astype("Int64")
    return df


def atualizar_cache(pasta, log=print):
    """Converte cada aba em parquet em <pasta>/.cache, so se o arquivo mudou. Devolve a lista de tabelas."""
    pasta = Path(pasta)
    if not pasta.is_dir():
        sys.exit(f"Pasta nao encontrada: {pasta}. Crie a pasta e coloque os Excel/CSV nela.")
    cache = pasta / ".cache"
    cache.mkdir(exist_ok=True)
    mf_path = cache / "manifest.json"
    try:
        manifesto = json.loads(mf_path.read_text(encoding="utf-8"))
    except Exception:
        manifesto = {}
    novo = {}
    con = duckdb.connect()
    arquivos = [p for p in sorted(pasta.rglob("*"))
                if p.is_file() and p.suffix.lower() in EXTENSOES
                and ".cache" not in p.parts and not p.name.startswith("~$")]
    # arquivos cujo cache ainda vale (guardam os nomes que ja tinham)
    em_dia = {}
    usados = set()
    for p in arquivos:
        rel = str(p.relative_to(pasta))
        ant = manifesto.get(rel)
        try:
            mt = p.stat().st_mtime
        except OSError:
            mt = None
        if ant and ant.get("mtime") == mt and all((cache / f"{t}.parquet").exists() for t in ant["tabelas"]):
            em_dia[rel] = ant
            usados.update(ant["tabelas"])
    for p in arquivos:
        rel = str(p.relative_to(pasta))
        if rel in em_dia:
            novo[rel] = em_dia[rel]
            continue
        ant = manifesto.get(rel)
        log(f"Lendo {rel} ...")
        try:
            mt = p.stat().st_mtime
            abas = ler_arquivo(p)
        except Exception as e:
            if ant:
                log(f"  AVISO: nao consegui ler {rel} ({e}). Mantive o cache antigo.")
                novo[rel] = ant
                usados.update(ant["tabelas"])
            else:
                log(f"  AVISO: nao consegui ler {rel} ({e}). Arquivo ignorado.")
            continue
        tabelas = []
        for aba, df in abas.items():
            try:
                df = limpar_df(df)
                if df.shape[1] == 0:
                    continue
                nome = base = nome_tabela(p.stem, aba)
                k = 1
                while nome in usados:
                    k += 1
                    nome = f"{base}_{k}"
                if nome != base:
                    log(f"  AVISO: o nome {base} ja existe; a aba '{aba}' de {rel} virou {nome}.")
                destino = str(cache / f"{nome}.parquet").replace("\\", "/").replace("'", "''")
                con.register("df_tmp", df)
                try:
                    con.execute(f"COPY (SELECT * FROM df_tmp) TO '{destino}' (FORMAT PARQUET)")
                finally:
                    con.unregister("df_tmp")
                usados.add(nome)
                tabelas.append(nome)
            except Exception as e:
                log(f"  AVISO: a aba '{aba}' de {rel} falhou ({e}). Segui para a proxima.")
        novo[rel] = {"mtime": mt, "tabelas": tabelas}
    validos = {t for v in novo.values() for t in v["tabelas"]}
    for f in cache.glob("*.parquet"):
        if f.stem not in validos:
            f.unlink()
    if novo != manifesto or not mf_path.exists():
        mf_path.write_text(json.dumps(novo, ensure_ascii=False, indent=1), encoding="utf-8")
    return sorted(validos)


def abrir(pasta, tabelas):
    """Conexao DuckDB em memoria com uma view por tabela, apontando para o cache."""
    con = duckdb.connect()
    for t in tabelas:
        caminho = str((Path(pasta) / ".cache" / f"{t}.parquet").resolve()).replace("\\", "/").replace("'", "''")
        con.execute(f'CREATE VIEW "{t}" AS SELECT * FROM read_parquet(\'{caminho}\')')
    return con


def categoria(tipo):
    if tipo in INTEIROS or tipo.startswith("VARCHAR"):
        return "id"
    if tipo.startswith(("DATE", "TIMESTAMP")):
        return "data"
    if tipo.startswith(("DOUBLE", "FLOAT", "DECIMAL")):
        return "num"
    return None


def txt(v, n=24):
    s = re.sub(r"\s+", " ", str(v)).replace("|", "/")
    return s if len(s) <= n else s[:n - 1] + "..."


def perfil(con, tabela):
    total = con.execute(f'SELECT count(*) FROM "{tabela}"').fetchone()[0]
    colunas = []
    for nome, tipo, *_ in con.execute(f'DESCRIBE "{tabela}"').fetchall():
        q = f'"{nome}"'
        nao_nulos, distintos = con.execute(f'SELECT count({q}), count(DISTINCT {q}) FROM "{tabela}"').fetchone()
        exemplos = [r[0] for r in con.execute(
            f'SELECT DISTINCT {q} FROM "{tabela}" WHERE {q} IS NOT NULL LIMIT 3').fetchall()]
        mn = mx = "-"
        if nao_nulos and not tipo.startswith(("VARCHAR", "BOOLEAN")):
            mn, mx = con.execute(f'SELECT min({q}), max({q}) FROM "{tabela}"').fetchone()
        vazio = (total - nao_nulos) * 100 / total if total else 0
        colunas.append({"nome": nome, "tipo": tipo, "vazio": vazio, "distintos": distintos,
                        "exemplos": exemplos, "min": mn, "max": mx})
    return total, colunas


def valores(con, tabela, coluna):
    q = f'"{coluna}"'
    linhas = con.execute(f'SELECT DISTINCT {q} FROM "{tabela}" WHERE {q} IS NOT NULL LIMIT {LIMITE_DISTINTOS + 1}').fetchall()
    if len(linhas) > LIMITE_DISTINTOS:
        return None
    return {str(r[0]).strip().upper() for r in linhas}


def achar_ligacoes(con, perfis):
    itens = []
    for t, (_, cols) in perfis.items():
        for c in cols:
            cat = categoria(c["tipo"])
            if cat is None or c["distintos"] == 0:
                continue
            vals = valores(con, t, c["nome"]) if cat == "id" and c["distintos"] >= 2 else None
            itens.append((t, c["nome"], cat, vals))
    achados = []
    for i in range(len(itens)):
        for j in range(i + 1, len(itens)):
            ta, ca, cata, va = itens[i]
            tb, cb, catb, vb = itens[j]
            if ta == tb or cata != catb:
                continue
            nome_igual = ca == cb
            nome_parecido = nome_igual or difflib.SequenceMatcher(None, ca, cb).ratio() >= 0.85
            inter = sobre = None
            if va and vb:
                inter = len(va & vb)
                sobre = inter / min(len(va), len(vb))
            por_valor = sobre is not None and sobre >= 0.8 and inter >= 5
            if sobre is not None and nome_parecido and inter >= 3 and sobre >= 0.2:
                motivo = "valores + nome" if por_valor else "nome parecido"
            elif por_valor:
                motivo = "valores + nome" if nome_parecido else "valores"
            elif nome_igual and cata in ("data", "num"):
                motivo = "so o nome"
            else:
                continue
            achados.append((sobre if sobre is not None else -1, f"{ta}.{ca}", f"{tb}.{cb}", sobre, inter, motivo))
    achados.sort(key=lambda x: (-x[0], x[1], x[2]))
    return achados[:200]


def ler_tmdl(raiz):
    """Le blocos 'relationship' (fromColumn/toColumn) de arquivos .tmdl e .tmdl.md."""
    saida = []
    if not raiz.is_dir():
        return saida
    for p in sorted(raiz.rglob("*")):
        if not p.is_file() or not p.name.lower().endswith((".tmdl", ".tmdl.md")):
            continue
        linhas = p.read_text(encoding="utf-8", errors="ignore").splitlines()
        i = 0
        while i < len(linhas):
            m = re.match(r"^(\s*)relationship\b", linhas[i])
            if not m:
                i += 1
                continue
            recuo = len(m.group(1))
            bloco = []
            i += 1
            while i < len(linhas) and (not linhas[i].strip() or len(linhas[i]) - len(linhas[i].lstrip()) > recuo):
                bloco.append(linhas[i])
                i += 1
            texto = "\n".join(bloco)
            de = re.search(r"fromColumn:\s*(.+)", texto)
            para = re.search(r"toColumn:\s*(.+)", texto)
            if de and para:
                saida.append((de.group(1).strip(), para.group(1).strip(), p.name))
    return saida


def gerar_auto(pasta, con, tabelas, perfis, ligacoes, tmdl):
    L = [f"# Mapa dos dados", "",
         f"Gerado em {datetime.now():%Y-%m-%d %H:%M} a partir de `{pasta}`. "
         "Nomes de tabela e coluna estao em minusculo e sem acento.", "",
         "## Tabelas e colunas", ""]
    for t in tabelas:
        total, cols = perfis[t]
        L += [f"### {t} ({total} linhas)", "",
              "| coluna | tipo | vazio % | distintos | exemplos | min | max |", "|---|---|---|---|---|---|---|"]
        for c in cols:
            L.append(f"| {c['nome']} | {c['tipo']} | {c['vazio']:.0f} | {c['distintos']} | "
                     f"{txt(', '.join(txt(e, 20) for e in c['exemplos']), 60)} | {txt(c['min'])} | {txt(c['max'])} |")
        L.append("")
    L += ["## Ligacoes candidatas (descobertas pelos dados)", "",
          "Sao palpites: confirme nas Notas do William antes de confiar.", ""]
    if ligacoes:
        L += ["| coluna A | coluna B | sobreposicao | em comum | motivo |", "|---|---|---|---|---|"]
        for _, a, b, sobre, inter, motivo in ligacoes:
            L.append(f"| {a} | {b} | {'-' if sobre is None else f'{sobre * 100:.0f}%'} | "
                     f"{'-' if inter is None else inter} | {motivo} |")
    else:
        L.append("Nenhuma ligacao encontrada.")
    L += ["", "## Ligacoes do modelo do BI", ""]
    if tmdl:
        L += ["| de | para | arquivo |", "|---|---|---|"] + [f"| {a} | {b} | {f} |" for a, b, f in tmdl]
    else:
        L.append("Nenhum bloco relationship encontrado nos arquivos .tmdl de GMS/PowerBI.")
    return "\n".join(L) + "\n"


def gravar_mapa(caminho, auto):
    notas = NOTAS_PADRAO
    if caminho.exists():
        antigo = caminho.read_text(encoding="utf-8")
        i = antigo.find(NOTAS)
        if i >= 0:
            notas = antigo[i:]
    if not notas.endswith("\n"):
        notas += "\n"
    tmp = caminho.with_name(caminho.name + ".tmp")
    tmp.write_text(f"{INI}\n{auto}{FIM}\n\n{notas}", encoding="utf-8", newline="\n")
    os.replace(tmp, caminho)


def principal(pasta="dados"):
    pasta = Path(pasta)
    tabelas = atualizar_cache(pasta)
    if not tabelas:
        sys.exit(f"Nenhum .xlsx, .xlsm ou .csv em {pasta}")
    con = abrir(pasta, tabelas)
    perfis = {t: perfil(con, t) for t in tabelas}
    ligacoes = achar_ligacoes(con, perfis)
    tmdl = ler_tmdl(Path(__file__).resolve().parent.parent / "PowerBI")
    gravar_mapa(pasta / "mapa_dados.md", gerar_auto(pasta, con, tabelas, perfis, ligacoes, tmdl))
    print(f"{len(tabelas)} tabelas, {len(ligacoes)} ligacoes candidatas, {len(tmdl)} ligacoes do BI.")
    print(f"Mapa gravado em {pasta / 'mapa_dados.md'}")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    principal(sys.argv[1] if len(sys.argv) > 1 else "dados")
