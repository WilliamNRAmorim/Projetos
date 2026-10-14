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

## Estado em 14/10/2026
- `GMS_PlanoOPs_Sync` salvo com `GMS_LerPlanoOPs_v120` (v1.2.1: lê `ID` maiúsculo; antes o MERGE falhava com `items()`) e `ProdTuboOK` no corpo. Última execução: Succeeded; lista com 165 OPs `ProdTuboOK` e 127 encerradas de 229.
- `GMS_MarcaProdTubo` (id f0bbddd4-5904-411a-92d8-5e329e5f8e51) salvo e ligado. Gatilho: item criado ou modificado em `ficha_producao` (o app ATUALIZA a ficha ao mandar para a trançagem, não cria). Condição: `field_10 = Trançadeira` e `field_11 = Aguardando`. Run script `GMS_MarcaProdTubo_v100` em `PL_<MES>_Trançadeira.xlsx` (caminho montado por mês), `op = string(OP)`.
- Ainda sem teste real do GMS_MarcaProdTubo: validar com a próxima OP que entrar na trançagem.
