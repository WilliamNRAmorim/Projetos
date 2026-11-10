# Contratos de dados, métricas e correções

Versão 2.0 · 09/11/2026 · projeto lógico a validar em E1/E2. Não é schema já criado no SharePoint nem pacote importável do Power Automate.

Relacionado ao [plano](../PLANO_EXECUCAO_GMS.md) e aos [gaps](GAPS_E_DECISOES.md). Campos e regras devem ser conferidos na origem antes da implementação; os nomes abaixo vêm do mapa de 09/11.

## 1. Identidades e fontes

| Fonte | Identidade/grão a preservar | Campos documentados relevantes | Não presumir |
|---|---|---|---|
| ficha_producao | Site + lista + ID; uma ficha/OP/lote | OP, Mangueira, field_12 (lote), field_10 (etapa), field_11 (situação), Tran_x00e7_adeira | OP única em toda a lista |
| Eventos_Producao | Site + lista + ID; um evento | origem, origem_ID, etapa, tipo, data_hora, data_ref, turno, metros, refugo, sobra, recurso | origem_ID sozinho identifica a lista; recurso é máquina da etapa |
| Hora-Hora | ID da linha; chave de janela a validar: data de referência + turno + célula + Hora | field_0, field_2, field_3, field_4, field_5, field_7, field_11, field_12, TurnoH, Status, Minutos | Rótulo da Hora representa literalmente o começo atual; acumulados são valores por janela |
| RegistrosInspeção | ID da medição | OP_ID, Quantidade_Inspe_x00e7__x00e3_o, DataHoraInspecao, TurnoTeste, Mangueira, Tran_x00e7_adeira, cabine_teste; Created de sistema | Data do cadastro e data da inspeção são equivalentes |
| TiposErros | ID da linha na fonte viva | A, _x0043_, OP_ID, OP_refugo, ID_RegistroInspecao, DataHoraRefugo, Tran_x00e7_adeira, TurnoErro | OP+erro+quantidade+data prova duplicidade |
| MB51 | Sistema/mandante + ano do documento + documento + item, conforme disponibilidade do export | order, material, movement_type, quantity, unit_of_entry, user_name, posting_date | Item sozinho é único; arquivo contém período completo |
| Packing | ID + slice no arquivo de origem | pn, qtd_m, cancelled | ID/slice se liga ao ID de outra lista |

Para eventos ligados à ficha usar `origem = ficha_producao` e `origem_ID = ID`. Para refugo e inspeção ligados por OP, conferir quantas fichas candidatas existem. Se várias apontarem o mesmo produto validado, deduzir uma dimensão produto única sem replicar o fato; se conflitarem, marcar vínculo ambíguo. Um valor sem produto pode compor um total da fonte, mas não um ranking por produto certificado sem expor sua exclusão e quantidade.

Não usar o campo `recurso` para atribuir produção de Tubo, Bandagem ou outra etapa à trançadeira de origem. “Máquina da etapa”, “trançadeira de origem” e “cabine de teste” são dimensões distintas. Se a etapa não tiver máquina identificável, oferecer o agregado da etapa e informar a dimensão indisponível.

## 2. Tipos e tempo

- Adaptadores separados para API viva e cada formato de export. A cultura faz parte do adaptador: `1,050` no export americano não é automaticamente `1,050` decimal brasileiro. Valores inválidos vão para pendência com ID, nunca para zero.
- Preservar valor bruto e normalizado no conjunto de auditoria. Quantidades e totais devem usar precisão decimal compatível com a origem. A tolerância de teste será a precisão aprovada, não uma porcentagem arbitrária para esconder diferenças.
- Instantes: armazenar UTC e converter com fuso explícito `America/Sao_Paulo` para aplicação da regra. O identificador de fuso da implementação pode diferir; provar a equivalência no conector usado.
- Datas já carimbadas como dia produtivo, como a Data do Hora-Hora, não recebem novamente o deslocamento de 05h20. Data de lançamento SAP segue seu próprio calendário de negócio.
- Períodos têm início inclusivo e fim exclusivo. Para dia produtivo D vigente: D 05h20 até D+1 05h20 local. Para uma data de referência já armazenada: selecionar a data D na convenção daquela fonte.
- Turno vigente documentado: T1 [05h20,13h57), T2 [13h57,22h20), T3 [22h20,05h20). Aplicação histórica depende de D01. Preservar `turno_gravado`, `turno_regra` e `regra_versao` quando houver recálculo aprovado.
- Entre 27 e 29/10, não afirmar a data exata da migração sem evidência. Antes de 05/10 também existem fronteiras diferentes. O formato do rótulo da janela não corrige o dado automaticamente.
- Não usar Modified como data de produção ou como mecanismo incremental nesta implementação: a documentação do GMS o proíbe. O reprocessamento inicial será por releitura das partições do período suportado. Um mecanismo futuro de captura de mudanças exige decisão específica.

