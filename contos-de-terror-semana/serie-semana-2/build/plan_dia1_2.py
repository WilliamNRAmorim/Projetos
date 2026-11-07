# (de, ate, cenario, opcoes, [personagens visiveis], {poses})
H, M, O, Z = 'helena', 'mi', 'otavio', 'zelia'
def p1(b): b(1, [(1,4,['portaria_ambar','corredor_magenta'],{},[H],{H:['neutro','olhando','seria']}), (5,8,['casa_dois_andares','vila_noite'],{},[H],{H:['olhando','hesitante','neutro']}), (9,10,'quarto_lilas',{},[H],{H:['assustado','medo']})],
    sons_extra=[(7,0.5,'respirar',{'vol':0.15}), (10,1.0,'stinger',{'vol':0.3})], destaque=['davi','giz','branco'])
def p2(b): b(2, [(1,5,['quarto_lilas','quarto_terra'],{},[H],{H:['cansada','neutro','olhando']}), (6,9,['quarto_lilas','quarto_terra'],{},[H],{H:['assustado','medo']}), (10,11,'quarto_terra',{},[H],{H:'medo'})],
    sons_extra=[(5,1.5,'rangido',{'vol':0.35}), (7,1.0,'rangido',{'vol':0.4}), (9,0.5,'rangido',{'vol':0.35})], destaque=['giz','circulo','helena'])
def p3(b): b(3, [(1,1,'quarto_terra',{},[H],{H:'cansada'}), (2,9,['quarto_terra','quarto_terra','olhos_fechados'],{},[H],{H:'silencio'}), (10,12,['quarto_terra','quarto_lilas'],{},[H],{H:['medo','assustado']})],
    sons_extra=[(2,0,'tiquetaque',{'lentidao':1,'vol':0.2}), (3,2.5,'tiquetaquePara',{'vol':0.25}), (4,0.5,'rangido',{'vol':0.3}), (9,0,'silencioDuck',{'dur':1.5})],
    rate_narr='-6%', destaque=['3h33','finja','fingindo'])
def p4(b): b(4, [(1,4,['vila_noite','cruzamento_noite'],{},[H,Z]), (5,12,'sala_benzedeira',{},[H,Z],{H:['neutro','olhando','assustado'],Z:['seria','neutro','sentadaSeria']})], sons_extra=[(5,0,'vento',{'vol':0.7},12)], rate_narr='-4%', destaque=['giz','credor','esteve'])
def p5(b): b(5, [(1,3,'volante_pov',{},[]), (4,14,'estrada_gps',{},[])], sons_extra=[(4,0,'chiado',{'vol':0.09},14)], rate_narr='+8%', destaque=['rádio','placa','poço'])
def p6(b): b(6, [(1,4,['portaria_ambar','corredor_magenta'],{},[H,O],{O:['seria','neutro']}), (5,8,['corredor_magenta','portaria_ambar'],{},[H,O],{O:['seria','encarando']}), (9,11,['quarto_coronel','quarto_coronel'],{},[H],{H:['lendo','assustado','medo']})], sons_extra=[(11,0.5,'stinger',{'vol':0.3})], destaque=['limpa','usada','caderno'])
def p7(b): b(7, [(1,3,'quarto_magenta',{},[H],{H:['cansada','neutro']}), (4,13,'corredor_magenta',{},[H],{H:'telefone'}), (14,15,'quarto_magenta',{},[H],{H:['medo','assustado']})], sons_extra=[(2,1.0,'celularToque',{'vol':0.3})], rate_narr='-4%', destaque=['pai','troquei','dele'])
def p8(b): b(8, [(1,4,['quarto_terra','corredor_magenta'],{},[H,M]), (5,17,['quarto_terra','quarto_terra','olhos_fechados'],{},[H],{H:'silencio'}), (18,18,'corredor_magenta',{},[H,M],{H:'medo'})], sons_extra=[(5,0,'respirar',{'vol':0.12},17), (13,0.2,'silencioDuck',{'dur':2.0})], destaque=['sim','entrar','porta'])
PLANOS = {1:p1,2:p2,3:p3,4:p4,5:p5,6:p6,7:p7,8:p8}
