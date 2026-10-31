#!/usr/bin/env python3
"""FASE 1 da higienização do GMS: diagnóstico SÓ LEITURA.

Lê os exports de `GMS/Sharepoint Data GMS` (não grava nada lá, nem no SharePoint, nem em GMS/IA/dados)
e escreve `Diagnostico_<data>.md` nesta pasta com CONTAGENS e IDs de amostra (nunca linhas de produção).

Uso:  python -I diagnostico_gms.py [--hh CAMINHO_EXPORT_HORAHORA.csv] [--data 2026-10-31]
O export da Hora-Hora não está na pasta de fontes; se o William der um CSV (colunas internas da lista:
ID, Title, field_0 Data, field_2 Célula, field_3 Hora, field_4 Mangueira, field_7 Real, field_11 Parado,
TurnoH, Status, Minutos), passe em --hh e as verificações da Hora-Hora também rodam.
"""
import argparse, collections, datetime as dt, hashlib, re, sys
from pathlib import Path
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]            # .../GMS
SRC = RAIZ / "Sharepoint Data GMS"
OUT = Path(__file__).resolve().parent
USUARIOS_REFUGO = {"U445131", "U452021"}              # lançam refugo (101) na MB51 (COMO_USAR_OS_DADOS.md)
FMT = "%m/%d/%Y %I:%M %p"
NORMA_INI, NORMA_FIM = dt.date(2026, 10, 5), dt.date(2026, 10, 27)   # janela da NORMA MEL-250
HOJE = dt.date(2026, 10, 31)

# turnos da NORMA de 27/10 (MEL-250): T1 320-836, T2 837-1339, T3 1340-319
def turno_norma(minuto):
    return 1 if 320 <= minuto <= 836 else 2 if 837 <= minuto <= 1339 else 3

def minuto(ts):
    return ts.hour * 60 + ts.minute

def dia_produtivo(ts):
    """dia produtivo começa 05:20; antes disso pertence ao dia anterior"""
    return (ts - pd.Timedelta(minutes=320)).date()

def lido(path, **kw):
    for enc in ("utf-8-sig", "cp1252"):
        try:
            return pd.read_csv(path, encoding=enc, dtype=str, low_memory=False, **kw)
        except UnicodeDecodeError:
            continue
    raise RuntimeError(path)

def col(df, *prefixos):
    """acha coluna por prefixo (os nomes vêm com acento quebrado no export)"""
    for p in prefixos:
        for c in df.columns:
            if c.strip().lower().startswith(p.lower()):
                return c
    return None

def dt_col(s):
    return pd.to_datetime(s, format=FMT, errors="coerce")

def num(s):
    return pd.to_numeric(s.astype(str).str.replace(",", "", regex=False), errors="coerce")

def turno_txt(s):
    """'Turno 3' -> 3; '3' -> 3; vazio -> NaN"""
    return pd.to_numeric(s.astype(str).str.extract(r"(\d)")[0], errors="coerce")

def amostra(ids, n=5):
    ids = [str(i) for i in ids if str(i) != "nan"]
    ids = sorted(set(ids), key=lambda x: (len(x), x))
    return ", ".join(ids[:n]) + (f" … (+{len(ids)-n})" if len(ids) > n else "") if ids else "—"

ALIASES = RAIZ.parent / "Producao_GMS_x_MB51" / "dados" / "aliases_mangueira.csv"

def norm_material(desc):
    """'HOSE-AER, GH781, -6, R2/2SC' -> 'GH781-6' (cópia de Refugo/Refugo_por_Material/gms_dados.py, que não é importável daqui)"""
    m = re.match(r"HOSE-\w+,\s*([A-Z0-9]+),\s*-(\d+L?),", str(desc).strip())
    if not m: return str(desc).strip()
    fam, sz = m.groups()
    if sz.endswith("L"): sz = sz[:-1].zfill(2) + "L"
    elif fam.startswith("FC"): sz = sz.zfill(2)
    return f"{fam}-{sz}"

def aliases():
    try:
        a = pd.read_csv(ALIASES, sep=";", encoding="utf-8-sig", dtype=str)
        return {str(r.nome_gms).strip().upper(): str(r.material_sap).strip().upper() for r in a.itertuples()}
    except Exception:
        return {}

def norm_nome(s):
    s = str(s).upper().strip()
    s = re.sub(r"\s+", "", s)
    s = re.sub(r"[_\-]+", "", s)
    return s

R = []        # linhas do relatório
def h(t, n=2): R.append(f"\n{'#'*n} {t}\n")
def p(t=""): R.append(t)
def tab(cab, linhas):
    R.append("| " + " | ".join(cab) + " |"); R.append("|" + "---|" * len(cab))
    for l in linhas: R.append("| " + " | ".join(str(x) for x in l) + " |")
    R.append("")

# ------------------------------------------------------------------ carga
def carregar():
    D = {}
    D["ficha"] = lido(SRC / "ficha_producao.csv")
    D["insp"] = lido(SRC / "RegistrosInspeção.csv")
    D["erros"] = lido(SRC / "TiposErros.csv")
    D["mb51"] = pd.read_excel(SRC / "mb51.xlsx", dtype=str)
    D["pack"] = pd.read_excel(SRC / "BD Packing List.xlsx", dtype=str)
    return D

