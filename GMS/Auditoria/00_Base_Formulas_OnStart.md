# Auditoria GMS — 00 · Base (Formulas.txt + OnStart.txt + propriedades do App)

Escopo lido por inteiro: `Telas/Formulas.txt` (1213 linhas), `Telas/OnStart.txt` (174), `StartScreen`, `BackEnabled`,
`ConfirmExit*`, `MinScreen*`, `OnError`, `OnMessage`, `SizeBreakpoints`, `Theme`.
Nada em `Telas/` foi alterado. Os achados abaixo são propostas; cada linha cita arquivo e linha.
Legenda: **[DADO]** pode gravar/mostrar número errado · **[PERF]** custo de carga · **[LIMPEZA]** sem risco funcional · **[DECISÃO]** precisa do William.

## A. Risco de dado

1. **[DADO] `scr_Catenaria_1.txt:942-946` grava `Turno` com globais congeladas no OnStart.**
   `Now() >= gblTurno1_Inicio && Now() <= gblTurno1_Fim` usa `Today()+Time(...)` calculado quando o app abriu
   (`OnStart.txt:143-147`) e as fronteiras antigas 13:47 / 13:48 / 22:40 / 22:41 (as vigentes são 13:57 e 22:20).
   Tablet aberto desde o dia anterior: `Now()` passa de todos os limites e a tela grava `Turno = 3` o dia inteiro.
   Também há um buraco de 1 minuto (13:47→13:48) que cai em 3. Correção: `Turno: fx_TurnoEm(Now())` (o `Now()` está num
   `OnSelect`, onde é permitido) e remover os 5 `Set(gblTurno…)` do OnStart. A Catenária é o **único** uso deles.

2. **[DECISÃO] Fronteira do 2º para o 3º turno não fecha entre as UDFs.**
   `fx_Turno` (`Formulas.txt:122-127`): 2º turno vai até o minuto 1360 (22:40), 3º começa em 1361 (22:41).
   `fx_InicioTurnoMin(3)` (`:669`) = 1340 (22:20) e a `fx_GradeHoraHora` termina o 2º turno às 22:20 (soma 503 min).
   Os comentários (`:116`, `:558`) falam em 563 min e "hora extra até 23:20". Entre 22:20 e 22:40 um Patch grava
   `Turno = 2` enquanto a grade do Hora-Hora já considera 3º turno. O comentário em `:667` diz que as duas "têm que fechar".
   Pergunta única para o William: **o 3º turno começa às 22:20 ou às 22:41?** A resposta define qual das duas muda.

3. **[DADO] Motivos de parada não somam entre etapas.** `fx_MotivosParadaCobertura` (`:962-966`) afirma que os códigos são
   "OS MESMOS da fx_MotivosParada", mas `fx_MotivosParada` (`:618-652`) não tem prefixo numérico e os textos divergem:
   "Almoço" × "21 - Refeição", "Falta de Carretel" × "6 - Falta de Carretel", "Análise/Problema no tubo" × "31 - Problema no tubo".
   Se o BI não normaliza, o Pareto separa em duas barras o que é o mesmo motivo. Confirmar como o BI trata antes de mexer.

4. **[DADO] `OnStart.txt:47-48`: `FM0480` e bitola 8 duplicada.** Todos os outros PNs seguem `FM00xxx` (5 dígitos); este tem 4.
   A bitola 8 aparece duas vezes (`FM0480` e `FM00500`). `ColTabelaBitolas` é usada por `scr_mandril_1` (9 referências).
   Provável `FM00480`. Confirmar com a planilha de PN.

5. **[DADO] `fx_VelocidadeFallbackSpiral` (`:793-794`):** `EC415-16 = 276` foge da progressão das outras bitolas
   (216, 240, 288, 354, 456). Pode ser real; conferir.

## B. Performance

