# Defesa do TCC (GMS): roteiro de fala

A fala completa de cada slide, com o tempo previsto e o acumulado. É o mesmo texto que vai nas notas do apresentador do `GMS_Defesa.pptx`. Os capítulos entram aqui conforme são construídos.

Como ler: cada bloco é um clique. O que está entre colchetes você troca na hora. Não precisa decorar: a frase em negrito é a que não pode faltar.

## Capítulo 1 · O problema (0:00 a 3:30)

### 1a · 0:08 · acumulado 0:08
Na tela: a ficha verde, inteira.

**Tudo o que esta célula sabia sobre si mesma estava escrito aqui: numa ficha de papel.**

### 1b · 0:08 · acumulado 0:16
Na tela: a câmera entra na ficha e os números acendem.

A OP, a metragem, quem fez, em que turno. Preenchido à mão, etapa por etapa.

### 1c · 0:08 · acumulado 0:24
Na tela: os números saem do papel.

**Reparem: estava tudo aqui.** Nunca faltou dado nesta célula.

### 1d · 0:08 · acumulado 0:32
Na tela: os números viram o fio.

O que faltava era o caminho. O dado saía da estação e demorava a chegar em quem decide.

### 1e · 0:08 · acumulado 0:40
Na tela: o fio entra no carretel.

Este trabalho é sobre encurtar esse caminho.

### 2 · 0:20 · acumulado 1:00
Na tela: a capa.

[Bom dia / Boa tarde.] Meu nome é [seu nome], e este é o meu trabalho de conclusão de curso: [título do TCC]. O sistema se chama Guaratinguetá Manufacturing System. Vocês vão ver este carretel se fechar aos poucos, até o fim da apresentação.

### 3 · 0:35 · acumulado 1:35
Na tela: "1 a 2 dias".

**Um a dois dias.** Era esse o tempo que a informação levava para sair da estação de trabalho e chegar à mesa da supervisão. A ficha rodava a célula e voltava com graxa, às vezes rasgada. Só então alguém olhava. Com esse atraso, a gestão não acompanhava o turno: reagia ao dia anterior.

### 4 · 0:40 · acumulado 2:15
Na tela: o fio com três paradas. Um clique por parada.

O caminho era este. A ficha era preenchida à mão ao longo das oito etapas da célula. No turno seguinte, alguém digitava tudo de novo numa planilha. E só depois o apontamento era lançado no SAP. Três paradas, e em cada uma o dado ficava esperando. **Nenhuma delas acrescentava informação: era o mesmo dado, copiado de um lugar para o outro.**

### 5 · 0:35 · acumulado 2:50
Na tela: as oito estações apagadas, "Cegueira operacional".

Isso tem nome na literatura: **cegueira operacional**. A célula tem oito etapas em sequência, do mandril até a extração e a inspeção. São os oito arcos da logo do sistema. E a gestão não enxergava nenhuma delas no turno em que as coisas aconteciam. Calcular OEE era inviável, porque não havia registro consistente. E conferir uma única OP fechada contra o SAP custava uma manhã.

### 6 · 0:40 · acumulado 3:30
Na tela: "O dado já existia. O custo era chegar até ele." Um clique para a segunda frase, outro para as três palavras.

Esta é a tese do trabalho. **O dado já existia.** A ficha de papel registrava os mesmos campos que o sistema registra hoje. O que era caro era chegar até ele. E esse custo aparece em três planos. O tempo: quanto o dado demora até quem decide. A visibilidade: se dá para ver o estado da produção sem ninguém sair procurando. E a conexão: se o dado do chão de fábrica conversa com os sistemas da empresa. É nesses três planos que eu vou mostrar o resultado, lá na frente.

## Capítulo 2 · O método (3:30 a 6:00)

### 7 · 0:40 · acumulado 4:10
Na tela: o relógio de 24 horas em três arcos, os turnos, com "2 semanas", "3 turnos", "12 processos".

