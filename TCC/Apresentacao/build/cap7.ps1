# cap7.ps1 - Capitulo 7 (FOREST CITY E O FUTURO, quadros 25a, 25b, 25c e 26 = 4 slides = slides 43 a 46).
# NAO regera os capitulos anteriores: abre GMS_Defesa.pptx (42 slides), apaga o que houver alem do 42 (idempotente), acrescenta os 4 slides, salva e exporta previa/cap7/.
# Uso (depois de cap1 a cap6):  powershell -NoProfile -ExecutionPolicy Bypass -File cap7.ps1 [-SemVideo]
# Globo de pontos so com ovais do PowerPoint (contorno das Americas escrito a mao, sem fonte externa); o fio de voo e um arco que cresce (mesma caixa, so o angulo final muda).
param([switch]$SemVideo)
$ErrorActionPreference='Stop'
. "$PSScriptRoot\gms_lib.ps1"
$root=(Resolve-Path "$PSScriptRoot\..").Path
$pptx=Join-Path $root 'GMS_Defesa.pptx'
$prev=Join-Path $root 'previa\cap7'
if(-not (Test-Path $pptx)){ throw 'GMS_Defesa.pptx nao existe: rode cap1 a cap6 antes.' }
$rot=Get-Roteiro (Join-Path $root 'roteiro.md')

# ATENCAO: nomes de variavel nao diferenciam maiusculas; nao use $BG, $RED, $GR, $TX, $T2, $CH, $LN, $SF (colidem com a lib).
$ORG=$script:CH[6]                 # laranja #F97316 (capitulo 7)
$ORGL='#FDBA74'                    # laranja claro (nos em construcao)
$MR=$script:CH[5]                  # vermelho #EF4444 (o mesmo dos marcadores do 42)
$DOTC='#64748B'                    # cinza azulado apagado (terra)
$LAST=42
$FR=@(0.25,0.5,0.75,1.0)
$CIT='seção 4.9, Quadro 8'
$CAP='Forest City e o futuro'

function Txt2($s,[string]$name,[string]$text,[double]$x,[double]$top,[double]$size,[hashtable]$o){   # posiciona pelo TOPO da caixa (px)
  Add-Txt $s $name $text $x ($top+$size*$script:ASC) $size $o }

# ---------- o globo: projecao ortografica centrada em lat 10, lon -57 ----------
$GCX=624; $GCY=580; $GRAD=310; $LAT0=10.0; $LON0=-57.0; $STEP=3.6
function Proj([double]$lat,[double]$lon){
  $la=$lat*[Math]::PI/180; $dl=($lon-$LON0)*[Math]::PI/180; $l0=$LAT0*[Math]::PI/180
  $cc=[Math]::Sin($l0)*[Math]::Sin($la)+[Math]::Cos($l0)*[Math]::Cos($la)*[Math]::Cos($dl)
  $px=$GRAD*[Math]::Cos($la)*[Math]::Sin($dl)
  $py=$GRAD*([Math]::Cos($l0)*[Math]::Sin($la)-[Math]::Sin($l0)*[Math]::Cos($la)*[Math]::Cos($dl))
  ,@(($GCX+$px),($GCY-$py),$cc) }

