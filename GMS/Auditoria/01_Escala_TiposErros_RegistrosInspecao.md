# Auditoria GMS — 01 · Escala de `TiposErros` e `RegistrosInspeção` (apontamento de erro na cabine)

Fonte dos números: `Sharepoint Data GMS/RegistrosInspeção.csv` e `TiposErros.csv` (export até **02/10/2026**; datas em M/D/AAAA).
Código lido: `scr_Finalização_1.txt`, `scr_ConsultaOP_1.txt`, `OnStart.txt`.

## 1. Tamanho real (maior que "2 mil")

| | RegistrosInspeção | TiposErros |
|---|---|---|
| Linhas hoje | **16.542** | **5.434** |
| Primeiro dado | 11/11/2025 (uso real desde fev/2026) | 11/11/2025 (idem) |
| Ritmo (últimos 90 dias) | ~55 linhas/dia (pico 160) | ~22 linhas/dia (pico 70) |
| Ritmo (últimos 30 dias) | ~81/dia | ~38/dia |
| Projeção em 12 meses | ~36.700 | ~13.500 |
| Maior OP | 35 linhas | 29 linhas |
| OPs distintas | 2.226 | 1.612 |
| `OP_ID` | 100% numérico, nenhum vazio | 100% numérico, nenhum vazio |
| `cabine_teste` em branco | 96% (15.862) | 94% (5.087) — só as linhas recentes têm cabine |

Duas listas, dois limites diferentes:
- **Limite de linhas do app (2.000)** — `DefaultConnectedDataSourceMaxGetRowsCount = 2000` (já no máximo). Afeta consultas que o
  SharePoint não consegue filtrar (não delegáveis).
- **Limite de exibição de lista do SharePoint (5.000)** — as **duas listas já passaram dele** (`RegistrosInspeção` há meses,
  `TiposErros` em set/2026). Consulta que filtra coluna **sem índice** numa lista acima disso é recusada pelo SharePoint.

## 2. O que o código faz hoje (e por que o volume por consulta é seguro)

Todo acesso a essas listas é uma destas formas:
- `Filter(<lista>, OP_ID = <OP>)` → no máximo **35** linhas (inspeção) / **29** (refugo) por OP. Delegável (`=` em coluna número).
- `Filter(RegistrosInspeção, Created >= ctxIniDiaExt, Created < ctxFimDiaExt)` (Finalização, "hoje na cabine") → no máximo
  **160** linhas por dia. Delegável (`>=`/`<` em data).
- `Patch`/`Remove` por registro.
- `Sum(Filter(... OP_ID = X ...), Quantidade)` e `CountRows(Filter(...))` na ConsultaOP: o SharePoint não delega `Sum`/`CountRows`
  (documentação oficial), mas o `Filter` interno delega, então a soma roda localmente sobre as poucas linhas da OP. Correto.

Conclusão: **o app não depende de trazer mais de 2.000 linhas em nenhum caso de uso**. Não precisa de mudança de fórmula para o
volume atual nem para 5× o volume.

## 3. Onde a referência pode se perder (o risco de verdade)

O único ponto de falha é o **índice**. Sem índice em `OP_ID` e em `Created`, o SharePoint recusa a consulta (lista acima de 5.000)
e a tela pode mostrar **lista vazia no lugar de erro** — o operador acha que não há lance/refugo registrado naquela OP.

Eu não consigo ver as configurações da lista daqui. Se a Finalização está funcionando hoje com 16 mil linhas, `OP_ID` e `Created`
em `RegistrosInspeção` provavelmente já têm índice; **`TiposErros` cruzou 5.000 em setembro** e é o mais exposto.

