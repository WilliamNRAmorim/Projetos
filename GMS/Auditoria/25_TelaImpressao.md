# Auditoria 25 — TelaImpressao (Packing List) refeita em A4 paisagem

Template do Studio ("Portrait print") recebido: tela 1123×794 + botão Print que some com `Screen.Printing`. 1123×794 px = A4 paisagem (297×210 mm a 96 dpi), mesma proporção da folha.

## Por que saía pequeno
`Print()` encaixa a TELA inteira na folha. A tela era 1366×768 (proporção 1,78; a folha é 1,41): o conteúdo era reduzido a 0,217 mm/px, ocupava só ~165 mm dos 210 mm de altura e sobrava faixa em branco. Agora 1 px = 0,2645 mm (20% maior) e a tela preenche a folha inteira.

## O que mudou
- Tela 1123×794; coluna esquerda (data, local, ID pallet, part-number, código de barras da mangueira, total e código de barras do total) em 500 px; lista de lances à direita em 559 px.
- Códigos de barras com 500 px (≈132 mm na folha, antes ≈122 mm): melhor para o leitor.
- Cores, bordas e fontes por token (zero RGBA, zero Color.<nome>); botão "Confirmar Impressão" trocado para Classic/Button@2.2.0 (o Button@0.0.45 era recusado pela QA). Botões sempre escondidos na impressão (`TelaImpressao.Printing`).
- Mesmos controles e mesmos nomes; a tabela de lances continua vindo de `varHTMLLances` (26 lances).

## Ao imprimir (diálogo do navegador)
Orientação **Paisagem**, margens **Nenhuma**, escala **100%** (ou "Ajustar à página"), cabeçalhos e rodapés **desligados**.

## Pendente
`scr_FichaImpressao` (ficha de consulta da OP) tem o mesmo problema de tamanho e ainda não foi refeita.
