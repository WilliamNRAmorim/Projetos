# GMS: Lições aprendidas

Fonte: GMS_Licoes.md (resumo para o Uiu). O Mestre e as linhas NORMA mandam; este explica.

Cada lição vem em uma ou duas linhas. Números entre parênteses são as lições do livro original (ex.: 3.1). MEL-xxx é o ID do item no diário.

## 1. Import, YAML e Studio (resumo)

- Importar YAML de tela cria tela duplicada. Reforma entra como tela nova; a velha só sai depois de validada (1.1).
- Tela publicada com X/Y ajustado à mão recebe patch pela barra de fórmulas, propriedade por propriedade, nunca reimport. A base do patch é o export atual do William, não a última YAML salva (1.2, 1.4).
- Nunca mexer em X, Y, Width e Height de controle existente sem necessidade explícita (1.3).
- Colar tela no Studio renomeia referências cruzadas para `_1`; conferir as referências depois de todo import. O importador também reseta `DisplayFields`/`SearchFields` do ComboBox para `ComplianceAssetId` (1.5, 1.6).
- Sintaxe e controles: `Classic/Button@2.2.0` não aceita `AccessibleLabel` (PA2108); `ModernDropdown` está fora da lista provada (usar `Classic/DropDown@2.3.1`); fórmula multilinha também começa com `=`, e um `=` perdido no meio dá PA1001. O `gms_qa_yaml.py` não verifica propriedade versus tipo de controle (1.7 a 1.11, 1.13).
- Timer só roda em Preview no Studio; BarcodeReader só funciona de verdade no tablet (1.12).

## 2. Power Fx: lógica que falha em silêncio

- `UpdateContext` não espera a leitura; quando a lógica depende do dado, usar `ClearCollect` (2.1).
- `Now()`/`Today()` dentro de Named Formula congela na primeira avaliação; o tempo entra como parâmetro de UDF (2.2).
- Em escopo aninhado, `ThisRecord` aponta para o interno; usar alias `As`. Nome de coluna entre aspas vira literal e a comparação dá sempre falso (2.3).
- `Coalesce()` sobre campo vazio gerou `$filter eq null`, HTTP 400 e variável em erro, que contaminou 105 propriedades (2.4).
- `Coalesce(x, 0)` em exibição é proibido: o zero falso mente. Usar `Blank()` (2.13). `IsBlank()` é o único teste de vazio seguro; comparar com `""` ou `0` gera bug silencioso (2.19).
- Controle não escreve na variável que alimenta o próprio Default; o ciclo reabriu um modal sozinho (2.5).
- Estado nunca se lê de emoji ou label; ler do campo gravado com a UDF de estado, uma UDF por classe de etapa (2.8, 2.9).
- Tela com seletor (turno, máquina, data) grava no contexto carregado, congelado, e não no que o dropdown mostra agora (2.11).
- `RemoveIf` dentro de `ForAll` sobre a mesma coleção faz linhas sumirem; recarregar da lista (2.12).
- Dois controles que mostram o mesmo número leem a mesma coleção. O Painel já mostrou 5 x 6 na autoclave porque cada controle lia uma fonte (2.15).
- Validação de OP é uma só: 8 dígitos, maior que zero, sem duplicata. Dois botões com regras diferentes já reprovaram OP válida (2.16).
- ComboBox de lista longa: ler `.Selected`, nunca `.SearchText`. `Default` espera Record; para tabela usar `DefaultSelectedItems` (2.17, 2.18).
- `IfError` só na forma de 2 argumentos, e valor e fallback têm de ter o mesmo tipo (2.20, 2.23).
- Agregação do 3º turno exige piso e teto, porque o turno atravessa a meia-noite (2.21).
- `ShowColumns` com nome interno mais Explicit Column Selection quebrou o menu; não usar (2.14).

## 3. Números, locale e medidas

