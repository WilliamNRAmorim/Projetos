# Saldo da ProdHose (PROD-GR-HOSE) em 18/11/2026: 8.579 m

Fontes: saldo colado pelo William (prodhose_2026-11-18.csv), MB51 de 18/11 (101/102, GRT4, M), Packing_Pallets e RegistrosInspeção ao vivo.
Desde 15/10, para quase todo material, SAP bom = metro do GMS em pallet. O saldo não vem de lance sem packlist recente.

| Grupo | m | O que é | Ação |
|---|---|---|---|
| A. Em fluxo | 2.580 | Pallets impressos em 16-18/11 ainda não transferidos (GH493-8 1.113 = pallets de hoje; GH781-4 595,5 = pallets desde 17/11 23:31; GH493-12, GH781-12, EC118-04L, FC735-10, EC118-08L, GH681-4...) | Nenhuma, sai sozinho |
| A'. Lances corrigidos | 641 | GH493-16 (30750671), FC735-12, EC415-16, FC839B-06, GH781-8: lances do lote 3 e da 30750671 sem pallet | Imprimir packlist (fichas 4059, 4137, 4232, 4264, 4265, 4355, 4459, 4487, reimprimir 4267) |
| B. Parado há semanas, material em produção | 2.333 | EC215-06L 698,8 (último pallet 22/10), GH781-6 735,2 (04/11), EC215-10L 232,6 (20/10), FC839B-04 212,4 (14/11), GH681-6 186,9 (07/11), HC139-7_S-GX 169,7 (05/11), 2556-12, HC101-6, GH681-12 16,9, EC215-16L, GH681-8, FC839B-08 3,0 | Conferir fisicamente: pallet impresso e não transferido no EWM, ou refugo que entrou e não saiu |
| C. Antigo (antes do packlist do GMS ou sem produção recente) | 3.025 | EC215-08LRL 1.024,6 (último SAP 03/08), EC215-08L 907,6 (09/10; 563,8 m de lances de 06-14/10 sem pallet), FC735-08 412,3 (05/10), HC101-8 198 (05/10), 2556-8 147,4 (31/08), EC118-10L 98,8 (= 1 doc da OP 29878655, 26/08), 12055040 60,6, EC115-10L 50,7 (06/2026), GH493-10 34,5 (= 1 doc da OP 30446700, 09/10), 12078544 23,9 (= 1 doc da OP 26992559, 12/2025) e restos < 30 m; FC350-20, EC600-12 e FC254-08 sem 101 no MB51 desde 11/2024 | Inventário: existe na prateleira? Se não, baixar no EWM |

## Refugo preso na ProdHose
O refugo também entra por 101 no GRT4 (usuário U452021). Em alguns materiais o saldo é exatamente refugo que nunca saiu:
- GH781-10 182,18 m = os 32 últimos refugos (15/09 a 17/11)
- GH681-12 16,9 m = os 4 últimos refugos (29-30/10)
- FC839B-08 3,0 m = refugo de 09/11 (OP 30721705)
- 2556-12 40,7 m = refugo de 09/11 (OP 30766829)
Nos outros materiais o refugo sai. Falta saber quem baixa o refugo da ProdHose e por que nesses não baixou.

Limite: sem os movimentos do EWM não dá para ligar cada metro a um pallet; o grupo de cada material é pela data do último pallet e do último SAP.
