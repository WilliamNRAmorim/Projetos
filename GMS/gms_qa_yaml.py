import yaml, re, sys, collections, os, builtins
# Power Apps usa "= " sozinho (propriedade vazia); PyYAML trata como tag :value
yaml.SafeLoader.add_constructor('tag:yaml.org,2002:value', lambda l,n: "=")

# [v5 · 22/10] Saida com codigo 1 quando algum teste imprimir FALHOU (alerta nao conta).
_FALHOU = []
_print0 = builtins.print
def print(*a, **k):
    t = " ".join(str(x) for x in a)
    for ln in t.split("\n"):
        if "FALHOU" in ln and not ln.lstrip().startswith("==="): _FALHOU.append(ln[:120])
    _print0(*a, **k)
def _sai(code=None):
    if code is None: code = 1 if _FALHOU else 0
    _print0("\n>>> RESULTADO:", ("FALHOU em %d teste(s) -> exit 1" % len(_FALHOU)) if code else "sem FALHOU -> exit 0")
    sys.exit(code)

def mascara(f):
    """Texto de strings e comentarios trocado por 'x'/espaco, mesmo tamanho (indices preservados)."""
    o=[]; i=0; n=len(f)
    while i<n:
        c=f[i]
        if c=='"':
            o.append('"'); i+=1
            while i<n and f[i]!='"': o.append('x' if f[i]!="\n" else "\n"); i+=1
            o.append('"'); i+=1
        elif f.startswith("//",i):
            while i<n and f[i]!="\n": o.append(" "); i+=1
        elif f.startswith("/*",i):
            j=f.find("*/",i+2); j=n if j<0 else j+2
            o.append("".join(" " if ch!="\n" else "\n" for ch in f[i:j])); i=j
        else: o.append(c); i+=1
    return "".join(o)

def args_de(m, ini):
    """m = texto mascarado; ini = indice logo apos '('. Devolve ([(a,b) de cada argumento], indice apos ')')."""
    prof=1; i=ini; a=ini; out=[]
    while i<len(m) and prof:
        c=m[i]
        if c in "({[": prof+=1
        elif c in ")}]":
            prof-=1
            if prof==0: out.append((a,i))
        elif c=="," and prof==1: out.append((a,i)); a=i+1
        i+=1
    return out, i

def ultimo_stmt(t):
    prof=0; ult=0
    for i,c in enumerate(t):
        if c in "({[": prof+=1
        elif c in ")}]": prof-=1
        elif c==";" and prof==0: ult=i+1
    return t[ult:].strip()

def formulas_fx(caminho):
    """Definicoes do Formulas.txt: {nome: [linhas]} ou None se nao existir."""
    d=collections.defaultdict(list)
    try:
        for i,l in enumerate(open(caminho,encoding="utf-8").read().split("\n"),1):
            m=re.match(r"(fx_\w+)", l)
            if m: d[m.group(1)].append(i)
    except OSError: return None
    return d

AQUI = os.path.dirname(os.path.abspath(__file__))
FORMULAS_TXT = os.path.join(AQUI, "Telas", "Formulas.txt")

if len(sys.argv)<2:
    print("uso: python gms_qa_yaml.py Telas/scr_X.txt"); sys.exit(2)
path = sys.argv[1]
try:
    with open(path, encoding="utf-8-sig") as fh: raw = fh.read()
except (OSError, ValueError) as e:
    print("FALHOU: nao consegui ler", path, e); sys.exit(1)

if os.path.basename(path).lower()=="formulas.txt":
    print("=== F. Formulas.txt (App.Formulas) ===")
    defs=formulas_fx(path)
    dups={k:v for k,v in defs.items() if len(v)>1}
    print("fx_ duplicada:", "OK" if not dups else "FALHOU: "+str(dups))
    m=mascara(raw)
    pilha=[]; mal=None
    for i,ch in enumerate(m):
        if ch in "({[": pilha.append((ch,i))
        elif ch in ")}]":
            if not pilha or {")":"(","}":"{","]":"["}[ch]!=pilha[-1][0]: mal=i; break
            pilha.pop()
    if pilha and mal is None: mal=pilha[-1][1]
    print("Parenteses/chaves:", "OK" if mal is None else "FALHOU: linha %d" % (raw[:mal].count("\n")+1))
    ruins=[]
    for dm in re.finditer(r"^(fx_\w+)(\s*\()?", m, re.M):
        if dm.group(2): continue
        fim=m.find(";", dm.end())
        corpo=m[dm.end(): fim if fim>=0 else len(m)]
        if re.search(r"\b(Now|Today|Rand)\(\)", corpo): ruins.append(dm.group(1))
    print("Now()/Today()/Rand() em Named Formula:", "OK" if not ruins else "FALHOU: "+str(ruins))
    print("Definicoes fx_:", len(defs))
    _sai()

