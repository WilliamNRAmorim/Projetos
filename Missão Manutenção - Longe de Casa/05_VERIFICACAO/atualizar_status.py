"""Atualiza STATUS_VERIFICACAO.xlsx a partir das respostas (planilhas, POR_CONFIANCA e RESPOSTAS_IDENTIFICADOR*.csv).

Usa a mesma junção de respostas do gerar_verificacao.py. Não mexe nas planilhas de verificação.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gerar_verificacao as G


def main():
    if os.path.exists(G.STATUS_XLSX):
        try:
            with open(G.STATUS_XLSX, "ab"):
                pass
        except PermissionError:
            raise SystemExit("ERRO: STATUS_VERIFICACAO.xlsx está aberto no Excel. Feche o arquivo e rode de novo.")
    os.makedirs(G.DIR_DADOS, exist_ok=True)
    resp = G.coletar_respostas()
    G.salvar_respostas(resp)
    print(f"Respostas juntadas: {len(resp)} material(is)")
    itens = G.montar_itens()
    G.gerar_status(itens, resp)


if __name__ == "__main__":
    main()
