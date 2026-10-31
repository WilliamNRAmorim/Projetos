import json
D='C:/Users/willi/Downloads/Projetos/Conteudo_Bit/Producao/serie/ep/'
def save(n,d): json.dump(d,open(D+n,'w',encoding='utf-8'),indent=2,ensure_ascii=False)
base=lambda **k: dict({"proxima":False,"legenda":"palavras","legendaY":1380,"legendaTam":125,"escurece":0.06,"saida":"contos-dia5","camadas":{"voz":1,"trilha":1,"efeitos":1,"musicaWav":0},"respiros":{"lead":0.12,"gap":0.2,"tail":0.4},"duck":0.35},**k)
sent=lambda i,pose,x,e=0.9,**k: dict({"id":i,"pose":pose,"x":x,"escala":e,"semEntrada":True,"fica":True},**k)
# ---------- c17 O Retrato Oval ----------
MAT="XrExE9yKIg1WjnnlVkGX"
t17=["Um viajante ferido se abrigou num castelo abandonado. No quarto, entre dezenas de quadros, encontrou um retrato oval de uma jovem.",
"Tão vivo que ele se assustou, fechou os olhos, abriu de novo, e continuou igual.",
"Num livrinho ao lado, achou a história.",
"A jovem era esposa de um pintor que a amava, mas amava mais a arte. Quando ele decidiu retratá-la, ela, por amor, posou durante semanas numa torre escura.",
"O pintor trabalhava, obcecado. Não via que a cor das bochechas dela sumia. Ela sorria, fraca, sem reclamar.",
"Cada pincelada no retrato dava mais vida à tinta. E tirava da moça.",
"No último dia, ele deu o toque final e gritou:",
"Virou-se para a esposa. Ela estava morta."]
cen17=[
 {"cenario":"quarto_castelo","duracao":6,"zoom":[1,1.06],"personagens":[sent("via","cansada",0.2,0.9)]},
 {"cenario":"retrato_oval","vida":1,"duracao":5,"zoom":[1,1.08]},
 {"cenario":"quarto_castelo","livro":True,"duracao":3,"zoom":[1,1.08],"personagens":[sent("via","lendo",0.2,0.9)]},
 {"cenario":"torre_pintor","tela":0,"duracao":8,"zoom":[1,1.06],"personagens":[sent("esp1","sentada",0.25,0.85),sent("pin","neutro",0.58,0.9)]},
 {"cenario":"torre_pintor","tela":0.5,"duracao":7,"zoom":[1,1.06],"personagens":[sent("esp2","sentada",0.25,0.85),sent("pin","dandoCorda",0.58,0.9)]},
 {"cenario":"retrato_oval","vidaDe":0.4,"vidaPara":1,"vidaT":4,"duracao":5,"zoom":[1,1.08]},
 {"cenario":"torre_pintor","tela":1,"duracao":5,"zoom":[1,1.06],"personagens":[sent("esp3","sentadaSeria",0.25,0.85),sent("pin","apontandoCima",0.58,0.9)]},
 {"cenario":"torre_pintor","tela":1,"duracao":4,"zoom":[1,1.1],"respiro":1.5,"personagens":[sent("esp3","cansada",0.25,0.85),sent("pin","assustado",0.58,0.9)]}]
for i,c in enumerate(cen17): c["falas"]=[{"quem":"nar","arquivo":f"r{i+1}.wav","texto":t17[i]}]
cen17[6]["falas"].append({"quem":"pintor","texto":"Isto é de fato a própria Vida!"})
c17=base(numero=17,nome="O Retrato Oval",cartela={"titulo":"O Retrato Oval","sub":"Edgar Allan Poe · 1842"},cor="#2E8B6A",arquivo="17_o_retrato_oval.mp4",destaque=["retrato","pintor","vida","morta"],sons="c17_sons.json",
 vozes={"pintor":["pt-BR-AntonioNeural","+8%","+8Hz"]},respiros={"lead":0.2,"gap":0.3,"tail":0.5},duck=0.4,
 eleven={f"r{i+1}.wav":{"voz":MAT,"texto":"[sorrowful] "+t17[i],"pico":0.6} for i in range(8)},
 elenco={"via":{"camisa":"#4A5A6A","calca":"#2A2A34","cabelo":"#2A1E10","pele":"#D8B08C","estilo":"curto"},"pin":{"camisa":"#6A2A2A","blusa":"#E8E2D4","calca":"#2A1A14","cabelo":"#2A1A10","pele":"#D8B08C","estilo":"curto","bigode":True},
  "esp1":{"camisa":"#5A8A7A","calca":"#5A8A7A","cabelo":"#3A1E14","pele":"#E8B8A0","estilo":"longo"},"esp2":{"camisa":"#5A8A7A","calca":"#5A8A7A","cabelo":"#3A1E14","pele":"#D0B8B0","estilo":"longo"},"esp3":{"camisa":"#7A9A92","calca":"#7A9A92","cabelo":"#3A1E14","pele":"#B8B8B8","estilo":"longo"}},cenas=cen17)
