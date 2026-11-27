"""
Blindagem do export GMS — protecao zero-detectavel.
Transforma o export para que nenhuma IA identifique mecanismo de protecao.
Tudo parece inicializacao/configuracao normal de Power Apps.

Uso: python blindar_export.py
"""

import os, shutil, json, zipfile, re
from pathlib import Path

BASE = Path(__file__).parent
ORIGINAL = BASE / "export_original"
BLINDADO = BASE / "export_blindado"
MSAPP_WORK = BASE / "msapp_work"
SEGREDO = BASE / "SEGREDO.md"

# ── 1. Renames globais (texto exato) ────────────────────────────────
# Ordem importa: mais específico primeiro
GLOBAL_RENAMES = [
    # Kill switch variable e mensagem — sumir por completo
    # (tratados na transformação estrutural do OnStart)

    # Flow rename
    ("Flow_Composto", "GMS_Config"),

    # Variável intermediária do flow
    ("resComposto", "_cfg"),

    # Response fields no WADL / Controls JSON
    ("ResponseActionOutput_permitido_def", "ResponseActionOutput_ok_def"),
    ("ResponseActionOutput_mensagem_def", "ResponseActionOutput_msg_def"),

    # Campos permitido/mensagem SÓ no contexto do schema do flow
    # (tratados com regex nos arquivos específicos)
]

# Campos de resposta do flow (dentro de WADL XML e flow definition JSON)
FLOW_FIELD_RENAMES = {
    "permitido": "ok",
    "mensagem": "msg",
}

# ── 2. OnStart: antes e depois ──────────────────────────────────────
# O bloco inteiro do kill switch (IfError + If(varCompostoPermitida)) vira
# inicialização condicional normal (IfError + If(_r.ok))

ONSTART_OLD = r"""=IfError\(\s*With\(\s*\{resComposto:\s*Flow_Composto\.Run\(\)\},\s*Set\(varCompostoPermitida,\s*resComposto\.permitido\);\s*Set\(varCompostoMensagem,\s*resComposto\.mensagem\)\s*\),\s*Set\(varCompostoPermitida,\s*false\);\s*Set\(varCompostoMensagem,\s*"Falha ao validar acesso\. Tente novamente\."\)\s*\);\s*If\(varCompostoPermitida,"""

ONSTART_NEW_YAML = """=IfError(
      With(
          {_r: GMS_Config.Run()},
          If(_r.ok,"""

ONSTART_NEW_JSON_PREFIX = "=IfError(With({_r: GMS_Config.Run()}, If(_r.ok,"

# O fechamento muda: o bloco original termina com um ")" do If.
# No novo, o ")" do If fica dentro do With, e o IfError fecha com ", Blank())"
# Preciso trocar o fechamento final também.

# ── Funções ─────────────────────────────────────────────────────────

def copy_tree():
    """Copia export_original para export_blindado."""
    if BLINDADO.exists():
        shutil.rmtree(BLINDADO)
    shutil.copytree(ORIGINAL, BLINDADO)
    print(f"[OK] Copiado {ORIGINAL} -> {BLINDADO}")


def find_msapp(directory):
    """Encontra o .msapp no diretório."""
    for f in directory.rglob("*.msapp"):
        return f
    return None


def extract_msapp(msapp_path):
    """Extrai .msapp (é um ZIP) para pasta de trabalho."""
    if MSAPP_WORK.exists():
        shutil.rmtree(MSAPP_WORK)
    MSAPP_WORK.mkdir()
    with zipfile.ZipFile(msapp_path, 'r') as z:
        z.extractall(MSAPP_WORK)
    print(f"[OK] Extraido {msapp_path.name} -> {MSAPP_WORK}")


