"""Gera as definições dos fluxos do Uiu v4 (MEL-276). Só leitura no SharePoint e no Power BI.

Saída, na mesma pasta:
  consultar_gms.json, ler_linhas.json, perguntar_bi.json  -> clientdata de produção (gatilho do agente)
  teste_lote.json                                         -> o mesmo pipeline do Consultar GMS, em lote, para o fluxo temporário
As regras estão em ../ESPECIFICACAO_INDICADORES.md. Uso: python gerar_fluxos.py
"""
import csv
import json
import pathlib

AQUI = pathlib.Path(__file__).parent
GMS = AQUI.parents[3]
SITE = 'https://danfoss.sharepoint.com/sites/OperationsGuaratingueta'
REF_SP = 'cra6eb_uiu_gms.connectionreference.SharePointCrb333ea9016'
REF_PBI = 'cra6eb_teste_uiu_powerbi'
WS, DS = '629ca442-8019-47e0-83e4-0d48b2d30974', 'b48699da-af0b-4f0e-9b2e-f89cc657dbc1'
QTD = 'Quantidade_Inspe_x00e7__x00e3_o'
TRANC = 'Tran_x00e7_adeira'
N = '_nada'  # coluna que não existe: devolve vazio

# ---------------------------------------------------------------- tabelas de regra
BASE = dict(data=N, tipo='dia', v=N, conta='nao', maquina=N, mangueira=N, etapa=N, etapaFixa='', codigo=N, cabine=N, op=N, turno=N, orig=N, janela=N, extra='')
HH = dict(lista='Hora-Hora', sel='ID,field_0,field_2,field_3,field_4,field_5,field_7,field_11,field_12,TurnoH', data='field_0', maquina='field_2',
          mangueira='field_4', turno='TurnoH', codigo='field_12', janela='field_3', etapaFixa='Trançagem')
FONTES = {
    'insp': dict(lista='RegistrosInspeção', sel=f'ID,OP_ID,{QTD},DataHoraInspecao,Mangueira,{TRANC},cabine_teste', data='DataHoraInspecao', tipo='inst', v=QTD,
                 maquina=TRANC, mangueira='Mangueira', cabine='cabine_teste', op='OP_ID', turno='*hora', etapaFixa='Extração'),
    'ref': dict(lista='TiposErros', sel=f'ID,Created,A,OData__x0043_,OP_ID,DataHoraRefugo,{TRANC},TurnoErro,cabine_teste', data='DataHoraRefugo', v='OData__x0043_',
                codigo='A', maquina=TRANC, cabine='cabine_teste', op='OP_ID', turno='TurnoErro'),
    'ev': dict(lista='Eventos_Producao', sel='ID,etapa,tipo,turno,metros,origem_ID,data_ref', data='data_ref', v='metros', etapa='etapa', turno='turno', codigo='tipo',
               orig='origem_ID', extra="origem eq 'ficha_producao' and (tipo eq 'Fim' or tipo eq 'Parcial' or tipo eq 'Início')"),
    'hh7': dict(HH, v='field_7'), 'hh5': dict(HH, v='field_5'), 'hh11': dict(HH, v='field_11'),
    'mp': dict(lista='Producao_Montagem', sel='ID,field_1,field_2,field_3,field_9,field_13', data='field_1', v='field_9', maquina='field_3', turno='field_2', codigo='field_13'),
    'mpar': dict(lista='Paradas_Montagem', sel='ID,field_1,field_2,field_3,field_5,field_6', data='field_1', v='field_6', maquina='field_3', turno='field_2', codigo='field_5'),
    'bob': dict(lista='Refugo_Bobinadeira', sel='ID,field_2,field_4,field_6,Maquina,Motivos', data='field_2', tipo='inst', v='field_6', maquina='Maquina', codigo='Motivos'),
    'man': dict(lista='RefugoExtrusora_estrutura', sel='ID,field_4,field_5,field_7', data='field_7', tipo='inst', v='field_5', codigo='field_4'),
    'wip': dict(lista='ficha_producao', sel=f'ID,OP,Mangueira,{TRANC},field_10', tipo='foto', conta='sim', etapa='field_10', maquina=TRANC, mangueira='Mangueira', op='OP',
                extra="field_11 eq 'Em processo'"),
}
FONTES = {k: {**BASE, 'nome': k, **v} for k, v in FONTES.items()}


def ind(fontes, un, modo, dims, fixas=(), avisos=''):
    return dict(fontes=list(fontes), un=un, modo=modo, dims=list(dims), fixas=list(fixas), aviso=avisos)


INDICADORES = {
    'inspecao_boa': ind(['insp'], 'm', 'normal', ['dia', 'turno', 'mangueira', 'maquina', 'cabine', 'op'], avisos='Lance lançado depois muda dia já respondido.'),
    'refugo': ind(['ref'], 'm', 'normal', ['dia', 'codigo', 'maquina', 'cabine', 'op', 'turno'],
                  avisos='Refugo é pelo dia do registro (civil), a coluna não guarda a hora. Máquina = trançadeira de origem da OP, não prova de causa. Repetidos não são excluídos.'),
    'perc_refugo': ind(['insp', 'ref'], '%', 'perc', ['maquina', 'cabine', 'op'], avisos='Cabine, dia civil nas duas pontas. Não é o % Refugo Cabine do BI, que usa a ficha.'),
    'producao_etapa': ind(['ev', 'hh7', 'insp'], 'm', 'semtotal', ['dia', 'turno', 'etapa'], ['etapa'],
                          'Etapas nunca se somam. Trançagem = Hora-Hora; Vulcanização = Início; Extração = inspeção. Cancelamento na Trançagem não é descontável (a Hora-Hora não tem ficha).'),
    'trancagem_real': ind(['hh7'], 'm', 'normal', ['dia', 'turno', 'maquina', 'mangueira'], avisos='Duas passadas: a lista guarda a metade. O BI corta o dia às 05:00 (hora cheia); por dia pode diferir.'),
    'trancagem_meta_gravada': ind(['hh5'], 'm', 'normal', ['dia', 'turno', 'maquina'], avisos='Não é a meta do painel. Meta e aderência oficiais: Perguntar ao BI.'),
    'deficit_hora_hora': ind(['hh11'], 'min', 'semtotal', ['dia', 'turno', 'maquina', 'codigo'], ['bloco'],
                             'Déficit contra a meta, não cronômetro. Os blocos nunca se somam. Parada oficial: Perguntar ao BI.'),
    'montagem_pecas': ind(['mp'], 'pç', 'normal', ['dia', 'turno', 'maquina', 'codigo']),
    'montagem_paradas': ind(['mpar'], 'min', 'semtotal', ['dia', 'turno', 'maquina', 'codigo'], ['bloco'],
                            'Parada real, TE e RF nunca se somam. O desconto da OT com RF é do BI.'),
    'refugo_fio': ind(['bob'], 'unidade a confirmar', 'normal', ['dia', 'maquina', 'codigo'], avisos='Não soma com metros.'),
    'refugo_mandril': ind(['man'], 'kg', 'normal', ['dia', 'codigo'], avisos='Em kg: nunca percentual sobre metros.'),
    'ops_em_processo': ind(['wip'], 'fichas', 'normal', ['etapa', 'maquina', 'mangueira', 'op'], avisos='Foto de agora. Diga "na etapa", nunca "parada".'),
}
COM_OP = ['inspecao_boa', 'refugo', 'perc_refugo']
CEL = ['TH01', 'TH02', 'TH03', 'TH04', 'TH05', 'TH06', 'TH07', 'TO04', 'TM01', 'TM04', 'SPIRAL']

