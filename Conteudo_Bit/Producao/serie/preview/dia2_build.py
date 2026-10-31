import json
D='C:/Users/willi/Downloads/Projetos/Conteudo_Bit/Producao/serie/ep/'
def save(n,d): json.dump(d,open(D+n,'w',encoding='utf-8'),indent=2,ensure_ascii=False)
base=lambda **k: dict({"proxima":False,"legenda":"palavras","legendaY":1380,"legendaTam":125,"escurece":0.06,"saida":"contos-dia2","camadas":{"voz":1,"trilha":1,"efeitos":1,"musicaWav":0},"respiros":{"lead":0.12,"gap":0.2,"tail":0.4},"duck":0.35},**k)
sent=lambda i,pose,x,e=0.8: {"id":i,"pose":pose,"x":x,"escala":e,"semEntrada":True,"fica":True}
# ---- c05 Coração Delator
pol={"camisa":"#2A3550","calca":"#1C2234","cabelo":"#2A2A2A","pele":"#C99A74","estilo":"careca","bigode":True}
c05=base(numero=5,nome="O Coração Delator",cartela={"titulo":"O Coração Delator","sub":"Edgar Allan Poe · 1843"},cor="#D6C25A",arquivo="05_o_coracao_delator.mp4",destaque=["coração","olho","oitava"],sons="c05_sons.json",
 vozes={"narrador":["pt-BR-AntonioNeural","+14%","+0Hz"]},duck=0.4,
 eleven={"grito.wav":{"voz":"pNInz6obpgDQGcFmaJgB","texto":"[shouting] Tirem as tábuas! Aqui, aqui! É o coração dele!","estab":0.3,"pico":0.95}},
 elenco={"nar":{"camisa":"#6A5A2A","blusa":"#E8E2D4","calca":"#2A2418","cabelo":"#2A1E10","pele":"#D8B08C","estilo":"curto"},"p1":pol,"p2":dict(pol,cabelo="#6A6A6A"),"p3":dict(pol,bigode=False)},
 cenas=[
 {"cenario":"olho_close","aberto":1,"duracao":5,"zoom":[1,1.1],"rateNarrador":"+8%","narracao":"Ele jurava que era são. Só não suportava o olho do velho: pálido, azulado, como o de um abutre."},
 {"cenario":"quarto_velho","feixe":True,"duracao":5,"zoom":[1,1.08],"rateNarrador":"+12%","narracao":"Durante sete noites, à meia-noite, ele abria a porta do quarto devagar e olhava o velho dormir.","personagens":[sent("nar","lanterna",0.1,0.95)]},
 {"cenario":"olho_close","abreEm":0.7,"feixe":True,"duracao":4,"zoom":[1,1.14],"rateNarrador":"+16%","narracao":"Na oitava, o velho acordou. O olho estava aberto."},
 {"cenario":"assoalho","duracao":4.5,"zoom":[1,1.08],"rateNarrador":"+20%","narracao":"Ele não aguentou. Matou o velho e escondeu o corpo sob as tábuas do assoalho."},
 {"cenario":"sala_policia","cadeiras":[0.15,0.36,0.57,0.82],"duracao":6,"zoom":[1,1.06],"rateNarrador":"+22%","narracao":"A polícia chegou, por causa de um grito de vizinho. Ele os recebeu com calma. Ofereceu cadeiras. Sentou-se exatamente sobre o lugar.","personagens":[sent("p1","sentadaSeria",0.15),sent("p2","sentadaSeria",0.36),sent("p3","sentadaSeria",0.57),sent("nar","sentada",0.82)]},
 {"cenario":"sala_policia","bpm":70,"duracao":6,"zoom":[1,1.1],"rateNarrador":"+22%","narracao":"Eles conversavam. Ele sorria. Então ouviu um som baixo, abafado, regular, como um relógio embrulhado em algodão.","personagens":[{"id":"nar","pose":"sorrindo","x":0.5,"escala":1.7,"y":560,"semEntrada":True,"fica":True}]},
 {"cenario":"sala_policia","cadeiras":[0.15,0.36,0.57],"bpm":100,"duracao":5,"zoom":[1,1.1],"rateNarrador":"+30%","narracao":"Batia mais forte. Mais rápido. Os policiais continuavam conversando. Será que não ouviam?","personagens":[sent("p1","sentadaSeria",0.15),sent("p2","sentadaSeria",0.36),sent("p3","sentadaSeria",0.57),sent("nar","medo",0.86,0.9)]},
 {"cenario":"assoalho","bpm":130,"duracao":3,"zoom":[1,1.12],"respiro":1.0,"rateNarrador":"+8%","narracao":"Era o coração do velho."},
 {"cenario":"sala_policia","bpm":150,"duracao":4,"zoom":[1.05,1.2],"rateNarrador":"+25%","narracao":"Ele gritou:","falas":[{"quem":"grito","arquivo":"grito.wav","texto":"Tirem as tábuas! Aqui, aqui! É o coração dele!"}],"personagens":[{"id":"nar","pose":"assustado","x":0.5,"escala":1.7,"y":560,"semEntrada":True,"fica":True}]}])
