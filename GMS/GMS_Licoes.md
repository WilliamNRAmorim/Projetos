# GMS — Livro de Lições
### O que funciona, o que não funciona e por quê · consolidado em 25/09/2026 · + memória legada em 26/09

> **Para que serve:** reúne num só lugar o aprendizado que estava espalhado em conversas, COLARs e lotes de diário, para não se perder quando versões antigas saem do projeto.
> **Hierarquia:** `GMS_Mestre.md` + linhas `NORMA` do Diário **mandam**. Este arquivo **explica e lembra**. Se algo aqui contradisser o Mestre, o Mestre vence e a divergência vira pergunta.
> **Como crescer:** toda sessão que pagar uma lição nova acrescenta **uma linha** na seção certa, com a fonte. Lição promovida a NORMA ganha a marca `→ NORMA dd/mm`.
> **Legenda de fonte:** `Mestre §x` · `Diário dd/mm` · `COLAR <tela> vX` · `conversa dd/mm`.

---

## 1. Import, YAML e Studio

| # | Lição | Fonte |
|---|---|---|
| 1.1 | Importar YAML de tela cria **tela duplicada**. Reforma de tela existente entra como tela nova, com nomes novos, e a velha só sai depois de validada | Mestre §3.8.9 |
| 1.2 | Tela publicada com X/Y ajustado à mão recebe **patch pela barra de fórmulas**, propriedade por propriedade, e nunca reimport | Diário 18/08 (DECISÃO) |
| 1.3 | **Nunca mexer em X, Y, Width e Height** de controle existente sem necessidade explícita, e listar o que mudou. O Painel v0.4.0 moveu controles sem motivo e precisou ser refeito por diff geométrico na v0.4.1 | conversa 23/09 |
| 1.4 | A base do patch é **o export atual do William**, não a última YAML salva no projeto. Ele ajusta layout entre versões, e montar sobre a versão salva apaga esse trabalho | conversa 24/09 (Painel v0.8.0), 25/09 (Extrusora) |
| 1.5 | Colar tela no Studio **renomeia referências cruzadas** para `_1`. Depois de todo import, conferir as referências, não só o PA1001 | Diário 18/08 |
| 1.6 | O importador do Studio **reseta `DisplayFields`/`SearchFields` do ComboBox** para `ComplianceAssetId`. Reconfigurar para `Title` depois do import | conversa 28/08 (Debandagem) |
| 1.7 | `Classic/Button@2.2.0` **não aceita `AccessibleLabel`** (PA2108). `Classic/Icon@2.5.0` aceita. No botão, quem é lido pelo leitor de tela é o `Text` | conversa 24/09 |
| 1.8 | `OnChange` é válido em `Classic/TextInput`, `Classic/DropDown` e `Classic/ComboBox` (a acusação do QA era falso positivo) | COLAR HoraHora v0.5.0 |
| 1.9 | `Classic/DatePicker@2.6.0` entrou na lista de controles provados | Diário 17/08 (NORMA) |
| 1.10 | `ModernDropdown` está fora da lista provada. Usar `Classic/DropDown@2.3.1` | COLAR HoraHora v0.5.0 |
| 1.11 | O `gms_qa_yaml.py` **não verifica propriedade × tipo de controle**. PA2108 passa pelo QA e só estoura no import. Pendente: adicionar esse teste | conversa 24/09 |
| 1.12 | Timer só roda em **Preview** no Studio. BarcodeReader só funciona de verdade no **tablet** | MS Learn; Mestre §3.9.6 |

## 2. Power Fx: lógica que falha em silêncio