# ------------------------------------------------------------------ 0 inventário e pares
def inventario(D, hh):
    h("0. Fontes e pares duplicados")
    f, i, e, m, k = D["ficha"], D["insp"], D["erros"], D["mb51"], D["pack"]
    cf, ci, ce = col(f, "Created"), col(i, "DataHoraInspecao"), col(e, "Criado")
    linhas = []
    for nome, df, c in (("ficha_producao.csv", f, cf), ("RegistrosInspeção.csv", i, ci), ("TiposErros.csv", e, ce)):
        s = dt_col(df[c]); linhas.append([nome, len(df), s.min().date(), s.max().date(), (SRC / nome).stat().st_mtime and dt.datetime.fromtimestamp((SRC / nome).stat().st_mtime).date()])
    s = pd.to_datetime(m["Posting Date"], errors="coerce"); linhas.append(["mb51.xlsx (Sheet1)", len(m), s.min().date(), s.max().date(), dt.datetime.fromtimestamp((SRC / "mb51.xlsx").stat().st_mtime).date()])
    s = pd.to_datetime(k["Timestamp"], errors="coerce"); linhas.append(["BD Packing List.xlsx", len(k), s.min().date(), s.max().date(), dt.datetime.fromtimestamp((SRC / "BD Packing List.xlsx").stat().st_mtime).date()])
    if hh is not None: linhas.append(["Hora-Hora (--hh)", len(hh), "", "", ""])
    tab(["Arquivo", "Linhas", "Primeira data", "Última data", "Arquivo gravado em"], linhas)
    p("**Os exports são fotografias antigas:** a ficha vai só até 06/10, a inspeção e os erros até 02/10 e a MB51 até 21/10. "
      "A janela da NORMA (05 a 27/10) só está coberta de verdade na ficha por 05 e 06/10.")
    p("")
    p("**Pares `.txt` / `.csv` / `.xlsx`:** os `.txt` da pasta têm 190 a 260 bytes e guardam só o link do SharePoint; não há conteúdo "
      "para comparar. Pares com conteúdo de verdade: nenhum com `.csv` e `.xlsx` do mesmo nome. Único caso de dado repetido em dois "
      "arquivos: a MB51 está em `mb51.xlsx` (24/10) e na aba `MB51` da `Máscara de produção.xlsx` (06/10). Comparação abaixo.")
    # MB51 xlsx x aba MB51 da máscara
    try:
        a = pd.read_excel(SRC / "Máscara de produção.xlsx", sheet_name="MB51", dtype=str, header=0)
        a = a.dropna(subset=["Material Document"]);
        ka = set(zip(a["Material Document"], a["Material Doc.Item"]))
        kb = set(zip(m["Material Document"], m["Material Doc.Item"]))
        so_a, so_b = ka - kb, kb - ka
        da = pd.to_datetime(a["Posting Date"], errors="coerce")
        db_ = pd.to_datetime(m["Posting Date"], errors="coerce")
        tab(["Medida", "Valor"], [
            ["Itens na aba MB51 da Máscara (documento+item)", len(ka)], ["Itens no mb51.xlsx", len(kb)],
            ["Só na Máscara", len(so_a)], ["Só no mb51.xlsx", len(so_b)],
            ["Período da Máscara", f"{da.min().date()} a {da.max().date()}"], ["Período do mb51.xlsx", f"{db_.min().date()} a {db_.max().date()}"],
        ])
        # dos itens em comum, quantidade diferente?
        ca = a.set_index(["Material Document", "Material Doc.Item"])["Qty in unit of entry"]
        cb = m.set_index(["Material Document", "Material Doc.Item"])["Qty in unit of entry"]
        ca = ca[~ca.index.duplicated()]; cb = cb[~cb.index.duplicated()]
        comum = ca.index.intersection(cb.index)
        dif = (pd.to_numeric(ca[comum], errors="coerce").fillna(0) != pd.to_numeric(cb[comum], errors="coerce").fillna(0)).sum()
        p(f"Dos {len(comum)} itens em comum, **{dif}** têm quantidade diferente. "
          f"Conclusão: usar o `mb51.xlsx` (mais novo e {'mais completo' if len(kb) >= len(ka) else 'menor'}); a diferença é de período, não de conteúdo, se o número acima for 0.")
    except Exception as ex:
        p(f"Comparação da MB51 não executada: {type(ex).__name__}.")

# ------------------------------------------------------------------ 1 duplicados
def duplicados(D, hh):
    h("1. Duplicados")
    f, i, e, m, k = D["ficha"], D["insp"], D["erros"], D["mb51"], D["pack"]
    L = []
    def dup(nome, df, chave, idcol=None):
        d = df[df.duplicated(chave, keep=False) & df[chave[0]].notna()]
        grupos = d.groupby(chave, dropna=False).ngroups if len(d) else 0
        ids = d[idcol] if idcol and idcol in d else d[chave[0]]
        L.append([nome, "+".join(chave), grupos, len(d) - grupos, amostra(ids)])
    dup("ficha_producao", f, ["ID"]); dup("ficha_producao", f, ["OP"], "ID")
    cf_in = col(f, "data_hora_inicio_mandril")
    dup("RegistrosInspeção (linha inteira)", i, list(i.columns))
    dup("RegistrosInspeção (OP+hora+qtd+cabine)", i, ["OP_ID", "DataHoraInspecao", "Quantidade", "cabine_teste"])
    dup("TiposErros (linha inteira)", e, list(e.columns))
    dup("TiposErros (OP+código+qtd+criado)", e, ["OP_ID", "CodigoErro", "Quantidade", "Criado"])
    dup("MB51 (documento+item)", m, ["Material Document", "Material Doc.Item"], "Material Document")
    dup("Packing List (ID+Slice)", k, ["ID", "Slice"])
    p("Packing List: `ID` sozinho se repete por desenho (um ID tem várias fatias), por isso a chave é ID+Slice.")
    tab(["Fonte", "Chave", "Grupos repetidos", "Linhas a mais", "Amostra de IDs"], L)
    p("Linhas a mais = linhas que sobrariam se cada grupo ficasse com uma. OP_ID/Order são identificadores de ordem, não dado pessoal.")
    if hh is not None:
        hh_dup(hh)
    else:
        p("**Hora-Hora: NÃO EXECUTADO** (sem export local; ver seção 10).")

