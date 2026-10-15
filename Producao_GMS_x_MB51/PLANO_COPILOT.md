# Plano para o GitHub Copilot (Sonnet 5.5): tratar divergência GMS x MB51 por OP

Este arquivo tem todo o contexto. Não precisa perguntar nada ao William antes de começar. Trabalhe na pasta `Producao_GMS_x_MB51/`.

## Objetivo
Tratar as divergências de metragem entre o GMS (apontamento do app) e a MB51 (SAP, movimentos 101/102), **OP por OP, da mais divergente para a menos**. Para cada OP divergente, achar OPs da **mesma mangueira (Material SAP)** que compensam a diferença, porque o erro típico é lance lançado na OP errada.

Exemplos da lógica (William):
- MB51 600 m e GMS 900 m: o GMS tem 300 m a mais. Procurar uma OP da mesma mangueira em que a MB51 tenha ~300 m a mais que o GMS, ou duas OPs com ~150 m a mais cada.
- MB51 550 m e GMS 500 m: o inverso. Procurar OP(s) da mesma mangueira em que o GMS tenha a mais o que falta.
- Resumindo: a divergência da OP tem sinal; a OP candidata precisa ter **sinal oposto**, e a soma das candidatas deve fechar a diferença.

## Arquivos
- `Conferencia_Lances_por_OP.xlsx` (gerado por `conferir_lances_por_op.py`). Abas usadas:
  - `Resumo por OP`: colunas OP, Mangueira no GMS, Material SAP (col. C), 1º lance GMS (F), Último lance GMS (G), GMS total (J), MB51 líquido (K), **Dif. MB51 − GMS (L)**, Situação (U).
  - `MB51 sem GMS`: OPs que só existem no SAP (OP, Material SAP, 1º/último lançamento, MB51 líquido). Contam como candidatas com diferença positiva.
  - `Lance em outra OP`: lances do GMS que a MB51 lançou em outra OP (prova direta de troca). Colunas: Material, OP do GMS, Lance, Data, Qtd, OP onde foi lançado.
  - `Linha a linha`: lance a lance, com Situação e observação "Provável lance lançado na OP X".
  - `Lances excluídos`: lances que o William decidiu ignorar (erro de digitação no GMS).
- `top_ops_compensacao.py`: script pronto que faz o ranking e a busca. Rodar de dentro da pasta: `python -I top_ops_compensacao.py`.
- `aliases_mangueira.csv`: nome GMS x Material SAP. Nunca zerar mangueira sem match; ligar pela OP.
- Fontes brutas: `mb51 (5).xlsx`, `dados/inspecao_14out.csv`, `dados/refugo_14out.csv`.

## Regras de negócio (não mudar)
1. Dif. = MB51 líquido − GMS total. Negativa = GMS tem a mais. Positiva = SAP tem a mais.
2. Ignorar a OP `0` (lances sem OP, não é OP real).
3. Ignorar OPs com 1º lance a partir de 13/10/2026: a MB51 ainda não recebeu (defasagem, não é divergência).
4. Candidata = mesma Material SAP, sinal de diferença oposto, atividade dentro de ±60 dias do 1º/último lance da OP. Combinações de 1, 2 ou 3 OPs; tolerância de sobra = máx(2 m, 0,5% da diferença). Preferir menos OPs e menor sobra.
5. Soma coincidente não basta: em mangueira com muitas OPs (ex.: GH781-12, GH781-4) sempre aparece combinação que fecha por acaso. Dar mais confiança quando houver **prova por lance** (aba `Lance em outra OP` apontando a OP candidata) ou datas próximas; marcar como "fraca" quando só houver a soma.
6. Divergência por mangueira = soma SAP − soma GMS; OP que só existe no SAP entra na conta só se diminuir a divergência da mangueira (decisão de 14/10).
7. Se o GMS tem um lance claramente absurdo (ex.: milhares de metros em poucos minutos), é erro de digitação, não troca de OP: não buscar compensação, listar como "corrigir no GMS" e pedir decisão do William.

## Passo a passo
1. Rodar `python -I top_ops_compensacao.py` e ler o resultado das 10 mais divergentes.
2. Para cada OP, montar uma linha: OP, mangueira, GMS, MB51, diferença, **proposta** (qual OP/OPs compensam e quanto sobra), **confiança** (forte = prova por lance; média = soma + data próxima; fraca = só soma; nenhuma), e **ação sugerida** (mover lance de OP no GMS, lançar no SAP, corrigir digitação).
3. Apresentar ao William em tabela curta. Esperar o "sim" dele por proposta antes de qualquer ação.
4. Depois, repetir para as próximas 10 (ajustar o corte no script: `top=top[:10]` vira fatia seguinte) até acabar as OPs com |dif| > 50 m.
5. Quando ele aceitar/recusar uma proposta, anotar a decisão em `lances_excluidos.csv` (se for exclusão) ou em um arquivo `decisoes_compensacao.csv` (OP;OP_compensadora;metros;decisao;data) e rodar `conferir_lances_por_op.py` de novo.

## Limites
- Não alterar dados no SharePoint, no SAP nem no app GMS. Este plano só analisa e propõe.
- Não enviar dados de produção/SAP a serviço externo.
- Commit por assunto e push na main, com mensagem curta em português.
- Respostas curtas e no detalhe: o William prefere conversar o caso a caso a receber resumo genérico.
