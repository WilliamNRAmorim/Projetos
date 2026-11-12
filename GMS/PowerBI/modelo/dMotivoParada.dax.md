# MEL-107 / MEL-266 — dimensão de motivo padronizado com família OEE2 (DAX para colar no modelo "(GMS)")

> Gerado por `gerar_mapa_motivos.py`. **Versão 2 (OEE2, MEL-266): NÃO APLICADA.** Entra com o script de `oee2.tmdl.md`, só com o "libero" do William e a revisão do `revisor`.
> **Versão 1 (MEL-107, só Motivo e Tipo): APLICADA em 13/10/2026** no modelo (GMS) do workspace Controle de Fabricação, pelo editor TMDL do serviço, com o "sim" do William. Verificação: 32 motivos padrão em Hora-Hora, 0 linhas sem Tipo, soma por Tipo = total (8.906,67 h / 13.622 linhas). A versão 1 está no git (commit anterior a este arquivo) e no roteiro de volta de `oee2.tmdl.md`.
> Rollback da versão 1: apagar a tabela `dMotivoParada`, as colunas `Hora-Hora[Motivo Padrão]` e `Hora-Hora[Motivo 2 Padrão]` e os 3 relacionamentos pelo TMDL view.
> Vale para o Power BI Desktop (arquivo-fonte do modelo) e para a edição web do modelo. Se o modelo for
> republicado de um .pbix antigo, estas colunas somem: por isso o DAX fica versionado aqui.
> Colunas novas: `Família` (Azul, Cinza, Amarela, Vermelha; vazio na Montagem), `Categoria Danfoss`, `No OEE2` (Sim/Não), `Componente` (Disponibilidade/Performance), `Ordem Família` (1 a 4; 9 na Montagem) e `Cor` (hex do tema claro). Mapa e justificativa: seção A de `Analises/OEE2_HoraHora/PLANO_OEE2.md`.

## 1) Tabela calculada `dMotivoParada` (uma linha por motivo padrão)

