# PLANO_OEE2 — Hora-Hora do GMS e BI no padrão OEE2 da Danfoss (MEL-266)

> Plano aprovado pelo William em 09/11/2026 (escopo: só Hora-Hora de mangueira, sem Montagem). Execução fase a fase; nada no app, no SharePoint ou no modelo `(GMS)` muda sem o "libero" dele.

## Atualização de 12/11/2026: o plano depois da hora cheia (MEL-267) e do redesign (MEL-268)

**Documento conferido de novo.** O PDF que o William mandou em 12/11 (`Factbird Governance (1).pdf`) é o mesmo arquivo de `Dados_Brutos/Factbird_Governance_OEE.pdf` (mesmo MD5). As páginas 10, 11 e 12 batem com o resumo abaixo e com as seções A e B:
- OEE2 = valorizado ÷ tempo de produção. O tempo de produção já tira o "sem atividade" e as "atividades não produtivas".
- Troca, setup e limpeza são perda de disponibilidade.
- Quebra, microparada, ociosidade e velocidade são perdas na operação.
- Refugo é perda de qualidade.
- TCU = valorizado ÷ tempo total (24/7).
- A Danfoss chama o OEE2 só de "OEE".

**Estado em 12/11.** Só a fase 0 está feita (este plano). O modelo não tem nenhuma medida OEE2 e o relatório não tem a página. **Hoje o Hora-Hora não calcula OEE2.**

**O que muda nas seções B e D por causa do que entrou em 11/11:**
1. **Grão.** Passa a ser a `fHoraCheia`, não a `fHoraHora`:
   - dia produtivo de 05:00 a 05:00 (`Data BI`);
   - `Turno BI` em 05-14, 14-22 e 22-05;
   - `Min` = minutos da fatia;
   - `P` = `fHoraCheia[Parado]`, que já vem capado na fatia.
   - O achado 4 (linhas com `Minutos` = 0) já está resolvido: a `fHoraCheia` usa a duração do rótulo.
2. **Pausa de 45 min.** Segue a regra da seção B, com o turno de máquina = `Célula × Data BI × Turno BI` e Real > 0.
   - A `fHoraCheia` já coloca os 45 min na janela do Almoço lançado, ou na hora padrão quando o turno não lançou Almoço. Para o OEE2 isso só muda onde a pausa aparece no gráfico por hora; o total por turno é o mesmo.
3. **A meta da `fHoraCheia` já vem sem os 45 min da refeição.**
   - O valorizado oficial não usa a meta (Janela − Σ P), então não é afetado.
   - A medida de controle `Valorizado (Real)` usa a meta. Ela precisa da meta **cheia**: coluna nova `Meta Cheia` = `Meta Hora × Fração`. Com a meta descontada, a janela da refeição contaria como tempo valorizado.
4. **Os 21h35 (1295/1440)** continuam só no cartão Meta e na HH Aderência. Nunca entram no OEE2.
5. **Página.** `pg_oee2` "OEE2 Trançagem" nasce no layout novo (menu lateral, cabeçalho e cardVisual) e vira o item "OEE2" no menu Mangueira das 11 páginas.

**Passos para entregar, cada um com o "sim" do William:**
- **1. Modelo** (script TMDL, aplicado com Libero; o **revisor** confere a regra de parada e a pausa):
  - `dMotivoParada` com Família, Categoria, No OEE2, Componente, Ordem e Cor da seção A, gerada pelo `gerar_mapa_motivos.py`;
  - coluna `Meta Cheia` na `fHoraCheia`;
  - tabela `dEtapaOEE`;
  - medidas da pasta OEE2.
  - Nenhuma medida existente muda.
- **2. Validação:** script pandas sobre o CSV da lista. O BI precisa bater em ±0,5 ponto no mesmo período e filtro, por máquina e por turno.
- **3. Relatório:** `pg_oee2` com os cartões OEE2, TCU, D, P e Q (referência de set a nov, sem meta fixa), cascata nas cores das famílias, Pareto por categoria e por motivo, matriz máquina × turno, linha por dia e rodapé com as limitações. Mais o item no menu.
- **4. App** (depois): dropdown de motivos ordenado por família. Depende do export do App.Formulas.

**O que a tela de OEE do app de homologação (PPLMS, dia 11/11/2026) ensina para o BI.** O William abriu essa tela em 12/11. Ela importa os apontamentos e a qualidade do GMS e calcula o OEE por máquina. Os números de 11/11:

