# Prompt: apresentação de defesa do TCC (GMS)

> Para colar numa sessão nova (Fable 5.2, esforço extra), aberta na raiz `C:\Users\willi\Downloads\Projetos`.

---

Você é o diretor artístico e o roteirista da apresentação de defesa do meu TCC. Quero a melhor apresentação que eu já fiz: 20 minutos, cara de abertura de filme, mas que uma banca de engenharia respeite. Ela não pode ficar só no acadêmico: tem que mostrar o GMS funcionando na fábrica.

As ideias que eu dou abaixo são exemplos. Pode trocar, cortar ou inventar coisa que eu não pedi, desde que você explique por quê.

## 1. O que é o GMS (leia antes de criar)
Fonte oficial: o próprio TCC. Leia nesta ordem:
1. `GMS/TCC_resumo.md`: tese, linha do tempo, regras de conteúdo público.
2. `TCC/Fase2/TCC_GMS_Fase2.md`: o texto final (resultados, MESA-11, Forest City na seção 4.9, limitações).
3. `TCC/Fase2/figuras/`: as figuras do TCC (arquitetura, linha do tempo, BI, navegação). Pode redesenhar todas no estilo da apresentação.
4. `GMS/GMS_Indice.md` e `GMS/GMS_Mestre.md`: o que o GMS virou depois do texto (painéis, Hora-Hora, OEE, conferência com o SAP, simulador, assistente Uiu etc.).
5. A logo: `Conteudo_Bit/Marca/logo_gms_escuro.svg` e `logo_gms_claro.svg` (o carretel em arcos coloridos com "GMS"). Ela é a protagonista visual: dá para animar os arcos se montando como um carretel girando.

Tese, que deve ser a frase que a banca leva para casa: **"Não criamos o dado. Zeramos o custo de acessá-lo."**

## 2. Regras que não se discutem
- **Conteúdo:** siga as regras de conteúdo público do `TCC_resumo.md`. Sem nome da empresa, do orientador ou de colegas, a menos que eu libere. Número da empresa só relativo (%, antes × depois), sem fato pontual (data de lote, contagem de um mês, valor em R$). O dado do papel (kg/ano) só com o meu aval. Nada de print com OP, nome de pessoa ou quantidade real visível: borre ou recrie a tela com dado fictício.
- **Autoria:** o GMS não é apresentado como "feito com IA". Fui eu que fiz, e escrevi partes à mão. A apresentação pode ser feita com IA, mas o sistema não.
- **Fidelidade:** a linha do tempo e cada ponta do GMS saem dos arquivos do repositório. Não invente módulo, data nem resultado. Se faltar informação, pergunte.
- **Sem fonte externa paga.** Imagem, ícone, modelo 3D, fonte e música: licença aberta (CC0, CC-BY com crédito, Google Fonts, Poly Haven, Sketchfab CC, Pixabay, Freesound CC0), ou gerado no Gemini ou no ChatGPT Plus, que eu tenho. Guarde a lista de créditos num slide final ou nas notas.
- **Time do repositório:** siga o `CLAUDE.md`. Toda imagem, áudio e vídeo passa pelo `produtor-de-artes`. Plano aprovado antes de construir. Commit e push na main ao fim de cada etapa.

## 3. O que eu imaginei (sugestões, não regras)
- **Abertura de cinema:** a ficha verde de papel em close, a câmera se aproxima e a ficha se rasga, ou se desfaz em partículas que viram dados e montam a logo do GMS.
- **Mangueira 3D como fio condutor:** somos mangueira hidráulica de alta pressão e conjuntos montados. Uma mangueira trançada (com camadas de arame, borracha e o terminal crimpado) pode atravessar os slides como a linha do tempo, ou se abrir num corte que mostra as camadas, cada uma sendo uma camada do sistema (coleta → dados → orquestração → análise).
- **A expansão em rede:** o GMS no centro, como um núcleo, e as pontas acendendo uma a uma: **Manufatura** (células, trançagem, montagem, painéis na TV), **Qualidade** (refugo, inspeção, rastreabilidade), **Planejamento** (OP, simulador de headcount × demanda), **Logística** (packing list, conferência com o SAP), **Engenharia** (setup, parada, OEE, dados para decisão). Confira nos arquivos o que realmente existe em cada ponta e separe o que **já existe** do que **pode existir** (o mapa do futuro).
- **Relatórios:** uma parede ou um carrossel 3D com os relatórios de produção que existem hoje e os que o dado já permite criar.
- **Forest City (Carolina do Norte, EUA):** o clímax prático. O sistema que nasceu numa célula vai ser replicado em outra planta, em outro país. Um globo ou um arco de voo de Guaratinguetá até Forest City.
- **Demonstração ao vivo no tablet:** vou mostrar o GMS rodando em tempo real no tablet, para provar que ele não depende de PC ou notebook. A apresentação precisa preparar esse momento (um slide de "agora, ao vivo") e ter um plano B: um vídeo curto gravado da mesma demonstração, caso a rede ou o espelhamento falhe.

