# Créditos e origem dos ativos

Nada nesta apresentação foi baixado de fonte externa: nenhuma imagem, ícone, modelo 3D, vídeo, música ou fonte de terceiros entra no repositório nem no arquivo `GMS_Defesa.pptx`. O deck não embute vídeo nem áudio: a única mídia é imagem (PNG). Dado de produção, nome de empresa, de pessoa e foto da fábrica não aparecem em nenhum ativo.

## Fontes (tipografia)

| Fonte | Onde aparece | Origem e licença |
|---|---|---|
| Bahnschrift (variações Condensed, SemiBold, SemiLight) | Quase todo o texto: rótulos, frases-guia, números, "GMS" do slide final | Acompanha o Windows 10 (versão 1709) e o Windows 11. Licença da Microsoft, uso dentro do Windows e do Office. Não está embutida no arquivo nem distribuída aqui. |
| Consolas | Rodapé dos slides (contador e citação), código e tabelas técnicas | Acompanha o Windows e o Office. Licença da Microsoft, mesma condição. Não embutida. |
| Ink Free | Letra manuscrita da ficha de papel (dado fictício) | Acompanha o Windows 10 e o Windows 11. Licença da Microsoft, mesma condição. Não embutida. |

Consequência prática: o deck só mostra a tipografia certa em computador com Windows 10 ou 11 (ou com essas fontes instaladas). Em outro sistema o PowerPoint troca por uma fonte mais larga e o texto pode invadir o vizinho; para esse caso valem o `GMS_Defesa.pdf` e o `GMS_Defesa.mp4`, que já têm as fontes gravadas.

## Imagens e marcas

| Ativo | Arquivo | Autoria e licença |
|---|---|---|
| Logo da UNISAL | `unisal_logo.png` | Marca da instituição de ensino, extraída do trabalho do próprio aluno (pitch do TCC I). Aparece só na capa, sobre placa branca, sem recolorir nem distorcer. Não é do repositório e não tem licença aberta: uso institucional, só na defesa. |
| Carretel e logo do GMS | Formas do PowerPoint, desenhadas em `build/gms_lib.ps1` a partir de `Conteudo_Bit/Marca/logo_gms_escuro.svg` | Marca do próprio projeto, de autoria do aluno. Nenhum arquivo de imagem. |
| Ficha de papel da abertura | Formas e texto do PowerPoint (`Add-Ficha`, em `build/gms_lib.ps1`) | Autoria própria. Todo o preenchimento é fictício; não é digitalização de ficha real. |
| Globo de pontos (slides 43 a 45) | Ovais do PowerPoint, gerados por `build/cap7.ps1` | Autoria própria. O contorno das Américas, da Groenlândia e de algumas ilhas foi aproximado à mão no script, sem fonte externa e sem arquivo de imagem. |
| Mangueira hidráulica (slides 15 a 19 e 47) | `mangueira.glb`, `camadas/*.glb`, `mangueira_*.png` e `pecas/pc_*.png` | Autoria própria. Modelo gerado por código (numpy e Pillow) em `gerador/gerar_mangueira.py`, com 123.008 triângulos; as imagens saem de um rasterizador próprio (`gerador/renderizar.py`) e são recortadas por `gerador/recortar_pecas.py`. O deck usa as imagens; os `.glb` ficam como ativo para quem quiser inserir o modelo 3D à mão. Nada baixado, nenhum modelo de terceiros. |
| Telas recriadas do GMS | `telas/*.png` (cartões do mosaico e telas do tablet e do plano B) | Autoria própria. Recriadas por `gerador/gerar_telas.py` (Pillow) com dado 100% fictício; nenhum print real, nenhuma OP, pessoa ou quantidade verdadeira. |

## Ferramentas de montagem

- O deck é montado por scripts PowerShell que dirigem o PowerPoint pelo COM do Windows (`build/`). Os ativos de imagem e o modelo 3D são gerados por scripts Python com numpy e Pillow, ambos de código aberto, usados só na máquina do autor e não distribuídos aqui.

## Licenças das peças de terceiros

Não há peça de terceiros com licença aberta (CC0, CC-BY, Google Fonts etc.) neste conjunto. As únicas peças que não são de autoria própria são a logo da UNISAL e as três fontes do Windows, descritas acima.
