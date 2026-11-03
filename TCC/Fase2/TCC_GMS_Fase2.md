## RESUMO

O registro em papel no chão de fábrica faz a informação chegar à gestão com dias de atraso e mantém as decisões numa postura reativa. Em multinacionais, a governança de Tecnologia da Informação (TI) agrava o quadro ao restringir ferramentas não homologadas. Este trabalho apresenta a finalização, validação e análise do Guaratinguetá Manufacturing System (GMS), um Sistema de Execução de Manufatura (MES) construído sobre o ecossistema *low-code* da Microsoft para uma célula de mangueiras hidráulicas no interior paulista. A arquitetura reúne Power Apps, SharePoint, Power Automate e Power BI, mantidos por norma escrita e testes automatizados. O estudo de caso validou o sistema por comparação com o papel, auditoria das telas, conciliação com o SAP e confronto com o sensor de estado de uma trançadeira. Em agosto de 2026, 96,4% das ordens de produção registradas no GMS também estavam no SAP, e, na máquina que tem sensor, o tempo parado registrado nos turnos fechados ficou a até 6% do medido pelo equipamento. Ao medir na origem, o sistema expôs erros na definição dos próprios indicadores, como um volume contado 8,3 vezes. A resposta a reclamações 36 vezes mais rápida, registrada no dossiê corporativo, é estimativa da equipe, sem cronometragem, e o ganho de produtividade, de 0,22%, é marginal. A contribuição está na mudança do regime informacional: o dado passou a ser acessível no turno e auditável contra o ERP. O GMS foi escolhido para a planta de Forest City, nos Estados Unidos, onde será replicado.

Palavras-chave: Sistemas de Execução de Manufatura; *Low-Code*; Power Platform; Digitalização de Processos; Indústria 4.0.

## 1. INTRODUÇÃO

Este trabalho foi desenvolvido em uma corporação multinacional do setor de soluções hidráulicas, numa unidade do interior de São Paulo que fabrica mangueiras hidráulicas. A célula estudada tem oito estações em sequência fixa, do Mandril à Extração e Inspeção, e cada ordem de produção (OP) passa por todas. A literatura de Indústria 4.0 trata a coleta de dados na origem como alicerce da manufatura inteligente (KUSIAK, 2018; TAO et al., 2018), mas nessa célula o apontamento era feito em papel e só chegava à gestão depois de consolidação manual, o que se chama de cegueira operacional (JESUS et al., 2025; WU; XU; ZHENG, 2024).

O dossiê corporativo descreve o ponto de partida: cerca de 2.900 lançamentos manuais por mês e aproximadamente 28 fontes de dados desconectadas. Em março de 2026, com o papel ainda correndo em paralelo às telas, a célula preencheu 387 fichas. A ficha voltava com graxa e rasgos e chegava à supervisão com um a dois dias de atraso. O cálculo do *Overall Equipment Effectiveness* (OEE) ficava inviável, pois depende de registros consistentes de disponibilidade, desempenho e qualidade (NAKAJIMA, 1988; SCHIRALDI; VARISCO, 2020), e conferir uma OP fechada contra o *Enterprise Resource Planning* (ERP) da corporação, o SAP, custava uma manhã. Uma OP chegou a ficar 4.162 horas parada numa etapa sem que ninguém percebesse.

A resposta foi o Guaratinguetá Manufacturing System (GMS), um Sistema de Execução de Manufatura (*Manufacturing Execution System*, MES) construído sobre o ecossistema *low-code* da Microsoft, o Power Platform. A escolha foi restrição, não preferência: a governança de TI limita o que não foi homologado, e o Power Platform já estava homologado na empresa, caminho que Michael e Wortmann (2024) descrevem na manufatura. A Figura 1 resume o que mudou no caminho da informação.

[[FIGURA 1 | Fluxo da informação antes e depois do GMS | fig01_fluxo_antes_depois.png | Fonte: elaboração própria (2026).]]

O objetivo geral permanece o do Trabalho de Conclusão de Curso (TCC) I: converter a célula em um ambiente operado sobre dados em tempo real, em que a gestão acompanha o turno corrente e não o dia anterior. Os objetivos específicos passam a ser concluir as camadas de coleta, orquestração e análise; validar o sistema contra o papel e o SAP; comparar o resultado com trabalhos relacionados; e preparar a replicação. O método é o estudo de caso aplicado e exploratório (MIGUEL et al., 2012), com ciclos diários de *Rapid Application Development* (RAD) (MARTIN, 1991). A tese defendida é que o GMS não substitui uma folha de papel, mas a forma como a célula acessa informação sobre si mesma: o papel já registrava os mesmos campos, e o que muda é o custo de acessá-los.

O GMS foi escolhido para uso na planta da corporação em Forest City, Carolina do Norte, nos Estados Unidos da América (EUA). Este trabalho trata a replicação como próxima etapa, sem antecipar datas ou escopo, e levanta os requisitos de adaptação que o projeto revelou. A ISA-95 da *International Society of Automation* (ISA) e as funções da *Manufacturing Enterprise Solutions Association* (MESA), que balizam o sistema, foram publicadas nos Estados Unidos (ANSI/ISA-95, 2010; MESA INTERNATIONAL, 1997).

## 2. REVISÃO BIBLIOGRÁFICA

Esta seção condensa a revisão do TCC I e acrescenta os trabalhos novos, do MES ao contexto norte-americano.

### 2.1 Sistemas de Execução de Manufatura, ISA-95 e o modelo MESA-11

Xu, Xu e Li (2018) traçam o panorama da Indústria 4.0 e de suas tecnologias habilitadoras, como internet das coisas, sistemas ciber-físicos e *big data*. Todas começam pelo dado de produção, e é na coleta desse dado que o MES ganha lugar. Conforme a MESA International (1997) e a norma ANSI/ISA-95 (2010), ele gerencia a execução da produção entre o planejamento empresarial, no nível 4, e o controle de processo, nos níveis 1 e 2. A Figura 2 mostra o GMS no nível 3, com o SAP acima e, abaixo, máquinas que ainda não alimentam o sistema por sensor, de modo que o dado nasce do apontamento do operador. Para Scholten (2007), a aderência à ISA-95 garante a coerência do MES com as demais camadas. Mantravadi, Srai e Møller (2023) analisam casos de MES e de gestão de operações de manufatura (*Manufacturing Operations Management*, MOM) de nova geração, inclusive a integração entre tecnologia da informação e tecnologia operacional. O GMS cobre a ligação entre os níveis 3 e 4; a tecnologia operacional fica fora dele.

O modelo da MESA International (1997) enumera onze funções: alocação e status de recursos, programação detalhada, despacho de unidades de produção, controle de documentos, coleta e aquisição de dados, gestão de mão de obra, gestão da qualidade, gestão de processo, gestão de manutenção, rastreamento e genealogia do produto e análise de desempenho.

O OEE foi formalizado na manutenção produtiva total (*Total Productive Maintenance*, TPM) por Nakajima (1988), e Schiraldi e Varisco (2020) comparam a norma ISO 22400 com a literatura quanto à consistência entre disponibilidade, desempenho e qualidade. Na norma do GMS, a parada real, em que a célula não consegue produzir, nunca se soma ao tempo excedido, em que a célula produz acima do tempo da meta; a seção 4.3 mostra o que acontecia antes dessa separação. Enquanto a velocidade for cadastrada, e não medida, o OEE do GMS é simplificado.

[[FIGURA 2 | Posição do GMS na hierarquia funcional da ISA-95 | fig02_isa95.png | Fonte: elaboração própria (2026).]]

### 2.2 O paradigma *low-code* e a governança de TI

A plataforma *low-code* troca código por configuração visual, o que Di Ruscio et al. (2022) leem como a outra face da engenharia dirigida a modelos. Na manufatura, ela tem servido para depender menos da equipe de TI (MICHAEL; WORTMANN, 2024) e para levar o desenvolvimento a quem conhece o problema de negócio (SILVA et al., 2025), caso deste projeto, em que o autor levantou os requisitos e escreveu as telas. O custo aparece depois. Bock e Frank (2021) apontam a dependência do fornecedor; revisões e relatos de praticantes acrescentam dificuldades de governança, depuração e manutenção (AJIMATI; CARROLL; MAHER, 2025; LUO et al., 2021). A homologação evita o *Shadow IT*, sistema usado na área de negócio sem aprovação da TI (HAAG; ECKHARDT, 2017), mas não evita a dívida técnica, classificada em dez tipos por Li, Avgeriou e Liang (2015), que no GMS aparece como fórmula copiada entre telas.

### 2.3 Visibilidade operacional e custo da informação

Wu, Xu e Zheng (2024) descrevem a fábrica inteligente como aquela em que o estado da produção chega à gestão no mesmo intervalo do evento físico, e Lin (2025) mostra que o ganho central da digitalização nas pequenas e médias empresas (PMEs) é informacional, pois o dado deixa de ser garimpado. O fio comum é o custo de acesso, lido aqui em três planos: o do tempo, quanto o dado demora a chegar a quem decide; o da visibilidade, se o estado da produção pode ser visto sem que alguém o procure; e o da conexão, se o dado do chão conversa com os sistemas da empresa. A ficha de papel já registrava os mesmos campos, e o que o sistema muda é o custo de acessá-los.

### 2.4 Qualidade de dado, rastreabilidade e genealogia

