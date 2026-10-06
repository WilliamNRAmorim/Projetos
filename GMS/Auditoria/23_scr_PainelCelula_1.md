# Auditoria 23 — scr_PainelCelula_1 (v0.10.2 → v0.10.3) + Formulas v3.0.9

Leitura linha a linha das 6.540 linhas. A tela é a mais elaborada do app e já está no padrão (carga local, sem chamada de rede por posto, velocidade em coleção diária, Hora-Hora por ID, ficha de consulta sem Patch). Geometria inalterada; QA: RGBA literal zerado, sem nova falha.

## Corrigido
- **TV mentindo "sincronizado":** se o Refresh de ficha, eventos, Hora-Hora ou DM falhasse (rede), o painel recalculava com dado velho e mostrava "Sincronizado às HH:MM" como se estivesse tudo certo. Agora a falha liga `varFalhaPnl`: o rodapé fica laranja com "Sem conexão com o servidor — dados das HH:MM · tentando de novo a cada 2 min". A autonomia de tubo continua descontando o relógio a partir do instante do cálculo (`varSincPnl`), e o aviso usa `varUltOkPnl` (última carga boa).
- **Cor solta:** `RGBA(242, 201, 76, 1)` (batelada incompleta) aparecia 50 vezes; virou o token `fx_CorBatelada` (Formulas v3.0.9, aditiva).
- Rótulo de versão estava em 7 pt (ilegível na TV); passou para o tamanho de apoio.

## Para publicar
Colar `Formulas.txt` v3.0.9 ANTES da tela (a tela usa `fx_CorBatelada`).

## Observações (não mexidas)
- Descarte de OP (MEL-222): o painel só lê "Em processo" e "Aguardando"; OP "Cancelado" some sozinha da fila e do andon.
- `Today()` em `InicioParada` fica (só hora cheia de relógio, sem risco).
- Os 60 botões de bolinha e a grade de bateladas são repetição por limite do Canvas (sem laço de controles); manter.
