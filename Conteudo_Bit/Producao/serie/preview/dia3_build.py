import json
D='C:/Users/willi/Downloads/Projetos/Conteudo_Bit/Producao/serie/ep/'
def save(n,d): json.dump(d,open(D+n,'w',encoding='utf-8'),indent=2,ensure_ascii=False)
base=lambda **k: dict({"proxima":False,"legenda":"palavras","legendaY":1380,"legendaTam":125,"escurece":0.06,"saida":"contos-dia3","camadas":{"voz":1,"trilha":1,"efeitos":1,"musicaWav":0},"respiros":{"lead":0.12,"gap":0.2,"tail":0.4},"duck":0.35},**k)
sent=lambda i,pose,x,e=0.9,**k: dict({"id":i,"pose":pose,"x":x,"escala":e,"semEntrada":True,"fica":True},**k)
# ---------- c09 O Enfermeiro (sépia) ----------
BILL="pqHfZKP75CvOlQylNhV4"
t9=["Procópio aceitou ser enfermeiro do coronel Felisberto, numa vila do interior. Doente e cruel, o velho se deleitava com a dor dos outros.",
"Procópio aguentou insultos e humilhações, sem dormir direito.",
"Na noite de vinte e quatro de agosto de 1860, o coronel teve um acesso de fúria. Procópio adormeceu, e acordou com os gritos.",
"Levou uma moringa na cara. Houve uma luta. Suas mãos apertaram o pescoço do velho. O coronel morreu.",
"Procópio escondeu as marcas, vestiu o corpo, chamou o vigário e o médico. Ninguém desconfiou.",
"O coronel deixou a ele toda a herança. Ele deu uma parte e ergueu um túmulo de mármore.",
"O remorso pesava. Mas aos poucos o povo falou mal do morto, e Procópio sentiu alívio.",
"No fim, escreveu uma emenda ao Sermão da Montanha: Bem-aventurados os que possuem, porque eles serão consolados."]
cen9=[
 {"cenario":"varanda_vila","duracao":4,"zoom":[1,1.08],"personagens":[sent("proc","neutro",0.3,0.95)]},
 {"cenario":"quarto_coronel","grita":True,"hora":[11,10],"duracao":4,"zoom":[1,1.08],"personagens":[sent("proc","cansada",0.2)]},
 {"cenario":"quarto_coronel","hora":[11,55],"duracao":5,"zoom":[1,1.1],"personagens":[sent("proc","cansada",0.2)]},
 {"cenario":"quarto_coronel","luta":True,"hora":[0,5],"duracao":5,"zoom":[1,1.1],"escurece":0.15},
 {"cenario":"quarto_coronel","lencol":True,"dia":True,"hora":[6,0],"duracao":5,"zoom":[1,1.06],"personagens":[sent("proc","neutro",0.17,0.85),sent("vig","assentindo",0.45,0.85),sent("med","assentindo",0.72,0.85)]},
 {"cenario":"tumulo","duracao":5,"zoom":[1,1.08],"personagens":[sent("proc","cansada",0.2,0.95)]},
 {"cenario":"varanda_vila","duracao":5,"zoom":[1,1.08],"personagens":[sent("proc","aliviada",0.5,0.95)]},
 {"cenario":"fundo_cor","topo":"#4A3A22","base":"#1A1208","brilho":"#C9A56A","brilhoY":700,"duracao":6,"zoom":[1.02,1.18],"textoTela":"BEM-AVENTURADOS OS QUE POSSUEM","textoY":330,"textoEntra":4.6,"respiro":1.5,"personagens":[sent("proc","sorrindo",0.5,1.7,y=560)]}]
for i,c in enumerate(cen9): c["falas"]=[{"quem":"proc","arquivo":f"e{i+1}.wav","texto":t9[i]}]
c09=base(numero=9,nome="O Enfermeiro",cartela={"titulo":"O Enfermeiro","sub":"Machado de Assis · 1896"},cor="#C9A56A",arquivo="09_o_enfermeiro.mp4",destaque=["procópio","coronel","herança","possuem"],sons="c09_sons.json",
 respiros={"lead":0.2,"gap":0.3,"tail":0.6},duck=0.4,
 eleven={f"e{i+1}.wav":{"voz":BILL,"texto":"[solemnly] "+t9[i],"pico":0.6} for i in range(8)},
 elenco={"proc":{"camisa":"#6A5A3A","blusa":"#E8E2D4","calca":"#2A2418","cabelo":"#2A1E10","pele":"#D8B08C","estilo":"curto"},"vig":{"camisa":"#17131B","calca":"#17131B","cabelo":"#8C8B86","pele":"#D8B08C","estilo":"careca"},"med":{"camisa":"#3A3A4A","blusa":"#E8E2D4","calca":"#2A2A34","cabelo":"#2A2A2A","pele":"#C99A74","estilo":"curto","bigode":True}},cenas=cen9)
