# Plano · integrar o sensor Factbird (TH07) ao GMS · 20/10/2026

Status: **proposta, aguardando aprovação do William.** Nada foi alterado no app, no SharePoint, no Power Automate nem no Factbird.
Referências: C20 (Mestre), MEL-047 (piloto Factbird, bloqueado no token da API), MEL-070 (Sinóptico v2 com estado de sensor), C3, C4, C13, C19.

## 1. O que já sabemos (evidência de 20/10)

- Só a **TH07** tem sensor no Factbird (linha `GUA_HoseManufacturing_BraiderTH07`, sensor "Braider TH07 Uptime", código 42TH07). O sensor é só **ligado/desligado**: não dá motivo nem peça boa.
- O **MCP do Factbird** só tem 2 ferramentas (`fuzzy_search_node_ids` e `factbird_metrics`) e devolve **KPI agregado**, sem hora de cada parada. Serve para conferência, não para alimentar o GMS.
- O portal do Factbird **tem** o dado com hora: lista de paradas (resolução de 5 s) e gráfico de uptime por minuto, com histórico de pelo menos 3 semanas. O "Scheduled reports" só manda PDF por e-mail: não serve como feed.
- Comparação hora a hora, TH07, 01 a 15/10 (251 horas): `GMS/Analises/Sensor_TH07/`.
  - Total do turno fecha no 1º e no 2º (±5 a 6%), mas só 34 de 83 e 61 de 99 horas batem na hora.
  - **3º turno: 56 horas, `Tempo Parado` = 0 em todas**, e o sensor viu 979 min parados.
  - Das 153 horas com 0 parado no GMS, em 39% o sensor viu 10 min ou mais.
  - Parada longa apontada (45 min ou mais) tem confirmação do sensor em 79% das vezes.

**Conclusão:** o sensor é bom para dizer **quanto tempo** a máquina ficou parada. O operador continua sendo a fonte do **motivo**. A integração útil é o sensor sugerir o tempo e o operador escolher o motivo.

## 2. O que o sensor NÃO resolve (regras do GMS que ficam como estão)

- **Setup** = intervalo entre a última peça boa de uma OAP e a primeira peça boa da próxima. O sensor não vê peça boa nem OAP, então **não calcula setup**. Pode servir só como aviso ("máquina ficou X min parada entre duas OAPs").
- **Parada real nunca é somada com tempo excedido.** O sensor entra só como parada.
- **Turnos** seguem `fx_Turno`, `fx_InicioTurnoMin`, `fx_GradeHoraHora`: o sensor é cortado nas mesmas janelas do GMS (05:20, 13:47/13:57, 22:20 e horas cheias).
- O apontamento do operador **não é aposentado**; o sensor entra em paralelo, como o C20 já prevê.

## 3. Fases

### F0 · Acesso ao dado do Factbird (bloqueio hoje)
O C20 está parado no token da API. Perguntar à Danfoss/Factbird (suporte ou dono do contrato):
1. Existe API (GraphQL ou REST) com a lista de paradas e o uptime por intervalo, por linha? Como a conta do William ou uma conta de serviço obtém o token?
2. Existe webhook de início e fim de parada?
3. Existe exportação agendada de dados (CSV/Excel em pasta, SharePoint ou e-mail com anexo), além do PDF?
4. Qual a política de retenção do histórico e de uso do token (rate limit, rotação)?
5. Quando as outras trançadeiras recebem sensor?

**Ponte enquanto não houver token:** exportação manual do CSV de paradas e do gráfico (já funciona) e carga em lote. Serve para validar o desenho, não para operação.

### F1 · Validação sem mexer no app (1 a 2 semanas)
- Estender a comparação (ainda em arquivo de análise) para 3 a 4 semanas, com export novo do Hora-Hora.
- Definir com o William os três parâmetros: corte de ruído do sensor (hoje ≥ 1 min), faixa de "bate" (hoje ± 5 min) e quando uma divergência vira alerta.
- Saída: um número de confiabilidade por turno (1º, 2º, 3º) e um critério de pronto para a F4.
- Sem alteração de arquivo do app.

### F2 · Ingestão do sensor (precisa de F0)
- Lista SharePoint nova `Sensor_Paradas` (criação só com "sim"): `Maquina`, `Inicio`, `Fim`, `DuracaoSeg`, `IDExterno` (idempotência), `Fonte`.
- Fluxo Power Automate `GMS_SensorParadas_Sync`: recorrente (sugestão: a cada 10 a 15 min), lê as paradas novas do Factbird e grava na lista. Chave `IDExterno` evita duplicar. Falha de leitura registra e não derruba o fluxo.
- Fuso: guardar em UTC e converter para horário de Brasília no corte das janelas (a coluna `Data` do Hora-Hora já está em UTC, meia-noite BRT = 03:00Z).
- Os dados ficam no tenant da Danfoss: nada sai para serviço externo.

