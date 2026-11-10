# Brief Fable: missões L e P2 (10/11/2026)

Fonte: `PLANO_FABLE.md`, seções 10.2 (P2), 10.6 e 10.7 (missão L). Quem escreveu: chefe (Sonnet). Quem executa: sessão Fable, esforço extra.

## Regras que valem para tudo
- Diagnóstico e proposta primeiro. Nenhuma mudança em produção (app em uso na fábrica, SharePoint, Power Automate, Copilot Studio, Power BI publicado) sem o "sim" do William e cópia de segurança.
- Não publicar, não enviar, não baixar nada da internet, não apagar em definitivo. Não clicar em Export nem em Save As sem o "sim" do William.
- Não editar nenhum arquivo de `.claude/agents/`, `CLAUDE.md` nem `settings.json`.
- Commit por marco, com mensagem por assunto, e push na `main` (autorização permanente do William). Listar o staged antes de cada commit; nunca `git add` de pasta sem checar `.env` e dados com token.
- Dado de produção, SAP e pessoal pode ficar no repositório (regra de 31/10).
- Regra de negócio (turno, parada/setup, OEE, norma) passa pelo `revisor` antes de virar entrega final. O chefe chama.
- Contexto da sessão abaixo de ~150k. Passou disso: commitar, escrever o estado em arquivo e parar.
- Não ler arquivo grande inteiro (diário, Mestre, xlsx): usar `gms.py`, trechos e `grep`.

## Missão L: revisão de layout e eficácia
Objetivo: diagnóstico de design e eficácia do que o supervisor usa.
1. **Power BI**: ler o projeto oficial `GMS/PowerBI/GMS_Painel.pbip` (e `GMS/PowerBI/GMS_Painel.Report`, `layout_salvo.json`, `GMS/PowerBI/gerar_relatorio.py`) e o `GMS/GMS_Mestre_BI.md`. Avaliar hierarquia, o que o supervisor vê em 5 s, cores, densidade, uso em tablet e celular. Não mexer no layout salvo (regra: layout do BI salvo é o vigente; mudança só com pedido).
2. **Power Apps**: avaliar `GMS/Telas/` como designer de app de chão de fábrica: tablet na linha, tamanho de alvo de toque, fluxo do apontamento, cliques até concluir, erro e feedback, desempenho. Regra: patch por bloco, nunca mexer em X/Y/Width/Height sem listar. Triagem de qualidade com `gms_qa_yaml.py`, se existir.
3. **Power Automate**: avaliar os 5 fluxos exportados em `C:\Users\U445131\AppData\Local\Temp\claude\9be407617cb2adde\8425b14e-b087-4fbb-9981-21fa6810c428\scratchpad\fluxos_20261110\` (definições em `Microsoft.Flow\flows\<id>\definition.json`) e a documentação em `Documentos_GMS/` e `GMS/Planejamento/`. Checar gatilhos, concorrência, paginação (lista de 5 000 itens), tratamento de erro, tempo de execução. Conferir a unidade da hora de parada do Monitor Solda Mandril (metros por hora ou por minuto?).
4. **Entrega**: diagnóstico com prioridade, proposta aplicável e mockup antes/depois (folha de imagem). Arquivo em `GMS/Auditoria_Fable/L_diagnostico.md`.

## Missão P2: gêmeo digital da célula GMS
Objetivo: simulador da célula (8 etapas, turnos, paradas, setup, refugo, headcount) calibrado com o histórico real, com backtest, para what-if de demanda x pessoas e sequenciamento.
- Dados: `GMS/IA/dados`, `Producao_GMS_x_MB51/dados`, `Dados_Historicos`, `dados_diarios.json`. Ler por `grep` e trechos.
- Calibrar com histórico. Backtest com dias já conferidos. Dizer o erro, não só o ajuste.
- Não validar DAX no Power BI daqui (não tem o modelo vivo; isso é do PC da fábrica).
- Regra de turno e de parada/setup: passar pelo `revisor` antes de dar a conta por certa.
- Entrega: código do simulador e relatório de backtest em `GMS/Simulador_Celula/`, com `LEIAME.md` de como rodar.

## Como terminar
- Arquivo de estado em `GMS/Auditoria_Fable/ESTADO_L_P2.md`: o que ficou pronto, o que falta, onde parou.
- Ao final, um resumo curto para o William: o que achou (top 5 de cada frente), o que precisa do "sim" dele e o que depende do PC da fábrica.
- Gasto: anotar `get_usage` antes e depois no `registro.md` (uma linha).
