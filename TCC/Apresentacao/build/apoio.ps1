# apoio.ps1 - Slides de APOIO (ocultos), depois do slide 48: indice + A1..A9 (os quadros longos viram varios slides).
# NAO regera os capitulos: abre GMS_Defesa.pptx (48 slides), apaga o que houver alem do 48 (idempotente), acrescenta os slides de apoio,
# poe o ponto 'ligaApoio' no 48, salva (Save-GmsDeck) e regrava a passagem dos slides de apoio como fade simples; exporta previa/apoio/.
# Uso (depois de cap1 a cap8):  powershell -NoProfile -ExecutionPolicy Bypass -File apoio.ps1 [-TextoSaida caminho.md]
# O texto dos quadros sai direto de TCC/Fase2/TCC_GMS_Fase2.md (nada digitado a mao); -TextoSaida grava, fora do repositorio,
# o texto de cada slide com a origem (linha do TCC) para conferencia.
param([string]$TextoSaida='')
$ErrorActionPreference='Stop'
. "$PSScriptRoot\gms_lib.ps1"
$root=(Resolve-Path "$PSScriptRoot\..").Path
$pptx=Join-Path $root 'GMS_Defesa.pptx'
$prev=Join-Path $root 'previa\apoio'
$tccPath=(Resolve-Path (Join-Path $root '..\Fase2\TCC_GMS_Fase2.md')).Path
if(-not (Test-Path $pptx)){ throw 'GMS_Defesa.pptx nao existe: rode cap1 a cap8 antes.' }

# ATENCAO: nomes de variavel nao diferenciam maiusculas; nao use $BG, $SF, $LN, $TX, $T2, $GR, $SE, $RED, $INK, $GD, $CH, $ASC, $app, $pres (colidem com a lib).
$LAST=48
$NEU='#94A3B8'; $NEUF='#273241'; $NEUL='#3B4A5E'; $ROWL='#2B3644'; $CTX='#DDE3EA'   # cinza azulado do apoio (as oito cores de capitulo ficam de fora)
$FT='Bahnschrift SemiLight Condensed'; $FTB='Bahnschrift SemiBold Condensed'
$LQ=[string][char]0x201C; $RQ=[string][char]0x201D
$script:FIRST=@{}                    # codigo -> indice do primeiro slide
$script:LOG=New-Object 'System.Collections.Generic.List[string]'

# ---------------- leitura do TCC ----------------
$tccLines=[IO.File]::ReadAllLines($tccPath,[Text.Encoding]::UTF8)
function Split-Row([string]$l){ $p=@($l.Trim().Trim('|') -split '\|' | ForEach-Object { $_.Trim() }); ,$p }
function Get-TccTabela([string]$marca){
  $i=0; while($i -lt $tccLines.Count -and -not $tccLines[$i].StartsWith("[[$marca |")){ $i++ }
  if($i -ge $tccLines.Count){ throw "tabela nao encontrada no TCC: $marca" }
  $j=$i+1; while($tccLines[$j] -notmatch '^\|'){ $j++ }
  $hdr=Split-Row $tccLines[$j]; $hn=$j+1
  $j+=2; $rows=@(); $nums=@()
  while($j -lt $tccLines.Count -and $tccLines[$j] -match '^\|'){ $rows+=,(Split-Row $tccLines[$j]); $nums+=($j+1); $j++ }
  @{hdr=$hdr; rows=$rows; nums=$nums; hnum=$hn; cap=$tccLines[$i]; capnum=($i+1)}
}