PROG, CAD = [], []
with open(GMS / 'PowerBI' / 'modelo' / 'dMotivoParada.csv', encoding='utf-8-sig') as f:
    for r in csv.DictReader(f, delimiter=';'):
        if r['Família']:  # só motivos da Hora-Hora; os da Montagem não têm família
            CAD.append(r['Motivo'])
            if r['Tipo'] == 'Programada':
                PROG.append(r['Motivo'])


# ---------------------------------------------------------------- utilidades
def compose(v, apos=None):
    return {'type': 'Compose', 'inputs': v, 'runAfter': {a: ['Succeeded'] for a in ([apos] if apos else [])}}


def setvar(n, v, apos=None):
    return {'type': 'SetVariable', 'inputs': {'name': n, 'value': v}, 'runAfter': {a: ['Succeeded'] for a in ([apos] if apos else [])}}


def seq(acoes):
    """Encadeia as ações na ordem do dicionário."""
    ant = None
    for k, a in acoes.items():
        a['runAfter'] = {ant: ['Succeeded']} if ant else {}
        ant = k
    return acoes


def select(de, campos):
    return {'type': 'Select', 'inputs': {'from': de, 'select': campos}, 'runAfter': {}}


def query(de, onde):
    return {'type': 'Query', 'inputs': {'from': de, 'where': onde}, 'runAfter': {}}


def initvar(n, t, v):
    return {'type': 'InitializeVariable', 'inputs': {'variables': [{'name': n, 'type': t, 'value': v}]}, 'runAfter': {}}


def http_get(uri):
    return {'type': 'OpenApiConnection', 'inputs': {
        'host': {'connectionName': 'shared_sharepointonline', 'operationId': 'HttpRequest', 'apiId': '/providers/Microsoft.PowerApps/apis/shared_sharepointonline'},
        'parameters': {'dataset': SITE, 'parameters/method': 'GET', 'parameters/uri': uri, 'parameters/headers': {'Accept': 'application/json;odata=nometadata'}},
        'authentication': "@parameters('$authentication')"}, 'runAfter': {}}


E = "outputs('Entrada')"
F = "outputs('Fonte')"
P = "outputs('Param')"


def soma_xml(arr, campo):
    """Soma exata do campo de um array de objetos; array vazio dá 0."""
    return f"xpath(xml(json(concat('{{\"r\":{{\"i\":', string(union({arr}, json('[{{\"i\":\"zero\",\"v\":0,\"r\":0}}]'))), '}}}}'))), 'sum(/r/i/{campo})')"


