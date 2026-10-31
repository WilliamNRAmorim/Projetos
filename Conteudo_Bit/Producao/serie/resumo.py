import json,sys
t=open(sys.argv[1],encoding='utf-8').read(); d=json.loads(t[t.index('{"motor"'):]); m=json.loads(d['mix']); mo=json.loads(d['motor'])
print({k:v for k,v in m.items() if k!='porCena'}, 'dur',mo['dur'])
for c in m['porCena']: print(c['cena'],'voz',c['vozDb'],'cama',c['camaSobVozDb'],'marg',c['margemDb'],'p5',c['margemP5Db'],'<6dB',c['janelasAbaixo6dB'],'/',c['janelasFala'],'semvoz',c['camaSemVozDb'])