save('c05_coracao_delator.json',c05)
save('c05_sons.json',{"versao":1,"episodio":"c05","nota":"Coracao Delator: drone grave, vento, batimento que acelera (cena 6 a 9) ate o grito.","cues":[
 {"cena":1,"offset":0,"tipo":"drone","ateCena":9,"params":{"tomInicial":38,"subida":3,"vol":0.3}},
 {"cena":1,"offset":0,"tipo":"vento","ateCena":4,"params":{"vol":0.2}},
 {"cena":6,"offset":0,"tipo":"batimento","ateCena":6,"params":{"bpm":70,"vol":0.4}},
 {"cena":7,"offset":0,"tipo":"batimento","ateCena":7,"params":{"bpm":100,"vol":0.6}},
 {"cena":8,"offset":0,"tipo":"batimento","ateCena":8,"params":{"bpm":130,"vol":0.8}},
 {"cena":9,"offset":0,"tipo":"batimento","ateCena":9,"params":{"bpm":150,"vol":1.0}}]})
# ---- c06 Loira
be={"camisa":"#F2F2F2","calca":"#2F4A7A","cabelo":"#2B1D16","pele":"#C99A74","estilo":"longo"}
lo={"camisa":"#D8D8E6","calca":"#D8D8E6","cabelo":"#E8D27A","pele":"#E8E2DC","estilo":"longo"}
c06=base(numero=6,nome="Loira do banheiro",cartela={"titulo":"Loira do banheiro","sub":"Folclore brasileiro"},cor="#E86FA8",arquivo="06_loira_do_banheiro.mp4",destaque=["loira","olha","três"],sons="c06_sons.json",
 vozes={"narrador":["pt-BR-ThalitaMultilingualNeural","+0%","+0Hz"],"bia":["pt-BR-ThalitaMultilingualNeural","+4%","+6Hz"],"dalva":["pt-BR-FranciscaNeural","-22%","-24Hz"]},
 elenco={"bia":be,"loira":lo},
 cenas=[
 {"cenario":"banheiro_escola","fechada":-1,"duracao":5,"zoom":[1,1.08],"rateNarrador":"+8%","pitchNarrador":"+10Hz","narracao":"Na escola da Bia, todo mundo conhecia a lenda. Se você chamar três vezes no banheiro, a Loira aparece."},
 {"cenario":"banheiro_escola","fechada":-1,"duracao":5,"zoom":[1,1.08],"rateNarrador":"+8%","pitchNarrador":"+8Hz","narracao":"No recreio, a Bia entrou sozinha numa cabine, trancou a porta e riu de si mesma.","personagens":[sent("bia","aliviada",0.5,0.95)]},
 {"cenario":"banheiro_escola","fechada":1,"duracao":4,"zoom":[1,1.1],"falas":[{"quem":"bia","texto":"Loira do banheiro. Loira do banheiro. Loira do banheiro."}]},
 {"cenario":"espelho_pia","fechada":-1,"duracao":5,"zoom":[1,1.06],"rateNarrador":"+0%","pitchNarrador":"+0Hz","narracao":"Nada. Riu de novo, mais alto. Saiu, lavou as mãos e olhou para o espelho."},
 {"cenario":"espelho_pia","fechada":2,"duracao":4,"zoom":[1,1.1],"rateNarrador":"-4%","pitchNarrador":"-6Hz","narracao":"Atrás dela, no reflexo, uma das cabines estava fechada."},
 {"cenario":"banheiro_escola","fechada":2,"luzSob":True,"duracao":5,"zoom":[1,1.08],"rateNarrador":"-8%","pitchNarrador":"-10Hz","narracao":"Ela tinha saído de uma cabine. As outras estavam todas abertas.","personagens":[sent("bia","neutro",0.15,0.8)]},
 {"cenario":"banheiro_escola","fechada":2,"luzSob":True,"duracao":6,"zoom":[1.1,1.3],"rateNarrador":"-12%","pitchNarrador":"-14Hz","narracao":"Alguém estava lá dentro. Uma voz baixa, quase um sussurro, disse:","falas":[{"quem":"dalva","texto":"Você me chamou. Só que eu não saio quando chamam."}]},
 {"cenario":"banheiro_escola","fechada":2,"abreEm":0.3,"luzSob":True,"duracao":4,"zoom":[1.1,1.25],"respiro":0.8,"rateNarrador":"-14%","pitchNarrador":"-16Hz","narracao":"A porta se abriu devagar."},
 {"cenario":"banheiro_escola","fechada":2,"abreEm":-5,"duracao":4,"zoom":[1.1,1.3],"falas":[{"quem":"dalva","texto":"Eu saio quando você olha."}],"personagens":[{"id":"loira","pose":"encarando","x":0.63,"escala":1.0,"semEntrada":True,"fica":True}]}])