print("=== 1. PARSE PyYAML ===")
try:
    doc = yaml.safe_load(raw)
    print("OK")
except Exception as e:
    print("FALHOU:", e); _sai(1)

VERSOES_OK = {
 "Classic/Button":"2.2.0","Classic/TextInput":"2.3.2","Classic/DropDown":"2.3.1",
 "Classic/ComboBox":"2.4.0","Classic/Icon":"2.5.0","Classic/DatePicker":"2.6.0",
 "Label":"2.5.1","Rectangle":"2.3.0","GroupContainer":"1.5.0","Gallery":"2.15.0",
 "Timer":"2.1.0","Image":"2.2.3","Spinner":"1.4.6","HtmlViewer":"2.1.0",
 "ModernText":"1.0.0","ModernIcon":"1.1.1","BarcodeReader":"1.0.25",
 "Form":"2.4.4","Attachments":"2.3.0","FormViewer":"2.3.4","TypedDataCard":"1.0.7","ModernButton":"1.0.0",
 "PenInput":"2.1.0",  # [21/10] MEL-114 caneta do zoom da foto; versao NAO provada no Studio
}

nomes = []
ctrls = []
def walk(node):
    if isinstance(node, dict):
        for k,v in node.items():
            if isinstance(v, dict) and "Control" in v:
                nomes.append(k); ctrls.append((k, v["Control"]))
                walk(v.get("Children"))
            else:
                walk(v)
    elif isinstance(node, list):
        for i in node: walk(i)

screens = (doc or {}).get("Screens") if isinstance(doc, dict) else None
if not isinstance(screens, dict):
    print("FALHOU: YAML sem 'Screens'"); sys.exit(1)
for sname, sbody in screens.items():
    sbody = sbody or {}
    nomes.append(sname)
    walk(sbody.get("Children"))

print("\n=== 2. PA1001 (nomes duplicados) ===")
dup = [n for n,c in collections.Counter(nomes).items() if c>1]
print("OK - nenhum duplicado" if not dup else f"FALHOU: {dup}")

print("\n=== 3. Versoes de controle (B 3.8.6) ===")
bad=[]
for n,c in ctrls:
    tipo, ver = c.rsplit("@",1)
    if tipo not in VERSOES_OK: bad.append((n,c,"tipo fora da lista"))
    elif VERSOES_OK[tipo]!=ver: bad.append((n,c,f"esperado @{VERSOES_OK[tipo]}"))
print("OK" if not bad else "FALHOU: "+str(bad))

print("\n=== 4. Nome sem espaco / prefixo (1.1) ===")
comesp=[n for n in nomes if " " in n]
print("Com espaco (legado mantido):", comesp if comesp else "nenhum")
PREFIX = ("scr_","gal_","frm_","ctn_","cntr_","btn_","ico_","rct_","lbl_","tmr_",
          "cmb_","inp_","spr_","html_","dc_","bcr_","chk_","tgl_","dte_","img_","cmp_","att_","pen_")
sem_prefixo=[n for n in nomes if not n.startswith(PREFIX)]
print("Sem prefixo de tipo:", sem_prefixo if sem_prefixo else "nenhum")

print("\n=== 5. Balanceamento de parenteses/chaves/colchetes por formula ===")
def coleta_formulas(node, prefix=""):
    out=[]
    if isinstance(node, dict):
        for k,v in node.items():
            if isinstance(v,dict) and "Control" in v:
                for pk,pv in (v.get("Properties") or {}).items():
                    if isinstance(pv,str): out.append((k+"."+pk, pv))
                out += coleta_formulas(v.get("Children"), k)
            else:
                out += coleta_formulas(v, prefix)
    elif isinstance(node,list):
        for i in node: out += coleta_formulas(i, prefix)
    return out

formulas=[]
for sname,sbody in screens.items():
    for pk,pv in (sbody.get("Properties") or {}).items():
        if isinstance(pv,str): formulas.append((sname+"."+pk,pv))
    formulas += coleta_formulas(sbody.get("Children"))