Antes de escrever qualquer tela, fui ver o trabalho onde ele acontece. É o Gemba Walk. **Duas semanas, nos três turnos, com doze processos mapeados.** Em cada um eu anotava três coisas: o que o operador escrevia, o que consultava antes e para onde a ficha seguia. E quem levantou o requisito foi quem escreveu a tela. Não há intermediário entre quem pede e quem entrega, e o operador virou critério de projeto desde a primeira tela.

### 8 · 0:35 · acumulado 4:45
Na tela: o mesmo anel, com três trechos: manhã na estação, tarde desenvolvendo, versão nova no turno seguinte.

O desenvolvimento seguiu um ciclo diário, o RAD, *Rapid Application Development*. De manhã, eu na estação, observando. À tarde, desenvolvendo. E no turno seguinte, a versão nova já estava em uso. **Um ciclo por dia: observar, construir, devolver ao turno.** Cada publicação deixava uma linha no diário de decisões, e daqui a pouco eu volto a ele.

### 9 · 0:40 · acumulado 5:25
Na tela: o anel vira fio e bate num muro de blocos, com uma única passagem acesa. "Low-code por restrição, não por preferência."

Agora, uma escolha que pode parecer gosto. Não foi. A governança de TI limita o que não foi homologado, e o Power Platform já estava homologado na empresa. Era a única passagem. **Low-code por restrição, não por preferência.** Isso evita o *Shadow IT*, o sistema que a área de negócio usa sem aprovação da TI. Mas não evita a dívida técnica, como a fórmula copiada entre telas. Por isso eu tratei o aplicativo como software, e já mostro como.

### 10 · 0:35 · acumulado 6:00
Na tela: a passagem vira a tela de um tablet com um botão. Mão com luva, cota de 48 px. "Avisar, não bloquear."

É na tela que o método vira decisão. O operador trabalha de luva, por isso os alvos de toque têm 48 pixels. E quando o dado diverge do cadastro da Engenharia, a tela avisa e deixa seguir. **Avisar, não bloquear.** Bloquear por cadastro desatualizado faz o operador abandonar o sistema. Já a metragem em branco ou zero impede o envio, porque aí o dado não existe.

## Capítulo 3 · A construção (6:00 a 9:35)

### 11a · 0:14 · acumulado 6:14
Na tela: o tablet encosta na ponta da mangueira, que é o terminal.

Esta é a arquitetura, e eu a mostro como uma mangueira. O tablet é o terminal: um por estação, e é por ele que o operador aponta.

### 11b · 0:14 · acumulado 6:28
Na tela: a mangueira se abre em vista explodida. Acendem a coleta (Power Apps) e os dados (Microsoft Lists).

Primeira camada, a coleta, no Power Apps: as telas por etapa, a validação na origem, a leitura do código de barras. Segunda, os dados, no Microsoft Lists, onde a ficha de produção, com uma linha por OP, é o eixo das telas.

### 11c · 0:14 · acumulado 6:42
Na tela: acende a orquestração (Power Automate).

Terceira, a orquestração, no Power Automate, com fluxos agendados e por evento. É aqui que vale a regra: **o cálculo pesado não roda no tablet.** O Power Automate o executa em horário agendado e grava o resultado já pronto.

### 11d · 0:13 · acumulado 6:55
Na tela: acende a análise (Power BI). As quatro camadas juntas.

Quarta, a análise, no Power BI, em camadas e modelo estrela. Quatro camadas, todas dentro do Power Platform que a TI já havia homologado.

### 12 · 0:30 · acumulado 7:25
Na tela: as três faixas da ISA-95. O nível 3 (GMS) aceso, o nível 4 (SAP) acima, os níveis 1 e 2 apagados. "O dado nasce do apontamento do operador."

