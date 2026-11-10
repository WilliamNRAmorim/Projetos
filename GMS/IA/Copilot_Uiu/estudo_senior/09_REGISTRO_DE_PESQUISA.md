# Registro de pesquisa e lacunas

Data de pesquisa, 09/11/2026. Foco solicitado por William, Uiu no Copilot Studio para manufatura, mangueiras hidráulicas, conjuntos, MES, SAP, qualidade e Danfoss.

## Método

Foram pesquisadas fontes primárias Microsoft Learn, Microsoft Power Platform, Danfoss/PowerSource, SAP Help, ISA, ISO e ASQ. Foram abertas páginas selecionadas, consultados trechos de catálogos e extraída uma transcrição oficial de vídeo. A síntese aplica as referências ao estado documentado do Uiu. O inventário 07 registra o grau de acesso de cada fonte.

A pesquisa produziu documentação e critérios de avaliação. O conteúdo técnico interno foi usado como contexto e identificado como regra local. As propostas novas estão descritas como propostas de projeto.

## Cobertura e aprofundamento

| Área | Material trabalhado | Aprofundamento ainda necessário |
|---|---|---|
| Copilot Studio | Orquestração, conhecimento, ferramentas, avaliação, mecanismos, ALM e telemetria | Conferir opções disponíveis no tenant |
| IA e análise | Instruções, especialização, Code interpreter e medição | Benchmark com Uiu real |
| Vídeos | Uma transcrição integral e descrições de materiais adicionais | Webinar sem transcrição e aulas autenticadas |
| Danfoss | Produto GH781-6, manual de prensa, catálogo e ementas | Família/região e revisão efetivamente usadas na planta |
| Engenharia | Modelo de conhecimento e investigação de falhas | Desenhos, receitas e homologações internas |
| Normas | Escopo e edição públicos de três referências ISO | Texto completo aplicável ao produto/cliente |
| MES e SAP | ISA-95 e referências de integração/genealogia SAP | Sistema real, APIs, regras e permissões da fábrica |
| Qualidade | SPC, FMEA, medição e proposta de rastreabilidade | Plano de controle e dados aprovados |
| Dados GMS | Regras e limites encontrados no pacote local | Fotografia atual e conferência no ambiente corporativo |

## Divergências encontradas

1. O resumo indexado de Agents overview descrevia quatro mecanismos, enquanto a página aberta descreveu três. A síntese usa a página aberta e evita fixar uma contagem como critério de arquitetura.
2. A FAQ antiga de orquestração encontrada na busca afirma suporte apenas ao inglês, enquanto documentação atual de avaliação trata múltiplos idiomas. Esse conflito impede usar o trecho antigo como prova de restrição atual. O comportamento em pt-BR será testado na configuração real.
3. O tutorial de avaliação usa Classification. A documentação atual descreve Custom. O recurso precisa ser localizado na experiência do Uiu.
4. O plano inicial do Uiu descreve Default. O registro de passagem posterior descreve DPS – Non Prod. Para o estado histórico, prevalece o registro posterior.
5. O Diário local principal está atrás do pacote recente importado de GMS/IA. O documento de normas do pacote contém decisões de 09/11 ausentes no Diário local. Essas decisões devem ser confirmadas na fonte vigente antes de mudar regra operacional.
6. A versão 2022 da ISO 18752 aparece em buscas, mas a página ISO aponta a edição 2025 como sucessora. A aplicabilidade contratual precisa considerar a revisão exigida pelo produto/cliente.
7. O plano de agregação sugere deduplicar por campos de negócio. A análise deste estudo identifica o risco de remover eventos legítimos coincidentes. A chave e a regra de decisão precisam de validação com IDs de origem.
8. O plano associa Code interpreter à resolução de agregados. A documentação evidencia que os dados devem ser fornecidos explicitamente. A extração completa continua sendo uma dependência.

## Itens necessários para fechar a competência de engenharia

- Catálogos e fichas aprovados das famílias prioritárias da planta.
- Desenhos de conjunto, lista de materiais e revisões.
- Especificações atuais de montagem por combinação e equipamento.
- Plano de controle, PFMEA/DFMEA e procedimentos de ensaio.
- Critérios de amostragem, aceitação e liberação.
- Histórico de não conformidades com causa confirmada.
- Dados de calibração e estudos do sistema de medição.
- Requisitos específicos de cliente.
- Política de uso dos documentos internos pelo agente.

## Questões para validar com os responsáveis durante a implementação

Qual é a fonte aprovada de especificação por produto? Quais dados são atuais e quais são exports históricos? Quem aprova revisão de norma e de procedimento? O Uiu seguirá restrito ao William? Qual sistema SAP e cenário de integração estão disponíveis? Qual conjunto de produtos será usado para o primeiro benchmark de engenharia?

Essas respostas devem ser coletadas na execução concreta. Elas não impedem o uso imediato desta pesquisa para organizar conhecimento e testar os comportamentos já disponíveis.

## Registro de entrega

Pacote criado em estudo_senior com referências, síntese, arquitetura, trilha e casos de avaliação. O agente publicado precisa passar por implementação e medição para demonstrar a evolução proposta. Este pacote é a base documental dessa evolução.

A documentação pública consultada continua sujeita a atualização. Ao retomar, confirmar a página oficial da capacidade a alterar e registrar a data da nova verificação.
