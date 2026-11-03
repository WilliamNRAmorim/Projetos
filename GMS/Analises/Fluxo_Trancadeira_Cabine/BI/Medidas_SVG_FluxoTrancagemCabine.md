# Medidas SVG: cartões por etapa (layout da `ilustracao_headcount.html`) — PENDENTE DE APLICAR

Precisa do Bloco 1 a 3 de `Medidas_FluxoTrancagemCabine.md` já aplicado (usa `Pessoas por Dia`, `Pessoas Máx no Dia`,
`Vazão por Etapa (m/dia)`, `m por Pessoa`, `Conteúdo de Mão de Obra (pessoas/1.000 m)` e as auxiliares).

| Medida | O que desenha | Onde usar |
|---|---|---|
| `SVG Cartão Etapa` | cartão completo da etapa: "ETAPA n", nome, ícones de pessoa, pessoas/dia com "máx", barra de metros/dia, caixa m/pessoa + pessoas a cada 1.000 m, borda e selo laranja nas 2 etapas com mais gente por metro, seta para a próxima etapa | matriz com `dEtapa[Etapa no Fluxo]` nas colunas (6 cartões lado a lado) |
| `SVG Pessoas` | (b) só a fileira de ícones: 1 por pessoa, o último preenchido pela fração, o resto em cinza até o máximo observado | tabela/matriz por etapa |
| `SVG Barra Metros` | (a) barra de metros/dia com o valor | tabela/matriz por etapa |
| `SVG Conteúdo` | (c) barra de pessoas por 1.000 m com linha tracejada da média do trecho; laranja nas 2 maiores, verde nas demais | tabela com as 6 etapas em linhas |

Cores fixas do tema escuro da ilustração (o SVG não lê o tema do Power BI). No SVG, `#` vira `%23` (senão o
navegador corta a URL no `#`). Percentual também não pode aparecer cru no SVG; por isso a fração do ícone vai em 0–1.

## Como marcar "URL da imagem"

Depois de aplicar, para cada uma das 4 medidas `SVG ...`:
1. Painel **Dados** → clique na medida → faixa **Ferramentas de medida** → **Categoria de dados** = **URL da imagem**.
   (No TMDL abaixo isso já vai como `dataCategory: ImageUrl`. Se o TMDL view recusar essa linha, apague-a e marque à mão.)
2. Na matriz/tabela: **Formatar visual → Visual → Tamanho da imagem**: Altura e Largura (valores abaixo).
   Sem isso a imagem sai pequena (padrão 75 px de altura).

Tamanho de cada imagem:
- `SVG Cartão Etapa`: 208 × 304 (largura × altura).
- `SVG Pessoas`: 154 × 50. `SVG Barra Metros`: 240 × 22. `SVG Conteúdo`: 440 × 32.

## Montar os 6 cartões (matriz)

1. Visual **Matriz**. **Colunas**: `dEtapa[Etapa no Fluxo]`. **Valores**: `SVG Cartão Etapa`. Linhas: vazio.
2. Filtro deste visual: `dEtapa[Trecho Tranç-Cabine]` = Verdadeiro. A ordem sai pela `Ordem_Fluxo` (a coluna
   `Etapa no Fluxo` já vem com "Classificar por coluna" = `Ordem_Fluxo` no TMDL). Conferir no visual:
   **Mais opções (...) → Classificar eixo → Etapa no Fluxo, crescente**.
3. **Subtotais de coluna**: desligado. **Grade**: linhas horizontais e verticais desligadas, contorno nenhum,
   espaçamento interno das linhas 0.
4. **Cabeçalhos de coluna**: fonte 9, cor "Plano de fundo" do tema (some no fundo; o nome já está no cartão).
5. **Tamanho da imagem**: altura 304, largura 208. Visual sem borda e sem fundo próprio (o cartão já tem os dois).
6. Título com formatação condicional (**fx → Valor do campo → `Título Cartões`**).

Etapa sem dado no filtro: o cartão some (BLANK), não aparece zerado.

## Bloco 4 — TMDL (colar depois dos Blocos 1–3)

