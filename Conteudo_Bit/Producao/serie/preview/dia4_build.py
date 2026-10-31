import json
D='C:/Users/willi/Downloads/Projetos/Conteudo_Bit/Producao/serie/ep/'
def save(n,d): json.dump(d,open(D+n,'w',encoding='utf-8'),indent=2,ensure_ascii=False)
base=lambda **k: dict({"proxima":False,"legenda":"palavras","legendaY":1380,"legendaTam":125,"escurece":0.06,"saida":"contos-dia4","camadas":{"voz":1,"trilha":1,"efeitos":1,"musicaWav":0},"respiros":{"lead":0.12,"gap":0.2,"tail":0.4},"duck":0.35},**k)
sent=lambda i,pose,x,e=0.9,**k: dict({"id":i,"pose":pose,"x":x,"escala":e,"semEntrada":True,"fica":True},**k)
# ---------- c13 O Gato Preto ----------
DAN="onwK4e9ZLuTAKqWW03F9"
t13=["Ele amava os animais. Até que a bebida o transformou.",
"Num ataque de raiva, fez mal a Plutão, seu gato preto, e depois cometeu algo ainda pior.",
"Naquela noite, um incêndio destruiu a casa. Só ficou uma parede, com a silhueta de um gato gigante marcada no reboco.",
"Tempos depois, achou numa taberna outro gato preto, quase igual, com uma mancha branca no peito. Dia após dia, a mancha ia ganhando a forma de uma forca.",
"No porão, o gato quase o derrubou na escada. Ele ergueu um machado. A esposa segurou seu braço. E o golpe caiu nela.",
"Ele a emparedou no porão. No quarto dia, a polícia veio, e nada achou.",
"Ao sair, ele bateu na parede com a bengala, orgulhoso: Cavalheiros, é uma construção sólida.",
"E de dentro da parede, veio um uivo."]
cen13=[
 {"cenario":"taberna","gato":True,"duracao":4,"zoom":[1,1.08],"personagens":[sent("nar","neutro",0.62,0.9)]},
 {"cenario":"taberna","gato":True,"close":True,"duracao":5,"zoom":[1,1.1],"escurece":0.5},
 {"cenario":"casa_queimada","duracao":6,"zoom":[1,1.08]},
 {"cenario":"taberna","gato":True,"close":True,"forca":True,"duracao":8,"zoom":[1,1.1]},
 {"cenario":"porao","sombra":True,"duracao":7,"zoom":[1,1.08],"personagens":[sent("esp","medo",0.84,0.8)]},
 {"cenario":"porao","parede":"nova","duracao":5,"zoom":[1,1.08],"personagens":[sent("nar","neutro",0.2,0.9)]},
 {"cenario":"porao","parede":"nova","duracao":6,"zoom":[1,1.08],"personagens":[sent("nar","apontando",0.2,0.9),sent("pol1","neutro",0.62,0.9),sent("pol2","neutro",0.8,0.9)]},
 {"cenario":"porao","parede":"desaba","desabaEm":1.2,"duracao":5,"zoom":[1.04,1.14],"respiro":1.2}]
for i,c in enumerate(cen13): c["falas"]=[{"quem":"nar","arquivo":f"g{i+1}.wav","texto":t13[i]}]
c13=base(numero=13,nome="O Gato Preto",cartela={"titulo":"O Gato Preto","sub":"Edgar Allan Poe · 1843"},cor="#8A94A6",arquivo="13_o_gato_preto.mp4",destaque=["gato","forca","parede","uivo"],sons="c13_sons.json",
 respiros={"lead":0.2,"gap":0.3,"tail":0.5},duck=0.4,
 eleven={f"g{i+1}.wav":{"voz":DAN,"texto":"[dramatically] "+t13[i],"pico":0.6} for i in range(8)},
 elenco={"nar":{"camisa":"#2A2E44","blusa":"#E8E2D4","calca":"#1C1C24","cabelo":"#3A2A22","pele":"#D8B08C","estilo":"curto","bigode":True},"esp":{"camisa":"#7A5A6A","calca":"#7A5A6A","cabelo":"#4A3A32","pele":"#E0BC9C","estilo":"longo"},"pol1":{"camisa":"#2A3550","calca":"#1C2234","cabelo":"#2A2A2A","pele":"#C99A74","estilo":"careca","bigode":True},"pol2":{"camisa":"#2A3550","calca":"#1C2234","cabelo":"#6A6A6A","pele":"#C99A74","estilo":"careca"}},cenas=cen13)