| Máquina | Metros | OEE | Disponibilidade | Performance | Qualidade |
|---|---|---|---|---|---|
| Spiral | 440 | 12,4% | 51,9% | 24,2% | 98,9% |
| TH01 | 1.481 | 152,1% | 95,2% | 162,4% | 98,4% |
| TH02 | 419 | 93,9% | 100% | 93,9% | 100% |
| TH03 | 0 | 0% | 37,7% | 0% | 97,7% |
| TH04 | 0 | 0% | 100% | 0% | 100% |
| TH05 | 0 | — | — | — | — |
| TH06 | 2.011 | 92,4% | 90,2% | 102,9% | 99,6% |
| TH07 | 2.325 | 75,3% | 83,9% | 90,3% | 99,3% |
| TM01 | 1.010 | 78,7% | 84,0% | 94,7% | 98,9% |
| TM04 | 0 | 0% | 100% | 0% | 100% |
| TO04 | 143 | 9,9% | 93,6% | 10,9% | 97,7% |

- Média simples de 10 máquinas: OEE 51,5%, disponibilidade 83,7%, performance 57,9%, qualidade 99,0%.
- Metas: OEE 69,8%, disponibilidade 70%, performance 100%, qualidade 99,8%.

Quatro pontos em que a tela foge do documento. O BI tem de fazer diferente:
1. **Performance acima de 100%** (TH01 162%, TH06 103%) significa que a velocidade validada está abaixo do real. Na TH01 isso já se sabe: são as duas passadas, MEL-241. Pelo documento, performance = velocidade real ÷ velocidade validada máxima, então não passa de 100%. O BI **não capa em silêncio**: mostra a máquina com aviso "velocidade validada abaixo do real" e conta no máximo a janela inteira como valorizada. Isso já vem da conta Janela − Σ P, porque o parado nunca é negativo.
2. **Máquina sem produção planejada** (TH03, TH04 e TM04 com 0 m) é "sem atividade" (azul). Fica **fora do OEE2**, em branco e não 0%, e entra só no TCU. Na tela ela aparece com 0% e disponibilidade de 100%, o que derruba a média.
3. **OEE consolidado é ponderado pelo tempo:** Σ valorizado ÷ Σ tempo de produção, nunca média simples das máquinas. A própria tela avisa que a média dela "não é OEE consolidado".
4. **TO04 com 10,9% e a Spiral com 24%** são o mesmo sintoma do item 1 ao contrário: velocidade validada alta demais ou apontamento incompleto. O BI mostra isso sem esconder, e a lista de máquinas fora do padrão vai para o William.
- **Conferência cruzada na validação (passo 2):** comparar o OEE2 do BI de 11/11 por máquina com esta tabela. Diferença só é aceita se for explicada por um dos 4 itens acima.
- **Metas:** a tela usa 69,8% / 70% / 100% / 99,8%. O BI segue sem meta fixa (Q3 de 09/11) e mostra a referência de set a nov, até o William decidir adotar essas metas.

**O que dá para garantir e o que não dá:**
- **Dá:** depois dos passos 1 a 3, o BI calcula OEE2 e TCU exatamente pela definição das páginas 10 a 12, com cada motivo na família certa.
- **Não dá sem sensor:**
  - separar microparada e velocidade reduzida de parada (só pela classificação do motivo);
  - a qualidade, que fica pela data do refugo.
- Por isso o cartão leva o rótulo "OEE2 (apontamento)".

## Contexto
Escopo: só o Hora-Hora da célula de mangueiras (Trançagem; Cobertura, Mandril e Tubo só no mapeamento). A Montagem fica fora.
O William quer que o Hora-Hora siga o padrão de apontamento do OEE da Danfoss (o OEE2 do Factbird, que a Danfoss chama só de OEE) e que o Power BI chegue ao nível do relatório de paradas do Factbird: OEE2 e TCU, cascata, Pareto por categoria e causa, por célula, turno, mangueira e dia.
Fonte: `Dados_Brutos/Factbird_Governance_OEE.pdf`, páginas 10 a 12 e 17 a 20.

**O padrão Danfoss, resumido (páginas 10, 11 e 12):**
- Há 4 famílias de parada:
  - Azul, sem atividade: fim de semana, feriado, sem produção planejada.
  - Cinza, atividades não produtivas: manutenção planejada (preventiva, autônoma), validação (teste), pessoal (pausa, reunião, treinamento).
  - Amarela, troca de lote: preparação, troca de ferramenta, checagem de qualidade, partida, reabastecimento, limpeza.
  - Vermelha, perdas durante a operação: defeito de máquina, defeito de processo (OP faltando, material faltando, enrosco, quebra de material), espera (especialista, operador, material, manutenção), utilidades, TI, limpeza após quebra.
