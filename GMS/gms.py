#!/usr/bin/env python3
# gms.py — visões derivadas do GMS_Diario.md (append-only). Nao escreve no diario.
# Uso:
#   python3 gms.py --estado          estado atual de tudo (o que o Claude le)
#   python3 gms.py --backlog         MELs abertas, por fase
#   python3 gms.py --backlog F0      so uma fase
#   python3 gms.py --mel 073         historico completo de um ID
#   python3 gms.py --tela scr_tubo_1 historico de um alvo
#   python3 gms.py --novo            proximo ID livre
#   python3 gms.py --pendencias      insumos/perguntas em aberto
#   python3 gms.py --consolidar      NORMA/LICAO ainda nao absorvidas pelo Mestre
#   python3 gms.py --check           valida a gramatica das linhas
import re, sys, os, collections

ARQ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "GMS_Diario.md")

FECHA   = {"VALIDADO", "FEITO", "DESCARTADO"}
SAI     = {"ENTREGUE", "PUBLICADO", "BLOQUEADO"} | FECHA
REABRE  = {"ABERTO", "REVERTIDO", "RESOLVIDO"}
TIPOS   = REABRE | SAI | {"PENDÊNCIA", "LIÇÃO", "NORMA", "DECISÃO"}


def carrega():
    if not os.path.exists(ARQ):
        sys.exit(f"nao achei {ARQ}")
    linhas = []
    dentro = False
    for n, l in enumerate(open(ARQ, encoding="utf-8"), 1):
        if l.startswith("## LINHAS"):
            dentro = True
            continue
        if not dentro:
            continue
        l = l.rstrip("\n")
        if not l.strip() or l.startswith("#") or l.startswith("<!--"):
            continue
        p = [c.strip() for c in l.split("|")]
        if len(p) != 6:
            linhas.append({"erro": f"linha {n}: {len(p)} campos (esperado 6)", "raw": l, "n": n})
            continue
        linhas.append({"n": n, "data": p[0], "tipo": p[1], "alvo": p[2],
                       "ver": p[3], "refs": [] if p[4] == "—" else p[4].split(),
                       "texto": p[5], "raw": l, "erro": None})
    return linhas


def por_id(linhas):
    h = collections.defaultdict(list)
    for e in linhas:
        if e.get("erro"):
            continue
        for r in e["refs"]:
            if r.startswith("MEL-"):
                h[r].append(e)
    return h


def tag(txt, nome, default="?"):
    m = re.search(r"#" + nome + r"([A-Za-z0-9_:.\-]+)", txt)
    return m.group(1) if m else default


def cmd_backlog(linhas, fase=None):
    h = por_id(linhas)
    buckets = collections.defaultdict(list)
    for mid, evs in sorted(h.items()):
        ult = evs[-1]
        if ult["tipo"] in FECHA:
            continue
        f = "F" + tag(evs[0]["texto"], "F", "?")
        if fase and f != fase.upper():
            continue
        estado = "aberto" if ult["tipo"] in REABRE else ult["tipo"].lower()
        buckets[f].append((mid, estado, evs[0]["texto"]))
    for f in sorted(buckets):
        print(f"\n### {f} ({len(buckets[f])} itens)")
        for mid, estado, txt in buckets[f]:
            esf, imp = tag(txt, "esf"), tag(txt, "imp")
            corpo = re.sub(r"\s*#\S+", "", txt)
            marca = "" if estado == "aberto" else f" [{estado}]"
            print(f"  {mid} · esf {esf} · imp {imp}{marca} — {corpo[:110]}")


def cmd_estado(linhas):
    print("=" * 68)
    print("ESTADO GMS — derivado do diario")
    print("=" * 68)
    h = por_id(linhas)
    ab = sum(1 for e in h.values() if e[-1]["tipo"] not in FECHA)
    print(f"\nMELs: {len(h)} total · {ab} nao fechadas · {len(h)-ab} fechadas")

    print("\n-- ALVOS (ultimo estado de cada tela/lista) --")
    alvos = {}
    for e in linhas:
        if e.get("erro") or e["alvo"] == "—":
            continue
        alvos[e["alvo"]] = e
    for a, e in sorted(alvos.items()):
        v = "" if e["ver"] == "—" else " " + e["ver"]
        print(f"  {a}{v} · {e['tipo']} · {e['data']} — {e['texto'][:70]}")

    print("\n-- AGUARDANDO PUBLISH --")
    n = 0
    for mid, evs in sorted(h.items()):
        if evs[-1]["tipo"] == "ENTREGUE":
            print(f"  {mid} · {evs[-1]['alvo']} {evs[-1]['ver']} ({evs[-1]['data']})")
            n += 1
    print("  nenhum" if not n else "")

    cmd_pendencias(linhas, cabecalho=False)

    print("\n-- NORMAS FORA DO MESTRE (aplicar mesmo assim) --")
    n = 0
    for e in linhas:
        if e.get("erro") or e["tipo"] != "NORMA" or e["alvo"] == "GMS_Mestre":
            continue
        print(f"  {e['data']} · {' '.join(e['refs']) or '—'} — {e['texto'][:90]}")
        n += 1
    print("  nenhuma" if not n else "")


