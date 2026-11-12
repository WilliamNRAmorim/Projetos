# -*- coding: utf-8 -*-
"""MEL-107: padronizacao dos motivos de parada (Hora-Hora e Paradas_Montagem).

Entrada : motivos_brutos_2026-10-13.csv  (fonte|motivo_bruto|linhas) - lido do modelo (GMS) em 13/10/2026,
          so rotulos e contagens, nenhum dado pessoal.
Saida   : motivos_mapa.csv        (cada texto bruto -> motivo padrao -> tipo)
          dMotivoParada.csv       (a dimensao: 1 linha por motivo padrao)
          dMotivoParada.dax.md    (tabela calculada + colunas calculadas prontas para colar no modelo)
Regras  : (1) tira o prefixo numerico "NN - " (era a posicao no dropdown e mudou ao longo do tempo);
          (2) a lista canonica e a fx_MotivosParada do app (Telas/Formulas.txt), com o Tipo dela;
          (3) sinonimos: "Refeicao" -> "Almoco" e "Problema no tubo" -> "Analise/Problema no tubo";
          (4) Montagem mantem o codigo de letras (RF, TE...), que e identificador e nao numero.
MEL-266 (OEE2): a dimensao ganha Familia (Azul/Cinza/Amarela/Vermelha), Categoria Danfoss, No OEE2, Componente,
          Ordem Familia e Cor, pelo mapa da secao A de Analises/OEE2_HoraHora/PLANO_OEE2.md (padrao Danfoss, Factbird
          Governance p. 10-12). Motivos da Montagem ficam sem familia (texto vazio, ordem 9). Os motivos que faltavam
          (Registro de Pick/Peck, TESTE ENGENHARIA, Bobinagem de Arame Espiral, Puxada do Insulation e os da Cobertura,
          Mandril e Tubo) entram em OUTROS_HH. Chave duplicada (sem diferenciar maiuscula) aborta a geracao.
"""
import csv
import re
from pathlib import Path

AQUI = Path(__file__).parent

# Lista oficial do app (Telas/Formulas.txt, fx_MotivosParada) - Tipo definido pelo William/MEL-100
CANON_HH = {
    "Amostra": "Programada", "Manut. Prod. Total (MPT)": "Programada", "Manutenção Preventiva": "Programada",
    "Manutenção Corretiva": "Falha", "Alimentação de fio": "Processo", "Troca de boneca": "Processo",
    "Falta de Carretel": "Material", "Falta de tubo": "Material", "Falta de Mandril": "Material",
    "Falta de Mandril Soldado": "Material", "Falta de fio - Bobinadeira": "Material",
    "Falta de programação": "Organizacional", "Quebra de fio": "Falha", "Falta de energia / ar": "Falha",
    "Falta de operador": "Organizacional", "Set-up": "Programada", "Ajuste da Máquina": "Processo",
    "Falta de insulation": "Material", "Falta de Lenon": "Material", "Troca de Lenon": "Processo",
    "Falta de Mangueira": "Material", "Almoço": "Programada", "Troca de Carretel": "Processo",
    "Emenda de Fita": "Processo", "Divergência do Tempo Padrão": "Organizacional", "Reunião": "Programada",
    "Execução Check List Lean": "Programada", "Falta de Demanda": "Organizacional", "Resto de fio": "Material",
    "Motivo Não Declarado": "Organizacional", "Sem apontamento": "Organizacional",
    "Análise/Problema no tubo": "Falha",
}
# Montagem: lista de letras do app da Montagem. TIPO = PROPOSTA (a confirmar), exceto RF e TE.
CANON_PM = {
    "AP - Alteracao de Planejamento": "Organizacional",
    "AU - Auditoria (Qualidade / Seguranca)": "Programada",
    "CA - Calibracao / Verificacao de Instrumento": "Programada",
    "FC - Falta de Componentes (O-ring, sleeve, mola, adaptador...)": "Material",
    "FI - Falta de Embalagem / Termoencolhível": "Material",
    "IT - Aguardando Instrucao de Trabalho / liberacao Engenharia": "Organizacional",
    "LI - 5S": "Programada",
    "RF - Refeição": "Programada",
    "RT - Retrabalho": "Processo",
    "TE - Tempo Excedido": "Excedido",   # nunca somar com parada real (GMS/CLAUDE.md, MEL-127)
    "TU - Troca de Turno": "Programada",
    "VR - Velocidade Reduzida": "Processo",
}
SINONIMOS = {"refeição": "Almoço", "problema no tubo": "Análise/Problema no tubo"}

