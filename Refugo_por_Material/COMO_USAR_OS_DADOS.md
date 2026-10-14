# Como lidar com os dados de conferência SAP x GMS (refugo e produção boa)

Guia criado em 07/10/2026 na análise de refugo lançado errado (16/05 a 16/09/2026). Serve para quem
for refazer o cálculo (pessoa ou Claude) sem repetir os tropeços. O código está em `gms_dados.py`.

## 1. De onde vêm os números

| O quê | Arquivo | Aba / campo |
|---|---|---|
| SAP (MB51: lançamentos de produção e refugo) | `Relatorio_Conferencia_MB51_v3_2.xlsx` | aba `MB51` (também há `Sharepoint Data GMS/mb51.xlsx`, o export cru) |
| GMS x SAP x packlist por OP | `Relatorio_Conferencia_MB51_v3_2.xlsx` | aba `Conf_Geral` (1 linha por OP; texto da conferência na coluna `Obs.`) |
| Refugo do GMS | `Sharepoint Data GMS/TiposErros.csv` (e aba `TiposErros` do relatório) | 1 linha por apontamento de refugo |
| Inspeção boa do GMS | `Sharepoint Data GMS/RegistrosInspeção.csv` | `OP_ID`, `Quantidade`, `CodigoDefeito`, `cabine_teste` |
| Etapas por OP (lote em cada máquina) | `Sharepoint Data GMS/ficha_producao.csv` | `quantidade_*` por etapa; `quantidade_debandagem`, `quantidade_extracao` |
| Refugo SAP x GMS linha a linha (já casado) | `Analises/Refugo_SAP_vs_GMS/Refugo_GMS_alinhado_ao_SAP.xlsx` | abas `Por OP` e `Ajustes` (variação = SAP − GMS) |
| Plano de tratativa (150 OPs de erro de refugo) | `Analises/Conferencia_MB51/Plano_Tratativa_MB51.xlsx` | aba `Refugo` |

Os `.txt` ao lado de cada export em `Sharepoint Data GMS/` são só o link do SharePoint. A fonte viva é o
SharePoint; o que está no repositório é uma fotografia (relatório base de 01/10/2026, exports de 06/10 e a
`ficha_producao` de 07/10). Antes de afirmar algo "de hoje", confira a data do arquivo.

## 2. Como o refugo aparece em cada sistema

- **SAP:** lançamento 101 (entrada de produção) feito pelos usuários `U445131` e `U452021`. O SAP **não informa o
  tipo de defeito**. Estorno é 102.
- **GMS:** linhas da lista `TiposErros` (tipo, quantidade em metros, data de criação). Linhas novas (a partir
  de set/2026) vêm sem `Id` no export: identifique pela data de criação.
- **Produção boa:** no SAP é 101 menos 102 **sem** os lançamentos dos usuários de refugo. No GMS é a inspeção
  (`quantidade_extracao` da ficha / `GMS: inspeção (m)` na `Conf_Geral`). O total do GMS é boa + refugo.

## 3. Regras que usamos (e por quê)

1. **SAP é a verdade absoluta.** O GMS é ajustado para bater com o SAP. Diferença = SAP − GMS: negativa = faltou
   lançar no SAP; positiva = sobrou no SAP (duplicado ou excesso).
2. **Material não compensa com material.** Inventário é por material: faltar na GH781-8 não cancela duplicado na
   GH781-10. Some faltou e sobrou **separados**; só compense dentro do mesmo material. (Erro cometido na primeira
   versão: citei um "saldo líquido" geral que não vale para inventário.)
3. **Lance mandado em outra OP é costume da fábrica.** Aparece como falta numa OP e sobra de mesmo valor na OP
   vizinha (ex.: GH781-4, OP 29422610 x 29367063: 63,23 m). Dentro do mesmo material isso se anula. Já a produção
   boa divergente foi tratada como justificada (troca de OP ou GMS sem registro no dia), e a análise de refugo
   ignora a divergência de produção boa.
4. **Data do erro:** data do lançamento no SAP quando existe; senão (refugo que o SAP não recebeu) a data de
   criação no GMS. Dia sem produção (fim de semana, parada) soma no próximo dia de produção.
5. **PPM = metros errados ÷ metros de produção boa × 1.000.000.** Base de produção = SAP (cobre OPs que o GMS
   não tem). Material de produção pequena infla o PPM (ex.: FC839B-08, 1.900 m, 32 m de erro = 16.904 ppm).
6. **PPM de refugo é para uso interno** (lição 7.6 do `GMS_Licoes.md`: não mostrar a público externo).

## 4. Pegadinhas

