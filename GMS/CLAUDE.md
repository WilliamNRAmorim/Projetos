# PROJETO GMS — Guaratinguetá Manufacturing System

MES híbrido (MES+APS+SCADA+LIMS+Lean+IA) em Power Platform: Power Apps Canvas (YAML), SharePoint Lists,
Power Automate, Power BI. Em produção na Danfoss Guaratinguetá (célula de mangueiras hidráulicas, 8 etapas:
Mandril → Tubo → Trançagem → Cobertura → Bandagem → Vulcanização → Debandagem → Extração/Teste,
+ Extrusora/Bobinadeira/Catenária + Montagem).

Idioma: PT-BR direto e informal. Respostas orientadas a ação. Uma única melhor solução, nunca cardápio de opções.

## LEIA ANTES DE QUALQUER COISA (nesta ordem)

1. `GMS_Indice.md` — qual arquivo é a versão vigente de cada tela e do App.Formulas.
2. `GMS_Mestre.md` — norma do app (Parte 0 P1–P11, A, B padrões, C conceitos C1–C40).
3. As **últimas ~40 linhas** do `GMS_Diario.md` + saída de `python gms.py --estado`. Nunca o diário inteiro.
4. `GMS_Licoes.md` — o que funciona e o que não funciona (o Mestre e as linhas NORMA mandam; este explica).
5. Só se a tarefa for de BI: `GMS_Mestre_BI.md`.

## FONTES DE VERDADE (precedência)

1. Linhas `NORMA` do `GMS_Diario.md` posteriores à última consolidação (P1).
2. `GMS_Mestre.md` — Parte 0 (P1–P11), A, B (padrões), C (C1–C40).
3. `GMS_Mestre_BI.md` — modelo semântico, DAX e relatórios.

Backlog, estado e próximo MEL NÃO estão no Mestre: saem do `GMS_Diario.md` via `gms.py`
(`--estado`, `--backlog`, `--novo`). Se a conversa contradisser o documento, o documento vence —
salvo emenda explícita ("isso emenda o Mestre, seção X") entregue como linha NORMA.

## PASTA `Telas/` — FONTE DE VERDADE DAS TELAS

- **Em 01/10/2026 a pasta `Telas/` está 100% atualizada: é verdade absoluta** para tudo que está publicado
  hoje (um `.txt` em YAML por tela `scr_*`, mais `Formulas.txt`, `OnStart.txt` e o resto das propriedades do App).
  Leia a tela daqui antes de patchear; **não precisa mais pedir o export** enquanto o arquivo da pasta estiver
  sincronizado. Para o App.Formulas, `Telas/Formulas.txt` é o vigente (o `App_Formulas_v3.0.2.powerfx` é histórico).
- **Regra de manutenção (norma do William, 01/10/2026): toda vez que uma tela mudar, o arquivo dela em
  `Telas/` tem que mudar junto, no mesmo ciclo.** Entregou patch de tela, `Formulas.txt` ou `OnStart.txt`?
  Aplique o mesmo patch no `.txt` correspondente (arquivo inteiro, versão nova) e diga qual arquivo foi gravado.
  Tela nova vira `Telas/scr_<Nome>.txt`. Tela excluída do app sai da pasta.
- Isso vale a partir de 01/10/2026. Se William editar o layout à mão no Studio fora da conversa, a pasta
  atrasa: nesse caso peça o export dessa tela e regrave o `.txt`.
- Ordem do ciclo: ler o `.txt` → patchar → `gms_qa_yaml.py` no resultado → gravar o `.txt` → linhas de diário.

## BASE DE CÓDIGO

- Antes de patchear tela publicada, leia o `.txt` dela em `Telas/` (verdade absoluta em 01/10/2026). Só peça
  export novo se William disser que mexeu à mão depois disso.
- Nunca altere X, Y, Width, Height de controle existente sem necessidade explícita.
  Quando alterar, liste quais controles mudaram.
- Tela publicada com layout ajustado à mão recebe patch por bloco (barra de fórmulas), nunca reimport.

## RESUMO OPERACIONAL (não substitui o Mestre)

1. Melhoria vence conservadorismo, com evidência (auditoria, doc oficial ou dado do GMS).
2. Patch cirúrgico, nunca rewrite; bloco YAML sempre completo; só versões de controle provadas (B §3.8);
   QA (`gms_qa_yaml.py`) antes de entregar. Uma única melhor solução — nunca cardápio de opções.