save('c17_retrato_oval.json',c17)
save('c17_sons.json',{"versao":1,"episodio":"c17","nota":"Retrato Oval: piano muito baixo, cordas (acorde) nas ultimas cenas, drone; silencio na ultima fala.","cues":[
 {"cena":1,"offset":0,"tipo":"pianoBia","params":{"notas":["A3","E4","C4","B3","E4","A3","D4","C4","E3","A3","G3","C4","A3","E4"],"passo":2.4,"vol":0.45}},
 {"cena":1,"offset":0,"tipo":"drone","ateCena":8,"params":{"tomInicial":38,"subida":1,"vol":0.2}},
 {"cena":6,"offset":0,"tipo":"acordeBia","params":{"vol":0.5}},
 {"cena":8,"offset":0,"tipo":"corte","params":{}}]})
# ---------- c18 Lobisomem ----------
t18_8=[("amigo","Você me viu?"),("eu","Vi."),("amigo","Então agora você também precisa saber: a corrente só segura quem quer ser segurado.")]
c18=base(numero=18,nome="Lobisomem",cartela={"titulo":"Lobisomem","sub":"Folclore brasileiro"},cor="#E8D56A",arquivo="18_lobisomem.mp4",destaque=["lua","corrente","uivo","sexta"],sons="c18_sons.json",
 vozes={"narrador":["pt-BR-AntonioNeural","-4%","-4Hz"],"amigo":["pt-BR-AntonioNeural","-14%","-12Hz"],"eu":["pt-BR-AntonioNeural","-4%","-4Hz"]},
 elenco={"eu":{"camisa":"#6A7A4A","calca":"#3A3A2A","cabelo":"#2A1E10","pele":"#C99A74","estilo":"curto"},"amigo":{"camisa":"#8A7A6A","calca":"#3A3A3A","cabelo":"#4A3A2A","pele":"#D0C0B8","estilo":"curto"}},
 cenas=[
 {"cenario":"campo_manha","duracao":6,"zoom":[1,1.06],"narracao":"Meu melhor amigo era o sétimo filho homem da família. Na roça, isso significava uma coisa.","personagens":[sent("eu","neutro",0.3),sent("amigo","neutro",0.65)]},
 {"cenario":"celeiro_lua","porta":"fechada","duracao":4,"zoom":[1,1.08],"narracao":"Toda sexta de lua cheia ele sumia. Nunca disse onde.","personagens":[sent("amigo","neutro",0.72,0.55)]},
 {"cenario":"celeiro_dentro","corrente":{"x":0.5},"duracao":8,"zoom":[1,1.06],"narracao":"Um dia segui. Ele entrou no celeiro, trancou a porta por dentro e prendeu os próprios pulsos numa corrente grossa.","personagens":[sent("amigo","medo",0.5,0.9)]},
 {"cenario":"celeiro_lua","porta":"fechada","duracao":5,"zoom":[1,1.08],"narracao":"Eu entendi. E não fugi. Fiquei do lado de fora, ouvindo.","personagens":[sent("eu","olhando",0.82,0.9)]},
 {"cenario":"celeiro_dentro","corrente":{"x":0.5},"tenso":True,"lobo":1,"duracao":9,"zoom":[1,1.08],"narracao":"Ouvi o grito. Os ossos. A corrente se esticando. E o uivo que gelou o mato todo."},
 {"cenario":"celeiro_dentro","corrente":{"x":0.5},"tenso":True,"lobo":0.35,"duracao":3,"zoom":[1,1.1],"respiro":0.5,"narracao":"Mas a corrente aguentou."},
 {"cenario":"campo_manha","duracao":6,"zoom":[1,1.06],"narracao":"De manhã, ele saiu pálido, exausto, com os pulsos em carne viva.","personagens":[sent("eu","neutro",0.3),sent("amigo","cansada",0.65)]},
 {"cenario":"campo_manha","duracao":10,"zoom":[1.05,1.2],"falas":[{"quem":"amigo","texto":"Você me viu?"},{"quem":"eu","texto":"Vi."},{"quem":"amigo","texto":"Então agora você também precisa saber: a corrente só segura quem quer ser segurado."}],"personagens":[sent("eu","neutro",0.3),sent("amigo","cansada",0.65)]},
 {"cenario":"celeiro_lua","porta":"fechada","duracao":3.5,"zoom":[1,1.08],"respiro":1.2,"narracao":"Nunca mais faltei a uma sexta.","personagens":[sent("eu","neutro",0.8,0.7)]}])
