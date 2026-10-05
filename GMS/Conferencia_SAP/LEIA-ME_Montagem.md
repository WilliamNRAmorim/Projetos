# Conferência diária GMS × SAP × Packing: montagem (MEL-196 · C29)

**O que é:** todo dia útil de manhã um fluxo confere, lance por lance, o que a cabine apontou no GMS, o que o SAP recebeu (MB51) e o que foi para o Packing List. Ele te manda um e-mail com as pendências e grava cada uma na lista `Conferencia_SAP`. A tela **Gestão → Conferência GMS × SAP × Packing** lê essa lista e registra a tratativa. Quando alguém corrige no GMS, no SAP ou no Packing, a conferência do dia seguinte vê que bateu e fecha a pendência sozinha.

```
Ter–Sáb 08:00 ─► fluxo GMS_Conferencia_Diaria
                 ├─ espera o mb51.xlsx ser atualizado hoje (até 4 h)
                 ├─ Office Script GMS_LerPacking        @ BD Packing List.xlsx  (só leitura)
                 ├─ SharePoint: RegistrosInspeção, TiposErros, ficha_producao, pendências abertas
                 ├─ Office Script GMS_ConferenciaDiaria @ mb51.xlsx            (só leitura)
                 ├─ cria/atualiza itens na lista Conferencia_SAP
                 └─ e-mail HTML pra você
GMS ─► scr_ConferenciaSAP lê Conferencia_SAP, grava Tratativa / Responsável / Justificado
```

Conectores: SharePoint, Excel Online (Business) e Outlook. Todos padrão, nenhum premium.

---

## Regras que o motor aplica (validadas no export de 02/10)

| Ponto | Regra | Base |
|---|---|---|
| OP conforme | GMS aprovado + GMS refugo = SAP 101−102 (unidade M, depósito GRT4), tolerância **0,5 m** | 280 de 331 OPs de set/26 fecham com diferença zero |
| Lance aprovado → SAP | Mesmo dia; o 3º turno pode virar o dia | 99,8% dos lances caem no SAP no mesmo dia |
| Lance aprovado → Packing | Mesmo dia; o 3º turno pode virar o dia | William, 02/10 |
| Sábado | Domingo não trabalha. O 3º turno de sábado pode terminar na segunda, então lance de **sábado é cobrado na segunda** | William, 02/10 |
| Refugo → SAP | Entra em lote: **seg→ter, ter→qui, qua→qui, qui→sex, sex→seg, sáb→seg**. Só vira pendência depois do dia do lote | William + medido ago–set/26 |
| Refugo → Packing | Não vai para o Packing. É só GMS × SAP | William, 02/10 |
| Refugo somado no SAP | Um doc do SAP pode somar vários refugos do GMS (ex.: 5,4 = 4,5 + 0,9) e o motor casa por subconjunto | caso OP 30364966 |
| Estorno 102 | Anula o 101 de mesma metragem | Lição MB51 31/08 |
| Packing sem OP | O romaneio só tem PN. O motor casa por PN + metragem exata + horário e, se não achar, tenta metragem ±1 m ("no GMS está 82,3 m") | 94% dos slices casam exato |

**Categorias** (uma por OP, na ordem do seu `Plano_Tratativa_MB51.xlsx`): OP digitada errada no GMS · SAP lançou, GMS não tem a OP · GMS apontou, SAP não lançou a OP · Lance apontado na OP errada (troca entre duas OPs do mesmo PN) · Metragem digitada diferente · SAP lançou lance que o GMS não tem · GMS apontou lance que o SAP não tem · Refugo a mais no SAP · Refugo faltando no SAP · Outra divergência · Packing sem lance no GMS · Romaneio duplicado · ID de romaneio repetido · Lance aprovado sem packing.

O que o motor **não** faz: não importa o backlog antigo (as 304 OPs de mai–set do Plano_Tratativa). Ele começa do dia em que ligar e só olha o que teve movimento no dia ou o que está aberto na lista.

---

## Passo 1 · Lista `Conferencia_SAP` (site OperationsGuaratingueta)

Crie a lista em branco e as colunas **com estes nomes exatos, sem acento e sem espaço**. O nome interno nasce igual ao digitado e é por ele que o app e o fluxo leem. Depois de criada, pode renomear o "nome de exibição" se quiser.

