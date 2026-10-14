# Prod. Tubo: o que muda no Power Automate (14/10/2026)

Regra: a OP só some do `cmb_OpTubo_1` quando a coluna J (Prod. Tubo) do `PL_<mês>` está "OK". Impressão (coluna H) não esconde nada. Quando a ficha da trançadeira abre, o fluxo escreve "OK" na J.

## Antes de tudo
Lista `Plano_OPs`: criar coluna `ProdTuboOK` (Sim/Não, padrão Não).

## 1. GMS_PlanoOPs_Sync (existente)
- `GMS_LerPlanoOPs` v1.2.0 no OneDrive (Office Scripts). `Run script` ganha `prodOK` na saída.
- `Get items`: o JSON de existentes passa a incluir `ProdTuboOK`.
- No `Apply to each`, o passo que cria/atualiza item em `Plano_OPs` ganha `ProdTuboOK` = `item()?['prodOK']`.

## 2. GMS_MarcaProdTubo (novo, só liga com "sim" do William)
- Gatilho: SharePoint, quando item é criado em `ficha_producao`; condição `processo = Trançadeira` e `OP` com 8 dígitos.
- `Run script` (Excel Online/Business) em `PL_<MÊS>_Trançadeira.xlsx` com `GMS_MarcaProdTubo` e `op` = OP da ficha. Mês pelo `Created` da ficha.
- Script não sobrescreve J preenchida. Retorno `marcado=false` com motivo: registrar, sem erro.
- Depois do script, atualizar `Plano_OPs.ProdTuboOK = Sim` para a OP (o app reflete sem esperar o Sync).
