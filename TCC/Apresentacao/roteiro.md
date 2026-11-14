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
