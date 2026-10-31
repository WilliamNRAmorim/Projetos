# IA da manufatura (grátis e local)

Responde perguntas em português sobre exports de Excel/CSV. Roda no seu PC (Ollama + DuckDB). Nada vai para a internet.

## Instalar (uma vez)
1. Instale o Ollama e baixe o modelo: `ollama pull qwen3:8b` (PC fraco: `qwen3:4b` e `set GMS_MODELO=qwen3:4b`).
2. `pip install duckdb pandas openpyxl`

## Usar
1. Crie a pasta `dados` aqui dentro e solte os `.xlsx`, `.xlsm` ou `.csv` (cada aba vira uma tabela).
2. `python gms_mapear.py dados` descobre colunas e ligações e escreve `dados/mapa_dados.md`.
   Escreva suas correções em "Notas do William" nesse arquivo: essa parte nunca é apagada.
3. `python gms_ia.py dados` e pergunte. Depois de cada resposta: `+` (certo), `- o certo era...` (errado) ou Enter.

## Treinar
`python gms_ia.py dados --treinar treino_exemplo.md` (blocos `P:` pergunta e `R:` resposta esperada).
No fim grava a linha do Placar na `memoria.md`.

## Limpar a memória
`python gms_ia.py --limpar` tira repetidos e pergunta, um a um, os fatos "(a conferir)".

## Arquivos
`memoria_modelo.md` (modelo vazio, vai ao git), `glossario.md` (regras da fábrica), `treino_exemplo.md`.
A `memoria.md` é criada na primeira vez a partir do modelo e guarda o que você aprovou. Ela, o `mapa_dados.md`,
a pasta `dados` e o cache ficam fora do git (`.gitignore`). Não coloque dados de produção nos `.md`.
Se a `memoria.md` estiver aberta em outro programa, a IA avisa e mostra a linha para você copiar à mão.
Cada consulta tem limite de 60 segundos e a IA só enxerga o cache (não abre outros arquivos do PC).