- **OEE2 = tempo valorizado ÷ tempo de produção.** O tempo de produção é o tempo de equipamento menos azul e cinza. A amarela entra no OEE2 como perda de disponibilidade.
- **TCU = tempo valorizado ÷ tempo total do equipamento (24/7).** Azul e cinza entram no TCU.
- Disponibilidade = perdas amarelas. Performance = vermelhas (quebras, microparadas, ociosidade por falta de material, velocidade reduzida). Qualidade = refugo e retrabalho.
  - **Diferente do OEE clássico:** a Danfoss põe quebra em Performance, não em Disponibilidade. Este plano segue a Danfoss.

## Achados que mudam o desenho (conferidos por dois caminhos)
1. **O Tempo Parado do Hora-Hora é tempo equivalente perdido, não tempo de máquina parada.**
   - Set a nov: a soma do proporcional `Min × (Meta − Real) ÷ Meta` dá 228.957 min; o Tempo Parado gravado e capado dá 225.953 min (1,3% de diferença).
   - Por isso parada, microparada e velocidade reduzida chegam misturadas. Quem separa disponibilidade de performance é **só a classificação do motivo**. Microparada não é mensurável sem sensor (o Factbird só cobre a TH07).
2. **OEE2 estimado da Trançagem, de 01/09 a 06/11** (10 máquinas, 8.140 linhas). É estimativa: vem do apontamento, não de sensor.

   | | Minutos |
   |---|---|
   | Janelas | 429.920 |
   | Planejada (azul + cinza) | 51.431 |
   | **Tempo de produção** | **378.489** |
   | Amarela | 60.681 |
   | Vermelha | 114.532 |
   | **Tempo valorizado, pelas perdas** | **203.276** |
   | Tempo valorizado, por Real ÷ velocidade (2º caminho) | 200.105 |

   - **OEE2 sem qualidade ≈ 53,7%**, pelo 2º caminho 52,9%. A diferença vem dos 929 min de produção acima da meta e do arredondamento do Tempo Parado.
   - Disponibilidade 84,0% · Performance 64,0% · Qualidade ≈ 98,5% (`TiposErros`: 5.534 m de refugo com trançadeira contra 378.344 m produzidos; a data é a do refugo, não a da trança) → **OEE2 ≈ 52,9%**.
   - **TCU ≈ 19%**: valorizado 202.924 min × Q 0,985 ÷ (11 máquinas × 1.440 min × 67 dias). A pausa fixa não muda o TCU.
   - Por máquina: TH06 67% · TM01 63% · TO04 63% · TH01 60% · TH02 60% · TH07 58% · TH05 54% · TH03 41% · TM04 36% · **Spiral 18%**. A Spiral sugere velocidade validada errada; a meta das duas passadas (MEL-241) afeta TH01 e TO04.
3. **A refeição só é declarada em 59% dos turnos de máquina com produção** (1º turno 48%, 2º 65%, 3º 75%; mediana de 45/45/60 min).
   - Nos outros turnos a pausa cai em Motivo Não Declarado ou em outro motivo vermelho.
   - Isso derruba o OEE2 em cerca de 4 pontos (≈ 16.600 min, estimativa).
   - **Decidido pelo William em 09/11 (Q1): pausa fixa de 45 min em cada turno.** Com a regra da seção B, o OEE2 de set a nov fica ≈ 55,1% sem qualidade e ≈ 54,3% com qualidade (disponibilidade 83,5%, performance 66,0%). Detalhes:
     - 786 turnos de máquina com produção × 45 min = 35.365 min de pausa, contra 25.818 min declarados como refeição.
     - Em 253 turnos a refeição declarada passou de 45 min; os 3.358 min de sobra ficam como perda vermelha.
4. **509 linhas de set a nov têm `Minutos` = 0**, com 16.586 min de Tempo Parado. Elas saem do cálculo até o BI derivar os minutos do rótulo da hora (fase 1).
5. **Motivo 2 não tem tempo próprio** (1.112 linhas): entra só como contagem, nunca no Pareto de minutos.
6. **A regra do dia útil não pode entrar no OEE2.** Ela já é uma pausa planejada embutida na meta; somada ao cinza, a pausa seria descontada duas vezes.
   - Em 09/11/2026 o William trocou 21h35 (1295/1440) por **21h45 (1305/1440)**: são os mesmos 45 min por turno do OEE2.
   - A troca foi feita em `HH Meta Útil (m)` e `HH Aderência`, no `reportExtensions.json`. Só vale depois que ele reabrir o projeto e publicar.

## A. Mapeamento: motivo → família / categoria / OEE2 / componente
Fora do OEE2 = parada planejada: sai do tempo de produção, mas entra no TCU. A coluna de minutos é de 01/09 a 06/11/2026, motivo principal, Tempo Parado capado na janela; os motivos numerados antigos estão somados ao texto limpo.

