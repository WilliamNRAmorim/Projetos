# Vozes ElevenLabs v3 de uma peça dos contos (sussurro com [whispers]). Uso: python gen_voz_eleven.py c03 [--force]
# O JSON da peça traz "eleven": { "arquivo.wav": { "voz": "<voice_id>", "texto": "[whispers] ...", "estab": 0.5, "pico": 0.5 } }.
# A chave fica em ~/.elevenlabs e NUNCA é impressa. Saída: PCM 24 kHz recortado (silêncio das pontas) e normalizado pelo pico, gravado como WAV em ..\stems\serie\ep<id>\.
import json, os, sys, wave, struct, urllib.request, array
ep = sys.argv[1]; force = "--force" in sys.argv
base = os.path.dirname(os.path.abspath(__file__))
idx = json.load(open(os.path.join(base, "ep", "indice.json"), encoding="utf-8"))
d = json.load(open(os.path.join(base, "ep", idx[ep]), encoding="utf-8"))
k = open(os.path.expanduser("~/.elevenlabs")).read().strip()
if "=" in k[:30] and not k.startswith("sk_"): k = k.split("=", 1)[1].strip().strip("\"'")
out = os.path.normpath(os.path.join(base, "..", "stems", "serie", f"ep{ep}")); os.makedirs(out, exist_ok=True)
for nome, c in d.get("eleven", {}).items():
    dest = os.path.join(out, nome)
    if os.path.exists(dest) and not force: continue
    body = json.dumps({"text": c["texto"], "model_id": "eleven_v3", "voice_settings": {"stability": c.get("estab", 0.5)}}).encode("utf-8")
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{c['voz']}?output_format=pcm_24000", data=body, headers={"xi-api-key": k, "Content-Type": "application/json", "Accept": "application/octet-stream"})
    try: raw = urllib.request.urlopen(req, timeout=120).read()
    except urllib.error.HTTPError as e: print("ERRO", nome, e.code, e.read()[:200]); continue
    s = array.array("h"); s.frombytes(raw[: len(raw) // 2 * 2])
    pk = max(1, max(abs(x) for x in s)); th = pk * 0.03
    a = next((i for i, x in enumerate(s) if abs(x) > th), 0); b = len(s) - next((i for i, x in enumerate(reversed(s)) if abs(x) > th), 0)
    a = max(0, a - int(0.04 * 24000)); b = min(len(s), b + int(0.10 * 24000)); seg = s[a:b]
    g = c.get("pico", 0.5) * 32767 / pk
    with wave.open(dest, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(array.array("h", [max(-32767, min(32767, int(x * g))) for x in seg]).tobytes())
    print("ok", nome, round(len(seg) / 24000, 2), "s")
