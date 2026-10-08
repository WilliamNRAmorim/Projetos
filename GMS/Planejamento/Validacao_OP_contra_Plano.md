# Validar OP contra o Plano da Trançadeira (08/10/2026)

Objetivo: o operador só abre ficha com OP que existe no plano do mês. OP inventada (12345678, 11111111) não passa.

## O que há no Excel do plano (15 arquivos em `Plano_Trancadeira_2026/`, cópia local do SharePoint)
- `PL_<MES>_Trançadeira.xlsx`, um por mês (JAN a OUT + `Padrão`). Abas por trançadora: `TE.01 TH.01..TH.07 TM.01 TM.04 TO.04`.
  Cabeçalho na linha 4, dados da linha 5: B Mês, C Trançadeira, **D Ordem (OP, 8 dígitos)**, **E Mangueira (PN)**, F Plano-Quant (m), G Dt Conclusão, H Status impressão, I Resultado cabine, J Prod. tubo, K Comentários, L Data lib. OP, M Data término, N OTC.
- Aba `Plano` (B2:Y99): resumo por PN × trançadora (A planejar, GAP). Aba `COOIS`: ordens do SAP (A Material, **B Order**, C Qtd, ..., N System Status) = lista de OPs válidas do SAP.
- Abas `MANDRIL`, `Extrusora de Mandril`, `KANBAN MANDRIL` e os arquivos `OT´S Mandril_*.xlsx` (OPs de mandril, outra estrutura).
- Contagem de OPs por mês (sheets de trançadora / COOIS): ABR 357/0, MAI 368/431, JUN 365/379, JUL 80/117, AGO 371/407, SET 335/416, OUT 161/192.

## Teste feito hoje: fichas de 01/09 a 08/10 (431) contra OUT+SET (plano + COOIS)
- 7 OPs fora do plano e 8 fichas sem OP.
- **Claramente inventadas:** 45693212 (ficha 3571, 08/09), 45698721 (3714, 21/09), 75632568 (3845, 30/09), 10010000 (3861, 01/10). Todas com Mangueira 0 ou 1.
- **Provável digitação errada:** 30337761 (3841, 30/09, GH781-8; parece 30347761, que está no plano), 30307302 (3754, 23/09) e 30406478 (3890, 03/10); conferir se estão em outro mês/arquivo.
- 8 fichas sem OP (3839, 3840, 3850, 3892, 3925 etc., etapa M ou T).
Ou seja: a regra pegaria os 4 casos óbvios sem barrar produção real (424 de 431 passam).

## Proposta
1. **Lista SharePoint `Plano_OPs`** (OP texto único, PN, Trancadeira, Mes, QtdPlanejada m, Origem = Plano|COOIS, Atualizado). Fonte única de verdade para o app. Excel continua do planejamento; o app nunca escreve nele.
2. **Carga**: Office Script (padrão do GMS_ConferenciaDiaria) + fluxo agendado lê `PL_<mês atual>` e o próximo (abas das trançadoras + COOIS) e faz upsert na lista. Roda de hora em hora (o plano muda no mês).
3. **App** (`scr_mandril_1:2735`, `scr_tubo_1:2729`, onde nasce a ficha): antes do `Patch(Defaults(ficha_producao))`, exigir `^\d{8}$` e `LookUp(Plano_OPs, OP = ...)`. Se não achar: bloqueia e mostra "OP não está no plano do mês. Chame o PCP/supervisor". Se o PN digitado difere do plano: aviso forte. Exceção (OP urgente fora do plano) só com PIN do supervisor e motivo gravado na ficha, para rastrear.
4. **Conferência diária**: nova categoria "OP fora do plano" para o que passar pela exceção ou entrar sem validação.
5. **Limpeza**: marcar as 4 fichas inventadas para a supervisão corrigir (não apago nada sem aprovação).

Decisões para o William antes de implementar: (a) COOIS vale como plano ou só as abas das trançadoras? (b) quem aprova exceção e como (PIN, lista de supervisores?) (c) OP de mandril entra na mesma lista? (d) o app deve funcionar offline sem consultar a lista (cache local `colPlanoOPs` no OnStart)?

## Decisões do William (08/10/2026)
- COOIS (export do SAP com as ordens de produção, status REL/TECO): entra como fonte, marcada `Origem=COOIS`. Serve para OP real que ainda não foi alocada a uma trançadora.
- Exceção (OP fora do plano): aprovam william.amorim@danfoss.com ou carlos.brizon@danfoss.com.
- OP de mandril entra na mesma lista só vindo da aba `Extrusora de Mandril` (col. D Ordem, C mandril FMxxxxx, E bitola); a solda de mandril NÃO usa a lista.
- App só funciona com rede: consulta a lista ao vivo, sem cópia offline.
- Carga automática: Power Automate + Office Script lendo o Excel do mês e gravando em `Plano_OPs`.

## Feito (08/10/2026)
- Lista SharePoint `Plano_OPs` criada (Title = OP, PN, Trancadeira, Mes, QtdPlanejada, Origem, Atualizado).
- Carga inicial de OUTUBRO: 194 OPs (161 Plano, 1 PlanoMandril, 32 COOIS); `seed_outubro.json` guarda os dados.
## Falta
1. Office Script `GMS_PlanoOPs` (lê `PL_<MES>_Trançadeira.xlsx`: abas T*.xx, Extrusora de Mandril, COOIS) + fluxo `GMS_PlanoOPs_Sync` (upsert por OP; mês atual e anterior).
2. Lista `Excecoes_OP` (OP, motivo, quem aprovou, data) e regra no app (scr_mandril_1/scr_tubo_1).
3. Categoria "OP fora do plano" na conferência diária.
