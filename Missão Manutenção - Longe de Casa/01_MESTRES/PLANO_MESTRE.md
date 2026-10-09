# PLANO – Arquivos Mestre (Missão Manutenção – Longe de Casa)

## Objetivo
Registrar toda e qualquer modificação, o que fazer / não fazer, aprendizados e erros, e identificar peças desconhecidas a partir de fotos, usando os manuais desta pasta.

## Por que 2 mestres
A pasta é compartilhada (OneDrive). Dois editores no mesmo arquivo geram conflito/cópias duplicadas. Então:
- `MESTRE_VITOR.md` → só o Vitor escreve.
- `MESTRE_EU.md` → só você escreve (renomeie para seu nome).
- Quando pedirem ao Copilot, ele lê os dois e consolida em `CONSOLIDADO.md` (só o Copilot escreve nele). Ambos consultam o consolidado.

## Manuais na pasta (base de conhecimento)
| Arquivo | Conteúdo | Obs. |
|---|---|---|
| `225-II 20C Parts List.pdf` | Catálogo de peças trançadeira 225-II, 20 carriers (262-EN rev 10-2017) | texto legível |
| `262-EN - 225-II - 24C PARTS SECTION - 01-2025.pdf` | Peças 24 carriers | texto legível |
| `262-EN - 225-II - COMMON PARTS SECTION - 01-2018.pdf` | Peças comuns: rotores, shuttles, carriers | texto legível |
| `261-EN 225-II Parts List -06-09.pdf` | Lista de peças 225-II (94 pág.) | **escaneado, sem texto** – precisa OCR/leitura visual |
| `RB2 24C Parts List 2022.pdf` | Peças RB2 24C (89 pág.) | texto legível |
| `guia_preenchimento_cadastro_material.pdf` | Como preencher cadastro de material | ver regras abaixo |

Fabricante: Magnatech International (Robesonia, PA, EUA). Códigos no padrão `B1-xxxxx` / `BM-xxxx`.

## Fluxo de identificação por foto
1. Envie a foto (ideal: peça inteira, close de marcações/gravações, objeto de escala, local da máquina onde estava).
2. Informe: máquina (225-II 20C / 24C / RB2), conjunto/região, medidas.
3. Copilot busca nos manuais e responde: código `B1-`, descrição EN, conjunto pai, quantidade, nível de confiança e páginas de referência.
4. Se não houver certeza, responde "candidatos" e o que medir/fotografar a mais.
5. O resultado entra no mestre de quem pediu (seção Peças identificadas).

## Regras do cadastro de material (do guia)
- GRT: não mexer. NCM: em branco. Categoria: 1.1.1.
- Nome: português, conforme o fornecedor. Descrição: inglês, copiada do manual.
- Descrição Fornecedor: código do manual (ex.: `B1-90666-1`).
- Unidade: UN/kg/m… Estoque mínimo 0.00; máx. e preço em branco. Ativo marcado.

## Regras de edição
- Toda modificação vira uma linha no Registro de Modificações (data, quem, o quê, por quê).
- Nunca apagar entradas; corrigir criando nova linha referenciando a antiga.
- Fotos em subpasta `fotos\AAAA-MM-DD_descricao\`.

## Próximos passos
1. [ ] Renomear mestres com os nomes reais.
2. [x] OCR do `261-EN` → `261-EN_OCR_texto.txt` (qualidade boa, mas confira códigos críticos no PDF original).
3. [x] Índice de peças → `INDICE_PECAS.csv` (1144 linhas, 758 códigos; abre no Excel, separador `;`). Cobre 20C, 24C, COMUM e RB2. Ainda não inclui o 261 (só OCR em texto).
4. [ ] Enviar primeiras fotos.
