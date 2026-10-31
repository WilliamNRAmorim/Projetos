import json
D='C:/Users/willi/Downloads/Projetos/Conteudo_Bit/Producao/serie/ep/'
def save(n,d): json.dump(d,open(D+n,'w',encoding='utf-8'),indent=2,ensure_ascii=False)
base=lambda **k: dict({"proxima":False,"legenda":"palavras","legendaY":1380,"legendaTam":125,"escurece":0.06,"saida":"contos-dia7","camadas":{"voz":1,"trilha":1,"efeitos":1,"musicaWav":0},"respiros":{"lead":0.12,"gap":0.2,"tail":0.4},"duck":0.35},**k)
sent=lambda i,pose,x,e=0.9,**k: dict({"id":i,"pose":pose,"x":x,"escala":e,"semEntrada":True,"fica":True},**k)
# ---------- c25 A Máscara da Morte Rubra ----------
GEO="JBFqnCBsd6RMkjVDRZzb"
t25=["Uma peste chamada Morte Rubra devastava o país. Quem a pegava morria em meia hora.",
"O príncipe Próspero reuniu mil amigos numa abadia fortificada e soldou os portões.",
"Depois de meses, deram um baile de máscaras em sete salões coloridos.",
"O último, todo preto, tinha um relógio de ébano. A cada hora, a música parava.",
"À meia-noite, surgiu uma figura alta, em mortalha, com máscara de cadáver e roupas manchadas de vermelho.",
"Próspero, furioso, perseguiu-a de sala em sala com um punhal.",
"No último salão, a figura se virou. O príncipe caiu morto.",
"Quando a agarraram, debaixo da mortalha não havia ninguém.",
"A Morte Rubra reinava sobre todos."]
mo=lambda x,e,y=940,**k: dict({"tipo":"morte_mascara","x":x,"escala":e,"y":y,"entra":0},**k)
cen25=[
 {"cenario":"ceu_rubro","duracao":6},
 {"cenario":"abadia_muralha","duracao":6,"personagens":[sent("pros","neutro",0.5,0.55)]},
 {"cenario":"salao_cores","cor":"azul","proximo":"roxo","duracao":5,"personagens":[sent("gu1","maosDadas",0.28,0.8),sent("gu2","neutro",0.72,0.8)]},
 {"cenario":"relogio_ebano","hora":[12,0],"toca":True,"tocaEm":4.0,"duracao":6.5},
 {"cenario":"salao_cores","cor":"branco","proximo":"violeta","duracao":7,"personagens":[sent("gu1","assustado",0.18,0.7),sent("gu2","medo",0.84,0.7)],"objetos":[mo(0.5,0.42)]},
 {"cenario":"salao_cores","cor":"laranja","proximo":"branco","duracao":5,"personagens":[sent("pros","correndo",0.25,0.8)],"objetos":[mo(0.5,0.4)]},
 {"cenario":"salao_cores","cor":"preto","duracao":5,"zoom":[1,1.12],"personagens":[sent("pros","medo",0.2,0.85,ate=3.6)],"objetos":[mo(0.55,1.15,1240)]},
 {"cenario":"salao_cores","cor":"preto","duracao":5,"personagens":[sent("gu1","assustado",0.18,0.8),sent("gu2","medo",0.82,0.8)],"objetos":[{"tipo":"mortalha_vazia","x":0.5,"y":1240,"entra":0.3}]},
 {"cenario":"salao_cores","cor":"preto","apaga":True,"duracao":5,"respiro":2.0,"zoom":[1,1.1]}]
for i,c in enumerate(cen25):
    c["zoom"]=c.get("zoom",[1,1.07]); c["falas"]=[{"quem":"nar","arquivo":f"g{i+1}.wav","texto":t25[i]}]
c25=base(numero=25,nome="A Máscara da Morte Rubra",cartela={"titulo":"Máscara da Morte Rubra","sub":"Edgar Allan Poe · 1842"},cor="#D01030",arquivo="25_mascara_da_morte_rubra.mp4",destaque=["morte","rubra","relógio","ninguém"],sons="c25_sons.json",
 respiros={"lead":0.2,"gap":0.3,"tail":0.5},duck=0.4,
 eleven={f"g{i+1}.wav":{"voz":GEO,"texto":"[solemnly] "+t25[i],"pico":0.6} for i in range(9)},
 elenco={"pros":{"camisa":"#7A2AA0","blusa":"#E8D8F0","calca":"#2A1A3A","cabelo":"#2A1A10","pele":"#D8B08C","estilo":"curto","bigode":True},"gu1":{"camisa":"#2A5AD0","calca":"#1A2A5A","cabelo":"#4A2A1A","pele":"#D8B08C","estilo":"longo"},"gu2":{"camisa":"#E8842A","calca":"#5A2A1A","cabelo":"#1A1210","pele":"#C99A74","estilo":"curto"}},cenas=cen25)