Em revisão sistemática sobre sistemas ciber-físicos e internet das coisas (*Internet of Things*, IoT), completude, consistência e acurácia aparecem como requisitos de qualidade do dado (GOKNIL et al., 2023). Speicher et al. (2026), ao estudar um fabricante de médio porte da Pensilvânia que se prepara para MES, concluem que ele depende de dado oportuno e preciso. O *digital thread*, fio de dados que atravessa o ciclo de vida do produto (ABDEL-ATY; NEGRI, 2024), no GMS é a ficha de produção, com uma linha por OP e rastreio por carretel; a genealogia entre lotes continua como proposta. Das três dimensões, a acurácia é a única que não se verifica dentro do próprio registro, pois exige uma fonte independente do apontamento, papel que nos trabalhos de monitoramento em tempo real cabe ao sinal da máquina (TAPIA et al., 2024).

### 2.5 Fator humano e adoção de tecnologia no chão de fábrica

Atkin et al. (2017) mostraram que até tecnologia de benefício claro e custo zero encontra resistência quando muda a rotina de quem opera. Kaasinen et al. (2020), que desenvolveram soluções Operator 4.0 junto com operadores, chegam ao mesmo ponto pelo outro lado, pois o engajamento do trabalhador decide o resultado. A aceitação de tecnologia tem duas décadas de estudo (VENKATESH; THONG; XU, 2016), e a Indústria 5.0 põe o humano no centro (LENG et al., 2022), inclusive na manufatura de defeito zero, em que ele deixa de ser tratado só como fonte de erro (WAN; LEIRMO, 2023). No GMS isso virou regra de tela, com alvos de toque de 48 px porque o operador usa luva, e aviso em vez de bloqueio quando o cadastro diverge.

### 2.6 Manufatura inteligente nos Estados Unidos e replicação

Em PMEs, plataformas *low-code* já integram ativos de manufatura a gêmeos digitais, com operadores criando *dashboards* e fluxos sem programação avançada (KOPROV; STARLY, 2025). Helu et al. (2020), do *National Institute of Standards and Technology* (NIST), propõem um *pipeline* de dados escalável para várias fontes do chão de fábrica. Levar um sistema a outro país exige ainda teste de internacionalização (ALAMEER; HALFOND, 2016; COUTO; MIRANDA; CARTAXO, 2026).

### 2.7 Trabalhos relacionados

O Quadro 1 confronta oito trabalhos recentes com o GMS.

[[QUADRO 1 | Trabalhos relacionados e posicionamento do GMS | Fonte: elaboração própria (2026).]]

| Trabalho | Contexto e tecnologia | Contribuição | Diferença em relação ao GMS |
|---|---|---|---|
| Heuer et al. (2024) | Empresas de manufatura; casos de uso de *low-code* | Tipifica usos recorrentes: formulários, rastreamento de ordens, coleta de dados de processo | Oferece o catálogo; o GMS é uma implantação que cobre vários desses usos numa só célula |
| Santos et al. (2025) | Gestão de processos de negócio; *low-code* e hiperautomação | Propõe o ciclo iBPM para reduzir a intervenção humana em fluxos repetitivos | Foco em processo de negócio; o GMS leva a lógica ao chão de fábrica e à conciliação com o SAP |
| Koprov e Starly (2025) | PMEs; *low-code* com Node-RED e MQTT Sparkplug B | Integra ativos de manufatura a gêmeos digitais; operadores criam *dashboards* e fluxos | Parte de máquinas conectadas; o GMS parte do apontamento humano, sem sensor |
| Bianchini et al. (2024) | MES em PMEs; indicadores na linha de produção | Descreve a captura de dados pelo MES e o desenvolvimento de indicadores, com obstáculos de orçamento e transferência de tecnologia | O GMS responde com desenvolvimento interno e investimento de capital zero, sob governança corporativa |
| Gomes et al. (2024) | PMEs; fatores de adoção de MES na Indústria 4.0 | Identifica os fatores que levam PMEs a adotar MES, tratado como meio de integração vertical | Lista fatores; o GMS os põe à prova em implantação incremental e registra o que falhou |
| Speicher et al. (2026) | Fabricante de médio porte na Pensilvânia (EUA); preparo para MES e IoT industrial | Mostra que o MES depende de dado de chão de fábrica oportuno e preciso | Caso de preparação; o GMS já opera e audita a qualidade do dado em produção |
| Novochadlo e Paladini (2024) | Três centros de montagem manual; OEE em tempo real com IoT e nuvem | Reduz paradas não planejadas e eleva a eficiência média em 12,3% em sete meses, com ressalva de prazo curto e sazonalidade | Mede ganho de eficiência com OEE vindo de sensor; o GMS mede o acesso à informação e declara marginal o ganho de produtividade |
| Tapia et al. (2024) | Fresadora de cinco eixos; monitoramento em tempo real | Plataforma escalável que coleta, processa, detecta *outliers* e exibe em *dashboard* | Mesma cadeia coleta, processamento e painel; o GMS troca o sensor da máquina pelo apontamento do operador |

## 3. METODOLOGIA

Esta seção descreve como a pesquisa foi conduzida e como o sistema foi construído e verificado.

### 3.1 Classificação da pesquisa e levantamento de requisitos

O trabalho mantém a classificação do TCC I: estudo de caso aplicado e exploratório (MIGUEL et al., 2012), numa célula em produção real, sem ambiente de teste isolado. O levantamento de requisitos seguiu o *Gemba Walk*, observação do trabalho no lugar onde o valor é gerado (IMAI, 2012; WOMACK; JONES, 1996). Durante duas semanas o autor acompanhou os três turnos e mapeou 12 processos, anotando o que o operador escrevia, o que consultava antes e para onde a ficha seguia. Como quem levantou o requisito escreveu a tela, não há a assimetria de informação entre comprador e fornecedor que Tabim et al. (2024) analisam nos MES comerciais, e o engajamento do trabalhador (KAASINEN et al., 2020) virou critério de projeto desde as primeiras telas.

### 3.2 Ciclo de desenvolvimento

O desenvolvimento seguiu o RAD, mantido do TCC I porque a plataforma trabalha por abstração visual e declarativa (DI RUSCIO et al., 2022), em cadência diária, com manhã na estação observando, tarde no desenvolvimento e versão nova no turno seguinte. Nesta etapa o ciclo ganhou um portão de qualidade antes da publicação, em que a tela passa por uma bateria automatizada de garantia de qualidade (*quality assurance*, QA) e a decisão vai para o diário. A bateria não chega a ser integração contínua (HILTON et al., 2016).

### 3.3 Arquitetura técnica e ferramentas

A pilha continua restrita ao Power Platform, homologado pela governança de TI. A Figura 3 mostra as camadas e o Quadro 2 a responsabilidade de cada ferramenta; a separação em camadas acompanha a lógica dos MES e MOM de nova geração (MANTRAVADI; SRAI; MØLLER, 2023). Pelo escopo, o GMS é um MES híbrido, que incorpora supervisão por painel e registros de qualidade e se limita a validar a OP contra o plano, sem programar a produção.

[[QUADRO 2 | Ferramentas e responsabilidades por camada | Fonte: elaboração própria (2026).]]

| Camada | Ferramenta | Responsabilidade |
|---|---|---|
| Coleta | Power Apps Canvas, Power Fx | Telas por etapa, validação na origem, leitura de código de barras |
| Regras e padrão visual | App.Formulas, em 19 seções | Fórmulas nomeadas, funções definidas pelo usuário e tokens de design com prefixo fx_ |
| Persistência | Microsoft Lists (SharePoint) | Mais de 30 listas; a ficha de produção, com uma linha por OP, é o eixo das telas de etapa |
| Orquestração | Power Automate | Fluxos agendados e por evento; notificação e cálculo pesado |
| Conciliação | Office Scripts (TypeScript) | Conferência entre GMS, SAP e *packing list*, sem escrita na planilha |
| Análise | Power BI | Camadas Bronze, Prata e Ouro; modelo estrela |
| Dispositivos | Tablet, leitor, impressora, TV | Um terminal por estação; romaneio de embarque (*packing list*) com Code 39 e Code 128; painel de gestão |
| Acesso | E-mail corporativo | Setor definido por mapeamento; sem mapeamento, perfil de gestão |

O arquivo App.Formulas reúne, em 19 seções, cores, tipografia, geometria, tempo e regras de estado de etapa; o que depende do tempo vira função definida pelo usuário que recebe o instante como parâmetro, e os tokens com prefixo fx_ proíbem cor e tamanho escritos à mão. As telas nascem de modelos (*templates*) parametrizados pela etapa, e o código de cada uma é um arquivo YAML. A ficha de produção tem uma linha por OP e é chaveada pelo identificador do item, nunca pelo número da OP, que nasce vazio e é editável. Consultas não delegáveis retornam 500 registros, até 2.000 por configuração, e ignoram o resto sem avisar; por isso os filtros usam funções delegáveis e as colunas de filtro são indexadas. O cálculo pesado não roda no tablet: o Power Automate o executa em horário agendado e grava o resultado pronto, e os Office Scripts fazem a conciliação com o SAP. No Power BI, ferramenta de *Business Intelligence* (BI), a camada Prata resolve turno e data de referência uma única vez.

[[FIGURA 3 | Arquitetura do GMS em camadas e ferramentas | fig05_arquitetura.png | Fonte: elaboração própria (2026).]]

### 3.4 Fluxo genérico de operação das telas

