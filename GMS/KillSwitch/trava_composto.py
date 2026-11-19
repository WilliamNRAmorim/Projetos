#!/usr/bin/env python3
"""GMS · kill switch Composto v0.3.0 (MEL-274) · aplica a trava varCompostoPermitida nas camadas C2 a C5.

Uso (python 3.12, sem dependencia externa):
    python -I trava_composto.py <pasta Src do app desempacotado> <pasta de saida> [relatorio.csv]

- Trabalha numa COPIA: a pasta de saida recebe o conteudo inteiro de <pasta Src>/.. (src) ja alterado.
  Se <pasta Src> for ".../src/Src", a saida e uma copia de ".../src" e as telas ficam em <saida>/Src.
- Idempotente: pula toda propriedade que ja contenha `varCompostoPermitida`.
- Camadas:
    C2  OnVisible de toda tela sem trava
    C3  todo OnTimerEnd
    C4  toda propriedade de comportamento (On*), exceto vazia, =false, =true
    C5  propriedade que NAO e de comportamento e le fonte de dados conectada
- Nao mexe em App.fx.yaml (OnStart, OnError, Formulas, StartScreen).
- Formato gerado (original em linhas proprias, `)` em linha propria):
        Prop: |-
            =If(varCompostoPermitida,
                <original sem o '=' inicial, +4 de recuo>
            )
"""
import csv
import json
import re
import shutil
import sys
import urllib.parse
from pathlib import Path

VAR = "varCompostoPermitida"

# Propriedades que comecam com "On" mas NAO sao de comportamento (visuais).
ON_VISUAIS = {"OnColor", "OnFill", "OnTimerFill"}


# Propriedades que sao ligacao estatica a uma fonte (nao aceitam If): o Form exige a fonte "crua".
NAO_FORMULA = {"DataSource"}


def eh_comportamento(nome: str) -> bool:
    return re.match(r"^On[A-Z]", nome) is not None and nome not in ON_VISUAIS


# --------------------------------------------------------------------------- lexer
def varrer(texto: str):
    """Devolve (codigo, linhas_em_string).
    codigo: o texto com strings e comentarios trocados por espacos (quebras de linha mantidas).
    linhas_em_string: indices (0-based) das linhas que COMECAM dentro de um literal de texto."""
    n = len(texto)
    out = list(texto)
    pilha = ["code"]
    dentro = set()
    linha = 0
    i = 0

    def branquear(a, b):
        for k in range(a, b):
            if out[k] != "\n":
                out[k] = " "

    while i < n:
        c = texto[i]
        modo = pilha[-1]
        if c == "\n":
            linha += 1
            if modo in ("str", "istr"):
                dentro.add(linha)
            i += 1
            continue
        if modo in ("code", "brace", "icode"):
            if texto.startswith("//", i):
                j = texto.find("\n", i)
                j = n if j < 0 else j
                branquear(i, j)
                i = j
                continue
            if texto.startswith("/*", i):
                j = texto.find("*/", i + 2)
                j = n if j < 0 else j + 2
                # linhas dentro do comentario de bloco nao sao string; so branqueia
                branquear(i, j)
                linha += texto.count("\n", i, j)
                i = j
                continue
            if texto.startswith('$"', i):
                pilha.append("istr")
                out[i] = out[i + 1] = " "
                i += 2
                continue
            if c == '"':
                pilha.append("str")
                out[i] = " "
                i += 1
                continue
            if c == "'":
                j = i + 1
                while j < n:
                    if texto[j] == "'":
                        if j + 1 < n and texto[j + 1] == "'":
                            j += 2
                            continue
                        break
                    j += 1
                i = j + 1
                continue
            if c == "{":
                pilha.append("brace" if modo != "icode" else "brace")
                i += 1
                continue
            if c == "}":
                if modo in ("brace", "icode"):
                    pilha.pop()
                i += 1
                continue
            i += 1
            continue
        if modo == "str":
            if texto.startswith('""', i):
                out[i] = out[i + 1] = " "
                i += 2
                continue
            out[i] = " "
            if c == '"':
                pilha.pop()
            i += 1
            continue
        if modo == "istr":
            if texto.startswith('""', i) or texto.startswith("{{", i) or texto.startswith("}}", i):
                out[i] = out[i + 1] = " "
                i += 2
                continue
            if c == "{":
                pilha.append("icode")
                out[i] = " "
                i += 1
                continue
            out[i] = " "
            if c == '"':
                pilha.pop()
            i += 1
            continue
    return "".join(out), dentro


RE_IDENT = re.compile(r"'(?:[^']|'')*'|[^\W\d]\w*", re.UNICODE)