save('c13_gato_preto.json',c13)
save('c13_sons.json',{"versao":1,"episodio":"c13","nota":"Gato Preto: solene, pouca musica; drone grave, vento, crepitar do incendio, batimento lento no porao, uivo e gongo seco no final.","cues":[
 {"cena":1,"offset":0,"tipo":"drone","ateCena":8,"params":{"tomInicial":38,"subida":2,"vol":0.28}},
 {"cena":1,"offset":0,"tipo":"vento","ateCena":2,"params":{"vol":0.2}},
 {"cena":3,"offset":0,"tipo":"crepitar","ateCena":3,"params":{"vol":0.3}},
 {"cena":5,"offset":0,"tipo":"batimento","ateCena":7,"params":{"bpm":56,"vol":0.4}},
 {"cena":8,"offset":0.5,"tipo":"uivoGato","params":{"dur":2.4,"vol":1.0}},
 {"cena":8,"offset":2.0,"tipo":"gongo","params":{"vol":1.0}}]})
# ---------- c14 Mula sem cabeça ----------
c14=base(numero=14,nome="Mula sem cabeça",cartela={"titulo":"Mula sem cabeça","sub":"Folclore brasileiro"},cor="#FF7A1A",arquivo="14_mula_sem_cabeca.mp4",destaque=["mula","galope","fogo","ferradura"],sons="c14_sons.json",
 vozes={"narrador":["pt-BR-ThalitaMultilingualNeural","+16%","+6Hz"],"viz":["pt-BR-FranciscaNeural","+8%","-8Hz"]},
 elenco={"viz":{"camisa":"#7A9A6A","blusa":"#E8E2D4","calca":"#4A3A4A","cabelo":"#4A3A32","pele":"#C99A74","estilo":"coque"}},
 cenas=[
 {"cenario":"vila_noite","mula":{"x0":-400,"x1":1500,"dur":7,"ini":8,"esc":1.2},"brilho":0.15,"duracao":12,"zoom":[1,1.06],"narracao":"Na vila de Seu João, todo mundo sabia: de quinta para sexta, uma mulher amaldiçoada galopava pelas ruas como uma mula de fogo. Sem cabeça. Chamas no lugar do pescoço."},
 {"cenario":"vila_noite","duracao":5,"zoom":[1,1.08],"narracao":"A vizinha avisava:","falas":[{"quem":"viz","texto":"Se ouvir o galope, tranque tudo e não olhe!"}],"personagens":[sent("viz","silencio",0.5,0.95)]},
 {"cenario":"vila_noite","brilho":0.6,"duracao":6,"zoom":[1,1.1],"narracao":"Naquela noite, o galope chegou. Casco, casco, casco, cada vez mais forte. A rua inteira se calou."},
 {"cenario":"janela_quarto","olhos":"fechados","fogo":0.4,"duracao":3.5,"zoom":[1,1.08],"narracao":"Seu João ficou na cama, de olhos fechados."},
 {"cenario":"janela_quarto","olhos":"abertos","fogo":0.5,"fresta":0.3,"duracao":5,"zoom":[1,1.08],"narracao":"Mas a curiosidade falou mais alto. Ele abriu uma frestinha da janela."},
 {"cenario":"janela_quarto","olhos":"abertos","fogo":1,"fresta":0.7,"mulaJanela":True,"duracao":5,"zoom":[1,1.1],"narracao":"Viu o brilho laranja, o fogo, a forma que passava veloz."},
 {"cenario":"vila_noite","mulaParada":540,"brilho":1,"duracao":5,"zoom":[1,1.1],"narracao":"E depois, um relincho. Que parou bem em frente à casa dele."},
 {"cenario":"porta_ferradura","duracao":8,"zoom":[1,1.08],"respiro":1.2,"narracao":"Na manhã seguinte, os vizinhos acharam a janela dele aberta. E na porta, queimada na madeira, uma ferradura."}])
