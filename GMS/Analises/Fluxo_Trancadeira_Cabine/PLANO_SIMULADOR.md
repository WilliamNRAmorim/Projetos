# Plano: simulador de headcount x demanda, da trançagem à cabine (01/11/2026)

Aprovado pelo William em 01/11/2026. A construção é numa sessão nova, em Sonnet, a partir deste arquivo.

## Objetivo
Dado o número de pessoas por etapa e turno e a demanda (metros por dia ou semana, com o mix de mangueiras), mostrar:
- a capacidade de cada etapa;
- o gargalo;
- o volume que sai na cabine e se a demanda é atendida;
- a conta inversa: quantas pessoas por etapa para entregar X m.

Tem que ser assertivo: provado contra o histórico antes de usar.

## Etapas cobertas
Trançagem → Cobertura → Bandagem → Vulcanização → Debandagem → Extração/Cabine.

## Fontes
- `GMS/Sharepoint Data GMS/ficha_producao.csv` (ou `GMS/IA/dados/ficha_producao.csv`): metros, fichas, hora de fim e operador por etapa. A base de extração já existe em `extrair_dados.py`.
- **Escala real (decisão do William):** planilha com as pessoas por etapa e turno de alguns meses. O William vai mandar. Até lá, monte tudo com o "quem apontou" (operadores distintos na ficha) como substituto e marque que é provisório.
- Limites de máquina: número de trançadeiras, capacidade da autoclave e velocidade/meta por mangueira. Fontes: `GMS/Engenharia`, `GMS/GMS_Mestre_BI.md` (Meta HH = minutos × velocidade da mangueira) e `GMS/IA/glossario.md`.
- Turnos: NORMA de 27/10/2026 (MEL-250). 1º 05:20–13:56 (517 min), 2º 13:57–22:19 (503 min), 3º 22:20–05:19 (420 min). O `GMS/CLAUDE.md` ainda traz a régua antiga; vale a NORMA.

## Passos
1. **Calibração** (`executor`, Sonnet): script Python que gera `parametros_simulador.csv`:
   - metros por pessoa·turno, por etapa e por família de mangueira (mediana e p25/p75, tirando dias atípicos como a parada de julho);
   - teto de máquina por etapa.
2. **Modelo:** capacidade da etapa = mín(pessoas × produtividade, máquinas × velocidade × minutos do turno). Volume na cabine = mín(demanda, capacidade de cada etapa), considerando o estoque entre etapas e o lead time quando ajudar no acerto.
3. **Prova com o passado:**
   - rodar o modelo com o headcount real de cada dia e comparar com o volume real, por etapa e na cabine;
   - meta de erro ≤ 10–15% por dia (MAPE);
   - relatório `backtest_simulador.md` com o erro, os dias em que mais errou e o motivo;
   - se não atingir a meta, ajustar a calibração (mix, turno, estoque) antes de seguir.
4. **Entrega no Power BI:**
   - parâmetros de "e se" (pessoas por etapa e turno, demanda, mix);
   - tabela de calibração;
   - medidas DAX: capacidade por etapa, gargalo, volume previsto, aderência à demanda, pessoas necessárias;
   - tudo num arquivo para colar no PC onde está o BI (`DAX_simulador.md`), seguindo o `GMS/GMS_Mestre_BI.md`.
5. **Revisão:**
   - `revisor` (Opus) para minutos de turno, meta e parada;
   - `revisor-leve` para scripts e DAX sem regra de negócio.
6. **Fechamento:** diário (`python GMS/gms.py --novo` para o MEL), `registro.md`, commit por assunto e push na main.

## Aceite
- O backtest atinge a meta de erro, ou o relatório explica por que não e o que falta (provavelmente a escala real).
- A conta inversa (pessoas para a demanda) bate com a direta.
- O DAX está pronto para colar, com os nomes de tabela e coluna do modelo do William (pedir o export ou o TMDL se precisar).
