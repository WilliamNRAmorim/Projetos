# Tela `scr_ControleTrancagem_1`: guia de colagem (MEL-241)

Arquivo: `Telas/scr_ControleTrancagem_1.txt` (v0.1.0, 08/10/2026). Substitui a folha impressa AM-DM-02 REV. 5 (diâmetro por horário, X̄ e R).
**Status: escrita e passou na bateria `gms_qa_yaml.py` (48 controles, 0 falhas), mas NÃO foi aberta no Studio.** Os gráficos foram conferidos num protótipo SVG com os mesmos números, não no app.

## 1. Criar a lista SharePoint `Controle_Medicao` (antes de tudo)
Nomes internos sem acento nem espaço (a tela grava por esses nomes). Tipo entre parênteses.

| Coluna | Tipo | Observação |
|---|---|---|
| Title | Texto | Chave: `Máquina\|Mangueira\|Trama\|aaaammdd\|HH` |
| Processo | Texto | "Trançagem" (hoje); Catenária e outros depois |
| Maquina | Texto | TH01…TO04 |
| Mangueira | Texto | Mesmo texto de `NomeMangueira` |
| Trama | Texto | "1ª Trama" ou "2ª Trama" |
| DataHora | Data e hora | Horário da janela (00h, 02h…22h) |
| Turno | Número | 1, 2 ou 3 |
| Horario | Número | 0, 2, 4 … 22 |
| Amostra1…Amostra5 | Número (casas decimais: automático) | Em polegadas |
| LimInf, Nominal, LimSup | Número (automático) | Cópia do delineamento no ato |
| XBarra, Amplitude | Número (automático) | X̄ e R da hora |
| ForaFaixa | Sim/Não | Alguma amostra fora de LIE/LSE |
| Operador | Texto | |
| Observacao | Texto (várias linhas) | |

**Índices:** `DataHora` e `Maquina` (List Settings > Indexed columns). Volume: até 10 máquinas × 2 tramas × 12 horários = 240 linhas/dia.

## 2. Ordem de colagem no Studio (lição 9.5: fora de ordem dá erro em cascata)
1. Dados > Adicionar dados > SharePoint > `Controle_Medicao`.
2. Colar `Telas/scr_ControleTrancagem_1.txt` (menu da tela > Colar código). `OnStart` e `Formulas` não mudam: a tela usa só o que já existe (`fx_DiametroPol`, `fx_ForaDaFaixa`, `fx_MedidaBR`, `fx_NormCodigo`, `fx_NumSpec`, `fx_Turno`, `fx_DataRefEm` não é usada, `colMangueiras`, `DM_TRANÇAGEM`, `Colaboradores`).
3. Conferir erros do Studio. Pontos que podem pedir ajuste (não testei):
   - `Variant: Horizontal` da galeria: se o Studio recusar, trocar para `Vertical` e ajustar `Layout` na barra de fórmulas.
   - Se `Controle_Medicao` nomear colunas de outro jeito, ajustar o `Patch` no botão `btn_SalvarCTR`.
   - `cmb_OperadorCTR` lê `colColabCTR` montada com o mesmo bloco da Trançagem (`Colaboradores.Nome`).
4. Botão de entrada (a tela não é chamada por ninguém ainda): na `scr_HoraHora_Trancagem_2` (ou `scr_Trancagem_3`) acrescentar um botão com `OnSelect: =Navigate(scr_ControleTrancagem_1)`. Não alterei as telas publicadas.

## 3. Como a tela funciona
- Escolhe dia, máquina, mangueira e trama. O delineamento (`DM_TRANÇAGEM`) traz LIE, média, LSE e picks; a faixa fica no topo.
- Grade igual à folha: 12 horários (0h a 22h) × 5 amostras. Em pol, aceita "0,665" ou "665".
- Amostra fora do LIE/LSE fica vermelha; X̄ e R aparecem embaixo de cada horário; os dois gráficos (X̄ com LIE/média/LSE, e R) desenham as linhas de variação como na folha.
- **Salvar** grava uma linha por horário (cria ou atualiza), guarda LIE/média/LSE da hora, X̄, R e o operador. Esvaziar as 5 amostras de um horário já salvo e salvar apaga aquela linha.
- Trocar dia, máquina, mangueira ou trama fica bloqueado enquanto houver medida não salva (Salvar ou Descartar).

## 4. Fora desta versão
Tensão nas bonecas, nº de fios, ∅ do tubo, fios sobrepostos em 150 mm e picks medidos (todos da folha) ainda não entram; podem virar colunas da mesma lista depois.
