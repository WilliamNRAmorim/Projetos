# MESTRE – (seu nome)
> Somente você edita este arquivo. Consulte também `MESTRE_VITOR.md` e `CONSOLIDADO.md`.

## 1. Registro de modificações
| Data | Quem | Máquina/Local | O que foi feito | Por quê | Foto/Ref |
|---|---|---|---|---|---|
| 2026-10-10 | Claude (pedido do William) | PC de casa | Instalado Python 3.12 + openpyxl, pandas, pymupdf, pillow | Os scripts da pasta (atualizar_status, juntar_blocos) não rodavam neste PC | — |
| 2026-10-11 | Claude (pedido do William) | 05_VERIFICACAO, 02_MANUAIS | Correções da revisão aplicadas e testadas: o GERAL manda (inclusive célula apagada); CSV, SUB antigo e cópia de conflito do OneDrive só preenchem vazio e diferente do último retrato (dados/retrato_geracao.json); com resposta no GERAL, código/nome/parte final não mudam; para se o GERAL não abrir; grava tudo em .novo e troca junto; backup com segundos; exige --confirmo (o .bat pede SIM); SUB só consulta; HTML copia 4 a 6 colunas e só diz 'Sim' na 1ª candidata; gerar_status agora também troca o .novo; `gerar_catalogo.py --extrair` grava em catalogo_extracao.json (não apaga os recortes); documentos atualizados | Primeira versão reprovada pelo revisor (Opus) por 4 caminhos de perda de resposta | 05_VERIFICACAO/LEIA-ME.md |
| 2026-10-11 | Claude (pedido do William) | 05_VERIFICACAO | Decisão: as peças não serão medidas. Removida do IDENTIFICADOR.html a aba 'Medi a peça' (e o campo Medidas anotadas e o 'O que medir'); LEIA-ME, protocolo e Leia-me do Excel atualizados; teste no navegador ok (NI-42, tecla X copia 1 / 193-357 / nome / parte). Colunas de medidas do Excel e o cartão de escala ficam, sem uso | Medição não faz parte do fluxo | IDENTIFICADOR.html |
| 2026-10-10 | Claude (pedido do William) | 02_MANUAIS | Início do catálogo visual único (gerar_catalogo.py): 6 manuais, medidas tiradas da descrição, tipo em PT, recorte do desenho com a peça circulada, atlas por tipo | Candidatas da verificação estavam fracas (nenhuma acima de 55%, 77 de 84 abaixo de 40%) e só em texto | Plano aprovado em 10/10 |
| 2026-10-11 | Claude (pedido do William) | 05_VERIFICACAO | Tiradas do Excel as colunas 'Medir para confirmar' e 'Medidas anotadas (mm)' (GERAL, SUB, status); o botão Copiar passou a 4 ou 5 colunas; CARTAO_DE_ESCALA_A4.pdf e gerar_cartao_escala.py apagados. Colunas amarelas agora: candidata, código, nome, parte, observação. Regenerado com --confirmo: respostas do aprendiz mantidas (NI-42, NI-97, NI-101); teste no navegador ok. Quem tiver o GERAL antigo aberto/copiado em outro PC deve fechar e esperar o OneDrive sincronizar | Peças não serão medidas | 05_VERIFICACAO |
| 2026-10-10 | Claude (pedido do William) | 05_VERIFICACAO | Lista de 202 materiais para nova rodada de identificação por IA (84 NI + 110 nome livre + 8 código fora dos manuais), em 174 lotes | Os de nome livre também ficam sem código de manual para o cadastro | — |
| 2026-10-10 | Claude (pedido do William) | 02_MANUAIS | Catálogo pronto: CATALOGO_PECAS.xlsx (com Øint/Øext/Comp em mm para filtrar com o paquímetro), dados/catalogo.json (3205 ocorrências em 6 manuais), recortes/ (desenho com balão e ponta da linha de chamada em vermelho), atlas/ (128 folhas por tipo), manual 09-2026 em imagens | Balão achado em 85,5% das peças dos manuais com texto; conferência de 24 recortes: 22 certos | gerar_catalogo.py |
| 2026-10-11 | Claude (pedido do William) | 05_VERIFICACAO | Rodada de IA concluída para os 202 materiais (identificação + verificação adversária onde a 1ª candidata tinha >= 25%): 8 com 70%+, 31 entre 40 e 69%, 20 com a 1ª candidata sustentada pelo verificador, 26 provavelmente fora dos manuais | Candidatas antigas eram fracas | dados/candidatos_ia.json |
| 2026-10-11 | Claude (pedido do William) | 05_VERIFICACAO | Novo: IDENTIFICADOR.html (lupa de identificação), VERIFICACAO_GERAL.xlsx com o desenho de cada candidata dentro da célula, POR_CONFIANCA refeito, STATUS por grupo e faixa, GERAR_VERIFICACAO.bat, CARTAO_DE_ESCALA_A4.pdf; juntar_blocos.py removido | Plano aprovado em 10/10 | LEIA-ME.md da pasta |
| 2026-10-11 | Claude (pedido do William) | 05_VERIFICACAO | Decisão: o Excel compartilhado (OneDrive, salvamento automático) é o registro oficial nos 3 PCs; o HTML é só lupa e tem o botão "Copiar para o Excel" (cola as 6 colunas amarelas de uma vez) | HTML aberto da pasta não consegue gravar num lugar comum sem servidor, e não há onde hospedar | Pergunta do William em 11/10 |
| 2026-10-10 | Claude (pedido do William) | 02_MANUAIS | Manual 261 (escaneado) estruturado em dados/261_estruturado.csv: 1649 linhas, 30 páginas de desenho, 40 códigos marcados como dúvida | Antes só existia o texto do OCR, embaralhado | Lido página a página pela imagem |

