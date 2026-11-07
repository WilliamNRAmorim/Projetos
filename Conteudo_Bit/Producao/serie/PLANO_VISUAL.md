# Plano: subir o visual do motor das histórias (07/11/2026)

Situação de partida: nota 7/10 (produção 9, áudio 8, visual 6, código 5).
Objetivo: melhorar o visual sem mudar nenhum episódio já publicado e com prova em cada fase.
Status: **aguardando aprovação do William.**

## Regras de todas as fases
- Todo recurso novo é uma opção no JSON, desligada por padrão (`"visual": {...}` no episódio ou na cena).
- Antes da Fase 1, salvar o hash dos quadros dos episódios publicados (c01–c28, s01–s28, o25–o28). Ao fim de cada fase o hash precisa continuar igual.
- Cada fase termina com uma folha de contato antes/depois de um episódio de teste (base: c04 e um episódio da saga). Só começa a próxima fase depois do ok do William.
- Mudança de render passa pelo `revisor-leve`. Commit por assunto e push na main.

## Fases (da que rende mais por custo para a que rende menos)
| # | Fase | O que muda | Quem | Esforço |
|---|---|---|---|---|
| 0 | Linha de base | Hash dos quadros publicados e folha "antes" | executor (Sonnet) | P |
| 1 | Atmosfera | Vinheta, grão animado, neblina, poeira e luz que pisca (vela, lanterna, lâmpada). Textura gerada uma vez e reaproveitada, para não pesar no render | executor + revisor-leve | P/M |
| 2 | Personagens em vetor | Olho com brilho, sobrancelha, boca por pose, silhueta de cabelo e roupa, sombra no chão | executor + revisor-leve | M |
| 3 | Composição | Metade de baixo ocupada (chão, primeiro plano, sombra projetada), close, plongée, contraplongée e legenda que se adapta | executor | M |
| 4 | Movimento | Piscar, respirar, virar a cabeça, olhar que muda, sombra que anda | executor + revisor-leve | M |
| 5 | Cenários em PNG | Só os cenários de maior impacto, gerados num único lote no Gemini com estilo fixo (o motor já aceita `NOME.png`) | produtor-de-artes (Opus), 1 chamada | G |
| 6 | Código | Dividir o motor.js em módulos (cenário, pose, efeito, render), juntar os contos*.js num único registro e tirar os scripts de build de preview/ | executor + revisor-leve | M/G |
| 7 | Limpeza | 37 pastas preview/edgeprof-* movidas para _arquivo e apagadas só com o "sim" | chefe | P |

Ajuste do chefe ao plano do planejador: personagens subiram para a Fase 2 porque são o ponto mais fraco do visual. Código ficou para o fim, para não reorganizar um motor que ainda está mudando.

## Decisões do William (a recomendação vem primeiro)
1. Personagens: **vetor melhorado** ou PNG gerado. O vetor sai mais barato e fica igual em todos os episódios.
2. Estilo: **flat com atmosfera (grão, vinheta, luz)** ou traço pesado com hachura.
3. Pastas edgeprof-*: **mover para _arquivo e apagar depois de conferir** ou apagar já.

## Riscos
- Grão e neblina calculados a cada quadro podem deixar o render lento. Medir o tempo no episódio de teste.
- A vinheta pode tirar contraste da legenda. Conferir com `&safe=1`.
- Uma opção mal desligada pode mudar um episódio antigo. O hash da Fase 0 pega isso.
- Um PNG gerado pode mudar de cara de uma cena para outra. Conferir a folha antes de usar.