# contornos grosseiros, "lon,lat" em graus, escritos a mao (Americas, Groenlandia e as maiores ilhas do Atlantico)
$POLY=[ordered]@{
 NA='-168,65 -166,69 -156,71.5 -141,69.5 -128,70 -115,68 -105,68 -95,69 -90,68 -94,61 -93,58 -88,56 -82,55 -80,52 -79,55 -77,60 -78,62.5 -73,62 -70,60 -65,60 -62,57 -57,53 -56,51.5 -60,50 -66,50 -64,49 -60,46 -66,44 -70,43.5 -70,41.7 -74,40.5 -75.5,38 -76,35 -78,34 -81,31.5 -80,27 -80,25.2 -82,26.5 -82.8,29 -84,30 -86,30.3 -89,30 -90,29 -94,29.5 -97,27 -97.5,24 -97.5,22 -97,21 -96,19 -94.5,18.2 -91,18.8 -90.5,21 -87,21.5 -87.5,18 -88,16 -88,15.8 -84,15.8 -83.2,15 -83.5,11 -81.5,9 -79,9.5 -77.5,8.5 -78,7.5 -80.5,7.2 -83,8.2 -85.7,10 -87.5,13 -91.5,14 -94.5,16 -98,16 -102,18 -105.5,20 -105.5,21.5 -109.5,23 -112,26 -115,29.5 -117,32.5 -120.5,34.5 -122.5,37.5 -124,40.5 -124.5,46 -124.5,48.3 -123,49 -127,51 -130,54.5 -134,57.5 -138,59 -145,60.5 -150,59.5 -154,57.5 -158,56 -163,55 -160,58.5 -165,61 -166,64'
 SA='-77.5,8.5 -75.5,10.5 -72,12 -71.5,10.5 -68,10.5 -64,10.6 -61,10.5 -60,8.5 -57,6 -52,5 -50,1.5 -50,0 -48,-1 -44,-2.5 -40,-3 -35,-5.2 -34.8,-8 -37,-12 -39,-15 -39.5,-18 -41,-22 -44,-23 -48,-25.5 -48.7,-28.5 -52,-32 -54,-34.5 -57,-35 -57.5,-38 -62,-39 -65,-41 -65,-45 -67.5,-46.5 -66,-48 -69,-51.5 -68.5,-53 -72,-53.5 -74.5,-51 -75.5,-47 -73.7,-42 -73.5,-37 -71.5,-32 -71.5,-28 -70.3,-23 -70.3,-18.5 -76,-14 -79,-8 -81.2,-5 -80,-2.5 -80,0 -79,2 -77.5,4 -77.5,7'
 GR='-73,78 -60,82 -35,83.5 -20,81 -18,76 -22,70 -31,68 -40,65 -43,60 -48,61 -52,65 -54,69 -58,75 -68,76.5'
 BAF='-89,73 -80,73.8 -70,71 -62,67 -65,63 -72,64 -78,64.5 -74,67 -85,70'
 CUB='-85,22 -82,23.2 -78,22.8 -74.2,20.3 -77.5,19.8 -80,21.7 -84,21.8'
 HIS='-74.4,19.8 -72,19.9 -68.4,18.8 -68.5,18.2 -71.5,17.7 -74.4,18.4'
 NFL='-59,47.5 -53,46.7 -52.8,49.5 -55.5,51.6 -59,49'
}
$PXS=@(); $PYS=@()
foreach($k in $POLY.Keys){
  $pr=@($POLY[$k].Split(' ',[StringSplitOptions]::RemoveEmptyEntries))
  $xa=New-Object 'double[]' $pr.Count; $ya=New-Object 'double[]' $pr.Count
  for($i=0;$i -lt $pr.Count;$i++){ $c=$pr[$i].Split(','); $xa[$i]=[double]$c[0]; $ya[$i]=[double]$c[1] }
  $PXS+=,$xa; $PYS+=,$ya }
function Test-Land([double]$lon,[double]$lat){
  for($p=0;$p -lt $PXS.Count;$p++){
    $xa=$PXS[$p]; $ya=$PYS[$p]; $n=$xa.Length; $inside=$false; $j=$n-1
    for($i=0;$i -lt $n;$i++){
      if(($ya[$i] -gt $lat) -ne ($ya[$j] -gt $lat)){
        $xi=($xa[$j]-$xa[$i])*($lat-$ya[$i])/($ya[$j]-$ya[$i])+$xa[$i]
        if($lon -lt $xi){ $inside=-not $inside } }
      $j=$i }
    if($inside){ return $true } }
  return $false }
$DOTS=New-Object System.Collections.ArrayList
for($lat=-56.0; $lat -le 84.0; $lat+=$STEP){
  for($lon=-170.0; $lon -le -10.0; $lon+=$STEP){
    if(Test-Land $lon $lat){
      $q=Proj $lat $lon
      if($q[2] -gt 0.12){ $d=7+5*[Math]::Min(1.0,$q[2]/0.5); $null=$DOTS.Add(@($q[0],$q[1],$d)) } } } }
"pontos de terra: $($DOTS.Count)"

function Add-Globo($s){
  $null=Add-Box $s '!!globo' 9 ($GCX-$GRAD) ($GCY-$GRAD) (2*$GRAD) (2*$GRAD) $script:BG '#3A4553' 2
  for($i=0;$i -lt $DOTS.Count;$i++){ $q=$DOTS[$i]; $null=Add-Box $s ("!!tr{0}" -f $i) 9 ($q[0]-$q[2]/2) ($q[1]-$q[2]/2) $q[2] $q[2] $DOTC $null } }

