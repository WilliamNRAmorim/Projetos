# CLAUDE.md: repositório Projetos

Vale para todo o repositório (GMS, Conteudo_Bit e o resto). Cada projeto tem o seu CLAUDE.md com as regras próprias (ex.: `GMS/CLAUDE.md`); leia o da pasta onde for trabalhar. Plano de uso de modelos em `PLANO.md`.

## Modelo e roteamento
- A sessão principal roda em Sonnet 5.5. Opus só dentro do `revisor` e do `produtor-de-artes`.
- Pedido simples, pergunta ou ajuste pequeno: fazer direto na sessão principal, sem subagente.
- Busca e leitura em muitos arquivos: `explorador` (Haiku). Só leitura.
- Tarefa com vários passos: `planejador` (Haiku) primeiro; depois `executor` (Sonnet 5.5).
- Toda peça de imagem, áudio ou vídeo (capa, carrossel, narração, render): `produtor-de-artes` (Opus 5.5, esforço médio). Os agentes de texto só entregam roteiro e legenda.
- Mudança em regra de negócio, arquitetura ou norma: `revisor` (Opus 5.5) antes de aplicar. No GMS isso inclui turno e cálculo de parada/setup.
- Os subagentes ficam em `.claude/agents/` na raiz e valem em qualquer pasta do repositório.

## Processo
- Mudança com mais de um arquivo começa com plano aprovado.
- Toda alteração: commit por assunto e push na main.
- Não enviar dados de produção, SAP ou dados pessoais a serviços externos.
- Ao final: arquivos alterados, verificação, modelo usado em cada etapa e pendências.
