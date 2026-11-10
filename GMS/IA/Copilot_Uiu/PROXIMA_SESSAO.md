# Uiu: onde parou (09/11/2026) e o que executar a seguir

> **Atualização da retomada — planejamento v2.0, 09/11/2026.** Começar por [PLANO_EXECUCAO_GMS.md](PLANO_EXECUCAO_GMS.md), depois [gaps e decisões](planejamento/GAPS_E_DECISOES.md), [contratos](planejamento/CONTRATOS_E_METRICAS.md) e [execução e aceite](planejamento/EXECUCAO_E_ACEITE.md). Próximo pacote: E0, conferência do agente DPS e das versões de fonte; depois E1/E2, definição e prova de extração da TiposErros. O material abaixo é o histórico anterior, não uma ordem para executar diretamente a lista de agregados.
>
> Correções de planejamento: não excluir refugo só pela combinação OP/erro/quantidade/data; não usar Code Interpreter como garantia de leitura completa; não agregar todas as etapas apenas por Fim; não usar recurso dos eventos como máquina da etapa. A implantação das melhorias e os testes no tenant permanecem pendentes. O português no Teams deve ser conferido antes de republicar, pois o estado documentado pode ter mudado.

Para abrir a próxima sessão: "seguir `GMS/IA/Copilot_Uiu/PROXIMA_SESSAO.md`". Ler também `PLANO_UIU.md` e `instrucoes/estado_studio_2026-11-09.md` (histórico detalhado do dia).

## Estado em 09/11 à noite

### Onde o Uiu roda
- **Agente em uso:** ambiente **Copilot Studio - DPS - Non Prod**.
  - Ambiente: `8944b737-0def-e6f9-93c8-840d950e5e44` (`https://org4c52fdd5.crm4.dynamics.com/`).
  - Bot: `dd8888ce-de52-4f4a-be5f-1a2109a461cf` (schema `cra6eb_uiu_gms`, solução `Cra6eb0`).
  - Link do Studio: `https://copilotstudio.microsoft.com/environments/8944b737-0def-e6f9-93c8-840d950e5e44/bots/dd8888ce-de52-4f4a-be5f-1a2109a461cf/overview`
  - **Publicado** em 09/11 às 14:39, canal **Microsoft 365 e Teams** ligado, só para o William.
  - Link de instalação no Teams: `https://teams.microsoft.com/l/app/?titleId=T_dac66a92-143f-e29c-4341-5bcdf60f8c24`
- **Agente antigo** (cópia de segurança, não mexer): ambiente Default "Personal Productivity" (`097464b8-069c-453e-9254-c17ec707310d`), bot `c7f7f81f-d064-f111-a826-7ced8d968c44`. Lá a DLP "Allow default connectors - Danfoss Default" bloqueia todos os canais e o Knowledge (por arquivo e por SharePoint), por isso o Uiu mudou de ambiente.

### O que o Uiu do DPS tem
- **Ferramentas:** 32 de leitura do conector SharePoint, entre elas "Get items" genérica e **"Ler conhecimento do GMS"**. Esta lê a lista `Uiu_Conhecimento` filtrando `Arquivo eq 'NOME.md'`, ordem `Ordem`.
- **Conexão:** SharePoint com a conta do William, ligada nas duas referências de conexão.
- **Instruções:** `instrucoes/instrucoes_uiu_v2.md` mais a linha "IDIOMA" no topo (5.651/8.000).
- **Configurações:** orquestração generativa ligada; Deep reasoning ligado (premium); "Allow ungrounded responses" ligado.
- **Português:** "Response formatting" com a regra de responder sempre em pt-BR; saudação (Conversation Start) e Fallback traduzidos.
- **Code interpreter:** desligado.

### Conhecimento
- **Lista SharePoint `Uiu_Conhecimento`** (site OperationsGuaratingueta, Id `69ffd42a-1f85-452d-a4ee-cef4ec30b4fb`).
  - Uma linha por seção `##` dos 11 `.md` de `conhecimento/`: 75 linhas.
  - Colunas: Title, Arquivo (indexado), Secao, Ordem, Texto.
- **Os mesmos `.md`** estão em `PackLists/Copilot_Uiu/conhecimento/` no SharePoint.
- **Para atualizar:** editar o `.md` e commitar, subir o arquivo no SharePoint e regravar as linhas daquele Arquivo na lista (apagar só para a lixeira), com "sim".

### Testes que passaram (painel de teste do DPS)
- "OPs em processo na Trançadeira" devolveu 5 OPs reais, com máquina, turno e aviso de UTC.
- No Default, a pergunta de turno (22:30 de 15/10) foi respondida certo lendo a `Uiu_Conhecimento`.

