---
name: canvas-apps-boas-praticas
description: Boas práticas da Microsoft para Power Apps Canvas (Power Fx, controles, layout, comportamento, design, sintaxe do .pa.yaml e checklist de QA). Use ao escrever, revisar ou evoluir telas do GMS (GMS/Telas/*.txt), ao escolher controle ou padrão de fórmula, ou ao decidir como melhorar o app. Sem MCP: só leitura de referências.
user-invocable: true
---

# Boas práticas de Canvas Apps (referência Microsoft)

Obs.: ControlGuide, DesignGuide e QAChecks citam ferramentas MCP (`compile_canvas` etc.); ignore essas menções — aqui valida-se com `gms_qa_yaml.py`.

Conteúdo oficial do plugin `canvas-apps` (microsoft/power-platform-skills, MIT), copiado em
`.claude/plugins/canvas-apps/references/`. Não há servidor MCP neste projeto: leia os guias e aplique ao YAML local.

## Precedência (importante)
1. `GMS/CLAUDE.md` e `GMS/GMS_Mestre.md` (normas do William) **vencem** qualquer guia.
2. Os guias abaixo valem onde o Mestre é omisso. Em conflito, siga o Mestre e diga qual regra foi preterida.
3. Nunca altere tela sem aprovação do William; patch cirúrgico, QA com `gms_qa_yaml.py`, linha de diário.

## Quando ler cada guia
| Preciso de… | Leia |
|---|---|
| Fórmula, delegação, `With`, `Concurrent`, nomes de fórmula, erros | `PowerFxGuide.md` |
| Escolher/configurar controle, propriedades, enums | `ControlGuide.md` |
| Eventos (`OnSelect`, `OnVisible`, `OnStart`), variáveis, navegação, tratamento de erro | `BehaviorGuide.md` |
| Estrutura da tela, espaçamento, responsividade | `LayoutGuide.md`, `GridLayoutGuide.md` |
| Cores, tipografia, acessibilidade, consistência visual | `DesignGuide.md` |
| Sintaxe do YAML (indentação, `=`, strings, erros de parse) | `YamlSyntax.md` |
| Checklist antes de entregar | `QAChecks.md` |
| Planejar uma tela ou app novo | `PlanTemplates.md` |

## Auditoria de desempenho e qualidade
A skill `analyze-canvas-performance` (Microsoft Power CAT) audita o YAML: delegação, N+1, coleções
excessivas, `ForAll`, `OnStart` pesado, `Concurrent`, `DelayOutput`, tratamento de erro, nomes e acessibilidade.
Peça "analise a tela scr_X.txt" e ela gera um relatório priorizado, sem alterar nada até aprovação.

## Como evoluir o GMS
- Priorize pelo Mestre: confiabilidade do dado → esforço do operador → decisão da supervisão → estética.
- Meça antes de otimizar (auditoria acima) e registre achados em `GMS/Auditoria/NN_*.md`.
- Mudanças em lote só depois de aprovadas, tela a tela, com QA e diário.
