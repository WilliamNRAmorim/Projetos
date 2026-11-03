# Plano: levar o piloto "Fluxo Trançagem → Cabine" ao GMS_Painel (03/11/2026)

Status: **proposta, nada executado.** Precisa do "sim" do William por fase. Quem publica é o William; nenhum agente publica.

## O que existe hoje
- Piloto validado só na cópia local `GMS/PowerBI/Modelo_PBIP_teste` (modelo + 2 páginas, tema claro, SVG claro). KPIs conferidos contra o HTML.
- `GMS_Painel.Report` (repositório) é só a parte visual, ligada ao vivo ao modelo `(GMS)` do workspace "Controle de Fabricação". O modelo vive no serviço; o arquivo-fonte local de referência é o `(GMS).pbix` da pasta "BI Controle diário de produção - Mangueiras" (SharePoint).
- O modelo publicado **não tem** `fn_Turno`, `fn_DataRef`, `dTurno`, `dEtapa`, `fPessoasEtapaOP` nem a coluna `dCalendario[Mês/Ano]`. Tem `fHoraHora` e outras tabelas que o snapshot do repositório não tem (o snapshot é de um .pbix de 18 dias).
- `GMS_Painel.Report` está com 26 arquivos de visual modificados (alterações do William, não commitadas).

## Antes de tudo (decisões e pré-requisitos do William)
1. **Fuso:** conferir numa ficha conhecida se `ficha_producao` já está em hora local (padrão do piloto: `FichaJaEmHoraLocal = true`).
2. **Fronteira do 2º turno:** o piloto usa 13:57 (norma); `Etapas[Turno]` e `Turno_Producao` usam 13:40; `Turno Atual` usa 13:48. Decidir com o revisor. O piloto não altera as colunas existentes.
3. **Mês:** `dCalendario[Mês]` sem "Classificar por Mês Nº". O piloto usa a coluna nova `Mês/Ano`, mas outros visuais continuam em ordem alfabética até corrigir.
4. **ID MEL real** (`python gms.py --novo`) para as medidas (hoje `MEL-???`) e linhas DECISÃO no diário.
5. **Alterações pendentes do `GMS_Painel.Report`:** salvar/commitar o estado atual antes de qualquer coisa nova (regra: layout salvo é o vigente, não regerar por cima).

## Fase 1 — Modelo (cópia do arquivo-fonte, nunca o publicado)
1. Fazer uma cópia do `(GMS).pbix` atual (ou salvar o modelo ao vivo como projeto, se o William tiver acesso de edição) em pasta de trabalho fora do SharePoint.
2. Ler o TMDL real (`Medidas`, `dCalendario`, `ficha_producao`, `Etapas`) e conferir **colisão de nomes** com as 138+ medidas existentes e checar se já existem `dTurno`/`fn_*`.
3. Aplicar os blocos 0 a 4 e o 2b (funções, `dTurno`, `dEtapa`, `fPessoasEtapaOP`, relacionamentos, 54 medidas, SVG claro, coluna `Mês/Ano`) no TMDL view.
4. Rodar a consulta de conferência (`Consulta_Conferencia.dax`) e comparar com o HTML (eficiência 57%, CV 23%, rendimento ~85%).
5. Revisor (Opus) lê o diff de TMDL: regra de turno, nomenclatura, ligação por `Data de Referência`, contexto de filtro.
6. **Saída:** arquivo `.pbix`/projeto atualizado para o William revisar. **O William publica o modelo** (substitui o semântico no serviço). Plano de volta: manter o `.pbix` anterior intacto e o histórico de versões do serviço.

## Fase 2 — Páginas no GMS_Painel.Report
1. Só depois do modelo publicado e conferido.
2. Rodar `gerar_paginas_fluxo.py` numa **cópia** do `GMS_Painel.Report` (parâmetro do caminho e `--forcar`): ele cria só `pg_fluxo_1` e `pg_fluxo_2` e acrescenta ao `pages.json`, sem tocar nas páginas existentes nem no `report.json`.
3. Conferir no Desktop (aplicar, atualizar, páginas claras, filtros, "Ajustar à página") e comparar com a cópia de teste.
4. O William copia a cópia validada para o `GMS_Painel.Report` (ou aprova que eu grave) e publica o relatório.
5. Plano de volta: diff do `pages.json`; remover as 2 pastas de página restaura o estado anterior.

## Riscos
- Colisão de nomes de medida ou de tabelas auxiliares com o modelo real.
- Tema: o piloto não usa tema do relatório, então não afeta as outras páginas.
- Conferência numérica muda um pouco (data de referência 05:20 contra data civil da Visão Geral).
- Dados: os números de pessoas de dez/2025 a mai/2026 ainda têm códigos de operador sem nome (Cobertura e Mandril); estimativa, não escala oficial.
- Depende de `Mês/Ano` e das funções estarem no modelo antes de abrir as páginas novas, senão os visuais quebram.

## Quem faz o quê
- Eu (Sonnet) conduzo e confiro; `executor` (Opus alto) aplica TMDL e gera páginas; `revisor` (Opus) revisa; **William decide as pendências, aprova cada fase e publica**.
- Nada vai ao serviço sem o "sim" explícito. Sem commit de dados de produção.

## Estimativa
Fase 1: 1 a 2 horas (maior parte é conferir colisão e rodar a atualização). Fase 2: 30 a 60 minutos. Decisões do William podem rodar em paralelo.