Todas as telas seguem um padrão parametrizado pela etapa. O terminal da estação abre a tela da etapa, a fila mostra só as ordens disponíveis, o operador seleciona a OP ou lê o código do carretel, preenche os campos e grava, e a ordem entra na fila da etapa seguinte. Quando o dado diverge da planilha de engenharia, como o fio previsto para a OP, a tela avisa e deixa seguir, porque bloquear por planilha desatualizada faz o operador abandonar o sistema; metragem em branco ou zero, ao contrário, impede o envio.

### 3.5 Engenharia de software *low-code*

Como a dívida técnica também se acumula numa plataforma *low-code*, em fórmula copiada e em tela extensa (seção 2.2), o projeto tratou o aplicativo como software. A norma escrita reúne princípios, padrões e 40 conceitos catalogados. As decisões vão para um diário só de acréscimo, com 13 tipos de linha, o que responde ao problema de decisões sem registro estruturado descrito por Weinreich, Groher e Miesbauer (2015); o original foi perdido e reconstruído em outubro de 2026, com setembro aproximado. O backlog tem mais de 250 itens rastreáveis, o código das telas fica em pasta versionada e, antes de cada entrega, a bateria automatizada, com 19 verificações e um inventário da tela, precisa passar. O Apêndice B detalha as telas.

### 3.6 Método de validação

A validação combina oito frentes, resumidas no Quadro 3. Três frentes vêm do TCC I: a comparação diária entre papel e digital, por três meses; a adesão, medida pela continuidade dos registros ao longo dos turnos; e a comparação do ciclo medido com a estimativa histórica. As demais perguntam se o código está correto, se o dado confere com o ERP, se o apontamento confere com o evento físico e se o resultado declarado resiste a escrutínio. Cada indicador do GMS recebe definição escrita, cautela que o confronto de Schiraldi e Varisco (2020) entre a ISO 22400 e a literatura sobre OEE justifica, e o ganho de produtividade é lido com reserva na subseção 4.5.

Como o autor desenvolveu e também avaliou o sistema, as frentes foram apoiadas, sempre que possível, em fontes que ele não produz. A extração do SAP é lançada por outros usuários, e o sensor da trançadeira mede a máquina sem passar pelo operador nem pelo aplicativo. O diário, por sua vez, guarda também o que deu errado, inclusive decisões revertidas e um alarme falso de agosto de 2026, registrado de propósito para lembrar que o sinal de sucesso de uma ferramenta não prova que o dado chegou. A mitigação é parcial, pois a escolha das análises e a leitura dos resultados continuam com o autor, como se discute na seção 4.10.

[[QUADRO 3 | Frentes de validação, instrumentos e critérios | Fonte: elaboração própria (2026).]]

| Frente | Instrumento | Critério de aceite |
|---|---|---|
| Papel × digital | Comparação diária e qualitativa por 3 meses | Divergências de campo identificadas e tratadas antes da retirada do papel |
| QA automatizado | Bateria de 19 verificações e inventário | Aprovação antes da publicação |
| Auditoria por tela | 25 telas, 2.854 apontamentos do verificador | Defeitos triados e corrigidos |
| Conciliação com o SAP | GMS × SAP × *packing list* | OP com diferença zero ou tratativa aberta |
| Indicadores do Kaizen | Dossiê corporativo | Valores relativos, lidos com reserva por falta de auditoria independente |
| Adesão | Cobertura e fechamento do Hora-Hora por turno | Registros contínuos e turnos fechados em todos os turnos |
| Acurácia | Tempo parado do Hora-Hora × sensor de estado da trançadeira | Diferença por hora e por turno documentada |
| Medição × estimativa | Ciclo medido contra tempo padrão da Engenharia | Diferença por etapa documentada |

## 4. RESULTADOS E DISCUSSÃO

Esta seção apresenta o que a implantação entregou, como foi verificado e o que significa, e termina na replicação e nas limitações.

### 4.1 Finalização da implementação

A Figura 4 mostra a célula como opera hoje, com as oito etapas em sequência e a fila de cada uma visível para a seguinte. O Quadro 4 compara o TCC I com o estado atual. A ficha de produção em papel foi retirada a partir de maio de 2026, depois de três meses de validação em paralelo, e o mesmo registro alimenta hoje o painel de TV, com alertas no estilo *Andon*, o Hora-Hora, que acompanha o realizado contra a meta por janela de tempo, e a conferência com o SAP, sem nova digitação. O critério de adesão herdado do TCC I, a continuidade dos registros em todos os turnos, foi medido no Hora-Hora, e o resultado está na seção 4.4. Na ficha de produção a evidência é indireta: com a retirada do papel, o registro digital ficou como o único da OP, e, segundo o diário de decisões, os campos de operador e turno com erro, que no histórico variavam de 6% a 93%, ficaram próximos de zero nos 60 dias mais recentes, indício da qualidade do registro e não da continuidade.

[[QUADRO 4 | Situação final de implantação por módulo (TCC I × TCC II) | Fonte: elaboração própria (2026).]]

| Módulo | TCC I | TCC II |
|---|---|---|
| Coleta | Oito telas de etapas produtivas: implantado e em operação | Em produção; papel retirado desde maio/2026 |
| Persistência | Cinco listas estruturadas: implantado e em operação | Mais de 30 listas; a ficha de produção é o eixo das etapas; consolidação das demais pendente |
| Hora a hora | Implantado (etapa Trançagem) | Telas na Trançagem, na Montagem e na Cobertura; lista higienizada de setembro a outubro |
| Análise gerencial | Painéis em Power BI: em desenvolvimento | Camadas Bronze, Prata e Ouro; páginas de fluxo, paradas, Hora-Hora, Montagem e Extrusora (seção 4.3) |
| Orquestração | Fluxos em Power Automate: em desenvolvimento | Conferência com o SAP, sincronização do plano de OPs e dos tempos da Montagem, início do resfriamento (seção 4.2) |
| Painéis de TV (*Andon*) | Fora do escopo da etapa | Célula e Montagem, com alertas derivados do dado e filtro por dia e turno (seção 4.6) |
| Preparação de fio e montagem | Fora do escopo da etapa | Telas próprias, com bipe de etiqueta |
| Ficha técnica e finalização | Fora do escopo da etapa | Dado mestre consultado pelas telas; *packing list* registrado por pallet no GMS, com código de barras |
| Validação de OP | Já existia, contra a lista de planejamento (seção 3.6 do TCC I) | Escolha em lista sincronizada com o plano; exceção aprovada pela supervisão; cancelamento de OP |
| Controle estatístico | Fora do escopo da etapa | Carta X̄-R da trançagem (formulário AM-DM-02) em paralelo ao papel |

[[FIGURA 4 | Fluxo da célula e filas por etapa no GMS | fig07_fluxo_celula.png | Fonte: elaboração própria (2026).]]

Entre a qualificação e o fechamento deste trabalho, o escopo cresceu em direções que o TCC I não previa. A OP deixou de ser digitada: depois que as fichas de setembro e outubro de 2026 mostraram quatro números inventados em 431 registros, ela passou a ser escolhida numa lista sincronizada com o plano da trançadeira por um Office Script, e o caso fora do plano virou pedido de exceção aprovado pela supervisão. O *packing list*, que vinha de uma base externa apagada em 8 de outubro de 2026, passou a ser registrado por pallet no próprio GMS, com o código de barras do total igual ao da macro antiga e testado com o leitor. A carta de controle X̄-R da trançagem ganhou tela própria e corre em paralelo ao papel, e o tempo padrão da Montagem saiu do pacote do aplicativo para uma lista sincronizada por fluxo. Na conferência com o SAP, o nome da mangueira no GMS passou a ser ligado ao material do ERP pela OP, com uma tabela de apelidos, porque a mesma mangueira aparece com grafias diferentes nos dois sistemas.

A entrada dos módulos foi incremental, como na implantação por etapas descrita por Frank, Dalenogare e Ayala (2019) e nos modelos de maturidade de Mittal et al. (2018); a Figura 5 registra a cronologia.

[[FIGURA 5 | Linha do tempo do projeto | fig08_linha_tempo.png | Fonte: elaboração própria (2026).]]

### 4.2 Camada de orquestração

A Figura 6 descreve a conferência entre o GMS, o SAP (extração MB51) e a *packing list*. Um fluxo agendado de terça a sábado, às 08:00, chama um Office Script, somente leitura, que classifica as divergências em 14 categorias (depois 20), envia um e-mail diário e abre itens numa lista de tratativa com responsável, tomando o SAP como referência quando os registros divergem. O fluxo foi ligado em 2 de outubro de 2026 e reescrito no dia 8, quando a base antiga de *packing list* foi apagada: desde então o romaneio é casado com a inspeção lance a lance, pelo identificador do registro, e só é cobrado de OP finalizada. No teste dessa versão, sobre o dia 7 de outubro, 12 das 16 OPs conferidas estavam conformes e as quatro restantes eram divergências reais com o SAP. Outros dois fluxos levam para listas o plano de OPs da trançadeira e o tempo padrão da Montagem, e um terceiro inicia o resfriamento 110 minutos depois do início da vulcanização, conferido em cinco OPs reais, com a verificação pelo aplicativo ainda pendente.

