# GMS: revisão do filme (prévia sem voz, 62 s)

Revisado quadro a quadro nas versões 16:9 e 9:16, com base no checklist da skill `motion-design`.

## 1. S03: a linha do tempo não segue uma linha (9,9 a 19,9 s), prioridade alta

**Problema.** A cena mostra três etiquetas soltas: "WAVE 1 · 1 MONTH", depois "WAVE 2 · 5 MONTHS" e depois "WAVE 3 · 2 MONTHS". As marcas da barra ficam igualmente espaçadas. Quem assiste lê os números 1 → 5 → 2 e entende que voltou no tempo. Na verdade são durações de fases consecutivas, mas nada na tela mostra que elas somam 8 meses.

**Correção: uma régua única de 8 meses, sempre andando para a direita.**

```
 M1 | M2  M3  M4  M5  M6 | M7  M8        TODAY
[██]|[████████████████████]|[████████]  →  ● all 8 stages live
DIAGNOSE      BUILD            HARDEN
```

- Uma trilha com 8 marcas (M1 a M8) e um cursor que só avança. Cada fase é um trecho **proporcional** da régua (1/8, 5/8, 2/8), então "5 meses" aparece maior sem precisar de explicação.
- Contador fixo no canto: **Month 1 → Month 8**. É o número que sobe e dá a sensação de linha.
- Nomes das fases iguais aos do Kaizen: **Diagnose · Build · Harden** (no lugar de "Wave 1/2/3").
- O print de fundo muda no limite de cada fase. O tempo de tela pode seguir 2 s / 4 s / 2,5 s, sugerindo a proporção.
- Fecha em **TODAY**: a régua completa vira o anel das 8 etapas, o mesmo símbolo do final. Isso amarra S03 com S09.

**Novo texto da narração (S03):**

> Month **one**: mapping the cell. Months **two to six**: building it. Months **seven and eight**: making every number **match the floor**.

São cerca de 19 palavras (≈ 7 s), que cabem nos 10 s da cena sem acelerar a voz. A versão antiga dizia "One month… Five months… Two months…" e recriava o mesmo vai-e-volta.

## 2. Legendas atrasadas, prioridade alta

As legendas gravadas no vídeo ficam **uma frase atrás** da imagem. Por exemplo, aos 13,5 s o título diz "Building" e a legenda ainda está em "mapping the cell with the". O mesmo acontece em S04 a S07. Elas foram cronometradas para uma voz estimada. **Gere as legendas de novo a partir da voz real**, depois do `mix.py`, e não antes.

## 3. Números de impacto somem rápido demais (S08, 44 a 52 s), prioridade média

Os números estão corretos e conferem com o Kaizen (36×, −97%, 0 → 100%, €0). O problema é que a contagem dura ~1,5 s e o número final fica parado só **~0,6 s** antes do corte. No celular, ninguém lê "−97%".

- Contagem em 0,6 a 0,8 s, com ease-out e um pequeno overshoot. O número final fica parado **≥ 1,2 s**.
- Mantém o ritmo de 2 s por número (o cue sheet não muda).

## 4. Versão 9:16: telas do app pequenas demais, prioridade média

No vertical, os prints do app (que são horizontais) ocupam ~30% da altura e o resto fica vazio. No celular, o campo da OP, o carretel e o alerta ficam ilegíveis.

- Aplique um **punch-in** de 1,6 a 2× no ponto da ação: no campo enquanto digita a OP (S04), no card "parada sem motivo" (S05) e na lista de motivos (S07).
- Mantenha títulos e legendas fora dos 20% inferiores, que a interface do Instagram cobre.

## 5. Ritmo da abertura para o Reel, prioridade baixa

S02 tem 6 palavras com 1 s cada. São 6 s só de texto antes de aparecer o produto. A 120 BPM, dá pra usar **meio tempo (0,5 s) por palavra**, sem sair do ritmo da música. O app aparece ~3 s antes, o que importa no Reel, onde a retenção cai nos primeiros 3 s.

**Opcional:** um corte de ~30 s só pro Reel (S01 → S02 curto → S04 → S06 → S08 → S09). O filme de 62 s fica pra LinkedIn e apresentação.

## 6. Antes de publicar

- Confira se o rodapé do S08 e as telas mostram nome da empresa, OPs reais ou nomes de operadores. Se mostrarem, desfoque. O documento do Kaizen cita a empresa e é interno.
- "€0 capex" está em euro porque segue o Kaizen. Num post em PT-BR, vale "custo zero de investimento".

## O que eu não consegui fazer daqui

O código que **renderiza** o vídeo não está nesta pasta. O `LEIA-ME` da trilha cita `../out/GMS_Filme_Roteiro_e_Tempos.md` e os MP4 "mudo" em 1080p, que ficaram no outro projeto. Se você colocar aqui a pasta do projeto que gerou o filme, eu aplico as correções 1 a 5 e renderizo de novo.
