# Como arrumar a lista Hora-Hora e o BI (roteiro para sessões novas)

Escrito em 28/10/2026 depois de uma sessão longa (23 a 28/10) em que tudo isto foi feito e dado certo. Serve para uma sessão
nova repetir sem redescobrir. Leia inteiro antes de mexer. Regras de aprovação no fim do arquivo.

## 0. Mapa rápido

| Coisa | Onde |
|---|---|
| Lista (o "banco de dados") | SharePoint `https://danfoss.sharepoint.com/sites/OperationsGuaratingueta`, lista **Hora-Hora**. Tela: `/Lists/HoraHora/AllItems.aspx`. REST: `_api/web/lists/getbytitle('Hora-Hora')` |
| Modelo semântico `(GMS)` | Workspace `629ca442-8019-47e0-83e4-0d48b2d30974`, modelo `b48699da-af0b-4f0e-9b2e-f89cc657dbc1` |
| Visão DAX | `https://app.powerbi.com/groups/629ca442-8019-47e0-83e4-0d48b2d30974/modeling/b48699da-af0b-4f0e-9b2e-f89cc657dbc1/daxQueryView?experience=power-bi` |
| Visão TMDL | mesma URL trocando `daxQueryView` por `tmdlView` |
| Configurações do modelo (agendamento) | `https://app.powerbi.com/groups/629ca442-8019-47e0-83e4-0d48b2d30974/settings/datasets/b48699da-af0b-4f0e-9b2e-f89cc657dbc1?experience=power-bi` |
| Relatório (arquivos) | `GMS/PowerBI/GMS_Painel.Report/definition/` (PBIR). Medidas do relatório em `reportExtensions.json` |
| Documentos do BI | `GMS/PowerBI/modelo/fHoraHora.tmdl.md` e `fHoraHora_dia_produtivo.tmdl.md`; norma em `GMS_Mestre_BI.md` |
| Regra do app | `GMS/Telas/scr_HoraHora_Trancagem_2.txt` (Fechar turno, linhas 1184 a 1208) e `Telas/Formulas.txt` (seção §4 Tempo) |
| Backups e CSVs | `GMS/Analises/Higienizacao_HoraHora/` (só locais, fora do git) |
| Diário | `GMS/GMS_Diario.md` (acrescentar linhas; `python gms.py --check`) |

## 1. Colunas da lista (nomes internos, os que a API usa)

`Title` = "DD/MM/AAAA - Nº Turno - CÉLULA" · `field_0` Data (meia-noite local gravada como `...T03:00:00Z`; data de produção do turno) ·
`field_2` Célula · `field_3` Hora (rótulo da janela) · `field_4` Mangueira · `field_5` Meta Hora · `field_6` Meta Acum · `field_7` Real. Hora ·
`field_8` Real. Acum · `field_9` Diferença (Meta − Real) · `field_11` Tempo Parado (min) · `field_12` Motivo · `field_13` Motivo 2 ·
`field_14` Comentário · `field_15` Rendimento (%) · `TurnoH` Turno ("1º Turno" etc.) · `Status` ("Finalizado") · `Minutos` (duração da janela).

Janelas e minutos de um dia (o dia de produção vai de 05:20 a 05:20; o 3º turno fica com a Data do dia em que começa):

| Turno | Janelas (rótulo : minutos) |
|---|---|
| 1º | 05:20 - 06:00 : 40 · 06:00 - 07:00 … 12:00 - 13:00 : 60 cada · 13:00 - 13:57 : 57 (total 517) |
| 2º | 13:47 - 15:00 : 63 · 15:00 - 16:00 … 21:00 - 22:00 : 60 cada · 22:00 - 22:20 : 41 (total 524) |
| 3º | 22:20 - 23:00 : **19** · 23:00 - 00:00 … 04:00 - 05:00 : 60 cada · 05:00 - 05:20 : 20 (total 399) |