save('c25_mascara.json',c25)
save('c25_sons.json',{"versao":1,"episodio":"c25","nota":"Mascara da Morte Rubra: drone grave, badalada do relogio com silencio, corte total na ultima frase.","cues":[
 {"cena":1,"offset":0,"tipo":"drone","ateCena":8,"params":{"tomInicial":36,"subida":2,"vol":0.28}},
 {"cena":1,"offset":0,"tipo":"vento","ateCena":2,"params":{"vol":0.25}},
 {"cena":4,"offset":4.0,"tipo":"badalada","params":{"vol":0.8}},
 {"cena":4,"offset":4.2,"tipo":"silencio","params":{"dur":1.8}},
 {"cena":7,"offset":0,"tipo":"batimento","ateCena":7,"params":{"bpm":80,"vol":0.4}},
 {"cena":9,"offset":0,"tipo":"corte","params":{}}]})
# ---------- c26 Iara ----------
t26=["O pescador remava sozinho quando a canção chegou, doce, vinda da água.",
"Ele sabia que era a Iara, a sereia do rio que atrai os homens. Pôs os dedos nos ouvidos.",
"Não adiantou. A voz entrava pelos dedos, pelos ossos.",
"E, de repente, ela cantou o nome dele. Com a voz da esposa:",
"Ele olhou. Era a esposa, de camisola, de pé sobre a água, com os cabelos soltos.",
"Mas a esposa estava em casa, com febre, de cama.",
"A voz dizia, doce:",
"Ele pulou do barco.",
"De manhã, a canoa foi achada rodando no meio do rio.",
"E na margem, a esposa, curada da febre, sem saber por quê."]
P=lambda pose,**k: sent("pesc",pose,0.69,0.7,y=140,**k)
cen26=[
 {"cenario":"rio_iara","canoa":0.69,"personagens":[P("neutro")],"duracao":5},
 {"cenario":"rio_iara","canoa":0.69,"iara":0.3,"personagens":[P("orelhas")],"duracao":7},
 {"cenario":"rio_iara","canoa":0.69,"ondas":True,"personagens":[P("orelhas")],"duracao":5},
 {"cenario":"rio_iara","canoa":0.69,"ondas":True,"iara":0.6,"personagens":[P("medo")],"duracao":5,"falas":[{"quem":"esp","texto":"Zé... volta para casa, Zé..."}]},
 {"cenario":"rio_iara","canoa":0.69,"iara":1,"personagens":[P("olhando"),sent("esp","sorrindo",0.22,0.9)],"duracao":7},
 {"cenario":"quarto_lua","olhos":"fechados","duracao":4},
 {"cenario":"rio_iara","canoa":0.69,"iara":1,"personagens":[sent("esp","sorrindo",0.28,1.4,y=120)],"duracao":4,"falas":[{"quem":"esp","texto":"Vem. Eu te espero."}]},
 {"cenario":"rio_iara","canoa":0.69,"ondas":True,"ondasX":745,"ondasY":1400,"duracao":3},
 {"cenario":"rio_iara","manha":True,"canoa":0.5,"gira":True,"duracao":5},
 {"cenario":"rio_iara","manha":True,"margem":True,"personagens":[sent("esp","aliviada",0.5,1.0)],"duracao":5,"respiro":1.5}]
rt26=[("-18%","+6Hz")]*10
for i,c in enumerate(cen26):
    c["zoom"]=[1,1.08]; c["narracao"]=t26[i]; c["rateNarrador"]="-18%"; c["pitchNarrador"]="+6Hz"
cen26[7]["personagens"]=[P("assustado",ate=1.4)]
c26=base(numero=26,nome="Iara",cartela={"titulo":"Iara","sub":"Folclore brasileiro"},cor="#2ACFCF",arquivo="26_iara.mp4",destaque=["iara","canção","água","vem"],sons="c26_sons.json",
 vozes={"narrador":["pt-BR-FranciscaNeural","-18%","+6Hz"],"esp":["pt-BR-ThalitaMultilingualNeural","-14%","+12Hz"]},
 elenco={"pesc":{"camisa":"#8A6A3A","calca":"#4A4A3A","cabelo":"#2A1E10","pele":"#B98560","estilo":"curto"},"esp":{"camisa":"#E8E4F0","calca":"#E8E4F0","cabelo":"#2A1810","pele":"#E0BC9C","estilo":"longo"}},cenas=cen26)