# ---------------------------------------------------------------- pipeline do Consultar GMS
def pipeline():
    bx = f"toLower(trim(coalesce({E}?['agrupar'],'-')))"
    c1 = f"first(split(trim(coalesce({E}?['onde'],'-')),';'))"
    c2 = f"coalesce(first(skip(split(trim(coalesce({E}?['onde'],'-')),';'),1)),'-')"

    def dim(c):
        return f"toLower(trim(first(split({c},'='))))"

    def val(c):
        bruto = f"trim(last(split({c},'=')))"
        semnum = f"if(and(equals({dim(c)},'codigo'),contains({bruto},' - '),isInt(trim(first(split(concat({bruto},' - '),' - '))))),trim(join(skip(split({bruto},' - '),1),' - ')),{bruto})"
        almoco = f"if(and(equals({dim(c)},'codigo'),equals(toLower({semnum}),'refeição'),equals(toLower(trim(coalesce({E}?['indicador'],'-'))),'deficit_hora_hora')),'Almoço',{semnum})"
        return f"if(equals({dim(c)},'maquina'),toUpper(replace(replace({bruto},'-',''),'.','')),if(equals({dim(c)},'turno'),take(concat({bruto},' '),1),{almoco}))"

    def iso(campo):
        s = f"split(concat(trim(coalesce({E}?['{campo}'],'-')),'/-/-'),'/')"
        return f"if(equals(length(trim(coalesce({E}?['{campo}'],'-'))),10),concat({s}[2],'-',{s}[1],'-',{s}[0]),'-')"

    partes_onde = f"split(trim(coalesce({E}?['onde'],'-')),';')"
    onde_ok = f"and(lessOrEquals(length({partes_onde}),2),or(equals(trim({c1}),'-'),equals(length(split({c1},'=')),2)),or(equals(trim({c2}),'-'),empty(trim({c2})),equals(length(split({c2},'=')),2)))"
    agr_ok = f"lessOrEquals(length(split({bx},',')),2)"
    corte_ok = f"contains(createArray('civil','produtivo','-',''),toLower(trim(coalesce({E}?['corte'],'-'))))"

    param = {
        'ind': f"@{{toLower(trim(coalesce({E}?['indicador'],'-')))}}",
        'ini': f"@{{{iso('de')}}}", 'fim': f"@{{{iso('ate')}}}",
        'g1': f"@{{if(or(equals({bx},'-'),empty({bx})),'',trim(first(split({bx},','))))}}",
        'g2': f"@{{trim(coalesce(first(skip(split({bx},','),1)),''))}}",
        'd1': f"@{{{dim(c1)}}}", 'v1': f"@{{{val(c1)}}}", 'd2': f"@{{{dim(c2)}}}", 'v2': f"@{{{val(c2)}}}",
        'civil': f"@{{equals(toLower(trim(coalesce({E}?['corte'],'-'))),'civil')}}",
    }
    cfg = "outputs('Indic')"
    tem_turno = f"or(equals({P}?['g1'],'turno'),equals({P}?['g2'],'turno'),equals({P}?['d1'],'turno'),equals({P}?['d2'],'turno'))"
    op_bruto = f"if(equals({P}?['d1'],'op'),{P}?['v1'],if(equals({P}?['d2'],'op'),{P}?['v2'],''))"
    datas_ok = f"and(not(equals({P}?['ini'],'-')),not(equals({P}?['fim'],'-')),lessOrEquals({P}?['ini'],{P}?['fim']))"
    sem_data_ok = f"or(equals({P}?['ind'],'ops_em_processo'),and(equals({P}?['ini'],'-'),equals({P}?['fim'],'-'),isInt({op_bruto}),contains(createArray({','.join(repr(x) for x in COM_OP)}),{P}?['ind'])))"
    dims_ok = ' , '.join(f"or(empty({P}?['{g}']),equals({P}?['{g}'],'-'),contains({cfg}?['dims'],{P}?['{g}']))" for g in ('g1', 'g2', 'd1', 'd2'))

    # corte que vale para colunas com hora
    corte = (f"if(contains(createArray('perc_refugo','refugo'),{P}?['ind']),'civil',if(and(equals({P}?['civil'],'True'),not({tem_turno}),"
             f"contains(createArray('inspecao_boa','refugo_fio','refugo_mandril'),{P}?['ind'])),'civil','produtivo'))")

    hora = f"if(equals({F}?['tipo'],'inst'),if(equals(outputs('Corte'),'civil'),'03:00','08:20'),'00:00')"
    f_op = f"@{{if(and(isInt({op_bruto}),not(equals({F}?['op'],'{N}'))),concat({F}?['op'],' eq ',{op_bruto}),'')}}"
    f_data = (f"@{{if(or(equals({F}?['tipo'],'foto'),equals({P}?['ini'],'-')),'',concat({F}?['data'],' ge datetime''',{P}?['ini'],'T',{hora},':00Z'' and ',{F}?['data'],"
              f"' lt datetime''',formatDateTime(addDays(coalesce(if(equals({P}?['fim'],'-'),null,{P}?['fim']),'2026-01-01'),1),'yyyy-MM-dd'),'T',{hora},':00Z'''))}}")

    col = lambda k: f"item()?[{F}?['{k}']]"
    txt = lambda k: f"trim(string(coalesce({col(k)},'')))"
    dt = f"addMinutes(coalesce({col('data')},'2026-01-01T03:00:00Z'),if(and(equals({F}?['tipo'],'inst'),equals(outputs('Corte'),'produtivo')),-500,-180))"
    # minutos desde 05:20 de Brasília (08:20Z = 500 min): 1º 517, 2º 503, 3º 420
    mt = f"add(mul(int(formatDateTime(addMinutes(coalesce({col('data')},'2026-01-01T08:20:00Z'),-500),'HH')),60),int(formatDateTime(addMinutes(coalesce({col('data')},'2026-01-01T08:20:00Z'),-500),'mm')))"
    maq = f"toUpper(replace(replace({txt('maquina')},'-',''),'.',''))"
    norm = {
        'i': f"@{{concat({F}?['nome'],':',string(item()?['ID']))}}", 'id': "@int(item()?['ID'])",
        'dia': f"@{{if(equals({F}?['tipo'],'foto'),'',formatDateTime({dt},'dd/MM/yyyy'))}}",
        'turno': f"@{{if(equals({F}?['turno'],'*hora'),if(less({mt},517),'1',if(less({mt},1020),'2','3')),take(concat({txt('turno')},' '),1))}}",
        'maquina': f"@{{{maq}}}", 'mangueira': f"@{{{txt('mangueira')}}}",
        'etapa': f"@{{if(empty({F}?['etapaFixa']),{txt('etapa')},{F}?['etapaFixa'])}}",
        'codigo': f"@{{if(isInt(trim(first(split(concat({txt('codigo')},' - '),' - ')))),trim(join(skip(split({txt('codigo')},' - '),1),' - ')),{txt('codigo')})}}",
        'cabine': f"@{{{txt('cabine')}}}", 'op': f"@{{first(split(string(coalesce({col('op')},'')),'.'))}}",
        'orig': f"@{{first(split(string(coalesce({col('orig')},'')),'.'))}}",
        'dk': f"@{{concat(string(coalesce({col('data')},'')),'|',{maq},'|',{txt('turno')},'|',{txt('janela')})}}",
        'v': f"@if(equals({F}?['conta'],'sim'),1,float(coalesce({col('v')},0)))",
        'r': f"@if(equals({F}?['nome'],'ref'),float(coalesce({col('v')},0)),0)",
        'dd': f"@div(sub(ticks(coalesce(item()?['Created'],'2026-01-01T00:00:00Z')),ticks(coalesce({col('data')},'2026-01-01T00:00:00Z'))),864000000000)",
    }
    cod = "item()?['codigo']"
    motivo = f"if(equals({cod},'Refeição'),'Almoço',if(equals({cod},'Problema no tubo'),'Análise/Problema no tubo',{cod}))"
    bloco = (f"if(equals(outputs('Param')?['ind'],'deficit_hora_hora'),if(empty({cod}),'sem motivo',if(contains(outputs('Programada'),{motivo}),'pausa programada',"
             f"if(equals({motivo},'Divergência do Tempo Padrão'),'velocidade reduzida',if(contains(outputs('Cadastro'),{motivo}),'demais motivos','motivo fora do cadastro')))),"
             f"if(equals(outputs('Param')?['ind'],'montagem_paradas'),if(equals({cod},'TE - Tempo Excedido'),'TE (tempo excedido)',if(startsWith(toUpper(trim({cod})),'RF'),'RF (refeição)','parada real')),''))")
    norm2 = {k: f"@item()?['{k}']" for k in norm}
    norm2['codigo'] = f"@{{if(equals({F}?['nome'],'hh11'),{motivo},{cod})}}"
    norm2['bloco'] = f"@{{{bloco}}}"

    def sem_acento(x):
        for a, b in (('ç', 'c'), ('ã', 'a'), ('á', 'a'), ('â', 'a'), ('à', 'a'), ('é', 'e'), ('ê', 'e'), ('í', 'i'), ('ó', 'o'), ('ô', 'o'), ('õ', 'o'), ('ú', 'u')):
            x = f"replace({x},'{a}','{b}')"
        return x

    def cond(d, v):
        x = sem_acento(f"toLower(string(coalesce(item()?[{P}?['{d}']],'')))")
        y = sem_acento(f"toLower({P}?['{v}'])")
        return f"or(equals({P}?['{d}'],'-'),empty({P}?['{d}']),equals({x},{y}),startsWith({x},concat({y},' ')))"

    nome = f"{F}?['nome']"
    # Cancelada (MEL-260): mesma ficha e mesma etapa, ID menor que o do último Cancelado
    canc = f"less(float(item()?['id']),float(xpath(xml(variables('Canc')),concat('sum(/r/c[k=\"',item()?['orig'],'|',item()?['etapa'],'\"][last()]/id)'))))"
    ev_fora = (f"and(equals({nome},'ev'),or(equals(item()?['etapa'],'Trançagem'),equals(item()?['etapa'],'Extração'),"
               f"and(equals(item()?['etapa'],'Vulcanização'),not(equals(item()?['codigo'],'Início'))),"
               f"and(not(equals(item()?['etapa'],'Vulcanização')),equals(item()?['codigo'],'Início'))))")
    hh_fora = f"and(startsWith({nome},'hh'),not(contains(outputs('Celulas'),item()?['maquina'])))"
    longe = f"and(not(equals({P}?['ini'],'-')),or(greater(item()?['dd'],60),less(item()?['dd'],-60)))"

    uri = (f"@{{concat('_api/web/lists/getbytitle(''',encodeUriComponent({F}?['lista']),''')/items?$select=',{F}?['sel'],'&$filter=',"
           f"encodeUriComponent(join(body('Partes'),' and ')),'&$orderby=ID&$top=5000')}}")

    fonte = seq({
        'Fonte': compose("@outputs('Fontes')?[items('Cada_fonte')]"),
        'Partes': query(None, "@not(empty(item()))"),
        'Uri_ini': setvar('Uri', uri),
        'Zera_brutas': setvar('Brutas', []),
        'Zera_pag': setvar('Paginas', 0),
        'Paginar': {'type': 'Until', 'expression': "@or(equals(variables('Uri'),''),greaterOrEquals(variables('Paginas'),10))", 'limit': {'count': 12, 'timeout': 'PT80S'}, 'actions': seq({
            'Ler': http_get("@variables('Uri')"),
            'Juntar': compose("@union(variables('Brutas'),body('Ler')?['value'])"),
            'Guardar': setvar('Brutas', "@outputs('Juntar')"),
            'Contar': {'type': 'IncrementVariable', 'inputs': {'name': 'Paginas', 'value': 1}, 'runAfter': {}},
            'Proxima': setvar('Uri', f"@{{if(empty(body('Ler')?['odata.nextLink']),'',replace(body('Ler')?['odata.nextLink'],'{SITE}/',''))}}"),
        })},
        'Completo_val': compose("@and(variables('Completo'),equals(variables('Uri'),''))"),
        'Completo_set': setvar('Completo', "@outputs('Completo_val')"),
        'Se_ev': {'type': 'If', 'expression': {'equals': [f'@{nome}', 'ev']}, 'actions': seq({
            'Ler_canc': http_get(f"_api/web/lists/getbytitle('Eventos_Producao')/items?$select=ID,origem,origem_ID,etapa&$filter=tipo%20eq%20%27Cancelado%27&$orderby=ID&$top=5000"),
            'So_ficha': query("@body('Ler_canc')?['value']", "@equals(item()?['origem'],'ficha_producao')"),
            'Linhas_canc': select("@body('So_ficha')", "@{concat('<c><k>',first(split(string(item()?['origem_ID']),'.')),'|',item()?['etapa'],'</k><id>',string(item()?['ID']),'</id></c>')}"),
            'Canc_set': setvar('Canc', "@{concat('<r>',join(body('Linhas_canc'),''),'</r>')}"),
            'Ler_sem_evento': http_get("_api/web/lists/getbytitle('ficha_producao')/items?$select=ID&$filter=field_11%20eq%20%27Cancelado%27&$orderby=ID&$top=5000"),
            'Ids_fichas_canc': select("@coalesce(body('Ler_sem_evento')?['value'],json('[]'))", "@{string(item()?['ID'])}"),
        }), 'else': {'actions': {}}, 'runAfter': {}},
        'Norm': select("@variables('Brutas')", norm),
        'Norm2': select("@body('Norm')", norm2),
        'Base': query("@body('Norm2')", f"@and(not({ev_fora}),not({hh_fora}))"),
        'Boas_set': setvar('Boas_v', "@body('Base')"),
        'Chaves_hh': select("@body('Base')", "@{item()?['dk']}"),
        'Se_dup': {'type': 'If', 'expression': {'and': [{'equals': [f"@startsWith({nome},'hh')", True]}, {'greater': ["@length(body('Base'))", "@length(union(body('Chaves_hh'),body('Chaves_hh')))"]}]}, 'actions': seq({
            'Pares_dup': select("@body('Base')", {'k': "@item()?['dk']", 'id': "@item()?['id']"}),
            'Ultimas': compose("@xpath(xml(json(concat('{\"r\":{\"i\":',string(body('Pares_dup')),'}}'))),'/r/i[not(k=following-sibling::i/k)]/id/text()')"),
            'So_ultimas': query("@body('Base')", "@contains(outputs('Ultimas'),string(item()?['id']))"),
            'Ultimas_set': setvar('Boas_v', "@body('So_ultimas')"),
            'Aviso_d': {'type': 'AppendToArrayVariable', 'inputs': {'name': 'Avisos', 'value': "@{concat(string(sub(length(body('Base')),length(body('So_ultimas')))),' janela(s) repetida(s) na Hora-Hora: vale a última')}"}, 'runAfter': {}},
        }), 'else': {'actions': {}}, 'runAfter': {}},
        # só quando há filtro em onde
        'Se_filtro': {'type': 'If', 'expression': f"@not(and(equals({P}?['d1'],'-'),or(equals({P}?['d2'],'-'),empty({P}?['d2']))))", 'actions': seq({
            'Antes': compose("@variables('Boas_v')"),
            'Filtrar': query("@outputs('Antes')", f"@and({cond('d1', 'v1')},{cond('d2', 'v2')})"),
            'Filtrar_set': setvar('Boas_v', "@body('Filtrar')"),
            'Vals': select("@body('Base')", f"@{{string(coalesce(item()?[{P}?['d1']],''))}}"),
            'Se_vazio': {'type': 'If', 'expression': f"@and(empty(body('Filtrar')),not(empty(body('Base'))),not(equals({P}?['ind'],'producao_etapa')))", 'actions': {
                'Aviso_v': {'type': 'AppendToArrayVariable', 'inputs': {'name': 'Avisos', 'value': "@{concat('Nenhuma linha com esse filtro em ',outputs('Fonte')?['lista'],'. Valores que existem no período: ',join(take(union(body('Vals'),body('Vals')),25),', '))}"}, 'runAfter': {}}},
                'else': {'actions': {}}, 'runAfter': {}},
        }), 'else': {'actions': {}}, 'runAfter': {}},
        # só no refugo: datas trocadas e linhas repetidas
        'Se_ref': {'type': 'If', 'expression': {'equals': [f'@{nome}', 'ref']}, 'actions': seq({
            'Antes_ref': compose("@variables('Boas_v')"),
            'Trocadas': query("@outputs('Antes_ref')", f"@{longe}"),
            'Nao_trocadas': query("@outputs('Antes_ref')", f"@not({longe})"),
            'Ref_set': setvar('Boas_v', "@body('Nao_trocadas')"),
            'Aviso_trocadas': {'type': 'If', 'expression': {'greater': ["@length(body('Trocadas'))", 0]}, 'actions': {
                'Aviso_t': {'type': 'AppendToArrayVariable', 'inputs': {'name': 'Avisos', 'value': "@{concat(string(length(body('Trocadas'))),' linha(s) de refugo com dia e mês trocados ficaram fora (',formatNumber(" + soma_xml("body('Trocadas')", 'v') + ",'0.00','en-US'),' m); saem do mês errado, mas não voltam ao certo')}"}, 'runAfter': {}}},
                'else': {'actions': {}}, 'runAfter': {}},
            'Chave_rep': select("@body('Nao_trocadas')", "@{concat(item()?['dia'],'|',item()?['op'],'|',item()?['codigo'],'|',string(item()?['v']))}"),
            'Se_rep': {'type': 'If', 'expression': "@greater(length(body('Chave_rep')),length(union(body('Chave_rep'),body('Chave_rep'))))", 'actions': {
                'Aviso_r': {'type': 'AppendToArrayVariable', 'inputs': {'name': 'Avisos', 'value': "@{concat(string(sub(length(body('Chave_rep')),length(union(body('Chave_rep'),body('Chave_rep'))))),' linha(s) de refugo iguais a outra (dia, OP, código e metros); não foram excluídas')}"}, 'runAfter': {}}},
                'else': {'actions': {}}, 'runAfter': {}},
        }), 'else': {'actions': {}}, 'runAfter': {}},
        # só nos eventos: canceladas
        'Se_ev2': {'type': 'If', 'expression': {'equals': [f'@{nome}', 'ev']}, 'actions': seq({
            'Antes_ev': compose("@variables('Boas_v')"),
            'Canceladas': query("@outputs('Antes_ev')", f"@{canc}"),
            'Nao_canceladas': query("@outputs('Antes_ev')", f"@not({canc})"),
            'Ev_set': setvar('Boas_v', "@body('Nao_canceladas')"),
            'Aviso_canceladas': {'type': 'If', 'expression': {'greater': ["@length(body('Canceladas'))", 0]}, 'actions': seq({
                'Fichas_c': select("@body('Canceladas')", "@{concat('ficha ',item()?['orig'],' ',item()?['etapa'],' ',item()?['codigo'],' ',string(item()?['v']),' m')}"),
                'Aviso_c': {'type': 'AppendToArrayVariable', 'inputs': {'name': 'Avisos', 'value': "@{concat('Descontado por cancelamento: ',join(body('Fichas_c'),'; '))}"}, 'runAfter': {}}}),
                'else': {'actions': {}}, 'runAfter': {}},
            'Suspeitas': query("@body('Nao_canceladas')", "@and(contains(coalesce(body('Ids_fichas_canc'),json('[]')),item()?['orig']),greater(item()?['v'],0))"),
            'Susp_txt': select("@body('Suspeitas')", "@{concat('ficha ',item()?['orig'],' ',item()?['etapa'],' ',string(item()?['v']),' m')}"),
            'Se_susp': {'type': 'If', 'expression': {'greater': ["@length(body('Suspeitas'))", 0]}, 'actions': {
                'Aviso_s': {'type': 'AppendToArrayVariable', 'inputs': {'name': 'Avisos', 'value': "@{concat('Ficha com situação Cancelado sem desconto (segue somada): ',join(body('Susp_txt'),'; '))}"}, 'runAfter': {}}},
                'else': {'actions': {}}, 'runAfter': {}},
        }), 'else': {'actions': {}}, 'runAfter': {}},
        'Acumular': compose("@union(variables('Linhas'),variables('Boas_v'))"),
        'Acumular_set': setvar('Linhas', "@outputs('Acumular')"),
    })
    fonte['Se_ev']['actions']['Ids_fichas_canc']['runAfter'] = {'Ler_sem_evento': ['Succeeded', 'Failed', 'TimedOut']}
    fonte['Se_ev']['actions']['Aviso_f'] = {'type': 'AppendToArrayVariable', 'inputs': {'name': 'Avisos', 'value': 'Não consegui conferir fichas com situação Cancelado.'}, 'runAfter': {'Ler_sem_evento': ['Failed', 'TimedOut']}}
    fonte['Partes']['inputs']['from'] = "@createArray(" + f_op[2:-1] + ',' + f_data[2:-1] + f",{F}?['extra'])"

    dims = ["first(outputs('G'))", "first(skip(outputs('G'),1))", "first(skip(outputs('G'),2))"]

    def vd(d):
        return f"if(empty(string(coalesce(item()?[coalesce({d},'{N}')],''))),'(vazio)',string(item()?[coalesce({d},'{N}')]))"
    chave = f"if(empty(outputs('G')),'total',concat({vd(dims[0])},if(empty({dims[1]}),'',concat(' | ',{vd(dims[1])})),if(empty({dims[2]}),'',concat(' | ',{vd(dims[2])}))))"
    vazio_xml = "xml('<r/>')"
    perc = "@if(and(equals({m},'perc'),greater(float({s}),0)),float(formatNumber(div(mul(float({r}),float('100.0')),if(greater(float({s}),0),float({s}),float('1.0'))),'0.00','en-US')),null)"

    def xs(arr, campo):
        return f"xpath(xml(json(concat('{{\"r\":{{\"i\":',string({arr}),'}}}}'))),'sum(/r/i/{campo})')"
    modo = "outputs('Indic')?['modo']"

    contas = seq({
        'Corte': compose(f"@{{{corte}}}"),
        'Cada_fonte': {'type': 'Foreach', 'foreach': "@outputs('Indic')?['fontes']", 'runtimeConfiguration': {'concurrency': {'repetitions': 1}}, 'actions': fonte, 'runAfter': {}},
        'G_bruto': compose(f"@union(outputs('Indic')?['fixas'],createArray({P}?['g1'],{P}?['g2']))"),
        'G': query("@outputs('G_bruto')", "@and(not(empty(item())),not(equals(item(),'-')))"),
        'Pares': select("@variables('Linhas')", {'k': f"@{{{chave.replace(chr(39)+'G'+chr(39), chr(39)+'G'+chr(39))}}}", 'v': "@item()?['v']", 'r': "@item()?['r']", 'i': "@item()?['i']"}),
        'So_chaves': select("@body('Pares')", "@item()?['k']"),
        'Distintas': compose("@union(body('So_chaves'),body('So_chaves'))"),
        'Se_grupos': {'type': 'If', 'expression': {'lessOrEquals': ["@length(outputs('Distintas'))", 300]}, 'actions': seq({
            'Cada_grupo': {'type': 'Foreach', 'foreach': "@outputs('Distintas')", 'runtimeConfiguration': {'concurrency': {'repetitions': 20}}, 'actions': seq({
                'Do_grupo': query("@body('Pares')", "@equals(item()?['k'],items('Cada_grupo'))"),
                'Somas': compose({'v': f"@{xs(chr(98) + 'ody(' + chr(39) + 'Do_grupo' + chr(39) + ')', 'v')}", 'r': f"@{xs(chr(98) + 'ody(' + chr(39) + 'Do_grupo' + chr(39) + ')', 'r')}"}),
                'Guarda_grupo': {'type': 'AppendToArrayVariable', 'inputs': {'name': 'Grupos', 'value': {
                    'chave': "@items('Cada_grupo')", 'soma': "@float(formatNumber(outputs('Somas')?['v'],'0.00','en-US'))", 'refugo': f"@if(equals({modo},'perc'),float(formatNumber(outputs('Somas')?['r'],'0.00','en-US')),null)",
                    'perc': perc.format(m=modo, s="outputs('Somas')?['v']", r="outputs('Somas')?['r']"), 'linhas': "@length(body('Do_grupo'))"}}, 'runAfter': {}},
            }), 'runAfter': {}},
        }), 'else': {'actions': {'Aviso_300': {'type': 'AppendToArrayVariable', 'inputs': {'name': 'Avisos', 'value': "@{concat('Agrupamento com ',string(length(outputs('Distintas'))),' grupos (limite 300): filtre mais; grupos não listados')}"}, 'runAfter': {}}}}, 'runAfter': {}},
        'Total': compose({'v': '@' + soma_xml("body('Pares')", 'v'), 'r': '@' + soma_xml("body('Pares')", 'r')}),
        'Aviso_turno_antigo': {'type': 'If', 'expression': f"@and({tem_turno},not(equals({P}?['ind'],'inspecao_boa')),not(equals({P}?['ini'],'-')),lessOrEquals({P}?['ini'],'2026-10-29'),greaterOrEquals({P}?['fim'],'2026-10-05'))", 'actions': {
            'Aviso_ta': {'type': 'AppendToArrayVariable', 'inputs': {'name': 'Avisos', 'value': 'O período toca 05/10 a 29/10/2026: turno gravado pode ter a fronteira antiga (22:41).'}, 'runAfter': {}}}, 'else': {'actions': {}}, 'runAfter': {}},
        'Aviso_corte': {'type': 'If', 'expression': f"@and(contains(createArray('civil','produtivo'),toLower(trim(coalesce({E}?['corte'],'-')))),not(equals(toLower(trim(coalesce({E}?['corte'],'-'))),outputs('Corte'))),not(contains(createArray('montagem_pecas','montagem_paradas','ops_em_processo'),{P}?['ind'])))", 'actions': {
            'Aviso_co': {'type': 'AppendToArrayVariable', 'inputs': {'name': 'Avisos', 'value': "@{concat('Pedido em dia ',toLower(trim(coalesce(" + E + "?['corte'],'-'))),', aplicado o dia ',outputs('Corte'),': é o único que o dado (ou o turno) permite aqui.')}"}, 'runAfter': {}}}, 'else': {'actions': {}}, 'runAfter': {}},
        'Aviso_ref_turno': {'type': 'If', 'expression': f"@and({tem_turno},equals({P}?['ind'],'refugo'))", 'actions': {
            'Aviso_rt': {'type': 'AppendToArrayVariable', 'inputs': {'name': 'Avisos', 'value': 'Refugo por turno em dia civil mistura dois 3ºs turnos.'}, 'runAfter': {}}}, 'else': {'actions': {}}, 'runAfter': {}},
        'Periodo': compose("@{if(equals(" + P + "?['ind'],'ops_em_processo'),'agora',if(equals(" + P + "?['ini'],'-'),'todo o histórico da OP',"
                           "if(contains(createArray('montagem_pecas','montagem_paradas')," + P + "?['ind']),concat(" + E + "?['de'],' a '," + E + "?['ate'],' (dia gravado pela tela)'),if(or(contains(createArray('refugo')," + P + "?['ind']),equals(outputs('Corte'),'civil')),concat(" + E + "?['de'],' 00:00 a '," + E + "?['ate'],' 23:59 (dia civil, Brasília)'),"
                           "concat(" + E + "?['de'],' 05:20 a ',formatDateTime(addDays(" + P + "?['fim'],1),'dd/MM/yyyy'),' 05:20 (dia produtivo, Brasília)')))))}"),
        'Fontes_txt': select("@outputs('Indic')?['fontes']", "@{outputs('Fontes')?[item()]?['lista']}"),
        'Resultado': compose({
            'indicador': f"@{P}?['ind']", 'unidade': "@outputs('Indic')?['un']", 'periodo': "@outputs('Periodo')",
            'corte': "@outputs('Corte')", 'fonte': "@{join(body('Fontes_txt'),', ')}",
            'situacao': "@if(empty(variables('Linhas')),'0 registros (não diga que produziu zero)','ok')",
            'valor': f"@if(or(empty(variables('Linhas')),equals({modo},'semtotal'),equals({modo},'perc')),null,float(formatNumber(outputs('Total')?['v'],'0.00','en-US')))",
            'perc_total': perc.format(m=modo, s="outputs('Total')?['v']", r="outputs('Total')?['r']"),
            'refugo_total': f"@if(equals({modo},'perc'),float(formatNumber(outputs('Total')?['r'],'0.00','en-US')),null)",
            'boa_mais_refugo': f"@if(equals({modo},'perc'),float(formatNumber(outputs('Total')?['v'],'0.00','en-US')),null)",
            'linhas': "@length(variables('Linhas'))", 'completo': "@variables('Completo')",
            'agrupado_por': "@{join(body('G'),', ')}", 'grupos': "@reverse(sort(variables('Grupos'),'soma'))",
            'avisos': "@union(variables('Avisos'),createArray(outputs('Indic')?['aviso']))", 'consultado_em': "@{convertTimeZone(utcNow(),'UTC','E. South America Standard Time','dd/MM/yyyy HH:mm')}"}),
        'Saida_ok': setvar('Saida', "@{string(outputs('Resultado'))}"),
    })
    txt_contas = json.dumps(contas, ensure_ascii=False).replace("outputs('G')", "body('G')")
    contas = json.loads(txt_contas)

    caso = seq({
        'Zera_linhas': setvar('Linhas', []), 'Zera_grupos': setvar('Grupos', []), 'Zera_avisos': setvar('Avisos', []),
        'Zera_saida': setvar('Saida', ''), 'Zera_completo': setvar('Completo', True), 'Zera_canc': setvar('Canc', '<r><c><k>-</k><id>0</id></c></r>'),
        'Param': compose(param),
        'Indic': compose(f"@coalesce(outputs('Indicadores')?[{P}?['ind']],outputs('Indicador_vazio'))"),
        'Valido': {'type': 'If', 'expression': f"@and(not(empty(outputs('Indic')?['fontes'])),or({datas_ok},{sem_data_ok}),{dims_ok},{onde_ok},{agr_ok},{corte_ok})", 'actions': contas,
                   'else': {'actions': {'Saida_erro': setvar('Saida', "@{concat('{\"erro\":\"entrada inválida\",\"regras\":\"indicador: " + ', '.join(INDICADORES) + ". Datas DD/MM/AAAA com de <= ate (ou - nos dois quando onde tem op=número em inspecao_boa, refugo ou perc_refugo). Dimensões deste indicador: ',join(coalesce(outputs('Indic')?['dims'],json('[]')),' / '),'. corte: civil ou produtivo. agrupar: até 2. onde: até 2, dimensao=valor;dimensao=valor\"}')}")}}, 'runAfter': {}},
    })
    return caso