Na hierarquia da ISA-95, o GMS fica no **nível 3**: faz a ligação com o SAP, no nível 4. Abaixo, os níveis 1 e 2 são as máquinas que ainda não alimentam o sistema por sensor. **Por isso o dado nasce do apontamento do operador.** E isso é também o que o GMS não mede: o que a máquina faz sem que alguém aponte. A tecnologia operacional fica fora dele.

### 13a · 0:20 · acumulado 7:45
Na tela: a câmera voa pelo fio. Agosto de 2025: Gemba Walk e início. Outubro de 2025: primeiras telas em produção.

Esta é a linha do tempo do projeto, e a câmera percorre o fio de ponta a ponta. Agosto de 2025: o Gemba Walk e o início do desenvolvimento. Em outubro de 2025, as primeiras telas já estavam em produção na célula, ainda lado a lado com o papel.

### 13b · 0:20 · acumulado 8:05
Na tela: papel e digital em paralelo até maio de 2026, quando a ficha sai.

Depois, papel e digital correram em paralelo: foram três meses de validação, com comparação diária entre os dois, até a retirada do papel. Em maio de 2026, a ficha deixou de circular. **Nove meses, do início até a ficha sair.**

### 13c · 0:20 · acumulado 8:25
Na tela: jun a out/2026: qualificação, norma escrita, Kaizen Award, painel na TV, conferência diária com o SAP. A ponta segue tracejada.

De junho a outubro de 2026: consolidação e expansão. A qualificação do TCC I, a norma escrita, o Kaizen Award, o painel de TV da Célula e a conferência diária com o SAP. A ponta continua tracejada: é futuro, e eu falo dele no fim.

### 14 · 0:40 · acumulado 9:05
Na tela: "2 × 7", uma barra curta e uma longa. "A barreira foi a adoção, não a técnica." Rodapé: Atkin et al. (2017).

Desses nove meses, dois foram de desenvolvimento e sete de implantação. [Dois por sete.] **A barreira foi a adoção, não a técnica.** Atkin e colegas, em 2017, mostraram que até tecnologia de benefício claro e custo zero encontra resistência quando muda a rotina de quem opera. Aqui apareceu o mesmo padrão: segundo o dossiê corporativo, a célula só passou a confiar no sistema quando os números bateram com o que se via no chão.

### 15 · 0:30 · acumulado 9:35
Na tela: três cartões: norma escrita, diário de decisões, código versionado. "Low-code com disciplina de software."

Por isso a construção tem uma disciplina própria: **low-code com disciplina de software.** Três cartões. A norma escrita, com princípios, padrões e conceitos catalogados. O diário de decisões, só de acréscimo. E o código das telas, em pasta versionada. O diário guarda também o que deu errado: decisões revertidas e até um alarme falso, registrado de propósito, para lembrar que o sinal de sucesso de uma ferramenta não prova que o dado chegou.

## Capítulo 4 · A expansão e o ao vivo (9:35 a 14:30)

### 16a · 0:11 · acumulado 9:46
Na tela: o carretel vem para o centro e vira o núcleo. As cinco pontas ainda apagadas.

Até aqui, uma célula. Agora, **o que nasceu nela e onde chegou.** O carretel vai para o centro, e a partir dele o sistema alcança cinco áreas. Vou acendendo uma a uma.

### 16b · 0:11 · acumulado 9:57
Na tela: acende a ponta Manufatura: 8 etapas apontadas na estação, Hora-Hora, painéis de TV da Célula e da Montagem.

Manufatura, de onde tudo partiu: as oito etapas apontadas na estação, o Hora-Hora, que compara o realizado com a meta por janela de tempo, e os painéis de TV da Célula e da Montagem. O papel saiu em maio de 2026.

### 16c · 0:11 · acumulado 10:08
Na tela: acende a ponta Qualidade: inspeção e refugo tipificado, medida conferida contra a especificação, carta X̄-R da trançagem (em paralelo ao papel).

