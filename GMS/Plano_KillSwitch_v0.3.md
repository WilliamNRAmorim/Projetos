# Plano: kill switch Composto v0.3.0, trava em todo lugar (MEL-274)

Status: AGUARDANDO APROVAÇÃO DO WILLIAM (19/11/2026)
Anterior: `Plano_KillSwitch.md` (v0.2.x, trava só no OnVisible)

## 1. Por que mudar
Teste de 19/11 às 10:37: o Flow respondeu `permitido=false`, a tela "Selecione o Setor" abriu vazia e,
minutos depois, encheu (13 OP em processo, 33 aguardando). O timer de 120 s (`OnTimerEnd = Select(btn_RecarregarMenu_1)`)
recarrega sem olhar a trava. A v0.2.1 só trava a abertura das telas.

Mapa do app real (export de 19/11, 36 telas):

| Ponto de entrada | Total | Com trava hoje |
|---|---|---|
| OnVisible das telas | 32 | 23 |
| OnTimerEnd (timers) | 50 | 0 |
| Ações (OnSelect, OnChange, OnCheck...) | 760 | 1 (OnStart) |
| …das quais gravam (Patch, SubmitForm, Remove, UpdateIf, Collect, Flow.Run) | 131 | 1 |
| …das quais navegam (Navigate) | 63 | 0 |
| Leitura direta de lista em propriedade de dado (Items, Text, Default..., Visible) | ~100 | 0 |

Telas sem nenhuma trava hoje: scr_ConsultaOP_1, scr_FichaTecnica_1, scr_HistoricoTurno_Mandril/Tubo,
scr_HoraHora_Mandril_2, scr_Monitor_Mandril, scr_PainelCelula_1, scr_PainelMontagem_1, scr_SelecaoGestao_1,
scr_FichaImpressao, Splash. **Muda uma decisão de 17/11**: painéis de TV e telas de leitura passam a ser travados também
("trava em tudo quanto é lado", pedido do William em 19/11).

## 2. Estrutura (6 camadas, uma variável)

```
Lista Composto (SharePoint, só o William edita)
   Ativo (Sim/Não) · DataBloqueio (06/01/2027 13:59)
        │
        ▼
Flow_Composto (Power Automate, conexão do William)
   permitido = Ativo E agora < DataBloqueio   (erro ou data vazia = bloqueado)
        │
        ▼
C1  App.OnStart ............ chama o Flow 1 vez e grava varCompostoPermitida (true/false)
C2  OnVisible  (32 telas) .. If(varCompostoPermitida, <original>)          [hoje 23 → 32]
C3  OnTimerEnd (50) ........ If(varCompostoPermitida, <original>)          [NOVO: fecha o furo de hoje]
C4  Toda ação  (760) ....... If(varCompostoPermitida, <original>)          [NOVO: botão não grava, não navega, não recarrega]
C5  Leitura direta (~100) .. If(varCompostoPermitida, <original>)          [NOVO: galeria/rótulo não consulta a lista]
C6  App.OnError ............ silencioso (Trace), sem mensagem              [igual]
```

Regras que valem para todas as camadas:
- Variável vazia (Flow ainda não respondeu) conta como bloqueado: `If(Blank, …)` não roda nada.
- Bloqueado = app abre, telas sem dado, botões não fazem nada, sem mensagem (decisão de 17/11).
- Liberar exige reabrir o app (a variável só é lida no OnStart). Sem timer de revalidação, como em 17/11.
- Splash: o timer que leva ao Menu também é travado (o app fica parado na Splash quando bloqueado).
  **Exceção opcional**: se você preferir que o app pelo menos chegue ao Menu, a Splash fica de fora.

## 3. Como fica o código

Ação (ex.: botão Salvar):
```
// antes
Patch(ficha_producao, gal.Selected, {...}); Navigate(scr_Mandril_1)
// depois
If(varCompostoPermitida,
    Patch(ficha_producao, gal.Selected, {...}); Navigate(scr_Mandril_1)
)
```
Timer de recarga (o furo de hoje):
```
OnTimerEnd: =If(varCompostoPermitida,
    Select(btn_RecarregarMenu_1)
)
```
Leitura direta (galeria):
```
Items: =If(varCompostoPermitida,
    Filter(Controle_Catenaria, DataHora >= locCorte_cat)
)
```
Bloqueado, devolve tabela vazia (mesmo tipo, a galeria não quebra).

Cuidado técnico: o original vai numa linha própria e o `)` em outra, porque uma fórmula que termina
em comentário `//` engoliria o parêntese se ficasse na mesma linha.

## 4. Passos
1. **Baixar o app atual** (`pac canvas download`): ele foi salvo hoje de novo, não uso o export das 10:21.
2. **Desempacotar** (`pac canvas unpack`) numa pasta de trabalho.
3. **Script `GMS/KillSwitch/trava_composto.py`** (executor, Sonnet): aplica C2 a C5 em todas as telas.
   É idempotente (pula o que já tem `varCompostoPermitida`) e gera `relatorio_trava.csv` com cada propriedade mudada (tela, controle, propriedade, antes, depois).
   Fica de fora: App.Formulas (fórmulas nomeadas só rodam quando alguém as usa, e quem usa já está travado),
   propriedades de aparência (Fill, X, Y, Color...), e o próprio Flow_Composto no OnStart.
4. **Empacotar** (`pac canvas pack`) → `Downloads/GMS_KillSwitch_v0.3.0.msapp`. Desempacotar de novo e contar:
   0 ponto de entrada sem trava, 0 erro novo no App Checker.
5. **Revisor (Opus)**: script, relatório e amostra do código (tipos do If sem senão, delegação dos Filter,
   comentários, fórmulas com `;`). Só sigo se ele aprovar.
6. **Você importa e testa** (roteiro abaixo). Publicar é com você.
7. **Atualizar `Telas/`** com o export do app novo (resolve a divergência de 17/11: Telas/ passa a ser cópia fiel).

## 5. Roteiro de teste (você)
Bloqueado (lista com data passada, ou Ativo = Não):
- [ ] abrir o app: Menu sem nada / Splash parada
- [ ] esperar 3 min na tela de setores: continua vazia (o furo de hoje)
- [ ] clicar em Salvar/Enviar numa tela de produção: nada grava (conferir a lista)
- [ ] Flow_Composto: 1 execução com permitido=false
Liberado (voltar para 06/01/2027 13:59, Ativo = Sim):
- [ ] reabrir o app: tudo carrega, timers atualizam, gravar uma ficha de teste funciona

## 6. Riscos
- Se a conexão do William cair ou o Flow falhar, o app inteiro para (igual hoje, decisão de 17/11), agora sem nenhuma brecha.
- Mudança em 760+ fórmulas: só por script e com relatório, nada à mão. Volta atrás = reimportar a v0.2.1 (`Downloads/GMS_KillSwitch.msapp`).
- `pac canvas pack` é Preview (funcionou em 17/11).
- Cada operador vai ver a janela "Allow" na 1ª abertura do app novo.