## 3. Catálogo inicial de métricas

Cada registro do catálogo implementado terá: ID/versão, nome ao usuário, unidade, origem, grão, campo temporal, inclusão/exclusão, dimensões permitidas, precisão, proprietário e status de liberação. Os códigos abaixo são locais ao Uiu, não substituem K01–K20.

| Métrica | Cálculo e recorte | Fonte/tempo | Condição de liberação |
|---|---|---|---|
| U-REF-LINHA | Soma do refugo registrado na TiposErros; ranking só após agregar todos os fatos elegíveis | _x0043_; data efetiva de refugo e fallback a confirmar em amostra | E3; vínculos não multiplicam linhas; duplicados suspeitos visíveis; cobertura do período comprovada |
| U-REF-CONS | Refugo consolidado das origens de K10, sem misturar unidades nem sobreposição | Linha + bobinadeira + extrusora | E4 posterior; mapear primeiro unidade, identidade e sobreposição de cada origem |
| U-PROD-MANDRIL | Metros de Fim + Parcial conforme MEL-260; regras de cancelamento por indicador | Eventos; data_ref/data_hora e turno validados | D02; Fim pode conter ajuste com sinal; não usar quantidade atual da ficha reduzida por split como gabarito único |
| U-PROD-TRANC | Real da linha selecionada por janela segundo a regra publicada de MEL-263 | Hora-Hora field_7, data/turno da janela | Provar seleção da última linha e exceções; não somar field_8 acumulado; D04 para equivalência com estimativas do painel |
| U-PROD-EXTR | Soma das medições de inspeção elegíveis, sem somar novamente Fim da OP | RegistrosInspeção; campo temporal decidido em D03 | D02/D03; separar inspeção boa, reensaio/repetição e critério de elegibilidade a conferir |
| U-PROD-ETAPA | Soma dos eventos elegíveis por etapa, segundo política específica dessa etapa | Eventos por origem e ID de ficha | E4; confirmar deltas versus acumulados; não herdar a regra de Mandril sem prova |
| U-PROD-FINAL | Saída terminal elegível, contada uma vez | Indicador terminal aprovado | Não chamar soma de etapas de produção final; compatibilidade com K02 explicitada |
| U-REF-TAXA | Refugo / (bom + refugo), quando ambos pertencem ao mesmo processo e recorte | Duas bases compatíveis | Zero/vazio no denominador = indisponível; não calcular taxa de máquina com produção apenas da célula |
| U-HH-ADER | Real / meta aplicável; meta por janela e contexto de filtro | Hora-Hora e versão vigente da medida | Fator 1305/1440 só em HH Meta Útil/HH Aderência sem hora filtrada; não aplicar no OEE2 |
| U-TEMPO | Totais separados por classe de perda e origem do tempo | Hora-Hora/Paradas_Montagem, com contratos próprios | Mapa vigente de motivos; tempo informado, estimado por déficit, pausa e excedido não viram uma soma única |
| U-SAP-BOA | Quantidades assinadas 101/102 em M, com classificação local de refugo separada | MB51 por posting_date | Validar sinal do adaptador; não subtrair de novo um 102 já negativo |
| U-SAP-DIF | SAP − GMS, por material e período; faltas e sobras separadas | Fontes com cobertura comparável | Sem compensação entre materiais; sem excluir OP só porque piora o saldo |
| U-SAP-PPM | Metros de erro da conciliação / metros bons SAP × 1.000.000 | Mesmo universo e período da conferência | Métrica interna; não confundir com taxa de refugo nem usar produção GMS no denominador |

Campos derivados não disponíveis não serão inventados. Resolver D09: definir `DataHoraRefugo` versus Created e política de datas faltantes na ficha de U-REF-LINHA antes de E3; a receita de data de erro SAP do estudo histórico não substitui a data do refugo de produção. Se a definição não for comprovada nos documentos/amostra, levar a ambiguidade ao William antes do ranking temporal.