| Motivo (texto limpo) | Família | Categoria Danfoss | No OEE2? | Componente | Linhas | Min |
|---|---|---|---|---|---|---|
| Falta de Demanda | Azul | Sem atividade / sem produção planejada | não | — | 5 | 280 |
| Refeição / Almoço / 21-Refeição | Cinza | Pessoal: pausa | não | — | 542 | 25.818 |
| Reunião (Mandril: Reunião/Treinamento) | Cinza | Pessoal: reunião / treinamento | não | — | 196 | 8.684 |
| Manutenção Preventiva (+ "Fora do Prazo") | Cinza | Manutenção planejada | não | — | 278 | 15.530 |
| Manut. Prod. Total (MPT) | Cinza | Manutenção planejada / autônoma | não | — | 0 | 0 |
| Amostra ⚠ | Cinza | Validação (teste de produto) | não | — | 25 | 1.119 |
| TESTE ENGENHARIA | Cinza | Validação | não | — | 0* | 0 |
| Set-up | Amarela | Troca de lote: preparação / troca de ferramenta | sim | Disponibilidade | 400 | 19.829 |
| Registro de Pick (e "Peck") | Amarela | Troca de lote: checagem de qualidade | sim | Disponibilidade | 7 | 118 |
| Execução Check List Lean ⚠ | Amarela | Partida / início de turno | sim | Disponibilidade | 49 | 1.232 |
| Alimentação de fio ⚠ | Amarela | Reabastecimento | sim | Disponibilidade | 572 | 25.632 |
| Troca de Carretel ⚠ | Amarela | Reabastecimento | sim | Disponibilidade | 361 | 9.652 |
| Troca de Lenon / Troca de boneca | Amarela | Reabastecimento | sim | Disponibilidade | 113 | 3.350 |
| Emenda de Fita ⚠ | Amarela | Reabastecimento | sim | Disponibilidade | 33 | 430 |
| Bobinagem de Arame Espiral / Puxada do Insulation | Amarela | Reabastecimento (preparo de material) | sim | Disponibilidade | 8 | 438 |
| Manutenção Corretiva | Vermelha | Defeito de máquina | sim | Performance | 355 | 16.664 |
| Ajuste da Máquina ⚠ | Vermelha | Defeito de máquina (re-set) | sim | Performance | 327 | 8.702 |
| Quebra de fio | Vermelha | Defeito de processo: quebra de material | sim | Performance | 290 | 6.108 |
| Análise/Problema no tubo (+ "Problema no tubo") | Vermelha | Defeito de processo: material ruim | sim | Performance | 35 | 1.577 |
| Resto de fio ⚠ | Vermelha | Defeito de processo | sim | Performance | 25 | 1.018 |
| Falta de programação | Vermelha | Defeito de processo: OP faltando | sim | Performance | 0 | 0 |
| Falta de fio - Bobinadeira | Vermelha | Espera: material | sim | Performance | 431 | 21.099 |
| Falta de tubo ⚠ | Vermelha | Espera: material | sim | Performance | 287 | 14.976 |
| Falta de insulation / Carretel / Lenon / Mandril / Mandril Soldado / Mangueira | Vermelha | Espera: material | sim | Performance | 117 | 5.312 |
| Falta de operador ⚠ | Vermelha | Espera: operador | sim | Performance | 280 | 12.580 |
| Falta de energia / ar | Vermelha | Utilidades | sim | Performance | 39 | 1.148 |
| Divergência do Tempo Padrão | Vermelha | **Velocidade reduzida** | sim | Performance | 397 | 4.039 |
| Motivo Não Declarado ⚠ | Vermelha | Não declarado (sem par no padrão) | sim | Performance | 767 | 20.419 |
| Sem apontamento ⚠ | Vermelha | Não declarado | sim | Performance | 51 | 889 |
| (sem motivo; 92% no ou acima da meta) | — | — | — | — | 2.150 | 352 |

\* TESTE ENGENHARIA aparece só no Motivo 2.

**Totais de set a nov:**

| Família | Min | Horas | Parte da perda |
|---|---|---|---|
| Vermelha | 114.532 | 1.909 h | 50% |
| Amarela | 60.681 | 1.011 h | 27% |
| Cinza | 51.151 | 853 h | 22% |
| Azul | 280 | 5 h | 0,1% |

**Motivos das outras listas, para a `dMotivoParada` ficar completa:**
- Cobertura, Mandril e Tubo:
  - Troca de composto e Troca de Ferramental (fieira/matriz): amarela, troca de lote.
  - Falta de composto e Falta de desmoldante: vermelha, espera por material.
  - Problemas com composto e Problemas de qualidade: vermelha, defeito de processo.
  - Inventário: azul.
