# Terça: o que trazer e fazer no PC da fábrica (simulador)

Estado hoje: calibração e backtest rodados com headcount PROVISÓRIO (quem apontou). Meta de erro diário NÃO atingida (ver `backtest_simulador.md`). Falta a escala real.

## 1. Trazer
1. **Escala real** em CSV UTF-8, salvo como `GMS/Analises/Fluxo_Trancadeira_Cabine/escala_real.csv`, uma linha por dia × turno × etapa:
   ```
   data_ref,turno,etapa,pessoas
   2026-08-17,1,tranc,6
   ```
   - `data_ref`: AAAA-MM-DD (dia produtivo, começa 05:20); `turno`: 1, 2 ou 3 (NORMA 27/10, MEL-250);
   - `etapa`: tranc, cob, band, vulc, deb, cab;
   - `pessoas`: quem estava escalado (inteiro). Alguns meses, de preferência março a outubro/2026.
2. **Export ou TMDL do modelo do Power BI** (pasta .pbip/TMDL ou lista de tabelas e colunas) — para trocar os nomes do simulador pelos reais e fazer a seção 5 do DAX.
3. (Se tiver) CSV novo da `ficha_producao` com dados depois de 06/10, em `GMS/Sharepoint Data GMS/`.

## 2. Recalibrar e refazer o backtest
Na pasta `GMS/Analises/Fluxo_Trancadeira_Cabine`:
```
python calibrar_simulador.py
python backtest_simulador.py
```
Gera de novo `parametros_simulador.csv` e `backtest_simulador.md`. Com a escala real, a coluna `obs` deixa de dizer "provisorio".

## 3. Colar no BI
Seguir `DAX_simulador.md`: importar `parametros_simulador.csv` como `tCalibracao`, criar `tEtapaSim`, `tCenario`, os parâmetros e as medidas. Atualizar o k padrão do `p_Fator` pelo valor do backtest novo.

## 4. Depois
Mandar o resultado do backtest para ajustar (mix, estoque, teto de máquina com a velocidade por mangueira do `DM_Velocidade`).
