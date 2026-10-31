# IA da manufatura, grátis e local: guia para testar na terça

Pesquisa de 31/10/2026, feita pelo chefe a pedido do William. Objetivo: uma IA que responda sobre a manufatura com base nos dados do GMS, **sem Copilot Studio e sem custo**.

## A decisão (uma só)

Rodar tudo **no próprio PC corporativo**: modelo de linguagem local (Ollama) + banco local (DuckDB) + um script Python que transforma a pergunta em consulta SQL, roda a consulta e responde em português.

Por que esse caminho:
- **Grátis**: Ollama, DuckDB, Python e os modelos (Qwen3, Phi-4-mini) são abertos e sem licença paga.
- **O dado não sai do PC**: nada vai para a nuvem (nem ChatGPT, Gemini ou Copilot). Isso cumpre a regra de não mandar dado de produção ou SAP para serviço externo.
- **Não precisa de administrador**: o instalador do Ollama para Windows roda sem direito de admin e instala na pasta do usuário (`%LOCALAPPDATA%\Programs\Ollama`; os modelos ficam em `%HOMEPATH%\.ollama`).
- **Número certo**: a IA não "lembra" número. Ela escreve o SQL, o DuckDB calcula, e ela só explica o resultado. Isso evita a IA inventar produção, refugo ou parada.

O limite honesto: num PC sem placa de vídeo, a resposta leva de 20 s a 2 min. Serve para teste e para perguntas de supervisão, não para o chão de fábrica em tempo real.

## Qual tipo de IA serve para qual pergunta

Você falou em generativa, por reforço e outras. Este é o mapa, com o que vale testar agora e o que fica para depois.

| Tipo de IA | Pergunta que ela responde | Ferramenta grátis | Quando |
|---|---|---|---|
| **Generativa + SQL** (texto para consulta) | "Quanto a TH07 produziu no 2º turno ontem?", "Qual mangueira teve mais refugo em outubro?" | Ollama + DuckDB + script abaixo | **Terça** |
| **Generativa + documentos** (RAG) | "O que o Mestre diz sobre setup?", "Qual a regra de turno?", "Como trocar a peça X da trançadeira?" | AnythingLLM Desktop ou Open WebUI ligado ao Ollama | Terça, se sobrar tempo |
| **Aprendizado de máquina clássico** (supervisionado) | "Qual OP tem mais chance de dar refugo?", "Que fator mais explica a parada?" | Python: scikit-learn ou LightGBM + SHAP (mostra o peso de cada fator) | Depois, com histórico limpo |
| **Séries temporais** (previsão e anomalia) | "A TH07 está fora do normal hoje?", "Quanto vamos produzir na semana?" | Modelos abertos Chronos-2 ou TimesFM; ou só estatística (média móvel, desvio) | Depois, com dado de sensor |
| **Otimização** (pesquisa operacional) | "Qual a melhor sequência de OPs para reduzir setup?" | Google OR-Tools (CP-SAT), grátis | Antes de pensar em reforço |
| **Aprendizado por reforço** | O mesmo da linha acima, quando a fábrica muda o tempo todo (quebra, urgência) | Gymnasium + Stable-Baselines3 (PPO) | Só com simulador da célula pronto; não é coisa de terça |
| **Causal** | "Se eu mudar a velocidade, o refugo cai?" (causa, não só correlação) | DoWhy (Python) | Depois |

Sobre reforço: a literatura recente (2025 e 2026) mostra que quase todo estudo de programação da produção por reforço roda em simulação; casos em fábrica real ainda são poucos e exigem um simulador da linha com tempo de setup e quebra. Para o GMS, o caminho que dá resultado mais rápido é: primeiro OR-Tools (otimização com regra fixa), depois reforço só se a otimização não aguentar a variação do dia a dia.

## Antes de terça: o que conferir no PC da empresa

1. **Memória**: Configurações > Sistema > Sobre. Com 16 GB de RAM, use `qwen3:8b`. Com 8 GB, use `qwen3:4b` ou `phi4-mini`.
2. **Política de TI**: veja se instalar programa na pasta do usuário é permitido. Se não for, não force; peça à TI. O Ollama baixa os modelos da internet (de 2,5 a 5 GB), então o proxy pode bloquear.
3. **Python**: veja se já tem (`python --version`). Se não tiver, a versão "embeddable" do python.org roda sem instalar.

## Passo a passo na terça (cerca de 1 hora)

**1. Instalar o Ollama e baixar o modelo**

```bash
ollama pull qwen3:8b
```

Teste: `ollama run qwen3:8b "diga oi em uma frase"`.

**2. Instalar o DuckDB no Python**

```bash
pip install duckdb
```

**3. Separar os dados**

Crie uma pasta `dados` e coloque 2 ou 3 listas do GMS exportadas do SharePoint em CSV (na lista: Exportar > Exportar para CSV). Comece pelas que você mais pergunta (ex.: fichas de OP, eventos de parada, refugo). Dê nomes simples aos arquivos: `fichas.csv`, `paradas.csv`, `refugo.csv`.