save('c06_loira_banheiro.json',c06)
save('c06_sons.json',{"versao":1,"episodio":"c06","nota":"Loira: pinga e zumbido de lampada; rangido da porta; silencio na virada.","cues":[
 {"cena":1,"offset":0,"tipo":"pinga","ateCena":8,"params":{"vol":0.8}},
 {"cena":1,"offset":0,"tipo":"zumbidoLuz","ateCena":8,"params":{"vol":0.08}},
 {"cena":8,"offset":0.2,"tipo":"rangido","params":{"dur":2.4,"vol":0.9}},
 {"cena":9,"offset":0,"tipo":"stinger","params":{"intensidade":0.35}}]})
# ---- c07 Motorista
ana={"camisa":"#E0E0F0","calca":"#2F3A52","cabelo":"#1B1412","pele":"#D8B08C","estilo":"longo"}
m1={"camisa":"#2A2A32","calca":"#1C1C24","cabelo":"#1B1412","pele":"#D8B08C","estilo":"curto"}
m2={"camisa":"#4A7A5A","calca":"#1C2A22","cabelo":"#4A2E1E","pele":"#B98560","estilo":"curto","bigode":True}
c07=base(numero=7,nome="Motorista de app",cartela={"titulo":"Motorista de app","sub":"Original · não entre"},cor="#8A5CE0",arquivo="07_motorista_de_app.mp4",destaque=["ana","corolla","gol","nome"],sons="c07_sons.json",
 vozes={"narrador":["pt-BR-FranciscaNeural","+20%","+0Hz"],"mot1":["pt-BR-AntonioNeural","+0%","+0Hz"],"mot2":["pt-BR-AntonioNeural","-6%","-4Hz"]},
 elenco={"ana":ana,"m1":m1,"m2":m2},
 cenas=[
 {"cenario":"rua_roxa","duracao":3.5,"zoom":[1,1.08],"narracao":"Pedi um carro às duas da manhã.","personagens":[sent("ana","neutro",0.25,0.9)],"objetos":[{"tipo":"celular_app","x":0.72,"y":0.42,"escala":0.6,"nome":"A.","carro":"prata","msg":"A CAMINHO","entra":0.4}]},
 {"cenario":"carro_janela","cor":"preto","duracao":5,"zoom":[1,1.08],"narracao":"O carro parou e o vidro desceu. O motorista sorriu:","falas":[{"quem":"mot1","texto":"Boa noite, Ana! Pode entrar."}],"personagens":[{"id":"m1","pose":"sorrindo","x":0.5,"escala":1.25,"semEntrada":True,"fica":True}],"objetos":[{"tipo":"porta_carro","cor":"preto","entra":0}]},
 {"cenario":"rua_roxa","carros":[{"x":600,"esc":0.8,"cor":"preto"}],"duracao":5,"zoom":[1,1.08],"narracao":"Eu não tinha dito meu nome. O aplicativo mostra só a inicial.","personagens":[sent("ana","hesitante",0.15,0.85)],"objetos":[{"tipo":"celular_app","x":0.72,"y":0.3,"escala":0.5,"nome":"A.","carro":"prata","msg":"A CAMINHO","entra":0}]},
 {"cenario":"rua_roxa","carros":[{"x":600,"esc":0.8,"cor":"preto"}],"duracao":8,"zoom":[1,1.06],"narracao":"Abri a porta de trás e olhei o celular: o carro do app era um Gol prata. Aquele era um Corolla preto.","personagens":[sent("ana","assustado",0.15,0.85)],"objetos":[{"tipo":"celular_app","x":0.72,"y":0.3,"escala":0.6,"nome":"A.","carro":"prata","msg":"A CAMINHO","entra":0}]},
 {"cenario":"carro_janela","cor":"preto","duracao":7,"zoom":[1,1.12],"narracao":"Fechei a porta de volta e dei um passo atrás. O motorista continuou sorrindo. Não ligou o motor, não se mexeu.","personagens":[{"id":"m1","pose":"sorrindo","x":0.5,"escala":1.25,"semEntrada":True,"fica":True}],"objetos":[{"tipo":"porta_carro","cor":"preto","entra":0}]},
 {"cenario":"rua_roxa","carros":[{"x":640,"esc":0.8,"cor":"prata"}],"duracao":6,"zoom":[1,1.08],"narracao":"Dois minutos depois, um Gol prata parou na esquina. O Corolla preto já tinha ido embora.","personagens":[sent("ana","hesitante",0.15,0.85)]},
 {"cenario":"carro_janela","cor":"prata","duracao":4.5,"zoom":[1,1.08],"narracao":"O motorista do Gol perguntou:","falas":[{"quem":"mot2","texto":"Você é a Ana?"}],"personagens":[{"id":"m2","pose":"neutro","x":0.5,"escala":1.25,"semEntrada":True,"fica":True}],"objetos":[{"tipo":"porta_carro","cor":"prata","entra":0}]},
 {"cenario":"carro_janela","cor":"prata","duracao":7,"zoom":[1,1.1],"narracao":"Eu mal consegui responder. Ele deu de ombros:","falas":[{"quem":"mot2","texto":"Estranho. Eu cheguei agora. Quem estava falando com você?"}],"respiro":2.0,"personagens":[{"id":"m2","pose":"negando","x":0.5,"escala":1.25,"semEntrada":True,"fica":True}],"objetos":[{"tipo":"porta_carro","cor":"prata","entra":0}]}])