def identificadores(codigo: str):
    """Identificadores de uso (nao precedidos de '.' ou '!', nem seguidos de ':' de campo de registro)."""
    achados = []
    for m in RE_IDENT.finditer(codigo):
        ini, fim = m.span()
        k = ini - 1
        while k >= 0 and codigo[k] in " \t\r\n":
            k -= 1
        if k >= 0 and codigo[k] in ".!":
            continue
        k = fim
        while k < len(codigo) and codigo[k] in " \t\r\n":
            k += 1
        if k < len(codigo) and codigo[k] == ":" and not codigo.startswith(":=", k):
            continue
        nome = m.group(0)
        if nome.startswith("'"):
            nome = nome[1:-1].replace("''", "'")
        achados.append(nome)
    return achados


# --------------------------------------------------------------------------- fontes
def fontes_conectadas(pasta_ds: Path):
    nomes = set()
    for f in sorted(pasta_ds.glob("*.json")):
        try:
            dados = json.loads(f.read_bytes().decode("utf-8-sig", errors="replace"))
        except Exception as e:  # noqa
            print(f"AVISO: {f.name} ilegivel ({e})", file=sys.stderr)
            continue
        if isinstance(dados, dict):
            dados = [dados]
        for o in dados:
            if o.get("Type") != "ConnectedDataSourceInfo":
                continue
            nomes.add(o.get("Name", ""))
            try:
                nomes.add(urllib.parse.unquote(f.stem, encoding="cp1252"))
            except Exception:  # noqa
                pass
            nomes.add(urllib.parse.unquote(f.stem, encoding="utf-8", errors="ignore"))
    nomes.discard("")
    return {n for n in nomes if "�" not in n}


# --------------------------------------------------------------------------- parser de YAML (formato pac)
RE_CTRL = re.compile(r"^( *)([^\s:][^:]*?) As ([\w.]+):\s*$")
RE_PROP = re.compile(r"^( *)([A-Za-z_][\w]*):(?: (.*))?$")


def recuo(l: str) -> int:
    return len(l) - len(l.lstrip(" "))


def processar_arquivo(caminho: Path, fontes: set, camadas_log: list, avisos: list):
    bruto = caminho.read_bytes().decode("utf-8")
    nl = "\r\n" if "\r\n" in bruto else "\n"
    linhas = bruto.split(nl)
    saida = []
    pilha = []  # (recuo, nome, tipo)
    tela = None
    i = 0
    n = len(linhas)
    while i < n:
        l = linhas[i]
        if not l.strip():
            saida.append(l)
            i += 1
            continue
        mc = RE_CTRL.match(l)
        if mc:
            ind = len(mc.group(1))
            while pilha and pilha[-1][0] >= ind:
                pilha.pop()
            pilha.append((ind, mc.group(2), mc.group(3)))
            if ind == 0 and tela is None:
                tela = mc.group(2)
            saida.append(l)
            i += 1
            continue
        mp = RE_PROP.match(l)
        if not mp or not pilha:
            saida.append(l)
            i += 1
            continue
        ind = len(mp.group(1))
        nome = mp.group(2)
        valor = mp.group(3) or ""
        while pilha and pilha[-1][0] >= ind:
            pilha.pop()
        dono = pilha[-1] if pilha else (0, "?", "?")
        if valor.strip().startswith("|"):
            # bloco: conteudo = linhas seguintes em branco ou com recuo > ind
            j = i + 1
            corpo = []
            while j < n and (not linhas[j].strip() or recuo(linhas[j]) > ind):
                corpo.append(linhas[j])
                j += 1
            # linhas em branco finais pertencem ao proximo trecho
            fim_vazias = 0
            while corpo and not corpo[-1].strip():
                corpo.pop()
                fim_vazias += 1
            primeiras = [x for x in corpo if x.strip()]
            bi = recuo(primeiras[0]) if primeiras else ind + 4
            conteudo = [x[bi:] if x.strip() else "" for x in corpo]
            cab = l
            fim = j - fim_vazias
            vazias_finais = linhas[fim:j]
            bloco = True
        else:
            conteudo = [valor]
            cab = None
            fim = i + 1
            vazias_finais = []
            bloco = False
            # valor simples nao pode continuar na linha seguinte
            if fim < n and linhas[fim].strip() and recuo(linhas[fim]) > ind and not RE_CTRL.match(linhas[fim]):
                mnext = RE_PROP.match(linhas[fim])
                if not mnext or recuo(linhas[fim]) > ind + 4:
                    avisos.append(f"{caminho.name}:{i+1} {nome}: valor simples com continuacao, nao tratado")
        original_txt = "\n".join(conteudo)
        decisao = decidir(nome, original_txt, dono, tela, fontes)
        if decisao and VAR not in original_txt and conteudo and conteudo[0].lstrip().startswith("="):
            camada = decisao
            novo = embrulhar(nome, ind, conteudo)
            saida.extend(novo)
            camadas_log.append((tela, dono[1], nome, camada, primeira_linha(conteudo)))
        else:
            saida.extend(linhas[i:fim])
        saida.extend(vazias_finais)
        i = j if bloco else fim
    caminho.write_bytes(nl.join(saida).encode("utf-8"))
    return tela