A norma do aplicativo proíbe gravar dentro de cronômetro de tela, que só lê dados, e por isso o resfriamento ficou num fluxo agendado a cada cinco minutos. Três falhas ficaram registradas: o primeiro teste real do script acusou "Invalid array length", porque o ambiente compila para ES5, versão antiga do JavaScript; a execução agendada de 9 de outubro falhou por usar o nome de exibição de uma coluna, e não o interno; e uma integração publicada pela metade, com a extrusora na versão nova e a solda na antiga, perdeu a baixa de mandril.

[[FIGURA 6 | Fluxo da conferência diária GMS × SAP × Packing List | fig09_conferencia.png | Fonte: elaboração própria (2026).]]

### 4.3 Camada analítica e indicadores

A camada analítica segue o desenho do Apêndice A (Figura 10). Os indicadores entregues são tempo de ciclo por etapa e *lead time* da OP, ambos pela mediana, com percentil 90 no segundo; índice de gargalo, razão entre o trabalho em processo (*work in progress*, WIP) e a vazão recente; idade da OP na etapa; e o Hora-Hora. A mediana foi escolhida porque uma única OP com 4.162 horas na etapa distorce qualquer média. Em outubro de 2026 o relatório ganhou páginas de paradas, da Montagem e da Extrusora, e os 143 textos de motivo de parada digitados ao longo do tempo foram reduzidos a 44 motivos padrão, porque o número que os precedia era só a posição do item no menu da tela e mudou de sentido mais de uma vez. O dia produtivo do Hora-Hora no BI passou a ir das 05:20 às 05:20, como a base já grava, e foi conferido contra o rodapé do aplicativo numa máquina e num dia. A Figura 7 mostra a página de paradas do relatório, com o Pareto dos motivos padrão e o tempo parado por turno, em que o 3º turno quase não aparece, efeito da adesão discutida na seção 4.4.

Os primeiros meses de dado digital desmentiram números que a célula usava. Cerca de 20,5% do histórico do Hora-Hora havia sido medido contra velocidades teóricas não confirmadas, e a meta saía inflada em 4,9%, 5,0% e 14,3% nos três turnos, porque o fator da primeira janela era cobrado cheio em janelas mais curtas. Dos minutos de "parada" da Montagem, 74% eram tempo excedido, e o painel passou a mostrar os dois em cartões separados. Na Extrusora, a produção é medida em metros e o refugo é lançado em quilos, mas o percentual de refugo que existia no modelo somava as duas unidades; o indicador oficial passou a ser quilos de refugo por mil metros extrudados. Bianchini et al. (2024) derivam indicadores do dado que o MES coleta; o caso acrescenta que a definição de cada indicador também precisa ser conferida contra o chão de fábrica antes de entrar no painel.

[[FIGURA 7 | Página de paradas do relatório do GMS no Power BI | prints/bi_paradas.png | Fonte: elaboração própria (2026).]]

A comparação prometida no TCC I entre o ciclo medido e a estimativa histórica foi feita contra o tempo padrão de cada OP, a metragem da etapa dividida pela velocidade de delineamento da Engenharia, mesma base da meta do Hora-Hora. Na Tabela 1, de maio a outubro de 2026, sem as trançadeiras espirais e as de duas passadas, o ciclo medido fica de 55% a 114% acima do padrão na mediana, com cauda longa. A diferença não é só perda: o padrão conta a máquina na velocidade nominal, e o ciclo apontado inclui troca de carretel, ajuste, parada e atraso no apontamento, causas que a comparação não separa.

[[TABELA 1 | Mediana do ciclo medido no GMS e do tempo padrão por etapa (maio a outubro de 2026) | Fonte: elaboração própria (2026), com dados do GMS e do delineamento da Engenharia.]]

| Etapa | OPs | Ciclo (min) | Padrão (min) | Diferença | Razão ciclo/padrão (P90) |
|---|---|---|---|---|---|
| Tubo | 1.406 | 39 | 18 | +21 (+114%) | 2,15 (4,16) |
| Trançagem | 897 | 446 | 288 | +158 (+55%) | 1,77 (6,80) |
| Cobertura | 1.370 | 27 | 15 | +12 (+79%) | 1,76 (3,66) |

### 4.4 Testes e validação

A comparação entre papel e digital, primeira frente do Quadro 3, foi diária e qualitativa nos três meses de paralelo, até a retirada do papel em maio de 2026, e não contou divergências por campo. Ela revelou as primeiras classes de defeito do Quadro 5, a inversão de dia e mês, o fuso do *tenant* e o separador decimal, além de OPs sem correspondência no SAP, tratadas depois pela escolha da OP no plano (seção 4.1), e o papel saiu quando essas classes deixaram de aparecer. Das demais frentes, cinco têm a evidência nesta seção: a bateria de QA, a auditoria por tela, a conciliação com o SAP, a adesão e a acurácia; a medição contra a estimativa está na seção 4.3, e os indicadores do Kaizen, na 4.5.

[[QUADRO 5 | Classes de defeito encontradas na validação e tratamento adotado | Fonte: elaboração própria (2026).]]

| Classe de defeito | Tratamento adotado |
|---|---|
| Delegação silenciosa (soma parcial) | Cálculo materializado fora da consulta; avisos auditados |
| Cultura e separador decimal | Leitura sempre em en-US, exibição em pt-BR |
| Dia e mês invertidos em terminais com configuração regional divergente | Correção de configuração |
| Horário gravado no fuso padrão do *tenant* | Conversão de fuso |
| Tempo congelado e turno inconsistente | Turno carimbado no envio; fronteiras reunidas na seção de tempo do App.Formulas e repetidas na dimensão de turno do BI |
| Variável sem tipo definido | Padrão de inicialização com registro de referência |
| Concorrência de gravação | Gravação linha a linha, sem lote |
| Corrida entre carga e gravação (registro com a célula de outra máquina) | Célula, turno e data carimbados em cada linha; tela travada durante a carga |
| Filtro em Excel no servidor | Coleção local filtrada |

A leitura do ponto decimal pela cultura pt-BR do tablet inflou a meta em dez vezes até ser detectada. Na conciliação com o SAP, uma análise retrospectiva de agosto de 2026, feita antes do fluxo diário, encontrou contrapartida no ERP para 2.222 das 2.304 OPs do GMS (96,4%) e aderência de metragem de 83,4%, com 927.769 m no GMS contra 1.111.773 m no SAP. A mesma análise explica a maior parte da diferença de 184.004 m: 391 OPs estavam nos dois sistemas mas nunca tinham passado pela inspeção, que é de onde o GMS tira a metragem produzida, e carregavam 193.626 m no SAP. A ordem de grandeza confirma a hipótese no agregado, mas não OP a OP, pois há divergências individuais nos dois sentidos. Em setembro, cerca de 85% das OPs fecharam com diferença zero entre GMS, SAP e refugo, e a quantidade vazia caiu para 2 de 1.700 campos nas OPs finalizadas depois de 15 de setembro.

A conciliação também mostrou que a referência erra. Ao tratar lance a lance as OPs mais divergentes de maio a setembro de 2026, apareceram lances gravados na OP vizinha, no GMS e no SAP, refugo lançado em duplicidade e refugo lançado no ERP com o material errado. Depois de dois lotes de tratativas, a divergência somada em módulo no período caiu de 4.531,2 m para 2.975,4 m. No refugo, o que estava lançado errado no SAP entre 16 de maio e 16 de setembro somava 580,9 m em 39 materiais, apenas 0,10% dos 596.547 m de produção boa, mas cerca de 12% do refugo lançado. Como o inventário é controlado por material, a regra adotada soma o que faltou e o que sobrou separadamente, sem compensar um material com outro. Tomar o SAP como referência é, portanto, uma convenção da conferência, e não a garantia de que ele esteja certo.

A lista do Hora-Hora foi higienizada em outubro: dos 4.024 registros de 14 de setembro a 15 de outubro, 102 eram janelas duplicadas e 27 traziam a célula de outra máquina, efeito da corrida entre carga e gravação do Quadro 5. A adesão, que o TCC I propôs medir pela continuidade dos registros em todos os turnos, foi medida nessa lista, já sem as duplicatas. Das 225 combinações de máquina e dia com algum registro no período, o 1º turno registrou em 89%, o 2º em 82% e o 3º em 26%. O fechamento do turno, passo que confirma o registro, ocorreu em 58% dos turnos registrados do 1º, em 89% do 2º e em nenhum do 3º, e só 4,5% das janelas noturnas tinham parada apontada, contra cerca de 57% nos outros turnos. Parte da baixa cobertura noturna vem de máquinas que não trabalham no 3º turno, o que a auditoria do painel de TV também apontou, mas o fechamento ausente indica que a adesão é desigual entre os turnos e menor à noite. A ficha de produção, que não depende desse fechamento, não teve medida equivalente.

