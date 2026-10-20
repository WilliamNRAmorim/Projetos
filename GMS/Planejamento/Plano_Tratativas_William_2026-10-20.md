# Plano de execução · tratativas do William (Acompanhamento_Validacao_OEE_v2) · 20/10/2026

Fonte: aba Registro Diário da planilha + conferência (somente leitura) na lista Hora-Hora e na ficha_producao.
Nada foi gravado no SharePoint nesta rodada.

| Linha | Tratativa | Situação real | Próximo passo | Prazo |
|---|---|---|---|---|
| 13 | Dividir por 2 os metros da TH01 (duas passagens) | Feito no app: `fx_DuasPassagens` v3.0.11 + `scr_HoraHora_Trancagem_2` v0.6.5 (Real e Meta ÷ 2 em TH01/TO04). Falta publicar | William cola `fx_DuasPassagens` v3.0.11 no App.Formulas, cola a tela v0.6.5 e publica; depois marca **Concluído** na planilha | hoje 20/10 |
| 11 | Apagar duplicados de setembro (TO04) e ver as outras máquinas | 01/09-15/10 já limpo em 19/10 (MEL-243). **Sobra setembro anterior ao ID 26000**: 143 grupos duplicados. TO04: 03/09 1º turno (IDs 24478-24486, rascunho zerado criado em 02/09 duplicando o turno real, ID 24672-24680) | Aprovar a lixeira de 143 grupos: 126 AUTO (idênticos ou o outro registro é zero) e 17 REVISAR (Real diferente, ver abaixo). Mesma regra de 19/10: fica o Finalizado, depois o maior Real, depois o último Modified | hoje 20/10 |
| 10 | Levantar máquinas sem dados em setembro e regularizar | 01-12/09: todas as 10 máquinas têm dado nos dias úteis. 13/09 (domingo) só Spiral. Lacunas depois: TH02 16/09-01/10, TM04 21-30/09, TH05 18/09 e 21/09, TH05 05-15/10, TH03 16/09. A ficha mostra TH02 e TM04 sem OP nesses dias (parada provável); **TH05 tem OP na ficha em 22-29/09 e 02/10 e 05/10**, então 18/09, 21/09 e 05-15/10 são lacunas reais a confirmar | Conferir ao vivo a ficha_producao de TH05 (OP em processo 18/09, 21/09 e 05-15/10) e perguntar ao operador/líder; as que rodaram sem registro entram como `Motivo Não Declarado` ou ficam como lacuna justificada | sem prazo: sugiro 23/10 |
| 12 | Regra de apontamento na troca de turno | Origem do problema: o turno some em dois registros (rascunho pré-criado + gravação do dia seguinte). Ver proposta abaixo | Decisão do William e depois patch no app (MEL a abrir; ID real só com `gms.py --novo`) | hoje 20/10 (decisão); patch depois |
| 16 | (ação em branco) | Linha sem ação corretiva | William descreve a ação; preencher na planilha | hoje 20/10 |

## 17 grupos REVISAR (não entram sem decisão)
- 03/09 TM04 05:20, TH02 05:20, TH03 05:20: Real diferente entre os dois registros.
- 03/09 TH01 06:00 (R60 com mangueira EC115-06L vs R100 sem mangueira).
- 03/09 TH06 2º turno (7 janelas com 3 a 5 cópias cada) e 04/09 TH06 1º turno (2 janelas): quadruplicado/quintuplicado com Real e mangueira (inclusive null e EC115-12LRL) diferentes.
- 12/09 TH06 2º turno 13:47, 15:00 e 18:00 (mangueira 2556-12, null, GH781-8 misturadas).
- Regra proposta: fica o Finalizado; se há mais de um, o maior Real; empate, o último Modified. Qualquer janela em que a regra descartaria um Real maior do que o mantido sai da lista e vem a você.

## Linha 12 · proposta de regra de troca de turno
1. A abertura do turno seguinte só cria as 9 linhas se não existir Data + Turno + Célula (checagem antes do Patch).
2. Ao fechar o turno, o que está em Rascunho sem Real e sem motivo vira `Motivo Não Declarado` (já existe na v0.6.2/0.6.3).
3. Registro atrasado (apontar depois de o turno encerrar): permitido por X horas pelo líder, com carimbo de "apontamento tardio" e sem criar nova linha.
4. Corrigir `Title` e `Célula` no gravador (causa dos 27 Title≠Célula).
Preciso do seu aceite nos itens 1 e 3 (X horas) antes de patchear o app.

## Ordem de execução
1. Hoje: publicar a TH01 (linha 13), aprovar a lixeira do setembro antigo (linha 11), decidir a regra da linha 12, preencher a 16.
2. Depois do "sim": aplico a lixeira em lotes pelo navegador (restaurável), recalculo acumulados e confiro 0 duplicados, como em 19/10.
3. Levantamento da TH05 (linha 10) e MEL novo para a regra de troca de turno.
4. Registro no GMS_Diario.md (ABERTO/FEITO) ao final.
