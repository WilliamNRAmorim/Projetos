# Simulador da célula de mangueiras (missão P2, 10/11/2026)

Diagnóstico e proposta. Lê só arquivos locais; não toca em app, SharePoint, fluxo nem BI.

## Como rodar
Na pasta `GMS/Simulador_Celula`, com Python 3.12, numpy, pandas e openpyxl (já instalados):

```
python simulador.py
```

Leva cerca de 10 s. Calibra, grava `parametros.json`, `BACKTEST.md` e `WHATIF_exemplo.md`.

What-if avulso (compara o cenário pedido com a base):

```
python simulador.py whatif --demanda 8000 --t3 trancagem,extracao --pessoas extracao=-1 --sem falta_tubo --trocas 0.5 --maquinas 7 --refugo 0.02
```

- `--t3`: etapas com 3º turno (`todas` vale para as 8). `--pessoas etapa=±n`: pessoas a mais ou a menos por turno sobre a referência.
- `--sem`: tira uma classe de parada da trançagem (`falta_tubo`, `falta_fio`, `manutencao`, `falta_operador`, `outras_paradas`, `zero_sem_motivo`).
- `--trocas`: multiplica a frequência de troca de mangueira (sequenciamento). `--maquinas`: teto de trançadeiras por turno.

Se as planilhas de Eficiência mudarem, rode antes `python extrair_eficiencia.py` (regrava `dados/*.csv`).

## O que o simulador faz
Anda de turno em turno pelas 8 etapas (mandril, tubo, trançagem, cobertura, bandagem, vulcanização, debandagem, extração/teste), com estoque entre elas, e repete 300 vezes com sorteios do histórico.
- **Trançagem, por máquina e turno**: metros = horas disponíveis × velocidade cadastrada da mangueira × desempenho sorteado do histórico da própria máquina. Turno com troca de mangueira sorteia do histórico de turnos com troca.
- **Demais etapas**: capacidade do turno sorteada do real histórico daquele turno; a saída é o menor entre capacidade e estoque de entrada. Mandril e tubo são puxados: param quando o estoque à frente enche.
- **Refugo**: a perda entre etapas já está no fator de passagem; `--refugo` reescala a saída boa da extração.

## Regra de turno, parada e setup usada (PENDENTE de `revisor`)
1. Dia produtivo começa 05:20. T1 05:20–13:57 (517 min), T2 13:57–22:20 (503 min), T3 22:20–05:20 (420 min). Hora extra do T2 até 23:20 não entra como tempo regular.
2. Tempo disponível = duração menos 45 min de pausa por turno: 472, 458 e 375 min (1.305 por dia, regra do BI desde 09/11). A planilha de Eficiência usa 7,38 h, 7,33 h e 6,55 h (1.275,6 min); a diferença de 2,3% fica dentro do desempenho calibrado.
3. Parada real e ritmo não se somam: cada turno de máquina cai em uma classe só. Com motivo de parada na planilha, a perda é parada daquela classe. Sem motivo, a diferença para a velocidade cadastrada é ritmo (tempo excedido), não parada.
4. Setup: a planilha não tem hora de peça. Proxy: turno em que a mangueira da máquina é diferente da do turno planejado anterior, ou motivo "set-up/troca". Parada com motivo próprio num turno de troca fica na classe da parada, não em setup. Troca de OP com a mesma mangueira não aparece.
5. Nas demais etapas a planilha não separa parada de ritmo; o simulador só fala em capacidade.

Divergência a decidir pelo `revisor`: item 2 (qual hora disponível vale) e item 4 (proxy de setup por turno em vez do intervalo entre última e primeira peça boa).

## De onde veio cada parâmetro
| Parâmetro | Origem |
|---|---|
| Real por etapa e turno; trançadeira por máquina (mangueira, velocidade, real, motivo) | Histórico: planilhas de Eficiência, 01/04 a 04/11/2026, 148 dias com produção |
| Desempenho, classes de parada, perda por classe, setup | Histórico (treino: 01/04 a 31/08) |
| Fator de passagem entre etapas (`f`) | Histórico (treino): razão dos metros de etapas vizinhas |
| Escala de capacidade (`k`) | Calibrada por simulação só com o treino, até zerar o viés |
| Vulcanização (capacidade e real) | Histórico da ficha de produção (até 06/10); lote acima de 3.000 m descartado |
| Refugo 0,79% | Histórico do GMS, abr–ago: 5.034 m de refugo em 634.516 m (TiposErros sem duplicata + inspeção). Não é número de SAP |
| Pessoas de referência por etapa e turno | **Provisório**: mediana de operadores distintos que apontaram na ficha |
| Turno trabalhado por etapa | **Suposição**: turno com real > 0 na planilha (não há escala real; a coluna planejado vem preenchida até em dia sem produção) |
| Efeito de pessoas | **Suposição**: linear abaixo da referência; acima, ganho só em mandril, bandagem, debandagem e extração, até 1,5× |
| Estoque máximo de tubo e de mandril, estoque inicial | **Suposição**: 1,5 dia e 1 dia de fluxo; começa com meio dia |
| Fluxo no mesmo turno | **Suposição**: o que uma etapa produz já serve à seguinte no mesmo turno |
| Falta de tubo | Entra como parada histórica da trançadeira, não pelo estoque simulado (o estoque real é por bitola) |

## Limites conhecidos
- O calendário de turnos entra como dado. Isso ajuda o simulador contra a mediana ingênua, que não conhece o calendário.
- Faixa p10–p90 estreita na trançagem (o real cai dentro em 55% dos dias de teste): os sorteios por máquina são independentes e o dia ruim costuma ser comum a várias.
- Sem mix por bitola nas etapas de linha. Sequenciamento só enxerga troca de mangueira na trançadeira.
- `COMO_USAR_OS_DADOS.md` não está em `GMS/Analises/Refugo_por_Material/`; usei as regras resumidas em `GMS/IA/dados/mapa_dados.md`.
- O simulador anterior (`GMS/Analises/Fluxo_Trancadeira_Cabine`) fica como está; este não o substitui no BI.