**4. Escrever o glossário** (é o que mais melhora a resposta)

Crie `dados/glossario.md` com o significado das colunas e das regras, em frases curtas. Exemplo de conteúdo (sem dado real):

```
- Turno: 1º 05:20 às 13:57; 2º a partir de 13:57 (hora extra até 23:20); 3º 22:20 às 05:20. O dia produtivo começa às 05:20.
- Parada real (célula sem produzir) nunca soma com tempo excedido.
- Coluna Etapa: Mandril, Tubo, Trancagem, Cobertura, Bandagem, Vulcanizacao, Debandagem, Extracao.
- Status Cancelado não conta como produção.
- Metragem em metros; refugo em metros.
```

Confira os horários e as regras no `GMS_Mestre.md` antes de usar.

**5. Rodar o script** (código no fim deste guia, salve como `gms_pergunta.py` ao lado da pasta `dados`)

```bash
python gms_pergunta.py dados
```

Ele mostra o SQL que gerou antes de responder. Assim você confere se a conta está certa.

**6. Medir se presta** (sem isso não dá para confiar)

Escreva 20 perguntas cuja resposta você já sabe pelo Power BI. Rode as 20 e anote quantas acertou. Abaixo de 15 de 20: melhore o glossário (é quase sempre ali o erro) e rode de novo. Só mostre à supervisão depois de passar de 17 de 20.

## Para perguntas sobre documentos (opcional na terça)

Instale o **AnythingLLM Desktop** (grátis, roda local), escolha o Ollama como motor, crie um espaço "GMS" e solte lá o `GMS_Mestre.md`, o `GMS_Licoes.md` e os manuais das máquinas. Ele responde citando o trecho do documento. Não coloque planilha de produção ali: para número, use o script de SQL.

## Alternativa grátis sem instalar nada

O **Q&A do Power BI Desktop** (visual "Perguntas e respostas") aceita pergunta em texto sobre o modelo que você já tem, sem Copilot e sem licença extra. É limitado (inglês funciona melhor e não explica o porquê), mas roda em minutos no `.pbix` do GMS.

## Riscos e cuidados

- **Nada de serviço externo** com dado do GMS ou do SAP: nem ChatGPT, Gemini ou site de "chat com seu CSV".
- O script só aceita consulta de leitura (SELECT). Ele não grava nem apaga nada, e trabalha numa cópia em CSV, não no SharePoint.
- A resposta é tão boa quanto o dado. Se a lista tem lacuna (dias em que o GMS ficou fora do ar), a IA vai responder com a lacuna.
- Modelo pequeno erra em pergunta com muitas tabelas. Comece com uma tabela por pergunta.

## Script `gms_pergunta.py`

Usa só Python, `duckdb` e o Ollama local. Nada sai do PC.

