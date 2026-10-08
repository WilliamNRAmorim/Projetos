# OP vira dropdown do plano: como aplicar (08/10/2026)

Os dois arquivos já estão prontos em `Telas/`, sem trechos soltos: copie o `.txt` inteiro.
- `Telas/scr_tubo_1.txt`
- `Telas/scr_ExtrusoraMandril_1.txt`

## Passos
1. No Studio, **Dados > Adicionar dados > `Plano_OPs`** (site Operations Guaratingueta). Sem isso dá "Name isn't valid".
2. Colar cada tela (YAML inteiro) no lugar da atual.
3. Salvar, publicar e reabrir o app nos tablets.
4. Tocar no ícone de atualizar de cada tela uma vez (carrega o plano).

## O que mudou
- `inp_OpTubo_1` virou `cmb_OpTubo_1` (mesma posição X369 Y583). `inp_OpExt` virou `cmb_OpExt` (X531 Y354). Lista só com OP do plano, não encerrada e fora de qualquer ficha. OP obrigatória na extrusora ao fechar.
- Atualizar (ícone na tubo, `btn_CarregarExt` na extrusora) agora lê `Plano_OPs` e as OPs em uso.
- Ao enviar no tubo: bloqueia OP fora do plano ou encerrada ("Toque em atualizar e escolha de novo"); a trava de OP duplicada continua.
- Salvar sem fechar na extrusora aceita OP vazia (rascunho). Fechar exige.

## Teste
1. Dropdown mostra só OP do tipo da tela; digitar parte do PN filtra.
2. Enviar com uma OP: some da lista das duas telas.
3. OP encerrada (TECO) e OP já usada não aparecem; 12345678 não é possível.
4. Plano mudou no Excel? Esperar o fluxo (até ~1 h, depende de salvarem o arquivo) e tocar em atualizar.

Obs.: a lista `ControleExtrusora_estrutura` já tem OP suja de antes (123, 2983346 com 7 dígitos, OPs repetidas). Não foi tocada.