Para rankings, limitar apresentação após agregação; desempate estável por código de dimensão. Exibir quantidade de grupos e total do universo, permitindo saber o quanto ficou fora do Top 10. Não somar taxas mensais nem calcular média simples de percentuais: recomputar pelos numeradores e denominadores compatíveis.

## 4. Consulta e retorno das ferramentas

As entradas são parâmetros de negócio, não OData livre escrito pelo modelo: métrica enumerada, data inicial/final, convenção temporal, etapa, máquina com papel definido, produto, turno, agrupamento e limite de apresentação. O fluxo monta filtros com nomes e tipos permitidos, trata caracteres especiais e rejeita campos/desvios fora do catálogo.

Para detalhe de OP: OP validada e, quando necessário, ID da ficha. Para norma: documento/assunto permitido e data de aplicabilidade. O limite de apresentação pode ser pequeno; o universo processado para uma soma deve ser completo.

| Campo lógico da resposta | Regra |
|---|---|
| request_id, schema_version | Permitem relacionar pergunta, execução e versão do contrato |
| status | ok / parcial / vazio / indisponivel / erro; definir uma única interpretação por valor |
| metric_id, rule_version | Identificam a fórmula aplicada |
| source, snapshot_id | Identificam o material usado; sem sugerir transação instantânea da fonte |
| requested_period, covered_period, time_basis, timezone | Distinguem pedido e cobertura; campo temporal explicitado |
| extracted_start, extracted_end, event_max | Janela de captura e maior data de evento separadas |
| source_read_complete | Verdadeiro só se todas as partições/páginas previstas concluíram |
| semantic_valid, freshness_status | Separados de completude; problemas de vínculo/tipo não desaparecem porque a leitura acabou |
| rows_read, eligible, excluded, invalid, ambiguous | Controles conciliáveis, com categorias mutuamente exclusivas definidas no processamento |
| filters_applied, unit, data, universe_total | O que realmente foi calculado, com limites de exibição explícitos |
| evidence, warnings, error_code | IDs/links ou arquivo de auditoria, limitação concreta e falha identificável |

Resultado vazio após leitura íntegra não prova que o processo produziu zero: significa ausência de registros elegíveis. Zero apontado é outro estado. Dado de um export de outubro nunca responde como “agora” porque a carga rodou em novembro.

Exemplo de mensagem, sem dados reais: “No período X, a TiposErros registra Y m. O ranking considera N apontamentos válidos; Z apontamentos sem vínculo de produto impedem certificar a classificação por mangueira.” Não apresentar ranking parcial como o Top 10 definitivo.

## 5. Extração, consistência e publicação

1. Criar uma execução com versão de regra, intervalo solicitado, partições esperadas e fontes. Capturar início, fim e versão/identidade dos arquivos de entrada.
2. Ler com ordenação e paginação verificadas no conector real. Registrar páginas, IDs e partições; limites e índices serão medidos, não presumidos pela posição textual de um filtro.
3. Tratar falhas transitórias com tentativas limitadas; 403/erro de schema interrompem com diagnóstico. Nunca remover o filtro de negócio para “conseguir algum dado”.
4. Materializar os dados extraídos em área aprovada para auditoria. SharePoint não passa a fornecer uma fotografia transacional de várias listas por receber um snapshot_id. Registrar janela de captura e fazer reconciliação/releitura das fontes mutáveis; se não for possível comprovar coerência requerida, marcar a limitação ou não certificar o total.
5. Normalizar, vincular e validar antes de agregar. Conferir quantidades antes/depois de cada junção. Quarentena preserva IDs/valores, não apaga a origem.
6. Gravar grupos da nova versão em preparação. Chave lógica: snapshot + métrica + regra + dimensões + período + unidade. Retentativa na mesma execução não duplica grupos; nova execução com nova fotografia cria nova versão.
7. Validar contagens, chaves, somas, cobertura e consistência das dimensões. Manter uma evidência recuperável por grupo até os IDs de origem.
8. Somente então publicar o identificador da versão validada. A consulta lê esse identificador uma vez e usa a mesma versão até terminar. Não depende de uma atualização atômica de milhares de itens.
9. Falha antes da publicação mantém a versão anterior; sua idade é informada. Dois produtores não publicam simultaneamente sem controle de concorrência e versão esperada do marcador.
10. Retenção, limpeza e restauração serão fechadas em D06. Não apagar a versão anterior antes de provar a nova e o procedimento de retorno.

