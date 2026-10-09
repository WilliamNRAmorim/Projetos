# Post de LinkedIn: IA perto de dado de fábrica (impessoal)

Rascunho para aprovação (versão em texto corrido). Não publicado nem agendado. Sem primeira pessoa e sem citar o GMS, a Danfoss ou o uso de IA pelo autor.

## Texto

Quando a IA chega perto do chão de fábrica, o risco não está no código que ela escreve. Está nos dados que ela enxerga.

Uma planta gera informação que não pertence a quem desenvolve: ordens de produção, códigos do SAP, nomes de operadores, tempos de parada. Nada disso deveria sair da empresa para virar contexto de um serviço externo, nem por conveniência, nem por pressa. Se a ferramenta precisa de um exemplo, o exemplo é inventado, com a mesma forma do real.

O segundo ponto é o que o agente consegue fazer. Ele herda as permissões de quem o roda: se o seu usuário alcança uma pasta ou um sistema, ele também alcança. Dar só o que a tarefa precisa é a medida de segurança mais barata que existe.

O terceiro é como tratar o que ele entrega. Agentes erram de forma plausível: a resposta sai fluente, confiante e errada, e nenhum alerta toca.

No chão de fábrica, isso é um registro que parece certo e não está. Por isso resposta de IA é candidata, não prova, e o que fecha a tarefa é uma validação que não depende da IA.

Nada disso é desconfiar da tecnologia. É decidir antes o que ela pode ver, o que ela pode fazer e quem confere.

#EngenhariaDeComputação #Indústria40 #SegurançaDaInformação #InteligênciaArtificial #Manufatura
## Fatos e origem
| Afirmação | Origem |
|---|---|
| Dado de produção, SAP e pessoal não vão a serviço externo | Regra do `CLAUDE.md` do repositório (prática do William), escrita como regra geral |
| O agente herda as permissões de quem o roda | Fato geral do Claude Code (Bash roda sob o usuário); debatido em post de Dug Falby no LinkedIn, 06/10/2026 |
| "Agentes falham de forma plausível" | Ideia de Arun Thachi (LinkedIn, out/2026), reescrita com outras palavras; não citada |
| Validação independente da IA fecha a tarefa | Tese de Chris Pietschmann (LinkedIn, set/2026), reescrita; não citada |

## Para o William decidir
- O post não diz que você usa IA, mas implica que você pensa no assunto.
- Confirmar que citar "SAP" e "ordens de produção" como exemplos genéricos é aceitável na empresa.
- Hashtag de segurança pode atrair público fora do seu (TI/segurança). Opcional.
