# cap1.ps1 - Capitulo 1 (10 slides) da defesa. Gera TCC/Apresentacao/GMS_Defesa.pptx, previa/cap1/slide_NN.png e cap1.mp4.
# Uso: powershell -NoProfile -ExecutionPolicy Bypass -File cap1.ps1 [-SemVideo]
param([switch]$SemVideo)
$ErrorActionPreference='Stop'
. "$PSScriptRoot\gms_lib.ps1"
$root=(Resolve-Path "$PSScriptRoot\..").Path
$pptx=Join-Path $root 'GMS_Defesa.pptx'
$prev=Join-Path $root 'previa\cap1'
$rot=Get-Roteiro (Join-Path $root 'roteiro.md')

$BLUE=$script:CH[0]
$FRAC=@{ '1a'=0; '1b'=0.1; '1c'=0.2; '1d'=0.3; '1e'=0.4; '2'=0.5; '3'=0.6; '4'=0.7; '5'=0.8; '6'=0.9 }
$FV='000123','250 m','07','2º'
$NX=700,1040,1330,1580; $NDY=-40,30,-70,10
$W=700   # altura do fio horizontal (px)

function Reel-Small($s,$id){ Add-Reel $s 1800 985 62 $FRAC[$id] }
function Dot-At([double]$cx,[double]$cy,[double]$r,[double]$frac){ $ang= if($frac -gt 0){-86+37*$frac}else{-90}; @{x=$cx+$r*[Math]::Cos($ang*[Math]::PI/180); y=$cy+$r*[Math]::Sin($ang*[Math]::PI/180)} }

# numeros manuscritos da ficha: posicao dentro da ficha (x,y,w da ficha)
function Add-FichaNumeros($s,[double]$x,[double]$y,[double]$w,$color,$glow){
  $h=1.25*$w
  for($i=0;$i -lt 4;$i++){
    $o=@{font=$script:F_HAND;color=$color;align='l';round=$BLUE}
    if($glow){ $o.glow=$BLUE }
    $null=Add-Txt $s "!!n$($i+1)" $FV[$i] ($x+0.52*$w) ($y+$h*(0.16+0.14*$i+0.095)) ($w*0.075) $o
  } }
function Add-Campos($s,[double]$x,[double]$y,[double]$w,[double]$transp){
  $h=1.25*$w
  for($i=0;$i -lt 4;$i++){ $ry=$y+$h*(0.16+0.14*$i); $null=Add-Box $s "!!campo$($i+1)" 1 ($x+0.46*$w) ($ry+0.01*$h) (0.49*$w) (0.12*$h) $BLUE $null 2 }
  for($i=0;$i -lt 4;$i++){ $s.Shapes.Item("!!campo$($i+1)").Fill.Transparency=$transp } }
function Add-Marcas($s,[double]$x,[double]$y,[double]$w){
  $h=1.25*$w; $gy=$y+$h*0.74; $t='X','✓','✓'
  for($j=0;$j -lt 3;$j++){ $null=Add-Txt $s "!!marca$($j+1)" $t[$j] ($x+0.19*$w+$j*0.3067*$w) ($gy+$h*0.11) ($w*0.05) @{font=$script:F_HAND;color=$script:INK;align='m'} } }
function To-Dot($sh,[double]$cx,[double]$cy,[double]$dpx,$hex){
  $sh.TextFrame2.AutoSize=0; $sh.TextFrame2.WordWrap=0
  $sh.TextFrame.TextRange.Font.Size=2; $sh.TextFrame.TextRange.Font.Color.RGB=(Get-Rgb $hex)
  $sh.Fill.Visible=-1; $sh.Fill.Solid(); $sh.Fill.ForeColor.RGB=(Get-Rgb $hex); $sh.Fill.Transparency=0
  $sh.Adjustments.Item(1)=0.5
  $sh.Left=($cx-$dpx/2)/2; $sh.Top=($cy-$dpx/2)/2; $sh.Width=$dpx/2; $sh.Height=$dpx/2 }
function Add-Mesa($s){
  $m=Add-Box $s '!!mesa' 1 1484 610 340 180 $script:SF $script:LN 3
  $tf=$m.TextFrame; $tf.TextRange.Text="mesa`rsupervisão"; $tf.WordWrap=0; $m.TextFrame2.MarginLeft=0; $m.TextFrame2.MarginRight=0
  $tf.TextRange.ParagraphFormat.Alignment=2; $tf.VerticalAnchor=3
  $p1=$tf.TextRange.Paragraphs(1); $p1.Font.Name=$script:F_COND; $p1.Font.Bold=-1; $p1.Font.Size=28; $p1.Font.Color.RGB=(Get-Rgb $script:TX)
  $p2=$tf.TextRange.Paragraphs(2); $p2.Font.Name=$script:F_LIGHT; $p2.Font.Bold=0; $p2.Font.Size=28; $p2.Font.Color.RGB=(Get-Rgb $script:T2)
  $m }