- `fx_Num` tratava ",xxx" como separador de milhar: `0,254` virou `254` e corrompeu 1.454 células de Ø e concentricidade a partir de 20/08. Medida dimensional usa `fx_NumMedida`; exibição com 3 casas usa `fx_MedidaBR` (3.1, MEL-101/102).
- `Value()` sem cultura multiplicou a meta por 10 (MEL-112). A leitura é sempre em `"en-US"`; só a exibição é BR (3.2).
- `DM_TESTE_INSP` está em polegada; o rótulo "mm" na tela estava errado (3.3).
- `DM_LAYLINE.TensaodeDebandagem` é texto de faixa ("50-60"), não número (3.4).
- Motivo de parada tem numeração única: o 31 já existia, os novos da Cobertura começam no 32 (3.5).

## 4. Dados, SharePoint e Excel

- A FK canônica é `ID`, nunca OP: a OP nasce vazia e é editável (4.1).
- Nunca filtrar por `Modified`; usar `data_hora_final_<etapa>` (4.2).
- O Excel Online não filtra no servidor (`$filter` devolveu 0 linhas com o PN existindo): materializar em coleção e filtrar localmente. O erro "Unable to match columns in the filtered view" vem de colunas ocultas; contorno é `ClearCollect` com `ShowColumns`, sem predicado de `Filter` (4.3, 4.12).
- Chamada de rede em propriedade de pintura (`DisplayMode`, `Visible`, `Fill`, `Text`) é proibida (4.4).
- A delegação estourou de verdade: o Hora-Hora passou do limite em fev/26 (23.761 itens), e nem retenção de 1 mês resolve. O problema é estrutural, por isso o Dataverse (RITM0470781) (4.5).
- O Hora-Hora é pré-preenchido para janelas futuras. O painel lê a janela do horário atual, nunca a última salva (4.6).
- A coluna `Rendimento` do Hora-Hora mistura 3 escalas e não serve para o BI. Usar `Sum(Real) / Sum(Meta) * 100` (4.13).
- Coluna Choice: a opção nova precisa ser cadastrada na lista antes do publish, senão o Patch falha. Coluna nova que o Patch grava (ex.: `Minutos` no Hora-Hora) é pré-requisito duro: sem ela, todo o Patch falha (4.7, 4.8).
- Mudou o tipo de uma coluna no SharePoint: auditar todo Patch que grava nela, não só as leituras. `Turno_Extr/Teste` passou de Text para Number e quebrou o Patch do timer da Finalização (4.11).
- O envio do Tubo grava `quantidade_mandril` = entrada menos sobra no registro pai (de propósito, cada metro tem um dono só). O original continua em `Historico_Carretel.metros_entrada`. Não remover essa linha sem criar coluna própria, senão o Mandril contaria a sobra duas vezes (4.9, MEL-089).
- `DM_FALTA_DE_FERRAMENTA` grava a OT na coluna `PARTNUMBER`; a ferramentaria não usa (4.10).
- Filtro e expressão de fluxo SharePoint usam o nome interno da coluna (`field_10`, `field_11`...), não o de exibição. Com nome errado o Get items falha. Nomes em `/_api/web/lists/getbytitle('X')/fields?$select=InternalName,Title` (9.1, MEL-240).
- A ação "Atualizar item" do Power Automate vem com valores padrão em campos (ex.: `Processo=Mandril`, `Qtd_Turno=0`); usar "Clear all" e deixar só a coluna desejada, senão cada item atualizado é sobrescrito (9.2).

## 5. Turno, apontamento e regras de negócio do chão