### Passos no SharePoint (William) — 5 minutos por lista
1. Lista → engrenagem → **Configurações da lista** → **Colunas indexadas** (ou "Indexed columns").
2. Conferir se existem índices em **`OP_ID`** e em **`Criado` (Created)**. Se faltar, **Criar um novo índice** nas duas colunas.
3. Fazer nas duas listas: `RegistrosInspeção` e `TiposErros`.
4. Se o SharePoint recusar criar índice por a lista já ter mais de 5.000 itens, me avise: o caminho muda (visão filtrada ou
   arquivar linhas antigas antes).
5. Validar no Power Apps Studio → **Monitor**: abrir a Finalização, selecionar uma OP e conferir que as chamadas a
   `RegistrosInspeção` e `TiposErros` voltam sem erro de limite.

## 4. Retenção: a cabine precisa de no máximo 1 semana (William, 05/10/2026)

Com 7 dias de retenção as listas vivas ficam com ~390 linhas (`RegistrosInspeção`, 55/dia) e ~150 (`TiposErros`, 22/dia): voltam para
muito abaixo do limite de 5.000 e deixam de depender de índice para funcionar. O histórico sai das listas vivas e vai para arquivo.
O índice em `OP_ID` e `Criado` continua valendo como seguro, e é o que permite a carga inicial abaixo.

### Regra do fluxo (Power Automate agendado, 1x por dia, de madrugada)
1. Para cada lista, pegar as linhas com `Criado` **anterior a 7 dias**.
2. **Exceto** linhas de OP ainda aberta (`ficha_producao.processo <> "Finalizado"`): OP parada há mais de 7 dias continua na fila da
   Finalização, e o operador não pode perder o lance/refugo dela (a OP zumbi da auditoria tinha 4.162 h).
3. Copiar as linhas para `RegistrosInspeção_Arquivo` / `TiposErros_Arquivo` (mesmas colunas) e **só depois** apagar da lista viva.
4. O BI passa a ler a lista viva + a de arquivo (união), senão o histórico some dos relatórios.

### Carga inicial (destrutiva — fazer em etapas, com conferência)
1. Criar as duas listas de arquivo com as mesmas colunas e índice em `OP_ID` e `Criado`.
2. **Copiar** (não mover) as ~16,5 mil + ~5,4 mil linhas antigas para o arquivo.
3. Conferir contagem: arquivo + vivo = total do export (16.542 e 5.434 em 02/10).
4. Atualizar o BI para ler as duas.
5. Só então apagar da lista viva o que já está no arquivo.
Não executei nada disso: precisa de acesso ao SharePoint e ao Power Automate, e apaga dados.

### Efeito colateral que precisa de decisão
A `scr_ConsultaOP_1` mostra lances e refugo de **qualquer OP** (`Filter(RegistrosInspeção, OP_ID = ...)`). Depois do arquivamento, uma OP
com mais de 7 dias fecha com "0 REGISTROS" nessa tela, embora o dado exista no arquivo. Opções: aceitar (a consulta serve só à
semana corrente) ou a ConsultaOP ler o arquivo quando a lista viva vier vazia. Fica para a auditoria da `scr_ConsultaOP_1`.

## 5. O que já foi feito no código (esta rodada)

- Removida do `OnStart` a carga `colSup_Refugo` (`Filter(TiposErros, DateValue(Created,"en-US") >= Today())`): era **não delegável**,
  lia só as primeiras 2.000 linhas de uma lista de 5.434 e nenhuma tela usava o resultado.

## 6. Entra na auditoria da `scr_Finalização_1` (próxima etapa)

- Envolver as ~10 cargas `ClearCollect(colLancesExt/colRefugoExt/colInspDiaExt, Filter(...))` em `IfError` + `Notify`, para que
  falha de leitura nunca vire "lista vazia" silenciosa.
- Ler a tela inteira (3.085 linhas) antes de propor qualquer outra mudança.

## 7. Dados: observações do CSV
- `TiposErros`: `Turno Erro` em branco em 971 linhas e `DataHoraRefugo` em branco em 358 (histórico anterior aos campos).
- `RegistrosInspeção`: `TurnoTeste` em branco em 21 linhas.
