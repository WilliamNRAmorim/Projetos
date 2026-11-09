# Dados SAP x GMS: fontes, regras, pegadinhas e colunas

Base de conhecimento do Uiu para conferência de refugo, produção boa e PPM. Fonte: guia de 07/10/2026 (análise de refugo lançado errado de 16/05 a 16/09/2026) e notas de 01/11/2026. Os exports são fotografias: ficha até 06/10/2026, inspeção e erros até 02/10, MB51 até 21/10. Nunca diga "de hoje" sem checar a data do arquivo.

## 1. Fontes

- **SAP (MB51)**: lançamentos de produção e refugo, no relatório de conferência (aba MB51) e no export cru da MB51.
- **Conferência por OP (Conf_Geral)**: uma linha por OP com GMS x SAP x packlist; o texto da conferência fica na coluna Obs.
- **Refugo do GMS**: lista TiposErros, uma linha por apontamento de refugo.
- **Inspeção boa do GMS**: lista RegistrosInspeção.
- **Etapas por OP**: ficha_producao (lote em cada máquina/etapa).
- **Refugo SAP x GMS já casado, linha a linha**: planilha Refugo_GMS_alinhado_ao_SAP (abas Por OP e Ajustes).
- **Plano de tratativa**: 150 OPs com erro de refugo.
- A fonte viva é o SharePoint; o que há nos arquivos é uma fotografia.

## 2. Como o refugo e a produção boa aparecem

- **SAP**: o refugo é lançamento 101 (entrada de produção) feito pelos usuários U445131 e U452021. O SAP **não informa o tipo de defeito**. Estorno é 102.
- **GMS**: linhas da TiposErros (tipo, quantidade em metros, data de criação). Linhas novas (a partir de set/2026) vêm sem Id no export; identifique pela data de criação.
- **Produção boa no SAP** = 101 menos 102, sem os lançamentos dos dois usuários de refugo.
- **Produção boa no GMS** = a inspeção (quantidade_extracao da ficha). O total do GMS é boa + refugo.

## 3. Regras

1. **SAP é a verdade absoluta.** O GMS é ajustado para bater com o SAP. **Variação = SAP − GMS**: negativa = faltou lançar no SAP; positiva = sobrou no SAP (duplicado ou excesso).
2. **Material não compensa com material.** Faltou e sobrou se somam **separados por material**. Só compensa dentro do mesmo material (faltar na GH781-8 não cancela duplicado na GH781-10). Não cite "saldo líquido" geral: não vale para inventário.
3. **Lance mandado em outra OP é costume da fábrica.** Aparece como falta numa OP e sobra igual na OP vizinha do mesmo material (ex.: GH781-4, OP 29422610 x 29367063: 63,23 m). Dentro do mesmo material isso se anula. A produção boa divergente foi tratada como justificada (troca de OP ou GMS sem registro no dia); a análise de refugo ignora essa divergência.
4. **Data do erro**: a data do lançamento no SAP; sem lançamento no SAP (refugo que o SAP não recebeu), a data de criação no GMS. Dia sem produção soma no próximo dia de produção.
5. **PPM = metros errados ÷ metros de produção boa × 1.000.000.** A base de produção é o SAP. Material de produção pequena infla o PPM (ex.: FC839B-08, 1.900 m com 32 m de erro = 16.904 ppm).
6. **PPM de refugo é só de uso interno**: não mostrar a público externo.
7. **Metros de mangueira = só unidade M.** A MB51 mistura M, PC e KG (cerca de 6,6 mil linhas em peças ficam de fora).

## 4. Pegadinhas

- **Nome do material não é padrão.** "GH781-6" e "HOSE-AER, GH781, -6, R2/2SC" são o mesmo item na prática. Confirme com o código SAP antes de afirmar.
- **Nunca zere nem descarte uma mangueira por não achar o nome.** Ligue o nome do GMS ao material SAP **pela OP** (a mesma OP nos dois lados). Há uma tabela de apelidos aprendidos (aliases_mangueira). Casos que já pegaram: 2583-12 = código 12055040; GH493-6/8/10/12/16 = descrição genérica "HOSE R12"; HC101-6 tem descrição "-5" no SAP; HC139-7_S-GX, EC215-08LRL e EC215-12LRL são códigos próprios (compare pelo código); GH781-6-2, EC215-06L-2 e FC735-4 são grafias do GMS do mesmo material.
- Se o GMS diz uma mangueira e a OP no SAP é de outra (ex.: OP 29878642, GH781-8 no GMS e FC735-08 no SAP), é divergência real da OP, não apelido.
- **Formato dos exports do SharePoint**: colunas de quantidade e de data vêm como **texto**. Datas no formato `MM/DD/AAAA h:mm AM/PM` (ex.: 05/29/2026 3:10 PM). Números com vírgula de milhar na ficha ("1,050") e ponto decimal ("944.20"): tire a vírgula antes de somar. Colunas turno_* misturam "3" e "Turno 3".
- A ficha tem **uma linha por OP**, com o lote em cada etapa (o comprimento cresce: 800 m na trançagem, 1.050 m na debandagem). A debandagem **não** é teto exato: em várias OPs a extração passa dela.
- **Parada de julho**: sem produção de 04 a 26/07/2026 no SAP e no GMS (provavelmente férias coletivas, a confirmar). Mês de produção pequena distorce o PPM.
- **Meses somados diferem do período inteiro**: a compensação é feita dentro de cada mês (661 m) e no período (581 m); troca de OP que atravessa meses aparece maior nos meses.
- Linhas "e mais N" do texto da conferência não foram somadas: os totais de lances são piso.
- Há 84 grupos repetidos na TiposErros (92 linhas a mais) por OP + erro + quantidade + criado.
- Ao procurar OP sem par (OP no GMS que não existe no SAP e vice-versa), use o método "tem de um lado e não tem do outro" por OP; um filtro do tipo "não está na lista" devolveu zero com a MB51 deste cache.

