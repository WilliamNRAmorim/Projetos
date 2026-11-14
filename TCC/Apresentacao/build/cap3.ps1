# cap3.ps1 - Capitulo 3 (A CONSTRUCAO, quadros 11 a 15 = 10 slides: 11a-11d, 12, 13a-13c, 14, 15 = slides 15 a 24).
# NAO regera cap1 nem cap2: abre GMS_Defesa.pptx (14 slides), apaga o que houver alem do 14 (idempotente), acrescenta os 10 slides,
# salva (Save-GmsDeck reaplica o Morph) e exporta previa/cap3/.
# Uso (depois de cap1.ps1 e cap2.ps1):  powershell -NoProfile -ExecutionPolicy Bypass -File cap3.ps1 [-SemVideo]
# Mangueira: o COM desta maquina nao aceita Shapes.Add3DModel (erro "valor fora dos limites", ate com um .glb minimo),
# entao as 4 camadas entram como imagens (assets/pecas/pc_<camada>_{on,off}.png, geradas de assets/mangueira_*.png por
# assets/gerador/recortar_pecas.py). Cada camada e um objeto !!mg* com o mesmo nome em todos os slides: o Morph move a peca
# (montada, explodida, deitada na faixa) e faz fade entre a imagem apagada e a acesa.
param([switch]$SemVideo)
$ErrorActionPreference='Stop'
. "$PSScriptRoot\gms_lib.ps1"
$root=(Resolve-Path "$PSScriptRoot\..").Path
$pptx=Join-Path $root 'GMS_Defesa.pptx'
$prev=Join-Path $root 'previa\cap3'
$pecas=Join-Path $root 'assets\pecas'
if(-not (Test-Path $pptx)){ throw 'GMS_Defesa.pptx nao existe: rode cap1.ps1 e cap2.ps1 antes.' }
$rot=Get-Roteiro (Join-Path $root 'roteiro.md')

$IND=$script:CH[2]; $INDL='#A5B4FC'; $INDD='#312E81'; $CY=$script:CH[1]
$TOTAL=10                          # slides do capitulo; o arco indigo cresce de 1/10 a 10/10 de forma monotona
$script:k=0
function Frac { $script:k++; [double]$script:k/$TOTAL }

# ---------- pecas da mangueira ----------
$PC=@(  # nome, arquivo, corpo x0, corpo x1 (px nativos), largura da imagem recortada
  @{n='Terminal';  f='terminal';  b0=181;  b1=533;  w=443},
  @{n='Tubo';      f='tubo';      b0=566;  b1=935;  w=460},
  @{n='Tranca';    f='tranca';    b0=960;  b1=1327; w=458},
  @{n='Cobertura'; f='cobertura'; b0=1335; b1=1710; w=466})
$PAD=45; $CROPH=340; $AXIS=170     # recorte nativo: 45 px de folga de cada lado, 340 de altura, eixo a 170 do topo
function Add-Pic($s,[string]$name,[string]$file,[double]$x,[double]$y,[double]$w,[double]$h){
  $p=$s.Shapes.AddPicture($file,0,-1,[single]($x/2),[single]($y/2),[single]($w/2),[single]($h/2)); $p.Name=$name; $p }
# mode: 'ab' montada (corpos encostados), 'ex' explodida (centrada em $cols), 'faixa' montada, escala menor.
# ax = x do corpo esquerdo do terminal (ab/faixa); ay = y do eixo; sc = escala; on = 4 booleanos (camada acesa)
function Add-Pecas($s,[string]$mode,[double]$ax,[double]$ay,[double]$sc,[bool[]]$on,[double[]]$cols){
  $cursor=$ax
  for($i=0;$i -lt 4;$i++){
    $p=$PC[$i]; $bw=($p.b1-$p.b0+1)
    if($mode -eq 'ex'){ $bl=$cols[$i]-$bw*$sc/2 } else { $bl=$cursor; $cursor+=$bw*$sc }
    $st= if($on[$i]){'on'}else{'off'}
    $null=Add-Pic $s ("!!mg"+$p.n) (Join-Path $pecas ("pc_"+$p.f+"_"+$st+".png")) ($bl-$PAD*$sc) ($ay-$AXIS*$sc) ($p.w*$sc) ($CROPH*$sc) }
}

