# Auditoria GMS — 04 · `scr_selecaosetor_1` (menu de setores)

Lida por inteiro (1.086 linhas, 47 controles). QA do projeto idêntico ao baseline; nenhum X/Y/Width/Height mudou.

## Aplicado
- **Cards de etapa mostravam só uma OP.** `colEstadoEtapaMenu` pegava a primeira OP "Em processo" da etapa. Na Vulcanização podem estar
  até `fx_AutoclaveMax` (5) ao mesmo tempo. Agora a coleção guarda `Ativas` e o card diz "3 OPs em processo" / "Toque para ver as OPs"
  quando há mais de uma; com uma só, continua "OP 123" e a mangueira. (Trançagem, Mandril e Extr./Teste já são por posto e não mudam.)

## Já estava certo
Atualização automática a cada 120 s (`tmr_DadosMenu_1`; é de onde veio o padrão que virou NORMA, e aqui não precisa de trava de
"operador parado" porque o menu não tem modal nem campo), tokens `fx_` em cor/raio/fonte, cards por overlay com `OnSelect` no botão
transparente, `DisplayMode` por `varAcessoRestrito`, relógio por `ctxAgora`, leitura delegável por igualdade
(`status_processo = "Em processo"/"Aguardando"`), `CarreteisMandril` lido inteiro (é uma frota física fixa: Vazio, Enchendo, Cheio,
Em uso — não cresce).

## Não aplicado
1. `colExtAbertaMenu` só olha extrusões dos últimos 7 dias: uma extrusão aberta há mais tempo some do card "Extrusora Mandril" (e do alerta de
   "solda sem reserva"). Provavelmente aceitável; confirmar com a operação.
2. Toda a carga mora no `OnSelect` de um botão invisível de 1×1 px em (1360, 756). É o padrão do app (Tubo, Trançagem e Mandril fazem igual), mas
   entra na ordem de foco do teclado; ver na rodada de acessibilidade.
3. Rótulo de acessibilidade: 6 controles interativos sem `AccessibleLabel` (cards de etapa, de posto e botão voltar). Rodada final.
4. Estilo: `Radius = 100` literal no botão voltar (círculo) e `[$-pt-BR]#.##0` no estoque de mandril, enquanto o resto usa `fx_MetrosBR`. Sem erro.
5. Os ícones dos cards já são mídia do app com nomes do Lucide (`send`, `cylinder`, `pipette`, `layers`, `disc`, `flame`, `undo-2`,
   `activity`, `hash`, `pen-line`): na pasta `GMS/Icones/lucide` bastará manter estes e os que entrarem depois.
