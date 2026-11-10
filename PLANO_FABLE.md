# PLANO FABLE: aproveitar o Fable até 16/11/2026

Escrito em 09/11/2026 (noite). Versão 2, depois de auditar a versão 1 (seção 8).

## 1. O que o medidor mostra (lido em 09/11, 23h56)
- Plano Pro. Limite de 5 h: 6%. Semanal geral: 28%. **Semanal Fable: 0%, barra própria.**
- As duas semanais reiniciam em **15/11 às 08h (Brasília)**. Ou seja: o Fable tem **uma barra cheia agora (10/11 a 15/11 08h)** e **uma segunda barra cheia de 15/11 08h a 16/11**.
- Preço de tabela: Fable custa 2,5x o Opus e 5x o Sonnet (entrada US$ 10, saída US$ 50 por milhão). Cada token Fable tem que virar algo que dure.
- Não sei se o Fable também desconta da barra geral. O primeiro bloco mede isso (seção 4). Até lá, vale a trava: barra geral acima de 85% = para os blocos Fable.

## 2. Princípio
**Fable faz o que é difícil de acertar e dura depois do dia 16: motores, contratos de dados, suítes de teste, especificações, revisão de regra de negócio.** Sonnet e Opus executam em cima do que o Fable deixou escrito.
Fable não faz: lote de Hora-Hora, clique no Studio, git, formatação, texto de rede, o que o Sonnet resolve igual. Isso continua no Sonnet para não gastar a barra geral.

## 3. Onde gastar (ordem de retorno)
Fatia = parte da barra Fable de cada janela. Ajusta depois da calibração.

| # | Frente | Fatia | O que o Fable entrega (fica no repositório) | Quem usa depois |
|---|---|---|---|---|
| A | **Motor gráfico dos vídeos (Bit)** | 30% | Fases 1 a 4 do `Producao/serie/PLANO_VISUAL.md` (atmosfera, personagem em vetor, composição, movimento) e, na segunda barra, a Fase 6 (motor em módulos). Cada fase com folha de contato antes/depois e hash dos episódios já publicados intacto. Mais o `MOTOR_GUIA.md`: como pedir cada efeito pelo JSON. | Sonnet renderiza os episódios; Opus (`produtor-de-artes`) só faz imagem, áudio e a Fase 5 (cenários PNG) |
| B | **Power BI** | 20% | OEE2 Danfoss (MEL-266): medidas DAX conferidas contra um dia de produção já validado à mão; revisão de desempenho do modelo; `GMS_Mestre_BI.md` atualizado | Sonnet mantém e atualiza |
| C | **Power Apps (Canvas)** | 15% | Triagem das 254 MELs abertas (fechar o obsoleto, ranquear o resto); auditoria das `Telas/` (skill `analyze-canvas-performance` + `gms_qa_yaml.py`); patches difíceis (App.OnStart, fx_CorEtapaBobinagem, limite de linhas) | Sonnet aplica os patches seguintes pelo mesmo padrão |
| D | **IA: Copilot Studio (Uiu)** | 15% | F2: especificação da lista `Uiu_Agregados` (com as correções de planejamento do `PROXIMA_SESSAO.md`), instruções v3 e uma **bateria de 50 perguntas com resposta esperada** para provar o agente | Opus/Sonnet executa no navegador do app; a bateria roda a cada mudança |
| E | **Qualidade, Engenharia, Produção e apontamento** | 10% | Contratos de dados (refugo/TiposErros sem duplicado, tempo padrão, Hora-Hora, divergência), regras de validação do apontamento e um script de conferência diária | Sonnet roda a conferência |
| F | **Power Automate** | 5% | Padrão de fluxo (tratamento de erro, log, nomes) e auditoria. **Precisa que você exporte os fluxos** (não tenho acesso aqui) | Sonnet |
| R | **Reserva** | 5% | Correções que o Sonnet/Opus apontarem nos entregues do Fable | Fable |

## 4. Calendário (blocos de 1 sessão Fable cada)
Regra de ritmo: no máximo **2 blocos por janela de 5 h**, porque o gargalo no Pro é o limite de 5 h, não só o semanal. Cada bloco: sessão nova, brief em arquivo, 1 entrega, commit no fim.

