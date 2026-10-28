# GMS_Tempos_Sync: PN prod time.xlsx → lista Tempos_Montagem (28/10/2026)

Por quê: a fonte `Tempos` do app (Material, TempoMinPc; 3.995 linhas) estava **embutida no .msapp**, igual à aba **Tempos Montagem**
(tabela `Tempos_montagem`) do `PN prod time.xlsx`. Qualquer atualização do Luis exigia reimportar e republicar. Agora o fluxo copia o Excel para a lista.

## Feito em 28/10/2026
- Lista `Tempos_Montagem` criada no site (vazia, 0 itens): `Title` com nome de exibição **Material** (indexado) e `TempoMinPc` (número).
  Com esses nomes as fórmulas do app (`LookUp(Tempos, Material = ...).TempoMinPc`) não mudam.
- Script `GMS_LerTemposMontagem.ts` (nesta pasta). Falta gravar no OneDrive: pasta sincronizada `Documents\Office Scripts`
  como `GMS_LerTemposMontagem_v100` (a REST dá 403, igual ao GMS_LerPlanoOPs).

## Fluxo GMS_Tempos_Sync (montar no Power Automate)
1. **Gatilho**: SharePoint, *Quando um arquivo é criado ou modificado (somente propriedades)* ou *(propriedades e conteúdo)* —
   biblioteca Documents, pasta `/Apps/Relatórios`. Condição: `Nome do arquivo com extensão` = `PN prod time.xlsx`.
   Para não rodar em cascata, em *Configurações* do gatilho: concorrência 1 e, se a edição disparar várias vezes, adicione *Delay* de 2 min.
2. **Get items** (Tempos_Montagem): *Top Count* 5000, paginação ligada com limite 5000. Selecionar colunas: `ID,Title,TempoMinPc`.
3. **Select** (de `value`): `id` = `item()?['ID']`, `m` = `item()?['Title']`, `t` = `item()?['TempoMinPc']`.
4. **Run script** (Excel Online (Business)): Local `OneDrive`/ `Documents`, arquivo `PN prod time.xlsx` (caminho da biblioteca, não cópia),
   script `GMS_LerTemposMontagem_v100`, `existentesJson` = `string(body('Select'))`.
5. **Parse JSON** da saída (`result`): esquema `{total, novos[{m,t}], alterados[{id,m,t}], duplicados, invalidos}`.
6. **Apply to each** em `novos` (concorrência 20): *Create item* em `Tempos_Montagem` — `Title` = `m`, `TempoMinPc` = `t`.
7. **Apply to each** em `alterados` (concorrência 20): *Update item* — `Id` = `id`, `Title` = `m`, `TempoMinPc` = `t`.
8. **Aviso de falha**: ramo *configurar execução após* (has failed / has timed out) no último passo → *Enviar e-mail (V2)* para
   william.amorim@danfoss.com, assunto `GMS_Tempos_Sync falhou`, com o link da execução.
9. Opcional: e-mail curto com `novos`, `alterados`, `duplicados`, `invalidos` quando `invalidos` ou `duplicados` forem > 0.

## Carga inicial e conferência
- Primeira execução: `novos` ≈ 3.995 (lista vazia). Pode passar de 10 min; rode uma vez à mão.
- Conferir: `ItemCount` da lista = 3.995 e valores iguais à aba. Segunda execução imediata deve dar `novos` = 0 e `alterados` = 0.
- Limite do conector: arquivo de 6,5 MB com uma aba de 61 MB descompactada (Routing). Se o *Run script* reclamar de tamanho,
  pedir ao Luis um arquivo só com a aba Tempos Montagem.

## Depois (no Studio, William publica)
- Adicionar a fonte `Tempos_Montagem` e trocar `Tempos` (estática) por ela; as fórmulas não mudam (Material / TempoMinPc).
  `LookUp` por `Material =` em lista SharePoint é delegável; a coluna está indexada. Respeitar a lição 4.4 (sem LookUp em propriedade de pintura).
- Quando estiver validado, remover a fonte estática `Tempos` do app.
