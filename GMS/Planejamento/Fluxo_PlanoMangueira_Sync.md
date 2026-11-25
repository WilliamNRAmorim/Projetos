# GMS_PlanoMangueira_Sync (25/11/2026, MEL-275) — CRIADO E LIGADO em 25/11 10:09 (sim do William)

Id 638992a0-4483-4f09-b707-43facf088cd1, cópia do GMS_PlanoOPs_Sync (que não mudou). Desligar: make.powerautomate.com, menu ⋯, Enabled.

Mantém a lista `GMS_PlanoMangueira` igual à aba "Plano" do `PL_<MES>_Trançadeira.xlsx`. Script: `GMS_LerPlanoMangueira.ts` v1.0.0.

1. **Gatilho:** SharePoint, "When a file is created or modified (properties only)", biblioteca Documents, pasta `Manufatura operação/1 - Mangueira/3_Controle de Ot´s mangueira/Plano Trançadeira` (a de cima, com subpastas: não para na virada do ano). Concorrência 1. Condição: nome começa com `PL_`, termina com `.xlsx` e não contém `Padr`.
2. **Espera** (como o GMS_PlanoOPs_Sync): Delay, lê o arquivo de novo e encerra como Cancelled se ele foi salvo depois do gatilho (só a última gravação roda).
3. **Get items** `GMS_PlanoMangueira` (Top 5000, colunas ID, Title, Mes, CStandard, Tipo, Arame, Volume).
4. **Run script** `GMS_LerPlanoMangueira_v100`: nome do arquivo, pasta, `string(body/value)`, `formatDateTime(convertFromUtc(utcNow(),'E. South America Standard Time'),'yyyy-MM')`. returnSchema objeto `{result:string}` (lição de 08/10).
5. **Compose (trava):** `div(1,if(equals(json(body('Run_script')?['result'])?['ok'],true),1,0))`. Com `ok` = false dá erro de propósito, o laço é pulado e nada é gravado.
6. **Apply to each** em `json(body('Run_script')?['result'])?['linhas']` (sequencial), HTTP SharePoint em `lists(guid'34631d40-3ad8-4226-82d6-8d5f8fd1ce0a')/items`: `id` 0 = POST; senão MERGE com IF-MATCH `*`. Nunca DELETE.
7. **E-mail** só para o William (laço failed, timed out ou skipped) com o `erro` da trava e o nome do arquivo.

O BI mostra no refresh seguinte do modelo. Testes (25/11): 16 mutações ok; 12 planos de 2026 (barrou PL_ABRIL, PL_Padrão, JAN e JUL da cópia); PL_NOV vivo x lista = 0 mudanças; PL_NOV x lista antiga = as mesmas 10 mudanças gravadas com o sim.
Teste real (25/11 12:37): salvamento do PL_NOV disparou o fluxo; 1ª execução cancelada pela espera, 2ª com sucesso (ok, 158.966 = 158.966, 0 linhas). Sem teste real: gravação (POST/MERGE) e e-mail de trava.
