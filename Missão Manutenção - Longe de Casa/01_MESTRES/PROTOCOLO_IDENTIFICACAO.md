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

## Sem medição
Decisão de 11/10: as peças não serão medidas. A identificação é por foto, gravações, formato e comparação com o desenho dos manuais no `05_VERIFICACAO\IDENTIFICADOR.html`; confirmou a candidata, use **Copiar para o Excel** (tecla X) e cole nas colunas amarelas do `VERIFICACAO_GERAL.xlsx` no OneDrive.