```
createOrReplace

	ref table Medidas

		measure '_SVG Pessoas (fragmento)' =
				-- Ícones de pessoa (7 por linha, até 14): 1 por pessoa da média, o último preenchido pela fração, cinza até o máximo do dia. Fragmento sem <svg>.
				VAR Pessoas = [Pessoas por Dia]
				VAR Maximo = [Pessoas Máx no Dia]
				VAR CorOn = "%235b9bf0"
				VAR CorOff = "%23333d4a"
				VAR Total = MIN ( 14, MAX ( Maximo, ROUNDUP ( Pessoas, 0 ) ) )
				RETURN
				    IF (
				        Total > 0,
				        CONCATENATEX (
				            GENERATESERIES ( 0, Total - 1, 1 ),
				            VAR i = [Value]
				            VAR f = MAX ( 0, MIN ( 1, Pessoas - i ) )
				            VAR Of = FORMAT ( f, "0.00", "en-US" )
				            VAR x = MOD ( i, 7 ) * 22
				            VAR y = INT ( i / 7 ) * 26
				            RETURN
				                "<linearGradient id='p" & i & "'><stop offset='" & Of & "' stop-color='" & CorOn
				                    & "'/><stop offset='" & Of & "' stop-color='" & CorOff & "'/></linearGradient>"
				                    & "<g transform='translate(" & x & " " & y & ")'>"
				                    & "<circle cx='10' cy='5' r='4.6' fill='url(%23p" & i & ")'/>"
				                    & "<path d='M2 24v-6a8 8 0 0 1 16 0v6z' fill='url(%23p" & i & ")'/></g>",
				            "",
				            [Value], ASC
				        )
				    )
			isHidden
			displayFolder: Fluxo Tranç→Cabine\Auxiliares

		measure '_SVG Barra Metros (fragmento)' =
				-- Trilho de 156 px e barra de metros/dia proporcional à maior vazão do trecho (+5%). Fragmento sem <svg>.
				VAR Metros = [Vazão por Etapa (m/dia)]
				VAR Escala = [_Maior Vazão do Trecho] * 1.05
				VAR L = IF ( Escala > 0 && NOT ISBLANK ( Metros ), ROUND ( 156 * DIVIDE ( Metros, Escala ), 1 ), 0 )
				RETURN
				    "<rect x='0' y='0' width='156' height='10' rx='5' fill='%2322344d'/>"
				        & IF ( L > 0, "<rect x='0' y='0' width='" & FORMAT ( L, "0.0", "en-US" ) & "' height='10' rx='5' fill='%235b9bf0'/>" )
			isHidden
			displayFolder: Fluxo Tranç→Cabine\Auxiliares

		measure 'SVG Cartão Etapa' =
				-- Cartão da etapa no layout aprovado (ilustracao_headcount.html). Laranja = 2 etapas com mais pessoas por 1.000 m no filtro.
				VAR Ordem = SELECTEDVALUE ( dEtapa[Ordem_Fluxo] )
				VAR Nome = SELECTEDVALUE ( dEtapa[Etapa no Fluxo] )
				VAR NoTrecho = SELECTEDVALUE ( dEtapa[Trecho Tranç-Cabine] )
				VAR Primeira = CALCULATE ( MIN ( dEtapa[Ordem_Fluxo] ), REMOVEFILTERS ( dEtapa ), dEtapa[Trecho Tranç-Cabine] = TRUE () )
				VAR Ultima = CALCULATE ( MAX ( dEtapa[Ordem_Fluxo] ), REMOVEFILTERS ( dEtapa ), dEtapa[Trecho Tranç-Cabine] = TRUE () )
				VAR Pessoas = [Pessoas por Dia]
				VAR Maximo = [Pessoas Máx no Dia]
				VAR Metros = [Vazão por Etapa (m/dia)]
				VAR MPessoa = [m por Pessoa]
				VAR Conteudo = [Conteúdo de Mão de Obra (pessoas/1.000 m)]
				VAR Pos = [_Posição Conteúdo]
				VAR Quente = NOT ISBLANK ( Pos ) && Pos <= 2
				-- Paleta escura da ilustração
				VAR Cartao = "%231a212b"
				VAR Tinta = "%23e7ebf0"
				VAR Suave = "%239aa5b3"
				VAR Linha = "%232b3440"
				VAR Laranja = "%23ff8a50"
				VAR LaranjaFundo = "%233a2418"
				VAR Verde = "%235fcf75"
				VAR VerdeFundo = "%231c3323"
				VAR Contorno =
				    IF (
				        Quente,
				        "<rect x='3' y='12' width='180' height='288' rx='14' fill='none' stroke='" & LaranjaFundo & "' stroke-width='6'/>"
				            & "<rect x='3' y='12' width='180' height='288' rx='14' fill='" & Cartao & "' stroke='" & Laranja & "' stroke-width='1.5'/>",
				        "<rect x='3.5' y='12.5' width='179' height='287' rx='14' fill='" & Cartao & "' stroke='" & Linha & "' stroke-width='1'/>"
				    )
				VAR Selo =
				    IF (
				        Quente,
				        "<rect x='67' y='1' width='104' height='21' rx='10.5' fill='" & Laranja & "'/>"
				            & "<text x='119' y='15.5' text-anchor='middle' font-size='11' font-weight='700' fill='%2311161d'>mais gente/metro</text>"
				    )
				VAR Cabecalho =
				    "<text x='15' y='40' font-size='11' font-weight='700' letter-spacing='0.7' fill='" & Suave & "'>ETAPA " & ( Ordem - Primeira + 1 ) & "</text>"
				        & "<text x='15' y='60' font-size='16.5' font-weight='700' fill='" & Tinta & "'>" & Nome & "</text>"
				VAR Icones = "<g transform='translate(15 72)'>" & [_SVG Pessoas (fragmento)] & "</g>"
				VAR Numero =
				    "<text x='15' y='148' fill='" & Tinta & "'><tspan font-size='22' font-weight='700'>" & FORMAT ( Pessoas, "0.0", "pt-BR" ) & "</tspan>"
				        & "<tspan font-size='11.5' fill='" & Suave & "'> pessoas/dia" & IF ( NOT ISBLANK ( Maximo ), " · máx " & FORMAT ( Maximo, "0" ) ) & "</tspan></text>"
				VAR Barra =
				    "<text x='15' y='174' font-size='12' fill='" & Suave & "'>Metros por dia</text>"
				        & "<g transform='translate(15 181)'>" & [_SVG Barra Metros (fragmento)] & "</g>"
				        & "<text x='15' y='210' font-size='13' fill='" & Tinta & "'><tspan font-weight='700'>" & FORMAT ( Metros, "#,0", "pt-BR" ) & "</tspan> m/dia</text>"
				VAR Caixa =
				    "<rect x='15' y='232' width='156' height='54' rx='10' fill='" & IF ( Quente, LaranjaFundo, VerdeFundo ) & "'/>"
				        & "<text x='25' y='256' fill='" & Tinta & "'><tspan font-size='18' font-weight='700' fill='" & IF ( Quente, Laranja, Verde ) & "'>"
				        & FORMAT ( MPessoa, "#,0", "pt-BR" ) & "</tspan><tspan font-size='13'> m/pessoa</tspan></text>"
				        & "<text x='25' y='275' font-size='11' fill='" & Suave & "'>" & FORMAT ( Conteudo, "0.00", "pt-BR" ) & " pessoa a cada 1.000 m</text>"
				VAR Seta =
				    IF (
				        Ordem < Ultima,
				        "<path d='M189 156h12M197 151l5 5-5 5' fill='none' stroke='" & Suave & "' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/>"
				    )
				RETURN
				    IF (
				        NOT NoTrecho || ( ISBLANK ( Metros ) && ISBLANK ( Pessoas ) ),
				        BLANK (),
				        "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='208' height='304' viewBox='0 0 208 304' font-family='Segoe UI, sans-serif'>"
				            & Contorno & Selo & Cabecalho & Icones & Numero & Barra & Caixa & Seta & "</svg>"
				    )
			dataCategory: ImageUrl
			displayFolder: Fluxo Tranç→Cabine

		measure 'SVG Pessoas' =
				-- (b) Só os ícones de pessoa da etapa (mesma regra do cartão).
				VAR Frag = [_SVG Pessoas (fragmento)]
				RETURN
				    IF (
				        NOT ISBLANK ( Frag ),
				        "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='154' height='50' viewBox='0 0 154 50'>" & Frag & "</svg>"
				    )
			dataCategory: ImageUrl
			displayFolder: Fluxo Tranç→Cabine

		measure 'SVG Barra Metros' =
				-- (a) Barra de metros/dia da etapa com o valor à direita.
				VAR Metros = [Vazão por Etapa (m/dia)]
				RETURN
				    IF (
				        NOT ISBLANK ( Metros ),
				        "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='22' viewBox='0 0 240 22' font-family='Segoe UI, sans-serif'>"
				            & "<g transform='translate(0 6)'>" & [_SVG Barra Metros (fragmento)] & "</g>"
				            & "<text x='236' y='15.5' text-anchor='end' font-size='13' font-weight='700' fill='%23e7ebf0'>" & FORMAT ( Metros, "#,0", "pt-BR" ) & "</text></svg>"
				    )
			dataCategory: ImageUrl
			displayFolder: Fluxo Tranç→Cabine

		measure 'SVG Conteúdo' =
				-- (c) Pessoas por 1.000 m da etapa; tracejado = média do trecho. Laranja nas 2 maiores, verde nas demais.
				VAR Conteudo = [Conteúdo de Mão de Obra (pessoas/1.000 m)]
				VAR Media = [Conteúdo Médio do Trecho (pessoas/1.000 m)]
				VAR Escala = [_Maior Conteúdo do Trecho] * 1.1
				VAR Pos = [_Posição Conteúdo]
				VAR Quente = NOT ISBLANK ( Pos ) && Pos <= 2
				VAR W = 380
				VAR Lc = ROUND ( W * DIVIDE ( Conteudo, Escala ), 1 )
				VAR Lm = ROUND ( W * DIVIDE ( Media, Escala ), 1 )
				VAR XMedia = FORMAT ( Lm, "0.0", "en-US" )
				RETURN
				    IF (
				        NOT ISBLANK ( Conteudo ) && Escala > 0,
				        "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='440' height='32' viewBox='0 0 440 32' font-family='Segoe UI, sans-serif'>"
				            & "<rect x='0' y='7' width='" & W & "' height='18' rx='6' fill='%2322344d'/>"
				            & "<rect x='0' y='7' width='" & FORMAT ( Lc, "0.0", "en-US" ) & "' height='18' rx='6' fill='" & IF ( Quente, "%23ff8a50", "%235fcf75" ) & "'/>"
				            & IF ( NOT ISBLANK ( Media ), "<line x1='" & XMedia & "' x2='" & XMedia & "' y1='2' y2='30' stroke='%23e7ebf0' stroke-width='1.5' stroke-dasharray='4 3'/>" )
				            & "<text x='436' y='21' text-anchor='end' font-size='14' font-weight='700' fill='" & IF ( Quente, "%23ff8a50", "%23e7ebf0" ) & "'>"
				            & FORMAT ( Conteudo, "0.00", "pt-BR" ) & "</text></svg>"
				    )
			dataCategory: ImageUrl
			displayFolder: Fluxo Tranç→Cabine
```

