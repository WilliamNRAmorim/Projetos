# Plano: incluir GH781-6-2 na lista de mangueiras do app (MEL-254)

Pedido do chão (áudio de 26/10 17:50) + foto da ficha do Tubo (GH781-6, Ø 0,465 acusando "fora da faixa 0,490 a 0,510").

## Evidência
- GH781-6-2 é produto real: DM_TRANÇAGEM/AMDM02_Spec tem a linha `GH781-6-2|DD240601` (construção diferente da GH781-6, DD200601); `aliases_mangueira.csv` já liga GH781-6-2 ao material SAP GH781-6 ("mesmo produto, nome diferente no SAP"); a ficha tem 4 registros e a inspeção 14 com esse nome.
- `colMangueiras` (OnStart, 70 itens, escrita à mão) NÃO tem GH781-6-2. O operador só consegue escolher GH781-6, cuja faixa de diâmetro no DM_TUBE_EXTRUSION é 0,490–0,510; daí o aviso falso.
- A faixa vem de `colSpecTubo` (DM_TUBE_EXTRUSION) por PARTNUMBER = mangueira escolhida. Sem linha para GH781-6-2 lá, a tela já mostra "Sem delineamento cadastrado… pode continuar sem faixa" (scr_tubo_1, linha 3305), sem bloquear.

## Mudança (1 arquivo)
- `Telas/OnStart.txt`: acrescentar `"GH781-6-2"` logo depois de `"GH781-6"` em `colMangueiras`. Os combos de Tubo, Bandagem, Cobertura, Vulcanização, Catenária e Trançagem leem essa coleção; nenhum mais precisa mudar.
- Não mexer em `fx_PNImpressao` (etiqueta continua imprimindo GH781-6 sem o "-2", de propósito) nem em `fx_MangCanon` (GH781-6-2 e GH781-6 continuam chaves distintas).

## Fora do app (Engenharia)
- DM_TUBE_EXTRUSION precisa de uma linha PARTNUMBER = GH781-6-2 com MIN_OD/MAX_OD certos (o chão sugere confirmar com a Engenharia). Até lá o app avisa "sem delineamento" e deixa continuar.

## Riscos / revisão
- Risco baixo: item novo numa lista; nada gravado muda. Registros antigos de GH781-6 não são reclassificados.
- Teste: abrir Tubo, escolher GH781-6-2 → aparece na lista, sem aviso de faixa errada (aviso "sem delineamento" até a Engenharia cadastrar); GH781-6 segue com 0,490–0,510.
- Publicar: colar o OnStart.txt no Studio e rodar o OnStart (reabrir o app).
- Observação: a ficha também tem `EC215-06L-2` (1 registro) fora da lista; não incluído sem pedido.