# ------------------------------------------------------------------ 2 vazios
def vazios(D, hh):
    h("2. Campos obrigatórios vazios")
    f, i, e, m, k = D["ficha"], D["insp"], D["erros"], D["mb51"], D["pack"]
    L = []
    def v(nome, df, cols, filtro=None, idc=None):
        x = df if filtro is None else df[filtro]
        for c in cols:
            if c is None: continue
            mask = x[c].isna() | (x[c].astype(str).str.strip() == "")
            L.append([nome, c.replace("�", "?"), len(x), int(mask.sum()), f"{100*mask.mean():.1f}%", amostra(x.loc[mask, idc]) if idc and mask.any() else "—"])
    fin = f["status_processo"].eq("Finalizado")
    v("ficha (todas)", f, ["OP", "Mangueira", "status_processo", "Bitola"], idc="ID")
    v("ficha (Finalizado)", f, [col(f, "data_hora_final_mandril"), col(f, "data_hora_final_trancadeira"), col(f, "data_hora_final_cobertura"),
                               col(f, "data_hora_final_vulcanizacao"), col(f, "data_hora_final_debandagem"), col(f, "data_hora_final_extracao"),
                               col(f, "quantidade_mandril"), col(f, "quantidade_extracao"), col(f, "Turno_mandril"), col(f, "Turno_Extr")], fin, "ID")
    ii = i.reset_index().rename(columns={"index": "linha"}); ii["linha"] = ii["linha"].astype(str)
    v("RegistrosInspeção", ii, ["OP_ID", "Quantidade", "DataHoraInspecao", "TurnoTeste", "Mangueira", "cabine_teste"], idc="linha")
    ee = e.reset_index().rename(columns={"index": "linha"}); ee["linha"] = ee["linha"].astype(str)
    v("TiposErros", ee, ["OP_ID", "CodigoErro", "Quantidade", "Criado", "DataHoraRefugo", "Turno Erro", col(e, "Tran")], idc="linha")
    v("MB51", m, ["Order", "Material", "Posting Date", "Quantity", "Unit of Entry", "User Name"], idc="Material Document")
    v("Packing List", k, ["PN", "QTd (m)", "Timestamp", "Cabine"], idc="ID")
    tab(["Fonte", "Campo", "Linhas", "Vazios", "%", "Amostra de IDs/linha"], L)
    p("Os campos de ficha só são obrigatórios na etapa já feita; `data_hora_final_*` e `quantidade_*` vazios em ficha Finalizado indicam etapa pulada "
      "ou ficha aberta direto numa etapa seguinte (a regra de quais etapas cada mangueira usa é a Fase 2). "
      "`TiposErros.DataHoraRefugo` vazio é antigo e não é erro (a data vale por `Criado`).")

# ------------------------------------------------------------------ 3 datas
ETAPAS = [("mandril", "Turno_mandril", "data_hora_inicio_mandril", "data_hora_final_mandril"),
          ("tubo", "Turno_Tubo", "data_hora_inicio_tubo", "data_hora_final_tubo"),
          ("trançagem", "Turno_Tran", "data_hora_inicio_trancadeira", "data_hora_final_trancadeira"),
          ("cobertura", "Turno_Cobertura", "data_hora_inicio_cobertura", "data_hora_final_cobertura"),
          ("bandagem", "Turno_Bandagem", "data_hora_inicio_bandagem", "data_hora_final_bandagem"),
          ("vulcanização", "Turno_Vulcan", "data_hora_inicio_vulcanizacao", "data_hora_final_vulcanizacao"),
          ("debandagem", "Turno_Debandagem", "data_hora_inicio_debandagem", "data_hora_final_debandagem"),
          ("extração/teste", "Turno_Extr", "data_hora_inicio_extracao", "data_hora_final_extracao")]

def etapas(f):
    out = []
    for nome, tc, ic, fc in ETAPAS:
        out.append((nome, col(f, tc), col(f, ic), col(f, fc), col(f, "quantidade_" + {"trançagem": "trancagem", "extração/teste": "extracao", "vulcanização": "vulcanizacao"}.get(nome, nome))))
    return out

def datas(D, hh):
    h("3. Datas impossíveis")
    f, i, e, m, k = D["ficha"], D["insp"], D["erros"], D["mb51"], D["pack"]
    L = []
    corte_min = pd.Timestamp("2025-11-01")   # a lista nasceu em 11/2025 (primeira data dos exports)
    hoje = pd.Timestamp(HOJE) + pd.Timedelta(days=1)
    def chk(nome, serie, ids, antigo=True):
        s = serie
        fut = s > hoje; ant = (s < corte_min) if antigo else (s < pd.Timestamp("2000-01-01")); inval = s.isna() & ids.notna() & (serie.index == serie.index)  # inválido tratado à parte
        L.append([nome, int(fut.sum()), int(ant.sum()), amostra(ids[fut | ant])])
    for nome, tc, ic, fc, qc in etapas(f):
        if ic and fc:
            a, b = dt_col(f[ic]), dt_col(f[fc])
            chk(f"ficha.{fc[:30]}", b, f["ID"])
            inv = (b < a)
            L.append([f"ficha: final antes do início ({nome})", int(inv.sum()), "—", amostra(f.loc[inv, "ID"])])
            longa = (b - a) > pd.Timedelta(days=7)
            L.append([f"ficha: etapa com mais de 7 dias ({nome})", int(longa.sum()), "—", amostra(f.loc[longa, "ID"])])
    ci = col(i, "DataHoraInspecao"); chk("inspeção.DataHoraInspecao", dt_col(i[ci]), i.index.to_series().astype(str))
    ce = col(e, "Criado"); chk("TiposErros.Criado", dt_col(e[ce]), e.index.to_series().astype(str))
    pm = pd.to_datetime(m["Posting Date"], errors="coerce"); chk("MB51.Posting Date (antes de 2000 em vez de 11/2025: a MB51 começa em 11/2024)", pm, m["Material Document"], antigo=False)
    pk = pd.to_datetime(k["Timestamp"], errors="coerce"); chk("PackingList.Timestamp", pk, k["ID"])
    # data não interpretável
    nao = [["ficha (Created)", int(dt_col(f["Created"]).isna().sum())], ["inspeção", int(dt_col(i[ci]).isna().sum())], ["TiposErros.Criado", int(dt_col(e[ce]).isna().sum())]]
    tab(["Verificação", "Futuras / fim<início / longas", "Antes de 11/2025", "Amostra de IDs"], L)
    p("Datas que não viram data (não preenchem o formato `MM/DD/AAAA h:mm AM/PM`): " + "; ".join(f"{a} = {b}" for a, b in nao) + ".")
    p("`data_ref` fora do dia produtivo de 05:20 só existe na Hora-Hora (`field_0` x `Title` x hora de criação): " + ("ver seção 10." if hh is not None else "**NÃO EXECUTADO** (sem export)."))