# ---------------- texto rico (*italico*) e celulas ----------------
function Get-Rich([string]$raw){
  $plain=''; $spans=@()
  foreach($p in [regex]::Split($raw,'(\*[^*]+\*)')){
    if($p -match '^\*([^*]+)\*$'){ $spans+=,@(($plain.Length+1),$Matches[1].Length); $plain+=$Matches[1] } else { $plain+=$p } }
  @{plain=$plain; spans=$spans}
}
function Set-Cell($tb,[int]$r,[int]$c,[string]$raw,[bool]$head,[bool]$first,[double]$szpx,[int]$al){
  $cell=$tb.Cell($r,$c); $sh=$cell.Shape; $tf=$sh.TextFrame
  $tf.MarginLeft=8; $tf.MarginRight=8; $tf.MarginTop=4; $tf.MarginBottom=4
  $tf.VerticalAnchor= $(if($head){3}else{1})
  $rich=Get-Rich $raw
  $tr=$tf.TextRange; $tr.Text=$rich.plain
  $tr.Font.Name= $(if($head -or $first){$FTB}else{$FT})
  $tr.Font.Size=$szpx/2; $tr.Font.Bold=0
  $col= $(if($head){$NEU}elseif($first){$script:TX}else{$CTX})
  $tr.Font.Color.RGB=(Get-Rgb $col)
  $tr.ParagraphFormat.Alignment=$al
  foreach($sp in $rich.spans){ $tr.Characters($sp[0],$sp[1]).Font.Italic=-1 }
  if($head){ $sh.Fill.Visible=-1; $sh.Fill.Solid(); $sh.Fill.ForeColor.RGB=(Get-Rgb $NEUF) } else { $sh.Fill.Visible=0 }
  $b=$cell.Borders.Item(3); $b.Visible=-1; $b.ForeColor.RGB=(Get-Rgb $(if($head){$NEU}else{$ROWL})); $b.Weight=$(if($head){1.25}else{0.75})
}
# tabela nativa (estilo 'sem estilo, sem grade'); cols em px; hdr pode ser $null; sz em px (40 = 20 pt)
function New-Tabela($s,[string]$name,[double]$x,[double]$y,[double[]]$cols,$hdr,$rows,[double]$sz,[int[]]$align=@()){
  $r0= $(if($hdr){1}else{0}); $nr=$rows.Count+$r0; $nc=$cols.Count
  $w=0; foreach($cw in $cols){ $w+=$cw }
  $shp=$s.Shapes.AddTable($nr,$nc,$x/2,$y/2,$w/2,$nr*20); $shp.Name=$name
  $tb=$shp.Table
  $tb.ApplyStyle('{2D5ABB26-0587-4C30-8999-92F81FD0307C}',$false)
  for($c=1;$c -le $nc;$c++){ $tb.Columns.Item($c).Width=$cols[$c-1]/2 }
  for($c=1;$c -le $nc;$c++){
    $al= $(if($align.Count -ge $c){$align[$c-1]}else{1})
    if($hdr){ Set-Cell $tb 1 $c $hdr[$c-1] $true $false $sz $al }
    for($r=0;$r -lt $rows.Count;$r++){ Set-Cell $tb ($r+1+$r0) $c $rows[$r][$c-1] $false (($c -eq 1) -and ($nc -gt 1)) $sz $al } }
  $shp
}
function Measure-Tabela([double[]]$cols,$hdr,$rows,[double]$sz,[int[]]$align=@()){
  $sc=New-GmsSlide
  $shp=New-Tabela $sc 'medida' 96 260 $cols $hdr $rows $sz $align
  $tb=$shp.Table; $hh=0; $off=0; $hs=@()
  if($hdr){ $hh=$tb.Rows.Item(1).Height*2; $off=1 }
  for($r=1;$r -le $rows.Count;$r++){ $hs+=($tb.Rows.Item($r+$off).Height*2) }
  $sc.Delete(); $script:slideN--
  @{hh=$hh; hs=$hs}
}
# divide as linhas em paginas (equilibradas) de no maximo $maxH px
function Get-Paginas([double]$hh,[double[]]$hs,[double]$maxH,[bool]$bal=$true){
  $avail=$maxH-$hh; $n=1; $acc=0
  foreach($h in $hs){ if($acc+$h -gt $avail){ $n++; $acc=$h } else { $acc+=$h } }
  $tot=0; foreach($h in $hs){ $tot+=$h }; $target=$tot/$n
  $pages=@(); $cur=@(); $acc=0
  for($i=0;$i -lt $hs.Count;$i++){
    $h=$hs[$i]; $left=$n-$pages.Count-1; $cut=$false
    if($cur.Count -gt 0){
      if($acc+$h -gt $avail){ $cut=$true }
      elseif($bal -and $left -gt 0 -and ($acc+$h/2) -gt $target){ $cut=$true } }
    if($cut){ $pages+=,@($cur); $cur=@(); $acc=0 }
    $cur+=$i; $acc+=$h }
  $pages+=,@($cur)
  ,$pages
}

# ---------------- slide de apoio (moldura, ponto de volta, oculto) ----------------
function New-ApoioSlide([string]$contador,[string]$frase,[string]$fonte,[string]$nota,[bool]$comPonto=$true){
  $s=New-GmsSlide
  Add-Moldura $s 'Apoio' $NEU $frase $contador $fonte
  if($comPonto){ $dot=Add-Box $s 'voltaIndice' 9 96 920 24 24 $script:LN '#8B97A6' 1; $dot.Line.Transparency=0.5 }
  Set-Notes $s $nota
  $s.SlideShowTransition.Hidden=-1
  $s
}
function Add-Log([string[]]$l){ foreach($x in $l){ $script:LOG.Add($x) } }
function Fmt-Nums($nums,$idx){ $v=@(); foreach($i in $idx){ $v+=$nums[$i] }; ($v -join ', ') }