Os rótulos `13:47` e `22:20` são antigos: o app troca de turno às **13:57** e **22:41** (Formulas.txt §4). Por isso 19 e 41 minutos. Não "corrigir" para 40 sem decisão do William.
Motivos oficiais: `fx_MotivosParada` em `Telas/Formulas.txt` (ex.: "Amostra", "Refeição", "Almoço", "Motivo Não Declarado"). Em outubro os motivos são sem número; em setembro tinham "21 - Refeição".

## 2. Preparar o ambiente (a parte que mais dá errado)

1. **Painel do navegador largo e visível.** Se estiver estreito (< 600 px) ou oculto, o Power BI não desenha e os cliques erram. Peça ao William para abrir e alargar. `resize_window` com emulação costuma piorar.
2. Se cair na tela de login da Microsoft, **peça ao William para entrar** (não digitar senha por ele). Depois voltar para a URL.
3. Screenshots **atrasam um passo**: espere 2 a 3 s e tire outro antes de concluir que algo não funcionou.
4. No editor DAX/TMDL (Monaco): `type` digita bem. Para executar use o botão **Run** (clique) — `ctrl+Enter` às vezes não dispara. `Update model with changes` só habilita depois de **clicar dentro do editor**.
5. Os resultados da consulta DAX ficam num painel que **não é texto da página**. Leia por screenshot/zoom e **role a grade para a direita** (`scroll right`, no máximo 10 por vez). Para ler muitas colunas, faça consultas com poucas colunas.
6. No shell do navegador, `javascript_tool` serve para **ler** o SharePoint (REST) e para os lotes aprovados pelo William. Ele roda na origem `danfoss.sharepoint.com`, então a aba precisa estar numa página de lá.

## 3. Ler a lista em JavaScript (SharePoint REST)

Armadilhas já pagas:
- Filtro por `field_0` (Data) estoura o **limite de visualização de lista (5.000)**. **Filtrar e paginar por faixas de ID**: `$filter=ID ge A and ID lt A+1500&$top=1500`.
- `GET .../items(ID)` devolve **Atom/XML** mesmo com `Accept` JSON. Use `GET .../items?$filter=ID eq N` (coleção) com `Accept: application/json;odata=verbose` e leia `d.results`, ou `odata=nometadata` e leia `value`.
- Em alguns casos `$select` junto de `$filter` volta XML; sem `$select` funciona. Sempre `await r.text()` + `JSON.parse` dentro de `try` para não quebrar o lote.
- `contextinfo` (POST) devolve o digest: `fetch(site+'/_api/contextinfo',{method:'POST',headers:{Accept:'application/json;odata=verbose'}})`, e o valor está em `"FormDigestValue":"..."` (use regex no texto).
- Guarde as linhas em `window.__x` para reutilizar na mesma aba (se navegar para outra URL, perde).

Padrão de leitura de todo o histórico:
```js
const jh={headers:{Accept:'application/json;odata=nometadata'}};
const base="https://danfoss.sharepoint.com/sites/OperationsGuaratingueta/_api/web/lists/getbytitle('Hora-Hora')";
let rows=[]; for(let a=0;a<32000;a+=1500){ const t=await (await fetch(base+`/items?$filter=ID ge ${a} and ID lt ${a+1500}&$top=1500`,jh)).text(); try{rows=rows.concat(JSON.parse(t).value||[]);}catch(e){} }
```

## 4. Saúde do apontamento: o que checar e como corrigir

Regra do app ("Fechar turno", `scr_HoraHora_Trancagem_2.txt` linhas 1184 a 1208) — vale para janelas **fechadas**, com `Minutos > 0` e `Meta > 0`:
- abaixo da meta = `Real < Meta`;
- **ND**: abaixo da meta e Motivo vazio → Motivo = "Motivo Não Declarado" e Tempo Parado = `min(Minutos, round(Minutos × (Meta − Real) ÷ Meta))`;
- **NT**: abaixo da meta, Motivo preenchido e Tempo Parado ≤ 0 → Tempo Parado = o mesmo proporcional (o motivo fica);
- **CAP**: Tempo Parado > Minutos → Tempo Parado = Minutos.

