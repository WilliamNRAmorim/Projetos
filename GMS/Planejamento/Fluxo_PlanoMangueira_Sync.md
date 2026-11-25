# GMS_PlanoMangueira_Sync (proposto em 25/11/2026, MEL-275) — NÃO CRIADO, aguarda o sim do William

Mantém a lista `GMS_PlanoMangueira` igual à aba "Plano" do `PL_<MES>_Trançadeira.xlsx`. Script: `GMS_LerPlanoMangueira.ts` v1.0.0.

1. **Gatilho:** SharePoint, "When a file is created or modified (properties only)", biblioteca Documents, pasta `Manufatura operação/1 - Mangueira/3_Controle de Ot´s mangueira/Plano Trançadeira` (a de cima, com subpastas: não para na virada do ano). Concorrência 1. Condição: nome começa com `PL_`, termina com `.xlsx` e não contém `Padr`.
2. **Espera** 30 s (como o GMS_PlanoOPs_Sync).
3. **Get items** `GMS_PlanoMangueira` (Top 5000, colunas ID, Title, Mes, CStandard, Tipo, Arame, Volume).
4. **Run script** `GMS_LerPlanoMangueira_v100`: nome do arquivo, pasta, `string(body/value)`, `formatDateTime(convertFromUtc(utcNow(),'E. South America Standard Time'),'yyyy-MM')`. returnSchema objeto `{result:string}` (lição de 08/10).
5. **Se `ok` = false:** e-mail só para o William com o `erro`; nada é gravado.
6. **Se `ok`:** Apply to each em `linhas` (sequencial): `id` 0 = POST; senão MERGE com IF-MATCH `*`. Nunca DELETE.
7. **Falha em qualquer passo** (failed, timed out, skipped): e-mail só para o William.

O BI mostra no refresh seguinte do modelo. Testes (25/11): 16 mutações ok; 12 planos de 2026 (barrou PL_ABRIL, PL_Padrão, JAN e JUL da cópia); PL_NOV vivo x lista = 0 mudanças; PL_NOV x lista antiga = as mesmas 10 mudanças gravadas com o sim.