## 2. FAZER ✅
- (Claude, 10/10) Medir antes de decidir: Øint, Øext, comprimento, rosca, nº de dentes com paquímetro; a foto sozinha não dá tamanho.
- (Claude, 10/10) Fotografar a peça em cima de uma régua ou do cartão de escala, mais um close de qualquer gravação ou número.
- (Claude, 10/10) Peça com designação comercial (rolamento, retentor, elo de corrente): procurar pela designação antes de procurar pela foto.
- (Claude, 10/10) Antes de cadastrar, ver se o código já tem GRT.
- (Claude, 10/10) Pedir os manuais das trançadeiras têxteis (H5/HS, "boneca") para os 21 materiais que não são Magnatech.

## 3. NÃO FAZER ❌
- 

## 4. Aprendizados
| Data | Aprendizado | Contexto |
|---|---|---|
| 2026-10-10 | Foto sem referência de tamanho não dá medida; o que dá para usar é o que não depende de escala: proporção comprimento/diâmetro, Øint/Øext, nº de dentes, furos, rasgos, flange | Ex.: NI-36 (roda dentada) dá para contar os dentes, mas não medir o diâmetro |
| 2026-10-10 | Nos manuais com texto (20C, 24C, COMUM 2018 e 09-2026, RB2) o número do balão e a linha de chamada estão em vetor: dá para achar e circular a peça automaticamente | Testado na COMUM 09-2026 pág. 14, item 3 (B1-2378) |
| 2026-10-10 | O manual 261 é escaneado e o texto do OCR sai embaralhado (colunas fora de ordem); para estruturar, precisa ler a imagem da página | 261-EN_OCR_texto.txt |
| 2026-10-10 | O INDICE_PECAS.csv não tinha o 261 nem o manual COMUM 09-2026 | 1144 linhas, só 20C, 24C, COMUM 2018 e RB2 |
| 2026-10-10 | DESCOBERTA: 2 dos 8 "código não está nos manuais" ESTÃO nos manuais. B6-778-5 = LOCK,BOBBIN (COMUM p20 e RB2 p78); B6-359-2 BPI = DX BEARING STRIP, FOR TRAILING EDGE (RB2 p36). A base errou por causa de espaço e do sufixo BPI | BASE_MATERIAIS, aba Materiais |
| 2026-10-10 | DESCOBERTA: os outros 6 (B1004-74000, B2-90298-72, B6-1062-1, B6-367-2, B6-554-2, CTD-B6-1061) não aparecem em nenhum dos 6 manuais, nem no novo de 09-2026 | Precisa de outro manual ou de consulta à Magnatech |
| 2026-10-10 | DESCOBERTA: os 29 registros "BUSHING ADIPRENE C / F / R" somam 490 unidades em 29 caixas, mas são só 3 peças (C=150, F=182, R=158 un). Identificar 3 resolve 29 linhas | Nomes com erro de digitação (ADEPRINE, ADIPENE, ADRIPRENE) |
| 2026-10-10 | DESCOBERTA: os manuais quase não usam cor para molas; a única é 57-277 "SPRING, COMPRESSION, GR/BL 3/4 X 3/8 X 2" (RB2, Inner e Outer Carrier, p74 e p82). Hipótese: é a "MOLA VERDE/AZUL". Confirmar medindo (3/4" = 19 mm, 3/8" = 9,5 mm, 2" = 51 mm) | Não confirmado, só hipótese |
| 2026-10-10 | DESCOBERTA: 21 materiais parecem ser de trançadeira têxtil ("boneca", H5, HS, AM94, MAYER A29, MTEK-250-24A), não da Magnatech 225-II/RB2. Os 6 manuais não cobrem essas peças | Pedir o manual dessas máquinas aumenta muito a chance de identificar |
| 2026-10-10 | DESCOBERTA: 22 materiais são peças comerciais com designação padrão (rolamentos KOYO B-1616, INA SCH 1612 V, Torrington JH 1412 e HJ-324120, 627Z, IKO BA69Z, INA SCE69; retentor 20x47x7 Freudenberg; emenda de corrente ASA 40). Dá para identificar pela designação, sem foto, e achar o equivalente no manual (rolamentos 904-xxx) | Compra no mercado pela designação |
| 2026-10-10 | DESCOBERTA: 16 códigos de manual já têm código GRT (ex.: B1-2928 = GRT000045 Inner Lug Pad). Conferir antes de cadastrar, para não duplicar | Coluna "Já no GRT?" da verificação |

## 5. Erros cometidos
| Data | Erro | Consequência | Como evitar |
|---|---|---|---|
| 2026-10-10 | Respostas do aprendiz gravadas só no SUB2_MEDIA (NI-42, NI-101, NI-97 = candidata 1) e não no VERIFICACAO_GERAL | O atualizar_status lia só o GERAL: os 3 apareciam como "Pendente" e sumiriam se o GERAL fosse refeito | Ao refazer planilhas, juntar antes as respostas de todos os arquivos (GERAL, SUB, exportações) |
| 2026-10-10 | Nomes diferentes entre o pré-cadastro e as fotos (espaço duplo, "(1)", ponto no fim, "GRANDE" a mais) | 10 materiais pareciam sem foto; 6 tinham foto | Ligar foto ao material pela coluna "Pasta de fotos" e, na falta, por nome normalizado; tratar a lista de exceções |
| 2026-10-10 | Google Lens testado com a foto do ROTOR DO CARRIER H5 | Voltou placa de partida de moto e bomba de diesel: nada útil | Usar o Lens só para peça com marca/gravação legível; para peça Magnatech, comparar com o desenho do manual |
| 2026-10-10 | Primeira versão do catálogo gerava uma "página marcada" por peça (99 MB) e uma cópia da página do 261 para cada peça (48 MB) | Pasta pesada para o OneDrive e o git, sem ganho | A tela marca o balão por cima da página que já existe; o 261 usa um arquivo por página |
| 2026-10-10 | Peça pequena com linha de chamada compartilhada (parafusos 136-047 no 20C, 137-019 no 24C) | A ponta vermelha às vezes cai fora da peça; o balão está certo | Em parafuso e pino, confiar no número do balão, não na ponta |
| 2026-10-10 | "BEARING LOCK WASHER" (151-012) saiu com nome "Rolamento" | Nome PT errado no catálogo | Corrigido: arruela/porca de trava de rolamento têm prioridade sobre "rolamento" |
| 2026-10-10 | Rodada de IA disparada com 280 agentes de uma vez (identificar + verificar + ferramentas) | Bateu o limite de uso da conta no meio: 107 prontos, 173 caíram, inclusive o executor das ferramentas | Rodar em partes e verificar só onde vale (1ª candidata >= 25%); retomar pelo cache, que não refaz o que já terminou |
| 2026-10-10 | O que ficou abaixo de 40% na rodada nova não é falha da IA: sem escala, a foto quase nunca fecha a peça sozinha (das 125 primeiras, 6 com 70%+, 24 entre 40 e 69%) | Sem medir, a confirmação continua dependendo do aprendiz | Medir com paquímetro e usar o painel "Medi a peça" do Identificador |
| 2026-10-11 | Ao retomar a rodada de IA, o cache não reaproveitou as 107 identificações já prontas | Elas foram refeitas: cerca de 2 milhões de tokens a mais | Antes de retomar, testar com 1 agente se o cache bate; se não bater, mandar só os lotes que faltam |
| 2026-10-11 | Ao incluir o botão "Copiar para o Excel", os escapes \t e \n viraram TAB e quebra de linha de verdade dentro do código da tela | A tela pararia de funcionar | O teste de sintaxe (esprima) pegou antes de entregar; sempre validar o JS depois de mexer no modelo |
| 2026-10-11 | Resposta antiga do aprendiz guardava só o número da candidata, sem código | Ao copiar para o Excel, o código saía vazio | O botão completa código, nome e parte a partir da candidata escolhida |
| 2026-10-10 | juntar_blocos.py dependia das pastas BLOCO_xx (que não existem mais) e de um caminho do PC do trabalho (materiais.csv do GRT) | Não dava para refazer a verificação em outro PC | Caminhos relativos à pasta; arquivo externo opcional, com cópia local do que já se sabe |
| 2026-10-11 | A 1ª versão do gerador foi reprovada na revisão: 4 caminhos podiam apagar ou trocar respostas (célula apagada voltava de um CSV antigo, cópia do OneDrive sobrescrevia, número de candidata inexistente zerava a resposta, falha no meio deixava arquivos pela metade) | Perda silenciosa de resposta do aprendiz nos 3 PCs | Regra de junção nova (o GERAL manda), gravação em .novo com troca no fim, --confirmo e backup; simulado numa cópia: apagar vale, CSV só entra em vazio, número inválido avisa |
| 2026-10-11 | Na correção, `gerar_status` gravava o STATUS em .novo mas ninguém o trocava, e um CSV podia por código diferente da candidata já escolhida no GERAL | STATUS ficava velho com arquivo .novo sobrando; código final conflitante | Pego pelo teste (sobrou .novo; simulação com CSV conflitante); corrigido. Lição: testar a regra em cópia antes de dar por pronta |

## 6. Peças identificadas
| Data | Foto | Código B1-/BM- | Descrição (EN) | Nome (PT) | Conjunto | Manual/pág. | Confiança | Cadastrada? |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |

## 7. Peças pendentes / dúvidas
| Data | Foto | Onde estava | Medidas/marcações | Status |
|---|---|---|---|---|
| | | | | |