def primeira_linha(conteudo):
    for x in conteudo:
        s = x.strip()
        if s and s != "=":
            return s[:160]
    return ""


def decidir(nome, original_txt, dono, tela, fontes):
    """Devolve 'C2'..'C5' ou None."""
    corpo = original_txt.lstrip()
    if not corpo.startswith("="):
        return None
    if tela == "App" and dono[2] == "appinfo":
        return None
    if eh_comportamento(nome):
        sem = re.sub(r"\s+", "", corpo[1:])
        sem_cod = varrer(corpo[1:])[0].strip()
        if sem == "" or sem.lower() in ("false", "true") or sem_cod == "":
            return None
        if nome == "OnVisible":
            return "C2"
        if nome == "OnTimerEnd":
            return "C3"
        return "C4"
    if nome in NAO_FORMULA:
        return None
    codigo, _ = varrer(corpo[1:])
    if any(idn in fontes for idn in identificadores(codigo)):
        return "C5"
    return None


def embrulhar(nome, ind, conteudo):
    """Monta as linhas da propriedade embrulhada. conteudo[0] comeca com '='."""
    texto = "\n".join(conteudo)
    primeiro = conteudo[0].lstrip()[1:]  # sem o '=' inicial
    resto = conteudo[1:]
    # linhas que comecam dentro de string nao podem ser reindentadas
    _, dentro = varrer(texto[texto.index("=") + 1:])
    # indices em 'dentro' contam a partir da linha 0 do texto sem '='; a linha k>=1 corresponde a conteudo[k]
    pad_prop = " " * ind
    pad_corpo = " " * (ind + 4)
    pad_orig = " " * (ind + 8)
    out = [f"{pad_prop}{nome}: |-", f"{pad_corpo}=If({VAR},"]
    if primeiro.strip():
        out.append(pad_orig + primeiro.strip() if False else pad_orig + primeiro.lstrip())
    for k, x in enumerate(resto, start=1):
        if not x.strip():
            out.append(pad_corpo)  # o parser do pac exige o recuo do bloco tambem nas linhas em branco
        elif k in dentro:
            out.append(pad_corpo + x)  # sem o +4 (conteudo literal de texto)
        else:
            out.append(pad_orig + x)
    # v0.3.0 (revisao do chefe): tira o ';' final do original, para nao ficar 'a; b;' colado no ')'.
    # Tirar o ultimo ';' de uma cadeia nunca muda o que ela faz. So mexe se a linha termina em ';' sem comentario.
    for i in range(len(out) - 1, 1, -1):
        s = out[i].strip()
        if not s or s.startswith("//"):
            continue
        if s.endswith(";"):
            out[i] = out[i].rstrip()[:-1].rstrip()
        break
    out.append(f"{pad_corpo})")
    return out


# --------------------------------------------------------------------------- main
def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    src_telas = Path(argv[1]).resolve()
    destino = Path(argv[2]).resolve()
    rel_csv = Path(argv[3]) if len(argv) > 3 else destino.parent / "relatorio_trava.csv"
    raiz_origem = src_telas.parent if src_telas.name == "Src" else src_telas
    if destino.exists():
        print(f"ERRO: {destino} ja existe; apague ou escolha outra pasta (trabalho sempre numa copia nova).")
        return 1
    shutil.copytree(raiz_origem, destino)
    telas = destino / "Src" if (destino / "Src").is_dir() else destino
    fontes = fontes_conectadas(destino / "DataSources")
    print(f"{len(fontes)} fontes conectadas")
    log, avisos = [], []
    for f in sorted(telas.glob("*.fx.yaml")):
        if f.name == "App.fx.yaml":
            continue
        processar_arquivo(f, fontes, log, avisos)
    rel_csv.parent.mkdir(parents=True, exist_ok=True)
    with open(rel_csv, "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["tela", "controle", "propriedade", "camada", "primeira_linha_original"])
        w.writerows(log)
    por_c, por_t = {}, {}
    for t, c, p, cam, _ in log:
        por_c[cam] = por_c.get(cam, 0) + 1
        por_t[t] = por_t.get(t, 0) + 1
    print("Por camada:", dict(sorted(por_c.items())), "total", len(log))
    print("Por tela:")
    for t, q in sorted(por_t.items()):
        print(f"  {t}: {q}")
    for a in avisos:
        print("AVISO:", a)
    print("Relatorio:", rel_csv)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