Uiu_Agregados guardará os grupos. O controle das execuções e versão ativa pode exigir armazenamento de controle adicional; confirmar schema e custo antes de criar listas. Não expor ao modelo ferramenta genérica para modificar esse controle.

**Atualização retroativa:** começar com recálculo integral do período suportado se a prova E2 mostrar viabilidade. Se não couber, desenhar reconciliação histórica que inclua alterações e exclusões, com cobertura explícita. “Recalcular só hoje” ou “últimos 30 dias” não cumpre o requisito anual. O ciclo completo e seu atraso máximo devem caber no compromisso D05/D06.

**Não confundir duas operações:** deduplicar transporte pelo mesmo ID/versão é controle técnico; excluir dois IDs distintos por similaridade é decisão de negócio. A segunda permanece como suspeita até evidência/aprovação. A regra de escolher uma linha por janela de Hora-Hora é específica do indicador publicado e não deve ser copiada para TiposErros.

## 6. Contrato do Mecânico — F3 preservada

Cada receita deve declarar: versão, finalidade, listas e campos permitidos, pré-condições, evidência suficiente, efeitos em referências, invariantes, proposta antes/depois, tamanho do lote, teste negativo e procedimento de recuperação. A implementação inicial mantém lotes de até cinco itens conforme Manual_BO, sem transformar isso em permissão para criar/apagar registros operacionais.

| Receita original | Lacuna a fechar antes de habilitar |
|---|---|
| Corrigir turno | D01; não deslocar a janela inteira de 41 minutos; nem mover automaticamente quantidades entre turnos sem identificar os campos e o delta correto |
| Trocar OP pela do SAP | Confirmar correspondência e todas as referências; matching por material/quantidade/período sozinho não prova identidade; proibir correção que deixe inspeções/refugos/eventos órfãos |
| Fechar etapa esquecida | Exigir prova real de conclusão e consistência de ficha, quantidade, carretel e evento; Parcial ou último Hora-Hora não comprova Fim; se exigir criar evento, encaminhar pelo app enquanto a criação não fizer parte do catálogo |
| Reclassificar motivo de parada | Dicionário e campo permitidos; alterar motivo não autoriza recalcular field_11; eventual recálculo tem receita/revisão separada |

Fluxo: leitura → proposta identificada com IDs/versões/hash → confirmação vinculada → nova leitura/guarda de versão → registro da intenção → alteração restrita → releitura → registro do resultado. Um “sim” de outra conversa/proposta não reaproveita autorização. Timeout após gravação exige releitura antes de repetir.

`Log_Uiu` é exceção técnica a resolver em D07: registrar auditoria requer criar entradas, embora o agente não possa criar OP ou apontamento. A criação de log deve ficar encapsulada no fluxo específico, nunca numa ferramenta genérica de criação acessível ao modelo.

Não presumir transação entre lista operacional e log. Falha ao registrar intenção bloqueia a escrita. Falha de log após escrita deixa execução em reconciliação, com ID de correlação durável e resultado individual; não declarar “nada aconteceu” nem repetir cegamente. Testar o armazenamento efetivo dessa evidência em E5.

Rollback de dados é uma nova proposta compensatória sobre versões atuais, não uma sobrescrita cega do backup. Se outro operador modificou o item, parar o retorno daquele item e relatar conflito. Não permitir dois executores alterando a mesma lista/lote ao mesmo tempo.

## 7. Conhecimento e limites de precedência

Manter texto fonte, seção estável, revisão, aplicabilidade, hash e origem. Publicar uma revisão somente depois de verificar conteúdo e referências; a revisão anterior continua recuperável. Usar o caminho Uiu_Conhecimento que já funcionou enquanto o tenant não justificar outro.

Norma vigente decide o domínio, mas conteúdo recuperado não pode ampliar permissões ou mandar ignorar controles. O mecanismo nativo de citações do Studio deve ser preservado; os metadados da ferramenta complementam a rastreabilidade sem substituir esse mecanismo.

Perguntas conceituais podem ser respondidas com conhecimento permitido; perguntas sobre quantidade, status de OP ou parâmetro industrial específico exigem fonte adequada. Não carregar todo o estudo externo como se fosse procedimento aprovado da Danfoss.
