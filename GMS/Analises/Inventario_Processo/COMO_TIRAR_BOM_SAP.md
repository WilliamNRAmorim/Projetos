# Como tirar a BOM das mangueiras do SAP (para a lista GMS_BOM_Mangueira)

Não precisa do relatório de lista técnica (CS11/CS12, que é uma mangueira por vez). A COOIS, que você já exporta para
o BI, tem outra lista que traz os componentes de cada OP. Um único export cobre todas as mangueiras de uma vez.

## Passo a passo (uma vez; repetir só quando a engenharia mudar BOM ou entrar mangueira nova)

1. Transação **COOIS**.
2. No campo **Lista** (List), troque "Cabeçalhos de ordem" por **Visão geral componentes** (Components).
3. Seleção:
   - Centro (Plant): **H204**
   - Tipo de ordem (Order Type): **ZBM1**
   - Planejador MRP (MRP controller): **AIH** (mangueira; supervisor HOS)
   - Data de início base (Basic start date): **01/05/2026 até hoje** (6 meses pega todas as mangueiras que rodam)
   - Em "Seleção de status", desmarque o filtro de status, para vir OP aberta e encerrada.
4. Execute (F8).
5. Se faltar coluna, abra o layout (Ctrl+F8) e deixe pelo menos: **Ordem**, **Material** (o componente),
   **Qtd. necessária** (Requirement Quantity), **Unidade**, **Texto breve do material**, **Item** e **Qtd. retirada** (Quantity Withdrawn).
6. Exporte: menu **Lista > Exportar > Planilha** (Ctrl+Shift+F7) e grave como
   `Dados_Brutos/coois_componentes_AAAA-MM-DD.xlsx` dentro de Projetos.

Pronto. O chefe cruza com a COOIS de cabeçalho (quantidade da OP em metros e a mangueira), tira a BOM por metro de
cada mangueira (mediana das OPs) e grava na lista GMS_BOM_Mangueira. O inventário lê a lista.

## Por que a MB51 não serve
A MB51 que vai para o BI só traz movimento 101/102 (entrada de produção). O consumo (261) não vem, então não dá
para tirar o insumo por metro dela.
