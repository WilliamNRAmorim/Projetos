# GMS — Índice do Projeto
### Qual arquivo é a versão vigente de cada coisa · atualizado em 02/10/2026

> **Regra de leitura para o Claude:**
> 1. Leia este índice para saber **onde** está cada coisa.
> 2. Antes de patchear uma tela, leia o `.txt` dela em `Telas/` (verdade absoluta em 01/10/2026). Só peça export novo se o William disser que mexeu à mão depois.
> 3. Normas: `GMS_Mestre.md` (+ NORMAs do Diário). Aprendizado: `GMS_Licoes.md`.
>
> **Regra de manutenção:** entregou versão nova de uma tela? Atualize a linha dela aqui e **apague a YAML anterior** do projeto. O COLAR da versão anterior só sai depois que as linhas de diário dele estiverem dentro do `GMS_Diario.md`.

> **Nota da pasta local (01/10/2026):** este índice foi copiado do Knowledge do Project. Os caminhos `claude/...` abaixo
> se referem ao Knowledge. Nesta pasta, a versão vigente de cada tela é `Telas/scr_*.txt` (verdade absoluta em
> 01/10/2026, mantida em sincronia a cada mudança; ver CLAUDE.md). A coluna "YAML no projeto" da tabela abaixo
> é histórico: vale o arquivo de `Telas/`. Os COLAR, PATCH, conceitos e auditorias continuam só no Knowledge.

---

## Norma, estado e ferramentas

| O quê | Arquivo | Situação |
|---|---|---|
| Norma do app | `GMS_Mestre.md` | v2.0 (17/08). NORMAs posteriores ainda não consolidadas |
| Norma do BI | `claude/GMS_Mestre_BI.md` + `claude/GMS_Tema_BI.json` | 31/08 |
| Diário | `GMS_Diario.md` | **Reconstruído em 01/10/2026** (616 linhas, `--check` 0 erro). Exato até 03/09 (MEL-140); 04–30/09 aproximado, MEL-141..195 com tag `#recon`. Próximo ID: MEL-196 |
| Lotes de diário não colados | `claude/GMS_Diario_linhas_*` (8 arquivos, 19/08 → 02/09) | Absorvidos no diário reconstruído. Podem sair do Knowledge depois que o Diário subir para o Project |
| Derivação de estado | `gms.py` | `--estado`, `--backlog`, `--novo`, `--check`, `--consolidar` |
| QA de YAML | `gms_qa_yaml.py` (03/09) + `claude/PATCH_gms_qa_yaml_BarcodeReaderSize.md` (14/09) | Não testa propriedade × controle (Lições 1.11) |
| Lições | `claude/GMS_Licoes.md` | vivo |
| Conferência GMS × SAP × Packing (MEL-196) | `Conferencia_SAP/` — `GMS_ConferenciaDiaria.ts` v1.0.0, `GMS_LerPacking.ts` v1.0.0, `LEIA-ME_Montagem.md` (lista + fluxo), exemplo de e-mail | 02/10. Fluxo `GMS_Conferencia_Diaria` a montar. App.Formulas v3.0.4 (§16) em `Telas/Formulas.txt` |

## App.Formulas

| Camada | Arquivo |
|---|---|
| Base completa | `claude/App_Formulas_v2.8.powerfx` (21/09, montada a partir do arquivo real, que estava em v2.7.3) |
| Acréscimo §14 Painel | `claude/App_Formulas_patch_v2.9_Painel.powerfx` (22/09) |
| Acréscimos posteriores | Dentro dos COLAR do Painel v0.8.x/v0.9.0 (ex.: `fx_DetFechaSeg = 90`) |
| Notas de patch com lição | `claude/PATCH_AppFormulas_v2.6.1_TM04.md`, `claude/PATCH_AppFormulas_v2.7.3_LocaleVelocidade.md` |
| OnStart | `claude/OnStart_colVelocidadeProducao_2026-09-03.powerfx`, `claude/App_OnStart_patch_FichaTecnica.powerfx` |

⚠ A v2.8 + patches é reconstrução. **O arquivo que vale é o do Studio**: peça o export antes de gerar uma versão nova e consolide num `App_Formulas_v3.0.powerfx` único.

> **Atualização (30/09/2026):** o consolidado `App_Formulas_v3.0.2.powerfx` (30/09) já existe e está nesta pasta. Ele
> substitui a tabela acima (v2.8 + patches). Mesmo assim, o export do Studio continua sendo a fonte real.

## Telas: versão vigente no projeto