save('c09_enfermeiro.json',c09)
save('c09_sons.json',{"versao":1,"episodio":"c09","nota":"Enfermeiro: solene; relogio de parede ao fundo (tique-taque lento) nas cenas do quarto, drone grave, batidas na luta e silencio, vento na varanda.","cues":[
 {"cena":1,"offset":0,"tipo":"drone","ateCena":8,"params":{"tomInicial":36,"subida":1,"vol":0.25}},
 {"cena":1,"offset":0,"tipo":"vento","ateCena":1,"params":{"vol":0.2}},
 {"cena":2,"offset":0,"tipo":"tiquetaque","ateCena":5,"params":{"lentidao":0.7,"vol":0.4}},
 {"cena":4,"offset":0.9,"tipo":"batidas","params":{"n":3,"espacamento":0.45,"vol":0.5}},
 {"cena":4,"offset":3.0,"tipo":"silencio","params":{"dur":1.6}},
 {"cena":6,"offset":0,"tipo":"vento","ateCena":7,"params":{"vol":0.15}},
 {"cena":8,"offset":0,"tipo":"tiquetaque","ateCena":8,"params":{"lentidao":0.7,"vol":0.3}}]})
# ---------- c10 Curupira (verde-floresta) ----------
pg=lambda n,x0,y0,tb: [[x0+(30 if i%2 else -30),y0+i*130,1.0,tb] for i in range(n)]
c10=base(numero=10,nome="Curupira",cartela={"titulo":"Curupira","sub":"Folclore brasileiro"},cor="#3CB371",arquivo="10_curupira.mp4",destaque=["pegadas","curupira","fogo","duas"],sons="c10_sons.json",
 vozes={"narrador":["pt-BR-AntonioNeural","-8%","-8Hz"],"cur":["pt-BR-ThalitaMultilingualNeural","-10%","+28Hz"]},
 elenco={"cac":{"camisa":"#6A4A2A","calca":"#3A3A2A","cabelo":"#2A1E10","pele":"#B98560","estilo":"curto","mochila":"#4A3A22"},"cur":{"camisa":"#3A6A3A","calca":"#2A4A2A","cabelo":"#E8401A","pele":"#D8B08C","estilo":"curto"}},
 cenas=[
 {"cenario":"mata_noite","duracao":4,"zoom":[1,1.08],"narracao":"O caçador se perdeu na floresta ao entardecer.","personagens":[sent("cac","procurando",0.3)]},
 {"cenario":"pegadas_close","duracao":6,"zoom":[1,1.08],"narracao":"Achou pegadas no chão úmido e pensou: Alguém passou por aqui. Vou seguir para sair."},
 {"cenario":"mata_noite","clareira":True,"pegadas":pg(4,540,1330,False),"duracao":5,"zoom":[1,1.08],"narracao":"Andou por uma hora. As pegadas continuavam, firmes, em direção à clareira.","personagens":[sent("cac","olhando",0.3)]},
 {"cenario":"pegadas_close","reverso":True,"realce":True,"duracao":6,"zoom":[1,1.1],"narracao":"Só então ele reparou: os dedos dos pés estavam virados para trás. O calcanhar apontava para a frente."},
 {"cenario":"mata_noite","noite":True,"duracao":5,"zoom":[1,1.1],"narracao":"Ele tentou voltar pelo mesmo caminho. As pegadas dele sumiram.","personagens":[sent("cac","assustado",0.5)]},
 {"cenario":"mata_noite","galho":True,"duracao":6,"zoom":[1,1.1],"narracao":"Ouviu um assobio. De cima de uma árvore, uma criança de cabelo vermelho como fogo sorriu.","personagens":[sent("cac","assustado",0.2,0.8),sent("cur","sorrindo",0.58,0.55,y=-520,entra=1.5,semEntrada=False)]},
 {"cenario":"mata_noite","galho":True,"duracao":5,"zoom":[1.1,1.3],"falas":[{"quem":"cur","texto":"Você seguiu o meu caminho. Agora o seu é o meu."}],"personagens":[sent("cur","sorrindo",0.58,0.55,y=-520)]},
 {"cenario":"pegadas_close","duas":True,"duracao":6,"zoom":[1,1.12],"respiro":1.0,"narracao":"Nunca mais encontraram o caçador. As pegadas, sim. Dava para ver que continuavam. Só que agora eram duas."}])