def desbalanceado(f):
    s = re.sub(r'"(?:[^"\\]|\\.)*"', '""', f, flags=re.S)
    s = re.sub(r"//[^\n]*", "", s)
    pares={")":"(","}":"{","]":"["}
    pilha=[]
    for ch in s:
        if ch in "({[": pilha.append(ch)
        elif ch in ")}]":
            if not pilha or pilha[-1]!=pares[ch]: return True
            pilha.pop()
    return bool(pilha)

ruins=[(n,) for n,f in formulas if desbalanceado(f)]
print("OK" if not ruins else "FALHOU: "+str(ruins))

print("\n=== 6. Padroes proibidos ===")
proib = {
 "Now() comparado a numero (3.3)": r"Now\(\)\s*[<>]=?\s*\d",
 "Hour(Now()) comparado a numero (3.3)": r"Hour\(\s*Now\(\)\s*\)\s*[<>]=?\s*\d",
 "filtro por Modified (3.3)": r"(Filter|LookUp)\([^)]*\bModified\b\s*[<>=]",
 "referencia a .Text de Label em logica (3.10.2)": r"lbl_\w+\.Text\s*=",
 "Form/TypedDataCard (3.12)": r"(TypedDataCard|Control:\s*Form@|FormViewer@|SubmitForm|ResetForm|EditForm|NewForm|\.Updates|\.Valid\b)",
}
for nome,rx in proib.items():
    hits=[n for n,f in formulas if re.search(rx,f)]
    print(f"{nome}: {'OK' if not hits else 'ACHOU '+str(hits)}")

tmr_bad=[]
for n,c in ctrls:
    if c.startswith("Timer@"):
        for fn,f in formulas:
            if fn.startswith(n+".") and re.search(r"\bPatch\(", f): tmr_bad.append(fn)
print("Patch dentro de Timer (3.4):", "OK" if not tmr_bad else tmr_bad)

print("\n=== 7. Referencia orfa a controle ===")
# [v5 · 22/10] Reconhece: colecoes criadas no arquivo (Collect/ClearCollect em qualquer propriedade),
# variaveis Set(), aliases "As x", colunas de record ({a: ..., b: ...}) e nomes fx_ do Formulas.txt.
conhecidos=set(nomes)|{"Parent","Self","ThisItem","App","ThisRecord"}
for n,f in formulas:
    m_=mascara(f)
    conhecidos |= set(re.findall(r"\b(?:Clear)?Collect\(\s*([A-Za-zÀ-ÿ_]\w*)", m_))
    conhecidos |= set(re.findall(r"\bSet\(\s*([A-Za-zÀ-ÿ_]\w*)", m_))
    conhecidos |= set(re.findall(r"\bAs\s+([A-Za-zÀ-ÿ_]\w*)", m_))
    conhecidos |= set(re.findall(r"[{,(]\s*([A-Za-zÀ-ÿ_]\w*)\s*:(?!=)", m_))
_dfx=formulas_fx(FORMULAS_TXT)
if _dfx: conhecidos |= set(_dfx)
refs=set()
for n,f in formulas:
    mf=mascara(f)
    # colunas de fonte em escopo implicito: argumentos 2+ de Filter/LookUp/AddColumns/Sort/Search/ForAll/Sum...
    esc=[]
    for tm in re.finditer(r"\b(Filter|LookUp|AddColumns|Sort|SortByColumns|Search|ForAll|Sum|Average|Max|Min|CountIf|With|Concat|RenameColumns|GroupBy|Distinct|First|Last|FirstN|LastN)\(", mf):
        ags,_=args_de(mf, tm.end())
        esc += [(a,b) for a,b in ags[1:]]
    for m in re.finditer(r"(?<![\w.])([A-Za-zÀ-ÿ_][A-Za-zÀ-ÿ0-9_]*)\.(Text|Selected|SelectedDate|Value|X|Y|Width|Height|Fill|Visible|DisplayMode|Barcodes|AllItems)\b", mf):
        if any(a<=m.start()<b for a,b in esc): continue
        refs.add(m.group(1))
orfas=sorted(r for r in refs if r not in conhecidos)
print("Refs nao resolvidas (checar se sao fontes/vars/alias As):", orfas)