- **Escopo: só o Hora-Hora da célula de mangueiras. A Montagem fica fora.** As linhas de Montagem que já existem na `dMotivoParada` (TE, AU, CA, LI, RT, VR, FC, FI, AP, IT, TU, RF) não são tocadas e não recebem família. A página OEE2 filtra só a `fHoraHora`.

**Motivos ambíguos (⚠) e a escolha feita pelo padrão Danfoss:**
- **Falta de operador** fica vermelha. A Danfoss lista "Waiting for Operator" quando a linha estava planejada; máquina sem gente planejada não abre turno (já é a regra de máquina ativa do app). 210 h.
- **Alimentação de fio, Troca de Carretel, Emenda de Fita** ficam amarelas (reabastecimento). Se forem causadas por quebra, o operador deve usar Quebra de fio.
- **Ajuste da Máquina** fica vermelho (re-set de máquina). O ajuste logo depois de troca de OP deveria ir como Set-up.
- **Execução Check List Lean** fica amarela: a Danfoss põe início de turno em setup e ajustes.
- **Amostra** fica cinza (validação), porque a meta já é zero no app.
- **Falta de tubo** fica vermelha (falta de material a montante). Só seria azul se não houvesse OP planejada; para isso existe Falta de Demanda.
- **Motivo Não Declarado e Sem apontamento** ficam vermelhos: perda dentro do tempo planejado, sem causa, igual ao "unregistered" do Factbird.
- **Refeição** fica cinza pela pausa fixa de 45 min por turno (Q1, seção B).

**Categorias do padrão que o GMS não tem:**
- Fim de semana e feriado: saem do calendário, não de motivo.
- Treinamento separado de reunião.
- Limpeza (fim de turno, semanal, após quebra).
- Checagem de qualidade fora do Pick.
- Partida.
- Esperando manutenção, separado de manutenção em andamento.
- Esperando especialista.
- TI (computador, rede).
- Microparada.
- Refugo como causa.

**Recomendação:** não criar motivo novo agora. A Danfoss pede poucos motivos, e os 35 cobrem as 4 famílias. Reavaliar Limpeza e Treinamento depois de um mês de OEE2 no BI.

## B. Como calcular (grão: linha da `fHoraHora`, filtro por célula, turno, mangueira e dia produtivo 05:20–05:20)

**Campos de cada linha:**
- `Min` = `Minutos BI`. Se `Minutos` = 0, derivar do rótulo da `Hora BI` na fase 1.
- `P` = MIN(`Parado BI`, `Min`).
- Família pela `dMotivoParada`.

**Tempos:**
- Janela = Σ Min
- Planejada = Σ P das linhas azuis e cinzas (com a pausa fixa de 45 min por turno no lugar da refeição declarada; ver abaixo)
- Produção = Janela − Planejada
- Amarela = Σ P das linhas amarelas
- Vermelha = Σ P das linhas vermelhas e não declaradas
- **Valorizado = Produção − Amarela − Vermelha.** É o caminho oficial. Cada linha é capada na sua janela, então o excedente de uma janela nunca abate a parada de outra (regra "parada real nunca soma com tempo excedido").

**Índices:**
- Disponibilidade = (Produção − Amarela) ÷ Produção
- Performance = Valorizado ÷ (Produção − Amarela)
- Qualidade = 1 − Refugo (m) ÷ Real (m). Refugo = `TiposErros[Quantidade]` com `Trançadeira` normalizada (TH-02→TH02, TM.01→TM01), na data do refugo (aproximação declarada).
- **OEE2 = D × P × Q**
- **TCU = Valorizado × Q ÷ (1.440 × dias do filtro × todas as 11 máquinas da `fx_CelulasTrancagem`)**. É fixo e não depende do planejamento, que muda o tempo todo (William, 09/11). As horas sem linha no Hora-Hora são azuis (sem atividade).

**Pausa de refeição (decisão do William, 09/11/2026: 45 min fixos em cada turno):**
- **Quem recebe a pausa:** todo turno de máquina (Data × Turno × Célula) com Real > 0 recebe pausa planejada de MIN(45, Σ Min do turno). Ela entra em Planejada (cinza).
- **Refeição declarada nesses turnos:** os minutos com motivo Refeição ou Almoço saem do cinza e são absorvidos pela pausa fixa.
- **Turno sem produção:** a refeição declarada segue cinza, como qualquer motivo.
- **Valorizado:** Janela − Σ P de todas as linhas, independente da pausa. Por isso a pausa fixa não desconta duas vezes.
- **Vermelha na cascata:** é o resíduo, Produção − Amarela − Valorizado. Ela inclui:
  - a refeição declarada acima de 45 min;
  - a pausa não declarada que o operador lançou em outro motivo.