| # | Lição | Fonte |
|---|---|---|
| 2.1 | `UpdateContext` não espera a leitura. Quando a lógica depende do dado, usar `ClearCollect` | Mestre §3.1 |
| 2.2 | `Now()`/`Today()` dentro de Named Formula **congela** na primeira avaliação. Tempo entra como parâmetro de UDF | Mestre §3.2 |
| 2.3 | Em escopo aninhado, `ThisRecord` aponta para o interno: usar alias `As`. Nome de coluna entre aspas vira literal e a comparação dá sempre falso | Mestre §3.13 |
| 2.4 | `Coalesce()` sobre campo vazio gerou `$filter eq null`, HTTP 400 e variável em **erro** (não Blank). O erro contaminou 105 propriedades | Diário 18/08 |
| 2.5 | Controle **não escreve na variável que alimenta o próprio Default**. O ciclo reabria o modal sozinho | Diário 18/08 |
| 2.6 | Conteúdo derivado de spec vai em `Items` reativo (`With` + `LookUp` local), nunca em coleção remontada por botão | Diário 18/08 (NORMA) |
| 2.7 | `varSpec<Etapa>` tem **um** ponto de escrita. Selecionar item na fila não recarrega spec | Diário 18/08 (NORMA) |
| 2.8 | Estado nunca se lê de emoji ou label (`lbl.Text = "🟢"`). Ler do campo gravado com a UDF de estado | Diário 18/08; Mestre §3.10 |
| 2.9 | Estado de etapa é UDF **por classe** (`fx_EstadoContinuo`, `fx_EstadoVulca`), nunca uma cópia por etapa | Diário 18/08 (NORMA) |
| 2.10 | Um alvo = um botão. Ícone sobreposto faz só `Select()`. Lógica pesada fica num botão oculto, e os visíveis só setam o modo e chamam `Select()` | Mestre §5.8; Diário 18/08 |
| 2.11 | Tela com seletor (turno, máquina, data) grava no contexto **carregado**, congelado em `ctx`, e não no que o dropdown mostra agora | COLAR HoraHora v0.5.0 (NORMA 03/09) |
| 2.12 | `RemoveIf` dentro de `ForAll` sobre a mesma coleção faz linhas sumirem. Recarregar da lista | COLAR HoraHora v0.5.0 |
| 2.13 | **`Coalesce(x, 0)` em exibição é proibido:** zero falso mente. Usar `Blank()` | conversa 23/09 (Painel) |
| 2.14 | `ShowColumns` com nome interno + *Explicit Column Selection* quebrou o menu na v0.7.1. Não usar | conversa 25/09 |
| 2.15 | Dois controles que mostram o mesmo número leem **a mesma coleção**. O Painel mostrou 5 × 6 na autoclave porque cada controle lia uma fonte | conversa 25/09 (Painel v0.9.2) |
| 2.16 | Validação de OP divergia entre dois botões (uma regra reprovava OP válida). A regra é uma só: 8 dígitos, > 0, sem duplicata | Diário 18/08 |
| 2.17 | ComboBox de lista longa usa `IsSearchable: true`. A barreira é **ler `.Selected`**, nunca `.SearchText`, e não impedir a digitação | Diário 18/08 (NORMA emendada) |
| 2.18 | `Default` espera Record. Para ComboBox que recebe tabela, usar `DefaultSelectedItems` ("Expected Record value") | Diário 18/08 |
| 2.19 | `IsBlank()` é o único teste de vazio seguro. Comparar com `""` ou `0` gera bug silencioso | memória legada |
| 2.20 | `IfError` só na forma de 2 argumentos (regra do projeto) | memória legada |
| 2.21 | Agregação do 3º turno exige piso **e** teto, porque o turno atravessa a meia-noite | memória legada |
| 2.22 | Code 128B offline: 4 UDFs (`C128Val`, `C128Pat`, `C128Encode`, `C128SVG`) renderizadas num `Image` com `"data:image/svg+xml," & EncodeUrl(...)`, sem API externa | memória legada |

## 3. Números, locale e medidas

