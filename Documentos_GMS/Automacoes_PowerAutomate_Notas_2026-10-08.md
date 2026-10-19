# Automações Power Automate — notas da ausência (08/10/2026)

Ambiente: Default-097464b8-069c-453e-9254-c17ec707310d ("Personal Productivity"), conta do William, logada no navegador embutido do Claude.

## O que foi feito
- Nada foi criado, alterado ou salvo no Power Automate.
- Fluxos existentes (My flows): `GMS_PackListParaFicha` (instantâneo, 17 h), `GMS_Conferencia_Diaria` (agendado, 1 d), `Conceder Acesso GMS` (instantâneo, 3 meses), `Monitor Solda Mandril` (agendado, 3 meses).

## Bloqueios
- Os cliques de criação de fluxo ("New flow") foram negados duas vezes pelo controle de permissões do Claude Code (08/10): 1ª "configuração persistente", 2ª "ação não pedida em app conectado", mesmo depois da autorização do William no chat. Não contornado.
- Para continuar: liberar a ação de criar fluxos nas permissões da sessão (ou o William clicar em New flow > Scheduled cloud flow e eu monto os passos dali).

## Fila (ordem)
1. `GMS_AutoResfriamentoVulca` (MEL-240): spec pronta em `Documentos_GMS/MEL-240_Auto_Resfriamento_110min.md`. Recurrence 5 min; Get items em ficha_producao com filtro (processo Vulcanização, status Em processo, InicioResfriamento_Vulcanizacao nulo, data_hora_inicio_vulcanizacao <= utcNow-110 min); Update item gravando início + 110 min. NÃO criado.
2. Pallet dividido fase 2 (MEL-239): lista `Packing_Pallets` + `GMS_PackListParaFicha` gravando uma linha por impressão (`Packlists/docs/Plano_Pallet_Fase2.md`). NÃO feito.
3. Arquivamento RegistrosInspeção (MEL-199): depende da decisão do William (por quantos meses). NÃO feito.
4. MEL-237: ligar `GMS_PackListParaFicha` no app: mexe no Studio, só com "pode" do William.

## MEL-231: tirar o `Monitor Solda Mandril` do Power Automate
- A tela `scr_Monitor_Mandril` só LÊ a lista `Estado_Trancadeiras` (colunas usadas: ID, Title, Mangueira_Atual, Proxima_Mangueira, Velocidade, Bitola, Quantidade_m, Hora_Parada, Status = Manutencao/SemPlano). Recarrega a cada 30 s.
- O fluxo (agendado) lê, nesta ordem: Estado Trancadeiras, DM Velocidade, ficha producao; depois Normaliza Fichas, Filtra Trançadeira, Normaliza Velocidade, Initialize variable, e um loop "Por Maquina" com 11 ações (calcula e grava Hora_Parada/Quantidade_m por trançadeira).
- Lógica do loop AINDA NÃO LIDA (o Code view abriu mas o texto não veio na leitura). Próximo passo: abrir o fluxo > Edit > loop "Por Maquina" > Code view, e copiar as expressões.
- Proposta: calcular no app (UDF/named formula) a partir das mesmas fontes, como o Painel da Célula, e deixar `Estado_Trancadeiras` só como cadastro (Status manutenção). Só depois de validar com a tela, desligar o fluxo (desligar, não apagar).
- Sem alteração no app sem aprovação do William.

## Para validar depois
- [ ] Liberar criação de fluxos e criar `GMS_AutoResfriamentoVulca`.
- [ ] Ler a lógica do loop "Por Maquina" e escrever a fórmula equivalente.
- [ ] Decisão do William: meses de arquivamento (MEL-199).