- **Pareto:** continua mostrando o motivo declarado.
- **Fica de fora:** a regra dos 21h45 (135 min/dia, a mesma pausa) continua valendo só em `HH Meta Útil (m)` e `HH Aderência`. Ela não entra no OEE2.
- **Revisor:** confere esta regra (cálculo de parada).

**Conferência obrigatória:**
- Medida de controle `OEE Valorizado (Real)` = Σ MIN(Real BI, Meta BI) × Min ÷ Meta BI.
- A diferença para o oficial tem de ficar abaixo de 2%. Hoje é 1,6%.

**Velocidade validada:**
- A Meta Hora vem do `DM_ENGRENAGENS` (velocidade teórica).
- O desvio aprovado (`DM_ENGRENAGENS_DESVIO`) baixa a velocidade validada e esconde a perda de velocidade. É correto pela Danfoss se o desvio for aprovado e com prazo, e é por isso que o desvio tem `Fim`.

**Setup:**
- O amarelo "Set-up" do OEE2 é a perda em metros nas janelas declaradas como Set-up. Não é o KPI de setup.
- O KPI de setup continua sendo da última peça boa da OAP até a primeira peça boa da próxima (ficha), nunca por cliques. No visual, o rótulo é "Set-up declarado no Hora-Hora". O `revisor` confere.

**O que falta, declarado no visual:**
- Microparada e velocidade reduzida não se separam de parada sem sensor. A Divergência do Tempo Padrão é a única velocidade reduzida declarada.
- A Qualidade é por data do refugo, não da trança.
- Rótulo: "OEE2 (apontamento)", na linha da regra K18 de honestidade do Mestre BI.

## C. Mudanças no app (fase 2, depois do BI validado)
1. **`fx_MotivosParada` em `Telas/Formulas.txt`:**
   - Novas colunas `Familia`, `Categoria`, `NoOEE2` (Boolean) e `Ordem`. O `Tipo` fica (MTBF).
   - O texto de cada motivo não muda, porque é a chave gravada no SharePoint e no histórico.
   - Readicionar "Divergência do Tempo Padrão". **Antes, pedir o export do App.Formulas**, porque o `Formulas.txt` está atrás do Studio (DECISÃO de 06/11, MEL-256).
2. **Mesmas colunas na `fx_MotivosParadaCobertura`.**
3. **`scr_HoraHora_Trancagem_2.txt`:** `Items` dos 3 dropdowns (`cmb_MotivoHHT`, `cmb_Motivo2HHT`, `cmb_MotivoSemProdHHT`) = `SortByColumns(fx_MotivosParada, "Ordem")`.
   - Agrupa por família: planejadas primeiro, depois troca, depois perdas.
   - Mesmo controle `Classic/DropDown@2.3.1` (provado). Sem mexer em X, Y, Width, Height.
4. **Mandril e Tubo** (listas próprias `Hora_Hora_Mandril` e `Hora_Hora_Tubo`, arrays dentro da tela): fora desta rodada. A `dMotivoParada` já cobre os textos deles.
5. **Ciclo:** ler o `.txt` → patchar → `python gms_qa_yaml.py Telas\scr_HoraHora_Trancagem_2.txt` → gravar `Telas/` (Formulas e tela) → diário (MEL-266, `gms.py --check`) → o William cola no Studio e publica.
   - Nenhum dado do SharePoint muda.

## D. Mudanças no BI
1. **D0, leitura (sem gravar):**
   - `INFO.TABLES`, `INFO.RELATIONSHIPS` e `INFO.MEASURES` para confirmar onde vivem `Motivo Padrão`, `Minutos BI`, `Parado BI` e `Real BI`. Hoje a página Paradas usa `'Hora-Hora'` e a Hora-Hora usa `fHoraHora`.
   - Relação `fHoraHora[Motivo Padrão]` → `dMotivoParada`.
2. **Modelo (com libero e revisor):**
   - `dMotivoParada` (DATATABLE em `PowerBI/modelo/dMotivoParada.dax.md`): mais `Família`, `Ordem Família`, `Categoria`, `No OEE2`, `Componente` e `Cor` (hex do tema claro).
   - Fonte mestre: `motivos_mapa.csv` e `dMotivoParada.csv`, estendidos e gerados por `gerar_mapa_motivos.py` (reaproveitar; ele gera os dois e passa a gerar o DAX).
   - Na `fHoraHora`, coluna `Minutos OEE`: `Minutos BI`, ou, se `Minutos` = 0, os minutos da grade pelo rótulo da hora.
   - Tabela desconectada `dEtapaOEE` para a cascata: Janela, Planejada, Produção, Amarela, Vermelha, Operando, Valorizado, Refugo, Valorizado bom.
   - **Medidas base no modelo, pasta "OEE2"**: Janela, Planejada, Produção, Amarela, Vermelha, Valorizado, Valorizado (Real), Disponibilidade, Performance, Qualidade, OEE2, TCU e Cascata (SWITCH).
     - Vão no modelo porque medida de relatório não pode chamar outra medida de relatório (seção 11 do roteiro).
     - **Medida existente não muda**: `HH Meta Útil (m)`, `HH Aderência`, `HH Parado (min)` e a regra dos 21h45 ficam como estão.
