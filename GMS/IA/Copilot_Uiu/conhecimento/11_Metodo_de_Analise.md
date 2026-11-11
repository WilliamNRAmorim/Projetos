# 11 · Método de análise do Uiu

Escrito em 10/11/2026. É o jeito de trabalhar que as instruções do Uiu resumem. Não tem regra de negócio nova: as regras estão em 10_Processos_e_Relacoes.md e nas normas.

## 1. Os sete passos

1. **Classificar a pergunta.** Fato de uma OP, estado atual, total ou ranking, diagnóstico (por quê), conceito ou cruzamento entre áreas. O tipo decide a fonte e o cuidado.
2. **Fixar o recorte.** Período em dia produtivo (05:20 a 05:20), etapa, máquina, mangueira, turno e unidade. "Ontem" é o dia produtivo de ontem. Sem período na pergunta, assuma o mais provável e diga qual foi.
3. **Ler a regra antes do dado.** KPI, turno, parada, meta e nome de coluna têm definição escrita. Leia primeiro.
4. **Escolher fontes e chave.** Diga a si mesmo qual lista responde e por qual coluna ela se liga às outras. Declare o grão: uma linha é uma ficha, um evento, uma janela ou uma inspeção.
5. **Consultar e provar a cobertura.** Compare as linhas devolvidas com o limite pedido. Bateu no limite, faltou dado: parta o período. Some só depois.
6. **Criticar o resultado.** Ordem de grandeza, unidade, denominador, repetição, valor de preenchimento, período com regra antiga. Uma conta que surpreende merece um segundo caminho de cálculo.
7. **Responder com fonte.** Número, evidência, leitura e a linha de fonte, período, linhas lidas e cobertura.

## 2. Roteiros prontos

**A produção caiu. Por quê?**
1. Caiu contra o quê: meta, dia anterior ou média? Em metros ou em aderência?
2. Tempo: houve menos turnos, menos máquinas rodando, feriado?
3. Parada e pausa: minutos por motivo, pausa programada separada.
4. Ritmo: janelas com produção abaixo da meta sem motivo.
5. Mix: a mangueira do dia tem velocidade teórica menor? Houve mais trocas?
6. Material: fila vazia antes da etapa (falta de tubo, de fio)?
7. Diga qual parcela explica mais e qual é só hipótese.

**O refugo subiu. Por quê?**
1. Subiu em metros ou em %? O denominador é do mesmo recorte?
2. Qual código de erro puxou a alta?
3. Em quais OPs? Elas têm máquina, lote de composto, lote de fio, operador ou turno em comum?
4. A etapa suspeita rodou quando? Compare com a data do refugo.
5. Há linha repetida na TiposErros inflando o número?

**Qual é o gargalo?**
1. OPs em processo e aguardando por etapa (foto de agora).
2. Idade da OP mais velha em cada etapa. OP zumbi fora da conta.
3. Vazão recente da etapa. Fila grande com vazão alta não é gargalo.
4. Fila não é parada de máquina.

**O número não bate com o painel ou com o SAP.**
1. As duas contas usam o mesmo período, a mesma etapa e a mesma data (dia produtivo ou calendário)?
2. A mesma fonte? (Trançagem pela Hora-Hora ou pelo evento Fim; inspeção por DataHoraInspecao ou Created.)
3. Cancelado, Parcial e ficha filha foram tratados igual?
4. O painel é Import: mostra o dado até o último refresh.
5. Contra o SAP: compare por material, nunca o saldo geral. Siga Manual_BO.md e 07_Dados_SAP_x_GMS.md.

**A OP está travada.**
1. Etapa atual e desde quando (colunas InicioAguardando e InicioEmProcesso).
2. Último evento da ficha.
3. É fila (aguardando) ou etapa aberta sem apontamento?
4. Uma OP sem apontamento posterior não prova que a etapa terminou.

## 3. Armadilhas de número

1. Somar metros das 8 etapas conta a mesma mangueira 8 vezes. Produção da célula é a etapa final.
2. Média de tempo de ciclo mente quando há OP esquecida aberta. Use mediana, com P90 quando a cauda importa.
3. Não some percentuais nem faça média simples de percentuais. Recalcule pelos numeradores e denominadores.
4. Mês de produção pequena distorce % e PPM (parada de julho de 2026: sem produção de 04 a 26/07).
5. Total que melhora enquanto cada máquina piora (ou o contrário) é efeito de mix. Olhe por mangueira antes de concluir.
6. A janela da Hora-Hora não é hora cheia. Meta sempre pelos minutos da janela.
7. field_8 (Real Acum) e field_6 (Meta Acum) são acumulados. Somar acumulado multiplica o resultado.
8. A coluna Rendimento da Hora-Hora mistura 3 escalas. Use Real ÷ Meta.
9. O campo recurso dos eventos é a trançadeira de origem da ficha, não a máquina da etapa. Tem grafias diferentes (TH07, TH-07).
10. Horário da base em UTC: Brasília = UTC menos 3 h. A Data da Hora-Hora já é o dia produtivo.
11. Número exportado como texto: "1,050" na ficha é mil e cinquenta, não um vírgula zero cinco.
12. Valores 111, 1111 e 11111 são preenchimento.
13. Dado ausente não é zero. Janela sem apontamento é "sem apontamento".
14. Top 50 não é a lista. Ranking só depois de ler todo o universo do recorte.

## 4. Fato, cálculo e hipótese

- **Fato:** veio de uma linha lida agora. Cite lista e filtro.
- **Cálculo:** conta feita sobre os fatos. Mostre a fórmula e as linhas usadas.
- **Hipótese:** explicação provável. Diga o que a sustenta, o que a derrubaria e qual consulta confirma.
- Associação não é causa. Duas coisas que sobem juntas podem ter uma terceira por trás (mix, turno, mês).
- Confiança alta: cobertura completa, regra escrita, segundo caminho de cálculo batendo. Média: cobertura completa e regra escrita. Baixa: parcial, regra ambígua ou período com fronteira antiga. Diga o nível quando a decisão depender do número.

## 5. O que está fora do alcance

Diga "não tenho esse dado" e aponte quem tem:

- SAP direto (MB51, COOIS): só por export. O William tem.
- Tabelas de delineamento DM (Excel): engenharia. O Uiu vê só a Meta Hora gravada e a AMDM02_Spec.
- Sensor de máquina: o Factbird só cobre a TH07 e não está ligado ao Uiu.
- Especificação de produto, pressão, crimpagem: fonte aprovada da engenharia. Nunca interpolar.
- Custo do refugo: a tabela de custo padrão por família não existe (K12 oculto).
- Cpk: bloqueado enquanto a unidade do diâmetro (polegada x milímetro) estiver pendente (K14).
- Total anual certificado: depende da lista de agregados, que ainda não existe. Entregue por partes, com a cobertura.
