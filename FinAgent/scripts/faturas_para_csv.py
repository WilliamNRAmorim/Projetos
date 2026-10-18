"""Converte faturas PDF do cartão Mercado Pago em CSV no formato do extrato do app.

Uso: python -I faturas_para_csv.py <saida.csv> <fatura1.pdf> [<fatura2.pdf> ...]
Requer `pdftotext` (poppler) no PATH. Roda só no computador; o CSV tem dados pessoais
e NÃO deve ir para o git. Mostra no terminal a conferência da soma por fatura.
"""
import re
import subprocess
import sys
from datetime import date

LINHA = re.compile(r"^(\d{2})/(\d{2}) (.+?) R\$ ([\d.]+,\d{2})$")
CONSUMOS = re.compile(r"Consumos de (\d{2})/(\d{2}) a (\d{2})/(\d{2}) R\$ ([\d.]+,\d{2})")
EMITIDA = re.compile(r"Emitid[ao] em: \d{2}/(\d{2})/(\d{4})")
PREFIXO = "Pagamento com cartão Visa "  # sem 'fatura': o app não confunde com pagamento de fatura


def num(s):
    return round(float(s.replace(".", "").replace(",", ".")), 2)


def texto(pdf):
    return subprocess.run(
        ["pdftotext", "-raw", "-enc", "UTF-8", pdf, "-"], capture_output=True, text=True, encoding="utf-8", check=True
    ).stdout


def ler_fatura(pdf):
    t = texto(pdf)
    emitida = EMITIDA.search(t)
    consumos = CONSUMOS.search(t)
    if not emitida or not consumos:
        raise SystemExit(f"{pdf}: cabeçalho da fatura não reconhecido")
    mes_em, ano_em = int(emitida.group(1)), int(emitida.group(2))
    total = num(consumos.group(5))
    itens = []
    for linha in t.splitlines():
        m = LINHA.match(linha.strip())
        if not m or "Pagamento da fatura" in m.group(3) or m.group(3).startswith("Crédito"):
            continue
        dia, mes = int(m.group(1)), int(m.group(2))
        ano = ano_em - 1 if mes > mes_em else ano_em  # compra de dez em fatura de jan
        itens.append((date(ano, mes, dia).isoformat(), m.group(3).strip(), num(m.group(4)), f"{ano_em}-{mes_em:02d}"))
    return itens, total


def main():
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    saida, pdfs = sys.argv[1], sys.argv[2:]
    todas, ok = [], True
    for pdf in pdfs:
        itens, total = ler_fatura(pdf)
        soma = round(sum(i[2] for i in itens), 2)
        marca = "OK " if abs(soma - total) < 0.005 else "DIVERGE"
        ok &= marca == "OK "
        print(f"{marca} {pdf.split('/')[-1].split(chr(92))[-1]}: {len(itens)} linhas, soma {soma:.2f} x fatura {total:.2f}")
        todas += itens
    todas.sort(key=lambda x: x[0])  # ordem crescente; saldo 0 em todas (não é conta)
    with open(saida, "w", encoding="utf-8", newline="") as f:
        f.write("RELEASE_DATE;TRANSACTION_TYPE;REFERENCE_ID;TRANSACTION_NET_AMOUNT;PARTIAL_BALANCE\n")
        vistos = {}
        for d, nome, v, fat in todas:
            a, m_, dia = d.split("-")
            k = (fat, d, nome, v)
            vistos[k] = vistos.get(k, 0) + 1  # ref estável (inclui o mês da fatura): reimportar com outubro não duplica nem perde
            valor = f"-{v:.2f}".replace(".", ",")
            f.write(f"{dia}-{m_}-{a};{PREFIXO}{nome};CARTAO-{fat}-{d}-{v:.2f}-{vistos[k]};{valor};0,00\n")
    print(f"{len(todas)} linhas -> {saida}")
    if not ok:
        raise SystemExit("Alguma soma não bate: confira antes de importar.")


main()