# MEL-266: motivos que existem nas listas (Hora-Hora de 06/11, Cobertura, Mandril, Tubo) mas nao estavam na lista oficial
# da Trancagem. Tipo igual ao do app (fx_MotivosParadaCobertura) onde ja existe; os outros seguem a mesma logica.
OUTROS_HH = {
    "Registro de Pick": "Processo", "Registro de Peck": "Processo",       # "Peck" e erro de digitacao, mas esta gravado
    "TESTE ENGENHARIA": "Programada", "Bobinagem de Arame Espiral": "Processo", "Puxada do Insulation": "Processo",
    "Manutenção Preventiva (Fora do Prazo)": "Programada", "Reunião/Treinamento": "Programada",
    "Falta de Mangueira Trançada": "Material",
    "Troca de composto": "Processo", "Falta de composto": "Material", "Problemas com composto": "Material",
    "Troca de Ferramental (fieira/matriz)": "Processo", "Problemas de qualidade": "Processo",
    "Falta de desmoldante": "Material", "Inventário": "Programada",
}

# Familia Danfoss (Factbird Governance p. 10-12): motivo padrao -> (Familia, Categoria Danfoss, Componente do OEE2)
#   Azul = sem atividade; Cinza = atividade nao produtiva (as duas saem do tempo de producao, "No OEE2" = Nao)
#   Amarela = troca de lote (Disponibilidade); Vermelha = perda na operacao (Performance; a Danfoss poe quebra aqui).
CINZA_MAN, CINZA_VAL, CINZA_PES = "Manutenção planejada", "Validação (teste de produto)", "Pessoal: reunião / treinamento"
A_SETUP, A_REAB = "Troca de lote: preparação / troca de ferramenta", "Reabastecimento"
V_MAT, V_PROC, V_NAO = "Espera: material", "Defeito de processo", "Não declarado"
FAMILIA = {
    "Falta de Demanda": ("Azul", "Sem atividade / sem produção planejada"),
    "Inventário": ("Azul", "Sem atividade / sem produção planejada"),
    "Almoço": ("Cinza", "Pessoal: pausa"),
    "Reunião": ("Cinza", CINZA_PES), "Reunião/Treinamento": ("Cinza", CINZA_PES),
    "Manutenção Preventiva": ("Cinza", CINZA_MAN), "Manutenção Preventiva (Fora do Prazo)": ("Cinza", CINZA_MAN),
    "Manut. Prod. Total (MPT)": ("Cinza", "Manutenção planejada / autônoma"),
    "Amostra": ("Cinza", CINZA_VAL), "TESTE ENGENHARIA": ("Cinza", CINZA_VAL),
    "Set-up": ("Amarela", A_SETUP), "Troca de composto": ("Amarela", A_SETUP),
    "Troca de Ferramental (fieira/matriz)": ("Amarela", A_SETUP),
    "Registro de Pick": ("Amarela", "Troca de lote: checagem de qualidade"),
    "Registro de Peck": ("Amarela", "Troca de lote: checagem de qualidade"),
    "Execução Check List Lean": ("Amarela", "Partida / início de turno"),
    "Alimentação de fio": ("Amarela", A_REAB), "Troca de Carretel": ("Amarela", A_REAB),
    "Troca de Lenon": ("Amarela", A_REAB), "Troca de boneca": ("Amarela", A_REAB),
    "Emenda de Fita": ("Amarela", A_REAB),
    "Bobinagem de Arame Espiral": ("Amarela", "Reabastecimento (preparo de material)"),
    "Puxada do Insulation": ("Amarela", "Reabastecimento (preparo de material)"),
    "Manutenção Corretiva": ("Vermelha", "Defeito de máquina"),
    "Ajuste da Máquina": ("Vermelha", "Defeito de máquina (re-set)"),
    "Quebra de fio": ("Vermelha", "Defeito de processo: quebra de material"),
    "Análise/Problema no tubo": ("Vermelha", "Defeito de processo: material ruim"),
    "Resto de fio": ("Vermelha", V_PROC), "Problemas com composto": ("Vermelha", V_PROC),
    "Problemas de qualidade": ("Vermelha", V_PROC),
    "Falta de programação": ("Vermelha", "Defeito de processo: OP faltando"),
    "Falta de fio - Bobinadeira": ("Vermelha", V_MAT), "Falta de tubo": ("Vermelha", V_MAT),
    "Falta de insulation": ("Vermelha", V_MAT), "Falta de Carretel": ("Vermelha", V_MAT),
    "Falta de Lenon": ("Vermelha", V_MAT), "Falta de Mandril": ("Vermelha", V_MAT),
    "Falta de Mandril Soldado": ("Vermelha", V_MAT), "Falta de Mangueira": ("Vermelha", V_MAT),
    "Falta de Mangueira Trançada": ("Vermelha", V_MAT), "Falta de composto": ("Vermelha", V_MAT),
    "Falta de desmoldante": ("Vermelha", V_MAT),
    "Falta de operador": ("Vermelha", "Espera: operador"),
    "Falta de energia / ar": ("Vermelha", "Utilidades"),
    "Divergência do Tempo Padrão": ("Vermelha", "Velocidade reduzida"),
    "Motivo Não Declarado": ("Vermelha", V_NAO), "Sem apontamento": ("Vermelha", V_NAO),
}
ORDEM_FAMILIA = {"Azul": 1, "Cinza": 2, "Amarela": 3, "Vermelha": 4, "": 9}
# Cor da familia (tema claro do GMS_Tema: azul do painel, cinza #8A8F96, vermelho Danfoss; amarelo proprio)
COR_FAMILIA = {"Azul": "#2C6FBF", "Cinza": "#8A8F96", "Amarela": "#F2B01E", "Vermelha": "#E2000F", "": ""}


