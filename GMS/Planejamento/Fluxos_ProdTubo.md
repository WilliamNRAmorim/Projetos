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

## Pendências de 15/10/2026: passo a passo (nada disto foi feito no Power Automate/SharePoint)

Ordem sugerida: 1, 2, 3, 4, 5. Os itens 1, 2, 3 e 5 mexem em recurso compartilhado: só com o "sim" do William a cada alteração.

### 1. Provar o GMS_MarcaProdTubo
- Pegar uma OP que ainda NÃO tem OK na J e mandar da fila do Tubo para a trançagem (vira `field_10 = Trançadeira`, `field_11 = Aguardando`).
- Em Power Automate > GMS_MarcaProdTubo > Histórico de execuções: abrir a execução, ver a saída do `Run script` (`marcado=true`, aba, linha) e conferir a J da OP em `PL_<MÊS>_Trançadeira.xlsx`.
- Se a J já estava OK por digitação, o retorno vem `marcado=false` (motivo "J ja preenchida"): isso NÃO prova nada. Escolher OP com J vazia.

### 2. GMS_LimpaProdTubo (script + fluxo)
- Script pronto: `GMS_LimpaProdTubo.ts`. Gravar no OneDrive pela pasta sincronizada `Documents\Office Scripts` (a REST dá 403) como `GMS_LimpaProdTubo_v100`. Limpa a J só se vale "OK".
- Para saber se o OK foi do fluxo (e não digitado): criar coluna `OKPeloGMS` (Sim/Não, padrão Não) em `Plano_OPs`. No GMS_MarcaProdTubo, depois do `Run script`, se `marcado = true`: atualizar `Plano_OPs.OKPeloGMS = Sim` da OP (junto do `ProdTuboOK = Sim`).
- Fluxo novo `GMS_LimpaProdTubo`: gatilho SharePoint, item modificado em `ficha_producao`; condição `status_processo = Cancelado` e `OP` com 8 dígitos. Buscar a OP em `Plano_OPs`; só seguir se `OKPeloGMS = Sim`. `Run script` GMS_LimpaProdTubo_v100 no `PL_<MÊS>_Trançadeira.xlsx` (mesmo caminho por mês do MarcaProdTubo). Se `limpo = true`: `Plano_OPs.ProdTuboOK = Não` e `OKPeloGMS = Não`.
- Cancelamento de OP digitada à mão (OKPeloGMS = Não): J fica como está, de propósito.

### 3. Excecoes_OP: Alertar-me
- Lista `Excecoes_OP` > ... > Alertar-me: "Novos itens são adicionados", e-mail imediato, para william.amorim@danfoss.com e carlos.brizon@danfoss.com. Aprovação segue manual na visão Pendentes (Status Pendente → Aprovada).
- Teste ponta a ponta (linha de teste) só com sim do William.

### 4. Colar os botões de cancelar
- `Telas/_colar_cancelar_Tubo.yaml` em `scr_tubo_1` e `Telas/_colar_cancelar_Trancagem.yaml` em `scr_Trancagem_3` (os .txt das telas já estão atualizados no repo). Publicar e testar com 1 OP: ficha vira Cancelado, carretel liberado, OP volta ao dropdown.
- Lembrar: o filtro de Cancelado é local (`Filter(Filter(fonte, ...), Coalesce(status_processo, "") <> "Cancelado")`), não direto no SharePoint.

### 5. Aviso de falha do GMS_PlanoOPs_Sync
- No fluxo, ramo paralelo "configurar execução após" (has failed / has timed out) ligado ao último passo do escopo: ação "Enviar e-mail (V2)" para william.amorim@danfoss.com com assunto "GMS_PlanoOPs_Sync falhou" e o link da execução (`workflow()?['run']?['name']`). Padrão igual ao Avisar_Falha da Conferência Diária.
- Anotar: concorrência 1 do fluxo gerou aviso de throttling em 08/10; observar se o aviso se repete.