# Guaratingueta e Forest City (Carolina do Norte) no globo; o fio de voo e um arco de circulo (raio 250) que sai de Guaratingueta e chega a Forest City
$G=Proj (-22.7) (-45.2); $F=Proj 35.3 (-81.9)
$dx=$F[0]-$G[0]; $dy=$F[1]-$G[1]; $L=[Math]::Sqrt($dx*$dx+$dy*$dy); $ux=$dx/$L; $uy=$dy/$L
$RF=250; $dd=[Math]::Sqrt($RF*$RF-($L/2)*($L/2))
$AX=($G[0]+$F[0])/2+$dd*(-$uy); $AY=($G[1]+$F[1])/2+$dd*$ux     # centro do arco: o fio abaulha para o lado oeste
$A0=[Math]::Atan2($G[1]-$AY,$G[0]-$AX)*180/[Math]::PI; if($A0 -lt 0){ $A0+=360 }
$A1=[Math]::Atan2($F[1]-$AY,$F[0]-$AX)*180/[Math]::PI; if($A1 -lt 0){ $A1+=360 }; if($A1 -le $A0){ $A1+=360 }
$A0=[Math]::Round($A0,2); $A1=[Math]::Round($A1,2)
"fio de voo: centro ($([int]$AX),$([int]$AY)) raio $RF angulos $A0 -> $A1; G=($([int]$G[0]),$([int]$G[1])) FC=($([int]$F[0]),$([int]$F[1]))"
function Add-Voo($s,[double]$fim){ $null=Add-FioArc $s '!!fioVoo' $AX $AY $RF $RF $A0 $fim $ORG 6 }
function Add-Marc($s){ for($n=1;$n -le 4;$n++){ $null=Add-Box $s "!!marc$n" 5 ($G[0]-11) ($G[1]-11) 22 22 $MR $null 1 0.5 } }
function Add-PontoFC($s){ $null=Add-Box $s '!!pFC' 5 ($F[0]-11) ($F[1]-11) 22 22 $ORG $null 1 0.5 }
function Add-RotuloFC($s){
  $b=Add-Txt $s '!!lblFC' ("Forest City,`rCarolina do Norte") 562 (412+56*$script:ASC) 56 @{font=$script:F_COND;bold=$true;color=$script:TX}
  $pf=$b.TextFrame.TextRange.ParagraphFormat; $pf.LineRuleWithin=-1; $pf.SpaceWithin=0.9
  $b.TextFrame.TextRange.Characters(1,12).Font.Color.RGB=(Get-Rgb $ORG) }

# ---------- etiquetas (45) e nos (46) ----------
$ETX=@(972,1414,972,1414,972,1414); $ETW=410; $ETH=184
$ETY=@(260,260,476,476,692,692)
$ETT=@('Data','Decimal','Fuso','Idioma','Turnos','ERP')
$CARDH=130; $CARDW=322; $CARDWL=340
$RT=@(260,422,584,746)                      # topo das quatro fileiras de cartoes
$RC=@(325,487,649,811)                      # centro das fileiras
# destino de cada etiqueta (coluna 3 = x 1148, coluna 4 = x 1502) e texto do no
$DEST=@(@{x=1148;y=584;t='Modo offline'},@{x=1502;y=260;t='Sensores nas máquinas'},@{x=1148;y=746;t='IA da plataforma'},
        @{x=1502;y=422;t='Dataverse'},@{x=1502;y=746;t='Programação detalhada'},@{x=1502;y=584;t='Genealogia entre lotes'})
$NOVOS=@(@{x=96;y=260;t='Integração direta com o ERP';c=$false},@{x=96;y=422;t='OEE por hora';c=$true},
         @{x=96;y=584;t=('Simulador de demanda × pessoas' -replace ' × ',([string][char]0xA0+'×'+[char]0xA0));c=$true})
$LIT=@(@{n=1;side='L';row=0;ang=247.5;t='Manufatura'},@{n=2;side='R';row=0;ang=292.5;t='Qualidade'},
       @{n=3;side='L';row=1;ang=202.5;t='Planejamento'},@{n=4;side='R';row=1;ang=337.5;t='Logística'},
       @{n=5;side='L';row=2;ang=157.5;t='Engenharia'})