# ------------------------------------------------------------------ 4 turno
def turno(D, hh):
    h("4. Turno x horário (NORMA de 27/10, MEL-250: T1 320–836, T2 837–1339, T3 1340–319)")
    f, i, e = D["ficha"], D["insp"], D["erros"]
    L, janela = [], []
    def aval(nome, ids, t_reg, ts, ts2=None):
        ok = ts.notna() & t_reg.notna()
        esp = ts[ok].map(lambda x: turno_norma(minuto(x)))
        reg = t_reg[ok].astype(int)
        dif = esp != reg
        dia = ts[ok].map(lambda x: dia_produtivo(x))
        m_ = (reg == 2) & (esp == 3)
        j = m_ & (ts[ok].map(minuto).between(1340, 1360)) & (dia.map(lambda d: NORMA_INI <= d <= NORMA_FIM))
        # formato "Turno 3" vs "3" será visto à parte
        if ts2 is not None:      # também confere contra o INÍCIO da etapa: só conta erro se não bate com nenhum dos dois
            t2 = ts2[ok]
            esp2 = t2.map(lambda x: turno_norma(minuto(x)) if pd.notna(x) else -1)
            ambos = int(((esp != reg) & (esp2 != reg)).sum())
        else:
            ambos = "—"
        L.append([nome, int(ok.sum()), int(dif.sum()), ambos, int(m_.sum()), int(j.sum()), amostra(ids[ok][j])])
        return int(j.sum())
    n_ficha = 0
    for nome, tc, ic, fc, qc in etapas(f):
        if not (tc and fc): continue
        t = turno_txt(f[tc]); ts = dt_col(f[fc])
        n_ficha += aval(f"ficha {nome}", f["ID"], t, ts, dt_col(f[ic]) if ic else None)
    p("`Turno` do registro x turno que a NORMA dá ao horário do FIM da etapa (`data_hora_final_*`). Coluna \"T2 em 22:20–22:40\" = registro T2 com horário entre 22:20 e 22:40 e data de 05 a 27/10.")
    # inspeção e erros
    aval("inspeção (TurnoTeste x DataHoraInspecao)", i.index.to_series().astype(str), turno_txt(i["TurnoTeste"]), dt_col(i["DataHoraInspecao"]))
    ce = col(e, "Criado")
    aval("TiposErros (Turno Erro x Criado)", e.index.to_series().astype(str), turno_txt(e["Turno Erro"]), dt_col(e[ce]))
    tab(["Origem", "Com turno e hora", "Turno ≠ NORMA no fim", "≠ no fim e no início", "Registrado T2 mas NORMA diz T3", "T2 em 22:20–22:40 (05–27/10)", "Amostra de IDs"], L)
    p(f"**Aceite:** esperado 46 fins de etapa da ficha com T2 entre 22:20 e 22:40 de 05 a 27/10 (contagem de 29/10 na lista viva). "
      f"Neste export (ficha até 06/10) deu **{n_ficha}**. **ACEITE NÃO ATINGIDO.** Provável causa: o arquivo termina em 06/10 (só 05 e 06/10 dentro da janela), mas isso não está provado. "
      f"Para reproduzir 46 é preciso um export novo da `ficha_producao`. "
      f"Os 146 da Hora-Hora não dá para conferir: o export da Hora-Hora não está na pasta (seção 10).")
    # formatos de turno
    F = collections.Counter()
    for nome, tc, ic, fc, qc in etapas(f):
        if tc:
            for v_ in f[tc].dropna().unique(): F[("ficha", v_)] += int((f[tc] == v_).sum())
    fmt = {}
    for (src, v_), n in F.items():
        k_ = "texto 'Turno N'" if str(v_).startswith("Turno") else "número N"
        fmt[k_] = fmt.get(k_, 0) + n
    p(f"Formato do campo turno na ficha: {fmt}. Mistura de `3` e `Turno 3` para o mesmo valor; a limpeza da Fase 3 normaliza para `N`.")
    # fronteiras por período: quantos registros em cada faixa de horário, por turno gravado
    acc = collections.defaultdict(lambda: [0, 0, 0, 0])
    for nome, tc, ic, fc, qc in etapas(f):
        if not (tc and fc): continue
        t = turno_txt(f[tc]); ts = dt_col(f[fc]); ok = ts.notna() & t.notna()
        mins = ts[ok].map(minuto); reg = t[ok].astype(int); dia = ts[ok].map(lambda x: dia_produtivo(x))
        per = dia.map(lambda d: "antes de 05/10" if d < NORMA_INI else ("05 a 27/10" if d <= NORMA_FIM else "depois de 27/10"))
        for lab, a, b in (("13:47–13:56", 827, 836), ("22:20–22:40", 1340, 1360)):
            for pr in ("antes de 05/10", "05 a 27/10", "depois de 27/10"):
                sel = mins.between(a, b) & (per == pr)
                r = acc[(lab, pr)]; r[0] += int(sel.sum())
                for tt in (1, 2, 3): r[tt] += int((sel & (reg == tt)).sum())
    tab(["Faixa de horário (fim da etapa, ficha)", "Período", "Registros", "Gravados T1", "Gravados T2", "Gravados T3"],
        [[k_[0], k_[1], v_[0], v_[1], v_[2], v_[3]] for k_, v_ in sorted(acc.items())])
    p("Leitura: em 13:47–13:56 a NORMA dá T1; em 22:20–22:40 dá T3. Antes de 05/10 a regra do app já era outra para 13:47 (T2 a partir de 13:47) mas, "
      "segundo o glossário, a virada para T3 era 22:20; então os registros T2 em 22:20–22:40 antes de 05/10 também divergem da NORMA e NÃO se pode dizer que \"só 05 a 27/10 precisa de correção\": "
      "se os registros anteriores a 05/10 entram na correção é decisão do William. A janela 05 a 27/10 está fixa no script (o glossário fala em \"~29/10\" para a volta; data real a confirmar). "
      "O fim da etapa vale como horário de turno só onde o app gravava o turno no fim (app atual); no histórico, parte das divergências (mandril, tubo, cobertura: 26 a 44% não batem nem com início nem com fim) "
      "tem outra causa que este diagnóstico não explica, e não há tabela de divergência total por período. Os campos Qtd_Turno1/2/3 da ficha não foram conferidos.")

