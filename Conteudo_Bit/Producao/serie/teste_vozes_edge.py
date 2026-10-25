# Teste de elenco com vozes neurais gratuitas do Edge (edge-tts). Sem chave, sem custo.
import asyncio, os, edge_tts
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "preview", "vozes_edge")
os.makedirs(out, exist_ok=True)
NARR = "A dona se chamava Dalva. Sorria demais. Piscava de menos."
# arquivo, voz, texto, rate, pitch, volume
T = [
 ("narrador_antonio_normal", "pt-BR-AntonioNeural", NARR, "+0%", "+0Hz"),
 ("narrador_antonio_grave_lento", "pt-BR-AntonioNeural", NARR, "-12%", "-10Hz"),
 ("narrador_francisca_lenta", "pt-BR-FranciscaNeural", NARR, "-10%", "-4Hz"),
 ("bia_thalita", "pt-BR-ThalitaMultilingualNeural", "Oi, eu sou a Bia.", "+0%", "+0Hz"),
 ("bia_francisca", "pt-BR-FranciscaNeural", "Oi, eu sou a Bia.", "+0%", "+0Hz"),
 ("dalva_francisca_doce_lenta", "pt-BR-FranciscaNeural", "Atende o sete, Bia. Meu bem, é só atender.", "-22%", "-8Hz"),
 ("dalva_thalita_grave_lenta", "pt-BR-ThalitaMultilingualNeural", "Atende o sete, Bia. Meu bem, é só atender.", "-22%", "-10Hz"),
 ("osmar_antonio_velho", "pt-BR-AntonioNeural", "Você disse o seu nome, menina.", "-18%", "-14Hz"),
 ("junior_thalita_crianca", "pt-BR-ThalitaMultilingualNeural", "Moça, não olha pra cima.", "+5%", "+30Hz"),
]
async def main():
    for nome, voz, txt, rate, pitch in T:
        f = os.path.join(out, nome + ".mp3")
        try:
            await edge_tts.Communicate(txt, voz, rate=rate, pitch=pitch).save(f)
            print("ok", nome, os.path.getsize(f))
        except Exception as e:
            print("falhou", nome, e)
asyncio.run(main())
