import yaml, re, sys, collections
# Power Apps usa "= " sozinho (propriedade vazia); PyYAML trata como tag :value
yaml.SafeLoader.add_constructor('tag:yaml.org,2002:value', lambda l,n: "=")

path = sys.argv[1]
raw = open(path, encoding="utf-8").read()

print("=== 1. PARSE PyYAML ===")
try:
    doc = yaml.safe_load(raw)
    print("OK")
except Exception as e:
    print("FALHOU:", e); sys.exit(1)

VERSOES_OK = {
 "Classic/Button":"2.2.0","Classic/TextInput":"2.3.2","Classic/DropDown":"2.3.1",
 "Classic/ComboBox":"2.4.0","Classic/Icon":"2.5.0","Classic/DatePicker":"2.6.0",
 "Label":"2.5.1","Rectangle":"2.3.0","GroupContainer":"1.5.0","Gallery":"2.15.0",
 "Timer":"2.1.0","Image":"2.2.3","Spinner":"1.4.6","HtmlViewer":"2.1.0",
 "ModernText":"1.0.0","ModernIcon":"1.1.1","BarcodeReader":"1.0.25",
 "Form":"2.4.4","FormViewer":"2.3.4","TypedDataCard":"1.0.7","ModernButton":"1.0.0",
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

screens = doc["Screens"]
for sname, sbody in screens.items():
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
          "cmb_","inp_","spr_","html_","dc_","bcr_","chk_","tgl_","dte_","img_","cmp_")
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
conhecidos=set(nomes)|{"Parent","Self","ThisItem","App","ThisRecord"}
refs=set()
for n,f in formulas:
    for m in re.finditer(r"\b([A-Za-zÀ-ÿ_][A-Za-zÀ-ÿ0-9_]*)\.(Text|Selected|SelectedDate|Value|X|Y|Width|Height|Fill|Visible|DisplayMode|Barcodes|AllItems)\b", f):
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
   "PressedBorderColor"},
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

print("\n=== 10. Inventario ===")
print("Controles:", len(ctrls), "| Formulas:", len(formulas), "| Linhas:", raw.count("\n")+1)
