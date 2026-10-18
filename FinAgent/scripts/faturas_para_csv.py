"""Converte faturas PDF do cartão Mercado Pago em CSV no formato do extrato do app.

Uso: python -I faturas_para_csv.py <saida.csv> <fatura1.pdf> [<fatura2.pdf> ...]
Requer `pdftotext` (poppler) no PATH. Roda só no computador; o CSV tem dados pessoais
e NÃO deve ir para o git. Mostra no terminal a conferência da soma por fatura.

Pode rodar só com a fatura nova: cada linha leva o mês da fatura na referência, então o app
soma ao que já tem sem duplicar. Créditos/estornos ("Crédito concedido", "Estorno"...) viram uma linha
positiva ligada à compra de mesmo valor da mesma fatura; sem compra correspondente o script avisa.
"""
import re
import subprocess
import sys
from datetime import date

LINHA = re.compile(r"^(\d{2})/(\d{2}) (.+?) R\$ ([\d.]+,\d{2})$")
CONSUMOS = re.compile(r"Consumos de (\d{2})/(\d{2}) a (\d{2})/(\d{2}) R\$ ([\d.]+,\d{2})")
EMITIDA = re.compile(r"Emitid[ao] em: \d{2}/(\d{2})/(\d{4})")
CREDITO = re.compile(r"^(Crédito|Estorno|Reembolso|Devolução)", re.I)
PREFIXO = "Pagamento com cartão Visa "  # sem 'fatura': o app não confunde com pagamento de fatura
PREFIXO_ESTORNO = "Estorno cartão Visa "


def num(s):
    return round(float(s.replace(".", "").replace(",", ".")), 2)


def texto(pdf):
    return subprocess.run(
        ["pdftotext", "-raw", "-enc", "UTF-8", pdf, "-"], capture_output=True, text=True, encoding="utf-8", check=True
    ).stdout


def ler_fatura(pdf):
    """Devolve (compras, creditos, total_consumos); cada item é (data_iso, descricao, valor, mes_da_fatura)."""
    t = texto(pdf)
    emitida = EMITIDA.search(t)
    consumos = CONSUMOS.search(t)
    if not emitida or not consumos:
        raise SystemExit(f"{pdf}: cabeçalho da fatura não reconhecido")
    mes_em, ano_em = int(emitida.group(1)), int(emitida.group(2))
    total = num(consumos.group(5))
    compras, creditos = [], []
    for linha in t.splitlines():
        m = LINHA.match(linha.strip())
        if not m or "Pagamento da fatura" in m.group(3):
            continue
        dia, mes = int(m.group(1)), int(m.group(2))
        ano = ano_em - 1 if mes > mes_em else ano_em  # compra de dez em fatura de jan
        item = (date(ano, mes, dia).isoformat(), m.group(3).strip(), num(m.group(4)), f"{ano_em}-{mes_em:02d}")
        (creditos if CREDITO.match(item[1]) else compras).append(item)
    return compras, creditos, total


def linhas_do_csv(compras, creditos):
    """Linhas (data, tipo, valor, ref). A ref da compra é estável; o estorno repete a ref da compra anulada."""
    vistos, pagas, linhas, orfaos = {}, {}, [], {}
    for d, nome, v, fat in compras:
        k = (fat, d, nome, v)
        vistos[k] = vistos.get(k, 0) + 1  # ref estável (inclui o mês da fatura): reimportar não duplica nem perde
        ref = f"CARTAO-{fat}-{d}-{v:.2f}-{vistos[k]}"
        linhas.append((d, PREFIXO + nome, -v, ref))
        pagas[ref] = (fat, d, nome, v, False)  # ref -> compra, ainda sem estorno
    avisos = []
    for d, desc, v, fat in creditos:
        livres = [r for r, (f, _, _, vv, usada) in pagas.items() if f == fat and vv == v and not usada]
        mesmo_dia = [r for r in livres if pagas[r][1] == d]
        candidatas = mesmo_dia or livres
        escolhida = (candidatas or [None])[0]
        if len({pagas[r][2] for r in candidatas}) > 1:
            avisos.append(f"crédito {d} {v:.2f}: mais de uma compra de mesmo valor ({', '.join(sorted({pagas[r][2] for r in candidatas}))}); anulei a primeira, confira")
        if escolhida is None:
            avisos.append(f"crédito sem compra correspondente: {d} {desc} {v:.2f} (fatura {fat}); fica de fora dos totais")
            orfaos[(fat, d, v)] = orfaos.get((fat, d, v), 0) + 1  # ref única mesmo com dois créditos iguais no dia
            linhas.append((d, PREFIXO_ESTORNO + desc, v, f"CARTAO-{fat}-{d}-{v:.2f}-E{orfaos[(fat, d, v)]}"))
            continue
        f, _, nome, vv, _ = pagas[escolhida]
        pagas[escolhida] = (f, pagas[escolhida][1], nome, vv, True)
        linhas.append((d, PREFIXO_ESTORNO + nome, v, escolhida))
    return linhas, avisos


def main():
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    saida, pdfs = sys.argv[1], sys.argv[2:]
    compras_todas, creditos_todos, ok = [], [], True
    for pdf in pdfs:
        compras, creditos, total = ler_fatura(pdf)
        soma = round(sum(c[2] for c in compras), 2)
        marca = "OK " if abs(soma - total) < 0.005 else "DIVERGE"
        ok &= marca == "OK "
        extra = f", {len(creditos)} crédito(s) {sum(c[2] for c in creditos):.2f}" if creditos else ""
        print(f"{marca} {pdf.split('/')[-1].split(chr(92))[-1]}: {len(compras)} compras, soma {soma:.2f} x fatura {total:.2f}{extra}")
        compras_todas += compras
        creditos_todos += creditos
    linhas, avisos = linhas_do_csv(compras_todas, creditos_todos)
    linhas.sort(key=lambda x: x[0])  # ordem crescente; saldo 0 em todas (não é conta)
    with open(saida, "w", encoding="utf-8", newline="") as f:
        f.write("RELEASE_DATE;TRANSACTION_TYPE;REFERENCE_ID;TRANSACTION_NET_AMOUNT;PARTIAL_BALANCE\n")
        for d, tipo, valor, ref in linhas:
            a, m_, dia = d.split("-")
            valor_txt = f"{valor:.2f}".replace(".", ",")
            f.write(f"{dia}-{m_}-{a};{tipo};{ref};{valor_txt};0,00\n")
    print(f"{len(linhas)} linhas -> {saida}")
    for a in avisos:
        print("AVISO:", a)
    if not ok:
        raise SystemExit("Alguma soma não bate: confira antes de importar.")


main()