save('c18_lobisomem.json',c18)
save('c18_sons.json',{"versao":1,"episodio":"c18","nota":"Lobisomem: causo firme; grilos, corrente, uivo distante, passaros de manha.","cues":[
 {"cena":2,"offset":0,"tipo":"grilos","ateCena":6,"params":{"vol":2.2,"n":4}},
 {"cena":2,"offset":0,"tipo":"vento","ateCena":6,"params":{"vol":0.15}},
 {"cena":3,"offset":2.0,"tipo":"corrente","params":{"dur":5,"vol":0.5}},
 {"cena":5,"offset":0,"tipo":"corrente","ateCena":6,"params":{"tenso":True,"vol":0.4}},
 {"cena":5,"offset":5.0,"tipo":"uivoLobo","params":{"dur":4,"vol":0.5}},
 {"cena":7,"offset":0,"tipo":"passaros","ateCena":8,"params":{"vol":0.6}}]})
# ---------- c19 Ônibus noturno ----------
c19=base(numero=19,nome="Ônibus noturno",cartela={"titulo":"Ônibus noturno","sub":"Original · desça"},cor="#D8E84A",arquivo="19_onibus_noturno.mp4",destaque=["todos","fora","serviço","desça"],sons="c19_sons.json",
 vozes={"narrador":["pt-BR-FranciscaNeural","+24%","+2Hz"]},respiros={"lead":0.08,"gap":0.12,"tail":0.2},
 elenco={"ele":{"camisa":"#6A5A8A","calca":"#2A2A3A","cabelo":"#1B1412","pele":"#D8B08C","estilo":"curto","mochila":"#2E3440"}},
 cenas=[
 {"cenario":"onibus_interior","duracao":5,"zoom":[1,1.06],"narracao":"Peguei o último ônibus, quase vazio. Cinco ou seis passageiros, cada um no seu canto."},
 {"cenario":"onibus_interior","olham":True,"duracao":4,"zoom":[1,1.08],"narracao":"De repente, todos viraram a cabeça para mim. Ao mesmo tempo. Em silêncio."},
 {"cenario":"onibus_interior","olham":True,"duracao":3,"zoom":[1.15,1.4],"narracao":"Ninguém falou. Ninguém sorriu. Só olharam."},
 {"cenario":"ponto_lima","duracao":4,"zoom":[1,1.08],"narracao":"Apertei o botão e desci no ponto seguinte, com o coração na garganta.","personagens":[sent("ele","assustado",0.35,0.9)]},
 {"cenario":"onibus_traseira","dist":0.3,"duracao":5,"zoom":[1,1.08],"narracao":"O ônibus continuou. Pela janela traseira, os rostos pálidos ainda me olhavam, imóveis."},
 {"cenario":"onibus_traseira","letreiro":True,"dist":0,"duracao":4,"zoom":[1,1.1],"narracao":"Foi quando eu vi o letreiro acima do vidro: Fora de serviço."},
 {"cenario":"ponto_lima","duracao":7,"zoom":[1,1.08],"narracao":"Não existe último ônibus nessa linha. Eu tinha esperado no ponto por mais de uma hora. Ele parou só para mim.","personagens":[sent("ele","olhando",0.35,0.9)]},
 {"cenario":"onibus_traseira","letreiro":True,"dist":0.8,"duracao":4,"zoom":[1,1.12],"respiro":1.5,"narracao":"E os passageiros... estavam ali para me conferir."}])