function Add-Card($s,$name,$text,$x,$y,$w,$h){
  $m=Add-Box $s $name 1 $x $y $w $h $script:SF $script:LN 3
  $r=$m.TextFrame.TextRange; $r.Text=$text; $r.Font.Name=$script:F_COND; $r.Font.Bold=-1; $r.Font.Size=28; $r.Font.Color.RGB=(Get-Rgb $script:TX); $r.ParagraphFormat.Alignment=2
  $m.TextFrame.VerticalAnchor=3; $m }
function Add-Parada($s,$name,$t1,$t2,$x,$y,$w,$h){
  $m=Add-Box $s $name 1 $x $y $w $h $script:SF $script:LN 3
  $m.TextFrame2.MarginLeft=0; $m.TextFrame2.MarginRight=0; $m.TextFrame.WordWrap=0
  $tf=$m.TextFrame; $tf.TextRange.Text="$t1`r$t2"; $tf.TextRange.ParagraphFormat.Alignment=2; $tf.VerticalAnchor=3
  $p1=$tf.TextRange.Paragraphs(1); $p1.Font.Name=$script:F_COND; $p1.Font.Bold=-1; $p1.Font.Size=28; $p1.Font.Color.RGB=(Get-Rgb $script:TX)
  $p2=$tf.TextRange.Paragraphs(2); $p2.Font.Name=$script:F_COND; $p2.Font.Bold=0; $p2.Font.Size=28; $p2.Font.Color.RGB=(Get-Rgb $script:T2)
  $m }
function Add-Estacao($s,$i,$x,$y){
  $m=Add-Box $s "!!e$i" 5 ($x-70) ($y-70) 140 140 $script:SF $script:LN 3 0
  $r=$m.TextFrame.TextRange; $r.Text="$i"; $r.Font.Name=$script:F_MONO; $r.Font.Bold=0; $r.Font.Size=28; $r.Font.Color.RGB=(Get-Rgb $script:T2); $r.ParagraphFormat.Alignment=2
  $m.TextFrame.VerticalAnchor=3; $m.TextFrame2.MarginLeft=0; $m.TextFrame2.MarginRight=0; $m }

# Regra: cada arco do fio tem a MESMA caixa nos dois slides de uma transicao; so os angulos mudam.
function Fio-1d($s,[double]$dx,[double]$dy){ $B=$script:CH[0]
  $null=Add-FioArc $s '!!fioA3' 1600 $dy ($dx-1600) ($dy-$W) 270 271 $B
  $null=Add-FioLine $s '!!fioL1' 680 $W 1640 $W $B }
function Fio-1e($s,[double]$dx,[double]$dy){ $B=$script:CH[0]
  $null=Add-FioArc $s '!!fioA3' 1600 $dy ($dx-1600) ($dy-$W) 270 359 $B
  $null=Add-FioLine $s '!!fioL1' 680 $W 1600 $W $B }
# slides 3 e 4: arcos primeiro (ficam atras); no slide 3 as linhas cobrem os vaos e o laco tem abertura de 1 grau na ponta esquerda
function Fio-34($s,[bool]$ext){
  $B=$script:CH[0]; $a0= if($ext){179}else{0}
  foreach($k in 1..3){ $null=Add-FioArc $s "!!fioA$k" (160+400*$k) $W 60 105 $a0 180 $B }
  $e1= if($ext){620}else{500}; $e2= if($ext){1020}else{900}; $e3= if($ext){1420}else{1300}
  $null=Add-FioLine $s '!!fioL1' 320 $W $e1 $W $B
  $null=Add-FioLine $s '!!fioL2' 620 $W $e2 $W $B
  $null=Add-FioLine $s '!!fioL3' 1020 $W $e3 $W $B
  $null=Add-FioLine $s '!!fioL4' 1420 $W 1600 $W $B }
function Fio-5($s){
  $B=$script:CH[0]
  $null=Add-FioLine $s '!!fioL1' 96 420 1500 420 $B 5
  $null=Add-FioArc $s '!!fioA1' 1500 560 220 140 270 90 $B 5
  $null=Add-FioLine $s '!!fioL2' 1500 700 96 700 $B 5 }
