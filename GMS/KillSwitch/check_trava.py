import sys,glob,json,re,os,urllib.parse
try:
    import yaml
    yaml.SafeLoader.add_constructor('tag:yaml.org,2002:value',lambda l,n:'=')
except ImportError:
    print("sem pyyaml"); sys.exit(3)
root=sys.argv[1]; orig=sys.argv[2]
names=set()
for f in glob.glob(root+'/DataSources/*.json'):
    d=json.loads(open(f,'rb').read().decode('utf-8-sig','replace'))
    for o in d:
        if o.get('Type')=='ConnectedDataSourceInfo':
            names.add(o['Name']); names.add(urllib.parse.unquote(os.path.basename(f)[:-5],encoding='cp1252'))
names={n for n in names if '�' not in n}
V='varCompostoPermitida'
def walk(node,path,out,cnt):
    for k,v in node.items():
        m=re.match(r'^(.*?) As ([\w.]+)$',k)
        if m and isinstance(v,dict):
            cnt[0]+=1; walk(v,path+[m.group(1)],out,cnt)
        elif isinstance(v,str): out.append((path,k,v))
def load(d):
    res={}
    for f in sorted(glob.glob(d+'/Src/*.fx.yaml')):
        y=yaml.safe_load(open(f,encoding='utf-8'))
        out=[];cnt=[0]; walk(y,[],out,cnt)
        res[os.path.basename(f)]=(out,cnt[0])
    return res
new=load(root); old=load(orig)
bad_on=bad_t=bad_c5=0; ctr_ok=True
for f,(props,c) in new.items():
    if c!=old[f][1]: ctr_ok=False; print("CONTROLES DIFERENTES",f,c,old[f][1])
    if f=='App.fx.yaml': continue
    for path,k,v in props:
        beh=re.match(r'^On[A-Z]',k) and k not in('OnColor','OnFill')
        s=v.strip()
        if beh:
            if s.lstrip('=').strip().lower() in ('','false','true'): continue
            if V not in v:
                bad_on+=1; print('ON sem trava',f,path[-1:],k)
                if k=='OnTimerEnd': bad_t+=1
        else:
            if k=='DataSource': continue
            code=re.sub(r'"(?:[^"]|"")*"','""',v)
            code=re.sub(r'//[^\n]*','',code)
            for n in names:
                if re.search(r"(?<![\w.'])(?:'%s'|%s)(?![\w'])"%(re.escape(n),re.escape(n)),code) and V not in v:
                    bad_c5+=1; print('C5 sem trava',f,path[-1:],k,n); break
print("On* sem trava:",bad_on,"| OnTimerEnd sem trava:",bad_t,"| nao-On lendo fonte sem trava:",bad_c5,"| controles iguais:",ctr_ok, "| total controles", sum(c for _,c in new.values()))
# equivalencia: tirar o embrulho e comparar com o original (so espaco muda)
bad=0;nw=0
for f,(props,c) in new.items():
    o={ (tuple(p),k):v for p,k,v in old[f][0]}
    for p,k,v in props:
        ov=o.get((tuple(p),k))
        if ov is None or ov==v: continue
        nw+=1
        m=re.match(r'^=If\(varCompostoPermitida,\n(.*)\n\s*\)$',v,re.S)
        if not m: bad+=1; print('formato',f,p[-1:],k); continue
        a=re.sub(r'\s+','',m.group(1)); b=re.sub(r'\s+','',ov.lstrip()[1:])
        if a!=b: bad+=1; print('DIFERE',f,p[-1:],k)
print('embrulhadas',nw,'divergentes',bad)
