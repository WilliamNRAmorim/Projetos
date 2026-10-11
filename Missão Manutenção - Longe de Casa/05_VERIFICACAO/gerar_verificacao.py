# -*- coding: utf-8 -*-
"""
Gera os arquivos de verificação das peças:
  - VERIFICACAO_GERAL.xlsx (abas Verificar, Conferir códigos, Leia-me)
  - POR_CONFIANCA/SUB1_ALTA_70-100.xlsx, SUB2_MEDIA_40-69.xlsx, SUB3_BAIXA_0-39.xlsx
  - IDENTIFICADOR.html (funciona sem internet e sem Python)
  - dados/respostas.json (todas as respostas do aprendiz juntas)
  - STATUS_VERIFICACAO.xlsx (mesma lógica do atualizar_status.py)

Uso:  python gerar_verificacao.py
Antes de sobrescrever, copia os xlsx atuais para _backup/AAAA-MM-DD_HHMM/.
Todos os caminhos são relativos à pasta deste script.
"""
import os, re, io, sys, json, csv, glob, shutil, datetime, unicodedata, urllib.parse

# Caminho (opcional) do materiais.csv do PC do trabalho; colunas: grt;nome;descricao_fornecedor
CSV_GRT_EXTERNO = ""

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
BASE_XLSX = os.path.join(RAIZ, "BASE_MATERIAIS.xlsx")
DIR_MANUAIS = os.path.join(RAIZ, "02_MANUAIS")
DIR_FOTOS = os.path.join(RAIZ, "04_FOTOS")
CATALOGO_JSON = os.path.join(DIR_MANUAIS, "dados", "catalogo.json")
DIR_DADOS = os.path.join(AQUI, "dados")
IA_JSON = os.path.join(DIR_DADOS, "candidatos_ia.json")
IA_EXEMPLO_JSON = os.path.join(DIR_DADOS, "candidatos_ia_exemplo.json")
LEGADO_JSON = os.path.join(DIR_DADOS, "legado_verificacao.json")
RESPOSTAS_JSON = os.path.join(DIR_DADOS, "respostas.json")
RETRATO_JSON = os.path.join(DIR_DADOS, "retrato_geracao.json")   # o que a última geração escreveu nas colunas amarelas
CAMPOS_RESP = ("codigo_final", "nome_final", "parte_final", "obs")
GRT_CSV = os.path.join(DIR_DADOS, "grt_conhecidos.csv")
GERAL_XLSX = os.path.join(AQUI, "VERIFICACAO_GERAL.xlsx")
DIR_SUBS = os.path.join(AQUI, "POR_CONFIANCA")
STATUS_XLSX = os.path.join(AQUI, "STATUS_VERIFICACAO.xlsx")
HTML_SAIDA = os.path.join(AQUI, "IDENTIFICADOR.html")
HTML_MODELO = os.path.join(AQUI, "modelo_identificador.html")

EXC_PASTAS = {
    "ACIONADOR DA BONECA TEXTIL (1)": "ACIONADOR_DA_BONECA_TEXTIL",
    "ACIONADOR DA BONECA TEXTIL (2)": "ACIONADOR_DA_BONECA_TEXTIL",
    "ACIONADOR DA BONECA TEXTIL B1- 6164(3)": "ACIONADOR_DA_BONECA_TEXTIL_3",
    "MOLA CARRIER AZUL GRANDE": "MOLA_CARRIER_AZUL",
}
# do mais atual para o mais antigo
ORDEM_MANUAIS = ["COMUM26", "24C", "RB2", "COMUM18", "20C", "261"]
G_NI, G_LIVRE, G_COD, G_CONF = "NI", "Nome livre", "Código a conferir", "Conferir códigos"
ST_PEND, ST_OK, ST_NENHUMA, ST_FOTOS = "Pendente", "Conferido", "Nenhuma", "Mais fotos"

AZUL, MARROM, AMARELO_CLARO = "1F4E78", "7F6000", "FFF2CC"
ALTURA_LINHA = 135  # pontos
W_FOTO, H_FOTO = 300, 170
W_DES, H_DES = 210, 170


# ---------------------------------------------------------------- utilidades
def sem_acento(s):
    s = unicodedata.normalize("NFD", str(s))
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def hnorm(s):
    return sem_acento(s or "").strip().lower()


def norm_cod(s):
    return re.sub(r"\s+", "", str(s or "").upper())


def cod_chave(s):
    """Chave de comparação de código: usa só o primeiro de 'A / B'."""
    return norm_cod(str(s or "").split("/")[0])


def vazio(v):
    return v is None or str(v).strip() == ""


def txt(v):
    return "" if v is None else str(v).strip()


def agora_iso():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


def mtime_iso(path):
    return datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d %H:%M")


def chave_natural(s):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", str(s))]


# ---------------------------------------------------------------- catálogo
_CAT = {}


def catalogo():
    if not _CAT:
        d = json.load(open(CATALOGO_JSON, encoding="utf8"))
        _CAT["manuais"] = d["manuais"]
        _CAT["pecas"] = d["pecas"]
        idx = {}
        for p in d["pecas"]:
            idx.setdefault(norm_cod(p["codigo_norm"] or p["codigo"]), []).append(p)
        _CAT["idx"] = idx
        _CAT["rot2id"] = {m["rotulo"]: k for k, m in d["manuais"].items()}
    return _CAT


def ordem_ocorrencia(p):
    try:
        o = ORDEM_MANUAIS.index(p["manual"])
    except ValueError:
        o = 99
    return (o, p.get("pagina_desenho") or 0)


def achar_ocorrencia(codigo, manual=None, pagina=None):
    """Liga um código à ocorrência do catálogo (manual+página; senão o manual mais atual)."""
    idx = catalogo()["idx"]
    partes = [norm_cod(x) for x in str(codigo or "").split("/") if x.strip()]
    for k in partes:
        occ = idx.get(k)
        if not occ:
            continue
        if manual and pagina:
            ok = [o for o in occ if o["manual"] == manual and pagina in (o.get("pagina_lista"), o.get("pagina_desenho"))]
            if ok:
                return sorted(ok, key=ordem_ocorrencia)[0]
        return sorted(occ, key=ordem_ocorrencia)[0]
    return None


def ocorrencias_codigo(codigo):
    idx = catalogo()["idx"]
    for k in [norm_cod(x) for x in str(codigo or "").split("/") if x.strip()]:
        if k in idx:
            return sorted(idx[k], key=ordem_ocorrencia)
    return []


def recorte_de(p):
    """Imagem do desenho (relativa a 02_MANUAIS); cai na página inteira se faltar o recorte."""
    if not p:
        return ""
    r = p.get("recorte") or ""
    if r and os.path.exists(os.path.join(DIR_MANUAIS, r)):
        return r
    pm = p.get("pagina_marcada") or ""
    if pm and os.path.exists(os.path.join(DIR_MANUAIS, pm)):
        return pm
    return ""


# ---------------------------------------------------------------- GRT
def carregar_grt():
    """Mapa código normalizado -> (grt, nome)."""
    m = {}
    if os.path.exists(GRT_CSV):
        with open(GRT_CSV, encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f, delimiter=";"):
                if r.get("codigo") and r.get("grt"):
                    m[cod_chave(r["codigo"])] = (r["grt"].strip(), (r.get("nome") or "").strip())
    if CSV_GRT_EXTERNO and os.path.exists(CSV_GRT_EXTERNO):
        try:
            with open(CSV_GRT_EXTERNO, encoding="utf-8-sig", newline="") as f:
                for r in csv.DictReader(f, delimiter=";"):
                    k = cod_chave(r.get("descricao_fornecedor") or "")
                    if k and r.get("grt") and k not in m:
                        m[k] = (r["grt"].strip(), (r.get("nome") or "").strip())
        except Exception as e:
            print("Aviso: não consegui ler CSV_GRT_EXTERNO:", e)
    return m