INICIO_TABELAS = {
    'Fontes': compose(FONTES), 'Indicadores': compose(INDICADORES), 'Indicador_vazio': compose(dict(fontes=[], dims=[], fixas=[], un='', modo='', aviso='')),
    'Celulas': compose(CEL), 'Programada': compose(PROG), 'Cadastro': compose(CAD),
}
VARS = [('Uri', 'string', ''), ('Linhas', 'array', []), ('Brutas', 'array', []), ('Boas_v', 'array', []), ('Grupos', 'array', []), ('Avisos', 'array', []),
        ('Paginas', 'integer', 0), ('Completo', 'boolean', True), ('Canc', 'string', ''), ('Saida', 'string', '')]


def gatilho(campos):
    props, req = {}, []
    for n, (titulo, desc) in enumerate(campos):
        k = 'text' if n == 0 else f'text_{n}'
        props[k] = {'title': titulo, 'type': 'string', 'x-ms-dynamically-added': True, 'description': desc, 'x-ms-content-hint': 'TEXT'}
        req.append(k)
    return {'manual': {'type': 'Request', 'kind': 'Skills', 'inputs': {'schema': {'type': 'object', 'properties': props, 'required': req}}}}


def resposta(valor, apos):
    return {'type': 'Response', 'kind': 'Skills', 'inputs': {'statusCode': 200, 'body': {'resultado': valor}, 'schema': {'type': 'object', 'properties': {
        'resultado': {'title': 'resultado', 'type': 'string', 'x-ms-content-hint': 'TEXT', 'x-ms-dynamically-added': True}}, 'additionalProperties': {}}},
        'runAfter': {apos: ['Succeeded', 'Failed', 'TimedOut', 'Skipped']}}