# quadro longo -> n slides (A1a, A1b, ...)
function New-ItemTabela([string]$cod,[string]$frase,[string]$fonte,[string]$srcTxt,[double[]]$cols,$hdr,$rows,[double]$sz,[int[]]$align,$nums,[string]$origem,[string]$omit,[bool]$bal=$true){
  $m=Measure-Tabela $cols $hdr $rows $sz $align
  $pg=Get-Paginas $m.hh $m.hs 626 $bal
  $n=$pg.Count
  for($p=0;$p -lt $n;$p++){
    $c= $(if($n -gt 1){ $cod+[string][char](97+$p) }else{ $cod })
    $nota="Apoio, fora dos 20 minutos. Fonte: $srcTxt." + $(if($n -gt 1){" Parte $($p+1) de $n."}else{''})
    $s=New-ApoioSlide "$c / A9" $frase $fonte $nota
    $sub=@(); foreach($i in $pg[$p]){ $sub+=,$rows[$i] }
    $null=New-Tabela $s 'tabela' 96 260 $cols $hdr $sub $sz $align
    if($p -eq 0){ $script:FIRST[$cod]=$s.SlideIndex }
    Add-Log @("","### Slide $($s.SlideIndex) ($c)","Frase-guia: $(($frase -replace '[{}]',''))","Rodape: $c / A9 · $fonte","Nota: $nota","Origem: $origem; linhas do TCC desta pagina: $(Fmt-Nums $nums $pg[$p])","Omitido/abreviado: $omit","Conteudo:")
    if($hdr){ Add-Log @("| " + ($hdr -join ' | ') + " |") }
    foreach($r in $sub){ Add-Log @("| " + ($r -join ' | ') + " |") }
  }
}

function Add-Chip($s,[string]$name,[double]$x,[double]$y,[double]$w,[double]$h,[string]$text,[double]$szpx,[string]$fill,[string]$line,[string]$color,[bool]$bold,[int]$al=1,[string]$font=''){
  $sh=Add-Box $s $name 5 $x $y $w $h $fill $line 2 0.1
  $tf=$sh.TextFrame; $tf.AutoSize=0; $tf.WordWrap=-1
  $tf.MarginLeft=10; $tf.MarginRight=10; $tf.MarginTop=4; $tf.MarginBottom=4; $tf.VerticalAnchor=3
  $tr=$tf.TextRange; $tr.Text=$text
  $tr.Font.Name= $(if($font){$font}elseif($bold){$FTB}else{$FT}); $tr.Font.Size=$szpx/2; $tr.Font.Bold=0
  $tr.Font.Color.RGB=(Get-Rgb $color); $tr.ParagraphFormat.Alignment=$al
  $sh
}