- **Nome do material não é padrão.** `GH781-6` e `HOSE-AER, GH781, -6, R2/2SC` são o mesmo item na prática;
  `norm_material()` junta os dois. Confirme com o código SAP antes de afirmar. Seis materiais (EC215-08LRL,
  2583-12, HC139-7_S-GX, HC101-6, GH493-12, GH493-16) **não têm produção casada na MB51** (descrição diferente);
  ficam sem PPM por material.
  **Resolvido em 14/10/2026:** a MB51 nova (`Producao_GMS_x_MB51/mb51 (5).xlsx`) traz a coluna `Material` (código) e a
  `Order`. Nunca zere nem descarte uma mangueira por não achar o nome: ligue o nome do GMS ao material SAP **pela OP**
  (a mesma OP nos dois lados). Tabela aprendida em `Producao_GMS_x_MB51/aliases_mangueira.csv`. Casos que já pegaram:
  `2583-12` = **12055040** "Hose, 100R3Polyester Braid" (confirmado pelo William); `GH493-6/8/10/12/16` = descrição
  genérica "HOSE R12" (o código é o nome); `HC101-6` tem descrição "-5" no SAP; `HC139-7_S-GX` e `EC215-08LRL`/`EC215-12LRL`
  são códigos próprios (a descrição normalizada cai no HC139-7 / EC215-08L / EC215-12L, então compare pelo código);
  `GH781-6-2`, `EC215-06L-2` e `FC735-4` são grafias do GMS do mesmo material. Quando o GMS diz uma mangueira e a OP
  no SAP é de outra (ex.: OP 29878642 GH781-8 no GMS e FC735-08 no SAP), é divergência real da OP, não alias.
  Script: `Producao_GMS_x_MB51/conferir_lances_por_op.py` (casamento lance a lance por OP).
- **A coluna `Material` da MB51 vem vazia;** use `Material Description`.
- **Unidades:** a MB51 mistura `M`, `PC` e `KG`. Metros de mangueira = só `M` (descarta ~6,6 mil linhas em peças).
- **Formato dos CSVs do SharePoint:** datas `MM/DD/AAAA h:mm AM/PM`; números com vírgula de milhar na ficha
  (`"1,050"`) e ponto decimal (`"944.20"`). Converta com `float(s.replace(",", ""))`.
- **A `ficha_producao` tem uma linha por OP,** com o lote em cada etapa (o comprimento cresce: 800 m na trançagem,
  1.050 m na debandagem). A debandagem **não** é teto exato: em várias OPs a extração passa dela.
- **Parada de julho:** sem produção de 04 a 26/07 no SAP e no GMS (provável férias coletivas; confirmar).
  Mês de produção pequena distorce PPM.
- **Meses somados ≠ período inteiro:** a compensação é feita dentro de cada mês (661 m) e no período (581 m); uma
  troca de OP que atravessa meses aparece maior nos meses.
- **Linhas "e mais N" do texto da conferência não foram somadas:** os totais de lances são piso.

## 5. Receitas

```python
import datetime as dt, gms_dados as g
ini, fim = dt.date(2026, 5, 16), dt.date(2026, 9, 16)
lin = g.linhas_refugo(ini, fim)             # (data, OP, material, ação, variação)
faltou, sobrou, por_mat = g.faltou_sobrou(lin)
dia, mat = g.producao_boa_sap(ini, fim)     # metros bons por dia e por material
g.ppm(faltou + sobrou, sum(dia.values()))   # ≈ 974
```

`python gms_dados.py` imprime o resumo do período. Para uma OP: filtre a aba `MB51` por `Order` (a MB51 da OP
29072011 mostra 20 entradas 101 de produção boa, 1 estorno 102 e nenhum lançamento de usuário de refugo).

## 6. Números de referência (para conferir se refez certo)

Período 16/05 a 16/09/2026: **faltou 211,6 m + sobrou 369,3 m = 580,9 m em 39 materiais**; produção boa SAP
596.547 m (GMS 492.691 m); **974 ppm** (SAP) / 1.179 ppm (GMS). Mensal (PPM total): mai 1.986, jun 1.538,
jul 982, ago 434, set 553. Em maio o erro era sobretudo falta; de junho em diante é sobra (duplicado/excesso).
GH781-4: 116 m faltando, 113,2 m deles na OP 29072011 (22 apontamentos no GMS em 29/05, nada no SAP; produção
boa 944,2 m + refugo 113,2 m = 1.057,4 m contra 1.050 m na debandagem).

## 7. O que ainda não está fechado

- Confirmar o código SAP dos materiais agrupados por nome e achar a produção dos seis sem PPM.
- Confirmar com a produção se os 113,2 m de refugo da OP 29072011 são reais (índice de 12%, mediana da GH781-4 é 1,1%).
- Separar, material a material, o que é troca de OP (se anula) e o que é refugo realmente não enviado.
- Os arquivos são de 01/10/2026 (relatório) e 06–07/10 (exports); correções feitas depois não aparecem.
