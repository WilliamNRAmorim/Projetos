# Hora-Hora do Mandril e do Tubo no padrão da Trançagem (MEL-224)

Telas: `Telas/scr_HoraHora_Mandril_2.txt` e `Telas/scr_HoraHora_Tubo_2.txt` (antes moldes em `Telas/Moldes`). Mesmo contrato da `scr_HoraHora_Trancagem_2` (cabeçalho, grade por hora, replicar, pendências, fechar turno, falhas sem duplicar), gravando na lista `Hora-Hora` com Célula = "Mandril" ou "Tubo".
**Status: passam na bateria `gms_qa_yaml.py`, mas NÃO foram abertas no Studio.**

## As 4 definições que estavam pendentes
| # | Pergunta | Como ficou |
|---|---|---|
| 1 | Fonte da velocidade por hora | **Tubo**: `DM_TUBE_EXTRUSION.SPEEDY_mpm` (m/min, preenchido nas 89 linhas), ×60 pela `fx_VelCobHora`, igual à Cobertura. **Mandril**: o `DM_MANDREL` ainda não tem a velocidade da linha de solda preenchida, então a **meta fica em branco** para o operador digitar |
| 2 | Lista de máquinas | Uma célula só por etapa ("Mandril", "Tubo"), como o molde. Dividir por solda A/B ou por extrusora exige coluna nova na lista `Hora-Hora` |
| 3 | Motivos de parada | `fx_MotivosParada` (a mesma da Trançagem) |
| 4 | Destino dos dados | Lista `Hora-Hora`. O `GMS_Mestre_BI` só cita `Hora-Hora` (hora-hora das linhas); as listas antigas `Hora_Hora_Mandril` e `Hora_Hora_Tubo` não aparecem no modelo do BI |

## O que mudou nas telas existentes
- `scr_tubo_1` v0.5.4: o botão Hora a Hora abre `scr_HoraHora_Tubo_2`.
- `scr_mandril_1` v0.5.7: o botão Hora a Hora abre `scr_HoraHora_Mandril_2`.
- Os spinners das duas telas novas já saíram em `Spinner@1.4.6`.

## Ordem de colagem
1. Colar `scr_HoraHora_Tubo_2` e `scr_HoraHora_Mandril_2` (elas voltam para `scr_tubo_1` e `scr_mandril_1`, que já existem).
2. Colar as versões novas de `scr_tubo_1` e `scr_mandril_1` (o botão passa a apontar para as telas novas).
3. Testar um apontamento em cada e conferir que a linha entra em `Hora-Hora` com Célula = Tubo / Mandril.
4. Só depois excluir no Studio `scrHoraHora_Mandril` e `scrHoraHora_Tubo`, as fontes `Hora_Hora_Mandril` e `Hora_Hora_Tubo`, e apagar `Telas/scrHoraHora_Mandril.txt` e `Telas/scrHoraHora_Tubo.txt`. Os dados antigos continuam nas listas; migrar histórico é decisão à parte.

## Pendências do William
- Quando a Engenharia preencher a velocidade da solda no `DM_MANDREL`, trocar `MFG: 0` na `scr_HoraHora_Mandril_2` (o comentário no código mostra onde).
- Confirmar se o BI deve passar a contar "Mandril" e "Tubo" como células do Hora-Hora (a dimensão de células do BI hoje lista as linhas de trançagem e cobertura).
