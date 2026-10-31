import json
D='C:/Users/willi/Downloads/Projetos/Conteudo_Bit/Producao/serie/ep/'
def save(n,d): json.dump(d,open(D+n,'w',encoding='utf-8'),indent=2,ensure_ascii=False)
base=lambda **k: dict({"proxima":False,"legenda":"palavras","legendaY":1380,"legendaTam":125,"escurece":0.06,"saida":"contos-dia6","camadas":{"voz":1,"trilha":1,"efeitos":1,"musicaWav":0},"respiros":{"lead":0.12,"gap":0.2,"tail":0.4},"duck":0.35},**k)
sent=lambda i,pose,x,e=0.9,**k: dict({"id":i,"pose":pose,"x":x,"escala":e,"semEntrada":True,"fica":True},**k)
# ---------- c21 O Barril de Amontillado ----------
ERIC="cjVigY5qzO86Huf0OWal"
t21=["Montresor jurou vingança contra Fortunato, que o ofendera mil vezes. Mas nunca deixou que ele percebesse.",
"No Carnaval, encontrou Fortunato bêbado e fantasiado de bobo da corte.",
"Comprei um barril de Amontillado. Mas não tenho certeza. Vou pedir a Luchesi que prove.",
None,
"Desceram pelas catacumbas úmidas, onde repousavam os ossos da família de Montresor. Fortunato tossia. Continuava rindo.",
"No fundo, numa pequena cripta, Montresor o acorrentou à parede.",
"Começou a levantar tijolos, um por um.",
"Fortunato riu, e depois implorou. Montresor não respondeu. Só os guizos tilintaram.",
"Meio século depois, ninguém tocou naquela parede. In pace requiescat."]
gor=lambda x,e=0.9: {"tipo":"gorro_guizos","x":x,"escala":e,"entra":0}
cen21=[
 {"cenario":"carnaval_noite","duracao":6,"zoom":[1,1.06],"personagens":[sent("mon","sorrindo",0.35)]},
 {"cenario":"carnaval_noite","duracao":5,"zoom":[1,1.06],"personagens":[sent("mon","sorrindo",0.25),sent("fort","neutro",0.68)],"objetos":[gor(0.68)]},
 {"cenario":"carnaval_noite","duracao":5,"zoom":[1,1.08],"personagens":[sent("mon","sorrindo",0.25),sent("fort","neutro",0.68)],"objetos":[gor(0.68)]},
 {"cenario":"carnaval_noite","duracao":4,"zoom":[1,1.08],"falas":[{"quem":"fort","texto":"Luchesi? Ele não distingue um Amontillado de um xerez. Vamos!"}],"personagens":[sent("mon","sorrindo",0.25),sent("fort","apontando",0.68)],"objetos":[gor(0.68)]},
 {"cenario":"catacumbas","duracao":7,"zoom":[1,1.06],"personagens":[sent("mon","neutro",0.3),sent("fort","neutro",0.66)],"objetos":[gor(0.66)]},
 {"cenario":"nicho_parede","corrente":True,"duracao":4,"zoom":[1,1.06],"personagens":[sent("mon","sorrindo",0.15),sent("fort","neutro",0.5)],"objetos":[gor(0.5)]},
 {"cenario":"nicho_parede","corrente":True,"duracao":4,"zoom":[1,1.06],"personagens":[sent("fort","neutro",0.5)],"objetos":[gor(0.5),{"tipo":"tijolos_nicho","max":0.5,"dur":3,"entra":0.2}]},
 {"cenario":"nicho_parede","corrente":True,"duracao":6,"zoom":[1,1.1],"personagens":[sent("fort","medo",0.5)],"objetos":[gor(0.5),{"tipo":"tijolos_nicho","max":0.92,"dur":5,"entra":0.2}]},
 {"cenario":"nicho_parede","corrente":True,"duracao":5,"zoom":[1,1.1],"respiro":1.5,"objetos":[{"tipo":"tijolos_nicho","max":1,"dur":0.1,"entra":0}]}]
for i,c in enumerate(cen21):
    if t21[i]: c["falas"]=[{"quem":"mon","arquivo":f"m{i+1}.wav","texto":t21[i]}]+c.get("falas",[])
c21=base(numero=21,nome="O Barril de Amontillado",cartela={"titulo":"Barril de Amontillado","sub":"Edgar Allan Poe · 1846"},cor="#2A8CA8",arquivo="21_barril_de_amontillado.mp4",destaque=["vingança","amontillado","tijolos","pace"],sons="c21_sons.json",
 vozes={"fort":["pt-BR-AntonioNeural","+14%","+10Hz"]},respiros={"lead":0.2,"gap":0.3,"tail":0.5},duck=0.4,
 eleven={f"m{i+1}.wav":{"voz":ERIC,"texto":"[smiling] "+t21[i],"pico":0.6} for i in range(9) if t21[i]},
 elenco={"mon":{"camisa":"#0A0A12","calca":"#0A0A12","cabelo":"#0A0A12","pele":"#D8B08C","estilo":"curto","capuz":True},"fort":{"camisa":"#C84A4A","listras":True,"calca":"#2A6AA8","cabelo":"#6A3A1A","pele":"#E0A888","estilo":"curto","bigode":True}},cenas=cen21)