| # | Lição | Fonte |
|---|---|---|
| 3.1 | `fx_Num` trata ",xxx" como separador de milhar: `0,254` virou `254`. Isso corrompeu 1.454 células de Ø e concentricidade a partir de 20/08. Medida dimensional usa `fx_NumMedida`, e a exibição com 3 casas usa `fx_MedidaBR` | conversa 28/08 (MEL-101/102) |
| 3.2 | `Value()` sem cultura multiplicou a meta por 10 (MEL-112). A leitura é sempre em `"en-US"`, e só a exibição é BR | conversa 24/09 |
| 3.3 | `DM_TESTE_INSP` está em **polegada**. O rótulo "mm" na tela estava errado | conversa 28/08 |
| 3.4 | `DM_LAYLINE.TensaodeDebandagem` é **texto de faixa** ("50-60"), não número, e `fx_NumSpec` devolve 0 | conversa 28/08 |
| 3.5 | Motivo de parada tem numeração única: o 31 já existia, então os novos da Cobertura começam no 32 | conversa 21/09 |

## 4. Dados, SharePoint e Excel

| # | Lição | Fonte |
|---|---|---|
| 4.1 | A FK canônica é `ID`, nunca OP: a OP nasce vazia e é editável | memória data-schema |
| 4.2 | Nunca filtrar por `Modified`. Usar o `data_hora_final_<etapa>` | Mestre §3.3 |
| 4.3 | O Excel Online **não filtra no servidor** (`$filter` devolveu 0 linhas com o PN existindo). Materializar em coleção e filtrar localmente | Diário 18/08 |
| 4.4 | Chamada de rede em propriedade de pintura (`DisplayMode`, `Visible`, `Fill`, `Text`) é proibida | Diário 18/08 (NORMA) |
| 4.5 | A delegação estourou de verdade: o Hora-Hora passou do limite em fev/26 (23.761 itens), e nem retenção de 1 mês resolve. O problema é estrutural, por isso o Dataverse (RITM0470781) | conversa 27/08 |
| 4.6 | O Hora-Hora é **pré-preenchido** para janelas futuras. O painel lê a janela do horário atual, nunca a última salva | memória overview (Painel) |
| 4.7 | Coluna **Choice**: a opção nova precisa ser cadastrada na lista **antes** do publish, senão o Patch falha | conversa 25/09 (Extrusora) |
| 4.8 | Coluna nova que o Patch grava (ex.: `Minutos` no Hora-Hora) é pré-requisito duro. Sem ela, **todo** o Patch falha | COLAR HoraHora v0.5.0 |
| 4.9 | O envio do Tubo grava `quantidade_mandril` = entrada − sobra no registro pai (split C38, de propósito: cada metro tem um dono só). O original continua em `Historico_Carretel.metros_entrada` (etapa Tubo) e o `sobra` no evento Fim. **Não remover** essa linha sem criar antes coluna própria para o original: o filho copia os campos do Mandril e o volume do Mandril passaria a contar a sobra duas vezes (MEL-089, resolvido como projeto) | Diário 06/10 |
| 4.10 | `DM_FALTA_DE_FERRAMENTA` grava a OT na coluna `PARTNUMBER`. A ferramentaria não usa, e o fluxo saiu das telas | Diário 18/08; memória |
| 4.11 | Mudou o tipo de uma coluna no SharePoint: auditar **todo Patch** que grava nela, não só as leituras. `Turno_Extr/Teste` passou de Text para Number e quebrou o Patch do timer da Finalização | memória legada |
| 4.12 | Excel Online: o erro "Unable to match columns in the filtered view" vem de **colunas ocultas**. O contorno é `ClearCollect` com `ShowColumns`, sem predicado de `Filter`. Não confundir com a 2.14, onde o problema era `ShowColumns` com nome interno + Explicit Column Selection | memória legada |
| 4.13 | A coluna `Rendimento` do Hora-Hora mistura 3 escalas e não serve para o BI. Usar `Sum(Real) / Sum(Meta) * 100` | memória legada |

