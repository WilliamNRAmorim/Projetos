# Treino por reforço da IA do GMS

Ajusta o modelo local (Qwen3 4B) com as suas perguntas aprovadas. O modelo escreve SQL, o SQL roda nos dados e a nota vem do resultado.

## Quando vale treinar
- Você tem pelo menos 100 perguntas validadas (SFT) e 30 com resposta conferível para avaliar (o `exportar_treino.py` avisa).
- O `qwen3:8b` com a memória já está acertando bem e travou num patamar (veja o Placar da `memoria.md`).
- Com poucos exemplos o placar oscila e o treino pode piorar. Nesse caso, junte mais perguntas antes.

## Passo a passo
1. **Exportar** (no PC, pasta `GMS/IA/treino`):
   `python exportar_treino.py ../dados meu_treino.md`
   Lê `IA/memoria.md` e os arquivos `P:`/`R:`. Linha opcional `SQL:` no bloco dá o SQL de referência (a resposta certa passa a ser o resultado dele).
   Gera `sft.jsonl`, `dpo.jsonl`, `grpo.jsonl`, `eval.jsonl` e `pacote_treino.zip` (inclui os dados do cache e o mapa).
   Cerca de 20% das perguntas vão para `eval.jsonl` e nunca entram no treino. Os ids ficam em `eval_ids.txt`: a lista só cresce, e pergunta que já esteve no eval nunca vai ao treino (apague o arquivo só se quiser recomeçar a avaliação do zero). Atenção: paráfrase de uma pergunta do eval com o mesmo SQL pode vazar para o treino; evite reescrever as mesmas perguntas.
2. **Treinar**: abra `treino_gms.ipynb` no Google Colab ou Kaggle com GPU T4, rode as células em ordem e suba o zip quando pedir.
   Ao fim ele baixa o `.gguf` e o `Modelfile`.
3. **Criar o modelo no Ollama** (arquivos na mesma pasta): `ollama create gms-qwen -f Modelfile`
4. **Avaliar** lado a lado: `python avaliar.py ../dados eval.jsonl --modelos qwen3:8b gms-qwen`
   Roda cada modelo em dois modos: sem memória (prompt do eval.jsonl) e com memória (a `memoria.md`, sem as linhas da própria pergunta). Grava uma linha de Placar por modo, dizendo qual.
5. **Usar** só se o `gms-qwen` ganhou: `set GMS_MODELO=gms-qwen` e `python gms_ia.py dados`.

## Cuidados
- O pacote leva os dados do cache para o Colab/Kaggle (serviço externo). Autorizado pelo William para dados de produção; apague o zip depois.
- O prompt do treino não inclui a memória (senão a resposta apareceria dentro do prompt). Em uso normal a memória continua entrando e ajuda.
- O gabarito fica congelado no momento da exportação (resultado do SQL de referência nos dados daquele dia). **Quando o cache dos dados mudar, exporte de novo**, senão o treino e a avaliação conferem contra números velhos.
- Resultado só vale se tiver a forma do gabarito (mesmo nº de linhas), usar uma tabela (`FROM`) e não vier vazio; gabarito vazio não entra no treino nem no eval.
- O Modelfile fixa `num_ctx 8192` e o `gms_ia.py` manda o mesmo `num_ctx` ao Ollama.
- Rode sempre a avaliação nas mesmas perguntas do `eval.jsonl`. Se mudar a base de perguntas, exporte de novo.