# ---------- textos ----------
function Add-Rot2($s,$name,$t1,$t2,[double]$x,[double]$top,$c1){   # titulo 72 px + linha de apoio 56 px cinza
  $t=Add-Txt $s $name "$t1`r$t2" $x ($top+72*$script:ASC) 72 @{font=$script:F_COND;bold=$true;color=$c1}
  $p2=$t.TextFrame.TextRange.Paragraphs(2); $p2.Font.Name=$script:F_LIGHT; $p2.Font.Bold=0; $p2.Font.Size=28; $p2.Font.Color.RGB=(Get-Rgb $script:T2); $t }

# ---------- slides do quadro 11 ----------
$COLS=@(303,741,1179,1617)         # centros das 4 colunas de 3 colunas da grade (414 px cada)
$LAB=@(@('Coleta','Power Apps'),@('Dados','Microsoft Lists'),@('Orquestração','Power Automate'),@('Análise','Power BI'))
function Add-Camadas($s,[bool[]]$on){
  for($i=0;$i -lt 4;$i++){
    $nc= if($on[$i]){$INDL}else{Mix-Hex $IND 0.6}; $tc= if($on[$i]){$script:TX}else{Mix-Hex $script:T2 0.6}
    $null=Add-Txt $s "!!lab$($PC[$i].n)" $LAB[$i][0] $COLS[$i] (275+72*$script:ASC) 72 @{font=$script:F_COND;bold=$true;color=$nc;align='m'}
    $null=Add-Txt $s "!!ferr$($PC[$i].n)" $LAB[$i][1] $COLS[$i] (725+56*$script:ASC) 56 @{color=$tc;align='m'} }
}