## 5. Regras de negócio do chão (confirmadas pelo William)

| # | Lição | Fonte |
|---|---|---|
| 5.1 | **A janela horária não é uma hora.** Meta = velocidade × minutos da janela / 60, sempre por linha. Com a regra antiga o 3º turno aparecia 10 pontos pior do que era | COLAR HoraHora v0.5.0 (NORMA 03/09) |
| 5.2 | Poka-yoke só cobra **janela já fechada**. Alerta sem base ensina o operador a ignorar alerta | COLAR HoraHora v0.5.0 (NORMA 03/09) |
| 5.3 | Salvar rascunho nunca exige motivo. Fechar turno exige zero pendência. Trocar de turno ou máquina **salva antes** de recarregar | COLAR HoraHora v0.5.0 (DECISÃO) |
| 5.4 | Parada real ≠ tempo excedido, e os dois nunca se somam. Setup = intervalo entre a última peça boa de uma OAP e a primeira da seguinte. Unidade única é minuto. Refeição desconta 45 min, café tem 10 min. Toda análise usa os dois turnos | reunião 31/08 |
| 5.5 | Montagem: o turno da tela fica congelado no `OnVisible` e muda só por ação do operador. OP `EmAndamento` nunca sai da galeria por filtro de turno | conversa 28/08 |
| 5.6 | Autoclave: máximo de 5 carretéis por batelada e 5 bateladas por dia. Batelada real = Início sem outro Início nos 30 min anteriores | memória overview |
| 5.7 | Um carretel pode levar 2 OPs. A fila da trançadeira conta **carretel**, não OP, e exclui o carretel montado | conversa 25/09 (Painel v0.8.1) |
| 5.8 | Entrada da OP: o operador segue a planilha de sequenciamento, escolhe o carretel de saída **e só então** cola a OP. Carretel e OP ficam vinculados nesse momento | memória overview |
| 5.9 | Consumo de fio da trançagem não é 1:1 (sobra é reaproveitada). O modelo atual é mais sofisticado do que o chão tem | memória /areas/gms |
| 5.10 | Carretel da extrusora de mandril: Vazio → Enchendo → Cheio → **Em uso** → Vazio (ou volta a Cheio se sobrou) | conversa 25/09 (Extrusora v0.2.0) |

## 6. Plataforma e infraestrutura

| # | Lição | Fonte |
|---|---|---|
| 6.1 | O app da Store (WebView2) perde token, suspende timer quando perde o foco e acumula memória. Nos terminais de chão, usar **Edge em modo quiosque** no web player | conversa 17/09 |
| 6.2 | **Timer com `Visible: false` roda.** A doc da Microsoft recomenda isso para timer de fundo, e o Mestre §3.11 também. A lição de 21/09 ("precisa `Visible: true`") **não é confirmada**, e a causa do cronômetro congelado (MEL-139) continua aberta. Investigar com Monitor, `AutoPause` e o app da Store (6.1) | MS Learn (control-timer) |
| 6.3 | A rede da Danfoss **bloqueia links de artifact do claude.ai**. Entrega visual sai em PNG ou arquivo `.html` | memória ways-of-working |
| 6.4 | O espaço de arquivos do Projeto (knowledge) tem 2 MB. Só a versão vigente de cada tela fica no projeto, e histórico de código mora no Git (MEL-018) | auditoria 25/09 |

## 7. Processo de trabalho (William + Claude)

