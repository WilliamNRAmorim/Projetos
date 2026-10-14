# Relatório de divergência: Packing List passa a vir do GMS (plano, nada aplicado)

Contexto: a conferência diária (MEL-196, fluxo `GMS_Conferencia_Diaria` + scripts `GMS_LerPacking` e `GMS_ConferenciaDiaria`) compara GMS × SAP (MB51) × Packing List. Hoje o Packing List é o `BD Packing List.xlsx` (Excel da cabine). Com o packlist saindo do GMS, a fonte e algumas regras mudam.

## O que muda na fonte
| Hoje | Depois |
|---|---|
| Office Script `GMS_LerPacking` lê o `BD Packing List.xlsx` (aba Data Base: ID, PN, Slice, Qtd, Timestamp, cancelado) | Conector SharePoint lê `Packing_Pallets` (Title = OP, FichaID, Pallet, **LanceIDs**, QtdLances, TotalM, Turno, DataHoraImp, LinkPDF) e `Packing_Manual` (OP digitada, Lances, TotalM, Status Pendente/Regularizado) |
| Histórico até 01/10 (BD, último romaneio 1496) | Continua valendo como base histórica (somente leitura); vale para datas ≤ 01/10 |

## O que muda nas regras (e fica mais simples)
1. **Casamento exato por lance.** O romaneio do Excel não tinha OP, então o motor casava por PN + metragem + horário (94% exato, o resto ±1 m). `Packing_Pallets.LanceIDs` guarda os IDs de `RegistrosInspeção`: um lance está "no packing" se o ID aparece em algum `LanceIDs`. Fim do casamento aproximado.
2. **Categorias do BD que somem:** "ID de romaneio repetido" e "romaneio repete outro" (o Packing não travava) deixam de existir: o pallet é único por ficha.
3. **Categorias novas:**
   - lance aprovado em dois pallets (duplicado);
   - `LanceIDs` com lance que não existe ou foi apagado;
   - `TotalM` do pallet diferente da soma dos lances;
   - OP finalizada sem nenhum pallet;
   - Packing manual ainda Pendente com OP que já existe no sistema (regularizar).
4. **Data do packing** = `DataHoraImp` do pallet. A regra do mesmo dia (3º turno pode virar o dia, sábado cobrado na segunda) continua igual.
5. **Refugo × Packing:** continua não indo para o Packing (só GMS × SAP).

## Pré-requisitos (sem isso a conferência acusaria tudo)
- O app precisa **gravar em `Packing_Pallets` a cada impressão** (fase 2 do pallet dividido: lista criada em 08/10; fonte ainda não adicionada no Studio e telas ainda não coladas).
- **Não carregar em `Packing_Pallets` os packlists reconstruídos** (grupos 3 e 4 do lote oficial): eles são reconstrução pelos lances, não packing físico, e esconderiam divergência real (lance "com packing" sem ter saído da cabine). Só impressão real entra na lista.
- Período de transição: antes da lista existir, a conferência de dias novos lê só o que o app gravou; para datas ≤ 01/10 mantém o BD.

## Mudanças técnicas
1. Fluxo: trocar a ação `Ler_Packing` (Executar script no BD) por duas ações "Obter itens" (`Packing_Pallets` filtrado pelos últimos 30 dias por `DataHoraImp`, `Packing_Manual` Pendente). Usar nomes **internos** das colunas (lição MEL-240).
2. Script `GMS_ConferenciaDiaria.ts`: o parâmetro de packing muda de "slices do BD" para "pallets com LanceIDs"; o casamento passa a ser por ID de lance. Manter o caminho do BD para datas ≤ 01/10.
3. Lista `Conferencia_SAP`: coluna `Packing_m` passa a somar `QtdLances/TotalM` do pallet; adicionar categoria nas opções do relatório.
4. E-mail HTML: textos das categorias novas e remoção das do BD.
5. Teste: rodar o fluxo na mão sobre 6 e 7/10 e comparar com o resultado atual (BD) antes de desligar o caminho antigo.

## Decisões pendentes (William)
- Ligar a gravação em `Packing_Pallets` no app (colar `scr_Finalização_1`/`TelaImpressao`, publicar).
- Aprovar a reescrita do fluxo e do script (só depois do app gravando).