save('c14_mula.json',c14)
save('c14_sons.json',{"versao":1,"episodio":"c14","nota":"Mula: galope que cresce (cenas 1 a 6), relincho na 7, fogo crepitando, grilos no comeco, passaros de manha.","cues":[
 {"cena":1,"offset":0,"tipo":"grilos","ateCena":2,"params":{"vol":2.2,"n":4}},
 {"cena":1,"offset":8,"tipo":"galope","params":{"dur":6,"de":0.1,"para":0.6,"vol":0.7}},
 {"cena":3,"offset":0,"tipo":"galope","ateCena":4,"params":{"de":0.2,"para":1.0,"vol":0.7}},
 {"cena":5,"offset":0,"tipo":"galope","ateCena":6,"params":{"de":0.8,"para":0.8,"vol":0.6}},
 {"cena":6,"offset":0,"tipo":"crepitar","ateCena":7,"params":{"vol":0.25}},
 {"cena":7,"offset":0.4,"tipo":"relincho","params":{"vol":1.0}},
 {"cena":8,"offset":0,"tipo":"passaros","ateCena":8,"params":{"vol":0.6}}]})
# ---------- c15 GPS ----------
c15=base(numero=15,nome="GPS",cartela={"titulo":"GPS","sub":"Original · não vire"},cor="#39FF88",arquivo="15_gps.mp4",destaque=["gps","mato","casa","minha"],sons="c15_sons.json",
 vozes={"narrador":["pt-BR-AntonioNeural","-4%","-6Hz"],"gps":["pt-BR-ThalitaMultilingualNeural","+0%","-2Hz"]},
 cenas=[
 {"cenario":"estrada_gps","duracao":4,"zoom":[1,1.06],"narracao":"Dirigia de madrugada, voltando de uma viagem."},
 {"cenario":"gps_tela","linha1":"VIRE À DIREITA","linha2":"EM 200 m","duracao":4,"zoom":[1,1.06],"narracao":"O GPS falou:","falas":[{"quem":"gps","texto":"Vire à direita."}]},
 {"cenario":"estrada_gps","mato":True,"duracao":4,"zoom":[1,1.08],"narracao":"Olhei. Na direita, só mato."},
 {"cenario":"gps_tela","linha1":"RECALCULANDO...","linha2":"VIRE À DIREITA","duracao":6,"zoom":[1,1.06],"narracao":"Continuei reto. O GPS recalculou. A voz parecia irritada. Segundos depois:","falas":[{"quem":"gps","texto":"Vire à direita."}]},
 {"cenario":"estrada_gps","mato":True,"duracao":7,"zoom":[1,1.08],"narracao":"De novo, mato. Na terceira vez, parei o carro. Digitei o destino de novo: Casa."},
 {"cenario":"gps_tela","linha1":"DESTINO: CASA","linha2":"CHEGADA","duracao":5,"zoom":[1,1.06],"narracao":"O GPS respondeu:","falas":[{"quem":"gps","texto":"Você chegou ao seu destino."}]},
 {"cenario":"casa_dois_andares","duracao":6,"zoom":[1,1.08],"narracao":"Levantei os olhos. Estava na frente de uma casa de dois andares, que eu nunca vi na vida."},
 {"cenario":"casa_dois_andares","garagem":True,"duracao":4,"zoom":[1,1.1],"narracao":"Na garagem, meu carro. Igualzinho ao que eu dirigia."},
 {"cenario":"casa_dois_andares","garagem":True,"janela":True,"duracao":6,"zoom":[1,1.14],"respiro":1.8,"narracao":"Na janela do segundo andar, uma luz acesa. E, de costas, uma silhueta. A minha."}])