def pacote(triggers, actions, refs):
    cr = {}
    if 'sp' in refs:
        cr['shared_sharepointonline'] = {'runtimeSource': 'embedded', 'connection': {'connectionReferenceLogicalName': REF_SP}, 'api': {'name': 'shared_sharepointonline'}}
    if 'pbi' in refs:
        cr['shared_powerbi'] = {'runtimeSource': 'embedded', 'connection': {'connectionReferenceLogicalName': REF_PBI}, 'api': {'name': 'shared_powerbi'}}
    return {'properties': {'connectionReferences': cr, 'definition': {
        '$schema': 'https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#', 'contentVersion': '1.0.0.0',
        'parameters': {'$connections': {'defaultValue': {}, 'type': 'Object'}, '$authentication': {'defaultValue': {}, 'type': 'SecureObject'}},
        'triggers': triggers, 'actions': actions}}, 'schemaVersion': '1.0.0.0'}


ERRO = "@{if(empty(variables('Saida')),'{\"erro\":\"a consulta falhou. Confira datas DD/MM/AAAA, o indicador e o filtro, ou reduza o período\"}',variables('Saida'))}"
CAMPOS = [('indicador', 'Um destes: ' + ', '.join(INDICADORES)),
          ('de', 'Data inicial DD/MM/AAAA; - só com op= em onde ou em ops_em_processo'), ('ate', 'Data final DD/MM/AAAA, inclusive; - só com op= em onde ou em ops_em_processo'),
          ('corte', 'produtivo (05:20 a 05:20, padrão) ou civil (00:00 a 23:59)'),
          ('agrupar', 'Até 2 dimensões separadas por vírgula: dia, turno, mangueira, maquina, etapa, codigo, cabine, op; - para total'),
          ('onde', 'Filtro dimensao=valor;dimensao=valor (ex.: maquina=TH06;op=30803591); - para nenhum')]