A acurácia frente ao evento físico foi estimada na única máquina com sensor de estado, uma trançadeira, de 1º a 15 de outubro de 2026. O sensor só distingue máquina ligada e desligada, sem motivo nem peça boa. Das 251 horas comparadas, 121 (48%) bateram com diferença de até cinco minutos. Nos turnos fechados, o total apontado ficou perto do medido, com 2.000 minutos contra 1.906 no 1º turno e 2.026 contra 2.151 no 2º, mas a distribuição por hora não fechou. As paradas longas foram confirmadas: em 34 das 43 horas com 45 minutos ou mais de parada apontada, o sensor viu 40 minutos ou mais. Escapam a parada curta, pois em 60 das 153 horas apontadas sem parada o sensor registrou dez minutos ou mais, e o 3º turno, sem nenhuma parada apontada nas 56 horas em que o sensor viu 979 minutos de máquina parada. Depois dessa comparação, o tempo parado deixou de ser digitado: desde 29 de outubro de 2026 a tela o calcula como a fração da janela que faltou para a meta, derivada da velocidade cadastrada da máquina, com o realizado lido no metrador. A Tabela 2 aplica essa regra às mesmas 251 horas e mede o erro médio absoluto por hora e o viés, diferença média entre sensor e GMS, positiva quando o GMS aponta menos parada. Nos turnos fechados as duas formas erram cerca de nove minutos por hora, com viés perto de zero; no 3º turno o erro caiu de 17,5 minutos, todos para menos, para 9,5. O erro restante vem da distribuição entre as horas e de o cálculo contar como parada a perda de velocidade, que o sensor de ligado e desligado não vê.

[[TABELA 2 | Erro médio absoluto e viés do tempo parado frente ao sensor, em minutos por hora (trançadeira, 1º a 15 de outubro de 2026) | Fonte: elaboração própria (2026), com dados do GMS e do sensor de estado.]]

| Grupo | Horas | Digitado: erro | Digitado: viés | Calculado: erro | Calculado: viés |
|---|---|---|---|---|---|
| 1º e 2º turnos fechados | 182 | 8,5 | +0,2 | 9,0 | +0,1 |
| 3º turno | 56 | 17,5 | +17,5 | 9,5 | +0,4 |
| Todas as horas | 251 | 11,2 | +4,9 | 10,4 | −1,3 |

Nos termos de Goknil et al. (2023), a cobertura de 96,4% e a quantidade vazia medem completude, a diferença zero contra o SAP mede consistência com a referência do projeto, e a comparação com o sensor é a primeira medida de acurácia, restrita a uma máquina e a quinze dias, com erro médio de cerca de nove minutos por hora.

### 4.5 Análise dos resultados

Os indicadores do Quadro 6 vêm do dossiê corporativo do Kaizen e não pesam igual. O dossiê não descreve o método; os valores relativos são estimativas da equipe do Kaizen, que informou o ponto de partida de dois deles: achar o lote de uma reclamação levava de um a dois dias nas fichas de papel, e digitalizar o dia anterior, cerca de quatro horas. O WIP visível passou de nenhuma etapa para todas. Por isso o quadro não traz colunas de antes e depois, e sim o que cada valor mede e a ressalva que o acompanha. Resposta a reclamação, consolidação de relatórios e WIP visível medem o acesso ao dado, que é onde o sistema atua. O escopo de contenção, entendido como o conjunto de lotes e ordens a segregar diante de uma reclamação de qualidade, depende da rastreabilidade por OP e por carretel. O dossiê estima ainda, sem auditoria independente, impacto de cerca de R$ 15,7 mil em qualidade, R$ 75,4 mil em entrega e produtividade e R$ 38,6 mil em custo da informação, valores convertidos do euro pela cotação PTAX de venda de 29 de outubro de 2026, de R$ 6,00 (BANCO CENTRAL DO BRASIL, 2026), com investimento de capital (*capital expenditure*, capex) zero, pois licenças e tablets já existiam. Do lado do papel, o levantamento do projeto estima em 336 kg por ano o consumo das fichas da célula, dos quais 80 kg já foram eliminados.

[[QUADRO 6 | Indicadores de resultado do GMS segundo o dossiê corporativo | Fonte: elaboração própria (2026), com base no dossiê corporativo.]]

| Indicador | Valor no dossiê | O que mede | Ressalva |
|---|---|---|---|
| Resposta a reclamação | 36 vezes mais rápida (de horas para minutos) | Acesso ao histórico da OP | Estimativa da equipe: de um a dois dias para achar o lote a minutos na consulta da OP; sem cronometragem |
| Escopo de contenção | 87,5% menor | Rastreabilidade por lote | Sem linha de base detalhada |
| Consolidação de relatórios | 97% menos horas | Custo da informação | Estimativa da equipe: cerca de 4 h por dia para digitalizar o dia anterior |
| WIP visível por etapa | De 0% para 100% das etapas | Visibilidade do estado da célula | Coerente com a fila por etapa (seção 4.1) |
| Produtividade por turno | +0,22% | Desempenho da célula | Marginal e não isolável de outras mudanças |

O ganho de produtividade, +0,22%, é marginal e não se isola de outras mudanças no período, e o dossiê registra também a eliminação de um erro de cerca de 14% na meta de produção, sem detalhar o método. Novochadlo e Paladini (2024) obtiveram aumento de 12,3% na eficiência média em sete meses com OEE em tempo real e ressalvam o prazo curto e a sazonalidade. Dalenogare et al. (2018) avaliam, em indústrias brasileiras, a contribuição esperada dessas tecnologias para o desempenho, e o +0,22% não confirma nem refuta essa expectativa. O que o estudo sustenta com dado próprio é o tempo de acesso: o apontamento fica na lista no instante do registro, e a conferência com o SAP passou a sair de terça a sábado. A resposta a reclamações em minutos é estimativa da equipe do Kaizen e não foi cronometrada. O efeito sobre as demais decisões não foi medido.

### 4.6 Interpretação: o regime informacional e a auditabilidade dos indicadores

Os três planos da seção 2.3 passam a ter evidência própria. No plano do tempo, o apontamento que levava de um a dois dias para chegar à supervisão fica disponível na lista no instante do registro e no painel de TV em até dois minutos, ciclo de recarga da tela, enquanto o Power BI segue o agendamento do conjunto de dados, limitado a oito atualizações por dia na capacidade compartilhada em que roda; esse intervalo, e não o volume de dados, é a marca da visibilidade operacional para Wu, Xu e Zheng (2024). No plano da conexão, a conferência com o SAP ligou o dado da célula ao ERP, e as divergências que restam viram item de tratativa com responsável.

O plano da visibilidade é o que os painéis de TV materializam. A Figura 8 mostra o painel da Célula numa tarde de outubro de 2026: cada etapa aparece com o estado, a OP em curso, a fila de carretéis e a metragem por turno, as onze trançadeiras trazem o tempo de autonomia ou o motivo da parada apontada no Hora-Hora, e o quadro "Onde olhar agora" reúne os alertas abertos em páginas, oito naquele momento, a primeira com três trançadeiras paradas por alimentação de fio. A ordem que antes ficou parada sem que ninguém percebesse passou a ser uma fila com idade, à vista em todas as etapas.

A Figura 9 mostra o painel da Montagem, criado na mesma rodada. As doze estações aparecem em cartões com o estado da ordem de trabalho e o tempo contra a meta, e o cabeçalho separa a parada real do tempo excedido, conforme a regra que proíbe somar os dois. Na leitura da figura, nenhuma estação estava parada de fato, mas havia 771 minutos acima da meta no turno, e o quadro "Onde olhar" apontava uma estação acima da meta e três sem ordem de trabalho aberta, a mais antiga havia 56 minutos. Antes dos painéis, a mesma informação exigia caminhar pela planta ou esperar o relatório do dia seguinte.

[[FIGURA 8 | Painel de TV da Célula | prints/painel_celula_v0.14.1.png | Fonte: elaboração própria (2026).]]

[[FIGURA 9 | Painel de TV da Montagem | prints/painel_montagem_v0.2.1.png | Fonte: elaboração própria (2026).]]

O TCC I não previa que o sistema fosse expor erros na definição dos próprios indicadores. Ao medir na origem, ele mostrou que o indicador de volume contava 8,3 vezes a saída real, porque o mesmo metro era somado em cada etapa. A meta inflada do Hora-Hora, a "parada" que era tempo excedido, o refugo da Extrusora que somava quilos com metros e os motivos numerados pela posição no menu, da seção 4.3, vêm da mesma raiz, e a aderência do 3º turno subiu de 75,1% para 85,9% só com a correção da meta. O mesmo vale para a qualidade: a taxa de refugo registrada mudou de patamar a partir de maio de 2026, mês da retirada do papel, e a análise feita até aqui não separa o quanto é mudança do processo e o quanto é registro mais completo. Segundo o dossiê corporativo, a célula só passou a confiar no sistema quando os números bateram com o que se via no chão.

### 4.7 Aderência ao modelo MESA-11

O Quadro 7 amplia o confronto do TCC I, cujo documento listava oito funções do modelo da MESA International (1997); a qualificação já usou as onze, e a coluna "TCC I" traz esse placar. Nenhuma função mudou de situação em relação ao TCC I. A análise de desempenho avançou, com as camadas Bronze, Prata e Ouro, o tempo de ciclo e o índice de gargalo, mas continua em expansão enquanto o OEE for calculado com velocidade cadastrada e a acurácia do Hora-Hora estiver conferida numa só máquina. Das onze funções, seis estão implementadas, uma em expansão, duas parciais e duas fora do escopo. O rastreamento mantém a ressalva da genealogia entre lotes, ainda proposta.

[[QUADRO 7 | Funções MESA-11 e cobertura no GMS (TCC I × TCC II) | Fonte: elaboração própria (2026), com base em MESA International (1997).]]