3. **Relatório** (PBIR por JSON, `json.dump(indent=2, ensure_ascii=False)`, CRLF):
   - **Página nova** `pg_oee2` "OEE2 Trançagem". Não regerar nem mexer no layout das páginas salvas.
   - Visuais:
     - Cartões OEE2, TCU, D, P e Q com meta (a meta é pergunta Q3).
     - Cascata nativa por `dEtapaOEE`, nas cores das famílias.
     - Pareto por categoria e Pareto por motivo, com cor da família.
     - Matriz de máquina × turno com o OEE2.
     - Linha por dia produtivo.
     - Segmentação por célula, turno, mangueira e data.
     - Rodapé com as limitações (B).
   - Tema claro vigente.
4. **Histórico:**
   - Nada é regravado no SharePoint. Os motivos numerados já caem no texto limpo pela `Motivo Padrão` (tira "NN - ", Refeição → Almoço, Problema no tubo → Análise/Problema no tubo).
   - Faltam no DATATABLE: "Registro de Pick", "Registro de Peck", "TESTE ENGENHARIA", "Bobinagem de Arame Espiral", "Puxada do Insulation", "Troca de boneca" (conferir) e os da Cobertura.
   - Linha sem motivo e no ou acima da meta: P = 0, não afeta nada.
   - Janeiro a 03/09 entra só como leitura. A página abre por padrão em 04/09 em diante (pós-higienização).

## E. Fases, risco, revisão, quem publica, volta
| Fase | O quê | Risco | Revisor | Publica | Volta |
|---|---|---|---|---|---|
| 0 | Gravar este plano em `Analises/OEE2_HoraHora/`, mais `mapa_oee2.csv` e o script de conferência (pandas). Diário MEL-266 ABERTO | nenhum | revisor-leve | — | git revert |
| 1 | Modelo: `dMotivoParada` estendida, `Minutos OEE`, `dEtapaOEE`, medidas OEE2. Refresh | médio: medida errada no painel vivo; DATATABLE com chave duplicada | **revisor** (parada/setup, turno, pausa de 45 min, 21h45, excedido) | William aplica o refresh; eu aplico no TMDL só com libero | script TMDL anterior salvo; apagar colunas, tabela e medidas novas |
| 2 | Validar no próprio GMS: um dia × turno × máquina contra a lista e o script pandas | — | — | — | — |
| 3 | Relatório: página `pg_oee2` | baixo: página nova; o William precisa reabrir o projeto antes de publicar | revisor-leve | **William** pelo Desktop | apagar a pasta da página |
| 4 | App: colunas na `fx_MotivosParada` / `Cobertura`, `Items` ordenado, Divergência de volta (depois do export) | baixo: o texto gravado não muda | revisor-leve (sem regra de parada) | **William** cola e publica | colar o `Formulas.txt` anterior do git |
| 5 | Depois de 1 mês: decidir Limpeza e Treinamento, e a pausa fixa | — | revisor | — | — |

## F. Perguntas para o William (só o que é dele)
- **Q1: RESPONDIDA em 09/11/2026.** Pausa fixa de 45 min em cada turno (135 min/dia por máquina), com a regra da seção B. A sugestão era 45/45/55; o William fixou 45 nos três turnos.
- **Q2: RESPONDIDA em 09/11/2026.** O TCU conta todas as 11 máquinas, inclusive a TH04. O planejamento muda a todo momento, então não se define máquina fora; o critério vai ficando mais certeiro com o uso do padrão.
- **Q3: RESPONDIDA em 09/11/2026.** Não há Factbird; a fonte é o GMS.
  - Sem meta fixa por enquanto. O cartão mostra a **referência de partida do GMS** (set a nov: OEE2 ≈ 54%, TCU ≈ 19%) e a tendência.
  - A meta é definida depois de alguns meses de OEE2 no padrão.
  - A comparação com o Factbird sai da verificação.

