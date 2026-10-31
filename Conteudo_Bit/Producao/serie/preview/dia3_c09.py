import json,os
exec(open('C:/Users/willi/Downloads/Projetos/Conteudo_Bit/Producao/serie/preview/dia3_build.py',encoding='utf-8').read().split('# ---------- c09')[0])
BILL="pqHfZKP75CvOlQylNhV4"
t9=["Procópio foi ser enfermeiro do coronel Felisberto, um velho cruel que se deleitava com a dor dos outros.",
"Na noite de vinte e quatro de agosto de 1860, o coronel teve um acesso de fúria. Procópio adormeceu, e acordou com os gritos.",
"Levou uma moringa na cara. Houve uma luta. Suas mãos apertaram o pescoço do velho. O coronel morreu.",
"Procópio escondeu as marcas e chamou o vigário e o médico. Ninguém desconfiou.",
"O coronel deixou a ele toda a herança. Ele deu uma parte e ergueu um túmulo de mármore.",
"O remorso pesava. Mas aos poucos o povo falou mal do morto, e Procópio sentiu alívio.",
"No fim, escreveu uma emenda ao Sermão da Montanha: Bem-aventurados os que possuem, porque eles serão consolados."]
cen9=[
 {"cenario":"varanda_vila","duracao":4,"zoom":[1,1.08],"personagens":[sent("proc","neutro",0.3,0.95)]},
 {"cenario":"quarto_coronel","grita":True,"hora":[11,50],"duracao":5,"zoom":[1,1.08],"personagens":[sent("proc","cansada",0.2)]},
 {"cenario":"quarto_coronel","luta":True,"hora":[0,5],"duracao":5,"zoom":[1,1.1],"escurece":0.15},
 {"cenario":"quarto_coronel","lencol":True,"dia":True,"hora":[6,0],"duracao":5,"zoom":[1,1.06],"personagens":[sent("proc","neutro",0.17,0.85),sent("vig","assentindo",0.45,0.85),sent("med","assentindo",0.72,0.85)]},
 {"cenario":"tumulo","duracao":5,"zoom":[1,1.08],"personagens":[sent("proc","cansada",0.2,0.95)]},
 {"cenario":"varanda_vila","duracao":5,"zoom":[1,1.08],"personagens":[sent("proc","aliviada",0.5,0.95)]},
 {"cenario":"fundo_cor","topo":"#4A3A22","base":"#1A1208","brilho":"#C9A56A","brilhoY":700,"duracao":6,"zoom":[1.02,1.18],"textoTela":"BEM-AVENTURADOS OS QUE POSSUEM","textoY":330,"textoEntra":4.6,"respiro":1.2,"personagens":[sent("proc","sorrindo",0.5,1.7,y=560)]}]
for i,c in enumerate(cen9): c["falas"]=[{"quem":"proc","arquivo":f"e{i+1}.wav","texto":t9[i]}]
old=json.load(open(D+'c09_enfermeiro.json',encoding='utf-8'))
old.update({"eleven":{f"e{i+1}.wav":{"voz":BILL,"texto":"[solemnly] "+t9[i],"pico":0.6} for i in range(7)},"cenas":cen9,"respiros":{"lead":0.15,"gap":0.25,"tail":0.4}})
save('c09_enfermeiro.json',old)
save('c09_sons.json',{"versao":1,"episodio":"c09","nota":"Enfermeiro: solene; relogio de parede (tique-taque lento) nas cenas do quarto, drone grave, batidas na luta e silencio, vento na varanda.","cues":[
 {"cena":1,"offset":0,"tipo":"drone","ateCena":7,"params":{"tomInicial":36,"subida":1,"vol":0.25}},
 {"cena":1,"offset":0,"tipo":"vento","ateCena":1,"params":{"vol":0.2}},
 {"cena":2,"offset":0,"tipo":"tiquetaque","ateCena":4,"params":{"lentidao":0.7,"vol":0.4}},
 {"cena":3,"offset":0.9,"tipo":"batidas","params":{"n":3,"espacamento":0.45,"vol":0.5}},
 {"cena":3,"offset":3.0,"tipo":"silencio","params":{"dur":1.6}},
 {"cena":5,"offset":0,"tipo":"vento","ateCena":6,"params":{"vol":0.15}},
 {"cena":7,"offset":0,"tipo":"tiquetaque","ateCena":7,"params":{"lentidao":0.7,"vol":0.3}}]})
d=json.load(open(D+'c10_sons.json',encoding='utf-8'))
for c in d['cues']:
    if c['tipo']=='assobio': c['params']['vol']=0.45
    if c['tipo']=='drone': c['params']['vol']=0.2
    if c['tipo']=='grilos': c['params']['vol']=2.2
json.dump(d,open(D+'c10_sons.json','w',encoding='utf-8'),indent=2,ensure_ascii=False)
