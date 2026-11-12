# Estado da missão P2: gêmeo digital da célula GMS

Atualizado em 12/11/2026 (madrugada). **Missão pausada no marco 1**, pela regra do contexto (sessão passou de 150k tokens) e porque a janela de 5 horas chegou a 78%.

Barra no início: geral 84%, Fable 62%, janela de 5 h 53%. Na pausa: geral 87%, Fable 69%, janela de 5 h 78%.

## Feito (marco 1, commitado)
- `gemeo/gemeo.py`: motor de eventos discretos, OP a OP, pelas 8 etapas (Mandril a Extração/Teste), com turnos da NORMA de 27/10 (MEL-250), fila, servidores por turno, retomada na virada, posições por trançadeira, setup da Trançagem em 3 níveis, rendimento de metros por etapa e leitura do Hora-Hora antigo para o mix de paradas.
- `gemeo/gemeo_backtest.py`: calibra no treino (01/03 a 12/08/2026), mede no teste (13/08 a 05/10/2026), grava `gemeo/gemeo_parametros.json`, `gemeo/saida/backtest_diario.csv`, `gemeo/saida/backtest_resumo.csv` e `GEMEO_BACKTEST.md`.
- Rodar: `python -X utf8 gemeo_backtest.py` dentro de `gemeo/` (cerca de 1 minuto).

## O que o backtest mostrou (teste, fora da amostra)
- Lead time da liberação ao fim da Extração: real 56 h, gêmeo 57 h (mediana).
- Erro semanal (MAPE) por etapa: Tubo 11,7%; Trançagem 14,2%; Cobertura 10,3%; Bandagem 10,3%; Vulcanização 10,6%; Debandagem 13,6%; Extração 12,5%.
- Erro diário (WAPE): Trançagem 29,2%; Cobertura 17,0%; Bandagem 19,2%; Vulcanização 18,0%; Debandagem 21,6%; Extração 21,9%.
- **A mediana fixa de metros por dia ainda erra menos que o gêmeo** no diário (Extração 14,1%) e no semanal (11,0%). O gêmeo ganha com folga do modelo "só desloca" (37,2% no diário da Extração). Ou seja: para prever um dia comum de um período estável, a média basta; o gêmeo serve para o "e se" (mudar pessoas, demanda, sequência), que a média não responde.
- O `kappa` da Trançagem ficou em 1,75 e o do Mandril em 0,5, as bordas da grade: sinal de ajuste frágil nessas duas etapas.

## Falta (nesta ordem)
1. **What-if de demanda × pessoas** (`gemeo/gemeo_whatif.py`): gerar OPs pelo mix dos últimos 90 dias, equipe por etapa e turno, 6 semanas com 2 de aquecimento; saída por cenário (atendimento, gargalo, ocupação, fila, lead time) em `gemeo/saida/whatif_*.csv`; conta inversa (pessoas para a demanda). Na Trançagem, máquinas rodando = mín(posições, pessoas × `tranc_maq_por_pessoa`, hoje 3,0).
2. **APS simples** (`gemeo/gemeo_aps.py`): mesma carteira de uma semana real, comparar ordem de chegada × agrupar por mangueira e bitola × menor lote primeiro; `simular()` já aceita `pri` (prioridade por OP na Trançagem).
3. **Power BI**: tabelas `tGemeoBacktest`, `tGemeoCenario`, `tGemeoEtapa`, `tGemeoAPS` em TMDL (ver o padrão dos `PowerBI/modelo/*.tmdl.md`) lendo os CSV de `gemeo/saida/`, com medidas DAX documentadas; atualizar `DAX_simulador.md`. Nada é publicado daqui.
4. **Revisor (Opus, só leitura)** sobre turno e parada/setup: `SLOT_INI`, `SLOT_MIN`, `turno_de`, `trabalho`, `slots_reais`, o setup de `calibrar` e `paradas_hh` em `gemeo/gemeo.py`.
5. **Relatório de erro** (`GEMEO_ONDE_NAO_CONFIAR.md`), **roteiro do PC da fábrica** (`ROTEIRO_PC_FABRICA_GEMEO.md`) e auto-ataque (caso extremo: zero pessoas, demanda zero, uma máquina só, OP sem trançadeira; regressão do backtest).
6. Linha final no diário e no `registro.md`.

## Para o William conferir (regra de negócio)
- **Turno:** o gêmeo usa 05:20 / 13:57 / 22:20 (517, 503 e 420 min). Hora extra do 2º turno até 23:20 cai no 3º turno. Refeição de 45 min não é descontada à parte: está dentro da taxa medida.
- **Setup da Trançagem:** medido por apontamento (fim de um lote ao início do seguinte na mesma máquina, só quando o seguinte já estava pronto no Tubo): 22 min na mesma mangueira, 120 min trocando mangueira na mesma bitola, 547 min trocando bitola. A regra do GMS é última peça boa à primeira peça boa, nunca por clique; então este número é provisório.
- **Paradas:** não entram dia a dia, porque o Hora-Hora da era GMS não está neste PC. O Hora-Hora antigo (08/2023 a 07/2026) dá parado = 41% dos minutos das janelas registradas; se a planilha antiga só tem janela com parada, esse número superestima. Motivos: Falta de tubo 18%, Set-up 13%, Falta de fio 12%, Alimentação de fio 12%.
- **Pessoas:** continuam sendo "quem apontou", não a escala real. `escala_real.csv` ainda falta.
- **Posições por trançadeira:** 19% dos lotes seguidos na mesma máquina se sobrepõem no apontamento; o gêmeo aceita 2 lotes simultâneos na maioria das máquinas e 3 na TH07 e na TO04. Confirmar se isso existe na prática ou se é atraso de apontamento.
- **Rendimento Mandril → Tubo de 0,87:** parece diferença de unidade ou de cadastro, não refugo. Conferir.
- **Não modelado:** Extrusora, Bobinadeira e Catenária (sem dado local); falta de fio e de tubo aparecem só como motivo de parada.