### F3 · Consolidação por janela do GMS
- Fluxo (ou segundo passo do mesmo fluxo) soma a parada do sensor em cada janela do `fx_GradeHoraHora` e grava em coluna paralela da lista Hora-Hora: `ParadoSensor` (min), `NParadasSensor`, `FonteSensor`.
- Colunas **novas e opcionais**, sem mexer em `Tempo Parado (min)`. Itens antigos ficam em branco (`Blank()`, nunca 0).
- Calcular no fluxo e não no app evita varrer a lista de paradas dentro do Power Apps (limite de delegação).

### F4 · App: Hora-Hora da Trançagem (só TH07, depois outras)
Mudança em `Telas/scr_HoraHora_Trancagem_2.txt` (+ `Formulas.txt` se virar Named Formula). Proposta:
1. Mostrar ao lado do campo **PARADO** o valor do sensor da janela ("Sensor: 22 min"), só para máquinas com sensor.
2. **Sugerir** o valor quando o operador não digitou (pré-preenche com o do sensor, marcado como sugerido; o operador confirma ou corrige).
3. Divergência acima do limite da F1: destaque discreto, **sem bloquear** o salvamento.
4. **3º turno:** a sugestão resolve o buraco de 0 parado.
5. Na regra existente "janela abaixo da meta sem motivo vira Motivo Não Declarado com tempo proporcional", usar o tempo do sensor como base quando existir.
6. Nunca sobrescrever digitação do operador. Nunca somar parada com tempo excedido.
- Tela com layout ajustado à mão: patch por bloco, sem mexer em X/Y/Width/Height de controle existente. QA com `gms_qa_yaml.py` antes de entregar. Quem publica é o William.

### F5 · BI
- Coluna paralela `ParadoSensor` no modelo (`GMS_Mestre_BI.md`) e uma visão "apontado x sensor" por turno. Conferir `dTurno`. Não alterar o Mestre sem pedido explícito.

### F6 · Setup e demais máquinas
- Setup continua pela regra da peça boa. Sensor só como alerta de intervalo parado entre OAPs.
- Expandir para outras trançadeiras só quando o sensor existir nelas (F0, pergunta 5).
- C20 original (`inicio_sensor`/`fim_sensor` na ficha) fica para depois da validação: o sensor atual não separa início de produção de início de setup.

## 4. Decisões do William

1. Autorizar a pergunta à Danfoss/Factbird da F0 (você é quem tem o contato).
2. Aceitar o desenho "sensor sugere o **tempo**, operador escolhe o **motivo**" para a F4.
3. Limite de divergência e corte de ruído na F1 (proponho 1 min e ± 5 min até medir mais).
4. Ordem: F0 e F1 em paralelo; F2 em diante só com o token.

## 5. Riscos

- **Sem token**, só há a ponte manual: não vira operação.
- Ruído do sensor (muitas paradas de 5 s) infla contagem de parada se não houver corte.
- Sensor "ligado" pode ser máquina energizada sem produzir: o sensor mede uptime, não produção.
- Confiar no sensor sem validação distorce o BI: por isso F4 só depois da F1.
- Mudança de turno e fuso (UTC x Brasília) já causaram duplicados no Hora-Hora; a F3 corta nas mesmas janelas.

## 6. Processo

- Mudança no app, na regra de parada ou em turno passa pelo **`revisor`** antes de aplicar (regra de negócio). Eu chamo o revisor com o plano aprovado, antes da F3/F4.
- Mudança em mais de um arquivo só começa com este plano aprovado.
- Cada fase termina em linhas de diário (MEL-047 e novos itens: ID real só com `python gms.py --novo`; até lá "MEL-???").
- Criar lista SharePoint, fluxo ou coluna: só com o "sim" do William a cada alteração.

## 7. Arquivos por fase

| Fase | Mexe em |
|---|---|
| F0 | nenhum arquivo (pergunta ao Factbird) |
| F1 | `Analises/Sensor_TH07/` (novos CSV/MD) |
| F2 | SharePoint (lista nova), Power Automate (fluxo novo); doc em `Planejamento/` |
| F3 | Lista Hora-Hora (colunas novas), fluxo |
| F4 | `Telas/scr_HoraHora_Trancagem_2.txt`, possivelmente `Telas/Formulas.txt` |
| F5 | modelo do BI, `GMS_Mestre_BI.md` (só com pedido) |
