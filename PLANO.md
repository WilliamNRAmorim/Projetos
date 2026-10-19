# PLANO: uso de modelos no GMS

## 0. Limites
- Não enviar dados de produção, SAP ou dados pessoais ao agente.
- Não instalar skills ou roteadores de terceiros sem ler e aprovar.
- Normas (`GMS_Mestre.md`, `GMS_Mestre_BI.md`) não mudam sem pedido explícito.
- `GMS_Diario.md` é somente append.
- `gms.py` deriva backlog e estado. Não editar os dados derivados à mão.

## 1. Teste dos modelos (antes de tudo)
1.1 Criar `.claude/agents/teste-modelo.md` com `model: claude-haiku-5-5` e tarefa trivial (listar arquivos). Conferir no histórico qual modelo rodou.
1.2 Repetir com `claude-sonnet-5-5`.
1.3 Apagar o arquivo de teste.
Concluído quando: os dois IDs confirmados. Se o Claude Code não aceitar o formato, parar e reportar.

## 2. Linha de base (5 dias úteis)
2.1 Por sessão: tipo de tarefa (exploração, implementação, planejamento, revisão, depuração), modelo, subagentes usados, tempo até entrega e número de correções.
2.2 Ao final de cada dia, rodar `/usage` e anotar o consumo. Conferência extra: `python Ferramentas/token_audit.py --project Projetos --days 7` (copiado de bryanvine/token-saver, lido e sem rede; preços fixos no código, valor é estimativa; pode não contar transcrições de subagentes, confirmar antes de usar na etapa 3).
Concluído quando: pelo menos 15 sessões registradas.

## 3. Comparação com e sem subagentes
3.1 Em metade das sessões, usar subagentes conforme o CLAUDE.md. Na outra metade, trabalhar só na sessão principal.
3.2 Comparar custo médio, tempo e correções por tipo de tarefa.
3.3 Decisão por tipo de tarefa:
- Subagente reduziu custo sem mais correções: manter.
- Subagente aumentou custo: remover daquele tipo de tarefa.
- Revisor (Opus): manter só se evitou erros reais em turno, parada ou norma.

## 4. Verificação
- Teste verde não prova correção. Conferir a intenção.
- Revisão humana obrigatória para: cálculos de parada, OEE e produtividade; regras de turno; o que vai para tablet na linha; mudanças em normas.
- Medidas DAX validadas contra um dia de produção já conferido à mão.

## 5. Não fazer
- Não usar Opus como sessão principal.
- Não deixar a IA decidir turno ou cálculo de parada sem revisão humana.
- Não tratar relatos de economia como garantia.