$offTL=@{}   # objetos fora da tela por completo (camera): ficam fora do teste de layout naquele slide
$null=Open-GmsDeckForAppend $pptx
try {
  if($script:pres.Slides.Count -lt 14){ throw 'o deck tem menos de 14 slides: rode cap1.ps1 e cap2.ps1.' }
  while($script:pres.Slides.Count -gt 14){ $script:pres.Slides.Item($script:pres.Slides.Count).Delete() }   # idempotente
  $script:slideN=14
  $FR11='Quatro camadas em {{uma mangueira}}.'

  # ---- 15 (11a): o tablet encolhe e vira o terminal da mangueira montada ----
  $s=New-GmsSlide
  $null=Add-FioLine $s '!!fioL1' 96 570 200 570 $CY 6
  $null=Add-Box $s '!!tablet' 5 200 490 240 160 $script:SF $script:T2 4 0.06
  $null=Add-Box $s '!!passagem' 1 214 504 212 132 '#0B1A22' $CY 4
  Add-Pecas $s 'ab' 440 570 0.92 @($true,$false,$false,$false) $null
  $null=Add-Box $s '!!pontaFio' 9 186 556 28 28 $script:RED $null
  $null=Add-Txt $s 'nota_terminal' 'Terminal: um tablet por estação' 200 (730+56*$script:ASC) 56 @{color=$script:TX}
  Add-Moldura $s 'A construção' $IND $FR11 '11 / 28' 'seção 3.3 e Quadro 2'
  $null=Add-ReelCap $s 1800 985 62 3 (Frac); Set-Notes $s $rot['11a']

  # ---- 16 a 18 (11b, 11c, 11d): vista explodida, uma camada acende por vez (acumulando) ----
  $steps=@(@('11b',@($true,$true,$false,$false)),@('11c',@($true,$true,$true,$false)),@('11d',@($true,$true,$true,$true)))
  foreach($st in $steps){
    $s=New-GmsSlide
    Add-Pecas $s 'ex' 0 565 1.05 $st[1] $COLS
    Add-Camadas $s $st[1]
    if($st[0] -eq '11c'){ $null=Add-Txt $s 'nota_calculo' 'O cálculo pesado não roda no tablet.' 960 (830+56*$script:ASC) 56 @{color=$script:TX;align='m'} }
    Add-Moldura $s 'A construção' $IND $FR11 '11 / 28' 'seção 3.3 e Quadro 2'
    $null=Add-ReelCap $s 1800 985 62 3 (Frac); Set-Notes $s $rot[$st[0]] }

  # ---- 19 (12): ISA-95, a mangueira fecha e deita na faixa do meio ----
  $s=New-GmsSlide
  $null=Add-Box $s 'faixa4' 1 96 260 1584 190 $script:SF $script:LN 3
  $null=Add-Box $s '!!faixa3' 1 96 485 1584 190 '#14163A' $IND 4
  $null=Add-Box $s 'faixa12' 1 96 710 1584 190 $script:SF $script:LN 3
  $null=Add-Rot2 $s 'lab_n4' 'NÍVEL 4 · SAP' 'planejamento da empresa' 128 278 (Mix-Hex $script:TX 0.55)
  $null=Add-Rot2 $s 'lab_n3' 'NÍVEL 3 · GMS' 'liga a célula ao SAP' 128 503 $INDL
  $null=Add-Rot2 $s 'lab_n12' 'NÍVEIS 1 E 2 · MÁQUINAS' 'ainda não alimentam o sistema' 128 728 (Mix-Hex $script:TX 0.4)
  Add-Pecas $s 'faixa' 900 580 0.5 @($true,$true,$true,$true) $null
  Add-Moldura $s 'A construção' $IND 'O dado nasce do {{apontamento do operador}}.' '12 / 28' 'seção 2.1 e Figura 2'
  $null=Add-ReelCap $s 1800 985 62 3 (Frac); Set-Notes $s $rot['12']

  # ---- 20 a 22 (13a, 13b, 13c): a faixa vira o fio da linha do tempo e a camera voa por ele ----
  $D=350
  $items=@(
    @{i=0;m=0;  t='Gemba Walk e início';        d='ago/2025'},
    @{i=1;m=2;  t='Primeiras telas em produção'; d='out/2025'},
    @{i=2;m=9;  t='A ficha sai';                d='mai/2026'},
    @{i=3;m=10; t='Qualificação';               d='jun a out/2026'},
    @{i=4;m=11; t='Norma escrita';              d=''},
    @{i=5;m=12; t='Kaizen Award';               d=''},
    @{i=6;m=13; t='Painel na TV';               d=''},
    @{i=7;m=14; t='Conferência com o SAP';      d=''})
  $tl=@(@{id='13a';base=120;lab=860},@{id='13b';base=-1564;lab=300},@{id='13c';base=-3380;lab=$null})
  foreach($T in $tl){
    $s=New-GmsSlide; $ix=$script:slideN; $off=@(); $b=$T.base
    function X([int]$m){ $b+$D*$m }
    $x0=(X 0); $x2=(X 2); $x9=(X 9); $x14=(X 14)
    $th=Add-Box $s '!!faixa3' 1 ($x0-24) 626 ($x14-$x0+24) 8 $IND $IND 1
    $null=Add-Box $s '!!barraDev' 1 $x0 590 ($x2-$x0) 80 '#0E7490' $CY 3
    $null=Add-Box $s '!!barraPar' 1 $x2 590 ($x9-$x2) 80 $INDD $IND 3
    $fu=Add-FioLine $s '!!fioFut' $x14 630 ($x14+280) 630 $IND 8; $fu.Line.DashStyle=4
    $null=Add-Box $s '!!pontaFio' 9 ($x14+266) 616 28 28 $script:RED $null
    if($T.lab -ne $null){ $null=Add-Txt $s '!!labPar' 'papel e digital em paralelo' $T.lab (602+56*$script:ASC) 56 @{color=$script:TX} }
    foreach($it in $items){
      $x=(X $it.m); $n=$it.i
      $null=Add-Box $s "!!mk$n" 9 ($x-16) 614 32 32 $INDL $null
      $w= if($n -eq 2){240}else{300}
      $null=Add-Txt $s "!!t$n" $it.t ($x-16) (340+60*$script:ASC) 60 @{font=$script:F_COND;bold=$true;wrap=$w}
      if($it.d){ $null=Add-Txt $s "!!d$n" $it.d ($x-16) (710+56*$script:ASC) 56 @{font=$script:F_MONO;color=$INDL} }
      if(($x-16) -ge 1920 -or ($x-16+$w) -le 96){ $off+="!!mk$n","!!t$n"; if($it.d){ $off+="!!d$n" } } }
    $offTL[$ix]='^('+(($off+'!!faixa3','!!barraDev','!!barraPar','!!fioFut','!!labPar') -join '|')+')$'
    $fg= if($T.id -eq '13c'){ 'Depois, {{consolidação e expansão}}.' } else { '{{Nove meses}} até a ficha sair.' }
    Add-Moldura $s 'A construção' $IND $fg '13 / 28' 'Figura 5 e seção 4.1'
    $null=Add-ReelCap $s 1800 985 62 3 (Frac); Set-Notes $s $rot[$T.id] }

  # ---- 23 (14): "2 x 7": os dois primeiros trechos viram as duas barras ----
  $s=New-GmsSlide
  $null=Add-Txt $s 'lab_dev' '2 meses desenvolvendo' 96 (320+56*$script:ASC) 56 @{color=$script:TX}
  $null=Add-Box $s '!!barraDev' 1 96 430 360 100 '#0E7490' $CY 3
  $null=Add-Txt $s 'lab_impl' '7 meses implantando' 96 (590+56*$script:ASC) 56 @{color=$script:TX}
  $null=Add-Box $s '!!barraPar' 1 96 690 1260 100 $INDD $IND 3
  $h=Add-Txt $s 'num_2x7' '2 × 7' 1130 (300+240*$script:ASC) 240 @{font=$script:F_COND;bold=$true;color=$script:TX}
  $h.TextFrame.TextRange.Characters(1,1).Font.Color.RGB=(Get-Rgb $CY); $h.TextFrame.TextRange.Characters(5,1).Font.Color.RGB=(Get-Rgb $INDL); $h.TextFrame.TextRange.Characters(3,1).Font.Color.RGB=(Get-Rgb $script:T2)
  Add-Moldura $s 'A construção' $IND 'A barreira foi a {{adoção}}, não a técnica.' '14 / 28' 'seção 2.5 e 4.6 (ATKIN et al., 2017)'
  $null=Add-ReelCap $s 1800 985 62 3 (Frac); Set-Notes $s $rot['14']

  # ---- 24 (15): as duas barras se dividem em tres cartoes ----
  $s=New-GmsSlide
  $cx=@(96,680,1264); $nm=@('!!barraDev','!!barraPar','!!card3')
  $gl=@('§','+','</>'); $ti=@('Norma escrita','Diário de decisões','Código versionado')
  for($i=0;$i -lt 3;$i++){
    $null=Add-Box $s $nm[$i] 1 $cx[$i] 330 560 470 $script:SF $IND 4
    $null=Add-Txt $s "glifo$($i+1)" $gl[$i] ($cx[$i]+40) (370+150*$script:ASC) 150 @{font=$script:F_MONO;color=$INDL}
    $null=Add-Txt $s "titulo_card$($i+1)" $ti[$i] ($cx[$i]+40) (620+72*$script:ASC) 72 @{font=$script:F_COND;bold=$true;wrap=480} }
  Add-Moldura $s 'A construção' $IND 'Low-code com {{disciplina de software}}.' '15 / 28' 'seções 3.5 e 3.6'
  $null=Add-ReelCap $s 1800 985 62 3 (Frac); Set-Notes $s $rot['15']

  foreach($sl in $script:pres.Slides){ $sl.SlideShowTransition.AdvanceOnClick=-1; $sl.SlideShowTransition.AdvanceOnTime=0 }
  Save-GmsDeck $pptx 1.2
  "salvo: $pptx"

  $null=Open-GmsDeck $pptx
  $idx=15..24
  Export-GmsSlides $prev 1920 1080 $idx
  "PNGs (slides 15 a 24, numeracao do deck): $prev"
  $exc=@{}; foreach($k2 in $offTL.Keys){ $exc[[int]$k2]=@($offTL[$k2]) }
  $nviol=Test-GmsLayout -Slides $idx -Except $exc -ExceptAll @('^!!mg') -Families @('^(!!tablet|!!passagem)','^(faixa|!!faixa3|lab_n|!!mg)','^(!!barra|!!labPar|!!faixa3|!!fioFut|!!mk)','^(!!barra|!!card|glifo|titulo_card)')
  "violacoes de layout: $nviol"
  "pdf: $(Export-GmsPdf (Join-Path $prev 'cap3.pdf'))"
  if(-not $SemVideo){
    # video do slide 14 (ultimo do cap2) ao 24: copia temporaria sem os slides 1 a 13
    $tmp=Join-Path $env:TEMP 'gms_cap3_video.pptx'
    if(Test-Path $tmp){ Remove-Item $tmp -Force }
    $script:pres.SaveCopyAs($tmp)
    $orig=$script:pres
    $v=$script:app.Presentations.Open($tmp,0,0,0)
    for($i=1;$i -le 13;$i++){ $v.Slides.Item(1).Delete() }
    try{ $v.Slides.Item(1).SlideShowTransition.EntryEffect=0 }catch{}
    $script:pres=$v
    $ok=Export-GmsVideo (Join-Path $prev 'cap3.mp4') 3 720 600
    "video: $ok"
    $v.Saved=-1; $v.Close(); $script:pres=$orig
    Remove-Item $tmp -Force -ErrorAction SilentlyContinue
  }
} finally { Close-GmsDeck }