save('c10_curupira.json',c10)
save('c10_sons.json',{"versao":1,"episodio":"c10","nota":"Curupira: mata ao entardecer (passaros, grilos, vento); assobio na cena 6; drone no final.","cues":[
 {"cena":1,"offset":0,"tipo":"passaros","ateCena":3,"params":{"vol":0.7}},
 {"cena":1,"offset":0,"tipo":"grilos","ateCena":8,"params":{"vol":3,"n":5}},
 {"cena":1,"offset":0,"tipo":"vento","ateCena":8,"params":{"vol":0.25}},
 {"cena":6,"offset":0.4,"tipo":"assobio","params":{"vol":1.0}},
 {"cena":7,"offset":0,"tipo":"drone","ateCena":8,"params":{"tomInicial":40,"subida":2,"vol":0.3}}]})
# ---------- c11 Criança pede carona (vermelho/chuva) ----------
c11=base(numero=11,nome="Criança pede carona",cartela={"titulo":"Criança pede carona","sub":"Original · não pare"},cor="#E03A3A",arquivo="11_crianca_pede_carona.mp4",destaque=["menino","cemitério","vez","vazio"],sons="c11_sons.json",
 vozes={"narrador":["pt-BR-AntonioNeural","-6%","-14Hz"],"men":["pt-BR-ThalitaMultilingualNeural","+0%","+30Hz"],"men2":["pt-BR-ThalitaMultilingualNeural","-15%","+10Hz"]},
 elenco={"men":{"camisa":"#C8D0E0","calca":"#3A4A6A","cabelo":"#2A1E14","pele":"#D8B08C","estilo":"curto"}},
 cenas=[
 {"cenario":"volante_pov","duracao":3.5,"zoom":[1,1.06],"narracao":"Eu dirigia pela BR às três da manhã."},
 {"cenario":"estrada_chuva","duracao":8,"zoom":[1,1.08],"narracao":"Na curva, sob a chuva, vi um menino de uns oito anos, de camiseta molhada, acenando. Parei, claro. Quem não pararia?","personagens":[sent("men","acenando",0.72,0.6,entra=0.5,semEntrada=False)]},
 {"cenario":"volante_pov","retro":True,"menino":True,"duracao":5,"zoom":[1,1.06],"narracao":"Ele entrou no banco de trás.","falas":[{"quem":"men","texto":"Pode me levar para casa? É logo ali."}]},
 {"cenario":"volante_pov","retro":True,"menino":True,"duracao":5,"zoom":[1,1.06],"narracao":"Dirigi. Ele me guiava calado: Aqui. Mais um pouco."},
 {"cenario":"portao_cemiterio","duracao":6,"zoom":[1,1.1],"narracao":"Cheguei em frente a um portão de ferro. Enorme. Enferrujado. Era o cemitério."},
 {"cenario":"volante_pov","retro":True,"vazio":True,"duracao":5,"zoom":[1,1.1],"narracao":"Olhei pelo retrovisor. O banco de trás estava vazio, molhado."},
 {"cenario":"volante_pov","passageiro":True,"duracao":6,"zoom":[1,1.06],"narracao":"Uma voz baixa, ao meu lado, disse:","falas":[{"quem":"men2","texto":"Obrigado, moço. Agora é a sua vez."}]},
 {"cenario":"portao_cemiterio","manha":True,"duracao":7,"zoom":[1,1.08],"respiro":1.8,"narracao":"O motor morreu. De manhã, acharam meu carro em frente ao portão. Faróis acesos. Porta aberta. Vazio."}])
save('c11_carona.json',c11)
save('c11_sons.json',{"versao":1,"episodio":"c11","nota":"Carona: chuva forte, motor e limpador; na cena 8 o motor morre (corte) e fica so o vento da manha.","cues":[
 {"cena":1,"offset":0,"tipo":"chuva","ateCena":7,"params":{"vol":0.55}},
 {"cena":1,"offset":0,"tipo":"elevadorZumbido","ateCena":7,"params":{"vol":0.3}},
 {"cena":1,"offset":0,"tipo":"limpador","ateCena":7,"params":{"vol":0.8}},
 {"cena":8,"offset":0.2,"tipo":"vento","ateCena":8,"params":{"vol":0.3}}]})
