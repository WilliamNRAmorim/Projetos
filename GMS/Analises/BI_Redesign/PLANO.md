# Redesign do GMS_Painel (Power BI): plano

Pedido do William em 12/11/2026: o painel tem cara de amador; ele quer layout de nível sênior. As informações continuam as mesmas: muda só a aparência e a navegação. Nenhuma medida de regra de negócio muda.

Protótipo da linguagem visual: `mockup_visao_geral.html` (nesta pasta).

## Diagnóstico do painel de hoje
- Faixa vermelha de 48 px no topo e duas fileiras de botões de navegação, o que ocupa ~90 px de altura em toda página.
- Cartão antigo (`card`) com borda colorida de 3 px. A cor de status pesa demais e a hierarquia fica fraca.
- Formatação escrita à mão em cada visual (cor, fonte, tamanho): ~226 visuais em 10 páginas. Contraria a B.6.1 do Mestre_BI (hardcode proibido) e impede mudar tudo de uma vez.
- Títulos, eixos, grade e legenda variam de página para página, e os filtros mudam de lugar.

## Linguagem visual nova
- **Menu lateral fixo** de 200 px em grafite (#1E1E1E): logo, seção MANGUEIRA (8 páginas) e MONTAGEM (2). A página atual fica marcada por uma barra vermelha de 3 px. Embaixo ficam a data de atualização e a fonte. Isso substitui a faixa vermelha, os botões mod_* e os sub_*.
- **Cabeçalho** em cada página: título de 22 px, subtítulo com o recorte (etapa, período, turno) e os filtros em lista suspensa no canto direito, sempre na mesma posição.
- **Cartões novos** (`cardVisual`): rótulo em caixa alta, valor de 30 px, linha de referência (meta ou base, com a variação e uma seta) e barra de destaque à esquerda com a cor de status. Cor sempre acompanhada de seta ou texto (B.6.4).
- **Gráficos**: título é a pergunta (B.6.2), subtítulo é a unidade e a ordenação, grade quase invisível, sem título de eixo, rótulo direto no dado. Real × meta em barras sobrepostas (meta larga em cinza claro atrás, real fina na frente).
- **Cores**: vermelho Danfoss #E2000F nas barras e cinza #3C3C3B na linha de meta, como o William preferiu em 11/11. As cores condicionais por medida (VG Cor Máquina, VG Aderência Cor etc.) continuam.
- **Tema único** `GMS_Tema` v2 com `visualStyles` completo: fonte Segoe UI, tamanhos, cartão, eixo, grade, borda, espaçamento, segmentação e botão. Os visuais perdem a formatação escrita à mão e herdam do tema.
- Canvas de 1280 × 720, grade de 8 px e espaço de 16 px entre blocos (B.6.3).

## Passos
1. **Cópia de trabalho**: `GMS/PowerBI/Painel_Redesign/` com cópia do `GMS_Painel.Report` e um `.pbip` que aponta para o mesmo modelo. A versão vigente não é tocada até o William aprovar.
2. **Tema v2**: reescrever `GMS_Tema.json` na cópia.
3. **Piloto na Visão Geral**: menu lateral, cabeçalho, 4 `cardVisual` e formatação limpa nos 3 gráficos. Mesmos campos, medidas e filtros. Se a linha de referência pedir texto novo (ex.: "▼ 4,2%"), ela vira medida de rótulo no `reportExtensions.json`, sem regra nova.
4. **William abre a cópia no Desktop e aprova o piloto** (ou pede ajuste).
5. **Levar às outras 9 páginas** com o mesmo esqueleto: script que troca só a formatação e a posição e mantém `query`, filtros e cores condicionais. Tela por tela, sem rodar o `gerar_relatorio.py` por cima.
6. **Conferência**: `revisor-leve` confere os JSON (campos e medidas idênticos aos da vigente; ESCALAR se tocar medida de regra). O William valida no Desktop.
7. **Troca**: a cópia vira o `GMS_Painel.Report`, `python gerar_relatorio.py --extrair-layout` atualiza o `layout_salvo.json`, entram as linhas no diário e se faz o commit. O William publica.

## Pontos de norma (para o William saber)
- B.6.1 do Mestre_BI manda série em azul e vermelho reservado. O painel já usa vermelho por escolha do William (11/11). O Mestre_BI não muda; a escolha entra no diário como DECISÃO.
- B.6.3 limita a 8 visuais por página. O menu lateral soma ~12 itens (botões e forma); só gráficos e cartões contam para o limite.

## Time
- Desenho e plano: chefe. Execução dos passos 1 a 5: `executor` (Sonnet), de preferência em sessão nova a partir deste plano. Conferência: `revisor-leve`.
