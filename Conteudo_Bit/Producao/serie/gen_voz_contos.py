# Vozes dos contos (edge-tts). Uso: python gen_voz_contos.py c01 [--force]
# Lê ep/indice.json -> ep/<arquivo>.json. O JSON da peça traz "vozes": {"quem": ["voz","rate","pitch"]}; cada cena tem "narracao" (narrador) e "falas" [{quem, texto, rate?, pitch?, arquivo?}].
# Fala com "arquivo" (ex.: ElevenLabs) não é gerada aqui. Saída: ..\stems\serie\ep<id>\cenaN_K.mp3 (K = ordem: narração primeiro, depois falas).
import asyncio, json, os, sys, edge_tts
async def main():
    ep = sys.argv[1]; force = "--force" in sys.argv
    base = os.path.dirname(os.path.abspath(__file__))
    idx = json.load(open(os.path.join(base, "ep", "indice.json"), encoding="utf-8"))
    d = json.load(open(os.path.join(base, "ep", idx[ep]), encoding="utf-8"))
    V = d.get("vozes", {})
    out = os.path.normpath(os.path.join(base, "..", "stems", "serie", f"ep{ep}")); os.makedirs(out, exist_ok=True)
    for i, c in enumerate(d["cenas"], 1):
        segs = []
        if c.get("narracao"): segs.append(("narrador", c["narracao"], c.get("rateNarrador"), None, None))
        for f in c.get("falas", []): segs.append((f.get("quem", "narrador"), f["texto"], f.get("rate"), f.get("pitch"), f.get("arquivo")))
        for k, (quem, txt, rate, pitch, arq) in enumerate(segs, 1):
            if arq: continue
            f = os.path.join(out, f"cena{i}_{k}.mp3")
            if os.path.exists(f) and not force: continue
            v, r, p = V[quem]
            await edge_tts.Communicate(txt, v, rate=rate or r, pitch=pitch or p).save(f)
            print("ok", i, k, quem, os.path.getsize(f))
asyncio.run(main())