| Função (MESA-11) | TCC I | TCC II | Justificativa |
|---|---|---|---|
| Coleta e aquisição de dados | Implementada | Implementada | Apontamento por tablet e leitor de código de barras |
| Controle de documentos | Implementada | Implementada | Ficha digital e ficha técnica como dado mestre |
| Rastreamento e genealogia | Implementada | Implementada | Rastro por OP e carretel; genealogia N:N continua proposta |
| Gestão da qualidade | Implementada | Implementada | Inspeção, refugo tipificado, carta X̄-R da trançagem e conferência com o SAP |
| Gestão de processo | Implementada | Implementada | Estado da etapa derivado dos campos gravados e avanço da ordem entre estações |
| Despacho de unidades de produção | Implementada | Implementada | OP escolhida em lista sincronizada com o plano e liberada na fila da etapa |
| Análise de desempenho | Em expansão | Em expansão | Modelo estrela, ciclo e gargalo; OEE com velocidade cadastrada e Hora-Hora conferido numa só máquina |
| Alocação e status de recursos | Parcial | Parcial | Estado de cada máquina no painel de TV; status de manutenção das trançadeiras nunca gravado |
| Gestão de mão de obra | Parcial | Parcial | Operador e turno registrados; sem gestão de escala |
| Programação detalhada | Fora do escopo | Fora do escopo | Integração com o planejamento recolhida; sistema de programação avançada (*Advanced Planning and Scheduling*, APS) fica para depois |
| Gestão de manutenção | Fora do escopo | Fora do escopo | Depende de coleta automática nos níveis 1 e 2 |

### 4.8 Comparação com trabalhos relacionados

Além do posicionamento do Quadro 1, pesam duas diferenças. Heuer et al. (2024) e Michael e Wortmann (2024) descrevem o uso de *low-code* na manufatura sem relatar operação em três turnos com conciliação diária contra o ERP, e o GMS contornou com capex zero e desenvolvimento interno os obstáculos de orçamento e de transferência de tecnologia que Bianchini et al. (2024) apontam no MES das PMEs.

Em sentido inverso, o GMS fica atrás em dois pontos. Não mede a máquina, e por isso o OEE é calculado com velocidade cadastrada, ao passo que Tapia et al. (2024) e Novochadlo e Paladini (2024) partem de sinal de equipamento. Depende de uma pilha proprietária, enquanto Koprov e Starly (2025) usam protocolos abertos. Há, porém, um uso do sinal de máquina que esses trabalhos não exploram: no GMS, o único sensor disponível serviu para auditar o apontamento humano, e não para substituí-lo (seção 4.4). Entre os trabalhos consultados, nenhum relata a auditoria dos próprios indicadores da seção 4.6.

### 4.9 Replicação na planta de Forest City, Carolina do Norte (EUA)

A planta de Forest City é a próxima etapa e fica fora dos resultados; aqui se derivam da experiência brasileira os requisitos que ela terá de cumprir. A arquitetura em camadas e a bateria de QA não dependem do país, mas a norma escrita, hoje em português, precisará de versão em inglês. Mudam os pontos em que o Brasil mostrou defeito, listados no Quadro 8. Como visto na seção 2.6, traduzir rótulos não basta.

[[QUADRO 8 | Requisitos de adaptação para a planta de Forest City (EUA) | Fonte: elaboração própria (2026).]]

| Requisito | Origem no Brasil | Adaptação |
|---|---|---|
| Formato de data | Inversão de dia e mês em terminais com configuração regional divergente | Padrão mm/dd e leitura em formato fixo antes de gravar |
| Separador decimal | Valor 0,254 lido como 254 pela cultura do dispositivo | Leitura já fixa em en-US; exibição passa de pt-BR para en-US |
| Fuso horário | Horário gravado no fuso padrão do *tenant*; fuso fixo de -3 h no Office Script da conferência | Eastern Time, com horário de verão; fuso como parâmetro no aplicativo, no script e na camada Prata |
| Idioma | Rótulos, norma e motivos de parada em português | Interface e motivos de parada em inglês; norma escrita traduzida |
| Unidades | Metros nas fichas e na conferência | Possível uso de pés; conversão na entrada |
| Grade de turnos | Fronteiras nas fórmulas do app e, à parte, na dimensão de turno do BI, alinhadas à mão a cada mudança | Grade própria da planta, numa fonte única lida pelo app e pelo BI |
| Conferência com o ERP | Casamento diário GMS × SAP × *packing list* | Extração do ERP da própria planta; categorias de divergência revistas se o fluxo de lançamento for outro |

### 4.10 Limitações do estudo

O estudo é de caso único, numa célula de uma planta. O autor desenvolveu, implantou e avaliou o sistema, papel duplo que favorece leituras benignas; o apoio em fontes que ele não produz, o SAP e o sensor, reduz esse viés sem eliminá-lo (seção 3.6). Há o acoplamento ao fornecedor, risco conhecido do *low-code* (BOCK; FRANK, 2021; LUO et al., 2021), que aparece nos limites de delegação e de itens do SharePoint, ultrapassados pelo Hora-Hora e motivo do pedido de migração para o Dataverse, a base de dados relacional da plataforma. Norma escrita e diário de decisões mitigam a dependência do autor, mas a dívida técnica das telas extensas permanece.

Quanto à evidência, a diferença de 16,6% na aderência de metragem tem ordem de grandeza compatível com as OPs sem inspeção, mas não foi confirmada OP a OP, e as conciliações vêm de janelas distintas. O OEE é simplificado porque a velocidade é cadastrada. A acurácia foi medida numa só máquina, por quinze dias, com um sensor que não distingue motivo, e a adesão por turno foi medida no Hora-Hora, e não na ficha de produção. A fronteira do 3º turno mudou duas vezes em outubro de 2026, e os registros gravados entre 22:20 e 22:40 nesse intervalo ainda levam o turno anterior. As comparações com o papel e com o tempo padrão não separam causas, e os indicadores do dossiê são estimativas da equipe; os valores monetários e a estimativa de papel não têm auditoria independente.

## 5. CONSIDERAÇÕES FINAIS

Dos objetivos específicos, a coleta foi concluída e o sistema foi validado contra o papel, o SAP e, numa máquina, o sensor de estado (seções 4.1 e 4.4). A orquestração e a análise entraram em operação; no fechamento, a conferência diária com o SAP rodava com o *packing list* registrado no próprio GMS, as tratativas das divergências antigas seguiam em curso e a lista do Hora-Hora estava higienizada de setembro a outubro, com o tempo parado calculado pela produção publicado em 29 de outubro (seções 4.2 a 4.4). A comparação consta na seção 4.8, e a preparação da replicação ficou nos requisitos do Quadro 8, sem implantação. O objetivo geral foi atendido em parte: o dado chega à lista no instante do registro e ao painel de TV em até dois minutos, mas o Power BI depende do agendamento do conjunto de dados, e a adesão do 3º turno ao registro horário ainda é baixa.

Na prática, o sistema foi implantado sem investimento de capital, e os ganhos que o dossiê corporativo declara, como a resposta 36 vezes mais rápida às reclamações e o +0,22% de produtividade, ficam com a ressalva de método da seção 4.5. A contribuição metodológica é manter um sistema *low-code* com disciplina de software, com diário de decisões (WEINREICH; GROHER; MIESBAUER, 2015) e uma bateria de testes que se aproxima, em escala pequena, da integração contínua (HILTON et al., 2016). A conceitual é a lente do custo da informação, que levou à auditoria dos próprios indicadores da seção 4.6, e a prática de conferir o apontamento humano contra fontes que o operador não controla, o ERP e o sinal da máquina, que mostrou onde o registro é confiável, nas paradas longas e nos turnos fechados, e onde não é, na parada curta e no turno da noite, em que o cálculo do tempo parado pela produção reduziu o erro de 17,5 para 9,5 minutos por hora.

Na própria célula, ficam por fazer a medida de adesão na ficha de produção, a comparação com sensor em outras máquinas e o acompanhamento do 3º turno. Os demais trabalhos futuros começam em Forest City, onde a replicação exige internacionalização planejada e testada, e não só tradução de rótulos (ALAMEER; HALFOND, 2016; COUTO; MIRANDA; CARTAXO, 2026), com os requisitos do Quadro 8. O crescimento dos dados e a migração para o Dataverse pedem um *pipeline* que escale (HELU et al., 2020). Ficam ainda a programação detalhada, a coleta automática de máquinas nos níveis 1 e 2 da ISA-95 (LU; XU; WANG, 2020; TAPIA et al., 2024), a genealogia N:N (ABDEL-ATY; NEGRI, 2024), as funções de IA da plataforma, o modo *offline* e a integração direta com o ERP.

Retomando a tese, o GMS não substituiu uma folha de papel, mas a forma como a célula acessa informação sobre si mesma. Gerou também informação derivada que o papel não comportava, como a idade da OP na etapa, mas não criou o dado de origem: reduziu-se a quase nada o custo de acessá-lo.

## REFERÊNCIAS BIBLIOGRÁFICAS

ABDEL-ATY, T. A.; NEGRI, E. Conceptualizing the digital thread for smart manufacturing: a systematic literature review. *Journal of Intelligent Manufacturing*, [S.l.], v. 35, n. 8, p. 3629-3653, 2024. DOI: 10.1007/s10845-024-02407-1. Disponível em: https://doi.org/10.1007/s10845-024-02407-1. Acesso em: out. 2026.

AJIMATI, M. O.; CARROLL, N.; MAHER, M. Adoption of low-code and no-code development: a systematic literature review and future research agenda. *Journal of Systems and Software*, [S.l.], v. 222, art. 112300, 2025. DOI: 10.1016/j.jss.2024.112300. Disponível em: https://doi.org/10.1016/j.jss.2024.112300. Acesso em: out. 2026.

