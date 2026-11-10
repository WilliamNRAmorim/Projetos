# Estado das missões L e P2 (Fable)

Atualizado em 10/11/2026, ao fim da missão L.

## Missão L: pronta (diagnóstico e proposta)
- `L_diagnostico.md`: achados com prioridade, proposta, o que pede "sim" e o que depende do PC da fábrica.
- `L_mockup_antes_depois.png`: folha antes/depois (BI na mesa, BI no celular, linha de lance do app).
- `gerar_mockup_L.py`: gera a folha de novo.
- Nada foi alterado em produção, no layout salvo do BI, nas telas nem nos fluxos.

### O que falta na L
- Passar pelo `revisor` os itens marcados [revisor] no diagnóstico: B5 (`dTurno`), B6 (duas tabelas de Hora-Hora e filtro de Almoço), A4 (ordem dos `Patch` do Mandril) e 3.2 (duas fontes de velocidade, só a primeira OP em processo).
- Conferências no PC da fábrica (seção 6 do diagnóstico).
- Consultar o limite diário de ações do Power Automate para a licença do William (F6).
- Não rodei as skills `analyze-canvas-performance` e `canvas-apps-boas-praticas`; a parte de app usou script próprio e o `gms_qa_yaml.py`.

## Missão P2: não começou
- Entrega esperada: simulador e relatório de backtest em `GMS/Simulador_Celula/`, com `LEIAME.md`.
- Dados a usar: `GMS/IA/dados`, `Producao_GMS_x_MB51/dados`, `Dados_Historicos`, `dados_diarios.json` (por `grep` e trechos).
- Abrir em sessão nova: a sessão da L terminou com cerca de 230 mil tokens de contexto, acima dos 150 mil do brief.
- Regra de turno e de parada/setup passa pelo `revisor` antes de dar a conta por certa.

## Onde parou
- Commit da L na `main`.
- Próximo passo: o William lê o `L_diagnostico.md` e diz o que entra; depois, P2 em sessão nova.
