# 00 · Pacote de conhecimento do Uiu (leia primeiro)

Pacote F0 de `GMS/IA/Copilot_Uiu/PLANO_UIU.md`, gerado em 09/11/2026. Cada arquivo é um resumo curado de um documento do repositório GMS; o documento de origem é citado no topo de cada um.

## Precedência quando dois arquivos brigarem
1. 08_Normas_Diario.md (linha NORMA/DECISÃO mais nova vence).
2. 01_Norma_do_App.md (Mestre do app).
3. 02_KPIs_do_BI.md (Mestre do BI e decisões vigentes da meta).
4. Os demais (lições, roteiro, dados, glossário, memória) explicam; não mandam.
SAP é a verdade de quantidade (07). Dado das listas SharePoint é a verdade do que foi apontado (09).

## Arquivos
- 01_Norma_do_App.md: protocolo, conceitos C1–C40 e padrões técnicos do app Power Apps.
- 02_KPIs_do_BI.md: KPIs do Power BI (fórmula, recorte, armadilha) e regras vigentes da meta.
- 03_Licoes.md: o que funciona e o que não funciona no GMS.
- 04_Glossario.md: etapas, regras de negócio, turnos e dia produtivo.
- 05_Memoria_IA.md: fatos registrados pela IA local (ainda "a conferir").
- 06_Roteiro_HoraHora.md: lista Hora-Hora, janelas e minutos por turno, Fechar turno (ND/NT/CAP).
- 07_Dados_SAP_x_GMS.md: conferência GMS x MB51, refugo, PPM e pegadinhas.
- 08_Normas_Diario.md: linhas NORMA e DECISÃO do Diário desde 01/09/2026, mais novas primeiro.
- 09_Mapa_Listas.md: listas SharePoint e nomes internos das colunas para o `$filter`.
- Manual_BO.md: receitas de diagnóstico e correção (sintoma, consulta, confirmação, causa, correção).

## Regras que nunca mudam
- Nenhuma gravação sem mostrar antes → depois e receber o "sim" do William. Um "sim" vale para um lote.
- Nunca apagar em definitivo; o Uiu não cria nem apaga item.
- Nunca zerar ou descartar mangueira por não achar o nome: ligar pela OP.
- Parada, pausa e tempo excedido nunca se somam.

## Atualizar o pacote
O `08` é gerado por `GMS/IA/Copilot_Uiu/gerar_normas_diario.py`; rode de novo antes de cada upload. Os outros são resumos: quando o documento de origem mudar, refaça o resumo dele.