# ---------------------------------------------------------------- BASE
def pasta_de_fotos(mat, pasta):
    if not vazio(pasta):
        return str(pasta).strip()
    if mat in EXC_PASTAS:
        return EXC_PASTAS[mat]
    n = re.sub(r"\s*\(\d+\)\s*$", "", mat)
    return re.sub(r"[\W_]+", "_", n.upper()).strip("_")


def listar_fotos(pasta):
    d = os.path.join(DIR_FOTOS, pasta)
    if not pasta or not os.path.isdir(d):
        return []
    return sorted(f for f in os.listdir(d) if f.lower().endswith((".jpg", ".jpeg", ".png")))


def ler_base():
    import openpyxl
    ws = openpyxl.load_workbook(BASE_XLSX, data_only=True)["Materiais"]
    cab = [c.value for c in ws[1]]
    linhas = []
    for r in ws.iter_rows(min_row=2, values_only=True):
        d = dict(zip(cab, r))
        if vazio(d.get("Material (como anotado)")):
            continue
        linhas.append(d)
    return linhas


def grupo_de(d):
    st = txt(d.get("Status"))
    if st == "Encontrado nos manuais":
        return G_CONF
    if st.startswith("Código não"):
        return G_COD
    if txt(d.get("Tipo")).startswith("Não identificado"):
        return G_NI
    return G_LIVRE


# ---------------------------------------------------------------- legado (candidatas antigas)
def parse_cand_txt(t):
    """'CÓDIGO\\nDESCRIÇÃO\\nParte\\nManual pX · NN%' -> dict."""
    linhas = [l.strip() for l in str(t).split("\n") if l.strip()]
    if not linhas:
        return None
    c = {"codigo": linhas[0], "descricao": linhas[1] if len(linhas) > 1 else "",
         "parte": linhas[2] if len(linhas) > 3 else "", "manual": "", "pagina": None, "pct": None}
    m = re.search(r"^(.*?)\s+p(\d+)\s*·\s*(\d+)\s*%", linhas[-1])
    if m:
        c["manual"] = catalogo()["rot2id"].get(m.group(1).strip(), "")
        c["pagina"] = int(m.group(2))
        c["pct"] = int(m.group(3))
    return c


def _indices_cabecalho(cab):
    """Mapeia colunas pelo NOME do cabeçalho."""
    ix = {"cands": []}
    for i, h in enumerate(cab):
        n = hnorm(h)
        if not n:
            continue
        if re.match(r"candidata \d", n):
            ix["cands"].append((int(re.match(r"candidata (\d)", n).group(1)), i))
        elif n.startswith("material"):
            ix.setdefault("mat", i)
        elif n.startswith("aprendiz") or n.startswith("candidata escolhida"):
            ix.setdefault("resp", i)
        elif "codigo" in n and "final" in n:
            ix.setdefault("cod", i)
        elif "nome" in n and "final" in n:
            ix.setdefault("nome", i)
        elif "parte" in n and "final" in n:
            ix.setdefault("parte", i)
        elif n.startswith("observ"):
            ix.setdefault("obs", i)
        elif "medidas" in n and "anotadas" in n:
            ix.setdefault("med", i)
        elif n == "status":
            ix.setdefault("status", i)
        elif n == "data":
            ix.setdefault("data", i)
        elif n.startswith("o que"):
            ix.setdefault("oque", i)
        elif n.startswith("nome sugerido"):
            ix.setdefault("nomesug", i)
        elif n.startswith("medir"):
            ix.setdefault("medir", i)
        elif n.startswith("maior"):
            ix.setdefault("maior", i)
    ix["cands"].sort()
    return ix


def _abrir_xlsx(path, obrigatorio=False):
    """obrigatorio=True (VERIFICACAO_GERAL): se não der para ler, PARA tudo, para não sobrescrever respostas."""
    import openpyxl
    try:
        return openpyxl.load_workbook(path, read_only=True, data_only=True)
    except Exception as e:
        if obrigatorio:
            raise SystemExit(f"ERRO: não consegui ler {os.path.basename(path)} ({e}).\n"
                             "Nada foi alterado. Espere o OneDrive terminar de sincronizar, feche o arquivo e rode de novo.")
        print(f"AVISO: não consegui abrir {os.path.basename(path)} ({e}). Ignorado nesta rodada.")
        return None


