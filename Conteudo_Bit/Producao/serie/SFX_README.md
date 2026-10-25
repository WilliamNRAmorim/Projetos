# sfx.js - sons e música sintetizados (Plantão Noturno)

Módulo autônomo, só Web Audio, sem arquivos nem licença. Teste: abrir `sfx_demo.html` (tocar, WAV de cada um, WAV de todos).

## API
```js
const s = Sfx.create(audioCtx, audioCtx.destination);   // opts: {seed}
s.chuva(t, 30, {zinco:true});  s.stinger(t+12, 1);       // t em segundos do contexto
```
Todos os métodos retornam `{t, fim}`. Opção comum: `vol` (multiplicador). Também `s.tocar(tipo, t, params)` (params em objeto).

| Método | Argumentos / opções |
|---|---|
| `drone(t,dur,{tomInicial=55,subida=3})` | subida em semitons ao longo de `dur` |
| `pulso(t,dur,bpm=60)` / `batimento(t,dur,bpm=70)` | pulso grave / lub-dub |
| `tiquetaque(t,dur,{lentidao=0..1,intervalo=1})` | `lentidao` alonga o intervalo e abafa; `param` = alias de `intervalo` |
| `tiquetaquePara(t,{silencio=2.5})` | último tique pesado + abaixa a cama por `silencio` s |
| `stinger(t,intensidade=1)` | 0..1 (pico -6 dBFS em 1) |
| `chuva(t,dur,{zinco,corte})` | `zinco` = telhado; `corte:true` = termina em 40 ms |
| `campainha(t)`, `papelRasgando(t)`, `acordeBia(t,{dur})` | |
| `passosChinelo(t,n,{passo=0.75})`, `batidas(t,n=3,espacamento=1.5)` | |
| `cantarolar(t,dur)`, `zumbidoLuz(t,dur)`, `passaros(t,dur)`, `vento(t,dur)` | |
| `celularToque(t,{abafado=true})` | |
| `caixinha(t,dur,{desafinada,lenta,reversa,afasta})` | melodia de ninar em lá menor; `afasta` = volume cai ~18 dB e abafa ao longo de dur |
| `pianoBia(t,notas,{passo=1.2})` | notas: MIDI, nome (`"A3"`) ou acorde (array) |
| `silencioDuck(t,dur,{nivel=0.03})` | abaixa a "cama" (drone, pulso, tique-taque, chuva, vento, zumbido, batimento, caixinha, pássaros) |

Chame os `silencioDuck`/`tiquetaquePara` em ordem cronológica (automação do barramento).

## Offline e cue-sheet
`Sfx.renderOffline(cues, duracao, {sampleRate, seed, inicios})` -> `Promise<AudioBuffer>` (estéreo). `cues = [{t, tipo, params}]`.
Cue-sheet por episódio (JSON), para o motor ler depois:
```json
{ "versao": 1, "episodio": "ep01", "cues": [
  { "cena": 1, "offset": 0,   "tipo": "chuva",   "params": { "dur": 40, "zinco": true } },
  { "cena": 3, "offset": 1.2, "tipo": "caixinha","params": { "dur": 8, "desafinada": true } },
  { "cena": 11,"offset": 0,   "tipo": "stinger", "params": { "intensidade": 0.8 } } ] }
```
`Sfx.resolverFolha(folha, inicios)` converte para cues com `t = inicio da cena + offset` (`inicios` = `{cena: segundos}` ou função). `Sfx.agendar(inst, cues, t0)` toca no contexto vivo. Auxiliares: `Sfx.analisar(buffer)`, `Sfx.toWav(buffer|[buffers], gap)`.

## Verificação (OfflineAudioContext no Chrome, 44,1 kHz, cada som sozinho)
Alvo: cama/efeitos -18 a -12 dBFS de pico, stinger -6. Ganhos de calibração (`CAL`) ajustados por medição.

