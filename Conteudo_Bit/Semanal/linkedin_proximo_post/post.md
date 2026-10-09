# Post de LinkedIn (só texto): método do GMS (Gemba walk + RAD)

Escrito pelo Din em 08/10/2026 a partir do `brief.md`. Rascunho para aprovação. Não publicado nem agendado.

## Texto final

Eu não escrevia a primeira tela do GMS antes de ver a ficha de papel sendo usada na estação.

Essa decisão não aparece no código, mas define como o sistema foi construído.

O GMS é um MES (sistema de execução da manufatura) feito 100% em low-code, e é o estudo de caso do meu TCC em Engenharia de Computação. A construção começou com um Gemba walk: duas semanas observando a célula nos três turnos. Gemba é o termo japonês para o lugar onde o trabalho realmente acontece, e a caminhada serve para ver esse lugar antes de decidir qualquer coisa.

Depois veio o desenvolvimento em RAD (desenvolvimento rápido de aplicações), com um ciclo diário. De manhã eu observava na estação. À tarde, desenvolvia. A versão nova entrava no turno seguinte.

Com esse ritmo, o problema aparecia cedo, não no fim do projeto.

A ficha de papel tinha 8 etapas, e a informação chegava com 1 a 2 dias de atraso. O desenvolvimento levou 2 meses e a implantação, 7: 9 meses no total.

O requisito estava na estação. Minha parte foi chegar lá antes de abrir o editor.

#EngenhariaDeComputação #Manufatura #LowCode #Indústria40

## Variante de gancho (trocar só as duas primeiras linhas)

Passei duas semanas observando a estação nos três turnos antes de abrir o Power Apps.

Esse método não aparece no código, mas define a ordem em que o sistema foi construído.

## Fatos usados e fonte

| # | Fato no texto | Fonte | Situação |
|---|---|---|---|
| 1 | GMS é um MES feito 100% em low-code, estudo de caso do TCC em Engenharia de Computação | `GMS/TCC_resumo.md` (O que é) | Confirmado |
| 2 | Ficha de papel com 8 etapas; informação chegava com 1 a 2 dias de atraso | `GMS/TCC_resumo.md` (Problema) | Confirmado |
| 3 | Gemba walk de 2 semanas nos 3 turnos, antes do desenvolvimento | `GMS/TCC_resumo.md` (Método) | Confirmado no resumo. A ordem "antes de qualquer tela" é leitura do resumo; confirmar no TCC completo |
| 4 | Gemba é o termo japonês para o lugar onde o trabalho realmente acontece | [Lean Enterprise Institute, lexicon Gemba](https://www.lean.org/lexicon-terms/gemba/) (LEI traduz como "actual place"; o texto usa "lugar onde o trabalho realmente acontece") | Conferido por WebSearch em 08/10/2026 |
| 5 | RAD = desenvolvimento rápido de aplicações | [Computer Weekly, definição de RAD](https://www.computerweekly.com/de/definition/Rapid-Application-Development-RAD) | Conferido por WebSearch em 08/10/2026. Sem James Martin: o TCC_resumo não cita e o texto não cita |
| 6 | RAD com ciclo diário: de manhã na estação, à tarde desenvolvendo, versão nova no turno seguinte | `GMS/TCC_resumo.md` (Método) | Confirmado |
| 7 | Desenvolvimento 2 meses, implantação 7, 9 no total | `GMS/TCC_resumo.md` (Linha do tempo; fonte oficial é o TCC) | Confirmado. Não há "8 meses" |
| 8 | "Com esse ritmo, o problema aparecia cedo, não no fim do projeto" | Inferência do ciclo diário em `GMS/TCC_resumo.md` (Método) | Leitura do ciclo, não dado. Confirmar com o William |
| 9 | "Eu não escrevia a primeira tela antes de ver a ficha de papel sendo usada na estação" (gancho) | Não está no TCC_resumo. Deriva do Gemba walk e da ficha física (itens 2 e 3) | **Precisa de confirmação do William** (é relato de bastidor pessoal) |

Ficou de fora de propósito: nomes (empresa, orientador, colegas), números da empresa (produção, refugo, OEE, kg de papel), operadores, cenas, bugs, métricas de cada ciclo, Will Station, Atkin et al., "adoção" como lição, a frase "Não criamos o dado. Zeramos o custo de acessá-lo", a lista do MESA-11 e "low-code por restrição" como tese.

## Pendências antes de aprovar

- William confirmar o gancho (item 9) e a inferência do item 8.
- Confirmar no TCC completo a ordem Gemba antes do desenvolvimento (item 3).
- Escolher entre o gancho principal e a variante.
- Ângulo "método" contra o que já saiu no perfil pessoal (MESA-11 de 07/10; "low-code por restrição" em `Videos/Publicar/posts_prontos.md`): não repete, mas William confirma.
- Data: terça ou quarta, 8h–10h, para a semana seguinte, conforme a rotina.