```dax
dMotivoParada =
DATATABLE(
    "Motivo", STRING,
    "Tipo", STRING,
    "Família", STRING,
    "Categoria Danfoss", STRING,
    "No OEE2", STRING,
    "Componente", STRING,
    "Ordem Família", INTEGER,
    "Cor", STRING,
    {
        {"Falta de Demanda", "Organizacional", "Azul", "Sem atividade / sem produção planejada", "Não", "—", 1, "#2C6FBF"},
        {"Inventário", "Programada", "Azul", "Sem atividade / sem produção planejada", "Não", "—", 1, "#2C6FBF"},
        {"Manutenção Preventiva", "Programada", "Cinza", "Manutenção planejada", "Não", "—", 2, "#8A8F96"},
        {"Manutenção Preventiva (Fora do Prazo)", "Programada", "Cinza", "Manutenção planejada", "Não", "—", 2, "#8A8F96"},
        {"Manut. Prod. Total (MPT)", "Programada", "Cinza", "Manutenção planejada / autônoma", "Não", "—", 2, "#8A8F96"},
        {"Almoço", "Programada", "Cinza", "Pessoal: pausa", "Não", "—", 2, "#8A8F96"},
        {"Reunião", "Programada", "Cinza", "Pessoal: reunião / treinamento", "Não", "—", 2, "#8A8F96"},
        {"Reunião/Treinamento", "Programada", "Cinza", "Pessoal: reunião / treinamento", "Não", "—", 2, "#8A8F96"},
        {"Amostra", "Programada", "Cinza", "Validação (teste de produto)", "Não", "—", 2, "#8A8F96"},
        {"TESTE ENGENHARIA", "Programada", "Cinza", "Validação (teste de produto)", "Não", "—", 2, "#8A8F96"},
        {"Execução Check List Lean", "Programada", "Amarela", "Partida / início de turno", "Sim", "Disponibilidade", 3, "#F2B01E"},
        {"Alimentação de fio", "Processo", "Amarela", "Reabastecimento", "Sim", "Disponibilidade", 3, "#F2B01E"},
        {"Emenda de Fita", "Processo", "Amarela", "Reabastecimento", "Sim", "Disponibilidade", 3, "#F2B01E"},
        {"Troca de Carretel", "Processo", "Amarela", "Reabastecimento", "Sim", "Disponibilidade", 3, "#F2B01E"},
        {"Troca de Lenon", "Processo", "Amarela", "Reabastecimento", "Sim", "Disponibilidade", 3, "#F2B01E"},
        {"Troca de boneca", "Processo", "Amarela", "Reabastecimento", "Sim", "Disponibilidade", 3, "#F2B01E"},
        {"Bobinagem de Arame Espiral", "Processo", "Amarela", "Reabastecimento (preparo de material)", "Sim", "Disponibilidade", 3, "#F2B01E"},
        {"Puxada do Insulation", "Processo", "Amarela", "Reabastecimento (preparo de material)", "Sim", "Disponibilidade", 3, "#F2B01E"},
        {"Registro de Peck", "Processo", "Amarela", "Troca de lote: checagem de qualidade", "Sim", "Disponibilidade", 3, "#F2B01E"},
        {"Registro de Pick", "Processo", "Amarela", "Troca de lote: checagem de qualidade", "Sim", "Disponibilidade", 3, "#F2B01E"},
        {"Set-up", "Programada", "Amarela", "Troca de lote: preparação / troca de ferramenta", "Sim", "Disponibilidade", 3, "#F2B01E"},
        {"Troca de Ferramental (fieira/matriz)", "Processo", "Amarela", "Troca de lote: preparação / troca de ferramenta", "Sim", "Disponibilidade", 3, "#F2B01E"},
        {"Troca de composto", "Processo", "Amarela", "Troca de lote: preparação / troca de ferramenta", "Sim", "Disponibilidade", 3, "#F2B01E"},
        {"Manutenção Corretiva", "Falha", "Vermelha", "Defeito de máquina", "Sim", "Performance", 4, "#E2000F"},
        {"Ajuste da Máquina", "Processo", "Vermelha", "Defeito de máquina (re-set)", "Sim", "Performance", 4, "#E2000F"},
        {"Problemas com composto", "Material", "Vermelha", "Defeito de processo", "Sim", "Performance", 4, "#E2000F"},
        {"Problemas de qualidade", "Processo", "Vermelha", "Defeito de processo", "Sim", "Performance", 4, "#E2000F"},
        {"Resto de fio", "Material", "Vermelha", "Defeito de processo", "Sim", "Performance", 4, "#E2000F"},
        {"Falta de programação", "Organizacional", "Vermelha", "Defeito de processo: OP faltando", "Sim", "Performance", 4, "#E2000F"},
        {"Análise/Problema no tubo", "Falha", "Vermelha", "Defeito de processo: material ruim", "Sim", "Performance", 4, "#E2000F"},
        {"Quebra de fio", "Falha", "Vermelha", "Defeito de processo: quebra de material", "Sim", "Performance", 4, "#E2000F"},
        {"Falta de Carretel", "Material", "Vermelha", "Espera: material", "Sim", "Performance", 4, "#E2000F"},
        {"Falta de Lenon", "Material", "Vermelha", "Espera: material", "Sim", "Performance", 4, "#E2000F"},
        {"Falta de Mandril", "Material", "Vermelha", "Espera: material", "Sim", "Performance", 4, "#E2000F"},
        {"Falta de Mandril Soldado", "Material", "Vermelha", "Espera: material", "Sim", "Performance", 4, "#E2000F"},
        {"Falta de Mangueira", "Material", "Vermelha", "Espera: material", "Sim", "Performance", 4, "#E2000F"},
        {"Falta de Mangueira Trançada", "Material", "Vermelha", "Espera: material", "Sim", "Performance", 4, "#E2000F"},
        {"Falta de composto", "Material", "Vermelha", "Espera: material", "Sim", "Performance", 4, "#E2000F"},
        {"Falta de desmoldante", "Material", "Vermelha", "Espera: material", "Sim", "Performance", 4, "#E2000F"},
        {"Falta de fio - Bobinadeira", "Material", "Vermelha", "Espera: material", "Sim", "Performance", 4, "#E2000F"},
        {"Falta de insulation", "Material", "Vermelha", "Espera: material", "Sim", "Performance", 4, "#E2000F"},
        {"Falta de tubo", "Material", "Vermelha", "Espera: material", "Sim", "Performance", 4, "#E2000F"},
        {"Falta de operador", "Organizacional", "Vermelha", "Espera: operador", "Sim", "Performance", 4, "#E2000F"},
        {"Motivo Não Declarado", "Organizacional", "Vermelha", "Não declarado", "Sim", "Performance", 4, "#E2000F"},
        {"Sem apontamento", "Organizacional", "Vermelha", "Não declarado", "Sim", "Performance", 4, "#E2000F"},
        {"Falta de energia / ar", "Falha", "Vermelha", "Utilidades", "Sim", "Performance", 4, "#E2000F"},
        {"Divergência do Tempo Padrão", "Organizacional", "Vermelha", "Velocidade reduzida", "Sim", "Performance", 4, "#E2000F"},
        {"AP - Alteracao de Planejamento", "Organizacional", "", "", "", "", 9, ""},
        {"AU - Auditoria (Qualidade / Seguranca)", "Programada", "", "", "", "", 9, ""},
        {"CA - Calibracao / Verificacao de Instrumento", "Programada", "", "", "", "", 9, ""},
        {"FC - Falta de Componentes (O-ring, sleeve, mola, adaptador...)", "Material", "", "", "", "", 9, ""},
        {"FI - Falta de Embalagem / Termoencolhível", "Material", "", "", "", "", 9, ""},
        {"IT - Aguardando Instrucao de Trabalho / liberacao Engenharia", "Organizacional", "", "", "", "", 9, ""},
        {"LI - 5S", "Programada", "", "", "", "", 9, ""},
        {"RF - Refeição", "Programada", "", "", "", "", 9, ""},
        {"RT - Retrabalho", "Processo", "", "", "", "", 9, ""},
        {"TE - Tempo Excedido", "Excedido", "", "", "", "", 9, ""},
        {"TU - Troca de Turno", "Programada", "", "", "", "", 9, ""},
        {"VR - Velocidade Reduzida", "Processo", "", "", "", "", 9, ""}
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