| Tela / módulo | Nome da tela | YAML no projeto | Patches por cima | Fora do projeto (subir) |
|---|---|---|---|---|
| Menu (Seleção de setor) | `scr_selecaosetor_1` | v0.7.1 | — | — |
| Seleção de Gestão | `scr_SelecaoGestao_1` | **v0.2.0** (02/10, `Telas/`) — card Conferência SAP | — | — |
| Conferência GMS × SAP × Packing | `scr_ConferenciaSAP` | **v0.1.1** (05/10, `Telas/`) | — | — |
| Painel da Célula (TV) | `scr_PainelCelula_1` | v0.8.1 | COLAR v0.9.0 (ficha de consulta) | **v0.9.1 / v0.9.2** (25/09) |
| Extrusora de Mandril | `scr_ExtrusoraMandril_2` | — | — | **v0.2.0** + COLAR EstoqueSolda (25/09) |
| Solda de Mandril | `scr_mandril_1` | v0.5.4 | COLAR v0.5.4 KanbanPelaFila | — |
| Tubo | `scr_tubo_1` | v0.4.0 | COLAR v0.4.1 + PATCH v0.4.1a | — |
| Trançagem | `scr_Trancagem_3` | v0.5.0 | COLAR v0.5.1 ComboOperador, v0.5.2 FiltroMaquina | — |
| Hora-Hora Trançagem | `scr_HoraHora_Trancagem_2` | v0.5.8 | COLAR v0.5.9 VelocidadeViva | — |
| AM-DM-02 Controle de Trançagem | `scr_AMDM02_Trancagem_1` | **v0.4.0** (21/10, `Telas/`) — folha por trança (seletor 1ª/2ª no cabeçalho, chave Data|Máquina|Trança), coleta na hora real com prazo +2 h, dia produtivo 05:20–05:20, carta X̄-R pela hora; listas em `Engenharia/Trancagem/AMDM02_schema.md` (MEL-114) | — | Criar a coluna Tranca (número, indexada) na AMDM02_Folha; HoraColeta já feita; colar Formulas v3.0.12 (§17 nova) e a tela no Studio |
| Hora-Hora Cobertura | `scr_HoraHora_Cobertura_1` (manual) e `scr_HoraHora_CoberturaGMS_1` (derivada) | v0.1.0 | — | — |
| Cobertura | `scr_Cobertura_2` | v0.3.0 | COLAR v0.4.0 Delineamento | — |
| Bandagem | `scr_Bandagem_2` | v0.3.0 | — | — |
| Vulcanização | `scr_Vulcanizacao_2` / `_1` | — | — | v0.2.0 (17/08). Trava de 5 carretéis (set/26) |
| Debandagem | `scr_Debandagem_2` | — | — | **v0.4.0** (28/08) |
| Extração/Teste | `scr_ExtracaoTeste_2` | v0.3.0 | — | **v0.4.0** COLAR (28/08) + cabines L1/L2 |
| Finalização | `scr_Finalizacao_1` | v0.4.0 | — | — |
| Bobinadeira | `scr_Bobinadeira_2` | v0.3.0 | — | — |
| Refugo Bobinadeira | `scr_RefugoBobinadeira_1` | v0.3.0 | — | — |
| Consulta OP | `scr_ConsultaOP_2` | v0.3.0 | — | — |
| Volume Diário | `scr_VolumeDiario_2` | v1.0.0 | PATCH v1.0.1 SaidaDaCelula | — |
| Ficha Técnica | `scr_FichaTecnica_1` | v1.2.1 | COLAR Menu_FichaTecnica | — |
| Montagem Hora-Hora | `scr_Montagem_HoraHora` | v0.5.0 | COLAR v0.5.0 ColunasCarimbadas | — |

Pergunta aberta desde 03/09: **quais telas `_1` legadas ainda estão publicadas?** A resposta fecha a coluna "Nome da tela".

## Conceito, gestão e apresentação

| Grupo | Arquivos |
|---|---|
| Conceitos | `GMS_Conceito_KanbanMandril`, `GMS_Conceito_KanbanTrancadeiras`, `GMS_Fluxo_AlertaKanbanTubo`, `PADRAO_relogio_de_tela`, `SHAREPOINT_FifoBobinadeira_v0.4.0` |
| Auditorias e validações | `GMS_Auditoria_BI_2026-08-31`, `GMS_Auditoria_BI_2026-09-01_ParadasMontagem`, `GMS_Conferencia_Velocidades_2026-09-03`, `GMS_Validacao_HoraHora_v0.5.4_2026-09-08` |
| Reunião | `GMS_Pauta_Reuniao`, `GMS_Reuniao_2026-08-31_Montagem_Produtividade`, `GMS_Briefing_Diario` (última execução: 01/09), `GMS_Estado_Celula.html` |
| Painel (resumo) | `GMS_Resumo_Painel_Celula_2026-09-22a24` |
| Mapas | `claude_GMS_Mapa_Navegacao_v3.html` / `.html.html` (03–04/09), `GMS_Mapa_Navegacao_v2.html` (17/08, histórico) |
| Apresentação | `PROMPT_Apresentacao_GMS_EUA.md`, `GMS_Kaizen_Award_EN_v4.pptx` |

## Limpeza de 25/09/2026 (o que saiu e por quê)

- **22 YAMLs de versões superadas**: Painel v0.1.0–v0.8.0, HoraHora Trançagem v0.5.0–0.5.2, Tubo v0.3.0–0.3.2, Mandril v0.5.0/0.5.3, Trançagem v0.4.0, Seleção v0.6.0/v0.7.0, Montagem v0.3.0/v0.4.0.
- **App.Formulas antigos**: v2.0, v2.4, v2.5, v2.6 e 11 patches anteriores à v2.8, que já contém tudo.
- **Resto do pacote `.msapp` de 03/07**: manifest, identity, logo e o json do app (×2).
- **Nenhum COLAR, diário, conceito ou auditoria foi apagado.** As lições desses arquivos continuam no projeto e em `GMS_Licoes.md`.
- Espaço de arquivos do projeto: **1,957 MB → ~1,13 MB**.