def atributos_oee2(motivo: str):
    """(Familia, Categoria Danfoss, No OEE2, Componente, Ordem Familia, Cor). Montagem e o que nao esta no mapa: vazio."""
    fam, cat = FAMILIA.get(motivo, ("", ""))
    if fam in ("Azul", "Cinza"):
        no, comp = "Não", "—"
    elif fam == "Amarela":
        no, comp = "Sim", "Disponibilidade"
    elif fam == "Vermelha":
        no, comp = "Sim", "Performance"
    else:
        no, comp = "", ""
    return fam, cat, no, comp, ORDEM_FAMILIA[fam], COR_FAMILIA[fam]



def limpa(bruto: str) -> str:
    t = bruto.strip()
    m = re.match(r"^\s*\d+\s*-\s*(.+)$", t)          # "24- Emenda" tambem
    return (m.group(1) if m else t).strip()


def padrao(fonte: str, bruto: str):
    if fonte.startswith("PM"):
        return bruto, CANON_PM[bruto], ""
    s = limpa(bruto)
    obs = "sem número" if s != bruto.strip() else ""
    if s.lower() in SINONIMOS:
        s, obs = SINONIMOS[s.lower()], (obs + "; sinônimo").strip("; ")
    canon = {k.lower(): k for k in CANON_HH}
    if s.lower() not in canon:
        raise SystemExit(f"motivo fora da lista oficial: {bruto!r}")
    s = canon[s.lower()]
    return s, CANON_HH[s], obs


def main():
    linhas = [l.rstrip("\n").split("|") for l in (AQUI / "motivos_brutos_2026-10-13.csv").read_text(
        encoding="utf-8").splitlines() if l.strip()]
    mapa = []
    for fonte, bruto, n in linhas:
        p, tipo, obs = padrao(fonte, bruto)
        mapa.append((fonte, bruto, int(n), p, tipo, obs))
    with open(AQUI / "motivos_mapa.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["Fonte", "Motivo_bruto", "Linhas", "Motivo_padrao", "Tipo", "Obs", "Familia", "Categoria_Danfoss"])
        w.writerows((*m, *atributos_oee2(m[3])[:2]) for m in sorted(mapa, key=lambda x: (x[0], x[3], x[1])))
    dim = {}
    for _, _, _, p, t, _ in mapa:
        dim[p] = t
    for p, t in {**CANON_HH, **OUTROS_HH, **CANON_PM}.items():
        dim.setdefault(p, t)
    # chave duplicada (DAX nao diferencia maiuscula de minuscula) derrubaria o relacionamento com a Hora-Hora
    vistos = {}
    for p in dim:
        k = p.casefold()
        assert k not in vistos, f"chave duplicada na dMotivoParada: {p!r} e {vistos[k]!r}"
        vistos[k] = p
    sem_familia = [p for p in dim if p not in CANON_PM and p not in FAMILIA]
    assert not sem_familia, f"motivo da Trançagem/Cobertura sem família: {sem_familia}"
    extras = [p for p in FAMILIA if p not in dim]
    assert not extras, f"família para motivo que não está na dimensão: {extras}"
    linhas_dim = sorted(((p, t, *atributos_oee2(p)) for p, t in dim.items()), key=lambda x: (x[6], x[3], x[0]))
    with open(AQUI / "dMotivoParada.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["Motivo", "Tipo", "Família", "Categoria Danfoss", "No OEE2", "Componente", "Ordem Família", "Cor"])
        w.writerows(linhas_dim)
    antes = {(f, b) for f, b, *_ in mapa}
    print(f"{len(antes)} textos brutos -> {len(dim)} motivos padrão "
          f"({len({p for f, _, _, p, _, _ in mapa if f.startswith('HH')})} em Hora-Hora, "
          f"{len({p for f, _, _, p, _, _ in mapa if f.startswith('PM')})} na Montagem; "
          f"{len(OUTROS_HH)} motivos novos de Hora-Hora/Cobertura/Mandril/Tubo; "
          f"{sum(1 for r in linhas_dim if r[2])} com família OEE2)")
    linhas_dax = ",\n        ".join(
        "{" + ", ".join(f'"{v}"' if i != 6 else str(v) for i, v in enumerate(r)) + "}" for r in linhas_dim)
    (AQUI / "dMotivoParada.dax.md").write_text(DAX.replace("@@LINHAS@@", linhas_dax), encoding="utf-8")


DAX = '''# MEL-107 / MEL-266 — dimensão de motivo padronizado com família OEE2 (DAX para colar no modelo "(GMS)")

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
        @@LINHAS@@
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
'''

if __name__ == "__main__":
    main()