ALAMEER, A.; HALFOND, W. G. J. An empirical study of internationalization failures in the web. In: IEEE INTERNATIONAL CONFERENCE ON SOFTWARE MAINTENANCE AND EVOLUTION (ICSME), 2016, Raleigh. Proceedings [...]. [S.l.]: IEEE, 2016. p. 88-98. DOI: 10.1109/ICSME.2016.55. Disponível em: https://doi.org/10.1109/ICSME.2016.55. Acesso em: out. 2026.

ANSI/ISA-95.00.01-2010. *Enterprise-Control System Integration – Part 1: Models and Terminology*. Research Triangle Park: International Society of Automation, 2010. ISBN 978-1-936007-72-9.

ATKIN, D. et al. Organizational barriers to technology adoption: evidence from soccer-ball producers in Pakistan. *The Quarterly Journal of Economics*, Oxford, v. 132, n. 3, p. 1101-1164, 2017. DOI: 10.1093/qje/qjx010. Disponível em: https://doi.org/10.1093/qje/qjx010. Acesso em: out. 2026.

BANCO CENTRAL DO BRASIL. *Cotações e boletins*: taxa PTAX. Brasília, DF: BCB, 2026. Disponível em: https://www.bcb.gov.br/estabilidadefinanceira/historicocotacoes. Acesso em: 30 out. 2026.

BIANCHINI, A. et al. Manufacturing execution system application within manufacturing small-medium enterprises towards key performance indicators development and their implementation in the production line. *Sustainability*, Basel, v. 16, n. 7, art. 2974, abr. 2024. DOI: 10.3390/su16072974. Disponível em: https://doi.org/10.3390/su16072974. Acesso em: out. 2026.

BOCK, A. C.; FRANK, U. Low-code platform. *Business & Information Systems Engineering*, [S.l.], v. 63, n. 6, p. 733-740, 2021. DOI: 10.1007/s12599-021-00726-8. Disponível em: https://doi.org/10.1007/s12599-021-00726-8. Acesso em: out. 2026.

COUTO, M.; MIRANDA, B.; CARTAXO, B. A systematic mapping study on Localization (l10n) and Internationalization (i18n) testing. *Information and Software Technology*, [S.l.], v. 199, art. 108258, nov. 2026. DOI: 10.1016/j.infsof.2026.108258. Disponível em: https://doi.org/10.1016/j.infsof.2026.108258. Acesso em: out. 2026.

DALENOGARE, L. S. et al. The expected contribution of Industry 4.0 technologies for industrial performance. *International Journal of Production Economics*, [S.l.], v. 204, p. 383-394, out. 2018. DOI: 10.1016/j.ijpe.2018.08.019. Disponível em: https://doi.org/10.1016/j.ijpe.2018.08.019. Acesso em: out. 2026.

DI RUSCIO, D.; KOLOVOS, D.; DE LARA, J.; PIERANTONIO, A.; TISI, M.; WIMMER, M. Low-code development and model-driven engineering: two sides of the same coin? *Software and Systems Modeling*, [S.l.], v. 21, n. 2, p. 437-446, 2022. DOI: 10.1007/s10270-021-00970-2. Disponível em: https://doi.org/10.1007/s10270-021-00970-2. Acesso em: out. 2026.

FRANK, A. G.; DALENOGARE, L. S.; AYALA, N. F. Industry 4.0 technologies: implementation patterns in manufacturing companies. *International Journal of Production Economics*, [S.l.], v. 210, p. 15-26, abr. 2019. DOI: 10.1016/j.ijpe.2019.01.004. Disponível em: https://doi.org/10.1016/j.ijpe.2019.01.004. Acesso em: out. 2026.

GOKNIL, A.; NGUYEN, P.; SEN, S.; POLITAKI, D.; NIAVIS, H.; PEDERSEN, K. J.; SUYUTHI, A.; ANAND, A.; ZIEGENBEIN, A. A systematic review of data quality in CPS and IoT for Industry 4.0. *ACM Computing Surveys*, [S.l.], v. 55, n. 14s, p. 1-38, 2023. DOI: 10.1145/3593043. Disponível em: https://doi.org/10.1145/3593043. Acesso em: out. 2026.

GOMES, C. et al. Exploring key factors for implementing manufacturing execution systems (MES) within the framework of Industry 4.0 for small and medium-sized enterprises (SMEs) in the manufacturing sector. *Production*, São Paulo, v. 34, e20230085, 2024. DOI: 10.1590/0103-6513.20230085. Disponível em: https://doi.org/10.1590/0103-6513.20230085. Acesso em: out. 2026.

HAAG, S.; ECKHARDT, A. Shadow IT. *Business & Information Systems Engineering*, [S.l.], v. 59, n. 6, p. 469-473, 2017. DOI: 10.1007/s12599-017-0497-x. Disponível em: https://doi.org/10.1007/s12599-017-0497-x. Acesso em: out. 2026.

HELU, M. et al. Scalable data pipeline architecture to support the industrial internet of things. *CIRP Annals*, [S.l.], v. 69, n. 1, p. 385-388, 2020. DOI: 10.1016/j.cirp.2020.04.006. Disponível em: https://doi.org/10.1016/j.cirp.2020.04.006. Acesso em: out. 2026.

HEUER, M. et al. Description and typification of low-code use cases in manufacturing companies. In: IEEE INTERNATIONAL CONFERENCE ON INDUSTRIAL ENGINEERING AND ENGINEERING MANAGEMENT (IEEM), 2023, Singapura. Anais [...]. [S.l.]: IEEE, 2024. DOI: 10.1109/IEEM58616.2023.10438157. Disponível em: https://doi.org/10.1109/IEEM58616.2023.10438157. Acesso em: abr. 2025.

HILTON, M. et al. Usage, costs, and benefits of continuous integration in open-source projects. In: IEEE/ACM INTERNATIONAL CONFERENCE ON AUTOMATED SOFTWARE ENGINEERING (ASE), 31., 2016, Singapore. Proceedings [...]. [S.l.]: ACM, 2016. p. 426-437. DOI: 10.1145/2970276.2970358. Disponível em: https://doi.org/10.1145/2970276.2970358. Acesso em: out. 2026.

IMAI, M. *Gemba Kaizen: a commonsense approach to a continuous improvement strategy*. 2nd ed. New York: McGraw-Hill, 2012. ISBN 978-0-07-179035-2.

JESUS, C. et al. Impact of adopting industry 4.0 practices and technologies on time and motion study: a pilot study revealing efficiency gains in a multi-operation workstation. *Production & Manufacturing Research*, [S.l.], v. 13, n. 1, 2025. DOI: 10.1080/21693277.2025.2476436. Disponível em: https://doi.org/10.1080/21693277.2025.2476436. Acesso em: abr. 2025.

KAASINEN, E.; SCHMALFUSS, F.; ÖZTURK, C.; AROMAA, S.; BOUBEKEUR, M.; HEILALA, J.; HEIKKILÄ, P.; KUULA, T.; LIINASUO, M.; MACH, S.; MEHTA, R.; PETÄJÄ, E.; WALTER, T. Empowering and engaging industrial workers with Operator 4.0 solutions. *Computers & Industrial Engineering*, [S.l.], v. 139, art. 105678, 2020. DOI: 10.1016/j.cie.2019.01.052. Disponível em: https://doi.org/10.1016/j.cie.2019.01.052. Acesso em: out. 2026.

KOPROV, P.; STARLY, B. Industrial metaverse meets IIoT: low-code platforms for machine-to-machine and human-to-machine integration. *Manufacturing Letters*, [S.l.], v. 44, p. 1254-1265, ago. 2025. DOI: 10.1016/j.mfglet.2025.06.145. Disponível em: https://doi.org/10.1016/j.mfglet.2025.06.145. Acesso em: out. 2026.

KUSIAK, A. Smart manufacturing. *International Journal of Production Research*, [S.l.], v. 56, n. 1-2, p. 508-517, 2018. DOI: 10.1080/00207543.2017.1351644. Disponível em: https://doi.org/10.1080/00207543.2017.1351644. Acesso em: out. 2026.

LENG, J. et al. Industry 5.0: prospect and retrospect. *Journal of Manufacturing Systems*, [S.l.], v. 65, p. 279-295, out. 2022. DOI: 10.1016/j.jmsy.2022.09.017. Disponível em: https://doi.org/10.1016/j.jmsy.2022.09.017. Acesso em: out. 2026.

LI, Z.; AVGERIOU, P.; LIANG, P. A systematic mapping study on technical debt and its management. *Journal of Systems and Software*, [S.l.], v. 101, p. 193-220, mar. 2015. DOI: 10.1016/j.jss.2014.12.027. Disponível em: https://doi.org/10.1016/j.jss.2014.12.027. Acesso em: out. 2026.

LIN, C.-T. Blockchain-based shop floor control system for small and medium-sized enterprise evolution to industry 4.0. *Scientific Reports*, [S.l.], v. 15, 2025. DOI: 10.1038/s41598-025-13809-3. Disponível em: https://doi.org/10.1038/s41598-025-13809-3. Acesso em: maio 2026.

