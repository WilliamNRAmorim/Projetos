# Projetos

| Pasta | O que tem |
|---|---|
| [`GMS/`](GMS) | Guaratinguetá Manufacturing System, o MES em Power Platform (app, telas, auditorias, documentação). |
| [`Producao_GMS_x_MB51/`](Producao_GMS_x_MB51) | Conciliação de metros entre o GMS e o SAP (MB51): `scripts/`, `dados/`, `registros/` (log das tratativas), `resultados/`, `docs/`, `Apresentação/` (deck e Excel das divergências). Tracker: `Pendentes_GMS_x_SAP.xlsx`. |
| [`Refugo/`](Refugo) | Análises de refugo: `Refugo_por_Material`, `Refugo_SAP_vs_GMS`, `PPM_Refugo`. |
| [`Packlists/`](Packlists) | Geradores e PDFs de packlist (`Packlists_Lote_Oficial`, `Packlists_6e7_Outubro`, `Lote_Teste_PackList`) e planos em `docs/`. |
| [`Dados_Historicos/`](Dados_Historicos) | Dados de antes do GMS e planilhas de controle: `HoraHora_pre_GMS/` (bancos de Hora-Hora 2023–2026 e a ferramenta Excel antiga) e `Eficiencia_Processo/2026/` (Controle do Processo Mangueira, uma aba por dia). |
| [`Documentos_GMS/`](Documentos_GMS) | Notas e auditorias soltas do GMS (MEL-231, MEL-240, automações Power Automate, saúde da ficha). |
| [`Conteudo_Bit/`](Conteudo_Bit) | Conteúdo de redes sobre os projetos (marca, vídeos, motor de render, Will Station). |
| [`FinAgent/`](FinAgent) · [`Sala_Agentes/`](Sala_Agentes) · [`TCC/`](TCC) · [`Ferramentas/`](Ferramentas) · `Missão Manutenção - Longe de Casa/` | Projetos próprios e utilitários. |

Regras e roteamento de modelos: `CLAUDE.md` e `PLANO.md`. Subagentes em `.claude/agents/`.

Scripts da conciliação rodam da raiz do repositório: `python -I Producao_GMS_x_MB51/scripts/<script>.py`.