Fora do "óbvio" (não corrigir sem o William decidir item a item):
- **Velocidade errada**: meta por minuto fora do padrão da mesma máquina e mangueira. Em outubro todas as 95 linhas eram de **TH01 e TO04 (duas passadas, MEL-241)**; a decisão da meta das duas passadas está **adiada pelo William**.
- Mangueira ≠ OP em processo, duplicados com conteúdo diferente, Title ≠ Célula, Data ≠ Title: ver `LEIA-ME.md` desta pasta (MEL-243) e os CSVs.
- **Janeiro até 03/09/2026**: sem `Minutos` (coluna nasceu em 03/09, MEL-100) e meta antiga inflada (MEL-106). Não há base para o proporcional; não alterar.
- **O dia de hoje**: janelas ainda abertas. Pular `Data` ≥ hoje.

Varredura (só leitura) e lista de correções:
```js
const n=v=>v==null?0:Number(v), blank=s=>!s||String(s).trim()==='';
const fix=[];
for(const x of rows){ if(x.field_0.slice(0,10)>=HOJE) continue;
  const meta=n(x.field_5),real=n(x.field_7),par=n(x.field_11),min=n(x.Minutos); if(!(min>0&&meta>0)) continue;
  const dev=real<meta, ND=dev&&blank(x.field_12), NT=dev&&!blank(x.field_12)&&par<=0;
  let novo=par,mot=x.field_12,tipo='';
  if(ND||NT){novo=Math.min(min,Math.round(min*(meta-real)/meta));tipo=ND?'ND':'NT';if(ND)mot='Motivo Não Declarado';}
  if(novo>min){novo=min;tipo=tipo?tipo+'+CAP':'CAP';}
  if(tipo) fix.push([x.ID,x.field_0.slice(0,10),x.field_2,x.field_3,x.TurnoH,min,meta,real,par,x.field_12||'',novo,mot||'',tipo].join(';'));
}
```
Em 23/10 isso deu 80 casos (30/09 a 22/10) e 79 (04 a 29/09). Depois de aplicar, a releitura deve dar 0, 0 e 0.

### Gravar (só com o "Libero" do William para o lote)
1. **Backup antes**: escreva um CSV com o valor de antes e o novo em `Analises/Higienizacao_HoraHora/` (ex.: `HoraHora_saude_apontamento_AAAA-MM-DD.csv`). Use a ferramenta Write (heredoc com acentos falhou uma vez).
2. Para cada item: **reler** e só gravar se `field_11` e `field_12` ainda forem os que você leu; senão, pular e relatar.
3. Gravar com MERGE:
```js
const vh={Accept:'application/json;odata=verbose'};
const dig=(await (await fetch(site+'/_api/contextinfo',{method:'POST',headers:vh})).text()).match(/"FormDigestValue":"([^"]+)"/)[1];
const tipoEnt=(await fetch(base+'?$select=ListItemEntityTypeFullName',{headers:vh}).then(r=>r.json())).d.ListItemEntityTypeFullName;
await fetch(base+'/items('+id+')',{method:'POST',headers:{...vh,'Content-Type':'application/json;odata=verbose','IF-MATCH':'*','X-HTTP-Method':'MERGE','X-RequestDigest':dig},body:JSON.stringify({__metadata:{type:tipoEnt},field_11:novoParado /*,field_12:'Motivo Não Declarado' só no ND*/}));
```
Lotes de ~40 por chamada. Testar com 3 primeiro e reler o item.
4. **Reler a lista inteira** e mostrar zero casos.

## 5. Criar linhas que faltam (ex.: noite sem registro)
1. Confirmar por leitura que **não existe** registro daquela `Data` + `TurnoH` + `Célula` (e checar de novo antes de gravar).
2. Pegar como modelo a **noite anterior da mesma máquina** (mangueira, meta por janela). Meta Acum e Real Acum acumulam na ordem das janelas; `field_9 = Meta − Real`; `Rendimento = Real/Meta×100`.
3. Parada total: `Real = 0`, `Tempo Parado = Minutos` da janela, só `field_12` preenchido (Motivo 2 vazio); `Status = "Finalizado"`.
4. `POST base+'/items'` com `__metadata.type` e `field_0 = 'AAAA-MM-DDT03:00:00Z'`. Relê e confere a soma de minutos do turno (1º 517, 2º 524, 3º 399) e a meta contra a noite modelo.
Exemplo feito: TH06, noite 23/10, IDs 31374 a 31381.