LU, Y.; XU, X.; WANG, L. Smart manufacturing process and system automation: a critical review of the standards and envisioned scenarios. *Journal of Manufacturing Systems*, [S.l.], v. 56, p. 312-325, jul. 2020. DOI: 10.1016/j.jmsy.2020.06.010. Disponível em: https://doi.org/10.1016/j.jmsy.2020.06.010. Acesso em: out. 2026.

LUO, Y. et al. Characteristics and challenges of low-code development: the practitioners' perspective. In: ACM/IEEE INTERNATIONAL SYMPOSIUM ON EMPIRICAL SOFTWARE ENGINEERING AND MEASUREMENT (ESEM), 15., 2021, Bari. Proceedings [...]. [S.l.]: ACM, 2021. p. 1-11. DOI: 10.1145/3475716.3475782. Disponível em: https://doi.org/10.1145/3475716.3475782. Acesso em: out. 2026.

MANTRAVADI, S.; SRAI, J. S.; MØLLER, C. Application of MES/MOM for Industry 4.0 supply chains: a cross-case analysis. *Computers in Industry*, [S.l.], v. 148, art. 103907, jun. 2023. DOI: 10.1016/j.compind.2023.103907. Disponível em: https://doi.org/10.1016/j.compind.2023.103907. Acesso em: out. 2026.

MARTIN, J. *Rapid Application Development*. New York: Macmillan, 1991. ISBN 978-0-02-376775-2.

MESA INTERNATIONAL. *MES Explained: a high level vision*. White Paper No. 6. Pittsburgh: MESA International, 1997.

MICHAEL, J.; WORTMANN, F. The potential of low-code development in the manufacturing industry. In: IEEE INTERNATIONAL CONFERENCE ON EMERGING TECHNOLOGIES AND FACTORY AUTOMATION (ETFA), 28., 2023, [S.l.]. Anais [...]. [S.l.]: IEEE, 2024. DOI: 10.1109/ETFA54631.2023.10275503. Disponível em: https://doi.org/10.1109/ETFA54631.2023.10275503. Acesso em: abr. 2025.

MIGUEL, P. A. C. et al. *Metodologia de pesquisa em engenharia de produção e gestão de operações*. 2. ed. Rio de Janeiro: Elsevier, 2012.

MITTAL, S. et al. A critical review of smart manufacturing & Industry 4.0 maturity models: implications for small and medium-sized enterprises (SMEs). *Journal of Manufacturing Systems*, [S.l.], v. 49, p. 194-214, out. 2018. DOI: 10.1016/j.jmsy.2018.10.005. Disponível em: https://doi.org/10.1016/j.jmsy.2018.10.005. Acesso em: out. 2026.

NAKAJIMA, S. *Introduction to TPM: Total Productive Maintenance*. Cambridge: Productivity Press, 1988. ISBN 978-0-915299-23-2.

NOVOCHADLO, Y. M.; PALADINI, E. P. The application of real-time overall equipment efficiency indicator in a medium-sized company. *Brazilian Journal of Operations & Production Management*, [S.l.], v. 21, n. 2, art. 2042, 2024. DOI: 10.14488/BJOPM.2042.2024. Disponível em: https://doi.org/10.14488/BJOPM.2042.2024. Acesso em: out. 2026.

SANTOS, J. et al. The iBPM lifecycle: integrating low-code and hyperautomation into business process management. *IEEE Access*, [S.l.], v. 13, 2025. DOI: 10.1109/ACCESS.2025.3564068. Disponível em: https://doi.org/10.1109/ACCESS.2025.3564068. Acesso em: abr. 2025.

SCHIRALDI, M. M.; VARISCO, M. Overall equipment effectiveness: consistency of ISO standard with literature. *Computers & Industrial Engineering*, [S.l.], v. 145, art. 106518, jul. 2020. DOI: 10.1016/j.cie.2020.106518. Disponível em: https://doi.org/10.1016/j.cie.2020.106518. Acesso em: out. 2026.

SCHOLTEN, B. *The road to integration: a guide to applying the ISA-95 standard in manufacturing*. Research Triangle Park: International Society of Automation, 2007. ISBN 978-0-9792343-8-5.

SILVA, A. et al. Democratizing digital transformation: a multisector study of low-code adoption patterns, limitations, and emerging paradigms. *Applied Sciences*, [S.l.], v. 15, n. 12, p. 6481, 2025. DOI: 10.3390/app15126481. Disponível em: https://doi.org/10.3390/app15126481. Acesso em: abr. 2025.

SPEICHER, T. L. et al. Preparing for the digital transformation of a production shop floor. *Journal of Manufacturing and Materials Processing*, Basel, v. 10, n. 7, art. 257, jul. 2026. DOI: 10.3390/jmmp10070257. Disponível em: https://doi.org/10.3390/jmmp10070257. Acesso em: out. 2026.

TABIM, V. M. et al. Implementing manufacturing execution systems (MES) for Industry 4.0: overcoming buyer-provider information asymmetries through knowledge sharing dynamics. *Computers & Industrial Engineering*, [S.l.], v. 196, art. 110483, out. 2024. DOI: 10.1016/j.cie.2024.110483. Disponível em: https://doi.org/10.1016/j.cie.2024.110483. Acesso em: out. 2026.

TAO, F.; QI, Q.; LIU, A.; KUSIAK, A. Data-driven smart manufacturing. *Journal of Manufacturing Systems*, [S.l.], v. 48, p. 157-169, 2018. DOI: 10.1016/j.jmsy.2018.01.006. Disponível em: https://doi.org/10.1016/j.jmsy.2018.01.006. Acesso em: out. 2026.

TAPIA, E. et al. Implementation of a scalable platform for real-time monitoring of machine tools. *Computers in Industry*, [S.l.], v. 155, art. 104065, fev. 2024. DOI: 10.1016/j.compind.2023.104065. Disponível em: https://doi.org/10.1016/j.compind.2023.104065. Acesso em: out. 2026.

VENKATESH, V.; THONG, J. Y. L.; XU, X. Unified theory of acceptance and use of technology: a synthesis and the road ahead. *Journal of the Association for Information Systems*, [S.l.], v. 17, n. 5, p. 328-376, 2016. DOI: 10.17705/1jais.00428. Disponível em: https://doi.org/10.17705/1jais.00428. Acesso em: out. 2026.

WAN, P. K.; LEIRMO, T. L. Human-centric zero-defect manufacturing: state-of-the-art review, perspectives, and challenges. *Computers in Industry*, [S.l.], v. 144, art. 103792, jan. 2023. DOI: 10.1016/j.compind.2022.103792. Disponível em: https://doi.org/10.1016/j.compind.2022.103792. Acesso em: out. 2026.

WEINREICH, R.; GROHER, I.; MIESBAUER, C. An expert survey on kinds, influence factors and documentation of design decisions in practice. *Future Generation Computer Systems*, [S.l.], v. 47, p. 145-160, jun. 2015. DOI: 10.1016/j.future.2014.12.002. Disponível em: https://doi.org/10.1016/j.future.2014.12.002. Acesso em: out. 2026.

WOMACK, J. P.; JONES, D. T. *Lean Thinking: banish waste and create wealth in your corporation*. New York: Simon & Schuster, 1996. ISBN 978-0-7432-4927-0.

WU, K.; XU, J.; ZHENG, M. Industry 4.0: review and proposal for implementing a smart factory. *The International Journal of Advanced Manufacturing Technology*, [S.l.], v. 133, p. 1331-1347, 2024. DOI: 10.1007/s00170-024-13839-7. Disponível em: https://doi.org/10.1007/s00170-024-13839-7. Acesso em: maio 2026.

XU, L. D.; XU, E. L.; LI, L. Industry 4.0: state of the art and future trends. *International Journal of Production Research*, [S.l.], v. 56, n. 8, p. 2941-2962, 2018. DOI: 10.1080/00207543.2018.1444806. Disponível em: https://doi.org/10.1080/00207543.2018.1444806. Acesso em: out. 2026.

## APÊNDICE A – ARQUITETURA DE DADOS

[[FIGURA 10 | Arquitetura analítica em camadas e modelo estrela | fig11_bi.png | Fonte: elaboração própria (2026).]]

## APÊNDICE B – INVENTÁRIO DE TELAS

O Quadro 9 lista dez telas principais do GMS, entre as cerca de 30 do aplicativo, com a função e o tamanho em linhas de YAML na versão vigente no fim de outubro de 2026.

[[QUADRO 9 | Inventário das principais telas do GMS | Fonte: elaboração própria (2026).]]

| Tela | Função | Linhas de YAML |
|---|---|---|
| Painel da Célula | Painel de gestão para TV, com alertas derivados do dado | 7.663 |
| Trançagem | Apontamento da etapa de trançagem | 5.076 |
| Tubo | Apontamento da etapa de tubo, com OP escolhida do plano e cancelamento | 4.521 |
| Mandril | Apontamento da etapa de mandril e estado dos carretéis | 3.975 |
| Finalização | Fechamento da OP, *packing list* por pallet e código de barras | 3.593 |
| AM-DM-02 | Carta de controle X̄-R da trançagem, com foto do contador de *picks* | 2.906 |
| Hora-Hora da Trançagem | Registro de motivo e ação por janela, com meta derivada | 2.866 |
| Painel da Montagem | Painel de gestão da Montagem para TV | 2.496 |
| Consulta de OP | Histórico e estado de uma OP; reimpressão do *packing list* | 1.707 |
| Tratativa da Conferência | Tratamento das divergências GMS × SAP × *packing list* | 1.115 |