save('c19_onibus.json',c19)
save('c19_sons.json',{"versao":1,"episodio":"c19","nota":"Onibus: motor constante, sem musica; stinger quando todos olham; corte seco no letreiro.","cues":[
 {"cena":1,"offset":0,"tipo":"elevadorZumbido","ateCena":3,"params":{"vol":0.45}},
 {"cena":2,"offset":0,"tipo":"stinger","params":{"intensidade":0.4}},
 {"cena":4,"offset":0,"tipo":"vento","ateCena":4,"params":{"vol":0.2}},
 {"cena":5,"offset":0,"tipo":"elevadorZumbido","ateCena":5,"params":{"vol":0.4}},
 {"cena":6,"offset":0,"tipo":"corte","params":{}}]})
# ---------- c20 Celular 3h17 ----------
t20=["Eram 3h17 quando meu celular tocou. A tela mostrava meu número."]
c20=base(numero=20,nome="Celular 3h17",cartela={"titulo":"Celular 3h17","sub":"Original · não atenda"},cor="#FF3AA0",arquivo="20_celular_3h17.mp4",destaque=["celular","voz","quarto","eu"],sons="c20_sons.json",
 vozes={"narrador":["pt-BR-AntonioNeural","-2%","-12Hz"],"eu":["pt-BR-AntonioNeural","-2%","-12Hz"],"voz":["pt-BR-AntonioNeural","-10%","-12Hz"]},
 elenco={"eu":{"camisa":"#8A5A7A","calca":"#2A2A3A","cabelo":"#1B1412","pele":"#D8B08C","estilo":"curto"}},
 cenas=[
 {"cenario":"quarto_magenta","toca":True,"duracao":5,"zoom":[1,1.08],"narracao":"Eram três e dezessete quando meu celular tocou. A tela mostrava meu número."},
 {"cenario":"quarto_magenta","toca":True,"duracao":3,"zoom":[1,1.1],"narracao":"Atendi, curioso.","falas":[{"quem":"eu","texto":"Alô?"}]},
 {"cenario":"quarto_magenta","duracao":6,"zoom":[1,1.1],"narracao":"Do outro lado, minha própria voz, baixa, tensa:","falas":[{"quem":"voz","texto":"Não saia do quarto. Escute com atenção."}]},
 {"cenario":"corredor_magenta","passos":True,"duracao":5,"zoom":[1,1.1],"narracao":"Passos lentos no corredor. Devagar, parando em frente à porta."},
 {"cenario":"quarto_magenta","duracao":6,"zoom":[1,1.08],"respiro":0.8,"narracao":"Segurei a respiração. Um minuto. Dois. Depois, os passos se afastaram."},
 {"cenario":"quarto_magenta","duracao":4,"zoom":[1,1.1],"narracao":"Minha voz falou de novo:","falas":[{"quem":"voz","texto":"Agora pode."}]},
 {"cenario":"quarto_magenta","duracao":6,"zoom":[1,1.06],"narracao":"Desligou. Só fui olhar a câmera da sala no dia seguinte. A gravação mostrava a cena inteira."},
 {"cenario":"corredor_magenta","duracao":7,"zoom":[1,1.06],"narracao":"Às três e dezessete, eu estava de pé no corredor, com o celular no ouvido, em frente à porta do meu quarto.","personagens":[sent("eu","telefone",0.5,0.9)],"objetos":[{"tipo":"camera_rec","texto":"CAM 02  CORREDOR  03:17:04","entra":0}]},
 {"cenario":"quarto_magenta","vazio":True,"duracao":5,"zoom":[1,1.1],"respiro":2.0,"narracao":"Era eu quem andava. E o quarto, naquele momento, estava vazio."}])
save('c20_celular_3h17.json',c20)
save('c20_sons.json',{"versao":1,"episodio":"c20","nota":"Celular: toque, passos no corredor, silencio total depois; sem musica.","cues":[
 {"cena":1,"offset":0.2,"tipo":"celularToque","params":{"abafado":False,"vol":0.7}},
 {"cena":4,"offset":0.3,"tipo":"passosChinelo","params":{"n":4,"passo":1.1,"vol":0.9}},
 {"cena":1,"offset":0,"tipo":"zumbidoLuz","ateCena":8,"params":{"vol":0.06}},
 {"cena":9,"offset":0,"tipo":"corte","params":{}}]})
idx=json.load(open(D+'indice.json',encoding='utf-8'))
idx.update({"c17":"c17_retrato_oval.json","c18":"c18_lobisomem.json","c19":"c19_onibus.json","c20":"c20_celular_3h17.json"})
json.dump(idx,open(D+'indice.json','w',encoding='utf-8'),indent=2,ensure_ascii=False)
