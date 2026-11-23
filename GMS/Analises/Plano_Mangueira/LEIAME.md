# Plano de mangueira x SAP (página nova do GMS_Painel)

Status em 19/11/2026: **pronto no disco, NADA aplicado/publicado**. DAX não testado no modelo vivo (só balanceamento e conferência em Python).

## O que tem
- `conferir.py`: reproduz as medidas HP em Python (plano e classe da aba Dados, produzido da aba MB51 da planilha, unidade M). Mostra por C.Standard, Tipo e Arame com 22 e 23 dias úteis. `--hoje AAAA-MM-DD` simula o corte; `--sap MB51 COOIS` compara com a regra MRP AIH.
- `gerar_lista.py` e `nov_2026_lista.csv`: 45 linhas de novembro para a lista `GMS_PlanoMangueira` (Volume > 0 mais as de Volume 0 com produção; soma 162.016 m).
- `prototipo.py` e `prototipo.html`: prévia com o mesmo desenho das medidas.
- Modelo: `GMS/PowerBI/modelo/plano_mangueira.tmdl.md` (3 passos + decisões + verificação).
- Relatório: `pages/pg_plano_mangueira`, `pages.json`, botão `sub_plano_mangueira` em todas as páginas, 5 medidas `HP · SVG ...` no `reportExtensions.json`.

## Passos (William)
1. Gravar os itens do CSV na lista `GMS_PlanoMangueira` (o chefe grava).
2. Aplicar os 3 passos do `plano_mangueira.tmdl.md` no modelo vivo (depende do `mascara_producao.tmdl.md`), atualizar, rodar a verificação (seção 4 do .tmdl.md).
3. Reabrir `GMS_Painel.pbip`, conferir a página, publicar.

## Conferência (planilha x modelo)
- A planilha salva tem 13 dias e MTD 85.671 m (52,9%). Com `--hoje 2026-11-18` (corte 17/11, 13 dias) o script dá 85.746 m (52,9%); diferença de 2 linhas que mudaram na MB51 depois do cache (GH781-6 e 2556-12).
- Atraso difere por dias úteis: modelo 22 (GMS_MetaMensal), planilha 23 digitado.
- MRP AIH (COOIS) até 17/11: 85.746,1 m no plano e 0 m fora do plano, igual à MB51 da planilha. Todas as linhas AIH são unidade M.
