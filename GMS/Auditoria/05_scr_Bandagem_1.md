# Auditoria GMS — 05 · `scr_Bandagem_1` (v0.3.0 → v0.3.1)

Lida por inteiro (2.696 linhas, 154 controles). QA do projeto idêntico ao baseline (o único FALHOU, `img_FitaTransferBand.ImagePosition`, já existia).
Nenhum controle existente mudou de X/Y/Width/Height; 7 controles novos e 2 trocados.

## Aplicado
| # | Onde | Mudança |
|---|---|---|
| 1 | tela | `tmr_AutoRefreshBand`: atualiza a fila a cada 120 s, só com o operador parado (sem gravar e sem modal) — NORMA MEL-202 |
| 2 | metragem | A trava de metragem ≤ 0 já existia; agora é `fx_MetragemOk` e a leitura do campo passa de `Value()` para `fx_Num` (12 pontos): aceita vírgula e ponto e não quebra com texto |
| 3 | margem | Balanço e saldo só ficam vermelhos acima da margem (`fx_MetragemSubiu`, 10%); novo `lbl_AlertaMargemBand` explica ("passa 18% da recebida… margem aceita: 10%"). **Só avisa, não bloqueia** |
| 4 | delineamento | O **filme UHMWPE** não era conferido: novo `lbl_AlertaFilmeBand` + borda âmbar em `inp_FilmeBand` quando a mangueira leva filme e o código está vazio ou diferente do Delineamento. Aviso, não bloqueia (a fita continua bloqueando, como já era) |
| 5 | início | Não inicia a Bandagem de OP sem metragem recebida da Cobertura (a que está na fila hoje tem 660 m) |
| 6 | editar OP | Mangueira passa a ser lista (`colMangueiras`) com "OUTRA (amostra ou nova)", como na Vulcanização |
| 7 | ícone | `ico_SetupLateralBand` (Classic, olho) → `img_SetupLateralBand` com o Lucide `drafting-compass`, igual ao `pen-line` do botão ao lado |
| 8 | dado | Um instante só (`_agora`) com `fx_TurnoEm`/`fx_DataRefEm` (11 pontos); fita e filme gravados com `Trim` |
| 9 | tela | 6 labels de metragem por `fx_MetrosUn` ("—" em vez de "0 m"); fontes Arial/Segoe UI por `fx_FonteFamilia`; chip Total por token |

## Não aplicado
1. **Fita é bloqueio, filme é aviso.** A fita (código) bloqueia o envio se difere do Delineamento; mantive, porque é como já operava.
   O William pediu "aviso de tudo": se quiser a fita também só como aviso, é uma linha.
2. **Ícones Classic** (`Icon.ArrowLeft`, `Icon.Reload`, `Icon.View`, `Icon.CheckBadge`, etc.) estão datados em todas as telas. Só troquei o que tem
   Lucide já importado como mídia e não depende de cor. Os outros precisam de SVG com cor fixa (a imagem não aceita `Color`).
3. `Cód_Fita_Bandagem` obrigatória mesmo quando a mangueira não leva fita (`"-"` no Delineamento): o operador precisa digitar "-". Confirmar se é intencional.
4. Nomes de coluna com espaço inicial (`' Qtd_Turno2_Bandagem'`, `' Qtd_Turno3_Bandagem'`) vêm da lista; funcionam, mas são frágeis.
5. "MENU LATERAL" e os caracteres invisíveis nos botões laterais: mesma observação da Vulcanização (rodada de acessibilidade).
