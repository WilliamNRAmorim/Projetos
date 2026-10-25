# Gera as vozes de um episodio da serie com edge-tts (gratuito, sem chave). Uso: python gen_voz_serie_edge.py 01 [--force]
# Le ep/indice.json -> ep/<arquivo>.json e grava ..\stems\serie\epXX\cenaN_K.mp3 (K = ordem de fala na cena: narracao primeiro, depois 'falas').
# Cena: "narracao" = narrador ("rateNarrador": "+18%" muda o ritmo só nessa cena); "falas": [{"quem": "bia|dalva|osmar|sete|narrador", "texto": "..."}] tocadas em ordem depois da narracao.
import asyncio, json, os, sys, edge_tts
VOZES = {  # quem: (voz, rate, pitch)  (aprovadas pelo William; 'sete' = voz do quarto 7 pelo interfone, variante lenta/grave do narrador)
    "narrador": ("pt-BR-AntonioNeural", "+10%", "+0Hz"),  # +10% (William, 25/10: estava lento)
    "bia": ("pt-BR-ThalitaMultilingualNeural", "+0%", "+0Hz"),
    "dalva": ("pt-BR-ThalitaMultilingualNeural", "-22%", "-10Hz"),
    "osmar": ("pt-BR-AntonioNeural", "-18%", "-14Hz"),
    "sete": ("pt-BR-AntonioNeural", "-22%", "-12Hz"),
}
def segmentos(c):
    s = []
    if c.get("narracao"): s.append(("narrador", c["narracao"], None))
    for f in c.get("falas", []): s.append((f.get("quem", "narrador"), f["texto"], f.get("rate")))  # "rate" por fala (ex.: "-32%" alonga a palavra)
    return s
async def main():
    ep = sys.argv[1]; force = "--force" in sys.argv
    base = os.path.dirname(os.path.abspath(__file__))
    idx = json.load(open(os.path.join(base, "ep", "indice.json"), encoding="utf-8"))
    d = json.load(open(os.path.join(base, "ep", idx[ep]), encoding="utf-8"))
    out = os.path.normpath(os.path.join(base, "..", "stems", "serie", f"ep{ep}")); os.makedirs(out, exist_ok=True)
    for i, c in enumerate(d["cenas"], 1):
        for k, (quem, txt, rate) in enumerate(segmentos(c), 1):
            f = os.path.join(out, f"cena{i}_{k}.mp3")
            if os.path.exists(f) and not force: continue
            v, r, p = VOZES[quem]
            if quem == "narrador" and c.get("rateNarrador"): r = c["rateNarrador"]
            if rate: r = rate  # ritmo do narrador só nessa cena (ex.: lista de regras)
            await edge_tts.Communicate(txt, v, rate=r, pitch=p).save(f)
            print("ok", i, k, quem, os.path.getsize(f))
asyncio.run(main())
