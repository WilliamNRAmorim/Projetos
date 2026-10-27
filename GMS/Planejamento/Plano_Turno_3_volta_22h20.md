# Plano: 3º turno volta para 22:20 (reverte MEL-198 / v3.0.5)

Pedido: William, 27/10/2026 (feedback do chão na TH02: a última janela do 2º turno mostra "22:00 - 22:41"; o horário real é até 22:20).
Decisão a registrar: DECISÃO + NORMA novas (MEL-250) que revogam a NORMA de 05/10 (MEL-198).

## Régua alvo (igual à anterior à v3.0.5, commit 8102c59^)
T1 05:20 (320) → 836 · T2 13:57 (837) → 1339 · T3 22:20 (1340) → 319.
Janelas: T1 517 min · T2 503 min (última "22:00 - 22:20", 20 min) · T3 420 min.

## Mudanças em Telas/Formulas.txt (versão nova v3.0.15)
1. `fx_Turno`: `minutosDoDia < 1361` → `< 1340`.
2. `fx_InicioTurnoMin`: 3 → 1340.
3. `fx_GradeHoraHora`, 2º turno Ord 9: `Rotulo "22:00 - 22:20"`, `Minutos 20`, `Fim 503`.
4. `fx_GradeHoraHora`, 3º turno: Ord 1 `Rotulo "22:20 - 23:00"`, `Minutos 40`, `Fim 40`; Fim das demais 100/160/220/280/340/400; Ord 8 (05:00-05:20) Fim 420. Chaves `Hora` NÃO mudam.
5. Comentários §4, §11 e o do cabeçalho (v3.0.5/22:41, "524/399", linha ~1759 `1361 + 399`) atualizados para 1340/503/420; adicionar nota da reversão.

## Telas (só texto/rótulo; lógica já lê a grade)
- `scr_HistoricoTurno_Tubo.txt:205` e `scr_HistoricoTurno_Mandril.txt:218`: "13:57 às 22:41" → "13:57 às 22:20"; "22:41 às 05:20" → "22:20 às 05:20". Conferir se o filtro delas usa fx_Turno/grade ou literal.
- `scr_PainelCelula_1.txt` (comentários linhas ~341 e ~598) e patches `_patch_PainelCelula_*`: só comentário; a janela atual vem da grade, então o bug A1 (22:20–22:40 sem janela atual) deixa de existir sem mudar código.
- Nenhuma outra tela tem 1361/1340 literal (grep feito).

## BI e documentos (precisam do "sim" do William por serem norma)
- `GMS_Mestre_BI.md` (linhas 232, 286, 412) e `PowerBI/modelo/fHoraHora_dia_produtivo.tmdl.md` (linha 54): dTurno hoje 22:41/1361 → 22:20/1340. `GMS/CLAUDE.md` já diz 22:20.
- `GMS_Mestre.md` (exemplo linha 501, B §3.2): emenda via linha NORMA no Diário; não editar o Mestre sem pedido explícito.
- O .pbix é do William: entregar o trecho DAX/M da dTurno pronto para colar.

## Diário
Linhas: DECISÃO (William, 27/10, 22:20), NORMA (T3 22:20/1340; grade 517/503/420; revoga MEL-198), ENTREGUE (Formulas, telas), PENDÊNCIA (publicar no Studio; BI).

## Riscos e pendências
- Dados já gravados desde 05/10: registros feitos entre 22:20 e 22:40 ficaram com Turno=2 (e janela "22:00 - 22:20"); com a nova régua deveriam ser Turno=3. Não regravar nada sem pedido; avaliar com consulta e decidir.
- Metas de Hora-Hora gravadas já calculadas com 41/19 min não mudam retroativamente.
- Hora extra do 2º turno (CLAUDE.md fala em até 23:20; BI trata "22:20 - 23:20" como hora extra) NÃO é tratada aqui: janela de hora extra continua fora desta mudança.
- Ordem para publicar: colar Formulas inteiro no Studio PRIMEIRO, depois as telas; BI no mesmo dia, senão app e BI divergem entre 22:20 e 22:40.
- Casos de teste de fronteira: 22:19→T2, 22:20→T3, 22:21→T3, 13:56→T1, 13:57→T2, 05:19→T3, 05:20→T1; janelas somam 1440.

## Verificação
`python gms_qa_yaml.py` nas telas tocadas; `python gms.py --check`; conferir soma das janelas = 1440 e fx_Turno x fx_InicioTurnoMin x grade coerentes.