save('c21_amontillado.json',c21)
save('c21_sons.json',{"versao":1,"episodio":"c21","nota":"Amontillado: guizos de bobo ao fundo (leves no carnaval, agitados no nicho), drone grave, silencio so com guizos no final.","cues":[
 {"cena":1,"offset":0,"tipo":"drone","ateCena":8,"params":{"tomInicial":38,"subida":1,"vol":0.22}},
 {"cena":2,"offset":0,"tipo":"guizos","ateCena":5,"params":{"intervalo":0.7,"vol":0.4}},
 {"cena":6,"offset":0,"tipo":"guizos","ateCena":8,"params":{"intervalo":0.4,"vol":0.5}},
 {"cena":9,"offset":0,"tipo":"guizos","params":{"dur":3,"intervalo":1.2,"vol":0.4}}]})
# ---------- c22 Corpo-seco ----------
t22=["Seu Antônio foi o homem mais cruel da cidade. Maltratava a mãe, os vizinhos, os bichos. Morreu numa terça. Enterraram na quarta.",
"Na quinta, o coveiro viu o chão aberto. O caixão estava vazio.",
"Cavaram de novo. No dia seguinte, a mesma cova aberta. Terra expulsa para fora. Cada noite, o mesmo.",
"A velha benzedeira explicou:",
"Na outra semana, dois meninos viram um homem seco, de pele colada nos ossos, parado no cruzamento, olhando para as casas.",
"Os olhos dele reluziam.",
"Ele procurava alguém."]
cen22=[
 {"cenario":"cemiterio_noite","dia":True,"caixao":True,"duracao":9},
 {"cenario":"cemiterio_noite","cova":True,"duracao":5,"personagens":[sent("cov","olhando",0.82,0.9)]},
 {"cenario":"cemiterio_noite","cova":True,"sopro":True,"duracao":8,"personagens":[sent("cov","cansada",0.15,0.9)]},
 {"cenario":"sala_benzedeira","duracao":9,"personagens":[sent("ben","seria",0.55,0.95)],"falas":[{"quem":"ben","texto":"A terra não aguenta o corpo dele. Nem para apodrecer ele serve. Vira corpo-seco. Anda à noite, sem comer nem descansar, odiando todo mundo."}]},
 {"cenario":"cruzamento_noite","corpo":0.45,"olhos":0,"duracao":8,"personagens":[sent("me1","assustado",0.18,0.6),sent("me2","assustado",0.34,0.55)]},
 {"cenario":"cruzamento_noite","corpo":0.85,"olhos":1,"duracao":3,"zoom":[1.1,1.3]},
 {"cenario":"cruzamento_noite","corpo":1,"olhos":1,"duracao":3,"zoom":[1.2,1.5],"respiro":1.5}]
for i,c in enumerate(cen22):
    c["zoom"]=c.get("zoom",[1,1.07])
    if t22[i] and c.get("falas") is None: c["narracao"]=t22[i]
    elif t22[i]: c["narracao"]=t22[i]
c22=base(numero=22,nome="Corpo-seco",cartela={"titulo":"Corpo-seco","sub":"Folclore brasileiro"},cor="#B8C8A8",arquivo="22_corpo_seco.mp4",destaque=["corpo-seco","terra","olhos","cova"],sons="c22_sons.json",
 vozes={"narrador":["pt-BR-AntonioNeural","-10%","-10Hz"],"ben":["pt-BR-FranciscaNeural","-22%","-22Hz"]},
 elenco={"cov":{"camisa":"#5A4A3A","calca":"#2A2418","cabelo":"#4A4A4A","pele":"#B98560","estilo":"careca","bigode":True},"ben":{"camisa":"#5A5A8A","blusa":"#D8D2C4","calca":"#3A3A4A","cabelo":"#BDBBB4","pele":"#B98560","estilo":"coque"},"me1":{"camisa":"#8A6A3A","calca":"#3A3A4A","cabelo":"#1B1412","pele":"#C99A74","estilo":"curto"},"me2":{"camisa":"#4A6A8A","calca":"#3A3A4A","cabelo":"#2A1E10","pele":"#B98560","estilo":"curto"}},cenas=cen22)