def consultar():
    cab = seq({**{f'Ini_{n}': initvar(n, t, v) for n, t, v in VARS}, **json.loads(json.dumps(INICIO_TABELAS))})
    ent = {n: f"@{{triggerBody()?['{'text' if i == 0 else 'text_' + str(i)}']}}" for i, (n, _) in enumerate(CAMPOS)}
    cab['Entrada'] = compose(ent, list(cab)[-1])
    cab['Consulta'] = {'type': 'Scope', 'actions': pipeline(), 'runAfter': {'Entrada': ['Succeeded']}}
    cab['Responder'] = resposta(ERRO, 'Consulta')
    return pacote(gatilho(CAMPOS), cab, ['sp'])


def teste():
    casos = [
        ['inspecao_boa', '13/11/2026', '13/11/2026', 'civil', '-', '-'], ['inspecao_boa', '13/11/2026', '13/11/2026', 'produtivo', 'turno', '-'],
        ['inspecao_boa', '13/11/2026', '13/11/2026', 'civil', 'turno', '-'], ['inspecao_boa', '13/11/2026', '13/11/2026', 'civil', 'cabine', '-'],
        ['inspecao_boa', '09/11/2026', '13/11/2026', 'produtivo', '-', '-'], ['inspecao_boa', '01/10/2026', '31/10/2026', 'civil', 'mangueira', '-'],
        ['inspecao_boa', '15/11/2026', '15/11/2026', 'produtivo', '-', '-'], ['refugo', '13/11/2026', '13/11/2026', 'produtivo', 'codigo', '-'],
        ['perc_refugo', '13/11/2026', '13/11/2026', 'civil', '-', '-'], ['perc_refugo', '13/11/2026', '13/11/2026', 'civil', 'maquina', '-'],
        ['refugo', '01/10/2026', '31/10/2026', 'civil', 'codigo', '-'], ['refugo', '01/10/2026', '31/10/2026', 'civil', 'maquina', '-'],
        ['producao_etapa', '13/11/2026', '13/11/2026', 'produtivo', '-', '-'], ['producao_etapa', '13/11/2026', '13/11/2026', 'produtivo', 'turno', 'etapa=Cobertura'],
        ['trancagem_real', '13/11/2026', '13/11/2026', 'produtivo', 'maquina', '-'], ['trancagem_real', '13/11/2026', '13/11/2026', 'produtivo', 'turno', '-'],
        ['trancagem_real', '13/11/2026', '13/11/2026', 'produtivo', '-', 'maquina=TH-05'], ['trancagem_real', '09/11/2026', '13/11/2026', 'produtivo', 'maquina', '-'],
        ['deficit_hora_hora', '13/11/2026', '13/11/2026', 'produtivo', 'codigo', '-'], ['montagem_pecas', '13/11/2026', '13/11/2026', 'produtivo', 'maquina', '-'],
        ['montagem_paradas', '13/11/2026', '13/11/2026', 'produtivo', '-', '-'], ['inspecao_boa', '-', '-', '-', 'mangueira', 'op=30803591'],
        ['refugo', '-', '-', '-', 'codigo', 'op=30803591'], ['ops_em_processo', '-', '-', '-', 'etapa', '-'],
        ['refugo_fio', '13/11/2026', '13/11/2026', 'produtivo', 'codigo', '-'], ['trancagem_real', '01/10/2026', '31/10/2026', 'produtivo', '-', '-'],
        ['inspecao_boa', '13/11/2026', '13/11/2026', 'civil', '-', 'turno=3º Turno'], ['trancagem_real', '13/11/2026', '13/11/2026', 'civil', '-', '-'],
        ['deficit_hora_hora', '13/11/2026', '13/11/2026', 'produtivo', 'maquina', 'codigo=21 - Refeição'], ['producao_etapa', '13/11/2026', '13/11/2026', 'produtivo', '-', 'etapa=Vulcanizacao'],
        ['inspecao_boa', '13/11/2026', '13/11/2026', 'civil', '-', 'maquina=TH99'], ['inspecao_boa', '13/11/2026', '13/11/2026', 'civil', '-', 'maquina'],
        ['inspecao_boa', '13/11/2026', '13/11/2026', 'civil', 'dia,turno,cabine', '-'], ['inspecao_boa', '13/11/2026', '13/11/2026', 'noturno', '-', '-'],
        ['inspecao_boa', '13/11/2026', '13/11/2026', 'civil', '-', 'cabine=CABINE_L1;maquina=TH06;op=1'], ['trancagem_real', '01/10/2026', '31/10/2026', 'produtivo', '-', 'mangueira=GH781-8'],
        ['oee', '13/11/2026', '13/11/2026', 'produtivo', '-', '-'], ['refugo', '13/11/2026', '12/11/2026', 'civil', '-', '-'],
    ]
    casos = [dict(zip([n for n, _ in CAMPOS], c)) for c in casos]
    cab = seq({**{f'Ini_{n}': initvar(n, t, v) for n, t, v in VARS + [('Resultados', 'array', [])]}, **json.loads(json.dumps(INICIO_TABELAS))})
    corpo = {'Entrada': compose("@items('Cada_caso')"), 'Consulta': {'type': 'Scope', 'actions': pipeline(), 'runAfter': {'Entrada': ['Succeeded']}},
             'Anota': {'type': 'AppendToArrayVariable', 'inputs': {'name': 'Resultados', 'value': {'caso': "@items('Cada_caso')", 'saida': ERRO}}, 'runAfter': {'Consulta': ['Succeeded', 'Failed', 'TimedOut', 'Skipped']}}}
    cab['Cada_caso'] = {'type': 'Foreach', 'foreach': casos, 'runtimeConfiguration': {'concurrency': {'repetitions': 1}}, 'actions': corpo, 'runAfter': {list(cab)[-1]: ['Succeeded']}}
    cab['Resumo'] = {'type': 'Compose', 'inputs': "@variables('Resultados')", 'runAfter': {'Cada_caso': ['Succeeded', 'Failed']}}
    return pacote({'Recorrencia': {'type': 'Recurrence', 'recurrence': {'frequency': 'Month', 'interval': 12}}}, cab, ['sp'])