Qualidade. A inspeção e o refugo são tipificados. A medida que o operador registra é conferida contra a faixa especificada na hora, e **a tela avisa, sem bloquear.** E a carta de controle X̄-R da trançagem ganhou tela própria, que corre em paralelo ao papel.

### 16d · 0:11 · acumulado 10:19
Na tela: acende a ponta Planejamento: OP escolhida no plano sincronizado, exceção aprovada pela supervisão.

Planejamento. A OP deixou de ser digitada: depois que as fichas mostraram números de OP inventados, ela passou a ser escolhida numa lista sincronizada com o plano. Fora do plano, só com **pedido de exceção aprovado pela supervisão.**

### 16e · 0:11 · acumulado 10:30
Na tela: acende a ponta Logística: packing list por pallet com código de barras, conferência diária com o SAP.

Logística. O packing list é registrado por pallet no próprio sistema, com código de barras. E a conferência diária com o SAP, de terça a sábado, sem nova digitação: **o SAP é a referência quando os registros divergem.**

### 16f · 0:10 · acumulado 10:40
Na tela: acende a ponta Engenharia. Surgem nós tracejados, sem nome.

Engenharia. Os cadastros de delineamento são lidos pelas telas, e o ciclo, o gargalo e as paradas aparecem no BI. Estes nós tracejados, sem nome, são o que **ainda não existe.** Eu volto a eles no fim.

### 17 · 0:30 · acumulado 11:10
Na tela: o mosaico de oito cartões de relatório. Acesos: fila por etapa, paradas, Hora-Hora, Montagem e Extrusora. Tracejados: OEE por hora, simulador de demanda × pessoas, genealogia entre lotes. Dado fictício.

Este é o relatório, com dado ilustrativo. Acesos, os cinco que **já existem**: a fila de cada etapa, as paradas, o Hora-Hora, a Montagem e a Extrusora. Tracejados, o que **ainda não foi entregue**: OEE por hora, um simulador de demanda contra pessoas e a genealogia entre lotes.

### 18 · 3:20 · acumulado 14:30
Na tela: "Agora, ao vivo." Os três passos e "No tablet, na mão." O tablet fica na mão, não vai ao projetor.

**Frase de entrada:** Agora, ao vivo. Vou pegar o tablet, e vocês acompanham pelo que eu descrever. São três coisas.

**Passo 1 · apontar uma etapa (cerca de 1:10).** Abro a tela de uma etapa. Escolho a OP na lista, que vem do plano. Digito a metragem e aponto. Reparem no que a tela faz se eu errar: avisa, mas deixa seguir. Metragem em branco ou zero, não: aí o dado não existe.

**Passo 2 · ver o painel reagir (cerca de 1:10).** Olho o painel da Célula. O apontamento que acabei de fazer já está na fila da etapa. Na lista ele aparece no instante do registro, e no painel de TV em até dois minutos, que é o ciclo de recarga da tela.

**Passo 3 · achar uma OP (cerca de 0:50).** Abro a consulta e procuro uma OP. Era isso que, no papel, custava uma manhã. Aqui: digito, e ela aparece com o estado e o histórico.

**Frase de saída:** Foi isso. O dado não mudou: mudou o custo de chegar até ele. Vamos ver o que isso produziu.

[Se a rede cair: um clique no ponto discreto do slide leva aos três slides de reserva. Narre as mesmas três ações; o último volta ao fluxo.]

### 18B1 · 0:50 · acumulado 14:30
Na tela: plano B, passo 1 · apontar uma etapa, em tela recriada. Fora da conta de tempo.

Sem o tablet, vejo aqui a mesma tela, com dado ilustrativo. Escolho a OP na lista, informo a metragem e aponto. Se a medida divergir do cadastro, a tela avisa e deixa seguir.

### 18B2 · 0:50 · acumulado 14:30
Na tela: plano B, passo 2 · o painel reage. Fora da conta de tempo.

O apontamento aparece na fila da etapa. É o painel da Célula, no instante em que o registro entra, e em até dois minutos na TV.

