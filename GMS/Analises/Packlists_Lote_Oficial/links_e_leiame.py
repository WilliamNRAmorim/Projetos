"""Gera links_para_gravar.csv (B e C) e o LEIA-ME da pasta saida/, e compacta cada pasta em .zip."""
import csv, os, zipfile, collections

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, 'saida')
BASE = 'https://danfoss.sharepoint.com/sites/OperationsGuaratingueta/PackLists/'

ind = list(csv.reader(open(os.path.join(SAIDA, 'indice.csv'), encoding='utf-8-sig'), delimiter=';'))
cab, rows = ind[0], ind[1:]

with open(os.path.join(SAIDA, 'links_para_gravar.csv'), 'w', newline='', encoding='utf-8-sig') as fh:
    w = csv.writer(fh, delimiter=';')
    w.writerow(['onde_gravar', 'chave', 'url_do_pdf', 'obs'])
    for g, arq, idp, pn, n, tot, tt, data, obs in rows:
        nome = arq.split('/')[1]
        if g == 'B_BD_sem_ficha':
            bd = obs.split('=')[1]
            w.writerow(['Packing_Manual (coluna LinkPDF, a criar)', 'Title = BD antigo #' + bd, BASE + nome, 'OrigemBD=' + bd])
        elif g == 'C_GMS_reconstruido' and not nome.endswith(tuple('_P%d.pdf' % i for i in range(2, 9))):
            ficha = obs.split()[1]
            w.writerow(['ficha_producao (coluna PackList Cabine)', 'ID = ' + ficha, BASE + nome, 'OP ' + idp.split()[0]])

c = collections.Counter(r[0] for r in rows)
open(os.path.join(SAIDA, 'LEIA-ME.txt'), 'w', encoding='utf-8').write("""PACKLISTS (lote oficial) - gerado em 08/10/2026 - nada foi gravado no SharePoint

Código de barras igual ao Excel antigo: part number em Code 39 (*PN*) e TOTAL em Code 128 Start A, texto = soma crua com vírgula.
Todos os PDFs: A4 paisagem, 1 página, mesmo desenho dos PDFs de 06/10.

PASTAS
1_substituir_PackLists  (%d)  MESMO nome dos PDFs já publicados. Subir em PackLists escolhendo SUBSTITUIR.
                              Os links em "PackList Cabine" já apontam para esses nomes, não precisa mexer em lista.
                              Conferido: data, ID, part-number, 26 lances e total idênticos aos publicados.
2_BD_sem_ficha          (%d)  Romaneios do BD antigo sem ficha no GMS (os de Packing_Manual). Arquivos NOVOS.
3_GMS_pos_BD            (%d)  OPs do GMS sem romaneio no BD, de 04/05/2026 em diante (reconstruídas pelos lances). NOVOS.
4_GMS_pre_BD            (%d)  OPs do GMS sem romaneio no BD, antes de 04/05/2026 (reconstruídas). NOVOS. Só suba se a logística
                              quiser; antes do BD não se sabe como os pallets foram divididos na época.

ARQUIVOS
indice.csv              grupo, arquivo, id do pallet, part-number, lances, total, texto do código do total, data
links_para_gravar.csv   onde gravar o link de cada PDF novo (Packing_Manual e PackList Cabine) com a URL pronta
nao_gerados.csv         OPs que ficaram de fora e por quê (28 OPs sem ficha/part-number no GMS)

COMO SUBIR (SharePoint, biblioteca PackLists)
1) Abra a biblioteca PackLists > Carregar > Arquivos (ou arraste a pasta) > escolha todos os PDFs de uma pasta.
2) Na pasta 1, quando perguntar sobre arquivos com o mesmo nome, escolha Substituir tudo (a biblioteca guarda a versão anterior).
3) Links: pastas 3 e 4 precisam do link em "PackList Cabine" da ficha; a pasta 2 no Packing_Manual (coluna LinkPDF).
   O links_para_gravar.csv tem a chave e a URL de cada um (cole pela visualização em grade).

TESTE ANTES DE TUDO: imprima 1 PDF de cada pasta e bipe o código do total (conferir com o Excel antigo para o mesmo total).
""" % (c['A_substitui_existente'], c['B_BD_sem_ficha'], sum(1 for r in rows if r[1].startswith('3_')), sum(1 for r in rows if r[1].startswith('4_'))))

for pasta in sorted(os.listdir(SAIDA)):
    p = os.path.join(SAIDA, pasta)
    if os.path.isdir(p):
        with zipfile.ZipFile(os.path.join(SAIDA, pasta + '.zip'), 'w', zipfile.ZIP_DEFLATED) as z:
            for f in sorted(os.listdir(p)):
                z.write(os.path.join(p, f), f)
for f in sorted(os.listdir(SAIDA)):
    if f.endswith('.zip'):
        print(f, round(os.path.getsize(os.path.join(SAIDA, f)) / 1e6, 1), 'MB')
