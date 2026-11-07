# Gerador dos JSONs da saga a partir de roteiros-saga.md. Uso: python build_saga.py 1 [2 3 ...]
# Cada linha "PERSONAGEM: texto" vira uma cena; PLAN define cenario/personagens por faixa de linhas.
import re, json, sys, os
BASE = r'C:\Users\willi\Downloads\Projetos'
ROT = BASE + r'\contos-de-terror-semana\serie-semana-2\roteiros-saga.md'
SER = BASE + r'\Conteudo_Bit\Producao\serie'
VOZES = {"narrador":["pt-BR-AntonioNeural","+0%","+0Hz"],"helena":["pt-BR-FranciscaNeural","+4%","+0Hz"],"otavio":["pt-BR-AntonioNeural","-12%","-12Hz"],"mi":["pt-BR-ThalitaMultilingualNeural","+10%","+4Hz"],"zelia":["pt-BR-FranciscaNeural","-16%","-6Hz"],"nilo":["pt-BR-AntonioNeural","+6%","+8Hz"],"aurelio":["pt-BR-AntonioNeural","-4%","-4Hz"],"clara":["pt-BR-FranciscaNeural","+18%","+20Hz"],"davi":["pt-BR-ThalitaMultilingualNeural","+14%","+18Hz"],"pai":["pt-BR-AntonioNeural","-14%","-10Hz"],"atendente":["pt-BR-AntonioNeural","+0%","+10Hz"],"credor":["pt-BR-AntonioNeural","+0%","+0Hz"]}
ELENCO = {"helena":{"camisa":"#3A6EA5","calca":"#2A2A3A","cabelo":"#2A1810","pele":"#D8B08C","estilo":"longo"},"otavio":{"camisa":"#5A4A3A","calca":"#2F2F3A","cabelo":"#8C8B86","pele":"#C9A07A","estilo":"careca","oculos":True,"bigode":True},"mi":{"camisa":"#E0A030","calca":"#2A3A52","cabelo":"#1B1412","pele":"#B98560","estilo":"coque"},"zelia":{"camisa":"#8A6A9A","calca":"#3A2F3A","cabelo":"#CFCFCF","pele":"#B98560","estilo":"coque"},"nilo":{"camisa":"#6A7A5A","calca":"#3A3326","cabelo":"#3A3326","pele":"#C9A07A","estilo":"calvo","bigode":True},"aurelio":{"camisa":"#2A2A44","calca":"#1A1A28","cabelo":"#4A4A4A","pele":"#D8B08C","estilo":"curto","oculos":True},"clara":{"camisa":"#E8E4F0","calca":"#E8E4F0","cabelo":"#4A2E1E","pele":"#E0BC9C","estilo":"longo"},"davi":{"camisa":"#6A8AB0","calca":"#2A2A3A","cabelo":"#2A1810","pele":"#D8B08C","estilo":"curto"},"pai":{"camisa":"#7A4A3A","calca":"#2F2F3A","cabelo":"#4A3A2A","pele":"#C9A07A","estilo":"curto"}}
COR = {1:"#E8E4D0",2:"#E08A3C",3:"#E8D44A",4:"#8FC8FF",5:"#B084FF",6:"#FF4A2A",7:"#9BC43A"}
ELEVEN = "nPczCjzI2devNBz1zQrb"
SLUG = "chegada circulo 3h33 zelia radio otavio ligacao gravacao 403 fiador recibo sombra_otavio caderno foto procissao prefeito marca homem_costas represa davi traicao eu_aceito clara ultimo_giz poco ritual nome porto_sereno".split()
def parse(n):
    t = open(ROT, encoding='utf8').read()
    blocks = re.split(r'\n## ', t)[1:]
    b = blocks[n-1]; L = b.split('\n'); nome = re.sub(r'^EP \d+/28 · | \(\d+h\)$', '', L[0]).strip()
    lines = []
    for l in L[1:]:
        m = re.match(r'^([A-ZÁÉÍÓÚÇ]+): (.*)', l)
        if m: lines.append((m.group(1).lower().replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ç','c'), m.group(2)))
    return nome, lines
def build(n, plan, sons_extra=(), rate_narr="+0%", pitch_narr="+0Hz", abertura=2.2, zoom=(1,1.08), destaque=()):
    nome, lines = parse(n); dia = (n-1)//4 + 1; slug = SLUG[n-1]; sid = f"s{n:02d}"
    cenas = [{"cenario": (plan[0][2][0] if isinstance(plan[0][2], list) else plan[0][2]), **plan[0][3], "duracao": abertura, "zoom": [1, 1.06]}]
    eleven = {}; usados = set(); k = 0
    for i, (quem, txt) in enumerate(lines, 1):
        seg = next(x for x in plan if x[0] <= i <= x[1]); _, _, cen0, opts, vis = seg[:5]; poses = seg[5] if len(seg) > 5 else {}
        cen = cen0[(i - seg[0]) % len(cen0)] if isinstance(cen0, list) else cen0
        c = {"cenario": cen, **opts}
        pers = []
        paisagem = (quem == "narrador" and (i - seg[0]) % 2 == 1) or cen in ("olhos_fechados", "quarto_terra", "quarto_musgo", "quarto_lilas")
        if not paisagem:
            for j, pid in enumerate(vis):
                x = (0.3 if (i % 2) else 0.6) if len(vis) == 1 else (0.28 if j == 0 else 0.72)
                po = poses.get(pid, "neutro"); po = po[i % len(po)] if isinstance(po, list) else po
                p = {"id": pid, "pose": po, "x": x, "escala": 0.9, "semEntrada": True, "fica": True}
                if j == 1 or (len(vis) == 1 and x > 0.5): p["flip"] = True
                if pid in ("clara", "davi"): p["escala"] = 0.6
                pers.append(p); usados.add(pid)
        if pers: c["personagens"] = pers
        zs = [[1, 1.1], [1.12, 1.0], [1.03, 1.14], [1.1, 1.02]]
        c["duracao"] = 2.5; c["zoom"] = zs[i % 4] if not paisagem else [1.0, 1.16]
        if quem == "narrador": c["narracao"] = txt; c["rateNarrador"] = rate_narr; c["pitchNarrador"] = pitch_narr
        elif quem == "credor":
            k += 1; arq = f"credor_{k}.wav"; eleven[arq] = {"voz": ELEVEN, "texto": "[whispers] " + txt, "estab": 0.5, "pico": 0.5}
            c["falas"] = [{"quem": "credor", "arquivo": arq, "texto": txt}]
        else: c["falas"] = [{"quem": quem, "texto": txt}]
        if i == len(lines): c["respiro"] = 1.2
        cenas.append(c)
    sons = [{"cena": 1, "offset": 0, "tipo": "drone", "ateCena": len(cenas), "params": {"tomInicial": 42, "subida": 0.2, "vol": 0.2}}]
    for (li, off, tipo, params, *r) in sons_extra:
        cue = {"cena": li + 1, "offset": off, "tipo": tipo, "params": params}
        if r: cue["ateCena"] = r[0] + 1
        sons.append(cue)
    ep = {"numero": n, "nome": nome.title(), "proxima": False, "legenda": "palavras", "legendaY": 1380, "legendaTam": 120, "escurece": 0.06, "saida": f"saga-dia{dia}",
          "camadas": {"voz": 1, "trilha": 1, "efeitos": 1, "musicaWav": 0}, "respiros": {"lead": 0.12, "gap": 0.15, "tail": 0.4}, "duck": 0.35,
          "cartela": {"titulo": "PORTO SERENO", "sub": f"EP {n:02d}/28 · {nome.upper()}"}, "cor": COR[dia], "arquivo": f"{n:02d}_{slug}.mp4",
          "destaque": list(destaque), "sons": f"{sid}_sons.json", "vozes": {k2: v for k2, v in VOZES.items()}, "elenco": {k2: ELENCO[k2] for k2 in usados if k2 in ELENCO}, "cenas": cenas}
    if eleven: ep["eleven"] = eleven
    json.dump(ep, open(f"{SER}\ep\{sid}_{slug}.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
    json.dump({"versao": 1, "episodio": sid, "cues": sons}, open(f"{SER}\ep\{sid}_sons.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
    print(sid, nome, len(lines), "linhas", sum(len(x[1].split()) for x in lines), "palavras")
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(__file__)); import plan_dia1_2
    for a in sys.argv[1:]: plan_dia1_2.PLANOS[int(a)](build)
