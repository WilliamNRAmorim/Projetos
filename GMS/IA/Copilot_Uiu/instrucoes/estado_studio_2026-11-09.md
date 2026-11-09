# Estado do Uiu no Copilot Studio (09/11/2026, fim da F0)

## Por que o conhecimento não está em "Knowledge"
A DLP "Allow default connectors - Danfoss Default" bloqueia os dois conectores de conhecimento:
- *Knowledge source with documents* (upload do PC): os 11 .md ficaram "Bloqueado".
- *Knowledge source with SharePoint and OneDrive*: os 11 .docx em `PackLists/Copilot_Uiu/conhecimento_docx` também ficaram "Bloqueado".
O William removeu os 22 itens. O conector SharePoint comum (o das listas) continua liberado.

## Caminho que funciona
- Lista SharePoint `Uiu_Conhecimento` (site OperationsGuaratingueta, Id 69ffd42a-1f85-452d-a4ee-cef4ec30b4fb).
  Colunas: `Title` (arquivo · seção), `Arquivo` (texto, indexado), `Secao`, `Ordem` (número), `Texto` (nota, texto puro).
  75 linhas = cada seção `##` dos 11 .md de `conhecimento/`. Conferido: o texto juntado por arquivo é igual ao .md de origem.
- Ferramenta do Uiu **Ler conhecimento do GMS** = SharePoint *Get items*: Site Address e List Name fixos, `Filter Query` preenchido pela IA (`Arquivo eq 'NOME.md'`), `Order By` = `Ordem`.
- Ferramenta **Ler documento do GMS** (SharePoint *Get file content using path*) ficou DESLIGADA: devolve o arquivo como binário e o Uiu não lê o texto.
- Instruções: seção CONHECIMENTO no fim (tabela assunto → arquivo), 5.524/8.000 caracteres. Não publicado: vale no painel de teste.

## Teste
Pergunta "apontamento às 22:30 de 15/10 caiu em qual turno?": o Uiu leu a lista e respondeu 2º turno, porque de 05/10 até a v3.0.15 o app virava o 3º às 22:41 (correto pelo 06_Roteiro_HoraHora).

## Como atualizar
1. Editar o .md em `GMS/IA/Copilot_Uiu/conhecimento/` (o 08 sai de `gerar_normas_diario.py`) e commitar.
2. Subir o .md novo para `PackLists/Copilot_Uiu/conhecimento/` no SharePoint.
3. Regravar as linhas daquele `Arquivo` na `Uiu_Conhecimento` (apagar as antigas para a lixeira e inserir as novas, uma por seção `##`), com o "sim" do William.

## Correção de 09/11 (tarde)
- Erro "ModelDisplayName excede 64 caracteres": 28 das ferramentas originais tinham nome de 65 a 81 caracteres. Todas renomeadas com a regra "Retrieve specific" → "Get", "Create new" → "Create", sem o sufixo "SharePoint table/table" (ex.: "Get production record from ficha_producao"). Conferido: nenhuma das 62 passa de 64. O erro saiu da lista de avisos.
- Avisos que sobram (4): nenhum canal configurado; ferramentas usam a credencial do autor; nenhuma avaliação rodada; **o agente usa recurso premium e precisa de licença premium para publicar**. Este último trava a publicação, e sem publicar não dá para pôr no Teams. O William ligou o Deep reasoning (premium) em 09/11.
- Tentativa de publicar (com "sim" do William, Deep reasoning ligado): o Studio não publicou. Botão Publish desabilitado e status "Not published". Na página Publish, todos os canais (Microsoft 365 e Teams, SharePoint e os de atendimento) mostram "Policy violation": "This channel isn't available because of your organization's data loss prevention policy" (admin 1234@danfoss.com). Ou seja, o bloqueio do Teams é a DLP "Allow default connectors - Danfoss Default", não a licença. Saída: TI liberar o conector de canal "Microsoft Teams + Microsoft 365" do Copilot Studio nessa política, ou mover o Uiu para um ambiente com política que permita.