| Som (demo) | dur s | pico dBFS | RMS dBFS | NaN | amostras >=0,999 | silêncio total | borda ini/fim |
|---|---|---|---|---|---|---|---|
| drone | 10.0 | -15.0 | -24.5 | 0 | 0 | não | 0 |
| pulso | 8.0 | -15.0 | -34.4 | 0 | 0 | não | 0 |
| tiquetaque | 10.0 | -15.0 | -43.0 | 0 | 0 | não | 0 |
| tiquetaque (lentidão 1) | 14.0 | -15.0 | -46.3 | 0 | 0 | não | 0 |
| tiquetaque + para + drone | 8.0 | -11.8 | -28.0 | 0 | 0 | não | 0 |
| stinger (1.0) | 5.0 | -6.0 | -29.9 | 0 | 0 | não | 7e-10 |
| stinger (0.4) | 5.0 | -10.3 | -34.2 | 0 | 0 | não | 4e-10 |
| chuva zinco | 12.0 | -15.0 | -30.3 | 0 | 0 | não | 0 |
| chuva abafada | 12.0 | -16.5 | -29.9 | 0 | 0 | não | 0 |
| campainha | 5.0 | -12.0 | -33.3 | 0 | 0 | não | 2e-14 |
| passosChinelo | 6.0 | -14.0 | -38.7 | 0 | 0 | não | 0 |
| cantarolar | 8.0 | -16.0 | -27.2 | 0 | 0 | não | 0 |
| batidas | 7.0 | -12.0 | -37.7 | 0 | 0 | não | 8e-19 |
| celularToque | 5.0 | -14.0 | -27.6 | 0 | 0 | não | 0 |
| zumbidoLuz | 7.0 | -16.0 | -27.4 | 0 | 0 | não | 0 |
| papelRasgando | 2.5 | -14.0 | -33.0 | 0 | 0 | não | 0 |
| passaros | 9.0 | -17.0 | -32.9 | 0 | 0 | não | 0 |
| vento | 9.0 | -16.0 | -32.5 | 0 | 0 | não | 0 |
| caixinha | 10.0 | -18.5 | -31.7 | 0 | 0 | não | 0 |
| caixinha desafinada+lenta | 14.0 | -19.4 | -32.9 | 0 | 0 | não | 0 |
| caixinha reversa | 10.0 | -15.0 | -25.2 | 0 | 0 | não | 0 |
| pianoBia | 9.0 | -15.0 | -29.2 | 0 | 0 | não | 5e-9 |
| acordeBia | 5.0 | -15.0 | -28.4 | 0 | 0 | não | 0 |
| batimento | 8.0 | -14.0 | -32.2 | 0 | 0 | não | 0 |
| silencioDuck (drone+chuva+duck+stinger 0.8) | 9.0 | -6.7 | -25.8 | 0 | 0 | não | 7e-8 |

Outras checagens: o `silencioDuck` derrubou o RMS da cama de -23,9 dB para -52,3 dB e ela voltou (-28,4 dB, com o stinger no trecho); a cue-sheet resolvida por `resolverFolha` renderiza (campainha a -12,0 dB); duas renderizações iguais diferem no máximo 7e-7 (-123 dB, ruído numérico). Cada som começa e termina em zero (borda < 1e-7), então não há estalo nas pontas.

## O que não dá para garantir sem ouvir
- Se cada som "parece" o que é: relógio de parede, sino de balcão, caixinha de música, passos de chinelo e cantarolar de idosa são aproximações sintéticas; o cantarolar e o piano são os mais distantes do real.
- Estalos internos (descontinuidades no meio do som) e o equilíbrio de timbre; a medição só cobre pico, RMS, bordas e saturação.
- Se a cama de -15 dB de pico fica sob a voz do ElevenLabs: o RMS real é bem menor (-24 a -46 dB), mas o equilíbrio com a voz precisa de ouvido; ajuste por `vol` ou `CAL`.
- Os valores de CAL foram calibrados com o Chrome; outro navegador pode diferir em décimos de dB.