$LNX=776; $RNX=1144; $CX=960; $CY=580; $RN=140

function Add-TxtNaCaixa($s,[string]$name,[string]$text,[double]$x,[double]$y,[double]$w,[double]$h,[double]$size,[string]$cor){
  $b=Add-Txt $s $name $text ($x+16) (0+$size*$script:ASC) $size @{font=$script:F_COND;bold=$true;color=$cor;align='m';wrap=($w-24)}
  $pf=$b.TextFrame.TextRange.ParagraphFormat; $pf.LineRuleWithin=-1; $pf.SpaceWithin=0.9
  $b.Left=($x+$w/2)/2-$b.Width/2; $b.Top=($y+$h/2)/2-$b.Height/2; $b }

$null=Open-GmsDeckForAppend $pptx
try {
  if($script:pres.Slides.Count -lt $LAST){ throw "o deck tem menos de $LAST slides: rode cap1 a cap6." }
  while($script:pres.Slides.Count -gt $LAST){ $script:pres.Slides.Item($script:pres.Slides.Count).Delete() }   # idempotente
  $script:slideN=$LAST

  # ---- 43 (25a): o globo de pontos; os quatro marcadores do 42 recolhem num ponto vermelho em Guaratingueta ----
  $s=New-GmsSlide
  Add-Globo $s
  Add-Voo $s ($A0+1)                      # toco de 1 grau, escondido sob o ponto
  Add-Marc $s
  Add-Moldura $s $CAP $ORG 'Tudo isto nasceu em {{Guaratinguetá}}.' '25 / 28' $CIT
  $null=Add-ReelCap $s 1800 985 62 7 $FR[0]; Set-Notes $s $rot['25a']

  # ---- 44 (25b): o fio sobe em arco e pousa em Forest City ----
  $s=New-GmsSlide
  Add-Globo $s
  Add-Voo $s $A1
  Add-Marc $s
  Add-PontoFC $s
  Add-RotuloFC $s
  Add-Moldura $s $CAP $ORG 'A próxima etapa é {{Forest City}}.' '25 / 28' $CIT
  $null=Add-ReelCap $s 1800 985 62 7 $FR[1]; Set-Notes $s $rot['25b']

  # ---- 45 (25c): seis etiquetas (o que deu defeito aqui) na metade direita ----
  $s=New-GmsSlide
  Add-Globo $s
  Add-Voo $s $A1
  Add-Marc $s
  Add-PontoFC $s
  Add-RotuloFC $s
  for($i=0;$i -lt 6;$i++){
    $null=Add-Box $s "!!et$($i+1)" 5 $ETX[$i] $ETY[$i] $ETW $ETH $script:BG $ORG 4 0.12 }
  for($i=0;$i -lt 6;$i++){
    $null=Add-TxtNaCaixa $s "!!et$($i+1)t" $ETT[$i] $ETX[$i] $ETY[$i] $ETW $ETH 88 $script:TX }
  Add-Moldura $s $CAP $ORG 'O que deu defeito aqui virou {{requisito}} lá.' '25 / 28' $CIT
  $null=Add-ReelCap $s 1800 985 62 7 $FR[2]; Set-Notes $s $rot['25c']

  # ---- 46 (26): a rede do capitulo 4 volta, com os nos tracejados nomeados ----
  $s=New-GmsSlide
  # fios (por baixo do anel): nascem de um toco sob o anel e esticam ate o no
  foreach($q in $LIT){
    $nx= if($q.side -eq 'L'){$LNX}else{$RNX}; $ny=$RC[$q.row]
    $a=$q.ang*[Math]::PI/180
    $null=Add-FioLine $s "!!fio$($q.n)" ($CX+$RN*[Math]::Cos($a)) ($CY+$RN*[Math]::Sin($a)) $nx $ny $ORG 6 }
  # as cinco pontas acesas: so o titulo
  foreach($q in $LIT){
    $ny=$RC[$q.row]
    if($q.side -eq 'L'){ $null=Txt2 $s "!!pt$($q.n)" $q.t ($LNX-18-32) ($ny-34) 56 @{font=$script:F_COND;bold=$true;color=$script:TX;align='r'} }
    else               { $null=Txt2 $s "!!pt$($q.n)" $q.t ($RNX+18+32) ($ny-34) 56 @{font=$script:F_COND;bold=$true;color=$script:TX} }
    $nx= if($q.side -eq 'L'){$LNX}else{$RNX}
    $null=Add-Box $s "!!nd$($q.n)" 5 ($nx-18) ($ny-18) 36 36 $ORG $null 1 0.5 }
  # as seis etiquetas viajam para seis nos tracejados (sete do futuro: traco normal) e trocam o texto
  $CNO=Mix-Hex $ORG 0.6
  for($i=0;$i -lt 6;$i++){
    $d=$DEST[$i]
    $b=Add-Box $s "!!et$($i+1)" 5 $d.x $d.y $CARDW $CARDH $script:BG $CNO 4 0.12; $b.Line.DashStyle=4 }
  for($i=0;$i -lt 6;$i++){
    $d=$DEST[$i]
    $null=Add-TxtNaCaixa $s "!!et$($i+1)t" $d.t $d.x $d.y $CARDW $CARDH 48 (Mix-Hex $script:TX 0.8) }
  # os outros tres nascem por fade; dois deles ja em construcao (traco mais forte e mais claro)
  for($i=0;$i -lt 3;$i++){
    $d=$NOVOS[$i]
    if($d.c){ $b=Add-Box $s "!!nt$($i+1)" 5 $d.x $d.y $CARDWL $CARDH $script:BG $ORGL 7 0.12; $cor=$script:TX }
    else    { $b=Add-Box $s "!!nt$($i+1)" 5 $d.x $d.y $CARDWL $CARDH $script:BG $CNO 4 0.12; $cor=(Mix-Hex $script:TX 0.8) }
    $b.Line.DashStyle=4
    $null=Add-TxtNaCaixa $s "tx$($i+1)" $d.t $d.x $d.y $CARDWL $CARDH 48 $cor }
  Add-Moldura $s $CAP $ORG 'O que {{fica por fazer}}.' '26 / 28' 'seção 5'
  $null=Add-ReelCap $s $CX $CY $RN 7 $FR[3]; Set-Notes $s $rot['26']

  foreach($sl in $script:pres.Slides){ $sl.SlideShowTransition.AdvanceOnClick=-1; $sl.SlideShowTransition.AdvanceOnTime=0 }
  Save-GmsDeck $pptx 1.2
  "salvo: $pptx"

  $null=Open-GmsDeck $pptx
  $idx=43..46
  Export-GmsSlides $prev 1920 1080 $idx
  "PNGs (slides 43 a 46, numeracao do deck): $prev"
  $famL=@('^(!!globo|!!lblFC|!!pFC|!!marc\d)$')
  for($i=1;$i -le 6;$i++){ $famL+="^!!et${i}t?$" }
  for($i=1;$i -le 3;$i++){ $famL+="^(!!nt$i|tx$i)$" }
  $nviol=Test-GmsLayout -Slides $idx -ExceptAll @('^!!tr\d+$') -Families $famL
  "violacoes de layout: $nviol"
  "pdf: $(Export-GmsPdf (Join-Path $prev 'cap7.pdf'))"
  if(-not $SemVideo){
    # video do slide 42 (ultimo do cap6) ao 46: copia temporaria sem os slides 1 a 41
    $tmp=Join-Path $env:TEMP 'gms_cap7_video.pptx'
    if(Test-Path $tmp){ Remove-Item $tmp -Force }
    $script:pres.SaveCopyAs($tmp)
    $orig=$script:pres
    $v=$script:app.Presentations.Open($tmp,0,0,0)
    for($i=1;$i -le 41;$i++){ $v.Slides.Item(1).Delete() }
    foreach($sl in $v.Slides){ $sl.SlideShowTransition.Hidden=0 }
    try{ $v.Slides.Item(1).SlideShowTransition.EntryEffect=0 }catch{}
    $script:pres=$v
    $ok=Export-GmsVideo (Join-Path $prev 'cap7.mp4') 3 720 1200
    "video: $ok"
    $v.Saved=-1; $v.Close(); $script:pres=$orig
    Remove-Item $tmp -Force -ErrorAction SilentlyContinue
  }
} finally { Close-GmsDeck }