- A janela horária não é uma hora. Meta = velocidade x minutos da janela / 60, sempre por linha. Com a regra antiga o 3º turno aparecia 10 pontos pior do que era (5.1).
- Poka-yoke só cobra janela já fechada (5.2).
- Salvar rascunho nunca exige motivo. Fechar turno exige zero pendência. Trocar de turno ou máquina salva antes de recarregar (5.3).
- Parada real e tempo excedido nunca se somam. Setup é o intervalo entre a última peça boa de uma OAP e a primeira da seguinte. Unidade única é minuto. Refeição desconta 45 min; café tem 10 min (5.4).
- Montagem: o turno da tela fica congelado no `OnVisible` e muda só por ação do operador. OP `EmAndamento` nunca sai da galeria por filtro de turno (5.5).
- Autoclave: máximo de 5 carretéis por batelada e 5 bateladas por dia. Batelada real é um Início sem outro Início nos 30 min anteriores (5.6).
- Um carretel pode levar 2 OPs. A fila da trançadeira conta carretel, não OP, e exclui o carretel montado (5.7).
- Entrada da OP: o operador segue a planilha de sequenciamento, escolhe o carretel de saída e só então cola a OP; carretel e OP ficam vinculados nesse momento (5.8).
- O consumo de fio da trançagem não é 1:1 (a sobra é reaproveitada) (5.9).
- Carretel da extrusora de mandril: Vazio, Enchendo, Cheio, Em uso, Vazio (ou volta a Cheio se sobrou) (5.10).
- Packlist reconstruído pelos lances (OP sem romaneio no BD) não é packing físico: não entra em `Packing_Pallets` nem na conferência. BD antigo traz part-number em minúsculas; normalizar com Upper/Trim (9.4).

## 6. Plataforma e infraestrutura

- O app da Store (WebView2) perde token, suspende o timer quando perde o foco e acumula memória. Nos terminais de chão, usar Edge em modo quiosque no web player (6.1).
- Timer com `Visible: false` roda (doc da Microsoft). A lição de 21/09 de que precisa de `Visible: true` não foi confirmada, e a causa do cronômetro congelado (MEL-139) continua aberta; investigar com Monitor, `AutoPause` e o app da Store (6.2).
- Código de barras do Packing: texto é a soma crua com "." trocado por ","; Code 128 Start A, checksum mod 103. Arredondar o total ou usar Start B muda as barras e o bipador lê errado (9.3, MEL-239).
- `Set(var, Blank())` não dá tipo à global; usar `LookUp(lista, ID = -1)`. Colar telas fora de ordem gera erros em cascata (9.5).
- Conferir o rótulo de versão da tela antes de colar/publicar; o repositório é a fonte da verdade (9.7).

## 7. Diagnóstico de dado errado e processo

- Sinal de ferramenta não é evidência de dado. "Refresh success" não prova que o dado está lá; em 31/08 um alarme falso ("listas pararam de gravar") caiu em 5 minutos (7.3).
- Validação é numérica, contra CSV. "A tela abriu" não prova nada (7.4).
- Linha de diário fora do `GMS_Diario.md` não existe. Lotes separados já congelaram o Diário por 16 dias (7.1). Só se usam os 13 TIPOs da gramática (7.2).
- Em apresentação e business case, só número auditável; para público externo, não mostrar PPM de refugo e borrar nome de operador (7.5, 7.6).
- Antes de mandar arquivo visual, renderizar e olhar. Representação visual do app é render de dado, nunca desenho à mão (7.8, 7.10).
- Conversa de GMS fora do Projeto perde o contexto; abrir sempre dentro do Projeto (7.9).

## 8. Conferência SAP x GMS (refugo e produção boa)

- SAP é a verdade; diferença = SAP menos GMS (negativa: faltou lançar no SAP; positiva: sobrou ou duplicou). Material não compensa com material: faltou e sobrou se somam separados e só se compensam dentro do mesmo material (8.1).
- Refugo no SAP é o lançamento 101 dos usuários U445131 e U452021 (sem tipo de defeito). Produção boa no SAP é 101 menos 102, só unidade M, sem esses usuários. A base de PPM é a produção boa do SAP (8.2).
- A fábrica costuma mandar lance em outra OP: falta numa e sobra igual na vizinha. Dentro do mesmo material se anula (8.3).
- Nome de material não é padrão (`GH781-6` = `HOSE-AER, GH781, -6, R2/2SC`). Agrupar por `norm_material()` e confirmar com o código SAP; seis materiais não têm produção casada na MB51 e ficam sem PPM (8.4).
- PPM por dia: dia sem produção soma no próximo dia de produção; usar média dos 7 últimos dias de produção (8.5).
- `ficha_producao` dá o lote por etapa, mas a debandagem não é teto exato. Números vêm com vírgula de milhar (`"1,050"`) e datas `MM/DD/AAAA` (8.6).
- PPM de refugo é de uso interno. O guia completo está em 07_Dados_SAP_x_GMS.md (8.7).