## 6. Excluir linhas (só lixeira, nunca definitivo)
- Pela **tela da lista** (não por script): `.../Lists/HoraHora/AllItems.aspx?FilterField1=ID&FilterValue1=<ID>&FilterType1=Counter`, esperar carregar, **conferir o título do item**, clicar na bolinha da linha, menu `...` da barra, `Delete`, confirmar ("send this item to the recycle bin"). Depois reler pela API: o ID não pode mais existir.
- Confira a barra de comandos a cada item: às vezes aparece um ícone extra e o `...` muda de lugar (os cliques erram o alvo).
- Esvaziar a lixeira ou apagar em definitivo: **nunca**. Recuperável por 93 dias.

## 7. O modelo (GMS) no Power BI

Colunas BI na `fHoraHora` (docs em `PowerBI/modelo/fHoraHora_dia_produtivo.tmdl.md`):
`Data BI` (= `Data`, regra 05:20 a 05:20) · `HoraOrdem BI` (= `HoraOrdem`) · `Hora BI` (cópia da `Hora`, ordena por `HoraOrdem BI`; **a `Hora` não pode ordenar por coluna que a lê: dependência circular**) ·
`Minutos BI` (13:00-13:57 −10 e 13:47-15:00 +10) · `Meta Hora BI` (proporcional aos minutos fora de "Almoço") · `Real BI` e `Parado BI` (10/57 passa da janela 13:00-13:57 para a 13:47-15:00 da mesma máquina e dia).
Relacionamento ativo `fHoraHora[Data BI]` → `dCalendario[Date]`; o antigo por `Data` (`7c1e5b2a-4d36-4f9b-a8e0-2b6d9c3f1a47`) ficou inativo. O aviso "Cannot convert value '' of type Text to type Number" vinha de `VALUE` em coluna calculada: use `IFERROR`.

### Alterar coluna ou relacionamento (TMDL View, "Apply")
- **O editor soma a indentação**: digite as linhas **sem espaços à esquerda** e use as teclas `Tab` (aprofundar) e `shift+Tab` (recuar). Estrutura: `createOrReplace` / Tab `ref table fHoraHora` / Tab `column 'X' =` / Tab Tab *expressão* / `Escape shift+Tab` / propriedades (`dataType`, `formatString`, `summarizeBy`, `isHidden`, `sortByColumn`).
- `Escape` depois de digitar fecha o autocompletar (não use Enter sobre a sugestão).
- Para editar um bloco existente **apague tudo e redigite o script inteiro**; editar no meio por `ctrl+g` já corrompeu o script.
- Um aviso do editor para coluna que nasce no mesmo script ("Minutos BI" não resolvido) é esperado.
- Depois de aplicar, **as colunas calculadas só têm valor depois de um refresh**. Consulta antes disso dá "needs to be recalculated or refreshed".
- Nome duplicado: o documento M já tem uma consulta chamada `Refugo_Bobinadeira` (por isso a tabela nova se chama `Refugo_Bobinadeira_SP`).

### Alterar medida (DAX query view)
`DEFINE` + `MEASURE 'Tabela'[Nome] =` e a expressão em **várias linhas** (em uma linha só o editor não reconhece). Aparece "Overwrite measure" e `Update model with changes (1)`; clique no editor, depois no botão, depois "Update model". Termine com `EVALUATE ROW(...)` para testar antes.

### Armadilhas de DAX (já erradas uma vez)
- `CALCULATE(SUM(x), col <> "Almoço")` **substitui o filtro do eixo** da mesma coluna e mostra o total em todas as barras. Use `KEEPFILTERS(col <> "Almoço")`.
- Medida/coluna que faz `VALUE("")` quebra: `IFERROR`.
- Para medir só leitura use `SUMMARIZECOLUMNS`/`CALCULATETABLE`; para ver quem está em erro: `INFO.MEASURES()` e `INFO.COLUMNS()` com `[State] <> 1` (deu 0 em 23/10).

