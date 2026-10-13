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
        w.writerow(["Fonte", "Motivo_bruto", "Linhas", "Motivo_padrao", "Tipo", "Obs"])
        w.writerows(sorted(mapa, key=lambda x: (x[0], x[3], x[1])))
    dim = {}
    for _, _, _, p, t, _ in mapa:
        dim[p] = t
    for p, t in {**CANON_HH, **CANON_PM}.items():
        dim.setdefault(p, t)
    with open(AQUI / "dMotivoParada.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["Motivo", "Tipo"])
        w.writerows(sorted(dim.items(), key=lambda x: (x[1], x[0])))
    # antes x depois
    antes = {(f, b) for f, b, *_ in mapa}
    print(f"{len(antes)} textos brutos -> {len(dim)} motivos padrão "
          f"({len({p for f, _, _, p, _, _ in mapa if f.startswith('HH')})} em Hora-Hora, "
          f"{len({p for f, _, _, p, _, _ in mapa if f.startswith('PM')})} na Montagem)")
    linhas_dax = ",\n        ".join(f'{{"{p}", "{t}"}}' for p, t in sorted(dim.items(), key=lambda x: (x[1], x[0])))
    (AQUI / "dMotivoParada.dax.md").write_text(DAX.replace("@@LINHAS@@", linhas_dax), encoding="utf-8")


DAX = '''# MEL-107 — motivo padronizado (DAX para colar no modelo "(GMS)")

> Gerado por `gerar_mapa_motivos.py`. **Não aplicado.** Aplicar só com o "sim" do William, depois da revisão.
> Vale para o Power BI Desktop (arquivo-fonte do modelo) e para a edição web do modelo. Se o modelo for
> republicado de um .pbix antigo, estas colunas somem: por isso o DAX fica versionado aqui.

## 1) Tabela calculada `dMotivoParada` (uma linha por motivo padrão)

```dax
dMotivoParada =
DATATABLE(
    "Motivo", STRING,
    "Tipo", STRING,
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
