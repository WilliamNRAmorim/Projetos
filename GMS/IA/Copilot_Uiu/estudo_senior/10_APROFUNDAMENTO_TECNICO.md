# Aprofundamento em integração produto e estatística

Complemento do estudo de 09/11/2026. As referências desta seção foram abertas após a primeira consolidação.

## 1. Caminho técnico de integração SAP

A Microsoft documenta conectores SAP ERP e SAP OData. O primeiro usa chamadas RFC/BAPI e componentes de integração com o SAP. O segundo depende de serviços OData disponíveis no sistema. O caminho precisa ser escolhido com a equipe SAP a partir da versão instalada, serviços liberados, autenticação e infraestrutura. [Opções de conexão](https://learn.microsoft.com/en-us/power-platform/sap/connect/connect-power-platform-and-sap)

A arquitetura de referência mostra o fluxo entre Power Platform, conector, gateway e SAP. As autorizações do sistema SAP continuam relevantes. A documentação também apresenta alternativas e suas limitações. [Arquitetura SAP](https://learn.microsoft.com/en-us/power-platform/architecture/reference-architectures/arch-pattern-sap)

Proposta de levantamento para o Uiu

| Pergunta de implantação | Decisão que permite tomar |
|---|---|
| Qual sistema, mandante e centro? | Fixar o escopo correto |
| Qual API aprovada fornece ordem/material/movimento? | Definir contrato estável de leitura |
| Qual identidade executa a consulta? | Aplicar autorização correspondente |
| A infraestrutura já existe? | Estimar esforço com TI |
| A fonte permite filtro e paginação? | Definir cobertura da consulta |
| Como estorno e alteração retroativa aparecem? | Atualizar indicadores corretamente |
| Qual atraso é aceitável? | Escolher consulta ao vivo ou fotografia |
| Qual ambiente permite testes? | Validar com dados controlados |

A proposta inicial é disponibilizar consultas de negócio estreitas para OP, material e movimentos. A extração deve retornar códigos de origem e manter o vínculo até documento/item. A documentação pública não confirma qual desses caminhos está disponível no tenant Danfoss.

## 2. Paginação SharePoint como requisito funcional

A orientação de Get items descreve retorno padrão limitado, Top Count, filtros de servidor e limitações em listas grandes. O limite de consulta, a paginação do fluxo e o limite de exibição da lista precisam ser tratados separadamente na configuração. O estudo recomenda testar o caso em que o registro desejado está além da primeira página. [Get items e Get files](https://learn.microsoft.com/pt-pt/sharepoint/dev/business-apps/power-automate/guidance/working-with-get-items-and-get-files)

Procedimento de verificação proposto

1. Criar uma fotografia de teste cujo total seja conhecido.
2. Colocar registros elegíveis no início, meio e fim da sequência.
3. Executar a consulta com o filtro real.
4. Conferir IDs retornados, quantidade de páginas e total.
5. Repetir com uma página falhando.
6. Repetir após inserção ou alteração concorrente.
7. Verificar se completo=true só aparece no caso íntegro.

Aumentar Top Count precisa ser acompanhado de medição de payload e tempo. O processamento de indicadores deve ser capaz de devolver evidência compacta ao agente.

## 3. Impulso temperatura e compatibilidade

O guia EC881 da Danfoss relaciona seleção de mangueira a pressão, impulso, temperatura, fluido, dimensão e aplicação. O ensaio de impulso caracteriza desempenho sob ciclos definidos. Seu resultado precisa ser interpretado junto das condições de ensaio e da especificação da família. Uma contagem de ciclos de laboratório não deve ser convertida diretamente em anos de serviço sem um modelo de vida validado. [Guia EC881](https://assets.danfoss.com/documents/latest/383156/AD480662588951en-000101.pdf)

Os dados técnicos Danfoss consultados destacam efeitos combinados de temperatura e pressão e compatibilidade dos materiais da mangueira, conexão e vedação. Aplicação proposta: o Uiu deve pedir a condição de aplicação e identificar cada material envolvido antes de produzir uma recomendação. [Dados técnicos Danfoss](https://assets.danfoss.com/documents/latest/284127/AF445763801901en-000101.pdf)

Proposta de formulário de aplicação

| Campo | Informação a registrar |
|---|---|
| Fluido | Designação completa, concentração e condição |
| Pressão | Contínua, transientes e perfil conhecido |
| Temperatura | Fluido, ambiente e extremos |
| Movimento | Frequência, plano de flexão e instalação |
| Geometria | Comprimento, raio, suportes e interferências |
| Ambiente | Abrasão, agentes externos e exposição |
| Conexão | Código, vedação, orientação e homologação |
| Objetivo | Vida requerida, norma e exigência do cliente |

A seleção final será feita com as fontes aprovadas da engenharia. O formulário serve para evitar conclusões baseadas em apenas um atributo.

## 4. Capacidade de processo com hipótese explícita

O NIST relaciona capacidade à comparação entre variação de processo sob controle e especificação. As expressões usuais de Cp e Cpk pressupõem condições estatísticas, incluindo o modelo de distribuição adequado. O Uiu precisa guardar o método de estimativa da dispersão e identificar limites unilaterais ou bilaterais. [Capacidade de processo NIST](https://www.itl.nist.gov/div898/handbook/pmc/section1/pmc16.htm)

Para especificação bilateral e método adequado, a relação usual é Cp = (USL − LSL)/(6σ), e Cpk considera a menor distância da média a um dos limites, dividida por 3σ. O valor de σ precisa vir do método aprovado para os dados. Uma mistura de produtos ou mudanças de processo pode invalidar a interpretação do índice.

A estabilidade deve ser examinada na sequência temporal. Médias e variâncias que mudam ao longo do tempo exigem investigação antes da conclusão de capacidade. [Estabilidade NIST](https://www.itl.nist.gov/div898/handbook/ppc/section4/ppc45.htm)

Exercício sintético para validar o cálculo do Uiu: USL=10, LSL=8, média=9 e σ=0,2 resultam em Cp e Cpk de aproximadamente 1,667. Se a média passar a 9,4 com o mesmo σ, Cp permanece aproximadamente 1,667 e Cpk passa a 1,0. O exercício testa a distinção entre dispersão e descentramento. Ele não define critério de aprovação de produto.

Proposta de resposta estatística

“Foi usada a revisão R da especificação, com N observações do produto P, no período D. O método de dispersão foi M. O resultado é X. A avaliação de estabilidade apresentou Y. A conclusão depende das hipóteses H e da validação do sistema de medição.”

Esse formato permite auditar a análise e revisar a conclusão quando a base de dados ou o método mudar.
