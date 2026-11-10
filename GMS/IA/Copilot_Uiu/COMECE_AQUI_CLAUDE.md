# Claude — começar aqui em 10/11/2026

Passagem preparada em 09/11/2026, horário de Brasília. Objetivo: executar a evolução do Uiu conforme o GMS, aproveitando o planejamento existente e evitando retrabalho. Não reiniciar a pesquisa nem criar outra lista de 50 melhorias.

## Pedido pronto para William usar

> Leia GMS/IA/Copilot_Uiu/COMECE_AQUI_CLAUDE.md e os quatro documentos de planejamento indicados. Execute os pacotes na ordem de dependência, começando por E0, e avance nos que estiverem desbloqueados. Preserve as decisões aprovadas do GMS. Consulte documentos e dados antes de me perguntar; apresente apenas ambiguidades reais, com evidência. Diferencie preparado, implementado, testado e publicado. Não marque gap resolvido sem prova.

## 1. Ler nesta ordem

Cumprir também as instruções aplicáveis do repositório e de GMS/CLAUDE.md.

1. [Plano vigente](PLANO_EXECUCAO_GMS.md): escopo, E0–E6, fases F0–F5 e critérios de avanço.
2. [Gaps e decisões](planejamento/GAPS_E_DECISOES.md): G01–G30, decisões D01–D09 e destinação das 50 propostas.
3. [Contratos e métricas](planejamento/CONTRATOS_E_METRICAS.md): fontes, identidades, datas, cálculos, atualização e Mecânico.
4. [Execução e aceite](planejamento/EXECUCAO_E_ACEITE.md): tarefas por pacote, 36 casos adicionais, uso dos 60 existentes e recuperação.

[PLANO_UIU.md](PLANO_UIU.md) e [PROXIMA_SESSAO.md](PROXIMA_SESSAO.md) preservam o histórico e as decisões anteriores. Não executar isoladamente suas instruções antigas. O estudo_senior é referência, não backlog obrigatório.

## 2. O que realmente foi feito

- Revisão documental do plano, 30 gaps mapeados, nove decisões pendentes e contratos definidos como proposta de implementação.
- Quatro documentos de planejamento gravados e entradas dos dois arquivos antigos apontando para o plano vigente.
- Verificação documental aprovada em 11 checagens: links, identificadores, cobertura das 50 propostas e preservação da bateria existente. Resultado em [VERIFICACAO_DOCUMENTAL.json](planejamento/VERIFICACAO_DOCUMENTAL.json).
- Nenhuma melhoria desta revisão foi implantada no tenant. Nenhum dos 36 testes adicionais foi executado no agente. Os 60 casos anteriores também não têm execução comprovada por esta revisão.
- Não houve revisão independente por outro agente. Não confundir os dois testes pontuais históricos com aceite da nova versão.
- Para usar em outro PC, atualizar o repositório e verificar que esta passagem e seus quatro documentos de planejamento estão presentes na revisão obtida. Não executar uma cópia antiga que contenha somente PLANO_UIU.md. A presença no outro PC precisa ser conferida mesmo depois do envio ao GitHub.

## 3. Começar a execução

**E0:** conferir o Uiu no DPS - Non Prod, ambiente `8944b737-0def-e6f9-93c8-840d950e5e44`, bot `dd8888ce-de52-4f4a-be5f-1a2109a461cf`. Registrar estado vivo, configuração recuperável, rascunho versus publicado, ferramentas, conexões e identidade. O Default antigo é cópia histórica; não alterar por engano.

Não assumir login disponível. Se depender da entrada corporativa de William, continuar as tarefas locais independentes enquanto esse acesso fica pendente. Não reutilizar conclusões sobre limitações de ferramentas de outra sessão sem verificar os recursos atuais.

**E0/E1:** conciliar fontes: Diário local termina em 06/11, mas o conhecimento contém decisões de 09/11. Não regenerar o conhecimento pelo Diário incompleto nem reservar MEL com base nessa cópia desatualizada.

**E1/E2:** preparar a primeira métrica, refugo registrado na TiposErros, e sua prova de extração. Confirmar campos, identidade, data, unidade, cobertura e vínculo com produto; preparar gabarito independente. D09 bloqueia certificação do ranking temporal se a evidência não resolver a regra.

**E3:** entregar o Top 10 anual por mangueira/trançadeira no Uiu, depois de provar cálculo completo e testar no Studio e no Teams. Avançar para E4–E6 conforme as dependências, sem aguardar decisões de domínios que não afetem o pacote atual.

## 4. Pontos que não podem virar suposição no código

- TiposErros não representa sozinho todo o refugo consolidado K10.
- OP não é chave primária da ficha; uma junção pode multiplicar refugo.
- Dois IDs de refugo semelhantes não são duplicata confirmada.
- recurso do evento indica trançadeira de origem, não necessariamente máquina da etapa.
- Parcial e ausência de apontamento posterior não comprovam conclusão da etapa.
- Cancelamento não autoriza zerar indiscriminadamente Fim de etapas anteriores.
- Data efetiva da mudança de turno, data da inspeção e estimativa de janelas exigem as decisões indicadas no plano.
- Code Interpreter e Top Count alto não comprovam leitura completa.
- Não prometer consistência transacional entre listas só porque existe snapshot_id.
- F3 continua prevista: habilitar cada receita somente com pré-condições, confirmação vinculada, guarda de versão, auditoria e releitura.

## 5. Como terminar cada pacote

Registrar o que mudou, fontes/versões, testes realmente executados e resultados, pendências, estado de publicação e próxima ação. Guardar evidências e versão recuperável. Atualizar o estado sem apagar o histórico; integrar as linhas de Diário preparadas somente após conciliar sua versão.

Não garantir ausência de erros. Demonstrar o resultado pelos critérios de aceite e interromper apenas o passo que dependa de informação, acesso ou decisão ainda ausente.