# ------------------------------------------------------------------ 5 lacunas
def lacunas(D, hh):
    h("5. Lacunas (dias sem registro por máquina)")
    f, i, e = D["ficha"], D["insp"], D["erros"]
    def lac(nome, serie_maq, serie_data):
        df = pd.DataFrame({"m": serie_maq.astype(str).str.upper().str.strip(), "d": serie_data.dt.date}).dropna()
        df = df[df.m != "NAN"]
        total = df.groupby("d").size()
        if total.empty: return []
        med = total.median()
        uteis = set(total[total >= 0.4 * med].index)     # dias em que a fábrica registrou o normal (descarta fim de semana/parada)
        out = []
        for maq, g in df.groupby("m"):
            dias = set(g.d); ini, fim = min(dias), max(dias)
            if len(g) < 30: continue
            esperados = [d for d in uteis if ini <= d <= fim]
            falt = sorted(d for d in esperados if d not in dias)
            out.append([nome, maq, f"{ini} a {fim}", len(esperados), len(falt), ", ".join(str(x) for x in falt[:4]) + (" …" if len(falt) > 4 else "")])
        return out
    L = []
    ct = col(f, "Tran")   # trançadeira
    L += lac("ficha (fim trançagem)", f[ct], dt_col(f[col(f, "data_hora_final_trancadeira")]))
    L += lac("ficha (fim mandril)", f[col(f, "maquina_mandril")], dt_col(f[col(f, "data_hora_final_mandril")]))
    L += lac("inspeção (cabine)", i["cabine_teste"], dt_col(i["DataHoraInspecao"]))
    tab(["Fonte", "Máquina", "Período da máquina", "Dias úteis esperados", "Dias sem registro", "Primeiros dias sem registro"], L)
    p("Dia útil = dia em que a fábrica toda lançou pelo menos 40% da mediana diária; lacuna = dia útil dentro do período da máquina em que ela não lançou nada. "
      "Máquina que parou por manutenção também aparece aqui; é lacuna a registrar, nunca dado a inventar. "
      "Mandril por máquina usa só o fim de etapa. Lacunas da Hora-Hora (janelas faltando por célula e turno): " + ("seção 10." if hh is not None else "**NÃO EXECUTADO**."))

# ------------------------------------------------------------------ 6 OP x MB51
def op_mb51(D):
    h("6. OP do GMS que não existe na MB51")
    f, i, e, m = D["ficha"], D["insp"], D["erros"], D["mb51"]
    mo = set(m["Order"].dropna().astype(str).str.strip())
    pmax = pd.to_datetime(m["Posting Date"], errors="coerce").max()
    pmin_ordens = pd.to_datetime(m["Posting Date"], errors="coerce").min()
    p(f"MB51 do arquivo vai de {pmin_ordens.date()} a {pmax.date()}; {len(mo)} ordens distintas. OP do GMS sem ordem na MB51 só é falha de dado "
      f"depois que o SAP lança, então a conta exclui fichas Canceladas e fichas criadas depois de {(pmax - pd.Timedelta(days=15)).date()}.")
    L = []
    fc = f[(f["status_processo"] != "Cancelado") & f["OP"].notna()].copy()
    fc["cre"] = dt_col(fc["Created"])
    fc = fc[fc.cre <= pmax - pd.Timedelta(days=15)]
    fc["OPn"] = fc["OP"].astype(str).str.strip()
    sem = fc[~fc["OPn"].isin(mo)]
    L.append(["ficha (OP)", fc["OPn"].nunique(), sem["OPn"].nunique(), f"{100*sem['OPn'].nunique()/max(fc['OPn'].nunique(),1):.1f}%", amostra(sem["ID"])])
    ii = i.copy(); ii["cre"] = dt_col(ii["DataHoraInspecao"]); ii = ii[ii.cre <= pmax - pd.Timedelta(days=15)]
    ii["OPn"] = ii["OP_ID"].astype(str).str.strip()
    sem_i = ii[~ii["OPn"].isin(mo) & ii["OP_ID"].notna()]
    L.append(["inspeção (OP_ID)", ii["OPn"].nunique(), sem_i["OPn"].nunique(), f"{100*sem_i['OPn'].nunique()/max(ii['OPn'].nunique(),1):.1f}%", amostra(sem_i["OPn"])])
    ee = e.copy(); ee["cre"] = dt_col(ee["Criado"]); ee = ee[ee.cre <= pmax - pd.Timedelta(days=15)]
    ee["OPn"] = ee["OP_ID"].astype(str).str.strip()
    sem_e = ee[~ee["OPn"].isin(mo) & ee["OP_ID"].notna()]
    L.append(["TiposErros (OP_ID)", ee["OPn"].nunique(), sem_e["OPn"].nunique(), f"{100*sem_e['OPn'].nunique()/max(ee['OPn'].nunique(),1):.1f}%", amostra(sem_e["OPn"])])
    tab(["Origem", "OPs avaliadas", "OPs sem ordem na MB51", "%", "Amostra"], L)
    # por mês
    sem["mes"] = sem.cre.dt.to_period("M").astype(str)
    mes = sem.groupby("mes")["OPn"].nunique()
    base = fc.assign(mes=fc.cre.dt.to_period("M").astype(str)).groupby("mes")["OPn"].nunique()
    tab(["Mês de criação da ficha", "OPs", "Sem MB51", "%"], [[k_, int(base[k_]), int(mes.get(k_, 0)), f"{100*mes.get(k_,0)/base[k_]:.0f}%"] for k_ in base.index])
    p("Se o percentual por mês for alto só nos meses antigos, a MB51 exportada não cobre o período (a MB51 vai de 11/2024, mas só traz ordens com lançamento). "
      "A conferência fina (casar nome da mangueira por OP) é a seção 9.")