| Quando | Bloco | Antes do bloco (Sonnet, barato) |
|---|---|---|
| **Ter 10** manhã | **B1 calibração + A1:** Fase 1 (atmosfera) do motor. Medir quantos % da barra Fable e da geral o bloco gastou | Fase 0: hash dos quadros publicados e folha "antes" |
| Ter 10 tarde | B2 · D: especificação `Uiu_Agregados` + bateria das 50 perguntas | Republicar o Uiu do DPS (pendência, pede seu "sim") |
| **Qua 11** | B3 · B: OEE2 no modelo e validação DAX · B4 · A: Fase 2 (personagens) | Mostrar o dia de produção conferido à mão para a validação |
| **Qui 12** | B5 · C: triagem do backlog e auditoria das telas · B6 · E: contrato de refugo/TiposErros | `gms.py --estado` rodando (hoje quebra com acento, ver pendências) |
| **Sex 13** | B7 · A: Fases 3 e 4 (composição e movimento) · B8 · E: Engenharia e apontamento | Exportar os fluxos do Power Automate |
| **Sáb 14** | B9 · F: Power Automate (com o export) · bloco de **correções (R)** | Rotina semanal do Bit (sáb 20h) segue no Sonnet, sem tocar na barra Fable |
| **Dom 15, depois das 08h** (barra nova) | B10 · A: Fase 6 (motor em módulos) + `MOTOR_GUIA.md` final | Hash dos publicados continua igual |
| **Seg 16** | B11: revisão cruzada de tudo que o Fable fez (Fable lendo o próprio trabalho com olho frio) e **manual de uso sem Fable** | |

Se um bloco estourar o limite de 5 h, o trabalho já está commitado por entrega; o próximo bloco continua do arquivo, não da conversa.

## 5. Como rodar cada bloco (mecânica)
1. Sessão nova, modelo Fable, esforço alto só no bloco que for arquitetura (A, B, D); médio no resto.
2. O chefe (Sonnet) escreve o brief em arquivo: objetivo, arquivos, o que é "pronto", o que **não** pode mudar. Nada de conversa longa dentro da sessão Fable.
3. Antes e depois de cada bloco: `get_usage` (barra Fable e geral). O delta vai no `registro.md`.
4. Entrega só vale com prova: folha de contato (vídeo), conferência contra o dia validado (DAX), `gms_qa_yaml.py` verde (telas), bateria rodada (Uiu).
5. Revisão: regra de negócio (turno, parada/setup, OEE, norma) continua passando pelo tipo `revisor`. Nesta semana dá para chamá-lo com o modelo Fable no pedido, sem editar o arquivo do agente. Quem decide é você.
6. Publicar, agendar, enviar, apagar em definitivo: continua pedindo seu "sim" a cada ação.

## 6. Trava de segurança de uso
- Barra **geral** acima de 85%: pausa os blocos Fable (Sonnet precisa de folga para Hora-Hora, rotina do sábado e o dia a dia).
- Bloco que gastar mais que o dobro do previsto: para, commita e reavalia a fatia.
- Nada de Fable para tarefa que o Sonnet fez bem antes (registro de 09/11 mostra Hora-Hora e Studio ok no Sonnet/Opus).

## 7. Deixar o legado para depois do dia 16
Até 16/11 ficam escritos: `MOTOR_GUIA.md`, contratos de dados, bateria do Uiu, script de conferência diária e o manual "como pedir ao Sonnet o que o Fable pedia". Assim o Sonnet/Opus usa o motor novo sem precisar do Fable.