| Coluna | Tipo | Observação |
|---|---|---|
| Title | (já existe) | chave: OP ou "PL 1489" (romaneio) |
| OP | Linha de texto | |
| PN | Linha de texto | |
| Categoria | Linha de texto | |
| Prioridade | Número, 0 casas | 1 = mais grave · 99 = resolvido |
| Status | **Linha de texto** (não Escolha) | Aberto / Justificado / Resolvido. Texto delega no filtro (B §4.2, Lição 4.7) |
| DataRef | Data (só data) | dia da última conferência |
| DataDeteccao | Data (só data) | primeiro dia em que apareceu |
| GMS_m | Número, 2 casas | |
| Refugo_m | Número, 2 casas | |
| SAP_m | Número, 2 casas | |
| Packing_m | Número, 2 casas | |
| Dif_m | Número, 2 casas | GMS + refugo − SAP |
| ProvavelOP | Linha de texto | |
| Detalhe | Várias linhas, **texto sem formatação** | |
| Acao | Linha de texto | |
| QuemResolve | Linha de texto | |
| Cabine | Linha de texto | |
| Tratativa | Várias linhas, texto sem formatação | quem grava é a tela |
| Responsavel | Linha de texto | quem grava é a tela |
| DataTratativa | Data **e hora** | quem grava é a tela |

**Configurações da lista → Indexar colunas:** crie índice em `Status` e em `Title`. São uns 15 itens por dia, então a lista passa de 5.000 em cerca de um ano, e sem índice o filtro para de funcionar nesse ponto (B §4.2).

**ficha_producao → criar modo de exibição `Conf_SAP`** só com as colunas `OP` e `Mangueira`. O fluxo lê a ficha por esse modo e evita trazer as 113 colunas.

---

## Passo 2 · Os dois Office Scripts

1. Abra o **mb51.xlsx** no Excel **na web** → guia **Automatizar** → **Novo script**.
2. Apague o conteúdo, cole o arquivo inteiro `GMS_ConferenciaDiaria.ts`, renomeie o script para `GMS_ConferenciaDiaria` e salve.
3. Novo script de novo: cole `GMS_LerPacking.ts` e salve como `GMS_LerPacking`.

Os scripts ficam no seu OneDrive (Documentos/Office Scripts) e servem para qualquer planilha. **Nenhum dos dois escreve na planilha.**

**Teste de fumaça (2 min):** com o mb51.xlsx aberto, rode `GMS_ConferenciaDiaria` pelo painel. Em `dataRef` deixe vazio, nos cinco campos `...Json` coloque `[]`, tolerância `0.5` e janela `30`. Ele precisa terminar sem erro e mostrar o resultado no log. Isso prova que ele acha as colunas do MB51 e lê as ~110 mil linhas (aqui, contra o export, foram 31 leituras de bloco). Como o teste vai sem GMS, toda OP do dia sai como "SAP lançou, GMS não tem a OP". É o esperado.

---

## Passo 3 · Fluxo `GMS_Conferencia_Diaria` (fluxo de nuvem agendado)

> **O mb51.xlsx é recriado todo dia pelo supervisor (export do SAP).** Por isso: (1) o script fica no
> OneDrive do dono do fluxo, nunca dentro da planilha, e ninguém cola nada de novo; (2) o fluxo **não**
> escolhe o arquivo no seletor (arquivo recriado ganha ID novo e o fluxo quebraria): ele faz
> *Obter metadados do arquivo usando o caminho* a cada execução e passa o **Id** para o *Executar script*
> (campo Arquivo → valor personalizado → Id dinâmico); (3) o motor acha a aba e a linha de cabeçalho
> pelos nomes das colunas do MB51. Só o nome e a pasta do arquivo precisam continuar iguais.

Coloque os passos 3.2 a 3.10 dentro de um **Escopo** chamado `Conferir` (o 3.11 depende disso).

**3.1 Gatilho: Recorrência.** Frequência Semana · dias **terça, quarta, quinta, sexta, sábado** · hora 8 · minuto 0 · fuso (UTC-03:00) Brasília.
Terça confere segunda (e o sábado anterior junto), ..., sábado confere sexta. Na segunda de manhã não roda: a produção de sábado só vence na segunda.