6. **[PERF] `fx_VelocidadeTeorica` (`Formulas.txt:768-777`) lê `DM_ENGRENAGENS` dentro de uma UDF.** Isso quebra duas regras do
   próprio cabeçalho (UDF não lê fonte, `:13` · só a §10 toca fonte, `:4`). O `LookUp` aplica `fx_NormCodigo` nos dois lados
   da comparação, então não delega e varre a tabela inteira a cada chamada; se for chamada por linha de galeria, é N+1.
   Proposta: carregar uma coleção com a chave já normalizada, uma vez, e a UDF receber essa tabela. Medir no Monitor antes e depois.

7. **[PERF] `OnStart.txt:172-174` carrega 3 coleções que nenhuma tela usa** (`colSup_OPs`, `colSup_Refugo`, `colSup_HoraHora`).
   Duas delas filtram com `DateValue(Created, "en-US") >= Today()`, que não é delegável; `TiposErros` já tem ~1.574 linhas
   (Mestre) e o limite de dados é 2.000. Além de custo morto em toda abertura, `Today()` fica congelado na abertura.

8. **[PERF] OnStart quase todo sequencial.** Só o 1º bloco usa `Concurrent` (`:8-39`). Os cadastros estáticos
   (`colMangueiras`, `colTrancadeiras`, `ColTabelaBitolas`) podem virar Named Formulas (avaliadas sob demanda), como a
   Microsoft recomenda. `colTrancadeiras` (11 nomes) duplica `fx_CelulasTrancagem` (as mesmas 11): duas verdades.

## C. Limpeza (grep nas 43 telas e arquivos de App: zero uso fora do OnStart)

Candidatos a remover do OnStart: `colMachines` (mock com OPs fictícias, `:149-162`), `colDefeitos`, `colMangueiraTrancadeira`
(70 linhas), `colSup_OPs`, `colSup_Refugo`, `colSup_HoraHora`, `varMapa`, `varQrMangueira`, `varQrTotal`, `varBarcodeSVG`,
`varConteudoHTML` (setada duas vezes: `:4` e `:164`), `gblTurno3_Inicio`. (`colDefeitosExt` da Finalização é outra coleção.)
A coleção `Turno` não tem prefixo `col` e tem o mesmo nome de colunas das listas; não conclui uso por grep, varrer antes de renomear.

Em `Formulas.txt`:
- **Cabeçalho corrompido** (`:1-9`): frases cortadas e coladas umas nas outras ("cabeçalho ainda dizia vfonte de dados…").
  Diz `v3.0.2`, mas contém as §15 (v3.0.3) e §16 (v3.0.4). `:886` cita `scr_HoraHora_CoberturaGMS_1`, que não existe no repositório.
- Sem uso nas 43 telas e arquivos de App: `fx_EspacoS/M/L`, `fx_BalizaTam`, `fx_ProcessoDeEtapa`, `fx_DataBR`,
  `fx_CorTipoEvento`, `fx_RecursoCanon`, `fx_PctRefugoProduzido`; `fx_EtapasLinha` e `fx_CorEtapa` só têm uso interno.
  Podem servir a uma tela que não está no repositório (Diário de Bordo, C25). **Não apagar sem confirmar.**
- `fx_EstadoVulca` (`:326`) recebe `agora` e não usa.
- Nenhuma tela usa `fx_` indefinido (checado).
- `App.StartScreen` está declarativo (bom). Depende só de `MapeamentoSetor`, sem variável do OnStart: sem risco de corrida.
- `OnError` e `OnMessage` vazios: sem tratamento global de erro.

## D. Oportunidades (plataforma 2026, sem Dataverse)

- UDF de **comportamento** (`Nome(...): Void = { ... }`) para o bloco repetido "Patch + IfError + Notify" das telas.
- `App.OnError` global para registrar falhas de escrita que hoje passam em silêncio.
- Cadastros em Named Formula; `DelayOutput` nas buscas; `Patch(fonte, ForAll(...))` nas gravações em lote.

## Próximo

Ordem proposta: `scr_Vulcanizacao_1` (referência do padrão), depois as telas pequenas e médias, por último as maiores
(`PainelCelula`, `Trancagem_3`, `mandril_1`, `tubo_1`).
