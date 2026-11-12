# MOTOR_GUIA: como pedir cada efeito pelo JSON

Para quem escreve o episódio (Sonnet/Opus): basta editar o JSON em `ep/` e rodar o render. Não é preciso mexer no `motor.js` nem no `motor_fx.js`.

**Regra de ouro:** tudo aqui vive na chave `"visual"`. Episódio sem `"visual"` sai idêntico ao que já foi publicado (provado por hash). Nunca coloque `"visual"` num JSON já publicado (c01–c28, s01–s28, o25–o28): copie para um arquivo novo.

## 1. Receita rápida

No episódio (vale para todas as cenas):
```json
"visual": "terror"
```
Atalhos prontos: `"terror"` (vinheta, grão, poeira, neblina leve, brilho), `"noite"` (luar azulado e neblina), `"vela"` (escuro com uma vela no centro), `"limpo"` (só o básico). Todos já ligam personagens v2, movimento, sombra e legenda automática.

Para partir de um atalho e mudar um campo: `"visual": { "preset": "terror", "neblina": 0 }`.

`"visual": true` é o mesmo que `"limpo"`.

Na cena, `"visual": { ... }` sobrescreve campo a campo o do episódio. `"visual": false` desliga tudo naquela cena. `"luz": null` desliga só a luz.

## 2. Atmosfera (Fase 1)

| Campo | Valor | O que faz |
|---|---|---|
| `vinheta` | 0 a 1 | Escurece as bordas. 0,5 é o normal. |
| `grao` | 0 a 1 | Grão de filme que se mexe (troca a cada 2 quadros). |
| `neblina` | 0 a 1 | 5 faixas lentas na metade de baixo. `neblinaCor`: `"#B9B4C0"`. |
| `poeira` | 0 a 1 | 70 partículas lentas; brilham mais perto da luz. |
| `brilho` | 0 a 1 | Halo nas partes claras (janela, lâmpada, tela). 0,3 a 0,45. |
| `cor` | nome ou `{ "cor": "#hex", "forca": 0.45 }` | Tinge a cena: `frio`, `quente`, `sepia`, `verde`, `sangue`, `luar`, `roxo`. |
| `escuro` | 0 a 1 | Escuridão geral; as luzes abrem buracos nela. Com `luz` o padrão é 0,45. `escuroCor` muda o tom. |
| `luz` | objeto ou lista | Ver abaixo. |

```json
"luz": { "tipo": "vela", "x": 0.2, "y": 0.6, "raio": 520, "intensidade": 0.7, "cor": "#FFC98A" }
```
- `tipo`: `vela` (treme), `lanterna` (firme, cai de vez em quando), `lampada` (pisca em rajadas), `tv` (cintila azulado), `raio` (dois clarões a cada ~5 s), `fixa`.
- `x`, `y`: até 2 é fração da tela (0,5 = meio); acima disso são pixels. A luz fica presa à tela, não à câmera.
- A luz também decide o lado da sombra e do fio de luz nos personagens (usa a primeira da lista).

## 3. Personagens em vetor v2 (Fase 2)

| Campo | Valor | O que faz |
|---|---|---|
| `personagens` | `true` | Olho com íris e brilho, pálpebra, sobrancelha por expressão, nariz, boca por pose, orelha, cabelo com franja e mecha, gola, cinto, lado na sombra. |
| `sombra` | `true` | Sombra de contato + sombra projetada para o lado oposto ao da luz. |

Nada muda em `elenco` nem nas poses: os mesmos nomes (`neutro`, `assustado`, `olhando`...) ganham o rosto novo. Extras opcionais no `elenco`: `"olhos": "#4A3222"` (cor da íris).

A boca abre e fecha sozinha quando o personagem fala: a fala precisa ter `"quem"` igual ao `id` do personagem (ou o personagem ter `"voz": "nome"` igual ao `quem`).

Limites: personagem de costas ganha a roupa nova mas não rosto nem cabelo novos; hóspede com `luz` (contorno de luz) não tem sombra; gente desenhada pelo próprio cenário (cama, espelho, olho mágico) continua no traço antigo.

## 4. Composição (Fase 3)

### Câmera
```json
"camera": { "plano": "close", "foco": "helena", "mao": 0.5 }
```
| Campo | Valor | O que faz |
|---|---|---|
| `plano` | `aberto`, `medio`, `close`, `detalhe` | Enquadramento. `close` pega cabeça e ombros. |
| `foco` | `id` do personagem ou `[x, y]` | Onde a câmera mira. Sem `foco`, usa `x`/`y` (padrão: centro). |
| `zoom` | número | Zoom livre em vez de `plano` (1 = normal). |
| `ate` | `"close"` ou `{ "zoom": 1.5, "foco": [0.5, 0.3] }` | Aproxima devagar do primeiro enquadramento até este. `dura` (s) e `espera` (s) ajustam. |
| `angulo` | `plongee`, `contra` | Visto de cima (personagem pequeno, oprimido) ou de baixo (ameaçador). `forca` 0 a 0,5 (padrão 0,26). |
| `mao` | 0 a 1 | Câmera na mão: balanço leve. 0,5 já aparece. |
| `inclina` | radianos | Horizonte torto (0,04 a 0,08). |

