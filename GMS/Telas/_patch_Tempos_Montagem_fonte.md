# Trocar a fonte Tempos (embutida no .msapp) pela lista Tempos_Montagem (29/10/2026)

Nenhuma tela foi editada. Só vale depois da carga inicial conferida (lista com 3.995 itens e segunda execução do fluxo com `novos` = 0 e `alterados` = 0).

## O que muda
Só uma linha nova no `App.Formulas`. As 7 fórmulas que usam `LookUp(Tempos, Material = ...).TempoMinPc` continuam iguais, em `scr_Montagem_HoraHora` (linhas 518, 774, 842, 856, 906, 1726) e `scr_selecaosetor_Montagem` (linha 102).
A coluna `Title` da lista aparece como **Material** (nome de exibição), então `Material` e `TempoMinPc` seguem valendo.

## Passos no Studio (você publica)
1. **Dados > Adicionar dados > `Tempos_Montagem`** (site Operations Guaratingueta).
2. **Dados**: remover a fonte estática `Tempos`. Sem isso o nome conflita com a fórmula do passo 3.
3. Em **App > Formulas**, acrescentar ao fim, depois de conferir que o último item termina com `;`:

```powerfx
// Tempos de montagem (min/peça) por PN. Fonte: lista Tempos_Montagem, mantida pelo fluxo GMS_Tempos_Sync.
// Mantém o nome Tempos para as fórmulas existentes não mudarem. Material = Title; indexado, LookUp delegável.
Tempos = Tempos_Montagem;
```

4. Esperar o Studio recalcular. Nenhuma fórmula pode ficar com erro vermelho.
5. Salvar, publicar e reabrir o app.

## Teste
1. Hora-Hora da Montagem: abrir um PN com tempo conhecido e conferir `TempoMinPc` igual à aba Tempos Montagem do PN prod time.xlsx.
2. Sem aviso de delegação (triângulo azul) nas linhas com `LookUp(Tempos, ...)`.
3. `scr_selecaosetor_Montagem`: o valor calculado a partir de `TempoMinPc` bate com o de antes da troca.
4. PN que não existe na lista: continua dando em branco (nas linhas com `Coalesce(..., 0)` dá 0, como já era).

## Reverter
Remover a linha `Tempos = Tempos_Montagem;`. Como a fonte estática foi removida, reimportar o `Tempos` do .msapp anterior (publicação anterior no histórico de versões do app).

## Observações
- Respeita a lição 4.4: nenhum `LookUp(Tempos, ...)` em propriedade de pintura (`Formulas.txt`, linha 1846).
- Se o Studio recusar `Tempos = Tempos_Montagem;`, o plano B é trocar `Tempos` por `Tempos_Montagem` nas 7 fórmulas (Ctrl+H do Studio não existe: editar uma a uma).
- `Formulas.txt` e as telas em `Telas/` só mudam depois que você publicar e confirmar (regra de manutenção: pasta igual ao publicado).