| # | Lição | Fonte |
|---|---|---|
| 7.1 | **Linha de diário fora do `GMS_Diario.md` não existe.** Lotes separados congelaram o Diário por 16 dias em ago/set, e isso voltou a acontecer em set (MEL-XXX/???) | conversa 03/09; auditoria 25/09 |
| 7.2 | Só se usam os 13 TIPOs da gramática. `CORREÇÃO` e `ACHADO` não existem: o primeiro vira `LIÇÃO`/`FEITO`, o segundo virou `LIÇÃO` | Diário (gramática); conversa 03/09 |
| 7.3 | Sinal de ferramenta ≠ evidência de dado. "Refresh success" não prova que o dado está lá. Em 31/08, um alarme falso ("listas pararam de gravar") caiu em 5 minutos | reunião 31/08 |
| 7.4 | Validação é **numérica, contra CSV**. "A tela abriu" não prova nada | Mestre §3.13 / §7.2.5 |
| 7.5 | Em apresentação e business case, **só número auditável**. O €21,6k/ano saiu do deck, e o canvas do RITM ficou só com quality + reporting hours | conversas 27/08, 25/09 |
| 7.6 | Para público externo: não mostrar PPM de refugo e borrar nome de operador em print | conversa 25/09 (deck) |
| 7.7 | Formato de entrega: YAML para Power Apps, `.md` para COLAR, e nunca XLSX quando o pedido é tela | conversa 21/09 |
| 7.8 | Antes de mandar arquivo visual, **renderizar e olhar**. O deck saiu uma vez com prints sobrepostos e tela achatada | conversa 25/09 |
| 7.10 | Representação visual do app (mapa, estado da célula) é **render de dado**, nunca desenho à mão. É a mesma lógica do delineamento (B §5.9) | memória legada; conversa 03/09 |
| 7.9 | Conversa de GMS fora do Projeto perde o contexto (resumos chamaram o GMS de "Gestão de Manufatura") e depois precisa ser importada à mão. Abrir sempre dentro do Projeto | conversas 22–24/09 |

## 8. Conferência SAP x GMS (refugo e produção boa)

| # | Lição | Fonte |
|---|---|---|
| 8.1 | SAP é a verdade; diferença = SAP − GMS (negativa = faltou lançar no SAP, positiva = sobrou/duplicado). **Material não compensa com material**: inventário é por material, então faltou e sobrou são somados separados e só se compensam dentro do mesmo material. Citar "saldo líquido" geral foi erro e foi corrigido | conversa 07/10 |
| 8.2 | Refugo no SAP = lançamento 101 dos usuários U445131 e U452021 (sem tipo de defeito); produção boa no SAP = 101 menos 102, só unidade M, sem esses usuários. Base de PPM = produção boa do SAP, porque cobre OPs que o GMS não tem | conversa 07/10; `Analises/Refugo_por_Material/gms_dados.py` |
| 8.3 | A fábrica costuma mandar lance em outra OP: falta numa OP e sobra igual na vizinha (GH781-4: 63,23 / 62,5 / 19,6 m). Dentro do mesmo material se anula. A divergência de produção boa é tratada como justificada; a análise de refugo não a usa | conversa 07/10 |
| 8.4 | Nome de material não é padrão (`GH781-6` = `HOSE-AER, GH781, -6, R2/2SC`). Agrupar por `norm_material()` e confirmar com o código SAP; seis materiais não têm produção casada na MB51 e ficam sem PPM | conversa 07/10 |
| 8.5 | PPM por mês e por dia: dia sem produção soma no próximo dia de produção; usar média dos 7 últimos dias de produção (a janela de 7 dias corridos disparou no retorno da parada de julho). Meses somados (661 m) passam do período inteiro (581 m) por causa de trocas de OP entre meses | conversa 07/10 |
| 8.6 | `ficha_producao` dá o lote por etapa e ajuda a testar se refugo é plausível (boa + refugo contra `quantidade_debandagem`), mas a debandagem não é teto exato. Números vêm com vírgula de milhar (`"1,050"`) e datas `MM/DD/AAAA` | conversa 07/10 |
| 8.7 | PPM de refugo é de uso interno (ver 7.6); o guia completo, com receitas e números de referência, está em `Analises/Refugo_por_Material/COMO_USAR_OS_DADOS.md` | conversa 07/10 |