print("\n=== 8. Now() em propriedade de exibicao (3.11) ===")
acao={"OnSelect","OnVisible","OnTimerEnd","OnStart","OnChange","OnSuccess","OnScan","OnHidden"}
hits=[n for n,f in formulas if "Now()" in f and n.split(".")[-1] not in acao]
print("OK" if not hits else "ACHOU: "+str(hits))

print("\n=== 9. Hardcode de cor/tamanho (5.2) ===")
rgba=[n for n,f in formulas if re.search(r"\bRGBA\(", f)]
print("RGBA literal:", "OK" if not rgba else rgba)
colorval=[n for n,f in formulas if re.search(r"\bColorValue\(", f)]
print("ColorValue literal:", "OK" if not colorval else colorval)
cores_nom=[n for n,f in formulas if re.search(r"\bColor\.(?!Transparent\b)\w+", f)]
print("Color.<nome> (fora de Transparent):", "OK" if not cores_nom else cores_nom)

print("\n=== 11. Propriedade invalida em controle (PA2108) ===")
# [v2 · 01/09] Era so lista de PROIBIDAS por controle moderno, e por isso passou verde
# num YAML que o Studio recusou com 10 erros (AccessibleLabel em Classic/Button e
# Radius* em Rectangle). Agora e WHITELIST: o que nao esta na lista do tipo, acusa.
# [v3 · 03/09] OnChange acrescentado a Classic/TextInput, Classic/DropDown e
# Classic/ComboBox: a propriedade EXISTE nos tres (doc oficial) e a ausencia dela
# era falso positivo — nenhuma tela publicada ate aqui tinha usado.
COMUM = {"Height","Width","X","Y","Visible","Fill","Font","FontWeight","Size","Color","Text","Align"}
RAIO  = {"RadiusBottomLeft","RadiusBottomRight","RadiusTopLeft","RadiusTopRight"}
PAD   = {"PaddingBottom","PaddingLeft","PaddingRight","PaddingTop"}
CHEV  = {"ChevronBackground","ChevronFill","ChevronHoverBackground","ChevronHoverFill"}
SEL   = {"PressedColor","PressedFill","SelectionColor","SelectionFill"}
PERMITIDAS = {
 # Classic/Button NAO tem AccessibleLabel (o Text ja e o rotulo acessivel).
 "Classic/Button": COMUM|RAIO|{"BorderColor","BorderThickness","DisabledFill","DisabledBorderColor",
   "DisplayMode","HoverFill","HoverColor","HoverBorderColor","OnSelect","PressedFill","PressedColor",
   "PressedBorderColor",
   # [v5 · 22/10] Focused*: existem no Classic/Button (falso positivo do teste 11 no Painel)
   "FocusedBorderColor","FocusedBorderThickness"},
 # Rectangle NAO tem Radius*. Superficie com canto arredondado = Classic/Button DisplayMode.View.
 "Rectangle": {"Fill","Height","Width","X","Y","Visible","BorderColor","BorderThickness","OnSelect"},
 # [v4 · 02/10] VerticalAlign acrescentado: existe no Label classico e ja esta publicado
 # (scr_SelecaoGestao_1, lbl_Desc*) — a ausencia era falso positivo.
 "Label": COMUM|{"AccessibleLabel","BorderColor","BorderThickness","PaddingLeft","AutoHeight","Wrap",
   "Live","OnSelect","Tooltip","VerticalAlign"},
 "ModernText": COMUM|RAIO|PAD|{"VerticalAlign","BorderColor","BorderStyle","BorderThickness","AutoHeight"},
 "ModernButton": COMUM|RAIO|PAD|{"VerticalAlign","OnSelect","DisplayMode"},
 "Gallery": {"BorderColor","Fill","Height","Items","OnSelect","ShowScrollbar","TemplateFill",
   "TemplateSize","WrapCount","Width","X","Y","Default","DisplayMode","Visible","TemplatePadding"},
 "Timer": {"AutoStart","Duration","Fill","Font","Height","OnTimerEnd","Repeat","Start","Visible",
   "Width","X","Y","Text","Color","BorderColor","DisabledBorderColor","DisabledColor","DisabledFill",
   "HoverBorderColor","HoverColor","HoverFill","PressedBorderColor","PressedColor","PressedFill"},
 "Classic/DropDown": COMUM|CHEV|SEL|{"AccessibleLabel","BorderColor","Default","HoverFill","Items",
   "Items.Value","AllowEmptySelection","DisplayMode","OnChange"},
 "Classic/ComboBox": COMUM|CHEV|SEL|{"AccessibleLabel","BorderColor","DefaultSelectedItems",
   "DisplayFields","DisplayMode","HoverFill","InputTextPlaceholder","IsSearchable","Items",
   "SearchFields","SelectMultiple","OnChange"},
 "Classic/TextInput": COMUM|RAIO|{"AccessibleLabel","BorderColor","Default","DelayOutput","DisplayMode",
   "Format","HintText","HoverFill","HoverBorderColor","PaddingLeft","Mode","MaxLength","OnChange"},
 "Classic/Icon": {"AccessibleLabel","Color","Height","Icon","OnSelect","Width","X","Y","Visible",
   "BorderColor","DisplayMode","Tooltip","Rotation"},
 "GroupContainer": {"Fill","Height","Visible","Width","X","Y","LayoutMode","LayoutDirection"},
 "Spinner": {"Height","SpinnerSize","Visible","Width","X","Y"},
 "PenInput": {"Height","Width","X","Y","Visible","Color","Size","Fill","DisplayMode"},
 "Image": {"Height","Width","X","Y","Visible","Image","OnSelect","BorderColor","DisplayMode","Tooltip"},
 "HtmlViewer": COMUM|PAD|{"HtmlText","DisplayMode","AutoHeight"},
 "BarcodeReader": {"Height","Width","X","Y","Visible","OnScan","BarcodeType","Text","Font","Size"},
}
inval=[]
def walk_props(node, out):
    if isinstance(node, dict):
        for k,v in node.items():
            if isinstance(v, dict) and "Control" in v:
                tipo = v["Control"].split("@")[0]
                if tipo in PERMITIDAS:
                    for pk in (v.get("Properties") or {}):
                        if pk not in PERMITIDAS[tipo]:
                            out.append(f"{k}.{pk} ({v['Control']})")
                walk_props(v.get("Children"), out)
            else:
                walk_props(v, out)
    elif isinstance(node, list):
        for i in node: walk_props(i, out)
    return out