## 5. Receitas de conferência (em palavras)

- **Refugo errado de um período**: pegue as linhas de refugo com data, OP, material, ação e variação (SAP − GMS). Separe as de variação negativa (faltou) e positiva (sobrou). Some cada grupo por material, sem misturar materiais. O erro total é faltou + sobrou.
- **Produção boa no SAP**: some a quantidade em M dos lançamentos 101, subtraia os 102, e exclua os dois usuários de refugo. Some por dia e por material.
- **PPM**: erro total ÷ produção boa SAP do mesmo período × 1.000.000.
- **Uma OP**: filtre a MB51 pela coluna da OP. A OP 29072011, por exemplo, mostra 20 entradas 101 de produção boa, 1 estorno 102 e nenhum lançamento de usuário de refugo.
- **Ligar as bases**: a OP liga tudo (ficha, MB51, inspeção, erros). Os erros e as inspeções não trazem o nome da mangueira: ligue pela OP à ficha.

## 6. Números de referência (para conferir se refez certo)

- Período 16/05 a 16/09/2026: **faltou 211,6 m + sobrou 369,3 m = 580,9 m em 39 materiais**.
- Produção boa SAP: 596.547 m (GMS: 492.691 m). **974 ppm** (SAP) e 1.179 ppm (GMS).
- PPM total por mês: mai 1.986, jun 1.538, jul 982, ago 434, set 553. Em maio o erro era sobretudo falta; de junho em diante é sobra (duplicado ou excesso).
- GH781-4: 116 m faltando, 113,2 m deles na OP 29072011 (22 apontamentos no GMS em 29/05, nada no SAP; produção boa 944,2 m + refugo 113,2 m = 1.057,4 m contra 1.050 m na debandagem).

## 7. Tabelas e colunas dos exports

### ficha_producao
Uma linha por OP (ficha), com o lote em cada etapa.
- `op`: número da OP (chave que liga tudo).
- `mangueira`: nome da mangueira no GMS.
- `status_processo`: Finalizado, Aguardando, Em processo ou Cancelado.
- `quantidade_*`: metros por etapa, em texto com vírgula de milhar. `quantidade_extracao` é a produção boa do GMS; `quantidade_debandagem` é a metragem na debandagem (não é teto exato).
- `bitola`, `trancadeira` (códigos TH/TM), datas (como `datafinalizacao`) em texto, e `turno_*` misturando "3" e "Turno 3".

### mb51 (SAP)
Uma linha por item de documento de material.
- `order`: a OP. `material`: código SAP. `material_description`: nome no SAP.
- `movement_type`: 101 = entrada de produção; 102 = estorno (quantidade negativa).
- `quantity` e `unit_of_entry`: quantidade e unidade (M, PC, KG; só M é metro de mangueira).
- `user_name`: usuário do lançamento; U445131 e U452021 lançam refugo.
- `posting_date`: data do lançamento. `material_document` (com o item do documento): identifica o documento; o item sozinho não identifica nada.
- A cópia da aba MB51 da Máscara de produção (até 01/10) tem o mesmo conteúdo, só menos recente: use a MB51 mais nova.

### registrosinspecao (inspeção boa do GMS)
Uma linha por medição.
- `op_id`: OP. `quantidade`: metros, em texto. `datahorainspecao`: texto. `turnoteste`.
- `mangueira` (cerca de 13% vazio), `trancadeira`, `concentricidade`, `cabine_teste` (só em registros novos) e `CodigoDefeito`.

### tiposerros (refugo do GMS)
Uma linha por apontamento.
- `op_id`: OP. `codigoerro`: causa. `quantidade`: metros.
- `criado`: data de criação (texto). `datahorarefugo`: data do refugo (texto). `turno_erro`, `trancadeira`.
- Não tem o nome da mangueira: ligue à ficha pela OP. Linhas novas (de set/2026) vêm sem Id.

### packing list (bd_packing_list__data_base)
- A chave é `id` + `slice` (um id tem várias fatias).
- `pn`: nome da mangueira (a ligação é por nome). `qtd_m`: metros.
- `cancelled`: 1 = cancelado; vazio ou 0 = válido.
- Não junte por `id` ou `slice` com outras tabelas: só batem por coincidência de número.

### Outras
- Cadastro de mangueiras: nome (mangueira_hose), tipo, bitola e wires.
- As demais abas da Máscara de produção (plano, resumo, COOIS, detalhes, cálculo de horas, etc.) são apoio de planejamento em formato de tabela dinâmica, sem documentação das colunas. Não responda com base nelas sem conferir.

## 8. O que ainda não está fechado

- Confirmar o código SAP dos materiais agrupados por nome e achar a produção dos seis materiais sem PPM (EC215-08LRL, 2583-12, HC139-7_S-GX, HC101-6, GH493-12 e GH493-16; a ligação pela OP resolveu parte em 14/10/2026).
- Confirmar com a produção se os 113,2 m de refugo da OP 29072011 são reais (índice de 12% contra mediana de 1,1% da GH781-4).
- Separar, material a material, o que é troca de OP (se anula) e o que é refugo realmente não enviado.
- Os arquivos são de 01/10/2026 (relatório) e de 06 a 07/10 (exports); correções feitas depois não aparecem.