def ler_linhas():
    listas = sorted({f['lista'] for f in FONTES.values()} | {'Plano_OPs', 'Packing_Pallets', 'Conferencia_SAP', 'FifoBobinadeira', 'Controle_Catenaria', 'Historico_Carretel', 'lista_carreteis', 'ControleExtrusora_estrutura'})
    campos = [('lista', 'Nome exato da lista: ' + ', '.join(listas)), ('colunas', 'Colunas internas separadas por vírgula (ex.: ID,OP,field_10)'),
              ('filtro', 'Filtro OData com nomes internos; primeiro critério em coluna indexada. Datas em UTC. Para total use Consultar GMS'), ('ordem', 'Coluna e direção (ex.: ID desc)'), ('top', '1 a 50')]
    t = lambda i: f"trim(coalesce(triggerBody()?['{'text' if i == 0 else 'text_' + str(i)}'],''))"
    uri = f"@{{concat('_api/web/lists/getbytitle(''',encodeUriComponent({t(0)}),''')/items?$select=',encodeUriComponent({t(1)}),'&$filter=',encodeUriComponent({t(2)}),'&$orderby=',encodeUriComponent({t(3)}),'&$top=',if(isInt({t(4)}),string(min(50,max(1,int({t(4)})))),'20'))}}"
    ac = {'Ini_Saida': initvar('Saida', 'string', ''), 'Listas': compose(listas, 'Ini_Saida')}
    ac['Consulta'] = {'type': 'Scope', 'runAfter': {'Listas': ['Succeeded']}, 'actions': {'Valido': {'type': 'If', 'expression': f"@and(contains(outputs('Listas'),{t(0)}),not(empty({t(1)})),not(empty({t(2)})),not(equals({t(2)},'-')))", 'actions': seq({
        'Ler': http_get(uri),
        'Saida_ok': setvar('Saida', "@{concat('{\"linhas_lidas\":',string(length(body('Ler')?['value'])),',\"tem_mais\":',if(empty(body('Ler')?['odata.nextLink']),'false','true'),',\"aviso\":\"amostra para detalhe, nunca some; horários em UTC\",\"linhas\":',if(greater(length(string(body('Ler')?['value'])),24000),'\"resposta grande demais: peça menos colunas ou linhas\"',string(body('Ler')?['value'])),'}')}"),
    }), 'else': {'actions': {'Saida_inv': setvar('Saida', '{"erro":"lista fora da permitida, ou colunas/filtro vazios"}')}}, 'runAfter': {}}}}
    ac['Responder'] = resposta(ERRO, 'Consulta')
    return pacote(gatilho(campos), ac, ['sp'])