for sname, sbody in screens.items():
    walk_props(sbody.get("Children"), inval)
print("OK" if not inval else "FALHOU: "+str(inval))

print("\n=== 12. Nome de coluna como STRING em funcao de coluna (B 3.13) ===")
rx_col = r'(Ungroup|ShowColumns|RenameColumns|DropColumns|GroupBy)\s*\([^()]*"'
col_str = [n for n,f in formulas if re.search(rx_col, f)]
print("OK" if not col_str else "FALHOU: "+str(col_str))

print("\n=== 13. String de linha unica com ': ' (quebra o parse do import) ===")
risco=[]
for i,l in enumerate(raw.split("\n"),1):
    m=re.match(r'\s+(\w+): =(.*)$', l)
    if m and ": " in m.group(2): risco.append(f"linha {i}: {m.group(1)}")
print("OK" if not risco else "FALHOU: "+str(risco))

print("\n=== 14. Set() de global sem tipo definido ===")
rx_if1 = re.compile(r"Set\(\s*(var\w+)\s*,\s*If\(", re.S)
sem_tipo=[]
for n,f in formulas:
    for m in rx_if1.finditer(f):
        i=m.end(); prof=1; virg=0
        while i < len(f) and prof:
            c=f[i]
            if c=="(": prof+=1
            elif c==")": prof-=1
            elif c=="," and prof==1: virg+=1
            i+=1
        if virg < 2: sem_tipo.append(f"{n}: Set({m.group(1)}, If(...)) sem ramo else")
print("OK" if not sem_tipo else "FALHOU: "+str(sem_tipo))

print("\n=== 15. Global que recebe REGISTRO (colisao de tipo entre telas) ===")
rx_reg = re.compile(r"Set\(\s*(var\w+)\s*,\s*(LookUp|Patch|First|Last)\(|Set\(\s*(var\w+)\s*,\s*\w+\.Selected\b")
globais=set()
for n,f in formulas:
    for m in rx_reg.finditer(f):
        globais.add(m.group(1) or m.group(3))
print("Conferir manualmente contra as outras telas:", sorted(globais) if globais else "nenhuma")

print("\n=== 16. Formula sem '=' no inicio (PA1001 YamlInvalidSyntax) ===")
sem_igual=[n for n,f in formulas if not f.lstrip().startswith("=")]
print("OK" if not sem_igual else "FALHOU: "+str(sem_igual))