# ------------------------------------------------------------------ 7 faixas
def faixas(D):
    h("7. Unidades e valores fora de faixa")
    f, i, e, m, k = D["ficha"], D["insp"], D["erros"], D["mb51"], D["pack"]
    L = []
    def faixa(nome, serie, ids, teto=None):
        n = num(serie)
        nao = serie.notna() & n.isna()
        neg = n < 0; zero = n == 0
        q1, q3 = n.quantile(.25), n.quantile(.75); iqr = q3 - q1
        alto = n > (q3 + 6 * iqr) if iqr > 0 else n > n.quantile(.999)
        if teto is not None: alto = alto | (n > teto)
        L.append([nome, int(n.notna().sum()), int(nao.sum()), int(neg.sum()), int(zero.sum()), int(alto.sum()), f"{n.min():g} … {n.max():g}", amostra(ids[nao | neg | alto])])
    for nome, tc, ic, fc, qc in etapas(f):
        if qc: faixa(f"ficha.{qc}", f[qc], f["ID"])
    ix = i.index.to_series().astype(str)
    faixa("inspeção.Quantidade", i["Quantidade"], ix)
    for c in ("Diametro_Interno", "Diametro_Externo", "Concentricidade"): faixa(f"inspeção.{c}", i[c], ix)
    faixa("TiposErros.Quantidade", e["Quantidade"], e.index.to_series().astype(str))
    faixa("PackingList.QTd (m)", k["QTd (m)"], k["ID"])
    faixa("PackingList.ID Total Length (m)", k["ID Total Length (m)"], k["ID"])
    tab(["Campo", "Válidos", "Não numéricos", "Negativos", "Zeros", "Muito acima (cerca de 6×IQR)", "Faixa", "Amostra de IDs"], L)
    p("\"Muito acima\" é heurística estatística (Q3 + 6×IQR); não é limite de negócio. Os limites reais (comprimento máximo de lance, diâmetro por mangueira) saem do DM_* e são decisão da Fase 2.")
    # MB51: unidade x movimento x sinal
    u = m.groupby(["Unit of Entry", "Movement type"]).size()
    qn = pd.to_numeric(m["Qty in unit of entry"], errors="coerce")
    sinal = [["101 com quantidade ≤ 0", int(((m["Movement type"] == "101") & (qn <= 0)).sum())],
             ["102 com quantidade > 0", int(((m["Movement type"] == "102") & (qn > 0)).sum())],
             ["Unidade diferente de M, PC, KG", int((~m["Unit of Entry"].isin(["M", "PC", "KG"])).sum())],
             ["Unidade vazia", int(m["Unit of Entry"].isna().sum())]]
    tab(["MB51: verificação", "Linhas"], sinal)
    p("MB51 por unidade e movimento: " + "; ".join(f"{a}/{b} = {n}" for (a, b), n in u.items()) + ". Metros de mangueira = só unidade `M`.")
    # extração acima da debandagem (informativo)
    qe, qd = num(f[col(f, "quantidade_extracao")]), num(f[col(f, "quantidade_debandagem")])
    x = (qe > qd * 1.0) & qd.notna()
    p(f"Extração maior que a debandagem: {int(x.sum())} fichas (amostra de IDs: {amostra(f.loc[x,'ID'])}). Não é erro por si (COMO_USAR_OS_DADOS §4); fica só como informação.")

