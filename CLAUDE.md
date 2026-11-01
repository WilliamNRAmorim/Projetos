# CLAUDE.md: repositório Projetos

Vale para todo o repositório (GMS, Conteudo_Bit e o resto). Cada projeto tem o seu CLAUDE.md com as regras próprias (ex.: `GMS/CLAUDE.md`); leia o da pasta onde for trabalhar. Plano de uso de modelos em `PLANO.md`.

## Modelo e roteamento
- O agente padrão da sessão é o `chefe` (Sonnet 5.5, esforço médio). Ele decide como dividir o time para gastar o mínimo de tokens; as regras de divisão estão em `.claude/agents/chefe.md`, que é a fonte única.
- Opus só dentro do `revisor` (regra de negócio, arquitetura, norma; no GMS, turno e cálculo de parada/setup) e do `produtor-de-artes` (toda imagem, áudio e vídeo). Revisão comum vai ao `revisor-leve` (Sonnet).
- O `financeiro` analisa o chefe uma vez por dia (22h) e grava lições em `.claude/orquestracao/licoes.md`. Mudança nas regras do chefe só com aprovação do William.
- Os subagentes ficam em `.claude/agents/` na raiz e valem em qualquer pasta do repositório.
- Publicar, agendar, enviar, curtir, comentar, seguir, comprar e apagar em definitivo pedem o "sim" do William a cada ação. Subagente nunca faz isso: devolve o arquivo ao chefe.

## Processo
- Mudança com mais de um arquivo começa com plano aprovado.
- Toda alteração: commit por assunto e push na main.
- Pode enviar dados de produção, SAP ou dados pessoais a serviços externos.
- Ao final: arquivos alterados, verificação, modelo usado em cada etapa e pendências.
