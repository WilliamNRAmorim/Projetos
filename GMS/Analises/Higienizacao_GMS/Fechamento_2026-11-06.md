# Fechamento da higienização da ficha_producao, janeiro a setembro/2026 (04 a 06/11/2026)
Sem nomes e sem metros de produção (estes ficam em `C:\Users\U445131\Downloads\` e na própria lista). Detalhe por rodada: `Auditoria_2026-11-04_*.md`, `Auditoria_2026-11-05_*.md`, `Auditoria_2026-11-06_*.md` e `Metodo_mensal_ficha.md`.

## O que foi feito (tudo com "sim" do William, guarda de releitura, conferência depois e valor antigo guardado)
| Frente | Resultado |
|---|---|
| Máquina (Trançadeira) | padronizada (TE0/TE01 = Spiral); 13 correções; 2 fichas apagadas a pedido; BI (`limpeza_ficha_producao.m.md`) corrigido |
| Bitola e lote do carretel | tabela fechada: 3→800, 4→800, 5→800, 6→680, 7→680, 8→680, 10→460, 12→400, 16→250 |
| Operadores | nomes parciais resolvidos; códigos, zeros e vazios estimados por etapa e turno do horário real do fim (jan a mai); marca e valores originais na observação da trançagem |
| Quantidades | cadeia anterior = seguinte + refugo, tolerância 1,5x o lote; jan a set corrigidos; grupos 1 e 2 de fichas ambíguas resolvidos |
| Datas de fim | regras R1/R2/R3/R4 + R1b/R5 em duas passadas; jan 93,2%, fev 99%, mar a abr 100% em ordem |
| Fichas ausentes | 131 reconstruídas a partir do SAP + ficha modelo (jan 59, fev 15, mar 22, abr 6, mai 29), prefixo `RECONSTRUIDA_SAP` |
| Extração de janeiro | estimada onde faltava; 27 fichas finais a partir da vulcanização (OP lançada no SAP) |
| Conciliação CP x SAP x GMS x BD Packing List | feita de jan a set; fev a abr entre 98% e 112%; julho foi parada de férias coletivas (04 a 26/07) |

## Saúde por mês (fichas originais, depois das correções)
| Mês | Ficha 100% saudável | Operadores estimados |
|---|---|---|
| Janeiro | 92,5% | ~97% |
| Fevereiro | ~97% | ~97% |
| Março | 95,7% | 66% |
| Abril | 98,3% | 62% |
| Maio | 94,5% | 26% |
| Junho | 97,8% | 0% |
| Julho | 100% | 0% |
| Agosto | 98,4% | 0% |
| Setembro | 98,5% | 0% |

## Atenção para o BI (sessão do BI)
- Filtrar `Title` começando em `RECONSTRUIDA_SAP` nas visões de pessoas, refugo e rastreio por OP; o `Created` dessas fichas é novembro, o mês certo vem das datas de fim.
- Operadores estimados: a observação da trançagem começa com "[Operadores estimados ...]" (jan a mai); essas fichas só servem para tendência por turno, não para quem trabalhou na OP.
- Julho: sem produção de 04 a 26/07 (férias coletivas), não é lacuna.

## Pendências que dependem do William
1. Códigos de operador (jan a mai): diretório de funcionários para trocar a estimativa pelo nome real.
2. Fichas 2735 e 4036 (quantidades idênticas em meses diferentes): conferir se uma é cópia.
3. Ficha 1047 de janeiro (OP sem lançamento no SAP) e as 20 fichas de janeiro e 3 de fevereiro sem data de fim em alguma etapa.
4. Outubro e novembro: só a saúde de outubro foi medida (93,6%) e as quantidades corrigidas; novembro tem 19 fichas em andamento.