save('c07_motorista_app.json',c07)
save('c07_sons.json',{"versao":1,"episodio":"c07","nota":"Motorista: sem musica; ping do app, motor em marcha lenta, vento.","cues":[
 {"cena":1,"offset":0.2,"tipo":"celularToque","params":{"abafado":True,"vol":0.5}},
 {"cena":1,"offset":0,"tipo":"vento","ateCena":8,"params":{"vol":0.2}},
 {"cena":2,"offset":0,"tipo":"elevadorZumbido","ateCena":2,"params":{"vol":0.3}},
 {"cena":5,"offset":0,"tipo":"elevadorZumbido","ateCena":5,"params":{"vol":0.3}},
 {"cena":7,"offset":0,"tipo":"elevadorZumbido","ateCena":8,"params":{"vol":0.3}}]})
# ---- c08 Luz do banheiro
L="pFZP5JQG7iQjIQuC4Bku"
tx=["Moro sozinha há dois anos... Ontem, de madrugada, vi uma luz embaixo da porta do banheiro.","Eu sempre apago. Abri, e a lâmpada estava acesa.","Apaguei e fui lavar o rosto. A luz acendeu de novo.","Aí eu olhei para o espelho.","Meu reflexo estava normal. Mas atrás dele, a porta do banheiro estava aberta... escancarada, e o corredor escuro lá fora.","Eu sempre fecho aquela porta. Eu tinha fechado.","Virei devagar. A porta real estava fechada.","Olhei para o espelho de novo.","Meu reflexo ainda estava de frente para o espelho... Eu já tinha virado."]
leg=[t.replace('...','.') for t in tx]
cen=[{"cenario":"corredor_ciano","pisca":True},{"cenario":"banheiro_ciano"},{"cenario":"banheiro_ciano","piscaEm":2.4},{"cenario":"banheiro_ciano","espelho":True},{"cenario":"banheiro_ciano","espelho":True,"portaRefAberta":True},{"cenario":"banheiro_ciano","espelho":True,"portaRefAberta":True},{"cenario":"porta_ciano"},{"cenario":"banheiro_ciano","espelho":True,"portaRefAberta":True},{"cenario":"banheiro_ciano","espelho":True,"portaRefAberta":True,"refCostas":True}]
zm=[[1,1.08],[1,1.08],[1,1.08],[1,1.1],[1.02,1.12],[1.1,1.24],[1,1.08],[1,1.1],[1.04,1.2]]
for i,c in enumerate(cen):
    c["zoom"]=zm[i]; c["duracao"]=3; c["falas"]=[{"quem":"ana","arquivo":f"ana_{i+1}.wav","texto":leg[i]}]
