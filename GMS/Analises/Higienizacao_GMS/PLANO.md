# Plano: limpar o histórico do GMS (31/10/2026)

Feito pelo `planejador` (Haiku) e conferido pelo chefe. **Aguarda aprovação do William.** Destino: cópia limpa para a IA local (`GMS/IA/dados`, fora do git) e, se aprovado, correção na fonte (SharePoint).

## Antes de começar
- Referência de dados: `Refugo/Refugo_por_Material/COMO_USAR_OS_DADOS.md` (foi movido na reorganização; o `GMS/CLAUDE.md` ainda aponta o caminho antigo `GMS/Analises/...`).
- Base existente: `GMS/Analises/Higienizacao_HoraHora/` (roteiro e log). Correções já feitas à mão (TH07 27 a 30/10, ID 31560) entram como "já tratado".
- Pares duplicados em `GMS/Sharepoint Data GMS` (MB51 .txt/.xlsx, RegistrosInspeção, TiposErros, Máscara de produção, BD Packing List, ficha_producao): comparar o conteúdo; só perguntar ao William se forem diferentes.

## Fase 1: diagnóstico (só leitura)
Script local no PC; relatório em `GMS/Analises/Higienizacao_GMS/` só com contagens e IDs, sem linhas de produção. Verificações:
- duplicados (mesma chave Hora-Hora, ficha, OP, janela);
- campos obrigatórios vazios;
- datas impossíveis (futuras, data_ref fora do dia produtivo de 05:20);
- turno x horário pela NORMA de 27/10 (T1 320–836, T2 837–1339, T3 1340–319); esperado 146 Hora-Hora + 46 ficha com T2 entre 22:20 e 22:40 de 05 a 27/10;
- lacunas (dias sem registro por máquina);
- OP do GMS que não existe no MB51;
- unidades e valores fora de faixa;
- nomes de máquina e mangueira escritos de jeitos diferentes;
- divergência GMS x MB51 por OP e mangueira (SAP é a verdade; faltou e sobrou somados separados, por material).

Quem: `executor` (Sonnet) faz; `revisor` (Opus) confere método e regras de turno e parada.

## Fase 2: regras de correção (William aprova por escrito)
- Turno: T2 entre 22:20 e 22:40 (05 a 27/10) vira T3 (NORMA MEL-250). Passa pelo `revisor`.
- Hora e data: só corrige com evidência no próprio registro; senão marca "a conferir".
- Duplicado: fica o de maior ID ou o Finalizado; o outro vai para a lixeira.
- Lacuna: não inventa dado; fica registrada como lacuna.
- GMS x SAP: vale o SAP; o valor antigo do GMS é guardado antes da troca.
- Nomes e unidades: tabela de equivalência aprovada pelo William.
- Nunca apagar em definitivo (só lixeira); todo valor trocado guarda o antigo.
- Tempo Parado do Hora-Hora (MEL-255) não é parada real: não somar nem recalcular sem o `revisor`.

## Fase 3: aplicação
- 3A, cópia limpa para a IA: `.xlsx` limpos em `GMS/IA/dados`. Não mexe em produção; o William vê o relatório antes.
- 3B, fonte SharePoint: lotes de 5, com antes/depois e ID mostrados ao William; "sim" a cada lote; backup antes.
- Diário ao final (FEITO, PENDÊNCIA, NORMA quando houver regra nova).

## Aceite
- Fase 1: contagens batem com o diário (146 + 46).
- Fase 2: regras aprovadas por escrito.
- Fase 3: cada lote com antes/depois guardado, removidos na lixeira, releitura conferida.
