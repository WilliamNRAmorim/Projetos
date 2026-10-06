# Auditoria 16 — scr_Catenaria_1 (sem rótulo de versão; 1.356 → 1.432 linhas)

Tela herdada do primeiro modelo (formulário com cartões, cores fixas). Leitura linha a linha. Geometria inalterada; QA: zero RGBA literal, zero Color.<nome>, ACHOU de Now() zerado, sem nova falha.

## Padronização de números (pedido do William)
Tudo que o operador digita vira UM formato antes de gravar: ponto ou vírgula são aceitos na digitação, a lista recebe sempre ponto decimal com 2 a 4 casas ("0.30", "88.90").
- Diâmetro espec. (pol): `fx_DiametroPol` (aceita milésimo digitado, "300" = 0.300).
- Diâmetro espec./atual (mm) e tensão: `fx_NumMedida`.
- Nº de fios: `fx_Num`, inteiro > 0.
- Máquina e E-Number: `Trim` + `Upper`. Observação: `Trim`.
- Inválido (texto, vazio, "1,2,3") bloqueia o Registrar.

## Corrigido
- **Lixeira** apagava o apontamento no primeiro toque, sem confirmar nem checar erro. Agora o 1º toque arma (ícone escurece e preenche, aviso na tela), o 2º exclui; checa `Errors` e usa o overlay.
- **Zebra da galeria** usava `Mod(Aprovado, 2)` (booleano): pintava por aprovado/reprovado. Agora `Mod(ID, 2)`.
- **Botão Registrar** não tinha DisplayMode (ficava sempre ativo) e o ícone de enviar por cima não clicava. Agora habilita só com tudo válido e o ícone aciona o botão.
- Um único `Now()` por gravação (Title e DataHora ficavam com instantes diferentes).
- Relógio sem `Now()` volátil (`ctxAgora` a cada 30 s); lista atualiza sozinha a cada 120 s; refresh com IfError.
- "Hoje" da hora na galeria sem `Today()`; contagem do título pela própria galeria.
- Cores, fontes e tamanhos migrados para os tokens (`fx_Cor*`, `fx_FonteFamilia`, `fx_Fonte*`).

## Mantido / pendente
- Colunas de diâmetro e tensão continuam Texto no SharePoint (mudar para Número exige criar coluna nova).
- Sem alerta automático de diâmetro atual × espec.: falta tolerância definida pela Engenharia.
- Formulário (cartões) mantido por ora; reescrever sem Form fica para a rodada de layout.