O `zoom` e o `pan` antigos da cena continuam valendo e somam com a câmera. Forma curta: `"camera": "close"`.

### Chão
```json
"chao": { "tipo": "tabua", "cor": "#2A211B", "tapete": "#5A1F1A" }
```
Ocupa a metade de baixo com piso em perspectiva e poça de luz. `tipo`: `tabua`, `ladrilho`, `terra`, `asfalto`, `liso`. `y` (padrão: linha dos pés), `fuga` (0 a 1, ponto de fuga), `tapete` (cor), `tapeteX` e `linha` (cor das juntas). Use em cenário cujo chão é liso; em cenário que já desenha piso, deixe sem.

### Primeiro plano
```json
"primeiroPlano": ["galhos", { "tipo": "batente", "lado": "esq" }]
```
Silhuetas escuras e desfocadas na frente da cena, com paralaxe. `tipo`: `batente`, `moldura` (espiando por uma porta), `cortina`, `planta`, `galhos`, `grade`, `mesa`, `ombro` (alguém de costas perto da câmera), `degraus`. Opções: `lado` (`esq`/`dir`), `cor`, `desfoque`, `alfa`, `escala`, `x`, `y`.

### Legenda
- `"legenda": "auto"`: escolhe, uma vez por cena, a altura que não cobre nenhum rosto. `legendaY` na cena continua mandando.
- `"legendaFundo": 0.4`: faixa escura suave atrás da legenda, para cena clara.

## 5. Movimento (Fase 4)

| Campo | Onde | O que faz |
|---|---|---|
| `movimento: true` | `visual` | Pisca a cada 3 a 6 s (às vezes duas vezes), respira mais, cabeça e peso do corpo nunca param, olhada de lado de vez em quando, braços soltos balançam. |
| `olha` | no personagem | `"olha": "porteiro"` (id) ou `"olha": 0.8` (x de 0 a 1): olhos e rosto viram para lá. |

Poses de olhar fixo (`sorrindo`, `encarando`, `seria`...) não piscam de propósito: é o que dá medo.

## 6. Exemplo completo de cena
```json
{ "cenario": "corredor", "duracao": 5, "narracao": "Ela parou na porta.",
  "falas": [{ "quem": "ana", "texto": "Tem alguém aí?" }],
  "personagens": [{ "id": "ana", "pose": "hesitante", "x": 0.4, "olha": 0.9 }],
  "visual": { "luz": { "tipo": "lampada", "x": 0.5, "y": 0.12, "raio": 600 },
              "camera": { "plano": "medio", "ate": "close", "foco": "ana", "mao": 0.5 },
              "primeiroPlano": [{ "tipo": "batente", "lado": "dir" }], "cor": "frio" } }
```

## 7. Rodar e conferir

Com o `Producao/serve.ps1` aberto, dentro de `Producao/serie`:

| Para | Comando |
|---|---|
| Folha de contato (meio de cada cena) | `node linha_base.js folha <id> preview/motor/<id>.png` |
| Quadros escolhidos | `node linha_base.js folha <id> saida.png 3.2,6.5,9` |
| Ver só até uma fase | acrescente `--q=fase=1` (1 atmosfera, 2 personagens, 3 composição) |
| Tempo de render estimado | `node linha_base.js tempo <id>` |
| Provar que os publicados não mudaram | `node linha_base.js conferir` (4 min; tem de dar `IGUAL`) |
| Render do MP4 | `node driver.js render "http://127.0.0.1:5178/Producao/serie/contos.html?ep=<id>&render=1"` |

`<id>` é a chave em `ep/indice.json`. Episódios `s*` e `o*` usam `saga_o.html`; o `linha_base.js` escolhe a página sozinho.

Exemplos prontos para copiar: `ep/c04_visual_teste.json` (id `t04`) e `ep/s01_visual_teste.json` (id `t_s01`).

## 8. Antes de publicar
1. `node linha_base.js conferir` tem de dar `IGUAL`.
2. Olhe a folha com `&safe=1` na URL: a vinheta e o primeiro plano não podem tirar contraste da legenda.
3. `luz` com `lampada` ou `raio` pisca forte; evite em cena longa de leitura.
4. Custo: a camada visual acrescenta cerca de 35 ms por quadro (medido no s01: 31 para 65 ms). O que pesa mesmo é `desfoque` na cena (centenas de ms por quadro).
5. Não mude `linha_base.json` à mão. Só regrave (`gravar`) quando um episódio novo for publicado, e só para o id dele: `node linha_base.js gravar c29`.