def atualizar_legado():
    """Guarda as candidatas/dados do VERIFICACAO_GERAL no formato antigo (uma vez), p/ reaproveitar."""
    legado = {}
    if os.path.exists(LEGADO_JSON):
        legado = json.load(open(LEGADO_JSON, encoding="utf8"))
    if not os.path.exists(GERAL_XLSX):
        return legado
    wb = _abrir_xlsx(GERAL_XLSX, obrigatorio=True)
    for ws in wb.worksheets:
        linhas = ws.iter_rows(values_only=True)
        cab = next(linhas, None)
        if not cab:
            continue
        ix = _indices_cabecalho(cab)
        antigo = "mat" in ix and ix["cands"] and not any(hnorm(h).startswith("desenho") for h in cab)
        if not antigo:
            continue
        novo = {}
        for r in linhas:
            mat = txt(r[ix["mat"]]) if ix["mat"] < len(r) else ""
            if not mat:
                continue
            g = lambda k: txt(r[ix[k]]) if k in ix and ix[k] < len(r) else ""
            grt_txt = ""
            for i, h in enumerate(cab):
                if hnorm(h).startswith("ja no grt") and i < len(r):
                    grt_txt = txt(r[i])
            todas = [txt(r[i]) for _, i in ix["cands"] if i < len(r) and txt(r[i])]
            # a planilha antiga deslocava colunas quando havia menos de 5 candidatas: texto sem "pág · %" não é candidata
            validas = [t for t in todas if re.search(r"p\d+\s*·\s*\d+\s*%\s*$", t.strip().split(chr(10))[-1])]
            sobra = [t for t in todas if t not in validas]
            medir = g("medir") or (sobra[0] if sobra else "")
            novo[mat] = {"oque": g("oque"), "nome": g("nomesug"), "medir": medir, "maior": g("maior"),
                         "grt": grt_txt, "cands": validas}
        legado.update(novo)
    os.makedirs(DIR_DADOS, exist_ok=True)
    json.dump(legado, open(LEGADO_JSON, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    return legado


# ---------------------------------------------------------------- respostas
INVALIDO = ("invalido", "")


def interpretar_resposta(v, lista_codigos):
    """Devolve ('cand', codigo) | ('flag', 'Nenhuma'/'Mais fotos') | None."""
    if v is None:
        return None
    if isinstance(v, float) and v == int(v):
        v = int(v)
    s = str(v).strip()
    if not s:
        return None
    n = hnorm(s)
    if re.fullmatch(r"[1-9]", n):
        k = int(n)
        if k <= len(lista_codigos) and lista_codigos[k - 1]:
            return ("cand", lista_codigos[k - 1])
        return INVALIDO   # número de candidata que não existe na linha: mantém a resposta anterior
    if n in ("sim", "s", "confere", "ok"):
        return ("cand", lista_codigos[0]) if lista_codigos else None
    if n in ("nenhuma", "nao", "não", "nenhum"):
        return ("flag", ST_NENHUMA)
    if n.startswith("mais foto"):
        return ("flag", ST_FOTOS)
    return ("cand", s)  # código digitado


def ler_fonte_xlsx(path, obrigatorio=False):
    wb = _abrir_xlsx(path, obrigatorio)
    if wb is None:
        return []
    saida = []
    for ws in wb.worksheets:
        linhas = ws.iter_rows(values_only=True)
        cab = next(linhas, None)
        if not cab:
            continue
        ix = _indices_cabecalho(cab)
        if "mat" not in ix or "resp" not in ix:
            continue
        for r in linhas:
            if ix["mat"] >= len(r) or vazio(r[ix["mat"]]):
                continue
            g = lambda k: r[ix[k]] if k in ix and ix[k] < len(r) else None
            lista = []
            for _, i in ix["cands"]:
                t = txt(r[i]) if i < len(r) else ""
                lista.append(t.split("\n")[0].strip() if t else "")
            saida.append((txt(r[ix["mat"]]), interpretar_resposta(g("resp"), lista),
                          {"codigo_final": txt(g("cod")), "nome_final": txt(g("nome")), "parte_final": txt(g("parte")),
                           "obs": txt(g("obs")), "medidas": txt(g("med"))}, ""))
    wb.close()
    return saida


def ler_fonte_csv(path):
    saida = []
    with open(path, encoding="utf-8-sig", newline="") as f:
        rd = csv.reader(f, delimiter=";")
        cab = next(rd, None)
        if not cab:
            return []
        ix = _indices_cabecalho(cab)
        if "mat" not in ix:
            return []
        for r in rd:
            if ix["mat"] >= len(r) or vazio(r[ix["mat"]]):
                continue
            g = lambda k: r[ix[k]] if k in ix and ix[k] < len(r) else ""
            resp = interpretar_resposta(g("resp"), [])
            st = hnorm(g("status"))
            if resp is None and st in ("nenhuma",):
                resp = ("flag", ST_NENHUMA)
            elif resp is None and st.startswith("mais foto"):
                resp = ("flag", ST_FOTOS)
            saida.append((txt(r[ix["mat"]]), resp,
                          {"codigo_final": txt(g("cod")), "nome_final": txt(g("nome")), "parte_final": txt(g("parte")),
                           "obs": txt(g("obs")), "medidas": txt(g("med"))}, txt(g("data"))))
    return saida


def status_de(rec):
    if rec.get("codigo_final") or rec.get("candidata_codigo"):
        return ST_OK
    if rec.get("flag") in (ST_NENHUMA, ST_FOTOS):
        return rec["flag"]
    return ST_PEND


def _rec_vazio():
    return {"candidata_codigo": "", "flag": "", "codigo_final": "", "nome_final": "", "parte_final": "", "obs": "",
            "medidas": "", "status": ST_PEND, "fonte": "", "data": ""}


def _carregar_json(path):
    if os.path.exists(path):
        try:
            return json.load(open(path, encoding="utf8"))
        except Exception:
            pass
    return {}


def fontes_secundarias():
    """Cópias de conflito do OneDrive (VERIFICACAO_GERAL-PC.xlsx), SUB antigos com colunas amarelas e CSV do Identificador."""
    out = []
    for p in glob.glob(os.path.join(AQUI, "VERIFICACAO_GERAL*.xlsx")):
        if os.path.abspath(p) != os.path.abspath(GERAL_XLSX) and not os.path.basename(p).startswith("~$"):
            print(f"AVISO: cópia de conflito encontrada: {os.path.basename(p)}. Respostas novas dela serão aproveitadas; "
                  "depois confira e apague a cópia.")
            out.append((os.path.getmtime(p), p, "xlsx"))
    for p in sorted(glob.glob(os.path.join(DIR_SUBS, "*.xlsx"))):
        if not os.path.basename(p).startswith("~$"):
            out.append((os.path.getmtime(p), p, "xlsx"))
    for p in glob.glob(os.path.join(AQUI, "RESPOSTAS_IDENTIFICADOR*.csv")):
        out.append((os.path.getmtime(p), p, "csv"))
    return sorted(out)


def coletar_respostas():
    """Junta as respostas.
    1) O VERIFICACAO_GERAL.xlsx manda: o que está nele vale, inclusive célula apagada.
    2) As outras fontes (CSV do Identificador, cópia de conflito, SUB antigo) só preenchem o que está VAZIO no GERAL
       e que é DIFERENTE do que a última geração escreveu (retrato): assim cópia velha não desfaz resposta nova.
    Se o GERAL ainda não existe, parte de dados/respostas.json."""
    anterior = _carregar_json(RESPOSTAS_JSON)
    retrato = _carregar_json(RETRATO_JSON) or anterior
    resp = {}
    if os.path.exists(GERAL_XLSX):
        mt_g = datetime.datetime.fromtimestamp(os.path.getmtime(GERAL_XLSX)).strftime("%Y-%m-%d %H:%M")
        for mat, rp, campos, _ in ler_fonte_xlsx(GERAL_XLSX, obrigatorio=True):
            rec, ant = _rec_vazio(), anterior.get(mat, {})
            if rp == INVALIDO:
                print(f"AVISO: {mat}: número de candidata que não existe na linha; mantida a resposta anterior.")
                rec["candidata_codigo"], rec["flag"] = ant.get("candidata_codigo", ""), ant.get("flag", "")
            elif rp and rp[0] == "cand":
                rec["candidata_codigo"] = rp[1]
            elif rp:
                rec["flag"] = rp[1]
            for k in CAMPOS_RESP:
                rec[k] = campos.get(k, "")
            igual = all(rec.get(k, "") == ant.get(k, "") for k in ("candidata_codigo", "flag") + CAMPOS_RESP)
            if igual and ant:
                rec["fonte"], rec["data"] = ant.get("fonte", ""), ant.get("data", "")
            else:
                rec["fonte"], rec["data"] = "VERIFICACAO_GERAL.xlsx", mt_g
            resp[mat] = rec
        for mat, r in anterior.items():      # material que não está no GERAL: guarda como estava
            resp.setdefault(mat, r)
    else:
        resp = {m: dict(_rec_vazio(), **r) for m, r in anterior.items()}
    for mt, p, tipo in fontes_secundarias():
        try:
            linhas = ler_fonte_xlsx(p) if tipo == "xlsx" else ler_fonte_csv(p)
        except Exception as e:
            print(f"AVISO: não consegui ler {os.path.basename(p)}: {e}")
            continue
        nome = os.path.basename(p)
        for mat, rp, campos, data in linhas:
            rec, ret = resp.setdefault(mat, _rec_vazio()), retrato.get(mat, {})
            mudou = False
            tinha_resp = bool(rec["candidata_codigo"] or rec["flag"])   # o GERAL já decidiu: código/nome/parte não mudam
            if rp and rp != INVALIDO and not tinha_resp:
                if rp[0] == "cand" and cod_chave(rp[1]) != cod_chave(ret.get("candidata_codigo", "")):
                    rec["candidata_codigo"], mudou = rp[1], True
                elif rp[0] == "flag" and rp[1] != ret.get("flag", ""):
                    rec["flag"], mudou = rp[1], True
            for k in CAMPOS_RESP:
                v = campos.get(k, "")
                if tinha_resp and k in ("codigo_final", "nome_final", "parte_final"):
                    continue
                if v and not rec.get(k) and v != ret.get(k, ""):
                    rec[k], mudou = v, True
            if mudou:
                rec["fonte"] = nome
                rec["data"] = data or datetime.datetime.fromtimestamp(mt).strftime("%Y-%m-%d %H:%M")
                print(f"  {mat}: completado a partir de {nome}")
    for rec in resp.values():
        rec["status"] = status_de(rec)
    return {m: r for m, r in resp.items() if any(r.get(k) for k in ("candidata_codigo", "flag") + CAMPOS_RESP)}


def salvar_respostas(resp):
    os.makedirs(DIR_DADOS, exist_ok=True)
    json.dump(resp, open(RESPOSTAS_JSON, "w", encoding="utf8"), ensure_ascii=False, indent=1, sort_keys=True)


# ---------------------------------------------------------------- itens
def _int_pct(v):
    if v is None or v == "":
        return None
    try:
        return int(round(float(str(v).replace("%", "").strip())))
    except ValueError:
        return None


def enriquecer_candidata(c, grt):
    """c: dict com codigo, descricao, manual(id ou rótulo), pagina, pct, ... -> dict completo."""
    manual = c.get("manual") or ""
    if manual not in catalogo()["manuais"]:
        manual = catalogo()["rot2id"].get(manual, manual if manual in catalogo()["manuais"] else "")
    pagina = c.get("pagina")
    try:
        pagina = int(pagina) if pagina not in (None, "") else None
    except (TypeError, ValueError):
        pagina = None
    occ = achar_ocorrencia(c.get("codigo"), manual or None, pagina)
    out = {
        "codigo": txt(c.get("codigo")), "descricao": txt(c.get("descricao")), "pct": _int_pct(c.get("pct")),
        "motivo": txt(c.get("motivo")), "diferencia": txt(c.get("diferencia")),
        "veredito": txt(c.get("veredito")).lower(), "nota": txt(c.get("nota_verificacao") or c.get("nota")),
        "pid": None, "nome_pt": "", "conjunto": txt(c.get("parte")), "maquina": "", "manual": manual, "manual_rotulo": "",
        "pagina": pagina, "pagina_lista": None, "recorte": "", "pagina_marcada": "", "baloes": [], "pontas": [],
        "medidas_txt": "", "tipo": "",
    }
    if occ:
        man = catalogo()["manuais"][occ["manual"]]
        out.update({
            "pid": occ["id"], "nome_pt": occ["nome_pt"], "conjunto": occ["conjunto"], "maquina": occ["maquina"],
            "manual": occ["manual"], "manual_rotulo": man["rotulo"], "pagina": occ["pagina_desenho"],
            "pagina_lista": occ["pagina_lista"], "recorte": recorte_de(occ), "pagina_marcada": occ.get("pagina_marcada") or "",
            "baloes": occ.get("baloes") or [], "pontas": occ.get("pontas") or [], "medidas_txt": occ.get("medidas_txt") or "",
            "tipo": occ.get("tipo") or "",
        })
        if not out["descricao"]:
            out["descricao"] = occ["descricao"]
        # só o código "oficial" do catálogo quando o código da IA tiver sido escrito diferente
        if not out["codigo"]:
            out["codigo"] = occ["codigo"]
    else:
        rec = txt(c.get("recorte"))
        if rec and os.path.exists(os.path.join(DIR_MANUAIS, rec)):
            out["recorte"] = rec
        if manual:
            out["manual_rotulo"] = catalogo()["manuais"][manual]["rotulo"]
    g = grt.get(cod_chave(out["codigo"]))
    out["grt"] = f"{g[0]} {g[1]}".strip() if g else ""
    return out


def _ordenar_cands(cands):
    cands = sorted(cands, key=lambda c: (c["veredito"] == "refutada", -(c["pct"] if c["pct"] is not None else -1)))
    vistos, res = set(), []
    for c in cands:
        k = cod_chave(c["codigo"])
        if k in vistos:
            continue
        vistos.add(k)
        res.append(c)
    return res[:5]


def faixa_de(maior, tem):
    if not tem or maior is None:
        return "SEM_CANDIDATA"
    return "ALTA" if maior >= 70 else ("MEDIA" if maior >= 40 else "BAIXA")


def carregar_ia():
    for p, nome in ((IA_JSON, "candidatos_ia.json"), (IA_EXEMPLO_JSON, "candidatos_ia_exemplo.json (EXEMPLO)")):
        if os.path.exists(p):
            try:
                d = json.load(open(p, encoding="utf8"))
                return d.get("itens", {}), nome
            except Exception as e:
                print("Aviso: erro lendo", p, e)
    return {}, "(nenhum)"


def montar_itens(legado=None, verbose=False):
    """Lista de itens (um por material da BASE) com fotos, candidatas e dados da IA."""
    legado = legado if legado is not None else (json.load(open(LEGADO_JSON, encoding="utf8")) if os.path.exists(LEGADO_JSON) else {})
    grt = carregar_grt()
    ia, ia_nome = carregar_ia()
    if verbose:
        print("Fonte da IA:", ia_nome, "-", len(ia), "itens")
    itens = []
    for d in ler_base():
        mat = txt(d["Material (como anotado)"])
        g = grupo_de(d)
        pasta = pasta_de_fotos(mat, d.get("Pasta de fotos"))
        fotos = listar_fotos(pasta)
        it = {"material": mat, "grupo": g, "local": txt(d.get("Locais (Pallet/Caixa/Qtd)")),
              "qtd": d.get("Qtd total"), "un": txt(d.get("Un")), "pasta": pasta, "fotos": fotos,
              "status_base": txt(d.get("Status")), "codigo_manual": txt(d.get("Código no manual")),
              "desc_manual": txt(d.get("Descrição EN (manual)")), "maq_manual": txt(d.get("Máquina")),
              "ia": None, "fonte_cands": "", "oque": "", "nome_sug": "", "medir": ""}
        lg = legado.get(mat, {})
        brutas = []
        if g == G_CONF:
            occs = ocorrencias_codigo(it["codigo_manual"])
            if occs:
                brutas = [{"codigo": it["codigo_manual"], "manual": occs[0]["manual"], "pagina": occs[0]["pagina_desenho"],
                           "descricao": it["desc_manual"]}]
            it["fonte_cands"] = "BASE"
            it["oque"] = it["desc_manual"]
            it["medir"] = "Confira o desenho com a peça: formato, furos, tamanho. Se não for esta, marque Nenhuma."
        elif mat in ia:
            x = ia[mat]
            it["ia"] = x
            brutas = list(x.get("candidatas") or [])
            it["fonte_cands"] = "IA"
            it["oque"] = txt(x.get("descricao_peca"))
            it["nome_sug"] = txt(x.get("nome_pt"))
            m = x.get("medir")
            it["medir"] = "; ".join(m) if isinstance(m, list) else txt(m)
        if not brutas and lg.get("cands"):
            for t in lg["cands"]:
                c = parse_cand_txt(t)
                if c:
                    brutas.append(c)
            it["fonte_cands"] = "legado"
            it["oque"] = it["oque"] or lg.get("oque", "")
            it["nome_sug"] = it["nome_sug"] or lg.get("nome", "")
            it["medir"] = it["medir"] or lg.get("medir", "")
        elif lg:
            it["oque"] = it["oque"] or lg.get("oque", "")
            it["nome_sug"] = it["nome_sug"] or lg.get("nome", "")
            it["medir"] = it["medir"] or lg.get("medir", "")
        cands = [enriquecer_candidata(c, grt) for c in brutas if txt(c.get("codigo"))]
        it["cands"] = cands if g == G_CONF else _ordenar_cands(cands)
        pcts = [c["pct"] for c in it["cands"] if c["pct"] is not None and c["veredito"] != "refutada"] or \
               [c["pct"] for c in it["cands"] if c["pct"] is not None]
        it["maior"] = max(pcts) if pcts else None
        it["faixa"] = "CONFERIR" if g == G_CONF else faixa_de(it["maior"], bool(it["cands"]))
        it["grt_txt"] = "\n".join(f"{c['codigo']} = {c['grt']}" for c in it["cands"] if c.get("grt"))
        itens.append(it)

    def ordem(it):
        gi = [G_NI, G_LIVRE, G_COD, G_CONF].index(it["grupo"])
        return (gi, chave_natural(it["material"]))
    itens.sort(key=ordem)
    return itens


# ---------------------------------------------------------------- imagens
_THUMBS = {}


def miniatura(path, caixa, qualidade=75):
    chave = (path, caixa)
    if chave in _THUMBS:
        return _THUMBS[chave]
    from PIL import Image as PI
    try:
        im = PI.open(path)
        im = im.convert("RGB")
        im.thumbnail(caixa)
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=qualidade, optimize=True)
        _THUMBS[chave] = (buf.getvalue(), im.size)
    except Exception as e:
        print("Aviso: imagem ilegível", path, e)
        _THUMBS[chave] = None
    return _THUMBS[chave]


def inserir_imagem(ws, ref, path, caixa):
    from openpyxl.drawing.image import Image as XI
    r = miniatura(path, caixa)
    if not r:
        return False
    buf, (w, h) = r
    img = XI(io.BytesIO(buf))
    img.width, img.height = w, h
    ws.add_image(img, ref)
    return True


# ---------------------------------------------------------------- planilhas
def _col(n):
    from openpyxl.utils import get_column_letter
    return get_column_letter(n)


def _url_rel(prefixo, rel):
    return prefixo + urllib.parse.quote(rel.replace("\\", "/"), safe="/.-_~")


def selo(v):
    return {"sustenta": "✓sustenta", "duvidosa": "?duvidosa", "refutada": "✗refutada"}.get(v, "")


def texto_candidata(c):
    linhas = [c["codigo"]]
    if c["nome_pt"]:
        linhas.append(c["nome_pt"])
    if c["descricao"]:
        linhas.append(c["descricao"])
    if c["conjunto"] or c["maquina"]:
        linhas.append(" · ".join(x for x in (c["conjunto"], c["maquina"]) if x))
    l5 = []
    if c["manual_rotulo"] or c["manual"]:
        l5.append(f"{c['manual_rotulo'] or c['manual']}" + (f" pág. {c['pagina']}" if c["pagina"] else ""))
    if c["pct"] is not None:
        l5.append(f"{c['pct']}%")
    if selo(c["veredito"]):
        l5.append(selo(c["veredito"]))
    if l5:
        linhas.append(" · ".join(l5))
    if c["medidas_txt"]:
        linhas.append("Esperado: " + c["medidas_txt"])
    return "\n".join(linhas)


def preencher_resposta(it, rec):
    """Valores das colunas amarelas para o item (lista de candidatas da planilha nova)."""
    out = {"resp": "", "cod": "", "nome": "", "parte": "", "obs": ""}
    if not rec:
        return out
    cod_f = rec.get("codigo_final", "")
    obs = rec.get("obs", "")
    if rec.get("flag"):
        out["resp"] = rec["flag"]
    elif rec.get("candidata_codigo"):
        k = cod_chave(rec["candidata_codigo"])
        pos = [i for i, c in enumerate(it["cands"]) if cod_chave(c["codigo"]) == k]
        if pos:
            out["resp"] = ("Sim" if it["grupo"] == G_CONF else pos[0] + 1)
        else:
            if not cod_f:
                cod_f = rec["candidata_codigo"]
            antiga = f"Resposta anterior: candidata = {rec['candidata_codigo']}"
            if antiga not in obs:
                obs = (obs + " | " if obs else "") + antiga
    out.update({"cod": cod_f, "nome": rec.get("nome_final", ""), "parte": rec.get("parte_final", ""), "obs": obs})
    return out


def _estilo_cab(ws, ncols, amarelas_ini):
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    for c in range(1, ncols + 1):
        cel = ws.cell(row=1, column=c)
        cor = MARROM if amarelas_ini and c >= amarelas_ini[0] and c <= amarelas_ini[1] else AZUL
        cel.fill = PatternFill("solid", fgColor=cor)
        cel.font = Font(bold=True, color="FFFFFF", size=10)
        cel.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.row_dimensions[1].height = 48


def construir_aba_verificar(wb, titulo, itens, resp, prefixo, consulta=False):
    """prefixo: '../' (arquivo em 05_VERIFICACAO) ou '../../' (em POR_CONFIANCA).
    consulta=True (arquivos POR_CONFIANCA): sem colunas amarelas; só mostra a resposta do GERAL na hora da geração."""
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.worksheet.datavalidation import DataValidation
    ws = wb.create_sheet(titulo)
    cab = ["Grupo", "Material", "Foto", "Local (pallet / caixa / qtd)", "O que é (IA)", "Nome sugerido (PT)"]
    for k in range(1, 6):
        cab += [f"Desenho {k}", f"Candidata {k}"]
    cab += ["Maior %", "Já no GRT?"]
    if consulta:
        cab += ["Situação no GERAL (só consulta)", "Faixa"]
    else:
        cab += ["APRENDIZ: qual candidata confere? (1-5 / Nenhuma / Mais fotos)", "Código FINAL confirmado",
                "Nome da peça FINAL", "Parte da máquina FINAL", "Observação do aprendiz", "Faixa"]
    ws.append(cab)
    n_res = 6 + 10 + 2  # colunas até "Já no GRT?"
    c_resp = n_res + 1
    _estilo_cab(ws, len(cab), None if consulta else (c_resp, c_resp + 4))
    larg = [9, 16, 43, 17, 30, 22] + [30, 36] * 5 + [8, 26, 22, 20, 22, 30, 30, 11]
    for i, w in enumerate(larg, 1):
        ws.column_dimensions[_col(i)].width = w
    fino = Side(style="thin", color="BFBFBF")
    borda = Border(left=fino, right=fino, top=fino, bottom=fino)
    topo = Alignment(vertical="top", wrap_text=True)
    amarelo = PatternFill("solid", fgColor=AMARELO_CLARO)
    for r, it in enumerate(itens, 2):
        ws.row_dimensions[r].height = ALTURA_LINHA
        loc = it["local"] + (f"\nQtd: {it['qtd']} {it['un']}" if it["qtd"] not in (None, "") else "")
        if len(it["fotos"]) > 1:
            loc += f"\n({len(it['fotos'])} fotos)"
        if not it["fotos"]:
            loc += "\nSEM FOTO"
        vals = [it["grupo"], it["material"], "", loc, it["oque"], it["nome_sug"]]
        for i, v in enumerate(vals, 1):
            ws.cell(row=r, column=i, value=v)
        if it["fotos"]:
            rel = f"04_FOTOS/{it['pasta']}/{it['fotos'][0]}"
            ws.cell(row=r, column=2).hyperlink = _url_rel(prefixo, rel)
            ws.cell(row=r, column=2).font = Font(color="0563C1", underline="single", bold=True)
            inserir_imagem(ws, f"C{r}", os.path.join(DIR_FOTOS, it["pasta"], it["fotos"][0]), (W_FOTO, H_FOTO))
        for k in range(5):
            cdes, ctxt = 7 + 2 * k, 8 + 2 * k
            if k < len(it["cands"]):
                c = it["cands"][k]
                cel = ws.cell(row=r, column=ctxt, value=texto_candidata(c))
                if c["recorte"]:
                    p = os.path.join(DIR_MANUAIS, c["recorte"])
                    inserir_imagem(ws, f"{_col(cdes)}{r}", p, (W_DES, H_DES))
                    cel.hyperlink = _url_rel(prefixo + "02_MANUAIS/", c["recorte"])
                    cel.font = Font(size=8, color="0563C1")
                else:
                    cel.font = Font(size=8)
                if c["veredito"] == "refutada":
                    cel.font = Font(size=8, color="7F7F7F", strike=False, italic=True)
        ws.cell(row=r, column=n_res - 1, value=it["maior"])
        ws.cell(row=r, column=n_res, value=it["grt_txt"])
        a = preencher_resposta(it, resp.get(it["material"]))
        if consulta:
            sit = " · ".join(str(x) for x in (a["resp"], a["cod"]) if x not in ("", None)) or "pendente"
            ws.cell(row=r, column=c_resp, value=sit)
            ws.cell(row=r, column=c_resp + 1, value=it["faixa"])
        else:
            for j, key in enumerate(("resp", "cod", "nome", "parte", "obs")):
                cel = ws.cell(row=r, column=c_resp + j, value=a[key] if a[key] != "" else None)
                cel.fill = amarelo
            ws.cell(row=r, column=c_resp + 5, value=it["faixa"])
        for c in range(1, len(cab) + 1):
            cel = ws.cell(row=r, column=c)
            cel.alignment = topo
            cel.border = borda
            if cel.font.sz == 11 and not cel.hyperlink:
                cel.font = Font(size=9)
        m = it["maior"]
        if m is not None:
            ws.cell(row=r, column=n_res - 1).fill = PatternFill(
                "solid", fgColor="C6EFCE" if m >= 70 else ("FFEB9C" if m >= 40 else "F8CBAD"))
            ws.cell(row=r, column=n_res - 1).alignment = Alignment(horizontal="center", vertical="top")
    dv = DataValidation(type="list", formula1='"1,2,3,4,5,Nenhuma,Mais fotos"', allow_blank=True)
    dv.error = "Escolha 1 a 5, Nenhuma ou Mais fotos"
    dv.errorTitle = "Valor inválido"
    if not consulta:
        ws.add_data_validation(dv)
        if len(itens):
            dv.add(f"{_col(c_resp)}2:{_col(c_resp)}{len(itens) + 1}")
    ws.freeze_panes = "D2"
    ws.auto_filter.ref = f"A1:{_col(len(cab))}{len(itens) + 1}"
    return ws


def construir_aba_conferir(wb, titulo, itens, resp, prefixo):
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.worksheet.datavalidation import DataValidation
    ws = wb.create_sheet(titulo)
    cab = ["Grupo", "Material", "Foto", "Local (pallet / caixa / qtd)", "Código anotado → descrição (manual)",
           "Desenho 1", "Candidata 1", "O que conferir",
           "APRENDIZ: o código confere? (Sim / Nenhuma / Mais fotos)", "Código FINAL confirmado",
           "Nome da peça FINAL", "Parte da máquina FINAL", "Observação do aprendiz", "Faixa"]
    ws.append(cab)
    _estilo_cab(ws, len(cab), (9, 13))
    for i, w in enumerate([9, 20, 43, 17, 34, 30, 40, 34, 22, 20, 22, 30, 30, 11], 1):
        ws.column_dimensions[_col(i)].width = w
    fino = Side(style="thin", color="BFBFBF")
    borda = Border(left=fino, right=fino, top=fino, bottom=fino)
    topo = Alignment(vertical="top", wrap_text=True)
    amarelo = PatternFill("solid", fgColor=AMARELO_CLARO)
    for r, it in enumerate(itens, 2):
        ws.row_dimensions[r].height = ALTURA_LINHA
        loc = it["local"] + (f"\nQtd: {it['qtd']} {it['un']}" if it["qtd"] not in (None, "") else "")
        if not it["fotos"]:
            loc += "\nSEM FOTO"
        vals = [it["grupo"], it["material"], "", loc, f"{it['codigo_manual']}\n{it['desc_manual']}\n{it['maq_manual']}"]
        for i, v in enumerate(vals, 1):
            ws.cell(row=r, column=i, value=v)
        if it["fotos"]:
            ws.cell(row=r, column=2).hyperlink = _url_rel(prefixo, f"04_FOTOS/{it['pasta']}/{it['fotos'][0]}")
            ws.cell(row=r, column=2).font = Font(color="0563C1", underline="single", bold=True)
            inserir_imagem(ws, f"C{r}", os.path.join(DIR_FOTOS, it["pasta"], it["fotos"][0]), (W_FOTO, H_FOTO))
        if it["cands"]:
            c = it["cands"][0]
            cel = ws.cell(row=r, column=7, value=texto_candidata(c))
            if c["recorte"]:
                inserir_imagem(ws, f"F{r}", os.path.join(DIR_MANUAIS, c["recorte"]), (W_DES, H_DES))
                cel.hyperlink = _url_rel(prefixo + "02_MANUAIS/", c["recorte"])
                cel.font = Font(size=8, color="0563C1")
        else:
            ws.cell(row=r, column=7, value="Código não localizado no catálogo")
        ws.cell(row=r, column=8, value=it["medir"])
        a = preencher_resposta(it, resp.get(it["material"]))
        for j, key in enumerate(("resp", "cod", "nome", "parte", "obs")):
            cel = ws.cell(row=r, column=9 + j, value=a[key] if a[key] != "" else None)
            cel.fill = amarelo
        ws.cell(row=r, column=14, value=it["faixa"])
        for c in range(1, len(cab) + 1):
            cel = ws.cell(row=r, column=c)
            cel.alignment = topo
            cel.border = borda
            if c not in (2, 7):
                cel.font = Font(size=9)
    dv = DataValidation(type="list", formula1='"Sim,Nenhuma,Mais fotos"', allow_blank=True)
    ws.add_data_validation(dv)
    if itens:
        dv.add(f"I2:I{len(itens) + 1}")
    ws.freeze_panes = "D2"
    ws.auto_filter.ref = f"A1:{_col(len(cab))}{len(itens) + 1}"
    return ws


TEXTO_LEIAME = [
    "VERIFICAÇÃO DE PEÇAS - como usar",
    "",
    "ESTE ARQUIVO (VERIFICACAO_GERAL.xlsx) É O REGISTRO OFICIAL. Use com o salvamento automático ligado: os 3 PCs veem na hora.",
    "",
    "1. Na aba 'Verificar': cada linha é um material. Veja a foto e as candidatas (desenho do manual + dados).",
    "2. Compare a peça com o desenho do manual de cada candidata (as peças não são medidas).",
    "3. Preencha só as colunas AMARELAS: o número da candidata que confere (1 a 5), Nenhuma ou Mais fotos;",
    "   e, se quiser, código final, nome, parte da máquina e observação.",
    "   Pelo IDENTIFICADOR.html: botão 'Copiar para o Excel' e cole (Ctrl+V) na 1ª coluna amarela da linha do material.",
    "4. Aba 'Conferir códigos': materiais cujo código já foi achado nos manuais. Só confirme visualmente (Sim / Nenhuma).",
    "5. Os percentuais são estimativas por foto. Só vale como definitivo o que o aprendiz conferir.",
    "6. Clique no nome do material para abrir a foto grande e no texto da candidata para abrir o desenho do manual.",
    "",
    "Status: dois cliques em ATUALIZAR_STATUS.bat (não altera este arquivo).",
    "GERAR_VERIFICACAO.bat REESCREVE este arquivo: só rode com ele FECHADO nos 3 PCs. As respostas daqui são mantidas.",
]
TEXTO_LEIAME_SUB = [
    "ARQUIVO SÓ PARA CONSULTA E IMPRESSÃO",
    "",
    "Este arquivo mostra uma parte dos materiais (separados pela maior % da IA).",
    "NÃO preencha aqui: registre no VERIFICACAO_GERAL.xlsx (pasta 05_VERIFICACAO), que é o registro oficial dos 3 PCs.",
    "A coluna 'Situação no GERAL' mostra a resposta que existia quando este arquivo foi gerado.",
]


def aba_leiame(wb, texto=None):
    from openpyxl.styles import Font
    ws = wb.create_sheet("Leia-me")
    for l in (texto or TEXTO_LEIAME):
        ws.append([l])
    ws.append([])
    ws.append([f"Gerado em {GERADO_EM}"])
    ws["A1"].font = Font(bold=True, size=14, color=AZUL)
    ws.column_dimensions["A"].width = 130
    return ws


GERADO_EM = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
PENDENTES = []   # (arquivo temporário, arquivo final): trocados todos juntos no fim


def salvar_wb(wb, caminho):
    """Grava num arquivo temporário; a troca pelo definitivo acontece só no fim (trocar_todos)."""
    tmp = caminho + ".novo"
    wb.save(tmp)
    PENDENTES.append((tmp, caminho))


def arquivos_livres(caminhos):
    """Confere, ANTES de gravar qualquer coisa, se nenhum arquivo de saída está aberto/bloqueado."""
    presos = []
    for c in caminhos:
        dono = os.path.join(os.path.dirname(c), "~$" + os.path.basename(c))
        if os.path.exists(dono):
            presos.append(os.path.basename(c) + " (aberto no Excel neste PC)")
            continue
        if os.path.exists(c):
            try:
                open(c, "r+b").close()
            except OSError:
                presos.append(os.path.basename(c))
    if presos:
        raise SystemExit("ERRO: feche estes arquivos e rode de novo (nada foi alterado):\n  " + "\n  ".join(presos))


def trocar_todos():
    for tmp, final in PENDENTES:
        os.replace(tmp, final)
    PENDENTES.clear()


def novo_wb():
    import openpyxl
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    return wb


def backup_xlsx():
    destino = os.path.join(AQUI, "_backup", datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S"))
    k = 1
    while os.path.exists(destino):          # nunca sobrescreve um backup
        k += 1
        destino = os.path.join(AQUI, "_backup", datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S") + f"_{k}")
    arqs = [GERAL_XLSX, STATUS_XLSX] + sorted(glob.glob(os.path.join(DIR_SUBS, "*.xlsx")))
    feitos = 0
    for a in arqs:
        if os.path.exists(a) and not os.path.basename(a).startswith("~$"):
            rel = os.path.relpath(a, AQUI)
            d = os.path.join(destino, os.path.dirname(rel))
            os.makedirs(d, exist_ok=True)
            shutil.copy2(a, os.path.join(d, os.path.basename(a)))
            feitos += 1
    if feitos:
        print(f"Backup: {feitos} arquivo(s) em {os.path.relpath(destino, AQUI)}")


# ---------------------------------------------------------------- status
def classificar_status(it, rec):
    st = status_de(rec) if rec else ST_PEND
    if st == ST_PEND and not it["fotos"]:
        return "Sem foto"
    return st


def gerar_status(itens, resp):
    from openpyxl.styles import Font, PatternFill, Alignment
    wb = novo_wb()
    cols = ["Total", ST_OK, ST_NENHUMA, ST_FOTOS, ST_PEND, "Sem foto"]
    ws = wb.create_sheet("Resumo")
    cls = {id(it): classificar_status(it, resp.get(it["material"])) for it in itens}

    def tabela(titulo, chave, valores):
        ws.append([titulo] + cols)
        lin_cab = ws.max_row
        tot = [0] * 6
        for v in valores:
            sub = [it for it in itens if chave(it) == v]
            if not sub:
                continue
            linha = [len(sub)] + [sum(1 for it in sub if cls[id(it)] == c) for c in cols[1:]]
            ws.append([v] + linha)
            tot = [a + b for a, b in zip(tot, linha)]
        ws.append(["TOTAL"] + tot)
        ws.cell(row=ws.max_row, column=1).font = Font(bold=True)
        for c in range(1, 8):
            cel = ws.cell(row=lin_cab, column=c)
            cel.font = Font(bold=True, color="FFFFFF")
            cel.fill = PatternFill("solid", fgColor=AZUL)
            cel.alignment = Alignment(horizontal="center", wrap_text=True)
        ws.append([])
    tabela("Por grupo", lambda it: it["grupo"], [G_NI, G_LIVRE, G_COD, G_CONF])
    tabela("Por faixa de confiança", lambda it: it["faixa"], ["ALTA", "MEDIA", "BAIXA", "SEM_CANDIDATA", "CONFERIR"])
    ws.append(["Atualizado em", datetime.datetime.now().strftime("%d/%m/%Y %H:%M")])
    ws.column_dimensions["A"].width = 26
    for c in "BCDEFG":
        ws.column_dimensions[c].width = 13
    det = wb.create_sheet("Detalhe")
    det.append(["Grupo", "Faixa", "Material", "Local", "Status", "Candidata escolhida", "Código FINAL", "Nome FINAL",
                "Parte da máquina FINAL", "Observação", "Fonte da resposta", "Data"])
    cor = {ST_OK: "C6EFCE", ST_PEND: "FFC7CE", "Sem foto": "D9D9D9", ST_NENHUMA: "FFEB9C", ST_FOTOS: "DDEBF7"}
    for it in itens:
        rec = resp.get(it["material"], {})
        st = cls[id(it)]
        det.append([it["grupo"], it["faixa"], it["material"], it["local"], st,
                    rec.get("candidata_codigo") or rec.get("flag", ""), rec.get("codigo_final", ""),
                    rec.get("nome_final", ""), rec.get("parte_final", ""), rec.get("obs", ""),
                    rec.get("fonte", ""), rec.get("data", "")])
        det.cell(row=det.max_row, column=5).fill = PatternFill("solid", fgColor=cor.get(st, "FFFFFF"))
    for c in det[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor=AZUL)
        c.alignment = Alignment(horizontal="center", wrap_text=True)
    for i, w in enumerate([16, 14, 26, 18, 12, 18, 18, 26, 24, 40, 20, 34, 16], 1):
        det.column_dimensions[_col(i)].width = w
    det.freeze_panes = "D2"
    det.auto_filter.ref = det.dimensions
    salvar_wb(wb, STATUS_XLSX)
    trocar_todos()
    ok = sum(1 for it in itens if cls[id(it)] == ST_OK)
    print(f"Status: {ok} conferidos de {len(itens)} -> {os.path.basename(STATUS_XLSX)}")
    return ok


# ---------------------------------------------------------------- HTML
def dados_html(itens, resp):
    cat = catalogo()
    grt = carregar_grt()
    pecas = []
    for p in cat["pecas"]:
        m = p.get("medidas") or {}
        mm = lambda k: round(m[k] * 25.4, 2) if isinstance(m.get(k), (int, float)) else None
        pecas.append({
            "i": p["id"], "c": p["codigo"], "d": p["descricao"], "t": p["tipo"], "n": p["nome_pt"], "m": p["maquina"],
            "j": p["conjunto"], "a": p["manual"], "p": p["pagina_desenho"], "l": p["pagina_lista"],
            "r": recorte_de(p), "g": p.get("pagina_marcada") or "", "b": p.get("baloes") or [], "o": p.get("pontas") or [],
            "x": p.get("medidas_txt") or "",
            "v": {"id": mm("id_in"), "od": mm("od_in"), "c": mm("comp_in"), "e": mm("espessura_in")},
            "s": m.get("rosca") or "", "z": m.get("dentes") if isinstance(m.get("dentes"), int) else None,
            "k": ORDEM_MANUAIS.index(p["manual"]) if p["manual"] in ORDEM_MANUAIS else 9,
        })
    its = []
    for it in itens:
        ia = it["ia"] or {}
        its.append({
            "m": it["material"], "g": it["grupo"], "loc": it["local"], "qtd": it["qtd"], "un": it["un"],
            "fotos": [f"../04_FOTOS/{it['pasta']}/{f}" for f in it["fotos"]],
            "oque": it["oque"], "nome": it["nome_sug"], "tipo": txt(ia.get("tipo")), "inv": ia.get("invariantes") or [],
            "marc": ia.get("marcacoes") if not isinstance(ia.get("marcacoes"), list) else "; ".join(map(str, ia["marcacoes"])),
            "fora": bool(ia.get("fora_do_catalogo")), "sug": txt(ia.get("sugestao_comercial")),
            "conf": txt(ia.get("confianca")), "medir": it["medir"], "verif": txt(ia.get("verificacao")),
            "fonte": it["fonte_cands"], "maior": it["maior"], "faixa": it["faixa"],
            "c": [{
                "cod": c["codigo"], "desc": c["descricao"], "nome": c["nome_pt"], "conj": c["conjunto"], "maq": c["maquina"],
                "man": c["manual_rotulo"], "pag": c["pagina"], "lista": c["pagina_lista"], "rec": c["recorte"],
                "pm": c["pagina_marcada"], "bal": c["baloes"], "pon": c["pontas"], "med": c["medidas_txt"],
                "pct": c["pct"], "mot": c["motivo"], "dif": c["diferencia"], "ver": c["veredito"], "nota": c["nota"],
                "grt": c["grt"], "pid": c["pid"], "tipo": c["tipo"],
            } for c in it["cands"]],
        })
    return {
        "gerado_em": agora_iso(),
        "manuais": {k: v["rotulo"] for k, v in cat["manuais"].items()},
        "itens": its, "catalogo": pecas,
        "grt": {k: f"{v[0]} {v[1]}".strip() for k, v in grt.items()},
        "respostas": resp,
    }


def gerar_html(itens, resp):
    if not os.path.exists(HTML_MODELO):
        print("AVISO: modelo_identificador.html não encontrado; IDENTIFICADOR.html não foi gerado.")
        return
    modelo = open(HTML_MODELO, encoding="utf8").read()
    js = json.dumps(dados_html(itens, resp), ensure_ascii=False, separators=(",", ":"))
    js = js.replace("</", "<\\/").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    out = modelo.replace("/*__DADOS__*/", js)
    with open(HTML_SAIDA + ".novo", "w", encoding="utf8") as f:
        f.write(out)
    PENDENTES.append((HTML_SAIDA + ".novo", HTML_SAIDA))
    print(f"IDENTIFICADOR.html: {len(out.encode('utf8')) / 1e6:.1f} MB")


# ---------------------------------------------------------------- principal
SUBS = [("SUB1_ALTA_70-100.xlsx", ("ALTA",)), ("SUB2_MEDIA_40-69.xlsx", ("MEDIA",)),
        ("SUB3_BAIXA_0-39.xlsx", ("BAIXA", "SEM_CANDIDATA"))]


def main():
    os.makedirs(DIR_DADOS, exist_ok=True)
    os.makedirs(DIR_SUBS, exist_ok=True)
    if os.path.exists(GERAL_XLSX) and "--confirmo" not in sys.argv:
        raise SystemExit("Este script REESCREVE o VERIFICACAO_GERAL.xlsx, que é usado nos 3 PCs.\n"
                         "Feche o arquivo em todos os PCs, espere o OneDrive sincronizar e rode pelo GERAR_VERIFICACAO.bat\n"
                         "(ou: python -X utf8 gerar_verificacao.py --confirmo).")
    saidas = [GERAL_XLSX, STATUS_XLSX, HTML_SAIDA] + [os.path.join(DIR_SUBS, n) for n, _ in SUBS]
    arquivos_livres(saidas)
    legado = atualizar_legado()          # candidatas antigas (antes de sobrescrever)
    resp = coletar_respostas()           # respostas de todos os lugares
    salvar_respostas(resp)
    print(f"Respostas juntadas: {len(resp)} material(is)")
    itens = montar_itens(legado, verbose=True)
    backup_xlsx()
    verificar = [i for i in itens if i["grupo"] != G_CONF]
    conferir = [i for i in itens if i["grupo"] == G_CONF]

    wb = novo_wb()
    construir_aba_verificar(wb, "Verificar", verificar, resp, "../")
    construir_aba_conferir(wb, "Conferir códigos", conferir, resp, "../")
    aba_leiame(wb)
    try:
        salvar_wb(wb, GERAL_XLSX)
        print(f"VERIFICACAO_GERAL.xlsx: {len(verificar)} linhas em Verificar, {len(conferir)} em Conferir")
        for nome, faixas in SUBS:
            sel = [i for i in verificar if i["faixa"] in faixas]
            sel.sort(key=lambda i: (i["faixa"] != faixas[0], -(i["maior"] or 0)))
            w = novo_wb()
            construir_aba_verificar(w, "Verificar", sel, resp, "../../", consulta=True)
            aba_leiame(w, TEXTO_LEIAME_SUB)
            salvar_wb(w, os.path.join(DIR_SUBS, nome))
            print(f"{nome}: {len(sel)} linhas (só consulta)")
        gerar_html(itens, resp)
        trocar_todos()                     # só agora os arquivos novos substituem os antigos, todos juntos
    except BaseException:
        for tmp, _ in PENDENTES:
            if os.path.exists(tmp):
                os.remove(tmp)
        raise
    json.dump(resp, open(RETRATO_JSON, "w", encoding="utf8"), ensure_ascii=False, indent=1, sort_keys=True)
    print(f"VERIFICACAO_GERAL.xlsx: {os.path.getsize(GERAL_XLSX) / 1e6:.1f} MB")
    gerar_status(itens, resp)
    sem = [i["material"] for i in itens if not i["fotos"]]
    if sem:
        print("Sem foto:", ", ".join(sem))


if __name__ == "__main__":
    main()