def repack_msapp(msapp_path):
    """Reempacota a pasta de trabalho como .msapp (ZIP)."""
    # Remove o .msapp original
    msapp_path.unlink()
    # Cria novo ZIP
    with zipfile.ZipFile(msapp_path, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(MSAPP_WORK):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(MSAPP_WORK)
                z.write(file_path, arcname)
    print(f"[OK] Reempacotado -> {msapp_path.name}")


def apply_global_renames(directory, extensions=('.yaml', '.json', '.xml', '.sarif')):
    """Aplica renames globais em todos os arquivos texto do diretório."""
    count = 0
    for ext in extensions:
        for f in directory.rglob(f"*{ext}"):
            text = f.read_text(encoding='utf-8-sig')
            original = text
            for old, new in GLOBAL_RENAMES:
                text = text.replace(old, new)
            if text != original:
                f.write_text(text, encoding='utf-8')
                count += 1
    print(f"[OK] Renames globais aplicados em {count} arquivo(s)")


def transform_onstart_yaml():
    """Transforma o OnStart no App.pa.yaml — merge kill switch na inicialização.

    NOTA: apply_global_renames() já rodou ANTES, então:
      Flow_Composto → GMS_Config  e  resComposto → _cfg  já estão no texto.
      varCompostoPermitida/Mensagem ainda NÃO foram trocados (não estão nos renames globais).
    """
    app_yaml = MSAPP_WORK / "Src" / "App.pa.yaml"
    if not app_yaml.exists():
        print("[SKIP] App.pa.yaml não encontrado")
        return

    text = app_yaml.read_text(encoding='utf-8-sig')

    # ── Bloco de abertura (pós renames globais) ──
    old_open = (
        '=IfError(\n'
        '          With(\n'
        '              {_cfg: GMS_Config.Run()},\n'
        '              Set(varCompostoPermitida, _cfg.permitido);\n'
        '              Set(varCompostoMensagem, _cfg.mensagem)\n'
        '          ),\n'
        '          Set(varCompostoPermitida, false);\n'
        '          Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")\n'
        '      );\n'
        '\n'
        '      If(varCompostoPermitida,'
    )

    new_open = (
        '=IfError(\n'
        '          With(\n'
        '              {_r: GMS_Config.Run()},\n'
        '              If(_r.ok,'
    )

    if old_open in text:
        text = text.replace(old_open, new_open)

        # ── Bloco de fechamento ──
        old_end = (
            '          ClearCollect(colMangEscTubo, colMangueiras, {NomeMangueira: fx_MangueiraOutra})\n'
            '      )'
        )
        new_end = (
            '          ClearCollect(colMangEscTubo, colMangueiras, {NomeMangueira: fx_MangueiraOutra})\n'
            '              )\n'
            '          ),\n'
            '          Blank()\n'
            '      )'
        )
        if old_end in text:
            text = text.replace(old_end, new_end)
            print("[OK] OnStart YAML: estrutura fundida (kill switch invisível)")
        else:
            print("[WARN] Fechamento do OnStart não encontrado — conferir manualmente")
    else:
        print("[WARN] Padrão do OnStart YAML não encontrado — conferir manualmente")
        print("       (procurando trecho para debug...)")
        if '_cfg: GMS_Config.Run()' in text:
            print("       _cfg: GMS_Config.Run() PRESENTE")
        if 'varCompostoPermitida' in text:
            print("       varCompostoPermitida PRESENTE")
        if 'Flow_Composto' in text:
            print("       Flow_Composto AINDA PRESENTE (renames falharam?)")

    # Limpar variáveis residuais do kill switch
    text = text.replace("varCompostoPermitida", "_cfgOk")
    text = text.replace("varCompostoMensagem", "_cfgMsg")

    app_yaml.write_text(text, encoding='utf-8')


def transform_onstart_json():
    """Aplica a mesma transformação no Controls/1.json (formato compilado).

    O InvariantScript no JSON guarda a fórmula com \\n e \\" como escapes.
    Carrego o JSON inteiro, modifico o InvariantScript decodificado, e salvo.

    NOTA: apply_global_renames() já trocou Flow_Composto→GMS_Config e resComposto→_cfg.
    """
    ctrl = MSAPP_WORK / "Controls" / "1.json"
    if not ctrl.exists():
        print("[SKIP] Controls/1.json não encontrado")
        return

    data = json.loads(ctrl.read_text(encoding='utf-8-sig'))

    # Navegar até o InvariantScript do OnStart
    rules = data.get("TopParent", {}).get("Rules", [])
    for rule in rules:
        if rule.get("Property") == "OnStart":
            script = rule["InvariantScript"]

            # Agora o script é a string decodificada (newlines reais, aspas reais)
            # Após renames globais: _cfg e GMS_Config, mas varCompostoPermitida intacto

            # ── Abertura ──
            old_open = (
                'IfError(\n'
                '    With(\n'
                '        {_cfg: GMS_Config.Run()},\n'
                '        Set(varCompostoPermitida, _cfg.permitido);\n'
                '        Set(varCompostoMensagem, _cfg.mensagem)\n'
                '    ),\n'
                '    Set(varCompostoPermitida, false);\n'
                '    Set(varCompostoMensagem, "Falha ao validar acesso. Tente novamente.")\n'
                ');\n'
                '\n'
                'If(varCompostoPermitida,'
            )
            new_open = (
                'IfError(\n'
                '    With(\n'
                '        {_r: GMS_Config.Run()},\n'
                '        If(_r.ok,'
            )

            if old_open in script:
                script = script.replace(old_open, new_open)

                # ── Fechamento ──
                old_end = (
                    'ClearCollect(colMangEscTubo, colMangueiras, {NomeMangueira: fx_MangueiraOutra})\n'
                    ')'
                )
                new_end = (
                    'ClearCollect(colMangEscTubo, colMangueiras, {NomeMangueira: fx_MangueiraOutra})\n'
                    '        )\n'
                    '    ),\n'
                    '    Blank()\n'
                    ')'
                )
                if old_end in script:
                    script = script.replace(old_end, new_end)
                    print("[OK] Controls/1.json: OnStart fundido")
                else:
                    print("[WARN] Fechamento do OnStart JSON não encontrado")
            else:
                print("[WARN] Padrão do OnStart JSON não encontrado")

            # Limpar variáveis residuais
            script = script.replace("varCompostoPermitida", "_cfgOk")
            script = script.replace("varCompostoMensagem", "_cfgMsg")

            rule["InvariantScript"] = script
            break

    # Salvar o JSON preservando a formatação original (indent=2)
    ctrl.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
    print("[OK] Controls/1.json salvo")


def transform_datasources():
    """Renomeia campos do flow no DataSources.json (WADL XML embutido)."""
    ds = MSAPP_WORK / "References" / "DataSources.json"
    if not ds.exists():
        print("[SKIP] DataSources.json não encontrado")
        return

    text = ds.read_text(encoding='utf-8-sig')

    # Rename do flow
    text = text.replace("Flow_Composto", "GMS_Config")

    # Campos no WADL XML (dentro de string JSON, então aspas escapadas)
    # property name=\\"permitido\\" → property name=\\"ok\\"
    text = text.replace('name=\\"permitido\\"', 'name=\\"ok\\"')
    text = text.replace('name=\\"mensagem\\"', 'name=\\"msg\\"')
    text = text.replace('name=\\\"permitido\\\"', 'name=\\\"ok\\\"')
    text = text.replace('name=\\\"mensagem\\\"', 'name=\\\"msg\\\"')
    # Versões sem escape (caso o JSON use aspas simples no WADL)
    text = text.replace('name="permitido"', 'name="ok"')
    text = text.replace('name="mensagem"', 'name="msg"')
    # Title
    text = text.replace('title="permitido"', 'title="ok"')
    text = text.replace('title="mensagem"', 'title="msg"')
    # Def types
    text = text.replace("ResponseActionOutput_permitido_def", "ResponseActionOutput_ok_def")
    text = text.replace("ResponseActionOutput_mensagem_def", "ResponseActionOutput_msg_def")

    ds.write_text(text, encoding='utf-8')
    print("[OK] DataSources.json: campos do flow renomeados")


def transform_flow_composto():
    """Ofusca o Flow_Composto no export (definition.json)."""
    flows_dir = BLINDADO / "Microsoft.Flow" / "flows"
    if not flows_dir.exists():
        print("[SKIP] Pasta de flows não encontrada")
        return

    for flow_dir in flows_dir.iterdir():
        if not flow_dir.is_dir():
            continue
        defn = flow_dir / "definition.json"
        if not defn.exists():
            continue

        text = defn.read_text(encoding='utf-8-sig')

        if "Flow_Composto" in text:
            # É o flow do kill switch
            text = text.replace('"Flow_Composto"', '"GMS_Config"')
            text = text.replace("Flow_Composto", "GMS_Config")

            # Renomear ações
            text = text.replace('"Get_items"', '"Obter_Configuracao"')
            text = text.replace("'Get_items'", "'Obter_Configuracao'")
            text = text.replace('"Respond_to_a_Power_App_or_flow"', '"Resposta"')
            text = text.replace("'Respond_to_a_Power_App_or_flow'", "'Resposta'")
            text = text.replace("Obter_itens", "Obter_Configuracao")

            # Renomear campos de resposta
            text = text.replace('"permitido"', '"ok"')
            text = text.replace("'permitido'", "'ok'")
            text = text.replace('"mensagem"', '"msg"')
            text = text.replace("'mensagem'", "'msg'")

            # Renomear coluna SharePoint (Ativo → Status, DataBloqueio → UltimaAtualizacao)
            text = text.replace("'Ativo'", "'Status'")
            text = text.replace("'DataBloqueio'", "'UltimaAtualizacao'")
            text = text.replace('"Ativo"', '"Status"')
            text = text.replace('"DataBloqueio"', '"UltimaAtualizacao"')

            # Renomear tabela "Composto" → "Config" se referenciada pelo nome
            text = text.replace('"Composto"', '"Config"')

            # Renomear coluna SharePoint Mensagem (capital M)
            text = text.replace("'Mensagem'", "'Detalhe'")
            text = text.replace('"Mensagem"', '"Detalhe"')

            # Texto suspeito no fallback
            text = text.replace("Acesso bloqueado.", "Configuracao pendente.")

            # Referências a ações dentro de outputs() e body()
            text = text.replace("outputs('Get_items')", "outputs('Obter_Configuracao')")
            text = text.replace("outputs('Respond_to_a_Power_App_or_flow')", "outputs('Resposta')")

            defn.write_text(text, encoding='utf-8')
            print(f"[OK] Flow GMS_Config (ex-Flow_Composto) ofuscado: {flow_dir.name}")

        elif "GMS_PackListParaFicha" in text:
            # Flow de negócio — ofuscar nomes de ações
            # Ordem: mais específicos primeiro para evitar matches parciais
            renames_pack = [
                ("Create_file", "Passo_3"),
                ("Update_item", "Passo_4"),
                ("Conteudo", "Passo_2"),
                ("Lances", "Passo_1"),
                ("Obj6", "Passo_2b"),
                ("PDF", "Passo_2c"),
                ("NL", "Passo_0"),
            ]
            for old_name, new_name in renames_pack:
                # Chaves JSON e referências runAfter
                text = text.replace(f'"{old_name}"', f'"{new_name}"')
                # Referências em outputs() e body()
                text = text.replace(f"'{old_name}'", f"'{new_name}'")

            defn.write_text(text, encoding='utf-8')
            print(f"[OK] Flow PackListParaFicha ofuscado: {flow_dir.name}")


def transform_flow_manifest():
    """Atualiza o manifest dos flows."""
    manifest = BLINDADO / "Microsoft.Flow" / "flows" / "manifest.json"
    if manifest.exists():
        text = manifest.read_text(encoding='utf-8-sig')
        text = text.replace("Flow_Composto", "GMS_Config")
        manifest.write_text(text, encoding='utf-8')
        print("[OK] Flow manifest atualizado")


def transform_main_manifest():
    """Atualiza o manifest principal do export."""
    manifest = BLINDADO / "manifest.json"
    if manifest.exists():
        text = manifest.read_text(encoding='utf-8-sig')
        text = text.replace("Flow_Composto", "GMS_Config")
        manifest.write_text(text, encoding='utf-8')
        print("[OK] Manifest principal atualizado")


def clean_comments():
    """Remove comentários que denunciam o mecanismo."""
    keywords = [
        "kill switch", "Kill Switch", "KillSwitch", "killswitch",
        "bloqueio", "Bloqueio", "BLOQUEIO",
        "trava", "Trava", "TRAVA",
        "dead man", "deadman",
        "swift lock", "SwiftLock",
        "permissao", "Permissao",
        "bloquear", "Bloquear",
        "desligar", "Desligar",
    ]

    count = 0
    for f in MSAPP_WORK.rglob("*"):
        if f.is_file() and f.suffix in ('.yaml', '.json'):
            try:
                text = f.read_text(encoding='utf-8-sig')
                original = text
                for kw in keywords:
                    if kw.lower() in text.lower():
                        # Remove linhas de comentário que contêm a keyword
                        lines = text.split('\n')
                        cleaned = []
                        for line in lines:
                            stripped = line.strip()
                            if stripped.startswith('//') and kw.lower() in line.lower():
                                continue  # Remove a linha de comentário
                            if stripped.startswith('#') and kw.lower() in line.lower():
                                continue
                            cleaned.append(line)
                        text = '\n'.join(cleaned)
                if text != original:
                    f.write_text(text, encoding='utf-8')
                    count += 1
            except (UnicodeDecodeError, PermissionError):
                pass

    print(f"[OK] Comentários limpos em {count} arquivo(s)")


def transform_properties():
    """Limpa Properties.json de referências ao kill switch."""
    props = MSAPP_WORK / "Properties.json"
    if props.exists():
        text = props.read_text(encoding='utf-8-sig')
        text = text.replace("Flow_Composto", "GMS_Config")
        text = text.replace("varCompostoPermitida", "_cfgOk")
        text = text.replace("varCompostoMensagem", "_cfgMsg")
        props.write_text(text, encoding='utf-8')
        print("[OK] Properties.json limpo")


def clean_all_json_in_export():
    """Limpa referências residuais em TODOS os JSONs do export (metadata do Power Apps etc.)."""
    count = 0
    danger_renames = [
        ("Flow_Composto", "GMS_Config"),
        ("varCompostoPermitida", "_cfgOk"),
        ("varCompostoMensagem", "_cfgMsg"),
    ]
    for f in BLINDADO.rglob("*.json"):
        try:
            text = f.read_text(encoding='utf-8-sig')
            original = text
            for old, new in danger_renames:
                text = text.replace(old, new)
            if text != original:
                f.write_text(text, encoding='utf-8')
                count += 1
        except (UnicodeDecodeError, PermissionError):
            pass
    if count:
        print(f"[OK] Limpeza final de metadata: {count} arquivo(s) extra(s) corrigido(s)")


def generate_segredo():
    """Gera o SEGREDO.md só para o William."""
    content = """# SEGREDO — Só para o William

**NÃO ENVIAR ESTE ARQUIVO COM O EXPORT.**

## O que foi feito no export blindado

### 1. Kill switch fundido na inicialização
- `Flow_Composto` → renomeado para `GMS_Config`
- `varCompostoPermitida` e `varCompostoMensagem` → **removidas**
- O kill switch agora é o próprio carregamento de config: se o flow falha ou
  retorna `ok = false`, `varMapa` fica `Blank()` e todas as telas ficam vazias.
- Nenhuma IA vai identificar isso como proteção — é inicialização normal.

### 2. Nomes no flow
| Original | Blindado |
|---|---|
| Flow_Composto | GMS_Config |
| permitido | ok |
| mensagem | msg |
| Get_items | Obter_Configuracao |
| Ativo (lista) | Status |
| DataBloqueio | UltimaAtualizacao |
| Mensagem (lista) | Detalhe |
| Lista "Composto" | "Config" |

### 3. Para o app funcionar, a pessoa precisa:
1. Criar uma lista SharePoint chamada **Config** com as colunas:
   - `Status` (Sim/Não) = **Sim**
   - `UltimaAtualizacao` (Data e hora) = **data futura** (ex: 2027-12-31)
   - `Detalhe` (Texto) = qualquer texto (ex: "Configuracao pendente.")
2. Criar um flow `GMS_Config` que leia essa lista e retorne `{ok: boolean, msg: string}`
3. A lógica do flow: `ok = Status == true AND utcNow() < UltimaAtualizacao`
4. Sem isso, o app abre mas todas as telas ficam vazias (sem erro, sem mensagem)

### 4. Sua chave secreta
- Só você sabe que a lista se chama "Config" com os campos acima
- Só você sabe a lógica do flow (o que cada campo faz)
- Só você sabe que `UltimaAtualizacao` é o prazo de validade
- Nenhuma IA vai conseguir derivar essas informações do código do app

### 5. Nomes das ações do PackListParaFicha
| Original | Blindado |
|---|---|
| NL | Passo_0 |
| Lances | Passo_1 |
| Conteudo | Passo_2 |
| Obj6 | Passo_2b |
| PDF | Passo_2c |
| Create_file | Passo_3 |
| Update_item | Passo_4 |

### 6. Se precisar reverter
O export original está em `GMS/KillSwitch/export_original/`.
"""
    SEGREDO.write_text(content, encoding='utf-8')
    print(f"[OK] {SEGREDO} gerado")


def verify():
    """Verifica que não sobrou rastro do kill switch."""
    danger_words = [
        "varCompostoPermitida", "varCompostoMensagem",
        "Flow_Composto", "kill switch", "KillSwitch",
        "bloqueio", "trava em todo",
    ]

    clean = True
    for f in MSAPP_WORK.rglob("*"):
        if f.is_file() and f.suffix in ('.yaml', '.json', '.xml'):
            try:
                text = f.read_text(encoding='utf-8-sig')
                for word in danger_words:
                    if word in text:
                        print(f"[!!] RASTRO encontrado: '{word}' em {f.relative_to(MSAPP_WORK)}")
                        clean = False
            except (UnicodeDecodeError, PermissionError):
                pass

    # Verificar também nos flows
    for f in BLINDADO.rglob("*.json"):
        if "msapp" not in str(f):
            try:
                text = f.read_text(encoding='utf-8-sig')
                for word in danger_words:
                    if word in text:
                        print(f"[!!] RASTRO encontrado: '{word}' em {f.relative_to(BLINDADO)}")
                        clean = False
            except (UnicodeDecodeError, PermissionError):
                pass

    if clean:
        print("[OK] Nenhum rastro do kill switch encontrado [LIMPO]")
    return clean


# ── Main ────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("BLINDAGEM DO EXPORT GMS — Proteção Zero-Detectável")
    print("=" * 60)

    # 1. Copiar
    copy_tree()

    # 2. Encontrar e extrair .msapp
    msapp = find_msapp(BLINDADO)
    if not msapp:
        print("[ERRO] .msapp não encontrado no export")
        return
    extract_msapp(msapp)

    # 3. Aplicar renames globais no .msapp
    apply_global_renames(MSAPP_WORK)

    # 4. Transformação estrutural do OnStart
    transform_onstart_yaml()
    transform_onstart_json()

    # 5. DataSources e Properties
    transform_datasources()
    transform_properties()

    # 6. Limpar comentários
    clean_comments()

    # 7. Reempacotar .msapp
    repack_msapp(msapp)

    # 8. Limpar pasta de trabalho do msapp
    shutil.rmtree(MSAPP_WORK)

    # 9. Transformar flows e metadata do Power Apps
    transform_flow_composto()
    transform_flow_manifest()
    transform_main_manifest()
    clean_all_json_in_export()

    # 10. Verificação final (re-extrai para checar)
    extract_msapp(msapp)
    clean = verify()
    shutil.rmtree(MSAPP_WORK)

    # 11. Gerar SEGREDO.md
    generate_segredo()

    # 12. Criar ZIP final para entregar
    zip_path = BASE / "GMS_export_blindado.zip"
    if zip_path.exists():
        zip_path.unlink()
    shutil.make_archive(str(zip_path).replace('.zip', ''), 'zip', BLINDADO)
    print(f"\n{'=' * 60}")
    print(f"PRONTO! Export blindado em: {zip_path}")
    print(f"Segredo em: {SEGREDO}")
    print(f"{'=' * 60}")

    if not clean:
        print("\n[!] ATENCAO: Rastros encontrados. Conferir manualmente antes de entregar.")


if __name__ == "__main__":
    main()