# ------------------------------------------------------------------ 8 nomes
def nomes(D):
    h("8. Nomes de máquina e mangueira escritos de jeitos diferentes")
    f, i, e, m = D["ficha"], D["insp"], D["erros"], D["mb51"]
    def grupos(nome, serie):
        s = serie.dropna().astype(str).str.strip()
        s = s[s != ""]
        cont = s.value_counts()
        g = collections.defaultdict(list)
        for v_, n in cont.items(): g[norm_nome(v_)].append((v_, n))
        multi = {k_: v_ for k_, v_ in g.items() if len(v_) > 1}
        return len(cont), multi
    L = []
    for nome, serie in (("Mangueira (ficha)", f["Mangueira"]), ("Mangueira (inspeção)", i["Mangueira"]), ("Trançadeira (ficha)", f[col(f, "Tran")]),
                        ("Trançadeira (inspeção)", i[col(i, "Tran")]), ("Trançadeira (TiposErros)", e[col(e, "Tran")]),
                        ("maquina_mandril (ficha)", f["maquina_mandril"]), ("cabine_teste (inspeção)", i["cabine_teste"])):
        n, multi = grupos(nome, serie)
        ex = "; ".join("/".join(f"{a}({b})" for a, b in v_) for v_ in list(multi.values())[:6])
        L.append([nome, n, len(multi), ex or "—"])
    tab(["Campo", "Valores distintos", "Grupos com mais de uma grafia", "Exemplos (grafia(contagem))"], L)
    p("Grupo = mesmo texto depois de maiúscula, espaços, `-` e `_` removidos. Grafias que diferem de outro jeito (`GH781-6-2` x `GH781-6`, `TO04` x `TO-04`, "
      "`-N` de sufixo) ficam para a tabela de equivalência da Fase 2.")
    # nomes de mangueira da ficha que o SAP não conhece, por descrição normalizada
    desc = set(m["Material Description"].dropna().map(norm_nome))
    nomesf = f["Mangueira"].dropna().astype(str).str.strip().unique()
    sem = [n for n in nomesf if not any(norm_nome(n) in d for d in desc)]
    p(f"Mangueiras da ficha (distintas: {len(nomesf)}) cujo nome não aparece em nenhuma `Material Description` da MB51 (busca por contém, normalizada): "
      f"**{len(sem)}**. Lista: {', '.join(sorted(sem)[:15])}{' …' if len(sem) > 15 else ''}. É o caso conhecido de nome do GMS diferente do SAP; liga-se pela OP (seção 9).")

# ------------------------------------------------------------------ 9 GMS x MB51
def gms_x_sap(D):
    h("9. Divergência GMS x MB51 por OP (SAP é a verdade)")
    f, i, e, m = D["ficha"], D["insp"], D["erros"], D["mb51"]
    q = pd.to_numeric(m["Qty in unit of entry"], errors="coerce")
    m = m.assign(q=q, d=pd.to_datetime(m["Posting Date"], errors="coerce"), mov=m["Movement type"])
    mm = m[(m["Unit of Entry"] == "M") & m.mov.isin(["101", "102"]) & m.Order.notna()]
    ref = mm["User Name"].isin(USUARIOS_REFUGO)
    sinal = mm.mov.map({"101": 1, "102": -1})
    # q já vem com sinal? confere
    neg102 = int(((mm.mov == "102") & (mm.q < 0)).sum()); pos102 = int(((mm.mov == "102") & (mm.q > 0)).sum())
    if neg102 > pos102: sinal = 1                      # 102 já vem negativo
    sap_boa = mm[~ref].assign(v=mm[~ref].q * (mm[~ref].mov.map({"101": 1, "102": -1}) if neg102 <= pos102 else 1)).groupby("Order")["v"].sum()
    sap_ref = mm[ref].assign(v=mm[ref].q * (mm[ref].mov.map({"101": 1, "102": -1}) if neg102 <= pos102 else 1)).groupby("Order")["v"].sum()
    mat = mm.groupby("Order")["Material Description"].first().map(norm_nome)
    last = mm.groupby("Order")["d"].max()
    gms_boa = num(i["Quantidade"]).groupby(i["OP_ID"].astype(str).str.strip()).sum()
    gms_ref = num(e["Quantidade"]).groupby(e["OP_ID"].astype(str).str.strip()).sum()
    di = dt_col(i["DataHoraInspecao"]); de = dt_col(e["Criado"])
    p(f"Período em comum entre GMS e SAP: GMS (inspeção/erros) vai até {max(di.max(), de.max()).date()}; MB51 até {m.d.max().date()}. "
      f"Só entram OPs que existem nos dois lados e cujo último lançamento SAP é até {max(di.max(), de.max()).date()}. "
      f"Boa = 101 − 102 sem os usuários de refugo; refugo = lançamentos dos usuários de refugo. Metros, tolerância 1 m. "
      f"Convenção: variação = SAP − GMS (negativa = faltou lançar no SAP; positiva = sobrou no SAP).")
    teto = max(di.max(), de.max())
    L = []
    for nome, sap, gms in (("Produção boa", sap_boa, gms_boa), ("Refugo", sap_ref, gms_ref)):
        ops = sorted(set(sap.index) & set(gms.index))
        ops = [o for o in ops if last.get(o, pd.NaT) <= teto]
        var = pd.Series({o: sap[o] - gms[o] for o in ops})
        fal, sob = var[var < -1], var[var > 1]
        # faltou e sobrou somados por material, nunca entre materiais
        mat_ops = pd.Series({o: mat.get(o, "?") for o in ops})
        fal_m = fal.groupby(mat_ops[fal.index]).sum(); sob_m = sob.groupby(mat_ops[sob.index]).sum()
        L.append([nome, len(ops), int((var.abs() <= 1).sum()), len(fal), f"{fal.sum():.0f}", len(sob), f"{sob.sum():.0f}", f"{len(fal_m)} / {len(sob_m)}", amostra(var.abs().sort_values(ascending=False).index[:5], 5)])
    tab(["Medida", "OPs nos dois lados", "Dentro de 1 m", "OPs que faltou", "Faltou (m)", "OPs que sobrou", "Sobrou (m)", "Materiais com falta / com sobra", "OPs de maior variação (IDs)"], L)
    p("Faltou e sobrou NÃO se compensam entre materiais (regra do COMO_USAR_OS_DADOS §3): os totais acima ficam separados e a coluna de materiais conta onde cada um ocorre. "
      "Compensação só dentro do mesmo material, e troca de OP entre OPs vizinhas do mesmo material é costume da fábrica (Fase 2 decide). "
      "OP que existe só num lado está na seção 6.")
    # mangueira do GMS x material da OP no SAP (nome do SAP normalizado como em gms_dados.norm_material)
    al = aliases()
    matsap = mm.groupby("Order")["Material Description"].first().map(lambda x: norm_material(x).upper())
    fa = f.dropna(subset=["OP", "Mangueira"]).copy(); fa["OPn"] = fa["OP"].astype(str).str.strip()
    fa = fa[fa.OPn.isin(set(matsap.index))]
    fa["g"] = fa.Mangueira.astype(str).str.strip().str.upper(); fa["s"] = fa.OPn.map(matsap)
    igual = fa.g == fa.s
    alias = ~igual & (fa.g.map(lambda x: al.get(x, "")) == fa.s)
    resto = fa[~igual & ~alias]
    por_par = resto.groupby(["g", "s"]).size().sort_values(ascending=False)
    p(f"Mangueira da ficha x material da mesma OP no SAP ({len(fa)} fichas com OP nos dois lados): igual = **{int(igual.sum())}**; "
      f"alias já conhecido em `aliases_mangueira.csv` = **{int(alias.sum())}**; **diverge = {len(resto)}** em {por_par.size} pares distintos "
      f"(IDs de ficha: {amostra(resto['ID'])}). Pares que mais se repetem (GMS → SAP, fichas): "
      + "; ".join(f"{a}→{b} ({n})" for (a, b), n in por_par.head(8).items()) + ". "
      "Parte desses é alias novo (grafia do mesmo material, ex.: sufixo `-2`); parte é divergência real de OP. A Fase 2 separa as duas.")