## PENDENTE: primeiro passo de amanhã
1. **Republicar o Uiu do DPS**, porque as correções de português ainda não estão no Teams. Pede o "sim" do William na hora.
2. **Testar no Teams:** "oq vc pode fazer?" tem que vir em português, sem cair no "não entendi".

## A EXECUTAR: F2, Uiu responde qualquer pergunta, inclusive agregados (pedido do William em 09/11)
O William quer que o Uiu responda tudo sem mandar para o Power BI. Exemplo que falhou: "top 10 anual de refugo por mangueira/trançadeira". Plano proposto em 09/11; o William disse que amanhã é só executar. Confirmar com ele no começo, em uma linha.

1. **Lista `Uiu_Agregados`** (site OperationsGuaratingueta), calculada pela API REST no navegador do app, como foi feito com a `Uiu_Conhecimento`:
   - **Refugo:** por mês × mangueira × trançadeira × código de erro, em metros. Fonte: TiposErros (`_x0043_` = quantidade, `A` = código, `OP_ID`, `DataHoraRefugo`, `Tran_x00e7_adeira`), com a mangueira tirada da `ficha_producao` pela OP. **Tirar os grupos duplicados da TiposErros** (OP + erro + quantidade + data).
   - **Produção:** por dia × etapa × turno × máquina, em metros. Fonte: Eventos_Producao tipo Fim, sem Cancelado; Parcial de ficha cancelada = 0 m; Trançagem pela Hora-Hora (DECISÃO MEL-263).
   - **Paradas:** por dia × máquina × motivo, em minutos. Fonte: Hora-Hora `field_11`/`field_12`. **Pausa programada (Refeição, Set-up etc.) separada de parada; nunca somar parada com tempo excedido.**
   - Colunas sugeridas: Tipo (refugo/producao/parada), Periodo, Etapa, Maquina, Mangueira, Turno, Motivo, Valor, Unidade, AtualizadoEm.
   - Turno pela NORMA de 27/10 (MEL-250). O período de 05/10 a 27/10 tem o problema 22:20–22:40: marcar ou avisar.
2. **Revisão:** as regras de contagem (refugo, turno, parada) passam pelo `revisor` (Opus) antes de gravar. O tipo `revisor` não carregou nesta sessão; se falhar de novo, usar o `executor` com `model: opus` e as instruções de `.claude/agents/revisor.md`, como foi feito em 09/11.
3. **Gravar a lista:** com o "sim" do William, mostrando antes as primeiras linhas e os totais.
4. **No Uiu do DPS:**
   - adicionar a ferramenta **"Ler agregados do GMS"** (SharePoint Get items na `Uiu_Agregados`, Top Count alto, Filter Query pela IA);
   - trocar nas instruções o bloco "LIMITE IMPORTANTE" por "para totais, rankings e comparações use Ler agregados do GMS; para detalhe de uma OP use as listas".
5. **Code interpreter:** ligar em Settings → Generative AI → File processing capabilities (premium; precisa do "sim" na hora).
6. **Testar:** top 10 anual de refugo, mês de pico, produção por turno da semana, parada por máquina no mês. Depois republicar, com "sim".
7. **Depois:** fluxo diário no Power Automate (`GMS_Uiu_Agregados`) que recalcula a lista sozinho.

## Ferramentas e acessos (atenção ao trocar de PC)
- **Power Platform CLI:** `pac` 2.14.1 instalado só no PC da Danfoss (`dotnet tool install --global Microsoft.PowerApps.CLI.Tool --add-source https://api.nuget.org/v3/index.json`). O login (`pac auth create --deviceCode`) fica nesse PC. Em outro PC é preciso instalar e logar de novo.
- **Comandos de cópia de agente:** `pac copilot extract-template` e `pac copilot create`. O template não leva as instruções nem as conexões.
- **Navegador:** usar o navegador embutido do app (`mcp__Claude_Browser__*`). O SharePoint e o Studio já estão logados no PC da Danfoss; em casa, o William precisa entrar.
- **Limites do navegador:** o navegador do app não faz upload de arquivo do PC nem abre pop-up de consentimento. Upload é o William que faz no Edge, e conexão nova é ele que cria pelo clique dele.
- **Colar texto longo no Studio:** usar `ClipboardEvent('paste')` com `DataTransfer` (no editor de instruções e no Monaco do editor de código). Digitar texto longo de uma vez não funciona.

## Regras que continuam valendo
- Publicar, compartilhar, ligar recurso premium, criar lista e gravar no SharePoint: "sim" do William a cada ação.
- Apagar só para a lixeira.
- Turno, parada e setup passam pelo `revisor`.