save('c15_gps.json',c15)
save('c15_sons.json',{"versao":1,"episodio":"c15","nota":"GPS: motor em marcha, bip do GPS antes da voz, silencio e stinger na ultima cena.","cues":[
 {"cena":1,"offset":0,"tipo":"elevadorZumbido","ateCena":8,"params":{"vol":0.3}},
 {"cena":2,"offset":0.8,"tipo":"ding","params":{"vol":0.5}},
 {"cena":4,"offset":3.0,"tipo":"ding","params":{"vol":0.5}},
 {"cena":6,"offset":0.6,"tipo":"ding","params":{"vol":0.5}},
 {"cena":9,"offset":0,"tipo":"corte","params":{}},
 {"cena":9,"offset":0.0,"tipo":"stinger","params":{"intensidade":0.3}}]})
# ---------- c16 Pisadeira ----------
ROG="CwhRBWXzGAHq8TQ4Fs17"
t16=["Dormi de barriga cheia, como a minha avó sempre dizia para não fazer.",
"Às três da manhã, acordei. Não conseguia me mexer. Nem o dedo. Nem a boca para gritar.",
"Sentia um peso enorme no peito.",
"Veio à cabeça o que a vovó me contou da Pisadeira: uma velha de unhas compridas, que anda pelos telhados e pisa no peito de quem dorme de barriga cheia.",
"Eu só precisava manter os olhos fechados.",
"O peso se mexia. Subiu para o pescoço. Duas unhas frias, finas, encostaram no meu queixo.",
"Uma voz rouca sussurrou:",
"Aguentei até o dia clarear. Quando o peso sumiu, abri os olhos.",
"Tinha quatro marcas de unha no meu peito. E uma telha quebrada no teto."]
cen16=[
 {"cenario":"quarto_terra","olhos":"fechados"},{"cenario":"quarto_terra","olhos":"abertos"},{"cenario":"quarto_terra","olhos":"abertos","peso":True},
 {"cenario":"telhado_noite"},{"cenario":"olhos_fechados"},{"cenario":"olhos_fechados","unhas":True},
 {"cenario":"olhos_fechados","unhas":True,"unhasEm":-3},{"cenario":"quarto_terra","manha":True,"olhos":"abertos","telha":True},
 {"cenario":"quarto_terra","manha":True,"olhos":"abertos","marcas":True,"telha":True,"respiro":1.8}]
for i,c in enumerate(cen16):
    c["duracao"]=3; c["zoom"]=[1,1.08]; c["falas"]=[{"quem":"eu","arquivo":f"p{i+1}.wav","texto":t16[i]}]
cen16[6]["falas"].append({"quem":"pisa","texto":"Abre. Só um pouquinho."})
c16=base(numero=16,nome="Pisadeira",cartela={"titulo":"Pisadeira","sub":"Folclore brasileiro"},cor="#D2693A",arquivo="16_pisadeira.mp4",destaque=["pisadeira","olhos","abre","unha"],sons="c16_sons.json",
 vozes={"pisa":["pt-BR-FranciscaNeural","-26%","-28Hz"]},respiros={"lead":0.25,"gap":0.3,"tail":0.6},duck=0.4,
 eleven={f"p{i+1}.wav":{"voz":ROG,"texto":"[whispers] "+t16[i],"pico":0.5} for i in range(9)},cenas=cen16)
save('c16_pisadeira.json',c16)
save('c16_sons.json',{"versao":1,"episodio":"c16","nota":"Pisadeira: sussurro; respiracao lenta, drone baixissimo, unha raspando nas cenas 6 e 7, silencio na ultima.","cues":[
 {"cena":1,"offset":0,"tipo":"respirar","ateCena":8,"params":{"vol":0.5,"ritmo":3.4}},
 {"cena":1,"offset":0,"tipo":"drone","ateCena":8,"params":{"tomInicial":38,"subida":1,"vol":0.2}},
 {"cena":6,"offset":0.5,"tipo":"raspar","ateCena":7,"params":{"vol":0.8}},
 {"cena":9,"offset":0,"tipo":"corte","params":{}}]})
idx=json.load(open(D+'indice.json',encoding='utf-8'))
idx.update({"c13":"c13_gato_preto.json","c14":"c14_mula.json","c15":"c15_gps.json","c16":"c16_pisadeira.json"})
json.dump(idx,open(D+'indice.json','w',encoding='utf-8'),indent=2,ensure_ascii=False)