## 8. Auditoria do próprio plano (o que corrigi)
1. **V1 mandava Fable para tudo.** Errado: gasta barra com o que o Sonnet faz igual. Corrigido: só motor, contratos, testes, especificação e revisão (seção 2).
2. **V1 ignorava o limite de 5 h.** Mesmo com semanal sobrando, 2 blocos pesados na mesma janela travam o dia. Corrigido: máximo 2 por janela (seção 4).
3. **V1 não protegia a barra geral.** Se o Fable também desconta dela, ficaria sem Sonnet no sábado. Corrigido: calibração no B1 e trava de 85% (seção 6).
4. **V1 punha o Fable decidindo turno e OEE sozinho.** Contra a regra do repositório. Corrigido: revisão do `revisor` e conferência contra dia validado à mão.
5. **V1 deixava a conversa como memória.** Se o limite cortasse o bloco, perdia-se o raciocínio. Corrigido: brief em arquivo, commit por entrega.
6. **V1 não considerava a virada de 15/11 às 08h.** Corrigido: barra nova vira a Fase 6 e a revisão final.
7. **Power Automate sem dado.** Não consigo ver os fluxos daqui. Fatia reduzida a 5% e depende do seu export.
8. **Sem produto final.** Faltava garantir que o Sonnet use o motor depois. Corrigido: seção 7.

## 9. Pendências e incertezas
- Não confirmei a capacidade nem a hora exata de fim da promoção do Fable 5.2; confirmo pelo nome do modelo no B1 e você me diz se a data mudar.
- Fatias em % são estimativa até a calibração do B1.
- `python gms.py --estado` quebra no Windows com acento (cp1252). Corrigir com `PYTHONIOENCODING=utf-8` ou `-X utf8` antes do B5.
- Fase 5 do motor (cenários em PNG pelo Gemini) fica com o `produtor-de-artes`, é imagem.

---

# 10. V3 — ESCOPO AMBICIOSO (10/11/2026). Substitui as seções 2, 3 e 4.

Motivo: a v2 media o Fable pelo tamanho do Sonnet. O gargalo real é a barra (limite de 5 h e semanal), não a capacidade. Então cada janela de 5 h vira **uma missão grande, ponta a ponta**, e não vários blocos pequenos.

## 10.1 Como o Fable trabalha (muda tudo)
- **Brief por resultado, não por passo.** O chefe escreve só: objetivo, critério de aceite, o que não pode quebrar, onde gravar. O Fable decide arquitetura, ordem e ferramentas. Nada de micro-instrução do Sonnet.
- **Missão = uma sessão Fable inteira, longa e autônoma**, com ferramentas liberadas (código, testes, navegador, Power BI MCP, pac CLI), commit a cada marco.
- **Ele se audita:** a última hora de cada missão é ele mesmo atacando a entrega (teste, caso extremo, regressão) e corrigindo.
- **Paralelismo:** se você escrever "ultracode" ou "use um workflow", o Fable abre vários agentes na missão. Custa muito mais barra; uso só na missão P1 e P2.
- Trava: barra geral > 85% pausa; produção real (app em uso na fábrica, SAP, normas) nunca é alterada sem seu "sim" e sem cópia de segurança.

## 10.2 As missões (ordem de valor)

**P1. Motor de cinema do Bit.** Reconstruir o motor de vídeo em 3D/WebGL: Three.js com PBR, iluminação, sombras, câmera com lente e movimento, pós-processamento (bloom, grão, profundidade de campo, color grading), personagens riggados com expressão, cenários procedurais, render determinístico em MP4. Meta: qualidade de curta animado, não de slide. Entrega: motor + `MOTOR_GUIA.md` + 3 episódios-teste + hash dos publicados intactos. Depois, Sonnet/Opus só escrevem o JSON do episódio e rodam o render.

**P2. Gêmeo digital da célula GMS.** Simulador completo (8 etapas, turnos, paradas, setup, refugo, headcount) calibrado com o histórico real, com backtest. Faz what-if de demanda x pessoas e sequenciamento (APS), e entrega o resultado no Power BI. É a pendência de 01/11 (simulador headcount x demanda), agora sem o corte de tamanho.

**P3. Uiu / William do GMS completo.** F2 inteira: `Uiu_Agregados`, 4 agentes-filho, escrita com confirmação, bateria de 50+ perguntas com resposta esperada rodando sozinha, e uma versão local de reserva (Ollama + DuckDB) caso a DLP bloqueie. Fable opera o Studio e o SharePoint direto.

