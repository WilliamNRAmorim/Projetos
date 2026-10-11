# Plano para terminar: identificação de peças (para o Sonnet 5.5, esforço médio)

Escrito em 11/10/2026 pela sessão anterior (Opus, ultracode), que parou para economizar tokens. Tudo abaixo já está no disco, **sem commit**. Siga na ordem. Não precisa de subagente para nada disso: faça direto.

- Python deste PC: `C:/Users/willi/AppData/Local/Programs/Python/Python312/python.exe` (rode sempre com `-X utf8`).
- Pasta: `C:/Users/willi/Downloads/Projetos/Missão Manutenção - Longe de Casa` (abaixo, "a pasta").
- Contexto do que foi feito e dos erros: `01_MESTRES/MESTRE_EU.md`, linhas marcadas "Claude (pedido do William)". O William quer que tudo seja registrado lá: modificações, aprendizados e erros.

## O que já existe
- `02_MANUAIS`: `gerar_catalogo.py`, `CATALOGO_PECAS.xlsx`, `dados/catalogo.json` (3205 peças de 6 manuais), `dados/261_estruturado.csv`, `recortes/` (desenho com o balão marcado), `atlas/` (128 folhas), e as imagens do manual 09-2026.
- `05_VERIFICACAO`:
  - `gerar_verificacao.py`, `modelo_identificador.html` → `IDENTIFICADOR.html`, `VERIFICACAO_GERAL.xlsx`, `POR_CONFIANCA/SUB1..3`, `atualizar_status.py`, `.bat`, `CARTAO_DE_ESCALA_A4.pdf`, `gerar_cartao_escala.py`;
  - em `dados/`: `candidatos_ia.json` (rodada de IA dos 202 materiais, já paga, **não refazer**) e `respostas.json`.
- Respostas do aprendiz que precisam continuar valendo: NI-42 = 193-357, NI-101 = 57-332, NI-97 = 137-070 (todas candidata 1).
- Como se usa nos 3 PCs (decisão de 11/10): o registro oficial é o `VERIFICACAO_GERAL.xlsx` no OneDrive, com salvamento automático ligado. O `IDENTIFICADOR.html` é só uma lupa; o botão "Copiar para o Excel" (tecla X) cola as colunas amarelas.

## Correções da revisão que JÁ foram aplicadas, mas ainda NÃO testadas
O revisor (Opus) reprovou a 1ª versão. Já mudou no código:
1. `gerar_verificacao.py`:
   - O GERAL manda, inclusive célula apagada. CSV, SUB antigo e cópia de conflito do OneDrive (`VERIFICACAO_GERAL-*.xlsx`) só preenchem o que está vazio no GERAL e é diferente do retrato da última geração (`dados/retrato_geracao.json`).
   - Para tudo se o GERAL não puder ser lido.
   - Número de candidata que não existe mantém a resposta anterior.
   - Confere todos os arquivos de saída antes de gravar; grava em `.novo` e troca todos juntos no fim.
   - O backup tem segundos no nome e nunca sobrescreve outro.
   - Exige `--confirmo` se o GERAL existir.
   - Os SUB viraram "só consulta" (sem colunas amarelas).
   - O Leia-me dos xlsx mostra "Gerado em".
2. `modelo_identificador.html`:
   - "Sim" só sai quando a escolhida é a 1ª candidata, na aba Conferir códigos.
   - A cópia leva 4, 5 ou 6 colunas, para não apagar no Excel a observação ou as medidas que outro PC escreveu.
   - `esc(p.i)`.
   - Aviso quando o localStorage falha.
   - A importação não sobrescreve um rascunho mais novo.
   - Textos falam do Excel, não do CSV.
3. `GERAR_VERIFICACAO.bat` (pede para digitar SIM) e `ATUALIZAR_STATUS.bat`: os dois checam o `import openpyxl, PIL` e mostram o comando `pip install`.

Decisões A, B e C da revisão, tomadas pela opção recomendada (o William pode mudar):
- **A:** só regera com confirmação.
- **B:** apagar no GERAL vale.
- **C:** os SUB são só consulta.

