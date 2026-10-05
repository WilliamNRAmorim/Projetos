# Auditoria GMS — 03 · O que mais erram na `ficha_producao`

Fonte: `Sharepoint Data GMS/ficha_producao.csv` (export de 02/10/2026, 2.648 linhas × 113 colunas).
Base: OPs **concluídas** com `Criado` ≥ 01/02/2026 (2.292). "Últimos 60 dias" = 629 OPs; "antes" = 1.663.
Limite honesto: **não tenho as tabelas de delineamento (DM_*) no repositório**, então não consigo medir "fora da especificação" de verdade,
só incoerências que aparecem no próprio dado (vazio, escala, metragem que sobe, validade vencida).

## 1. O que já foi corrigido (era grande, hoje ≈ 0)

| Campo | antes | últimos 60 d |
|---|---|---|
| Sem operador: Cobertura / Bandagem / Vulcanização / Debandagem | 9,1% / 11,9% / 10,3% / 14,6% | 0% / 0,8% / 0% / 0% |
| Sem turno: Vulcanização / Extração | 13,8% / 93,0% | 0% / 0% |
| Fim antes do início na Extração | 5,9% (90) | 0% |
| Metragem 0/vazia por etapa (Trançagem a Extração) | 4,1% a 9,9% | 0,8% a 1,1% (5 a 7 OPs) |
| `Cód_Fita_Bandagem` em branco | 93% | 4% |

## 2. O que ainda erram hoje (últimos 60 dias, ordem de tamanho)

1. **Metragem que *aumenta* de uma etapa para a seguinte (>5%)**: Trançagem→Cobertura **13,7%** (85 OPs), Cobertura→Bandagem 6,8%,
   Mandril→Tubo 6,5%, Tubo→Trançagem 4,7%, Debandagem→Extração 4,2%, Vulcanização→Debandagem 1,9%, Bandagem→Vulcanização **0%**
   (a herança automática funcionou). Mangueira não ganha metro no processo: é digitação ou medição diferente. A Trançagem pode ter
   motivo legítimo; a tolerância certa é decisão da engenharia.
2. **Composto vencido no uso** (validade anterior ao início da etapa): Tubo 2,1% (13), Cobertura 2,0% (12). Ou o composto vencido foi
   usado, ou a validade foi digitada errada. Nos dois casos o app hoje não barra nem destaca.
3. **Diâmetro em branco ou escala diferente**:
   - Cobertura: 4,6% em branco e **13,9% com valor > 5** (provável milésimo digitado no lugar de polegada; "0,48" e "480" na mesma coluna).
   - Tubo: 2,4% com valor > 5. Trançagem: 2,2% em branco e **56,8% > 5**: a coluna `Diametro_Trançagem` guarda milésimos (ex. 412), diferente das
     colunas vizinhas (0,48). Confirmar se é convenção; se for, a conferência com o delineamento precisa converter.
4. **Metragem 0 ou vazia**: ~1% por etapa (5 a 7 OPs em 60 dias). Coberto pela regra nova (fx_MetragemOk).
5. **Validade do composto da Cobertura em branco**: 2,7% (17). `Cod.Cobertura` em branco: 0,6% (4).
6. **Mangueira escrita de mais de um jeito**: `GH781-6`/`gh781-6`, `GH781-08`/`GH781-8`, `EC118-04L`/`EC118-4L`, `EC215-08L`/`EC215-08LRL`
   (a última pode ser produto diferente). O combo de mangueira resolve na origem.
7. `Código_Filme_UHMWPE` em branco em 51% das OPs: provavelmente só algumas mangueiras usam filme; não dá para exigir de todas sem a regra.

## 3. Por que só alguns campos têm aviso

Hoje só duas telas comparam a medida digitada com o delineamento:
- `scr_Finalização_1`: Ø interno e Ø externo (`fx_ForaDaFaixa`).
- `scr_Trancagem_3`: picks (`fx_ForaDaFaixa`).

`scr_mandril_1`, `scr_tubo_1`, `scr_Cobertura_2` e `scr_Bandagem_1` **mostram** a especificação no modal "Delineamento", mas **não
avisam** quando o operador digita fora dela. É o que o William descreveu: o detalhe de engenharia existe em alguns campos e não em todos.

## 4. Proposta (uma só): aviso de delineamento em todos os campos medidos

Mesma regra em toda etapa, sem bloquear (o alerta só grita quando há spec; spec ausente nunca acusa, igual ao `fx_ForaDaFaixa`):
- campo medido fora da faixa → borda vermelha + faixa "fora do delineamento (mín–máx)" no próprio campo;
- aplicado a: Mandril (Ø), Tubo (Ø externo, espessura, fieira), Trançagem (Ø, além do picks que já existe), Cobertura (Ø externo, espessura, fieira),
  Bandagem (fita, filme, layline);
- composto com validade anterior ao início da etapa → aviso forte (C18);
- metragem que sobe em relação à etapa anterior → aviso (limite a definir pela engenharia).

Entra tela por tela, na auditoria de cada uma (cada tela tem a sua fonte de spec). Para a conferência valer, falta:
1. as tabelas DM_* (ou a lista SharePoint de onde vêm) exportadas, para eu medir quantas OPs já saíram fora da faixa;
2. confirmação da unidade da coluna `Diametro_Trançagem` (milésimos);
3. a tolerância aceita para a metragem entre etapas (hoje usei 5% só para medir).
