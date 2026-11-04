# Método mensal de limpeza da ficha_producao (começou por janeiro/2026, 04/11/2026)

Sem nomes de funcionários e sem dado de produção linha a linha (estes ficam em `C:\Users\U445131\Downloads\`).

## Fonte de verdade por assunto
- **CP_<mês>2026.xlsx (Controle de Produção):** metros por dia, turno e processo (Trançadeiras, Bandagem, Debandagem, Extração). Sem OP. Serve só de **régua de cobertura mensal** da ficha, não corrige ficha a ficha. Abas `01`..`31`; cabeçalho de data traz 2025 por engano; a partir de 12/01 só 2 turnos.
- **Lista viva `ficha_producao`:** leitura pela API REST no navegador nativo (campos: quantidades field_6/14/22/28/33/37/41/46; operadores field_8/18/24/30/34/38/42/47; defeitos field_15/23/29; datas de fim field_9/17/20/26/32/36/40/44; Bitola, Trançadeira e Mangueira têm nome interno próprio). Mês da ficha = `Created`.

## Passos de cada mês
1. Cobertura: soma da ficha por etapa (m) contra o CP do mês.
2. Operadores (8 campos por ficha), por classe: nome completo; vazio; zero (`0`, `000`...); código; dupla (`X/Y`); nome parcial.
   - Nome parcial com **um único** colaborador da lista que contém o token = lote de alta confiança (William confirma o lote).
   - Código, dupla e zero: só com confirmação do William (diretório de funcionários).
3. Máquina: `TE01`/`TE0` = Spiral (não é lixo); variações de hífen/ponto padronizam; `T004` e vazios com evidência.
4. Bitola: o sufixo da mangueira (`HC139-7`, `GH781-12`) indica a bitola. Bitola 7 existe (HC139-7) mas não está na tabela de carretel: William define os metros.
5. Quantidades: regra anterior = seguinte + refugo da seguinte (defeito_tubo/trancagem/cobertura); nunca subtrair refugo do lote nem mexer nos `defeito_*`. **Valores 111, 1111 e 11111 são digitação de preenchimento**: não servem de âncora da cadeia; a cobertura recebe a quantidade da bandagem. Razão acima de 8× entre etapas vai para decisão (provável zero a mais). Ficha com etapa seguinte vazia e ancoragem em etapa posterior conflitante vai para decisão.
6. Gravar só com "sim" do William (uma gravação por aprovação), relendo cada item antes, conferindo depois, guardando valor antigo (CSV em Downloads).

## Janeiro/2026 (292 fichas criadas em jan)
Cobertura contra o CP: trançagem 69%, bandagem 79%, debandagem 70%, extração 36% (só 154 fichas com quantidade_extracao; só 1 ficha com data de fim da debandagem).
