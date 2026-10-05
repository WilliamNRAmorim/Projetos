# Auditoria GMS — 09 · `scr_ConsultaOP_1` (v0.3.0 → v0.3.1)

Lida por inteiro (1.320 linhas, 105 controles → 110). QA idêntico ao baseline; parênteses balanceados.

## Bug da busca (relatado pelo William)
**Sintoma:** depois de pesquisar uma OP, só dava para pesquisar outra clicando no X.
**Causa:** a lista era atualizada só no `OnChange` do campo, que dispara ao confirmar a digitação, e cada busca trocava a coleção por inteiro.
**Correção:** a galeria `gal_FilaCOP` passou a ler o texto digitado direto (`Items` com `With`): vazio mostra as OPs em andamento, número filtra a OP, texto filtra o início da mangueira. Sem `OnChange` para a lista, não existe mais estado preso. O X só limpa o campo.

## Recentes de volta (pedido do William)
- Até 4 chips "RECENTES" logo abaixo do campo; tocar no chip busca a OP de novo.
- Entra na lista a OP tocada na fila ou digitada com número exato. Vale enquanto o app está aberto (o Power Apps no navegador não guarda coleção entre aberturas).
- Sem recentes, o espaço some: a lista continua começando no mesmo lugar de antes.
- Controles que mudaram de posição: `lbl_ContagemCOP` (Y 158 → 216 com recentes), `lbl_VazioBuscaCOP` (Y 220 → 280), `gal_FilaCOP` (Y 184 → 240, altura segue até o fim da tela). Sem recentes, ficam exatamente onde estavam.

## Outras correções
| # | Onde | Correção |
|---|---|---|
| 1 | Recarregar | Agora faz `Refresh(ficha_producao)` antes (antes só relia a cópia local) e avisa se a leitura falhar. |
| 2 | OnVisible | Leitura em `IfError` + aviso. |
| 3 | Itens da fila | Filhos passam o toque à galeria (`Select(Parent)`); o `ModernText` do status não aceita `OnSelect` (QA do projeto). |
| 4 | 8 quantidades das etapas | `fx_Ou(Text(x))` mostrava "1138,5" sem unidade; agora `fx_MetrosUn` ("—" quando vazio). |
| 5 | Refugo total | `Text(..., "#.##0,##")` depende do idioma do navegador; agora `fx_QtdBR`. |
| 6 | Inspeção e erros | Quantidade por `fx_MetrosUn`; diâmetros e concentricidade por `fx_MedidaBR` (3 casas, "—" se vazio). |
| 7 | Versão | 0.3.1. |

## Não aplicado
- **Atualização automática (120 s):** não faz sentido aqui. É tela de consulta, e recarregar a lista trocaria a OP que a pessoa está lendo.
- **Valores em milésimos antigos** (ex. Ø 412) aparecem como 412,000: é o dado gravado. Corrigir histórico é decisão à parte.
- A11Y (rodada final): caracteres invisíveis em "Ficha para impressão", `AccessibleLabel` nos botões das abas.