## Geometria do cartão (208 × 304, para ajuste fino)

| Elemento | Posição |
|---|---|
| Cartão | x 3, y 12, 180 × 288, cantos 14; borda 1 px cinza ou 1,5 px laranja + halo de 6 px |
| Selo "mais gente/metro" | x 67, y 1, 104 × 21 (centrado em x 119); texto escuro `#11161d` sobre laranja (7,6:1). Branco, como na ilustração, dá 2,3:1 e reprova a §B.6.4 |
| "ETAPA n" / nome | y 40 / y 60, x 15 |
| Ícones | início em (15, 72); 7 por linha, passo 22 px, linhas a cada 26 px; até 14 ícones |
| Pessoas/dia + máx | y 148 |
| "Metros por dia" / barra / valor | y 174 / y 181 (156 × 10) / y 210 |
| Caixa m/pessoa | x 15, y 232, 156 × 54, cantos 10 |
| Seta | x 189 a 202, y 156 (some na última etapa) |

Mais de 14 pessoas por dia numa etapa: os ícones param em 14 e o número abaixo mostra o valor real.

## Tema claro (se um dia trocar)

O SVG não segue o tema. Para a versão clara, troque os valores das VARs (mesmos nomes) pelos da ilustração no modo claro:
`Cartao %23ffffff`, `Tinta %231b2430`, `Suave %235b6675`, `Linha %23dfe3e9`, `Laranja %23d9480f`,
`LaranjaFundo %23fde7dc`, `Verde %232f9e44`, `VerdeFundo %23e3f4e6`; nos fragmentos: ícone `%233a7bd5` / apagado
`%23d9dee5`, trilho `%23d6e4f7`, barra `%233a7bd5`; no `SVG Conteúdo` o texto e a linha da média passam a `%231b2430`.