## 4. Formato e técnica
Quero um **PowerPoint (.pptx)**, porque é o que vai rodar na defesa. O PowerPoint do Microsoft 365 está instalado nesta máquina (`POWERPNT.EXE`, versão 16.0.20527), então você pode automatizar pelo COM do Windows (PowerShell ou Python com `win32com`) e usar o que o python-pptx não faz.
Recomendo, mas a escolha é sua se tiver motivo:
- **Transição Transformar (Morph)** como linguagem principal: objetos com o mesmo nome (`!!nome`) atravessando os slides, câmera que "voa" pela linha do tempo, zoom de resumo para navegar entre as pontas.
- **Modelos 3D (.glb)** inseridos pelo PowerPoint (`Shapes.Add3DModel`) e girados com Morph: a mangueira, o terminal, o carretel da logo. Use modelo aberto ou modele em Blender por script.
- **Vídeos curtos embutidos** (MP4, 1080p, sem som ou com trilha baixa) para os momentos que o PowerPoint não faz sozinho, como a ficha rasgando, partículas e o voo até Forest City. Pode renderizar em Blender, three.js ou Remotion. Tudo offline, sem depender de internet na hora.
- Paleta escura e cinematográfica, com as cores dos arcos da logo como destaque. Uma família tipográfica forte, embutida no arquivo ou convertida em forma, para não quebrar em outro computador.
- 16:9, legível no projetor do fundo da sala: no máximo uma ideia por slide e texto grande. O que eu vou falar fica nas **notas do apresentador**.

Se você concluir que parte disso funciona melhor fora do PowerPoint (por exemplo, uma página web em three.js para um único momento), proponha e explique o ganho e o risco. O arquivo principal continua sendo .pptx.

## 5. Roteiro de 20 minutos (proponha o seu)
Um arco possível, só para dar a escala:
1. **0 a 2 min · O problema:** a ficha de papel, a cegueira operacional, a informação que chegava 1 a 2 dias depois.
2. **2 a 5 min · O método:** Gemba Walk nos três turnos, ciclo diário, low-code por restrição (não por preferência).
3. **5 a 9 min · A construção:** as 4 camadas, a linha do tempo de 9 meses (2 de desenvolvimento e 7 de implantação), a adoção como a barreira real.
4. **9 a 13 min · A expansão:** o núcleo e as pontas. Aqui entra a demonstração ao vivo no tablet (3 a 4 min).
5. **13 a 17 min · Resultados:** antes × depois, MESA-11, relatórios, Forest City.
6. **17 a 20 min · Limitações, futuro e fechamento** com a tese e a logo. Sobra tempo para a banca.

Cada slide com a fala nas notas e o tempo previsto. A soma tem que dar 20 min com a demonstração dentro.

## 6. Como trabalhar
1. **Pesquise antes:** procure referências de apresentação cinematográfica com Morph e 3D no PowerPoint, aberturas de keynote (Apple, Tesla) e motion design industrial. Me traga 5 a 8 referências com o que vamos aproveitar de cada uma.
2. **Perguntas, de uma vez só e só o que for decisão minha:** data da defesa, se posso mostrar o nome ou a logo da empresa, se posso usar fotos reais da fábrica (`GMS/Midia_fabrica`), como o tablet vai para o projetor (espelhamento, HDMI ou só na mão) e o modelo do tablet.
3. **Tratamento e storyboard:** conceito em um parágrafo, paleta, tipografia e um storyboard slide a slide (imagem de rascunho, transição, animação, fala e tempo). Com estimativa de custo e tempo de cada peça visual. **Espere eu aprovar.**
4. **Construa por blocos:** abertura, método, construção, expansão, resultados e fechamento. Depois de cada bloco, exporte os slides em imagem e grave um vídeo curto das transições para eu ver. No máximo 1 a 2 rodadas de ajuste por bloco.
5. **Verificação final:** abrir o .pptx do zero, rodar a apresentação inteira cronometrada, conferir que os vídeos e o 3D rodam offline, que as fontes não trocam e que nenhum dado confidencial aparece (passe slide por slide). Exporte também um **PDF** e um **MP4** da apresentação como reserva.

## 7. Entrega
Na pasta `TCC/Apresentacao/`:
- `GMS_Defesa.pptx` (o principal), `GMS_Defesa.pdf` e `GMS_Defesa.mp4` (reservas).
- `assets/`: modelos 3D, vídeos, imagens e fontes usados, com `CREDITOS.md`.
- `roteiro.md`: a fala completa e o tempo de cada slide, para eu ensaiar.
- `demo_tablet.md`: o passo a passo da demonstração ao vivo e o plano B.

Ao final: arquivos criados, como verificou, modelo usado em cada etapa e o que ficou pendente.