$null=Open-GmsDeckForAppend $pptx
try {
  if($script:pres.Slides.Count -lt $LAST){ throw "o deck tem menos de $LAST slides: rode cap1 a cap8." }
  # idempotente: tira o ponto antigo do 48 e apaga o que passar dele
  $s48=$script:pres.Slides.Item($LAST)
  for($k=$s48.Shapes.Count;$k -ge 1;$k--){ if($s48.Shapes.Item($k).Name -eq 'ligaApoio'){ $s48.Shapes.Item($k).Delete() } }
  while($script:pres.Slides.Count -gt $LAST){ $script:pres.Slides.Item($script:pres.Slides.Count).Delete() }
  $script:slideN=$LAST

  # ================= indice =================
  $itens=@(
    @('A1','Arquitetura completa (Quadro 2)'),
    @('A2','Modelo de dados e camadas do BI'),
    @('A3','Classes de defeito da validação (Quadro 5)'),
    @('A4','Erro frente ao sensor (Tabela 2)'),
    @('A5','MESA-11 completo (Quadro 7)'),
    @('A6','Requisitos de Forest City (Quadro 8)'),
    @('A7','Trabalhos relacionados (Quadro 1)'),
    @('A8','Referências'),
    @('A9','Créditos e licenças'))
  $sI=New-ApoioSlide 'Apoio · índice dos 9 temas' 'Para as {{perguntas}}.' 'slides ocultos' 'Apoio, fora dos 20 minutos. Índice clicável: cada item leva ao slide de apoio correspondente.' $false
  for($i=0;$i -lt 9;$i++){
    $x=96+($i % 3)*(552+36); $y=272+[int][Math]::Floor($i/3)*(180+32)
    $sh=Add-Box $sI ("ap{0}" -f ($i+1)) 5 $x $y 552 180 $NEUF $NEUL 2 0.08
    $tf=$sh.TextFrame; $tf.AutoSize=0; $tf.WordWrap=-1; $tf.MarginLeft=14; $tf.MarginRight=14; $tf.MarginTop=6; $tf.MarginBottom=6; $tf.VerticalAnchor=3
    $tr=$tf.TextRange; $tr.Text=("{0}   {1}" -f $itens[$i][0],$itens[$i][1])
    $tr.Font.Name=$FTB; $tr.Font.Size=24; $tr.Font.Bold=0; $tr.Font.Color.RGB=(Get-Rgb $script:TX); $tr.ParagraphFormat.Alignment=1
    $tr.Characters(1,2).Font.Color.RGB=(Get-Rgb $NEU)
  }
  $idxPos=$sI.SlideIndex
  Add-Log @("","### Slide $idxPos (indice)","Frase-guia: Para as perguntas.","Rodape: Apoio · índice dos 9 temas · slides ocultos","Nota: Apoio, fora dos 20 minutos. Índice clicável: cada item leva ao slide de apoio correspondente.","Origem: storyboard.md seção 6 (linha 'Apoio'); sem texto do TCC.","Omitido/abreviado: nada (os títulos seguem o storyboard).","Conteudo:")
  foreach($it in $itens){ Add-Log @("- $($it[0])   $($it[1])") }

  # ================= A1: arquitetura (Quadro 2) =================
  $q2=Get-TccTabela 'QUADRO 2'
  New-ItemTabela 'A1' 'A {{arquitetura}}, por camada.' 'Quadro 2, seção 3.3' 'Quadro 2 do TCC' @(250,560,918) $q2.hdr $q2.rows 48 @(1,1,1) $q2.nums "TCC_GMS_Fase2.md, seção 3.3, Quadro 2 (cabeçalho linha $($q2.hnum))" 'nada omitido (todas as linhas e colunas, mesma ordem)'

  # ================= A2: modelo de dados e camadas do BI =================
  $s=New-ApoioSlide 'A2a / A9' 'O {{modelo}} de dados do BI.' 'Figura 10 (Apêndice A), seções 3.3 e 4.3' 'Apoio, fora dos 20 minutos. Fonte: Figura 10 do Apêndice A e seções 3.3 e 4.3 do TCC. Parte 1 de 2.'
  $script:FIRST['A2']=$s.SlideIndex
  $cam=@(
    @('Fontes','listas do SharePoint (≈ 28); Excel de dados mestres; export do SAP (MB51)'),
    @('Bronze','consultas de origem (Power Query, não carregadas)'),
    @('Prata','tipagem, unpivot para OP × etapa, data de referência e turno; turno e data de referência resolvidos uma única vez'),
    @('Ouro','modelo semântico em estrela: fato Etapas (OP × etapa), dimensões e demais fatos; alimenta os relatórios e as medidas DAX (A2b)'))
  for($i=0;$i -lt 4;$i++){
    $y=272+$i*(128+32)
    $null=Add-Chip $s ("cam{0}" -f ($i+1)) 96 $y 360 128 $cam[$i][0] 56 $NEUF $NEUL $NEU $true 1 $FTB
    $null=Add-Chip $s ("camd{0}" -f ($i+1)) 488 $y 1336 128 $cam[$i][1] 44 $script:SF $NEUL $script:TX $false 1 $FT
  }
  Add-Log @("","### Slide $($s.SlideIndex) (A2a)","Frase-guia: O modelo de dados do BI.","Rodape: A2a / A9 · Figura 10 (Apêndice A), seções 3.3 e 4.3","Nota: Apoio, fora dos 20 minutos. Fonte: Figura 10 do Apêndice A e seções 3.3 e 4.3 do TCC. Parte 1 de 2.","Origem: Figura 10 (TCC/Fase2/figuras/fig11_bi.png e fonte/fig11_bi.html) para Fontes, Bronze, Prata e Ouro; seção 3.3 (linha 103, Quadro 2 'Análise: Camadas Bronze, Prata e Ouro; modelo estrela' e linha 107: 'a camada Prata resolve turno e data de referência uma única vez'); seção 4.3 (linha 179: indicadores entregues).","Omitido/abreviado: o Apêndice A é só a Figura 10 (imagem, sem texto no markdown); redesenhei o conteúdo dela como linhas (Fontes, Bronze, Prata, Ouro) sem as setas. A frase 'alimenta os relatórios e as medidas DAX (A2b)' liga as camadas ao slide seguinte (a figura mostra a seta Ouro para Relatórios). A frase sobre o turno e a data de referência vem da seção 3.3.","Conteudo:")
  foreach($c in $cam){ Add-Log @("- $($c[0]): $($c[1])") }

  $s=New-ApoioSlide 'A2b / A9' 'O {{modelo}} de dados do BI (cont.)' 'Figura 10 (Apêndice A), seção 4.3' 'Apoio, fora dos 20 minutos. Fonte: Figura 10 do Apêndice A e seção 4.3 do TCC. Parte 2 de 2.'
  $null=Add-Txt $s 'tOuro' 'Ouro: modelo semântico' 96 (260+56*$script:ASC) 56 @{font=$script:F_SEMICOND;color=$NEU}
  $null=Add-Chip $s 'fato' 96 363 1064 88 "Fato (lado ${LQ}muitos${RQ}): Etapas (OP × etapa)" 52 $NEUF $NEU $script:TX $true 2 $FTB
  $null=Add-Txt $s 'tDim' "Dimensões (lado ${LQ}um${RQ}); relações 1:N de sentido único" 96 (483+44*$script:ASC) 44 @{font=$FT;color=$script:T2;wrap=1064}
  $dim=@('Calendário','Turno','Etapa','OP','Mangueira','Posto','Colaborador')
  for($i=0;$i -lt 7;$i++){
    if($i -lt 4){ $x=96+$i*272; $y=568 } else { $x=96+($i-4)*272; $y=668 }
    $null=Add-Chip $s ("dim{0}" -f ($i+1)) $x $y 240 68 $dim[$i] 48 $script:SF $NEUL $script:TX $false 2 $FT
  }
  $null=Add-Txt $s 'tFatos' 'Demais fatos: Refugo, Inspeção, Hora-Hora, Parada, Carretel, Evento, Fluxo de etapas' 96 (768+44*$script:ASC) 44 @{font=$FT;color=$CTX;wrap=1064}
  $null=Add-Txt $s 'tRel' 'Relatórios e medidas DAX' 1192 (260+56*$script:ASC) 56 @{font=$script:F_SEMICOND;color=$NEU;wrap=632}
  $rel=@('Tempo de ciclo por etapa (mediana)','Lead time da OP (mediana e P90)','Índice de gargalo (WIP ÷ vazão)','Idade da OP na etapa','Hora-Hora: real × meta')
  $lst=Add-Txt $s 'listaRel' ($rel -join "`r") 1192 (363+48*$script:ASC) 48 @{font=$FT;color=$script:TX;wrap=632}
  $pf=$lst.TextFrame.TextRange.ParagraphFormat; $pf.Bullet.Visible=-1; $pf.Bullet.Character=8226; $pf.SpaceAfter=16
  $lst.TextFrame.Ruler.Levels.Item(1).FirstMargin=0; $lst.TextFrame.Ruler.Levels.Item(1).LeftMargin=20
  Add-Log @("","### Slide $($s.SlideIndex) (A2b)","Frase-guia: O modelo de dados do BI (cont.)","Rodape: A2b / A9 · Figura 10 (Apêndice A), seção 4.3","Nota: Apoio, fora dos 20 minutos. Fonte: Figura 10 do Apêndice A e seção 4.3 do TCC. Parte 2 de 2.","Origem: Figura 10 (fig11_bi.png / fig11_bi.html): modelo semântico Ouro, fato Etapas (OP × etapa), dimensões Calendário, Turno, Etapa, OP, Mangueira, Posto, Colaborador, 'Demais fatos', notação (1 = lado um, * = lado muitos, relações 1:N de sentido único) e a caixa 'Relatórios e medidas DAX' com os cinco itens; seção 4.3, linha 179, confere os indicadores (ciclo e lead time pela mediana, P90 no lead time, índice de gargalo = WIP / vazão recente, idade da OP na etapa, Hora-Hora).","Omitido/abreviado: sem as linhas desenhadas entre fato e dimensões nem os símbolos 1 e * em cada ligação (a notação vai por escrito no rótulo e na caixa do fato); sem as setas.","Conteudo:","- Ouro: modelo semântico","- Fato (lado ${LQ}muitos${RQ}): Etapas (OP × etapa)","- Dimensões (lado ${LQ}um${RQ}); relações 1:N de sentido único: $($dim -join ', ')","- Demais fatos: Refugo, Inspeção, Hora-Hora, Parada, Carretel, Evento, Fluxo de etapas","- Relatórios e medidas DAX: $($rel -join '; ')")

  # ================= A3: classes de defeito (Quadro 5) =================
  $q5=Get-TccTabela 'QUADRO 5'
  New-ItemTabela 'A3' 'Os {{defeitos}} e o tratamento.' 'Quadro 5, seção 4.4' 'Quadro 5 do TCC' @(760,968) $q5.hdr $q5.rows 48 @(1,1) $q5.nums "TCC_GMS_Fase2.md, seção 4.4, Quadro 5 (cabeçalho linha $($q5.hnum))" 'nada omitido (todas as linhas, mesma ordem); sem contagem absoluta no quadro'

  # ================= A4: erro frente ao sensor (Tabela 2, so as colunas de erro) =================
  $tab2=Get-TccTabela 'TABELA 2'
  $capT=($tab2.cap.Trim('[',']') -split ' \| ')[1]
  $h4=@($tab2.hdr[0],$tab2.hdr[2],$tab2.hdr[3],$tab2.hdr[4],$tab2.hdr[5])
  $r4=@(); foreach($r in $tab2.rows){ $r4+=,@($r[0],$r[2],$r[3],$r[4],$r[5]) }
  $nota4='Nos turnos fechados, as duas formas erram cerca de nove minutos por hora, sem tendência para mais ou para menos; no 3º turno, o cálculo pela produção recupera a parada que faltava.'
  $s=New-ApoioSlide 'A4 / A9' 'O erro frente ao {{sensor}}.' 'Tabela 2, seção 4.4' 'Apoio, fora dos 20 minutos. Fonte: Tabela 2 do TCC.'
  $script:FIRST['A4']=$s.SlideIndex
  $leg=Add-Txt $s 'legenda' $capT 96 (260+48*$script:ASC) 48 @{font=$FT;color=$script:T2;wrap=1728}
  $yT=[Math]::Ceiling(($leg.Top+$leg.Height)*2+32)
  $tbl4=New-Tabela $s 'tabela' 96 $yT @(560,292,292,292,292) $h4 $r4 52 @(1,2,2,2,2)
  $yN=[Math]::Ceiling(($tbl4.Top+$tbl4.Height)*2+32)
  $null=Add-Txt $s 'leitura' $nota4 96 ($yN+48*$script:ASC) 48 @{font=$FT;color=$CTX;wrap=1728}
  Add-Log @("","### Slide $($s.SlideIndex) (A4)","Frase-guia: O erro frente ao sensor.","Rodape: A4 / A9 · Tabela 2, seção 4.4","Nota: Apoio, fora dos 20 minutos. Fonte: Tabela 2 do TCC.","Origem: TCC_GMS_Fase2.md, Tabela 2 (legenda linha $($tab2.capnum), cabeçalho linha $($tab2.hnum), linhas $($tab2.nums -join ', ')); texto de leitura: seção 4.4, linha 219 (trecho do parágrafo que apresenta a Tabela 2, de 'Nos turnos fechados' até 'que faltava', copiado inteiro).","Omitido/abreviado: coluna 'Horas' (182, 56, 251) omitida, como pedido (só colunas de erro); o resto da legenda, a unidade e as linhas estão completos. Tabela 2 não tem contagem de produção.","Conteudo:","Legenda: $capT","| " + ($h4 -join ' | ') + " |")
  foreach($r in $r4){ Add-Log @("| " + ($r -join ' | ') + " |") }
  Add-Log @("Leitura: $nota4")

  # ================= A5: MESA-11 (Quadro 7) =================
  $q7=Get-TccTabela 'QUADRO 7'
  New-ItemTabela 'A5' 'O {{MESA-11}}, função a função.' 'Quadro 7, seção 4.7' 'Quadro 7 do TCC' @(420,270,270,768) $q7.hdr $q7.rows 44 @(1,1,1,1) $q7.nums "TCC_GMS_Fase2.md, seção 4.7, Quadro 7 (cabeçalho linha $($q7.hnum))" 'nada omitido (as 11 funções, mesma ordem)'

  # ================= A6: requisitos de Forest City (Quadro 8) =================
  $q8=Get-TccTabela 'QUADRO 8'
  New-ItemTabela 'A6' '{{Requisitos}} de Forest City.' 'Quadro 8, seção 4.9' 'Quadro 8 do TCC' @(280,725,723) $q8.hdr $q8.rows 48 @(1,1,1) $q8.nums "TCC_GMS_Fase2.md, seção 4.9, Quadro 8 (cabeçalho linha $($q8.hnum))" 'nada omitido (as 6 linhas, mesma ordem); o título do quadro cita o nome da planta, o slide não'

  # ================= A7: trabalhos relacionados (Quadro 1) =================
  $q1=Get-TccTabela 'QUADRO 1'
  New-ItemTabela 'A7' 'Os {{trabalhos}} relacionados.' 'Quadro 1, seção 2.7' 'Quadro 1 do TCC' @(250,480,500,498) $q1.hdr $q1.rows 44 @(1,1,1,1) $q1.nums "TCC_GMS_Fase2.md, seção 2.7, Quadro 1 (cabeçalho linha $($q1.hnum))" 'nada omitido (os 8 trabalhos, mesma ordem)'

  # ================= A8: referencias citadas na apresentacao e nos quadros 1 =================
  $refStart=0; for($i=0;$i -lt $tccLines.Count;$i++){ if($tccLines[$i] -eq '## REFERÊNCIAS BIBLIOGRÁFICAS'){ $refStart=$i; break } }
  $refKeys=@('ATKIN, D.','BIANCHINI, A.','DI RUSCIO, D.','GOMES, C.','HEUER, M.','IMAI, M.','JESUS, C.','KOPROV, P.','MESA INTERNATIONAL.','NOVOCHADLO, Y.','SANTOS, J.','SPEICHER, T.','TAPIA, E.','WOMACK, J.','WU, K.')
  $refRows=@(); $refNums=@()
  foreach($key in $refKeys){
    $found=-1; for($i=$refStart;$i -lt $tccLines.Count;$i++){ if($tccLines[$i].StartsWith($key)){ $found=$i; break } }
    if($found -lt 0){ throw "referencia nao encontrada: $key" }
    $txt=($tccLines[$found] -replace ' Disponível em:.*$','') -replace ' Acesso em:.*$',''
    $refRows+=,@($txt); $refNums+=($found+1) }
  New-ItemTabela 'A8' 'As {{referências}} citadas.' 'citadas no deck e no Quadro 1; lista completa no TCC' 'referências do TCC' @(1728) $null $refRows 40 @(1) $refNums 'TCC_GMS_Fase2.md, REFERÊNCIAS BIBLIOGRÁFICAS (linhas ao lado); citadas nos slides: Imai (2012), Womack e Jones (1996), Di Ruscio et al. (2022), Atkin et al. (2017), Jesus et al. (2025), Wu, Xu e Zheng (2024), MESA International (1997); mais os oito trabalhos do Quadro 1 (Heuer, Santos, Koprov e Starly, Bianchini, Gomes, Speicher, Novochadlo e Paladini, Tapia). O Quadro 8 não cita autor' 'omitidos "Disponível em: ..." e "Acesso em: ..." (o DOI fica); as outras ~35 referências do TCC não entram (a lista completa está no TCC)'

  # ================= A9: creditos e licencas (assets/CREDITOS.md) =================
  $c9=@(
    @('Bahnschrift, Consolas e Ink Free','Quase todo o texto (Bahnschrift); rodapé e tabelas (Consolas); a Ink Free só na ficha de papel','Fontes do Windows e do Office (Microsoft); não embutidas nem distribuídas'),
    @('Logo da UNISAL','Só na capa, sobre placa branca','Marca da instituição de ensino; uso institucional, só na defesa; sem licença aberta'),
    @('Carretel e logo do GMS','Cantos dos slides e slide final','Formas do PowerPoint; marca do próprio projeto, autoria própria'),
    @('Ficha de papel da abertura','Slides de abertura','Formas e texto do PowerPoint; autoria própria; preenchimento fictício'),
    @('Globo de pontos','Slides 43 a 45','Ovais do PowerPoint; autoria própria; contorno aproximado à mão, sem fonte externa'),
    @('Mangueira hidráulica','Slides 15 a 19 e 47','Autoria própria; imagens e modelo criados por scripts próprios; nenhum modelo de terceiros'),
    @('Telas recriadas do GMS','Mosaico, tablet e plano B','Autoria própria; dado 100% fictício; nenhum print real'),
    @('Peças de terceiros','Logo e fontes','Só a logo da UNISAL e as três fontes do Windows; nada foi baixado; o deck não embute vídeo nem áudio'))
  New-ItemTabela 'A9' '{{Créditos}} e licenças.' 'assets/CREDITOS.md' 'assets/CREDITOS.md do repositório' @(430,470,828) @('Ativo','Onde aparece','Origem e licença') $c9 44 @(1,1,1) @(9,19,20,21,22,23,24,3) 'assets/CREDITOS.md (tabela Fontes, linhas 9 a 11; tabela Imagens e marcas, linhas 19 a 24; seção de licenças, linha 32; introdução, linha 3)' 'resumido: uma linha para as três fontes; sem o tamanho do modelo (triângulos), sem os nomes dos arquivos e sem a lista de ferramentas de montagem'

  # ================= ligacoes =================
  $nTot=$script:pres.Slides.Count
  $sIdx=$script:pres.Slides.Item($idxPos)
  for($i=0;$i -lt 9;$i++){
    $tg=$script:pres.Slides.Item($script:FIRST[$itens[$i][0]])
    $as=$sI.Shapes.Item("ap$($i+1)").ActionSettings.Item(1)
    $as.Action=7; $as.Hyperlink.SubAddress=("{0},{1},{2}" -f $tg.SlideID,$tg.SlideIndex,$itens[$i][0])
  }
  for($n=$idxPos+1;$n -le $nTot;$n++){
    $sl=$script:pres.Slides.Item($n)
    $as=$sl.Shapes.Item('voltaIndice').ActionSettings.Item(1)
    $as.Action=7; $as.Hyperlink.SubAddress=("{0},{1},{2}" -f $sIdx.SlideID,$sIdx.SlideIndex,'Apoio')
  }
  $dot=Add-Box $s48 'ligaApoio' 9 96 920 24 24 $script:LN '#8B97A6' 1
  $dot.Line.Transparency=0.5
  $as=$dot.ActionSettings.Item(1); $as.Action=7; $as.Hyperlink.SubAddress=("{0},{1},{2}" -f $sIdx.SlideID,$sIdx.SlideIndex,'Apoio')

  # ================= conferencias antes de salvar =================
  $idx=($idxPos)..($nTot)
  $nviol=Test-GmsLayout -Slides $idx
  "violacoes de layout (slides $idxPos a $nTot): $nviol"
  # depois do teste (que usa os nomes da moldura), nenhum nome '!!' nos slides de apoio
  foreach($sl in $script:pres.Slides){ if($sl.SlideIndex -gt $LAST){ foreach($sh in $sl.Shapes){ if($sh.Name.StartsWith('!!')){ $sh.Name=$sh.Name.Substring(2) } } } }
  foreach($sl in $script:pres.Slides){ $sl.SlideShowTransition.AdvanceOnClick=-1; $sl.SlideShowTransition.AdvanceOnTime=0 }
  Save-GmsDeck $pptx 1.2
  "salvo: $pptx"

  # ================= passagem: fade simples so nos slides de apoio =================
  $z=[IO.Compression.ZipFile]::Open($pptx,'Update')
  $u8=New-Object Text.UTF8Encoding($false)
  $rd={ param($e) $r=New-Object IO.StreamReader($e.Open(),$u8); $x=$r.ReadToEnd(); $r.Close(); $x }
  $px=& $rd $z.GetEntry('ppt/presentation.xml'); $pr=& $rd $z.GetEntry('ppt/_rels/presentation.xml.rels')
  $ids=@([regex]::Matches($px,'<p:sldId [^>]*r:id="(rId\d+)"') | ForEach-Object { $_.Groups[1].Value })
  $map=@{}
  foreach($m in [regex]::Matches($pr,'<Relationship [^>]*>')){ $v=$m.Value; if($v -match 'Id="(rId\d+)"'){ $rid=$Matches[1]; if($v -match 'Target="(slides/slide\d+\.xml)"'){ $map[$rid]=$Matches[1] } } }
  $fade='<p:transition spd="med"><p:fade/></p:transition>'
  for($n=$LAST+1;$n -le $ids.Count;$n++){
    $en='ppt/'+$map[$ids[$n-1]]
    $x=& $rd $z.GetEntry($en)
    $x=[regex]::Replace($x,'<mc:AlternateContent[^>]*>(?:(?!</mc:AlternateContent>).)*?</mc:AlternateContent>',{ param($m) if($m.Value -match '<p:transition'){ '' } else { $m.Value } },'Singleline')
    $x=$x -replace '<p:transition[^>]*/>',''
    $x=[regex]::Replace($x,'<p:transition[^>]*>.*?</p:transition>','','Singleline')
    $x=$x -replace '</p:clrMapOvr>',('</p:clrMapOvr>'+$fade)
    $z.GetEntry($en).Delete(); $ne=$z.CreateEntry($en); $w=New-Object IO.StreamWriter($ne.Open(),$u8); $w.Write($x); $w.Close()
  }
  $z.Dispose()
  "fade gravado nos slides $($LAST+1) a $($ids.Count)"

  # ================= PNGs dos slides novos =================
  New-Item -ItemType Directory -Force $prev | Out-Null
  Remove-Item (Join-Path $prev 'slide_*.png') -Force -ErrorAction SilentlyContinue
  $null=Open-GmsDeck $pptx
  Export-GmsSlides $prev 1920 1080 $idx
  "PNGs (slides $idxPos a $nTot, numeracao do deck): $prev"

  if($TextoSaida){
    $hd=@('# Texto dos slides de apoio (gerado por build/apoio.ps1)','','Fonte do conteudo: TCC/Fase2/TCC_GMS_Fase2.md (numero de linha 1-based) e assets/CREDITOS.md. Slides ocultos, depois do 48.')
    [IO.File]::WriteAllLines($TextoSaida,[string[]]($hd+$script:LOG),(New-Object Text.UTF8Encoding($true)))
    "texto: $TextoSaida"
  }
} finally { Close-GmsDeck }
