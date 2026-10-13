# MEL-107 — motivo padronizado (DAX para colar no modelo "(GMS)")

> Gerado por `gerar_mapa_motivos.py`. **APLICADO em 13/10/2026** no modelo (GMS) do workspace Controle de Fabricação, pelo editor TMDL do serviço, com o "sim" do William. Revisão do `revisor` não ocorreu (agente indisponível na sessão). Atualização de dados feita às 10:17; verificação: 32 motivos padrão em Hora-Hora, 0 linhas sem Tipo, soma por Tipo = total (8.906,67 h / 13.622 linhas).
> Rollback: apagar a tabela `dMotivoParada`, as colunas `Hora-Hora[Motivo Padrão]` e `Hora-Hora[Motivo 2 Padrão]` e os 3 relacionamentos pelo TMDL view.
> Vale para o Power BI Desktop (arquivo-fonte do modelo) e para a edição web do modelo. Se o modelo for
> republicado de um .pbix antigo, estas colunas somem: por isso o DAX fica versionado aqui.

## 1) Tabela calculada `dMotivoParada` (uma linha por motivo padrão)

```dax
dMotivoParada =
DATATABLE(
    "Motivo", STRING,
    "Tipo", STRING,
    {
        {"TE - Tempo Excedido", "Excedido"},
        {"Análise/Problema no tubo", "Falha"},
        {"Falta de energia / ar", "Falha"},
        {"Manutenção Corretiva", "Falha"},
        {"Quebra de fio", "Falha"},
        {"FC - Falta de Componentes (O-ring, sleeve, mola, adaptador...)", "Material"},
        {"FI - Falta de Embalagem / Termoencolhível", "Material"},
        {"Falta de Carretel", "Material"},
        {"Falta de Lenon", "Material"},
        {"Falta de Mandril", "Material"},
        {"Falta de Mandril Soldado", "Material"},
        {"Falta de Mangueira", "Material"},
        {"Falta de fio - Bobinadeira", "Material"},
        {"Falta de insulation", "Material"},
        {"Falta de tubo", "Material"},
        {"Resto de fio", "Material"},
        {"AP - Alteracao de Planejamento", "Organizacional"},
        {"Divergência do Tempo Padrão", "Organizacional"},
        {"Falta de Demanda", "Organizacional"},
        {"Falta de operador", "Organizacional"},
        {"Falta de programação", "Organizacional"},
        {"IT - Aguardando Instrucao de Trabalho / liberacao Engenharia", "Organizacional"},
        {"Motivo Não Declarado", "Organizacional"},
        {"Sem apontamento", "Organizacional"},
        {"Ajuste da Máquina", "Processo"},
        {"Alimentação de fio", "Processo"},
        {"Emenda de Fita", "Processo"},
        {"RT - Retrabalho", "Processo"},
        {"Troca de Carretel", "Processo"},
        {"Troca de Lenon", "Processo"},
        {"Troca de boneca", "Processo"},
        {"VR - Velocidade Reduzida", "Processo"},
        {"AU - Auditoria (Qualidade / Seguranca)", "Programada"},
        {"Almoço", "Programada"},
        {"Amostra", "Programada"},
        {"CA - Calibracao / Verificacao de Instrumento", "Programada"},
        {"Execução Check List Lean", "Programada"},
        {"LI - 5S", "Programada"},
        {"Manut. Prod. Total (MPT)", "Programada"},
        {"Manutenção Preventiva", "Programada"},
        {"RF - Refeição", "Programada"},
        {"Reunião", "Programada"},
        {"Set-up", "Programada"},
        {"TU - Troca de Turno", "Programada"}
    }
)
```

## 2) Coluna calculada `Hora-Hora[Motivo Padrão]` (repetir igual para `Hora-Hora[Motivo 2]` → "Motivo 2 Padrão")

```dax
Motivo Padrão =
VAR t = TRIM ( 'Hora-Hora'[Motivo] )
VAR p = IFERROR ( SEARCH ( "-", t ), 0 )
VAR pre = IF ( p > 1, TRIM ( LEFT ( t, p - 1 ) ), "" )
-- tira o prefixo "NN - " (posição antiga no dropdown); "Set-up" e "Falta de fio - Bobinadeira" não são números
VAR limpo = IF ( IFERROR ( VALUE ( pre ), -1 ) >= 0, TRIM ( MID ( t, p + 1, 300 ) ), t )
RETURN
    IF (
        ISBLANK ( 'Hora-Hora'[Motivo] ), BLANK (),
        SWITCH (
            TRUE (),
            limpo = "Refeição", "Almoço",
            limpo = "Problema no tubo", "Análise/Problema no tubo",
            limpo
        )
    )
```

## 3) Relacionamentos (muitos-para-um, sentido único)

- `Hora-Hora[Motivo Padrão]` → `dMotivoParada[Motivo]`
- `Hora-Hora[Motivo 2 Padrão]` → `dMotivoParada[Motivo]` (inativo; ativar com USERELATIONSHIP quando precisar)
- `Paradas_Montagem[Motivo]` → `dMotivoParada[Motivo]` (a Montagem já grava o código de letras, sem número)

## 4) Depois de aplicado, no relatório

- Trocar `Hora-Hora[Motivo]` por `Hora-Hora[Motivo Padrão]` nos visuais, slicers e no filtro de refeição
  (um filtro só: `Almoço`). Usar `dMotivoParada[Tipo]` para separar Falha de Programada (MTBF, C19/K17).
- Na Montagem, filtrar `Tipo <> "Excedido"` onde se soma parada real: `TE - Tempo Excedido` nunca soma com parada.
