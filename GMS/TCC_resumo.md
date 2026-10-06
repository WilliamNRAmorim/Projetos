# GMS como TCC: o essencial

Documento completo (Google Docs): [Preparacao_Qualificacao_GMS](https://docs.google.com/document/d/11Rhh8ZvfefE0LPPI5nm26XXGOgWeqO2dtqiW8WR3iFU/edit)

- **O que é:** implantação de um MES (sistema de execução da manufatura) feito 100% em low-code, numa multinacional de soluções hidráulicas no interior de SP. É estudo de caso aplicado.
- **Tese:** "O GMS não substituiu uma folha de papel. Substituiu a forma como a célula acessa informação sobre si mesma." Versão curta: **"Não criamos o dado. Zeramos o custo de acessá-lo."**
- **Problema:** ficha física em 8 etapas, transcrita no turno seguinte pro Excel e depois pro SAP. A informação chegava com 1 a 2 dias de atraso ("cegueira operacional"), não havia como calcular OEE, e achar uma OP fechada podia custar uma manhã.
- **Solução, em 4 camadas:** Power Apps (coleta) → Microsoft Lists (dados) → Power Automate (orquestração) → Power BI (análise). Low-code foi **restrição, não preferência**: era o que a governança de TI permitia.
- **Método:** Gemba Walk (2 semanas nos 3 turnos) e RAD com ciclo diário (de manhã observando na estação, à tarde desenvolvendo, versão nova no turno seguinte).
- **Aderência ao MESA-11:** 6 funções implementadas, 1 em expansão, 2 parciais e 2 fora do escopo.
- **Linha do tempo (pelo TCC):** começou em ago/2025, primeiras telas em out/2025, 3 meses de validação papel × digital. **9 meses no total: 2 de desenvolvimento e 7 de implantação.** **Fonte oficial: o TCC** (o vídeo longo e o texto do LinkedIn já foram corrigidos de "8 meses").
- **Lição mais forte:** a barreira foi a adoção, não a técnica (Atkin et al., 2017).

## Regras pra conteúdo público
- Os dados quantitativos da empresa são confidenciais (o próprio TCC declara isso).
- O dado do papel (336 kg/ano, 80 kg já eliminados) **só pode ser usado com aval da empresa**.
- Não citar nomes de orientador, coorientador, colegas nem da empresa.
- Frases e conceitos que podem ser usados: a tese, "low-code por restrição", "cegueira operacional", a proporção 2 meses de desenvolvimento × 7 de implantação (se confirmada), Gemba Walk, ciclo diário.

## O que está nesta pasta
- `app_e_paineis/`: o app (.msapp), o modelo do Power BI (.pbit), a planilha do Painel de Controle, o Hora-Hora e o mapa de navegação v2.
- `telas_do_app/`: prints reais das telas (mar/2026). Antes de usar num post, confira se a tela mostra dado real (OP, nome, quantidade).
- Os dados reais de produção e as fotos e vídeos da fábrica ficam em `02_Kaizen_INTERNO/` (nunca publicar).
