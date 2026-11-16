# Validação da página Produção x meta (SAP) contra a planilha Máscara de produção (16/11/2026, MEL-273)

Objetivo: a planilha vai ser descontinuada e a página do GMS_Painel tem de dar a resposta certa em qualquer mês do filtro.

## Fontes comparadas
- BI: modelo (GMS), refresh de 16/11 10:29, mb51.xlsx e coois.xlsx de 16/11 08:31; consultas DAX simulando o filtro de cada mês.
- Planilha no SharePoint (versão 201, 16/11 09:23), lida por Excel REST: aba Resumo e tabela dinâmica.
- Cópia local da planilha de 13/11 (tabela mb51_coois, 115 mil linhas), recalculada em Python (`valida.py`) com a mesma regra.

## 1. Mês atual (novembro): CERTO
- Dia a dia de 03 a 13/11 igual nos 3 produtos (ex.: 13/11 Mangueira 7.915,86 m, Montagem 2.220, Fittings 265).
- Diferença só no sábado 14/11: a MB51 dentro da planilha estava com o dia pela metade (Mangueira 1.556,8 m × 7.962,8 no BI; Montagem sem o dia).
- Meta: a planilha passou a Mangueira para 7.000; lista atualizada; carinhas iguais (Mangueira ☹ −3.732 m, Montagem ☹ −2.147, Fittings 😊 +1.651).
- Linhas sem MRP em novembro (43.360 pç) são só entrada de compra sem OP (cápsulas CleanSeal/CapSeal, tampões): ficam fora, certo.

## 2. Meses anteriores no filtro: ERRADO (a menor), e piora com o tempo
O produto vem do MRP controller da COOIS, ligado pela OP. A COOIS exportada só traz as OPs atuais; quando a OP sai da COOIS, a produção dela perde o produto e some da conta.

| Mês | Produto | BI (COOIS de 16/11) | Planilha local (COOIS de 13/11) | Sem MRP com OP (planilha) |
|---|---|---|---|---|
| out | Mangueira | 103.631,5 m | 136.036,1 m | +34.024,9 m |
| out | Montagem | 49.242 | 49.242 | — |
| out | Fittings | 11.618 | 11.618 | — |
| set | Mangueira | 1.018,4 m | 1.500,0 m | +157.778 m |
| set | Montagem | 28.353 | 43.388 | +12.830 (GRT4) +11.387/−11.000 (KAN) |
| set | Fittings | 14.204 | 20.827 | — |

Consequência: o mês atual também vai encolher depois que as OPs dele forem encerradas e saírem da COOIS. A planilha tinha o mesmo defeito, mas só olhava o mês corrente.

## 3. Como classificar sem depender da COOIS (testado na MB51 com MRP conhecido)
- Depósito GRT4 + metro + OP → sempre AIH (Mangueira): 3.722 de 3.722 linhas com MRP.
- Depósito KAN + peça + OP → AWE (Montagem): 159 de 160.
- Depósito GRT4 + peça + OP → mistura Montagem (Z35/AWE) e Fittings (AO0); a descrição separa: HOSE ASSY, BUNDLE, CUTED HOSE/NYLON, SLEEVE, MANG MONT, CAPA = Montagem; HOSE FTG, CON PRENS, FTNG, HOSE NIPPLE, NIPLE, TUBO MONTADO, CON MONT, CON ESPECIAL = Fittings.
- Material → MRP (aprendido das OPs que estão na COOIS): cobre 1.005 dos 2.659 materiais que hoje ficam sem MRP; 1 material com 2 MRPs (AXE17138-BRA).
- Fonte definitiva: o MRP controller é dado do cadastro do material no SAP (MARC). Um export material × MRP controller resolveria sem regra de descrição.

## 4. O que mais existe na planilha e não está no BI
- Aba "Power Automate": produção de ontem por HOS/HAS/FIT (em 16/11 mostrava 15/11 = 0); algum fluxo lê essa tabela.
- Aba "Cálculo de horas (HOSE)": tabela dinâmica de horas por construção e por dia (metros convertidos em horas).
- Aba "ANALISE MEDIA": hoje mostra #SPILL! (quebrada).
- Abas de apoio: Plano (oculta), Conferencia (oculta), Cadastro Mangueiras, Detalhes1/Detail1 (detalhe de tabela dinâmica), COOIS, MB51, Resumo BI.
