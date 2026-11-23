# Plano de mangueira x SAP: próxima sessão (deixado em 23/11/2026)

Plano aprovado pelo William em 19/11. Tudo pronto no disco e commitado; nada aplicado no modelo nem publicado.

## Falta, nesta ordem
1. **Revisor (Opus)**: revisar `GMS/PowerBI/modelo/plano_mangueira.tmdl.md` (tabelas dPlanoMangueira, dClasseMangueira, medidas HP) e as 5 medidas `HP · SVG ...` do `GMS/PowerBI/GMS_Painel.Report/definition/reportExtensions.json` (página `pg_plano_mangueira`). Regra: Plano = soma do Volume do mês; Produzido = fProducaoSAP Mangueira por Material até o corte da Máscara SAP; ritmo = dias contabilizados ÷ dias úteis (GMS_MetaMensal); Atraso = (ritmo − %) × plano, positivo = atrasado; Para fechar = (plano − produzido) ÷ (úteis − contabilizados), vazio com mês fechado; produção sem plano = "Fora do plano". Olhar caixa do código (`ec215-06L`), nomes que conflitam (`Atraso`, `Dias Restantes`), totais, divisão por zero no SVG. Na sessão de 19–23/11 o agente `revisor` não carregou.
2. **Gravar novembro na lista `GMS_PlanoMangueira`** (Id 34631d40-3ad8-4226-82d6-8d5f8fd1ce0a, site OperationsGuaratingueta, colunas Title, Mes, CStandard, Tipo, Arame, Volume). O William deu o "sim" em 23/11 para gravar os 45 itens de `nov_2026_lista.csv` (162.016 m, Mes = 2026-11-01T03:00:00Z), mas o login do navegador embutido expirou e **nada foi gravado**. Conferir `ItemCount = 0` antes (não duplicar) e reler depois (45 itens, soma 162.016).
3. William cola os 3 passos do `plano_mangueira.tmdl.md` no TMDL view (depois do `mascara_producao.tmdl.md`), atualiza, roda a verificação da seção 4, reabre `GMS_Painel.pbip`, confere com `prototipo.html` e publica.

## Pontos para o William
- Dias úteis de novembro: 22 na GMS_MetaMensal x 23 na planilha. Se for 23, corrigir a lista (muda também a Máscara SAP).
- Conferência (`conferir.py --hoje 2026-11-18`): 85.746 m x 85.671 m da planilha salva (2 linhas da MB51 mudaram depois: GH781-6 e 2556-12).
