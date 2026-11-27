# levar_pagina_oficial.py: leva a página pg_inventario_processo da cópia de teste para o GMS_Painel oficial (MEL-278).
# Só acrescenta: a página (com a moldura do menu copiada da pg_plano_mangueira), o botão "Inventário em processo"
# no menu de todas as páginas (y 594, logo abaixo do Plano de mangueira), as 5 medidas "IP · SVG" e a página no pages.json.
# Não mexe em posição nem formato de nada que já existe. Recusa rodar se a página já existir (ajustes do William).
# Uso: python -I -X utf8 levar_pagina_oficial.py
import copy, json, os, shutil, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
PBI = os.path.join(AQUI, "..", "..", "PowerBI")
TESTE = os.path.join(PBI, "Painel_PBIP_teste", "GMS_Painel.Report", "definition")
OFIC = os.path.join(PBI, "GMS_Painel.Report", "definition")
PAGES = os.path.join(OFIC, "pages")
NOME = "pg_inventario_processo"
NOVA = os.path.join(PAGES, NOME)
MOLDE = os.path.join(PAGES, "pg_plano_mangueira")
MOLDURA = ("sub_", "txt_secao", "nav_barra_ativa", "faixa", "logo", "txt_app", "atualizado")
Y_BOTAO = 594
FORA_DO_TESTE = {"nav", "atualizado"}  # navegador de páginas e rodapé do teste dão lugar à moldura oficial


def ler(p):
    return json.load(open(p, encoding="utf-8"))


def gravar(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(json.dumps(d, ensure_ascii=False, indent=2))


def botao(modelo, destino_nome, y):
    b = copy.deepcopy(modelo)
    b["name"] = "sub_inventario_processo"
    b["position"]["y"] = y
    b["position"]["z"] = b["position"]["tabOrder"] = 19100
    for t in b["visual"]["objects"]["text"]:
        if "text" in t.get("properties", {}):
            t["properties"]["text"] = {"expr": {"Literal": {"Value": "'Inventário em processo'"}}}
    for l in b["visual"].get("visualContainerObjects", {}).get("visualLink", []):
        if "navigationSection" in l.get("properties", {}):
            l["properties"]["navigationSection"] = {"expr": {"Literal": {"Value": "'%s'" % destino_nome}}}
    vco = b["visual"].get("visualContainerObjects", {})
    for k in ("title", "visualTooltip"):
        for t in vco.get(k, []):
            for pk in ("text", "titleText"):
                if pk in t.get("properties", {}):
                    t["properties"][pk] = {"expr": {"Literal": {"Value": "'Inventário em processo'"}}}
    return b


def main():
    if os.path.isdir(NOVA):
        sys.exit("A página já existe no oficial (pode ter ajustes do William). Edite direto.")
    paginas = ler(os.path.join(PAGES, "pages.json"))
    ativo = ler(os.path.join(MOLDE, "visuals", "sub_plano_mangueira", "visual.json"))  # estilo de botão ativo
    inativo = ler(os.path.join(PAGES, "pg_visao_geral", "visuals", "sub_plano_mangueira", "visual.json"))

    # 1) página nova: page.json do molde + moldura + conteúdo do teste encaixado à direita do menu
    os.makedirs(os.path.join(NOVA, "visuals"))
    pg = ler(os.path.join(MOLDE, "page.json"))
    pg["name"], pg["displayName"] = NOME, "Inventário em processo"
    pg.pop("visibility", None)
    gravar(os.path.join(NOVA, "page.json"), pg)
    for v in os.listdir(os.path.join(MOLDE, "visuals")):
        if v.startswith(MOLDURA):
            shutil.copytree(os.path.join(MOLDE, "visuals", v), os.path.join(NOVA, "visuals", v))
    gravar(os.path.join(NOVA, "visuals", "sub_plano_mangueira", "visual.json"), inativo)  # aqui o plano não é a página ativa
    gravar(os.path.join(NOVA, "visuals", "sub_inventario_processo", "visual.json"), botao(ativo, NOME, Y_BOTAO))
    barra = ler(os.path.join(NOVA, "visuals", "nav_barra_ativa", "visual.json"))
    barra["position"]["y"] = Y_BOTAO
    gravar(os.path.join(NOVA, "visuals", "nav_barra_ativa", "visual.json"), barra)

    fx = 1048 / 1248  # teste: x 16..1264; oficial: x 216..1264
    for v in os.listdir(os.path.join(TESTE, "pages", NOME, "visuals")):
        if v in FORA_DO_TESTE:
            continue
        d = ler(os.path.join(TESTE, "pages", NOME, "visuals", v, "visual.json"))
        p = d["position"]
        p["x"] = round(216 + (p["x"] - 16) * fx, 1)
        p["width"] = round(p["width"] * fx, 1)
        if v == "titulo":
            p["x"], p["y"] = 216, 8
        if v == "t_ops":
            p["height"] = 712 - p["y"]  # usa o espaço do rodapé que saiu
        gravar(os.path.join(NOVA, "visuals", v, "visual.json"), d)

    # 2) botão no menu de todas as outras páginas (inativo)
    for nome in paginas["pageOrder"]:
        pasta = os.path.join(PAGES, nome, "visuals")
        if nome == NOME or not os.path.isdir(os.path.join(pasta, "sub_plano_mangueira")):
            continue
        gravar(os.path.join(pasta, "sub_inventario_processo", "visual.json"), botao(inativo, NOME, Y_BOTAO))

    # 3) medidas SVG do relatório
    pe = os.path.join(OFIC, "reportExtensions.json")
    of, te = ler(pe), ler(os.path.join(TESTE, "reportExtensions.json"))
    tem = {m["name"] for m in of["entities"][0]["measures"]}
    novas = [m for m in te["entities"][0]["measures"] if m["name"].startswith("IP · SVG") and m["name"] not in tem]
    of["entities"][0]["measures"].extend(novas)
    gravar(pe, of)

    # 4) pages.json: só acrescenta a página no fim
    paginas["pageOrder"].append(NOME)
    gravar(os.path.join(PAGES, "pages.json"), paginas)
    print("ok:", len(novas), "medidas SVG;", sorted(os.listdir(os.path.join(NOVA, "visuals"))))


if __name__ == "__main__":
    main()
