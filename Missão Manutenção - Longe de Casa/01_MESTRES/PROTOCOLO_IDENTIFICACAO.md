# Protocolo de identificação de peça por foto

## Regra de resposta
- **Certeza alta** (código/gravação legível na foto OU geometria + medida batem com um único item): responder 1 peça, dizendo a evidência.
- **Qualquer outro caso**: listar **até 5 candidatas**, ranqueadas, cada uma com: código, descrição EN, conjunto, máquina, manual/página, motivo da semelhança, o que diferencia das outras e grau de confiança (%).
- Fechar sempre com o que medir/fotografar para desempatar.

## Como a busca é feita
1. Ler marcações, gravações e plaquetas na foto.
2. Procurar código/palavras em `INDICE_PECAS.csv` e `261-EN_OCR_texto.txt`.
3. Comparar visualmente a foto com as páginas de desenho em `manuais_imagens\` (uma PNG por página de cada manual).
4. Cruzar medidas (rosca, diâmetro, comprimento) com a descrição (ex.: `SCREW,SOC HD CAP 3/8-16 X 3/4`).

## Foto ideal
Peça inteira + close das marcações, régua/paquímetro ao lado, fundo liso, e onde ela estava na máquina (20C, 24C ou RB2).

## Cadastro
Depois de confirmada, seguir `guia_preenchimento_cadastro_material.pdf`.

## Medir antes de decidir
- **Cartão de escala**: imprima `05_VERIFICACAO\CARTAO_DE_ESCALA_A4.pdf` em 100% (confira o quadrado de 50 mm) e fotografe a peça inteira, de cima, sobre o cartão. Faça também um close das gravações e uma foto de lado.
- **Medidas que não dependem de escala** (valem mesmo sem régua na foto): número de dentes, tipo de rosca (passo fino ou grosso), formato (sextavado, cilíndrico, cônico), furo passante ou cego, chanfros, rebaixos, gravações e relação entre diâmetros (ex.: Øext é cerca de 2x o Øint).
- **Paquímetro**: meça Øint, Øext, comprimento e espessura (mm ou polegadas) e anote junto com a rosca. Os manuais estão em polegadas; o Identificador mostra o esperado em mm e pol.
- **Identificador** (`05_VERIFICACAO\IDENTIFICADOR.html`): na aba "Medi a peça", digite as medidas e veja o ranking do catálogo inteiro (tolerância de 0,4 mm ou 3%, o maior; dentes ±1; rosca igual). Compare o desenho (página inteira do manual), confirme a candidata e use **Copiar para o Excel** (tecla X) para colar a resposta nas colunas amarelas do `VERIFICACAO_GERAL.xlsx` compartilhado no OneDrive.