save('c22_corpo_seco.json',c22)
save('c22_sons.json',{"versao":1,"episodio":"c22","nota":"Corpo-seco: vento e terra, drone grave; grilos no cemiterio; silencio no final.","cues":[
 {"cena":1,"offset":0,"tipo":"vento","ateCena":7,"params":{"vol":0.35}},
 {"cena":1,"offset":0,"tipo":"drone","ateCena":7,"params":{"tomInicial":36,"subida":2,"vol":0.26}},
 {"cena":2,"offset":0,"tipo":"grilos","ateCena":3,"params":{"vol":2,"n":3}},
 {"cena":7,"offset":0.5,"tipo":"corte","params":{}}]})
# ---------- c23 Babá eletrônica ----------
LIL="pFZP5JQG7iQjIQuC4Bku"
mae={"camisa":"#C8A0B8","calca":"#3A4A6A","cabelo":"#4A2E1E","pele":"#E0BC9C","estilo":"longo"}
t23=["Meu filho tem um ano e dorme no quarto do fim do corredor.",
"Estava na cozinha quando a babá eletrônica fez um chiado. E uma voz baixa disse:",
"Meu filho riu. Ele nunca ri dormindo.",
"Larguei tudo e corri.",
"Abri a porta: o berço, a janela fechada, nada. Meu filho acordado, olhando para o canto do teto, sorrindo.",
"Ele me olhou e disse, mal falando:",
"Peguei meu filho no colo. Voltei para a cozinha com as pernas bambas.",
"A babá eletrônica estava sobre o balcão. Tinha a tomada puxada e as pilhas na gaveta, há semanas.",
"Desligada."]
cen23=[
 {"cenario":"quarto_bebe"},
 {"cenario":"cozinha_menta","chiado":True,"falas":[{"quem":"baba","arquivo":"baba.wav","texto":"Shh. Já passou. Ela já foi embora."}]},
 {"cenario":"quarto_bebe","acordado":True,"sorri":True},
 {"cenario":"corredor_menta","personagens":[sent("mae","correndo",0.5,0.6)]},
 {"cenario":"quarto_bebe","acordado":True,"sorri":True,"canto":True},
 {"cenario":"quarto_bebe","acordado":True,"sorri":True,"canto":True,"falas":[{"quem":"bebe","texto":"Mamãe. Ela disse que você ia demorar."}]},
 {"cenario":"cozinha_menta","personagens":[sent("mae","assustado",0.3,0.9)]},
 {"cenario":"cozinha_menta","perto":True,"duracao":9},
 {"cenario":"cozinha_menta","perto":True,"desligada":True,"respiro":2.0}]
rt=[("+6%","+0Hz"),("+10%","+2Hz"),("+14%","+4Hz"),("+22%","+6Hz"),("+24%","+8Hz"),("+26%","+10Hz"),("+28%","+12Hz"),("+22%","+8Hz"),("-6%","-4Hz")]
for i,c in enumerate(cen23):
    c.setdefault("duracao",4); c["zoom"]=[1,1.08]; c["narracao"]=t23[i]; c["rateNarrador"]=rt[i][0]; c["pitchNarrador"]=rt[i][1]
c23=base(numero=23,nome="Babá eletrônica",cartela={"titulo":"Babá eletrônica","sub":"Original · não entre"},cor="#7FE8C0",arquivo="23_baba_eletronica.mp4",destaque=["babá","chiado","filho","desligada"],sons="c23_sons.json",
 vozes={"narrador":["pt-BR-FranciscaNeural","+10%","+0Hz"],"bebe":["pt-BR-ThalitaMultilingualNeural","+8%","+45Hz"]},
 eleven={"baba.wav":{"voz":LIL,"texto":"[whispers] Shh. Já passou. Ela já foi embora.","pico":0.7}},elenco={"mae":mae},cenas=cen23)
save('c23_baba.json',c23)
save('c23_sons.json',{"versao":1,"episodio":"c23","nota":"Baba: chiado, batimento acelerando, respiracao ofegante; corte seco e silencio no final.","cues":[
 {"cena":2,"offset":0.3,"tipo":"chiado","params":{"dur":3,"vol":0.5}},
 {"cena":2,"offset":0,"tipo":"batimento","ateCena":3,"params":{"bpm":72,"vol":0.3}},
 {"cena":4,"offset":0,"tipo":"batimento","ateCena":7,"params":{"bpm":110,"vol":0.45}},
 {"cena":4,"offset":0,"tipo":"respirar","ateCena":7,"params":{"ritmo":1.3,"vol":0.5}},
 {"cena":8,"offset":0,"tipo":"zumbidoLuz","ateCena":8,"params":{"vol":0.06}},
 {"cena":9,"offset":0,"tipo":"corte","params":{}}]})