def cmd_pendencias(linhas, cabecalho=True):
    if cabecalho:
        print("-- PENDENCIAS --")
    else:
        print("\n-- PENDENCIAS / BLOQUEIOS --")
    abertos = {}
    for e in linhas:
        if e.get("erro"):
            continue
        chave = " ".join(e["refs"]) or e["texto"][:40]
        if e["tipo"] in ("PENDÊNCIA", "BLOQUEADO"):
            abertos[chave] = e
        elif e["tipo"] in ("RESOLVIDO", "VALIDADO", "DESCARTADO") and chave in abertos:
            del abertos[chave]
    for e in abertos.values():
        print(f"  {e['data']} · {' '.join(e['refs']) or '—'} — {e['texto'][:95]}")
    if not abertos:
        print("  nenhuma")


def cmd_mel(linhas, num):
    alvo = "MEL-" + str(num).zfill(3)
    achou = False
    for e in linhas:
        if e.get("erro"):
            continue
        if alvo in e["refs"]:
            print(f"{e['data']} · {e['tipo']:<11} · {e['alvo']} {e['ver']} — {e['texto']}")
            achou = True
    if not achou:
        print(f"{alvo}: sem registro")


def cmd_tela(linhas, nome):
    for e in linhas:
        if not e.get("erro") and nome.lower() in e["alvo"].lower():
            print(f"{e['data']} · {e['tipo']:<11} · {e['ver']:<8} · {' '.join(e['refs']) or '—'} — {e['texto']}")


def cmd_novo(linhas):
    usados = set()
    for e in linhas:
        if e.get("erro"):
            continue
        for r in e["refs"]:
            m = re.fullmatch(r"MEL-(\d+)", r)
            if m:
                usados.add(int(m.group(1)))
    n = max(usados) + 1 if usados else 1
    print(f"Proximo ID livre: MEL-{n:03d}   (maior usado: MEL-{max(usados):03d})")
    print("\nModelo (copie, ajuste, cole no fim do diario):")
    print(f"2026-MM-DD | ABERTO | — | — | MEL-{n:03d} | descricao em uma frase #F1 #esfM #impA")


def cmd_consolidar(linhas):
    print("Linhas NORMA/LICAO posteriores a ultima consolidacao do Mestre:\n")
    corte = 0
    for i, e in enumerate(linhas):
        if not e.get("erro") and e["tipo"] == "NORMA" and e["alvo"] == "GMS_Mestre":
            corte = i
    n = 0
    for e in linhas[corte + 1:]:
        if not e.get("erro") and e["tipo"] in ("NORMA", "LIÇÃO", "DECISÃO"):
            print(f"  {e['data']} · {e['tipo']} · {' '.join(e['refs']) or '—'} — {e['texto']}")
            n += 1
    print("  nada a consolidar" if not n else f"\n{n} item(ns). Peça ao Claude: 'consolide isso no Mestre'.")


def cmd_check(linhas):
    erros = [e for e in linhas if e.get("erro")]
    for e in erros:
        print("ERRO", e["erro"], "->", e["raw"][:80])
    ruins = [e for e in linhas if not e.get("erro") and e["tipo"] not in TIPOS]
    for e in ruins:
        print(f"ERRO linha {e['n']}: TIPO invalido '{e['tipo']}'")
    datas = [e for e in linhas if not e.get("erro") and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", e["data"])]
    for e in datas:
        print(f"ERRO linha {e['n']}: data invalida '{e['data']}'")
    total = len(linhas)
    print(f"\n{total} linhas · {len(erros)+len(ruins)+len(datas)} erro(s)")


if __name__ == "__main__":
    L = carrega()
    a = sys.argv[1:] or ["--estado"]
    c = a[0]
    if c == "--estado":        cmd_estado(L)
    elif c == "--backlog":     cmd_backlog(L, a[1] if len(a) > 1 else None)
    elif c == "--mel":         cmd_mel(L, a[1])
    elif c == "--tela":        cmd_tela(L, a[1])
    elif c == "--novo":        cmd_novo(L)
    elif c == "--pendencias":  cmd_pendencias(L)
    elif c == "--consolidar":  cmd_consolidar(L)
    elif c == "--check":       cmd_check(L)
    else:                      print(__doc__ or "opcao invalida; veja o cabecalho do arquivo")