save('c26_iara.json',c26)
save('c26_sons.json',{"versao":1,"episodio":"c26","nota":"Iara: canto distante (cantarolar), agua e remos; corte na ultima cena da noite; passaros de manha.","cues":[
 {"cena":1,"offset":0,"tipo":"remo","ateCena":3,"params":{"ritmo":1.4,"vol":0.4}},
 {"cena":1,"offset":0.5,"tipo":"cantarolar","ateCena":7,"params":{"vol":0.5}},
 {"cena":1,"offset":0,"tipo":"vento","ateCena":8,"params":{"vol":0.15}},
 {"cena":9,"offset":0,"tipo":"passaros","ateCena":10,"params":{"vol":0.6}}]})
# ---------- c27 Homem do Saco ----------
JES="cgSgspJ2msm6clMCkdW9"; LIL="pFZP5JQG7iQjIQuC4Bku"
t27=["Quando eu era pequena, minha mãe sempre dizia: Se ouvir o Homem do Saco passar, fica quietinha. Ele só leva quem faz barulho.",
"Naquela noite, ouvi os passos arrastando na rua. O saco batendo no chão, pesado, mexendo.",
"Fiquei quietinha na cama, tapando a boca com a mão.",
"Os passos pararam em frente à nossa casa.",
"Do saco, vinha uma coisa: uns sussurros, muito baixinhos. Várias vozes de criança.",
None,
"Eu apertei a boca com as duas mãos. Depois de muito tempo, os passos foram embora.",
"Hoje, adulta, eu me lembro sempre dessas vozes.",
"O que eu nunca soube é por que elas estavam do lado de dentro."]
cen27=[
 {"cenario":"quarto_lilas","duracao":8,"personagens":[sent("ma","silencio",0.78,0.9)]},
 {"cenario":"rua_lilas","homem":0.15,"arrasta":True,"duracao":6},
 {"cenario":"quarto_lilas","mao":True,"duracao":4},
 {"cenario":"rua_lilas","homem":0.42,"duracao":3.5},
 {"cenario":"saco_close","duracao":6},
 {"cenario":"saco_close","duracao":8,"falas":[{"quem":"cri","arquivo":"w1.wav","texto":"Fica quieta..."},{"quem":"cri","arquivo":"w2.wav","texto":"Não responde..."},{"quem":"cri","arquivo":"w3.wav","texto":"Ele só leva quem responde..."}]},
 {"cenario":"quarto_lilas","mao":True,"duracao":6},
 {"cenario":"rua_lilas","duracao":4},
 {"cenario":"rua_lilas","duracao":5,"respiro":2.0,"zoom":[1,1.1]}]
for i,c in enumerate(cen27):
    c.setdefault("zoom",[1,1.07])
    if t27[i]: c["falas"]=[{"quem":"nar","arquivo":f"j{i+1}.wav","texto":t27[i]}]
el27={f"j{i+1}.wav":{"voz":JES,"texto":"[softly] "+t27[i],"pico":0.55} for i in range(9) if t27[i]}
el27.update({"w1.wav":{"voz":LIL,"texto":"[whispers] Fica quieta...","pico":0.5},"w2.wav":{"voz":LIL,"texto":"[whispers] Não responde...","pico":0.5},"w3.wav":{"voz":LIL,"texto":"[whispers] Ele só leva quem responde...","pico":0.5}})
c27=base(numero=27,nome="Homem do Saco",cartela={"titulo":"Homem do Saco","sub":"Folclore brasileiro"},cor="#9A8AC8",arquivo="27_homem_do_saco.mp4",destaque=["saco","quietinha","vozes","dentro"],sons="c27_sons.json",
 respiros={"lead":0.25,"gap":0.3,"tail":0.55},duck=0.4,eleven=el27,
 elenco={"ma":{"camisa":"#9A7AB8","calca":"#4A3A5A","cabelo":"#2A1810","pele":"#D8B08C","estilo":"coque"}},cenas=cen27)
save('c27_homem_saco.json',c27)
save('c27_sons.json',{"versao":1,"episodio":"c27","nota":"Homem do saco: passos e saco arrastando, silencio quando param, batimento lento, vento fraco.","cues":[
 {"cena":1,"offset":0,"tipo":"vento","ateCena":8,"params":{"vol":0.2}},
 {"cena":2,"offset":0.3,"tipo":"arrastar","params":{"dur":5.5,"ritmo":1.1,"vol":0.5}},
 {"cena":5,"offset":0,"tipo":"batimento","ateCena":7,"params":{"bpm":62,"vol":0.35}},
 {"cena":9,"offset":0,"tipo":"corte","params":{}}]})