**3.2 Esperar o MB51 de hoje.**
- *Inicializar variável* `varMB51Hoje` (Booleano) = `false`.
- *Fazer até* `varMB51Hoje` é igual a `true` · Alterar limites: Contagem 8, Tempo limite `PT4H`. Dentro:
  - SharePoint *Obter metadados do arquivo usando o caminho* (`MB51_Meta`): site OperationsGuaratingueta, caminho `/Shared Documents/Manufatura/Production planning/2_Production_Planning/Relatórios/mb51.xlsx` (escolha pelo seletor de pasta).
  - *Condição*: `convertTimeZone(body('MB51_Meta')?['LastModified'],'UTC','E. South America Standard Time','yyyy-MM-dd')` **é igual a** `convertTimeZone(utcNow(),'UTC','E. South America Standard Time','yyyy-MM-dd')`
    - Sim → *Definir variável* `varMB51Hoje` = `true`
    - Não → *Atraso* 30 minutos

  Se o MB51 não chegar em 4 h, o fluxo segue assim mesmo e o e-mail sai com faixa vermelha avisando que o MB51 não tem lançamento no dia. Nesse caso não confie no restante do e-mail.

**3.3 Packing.** Excel Online (Business) *Executar script* (`Ler_Packing`): Local = SharePoint OperationsGuaratingueta · Biblioteca = Documentos · Arquivo = `BD Packing List.xlsx` (pasta `Manufatura operação / 1 - Mangueira / 16_REGISTROS_DE_PRODUÇÃO / CABINES DE TESTE`) · Script = `GMS_LerPacking` · janelaDias = `30`.

**3.4 RegistrosInspeção.** SharePoint *Obter itens* (`Insp_Itens`): lista RegistrosInspeção · Ordenar por `ID desc` · Contagem superior `5000`.
Depois *Selecionar* (`Insp_JSON`): De = `value` do Insp_Itens. Mapear chave → valor, escolhendo o valor pelo conteúdo dinâmico:

| chave | valor (conteúdo dinâmico) |
|---|---|
| id | ID |
| op | OP_ID |
| q | Quantidade (Quantidade_Inspeção) |
| dt | DataHoraInspecao |
| cab | cabine_teste (se for coluna Escolha, use "cabine_teste Value") |

**3.5 TiposErros.** *Obter itens* (`Ref_Itens`), ordenado por `ID desc`, top `5000`. *Selecionar* (`Ref_JSON`): `id`→ID · `op`→OP_ID · `q`→Quantidade · `dt`→**Criado** · `cod`→CodigoErro · `cab`→cabine_teste.

**3.6 ficha_producao.** *Obter itens* (`Ficha_Itens`): top `5000`, ordenado por `ID desc`, *Limitar colunas por modo de exibição* = `Conf_SAP`. *Selecionar* (`Ficha_JSON`): `op`→OP · `pn`→Mangueira.

**3.7 Pendências abertas.** *Obter itens* (`Abertos_Itens`): lista Conferencia_SAP · Consulta de filtro `Status ne 'Resolvido'` · top `5000`. *Selecionar* (`Abertos_JSON`): `chave`→Title · `id`→ID · `status`→Status · `desde`→DataDeteccao · `categoria`→Categoria.

**3.8 Conferir.** *Executar script* (`Conferir`): Arquivo = `mb51.xlsx` (mesma pasta do 3.2) · Script = `GMS_ConferenciaDiaria`:

| parâmetro | valor (Expressão) |
|---|---|
| dataRef | *(vazio: o script confere o dia útil anterior)* |
| inspecoesJson | `string(body('Insp_JSON'))` |
| refugosJson | `string(body('Ref_JSON'))` |
| fichaJson | `string(body('Ficha_JSON'))` |
| packingJson | conteúdo dinâmico **result** do `Ler_Packing` |
| abertosJson | `string(body('Abertos_JSON'))` |
| toleranciaM | `0.5` |
| janelaDias | `30` |

Para reconferir um dia específico, preencha `dataRef` com `2026-10-01`.