### Atualizar o relatório
O relatório é **PBIR em arquivos** (`GMS_Painel.Report`). Edite os JSON com Python (`json.load`/`dump`, `indent=2`, `ensure_ascii=False`, preservando a quebra de linha) e **não regere o layout por cima**: desde 26/10 o layout salvo no Desktop é o vigente (memória `feedback_layout_bi_salvo`). Quem **publica é o William**, pelo Desktop; ele precisa **reabrir o projeto** para pegar o que você mudou nos arquivos, senão o Desktop sobrescreve.
Depois de qualquer mudança no modelo: pedir **refresh** ao William antes de validar e antes de trocar medida que lê coluna nova.

### Agendamento de atualização
Limite de **8 horários por dia** na capacidade compartilhada (também vale para API e "Atualizar agora"). Erro 400 ao salvar 28 horários foi isso. Mais exige Premium/PPU/Fabric. O William preferiu deixar como está (08:00, 10:30, 13:00, 13:30, 14:00, 16:00, 17:30, 20:00).

## 8. Validar com um caso real
Escolha uma máquina e um dia (usamos TH07). Compare `minutos BI` por turno (1º 507, 2º 534, 3º 399, total 1.440), meta BI, real e parado com o rodapé do app (as somas da tela). O app só mostra o dia corrente. O parado do BI exclui "Almoço"; o campo bruto não.

## 9. Fechar o ciclo (sempre)
1. Diário: linhas `DATA | TIPO | ALVO | VER | REF | TEXTO` (só os 13 tipos) e `python gms.py --check`.
2. `git add` **só os arquivos do assunto**: o repositório tem dezenas de arquivos do relatório alterados pelo Desktop que não são seus.
3. `git commit` com `Co-Authored-By` e `git pull --rebase --autostash origin main` antes do push (outras sessões commitam no mesmo repositório); `git push origin HEAD:main`.
4. `registro.md` e `preferencias.md` em `.claude/orquestracao/` ao final da demanda.

## 10. Permissões e o que o William já decidiu
- O sistema bloqueia escrita em recurso compartilhado (SharePoint, modelo) quando o "sim" não está claro. Peça no chat **"Libero: …"** para cada lote/ação, mostrando o número de itens e o backup. Um "sim" vale para uma ação.
- Apagar dado em definitivo: nunca (só lixeira, a pedido). Entrar em conta, aceitar permissões do app/Microsoft: é do William.
- Decisões em vigor: dia produtivo 05:20 a 05:20; hora do jantar conta com meta proporcional e refeição fora de Parado e Principal parada; 10 min de 13:47 a 13:57 vão para o 2º turno (minutos, meta, real e parado); janeiro a 03/09 não se mexe; meta das duas passadas adiada; atualização com 8 horários.
- Pendências abertas na data: refresh e publicação do relatório com `Real BI`/`Parado BI`; atualizar a medida do modelo `'Hora-Hora'[Real HH]` para `SUM(fHoraHora[Real BI])` (só depois do refresh); decisão da meta das duas passadas (MEL-241).

## Precedentes na pasta
- `LOG_TH07_2026-10-26_manutencao_preventiva.txt` e o `.tsv` ao lado: outra sessão gravou o 2º e o 3º turno da TH07 de 26/10 (17 itens, IDs 31551 a 31567, motivo Manutenção Preventiva), no mesmo padrão da seção 5. Para desfazer, os IDs vão para a lixeira da lista.
- TH06, noite 23/10, motivo "Amostra": IDs 31374 a 31381.

## 11. Atualização de 30/10/2026 (o que mudou e como se faz)