def perguntar_bi():
    rel = json.load(open(GMS / 'PowerBI' / 'GMS_Painel.Report' / 'definition' / 'reportExtensions.json', encoding='utf-8-sig'))
    med = {m['name']: (e['name'], m['expression']) for e in rel['entities'] for m in e.get('measures', [])}
    nomes = ['HH Meta Útil (m)', 'HH Real (m)', 'HH Aderência', 'HH Parado (min)', 'VG Cabine (m)']
    bloco = 'DEFINE\n' + '\n'.join(f"MEASURE {med[n][0]}[{n}] =\n{med[n][1]}\n" for n in nomes)
    campos = [('dax', 'Consulta DAX começando por EVALUATE (ou DEFINE). Use TOPN para listas. Já disponíveis: ' + ', '.join(f'[{n}]' for n in nomes))]
    q = "trim(coalesce(triggerBody()?['text'],''))"
    ac = {'Ini_Saida': initvar('Saida', 'string', ''), 'Medidas': compose(bloco, 'Ini_Saida')}
    ac['Consulta'] = {'type': 'Scope', 'runAfter': {'Medidas': ['Succeeded']}, 'actions': {'Valido': {'type': 'If', 'expression': f"@or(startsWith(toUpper({q}),'EVALUATE'),startsWith(toUpper({q}),'DEFINE'))", 'actions': seq({
        'Dax': compose(f"@{{concat(outputs('Medidas'),decodeUriComponent('%0A'),if(startsWith(toUpper({q}),'DEFINE'),substring({q},6),{q}))}}"),
        'Consultar': {'type': 'OpenApiConnection', 'inputs': {'host': {'connectionName': 'shared_powerbi', 'operationId': 'ExecuteDatasetQuery', 'apiId': '/providers/Microsoft.PowerApps/apis/shared_powerbi'},
                      'parameters': {'groupid': WS, 'datasetid': DS, 'specification/query': "@outputs('Dax')"}, 'authentication': "@parameters('$authentication')"}, 'runAfter': {}},
        'Saida_ok': setvar('Saida', "@{concat('{\"fonte\":\"modelo (GMS) do Power BI, última atualização do modelo\",\"linhas\":',string(length(coalesce(body('Consultar')?['firstTableRows'],json('[]')))),',\"dados\":',if(greater(length(string(body('Consultar')?['firstTableRows'])),24000),'\"resposta grande demais: use TOPN ou SUMMARIZECOLUMNS\"',string(coalesce(body('Consultar')?['firstTableRows'],json('[]')))),'}')}"),
    }), 'else': {'actions': {'Saida_inv': setvar('Saida', '{"erro":"a consulta precisa começar por EVALUATE ou DEFINE"}')}}, 'runAfter': {}}}}
    ac['Consulta']['actions']['Erro_dax'] = {'type': 'If', 'expression': "@empty(variables('Saida'))", 'actions': {
        'Saida_dax': setvar('Saida', "@{concat('{\"erro\":\"DAX recusado\",\"detalhe\":',string(coalesce(body('Consultar'),outputs('Consultar'))),'}')}")},
        'else': {'actions': {}}, 'runAfter': {'Valido': ['Failed', 'TimedOut']}}
    ac['Responder'] = resposta(ERRO, 'Consulta')
    return pacote(gatilho(campos), ac, ['pbi'])


if __name__ == '__main__':
    for nome, f in [('consultar_gms', consultar), ('teste_lote', teste), ('ler_linhas', ler_linhas), ('perguntar_bi', perguntar_bi)]:
        s = json.dumps(f(), ensure_ascii=False, indent=1)
        (AQUI / f'{nome}.json').write_text(s, encoding='utf-8', newline='\n')
        print(nome, len(s), 'programada', len(PROG), 'cadastro', len(CAD))