function Notes($s,$id){ Set-Notes $s $rot[$id] }

$null=New-GmsDeck
try {
  # ---- 1a ----
  $s=New-GmsSlide
  $null=Add-Ficha $s 660 100 600
  Add-Campos $s 660 100 600 1
  Add-FichaNumeros $s 660 100 600 $script:INK $false
  Add-Marcas $s 660 100 600
  $null=Reel-Small $s '1a'; Notes $s '1a'

  # ---- 1b ----
  $s=New-GmsSlide
  $null=Add-Ficha $s 210 -260 1500
  Add-Campos $s 210 -260 1500 0.78
  Add-FichaNumeros $s 210 -260 1500 $script:TX $true
  Add-Marcas $s 210 -260 1500
  $null=Reel-Small $s '1b'; Notes $s '1b'

  # ---- 1c ----
  $s=New-GmsSlide
  $null=Add-Ficha $s 120 240 400
  for($i=0;$i -lt 4;$i++){ $null=Add-Txt $s "!!n$($i+1)" $FV[$i] $NX[$i] (560+$NDY[$i]) 92 @{font=$script:F_HAND;color=$script:TX;align='m';round=$BLUE;glow=$BLUE} }
  $null=Reel-Small $s '1c'; Notes $s '1c'

  # ---- 1d ----
  $s=New-GmsSlide
  $null=Add-Ficha $s 120 240 400 0.45
  $d=Dot-At 1800 985 62 $FRAC['1e']; Fio-1d $s ([Math]::Round($d.x,1)) ([Math]::Round($d.y,1))
  for($i=0;$i -lt 4;$i++){ $n=Add-Txt $s "!!n$($i+1)" $FV[$i] $NX[$i] (560+$NDY[$i]) 92 @{font=$script:F_HAND;color=$script:TX;align='m';round=$BLUE}; To-Dot $n $NX[$i] $W 32 $BLUE }
  $null=Add-Box $s '!!pontaFio' 9 1626 686 28 28 $script:RED $null
  $null=Reel-Small $s '1d'; Notes $s '1d'

  # ---- 1e ----
  $s=New-GmsSlide
  $null=Add-Ficha $s 120 240 400 0.3
  $d=Dot-At 1800 985 62 $FRAC['1e']; $dx=[Math]::Round($d.x,1); $dy=[Math]::Round($d.y,1)
  Fio-1e $s $dx $dy
  for($i=0;$i -lt 4;$i++){ $n=Add-Txt $s "!!n$($i+1)" $FV[$i] $NX[$i] (560+$NDY[$i]) 92 @{font=$script:F_HAND;color=$script:TX;align='m';round=$BLUE}; To-Dot $n $NX[$i] $W 32 $BLUE }
  $null=Reel-Small $s '1e'
  $null=Add-Box $s '!!pontaFio' 9 ($dx-8.5) ($dy-8.5) 17 17 $script:RED $null
  Notes $s '1e'

  # ---- 2 (capa) ----
  $s=New-GmsSlide
  $null=Add-Reel $s 500 540 280 $FRAC['2']
  $null=Add-Box $s 'placa_logo' 1 1484 96 340 190 '#FFFFFF' $null
  $lg=$s.Shapes.AddPicture((Join-Path $root 'assets\unisal_logo.png'),0,-1,1504/2,116/2,300/2,150/2); $lg.Name='logo_unisal'
  $null=Add-Txt $s 'titulo_tcc' 'Digitalização de Processos em Manufatura Multinacional: Implementação de um Sistema de Execução de Manufatura via Ecossistema Low-Code' 880 380 64 @{font=$script:F_COND;bold=$true;wrap=944}
  $null=Add-Txt $s 'autor' 'William Nathan Ribeiro de Amorim' 880 722 56 @{wrap=944}
  $null=Add-Txt $s 'curso' 'Engenharia da Computação · UNISAL' 880 794 56 @{color=$script:T2;wrap=944}
  $null=Add-Txt $s 'sistema' 'Guaratinguetá Manufacturing System' 880 897 56 @{font=$script:F_SEMI;color=$BLUE;wrap=760}
  Notes $s '2'

  # ---- 3 ----
  $s=New-GmsSlide
  Fio-34 $s $true
  $null=Add-Ficha $s 96 590 180
  $null=Add-Mesa $s
  $null=Add-Txt $s '!!numero' '1 a 2 dias' 960 520 260 @{font=$script:F_COND;bold=$true;align='m'}
  Add-Moldura $s 'O problema' $BLUE '' '3 / 28' 'seção 1'
  $null=Reel-Small $s '3'; Notes $s '3'

  # ---- 4 ----
  $s=New-GmsSlide
  Fio-34 $s $false
  $null=Add-Ficha $s 96 590 180
  $null=Add-Mesa $s
  $null=Add-Txt $s '!!numero' '1 a 2 dias' 340 650 56 @{font=$script:F_COND;bold=$true;color=$BLUE}
  $c1=Add-Parada $s 'parada_ficha' 'Ficha' '8 etapas' 376 360 368 160
  $c2=Add-Parada $s 'parada_xls' 'Excel' 'turno seguinte' 776 360 368 160
  $c3=Add-Parada $s 'parada_sap' 'SAP' 'lançamento' 1176 360 368 160
  Add-Moldura $s 'O problema' $BLUE 'O dado passava por {{três paradas}}' '4 / 28' 'seção 1, Figura 1'
  $null=Reel-Small $s '4'; Notes $s '4'
  Add-ClickFade $s @($c1)
  Add-ClickFade $s @($c2)
  Add-ClickFade $s @($c3)

  # ---- 5 ----
  $s=New-GmsSlide
  $xs=480,820,1160,1500
  Fio-5 $s
  $i=0; foreach($x in $xs){ $i++; $null=Add-Estacao $s $i $x 420 }
  $i=4; foreach($x in @(1500,1160,820,480)){ $i++; $null=Add-Estacao $s $i $x 700 }
  Add-Moldura $s 'O problema' $BLUE '{{Cegueira operacional}}' '5 / 28' '(JESUS et al., 2025; WU; XU; ZHENG, 2024)'
  $st=Add-Box $s 'carimbo' 1 1500 130 300 100 $null $script:SE 6
  $st.Rotation=-9
  $r=$st.TextFrame.TextRange; $r.Text='ONTEM'; $r.Font.Name=$script:F_COND; $r.Font.Bold=-1; $r.Font.Size=32; $r.Font.Color.RGB=(Get-Rgb $script:SE); $r.ParagraphFormat.Alignment=2
  $st.TextFrame.VerticalAnchor=3; $st.TextFrame2.TextRange.Font.Spacing=3
  $null=Add-Txt $s 'linha_oee' 'OEE: impossível. Achar uma OP fechada: uma manhã.' 96 860 56 @{color=$script:T2}
  $null=Reel-Small $s '5'; Notes $s '5'

  # ---- 6 ----
  $s=New-GmsSlide
  $dc=Mix-Hex $BLUE 0.35
  for($i=0;$i -lt 8;$i++){
    $m=Add-Box $s "!!e$($i+1)" 5 (114+$i*241.7-18) (420-18) 36 36 $dc $null 2 0.5
    $m.TextFrame.TextRange.Text='' }
  Add-Moldura $s 'O problema' $BLUE 'O dado já existia.' '6 / 28' 'seção 2.3 (WU; XU; ZHENG, 2024)'
  $t2=Add-Txt $s 'frase_custo' 'O custo era chegar até ele.' 96 600 72 @{}
  $t3=Add-Txt $s 'tres_palavras' 'tempo · visibilidade · conexão' 96 730 72 @{font=$script:F_SEMI;color=$BLUE}
  $null=Reel-Small $s '6'; Notes $s '6'
  Add-ClickFade $s @($t2)
  Add-ClickFade $s @($t3)

  # ---- transicoes, salvar ----
  foreach($sl in $script:pres.Slides){ $sl.SlideShowTransition.AdvanceOnClick=-1; $sl.SlideShowTransition.AdvanceOnTime=0 }
  Save-GmsDeck $pptx 1.2
  "salvo: $pptx"

  # ---- exportar a partir do arquivo ja com Morph ----
  $null=Open-GmsDeck $pptx
  Export-GmsSlides $prev
  "PNGs: $prev"
  $nviol=Test-GmsLayout -Except @{ 2=@('^!!(ficha|n\d|campo|marca)') } -Families @('^(!!ficha|!!n\d|!!campo|!!marca)','^(autor|curso)$','^(placa_logo|logo_unisal)$')
  "violacoes de layout: $nviol"
  "pdf: $(Export-GmsPdf (Join-Path $prev 'cap1.pdf'))"
  if(-not $SemVideo){
    $ok=Export-GmsVideo (Join-Path $prev 'cap1.mp4') 3 720 300
    "video: $ok"
  }
} finally { Close-GmsDeck }