**P4. Auditor noturno do GMS.** Sistema que confere todo dia: GMS x MB51/SAP, refugo duplicado, turno, divergência de tempo padrão, dado parado, e abre as MELs sozinho no diário. Roda por Power Automate/Python. Cobre Qualidade, Engenharia, Produção e apontamento de uma vez.

**P5. GMS Cockpit + app de tablet em Code App (protótipo paralelo).** Painel único local (estado, backlog, diário, agentes, uso, alertas) e um protótipo React/Power Apps Code App do apontamento e do painel de célula, com PCF de Gantt/OEE. **Só protótipo ao lado**; o app em produção não é tocado.

Power BI e Power Apps não viram missão própria: entram dentro de P2, P4 e P5 e na triagem das 254 MELs (feita pela P4 no primeiro dia).

## 10.3 Calendário (uma missão por janela de 5 h; 2 janelas por dia)
| Quando | Missão |
|---|---|
| Ter 10 | **P1** (manhã, a maior) e **P3** (tarde) |
| Qua 11 | **P2** (dia inteiro, é a mais pesada em raciocínio) |
| Qui 12 | **P4** e continuação da P2 se não fechou |
| Sex 13 | **P5** |
| Sáb 14 | Continuação do que ficou aberto + correções que o Sonnet/Opus acharem. Rotina do Bit (20h) segue no Sonnet |
| Dom 15 (após 08h, barra nova) | **P1 fase 2**: polimento, mais personagens e cenários; `MOTOR_GUIA.md` final |
| Seg 16 | Revisão cruzada de tudo e manual "como usar sem o Fable" |

Calibração: a primeira missão (P1) mede quanto da barra uma missão grande consome. Se estourar, a ordem de corte é P5, depois P4; P1, P2 e P3 ficam.

## 10.4 O que isso não é
Não tenho como afirmar o teto do Fable 5.2: a escolha dos projetos acima é a minha aposta do que mais rende para você, e você pode trocar qualquer um. Se o Fable fizer mais do que o brief pede, melhor.

## 10.5 Redefinição do Fable (vale até 17/11, informada pelo William em 10/11)
Regra: **usar quando a barra Fable estiver em 90% ou mais e ainda houver missão pendente. Nunca com sobra.**
- Provável dia: quinta 12 ou sexta 13, depois de P1, P2 e P3. A calibração da P1 confirma o ritmo.
- Não esperar até domingo com a barra zerada: ficaria 2 a 3 dias parado, e a janela de 5 h limita o que dá para gastar em 15 e 16/11.
- Antes de clicar: `get_usage` e anotar o `resetsAt` do Fable. Depois de clicar: ler de novo. Se o horário passar a ser 7 dias após o clique, o ciclo mudou e a reinicialização de 15/11 08h deixou de existir; seguir o calendário só com a barra nova. Se ficou em 15/11 08h, ganhou uma terceira barra.
- Nunca depois de 16/11: a promoção do Fable 5.2 acaba nesse dia, então não sobra janela para gastar.
- Efeito no calendário: o Fable nunca fica parado esperando barra; P4 e P5 sobem um dia se a redefinição vier cedo.

## 10.6 Ajuste de 10/11: P1 (motor de cinema) deixa de ser prioridade
William: gosta, mas não é prioridade. P1 vira a última, só com barra que sobrar (ou na barra nova de 15/11).
Nova ordem: **P2 → P3 → P4 → P5 → P1.** Onde roda:
- **Aqui (este PC), sem o PC da fábrica:** análise, código, simulação, backtest, bateria do Uiu, auditor em Python sobre os dados exportados (`GMS/IA/dados`, `Producao_GMS_x_MB51/dados`, `Dados_Historicos`, `dados_diarios.json`) e edição dos arquivos do modelo (PBIP/TMDL) e das telas (`Telas/`).
- **Só no PC da fábrica:** abrir o Power BI Desktop com o modelo vivo para validar DAX contra o dia conferido, atualizar/publicar o relatório, e pegar export novo do SAP (MB51). Nada disso é pré-requisito para o Fable começar.
- **Depende do login, não do PC:** SharePoint, Copilot Studio e Power Automate pelo navegador do app, `pac`, Factbird. Confirmar no B1 se este PC está logado.
