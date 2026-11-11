# 12 · Diagnóstico de 10/11/2026 e simulador da célula

Fonte: GMS/Auditoria_Fable/L_diagnostico.md e GMS/Simulador_Celula/LEIAME.md, os dois de 10/11/2026. São diagnóstico e proposta: nada aqui foi aplicado em produção. "Medido" quer dizer que saiu de script sobre os arquivos do repositório; o que depende do PC da fábrica está marcado.

## 1. Power BI: 5 achados

Arquivo GMS_Painel: 10 páginas, 166 visuais.

1. A Visão Geral não diz se o dia está bom ou ruim: 6 cartões da mesma cor, sem meta, com variação só contra o mês anterior.
2. A cor padrão de série é o vermelho da marca; só 6 dos 30 gráficos têm cor própria. A norma B.6.1 proíbe.
3. Nenhuma das 10 páginas tem layout para celular.
4. Texto pequeno: 123 ocorrências de 9 pt e 7 de 8 pt.
5. Segmentação de Turno e de Período muda de lugar, de tipo e de tabela conforme a página (5 colunas de turno em 5 tabelas, 4 grupos de sincronização). O turno escolhido numa página não segue para a outra.

Risco a conferir no PC da fábrica: Visão Geral e Paradas usam a tabela Hora-Hora com filtro escondido de almoço; a página Hora-Hora usa a fHoraHora e trata refeição na medida. O "Tempo Parado" de uma pode não bater com o "Parado (min)" da outra no mesmo dia.

O que já está bom: toda página mostra "Dado atualizado até"; a página Hora-Hora Trançagem é a melhor do arquivo.

## 2. Power Apps: 5 achados

30 telas, 3.159 controles.

1. Ações em ícone de 24 × 24 px com 6 px de vão (editar e excluir lance, imprimir, dividir pallet na Finalização).
2. Texto de apoio em 11 e corpo em 13; rótulo cinza com contraste 2,6:1 em 584 usos (a norma pede 4,5:1).
3. App.OnError vazio: erro não tratado aparece ao operador como faixa técnica.
4. Gravação com 5 a 7 Patch em sequência no mesmo botão (Mandril). Se a rede cair no meio, a ficha fica meio gravada.
5. Lista de cerca de 70 mangueiras e 11 trançadeiras escrita à mão no OnStart: mangueira nova exige publicar o app.

O que já está bom: botões principais com 48 e 56 px; trava contra toque duplo (varProcessando); confirmação antes de excluir lance; conferência de erro depois do Patch.

## 3. Power Automate: 5 achados e uma data

5 fluxos: GMS_AutoResfriamentoVulca (a cada 5 min), GMS_Conferencia_Diaria (terça a sábado, 8h), GMS_PlanoOPs_Sync (arquivo alterado), GMS_Tempos_Sync (arquivo alterado), Monitor Solda Mandril (a cada 10 min).

1. **GMS_PlanoOPs_Sync para em 01/01/2027 sem avisar:** o gatilho olha a pasta "Plano Trançadeira/2026", escrita à mão. O plano de 2027 vai para outra pasta e o gatilho nunca dispara. Também só aceita arquivo com o prefixo do mês corrente. Proposta: gatilho na pasta mãe com subpastas e condição que aceite o mês corrente e o seguinte.
2. Monitor Solda Mandril lê DM_Velocidade sem Top Count: vêm só as 100 primeiras linhas. Combinação que ficar de fora sai com velocidade 0 e a máquina nunca aparece como crítica.
3. PlanoOPs_Sync e Tempos_Sync leem a lista de destino com Top 5000 sem paginação: acima disso o sincronismo cria duplicata.
4. Monitor Solda Mandril e AutoResfriamentoVulca não avisam quando falham; a tela do Monitor não mostra a idade do dado.
5. Conferencia_Diaria manda o e-mail de falha, mas a execução termina verde no histórico. Os e-mails de falha vão só para o William.

O Monitor trata a velocidade como metros por hora: hora da parada = agora + (material ÷ velocidade) × 3.600 s.

Ordem sugerida no diagnóstico: PlanoOPs_Sync (antes de 01/01/2027), Top Count e paginação, tema do BI, alvos de 48 px, App.OnError, aviso de falha.

## 4. Simulador da célula: o que faz

- Pasta GMS/Simulador_Celula. Lê só arquivos locais. Roda `python simulador.py` em cerca de 10 s.
- Anda de turno em turno pelas 8 etapas, com estoque entre elas, e repete 300 vezes com sorteios do histórico.
- Trançagem, por máquina e turno: metros = horas disponíveis × velocidade cadastrada da mangueira × desempenho sorteado do histórico da própria máquina.
- Demais etapas: capacidade do turno sorteada do real histórico; a saída é o menor entre capacidade e estoque de entrada. Mandril e Tubo param quando o estoque à frente enche.
- What-if: demanda, etapas com 3º turno, pessoas a mais ou a menos, tirar uma classe de parada (falta de tubo, falta de fio, manutenção, falta de operador), frequência de troca, número de máquinas, refugo.
- Histórico usado: planilhas de Eficiência de 01/04 a 04/11/2026, 148 dias com produção. Treino de 01/04 a 31/08.

## 5. Simulador: regra usada e limites

Regra do simulador, **não norma do GMS**. No LEIAME ela está marcada como pendente de revisão.

- Dia produtivo 05:20. Turnos de 517, 503 e 420 min. Tempo disponível = duração menos 45 min de pausa: 472, 458 e 375 min (1.305 no dia). A planilha de Eficiência usa 7,38 h, 7,33 h e 6,55 h (1.275,6 min); a diferença de 2,3% fica dentro do desempenho calibrado.
- Parada e ritmo não se somam: cada turno de máquina cai numa classe só. Com motivo de parada, a perda é parada daquela classe. Sem motivo, a diferença para a velocidade cadastrada é ritmo.
- Setup por aproximação: turno em que a mangueira da máquina é diferente da do turno planejado anterior, ou motivo "set-up/troca". Não é a definição da norma (intervalo entre peças boas), porque a planilha não tem hora de peça.

Limites que mudam a leitura do resultado:

- Pessoas de referência por etapa: provisório (mediana de operadores que apontaram).
- Turno trabalhado por etapa, efeito de pessoas, estoque máximo e fluxo no mesmo turno: suposições.
- Falta de tubo entra como parada histórica da trançadeira, não pelo estoque simulado.
- A faixa p10 a p90 da trançagem é estreita: o real cai dentro em 55% dos dias de teste.
- Sem mix por bitola nas etapas de linha.
- Refugo de 0,79% é do GMS (abril a agosto), não do SAP.

O Uiu não roda o simulador. Ele explica o que o simulador faz e seus limites, e diz que o cenário é rodado pelo William no repositório.