cen[8]["respiro"]=2.0
c08=base(numero=8,nome="Luz do banheiro",cartela={"titulo":"Luz do banheiro","sub":"Original · não olhe o espelho"},cor="#8FE3E8",arquivo="08_luz_do_banheiro.mp4",destaque=["espelho","virado","aberta"],sons="c08_sons.json",
 respiros={"lead":0.3,"gap":0.3,"tail":0.7},duck=0.4,
 eleven={f"ana_{i+1}.wav":{"voz":L,"texto":"[whispers] "+tx[i],"pico":0.5} for i in range(9)},cenas=cen)
save('c08_luz_banheiro.json',c08)
save('c08_sons.json',{"versao":1,"episodio":"c08","nota":"Luz do banheiro: sussurro; zumbido de lampada e pingo; silencio total na ultima fala.","cues":[
 {"cena":1,"offset":0,"tipo":"zumbidoLuz","ateCena":8,"params":{"vol":0.1}},
 {"cena":2,"offset":0,"tipo":"pinga","ateCena":8,"params":{"vol":0.5,"intervalo":2.4}},
 {"cena":9,"offset":0,"tipo":"corte","params":{}}]})
idx=json.load(open(D+'indice.json',encoding='utf-8'))
idx.update({"c05":"c05_coracao_delator.json","c06":"c06_loira_banheiro.json","c07":"c07_motorista_app.json","c08":"c08_luz_banheiro.json"})
json.dump(idx,open(D+'indice.json','w',encoding='utf-8'),indent=2,ensure_ascii=False)