# ---------- c12 Cuca (prata-azulada) ----------
tp=[("+8Hz","-10%"),("+6Hz","-10%"),("+4Hz","-10%"),("-4Hz","-12%"),("-10Hz","-12%"),("-14Hz","-14%"),("-18Hz","-16%"),("-10Hz","-12%")]
tx12=["A avó sempre cantava para o Pedro dormir: Nana, neném, que a Cuca vem pegar.",
"Uma noite, quando ele já estava quase dormindo, a canção veio da rua. Da janela. Uma voz de mulher, doce, a mesma melodia.",
"Ele sorriu, achando que era a avó. Mas a avó roncava no quarto ao lado.",
"A voz foi ficando mais perto. Mais perto.",
"Pedro lembrou do que a avó dizia: Se a Cuca cantar, finja que dorme. Ela só leva quem está acordado.",
"Ele fechou os olhos com força. Ouviu a janela se abrindo. O ranger lento. Um cheiro de lama.",
"A canção parou bem em cima do rosto dele. Alguns segundos. Muitos.",
"De manhã, a avó viu a janela aberta e o lençol dele cheio de marcas de escamas. Pedro dormia, sozinho, fingindo que dormia."]
cn=[{"cenario":"quarto_lua","olhos":"abertos","personagens":[sent("avo","neutro",0.82,0.9)]},
 {"cenario":"quarto_lua","olhos":"fechados"},{"cenario":"quarto_lua","olhos":"abertos"},
 {"cenario":"quarto_lua","olhos":"abertos","vulto":0.5},{"cenario":"quarto_lua","olhos":"abertos","vulto":0.7},
 {"cenario":"quarto_lua","olhos":"fechados","vulto":0.85,"jan":0.7},{"cenario":"quarto_lua","olhos":"fechados","vulto":1,"jan":1,"respiro":1.5},
 {"cenario":"quarto_lua","olhos":"fechados","manha":True,"jan":1,"escamas":True,"respiro":1.5,"personagens":[sent("avo","assustado",0.82,0.9)]}]
for i,c in enumerate(cn):
    c["duracao"]=4; c["zoom"]=[1,1.08+0.02*i]; c["rateNarrador"]=tp[i][1]; c["pitchNarrador"]=tp[i][0]; c["narracao"]=tx12[i]
cn[1]["falas"]=[{"quem":"cuca","texto":"Nana, neném..."}]
c12=base(numero=12,nome="Cuca",cartela={"titulo":"Cuca","sub":"Folclore brasileiro"},cor="#9FB4D8",arquivo="12_cuca.mp4",destaque=["cuca","dorme","finja"],sons="c12_sons.json",
 vozes={"narrador":["pt-BR-FranciscaNeural","-10%","+8Hz"],"cuca":["pt-BR-FranciscaNeural","-32%","+10Hz"]},
 elenco={"avo":{"camisa":"#8A6A9A","blusa":"#D8D2C4","calca":"#4A3A4A","cabelo":"#BDBBB4","pele":"#B98560","estilo":"coque"}},cenas=cn)
save('c12_cuca.json',c12)
save('c12_sons.json',{"versao":1,"episodio":"c12","nota":"Cuca: caixinha de ninar (doce) nas cenas 1 a 3, drone que desce nas cenas 4 a 7, rangido da janela na 6, silencio na 7, passaros de manha.","cues":[
 {"cena":1,"offset":0,"tipo":"caixinha","ateCena":3,"params":{"lenta":True,"vol":0.5}},
 {"cena":4,"offset":0,"tipo":"drone","ateCena":7,"params":{"tomInicial":44,"subida":-4,"vol":0.32}},
 {"cena":6,"offset":1.2,"tipo":"rangido","params":{"dur":2.6,"vol":0.9}},
 {"cena":7,"offset":0.5,"tipo":"silencio","params":{"dur":3.5}},
 {"cena":8,"offset":0,"tipo":"passaros","ateCena":8,"params":{"vol":0.6}}]})
idx=json.load(open(D+'indice.json',encoding='utf-8'))
idx.update({"c09":"c09_enfermeiro.json","c10":"c10_curupira.json","c11":"c11_carona.json","c12":"c12_cuca.json"})
json.dump(idx,open(D+'indice.json','w',encoding='utf-8'),indent=2,ensure_ascii=False)