```python
# gms_pergunta.py - pergunte em portugues aos CSVs do GMS. Tudo local (Ollama + DuckDB).
# Uso: python gms_pergunta.py dados      (modelo: set GMS_MODELO=qwen3:4b para trocar)
import glob, json, os, re, sys, urllib.request
import duckdb

PASTA = sys.argv[1] if len(sys.argv) > 1 else "dados"
MODELO = os.environ.get("GMS_MODELO", "qwen3:8b")
URL = "http://localhost:11434/api/chat"
PROIBIDO = re.compile(r"\b(insert|update|delete|drop|create|alter|copy|attach|detach|install|load|export|pragma|set|call)\b", re.I)

con = duckdb.connect()
tabelas = []
for arq in sorted(glob.glob(os.path.join(PASTA, "*.csv"))):
    nome = re.sub(r"\W+", "_", os.path.splitext(os.path.basename(arq))[0]).lower()
    caminho = os.path.abspath(arq).replace("\\", "/").replace("'", "''")
    con.execute(f"CREATE VIEW {nome} AS SELECT * FROM read_csv_auto('{caminho}', header=true)")
    tabelas.append(nome)
if not tabelas:
    sys.exit(f"Nenhum CSV em {PASTA}")

def esquema():
    partes = []
    for t in tabelas:
        cols = con.execute(f"DESCRIBE {t}").fetchall()
        exemplo = con.execute(f"SELECT * FROM {t} LIMIT 3").fetchall()
        partes.append(f"Tabela {t}: " + ", ".join(f'"{c[0]}" {c[1]}' for c in cols)
                      + f"\n  exemplo de linhas: {exemplo}")
    return "\n".join(partes)

glossario = ""
g = os.path.join(PASTA, "glossario.md")
if os.path.exists(g):
    glossario = open(g, encoding="utf-8").read()

def chat(mensagens):
    corpo = json.dumps({"model": MODELO, "messages": mensagens, "stream": False,
                        "think": False, "options": {"temperature": 0}}).encode()
    req = urllib.request.Request(URL, corpo, {"Content-Type": "application/json"})
    texto = json.loads(urllib.request.urlopen(req, timeout=900).read())["message"]["content"]
    return re.sub(r"<think>.*?</think>", "", texto, flags=re.S).strip()

def extrai_sql(texto):
    m = re.search(r"```(?:sql)?\s*(.*?)```", texto, re.S | re.I)
    sql = (m.group(1) if m else texto).strip().rstrip(";")
    if ";" in sql or not re.match(r"(select|with)\b", sql, re.I) or PROIBIDO.search(sql):
        raise ValueError("so aceito uma consulta SELECT de leitura")
    return sql

SISTEMA = ("Voce escreve UMA consulta SQL do DuckDB que responde a pergunta. Use so as tabelas e colunas abaixo, "
           "com nomes de coluna entre aspas duplas. Responda so com o SQL dentro de ```sql```.\n\n"
           f"{esquema()}\n\nGlossario da fabrica:\n{glossario}")

print(f"Modelo {MODELO}. Tabelas: {', '.join(tabelas)}. Linha vazia para sair.")
while True:
    pergunta = input("\nPergunta: ").strip()
    if not pergunta:
        break
    msgs = [{"role": "system", "content": SISTEMA}, {"role": "user", "content": pergunta}]
    for tentativa in range(2):
        try:
            sql = extrai_sql(chat(msgs))
            print(f"\nSQL:\n{sql}")
            cur = con.execute(sql)
            colunas = [d[0] for d in cur.description]
            linhas = cur.fetchmany(200)
            break
        except Exception as e:
            print(f"(erro: {e})")
            msgs += [{"role": "assistant", "content": locals().get("sql", "")},
                     {"role": "user", "content": f"Deu erro: {e}. Corrija e mande so o SQL."}]
    else:
        print("Nao consegui montar a consulta. Reescreva a pergunta ou melhore o glossario.")
        continue
    resultado = "\n".join([" | ".join(colunas)] + [" | ".join(map(str, l)) for l in linhas])
    print(f"\nResultado ({len(linhas)} linhas):\n{resultado[:2000]}")
    resposta = chat([{"role": "user", "content":
        f"Pergunta: {pergunta}\nSQL usado: {sql}\nResultado:\n{resultado[:6000]}\n\n"
        "Responda em portugues, curto, usando SO os numeros do resultado. Se o resultado estiver vazio, diga isso."}])
    print(f"\nResposta: {resposta}")
```

## Próximos passos depois de terça

1. Se acertar mais de 17 de 20: agendar a exportação das listas em CSV (Power Automate já existe no GMS) para os dados ficarem do dia.
2. Juntar o RAG dos documentos e o SQL num lugar só (Open WebUI com uma ferramenta que chama o script).
3. Primeiro modelo de aprendizado de máquina: prever refugo por OP com LightGBM + SHAP, usando o histórico do Refugo PPM que já está no BI.
4. Otimização de sequência de OPs com OR-Tools, usando a tabela de setup.

## Fontes

- [Ollama no Windows (instalação sem admin)](https://docs.ollama.com/windows)
- [Melhores modelos locais só com CPU em 2026](https://www.popularai.org/p/best-cpu-only-local-llm-2026)
- [Modelos locais por memória (8 a 128 GB)](https://llmhardware.io/guides/best-llms-to-run-locally)
- [Modelo local para notebook com 16 GB](https://www.promptquorum.com/prompt-bites/best-local-llm-16gb-ram-laptop)
- [DuckDB e texto para SQL com modelo local](https://motherduck.com/blog/duckdb-text2sql-llm/)
- [Agente de dados local com DuckDB (PyCon DE 2026)](https://pretalx.com/pyconde-pydata-2026/talk/AF9DNH/)
- [Lições práticas de RAG e texto para SQL](https://rajivshah.com/blog/practical-rag-text-to-sql.html)
- [Copiloto no MES (Critical Manufacturing)](https://www.criticalmanufacturing.com/blog/the-rise-of-copilots-transforming-the-interaction-with-manufacturing-execution-systems-mes/)
- [Agentes de IA no MES](https://www.iiot-world.com/smart-manufacturing/ai-agents-mes-beyond-chatbot/)
- [Reforço em programação da produção num cenário industrial de pintura (2026)](https://arxiv.org/abs/2608.14122)
- [Reforço com restrições práticas em produção real (FAIM 2025)](https://link.springer.com/chapter/10.1007/978-3-032-05610-8_2)
- [Revisão: reforço em despacho de semicondutores, validação e implantação](https://www.tandfonline.com/doi/full/10.1080/21693277.2025.2582472)
- [LineFlow: controle de linhas de produção por reforço](https://arxiv.org/pdf/2505.06744)
- [Modelos de base para séries temporais em manutenção preditiva](https://www.tigerdata.com/learn/foundation-models-predictive-maintenance)
- [Embeddings de séries temporais para vida útil restante (2026)](https://arxiv.org/pdf/2606.11990)
- [Da OEE à causa raiz com IA](https://tdengine.com/how-ai-helps-engineers-move-from-oee-monitoring-to-root-cause-analysis/)