# ---------- c28 Vizinho bate na parede ----------
t28=["Mudei para um apartamento novo, no sexto andar.",
"Na primeira noite, ouvi na parede do quarto: toc, toc, toc.",
"Achei que era o vizinho. Por educação, bati de volta, três vezes.",
"Silêncio. Depois, de novo: toc, toc, toc. Mais forte.",
"Bati de volta, brincando. Agora, mais devagar.",
"Do outro lado, a resposta foi rápida: toc, toc, toc, toc, toc, toc, toc.",
"Fiquei imóvel.",
"De manhã, perguntei ao síndico quem morava no apartamento vizinho ao meu quarto. Ele franziu a testa.",
"Sexto andar. Só tem o vazio. Desde então, não bato mais."]
rt28=[("+8%","+6Hz"),("+6%","+4Hz"),("+4%","+2Hz"),("+0%","+0Hz"),("-4%","-2Hz"),("-6%","-4Hz"),("-10%","-8Hz"),("-8%","-6Hz"),("-12%","-10Hz")]
E=lambda pose,x=0.3,**k: sent("eu",pose,x,0.9,**k)
cen28=[
 {"cenario":"quarto_salmao","personagens":[E("neutro",0.3)],"duracao":4},
 {"cenario":"quarto_salmao","ondas":True,"personagens":[E("neutro",0.3)],"duracao":5},
 {"cenario":"quarto_salmao","ondas":True,"personagens":[E("apontando",0.3)],"duracao":5},
 {"cenario":"quarto_salmao","ondas":True,"personagens":[E("assustado",0.3)],"duracao":5},
 {"cenario":"quarto_salmao","ondas":True,"personagens":[E("hesitante",0.3)],"duracao":4},
 {"cenario":"quarto_salmao","ondas":True,"personagens":[E("medo",0.3)],"duracao":6},
 {"cenario":"quarto_salmao","personagens":[E("encarando",0.3)],"duracao":3,"respiro":0.8},
 {"cenario":"fundo_cor","topo":"#B8705A","base":"#3A1810","brilho":"#E8825A","duracao":8,"personagens":[E("neutro",0.25),sent("sin","neutro",0.65,0.9)],"falas":[{"quem":"sin","texto":"Nenhum. Essa parede dá para a rua."}]},
 {"cenario":"predio_vazio","duracao":6,"respiro":2.0,"zoom":[1,1.1]}]
for i,c in enumerate(cen28):
    c.setdefault("zoom",[1,1.08]); c["narracao"]=t28[i]; c["rateNarrador"]=rt28[i][0]; c["pitchNarrador"]=rt28[i][1]
c28=base(numero=28,nome="Vizinho bate na parede",cartela={"titulo":"Vizinho bate na parede","sub":"Original · não bata de volta"},cor="#E8825A",arquivo="28_vizinho_bate_na_parede.mp4",destaque=["toc","parede","sexto","vazio"],sons="c28_sons.json",
 vozes={"narrador":["pt-BR-ThalitaMultilingualNeural","+8%","+6Hz"],"sin":["pt-BR-AntonioNeural","-6%","-8Hz"]},
 elenco={"eu":{"camisa":"#6A8AB0","calca":"#2A2A3A","cabelo":"#2A1810","pele":"#D8B08C","estilo":"longo"},"sin":{"camisa":"#6A5A3A","calca":"#3A3326","cabelo":"#8C8B86","pele":"#B98560","estilo":"careca","bigode":True}},cenas=cen28)
save('c28_vizinho.json',c28)
save('c28_sons.json',{"versao":1,"episodio":"c28","nota":"Vizinho: batidas na parede (tres, tres, sete rapidas); silencio; sem musica.","cues":[
 {"cena":2,"offset":3.0,"tipo":"batidas","params":{"n":3,"espacamento":0.5,"vol":0.5}},
 {"cena":3,"offset":3.2,"tipo":"batidas","params":{"n":3,"espacamento":0.5,"vol":0.5}},
 {"cena":4,"offset":2.2,"tipo":"batidas","params":{"n":3,"espacamento":0.4,"vol":0.7}},
 {"cena":5,"offset":2.0,"tipo":"batidas","params":{"n":3,"espacamento":0.8,"vol":0.5}},
 {"cena":6,"offset":2.5,"tipo":"batidas","params":{"n":7,"espacamento":0.16,"vol":0.8}},
 {"cena":1,"offset":0,"tipo":"zumbidoLuz","ateCena":7,"params":{"vol":0.05}},
 {"cena":9,"offset":0,"tipo":"vento","ateCena":9,"params":{"vol":0.25}}]})
idx=json.load(open(D+'indice.json',encoding='utf-8'))
idx.update({"c25":"c25_mascara.json","c26":"c26_iara.json","c27":"c27_homem_saco.json","c28":"c28_vizinho.json"})
json.dump(idx,open(D+'indice.json','w',encoding='utf-8'),indent=2,ensure_ascii=False)
