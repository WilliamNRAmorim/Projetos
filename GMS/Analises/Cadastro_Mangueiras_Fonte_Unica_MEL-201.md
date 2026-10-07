# MEL-201: cadastro único de mangueiras (08/10/2026)

Problema: `colMangueiras` (todos os combos de mangueira) era uma lista de 70 códigos escrita à mão no `OnStart`. Mangueira nova só entrava depois de republicar o app, e até lá o operador usava "OUTRA (amostra ou nova)". Havia ainda duas listas convivendo (MEL-037): a dos combos e o delineamento de cada etapa.

## O que mudou
- `Telas/Formulas.txt` v3.0.10: `fx_MangueirasBase` (os 70 códigos de antes, **nenhum nome alterado**) e `fx_EhVersaoMang` (versão alternativa do delineamento, código terminado em `-2` ou `-02`).
- `Telas/OnStart.txt`: `colMangueiras` = base + todo `PARTNUMBER` de `DM_TRANÇAGEM` e `DM_TUBE_EXTRUSION` que não esteja na base (comparado por `fx_NormCodigo`) e não seja versão alternativa. Mangueira nova cadastrada no DM aparece no combo sem republicar.

## Aplicação da norma de banco de dados (08/10)
- **Lista nova?** Não. Reaproveita o delineamento que já é fonte do app (`DM_TRANÇAGEM`, `DM_TUBE_EXTRUSION`); a Máscara de produção (aba Cadastro Mangueiras, 95 itens) não está no repositório e seria uma lista a mais.
- **Carga do app:** acrescenta 2 leituras de Excel ao `OnStart` (cerca de 90 linhas cada), dentro do `Concurrent`. Se falhar, `colMangueiras` fica só com a base, igual a antes.
- **Limite de 5.000 itens:** não se aplica (fontes de 90 linhas).

## O que entra e o que fica de fora (calculado com os arquivos de `Engenharia/DM_DATABASE`)
- **23 mangueiras novas no combo**: EC115-04LRL, 06LRL, 08LRL, 10LRL, 12LRL, 16LRL; EC118-04LRL, 06LRL, 08LRL, 10LRL, 12LRL, 16LRL; EC215-06LRL, 10LRL, 12LRL, 16LRL; EC415-08, EC415-10, EC415-10L; FC639-16; H28004, H28006, H28008.
- **7 versões alternativas ficam fora**: EC118-04L-2, EC118-04LRL-2, EC215-06L-2, EC215-06LRL-2, FC839B-04-2, GH781-6-2, H28006-2.
- **7 códigos da base que não existem em nenhum DM** (legado): 2807-10, 2807-12, EC215-04, EC600-16, H28004-250R, H28006-250R, H28008-250R.

## Decisões que ficam com o William
1. **H28004, H28006, H28008 (do DM) × H28004-250R, H28006-250R, H28008-250R (da base)**: hoje aparecem os dois nos combos. Qual é o nome real que a produção usa nas fichas? O outro sai.
2. Os outros 4 códigos de legado (2807-10, 2807-12, EC215-04, EC600-16): existem ou podem sair da base?
3. Os sufixos `-2`/`-02` realmente são versões e não mangueiras? Se algum for mangueira própria, entra no combo mudando a regra.

## Para colar no Studio (ordem)
1. `Telas/Formulas.txt` (App.Formulas) primeiro.
2. `Telas/OnStart.txt` (App.OnStart). Rodar o OnStart de novo (ou reabrir o app) para ver a lista nova.