print("\n=== 17. IfError: tipo do valor x tipo do fallback (licao 2.23) ===")
# [v5 · 22/10] Olha TODOS os argumentos (valor e fallbacks), nao so o 1o. Tipo de cada ramo = ultimo
# comando apos o ultimo ';' de nivel 1: Collect/ClearCollect=Table, Patch=Record, Notify/true/false=Boolean.
# Dois ramos de tipo conhecido e diferente = FALHOU ("Expecting a Boolean/Table"). Ramo Collect/Patch
# contra ramo de tipo nao reconhecido = ALERTA. Solucao: fechar todos os ramos com "; true".
def tipo_ramo(t):
    u=ultimo_stmt(t)
    if re.match(r"(Clear)?Collect\(", u): return "Table"
    if re.match(r"Patch\(", u): return "Record"
    if re.match(r"Notify\(", u) or u in ("true","false"): return "Boolean"
    return None
ife_f=[]; ife_a=[]
for n,f in formulas:
    m=mascara(f)
    for mm in re.finditer(r"\bIfError\(", m):
        ags,_=args_de(m, mm.end())
        tps=[tipo_ramo(m[a:b]) for a,b in ags]
        conhec=set(t for t in tps if t)
        if len(conhec)>1: ife_f.append(f"{n}: ramos {sorted(conhec)}")
        elif conhec & {"Table","Record"} and any(t is None for t in tps): ife_a.append(n)
print("OK" if not ife_f else "FALHOU (fechar os ramos com '; true' ou usar If(IsError(...), Notify(...))): "+str(sorted(set(ife_f))))
if ife_a: print("ALERTA (ramo Collect/Patch contra ramo de tipo nao reconhecido, conferir):", sorted(set(ife_a)))

print("\n=== 18. fx_ usada na tela x definida no Formulas.txt ===")
if _dfx is None:
    print("ALERTA: Formulas.txt nao encontrado em", FORMULAS_TXT)
else:
    usadas=collections.defaultdict(set)
    for n,f in formulas:
        for x in re.findall(r"\b(fx_\w+)", mascara(f)): usadas[x].add(n)
    nao_def={k:sorted(v)[:3] for k,v in usadas.items() if k not in _dfx}
    print(("OK (%d fx_ usadas, todas definidas)" % len(usadas)) if not nao_def else "FALHOU: fx_ nao definida no Formulas.txt (ordem de colagem): "+str(nao_def))

print("\n=== 19. Size escrito a mao (alerta) ===")
tipo_de={n:c.split("@")[0] for n,c in ctrls}
TXT_T={"Label","ModernText","ModernButton","Classic/Button","Classic/TextInput","Classic/DropDown","Classic/ComboBox","HtmlViewer"}
size_hand=[n for n,f in formulas
           if n.split(".")[-1]=="Size" and tipo_de.get(n.rsplit(".",1)[0]) in TXT_T
           and re.match(r"=\s*\d+(\.\d+)?\s*$", f.strip()) and float(f.strip()[1:])!=0]
print("OK" if not size_hand else "ALERTA (usar fx_Fonte*): %d -> %s" % (len(size_hand), size_hand[:12]))

print("\n=== 20. Coalesce(x, 0) em Text / .Attachments fora de Form (alerta) ===")
coal=[]
for n,f in formulas:
    if n.split(".")[-1]!="Text": continue
    m=mascara(f)
    for mm in re.finditer(r"\bCoalesce\(", m):
        ags,_=args_de(m, mm.end())
        if ags and m[ags[-1][0]:ags[-1][1]].strip()=="0": coal.append(n); break
print("Coalesce(x, 0) em Text:", "OK" if not coal else "ALERTA (usar Blank()): "+str(coal))
forms={n for n,c in ctrls if c.startswith(("Form@","FormViewer@"))}
att=sorted({n for n,f in formulas for x in re.findall(r"([A-Za-zÀ-ÿ_]\w*)\.Attachments\b", mascara(f)) if x not in forms})
print(".Attachments fora de Form:", "OK" if not att else "ALERTA: "+str(att))

print("\n=== 10. Inventario ===")
print("Controles:", len(ctrls), "| Formulas:", len(formulas), "| Linhas:", raw.count("\n")+1)
_sai()
