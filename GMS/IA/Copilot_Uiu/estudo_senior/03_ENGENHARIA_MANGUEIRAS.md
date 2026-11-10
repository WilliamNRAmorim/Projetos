# Engenharia de mangueiras hidráulicas e conjuntos montados

Pesquisa pública e proposta de organização do conhecimento do Uiu, 09/11/2026.

## 1. Organização do domínio

A base de engenharia deve ligar requisitos de aplicação, família de mangueira, dimensão, reforço, materiais, terminal, processo de montagem, ensaios e rastreabilidade. A seleção de uma mangueira depende do código exato e das condições de aplicação.

A ficha pública GH781-6 da Danfoss identifica construção com duas tranças de arame, tubo NBR e atributos de pressão e raio de curvatura. É um exemplo de registro específico por código. Para o Uiu, esses atributos devem ser recuperados por item e acompanhados da revisão, em vez de generalizados para toda a família GH781. [Danfoss PowerSource GH781-6](https://powersource.danfoss.com/products/p/GH781-6)

## 2. Registro de produto proposto

| Grupo | Campos necessários |
|---|---|
| Identidade | Código SAP, código comercial, descrição, família, bitola, revisão e mercado |
| Construção | Tubo, reforço, cobertura, camadas e norma declarada |
| Aplicação | Fluido, faixa térmica, pressão contínua, transientes, ambiente e movimento |
| Geometria | Diâmetro interno/externo, tolerância, comprimento e raio mínimo |
| Conexões | Terminal, rosca, vedação, orientação e combinação homologada |
| Montagem | Máquina, ferramental, ajuste aprovado, diâmetro e método de medição |
| Validação | Plano de ensaio, relatório, amostragem, aceite e responsável |
| Rastreabilidade | Lotes de materiais, lote produzido, conjunto, inspeção e expedição |

Campos ausentes são pendências do cadastro. O Uiu deve solicitar a informação necessária para uma conclusão técnica, mantendo o restante do trabalho documentado.

## 3. Normas verificadas

| Referência | Escopo público conferido | Aplicação ao conhecimento |
|---|---|---|
| ISO 18752:2025 | Mangueiras e conjuntos reforçados, classes de pressão | Identificar classe, grau, tipo e edição aplicável |
| ISO 6605:2017 | Métodos de ensaio para mangueiras e conjuntos hidráulicos | Ligar ensaio ao requisito específico do produto |
| ISO 4413:2010 | Regras gerais e segurança de sistemas hidráulicos | Contextualizar instalação e sistema |

A página ISO informa que a edição 2025 da ISO 18752 substitui a de 2022. O resumo também relaciona a pressão máxima do conjunto à menor pressão admissível de seus componentes. Essa regra exige verificar a compatibilidade e a homologação do conjunto, além das condições reais de aplicação. Os resumos públicos consultados cobrem escopo e edição. Critérios de aceitação por produto precisam da documentação completa aplicável. [ISO 18752](https://www.iso.org/standard/89310.html) · [ISO 6605](https://committee.iso.org/standard/67357.html) · [ISO 4413](https://www.iso.org/standard/44781.html)

Referências adicionais citadas em catálogos ou na família normativa incluem ensaio hidrostático, impulso, dimensões, envelhecimento e compatibilidade com fluidos. A edição e a aplicabilidade de cada uma devem ser conferidas antes de incluir parâmetros na base do Uiu.

## 4. Conhecimento por etapa da fábrica

A sequência abaixo vem do GMS local. Os campos sugeridos são uma proposta de levantamento com engenharia e qualidade.

| Etapa | Conhecimento que o Uiu precisa | Evidência para investigação |
|---|---|---|
| Mandril | Código, dimensão, lote e condição | Inspeção e rastreio do mandril |
| Tubo | Material, dimensão e especificação | Lote de composto, medições e receita vigente |
| Trançagem | Construção do reforço e configuração aprovada | Máquina, material, turno e registros de processo |
| Cobertura | Material e requisito dimensional | Lote, medições e ocorrências |
| Bandagem | Material e método previsto | Lote e condição do processo |
| Vulcanização | Receita aprovada e identificação da carga | Curva do ciclo e rastreabilidade da batelada |
| Debandagem | Critérios de integridade | Inspeção visual e ocorrências |
| Extração e teste | Procedimento e aceite do produto | Resultado, equipamento e calibração |
| Montagem | Corte, preparo, terminal, prensagem e identificação | Ordem do conjunto, receita e medição final |

A hipótese de defeito deve conectar a etapa que gerou a condição à etapa que a detectou. A data da inspeção pode ser posterior à operação causal. O Uiu precisa preservar ambas.

## 5. Conjuntos montados

A base deve conectar desenho do conjunto, lista de materiais, revisão do terminal e procedimento da prensa. O manual ET1187 da Danfoss direciona a montagem ao ferramental e às especificações apropriadas. A especificação de máquina e de combinação mangueira-terminal precisa acompanhar a consulta. [Manual Danfoss ET1187](https://assets.danfoss.com/documents/latest/284550/AQ435956054218en-000202.pdf)

Proposta de roteiro informacional para o agente

1. Identificar o conjunto e a revisão do desenho.
2. Recuperar mangueira e terminais exatos da lista de materiais.
3. Conferir a combinação homologada.
4. Recuperar procedimento de montagem e ferramental aplicável.
5. Conferir registros dimensionais e de preparação.
6. Recuperar ensaios e inspeções exigidos.
7. Verificar marcação, lote e liberação documentada.

O Uiu deve recuperar valores de crimpagem de fonte aprovada. Interpolar valores entre bitolas, copiar o ajuste de outra prensa ou escolher um terminal pela semelhança visual produz uma especificação sem base suficiente.

## 6. Pressão e desempenho

Pressão de trabalho, pressão de ensaio e pressão de ruptura têm funções distintas na especificação. A resposta deve nomear a grandeza e sua condição. Uma pressão de ruptura de catálogo não autoriza elevar a pressão de serviço.

Para avaliar uma aplicação, registrar pressão contínua e transientes, fluido, temperatura, movimento, raio, abrasão, terminais e vida requerida. A pressão nominal isolada é insuficiente para homologar uma aplicação. O parecer final precisa referenciar a especificação da combinação e os requisitos do cliente. [Catálogo Danfoss](https://assets.danfoss.com/documents/latest/469618/AF493753346832en-020102.pdf)

## 7. Limpeza e preservação

O catálogo Danfoss inclui limpeza, inspeção, teste e armazenamento. O Uiu deve consultar a instrução aplicável ao produto e ao cliente para orientar critérios de limpeza e preservação. Procedimentos de ensaio devem ser executados com equipamento e proteção previstos pela engenharia. O agente deve apontar documento e responsável quando faltarem condições seguras ou especificação. [Catálogo Danfoss, seções de limpeza e teste](https://assets.danfoss.com/documents/latest/469618/AF493753346832en-020102.pdf)

Cadastro proposto de qualidade do conjunto: método de limpeza, critério de contaminação, inspeção visual, vedação de extremidades, identificação, embalagem, condição de armazenamento e liberação.

## 8. Diagnóstico técnico com evidência

| Sintoma | Hipóteses para investigar | Evidências discriminantes |
|---|---|---|
| Vazamento junto ao terminal | Combinação, montagem, dimensão, inserção ou carga externa | Código, revisão, medida, ferramenta, fotos e histórico |
| Falha localizada na curva | Geometria instalada, movimento ou dano local | Roteamento, raio documentado, marcas e montagem |
| Bolha ou separação de camadas | Material, processo ou condição de uso | Lotes, ciclo, seção examinada e ensaio técnico |
| Diâmetro variável | Processo, material ou medição | Série temporal, instrumento e condições da linha |
| Falha em impulso | Produto, montagem, aplicação ou condição do ensaio | Relatório completo e parâmetros registrados |
| Contaminação interna | Corte, preparo, limpeza ou armazenamento | Inspeção e rastreabilidade dos passos |

Essas linhas são um roteiro de investigação proposto. O sintoma sozinho não determina a causa. Cada diagnóstico deve guardar hipótese, evidência favorável, evidência contrária, teste necessário e responsável pela decisão.

## 9. Danfoss e formação técnica

O catálogo de treinamento EMEA 2025 identifica Anatomy of a Hydraulic Hose, Fluid Conveyance Product Overview, RHHF e Hose Routing, Installation & Failure Analysis. A trilha é uma referência para estruturar o conhecimento do Uiu em fundamentos, produto, aplicação e falhas. Datas, preço, elegibilidade e disponibilidade dos cursos precisam ser consultados para a região atual. [Catálogo de cursos Danfoss](https://assets.danfoss.com/documents/latest/465902/AD513070919216en-000102.pdf)

A formação prática de montagem e avaliação de falhas exige os materiais e exercícios aprovados da Danfoss. Nesta pesquisa foram consultados documentos públicos e ementas. Receitas industriais, desenhos de clientes e procedimentos internos permanecem entradas necessárias para completar o conhecimento específico da planta.