3. Prioridade: confiabilidade do dado → esforço do operador → decisão da supervisão → estética.
4. Referenciar MEL-xxx e Cxx. Nunca inventar ID: sem ID real, "MEL-???" e avisar.
5. Tela nova nasce dos Templates (B §6) e dos tokens fx_ (B §5.2).
6. PROIBIDO: `Now()>=6` ou comparar data com número; filtrar por `Modified`; `Patch` dentro de Timer;
   `UpdateContext` quando a lógica depende do dado (usar `ClearCollect`); fonte Excel nova;
   rótulo de schema visível ao operador; hardcode de cor/tamanho; `Coalesce(x, 0)` em exibição (usar `Blank()`).
7. Em dúvida: UMA pergunta diagnóstica.
8. Todo ciclo termina em linhas de diário (`DATA | TIPO | ALVO | VER | REF | TEXTO`), só com os 13 TIPOs
   da gramática: ABERTO, ENTREGUE, PUBLICADO, VALIDADO, FEITO, BLOQUEADO, RESOLVIDO, PENDÊNCIA, LIÇÃO,
   NORMA, DECISÃO, REVERTIDO, DESCARTADO.
9. Entrega visual: PNG ou arquivo `.html` — a rede da Danfoss bloqueia links de artifact.
10. Knowledge do Project no limite (2 MB): salvar só a versão vigente de cada tela; atualizar `GMS_Indice.md`
    e apagar a YAML anterior ao entregar versão nova.

## FERRAMENTAS (rodar dentro desta pasta)

```
python gms.py --estado        # telas, aguardando publish, pendências, normas fora do Mestre
python gms.py --backlog [F0]  # MELs abertas por fase
python gms.py --novo          # próximo ID MEL livre + linha modelo
python gms.py --mel 073       # histórico de um item
python gms.py --check         # valida a gramática do diário
python gms_qa_yaml.py Telas\scr_X.txt    # bateria de QA de YAML (obrigatória antes de entregar)
```

`gms.py` lê o `GMS_Diario.md` que estiver **na mesma pasta**. Precisa de PyYAML para o QA (`pip install pyyaml`).

## CONFERÊNCIA SAP x GMS (refugo, produção boa, PPM)

Antes de mexer em números de MB51/refugo/packlist, leia `Analises/Refugo_por_Material/COMO_USAR_OS_DADOS.md`
(fontes, regras, pegadinhas, receitas e números de referência) e use `gms_dados.py` da mesma pasta. Regra
central: SAP é a verdade, e faltou/sobrou se somam separados por material, nunca entre materiais.

## ⚠ DIÁRIO — LEIA

O `GMS_Diario.md` desta pasta é uma **RECONSTRUÇÃO de 01/10/2026** (o original de 359 linhas / MEL-140 foi
perdido). Até 03/09 ele é exato (mesmos IDs, MEL-109..140). Da seção `## RECONSTRUÍDO` em diante (04–30/09) é
**aproximado**: vem dos pacotes COLAR/PATCH, com IDs MEL-141..195 atribuídos na reconstrução e tag `#recon`
em cada linha. Próximo ID livre: MEL-196 (confira com `python gms.py --novo`). Pode haver lacunas do que só
foi dito em conversa; na dúvida sobre um MEL de setembro, trate o diário como pista, não como prova, e o
`Telas/` como verdade. Se o William achar o diário original, ele substitui este.

## ESTRUTURA DA PASTA

```
GMS/
├── CLAUDE.md                  ← este arquivo
├── GMS_Indice.md              ← versão vigente de cada coisa
├── GMS_Mestre.md              ← norma do app
├── GMS_Mestre_BI.md           ← norma do BI
├── GMS_Licoes.md              ← livro de lições
├── GMS_Diario.md              ← append-only (RECONSTRUÍDO em 01/10 — ver aviso acima)
├── App_Formulas_v3.0.2.powerfx← App.Formulas consolidado (o do Studio é a fonte real: peça export)
├── gms.py                     ← views derivadas do diário
├── gms_qa_yaml.py             ← QA de YAML
└── Telas/                     ← YAML vigente de cada tela (scr_*.txt), Formulas.txt, OnStart.txt — SEMPRE sincronizada
```