# ---------- c24 Mapinguari ----------
t24=["O seringueiro andava sozinho pela mata quando sentiu o cheiro: podre, pesado, de carne de dias.",
"Lembrou do que os mais velhos diziam do Mapinguari: um bicho enorme, de pelo vermelho, um olho só no meio da testa. E uma boca aberta na barriga.",
"Os velhos avisavam:",
"Ele deu meia-volta, contra o vento. Ouviu os galhos estalarem. Um rugido que sacudiu a copa das árvores.",
"Correu até as pernas queimarem.",
"Chegou ao rio, entrou numa canoa, remou sem olhar para trás.",
"Só na margem seguinte, ofegante, olhou.",
"Entre as árvores, uma sombra imensa, com o olho brilhando.",
"E, no meio do corpo, uma boca sorrindo."]
ser={"camisa":"#8A6A3A","calca":"#4A4A3A","cabelo":"#2A1A10","pele":"#B98560","estilo":"curto","mochila":"#4A3A22"}
cen24=[
 {"cenario":"selva_vento","cheiro":True,"personagens":[sent("ser","procurando",0.3)]},
 {"cenario":"selva_vento","bicho":0.35,"bichoX":720,"bichoEsc":0.8,"personagens":[sent("ser","olhando",0.25)]},
 {"cenario":"selva_vento","ventoK":True,"falas":[{"quem":"velho","texto":"Ande contra o vento. O bicho caça pelo cheiro, não pela vista."}]},
 {"cenario":"selva_vento","ventoK":True,"bicho":0.4,"bichoX":900,"personagens":[sent("ser","correndo",0.4,0.9,flip=True)]},
 {"cenario":"selva_vento","ventoK":True,"personagens":[sent("ser","correndo",0.55,0.9,flip=True)]},
 {"cenario":"rio_noite","canoa":True,"personagens":[sent("ser","cansada",0.69,0.7,y=140)]},
 {"cenario":"rio_noite","canoa":True,"personagens":[sent("ser","olhando",0.69,0.7,y=140)]},
 {"cenario":"rio_noite","canoa":True,"bicho":0.8,"bichoX":220,"personagens":[sent("ser","olhando",0.69,0.7,y=140)]},
 {"cenario":"rio_noite","canoa":True,"bicho":1,"boca":True,"bichoX":220,"respiro":1.5,"zoom":[1.1,1.3],"personagens":[sent("ser","medo",0.69,0.7,y=140)]}]
rt4=["+14%","+14%","-6%","+22%","+26%","+16%","+10%","+8%","-4%"]
for i,c in enumerate(cen24):
    c.setdefault("duracao",4); c.setdefault("zoom",[1,1.08]); c["narracao"]=t24[i]; c["rateNarrador"]=rt4[i]
c24=base(numero=24,nome="Mapinguari",cartela={"titulo":"Mapinguari","sub":"Folclore brasileiro"},cor="#7BD04A",arquivo="24_mapinguari.mp4",destaque=["mapinguari","cheiro","vento","olho"],sons="c24_sons.json",
 vozes={"narrador":["pt-BR-AntonioNeural","+14%","+0Hz"],"velho":["pt-BR-AntonioNeural","-16%","-18Hz"]},elenco={"ser":ser},cenas=cen24)
save('c24_mapinguari.json',c24)
save('c24_sons.json',{"versao":1,"episodio":"c24","nota":"Mapinguari: vento forte, passos correndo, respiracao ofegante, rugido, remos e grilos no rio; silencio na ultima frase.","cues":[
 {"cena":1,"offset":0,"tipo":"vento","ateCena":5,"params":{"vol":0.4}},
 {"cena":1,"offset":0,"tipo":"grilos","ateCena":5,"params":{"vol":2,"n":4}},
 {"cena":4,"offset":4.5,"tipo":"rugido","params":{"dur":2.4,"vol":0.5}},
 {"cena":5,"offset":0,"tipo":"passosChinelo","params":{"n":8,"passo":0.3,"vol":0.8}},
 {"cena":4,"offset":0,"tipo":"respirar","ateCena":7,"params":{"ritmo":1.1,"vol":0.5}},
 {"cena":6,"offset":0,"tipo":"remo","ateCena":7,"params":{"ritmo":1.0,"vol":0.5}},
 {"cena":6,"offset":0,"tipo":"grilos","ateCena":8,"params":{"vol":2,"n":4}},
 {"cena":9,"offset":0,"tipo":"corte","params":{}}]})
idx=json.load(open(D+'indice.json',encoding='utf-8'))
idx.update({"c21":"c21_amontillado.json","c22":"c22_corpo_seco.json","c23":"c23_baba.json","c24":"c24_mapinguari.json"})
json.dump(idx,open(D+'indice.json','w',encoding='utf-8'),indent=2,ensure_ascii=False)