### 18B3 · 0:50 · acumulado 14:30
Na tela: plano B, passo 3 · achar uma OP. Fora da conta de tempo.

Consulto uma OP: estado e histórico. Era uma manhã de conferência; aqui é uma busca. Daqui sigo para os resultados.

## Capítulo 5 · Os resultados (14:30 a 17:20)

### 19 · 0:40 · acumulado 15:10
Na tela: a ficha da abertura à esquerda, o tablet à direita e três linhas entre os dois: tempo, visibilidade e conexão, cada uma com o antes e o depois.

Lembram dos três planos do começo: tempo, visibilidade e conexão? Agora com evidência. **No tempo,** o apontamento que levava de um a dois dias para chegar à supervisão fica na lista no instante do registro e, no painel de TV, em até dois minutos, que é o ciclo de recarga da tela. **Na visibilidade,** antes nenhuma etapa tinha a fila à vista; hoje todas têm, cada ordem com a sua idade. **Na conexão,** conferir uma OP fechada custava uma manhã; hoje a conferência com o SAP sai todo dia, de terça a sábado, e as divergências que restam viram item de tratativa com responsável.

### 20 · 0:30 · acumulado 15:40
Na tela: "O que o dossiê do Kaizen estima": 36×, 87,5% e 97%, com a faixa fixa "estimativas da equipe, sem cronometragem".

O dossiê corporativo do Kaizen traz três números: a resposta a reclamação 36 vezes mais rápida, o escopo de contenção 87,5% menor e 97% menos horas de consolidação de relatórios. **Leio os três com reserva.** São estimativas da equipe, sem cronometragem; o dossiê não descreve o método, e o escopo de contenção não tem linha de base detalhada. Por isso eu os cito, mas não os tomo como medida.

### 21a · 0:15 · acumulado 15:55
Na tela: "8,3×" sozinho e, abaixo, "O volume da célula era contado 8,3 vezes."

Aquilo é estimativa. **Isto o sistema mediu.** Ao medir o volume na origem, ele mostrou que o indicador contava 8,3 vezes a saída real: o mesmo metro era somado em cada etapa.

### 21b · 0:20 · acumulado 16:15
Na tela: o 8,3× encolhe para a base e entra a barra: "74% da 'parada' da Montagem era tempo excedido". É o próximo clique.

E não foi o único. Dos minutos de "parada" da Montagem, 74% eram tempo excedido, e a regra proíbe somar os dois com a parada real. O painel passou a mostrar os dois em cartões separados. **Ao medir na origem, o sistema auditou os próprios indicadores.** O TCC I não previa isso.

### 22 · 0:35 · acumulado 16:50
Na tela: duas barras: SAP, 96,4%; sensor, até 6%. Rodapé: Resumo; seção 4.4 e Tabela 2.

**Conferi contra fontes que eu não controlo.** A primeira é o SAP: numa análise retrospectiva de um mês, 96,4% das OPs do GMS também estavam lá. É cobertura, não garantia de que o SAP esteja certo. A segunda é o sensor da única máquina que tem um, durante quinze dias. Nos turnos fechados, hora a hora, o apontamento erra cerca de nove minutos, para mais ou para menos. Como o viés é próximo de zero, no total dos turnos fechados o tempo parado fica a até 6% do medido. **O sensor auditou o apontamento, não o substituiu.**

### 23 · 0:30 · acumulado 17:20
Na tela: o anel de onze arcos do MESA-11: seis acesos, um pulsando, dois meio acesos e dois apagados.

O modelo da MESA International lista onze funções de um sistema de execução. Seis estão implementadas, uma em expansão, duas parciais e duas fora do escopo. **Nenhuma função mudou de situação desde a qualificação. Mudou a prova.** A análise de desempenho segue em expansão enquanto o OEE usar velocidade cadastrada e a acurácia estiver conferida em uma só máquina. Falta dizer, com franqueza, o que isso não prova.