## Passos que faltam
1. **Rodar e testar o gerador.** `cd 05_VERIFICACAO` e `python -X utf8 gerar_verificacao.py --confirmo`. Confira com openpyxl:
   - aba Verificar com 202 linhas, Conferir códigos com 28;
   - NI-42, NI-101 e NI-97 com "1" na coluna "APRENDIZ: qual candidata confere?";
   - os SUB sem coluna que comece com "APRENDIZ";
   - `dados/retrato_geracao.json` criado;
   - nenhum arquivo `.novo` sobrando;
   - JS do `IDENTIFICADOR.html` válido (`pip install esprima`; `esprima.parseScript` em cada `<script>` que não seja `application/json`).
2. **Testar as regras de junção numa cópia da pasta, nunca na original.** Copie `05_VERIFICACAO` para o scratchpad e simule:
   - (a) apagar a resposta do NI-42 no GERAL e rodar de novo: ela deve continuar apagada;
   - (b) um CSV `RESPOSTAS_IDENTIFICADOR_x.csv` com NI-10 = B6-414-2 (vazio no GERAL): deve entrar;
   - (c) o mesmo CSV com NI-42 = outro código, com o GERAL preenchido: não deve entrar;
   - (d) digitar "5" numa linha com 2 candidatas: a resposta anterior se mantém e aparece um AVISO.
3. **`atualizar_status.py`**: rodar e conferir que dá 3 conferidos de 230.
4. **`02_MANUAIS/gerar_catalogo.py`**: com `--extrair`, gravar em `dados/catalogo_extracao.json`, sem sobrescrever o `catalogo.json`. Item 11 da revisão: hoje ele apaga os recortes do json.
5. **Documentos:**
   - `01_MESTRES/PROTOCOLO_IDENTIFICACAO.md` (por volta da linha 24): trocar "exporte as respostas e rode ATUALIZAR_STATUS.bat" por "Copiar para o Excel" no GERAL compartilhado.
   - `LEIA-ME.md` da raiz (linha 7): o `BASE_MATERIAIS.xlsx` fica na raiz da pasta, não em `03_BASE_DE_DADOS`.
   - `05_VERIFICACAO/LEIA-ME.md`: explicar a regra nova (o GERAL manda, os outros só completam o vazio, apagar vale), os SUB só consulta, o SIM do `.bat` e o `pip install openpyxl pillow pymupdf`.
6. **Teste rápido no navegador** (opcional): o navegador interno não abre `file://`. Use um servidor local temporário (`python -m http.server 5193 --directory "<a pasta>"`) e abra `/05_VERIFICACAO/IDENTIFICADOR.html`. Confira NI-42 → tecla X copia `1 | 193-357 | ...` e o console fica sem erro. Não deixe configuração nova no `.claude/launch.json`.
7. **Revisão**: `revisor-leve` (Sonnet) só nas mudanças desta lista. Corrija o que ele apontar.
8. **Registrar** no `01_MESTRES/MESTRE_EU.md`:
   - na seção 5, Erros: a revisão reprovou a 1ª versão por 4 caminhos de perda de resposta, e o que foi feito;
   - no Registro de modificações: as correções.
9. **Commit por assunto e push na main** (autorização permanente do William no CLAUDE.md):
   - `.gitignore` (já tem `_backup/` da verificação);
   - `02_MANUAIS` (catálogo; cerca de 80 MB de imagens, que é esperado);
   - `05_VERIFICACAO` e documentos;
   - `01_MESTRES/MESTRE_EU.md`;
   - `.claude/orquestracao/registro.md` e `preferencias.md`.
   - Não commitar `05_VERIFICACAO/_backup/` nem nada do scratchpad.

## Custos até aqui (uso.ps1)
10/10: US$ 47,50 no dia (explorador Sonnet US$ 26,10, que inclui cerca de metade de rodada refeita por erro de cache; principal Opus US$ 15,72; executor US$ 2,76). 11/10 até a parada: cerca de US$ 7 (principal Opus e revisor).

## Depois (ideias, só com o "sim" do William)
- Pedir os manuais das trançadeiras têxteis (H5/HS, "boneca"): 21 materiais não são Magnatech.
- Fotografar de novo, em cima do cartão de escala, os 163 materiais abaixo de 40%.
- Ver no GRT os 16 códigos que já têm cadastro, antes de cadastrar.
