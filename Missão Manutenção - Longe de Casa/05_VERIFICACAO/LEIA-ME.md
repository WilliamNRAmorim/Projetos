# 05_VERIFICACAO – conferência do aprendiz

Aqui o aprendiz confere, com a peça na mão, o que a IA sugeriu para cada material. A pasta é usada em 3 PCs pelo OneDrive:

- **O registro oficial é um só: `VERIFICACAO_GERAL.xlsx`**, aberto no Excel com o salvamento automático ligado. Assim os 3 PCs veem as respostas em tempo real.
- **`IDENTIFICADOR.html` é a lupa para identificar**: foto grande, candidatas com o desenho do manual marcado, "Medi a peça" e catálogo. Abre com dois cliques, sem Python e sem internet, e pode estar aberto nos 3 PCs ao mesmo tempo. O que se marca nele fica só naquele PC; para registrar, use o botão **Copiar para o Excel**.
- Os arquivos de `POR_CONFIANCA\` são só para consulta e impressão (não têm colunas amarelas). Não preencha neles, para não ter duas versões.

## Arquivos
| Arquivo | Para quê |
|---|---|
| `IDENTIFICADOR.html` | Tela de conferência: lista, foto com zoom, candidatas com desenho do manual, "Medi a peça", catálogo, exportar/importar. |
| `VERIFICACAO_GERAL.xlsx` | Uma linha por material (aba Verificar, 202), aba Conferir códigos (28) e Leia-me. Colunas amarelas = preencher. |
| `POR_CONFIANCA\SUB1_ALTA_70-100.xlsx`, `SUB2_MEDIA_40-69.xlsx`, `SUB3_BAIXA_0-39.xlsx` | Mesma planilha dividida pela maior % de cada material. |
| `STATUS_VERIFICACAO.xlsx` | Resumo por grupo e por faixa (Total, Conferido, Nenhuma, Mais fotos, Pendente, Sem foto) e detalhe por material. |
| `CARTAO_DE_ESCALA_A4.pdf` | Cartão para imprimir em 100% e fotografar a peça em cima dele. |
| `GERAR_VERIFICACAO.bat` / `gerar_verificacao.py` | Refaz as planilhas, o `IDENTIFICADOR.html` e o status. |
| `ATUALIZAR_STATUS.bat` / `atualizar_status.py` | Só junta as respostas e refaz `STATUS_VERIFICACAO.xlsx`. |
| `gerar_cartao_escala.py` | Refaz o `CARTAO_DE_ESCALA_A4.pdf`. |
| `modelo_identificador.html` | Modelo da tela (o gerador injeta os dados nele). |
| `dados\` | `respostas.json` (respostas juntadas), candidatas da IA, legado, GRT conhecidos. |
| `_backup\` | Cópia das planilhas antes de cada geração. |

## Fluxo do aprendiz (3 PCs)
1. No `IDENTIFICADOR.html`, escolha o material na lista (setas, J/K) e olhe a foto (roda = zoom, arrastar, duplo clique volta, R gira).
2. **Medir**: com o paquímetro, meça Øint, Øext, comprimento, espessura, rosca e dentes. Na aba "Medi a peça" aparecem, no catálogo inteiro, as peças com medidas próximas.
3. **Comparar o desenho**: clique no recorte da candidata para abrir a página inteira do manual (círculos vermelhos = número da peça).
4. **Confirmar**: botão "Confere" (teclas 1 a 5), N = nenhuma confere, M = preciso de mais fotos. Ajuste código, nome, parte da máquina, observação e medidas se precisar.
5. **Registrar no Excel**: clique em **Copiar para o Excel** (tecla X). No `VERIFICACAO_GERAL.xlsx`, clique na **1ª coluna amarela** da linha do material e cole (Ctrl+V). As 6 colunas amarelas (candidata, código, nome, parte, observação, medidas) se preenchem de uma vez e os outros PCs veem na hora. A numeração das candidatas é a mesma na tela e na planilha.

Também dá para preencher as colunas amarelas direto no Excel, sem a tela.

"Exportar (cópia)" na tela baixa um CSV de segurança (`RESPOSTAS_IDENTIFICADOR_...csv`). Se for salvo nesta pasta, o `ATUALIZAR_STATUS.bat` também o lê. "Importar respostas" carrega esse CSV em outro PC.

## Regra de junção das respostas (ao regenerar)
- **O `VERIFICACAO_GERAL.xlsx` manda**, inclusive célula apagada: se você apagou uma resposta no GERAL, ela continua apagada.
- CSV `RESPOSTAS_IDENTIFICADOR*.csv`, SUB antigo e cópia de conflito do OneDrive (`VERIFICACAO_GERAL-*.xlsx`) só preenchem o que está **vazio** no GERAL e é diferente do que havia na última geração (`dados\retrato_geracao.json`). Se o material já tem candidata ou "Nenhuma/Mais fotos" no GERAL, código, nome e parte final não mudam.
- Número de candidata que não existe na linha (ex.: 5 numa linha com 2) mantém a resposta anterior e mostra um AVISO.
- Se o GERAL não puder ser lido, o gerador para sem alterar nada.

## Como o status é calculado
Conferido = código final preenchido OU candidata escolhida com código. Nenhuma e Mais fotos vêm da marcação. Vale a regra de junção acima.

## Como regenerar
Dois cliques em `GERAR_VERIFICACAO.bat` e digite **SIM** quando ele pedir (ou `python -X utf8 gerar_verificacao.py --confirmo`; sem `--confirmo` e com o GERAL existente, o script não roda). Antes de sobrescrever, as respostas são juntadas e as planilhas antigas vão para `_backup\` (nome com data e hora, nunca sobrescreve outro backup). Todos os arquivos novos são gravados à parte e trocados juntos no fim. Se a análise nova da IA existir em `dados\candidatos_ia.json`, ela é usada. Rode só com o `VERIFICACAO_GERAL.xlsx` fechado nos 3 PCs (o gerador reescreve o arquivo; as respostas são guardadas antes). Se der erro de arquivo aberto, feche o Excel. Os `.bat` precisam de `pip install openpyxl pillow pymupdf` (mostram o comando se faltar).

As % são estimativas por foto, não confirmação. Só vale como definitivo o que o aprendiz conferir.