**3.9 Gravar na lista.** *Aplicar a cada* sobre **itens** (conteúdo dinâmico do `Conferir`). Dentro, uma *Condição*: `idLista` **é maior que** `0`.
- **Sim** → SharePoint *Atualizar item*: lista Conferencia_SAP · Id = `idLista` · Title = `chave` · OP = `op` · PN = `pn` · Categoria = `categoria` · Prioridade = `prioridade` · Status = `status` · DataRef = `dataRef` · GMS_m = `gmsM` · Refugo_m = `refugoGmsM` · SAP_m = `sapM` · Packing_m = `packingM` · Dif_m = `difM` · ProvavelOP = `provavelOP` · Detalhe = `detalhe` · Acao = `acao` · QuemResolve = `quemResolve` · Cabine = `cabine`.
  **Não mexa** em Tratativa, Responsavel, DataTratativa nem DataDeteccao: são da tela.
- **Não** → SharePoint *Criar item*: os mesmos campos **+ DataDeteccao = `dataRef`**.

**3.10 E-mail.** Outlook *Enviar um email (V2)*: Para = você (e quem mais precisar) · Assunto = **assunto** (dinâmico do Conferir) · Corpo: clique em `</>` (modo código) e coloque só o dinâmico **html** · Importância = `if(greater(outputs('Conferir')?['body/result/naoConformes'],0),'High','Normal')`.

**3.11 Aviso de falha.** Depois do escopo `Conferir`, um escopo `Avisar_falha` com *Configurar execução após* = "falhou" e "atingiu o tempo limite". Dentro dele, um e-mail "Conferência GMS × SAP NÃO rodou hoje" com este link da execução:
`concat('https://make.powerautomate.com/environments/', workflow()?['tags']?['environmentName'], '/flows/', workflow()?['name'], '/runs/', workflow()?['run']?['name'])`.
Sem esse escopo, um dia sem e-mail parece um dia sem problema.

**Primeira execução:** rode manualmente (Testar → Manualmente). Confira três coisas: o e-mail chegou, a lista ganhou um item por pendência, e um segundo teste em seguida **atualizou** os mesmos itens em vez de duplicar.

---

## Passo 4 · App (GMS)

1. **App.Formulas**: cole a §16 do `Telas/Formulas.txt` (de `//  §16 · CONFERÊNCIA` até o fim) no fim do App.Formulas do Studio.
2. **Dados → Adicionar dados → SharePoint → OperationsGuaratingueta → Conferencia_SAP.** É lista de resultado do C29: o app só lê e grava a tratativa.
3. **Tela nova**: importe `Telas/scr_ConferenciaSAP.txt` (tela inteira, nomes com sufixo `Conf`, nenhum colide com tela existente).
4. **Gestão**: na `scr_SelecaoGestao_1`, cole os 8 controles de `COLAR_Gestao_card_Conferencia.yaml` (card largo em Y 530, embaixo dos dois existentes; nenhum controle existente muda de lugar) e troque o texto de `lbl_VersaoGest` para `"Versão 0.2.0"`.
5. Publicar com comentário: `Conferência SAP v0.1.0 + Gestão v0.2.0 + Formulas v3.0.4 (MEL-196)`.

**Checklist antes do publish (B §7.2):** App Checker sem item novo · teste de barreira dupla: escolher uma pendência **Resolvida** (filtro "Resolvidas recentes") e confirmar que Salvar/Justificar ficam desabilitados e que, forçando o clique, aparece o aviso · teste offline: derrubar a rede, salvar tratativa e ver o aviso de falha · conferir 1 OP da tela contra o e-mail do mesmo dia (mesmos números).

---

## Arquivos desta pasta

| Arquivo | O que é |
|---|---|
| `GMS_ConferenciaDiaria.ts` | Motor (Office Script). Lê o MB51 da própria planilha e recebe GMS + Packing do fluxo |
| `GMS_LerPacking.ts` | Lê a aba `Data Base` do BD Packing List (não precisa de tabela formatada) |
| `COLAR_Gestao_card_Conferencia.yaml` | 8 controles do card novo na Gestão |
| `Exemplo_Email_2026-10-01.html` | E-mail real gerado pelo motor contra o export de 02/10 (dia conferido 01/10) |
| `../Telas/scr_ConferenciaSAP.txt` | Tela nova (QA verde) |
