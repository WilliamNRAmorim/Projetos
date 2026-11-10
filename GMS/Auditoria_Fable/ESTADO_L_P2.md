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

## Missão P2: simulador pronto, regra ainda sem `revisor` (10/11/2026)
Pasta `GMS/Simulador_Celula/`. Roda com `python simulador.py` (cerca de 10 s).
- `simulador.py`: calibração, simulação por turno das 8 etapas, backtest e what-if. `extrair_eficiencia.py`: lê as planilhas de Eficiência para `dados/*.csv`.
- `BACKTEST.md`: treino 01/04 a 31/08 (99 dias), teste 01/09 a 04/11 (49 dias). No teste, extração: WAPE 14,8% por dia, MAPE semanal 12,3%, viés +3,2%. Por etapa, WAPE de 14,4% a 16,4%. Soma das 7 etapas da planilha: WAPE 8,4%.
- `WHATIF_exemplo.md`: demanda de 8.000 m/dia contra turnos, pessoas, paradas e trocas.
- `LEIAME.md`: como rodar, regra de turno/parada/setup usada, origem de cada parâmetro e suposições.

### O que falta na P2
- **Passar pelo `revisor` a regra de turno, parada e setup** (seção própria do `LEIAME.md`). Não foi chamado: a sessão passou do teto de contexto do brief (150 mil; chegou a cerca de 200 mil) e parou. Até lá, a conta não está dada por certa.
- Escala real de pessoas por etapa e turno (hoje: quem apontou na ficha) e calendário real de turnos (hoje: turno com real > 0).
- Ler da planilha o estoque real (Tubo das Trançadeiras, Próxima Extração, Bandado) para iniciar e conferir o estoque simulado.
- Abas de janeiro a março têm outro layout e ficaram de fora.
- Ficha de produção depois de 06/10 (vulcanização só tem real até essa data).

## Onde parou
- L e P2 commitadas na `main`.
- Próximo passo: `revisor` na regra do simulador, em sessão nova e curta; o William lê `L_diagnostico.md`, `BACKTEST.md` e `WHATIF_exemplo.md` e diz o que entra.