### Decisões que substituem as da seção 10
- **Meta do BI NÃO é proporcional à refeição.** `Meta Hora BI = Meta Hora × Minutos BI ÷ Minutos` (VAR ref = 0). A hora do jantar mostra a meta cheia. A decisão de 23/10 ("meta proporcional") foi revogada pelo William em 30/10.
- **Regra dos 21h45 (1305/1440)**: vale só nas medidas do relatório `HH Meta Útil (m)` (cartão Meta) e `HH Aderência`, e só quando nenhuma hora está filtrada: `SUM(fHoraHora[Meta Hora BI]) * IF(ISFILTERED(fHoraHora[Hora BI]), 1, 1305/1440)`. A pausa é de 45 min em cada um dos 3 turnos (135 min/dia), a mesma do OEE2. Era 21h35 (1295/1440) até 09/11/2026, quando o William alinhou a regra com a pausa do OEE2 (MEL-266). As barras por hora usam a meta cheia. Medida de relatório não pode referenciar outra medida de relatório (erro semântico): copie a expressão.
- Parado e Principal parada seguem sem refeição ("Almoço" do Motivo Padrão).

### Como fazer, com o navegador do app (testado)
- **Abas**: a aba `seed` fica no SharePoint (leitura e gravação REST pelo `javascript_tool`) e a `tab-1` no Power BI. Não é preciso o Chrome com a extensão.
- **Editar uma coluna calculada**: TMDL view, clique direito na tabela no painel de dados, "Script TMDL to" > "Script tab". Isso gera o script com `dataType`, `formatString` e `lineTag`. Clique no começo da linha a mudar, `shift`+clique no fim, digite a linha nova, `Escape`, botão **Apply** e espere "Changes applied to the model". A coluna só recalcula depois do refresh.
- **Refresh**: página do workspace `.../groups/<id>/list`, botão "Refresh now" da linha do semantic model "(GMS)". Se o clique der "ref stale", não repita: confira se já aparece "Cancel refresh" na linha (alguém já disparou). O William costuma disparar sozinho.
- **Esconder o rótulo de uma série no gráfico**: no `visual.json`, em `objects.labels`, acrescentar `{"properties":{"show":{"expr":{"Literal":{"Value":"false"}}}},"selector":{"metadata":"Medidas.<nome da medida>"}}`. Gravar com `json.dumps(indent=2, ensure_ascii=False)` e CRLF; o diff fica só com as linhas novas.
- **Criar linhas (seção 5)**: tipo do item `SP.Data.HoraHoraListItem`; `$select=ListItemEntityTypeFullName` só volta certo com `odata=nometadata` (devolve JSON direto, sem `.d`). Modelo: o mesmo turno do dia anterior da máquina. O 2º turno tem 9 janelas e o 3º tem 8 (17 linhas, minutos 524 e 399). Antes de gravar, releia e aborte se já houver linha. Conferência final: releia e conte (sem duplicata).
- **Retorno vazio do `javascript_tool`** depois de um POST não quer dizer que falhou: releia a lista antes de tentar de novo, para não duplicar.

### Como trabalhar com o William
- Pedido curto e coloquial (ex.: "TH7 só o 1º turno com manutenção, coloca em todos") quer dizer: leia a lista, ache a lacuna e faça. Pergunte só o que muda o resultado (dia e motivo, quando o texto e os dados divergem) e **use o que está nos dados, não o que ele disse de memória**: ele falou "corretiva" e a lista tinha "preventiva".
- Quando ele diz "libero", é o "sim" daquela ação. Se o sistema ainda bloquear a escrita (SharePoint, modelo), pare, diga o que ia gravar, deixe o backup pronto e peça que ele libere a permissão; **não tente contornar**. Uma nova tentativa depois do "Tento de novo" funcionou.
- Pergunta "e a lógica de X?": busque no `git log -S` e no diário antes de responder (os 21h35 estavam no commit `9aab50b`, de 22/10, e a ordem das mudanças explicou tudo).
- Explique um número do painel com a linha da lista que o gera (ex.: 116 × 13 ÷ 60 = 25). Mostra de onde vem e resolve a dúvida.
- Ao fim de cada ajuste: linha no diário (MEL-257 neste assunto), `python gms.py --check`, commit só dos arquivos do assunto, `pull --rebase --autostash`, push na main. O relatório só vale depois que o William reabre o projeto no Desktop e publica; o modelo só depois do refresh.