# ------------------------------------------------------------------ 10 Hora-Hora
def hh_dup(hh):
    chave = [c for c in ("field_0", "TurnoH", "field_2", "field_3") if c in hh.columns]
    d = hh[hh.duplicated(chave, keep=False)]
    g = d.groupby(chave).ngroups if len(d) else 0
    p(f"Hora-Hora duplicados (data+turno+célula+hora): {g} grupos, {len(d)-g} linhas a mais, IDs: {amostra(d['ID'])}.")

def horahora(hh):
    h("10. Hora-Hora")
    if hh is None:
        p("**NÃO EXECUTADO.** A lista Hora-Hora não tem export na pasta `Sharepoint Data GMS` (os backups de 16/10 foram só para outra pasta do PC e "
          "não estão no repositório). As verificações abaixo foram escritas e ficam prontas para rodar com `--hh <csv>`:")
        p("- duplicados por data+turno+célula+hora; campos vazios; `Title` x `field_0`/`field_2`;")
        p("- turno x janela: `TurnoH` = 2º e `field_3` = `22:00 - 22:20` (41 min) na `field_0` de 05 a 27/10 → alvo 146 linhas (referência do diário de 29/10, não lida aqui: IDs 28835 a 31767, todas Finalizado). Atenção: a janela de 41 min mistura 20 min de T2 (22:00–22:19) e 21 de T3; trocar o `TurnoH` da linha inteira move produção de T2 para T3 e o Tempo Parado foi calculado sobre 41 min (MEL-255) — a Fase 2 precisa de regra de divisão ou marca 'a conferir';")
        p("- lacunas por célula e janela do turno; Tempo Parado > Minutos; Real/Meta fora de faixa.")
        p("Para obter o export: o William exporta a lista no SharePoint (CSV) ou autoriza uma leitura por navegador logado que grave direto em arquivo local "
          "(o conteúdo não deve passar por agentes: só contagens e IDs).")
        return
    h2 = hh.copy()
    ds = pd.to_datetime(h2["field_0"], errors="coerce")
    j = (h2["TurnoH"].astype(str).str.startswith("2")) & (h2["field_3"].astype(str).str.replace(" ", "").isin(["22:00-22:20"])) & (ds.dt.date >= NORMA_INI) & (ds.dt.date <= NORMA_FIM)
    p(f"T2 em 22:00–22:20 (41 min) de 05 a 27/10: **{int(j.sum())}** (esperado 146). IDs: {amostra(h2.loc[j,'ID'])}.")
    if "Minutos" in h2:
        mm = pd.to_numeric(h2["Minutos"], errors="coerce"); pa = pd.to_numeric(h2.get("field_11"), errors="coerce")
        x = pa > mm
        p(f"Tempo Parado maior que os minutos da janela: {int(x.sum())} (IDs: {amostra(h2.loc[x,'ID'])}). Lembrete: o Tempo Parado do Hora-Hora é calculado pelo sistema (MEL-255); não é parada real.")

# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hh", help="CSV exportado da lista Hora-Hora (opcional)")
    ap.add_argument("--data", default=HOJE.isoformat())
    a = ap.parse_args()
    hh = lido(a.hh) if a.hh else None
    D = carregar()
    R.append(f"# Diagnóstico do GMS — Fase 1 (só leitura) · {a.data}\n")
    p("Gerado por `diagnostico_gms.py` (nesta pasta). **Só contagens e IDs de amostra; nenhuma linha de produção.** Nada foi gravado no SharePoint nem em `GMS/IA/dados`. "
      "Plano: `PLANO.md`. Regras de turno: NORMA de 27/10/2026 (MEL-250).")
    for fn, args in ((inventario, (D, hh)), (duplicados, (D, hh)), (vazios, (D, hh)), (datas, (D, hh)), (turno, (D, hh)),
                     (lacunas, (D, hh)), (op_mb51, (D,)), (faixas, (D,)), (nomes, (D,)), (gms_x_sap, (D,)), (horahora, (hh,))):
        try:
            fn(*args)
        except Exception as ex:
            h(f"ERRO em {fn.__name__}")
            p(f"`{type(ex).__name__}: {ex}`")
            print("erro", fn.__name__, repr(ex), file=sys.stderr)
    destino = OUT / f"Diagnostico_{a.data}.md"
    destino.write_text("\n".join(R) + "\n", encoding="utf-8")
    print("gravado", destino)

if __name__ == "__main__":
    main()