**Escolhas adotadas pelo padrão Danfoss, sem pergunta:**
- Falta de operador e Falta de tubo vermelhas.
- Ajuste da Máquina vermelho.
- Alimentação de fio, Troca de Carretel e Emenda de Fita amarelas.
- Check List Lean amarelo.
- Amostra cinza.
- Não declarado vermelho.
- Nenhum motivo novo agora.
- Quebra em Performance.

## G. Conciliação Hora-Hora × ficha de produção: ADIADA (William, 09/11/2026)
> **Fora desta rodada.** A conciliação pode ter impacto grande e talvez precise valer de janeiro em diante, então não entra agora.
> Agora só se arruma o Hora-Hora no padrão OEE2 (seções A a E). Não há coluna `Confere Ficha` na fase 1 nem mudança no app de mangueira por OP.
> O que está abaixo fica registrado para quando o William retomar o assunto.
Regra: o produto que o Hora-Hora aponta numa janela tem de ser o da OP que a `ficha_producao` mostra na mesma trançadeira naquela hora, e os metros têm de fechar.
O cruzamento é por OP: cada OP com trançagem, mesma `Trançadeira`, e as janelas do Hora-Hora com produção cujo meio cai entre `data_hora_inicio_trancadeira` e `data_hora_final_trancadeira`.

Período de 04/09 a 06/11/2026. É uma primeira leitura, estimativa:
- 670 OPs com trançagem; 600 têm janela do Hora-Hora dentro do intervalo.
- **Metros fecham no total**: ficha 301.109 m, Hora-Hora 306.658 m (razão 1,02). Por OP, porém, só 54% ficam entre 0,8 e 1,2 (mediana 0,95).
- **Produto**: em 3.938 janelas dentro de OP, 79,5% têm a mesma mangueira da ficha. Em 56 OPs nenhuma janela bate.
- **Janela sem OP**: 795 de 4.623 janelas com produção (17%, 54.622 m) não caem em OP nenhuma da ficha naquela máquina e hora. 280 delas são da TO04.

O que mais explica a divergência de produto:
- **Mesmo produto escrito diferente** (não é erro de apontamento):
  - GH781-6 × GH781-6-2 (duas passadas, MEL-241);
  - HC139-7_SGX × HC139-7(S/G);
  - EC118-08L × EC118-08L-RL;
  - HC139-7-250MTS × HC139-7.
- **Produto diferente de verdade**:
  - TH01: ficha EC215-06L × Hora-Hora GH781-6 (97 janelas);
  - TH07: EC215-08L × GH781-8 (40);
  - TH02: EC115-08L × EC118-08L (51).

Ideias para quando for retomada (nada disto está agendado):
1. **BI:** coluna `Confere Ficha` na `fHoraHora`, com OK, produto diferente ou sem OP. Mais um cartão de % de janelas conferidas na página OEE2.
   - O OEE2 por mangueira só vale para as janelas conferidas. A velocidade validada (a Meta) depende do produto, então produto errado é meta errada.
   - A comparação usa uma tabela de sinônimos de nome, reaproveitando o `Producao_GMS_x_MB51/dados/aliases_mangueira.csv`; o mesmo produto não conta como divergência.
2. **App:** a mangueira da janela do Hora-Hora da Trançagem passa a vir da OP "Em processo" daquela trançadeira na ficha, que é o mesmo sinal da máquina ativa (MEL-111). O operador só escolhe entre as OPs da máquina. Plano próprio antes de mexer.
3. **Histórico:** nada é regravado. As divergências viram lista de conferência para a supervisão, por máquina.

## Verificação
- Script pandas (fase 0) recalcula do CSV os números da seção "Achados". O BI tem de bater com ele em ±0,5 ponto para o mesmo período e o mesmo filtro.
- Os dois caminhos do Valorizado (perdas × Real ÷ velocidade) têm de ficar dentro de 2%.
- Σ por família = Tempo Parado capado total (soma fecha).
- Um dia × turno × máquina explicado linha a linha.

## Arquivos
- **Novos:**
  - `GMS/Analises/OEE2_HoraHora/PLANO_OEE2.md`
  - `GMS/Analises/OEE2_HoraHora/mapa_oee2.csv`
  - `GMS/Analises/OEE2_HoraHora/conferir_oee2.py`
- **Depois, por fase:**
  - `GMS/PowerBI/modelo/dMotivoParada.dax.md`
  - `GMS/PowerBI/modelo/motivos_mapa.csv`
  - `GMS/PowerBI/modelo/gerar_mapa_motivos.py`
  - `GMS/PowerBI/GMS_Painel.Report/definition/pages/pg_oee2/`
  - `GMS/Telas/Formulas.txt`
  - `GMS/Telas/scr_HoraHora_Trancagem_2.txt`
  - `GMS/GMS_Diario.md`
