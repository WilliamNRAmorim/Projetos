# Estado do motor visual (missão P1 do PLANO_FABLE), 11/11/2026

## Entregue
| Fase | O que ficou | Prova |
|---|---|---|
| 0 Linha de base | `linha_base.js` + `linha_base.json`: hash de 1686 quadros (3 por cena) de c01–c28, s01–s28, o25–o28 | `preview/motor/f0_*_antes.png` |
| 1 Atmosfera | vinheta, grão animado, neblina, poeira, brilho, cor, escuro e luz (vela, lanterna, lâmpada, tv, raio, fixa) | `f1_*_depois.png` |
| 2 Personagens v2 | olho com íris e brilho, pálpebra, sobrancelha por expressão, nariz, boca por pose, orelha, cabelo com franja, gola, cinto, lado na sombra, sombra projetada | `f2_*_depois.png` |
| 3 Composição | câmera (médio, close, detalhe, aproximação, plongée, contraplongée, câmera na mão), chão em perspectiva, 9 primeiros planos, legenda automática e fundo de legenda | `f3_*_depois.png` |
| 4 Movimento | piscar, respirar, cabeça e peso que não param, olhada de lado, `olha` (olhar para alguém), boca que fala junto com a fala, sombra que segue os pés | `f4_*_depois.png`, `f4_s01_movimento.png` |

Episódios de teste: `t04` (`ep/c04_visual_teste.json`) e `t_s01` (`ep/s01_visual_teste.json`). O `t_s03` antigo continua funcionando.

## Conferência
- `node linha_base.js conferir` no fim: **IGUAL, 60 episódios, 1686 quadros** (`preview/motor/conferir_final.log`).
- Determinismo: `node linha_base.js hash t04 t_s01` duas vezes deu o mesmo hash.
- Teste de carga: 6 episódios publicados copiados com tudo ligado ao mesmo tempo (2 luzes, 8 primeiros planos, plongée, câmera na mão) renderizaram sem erro.
- `revisor-leve`: aprovado com ajustes; os ajustes foram aplicados (altura da legenda não depende mais do quadro pedido, foco da câmera em zoom baixo, poça de luz no mesmo tempo da luz, cor da neblina validada, texto do guia).

## Tempo de render (Edge headless, esta máquina)
| Episódio | Sem visual | Com tudo ligado |
|---|---|---|
| s01 (27 s) | 31 ms/quadro | 65 ms/quadro; MP4 inteiro sem voz em 39 s |
| s26 com carga máxima (60 s) | – | 70 ms/quadro |
| c04 (43 s) | 280 a 440 ms/quadro | 100 a 330 ms/quadro |

O c04 é lento por causa do `desfoque` da cena 6 (filtro de blur do canvas), que já existia; a medida dele oscila muito e a camada visual não é o gargalo.

## Achados no caminho
- O `README.md` descrevia a chave `visual` desde 07/11, mas o código nunca tinha entrado no `motor.js`. Agora existe, e os JSON de teste antigos (`t04`, `t_s03`) seguem válidos.
- `Semanal/teste-motor/` e `Semanal/teste-f1/` não estão no `.gitignore`. Os MP4 de teste ficaram fora do commit de propósito.
- O `driver.js` antigo ainda cria `preview/edgeprof-contos-*`. O `linha_base.js` usa a pasta temporária do sistema e não deixa nada no repositório.

## O que sobrou
1. **Fase 6 (motor em módulos)**: não feita, para poupar a barra. O `motor_fx.js` já nasceu separado; falta dividir o `motor.js` (cenário, pose, efeito, render) e juntar os `contos*.js`. O `linha_base.js conferir` é a rede de segurança para fazer isso.
2. **Fase 5 (cenários PNG)**: fora desta missão, é do `produtor-de-artes`.
3. **Fase 7 (limpeza)**: mover `preview/edgeprof-*` para `_arquivo` e só apagar com o "sim" do William. Trocar o perfil do `driver.js` para a pasta temporária evita que voltem.
4. Gente desenhada pelo próprio cenário (cama do `quarto_terra`, espelho, olho mágico) continua no traço antigo.
5. Pernas e braços ainda são traços de uma cor só (sem sombra nem dobra).
6. Ninguém viu um MP4 inteiro com voz: a conferência foi por folha de contato e por render sem voz. Vale o William assistir ao `t_s01` antes de usar num episódio de verdade.

## Para retomar
Leia `MOTOR_GUIA.md`. Suba o `Producao/serve.ps1`, rode `node linha_base.js conferir` antes e depois de qualquer mudança no `motor.js` ou no `motor_fx.js`.
