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
